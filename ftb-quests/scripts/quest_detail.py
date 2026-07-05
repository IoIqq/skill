"""Focused one-quest preview — id / shape / deps / tasks / rewards / lang for
a single quest.

Token-saving: replaces reading the WHOLE chapter file in the Step 4 per-node
polish loop. The agent runs this after regenerating to verify just the quest
it touched, not every quest in the chapter.

Resolves the quest by NAME: reads ``<output_dir>/quests.spec.json5`` for the
pack name, computes the 16-hex id (the same md5 formula the generator uses),
then finds that id in the generated chapter file. JSON5 packs also pull the
quest's lang entries; SNBT packs print the inline title/subtitle/description.

Usage::

    python scripts/quest_detail.py <output_dir> <chapter>/<quest>
    python scripts/quest_detail.py <output_dir> <chapter>/<quest> --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from ftbq import ids as ftbq_ids  # noqa: E402
from ftbq.json5 import Json5Error, parse, to_plain  # noqa: E402
from ftbq.snbt import SnbtError, parse_snbt_file  # noqa: E402


def _load_spec(output_dir: Path) -> dict | None:
    p = output_dir / "quests.spec.json5"
    if not p.exists():
        return None
    try:
        v = to_plain(parse(p.read_text(encoding="utf-8-sig"), filename=str(p)))
        return v if isinstance(v, dict) else None
    except (Json5Error, OSError):
        return None


def _detect_format(quests_root: Path) -> str:
    if (quests_root / "data.snbt").exists():
        return "snbt"
    return "json5"


def _load_chapter(quests_root: Path, chapter: str, fmt: str) -> dict | None:
    ext = "snbt" if fmt == "snbt" else "json5"
    p = quests_root / "chapters" / f"{chapter}.{ext}"
    if not p.exists():
        return None
    try:
        if fmt == "snbt":
            v = parse_snbt_file(p)
        else:
            v = to_plain(parse(p.read_text(encoding="utf-8-sig"),
                                 filename=str(p)))
        return v if isinstance(v, dict) else None
    except (Json5Error, SnbtError, OSError):
        return None


def _load_quest_lang(quests_root: Path, qid: str, locale: str) -> dict:
    """JSON5: pull ``quest.<qid>.{title,quest_subtitle,quest_desc}``."""
    p = quests_root / "lang" / locale / "quests.json5"
    if not p.exists():
        return {}
    try:
        data = to_plain(parse(p.read_text(encoding="utf-8-sig"),
                                filename=str(p)))
    except (Json5Error, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    out: dict[str, Any] = {}
    for sub in ("title", "quest_subtitle", "quest_desc"):
        key = f"quest.{qid}.{sub}"
        if key in data:
            out[sub] = data[key]
    return out


def _resolve_names(spec: dict, pack: str, chapter: str,
                   quest: str) -> tuple[dict[str, str], dict[str, str]]:
    """Build {task_id: name} / {reward_id: name} from the spec quest, so the
    on-disk task/reward objects (which carry only an id) can be labelled with
    their spec names."""
    task_names: dict[str, str] = {}
    reward_names: dict[str, str] = {}
    for ch in spec.get("chapters", []):
        if ch.get("name") != chapter:
            continue
        for q in ch.get("quests", []):
            if q.get("name") != quest:
                continue
            for t in q.get("tasks", []):
                if isinstance(t, dict) and t.get("name"):
                    task_names[ftbq_ids.task_id(pack, chapter, quest,
                                                  t["name"])] = t["name"]
            for r in q.get("rewards", []):
                if isinstance(r, dict) and r.get("name"):
                    reward_names[ftbq_ids.reward_id(pack, chapter, quest,
                                                       r["name"])] = r["name"]
    return task_names, reward_names


def _compact_fields(obj: dict, skip: set[str]) -> list[str]:
    """One ``k: v`` token per field (compact; item objects show id first)."""
    parts: list[str] = []
    for k, v in obj.items():
        if k in skip:
            continue
        if isinstance(v, dict):
            # show id first, then the rest, for item objects
            items = list(v.items())
            if "id" in v:
                items = [("id", v["id"])] + [(dk, dv) for dk, dv in items
                                              if dk != "id"]
            inner = ", ".join(f"{dk}: {dv}" for dk, dv in items)
            parts.append(f"{k}: {{ {inner} }}")
        elif isinstance(v, list):
            parts.append(f"{k}: {v}")
        else:
            parts.append(f"{k}: {v}")
    return parts


def build_detail(output_dir: Path, chapter: str, quest: str) -> dict:
    """Return a dict describing one quest (or raise ValueError)."""
    spec = _load_spec(output_dir)
    if spec is None:
        raise ValueError(f"no quests.spec.json5 at {output_dir}")
    pack = spec.get("pack", "")
    fmt = spec.get("format") or _detect_format(output_dir / "quests")
    quests_root = output_dir / "quests"
    qid = ftbq_ids.quest_id(pack, chapter, quest)
    chap = _load_chapter(quests_root, chapter, fmt)
    if chap is None:
        raise ValueError(f"chapter file not found: chapters/{chapter}.{fmt}")
    quests = chap.get("quests", []) if isinstance(chap.get("quests"), list) else []
    q = next((x for x in quests if isinstance(x, dict)
              and str(x.get("id", "")).upper() == qid), None)
    if q is None:
        raise ValueError(f"quest {chapter}/{quest} (id {qid}) not in chapter "
                         f"— has it been generated?")

    out: dict[str, Any] = {
        "ref": f"{chapter}/{quest}",
        "id": qid,
        "chapter": chapter,
        "shape": q.get("shape", ""),
        "x": q.get("x"),
        "y": q.get("y"),
        "dependencies": q.get("dependencies", []),
        "dependency_requirement": q.get("dependency_requirement", "all"),
        "tasks": q.get("tasks", []),
        "rewards": q.get("rewards", []),
        "format": fmt,
    }
    # Label on-disk tasks/rewards (id-only) with their spec names.
    task_names, reward_names = _resolve_names(spec, pack, chapter, quest)
    for t in out["tasks"]:
        if isinstance(t, dict) and t.get("id") in task_names:
            t["name"] = task_names[t["id"]]
    for r in out["rewards"]:
        if isinstance(r, dict) and r.get("id") in reward_names:
            r["name"] = reward_names[r["id"]]
    if fmt == "snbt":
        for f in ("title", "subtitle", "description"):
            if f in q:
                out[f] = q[f]
    else:
        locale = spec.get("default_locale") or "en_us"
        out["lang"] = {locale: _load_quest_lang(quests_root, qid, locale)}
    return out


def render_text(d: dict) -> str:
    lines: list[str] = [
        f"quest {d['ref']}   id: {d['id']}",
        f"  shape: {d['shape']}   x: {d['x']} y: {d['y']}   "
        f"depends_on: {d['dependencies']}   "
        f"dep_requirement: {d['dependency_requirement']}",
    ]
    tasks = d.get("tasks", [])
    lines.append(f"  tasks ({len(tasks)}):")
    for t in tasks:
        if not isinstance(t, dict):
            continue
        fields = _compact_fields(t, {"id", "type", "name"})
        lines.append(f"    {t.get('name', '?'):<14} {t.get('type', '?'):<22} "
                     + "  ".join(fields))
    rewards = d.get("rewards", [])
    lines.append(f"  rewards ({len(rewards)}):")
    for r in rewards:
        if not isinstance(r, dict):
            continue
        fields = _compact_fields(r, {"id", "type", "name"})
        lines.append(f"    {r.get('name', '?'):<14} {r.get('type', '?'):<22} "
                     + "  ".join(fields))
    if d.get("format") == "snbt":
        for f in ("title", "subtitle", "description"):
            if f in d:
                lines.append(f"  {f}: {d[f]}")
    else:
        for locale, lang in (d.get("lang") or {}).items():
            lines.append(f"  lang ({locale}):")
            for sub, val in lang.items():
                lines.append(f"    {sub}: {val}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Focused one-quest preview (token-saving for the Step 4 loop)")
    p.add_argument("output_dir", type=Path,
                    help="Generator output dir (holds quests.spec.json5 + quests/)")
    p.add_argument("ref", type=Path,
                    help="<chapter>/<quest> name")
    p.add_argument("--json", action="store_true", help="Machine-readable")
    args = p.parse_args(argv)

    ref = str(args.ref).replace("\\", "/")
    if "/" not in ref:
        print("error: ref must be <chapter>/<quest>", file=sys.stderr)
        return 2
    chapter, quest = ref.split("/", 1)
    try:
        d = build_detail(args.output_dir.resolve(), chapter, quest)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(d, indent=2, ensure_ascii=False))
    else:
        print(render_text(d))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
