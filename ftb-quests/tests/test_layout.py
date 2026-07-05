"""Layout determinism tests for ftb-quests generate_quests.auto_layout."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "generate_quests", ROOT / "scripts" / "generate_quests.py")
generate_quests = importlib.util.module_from_spec(_spec)
sys.modules["generate_quests"] = generate_quests
_spec.loader.exec_module(generate_quests)


def _quest(name: str, *, depends_on: list[str] = None) -> dict:
    return {"name": name, "depends_on": depends_on or []}


def test_linear_chain():
    """A → B → C must lay out at x = 0, 1.5, 3.0."""
    coords = generate_quests.auto_layout([
        _quest("a"),
        _quest("b", depends_on=["a"]),
        _quest("c", depends_on=["b"]),
    ])
    assert coords["a"] == (0.0, 0.0)
    assert coords["b"] == (1.5, 0.0)
    assert coords["c"] == (3.0, 0.0)


def test_fork():
    """A branches into B and C. Both at x=1.5, y offsets ±1.0."""
    coords = generate_quests.auto_layout([
        _quest("a"),
        _quest("b", depends_on=["a"]),
        _quest("c", depends_on=["a"]),
    ])
    assert coords["a"] == (0.0, 0.0)
    assert coords["b"][0] == 1.5
    assert coords["c"][0] == 1.5
    assert {coords["b"][1], coords["c"][1]} == {1.0, -1.0}


def test_diamond():
    """A → {B, C} → D. D should be at depth 2."""
    coords = generate_quests.auto_layout([
        _quest("a"),
        _quest("b", depends_on=["a"]),
        _quest("c", depends_on=["a"]),
        _quest("d", depends_on=["b", "c"]),
    ])
    assert coords["a"][0] == 0.0
    assert coords["b"][0] == 1.5
    assert coords["c"][0] == 1.5
    assert coords["d"][0] == 3.0


def test_layout_deterministic():
    """Two calls on the same input → exact same coordinates."""
    spec = [_quest("a"), _quest("b", depends_on=["a"]),
             _quest("c", depends_on=["a"]),
             _quest("d", depends_on=["a"])]
    a = generate_quests.auto_layout(spec)
    b = generate_quests.auto_layout(spec)
    assert a == b


def test_three_way_fork_distributed():
    """Three siblings at the same depth — y values should be distinct."""
    coords = generate_quests.auto_layout([
        _quest("root"),
        _quest("alpha", depends_on=["root"]),
        _quest("beta", depends_on=["root"]),
        _quest("gamma", depends_on=["root"]),
    ])
    ys = sorted(coords[n][1] for n in ("alpha", "beta", "gamma"))
    assert len(set(ys)) == 3  # all distinct


def test_independent_quests_at_same_depth():
    """Two roots (no deps) should both be at depth 0 — they share x=0
    but have distinct y values."""
    coords = generate_quests.auto_layout([_quest("a"), _quest("b")])
    assert coords["a"][0] == 0.0
    assert coords["b"][0] == 0.0
    assert coords["a"][1] != coords["b"][1]
