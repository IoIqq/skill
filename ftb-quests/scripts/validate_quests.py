"""Structured validator for FTB Quests configs.

Replaces the original 134-line regex-stripping script. Reuses
`ftbq.json5` for string-aware parsing with line/col tracking, so every
diagnostic carries an exact position.

Diagnostics are codes in the form ``E_*``. Severity is ``error`` or
``warning``. With ``--strict`` warnings count as errors (non-zero exit).
With ``--fix`` autofixable diagnostics are applied in-place to the
source files.

Usage::

    python scripts/validate_quests.py <quests_dir>
    python scripts/validate_quests.py <quests_dir> --json
    python scripts/validate_quests.py <quests_dir> --fix
    python scripts/validate_quests.py <quests_dir> --strict --manifest <path>
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq import ids as ftbq_ids  # noqa: E402
from ftbq.json5 import (Json5Error, Node, parse, parse_file,  # noqa: E402
                          to_plain)
from ftbq.snbt import SnbtError, parse_snbt_file  # noqa: E402


# ----------------------------------------------------------- diagnostics


SEVERITY_ERROR = "error"
SEVERITY_WARNING = "warning"


@dataclass
class Diagnostic:
    file: str
    line: int
    col: int
    severity: str
    code: str
    message: str
    hint: str | None = None
    autofix: dict | None = None

    def format_text(self) -> str:
        out = f"{self.file}:{self.line}:{self.col}: {self.severity}: {self.message}"
        if self.hint:
            out += f" {self.hint}"
        out += f" [{self.code}]"
        return out

    def to_json(self) -> dict:
        return {
            "file": self.file,
            "line": self.line,
            "col": self.col,
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "hint": self.hint,
        }


# ----------------------------------------------------------- file model


@dataclass
class ChapterFile:
    path: Path
    rel_path: str
    text: str
    root: Node
    plain: dict
    suffix_tokens: list


@dataclass
class BookModel:
    quests_dir: Path
    data_path: Path | None
    data: dict | None
    chapters: list[ChapterFile]
    reward_tables: list[ChapterFile]
    lang: dict[str, dict]
    manifest: dict | None
    parse_errors: list[Diagnostic] = field(default_factory=list)
    format: str = "json5"


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _wrap_snbt(value: Any, filename: str) -> Node:
    """Wrap a plain SNBT value (dict/list/scalar from ``parse_snbt``) in a
    Node tree so the Node-based checks work unchanged. SNBT positions aren't
    tracked, so every node sits at 1:1 — diagnostics still fire with the
    right code/severity/message, just without a precise line/col."""
    if isinstance(value, dict):
        return Node(value={k: _wrap_snbt(v, filename) for k, v in value.items()},
                    filename=filename, line=1, col=1, end_line=1, end_col=1)
    if isinstance(value, list):
        return Node(value=[_wrap_snbt(v, filename) for v in value],
                    filename=filename, line=1, col=1, end_line=1, end_col=1)
    return Node(value=value, filename=filename, line=1, col=1,
                end_line=1, end_col=1)


def _load_dir(quests_dir: Path, subdir: str,
                parse_errors: list[Diagnostic], *,
                fmt: str = "json5") -> list[ChapterFile]:
    """Load every ``<subdir>/*.json5`` (or ``*.snbt`` for the 1.20.1 format)
    as a parsed ChapterFile (the holder is generic enough for both chapter
    files and reward-table files). Parse errors are appended to
    ``parse_errors`` rather than aborting the load."""
    out: list[ChapterFile] = []
    d = quests_dir / subdir
    if not d.is_dir():
        return out
    ext = "snbt" if fmt == "snbt" else "json5"
    for path in sorted(d.glob(f"*.{ext}")):
        text = path.read_text(encoding="utf-8")
        if fmt == "snbt":
            try:
                plain = parse_snbt_file(path)
            except SnbtError as exc:
                parse_errors.append(Diagnostic(
                    file=_rel(path, quests_dir), line=1, col=1,
                    severity=SEVERITY_ERROR, code="E_PARSE",
                    message=str(exc)))
                continue
            root = _wrap_snbt(plain, str(path))
            out.append(ChapterFile(
                path=path, rel_path=_rel(path, quests_dir),
                text=text, root=root, plain=plain, suffix_tokens=[]))
            continue
        try:
            root = parse(text, filename=str(path))
        except Json5Error as exc:
            parse_errors.append(Diagnostic(
                file=_rel(path, quests_dir),
                line=exc.line, col=exc.col,
                severity=SEVERITY_ERROR, code="E_PARSE",
                message=exc.short_message))
            continue
        plain = to_plain(root)
        out.append(ChapterFile(
            path=path, rel_path=_rel(path, quests_dir),
            text=text, root=root, plain=plain,
            suffix_tokens=getattr(root, "_suffix_tokens", [])))
    return out


def _detect_format(quests_dir: Path) -> str:
    """Detect the on-disk format: SNBT if ``data.snbt`` or any ``.snbt``
    chapter/table exists, else JSON5."""
    if (quests_dir / "data.snbt").exists():
        return "snbt"
    for sub in ("chapters", "reward_tables"):
        d = quests_dir / sub
        if d.is_dir() and any(d.glob("*.snbt")):
            return "snbt"
    return "json5"


def load_book(quests_dir: Path, *,
                manifest_path: Path | None = None) -> BookModel:
    parse_errors: list[Diagnostic] = []
    fmt = _detect_format(quests_dir)
    ext = "snbt" if fmt == "snbt" else "json5"

    data_path = quests_dir / f"data.{ext}"
    data: dict | None = None
    if data_path.exists():
        try:
            if fmt == "snbt":
                data = parse_snbt_file(data_path)
            else:
                data = to_plain(parse_file(data_path))
        except (Json5Error, SnbtError) as exc:
            parse_errors.append(Diagnostic(
                file=_rel(data_path, quests_dir),
                line=getattr(exc, "line", 1), col=getattr(exc, "col", 1),
                severity=SEVERITY_ERROR, code="E_PARSE",
                message=getattr(exc, "short_message", str(exc))))

    chapters = _load_dir(quests_dir, "chapters", parse_errors, fmt=fmt)
    reward_tables = _load_dir(quests_dir, "reward_tables", parse_errors, fmt=fmt)

    lang: dict[str, dict] = {}
    lang_root = quests_dir / "lang"
    if lang_root.is_dir():
        for locale_dir in sorted(p for p in lang_root.iterdir() if p.is_dir()):
            lang_file = locale_dir / "quests.json5"
            if not lang_file.exists():
                continue
            try:
                lang[locale_dir.name] = to_plain(parse_file(lang_file))
            except Json5Error as exc:
                parse_errors.append(Diagnostic(
                    file=_rel(lang_file, quests_dir),
                    line=exc.line, col=exc.col,
                    severity=SEVERITY_ERROR, code="E_PARSE",
                    message=exc.short_message))

    manifest: dict | None = None
    if manifest_path is None:
        manifest_path = quests_dir / ".ftbq-cache" / "manifest.json5"
    if manifest_path.exists():
        try:
            manifest = to_plain(parse_file(manifest_path))
        except Json5Error as exc:
            parse_errors.append(Diagnostic(
                file=_rel(manifest_path, quests_dir),
                line=exc.line, col=exc.col,
                severity=SEVERITY_ERROR, code="E_PARSE",
                message=exc.short_message))

    return BookModel(quests_dir=quests_dir, data_path=data_path,
                      data=data, chapters=chapters, reward_tables=reward_tables,
                      lang=lang, manifest=manifest, parse_errors=parse_errors,
                      format=fmt)


HEX_RE = re.compile(r"^[0-9A-F]{16}$")


# ----------------------------------------------------------- validator


class Validator:
    def __init__(self, book: BookModel) -> None:
        self.book = book
        self.diagnostics: list[Diagnostic] = list(book.parse_errors)
        self.all_ids: dict[str, tuple[str, str, tuple[int, int]]] = {}
        # Decimal long values of reward-table ids, for `table_id` ref checks.
        self._table_longs: set[int] = set()

    def run(self) -> list[Diagnostic]:
        data_name = "data.snbt" if self.book.format == "snbt" else "data.json5"
        if not self.book.data_path or not self.book.data_path.exists():
            self.diagnostics.append(Diagnostic(
                file=data_name, line=1, col=1,
                severity=SEVERITY_ERROR, code="E_FILE_MISSING",
                message=f"{data_name} is missing"))
        if not (self.book.quests_dir / "chapters").is_dir():
            self.diagnostics.append(Diagnostic(
                file="chapters/", line=1, col=1,
                severity=SEVERITY_ERROR, code="E_DIR_MISSING",
                message="chapters/ directory is missing"))

        is_snbt = self.book.format == "snbt"
        for ch in self.book.chapters:
            self._check_chapter_file_fields(ch)
            self._check_filename_match(ch)
            self._index_ids(ch)
            self._check_id_formats(ch)
            if not is_snbt:
                # Inline text is expected (required) in SNBT; only the modern
                # JSON5 format ignores it.
                self._check_inline_text(ch)
            self._check_coord_dups(ch)
            self._check_bare_string_items(ch)
            if not is_snbt:
                # Type suffixes (1b, 0.0d, …) are legal SNBT, illegal JSON5.
                self._check_type_suffixes(ch)
        self._check_reward_tables()
        self._check_dependencies()
        self._check_table_id_references()
        self._check_lang_consistency()
        if self.book.manifest is not None:
            self._check_manifest_consistency()
        return self.diagnostics

    def _add(self, diag: Diagnostic) -> None:
        self.diagnostics.append(diag)

    def _iter_list_nodes(self, parent: Node, key: str):
        if not isinstance(parent.value, dict):
            return
        child = parent.value.get(key)
        if not isinstance(child, Node) or not isinstance(child.value, list):
            return
        for item in child.value:
            if isinstance(item, Node) and isinstance(item.value, dict):
                yield item

    def _scalar(self, node: Node, key: str) -> Any:
        if not isinstance(node.value, dict):
            return None
        child = node.value.get(key)
        if isinstance(child, Node):
            return child.value
        return child

    def _check_chapter_file_fields(self, ch: ChapterFile) -> None:
        for required in ("filename", "default_quest_shape"):
            if required not in (ch.plain or {}):
                self._add(Diagnostic(
                    file=ch.rel_path, line=ch.root.line, col=ch.root.col,
                    severity=SEVERITY_ERROR, code="E_FILE_FIELD_MISSING",
                    message=f"chapter missing required field {required!r}"))

    def _check_filename_match(self, ch: ChapterFile) -> None:
        declared = ch.plain.get("filename") if isinstance(ch.plain, dict) else None
        actual = ch.path.stem
        if declared and declared != actual:
            field_node = ch.root.child("filename")
            line = field_node.line if field_node else ch.root.line
            col = field_node.col if field_node else ch.root.col
            self._add(Diagnostic(
                file=ch.rel_path, line=line, col=col,
                severity=SEVERITY_ERROR, code="E_FILENAME_MISMATCH",
                message=f"filename {declared!r} differs from file stem {actual!r}",
                hint=f"rename file or change field to {actual!r}",
                autofix={"kind": "filename", "replacement": actual,
                         "field_node": field_node}))

    def _index_ids(self, ch: ChapterFile) -> None:
        if not isinstance(ch.plain, dict):
            return
        cid = ch.plain.get("id")
        if cid:
            self._record_id(cid, ch.rel_path, "chapter", ch.root.child("id"))
        for q_node in self._iter_list_nodes(ch.root, "quests"):
            qid = self._scalar(q_node, "id")
            if qid:
                self._record_id(qid, ch.rel_path, "quest", q_node.child("id"))
            for t_node in self._iter_list_nodes(q_node, "tasks"):
                tid = self._scalar(t_node, "id")
                if tid:
                    self._record_id(tid, ch.rel_path, "task",
                                      t_node.child("id"))
            for r_node in self._iter_list_nodes(q_node, "rewards"):
                rid = self._scalar(r_node, "id")
                if rid:
                    self._record_id(rid, ch.rel_path, "reward",
                                      r_node.child("id"))

    def _record_id(self, qid: str, file: str, kind: str,
                    id_node: Node | None) -> None:
        line = id_node.line if id_node else 1
        col = id_node.col if id_node else 1
        if qid in self.all_ids:
            self._add(Diagnostic(
                file=file, line=line, col=col,
                severity=SEVERITY_ERROR, code="E_ID_DUP",
                message=f"id {qid} is also used at {self.all_ids[qid][0]}"))
        else:
            self.all_ids[qid] = (file, kind, (line, col))

    def _check_id_formats(self, ch: ChapterFile) -> None:
        seen: list[tuple[Any, Node | None, str]] = []
        if isinstance(ch.plain, dict):
            seen.append((ch.plain.get("id"), ch.root.child("id"), "chapter"))
        for q_node in self._iter_list_nodes(ch.root, "quests"):
            seen.append((self._scalar(q_node, "id"), q_node.child("id"),
                          "quest"))
            for t_node in self._iter_list_nodes(q_node, "tasks"):
                seen.append((self._scalar(t_node, "id"),
                              t_node.child("id"), "task"))
            for r_node in self._iter_list_nodes(q_node, "rewards"):
                seen.append((self._scalar(r_node, "id"),
                              r_node.child("id"), "reward"))
        for qid, node, kind in seen:
            if qid is None:
                self._add(Diagnostic(
                    file=ch.rel_path,
                    line=node.line if node else ch.root.line,
                    col=node.col if node else ch.root.col,
                    severity=SEVERITY_ERROR, code="E_ID_MISSING",
                    message=f"{kind} missing required 'id' field"))
                continue
            if not isinstance(qid, str) or not HEX_RE.match(qid):
                self._add(Diagnostic(
                    file=ch.rel_path,
                    line=node.line if node else ch.root.line,
                    col=node.col if node else ch.root.col,
                    severity=SEVERITY_ERROR, code="E_ID_FORMAT",
                    message=f"id {qid!r} is not a 16-char uppercase hex"))

    def _check_inline_text(self, ch: ChapterFile) -> None:
        # Chapter-level inline text is also ignored by modern FTB Quests.
        if isinstance(ch.root.value, dict):
            for offending_field in ("title", "subtitle"):
                if offending_field in ch.root.value:
                    field_node = ch.root.value[offending_field]
                    line = field_node.line if isinstance(field_node, Node) else ch.root.line
                    col = field_node.col if isinstance(field_node, Node) else ch.root.col
                    self._add(Diagnostic(
                        file=ch.rel_path, line=line, col=col,
                        severity=SEVERITY_WARNING,
                        code="E_INLINE_TEXT_MODERN",
                        message=f"inline {offending_field!r} on chapter is "
                                 f"ignored by modern FTB Quests",
                        hint="move text to lang/<locale>/quests.json5"))
        for q_node in self._iter_list_nodes(ch.root, "quests"):
            for offending_field in ("title", "description", "subtitle"):
                if (isinstance(q_node.value, dict)
                        and offending_field in q_node.value):
                    field_node = q_node.value[offending_field]
                    line = field_node.line if isinstance(field_node, Node) else q_node.line
                    col = field_node.col if isinstance(field_node, Node) else q_node.col
                    self._add(Diagnostic(
                        file=ch.rel_path, line=line, col=col,
                        severity=SEVERITY_WARNING,
                        code="E_INLINE_TEXT_MODERN",
                        message=f"inline {offending_field!r} on quest is "
                                 f"ignored by modern FTB Quests",
                        hint="move text to lang/<locale>/quests.json5"))

    def _check_coord_dups(self, ch: ChapterFile) -> None:
        seen: dict[tuple[float, float], str] = {}
        for q_node in self._iter_list_nodes(ch.root, "quests"):
            x = self._scalar(q_node, "x")
            y = self._scalar(q_node, "y")
            qid = self._scalar(q_node, "id") or "?"
            if x is None or y is None:
                continue
            key = (float(x), float(y))
            if key in seen:
                self._add(Diagnostic(
                    file=ch.rel_path, line=q_node.line, col=q_node.col,
                    severity=SEVERITY_WARNING, code="E_COORD_DUP",
                    message=f"quest {qid} shares ({x}, {y}) with {seen[key]}"))
            else:
                seen[key] = qid

    def _check_bare_string_items(self, ch: ChapterFile) -> None:
        for q_node in self._iter_list_nodes(ch.root, "quests"):
            for t_node in self._iter_list_nodes(q_node, "tasks"):
                self._maybe_flag_bare_item(ch, t_node, container="task")
            for r_node in self._iter_list_nodes(q_node, "rewards"):
                self._maybe_flag_bare_item(ch, r_node, container="reward")

    def _maybe_flag_bare_item(self, ch: ChapterFile, parent: Node,
                                *, container: str) -> None:
        if not isinstance(parent.value, dict):
            return
        item = parent.value.get("item")
        if not isinstance(item, Node):
            return
        if isinstance(item.value, str):
            self._add(Diagnostic(
                file=ch.rel_path, line=item.line, col=item.col,
                severity=SEVERITY_ERROR, code="E_ITEM_BARE_STRING",
                message=f"bare-string item {item.value!r} on {container}; "
                         f"FTB Quests drops this on load",
                hint=f"replace with: {{ id: {item.value!r}, count: 1 }}",
                autofix={"kind": "item_object", "node": item}))

    def _check_type_suffixes(self, ch: ChapterFile) -> None:
        for tok in ch.suffix_tokens:
            self._add(Diagnostic(
                file=ch.rel_path, line=tok.line, col=tok.col,
                severity=SEVERITY_ERROR, code="E_TYPE_SUFFIX",
                message=f"type suffix {tok.value!r} is not valid in JSON5",
                hint=f"remove the trailing {tok.value!r}",
                autofix={"kind": "drop_suffix", "token": tok}))

    def _check_reward_tables(self) -> None:
        """Index reward-table ids + entry ids (for dup detection and
        ``table_id`` ref checks) and validate their formats."""
        for rt in self.book.reward_tables:
            if not isinstance(rt.plain, dict):
                continue
            tid = rt.plain.get("id")
            id_node = rt.root.child("id") if isinstance(rt.root.value, dict) else None
            if tid is None:
                self._add(Diagnostic(
                    file=rt.rel_path,
                    line=id_node.line if id_node else rt.root.line,
                    col=id_node.col if id_node else rt.root.col,
                    severity=SEVERITY_ERROR, code="E_ID_MISSING",
                    message="reward table missing 'id'"))
            elif not isinstance(tid, str) or not HEX_RE.match(tid):
                self._add(Diagnostic(
                    file=rt.rel_path,
                    line=id_node.line if id_node else rt.root.line,
                    col=id_node.col if id_node else rt.root.col,
                    severity=SEVERITY_ERROR, code="E_ID_FORMAT",
                    message=f"reward table id {tid!r} is not 16-char uppercase hex"))
            else:
                self._record_id(tid, rt.rel_path, "reward_table", id_node)
                try:
                    self._table_longs.add(int(tid, 16))
                except ValueError:
                    pass
            for r_node in self._iter_list_nodes(rt.root, "rewards"):
                rid = self._scalar(r_node, "id")
                rid_node = r_node.child("id")
                if rid is None:
                    self._add(Diagnostic(
                        file=rt.rel_path,
                        line=rid_node.line if rid_node else r_node.line,
                        col=rid_node.col if rid_node else r_node.col,
                        severity=SEVERITY_ERROR, code="E_ID_MISSING",
                        message="reward table entry missing 'id'"))
                    continue
                if not isinstance(rid, str) or not HEX_RE.match(rid):
                    self._add(Diagnostic(
                        file=rt.rel_path,
                        line=rid_node.line if rid_node else r_node.line,
                        col=rid_node.col if rid_node else r_node.col,
                        severity=SEVERITY_ERROR, code="E_ID_FORMAT",
                        message=f"reward table entry id {rid!r} is not 16-char uppercase hex"))
                else:
                    self._record_id(rid, rt.rel_path, "reward", rid_node)

    def _check_table_id_references(self) -> None:
        """Every ``table_id`` (numeric long) on a loot/random/choice/
        all_table reward should match a reward table in this book. A
        mismatch is a warning — it may be an external table the skill did
        not generate."""
        for ch in self.book.chapters:
            for q_node in self._iter_list_nodes(ch.root, "quests"):
                for r_node in self._iter_list_nodes(q_node, "rewards"):
                    if not isinstance(r_node.value, dict):
                        continue
                    tid_node = r_node.value.get("table_id")
                    if not isinstance(tid_node, Node):
                        continue
                    tid_val = tid_node.value
                    if tid_val is None:
                        continue
                    try:
                        long_val = int(tid_val)
                    except (TypeError, ValueError):
                        continue
                    if long_val not in self._table_longs:
                        self._add(Diagnostic(
                            file=ch.rel_path, line=tid_node.line,
                            col=tid_node.col, severity=SEVERITY_WARNING,
                            code="E_TABLE_MISSING",
                            message=f"table_id {tid_val} does not match any "
                                     f"reward table in this book",
                            hint="may reference an external table"))

    def _check_dependencies(self) -> None:
        for ch in self.book.chapters:
            for q_node in self._iter_list_nodes(ch.root, "quests"):
                deps_node = (q_node.value.get("dependencies")
                              if isinstance(q_node.value, dict) else None)
                if not isinstance(deps_node, Node):
                    continue
                if not isinstance(deps_node.value, list):
                    continue
                for dep_item in deps_node.value:
                    if not isinstance(dep_item, Node):
                        continue
                    target = dep_item.value
                    if not isinstance(target, str):
                        continue
                    if target not in self.all_ids:
                        suggestion = difflib.get_close_matches(
                            target, list(self.all_ids), n=1, cutoff=0.7)
                        hint = (f"Did you mean {suggestion[0]!r}?"
                                if suggestion else None)
                        self._add(Diagnostic(
                            file=ch.rel_path,
                            line=dep_item.line, col=dep_item.col,
                            severity=SEVERITY_ERROR, code="E_DEP_MISSING",
                            message=f"dependency {target!r} not found",
                            hint=hint))
        graph: dict[str, list[str]] = {}
        for ch in self.book.chapters:
            for q in (ch.plain.get("quests") or []):
                qid = q.get("id")
                if not qid:
                    continue
                graph[qid] = [d for d in (q.get("dependencies") or [])
                                if isinstance(d, str) and d in self.all_ids]
        for qid in list(graph):
            cycle = self._find_cycle(qid, graph, set(), [])
            if cycle:
                self._add(Diagnostic(
                    file=self.all_ids[qid][0],
                    line=self.all_ids[qid][2][0],
                    col=self.all_ids[qid][2][1],
                    severity=SEVERITY_ERROR, code="E_DEP_CYCLE",
                    message=f"dependency cycle: {' -> '.join(cycle)}"))
                break

    def _find_cycle(self, node: str, graph: dict[str, list[str]],
                      visited: set, stack: list) -> list | None:
        if node in stack:
            i = stack.index(node)
            return stack[i:] + [node]
        if node in visited:
            return None
        visited.add(node)
        stack.append(node)
        for n in graph.get(node, []):
            cycle = self._find_cycle(n, graph, visited, stack)
            if cycle:
                return cycle
        stack.pop()
        return None

    def _check_lang_consistency(self) -> None:
        for locale, entries in self.book.lang.items():
            for key in entries:
                m = re.match(r"^(chapter|quest)\.([0-9A-F]{16})\.\w+$", key)
                if not m:
                    continue
                ref_id = m.group(2)
                if ref_id not in self.all_ids:
                    self._add(Diagnostic(
                        file=f"lang/{locale}/quests.json5", line=1, col=1,
                        severity=SEVERITY_WARNING, code="E_LANG_ORPHAN",
                        message=f"lang key {key!r} references unknown id"))
        if self.book.lang:
            primary_locale = next(iter(self.book.lang))
            primary = self.book.lang[primary_locale]
            for qid, (file, kind, _) in self.all_ids.items():
                if kind not in ("chapter", "quest"):
                    continue
                key = f"{kind}.{qid}.title"
                if key not in primary:
                    self._add(Diagnostic(
                        file=file, line=1, col=1,
                        severity=SEVERITY_WARNING,
                        code="E_LANG_MISSING_TITLE",
                        message=f"no lang entry {key!r} in {primary_locale}"))

    def _check_manifest_consistency(self) -> None:
        manifest = self.book.manifest or {}
        entries = manifest.get("entries", [])
        manifest_ids: dict[str, dict] = {}
        for e in entries:
            qid = e.get("id")
            if qid in manifest_ids:
                self._add(Diagnostic(
                    file=".ftbq-cache/manifest.json5", line=1, col=1,
                    severity=SEVERITY_ERROR, code="E_MANIFEST_DUP_ID",
                    message=f"id {qid} appears in multiple manifest entries"))
            else:
                manifest_ids[qid] = e
        for qid, entry in manifest_ids.items():
            if qid not in self.all_ids:
                self._add(Diagnostic(
                    file=".ftbq-cache/manifest.json5", line=1, col=1,
                    severity=SEVERITY_WARNING, code="E_MANIFEST_DANGLING",
                    message=f"manifest tracks {qid} ({entry.get('kind')}) "
                             f"but no such id exists in the book"))
        for ch in self.book.chapters:
            if not isinstance(ch.plain, dict):
                continue
            cid = ch.plain.get("id")
            if cid in manifest_ids:
                expected = manifest_ids[cid].get("content_hash")
                disk_obj = {k: v for k, v in ch.plain.items() if k != "quests"}
                actual = ftbq_ids.content_hash(disk_obj)
                if expected and actual != expected:
                    self._add(Diagnostic(
                        file=ch.rel_path, line=ch.root.line, col=ch.root.col,
                        severity=SEVERITY_WARNING,
                        code="E_MANIFEST_HASH_MISMATCH",
                        message=f"chapter {cid} content differs from manifest"))
            for q in ch.plain.get("quests", []):
                qid = q.get("id")
                if qid not in manifest_ids:
                    continue
                expected = manifest_ids[qid].get("content_hash")
                disk_obj = {k: v for k, v in q.items() if k not in ("x", "y")}
                actual = ftbq_ids.content_hash(disk_obj)
                if expected and actual != expected:
                    self._add(Diagnostic(
                        file=ch.rel_path, line=ch.root.line, col=ch.root.col,
                        severity=SEVERITY_WARNING,
                        code="E_MANIFEST_HASH_MISMATCH",
                        message=f"quest {qid} content differs from manifest"))
        for rt in self.book.reward_tables:
            if not isinstance(rt.plain, dict):
                continue
            rid = rt.plain.get("id")
            if rid in manifest_ids:
                expected = manifest_ids[rid].get("content_hash")
                actual = ftbq_ids.content_hash(rt.plain)
                if expected and actual != expected:
                    self._add(Diagnostic(
                        file=rt.rel_path, line=rt.root.line, col=rt.root.col,
                        severity=SEVERITY_WARNING,
                        code="E_MANIFEST_HASH_MISMATCH",
                        message=f"reward table {rid} content differs from manifest"))


# ----------------------------------------------------------- fixer


class Fixer:
    """Applies autofix patches to chapter files in place."""

    def apply(self, book: BookModel,
                diagnostics: list[Diagnostic]) -> int:
        files: dict[str, list[Diagnostic]] = {}
        for diag in diagnostics:
            if not diag.autofix:
                continue
            files.setdefault(diag.file, []).append(diag)
        applied = 0
        for ch in book.chapters:
            if ch.rel_path not in files:
                continue
            # SNBT nodes all report line=1 col=1 (no position tracking);
            # text-span patching would corrupt the file.
            if ch.rel_path.endswith(".snbt"):
                continue
            text = ch.text
            patches: list[tuple[int, int, str]] = []
            for diag in files[ch.rel_path]:
                fix = diag.autofix
                if fix["kind"] == "item_object":
                    node = fix["node"]
                    start, end = self._span(text, node.line, node.col,
                                              node.end_line, node.end_col)
                    item_id = node.value
                    replacement = f'{{ id: "{item_id}", count: 1 }}'
                    patches.append((start, end, replacement))
                    applied += 1
                elif fix["kind"] == "drop_suffix":
                    tok = fix["token"]
                    start, end = self._span(text, tok.line, tok.col,
                                              tok.end_line, tok.end_col)
                    patches.append((start, end, ""))
                    applied += 1
                elif fix["kind"] == "filename":
                    field_node = fix.get("field_node")
                    if isinstance(field_node, Node):
                        start, end = self._span(text,
                                                  field_node.line,
                                                  field_node.col,
                                                  field_node.end_line,
                                                  field_node.end_col)
                        replacement = f'"{fix["replacement"]}"'
                        patches.append((start, end, replacement))
                        applied += 1
            if not patches:
                continue
            patches.sort(key=lambda p: p[0], reverse=True)
            for start, end, replacement in patches:
                text = text[:start] + replacement + text[end:]
            ch.path.write_text(text, encoding="utf-8")
        return applied

    @staticmethod
    def _span(text: str, line: int, col: int,
                end_line: int, end_col: int) -> tuple[int, int]:
        cur_line = 1
        cur_col = 1
        start = end = -1
        for i, ch in enumerate(text):
            if cur_line == line and cur_col == col and start == -1:
                start = i
            if cur_line == end_line and cur_col == end_col and start != -1:
                end = i
                return start, end
            if ch == "\n":
                cur_line += 1
                cur_col = 1
            else:
                cur_col += 1
        return start, len(text)


# ----------------------------------------------------------- output


def report_text(diagnostics: list[Diagnostic]) -> str:
    if not diagnostics:
        return "OK - no diagnostics."
    return "\n".join(d.format_text() for d in diagnostics)


def report_json(diagnostics: list[Diagnostic]) -> str:
    return json.dumps([d.to_json() for d in diagnostics], indent=2,
                       ensure_ascii=False)


def exit_code(diagnostics: list[Diagnostic], *, strict: bool) -> int:
    has_error = any(d.severity == SEVERITY_ERROR for d in diagnostics)
    has_warning = any(d.severity == SEVERITY_WARNING for d in diagnostics)
    if has_error or (strict and has_warning):
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Validate an FTB Quests config directory")
    p.add_argument("quests_dir", type=Path,
                    help="Path to config/ftbquests/quests/")
    p.add_argument("--json", action="store_true",
                    help="Emit machine-readable diagnostics")
    p.add_argument("--fix", action="store_true",
                    help="Apply autofixes for E_ITEM_BARE_STRING, "
                         "E_TYPE_SUFFIX, E_FILENAME_MISMATCH")
    p.add_argument("--strict", action="store_true",
                    help="Treat warnings as errors")
    p.add_argument("--manifest", type=Path,
                    help="Manifest path (default: "
                         "<quests_dir>/.ftbq-cache/manifest.json5)")
    args = p.parse_args(argv)

    quests_dir = args.quests_dir.resolve()
    if not quests_dir.exists():
        print(f"error: {quests_dir} does not exist", file=sys.stderr)
        return 2

    book = load_book(quests_dir, manifest_path=args.manifest)
    diags = Validator(book).run()

    if args.fix:
        applied = Fixer().apply(book, diags)
        if applied:
            book = load_book(quests_dir, manifest_path=args.manifest)
            diags = Validator(book).run()
            if not args.json:
                print(f"Applied {applied} autofix(es); re-validating...")

    if args.json:
        print(report_json(diags))
    else:
        print(report_text(diags))

    return exit_code(diags, strict=args.strict)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
