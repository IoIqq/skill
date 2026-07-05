"""Canonical SNBT emitter + parser — Minecraft 1.20.1 FTB Quests on-disk format.

FTB Quests for MC 1.20.1 (``FTBTeam/FTB-Quests`` branch ``1.20.1/main``) saves
quest data as SNBT via ``dev.ftb.mods.ftblibrary.snbt.SNBT``: ``data.snbt``,
``chapters/*.snbt``, ``reward_tables/*.snbt``, ``chapter_groups.snbt``. This
module is the SNBT counterpart to ``ftbq.canonical`` (the JSON5 emitter used
for the 1.21+ / ``main``-branch format). It shares canonical's path-tracking
+ per-path key-order contract, so the generator's ``*KEY_ORDER`` constants
apply unchanged — only the leaf syntax differs.

Verified against the Java source 2026-06-25:

* ``SNBT.writeLines`` / ``SNBTBuilder``: ``#`` (and ``//``) line comments,
  **TAB** indentation, **no commas** between members in multi-line form,
  ``{ k: v }`` / ``[ v ]`` containers, ``{ }`` / ``[ ]`` when empty.
* ``SNBTUtils.quoteAndEscape`` / ``isSimpleString``: double-quoted strings
  with only the six escapes (``\\" \\\\ \\t \\b \\n \\r \\f``); a key is
  unquoted when every char is in ``[A-Za-z0-9._-+\\u221E]``.
* Numbers carry Minecraft type suffixes via ``Tag.toString()``: long ``L``,
  double ``d``, float ``f``, byte ``b``, short ``s``, int bare. Which suffix
  a field needs is resolved here from the value's dotted path (the build step
  emits plain Python ints/floats and is format-neutral).
* ``id`` is a hex STRING (``putString("id", getCodeString())``); the top-bit
  mask in ``ftbq.ids`` stays required (``readID`` → ``parseCodeString`` →
  ``Long.parseLong(hex,16)`` throws for a leading digit 8-F).
* Text (``title`` / ``subtitle`` / ``description``) is INLINE; 1.20.1 has no
  lang files.

Public API:
    dumps_snbt(value, *, key_order=None, per_path_key_order=None) -> str
    dump_file_snbt(path, value, **kw) -> None
    parse_snbt(text, *, filename="<input>") -> Any
    parse_snbt_file(path) -> Any
    SnbtError
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ftbq.canonical import _format_float, _ordered_items

__all__ = [
    "SnbtError",
    "dumps_snbt",
    "dump_file_snbt",
    "parse_snbt",
    "parse_snbt_file",
]


class SnbtError(Exception):
    """Raised on an SNBT parse or emit error."""


# ------------------------------------------------------------------ quoting
# SNBTUtils.quoteAndEscape / isSimpleCharacter / isSimpleString.

_ESCAPES = {'"': '"', '\\': '\\', '\t': 't', '\b': 'b',
            '\n': 'n', '\r': 'r', '\f': 'f'}
_SIMPLE_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789._-+\u221e")  # \u221e == ∞, per isSimpleCharacter


def _is_simple(s: str) -> bool:
    return bool(s) and all(c in _SIMPLE_CHARS for c in s)


def _quote(s: str) -> str:
    out = ['"']
    for c in s:
        out.append('\\' + _ESCAPES[c] if c in _ESCAPES else c)
    out.append('"')
    return ''.join(out)


def _format_key(k: str) -> str:
    return k if _is_simple(k) else _quote(k)


# ------------------------------------------------------- per-field NBT types
# SNBT numbers need a type suffix chosen by field, not by Python type. The
# emitter resolves the NBT type from the value's dotted path (same scheme
# canonical uses: each list element adds ``[]``). Only non-default types are
# listed — anything not matched is an int (bare, no suffix); a Python float
# with no match is a double.
#
#   ItemTask.count  -> putLong -> ``N L``   (ItemReward.count is putInt, bare)
#   XPTask.value    -> putLong -> ``N L``   (ISingleLongValueTask family)
#   x/y/size/...    -> putDouble -> ``N.Nd``
#   empty_weight/weight -> putFloat -> ``N.Nf``
_SNBT_LONG_PATHS = {
    "quests.[].tasks.[].count",
    "quests.[].tasks.[].value",
}
_SNBT_DOUBLE_KEYS = {
    "x", "y", "size", "icon_scale",
    "width", "height", "rotation", "default_quest_size",
}
_SNBT_FLOAT_KEYS = {"empty_weight", "weight"}


def _nbt_type(path: tuple[str, ...]) -> str:
    """Return the NBT number type ('long'/'double'/'float'/'int') for a value
    at ``path`` (the path TO the value, so its last element is the field name
    for dict children)."""
    if not path or path[-1] == "[]":
        return "int"
    last = path[-1]
    if ".".join(path) in _SNBT_LONG_PATHS:
        return "long"
    if last in _SNBT_DOUBLE_KEYS:
        return "double"
    if last in _SNBT_FLOAT_KEYS:
        return "float"
    return "int"


def _format_number(value: Any, path: tuple[str, ...]) -> str:
    t = _nbt_type(path)
    if t == "long":
        return f"{int(value)}L"
    if t == "double":
        return _format_float(float(value)) + "d"
    if t == "float":
        return _format_float(float(value)) + "f"
    return str(int(value))


# ------------------------------------------------------------------- emitter

def dumps_snbt(value: Any, *, key_order: list[str] | None = None,
               per_path_key_order: dict[str, list[str]] | None = None) -> str:
    """Serialize ``value`` to an SNBT string (tab-indented, no commas).

    Same key-ordering contract as ``ftbq.canonical.dumps``: ``key_order`` is
    the head order for the root object; ``per_path_key_order`` overrides at
    dotted paths (``"quests.[]"``, ``"quests.[].tasks.[]"``, …). Keys are
    sorted after the head order.
    """
    return _emit(value, level=0, key_order=key_order,
                 per_path_key_order=per_path_key_order or {}, path=())


def _emit(value: Any, *, level: int, key_order: list[str] | None,
          per_path_key_order: dict[str, list[str]],
          path: tuple[str, ...]) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, str):
        return _quote(value)
    if isinstance(value, int):
        return _format_number(value, path)
    if isinstance(value, float):
        return _format_number(value, path)
    if isinstance(value, list):
        return _emit_list(value, level=level,
                          per_path_key_order=per_path_key_order, path=path)
    if isinstance(value, dict):
        return _emit_dict(value, level=level, key_order=key_order,
                          per_path_key_order=per_path_key_order, path=path)
    raise SnbtError(
        f"cannot emit {type(value).__name__} at {'.'.join(path) or '<root>'}")


def _emit_dict(value: dict, *, level: int, key_order: list[str] | None,
               per_path_key_order: dict[str, list[str]],
               path: tuple[str, ...]) -> str:
    if not value:
        return "{ }"
    path_key = ".".join(path) if path else ""
    effective_order = per_path_key_order.get(path_key, key_order)
    items = _ordered_items(value, effective_order, True)
    pad = "\t" * (level + 1)
    closer = "\t" * level
    lines = []
    for k, v in items:
        new_path = path + (str(k),)
        child_order = per_path_key_order.get(".".join(new_path))
        ks = _format_key(str(k))
        vs = _emit(v, level=level + 1, key_order=child_order,
                   per_path_key_order=per_path_key_order, path=new_path)
        lines.append(f"{pad}{ks}: {vs}")
    return "{\n" + "\n".join(lines) + "\n" + closer + "}"


def _emit_list(value: list, *, level: int,
               per_path_key_order: dict[str, list[str]],
               path: tuple[str, ...]) -> str:
    if not value:
        return "[ ]"
    new_path = path + ("[]",)
    # SNBT writes a single-element list inline (``[v]``); 2+ are multi-line
    # with no commas. Matches SNBT.appendCollection.
    if len(value) == 1:
        return "[" + _emit(value[0], level=level, key_order=None,
                           per_path_key_order=per_path_key_order,
                           path=new_path) + "]"
    pad = "\t" * (level + 1)
    closer = "\t" * level
    lines = []
    for item in value:
        lines.append(pad + _emit(item, level=level + 1, key_order=None,
                                 per_path_key_order=per_path_key_order,
                                 path=new_path))
    return "[\n" + "\n".join(lines) + "\n" + closer + "]"


def dump_file_snbt(path: str | Path, value: Any, **kw: Any) -> None:
    """Write ``value`` as SNBT to ``path`` (UTF-8, trailing newline)."""
    Path(path).write_text(dumps_snbt(value, **kw) + "\n", encoding="utf-8")


# -------------------------------------------------------------------- parser
# Port of FTB-Library ``SNBTParser`` (focused subset) to plain Python values.
# Handles everything FTB Quests emits: compounds, lists, quoted/unquoted
# strings, suffixed numbers, booleans, ``#`` / ``//`` line comments, optional
# commas/whitespace. Produces dict / list / str / int / float / bool / None.

_REVERSE = {'"': '"', '\\': '\\', 't': '\t', 'b': '\b',
            'n': '\n', 'r': '\r', 'f': '\f'}


def _try_int(s: str) -> int | None:
    try:
        return int(s)
    except (ValueError, TypeError):
        return None


def _try_float(s: str) -> float | None:
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _is_simple_char(c: str) -> bool:
    return c.isalpha() or c.isdigit() or c in "._-+\u221e"


def _get_number_type(s: str) -> str:
    """Port of SNBTUtils.getNumberType. Returns 'int'/'float'/'string'."""
    if not s:
        return "string"
    last = s[-1].lower()
    if last.isdigit() and _try_int(s) is not None:
        return "int"
    start = s[:-1]
    if last == "b" and _try_int(start) is not None:
        return "int"  # byte
    if last == "s" and _try_int(start) is not None:
        return "int"  # short
    if last == "l" and _try_int(start) is not None:
        return "int"  # long
    if last == "f" and _try_float(start) is not None:
        return "float"
    if last == "d" and _try_float(start) is not None:
        return "float"
    if _try_float(s) is not None:
        return "float"  # plain float-valued (e.g. "1.0") -> double
    return "string"


class _Parser:
    def __init__(self, text: str, filename: str):
        self.filename = filename
        # Whole comment lines (# or // after trim) are dropped, newlines kept
        # for position info — mirrors SNBTParser's constructor.
        buf: list[str] = []
        for line in text.splitlines():
            t = line.strip()
            if not (t.startswith("#") or t.startswith("//")):
                buf.append(line)
            buf.append("\n")
        self.buf = "".join(buf)
        if len(self.buf) < 2:
            raise SnbtError(f"{filename}: file must have at least two chars")
        self.pos = 0

    def _pos(self) -> str:
        row, col = 1, 1
        for ch in self.buf[:self.pos]:
            if ch == "\n":
                row += 1
                col = 1
            else:
                col += 1
        return f"{row}:{col}"

    def _next(self) -> str:
        if self.pos >= len(self.buf):
            raise SnbtError(f"{self.filename}: unexpected EOF")
        c = self.buf[self.pos]
        self.pos += 1
        return c

    def _next_ns(self) -> str:
        while True:
            c = self._next()
            if c > " ":  # skip whitespace (space, tab, CR, LF, ...)
                return c

    def read_tag(self, first: str) -> Any:
        if first == "{":
            return self._read_compound()
        if first == "[":
            return self._read_collection()
        if first == '"':
            return self._read_quoted('"')
        if first == "'":
            return self._read_quoted("'")
        s = self._read_word(first)
        return self._classify(s)

    def _read_word(self, first: str) -> str:
        sb = [first]
        while True:
            c = self._next()
            if _is_simple_char(c):
                sb.append(c)
            else:
                self.pos -= 1
                return "".join(sb)

    def _read_quoted(self, stop: str) -> str:
        sb: list[str] = []
        escape = False
        while True:
            c = self._next()
            if c == "\n":
                raise SnbtError(
                    f"{self.filename}: unterminated string @ {self._pos()}")
            if escape:
                escape = False
                # REVERSE_ESCAPE_CHARS: known escape -> real char; unknown
                # (e.g. \uXXXX, which FTB Quests never emits) -> literal.
                sb.append(_REVERSE.get(c, c))
            elif c == "\\":
                escape = True
            elif c == stop:
                return "".join(sb)
            else:
                sb.append(c)

    def _read_compound(self) -> dict:
        out: dict[str, Any] = {}
        while True:
            c = self._next_ns()
            if c == "}":
                return out
            if c == ",":
                continue
            if c == '"':
                key = self._read_quoted('"')
            elif c == "'":
                key = self._read_quoted("'")
            else:
                key = self._read_word(c)
            n = self._next_ns()
            if n not in (":", "="):
                raise SnbtError(
                    f"{self.filename}: expected ':' @ {self._pos()}, got {n!r}")
            out[key] = self.read_tag(self._next_ns())

    def _read_collection(self) -> Any:
        prev = self.pos
        n1 = self._next_ns()
        n2 = self._next_ns()
        if n2 == ";" and n1 in "ILBilb":
            return self._read_array(n1)
        self.pos = prev
        return self._read_list()

    def _read_list(self) -> list:
        out: list[Any] = []
        while True:
            c = self._next_ns()
            if c == "]":
                return out
            if c == ",":
                continue
            out.append(self.read_tag(c))

    def _read_array(self, type_: str) -> list:
        out: list[int] = []
        while True:
            c = self._next_ns()
            if c == "]":
                return out
            if c == ",":
                continue
            tag = self.read_tag(c)
            if isinstance(tag, bool) or not isinstance(tag, (int, float)):
                raise SnbtError(
                    f"{self.filename}: non-numeric entry in array @ {self._pos()}")
            out.append(int(tag))

    def _classify(self, s: str) -> Any:
        if s == "true":
            return True
        if s == "false":
            return False
        if s in ("null", "end", "END"):
            return None
        # Infinity / NaN tokens (the grammar accepts them; FTB Quests never
        # emits them, so fidelity to Java's exact-string list doesn't matter).
        if s in ("Infinity", "Infinityd", "+Infinity", "+Infinityd",
                 "\u221e", "\u221ed", "+\u221e", "+\u221ed",
                 "Infinityf", "+Infinityf", "\u221ef", "+\u221ef"):
            return float("inf")
        if s in ("-Infinity", "-Infinityd", "-\u221e", "-\u221ed",
                 "-Infinityf", "-\u221ef"):
            return float("-inf")
        if s in ("NaN", "NaNd", "NaNf"):
            return float("nan")
        t = _get_number_type(s)
        if t == "int":
            core = s[:-1] if s[-1] in "bBsSlL" else s  # drop byte/short/long suffix
            return int(core)
        if t == "float":
            core = s[:-1] if s[-1] in "dDfF" else s  # drop double/float suffix
            return float(core)
        return s


def parse_snbt(text: str, *, filename: str = "<input>") -> Any:
    """Parse SNBT ``text`` to plain Python (dict/list/str/int/float/bool/None)."""
    p = _Parser(text, filename)
    return p.read_tag(p._next_ns())


def parse_snbt_file(path: str | Path) -> Any:
    p = Path(path)
    return parse_snbt(p.read_text(encoding="utf-8-sig"), filename=str(p))
