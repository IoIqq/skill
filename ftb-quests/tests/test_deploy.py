"""Tests for ftbq.deploy — safe copy of the generated quests/ tree into a
live modpack folder: overwrite detection, additive-file merge, chapter
backup+replace, and the .ftbq-backup/<ts>/ mirror.

Pure-logic tests build source/target trees by hand (independent of
generate_quests); one integration test exercises the ``--deploy`` CLI gate.
"""

from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ftbq import deploy as ftbq_deploy  # noqa: E402
from ftbq.canonical import dump_file  # noqa: E402
from ftbq.json5 import parse_file, to_plain  # noqa: E402
from ftbq.snbt import dump_file_snbt, parse_snbt_file  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "generate_quests", ROOT / "scripts" / "generate_quests.py")
generate_quests = importlib.util.module_from_spec(_spec)
sys.modules["generate_quests"] = generate_quests
_spec.loader.exec_module(generate_quests)

FIXTURE = ROOT / "tests" / "fixtures" / "spec_stable.json5"

CHAPTER_ID = "558F3C8054F8FED0"
QUEST_ID = "AABBCCDDEEFF0011"


def _write(path: Path, obj, **kw) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dump_file(path, obj, **kw)


def _make_source(root: Path) -> None:
    """A minimal, hand-built quests/ tree (the skill's generated output)."""
    _write(root / "data.json5",
            {"default_quest_disable_jei": False, "skill_key": 1})
    _write(root / "chapter_groups.json5",
            {"chapter_groups": [
                {"id": "G1", "name": "grp1", "order_index": 0}]})
    _write(root / "chapters" / "intro.json5", {
        "id": CHAPTER_ID, "filename": "intro",
        "default_quest_shape": "circle", "group": "", "order_index": 0,
        "quests": [{"id": QUEST_ID, "x": 0.0, "y": 0.0, "shape": "circle",
                     "dependencies": [], "tasks": [], "rewards": []}]})
    _write(root / "lang" / "en_us" / "quests.json5", {
        f"chapter.{CHAPTER_ID}.title": "Intro",
        f"quest.{QUEST_ID}.title": "First",
    }, quote_keys=True)
    _write(root / ".ftbq-cache" / "manifest.json5",
            {"schema": 1, "pack": "p", "entries": []})


# --------------------------------------------------------------- scan_root


def test_scan_root_classifies_game_files_only(tmp_path: Path):
    src = tmp_path / "src"
    _make_source(src)
    # Stray analysis caches + a prior backup must NOT be deployed.
    _write(src / ".ftbq-cache" / "existing_quests.json5", {"x": 1})
    _write(src / ".ftbq-backup" / "old" / "data.json5", {"old": True})
    entries = {e.rel_path: e.kind for e in ftbq_deploy.scan_root(src)}
    assert entries["data.json5"] == "data"
    assert entries["chapter_groups.json5"] == "chapter_groups"
    assert entries["chapters/intro.json5"] == "chapter"
    assert entries["lang/en_us/quests.json5"] == "lang"
    assert entries[".ftbq-cache/manifest.json5"] == "manifest"
    assert "quests.spec.json5" not in entries
    assert ".ftbq-cache/existing_quests.json5" not in entries
    assert ".ftbq-backup/old/data.json5" not in entries


# --------------------------------------------------------------- new / unchanged


def test_new_files_copied_no_backup(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    plan = ftbq_deploy.plan(src, tgt)
    assert [p.action for p in plan.entries] == ["new"] * len(plan.entries)
    assert not plan.overwrites
    rep = ftbq_deploy.apply(plan, tgt)
    assert rep.counts["new"] == len(plan.entries)
    assert rep.counts["replace"] == 0
    assert rep.backup_dir is None  # nothing to back up
    # Files landed at the same relative paths (names preserved).
    assert (tgt / "chapters" / "intro.json5").exists()
    assert (tgt / "data.json5").exists()
    assert (tgt / "lang" / "en_us" / "quests.json5").exists()


def test_unchanged_files_skipped(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _make_source(tgt)  # identical content
    plan = ftbq_deploy.plan(src, tgt)
    assert all(p.action == "unchanged" for p in plan.entries)
    rep = ftbq_deploy.apply(plan, tgt)
    assert rep.counts["unchanged"] == len(plan.entries)
    assert rep.backup_dir is None
    assert not (tgt / ".ftbq-backup").exists()


# --------------------------------------------------------------- merge


def test_data_merge_keeps_pack_keys(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "data.json5",
            {"default_quest_disable_jei": True, "pack_only_key": "keepme"})
    plan = ftbq_deploy.plan(src, tgt)
    pf = next(p for p in plan.entries if p.rel_path == "data.json5")
    assert pf.action == "merge"
    assert pf.merge_stats == {"added": 1, "kept": 1, "overridden": 1}
    ftbq_deploy.apply(plan, tgt)
    d = to_plain(parse_file(tgt / "data.json5"))
    assert d["pack_only_key"] == "keepme"      # pack key preserved
    assert d["skill_key"] == 1                 # skill key added
    assert d["default_quest_disable_jei"] is False  # skill overrode pack's True


def test_lang_merge_preserves_other_quest_keys(tmp_path: Path):
    """CRITICAL regression: a blind copy would erase the pack's lang entries
    for quests the skill does not own. Merge must keep them."""
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "lang" / "en_us" / "quests.json5",
            {"quest.OTHERQUEST12345.title": "Other Pack Quest"})
    plan = ftbq_deploy.plan(src, tgt)
    pf = next(p for p in plan.entries if p.rel_path == "lang/en_us/quests.json5")
    assert pf.action == "merge"
    ftbq_deploy.apply(plan, tgt)
    lang = to_plain(parse_file(tgt / "lang" / "en_us" / "quests.json5"))
    assert "quest.OTHERQUEST12345.title" in lang   # pack key survived
    assert f"quest.{QUEST_ID}.title" in lang        # skill key added


def test_chapter_groups_union_by_id(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "chapter_groups.json5", {"chapter_groups": [
        {"id": "G1", "name": "grp1-old", "order_index": 9},   # overridden
        {"id": "G2", "name": "grp2", "order_index": 0}]})      # kept
    plan = ftbq_deploy.plan(src, tgt)
    pf = next(p for p in plan.entries
              if p.rel_path == "chapter_groups.json5")
    assert pf.action == "merge"
    assert pf.merge_stats == {"added": 0, "kept": 1, "overridden": 1}
    ftbq_deploy.apply(plan, tgt)
    groups = {g["id"]: g for g in
              to_plain(parse_file(tgt / "chapter_groups.json5"))["chapter_groups"]}
    assert set(groups) == {"G1", "G2"}
    assert groups["G1"]["name"] == "grp1"      # source overrode
    assert groups["G1"]["order_index"] == 0
    assert groups["G2"]["name"] == "grp2"      # pack group kept


# ------------------------------------------------------- replace + backup


def test_chapter_collision_backed_up_and_replaced(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "chapters" / "intro.json5",
            {"id": "OLDINTRO00000000", "filename": "intro", "quests": []})
    plan = ftbq_deploy.plan(src, tgt)
    pf = next(p for p in plan.entries if p.rel_path == "chapters/intro.json5")
    assert pf.action == "replace"
    assert pf.quest_overlap == []  # no shared quest IDs
    rep = ftbq_deploy.apply(plan, tgt)
    new = to_plain(parse_file(tgt / "chapters" / "intro.json5"))
    assert new["id"] == CHAPTER_ID  # replaced
    # Original backed up under .ftbq-backup/<ts>/chapters/intro.json5 (same name).
    backups = list((tgt / ".ftbq-backup").rglob("intro.json5"))
    assert len(backups) == 1
    assert to_plain(parse_file(backups[0]))["id"] == "OLDINTRO00000000"
    assert rep.counts["replace"] == 1


def test_manifest_replaced_and_backed_up(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / ".ftbq-cache" / "manifest.json5",
            {"schema": 1, "pack": "OLDPACK", "entries": []})
    plan = ftbq_deploy.plan(src, tgt)
    pf = next(p for p in plan.entries if p.rel_path == ".ftbq-cache/manifest.json5")
    assert pf.action == "replace"
    ftbq_deploy.apply(plan, tgt)
    m = to_plain(parse_file(tgt / ".ftbq-cache" / "manifest.json5"))
    assert m["pack"] == "p"  # skill's manifest won
    backups = list((tgt / ".ftbq-backup").rglob("manifest.json5"))
    assert len(backups) == 1


def test_backup_index_written_and_parseable(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "data.json5", {"pack_only_key": "keepme"})
    _write(tgt / "chapters" / "intro.json5",
            {"id": "OLD", "filename": "intro", "quests": []})
    plan = ftbq_deploy.plan(src, tgt)
    rep = ftbq_deploy.apply(plan, tgt)
    idx = to_plain(parse_file(rep.backup_dir / "BACKUP_INDEX.json5"))
    backed = {e["rel_path"] for e in idx["entries"]}
    assert "data.json5" in backed
    assert "chapters/intro.json5" in backed
    for e in idx["entries"]:
        assert e["reason"] in ("merge", "replace")
        assert e["original_signature"].startswith("sha256:")
        assert e["replaced_by_signature"].startswith("sha256:")


def test_backup_dir_is_dot_prefixed(tmp_path: Path):
    """FTB Quests' scanner skips dot-prefixed dirs (see reference §14), so
    .ftbq-backup never leaks into the loaded book."""
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "chapters" / "intro.json5",
            {"id": "OLD", "filename": "intro", "quests": []})
    plan = ftbq_deploy.plan(src, tgt)
    rep = ftbq_deploy.apply(plan, tgt)
    # The backup sits under <tgt>/.ftbq-backup/<ts>/ — dot-prefixed so FTB
    # Quests' scanner skips it (reference §14).
    assert rep.backup_dir.parent.name == ".ftbq-backup"
    assert rep.backup_dir.relative_to(tgt).parts[0] == ".ftbq-backup"


# --------------------------------------------------------------- names


def test_names_preserved_everywhere(tmp_path: Path):
    """File stems never change — the backup mirrors the original name so a
    replaced file is trivial to find next to its replacement."""
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "chapters" / "intro.json5",
            {"id": "OLD", "filename": "intro", "quests": []})
    plan = ftbq_deploy.plan(src, tgt)
    rep = ftbq_deploy.apply(plan, tgt)
    # Target chapter kept its name.
    assert (tgt / "chapters" / "intro.json5").exists()
    # Backup kept the same name + relative path.
    backup = rep.backup_dir / "chapters" / "intro.json5"
    assert backup.exists()
    assert backup.name == "intro.json5"


# ----------------------------------------------------------- flags / gate


def test_no_backup_flag_skips_backup(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "chapters" / "intro.json5",
            {"id": "OLD", "filename": "intro", "quests": []})
    plan = ftbq_deploy.plan(src, tgt)
    rep = ftbq_deploy.apply(plan, tgt, backup=False)
    assert rep.counts["replace"] == 1
    assert rep.backup_dir is None
    assert not (tgt / ".ftbq-backup").exists()
    # Replace still happened.
    assert to_plain(parse_file(tgt / "chapters" / "intro.json5"))["id"] == CHAPTER_ID


def test_plan_only_writes_nothing(tmp_path: Path):
    """plan() is a pure preview — it must not touch the target."""
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source(src)
    _write(tgt / "chapters" / "intro.json5",
            {"id": "OLD", "filename": "intro", "quests": []})
    ftbq_deploy.plan(src, tgt)
    assert to_plain(parse_file(tgt / "chapters" / "intro.json5"))["id"] == "OLD"
    assert not (tgt / ".ftbq-backup").exists()


def test_main_deploy_without_yes_writes_nothing(tmp_path: Path):
    """--deploy without --yes is a preview: generate runs, but the live
    target is untouched."""
    out = tmp_path / "out"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    tgt = tmp_path / "tgt" / "config" / "ftbquests" / "quests"
    _write(tgt / "data.json5", {"pack_only_key": "keepme"})
    rc = generate_quests.main([str(out), "--quests-dir", str(tgt),
                                "--spec", str(tmp_path / "quests.spec.json5")])
    assert rc == 0
    # Target untouched — still the pack's original data.
    assert to_plain(parse_file(tgt / "data.json5")) == {"pack_only_key": "keepme"}
    assert not (tgt / ".ftbq-backup").exists()


def test_main_deploy_with_yes_applies(tmp_path: Path):
    out = tmp_path / "out"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    tgt = tmp_path / "tgt" / "config" / "ftbquests" / "quests"
    _write(tgt / "data.json5", {"pack_only_key": "keepme"})
    rc = generate_quests.main([str(out), "--quests-dir", str(tgt),
                                "--spec", str(tmp_path / "quests.spec.json5"),
                                "--yes"])
    assert rc == 0
    d = to_plain(parse_file(tgt / "data.json5"))
    assert d["pack_only_key"] == "keepme"   # merged, not clobbered
    assert (tgt / ".ftbq-backup").exists()


def test_main_deploy_conflicts_with_dry_run(tmp_path: Path):
    out = tmp_path / "out"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    rc = generate_quests.main([str(out), "--deploy", str(tmp_path / "pack"),
                                "--spec", str(tmp_path / "quests.spec.json5"),
                                "--dry-run"])
    assert rc == 2


# ----------------------------------------------------------- merge helpers


def test_merge_data_deep_merges_nested():
    target = {"a": {"x": 1, "y": 2}, "keep": True}
    source = {"a": {"y": 9, "z": 3}, "add": 5}
    merged, stats = ftbq_deploy.merge_data(target, source)
    assert merged == {"a": {"x": 1, "y": 9, "z": 3}, "keep": True, "add": 5}
    assert stats == {"added": 1, "kept": 1, "overridden": 1}


def test_merge_lang_source_overrides_own_keys():
    target = {"quest.AAA.title": "Old", "quest.BBB.title": "Pack"}
    source = {"quest.AAA.title": "New"}
    merged, stats = ftbq_deploy.merge_lang(target, source)
    assert merged == {"quest.AAA.title": "New", "quest.BBB.title": "Pack"}
    assert stats == {"added": 0, "kept": 1, "overridden": 1}


def test_merge_chapter_groups_preserves_target_order():
    target = {"chapter_groups": [
        {"id": "G2", "name": "two", "order_index": 0},
        {"id": "G1", "name": "one", "order_index": 1}]}
    source = {"chapter_groups": [{"id": "G1", "name": "ONE", "order_index": 1}]}
    merged, stats = ftbq_deploy.merge_chapter_groups(target, source)
    ids = [g["id"] for g in merged["chapter_groups"]]
    assert ids == ["G2", "G1"]  # target order preserved, G1 overridden
    assert merged["chapter_groups"][1]["name"] == "ONE"
    assert stats == {"added": 0, "kept": 1, "overridden": 1}


# ---- reward tables -----------------------------------------------------


def _make_source_with_table(root: Path) -> None:
    _make_source(root)
    _write(root / "reward_tables" / "loot.json5", {
        "id": "0123456789ABCDEF", "rewards": [],
        "loot_size": 1, "hide_tooltip": False, "use_title": False})


def test_reward_table_new_file_copied(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source_with_table(src)
    plan = ftbq_deploy.plan(src, tgt)
    pf = next(p for p in plan.entries
              if p.rel_path == "reward_tables/loot.json5")
    assert pf.action == "new"
    ftbq_deploy.apply(plan, tgt)
    assert (tgt / "reward_tables" / "loot.json5").exists()


def test_reward_table_collision_backed_up_and_replaced(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_source_with_table(src)
    _write(tgt / "reward_tables" / "loot.json5",
            {"id": "OLDLOOT0000000000", "rewards": []})
    plan = ftbq_deploy.plan(src, tgt)
    pf = next(p for p in plan.entries
              if p.rel_path == "reward_tables/loot.json5")
    assert pf.action == "replace"
    rep = ftbq_deploy.apply(plan, tgt)
    new = to_plain(parse_file(tgt / "reward_tables" / "loot.json5"))
    assert new["id"] == "0123456789ABCDEF"  # skill's table won
    backups = list((tgt / ".ftbq-backup").rglob("loot.json5"))
    assert len(backups) == 1
    assert to_plain(parse_file(backups[0]))["id"] == "OLDLOOT0000000000"
    assert rep.counts["replace"] >= 1


# ---- SNBT (1.20.1) ------------------------------------------------------
# The deployer must handle ``.snbt`` source/target files with the same
# scan / plan / apply / merge logic as JSON5 (ftbq.deploy._classify,
# scan_root, _load, _emit_merged all dispatch by extension). 1.20.1 has no
# lang files.


def _write_snbt(path: Path, obj, **kw) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dump_file_snbt(path, obj, **kw)


def _make_snbt_source(root: Path) -> None:
    _write_snbt(root / "data.snbt",
                {"version": 13, "default_quest_disable_jei": False,
                 "skill_key": 1})
    _write_snbt(root / "chapters" / "intro.snbt", {
        "id": CHAPTER_ID, "filename": "intro",
        "default_quest_shape": "circle", "quests": [
            {"id": QUEST_ID, "x": 0.0, "y": 0.0, "tasks": [], "rewards": []}]})
    _write_snbt(root / ".ftbq-cache" / "manifest.json5",
                {"schema": 1, "pack": "p", "entries": []})


def test_snbt_classify_handles_both_extensions():
    assert ftbq_deploy._classify("data.snbt") == ftbq_deploy.KIND_DATA
    assert ftbq_deploy._classify("data.json5") == ftbq_deploy.KIND_DATA
    assert ftbq_deploy._classify("chapters/intro.snbt") == ftbq_deploy.KIND_CHAPTER
    assert ftbq_deploy._classify("reward_tables/loot.snbt") == ftbq_deploy.KIND_REWARD_TABLE
    # Manifest is always JSON5, even in an SNBT pack.
    assert ftbq_deploy._classify(".ftbq-cache/manifest.json5") == ftbq_deploy.KIND_MANIFEST
    # No lang/ branch for SNBT (1.20.1 has none), but JSON5 lang still classifies.
    assert ftbq_deploy._classify("lang/en_us/quests.json5") == ftbq_deploy.KIND_LANG


def test_snbt_scan_root_picks_up_snbt_files(tmp_path: Path):
    src = tmp_path / "src"
    _make_snbt_source(src)
    entries = {e.rel_path: e for e in ftbq_deploy.scan_root(src)}
    assert "data.snbt" in entries
    assert "chapters/intro.snbt" in entries
    assert entries["data.snbt"].kind == ftbq_deploy.KIND_DATA
    # The parsed value is correct (count type survives round-trip).
    assert entries["data.snbt"].plain["version"] == 13


def test_snbt_deploy_merges_data_and_preserves_user_chapter(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_snbt_source(src)
    # Target already has a data.snbt with a pack-only key + a user chapter.
    _write_snbt(tgt / "data.snbt",
                {"version": 13, "pack_only_key": "keepme"})
    _write_snbt(tgt / "chapters" / "user.snbt", {
        "id": "UUUUUUUUUUUUUUUU", "filename": "user",
        "default_quest_shape": "circle", "quests": []})
    plan = ftbq_deploy.plan(src, tgt)
    data_pf = next(p for p in plan.entries if p.rel_path == "data.snbt")
    assert data_pf.action == "merge"
    ftbq_deploy.apply(plan, tgt)
    merged = parse_snbt_file(tgt / "data.snbt")
    assert merged["pack_only_key"] == "keepme"   # pack key preserved
    assert merged["skill_key"] == 1              # skill key merged in
    assert merged["version"] == 13
    # User chapter untouched; skill chapter deployed.
    assert (tgt / "chapters" / "user.snbt").exists()
    assert (tgt / "chapters" / "intro.snbt").exists()
    # No lang/ deployed (1.20.1).
    assert not (tgt / "lang").exists()


def test_snbt_chapter_collision_backed_up_and_replaced(tmp_path: Path):
    src, tgt = tmp_path / "src", tmp_path / "tgt"
    _make_snbt_source(src)
    _write_snbt(tgt / "chapters" / "intro.snbt", {
        "id": "OLDOLDOLDOLDOLDOL", "filename": "intro",
        "default_quest_shape": "square", "quests": []})
    plan = ftbq_deploy.plan(src, tgt)
    pf = next(p for p in plan.entries if p.rel_path == "chapters/intro.snbt")
    assert pf.action == "replace"
    ftbq_deploy.apply(plan, tgt)
    new = parse_snbt_file(tgt / "chapters" / "intro.snbt")
    assert new["id"] == CHAPTER_ID  # skill's chapter won
    backups = list((tgt / ".ftbq-backup").rglob("intro.snbt"))
    assert len(backups) == 1
    assert parse_snbt_file(backups[0])["id"] == "OLDOLDOLDOLDOLDOL"

