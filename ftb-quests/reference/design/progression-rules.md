# FTB Quests — Progression Rules (Active)

> **Status:** Active | **Cycle:** 19 | **Updated:** 2026-07-19
> **Supersedes:** `progression-rules.archive.md` (R1–R54 remain authoritative in their modular homes; this file is the topology-aware overlay)
> **Purpose:** Provide executable validation rules for AI-generated quest configurations, with special emphasis on the intersection between dependency-graph topology and visual layout.

This file contains two sections. The first distills the core rules from R1–R54 into a quick-reference map — it does not redefine those rules, which live in the modular files (`mod-item-reachability.md`, `mod-dependency-graph.md`, `mod-reward-design.md`, `mod-teaching-pacing.md`, `mod-description-trust.md`, `mod-system-safety.md`). The second introduces new topology-aware rules (R55–R64), cross-cutting progression integrity rules (R65–R72), genre-specific progression rules (R73–R81), author-interview-derived design principles (R82–R90), community-design-wisdom rules (R91–R100), author-design-practice rules (R101–R105), international-author-design-philosophy rules (R106–R116), and quest-reward-integrity and progression-trigger rules (R125–R130) that close the gap between *what the dependency graph means* and *how the layout looks*, between *what the quest asks* and *what the player can actually do*, between *what the pack genre promises* and *what the quest book delivers*, between *what the author intends* and *what the config actually implements*, between *what experienced pack makers practice* and *what automated tools can validate*, between *what author toolkits enable* and *what the quest config alone enforces*, between *what Chinese and international pack-making traditions each independently discovered* and *what a unified validation framework can check*, and between *what a quest reward claims to give* and *what the player can meaningfully use without breaking progression*.

---

## Section A — Core Rules Quick Reference (R1–R54)

These rules are defined and maintained in their respective modular files. This table is a navigation aid, not a replacement.

### Item Reachability (R1–R4, R42)

| Rule | Name | Module | Step | Severity |
|------|------|--------|------|----------|
| R1 | Dimension-Reachability | mod-item-reachability | S4/S5 | ERROR (linear) / WARNING (flexible) |
| R2 | Tool-Tier Item Reachability | mod-item-reachability | S4/S5 | WARNING |
| R3 | Recipe-Chain Depth vs Dependency-Depth | mod-item-reachability | S4/S5 | WARNING |
| R4 | Pack-Type Stage Boundary | mod-item-reachability | S4/S5 | ERROR (expert) / WARNING (kitchen-sink) |
| R42 | Stage-Internal Item Reachability | mod-item-reachability | S5 | ERROR (expert) / WARNING (kitchen-sink) |

### Dependency Integrity (R5–R9, R36, R39, R43, R48)

| Rule | Name | Module | Step | Severity |
|------|------|--------|------|----------|
| R5 | Circular Dependency Detection | mod-dependency-graph | S4/S5 | ERROR |
| R6 | Unreachable Quest Detection | mod-dependency-graph | S5 | ERROR |
| R7 | Optional-Gate-Mandatory Check | mod-dependency-graph | S4/S5 | ERROR |
| R8 | Dependency Requirement Consistency | mod-dependency-graph | S5 | WARNING |
| R9 | Dependency Depth Reasonableness | mod-dependency-graph | S5 | WARNING |
| R36 | Dependency Root Isolation | mod-dependency-graph | S5 | WARNING |
| R39 | Guide Quest Deduplication | mod-dependency-graph | S5 | INFO |
| R43 | Stage-Quest Causal Chain Acyclic | mod-dependency-graph | S5 | ERROR |
| R48 | Quest Port Drift Adaptation Checklist | mod-dependency-graph | S5 | INFO |

### Reward Continuity (R10–R13, R31, R33–R34, R37–R38, R44–R46, R50–R51, R54)

| Rule | Name | Module | Step | Severity |
|------|------|--------|------|----------|
| R10 | Reward-to-Dependent Bridge | mod-reward-design | S4/S5 | WARNING |
| R11 | Reward-Target Accuracy | mod-reward-design | S5 | WARNING |
| R12 | Reward Value Progression | mod-reward-design | S5 | INFO |
| R13 | Capstone Reward Magnitude | mod-reward-design | S5 | WARNING |
| R31 | XP-Level Reward Relativity | mod-reward-design | S4 | WARNING |
| R33 | Reward Table Reference Integrity | mod-reward-design | S5 | ERROR |
| R34 | Reward Type Distribution Report | mod-reward-design | S5 | INFO |
| R37 | Capstone-Only Progression Break | mod-reward-design | S5 | WARNING |
| R38 | Tier Transition Milestone Reward | mod-reward-design | S5 | WARNING |
| R44 | Reward-Stage Matching | mod-reward-design | S5 | ERROR (expert) / WARNING (kitchen-sink) |
| R45 | Reward Guidance Bridging | mod-reward-design | S5 | WARNING |
| R46 | Questbook Role Declaration | mod-reward-design | S5 | INFO |
| R50 | Zero-Reward Design Safety Conditions | mod-reward-design | S5 | WARNING |
| R51 | Reward Architecture Role Alignment | mod-reward-design | S5 | INFO |
| R54 | Named Reward Table Semantic Match | mod-reward-design | S5 | WARNING |

### Teaching Order & Pacing (R14–R22, R40–R41, R47)

| Rule | Name | Module | Step | Severity |
|------|------|--------|------|----------|
| R14 | Teach-Then-Do Ordering | mod-teaching-pacing | S5 | ERROR |
| R15 | Complexity Escalation | mod-teaching-pacing | S5 | INFO |
| R16 | Dimension-Explore-Then-Craft | mod-teaching-pacing | S5 | WARNING |
| R17 | Tool-Reward-Before-Use | mod-teaching-pacing | S5 | WARNING |
| R18 | Description Coverage | mod-teaching-pacing | S4 | WARNING |
| R19 | Bottleneck Spacing | mod-teaching-pacing | S5 | WARNING |
| R20 | Chapter Completion Testability | mod-teaching-pacing | S5 | ERROR |
| R21 | Hidden Quest Signpost | mod-teaching-pacing | S5 | WARNING |
| R22 | Cross-Chapter Dependency Validity | mod-teaching-pacing | S4 | ERROR |
| R40 | Effort Preview in Description | mod-teaching-pacing | S4/S5 | INFO |
| R41 | Early-Game Flexible Progression Mode | mod-teaching-pacing | S5 | INFO |
| R47 | Companion Tool Delegation | mod-teaching-pacing | S5 | INFO |

### Description & Consistency (R23–R26, R49)

| Rule | Name | Module | Step | Severity |
|------|------|--------|------|----------|
| R23 | Description-Item Consistency | mod-description-trust | S4 | ERROR |
| R24 | Suggestion-Reachability | mod-description-trust | S4/S5 | WARNING |
| R25 | Task-Item Necessity | mod-description-trust | S5 | INFO |
| R26 | Quest-Mod Version Consistency | mod-description-trust | S4/S5 | INFO |
| R49 | Collection-Catalog Maintenance Cost | mod-description-trust | S5 | INFO |

### Safety & QA (R28–R30, R32, R35, R52–R53)

| Rule | Name | Module | Step | Severity |
|------|------|--------|------|----------|
| R28 | Command Reward Safety Scan | mod-system-safety | S4 | ERROR/WARNING |
| R29 | Team Progression Consistency | mod-system-safety | S5 | WARNING |
| R30 | Quest Visual Hierarchy & Size Consistency | mod-system-safety | S5 | WARNING |
| R32 | Chapter QA Coverage Heuristic | mod-system-safety | S5 | INFO |
| R35 | Shape Semantics Consistency Within Pack | mod-system-safety | S5 | INFO |
| R52 | Unlock Leniency Declaration | mod-system-safety | S5 | INFO |
| R53 | Task Complexity Utility Proportionality | mod-system-safety | S5 | INFO |

---

## Section B — Topology-Aware Layout Rules (R55–R64)

These rules bridge the gap between the dependency-graph topology (what kind of structure the quest chain forms) and the visual layout (where quests appear on the canvas). They exist because the topology-coordinates research (Cycle 11 Phase 1–2) revealed that layout quality is an implicit expectation: players feel when a quest book is "well-organized" even if they can't articulate why, and the seven topology types each have distinct layout constraints that, when violated, produce layouts that are confusing, overlapping, or misleading.

### R55 — Topology-Progression Mode Alignment

**Applicable when:** A chapter has been classified into one of the seven topology types (linear_chain, hub_fan, parallel_columns, diamond_convergence, tree_branching, grid_catalog, highway_branch) and the chapter or book has a `progression_mode` setting.

**Check:** The topology type should be compatible with the progression mode. Linear_chain and tree_branching imply sequential advancement — they work best with `default` or `linear` progression. Hub_fan and parallel_columns imply branching choice — they are most natural under `flexible` progression. Grid_catalog implies no ordering — it is only appropriate under `flexible`. Diamond_convergence works with either mode but is more powerful under `default` (where the convergence point creates a genuine narrative climax). Highway_branch implies a horizontal spine with optional branches — it works with `default` (forced spine progression) or `flexible` (branches available in any order).

```
TOPOLOGY_MODE_ALIGNMENT = {
    "linear_chain":       ["default", "linear"],
    "hub_fan":            ["flexible", "default"],
    "parallel_columns":   ["flexible"],
    "diamond_convergence":["default", "flexible"],
    "tree_branching":     ["default", "linear"],
    "grid_catalog":       ["flexible"],
    "highway_branch":     ["default", "flexible"],
}

for each chapter C:
    topology = classify_topology(C.quests)
    mode = C.progression_mode or C.book.progression_mode
    allowed = TOPOLOGY_MODE_ALIGNMENT.get(topology, [])
    if mode not in allowed:
        WARNING: "Chapter {C.name} uses {topology} topology with
                  {mode} progression. This combination may confuse players:
                  {topology} implies {implied_experience}, but {mode}
                  progression allows {allowed_experience}."
```

**R41 conflict resolution (Early-Game Flexible vs Topology Alignment):** R41 recommends that early-game and tutorial chapters use `flexible` progression mode to reduce friction for new players. This can conflict with R55 when an early-game tutorial chapter uses `linear_chain` topology — R55 expects `default` or `linear` for linear chains, but R41 recommends `flexible` for early-game. **Resolution:** when a chapter is tagged as early-game/tutorial (depth ≤ 3, quest count ≤ 15, or explicitly marked `order_index == 0`) AND uses `flexible` mode with `linear_chain` topology, this is an **intentional override**, not a violation. In this case, R55 should downgrade its WARNING to INFO with the note: "Early-game flexible mode (R41) overrides linear_chain alignment. Players can explore the tutorial chain in any order, which is acceptable for introductory content." This pattern appears in ATM-10's `basic_tools` chapter (6 quests, flexible mode, linear_chain topology — the player picks up tools in any order despite the chain's visual suggestion of sequence).

**Violation consequence:** A linear_chain under `flexible` mode lets players skip ahead past the chain's intended sequence, breaking the tutorial pacing that the chain was designed to enforce. A hub_fan under `linear` mode forces players to complete all branches sequentially when the layout visually suggests they could pick any branch — the visual affordance contradicts the mechanical gate. *Exception:* the R41 early-game override described above.

**Source:** topology-coordinates.md Phase 2 classification; design-guide.md §principles F1 ("Guidance and gating are two mechanisms; decouple them"); ATM-10's use of `flexible` with hub_fan topologies vs Monifactory's `default` with tree_branching.

---

### R56 — Depth-Axis Monotonicity

**Applicable when:** A chapter has been classified as linear_chain, tree_branching, or diamond_convergence, and the layout algorithm has assigned coordinates to all quests.

**Check:** The primary layout axis should show monotonic increase in dependency depth. For vertical layouts (y increases downward), quests at greater dependency depths should have larger y values. For horizontal layouts (x increases rightward), greater depth should map to larger x values. Occasional same-depth nodes at the same coordinate are acceptable (parallel branches), but depth should never *decrease* along the primary axis.

```
for each chapter C:
    topology = classify_topology(C.quests)
    if topology not in ("linear_chain", "tree_branching", "diamond_convergence"):
        continue

    primary_axis = "y" if topology in ("linear_chain", "tree_branching") else "x"
    depth_map = compute_depth(C.quests)

    violations = []
    for q1, q2 in all_quest_pairs(C):
        if depth_map[q1] < depth_map[q2]:
            # q2 is deeper — it should be further along primary axis
            if q2[primary_axis] < q1[primary_axis] - 1.0:
                violations.append((q1, q2))

    if violations:
        WARNING: "Chapter {C.name} has {len(violations)} depth-inversion pairs
                  where a deeper quest appears before a shallower one on the
                  primary layout axis. Players read top-to-bottom (or left-to-right)
                  and expect later content to appear later visually."
```

The 1.0-unit tolerance exists because zigzag layouts (like ATM-10 basic_tools) alternate x slightly while y progresses, and minor coordinate noise should not trigger false positives. The Monifactory progression chapter demonstrates perfect depth-axis monotonicity: its diagonal staircase (x from -9.5 to 4.5, y from -5.5 to 10.5) maps each depth increment to both +1.5 x and +1.5 y, so depth is monotonically increasing on both axes simultaneously.

**Violation consequence:** A quest at depth 8 appears above a quest at depth 3 on the canvas. Players scrolling top-to-bottom encounter endgame content before mid-game content. The visual reading order contradicts the dependency order, forcing players to constantly cross-reference the dependency arrows rather than following a natural visual flow.

**Source:** topology-coordinates.md Case 6 (Monifactory progression diagonal staircase, step Δx=1.5, Δy=1.5); Case 8 (Finality Genesis cataclysm, y-step 1.5 monotonic); Case 1 (ATM-10 basic_tools, diagonal down-left with consistent y decrease).

---

### R57 — Hub Node Size Dominance

**Applicable when:** A chapter contains hub nodes (fan_out >= 3) and the layout algorithm has assigned size values to all quests.

**Check:** A hub node's size must be strictly greater than the size of any quest that directly depends on it. This ensures that when a player looks at the quest book, the hub visually dominates its children — the size hierarchy mirrors the dependency hierarchy. The rule extends to convergence nodes (fan_in >= 3): a convergence node should be at least as large as the largest of its parent quests.

```
for each quest Q:
    if Q.fan_out >= 3:  # hub node
        children = find_direct_children(Q)
        max_child_size = max(c.size for c in children) if children else 0
        if Q.size <= max_child_size:
            WARNING: "Hub quest {Q.name} (size {Q.size}, fan_out {Q.fan_out})
                      is not larger than its largest child (size {max_child_size}).
                      Hub nodes should visually dominate their dependents."

    if Q.fan_in >= 3:  # convergence node
        parents = find_direct_parents(Q)
        max_parent_size = max(p.size for p in parents) if parents else 0
        if Q.size < max_parent_size:
            INFO: "Convergence quest {Q.name} (size {Q.size}, fan_in {Q.fan_in})
                   is smaller than its largest parent (size {max_parent_size}).
                   Consider increasing size to signal synthesis importance."
```

**Violation consequence:** When a hub node is the same size as its leaves, the player cannot tell at a glance which node is the organizational center. The ATM-10 basic_power chapter demonstrates correct hub dominance: root (gear, size 2.0) → sub-hubs (hexagon, size 1.5) → leaves (rsquare, size 1.0). The three-tier size hierarchy makes the tree structure immediately legible. Monifactory groundwork follows the same pattern: size 2.0 (3 root/milestone quests) → size 1.5 (8 sub-hubs) → size 1.0–1.25 (86 standard nodes).

**Source:** topology-coordinates.md Case 3 (ATM-10 basic_power, 3-tier size hierarchy); Case 5 (Monifactory groundwork, 3-tier hierarchy); Case 11 (ATM-10 create, root size 3.0 dominates all 205 children); design-guide.md §principles P3 ("the endgame node is the visual center and the biggest thing on the canvas").

---

### R58 — Collision-Free Adjacent Nodes

**Applicable when:** Layout coordinates have been assigned to all quests in a chapter.

> **Execution scope: Validation Only (Step 5).** R58 is a post-generation validation check — it must NOT be called during quest generation (Step 4). The all-pairs distance calculation and iterative push-apart loop in `topology-coordinates.md` Phase 4 require precise floating-point arithmetic that LLM agents cannot reliably perform. During generation, collisions are prevented by using the topology-specific spacing formulas from Phase 3 (y_spacing, column_x_gap, hub_radius, etc.), which produce inherently well-spaced layouts. R58 catches any residual overlaps that the spacing formulas miss, and reports them for manual correction.

**Check:** Every pair of quests must maintain a minimum center-to-center distance that accounts for both quests' sizes. The minimum distance is the sum of the two quests' effective radii (size × 0.5 for standard shapes, size × 0.35 for "none" shape which renders as a dot) plus a gap of at least 0.25 units. This prevents quest nodes from overlapping visually, which would make the quest book unreadable at default zoom.

```
MIN_GAP = 0.25  # minimum visual gap between quest edges

for each pair (q1, q2) in chapter:
    dist = sqrt((q1.x - q2.x)^2 + (q1.y - q2.y)^2)
    r1 = effective_radius(q1)  # size * 0.5 (or size * 0.35 for shape "none")
    r2 = effective_radius(q2)
    min_distance = r1 + r2 + MIN_GAP
    if dist < min_distance:
        ERROR: "Quests {q1.name} and {q2.name} overlap: center distance
                {dist:.2f} < required {min_distance:.2f}. Increase spacing
                or reduce quest sizes."
```

For diagonal neighbors (neither purely horizontal nor purely vertical), the diagonal bonus of 0.85 applies — diagonal distance is naturally perceived as longer, so a 15% reduction in minimum distance is acceptable. This explains the zigzag in ATM-10 basic_tools: quests alternate x by 0.5 while y decreases by 0.5, giving a diagonal distance of √(0.5² + 0.5²) ≈ 0.71, which is within the diagonal-toleranced minimum for size-1.0 quests (effective radius 0.5 + 0.5 + 0.25 = 1.25 normally, but 1.25 × 0.85 ≈ 1.06 for diagonal — still requires some spacing adjustment, hence the compact diagonal layout).

**Violation consequence:** Overlapping quest nodes are the most basic layout failure. Players cannot distinguish adjacent quests, cannot click the intended quest, and the dependency lines become a tangled mess. This is the first thing any player notices and the hardest to recover trust from.

**Source:** topology-coordinates.md Phase 4 collision detection algorithm; Case 1 (ATM-10 basic_tools diagonal zigzag); Phase 2 spacing formulas (minimum_center_distance = 1.0, preferred = 1.5).

---

### R59 — Bounding Box Viewport Fit

**Applicable when:** All quests in a chapter have been assigned coordinates.

**Check:** The chapter's bounding box (the rectangle enclosing all quest positions, padded by the largest quest's size on each side) should fit within the FTB Quests default viewport at standard zoom level. The observed maximum comfortable viewport is approximately 35 units wide and 30 units tall (based on FTB Evolution's create chapter reaching x=30.0 and RAD3's pathfinder spanning 13 units vertically). Chapters wider than 35 units force excessive horizontal scrolling; chapters taller than 30 units force excessive vertical scrolling.

```
MAX_WIDTH = 35.0   # FTB Evolution create reached x=30.0, leaving 5 units margin
MAX_HEIGHT = 30.0  # Monifactory progression spans 16 units vertically, comfortable
PADDING = 1.0      # viewport padding on each side

for each chapter C:
    min_x = min(q.x - q.size/2 for q in C.quests)
    max_x = max(q.x + q.size/2 for q in C.quests)
    min_y = min(q.y - q.size/2 for q in C.quests)
    max_y = max(q.y + q.size/2 for q in C.quests)

    width = (max_x - min_x) + 2 * PADDING
    height = (max_y - min_y) + 2 * PADDING

    if width > MAX_WIDTH:
        WARNING: "Chapter {C.name} spans {width:.1f} units wide
                  (max recommended: {MAX_WIDTH}). Consider splitting into
                  sub-chapters or compressing the layout."
    if height > MAX_HEIGHT:
        WARNING: "Chapter {C.name} spans {height:.1f} units tall
                  (max recommended: {MAX_HEIGHT}). Consider a more compact
                  topology or splitting into sub-chapters."
```

The MM2 botania chapter (27.5 × 17 units) and FTB Evolution create (30 × 12 units) are at the upper edge of comfortable width. The Monifactory progression chapter (14 × 16 units) and ATM-10 create (13 × 17 units) are within bounds. Craftoria's create chapter is the extreme outlier at 123 quests spread across a 30-unit width — it compensates with `default_quest_shape: "none"` to reduce visual clutter.

**Violation consequence:** Players must scroll extensively to see the full chapter, losing their spatial orientation. The quest book ceases to function as a visual map and becomes a scrollable list with extra steps. This is especially damaging in hub_fan layouts where the player needs to see the hub and all branches simultaneously to understand the structure.

**Source:** topology-coordinates.md Phase 6 finalize_layout (viewport clamping); Case 13 (FTB Evolution create, x=30.0); Case 10 (MM2 botania, 27.5 × 17 units).

---

### R60 — Topology-Shape Vocabulary Coherence

**Applicable when:** A chapter's topology has been classified and shape assignments have been made.

**Check:** The shape vocabulary used within a chapter should be coherent with the chapter's topology type. Hub_fan and tree_branching topologies benefit from at least 3 distinct shapes to differentiate root/hub, intermediate, and leaf nodes. Grid_catalog topologies should use at most 2 shapes (or shape "none" uniformly) to minimize visual noise. Linear_chain topologies can use 1–2 shapes comfortably. Diamond_convergence benefits from a distinctive shape at the convergence point.

```
TOPOLOGY_SHAPE_GUIDELINES = {
    "linear_chain":        {"min_shapes": 1, "max_shapes": 3,
                            "required_roles": []},
    "hub_fan":             {"min_shapes": 2, "max_shapes": 5,
                            "required_roles": ["hub", "leaf"]},
    "parallel_columns":    {"min_shapes": 1, "max_shapes": 3,
                            "required_roles": []},
    "diamond_convergence": {"min_shapes": 2, "max_shapes": 4,
                            "required_roles": ["convergence"]},
    "tree_branching":      {"min_shapes": 2, "max_shapes": 5,
                            "required_roles": ["root", "leaf"]},
    "grid_catalog":        {"min_shapes": 1, "max_shapes": 2,
                            "required_roles": []},
}

for each chapter C:
    topology = classify_topology(C.quests)
    shapes_used = set(q.shape for q in C.quests if q.shape)
    guidelines = TOPOLOGY_SHAPE_GUIDELINES.get(topology, {})

    if len(shapes_used) > guidelines.get("max_shapes", 99):
        INFO: "Chapter {C.name} ({topology}) uses {len(shapes_used)} distinct
               shapes. Consider simplifying — too many shapes in a
               {topology} layout creates visual noise rather than clarity."

    if len(shapes_used) < guidelines.get("min_shapes", 0):
        WARNING: "Chapter {C.name} ({topology}) uses only {len(shapes_used)}
                  shapes. {topology} layouts benefit from at least
                  {guidelines['min_shapes']} shapes to differentiate node roles."
```

The GT-Odyssey stoneage chapter (52 quests, 7 shape types) demonstrates the richest shape vocabulary in the dataset — each shape maps to a distinct structural role (gear=hubs, hexagon=tech, diamond=processing, pentagon=upgrades, octagon=milestones, circle=optional). This works because the chapter is small enough that shape variety compensates for low quest count. The ATM-10 create chapter (206 quests, 3 explicit shapes) takes the opposite approach — large chapters rely on coordinate placement and decorative images rather than shape diversity.

**Violation consequence:** Using only one shape in a hub_fan chapter makes it impossible to visually distinguish the hub from its leaves. Using 7 shapes in a grid_catalog chapter with 63 quests (like RAD3 milestones) would create overwhelming visual noise when the chapter's purpose is simply to display a trophy case. Shape diversity and chapter complexity have an inverse relationship — shape variety is a tool for small chapters to signal structure.

**Source:** topology-coordinates.md Case 12 (GT-Odyssey stoneage, 7 shapes/52 quests); Case 11 (ATM-10 create, 3 shapes/206 quests); Cross-Pack Key Observations (shape diversity inversely correlates with quest count).

---

### R61 — Convergence Point Visual Prominence

**Applicable when:** A chapter contains convergence nodes (fan_in >= 2) and layout coordinates have been assigned.

**Check:** Convergence nodes should be positioned at a coordinate that makes them visually prominent — typically at the bottom of a diamond, the center of a hub, or the rightmost point of a horizontal chain. The convergence node's position should be reachable by following the visual flow from any of its parent branches. Specifically, a convergence node's y-coordinate should be greater than (below) at least 80% of its parents in vertical layouts, or its x-coordinate should be greater than (to the right of) at least 80% of its parents in horizontal layouts.

```
for each quest Q:
    if Q.fan_in < 2:
        continue
    parents = find_direct_parents(Q)
    if not parents:
        continue

    # Determine layout direction from parent spread
    parent_y_spread = max(p.y for p in parents) - min(p.y for p in parents)
    parent_x_spread = max(p.x for p in parents) - min(p.x for p in parents)
    is_horizontal = parent_x_spread > parent_y_spread

    if is_horizontal:
        below_threshold = sum(1 for p in parents if Q.x >= p.x)
        ratio = below_threshold / len(parents)
    else:
        below_threshold = sum(1 for p in parents if Q.y >= p.y)
        ratio = below_threshold / len(parents)

    if ratio < 0.8:
        WARNING: "Convergence quest {Q.name} (fan_in {Q.fan_in}) is not
                  positioned at the natural visual endpoint of its parent
                  branches. Players may not perceive it as the synthesis point."
```

ATM-10's allthemodium chapter demonstrates correct convergence positioning: the diamond convergence quest at (10.5, -5.0) sits below both the upper branch (y ≈ 3.0–4.5) and the lower branch (y ≈ -2.5), creating a visual "pull" downward toward the chapter's capstone. The x-coordinate (10.5) is roughly centered between the two branches (upper: x ≈ 3.5–14, lower: x ≈ 3.5–21), reinforcing its role as the meeting point.

**Violation consequence:** A convergence node positioned above or to the left of its parents breaks the visual flow — the player's eye naturally moves downward or rightward through the chapter, and a convergence point that sits "behind" the flow is easily missed. The player may complete all parent branches without realizing there's a synthesis quest waiting.

**Source:** topology-coordinates.md Case 4 (ATM-10 allthemodium, convergence at (10.5, -5.0)); Phase 3 diamond_convergence coordinate assignment algorithm.

---

### R62 — Parallel Column Spacing Uniformity

**Applicable when:** A chapter has been classified as parallel_columns topology.

**Check:** All columns in a parallel_columns layout should have uniform x-spacing (within a tolerance of ±0.5 units) and consistent y-start and y-spacing values. Uniformity is what makes parallel columns readable — the player can scan across columns at the same y-level to compare equivalent progression steps. Irregular spacing breaks this scanning pattern.

```
COLUMN_SPACING_TOLERANCE = 0.5

for each chapter C:
    topology = classify_topology(C.quests)
    if topology != "parallel_columns":
        continue

    columns = group_by_root(C.quests)
    if len(columns) < 2:
        continue

    # Check x-spacing uniformity
    column_centers = [mean(q.x for q in col) for col in columns]
    spacings = [column_centers[i+1] - column_centers[i]
                for i in range(len(column_centers)-1)]
    avg_spacing = mean(spacings)
    max_deviation = max(abs(s - avg_spacing) for s in spacings)

    if max_deviation > COLUMN_SPACING_TOLERANCE:
        WARNING: "Chapter {C.name} has non-uniform column spacing
                  (max deviation: {max_deviation:.2f} units from mean
                  {avg_spacing:.2f}). Parallel columns should be evenly
                  spaced for visual scanning."

    # Check y-start consistency
    column_starts = [min(q.y for q in col) for col in columns]
    start_range = max(column_starts) - min(column_starts)
    if start_range > 1.0:
        INFO: "Chapter {C.name} columns start at different y-levels
               (range: {start_range:.2f}). Consider aligning column starts
               for a cleaner visual entry."
```

ATM-10's bounty_board is the cleanest parallel_columns example: 3 columns at x=-7.0, x=-5.0, x=-3.0 (exactly 2.0 spacing), all starting at y=-2.5, with consistent 1.5 y-spacing between kill tiers. This regularity makes the bounty board instantly scannable — the player sees three columns of identical height with matching kill-count tiers at each y-level.

**Violation consequence:** Non-uniform column spacing makes it impossible for the player to scan across columns at the same progression level. If one column is offset by 1 unit vertically, the kill-50 tier in column 1 sits at a different height than kill-50 in column 2, and the player cannot compare them without mentally re-aligning.

**Source:** topology-coordinates.md Case 2 (ATM-10 bounty_board, 2.0 column spacing, consistent y-start); Phase 3 parallel_columns coordinate assignment.

---

### R63 — Grid Catalog Aspect Ratio

**Applicable when:** A chapter has been classified as grid_catalog topology.

**Check:** Grid catalog chapters should have an aspect ratio (width:height) between 1:1 and 3:1. Ratios beyond 3:1 (extremely wide and short) produce a layout that requires excessive horizontal scrolling with minimal vertical context. Ratios below 1:1 (extremely tall and narrow) defeat the purpose of a grid layout, which is to present items in a scannable 2D arrangement.

```
MIN_ASPECT_RATIO = 1.0   # square
MAX_ASPECT_RATIO = 3.0   # wide rectangle

for each chapter C:
    topology = classify_topology(C.quests)
    if topology != "grid_catalog":
        continue

    width = max(q.x for q in C.quests) - min(q.x for q in C.quests)
    height = max(q.y for q in C.quests) - min(q.y for q in C.quests)
    if height == 0:
        continue

    aspect = width / height
    if aspect > MAX_ASPECT_RATIO:
        WARNING: "Chapter {C.name} (grid_catalog) has aspect ratio {aspect:.1f}:1
                  (too wide). Consider adding more rows or reducing columns."
    elif aspect < MIN_ASPECT_RATIO:
        WARNING: "Chapter {C.name} (grid_catalog) has aspect ratio 1:{1/aspect:.1f}
                  (too tall). A grid layout should be wider than tall for
                  comfortable scanning."
```

RAD3's milestones chapter (13.0 × 5.0, aspect 2.6:1) sits comfortably within the guideline. The 3-row × multi-column grid is scannable without excessive scrolling. A grid with aspect ratio 5:1 (like 30 × 6) would force the player to scroll horizontally through a narrow strip — defeating the grid's purpose as a compact trophy case.

**Violation consequence:** An excessively wide grid forces horizontal scrolling through a thin strip, losing the "spreadsheet at a glance" quality that makes grid catalogs useful. An excessively tall grid is just a single-column list with extra visual overhead.

**Source:** topology-coordinates.md Case 7 (RAD3 milestones, 13.0 × 5.0, aspect 2.6:1); Phase 3 grid_catalog coordinate assignment (columns = ceil(sqrt(quest_count))).

---

### R64 — Decorative Image Topology Alignment

**Applicable when:** A chapter uses decorative images (the `images` array in the chapter SNBT) and those images define visual regions that organize quests into compartments.

**Check:** Quest coordinates should fall within the bounds of their intended decorative image compartment, not in the gaps between compartments or outside all compartments. This rule requires that decorative images have known bounding boxes (extractable from the image's x, y, width, height fields) and that the author's compartmentalization intent is inferable from the image placement pattern.

```
for each chapter C:
    if not C.images:
        continue

    image_regions = [
        {"x_min": img.x, "x_max": img.x + img.width,
         "y_min": img.y, "y_max": img.y + img.height,
         "label": img.id or "unnamed"}
        for img in C.images if img.width and img.height
    ]

    if not image_regions:
        continue

    unassigned = []
    for quest in C.quests:
        inside_any = any(
            region["x_min"] <= quest.x <= region["x_max"] and
            region["y_min"] <= quest.y <= region["y_max"]
            for region in image_regions
        )
        if not inside_any:
            unassigned.append(quest)

    if unassigned and len(unassigned) > len(C.quests) * 0.3:
        WARNING: "Chapter {C.name} has {len(unassigned)} quests
                  ({len(unassigned)*100//len(C.quests)}%) outside any
                  decorative image compartment. If compartments are
                  intentional, these quests may be visually orphaned."
```

Craftoria's Create chapter is the canonical example of decorative image compartmentalization: its 8 colored "toolbox compartments" each define a visual region, and quests are placed within their respective compartment. Quests outside all compartments would appear floating in empty space between the toolbox drawers, breaking the visual metaphor.

**Violation consequence:** When decorative images define a visual structure (drawers, panels, shelves, compartments) but quests don't align with that structure, the decorative images become visual noise rather than organizational aids. The player sees a beautifully decorated quest book where the quests don't match the decoration — like labels on empty shelves.

**Source:** topology-coordinates.md Phase 2 (Craftoria Create chapter's 8 toolbox compartments); design-guide.md §field-findings (decorative images for visual compartmentalization).

---

## Section B2 — Cross-Cutting Progression Integrity Rules (R65–R72)

These rules were synthesized from author-facing design documents and community design discussions collected during Cycle 12 Phase 3. Unlike Section B's topology-aware layout rules, these rules operate across all topology types and address the "three hard problems" that recur across every pack archetype: **item cross-tier** (a task demands an item the player cannot yet obtain), **sequence inversion** (advanced instruction appears before basic instruction), and **reward disconnection** (a reward fails to guide the player toward the next logical step). Each rule is tagged with which of the three problems it primarily defends against.

### R65 — Tier-Bridge Equipment Sufficiency

**Primary defense:** 物品跨级 (Item Cross-Tier)

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires access to mod mob-dimension mappings and equipment tier lists that are not available during quest generation. Execute via external validation tool in Step 5. Without external mob/entity spawn data and equipment tier classifications, downgrade to INFO with note: "External data not available — tier-bridge equipment check skipped."

**Applicable when:** A quest requires the player to enter a new dimension, biome, or combat zone for the first time (detected via dimension-visit tasks, biome-visit tasks, or mob-kill tasks targeting entities native to that location).

**Check:** Before the player is expected to enter the new area, they must have access to equipment (armor, weapons, tools) from their current progression tier that is sufficient to survive basic encounters there. "Sufficient" means the player can defeat the area's common mobs (not bosses) and gather basic resources without requiring equipment from a *later* tier. This implements the adventure-pack design principle stated by Chinese modpack authors: "上一个世界的顶端装备对应于这个世界的小怪" (the previous world's top-tier equipment corresponds to this world's basic mobs).

```
for each quest Q:
    for each task T in Q.tasks:
        if T.type in ("dimension_visit", "biome_visit", "entity_kill"):
            target_location = extract_location(T)
            native_mobs = get_native_entities(target_location)
            if not native_mobs:
                continue

            # Find the player's expected equipment tier at this point
            reachable_equipment = find_reachable_equipment(
                quest_chain_up_to(Q),
                pack_type=pack.type
            )
            if not reachable_equipment:
                WARNING: "Quest {Q.name} sends player to {target_location}
                          but no equipment is reachable before this quest.
                          Player may face {native_mobs[0].name} with no
                          adequate gear."
                continue

            best_weapon_tier = max(e.tier for e in reachable_equipment
                                   if e.is_weapon)
            min_mob_tier = min(m.tier for m in native_mobs if m.is_common)

            if best_weapon_tier < min_mob_tier - 1:
                WARNING: "Quest {Q.name} requires entering {target_location}
                          where common mobs are tier {min_mob_tier}, but
                          player's best reachable weapon is tier
                          {best_weapon_tier}. Previous tier should handle
                          basic encounters (tier bridge principle)."
```

The "-1" tolerance allows for packs where entering a new dimension is intentionally challenging (expert packs), but the gap should not exceed one tier. In kitchen-sink packs, the tolerance should be 0 — the player's current equipment should always handle basic mobs in any area they are directed to.

**Violation consequence:** The player arrives in a new dimension and immediately dies to the first mob they encounter, with no way to craft better gear because the materials for that gear are in the dimension they just entered — a classic circular dependency expressed through combat rather than crafting.

**Source:** MC百科 "冒险包设计思路" (adventure pack design ideas) — "难度递进" principle; TheWinterRescue's temperature-gated progression where shelter technology always precedes exposure requirements.

---

### R66 — Cross-Branch Gate Independence

**Primary defense:** 物品跨级 (Item Cross-Tier)

**Applicable when:** A pack has multiple progression branches (e.g., tech, magic, adventure) and the quest book assigns quests to these branches via chapter structure or tag.

**Check:** Basic advancement within any single branch should not require items from another branch's mid-to-late stage. Cross-branch dependencies are acceptable only at convergence points (capstone quests, endgame milestones) or when the dependency is on the other branch's *early* stage (items obtainable within the first 3 quests of that branch). This implements CTNH's design principle: "除最终毕业物品的合成之外，魔法均为可选内容，发展过程中不会出现魔法卡科技的情况" (except for final graduation item crafting, magic is optional; tech progression will not be blocked by magic).

```
BRANCH_GATE_TOLERANCE = 3  # max depth into another branch for a dependency

for each quest Q:
    branch = classify_branch(Q)  # "tech", "magic", "adventure", etc.
    for each task T in Q.tasks:
        if T.type != "item_submit":
            continue
        required_item = T.item
        source_branch = find_primary_branch(required_item)
        if source_branch == branch:
            continue  # same-branch dependency, fine

        source_depth = find_depth_in_branch(required_item, source_branch)
        if source_depth > BRANCH_GATE_TOLERANCE:
            # Check if Q is a convergence/capstone quest
            if Q.is_capstone or Q.fan_in >= 2:
                continue  # cross-branch at convergence is intentional
            WARNING: "Quest {Q.name} ({branch} branch) requires
                      {required_item} from {source_branch} branch at depth
                      {source_depth}. This creates a cross-branch gate:
                      the player must advance deep into {source_branch}
                      to continue in {branch}. Consider making the
                      dependency optional or moving it to a convergence
                      point."
```

**Violation consequence:** The player is deep in the tech tree, following a satisfying progression chain, when suddenly they hit a wall — they need an item from the middle of the magic tree that they have zero context for. The tech branch's flow is broken, and the player must now context-switch to an entirely different playstyle to proceed. CTNH explicitly avoids this: adventure dimensions are required for resources, but "不会出现必须获得某种战利品或必须击败某个boss才能推进科技的情况" (no specific boss loot or kill is required to advance tech).

**Source:** CTNH MC百科 page — cross-branch independence principle; Enigmatica Expert mode's branch design where magic and tech have parallel but independent progressions with convergence only at capstone tiers.

---

### R67 — Weak Lock Bypass Detection

**Primary defense:** 物品跨级 (Item Cross-Tier)

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires access to mod recipe databases (all acquisition paths for a given item) that are not available during quest generation. Execute via external validation tool in Step 5. Without a complete recipe database (e.g., JEI/CraftTweaker export), downgrade to INFO with note: "External data not available — bypass detection is incomplete. Only known bypasses from training data are checked."

**Applicable when:** The pack uses stage gates (hard-coded progression barriers like GameStages locks, voltage tiers, or dimension locks) and a quest's task requires an item that has multiple acquisition paths.

**Check:** If a quest requires an item that is gated behind a stage barrier, but that item (or a functional equivalent) can be obtained through an alternate path that *doesn't* pass through the intended gate, the gate is "leaky." The stage lock principle from Chinese modpack design states: "阶段锁要是一种'弱锁'" (stage locks should be a kind of "weak lock") — meaning bypasses should exist but carry a cost. This rule detects *unintended* bypasses where the cost is trivially low.

```
for each quest Q:
    for each task T in Q.tasks:
        if T.type != "item_submit":
            continue
        required_item = T.item
        intended_stage = get_stage_gate(Q)
        if not intended_stage:
            continue

        all_paths = find_all_acquisition_paths(required_item)
        for path in all_paths:
            if path.bypasses_stage(intended_stage):
                bypass_cost = estimate_path_cost(path)
                intended_cost = estimate_intended_path_cost(intended_stage)
                if bypass_cost < intended_cost * 0.3:
                    WARNING: "Quest {Q.name} requires {required_item}
                              (gated by {intended_stage}), but an alternate
                              path exists at {bypass_cost:.0%} of the
                              intended cost: {path.description}. This
                              weak lock bypass may let players skip the
                              intended stage gate entirely."
```

The 30% threshold is calibrated from the "弱锁" design principle: bypasses should be possible but not trivially cheaper than the intended path. The mcmod.cn design article specifically recommends that bypass items should be "unstable or random" — providing satisfaction for clever players while keeping the main path reliable.

**Violation consequence:** A player discovers they can get a mid-game item through a trivial early-game recipe (e.g., a cross-mod interaction that produces a high-tier material from low-tier inputs). The stage gate becomes meaningless, and the player either accidentally trivializes the mid-game or — worse — they don't realize they bypassed the gate and encounter mid-game content without mid-game preparation.

**Source:** MC百科 "论较高难度、较长寿命整合包的设计与开发" — "弱锁" (weak lock) principle; "奖励bypass" concept where bypass items are "unstable or random"; ATM-10 discussion #3539 where players note "arbitrary progression steps being skipped for no reason" via quest rewards.

---

### R68 — Mod First-Appearance Teaching Precedence

**Primary defense:** 顺序倒置 (Sequence Inversion)

**Applicable when:** A mod appears for the first time in the quest book, and the player is expected to interact with that mod's mechanics.

**Check:** For every mod M that appears in the quest book, the *first* quest that references M must be a teaching quest — one that introduces M's core mechanic through description text or a simple task. No quest that uses M's *advanced* features (multi-block structures, complex automation, end-game materials) may appear before the teaching quest. This strengthens R14 (Teach-Then-Do) by adding mod-granularity tracking: it's not enough that the player was taught the *concept*; the specific mod must be introduced before it is used.

```
for each mod M in pack.mods:
    first_appearance = None
    first_advanced_use = None

    for quest in questbook.all_quests_ordered():
        for task in quest.tasks:
            if task.references_mod(M):
                if first_appearance is None:
                    first_appearance = quest
                if uses_advanced_feature(task, M) and first_advanced_use is None:
                    first_advanced_use = quest

    if first_appearance and first_advanced_use:
        if depth(first_advanced_use) < depth(first_appearance) + 2:
            WARNING: "Mod {M.name} first appears in quest
                      {first_appearance.name} but its advanced features
                      are used in {first_advanced_use.name} at depth
                      {depth(first_advanced_use)}. The teaching quest
                      should precede advanced use by at least 2 quests
                      to allow practice."
```

The "+2" gap is based on the pedagogical principle from CTNH's design: "详细的任务书、新的思索页面为玩家提供详细指导" (detailed quest book and new ponder pages provide thorough guidance). One quest introduces the mod; the next quest lets the player practice the basic mechanic; only then should advanced usage appear. This prevents the sequence inversion where a player encounters a Mekanism multiblock reactor quest before they've crafted their first metallurgic infuser.

**Violation consequence:** The player opens a quest that says "craft a Quantum Entangler" but the preceding quests in that chapter only taught them how to smelt osmium. The cognitive gap between what was taught and what is demanded breaks the learning flow and forces the player to seek external guides — the exact failure mode the quest book was supposed to prevent.

**Source:** CTNH MC百科 — "超过1200+的任务引导" (1200+ quest guides) principle; MC百科 "冒险包设计思路" — "教程的内容需要体现引导性" (tutorials should serve to guide); E2E Extended release notes correcting misleading quest descriptions.

---

### R69 — Description-Trigger Alignment

**Primary defense:** 顺序倒置 (Sequence Inversion)

**Applicable when:** A quest has description text that describes what the player should do, and tasks that define what the player must actually do to complete it.

**Check:** The quest's description text must accurately describe the task requirements. If the description says "craft X" but the task requires "submit 5 of Y", the description misleads the player about what they need to do. More subtly, if the description says "this unlocks the next stage" but the task doesn't actually trigger the stage advancement (because a *later* quest in the chain does), the player may believe they've progressed when they haven't.

```
TRIGGER_KEYWORDS = ["unlocks", "opens", "enables", "allows access",
                     "解锁", "开启", "允许进入", "下一阶段"]

for each quest Q:
    description = Q.description_text
    for task in Q.tasks:
        # Check if description mentions actions not in tasks
        if mentions_craft(description) and task.type != "item_submit":
            INFO: "Quest {Q.name} description mentions crafting but
                   task is {task.type}. Verify description accuracy."

    # Check if description claims progression advancement
    for keyword in TRIGGER_KEYWORDS:
        if keyword in description.lower():
            # Verify this quest actually leads to a gate-opening
            dependents = find_dependent_quests(Q)
            gate_opened = any(is_stage_gate(dep) for dep in dependents)
            if not gate_opened:
                WARNING: "Quest {Q.name} description says '{keyword}'
                          but no dependent quest opens a stage gate.
                          The description may mislead players about
                          what completing this quest achieves."
```

This rule implements the E2E Extended team's practice of refining "quest descriptions to align perfectly with actual gameplay triggers." When a quest description says "interacting with the arcane workbench actually shows the catalysts and completes the quest," the text and the trigger are aligned. When the description says something different from what the task actually checks, the player wastes time doing what the description says rather than what the game requires.

**Violation consequence:** The player reads "craft an osmium compressor" in the description, spends 10 minutes gathering osmium and crafting the compressor, then discovers the task actually requires submitting 16 steel casings. The description was describing the *context* (why you need this) rather than the *action* (what to do), and the mismatch wastes the player's time and erodes trust in the quest book as a reliable guide.

**Source:** E2E Extended release notes — quest description corrections to match gameplay triggers; MC百科 FTB Quests tutorial — description and task alignment best practices.

---

### R70 — Reward-to-Dependent Item Bridge

**Primary defense:** 奖励断链 (Reward Disconnection)

**Applicable when:** A quest has at least one dependent quest (a quest that requires this quest as a prerequisite) and at least one reward.

**Check:** At least one of the quest's rewards should contain an item that is directly useful for completing a dependent quest's task. "Directly useful" means the reward item is either (a) an ingredient in a dependent quest's item_submit task, (b) a tool needed for a dependent quest's task, or (c) a component of a multi-block structure required by a dependent quest. This strengthens R10 (Reward-to-Dependent Bridge) by adding item-level granularity: R10 checks that the *connection exists*; R70 checks that the *reward item itself* participates in the next step.

```
for each quest Q:
    dependents = find_direct_dependents(Q)
    if not dependents or not Q.rewards:
        continue

    reward_items = set()
    for reward in Q.rewards:
        if reward.type == "item":
            reward_items.add(reward.item)
        elif reward.type == "loot_table":
            reward_items.update(resolve_loot_table_items(reward))

    dependent_requirements = set()
    for dep in dependents:
        for task in dep.tasks:
            if task.type == "item_submit":
                dependent_requirements.add(task.item)

    bridging_items = reward_items & dependent_requirements
    if not bridging_items and reward_items and dependent_requirements:
        WARNING: "Quest {Q.name} rewards {list(reward_items)} but none
                  of these items appear in dependent quest requirements
                  {list(dependent_requirements)}. The reward does not
                  bridge to the next step. Consider adding at least one
                  bridging item to guide the player forward."
```

> **max_bridge_depth:** Default 1 (reward item appears in the direct dependent quest's tasks, as implemented above). Recommended 2 for expert packs (reward item may appear up to 2 dependency hops away). When `max_bridge_depth` > 1, extend the scan beyond direct dependents: traverse the dependency graph up to `max_bridge_depth` levels deep and check whether any reward item appears in the task requirements of quests within that range. This addresses the common expert-pack pattern where quest A rewards copper ingot, quest B (dependent of A) requires copper ingot and rewards copper wire, and quest C (dependent of B) requires copper wire — the reward bridges 2 hops rather than 1.

This rule captures the principle implicit in all well-designed expert packs: when you complete a quest that asks you to craft a machine, the reward should include materials or components for the *next* machine in the chain. The player finishes one step and finds themselves already partway to the next — the reward has done the work of the tutorial by putting the next step's ingredients in their inventory.

**Violation consequence:** The player completes a quest, receives 500 XP and a diamond as a reward, and then opens the next quest to find it requires 16 ender pearls and a nether star. The diamond is nice but irrelevant — the reward did nothing to prepare the player for what comes next. The quest chain feels disconnected, like a checklist rather than a journey.

**Source:** Synthesized from R10 (Reward-to-Dependent Bridge) + E2E Extended reward scaling philosophy; MC百科 "论较高难度整合包" — thematic rewards at chapter ends; FTB Quests tutorial — XP rewards become "微不足道" (insignificant) in late game.

---

### R71 — Recipe-Type Diversity Within Stage

**Primary defense:** General quality (indirectly prevents sequence inversion caused by monotonous grind)

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires access to mod recipe-type classifications (shaped crafting, smithing, multiblock processing, ritual, etc.) that are not available during quest generation for mod-specific recipe types. Execute via external validation tool in Step 5. For vanilla and common mod recipes, the rule is executable by the AI; for expert modpack custom recipe types (Create mixing, Mekanism chemical infuser, etc.), downgrade to INFO when mod-specific recipe data is not available.

**Applicable when:** A progression stage (defined by voltage tier, dimension access, or chapter boundaries) contains more than 5 quests with item_submit tasks.

**Check:** Within any single progression stage, the dominant recipe type (shaped crafting, smithing, multiblock processing, ritual, etc.) should not account for more than 60% of all recipe-based tasks. Excessive recipe-type monoculture creates a monotonous grind that tempts players to seek external automation shortcuts, bypassing the intended progression. The Chinese design literature states: "设计多样的配方类型（爆炸、仪式、粉碎、多方块）来消除重复单调的任务" (design diverse recipe types — explosion, ritual, crushing, multiblock — to eliminate repetitive, monotonous tasks).

```
DOMINANCE_THRESHOLD = 0.60

for each stage S in pack.stages:
    quests_in_stage = [q for q in questbook.quests
                       if stage_of(q) == S]
    recipe_tasks = [t for q in quests_in_stage for t in q.tasks
                    if t.type == "item_submit"]
    if len(recipe_tasks) < 5:
        continue

    recipe_types = [classify_recipe_type(t) for t in recipe_tasks]
    type_counts = Counter(recipe_types)
    dominant_type, dominant_count = type_counts.most_common(1)[0]
    ratio = dominant_count / len(recipe_tasks)

    if ratio > DOMINANCE_THRESHOLD:
        WARNING: "Stage {S.name} has {dominant_count}/{len(recipe_tasks)}
                  ({ratio:.0%}) tasks using {dominant_type} recipes.
                  This exceeds the 60% diversity threshold. Consider
                  introducing alternate recipe types to reduce monotony."
```

**Violation consequence:** A stage where 80% of tasks are "craft X in a crafting table" becomes a blur of identical actions. The player stops reading quest descriptions (they all say "craft this"), stops engaging with the mod's unique mechanics, and either burns out or installs a mod that auto-crafts everything — bypassing the intended learning experience entirely.

**Source:** MC百科 "论较高难度、较长寿命整合包的设计与开发" — recipe diversity principle; CTNH's use of custom recipe types (Create processing, GregTech voltage-tier machines, magic rituals) within each voltage tier.

---

### R72 — Late-Game Reward Relevance

**Primary defense:** 奖励断链 (Reward Disconnection)

**Applicable when:** A quest is in the late-game stage (defined as the final 30% of the pack's progression depth, or any quest at depth ≥ 80% of the maximum chain depth).

**Check:** Late-game quest rewards must be *relevant* to subsequent content. Specifically, at least one reward must be either (a) a component of a subsequent quest's recipe chain, (b) a tool or machine that enables new capabilities for subsequent quests, or (c) a prestige/capstone item that serves as a meaningful completion marker. Generic rewards (XP, diamonds, emeralds) in late-game quests fail this check because, as the FTB Quests tutorial notes, "经验奖励必然是微不足道了" (XP rewards will inevitably be insignificant in the late game).

```
LATE_GAME_DEPTH_RATIO = 0.80

for each quest Q:
    max_depth = max_questbook_depth()
    if depth(Q) < max_depth * LATE_GAME_DEPTH_RATIO:
        continue  # not late-game

    if not Q.rewards:
        continue

    subsequent_quests = find_all_descendants(Q, max_depth=3)
    if not subsequent_quests:
        continue  # terminal quest, different rules apply

    has_relevant_reward = False
    for reward in Q.rewards:
        reward_items = resolve_reward_items(reward)
        for item in reward_items:
            if is_generic_reward(item):
                continue  # XP, diamonds, etc.
            if any(item in get_recipe_ingredients(sq) for sq in subsequent_quests):
                has_relevant_reward = True
                break
            if is_tool_or_machine(item) and any(
                item.mod in get_required_mods(sq) for sq in subsequent_quests
            ):
                has_relevant_reward = True
                break
        if has_relevant_reward:
            break

    if not has_relevant_reward:
        WARNING: "Late-game quest {Q.name} (depth {depth(Q)}/{max_depth})
                  has no reward relevant to subsequent content. In late
                  game, generic rewards (XP, currency) are insignificant.
                  Add a reward that bridges to endgame content or serves
                  as a meaningful capstone."
```

**Violation consequence:** The player completes the second-to-last quest in a 200-quest expert pack and receives 1000 XP and 5 diamonds. They've been earning thousands of XP per hour from their automated farms, and they have chests full of diamonds. The reward is functionally worthless — it communicates that the quest book doesn't respect the player's late-game power level. The final push to endgame feels like a chore rather than a climax.

**Source:** MC百科 FTB Quests tutorial — "经验奖励必然是微不足道了" (XP rewards become insignificant); E2E Extended — loot crate tier scaling with effort; ATM-10 discussion #3539 — community debate about whether generous rewards "break progression" or just add variety.

---

## Section B.3 — Genre-Specific Progression Rules (R73–R81)

The following rules address progression validation needs unique to specific pack genres — skyblock, adventure/RPG, and farming/lifestyle. They complement the topology rules (R55–R64) and cross-cutting rules (R65–R72) by encoding genre-specific resource constraints, equipment gating, and environmental limitations that generic rules cannot capture. These rules emerged from Cycle 13 Phase 3 research into skyblock resource chain design (FTB Skies 2, Ex Nihilo Creatio, 收缩空岛), adventure boss progression (NFwC, Era of Black Death, Craftoria bosses), and farming seasonal mechanics (Harvest Festival, 节气 mod, Life-in-the-Village-4). R81 (Multi-Mod Resource Shortcut Detection) extends the genre-specific section to cover cross-mod processing chain interactions that affect all pack types.

---

### R73 — Skyblock Resource Chain Reachability

**Primary defense:** 物品跨级 (Item Cross-Tier) — skyblock variant

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires access to the pack's Ex Nihilo / Ex Deorum sieving configuration (SieveRegistry.json or KubeJS sieve scripts) and the mesh-tier progression definitions. Without sieve config data, downgrade to INFO with note: "Sieving config not available — ore piece availability unverified."

**Applicable pack types:** skyblock only (activate when pack_type = skyblock)

**Applicable when:** The pack is classified as a skyblock pack (no natural ore generation, primary resource acquisition through sieving, crop farming, mob drops, or crystallization) and a quest's `item_submit` task requires an item whose crafting chain includes smelted ores or processed minerals.

**Check:** For every item required by a quest task, trace the item's acquisition chain back to its raw resource origin. In a skyblock context, the origin must be one of: (a) a sievable material (gravel → ore piece → smelt → ingot), (b) a farmable crop or mob drop, (c) a crystallization / budding geode product, or (d) a crafted item from other skyblock-available components. If the chain requires mining (which is impossible in skyblock) or references an ore block that has no sieve drop at any mesh tier, the item is unreachable through skyblock mechanics. The FTB Skies 2 design philosophy explicitly structures three complementary resource paths — "Path of Prospecting" (mechanical sifting), "Path of Crystalmancy" (budding geodes and crystal synthesis), and "Path of Cultivation" (farming and beekeeping) — precisely to ensure every required item has at least one skyblock-native acquisition path.

```
SKYBLOCK_SOURCES = {"sieve", "crop", "mob_drop", "crystal", "fishing",
                     "trading", "beekeeping", "cobblestone_gen"}

for each quest Q:
    for each task T in Q.tasks:
        if T.type != "item_submit":
            continue
        required_item = T.item
        origin = trace_to_origin(required_item)
        if origin.type in SKYBLOCK_SOURCES:
            continue  # reachable through skyblock mechanics

        # Check if sieving config provides this ore
        if origin.type == "ore":
            sieve_drops = get_sieve_drops(origin.ore_block)
            if not sieve_drops:
                ERROR: "Quest {Q.name} requires {required_item} whose
                        crafting chain includes {origin.ore_block}, but
                        this ore has no sieve drop in any mesh tier.
                        In a skyblock pack, ores must be obtainable
                        through sieving. Add a sieve recipe or provide
                        an alternate skyblock-native path."
            else:
                min_mesh = get_minimum_mesh_tier(sieve_drops)
                quest_depth = dependency_depth(Q)
                mesh_unlock_depth = get_mesh_unlock_depth(min_mesh)
                if mesh_unlock_depth > quest_depth:
                    WARNING: "Quest {Q.name} (depth {quest_depth}) requires
                              {required_item} from sieve mesh tier
                              {min_mesh}, but that mesh unlocks at depth
                              {mesh_unlock_depth}. The ore is technically
                              sievable but not yet accessible at this
                              quest's progression point."
```

The mesh-tier unlock depth concept comes from Ex Nihilo Creatio's design: sieves "now take different meshes" and "each mesh gives potentially different results," creating a natural progression gate within the sieving mechanic itself. Hammers also "respect a mining level," meaning the player's tool tier gates which blocks they can crush into sievable gravel. A quest that requires a product of iron-mesh sieving cannot appear before the player has access to iron (which itself requires basic-mesh sieving → smelting → tool crafting).

**Violation consequence:** The player is playing a skyblock pack and reaches a quest that requires 16 osmium ingots. They check their sieving setup — osmium ore pieces have no sieve drop configured. They check the pack's crystallization path — no osmium crystal recipe exists. The item is simply unobtainable in the skyblock context, and the quest is permanently blocked. This is the skyblock-specific variant of R1 (Dimension-Reachability): instead of a wrong dimension, the problem is a wrong *resource acquisition paradigm*.

**Source:** FTB Skies 2 official design philosophy — three complementary resource paths (Crystalmancy / Cultivation / Prospecting); Ex Nihilo Creatio README — mesh-tier progression and mining-level hammer gating; MC百科 post/3327 — configuring GregTech ore sieve drops (with probability balance concerns); 收缩空岛 (Compact Sky) modpack — single-tree starting constraint forcing all resources through skyblock generation.

> **Agent instruction:** Ask the user for the pack's sieve config file path (typically config/exnihilo/SieveRegistry.json or kubejs/server_scripts/sieve.js). If unavailable, downgrade to INFO per the existing fallback.

---

### R74 — Adventure Boss Equipment Threshold

**Primary defense:** 顺序倒置 (Sequence Inversion) — adventure variant

> **[AUTHOR_PARAMETER_REQUIRED]** The `BOSS_TIER_MAP` used in this rule's validation logic maps boss entity IDs to numeric difficulty tiers. This mapping is pack-specific and must be provided by the pack author. If unavailable, the agent should classify bosses by mod tier order (e.g., Twilight Forest boss progression is well-documented: Naga → Lich → Hydra → Ur-Ghast → Snow Queen → Alpha Yeti → Snow Guardian → Final boss), or use entity HP as a tier proxy (HP < 50 = tier 1, 50-100 = tier 2, 100-200 = tier 3, 200+ = tier 4), or downgrade to INFO with note: "Boss tier mapping not available — equipment threshold unverified."

**Applicable when:** A quest contains a `kill` task targeting a boss-level entity (classified by mob HP > 100, custom boss AI, or named boss entity from boss mods like Mowzie's Mobs, Alex's Mobs, Cataclysm, Blue Skies, or Twilight Forest bosses), and the pack uses quest rewards as a primary equipment progression mechanism.

**Check:** Before a boss-kill quest, the player must have access to equipment that can reasonably defeat the boss. "Reasonable" is defined as: (a) the player's obtainable weapon damage per second exceeds the boss's effective HP within a 5-minute combat window, and (b) the player's obtainable armor provides sufficient damage reduction to survive at least 3 consecutive boss attacks at full health. Practically, this means: at least one prerequisite quest (direct or within 2 dependency hops) must reward or require equipment at a tier matching or exceeding the boss's expected difficulty tier. Boss mods typically classify bosses into tiers (e.g., Twilight Forest: Naga → Lich → Hydra → Ur-Ghast → Snow Queen → Alpha Yeti → Snow Guardian → Final boss). A quest requiring a Hydra kill should not appear before the player has access to equipment rewarded by Lich-tier quests.

```
BOSS_TIER_MAP = {
    # Example mappings — pack-specific data required
    "twilightforest:naga": 1,
    "twilightforest:lich": 2,
    "twilightforest:hydra": 3,
    "cataclysm:ender_golem": 4,
    "cataclysm:ignis": 5,
}

EQUIPMENT_TIERS = {
    "iron": 1, "diamond": 2, "netherite": 3,
    "draconic": 4, "creative": 99
}

for each quest Q:
    for each task T in Q.tasks:
        if T.type != "kill":
            continue
        boss_entity = T.entity
        boss_tier = BOSS_TIER_MAP.get(boss_entity, estimate_boss_tier(boss_entity))
        if boss_tier <= 0:
            continue  # not a boss, standard mob

        # Check prerequisite equipment
        prereqs = find_prerequisite_quests(Q, max_hops=2)
        max_equipment_tier = 0
        for prereq in prereqs:
            for reward in prereq.rewards:
                if is_equipment(reward.item):
                    eq_tier = EQUIPMENT_TIERS.get(classify_equipment(reward.item), 0)
                    max_equipment_tier = max(max_equipment_tier, eq_tier)
            for task in prereq.tasks:
                if task.type == "item_submit" and is_equipment(task.item):
                    eq_tier = EQUIPMENT_TIERS.get(classify_equipment(task.item), 0)
                    max_equipment_tier = max(max_equipment_tier, eq_tier)

        if max_equipment_tier < boss_tier - 1:
            WARNING: "Quest {Q.name} requires killing {boss_entity}
                      (tier {boss_tier}) but prerequisite quests only
                      provide equipment up to tier {max_equipment_tier}.
                      The player may lack adequate gear for this fight.
                      Add equipment rewards to prerequisite quests or
                      add equipment task requirements to this quest."
```

The threshold of `boss_tier - 1` allows the player to fight a tier-3 boss with tier-2 equipment (challenging but feasible), while flagging tier-1 equipment against a tier-3 boss (unreasonable). This mirrors the design principle observed across adventure packs: Era of Black Death distributes boss kills across tiers 1-4 with equipment progression quests between them, while NFwC's boss chapter (65% kill density, all bosses in one flat fan-out) relies on the player having completed all prior equipment-progression chapters.

**Violation consequence:** The player encounters a boss-kill quest for the Hydra (tier 3) but their best available weapon is an iron sword (tier 1) because no prerequisite quest rewarded diamond-tier equipment. The fight is technically possible but requires extreme skill, consumable spam, or cheese strategies — none of which the quest book prepared the player for. The boss quest becomes a wall rather than a climax.

**Source:** NFwC boss chapter analysis — 38 kill quests / 58 quests in flat fan-out from single root (boss tier diversity unmanaged); Craftoria bosses chapter — 20 kill tasks isolated in dedicated chapter with progression context; Era of Black Death — tiered boss progression (tiers 1-4) with equipment quests between boss tiers; NFwC #333 comprehensive review noting missing tool prerequisites.

> **Agent instruction:** The pack author must provide a boss tier mapping. If unavailable, classify bosses by mod tier order (Twilight Forest boss progression is well-documented), or use entity HP as a tier proxy, or downgrade to INFO.

---

### R75 — Farming Season-Quest Timing Compatibility

**Primary defense:** 物品跨级 (Item Cross-Tier) — seasonal variant

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires knowledge of the pack's seasonal crop configuration (which crops grow in which seasons, season duration, and whether greenhouse/season-override mechanics are available). Without crop-season mapping data, downgrade to INFO with note: "Seasonal crop config not available — season compatibility unverified."

**Applicable pack types:** farming/lifestyle with seasonal crop mods only

**Applicable when:** The pack uses a seasonal farming mod (Harvest Festival, 节气 / Solar Terms, Pam's HarvestCraft with seasonal addons, or any mod that restricts crop growth to specific in-game seasons) and a quest's `item_submit` task requires a crop or crop-derived item.

**Check:** For every crop-dependent item required by a quest, verify that the crop can be grown at the point in progression where the quest appears. Specifically: (a) the crop's required season must be reachable within the player's current progression — if the game has a linear season cycle (spring → summer → autumn → winter → spring), the player will pass through all seasons eventually, so this is only a *timing* problem when quests form a tight linear chain that the player is expected to complete within one or two season cycles; (b) if the pack provides a season-override mechanism (greenhouse with season-altering items, 节气 mod's 温室心髓, or similar), the quest description should mention this mechanism as an option when the required crop is out of season.

The 节气 mod documentation reveals that crop growth is governed by both season (春夏秋冬, 7 days per season by default) and humidity (5 levels). The greenhouse mechanic provides a bounded escape hatch — the 温室之心 can change the season within 15 blocks, but only if obtained through quest rewards or seasonal progression achievements (limited to once per season). This means the season-override is itself gated, and quest chains requiring greenhouse access must account for this dependency.

```
SEASON_CYCLE = ["spring", "summer", "autumn", "winter"]
SEASON_DAYS = 7  # default, pack-configurable

for each quest Q:
    for each task T in Q.tasks:
        if T.type != "item_submit":
            continue
        required_item = T.item
        crop = identify_source_crop(required_item)
        if not crop:
            continue
        crop_season = get_crop_season(crop)
        if not crop_season:
            continue  # not a seasonal crop

        # Check if the quest chain timing allows reaching the season
        chain_depth = dependency_depth(Q)
        estimated_days_to_quest = chain_depth * avg_quest_completion_days()
        current_season_at_quest = SEASON_CYCLE[
            int(estimated_days_to_quest / SEASON_DAYS) % 4
        ]
        if current_season_at_quest != crop_season:
            # Check for greenhouse/override availability
            has_season_override = check_prerequisite_has(
                Q, ["greenhouse", "season_core", "温室心髓"]
            )
            if not has_season_override:
                WARNING: "Quest {Q.name} requires {required_item}
                          (source crop: {crop}, season: {crop_season}),
                          but estimated progression timing places the
                          player in {current_season_at_quest}. No
                          season-override mechanism is available as a
                          prerequisite. Either (a) reorder the quest to
                          appear during {crop_season}, (b) add a
                          greenhouse/season-override prerequisite, or
                          (c) mention the season timing in the quest
                          description."
            else:
                INFO: "Quest {Q.name} requires out-of-season crop {crop}
                       ({crop_season}). Season override available via
                       prerequisite — verify description mentions this."
```

**Violation consequence:** The player reaches a cooking quest that requires strawberries (a summer crop) during autumn. They have no greenhouse. They must wait through autumn → winter → spring → summer (28 in-game days) to grow the strawberries, or they must discover on their own that a greenhouse mechanic exists. The quest chain stalls not because of a structural dependency problem but because of an environmental timing problem that the quest book didn't anticipate.

**Source:** Harvest Festival wiki (mcmod.cn) — four-season crop system with manual watering and seasonal restrictions ("每季度会有时令食物", vanilla crops restricted without config change); 节气 mod — season + humidity dual constraints with bounded greenhouse override ("温室之心放入温室心髓可改变15格内的季节", "完成节气模组的季节进度也可以得到对应温室心髓为奖励，仅限一次"); Farming Valley Lite — farming progression central to quest design.

> **Agent instruction:** The estimated average in-game days per quest is an author-provided estimate. Default: 1 in-game day per tutorial quest, 2-3 for progression quests.

---

### R76 — Skyblock Multi-Path Resource Redundancy

**Primary defense:** 奖励断链 (Reward Disconnection) — skyblock variant

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires a complete enumeration of all skyblock resource acquisition paths for each material (sieving drops, crop yields, mob farm outputs, trading tables, crystallization products). Without cross-path resource mapping data, downgrade to INFO with note: "Skyblock multi-path resource mapping not available — path redundancy unverified."

**Applicable when:** The pack is classified as a skyblock pack AND explicitly defines multiple resource generation paths (e.g., sieving + farming + crystallization, or sieving + mob farm + trading), AND a quest requires a material that is obtainable through only one of these paths.

**Check:** In a skyblock pack with multiple resource paths, any material required by a quest should be obtainable through at least two distinct paths, OR the quest should explicitly document which path the player needs to invest in. This is the skyblock-specific implementation of R66 (Cross-Branch Gate Independence): in skyblock, "branches" are resource generation methods, and a quest that requires a material from only one path forces the player to invest in that specific path even if they've been developing another. The FTB Skies 2 design explicitly describes its three paths as "unique, yet complementary" — meaning they should supplement each other, not create hard gates between them.

```
MIN_PATHS = 2

for each quest Q:
    for each task T in Q.tasks:
        if T.type != "item_submit":
            continue
        required_item = T.item
        origin_paths = get_all_skyblock_acquisition_paths(required_item)
        if len(origin_paths) >= MIN_PATHS:
            continue  # item available from multiple paths
        if len(origin_paths) == 1:
            path_name = origin_paths[0].path_name
            # Check if the path is clearly documented
            if path_name not in Q.description_text.lower():
                WARNING: "Quest {Q.name} requires {required_item} which is
                          only obtainable through {path_name} path. The
                          quest description does not mention this path.
                          Either (a) add an alternate acquisition path,
                          or (b) document the required path in the
                          description so the player knows which resource
                          system to invest in."
        elif len(origin_paths) == 0:
            ERROR: "Quest {Q.name} requires {required_item} but no
                    skyblock acquisition path exists. This item is
                    unreachable in the skyblock context."
```

The "complementary paths" principle from FTB Skies 2 has a practical consequence: when a player invests heavily in the Path of Cultivation (farming, bees), they should still be able to obtain basic metals through their farming products (perhaps via bees that produce ore-bearing combs, or crop-to-ore transmutation). If only the Path of Prospecting (sifting) provides metals, the farming-focused player hits a wall.

**Violation consequence:** The player has been developing the "farming path" for 10 hours, building crop farms, bee apiaries, and food processing chains. They reach a quest requiring 32 copper ingots. Copper is only available through the sifting path, which they haven't invested in at all. They must now abandon their farming infrastructure and build an entirely separate sifting setup — the two paths aren't complementary, they're isolated.

**Source:** FTB Skies 2 — "unique, yet complementary" three-path design; 收缩空岛 — "分模组任务线" (mod-specific quest lines) with diverse developmental choices; Ex Nihilo Creatio — configurable sieve drops enabling pack authors to create cross-path ore availability.

---

### R77 — Boss Kill Prerequisite Transparency

**Primary defense:** 顺序倒置 (Sequence Inversion) — description quality variant

**Applicable when:** A quest contains a `kill` task targeting a boss entity (as defined in R74) and the quest description does not include equipment recommendations, damage type hints, or tactical guidance.

**Check:** Every boss-kill quest should include at least one of the following in its description: (a) a recommended equipment tier or specific weapon/armor names, (b) damage type effectiveness hints (fire-weak, magic-resistant, etc.), (c) special mechanic warnings (phase transitions, area-of-effect attacks, environmental hazards), or (d) a reference to a prerequisite quest that provides this information. This is the boss-specific variant of AP5 (Empty Quest Description) — but with a stricter standard because boss fights are the highest-stakes moments in adventure packs, and unprepared players face total resource loss on death (especially in hardcore packs like NFwC where the entire pack revolves around combat).

```
BOSS_GUIDANCE_KEYWORDS = [
    "armor", "weapon", "sword", "shield", "bow", "damage", "resist",
    "weak", "strong", "phase", "attack", "dodge", "prepare", "tier",
    "recommended", "装备", "武器", "护甲", "伤害", "弱点", "阶段",
    "建议", "准备"
]

for each quest Q:
    has_kill_boss = any(
        T.type == "kill" and is_boss(T.entity)
        for T in Q.tasks
    )
    if not has_kill_boss:
        continue

    description = Q.description_text.lower()
    has_guidance = any(kw in description for kw in BOSS_GUIDANCE_KEYWORDS)

    # Check if prerequisite quests provide equipment context
    prereqs = find_prerequisite_quests(Q, max_hops=1)
    prereq_has_equipment = any(
        any(is_equipment(r.item) for r in pq.rewards)
        for pq in prereqs
    )

    if not has_guidance and not prereq_has_equipment:
        WARNING: "Quest {Q.name} requires a boss kill but provides
                  neither tactical guidance in the description nor
                  equipment rewards in prerequisite quests. Boss fights
                  are high-stakes moments — the player needs to know
                  what gear to bring and what mechanics to expect.
                  Add equipment recommendations or tactical hints."
```

**Violation consequence:** The player encounters a boss quest with the description "Defeat the Dragon." They enter the fight wearing iron armor with a basic sword and die instantly to the dragon's breath attack. They lose all their items (no keepInventory in hardcore packs). The quest gave no indication that fire resistance or ranged weapons would be necessary. The player must recover their gear, craft fire resistance potions (if they know they need them), and try again — but the quest book never told them what went wrong.

**Source:** NFwC #333 — comprehensive quest book review noting missing tool prerequisites and Create guidance gaps; GregTech-Odyssey #1440 — "no indication in questbook" that stainless steel requires platline setup (non-boss variant of same problem); GregTech-Odyssey #1602 — HV difficulty spike without warning causing burnout risk; Craftoria bosses chapter — kill quests with minimal description context.

---

### R78 — Collection Quest Item Attainability in Non-Combat Packs

**Primary defense:** 物品跨级 (Item Cross-Tier) — peaceful pack variant

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires access to the pack's recipe database and loot table configurations to verify that non-combat alternative acquisition paths (trading, fishing, farming, crafting, mob farm automation) exist for every combat-only item required by collection quests. Without recipe/loot table data, downgrade to INFO with note: "Non-combat alternative path data not available — item attainability unverified."

**Applicable when:** The pack is classified as a farming, lifestyle, or peaceful pack (no combat-focused chapters, no boss-kill quests outside optional content), AND a quest requires collecting multiple distinct items (a "collection quest" with 3+ item_submit tasks or a single task with `count >= 3`).

**Check:** In a non-combat pack, every item required by a collection quest must be obtainable without combat. Specifically, if an item's primary vanilla acquisition method is mob killing (e.g., blaze rods from blazes, ender pearls from endermen, bones from skeletons), the pack must provide an alternative non-combat acquisition path — trading with NPCs, fishing, farming (e.g., Woot-style mob farms that don't require player combat), crop drops, or crafting recipes. The Life-in-the-Village-4 design philosophy explicitly targets players who prefer to "farm peacefully" without combat, expanding culinary depth with "over 300 new foods and drinks" and an "expanded fishing system." A peaceful farming pack that suddenly requires 16 blaze rods (combat-only item) without providing a peaceful alternative breaks the pack's core promise to the player.

```
COMBAT_ONLY_ITEMS = {
    "minecraft:blaze_rod", "minecraft:ghast_tear",
    "minecraft:wither_skeleton_skull", "minecraft:nether_star",
    "minecraft:shulker_shell", "minecraft:dragon_breath",
    # Extend with pack-specific combat-only items
}

NON_COMBAT_ALTERNATIVES = {
    "trading", "fishing", "farming", "crafting", "sieving",
    "beekeeping", "mob_farm_auto", "loot_chest"
}

for each quest Q:
    combat_items = []
    for each task T in Q.tasks:
        if T.type != "item_submit":
            continue
        item = T.item
        if item in COMBAT_ONLY_ITEMS:
            # Check if pack provides non-combat alternative
            alt_paths = get_alternative_paths(item)
            non_combat_alts = [p for p in alt_paths
                               if p in NON_COMBAT_ALTERNATIVES]
            if not non_combat_alts:
                combat_items.append(item)

    if combat_items and pack_is_non_combat():
        WARNING: "Quest {Q.name} in a non-combat pack requires
                  {len(combat_items)} combat-only items: {combat_items}.
                  These items have no peaceful acquisition alternative.
                  Add trading, farming, or crafting alternatives, or
                  move this quest to optional combat content."
```

**Violation consequence:** The player chose a farming/lifestyle pack specifically because they don't enjoy combat. They've been happily growing crops, cooking food, and building their village for 20 hours. A quest requires 8 blaze rods for a potion-brewing chapter. There's no villager trading, no mob farm automation mod, and no crafting recipe for blaze rods. The player must either engage in combat (breaking the pack's promise) or skip the quest (breaking the quest chain).

**Source:** Life-in-the-Village-4 README — "farm peacefully" design philosophy, 300+ foods, expanded fishing, productive bees for automation; Harvest Festival wiki — vanilla crops obtainable only through village exploration (non-combat); 节气 mod — third-party mod crops can bypass seasonal restrictions (alternative path principle).

---

### R79 — Skyblock Space Constraint Task Compatibility

**Primary defense:** 顺序倒置 (Sequence Inversion) — spatial variant

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires mod multiblock structure dimension data (width, height, depth for each multiblock structure from Mekanism, Immersive Engineering, GregTech, Create, etc.) to validate whether the required structure fits within the player's available skyblock space at the given progression point. Without multiblock dimension data, downgrade to INFO with note: "Multiblock structure dimensions not available — space compatibility unverified."

**Applicable pack types:** skyblock only

**Applicable when:** The pack is classified as a skyblock pack AND a quest requires constructing a large multi-block structure (defined as a structure requiring more than 3x3x3 blocks of space, or any multi-block from mods like Mekanism, Immersive Engineering, GregTech, or Create that has a minimum footprint), AND the player has not yet been given access to space-expansion mechanisms.

**Check:** Skyblock packs constrain the player's available building space — the starting island is typically a 5x5 to 10x10 platform. Quests requiring large multi-block structures should not appear before the player has access to at least one of: (a) a cobblestone generator (infinite building material), (b) platform expansion items or mechanics, (c) island creation tools, or (d) sufficient void-platform building blocks from sieving/farming. The Ex Nihilo Creatio mod requires hammers that "respect a mining level" — which means the player needs to progress through tool tiers before they can crush certain blocks into sievable gravel, which gates the rate at which they can generate building material.

```
MIN_SPACE_THRESHOLD = 27  # 3x3x3 blocks

for each quest Q:
    for each task T in Q.tasks:
        if T.type != "item_submit":
            continue
        required_item = T.item
        structure = get_multiblock_structure(required_item)
        if not structure:
            continue
        structure_volume = structure.width * structure.height * structure.depth
        if structure_volume < MIN_SPACE_THRESHOLD:
            continue

        # Check if player has space-expansion access before this quest
        prereqs = find_prerequisite_quests(Q, max_hops=3)
        has_space_expansion = False
        space_expansion_items = [
            "cobblestone_generator", "platform_expander",
            "island_creator", "void_platform", "sky_orchid",
            "ex_nihilo:hammer",  # enables cobblestone crushing
        ]
        for prereq in prereqs:
            for reward in prereq.rewards:
                if any(sei in reward.item for sei in space_expansion_items):
                    has_space_expansion = True
                    break
            for task in prereq.tasks:
                if any(sei in task.item for sei in space_expansion_items):
                    has_space_expansion = True
                    break

        if not has_space_expansion:
            WARNING: "Quest {Q.name} requires building {structure.name}
                      ({structure.width}x{structure.height}x
                      {structure.depth} = {structure_volume} blocks)
                      but no prerequisite quest provides space-expansion
                      mechanisms. In a skyblock pack, the player may
                      not have enough building space or material at
                      this progression point."
```

**Violation consequence:** The player reaches a quest requiring a Mekanism 5x5x5 multiblock reactor in a skyblock pack. They're on a 7x7 starting island. They have no cobblestone generator (the prerequisite quest hasn't appeared yet in the chain). They literally cannot build the structure because they don't have the building materials or the space. The quest is structurally correct in the dependency graph but spatially impossible in the skyblock environment.

**Source:** 收缩空岛 (Compact Sky) — single-tree starting constraint, "能够让你逃出生天的只有一棵树"; Ex Nihilo Creatio — hammer mining-level gating affects cobblestone generation rate; FTB Skies 2 — "custom-designed floating islands" as starting space; FTB Skies 2 — "Over half a dozen uniquely custom built starting islands" showing space management as a design concern.

---

### R80 — Adventure Multi-Branch Narrative Unlock Timing

**Primary defense:** 顺序倒置 (Sequence Inversion) — narrative variant

**Applicable when:** The pack has an adventure/RPG classification with distinct "main quest" and "side quest" branches (identified by chapter naming conventions like "main", "story", "sidequest", "optional", or by `optional: true` grouping), AND side-branch quests have dependencies on main-branch quests.

**Check:** Side-branch quests should not require main-branch progression significantly beyond the point where the side branch diverges. If a side branch's first quest has a dependency on main-branch quest M (the divergence point), no quest in the side branch should depend on a main-branch quest that is more than 3 dependency hops past M. This ensures that the player who chooses to pursue a side branch can complete it without being forced back into the main branch. The CTNH cross-branch independence principle — "不会出现魔法卡科技的情况" — applies to main/side branch relationships as well as magic/tech branch relationships: a side quest should not become blocked because the player hasn't progressed far enough in the main story.

```
MAX_DIVERGENCE_DISTANCE = 3

for each side_quest SQ in side_branch_quests():
    main_branch_deps = [
        d for d in SQ.all_dependencies
        if is_main_branch_quest(d)
    ]
    if not main_branch_deps:
        continue  # pure side content, no main-branch deps

    # Find the divergence point (earliest main-branch dependency)
    divergence_point = min(main_branch_deps,
                           key=lambda q: dependency_depth(q))
    divergence_depth = dependency_depth(divergence_point)

    # Check if any main-branch dep is too far past divergence
    for dep in main_branch_deps:
        dep_depth = dependency_depth(dep)
        distance_past_divergence = dep_depth - divergence_depth
        if distance_past_divergence > MAX_DIVERGENCE_DISTANCE:
            WARNING: "Side quest {SQ.name} depends on main-branch quest
                      {dep.name} (depth {dep_depth}), which is
                      {distance_past_divergence} hops past the side
                      branch's divergence point (depth
                      {divergence_depth}). This forces the player to
                      progress deep into the main story to complete
                      a side quest. Consider removing this deep
                      dependency or making it optional."
```

**Violation consequence:** The player discovers an interesting side quest about exploring ancient ruins. The first quest in the side chain is accessible at main-quest chapter 3 (appropriate). But the third quest in the side chain requires an item from main-quest chapter 8. The player wanted a break from the main story to do something different — but the side content is gated behind main-story progress they haven't reached. The side quest isn't actually "side" content; it's just a main-quest detour with a different narrative skin.

**Source:** CTNH (MC百科) — cross-branch independence principle applied to main/side branches; Dragoncraft README — "dragon-themed adventure pack featuring custom quests, progression systems" with dungeon exploration alongside main quest; NFwC boss chapter — flat fan-out structure (no inter-boss dependencies) as a positive example of branch independence; TheWinterRescue profession chapters — side profession paths with 21-55% optional rate allowing non-linear exploration within tiers.

---

### R81 — Multi-Mod Resource Shortcut Detection

**Primary defense:** 物品跨级 (Item Cross-Tier) — cross-mod variant

> **[EXTERNAL_TOOL_REQUIRED]** This rule requires access to all mods' processing recipe data (crushing, macerating, smelting, chemical processing, etc.) to detect when two or more mods' processing chains intersect in a way that creates an unintended shortcut past a stage gate. Without cross-mod recipe data, downgrade to WARNING with note: "Cross-mod processing chains may create unintended progression shortcuts — manual review recommended."

**Applicable pack types:** all pack types with 2+ processing mods

**Applicable when:** The pack contains quests that use items from a tiered progression system (voltage tiers, stage gates, chapter-based unlocks) AND the pack includes 2 or more mods that provide ore-doubling, ore-tripling, or material-conversion processing chains (e.g., Create crushing wheels, Ex Nihilo sieve + hammer, GregTech macerator, Mekanism enrichment chamber, Immersive Engineering crusher, Thermal Expansion pulverizer).

**Check:** For every material required by a quest at stage N, trace all possible acquisition paths through all installed processing mods. If a path exists that uses a cross-mod conversion chain to obtain the material from a source available at stage N-2 or earlier, the shortcut bypasses the intended stage gate. For example: if stage 3 requires copper ingots and the intended path is "mine copper ore → smelt → copper ingot," but Create's crushing wheel can process copper ore blocks (available at stage 1 via Ex Nihilo sieve) into copper nuggets at a 4:1 ratio, the player can skip the stage-2 mining unlock entirely by using the stage-1 sieve → Create crushing shortcut.

```
for each quest Q at stage N:
    for each task T in Q.tasks:
        if T.type != "item_submit":
            continue
        required_item = T.item
        intended_paths = get_intended_acquisition_paths(required_item, stage=N)
        all_paths = get_all_cross_mod_paths(required_item)

        for path in all_paths:
            source_stage = max(origin_stage for origin in path.origins)
            if source_stage <= N - 2:
                WARNING: "Quest {Q.name} (stage {N}) requires {required_item}.
                          Cross-mod processing shortcut detected:
                          {path.description} sources material from
                          stage {source_stage}, bypassing stage {N-1} gate.
                          Consider gating the shortcut mod's processing
                          recipe or adding a stage-specific intermediate."
```

The risk is highest in packs with many processing mods: a pack with Create + Ex Nihilo + GregTech has at least 6 distinct ore-processing chains (crushing, sieving, macerating, ore washing, thermal centrifuge, chemical bath), any pair of which could intersect to create a shortcut. Expert packs that rely on precise tier gating are most vulnerable; kitchen-sink packs are less affected because stage gates are typically softer.

**Violation consequence:** The player discovers that they can bypass the entire tier-2 mining progression by combining tier-1 sieve outputs with Create crushing wheels processing. The tier-2 chapter's quests become trivially completable without engaging with any tier-2 content. The stage gate that was supposed to create a meaningful progression boundary is rendered meaningless by a cross-mod interaction the pack author didn't anticipate.

**Source:** R76 (Skyblock Multi-Path Resource Redundancy) for the related concept of multi-path resource analysis; R4 (Pack-Type Stage Boundary) for the stage gate that shortcuts bypass; Create mod crushing wheel mechanics (ore block → crushed ore → nugget conversion chain); Ex Nihilo hammer + sieve chain (ore block → gravel → sieve → ore piece).

---

## Section C — Rule Execution Priority

### Step 4 — Generation-time checks

Topology rules R55–R64 operate primarily at Step 5 (validation), but two can run during generation. Cross-cutting rules R65–R72 add three generation-time checks. Genre-specific rules R73–R81 are all Step 5 (validation-time) and activate only when the pack type matches their applicability conditions:

| Priority | Rule | Check type | Failure |
|----------|------|-----------|---------|
| P1 | R55 Topology-Progression Mode Alignment | topology + mode lookup | WARNING |
| P1 | R67 Weak Lock Bypass Detection | alternate path cost comparison | WARNING |
| P1 | R68 Mod First-Appearance Teaching Precedence | mod reference depth tracking | WARNING |
| P2 | R57 Hub Node Size Dominance | size comparison | WARNING |
| P2 | R69 Description-Trigger Alignment | description keyword scan | WARNING/INFO |

> **Note (Cycle 11 Phase 5 correction):** R58 (Collision-Free Adjacent Nodes) was previously listed here but has been moved to Step 5 only. Collision detection cannot be reliably executed by an LLM during generation; it is reserved for post-generation validation.

### Step 5 — Validation-time checks

All topology rules and cross-cutting rules run after coordinate assignment. Genre-specific rules R73–R81 run when the pack type matches:

| Priority | Rule | Check type |
|----------|------|-----------|
| P0 | R58 Collision-Free Adjacent Nodes | all-pairs distance |
| P1 | R55 Topology-Progression Mode Alignment | classification + lookup |
| P1 | R56 Depth-Axis Monotonicity | depth vs coordinate correlation |
| P1 | R59 Bounding Box Viewport Fit | min/max coordinate scan |
| P1 | R61 Convergence Point Visual Prominence | parent position comparison |
| P1 | R65 Tier-Bridge Equipment Sufficiency | equipment tier vs mob tier |
| P1 | R66 Cross-Branch Gate Independence | cross-branch dependency depth |
| P1 | R70 Reward-to-Dependent Item Bridge | reward item ∩ dependent requirement |
| P1 | R73 Skyblock Resource Chain Reachability | sieve config vs task items (skyblock only) |
| P1 | R74 Adventure Boss Equipment Threshold | boss tier vs equipment tier (adventure only) |
| P1 | R78 Collection Quest Item Attainability | combat-only items in peaceful packs (farming only) |
| P2 | R57 Hub Node Size Dominance | size hierarchy comparison |
| P2 | R62 Parallel Column Spacing Uniformity | column center variance |
| P2 | R63 Grid Catalog Aspect Ratio | width/height calculation |
| P2 | R64 Decorative Image Topology Alignment | bounding box containment |
| P2 | R72 Late-Game Reward Relevance | reward relevance vs descendants |
| P2 | R75 Farming Season-Quest Timing | crop season vs progression timing (farming only) |
| P2 | R76 Skyblock Multi-Path Redundancy | path count per item (skyblock only) |
| P2 | R77 Boss Kill Prerequisite Transparency | description keyword scan (adventure only) |
| P2 | R79 Skyblock Space Constraint Compatibility | structure volume vs expansion access (skyblock only) |
| P2 | R80 Adventure Multi-Branch Unlock Timing | divergence distance (adventure only) |
| P2 | R81 Multi-Mod Resource Shortcut Detection | cross-mod recipe path tracing (all packs with 2+ processing mods) |
| P3 | R60 Topology-Shape Vocabulary Coherence | shape count + role analysis |
| P3 | R71 Recipe-Type Diversity Within Stage | recipe type distribution |

---

## Section D — Design Philosophy Findings

The following observations were synthesized from author-facing sources during Cycle 11 Phase 3 research. They inform the topology rules above but are not themselves automated checks.

### How authors plan quest topology

Across all packs studied, quest topology is planned organically rather than systematically. No author in the accessible dataset describes using graph theory terminology (fan-out, convergence ratio, depth classification). Instead, authors think in terms of mod progression chains — "Mekanism needs these machines in this order" — and then arrange those chains spatially on the canvas. The topology emerges from the content, not from an a priori layout plan. This is why the six topology types identified in topology-coordinates.md are descriptive rather than prescriptive: they classify what authors produce, not what authors intend.

The closest thing to systematic topology planning appears in Monifactory's CONTRIBUTING.md, which mandates "top-to-bottom flow" for the main progression chapter and sidebars for tangential information. This is a layout policy, not a topology selection — it constrains the y-axis without specifying whether the topology should be linear, branching, or convergent.

### How authors handle the three hard problems

The three hard problems (item cross-tier, sequence inversion, reward disconnection) are addressed differently depending on pack type. Kitchen-sink packs like ATM-10 use `flexible` progression mode as a structural safety valve — if a player encounters a cross-tier item, they can simply do something else and come back later. Expert packs like Monifactory and GregTech-Odyssey use voltage-tier gating as a hard fence — every item is assigned to a tier, and the quest book mirrors the tier boundary exactly. The quest layout reinforces this: Monifactory's diagonal staircase makes the tier progression physically visible on the canvas.

### Shape and size selection logic

Shape selection is a pack-level decision expressed through `default_quest_shape` at the chapter level. Authors pick one shape per chapter as the "mod identity" (design-guide P1) and reserve other shapes for milestones and special roles. Size follows a clear hierarchy: root nodes and capstone convergence points get size 2.0–3.0, sub-hubs get 1.5, and standard chain nodes stay at 1.0. The ATM-10 create chapter's root at size 3.0 is the largest observed — it serves as a visual anchor that players can orient themselves toward from anywhere in the 206-quest chapter.

### Chapter dimensions

Authors determine chapter width and height implicitly through content volume, not by setting a target dimension. The widest chapters (FTB Evolution create at 30 units, MM2 botania at 27.5 units) are wide because their content is a long horizontal progression chain. The tallest chapters (Monifactory progression at 16 units vertical) are tall because their content is a deep staircase. No author in the dataset discusses setting a target bounding box before filling it — the bounding box is a consequence of the content, not a design input. This is why R59 (Bounding Box Viewport Fit) is a warning rather than a constraint: it alerts when the content has outgrown the viewport, not when the author failed to pre-plan dimensions.

### How authors think about the three hard problems — Cycle 12 Phase 3 additions

Cycle 12 Phase 3 uncovered author-facing design documents from Chinese modpack communities (MC百科, CSDN) and community discussions (ATM-10 GitHub, E2E Extended) that make the three hard problems more explicit than previous research cycles revealed.

**Item cross-tier as a "weak lock" problem.** The MC百科 article "论较高难度、较长寿命整合包的设计与开发" reframes stage gating as a "弱锁" (weak lock) design problem rather than a binary locked/unlocked choice. The author argues that stage locks should be bypassable — but bypasses should carry a cost ("unstable or random" bypass items that provide satisfaction without trivializing the gate). This is a more nuanced position than the kitchen-sink vs. expert-pack dichotomy observed in Cycle 11: it suggests a third approach where gates exist but are permeable, and the quest book's job is to make the *intended* path more attractive than the bypass. CTNH's cross-branch independence principle ("不会出现魔法卡科技的情况" — magic will not block tech) is a structural implementation of weak locks: cross-branch dependencies exist only at convergence points, so the player always has an unblocked path forward within their chosen branch.

**Sequence inversion as a description quality problem.** E2E Extended's release notes reveal that the team actively corrects quest descriptions that mislead players about what triggers completion. This reframes sequence inversion from a purely structural problem (wrong dependency order) to a *text quality* problem: even when the dependency graph is correct, a misleading description can cause the player to attempt advanced content before completing the prerequisite basics. The MC百科 adventure pack design article supports this with the principle "教程的内容需要体现引导性" (tutorials should serve to guide) — a tutorial quest that merely lists facts without guiding the player toward the correct next action is functionally equivalent to a missing tutorial.

**Reward disconnection as a pack-type-dependent problem.** The ATM-10 discussion #3539 reveals that reward disconnection is not equally damaging across pack types. In a kitchen-sink pack, generous but disconnected rewards (diamonds, XP, high-tier cables) are defended as harmless variety — the ATM-10 collaborator argues "it's not like you can all of a sudden beat the game once you get them." In an expert pack, the same disconnected rewards would be catastrophic because expert packs depend on carefully calibrated resource scarcity. This means R70 (Reward-to-Dependent Item Bridge) should be weighted higher in expert packs and lower in kitchen-sink packs, similar to how R1 and R4 already modulate severity by pack type.

**Recipe diversity as anti-burnout design.** The MC百科 design article introduces recipe-type diversity ("多样的配方类型") as a distinct concern from teaching order or item reachability. When 80% of a stage's tasks use the same recipe type, the player enters an "autopilot" mode where they stop reading quest descriptions and stop engaging with mod mechanics. This is not sequence inversion (the order may be correct) and not item cross-tier (the items may be available) — it's a *monotony* problem that manifests as player disengagement. R71 (Recipe-Type Diversity) captures this as a standalone quality metric.

### The "60% content" principle

The MC百科 adventure pack design article introduces a heuristic for gating severity: players should be able to experience "至少60%的相关内容" (at least 60% of the content) without hitting a hard wall. This is not the same as "no gating" — it means that at any point in the progression, at least 60% of the quest book's content should be accessible to the player at their current power level. Hard gates (dimension locks, voltage-tier barriers) should block at most 40% of the quest book at any given time. This principle has implications for R66 (Cross-Branch Gate Independence): if a cross-branch gate blocks more than 40% of the quest book's accessible content, it violates the 60% principle.

### Late-game reward economics

The MC百科 FTB Quests tutorial makes an explicit observation that late-game XP rewards are "微不足道" (insignificant). This is a specific instance of a broader principle: reward *utility* should track player *power level*. In the early game, 100 XP is meaningful because the player is level 0. In the late game, 100 XP is noise because the player's automated farms generate thousands of XP per hour. R72 (Late-Game Reward Relevance) operationalizes this by requiring that late-game rewards be either (a) components of subsequent content, (b) tools that enable new capabilities, or (c) prestige items that serve as meaningful completion markers. The E2E Extended team implements this through loot crate tier scaling — harder quests yield higher-tier loot crates with proportionally more useful contents.

### Genre-specific progression constraints — Cycle 13 Phase 3 findings

Cycle 13 Phase 3 research into skyblock, adventure, and farming pack design revealed that each genre imposes unique constraints on quest progression that generic rules (R1–R72) cannot fully capture. These constraints are not about *what* items are required or *when* they appear — they're about *how the genre's environment* makes certain items fundamentally different from their standard-Minecraft equivalents.

**Skyblock resource paradigm shift.** In a skyblock pack, ores are not mined — they are manufactured through sieving chains. This means that "item reachability" (R1–R4) is insufficient: the question isn't whether the item exists in the pack, but whether the *manufacturing chain* for that item is accessible. The Ex Nihilo Creatio README reveals that the mod deliberately introduced "a little extra progression" through mesh tiers and mining-level-respecting hammers, creating a progression system *within* the resource acquisition mechanic. FTB Skies 2 takes this further by defining three "unique, yet complementary" resource paths (Crystalmancy, Cultivation, Prospecting) — each path provides resources differently, and the pack's job is to ensure that no quest forces the player into a single path they haven't chosen. The 收缩空岛 pack demonstrates the extreme: starting with "只有一棵树" (only one tree), every resource in the entire pack must flow through skyblock generation mechanics. R73 (Skyblock Resource Chain Reachability) and R76 (Multi-Path Resource Redundancy) address these constraints.

**Adventure boss progression as equipment pacing.** Adventure packs face a unique challenge: boss fights are the highest-stakes moments (especially in hardcore packs like NFwC where death means total item loss), yet the quest book often provides inadequate equipment context. The NFwC boss chapter places 38 kill quests in a flat fan-out from a single root — 65% kill density, the highest in the dataset — but relies entirely on the player having completed all prior equipment chapters. Era of Black Death distributes boss kills across 4 tiers with equipment quests between them. R74 (Boss Equipment Threshold) and R77 (Boss Kill Prerequisite Transparency) address the equipment-pacing and description-quality aspects of this problem. R80 (Multi-Branch Narrative Unlock Timing) addresses the related problem of side quests being gated behind main-story progress.

**Farming seasonal timing as a hidden gate.** Farming/lifestyle packs introduce a constraint that doesn't exist in any other genre: the *time of year* gates item availability. The Harvest Festival mod restricts crops to specific seasons with a four-season cycle, and the 节气 (Solar Terms) mod adds humidity as a second constraint layer. Both mods provide greenhouse overrides, but those overrides are themselves gated — the 节气 mod's greenhouse heart is limited to once per season and must be earned through quest rewards. This creates a *timing gate* that looks invisible in the dependency graph: the item is technically craftable, but only during a specific season window. R75 (Farming Season-Quest Timing Compatibility) captures this. R78 (Collection Quest Item Attainability) addresses the related constraint that peaceful packs must provide non-combat alternatives for traditionally combat-only items.

**Space as a progression resource in skyblock.** A subtle constraint in skyblock packs is that *building space* is itself a gated resource. The starting island is small (5x5 to 10x10), and large multi-block structures (common in tech mods like Mekanism, GregTech, and Create) require more space than the player initially has. R79 (Skyblock Space Constraint Task Compatibility) checks that quests requiring large structures don't appear before the player has access to space-expansion mechanisms like cobblestone generators or platform builders.

### Author-voiced design principles — Cycle 14 Phase 3 findings

Cycle 14 Phase 3 gathered design philosophy statements from modpack authors across seven platforms (MC百科, Bilibili, Baidu Tieba, cesspit.net, GitHub repositories, MC百科 bbs forums, CurseForge descriptions). Unlike prior cycles that extracted rules from player complaints or config analysis, this cycle draws directly from *what authors say they intend* — the design rationale behind the choices we observe in the data. The findings are organized around the three hard problems and four specific validation points (PP13, PP14, AP36, AP37).

---

#### R82 — Backward Design Convergence (author-interview rule)

**Name:** Backward Design Convergence
**Severity:** INFO
**Applicable when:** Designing a quest book's overall progression arc, particularly the transition from early-game to mid-game.

The MC百科 adventure pack design article (post/6155) articulates a principle that experienced authors apply intuitively but that no prior rule captures explicitly: the endgame goal should dictate the early-game and mid-game steps. The author writes that creators must evaluate every mod's role — does it belong throughout the entire game, or does it gate a specific stage? This is a *backward design* approach: start from the power fantasy the player should achieve at the end, then work backward to determine what each earlier stage must teach and provide.

In practice, this means that when a quest book's final chapter requires the player to build a multiblock fusion reactor, every earlier chapter should contribute at least one component of the knowledge or material chain that leads to that reactor — either by teaching plasma physics (teaching quest), by providing superconducting wire (item quest), or by gating access to the dimension where tritium is found (dimension quest). A chapter that contributes nothing to the eventual endgame is either decorative content (which is fine in a kitchen-sink pack) or dead weight (which is a problem in an expert pack).

**Implementation check:** For each chapter in the quest book, verify that at least one of its terminal quests (quests with no chapter-internal dependents) either directly provides an item required by the final chapter, or provides a tool/ability that the final chapter's crafting chain depends on. Chapters where all terminal quests are dead-ends with respect to the endgame should be flagged as `INFO — decorative chapter, no endgame convergence`.

**Source:** MC百科 post/6155 — "关于制作冒险类整合包的一些心得分享" (adventure pack design experience); cesspit.net — "the reward goes in two different directions" (forward progression AND backward optimization).

---

#### R83 — Weak Lock Permeability (author-interview rule)

[Design guidance — requires mod-mechanics knowledge, not auto-verifiable. Use as Step 2 design principle, not Step 5 validation rule.]

**Name:** Weak Lock Permeability
**Severity:** WARNING (expert) / INFO (kitchen-sink)
**Applicable when:** A quest or chapter gate blocks player progression to the next stage.

The MC百科 article on high-difficulty long-lifespan pack design (post/4382) introduces the concept of "弱锁" (weak lock) — a stage gate that can be bypassed, but at a cost. The author explicitly states: "阶段锁要是一种'弱锁'" and elaborates that bypass items should be "不稳定，带有随机性" (unstable, carrying randomness) so that players who bypass a gate feel clever without trivializing the intended path.

This is a more sophisticated design principle than simple locked-vs-unlocked gating. A weak lock has three properties: (1) the gate exists and is clearly visible (the player knows they're being gated), (2) a bypass exists but is expensive, random, or limited in scope, and (3) the intended path is more efficient than the bypass. In FTB Quests config terms, this manifests as a quest whose dependency can technically be circumvented (via a rare loot drop, a villager trade, or a crafting recipe that uses materials from a later dimension) but where the bypass costs 5–10x more resources than following the intended quest chain.

The Path of Truth pack (真理之路) implements strict stage gating through Game Stages, Dimension Stages, and Item Stages mods — a hard-lock approach that the pack's FAQ explicitly defends: "如不认真阅读任务书...后果自负" (if you don't read the quest book, you bear the consequences). This represents the opposite end of the lock spectrum from weak locks, and the pack compensates by providing extremely detailed quest descriptions and a 30+ hour solo playtime that ensures players have time to learn.

**Implementation check:** For every stage gate (quest whose completion unlocks a new cluster of content), classify the lock type: hard_lock (no bypass possible, requires gamestage/itemfilter mods), weak_lock (bypass possible but costly), or no_lock (gate is cosmetic). Expert packs should use hard_lock or weak_lock for all major tier transitions. Kitchen-sink packs should use no_lock or weak_lock. Flag hard_lock gates in kitchen-sink packs as `WARNING — hard lock in kitchen-sink context may cause player frustration`.

**Source:** MC百科 post/4382 — "论较高难度、较长寿命整合包的设计与开发"; MC百科 modpack/826 (真理之路 / Path of Truth) — FAQ section on gamestage enforcement.

---

#### R84 — Mid-Game Mechan Density (author-interview rule)

**Name:** Mid-Game Mechan Density
**Severity:** INFO
**Applicable when:** Evaluating the pacing of a quest book's middle chapters.

The MC百科 post/4382 article makes a structural claim about playtime distribution that maps directly to quest book layout: the mid-game should consume the majority of playtime and should introduce "多个新鲜的设定/机制，而这个设定/机制要贯穿一大段内容" (multiple fresh settings/mechanics, and these settings/mechanics must run through a large segment of content). The early game should be brief and push players into the mid-game quickly. The late game should wrap up naturally without artificial time-gating, as "强行增加游戏时间来延长寿命反而会起到反作用" (forcibly increasing game time to extend lifespan will backfire).

In quest book terms, this translates to a chapter-count heuristic: if the quest book has N chapters total, roughly 15% should be early-game (tutorial + first mod introductions), 60–70% should be mid-game (deep mod integration, cross-mod recipes, branching progression), and 15–25% should be late-game (convergence, endgame crafting, capstone challenges). [Heuristic — derived from 2 packs (post/4382, Nova Engineering). Needs validation across broader pack dataset in Cycle 15+.] A quest book where early-game and mid-game are roughly equal in chapter count is front-loaded — the player spends too long in the tutorial phase before encountering the pack's signature content. A quest book where late-game exceeds 30% of chapters is likely padded with filler.

Nova Engineering: World (新星工程) implements this through its Tech Level system (1.0 to 14.0), where each level introduces a new mechanic that persists for multiple subsequent levels. The author explicitly optimized pacing so that "大部分研究的耗时均不超过半个小时" (most research takes no more than half an hour) and avoids "大量无用的前置研究" (large amounts of useless prerequisite research). This is the mid-game density principle in action: every mechanic introduced in the mid-game earns its keep by being reused across multiple subsequent tiers.

**Implementation check:** Classify each chapter as early_game, mid_game, or late_game based on its dependency depth relative to the pack's total depth range. Report the percentage distribution. Flag distributions where early_game > 25% or late_game > 30% as `INFO — unusual pacing distribution, review for front-loading or late-game padding`.

**Source:** MC百科 post/4382 — early/mid/late game proportion guidance; MC百科 modpack/784 (新星工程 / Nova Engineering: World) — Tech Level pacing description.

---

#### R85 — Dual-Direction Reward Principle (author-interview rule)

**Name:** Dual-Direction Reward Principle
**Severity:** WARNING
**Applicable when:** Designing rewards for mid-game and late-game quests.

The cesspit.net expert pack analysis articulates a reward design principle that distinguishes good expert packs from mediocre ones: "the reward goes in two different directions." When a player completes a mid-game quest, the reward should simultaneously (a) open new forward content (a new tool, a new material, access to a new dimension) and (b) improve backward content (make an earlier production chain faster, cheaper, or more automated). The author specifically notes that manual crafting should be restricted for high-demand items to force automation, and that reaching a new tier should allow the player to "refactor their earlier, slow production lines rather than simply abandoning them."

This principle extends R10 (Reward-to-Dependent Bridge) and R45 (Reward Guidance Bridging) by adding a backward-facing component. A reward that only points forward (gives you something for the next quest) is functional. A reward that points both forward AND backward (gives you something for the next quest AND something that improves your existing setup) creates the satisfaction loop that expert pack players describe as "the reward goes in two different directions."

The E2E Extended team implements this through loot crate tier scaling: when the team increased loot crate tiers for hard-to-obtain Botania items, they ensured that the reward crates contained both forward-looking items (components for the next tier's crafting chain) and backward-looking items (upgrades for the player's current mana generation or flower automation). The Adamantine-to-Ichorium armor swap exemplifies the backward direction: Ichorium was chosen over Adamantine because it "offered little unique gameplay beyond being indestructible" — the new armor had to provide *utility*, not just stats.

**Implementation check:** For each quest reward in chapters beyond the first 20% of the quest book, classify the reward direction: forward_only (reward item appears in a dependent quest's task), backward_only (reward item upgrades an already-completed quest's production chain), dual_direction (reward serves both), or dead_end (reward item doesn't appear anywhere in the remaining quest graph). Flag forward_only rewards in mid-game as `INFO — consider adding backward-facing utility`. Flag dead_end rewards in mid-game and late-game as `WARNING — reward has no progression connection`.

**Source:** cesspit.net — "Minecraft Is Not What You Think" (dual-direction reward analysis); E2E Extended release notes v1.83.0-beta (loot crate tier scaling, Adamantine-to-Ichorium swap).

---

#### R86 — Description-as-Pathway Clarity (author-interview rule)

**Name:** Description-as-Pathway Clarity
**Severity:** WARNING
**Applicable when:** Writing or validating quest descriptions, especially for gated or sequential content.

Multiple author sources converge on a principle that reframes quest descriptions from documentation to *navigation*. The MC百科 post/4382 article warns that "一个章节的连线风格要相近，不要让人的第一印象是乱" (a chapter's connection style should be similar, don't let people's first impression be chaos). The GTNH README states that quest book texts "will inform you what's required to progress." The Path of Truth FAQ threatens consequences: "如不认真阅读任务书和/或tooltip，在游戏中遇到任何额外困难后果自负" (if you don't read the quest book and/or tooltips, you bear the consequences of any extra difficulties). And the MC百科 post/6155 article states the principle directly: "教程的内容需要体现引导性" (tutorial content should serve to guide).

The common thread is that in expert and semi-gated packs, the quest description is not supplementary — it is the *primary navigation system*. Players who ignore descriptions will fail, and the pack author's job is to make descriptions so clear and so necessary that ignoring them is the player's deliberate choice, not an accident of poor writing.

This elevates R18 (Description Coverage) and R69 (Description Trust) from quality-of-life checks to progression-critical checks. A quest with no description in an expert pack is not just an INFO-level omission — it's a navigation blackout that can strand the player. The E2E Extended team's practice of actively correcting quest descriptions that mislead players about what triggers completion (documented in their release notes) shows that mature pack teams treat description accuracy as a progression integrity issue, not a cosmetic one.

**Implementation check:** For expert and semi-gated packs, flag any quest with a gate dependency (quest whose completion unlocks new content) that has no description as `WARNING — navigation blackout quest, expert pack requires description`. For kitchen-sink packs, maintain the existing `INFO` severity. Additionally, scan descriptions for hardcoded numbers (tier levels, item counts, energy values) and flag them as `INFO — potential R26 staleness candidate` for future-proofing.

**Source:** MC百科 post/4382 (visual organization principle); GTNH GitHub README (quest text as navigation); MC百科 modpack/826 Path of Truth FAQ; MC百科 post/6155 (tutorial guidance principle); E2E Extended release notes (active description correction).

---

#### R87 — Anti-Nerf Progression Respect (author-interview rule)

[Design guidance — requires mod-mechanics knowledge, not auto-verifiable. Use as Step 2 design principle, not Step 5 validation rule.]

**Name:** Anti-Nerf Progression Respect
**Severity:** WARNING
**Applicable when:** A quest or chapter transition reduces the player's effective power level (e.g., dimension-entry debuffs, equipment restrictions, stat resets).

The MC百科 post/4382 article warns explicitly against nerfing player stats after long grinding: "强行增加游戏时间来延长寿命反而会起到反作用" (forcibly increasing game time to extend lifespan will backfire), and specifically calls out the practice of stripping or reducing player capabilities at stage transitions as a frustration trigger. The CosmicFrontiers pack (星河边疆) demonstrates the correct approach: challenges "scale gradually so the overall experience is 并不让人感到难以承受" (not overwhelming), and when the player enters a hostile dimension, the pack requires them to "gather food buffs, upgrade equipment, and enhance personal abilities" rather than stripping their existing gear.

In FTB Quests terms, this rule flags any quest that (a) appears at a stage transition, (b) requires the player to enter a dimension or biome that applies debuffs, and (c) does not provide a quest reward or immediately-available crafting recipe that mitigates the debuff. The player has spent hours building up their equipment and abilities; the transition quest should acknowledge that investment by providing tools to cope with the new environment, not by nullifying their progress.

The Blue Skies dimension in Path of Truth illustrates a special case: the pack deliberately removed Blue Skies' equipment restrictions via the SkyBreaker mod, turning a potential anti-nerf violation into a resource-gathering opportunity. The FAQ defends this: "不要问为什么加入卡装备的蔚蓝" (don't ask why we added the equipment-restricting Blue Skies) — because they didn't keep the restriction.

**Implementation check:** For quests that unlock dimensions or biomes with known debuff mechanics (Cold Sweat temperature, Blue Skies equipment restriction, Twilight Forest progression barriers), verify that the quest's reward or an immediately-available follow-up quest provides the debuff mitigation item. Flag missing mitigations as `WARNING — stage transition without debuff mitigation, potential anti-nerf violation`.

**Source:** MC百科 post/4382 (anti-nerf principle); MC百科 modpack/931 CosmicFrontiers (gradual scaling philosophy); MC百科 modpack/826 Path of Truth (Blue Skies equipment restriction removal).

---

#### R88 — Reward-Type Contract Enforcement (validates PP13)

**Name:** Reward-Type Contract Enforcement
**Severity:** WARNING
**Applicable when:** Multiple quests within the same chapter use different reward types (loot crate, item, XP, command, choice).

Cycle 14 Phase 2 introduced PP13 (Reward-Type Contract) — the player expectation that reward types within a chapter will be consistent. This cycle provides author-side evidence that pack teams are aware of this contract. The E10 #517 issue (reported by a player, fixed immediately by a collaborator) shows that the Enigmatica team treats reward-type inconsistency as a bug, not a feature. The FTB dev team's decision to exclude loot rewards from "Claim All" (FTBTeam #509, explained by desht) further confirms that mixing reward types creates system-level flow inconsistencies that the mod itself cannot resolve gracefully.

The ATM-10 kitchen-sink context provides the counter-example: TheBedrockMaster's defense of varied rewards ("it's not like you can all of a sudden beat the game once you get them") shows that in a kitchen-sink pack, reward-type variety is acceptable because the pack's progression model doesn't depend on reward precision. The contract is genre-dependent: expert packs promise precision, kitchen-sink packs promise variety.

**Implementation check:** Group quests by chapter and reward type. If a chapter contains more than two distinct reward types (excluding XP, which is a universal bridge), flag as `WARNING — reward-type contract violation` for expert packs and `INFO — reward-type diversity` for kitchen-sink packs. If a chapter mixes loot_crate rewards with item rewards (the specific combination that breaks Claim All flow), flag as `WARNING — Claim All flow incompatibility` regardless of pack type.

**Source:** EnigmaticaModpacks/Enigmatica10 #517 (reward-type inconsistency reported as bug); FTBTeam/FTB-Mods-Issues #509 (loot reward Claim All exclusion); AllTheMods/ATM-10 #3539 (kitchen-sink reward philosophy defense).

---

#### R89 — Progression-as-Reward Viability Conditions (validates PP14)

**Name:** Progression-as-Reward Viability Conditions
**Severity:** INFO
**Applicable when:** A quest or chapter has zero explicit rewards (no item, XP, loot, command, or choice reward).

Cycle 14 Phase 2 introduced PP14 (Progression-as-Reward Social Contract) — the idea that in certain packs, the reward for completing a quest is *the ability to progress further*, not a tangible item. This cycle's research into Nova Engineering: World and the broader GT pack ecosystem provides author-side validation of this concept, along with explicit conditions under which it works.

Nova Engineering: World replaces the traditional quest book with HyperNet — "一个原创剧情化研究系统，贯穿发展全线" (an original story-driven research system running through the entire development line). The "reward" for completing a HyperNet research node is the unlock of the next research node and the narrative progression. The author explicitly designed this to "让玩家在枯燥的游戏过程中也能够体验到更多的细节和乐趣" (let players experience more details and fun during tedious gameplay). The narrative itself is the reward.

But this approach has strict viability conditions drawn from the research data:

1. **Narrative density:** The pack must provide enough descriptive text, lore, or story content per quest that the "unlocking the next chapter" feels like reading the next page of a book. Packs with zero-reward quests and empty descriptions violate this condition.
2. **Mechanical unlock:** Each zero-reward quest must unlock at least one new crafting recipe, dimension, or ability that the player could not access before. The "reward" must be mechanically tangible even if it's not delivered through the reward slot.
3. **Pacing ceiling:** The MC百科 post/4382 article's anti-padding principle applies: zero-reward quests must not be used as filler to extend playtime. "强行增加游戏时间来延长寿命反而会起到反作用."
4. **Genre alignment:** Zero-reward design works in narrative/GT/expert packs where the player expects a long, structured journey. It does not work in kitchen-sink or adventure packs where the player expects immediate tangible payoffs for effort. Exception: when `questbook_role=catalog` (per R50 condition 2), kitchen-sink packs are safe because the quest book serves as a reference catalog rather than an incentive delivery system — the player expects to look things up, not to be rewarded for doing so.

**Implementation check:** For zero-reward quests, verify conditions 1–4. If the quest has no description (condition 1 fail), unlocks no new content (condition 2 fail), is in a sequence of 5+ zero-reward quests (condition 3 risk), or is in a kitchen-sink/adventure pack without `questbook_role=catalog` (condition 4 fail), flag as `WARNING — progression-as-reward viability condition not met`. Otherwise, flag as `INFO — progression-as-reward design, verify player expectations match pack genre`.

**Source:** MC百科 modpack/784 Nova Engineering: World (HyperNet narrative system); MC百科 post/4382 (anti-padding principle); MC百科 modpack/931 CosmicFrontiers (17 technological ages with story-driven progression).
**Cross-reference:** R50 (Zero-Reward Design Safety Conditions — condition 2 questbook_role exception), PP14 (Progression-as-Reward Social Contract).

---

#### R90 — Convergence Item Backtracking Safety (validates AP37)

**Name:** Convergence Item Backtracking Safety
**Severity:** WARNING (expert) / INFO (kitchen-sink)
**Applicable when:** A convergence quest (fan-in of 10+ dependencies) requires items from multiple earlier chapters.

Cycle 14 Phase 2 introduced AP37 (Convergence Claustrophobia) — the risk that large convergence points force the player to backtrack through earlier content to gather items they didn't know they'd need. This cycle's research into CosmicFrontiers and GTNH provides author-perspective solutions to this problem.

CosmicFrontiers spans GregTech's 15 voltage levels and 17 technological ages, with the flow from Steam to IV "completely overhauled to integrate magic and custom production lines." The key design decision is that non-GT mods are "organically woven into the core tech progression" — meaning that the items required at convergence points are not bolted on from unrelated mods but are natural byproducts of the main progression chain. When a player reaches a convergence quest in CosmicFrontiers, they should already have most of the required items from their normal progression flow. Items they don't have should be obtainable within their current tier's content scope — not requiring a return to a much earlier tier.

GTNH's approach is similar but more explicit: the README states that the quest book allocates "content of other mods to a fitting point within the progression," and that "gated players must learn about the mod" before subsequent content becomes available. This means that by the time a convergence quest requires an item from mod X, the player has already been introduced to mod X several quests earlier and has the infrastructure to produce the item.

The MC百科 post/4382 article provides the negative case: the author warns against mods that are used once and discarded, which creates "orphan" items that the player has no reason to stockpile. When a convergence quest later requires these orphan items, the player must backtrack to a mod they've already mentally moved past.

**Implementation check:** For convergence quests with 10+ dependencies, analyze each required item's "home chapter" (the chapter where the item's crafting chain is primarily located). Calculate the distance between the convergence quest's chapter and the farthest home chapter. If the distance exceeds 3 chapters in expert packs or 5 chapters in kitchen-sink packs [Preliminary — based on 2 GT expert packs. Adventure/RPG convergence patterns may differ.], flag as `WARNING — convergence item requires long-range backtracking`. Additionally, check if the required item's crafting chain depends on any quest the player could have skipped (optional quests). If so, flag as `WARNING — convergence item depends on skippable content`.

**Source:** MC百科 modpack/931 CosmicFrontiers (organic mod integration); GTNH GitHub README (progression-point allocation); MC百科 post/4382 (anti-orphan-mod principle).

---

#### How the three hard problems map to author-interview rules

The Cycle 14 Phase 3 author interviews reveal that experienced pack authors think about the three hard problems in ways that are more holistic than the individual rules suggest. The problems are not solved by isolated checks but by interlocking design decisions that span the entire pack architecture.

**Item cross-tier (三硬伤 #1) → R82 + R83 + R90.** Authors prevent item cross-tier through backward design (R82): if you know the endgame requires a fusion reactor, you place superconductor wire three tiers before the reactor quest, not after. They implement gates as weak locks (R83) so that even if a cross-tier item slips through, the player can bypass it at a cost rather than getting stuck. And they ensure convergence points (R90) don't force backtracking, which is the most common way item cross-tier manifests in practice — not as a forward overshoot but as a backward pull.

**Sequence inversion (三硬伤 #2) → R84 + R86 + R87.** Authors prevent sequence inversion through mid-game density (R84): if the mid-game is dense enough, players won't rush ahead because there's always something meaningful to do at their current tier. They make descriptions the primary navigation system (R86) so that even if a player encounters advanced content early, the description tells them what prerequisites they need. And they avoid anti-nerf transitions (R87) that punish players for progressing, which can create the illusion of sequence inversion when the player's power level drops at a stage boundary.

**Reward disconnection (三硬伤 #3) → R85 + R88 + R89.** Authors prevent reward disconnection through dual-direction rewards (R85): if every reward points both forward and backward, there's no such thing as a dead-end reward. They enforce reward-type contracts (R88) so that the player can predict what kind of reward to expect, which makes disconnected rewards feel like bugs rather than design choices. And in zero-reward contexts (R89), they ensure that the progression unlock itself serves as a meaningful reward, which eliminates the expectation of tangible payoffs that would otherwise go unmet.

---

#### Contradictions and tensions observed

Two tensions emerged from comparing author statements across platforms:

**Tension 1: Lock strictness vs. pack genre.** The Path of Truth author advocates strict stage locking with severe consequences for non-compliance ("后果自负"), while the MC百科 post/4382 author advocates weak locks that can be bypassed. These are not contradictory — they represent different genre commitments. Path of Truth is a hardcore expert pack where the strict lock *is* the content (the journey of discovery through forced engagement). Post/4382 describes a more flexible expert pack where the bypass option adds replayability. R83 handles this by modulating severity based on pack type.

**Tension 2: Reward generosity vs. reward precision.** The ATM-10 collaborator TheBedrockMaster defends generous, varied rewards in kitchen-sink packs, while the E2E Extended team treats reward-type inconsistency as a bug. This tension is resolved by the pack-type axis: kitchen-sink packs promise variety and generosity; expert packs promise precision and intentionality. R88 implements this by applying different severities to the same observation depending on pack type.

---

## Section D — Community Design Wisdom Rules (R91–R100)

These rules are distilled from community-shared pack-making experience: MC百科 design articles, FTB Forum threads, adventure-pack design guides, and author commentary on Chinese and English platforms. Unlike R82–R90 (which came from identifiable pack authors), these rules emerge from collective community wisdom and cross-pack patterns. Each rule includes its original-language source quote for traceability.

---

#### R91 — Chapter Visual First-Impression Consistency

**Name:** Chapter Visual First-Impression Consistency
**Severity:** WARNING
**Applicable when:** Any chapter with more than 15 quests and mixed dependency structures.

The MC百科 post/4382 article — one of the most detailed Chinese-language pack-making experience shares — states explicitly: "一个章节的连线风格要相近，不要让人的第一印象是乱" (a chapter's connection style should be similar; don't let the first impression be chaos). This principle is validated by player feedback across multiple platforms: convergence zones in diamond_convergence chapters are where players most frequently report feeling overwhelmed, and the visual consistency of the dependency graph is the primary tool for mitigating this.

The post/4382 article further recommends adding thematic pixel art at the end of task lines: "任务线末尾添加契合主题的像素画以提升视觉体验." This creates visual bookends that help the player perceive chapter boundaries.

The Insurgence cookbook chapter (75% diamond shape, X[-8..8]×Y[-8..8]) is the gold standard for visual consistency. Its diamond_convergence layout means every quest in the chapter follows the same geometric logic, so the player's eye learns the pattern within seconds.

**Implementation check:** For each chapter, calculate the coefficient of variation of dependency fan-in values. If CV > 1.0 within a single chapter (indicating wildly inconsistent dependency counts), flag as `WARNING — chapter visual first-impression inconsistency`. Additionally, if a chapter contains more than 3 distinct shape types AND has more than 50 quests, flag as `INFO — high shape diversity, verify intentional design`.

**Source:** MC百科 post/4382 (chapter connection style principle); Cycle 15 Phase 1 Insurgence cookbook analysis (diamond_convergence gold standard).
**Cross-reference:** R35 (shape semantics consistency), R60 (shape consistency within chapter).

---

#### R92 — Olive-Shaped Equipment/Reward Distribution

**Name:** Olive-Shaped Equipment and Reward Distribution
**Severity:** INFO
**Applicable when:** A pack has equipment tiers, reward tiers, or difficulty tiers.

The MC百科 adventure pack design thread (bbs.mcmod.cn thread-21004) establishes the "橄榄球形" (olive-shaped) distribution principle for equipment and rewards: "装备种类应呈现橄榄球形，即中阶物资丰富，而基础与顶级装备相对稀缺." This principle applies to quest rewards, equipment availability, and difficulty distribution alike.

Concretely, this means:
- **Equipment tiers:** If the pack has 4 tiers (e.g., 不入流/普通/精英/首领), the middle two tiers should contain ~60-70% of all equipment items, while tier 1 and tier 4 contain ~15-20% each.
- **Reward tiers:** Low-tier rewards (basic materials, XP) and high-tier rewards (rare items, endgame gear) should be sparse. Mid-tier rewards (useful tools, progression items, mod-specific currencies) should dominate.
- **Difficulty distribution:** The hardest and easiest quests should be rare. Most quests should sit in the comfortable middle difficulty range.

This mirrors the well-known game design principle of bell-curve distribution, but the adventure pack community has independently derived and named it for the quest-book context.

**Implementation check:** For packs with declared tier systems, count quests per tier. If the ratio of (tier 1 + top tier) / total > 50%, flag as `INFO — equipment distribution may be inverted (hourglass pattern instead of olive)`. If the middle tiers contain < 40% of all quests, flag as `INFO — olive distribution not met, mid-tier content may feel sparse`.

**Source:** MC百科 bbs thread-21004 (adventure pack design — equipment tier distribution).
**Cross-reference:** R12 (reward value progression), R15 (complexity escalation).

---

#### R93 — Dimension Transition Equipment Continuity

**Name:** Dimension Transition Equipment Continuity
**Severity:** WARNING
**Applicable when:** A pack uses dimension changes as progression milestones (Nether, End, custom dimensions).

The adventure pack design thread establishes a precise principle for dimension transitions: "前一维度的毕业级防具，应当刚好足以应对新维度基础怪物的攻击" (the graduation armor from the previous dimension should be just sufficient to handle the new dimension's basic enemies). This creates a "Goldilocks zone" where the transition feels both earned and challenging.

The principle has two failure modes:
1. **Over-prepared:** If the player's previous-dimension gear trivializes the new dimension's basic enemies, the dimension feels pointless and the player rushes through it.
2. **Under-prepared:** If the player's gear is insufficient even for basic enemies, the transition feels punishing and the player gets stuck.

The thread further recommends that each dimension should have its own ecosystem and trading mechanics, not just combat: "各个维度应当具备专属的生态系统与特色玩法（例如交易机制），而非单纯的战斗场景."

**Implementation check:** For dimension-gated progression, identify the "graduation quest" of dimension N and the "entry quest" of dimension N+1. Compare the equipment rewarded or required in the graduation quest with the equipment required in the entry quest's first combat encounter. If the graduation equipment tier is more than 2 levels above the entry requirement (over-prepared) or more than 1 level below (under-prepared), flag as `WARNING — dimension transition equipment discontinuity`.

**Source:** MC百科 bbs thread-21004 (dimension transition armor continuity principle); CosmicFrontiers MC百科 modpack/931 (GT voltage-tier as dimension analogue).
**Cross-reference:** R17 (tool-reward-before-use), R87 (anti-nerf transitions).

---

#### R94 — Crafting Depth Fatigue Ceiling

Applicability: The 2-level ceiling is primarily applicable to narrative, adventure, and progression-focused packs with linear crafting expectations. Sandbox and expert crafting packs (GregTech, Nova Engineering) intentionally embrace deep crafting chains as core gameplay — for these pack types, raise the fatigue ceiling from 2 to 5 levels and change the severity from WARNING to INFO.

**Name:** Crafting Depth Fatigue Ceiling
**Severity:** WARNING
**Applicable when:** A quest requires an item whose crafting recipe itself requires crafted components (nested crafting chains).

Two independent community sources converge on the same principle. The post/4382 article warns against repetitive mandatory operations: "避免在同一个地方进行多次必须的重复操作." The adventure pack design thread adds a quantitative ceiling: "嵌套合成可以有个一两次，过度复杂会引发玩家厌倦" (nested crafting can happen once or twice; excessive complexity causes player fatigue).

This establishes a concrete ceiling: **crafting chain nesting depth should not exceed 2 levels** for mandatory quests. A 2-level chain means: the quest requires item X, which requires crafted component Y, which requires crafted component Z. A 3-level chain (X→Y→Z→W) is the fatigue threshold.

Expert packs (GregTech, Nova Engineering) can push this to 3-4 levels because their players expect and enjoy deep crafting chains. But for non-expert packs, 2 levels is the soft ceiling.

The CosmicFrontiers approach of "organically weaving" mods into the GT progression provides an escape valve: when a crafting chain goes deep, each nesting level should introduce a *different mod's* mechanic, so the player is doing something new at each level rather than repeating the same operation.

**Implementation check:** For each quest task item, recursively trace the crafting chain depth. If the chain exceeds 2 levels in a non-expert pack or 4 levels in an expert pack, flag as `WARNING — crafting depth exceeds fatigue ceiling`. If the chain exceeds 2 levels AND two consecutive levels use the same mod's machines, flag as `WARNING — crafting depth with repetitive operations`.

**Source:** MC百科 post/4382 (anti-repetition principle); MC百科 bbs thread-21004 (1-2 nesting depth ceiling); CosmicFrontiers (organic mod weaving as depth escape valve).
**Cross-reference:** R3 (recipe-chain depth), R15 (complexity escalation).

---

#### R95 — Mod Reuse Anti-Orphan Principle

**Name:** Mod Reuse Anti-Orphan Principle
**Severity:** WARNING
**Applicable when:** A mod is introduced in one chapter and never referenced again in subsequent chapters.

The post/4382 article states firmly: "每一个模组都要有重复利用，杜绝一次性抛弃" (every mod must have repeated use; eliminate one-time-use-and-discard). This principle addresses the "orphan mod" problem: when a mod is introduced for a single quest and then abandoned, the player invests time learning its mechanics for no lasting payoff. Worse, when a later convergence quest requires an item from this orphan mod, the player must backtrack to content they've mentally discarded.

GTNH's approach validates this from the expert side: the README states that content from other mods is allocated "to a fitting point within the progression," implying each mod appears at multiple progression points, not just one.

CosmicFrontiers takes this further by weaving non-GT mods "organically into the core tech progression" — meaning each mod contributes to multiple voltage tiers, not just its introduction tier.

**Implementation check:** For each mod that provides quest task items, count the number of distinct chapters where its items appear as task requirements. If a mod appears in only 1 chapter and that chapter is not the final chapter, flag as `WARNING — potential orphan mod (single-chapter usage)`. If a mod appears in only 1 chapter AND that chapter has fewer than 5 quests using the mod, flag as `WARNING — confirmed orphan mod (minimal usage, single chapter)`.

**Source:** MC百科 post/4382 (mod reuse principle); GTNH GitHub README (progression-point allocation); CosmicFrontiers MC百科 modpack/931 (organic mod integration).
**Cross-reference:** R90 (convergence item backtracking safety), R81 (multi-processing-mod management).

---

#### R96 — Early-Game Velocity Imperative

**Name:** Early-Game Velocity Imperative
**Severity:** INFO
**Applicable when:** The early-game section (first 20% of total quests) has disproportionately high quest count or mandatory time sinks.

The post/4382 article delivers a blunt principle: "前期新鲜感消退极快，不宜强行拉长寿命，建议让玩家尽快进入中期" (early-game novelty fades fast; don't force-drag the lifespan; guide players to reach mid-game quickly) and "强行增加游戏时间来延长寿命反而会起到反作用" (forcibly extending playtime to increase lifespan will backfire).

This principle does NOT mean the early game should be trivial. It means the early game should be *dense with novelty* and *efficient in teaching*, not padded with repetitive resource gathering or empty quests. The early game's job is to hook the player and establish the pack's identity — once that's done, transition to mid-game where the bulk of playtime should occur.

The Techno Ages pack validates this: in stage 0, the pack is strict ("在阶段0你无法合成和使用下一个时代的物品") but the stage itself is short. The pack gets you through stage 0 quickly and into the more interesting stages where recipe modifications create novel experiences.

**Implementation check:** Calculate the ratio of early-game quests (first chapter or first 20% of total quests) to total quests. If this ratio exceeds 30% AND the early-game chapter has more than 5 mandatory item-submission tasks with identical or near-identical items, flag as `INFO — early game may be padded, consider acceleration`. If the early game contains more than 3 quests with descriptions shorter than 20 characters, flag as `INFO — early game quests may lack novelty density`.

**Source:** MC百科 post/4382 (early-game velocity principle); Techno Ages MC百科 modpack/332 (strict but brief stage 0).
**Cross-reference:** R19 (bottleneck spacing), R41 (early-game flexible progression mode).

---

#### R97 — Dimension-as-Gate Alternative

**Name:** Dimension-as-Gate Alternative
**Severity:** INFO
**Applicable when:** A pack uses quest book locks (stage gates) as the primary progression control mechanism.

The adventure pack design thread proposes an alternative to quest-book locking: "没必要非得用东西来卡进度，通过世界的变化来达到进度的改变" (there's no need to use things to gate progression; achieve progression change through world changes). The concrete method is adjusting resource and mob spawning per dimension to naturally limit equipment tier.

This principle is especially relevant for adventure/RPG packs where the quest book should feel like a guide, not a gatekeeper. By making dimension access the progression gate (the player literally cannot reach the Nether until they've built a portal, which requires specific materials only available after certain quests), the pack avoids the friction of quest-book lock screens.

The Medieval Minecraft pack validates this: "你前往末路之地的方式完全被改变了" (the way you reach the End is completely changed) — the End dimension is gated by gameplay mechanics (dragon egg hatching, specific items), not by quest book locks.

However, this approach has a trade-off: it's less precise than quest-book gates. Players may accidentally bypass intended progression order. The post/4382 "weak lock" principle (R83) provides the complementary solution: when dimension-as-gate is used, the quest book should still provide guidance and descriptions, even if it doesn't hard-lock.

**Implementation check:** For packs with `pack_type=adventure` or `pack_type=rpg`, count the ratio of quests with `lock` state vs. total quests. If more than 60% of quests use hard locks AND the pack has 3+ dimensions, flag as `INFO — consider dimension-as-gate alternative to reduce quest-book lock friction`. If fewer than 20% of quests have descriptions AND the pack relies on dimension gating, flag as `WARNING — dimension gating without quest book guidance, players may lack direction`.

**Source:** MC百科 bbs thread-21004 (dimension-based progression alternative); Medieval Minecraft MC百科 modpack/255 (End dimension gating).
**Cross-reference:** R67 (stage gate distribution), R83 (weak lock design), R86 (description as navigation).

---

#### R98 — Single-Game Cohesion Principle

Applicability: Primarily applicable to expert, narrative, and progression-focused packs. Kitchen-sink and sandbox packs intentionally embrace mod diversity without forced quest integration — for these pack types, raise the orphan-mod threshold from 15% to 50%.

**Name:** Single-Game Cohesion Principle
**Severity:** INFO
**Applicable when:** A pack contains more than 30 mods and uses a quest book for progression guidance.

The GTNH FTB Forum thread states the aspiration clearly: the pack should feel "more like a single game than a compilation of mods thrown together." This is achieved by using a central progression framework (GregTech's voltage tiers in GTNH, HyperNet in Nova Engineering, the cookbook in Insurgence) and allocating every mod's content to a fitting point within that framework.

The principle has three concrete implications:
1. **No orphan mods:** Every mod must contribute to the central progression (validated by R95).
2. **No orphan quests:** Every quest must either advance the central progression or provide a meaningful side activity that enriches the world.
3. **Consistent visual language:** The quest book's visual design (shapes, sizes, icons) should reflect the central progression's structure, not each mod's individual aesthetic.

CosmicFrontiers extends this by giving the pack a narrative wrapper (the "Space Jeff Bezos" revenge storyline) that ties all mods together under a single thematic umbrella, even when the mods themselves have unrelated themes.

The Create Chronicles pack takes a different approach: instead of a central tech tree, it uses cooking automation as the "single game" core, with all other mods orbiting around this central mechanic.

**Implementation check:** For each mod in the pack, classify its role: `core_progression` (required for advancement), `enrichment` (optional but thematic), or `utility` (QoL, no progression impact). If more than 30% of mods are classified as `enrichment` with zero quest references, flag as `INFO — potential cohesion gap (unused enrichment mods)`. If the pack has no single chapter or quest chain that touches more than 50% of all mods, flag as `INFO — no clear central progression spine detected`.

**Source:** GTNH FTB Forum thread (single-game aspiration); CosmicFrontiers MC百科 modpack/931 (narrative wrapper); Create Chronicles MC百科 modpack/1135 (cooking-as-core).
**Cross-reference:** R82 (backward design), R95 (anti-orphan).

---

#### R99 — Quest Pacing Rhythm

**Name:** Quest Pacing Rhythm (Undulation Principle)
**Severity:** INFO
**Applicable when:** A chapter contains more than 20 quests or a pack has more than 5 chapters.

The Sohu game design article establishes the "起伏" (undulation) principle: quest arrangement needs rhythmic variation. "Place relaxing puzzles or roaming after intense clashes, intersperse quick palate-cleansers within long chains, and leave room for independent wandering between core story beats."

The post/4382 article echoes this from the pack-maker perspective: the mid-game (the longest section) must have "多个新鲜的设定/机制，而这个设定/机制要贯穿一大段内容" (multiple fresh settings/mechanics, each spanning a large section of content). This means each major mid-game section should introduce at least one new mod or mechanic, and the quests within that section should explore it progressively from simple to complex.

Concretely, the rhythm pattern for a well-paced chapter should look like:
1. **Introduction** (1-3 quests): Teach the new mechanic with simple tasks
2. **Exploration** (3-8 quests): Gradually increase complexity
3. **Challenge** (1-2 quests): Hard task requiring mastery of the mechanic
4. **Palate cleanser** (1-2 quests): Easy reward-collection or lore quests
5. **Transition** (1 quest): Bridge to the next section

If a chapter has 3+ consecutive hard challenges without a palate cleanser, or 5+ consecutive easy quests without a challenge, the rhythm is broken.

**Implementation check:** For each chapter with >20 quests, classify each quest's difficulty (based on task complexity: item submission = easy, crafting = medium, multi-step = hard). Calculate the longest run of consecutive same-difficulty quests. If the longest run of hard quests > 3, flag as `INFO — pacing may lack relief (3+ consecutive hard quests)`. If the longest run of easy quests > 5, flag as `INFO — pacing may lack engagement (5+ consecutive easy quests)`.

**Source:** Sohu game quest design article (undulation principle); MC百科 post/4382 (mid-game freshness principle).
**Cross-reference:** R19 (bottleneck spacing), R15 (complexity escalation), R84 (mid-game density).

---

#### R100 — Tiered Optional Challenge Architecture

**Name:** Tiered Optional Challenge Architecture
**Severity:** INFO
**Applicable when:** A pack includes optional challenge content beyond the main progression path.

The Create Chronicles pack (MC百科 modpack/1135) implements a concrete pattern for optional challenges: "工程师公会提供三个难度的可选挑战，完成挑战会获得独特代币" (the Engineer Guild provides optional challenges at three difficulty levels; completing challenges earns unique tokens). These tokens are then traded in a custom shop system, creating a parallel economy that doesn't interfere with the main progression.

This pattern has three components:
1. **Tiered difficulty:** At least 3 difficulty levels (easy/medium/hard or bronze/silver/gold), so players of different skill levels can participate.
2. **Unique token rewards:** The challenge rewards are tokens/currencies that can only be spent in a dedicated shop, preventing them from inflating the main economy.
3. **Optional by design:** These challenges are never required for main progression. They exist for players who want extra engagement after completing the main content.

The GTNH coin system and lootbag approach validates a similar pattern: custom currencies earned through quest completion can be spent on useful items, but the main progression doesn't require spending them.

**Implementation check:** For packs with optional challenge content, verify: (1) challenges have at least 2 difficulty tiers, (2) challenge rewards use a dedicated currency or token (not standard progression items), (3) no main-progression quest depends on completing an optional challenge. If an optional challenge has only 1 difficulty level, flag as `INFO — single-difficulty challenge, consider tiered approach`. If a main-progression quest depends on an optional challenge reward, flag as `WARNING — main progression depends on optional content`.

**Source:** Create Chronicles MC百科 modpack/1135 (Engineer Guild challenge system); GTNH FTB Forum thread (coin and lootbag system).
**Cross-reference:** R46 (questbook role declaration), R12 (reward value progression).

---

#### How the three hard problems map to community-design-wisdom rules

The Cycle 15 Phase 3 community design wisdom reveals that experienced pack makers solve the three hard problems through holistic design habits that complement the more technical rules from R82–R90.

**Item cross-tier (三硬伤 #1) — R93 + R95 + R98.** The community approach to preventing item cross-tier is structural rather than formula-based. R93 ensures that dimension transitions maintain equipment continuity (the player's gear is always appropriate for their current tier). R95 eliminates orphan mods that create backtracking traps. R98 ensures the entire pack has a cohesive progression spine that prevents items from appearing "out of place." Together, these rules address the root cause of cross-tier issues: not individual recipe mistakes, but architectural incoherence.

**Sequence inversion (三硬伤 #2) — R96 + R97 + R99.** The community approach to preventing sequence inversion is pacing-based rather than lock-based. R96 ensures the early game doesn't drag (so players don't look for shortcuts). R97 offers dimension-as-gate as a natural alternative to quest-book locks (so the world itself prevents inversion). R99 ensures pacing rhythm prevents the "bored player syndrome" that leads to sequence-breaking attempts. These rules address the motivation for sequence inversion: players break sequence because they're bored, stuck, or confused — not because they're malicious.

**Reward disconnection (三硬伤 #3) — R92 + R94 + R100.** The community approach to preventing reward disconnection is distribution-based. R92 ensures rewards follow an olive-shaped distribution (so no reward is so rare it feels disconnected from effort). R94 ensures crafting depth doesn't create fatigue (so the reward is reachable without exhaustion). R100 provides a parallel reward economy for optional content (so challenge rewards don't interfere with main progression rewards). These rules address the structural causes of reward disconnection: imbalanced distribution and excessive friction.

---

#### New tensions from community wisdom

**Tension 3: Early velocity vs. early teaching.** R96 (early-game velocity imperative) pushes for fast early game, while R14 (teach-then-do) and R18 (description coverage) push for thorough early-game teaching. The resolution is that early-game quests should teach efficiently — every quest teaches something AND moves the player forward. Empty "fetch 64 cobblestone" quests waste time without teaching. The post/4382 article resolves this: "建议让玩家尽快进入中期" doesn't mean skip teaching — it means don't pad.

**Tension 4: Dimension-as-gate vs. quest-book precision.** R97 (dimension-as-gate) reduces quest-book lock friction, but dimension gating is less precise than quest-book locks. A player might reach the Nether through an unexpected route and skip intended content. The resolution is a hybrid approach: use dimension access as the primary gate, but supplement with quest-book descriptions and optional guidance (R86). The quest book tells the player what they *should* do; the dimension gate ensures they can't do what they *shouldn't*.

---

## Section E — Author Design Practice Rules (R101–R105)

> **Cycle 16 Phase 3 findings.** These five rules are derived from Cycle 16 Phase 3 author interviews and design articles, sourced primarily from Chinese pack-making communities (MC百科 post/6155 adventure pack experience, MC百科 thread-21004 adventure pack design philosophy, MC百科 post/4382 high-difficulty long-lifespan design, MC百科 post/1416 FTB Quests tutorial, klpbbs thread-130537 expert pack mod toolkit) and validated against specific pack implementations (C2MSE2 14-era architecture, Chroma Endless 2 step-by-step learning design, Sunlit Valley quest-book-as-guide approach). They complement the author-interview rules (R82–R90) and community-wisdom rules (R91–R100) with concrete, implementable practices observed in working packs.

---

#### R101 — Multi-Layer Stage Enforcement Toolkit

**Name:** Multi-Layer Stage Enforcement Toolkit
**Severity:** INFO
**Applicable when:** A pack uses progression gating (expert, semi-gated, or gated kitchen-sink) to prevent item cross-tier or sequence inversion. For packs on mod loaders that support stage-framework mods. Lightweight or vanilla+ packs that intentionally avoid stage-framework mods are exempt from this recommendation.

The klpbbs thread-130537 documents the systematic toolkit that Chinese expert-pack authors use to enforce stage boundaries through multiple independent layers. Rather than relying on a single lock mechanism, experienced authors combine: (1) **Quest-book dependencies** — the FTB Quests `dependencies` array controls which quests appear available; (2) **Game Stages framework** — a non-linear stage permission system where "游戏阶段是非线性的，玩家可以随时获得或失去游戏阶段" (game stages are non-linear; players can gain or lose them at any time); (3) **Item Stages** — prevents item usage entirely, where "即使拿到了物品也无法使用，如果拿在手上会自动丢掉" (items cannot be used and are auto-dropped if held without the required stage); (4) **Recipe Stages** — locks crafting recipes behind specific stages, so even if a player has the materials, they cannot craft; (5) **Ore Stages** — disguises world blocks until unlocked, where "方块会伪装成其他方块...且不允许玩家对其右键" (ores disguise as other blocks and block right-clicks until unlocked); (6) **Dimension Stages** — restricts dimension access based on world progress; (7) **Tool/Skill Stages** — limits tool creation and skill usage (TinkerStages, Skillable/Reskillable).

This multi-layer approach provides defense-in-depth against item cross-tier (三硬伤 #1). Even if a player somehow obtains an item from a later stage (e.g., through mob drops, trading, or loot), the Item Stages layer prevents them from using it. Even if they know the recipe, Recipe Stages prevents crafting. Even if they try to mine the ore directly, Ore Stages disguises it. The quest-book dependency is the visible layer; the stage framework is the invisible enforcement layer.

The MC百科 post/4382 article validates this by advocating "弱锁" (weak locks) that don't strictly forbid alternative paths but make the intended path the path of least resistance. Weak locks complement hard stage locks: the stage framework prevents accidental cross-tier, while weak locks in the quest book reward clever players who find legitimate shortcuts.

**Implementation check:** For packs using progression gating, document which enforcement layers are active. If a pack uses ONLY quest-book dependencies without any stage framework, flag as `INFO — single-layer progression gating, consider adding Item Stages or Recipe Stages for defense-in-depth`. If a pack uses 3+ layers, verify that the layers are consistent (no layer accidentally blocks a legitimate progression path). If a stage-locked item appears as a quest reward before the player has the corresponding stage, flag as `WARNING — reward item blocked by stage enforcement`.

**Source:** klpbbs thread-130537 (expert pack mod toolkit: Game Stages, Item Stages, Recipe Stages, Ore Stages, Dimension Stages, TinkerStages, Skillable/Reskillable, Triumph); MC百科 post/4382 (weak lock philosophy).
**Cross-reference:** R83 (weak lock permeability), R102 (era-based architecture), R4 (stage boundary), R67 (stage gate distribution).

---

#### R102 — Era-Based Quest Architecture for Long-Term Packs

**Name:** Era-Based Quest Architecture
**Severity:** INFO
**Applicable when:** A pack has more than 10 chapters or expects 100+ hours of gameplay.

The C2MSE2 pack (MC百科 modpack/1016) demonstrates a distinctive architectural pattern: organizing the quest book into 14 distinct "eras" (时代), each representing a self-contained progression unit with its own introduction, escalation, and capstone. The pack describes "一本任务书，指导你完成游戏包中 14 个主要 '时代' 的任务" (one quest book guiding you through 14 main eras), with over 300 quests total. A hidden 15th chapter is reserved for endgame players who defeat the Wither Storm on the final Ad Astra planet.

An "era" differs from a chapter in scope: each era may contain multiple chapters but represents a coherent progression phase with a clear beginning (introduction to the era's key mods), middle (escalation through the era's crafting chains), and end (capstone that transitions to the next era). The MC百科 post/6155 adventure pack experience article validates this approach with its "难度递进" (difficulty progression) philosophy: each stage should have clear objectives, and "高阶段的装备应该舒适地处理下一阶段的基础敌人" (top-tier equipment from a previous stage should comfortably handle basic enemies in the next).

Era-based architecture naturally prevents item cross-tier because items from one era should not appear in another era's crafting chains. It also prevents sequence inversion because era transitions serve as hard gates. The MC百科 thread-21004 design philosophy article describes the era transition as "这个世界无敌了，去往下一个世界" (becoming invincible in this world, moving to the next world) — the player moves on when they've mastered the current era, not when the quest book forces them to.

The post/4382 article adds a critical constraint: "确保每一个 mod 被复用而非丢弃" (ensure every mod is reused rather than discarded). An era should not use a mod once and abandon it; mods that span multiple eras should have their content distributed across those eras, not front-loaded.

**Implementation check:** For long-term packs (>10 chapters or >100 expected hours), verify: (1) each era (group of 2–5 related chapters) has a clear introduction quest that teaches the era's key mods, (2) cross-era dependencies only flow forward (later era depends on earlier era, never backward), (3) no item from era N+2 or later appears as a task requirement in era N, (4) each era has at least one capstone quest that serves as the era's transition point. If a pack has >10 chapters with no discernible era grouping, flag as `INFO — consider era-based architecture for long-term progression clarity`.

**Source:** C2MSE2 MC百科 modpack/1016 (14-era architecture, 300+ quests); MC百科 post/6155 (difficulty progression philosophy); MC百科 thread-21004 (dimension-as-era transition); MC百科 post/4382 (mod reuse across eras).
**Cross-reference:** R82 (backward design convergence), R101 (multi-layer stage enforcement), R84 (mid-game mechan density), R99 (quest pacing rhythm).

---

#### R103 — Tutorial Quest as Player Anchor

**Name:** Tutorial Quest as Player Anchor
**Severity:** WARNING
**Applicable when:** A pack includes tutorial or onboarding content (first chapter or introductory quests).

Multiple Cycle 16 Phase 3 sources converge on the same observation: the first quest in the first chapter serves as the player's primary reference point — their "anchor" when they feel lost. The Chroma Endless 2 pack (MC百科 modpack/702) describes this explicitly: "更会召唤你一步一步的学习、进化、并掌握每一种模式和机制" (the game calls you to learn, evolve, and master every mode and mechanism step by step), with "一套详尽的任务系统将会引导你完成复杂的整合包" (a comprehensive quest system guides you through the complex modpack). The Sunlit Valley pack states: "任务书将作为你最忠实的向导，提供了一系列详尽且循序渐进的教程任务" (the quest book serves as your most loyal guide, providing a series of detailed and step-by-step tutorial quests). The MC百科 post/1416 FTB Quests tutorial recommends that checkbox tasks "通常用于介绍辅助内容" (are typically used to introduce supplementary content), distinguishing teaching tasks from progression tasks.

The anchor quest pattern has three characteristics: (1) The anchor quest has the most detailed description in the chapter, explaining not just what to do but WHY; (2) The anchor quest has no dependencies (it's the entry point), ensuring it's always visible; (3) The anchor quest's reward introduces the pack's reward economy — a simple tool, starter XP, or a key item that opens up the next few quests. The anchor quest is NOT a "fetch 64 cobblestone" busywork task; it's a genuine teaching moment.

This pattern differs from R14 (teach-then-do ordering) in emphasis: R14 ensures teaching quests precede doing quests, while R103 ensures the FIRST teaching quest is designed as the player's permanent reference anchor — the quest they return to when confused.

**Implementation check:** For the first chapter's first quest: (1) verify it has no dependencies (entry point), (2) verify its description length exceeds the pack's median description length, (3) verify its reward is a starter item (tool, XP, or key resource) rather than a late-game item or dead-end cosmetic, (4) verify the chapter's subsequent quests form a dependency tree rooted at this anchor quest. If any condition fails, flag as `WARNING — first chapter anchor quest may not serve as effective player guide`.

**Source:** Chroma Endless 2 MC百科 modpack/702 (step-by-step learning); Sunlit Valley minecraftzw.com/45694 (quest book as loyal guide); MC百科 post/1416 (checkbox tasks for teaching).
**Cross-reference:** R14 (teach-then-do), R18 (description coverage), R102 (era-based architecture — each era should have its own anchor quest).

---

#### R104 — Crafting Method Variety Within Stage

**Name:** Crafting Method Variety Within Stage
**Severity:** INFO
**Applicable when:** A pack has stages with 5+ crafting-dependent quests.

The MC百科 post/4382 article explicitly warns against "重复性研磨" (repetitive grinding) and recommends "利用多样的制作方式" (utilizing diverse crafting methods). The specific advice is to mix vanilla methods (beacons, explosions, minecarts) with modded ones (infusion, rituals, trading) within each progression stage. The MC百科 thread-21004 design article adds: "防止重复性研磨，利用多样的制作方式" (prevent repetitive grinding through diverse crafting methods), and suggests that tech mods should be "强制并行的科技模组形成一条统一的进度线" (forced into a unified progression line from parallel tech mods) to reduce repetitive crafting patterns.

This rule extends R71 (recipe-type diversity within stage) by focusing on the crafting *method* — the physical interaction the player performs — rather than the recipe structure. A stage where every quest requires "put items in machine, wait for output" has low method variety even if the machines are different mods. A stage that alternates between crafting table assembly, machine processing, ritual infusion, villager trading, environmental interaction, and multiblock construction maintains player engagement through mechanical novelty.

The MC百科 post/6155 article validates this with its observation that packs become "水槽包" (kitchen-sink packs) when they "强制乏味的刷怪或重复性制作" (force tedious grinding or repetitive crafting). The antidote is not fewer quests but more varied crafting experiences within each quest.

**Implementation check:** For each stage with 5+ crafting-dependent quests, categorize each quest's primary crafting method (crafting table, furnace/smelting, mod machine, ritual/infusion, trading, environmental, multiblock, manual tool use). If any single method exceeds 60% of quests in a stage, flag as `INFO — crafting method variety low in this stage, consider diversifying crafting interactions`. If any stage has only 1 crafting method for all quests, flag as `WARNING — single crafting method stage, high risk of repetitive gameplay`. For genre-focused packs (farming, adventure, lifestyle), adapt the crafting method categories to match the pack's genre-appropriate interactions rather than using the tech/magic method list. The 60% threshold is a conversation-starter for genre packs, not a hard flag.

**Source:** MC百科 post/4382 (crafting variety recommendation); MC百科 thread-21004 (unified tech progression line); MC百科 post/6155 (anti-grinding philosophy).
**Cross-reference:** R71 (recipe-type diversity), R94 (crafting depth fatigue ceiling), R99 (quest pacing rhythm).

---

#### R105 — 60% Content Accessibility Ceiling

**Name:** 60% Content Accessibility Ceiling
**Severity:** INFO
**Applicable when:** All packs with more than 3 chapters.

The MC百科 post/6155 article states a design principle that multiple sources independently validate: "设计流程使用户至少能看到 60% 的内容" (design the flow so users can see at least 60% of the content). This principle targets both novices and speedrunners — the casual majority who won't complete every optional quest chain. The MC百科 thread-21004 article's olive-shaped equipment distribution validates this: mid-tier content should be abundant (accessible to the 60% majority) while only the extremes are rare (reserved for completionists). The post/4382 article's "建议让玩家尽快进入中期" (get players to mid-game quickly) ensures that the 60% threshold includes meaningful mid-game content, not just early-game tutorials.

This rule reframes R32 (chapter QA coverage heuristic) from a QA perspective to a design intent perspective. R32 asks "does the QA process cover enough quests?" — R105 asks "can a casual player following the main quest line access at least 60% of the pack's content without pursuing side quests or optional challenges?" If the answer is no, the pack's late-game content is gated behind a completionist wall that most players will never reach.

The C2MSE2 pack demonstrates the positive case: its 14-era architecture with 300+ quests is explicitly designed so that "非常详细的任务帮助玩家在游戏中循序渐进，不会遗漏任何内容" (very detailed quests help players progress step by step without missing any content). The main quest line threads through all 14 eras, while optional content branches off as side paths that enrich but never gate.

**Implementation check:** Calculate the ratio of quests accessible via the main dependency chain (following mandatory dependencies only) to total quests in the pack. If the ratio is below 60%, flag as `INFO — less than 60% of content accessible via main quest line, casual players may miss significant content`. Additionally, check if any chapter has zero quests reachable from the main chain — if so, flag as `WARNING — entire chapter unreachable from main progression path`.

**Source:** MC百科 post/6155 (60% accessibility design principle); MC百科 thread-21004 (olive-shaped distribution); MC百科 post/4382 (early-to-mid velocity); C2MSE2 MC百科 modpack/1016 (detailed quest guidance preventing content miss).
**Cross-reference:** R32 (chapter QA coverage), R41 (early-game flexible progression mode), R102 (era-based architecture).

---

### Section G — International Author Design Philosophy Rules (R106–R116)

These rules are derived from Cycle 17 Phase 3 research into English-language and cross-cultural author design philosophy, focusing on how international pack makers independently arrived at solutions to the three hard problems (item cross-tier, sequence inversion, reward disconnection), and how the Game Stages ecosystem bridges FTB Quests with runtime enforcement.

---

#### R106 — Dimensional Progression Naturalism

**Name:** Dimensional Progression Naturalism
**Severity:** WARNING
**Applicable when:** Packs with 2+ dimension-adding mods and dimension-gated content.

The MC百科 thread-21004 article articulates a design principle that has no equivalent articulation in English-language sources: progression should feel like "这个世界无敌了，去往下一个世界" (this world is conquered, move to the next world). Rather than artificial stage-locking that forces the player to check a quest book, the author argues that dimensions themselves should serve as natural progression gates. The player's sense of mastery over one dimension creates intrinsic motivation to explore the next. This principle is independently validated by SevTech Ages (ATLauncher), which uses vanilla advancement milestones as "age" gates — each age unlocks new mods, hides ore until the appropriate stage, dynamically hides items and recipes, and introduces new mobs as the player progresses. The SevTech approach demonstrates that the same naturalism principle can be implemented through vanilla advancements rather than FTB Quests, suggesting the principle is toolkit-agnostic.

This rule supplements R16 (dimension-explore-then-craft) by adding a motivational dimension: R16 checks that the player explores a dimension before crafting from its resources, but R106 checks that the dimension transition itself feels earned rather than arbitrary. If a pack gates a dimension behind a quest that requires no meaningful engagement with the current dimension, the transition feels forced rather than natural.

**Implementation check:** For each dimension-gating quest, verify that at least 3 other quests in the current dimension must be completed before the gate quest becomes available. If the gate quest has fewer than 3 same-dimension prerequisites, flag as `WARNING — dimension transition may feel abrupt, player has not meaningfully engaged with current dimension`. Additionally, check that the gate quest's task items are obtainable within the current dimension — if they require items from a dimension the player hasn't visited yet, flag as `ERROR — dimension gate requires cross-dimension items (R1 cross-tier)`.

**Source:** MC百科 thread-21004 (dimensional progression naturalism); SevTech Ages ATLauncher page (vanilla advancement age gates, player-based progression); MC百科 post/6155 (stage-specific goals).
**Cross-reference:** R16 (dimension-explore-then-craft), R1 (dimension-reachability), R102 (era-based architecture), R113 (multi-dimensional state synchronization).

---

#### R107 — Olive-Shaped Equipment Distribution

**Name:** Olive-Shaped Equipment Distribution Curve
**Severity:** INFO
**Applicable when:** Packs with tiered equipment systems (3+ tiers of weapons/armor/tools).

The MC百科 thread-21004 article states that equipment quantity should follow an olive shape: "两头少，中间多" (few at both ends, many in the middle). This distribution pattern ensures that early-game equipment is scarce (making each upgrade meaningful), mid-game equipment is abundant (providing variety and choice), and late-game equipment is again scarce (making endgame achievements feel exclusive). This pattern independently validates R105 (60% content accessibility ceiling) from an equipment perspective: the mid-game bulge corresponds to the 60% of content that casual players should access, while the narrow extremes serve completionists.

This principle contrasts with the common kitchen-sink approach of presenting all equipment tiers equally, which leads to early-game overwhelm (too many options before the player understands the mod ecosystem) and late-game anticlimax (too many equivalent endgame options diluting the sense of achievement). The olive shape is a specific instance of the broader pacing principle that mid-game density should exceed both early-game and late-game density (MC百科 post/4382).

**Implementation check:** Count the number of distinct equipment items (weapons, armor, tools) available at each tier. If the distribution does not follow an olive shape (mid-tier count < early-tier count OR mid-tier count < late-tier count), flag as `INFO — equipment distribution is not olive-shaped, early or late game may feel disproportionately sparse or dense`. This is an informational heuristic, not a hard constraint.

**Source:** MC百科 thread-21004 (olive-shaped equipment distribution); MC百科 post/4382 (mid-game density priority); MC百科 post/6155 (60% accessibility principle).
**Cross-reference:** R12 (reward value progression), R105 (60% content accessibility), R110 (mid-game density priority).

---

#### R108 — Gear-to-Mob Cross-Dimension Scaling

**Name:** Gear-to-Mob Cross-Dimension Scaling
**Severity:** WARNING
**Applicable when:** Packs with 2+ dimension-adding mods that include hostile mobs.

The MC百科 thread-21004 article establishes a precise scaling rule: "上一个阶段的顶端装备，可以应对这个阶段的小怪" (the previous stage's top-tier equipment should handle the current stage's basic mobs). This means the best gear from dimension N should be roughly equivalent to the baseline combat requirement of dimension N+1. The transition should feel challenging but not impossible — the player's investment in the previous dimension's endgame is rewarded with survivability in the next dimension's early game, but not with dominance over its endgame.

This rule addresses the item cross-tier problem (三硬伤 #1) from a combat balance perspective. If the previous dimension's best gear trivializes the next dimension's content, the player has no incentive to engage with the new dimension's equipment progression. If the previous dimension's best gear is insufficient for the next dimension's basic mobs, the player experiences a frustrating difficulty spike that may drive them to creative mode or quit.

The MC百科 post/6155 article validates this from the adventure pack perspective: "Clear endgame & scaling" requires defining "ultimate requirements for gear and events early on" with a "difficulty progression mindset" that ensures "stage-specific goals without early-game frustration."

**Implementation check:** For each dimension transition, compare the DPS/damage/armor values of the source dimension's best equipment against the target dimension's basic mob HP/damage. If source best DPS > 3× target basic mob HP, flag as `WARNING — previous dimension's best gear may trivialize next dimension's content`. If source best DPS < 0.3× target basic mob HP, flag as `WARNING — difficulty spike at dimension transition, player's best gear may be insufficient for basic survival`.

**Source:** MC百科 thread-21004 (gear-to-mob scaling principle); MC百科 post/6155 (clear endgame & scaling, difficulty progression mindset).
**Cross-reference:** R2 (tool-tier item reachability), R4 (stage boundary), R106 (dimensional progression naturalism).

---

#### R109 — Forced Anti-Skip Material Binding

**Name:** Forced Anti-Skip Material Binding via World Generation
**Severity:** WARNING
**Applicable when:** Expert/semi-gated packs with dimension-gated resources.

The MC百科 thread-21004 article identifies a critical author responsibility: players might skip dimensions unless forced by quest requirements or world-generation manipulation. The article recommends altering ore and mob generation rules to tie specific materials strictly to their intended dimensions ("需要改矿脉和怪物生成"). This prevents the player from obtaining dimension N+1 materials through dimension N's world generation, which would break the progression sequence.

This rule provides the world-generation enforcement layer for R101 (multi-layer stage enforcement). While R101 focuses on runtime locking (Game Stages, Item Stages, Recipe Stages), R109 addresses the root cause: if the material physically cannot be found in the wrong dimension, no runtime lock is needed for that specific cross-tier vector. The combination of world-generation binding (R109) + runtime stage locking (R101) + quest dependency gating (R4) creates a three-layer defense against item cross-tier that covers all three vectors: physical availability, technical usability, and progression awareness.

The MC百科 post/6155 article's principle that a mod can serve as either "a continuous thread or a specific stage gatekeeper" reinforces this: when a dimension is a stage gatekeeper, its unique materials must be exclusive to that dimension.

**Implementation check:** For each dimension-gated material, check world-generation configs to verify that the material's ore generation is restricted to its intended dimension. If a dimension N+1 material has ore generation entries in dimension N (or the overworld when it should be Nether/End-gated), flag as `WARNING — material [X] generates in dimension [N] but is intended for dimension [N+1], player may skip progression`. Additionally, check that mob drops required for dimension-gated recipes only spawn in the correct dimension.

**Source:** MC百科 thread-21004 (anti-skip material binding, ore/mob generation manipulation); MC百科 post/6155 (mod as stage gatekeeper vs continuous thread).
**Cross-reference:** R1 (dimension-reachability), R4 (stage boundary), R42 (stage-internal item reachability), R101 (multi-layer stage enforcement).

---

#### R110 — Mid-Game Density Priority

**Name:** Mid-Game Density Priority
**Severity:** INFO
**Applicable when:** All packs with 3+ chapters or 50+ quests.

The MC百科 post/4382 article establishes that mid-game "is the most critical phase and should occupy the majority of playtime." This article, addressing high-difficulty long-lifespan pack design, argues that the mid-game must integrate diverse crafting methods across multiple mods to prevent repetitive tasks, and introduce fresh overarching mechanics that span entire quest chapters to maintain interest. The early game should be designed to transition players to mid-game quickly ("建议让玩家尽快进入中期"), while the late game should focus on a satisfying conclusion without artificial time extension.

This principle independently converges with the Western "guided but not linear" ideal (Lesson 94) and the olive-shaped equipment distribution (R107). All three describe the same underlying pattern: the pack's center of gravity should be in the middle, not at the extremes. The early game is a funnel (narrow, directed, tutorial), the late game is a summit (narrow, challenging, conclusive), and the mid-game is a plateau (wide, varied, exploratory).

The MC百科 post/4382 article also warns against a common anti-pattern: "强行增加游戏时间来延长寿命反而会起到反作用" (forcibly increasing game time to extend lifespan will have the opposite effect). This directly targets the nested-crafting-chain fatigue that R94 addresses, but from the author's perspective rather than the player's.

**Implementation check:** Calculate the quest count distribution across early-game (chapters 1-2 or first 20% of dependency depth), mid-game (chapters 3-N-1 or middle 60%), and late-game (last chapter or final 20%). If mid-game quest count < 40% of total, flag as `INFO — mid-game may be under-dense relative to early/late game`. If early-game quest count > 30% of total, flag as `INFO — early game may be over-extended, consider accelerating transition to mid-game`.

**Source:** MC百科 post/4382 (mid-game density priority, anti-forced-lifespan); MC百科 post/6155 (early-to-mid velocity); MC百科 thread-21004 (olive-shaped distribution).
**Cross-reference:** R15 (complexity escalation), R19 (bottleneck spacing), R84 (mid-game density), R94 (crafting depth fatigue ceiling), R99 (pacing rhythm), R105 (60% accessibility).

---

#### R111 — Anti-Forced-Lifespan Extension

**Name:** Anti-Forced-Lifespan Extension
**Severity:** WARNING
**Applicable when:** Packs with nested crafting chains or 100+ hour estimated playtime.

The MC百科 post/4382 article warns explicitly: "强行增加游戏时间来延长寿命反而会起到反作用" (forcibly increasing game time to extend lifespan will have the opposite effect). This principle targets the common expert-pack anti-pattern of adding arbitrary grind layers (excessive nested crafting, artificial resource scarcity, repetitive kill quests) solely to inflate the pack's advertised playtime. The article argues that a pack should respect the player's time: every hour of gameplay should introduce new mechanics, decisions, or challenges, not repeat established patterns at higher numerical scales.

This rule complements R94 (crafting depth fatigue ceiling) by addressing the author's motivation rather than the player's experience. R94 detects when crafting chains are too deep; R111 detects when the author has made a deliberate choice to extend playtime through repetition rather than content. The distinction matters: a 5-layer crafting chain that introduces a new mechanic at each layer is engaging, while a 5-layer chain that repeats the same smelt→crush→smelt pattern at higher tiers is forced lifespan extension.

The MC百科 post/4382 article also emphasizes that "所有 previously introduced mods remain relevant" in the late game — if a mod introduced in the early game becomes obsolete by mid-game, the player's investment in learning that mod was wasted, which is another form of forced lifespan (the player spent time on content that didn't pay off).

**Implementation check:** For each chapter, calculate the ratio of unique task types (crafting, kill, dimension, advancement, item) to total quests. If a late-game chapter has < 2 unique task types and > 10 quests, flag as `WARNING — late-game chapter may be repetitive, consider adding task variety`. Additionally, check for "grind escalation" patterns: if 3+ consecutive quests in a chain require the same task type with increasing quantities (e.g., 10 iron → 50 iron → 200 iron), flag as `WARNING — potential forced lifespan extension through quantity escalation`.

**Source:** MC百科 post/4382 (anti-forced-lifespan principle); MC百科 post/6155 (respect player time); MC百科 thread-21004 (nested crafting limit).
**Cross-reference:** R94 (crafting depth fatigue), R99 (pacing rhythm), R15 (complexity escalation), R71 (recipe-type diversity).

---

#### R112 — Vanilla Enhancement Layering

**Name:** Vanilla Enhancement Layering
**Severity:** INFO
**Applicable when:** Packs that include vanilla+ or vanilla-compatible mods alongside major tech/magic mods.

The CSDN article on FTB Quests + GameStages integration describes a design pattern called "香草体验增强" (vanilla enhancement): rather than replacing core Minecraft mechanics, modded capabilities are progressively layered on top of vanilla functionality as the player advances. Base game elements remain functional throughout the pack, but modded capabilities add depth and efficiency at higher tiers. This approach ensures that players who prefer vanilla-style gameplay can still progress (albeit more slowly), while players who embrace modded mechanics gain access to more powerful tools.

This pattern is independently validated by SevTech Ages, which progressively reveals mods as the player advances through ages — the early ages use mostly vanilla mechanics with minimal mod additions, while later ages introduce complex mod systems. The vanilla foundation is never invalidated; it's supplemented. FTB University 1.19 (800+ quests) uses the same philosophy: its "school system" teaches mod mechanics as interactive tutorials that build on vanilla knowledge, creating a smooth transition from vanilla to modded gameplay.

This rule addresses the sequence inversion problem (三硬伤 #2) from a pedagogical perspective: if modded mechanics are introduced before the player understands the vanilla equivalent, the modded mechanic seems arbitrary rather than enhancing. The vanilla-first approach ensures the player always has a conceptual foundation before encountering mod complexity.

**Implementation check:** For each mod-introduction quest, check whether a vanilla equivalent task exists earlier in the dependency chain. If a mod's first quest requires the player to use a modded machine without a preceding vanilla crafting/furnace equivalent, flag as `INFO — mod introduced without vanilla foundation, player may not understand the mod's purpose`. This is informational because some mods (like FTB Quests itself) have no vanilla equivalent.

**Source:** CSDN doc/6amfp2j2im (vanilla enhancement layering, FTB Quests + GameStages); SevTech Ages ATLauncher page (progressive mod revelation); FTB University MC百科 modpack/996 (school system building on vanilla knowledge).
**Cross-reference:** R14 (teach-then-do ordering), R15 (complexity escalation), R103 (tutorial anchor quest).

---

#### R113 — Multi-Dimensional State Synchronization

**Name:** Multi-Dimensional State Synchronization on Stage Transition
**Severity:** WARNING
**Applicable when:** Expert/semi-gated packs using Game Stages or equivalent progression framework.

The CSDN article on FTB Quests + GameStages integration describes a design pattern where stage transitions dynamically alter multiple game dimensions simultaneously: time (XP and boss requirements), space (biome structures), resources (ore distribution), and social elements (villager trades). Rather than changing only one aspect per stage transition (e.g., unlocking a single mod), the synchronized approach creates a palpable world-change that reinforces the player's sense of progression.

This pattern is independently validated by SevTech Ages, which implements "hiding ore until unlocked, dynamically hidden items and recipes based on progress, new mobs appear as you progress" — all of which change simultaneously when the player reaches a new age. The MC百科 thread-21004 article's dimensional progression principle (R106) validates this from the player experience side: the feeling of "this world is conquered, move to the next world" requires multiple simultaneous changes, not just a new quest chapter.

The technical implementation described in the CSDN article involves a "lightweight bridge mod" that handles event listening and state synchronization between FTB Quests and GameStages, with configuration in `/config` (JSON for quests and stages) and `/scripts` (CraftTweaker for dynamic adjustments to drop rates and recipes based on active stage tags). This is the runtime infrastructure that makes R101 (multi-layer stage enforcement) work as a coherent system rather than a collection of independent locks.

**Implementation check:** For each stage transition (quest that grants a new game stage), count the number of game systems affected: (1) new recipes unlocked, (2) new dimensions/biomes accessible, (3) new ore generation activated, (4) new mob spawns enabled, (5) new villager trades available, (6) UI elements revealed (JEI categories, WAILA overlays, map features). If a stage transition affects fewer than 2 systems, flag as `WARNING — stage transition may feel underwhelming, consider synchronizing changes across multiple game systems`.

**Source:** CSDN doc/6amfp2j2im (multi-dimensional state synchronization, FTB Quests + GameStages bridge); SevTech Ages ATLauncher page (simultaneous ore/item/recipe/mob hiding); MC百科 thread-21004 (dimensional transition feel).
**Cross-reference:** R101 (multi-layer stage enforcement), R106 (dimensional progression naturalism), R38 (tier transition milestone reward).

---

#### R114 — Quest-to-Stage Reward Bridge

**Name:** Quest-to-Stage Reward Bridge Pattern
**Severity:** ERROR (expert) / WARNING (semi-gated)
**Applicable when:** Expert/semi-gated packs using Game Stages or equivalent.

The MC百科 post/2163 (Game Stages wiki translation) explicitly states that "大多数任务mod允许你把'解锁阶段'作为任务奖励" (most quest mods allow setting 'unlock stage' as a quest reward). This describes the bridge pattern that connects FTB Quests' visual dependency graph to Game Stages' runtime enforcement: when the player completes a quest, the quest's reward executes a command (typically `/gamestage add <player> <stage_name>`) that grants the player a new stage, which in turn activates Recipe Stages, Item Stages, Dimension Stages, and other enforcement layers.

The MC百科 post/1938 (Game Stages usage method) reinforces that stage manipulation commands are "更推荐通过CT、KubeJS或FTB Quests等其他mod来执行" (recommended to be executed through CT, KubeJS, or FTB Quests rather than command blocks). This establishes FTB Quests as the preferred bridge between the player-facing progression UI and the server-side enforcement infrastructure.

This rule is the operational implementation of R101 (multi-layer stage enforcement). Without the quest-to-stage bridge, the stage enforcement layers (Recipe Stages, Item Stages, etc.) have no trigger — they exist but never activate because nothing grants the player new stages. The bridge pattern ensures that the quest book's dependency graph and the runtime stage system stay synchronized: every quest that should advance the player's stage does so automatically upon completion.

**Implementation check:** For each quest that represents a stage transition (typically capstone quests, chapter-final quests, or era-gate quests), verify that the quest has a command reward that grants the appropriate game stage. If a quest is the last quest in a chapter and the next chapter requires a new stage, but the quest has no command reward, flag as `ERROR — chapter-final quest does not grant the required game stage, next chapter's content will remain locked`. Additionally, verify that the stage name in the command reward matches the stage name used in Recipe Stages/Item Stages configs (case-sensitive, lowercase + underscores only).

**Source:** MC百科 post/2163 (Game Stages wiki translation, quest reward integration); MC百科 post/1938 (Game Stages usage method, preferred execution methods); MC百科 post/5705 (Recipe Stages stage assignment).
**Cross-reference:** R101 (multi-layer stage enforcement), R10 (reward-to-dependent bridge), R45 (reward guidance bridging), R115 (container-level recipe locking).

---

#### R115 — Container-Level Recipe Locking

**Name:** Container-Level Recipe Locking for Anti-Bypass
**Severity:** ERROR (expert) / WARNING (semi-gated)
**Applicable when:** Expert packs using Recipe Stages with automation mods.

The MC百科 post/5705 (Recipe Stages wiki translation) documents a critical anti-bypass mechanism: `setContainerStages` locks crafting to specific machine types, preventing players from using advanced automation (like Refined Storage or Applied Energistics crafting grids) to bypass recipe stage restrictions. Without container-level locking, a player could set up an AE2 crafting terminal and craft stage-locked recipes before reaching the appropriate stage, because the Recipe Stages mod only checks the player's stage when the player is the crafting entity — not when an automation system crafts on the player's behalf.

The wiki translation describes the debugging workflow: authors use `setPrintContainers` to output the Java class names of machine GUIs to the log file, then apply `setContainerStages` to lock those specific containers to the appropriate stages. This is a defense-in-depth approach that complements R101's multi-layer enforcement: even if Item Stages fails to block an item (e.g., the player obtained it through a trading mod exploit), Recipe Stages with container locking prevents the player from crafting with it in any machine.

This rule addresses the item cross-tier problem (三硬伤 #1) from the automation bypass vector. Expert packs that use automation mods face a unique challenge: the very tools that make late-game gameplay engaging (automated crafting chains) can also be used to skip progression if not properly locked.

**Implementation check:** If the pack includes Recipe Stages and any automation crafting mod (Refined Storage, Applied Energistics, Create, etc.), verify that `setContainerStages` or `setPackageStages` is configured for the automation mod's container classes. If no container-level locking is found, flag as `WARNING — automation mods may bypass Recipe Stages restrictions, consider adding setContainerStages for [mod_name]`. Additionally, check that `setRecipeStageByMod` is applied to all gated mods, with `clearRecipeStage` only for intentionally unlocked basic items.

**Source:** MC百科 post/5705 (Recipe Stages wiki translation, container locking, debugging workflow); MC百科 post/5278 (Greedy Bag staged item pickup, JSON stage naming).
**Cross-reference:** R101 (multi-layer stage enforcement), R114 (quest-to-stage bridge), R4 (stage boundary), R42 (stage-internal item reachability).

---

#### R116 — Advancement-As-Progression-Gate Pattern

**Name:** Advancement-As-Progression-Gate (SevTech Pattern)
**Severity:** INFO
**Applicable when:** Packs that use vanilla advancements as the primary progression system, either instead of or alongside FTB Quests.

SevTech Ages demonstrates a distinctive progression pattern where vanilla advancements serve as the primary gate mechanism: "as you progress through the hundreds of custom advancements you will unlock new 'ages' which will show you new mods." Each age transition simultaneously unlocks new mods, reveals previously hidden ore, activates new recipes, introduces new mobs, and enables new items — all triggered by advancement completion rather than quest completion. The system uses player-based progression ("every progression point is player based and not server based") with optional team sync via the "Together Forever" mod.

This pattern validates the conceptual foundation of MP70 (Tome-Tier Progression Map) from a different implementation angle. MP70 describes using FTB Quests decorative images as tier markers for a progression roadmap; SevTech Ages uses vanilla advancements as the equivalent tier markers. Both patterns share the same core idea: a visible, trackable progression milestone system where each milestone unlocks a new "tier" of gameplay content. The key difference is implementation: FTB Quests provides visual customization (decorative images, custom shapes, quest descriptions) while vanilla advancements provide universal accessibility (every player has the advancement UI without needing the quest book open).

This rule is informational rather than prescriptive — it documents a validated alternative to the FTB Quests-native approach for packs that prefer vanilla integration. Authors who combine FTB Quests with vanilla advancements can use this pattern to create a dual-layer progression system where the quest book provides detailed guidance and the advancement system provides the hard gate.

**Implementation check:** If the pack uses vanilla advancements as progression gates, verify that each age/tier transition has: (1) a custom advancement that requires completion of multiple prerequisite advancements, (2) ore visibility changes tied to the age transition, (3) recipe visibility changes tied to the age transition, and (4) mob spawn changes tied to the age transition. If any of these four elements is missing, flag as `INFO — age transition may not feel comprehensive, consider adding [missing element] for a more synchronized stage change (R113)`.

**Source:** SevTech Ages ATLauncher page (vanilla advancement age gates, player-based progression, Together Forever team sync); MC百科 class/3668 (进度之书 mod, 8 packs using advancement book).
**Cross-reference:** MP70 (tome-tier progression map), R113 (multi-dimensional state synchronization), R106 (dimensional progression naturalism), R112 (vanilla enhancement layering).

---

#### How the three hard problems map to international-author-design-philosophy rules

The Cycle 17 Phase 3 research reveals that Chinese and international pack-making traditions independently converged on similar solutions to the three hard problems, but articulate them through different cultural lenses and implement them through different technical stacks.

**Item cross-tier (三硬伤 #1) — R107 + R108 + R109 + R115.** The international approach to preventing item cross-tier emphasizes world-generation manipulation (R109) and automation-bypass prevention (R115), complementing the Chinese approach of runtime stage locking (R101) and architectural era separation (R102). The MC百科 thread-21004 article's material-binding principle (R109) addresses the physical availability vector: if the ore doesn't generate in the wrong dimension, no runtime lock is needed for that specific item. The SevTech Ages approach validates this: "hiding ore until unlocked" is a world-generation-level enforcement that prevents cross-tier at the source. R115 addresses the automation vector that expert packs face: even with perfect stage locking, automation mods can bypass restrictions if container-level locking is not configured. Together, R101 (runtime) + R109 (physical) + R115 (automation) create a three-vector defense that covers all known cross-tier bypass paths.

**Sequence inversion (三硬伤 #2) — R106 + R108 + R112.** The international approach to preventing sequence inversion emphasizes motivational design (R106) and pedagogical sequencing (R112), complementing the Chinese approach of architectural gates (R102) and tutorial anchors (R103). The MC百科 thread-21004 article's "这个世界无敌了" principle (R106) ensures that the player wants to progress rather than being forced to progress — intrinsic motivation prevents sequence inversion because the player follows the intended path voluntarily. The vanilla enhancement layering principle (R112) ensures that the player understands vanilla mechanics before encountering mod complexity, preventing the confusion that leads to unintentional sequence breaking. R108's gear-to-mob scaling ensures that even if the player reaches a new dimension early, they cannot dominate it without the intended gear progression.

**Reward disconnection (三硬伤 #3) — R110 + R111 + R113 + R114.** The international approach to preventing reward disconnection emphasizes synchronized world changes (R113) and quest-to-stage bridge patterns (R114), complementing the Chinese approach of crafting variety (R104) and accessibility ceilings (R105). The CSDN article's multi-dimensional synchronization (R113) ensures that every stage transition is a meaningful reward — the player doesn't just get an item, they get a world-change. The quest-to-stage bridge (R114) ensures that the reward system is tightly coupled to the enforcement system: completing a quest immediately and visibly changes the game world. R110's mid-game density priority ensures that rewards are concentrated where most players spend most of their time, while R111 prevents the anti-pattern of grinding rewards through forced lifespan extension.

---

#### New tensions from international author design philosophy

**Tension 7: Naturalism (R106) vs. multi-layer enforcement (R101).** R106 advocates for progression that feels natural and intrinsically motivated ("this world is conquered"), while R101 advocates for defense-in-depth technical enforcement. The resolution is complementary: use naturalism as the design intent (the player should feel motivated to progress) and multi-layer enforcement as the safety net (even if the player finds an unintended shortcut, the enforcement layers prevent cross-tier). SevTech Ages demonstrates this resolution: the advancement system feels natural (you discover new ages by playing), but the ore hiding, item hiding, and recipe hiding provide technical enforcement that prevents bypass.

**Tension 8: Olive-shaped distribution (R107) vs. anti-forced-lifespan (R111).** R107 suggests mid-game should be the densest phase (more equipment options), while R111 warns against artificially extending playtime. The resolution is quality vs. quantity: R107 refers to the variety of meaningful options available at each tier, while R111 targets repetitive content that inflates playtime without adding variety. A mid-game with 50 diverse equipment options across 5 mods is olive-shaped and engaging; a mid-game with 50 variations of the same sword at incrementally higher damage values is forced lifespan extension.

**Tension 9: Vanilla enhancement layering (R112) vs. early-game acceleration (R110).** R112 suggests introducing mods gradually on top of vanilla foundations, while R110 suggests transitioning to mid-game quickly. The resolution is parallel introduction: introduce multiple mods simultaneously in the early-to-mid transition, each building on a different vanilla mechanic. The player learns several mods in parallel (accelerating the transition) while each mod is anchored to a vanilla concept they already understand (maintaining the enhancement layering).

The Cycle 16 Phase 3 author design practices reveal that experienced pack makers solve the three hard problems through systematic, layered approaches that go beyond individual quest design.

**Item cross-tier (三硬伤 #1) — R101 + R102 + R104.** The author-design-practice approach to preventing item cross-tier is layered and architectural. R101 provides defense-in-depth through multiple independent stage-locking mechanisms (quest dependencies + Game Stages + Item Stages + Recipe Stages + Ore Stages), so that even if one layer fails, others prevent the player from using out-of-stage items. R102 organizes the entire pack into eras with clear boundaries, making cross-era item leakage structurally unlikely. R104 ensures that within each era, the variety of crafting methods prevents the "grind to skip" behavior that leads to accidental cross-tier progression. Together, these rules address cross-tier at three levels: technical enforcement (R101), architectural separation (R102), and behavioral prevention (R104).

**Sequence inversion (三硬伤 #2) — R102 + R103.** The author-design-practice approach to preventing sequence inversion combines architectural gates with player guidance. R102's era transitions serve as hard gates that the player cannot bypass through quest-book manipulation alone. R103's tutorial anchor quest ensures the player always knows where they are in the progression sequence, reducing the confusion that leads to unintentional sequence breaking. The MC百科 post/4382 article's "弱锁" (weak lock) philosophy adds nuance: allow clever players to find shortcuts within an era (which feels rewarding), but prevent shortcuts across era boundaries (which would break progression).

**Reward disconnection (三硬伤 #3) — R103 + R104 + R105.** The author-design-practice approach to preventing reward disconnection focuses on quest design quality and content accessibility. R103 ensures that tutorial rewards teach the player how the reward economy works from the very first quest. R104's crafting variety ensures that rewards are meaningful (they enable new crafting methods, not just more of the same). R105 ensures that rewards are accessible to the majority of players — if 60% of players never reach the content where a reward matters, the reward is effectively disconnected from the player's experience.

---

#### New tensions from author design practices

**Tension 5: Multi-layer enforcement vs. weak lock philosophy.** R101 (multi-layer stage enforcement) advocates defense-in-depth with hard locks at multiple levels, while R83 (weak lock permeability) and the post/4382 article advocate weak locks that allow creative bypass. The resolution is scope-based: use hard stage enforcement for cross-era boundaries (where sequence breaking would be catastrophic), but use weak locks within an era (where a clever shortcut is a reward, not a bug). The Game Stages framework enforces the macro-progression; the quest-book's weak locks provide micro-progression flexibility.

**Tension 6: 60% accessibility vs. depth for completionists.** R105 (60% content accessibility ceiling) ensures casual players can reach most content, while expert packs traditionally demand 100% engagement. The resolution is the C2MSE2 hidden-chapter pattern: the main quest line provides 60% accessibility for casual players, while optional side chains and the hidden 15th chapter provide depth for completionists. The 60% floor is not a ceiling — it's the minimum viable experience.

---

### Cycle 18 Phase 3 — Trading Bypass Defense, Author Design Philosophy, and Progression Integrity Rules

The Cycle 18 Phase 3 research searched 9 platforms (Bilibili, MC百科, Reddit r/feedthebeast, klpbbs.com, CSDN, GitHub FTBTeam, mczfw.com, 知乎, MineBBS) for author interviews, design philosophy articles, and progression defense techniques. The most productive sources were MC百科 post/4382 (re-validated for weak-lock philosophy and mob tier classification), MC百科 post/6155 (adventure pack design insights with flow clarity principles), Nova Engineering's MC百科 page (narrative research system as alternative to traditional quest gates), klpbbs.com thread-130537 (comprehensive expert modpack mod list including Profession Lock), and the Profession Lock mod page (villager profession permanent locking for anti-exploit). These sources provide the basis for 8 new progression rules (R117–R124) that specifically address the AP42 (Villager Trading Hall Bypass) defense gap and expand the three-hard-problem defense matrix with acquisition-method verification, tech-level gating, and narrative-driven progression.

---

#### R117 — Villager Trade Progression Gating

**Name:** Villager Trade Progression Gating
**Severity:** WARNING (non-expert) / ERROR (expert/semi-gated)
**Applicable when:** Any pack using FTB Quests with item-submission tasks in a modpack that includes vanilla villager trading mechanics.

AP42 (Villager Trading Hall Bypass) documents the failure mode where vanilla villager trading provides quest-required items without following the intended progression path. This rule provides the progression-rule-level defense that AP42's fix section describes at the implementation level. The core insight is that FTB Quests item-submission tasks check only item presence, not acquisition method — and villager trading is the most commonly available alternative acquisition path in non-expert packs.

The defense strategy is tiered based on the pack's gating philosophy. For expert packs (Game Stages + Item Stages + Recipe Stages), villager trading should be gated through Item Stages (items the player hasn't unlocked cannot be received from trades) and custom villager trade modification (datapack removal of trades that provide progression-critical items). For semi-gated packs (some stage locking but not full Game Stages), the Profession Lock mod prevents villager profession cycling exploits while custom trade datapacks remove the specific trades that overlap with quest requirements. For non-expert packs with open-gating philosophy (like Engineer's Life 2's "if you have resources, you can craft anytime"), the minimum defense is a text quest at the pack start warning players that villager trading may bypass intended progression, plus targeted trade restrictions on the 3–5 most progression-critical items (typically enchanted books, emerald-based goods, and mod-specific seeds or components).

**Implementation check:** For each item-submission quest in the pack, check whether the required item can be obtained through vanilla villager trading. If yes, and the pack uses any form of stage gating, flag as `ERROR — item [X] required by quest [Y] is obtainable through villager trading, bypassing stage gate`. If the pack uses open-gating philosophy, flag as `WARNING — item [X] is obtainable through villager trading, which may reduce engagement with the intended crafting chain; consider adding a text quest or observation prerequisite`. For expert packs, additionally verify that the Profession Lock mod (or equivalent) is installed to prevent workstation cycling exploits.
**Source:** klpbbs.com thread-130537 (expert modpack常用模组, Game Stages ecosystem, Profession Lock); Profession Lock MC百科 class/9288 (permanent profession locking, "打破了沉浸感，让游戏变得更加简单"); MC百科 post/1015 (Game Stages ecosystem, Item Stages hiding); MC百科 modpack/191 (Engineer's Life 2 open-gating philosophy).
**Cross-reference:** AP42 (Villager Trading Hall Bypass), R101 (multi-layer stage enforcement), R115 (container-level recipe locking), R83 (weak lock permeability), Lesson 121 (open-gating vulnerability).

**L1 Heuristic Fallback:** When villager trading tables are not available for inspection (the common case — FTB Quests config does not contain villager trade data, and the pack's datapack or trade modification scripts may not be present in the config directory), flag the following item categories as `POTENTIAL_TRADING_BYPASS` without querying trade tables: (1) enchanted books, (2) emeralds / emerald blocks, (3) glass / stained glass, (4) crops (wheat, carrots, potatoes, beetroot), (5) books / paper / maps. These are the most commonly tradeable vanilla items and represent the highest-probability bypass vectors. When the pack uses modded villager trades (e.g., via MCA Reborn or custom trade mods), additionally flag any mod item whose namespace matches a tradeable good listed in the mod's trade registry — but only if the registry file is accessible. This fallback is deliberately conservative: it over-flags rather than under-flags, producing false positives that the author can dismiss rather than false negatives that let bypasses slip through.

---

#### R118 — Acquisition-Method Verification Layer

**Name:** Acquisition-Method Verification Layer (Engagement Proof)
**Severity:** WARNING
**Applicable when:** Packs where the quest book's pedagogical intent requires the player to engage with a specific mod or crafting system, not merely possess an item.

FTB Quests item-submission tasks verify possession but not provenance. This rule formalizes the principle that when acquisition method matters for pedagogical reasons (teaching the player how to use a mod), the quest should include supplementary verification tasks that prove engagement. The most common supplementary task types are: (1) observation tasks requiring the player to inspect a specific machine or block, (2) statistics tasks requiring the player to craft a certain number of items with a specific mod, (3) prerequisite text tasks that describe the crafting process the player should follow, and (4) Item Stages gating that prevents the item from being usable until the player has completed the prerequisite quests.

The create-advanced-industries pack validates this approach through its systematic use of `optional_task: true` on observation tasks within quests that also have item tasks (Lesson 120). This creates a "learn then do" pattern: the player can optionally observe the machine (building familiarity) but must submit the output (proving capability). Nova Engineering's narrative research system validates a more intensive variant: the player must complete research tasks (which require interacting with specific machines and systems) before the tech level advances, effectively using the research system as an engagement verification layer that replaces traditional item-submission gating.

**Implementation check:** For each item-submission quest that gates access to a new mod or technology, check whether the quest includes at least one supplementary verification task (observation, statistics, or prerequisite text). If the quest is a pure item-submission with no supplementary verification and the item is obtainable through multiple acquisition paths (crafting, trading, mob drops, dungeon loot), flag as `WARNING — quest teaches nothing about the mod's systems; consider adding an observation task for [machine/block] or a statistics task for [crafting count]`.
**Source:** Nova Engineering MC百科 modpack/784 (narrative research system, "原创剧情化研究系统，贯穿发展全线"); create-advanced-industries (Lesson 120, optional_task observation pattern); MC百科 post/6155 (deep modification of core mod to span entire playthrough as progression method).
**Cross-reference:** R14 (teach-then-do ordering), R103 (tutorial anchor quest), AP42 (Villager Trading Hall Bypass), R117 (Villager Trade Progression Gating).

---

#### R119 — Tech-Level Continuous Progression Scale

**[Design Guidance — not executable as config check. Requires custom mod or scripting framework (e.g., Nova Engineering's HyperNet). Not achievable with standard FTB Quests + Game Stages alone.]**

**Name:** Tech-Level Continuous Progression Scale
**Severity:** INFO
**Applicable when:** Expert packs with more than 3 distinct progression tiers or 50+ quests that use a tiered technology system. Requires a custom mod or scripting framework (e.g., Nova Engineering's HyperNet). Not achievable with standard FTB Quests + Game Stages alone.

Nova Engineering demonstrates a distinctive progression pattern where a continuous numerical tech level (1.0 to 14.0, divided into five eras) replaces binary stage gates. Each item, recipe, and machine is tagged with a minimum required tech level, and the player's tech level advances through completing research tasks. The tech level "直接反映了玩家当前阶段对于目标物品的难度" (directly reflects the player's current stage difficulty relative to the target item). This creates a finer-grained progression than binary "locked/unlocked" gates: the player's progression is a continuous number rather than a discrete stage, allowing gradual capability expansion within each era.

This pattern validates the conceptual foundation of R101 (multi-layer stage enforcement) from a granularity perspective. Binary stage gates create abrupt transitions where the player goes from "cannot use anything" to "can use everything" at a stage boundary. A continuous scale allows gradual unlocking within each era — tier 3.5 items become available before tier 4.0 items, creating a smoother progression curve that reduces the temptation to skip ahead. The approach also addresses reward disconnection (三硬伤 #3): when the tech level itself is the reward (each increment unlocks new recipes and capabilities), every quest that advances the tech level provides a meaningful reward that never becomes obsolete.

**Implementation check:** If the pack uses a tech-level system (continuous numerical progression or discrete tier numbers), verify that: (1) every progression-locked item has a clear minimum tech level requirement, (2) every recipe checks the player's tech level before allowing crafting, (3) tech level advancement is tied to completing specific quests or research tasks (not passive time accumulation), and (4) the player can see their current tech level at all times. If any element is missing, flag as `INFO — tech level system may benefit from [missing element] for smoother progression`.
**Source:** Nova Engineering MC百科 modpack/784 (Tech Level 1.0–14.0, five eras, "直接反映了玩家当前阶段对于目标物品的难度", HyperNet research system); MC百科 thread-21004 (Vazkii mob tier classification validating tier-based progression).
**Cross-reference:** R101 (multi-layer stage enforcement), R102 (era-based architecture), R92 (tier system calibration), R113 (multi-dimensional state synchronization), Lesson 129 (continuous tech level as fine-grained stage gating).

---

#### R120 — Narrative-Driven Research Progression

**Name:** Narrative-Driven Research as Progression Gate
**Severity:** INFO
**Applicable when:** Expert packs with 100+ hours of content that want an alternative to traditional quest-dependency progression gates. This pattern requires a custom research framework and 100+ original content pieces. Documented as a design possibility, not a recommendation.

Nova Engineering's "原创剧情化研究系统，贯穿发展全线" (original narrative-driven research system threading through the entire progression line) demonstrates that a story-based research system can replace traditional quest-dependency progression as the primary gating mechanism. Each research task requires the player to interact with specific machines and systems, and the research narrative provides context for why the player is doing each task. The system deliberately ensures "耗时均不超过半个小时" (time cost does not exceed half an hour) and avoids "漫长的等待" (long waits) and "大量无用的前置研究" (large amounts of useless prerequisite research).

This pattern addresses sequence inversion (三硬伤 #2) from a narrative perspective: if the research tasks form a coherent story, the player is motivated to complete them in order because breaking the sequence breaks the narrative coherence. It also addresses reward disconnection (三硬伤 #3): the research system IS the reward (completing research feels intrinsically rewarding because it advances the story and unlocks new capabilities). The key design constraint is the 30-minute-per-task limit — research tasks that take too long become "漫长的等待" and undermine the narrative momentum.

**Implementation check:** If the pack uses a narrative research system, verify that: (1) the research narrative forms a coherent story arc from start to finish, (2) individual research tasks take no more than 30 minutes of active play, (3) research tasks require interaction with specific machines or systems (not just waiting or resource submission), and (4) research completion unlocks meaningful capabilities (new recipes, machines, or tech level advancement). If any element is missing, flag as `INFO — narrative research system may benefit from [missing element]`.
**Source:** Nova Engineering MC百科 modpack/784 ("原创剧情化研究系统，贯穿发展全线", "耗时均不超过半个小时", "避免漫长的等待和大量无用的前置研究").
**Cross-reference:** R82 (backward design, book-level arc), R103 (tutorial anchor quest), R106 (dimensional naturalism — narrative progression should feel natural), R118 (acquisition-method verification — research tasks as engagement proof).

---

#### R121 — Equipment Tier Transition Smoothness

**[Design Guidance — requires game balance data not available in quest config. Use vanilla tier order (wood < stone < iron < diamond < netherite) as proxy for mod items.]**

**Name:** Equipment Tier Transition Smoothness (Vazkii Mob-Tier Principle)
**Severity:** WARNING
**Applicable when:** Packs with dimension-gated progression and tiered equipment (3+ tiers across 2+ dimensions).

Vazkii's modpack design philosophy (as documented in MC百科 thread-21004) establishes the principle that "前一个维度的终极装备应该与新领域的基础怪物匹配" (the previous dimension's ultimate gear should match the new realm's weakest mobs). This creates a smooth "bridge" at the tier boundary: the player enters the new content feeling competent (their old gear works on easy mobs) but motivated to upgrade (they need new gear for harder mobs). Vazkii classifies enemies into four tiers, with each tier's basic mobs matching the previous tier's endgame gear in power level, and each tier's boss mobs requiring the current tier's mid-game gear to defeat.

This rule addresses sequence inversion (三硬伤 #2) from the combat balance perspective: if the new dimension's mobs are too hard for the previous tier's best gear, the player is stuck and cannot progress without backtracking. If the new dimension's mobs are too easy for the old gear, the player has no motivation to engage with the new tier's content. The sweet spot is where the old gear is adequate for survival but inadequate for dominance — the player can explore safely but needs new equipment to tackle the dimension's challenges and bosses. The MC百科 post/6155 adventure pack article independently validates this: "最好的装备能舒适地打败当前基础怪物" (the best equipment should comfortably defeat current basic mobs).

**Implementation check:** For each dimension transition or tier boundary, verify that: (1) the previous tier's best armor and weapons can defeat the new dimension's basic mobs (but not bosses) within a reasonable fight duration, (2) the new dimension's basic resource drops can craft equipment noticeably better than the previous tier's best, and (3) the new dimension's bosses require the new tier's mid-game equipment to defeat. If condition (1) fails, flag as `WARNING — tier transition too harsh, player cannot explore new dimension with previous gear`. If condition (2) fails, flag as `WARNING — no motivation to upgrade equipment in new dimension`. If condition (3) fails, flag as `WARNING — boss too easy with old gear, no progression gate`.
**Source:** MC百科 thread-21004 (Vazkii four-tier mob classification, "前一个维度的终极装备应该与新领域的基础怪物匹配"); MC百科 post/6155 (adventure pack difficulty progression, equipment tier bridging); MC百科 post/4382 (gear strength control via dimension restriction).
**Cross-reference:** R108 (gear-to-mob scaling), R106 (dimensional naturalism), R93 (anti-nerf dimension transitions), R107 (olive-shaped equipment distribution).

---

#### R122 — Kitchen-Sink Pack Flow Clarity

**Name:** Kitchen-Sink Pack Flow Clarity (Anti-Overwhelm Guidance)
**Severity:** WARNING
**Applicable when:** Kitchen-sink or large multi-mod packs with more than 50 mods and 3+ quest chapters.

The MC百科 post/6155 article identifies a specific failure mode of "水槽包" (kitchen-sink packs): they "流程和引导不够明晰" (lack clear flow and guidance), causing players to feel overwhelmed by the number of available mods and quit before finding a progression direction. The fix is not to reduce mod count (which contradicts the kitchen-sink genre) but to provide an explicit primary progression spine that the player can follow, with side content available but clearly marked as optional.

This rule addresses reward disconnection (三硬伤 #3) from the navigation perspective: if the player cannot identify which quest chapter to pursue, they may pursue chapters in an order that makes rewards feel disconnected (e.g., completing a magic chapter that rewards magic items when the player is building a tech base). The primary spine should be the chapter sequence that makes the most rewards feel relevant to the player's current activities. The MC百科 post/6155 article validates the 60% accessibility principle (R105) from a different angle: ensuring players experience "至少60%的内容" (at least 60% of the content) requires clear guidance toward that 60%, not just making it available.

**Implementation check:** If the pack has more than 3 quest chapters covering different mods, verify that: (1) there is a clear starting chapter that introduces the pack's primary progression direction, (2) the quest book's chapter ordering or visual hierarchy communicates which chapters are primary vs. optional, (3) the first quest in the pack tells the player what to do first and where to go next, and (4) at least 60% of the pack's chapters are reachable by following the primary spine without requiring side content completion. If any element is missing, flag as `WARNING — kitchen-sink pack may lack clear flow guidance; players may feel overwhelmed and quit`.
**Source:** MC百科 post/6155 ("水槽包" failure from "流程和引导不够明晰", ensuring 60% content experience); MC百科 post/4382 (consistent visual styles for task branches, "什么提示要详细？什么提示要神秘？这都要靠你的经验").
**Cross-reference:** R105 (60% content accessibility), R41 (early-game flexible progression), AP41 (flat presentation hierarchy), R103 (tutorial anchor quest).

---

#### R123 — Open-Gating Compensatory Defense

**Name:** Open-Gating Compensatory Defense
**Severity:** WARNING
**Applicable when:** Non-expert packs that deliberately choose not to lock progression behind stages or recipes.

Engineer's Life 2 explicitly states "进度并没有被限制在某些东西后面...如果你有资源，你可以随时制作" (progression is not locked behind certain things... if you have resources, you can craft anytime). This open-gating philosophy (rooted in the "KISS原则" — Keep It Simple, Stupid) is player-friendly but creates a structural vulnerability: any alternative acquisition path (villager trading, mob farm drops, dungeon loot, creative mode) can bypass the intended progression without triggering any enforcement mechanism. The more open the gating, the more important it is to implement compensatory defenses.

The compensatory defense strategy has three layers. Layer 1 is documentation: a text quest at the pack start explicitly states the progression philosophy and warns that alternative acquisition paths may reduce the intended experience. Layer 2 is selective restriction: identify the 5–10 items whose early acquisition would most damage the progression experience (typically items that gate access to major technologies or dimensions) and restrict those specific items' alternative acquisition paths (even in an otherwise open pack). Layer 3 is engagement verification: add observation or statistics tasks to key progression quests that verify the player engaged with the intended crafting process, not just obtained the item through an alternative path. This rule is the progression-rule-level formalization of Lesson 121 (open-gating creates inherent vulnerability).

**Implementation check:** If the pack uses open-gating philosophy (no Game Stages, no Item Stages, no Recipe Stages), verify that: (1) a text quest at the pack start documents the progression philosophy and warns about alternative acquisition paths, (2) the 5–10 most progression-critical items have at least one alternative acquisition path restricted, and (3) key progression quests include supplementary engagement verification tasks. If layer 1 is missing, flag as `WARNING — open-gating pack lacks progression philosophy documentation`. If layer 2 or 3 is missing, flag as `WARNING — open-gating pack lacks compensatory defense against progression bypass`.
**Source:** MC百科 modpack/191 (Engineer's Life 2, "KISS原则", "如果你有资源，你可以随时制作"); MC百科 post/6155 (kitchen-sink failure from unclear flow, two methods for stage management).
**Cross-reference:** AP42 (Villager Trading Hall Bypass), R117 (Villager Trade Progression Gating), R83 (weak lock permeability), Lesson 121 (open-gating vulnerability), R122 (kitchen-sink flow clarity).

---

#### R124 — Author Playtesting Requirement

**[Author Process — not verifiable from config. Include as output reminder when generating complete packs.]**

**Name:** Author Playtesting Requirement (己所不欲，勿施于人)
**Severity:** INFO
**Applicable when:** All packs before initial public release.

Two independent Chinese community articles establish the same principle: "不敢玩自己的整合包的作者一定不是一个好作者" (an author who doesn't dare play their own modpack is certainly not a good author — MC百科 post/4382) and "作者应该亲自玩自己的整合包" (authors should personally play their own modpack — MC百科 post/6155). The MC百科 post/4382 article frames this as the ancient wisdom of "己所不欲，勿施于人" (do not do unto others what you would not have them do unto you): you cannot expect players to enjoy a pack you would not play yourself.

This rule addresses all three hard problems from the quality assurance perspective. Item cross-tier (三硬伤 #1) is caught when the author personally attempts to progress through the pack and discovers that items are available too early or too late. Sequence inversion (三硬伤 #2) is caught when the author follows the quest line and discovers that tutorials teach concepts in the wrong order or that prerequisites are missing. Reward disconnection (三硬伤 #3) is caught when the author receives quest rewards and discovers they are not useful for the next progression step. No automated check can replace the author's subjective experience of progression flow; the playtesting requirement ensures that at least one person has experienced the full progression before any player encounters it.

**Implementation check:** This rule is a process requirement rather than a config check. For QA purposes, verify that: (1) the pack author has documented their playtesting progress (e.g., a changelog noting which chapters have been personally tested), (2) at least 60% of the quest line has been playtested by the author before initial release (aligning with R105's 60% accessibility principle), and (3) the playtesting covered the critical progression path (not just side content). If the pack has known progression issues in the first 3 chapters that would have been caught by basic playtesting, flag as `INFO — pack appears unplaytested; critical progression issues found in early chapters`. Playtesting should include at least one deliberate bypass attempt: construct a villager trading hall, check mob farm outputs, and attempt to acquire gated items through non-intended paths. This specifically validates the R117/R118/R123 defense layers — if the author can bypass progression through legitimate game mechanics, the defense is incomplete.
**Source:** MC百科 post/4382 ("不敢玩自己的整合包的作者一定不是一个好作者", "己所不欲，勿施于人"); MC百科 post/6155 ("作者应该亲自玩自己的整合包").
**Cross-reference:** R105 (60% content accessibility — the author should playtest at least 60%), R32 (chapter QA coverage), AP45 (unplaytested release), Lesson 130 (playtesting as fundamental quality requirement).

---

#### R125 — Quest Reward Progression-Trivialization Check

**Name:** Quest Reward Progression-Trivialization Check
**Severity:** WARNING
**Applicable when:** Any quest rewards an item that the player could not yet craft through the intended progression chain, or when the reward item provides capabilities that bypass upcoming progression milestones.

The ATM-10 community debate (GitHub discussions #3539) crystallizes a fundamental tension in kitchen-sink quest reward design: a player complained that quest rewards handing out a Dragon Egg, Ender Chests, and an Ultimate Universal Cable "well before such items are naturally achievable" made the progression feel "skipped for no reason." A collaborator countered that this is "a kitchen sink pack" where early utility items don't let players "beat the game." Both positions have merit, but the underlying principle is clear: quest rewards that provide items the player *could* craft later through intended means create a paradox where the reward renders the intended crafting journey pointless. The specific case that triggered the complaint — an "ore sight charm" obtainable for just "4 nuggets" that instantly locates allthemodium — demonstrates the damage: it completely ruins the developers' intended scarcity and mining difficulty for the pack's signature rare resource.

The trivialization check operates at three levels. Level 1 (item-tier check): compare the reward item's position in the crafting dependency graph against the quest's position in the quest dependency graph — if the reward item is deeper in the crafting chain than the quest is in the quest chain, the reward hands the player something they haven't "earned" through the quest progression. Level 2 (capability-bypass check): identify whether the reward item grants a capability (flight, teleportation, auto-mining, ore detection) that removes an upcoming quest's *challenge* rather than merely supplying a *tool*. Level 3 (scarcity-nullification check): if the pack deliberately restricts a resource's availability (allthemodium, Draconic cores, Neutronium), verify that no quest reward provides that resource or a tool that trivially obtains it before the player has engaged with the intended acquisition process.

The multiplayer dimension compounds this problem: in server play, "progression is shared and duplicates can be op," meaning one player's quest reward can trivialize progression for the entire team. This rule does not contradict R12 (Reward Value Progression), which focuses on the *magnitude* of rewards increasing over time. R125 focuses on the *type* of reward — specifically whether it provides a capability or resource that short-circuits the next stage's intended challenge.

**Prerequisites:** Level 1 (item-tier check) requires access to the pack's recipe graph (KubeJS recipes, mod recipe data, or a pre-built recipe-depth index) — the quest config alone does not contain crafting chain depth information. Level 3 (scarcity-nullification check) requires the pack author to provide a "scarcity list" of deliberately restricted resources, either as a config file or as an interview-time declaration. Multiplayer severity escalation requires knowing whether the pack uses team-shared progression (e.g., FTB Teams with shared quest completion) — ask during the Step 2 interview. If these prerequisites are not available, the agent should skip the affected levels and note the gap in the Step 5 report.
**Implementation check:** For each quest that has an item reward, (1) resolve the reward item's crafting chain depth in the recipe graph, (2) compare against the quest's dependency depth in the quest graph, (3) flag as `WARNING — quest reward item [X] has crafting depth D1 but quest has dependency depth D2 where D1 > D2; reward may trivialize intended progression` if the reward item is deeper in crafting than the quest is in dependencies. Additionally, maintain a pack-level "scarcity list" of deliberately restricted resources (configurable by the pack author) and flag any quest that rewards a scarcity-list item or a tool that trivially obtains it as `WARNING — quest reward trivializes pack-scarcity resource [X]`. For multiplayer packs, multiply the severity: if the pack supports team-shared progression, flag as `ERROR` instead of `WARNING`.

**Edge case notes:**
- **Scarcity list initialization:** If the pack author does not provide an explicit scarcity list, the checker should auto-generate a candidate list by identifying resources whose world-generation is restricted (e.g., Ore Stages gated, dimension-gated, or boss-drop-only) and resources that appear as quest-dependency bottlenecks (≥3 quests depend on the same resource). Flag the auto-generated list as `INFO — auto-generated scarcity list; author should review and confirm`.
- **Convenience vs. trivialization boundary:** A reward that provides a *convenience* improvement (e.g., a backpack that expands inventory, a faster pickaxe for already-accessible ores) is acceptable even if it slightly accelerates progression. A reward that provides *trivialization* (e.g., an ore-sight charm for a deliberately-scarce resource, a flight ring in a pack where flight is gated) removes the *challenge* itself, not just the *tedium*. The test: if removing the reward would force the player to engage with a meaningful gameplay system (mining, exploration, puzzle-solving), the reward is trivializing. If removing it would only add time or clicks, the reward is a convenience.
- **Version-update risk:** Quest reward trivialization can emerge after mod updates that change item capabilities or crafting recipes. A reward that was balanced in v1.0 may become trivializing in v1.1 if the mod author buffs the item. Pack authors should re-verify R125 after any mod version change.
**Source:** ATM-10 GitHub discussions #3539 ("The Quest Book gives way too many rewards that break balance", "Dragon Egg / Ender Chests / Ultimate Universal Cable" before naturally achievable, "ore sight charm" trivializing allthemodium scarcity); cesspit.net node/2832 ("players bee lining right to end game in no time, rendering most content irrelevant").
**Cross-reference:** R12 (reward value progression), R10 (reward-to-dependent bridge), R4 (stage boundary), AP42 (trading hall bypass — same trivialization via different vector), R118 (acquisition-method verification).

---

#### R126 — Quest Task Detection Alignment

**Name:** Quest Task Detection Alignment
**Severity:** ERROR
**Applicable when:** Any quest uses item-crafting, item-collection, or block-placing tasks where the detection trigger could match unintended items or actions.

FTB Skies GitHub issue #3248 catalogs a devastating quest detection failure: "quests are not completing even with the item done." Players who crafted the correct items found that the quest book did not register completion. Worse, the detection misalignment caused *wrong* quests to complete: "harvesting flax incorrectly completed a cobblestone quest, while the flax quest only updated later when a chest was built." This represents the inverse failure mode — the quest detection system fires on an unrelated action, completing quest B when the player performs action A. The issue was version-update-induced (1.0.6 → 1.0.7) and likely related to a "unified system with the rainbow ingot icon" that confused the item-matching logic. The frustrated responses — enabling cheat mode to force completions, downgrading to the previous version — demonstrate that task detection failures break the fundamental contract between quest book and player: "do what the quest asks, get the reward."

The detection alignment problem has three root causes. Cause 1 (item unification collision): when multiple mods provide the same item (e.g., copper ingot from Mekanism, Thermal, Immersive Engineering), the quest task's item ID may not match the variant the player actually crafted. Ore Dictionary / Forge Tag matching mitigates this but can over-match: a task requesting "any copper ingot" may accept a mod-specific variant that has different NBT or capabilities. Cause 2 (NBT sensitivity mismatch): FTB Quests offers three NBT matching modes — `match` (exact), `ignore` (any NBT accepted), and `contain` (reward NBT is a superset). Selecting the wrong mode means either valid items are rejected (too strict) or invalid items are accepted (too loose). Cause 3 (trigger timing lag): the quest update cycle may not fire immediately on crafting — it might require a chunk reload, inventory refresh, or unrelated action to trigger, creating the illusion that the quest is broken.

**Prerequisites:** Checks (1) and (4) require knowing the pack's item unification targets — which mod's variant of each item is canonical. This is typically defined in KubeJS unification scripts (`kubejs/server_scripts/`) or a unification mod's config (e.g., Almost Unified, ChemLib). If the pack has no unification system, these checks are not applicable. Check (2) — Forge Tag resolution — requires access to the pack's data pack tag files (`data/<mod>/tags/`), which are typically available in the modpack directory. Check (3) — NBT matching mode — is fully executable from quest config alone, as the matching mode is a field on the task object.
**Implementation check:** For each quest with an item task, verify: (1) the task's item ID matches the canonical item ID used in the pack's unification system (e.g., if the pack unifies to `thermal:copper_ingot`, the quest must request `thermal:copper_ingot`, not `mekanism:ingot_copper`), (2) if the task uses Ore Dictionary / Forge Tag matching, verify the tag resolves to the intended item set and not a superset that includes unintended items, (3) the NBT matching mode is explicitly set (not relying on default) and is appropriate for the item type (exact for NBT-dependent items like enchanted tools, ignore for simple materials), and (4) if the pack uses an item unification mod, verify the quest task item ID matches the unification target. Flag mismatches as `ERROR — quest task item [X] does not match pack unification target [Y]; detection failure likely`.

**Edge case notes:**
- **Version-regression detection:** The FTB Skies #3248 failure was version-update-induced (1.0.6 → 1.0.7). When the pack updates FTB Quests or any mod that provides items referenced in quest tasks, re-run R126 checks on all affected quests. Flag as `ERROR — version change detected for mod [X]; re-verify all quest tasks referencing items from this mod`.
- **Fluid task detection:** This rule's implementation check focuses on item tasks but the same detection alignment principles apply to fluid tasks (fluid ID matching, NBT/data-component matching for modded fluids). For packs with fluid tasks (e.g., GTLS EV Case 63), verify fluid task IDs match the pack's canonical fluid registry.
- **Trigger timing lag fix:** Cause 3 (trigger timing lag) has no config-level fix — it is a mod-engine limitation. The practical mitigation is to add a quest description note warning players: "If this quest doesn't complete immediately, try closing and reopening the quest book or re-logging." For pack authors, prefer item-crafting tasks over item-collection tasks where possible, as crafting tasks trigger more reliably than inventory-presence checks.
- **Cross-mod tag collision:** When two mods define items under the same Forge tag (e.g., `#forge:ingots/copper`) but with different NBT or capabilities, tag-based task matching may over-accept. Verify that all items under the tag are functionally equivalent for the quest's purpose.
**Source:** GitHub FTBTeam/FTB-Modpack-Issues #3248 ("quests are not completing even with the item done", "harvesting flax incorrectly completed a cobblestone quest", version-update-induced detection failure 1.0.6 → 1.0.7).
**Cross-reference:** R33 (reward table reference integrity), R11 (reward-target accuracy), R42 (stage-internal item reachability).

---

#### R127 — Cross-Dimension Item Usability Warning

**Name:** Cross-Dimension Item Usability Warning
**Severity:** WARNING
**Applicable when:** A quest rewards an item that has dimension-specific behavior, or when a quest in one chapter requires an item that can only be obtained or used in a different dimension than the chapter's implied location.

MC百科 post/3137 documents a concrete cross-dimension item failure: "非交错次元维度的食物无法在交错次元食用" (food from non-Twilight dimensions cannot be eaten in the Twilight Forest dimension). The pack had to explicitly disable the equipment-nerf function ("整合包关闭了在交错次元削弱非交错次元装备的功能") to prevent players' gear from becoming useless when entering the Twilight Forest. This reveals a structural vulnerability in dimension-heavy packs: quest rewards designed in the context of one dimension may become useless, nerfed, or behave unexpectedly in another dimension where the player needs them for subsequent quests.

The problem manifests in three ways. Manifestation 1 (dead reward): the quest rewards food that can't be eaten, equipment that gets nerfed, or tools that don't function in the dimension where the next quest takes place — the reward is technically received but practically useless. Manifestation 2 (false dependency): a quest in Chapter A (Overworld-focused) requires an item from Chapter B (Nether-focused), but the quest dependency graph doesn't enforce that Chapter B is completed first — the player is stuck because they can't obtain the required item without entering a dimension they haven't unlocked. Manifestation 3 (config fragility): the dimension-specific behavior is controlled by a config option that the pack author may have forgotten to adjust (as in post/3137's "关闭了削弱功能"), meaning the problem exists silently until a player encounters it.

**Prerequisites:** Checking dimension-specific item behavior (food that can't be eaten, equipment that gets nerfed, tools that require specific dimension energy) requires mod-specific knowledge that is NOT available from quest configs, KubeJS scripts, or Forge tags alone — it is runtime behavior defined in mod source code. The agent cannot build a complete dimension-item compatibility matrix without playtesting or a curated item-dimension database. Without this data, the agent should limit the check to structural inference: identify the chapter's implied dimension context from task item IDs and dimension-type tasks, and flag cases where a reward item's mod origin is from a different dimension's content set than the chapter's implied dimension. Flag this limitation in the Step 5 report.
**Implementation check:** For each quest with an item reward or item task, (1) check if the item has dimension-specific behavior (food that can't be eaten in certain dimensions, equipment that gets nerfed, tools that require specific dimension's energy), (2) check the chapter's implied dimension context (if the chapter's quests predominantly reference Overworld/Nether/End/Twilight/custom dimensions), and (3) verify that the reward item is functional in the dimension where the player will most likely need it next. Flag as `WARNING — quest reward item [X] has known dimension-specific restrictions that may render it unusable in the context of the next dependent quest's dimension`. For item tasks, verify the required item is obtainable in the chapter's dimension context without requiring travel to a dimension that the dependency graph hasn't yet unlocked.
**Source:** MC百科 post/3137 (整合包常见问题与解决方案, "非交错次元维度的食物无法在交错次元食用", "整合包关闭了在交错次元削弱非交错次元装备的功能"); MC百科 bbs/thread-21004 (dimension-based progression design, "修改材料的生成世界，以及怪物的生成世界").
**Cross-reference:** R1 (dimension-reachability), R16 (dimension-explore-then-craft), R106 (dimensional naturalism), R108 (dimensional mob scaling).

---

#### R128 — Backward-Facing Shortcut Principle

**Name:** Backward-Facing Shortcut Principle
**Severity:** INFO
**Applicable when:** All packs with 3+ chapters or any pack that introduces new capabilities at stage transitions.

The cesspit.net analysis of modded Minecraft progression identifies a critical but under-documented design principle: good progression benefits should "open fresh technological avenues while supplying backward-facing shortcuts that let you 'optimize' what you've done." This means that when a player unlocks a new capability (e.g., a higher-tier machine, a teleportation method, an automation system), the new capability should not only enable forward progression (new items, new dimensions, new quests) but also provide a tangible improvement to something the player already built or did in the previous stage. An ore-doubling machine in Stage 3 should let the player re-process their Stage 2 ore stockpile more efficiently; a teleportation network in Stage 4 should let the player revisit Stage 2 bases without tedious travel; a logistics system in Stage 5 should let the player consolidate their Stage 3 scattered storage.

This principle connects to the three hard problems in a subtle but important way. For item cross-tier (三硬伤 #1), backward-facing shortcuts reduce the player's motivation to seek items from later stages: if the current stage already provides meaningful optimization of existing work, the player feels progression is smooth rather than abrupt. For sequence inversion (三硬伤 #2), backward-facing shortcuts create a natural incentive to complete earlier stages fully before advancing: the player knows that advancing will give them tools to optimize their earlier work, which motivates them to build that work properly in the first place. For reward disconnection (三硬伤 #3), backward-facing shortcuts make rewards feel immediately useful: the reward doesn't just sit in the chest waiting for the next stage — it improves what the player is already doing.

The MC百科 bbs/thread-21004 discussion validates this from the author's perspective: "每一个模组都要有重复利用，游玩一次后直接舍弃是绝对不可取的" (every mod must be reused; it's absolutely unacceptable to use a mod once and then discard it). This is the macro-level version of the same principle: each capability introduced should remain relevant throughout the pack, not become obsolete the moment a higher-tier alternative appears. The "equipment spindle distribution" (装备数量分布应呈"纺锤形") proposed in the same article is a specific application: the middle tiers have the most equipment variety because they benefit from both backward-facing optimization (earlier-tier materials are now cheaper to process) and forward-facing investment (later-tier materials are being accumulated).

**Prerequisites:** Checks (1) and (2) require qualitative design judgment — determining whether a reward "provides a measurable improvement to an activity from the previous stage" or whether machines "remain relevant" demands semantic understanding of gameplay mechanics that goes beyond config parsing. The agent should approximate this by checking structural proxies: does the reward item's mod match a mod that appears in the previous chapter's task list? Does the reward unlock a recipe that uses materials from the previous stage? Check (3) — whether quest descriptions mention backward-facing benefits — is directly executable via text analysis of quest_desc fields. If only check (3) is executable, report the result as a description-quality observation rather than a design validation.
**Implementation check:** At each major stage transition (chapter boundary, tier upgrade, dimension unlock), verify that: (1) the new stage's first 3–5 quests include at least one reward or unlock that provides a measurable improvement to an activity from the previous stage (ore processing speedup, travel time reduction, storage consolidation), (2) the previous stage's key machines/structures remain relevant after the transition (not rendered completely obsolete by the new stage's alternatives), and (3) the quest description of stage-transition quests explicitly mentions the backward-facing benefit to orient the player. If no backward-facing benefit is present at a stage transition, flag as `INFO — stage transition at [chapter X] lacks backward-facing shortcut; player may feel previous investment was wasted`.
**Source:** cesspit.net node/2832 ("backward-facing shortcuts that let you optimize what you've done", "Having fun in a game is all about solving problems"); MC百科 bbs/thread-21004 ("每一个模组都要有重复利用，游玩一次后直接舍弃是绝对不可取的", "装备数量分布应呈纺锤形").
**Cross-reference:** R10 (reward-to-dependent bridge), R12 (reward value progression), R85 (mid/late-game reward guidance), R114 (stage-to-quest bridging).

---

#### R129 — Quest-as-Stage-Trigger Integration

**Name:** Quest-as-Stage-Trigger Integration (任务完成即激活新阶段)
**Severity:** WARNING (orphan stages) / INFO (visibility without game-stage condition)
**Applicable when:** Expert or semi-gated packs using Game Stages, Item Stages, or equivalent progression-locking mods alongside FTB Quests.

The CSDN analysis of FTB Quest + GameStages integration formalizes a design pattern that expert packs have independently converged on: quest completion should serve as the canonical progression trigger that activates new game stages, rather than relying on separate trigger mechanisms (crafting a specific item, entering a dimension, killing a boss) that may or may not align with the quest book's visual dependency graph. The article describes this as a closed loop: "任务完成即激活新阶段" (quest completion activates the new stage), ensuring that every player action yields meaningful world feedback and opens up new gameplay layers. The system creates a "动态响应、自我演化的游戏世界模型" (dynamic response, self-evolving game world model) where the quest book is not merely a guide but the authoritative progression controller.

This pattern addresses a subtle but common failure: the quest book shows the player what to do, but the actual progression gate is controlled by a different mechanism (a KubeJS script that fires when the player crafts item X, a Game Stages tag that's added when the player enters dimension Y). When these two systems diverge — the quest says "craft item X to proceed" but the script actually triggers on "pick up item X from the ground" — the player can complete the quest without triggering the gate, or trigger the gate without completing the quest. The quest book becomes a liar: it claims the player has progressed when they haven't, or denies progress when they have.

The integration pattern has three implementation layers. Layer 1 (quest-command bridge): the quest's completion reward executes a command (typically `/gamestage add @p stage_name` or equivalent) that directly modifies the player's game stages. This ensures that the quest completion and the stage activation are atomic — they cannot diverge. Layer 2 (stage-conditional visibility): the quest itself uses `hide_until_deps_visible` or a game-stage condition to remain invisible until the previous stage is active, creating a clean visual progression where the quest book only shows what the player can currently engage with. Layer 3 (NPC-trade and ore-distribution sync): Game Stages tags synchronize NPC trades and ore world-generation with the player's progression, ensuring that the world itself evolves in lockstep with the quest book rather than having ores spawn that the player can't use yet or NPC trades that offer items from stages the player hasn't reached.

**Prerequisites:** Full execution of check (1) requires access to Game Stages / Item Stages configuration files (the list of all defined stages and their activation triggers) — without this, the agent can only verify the quest-side presence of `/gamestage` command rewards but cannot detect orphan stages activated by non-quest triggers. Check (2) is fully executable from quest config (presence of `hide_until_deps_visible` or game-stage conditions). Check (3) requires NPC trade configs and ore generation configs, which are external to the quest system. If Game Stages config is unavailable, the agent should limit the check to quest-side scanning (command rewards + visibility conditions) and note the gap.
**Implementation check:** For expert/semi-gated packs using Game Stages + FTB Quests: (1) verify that every game-stage transition has a corresponding quest whose completion reward executes the stage-activation command (no "orphan stages" activated by non-quest triggers), (2) verify that every quest whose task requires a game-stage-gated item has the appropriate `hide_until_deps_visible` or game-stage condition set, and (3) verify that NPC trades and ore generation configs reference the same game-stage tags as the quest book. Flag orphan stages as `WARNING — game stage [X] is activated by a non-quest trigger; quest book and progression gate may diverge`. Flag quests that don't use game-stage visibility conditions as `INFO — quest [X] is visible before its required game stage is active; player may see content they cannot yet engage with`.
**Source:** CSDN wenku/doc/6amfp2j2im (FTB Quest与GameStages结合, "任务完成即激活新阶段", "动态响应、自我演化的游戏世界模型", "渐进式赋能"); MC百科 class/1360 (游戏阶段/Game Stages mod documentation).
**Cross-reference:** R113 (game-stages multi-dimensional sync), R114 (quest-to-stage bridge), R115 (recipe-stages container locking), R117 (villager trade gating).

---

#### R130 — Item-as-Currency Reward Consistency

**Name:** Item-as-Currency Reward Consistency
**Severity:** WARNING
**Applicable when:** Quests reward currency items (e.g., GT silver_credit, FTB Money, custom coin items) and the pack has shop quests or a quest-shop economy.

The GregTech-Leisure-Server (Cycle 19 Phase 1) demonstrates a simpler alternative to ftbmoney: every quest rewards a `silver_credit` item that players spend in quest shops, creating an item-based economy without requiring the ftbmoney mod's economy system. The klpbbs.com thread-130537 confirms this as a recognized design bifurcation in the Chinese modding community: item-based vs. ftbmoney-based economies are a deliberate choice. But the item-as-currency approach introduces a unique set of consistency risks that don't apply to ftbmoney's abstracted balance system.

Risk 1 (currency-supply mismatch): if the total currency rewarded across all quests is less than the total cost of all shop quests, the player cannot purchase everything and must obtain currency through unintended means (mob farms, selling items to NPC traders). If the total currency is *more* than needed, the excess currency has no sink and the economy feels meaningless. Risk 2 (currency-item dual identity): the currency item (e.g., silver_credit) may also appear as a crafting material in non-quest recipes, creating a tension between spending it in shops and using it in crafting. If the player crafts with their currency, they can't afford the shop quests; if they save for shops, the crafting recipes that require the currency item are blocked. Risk 3 (currency obtainability outside quests): if the currency item can be obtained through mob drops, mining, or villager trading, the quest-shop economy can be bypassed entirely — the player farms currency without engaging with the quest progression.

**Prerequisites:** Check (1) — currency supply/demand ratio — is fully executable from quest config alone: the agent can sum all currency items across reward slots and sum all shop quest costs. Check (2) — currency item as crafting ingredient — requires access to mod/KubeJS recipe data to determine whether the currency item appears in any non-quest recipe. Check (3) — currency obtainability outside quests — requires mob drop tables, world generation configs, and villager trade configs, all external to the quest system. If recipe and drop data are unavailable, the agent should execute check (1) and note checks (2) and (3) as requiring manual author verification.
**Implementation check:** For packs using item-as-currency: (1) calculate total currency supply (sum of all currency items rewarded across all quests) and total currency demand (sum of all shop quest costs), flagging as `WARNING — currency supply [X] does not match demand [Y]; ratio [X/Y] indicates [oversupply/undersupply]` if the ratio deviates more than 20% from 1.0, (2) check if the currency item appears as a crafting ingredient in any non-quest recipe, flagging as `WARNING — currency item [X] is also a crafting ingredient; dual-identity creates spend-vs-craft tension`, and (3) check if the currency item has any non-quest acquisition path (mob drops, world generation, villager trades, crafting recipe), flagging as `WARNING — currency item [X] is obtainable outside quests through [method]; quest-shop economy can be bypassed`. For multiplayer packs, multiply supply calculations by expected player count and flag team-economy exploits.

**Edge case notes:**
- **Non-quest currency sinks:** The supply-demand calculation only counts quest-shop costs as demand. If the pack has non-quest currency sinks (Custom NPC shops, vending machines, mod-added trading systems, player-to-player trading on servers), these must be estimated separately and added to total demand. Failure to account for external sinks causes apparent oversupply in the quest economy while the actual economy is balanced. Flag as `INFO — pack has non-quest currency sinks; quest-economy ratio may not reflect total economy balance`.
- **Multi-currency tiers:** If the pack uses multiple currency items (e.g., silver_credit for early game, gold_credit for late game), run the supply-demand calculation independently for each currency tier. Also check cross-tier exchange: if players can convert silver to gold (or vice versa) through any mechanism, verify the exchange rate doesn't create arbitrage against quest-shop prices.
- **Currency in storage/containers:** Item-as-currency can be hoarded in chests, AE2/RS storage systems, or ender chests. Unlike ftbmoney's abstracted balance, physical currency items can be lost (lava, void, despawn), duplicated (copy-paste exploits on some server platforms), or accidentally spent on non-currency crafting. Consider recommending that pack authors add a quest-description note reminding players to keep currency in safe storage.
**Source:** GregTech-Leisure-Server (Cycle 19 Phase 1, silver_credit on every quest); klpbbs.com thread-130537 (FTB Money and Oxygen Core as common economy mods for expert packs, confirming item-based vs. ftbmoney-based bifurcation).
**Cross-reference:** R12 (reward value progression), R34 (reward type distribution), R50 (zero-reward safety), R46 (questbook role declaration), AP42 (trading hall bypass — currency farming is the same vector).

---

#### How the three hard problems map to Cycle 18 Phase 3 trading-bypass-defense and author-philosophy rules

The Cycle 18 Phase 3 research reveals that the AP42 (Villager Trading Hall Bypass) vulnerability exposes a fundamental gap in the existing defense matrix: all prior rules focused on preventing items from being *crafted* or *used* at the wrong stage, but none addressed the case where items are *acquired* through legitimate game mechanics that bypass the intended crafting chain. The new rules close this gap at three levels: acquisition-method verification (R118), villager-trade-specific gating (R117), and compensatory defense for open-gating packs (R123). Additionally, the new rules expand the defense matrix with narrative-driven progression (R120), tech-level continuous scaling (R119), and equipment tier transition smoothness (R121) — all of which reduce the player's motivation to seek alternative acquisition paths in the first place.

**Item cross-tier (三硬伤 #1) — R117 + R118 + R119 + R121.** R117 (Villager Trade Progression Gating) directly addresses the AP42 bypass vector: if villager trades are gated behind progression stages, the trading hall cannot provide items the player hasn't earned. R118 (Acquisition-Method Verification) extends this to all alternative acquisition paths by requiring engagement proof: even if the player obtains the item through an unintended path, the quest's supplementary tasks verify they also understand the intended crafting process. R119 (Tech-Level Continuous Scale) prevents cross-tier from a granularity perspective: with a continuous tech level, the player's progression is smooth rather than abrupt, reducing the incentive to seek bypasses. R121 (Equipment Tier Transition Smoothness) prevents cross-tier from the combat balance perspective: if each tier's equipment is well-calibrated against the mob difficulty, the player doesn't need to seek overpowered items from later tiers.

**Sequence inversion (三硬伤 #2) — R120 + R122 + R124.** R120 (Narrative Research Progression) prevents sequence inversion through narrative coherence: if the research tasks form a story, the player is motivated to complete them in order because breaking the sequence breaks the narrative. Nova Engineering validates this: the "剧情化研究系统，贯穿发展全线" keeps the player on the intended path because the story pulls them forward. R122 (Kitchen-Sink Flow Clarity) prevents unintentional sequence inversion: if the player knows which chapter to pursue (because the pack provides clear guidance), they won't accidentally pursue chapters in the wrong order. R124 (Author Playtesting) catches sequence inversions before release: the author, following the quest line from start to finish, discovers where tutorials teach concepts in the wrong order or where prerequisites are missing.

**Reward disconnection (三硬伤 #3) — R120 + R122 + R123.** R120 makes the research system itself the reward — completing research advances the story and unlocks new capabilities, which is intrinsically rewarding regardless of item rewards. R122 ensures the player can always identify their next progression step, preventing the feeling that rewards are disconnected from progress. R123 ensures that even in open-gating packs, the compensatory defense includes engagement verification tasks that make rewards feel earned. The MC百科 post/6155 article's observation that kitchen-sink packs fail because of "流程和引导不够明晰" validates that unclear flow is itself a form of reward disconnection: when the player doesn't know what to pursue next, every reward feels arbitrary.

---

#### New tensions from Cycle 18 Phase 3

**Tension 10: Item streamlining (Vazkii) vs. crafting variety (R104).** Vazkii's philosophy advocates eliminating redundant items so mod progression forms "一整条线" (a single continuous line), reducing repetitive gameplay. R104 (Crafting Method Variety) advocates diverse crafting methods within each stage to prevent monotony. The resolution is scope-dependent: at the macro level (which mods to include, which technologies to gate), follow Vazkii's streamlining to ensure a clear progression spine; at the micro level (how to craft each item within a stage), follow R104's variety to ensure diverse engagement. Nova Engineering demonstrates this: the tech level provides a single clear progression spine (Vazkii's "一整条线"), but within each tech level, the 100+ original multiblock machines provide diverse crafting methods (R104's variety).

**Tension 11: Narrative-driven research (R120) vs. traditional quest dependencies (R82).** R120 replaces traditional quest-dependency progression with a narrative research system that gates advancement through story-based tasks. R82 advocates backward design from the quest book's visual dependency graph. The resolution is implementation-dependent: for expert packs with 100+ hours of content where the research system can sustain a coherent narrative arc, R120 provides a more engaging progression experience than traditional quest dependencies. For smaller packs or packs without a custom research framework, R82's backward design from the quest book remains the more practical approach. Nova Engineering's success with narrative research is possible because the pack has 200+ mods, 100+ original machines, and a custom HyperNet framework — most packs cannot sustain this level of narrative infrastructure.

**Tension 12: Open-gating freedom (R123, EL2 philosophy) vs. progression integrity (AP42, R117).** R123 formalizes the compensatory defense for packs that deliberately choose open-gating (like Engineer's Life 2's "if you have resources, you can craft anytime"). AP42 and R117 document the progression integrity failures that open-gating enables (villager trading bypass). The resolution is selective restriction: maintain the open-gating philosophy for 90%+ of the pack's content (preserving player freedom), but identify the 5–10 items whose early acquisition would most damage the progression experience and restrict those specific items' alternative acquisition paths. This preserves the spirit of open-gating (the player feels free) while protecting the critical progression chokepoints (the player can't accidentally bypass the most important gates). The alternative — full open-gating with no restrictions — requires accepting that some players will bypass the intended progression and having faith that those players are making an informed choice.

---

#### How the three hard problems map to Cycle 19 Phase 3 quest-reward-integrity and progression-trigger rules

The Cycle 19 Phase 3 research identifies six new rules (R125–R130) that address previously unguarded failure modes in the reward-integrity and progression-trigger domains. Prior to this cycle, the defense matrix covered *what* items are gated (R1–R4, R42), *how* they are gated (R101, R113–R117), and *whether* the gating can be bypassed (R118, R123). But it did not address three critical questions: (1) do quest rewards themselves undermine the gating they're supposed to reinforce? (2) does the quest detection system actually work correctly? (3) does the quest book's progression trigger align with the underlying game-stage system?

**Item cross-tier (三硬伤 #1) — R125 + R127 + R130.** R125 (Quest Reward Progression-Trivialization) is the most direct defense against cross-tier via the reward vector: if the quest book hands the player items they shouldn't have yet, the quest book itself is the cross-tier source — not a villager trading hall, not a mob farm, but the reward mechanism the player trusts. The ATM-10 case (Dragon Egg, Ultimate Universal Cable, ore sight charm) proves this is not theoretical. R127 (Cross-Dimension Item Usability) prevents a subtler cross-tier: the player receives an item that works in Dimension A but is nerfed or useless in Dimension B where the next quest takes place, forcing the player to seek an alternative item from a different progression path. R130 (Item-as-Currency Consistency) prevents economy-based cross-tier: if the currency item is obtainable outside quests, the player can purchase shop items without completing the progression chain, bypassing the intended gating.

**Sequence inversion (三硬伤 #2) — R126 + R129.** R126 (Quest Task Detection Alignment) prevents a detection-level sequence inversion where the wrong quest completes on the wrong action: FTB Skies issue #3248 shows "harvesting flax incorrectly completed a cobblestone quest" — this is sequence inversion caused not by bad dependency design but by broken detection logic. The quest book claims cobblestone was crafted when the player harvested flax, inverting the teaching sequence. R129 (Quest-as-Stage-Trigger Integration) prevents a trigger-level sequence inversion where the quest book and the game-stage system disagree on the player's progression state: the quest says "you've progressed" but the game stage hasn't activated, or vice versa. This divergence means the player may attempt a stage-gated action that the quest book implied was available, creating confusion about the correct sequence.

**Reward disconnection (三硬伤 #3) — R125 + R128 + R130.** R125 prevents reward disconnection from the trivialization direction: when a reward provides an item the player can't yet use (because it requires infrastructure from a later stage) or an item that makes the next stage trivially easy, the reward feels disconnected from the player's actual progression state — it's either premature or redundant. R128 (Backward-Facing Shortcut Principle) prevents disconnection from the relevance direction: if every reward only enables forward progression but never improves existing work, the player accumulates tools they don't need yet while their current challenges remain unsolved. R130 prevents disconnection from the economy direction: if currency rewards can't be spent meaningfully (because shop quests are too expensive, or the currency has no sink), the reward feels arbitrary rather than earned.

---

#### New tensions from Cycle 19 Phase 3

**Tension 13: Reward generosity (kitchen-sink philosophy) vs. reward restraint (expert philosophy).** The ATM-10 debate (GitHub discussions #3539) exposes a fundamental philosophical divide: the kitchen-sink camp argues that "almost everything should be revisited and a general balance pass should be made" to prevent quest rewards from trivializing progression, while the expert camp responds that in "a kitchen sink pack" the early utility items don't "beat the game." R125 formalizes a middle ground: distinguish between *utility* rewards (tools that enhance current-stage activities) and *capability* rewards (items that skip upcoming stages). Kitchen-sink packs can freely give utility rewards but must restrain capability rewards. Expert packs should give neither — progression itself is the reward (R89). The resolution is pack-type-dependent: for kitchen-sink packs, allow generous rewards as long as no individual reward nullifies a pack-scarcity resource; for expert packs, enforce R50's zero-reward safety with maximum strictness.

**Tension 14: Quest-as-canonical-trigger (R129) vs. organic exploration (R123, open-gating).** R129 advocates making quest completion the authoritative progression controller: "任务完成即激活新阶段" (quest completion activates the new stage). R123 and the open-gating philosophy advocate letting players progress through organic exploration and resource acquisition without requiring quest completion. The resolution is audience-dependent: for expert packs where the crafting chain is 100+ hours long and every stage transition is a deliberate milestone, R129's quest-command bridge ensures tight synchronization between the quest book and the game world. For kitchen-sink or open-gating packs where the player may discover technologies through experimentation, the quest book should serve as a *guide* (documenting what the player has done) rather than a *gate* (controlling what the player can do). The quest book's role (guide vs. gate) should be explicitly declared at the pack start (aligning with R46, questbook role declaration).

**Tension 15: Item-as-currency simplicity (R130) vs. ftbmoney abstraction.** R130 documents the risks of item-as-currency (supply-demand mismatch, dual identity, external obtainability). The ftbmoney mod avoids all three risks by using an abstracted balance that can't be physically farmed. But item-as-currency has one advantage ftbmoney lacks: tangibility. The player holds the silver_credit in their inventory, sees it accumulate, and physically hands it to the shop quest. This tangibility creates a stronger psychological connection to the economy than an abstract number in a GUI. The resolution is audience-dependent: for packs where the economy is a minor side system, item-as-currency provides sufficient functionality with minimal mod overhead. For packs where the economy is a core progression mechanic (shop quests gating key items), ftbmoney's abstraction prevents the exploits that R130 documents.

> **Edge case notes for Cycle 19 tensions:**
> - **Hybrid pack types (T13/T14):** Many real-world packs are neither purely kitchen-sink nor purely expert — they may be kitchen-sink in early game and semi-expert in late game, or expert in tech branches but kitchen-sink in magic branches. For hybrid packs: apply T13's utility/capability distinction on a per-chapter basis (each chapter declares its own reward philosophy), and apply T14's guide/gate decision per progression system (tech stages use quest-as-gate, exploration content uses quest-as-guide). The pack should declare its hybrid structure in the first-chapter tutorial so players know which chapters enforce strict progression and which allow free exploration.
> - **"Artificial grind" as unmapped failure mode (T13 cross-ref to Lesson 156):** The cesspit.net analysis (Lesson 156) identifies four progression problems: blindness, aimlessness, overpowered shortcuts, and artificial grind. The first three map cleanly to the three hard problems. "Artificial grind" — where the player has a clear goal and the path is known but the execution is tedious (excessive grinding, repetitive tasks without meaningful engagement) — is a distinct failure mode not directly addressed by any existing rule. It relates tangentially to R15 (complexity escalation) and R99 (pacing rhythm), but neither rule explicitly guards against quests that are mechanically tedious rather than structurally broken. This is a candidate for a future rule (e.g., R131 "Quest Mechanical Engagement Minimum") if sufficient evidence accumulates.

---

## Appendix — Topology Rule Cross-Reference

| Rule | Topology types affected | References core rule |
|------|------------------------|---------------------|
| R55 | All seven (incl. highway_branch) | R9 (depth reasonableness), R41 (early-game flexible — see conflict resolution) |
| R56 | linear_chain, tree_branching, diamond_convergence, highway_branch | R14 (teach-then-do), R15 (complexity escalation) |
| R57 | hub_fan, tree_branching | R30 (visual hierarchy) |
| R58 | All seven | — (standalone layout invariant) |
| R59 | All seven | — (standalone viewport constraint) |
| R60 | All seven | R35 (shape semantics consistency) |
| R61 | diamond_convergence, hub_fan | R13 (capstone reward magnitude) |
| R62 | parallel_columns | — (standalone uniformity check) |
| R63 | grid_catalog | R18 (description coverage) |
| R64 | All (when decorative images present) | — (standalone alignment check) |
| R65 | All (when dimension/biome/mob tasks present) | R1–R4 (item reachability), R16 (dimension-explore-then-craft) |
| R66 | All (when multiple branches exist) | R4 (stage boundary), R10 (reward-to-dependent bridge) |
| R67 | All (when stage gates present) | R4 (stage boundary), R42 (stage-internal reachability) |
| R68 | All | R14 (teach-then-do), R18 (description coverage) |
| R69 | All | R23 (description-item consistency), R24 (suggestion-reachability) |
| R70 | All (when rewards and dependents exist) | R10 (reward-to-dependent bridge), R45 (reward guidance bridging) |
| R71 | All (when stage has >5 recipe tasks) | R15 (complexity escalation) |
| R72 | All (late-game quests) | R12 (reward value progression), R13 (capstone reward magnitude) |
| R73 | Skyblock packs (Ex Nihilo/Ex Deorum) | R1 (dimension-reachability), R4 (stage boundary), R42 (stage-internal reachability) |
| R74 | Adventure/RPG/hardcore packs (kill tasks) | R2 (tool-tier reachability), R17 (tool-reward-before-use) |
| R75 | Farming/lifestyle packs (seasonal crops) | R14 (teach-then-do), R4 (stage boundary) |
| R76 | Skyblock packs (multi-path resources) | R66 (cross-branch gate independence), R10 (reward-to-dependent bridge) |
| R77 | Adventure/RPG packs (boss quests) | R18 (description coverage), AP5 (empty quest description) |
| R78 | Farming/lifestyle/peaceful packs | R1 (dimension-reachability), R24 (suggestion-reachability) |
| R79 | Skyblock packs (multiblock structures) | R14 (teach-then-do), R17 (tool-reward-before-use) |
| R80 | Adventure/RPG packs (main + side branches) | R66 (cross-branch gate independence), R22 (cross-chapter dependency) |
| R81 | All packs with 2+ processing mods | R4 (stage boundary), R76 (multi-path resource redundancy) |
| R82 | All packs (book-level arc design) | R10 (reward-to-dependent bridge), R45 (reward guidance bridging) |
| R83 | All packs (stage gates present) | R4 (stage boundary), R67 (stage gate distribution) |
| R84 | All packs (pacing evaluation) | R15 (complexity escalation), R19 (bottleneck spacing) |
| R85 | All packs (mid/late-game rewards) | R10 (reward-to-dependent bridge), R12 (reward value progression), R45 (reward guidance bridging) |
| R86 | Expert/semi-gated packs | R18 (description coverage), R69 (description trust), R26 (quest-mod version consistency) |
| R87 | All packs (dimension/biome transitions) | R16 (dimension-explore-then-craft), R17 (tool-reward-before-use) |
| R88 | All packs (multi-reward-type chapters) | R34 (reward type distribution), R50 (zero-reward safety), PP13 (reward-type contract) |
| R89 | Narrative/GT/expert packs (zero-reward quests) | R50 (zero-reward safety, condition 2 questbook_role exception), PP14 (progression-as-reward) |
| R90 | All packs (convergence quests with 10+ deps) | R1–R4 (item reachability), R42 (stage-internal reachability), AP37 (convergence claustrophobia) |
| R91 | All packs (chapters with >15 quests) | R35 (shape semantics consistency), R60 (shape consistency within chapter) |
| R92 | All packs (tier systems present) | R12 (reward value progression), R15 (complexity escalation) |
| R93 | Adventure/RPG packs (dimension transitions) | R17 (tool-reward-before-use), R87 (anti-nerf transitions) |
| R94 | All packs (nested crafting chains) | R3 (recipe-chain depth), R15 (complexity escalation) |
| R95 | All packs (multi-mod progression) | R90 (convergence backtracking safety), R81 (multi-processing-mod management) |
| R96 | All packs (early-game pacing) | R19 (bottleneck spacing), R41 (early-game flexible progression mode) |
| R97 | Adventure/RPG packs (progression gating) | R67 (stage gate distribution), R83 (weak lock design), R86 (description as navigation) |
| R98 | All packs (>30 mods with quest book) | R82 (backward design), R95 (anti-orphan) |
| R99 | All packs (chapters >20 quests or >5 chapters) | R19 (bottleneck spacing), R15 (complexity escalation), R84 (mid-game density) |
| R100 | All packs (optional challenge content) | R46 (questbook role declaration), R12 (reward value progression) |
| R101 | Expert/semi-gated packs (progression gating) | R83 (weak lock permeability), R4 (stage boundary), R67 (stage gate distribution) |
| R102 | Long-term packs (>10 chapters or >100h) | R82 (backward design), R84 (mid-game density), R99 (pacing rhythm) |
| R103 | All packs (tutorial/onboarding content) | R14 (teach-then-do), R18 (description coverage), R102 (era-based architecture) |
| R104 | All packs (stages with 5+ crafting quests) | R71 (recipe-type diversity), R94 (crafting depth fatigue), R99 (pacing rhythm) |
| R105 | All packs (>3 chapters) | R32 (chapter QA coverage), R41 (early-game flexible), R102 (era-based architecture) |
| R106 | Packs with 2+ dimension mods (dimension-gated content) | R16 (dimension-explore-then-craft), R1 (dimension-reachability), R102 (era-based architecture) |
| R107 | Packs with tiered equipment (3+ tiers) | R12 (reward value progression), R105 (60% accessibility), R110 (mid-game density) |
| R108 | Packs with 2+ dimension mods (hostile mobs) | R2 (tool-tier reachability), R4 (stage boundary), R106 (dimensional naturalism) |
| R109 | Expert/semi-gated packs (dimension-gated resources) | R1 (dimension-reachability), R4 (stage boundary), R42 (stage-internal reachability), R101 (multi-layer enforcement) |
| R110 | All packs (3+ chapters or 50+ quests) | R15 (complexity escalation), R19 (bottleneck spacing), R84 (mid-game density), R94 (crafting depth fatigue) |
| R111 | Packs with nested crafting or 100h+ playtime | R94 (crafting depth fatigue), R99 (pacing rhythm), R15 (complexity escalation), R71 (recipe-type diversity) |
| R112 | Packs with vanilla+ mods alongside tech/magic mods | R14 (teach-then-do), R15 (complexity escalation), R103 (tutorial anchor) |
| R113 | Expert/semi-gated packs (Game Stages or equivalent) | R101 (multi-layer enforcement), R106 (dimensional naturalism), R38 (tier transition milestone) |
| R114 | Expert/semi-gated packs (Game Stages or equivalent) | R101 (multi-layer enforcement), R10 (reward-to-dependent bridge), R45 (reward guidance bridging) |
| R115 | Expert packs (Recipe Stages + automation mods) | R101 (multi-layer enforcement), R114 (quest-to-stage bridge), R4 (stage boundary), R42 (stage-internal reachability) |
| R116 | Packs using vanilla advancements as progression gates | MP70 (tome-tier progression map), R113 (multi-dimensional sync), R106 (dimensional naturalism) |
| R117 | All packs (FTB Quests + vanilla villager trading) | AP42 (trading hall bypass), R101 (multi-layer enforcement), R115 (container-level locking), R83 (weak lock permeability) |
| R118 | Packs where quest pedagogical intent requires mod engagement | R14 (teach-then-do), R103 (tutorial anchor), AP42 (trading bypass), R117 (villager trade gating) |
| R119 | Expert packs (3+ tiers, 50+ quests, tiered tech system) | R101 (multi-layer enforcement), R102 (era-based architecture), R92 (tier system calibration), R113 (multi-dimensional sync) |
| R120 | Expert packs (100+ hours, narrative research system) | R82 (backward design), R103 (tutorial anchor), R106 (dimensional naturalism), R118 (acquisition verification) |
| R121 | Packs with dimension-gated tiered equipment (3+ tiers) | R108 (gear-to-mob scaling), R106 (dimensional naturalism), R93 (anti-nerf transitions), R107 (olive-shaped distribution) |
| R122 | Kitchen-sink/large packs (50+ mods, 3+ chapters) | R105 (60% accessibility), R41 (early-game flexible), AP41 (flat presentation), R103 (tutorial anchor) |
| R123 | Non-expert packs with open-gating philosophy | AP42 (trading hall bypass), R117 (villager trade gating), R83 (weak lock permeability), R122 (flow clarity) |
| R124 | All packs (pre-release quality assurance) | R105 (60% accessibility), R32 (chapter QA coverage), AP45 (unplaytested release) |
| R125 | All packs (quest rewards with item drops) | R12 (reward value progression), R10 (reward-to-dependent bridge), R4 (stage boundary), R118 (acquisition-method verification) |
| R126 | All packs (item-crafting/collection tasks) | R33 (reward table reference integrity), R11 (reward-target accuracy), R42 (stage-internal item reachability) |
| R127 | Packs with 2+ dimension mods (cross-dimension rewards) | R1 (dimension-reachability), R16 (dimension-explore-then-craft), R106 (dimensional naturalism), R108 (dimensional mob scaling) |
| R128 | All packs with 3+ chapters (stage transitions) | R10 (reward-to-dependent bridge), R12 (reward value progression), R85 (mid/late-game reward guidance), R114 (stage-to-quest bridging) |
| R129 | Expert/semi-gated packs (Game Stages + FTB Quests) | R113 (multi-dimensional sync), R114 (quest-to-stage bridge), R115 (container-level locking), R117 (villager trade gating) |
| R130 | Packs using item-as-currency economy | R12 (reward value progression), R34 (reward type distribution), R50 (zero-reward safety), R46 (questbook role declaration), AP42 (trading hall bypass) |
