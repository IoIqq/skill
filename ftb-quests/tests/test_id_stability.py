"""End-to-end tests for scripts/generate_quests.py.

Covers idempotency, layout determinism, ID stability, lang rewriting,
manifest shape.
"""

from __future__ import annotations

import importlib.util
import shutil
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

from ftbq import ids as ftbq_ids
from ftbq.json5 import parse_file, to_plain
from ftbq.snbt import parse_snbt_file


FIXTURE = ROOT / "tests" / "fixtures" / "spec_stable.json5"


def _generate(tmp_path: Path) -> Path:
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    out.mkdir(parents=True, exist_ok=True)
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    return out


# ---- core invariants ---------------------------------------------------


def test_generates_expected_files(tmp_path: Path):
    out = _generate(tmp_path)
    assert (out / "quests" / "data.json5").exists()
    assert (out / "quests" / "chapters" / "intro.json5").exists()
    assert (out / "quests" / ".ftbq-cache" / "manifest.json5").exists()


def test_idempotent_byte_identical(tmp_path: Path):
    """Same spec → same chapter file, byte-for-byte."""
    out1 = _generate(tmp_path)
    chap1 = (out1 / "quests" / "chapters" / "intro.json5").read_bytes()
    # Tear down everything except spec and re-generate.
    for p in [out1 / "quests" / "chapters", out1 / "quests" / "data.json5"]:
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out1)
    chap2 = (out1 / "quests" / "chapters" / "intro.json5").read_bytes()
    assert chap1 == chap2


def test_quest_ids_match_md5_formula(tmp_path: Path):
    out = _generate(tmp_path)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    expected_punch = ftbq_ids.quest_id("stable-test-pack", "intro", "punch_wood")
    expected_bench = ftbq_ids.quest_id("stable-test-pack", "intro", "make_bench")
    quest_ids = {q["id"] for q in chap["quests"]}
    assert expected_punch in quest_ids
    assert expected_bench in quest_ids


def test_dependencies_resolved_to_hex(tmp_path: Path):
    out = _generate(tmp_path)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    bench = next(q for q in chap["quests"] if q["id"] ==
                  ftbq_ids.quest_id("stable-test-pack", "intro", "make_bench"))
    expected_dep = ftbq_ids.quest_id("stable-test-pack", "intro", "punch_wood")
    assert bench["dependencies"] == [expected_dep]


def test_bare_string_item_normalized(tmp_path: Path):
    out = _generate(tmp_path)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    punch = next(q for q in chap["quests"] if q["dependencies"] == [])
    item = punch["tasks"][0]["item"]
    assert isinstance(item, dict)
    assert item == {"id": "minecraft:oak_log", "count": 1}


def test_layout_assigns_increasing_x(tmp_path: Path):
    out = _generate(tmp_path)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    # punch_wood (depth 0) should be at x=0, make_bench (depth 1) at x=1.5
    by_id = {q["id"]: q for q in chap["quests"]}
    pw = by_id[ftbq_ids.quest_id("stable-test-pack", "intro", "punch_wood")]
    mb = by_id[ftbq_ids.quest_id("stable-test-pack", "intro", "make_bench")]
    assert pw["x"] == 0.0
    assert mb["x"] == 1.5


# ---- manifest ----------------------------------------------------------


def test_manifest_records_all_skill_owned_objects(tmp_path: Path):
    out = _generate(tmp_path)
    manifest = to_plain(parse_file(out / "quests" / ".ftbq-cache" / "manifest.json5"))
    kinds = [e["kind"] for e in manifest["entries"]]
    assert kinds.count("chapter") == 1
    assert kinds.count("quest") == 2
    assert kinds.count("task") == 2
    assert kinds.count("reward") == 2


def test_manifest_quest_has_aliases_field(tmp_path: Path):
    out = _generate(tmp_path)
    manifest = to_plain(parse_file(out / "quests" / ".ftbq-cache" / "manifest.json5"))
    quest_entries = [e for e in manifest["entries"] if e["kind"] == "quest"]
    for q in quest_entries:
        assert "aliases" in q
        assert q["aliases"] == []


def test_manifest_quest_x_y_separate_from_content_hash(tmp_path: Path):
    """A quest whose x/y differs but content is identical should hash
    the same — incremental merge needs this for 'position-edited'."""
    out = _generate(tmp_path)
    manifest = to_plain(parse_file(out / "quests" / ".ftbq-cache" / "manifest.json5"))
    quest_entry = next(e for e in manifest["entries"] if e["kind"] == "quest")
    assert "x" in quest_entry
    assert "y" in quest_entry
    assert "content_hash" in quest_entry


# ---- lang rewriting ----------------------------------------------------


def test_lang_placeholders_rewritten_to_hex(tmp_path: Path):
    out = _generate(tmp_path)
    out.mkdir(parents=True, exist_ok=True)
    lang_path = out / "quests" / "lang" / "en_us" / "quests.json5"
    lang_path.parent.mkdir(parents=True, exist_ok=True)
    placeholder = (
        '{\n'
        '  "@intro.title": "Intro Chapter",\n'
        '  "@intro/punch_wood.title": "Punch Wood",\n'
        '  "@intro/make_bench.title": "Make Bench",\n'
        '}\n'
    )
    lang_path.write_text(placeholder, encoding="utf-8")

    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    rewritten = to_plain(parse_file(lang_path))
    chapter_hex = ftbq_ids.chapter_id("stable-test-pack", "intro")
    quest_hex = ftbq_ids.quest_id("stable-test-pack", "intro", "punch_wood")
    assert f"chapter.{chapter_hex}.title" in rewritten
    assert f"quest.{quest_hex}.title" in rewritten
    # No raw @placeholder keys remain.
    assert not any(k.startswith("@") for k in rewritten)


# ---- spec validation ---------------------------------------------------


def test_load_spec_rejects_missing_pack(tmp_path: Path):
    bad = tmp_path / "bad.json5"
    bad.write_text('{ chapters: [] }', encoding="utf-8")
    with pytest.raises(generate_quests.SpecError):
        generate_quests.load_spec(bad)


def test_load_spec_rejects_unsupported_format(tmp_path: Path):
    bad = tmp_path / "bad.json5"
    bad.write_text(
        '{ pack: "p", format: "yaml", chapters: [] }',
        encoding="utf-8")
    with pytest.raises(generate_quests.SpecError):
        generate_quests.load_spec(bad)


def test_load_spec_accepts_snbt_format(tmp_path: Path):
    """1.20.1 SNBT is a supported format (see ftbq/snbt.py + reference §12);
    it must load and emit ``.snbt`` files with no lang/ directory."""
    spec_path = tmp_path / "quests.spec.json5"
    spec_path.write_text(
        '{ pack: "p", format: "snbt",'
        ' chapters: [{ name: "intro", quests: ['
        ' { name: "a", title: "A", tasks: [{ name: "t", type: "ftbquests:item",'
        ' item: { id: "minecraft:oak_log", count: 4 } }], rewards: [] } ] } ] }',
        encoding="utf-8")
    spec = generate_quests.load_spec(spec_path)
    assert spec["format"] == "snbt"
    out = tmp_path / "quests"
    out.mkdir(parents=True, exist_ok=True)
    manifest = generate_quests.generate(spec, out)
    assert manifest["format"] == "snbt"
    root = out / "quests"  # generate() writes under <output_dir>/quests/
    assert (root / "data.snbt").exists()
    assert (root / "chapters" / "intro.snbt").exists()
    assert not (root / "lang").exists()  # 1.20.1 has no lang files
    # Inline text is on the quest object, and task count is a long (ItemTask).
    chapter = parse_snbt_file(root / "chapters" / "intro.snbt")
    assert chapter["quests"][0]["title"] == "A"
    assert chapter["quests"][0]["tasks"][0]["count"] == 4
