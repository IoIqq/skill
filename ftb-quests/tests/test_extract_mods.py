"""Tests for scripts/extract_mods.py — golden tests on synthetic jars
built fresh in a tmp_path (no binary fixtures committed)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load extract_mods.py without it being on a normal Python path.
_spec = importlib.util.spec_from_file_location(
    "extract_mods", ROOT / "scripts" / "extract_mods.py")
extract_mods = importlib.util.module_from_spec(_spec)
sys.modules["extract_mods"] = extract_mods
_spec.loader.exec_module(extract_mods)


FORGE_TOML = """
modLoader = "javafml"
loaderVersion = "[40,)"
license = "MIT"

[[mods]]
modId = "create"
version = "0.5.1.j"
displayName = "Create"
side = "BOTH"
description = '''
Aesthetic kinetics — windmills, mixers, conveyors.
'''

[[dependencies.create]]
modId = "minecraft"
mandatory = true
versionRange = "[1.20.1]"
side = "BOTH"
"""

NEOFORGE_TOML = """
modLoader = "javafml"
loaderVersion = "[1,)"

[[mods]]
modId = "neomod"
version = "1.0.0"
displayName = "Neo Mod"
side = "CLIENT"
description = "A NeoForge mod."
"""

FABRIC_JSON = json.dumps({
    "schemaVersion": 1,
    "id": "jei",
    "version": "15.2.0",
    "name": "Just Enough Items",
    "description": "Recipe viewer",
    "environment": "client",
    "depends": {"minecraft": "1.20.1"},
})

LEGACY_MCMOD = json.dumps([{
    "modid": "tconstruct",
    "name": "Tinkers' Construct",
    "version": "1.12.2-2.13.0.183",
    "mcversion": "1.12.2",
    "description": "A tool customization mod.",
}])


def test_extracts_forge_toml(make_jar):
    jar = make_jar("create.jar",
                    {"META-INF/mods.toml": FORGE_TOML})
    meta = extract_mods.extract_one(jar)
    assert meta is not None
    assert meta["modid"] == "create"
    assert meta["loader"] == "forge"
    assert meta["side"] == "both"
    assert "1.20.1" in "".join(meta["mc_versions"])


def test_extracts_neoforge_toml(make_jar):
    jar = make_jar("neomod.jar",
                    {"META-INF/neoforge.mods.toml": NEOFORGE_TOML})
    meta = extract_mods.extract_one(jar)
    assert meta is not None
    assert meta["modid"] == "neomod"
    assert meta["loader"] == "neoforge"
    assert meta["side"] == "client"


def test_extracts_fabric_json(make_jar):
    jar = make_jar("jei.jar", {"fabric.mod.json": FABRIC_JSON})
    meta = extract_mods.extract_one(jar)
    assert meta is not None
    assert meta["modid"] == "jei"
    assert meta["loader"] == "fabric"
    assert meta["side"] == "client"


def test_extracts_legacy_mcmod(make_jar):
    jar = make_jar("tic.jar", {"mcmod.info": LEGACY_MCMOD})
    meta = extract_mods.extract_one(jar)
    assert meta is not None
    assert meta["modid"] == "tconstruct"
    assert meta["loader"] == "forge-legacy"


def test_unrecognized_jar(make_jar):
    """Has zip structure but no recognized metadata file."""
    jar = make_jar("random.jar", {"some/asset.png": b"\x89PNG"})
    meta = extract_mods.extract_one(jar)
    assert meta is None


def test_corrupt_jar_yields_none(tmp_path: Path):
    bad = tmp_path / "broken.jar"
    bad.write_bytes(b"not a zip at all")
    meta = extract_mods.extract_one(bad)
    assert meta is None


def test_neoforge_takes_priority_over_forge(make_jar):
    """When both files exist, NeoForge wins (the loader checks it first)."""
    jar = make_jar("dual.jar", {
        "META-INF/neoforge.mods.toml": NEOFORGE_TOML,
        "META-INF/mods.toml": FORGE_TOML,
    })
    meta = extract_mods.extract_one(jar)
    assert meta is not None
    assert meta["loader"] == "neoforge"
    assert meta["modid"] == "neomod"


def test_full_pipeline_writes_cache(tmp_path: Path, make_jar):
    """End-to-end: build several jars under <pack>/mods, run main(),
    verify the cache file shape."""
    pack = tmp_path / "pack"
    mods = pack / "mods"
    mods.mkdir(parents=True)

    for name, files in [
        ("create.jar", {"META-INF/mods.toml": FORGE_TOML}),
        ("jei.jar", {"fabric.mod.json": FABRIC_JSON}),
        ("broken.jar", {}),  # empty zip → no metadata
    ]:
        jar_path = mods / name
        import zipfile
        with zipfile.ZipFile(jar_path, "w") as zf:
            for arc, data in files.items():
                if isinstance(data, str):
                    data = data.encode("utf-8")
                zf.writestr(arc, data)

    output = pack / "config" / "ftbquests" / "quests"
    extract_mods.main([str(pack), "--output", str(output), "--quiet"])

    cache_path = output / ".ftbq-cache" / "mods.json5"
    assert cache_path.exists()

    # Reuse the JSON5 parser we trust.
    from ftbq.json5 import parse_file, to_plain
    cache = to_plain(parse_file(cache_path))
    assert cache["count"] == 2
    modids = {m["modid"] for m in cache["mods"]}
    assert modids == {"create", "jei"}
    assert len(cache["unparseable"]) == 1
    assert cache["unparseable"][0]["jar"].endswith("broken.jar")


def test_normalize_side_handles_variants():
    f = extract_mods._normalize_side
    assert f("CLIENT") == "client"
    assert f("server") == "server"
    assert f("BOTH") == "both"
    assert f("DEDICATED_SERVER") == "server"
    assert f(None) == "both"
    assert f("") == "both"
    assert f("garbage") == "both"


def test_fabric_environment_star_means_both(make_jar):
    obj = json.loads(FABRIC_JSON)
    obj["environment"] = "*"
    jar = make_jar("any.jar", {"fabric.mod.json": json.dumps(obj)})
    meta = extract_mods.extract_one(jar)
    assert meta is not None
    assert meta["side"] == "both"
