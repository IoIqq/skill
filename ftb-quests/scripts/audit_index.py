"""Build or refresh the audit index for one FTB Quests pack.

The codegraph ``analyze`` step: scan the pack once, cache file checksums +
description item-ID patterns to ``.ftbq-cache/audit_index.json5``.
``--status`` re-stats every file and reports fresh/stale WITHOUT rewriting —
the caller (audit_diff.py or the skill) rebuilds only when stale.

Usage::

    python scripts/audit_index.py <modpack_dir>
    python scripts/audit_index.py <modpack_dir> --status
    python scripts/audit_index.py <modpack_dir> --output <quests_dir>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq import audit as ftbq_audit  # noqa: E402


def _resolve_quests_dir(modpack_dir: Path, output: Path | None) -> Path:
    return (output or modpack_dir / "config" / "ftbquests" / "quests").resolve()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Build/refresh the FTB Quests audit index (.ftbq-cache/audit_index.json5)")
    p.add_argument("modpack_dir", type=Path,
                    help="Modpack root (containing config/ftbquests/quests)")
    p.add_argument("--output", "-o", type=Path,
                    help="Quests dir (default: <modpack>/config/ftbquests/quests)")
    p.add_argument("--status", action="store_true",
                    help="Only check freshness; do not rewrite the index")
    p.add_argument("--quiet", "-q", action="store_true")
    args = p.parse_args(argv)

    quests_dir = _resolve_quests_dir(args.modpack_dir, args.output)
    if not quests_dir.is_dir():
        print(f"error: quests dir not found: {quests_dir}", file=sys.stderr)
        return 2

    if args.status:
        cached = ftbq_audit.load_index(quests_dir)
        if cached is None:
            print(f"stale: no cached index at {quests_dir}/.ftbq-cache/")
            return 1
        fresh, changed = ftbq_audit.check_freshness(quests_dir, cached)
        if fresh:
            if not args.quiet:
                print(f"fresh: {cached.get('file_count', 0)} files, "
                      f"index scanned {cached.get('scanned_at', '?')}")
            return 0
        print(f"stale: {len(changed)} file(s) changed:")
        for rel in changed:
            print(f"  {rel}")
        return 1

    index = ftbq_audit.build_audit_index(quests_dir)
    path = ftbq_audit.write_index(quests_dir, index)
    if not args.quiet:
        print(f"Indexed {index['file_count']} files → {path}")
        qcount = len(index["quests"])
        pcount = sum(len(q["item_patterns"]) for q in index["quests"])
        print(f"  format: {index['format']}   "
              f"quests w/ item patterns: {qcount}   "
              f"total patterns: {pcount}")
        if qcount and not args.quiet:
            for q in index["quests"][:5]:
                print(f"  {q['id']} ({q['chapter']}): "
                      f"{len(q['item_patterns'])} pattern(s)")
            if qcount > 5:
                print(f"  … and {qcount - 5} more")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
