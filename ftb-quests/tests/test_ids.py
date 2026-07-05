"""Tests for ftbq.ids: deterministic md5 IDs and content hashing."""

from __future__ import annotations

from ftbq import ids


def test_chapter_id_stable():
    a = ids.chapter_id("create-astral", "getting_started")
    b = ids.chapter_id("create-astral", "getting_started")
    assert a == b
    assert len(a) == 16
    assert a == a.upper()
    assert all(c in "0123456789ABCDEF" for c in a)


def test_different_packs_yield_different_ids():
    a = ids.chapter_id("pack-a", "intro")
    b = ids.chapter_id("pack-b", "intro")
    assert a != b


def test_quest_id_independent_of_other_chapters():
    a = ids.quest_id("p", "ch1", "punch_wood")
    b = ids.quest_id("p", "ch2", "punch_wood")
    assert a != b


def test_task_namespace_is_quest_local():
    """Two quests with a task named 'collect' must yield different task IDs."""
    a = ids.task_id("p", "ch", "questA", "collect")
    b = ids.task_id("p", "ch", "questB", "collect")
    assert a != b


def test_reward_namespace_is_quest_local():
    a = ids.reward_id("p", "ch", "qA", "trophy")
    b = ids.reward_id("p", "ch", "qB", "trophy")
    assert a != b


def test_content_hash_drops_id_field():
    """Two objects identical except for 'id' must hash to the same value."""
    obj1 = {"id": "AAAA", "title": "x", "x": 0.0}
    obj2 = {"id": "BBBB", "title": "x", "x": 0.0}
    assert ids.content_hash(obj1) == ids.content_hash(obj2)


def test_content_hash_changes_on_real_change():
    obj1 = {"id": "AAAA", "title": "x"}
    obj2 = {"id": "AAAA", "title": "y"}
    assert ids.content_hash(obj1) != ids.content_hash(obj2)


def test_content_hash_recursive_id_strip():
    """Nested 'id' fields are also dropped."""
    obj1 = {"tasks": [{"id": "111", "type": "item"}]}
    obj2 = {"tasks": [{"id": "999", "type": "item"}]}
    assert ids.content_hash(obj1) == ids.content_hash(obj2)


def test_content_hash_key_order_independent():
    a = {"a": 1, "b": 2, "c": 3}
    b = {"c": 3, "b": 2, "a": 1}
    assert ids.content_hash(a) == ids.content_hash(b)


def test_content_hash_format():
    h = ids.content_hash({"x": 1})
    assert h.startswith("sha256:")
    assert len(h) == len("sha256:") + 64


# ---- top-bit mask (ids must parse as Java long in FTB Quests) -----------


def test_id_always_non_negative_long():
    """FTB Quests parses hex ids with Long.parseLong(hex,16), which throws
    for any magnitude > Long.MAX_VALUE (top hex digit 8-F) and then regenerates
    a random id — breaking dependency resolution. Every generated id must
    therefore have a top hex digit in 0-7."""
    import hashlib
    long_max = (1 << 63) - 1
    # Sample many distinct keys; none may produce a top-digit 8-F id.
    for i in range(200):
        key = f"pack/chapter/quest/q{i}"
        raw = int(hashlib.md5(key.encode()).hexdigest()[:16], 16)
        # Before masking, ~half would be > Long.MAX_VALUE; the helper must mask.
        gen = ids.quest_id("pack", "chapter", f"q{i}")
        assert int(gen, 16) <= long_max
        assert gen[0] in "01234567"


def test_id_round_trips_through_hex_to_long():
    """The long value must parse back to the same hex FTB Quests stores
    (getCodeString = String.format("%016X", id))."""
    qid = ids.quest_id("pack", "ch", "q")
    long_val = ids.hex_to_long(qid)
    assert f"{long_val:016X}" == qid


def test_reward_table_id_stable_and_loadable():
    a = ids.reward_table_id("pack", "common_loot")
    b = ids.reward_table_id("pack", "common_loot")
    assert a == b
    assert len(a) == 16
    assert a[0] in "01234567"  # top-bit masked
    assert ids.reward_table_id("pack", "rare_loot") != a


def test_hex_to_long_masks_oversized_external_id():
    """An external id above Long.MAX_VALUE must still fit a Java long."""
    big = "FFFFFFFFFFFFFFFF"
    assert ids.hex_to_long(big) == (1 << 63) - 1

