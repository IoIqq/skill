"""Incremental merge tests — pristine, content-edited, position-edited,
user-added, skill-deleted, rename. Each scenario runs a generation, then
mutates the output, then re-generates with a specific --mode.
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
from ftbq.canonical import dump_file
from ftbq.json5 import parse_file, to_plain


FIXTURE = ROOT / "tests" / "fixtures" / "spec_stable.json5"


@pytest.fixture
def initial_run(tmp_path: Path) -> tuple[Path, dict]:
    """Run the generator once and return (output_dir, manifest)."""
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    manifest = generate_quests.generate(spec, out)
    return out, manifest


# ---- classification ----------------------------------------------------


def test_classify_pristine(initial_run):
    out, manifest = initial_run
    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    quest = chap["quests"][0]
    assert generate_quests.classify_quest(
        quest, manifest["entries"]) == "pristine"


def test_classify_content_edited(initial_run):
    out, manifest = initial_run
    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    quest = dict(chap["quests"][0])
    quest["shape"] = "diamond"  # content change
    assert generate_quests.classify_quest(
        quest, manifest["entries"]) == "content-edited"


def test_classify_position_edited(initial_run):
    out, manifest = initial_run
    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    quest = dict(chap["quests"][0])
    quest["x"] = 99.0
    quest["y"] = 99.0
    assert generate_quests.classify_quest(
        quest, manifest["entries"]) == "position-edited"


def test_classify_user_added(initial_run):
    out, manifest = initial_run
    fake_quest = {"id": "ABCDEF0123456789", "x": 5.0, "y": 5.0,
                   "shape": "circle", "dependencies": [], "tasks": [],
                   "rewards": []}
    assert generate_quests.classify_quest(
        fake_quest, manifest["entries"]) == "user-added"


# ---- merge: preserve ---------------------------------------------------


def test_preserve_keeps_user_added_quest(tmp_path: Path):
    """User adds a brand-new quest in the chapter file. Re-running with
    --mode preserve must NOT delete it."""
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    chap_path = out / "quests" / "chapters" / "intro.json5"
    chap = to_plain(parse_file(chap_path))
    user_quest = {
        "id": "DEADBEEFCAFEBABE",
        "x": 5.0, "y": 5.0, "shape": "square",
        "dependencies": [],
        "tasks": [{"id": "FACEFACEFACEFACE", "type": "ftbquests:checkmark"}],
        "rewards": [],
    }
    chap["quests"].append(user_quest)
    dump_file(chap_path, chap)

    generate_quests.generate(spec, out, mode="preserve")
    chap2 = to_plain(parse_file(chap_path))
    user_ids = [q["id"] for q in chap2["quests"]]
    assert "DEADBEEFCAFEBABE" in user_ids


def test_preserve_keeps_user_edited_quest(tmp_path: Path):
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    chap_path = out / "quests" / "chapters" / "intro.json5"
    chap = to_plain(parse_file(chap_path))
    chap["quests"][0]["shape"] = "diamond"
    dump_file(chap_path, chap)

    generate_quests.generate(spec, out, mode="preserve")
    chap2 = to_plain(parse_file(chap_path))
    assert chap2["quests"][0]["shape"] == "diamond"


def test_preserve_keeps_position_edit(tmp_path: Path):
    """Even in default mode, x/y user moves should be preserved (per
    the design's position-edited classification)."""
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    chap_path = out / "quests" / "chapters" / "intro.json5"
    chap = to_plain(parse_file(chap_path))
    qid = chap["quests"][0]["id"]
    chap["quests"][0]["x"] = 7.0
    chap["quests"][0]["y"] = 3.0
    dump_file(chap_path, chap)

    generate_quests.generate(spec, out, mode="overwrite")
    chap2 = to_plain(parse_file(chap_path))
    moved = next(q for q in chap2["quests"] if q["id"] == qid)
    assert moved["x"] == 7.0
    assert moved["y"] == 3.0


# ---- merge: overwrite mode --------------------------------------------


def test_overwrite_drops_user_edits_to_skill_quests(tmp_path: Path):
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    chap_path = out / "quests" / "chapters" / "intro.json5"
    chap = to_plain(parse_file(chap_path))
    chap["quests"][0]["shape"] = "diamond"
    dump_file(chap_path, chap)

    generate_quests.generate(spec, out, mode="overwrite")
    chap2 = to_plain(parse_file(chap_path))
    assert chap2["quests"][0]["shape"] == "circle"


def test_overwrite_still_preserves_user_added(tmp_path: Path):
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    chap_path = out / "quests" / "chapters" / "intro.json5"
    chap = to_plain(parse_file(chap_path))
    chap["quests"].append({
        "id": "AAAAAAAAAAAAAAAA",
        "x": 9.0, "y": 0.0, "shape": "square",
        "dependencies": [], "tasks": [], "rewards": [],
    })
    dump_file(chap_path, chap)

    generate_quests.generate(spec, out, mode="overwrite")
    chap2 = to_plain(parse_file(chap_path))
    assert any(q["id"] == "AAAAAAAAAAAAAAAA" for q in chap2["quests"])


# ---- ask mode ----------------------------------------------------------


def test_ask_keep_path(tmp_path: Path):
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    chap_path = out / "quests" / "chapters" / "intro.json5"
    chap = to_plain(parse_file(chap_path))
    chap["quests"][0]["shape"] = "diamond"
    dump_file(chap_path, chap)

    decisions = []

    def prompt_fn(qid, classification, disk_q, new_q):
        decisions.append((qid, classification))
        return "keep"

    generate_quests.generate(spec, out, mode="ask", prompt_fn=prompt_fn)
    chap2 = to_plain(parse_file(chap_path))
    assert chap2["quests"][0]["shape"] == "diamond"
    assert decisions  # prompt was actually called


def test_ask_overwrite_path(tmp_path: Path):
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    chap_path = out / "quests" / "chapters" / "intro.json5"
    chap = to_plain(parse_file(chap_path))
    chap["quests"][0]["shape"] = "diamond"
    dump_file(chap_path, chap)

    generate_quests.generate(spec, out, mode="ask",
                                prompt_fn=lambda *a, **k: "overwrite")
    chap2 = to_plain(parse_file(chap_path))
    assert chap2["quests"][0]["shape"] == "circle"


# ---- rename detection --------------------------------------------------


def test_rename_preserves_old_id(tmp_path: Path):
    """Rename punch_wood → chop_wood in the spec. With rename_prompt_fn
    confirming, the chap's quest hex ID must equal the OLD md5."""
    out = tmp_path / "quests"
    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)

    old_id = ftbq_ids.quest_id("stable-test-pack", "intro", "punch_wood")

    # Rename in spec.
    spec_text = (tmp_path / "quests.spec.json5").read_text(encoding="utf-8")
    spec_text = spec_text.replace('"punch_wood"', '"chop_wood"')
    # The dependency chain still references "punch_wood" — fix that too.
    (tmp_path / "quests.spec.json5").write_text(spec_text, encoding="utf-8")
    spec2 = generate_quests.load_spec(tmp_path / "quests.spec.json5")

    def rename_prompt(old_name, candidates):
        if old_name == "punch_wood" and "chop_wood" in candidates:
            return "chop_wood"
        return None

    generate_quests.generate(spec2, out, mode="overwrite",
                                rename_prompt_fn=rename_prompt)

    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    chop_quest = next((q for q in chap["quests"] if q["id"] == old_id), None)
    assert chop_quest is not None  # old hex ID was preserved


# ---- adopt mode --------------------------------------------------------


def test_adopt_marks_existing_as_user_added(tmp_path: Path):
    """Pre-existing chapters/ on disk; first-ever generator run with
    --adopt should treat all of it as user-added."""
    out = tmp_path / "quests"
    (out / "quests" / "chapters").mkdir(parents=True)
    pre_existing = {
        "id": "C0DEC0DEC0DEC0DE",
        "filename": "intro",
        "default_quest_shape": "circle",
        "group": "",
        "order_index": 0,
        "quests": [{
            "id": "FEEDFACEFEEDFACE",
            "x": 0.0, "y": 0.0, "shape": "circle",
            "dependencies": [], "tasks": [], "rewards": [],
        }],
    }
    dump_file(out / "quests" / "chapters" / "intro.json5", pre_existing)

    shutil.copyfile(FIXTURE, tmp_path / "quests.spec.json5")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out, adopt=True)

    chap = to_plain(parse_file(out / "quests" / "chapters" / "intro.json5"))
    quest_ids = [q["id"] for q in chap["quests"]]
    # The pre-existing quest survives (user-added), even though its ID
    # was nowhere in the manifest.
    assert "FEEDFACEFEEDFACE" in quest_ids
