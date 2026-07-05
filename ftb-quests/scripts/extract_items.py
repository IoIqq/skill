"""Extract verified item/block ids (and display names) from a modpack's jars.

Walks ``<modpack>/mods/*.jar`` and reads each jar's
``assets/<modid>/lang/en_us.json`` (the standard Minecraft lang-file path),
deriving real item/block ids from the translation keys:

    "item.<modid>.<name>"   →  "<modid>:<name>"
    "block.<modid>.<name>"  →  "<modid>:<name>"

These ids **actually loaded in the pack's mods** — author item tasks/rewards
against this set instead of guessing (see SKILL.md "Verify, don't fabricate").

**Best-effort, not a complete registry:** not every registered item has a lang
key (internal/technical items often don't); a few lang keys describe variants
rather than discrete ids (e.g. ``item.minecraft.potion.effect.*``). Treat the
output as a *candidate set* — the in-game load-test (Step 5a) is still the
final verifier. Jars without a lang file are listed in ``no_lang``.

Two caches are written in one scan (the second is a byproduct of the first —
the lang values are read anyway, this just stops throwing them away):

* ``items.json5``       — id-only registry (``all_item_ids`` + per-mod lists).
* ``item_names.json5``  — lightweight **name → id** index for batch lookup
  (see ``lookup_item.py``). Carries the lang *values* (display names) for
  ``en_us`` (universal) and ``zh_cn`` (where the jar ships it). Names that
  map to ≥2 ids (common — "Copper Ingot" in minecraft/create/…) land in
  ``ambiguous`` so the lookup can surface them instead of silently picking.

Stdlib only. Usage::

    python scripts/extract_items.py <modpack_dir>
    python scripts/extract_items.py <modpack_dir> --output <quests_dir>
    python scripts/extract_items.py <modpack_dir> --no-names   # items.json5 only
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

# Allow running from anywhere — make the repo root importable.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq.canonical import dump_file  # noqa: E402

SCHEMA_VERSION = 1
NAMES_SCHEMA_VERSION = 1

# item.<modid>.<name>  /  block.<modid>.<name>  — name may contain dots.
_LANG_KEY_RE = re.compile(r"^(?:item|block)\.([a-z0-9_]+)\.(.+)$", re.IGNORECASE)
_LANG_PATH_RE = re.compile(r"^assets/([a-z0-9_]+)/lang/[^/]+\.json$",
                           re.IGNORECASE)


def _now() -> str:
    return (_dt.datetime.now(_dt.timezone.utc)
            .isoformat(timespec="seconds").replace("+00:00", "Z"))


def _read_zip(zf: zipfile.ZipFile, name: str) -> bytes | None:
    try:
        return zf.read(name)
    except KeyError:
        return None


def _decode(data: bytes) -> str:
    # latin-1 maps every byte, so it's the guaranteed-success fallback once
    # the utf-8 variants fail — no unreachable trailing return needed.
    for enc in ("utf-8-sig", "utf-8"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1")


def _names_from_lang(data: Any, ns: str) -> dict[str, str]:
    """``{display_name: id}`` for every item/block key in ``data`` whose
    lang-key namespace matches ``ns``. The lang *values* (display names) are
    the keys here; an empty/whitespace value is skipped."""
    out: dict[str, str] = {}
    if not isinstance(data, dict):
        return out
    for key, val in data.items():
        m = _LANG_KEY_RE.match(str(key))
        if m and m.group(1).lower() == ns and isinstance(val, str) and val:
            out[val] = f"{ns}:{m.group(2).lower()}"
    return out


def _extract_jar(jar_path: Path) -> tuple[str | None, list[str], str | None,
                                           dict[str, dict[str, str]]]:
    """Return ``(modid, sorted item ids, en_lang_file, names)`` for the first
    namespace in the jar that yields item/block keys. ``names`` is
    ``{"en_us": {name: id}, "zh_cn": {name: id}}`` (empty dicts where the jar
    ships no such locale). ``(None, [], None, {})`` if the jar has no lang file.

    The id set is derived from the ``en_us`` file when present (matching the
    pre-name-index behaviour, so ``all_item_ids`` stays stable), else from the
    first locale present. Display names are pulled from ``en_us`` and
    ``zh_cn`` specifically — never from an arbitrary fallback locale."""
    try:
        with zipfile.ZipFile(jar_path) as zf:
            namelist = zf.namelist()
            # Group lang files by asset namespace, prefer en_us per namespace.
            by_ns: dict[str, list[str]] = {}
            for n in namelist:
                m = _LANG_PATH_RE.match(n)
                if m:
                    by_ns.setdefault(m.group(1).lower(), []).append(n)
            if not by_ns:
                return None, [], None, {}
            for ns, files in by_ns.items():
                en_file = next((f for f in files
                                if f.endswith(("en_us.json", "en_ud.json"))),
                               None)
                prefer = en_file or files[0]
                raw = _read_zip(zf, prefer)
                if raw is None:
                    continue
                try:
                    data = json.loads(_decode(raw))
                except (json.JSONDecodeError, ValueError):
                    continue
                if not isinstance(data, dict):
                    continue
                items: set[str] = set()
                for key in data:
                    m = _LANG_KEY_RE.match(str(key))
                    if m and m.group(1).lower() == ns:
                        items.add(f"{ns}:{m.group(2).lower()}")
                if not items:
                    continue
                # English names: reuse the already-parsed `data` when the
                # prefer file IS en_us (the common case); otherwise read en_us
                # separately (it exists but wasn't the items source).
                en_names: dict[str, str] = {}
                if en_file is not None:
                    if en_file == prefer:
                        en_names = _names_from_lang(data, ns)
                    else:
                        en_raw = _read_zip(zf, en_file)
                        if en_raw is not None:
                            try:
                                en_names = _names_from_lang(
                                    json.loads(_decode(en_raw)), ns)
                            except (json.JSONDecodeError, ValueError):
                                pass
                # Chinese names: read zh_cn.json if the jar ships it.
                zh_names: dict[str, str] = {}
                zh_file = next((f for f in files if f.endswith("zh_cn.json")),
                               None)
                if zh_file is not None:
                    zh_raw = _read_zip(zf, zh_file)
                    if zh_raw is not None:
                        try:
                            zh_names = _names_from_lang(
                                json.loads(_decode(zh_raw)), ns)
                        except (json.JSONDecodeError, ValueError):
                            pass
                return ns, sorted(items), prefer, {"en_us": en_names,
                                                    "zh_cn": zh_names}
            return None, [], None, {}
    except (zipfile.BadZipFile, OSError):
        return None, [], None, {}


def scan_directory(modpack_dir: Path) -> tuple[list[dict], list[dict],
                                                dict[str, set[str]]]:
    """One pass over ``<modpack>/mods/*.jar``. Returns
    ``(mods_with_items, no_lang_jars, name_to_ids)`` where ``name_to_ids`` is
    ``{display_name: {id, …}}`` accumulated across every mod's en_us + zh_cn
    values — names mapping to ≥2 ids are the ambiguity set (surfaced later,
    never collapsed)."""
    mods_dir = modpack_dir / "mods"
    if not mods_dir.is_dir():
        return [], [{"jar": mods_dir.as_posix(),
                     "reason": "mods/ directory not found"}], {}
    parsed: list[dict] = []
    no_lang: list[dict] = []
    name_to_ids: dict[str, set[str]] = {}
    for jar in sorted(mods_dir.glob("*.jar")):
        modid, items, lang_file, names = _extract_jar(jar)
        if modid and items:
            parsed.append({
                "modid": modid,
                "items": items,
                "source_jar": jar.name,
                "lang_file": lang_file,
            })
            for locale_map in (names.get("en_us"), names.get("zh_cn")):
                if not locale_map:
                    continue
                for name, iid in locale_map.items():
                    name_to_ids.setdefault(name, set()).add(iid)
        else:
            no_lang.append({"jar": jar.name,
                            "reason": "no parseable assets/<modid>/lang/*.json"})
    return parsed, no_lang, name_to_ids


def _assemble_items(modpack_dir: Path, parsed: list[dict],
                     no_lang: list[dict]) -> dict:
    all_ids: set[str] = set()
    for m in parsed:
        all_ids |= set(m["items"])
    return {
        "schema": SCHEMA_VERSION,
        "scanned_at": _now(),
        "modpack_dir": modpack_dir.as_posix(),
        "count": len(parsed),
        "total_item_ids": len(all_ids),
        "all_item_ids": sorted(all_ids),
        "mods": parsed,
        "no_lang": no_lang,
    }


def _assemble_names(modpack_dir: Path,
                     name_to_ids: dict[str, set[str]]) -> dict:
    """Split the accumulator into ``name_to_id`` (1 name → 1 id) and
    ``ambiguous`` (1 name → ≥2 ids). One map + a small collision map — the
    lightest form that still surfaces ambiguity instead of hiding it."""
    name_to_id: dict[str, str] = {}
    ambiguous: dict[str, list[str]] = {}
    covered_ids: set[str] = set()
    for name, ids in name_to_ids.items():
        covered_ids |= ids
        if len(ids) == 1:
            name_to_id[name] = next(iter(ids))
        else:
            ambiguous[name] = sorted(ids)
    return {
        "schema": NAMES_SCHEMA_VERSION,
        "scanned_at": _now(),
        "modpack_dir": modpack_dir.as_posix(),
        "sources": ["en_us", "zh_cn"],
        "name_count": len(name_to_id) + len(ambiguous),
        "id_count": len(covered_ids),
        "name_to_id": dict(sorted(name_to_id.items())),
        "ambiguous": dict(sorted(ambiguous.items())),
    }


def build_cache(modpack_dir: Path) -> dict:
    """Items-only cache (back-compat entry point; ``main`` writes both files
    from one scan)."""
    parsed, no_lang, _ = scan_directory(modpack_dir)
    return _assemble_items(modpack_dir, parsed, no_lang)


def build_names_cache(modpack_dir: Path) -> dict:
    """Name→id index (back-compat entry point; ``main`` writes both files
    from one scan)."""
    _parsed, _no_lang, name_to_ids = scan_directory(modpack_dir)
    return _assemble_names(modpack_dir, name_to_ids)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract verified item/block ids + display names from "
                    "mod jars into .ftbq-cache/items.json5 and "
                    ".ftbq-cache/item_names.json5")
    parser.add_argument("modpack_dir", type=Path,
                        help="Path to the modpack root (the dir containing mods/)")
    parser.add_argument("--output", "-o", type=Path,
                        help="Quests output dir (default: "
                             "<modpack_dir>/config/ftbquests/quests)")
    parser.add_argument("--no-names", action="store_true",
                        help="Skip writing item_names.json5 (ids only)")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args(argv)

    modpack = args.modpack_dir.resolve()
    output = (args.output or
              modpack / "config" / "ftbquests" / "quests").resolve()
    cache_dir = output / ".ftbq-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # One scan feeds both caches.
    parsed, no_lang, name_to_ids = scan_directory(modpack)
    items_cache = _assemble_items(modpack, parsed, no_lang)
    dump_file(cache_dir / "items.json5", items_cache,
              key_order=["schema", "scanned_at", "modpack_dir", "count",
                         "total_item_ids", "all_item_ids", "mods", "no_lang"],
              per_path_key_order={
                  "mods.[]": ["modid", "items", "source_jar", "lang_file"],
                  "no_lang.[]": ["jar", "reason"],
              })
    wrote_names = False
    if not args.no_names:
        names_cache = _assemble_names(modpack, name_to_ids)
        dump_file(cache_dir / "item_names.json5", names_cache,
                  key_order=["schema", "scanned_at", "modpack_dir", "sources",
                             "name_count", "id_count", "name_to_id",
                             "ambiguous"])
        wrote_names = True

    if not args.quiet:
        print(f"Extracted {items_cache['total_item_ids']} item ids from "
              f"{items_cache['count']} mods → {cache_dir / 'items.json5'}")
        if wrote_names:
            nc = names_cache
            print(f"  + name→id index: {nc['name_count']} names "
                  f"({len(nc['ambiguous'])} ambiguous) covering "
                  f"{nc['id_count']} ids → "
                  f"{cache_dir / 'item_names.json5'}")
        if items_cache["no_lang"]:
            print(f"  ({len(items_cache['no_lang'])} jar(s) without a lang "
                  f"file — best-effort; not every mod ships one)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
