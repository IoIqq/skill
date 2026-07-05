"""Coverage for the hand-rolled JSON5 lexer/parser.

The most important guarantee is: ``//`` inside a string literal is not
treated as a comment. The old ``re.sub(r'//.*', '', ...)`` validator
would silently corrupt any URL or path containing ``//``.
"""

from __future__ import annotations

import math

import pytest

from ftbq.json5 import Json5Error, parse, to_plain


def _val(text):
    return to_plain(parse(text))


def test_basic_object():
    assert _val('{ a: 1, b: "two" }') == {"a": 1, "b": "two"}


def test_trailing_comma_object():
    assert _val('{ a: 1, b: 2, }') == {"a": 1, "b": 2}


def test_trailing_comma_array():
    assert _val('[1, 2, 3,]') == [1, 2, 3]


def test_unquoted_keys():
    assert _val('{ foo_bar: 1, $weird: 2 }') == {"foo_bar": 1, "$weird": 2}


def test_quoted_keys():
    assert _val('{ "a.b.c": 1 }') == {"a.b.c": 1}


def test_double_slash_inside_string():
    """The old regex stripper ate this. The new lexer must not."""
    val = _val('{ url: "http://example.com//foo" }')
    assert val == {"url": "http://example.com//foo"}


def test_block_comment_inside_string_kept():
    val = _val('{ s: "/* not a comment */" }')
    assert val == {"s": "/* not a comment */"}


def test_line_comment_stripped():
    val = _val('''{
        // leading comment
        a: 1, // trailing
        b: 2,
    }''')
    assert val == {"a": 1, "b": 2}


def test_block_comment_stripped():
    val = _val('{ /* hello */ a: /* mid */ 1 }')
    assert val == {"a": 1}


def test_negative_and_decimal_numbers():
    assert _val('[-3, 0.5, -1.25, 1e3]') == [-3, 0.5, -1.25, 1000.0]


def test_hex_number():
    assert _val('{ x: 0xFF }') == {"x": 255}


def test_infinity_and_nan():
    val = _val('{ p: Infinity, n: -Infinity, q: NaN }')
    assert val["p"] == math.inf
    assert val["n"] == -math.inf
    assert math.isnan(val["q"])


def test_booleans_and_null():
    assert _val('{ a: true, b: false, c: null }') == {"a": True, "b": False, "c": None}


def test_nested_arrays():
    assert _val('[[1, 2], [3, [4, 5]]]') == [[1, 2], [3, [4, 5]]]


def test_unicode_escape():
    assert _val('{ s: "\\u00e9" }') == {"s": "é"}


def test_unicode_literal():
    assert _val('{ s: "café" }') == {"s": "café"}


def test_single_quote_strings():
    assert _val("{ a: 'b' }") == {"a": "b"}


def test_escape_sequences():
    assert _val('{ s: "a\\tb\\nc" }') == {"s": "a\tb\nc"}


def test_parse_error_has_line_col():
    with pytest.raises(Json5Error) as exc_info:
        parse('{\n  bad =\n}')
    err = exc_info.value
    assert err.line == 2
    # Whatever message the lexer/parser chooses, it must be on line 2.
    assert ":2:" in str(err)


def test_parse_error_unterminated_string():
    with pytest.raises(Json5Error) as exc_info:
        parse('{ s: "no end\n}')
    assert "string" in str(exc_info.value).lower()


def test_parse_error_unterminated_block_comment():
    with pytest.raises(Json5Error) as exc_info:
        parse('{ /* never closes')
    assert "comment" in str(exc_info.value).lower()


def test_node_span_object():
    node = parse('{\n  a: 1\n}')
    assert node.line == 1
    assert node.col == 1
    assert node.end_line == 3


def test_node_span_value():
    node = parse('{\n  alpha: "value"\n}')
    alpha_child = node.value["alpha"]
    assert alpha_child.line == 2
    # column 10 is where the string literal begins
    assert alpha_child.col == 10


def test_type_suffixes_recorded_not_dropped():
    """Numbers with type suffixes parse successfully but suffix tokens
    are recorded on the root for the validator to flag."""
    node = parse('{ x: 0.0d, y: 1L, z: 5b }')
    suffixes = getattr(node, "_suffix_tokens", [])
    assert len(suffixes) == 3
    assert {tok.value for tok in suffixes} == {"d", "L", "b"}


def test_empty_object_and_array():
    assert _val('{}') == {}
    assert _val('[]') == []


def test_chapter_file_realistic():
    src = '''{
        id: "0123456789ABCDEF",
        filename: "start",
        default_quest_shape: "circle",
        quests: [
            {
                id: "1111111111111111",
                x: 0.0,
                y: 0.0,
                tasks: [
                    { id: "2222222222222222", type: "ftbquests:item",
                      item: { id: "minecraft:oak_log", count: 1 }, count: 4 },
                ],
            },
        ],
    }'''
    val = _val(src)
    assert val["filename"] == "start"
    assert val["quests"][0]["tasks"][0]["item"]["id"] == "minecraft:oak_log"
    assert val["quests"][0]["tasks"][0]["count"] == 4
