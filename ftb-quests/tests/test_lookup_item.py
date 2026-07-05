"""Tests for scripts/lookup_item.py — batch name→id lookup against a fake
.ftbq-cache/item_names.json5 (+ optional audit_index.json5 live merge)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "lookup_item", ROOT / "scripts" / "lookup_item.py")
lookup_item = importlib.util.module_from_spec(_spec)
sys.modules["lookup_item"] = lookup_item
_spec.loader.exec_module(lookup_item)

from ftbq.canonical import dump_file  # noqa: E402


def _write_name_index(cache_dir: Path, name_to_id=None, ambiguous=None):
    cache_dir.mkdir(parents=True, exist_ok=True)
    n2id = name_to_id or {}
    amb = ambiguous or {}
    idx = {
        "schema": 1, "scanned_at": "2026Z", "modpack_dir": "x",
        "sources": ["en_us", "zh_cn"],
        "name_count": len(n2id) + len(amb),
        "id_count": len(set(n2id.values())
                        | {i for ids in amb.values() for i in ids}),
        "name_to_id": dict(sorted(n2id.items())),
        "ambiguous": dict(sorted(amb.items())),
    }
    dump_file(cache_dir / "item_names.json5", idx,
              key_order=["schema", "scanned_at", "modpack_dir", "sources",
                         "name_count", "id_count", "name_to_id", "ambiguous"])


def _write_audit_index(cache_dir: Path, patterns: list[tuple[str, str]]):
    """patterns: [(item_id, name), …]. Written so ftbq_audit.load_index reads
    it back (quests_dir = cache_dir.parent)."""
    ips = [{"item_id": iid, "name": nm, "raw": f"&e{iid}{nm}&r"}
           for iid, nm in patterns]
    idx = {"schema": 1, "scanned_at": "2026Z", "quests_dir": "x",
           "format": "json5",
           "quests": [{"id": "AAAA", "chapter": "ch",
                       "source_file": "lang/en_us/quests.json5",
                       "locale": "en_us", "item_patterns": ips}]}
    dump_file(cache_dir / "audit_index.json5", idx,
              key_order=["schema", "scanned_at", "quests_dir", "format",
                         "quests"],
              per_path_key_order={
                  "quests.[]": ["id", "chapter", "source_file",
                                  "locale", "item_patterns"],
                  "quests.[].item_patterns.[]": ["item_id", "name", "raw"]})


@pytest.fixture
def cache_dir(tmp_path: Path) -> Path:
    return tmp_path / ".ftbq-cache"


def test_exact_name_found(cache_dir):
    _write_name_index(cache_dir, {"Cogwheel": "create:cogwheel"})
    res, _ = lookup_item.build_results(cache_dir.parent, ["Cogwheel"],
                                         cache_dir=cache_dir)
    assert res[0]["status"] == "found"
    assert res[0]["id"] == "create:cogwheel"
    assert res[0]["source"] == "jar"


def test_case_insensitive_match(cache_dir):
    _write_name_index(cache_dir, {"Cogwheel": "create:cogwheel"})
    res, _ = lookup_item.build_results(cache_dir.parent, ["cogwheel"],
                                         cache_dir=cache_dir)
    assert res[0]["status"] == "found"
    assert res[0]["id"] == "create:cogwheel"


def test_zh_name_found(cache_dir):
    _write_name_index(cache_dir, {"齿轮": "create:cogwheel"})
    res, _ = lookup_item.build_results(cache_dir.parent, ["齿轮"],
                                         cache_dir=cache_dir)
    assert res[0]["status"] == "found"
    assert res[0]["source"] == "jar"


def test_ambiguous_surfaces_all_ids(cache_dir):
    _write_name_index(cache_dir, ambiguous={
        "Copper Ingot": ["create:copper_ingot", "minecraft:copper_ingot"]})
    res, _ = lookup_item.build_results(cache_dir.parent, ["Copper Ingot"],
                                         cache_dir=cache_dir)
    assert res[0]["status"] == "ambiguous"
    assert {e["id"] for e in res[0]["ids"]} == {
        "create:copper_ingot", "minecraft:copper_ingot"}


def test_audit_merge_resolves_name(cache_dir):
    """item_names has only English; audit supplies the Chinese name."""
    _write_name_index(cache_dir, {"Cogwheel": "create:cogwheel"})
    _write_audit_index(cache_dir, [("create:cogwheel", "齿轮")])
    res, _ = lookup_item.build_results(cache_dir.parent, ["齿轮"],
                                         cache_dir=cache_dir)
    assert res[0]["status"] == "found"
    assert res[0]["id"] == "create:cogwheel"
    assert res[0]["source"] == "audit"


def test_audit_makes_ambiguous(cache_dir):
    """jar 齿轮→create:cogwheel; audit 齿轮→minecraft:cogwheel (diff id)."""
    _write_name_index(cache_dir, {"齿轮": "create:cogwheel"})
    _write_audit_index(cache_dir, [("minecraft:cogwheel", "齿轮")])
    res, _ = lookup_item.build_results(cache_dir.parent, ["齿轮"],
                                         cache_dir=cache_dir)
    assert res[0]["status"] == "ambiguous"
    assert {e["id"] for e in res[0]["ids"]} == {
        "create:cogwheel", "minecraft:cogwheel"}


def test_audit_same_id_keeps_unambiguous(cache_dir):
    """Both jar and audit give 齿轮→create:cogwheel (same id) → still found,
    source labelled audit (user-verified overrides jar on same id)."""
    _write_name_index(cache_dir, {"齿轮": "create:cogwheel"})
    _write_audit_index(cache_dir, [("create:cogwheel", "齿轮")])
    res, _ = lookup_item.build_results(cache_dir.parent, ["齿轮"],
                                         cache_dir=cache_dir)
    assert res[0]["status"] == "found"
    assert res[0]["source"] == "audit"


def test_not_found_returns_suggestions(cache_dir):
    _write_name_index(cache_dir, {"Iron Ingot": "minecraft:iron_ingot",
                                    "Iron Block": "minecraft:iron_block"})
    res, _ = lookup_item.build_results(cache_dir.parent, ["Nonsense"],
                                         cache_dir=cache_dir)
    assert res[0]["status"] == "not_found"
    assert isinstance(res[0]["suggestions"], list)


def test_partial_matches_substring(cache_dir):
    _write_name_index(cache_dir, {
        "Iron Ingot": "minecraft:iron_ingot",
        "Iron Block": "minecraft:iron_block",
        "Gold Ingot": "minecraft:gold_ingot",
    })
    res, _ = lookup_item.build_results(cache_dir.parent, ["Iron"],
                                         partial=True, cache_dir=cache_dir)
    assert res[0]["status"] == "partial"
    assert {m["name"] for m in res[0]["matches"]} == {
        "Iron Ingot", "Iron Block"}


def test_reverse_id_to_names(cache_dir):
    _write_name_index(cache_dir, {"Cogwheel": "create:cogwheel",
                                    "齿轮": "create:cogwheel"})
    res, _ = lookup_item.build_results(cache_dir.parent, ["create:cogwheel"],
                                         reverse=True, cache_dir=cache_dir)
    assert res[0]["status"] == "found"
    assert {n["name"] for n in res[0]["names"]} == {"Cogwheel", "齿轮"}


def test_reverse_not_found(cache_dir):
    _write_name_index(cache_dir, {"Cogwheel": "create:cogwheel"})
    res, _ = lookup_item.build_results(cache_dir.parent, ["minecraft:air"],
                                         reverse=True, cache_dir=cache_dir)
    assert res[0]["status"] == "not_found"


def test_missing_cache_returns_none(tmp_path: Path):
    cache_dir = tmp_path / ".ftbq-cache"  # never created
    res, _cd = lookup_item.build_results(tmp_path, ["Cogwheel"],
                                          cache_dir=cache_dir)
    assert res is None


def test_main_missing_cache_exit_2(tmp_path: Path, capsys):
    cache_dir = tmp_path / ".ftbq-cache"
    rc = lookup_item.main([str(tmp_path), "Cogwheel",
                            "--cache-dir", str(cache_dir)])
    assert rc == 2
    assert "extract_items" in capsys.readouterr().err


def test_main_json_output(tmp_path: Path, capsys):
    cache_dir = tmp_path / ".ftbq-cache"
    _write_name_index(cache_dir, {"Cogwheel": "create:cogwheel"})
    rc = lookup_item.main([str(tmp_path), "Cogwheel", "--json",
                            "--cache-dir", str(cache_dir)])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out[0]["id"] == "create:cogwheel"


def test_main_text_output(tmp_path: Path, capsys):
    cache_dir = tmp_path / ".ftbq-cache"
    _write_name_index(cache_dir, {"Cogwheel": "create:cogwheel"})
    rc = lookup_item.main([str(tmp_path), "Cogwheel",
                            "--cache-dir", str(cache_dir)])
    assert rc == 0
    assert "create:cogwheel" in capsys.readouterr().out
