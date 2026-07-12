# FTB Quests — Progression Rules (Active)

> **Status:** Active | **Cycle:** 11 | **Updated:** 2026-07-12
> **Supersedes:** `progression-rules.archive.md` (R1–R54 remain authoritative in their modular homes; this file is the topology-aware overlay)
> **Purpose:** Provide executable validation rules for AI-generated quest configurations, with special emphasis on the intersection between dependency-graph topology and visual layout.

This file contains two sections. The first distills the core rules from R1–R54 into a quick-reference map — it does not redefine those rules, which live in the modular files (`mod-item-reachability.md`, `mod-dependency-graph.md`, `mod-reward-design.md`, `mod-teaching-pacing.md`, `mod-description-trust.md`, `mod-system-safety.md`). The second introduces new topology-aware rules (R55–R64) that close the gap between *what the dependency graph means* and *how the layout looks*.

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

## Section C — Rule Execution Priority

### Step 4 — Generation-time checks

Topology rules R55–R64 operate primarily at Step 5 (validation), but two can run during generation:

| Priority | Rule | Check type | Failure |
|----------|------|-----------|---------|
| P1 | R55 Topology-Progression Mode Alignment | topology + mode lookup | WARNING |
| P2 | R57 Hub Node Size Dominance | size comparison | WARNING |

> **Note (Cycle 11 Phase 5 correction):** R58 (Collision-Free Adjacent Nodes) was previously listed here but has been moved to Step 5 only. Collision detection cannot be reliably executed by an LLM during generation; it is reserved for post-generation validation.

### Step 5 — Validation-time checks

All topology rules run after coordinate assignment:

| Priority | Rule | Check type |
|----------|------|-----------|
| P0 | R58 Collision-Free Adjacent Nodes | all-pairs distance |
| P1 | R55 Topology-Progression Mode Alignment | classification + lookup |
| P1 | R56 Depth-Axis Monotonicity | depth vs coordinate correlation |
| P1 | R59 Bounding Box Viewport Fit | min/max coordinate scan |
| P1 | R61 Convergence Point Visual Prominence | parent position comparison |
| P2 | R57 Hub Node Size Dominance | size hierarchy comparison |
| P2 | R62 Parallel Column Spacing Uniformity | column center variance |
| P2 | R63 Grid Catalog Aspect Ratio | width/height calculation |
| P2 | R64 Decorative Image Topology Alignment | bounding box containment |
| P3 | R60 Topology-Shape Vocabulary Coherence | shape count + role analysis |

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
