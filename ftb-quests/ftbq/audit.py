"""Audit index for FTB Quests packs — cache file checksums + description
item-ID patterns so repeat invocations skip the full scan.

Mirrors the codegraph-context ``analyze → status → query`` flow: build an
index once per pack, check freshness (stat each file, compare size+mtime),
and compute the DLC-source vs installed diff (Task A) + the description
``&e<item_id><中文名>&r`` pattern report (Task B) as cheap queries against
two cached indexes. Only files that actually changed trigger a rebuild.

Output: ``<quests_dir>/.ftbq-cache/audit_index.json5`` per pack.

Public API:

    build_audit_index(quests_dir)            -> dict
    check_freshness(quests_dir, cached)      -> (is_fresh, changed_files)
    diff_indexes(a, b)                       -> dict        # Task A
    item_report(index)                       -> dict        # Task B
    load_index(quests_dir)                   -> dict | None
    write_index(quests_dir, index)           -> None
    pack_pair_path(dlc_quests_dir)           -> Path
    load_pack_pair(dlc_quests_dir)           -> dict | None
    save_pack_pair(dlc_quests_dir, target)   -> None
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import re
from pathlib import Path
from typing import Any

from ftbq.canonical import dump_file  # noqa: E402
from ftbq.json5 import Json5Error, parse, to_plain  # noqa: E402
from ftbq.snbt import SnbtError, parse_snbt_file  # noqa: E402

__all__ = [
    "SCHEMA_VERSION",
    "build_audit_index",
    "check_freshness",
    "diff_indexes",
    "item_report",
    "load_index",
    "write_index",
    "build_report",
    "load_report",
    "save_report",
    "report_path",
    "report_fresh",
    "pack_pair_path",
    "load_pack_pair",
    "save_pack_pair",
]

SCHEMA_VERSION = 1

# A ``&e<item_id><chinese_name>&r`` (or ``§e…§r``) Minecraft formatting span.
# ``item_id`` is a resource-location fragment ``[a-z0-9_:]+``; the name is CJK
# (BMP + ext-A). The ``&r`` / ``§r`` boundary makes the split unambiguous.
_ITEM_PATTERN_RE = re.compile(
    r"[&§]e(?P<id>[a-z0-9_:]+)(?P<name>[\u4e00-\u9fff\u3400-\u4dbf]+)[&§]r")

_HEX_ID_RE = re.compile(r"^[0-9A-Fa-f]{16}$")

_AUDIT_INDEX_REL = ".ftbq-cache/audit_index.json5"
_PACK_PAIR_REL = ".ftbq-cache/pack_pair.json5"
_AUDIT_REPORT_REL = ".ftbq-cache/audit_report.json5"


# --------------------------------------------------------------------- helpers


def _now() -> str:
    return (_dt.datetime.now(_dt.timezone.utc)
            .isoformat(timespec="seconds").replace("+00:00", "Z"))


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _detect_format(quests_dir: Path) -> str:
    """SNBT if ``data.snbt`` or any ``.snbt`` chapter/table exists, else JSON5."""
    if (quests_dir / "data.snbt").exists():
        return "snbt"
    for sub in ("chapters", "reward_tables"):
        d = quests_dir / sub
        if d.is_dir() and any(d.glob("*.snbt")):
            return "snbt"
    return "json5"


def _walk_quest_files(quests_dir: Path) -> list[tuple[str, Path]]:
    """Every deployable ``.json5``/``.snbt`` under ``quests_dir`` as
    ``(posix_rel, abs_path)``, excluding the skill's own caches/backups."""
    if not quests_dir.is_dir():
        return []
    out: list[tuple[str, Path]] = []
    for path in quests_dir.rglob("*"):
        if path.suffix.lower() not in (".json5", ".snbt"):
            continue
        rel = path.relative_to(quests_dir).as_posix()
        if rel.startswith(".ftbq-cache/") or rel.startswith(".ftbq-backup/"):
            continue
        out.append((rel, path))
    out.sort(key=lambda t: t[0])
    return out


def _extract_item_patterns(text: str) -> list[dict]:
    """Pull every ``&e<id><name>&r`` span out of ``text``."""
    out: list[dict] = []
    if not isinstance(text, str):
        return out
    for m in _ITEM_PATTERN_RE.finditer(text):
        out.append({
            "item_id": m.group("id"),
            "name": m.group("name"),
            "raw": m.group(0),
        })
    return out


def _as_text_list(value: Any) -> list[str]:
    """Normalize a description field (str | list[str] | None) to a str list."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str)]
    return []


def _quest_chapter_map(quests_dir: Path, fmt: str) -> dict[str, str]:
    """Map quest hex-id → chapter filename, by scanning chapter files."""
    out: dict[str, str] = {}
    ch_dir = quests_dir / "chapters"
    if not ch_dir.is_dir():
        return out
    for ch_file in sorted(ch_dir.glob("*.snbt" if fmt == "snbt" else "*.json5")):
        try:
            if fmt == "snbt":
                data = parse_snbt_file(ch_file)
            else:
                data = to_plain(parse(ch_file.read_text(encoding="utf-8-sig"),
                                        filename=str(ch_file)))
        except (Json5Error, SnbtError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        chapter = str(data.get("filename") or data.get("id") or ch_file.stem)
        quests = data.get("quests")
        if not isinstance(quests, list):
            continue
        for q in quests:
            if isinstance(q, dict) and isinstance(q.get("id"), str):
                out[str(q["id"]).upper()] = chapter
    return out


# --------------------------------------------------------- pattern extraction


def _patterns_from_json5(quests_dir: Path,
                          chapter_of: dict[str, str]) -> list[dict]:
    """JSON5 (1.21+): descriptions live in ``lang/<locale>/quests.json5``
    as ``quest.<hex>.quest_desc`` (list[str]) etc. Scan every quest-keyed
    string value — the ``&e…&r`` regex is specific enough to avoid noise.
    ``chapter_of`` (quest hex → chapter filename) is supplied by the caller
    so the chapter walk isn't repeated."""
    out: list[dict] = []
    lang_root = quests_dir / "lang"
    if not lang_root.is_dir():
        return out
    for lang_file in sorted(lang_root.glob("*/quests.json5")):
        try:
            data = to_plain(parse(lang_file.read_text(encoding="utf-8-sig"),
                                    filename=str(lang_file)))
        except (Json5Error, OSError):
            continue
        if not isinstance(data, dict):
            continue
        locale = lang_file.parent.name
        rel = lang_file.relative_to(quests_dir).as_posix()
        seen: dict[str, list[dict]] = {}
        for key, val in data.items():
            m = re.match(r"^quest\.([0-9A-Fa-f]{16})\.\w+$", str(key))
            if not m:
                continue
            qid = m.group(1).upper()
            for t in _as_text_list(val):
                for p in _extract_item_patterns(t):
                    seen.setdefault(qid, []).append(p)
        for qid, patterns in seen.items():
            out.append({
                "id": qid,
                "chapter": chapter_of.get(qid, ""),
                "source_file": rel,
                "locale": locale,
                "item_patterns": patterns,
            })
    return out


def _patterns_from_snbt(quests_dir: Path) -> list[dict]:
    """SNBT (1.20.1): descriptions are inline on the quest object
    (``description`` / ``subtitle`` / ``title``). Scan each quest in place."""
    out: list[dict] = []
    ch_dir = quests_dir / "chapters"
    if not ch_dir.is_dir():
        return out
    for ch_file in sorted(ch_dir.glob("*.snbt")):
        try:
            data = parse_snbt_file(ch_file)
        except (SnbtError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        chapter = str(data.get("filename") or data.get("id") or ch_file.stem)
        rel = ch_file.relative_to(quests_dir).as_posix()
        quests = data.get("quests")
        if not isinstance(quests, list):
            continue
        for q in quests:
            if not isinstance(q, dict):
                continue
            qid = q.get("id")
            if not (isinstance(qid, str) and _HEX_ID_RE.match(qid)):
                continue
            patterns: list[dict] = []
            for field in ("description", "subtitle", "title"):
                for text in _as_text_list(q.get(field)):
                    patterns.extend(_extract_item_patterns(text))
            # flatten the nested lists and dedupe by raw
            flat: list[dict] = []
            seen_raw: set[str] = set()
            for p in patterns:
                if p["raw"] not in seen_raw:
                    seen_raw.add(p["raw"])
                    flat.append(p)
            if flat:
                out.append({
                    "id": qid.upper(),
                    "chapter": chapter,
                    "source_file": rel,
                    "item_patterns": flat,
                })
    return out


# ------------------------------------------------------------- public: build


def build_audit_index(quests_dir: Path) -> dict:
    """Walk ``quests_dir``, fingerprint every file, and harvest description
    item-ID patterns. Returns the index dict (caller writes it via
    :func:`write_index`). Empty/safe result if the dir is missing."""
    quests_dir = Path(quests_dir)
    fmt = _detect_format(quests_dir)
    files: list[dict] = []
    for rel, abs_path in _walk_quest_files(quests_dir):
        st = abs_path.stat()
        files.append({
            "path": rel,
            "sha256": _sha256_file(abs_path),
            "size": st.st_size,
            "mtime": st.st_mtime,
        })
    files.sort(key=lambda f: f["path"])
    # pack_hash: one digest over the (path, sha256) list — a quick identity
    # signal independent of per-file stat (which mtime can shift on touch).
    h = hashlib.sha256()
    for f in files:
        h.update(f"{f['path']}:{f['sha256']}\n".encode("utf-8"))
    pack_hash = "sha256:" + h.hexdigest()

    # chapter/quest counts give the audit report a self-describing summary
    # so a new conversation can read the report (not the quest files) for
    # context. chapter_of is reused by the JSON5 pattern extractor.
    chapter_of = _quest_chapter_map(quests_dir, fmt)
    chapter_count = len(set(chapter_of.values()))
    quest_count = len(chapter_of)
    if fmt == "snbt":
        quests = _patterns_from_snbt(quests_dir)
    else:
        quests = _patterns_from_json5(quests_dir, chapter_of)

    return {
        "schema": SCHEMA_VERSION,
        "scanned_at": _now(),
        "quests_dir": quests_dir.as_posix(),
        "format": fmt,
        "pack_hash": pack_hash,
        "file_count": len(files),
        "chapter_count": chapter_count,
        "quest_count": quest_count,
        "files": files,
        "quests": quests,
    }


# ---------------------------------------------------------- public: freshness


def check_freshness(quests_dir: Path,
                     cached: dict | None) -> tuple[bool, list[str]]:
    """Decide whether ``cached`` is still fresh for ``quests_dir``.

    Stat each current file; if every cached file's size+mtime matches AND
    the file set is unchanged, the index is fresh (no re-scan needed).
    Any size/mtime drift, added, or removed file → stale. Returns
    ``(is_fresh, changed_paths)``.
    """
    if not cached:
        return False, ["no cached index"]
    cached_files = {f["path"]: f for f in cached.get("files", [])}
    current = _walk_quest_files(quests_dir)
    current_paths = {rel for rel, _ in current}
    changed: list[str] = []
    for rel, abs_path in current:
        st = abs_path.stat()
        c = cached_files.get(rel)
        if c is None:
            changed.append(rel)
        elif st.st_size != c.get("size") or st.st_mtime != c.get("mtime"):
            changed.append(rel)
    for rel in cached_files:
        if rel not in current_paths:
            changed.append(rel)
    return (len(changed) == 0), sorted(changed)


# ----------------------------------------------------------- public: diff


def diff_indexes(a: dict, b: dict) -> dict:
    """Task A — file-level diff between two pack indexes.

    ``a`` is the DLC source, ``b`` the installed target. Returns whether
    they are content-identical and, if not, what's only in each side and
    what shares a path but differs in content.
    """
    a_files = {f["path"]: f["sha256"] for f in a.get("files", [])}
    b_files = {f["path"]: f["sha256"] for f in b.get("files", [])}
    only_a = sorted(set(a_files) - set(b_files))
    only_b = sorted(set(b_files) - set(a_files))
    differs = [
        {"path": p, "a_sha256": a_files[p], "b_sha256": b_files[p]}
        for p in sorted(set(a_files) & set(b_files))
        if a_files[p] != b_files[p]
    ]
    return {
        "identical": not (only_a or only_b or differs),
        "only_in_a": only_a,        # only in DLC source
        "only_in_b": only_b,        # only in installed
        "content_differs": differs,
        "a_dir": a.get("quests_dir", ""),
        "b_dir": b.get("quests_dir", ""),
        "a_pack_hash": a.get("pack_hash", ""),
        "b_pack_hash": b.get("pack_hash", ""),
    }


def item_report(index: dict) -> dict:
    """Task B — per-quest ``&e<item_id><中文名>&r`` patterns from one index."""
    quests = [q for q in index.get("quests", []) if q.get("item_patterns")]
    return {
        "quests_dir": index.get("quests_dir", ""),
        "format": index.get("format", ""),
        "quest_count": len(quests),
        "pattern_count": sum(len(q["item_patterns"]) for q in quests),
        "quests": quests,
    }


# ------------------------------------------------------------- public: io


def load_index(quests_dir: Path) -> dict | None:
    """Load the cached audit index for ``quests_dir`` (``None`` if absent
    or unparseable — caller treats that as a cold start)."""
    path = Path(quests_dir) / _AUDIT_INDEX_REL
    if not path.exists():
        return None
    try:
        return to_plain(parse(path.read_text(encoding="utf-8-sig"),
                                filename=str(path)))
    except (Json5Error, OSError):
        return None


def write_index(quests_dir: Path, index: dict) -> Path:
    path = Path(quests_dir) / _AUDIT_INDEX_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    dump_file(path, index,
              key_order=["schema", "scanned_at", "quests_dir", "format",
                           "pack_hash", "file_count", "chapter_count",
                           "quest_count", "files", "quests"],
              per_path_key_order={
                  "files.[]": ["path", "sha256", "size", "mtime"],
                  "quests.[]": ["id", "chapter", "source_file",
                                  "locale", "item_patterns"],
                  "quests.[].item_patterns.[]": ["item_id", "name", "raw"],
              })
    return path


# ------------------------------------------------------------- pack pair io


def pack_pair_path(dlc_quests_dir: Path) -> Path:
    """Where the remembered (DLC source → target) pair lives: inside the
    DLC source's own ``.ftbq-cache/``, so opening the DLC folder finds it."""
    return Path(dlc_quests_dir) / _PACK_PAIR_REL


def load_pack_pair(dlc_quests_dir: Path) -> dict | None:
    path = pack_pair_path(dlc_quests_dir)
    if not path.exists():
        return None
    try:
        return to_plain(parse(path.read_text(encoding="utf-8-sig"),
                                filename=str(path)))
    except (Json5Error, OSError):
        return None


def save_pack_pair(dlc_quests_dir: Path, target_quests_dir: Path) -> Path:
    path = pack_pair_path(dlc_quests_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    dump_file(path, {
        "dlc_quests_dir": Path(dlc_quests_dir).as_posix(),
        "target_quests_dir": Path(target_quests_dir).as_posix(),
        "remembered_at": _now(),
    }, key_order=["dlc_quests_dir", "target_quests_dir", "remembered_at"])
    return path


# ------------------------------------------------------------- audit report io
# The persisted verdict of one audit run: Task A (diff) + Task B (item
# patterns) + per-pack summaries, keyed by both packs' pack_hashes. A new
# conversation reads this instead of re-auditing — see ``report_fresh``.


def report_path(dlc_quests_dir: Path) -> Path:
    """The audit report lives in the DLC source's ``.ftbq-cache/`` (same
    place as the pack pair) so opening the DLC folder finds both."""
    return Path(dlc_quests_dir) / _AUDIT_REPORT_REL


def _pack_summary(idx: dict) -> dict:
    return {
        "quests_dir": idx.get("quests_dir", ""),
        "format": idx.get("format", ""),
        "pack_hash": idx.get("pack_hash", ""),
        "file_count": idx.get("file_count", 0),
        "chapter_count": idx.get("chapter_count", 0),
        "quest_count": idx.get("quest_count", 0),
        "pattern_count": sum(len(q.get("item_patterns", []))
                             for q in idx.get("quests", [])),
    }


def build_report(dlc_idx: dict, tgt_idx: dict, diff: dict,
                  dlc_item: dict, tgt_item: dict) -> dict:
    """Assemble the persisted audit verdict. ``diff`` is from
    :func:`diff_indexes` (a = DLC, b = target); ``*_item`` from
    :func:`item_report` (embedded in full so a resumed conversation can
    render per-quest patterns without re-reading files)."""
    return {
        "schema": SCHEMA_VERSION,
        "audited_at": _now(),
        "dlc": _pack_summary(dlc_idx),
        "target": _pack_summary(tgt_idx),
        "task_a": {
            "identical": diff.get("identical", False),
            "only_in_dlc": diff.get("only_in_a", []),
            "only_in_installed": diff.get("only_in_b", []),
            "content_differs": diff.get("content_differs", []),
        },
        "task_b": {
            "dlc": dlc_item,
            "target": tgt_item,
        },
    }


def save_report(dlc_quests_dir: Path, report: dict) -> Path:
    path = report_path(dlc_quests_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    dump_file(path, report,
              key_order=["schema", "audited_at", "dlc", "target",
                           "task_a", "task_b"],
              per_path_key_order={
                  "dlc": ["quests_dir", "format", "pack_hash", "file_count",
                            "chapter_count", "quest_count", "pattern_count"],
                  "target": ["quests_dir", "format", "pack_hash", "file_count",
                               "chapter_count", "quest_count", "pattern_count"],
                  "task_a": ["identical", "only_in_dlc", "only_in_installed",
                               "content_differs"],
                  "task_a.content_differs.[]": ["path", "a_sha256",
                                                  "b_sha256"],
              })
    return path


def load_report(dlc_quests_dir: Path) -> dict | None:
    path = report_path(dlc_quests_dir)
    if not path.exists():
        return None
    try:
        return to_plain(parse(path.read_text(encoding="utf-8-sig"),
                                filename=str(path)))
    except (Json5Error, OSError):
        return None


def report_fresh(report: dict | None, dlc_idx: dict | None,
                  tgt_idx: dict | None,
                  dlc_fresh: bool, tgt_fresh: bool) -> bool:
    """Is a saved report still valid to resume from?

    True iff: a report exists, both indexes are present, both are fresh
    (on-disk files unchanged since the index was built), AND the report's
    recorded pack_hashes still match the indexes' (catches the case where
    an index was rebuilt but the report wasn't). When this returns True a
    new conversation can print the saved verdict and skip re-auditing.
    """
    if not report or not dlc_idx or not tgt_idx:
        return False
    if not (dlc_fresh and tgt_fresh):
        return False
    return (report.get("dlc", {}).get("pack_hash")
            == dlc_idx.get("pack_hash")
            and report.get("target", {}).get("pack_hash")
            == tgt_idx.get("pack_hash"))
