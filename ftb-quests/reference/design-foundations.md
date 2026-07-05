# FTB Quests 1.20.1 — Design Foundations

Eight independent decision modules. Each module is one axis of choice. Combine modules to build any pack identity.

Evidence from 10+ shipped packs (8000+ quests analyzed) is cited inline as `[evidence: pack, N quests]` — never as the organizing principle.

---

## Module A — Progression Tightness

*How locked is the player? Controls `progression_mode` and dependency wiring.*

| Option | `progression_mode` | Dependency wiring | When to use | Tradeoff |
|---|---|---|---|---|
| **Freeform** | `"flexible"` | Few or no deps | Veterans, sandbox packs | No guidance, easy to get lost |
| **Guided** | `"flexible"` | Many deps but none lock | Kitchen-sinks, broad mod selection | Players can skip ahead |
| **Gated** | `"default"` | Gate quests unlock chapters | Expert packs, balanced progression | Forces specific path |
| **Forced linear** | `"default"` | Strict chain, each → next | Tutorials, narrative packs | Zero player choice |

**Key insight:** Guidance and gating are two mechanisms — decouple them. A quest book *guides* (shows next step) and *gates* (blocks until ready). Don't force one dependency graph to do both. [evidence: ATM10, 4601 quests — flexible graph guides, item tasks gate the endgame]

**Settings:**
- `progression_mode: "flexible"` — deps hide but don't lock; passive tasks (advancements/biomes) count
- `progression_mode: "default"` — quest locks until deps done; strict order

---

## Module B — Chapter Organization

*How is content chunked into chapters?*

| Option | Structure | When to use |
|---|---|---|
| **Per-mod** | One chapter per mod | Kitchen-sinks, players pick what to learn |
| **Themed** | One chapter per theme/age/dimension | Story packs, narrative progression |
| **Tier-gated** | Chapters by material tier | Endgame identity, expert packs |
| **Tutorial tiers** | Beginner → Advanced → Expert per mod | Teaching packs |
| **Hybrid** | Linear ch1 + per-mod middle + tier-gated capstone | Most real packs |

**Rules:**
- One chapter = one mod OR one theme, not both
- Follow the mod's native progression (ore → ingot → part → machine → upgrade)
- Capstone chapter (if any) is self-contained: components live in-chapter, cross-mod breadth comes from item tasks, not cross-chapter `depends_on`
- [evidence: ATM9/ATM10 per-mod + ATM Star capstone; SF4 per-age; E2:E gate-tiered; Academy per-mod × 3 tiers]

---

## Module C — Reward Philosophy

*What does completing a quest give the player?*

| Option | Density | Type | When to use |
|---|---|---|---|
| **Generous** | 1-2 rewards/quest | item + xp + loot | Celebrate every step, keep engagement |
| **Educational** | 1 reward/quest | materials for next lesson | Teaching packs, reduce grind |
| **Minimal** | 0.1-0.3/quest | xp only, or none | Expert packs, journey = reward |
| **Random** | 1/quest | loot tables, choice | Engagement via surprise |
| **Choice-based** | 1/quest (pick 1 of N) | choice rewards | Let players pick their path |

**Scaling rules:**
- **Density:** tech 60-95%, tutorial 30-50%, capstone 90-100%
- **XP scaling:** early 1-2x, mid 3-5x, endgame 6-9x
- **Item count:** single item=1, recipe materials=recipe count, fuel=16-64
- **Random:** exploration 50-90%, tech 0-20%, capstone 0%
- Generosity is density, not exotic types — pile standard rewards [evidence: ATM10 has no custom/command rewards, 1.5/quest]

**Anti-pattern:** Random rewards giving endgame items in early quests breaks progression. Curate loot tables carefully or use deterministic rewards. [evidence: Stoneblock 3 criticism]

---

## Module D — Cross-Mod Integration

*How much do mods interact through quests?*

| Option | Pattern | When to use |
|---|---|---|
| **Independent** | Mods in isolation, capstone is exception | Kitchen-sinks, mods are optional |
| **Teaching** | Quests explain how mods connect | Tutorial packs |
| **Recipe web** | Each important item needs 3-5 mods | Expert packs, force exploration |
| **Deep integration** | All mods route through one core mod's crafting | Themed packs with core mod |

**Representing synergy in quests:**
- Multiple item tasks on one quest = prove player used both mods
- `depends_on: ["<modA>/<key_quest>"]` = mod B gates after mod A
- `quest_links[]` (hexagon, size 2.0) = same quest in two chapters
- `type: "custom"` + KubeJS = deep integration checks

**Never fake synergy** — verify the interaction exists in JEI/EMI before writing the quest.

---

## Module E — Endgame Shape

*What is the final goal?*

| Option | Structure | When to use |
|---|---|---|
| **None** | Player-defined goals | Pure sandbox |
| **Convergence capstone** | One item requiring components from every major mod | Kitchen-sinks wanting a unifying goal |
| **Bragging rights** | Craft all creative/max items | Expert packs, completionists |
| **Meta-progression** | Points persist across worlds, unlock new content | Replayability-focused packs |
| **Story completion** | Explore all themes/locations/chapters | Narrative packs |

**Convergence capstone visual grammar:** origin `(0,0)`, chapter's largest shape (pentagon/octagon, size 5.0), components fan radially as dependents (each a sub-tree of 6-9). [evidence: ATM Star]

**Anti-pattern:** Endgame grind without purpose — if the capstone item has no use after crafting, the reward is hollow. Give it meaning. [evidence: Stoneblock 3 singularities criticism]

---

## Module F — Layout Family

*How are quests arranged spatially within a chapter?*

| Family | Aspect ratio | Spine | When to use |
|---|---|---|---|
| **Narrative** | ~2:1 (wider) | Horizontal line at y=0, branches fan vertically | Story, main path + branches |
| **Catalog** | ~1:1 (square) | None — uniform grid | Lookup, variants, tiers |
| **Tier-spine** | ~3:1 (wide) | Root at left → horizontal chain → converge right | Material tiers, tech ladders |
| **Convergence star** | ~1:1 | Center node, radial dependents | Capstone chapters |

**Clutter control (by chapter size):**

| Chapter size | Primary tool | Secondary tool |
|---|---|---|
| <30 quests | `hide_dependent_lines` (surgical) | None needed |
| 30-80 quests | `hide_until_deps_visible` (branch/leaf) | `hide_dependent_lines` (crossing edges) |
| 80+ quests | `hide_until_deps_visible` (most leaves) | Chapter sub-tabs via `quest_links` |

**Coordinate conventions:** x-step ~3.5, y-step 2.5-3.0 between branch rows, per-chapter-local coordinates.

---

## Module G — Task Type Mix

*What kinds of tasks do quests require?*

| Mix | Item % | Other % | When to use |
|---|---|---|---|
| **Item-heavy** | 90-98% | checkmark/advancement | Crafting-focused, kitchen-sinks |
| **Mixed** | 70-90% | kill/biome/structure/dimension | Diverse mechanics, exploration |
| **Tutorial-heavy** | 30-50% | checkmark 50-70% | Teaching chapters |

**When to use non-item tasks:**
- `checkmark` — tutorials, info, "read this"
- `advancement` — vanilla milestones
- `dimension` — first visit to new dimension
- `biome` — exploration milestones
- `kill` — boss fights (only when the fight IS the lesson)

**Default to `item`** — design around the item economy. Other types are seasoning. [evidence: 94.2% item across 722 tasks]

---

## Module H — Optional Content Strategy

*How is optional content designed?*

**Usage:** 2-14% of chapter content

**Three purposes:**

| Purpose | Design | Reward |
|---|---|---|
| **Alternative paths** | Different mods/appaches to same goal | Equivalent value |
| **Side content** | Interesting but not required | Modest (1 XP level) |
| **Convenience items** | Quality of life, not progression | Small utility |

**Visual:** size 1.25, `shape: "circle"`, `optional: true`

**Anti-patterns:**
- Fake optional — other quests depend on it
- Reward traps — large rewards force completion
- Hidden alternatives — choices not explained in text

---

## Decision Combinator

Pick one option from each module to define your pack:

```
A: Progression  →  B: Chapters  →  C: Rewards  →  D: Cross-Mod  →  E: Endgame  →  F: Layout  →  G: Tasks  →  H: Optional
```

**Kitchen-sink recipe:**
A=Guided, B=Per-mod+Hybrid, C=Generous, D=Independent+capstone, E=Convergence, F=Mixed, G=Item-heavy, H=Side content

**Tutorial recipe:**
A=Forced linear (tutorials) → Freeform (after), B=Tutorial tiers, C=Educational, D=Teaching, E=Story completion, F=Narrative, G=Mixed (checkmark-heavy), H=Alternative paths

**Expert recipe:**
A=Gated, B=Tier-gated, C=Minimal, D=Recipe web, E=Bragging rights, F=Tier-spine, G=Item-heavy, H=None

**Themed journey recipe:**
A=Guided, B=Themed, C=Moderate, D=Deep integration, E=Story completion, F=Narrative, G=Mixed, H=Side content

---

## Shape & Size Semantics

| Shape | Meaning | Size |
|---|---|---|
| `circle` | Default/intermediate | 1.0 |
| `square` | Stat/advancement hub | 2.0 |
| `gear` | Create milestone | 2.0 |
| `hexagon` | Cross-chapter quest_links | 2.0 |
| `rsquare` | Secret/optional | 1.5 |
| `diamond` | Special | 1.0-1.5 |
| `octagon` | Endgame/tier | 1.5-2.0 |
| `pentagon` | Capstone (largest) | 3.0-5.0 |

**Size tiers:** leaf (0.8-1.0, ~76%), hub (1.2-2.0, ~18%), boss (2.0-5.0, ~5%)

**Chapter `default_quest_shape` = mod identity.** Pick one shape per chapter; don't rainbow.

---

## Quest Text Patterns

| Slot | Where | Length | Job |
|---|---|---|---|
| `title` | Always visible | ≤4 words | Name the thing |
| `subtitle` | On hover | 1 line | The action |
| `description` | When opened | 2-4 sentences | Context, why, hint |

**Color codes:** `&6` (gold, primary), `&e` (yellow, highlights), `&r` (reset). Use sparingly.

**Write prose, not checklists.** The UI already shows item+count+reward. Spend text on *why* and *how*.

---

## Universal Anti-Patterns

1. **Fake optional** — optional quests that other quests depend on
2. **Random rewards breaking progression** — loot bags giving endgame items early
3. **Bolted-on quests** — quests disconnected from pack identity
4. **Endgame grind without purpose** — capstone items with no use after crafting
5. **Overwhelming choice** — too many mods with no guidance
6. **Tutorial overload** — forcing tutorials on players who don't need them
7. **Fake synergy** — cross-mod quests for mods that don't actually interact
8. **Long diagonals** — dependency lines crossing the whole chapter
9. **All-lines-visible** — in chapters >30 quests, creates visual noise
10. **Mixing layout families** — narrative + catalog in the same chapter

---

## Evidence Base

| Pack | Quests | Key contribution |
|---|---|---|
| ATM9/10 | 4601 | Module A (flexible), B (per-mod+capstone), C (generous), F (tier-spine) |
| Create: Delight Remake | 2295 | F (narrative+catalog), C (rich rewards), D (deep integration) |
| Enigmatica 2 Expert | 650+ | A (gated), D (recipe web), C (choice-based) |
| FTB Academy | 300+ | B (tutorial tiers), G (checkmark-heavy), C (educational) |
| Sky Factory 4 | 200+ | E (meta-progression), C (minimal) |
| Stoneblock 3 | 200-400 | Anti-patterns documented for C (random) and E (grind) |
| GTNH | 1000+ | A (forced linear), D (extreme recipe web), C (minimal) |
| Create: Astral | ~500 | B (themed), D (deep integration), E (story) |

All data collected 2026-07-04 to 2026-07-05.
