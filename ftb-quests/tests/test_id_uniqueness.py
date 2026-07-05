"""ID uniqueness guarantee — every task/reward/quest/... id is distinct.

The make_id scheme already keeps task and reward ids in disjoint key
prefixes (``task/<quest>`` vs ``reward/<quest>``), so they cannot collide
in practice. ``_validate_unique_ids`` is the provable backstop: it walks
the spec before any file is written and rejects any duplicate — the
realistic same-kind dup-name case (two tasks named ``t`` in one quest) or
the vanishingly rare cross-kind hash collision — naming both sites.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ftbq import ids as ftbq_ids  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "generate_quests_uid", ROOT / "scripts" / "generate_quests.py")
generate_quests = importlib.util.module_from_spec(_spec)
sys.modules["generate_quests_uid"] = generate_quests
_spec.loader.exec_module(generate_quests)

SpecError = generate_quests.SpecError


def _spec_from(tmp_path: Path, body: str) -> dict:
    p = tmp_path / "quests.spec.json5"
    p.write_text(body, encoding="utf-8")
    return generate_quests.load_spec(p)


def _gen(tmp_path: Path, body: str) -> Path:
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    generate_quests.generate(_spec_from(tmp_path, body), out)
    return out


_QUEST = (' quests: [{ name: "q", tasks: [%s], rewards: [%s] }] ')
_T_ITEM = '{ name: "%s", type: "ftbquests:item", item: "minecraft:stone" }'
_R_ITEM = '{ name: "%s", type: "ftbquests:item", item: "minecraft:apple" }'


def _pack(quests_body: str) -> str:
    return ('{ pack: "p", chapters: [{ name: "c",'
            ' default_quest_shape: "circle",' + quests_body + '}] }')


# --------------------------------------------------------- IdRegistry unit

def test_registry_accepts_distinct_ids():
    reg = ftbq_ids.IdRegistry()
    reg.register("1111111111111111", "task", "c/q/t1")
    reg.register("2222222222222222", "task", "c/q/t2")
    assert len(reg) == 2
    assert "1111111111111111" in reg


def test_registry_collision_names_both_sites():
    reg = ftbq_ids.IdRegistry()
    reg.register("1111111111111111", "task", "c/q/collect")
    with pytest.raises(ftbq_ids.IdCollisionError) as ei:
        reg.register("1111111111111111", "task", "c/q/collect")
    msg = str(ei.value)
    assert "1111111111111111" in msg
    assert "task" in msg
    assert "c/q/collect" in msg


# ---------------------------------------------------- same-kind collisions

def test_duplicate_task_name_in_quest_raises(tmp_path):
    body = _pack(_QUEST % (
        f"{_T_ITEM % 't'}, {_T_ITEM % 't'}", ""))
    with pytest.raises(SpecError, match="collides"):
        _gen(tmp_path, body)


def test_duplicate_reward_name_in_quest_raises(tmp_path):
    body = _pack(_QUEST % ("", f"{_R_ITEM % 'r'}, {_R_ITEM % 'r'}"))
    with pytest.raises(SpecError, match="collides"):
        _gen(tmp_path, body)


def test_duplicate_quest_name_in_chapter_raises(tmp_path):
    body = ('{ pack: "p", chapters: [{ name: "c",'
            ' default_quest_shape: "circle", quests: ['
            '{ name: "q", tasks: [], rewards: [] },'
            '{ name: "q", tasks: [], rewards: [] }'
            '] }] }')
    with pytest.raises(SpecError, match="collides"):
        _gen(tmp_path, body)


def test_duplicate_chapter_name_raises(tmp_path):
    body = ('{ pack: "p", chapters: ['
            '{ name: "c", default_quest_shape: "circle", quests: [] },'
            '{ name: "c", default_quest_shape: "circle", quests: [] }'
            '] }')
    with pytest.raises(SpecError, match="collides"):
        _gen(tmp_path, body)


def test_duplicate_table_entry_name_raises(tmp_path):
    body = ('{ pack: "p", chapters: [{ name: "c", default_quest_shape: "circle",'
            ' quests: [] }], reward_tables: [{ name: "tbl", rewards: ['
            '{ name: "e", type: "ftbquests:item", item: "minecraft:apple" },'
            '{ name: "e", type: "ftbquests:item", item: "minecraft:stone" }'
            '] }] }')
    with pytest.raises(SpecError, match="collides"):
        _gen(tmp_path, body)


# ----------------------------------------- the cross-kind guarantee (no false +

def test_same_task_and_reward_name_do_not_collide(tmp_path):
    """The user's core worry: a task and a reward sharing a name must NOT
    conflict. Different key prefixes (task/ vs reward/) → distinct ids."""
    body = _pack(_QUEST % (_T_ITEM % 'shared', _R_ITEM % 'shared'))
    out = _gen(tmp_path, body)  # must NOT raise
    from ftbq.json5 import parse_file, to_plain
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    q = chap["quests"][0]
    assert q["tasks"][0]["id"] != q["rewards"][0]["id"]


def test_same_task_name_across_quests_does_not_collide(tmp_path):
    """Same task name in two different quests → quest_name is in the key,
    so the ids differ."""
    body = ('{ pack: "p", chapters: [{ name: "c",'
            ' default_quest_shape: "circle", quests: ['
            '{ name: "q1", tasks: [%s], rewards: [] },'
            '{ name: "q2", tasks: [%s], rewards: [] }'
            '] }] }' % (_T_ITEM % 'gather', _T_ITEM % 'gather'))
    out = _gen(tmp_path, body)
    from ftbq.json5 import parse_file, to_plain
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    t1 = chap["quests"][0]["tasks"][0]["id"]
    t2 = chap["quests"][1]["tasks"][0]["id"]
    assert t1 != t2


def test_normal_multi_task_reward_pack_no_false_positive(tmp_path):
    """A well-formed pack with several tasks/rewards generates cleanly."""
    body = _pack(_QUEST % (
        f"{_T_ITEM % 't1'}, {_T_ITEM % 't2'}, {_T_ITEM % 't3'}",
        f"{_R_ITEM % 'r1'}, {_R_ITEM % 'r2'}"))
    out = _gen(tmp_path, body)
    from ftbq.json5 import parse_file, to_plain
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    q = chap["quests"][0]
    assert len(q["tasks"]) == 3
    assert len(q["rewards"]) == 2
    task_ids = [t["id"] for t in q["tasks"]]
    assert len(set(task_ids)) == 3


# ----------------------------------------------- fail-fast: no half pack

def test_no_files_written_on_collision(tmp_path):
    """Validation runs before any emit, so a colliding spec writes nothing."""
    body = _pack(_QUEST % (
        f"{_T_ITEM % 'dup'}, {_T_ITEM % 'dup'}", ""))
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    with pytest.raises(SpecError, match="collides"):
        generate_quests.generate(_spec_from(tmp_path, body), out)
    assert not (out / "quests" / "chapters").exists()
