"""Index existing FTB Quests in a modpack for task linkage.

The skill generates *new* quests, but a pack often already has quests from
other sources (hand-written, other tools, a community quest book). To keep
generated content from landing as an isolated, abrupt chunk, this helper
records a lightweight summary of every existing quest so the interview can
link to them — gate after, reward from, branch off, or just avoid
duplicating progression.

This is the CodeGraph "analyze → index → query" approach applied to quest
files: scan the on-disk quests, extract a per-quest digest, and write it to
``.ftbq-cache/existing_quests.json5``. The Step 1 indexer.

Modern JSON5 is parsed with the string-aware ``ftbq.json5`` parser; legacy
``.snbt`` files get a best-effort regex pass and are marked ``format: snbt``
with lower detail (modern packs are the default target). Stdlib only.

Output: ``<output_dir>/.ftbq-cache/existing_quests.json5``

Usage::

    python scripts/index_quests.py <modpack_dir>
    python scripts/index_quests.py <modpack_dir> --output <quests_dir>
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq.canonical import dump_file  # noqa: E402
from ftbq.json5 import Json5Error, parse, to_plain  # noqa: E402

SCHEMA_VERSION = 1

# A quest/chapter/object ID is the 16-char uppercase hex from the md5 formula.
_HEX_ID_RE = re.compile(r"^[0-9A-Fa-f]{16}$")
# Best-effort SNBT id/type harvest.
_SNBT_ID_RE = re.compile(r'id\s*:\s*"([0-9A-Fa-f]{16})"', re.IGNORECASE)
_SNBT_TYPE_RE = re.compile(r'type\s*:\s*"([^"]+)"')
# A resource location like ``create:cogwheel`` or ``minecraft:oak_log``.
# Matched against already-parsed string values (no surrounding quotes).
_NS_RE = re.compile(r"\b([a-z0-9_]+):[a-z0-9_/.\-]+\b", re.IGNORECASE)


def _is_hex_id(value: Any) -> bool:
    return isinstance(value, str) and bool(_HEX_ID_RE.match(value))


def _namespaces_from(value: Any) -> set[str]:
    """Pull mod namespaces (``create``, ``minecraft`` ...) out of item/fluid ids.

    Runs against already-parsed Python values (the JSON5 parser strips quotes),
    so the regex matches bare resource locations like ``create:cogwheel``."""
    out: set[str] = set()
    if isinstance(value, str):
        for m in _NS_RE.finditer(value):
            out.add(m.group(1).lower())
    elif isinstance(value, dict):
        for v in value.values():
            out |= _namespaces_from(v)
    elif isinstance(value, list):
        for v in value:
            out |= _namespaces_from(v)
    # ftbquests: and minecraft: are not interesting mod signals for linkage.
    out.discard("ftbquests")
    out.discard("minecraft")
    return out


def _item_ids_from(value: Any) -> set[str]:
    """Pull full resource-location ids (``create:cogwheel``, ``minecraft:stone``)
    out of parsed task/reward values. Broader than ``_namespaces_from`` — keeps
    the full id (not just the mod prefix) so the author has a verified list of
    item ids that actually loaded in this pack. Drops ``ftbquests:`` internals."""
    out: set[str] = set()
    if isinstance(value, str):
        for m in _NS_RE.finditer(value):
            out.add(m.group(0).lower())
    elif isinstance(value, dict):
        for v in value.values():
            out |= _item_ids_from(v)
    elif isinstance(value, list):
        for v in value:
            out |= _item_ids_from(v)
    return {i for i in out if not i.startswith("ftbquests:")}


def _task_type(task: Any) -> str:
    if isinstance(task, dict):
        t = task.get("type", "")
        return str(t) if t else ""
    return ""


def _quest_digest(quest: dict, *, chapter: str, source: str,
                  lang_titles: dict[str, str]) -> dict | None:
    qid = quest.get("id")
    if not _is_hex_id(qid):
        return None
    title = lang_titles.get(str(qid), "")
    tasks = quest.get("tasks") if isinstance(quest.get("tasks"), list) else []
    rewards = quest.get("rewards") if isinstance(quest.get("rewards"), list) else []
    mod_ids: set[str] = set()
    item_ids: set[str] = set()
    for t in tasks:
        mod_ids |= _namespaces_from(t)
        item_ids |= _item_ids_from(t)
    for r in rewards:
        mod_ids |= _namespaces_from(r)
        item_ids |= _item_ids_from(r)
    return {
        "id": str(qid),
        "chapter": chapter,
        "title": title,
        "shape": str(quest.get("shape", "")),
        "dependencies": [str(d) for d in quest.get("dependencies", [])
                         if _is_hex_id(d)],
        "task_types": sorted({_task_type(t) for t in tasks if _task_type(t)}),
        "reward_types": sorted({_task_type(r) for r in rewards if _task_type(r)}),
        "mod_ids": sorted(mod_ids),
        "item_ids": sorted(item_ids),
        "source_file": source,
    }


def _index_json5_file(path: Path, quests_out: list[dict],
                      *, lang_titles: dict[str, str]) -> int:
    """Parse one JSON5 file, append any quest digests found. Return quest count."""
    try:
        data = to_plain(parse(path.read_text(encoding="utf-8-sig"),
                                filename=str(path)))
    except (Json5Error, OSError):
        return 0
    source = path.as_posix()
    count = 0
    if isinstance(data, dict):
        # A chapter file: { id, filename, ..., quests: [...] }
        chapter = str(data.get("filename") or data.get("id") or path.stem)
        for q in data.get("quests", []) if isinstance(data.get("quests"), list) else []:
            if isinstance(q, dict):
                dig = _quest_digest(q, chapter=chapter, source=source,
                                    lang_titles=lang_titles)
                if dig:
                    quests_out.append(dig)
                    count += 1
        # A bare quest object at file root (some layouts).
        if _is_hex_id(data.get("id")) and isinstance(data.get("tasks"), list):
            dig = _quest_digest(data, chapter=path.stem, source=source,
                                lang_titles=lang_titles)
            if dig:
                quests_out.append(dig)
                count += 1
    return count


def _index_snbt_file(path: Path, quests_out: list[dict]) -> int:
    """Best-effort SNBT harvest: IDs + types, no titles/coords. Marked snbt."""
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return 0
    source = path.as_posix()
    ids = list(dict.fromkeys(_SNBT_ID_RE.findall(text)))  # dedupe, keep order
    types = sorted(set(_SNBT_TYPE_RE.findall(text)))
    count = 0
    for qid in ids:
        quests_out.append({
            "id": qid.upper(),
            "chapter": path.stem,
            "title": "",
            "shape": "",
            "dependencies": [],
            "task_types": types,
            "reward_types": [],
            "mod_ids": [],
            "source_file": source,
            "format": "snbt",
        })
        count += 1
    return count


def _load_lang_titles(quests_dir: Path) -> dict[str, str]:
    """Map hex quest ID → title from every lang/<locale>/quests.json5 found."""
    titles: dict[str, str] = {}
    lang_root = quests_dir / "lang"
    if not lang_root.is_dir():
        return titles
    for lang_file in sorted(lang_root.glob("*/quests.json5")):
        try:
            data = to_plain(parse(lang_file.read_text(encoding="utf-8-sig"),
                                    filename=str(lang_file)))
        except (Json5Error, OSError):
            continue
        if not isinstance(data, dict):
            continue
        for key, val in data.items():
            # Keys look like "quest.<HEX>.title" or "<HEX>.title".
            m = re.search(r"([0-9A-Fa-f]{16})\.title$", str(key))
            if m and isinstance(val, str) and val:
                titles.setdefault(m.group(1).upper(), val)
    return titles


def index_pack(quests_dir: Path) -> dict:
    lang_titles = _load_lang_titles(quests_dir)
    quests: list[dict] = []
    unindexed: list[dict] = []
    if not quests_dir.is_dir():
        return {
            "schema": SCHEMA_VERSION,
            "scanned_at": _now(),
            "quests_dir": quests_dir.as_posix(),
            "count": 0,
            "quests": [],
            "unindexed": [{"path": quests_dir.as_posix(),
                            "reason": "quests directory not found"}],
        }
    files = sorted([*quests_dir.rglob("*.json5"), *quests_dir.rglob("*.snbt")])
    for f in files:
        if f.suffix.lower() == ".json5":
            _index_json5_file(f, quests, lang_titles=lang_titles)
        else:
            _index_snbt_file(f, quests)
    # Dedupe by id (a quest can appear in a merged file + its own); keep first.
    seen: set[str] = set()
    deduped: list[dict] = []
    for q in quests:
        if q["id"] not in seen:
            seen.add(q["id"])
            deduped.append(q)
    # Verified item ids: every resource location referenced by an existing
    # quest's tasks/rewards actually loaded in this pack — author new tasks
    # against this set rather than guessing ids (see SKILL.md "Verify, don't
    # fabricate"). .snbt quests contribute lower detail (no item_ids).
    known_item_ids: set[str] = set()
    for q in deduped:
        known_item_ids |= set(q.get("item_ids", []))
    return {
        "schema": SCHEMA_VERSION,
        "scanned_at": _now(),
        "quests_dir": quests_dir.as_posix(),
        "count": len(deduped),
        "known_item_ids": sorted(known_item_ids),
        "quests": deduped,
        "unindexed": unindexed,
    }


def _now() -> str:
    return (_dt.datetime.now(_dt.timezone.utc)
            .isoformat(timespec="seconds").replace("+00:00", "Z"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Index existing FTB Quests into .ftbq-cache/existing_quests.json5")
    parser.add_argument("modpack_dir", type=Path,
                        help="Path to the modpack root (containing config/ftbquests/quests)")
    parser.add_argument("--output", "-o", type=Path,
                        help="Quests output dir (default: "
                             "<modpack_dir>/config/ftbquests/quests)")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args(argv)

    modpack = args.modpack_dir.resolve()
    quests_dir = (args.output or
                  modpack / "config" / "ftbquests" / "quests").resolve()
    cache_dir = quests_dir / ".ftbq-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache = index_pack(quests_dir)
    cache_path = cache_dir / "existing_quests.json5"
    dump_file(cache_path, cache,
              key_order=["schema", "scanned_at", "quests_dir", "count",
                          "known_item_ids", "quests", "unindexed"],
              per_path_key_order={
                  "quests.[]": ["id", "chapter", "title", "shape",
                                 "dependencies", "task_types", "reward_types",
                                 "mod_ids", "item_ids", "source_file",
                                 "format"],
              })
    if not args.quiet:
        print(f"Indexed {cache['count']} existing quests → {cache_path}")
        chapters = sorted({q["chapter"] for q in cache["quests"]})
        if chapters:
            print(f"  chapters: {', '.join(chapters)}")
        snbt = sum(1 for q in cache["quests"] if q.get("format") == "snbt")
        if snbt:
            print(f"  ({snbt} from legacy .snbt — lower detail)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
