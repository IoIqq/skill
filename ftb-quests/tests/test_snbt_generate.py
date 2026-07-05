"""End-to-end SNBT (Minecraft 1.20.1) generation tests.

Exercises every feature — reward tables, quest links, chapter images, an XP
task, a command reward, dependencies — through ``format: "snbt"`` generation,
then validates the result clean and checks idempotency. Mirrors the JSON5
suite's concerns (file layout, inline text, manifest shape) for the 1.20.1
on-disk format documented in reference §12.
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

_vspec = importlib.util.spec_from_file_location(
    "validate_quests", ROOT / "scripts" / "validate_quests.py")
validate_quests = importlib.util.module_from_spec(_vspec)
sys.modules["validate_quests"] = validate_quests
_vspec.loader.exec_module(validate_quests)

from ftbq.snbt import parse_snbt_file  # noqa: E402

PACK = "snbt-e2e-pack"

SPEC = (
    '{ pack: "' + PACK + '", format: "snbt",\n'
    '  data: { version: 13, default_reward_team: false,\n'
    '    default_consume_items: false, default_autoclaim_rewards: "default",\n'
    '    default_quest_shape: "circle", default_quest_disable_jei: false,\n'
    '    emergency_items_cooldown: 300 },\n'
    '  reward_tables: [\n'
    '    { name: "starter_loot", empty_weight: 1.0, loot_size: 1,\n'
    '      rewards: [ { name: "stick", type: "ftbquests:item",\n'
    '        item: { id: "minecraft:stick", count: 1 }, weight: 2.0 } ] } ],\n'
    '  chapters: [\n'
    '    { name: "intro", title: "Getting Started",\n'
    '      subtitle: ["An intro line"],\n'
    '      images: [ { name: "bg_oak", image: "minecraft:textures/block/oak_log.png",\n'
    '        x: 0, y: 0, width: 1, height: 1, rotation: 0 } ],\n'
    '      quests: [\n'
    '        { name: "punch_wood", title: "Punch Wood",\n'
    '          subtitle: "Hit a tree", description: ["Break", "wood"],\n'
    '          tasks: [ { name: "get_log", type: "ftbquests:item",\n'
    '            item: { id: "minecraft:oak_log", count: 4 } } ],\n'
    '          rewards: [ { name: "loot", type: "ftbquests:random",\n'
    '            table: "starter_loot" } ] },\n'
    '        { name: "gain_xp", title: "Gain XP", depends_on: ["punch_wood"],\n'
    '          tasks: [ { name: "xp", type: "ftbquests:xp", value: 30 } ],\n'
    '          rewards: [ { name: "cmd", type: "ftbquests:command",\n'
    '            command: "give {p} minecraft:apple 1" } ] } ],\n'
    '      quest_links: [ { name: "mirror_punch", linked_quest: "punch_wood",\n'
    '        x: 5, y: 0 } ] } ] }')


def _generate(tmp_path: Path) -> Path:
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    (tmp_path / "quests.spec.json5").write_text(SPEC, encoding="utf-8")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    return out


def _root(out: Path) -> Path:
    return out / "quests"  # generate() writes under <output_dir>/quests/


def test_emits_snbt_files_with_no_lang(tmp_path: Path):
    root = _root(_generate(tmp_path))
    assert (root / "data.snbt").exists()
    assert (root / "chapters" / "intro.snbt").exists()
    assert (root / "reward_tables" / "starter_loot.snbt").exists()
    assert (root / ".ftbq-cache" / "manifest.json5").exists()
    # 1.20.1 SNBT has no lang files — text is inline.
    assert not (root / "lang").exists()


def test_inline_text_and_typed_fields(tmp_path: Path):
    root = _root(_generate(tmp_path))
    chapter = parse_snbt_file(root / "chapters" / "intro.snbt")
    q = chapter["quests"][0]
    assert q["title"] == "Punch Wood"
    assert q["subtitle"] == "Hit a tree"
    assert q["description"] == ["Break", "wood"]
    # Chapter-level inline subtitle list + title.
    assert chapter["subtitle"] == ["An intro line"]
    assert chapter["title"] == "Getting Started"
    # ItemTask.count is a long; the embedded item count is an int.
    raw = (root / "chapters" / "intro.snbt").read_text(encoding="utf-8")
    assert "count: 4L" in raw  # task long
    # XP value is a long; command placeholder survives verbatim.
    assert "value: 30L" in raw
    assert 'command: "give {p} minecraft:apple 1"' in raw
    # table_id on the random reward is a decimal long (not a hex string).
    rand = [r for r in q["rewards"] if r["type"] == "ftbquests:random"][0]
    assert isinstance(rand["table_id"], int)


def test_quest_link_and_image_present(tmp_path: Path):
    root = _root(_generate(tmp_path))
    chapter = parse_snbt_file(root / "chapters" / "intro.snbt")
    assert chapter["quest_links"][0]["linked_quest"]  # resolved to hex
    assert chapter["images"][0]["image"].endswith("oak_log.png")


def test_validates_clean(tmp_path: Path):
    root = _root(_generate(tmp_path))
    book = validate_quests.load_book(root)
    assert book.format == "snbt"
    diags = validate_quests.Validator(book).run()
    # No errors; only possibly benign warnings (none expected here).
    errors = [d for d in diags if d.severity == "error"]
    assert errors == [], [d.format_text() for d in errors]


def test_idempotent_regeneration(tmp_path: Path):
    out = _generate(tmp_path)
    first = {p: p.read_bytes() for p in (out / "quests").rglob("*")
             if p.is_file()}
    # Re-generate into a fresh dir with the same spec -> byte-identical.
    out2 = tmp_path / "out2"
    out2.mkdir(parents=True, exist_ok=True)
    (tmp2 := tmp_path / "spec2.json5").write_text(SPEC, encoding="utf-8")
    spec = generate_quests.load_spec(tmp2)
    generate_quests.generate(spec, out2)
    second = {p.relative_to(out2 / "quests"): p.read_bytes()
              for p in (out2 / "quests").rglob("*") if p.is_file()}
    for rel, data in first.items():
        key = rel.relative_to(out / "quests")
        assert second[key] == data, f"{key} differs on re-run"
