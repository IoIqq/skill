"""Safe deployment of generated FTB Quests into a live modpack folder.

The generator writes a clean, copy-ready ``<output_dir>/quests/`` tree (game
files only — ``data.json5``, ``chapter_groups.json5``, ``chapters/*.json5``,
``lang/<locale>/quests.json5``, plus the skill's ``.ftbq-cache/manifest.json5``).
This module copies that tree into the modpack's ``config/ftbquests/quests/``
folder WITHOUT blindly clobbering originals:

* additive files (``data.json5``, ``chapter_groups.json5``, ``lang``) are
  MERGED so the new content and the pack's existing content coexist in one
  file (requirement: "新的内容和原版内容放在一起");
* chapter files and the manifest that already exist in the target are backed
  up to a co-located ``.ftbq-backup/<ts>/`` mirror, then replaced;
* a plan/report flags every overwrite (⚠️) before anything is written, and
  nothing is written until the caller passes ``backup``-apply with consent.

``.ftbq-backup/`` is dot-prefixed, so FTB Quests' chapter scanner skips it
(same reason ``.ftbq-cache/`` is safe — see reference §14). Backups mirror the
original relative path verbatim, so file names never change and a backup is
trivial to find next to its replacement.

Only depends on the shared ``ftbq.*`` core (json5 / canonical / ids), never on
``scripts/``, so the deploy logic stays portable and unit-testable.

Public API:

    scan_root(source_root)              -> list[FileEntry]
    plan(source_root, target_root)      -> DeploymentPlan
    apply(plan, target_root, *, backup) -> DeployReport
    render_report(plan, report=None)    -> str

Merge helpers (also used directly by tests): ``merge_data``,
``merge_chapter_groups``, ``merge_lang``.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ftbq.canonical import canonical_json, dump_file
from ftbq.json5 import Json5Error, parse, to_plain
from ftbq.snbt import SnbtError, dump_file_snbt, parse_snbt_file

# File kinds the deployer knows how to handle. Anything else under the source
# root (other ``.ftbq-cache/`` analysis artifacts, ``.ftbq-backup/`` itself,
# unknown stray files) is skipped — only game-loadable files deploy.
KIND_DATA = "data"
KIND_CHAPTER_GROUPS = "chapter_groups"
KIND_CHAPTER = "chapter"
KIND_REWARD_TABLE = "reward_table"
KIND_LANG = "lang"
KIND_MANIFEST = "manifest"

_MERGEABLE = (KIND_DATA, KIND_CHAPTER_GROUPS, KIND_LANG)


# --------------------------------------------------------------------- model


@dataclass
class FileEntry:
    """One source file the deployer may copy into the target."""

    rel_path: str          # posix, relative to source_root
    plain: Any             # parsed Python value
    signature: str         # "sha256:<hex>" over canonical_json(plain)
    kind: str              # one of KIND_*


@dataclass
class PlannedFile:
    """A source file classified against the target."""

    entry: FileEntry
    action: str            # new | unchanged | merge | replace
    target_signature: str | None = None
    merged: Any = None                 # merged value (merge only)
    merge_stats: dict | None = None    # {added, kept, overridden} (merge only)
    quest_overlap: list[str] | None = None  # shared quest IDs (chapter replace)
    note: str = ""

    @property
    def rel_path(self) -> str:
        """Convenience accessor delegating to the wrapped FileEntry so call
        sites can read ``pf.rel_path`` directly."""
        return self.entry.rel_path

    @property
    def kind(self) -> str:
        """Convenience accessor delegating to the wrapped FileEntry."""
        return self.entry.kind


@dataclass
class DeploymentPlan:
    source_root: Path
    target_root: Path
    entries: list[PlannedFile] = field(default_factory=list)

    @property
    def overwrites(self) -> list[PlannedFile]:
        return [p for p in self.entries if p.action in ("merge", "replace")]


@dataclass
class DeployReport:
    ts: str                       # backup timestamp folder name
    counts: dict
    backups: list[dict]
    backup_dir: Path | None


# ----------------------------------------------------------------- scanning


def _read_text(path: Path) -> str:
    """utf-8-sig strips a leading BOM if present (community packs sometimes
    ship one). Superset of plain utf-8, so it also reads the skill's output."""
    return path.read_text(encoding="utf-8-sig")


def _load(path: Path) -> Any:
    """Parse a source/target quest file to a plain value, dispatching by
    extension: ``.snbt`` (1.20.1) via the SNBT parser, ``.json5`` (1.21+)
    via the JSON5 parser. utf-8-sig strips a stray BOM either way."""
    if path.suffix == ".snbt":
        return parse_snbt_file(path)
    return to_plain(parse(_read_text(path), filename=str(path)))


def _classify(rel: str) -> str | None:
    # The skill-internal manifest is always JSON5 (FTB Quests' scanner skips
    # ``.ftbq-cache/`` and only reads its own format), even for an SNBT pack.
    if rel == ".ftbq-cache/manifest.json5":
        return KIND_MANIFEST
    if rel.startswith(".ftbq-cache/") or rel.startswith(".ftbq-backup/"):
        return None  # analysis caches / prior backups — never deploy
    # Strip the on-disk extension (json5 for 1.21+, snbt for 1.20.1) and
    # classify by path. ``lang/`` only appears in JSON5 packs (1.20.1 has no
    # lang files — text is inline).
    if rel.endswith(".json5") or rel.endswith(".snbt"):
        base = rel.rsplit(".", 1)[0]
    else:
        return None
    if base == "data":
        return KIND_DATA
    if base == "chapter_groups":
        return KIND_CHAPTER_GROUPS
    if base.startswith("chapters/"):
        return KIND_CHAPTER
    if base.startswith("reward_tables/"):
        return KIND_REWARD_TABLE
    if base.startswith("lang/"):
        return KIND_LANG
    return None  # unknown — not deployed


def signature(plain: Any) -> str:
    """Whole-file fingerprint. Uses ``canonical_json`` (keeps ``id``, sorts
    keys) so two files that differ only in whitespace/key order compare as
    equal — a no-op re-deploy never reports a spurious overwrite."""
    return "sha256:" + hashlib.sha256(
        canonical_json(plain).encode("utf-8")).hexdigest()


def scan_root(root: Path | str) -> list[FileEntry]:
    """Walk every ``*.json5`` / ``*.snbt`` under ``root`` and return one
    FileEntry per deployable game file (skips caches, backups, and
    unparseable files)."""
    root = Path(root)
    entries: list[FileEntry] = []
    if not root.is_dir():
        return entries
    paths = sorted([*root.rglob("*.json5"), *root.rglob("*.snbt")])
    for path in paths:
        rel = path.relative_to(root).as_posix()
        kind = _classify(rel)
        if kind is None:
            continue
        try:
            plain = _load(path)
        except (Json5Error, SnbtError, OSError) as exc:
            print(f"warning: skipping {rel}: {exc}", file=sys.stderr)
            continue  # skip broken source files rather than abort the deploy
        entries.append(FileEntry(rel_path=rel, plain=plain,
                                  signature=signature(plain), kind=kind))
    return entries


# ------------------------------------------------------------------- merge


def _dict_merge_stats(target: dict, source: dict, merged: dict) -> dict:
    t_keys = set(target)
    s_keys = set(source)
    overridden = {k for k in (s_keys & t_keys) if merged.get(k) != target.get(k)}
    return {
        "added": len(s_keys - t_keys),
        "kept": len(t_keys - s_keys),
        "overridden": len(overridden),
    }


def _deep_merge(target: dict, source: dict) -> dict:
    """Source overrides target; nested dicts merge recursively so a skill
    ``data`` block adds keys without dropping the pack's nested settings."""
    out = dict(target)
    for k, v in source.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def merge_data(target: Any, source: Any) -> tuple[dict, dict]:
    """Deep-merge two ``data.json5`` objects. Returns (merged, stats)."""
    target = target if isinstance(target, dict) else {}
    source = source if isinstance(source, dict) else {}
    merged = _deep_merge(target, source)
    return merged, _dict_merge_stats(target, source, merged)


def merge_lang(target: Any, source: Any) -> tuple[dict, dict]:
    """Flat key union for ``lang/<locale>/quests.json5``. Source keys override
    (they are ``quest/chapter.<skill-hex>.*`` and only the skill owns those);
    the pack's keys for OTHER quests are preserved — the critical regression
    a blind copy would have destroyed."""
    target = target if isinstance(target, dict) else {}
    source = source if isinstance(source, dict) else {}
    merged = {**target, **source}
    return merged, _dict_merge_stats(target, source, merged)


def _group_id(g: dict) -> str:
    return str(g.get("id") or g.get("name") or "")


def merge_chapter_groups(target: Any, source: Any) -> tuple[dict, dict]:
    """Union of ``chapter_groups`` lists by id; source overrides on collision.
    Returns the full ``{"chapter_groups": [...]}`` object plus stats."""
    t_list = ((target or {}).get("chapter_groups") or []) if isinstance(target, dict) else []
    s_list = ((source or {}).get("chapter_groups") or []) if isinstance(source, dict) else []
    t_by_id: dict[str, dict] = {}
    order: list[str] = []
    for g in t_list:
        gid = _group_id(g)
        if gid and gid not in t_by_id:
            t_by_id[gid] = g
            order.append(gid)
    s_by_id: dict[str, dict] = {_group_id(g): g for g in s_list if _group_id(g)}
    merged_by_id = dict(t_by_id)
    for gid, g in s_by_id.items():
        if gid not in merged_by_id:
            order.append(gid)
        merged_by_id[gid] = g  # source overrides existing / appends new
    merged_list = [merged_by_id[gid] for gid in order if gid in merged_by_id]
    t_ids, s_ids = set(t_by_id), set(s_by_id)
    overridden = {gid for gid in (s_ids & t_ids) if s_by_id[gid] != t_by_id[gid]}
    stats = {"added": len(s_ids - t_ids), "kept": len(t_ids - s_ids),
             "overridden": len(overridden)}
    return {"chapter_groups": merged_list}, stats


_MERGE = {
    KIND_DATA: merge_data,
    KIND_CHAPTER_GROUPS: merge_chapter_groups,
    KIND_LANG: merge_lang,
}


# ------------------------------------------------------------- classification


def _quest_ids(chapter: Any) -> set[str]:
    if not isinstance(chapter, dict):
        return set()
    return {str(q.get("id")) for q in (chapter.get("quests") or [])
            if isinstance(q, dict) and q.get("id")}


def plan(source_root: Path | str, target_root: Path | str) -> DeploymentPlan:
    """Classify every source game file against what already lives in the
    target. Does not write anything — safe to call for a preview."""
    source_root = Path(source_root)
    target_root = Path(target_root)
    entries: list[PlannedFile] = []
    for entry in scan_root(source_root):
        target_path = target_root / entry.rel_path
        if not target_path.exists():
            entries.append(PlannedFile(entry=entry, action="new"))
            continue
        try:
            t_plain = _load(target_path)
        except (Json5Error, SnbtError, OSError):
            # Can't merge into a broken file — back it up and replace.
            entries.append(PlannedFile(entry=entry, action="replace",
                                         note="target unparseable"))
            continue
        t_sig = signature(t_plain)
        if t_sig == entry.signature:
            entries.append(PlannedFile(entry=entry, action="unchanged",
                                         target_signature=t_sig))
            continue
        if entry.kind in _MERGEABLE:
            merged, stats = _MERGE[entry.kind](t_plain, entry.plain)
            entries.append(PlannedFile(entry=entry, action="merge",
                                         target_signature=t_sig,
                                         merged=merged, merge_stats=stats))
        else:  # chapter, manifest
            overlap = sorted(_quest_ids(entry.plain) & _quest_ids(t_plain)) \
                if entry.kind == KIND_CHAPTER else None
            entries.append(PlannedFile(entry=entry, action="replace",
                                         target_signature=t_sig,
                                         quest_overlap=overlap))
    return DeploymentPlan(source_root=source_root, target_root=target_root,
                           entries=entries)


# ------------------------------------------------------------------- apply


def _utc_stamp() -> str:
    """Compact, filesystem-safe timestamp for the backup folder name."""
    return (_dt.datetime.now(_dt.timezone.utc)
            .strftime("%Y%m%dT%H%M%SZ"))


def _utc_now() -> str:
    return (_dt.datetime.now(_dt.timezone.utc)
            .isoformat(timespec="seconds").replace("+00:00", "Z"))


def backup_file(target_root: Path, rel_path: str, ts: str) -> Path:
    """Copy ``target_root/rel_path`` to the ``.ftbq-backup/<ts>/`` mirror,
    preserving the relative path (and name) verbatim."""
    src = target_root / rel_path
    dst = target_root / ".ftbq-backup" / ts / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def _emit_merged(path: Path, kind: str, merged: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Emit in the target file's on-disk format: ``.snbt`` for 1.20.1 packs,
    # ``.json5`` for 1.21+. Lang keys contain dots (quest.<HEX>.title) and
    # only exist in JSON5 packs, so they stay quoted JSON5.
    if path.suffix == ".snbt":
        dump_file_snbt(path, merged)
    elif kind == KIND_LANG:
        dump_file(path, merged, quote_keys=True)
    else:
        dump_file(path, merged)


def apply(plan: DeploymentPlan, target_root: Path | str,
          *, backup: bool = True) -> DeployReport:
    """Execute a plan: copy new files, merge additive files, back up + replace
    chapters/manifest. Returns a report with backup locations. No confirmation
    here — the caller decides whether to call this (``--yes``)."""
    target_root = Path(target_root)
    target_root.mkdir(parents=True, exist_ok=True)
    ts = _utc_stamp()
    backups: list[dict] = []
    counts = {"new": 0, "merge": 0, "replace": 0, "unchanged": 0}

    for pf in plan.entries:
        src_path = plan.source_root / pf.rel_path
        dst_path = target_root / pf.rel_path

        if pf.action == "unchanged":
            counts["unchanged"] += 1
            continue

        if pf.action == "new":
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)
            counts["new"] += 1
            continue

        # merge / replace: the target file exists — back it up first.
        if backup:
            bpath = backup_file(target_root, pf.rel_path, ts)
            backups.append({
                "rel_path": pf.rel_path,
                "kind": pf.kind,
                "reason": pf.action,
                "backup_path": bpath.as_posix(),
                "original_signature": pf.target_signature,
                "replaced_by_signature": pf.entry.signature,
            })

        if pf.action == "merge" and pf.merged is not None:
            _emit_merged(dst_path, pf.kind, pf.merged)
            counts["merge"] += 1
        else:  # replace — copy the skill's exact bytes verbatim
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)
            counts["replace"] += 1

    backup_dir: Path | None = None
    if backups:
        backup_dir = target_root / ".ftbq-backup" / ts
        backup_dir.mkdir(parents=True, exist_ok=True)
        dump_file(backup_dir / "BACKUP_INDEX.json5", {
            "backed_up_at": _utc_now(),
            "source_root": plan.source_root.as_posix(),
            "target_root": target_root.as_posix(),
            "entries": backups,
        }, key_order=["backed_up_at", "source_root", "target_root", "entries"],
           per_path_key_order={"entries.[]": [
               "rel_path", "kind", "reason", "backup_path",
               "original_signature", "replaced_by_signature"]})
    return DeployReport(ts=ts, counts=counts, backups=backups,
                        backup_dir=backup_dir)


# ------------------------------------------------------------------ report


def _describe(pf: PlannedFile) -> str:
    if pf.action == "merge":
        s = pf.merge_stats or {}
        return (f"(merge: +{s.get('added', 0)} keys, "
                f"keeps {s.get('kept', 0)}, "
                f"overrides {s.get('overridden', 0)})")
    if pf.action == "replace":
        if pf.note:
            return f"(full replace — {pf.note})"
        if pf.kind == KIND_MANIFEST:
            return "(skill memory, replace)"
        if pf.kind == KIND_CHAPTER:
            ov = pf.quest_overlap or []
            n = f"{len(ov)}" if ov else "none"
            return f"(full replace; quest-ID overlap: {n})"
        if pf.kind == KIND_REWARD_TABLE:
            return "(full replace; reward table)"
        return "(full replace)"
    return ""


def render_report(plan: DeploymentPlan,
                  report: DeployReport | None = None) -> str:
    """Render the deploy plan (and, after apply, the outcome). The ⚠️ OVERWRITE
    block is the prominent highlight for files that touch modpack originals."""
    lines: list[str] = [
        "📦 FTB Quests deploy plan",
        f"   source: {plan.source_root}",
        f"   target: {plan.target_root}",
        "",
    ]
    new = [p for p in plan.entries if p.action == "new"]
    over = plan.overwrites
    unc = [p for p in plan.entries if p.action == "unchanged"]

    if new:
        lines.append(f"🆕 NEW ({len(new)}, safe to add):")
        for p in new:
            lines.append(f"   {p.rel_path}")
    if over:
        lines.append("")
        lines.append("⚠️  OVERWRITE — REPLACES modpack originals "
                     "(backup → .ftbq-backup/<ts>/):")
        for p in over:
            lines.append(f"   {p.rel_path}   {_describe(p)}")
    if unc:
        lines.append("")
        lines.append(f"✅ UNCHANGED ({len(unc)}, skip): "
                     + ", ".join(p.rel_path for p in unc))
    lines.append("")
    lines.append(f"📊 {len(new)} new, {len(over)} overwrite (backed up), "
                 f"{len(unc)} unchanged")
    if report is None:
        if over:
            lines.append("   Re-run with --yes to apply. "
                         "Backups will land under "
                         f"{plan.target_root}/.ftbq-backup/<timestamp>/")
        else:
            lines.append("   No overwrites — safe to apply with --yes "
                         "(or already in sync).")
    else:
        if report.backup_dir:
            lines.append(f"   ✅ Applied. Backups: {report.backup_dir}")
        else:
            lines.append("   ✅ Applied. No backups needed.")
    return "\n".join(lines)
