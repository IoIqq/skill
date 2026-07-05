"""Tests for reward table generation (Phase 2).

Covers: reward_tables/*.json5 emission, table_id resolution (name → decimal
long), item-entry `type` omission, weight defaulting, manifest tracking,
external-hex passthrough, and unknown-table rejection.
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
from ftbq.json5 import parse_file, to_plain  # noqa: E402

PACK = "rt-test-pack"


def _spec_text(extra_tables: str, extra_rewards: str = "") -> str:
    return (
        '{\n'
        f'  pack: "{PACK}",\n'
        '  chapters: [{\n'
        '    name: "c", default_quest_shape: "circle",\n'
        '    quests: [{ name: "q", depends_on: [], tasks: [],\n'
        f'      rewards: [{extra_rewards}]\n'
        '    }],\n'
        '  }],\n'
        f'  reward_tables: [{extra_tables}]\n'
        '}\n'
    )


def _generate(tmp_path: Path, spec_text: str) -> Path:
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    (tmp_path / "quests.spec.json5").write_text(spec_text, encoding="utf-8")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    return out


def test_reward_table_file_emitted(tmp_path: Path):
    spec = _spec_text(
        '  { name: "common_loot", rewards: ['
        ' { name: "diamond", type: "ftbquests:item", item: "minecraft:diamond", weight: 10 }'
        '] }')
    out = _generate(tmp_path, spec)
    path = out / "quests" / "reward_tables" / "common_loot.json5"
    assert path.exists()
    tbl = to_plain(parse_file(path))
    assert tbl["id"] == ftbq_ids.reward_table_id(PACK, "common_loot")
    assert tbl["loot_size"] == 1
    assert tbl["hide_tooltip"] is False
    assert tbl["use_title"] is False
    assert len(tbl["rewards"]) == 1


def test_item_entry_omits_type_nonitem_keeps_it(tmp_path: Path):
    spec = _spec_text(
        '  { name: "t", rewards: ['
        ' { name: "d", type: "ftbquests:item", item: "minecraft:diamond" },'
        ' { name: "c", type: "ftbquests:command", command: "/say hi" }'
        '] }')
    out = _generate(tmp_path, spec)
    tbl = to_plain(parse_file(out / "quests" / "reward_tables" / "t.json5"))
    diamond, cmd = tbl["rewards"]
    # item rewards omit `type` (implicit default in RewardTable)
    assert "type" not in diamond
    assert diamond["item"] == {"id": "minecraft:diamond", "count": 1}
    # non-item rewards declare `type`
    assert cmd["type"] == "ftbquests:command"
    assert cmd["command"] == "/say hi"


def test_weight_omitted_when_one(tmp_path: Path):
    spec = _spec_text(
        '  { name: "t", rewards: ['
        ' { name: "d", type: "ftbquests:item", item: "minecraft:diamond", weight: 1 }'
        '] }')
    out = _generate(tmp_path, spec)
    tbl = to_plain(parse_file(out / "quests" / "reward_tables" / "t.json5"))
    assert "weight" not in tbl["rewards"][0]


def test_table_id_resolved_from_name(tmp_path: Path):
    """A `random` reward referencing a table by name emits a numeric
    `table_id` = the decimal long of the table's id."""
    spec = _spec_text(
        '  { name: "common_loot", rewards: ['
        ' { name: "d", type: "ftbquests:item", item: "minecraft:diamond" }] }',
        extra_rewards='{ name: "rng", type: "ftbquests:random", table: "common_loot" }')
    out = _generate(tmp_path, spec)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    rng = chap["quests"][0]["rewards"][0]
    assert rng["type"] == "ftbquests:random"
    assert "table" not in rng
    table_hex = ftbq_ids.reward_table_id(PACK, "common_loot")
    assert rng["table_id"] == int(table_hex, 16)
    assert isinstance(rng["table_id"], int)


def test_external_hex_table_reference_passes_through(tmp_path: Path):
    spec = _spec_text(
        '  { name: "t", rewards: ['
        ' { name: "d", type: "ftbquests:item", item: "minecraft:diamond" }] }',
        extra_rewards=(
            '{ name: "ext", type: "ftbquests:loot", '
            'table: "0123456789ABCDEF" }'))
    out = _generate(tmp_path, spec)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    ext = chap["quests"][0]["rewards"][0]
    assert ext["table_id"] == int("0123456789ABCDEF", 16)


def test_unknown_table_name_rejected(tmp_path: Path):
    spec = _spec_text(
        '  { name: "t", rewards: ['
        ' { name: "d", type: "ftbquests:item", item: "minecraft:diamond" }] }',
        extra_rewards='{ name: "rng", type: "ftbquests:random", table: "nope" }')
    (tmp_path / "quests.spec.json5").write_text(spec, encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    spec_obj = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    with pytest.raises(generate_quests.SpecError):
        generate_quests.generate(spec_obj, out)


def test_manifest_tracks_reward_table(tmp_path: Path):
    spec = _spec_text(
        '  { name: "common_loot", rewards: ['
        ' { name: "d", type: "ftbquests:item", item: "minecraft:diamond" }] }')
    out = _generate(tmp_path, spec)
    manifest = to_plain(parse_file(out / "quests" / ".ftbq-cache" / "manifest.json5"))
    rt_entries = [e for e in manifest["entries"] if e["kind"] == "reward_table"]
    assert len(rt_entries) == 1
    assert rt_entries[0]["name"] == "common_loot"
    assert rt_entries[0]["file"] == "reward_tables/common_loot.json5"
    assert "content_hash" in rt_entries[0]


def test_reward_table_idempotent(tmp_path: Path):
    spec = _spec_text(
        '  { name: "common_loot", rewards: ['
        ' { name: "d", type: "ftbquests:item", item: "minecraft:diamond", weight: 3 }'
        '] }')
    out = _generate(tmp_path, spec)
    bytes1 = (out / "quests" / "reward_tables" / "common_loot.json5").read_bytes()
    # re-generate
    spec_obj = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec_obj, out)
    bytes2 = (out / "quests" / "reward_tables" / "common_loot.json5").read_bytes()
    assert bytes1 == bytes2


def test_empty_weight_and_loot_size_passthrough(tmp_path: Path):
    spec = _spec_text(
        '  { name: "t", empty_weight: 5, loot_size: 3, hide_tooltip: true,'
        ' use_title: true, rewards: ['
        ' { name: "d", type: "ftbquests:item", item: "minecraft:diamond" }] }')
    out = _generate(tmp_path, spec)
    tbl = to_plain(parse_file(out / "quests" / "reward_tables" / "t.json5"))
    assert tbl["empty_weight"] == 5
    assert tbl["loot_size"] == 3
    assert tbl["hide_tooltip"] is True
    assert tbl["use_title"] is True
