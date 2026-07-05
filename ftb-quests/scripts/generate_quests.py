"""Generate FTB Quests config files from a quests.spec.json5 source.

Pipeline (overwrite mode — incremental merge added later):

    quests.spec.json5  +  quests/lang/<locale>/quests.json5 (@placeholders)
        |
        v
    <output_dir>/quests/
        chapters/*.json5
        data.json5
        chapter_groups.json5  (only if spec.chapter_groups is non-empty)
        lang/<locale>/quests.json5  (placeholders rewritten to hex keys)
        .ftbq-cache/manifest.json5

Game files live under a clean ``quests/`` subfolder — copy it whole into
``<pack>/config/ftbquests/quests/`` for a new pack, or use ``--deploy`` to
merge it into an existing pack safely (additive files merged, originals
backed up to ``.ftbq-backup/<ts>/``; see ``ftbq.deploy``).
``quests.spec.json5`` stays at ``<output_dir>`` root and is never deployed.

Same spec → byte-identical output (sorted keys, 1-decimal floats, trailing
commas). The manifest captures every skill-owned ID with a content hash so
incremental merge can later distinguish pristine, user-edited, and
user-added quests.

Usage::

    python scripts/generate_quests.py <output_dir>
    python scripts/generate_quests.py <output_dir> --spec custom.spec.json5
    python scripts/generate_quests.py <output_dir> --mode {overwrite,preserve,ask}
    python scripts/generate_quests.py <output_dir> --adopt
    # preview a safe deploy into a live pack (writes nothing until --yes):
    python scripts/generate_quests.py <output_dir> --deploy <pack_root>
    python scripts/generate_quests.py <output_dir> --deploy <pack_root> --yes
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from collections import deque
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq import ids as ftbq_ids  # noqa: E402
from ftbq import deploy as ftbq_deploy  # noqa: E402
from ftbq.canonical import dump_file  # noqa: E402
from ftbq.json5 import Json5Error, parse, to_plain  # noqa: E402
from ftbq.snbt import SnbtError, dump_file_snbt, parse_snbt_file  # noqa: E402

__version__ = "0.3.0"
SCHEMA_VERSION = 1


# --------------------------------------------------------------------- specs


class SpecError(Exception):
    """Raised when the user-supplied spec is invalid."""


def load_spec(path: Path) -> dict:
    try:
        node = parse(path.read_text(encoding="utf-8"), filename=str(path))
    except Json5Error as exc:
        raise SpecError(str(exc)) from None
    spec = to_plain(node)
    if not isinstance(spec, dict):
        raise SpecError(f"{path}: top-level must be an object")
    _check_required(spec, ["pack", "chapters"], where=str(path))
    spec.setdefault("format", "json5")
    spec.setdefault("default_locale", "en_us")
    spec.setdefault("locales", [spec["default_locale"]])
    spec.setdefault("data", {})
    spec.setdefault("chapter_groups", [])
    spec.setdefault("reward_tables", [])
    if spec["format"] not in ("json5", "snbt"):
        raise SpecError(
            f"{path}: format {spec['format']!r} is not supported; "
            f"use 'json5' (current main) or 'snbt' (1.20.1)")
    return spec


def _check_required(obj: dict, fields: list[str], *, where: str) -> None:
    missing = [f for f in fields if f not in obj]
    if missing:
        raise SpecError(f"{where}: missing required field(s) {missing}")


# --------------------------------------------------------- ID + dependencies


def _validate_unique_ids(spec: dict,
                          rename_aliases: dict[tuple[str, str], list[str]]) -> None:
    """Guarantee every generated id is unique across all object kinds.

    Walks the spec and registers each id with the same functions the
    builders use (so it matches exactly what hits disk). A duplicate —
    same-kind (two tasks sharing a name in one quest) or the vanishingly
    rare cross-kind hash collision — raises SpecError naming both sites,
    *before* any file is written. Task and reward ids already use disjoint
    key prefixes (``task/<quest>`` vs ``reward/<quest>``) so they cannot
    collide in practice; this is the provable backstop.
    """
    pack = spec["pack"]
    reg = ftbq_ids.IdRegistry()
    for ch in spec["chapters"]:
        cname = ch["name"]
        reg.register(ftbq_ids.chapter_id(pack, cname),
                     "chapter", f"{pack}/{cname}")
        for img in ch.get("images", []):
            reg.register(ftbq_ids.image_id(pack, cname, img["name"]),
                         "chapter_image", f"{cname}/{img['name']}")
        for link in ch.get("quest_links", []):
            reg.register(ftbq_ids.quest_link_id(pack, cname, link["name"]),
                         "quest_link", f"{cname}/{link['name']}")
        for q in ch.get("quests", []):
            qname = q["name"]
            old = rename_aliases.get((cname, qname), [])
            qid = (ftbq_ids.quest_id(pack, cname, old[0])
                   if old else ftbq_ids.quest_id(pack, cname, qname))
            reg.register(qid, "quest", f"{cname}/{qname}")
            for t in q.get("tasks", []):
                reg.register(ftbq_ids.task_id(pack, cname, qname, t["name"]),
                             "task", f"{cname}/{qname}/{t['name']}")
            for r in q.get("rewards", []):
                reg.register(ftbq_ids.reward_id(pack, cname, qname, r["name"]),
                             "reward", f"{cname}/{qname}/{r['name']}")
    for tbl in spec.get("reward_tables", []):
        tname = tbl["name"]
        reg.register(ftbq_ids.reward_table_id(pack, tname),
                     "reward_table", f"{pack}/{tname}")
        for entry in tbl.get("rewards", []):
            reg.register(ftbq_ids.table_reward_id(pack, tname, entry["name"]),
                         "table_reward", f"{tname}/{entry['name']}")


def _resolve_dep_name(token: str, current_chapter: str) -> tuple[str, str]:
    if "/" in token:
        chap, qname = token.split("/", 1)
        return chap, qname
    return current_chapter, token


_HEX_ID_RE = re.compile(r"^[0-9A-Fa-f]{16}$")


def _is_external_hex_id(token: Any) -> bool:
    """True if a ``depends_on`` token is a raw 16-hex quest ID — a reference
    to a quest this skill did not generate (task linkage to existing pack
    content). Such tokens pass through to ``dependencies`` verbatim."""
    return isinstance(token, str) and bool(_HEX_ID_RE.match(token))


def _topo_sort(nodes: dict[str, list[str]]) -> list[str]:
    """Kahn's algorithm. Stable sort: ties broken alphabetically."""
    in_degree = {n: 0 for n in nodes}
    for n, deps in nodes.items():
        for d in deps:
            if d in in_degree:
                in_degree[n] += 1
    queue = deque(sorted(n for n, deg in in_degree.items() if deg == 0))
    out: list[str] = []
    while queue:
        n = queue.popleft()
        out.append(n)
        for m in sorted(nodes):
            if n in nodes[m] and in_degree[m] > 0:
                in_degree[m] -= 1
                if in_degree[m] == 0:
                    queue.append(m)
    if len(out) != len(nodes):
        cycle_nodes = [n for n, d in in_degree.items() if d > 0]
        raise SpecError(f"dependency cycle involving {cycle_nodes}")
    return out


# --------------------------------------------------------------------- layout


def auto_layout(quests: list[dict]) -> dict[str, tuple[float, float]]:
    """Compute (x, y) for each quest in a chapter.

    x = depth * 1.5, where depth is the longest path from any root.
    Multiple quests at the same depth get y offsets ±1.0 from the spine,
    deterministic by name.
    """
    name_to_quest = {q["name"]: q for q in quests}
    deps: dict[str, list[str]] = {}
    for q in quests:
        local: list[str] = []
        for token in q.get("depends_on", []):
            chap, qname = _resolve_dep_name(token, "")  # chapter ignored here
            if chap == "" and qname in name_to_quest:
                local.append(qname)
            elif qname in name_to_quest:
                local.append(qname)
        deps[q["name"]] = local

    depth: dict[str, int] = {}

    def compute_depth(name: str, stack: set[str]) -> int:
        if name in depth:
            return depth[name]
        if name in stack:
            raise SpecError(f"dependency cycle involving {name!r}")
        if not deps[name]:
            depth[name] = 0
            return 0
        d = 1 + max(compute_depth(n, stack | {name}) for n in deps[name])
        depth[name] = d
        return d

    for name in deps:
        compute_depth(name, set())

    # Group by depth, assign y offsets in a stable, alternating pattern.
    by_depth: dict[int, list[str]] = {}
    for name, d in depth.items():
        by_depth.setdefault(d, []).append(name)

    coords: dict[str, tuple[float, float]] = {}
    for d, names in by_depth.items():
        names.sort()
        n = len(names)
        # Convention: a single quest sits on the spine; two siblings split
        # ±1.0 around it; three siblings get one on the spine plus ±1.0;
        # n>=4 distributes with 1.0 spacing centered around 0.
        if n == 1:
            ys = [0.0]
        elif n == 2:
            ys = [-1.0, 1.0]
        else:
            base = -(n - 1) / 2.0
            ys = [round(base + i, 4) for i in range(n)]
        for name, y in zip(names, ys):
            coords[name] = (round(d * 1.5, 4), y)
    return coords


# --------------------------------------------------------- object normalization


def _normalize_item(item: Any) -> dict:
    """Normalize a spec item to the on-disk object form ``{id, count:1, ...}``.

    The on-disk item object's count is ALWAYS 1: FTB Quests' ``ItemTask``
    and ``ItemReward`` both read the SIBLING ``count`` field for the real
    quantity (``ItemTask.readData`` → ``getLong("count").orElse(1)``;
    ``ItemReward.claim`` → ``item.copyWithCount(count)``) and ignore the
    count inside the object. A count buried in the object would silently
    make the task require / the reward grant only 1. The caller lifts any
    such quantity to the sibling via ``_lift_item_count``.
    """
    if isinstance(item, str):
        return {"id": item, "count": 1}
    if isinstance(item, dict):
        out = dict(item)
        if "id" in out:
            out["count"] = 1
        return out
    raise SpecError(f"item must be a string or object, got {type(item).__name__}")


def _lift_item_count(out: dict, spec_obj: dict) -> None:
    """Lift a quantity buried in the spec item object to the sibling
    ``count`` field for ``ftbquests:item`` tasks/rewards.

    Keys off the presence of an ``item`` field (only item tasks/rewards have
    one) so it works for reward-table entries too, where the serializer
    omits ``type`` for item rewards. Without this, ``item: {id:"x", count:4}``
    would emit the object count and no sibling, so FTB Quests would
    require/grant 1.
    """
    if "item" not in out:  # only item tasks/rewards have an item to lift from
        return
    if "count" in out:  # explicit sibling count — canonical, nothing to lift
        return
    item = spec_obj.get("item")
    if isinstance(item, dict):
        c = item.get("count")
        if isinstance(c, (int, float)) and not isinstance(c, bool) and c != 1:
            out["count"] = c


def _build_task(spec_task: dict, *, pack: str, chapter: str,
                quest_name: str) -> dict:
    if "name" not in spec_task:
        raise SpecError(f"task in quest {quest_name!r} missing 'name'")
    if "type" not in spec_task:
        raise SpecError(
            f"task {spec_task['name']!r} in quest {quest_name!r} missing 'type'")
    out: dict[str, Any] = {
        "id": ftbq_ids.task_id(pack, chapter, quest_name, spec_task["name"]),
        "type": spec_task["type"],
    }
    for k, v in spec_task.items():
        if k in ("name",):
            continue
        if k == "item":
            out["item"] = _normalize_item(v)
        else:
            out[k] = v
    _lift_item_count(out, spec_task)
    # XPTask.readData requires `points` (orElseThrow — a missing value
    # throws on load and the quest book fails to open). Default to `true`
    # (value counts XP points; `false` = XP levels) so an XP task without
    # an explicit `points` still loads. See reference §7a.
    if out.get("type") == "ftbquests:xp" and "points" not in out:
        out["points"] = True
    return out


# Reward types whose effect comes from a referenced reward table — they emit
# a numeric ``table_id`` (the decimal long of the table's id) instead of
# carrying their own item/xp/command payload. See reference §17.
TABLE_REWARD_TYPES = {
    "ftbquests:loot", "ftbquests:random",
    "ftbquests:choice", "ftbquests:all_table",
}


def _resolve_table_id(spec_reward: dict, table_ids: dict[str, str],
                      *, quest_name: str) -> int | None:
    """Resolve a spec reward's ``table`` reference to the decimal long FTB
    Quests expects in ``table_id``. A bare 16-hex token references an external
    (non-skill) table and passes through; a name references a skill table."""
    token = spec_reward.get("table")
    if token is None:
        return None
    if _is_external_hex_id(token):
        return ftbq_ids.hex_to_long(str(token))
    if not isinstance(token, str) or token not in table_ids:
        raise SpecError(
            f"reward in quest {quest_name!r} references unknown reward "
            f"table {token!r}")
    return ftbq_ids.hex_to_long(table_ids[token])


def _build_reward(spec_reward: dict, *, pack: str, chapter: str,
                   quest_name: str,
                   table_ids: dict[str, str] | None = None) -> dict:
    if "name" not in spec_reward:
        raise SpecError(f"reward in quest {quest_name!r} missing 'name'")
    if "type" not in spec_reward:
        raise SpecError(
            f"reward {spec_reward['name']!r} in quest {quest_name!r} missing 'type'")
    out: dict[str, Any] = {
        "id": ftbq_ids.reward_id(pack, chapter, quest_name, spec_reward["name"]),
        "type": spec_reward["type"],
    }
    for k, v in spec_reward.items():
        if k in ("name", "table"):
            continue
        if k == "item":
            out["item"] = _normalize_item(v)
        else:
            out[k] = v
    _lift_item_count(out, spec_reward)
    # loot/random/choice/all_table rewards reference a reward table by the
    # decimal long of its id (field `table_id`), not by name/hex string.
    if out["type"] in TABLE_REWARD_TYPES:
        if "table" not in spec_reward:
            raise SpecError(
                f"reward {spec_reward['name']!r} in quest {quest_name!r} "
                f"is type {out['type']!r} but has no 'table' field")
        if table_ids is not None:
            tid = _resolve_table_id(spec_reward, table_ids, quest_name=quest_name)
            if tid is not None:
                out["table_id"] = tid
    return out


def _build_quest(spec_quest: dict, *, pack: str, chapter: str,
                  coords: dict[str, tuple[float, float]],
                  name_to_id: dict[tuple[str, str], str],
                  default_dep_chapter: str,
                  default_shape: str,
                  table_ids: dict[str, str] | None = None) -> dict:
    name = spec_quest["name"]
    qid = name_to_id.get((chapter, name)) or ftbq_ids.quest_id(
        pack, chapter, name)
    x, y = coords.get(name, (0.0, 0.0))
    if spec_quest.get("x") is not None:
        x = float(spec_quest["x"])
    if spec_quest.get("y") is not None:
        y = float(spec_quest["y"])

    deps = []
    for token in spec_quest.get("depends_on", []):
        # A 16-char hex token references an existing quest this skill did
        # NOT generate (hand-written, another tool, a community book) —
        # pass it through verbatim so new quests can link to pack content
        # without re-owning its ID. See SKILL.md "Task linkage".
        if _is_external_hex_id(token):
            deps.append(str(token).upper())
            continue
        chap, qname = _resolve_dep_name(token, default_dep_chapter)
        if (chap, qname) not in name_to_id:
            raise SpecError(
                f"quest {name!r} depends on unknown {chap}/{qname}")
        deps.append(name_to_id[(chap, qname)])

    quest: dict[str, Any] = {
        "id": qid,
        "x": float(x),
        "y": float(y),
        "shape": spec_quest.get("shape", default_shape),
        "dependencies": deps,
        "tasks": [_build_task(t, pack=pack, chapter=chapter, quest_name=name)
                   for t in spec_quest.get("tasks", [])],
        "rewards": [_build_reward(r, pack=pack, chapter=chapter, quest_name=name,
                                    table_ids=table_ids)
                     for r in spec_quest.get("rewards", [])],
    }
    if spec_quest.get("optional"):
        quest["optional"] = True
    if spec_quest.get("dependency_requirement", "all") != "all":
        quest["dependency_requirement"] = spec_quest["dependency_requirement"]
    # Pass through any additional FTB Quests fields unchanged.
    reserved = {"name", "x", "y", "shape", "depends_on", "optional",
                "dependency_requirement", "tasks", "rewards", "layout"}
    for k, v in spec_quest.items():
        if k not in reserved and k not in quest:
            quest[k] = v
    return quest


def _resolve_quest_ref(token: Any,
                        name_to_id: dict[tuple[str, str], str],
                        default_chapter: str, *, owner: str,
                        field: str) -> str:
    """Resolve a quest reference (``<chapter>/<quest>`` name or raw 16-hex)
    to a hex id, for quest links and image dependencies."""
    if _is_external_hex_id(token):
        return str(token).upper()
    chap, qname = _resolve_dep_name(token, default_chapter)
    if (chap, qname) not in name_to_id:
        raise SpecError(
            f"{owner} references unknown quest {chap}/{qname} ({field})")
    return name_to_id[(chap, qname)]


def _build_quest_link(spec_link: dict, *, pack: str, chapter: str,
                       name_to_id: dict[tuple[str, str], str]) -> dict:
    """A quest link mirrors a quest (usually from another chapter) at a
    position in this chapter. On-disk shape (QuestLink.writeData):
    ``{id, linked_quest, x, y, shape?, size?}`` — x/y are required."""
    if "name" not in spec_link:
        raise SpecError(f"quest link in chapter {chapter!r} missing 'name'")
    if "linked_quest" not in spec_link:
        raise SpecError(
            f"quest link {spec_link['name']!r} in chapter {chapter!r} "
            f"missing 'linked_quest'")
    link: dict[str, Any] = {
        "id": ftbq_ids.quest_link_id(pack, chapter, spec_link["name"]),
        "linked_quest": _resolve_quest_ref(
            spec_link["linked_quest"], name_to_id, chapter,
            owner=f"quest link {spec_link['name']!r}", field="linked_quest"),
        "x": float(spec_link.get("x", 0.0)),
        "y": float(spec_link.get("y", 0.0)),
    }
    if spec_link.get("shape"):
        link["shape"] = spec_link["shape"]
    if spec_link.get("size", 1) != 1:
        link["size"] = spec_link["size"]
    return link


def _build_chapter_image(spec_image: dict, *, pack: str, chapter: str,
                          name_to_id: dict[tuple[str, str], str]) -> dict:
    """A chapter background image. On-disk shape (ChapterImage.writeData):
    ``{id, image, x, y, width, height, rotation, color?, alpha?, order?,
    click?, dev?, corner?, dependency?}`` — x/y/width/height/rotation/image
    are required."""
    if "name" not in spec_image:
        raise SpecError(f"image in chapter {chapter!r} missing 'name'")
    img: dict[str, Any] = {
        "id": ftbq_ids.image_id(pack, chapter, spec_image["name"]),
        "image": spec_image.get("image", ""),
        "x": float(spec_image.get("x", 0.0)),
        "y": float(spec_image.get("y", 0.0)),
        "width": float(spec_image.get("width", 1.0)),
        "height": float(spec_image.get("height", 1.0)),
        "rotation": float(spec_image.get("rotation", 0.0)),
    }
    if spec_image.get("color") is not None:
        img["color"] = spec_image["color"]
    if spec_image.get("alpha", 255) != 255:
        img["alpha"] = spec_image["alpha"]
    if spec_image.get("order", 0) != 0:
        img["order"] = spec_image["order"]
    if spec_image.get("click"):
        img["click"] = spec_image["click"]
    if spec_image.get("dev"):
        img["dev"] = True
    if spec_image.get("corner"):
        img["corner"] = True
    dep = spec_image.get("dependency")
    if dep:
        img["dependency"] = _resolve_quest_ref(
            dep, name_to_id, chapter,
            owner=f"image {spec_image['name']!r}", field="dependency")
    return img


def _build_chapter(spec_chapter: dict, *, pack: str,
                    name_to_id: dict[tuple[str, str], str],
                    rename_aliases: dict[tuple[str, str], list[str]] | None = None,
                    table_ids: dict[str, str] | None = None,
                    ) -> dict:
    name = spec_chapter["name"]
    cid = ftbq_ids.chapter_id(pack, name)
    quests = spec_chapter.get("quests", [])
    layout_mode = spec_chapter.get("layout", {}).get("mode", "auto")
    if layout_mode == "auto":
        coords = auto_layout(quests)
    else:
        coords = {q["name"]: (float(q.get("x") or 0.0),
                                float(q.get("y") or 0.0))
                   for q in quests}

    default_shape = spec_chapter.get("default_quest_shape", "circle")

    built_quests = [
        _build_quest(q, pack=pack, chapter=name, coords=coords,
                      name_to_id=name_to_id, default_dep_chapter=name,
                      default_shape=default_shape, table_ids=table_ids)
        for q in quests
    ]

    chapter: dict[str, Any] = {
        "id": cid,
        "filename": name,
        "default_quest_shape": default_shape,
        "group": spec_chapter.get("group", ""),
        "order_index": spec_chapter.get("order_index", 0),
        "quests": built_quests,
    }
    quest_links = [_build_quest_link(l, pack=pack, chapter=name,
                                       name_to_id=name_to_id)
                    for l in spec_chapter.get("quest_links", [])]
    if quest_links:
        chapter["quest_links"] = quest_links
    images = [_build_chapter_image(i, pack=pack, chapter=name,
                                     name_to_id=name_to_id)
                for i in spec_chapter.get("images", [])]
    if images:
        chapter["images"] = images
    # Pass through any additional FTB Quests chapter fields unchanged
    # (progression_mode, always_invisible, visibility flags, autofocus_id,
    # default_quest_size, …). Spec-only directives are excluded.
    reserved = {"name", "group", "order_index", "default_quest_shape",
                "layout", "quests", "quest_links", "images"}
    for k, v in spec_chapter.items():
        if k not in reserved and k not in chapter:
            chapter[k] = v
    return chapter


# ---------------------------------------------------------- top-level emit


CHAPTER_KEY_ORDER = ["id", "filename", "group", "order_index",
                      "default_quest_shape", "quests", "quest_links",
                      "images"]
QUEST_KEY_ORDER = ["id", "x", "y", "shape", "optional",
                    "dependency_requirement", "dependencies",
                    "tasks", "rewards"]
TASK_KEY_ORDER = ["id", "type", "item", "count"]
REWARD_KEY_ORDER = ["id", "type", "item", "count", "table_id"]
QUEST_LINK_KEY_ORDER = ["id", "linked_quest", "x", "y", "shape", "size"]
IMAGE_KEY_ORDER = ["id", "image", "x", "y", "width", "height", "rotation",
                    "color", "alpha", "order", "click", "dev", "corner",
                    "dependency"]
# Reward table file: id first, then the weighted rewards list, then settings.
REWARD_TABLE_KEY_ORDER = ["id", "rewards", "empty_weight", "loot_size",
                           "hide_tooltip", "use_title", "loot_crate",
                           "loot_table_id"]
# Each weighted entry: id, optional type (omitted for item rewards), then the
# reward's own fields, then weight.
TABLE_REWARD_KEY_ORDER = ["id", "type", "item", "count", "weight"]


# --------------------------------------------------------- format dispatch
# ``json5`` targets current ``main`` (MC 1.21.x, FTB Quests 26.x); ``snbt``
# targets 1.20.1, which serializes via ``dev.ftb.mods.ftblibrary.snbt.SNBT`` —
# ``data.snbt`` / ``chapters/*.snbt`` / ``reward_tables/*.snbt`` / no lang
# files (text is inline). See ``ftbq/snbt.py`` and reference §12.
def _ext(fmt: str) -> str:
    return "snbt" if fmt == "snbt" else "json5"


def _dump(fmt: str, path: Path, value: Any, **kw: Any) -> None:
    """Write ``value`` in the pack's on-disk format (JSON5 or SNBT)."""
    if fmt == "snbt":
        dump_file_snbt(path, value, **kw)
    else:
        dump_file(path, value, **kw)


def _parse_disk(fmt: str, path: Path) -> dict | None:
    """Parse an existing on-disk chapter/table file to a plain dict, or
    return ``None`` if missing or unparseable (caller falls back to new)."""
    if not path.exists():
        return None
    if fmt == "snbt":
        try:
            return parse_snbt_file(path)
        except SnbtError:
            return None
    try:
        return to_plain(parse(path.read_text(encoding="utf-8"),
                                 filename=str(path)))
    except Json5Error:
        return None


def _build_name_index(spec: dict) -> dict[tuple[str, str], str]:
    pack = spec["pack"]
    out: dict[tuple[str, str], str] = {}
    for ch in spec["chapters"]:
        for q in ch.get("quests", []):
            out[(ch["name"], q["name"])] = ftbq_ids.quest_id(
                pack, ch["name"], q["name"])
    return out


def _emit_chapter_file(chapter: dict, quests_root: Path, *,
                       fmt: str = "json5") -> None:
    path = quests_root / "chapters" / f"{chapter['filename']}.{_ext(fmt)}"
    path.parent.mkdir(parents=True, exist_ok=True)
    _dump(fmt, path, chapter, key_order=CHAPTER_KEY_ORDER,
          per_path_key_order={
              "quests.[]": QUEST_KEY_ORDER,
              "quests.[].tasks.[]": TASK_KEY_ORDER,
              "quests.[].rewards.[]": REWARD_KEY_ORDER,
              "quest_links.[]": QUEST_LINK_KEY_ORDER,
              "images.[]": IMAGE_KEY_ORDER,
          })


def _emit_data_file(spec: dict, quests_root: Path, *,
                    fmt: str = "json5") -> None:
    data = dict(spec.get("data", {}))
    data.setdefault("default_quest_disable_jei", False)
    _dump(fmt, quests_root / f"data.{_ext(fmt)}", data)


def _emit_chapter_groups(spec: dict, quests_root: Path, *,
                         fmt: str = "json5") -> None:
    groups = spec.get("chapter_groups") or []
    if not groups:
        return
    out_groups = []
    for g in groups:
        gid = ftbq_ids.make_id(spec["pack"], g["name"], "chapter_group", g["name"])
        out_groups.append({
            "id": gid,
            "name": g["name"],
            "order_index": g.get("order_index", 0),
        })
    _dump(fmt, quests_root / f"chapter_groups.{_ext(fmt)}",
          {"chapter_groups": out_groups})


# ---------------------------------------------------------- reward tables


def _build_table_reward(spec_entry: dict, *, pack: str, table_name: str) -> dict:
    """Build one weighted reward entry inside a reward table.

    Mirrors ``RewardTable.writeData``: ``id`` always present; ``type`` omitted
    for item rewards (item is the implicit default there); the reward's own
    fields normalized like a chapter reward; ``weight`` only when != 1.
    """
    if "name" not in spec_entry:
        raise SpecError(f"reward table {table_name!r}: entry missing 'name'")
    if "type" not in spec_entry:
        raise SpecError(
            f"reward table {table_name!r}: entry {spec_entry['name']!r} "
            f"missing 'type'")
    rtype = spec_entry["type"]
    entry: dict[str, Any] = {
        "id": ftbq_ids.table_reward_id(pack, table_name, spec_entry["name"]),
    }
    # RewardTable omits `type` for item rewards (implicit). Other types must
    # declare it so RewardType.createReward picks the right class.
    if rtype != "ftbquests:item":
        entry["type"] = rtype
    for k, v in spec_entry.items():
        if k in ("name", "type", "weight"):
            continue
        if k == "item":
            entry["item"] = _normalize_item(v)
        else:
            entry[k] = v
    _lift_item_count(entry, spec_entry)
    weight = spec_entry.get("weight", 1)
    if weight != 1:
        entry["weight"] = weight
    return entry


def _build_reward_table(spec_table: dict, *, pack: str) -> dict:
    """Build the on-disk reward table object (no ``name`` field — the name is
    the file's stem, carried separately by the caller)."""
    name = spec_table["name"]
    table: dict[str, Any] = {
        "id": ftbq_ids.reward_table_id(pack, name),
        "rewards": [_build_table_reward(r, pack=pack, table_name=name)
                    for r in spec_table.get("rewards", [])],
    }
    if spec_table.get("empty_weight"):
        table["empty_weight"] = spec_table["empty_weight"]
    table["loot_size"] = spec_table.get("loot_size", 1)
    # FTB Quests reads an ABSENT hide_tooltip/use_title as TRUE (tooltip
    # hidden, table title forced). Emit them explicitly so the intent is
    # unambiguous; default to showing the reward list and not forcing a title.
    table["hide_tooltip"] = spec_table.get("hide_tooltip", False)
    table["use_title"] = spec_table.get("use_title", False)
    for k in ("loot_crate", "loot_table_id"):
        if k in spec_table:
            table[k] = spec_table[k]
    return table


def _emit_reward_table_file(table: dict, name: str, quests_root: Path,
                             *, fmt: str = "json5") -> None:
    path = quests_root / "reward_tables" / f"{name}.{_ext(fmt)}"
    path.parent.mkdir(parents=True, exist_ok=True)
    _dump(fmt, path, table, key_order=REWARD_TABLE_KEY_ORDER,
          per_path_key_order={"rewards.[]": TABLE_REWARD_KEY_ORDER})


def merge_reward_table(new_table: dict, name: str, quests_root: Path,
                        existing_manifest: dict, *, mode: str,
                        prompt_fn=None, fmt: str = "json5") -> dict:
    """Whole-table incremental merge (coarser than per-quest chapter merge).

    If the on-disk table is pristine (content_hash matches the manifest),
    re-emit. If it was user-edited, respect ``mode`` (preserve keeps the
    disk table; ask prompts; overwrite re-emits). A table whose disk id is
    not in the manifest is treated as fresh and re-emitted.
    """
    path = quests_root / "reward_tables" / f"{name}.{_ext(fmt)}"
    disk = _parse_disk(fmt, path)
    if disk is None:
        return new_table
    entries = (existing_manifest or {}).get("entries", [])
    disk_id = disk.get("id")
    entry = next((e for e in entries
                   if e.get("kind") == "reward_table"
                   and e.get("id") == disk_id), None)
    if entry is None:
        return new_table
    if ftbq_ids.content_hash(disk) == entry.get("content_hash"):
        return new_table  # pristine
    if mode == "preserve":
        return disk
    if mode == "ask" and prompt_fn is not None:
        action = prompt_fn(disk_id, "content-edited", disk, new_table)
        return disk if action == "keep" else new_table
    return new_table  # overwrite


# ---------------------------------------------------------------- lang


_LANG_PLACEHOLDER = re.compile(
    r"^@(?P<chapter>[^/.]+)(?:/(?P<quest>[^.]+))?\.(?P<sub>[a-z_]+)$")


def rewrite_lang(lang_obj: dict, *, pack: str,
                  name_to_id: dict[tuple[str, str], str],
                  chapter_ids: dict[str, str]) -> dict:
    out: dict[str, Any] = {}
    for key, value in lang_obj.items():
        m = _LANG_PLACEHOLDER.match(key)
        if not m:
            out[key] = value
            continue
        chap = m.group("chapter")
        quest = m.group("quest")
        sub = m.group("sub")
        if quest is None:
            if chap not in chapter_ids:
                raise SpecError(f"lang key {key!r} references unknown chapter")
            new_key = f"chapter.{chapter_ids[chap]}.{sub}"
        else:
            if (chap, quest) not in name_to_id:
                raise SpecError(f"lang key {key!r} references unknown quest")
            new_key = f"quest.{name_to_id[(chap, quest)]}.{sub}"
        out[new_key] = value
    return out


def _load_lang_file(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return to_plain(parse(path.read_text(encoding="utf-8"),
                                 filename=str(path)))
    except Json5Error as exc:
        raise SpecError(f"failed to parse lang file {path}: {exc}") from None


def _emit_lang_files(spec: dict, quests_root: Path,
                      name_to_id: dict[tuple[str, str], str],
                      chapter_ids: dict[str, str]) -> None:
    lang_dir = quests_root / "lang"
    for locale in spec.get("locales", []):
        # The LLM-authored file uses @<chapter>/<quest>.subkey placeholders.
        merged_path = lang_dir / locale / "quests.json5"
        existing = _load_lang_file(merged_path)
        # Lang policy: NEVER overwrite an existing rewritten key.
        # Only add new entries derived from the placeholder file.
        new_keys = rewrite_lang(existing, pack=spec["pack"],
                                  name_to_id=name_to_id,
                                  chapter_ids=chapter_ids)
        # Merge: rewritten keys take priority for new IDs, but existing
        # rewritten keys are preserved.
        result: dict[str, Any] = {}
        for key, value in new_keys.items():
            result[key] = value
        merged_path.parent.mkdir(parents=True, exist_ok=True)
        dump_file(merged_path, result, quote_keys=True)


# ---------------------------------------------------------------- manifest


MANIFEST_PATH_REL = ".ftbq-cache/manifest.json5"
MANIFEST_KEY_ORDER = ["schema", "pack", "generated_at", "generator_version",
                       "spec_hash", "entries"]
ENTRY_KEY_ORDER = ["kind", "chapter", "quest", "name", "id", "file",
                    "content_hash", "x", "y", "aliases"]


def _build_manifest_name_maps(
        spec: dict,
        rename_aliases: dict[tuple[str, str], list[str]],
) -> tuple[dict[tuple[str, str], str],
           dict[tuple[str, str, str], str],
           dict[tuple[str, str, str], str]]:
    """Build O(1) reverse-lookup maps for build_manifest.

    Returns:
        quest_names  : (chapter, quest_hex)          -> quest_name
        task_names   : (chapter, quest_hex, task_hex) -> task_name
        reward_names : (chapter, quest_hex, rew_hex)  -> reward_name

    Accounts for renamed quests: the stored hex is the *old* hex (from the
    first alias name), matching what _build_name_index_with_aliases emits.
    Task/reward IDs are derived from the current (new) quest name in spec.
    """
    pack = spec["pack"]
    quest_names: dict[tuple[str, str], str] = {}
    task_names: dict[tuple[str, str, str], str] = {}
    reward_names: dict[tuple[str, str, str], str] = {}
    for ch in spec["chapters"]:
        cname = ch["name"]
        for q in ch.get("quests", []):
            qname = q["name"]
            old_names = rename_aliases.get((cname, qname), [])
            qhex = (ftbq_ids.quest_id(pack, cname, old_names[0])
                    if old_names else ftbq_ids.quest_id(pack, cname, qname))
            quest_names[(cname, qhex)] = qname
            for t in q.get("tasks", []):
                thex = ftbq_ids.task_id(pack, cname, qname, t["name"])
                task_names[(cname, qhex, thex)] = t["name"]
            for r in q.get("rewards", []):
                rhex = ftbq_ids.reward_id(pack, cname, qname, r["name"])
                reward_names[(cname, qhex, rhex)] = r["name"]
    return quest_names, task_names, reward_names


def build_manifest(spec: dict, chapters: list[dict],
                     *, rename_aliases: dict[tuple[str, str], list[str]] | None = None,
                     tables: list[tuple[dict, str]] | None = None,
                     ) -> dict:
    pack = spec["pack"]
    fmt = spec.get("format", "json5")
    ext = _ext(fmt)
    rename_aliases = rename_aliases or {}
    quest_names, task_names, reward_names = _build_manifest_name_maps(
        spec, rename_aliases)
    entries: list[dict] = []
    for ch in chapters:
        ch_entry = {
            "kind": "chapter",
            "name": ch["filename"],
            "id": ch["id"],
            "file": f"chapters/{ch['filename']}.{ext}",
            "content_hash": ftbq_ids.content_hash(_chapter_for_hash(ch)),
        }
        entries.append(ch_entry)
        for q in ch["quests"]:
            qname = quest_names.get((ch["filename"], q["id"]), "")
            entries.append({
                "kind": "quest",
                "chapter": ch["filename"],
                "name": qname,
                "id": q["id"],
                "file": f"chapters/{ch['filename']}.{ext}",
                "content_hash": ftbq_ids.content_hash(_quest_for_hash(q)),
                "x": q["x"],
                "y": q["y"],
                "aliases": list(rename_aliases.get(
                    (ch["filename"], qname), [])),
            })
            for t in q.get("tasks", []):
                entries.append({
                    "kind": "task",
                    "chapter": ch["filename"],
                    "quest": qname,
                    "name": task_names.get((ch["filename"], q["id"], t["id"]), ""),
                    "id": t["id"],
                    "content_hash": ftbq_ids.content_hash(t),
                })
            for r in q.get("rewards", []):
                entries.append({
                    "kind": "reward",
                    "chapter": ch["filename"],
                    "quest": qname,
                    "name": reward_names.get((ch["filename"], q["id"], r["id"]), ""),
                    "id": r["id"],
                    "content_hash": ftbq_ids.content_hash(r),
                })
    for tbl, name in (tables or []):
        entries.append({
            "kind": "reward_table",
            "name": name,
            "id": tbl["id"],
            "file": f"reward_tables/{name}.{ext}",
            "content_hash": ftbq_ids.content_hash(tbl),
        })
    return {
        "schema": SCHEMA_VERSION,
        "format": fmt,
        "pack": pack,
        "generated_at": _utc_now(),
        "generator_version": __version__,
        "spec_hash": "sha256:" + ftbq_ids.content_hash(spec).split(":", 1)[1],
        "entries": entries,
    }


def _chapter_for_hash(ch: dict) -> dict:
    """Strip the quests list for chapter content hashing — quests have
    their own entries."""
    return {k: v for k, v in ch.items() if k != "quests"}


def _quest_for_hash(q: dict) -> dict:
    """Strip x/y from the content hash — those track separately so a
    user moving a quest in-game doesn't count as a content edit."""
    return {k: v for k, v in q.items() if k not in ("x", "y")}



def _emit_manifest(manifest: dict, quests_root: Path) -> None:
    path = quests_root / MANIFEST_PATH_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    dump_file(path, manifest, key_order=MANIFEST_KEY_ORDER,
               per_path_key_order={"entries.[]": ENTRY_KEY_ORDER})


def _quest_name_for_id(spec: dict, chapter_name: str, quest_hex: str,
                         name_to_id: dict[tuple[str, str], str]) -> str:
    """Reverse-look-up a spec quest name from its emitted hex ID. Honors
    the alias-aware name_to_id mapping (renamed quests keep their old ID)."""
    for (chap, name), qid in name_to_id.items():
        if chap == chapter_name and qid == quest_hex:
            return name
    return ""


def _utc_now() -> str:
    return (_dt.datetime.now(_dt.timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z"))


# ---------------------------------------------------- incremental merge


def _load_existing_manifest(quests_root: Path) -> dict | None:
    path = quests_root / MANIFEST_PATH_REL
    if not path.exists():
        return None
    try:
        return to_plain(parse(path.read_text(encoding="utf-8"),
                                 filename=str(path)))
    except Json5Error:
        return None


def classify_quest(disk_quest: dict, manifest_entries: list[dict]) -> str:
    """Return one of: pristine | content-edited | position-edited |
    user-added.

    `pristine`: ID + content_hash + (x,y) all match manifest.
    `content-edited`: ID matches but content_hash differs.
    `position-edited`: ID + content_hash match but (x,y) differ.
    `user-added`: ID is not in manifest.
    """
    qid = disk_quest.get("id")
    entry = next((e for e in manifest_entries
                   if e.get("kind") == "quest" and e.get("id") == qid), None)
    if entry is None:
        return "user-added"
    h_now = ftbq_ids.content_hash(_quest_for_hash(disk_quest))
    if h_now != entry.get("content_hash"):
        return "content-edited"
    if (disk_quest.get("x") != entry.get("x")
            or disk_quest.get("y") != entry.get("y")):
        return "position-edited"
    return "pristine"



def merge_chapter(new_chapter: dict, quests_root: Path,
                    existing_manifest: dict, *, mode: str,
                    prompt_fn=None, fmt: str = "json5") -> dict:
    """Merge a freshly built chapter dict against the existing on-disk
    chapter (if any). Returns the chapter dict that should be written.

    Position edits (only x/y differ) are ALWAYS preserved regardless of
    mode — moving a quest in-game is never destructive content drift.

    `mode`:
        overwrite — re-emit content for content-edited quests; preserve
                     user-added; drop skill-deleted unless prompted to keep
        preserve  — keep on-disk content for content-edited quests; pass
                     through user-added; keep skill-deleted
        ask       — call `prompt_fn(quest_id, classification, old, new)`
                     for each conflict; respect its return value
                     ("keep" | "overwrite")
    """
    chap_path = quests_root / "chapters" / f"{new_chapter['filename']}.{_ext(fmt)}"
    disk = _parse_disk(fmt, chap_path)
    if disk is None:
        return new_chapter

    entries = (existing_manifest or {}).get("entries", [])
    disk_quests_by_id = {q.get("id"): q for q in disk.get("quests", [])
                          if q.get("id")}

    merged: list[dict] = []
    seen_ids: set[str] = set()

    for new_q in new_chapter["quests"]:
        nid = new_q["id"]
        seen_ids.add(nid)
        if nid not in disk_quests_by_id:
            merged.append(new_q)
            continue
        disk_q = disk_quests_by_id[nid]
        cls = classify_quest(disk_q, entries)
        if cls == "pristine":
            merged.append(new_q)
        elif cls == "position-edited":
            # Always preserve user position edits.
            keep = dict(new_q)
            keep["x"] = disk_q.get("x", new_q["x"])
            keep["y"] = disk_q.get("y", new_q["y"])
            merged.append(keep)
        elif cls == "content-edited":
            if mode == "preserve":
                merged.append(disk_q)
            elif mode == "ask" and prompt_fn is not None:
                action = prompt_fn(new_q["id"], cls, disk_q, new_q)
                merged.append(disk_q if action == "keep" else new_q)
            else:
                # overwrite: re-emit but keep the user's x/y if changed.
                keep = dict(new_q)
                if (disk_q.get("x") != new_q["x"]
                        or disk_q.get("y") != new_q["y"]):
                    keep["x"] = disk_q.get("x", new_q["x"])
                    keep["y"] = disk_q.get("y", new_q["y"])
                merged.append(keep)
        else:
            merged.append(new_q)

    for did, dq in disk_quests_by_id.items():
        if did in seen_ids:
            continue
        cls = classify_quest(dq, entries)
        if cls == "user-added":
            merged.append(dq)
        elif mode == "preserve":
            merged.append(dq)
        elif mode == "ask" and prompt_fn is not None:
            action = prompt_fn(did, "skill-deleted", dq, None)
            if action == "keep":
                merged.append(dq)
        # overwrite: skill-deleted quests are dropped (intentional)

    out = dict(new_chapter)
    out["quests"] = merged
    return out


def reconcile_renames(spec: dict, existing_manifest: dict,
                        *, prompt_fn=None) -> dict[tuple[str, str], list[str]]:
    """For each chapter, identify quests in the manifest whose names
    are missing from the new spec. Returns
    ``{(chapter, new_name): [old_name, ...]}`` capturing the aliases
    that the operator confirmed (via prompt_fn) preserve the original
    hex ID.
    """
    pack = spec["pack"]
    aliases: dict[tuple[str, str], list[str]] = {}
    spec_names_by_chapter: dict[str, set[str]] = {
        ch["name"]: {q["name"] for q in ch.get("quests", [])}
        for ch in spec["chapters"]
    }
    manifest_quests = [e for e in existing_manifest.get("entries", [])
                        if e.get("kind") == "quest"]
    by_chapter: dict[str, list[dict]] = {}
    for e in manifest_quests:
        by_chapter.setdefault(e["chapter"], []).append(e)

    for ch_name, m_quests in by_chapter.items():
        spec_names = spec_names_by_chapter.get(ch_name, set())
        missing = [m for m in m_quests if m.get("name") not in spec_names]
        if not missing:
            continue
        # Candidate new names = spec names whose ID isn't already in the
        # manifest (i.e. genuinely new). For each missing manifest entry,
        # ask if it was renamed.
        existing_ids = {m["id"] for m in m_quests}
        candidates = []
        for new_name in spec_names_by_chapter.get(ch_name, set()):
            new_id = ftbq_ids.quest_id(pack, ch_name, new_name)
            if new_id not in existing_ids:
                candidates.append(new_name)
        for old_entry in missing:
            chosen = None
            if prompt_fn is not None:
                chosen = prompt_fn(old_entry["name"], candidates)
            if chosen and chosen in candidates:
                aliases.setdefault((ch_name, chosen), []).append(
                    old_entry["name"])
    return aliases


# --------------------------------------------------------------- driver


def generate(spec: dict, output_dir: Path, *,
              mode: str = "overwrite",
              prompt_fn=None,
              rename_prompt_fn=None,
              adopt: bool = False) -> dict:
    """Run the full pipeline. Returns the manifest dict.

    `mode`:
        overwrite — regenerate everything skill-owned (user-added quests
                     are still preserved)
        preserve  — keep on-disk content for any quest the manifest
                     classifies as user-edited
        ask       — call prompt_fn(quest_id, classification, disk_q,
                     new_q) per conflict, expect "keep" or "overwrite"
    `rename_prompt_fn(old_name, candidates)` is called when a manifest
        entry's name vanishes from the spec; return a string from
        candidates to confirm it was renamed (preserves the old hex ID),
        or None / falsy to treat as deletion.
    `adopt`: if True and there is no existing manifest but chapters/
        already has content, build a manifest treating ALL existing
        quests as user-added (skill won't touch them on re-run).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    quests_root = output_dir / "quests"
    quests_root.mkdir(parents=True, exist_ok=True)
    fmt = spec.get("format", "json5")
    existing_manifest = _load_existing_manifest(quests_root)

    # Adopt mode: synthesize a manifest from disk, marking everything as
    # user-added by leaving the manifest empty for those IDs. Then
    # generate fresh skill-owned content alongside.
    if adopt and existing_manifest is None:
        existing_manifest = _adopt_existing_pack(quests_root, spec["pack"])

    rename_aliases: dict[tuple[str, str], list[str]] = {}
    if existing_manifest is not None and rename_prompt_fn is not None:
        rename_aliases = reconcile_renames(spec, existing_manifest,
                                              prompt_fn=rename_prompt_fn)

    name_to_id = _build_name_index_with_aliases(spec, rename_aliases)
    chapter_ids = {ch["name"]: ftbq_ids.chapter_id(spec["pack"], ch["name"])
                    for ch in spec["chapters"]}
    # Reward tables are file-level; resolve their ids up front so chapter
    # rewards can reference them by name → numeric table_id.
    table_ids = {t["name"]: ftbq_ids.reward_table_id(spec["pack"], t["name"])
                  for t in spec.get("reward_tables", [])}

    # Guarantee no two ids collide (same-kind dup name, or the rare cross-kind
    # hash collision) BEFORE building/emitting — never write a half pack.
    try:
        _validate_unique_ids(spec, rename_aliases)
    except ftbq_ids.IdCollisionError as exc:
        raise SpecError(str(exc)) from None

    chapters_built = [_build_chapter(ch, pack=spec["pack"],
                                        name_to_id=name_to_id,
                                        rename_aliases=rename_aliases,
                                        table_ids=table_ids)
                       for ch in spec["chapters"]]

    for ch in chapters_built:
        merged = ch
        if existing_manifest is not None:
            merged = merge_chapter(ch, quests_root, existing_manifest,
                                      mode=mode, prompt_fn=prompt_fn, fmt=fmt)
        _emit_chapter_file(merged, quests_root, fmt=fmt)

    tables_built = [(_build_reward_table(t, pack=spec["pack"]), t["name"])
                     for t in spec.get("reward_tables", [])]
    for tbl, name in tables_built:
        merged = tbl
        if existing_manifest is not None:
            merged = merge_reward_table(tbl, name, quests_root,
                                          existing_manifest, mode=mode,
                                          prompt_fn=prompt_fn, fmt=fmt)
        _emit_reward_table_file(merged, name, quests_root, fmt=fmt)

    _emit_data_file(spec, quests_root, fmt=fmt)
    _emit_chapter_groups(spec, quests_root, fmt=fmt)
    # 1.20.1 SNBT has no lang files — text is inline on quests/chapters.
    if fmt != "snbt":
        _emit_lang_files(spec, quests_root, name_to_id, chapter_ids)

    manifest = build_manifest(spec, chapters_built,
                                rename_aliases=rename_aliases,
                                tables=tables_built)
    _emit_manifest(manifest, quests_root)
    return manifest


def _adopt_existing_pack(quests_root: Path, pack: str) -> dict:
    """Build an empty manifest. Existing on-disk quests will then be
    classified as user-added on subsequent runs."""
    return {
        "schema": SCHEMA_VERSION,
        "pack": pack,
        "generated_at": _utc_now(),
        "generator_version": __version__,
        "spec_hash": "sha256:adopt",
        "entries": [],
    }


def _build_name_index_with_aliases(
        spec: dict,
        rename_aliases: dict[tuple[str, str], list[str]],
) -> dict[tuple[str, str], str]:
    pack = spec["pack"]
    out: dict[tuple[str, str], str] = {}
    for ch in spec["chapters"]:
        for q in ch.get("quests", []):
            old_names = rename_aliases.get((ch["name"], q["name"]), [])
            if old_names:
                # Preserve the original hex ID by using the first old name.
                out[(ch["name"], q["name"])] = ftbq_ids.quest_id(
                    pack, ch["name"], old_names[0])
            else:
                out[(ch["name"], q["name"])] = ftbq_ids.quest_id(
                    pack, ch["name"], q["name"])
    return out


def _interactive_prompt(qid: str, classification: str,
                          disk: dict | None, new: dict | None) -> str:
    """Default ask-mode prompt — terminal-based."""
    if classification == "skill-deleted":
        title = (disk or {}).get("id", qid)
        ans = input(f"  Quest {title} is in the spec NO LONGER. Keep it on "
                     f"disk anyway? [keep/delete] ").strip().lower()
        return "keep" if ans.startswith("k") else "delete"
    short = qid[:8]
    ans = input(f"  Quest {short} is {classification}. "
                 f"[keep on-disk / overwrite from spec]? "
                 f"[k/o] ").strip().lower()
    if ans.startswith("k"):
        return "keep"
    return "overwrite"


def _interactive_rename_prompt(old_name: str,
                                  candidates: list[str]) -> str | None:
    if not candidates:
        return None
    print(f"  Spec quest {old_name!r} has disappeared.")
    print(f"  Candidates that could be a rename: {candidates}")
    ans = input(f"  Renamed to which? (blank = treat as deletion) ").strip()
    return ans if ans in candidates else None


def _run_deploy(quests_root: Path, target: Path, *,
                yes: bool, no_backup: bool) -> int:
    """Preview (and, with --yes, apply) a safe copy of the generated
    ``quests/`` tree into the live modpack folder. Prints the overwrite
    report; writes nothing unless ``yes`` is set."""
    plan = ftbq_deploy.plan(quests_root, target)
    if not yes:
        # Preview only — flag every overwrite, write nothing.
        print(ftbq_deploy.render_report(plan))
        return 0
    report = ftbq_deploy.apply(plan, target, backup=not no_backup)
    print(ftbq_deploy.render_report(plan, report))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Generate FTB Quests config from quests.spec.json5")
    p.add_argument("output_dir", type=Path,
                    help="Directory under which a clean quests/ subfolder "
                         "(chapters/, data.json5, lang/, .ftbq-cache/) "
                         "will be written")
    p.add_argument("--spec", type=Path,
                    help="Spec file (default: <output_dir>/quests.spec.json5)")
    p.add_argument("--mode", choices=["overwrite", "preserve", "ask"],
                    default="overwrite",
                    help="How to handle pre-existing chapter files")
    p.add_argument("--adopt", action="store_true",
                    help="First run on an existing pack: mark current "
                         "on-disk content as user-added in the manifest")
    p.add_argument("--no-rename-prompt", action="store_true",
                    help="Skip the interactive rename prompt; vanished "
                         "spec names are always treated as deletions")
    p.add_argument("--dry-run", action="store_true",
                    help="Build the manifest but don't write any files")
    deploy_grp = p.add_mutually_exclusive_group()
    deploy_grp.add_argument("--deploy", type=Path, metavar="PACK_ROOT",
                    help="After generating, safely merge <output_dir>/quests/ "
                         "into <PACK_ROOT>/config/ftbquests/quests/. Additive "
                         "files (data/chapter_groups/lang) are merged; chapters "
                         "and the manifest that already exist are backed up to "
                         ".ftbq-backup/<ts>/ then replaced. Writes nothing "
                         "until --yes.")
    deploy_grp.add_argument("--quests-dir", type=Path, metavar="DIR",
                    help="Like --deploy but target an explicit quests "
                         "directory instead of <pack>/config/ftbquests/quests.")
    p.add_argument("--yes", action="store_true",
                    help="Apply the deploy plan (otherwise only a preview is "
                         "printed). Backups are created unless --no-backup.")
    p.add_argument("--no-backup", action="store_true",
                    help="Skip backing up overwritten originals (dangerous, "
                         "irreversible) when applying a deploy.")
    args = p.parse_args(argv)

    if args.dry_run and (args.deploy or args.quests_dir):
        print("error: --deploy cannot be combined with --dry-run "
              "(nothing to deploy)", file=sys.stderr)
        return 2

    output_dir = args.output_dir.resolve()
    spec_path = (args.spec or (output_dir / "quests.spec.json5")).resolve()
    if not spec_path.exists():
        print(f"error: spec not found at {spec_path}", file=sys.stderr)
        return 2

    try:
        spec = load_spec(spec_path)
    except SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    prompt_fn = _interactive_prompt if args.mode == "ask" else None
    rename_fn = (None if args.no_rename_prompt
                  else _interactive_rename_prompt)

    if args.dry_run:
        # Build chapters and manifest in memory without writing.
        name_to_id = _build_name_index_with_aliases(spec, {})
        table_ids = {t["name"]: ftbq_ids.reward_table_id(spec["pack"], t["name"])
                      for t in spec.get("reward_tables", [])}
        chapters_built = [_build_chapter(ch, pack=spec["pack"],
                                            name_to_id=name_to_id,
                                            table_ids=table_ids)
                           for ch in spec["chapters"]]
        tables_built = [(_build_reward_table(t, pack=spec["pack"]), t["name"])
                         for t in spec.get("reward_tables", [])]
        manifest = build_manifest(spec, chapters_built, tables=tables_built)
    else:
        try:
            manifest = generate(spec, output_dir, mode=args.mode,
                                  prompt_fn=prompt_fn,
                                  rename_prompt_fn=rename_fn,
                                  adopt=args.adopt)
        except SpecError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    n_chap = sum(1 for e in manifest["entries"] if e["kind"] == "chapter")
    n_q = sum(1 for e in manifest["entries"] if e["kind"] == "quest")
    n_t = sum(1 for e in manifest["entries"] if e["kind"] == "task")
    n_r = sum(1 for e in manifest["entries"] if e["kind"] == "reward")
    n_rt = sum(1 for e in manifest["entries"] if e["kind"] == "reward_table")
    label = "(dry run) " if args.dry_run else ""
    print(f"{label}Generated {n_chap} chapters, {n_q} quests, {n_t} tasks, "
          f"{n_r} rewards, {n_rt} reward tables → {output_dir}/quests/")

    if args.deploy or args.quests_dir:
        target = (args.quests_dir
                  or args.deploy / "config" / "ftbquests" / "quests")
        return _run_deploy(output_dir / "quests", target.resolve(),
                            yes=args.yes, no_backup=args.no_backup)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
