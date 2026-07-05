"""Pytest config + fixtures shared across tests/."""

from __future__ import annotations

import io
import json
import sys
import zipfile
from pathlib import Path

import pytest

# Make the skill root importable so `import ftbq` works.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture
def tmp_quests_dir(tmp_path: Path) -> Path:
    d = tmp_path / "quests"
    d.mkdir()
    (d / "chapters").mkdir()
    return d


@pytest.fixture
def make_jar(tmp_path: Path):
    """Build a synthetic mod jar from a dict of {arcname: text}.

    Returns a callable used inside a test like::

        jar_path = make_jar("create.jar", {"META-INF/mods.toml": "..."})
    """
    counter = {"i": 0}

    def _make(name: str, files: dict[str, str | bytes]) -> Path:
        counter["i"] += 1
        path = tmp_path / f"{counter['i']:02d}_{name}"
        with zipfile.ZipFile(path, "w") as zf:
            for arcname, content in files.items():
                if isinstance(content, str):
                    content = content.encode("utf-8")
                zf.writestr(arcname, content)
        return path

    return _make
