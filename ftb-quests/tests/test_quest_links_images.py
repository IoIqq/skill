"""Tests for quest links and chapter background images (Phase 3)."""

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

PACK = "li-test-pack"


def _generate(tmp_path: Path, spec_text: str) -> Path:
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    (tmp_path / "quests.spec.json5").write_text(spec_text, encoding="utf-8")
    spec = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    generate_quests.generate(spec, out)
    return out


def test_quest_link_resolved_to_hex(tmp_path: Path):
    spec = (
        '{ pack: "' + PACK + '", chapters: [\n'
        '  { name: "src", default_quest_shape: "circle",\n'
        '    quests: [{ name: "origin", tasks: [], rewards: [] }] },\n'
        '  { name: "mirror", default_quest_shape: "circle",\n'
        '    quests: [],\n'
        '    quest_links: [{ name: "lnk", linked_quest: "src/origin",\n'
        '                     x: 3.0, y: -1.0 }] }\n] }')
    out = _generate(tmp_path, spec)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "mirror.json5"))
    link = chap["quest_links"][0]
    assert link["id"] == ftbq_ids.quest_link_id(PACK, "mirror", "lnk")
    assert link["linked_quest"] == ftbq_ids.quest_id(PACK, "src", "origin")
    assert link["x"] == 3.0
    assert link["y"] == -1.0
    assert "shape" not in link  # omitted when unset
    assert "size" not in link   # omitted when default 1


def test_quest_link_raw_hex_passthrough(tmp_path: Path):
    spec = (
        '{ pack: "' + PACK + '", chapters: [\n'
        '  { name: "c", default_quest_shape: "circle", quests: [],\n'
        '    quest_links: [{ name: "lnk",\n'
        '      linked_quest: "0123456789ABCDEF" }] }] }')
    out = _generate(tmp_path, spec)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    assert chap["quest_links"][0]["linked_quest"] == "0123456789ABCDEF"


def test_quest_links_omitted_when_empty(tmp_path: Path):
    spec = (
        '{ pack: "' + PACK + '", chapters: [\n'
        '  { name: "c", default_quest_shape: "circle",\n'
        '    quests: [{ name: "q", tasks: [], rewards: [] }] }] }')
    out = _generate(tmp_path, spec)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    assert "quest_links" not in chap
    assert "images" not in chap


def test_chapter_image_full(tmp_path: Path):
    spec = (
        '{ pack: "' + PACK + '", chapters: [\n'
        '  { name: "src", default_quest_shape: "circle",\n'
        '    quests: [{ name: "origin", tasks: [], rewards: [] }] },\n'
        '  { name: "c", default_quest_shape: "circle",\n'
        '    quests: [],\n'
        '    images: [{ name: "bg", image: "minecraft:textures/gui/bg.png",\n'
        '      x: 0.0, y: 0.0, width: 4.0, height: 2.0, rotation: 90.0,\n'
        '      color: 16777215, alpha: 128, order: 1,\n'
        '      click: "/say hi", dev: true, corner: true,\n'
        '      dependency: "src/origin" }] }] }')
    out = _generate(tmp_path, spec)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    img = chap["images"][0]
    assert img["id"] == ftbq_ids.image_id(PACK, "c", "bg")
    assert img["image"] == "minecraft:textures/gui/bg.png"
    assert img["width"] == 4.0
    assert img["height"] == 2.0
    assert img["rotation"] == 90.0
    assert img["alpha"] == 128
    assert img["order"] == 1
    assert img["click"] == "/say hi"
    assert img["dev"] is True
    assert img["corner"] is True
    assert img["dependency"] == ftbq_ids.quest_id(PACK, "src", "origin")


def test_chapter_passthrough_progression_mode(tmp_path: Path):
    """Extra chapter fields (progression_mode, etc.) pass through verbatim."""
    spec = (
        '{ pack: "' + PACK + '", chapters: [\n'
        '  { name: "c", default_quest_shape: "circle",\n'
        '    progression_mode: "linear", always_invisible: false,\n'
        '    quests: [{ name: "q", tasks: [], rewards: [] }] }] }')
    out = _generate(tmp_path, spec)
    chap = to_plain(parse_file(out / "quests" / "chapters" / "c.json5"))
    assert chap["progression_mode"] == "linear"
    assert chap["always_invisible"] is False
    assert "layout" not in chap  # spec-only directive, not emitted


def test_unknown_quest_link_target_rejected(tmp_path: Path):
    spec = (
        '{ pack: "' + PACK + '", chapters: [\n'
        '  { name: "c", default_quest_shape: "circle", quests: [],\n'
        '    quest_links: [{ name: "lnk", linked_quest: "nope/missing" }] }] }')
    (tmp_path / "quests.spec.json5").write_text(spec, encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)
    spec_obj = generate_quests.load_spec(tmp_path / "quests.spec.json5")
    with pytest.raises(generate_quests.SpecError):
        generate_quests.generate(spec_obj, out)
