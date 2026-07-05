"""Compact, agent-oriented pack briefing built from the ``.ftbq-cache/``
indexes.

Token-saving: one command's curated output replaces reading ``mods.json5``
(with its long descriptions), ``existing_quests.json5``, ``audit_report.json5``
and the chapter files raw. The agent runs this at conversation start for
orientation, then reads raw quest files ONLY when authoring a specific
quest (the Step 4 loop — use ``quest_detail.py`` for that one-quest view).

Reads whatever caches exist; a missing cache is reported as "not indexed"
with the command that builds it. Nothing is re-scanned here.

Usage::

    python scripts/pack_briefing.py <packroot>
    python scripts/pack_briefing.py <packroot> --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq.json5 import Json5Error, parse, to_plain  # noqa: E402


def _load_json5(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        v = to_plain(parse(path.read_text(encoding="utf-8-sig"),
                             filename=str(path)))
        return v if isinstance(v, dict) else None
    except (Json5Error, OSError):
        return None


def _detect_format(quests_dir: Path) -> str:
    if (quests_dir / "data.snbt").exists():
        return "snbt"
    for sub in ("chapters", "reward_tables"):
        d = quests_dir / sub
        if d.is_dir() and any(d.glob("*.snbt")):
            return "snbt"
    return "json5"


def build_briefing(packroot: Path) -> dict:
    """Curate a compact pack summary from the caches. Never re-scans."""
    quests_dir = packroot / "config" / "ftbquests" / "quests"
    cache = quests_dir / ".ftbq-cache"
    mods_cache = _load_json5(cache / "mods.json5")
    eq_cache = _load_json5(cache / "existing_quests.json5")
    report = _load_json5(cache / "audit_report.json5")
    fmt = _detect_format(quests_dir)

    mods = (mods_cache or {}).get("mods", [])
    mod_names = sorted({str(m.get("name") or m.get("modid") or "?")
                        for m in mods if isinstance(m, dict)})

    eq_quests = (eq_cache or {}).get("quests", [])
    chapters: dict[str, int] = {}
    task_freq: dict[str, int] = {}
    reward_freq: dict[str, int] = {}
    for q in eq_quests:
        if not isinstance(q, dict):
            continue
        ch = str(q.get("chapter") or "?")
        chapters[ch] = chapters.get(ch, 0) + 1
        for t in q.get("task_types", []) or []:
            task_freq[str(t)] = task_freq.get(str(t), 0) + 1
        for r in q.get("reward_types", []) or []:
            reward_freq[str(r)] = reward_freq.get(str(r), 0) + 1

    audit = None
    if report:
        ta = report.get("task_a", {}) or {}
        tb = report.get("task_b", {}) or {}
        audit = {
            "identical": bool(ta.get("identical")),
            "audited_at": report.get("audited_at", ""),
            "only_in_dlc": len(ta.get("only_in_dlc", []) or []),
            "only_in_installed": len(ta.get("only_in_installed", []) or []),
            "content_differs": len(ta.get("content_differs", []) or []),
            "dlc_patterns": (tb.get("dlc", {}) or {}).get("pattern_count", 0),
            "target_patterns": (tb.get("target", {}) or {}).get("pattern_count", 0),
        }

    return {
        "packroot": packroot.as_posix(),
        "quests_dir": quests_dir.as_posix(),
        "format": fmt,
        "mod_count": len(mods),
        "mod_names": mod_names,
        "chapter_count": len(chapters),
        "quest_count": len(eq_quests),
        "chapters": [{"name": k, "quests": v} for k, v in sorted(chapters.items())],
        "task_types": [[t, c] for t, c in sorted(task_freq.items(), key=lambda x: (-x[1], x[0]))],
        "reward_types": [[t, c] for t, c in sorted(reward_freq.items(), key=lambda x: (-x[1], x[0]))],
        "audit": audit,
        "caches": {
            "mods": mods_cache is not None,
            "existing_quests": eq_cache is not None,
            "audit_report": report is not None,
        },
    }


def _truncate(items: list, n: int) -> tuple[list, int]:
    return items[:n], max(0, len(items) - n)


def render_text(b: dict) -> str:
    lines: list[str] = [
        f"📦 FTB Quests pack briefing: {b['packroot']}",
        f"   format: {b['format']}   mods: {b['mod_count']}   "
        f"chapters: {b['chapter_count']}   quests: {b['quest_count']}",
    ]
    if b["mod_names"]:
        shown, rest = _truncate(b["mod_names"], 8)
        line = "   mods: " + ", ".join(shown)
        if rest:
            line += f", … (+{rest} more)"
        lines.append(line)
    if b["chapters"]:
        lines.append("   chapters:")
        for ch in b["chapters"]:
            lines.append(f"     {ch['name']:<28} {ch['quests']} quests")
    if b["task_types"]:
        shown, rest = _truncate(b["task_types"], 6)
        line = "   task types: " + ", ".join(f"{t} ({c})" for t, c in shown)
        if rest:
            line += f", … (+{rest})"
        lines.append(line)
    if b["reward_types"]:
        shown, rest = _truncate(b["reward_types"], 6)
        line = "   reward types: " + ", ".join(f"{t} ({c})" for t, c in shown)
        if rest:
            line += f", … (+{rest})"
        lines.append(line)
    a = b.get("audit")
    if a:
        verdict = "✅ identical" if a["identical"] else "⚠️ differs"
        lines.append(f"   audit: {verdict} (audited {a['audited_at']}); "
                     f"DLC patterns {a['dlc_patterns']}, target {a['target_patterns']}")
    c = b["caches"]
    def flag(ok, cmd):
        return "✓" if ok else f"✗ (run {cmd})"
    lines.append("   caches: " + "  ".join([
        f"mods {flag(c['mods'], 'extract_mods.py')}",
        f"existing_quests {flag(c['existing_quests'], 'index_quests.py')}",
        f"audit_report {flag(c['audit_report'], 'audit_diff.py')}",
    ]))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Compact pack briefing from .ftbq-cache/ (token-saving)")
    p.add_argument("packroot", type=Path, help="Modpack root")
    p.add_argument("--json", action="store_true", help="Machine-readable")
    args = p.parse_args(argv)

    root = args.packroot.resolve()
    quests_dir = root / "config" / "ftbquests" / "quests"
    if not quests_dir.is_dir():
        print(f"error: quests dir not found: {quests_dir}", file=sys.stderr)
        return 2

    b = build_briefing(root)
    if args.json:
        print(json.dumps(b, indent=2, ensure_ascii=False))
    else:
        print(render_text(b))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
