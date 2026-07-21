# Layout Quick Reference — shape, size, clutter flags, layout families

Load this before assigning or adjusting x/y/shape/size on any quest. For coordinate algorithms and topology classification, see `topology-coordinates.md`. For the reasoning behind these patterns, see `design-guide.md §layout-reasoning`.

## Three layout families — pick one per chapter, don't mix

| Family | When to use | Aspect | Spine | Hub handling |
|---|---|---|---|---|
| **Narrative/progression** | Story-driven chapter with a main path + branches | ~2:1 (wider than tall) | Horizontal line at `y=0`, x-step 3.5 | Vertical fan-out sub-trees |
| **Kitchen-sink/ATM** | Per-mod chapter in a kitchen-sink pack (ATM-style) | 1:1 to 3:1 | Compact grid, x-step 0.5–1.0 | `hide_dependency_lines` over spatial separation |
| **Reference/catalog** | Lookup grid of variants/tiers (no story order) | ~1:1 (square) | None — uniform grid | Adjacent-cell deps only |

The kitchen-sink/ATM family has 5 sub-templates (Compact Horizontal Spine, Vertical Tiered Cascade, Parallel Material Columns, Radial Hub, Decorated Freeform) plus 2 cross-genre templates (Hexagonal Expert Web for GregTech/expert, Narrative World Map for RPG/adventure) — full parameters + selection decision tree: `design-guide.md §atm-layout-patterns`. Genre-specific authoring patterns: `§pack-type-patterns`.

Key difference narrative vs kitchen-sink: tighter grid (0.5-unit vs 3.5-unit x-step), `hide_dependency_lines` as the primary anti-clutter lever (vs `hide_until_deps_visible` for narrative), and shape (not size) as the main semantic encoder.

## Clutter-reduction flags — depends on your layout family

| Flag | What it does | Narrative packs | Kitchen-sink/ATM packs |
|---|---|---|---|
| `hide_until_deps_visible: true` | Quest (and its lines) stay **hidden** until its dependencies are visible/complete | **Primary lever** — on most branch/leaf quests in chapters >~30 quests (~25% of quests in a polished 80-quest chapter) | Rare — only on gating/secret quests (~3% of ATM10) |
| `hide_dependency_lines: true` | Hides only the dependency *lines* (quest stays visible) | Surgically on specific crossing edges | **Primary lever** — ATM10 uses ×438; on hubs with >3 dependents and long cross-column lines |
| `hide_dependent_lines: true` | Hides lines from this quest TO its dependents | Surgical | Surgical, rare |
| `secret: true` | Quest is hidden until discovered | Hidden/bonus quests; pair with `rsquare` shape, `size: 1.5` | Rare (ATM10 uses ×0); kitchen-sinks prefer `optional` (×553) |

**Rule of thumb:** narrative/story chapters → `hide_until_deps_visible` first. Kitchen-sink/catalog chapters → `hide_dependency_lines` first. Both can coexist in the same book (different chapters, different families).

## Shape & size = semantic encoding (read importance at a glance)

| Shape | Meaning | Typical size | ATM usage pattern |
|---|---|---|---|
| `gear` | Create machine milestone (big moments) | 2.0 | Hub/section leader (avg 1.75) |
| `square` | Stat/advancement-based sub-hub | 2.0 | Sub-hub, variant grouping |
| `circle` | Small intermediate step | 1.0 | Default — leaf/intermediate (most common) |
| `rsquare` | Secret or special optional | 1.5 | Recipe cells, optional content (ATM: 26% of explicit shapes) |
| `pentagon` | A tier/variant in a parallel set | 1.0 | Capstone convergence node (ATM Star `size 5.0`) |
| `hexagon` | Cross-chapter `quest_links` only | 2.0 | Mid-tier connector, cross-link (ATM: 4%) |
| `diamond` | Special/one-off | 1.0–1.5 | Material-tier identity (ATM Allthemodium `default_quest_shape`) |
| `octagon` | — | 1.0–1.5 | Major branch point (ATM: ~3%, used as tier-gate hub) |

**Size distribution (ATM9/ATM10 combined, 883 quests):** default (1.0) ~70%, 1.2–1.25 ~15%, 1.5 ~5%, 2.0+ ~2%. Kitchen-sinks use size more conservatively than curated packs (Create: Delight peaks at 2.0 for hubs).

**Note — diamond as category marker:** when a chapter uses diamond shapes on independent quests with no fan-in (e.g. 12 structures to find), it's a semantic category marker, not topological convergence. Classify as `parallel_columns`, not `diamond_convergence`. See `topology-coordinates.md` Case 45.

## Coordinate conventions

- Coordinates are **per-chapter-local** (negative used freely; chapter sits at any global offset).
- Typical 80-quest narrative bounds: x ~29, y ~15 (aspect ~2:1).
- y-step between branch rows: 2.5–3.0 (narrative), 0.5–1.5 (catalog).
- Narrative: x-step 3.5, hub radius ≤2.5, dependents within ~2.5 hub radius, shared y-lanes.
- Main path left-to-right (`x` +1.0/step in scaffold, `y` flat), side branches offset (`y` ±1.0), spacing ~1.0, `size: 1.0`.
- Shapes in scaffold: main = `circle`, optional = `square`, boss/key = `hexagon`/`diamond`.

## Side quests & secrets — push to the periphery

Place secrets/schematics/links at chapter margins (large |y| or far x). Full guidance: `design-guide.md §layout-reasoning`.

## Anti-patterns to avoid

Long diagonals, stacking (overlapping nodes), crossing dependency lines, unbounded fan-out, all-lines-visible, y-scatter, mixing layout families in one chapter — full descriptions: `design-guide.md §layout-reasoning`. Collision detection + correction algorithm (R58): `topology-coordinates.md §Phase 4` + `progression-rules.md §Section B`.

## Chapter grouping & visual hierarchy

Tabs (`chapter_groups`), icons, semantic color, progressive-reveal UX — full guidance: `design-guide.md §layout-reasoning`. Quick rules: group ~5–8 chapters/tab; every chapter gets an `icon`; `hide_until_deps_visible` is the progressive-reveal lever above ~30 quests/chapter; `quest_links` (hexagon) for cross-listing, not duplicates.

## Reading direction

Chinese-language tree_branching chapters typically use vertical top-to-bottom reading direction (root at top, progression flows downward), consistent with Chinese text layout conventions. English-language packs usually flow left-to-right. When generating for a Chinese-language pack, consider top-to-bottom as the default primary axis. (Based on 1 Chinese case — additional packs needed to confirm.)
