"""Tests for ftbq.snbt — the SNBT parser (port of FTB-Library SNBTParser).

Covers: compounds, lists, quoted/unquoted strings, escapes, suffixed
numbers, booleans, null, ``#`` / ``//`` comments, optional commas, ``=``
separator, typed arrays, and the error cases (unterminated string, unclosed
compound, EOF, non-numeric array entry).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ftbq.snbt import SnbtError, parse_snbt  # noqa: E402


def p(s):
    return parse_snbt(s, filename="t")


# ----------------------------------------------------------- scalars

def test_int_long_short_byte():
    assert p("{ a: 1 b: 1L c: 1s d: 1b }") == {"a": 1, "b": 1, "c": 1, "d": 1}


def test_doubles_and_floats_with_and_without_suffix():
    v = p("{ a: 1.5d b: 1.0 c: 2f d: -3.0d e: 100 }")
    assert v == {"a": 1.5, "b": 1.0, "c": 2.0, "d": -3.0, "e": 100}
    assert isinstance(v["a"], float)
    assert isinstance(v["e"], int)


def test_booleans_and_null():
    assert p("{ t: true f: false n: null }") == {
        "t": True, "f": False, "n": None}


def test_negative_and_zero():
    assert p("{ x: -5 y: 0 z: -1.25d }") == {"x": -5, "y": 0, "z": -1.25}


# ----------------------------------------------------------- strings

def test_double_and_single_quoted_strings():
    assert p('{ a: "hi" b: \'bye\' }') == {"a": "hi", "b": "bye"}


def test_escape_sequences_in_string():
    assert p(r'{ a: "line\nbreak\ttab\"quote\\back" }')["a"] == (
        'line\nbreak\ttab"quote\\back')


def test_unquoted_word_value_becomes_string():
    # A bare word with no suffix and no dot parses as a string.
    assert p("{ shape: circle }") == {"shape": "circle"}


# ----------------------------------------------------------- structure

def test_nested_compound_and_list():
    assert p('{ a: { b: [ 1 2 3 ] } }') == {"a": {"b": [1, 2, 3]}}


def test_commas_optional():
    # With commas and without both parse identically.
    assert p("{ a: 1, b: 2 }") == p("{ a: 1 b: 2 }") == {"a": 1, "b": 2}


def test_equals_separator():
    assert p("{ a = 1 b = 2 }") == {"a": 1, "b": 2}


def test_quoted_keys():
    assert p('{ "weird key": 1 }') == {"weird key": 1}


def test_empty_compound_and_list():
    assert p("{ }") == {}
    assert p("{ a: [ ] }") == {"a": []}


def test_single_and_multi_element_lists():
    assert p("{ a: [ 1 ] b: [ 1 2 ] }") == {"a": [1], "b": [1, 2]}


# ----------------------------------------------------------- typed arrays

def test_int_and_long_and_byte_arrays():
    assert p("{ a: [I; 1 2 3] b: [L; 4 5] c: [B; 6 7] }") == {
        "a": [1, 2, 3], "b": [4, 5], "c": [6, 7]}


# ----------------------------------------------------------- comments

def test_hash_and_slash_line_comments():
    src = (
        "# a comment line\n"
        '{ a: 1\n'
        "// another comment\n"
        '  b: 2 }\n'
    )
    assert p(src) == {"a": 1, "b": 2}


# ----------------------------------------------------------- errors

def test_unterminated_string_raises():
    with pytest.raises(SnbtError):
        p('{ a: "no end }')


def test_unclosed_compound_raises():
    with pytest.raises(SnbtError):
        p("{ a: 1 ")


def test_missing_colon_raises():
    with pytest.raises(SnbtError):
        p("{ a 1 }")


def test_empty_input_raises():
    with pytest.raises(SnbtError):
        p("")


def test_non_numeric_array_entry_raises():
    with pytest.raises(SnbtError):
        p("{ a: [I; 1 \"x\" 3] }")
