"""Task linkage tests.

Two concerns:

* ``depends_on`` accepts a raw 16-hex ID referencing a quest this skill did
  NOT generate (an existing pack quest indexed by Step 1.7). Such a token
  must pass through to ``dependencies`` verbatim instead of being resolved
  against the skill-owned name index (which would raise SpecError).

* ``scripts/index_quests.py`` reads an existing pack's quest files and the
  lang file, and records a per-quest digest into the cache.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "generate_quests", ROOT / "scripts" / "generate_quests.py")
generate_quests = importlib.util.module_from_spec(_spec)
sys.modules["generate_quests"] = generate_quests
_spec.loader.exec_module(generate_quests)

from ftbq import ids as ftbq_ids  # noqa: E402


# ---------------------------------------------------------------- hex passthrough

def _build(quest_spec: dict, name_to_id=None, default_chapter="c"):
    """Call _build_quest with the minimum required kwargs."""
    return generate_quests._build_quest(
        quest_spec, pack="testpack", chapter=default_chapter,
        coords={}, name_to_id=name_to_id or {},
        default_dep_chapter=default_chapter, default_shape="circle")


def test_external_hex_dep_passes_through_unchanged():
    """A 16-hex token in depends_on is emitted verbatim (uppercased)."""
    q = _build({"name": "new_quest",
                "depends_on": ["a1b2c3d4e5f60718"]})
    assert q["dependencies"] == ["A1B2C3D4E5F60718"]


def test_external_hex_dep_mixed_with_named_dep():
    """Named deps resolve via name_to_id; hex deps pass through."""
    named_id = ftbq_ids.quest_id("testpack", "c", "prereq")
    q = _build({"name": "new_quest",
                "depends_on": ["prereq", "DEADBEEFDEADBEEF"]},
               name_to_id={("c", "prereq"): named_id})
    assert q["dependencies"] == [named_id, "DEADBEEFDEADBEEF"]


def test_lowercase_hex_normalized_to_uppercase():
    q = _build({"name": "new_quest",
                "depends_on": ["a1b2c3d4e5f60718"]})
    # FTB Quests IDs are uppercase hex; normalize so a hand-copied lowercase
    # id from the cache still matches on disk.
    assert q["dependencies"] == ["A1B2C3D4E5F60718"]


def test_15_char_string_is_not_treated_as_hex_id():
    """A 15-char string is a name, not a hex id → must raise (unknown dep)."""
    with pytest.raises(generate_quests.SpecError):
        _build({"name": "new_quest", "depends_on": ["1234567890abcde"]})


def test_17_char_string_is_not_treated_as_hex_id():
    with pytest.raises(generate_quests.SpecError):
        _build({"name": "new_quest", "depends_on": ["1234567890abcdef1"]})


def test_is_external_hex_id_helper():
    h = generate_quests._is_external_hex_id
    assert h("A1B2C3D4E5F60718") is True
    assert h("a1b2c3d4e5f60718") is True
    assert h("prereq") is False
    assert h("1234567890abcde") is False     # 15 chars
    assert h("1234567890abcdef1") is False   # 17 chars
    assert h(None) is False
    assert h(123) is False


# ---------------------------------------------------------------- end-to-end generation

def test_full_generation_with_external_hex_dep(tmp_path: Path):
    """A spec mixing named + hex deps generates without error and emits
    both in the chapter file's dependencies."""
    spec = {
        "pack": "testpack",
        "default_locale": "en_us",
        "locales": ["en_us"],
        "chapters": [{
            "name": "start",
            "order_index": 0,
            "default_quest_shape": "circle",
            "quests": [
                {"name": "first", "depends_on": [],
                 "tasks": [{"name": "t", "type": "ftbquests:item",
                            "item": "minecraft:oak_log", "count": 1}],
                 "rewards": []},
                {"name": "second", "depends_on": ["first", "A1B2C3D4E5F60718"],
                 "tasks": [{"name": "t", "type": "ftbquests:item",
                            "item": "minecraft:apple", "count": 1}],
                 "rewards": []},
            ],
        }],
    }
    out = tmp_path / "quests"
    generate_quests.generate(spec, out)
    from ftbq.json5 import parse_file, to_plain
    chap = to_plain(parse_file(out / "quests" / "chapters" / "start.json5"))
    second = next(q for q in chap["quests"] if q["id"].endswith("SECOND") or
                  q["id"] == ftbq_ids.quest_id("testpack", "start", "second"))
    first_id = ftbq_ids.quest_id("testpack", "start", "first")
    assert second["dependencies"] == [first_id, "A1B2C3D4E5F60718"]


# ---------------------------------------------------------------- index_quests.py

_ix_spec = importlib.util.spec_from_file_location(
    "index_quests", ROOT / "scripts" / "index_quests.py")
index_quests = importlib.util.module_from_spec(_ix_spec)
sys.modules["index_quests"] = index_quests
_ix_spec.loader.exec_module(index_quests)


def test_indexer_records_existing_quests_with_lang_titles(tmp_path: Path):
    """index_quests reads chapter files + lang, emits a per-quest digest."""
    quests_dir = tmp_path / "config" / "ftbquests" / "quests"
    chapters = quests_dir / "chapters"
    chapters.mkdir(parents=True)
    (chapters / "magic_101.json5").write_text(
        '{\n'
        '  id: "0123456789ABCDEF",\n'
        '  filename: "magic_101",\n'
        '  default_quest_shape: "circle",\n'
        '  quests: [\n'
        '    {\n'
        '      id: "A1B2C3D4E5F60718",\n'
        '      x: 0.0, y: 0.0, shape: "circle",\n'
        '      dependencies: [],\n'
        '      tasks: [{ id: "00000000000000AA", type: "ftbquests:item",\n'
        '                 item: { id: "create:cogwheel", count: 1 }, count: 4 }],\n'
        '      rewards: [{ id: "00000000000000BB", type: "ftbquests:item",\n'
        '                  item: { id: "minecraft:apple", count: 2 } }],\n'
        '    },\n'
        '  ],\n'
        '}\n', encoding="utf-8")
    (quests_dir / "lang" / "en_us").mkdir(parents=True)
    (quests_dir / "lang" / "en_us" / "quests.json5").write_text(
        '{ "quest.A1B2C3D4E5F60718.title": "Spin a Cog" }\n',
        encoding="utf-8")

    cache = index_quests.index_pack(quests_dir)

    assert cache["schema"] == 1
    assert cache["count"] == 1
    q = cache["quests"][0]
    assert q["id"] == "A1B2C3D4E5F60718"
    assert q["chapter"] == "magic_101"
    assert q["title"] == "Spin a Cog"
    assert q["shape"] == "circle"
    assert q["task_types"] == ["ftbquests:item"]
    assert q["reward_types"] == ["ftbquests:item"]
    assert "create" in q["mod_ids"]
    assert "minecraft" not in q["mod_ids"]  # minecraft namespace filtered out
    # JSON5 quests have no "format" key; only legacy .snbt harvests set it.
    assert q.get("format") is None


def test_indexer_handles_missing_quests_dir(tmp_path: Path):
    """A brand-new pack with no quests dir produces an empty index, not a crash."""
    cache = index_quests.index_pack(tmp_path / "nope")
    assert cache["count"] == 0
    assert cache["quests"] == []
    assert cache["unindexed"]


def test_indexer_dedupes_quest_seen_twice(tmp_path: Path):
    quests_dir = tmp_path / "quests"
    chapters = quests_dir / "chapters"
    chapters.mkdir(parents=True)
    same = ('{\n id: "FFFFFFFFFFFFFFFF", filename: "c", quests: [\n'
            '  { id: "A1B2C3D4E5F60718", x: 0.0, y: 0.0, dependencies: [],'
            ' tasks: [], rewards: [] }\n ]}\n')
    (chapters / "c.json5").write_text(same, encoding="utf-8")
    cache = index_quests.index_pack(quests_dir)
    ids = [q["id"] for q in cache["quests"]]
    assert ids.count("A1B2C3D4E5F60718") == 1

