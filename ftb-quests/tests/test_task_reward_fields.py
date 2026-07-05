"""Tests for task/reward field semantics fixed against the FTB Quests source.

Covers the two correctness bugs that produced files which silently misbehaved
or failed to load:

* item task/reward quantity lives in the SIBLING ``count`` field, not the
  item object (``ItemTask``/``ItemReward`` ignore the object count);
* ``ftbquests:xp`` tasks require a ``points`` boolean (``XPTask.readData``
  uses ``orElseThrow``) — the generator defaults it so the book loads.
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

from ftbq.json5 import parse_file, to_plain  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "spec_stable.json5"


def _generate(tmp_path: Path) -> Path:
    out = tmp_path / "quests"
    out.mkdir(parents=True, exist_ok=True)
    shutil_copy = __import__("shutil").copyfile
    shutil_copy(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    return out


def test_reward_count_lifted_to_sibling(tmp_path: Path):
    """The fixture's apple reward buries count in the object
    (``item: {id, count: 2}``). FTB Quests reads only the sibling ``count``,
    so the generator must lift it: object count 1 + sibling ``count: 2``."""
    out = _generate(tmp_path)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    punch = next(q for q in chap["quests"] if q["dependencies"] == [])
    apple = punch["rewards"][0]
    assert apple["item"] == {"id": "minecraft:apple", "count": 1}
    assert apple["count"] == 2


def test_explicit_sibling_reward_count_not_doubled(tmp_path: Path):
    """An explicit sibling ``count`` is the canonical form — the object
    count stays 1 and nothing is lifted/duplicated."""
    tmp_path.joinpath("quests.spec.json5").write_text(
        '{ pack: "p", chapters: [{ name: "c", default_quest_shape: "circle",'
        ' quests: [{ name: "q", tasks: [], rewards: ['
        ' { name: "r", type: "ftbquests:item", item: "minecraft:apple", count: 3 }'
        '] }] }] }', encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    reward = chap["quests"][0]["rewards"][0]
    assert reward["item"] == {"id": "minecraft:apple", "count": 1}
    assert reward["count"] == 3


def test_task_count_lifted_from_object(tmp_path: Path):
    """Same lift applies to item TASKS: ItemTask also reads sibling count."""
    tmp_path.joinpath("quests.spec.json5").write_text(
        '{ pack: "p", chapters: [{ name: "c", default_quest_shape: "circle",'
        ' quests: [{ name: "q", tasks: ['
        ' { name: "t", type: "ftbquests:item", item: { id: "minecraft:stone", count: 7 } }'
        '], rewards: [] }] }] }', encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    task = chap["quests"][0]["tasks"][0]
    assert task["item"] == {"id": "minecraft:stone", "count": 1}
    assert task["count"] == 7


def test_xp_task_defaults_points_true(tmp_path: Path):
    """XPTask.readData requires `points` (orElseThrow). A spec XP task
    without `points` must still produce a loadable file — default true."""
    tmp_path.joinpath("quests.spec.json5").write_text(
        '{ pack: "p", chapters: [{ name: "c", default_quest_shape: "circle",'
        ' quests: [{ name: "q", tasks: ['
        ' { name: "x", type: "ftbquests:xp", value: 30 }'
        '], rewards: [] }] }] }', encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    task = chap["quests"][0]["tasks"][0]
    assert task["value"] == 30
    assert task["points"] is True


def test_xp_task_points_passthrough(tmp_path: Path):
    """An explicit `points: false` (XP levels) is passed through unchanged."""
    tmp_path.joinpath("quests.spec.json5").write_text(
        '{ pack: "p", chapters: [{ name: "c", default_quest_shape: "circle",'
        ' quests: [{ name: "q", tasks: ['
        ' { name: "x", type: "ftbquests:xp", value: 30, points: false }'
        '], rewards: [] }] }] }', encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    task = chap["quests"][0]["tasks"][0]
    assert task["points"] is False
