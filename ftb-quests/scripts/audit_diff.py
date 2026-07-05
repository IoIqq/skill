"""Diff a DLC source pack against an installed FTB Quests pack (Task A)
and report description ``&e<item_id><中文名>&r`` patterns (Task B).

The codegraph ``query`` step, with a persisted verdict so a NEW
conversation doesn't re-audit:

* **resume (default)** — if ``.ftbq-cache/audit_report.json5`` exists AND
  both packs' indexes are fresh (on-disk files unchanged) AND the report's
  recorded ``pack_hash`` still matches, print the SAVED verdict and exit.
  No re-audit, no re-read of quest files. This is what keeps a new session
  from redoing the full audit.
* **full audit** — when there's no saved report or a pack is stale, load
  (rebuild if needed) both indexes, compute the diff + item report, SAVE
  the report, and print. ``--force`` skips resume and always recomputes.

Path resolution: arguments are modpack roots (containing
``config/ftbquests/quests``); ``--quests-dir`` targets explicit quests dirs.

Usage::

    python scripts/audit_diff.py <dlc_pack> <target_pack>   # audit (or resume if fresh)
    python scripts/audit_diff.py <dlc_pack>                 # target from remembered pair
    python scripts/audit_diff.py <dlc_pack> <target> --remember
    python scripts/audit_diff.py <dlc_pack> <target> --force  # skip resume, recompute
    python scripts/audit_diff.py --json <dlc_pack> <target>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq import audit as ftbq_audit  # noqa: E402


def _resolve_quests_dir(arg: Path, *, is_quests_dir: bool) -> Path:
    arg = arg.resolve()
    if is_quests_dir:
        return arg
    # Treat as a modpack root: <root>/config/ftbquests/quests
    return (arg / "config" / "ftbquests" / "quests").resolve()


def _load_or_build(quests_dir: Path, *, rebuild: bool,
                    quiet: bool) -> tuple[dict, str]:
    """Return (index, source_label). Rebuilds if stale/absent unless
    ``rebuild`` is False (then a stale/absent index is an error)."""
    cached = ftbq_audit.load_index(quests_dir)
    if cached is not None:
        fresh, _changed = ftbq_audit.check_freshness(quests_dir, cached)
        if fresh:
            return cached, "fresh"
        if not rebuild:
            print(f"error: index stale for {quests_dir} (run audit_index.py "
                  f"first, or drop --no-rebuild)", file=sys.stderr)
            sys.exit(2)
        if not quiet:
            print(f"  {quests_dir}: index stale — rebuilding...",
                  file=sys.stderr)
    elif not rebuild:
        print(f"error: no index for {quests_dir} (run audit_index.py first, "
              f"or drop --no-rebuild)", file=sys.stderr)
        sys.exit(2)
    else:
        if not quiet:
            print(f"  {quests_dir}: no index — building...", file=sys.stderr)
    index = ftbq_audit.build_audit_index(quests_dir)
    ftbq_audit.write_index(quests_dir, index)
    return index, "rebuilt"


def _resolve_pair(args: argparse.Namespace) -> tuple[Path, Path]:
    """Resolve (dlc_quests_dir, target_quests_dir) from CLI args or the
    remembered pack pair."""
    dlc_q: Path | None = None
    target_q: Path | None = None
    if args.dlc:
        dlc_q = _resolve_quests_dir(args.dlc, is_quests_dir=args.quests_dir)
    if args.target:
        target_q = _resolve_quests_dir(args.target,
                                        is_quests_dir=args.quests_dir)
    if dlc_q and target_q:
        return dlc_q, target_q
    if dlc_q and not target_q:
        pair = ftbq_audit.load_pack_pair(dlc_q)
        if pair and pair.get("target_quests_dir"):
            return dlc_q, Path(pair["target_quests_dir"])
        print(f"error: no remembered target for DLC {dlc_q}; pass the target "
              f"pack or run with --remember first", file=sys.stderr)
        sys.exit(2)
    # Neither given — look for a pack pair in CWD's .ftbq-cache/.
    cwd_pair = ftbq_audit.load_pack_pair(Path(".ftbq-cache"))
    if cwd_pair:
        dlc = cwd_pair.get("dlc_quests_dir")
        tgt = cwd_pair.get("target_quests_dir")
        if dlc and tgt:
            return Path(dlc), Path(tgt)
    print("error: need <dlc_pack> <target_pack> (or a remembered pair in "
          "CWD/.ftbq-cache/pack_pair.json5)", file=sys.stderr)
    sys.exit(2)


def _render_report_text(report: dict, source: str) -> str:
    dlc = report.get("dlc", {})
    tgt = report.get("target", {})
    ta = report.get("task_a", {})
    tb = report.get("task_b", {})
    lines: list[str] = [
        f"📦 FTB Quests audit: DLC source vs installed   ({source})",
        f"   DLC source : {dlc.get('quests_dir', '?')}   "
        f"({dlc.get('format', '?')}, {dlc.get('file_count', 0)} files, "
        f"{dlc.get('chapter_count', 0)} ch, {dlc.get('quest_count', 0)} quests)",
        f"   Installed  : {tgt.get('quests_dir', '?')}   "
        f"({tgt.get('format', '?')}, {tgt.get('file_count', 0)} files, "
        f"{tgt.get('chapter_count', 0)} ch, {tgt.get('quest_count', 0)} quests)",
        "",
        "Task A — file diff:",
    ]
    if ta.get("identical"):
        lines.append(f"   ✅ IDENTICAL — installed matches DLC source "
                     f"({dlc.get('file_count', 0)} files)")
    else:
        lines.append("   ⚠️  DIFFERS:")
        if ta.get("only_in_dlc"):
            lines.append(f"      only in DLC source ({len(ta['only_in_dlc'])}):")
            for p in ta["only_in_dlc"]:
                lines.append(f"         {p}")
        if ta.get("only_in_installed"):
            lines.append(f"      only in installed ({len(ta['only_in_installed'])}):")
            for p in ta["only_in_installed"]:
                lines.append(f"         {p}")
        if ta.get("content_differs"):
            lines.append(f"      content differs ({len(ta['content_differs'])}):")
            for d in ta["content_differs"]:
                lines.append(f"         {d['path']}")
    lines.append("")
    lines.append("Task B — description item-ID patterns:")
    for label, side in (("DLC source", tb.get("dlc", {})),
                        ("Installed", tb.get("target", {}))):
        lines.append(f"   {label}: {side.get('quest_count', 0)} quest(s), "
                     f"{side.get('pattern_count', 0)} pattern(s)")
        for q in side.get("quests", []):
            pats = ", ".join(f"{p['item_id']}→{p['name']}"
                              for p in q.get("item_patterns", [])[:8])
            if len(q.get("item_patterns", [])) > 8:
                pats += f", … (+{len(q['item_patterns']) - 8})"
            lines.append(f"      {q.get('id', '?')} ({q.get('chapter', '')}): {pats}")
    return "\n".join(lines)


def _report_json(report: dict, source: str) -> str:
    payload = {"source": source}
    payload.update(report)
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Diff DLC source vs installed FTB Quests pack + item-pattern report")
    p.add_argument("dlc", type=Path, nargs="?",
                    help="DLC source modpack root (or quests dir with --quests-dir)")
    p.add_argument("target", type=Path, nargs="?",
                    help="Installed target modpack root (or quests dir)")
    p.add_argument("--quests-dir", action="store_true",
                    help="Args are explicit quests dirs, not modpack roots")
    p.add_argument("--remember", action="store_true",
                    help="Save the pair to <dlc>/.ftbq-cache/pack_pair.json5")
    p.add_argument("--no-rebuild", action="store_true",
                    help="Error if an index is missing/stale instead of rebuilding")
    p.add_argument("--force", action="store_true",
                    help="Skip the resume check; always recompute the audit")
    p.add_argument("--json", action="store_true",
                    help="Machine-readable output")
    p.add_argument("--quiet", "-q", action="store_true")
    args = p.parse_args(argv)

    dlc_q, target_q = _resolve_pair(args)

    if args.remember:
        ftbq_audit.save_pack_pair(dlc_q, target_q)
        if not args.quiet and not args.json:
            print(f"remembered pair → {ftbq_audit.pack_pair_path(dlc_q)}",
                  file=sys.stderr)

    # Resume: if a saved report exists AND both indexes are fresh AND the
    # report's pack_hashes still match, print the saved verdict and exit —
    # no re-audit, no re-read of quest files. This is what keeps a new
    # conversation from re-running the full audit.
    if not args.force:
        report = ftbq_audit.load_report(dlc_q)
        dlc_idx = ftbq_audit.load_index(dlc_q)
        tgt_idx = ftbq_audit.load_index(target_q)
        if report is not None and dlc_idx and tgt_idx:
            dlc_fresh, _ = ftbq_audit.check_freshness(dlc_q, dlc_idx)
            tgt_fresh, _ = ftbq_audit.check_freshness(target_q, tgt_idx)
            if ftbq_audit.report_fresh(report, dlc_idx, tgt_idx,
                                         dlc_fresh, tgt_fresh):
                src = f"resumed from {report.get('audited_at', '?')}"
                if args.json:
                    print(_report_json(report, src))
                else:
                    print(_render_report_text(report, src))
                return 0 if report.get("task_a", {}).get("identical") else 1

    # Full audit: load/build indexes (rebuild stale), compute, SAVE report.
    dlc_idx, dlc_src = _load_or_build(dlc_q, rebuild=not args.no_rebuild,
                                        quiet=args.quiet)
    tgt_idx, tgt_src = _load_or_build(target_q, rebuild=not args.no_rebuild,
                                         quiet=args.quiet)
    diff = ftbq_audit.diff_indexes(dlc_idx, tgt_idx)
    dlc_item = ftbq_audit.item_report(dlc_idx)
    tgt_item = ftbq_audit.item_report(tgt_idx)
    report = ftbq_audit.build_report(dlc_idx, tgt_idx, diff,
                                       dlc_item, tgt_item)
    ftbq_audit.save_report(dlc_q, report)

    src = f"fresh ({dlc_src}/{tgt_src})"
    if args.json:
        print(_report_json(report, src))
    else:
        print(_render_report_text(report, src))
    return 0 if diff["identical"] else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
