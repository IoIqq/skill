"""Token-saving CLI tests: pack_briefing + quest_detail.

``pack_briefing`` curates the .ftbq-cache/ indexes into one compact summary
(replaces reading mods.json5/existing_quests.json5/audit_report raw).
``quest_detail`` previews one quest (replaces reading the whole chapter file
in the Step 4 loop).
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ftbq import ids as ftbq_ids  # noqa: E402
from ftbq.json5 import parse_file, to_plain  # noqa: E402

_spec_brief = importlib.util.spec_from_file_location(
    "pack_briefing_cli", ROOT / "scripts" / "pack_briefing.py")
briefing_cli = importlib.util.module_from_spec(_spec_brief)
sys.modules["pack_briefing_cli"] = briefing_cli
_spec_brief.loader.exec_module(briefing_cli)

_spec_qd = importlib.util.spec_from_file_location(
    "quest_detail_cli", ROOT / "scripts" / "quest_detail.py")
quest_detail_cli = importlib.util.module_from_spec(_spec_qd)
sys.modules["quest_detail_cli"] = quest_detail_cli
_spec_qd.loader.exec_module(quest_detail_cli)

_spec_gq = importlib.util.spec_from_file_location(
    "gq_brief", ROOT / "scripts" / "generate_quests.py")
generate_quests = importlib.util.module_from_spec(_spec_gq)
sys.modules["gq_brief"] = generate_quests
_spec_gq.loader.exec_module(generate_quests)

_spec_iq = importlib.util.spec_from_file_location(
    "index_quests_cli", ROOT / "scripts" / "index_quests.py")
index_quests = importlib.util.module_from_spec(_spec_iq)
sys.modules["index_quests_cli"] = index_quests
_spec_iq.loader.exec_module(index_quests)

_spec_ad = importlib.util.spec_from_file_location(
    "audit_diff_brief", ROOT / "scripts" / "audit_diff.py")
audit_diff = importlib.util.module_from_spec(_spec_ad)
sys.modules["audit_diff_brief"] = audit_diff
_spec_ad.loader.exec_module(audit_diff)


def _make_modpack(root: Path) -> Path:
    qd = root / "config" / "ftbquests" / "quests"
    qd.mkdir(parents=True, exist_ok=True)
    (qd / "data.json5").write_text("{ default_reward_team: false }\n",
                                    encoding="utf-8")
    (qd / "chapters").mkdir(exist_ok=True)
    (qd / "chapters" / "getting_started.json5").write_text(
        '{\n'
        '  id: "1111111111111111",\n'
        '  filename: "getting_started",\n'
        '  default_quest_shape: "circle",\n'
        '  quests: [\n'
        '    { id: "2222222222222222", x: 0.0, y: 0.0, shape: "circle",\n'
        '      dependencies: [], tasks: [], rewards: [] },\n'
        '  ],\n'
        '}\n', encoding="utf-8")
    (qd / "lang" / "en_us").mkdir(parents=True, exist_ok=True)
    (qd / "lang" / "en_us" / "quests.json5").write_text(
        '{\n'
        '  "quest.2222222222222222.quest_desc": '
        '["Collect &esmall_cogwheel小齿轮&r."],\n'
        '}\n', encoding="utf-8")
    return root


# --------------------------------------------------------------- pack_briefing

def test_pack_briefing_summarizes_caches(capsys):
    a = Path(__file__).parent / "_brief_a"
    b = Path(__file__).parent / "_brief_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_modpack(a)
        _make_modpack(b)
        # build caches: existing_quests (a) + audit indexes/report (a+b)
        index_quests.main([str(a), "-q"])
        audit_diff.main([str(a), str(b), "--remember", "-q"])
        capsys.readouterr()
        rc = briefing_cli.main([str(a), "--json"])
        assert rc == 0
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["format"] == "json5"
        assert data["chapter_count"] == 1
        assert data["quest_count"] == 1
        assert data["chapters"][0]["name"] == "getting_started"
        assert data["caches"]["existing_quests"] is True
        assert data["caches"]["audit_report"] is True
        assert data["caches"]["mods"] is False  # no mods/ dir
        assert data["audit"]["identical"] is True
        assert data["audit"]["dlc_patterns"] == 1
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_pack_briefing_text_mode_reports_missing_caches(capsys):
    a = Path(__file__).parent / "_brief_missing"
    if a.exists():
        import shutil
        shutil.rmtree(a)
    try:
        _make_modpack(a)
        # no caches built at all
        rc = briefing_cli.main([str(a)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "mods ✗" in out
        assert "existing_quests ✗" in out
        assert "audit_report ✗" in out
        # counts come from the existing_quests cache, which is missing → 0
        assert "quests: 0" in out
        assert "chapters: 0" in out
    finally:
        import shutil
        shutil.rmtree(a, ignore_errors=True)


# --------------------------------------------------------------- quest_detail

def _make_generated_pack(tmp_path: Path) -> Path:
    """A real generated output_dir with one quest that has tasks/rewards."""
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    (out / "quests.spec.json5").write_text(
        '{ pack: "p", format: "json5", default_locale: "en_us",'
        ' locales: ["en_us"], chapters: [{ name: "c",'
        ' default_quest_shape: "circle", quests: [{ name: "q", depends_on: [],'
        ' tasks: [{ name: "logs", type: "ftbquests:item",'
        ' item: "minecraft:oak_log", count: 4, consume_items: true }],'
        ' rewards: [{ name: "apple", type: "ftbquests:item",'
        ' item: "minecraft:apple", count: 2 }] }] }] }',
        encoding="utf-8")
    spec = generate_quests.load_spec(out / "quests.spec.json5")
    generate_quests.generate(spec, out)
    # add lang for the quest
    qid = ftbq_ids.quest_id("p", "c", "q")
    lang = out / "quests" / "lang" / "en_us" / "quests.json5"
    lang.parent.mkdir(parents=True, exist_ok=True)
    # the generator already wrote a lang file (possibly empty); rewrite w/ entries
    lang.write_text(
        f'{{ "quest.{qid}.title": "Punching Wood",'
        f' "quest.{qid}.quest_desc": ["Collect 4 oak logs."] }}\n',
        encoding="utf-8")
    return out


def test_quest_detail_shows_one_quest(tmp_path, capsys):
    out = _make_generated_pack(tmp_path)
    rc = quest_detail_cli.main([str(out), "c/q", "--json"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ref"] == "c/q"
    assert data["id"] == ftbq_ids.quest_id("p", "c", "q")
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["type"] == "ftbquests:item"
    assert len(data["rewards"]) == 1
    lang = data["lang"]["en_us"]
    assert lang["title"] == "Punching Wood"
    assert lang["quest_desc"] == ["Collect 4 oak logs."]


def test_quest_detail_text_is_compact(tmp_path, capsys):
    out = _make_generated_pack(tmp_path)
    rc = quest_detail_cli.main([str(out), "c/q"])
    assert rc == 0
    text = capsys.readouterr().out
    # one quest only — no other quest leaks in
    assert "logs" in text and "ftbquests:item" in text
    assert "apple" in text
    assert "Punching Wood" in text
    assert "Collect 4 oak logs" in text


def test_quest_detail_unknown_quest_errors(tmp_path, capsys):
    out = _make_generated_pack(tmp_path)
    rc = quest_detail_cli.main([str(out), "c/nope"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "not in chapter" in err


def test_quest_detail_skeleton_quest_empty_tasks(tmp_path, capsys):
    """A skeleton quest (empty tasks/rewards) previews cleanly — useful in
    the Step 4 loop before polishing a node."""
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    (out / "quests.spec.json5").write_text(
        '{ pack: "p", format: "json5", default_locale: "en_us",'
        ' locales: ["en_us"], chapters: [{ name: "c",'
        ' default_quest_shape: "circle", quests: [{ name: "q", depends_on: [],'
        ' tasks: [], rewards: [] }] }] }', encoding="utf-8")
    generate_quests.generate(generate_quests.load_spec(out / "quests.spec.json5"), out)
    rc = quest_detail_cli.main([str(out), "c/q", "--json"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert data["tasks"] == []
    assert data["rewards"] == []
