"""Tests for scripts/extract_items.py — synthetic jars built fresh in
tmp_path (no binary fixtures committed). Covers the id-only ``items.json5``
AND the name→id ``item_names.json5`` written in the same scan."""

from __future__ import annotations

import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load extract_items.py without it being on a normal Python path.
_spec = importlib.util.spec_from_file_location(
    "extract_items", ROOT / "scripts" / "extract_items.py")
extract_items = importlib.util.module_from_spec(_spec)
sys.modules["extract_items"] = extract_items
_spec.loader.exec_module(extract_items)


CREATE_EN = json.dumps({
    "item.create.cogwheel": "Cogwheel",
    "block.create.gearbox": "Gearbox",
})
CREATE_ZH = json.dumps({
    "item.create.cogwheel": "齿轮",
    "block.create.gearbox": "齿轮箱",
})
MC_EN = json.dumps({
    "item.minecraft.copper_ingot": "Copper Ingot",
    "item.minecraft.iron_ingot": "Iron Ingot",
})
CREATE_COPPER_EN = json.dumps({
    "item.create.copper_ingot": "Copper Ingot",
})


def test_extracts_ids_and_en_names(make_jar):
    jar = make_jar("create.jar",
                   {"assets/create/lang/en_us.json": CREATE_EN})
    modid, items, lang_file, names = extract_items._extract_jar(jar)
    assert modid == "create"
    assert "create:cogwheel" in items
    assert "create:gearbox" in items
    assert lang_file.endswith("en_us.json")
    assert names["en_us"]["Cogwheel"] == "create:cogwheel"
    assert names["en_us"]["Gearbox"] == "create:gearbox"
    assert names["zh_cn"] == {}


def test_zh_names_when_shipped(make_jar):
    jar = make_jar("create.jar", {
        "assets/create/lang/en_us.json": CREATE_EN,
        "assets/create/lang/zh_cn.json": CREATE_ZH,
    })
    _modid, _items, _lang_file, names = extract_items._extract_jar(jar)
    assert names["en_us"]["Cogwheel"] == "create:cogwheel"
    assert names["zh_cn"]["齿轮"] == "create:cogwheel"
    assert names["zh_cn"]["齿轮箱"] == "create:gearbox"


def test_no_lang_jar(make_jar):
    jar = make_jar("nolang.jar", {"META-INF/mods.toml": "modId=create"})
    modid, items, _lang_file, names = extract_items._extract_jar(jar)
    assert modid is None
    assert items == []
    assert names == {}


def test_corrupt_jar_yields_empty(tmp_path: Path):
    bad = tmp_path / "broken.jar"
    bad.write_bytes(b"not a zip at all")
    modid, items, _lang_file, names = extract_items._extract_jar(bad)
    assert modid is None
    assert items == []
    assert names == {}


def test_names_from_lang_skips_empty_values():
    data = {"item.create.x": "X", "item.create.y": "",
            "block.create.z": "Z", "item.other.noop": "N"}
    out = extract_items._names_from_lang(data, "create")
    # "y" skipped (empty value); "other.noop" skipped (namespace mismatch).
    assert out == {"X": "create:x", "Z": "create:z"}


def _build_jars(mods: Path, *specs: tuple[str, dict]) -> None:
    for name, files in specs:
        with zipfile.ZipFile(mods / name, "w") as zf:
            for arc, data in files.items():
                if isinstance(data, str):
                    data = data.encode("utf-8")
                zf.writestr(arc, data)


def test_ambiguous_name_across_mods(tmp_path: Path):
    """Two mods both ship 'Copper Ingot' → lands in `ambiguous`, not
    name_to_id. Iron Ingot (only minecraft) stays unambiguous."""
    pack = tmp_path / "pack"
    mods = pack / "mods"
    mods.mkdir(parents=True)
    _build_jars(mods,
        ("minecraft.jar", {"assets/minecraft/lang/en_us.json": MC_EN}),
        ("create.jar", {"assets/create/lang/en_us.json": CREATE_COPPER_EN}),
    )
    _parsed, _no_lang, name_to_ids = extract_items.scan_directory(pack)
    names_cache = extract_items._assemble_names(pack, name_to_ids)
    assert "Copper Ingot" not in names_cache["name_to_id"]
    assert "Copper Ingot" in names_cache["ambiguous"]
    assert set(names_cache["ambiguous"]["Copper Ingot"]) == {
        "minecraft:copper_ingot", "create:copper_ingot"}
    assert names_cache["name_to_id"]["Iron Ingot"] == "minecraft:iron_ingot"
    assert names_cache["name_count"] == 2  # Copper Ingot + Iron Ingot
    assert names_cache["id_count"] == 3


def test_build_cache_and_build_names_cache(tmp_path: Path):
    pack = tmp_path / "pack"
    mods = pack / "mods"
    mods.mkdir(parents=True)
    _build_jars(mods,
        ("create.jar", {"assets/create/lang/en_us.json": CREATE_EN,
                         "assets/create/lang/zh_cn.json": CREATE_ZH}),
    )
    items = extract_items.build_cache(pack)
    assert "create:cogwheel" in items["all_item_ids"]
    names = extract_items.build_names_cache(pack)
    assert names["name_to_id"]["Cogwheel"] == "create:cogwheel"
    assert names["name_to_id"]["齿轮"] == "create:cogwheel"


def test_full_pipeline_writes_both_caches(tmp_path: Path):
    pack = tmp_path / "pack"
    mods = pack / "mods"
    mods.mkdir(parents=True)
    _build_jars(mods,
        ("create.jar", {"assets/create/lang/en_us.json": CREATE_EN,
                         "assets/create/lang/zh_cn.json": CREATE_ZH}),
        ("empty.jar", {"META-INF/mods.toml": "modId=empty"}),
    )
    output = pack / "config" / "ftbquests" / "quests"
    rc = extract_items.main([str(pack), "--output", str(output), "--quiet"])
    assert rc == 0

    from ftbq.json5 import parse_file, to_plain
    items = to_plain(parse_file(output / ".ftbq-cache" / "items.json5"))
    assert "create:cogwheel" in items["all_item_ids"]
    assert items["count"] == 1
    assert len(items["no_lang"]) == 1

    names = to_plain(parse_file(output / ".ftbq-cache" / "item_names.json5"))
    assert names["name_to_id"]["Cogwheel"] == "create:cogwheel"
    assert names["name_to_id"]["齿轮"] == "create:cogwheel"
    assert names["ambiguous"] == {}


def test_no_names_flag_skips_name_index(tmp_path: Path):
    pack = tmp_path / "pack"
    mods = pack / "mods"
    mods.mkdir(parents=True)
    _build_jars(mods,
        ("create.jar", {"assets/create/lang/en_us.json": CREATE_EN}),
    )
    output = pack / "config" / "ftbquests" / "quests"
    extract_items.main([str(pack), "--output", str(output),
                         "--no-names", "--quiet"])
    assert (output / ".ftbq-cache" / "items.json5").exists()
    assert not (output / ".ftbq-cache" / "item_names.json5").exists()
