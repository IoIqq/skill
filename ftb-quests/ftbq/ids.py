"""Deterministic IDs and content fingerprints for FTB Quests objects.

The md5 formula is the documented contract (SKILL.md:86, reference §9):

    id = md5(f"{pack}/{chapter}/{obj}/{name}").hexdigest()[:16].upper()

`obj` is the kind path: ``chapter`` for chapters, ``quest/<quest_name>`` is
collapsed to ``quest`` (the chapter+quest_name pair already disambiguates
quests), tasks and rewards use ``task/<quest_name>.<name>`` and
``reward/<quest_name>.<name>`` respectively so a quest's own task/reward
namespace is independent of other quests in the same chapter.

**Top-bit mask.** FTB Quests stores ids as signed 64-bit ``long`` values and
generates them with ``Math.abs(nextLong())`` — i.e. always in
``[0, Long.MAX_VALUE]`` (top hex digit 0-7). On load it parses a hex-string id
with ``Long.parseLong(hex, 16)``, which **throws** for any magnitude above
``Long.MAX_VALUE`` (top digit 8-F); ``readID`` swallows that exception and
hands the object a brand-new random id, silently breaking every dependency
that referenced the original hex. So we mask the md5 digest's top bit
(``& 0x7FFFFFFFFFFFFFFF``) before formatting: the id is still a deterministic
16-char uppercase hex, but it always parses back to the same long FTB Quests
stores. This also keeps ``table_id`` (the decimal long a ``random``/``loot``/
``choice``/``all_table`` reward emits) within Java ``long`` range.

Content hash is sha256 over a canonical JSON dump of the object with
``id`` removed and keys sorted recursively.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

# FTB Quests ids are non-negative longs (Math.abs(nextLong())). Clearing the
# top bit keeps every generated id within [0, Long.MAX_VALUE] so FTB Quests'
# Long.parseLong-based loader round-trips it. See module docstring.
_LONG_MASK = (1 << 63) - 1  # 0x7FFFFFFFFFFFFFFF


def make_id(pack: str, chapter: str, obj_kind: str, name: str) -> str:
    """Return the 16-char uppercase hex ID for one object.

    Parameters mirror the documented formula. ``obj_kind`` is exactly the
    middle path segment ("chapter", "quest", "task/<quest>", "reward/<quest>",
    "reward_table"). The top bit is masked (see module docstring) so the id
    parses back cleanly in FTB Quests.
    """
    key = f"{pack}/{chapter}/{obj_kind}/{name}"
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()
    raw = int(digest[:16], 16) & _LONG_MASK
    return f"{raw:016X}"


def chapter_id(pack: str, chapter_name: str) -> str:
    return make_id(pack, chapter_name, "chapter", chapter_name)


def quest_id(pack: str, chapter_name: str, quest_name: str) -> str:
    return make_id(pack, chapter_name, "quest", quest_name)


def task_id(pack: str, chapter_name: str, quest_name: str, task_name: str) -> str:
    return make_id(pack, chapter_name, f"task/{quest_name}", task_name)


def reward_id(pack: str, chapter_name: str, quest_name: str, reward_name: str) -> str:
    return make_id(pack, chapter_name, f"reward/{quest_name}", reward_name)


def reward_table_id(pack: str, table_name: str) -> str:
    """16-hex id for a reward table. The md5 key is
    ``<pack>/<table_name>/reward_table/<table_name>`` (table_name occupies
    the chapter slot; reward tables have no chapter)."""
    return make_id(pack, table_name, "reward_table", table_name)


def table_reward_id(pack: str, table_name: str, entry_name: str) -> str:
    """16-hex id for one weighted reward entry inside a reward table. The
    ``table_reward`` kind path keeps it distinct from quest rewards."""
    return make_id(pack, table_name, f"table_reward/{entry_name}", entry_name)


def quest_link_id(pack: str, chapter_name: str, link_name: str) -> str:
    """16-hex id for a quest link (a mirror of a quest in another chapter)."""
    return make_id(pack, chapter_name, f"quest_link/{link_name}", link_name)


def image_id(pack: str, chapter_name: str, image_name: str) -> str:
    """16-hex id for a chapter background image."""
    return make_id(pack, chapter_name, f"image/{image_name}", image_name)


def hex_to_long(hex_id: str) -> int:
    """Parse a 16-hex id string to its non-negative long value — the form
    FTB Quests stores internally and the value ``table_id`` expects. The
    top bit is masked so an externally-supplied id above ``Long.MAX_VALUE``
    still fits a Java ``long`` (FTB Quests' own ids never set it)."""
    return int(hex_id, 16) & _LONG_MASK


class IdCollisionError(Exception):
    """Two distinct objects hashed to the same 16-hex id.

    Under the make_id scheme, objects of different kinds already use
    disjoint key prefixes (``task/<quest>`` vs ``reward/<quest>`` etc.) so
    cross-kind collisions are practically impossible; this is the provable
    backstop that guarantees they never silently happen. The realistic
    trigger is two same-kind objects sharing a name in the same scope
    (e.g. two tasks named ``collect`` in one quest) — a spec mistake the
    author wants flagged, not silently merged.
    """


class IdRegistry:
    """Guarantees no two generated ids collide.

    Register every id with its object kind + a human-readable location; a
    duplicate raises :class:`IdCollisionError` naming both sites. Used by
    the generator as a pre-emit validation pass so a pack with clashing ids
    is never written to disk.
    """

    def __init__(self) -> None:
        self._seen: dict[str, tuple[str, str]] = {}

    def register(self, id_str: str, kind: str, location: str) -> None:
        prev = self._seen.get(id_str)
        if prev is not None:
            raise IdCollisionError(
                f"{kind} id {id_str} at {location} collides with "
                f"{prev[0]} at {prev[1]} — give them distinct names")
        self._seen[id_str] = (kind, location)

    def __contains__(self, id_str: str) -> bool:
        return id_str in self._seen

    def __len__(self) -> int:
        return len(self._seen)




def _strip_id(value: Any) -> Any:
    """Recursively drop ``id`` keys so structural identity is hashed,
    not the very thing we computed from it."""
    if isinstance(value, dict):
        return {k: _strip_id(v) for k, v in value.items() if k != "id"}
    if isinstance(value, list):
        return [_strip_id(v) for v in value]
    return value


def content_hash(obj: Any) -> str:
    """Return ``sha256:<hex>`` for one quest/chapter/task/reward object.

    Deterministic across runs:
      * keys sorted recursively
      * id field excluded
      * separators chosen so whitespace cannot perturb the digest
    """
    canon = json.dumps(_strip_id(obj), sort_keys=True, separators=(",", ":"),
                        ensure_ascii=False)
    return "sha256:" + hashlib.sha256(canon.encode("utf-8")).hexdigest()
