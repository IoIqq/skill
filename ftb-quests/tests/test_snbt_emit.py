"""Tests for ftbq.snbt — the SNBT emitter (1.20.1 on-disk format).

Covers: per-field number suffixes (long/int/double/float), booleans, quoted
hex-string ids, tab indentation, no commas, key ordering, empty containers,
single-element lists, and round-trip through the parser.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ftbq.snbt import SnbtError, dumps_snbt, parse_snbt  # noqa: E402


# ----------------------------------------------------------- suffix fidelity
# Each field's NBT type is fixed by FTB Quests' writeData; the emitter must
# produce the exact suffix (or none) so 1.20.1 loads the value as the right
# tag type. See ftbq/snbt.py _SNBT_LONG_PATHS / _DOUBLE_KEYS / _FLOAT_KEYS.

def _emit_chapter(quest, **kw):
    chapter = {
        "id": "CCCCCCCCCCCCCCCC", "filename": "c", "quests": [quest],
        "quest_links": [], "images": [],
    }
    ppo = {"quests.[]": ["id", "x", "y", "tasks", "rewards", "title",
                         "description", "dependencies"],
           "quests.[].tasks.[]": ["id", "type", "item", "count", "value",
                                  "points"],
           "quests.[].rewards.[]": ["id", "type", "item", "count",
                                    "random_bonus", "table_id"]}
    ppo.update(kw.get("ppo", {}))
    return dumps_snbt(chapter, key_order=["id", "filename", "quests",
                                          "quest_links", "images"],
                      per_path_key_order=ppo)


def test_task_count_is_long_reward_count_is_bare():
    s = _emit_chapter({
        "id": "Q1", "x": 0.0, "y": 0.0,
        "tasks": [{"id": "T1", "type": "ftbquests:item",
                   "item": {"id": "minecraft:oak_log", "count": 1},
                   "count": 64}],
        "rewards": [{"id": "R1", "type": "ftbquests:item",
                     "item": {"id": "minecraft:stick", "count": 1},
                     "count": 8, "random_bonus": 2}],
    })
    # ItemTask.count -> putLong -> "64L"; ItemReward.count -> putInt -> "8"
    assert "count: 64L" in s
    assert "count: 8" in s and "count: 8L" not in s
    assert "random_bonus: 2" in s and "random_bonus: 2L" not in s
    # The item compound's embedded count is an int (ItemStack count), bare.
    assert "count: 1" in s


def test_xp_value_is_long_and_points_is_bool():
    s = _emit_chapter({
        "id": "Q2", "x": 0.0, "y": 0.0,
        "tasks": [{"id": "T2", "type": "ftbquests:xp", "value": 100,
                   "points": True}],
        "rewards": [],
    })
    assert "value: 100L" in s
    assert "points: true" in s


def test_coordinates_and_sizes_are_doubles():
    s = _emit_chapter({
        "id": "Q3", "x": 1.5, "y": -2.0, "size": 2.0, "icon_scale": 1.0,
        "tasks": [], "rewards": [],
    })
    assert "x: 1.5d" in s
    assert "y: -2.0d" in s
    assert "size: 2.0d" in s
    assert "icon_scale: 1.0d" in s
    assert "x: 1.5" == "x: 1.5"  # sanity
    assert "1.5d" in s and "1.5f" not in s


def test_quest_link_and_image_coordinates_are_doubles():
    chapter = {
        "id": "C", "filename": "c", "quests": [],
        "quest_links": [{"id": "L1", "linked_quest": "Q", "x": 1.0, "y": 0.0,
                         "size": 1.5}],
        "images": [{"id": "I1", "image": "x.png", "x": 0.0, "y": 0.0,
                    "width": 2.0, "height": 3.0, "rotation": 0.0}],
    }
    s = dumps_snbt(chapter, key_order=["id", "filename", "quests",
                                       "quest_links", "images"],
                   per_path_key_order={"quest_links.[]": ["id", "linked_quest",
                                                          "x", "y", "size"],
                                       "images.[]": ["id", "image", "x", "y",
                                                     "width", "height",
                                                     "rotation"]})
    assert "x: 1.0d" in s and "size: 1.5d" in s
    assert "width: 2.0d" in s and "height: 3.0d" in s and "rotation: 0.0d" in s


def test_reward_table_weights_are_floats():
    table = {"id": "T", "empty_weight": 1.0, "loot_size": 1,
             "rewards": [{"id": "E1", "item": {"id": "minecraft:stick",
                                               "count": 1}, "weight": 2.5}]}
    s = dumps_snbt(table, key_order=["id", "rewards", "empty_weight",
                                     "loot_size"],
                   per_path_key_order={"rewards.[]": ["id", "item", "weight"]})
    assert "empty_weight: 1.0f" in s
    assert "weight: 2.5f" in s
    assert "loot_size: 1" in s and "loot_size: 1L" not in s


def test_id_is_quoted_hex_string():
    s = _emit_chapter({"id": "1A2B3C4D5E6F7A8B", "x": 0.0, "y": 0.0,
                       "tasks": [], "rewards": []})
    assert 'id: "1A2B3C4D5E6F7A8B"' in s


# --------------------------------------------------------- structure / style

def test_no_commas_in_multiline_and_tab_indent():
    s = _emit_chapter({"id": "Q", "x": 0.0, "y": 0.0, "tasks": [], "rewards": []})
    # No line in a multi-line compound ends with a comma (SNBT multi-line
    # separates members by newlines, not commas).
    for line in s.splitlines():
        assert not line.rstrip().endswith(","), line
    # Indentation is tabs, not spaces.
    assert "\t" in s
    assert "    " not in s  # no 4-space indent


def test_empty_containers_and_single_element_list():
    s = dumps_snbt({"a": {}, "b": [], "c": ["only"]})
    assert "{ }" in s
    assert "[ ]" in s
    assert 'c: ["only"]' in s  # single-element list is inline


def test_key_order_and_per_path_order():
    out = {"id": "1", "z": 1, "a": 2, "tasks": []}
    s = dumps_snbt(out, key_order=["id", "tasks", "z", "a"])
    lines = [ln.strip() for ln in s.splitlines() if ":" in ln]
    keys = [ln.split(":")[0] for ln in lines]
    assert keys[:4] == ["id", "tasks", "z", "a"]


def test_strings_quoted_when_not_simple():
    # String VALUES are always quoted in SNBT (quoteAndEscape); only KEYS
    # are unquoted when every char is simple.
    s = dumps_snbt({"item": "minecraft:oak_log"})
    assert 'item: "minecraft:oak_log"' in s  # ':' is not a simple char -> key quoted
    # A simple key stays unquoted; its value is still quoted.
    s2 = dumps_snbt({"simple_id": "v"})
    assert 'simple_id: "v"' in s2
    assert '"simple_id"' not in s2  # key not quoted


def test_escape_quotes_and_backslash():
    s = dumps_snbt({"cmd": 'say "hi" \\ done'})
    assert '\\"hi\\"' in s and "\\\\" in s
    # round-trips back to the original
    back = parse_snbt(s)
    assert back["cmd"] == 'say "hi" \\ done'


# --------------------------------------------------------------- round-trip

def test_round_trip_full_chapter():
    chapter = {
        "id": "CCCCCCCCCCCCCCCC", "filename": "intro",
        "default_quest_size": 1.0,
        "quests": [{
            "id": "6A42C15CE3485849", "x": 0.0, "y": 0.0, "shape": "circle",
            "title": "Punch Wood", "subtitle": "hit a tree",
            "description": ["line one", "line two"],
            "dependencies": ["6A42C15CE3485849"],
            "tasks": [
                {"id": "T1", "type": "ftbquests:item",
                 "item": {"id": "minecraft:oak_log", "count": 1}, "count": 4},
                {"id": "T2", "type": "ftbquests:xp", "value": 30,
                 "points": True},
            ],
            "rewards": [{"id": "R1", "type": "ftbquests:item",
                         "item": {"id": "minecraft:stick", "count": 1},
                         "count": 8, "random_bonus": 1}],
        }],
        "quest_links": [{"id": "L1", "linked_quest": "6A42C15CE3485849",
                         "x": 1.0, "y": 0.0, "size": 1.0}],
        "images": [{"id": "I1", "image": "oak.png", "x": 0.0, "y": 0.0,
                    "width": 1.0, "height": 1.0, "rotation": 0.0}],
    }
    ppo = {"quests.[]": ["id", "x", "y", "shape", "title", "subtitle",
                         "description", "dependencies", "tasks", "rewards"],
           "quests.[].tasks.[]": ["id", "type", "item", "count", "value",
                                  "points"],
           "quests.[].rewards.[]": ["id", "type", "item", "count",
                                    "random_bonus"],
           "quest_links.[]": ["id", "linked_quest", "x", "y", "size"],
           "images.[]": ["id", "image", "x", "y", "width", "height",
                         "rotation"]}
    s = dumps_snbt(chapter, key_order=["id", "filename", "default_quest_size",
                                       "quests", "quest_links", "images"],
                   per_path_key_order=ppo)
    assert parse_snbt(s) == chapter


def test_emit_rejects_unknown_type():
    with pytest.raises(SnbtError):
        dumps_snbt({"x": object()})
