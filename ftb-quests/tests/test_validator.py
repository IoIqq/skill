"""Tests for scripts/validate_quests.py.

One scenario per diagnostic code (E_*). Each scenario constructs a
minimal quests/ tree on disk, runs the validator, and asserts the
expected code shows up.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "validate_quests", ROOT / "scripts" / "validate_quests.py")
validate_quests = importlib.util.module_from_spec(_spec)
sys.modules["validate_quests"] = validate_quests
_spec.loader.exec_module(validate_quests)


def _write(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _validate(quests_dir: Path):
    book = validate_quests.load_book(quests_dir)
    return validate_quests.Validator(book).run()


def _has_code(diags, code: str) -> bool:
    return any(d.code == code for d in diags)


def _scaffold(tmp_path: Path, *, chapter_body: str = None) -> Path:
    out = tmp_path / "quests"
    _write(out / "data.json5", "{ default_consume_items: true }\n")
    if chapter_body is None:
        chapter_body = (
            '{\n'
            '  id: "0123456789ABCDEF",\n'
            '  filename: "intro",\n'
            '  default_quest_shape: "circle",\n'
            '  group: "",\n'
            '  order_index: 0,\n'
            '  quests: [],\n'
            '}\n'
        )
    _write(out / "chapters" / "intro.json5", chapter_body)
    _write(out / "lang" / "en_us" / "quests.json5",
            '{ "chapter.0123456789ABCDEF.title": "Intro" }\n')
    return out


def test_baseline_clean(tmp_path: Path):
    out = _scaffold(tmp_path)
    diags = _validate(out)
    errors = [d for d in diags if d.severity == "error"]
    assert errors == []


def test_e_file_missing(tmp_path: Path):
    out = tmp_path / "quests"
    (out / "chapters").mkdir(parents=True)
    diags = _validate(out)
    assert _has_code(diags, "E_FILE_MISSING")


def test_e_dir_missing(tmp_path: Path):
    out = tmp_path / "quests"
    out.mkdir()
    _write(out / "data.json5", "{}\n")
    diags = _validate(out)
    assert _has_code(diags, "E_DIR_MISSING")


def test_e_filename_mismatch(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "WRONG_NAME",\n'
        '  default_quest_shape: "circle",\n  quests: [],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_FILENAME_MISMATCH")


def test_e_id_format(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "lowercase16chars",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_ID_FORMAT")


def test_e_id_dup(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "DEADBEEFDEADBEEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "DEADBEEFDEADBEEF", x: 0.0, y: 0.0,\n'
        '      dependencies: [], tasks: [], rewards: [] },\n  ],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_ID_DUP")


def test_e_dep_missing_with_fuzzy_hint(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      dependencies: ["BBBBBBBBBBBBBBBA"],\n'
        '      tasks: [], rewards: [] },\n'
        '    { id: "BBBBBBBBBBBBBBBB", x: 1.5, y: 0.0,\n'
        '      dependencies: [], tasks: [], rewards: [] },\n  ],\n}\n'
    ))
    diags = _validate(out)
    dep_errs = [d for d in diags if d.code == "E_DEP_MISSING"]
    assert dep_errs
    assert dep_errs[0].hint is not None
    assert "BBBBBBBBBBBBBBBB" in dep_errs[0].hint


def test_e_item_bare_string(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      dependencies: [],\n'
        '      tasks: [{ id: "1111111111111111", type: "ftbquests:item",\n'
        '                item: "minecraft:oak_log", count: 4 }],\n'
        '      rewards: [] },\n  ],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_ITEM_BARE_STRING")


def test_e_type_suffix(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0d, y: 0.0,\n'
        '      dependencies: [], tasks: [], rewards: [] },\n  ],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_TYPE_SUFFIX")


def test_e_inline_text_modern(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      title: "Inline Title (ignored on modern)",\n'
        '      dependencies: [], tasks: [], rewards: [] },\n  ],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_INLINE_TEXT_MODERN")


def test_e_coord_dup(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      dependencies: [], tasks: [], rewards: [] },\n'
        '    { id: "BBBBBBBBBBBBBBBB", x: 0.0, y: 0.0,\n'
        '      dependencies: [], tasks: [], rewards: [] },\n  ],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_COORD_DUP")


def test_e_lang_missing_title(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      dependencies: [], tasks: [], rewards: [] },\n  ],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_LANG_MISSING_TITLE")


def test_e_lang_orphan(tmp_path: Path):
    out = _scaffold(tmp_path)
    _write(out / "lang" / "en_us" / "quests.json5",
            '{ "chapter.0123456789ABCDEF.title": "Intro",\n'
            '  "quest.FFFFFFFFFFFFFFFF.title": "Orphan" }\n')
    diags = _validate(out)
    assert _has_code(diags, "E_LANG_ORPHAN")


def test_e_lang_no_warning_for_tasks_or_rewards(tmp_path: Path):
    """task/reward titles don't render in modern FTB Quests, so no
    E_LANG_MISSING_TITLE for them."""
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      dependencies: [],\n'
        '      tasks: [{ id: "1111111111111111", type: "ftbquests:checkmark" }],\n'
        '      rewards: [{ id: "2222222222222222", type: "ftbquests:xp", xp: 100 }] },\n'
        '  ],\n}\n'
    ))
    _write(out / "lang" / "en_us" / "quests.json5",
            '{ "chapter.0123456789ABCDEF.title": "Intro",\n'
            '  "quest.AAAAAAAAAAAAAAAA.title": "Q" }\n')
    diags = _validate(out)
    miss_diags = [d for d in diags if d.code == "E_LANG_MISSING_TITLE"]
    for d in miss_diags:
        assert "1111111111111111" not in d.message
        assert "2222222222222222" not in d.message


def test_double_slash_inside_string_is_not_a_comment(tmp_path: Path):
    """Regression for the OLD validator's regex bug: stripping // would
    also eat // inside strings, corrupting URLs."""
    out = _scaffold(tmp_path)
    _write(out / "data.json5",
            '{ wiki_url: "http://wiki.example.com//page" }\n')
    diags = _validate(out)
    parse_errs = [d for d in diags if d.code == "E_PARSE"]
    assert parse_errs == []


def test_text_output_format(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "lowercase16chars",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [],\n}\n'
    ))
    diags = _validate(out)
    text = validate_quests.report_text(diags)
    assert "[E_ID_FORMAT]" in text
    assert "intro.json5:" in text


def test_json_output_format(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "lowercase16chars",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [],\n}\n'
    ))
    diags = _validate(out)
    txt = validate_quests.report_json(diags)
    parsed = json.loads(txt)
    assert any(d["code"] == "E_ID_FORMAT" for d in parsed)
    for d in parsed:
        assert {"file", "line", "col", "severity", "code",
                 "message"}.issubset(d)


def test_strict_promotes_warnings(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      title: "inline",\n'
        '      dependencies: [], tasks: [], rewards: [] },\n  ],\n}\n'
    ))
    _write(out / "lang" / "en_us" / "quests.json5",
            '{ "chapter.0123456789ABCDEF.title": "Intro",\n'
            '  "quest.AAAAAAAAAAAAAAAA.title": "Q" }\n')
    diags = _validate(out)
    has_error = any(d.severity == "error" for d in diags)
    assert not has_error
    assert validate_quests.exit_code(diags, strict=False) == 0
    assert validate_quests.exit_code(diags, strict=True) == 1


def test_fix_bare_string_item(tmp_path: Path):
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      dependencies: [],\n'
        '      tasks: [{ id: "1111111111111111", type: "ftbquests:item",\n'
        '                item: "minecraft:oak_log", count: 4 }],\n'
        '      rewards: [] },\n  ],\n}\n'
    ))
    book = validate_quests.load_book(out)
    diags = validate_quests.Validator(book).run()
    applied = validate_quests.Fixer().apply(book, diags)
    assert applied >= 1

    text = (out / "chapters" / "intro.json5").read_text(encoding="utf-8")
    assert '{ id: "minecraft:oak_log", count: 1 }' in text
    assert 'item: "minecraft:oak_log"' not in text

    diags2 = _validate(out)
    assert not _has_code(diags2, "E_ITEM_BARE_STRING")


# ---- reward tables -----------------------------------------------------


def test_e_table_missing(tmp_path: Path):
    """A `table_id` that doesn't match any reward table → E_TABLE_MISSING."""
    out = _scaffold(tmp_path, chapter_body=(
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      dependencies: [],\n      tasks: [],\n'
        '      rewards: [{ id: "BBBBBBBBBBBBBBBB", type: "ftbquests:random",\n'
        '                  table_id: 999 }] },\n  ],\n}\n'
    ))
    diags = _validate(out)
    assert _has_code(diags, "E_TABLE_MISSING")


def test_valid_table_id_no_diag(tmp_path: Path):
    """A `table_id` matching a reward table's id long → no E_TABLE_MISSING."""
    tbl_hex = "0123456789ABCDEF"
    tid_long = int(tbl_hex, 16)
    body = (
        '{\n  id: "0123456789ABCDEF",\n  filename: "intro",\n'
        '  default_quest_shape: "circle",\n  quests: [\n'
        '    { id: "AAAAAAAAAAAAAAAA", x: 0.0, y: 0.0,\n'
        '      dependencies: [],\n      tasks: [],\n'
        '      rewards: [{ id: "BBBBBBBBBBBBBBBB", type: "ftbquests:loot",\n'
        '                  table_id: ' + str(tid_long) + ' }] },\n  ],\n}\n'
    )
    out = _scaffold(tmp_path, chapter_body=body)
    _write(out / "reward_tables" / "rt.json5",
           '{ id: "0123456789ABCDEF", rewards: [] }\n')
    diags = _validate(out)
    assert not _has_code(diags, "E_TABLE_MISSING")


def test_reward_table_bad_id_format(tmp_path: Path):
    out = _scaffold(tmp_path)
    _write(out / "reward_tables" / "rt.json5",
           '{ id: "NOT_HEX", rewards: [] }\n')
    diags = _validate(out)
    assert _has_code(diags, "E_ID_FORMAT")


def test_reward_table_entry_missing_id(tmp_path: Path):
    out = _scaffold(tmp_path)
    _write(out / "reward_tables" / "rt.json5",
           '{ id: "0123456789ABCDEF", rewards: [ { type: "ftbquests:item" } ] }\n')
    diags = _validate(out)
    assert _has_code(diags, "E_ID_MISSING")

