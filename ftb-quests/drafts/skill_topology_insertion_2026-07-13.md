# Draft: Step 3 Topology Coordinates Template Reference Guide

> **Date:** 2026-07-13
> **Target:** SKILL.md Step 3 (scaffold stage)
> **Risk:** MEDIUM — adds mandatory reference loading during scaffold; may increase Step 3 token spend but prevents topology misclassification
> **Cycle:** 13

---

## Insertion Point: After the existing "Topology-aware layout (Cycle 11)" paragraph

**Location:** SKILL.md line ~379, after the topology formula list ending with "diamond_convergence: sin-curve spread `x_spread = 3.0 + path_length * 0.5`" and before "Do NOT attempt collision detection during scaffold" (line ~380).

**Insert the following text AFTER the diamond_convergence formula line and BEFORE the `Do NOT attempt collision detection` line:**

```markdown
**Topology type selection — mandatory reference loading (Cycle 13):**

Before assigning coordinates in Step 3 scaffold, **read `reference/design/topology-coordinates.md` Phase 2** (Topology Classification) to classify each chapter's topology from its outline structure (quest count, depth, fan-out, convergence ratio). The classification determines which coordinate assignment strategy (Phase 3) and constraint formulas (Layer 2) apply.

**Pack-type → topology recommendations:** Use the following as starting recommendations, then confirm with the classification algorithm from Phase 2:

| pack_type | chapter_type | Recommended topology | Rationale |
|---|---|---|---|
| **skyblock** | getting_started / tutorial | `perpendicular_branch` (variant of `hub_fan`) | Skyblock openers branch from a single resource tree (sieving/farming/crystal) into mod-specific sub-chains; perpendicular layout separates resource paths visually |
| **skyblock** | mod progression | `linear_chain` or `parallel_columns` | Skyblock mod chains are typically linear (mesh tier → machine → upgrade) or parallel (sieving path vs farming path) |
| **expert** | main progression | `highway_branch` or `tree_branching` | Expert packs have a long horizontal spine (voltage tiers, age progression) with vertical branches into sub-systems; highway_branch matches the GTNH/Monifactory staircase pattern |
| **expert** | capstone / endgame | `diamond_convergence` | Expert endgame converges multiple parallel chains into a single capstone (Gregstar, ATM Star variant) |
| **adventure** / **rpg** | hub chapter | `hub_fan` | Adventure hubs (town, base camp) radiate into dungeon/boss/exploration branches; hub_fan matches the radial dungeon-crawl pattern |
| **adventure** / **rpg** | dungeon / boss chain | `linear_chain` | Boss progression is typically sequential (Naga → Lich → Hydra); linear chain enforces the tier-gated order |
| **farming** / **lifestyle** | recipe catalog | `grid_catalog` | Farming packs present large recipe collections (cooking, crafting) as scannable grids; grid_catalog matches the trophy-case layout |
| **farming** / **lifestyle** | seasonal progression | `linear_chain` with `parallel_columns` overlay | Seasonal progression follows spring→summer→autumn→winter as a linear chain, with parallel columns for concurrent crop/cooking/trading tracks |
| **kitchen-sink** | per-mod chapter | `hub_fan` or `highway_branch` | Kitchen-sink mod chapters have a central concept (the mod's key machine) with branches into sub-systems |
| **kitchen-sink** | capstone chapter | `diamond_convergence` | ATM-style capstone pulls one component per mod into a convergence point |

**Calibration cases (Cycle 13 Phase 2):** For skyblock and adventure pack layouts, cross-reference against the following real-pack cases from `reference/design/topology-coordinates.md`:

| Case | Pack | Chapter | Topology | Key data point |
|---|---|---|---|---|
| Case 21 | ATM9-Sky | getting_started | perpendicular_branch | Skyblock opener: single-root sieve chain branching into ore processing + farming + mob farm |
| Case 22 | ATM6-Sky | progression | linear_chain | Compact skyblock progression: 18 quests, depth 12, strict linear mesh-tier gating |
| Case 23 | Dragoncraft | the_beginning | hub_fan | Adventure hub: town center radiating into 5 dungeon branches, fan-out 5 |
| Case 24 | Life-in-the-Village-4 | farming | grid_catalog + linear | Farming catalog: 3-row grid of crop recipes with a linear seasonal progression spine |
| Case 25 | Ragnamod_VII | skyblock_main | parallel_columns | Multi-path skyblock: 4 parallel resource columns (sieve, farm, mob, crystal) |
| Case 26 | Gregitsky | expert_skyblock | highway_branch | Expert skyblock: horizontal voltage-tier spine with vertical processing branches |
| Case 27 | Rogue Mayhem | adventure_rpg | hub_fan + linear_chain | Adventure RPG: town hub (fan-out 4) with linear dungeon chains per branch |

Load the full case data from `reference/design/topology-coordinates.md` to compare your scaffold's quest count, depth, and fan-out against these real-pack baselines. If your chapter's metrics deviate significantly from the matching case (e.g., quest count 2× higher, fan-out 3× larger), reconsider the topology choice or split the chapter.

**Topology-per-chapter, not per-book:** Different chapters in the same pack typically use different topologies (as shown in Cases 23+27 where the same adventure pack uses hub_fan for the town chapter and linear_chain for dungeon chapters). Classify and assign topology per-chapter during scaffold.
```

---

## Risk Assessment

| Risk | Level | Explanation |
|---|---|---|
| Behavioral change | **MEDIUM** | Adds a mandatory reference-loading step to Step 3; previously topology selection was done in Step 2 interview and Step 3 just applied coordinates |
| False positive risk | **LOW** | The recommendations are starting points, not hard rules; the Phase 2 classification algorithm is the authority |
| Backward compatibility | **LOW** | The insertion is additive — existing topology-aware layout (Cycle 11) logic is unchanged |
| Integration with Step 2 | **LOW** | Step 2 already collects topology preference per chapter; this insertion provides the reference data to validate that choice during scaffold |
| Token impact | **MEDIUM** | Loading topology-coordinates.md Phase 2 + Cases 21-27 adds ~200 lines of reference reading per scaffold pass |

## Dependencies

- `reference/design/topology-coordinates.md` must contain Cases 21-27 with the data described above. If cases are numbered differently in the actual file, adjust the case numbers accordingly.
- The `pack_type` field must be collected in Step 2 (same dependency as Draft 1).
