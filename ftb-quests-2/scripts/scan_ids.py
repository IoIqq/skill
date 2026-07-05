#!/usr/bin/env python3
"""FTB Quests ID scanner and conflict detector.

Scans all .snbt files in a directory, extracts all IDs, and detects conflicts.
Usage: python scan_ids.py <directory> [--json]
"""

import argparse
import json
import os
import re
import sys


def extract_ids_from_snbt(content):
    ids = []
    # Match id: "XXXXXXXX" pattern
    id_pattern = re.findall(r'\bid:\s*"([A-Fa-f0-9]+)"', content)
    ids.extend(id_pattern)
    return ids


def scan_directory(directory):
    all_ids = {}
    conflicts = []
    files_scanned = 0

    for root, dirs, files in os.walk(directory):
        for fname in files:
            if not fname.endswith(".snbt"):
                continue
            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, directory)
            files_scanned += 1

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            ids = extract_ids_from_snbt(content)
            for quest_id in ids:
                if quest_id in all_ids:
                    conflicts.append({
                        "id": quest_id,
                        "files": [all_ids[quest_id], rel_path],
                    })
                else:
                    all_ids[quest_id] = rel_path

    return {
        "directory": directory,
        "files_scanned": files_scanned,
        "total_ids": len(all_ids),
        "conflicts": conflicts,
        "ids": all_ids,
    }


def main():
    parser = argparse.ArgumentParser(description="FTB Quests ID Scanner")
    parser.add_argument("directory", help="Directory containing .snbt files")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory", file=sys.stderr)
        sys.exit(1)

    result = scan_directory(args.directory)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Scanned {result['files_scanned']} files, found {result['total_ids']} IDs")
        if result["conflicts"]:
            print(f"\n[WARN] {len(result['conflicts'])} conflicts detected:")
            for conflict in result["conflicts"]:
                print(f"  ID {conflict['id']}: {conflict['files']}")
        else:
            print("[OK] No conflicts detected")

    sys.exit(1 if result["conflicts"] else 0)


if __name__ == "__main__":
    main()
