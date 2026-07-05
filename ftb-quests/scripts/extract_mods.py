"""Extract mod metadata from a modpack's mods/ directory.

Walks ``<modpack>/mods/*.jar`` and parses each jar for a recognized mod
metadata file:

    META-INF/neoforge.mods.toml      NeoForge (MC 1.20.5+)
    META-INF/mods.toml                Forge / NeoForge legacy
    fabric.mod.json                   Fabric / Quilt
    mcmod.info                        legacy Forge (MC <=1.12)

Output: ``<output_dir>/.ftbq-cache/mods.json5`` with one entry per
parseable jar plus an ``unparseable`` list. Stdlib only.

Usage::

    python scripts/extract_mods.py <modpack_dir>
    python scripts/extract_mods.py <modpack_dir> --output <quests_dir>
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

# Allow running from anywhere — make the repo root importable.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq.canonical import dump_file  # noqa: E402

try:
    import tomllib  # 3.11+
except ImportError:  # pragma: no cover
    try:
        import tomli as tomllib  # type: ignore
    except ImportError:  # pragma: no cover
        tomllib = None  # type: ignore


SCHEMA_VERSION = 1


def _read_zip(zf: zipfile.ZipFile, name: str) -> bytes | None:
    try:
        return zf.read(name)
    except KeyError:
        return None


def _decode(data: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1")


def _normalize_side(value: Any, *, default: str = "both") -> str:
    if not value:
        return default
    s = str(value).lower()
    if s in ("client", "client_only"):
        return "client"
    if s in ("server", "dedicated_server"):
        return "server"
    if s in ("both", "common", "all", "*"):
        return "both"
    return default


def _normalize_mc_versions(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value]
    return [str(value)]


def parse_neoforge_toml(zf: zipfile.ZipFile) -> dict | None:
    """NeoForge (MC 1.20.5+) ships META-INF/neoforge.mods.toml."""
    raw = _read_zip(zf, "META-INF/neoforge.mods.toml")
    if raw is None:
        return None
    return _parse_forge_like_toml(raw, loader="neoforge")


def parse_forge_toml(zf: zipfile.ZipFile) -> dict | None:
    raw = _read_zip(zf, "META-INF/mods.toml")
    if raw is None:
        return None
    return _parse_forge_like_toml(raw, loader="forge")


def _parse_forge_like_toml(raw: bytes, *, loader: str) -> dict | None:
    if tomllib is None:
        raise RuntimeError(
            "TOML support unavailable — install Python 3.11+ or `pip install tomli`")
    data = tomllib.loads(_decode(raw))
    mods = data.get("mods") or []
    if not mods:
        return None
    mod = mods[0]
    modid = mod.get("modId") or mod.get("modid")
    if not modid:
        return None
    # Side comes from [[mods]].side or top-level dependency block; default "both".
    side = mod.get("side") or data.get("side")
    deps = data.get("dependencies", {})
    mc_versions: list[str] = []
    for dep in deps.get(modid, []) if isinstance(deps.get(modid), list) else []:
        if dep.get("modId") in ("minecraft", "neoforge", "forge"):
            mc_versions.append(str(dep.get("versionRange", "")))
    return {
        "modid": str(modid),
        "name": str(mod.get("displayName", modid)),
        "version": str(mod.get("version", "")),
        "description": (mod.get("description") or "").strip(),
        "side": _normalize_side(side),
        "mc_versions": mc_versions,
        "loader": loader,
    }


def parse_fabric_json(zf: zipfile.ZipFile) -> dict | None:
    raw = _read_zip(zf, "fabric.mod.json")
    if raw is None:
        return None
    try:
        data = json.loads(_decode(raw))
    except json.JSONDecodeError:
        return None
    modid = data.get("id")
    if not modid:
        return None
    deps = data.get("depends") or {}
    mc_versions = _normalize_mc_versions(deps.get("minecraft"))
    description = data.get("description")
    if isinstance(description, dict):
        description = description.get("default", "")
    env = data.get("environment", "*")
    name = data.get("name", modid)
    if isinstance(name, dict):
        name = name.get("en_us", modid)
    return {
        "modid": str(modid),
        "name": str(name),
        "version": str(data.get("version", "")),
        "description": (description or "").strip(),
        "side": _normalize_side(env),
        "mc_versions": mc_versions,
        "loader": "fabric",
    }


def parse_legacy_mcmod(zf: zipfile.ZipFile) -> dict | None:
    raw = _read_zip(zf, "mcmod.info")
    if raw is None:
        return None
    text = _decode(raw)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict) and "modList" in data:
        data = data["modList"]
    if not isinstance(data, list) or not data:
        return None
    entry = data[0]
    if not isinstance(entry, dict):
        return None
    modid = entry.get("modid") or entry.get("modId")
    if not modid:
        return None
    return {
        "modid": str(modid),
        "name": str(entry.get("name", modid)),
        "version": str(entry.get("version", "")),
        "description": (entry.get("description") or "").strip(),
        "side": "both",
        "mc_versions": _normalize_mc_versions(entry.get("mcversion")),
        "loader": "forge-legacy",
    }


_LOADERS = (parse_neoforge_toml, parse_forge_toml, parse_fabric_json,
            parse_legacy_mcmod)


def extract_one(jar_path: Path) -> dict | None:
    """Return a metadata dict or None if the jar is unrecognized."""
    try:
        with zipfile.ZipFile(jar_path) as zf:
            for loader in _LOADERS:
                try:
                    meta = loader(zf)
                except Exception:
                    continue
                if meta is not None:
                    return meta
    except (zipfile.BadZipFile, OSError):
        return None
    return None


def scan_directory(modpack_dir: Path) -> tuple[list[dict], list[dict]]:
    mods_dir = modpack_dir / "mods"
    if not mods_dir.is_dir():
        raise FileNotFoundError(f"mods/ directory not found under {modpack_dir}")
    parsed: list[dict] = []
    unparseable: list[dict] = []
    for jar in sorted(mods_dir.glob("*.jar")):
        rel = jar.relative_to(modpack_dir).as_posix()
        meta = extract_one(jar)
        if meta is None:
            reason = "no recognizable metadata file"
            try:
                with zipfile.ZipFile(jar):
                    pass
            except (zipfile.BadZipFile, OSError) as exc:
                reason = f"unreadable archive: {exc}"
            unparseable.append({"jar": rel, "reason": reason})
        else:
            meta["source_jar"] = rel
            parsed.append(meta)
    parsed.sort(key=lambda m: m["modid"])
    return parsed, unparseable


def build_cache(modpack_dir: Path) -> dict:
    parsed, unparseable = scan_directory(modpack_dir)
    return {
        "schema": SCHEMA_VERSION,
        "scanned_at": _dt.datetime.now(_dt.timezone.utc)
                          .isoformat(timespec="seconds")
                          .replace("+00:00", "Z"),
        "modpack_dir": modpack_dir.as_posix(),
        "count": len(parsed),
        "mods": parsed,
        "unparseable": unparseable,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract mod metadata into .ftbq-cache/mods.json5")
    parser.add_argument("modpack_dir", type=Path,
                        help="Path to the modpack root (the dir containing mods/)")
    parser.add_argument("--output", "-o", type=Path,
                        help="Quests output dir (default: "
                             "<modpack_dir>/config/ftbquests/quests)")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args(argv)

    modpack = args.modpack_dir.resolve()
    output = (args.output or
              modpack / "config" / "ftbquests" / "quests").resolve()
    cache_dir = output / ".ftbq-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache = build_cache(modpack)
    cache_path = cache_dir / "mods.json5"
    dump_file(cache_path, cache, key_order=["schema", "scanned_at",
                                              "modpack_dir", "count",
                                              "mods", "unparseable"],
               per_path_key_order={
                   "mods.[]": ["modid", "name", "version", "loader",
                                "side", "mc_versions", "description",
                                "source_jar"],
                   "unparseable.[]": ["jar", "reason"],
               })
    if not args.quiet:
        print(f"Scanned {cache['count']} mods → {cache_path}")
        if cache["unparseable"]:
            print(f"  ({len(cache['unparseable'])} jar(s) unparseable)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
