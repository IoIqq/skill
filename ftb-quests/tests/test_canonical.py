"""Tests for ftbq.canonical: byte-stable JSON5 emitter."""

from __future__ import annotations

from ftbq.canonical import canonical_json, dumps


def test_emit_simple_object():
    out = dumps({"a": 1, "b": 2})
    assert "a: 1" in out
    assert "b: 2" in out


def test_emit_sorts_keys_by_default():
    out = dumps({"b": 1, "a": 2})
    a_pos = out.find("a:")
    b_pos = out.find("b:")
    assert 0 <= a_pos < b_pos


def test_emit_key_order_override():
    """Explicit order takes precedence over alphabetical."""
    out = dumps({"a": 1, "b": 2, "c": 3}, key_order=["c", "a"])
    c_pos = out.find("c:")
    a_pos = out.find("a:")
    b_pos = out.find("b:")
    assert 0 <= c_pos < a_pos < b_pos


def test_emit_byte_stable():
    obj = {"alpha": 1, "beta": [1, 2, 3], "gamma": {"x": 1.0}}
    assert dumps(obj) == dumps(obj)


def test_emit_floats_one_decimal():
    out = dumps({"x": 0.0, "y": 1.0, "z": -2.5})
    assert "x: 0.0" in out
    assert "y: 1.0" in out
    assert "z: -2.5" in out


def test_emit_unquoted_safe_keys():
    out = dumps({"id": "abc", "x": 1})
    assert "id:" in out
    assert "x:" in out


def test_emit_quoted_keys_with_dots():
    """Lang keys like 'quest.HEX.title' must stay quoted."""
    out = dumps({"chapter.ABCDEF.title": "Start"})
    assert '"chapter.ABCDEF.title":' in out


def test_emit_quote_keys_flag_forces_all():
    out = dumps({"a": 1}, quote_keys=True)
    assert '"a":' in out


def test_emit_trailing_comma():
    out = dumps({"a": 1, "b": 2})
    # Both inner entries end with a comma, including the last.
    inner = out.strip().splitlines()[1:-1]
    assert all(line.rstrip().endswith(",") for line in inner)


def test_emit_no_trailing_comma_when_disabled():
    out = dumps([1, 2, 3], trailing_comma=False)
    assert not out.rstrip()[:-1].rstrip().endswith(",")


def test_emit_empty_object_array():
    assert dumps({}) == "{}"
    assert dumps([]) == "[]"


def test_emit_string_escapes():
    out = dumps({"s": 'a "quote"'})
    assert '\\"quote\\"' in out


def test_canonical_json_stable():
    a = {"a": 1, "b": 2}
    b = {"b": 2, "a": 1}
    assert canonical_json(a) == canonical_json(b)


def test_emit_nested():
    out = dumps({"chapters": [{"id": "X", "quests": [{"id": "Y"}]}]})
    assert "chapters:" in out
    assert "quests:" in out


def test_emit_per_path_key_order():
    """Per-path key order lets chapter files put 'id'/'filename' first
    while every quest puts 'id' first."""
    obj = {"id": "X", "filename": "f", "quests": [{"id": "Q", "x": 0.0}]}
    out = dumps(obj,
                 key_order=["id", "filename"],
                 per_path_key_order={"quests.[]": ["id", "x"]})
    # Top level: id before filename before alphabetical rest.
    assert out.find("id:") < out.find("filename:")
    # Inside a quest: id before x.
    quest_start = out.find("{", out.find("quests:"))
    assert out.find("id:", quest_start) < out.find("x:", quest_start)
