"""Audit index tests — build / freshness / diff / item-pattern extraction.

Covers ``ftbq/audit.py`` (the codegraph-style analyze→status→query core)
and the two thin CLIs (``scripts/audit_index.py``, ``scripts/audit_diff.py``).
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ftbq import audit as ftbq_audit  # noqa: E402

_spec_index = importlib.util.spec_from_file_location(
    "audit_index_cli", ROOT / "scripts" / "audit_index.py")
audit_index_cli = importlib.util.module_from_spec(_spec_index)
sys.modules["audit_index_cli"] = audit_index_cli
_spec_index.loader.exec_module(audit_index_cli)

_spec_diff = importlib.util.spec_from_file_location(
    "audit_diff_cli", ROOT / "scripts" / "audit_diff.py")
audit_diff_cli = importlib.util.module_from_spec(_spec_diff)
sys.modules["audit_diff_cli"] = audit_diff_cli
_spec_diff.loader.exec_module(audit_diff_cli)


# ----------------------------------------------------------- pack fixtures

def _make_json5_pack(quests_dir: Path, *, with_patterns: bool = True) -> None:
    """A minimal JSON5 pack: one chapter + one lang file with quest_desc."""
    quests_dir.mkdir(parents=True, exist_ok=True)
    (quests_dir / "data.json5").write_text(
        '{ default_reward_team: false }\n', encoding="utf-8")
    desc = ('["Collect &esmall_cogwheel小齿轮&r, then '
            '&egearbox齿轮箱&r. Also &ecopper_ingot铜锭&r."]'
            if with_patterns else '["Plain description."]')
    (quests_dir / "chapters").mkdir(exist_ok=True)
    (quests_dir / "chapters" / "getting_started.json5").write_text(
        '{\n'
        '  id: "1111111111111111",\n'
        '  filename: "getting_started",\n'
        '  default_quest_shape: "circle",\n'
        '  quests: [\n'
        '    { id: "2222222222222222", x: 0.0, y: 0.0, shape: "circle",\n'
        '      dependencies: [], tasks: [], rewards: [] },\n'
        '  ],\n'
        '}\n', encoding="utf-8")
    (quests_dir / "lang" / "en_us").mkdir(parents=True, exist_ok=True)
    (quests_dir / "lang" / "en_us" / "quests.json5").write_text(
        '{\n'
        f'  "quest.2222222222222222.quest_desc": {desc},\n'
        '}\n', encoding="utf-8")


def _make_snbt_pack(quests_dir: Path, *, with_patterns: bool = True) -> None:
    """A minimal 1.20.1 SNBT pack: one chapter with inline description."""
    quests_dir.mkdir(parents=True, exist_ok=True)
    (quests_dir / "data.snbt").write_text('{ default_reward_team: false }\n',
                                          encoding="utf-8")
    desc = ('&esmall_cogwheel小齿轮&r and &ekelp_gel海带凝胶&r'
            if with_patterns else 'Plain description.')
    (quests_dir / "chapters").mkdir(exist_ok=True)
    (quests_dir / "chapters" / "getting_started.snbt").write_text(
        '{\n'
        '	id: "1111111111111111"\n'
        '	filename: "getting_started"\n'
        '	quests: [\n'
        '		{\n'
        '			id: "2222222222222222"\n'
        f'			description: ["{desc}"]\n'
        '		}\n'
        '	]\n'
        '}\n', encoding="utf-8")


def _make_modpack(root: Path, *, fmt: str = "json5",
                  with_patterns: bool = True) -> Path:
    """Build a pack under <root>/config/ftbquests/quests/ (modpack-root
    layout, what the CLIs expect) and return that quests dir."""
    qd = root / "config" / "ftbquests" / "quests"
    if fmt == "snbt":
        _make_snbt_pack(qd, with_patterns=with_patterns)
    else:
        _make_json5_pack(qd, with_patterns=with_patterns)
    return qd


# ----------------------------------------------------------- build_audit_index

def test_build_json5_pack_index():
    d = Path(__file__).parent / "_audit_tmp_json5"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d)
        idx = ftbq_audit.build_audit_index(d)
        assert idx["format"] == "json5"
        assert idx["file_count"] == 3  # data + chapter + lang
        paths = {f["path"] for f in idx["files"]}
        assert "data.json5" in paths
        assert "chapters/getting_started.json5" in paths
        assert "lang/en_us/quests.json5" in paths
        # every file entry carries the fingerprint fields
        for f in idx["files"]:
            assert {"path", "sha256", "size", "mtime"} <= set(f)
        assert idx["pack_hash"].startswith("sha256:")
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_build_skips_ftbq_cache():
    d = Path(__file__).parent / "_audit_tmp_skip"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d)
        # drop a stray file inside .ftbq-cache/ — must NOT be indexed
        (d / ".ftbq-cache").mkdir(parents=True, exist_ok=True)
        (d / ".ftbq-cache" / "stray.json5").write_text("{}", encoding="utf-8")
        idx = ftbq_audit.build_audit_index(d)
        paths = {f["path"] for f in idx["files"]}
        assert not any("ftbq-cache" in p for p in paths)
        assert idx["file_count"] == 3
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_build_missing_dir_returns_empty():
    idx = ftbq_audit.build_audit_index(Path("__nonexistent_pack__"))
    assert idx["file_count"] == 0
    assert idx["files"] == []
    assert idx["quests"] == []


# --------------------------------------------------------------- freshness

def test_freshness_fresh_after_build():
    d = Path(__file__).parent / "_audit_tmp_fresh"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d)
        idx = ftbq_audit.build_audit_index(d)
        fresh, changed = ftbq_audit.check_freshness(d, idx)
        assert fresh
        assert changed == []
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_freshness_stale_on_edit():
    d = Path(__file__).parent / "_audit_tmp_stale"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d)
        idx = ftbq_audit.build_audit_index(d)
        # rewrite a chapter with different content + newer mtime
        time.sleep(0.01)
        (d / "chapters" / "getting_started.json5").write_text(
            '{ id: "1111111111111111", filename: "getting_started" }\n',
            encoding="utf-8")
        fresh, changed = ftbq_audit.check_freshness(d, idx)
        assert not fresh
        assert "chapters/getting_started.json5" in changed
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_freshness_stale_on_add_remove():
    d = Path(__file__).parent / "_audit_tmp_addrem"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d)
        idx = ftbq_audit.build_audit_index(d)
        # add a new chapter
        time.sleep(0.01)
        (d / "chapters" / "extra.json5").write_text("{}", encoding="utf-8")
        fresh, changed = ftbq_audit.check_freshness(d, idx)
        assert not fresh
        assert "chapters/extra.json5" in changed
        # now remove it
        (d / "chapters" / "extra.json5").unlink()
        fresh2, _ = ftbq_audit.check_freshness(d, idx)
        assert fresh2  # back to matching the original index
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_freshness_no_cache_is_stale():
    d = Path(__file__).parent / "_audit_tmp_nocache"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d)
        fresh, changed = ftbq_audit.check_freshness(d, None)
        assert not fresh
        assert changed == ["no cached index"]
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------------------ diff

def test_diff_identical_packs():
    a = Path(__file__).parent / "_audit_diff_a"
    b = Path(__file__).parent / "_audit_diff_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_json5_pack(a)
        _make_json5_pack(b)
        ia = ftbq_audit.build_audit_index(a)
        ib = ftbq_audit.build_audit_index(b)
        diff = ftbq_audit.diff_indexes(ia, ib)
        assert diff["identical"] is True
        assert diff["only_in_a"] == []
        assert diff["only_in_b"] == []
        assert diff["content_differs"] == []
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_diff_detects_content_change():
    a = Path(__file__).parent / "_audit_diff_c"
    b = Path(__file__).parent / "_audit_diff_d"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_json5_pack(a)
        _make_json5_pack(b)
        # diverge b's chapter content
        time.sleep(0.01)
        (b / "chapters" / "getting_started.json5").write_text(
            '{ id: "1111111111111111", filename: "DIFFERENT" }\n',
            encoding="utf-8")
        ia = ftbq_audit.build_audit_index(a)
        ib = ftbq_audit.build_audit_index(b)
        diff = ftbq_audit.diff_indexes(ia, ib)
        assert diff["identical"] is False
        assert any(d["path"] == "chapters/getting_started.json5"
                   for d in diff["content_differs"])
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_diff_detects_only_in_each():
    a = Path(__file__).parent / "_audit_diff_e"
    b = Path(__file__).parent / "_audit_diff_f"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_json5_pack(a)
        _make_json5_pack(b)
        (a / "chapters" / "only_a.json5").write_text("{}", encoding="utf-8")
        (b / "chapters" / "only_b.json5").write_text("{}", encoding="utf-8")
        ia = ftbq_audit.build_audit_index(a)
        ib = ftbq_audit.build_audit_index(b)
        diff = ftbq_audit.diff_indexes(ia, ib)
        assert diff["identical"] is False
        assert "chapters/only_a.json5" in diff["only_in_a"]
        assert "chapters/only_b.json5" in diff["only_in_b"]
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


# ----------------------------------------------------- item pattern extraction

def test_extract_item_patterns_basic():
    out = ftbq_audit._extract_item_patterns(
        "Collect &esmall_cogwheel小齿轮&r then &egearbox齿轮箱&r.")
    assert len(out) == 2
    assert out[0] == {"item_id": "small_cogwheel", "name": "小齿轮",
                      "raw": "&esmall_cogwheel小齿轮&r"}
    assert out[1]["item_id"] == "gearbox"
    assert out[1]["name"] == "齿轮箱"


def test_extract_item_patterns_section_sign():
    # §e / §r variant (the other Minecraft formatting-code style)
    out = ftbq_audit._extract_item_patterns("§ecopper_ingot铜锭§r done")
    assert len(out) == 1
    assert out[0]["item_id"] == "copper_ingot"
    assert out[0]["name"] == "铜锭"


def test_extract_item_patterns_namespace_id():
    out = ftbq_audit._extract_item_patterns("&ecreate:cogwheel齿轮&r")
    assert out[0]["item_id"] == "create:cogwheel"
    assert out[0]["name"] == "齿轮"


def test_extract_item_patterns_none_when_no_span():
    assert ftbq_audit._extract_item_patterns("plain text no codes") == []
    assert ftbq_audit._extract_item_patterns("&eredstone红石") == []  # no &r


def test_item_report_json5_pack():
    d = Path(__file__).parent / "_audit_report_json5"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d, with_patterns=True)
        idx = ftbq_audit.build_audit_index(d)
        report = ftbq_audit.item_report(idx)
        assert report["quest_count"] == 1
        assert report["pattern_count"] == 3
        q = report["quests"][0]
        assert q["id"] == "2222222222222222"
        assert q["chapter"] == "getting_started"
        ids = {p["item_id"] for p in q["item_patterns"]}
        assert ids == {"small_cogwheel", "gearbox", "copper_ingot"}
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_item_report_snbt_pack():
    d = Path(__file__).parent / "_audit_report_snbt"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_snbt_pack(d, with_patterns=True)
        idx = ftbq_audit.build_audit_index(d)
        assert idx["format"] == "snbt"
        report = ftbq_audit.item_report(idx)
        assert report["quest_count"] == 1
        assert report["pattern_count"] == 2
        ids = {p["item_id"]
               for p in report["quests"][0]["item_patterns"]}
        assert ids == {"small_cogwheel", "kelp_gel"}
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_item_report_empty_when_no_patterns():
    d = Path(__file__).parent / "_audit_report_empty"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d, with_patterns=False)
        idx = ftbq_audit.build_audit_index(d)
        report = ftbq_audit.item_report(idx)
        assert report["quest_count"] == 0
        assert report["pattern_count"] == 0
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------------- index io

def test_write_then_load_index_roundtrip():
    d = Path(__file__).parent / "_audit_io"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d)
        idx = ftbq_audit.build_audit_index(d)
        path = ftbq_audit.write_index(d, idx)
        assert path.exists()
        loaded = ftbq_audit.load_index(d)
        assert loaded is not None
        assert loaded["pack_hash"] == idx["pack_hash"]
        assert loaded["file_count"] == idx["file_count"]
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_load_index_missing_returns_none():
    assert ftbq_audit.load_index(Path("__no_such_dir__")) is None


# ------------------------------------------------------------- pack pair io

def test_pack_pair_save_load():
    dlc = Path(__file__).parent / "_audit_pair_dlc"
    target = Path(__file__).parent / "_audit_pair_tgt"
    import shutil
    for d in (dlc, target):
        if d.exists():
            shutil.rmtree(d)
    try:
        dlc.mkdir(parents=True)
        ftbq_audit.save_pack_pair(dlc, target)
        pair = ftbq_audit.load_pack_pair(dlc)
        assert pair is not None
        assert pair["dlc_quests_dir"] == dlc.as_posix()
        assert pair["target_quests_dir"] == target.as_posix()
    finally:
        shutil.rmtree(dlc, ignore_errors=True)
        shutil.rmtree(target, ignore_errors=True)


def test_load_pack_pair_missing_returns_none():
    assert ftbq_audit.load_pack_pair(Path("__no_dlc__")) is None


# --------------------------------------------------------------- CLIs

def test_cli_audit_index_build_then_status(capsys):
    root = Path(__file__).parent / "_audit_cli_build"
    if root.exists():
        import shutil
        shutil.rmtree(root)
    try:
        qd = _make_modpack(root)
        # build
        rc = audit_index_cli.main([str(root), "--quiet"])
        assert rc == 0
        assert ftbq_audit.load_index(qd) is not None
        # status: fresh (--status always prints its verdict)
        rc = audit_index_cli.main([str(root), "--status"])
        assert rc == 0  # fresh
        out = capsys.readouterr().out
        assert "fresh" in out
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)


def test_cli_audit_index_status_stale(capsys):
    root = Path(__file__).parent / "_audit_cli_stale"
    if root.exists():
        import shutil
        shutil.rmtree(root)
    try:
        qd = _make_modpack(root)
        audit_index_cli.main([str(root), "--quiet"])
        time.sleep(0.01)
        (qd / "chapters" / "getting_started.json5").write_text(
            '{ id: "1111111111111111", filename: "x" }\n', encoding="utf-8")
        rc = audit_index_cli.main([str(root), "--status"])
        assert rc == 1  # stale
        out = capsys.readouterr().out
        assert "stale" in out
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)


def test_cli_audit_diff_identical(capsys):
    a = Path(__file__).parent / "_audit_cli_diff_a"
    b = Path(__file__).parent / "_audit_cli_diff_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_modpack(a)
        _make_modpack(b)
        # pre-build indexes so the diff loads them fresh
        audit_index_cli.main([str(a), "--quiet"])
        audit_index_cli.main([str(b), "--quiet"])
        rc = audit_diff_cli.main([str(a), str(b), "--quiet"])
        assert rc == 0  # identical
        out = capsys.readouterr().out
        assert "IDENTICAL" in out
        assert "Task B" in out
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_cli_audit_diff_differs_nonzero(capsys):
    a = Path(__file__).parent / "_audit_cli_diff_c"
    b = Path(__file__).parent / "_audit_cli_diff_d"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        qa = _make_modpack(a)
        qb = _make_modpack(b)
        time.sleep(0.01)
        (qb / "chapters" / "getting_started.json5").write_text(
            '{ id: "1111111111111111", filename: "DIFF" }\n', encoding="utf-8")
        rc = audit_diff_cli.main([str(a), str(b), "--quiet"])
        assert rc == 1  # differs
        out = capsys.readouterr().out
        assert "DIFFERS" in out
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_cli_audit_diff_remember_then_no_args(capsys):
    a = Path(__file__).parent / "_audit_cli_remember_a"
    b = Path(__file__).parent / "_audit_cli_remember_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        qa = _make_modpack(a)
        _make_modpack(b)
        audit_index_cli.main([str(a), "--quiet"])
        audit_index_cli.main([str(b), "--quiet"])
        # remember: pass BOTH paths so the pair is saved, then diff
        rc = audit_diff_cli.main([str(a), str(b), "--remember", "--quiet"])
        assert rc == 0
        assert ftbq_audit.load_pack_pair(qa) is not None
        # now invoke with only the DLC arg (no target) — uses remembered
        rc = audit_diff_cli.main([str(a), "--quiet"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "IDENTICAL" in out
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_cli_audit_diff_json(capsys):
    a = Path(__file__).parent / "_audit_cli_json_a"
    b = Path(__file__).parent / "_audit_cli_json_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_modpack(a)
        _make_modpack(b)
        rc = audit_diff_cli.main([str(a), str(b), "--json", "--quiet"])
        assert rc == 0
        out = capsys.readouterr().out
        payload = json.loads(out)
        assert payload["source"].startswith("fresh")
        assert payload["task_a"]["identical"] is True
        assert payload["task_b"]["dlc"]["pattern_count"] == 3
        assert payload["dlc"]["chapter_count"] == 1
        assert payload["dlc"]["quest_count"] == 1
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


# --------------------------------------------------- persisted report / resume

def test_index_has_chapter_quest_counts():
    d = Path(__file__).parent / "_audit_counts"
    if d.exists():
        import shutil
        shutil.rmtree(d)
    try:
        _make_json5_pack(d)
        idx = ftbq_audit.build_audit_index(d)
        assert idx["chapter_count"] == 1
        assert idx["quest_count"] == 1
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def test_report_save_load_roundtrip():
    a = Path(__file__).parent / "_audit_rpt_a"
    b = Path(__file__).parent / "_audit_rpt_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_modpack(a)
        _make_modpack(b)
        ia = ftbq_audit.build_audit_index(a / "config" / "ftbquests" / "quests")
        ib = ftbq_audit.build_audit_index(b / "config" / "ftbquests" / "quests")
        diff = ftbq_audit.diff_indexes(ia, ib)
        rep = ftbq_audit.build_report(ia, ib, diff,
                                        ftbq_audit.item_report(ia),
                                        ftbq_audit.item_report(ib))
        qa = a / "config" / "ftbquests" / "quests"
        path = ftbq_audit.save_report(qa, rep)
        assert path.exists()
        loaded = ftbq_audit.load_report(qa)
        assert loaded is not None
        assert loaded["task_a"]["identical"] is True
        assert loaded["dlc"]["pack_hash"] == ia["pack_hash"]
        assert loaded["task_b"]["dlc"]["pattern_count"] == 3
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_report_fresh_true_then_false_after_edit():
    a = Path(__file__).parent / "_audit_fresh_a"
    b = Path(__file__).parent / "_audit_fresh_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        qa = _make_modpack(a)
        qb = _make_modpack(b)
        ia = ftbq_audit.build_audit_index(qa)
        ib = ftbq_audit.build_audit_index(qb)
        ftbq_audit.write_index(qa, ia)
        ftbq_audit.write_index(qb, ib)
        diff = ftbq_audit.diff_indexes(ia, ib)
        rep = ftbq_audit.build_report(ia, ib, diff,
                                        ftbq_audit.item_report(ia),
                                        ftbq_audit.item_report(ib))
        # fresh: nothing changed since the indexes were built
        df, _ = ftbq_audit.check_freshness(qa, ia)
        tf, _ = ftbq_audit.check_freshness(qb, ib)
        assert ftbq_audit.report_fresh(rep, ia, ib, df, tf) is True
        # edit a DLC file → its index goes stale → report no longer fresh
        time.sleep(0.01)
        (qa / "data.json5").write_text("{ changed: true }\n", encoding="utf-8")
        df2, _ = ftbq_audit.check_freshness(qa, ia)
        assert ftbq_audit.report_fresh(rep, ia, ib, df2, tf) is False
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_cli_audit_diff_resumes_when_fresh(capsys):
    a = Path(__file__).parent / "_audit_resume_a"
    b = Path(__file__).parent / "_audit_resume_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_modpack(a)
        _make_modpack(b)
        # first run: full audit, saves the report
        rc1 = audit_diff_cli.main([str(a), str(b), "--quiet"])
        assert rc1 == 0
        capsymod = capsys.readouterr()
        assert "fresh" in capsymod.out
        # second run: nothing changed → resume from the saved report
        rc2 = audit_diff_cli.main([str(a), str(b), "--quiet"])
        assert rc2 == 0
        out2 = capsys.readouterr().out
        assert "resumed" in out2
        assert "IDENTICAL" in out2
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_cli_audit_diff_re_audits_when_stale(capsys):
    a = Path(__file__).parent / "_audit_rstale_a"
    b = Path(__file__).parent / "_audit_rstale_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        qa = _make_modpack(a)
        _make_modpack(b)
        audit_diff_cli.main([str(a), str(b), "--quiet"])
        capsys.readouterr()
        # edit a DLC file → report goes stale → next run re-audits
        time.sleep(0.01)
        (qa / "data.json5").write_text("{ changed: true }\n", encoding="utf-8")
        rc = audit_diff_cli.main([str(a), str(b), "--quiet"])
        out = capsys.readouterr().out
        assert "fresh" in out            # re-audited, not resumed
        assert "resumed" not in out
        assert rc == 1                   # the packs now differ
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def test_cli_audit_diff_force_skips_resume(capsys):
    a = Path(__file__).parent / "_audit_force_a"
    b = Path(__file__).parent / "_audit_force_b"
    import shutil
    for d in (a, b):
        if d.exists():
            shutil.rmtree(d)
    try:
        _make_modpack(a)
        _make_modpack(b)
        audit_diff_cli.main([str(a), str(b), "--quiet"])  # saves report
        capsys.readouterr()
        # --force must skip resume and recompute, even though nothing changed
        rc = audit_diff_cli.main([str(a), str(b), "--force", "--quiet"])
        out = capsys.readouterr().out
        assert "fresh" in out
        assert "resumed" not in out
        assert rc == 0
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)
