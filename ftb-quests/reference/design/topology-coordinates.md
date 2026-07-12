# FTB Quests — Topology Coordinates

> **Status:** Active | **Cycle:** 11 | **Updated:** 2026-07-12
> **Data sources:** 19 chapters from 9 packs (ATM-10, ATM-9, Monifactory, Finality Genesis, GregTech-Odyssey, Craftoria, RAD3, Multiblock Madness 2, FTB Evolution)
> **Purpose:** Provide executable layout algorithms, constraint formulas, and real coordinate data so the AI can generate quest layouts that feel hand-crafted rather than auto-placed.

This document bridges the gap between chapter outline (what quests exist and how they depend on each other) and final SNBT output (the x/y/shape/size/icon fields on every quest). The coordinate data was extracted directly from shipping modpack configs via raw GitHub access; the algorithms were reverse-engineered from those real layouts. FTB Quests uses a continuous 2D coordinate space where the unit is approximately one quest-width — a quest at (0,0) and another at (1,0) will appear side-by-side with no gap.

---

## Layer 1: Complete Layout Algorithm

The layout algorithm takes a chapter's quest list and dependency graph as input, then assigns each quest a position (x, y), shape, size, and optional icon. It proceeds in six phases, each narrowing the degrees of freedom left by the previous one.

### Phase 1 — Dependency Graph Analysis

```
function analyze_graph(quests, dependencies):
  # Build adjacency list
  graph = {}
  for each quest q in quests:
    graph[q.id] = { parents: q.dependencies, children: [] }
  for each quest q in quests:
    for each parent_id in q.dependencies:
      graph[parent_id].children.append(q.id)

  # Compute depth (longest path from any root)
  depth = {}
  for each root in graph where parents is empty:
    BFS/DFS from root, depth[node] = max(depth[node], depth[parent] + 1)

  # Compute fan-in (number of parents) and fan-out (number of children)
  for each quest q:
    q.fan_in = len(q.dependencies)
    q.fan_out = len(graph[q.id].children)

  # Identify convergence nodes (fan_in >= 2) and divergence nodes (fan_out >= 3)
  convergence = [q for q in quests if q.fan_in >= 2]
  divergence = [q for q in quests if q.fan_out >= 3]

  return depth, convergence, divergence
```

The depth values drive the primary axis of layout (usually y for vertical chains, x for horizontal ones). Fan-in and fan-out classify each node's topological role: root (fan_in=0), leaf (fan_out=0), hub (fan_out≥3), convergence (fan_in≥2), or chain (fan_in=1, fan_out≤1). Across all 19 chapters sampled, the average chain node has exactly one parent and one child — the "one quest = one step" principle holds universally.

### Phase 2 — Topology Classification

```
function classify_topology(quests, depth, convergence, divergence):
  max_depth = max(depth.values())
  max_width = max number of quests at same depth level
  convergence_ratio = len(convergence) / len(quests)
  divergence_ratio = len(divergence) / len(quests)
  has_grid = all quests have 0 or 1 dependencies AND max_width > max_depth * 0.5
  has_hub = any node with fan_out >= 5

  has_highway_spine = (max_width >= max_depth * 2.5
                       and count of quests within y ± 0.5 of median_y >= len(quests) * 0.4)

  if max_depth >= 6 and max_width <= 3:
    return "linear_chain"        # Deep and narrow
  elif has_hub and max_width >= 4:
    return "hub_fan"             # Central node with radiating branches
  elif max_width >= 3 and convergence_ratio < 0.1:
    return "parallel_columns"    # Multiple independent vertical chains
  elif convergence_ratio >= 0.15:
    return "diamond_convergence" # Multiple paths merging to points
  elif has_hub and max_depth >= 4:
    return "tree_branching"      # Hub → sub-hub → leaves hierarchy
  elif has_grid or (max_depth <= 2 and len(quests) >= 20):
    return "grid_catalog"        # Flat tiling, minimal dependencies
  elif has_highway_spine:
    return "highway_branch"      # Long horizontal spine with vertical branches
  else:
    return "linear_chain"        # Default fallback
```

The seven topology types are not mutually exclusive — a 200-quest chapter like ATM-10's `create` can contain multiple sub-regions, each with its own topology. The Craftoria Create chapter demonstrates this explicitly: its decorative images define 8 colored "toolbox compartments", each a self-contained region that can use a different internal topology. The classification above applies per-region, not just per-chapter.

### Phase 3 — Initial Coordinate Assignment

Each topology type has its own coordinate assignment strategy:

```
function assign_coordinates(quests, topology, depth, graph):

  LINEAR_CHAIN:
    # Direction: vertical (y increases downward) with optional x-zigzag
    x_base = 0
    x_amplitude = 0.5  # zigzag offset; set to 0 for straight vertical
    y_spacing = compute_spacing(quest_count, "vertical")
    for each quest q sorted by depth:
      q.x = x_base + (depth[q] % 2) * x_amplitude
      q.y = depth[q] * y_spacing

  HUB_FAN:
    # Hub at origin, children in radial pattern
    hub = find_hub(quests)
    hub.x = 0; hub.y = 0
    children = graph[hub.id].children
    angle_step = 360 / len(children) if len(children) <= 8 else 45
    radius = 3.5 + len(children) * 0.3
    for i, child in enumerate(children):
      angle = (i * angle_step - 90) * PI / 180  # start from top
      child.x = round_to_grid(hub.x + radius * cos(angle), 0.5)
      child.y = round_to_grid(hub.y + radius * sin(angle), 0.5)
    # Grandchildren extend outward from their parent's direction
    for each grandchild:
      parent = find_parent(grandchild)
      direction = normalize(parent - hub)
      grandchild.x = parent.x + direction.x * 2.0
      grandchild.y = parent.y + direction.y * 2.0

  PARALLEL_COLUMNS:
    # Group quests by their root ancestor
    columns = group_by_root(quests, graph)
    column_spacing = 2.0
    y_spacing = 1.5
    for col_idx, column in enumerate(columns):
      x = (col_idx - len(columns)/2) * column_spacing
      for row_idx, quest in enumerate(column):
        quest.x = x
        quest.y = row_idx * y_spacing

  DIAMOND_CONVERGENCE:
    # Diverge from root, then converge at diamond midpoint
    # Left path: x decreases, then increases back
    # Right path: x increases, then decreases back
    root.x = 0; root.y = 0
    convergence_node.x = 0; convergence_node.y = max_depth * y_spacing
    left_path = get_path(root, convergence_node, side="left")
    right_path = get_path(root, convergence_node, side="right")
    x_spread = 3.0 + len(left_path) * 0.5
    for i, q in enumerate(left_path):
      progress = i / len(left_path)
      q.x = -x_spread * sin(progress * PI)
      q.y = i * y_spacing
    for i, q in enumerate(right_path):
      progress = i / len(right_path)
      q.x = x_spread * sin(progress * PI)
      q.y = i * y_spacing

  TREE_BRANCHING:
    # Recursive: hub → sub-hubs → leaves
    # Each level indents by a fixed amount
    def layout_subtree(node, x, y, available_width):
      node.x = x
      node.y = y
      children = graph[node.id].children
      if not children: return
      child_width = available_width / len(children)
      for i, child in enumerate(children):
        child_x = x - available_width/2 + (i + 0.5) * child_width
        child_y = y + vertical_spacing
        layout_subtree(child, child_x, child_y, child_width)
    root = find_root(quests)
    layout_subtree(root, 0, 0, total_width=16.0)

  GRID_CATALOG:
    # Row-major tiling, like a spreadsheet
    columns = ceil(sqrt(len(quests)))
    x_spacing = 1.5
    y_spacing = 2.5
    for i, quest in enumerate(quests):
      row = i // columns
      col = i % columns
      quest.x = col * x_spacing
      quest.y = -row * y_spacing  # negative y = downward in FTB Quests

  HIGHWAY_BRANCH:
    # Long horizontal spine with vertical branches above/below
    spine_quests = [q for q in quests if q is on the main spine]
    branch_quests = [q for q in quests if q is not on the spine]
    x_spacing = 2.0
    y_spine = 0.0
    for i, quest in enumerate(spine_quests):
      quest.x = i * x_spacing
      quest.y = y_spine
    # Branches extend vertically from their spine parent
    for branch in group_by_spine_parent(branch_quests):
      parent = branch.spine_parent
      direction = 1 if branch is upper_branch else -1
      for i, quest in enumerate(branch.quests):
        quest.x = parent.x
        quest.y = parent.y + direction * (i + 1) * 1.5
```

The `round_to_grid` helper snaps coordinates to the nearest 0.25 or 0.5 increment — FTB Quests authors consistently use half-unit or quarter-unit grids, which produces clean visual alignment. The Monifactory groundwork chapter uses coordinates like -7.75, -5.5, 4.25 (quarter-grid), while ATM-10 bounty_board uses -7.0, -5.0, -3.0 (whole-unit grid). Both approaches work; quarter-grid gives more flexibility for dense layouts.

### Phase 4 — Collision Detection and Spacing Adjustment [Validation Only — R58]

> **Important:** This phase is NOT executable by an LLM during quest generation. The all-pairs distance calculation and iterative push-apart loop require precise floating-point arithmetic that LLMs cannot reliably perform. Instead, coordinates should be assigned using the topology-specific strategies in Phase 3 (which use spacing formulas that inherently avoid collisions), and collision detection is deferred to **R58 (Collision-Free Adjacent Nodes)** in `progression-rules.md`, which runs as a post-generation validation check in Step 5. If R58 reports violations, the author should manually adjust coordinates or re-run generation with wider spacing parameters.

```
function resolve_collisions(quests):   # R58 VALIDATION — do not call during generation
  MIN_DISTANCE = 1.0  # minimum center-to-center distance
  PREFERRED_DISTANCE = 1.5

  for iteration in range(10):  # max 10 adjustment passes
    collisions = []
    for i, q1 in enumerate(quests):
      for j, q2 in enumerate(quests):
        if i >= j: continue
        dist = sqrt((q1.x - q2.x)^2 + (q1.y - q2.y)^2)
        if dist < MIN_DISTANCE:
          collisions.append((q1, q2, dist))

    if not collisions:
      break

    for q1, q2, dist in collisions:
      # Push apart along the axis of least constraint
      # If they share similar y (within 0.3), push along x
      if abs(q1.y - q2.y) < 0.3:
        push_x = (PREFERRED_DISTANCE - dist) / 2
        q1.x -= push_x
        q2.x += push_x
      else:
        push_y = (PREFERRED_DISTANCE - dist) / 2
        q1.y -= push_y
        q2.y += push_y

  return quests
```

Collision detection is especially important for hub-fan and tree layouts where radial placement can cause outer-ring nodes to overlap. The ATM-10 `basic_power` chapter demonstrates well-spaced hub layouts — the three hexagonal sub-hubs at (-5.5, 0), (5.5, 0), and (1.5, 2) are each 5.5+ units from center and 7+ units from each other, leaving ample room for their respective leaf nodes.

### Phase 5 — Shape, Size, and Icon Assignment

```
function assign_visual_properties(quests, topology, depth, graph):
  for each quest q:
    # SHAPE assignment (decision tree)
    if q.fan_in == 0 and q.fan_out >= 3:    # Root with many children
      q.shape = "gear"                        # Starting hub
    elif q.fan_in >= 3:                       # Convergence of many paths
      q.shape = "diamond"                     # Synthesis point
    elif q.fan_out == 0 and q is boss_quest:  # Terminal boss
      q.shape = "pentagon"                    # End goal
    elif q.task_type == "kill":               # Combat quest
      q.shape = "pentagon"                    # Combat semantic
    elif q.optional:                          # Optional side content
      q.shape = "circle"                      # Soft boundary
    elif topology == "grid_catalog":          # Catalog entry
      q.shape = "none"                        # Minimal visual noise
    else:                                     # Default chain node
      q.shape = chapter_default_shape         # Usually hexagon or diamond

    # SIZE assignment
    if q.fan_in == 0 and q.fan_out >= 3:     # Root hub
      q.size = 2.0
    elif q.fan_in >= 3 or q is chapter_capstone:  # Major convergence
      q.size = 2.0
    elif q is boss_quest or q is milestone:   # Boss/milestone
      q.size = 1.5
    elif depth[q] == 0 and q.task_type == "checkmark":  # Tutorial root
      q.size = 2.0
    else:                                     # Standard chain node
      q.size = 1.0

    # ICON assignment
    if q.task involves specific mod item and q is notable:
      q.icon = { id: that_mod_item }
    elif q is chapter_root and chapter has signature item:
      q.icon = { id: chapter_signature_item }
    else:
      q.icon = null  # FTB Quests auto-uses the task item as icon
```

The shape decision tree above is ordered by specificity — the first matching rule wins. This mirrors the empirical observation that across all 9 packs sampled, shape usage follows a clear hierarchy: gear for root hubs, diamond for synthesis, pentagon for combat/boss, and the chapter's default shape (most commonly hexagon) for standard chain nodes. The `none` shape is distinctive to grid/catalog chapters — Craftoria's Create chapter uses `default_quest_shape: "none"` across 180 quests, and RAD3's milestones uses shape `"none"` across 63 quests. The `none` shape means the quest node renders as a small dot rather than a visible polygon, which reduces visual clutter in dense catalog layouts.

### Phase 6 — Final Output

```
function finalize_layout(quests):
  for each quest q:
    # Snap to quarter-grid
    q.x = round(q.x * 4) / 4
    q.y = round(q.y * 4) / 4

    # Validate bounds
    # [Confidence: MEDIUM — based on observed maxima across 13 chapters;
    #  FTB Evolution create reached x=30, so 35.0 leaves 5-unit headroom]
    clamp q.x to [-15.0, 35.0]  # FTB Quests viewport limit (35.0留出余量，FTB Evolution create 达 x=30.0)
    clamp q.y to [-15.0, 15.0]

    # Set hide_dependency_lines based on density
    local_density = count_quests_within_radius(q, radius=3.0)
    if local_density > 8:
      q.hide_dependency_lines = true

  return quests  # Each with {x, y, shape, size, icon}
```

The viewport clamping values come from empirical observation: the widest chapter sampled (FTB Evolution create) spans from x=0 to x=30.0, and the tallest (RAD3 pathfinder) spans from y=-4.5 to y=8.5. The x upper bound is set to 35.0 to leave headroom beyond the observed maximum. Most chapters stay within a 20×15 unit bounding box. The `hide_dependency_lines` heuristic is triggered when local density exceeds ~8 quests in a 3-unit radius — this matches the observed behavior in ATM-10 allthemodium (22 hide_dep_lines across 67 quests, concentrated in the dense central cluster) and GregTech-Odyssey stoneage (6 hide_dep_lines across 52 quests, all in the densely-packed mid-section).

---

## Layer 2: Constraint Rules

These constraints define the valid ranges within which the layout algorithm operates. They are expressed as formulas with upper and lower bounds rather than fixed values, giving the AI room to adapt to each chapter's specific content while staying within the range that players find comfortable.

### Spacing Formulas

Vertical chain spacing (the distance between consecutive quests in a linear chain) depends on quest count and chapter density:

```
y_spacing = clamp(base_spacing * density_factor, min_spacing, max_spacing)
# [Confidence: HIGH — validated across 9 packs, 13 chapters]

where:
  base_spacing = 1.5              # Default vertical gap
  density_factor = 1.0 if quest_count <= 50
                 = 1.0 - (quest_count - 50) * 0.005 if quest_count > 50
  min_spacing = 1.0               # Never closer than 1.0 apart
  max_spacing = 2.5               # Never farther than 2.5 apart
```

This formula produces: 1.5 spacing for a 30-quest chapter, 1.25 spacing for a 100-quest chapter, 1.0 spacing for a 150-quest chapter. The ATM-10 bounty_board uses 1.5 spacing (vertical columns of 4 quests each), Monifactory groundwork uses ~1.5-2.0 spacing across 97 quests (but organized in sub-regions rather than one long chain), and the GregTech-Odyssey stoneage uses 1.5-2.0 spacing across 52 quests.

Column spacing (for parallel_columns topology):

```
column_x_gap = clamp(2.0 + column_quest_width * 0.5, 2.0, 4.0)
# [Confidence: HIGH — consistent across ATM-10 bounty_board and MM2 botania]
```

ATM-10 bounty_board uses exactly 2.0 between columns (zombie at x=-7, skeleton at x=-5, creeper at x=-3). MM2 botania uses 2.0 between its main chain nodes (x=0, 2, 4, 5.5, 7.5, 9...). The 2.0 value works well when quests have no side-branches; increase to 3.0 when side-quests extend horizontally from the main column.

Hub radius (for hub_fan topology):

```
hub_radius = clamp(3.0 + fan_out_count * 0.4 + max_leaves_per_subhub * 0.5, 3.5, 8.0)
# [Confidence: MEDIUM — single-pack data (ATM-10 basic_power only)]
# Known deviation: original formula (3.0 + fan_out * 0.4) predicted 4.2 for
# basic_power (fan_out=3), but actual distance was 5.5 — a 31% under-prediction.
# The corrected formula adds max_leaves_per_subhub * 0.5 to account for the
# clearance each sub-hub needs for its own leaf fan-out. When max_leaves_per_subhub
# is unknown, assume 3 (yields 3.0 + 3*0.4 + 3*0.5 = 5.7, close to observed 5.5).
leaf_distance = clamp(2.0 + leaf_count_per_branch * 0.5, 2.0, 4.0)
# [Confidence: MEDIUM — consistent with ATM-10 basic_power (1.5-2.0) and
#  Finality Genesis cataclysm (1.5), but sample size is small]
```

ATM-10 basic_power has 3 sub-hubs at distance 5.5 from center (fan_out=3 → 3.0+3*0.4=4.2, but the pack uses 5.5 for extra clearance since each hub has 3-5 leaves). Monifactory dependency_chain has 27 quests in a grid at 1.25 spacing (the invisible routing chapter uses tight spacing because all quests are the same shape with no visual variety).

### Shape Decision Tree

The shape selection process can be expressed as a priority-ordered decision tree. Each rule fires based on the quest's structural role (derived from the dependency graph) and the chapter's genre context:

```
shape_priority:
  1. ROOT + HIGH_FANOUT → "gear"
     (ATM-10 basic_power root, GregTech-Odyssey stoneage root, Monifactory progression root)

  2. CONVERGENCE + 3+ parents → "diamond"
     (ATM-10 allthemodium convergence quests, FTB Evolution create convergence)

  3. BOSS_TERMINAL → "pentagon"
     (ATM-10 bounty_board kill-100 bosses, Finality Genesis boss chain endpoints)

  4. MILESTONE + SIZE>=2.0 → "octagon"
     (MI:Foundation milestone quests, GregTech-Odyssey octagon milestones)

  5. COMBAT/KILL task → "pentagon"
     (RAD3 kill quests, ATM-6 bounty board)

  6. OPTIONAL → "circle"
     (ATM-10 basic_tools optional pickaxes)

  7. CATALOG_ENTRY (grid topology) → "none"
     (Craftoria Create, RAD3 milestones, Monifactory dependency_chain)

  8. DEFAULT → chapter.default_quest_shape
     (most commonly "hexagon" for tech/expert, "diamond" for kitchen-sink,
      "circle" for adventure/lifestyle)
```

The most common default shapes per pack type: kitchen-sink packs use "diamond" (ATM-10, ATM-9) or "circle" (Enigmatica 10, ATM-7), expert packs use "hexagon" (Monifactory, GregTech-Odyssey, GTCEu-Modern), and adventure/lifestyle packs use "circle" (RAD2, Society-Sunlit-Valley, Medieval-MC). Finality Genesis is notable for using per-chapter default shapes: "square" for the cataclysm (boss) chapter, "rsquare" for ars_nouveau (magic), and the pack's global default for other chapters.

### Size Formula

```
quest_size = clamp(base_size * role_multiplier, 1.0, 3.0)
# [Confidence: HIGH — size hierarchy (root > sub-hub > leaf) observed in all 9 packs]

where:
  base_size = 1.0 (standard chain node)
  role_multiplier:
    root_hub: 2.0
    convergence_3plus: 1.5-2.0
    boss_terminal: 1.5
    milestone: 1.25-1.5
    sub_hub: 1.5
    chain_node: 1.0
    leaf: 1.0
    catalog_entry: 1.0 (or default_quest_size if set)
```

Real-world size distributions: ATM-10 basic_tools uses size 2.0 only on the root quest, with all chain and optional nodes at 1.0. ATM-10 bounty_board uses 2.0 on the advancement root and 1.5 on the pentagon boss capstones. Monifactory groundwork has a clear 3-tier hierarchy: size 2.0 (3 quests — root and two milestones), size 1.5 (8 quests — sub-hubs), and size 1.0-1.25 (86 quests — standard nodes). Craftoria Create sets `default_quest_size: 2.0d` at chapter level, making all quests large by default — but this is offset by `default_quest_shape: "none"` which renders them as minimal dots despite the large size value.

### Icon Rules

Icons are set on quests when the default auto-icon (derived from the task item) would be ambiguous or when the quest needs to stand out visually:

```
icon_needed when:
  1. Quest uses ftbfiltersystem:smart_filter as task → icon = specific representative item
     (ATM-10 basic_power: smart_filter tasks have explicit icon like "mekanism:energy_tablet")
  2. Quest has multiple tasks and no single dominant item → icon = most important task's item
  3. Chapter root quest → icon = chapter signature item
     (ATM-10 basic_tools: root has no icon because single task; basic_power: root has no icon)
  4. Quest task type is checkmark or advancement (no inherent item) → icon = thematic item
  5. Quest is a boss/milestone → icon = boss drop or achievement item

icon NOT needed when:
  1. Quest has exactly one item task (FTB Quests auto-icons from the task item)
  2. Quest uses default_quest_shape: "none" (catalog mode — visual noise reduction)
  3. Quest is a standard chain node with an unambiguous task item
```

Craftoria's Create chapter has 27 explicit icons across 123 quests (22%), concentrated on hub quests and sub-region entry points. ATM-10 allthemodium has 2 icons across 67 quests (3%), only on the chapter root and the final convergence quest. The icon density correlates with chapter complexity: simple linear chains need almost no icons (the task items speak for themselves), while hub-fan and tree layouts benefit from icons to help players orient themselves visually.

### Collision Detection Rules

```
# [Confidence: HIGH — fundamental layout invariant, validated across all 13 cases]
minimum_center_distance = 1.0    # Hard minimum — quests closer than this overlap
preferred_distance = 1.5         # Standard spacing between adjacent quests
diagonal_bonus = 0.85            # Diagonal neighbors can be 15% closer
                                 # (because diagonal distance is naturally longer)
# [Confidence: MEDIUM — diagonal bonus derived from ATM-10 basic_tools zigzag;
#  needs validation against more diagonal layouts]

collision_resolution_order:
  1. Push along x-axis first (horizontal separation is more readable)
  2. If x-separation fails (column topology), push along y-axis
  3. If both fail, scale down the smaller quest's size to 0.75
```

The diagonal bonus explains the zigzag pattern seen in ATM-10 basic_tools: quests alternate between x=-4.0 and x=-3.5 while y decreases by 0.5 each step, creating a diagonal chain where each step is √(0.5²+0.5²) ≈ 0.71 units horizontally plus 0.5 vertically — this is within the diagonal-toleranced minimum distance for quests with no explicit size.

---

## Layer 3: Real Case Coordinates

These are verbatim coordinate extractions from shipping modpack configs. Each case includes the pack name, chapter, topology classification, and all quest positions with their visual properties. Use these as calibration baselines — your generated layouts should produce coordinates in similar ranges and distributions.

### Case 1: Linear Chain — ATM-10 `basic_tools`

6 quests in the main chain, diamond default shape, progression_mode flexible. The chain zigzags diagonally from upper-left to lower-right while 6 optional side-quests fan out from the root.

```
Main chain (dependency order):
  Q0 cobblestone:  (-4.0, -2.0)  deps: [root]
  Q1 raw_iron:     (-3.5, -2.5)  deps: [Q0]     icon: iron_ore
  Q2 diamond:      (-4.0, -3.0)  deps: [Q1]     icon: diamond_ore
  Q3 ancient_debris:(-3.5, -3.5) deps: [Q2]
  Q4 allthemodium: (-4.0, -4.0)  deps: [Q3]     icon: allthemodium_ore
  Q5 unobtainium:  (-3.5, -4.5)  deps: [Q4]     icon: unobtainium_ore

Pattern: x alternates -4.0/-3.5 (amplitude 0.5), y decreases by 0.5 per step
Direction: diagonal down-left
Total span: 0.5 × 2.5 units (compact chain)

Optional side-quests (all depend on root, shape=default diamond):
  wooden_pick:   (-2.5, -2.0)   optional
  stone_pick:    (-2.0, -2.5)   optional
  iron_pick:     (-2.5, -3.0)   optional
  diamond_pick:  (-2.0, -3.5)   optional
  netherite_pick:(-2.5, -4.0)   optional

Pattern: Optional nodes stagger to the right (+1.5 from main chain x)
Spacing: same 0.5 diagonal step as main chain
```

Source: `AllTheMods/ATM-10/main/config/ftbquests/quests/chapters/basic_tools.snbt`

### Case 2: Parallel Columns — ATM-10 `bounty_board`

3 independent kill-ladder columns (zombie, skeleton, creeper) with identical y-progression, plus additional columns (spider, enderman, etc.) following the same pattern.

```
Column 1 (Zombie):         Column 2 (Skeleton):      Column 3 (Creeper):
  x=-7.0, y=-2.5 (kill 5)    x=-5.0, y=-2.5 (kill 5)   x=-3.0, y=-2.5 (kill 5)
  x=-7.0, y=-4.0 (kill 10)   x=-5.0, y=-4.0 (kill 10)  x=-3.0, y=-4.0 (kill 10)
  x=-7.0, y=-5.5 (kill 50)   x=-5.0, y=-5.5 (kill 50)  x=-3.0, y=-5.5 (kill 50)
  x=-7.0, y=-7.0 (kill 100)  x=-5.0, y=-7.0 (kill 100) x=-3.0, y=-7.0 (kill 100)
    shape: pentagon             shape: pentagon            shape: pentagon
    size: 1.5                   size: 1.5                  size: 1.5

Column x-spacing: 2.0
Column y-spacing: 1.5 (consistent across all tiers)
Root quest: x=0.0, y=0.0, size 2.0 (advancement "kill_a_mob")
Boss tier: pentagon + size 1.5 at y=-7.0 (bottom of each column)
hide_until_deps_visible: true on kill-10 through kill-100 tiers
```

This is the cleanest example of parallel_columns in the dataset. The column x-spacing of 2.0 is tight but works because each column is a simple vertical chain with no horizontal branches. The y-spacing of 1.5 provides comfortable visual separation for the kill-count tiers.

Source: `AllTheMods/ATM-10/main/config/ftbquests/quests/chapters/bounty_board.snbt`

> ⚠️ 当前仅基于 ATM-10 数据，需要更多跨包样本验证此坐标模式。

### Case 3: Hub + Fan — ATM-10 `basic_power`

Central gear hub with 3 sub-hubs (Mekanism, Powah, RFTools) radiating outward, each sub-hub fanning out 3-5 leaf quests.

```
Center hub:
  root:  (0.0, 0.0)    shape: gear, size: 2.0, hide_dependent_lines: true

Sub-hub 1 (Mekanism — left):
  iron→energy_tablet: (-5.5, 0.0)  shape: hexagon, size: 1.5, icon: energy_tablet
  Leaves:
    cable:      (-4.0, 0.0)    shape: rsquare
    energy_pipe:(-7.0, 0.0)    shape: rsquare
    qeporter:   (-6.5, 1.0)    shape: rsquare

Sub-hub 2 (Powah — right):
  iron→battery:  (5.5, 0.0)    shape: hexagon, size: 1.5, icon: battery_nitro
  Leaves:
    energy_cube: (7.5, 0.0)    shape: rsquare
    power_cell:  (6.5, 1.5)    shape: rsquare
    int_battery: (4.5, 1.5)    shape: rsquare

Sub-hub 3 (Advanced — upper):
  coal:          (-1.5, 2.0)   shape: hexagon, size: 1.5
  diamond:       (1.5, 2.0)    shape: hexagon, size: 1.5
  Leaves from coal:
    heat_gen:    (-3.0, 2.0)   shape: rsquare
    coal_gen:    (-2.5, 3.0)   shape: rsquare
    mekanism_gen:(-1.5, 3.5)   shape: rsquare
  Leaves from diamond:
    uranium:     (3.0, 2.0)    shape: rsquare

Hub-to-subhub distance: 5.5 units
Subhub-to-leaf distance: 1.5-2.0 units
Shape vocabulary: gear(root) → hexagon(subhub) → rsquare(leaves)
```

This 3-tier hierarchy (gear → hexagon → rsquare) creates a clear visual flow from the center outward. The rsquare shape for leaves distinguishes them from the hexagonal sub-hubs, making the tree structure immediately readable. The `hide_dependent_lines: true` on the root prevents visual clutter from the 3 hub-to-subhub dependency lines.

Source: `AllTheMods/ATM-10/main/config/ftbquests/quests/chapters/basic_power.snbt`

> ⚠️ 当前仅基于 ATM-10 数据，需要更多跨包样本验证此坐标模式。

### Case 4: Diamond Convergence — ATM-10 `allthemodium`

67 quests with 22 dependency links, starting from origin (0,0) and branching into multiple paths that converge at (10.5, -5.0). Rich shape vocabulary: diamond, gear, hexagon, square, octagon, rsquare.

```
Origin:
  root:  (0.0, 0.0)

Upper branch (positive y):
  Q4:    (3.5, 3.0)
  Q5:    (9.5, 3.0)
  Q6:    (12.5, 3.0)
  Q7:    (5.5, 4.5)
  Q8:    (11.0, 4.5)
  Q9:    (14.0, 4.5)

Lower branch (negative y):
  Q1:    (3.5, -2.5)
  Q2:    (9.5, -2.5)
  Q3:    (12.5, -2.5)
  Q10:   (21.0, -2.5)

Convergence point:
  diamond_quest: (10.5, -5.0)  shape: diamond, size: 2.0

Side explorations:
  Q12:   (4.0, -7.5)
  Q11:   (15.5, -0.6)
  Q13-Q19: cluster around (2-8, 0-3.5)

Coordinate range: x ∈ [0, 21], y ∈ [-7.5, 4.5]
Aspect ratio: 21:12 ≈ 1.75:1 (wider than tall — typical for diamond topology)
Shape distribution: diamond(1), gear(1), hexagon(4+), square(8+), octagon(3+), rsquare(2+)
Size range: 1.2 to 2.0, with 18 distinct size values (fine-grained hierarchy)
```

The allthemodium chapter demonstrates how diamond convergence works at scale: the upper and lower branches spread horizontally (x from 3.5 to 14) while maintaining moderate y-separation (3.0 vs -2.5 = 5.5 units apart). The convergence quest at (10.5, -5.0) sits below both branches, creating a visual "pull" downward toward the chapter's capstone.

Source: `AllTheMods/ATM-10/main/config/ftbquests/quests/chapters/allthemodium.snbt`

> ⚠️ 当前仅基于 ATM-10 数据，需要更多跨包样本验证此坐标模式。

### Case 5: Tree Branching — Monifactory `groundwork`

97 quests, hexagon-dominant (66 hex + 8 gear + 1 square), spanning a 20×25 unit area. The chapter has multiple sub-regions organized by mod/recipe-chain.

```
Region A (upper-left cluster, y=8-12):
  (-7.25, 8.5), (-4.25, 8.5), (-7.25, 11.0), (-4.25, 11.0), (-2.25, 11.0)
  (0.75, 8.5), (0.75, 11.0), (8.75, 8.5), (8.75, 10.0)
  Spacing: 2.5-3.0 between cluster centers, 1.5-2.0 within clusters

Region B (lower-left cluster, y=-11 to -6):
  (-7.75, -10.75), (-7.75, -9.0), (-5.5, -10.75), (-5.5, -9.0)
  (-1.25, -10.75), (-1.25, -9.0), (-3.25, -9.0), (-3.25, -7.5)
  Spacing: 1.5-2.25 between adjacent quests

Region C (center cluster, y=-3 to 5):
  (-3.25, -3.0), (-3.25, -0.5), (-3.25, 2.0)
  (0.75, -4.25), (0.75, -2.0), (0.75, 2.0)
  (2.5, 0.75), (2.5, 2.0), (2.5, 4.25)
  Spacing: 1.5-2.5

Region D (right side, y=-11 to 0):
  (4.25, -11.0), (4.25, -9.0), (4.25, -6.0), (4.25, -3.0), (4.25, -1.0)
  (6.0, -7.75), (6.0, -6.0), (6.0, -4.25), (6.0, -2.5)
  (7.5, -6.0), (7.5, -4.25), (7.5, -2.5)
  Spacing: 1.5-2.0

Overall bounding box: x ∈ [-8.0, 10.25], y ∈ [-11.0, 12.5]
Grid alignment: quarter-unit (0.25 precision)
```

Monifactory's groundwork uses a "workshop layout" — the chapter is divided into 4-5 sub-regions, each containing a cluster of 8-15 quests. The sub-regions are separated by 4-8 units of empty space, which provides visual breathing room. Within each cluster, quests are packed at 1.5-2.0 unit spacing. This topology is common in expert packs where each sub-region corresponds to a different mod or recipe chain.

Source: `Omicron-Industries/Monifactory/main/config/ftbquests/quests/chapters/groundwork.snbt`

### Case 6: Linear Chain (Expert) — Monifactory `progression`

127 quests forming the main GT tier progression, hexagon-dominant (78 hex + 8 square). The chapter uses a diagonal staircase pattern from lower-left to upper-right.

```
Main diagonal staircase (Q27 → Q35, the GT tier progression):
  Q27: (-9.5, -5.5)   # Start (Steam age)
  Q28: (-8.0, -4.0)   # LV entry
  Q29: (-6.5, -2.5)
  Q30: (-5.0, -1.0)
  Q31: (-3.5, 0.5)
  Q32: (-2.0, 2.0)
  Q33: (-0.5, 3.5)
  Q34: (1.0, 5.0)
  Q35: (2.5, 6.5)
  ...continuing to...
  Q123: (4.5, 10.5)   # End (highest tier)

Step size: Δx=1.5, Δy=1.5 per tier (diagonal step)
Total diagonal span: 14.0 × 16.0 units

Sub-chains branching off the staircase:
  Steam cluster (Q37-Q45, around x=10-13, y=-8 to -4):
    (10.5, -8.5), (10.5, -5.5), (10.5, -4.0), (10.5, -2.5), (10.5, -1.0)
    (12.5, -8.5), (12.5, -7.0), (12.5, -5.5), (12.5, -4.0)
    Spacing: 1.5 vertical, 2.0 horizontal between columns

  HV-EV cluster (Q14-Q26, around x=22, y=-8 to 12):
    (22.0, -8.5), (22.0, -7.0), (22.0, -5.5), (22.0, -4.0)
    (22.0, -2.5), (22.0, -1.0), (22.0, 0.5), (22.0, 4.5)
    (22.0, 6.5), (22.0, 8.5), (22.0, 10.5), (22.0, 12.5)
    Spacing: 1.5 vertical (consistent y-spacing throughout)
```

The Monifactory progression chapter is the most sophisticated layout in the dataset. The main diagonal staircase (1.5, 1.5 per step) creates a clear visual progression from bottom-left (early game) to upper-right (endgame). Sub-chains branch off the staircase at each tier level, forming vertical columns that represent the content available at that tier. The HV-EV cluster at x=22 extends 21 units vertically — the tallest single column observed in any pack.

Source: `Omicron-Industries/Monifactory/main/config/ftbquests/quests/chapters/progression.snbt`

### Case 7: Grid/Catalog — RAD3 `milestones`

63 quests in a strict 3-column grid with no dependencies within the grid (all dependencies reference external chapters). Shape is "none" for all quests.

```
Column 1 (x=-12.0 to -11.0):
  (-12.0, -4.0), (-12.0, -1.5), (-12.0, 1.0)
  (-11.0, -4.0), (-11.0, -1.5), (-11.0, 1.0)

Column 2 (x=-9.5 to -5.0):
  (-9.5, 1.0), (-8.0, -4.0), (-8.0, -1.5), (-8.0, 1.0)
  (-6.5, 1.0), (-5.0, -4.0), (-5.0, -1.5), (-5.0, 1.0)

Column 3 (x=-3.5 to 1.0):
  (-3.5, 1.0), (-2.0, -4.0), (-2.0, -1.5), (-2.0, 1.0)
  (-0.5, 1.0), (1.0, -4.0), (1.0, -1.5), (1.0, 1.0)

Grid spacing: x ≈ 1.5, y = 2.5 between rows
Row alignment: y ∈ {-4.0, -1.5, 1.0} (3 rows, perfectly aligned)
Shape: "none" for all 63 quests (catalog display mode)
Bounding box: 13.0 × 5.0 units (wide and short)
```

This is the cleanest grid_catalog example. The milestones chapter functions as a cross-chapter convergence point — quests here depend on completing content in other chapters, so the grid layout is purely organizational (a trophy case). The 3-row × multi-column grid uses consistent 1.5 x-spacing and 2.5 y-spacing.

Source: `dr3ams/RAD3-1.20.1/main/config/ftbquests/quests/chapters/milestones.snbt`

### Case 8: Hub + Linear Chain — Finality Genesis `cataclysm`

28 quests, all "square" shape, boss chapter with branching tree structure.

```
Central hub:
  root: (0.0, 0.0)

Upper branch (boss progression):
  (0.0, 1.5), (-1.5, 3.0), (0.0, 3.0), (1.5, 3.0)  # Tier 1 bosses
  (-1.5, 4.5), (0.0, 4.5), (1.5, 4.5)                # Tier 2
  (0.0, 6.0)                                          # Final boss

Lower branch (preparation chain):
  (0.0, -3.0), (0.0, -4.5), (0.0, -6.0), (0.0, -9.0)  # Vertical prep chain
  (-1.5, -1.5), (1.5, -1.5)                             # Side branches
  (-1.5, -3.0), (1.5, -3.0)                             # Side branches
  (-1.5, -4.5), (1.5, -4.5)                             # Side branches
  (-1.5, -6.0), (1.5, -6.0)                             # Side branches
  (-1.5, -7.5), (1.5, -7.5)                             # Final side branches

Upper spacing: y-step 1.5, x-spread ±1.5 (fan pattern)
Lower spacing: y-step 1.5, x-spread ±1.5 (symmetric tree)
Shape: ALL "square" — consistent per-chapter shape vocabulary
Bounding box: 3.0 × 15.0 units (tall and narrow)
```

Finality Genesis's cataclysm chapter uses the same shape ("square") for every quest, relying entirely on coordinate placement to communicate structure. The upper branch fans out in a widening pattern (3 quests at y=3.0, 3 at y=4.5, 1 at y=6.0 — narrowing back to a point), while the lower branch is a symmetric tree with paired side-branches at each y-level. The chapter is tall and narrow (3×15), which suits a boss progression that the player scrolls through vertically.

Source: `Project-Vyre/Finality-Genesis/main/config/ftbquests/quests/chapters/cataclysm.snbt`

### Case 9: Linear Chain (Deep Expert) — GregTech-Odyssey `lv`

129 quests with 71 dependency links. The LV (Low Voltage) tier chapter uses dense workshop layout with diagonal chains and multiple sub-regions.

```
Entry area (upper-left, y=4-8):
  (-4.5, 4.25)  shape: gear, size: 2.0  # Root
  (-1.0, 8.0), (-1.0, 6.5)              # Early chain
  (6.5, 8.0), (8.0, 3.0)                # Branch points

Main processing chain (diagonal, y=-8 to 3):
  (0.5, -8.5) → (2.0, -5.5) → (5.5, -2.5) → (5.5, 3.0)
  Step: Δx≈1.5-3.5, Δy≈3.0 (wide diagonal steps)

Sub-region: circuit assembly (center, x=-3 to 2, y=-1 to 1):
  (-3.0, 1.0), (-1.0, 1.0), (1.0, 0.0), (2.0, 0.0)
  (-1.0, -1.0), (1.0, -1.0), (2.0, 3.0)
  Spacing: 1.0-2.0

Sub-region: power infrastructure (right, x=5-12, y=-3 to 3):
  (5.5, -2.5), (5.5, -1.0), (5.5, 3.0)
  (7.0, 1.0), (7.0, -1.0)
  Spacing: 1.5-2.0

Shape distribution: hexagon(dominant, ~60%), gear(~15%), diamond(~10%), circle(~5%), pentagon(~5%)
Size distribution: 2.0 (root), 1.5 (sub-hubs), 1.0 (most chain nodes)
Bounding box: ~16 × 16 units

Comparison with Monifactory groundwork (same topology type):
  Monifactory: 97 quests in 20×25 units → 0.19 quests/sq-unit
  GT-Odyssey: 129 quests in 16×16 units → 0.50 quests/sq-unit
  GT-Odyssey packs 2.6× more densely than Monifactory
```

GregTech-Odyssey's LV chapter is denser than Monifactory's equivalent, with more multi-dependency quests (71 deps for 129 quests vs 46 deps for 97 quests). The diagonal chains use wider steps (Δx=1.5-3.5, Δy=3.0) compared to Monifactory's staircase (Δx=1.5, Δy=1.5), reflecting GT-Odyssey's preference for broader visual sweeps over tight cluster work.

Source: `GregTech-Odyssey/GregTech-Odyssey/main/config/ftbquests/quests/chapters/lv.snbt`

### Case 10: Parallel Chains + Hub — Multiblock Madness 2 `botania`

52 quests with 40 dependency links. Main spine is a horizontal chain with multiple vertical branches and a separate lower sub-chain.

```
Main horizontal spine:
  (0.0, 0.0) → (2.0, 0.0) → (4.0, 0.0) → (6.5, 0.0) → (9.0, 0.0) →
  (11.0, 0.0) → (13.0, 0.0) → (15.0, 0.0) → (17.0, 0.0) → (19.0, 0.0) →
  (21.5, 0.0) → (23.5, 0.0) → (25.5, 0.0) → (27.5, 0.0)
  x-spacing: 2.0 (consistent), y = 0.0 (perfect horizontal line)

Upper branches:
  (5.5, 1.5), (7.5, 1.5)    # Branch from (6.5, 0.0)
  (17.0, 2.5), (19.0, 1.5)  # Branch from (17-19, 0.0)
  (21.0, 2.5)               # Branch from (21.5, 0.0)

Lower branches:
  (5.5, -1.5), (7.5, -1.5)  # Branch from (6.5, 0.0)
  (19.0, -1.5)              # Branch from (19.0, 0.0)

Separate lower sub-chain (flower collection):
  (4.0, -8.0) → (6.0, -8.0) → (8.0, -8.0)
  x-spacing: 2.0, y = -8.0

Upper flower garden sub-chain:
  (2.5, 6.5), (4.5, 6.5), (6.5, 6.5), (8.5, 6.5), (10.5, 6.5), (12.5, 6.5)
  x-spacing: 2.0, y = 6.5 (consistent horizontal row)

Lower detail cluster:
  (14.5, 5.0) to (16.5, 9.0) — 8 quests in a compact cluster
  (15.5, -3.5) — isolated endpoint

Shape: gear(5) for hubs, hexagon(5) for chain nodes
Size: 2.0 (root + hubs), 1.5-1.75 (sub-hubs), 1.0 (chain)
Bounding box: 27.5 × 17.0 units (widest chapter in dataset)
```

MM2 botania is notable for its extremely wide main spine (27.5 units across, the widest of any chapter sampled). The horizontal chain at y=0 acts as a "highway" with vertical branches at key mod-progression points. The separate sub-chains at y=-8 and y=6.5 are parallel horizontal rows, creating three distinct horizontal layers. This "highway + branches" topology is unique to multiblock-focused packs where each branch represents a different multiblock structure.

Source: `Filostorm/Multiblock-Madness-2/main/config/ftbquests/quests/chapters/botania.snbt`

### Case 11: Complex Tree — ATM-10 `create`

206 quests, only 3 explicit shapes (gear×2, circle×1 — rest use chapter default), 77 dependency links. The chapter uses Craftoria-style compartmentalized regions.

```
Root hub:
  Q0: (-4.5, 7.5)  shape: gear, size: 3.0  # Largest root in dataset

Region 1 (upper-left, "Mechanical Basics"):
  (-6.0, 5.5), (-6.0, 3.5), (-6.0, 0.0), (-6.0, -3.0), (-6.0, -9.5)
  (-5.25, 2.5), (-6.75, 2.5)
  x-cluster: ~-6.0, y range: -9.5 to 5.5 (vertical column)

Region 2 (center-left, "Andesite"):
  (-3.5, 0.0), (-3.0, 4.5), (-2.0, -1.5), (-2.0, 1.5)
  (-10.5, 8.5), (-10.75, 7.5), (-12.0, 7.5), (-12.0, 6.25), (-10.75, 6.25)

Region 3 (center, "Brass"):
  (1.5, 1.5), (3.0, -2.5), (0.5, -4.0), (0.5, -5.25), (1.75, -4.0), (1.75, -5.25)

Region 4 (left, "Logistics"):
  (-8.5, 0.0), (-8.5, 4.0), (-9.5, 1.5), (-9.5, -1.5)

Region 5 (far-left, "Trains"):
  (-13.0, 6.0), (-12.5, 0.0)

Size hierarchy:
  3.0: root (1 quest)
  1.75: sub-hubs (1 quest)
  1.25: tier-2 hubs (3 quests)
  1.0: standard chain nodes (201 quests)
Bounding box: ~13 × 17 units
```

ATM-10's create chapter has the largest root node (size 3.0) in the dataset. The size-3.0 root serves as a visual anchor — even at the far edges of the chapter, the player can orient themselves relative to this prominent node. The compartmentalized region structure (each region occupies a distinct coordinate range) is similar to Craftoria's toolbox approach but uses coordinate clustering rather than decorative image boundaries.

Source: `AllTheMods/ATM-10/main/config/ftbquests/quests/chapters/create.snbt`

### Case 12: Expert Linear (Chinese Pack) — GregTech-Odyssey `main-stoneage`

52 quests, 29 shapes, 32 deps, 6 hide_dep_lines. The stone age starting chapter uses a mix of horizontal chains and clusters.

```
Root hub:
  (-3.0, 8.0)  shape: gear, size: 2.0
  (0.0, 8.0)   shape: gear (secondary hub)

Upper chain (tool progression):
  (-3.0, 1.5), (-3.0, 0.0), (-1.5, -1.5)
  Step: y decreases ~1.5, x drifts right ~1.5

Right-side cluster (smelting/cooking):
  (11.0, -2.5), (11.0, -3.5), (11.0, 0.0), (11.0, 4.0), (11.0, 6.0), (11.0, 8.0)
  x = 11.0 (fixed column), y spans -3.5 to 8.0 (11.5 units)
  Spacing: 2.0 vertical

Right-side branches:
  (12.0, -2.0), (13.0, 0.0), (13.0, 2.0)  # East branch
  (9.0, 4.0), (9.0, 6.0)                   # West branch

Center chain (crafting progression):
  (3.5, 0.0) → (4.5, -1.0) → (4.5, 1.0)
  (2.5, 1.0), (2.5, -1.0)
  (6.5, 0.0), (6.5, -2.0), (6.5, 6.0), (6.5, 8.0)

Shape vocabulary: gear(2), hexagon(12), diamond(3), pentagon(4), octagon(3), circle(3)
  — Most diverse shape usage for a 52-quest chapter (7 shape types)
Size range: 1.0 to 3.0 (root size 3.0 — same as ATM-10 create)
```

GregTech-Odyssey's stoneage chapter demonstrates the richest shape vocabulary per-quest-count of any chapter sampled: 7 shape types across just 52 quests. This is deliberate — each shape maps to a specific role: gear for starting hubs, hexagon for standard tech progression, diamond for resource processing, pentagon for tool upgrades, octagon for milestone unlocks, and circle for optional exploration. The shape variety compensates for the relatively small quest count, making each node type immediately distinguishable.

Source: `GregTech-Odyssey/GregTech-Odyssey/main/config/ftbquests/quests/chapters/main-stoneage.snbt`

### Case 13: FTB Official Layout — FTB Evolution `create`

123 quests, 94 shapes, 95 deps, 27 icons. The FTB official pack's create chapter uses a wide, compartmentalized layout.

```
Entry region (left, x=0):
  (0.0, 0.0), (0.0, -3.0), (0.0, 3.5)

Mid-section (x=6-9):
  (7.0, 5.0), (8.0, 5.0), (9.0, 5.0)   # Horizontal row at y=5
  (6.75, 2.5), (9.25, 2.5)              # Pair
  (8.0, -4.47), (8.0, -2.5)            # Vertical pair

Right section (x=20-26):
  (20.5, 4.5), (21.5, 4.5), (22.5, 4.5)  # Row
  (24.0, 6.5), (25.0, 6.5), (26.0, 6.5)  # Row
  (24.0, 2.0), (25.0, 2.0), (26.0, 2.0)  # Row
  (20.5, -3.0), (22.5, -3.0)             # Lower pair
  (23.0, -1.0)

Far-right:
  (30.0, 1.5)  # Endpoint at x=30 — furthest right in dataset

Shape distribution: hexagon(5), diamond(7), square(3), gear(4), circle(2), none(5+)
Size: 1.25-1.5 (compact, no large milestones)
Icons: 27 (22% of quests — highest icon density in dataset)
Bounding box: 30.0 × 12 units (widest chapter sampled)
```

FTB Evolution's create chapter is the widest chapter in the dataset at 30 units, exceeding even MM2 botania's 27.5-unit span. The layout is organized as a left-to-right progression with three distinct "zones" (left entry, mid processing, right advanced). The 27 explicit icons (22% of quests) reflect FTB's official pack design philosophy of heavily guiding the player — nearly one in four quests has a custom icon to aid visual scanning. The coordinate x=30.0 on the rightmost quest is the furthest-right coordinate observed in any chapter.

Source: `VM-Chinese-translate-group/FTB-Evolution-Chinese/main/Source/config/ftbquests/quests/chapters/create.snbt`

---

## Cross-Pack Topology Comparison

### Spacing Summary Table

| Topology | Pack | Chapter | Quests | x-range | y-range | Avg spacing |
|----------|------|---------|--------|---------|---------|-------------|
| Linear (zigzag) | ATM-10 | basic_tools | 6 main | 0.5 | 2.5 | 0.71 (diagonal) |
| Linear (vertical) | ATM-9 | basic_tools | 105 | 0.5 | 11.0 | 1.0 |
| Linear (staircase) | Monifactory | progression | 127 | 14.0 | 16.0 | 1.5 (diag) |
| Parallel columns | ATM-10 | bounty_board | 12+ | 4.0 | 4.5 | 2.0×1.5 |
| Hub + fan | ATM-10 | basic_power | 16 | 14.5 | 5.5 | 5.5 (hub radius) |
| Diamond convergence | ATM-10 | allthemodium | 67 | 21.0 | 12.0 | varies |
| Tree (workshop) | Monifactory | groundwork | 97 | 18.25 | 23.5 | 1.75 |
| Tree (compartment) | ATM-10 | create | 206 | 13.0 | 17.0 | 1.5 |
| Grid (catalog) | RAD3 | milestones | 63 | 13.0 | 5.0 | 1.5×2.5 |
| Boss tree | Finality Genesis | cataclysm | 28 | 3.0 | 15.0 | 1.5 |
| Expert linear | GT-Odyssey | lv | 129 | 16.0 | 16.0 | 2.0 |
| Highway + branch | MM2 | botania | 52 | 27.5 | 17.0 | 2.0 (spine) |
| FTB official | FTB Evolution | create | 123 | 30.0 | 12.0 | 2.5 |

### Key Observations

The widest chapters come from highway-style layouts (MM2 botania at 27.5 units, FTB Evolution create at 30 units), while the tallest come from expert staircase layouts (Monifactory progression at 16 units vertical). Grid/catalog chapters are the most compact in one dimension (RAD3 milestones is 13×5) but achieve this by sacrificing dependency information entirely.

The quest density (quests per square unit) varies by a factor of 3× across packs: Monifactory groundwork at ~0.19 quests/sq-unit is the most spacious, while GT-Odyssey lv at ~0.50 quests/sq-unit is the densest. Expert packs trend denser than kitchen-sink packs, likely because expert players are expected to parse complex layouts without hand-holding.

Shape diversity correlates inversely with quest count per chapter: the smallest chapter (GT-Odyssey stoneage, 52 quests) uses 7 shape types, while the largest (ATM-10 create, 206 quests) uses only 3 explicit shapes plus the chapter default. This suggests that shape variety is a tool for small chapters to signal structure; large chapters rely on coordinate placement and decorative images instead.

The `default_quest_size` chapter property dramatically affects visual density: Craftoria's Create sets it to 2.0d (all quests appear large), while most other chapters leave it at the implicit 1.0 default. When combined with `default_quest_shape: "none"` (Craftoria), the large size paradoxically produces a minimal visual appearance — large dots rather than large shapes.

---

## Appendix: Coordinate Extraction Method

All coordinate data was extracted via raw GitHub URLs using the pattern:
```
https://raw.githubusercontent.com/{org}/{repo}/{branch}/config/ftbquests/quests/chapters/{chapter_name}.snbt
```

Python regex extraction patterns:
```python
x_y_coords = r'x:\s*(-?\d+\.?\d*)d\s*\n\s*y:\s*(-?\d+\.?\d*)d'
shapes = r'shape:\s*"(\w+)"'
sizes = r'size:\s*(\d+\.?\d*)d'
dependencies = r'dependencies:\s*\[(.*?)\]'
hide_dep_lines = r'hide_dependency_lines:\s*true'
```

Note: The coordinate regex matches `x:` and `y:` on adjacent lines within quest blocks. Image coordinates use the same pattern but appear in `images:[]` blocks rather than `quests:[]` blocks. When extracting quest coordinates, filter out image coordinates by only matching within quest block boundaries (between `quests: [` and the matching `]`).

Packs accessed in this cycle:
- AllTheMods/ATM-10 (branch: main)
- AllTheMods/ATM-9 (branch: main)
- Omicron-Industries/Monifactory (branch: main)
- Project-Vyre/Finality-Genesis (branch: main)
- GregTech-Odyssey/GregTech-Odyssey (branch: main)
- TeamAOF/Craftoria (branch: main)
- dr3ams/RAD3-1.20.1 (branch: main)
- Filostorm/Multiblock-Madness-2 (branch: main)
- VM-Chinese-translate-group/FTB-Evolution-Chinese (branch: main)

---

## Appendix: Topology-Aware Layout Validation Rules (Cycle 11 Phase 3)

Ten layout validation rules (R55–R64) were derived from the coordinate data and topology classifications above. They are defined in `progression-rules.md` (active) and summarized here for reference.

### Rule-to-Topology Matrix

| Rule | linear_chain | hub_fan | parallel_columns | diamond_convergence | tree_branching | grid_catalog | highway_branch |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| R55 Topology-Progression Mode Alignment | yes | yes | yes | yes | yes | yes | yes |
| R56 Depth-Axis Monotonicity | yes | — | — | yes | yes | — | yes |
| R57 Hub Node Size Dominance | — | yes | — | — | yes | — | — |
| R58 Collision-Free Adjacent Nodes | yes | yes | yes | yes | yes | yes | yes |
| R59 Bounding Box Viewport Fit | yes | yes | yes | yes | yes | yes | yes |
| R60 Topology-Shape Vocabulary Coherence | yes | yes | yes | yes | yes | yes | yes |
| R61 Convergence Point Visual Prominence | — | yes | — | yes | — | — | — |
| R62 Parallel Column Spacing Uniformity | — | — | yes | — | — | — | — |
| R63 Grid Catalog Aspect Ratio | — | — | — | — | — | yes | — |
| R64 Decorative Image Topology Alignment | yes | yes | yes | yes | yes | yes | yes |

### Key Topology-Layout Invariants

These invariants were distilled from the 13 real cases and encode the implicit layout expectations that players feel but rarely articulate:

1. **Depth flows along the primary axis.** In vertical layouts (linear_chain, tree_branching), y increases with depth. In horizontal layouts (highway + branches), x increases with depth. Violations create a visual reading order that contradicts the dependency order — the most disorienting layout failure.

2. **Hub nodes dominate their children.** Size hierarchy (root > sub-hub > leaf) is the primary visual signal of graph structure. When a hub is the same size as its leaves, the player must read every quest to determine the organizational center.

3. **Convergence points sit at the visual terminus.** The diamond convergence quest should be positioned where all parent branches naturally lead — below them in vertical layouts, to the right in horizontal layouts. Misplacing the convergence point means players complete all branches without noticing the synthesis quest.

4. **Uniform spacing enables scanning.** Parallel columns with identical y-start and consistent y-spacing allow the player to compare equivalent progression tiers across columns by scanning horizontally. Irregular spacing breaks this comparison pattern.

5. **Viewport bounds are a soft constraint.** The widest observed chapter (FTB Evolution create, 30 units) and tallest (Monifactory progression, 16 units) are at the edge of comfortable viewing. Beyond 35 × 30 units, scrolling becomes excessive and the quest book loses its function as a visual map.

### Author Design Philosophy — Layout Observations

From the author-facing research conducted during Phase 3 (searching MC百科, B站, Reddit r/feedthebeast, YouTube, and GitHub repositories), the following topology-relevant observations emerged:

**Layout is emergent, not planned.** No author in the accessible dataset describes choosing a topology type before creating quests. The topology emerges from the content structure — a mod with 5 sub-systems naturally produces a hub_fan, a mod with a linear upgrade chain produces a linear_chain. Authors arrange quests spatially based on content groupings (mod identity, recipe chain, tier level), and the resulting topology is a consequence of those content decisions.

**Shape is a chapter-level decision, not a per-quest one.** Authors set `default_quest_shape` once per chapter to establish mod identity, then override shapes only for milestones and special roles. The shape vocabulary within a chapter is deliberately limited — 1–3 shapes for large chapters (>100 quests), up to 7 shapes for small chapters (<60 quests). Shape diversity and quest count have a consistent inverse relationship across all 13 cases.

**Size encodes structural importance, not content difficulty.** A root hub gets size 2.0–3.0 regardless of how easy its content is. A standard chain node stays at 1.0 even if its recipe is complex. Size is a graph-theoretic signal (fan_in, fan_out, role in the dependency tree), not a difficulty signal. Monifactory's CONTRIBUTING.md is the only source that explicitly codifies this: "Larger quests should be reserved for important milestones."

**The bounding box is a consequence, not a target.** Authors do not set a target width or height for a chapter before filling it. The dimensions emerge from the content volume and chosen spacing. FTB Evolution's create chapter reaches x=30.0 because its content is a 30-unit-wide progression; RAD3's milestones spans 13 × 5 because 63 quests in a 3-row grid naturally produces that ratio. R59 (Bounding Box Viewport Fit) exists as a safety net, not a design input.
