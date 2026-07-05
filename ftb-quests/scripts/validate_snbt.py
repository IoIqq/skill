#!/usr/bin/env python3
"""FTB Quests SNBT format validator.

Checks basic SNBT syntax: bracket matching, key quoting, string quoting, NBT tag format.
Usage: python validate_snbt.py <file_path> [--json]
"""

import argparse
import json
import re
import sys


def validate_snbt(content, filepath=""):
    errors = []
    warnings = []

    # Check bracket balance
    brace_count = 0
    bracket_count = 0
    in_string = False
    escape_next = False

    for i, ch in enumerate(content):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\":
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if brace_count < 0:
                errors.append(f"Unmatched closing brace at position {i}")
        elif ch == "[":
            bracket_count += 1
        elif ch == "]":
            bracket_count -= 1
            if bracket_count < 0:
                errors.append(f"Unmatched closing bracket at position {i}")

    if brace_count != 0:
        errors.append(f"Unbalanced braces: {brace_count} unclosed")
    if bracket_count != 0:
        errors.append(f"Unbalanced brackets: {bracket_count} unclosed")
    if in_string:
        errors.append("Unterminated string literal")

    # Check that keys are unquoted (FTB Quests convention)
    lines = content.split("\n")
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("#"):
            continue

        # Check for quoted keys (warning, not error)
        key_match = re.match(r'^"([^"]+)"\s*:', stripped)
        if key_match:
            warnings.append(
                f"Line {line_num}: Quoted key '{key_match.group(1)}' - FTB Quests uses unquoted keys"
            )

    # Check NBT tag format if present
    nbt_pattern = re.findall(r'"[^"]*\{[^"]*\}"', content)
    for nbt in nbt_pattern:
        inner = nbt[1:-1]
        # Check for type suffix markers (s/b/i/f/d)
        type_markers = re.findall(r'(?<![a-zA-Z])[0-9]+([sbidflSBIDFL])(?!\w)', inner)
        if not type_markers and re.search(r'[0-9]', inner):
            warnings.append(f"Possible NBT value without type marker: {nbt[:50]}...")

    return {"filepath": filepath, "valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description="FTB Quests SNBT Validator")
    parser.add_argument("file", help="Path to SNBT file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    result = validate_snbt(content, args.file)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result["valid"]:
            print(f"[OK] {args.file}: Valid SNBT")
        else:
            print(f"[FAIL] {args.file}: Invalid SNBT")
        for e in result["errors"]:
            print(f"  ERROR: {e}")
        for w in result["warnings"]:
            print(f"  WARN: {w}")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()