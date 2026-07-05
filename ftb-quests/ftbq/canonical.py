"""Canonical JSON5 emitter — byte-stable output for the FTB Quests skill.

The generator and the manifest writer both must emit byte-identical files
on identical inputs (so re-running produces a no-op diff). Standard
``json.dumps`` doesn't quite fit:

* FTB Quests likes JSON5 (unquoted keys, trailing commas)
* coordinates are floats; we need a single deterministic format
  (``0.0`` not ``0``, ``1.5`` not ``1.50000001``)
* keys must be sorted, but per-object key order can be overridden
  (chapter files want ``id`` first, then ``filename``, etc.)
* lang files use string keys with dots — those stay quoted

Public API:

    dumps(value, *, indent=2, sort_keys=True, key_order=None,
          quote_keys=False) -> str
    dump_file(path, value, **kw) -> None
    canonical_json(value) -> str          stable JSON for hashing

A value here is plain Python (dict/list/str/int/float/bool/None) — Node
trees should be flattened with ``ftbq.json5.to_plain`` first.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Identifiers that don't need quoting as JSON5 keys.
_SAFE_KEY_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_$"
                      "0123456789")


def _is_bare_key(key: str) -> bool:
    if not key:
        return False
    if key[0].isdigit():
        return False
    return all(ch in _SAFE_KEY_CHARS for ch in key)


def _format_float(value: float) -> str:
    if value != value:  # NaN
        return "NaN"
    if value == float("inf"):
        return "Infinity"
    if value == float("-inf"):
        return "-Infinity"
    if value == int(value) and abs(value) < 1e16:
        return f"{value:.1f}"
    return repr(value)


def _format_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _format_key(key: str, *, quote_keys: bool) -> str:
    if quote_keys or not _is_bare_key(key):
        return _format_string(key)
    return key


def _ordered_items(d: dict, key_order: list[str] | None,
                   sort_keys: bool) -> list[tuple[str, Any]]:
    if key_order:
        prefix = [k for k in key_order if k in d]
        rest_keys = [k for k in d if k not in set(key_order)]
        if sort_keys:
            rest_keys.sort()
        return [(k, d[k]) for k in prefix + rest_keys]
    if sort_keys:
        return sorted(d.items())
    return list(d.items())


def dumps(value: Any, *, indent: int = 2, sort_keys: bool = True,
          key_order: list[str] | None = None,
          quote_keys: bool = False,
          per_path_key_order: dict[str, list[str]] | None = None,
          trailing_comma: bool = True,
          path: tuple[str, ...] = (),
          ) -> str:
    """Serialize ``value`` to a JSON5 string.

    ``per_path_key_order`` lets callers supply different orders at
    different positions in the tree. Keys are dotted paths; an entry
    ``"chapters[].quests[]"`` matches every quest under any chapter.
    """
    return _emit(value, indent=indent, level=0, sort_keys=sort_keys,
                  key_order=key_order, quote_keys=quote_keys,
                  per_path_key_order=per_path_key_order or {},
                  trailing_comma=trailing_comma, path=path)


def _emit(value: Any, *, indent: int, level: int, sort_keys: bool,
          key_order: list[str] | None, quote_keys: bool,
          per_path_key_order: dict[str, list[str]],
          trailing_comma: bool, path: tuple[str, ...]) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return _format_string(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return _format_float(value)
    if isinstance(value, list):
        if not value:
            return "[]"
        pad = " " * (indent * (level + 1))
        closer_pad = " " * (indent * level)
        new_path = path + ("[]",)
        lines = []
        for item in value:
            lines.append(pad + _emit(item, indent=indent, level=level + 1,
                                       sort_keys=sort_keys, key_order=None,
                                       quote_keys=quote_keys,
                                       per_path_key_order=per_path_key_order,
                                       trailing_comma=trailing_comma,
                                       path=new_path))
        joiner = ",\n"
        body = joiner.join(lines)
        tail = ",\n" if trailing_comma else "\n"
        return "[\n" + body + tail + closer_pad + "]"
    if isinstance(value, dict):
        if not value:
            return "{}"
        path_key = ".".join(path) if path else ""
        effective_order = per_path_key_order.get(path_key, key_order)
        items = _ordered_items(value, effective_order, sort_keys)
        pad = " " * (indent * (level + 1))
        closer_pad = " " * (indent * level)
        lines = []
        for k, v in items:
            new_path = path + (str(k),)
            child_order = per_path_key_order.get(".".join(new_path))
            ks = _format_key(k, quote_keys=quote_keys)
            vs = _emit(v, indent=indent, level=level + 1,
                        sort_keys=sort_keys, key_order=child_order,
                        quote_keys=quote_keys,
                        per_path_key_order=per_path_key_order,
                        trailing_comma=trailing_comma,
                        path=new_path)
            lines.append(f"{pad}{ks}: {vs}")
        joiner = ",\n"
        body = joiner.join(lines)
        tail = ",\n" if trailing_comma else "\n"
        return "{\n" + body + tail + closer_pad + "}"
    raise TypeError(f"cannot serialize {type(value).__name__}")


def dump_file(path: str | Path, value: Any, **kw: Any) -> None:
    Path(path).write_text(dumps(value, **kw) + "\n", encoding="utf-8")


def canonical_json(value: Any) -> str:
    """Stable, compact JSON for hashing. NOT pretty-printed."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False)
