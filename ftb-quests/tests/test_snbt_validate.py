"""SNBT validator scenarios (1.20.1 format).

The structured validator (scripts/validate_quests.py) parses ``.snbt`` via
ftbq.snbt and runs the same diagnostic catalog as the JSON5 path. These
tests pin the SNBT-specific behaviour: format detection, the checks that
must NOT fire for SNBT (type suffixes are legal, inline text is expected),
and the checks that still do (dup id, missing dependency, parse error,
missing data file).
"""

from __future__ import annotations

import importlib.util
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


def _codes(diags):
    return {d.code for d in diags}


def _make(tmp_path: Path, *, data=True, chapter_body: str | None = None):
    qd = tmp_path / "quests"
    (qd / "chapters").mkdir(parents=True, exist_ok=True)
    if data:
        (qd / "data.snbt").write_text("{ version: 13 }\n", encoding="utf-8")
    if chapter_body is not None:
        (qd / "chapters" / "c.snbt").write_text(chapter_body, encoding="utf-8")
    book = validate_quests.load_book(qd)
    return book, validate_quests.Validator(book).run()


GOOD_CHAPTER = """{
  id: "CCCCCCCCCCCCCCCC"
  filename: "c"
  default_quest_shape: "circle"
  quests: [
    {
      id: "AAAAAAAAAAAAAAAA"
      x: 0.0d
      y: 0.0d
      title: "A"
      description: ["one", "two"]
      tasks: [
        { id: "1111111111111111", type: "ftbquests:item",
          item: { id: "minecraft:stone", count: 1 }, count: 4L }
      ]
      rewards: []
    }
  ]
}
"""


def test_detects_snbt_format_and_validates_clean(tmp_path: Path):
    book, diags = _make(tmp_path, chapter_body=GOOD_CHAPTER)
    assert book.format == "snbt"
    assert _codes(diags) == set(), [d.format_text() for d in diags]


def test_type_suffixes_not_flagged_for_snbt(tmp_path: Path):
    # 4L / 0.0d / 1b are legal SNBT — E_TYPE_SUFFIX must not fire.
    _, diags = _make(tmp_path, chapter_body=GOOD_CHAPTER)
    assert "E_TYPE_SUFFIX" not in _codes(diags)


def test_inline_text_not_flagged_for_snbt(tmp_path: Path):
    # title/description live inline in 1.20.1 — E_INLINE_TEXT_MODERN is the
    # JSON5-only check that warns inline text is ignored.
    _, diags = _make(tmp_path, chapter_body=GOOD_CHAPTER)
    assert "E_INLINE_TEXT_MODERN" not in _codes(diags)


def test_dup_id_fires(tmp_path: Path):
    body = """{
  id: "CCCCCCCCCCCCCCCC"
  filename: "c"
  default_quest_shape: "circle"
  quests: [
    { id: "AAAAAAAAAAAAAAAA", x: 0.0d, y: 0.0d, tasks: [], rewards: [] }
    { id: "AAAAAAAAAAAAAAAA", x: 1.0d, y: 0.0d, tasks: [], rewards: [] }
  ]
}
"""
    _, diags = _make(tmp_path, chapter_body=body)
    assert "E_ID_DUP" in _codes(diags)


def test_missing_dependency_fires(tmp_path: Path):
    body = GOOD_CHAPTER.replace(
        "      tasks: [",
        '      dependencies: ["ZZZZZZZZZZZZZZZZ"]\n      tasks: [', 1)
    _, diags = _make(tmp_path, chapter_body=body)
    assert "E_DEP_MISSING" in _codes(diags)


def test_parse_error_fires(tmp_path: Path):
    bad = "{ id: \"X\" filename: \"c\" "  # unclosed
    book, diags = _make(tmp_path, chapter_body=bad)
    assert "E_PARSE" in _codes(diags)


def test_missing_data_snbt_fires(tmp_path: Path):
    _, diags = _make(tmp_path, data=False, chapter_body=GOOD_CHAPTER)
    assert "E_FILE_MISSING" in _codes(diags)
    msg = next(d for d in diags if d.code == "E_FILE_MISSING")
    assert "data.snbt" in msg.message


def test_bad_id_format_fires(tmp_path: Path):
    body = GOOD_CHAPTER.replace("AAAAAAAAAAAAAAAA", "TOOSHORT")
    _, diags = _make(tmp_path, chapter_body=body)
    assert "E_ID_FORMAT" in _codes(diags)
