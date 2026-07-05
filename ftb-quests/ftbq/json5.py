"""String-aware JSON5 lexer + parser with source-span tracking.

Why hand-rolled instead of a third-party json5 lib:

* zero-install constraint of this skill (stdlib only)
* every value needs a (line, col) span so the validator can emit
  ``chapters/start.json5:42:7: error: ...`` style diagnostics — most
  json5 libraries throw away span info after parsing
* the lexer must NOT eat ``//`` inside string literals (the bug in the
  old regex-based stripper)

Public API:

    parse(text, *, filename="<input>") -> Node          tree with spans
    parse_file(path) -> Node
    Node.value                                          plain Python value
    Node.span -> (filename, line, col, end_line, end_col)
    Token.kind, Token.value, Token.line, Token.col      single token
    Json5Error                                          parse error

Numbers with type suffixes (``0.0d``, ``1b``, ``42L``) are tokenized as a
NUMBER followed by a SUFFIX token so the validator can flag them with
exact line/col. The parser still produces a node so downstream code keeps
running.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class Json5Error(Exception):
    def __init__(self, message: str, filename: str, line: int, col: int) -> None:
        super().__init__(f"{filename}:{line}:{col}: {message}")
        self.filename = filename
        self.line = line
        self.col = col
        self.short_message = message


@dataclass
class Token:
    kind: str
    value: Any
    line: int
    col: int
    end_line: int
    end_col: int
    raw: str = ""


@dataclass
class Node:
    value: Any
    filename: str
    line: int
    col: int
    end_line: int
    end_col: int
    children: list["Node"] = field(default_factory=list)
    keys: list["Node"] = field(default_factory=list)

    @property
    def span(self) -> tuple[str, int, int, int, int]:
        return (self.filename, self.line, self.col, self.end_line, self.end_col)

    def get(self, key: str, default: Any = None) -> Any:
        if isinstance(self.value, dict):
            v = self.value.get(key, default)
            return v.value if isinstance(v, Node) else v
        return default

    def child(self, key: str) -> "Node | None":
        if isinstance(self.value, dict) and key in self.value:
            v = self.value[key]
            return v if isinstance(v, Node) else None
        return None

    def to_plain(self) -> Any:
        return _to_plain(self)


def _to_plain(node: "Node | Any") -> Any:
    if isinstance(node, Node):
        return _to_plain(node.value)
    if isinstance(node, dict):
        return {k: _to_plain(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_to_plain(v) for v in node]
    return node


_PUNCT = {"{": "LBRACE", "}": "RBRACE", "[": "LBRACK", "]": "RBRACK",
          ",": "COMMA", ":": "COLON"}

_IDENT_START = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_$")
_IDENT_REST = _IDENT_START | set("0123456789")
_NUMBER_SUFFIXES = set("dDfFlLbBsS")


class Lexer:
    """Produces a token stream with line/col on every token."""

    def __init__(self, text: str, filename: str = "<input>") -> None:
        self.text = text
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: list[Token] = []

    def _peek(self, offset: int = 0) -> str:
        i = self.pos + offset
        return self.text[i] if i < len(self.text) else ""

    def _advance(self, n: int = 1) -> str:
        chunk = self.text[self.pos:self.pos + n]
        for ch in chunk:
            if ch == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
        self.pos += n
        return chunk

    def _error(self, msg: str) -> Json5Error:
        return Json5Error(msg, self.filename, self.line, self.col)

    def lex(self) -> list[Token]:
        while self.pos < len(self.text):
            ch = self._peek()
            if ch in " \t\r\n":
                self._advance()
                continue
            if ch == "/" and self._peek(1) == "/":
                self._consume_line_comment()
                continue
            if ch == "/" and self._peek(1) == "*":
                self._consume_block_comment()
                continue
            if ch in _PUNCT:
                start_l, start_c = self.line, self.col
                self._advance()
                self.tokens.append(Token(_PUNCT[ch], ch, start_l, start_c,
                                          self.line, self.col, ch))
                continue
            if ch in ("'", '"'):
                self._consume_string(ch)
                continue
            if ch.isdigit() or (ch == "." and self._peek(1).isdigit()):
                self._consume_number()
                continue
            if ch in "+-":
                nxt = self._peek(1)
                if nxt.isdigit() or nxt == ".":
                    self._consume_number()
                    continue
                if nxt in _IDENT_START:
                    self._consume_signed_identifier(ch)
                    continue
                raise self._error(f"unexpected character {ch!r}")
            if ch in _IDENT_START:
                self._consume_identifier()
                continue
            raise self._error(f"unexpected character {ch!r}")
        self.tokens.append(Token("EOF", None, self.line, self.col,
                                  self.line, self.col, ""))
        return self.tokens

    def _consume_line_comment(self) -> None:
        while self.pos < len(self.text) and self._peek() != "\n":
            self._advance()

    def _consume_block_comment(self) -> None:
        start_l, start_c = self.line, self.col
        self._advance(2)  # /*
        while self.pos < len(self.text):
            if self._peek() == "*" and self._peek(1) == "/":
                self._advance(2)
                return
            self._advance()
        raise Json5Error("unterminated /* */ comment", self.filename, start_l, start_c)

    def _consume_string(self, quote: str) -> None:
        start_l, start_c = self.line, self.col
        self._advance()  # opening quote
        buf: list[str] = []
        while self.pos < len(self.text):
            ch = self._peek()
            if ch == quote:
                self._advance()
                self.tokens.append(Token("STRING", "".join(buf), start_l,
                                          start_c, self.line, self.col,
                                          quote + "".join(buf) + quote))
                return
            if ch == "\\":
                self._advance()
                esc = self._peek()
                self._advance()
                buf.append(self._decode_escape(esc, start_l, start_c))
                continue
            if ch == "\n":
                raise Json5Error("unterminated string literal",
                                 self.filename, start_l, start_c)
            buf.append(ch)
            self._advance()
        raise Json5Error("unterminated string literal",
                         self.filename, start_l, start_c)

    def _decode_escape(self, esc: str, sl: int, sc: int) -> str:
        simple = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "'": "'",
                  "\\": "\\", "/": "/", "b": "\b", "f": "\f", "0": "\0",
                  "\n": ""}
        if esc in simple:
            return simple[esc]
        if esc == "u":
            hex_chars = self.text[self.pos:self.pos + 4]
            if len(hex_chars) < 4 or not all(c in "0123456789abcdefABCDEF"
                                             for c in hex_chars):
                raise Json5Error("bad \\u escape", self.filename, sl, sc)
            self._advance(4)
            return chr(int(hex_chars, 16))
        return esc

    def _consume_number(self) -> None:
        start_l, start_c = self.line, self.col
        start = self.pos
        if self._peek() in "+-":
            self._advance()
        # Hex literal 0x...
        if self._peek() == "0" and self._peek(1) in "xX":
            self._advance(2)
            while self._peek().lower() in "0123456789abcdef":
                self._advance()
            raw = self.text[start:self.pos]
            value = int(raw, 16)
            self.tokens.append(Token("NUMBER", value, start_l, start_c,
                                      self.line, self.col, raw))
            self._maybe_emit_suffix()
            return
        while self._peek().isdigit():
            self._advance()
        if self._peek() == ".":
            self._advance()
            while self._peek().isdigit():
                self._advance()
        if self._peek() in "eE":
            self._advance()
            if self._peek() in "+-":
                self._advance()
            while self._peek().isdigit():
                self._advance()
        raw = self.text[start:self.pos]
        try:
            value: float | int = int(raw) if "." not in raw and "e" not in raw \
                                              and "E" not in raw else float(raw)
        except ValueError:
            raise Json5Error(f"invalid number {raw!r}", self.filename,
                             start_l, start_c)
        self.tokens.append(Token("NUMBER", value, start_l, start_c,
                                  self.line, self.col, raw))
        self._maybe_emit_suffix()

    def _maybe_emit_suffix(self) -> None:
        ch = self._peek()
        if ch and ch in _NUMBER_SUFFIXES:
            sl, sc = self.line, self.col
            self._advance()
            self.tokens.append(Token("SUFFIX", ch, sl, sc,
                                      self.line, self.col, ch))

    def _consume_signed_identifier(self, sign: str) -> None:
        """Handle ``-Infinity`` / ``+NaN`` etc. as a single NUMBER token."""
        start_l, start_c = self.line, self.col
        self._advance()  # consume sign
        ident_start = self.pos
        while self.pos < len(self.text) and self._peek() in _IDENT_REST:
            self._advance()
        ident = self.text[ident_start:self.pos]
        raw = sign + ident
        if ident == "Infinity":
            value = float("-inf") if sign == "-" else float("inf")
        elif ident == "NaN":
            value = float("nan")
        else:
            raise Json5Error(f"unexpected {raw!r}", self.filename,
                             start_l, start_c)
        self.tokens.append(Token("NUMBER", value, start_l, start_c,
                                  self.line, self.col, raw))

    def _consume_identifier(self) -> None:
        start_l, start_c = self.line, self.col
        start = self.pos
        while self.pos < len(self.text) and self._peek() in _IDENT_REST:
            self._advance()
        raw = self.text[start:self.pos]
        if raw == "true":
            self.tokens.append(Token("BOOL", True, start_l, start_c,
                                      self.line, self.col, raw))
        elif raw == "false":
            self.tokens.append(Token("BOOL", False, start_l, start_c,
                                      self.line, self.col, raw))
        elif raw == "null":
            self.tokens.append(Token("NULL", None, start_l, start_c,
                                      self.line, self.col, raw))
        elif raw == "Infinity":
            self.tokens.append(Token("NUMBER", float("inf"), start_l, start_c,
                                      self.line, self.col, raw))
        elif raw == "NaN":
            self.tokens.append(Token("NUMBER", float("nan"), start_l, start_c,
                                      self.line, self.col, raw))
        else:
            self.tokens.append(Token("IDENT", raw, start_l, start_c,
                                      self.line, self.col, raw))


class Parser:
    """Recursive-descent JSON5 parser. Produces a Node tree."""

    def __init__(self, tokens: list[Token], filename: str = "<input>",
                 *, suffix_tokens: list[Token] | None = None) -> None:
        self.tokens = tokens
        self.filename = filename
        self.pos = 0
        # Suffix tokens are NOT semantically consumed during parse — they
        # exist purely so the validator can flag E_TYPE_SUFFIX with exact
        # spans. We swallow them silently here.
        self.suffix_tokens = suffix_tokens if suffix_tokens is not None else []

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _eat(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        # absorb a SUFFIX token following any number
        while (self.pos < len(self.tokens)
               and self.tokens[self.pos].kind == "SUFFIX"):
            self.suffix_tokens.append(self.tokens[self.pos])
            self.pos += 1
        return tok

    def _expect(self, kind: str) -> Token:
        tok = self._peek()
        if tok.kind != kind:
            raise Json5Error(f"expected {kind} got {tok.kind} ({tok.raw!r})",
                             self.filename, tok.line, tok.col)
        return self._eat()

    def parse(self) -> Node:
        # leading SUFFIX tokens shouldn't occur, but be safe
        while self._peek().kind == "SUFFIX":
            self.suffix_tokens.append(self._eat())
        node = self._parse_value()
        eof = self._peek()
        if eof.kind != "EOF":
            raise Json5Error(f"trailing content {eof.raw!r}",
                             self.filename, eof.line, eof.col)
        return node

    def _parse_value(self) -> Node:
        tok = self._peek()
        if tok.kind == "LBRACE":
            return self._parse_object()
        if tok.kind == "LBRACK":
            return self._parse_array()
        if tok.kind in ("STRING", "NUMBER", "BOOL", "NULL"):
            self._eat()
            return Node(tok.value, self.filename, tok.line, tok.col,
                         tok.end_line, tok.end_col)
        raise Json5Error(f"unexpected {tok.kind} ({tok.raw!r})",
                         self.filename, tok.line, tok.col)

    def _parse_object(self) -> Node:
        opener = self._expect("LBRACE")
        pairs: dict[str, Node] = {}
        keys: list[Node] = []
        while self._peek().kind != "RBRACE":
            key_tok = self._peek()
            if key_tok.kind == "STRING":
                self._eat()
                key = key_tok.value
            elif key_tok.kind == "IDENT":
                self._eat()
                key = key_tok.value
            else:
                raise Json5Error(
                    f"expected object key, got {key_tok.kind}",
                    self.filename, key_tok.line, key_tok.col)
            self._expect("COLON")
            value = self._parse_value()
            pairs[key] = value
            keys.append(Node(key, self.filename, key_tok.line, key_tok.col,
                              key_tok.end_line, key_tok.end_col))
            if self._peek().kind == "COMMA":
                self._eat()
                continue
            break
        closer = self._expect("RBRACE")
        return Node(pairs, self.filename, opener.line, opener.col,
                     closer.end_line, closer.end_col, keys=keys)

    def _parse_array(self) -> Node:
        opener = self._expect("LBRACK")
        items: list[Node] = []
        while self._peek().kind != "RBRACK":
            items.append(self._parse_value())
            if self._peek().kind == "COMMA":
                self._eat()
                continue
            break
        closer = self._expect("RBRACK")
        return Node(items, self.filename, opener.line, opener.col,
                     closer.end_line, closer.end_col)


def parse(text: str, *, filename: str = "<input>") -> Node:
    lexer = Lexer(text, filename)
    tokens = lexer.lex()
    parser = Parser(tokens, filename)
    node = parser.parse()
    # Annotate node with any suffix tokens collected during parse, so
    # downstream validators can find them. Stored at the root only.
    setattr(node, "_suffix_tokens", parser.suffix_tokens)
    return node


def parse_file(path: str | Path) -> Node:
    p = Path(path)
    return parse(p.read_text(encoding="utf-8"), filename=str(p))


def to_plain(node: Node | Any) -> Any:
    return _to_plain(node)

