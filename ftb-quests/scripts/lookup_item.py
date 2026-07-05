"""Batch item-name → id lookup against ``.ftbq-cache/item_names.json5``.

Token-saving: replaces N one-id greps of ``items.json5`` when writing many
item tasks (a 收集 / collection quest). One call resolves N display names →
ids, so the agent reads the game source **once** (at Step 1, via
``extract_items.py``) and reuses the persisted name index every time after.

The index carries ``en_us`` (universal) + ``zh_cn`` (where the jar ships it)
lang values. This CLI also live-merges the user-verified Chinese names that
``audit_index.py`` harvested from existing quest descriptions
(``&e<id><中文名>&r`` spans) — no second scan, just a read of the audit cache
at query time.

**Ambiguity is surfaced, never silently picked.** Many mods ship the same
display name (e.g. "Copper Ingot" in minecraft / create / immersiveengineering);
a name mapping to ≥2 ids prints every candidate with its mod prefix so the
agent/user can pick by chapter context — this is the 禁止脑补 guarantee.

Usage::

    python scripts/lookup_item.py <packroot> <name> [<name> ...]
    python scripts/lookup_item.py <packroot> <name>... --json
    python scripts/lookup_item.py <packroot> <name>... --partial
    python scripts/lookup_item.py <packroot> --reverse <id> [<id>...]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq import audit as ftbq_audit  # noqa: E402
from ftbq.json5 import Json5Error, parse_file, to_plain  # noqa: E402


def _load_name_index(cache_dir: Path) -> dict | None:
    """Load ``item_names.json5`` (None if absent/unparseable — caller treats
    that as a cold start with a 'run extract_items first' hint)."""
    p = cache_dir / "item_names.json5"
    if not p.exists():
        return None
    try:
        v = to_plain(parse_file(p))
        return v if isinstance(v, dict) else None
    except (Json5Error, OSError):
        return None


def _load_audit_names(quests_dir: Path) -> dict[str, str]:
    """``{name: id}`` reversed from ``audit_index.json5`` ``item_patterns``.
    Only namespaced ids (``modid:name``) are kept — a short id without a
    modid isn't a usable task item id."""
    idx = ftbq_audit.load_index(quests_dir)
    if not idx:
        return {}
    out: dict[str, str] = {}
    for q in idx.get("quests", []):
        for pat in q.get("item_patterns", []):
            iid = pat.get("item_id", "")
            nm = pat.get("name", "")
            if ":" in iid and nm:
                out[nm] = iid
    return out


def _build_map(name_index: dict, audit_names: dict) -> dict[str, dict[str, str]]:
    """Merge into ``name -> {id: source}``. Ambiguity emerges naturally when
    ≥2 ids land under one name. Audit overrides jar on the same (name, id)
    pair (user-verified); a *different* audit id for the same name makes it
    ambiguous rather than overwriting the jar id."""
    by_name: dict[str, dict[str, str]] = {}

    def _add(name: str, iid: str, source: str) -> None:
        d = by_name.setdefault(name, {})
        if iid not in d or source == "audit":
            d[iid] = source

    for name, iid in name_index.get("name_to_id", {}).items():
        _add(name, iid, "jar")
    for name, ids in name_index.get("ambiguous", {}).items():
        for iid in ids:
            _add(name, iid, "jar")
    for name, iid in audit_names.items():
        _add(name, iid, "audit")
    return by_name


def _result(query: str, idsrc: dict[str, str]) -> dict:
    """Collapse ``{id: source}`` into a found (1 id) or ambiguous (≥2) result."""
    if len(idsrc) == 1:
        iid, s = next(iter(idsrc.items()))
        return {"query": query, "status": "found", "id": iid, "source": s}
    return {"query": query, "status": "ambiguous",
            "ids": [{"id": iid, "source": s} for iid, s in sorted(idsrc.items())]}


def _suggestions(by_name: dict[str, dict[str, str]], query: str) -> list[str]:
    """Top ~10 names containing the query substring (case-insensitive); falls
    back to a shared-prefix hint for very short queries."""
    ql = query.lower()
    hits = [name for name in by_name if ql in name.lower()]
    if not hits and len(ql) >= 3:
        hits = [name for name in by_name if name.lower().startswith(ql[:3])]
    return sorted(hits)[:10]


def _query_forward(by_name: dict[str, dict[str, str]], query: str,
                   partial: bool) -> dict:
    if query in by_name:                       # exact, case-sensitive
        return _result(query, by_name[query])
    ql = query.lower()                         # exact, case-insensitive
    ci: dict[str, str] = {}
    for name, idsrc in by_name.items():
        if name.lower() == ql:
            for iid, s in idsrc.items():
                ci[iid] = s
    if ci:
        return _result(query, ci)
    if partial:                                # substring matches
        matches: list[dict] = []
        for name, idsrc in by_name.items():
            if ql and ql in name.lower():
                for iid, s in idsrc.items():
                    matches.append({"name": name, "id": iid, "source": s})
        if matches:
            matches.sort(key=lambda m: (m["name"], m["id"]))
            return {"query": query, "status": "partial", "matches": matches}
    return {"query": query, "status": "not_found",
            "suggestions": _suggestions(by_name, query)}


def _query_reverse(by_name: dict[str, dict[str, str]],
                    ids: list[str]) -> list[dict]:
    """Invert name→id to id→names in memory (no second scan; the on-disk
    index is name→id only to stay light)."""
    by_id: dict[str, list[tuple[str, str]]] = {}
    for name, idsrc in by_name.items():
        for iid, s in idsrc.items():
            by_id.setdefault(iid, []).append((name, s))
    out: list[dict] = []
    for qid in ids:
        if qid in by_id:
            names = sorted(by_id[qid])
            out.append({"query": qid, "status": "found",
                        "names": [{"name": n, "source": s} for n, s in names]})
        else:
            out.append({"query": qid, "status": "not_found"})
    return out


def render_text(results: list[dict]) -> str:
    lines: list[str] = []
    for r in results:
        q = r["query"]
        if "names" in r:                        # --reverse
            ns = r["names"]
            label = " / ".join(n["name"] for n in ns)
            src = ", ".join(dict.fromkeys(n["source"] for n in ns))
            lines.append(f"{q} → {label}   (source: {src})")
        elif r["status"] == "found":
            lines.append(f"{q} → {r['id']}   (source: {r['source']})")
        elif r["status"] == "ambiguous":
            lines.append(f"{q} → AMBIGUOUS ({len(r['ids'])} ids):")
            for e in r["ids"]:
                lines.append(f"    {e['id']}   (source: {e['source']})")
        elif r["status"] == "partial":
            lines.append(f"{q} → partial ({len(r['matches'])} matches):")
            for m in r["matches"]:
                lines.append(f"    {m['name']} → {m['id']}   "
                              f"(source: {m['source']})")
        else:                                   # not_found
            lines.append(f"{q} → NOT FOUND")
            sug = r.get("suggestions", [])
            if sug:
                lines.append(f"    suggestions: {', '.join(sug)}")
    return "\n".join(lines)


def build_results(packroot: Path, names: list[str], *, partial: bool = False,
                  reverse: bool = False, cache_dir: Path | None = None
                  ) -> tuple[list[dict] | None, Path]:
    """Resolve ``names`` against the cache. Returns ``(results, cache_dir)``;
    ``results`` is None when the name index is missing (caller emits the
    'run extract_items first' hint and exits 2)."""
    if cache_dir is not None:
        cache_dir = Path(cache_dir).resolve()
        quests_dir = cache_dir.parent
    else:
        quests_dir = (Path(packroot) / "config" / "ftbquests"
                      / "quests").resolve()
        cache_dir = quests_dir / ".ftbq-cache"
    name_index = _load_name_index(cache_dir)
    if name_index is None:
        return None, cache_dir
    audit_names = _load_audit_names(quests_dir)
    by_name = _build_map(name_index, audit_names)
    if reverse:
        return _query_reverse(by_name, names), cache_dir
    return [_query_forward(by_name, n, partial) for n in names], cache_dir


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Batch item-name → id lookup (token-saving for many "
                    "item tasks, e.g. collection quests)")
    p.add_argument("packroot", type=Path,
                    help="Modpack root (dir with mods/); cache resolved at "
                         "<packroot>/config/ftbquests/quests/.ftbq-cache/")
    p.add_argument("names", nargs="*",
                    help="Item display names to resolve (or ids with --reverse)")
    p.add_argument("--partial", action="store_true",
                    help="Also return substring name matches")
    p.add_argument("--reverse", action="store_true",
                    help="Treat inputs as ids; print each id's known names")
    p.add_argument("--cache-dir", type=Path,
                    help="Override the .ftbq-cache dir (e.g. a generator "
                         "output dir)")
    p.add_argument("--json", action="store_true",
                    help="Machine-readable output")
    args = p.parse_args(argv)
    if not args.names:
        p.error("provide at least one name (or id with --reverse)")

    results, cache_dir = build_results(
        args.packroot.resolve(), args.names, partial=args.partial,
        reverse=args.reverse, cache_dir=args.cache_dir)
    if results is None:
        print(f"error: {cache_dir / 'item_names.json5'} not found — "
              f"run `python scripts/extract_items.py <packroot>` first",
              file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(render_text(results))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
