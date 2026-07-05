#!/usr/bin/env python3
"""FTB Quests hash-based ID generator.

Generates deterministic 8-char hex IDs from quest content.
Usage: python hash_id.py --mod <mod_id> --item <item> --type <task_type> --chapter <chapter_id> --title <quest_title>
"""

import hashlib
import argparse
import json
import sys


def generate_id(mod_id, item_name, task_type, chapter_id, quest_title):
    raw = f"{mod_id}:{item_name}:{task_type}:{chapter_id}:{quest_title}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8].upper()


def main():
    parser = argparse.ArgumentParser(description="FTB Quests Hash ID Generator")
    parser.add_argument("--mod", required=True, help="Mod ID (e.g., create)")
    parser.add_argument("--item", required=True, help="Item/entity name (e.g., shaft)")
    parser.add_argument("--type", required=True, help="Task type (e.g., item, kill)")
    parser.add_argument("--chapter", required=True, help="Chapter ID")
    parser.add_argument("--title", required=True, help="Quest title")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    quest_id = generate_id(args.mod, args.item, args.type, args.chapter, args.title)

    if args.json:
        result = {
            "id": quest_id,
            "input": {
                "mod_id": args.mod,
                "item": args.item,
                "task_type": args.type,
                "chapter_id": args.chapter,
                "quest_title": args.title,
            },
        }
        print(json.dumps(result, indent=2))
    else:
        print(quest_id)


if __name__ == "__main__":
    main()