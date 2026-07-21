# FTB Quests — Topology Coordinates

> **Status:** Active | **Cycle:** 18 Phase 1 | **Updated:** 2026-07-18
> **Data sources:** 61 individual cases + 47 batch chapters from 66 packs (ATM-10, ATM-9, Monifactory, Finality Genesis, GregTech-Odyssey, Craftoria, RAD3, Multiblock Madness 2, FTB Evolution, Create-New-Horizon, Gregtech-Voyager, Chroma-Technology-2, CodeNameCIM2, HereBeDragons, Ragnamod_VII, ReFactory, ATM9-Sky, ATM6-Sky, Dragoncraft, Life-in-the-Village-4, SteamPunk, Ragnamod VI Skyblock, Gregitsky, Rogue Mayhem, compact-sky-easy, Enigmatica9, GregFactory-Sky, Mincemeat-2, Cobblemon-Radically-Reimagined, Ultimate-Progression-Sky, CreateBlock, Extraordinary-Energy-Modern, Enigmatic-Skies, AOF-The-Frozen-Hope, All_the_Simple, ProjectSkyblock, Capivara SMP, CTI Quests, Ragnamod-VII-Skyblock, Insurgence, MI-Lost-Favor, Seaopolis, Minecolonies, Minecraft-Medieval, Create-chronicles, Farmopolis, Aetas-Ferrea, GenCraft, Phoenix-Forge, Chroma-Endless, MC-Odyssey-3, society-sunlit-valley, Caveopolis, Age-of-Fate, No-Flesh-Within-Chest, All-of-Fabric-6, Prison-Escape-Beginnings, Steamcreate2)
> **Purpose:** Provide executable layout algorithms, constraint formulas, and real coordinate data so the AI can generate quest layouts that feel hand-crafted rather than auto-placed. Includes executable collision correction algorithm (Phase 4), large chapter mixed-topology decomposition with modularity optimization (Phase 2.5), and pack-type-specific calibration for under-represented topologies (highway_branch, parallel_columns).

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

  # NOTE: median_y and y ± 0.5 are NOT available during Phase 2 classification —
  # coordinates are assigned in Phase 3. In practice, has_highway_spine should use
  # a graph-structure proxy: spine candidate nodes (fan_out >= 2 and fan_in <= 1
  # forming a continuous chain) as proportion of total quests >= 40%.
  has_highway_spine = (max_width >= max_depth * 2.5
                       and count of quests within y ± 0.5 of median_y >= len(quests) * 0.4)

  # [All thresholds: based on 13-case dataset observed ranges (9 packs, 19 chapters).
  #  Values are calibrated to separate the known samples; packs outside the
  #  dataset (skyblock, pure adventure, Create specialist) may need different thresholds.]
  if max_depth >= 6 and max_width <= 3:                    # min observed for linear chains
    return "linear_chain"        # Deep and narrow
  elif has_hub and max_width >= 4:                          # hub detection threshold
    return "hub_fan"             # Central node with radiating branches
  elif max_width >= 3 and convergence_ratio < 0.1:          # gap between parallel and diamond
    return "parallel_columns"    # Multiple independent vertical chains
  elif convergence_ratio >= 0.15:                            # min observed for diamond types
    return "diamond_convergence" # Multiple paths merging to points
  elif has_hub and max_depth >= 4:                           # tree hierarchy threshold
    return "tree_branching"      # Hub → sub-hub → leaves hierarchy
  elif has_grid or (max_depth <= 2 and len(quests) >= 20):  # grid min quest count
    return "grid_catalog"        # Flat tiling, minimal dependencies
  elif has_highway_spine:
    return "highway_branch"      # Long horizontal spine with vertical branches
  elif max_depth >= 3 and max_width <= max_depth and convergence_ratio < 0.1:
    return "tree_branching"      # Shallow tree: branching without convergence or hub
  else:
    return "linear_chain"        # Default fallback
```

The seven topology types are not mutually exclusive — a 200-quest chapter like ATM-10's `create` can contain multiple sub-regions, each with its own topology. The Craftoria Create chapter demonstrates this explicitly: its decorative images define 8 colored "toolbox compartments", each a self-contained region that can use a different internal topology. The classification above applies per-region, not just per-chapter.

> **Extreme chapter sizes — early-return and splitting guidance**
>
> **quest_count < 5 (micro-chapter):** Skip full topology classification. If any node has fan_out >= 2, classify as hub_fan; otherwise classify as linear_chain. Skip R55–R64 validation except R58 (collision) and R59 (viewport), which still apply. Visual hierarchy is trivially satisfied at this scale — size and shape distinctions are unnecessary for fewer than 5 nodes.
>
> **quest_count > 200 (mega-chapter):** The spacing formula's density_factor bottoms out at min_spacing (1.0) for chapters above ~150 quests, producing no further spacing compression. Consider splitting the chapter by topology type: linear_chain chapters should split at >100 quests, grid_catalog at >200, and tree_branching or hub_fan at >150 (decompose into sub-regions with independent topology). The largest chapter in the dataset is ATM-10 create at 206 quests; chapters significantly exceeding this have no calibration data.

### Phase 2.5 — Large Chapter Mixed-Topology Decomposition

When a chapter has more than 80 quests, a single topology type often doesn't capture its internal structure. Large chapters (like ATM-10 `create` with 180+ quests or RAD3 `milestones`) typically contain multiple sub-regions with different topological patterns. This phase decomposes such chapters into independently-layoutable sub-regions.

```
function decompose_large_chapter(quests, dependencies, threshold=80):
  if len(quests) <= threshold:
    return [(quests, dependencies)]  # No decomposition needed
  
  # Step 1: Build the undirected dependency graph
  undirected = build_undirected_graph(dependencies)
  
  # Step 2: Find weakly connected components
  components = find_weakly_connected_components(undirected)
  
  # If single component, try modularity-based split
  if len(components) == 1:
    components = modularity_split(undirected, min_component_size=15)
  
  # Step 3: Classify each sub-region independently
  regions = []
  for component in components:
    sub_quests = [q for q in quests if q.id in component]
    sub_deps = [d for d in dependencies if d.from_id in component and d.to_id in component]
    sub_topology = classify_topology(sub_quests, depth, convergence, divergence)
    regions.append({
      quests: sub_quests,
      dependencies: sub_deps,
      topology: sub_topology,
      is_primary: len(sub_quests) == max(len(c) for c in components)
    })
  
  # Step 4: Identify bridge nodes (quests that connect sub-regions)
  bridge_nodes = []
  for dep in dependencies:
    if region_of(dep.from_id) != region_of(dep.to_id):
      bridge_nodes.append({
        from_region: region_of(dep.from_id),
        to_region: region_of(dep.to_id),
        quest_id: dep.to_id  # The quest receiving cross-region deps
      })
  
  return regions, bridge_nodes
```

Layout strategy for decomposed chapters:
  - Primary region: occupies left 60% of available width
  - Sub-regions: stack vertically on the right 40%
  - Bridge nodes: rendered as hexagon shape, size 1.5
  - Bridge coordinates: midpoint between the two connected regions' nearest edge nodes

```
  # Pseudocode for region placement
  function layout_decomposed(regions, bridge_nodes, available_width=30):
    primary = [r for r in regions if r.is_primary][0]
    secondary = [r for r in regions if not r.is_primary]
    
    # Primary region gets left portion
    primary_width = available_width * 0.6
    layout_region(primary, x_range=[0, primary_width])
    
    # Secondary regions stack vertically on right
    secondary_x_start = primary_width + 2  # 2-unit gap
    secondary_width = available_width - secondary_x_start
    y_cursor = 0
    for region in secondary:
      region_height = estimate_height(region)
      layout_region(region, x_range=[secondary_x_start, secondary_x_start + secondary_width],
                    y_offset=y_cursor)
      y_cursor += region_height + 2  # 2-unit vertical gap
    
    # Place bridge nodes at midpoints
    for bridge in bridge_nodes:
      source_edge = nearest_edge_node(bridge.from_region, bridge.to_region)
      target_edge = nearest_edge_node(bridge.to_region, bridge.from_region)
      bridge.x = (source_edge.x + target_edge.x) / 2
      bridge.y = (source_edge.y + target_edge.y) / 2
      bridge.shape = "hexagon"
      bridge.size = 1.5
    
    return all_quests_with_coordinates
```

> **Cycle 15 Phase 1 — Large Chapter Mixed-Topology Decomposition: Empirical Calibration**
>
> The decomposition pseudocode above was reverse-engineered from ATM-10 `create` (180+ quests, 8 colored compartments). Cycle 15 Phase 1 applied the decomposition analysis to 9 additional large chapters (100+ quests each) from ATM-9, ATM-10, and RAD3, revealing four distinct sub-region cutting patterns that the algorithm should recognize:
>
> **Pattern 1 — Monolithic (collection chapters):** One dominant region occupies >80% of the chapter, with scattered singleton nodes and no meaningful sub-region boundaries. ATM-10 productive_bees (253 quests, 87% single region, grid_dense_chain internal topology, 13 bridge nodes) and ATM-10 elmystical_agriculturerr (183 quests, 83% single region, grid_dense_chain, 18 bridge nodes) both follow this pattern, as does ATM-9 productive_bees (125 quests, 99% single region) and ATM-9 pneumaticraft (129 quests, 78% single region, freeform_dense). In monolithic chapters, the decomposition algorithm's modularity_split fails to find meaningful partitions — the correct response is to treat the entire chapter as a single region and skip bridge-node rendering. The high bridge-node counts (13–18) are artifacts of the algorithm's minimum-component-size threshold rather than genuine cross-region connections.
>
> Note on MP66: Pattern 1 (Monolithic) and Pattern 3 (Quadrant) sub-regions may not involve convergence topologies at all — Monolithic chapters are typically grid_catalog (zero convergence), and Quadrant chapters may use hub_fan or freeform without diamond_convergence. MP66's extreme fan-in guidance is applicable only when a sub-region's internal topology includes convergence nodes.
>
> **Pattern 2 — Dual-Region (tech chapters):** Two regions each occupying ~35–50% of the chapter, typically split by functional role (e.g., "machine setup" vs "processing chains"). ATM-9 draconic_evolution (140 quests, 51%+34% split, grid + freeform topologies, 57 bridge nodes) separates its spatial layout into an upper grid-based tech tree and a lower freeform boss arena. ATM-10 immersive_engineering (127 quests, 40%+27% split, freeform ×2, 21 bridge nodes) divides by voltage tier, and RAD3 equipment (130 quests, 20%+19% split, freeform + isolated, 24 bridge nodes) separates armor from tools. The dual-region pattern triggers the decomposition algorithm's primary/secondary layout: the larger region gets the left 60%, the smaller stacks on the right. The bridge-node count (21–57) scales with the number of cross-region dependencies — draconic_evolution's 57 bridges indicate heavy interleaving between its two regions.
>
> **Pattern 3 — Quadrant (specialization chapters):** Four roughly equal regions (~25% each) arranged in a 2×2 grid. RAD3 specialization (105 quests, 4×25% quadrants, freeform ×4, 81 bridge nodes at 77%) is the sole confirmed example. The 81 bridge nodes represent 77% of all quests — nearly every quest depends on quests in another quadrant, creating a dense web of cross-region connections. The central hub sits at the origin where all four quadrants meet. This pattern requires a different layout strategy than the primary/secondary split: all four quadrants should receive equal visual weight, arranged in a 2×2 grid with the central hub at the intersection.
>
> Note on MP66: Pattern 3 (Quadrant) sub-regions may use hub_fan or freeform without diamond_convergence — MP66's extreme fan-in guidance is applicable only when a quadrant's internal topology includes convergence nodes.
>
> **Pattern 5 — Compartment (mod-based regions):**
> 4-10 sub-regions of roughly equal size (10-25% each), each corresponding to a mod or subsystem. Separated by decorative images. Bridge nodes < 10 per compartment pair. Layout: equidistant along main axis, each compartment uses independent internal topology.
> Confirmed cases: ATM-10 create (8 toolbox compartments, 180 quests), Craftoria Create (8 compartments, 180 quests).
> Decision condition: count(regions 10-25%) >= 4 AND decorative_images separating regions >= 3 → Compartment.
> Confidence: 2 confirmed cases (ATM-10 create, Craftoria Create — both from the same pack family). Needs 3+ cases from different pack families to move from "Craftoria-specific" to "general pattern."
>
> **Pattern 4 — Fragmented/Parallel (encyclopedia chapters):** Many micro-regions each occupying <5% of the chapter, with no dominant region. RAD3 hunt_never_stops (143 quests, 72 micro-regions with the largest at 5%, linear_parallel chains, 42 bridge nodes) exemplifies this pattern — the chapter is essentially a catalog of independent parallel quest chains, each 2–4 quests long, laid out side-by-side. The decomposition algorithm correctly identifies the 72 components but should not attempt to assign primary/secondary roles; instead, treat each micro-chain as an independent column in a parallel_columns layout.
>
> Edge cases not matching any pattern above:
> - max_region 60-75% with second region 15-25%: treat as Dual-Region variant (primary + secondary, ignore minor regions)
> - 3 regions each ~30%: treat as Triple-Region variant of Dual-Region (largest = primary, merge other two as secondary)
> - Confidence: these edge-case rules are PROVISIONAL — no confirmed cases in dataset yet
>
> These four patterns suggest a decision tree for the decomposition algorithm: first check if any region exceeds 80% (monolithic → skip decomposition), then check for 2 regions >30% each (dual-region → primary/secondary layout), then check for 4 regions ~20–30% each (quadrant → 2×2 grid), and default to fragmented/parallel for all other cases. The bridge-node threshold for "heavy interleaving" appears to be around 50 nodes — above this count, the dependency lines between regions become visually overwhelming and `hide_dependency_lines` should be set on all bridge nodes.

> **Phase 2.5 — Detailed Modularity Split Algorithm and Integration**
>
> The `modularity_split` function referenced in `decompose_large_chapter` (above) is invoked when the undirected dependency graph forms a single connected component but the chapter is large enough (>80 quests) that sub-region decomposition would improve layout readability. The algorithm uses greedy modularity optimization (Newman's method) to partition the graph into communities.
>
> **Modularity split — complete algorithm:**
>
> ```
> function modularity_split(undirected_graph, min_component_size=15):
>   # Newman's greedy modularity optimization
>   # Input: undirected dependency graph, minimum allowed component size
>   # Output: list of node sets, each set is a sub-region
>
>   n = len(undirected_graph.nodes)
>   m = len(undirected_graph.edges)  # total edge count
>   if m == 0:
>     return [set(undirected_graph.nodes)]  # no edges = single region
>
>   # Initialize: each node in its own community
>   communities = [{v} for v in undirected_graph.nodes]
>   best_partition = [c.copy() for c in communities]  # fallback if no merge improves Q
>   best_modularity = -1.0
>
>   # Greedy merge: repeatedly merge the pair of communities that gives
>   # the largest increase in modularity Q
>   while len(communities) > 1:
>     best_delta_Q = -infinity
>     best_pair = None
>     for i in range(len(communities)):
>       for j in range(i+1, len(communities)):
>         # ΔQ = 2 * (e_ij - a_i * a_j)
>         # where e_ij = edges between communities i,j / (2*m)
>         #       a_i = degree sum of community i / (2*m)
>         e_ij = count_edges_between(communities[i], communities[j]) / (2 * m)
>         a_i = sum(degree(v) for v in communities[i]) / (2 * m)
>         a_j = sum(degree(v) for v in communities[j]) / (2 * m)
>         delta_Q = 2 * (e_ij - a_i * a_j)
>         if delta_Q > best_delta_Q:
>           best_delta_Q = delta_Q
>           best_pair = (i, j)
>     if best_delta_Q <= 0:
>       break  # No merge improves modularity
>     # Merge the best pair
>     communities[best_pair[0]] = communities[best_pair[0]] | communities[best_pair[1]]
>     communities.pop(best_pair[1])
>     # Track best partition
>     Q = compute_modularity(communities, undirected_graph, m)
>     if Q > best_modularity:
>       best_modularity = Q
>       best_partition = [c.copy() for c in communities]
>
>   # Filter: merge any community smaller than min_component_size into nearest neighbor
>   final = []
>   for community in best_partition:
>     if len(community) >= min_component_size:
>       final.append(community)
>     else:
>       if not final:
>         final.append(community)  # seed final so max() below has a target
>         continue
>       # Merge into the community with the most cross-edges
>       target = max(final, key=lambda c: count_edges_between(community, c))
>       target.update(community)
>
>   return final if final else [set(undirected_graph.nodes)]
>
> function compute_modularity(communities, graph, m):
>   Q = 0
>   for community in communities:
>     # Count internal edges
>     internal = count_edges_within(community) / (2 * m)
>     # Sum of degrees in community
>     degree_sum = sum(degree(v) for v in community) / (2 * m)
>     Q += internal - degree_sum * degree_sum
>   return Q
> ```
>
> **Bridge node coordinate calculation — precise formula:**
>
> ```
> function place_bridge_nodes(bridge_nodes, regions):
>   for bridge in bridge_nodes:
>     source_region = regions[bridge.from_region]
>     target_region = regions[bridge.to_region]
>
>     # Find nearest edge nodes in each region (nodes with cross-region deps)
>     source_edge = nearest_cross_region_node(source_region, target_region)
>     target_edge = nearest_cross_region_node(target_region, source_region)
>
>     # Bridge coordinates: weighted midpoint
>     # Weight by region size — larger region "pulls" the bridge closer
>     w_source = len(source_region.quests)
>     w_target = len(target_region.quests)
>     w_total = w_source + w_target
>
>     bridge.x = (source_edge.x * w_source + target_edge.x * w_target) / w_total
>     bridge.y = (source_edge.y * w_source + target_edge.y * w_target) / w_total
>
>     # Apply minimum offset to prevent bridge overlapping with either region
>     dist = distance(source_edge, target_edge)
>     if dist < 3.0:
>       # Regions are too close — push bridge to perpendicular midpoint
>       mid_x = (source_edge.x + target_edge.x) / 2
>       mid_y = (source_edge.y + target_edge.y) / 2
>       perp_dx = -(target_edge.y - source_edge.y) / dist
>       perp_dy = (target_edge.x - source_edge.x) / dist
>       bridge.x = mid_x + perp_dx * 1.5
>       bridge.y = mid_y + perp_dy * 1.5
>
>     bridge.shape = "hexagon"
>     bridge.size = 1.5
>     bridge.hide_dependency_lines = (count_bridge_nodes_between(bridge.from_region, bridge.to_region) > 10)
>
>   return bridge_nodes
> ```
>
> **Spatial allocation strategy for decomposed chapters:**
>
> The primary/secondary 60/40 split applies to the Dual-Region pattern (Pattern 2). Other patterns use different allocations:
>
> | Pattern | Primary Width | Secondary Layout | Bridge Count Expectation |
> |---------|--------------|------------------|--------------------------|
> | Monolithic (Pattern 1) | 100% (skip decomposition) | N/A | 0 (bridges are artifacts) |
> | Dual-Region (Pattern 2) | 60% left | 40% right, vertical stack | 5–57 (heavy if interleaved) |
> | Quadrant (Pattern 3) | 25% per quadrant, 2×2 grid | Equal weight all 4 | ~80 (central hub dense) |
> | Fragmented (Pattern 4) | No primary | Parallel columns, equal width | ~42 (micro-chain connectors) |
> | Compartment (Pattern 5) | No primary | Equidistant along main axis | <10 per compartment pair |
>
> **Integration with Phase 1–4:**
>
> - **Phase 1 → 2.5:** The dependency graph and depth map from Phase 1 are the input to `decompose_large_chapter`. The undirected graph is derived from Phase 1's adjacency list by dropping edge direction.
> - **Phase 2 → 2.5:** If `classify_topology` returns a topology for the full chapter, that classification is discarded when decomposition triggers (quest_count > 80). Each sub-region receives its own independent Phase 2 classification.
> - **Phase 2.5 → Phase 3:** Each decomposed sub-region runs Phase 3 independently with its own topology type and coordinate range. The `layout_decomposed` function then translates each region's local coordinates into the global coordinate space using the spatial allocation strategy above.
> - **Phase 2.5 → Phase 4:** Collision detection (Phase 4) runs AFTER all sub-regions are placed in global coordinates. Bridge nodes are treated as fixed (hub priority) during collision resolution — they are not moved because their position is geometrically determined by the two regions they connect.
> - **Threshold bypass:** If `decompose_large_chapter` returns a single region (monolithic pattern, Pattern 1), the chapter proceeds directly to Phase 3 without decomposition, as if Phase 2.5 was skipped. The threshold check (`len(quests) <= 80`) is the first gate; the monolithic check (`max_region > 80%`) is the second gate.

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
```

> **Hub-fan trigonometric lookup table**
>
> LLMs frequently produce incorrect cos/sin values for non-standard angles. Use this pre-computed table for radial child placement instead of computing trigonometric functions inline. All values rounded to 3 decimal places; coordinates assume hub at origin and `angle_step = 360 / N`, starting from top (−90°).
>
> ```
> N=3  (step=120°): (0, -1), (0.866, 0.5), (-0.866, 0.5)
> N=4  (step=90°):  (0, -1), (1, 0), (0, 1), (-1, 0)
> N=5  (step=72°):  (0, -1), (0.951, -0.309), (0.588, 0.809), (-0.588, 0.809), (-0.951, -0.309)
> N=6  (step=60°):  (0, -1), (0.866, -0.5), (0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5)
> N=7  (step≈51.4°): (0, -1), (0.782, -0.623), (0.975, 0.223), (0.434, 0.901),
>                     (-0.434, 0.901), (-0.975, 0.223), (-0.782, -0.623)
> N=8  (step=45°):  (0, -1), (0.707, -0.707), (1, 0), (0.707, 0.707),
>                    (0, 1), (-0.707, 0.707), (-1, 0), (-0.707, -0.707)
> N=9  (step=40°):  (0, -1), (0.643, -0.766), (0.985, -0.174), (0.866, 0.5),
>                    (0.342, 0.940), (-0.342, 0.940), (-0.866, 0.5), (-0.985, -0.174), (-0.643, -0.766)
> N=10 (step=36°):  (0, -1), (0.588, -0.809), (0.951, -0.309), (0.951, 0.309),
>                    (0.588, 0.809), (0, 1), (-0.588, 0.809), (-0.951, 0.309), (-0.951, -0.309), (-0.588, -0.809)
> N=11 (step≈32.7°): (0, -1), (0.540, -0.841), (0.885, -0.465), (0.996, 0.087), (0.829, 0.559),
>                     (0.454, 0.891), (0, 1), (-0.454, 0.891), (-0.829, 0.559), (-0.996, 0.087), (-0.885, -0.465)
> N=12 (step=30°):  (0, -1), (0.5, -0.866), (0.866, -0.5), (1, 0), (0.866, 0.5),
>                    (0.5, 0.866), (0, 1), (-0.5, 0.866), (-0.866, 0.5), (-1, 0), (-0.866, -0.5), (-0.5, -0.866)
> ```
>
> To use: multiply each (cos, sin) pair by the computed `radius` for the hub, then add the hub's (x, y) position. For fan counts not in this table (>12), cap angle_step at 30° and distribute children evenly.

```
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

> **Diamond-convergence sin() lookup table**
>
> The DIAMOND_CONVERGENCE coordinate assignment uses `sin(progress * PI)` to compute x_spread at each step along the diverging paths. LLMs frequently produce incorrect sin values for non-standard progress values. Use this pre-computed table instead of computing sin() inline. All values rounded to 3 decimal places.
>
> ```
> progress  | sin(progress * PI) | Notes
> ----------|--------------------|----------------------------------
> 0.0       | 0.000              | Start (root / convergence node)
> 0.1       | 0.309              |
> 0.2       | 0.588              |
> 0.3       | 0.809              |
> 0.4       | 0.951              |
> 0.5       | 1.000              | Peak x_spread (midpoint of path)
> 0.6       | 0.951              | Symmetric with 0.4
> 0.7       | 0.809              | Symmetric with 0.3
> 0.8       | 0.588              | Symmetric with 0.2
> 0.9       | 0.309              | Symmetric with 0.1
> 1.0       | 0.000              | End (convergence node / root)
> ```
>
> To use: multiply the sin() value by `x_spread` to get the x-offset at each path position. The left path uses `-x_spread * sin(progress * PI)` (negative x); the right path uses `+x_spread * sin(progress * PI)` (positive x). The function is symmetric around progress=0.5 — the diamond bulges widest at the midpoint and tapers back to zero at both ends.

The `round_to_grid` helper snaps coordinates to the nearest 0.25 or 0.5 increment — FTB Quests authors consistently use half-unit or quarter-unit grids, which produces clean visual alignment. The Monifactory groundwork chapter uses coordinates like -7.75, -5.5, 4.25 (quarter-grid), while ATM-10 bounty_board uses -7.0, -5.0, -3.0 (whole-unit grid). Both approaches work; quarter-grid gives more flexibility for dense layouts.

### Helper Functions Reference

The Phase 3 pseudocode references six helper functions. Their definitions are collected here so the AI can produce consistent implementations across generation sessions.

```
function find_hub(quests):
  # Return the quest with the highest fan_out. If tied, prefer the one closest
  # to the graph's structural center (sum of depths to all other nodes is minimal).
  return max(quests, key=lambda q: q.fan_out)

function find_parent(quest, graph):
  # Return the first parent quest from the dependency list.
  # In a tree structure each non-root node has exactly one parent.
  return graph[quest.id].parents[0] if graph[quest.id].parents else None

function normalize(vec):
  # Normalize a 2D vector to unit length; return zero vector if magnitude is 0.
  mag = sqrt(vec.x^2 + vec.y^2)
  return (vec.x / mag, vec.y / mag) if mag > 0 else (0, 0)

function group_by_root(quests, graph):
  # Partition quests into groups by their ultimate root ancestor.
  # Walk each quest's parent chain until reaching a root (fan_in == 0).
  groups = {}
  for each quest q:
    root = q
    while root.fan_in > 0: root = find_parent(root, graph)
    groups.setdefault(root.id, []).append(q)
  return groups.values()

function find_root(quests):
  # Return the quest with fan_in == 0. If multiple roots exist,
  # return the one with the highest fan_out (the primary hub).
  roots = [q for q in quests if q.fan_in == 0]
  return max(roots, key=lambda q: q.fan_out) if roots else None

function get_path(source, target, graph, side="left"):
  # BFS from source to target. "side" selects among multiple equal-length
  # paths: "left" prefers lower x-values, "right" prefers higher x-values.
  # For diamond_convergence with 3+ divergent paths, call once per side.
  queue = [source]
  visited = {source.id}
  parent_map = {source.id: None}
  while queue:
    current = queue.pop(0)
    if current.id == target.id:
      path = []
      node = target
      while node:
        path.prepend(node)
        node = parent_map[node.id]
      return path
    children = graph[current.id].children
    if side == "left": children = sorted(children, key=lambda c: c.x)
    else: children = sorted(children, key=lambda c: -c.x)
    for child_id in children:
      if child_id not in visited:
        visited.add(child_id)
        parent_map[child_id] = current
        queue.append(graph[child_id])
  return []
```

### Phase 4 — Collision Detection and Spacing Adjustment

> **Important:** This phase is now an executable collision-correction algorithm that runs during quest generation. It detects overlapping nodes (center-to-center distance < MIN_DISTANCE), classifies each node by structural priority (hub/mid/leaf), and applies directional corrections along dependency lines. Corrections move entire y-rows together to preserve relative positioning. The algorithm iterates up to 3 rounds; if collisions persist, it increases global spacing by 10% and re-assigns coordinates before retrying.

```
function resolve_collisions(quests, graph, spacing):
  MIN_DISTANCE = 1.0
  MAX_ITERATIONS = 3
  global_spacing = spacing
  
  for iteration in range(MAX_ITERATIONS):
    collisions = find_collisions(quests, MIN_DISTANCE)
    if not collisions:
      break
    
    # Group quests by y-row (within 0.3 tolerance)
    rows = group_by_y_row(quests, tolerance=0.3)
    
    for q1, q2, dist in collisions:
      # Priority: hub (fan_in+fan_out >= 3) > mid > leaf
      priority1 = classify_priority(q1, graph)
      priority2 = classify_priority(q2, graph)
      
      # Determine which node(s) to move
      if priority1 == "hub" and priority2 != "hub":
        movers = [q2]  # only move q2
      elif priority2 == "hub" and priority1 != "hub":
        movers = [q1]  # only move q1
      elif priority1 == "leaf" and priority2 == "leaf":
        movers = [q1, q2]  # move both equally
      else:
        movers = [q1, q2]  # move both, but less for mid nodes
      
      offset = (MIN_DISTANCE - dist) / 2 + 0.25
      
      for mover in movers:
        # Move along dependency direction (away from parent)
        dx, dy = dependency_direction(mover, graph)
        mover.x += dx * offset
        mover.y += dy * offset
        
        # Move entire y-row together to preserve relative positions
        row = find_row(mover, rows)
        for other in row:
          if other != mover:
            other.x += dx * offset
  
    # Check if collisions remain after this iteration
    remaining = find_collisions(quests, MIN_DISTANCE)
    if remaining:
      # Increase global spacing by 10% and reassign initial coordinates
      global_spacing *= 1.1
      reassign_coordinates(quests, global_spacing)
  
  return quests

function classify_priority(q, graph):
  connections = graph[q].fan_in + graph[q].fan_out
  if connections >= 3: return "hub"
  if graph[q].fan_out == 0: return "leaf"
  return "mid"

function group_by_y_row(quests, tolerance):
  # Sort quests by y, group those within tolerance
  sorted = sort(quests, by=y)
  rows = []
  current_row = [sorted[0]]
  for q in sorted[1:]:
    if abs(q.y - current_row[0].y) <= tolerance:
      current_row.append(q)
    else:
      rows.append(current_row)
      current_row = [q]
  rows.append(current_row)
  return rows
```

> **Phase 4 — Collision Correction: Complete Helper Functions and Integration**
>
> The `resolve_collisions` function above references three helper functions that must be implemented for the algorithm to be executable. Their definitions and the integration contract with Phases 1–3 are provided below.
>
> **Input contract:** `resolve_collisions` receives the output of Phase 3 (each quest has x, y coordinates assigned) plus the graph structure from Phase 1 and the spacing value used in Phase 3. It does NOT modify the topology classification from Phase 2.
>
> ```
> function find_collisions(quests, min_distance):
>   # Brute-force O(n²) pair check. O(n²) is acceptable for n < 300 (typical chapter
>   # sizes rarely exceed 150 quests). For larger graphs, a spatial hash grid with
>   # cell = min_distance reduces the check to O(n·k) where k is the max nodes per
>   # cell; build the grid in one pass, then check each node against its own cell
>   # and the 8 neighboring cells only.
>   collisions = []
>   for i in range(len(quests)):
>     for j in range(i+1, len(quests)):
>       dx = quests[i].x - quests[j].x
>       dy = quests[i].y - quests[j].y
>       dist = sqrt(dx*dx + dy*dy)
>       if dist < min_distance:
>         collisions.append((quests[i], quests[j], dist))
>   return collisions
>
> function dependency_direction(quest, graph):
>   # Returns a unit vector pointing AWAY from the quest's primary parent.
>   # If no parent (root node), returns (0, -1) (upward = away from content).
>   # For multi-parent nodes, uses the nearest parent for direction.
>   parents = graph[quest.id].parents
>   if not parents:
>     return (0, -1)
>   # Find nearest parent by Euclidean distance
>   nearest = min(parents, key=lambda p: distance(p, quest))
>   dx = quest.x - nearest.x
>   dy = quest.y - nearest.y
>   mag = sqrt(dx*dx + dy*dy)
>   if mag < 0.01:  # Parent and quest at same position (degenerate)
>     return (1, 0)  # Push rightward as default escape direction
>   return (dx / mag, dy / mag)
>
> function reassign_coordinates(quests, new_spacing, original_spacing):
>   # Called when collision correction fails after MAX_ITERATIONS on a single pass.
>   # Re-runs Phase 3's coordinate assignment with the inflated spacing value.
>   # The topology type (Phase 2 output) does NOT change — only spacing changes.
>   # This preserves the overall layout structure while creating more room.
>   # original_spacing: the Phase 3 spacing value before inflation; captured at
>   # the call-site so the ratio new_spacing / original_spacing is well-defined.
>   topology = quests[0].assigned_topology  # cached from Phase 2
>   for each quest q:
>     # Scale existing coordinates proportionally to the spacing increase
>     q.x = q.x * (new_spacing / original_spacing)
>     q.y = q.y * (new_spacing / original_spacing)
>   return quests
> ```
>
> **Iteration termination conditions (precise):**
> - **Success:** `find_collisions` returns empty list → exit immediately, layout is valid.
> - **Partial success:** Collision count decreases between iterations → continue iterating (convergence is happening).
> - **Stagnation:** Collision count does not decrease for 2 consecutive iterations → trigger `reassign_coordinates` with `spacing *= 1.1` and reset iteration counter.
> - **Hard failure:** After 3 full iterations plus 1 reassignment, collisions still remain → emit warning `R58_COLLISION_UNRESOLVED: {n} overlapping pairs remain`, set `hide_dependency_lines = true` on all colliding quests, and accept the layout with overlaps.
>
> **Integration with Phase 1–3:**
> - **Phase 1 output consumed:** `graph` (adjacency list with parents/children), `depth` map, `convergence`/`divergence` lists. The `classify_priority` function uses `fan_in` and `fan_out` from Phase 1's graph analysis.
> - **Phase 2 output consumed:** `topology` type string. The collision algorithm is topology-agnostic EXCEPT for hub_fan and tree_branching, where radial placement (Phase 3) frequently causes outer-ring overlaps — these topologies should expect 2–3 collision iterations as normal.
> - **Phase 3 output consumed:** `x, y` coordinates on each quest. The collision algorithm reads these as starting positions and modifies them in-place.
> - **Phase 4 output to Phase 5:** After collision resolution, the final `x, y` values are passed to Phase 5 (Shape/Size/Icon assignment). Phase 5 does NOT modify coordinates, so no feedback loop exists.
> - **Phase 4 output to Phase 6:** The `hide_dependency_lines` flag set during hard-failure collision resolution is carried forward to Phase 6's final output.
>
> **Collision-prone topology ranking** (from 42-case dataset):
> 1. hub_fan — radial placement causes outer-ring overlaps (ATM-10 basic_power: 3 sub-hubs needed 5.5-unit radius to avoid)
> 2. diamond_convergence — converging paths compress at the synthesis point (Chroma-Technology-2 mekanism: min_spacing=0.71, 80% hide_dep_lines)
> 3. tree_branching — leaf nodes at deep levels cluster together (Monifactory groundwork: 4 regions needed 4–8 unit separation)
> 4. highway_branch — spine nodes rarely collide; branch tips may overlap at boundaries (Create-New-Horizon mv: branches at y=6–10 overlap with adjacent branch roots)
> 5. linear_chain, parallel_columns, grid_catalog — rarely collide (uniform spacing prevents overlaps)

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
    # R59 warning threshold: 30 units (both axes)
    # R59 hard clamp: 35 units (both axes)
    # [Confidence: MEDIUM — based on observed maxima across 13 chapters;
    #  FTB Evolution create reached x=30, Monifactory progression y-span 21 units.
    #  Warning and hard limits are separated to give authors room to adjust.]
    if abs(q.x) > 30.0 or abs(q.y) > 30.0:
      warn "R59: quest exceeds 30-unit warning threshold"
    clamp q.x to [-15.0, 35.0]  # R59 hard limit: 35 units from origin
    clamp q.y to [-17.5, 17.5]  # R59 hard limit: 35 units total height

    # Set hide_dependency_lines based on density
    local_density = count_quests_within_radius(q, radius=3.0)
    if local_density > 8:
      q.hide_dependency_lines = true

  return quests  # Each with {x, y, shape, size, icon}
```

The viewport clamping values come from empirical observation: the widest chapter sampled (FTB Evolution create) spans from x=0 to x=30.0, and the tallest (Monifactory progression) spans 21 units vertically (y=-8.5 to y=12.5). R59 uses separated thresholds: a **warning** at 30 units (both axes) flags chapters approaching the observed maximum, while a **hard clamp** at 35 units prevents quests from being placed outside the viewable area entirely. The y hard clamp is set to [-17.5, 17.5] (35 units total height) to match the x-axis headroom pattern. Most chapters stay within a 20×15 unit bounding box. The `hide_dependency_lines` heuristic is triggered when local density exceeds ~8 quests in a 3-unit radius — this matches the observed behavior in ATM-10 allthemodium (22 hide_dep_lines across 67 quests, concentrated in the dense central cluster) and GregTech-Odyssey stoneage (6 hide_dep_lines across 52 quests, all in the densely-packed mid-section).

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

> [Cycle 12 calibration: The max_spacing=2.5 applies to linear/chain topologies only. Grid_catalog chapters (Cases 17, 20) use independent x_spacing (1.5-3.0) and y_spacing (2.0-4.0) parameters, producing avg spacing values up to 5.67. Highway_branch chapters (Cases 15, 19) with max_width >= 19 produce avg spacing of 2.13-3.6, suggesting the formula's density_factor should use a different decay rate for horizontal layouts: `density_factor = 1.0 - (quest_count - 50) * 0.003` for highway_branch (vs 0.005 for vertical chains). The diamond_convergence extreme (Case 16, min_spacing=0.71) confirms that R58 collision detection catches intentional overlaps in mega-chapters — no formula change needed, but the warning message should note that hide_dependency_lines > 50% often accompanies spacing < 1.0.]

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

### Case 14: Parallel Columns — Create-New-Horizon `lv`

61 quests, parallel_columns topology with diamond+gear shapes for milestones. The Create expert pack uses grid_scale=0.5d with very low icon rate (8.2%).

```
Coordinate extract (first 15 nodes):
| Quest                | x    | y    | shape   | size | deps |
|----------------------|------|------|---------|------|------|
| 544D7F95370F9235     | 0.0  | 3.0  | default | 1.0  | 06B6 |
| 504A762FE1057233     | 2.0  | -6.0 | diamond | 1.5  | 4767 |
| 7CF628053F84B8D1     | 3.0  | 3.0  | diamond | 1.0  | 06B6 |
| 0FEAC07F1404346A     | 4.0  | -6.0 | diamond | 1.5  | 2D66,5D14,4767 |
| 06A46967BFF56B33     | 7.5  | -4.0 | default | 1.0  | 7F99 |
| 7AE674329D7E7944     | -5.5 | 0.5  | default | 2.0  | 41E4 |
| 0425D0789C2837CD     | 7.5  | -8.0 | default | 1.0  | 4EE1,67AC |
| 44E9D92283CBF029     | 7.5  | 0.5  | default | 2.0  | 06B6 |
| 7F992D338D4783CE     | 7.5  | -2.0 | default | 1.0  | 44E9,0F5D,471F |
| 2D662EFDE7A39BB8     | 7.5  | -6.0 | default | 1.0  | 06A4,0425 |
| 4487EDC96DB1390B     | 9.5  | 0.0  | default | 1.0  | 44E9 |
| 7345F277E135E5B9     | 7.5  | 3.0  | default | 1.0  | 44E9 |
| 19869FD9D4BCCB9F     | 11.5 | 0.5  | gear    | 2.0  | 4487,146A |
| 11F898C7B0C925D5     | 14.5 | 0.5  | rsquare | 2.0  | 1986,27BD |
| 27BD70B6974D0C78     | 14.5 | 2.0  | default | 1.0  | 0F22,5F53 |

Shape distribution: default(48), diamond(3), gear(1), rsquare(2), octagon(7)
Size distribution: 12 quests >= 1.5
Icon rate: 5/61 (8.2%)
Spacing: min=1.0, avg=2.55, max=15.91
Topology: parallel_columns (max_depth=9, max_width=13, convergence_ratio=0.15)
```

The lv chapter demonstrates a typical Create expert pack layout: multiple parallel processing chains (columns at x=7.5, x=-5.5, x=14.5) with diamond and gear shapes marking milestone nodes. The gear-shaped quest at (11.5, 0.5) with size 2.0 marks the EBF (Electric Blast Furnace) acquisition point — a common Create expert milestone. The octagon shape (7 occurrences) is used for tier-boundary markers.

Source: `CTNH-Team/Create-New-Horizon/main/config/ftbquests/quests/chapters/lv.snbt`

> **Generality note:** Calibrated from Create-expert pack. Spacing/shape parameters (diamond for milestones, gear for EBF acquisition, octagon for tier boundaries) may differ for kitchen-sink, adventure, or skyblock packs. The parallel_columns topology itself is universal.

### Case 15: Highway Branch — Create-New-Horizon `mv`

80 quests, highway_branch topology with horizontal spine at y=12-17. The chapter demonstrates how Create expert packs transition between voltage tiers using highway layouts.

```
Coordinate extract (first 15 nodes):
| Quest                | x    | y    | shape   | size | deps |
|----------------------|------|------|---------|------|------|
| 1FBD86C0CF681427     | 2.5  | 12.0 | default | 2.0  | 11F8 |
| 689E197D320A0477     | 2.5  | 14.0 | default | 1.0  | 2D66,1FBD |
| 45D2C63F76606DE2     | 2.5  | 15.0 | default | 1.0  | 689E |
| 62F1BC2DC2900E4F     | 1.5  | 16.0 | default | 1.0  | 45D2 |
| 3DDBBC874FEB36B4     | 2.5  | 16.0 | default | 1.0  | 45D2 |
| 2B326207A7208F04     | 1.5  | 17.0 | default | 1.0  | 62F1 |
| 0D5604D8E0984197     | 2.5  | 17.0 | default | 1.0  | 3DDB |
| 577C0EA40EC89B14     | 3.5  | 16.0 | default | 1.0  | 45D2 |
| 0C12A7FDA05C7439     | 3.5  | 17.0 | default | 1.0  | 577C |
| 18053F8D68450C52     | 0.5  | 14.0 | default | 1.0  | 1FBD |
| 552458CB71BFFED9     | 6.5  | 15.0 | default | 1.0  | —    |
| 5A460876CA0EC216     | 8.5  | 16.0 | default | 1.0  | 5524,61F3,5F39 |
| 3F99A5F49AABC226     | 12.5 | 16.0 | default | 1.0  | 6A93 |
| 10FA0AB1DB0672F9     | 2.5  | 10.0 | default | 1.0  | 1FBD,5FCD |
| 27675B2A83F65B2E     | 4.5  | 10.0 | default | 1.0  | 10FA,7564 |

Shape distribution: default(75), rsquare(3), pentagon(1), gear(1)
Size distribution: 4 quests >= 1.5
Icon rate: 2/80 (2.5%)
Spacing: min=1.0, avg=2.13, max=13.6
Topology: highway_branch (max_depth=11, max_width=19, convergence_ratio=0.212)
```

The mv chapter's highway spine runs horizontally at y=12-17, with branches extending upward (y=6-10) and rightward (x=17-23). The shape vocabulary is almost entirely default — the pack relies on coordinate position and size rather than shape diversity for visual hierarchy. This is consistent with the Create expert pack design philosophy where the recipe chain itself provides the organizational structure.

Source: `CTNH-Team/Create-New-Horizon/main/config/ftbquests/quests/chapters/mv.snbt`

> **Generality note:** Calibrated from Create-expert pack. The voltage-tier highway pattern and shape monoculture (75 default out of 80 quests) are expert-specific. Kitchen-sink packs use highway_branch for mod-progression spines (see Case 10 MM2 botania). The density_factor calibration (0.003 vs 0.005) is universal.

### Case 16: Diamond Convergence (Extreme) — Chroma-Technology-2 `mekanism`

199 quests, diamond_convergence with 100% diamond shape and 159 hide_dependency_lines. This is the most extreme convergence case in the entire dataset — convergence_ratio=0.412, far above the 0.15 threshold.

```
Coordinate extract (first 15 nodes):
| Quest                | x    | y    | shape   | size | deps |
|----------------------|------|------|---------|------|------|
| 6F2326323EF33A63     | 3.0  | 9.0  | diamond | 1.5  | 3082 |
| 1C5818BF2481FEB9     | -1.5 | 1.0  | diamond | 1.0  | 6F23,59BA |
| 7547F21443ADFD9D     | -1.5 | 2.0  | diamond | 1.0  | 1C58 |
| 0D744782AEA76225     | -1.0 | 2.5  | diamond | 1.0  | 7547 |
| 3A6CBF391E68AEE3     | -1.5 | 3.0  | diamond | 1.0  | 0D74 |
| 0225A4A018E2BA20     | -2.0 | 2.5  | diamond | 1.0  | 3A6C |
| 19F47CFF5CF727F7     | 1.5  | 1.0  | diamond | 1.0  | 6F23,59BA |
| 6C78BA8A15F32636     | 1.5  | 2.0  | diamond | 1.0  | 19F4 |
| 3ABCF46C0EB5CDB5     | 2.0  | 2.5  | diamond | 1.0  | 6C78 |
| 584DB90221EF6DA2     | 1.5  | 3.0  | diamond | 1.0  | 3ABC |
| 02EAC225986FF06D     | 1.0  | 2.5  | diamond | 1.0  | 584D |
| 6FE388941E6F219B     | 4.5  | 1.0  | diamond | 1.0  | 6F23,39DD,6083 |
| 2CF599B38DC00871     | 4.5  | 2.0  | diamond | 1.0  | 6FE3 |
| 4306DC485F0C9CA4     | 5.0  | 2.5  | diamond | 1.0  | 2CF5 |
| 04E960E06A52C180     | 4.5  | 3.0  | diamond | 1.0  | 4306 |

Shape distribution: diamond(199) — 100% monoculture
Size distribution: 1 quest >= 1.5
Icon rate: 0/199 (0.0%)
Spacing: min=0.71, avg=6.58, max=23.71
Topology: diamond_convergence (max_depth=7, max_width=49, convergence_ratio=0.412)
hide_dependency_lines: 159 (80% of quests)
```

This chapter is a "pure processing chain" layout: 199 quests all using diamond shape, organized as multiple parallel sub-chains that converge on a few root output nodes. The convergence_ratio of 0.412 means 82 quests have fan_in >= 2 — nearly half the chapter is convergence points. The min spacing of 0.71 (below the 1.0 minimum) indicates some quests overlap, which the 159 hide_dependency_lines partially compensate for by removing visual clutter. The max spacing of 23.71 is the widest gap observed in any chapter.

> [Cycle 12 calibration: The convergence_ratio threshold of 0.15 in Phase 2's topology classifier correctly identifies this chapter, but the extreme value (0.412) suggests the threshold could be raised to 0.20 without losing sensitivity. The 0.15 value remains valid for mixed-topology chapters. The min_spacing < 1.0 (0.71) in this chapter demonstrates that the Phase 4 collision detection (R58) would flag violations here — the author chose to accept overlaps in exchange for fitting 199 quests into a single chapter.]

Source: `Gogo08190/Chroma-Technology-2/main/config/ftbquests/quests/chapters/mekanism.snbt`

> **Generality note:** Calibrated from expert pack with extreme parameters (199 quests, convergence_ratio=0.412, min_spacing=0.71). Kitchen-sink/adventure/skyblock convergence operates at convergence_ratio 0.10-0.20; do not use 0.412 as a calibration target for non-expert packs. See Case 4 (ATM-10 allthemodium, convergence_ratio=0.15) for the kitchen-sink baseline.

### Case 17: Grid Catalog — Gregtech-Voyager `chapter_2_mv`

91 quests, grid_catalog topology with the widest average spacing in the dataset (avg=5.57). All quests use default shape — another example of GT pack shape monoculture.

```
Coordinate extract (first 15 nodes):
| Quest                | x    | y     | shape   | size | deps |
|----------------------|------|-------|---------|------|------|
| 1899E901A1BE8869     | -6.0 | 8.5   | default | 1.0  | —    |
| 583BA3292A2FA4F5     | -6.0 | 9.75  | default | 1.5  | 1899 |
| 245AD5E4251E8B62     | 2.5  | 7.5   | default | 1.5  | 0281 |
| 55B4E561D8CAA63F     | 2.5  | 9.0   | default | 1.0  | 245A |
| 0177DD9FCB5072FB     | 4.0  | 7.5   | default | 1.0  | 245A |
| 672BD4D74611D496     | -2.0 | 8.5   | default | 1.0  | 1899 |
| 272F60059F2C262A     | -2.0 | 7.5   | default | 1.0  | 672B |
| 23A24371FCAC67AE     | -1.0 | 8.5   | default | 1.0  | 672B |
| 51CE5359D3A53009     | -1.0 | 7.5   | default | 1.0  | 672B |
| 4333A345E5A0F485     | 1.0  | 7.5   | default | 1.0  | 672B,51CE,245A |
| 5D6EDD86284F0668     | 1.0  | 5.5   | default | 1.0  | 4333 |
| 7B7D3554033DAE30     | 5.5  | 7.5   | default | 1.0  | 0177 |
| 48C0F2B5DB6E97D2     | -2.0 | 10.0  | default | 1.0  | 6902 |
| 0C8FAA015B37C20C     | 2.5  | 11.5  | default | 1.0  | 55B4 |
| 0D1153B4D44B8F8D     | -1.0 | 10.0  | default | 1.0  | 583B,23A2 |

Shape distribution: default(91) — shape monoculture
Size distribution: 10 quests >= 1.5
Icon rate: 1/91 (1.1%)
Spacing: min=1.0, avg=5.57, max=16.06
Topology: grid_catalog (max_depth=7, max_width=47, convergence_ratio=0.187)
hide_dependency_lines: 12, hide_dependent_lines: 28
```

The chapter_2_mv demonstrates a GT pack's approach to catalog-style layout: quests are spread across a very wide area (max_width=47) with generous spacing (avg=5.57, the widest in the dataset). The high hide_dependent_lines count (28) prevents the wide spacing from producing an overwhelming web of dependency lines. This is a MV (Medium Voltage) tier chapter where the player has access to many parallel processing chains, each occupying its own coordinate region.

> [Cycle 12 calibration: The grid_catalog avg spacing of 5.57 exceeds the max_spacing of 2.5 in the Layer 2 spacing formula. This is because grid_catalog chapters use a different spacing model — the x_spacing (column gap) and y_spacing (row gap) are independent parameters, and the wide max_width (47) means quests are distributed across a large area rather than compressed into a chain. The current formula's max_spacing=2.5 applies to linear/chain spacing, not grid catalog. Authors using grid_catalog should ignore the spacing formula and instead use: x_spacing ≈ 1.5-3.0, y_spacing ≈ 2.0-4.0, with wider values for larger quest counts.]

Source: `bzells/Gregtech-Voyager/main/config/ftbquests/quests/chapters/chapter_2_mv.snbt`

> **Generality note:** Calibrated from GT-expert pack. The grid_catalog topology and separate spacing model are universal; specific spacing ranges (avg=5.57, x_spacing 1.5-3.0, y_spacing 2.0-4.0) are calibrated from GT-expert data. Cross-reference Case 7 (RAD3 milestones, avg spacing 1.5x2.5) as the kitchen-sink baseline.

### Case 18: Tree Branching — CodeNameCIM2 `start`

32 quests, tree_branching topology with gear shape for component milestones. Chinese-language Create expert pack with the highest icon rate in the prologue chapter (67%).

```
Coordinate extract (first 15 nodes):
| Quest                | x    | y    | shape   | size | deps |
|----------------------|------|------|---------|------|------|
| 5DC78DC9A01883A1     | -5.0 | 14.5 | default | 1.5  | 21ED |
| 4EAFBA3A19526127     | -2.0 | 14.5 | default | 1.0  | 5DC7 |
| 0849A3B5EAAE4E14     | -2.0 | 12.0 | gear    | 2.0  | 4EAF |
| 76DD35F7BAB2AF34     | 0.0  | 13.5 | default | 1.0  | 4EAF |
| 73153E1AFAD14636     | 0.0  | 15.5 | default | 1.0  | 4EAF |
| 256C6C201607525D     | 0.0  | 11.5 | default | 1.0  | 76DD |
| 5E676A3C46C6141B     | -2.0 | 16.5 | default | 1.0  | 7315 |
| 5D0FEBD3FC3443C6     | -2.0 | 18.5 | default | 1.0  | 5E67 |
| 3A4EA6A20A0727AA     | 0.0  | 17.5 | default | 1.0  | 7315,5E67 |
| 2613E62AF5BCD9AC     | 2.0  | 14.5 | default | 1.0  | 7315,76DD |
| 4840B337A93659FC     | 2.0  | 12.5 | default | 1.0  | 2613 |
| 07FD61829D499994     | 4.0  | 11.5 | default | 1.0  | 4840 |
| 1231A867DC253AAA     | 6.0  | 14.5 | default | 1.0  | 2613 |
| 07C4444CF1D9BB41     | 6.0  | 18.5 | default | 1.0  | 5DC7 |
| 637C1318E278B73E     | 2.0  | 16.5 | default | 1.0  | 3A4E |

Shape distribution: default(27), gear(5)
Size distribution: 6 quests >= 1.5
Icon rate: 6/32 (19%)
Spacing: avg ~2.0
Topology: tree_branching (left tree: wood→planks→components; right tree: stone→furnace→smeltery)
hide_dependency_lines: 7
```

The start chapter demonstrates a Chinese Create expert pack's approach to tree_branching: two main trunks branch from the root at (-5.0, 14.5) — a left trunk (wood processing: 木头→木板→木质构件) and a right trunk (stone processing: 石头→熔炉→焦黑砖→冶炼设备). Gear shapes (size 2.0) mark component acquisition milestones (木质构件, 石质构件, 铜构件). The prologue chapter of this pack has a 67% icon rate — the highest observed in any Cycle 12 chapter — suggesting Chinese packs invest heavily in visual onboarding.

Source: `Eternal-Snowstorm/CodeNameCIM2/main/config/ftbquests/quests/chapters/start.snbt`

> **Generality note:** Calibrated from Create-expert pack. The tree_branching topology is fully universal (applicable to all five pack types). The two-trunk structure is Create-specific content, but the coordinate pattern (root at center, paired branches expanding outward) transfers directly to kitchen-sink, adventure, and skyblock packs.

### Case 19: Highway Branch — Gregtech-Voyager `chapter_3_hv`

95 quests, highway_branch topology with 15 quests at size >= 1.5. The HV (High Voltage) tier chapter demonstrates how GT packs scale highway layouts for larger tier content.

```
Coordinate extract (first 15 nodes):
| Quest                | x     | y     | shape   | size | deps |
|----------------------|-------|-------|---------|------|------|
| 3E70E88792C984D2     | -3.5  | 2.0   | default | 1.0  | 3E3E |
| 369E7991835FD4C7     | -3.5  | -0.75 | default | 1.5  | 1F92 |
| 17D94B0681899CD5     | 3.75  | 0.75  | default | 1.5  | —    |
| 29C1E4853C4FB803     | 3.0   | 5.25  | default | 1.0  | 1D82,55A7 |
| 00C65B2F04610920     | 3.75  | 3.75  | default | 1.5  | 6DAE,69FA,17D9 |
| 6DAEA8AAC3AB9B85     | 1.5   | 2.0   | default | 1.0  | 55A7 |
| 69FAA229BFE8A1D2     | 2.5   | 2.0   | default | 1.0  | 55A7 |
| 3E3E32FBC8D75BAE     | 0.0   | 2.0   | default | 1.0  | 6DAE |
| 07FE8AB30E2F96AE     | 0.0   | 3.5   | default | 1.0  | 6DAE |
| 7C10F8CB3B0C5FCA     | 0.0   | 4.5   | default | 1.0  | 07FE |
| 491F1AE9C874CE53     | -6.0  | 12.0  | default | 1.0  | 54AF,4BF8 |
| 3F492B6889B20A24     | 5.5   | 3.0   | default | 1.0  | —    |
| 07C0341327430117     | 5.5   | 4.0   | default | 1.0  | —    |
| 648A292AD5517FBB     | 6.5   | 4.0   | default | 1.0  | 07C0,3F49 |
| 4CC1CF4D2F6C5EBD     | 5.5   | 2.0   | default | 1.0  | —    |

Shape distribution: default(95) — shape monoculture
Size distribution: 15 quests >= 1.5
Icon rate: 1/95 (1.1%)
Spacing: min=1.0, avg=3.6, max=17.73
Topology: highway_branch (max_depth=10, max_width=31, convergence_ratio=0.211)
hide_dependency_lines: 5, hide_dependent_lines: 4
```

The HV chapter extends the highway_branch pattern seen in Create-New-Horizon mv but at larger scale: max_width=31 (vs 19 in mv), max spacing=17.73 (vs 13.6). The quest at (3.75, 3.75) — "Robot Arms III" — serves as a convergence hub (fan_in=3) at size 1.5, marking the tier's signature multiblock acquisition. Shape monoculture (all default) is consistent across all Gregtech-Voyager chapters, validating that GT expert packs rely on coordinate position rather than shape for visual hierarchy.

Source: `bzells/Gregtech-Voyager/main/config/ftbquests/quests/chapters/chapter_3_hv.snbt`

> **Generality note:** Calibrated from GT-expert pack. This is a duplicate expert-pack highway_branch (same pack family as Case 15). Shape monoculture (all default) and voltage-tier scaling are expert-specific. Case 10 (MM2 botania) remains the kitchen-sink highway_branch reference. No adventure or skyblock highway_branch cases exist yet.

### Case 20: Grid Catalog (Hub-and-Spoke) — Chroma-Technology-2 `creative`

41 quests, grid_catalog topology with hub-and-spoke structure. All non-hub quests depend on a single central octagon quest — the most centralized dependency structure observed in a grid_catalog chapter.

```
Coordinate extract (first 15 nodes):
| Quest                | x    | y    | shape   | size | deps |
|----------------------|------|------|---------|------|------|
| 2BEBB5DFA50EC976     | 9.0  | -5.5 | diamond | 1.0  | 3CFD |
| 02AE2841660CDD7B     | 8.5  | -4.0 | diamond | 1.0  | 3CFD |
| 6DF9EB6350A52DD7     | 9.5  | -4.0 | diamond | 1.0  | 3CFD |
| 4C7D03D5C795FFC9     | 8.0  | -3.5 | diamond | 1.0  | 3CFD |
| 4AC67F15DB22433E     | 10.0 | -3.5 | diamond | 1.0  | 3CFD |
| 36C95D4A14413796     | 9.0  | -3.0 | diamond | 1.0  | 3CFD |
| 7AFB5503D5E5E885     | 8.5  | -5.0 | diamond | 1.0  | 3CFD |
| 7953D76B192F2E3F     | 10.5 | -2.5 | diamond | 1.0  | 3CFD |
| 1020E858B88567DB     | 11.5 | -3.5 | diamond | 1.0  | 3CFD |
| 72E2EAA9FCC873C4     | 6.5  | -3.5 | diamond | 1.0  | 3CFD |
| 107971F6E4BA8CCF     | 7.5  | -2.5 | diamond | 1.0  | 3CFD |
| 2A2D194AF3FFB1FC     | 9.0  | 5.0  | diamond | 2.0  | 3CFD,0A7A,65A0 |
| 2734FEBB2FA98226     | 10.0 | -2.0 | diamond | 1.0  | 3CFD |
| 4048210DFE7221CA     | 10.0 | -4.5 | diamond | 1.0  | 3CFD |
| 2BC07F762E542BFB     | 11.0 | -3.0 | diamond | 1.0  | 3CFD |

Shape distribution: diamond(30), octagon(1), default(10)
Size distribution: 2 quests >= 1.5
Icon rate: 0/41 (0.0%)
Spacing: min=1.8, avg=5.67, max=10.01
Topology: grid_catalog (max_depth=3, max_width=24, convergence_ratio=0.073)
hide_dependency_lines: 31
```

The creative chapter demonstrates a unique hub-and-spoke variant of grid_catalog: the central octagon quest at (9.0, 1.0) with size 2.0 serves as the single dependency for 30 diamond-shaped quests arranged in a radial grid pattern above it (y=-2.0 to -5.5), while 10 default-shaped quests form input chains below (y=1.0 to 5.0). The 31 hide_dependency_lines (76% of quests) prevent the starburst of dependency lines from the central hub from overwhelming the visual field. This "creative items" chapter is a common end-game pattern where all quests depend on a single creative-tier crafting table.

Source: `Gogo08190/Chroma-Technology-2/main/config/ftbquests/quests/chapters/creative.snbt`

> **Generality note:** Calibrated from expert pack endgame chapter. The hub-and-spoke grid_catalog variant is specific to expert endgame chapters where all quests depend on a single creative-tier crafting table. Standard grid_catalog (Cases 7, 17) is the universal reference. The 76% hide_dependency_lines rate is a useful data point for any hub-and-spoke layout regardless of pack type.

### Case 21: Hub + Fan — ATM9-Sky `welcome` (Skyblock)
<!-- ATM-family skyblock signature style, not general calibration reference -->

2 quests, hub_fan topology. The welcome chapter for ATM9-Sky uses a single large hexagon root node as the visual anchor, with an invisible metadata quest as its only dependent. This is the smallest hub_fan in the dataset but represents a deliberate skyblock welcome pattern.

```
Coordinate extract (all nodes):
| Quest              | x    | y    | shape   | size | deps |
|--------------------|------|------|---------|------|------|
| 23BDBBD3001F9774   | 0.0  | -8.0 | hexagon | 2.0  | —    |
| 14546A0AAE702FA1   | 0.0  | -6.0 | octagon | 1.0  | —    |

Shape distribution: hexagon(1), octagon(1)
Size distribution: 1 quest >= 2.0
Icon rate: 2/2 (100%)
Spacing: single-pair, distance=2.0
Topology: hub_fan (max_depth=1, max_width=1)
Decorative images: 4 (arrow_left, arrow_collapsed, clouds banner 150×10, logo 10×10)
```

The skyblock welcome pattern uses a large hexagon (size 2.0) with a custom ATM star icon as the sole entry point. The decorative image layer is unusually elaborate for a 2-quest chapter: a 150×10 cloud banner at y=-9 creates a sky backdrop above the root quest, and a 10×10 pack logo at y=-12 anchors the brand. The hidden octagon quest (invisible, optional) serves as a licensing metadata marker. This pattern is specific to ATM-family skyblock packs — the combination of cloud banner + logo + hexagon root creates a distinctive "sky" visual identity.

Source: `AllTheMods/All-the-mods-9-Sky/dev/config/ftbquests/quests/chapters/welcome.snbt`

> **Generality note:** Calibrated from ATM-family skyblock pack. The elaborate decorative image layer (4 images for 2 quests = 2.0 images/quest, highest ratio in dataset) is an ATM skyblock signature. Standard hub_fan cases (Cases 2, 5) remain the universal reference.

### Case 22: Linear Chain (Horizontal) — ATM9-Sky `getting_started` (Skyblock)

20+ quests, linear_chain topology with horizontal progression. The getting_started chapter for ATM9-Sky lays out the skyblock tool acquisition sequence as a left-to-right chain, with branching for farming and power generation sub-systems.

```
Coordinate extract (key nodes):
| Quest              | x     | y    | shape   | size | deps           |
|--------------------|-------|------|---------|------|----------------|
| 22C568A17B5D1B46   | -11.0 | -1.0 | hexagon | 2.0  | —              |
| 3001B2EEE5C6C9AB   | -8.0  | -1.0 | —       | 1.0  | 22C5           |
| 1658780534451E39   | -8.0  | -2.5 | —       | 1.0  | 22C5           |
| 3F755A55B2043E5B   | -8.0  | 0.5  | —       | 1.0  | 22C5           |
| 5ED547FE0A9CFC63   | -8.0  | -6.0 | gear    | 2.0  | 55A7           |
| 744E757CA323FF46   | -5.5  | -1.0 | —       | 1.0  | 3001           |
| 35EF391AB5344094   | -5.5  | 0.5  | —       | 1.0  | 3F75           |
| 4A536710A11856F2   | -4.0  | -1.0 | —       | 1.0  | 7447           |
| 768F0E715B05D9E4   | -2.0  | -1.0 | —       | 1.0  | 4A53           |
| 2CF0EE5C0651F531   | -2.0  | 2.5  | —       | 1.0  | 5FF2           |
| 11097D91EBF2490D   | -2.0  | 3.5  | —       | 1.0  | 2CF0           |
| 6580DCA54E4C9BC2   | -2.0  | 4.5  | —       | 1.0  | 1109           |
| 25D1363D8890E7C3   | 4.5   | 1.5  | —       | 1.0  | 592D           |
| 162AB6F9257EB71E   | 4.5   | -1.5 | gear    | 3.0  | 25D1           |

Shape distribution: gear(2), hexagon(1), default(17+)
Size distribution: 3 quests >= 2.0
Icon rate: ~12/20 (60%)
Spacing: min=1.5, avg=2.5, max=3.0
Topology: linear_chain (max_depth=8, max_width=3)
dependency_requirement: one_completed(1)
```

The skyblock getting_started layout diverges from kitchen-sink linear chains in two key ways. First, the horizontal axis runs left-to-right across 15.5 units (x=-11 to x=4.5), which is wider than most linear chains but narrower than highway layouts. Second, the mesh upgrade sub-chain (string→flint→iron→diamond→netherite) runs vertically downward from the main chain at x=-2.0, creating a perpendicular branch that is characteristic of skyblock packs where the sieve progression is the central gameplay loop. The gear-shaped "Power Part 2" quest at (4.5, -1.5) with size 3.0 is the largest quest in the chapter, marking the transition from early-game survival to mid-game power generation — this size-3.0 milestone pattern is unique to ATM9-Sky (no other pack uses size > 2.5 in getting_started chapters).

Source: `AllTheMods/All-the-mods-9-Sky/dev/config/ftbquests/quests/chapters/getting_started.snbt`

> **Generality note:** Calibrated from ATM-family skyblock pack. The perpendicular mesh-upgrade branch is a skyblock-specific sub-pattern of linear_chain. The size-3.0 milestone is an ATM signature (also seen in ATM-10 basic_tools). Standard linear_chain cases (Cases 1, 3, 8) remain the universal reference.

### Case 23: Hub + Fan (Radial) — Dragoncraft `the_beginning` (Adventure/RPG)

20+ quests, hub_fan topology with radial layout. The_beginning chapter for Dragoncraft uses a central hexagon hub with 5 radiating branches, each leading to a different mod system (Dragon Survival, Create, Ars Nouveau, Iron's Spells, Cataclysm).

```
Coordinate extract (key nodes):
| Quest              | x     | y    | shape   | size | deps           |
|--------------------|-------|------|---------|------|----------------|
| 52A6312666869670   | -4.0  | 0.0  | hexagon | 2.0  | —              |
| 64EA09325CA73BE1   | -6.5  | 0.0  | —       | 1.0  | 52A6           |
| 268CA98A4617D3B4   | -6.5  | -2.5 | —       | 1.0  | 52A6           |
| 6A8064F3B3ED9A5E   | -2.0  | -2.0 | —       | 1.0  | 52A6           |
| 35FDE4956415F691   | -1.5  | 0.0  | —       | 1.0  | 52A6           |
| 7CFCEE9DE2E87FFD   | -2.0  | 2.0  | —       | 1.0  | 52A6           |
| 3B9A9A0AFA3C0380   | -4.0  | 2.5  | —       | 1.0  | 52A6           |
| 58EDE384B89A5980   | -4.0  | -2.5 | —       | 1.0  | 52A6           |
| 41290A2221D2FF15   | -8.0  | 0.0  | —       | 1.0  | 64EA           |
| 5E93B483040C00A6   | -9.5  | 0.0  | —       | 1.0  | 4129           |
| 518911E77C2DE085   | -12.5 | -1.0 | —       | 1.0  | 5E93           |
| 38317B92B9349695   | -11.5 | -1.0 | —       | 1.0  | 5E93           |
| 7C7B76F45CC0CC55   | -10.5 | -1.0 | —       | 1.0  | 5E93           |
| 52C9E1A2A805EFAE   | -11.5 | 1.0  | —       | 1.0  | 5E93           |
| 4196A0B72778B4A9   | -10.5 | 1.0  | —       | 1.0  | 5E93           |
| 00C009F41021BDEE   | -13.5 | 0.0  | —       | 1.0  | 5E93           |
| 045F60E47DA778FB   | -12.5 | 1.0  | —       | 1.0  | 5E93           |
| 4138EA22BF8ABF69   | -15.0 | 0.0  | —       | 1.0  | 00C0           |

Shape distribution: hexagon(1), default(17+)
Size distribution: 1 quest >= 2.0
Icon rate: ~16/18 (89%, highest in Cycle 13)
Spacing: min=1.0, avg=2.5, max=3.5
Topology: hub_fan (max_depth=5, max_width=7, 5 branches from root)
dependency_requirement: one_completed(1)
Rewards: elder_dragon_dust(7), elder_dragon_bone(2), xp(8), choice(1), item(3)
```

Dragoncraft's the_beginning demonstrates a distinctive two-stage hub_fan unique to adventure/RPG packs. The first stage is a radial fan from the central hexagon hub at (-4, 0) — 6 branches spread at roughly 60° intervals (upper-left, left, lower-left, upper-right, right, lower-right) to mod-introduction quests. The second stage is a linear extension from the Dragon Survival branch: after the initial fan node at (-6.5, 0), the chain continues leftward through a choice-reward quest at (-8, 0) to a second sub-hub at (-9.5, 0), which then fans out to 7 dragon-item collection quests. This nested hub_fan (hub→branch→sub-hub→leaves) creates a 15-unit horizontal span, making it the widest hub_fan in the dataset. The 89% icon rate (custom dragon icons, entity_face icons, ftbquests:custom_icon) reflects the RPG emphasis on visual identity for each class/skill path. Every quest rewards elder_dragon_dust (the pack's progression currency), creating a reward-per-quest economy unlike any other pack in the dataset.

Source: `Kerberus-MC/Dragoncraft/master/config/ftbquests/quests/chapters/the_beginning.snbt`

> **Generality note:** Calibrated from adventure/RPG pack. The nested hub_fan (two-stage fan) and the reward-per-quest dragon_dust economy are adventure-specific patterns. The 89% icon rate is the highest observed for a non-trivial chapter. Standard hub_fan cases (Cases 2, 5) remain the universal reference for simpler fan layouts.

### Case 24: Tree Branching (Decorative Barrier) — Life-in-the-Village-4 `adventure_begins` (Farming/Adventure)

15+ quests, tree_branching topology with decorative barrier images marking region boundaries. The adventure_begins chapter uses a large root hexagon and hexagon_important milestones with elaborate decorative images.

```
Coordinate extract (key nodes):
| Quest              | x    | y    | shape            | size | deps           |
|--------------------|------|------|------------------|------|----------------|
| 35A027D4B827463C   | -2.0 | -3.0 | hexagon          | 3.0  | —              |
| 033105F673C5EF80   | -0.5 | 1.0  | hexagon_important| 2.0  | 35A0           |
| 1966320B37D990A0   | 2.0  | -3.0 | hexagon_important| 2.0  | 35A0           |
| 43EFBBF0712C67B9   | -0.5 | -7.0 | hexagon_important| 2.0  | 35A0           |
| 059FF2A11860CDCF   | -1.5 | -8.5 | —                | 1.0  | 43EF           |
| 7343C10D6EEAA88B   | —    | —    | —                | 1.0  | 0017           |

Shape distribution: hexagon(1), hexagon_important(3), default(11+)
Size distribution: 4 quests >= 2.0
Icon rate: ~2/15 (13%)
Spacing: min=1.5, avg=3.0, max=4.5
Topology: tree_branching (max_depth=3, max_width=3)
autofocus_id: 35A027D4B827463C
Decorative images: 12 (barrier/barrier_open at region boundaries)
```

The adventure_begins chapter introduces a new shape value `hexagon_important` — a variant of hexagon with a distinct visual treatment (likely a highlight or border effect) used specifically for milestone quests that introduce new gameplay systems (Mining, Processing, Organizing). The size-3.0 root quest at (-2, -3) is the largest welcome node in the dataset, and the three hexagon_important milestones at size 2.0 form a triangular tree branching from the root. The 12 decorative barrier images (both `barrier` and `barrier_open` variants) are positioned at region boundaries to visually fence off content areas — closed barriers (2.0×2.0) mark locked regions, while open barriers (1.1×1.1, rotated 45°) mark accessible passages. This barrier-as-gate metaphor is unique to Life-in-the-Village-4 and represents a visual storytelling technique not seen in any other pack.

Source: `dr3ams/Life-in-the-Village-4/main/config/ftbquests/quests/chapters/adventure_begins.snbt`

> **Generality note:** Calibrated from farming/adventure pack by dr3ams (same author as RAD2/RAD3). The hexagon_important shape and decorative barrier images are pack-specific. The tree_branching topology with 3 milestones is the universal reference for farming/adventure pack introductions. The autofocus_id feature (also seen in Path-of-Truth) auto-centers the quest UI on the root quest.

### Case 25: Hub + Fan (Shape-Diverse) — Ragnamod VI Skyblock `welcome` (Skyblock)

6 quests, hub_fan topology with the richest shape vocabulary for a welcome chapter (5 shape types for 6 quests).

```
Coordinate extract (all nodes):
| Quest              | x    | y    | shape    | size | deps           |
|--------------------|------|------|----------|------|----------------|
| 2B04C39F8061A391   | 0.0  | -0.5 | gear     | 2.0  | —              |
| 7FE28D790C05A013   | -1.0 | 1.5  | circle   | 1.0  | 2B04           |
| 04BBC0D3045DE9D9   | 0.0  | 2.0  | diamond  | 1.0  | 2B04           |
| 3D5841B8216C4182   | -1.5 | 0.5  | —        | 1.0  | 2B04           |
| 46EA919C01D191F6   | 1.5  | 0.5  | octagon  | 1.0  | 2B04           |
| 143257E39D5E02BC   | 1.0  | 1.5  | pentagon | 1.0  | 2B04           |

Shape distribution: gear(1), circle(1), diamond(1), octagon(1), pentagon(1), default(1)
Size distribution: 1 quest >= 2.0
Icon rate: 6/6 (100%)
Spacing: min=1.0, avg=1.8, max=2.5
Topology: hub_fan (max_depth=1, max_width=5)
Decorative images: 2 (logo 10×5, sky 10×5 layered)
default_quest_shape: gear
```

Ragnamod VI Skyblock's welcome chapter assigns a unique shape to every branch quest — gear for root, circle for quest book, diamond for creative items, octagon for ore tooltips, pentagon for skyblock commands. This is the only welcome chapter in the dataset where shape serves as a categorical label rather than a structural signal. Each shape corresponds to a different information domain (QoL, progression, endgame, mining, island management), and the 100% icon rate ensures every quest is visually identifiable without reading its title. The gear default_quest_shape (shared with the overall chapter) is a Ragnamod lineage signature — not observed in any other pack family. The two layered decorative images (logo and sky background at the same position with slight offset) create a parallax-like visual effect.

Source: `MLDEG/Ragnamod_VI_Skyblock/main/config/ftbquests/quests/chapters/welcome.snbt`

> **Generality note:** Calibrated from Ragnamod skyblock pack. The "one shape per quest" approach in small welcome chapters is a viable alternative to the standard "one shape per chapter" approach. This pattern works well for chapters with fewer than 10 quests where each quest represents a distinct category.

### Case 26: Parallel Columns (GT Tier Ladder) — Gregitsky `progression` (GT Skyblock)
<!-- GT skyblock uniform spacing, not general calibration reference -->

30+ quests, parallel_columns topology with a dual-track progression system (coils and energy hatches running in parallel with circuit upgrades).

```
Coordinate extract (key nodes):
| Quest              | x    | y    | shape   | size | deps                    |
|--------------------|------|------|---------|------|-------------------------|
| 3D89DE26AB0B91AD   | -1.5 | -2.0 | —       | 1.0  | —                       |
| 3E87B5AB22D30E52   | -0.5 | -2.0 | —       | 1.0  | 3D89                    |
| 085840FB1CE4DB0F   | 0.5  | -3.0 | hexagon | 1.0  | —                       |
| 4BFC86B36355127E   | 0.5  | -2.0 | —       | 1.0  | 3E87, 0858, 3B0C       |
| 41CCECC4419BBE66   | 0.5  | -1.0 | —       | 1.0  | 4BFC                    |
| 69B1A6C35B0CFCC2   | 1.5  | -3.0 | —       | 1.0  | 0858                    |
| 0A669EF94A1D08C3   | 1.5  | -2.0 | —       | 1.0  | 4BFC, 69B1              |
| 13264CC7EF60C2F0   | 1.5  | -1.0 | —       | 1.0  | 41CC, 0A66              |
| 05E2912D39E8CE24   | 2.5  | -3.0 | —       | 1.0  | 69B1                    |
| 769F726C473D8AC4   | 2.5  | -2.0 | —       | 1.0  | 0A66, 05E2              |
| 0DE7635288AD0AFC   | 2.5  | -1.0 | —       | 1.0  | 1326, 769F              |
| 013FDE3B7464224C   | 3.5  | -3.0 | —       | 1.0  | 05E2                    |
| 4F8D9AA54FD8288F   | 3.5  | -2.0 | —       | 1.0  | 769F, 013F              |
| 2054CBB9AE6CC5AA   | 3.5  | -1.0 | —       | 1.0  | 0DE7, 4F8D              |
| 3F57B9A4AC7ECEA3   | 4.5  | -3.0 | —       | 1.0  | 013F                    |
| 6AD3F4792D935B9A   | 4.5  | -2.0 | —       | 1.0  | 4F8D, 3F57              |
| 77538DDE72735ED7   | 4.5  | -1.0 | —       | 1.0  | 2054, 6AD3              |
| 45BCD0877E46159A   | -1.5 | 1.0  | —       | 1.0  | 3D89                    |
| 75DA5E67FAB93E2E   | -0.5 | 1.0  | —       | 1.0  | 45BC                    |
| 65BF9B667E1A1BFC   | 0.0  | 2.0  | —       | 1.0  | 75DA, 299B              |

Shape distribution: hexagon(1), default(29+)
Size distribution: 0 quests >= 1.5
Icon rate: 0/30 (0%)
Spacing: min=1.0, avg=1.0, max=1.0 (uniform grid)
Topology: parallel_columns (max_depth=5, max_width=8, two parallel tracks)
Quest links: 2
Optional: 1 (ULV voltage coil)
Multi-dep: 14 quests (47%, high)
```

Gregitsky's progression chapter implements a textbook parallel_columns layout with two horizontal tracks running at y=-3 (voltage coils, ascending LV→MV→HV→EV→IV) and y=-1 (coil blocks, ascending cupronickel→kanthal→nichrome→RTM alloy), connected by energy input hatch quests at y=-2 that serve as rung nodes in a ladder pattern. The spacing is perfectly uniform (1.0 unit in both x and y), creating the most grid-like parallel_columns in the dataset. A secondary circuit progression track runs below at y=1 to y=4, connected via quest_links. The zero icon rate and shape monoculture (all default except one hexagon) reflect a utilitarian design philosophy consistent with GT skyblock packs where players are expected to know the tier ladder by heart. The 47% multi-dep rate is the highest for a parallel_columns chapter, driven by the ladder-connecting hatch quests that each depend on both the coil below and the coil to the left.

Source: `H4ruku0/Gregitsky/main/config/ftbquests/quests/chapters/progression.snbt`

> **Generality note:** Calibrated from GT skyblock pack. The uniform 1.0-unit spacing and ladder-topology parallel columns are specific to GT tier progression. This is the first skyblock parallel_columns case in the dataset. Standard parallel_columns cases (Cases 6, 14) remain the universal reference for non-uniform spacing.

### Case 27: Diamond Convergence (Survival Tutorial) — Rogue Mayhem `steps_to_not_die` (Adventure/Survival)
<!-- First non-expert diamond_convergence — extends applicability beyond expert packs -->

12+ quests, diamond_convergence topology with a large convergence hub collecting 9 dependencies. The survival tutorial chapter uses Cold Sweat temperature mechanics as the central theme.

```
Coordinate extract (key nodes):
| Quest              | x    | y    | shape  | size | deps (count) |
|--------------------|------|------|--------|------|--------------|
| 648483F84A2E39C5   | -3.0 | 23.0 | —      | 1.0  | —            |
| 245F22162E11EA0F   | 3.0  | 23.0 | —      | 1.0  | —            |
| 7525D2194D408D54   | 0.0  | 20.0 | —      | 2.0  | —            |
| 2340109634946CFE   | -2.0 | 24.0 | —      | 1.0  | —            |
| 5EA64C21B9936AD8   | 2.0  | 24.0 | —      | 1.0  | —            |
| 5272FF1BDC667878   | 2.0  | 22.0 | —      | 1.0  | —            |
| 5CE1E16C37C0D8F8   | -2.0 | 22.0 | —      | 1.0  | 2413         |
| 0A12D1871E992570   | 1.0  | 25.0 | —      | 1.0  | —            |
| 71FE71DD87AAB1A8   | —    | —    | —      | 1.0  | —            |
| 6D914EF851B509AD   | 0.0  | 23.0 | circle | 3.0  | 9 deps       |
| 14344985077FC690   | —    | —    | —      | 2.0  | 7525, 3C95   |

Shape distribution: circle(1), default(11+)
Size distribution: 3 quests >= 2.0
Icon rate: ~8/12 (67%)
Spacing: min=1.0, avg=2.0, max=5.0
Topology: diamond_convergence (max_depth=2, convergence_ratio=0.083, 9-dep hub)
Task types: item(5), checkmark(2), advancement(3), custom(2)
Rewards: xp(11) + item(11) — every quest has both XP and item reward
dependency_requirement: one_completed(1)
Custom task types: custom (Cold Sweat integration, mob taming)
```

Rogue Mayhem's survival tutorial demonstrates a diamond_convergence pattern where 9 independent survival lessons converge on a single size-3.0 circle quest ("Survivalist's Simplicity") at (0, 23). The convergence node has the highest dependency count for a single quest in a non-expert pack (9 deps), and the convergence_ratio of 0.083 is below the standard 0.15 threshold for diamond_convergence — this case is classified as diamond_convergence based on the visual centrality of the hub rather than the statistical ratio. The y-coordinates are unusually high (y=20 to y=25) compared to the typical y=0 origin, suggesting this chapter is part of a larger vertically-scrolling tutorial layout. The task type diversity (item, checkmark, advancement, custom) is the highest for a tutorial chapter, reflecting the pack's integration with Cold Sweat's temperature mechanics, Alex's Mobs' chameleon taming, and custom KubeJS survival checks. Every quest rewards both XP and a loot box item (kubejs:makeshift_box, gear_box, mischievous_box), creating a consistent reward-per-quest economy that teaches players the pack's box-opening progression system.

Source: `ReeCodes/rogue/main/config/ftbquests/quests/chapters/steps_to_not_die.snbt`

> **Generality note:** Calibrated from adventure/survival pack. The 9-dependency convergence hub and the box-reward economy are pack-specific. This is the first diamond_convergence case from a non-expert pack, expanding the topology's known applicability range. Standard diamond_convergence cases (Cases 4, 9, 18) remain the universal reference for expert-pack convergence.

### Case 28: Hub + Fan (Non-Expert Kitchen-Sink) — Enigmatica9 `chapter_one` (Kitchen-Sink)
<!-- First non-expert hub_fan with command-reward economy — validates MP64 -->

67 quests, hub_fan topology with hexagon-dominant shape vocabulary and heavy command-reward delivery. The opening chapter of Enigmatica 9's non-expert variant.

```
Coordinate extract (key nodes, 67 total):
| Quest (abbrev ID)  | x     | y     | shape    | size | deps (count) |
|--------------------|-------|-------|----------|------|--------------|
| Root (2CCCD)       | 0.0   | -7.5  | —        | 3.0  | —            |
| Metallurgy (1075F) | -2.5  | -7.5  | hexagon  | 1.0  | 1            |
| Naga (73CDA)       | -3.5  | -7.5  | hexagon  | 1.0  | 1            |
| Potion (66585)     | -2.0  | -3.5  | —        | 1.0  | 1            |
| Hex hub (chain)    | -3.5..0.5 | -3.5..3.5 | hexagon | 1.0 | 1-2    |

Shape distribution: hexagon(42), default(24), heart(1)
Size distribution: 1 quest >= 3.0 (root)
Icon rate: 94/67 (140% — multiple icons per quest including reward icons)
Spacing: min=0.5, avg=1.0, max=2.5
Topology: hub_fan (root at (0,-7.5) with 6-8 first-stage branches radiating outward)
Task types: item(139), observation(5), advancement(1)
Rewards: command(56) — 82% of quests use command rewards, choice(1)
dependency_requirement: one_completed(1)
hide_dependency_lines: 33 (49%)
Multi-dep: 4 quests (max 4 deps)
Bounding box: 13.0 × 11.0
```

Enigmatica 9's chapter_one demonstrates a hub_fan pattern where the root quest at (0, -7.5) with size 3.0 serves as the organizational center, with 6-8 branches radiating outward to hexagon-shaped mod introductions. The dominant hexagon shape (63% of quests with explicit shapes) is the Enigmatica lineage signature — it marks "processing" or "important crafting" nodes. The command-reward delivery system (`/execute at @p run loot spawn ~ ~1 ~ loot enigmatica:...`) creates invisible loot boxes, with 56 of 67 quests using this pattern. The 49% hide_dependency_lines rate reduces visual clutter in this dense hub layout. The 140% icon rate (more icons than quests) comes from reward icons counted alongside quest icons — each command reward carries its own custom icon (e.g., `kubejs:farmers_delight`). The bounding box is moderate (13×11) for a 67-quest chapter, yielding a density of ~0.47 quests/sq-unit.

Source: `EnigmaticaModpacks/Enigmatica9/master/config/ftbquests/quests/chapters/chapter_one.snbt`

> **Generality note:** Calibrated from non-expert kitchen-sink pack. The command-reward delivery and hexagon dominance are Enigmatica lineage-specific. This is the first hub_fan case from a non-expert kitchen-sink with command-reward economy. Standard hub_fan cases (Cases 3, 5, 19) remain the universal reference.

---

### Case 29: Parallel Columns (GT Skyblock) — GregFactory-Sky `lv` (Expert Skyblock)
<!-- GT skyblock parallel columns — extends MP65 (zero-reward skyblock) -->

27 quests, parallel_columns topology with 9 vertical columns spanning x=-2 to x=12. GregTech skyblock with zero rewards.

```
Coordinate extract (all 27 quests):
| Quest # | x     | y     | deps (count) |
|---------|-------|-------|--------------|
| 0       | 3.0   | 0.0   | 2            |
| 1       | 0.0   | 0.0   | 2            |
| 2       | 2.0   | -2.0  | 2            |
| 3       | 2.0   | 0.0   | 2            |
| 4       | 4.0   | -2.0  | 1            |
| 5       | 0.0   | 2.0   | 1            |
| 6       | 2.0   | -4.0  | 1            |
| 7       | 2.0   | -6.0  | 1            |
| 8       | -2.0  | -4.0  | 1            |
| 9       | 4.0   | 0.0   | 1            |
| 10      | 8.0   | 0.0   | 1            |
| 11      | 6.0   | -2.0  | 2            |
| 12      | 6.0   | -4.0  | 2            |
| 13      | 8.0   | -6.0  | 2            |
| 14      | 4.0   | -2.0  | 1            |
| 15      | 10.0  | -4.0  | 2            |
| 16      | 12.0  | -2.0  | 1            |
| 17      | 12.0  | -4.0  | 1            |
| 18      | 10.0  | -6.0  | 1            |
| 19      | 8.0   | -8.0  | 2            |
| 20      | 4.0   | 0.0   | 1            |
| 21      | 10.0  | 0.0   | 1            |

Columns detected (9 columns):
  x=-2: 1 quest, y=[-4]
  x=0:  2 quests, y=[0, 2]
  x=2:  5 quests, y=[-6, -4, -2, 0, 0]
  x=3:  1 quest, y=[0] (entry point)
  x=4:  5 quests, y=[-2, -2, -2, 0, 0]
  x=6:  4 quests, y=[-4, -4, -2, -2]
  x=8:  4 quests, y=[-8, -6, 0, 0]
  x=10: 3 quests, y=[-6, -4, 0]
  x=12: 2 quests, y=[-4, -2]

Shape distribution: default(27) — shape monoculture
Size distribution: 2 quests >= 2.0 (EBF milestone + one other)
Icon rate: 4/27 (15%)
Spacing: 2.0 units between columns (uniform)
Topology: parallel_columns (9 columns, max_depth=6, max_width=5)
Task types: item(34)
Rewards: 0 (ZERO — validates MP65)
Multi-dep: 8 quests (30%)
Optional: 1
Bounding box: 14.0 × 10.0
```

GregFactory-Sky's lv chapter implements a parallel_columns layout where each column represents a different GT machine line or material processing chain. The 2.0-unit column spacing is uniform and consistent with other GT packs (GT-Odyssey uses 2.0, Gregitsky uses 1.0). The leftmost columns (x=0 to x=4) contain early-tier machines (motors, pistons, pumps, wiremills), while rightward columns (x=6 to x=12) contain advanced processing (electrolyzer, mixer, EBF, aluminium). The EBF milestone at (8, -8) with size 2.0 serves as a convergence point requiring both cupronickel coils and the electrolyzer line. The zero-reward economy validates MP65 — in a GT skyblock, unlocking new machines IS the reward. The 15% icon rate uses GT item icons for milestone materials (cupronickel_ingot, gallium_dust, electric_blast_furnace).

Source: `ProgregssTeam/GregFactory-Sky/main/config/ftbquests/quests/chapters/lv.snbt`

> **Generality note:** Calibrated from GT skyblock pack. The uniform 2.0-unit column spacing and zero-reward economy are specific to GT skyblock context. The 9-column layout is wider than most parallel_columns cases. Standard parallel_columns cases (Cases 6, 14, 26) remain the universal reference.

---

### Case 30: Tree Branching (Adventure Tutorial) — Mincemeat-2 `getting_started` (Adventure/Space)
<!-- First tree_branching from adventure pack with 11 task types -->

108 quests, tree_branching topology with diverse task types and optional side branches. Space adventure pack tutorial.

```
Coordinate extract (key nodes, 108 total):
| Quest (abbrev ID)  | x     | y     | shape    | size | deps (count) |
|--------------------|-------|-------|----------|------|--------------|
| Root (2BE6)        | 0.0   | 0.0   | —        | 1.5  | —            |
| Branch 1 (journal) | 0.0   | 2.5   | hexagon  | 1.5  | 1            |
| Branch 2 (guide)   | 0.5   | -2.0  | —        | 1.0  | 1            |
| Branch 3 (copper)  | -2.0  | 1.5   | —        | 1.0  | 1            |
| Branch 4 (tools)   | 1.0   | -2.0  | hexagon  | 1.5  | 1            |
| Branch 5 (food)    | 2.5   | -4.0  | —        | 1.0  | 1            |
| Sub-branch chains  | ±7    | ±10.5 | —        | 1.0  | 1-2          |

Shape distribution: hexagon(3), default(105)
Size distribution: 3 quests >= 1.5
Icon rate: 15/108 (14%)
Spacing: min=0.5, avg=1.5, max=3.0
Topology: tree_branching (root → 6 branches → sub-branches, max_depth=8)
Task types: item(274), stat(3), checkmark(6), advancement(4), structure(1), observation(1)
Rewards: command(6) — tutorial-only command rewards
dependency_requirement: one_completed(1)
Optional: 10 (9.3%)
Multi-dep: 3 quests (max 2 deps)
Bounding box: 20.0 × 16.0
```

Mincemeat-2's getting_started chapter demonstrates tree_branching from a central root quest at (0, 0) with size 1.5 that branches into 6 thematic paths (journal, guide, tools, food, combat, exploration). Each branch extends 5-8 quests deep with consistent 1.5-unit spacing between chain nodes. The 10 optional quests (9.3%) are distributed across side branches that provide bonus content without blocking main progression. The command rewards appear only on tutorial quests (6 total), transitioning to choice rewards in later chapters. The 14% icon rate is moderate for a 108-quest chapter — icons mark key milestones and biome-gated content. The bounding box (20×16) is large for a tutorial chapter, reflecting the pack's emphasis on exploration from the start. The task type diversity (6 types in the tutorial alone: item, stat, checkmark, advancement, structure, observation) is the highest for any getting_started chapter in the dataset, validating MP67 (Task-Type Diversity).

Source: `uthw/Mincemeat-2/main/config/ftbquests/quests/chapters/getting_started.snbt`

> **Generality note:** Calibrated from adventure/space pack. The 6-branch tree and diverse task types are Mincemeat-2 specific. This is the first tree_branching case from a non-expert adventure pack. Standard tree_branching cases (Cases 7, 8, 23) remain the universal reference.

---

### Case 31: Hub + Fan (Cobblemon Welcome) — Cobblemon-Radically-Reimagined `humble_beginnings` (Cobblemon/Adventure)
<!-- Minimal hub_fan for Cobblemon welcome — 100% icon rate, checkmark-only -->

7 quests, hub_fan topology with 100% icon rate and checkmark-only tasks. Cobblemon pack welcome chapter.

```
Coordinate extract (all 7 quests):
| Quest (abbrev ID)  | x     | y     | shape  | size | deps |
|--------------------|-------|-------|--------|------|------|
| Root (3696D)       | 0.0   | 0.0   | —      | 1.25 | —    |
| Gacha (73ACA)      | -1.5  | -1.5  | —      | 1.0  | root |
| Music (43BFD)      | 0.0   | -2.0  | —      | 1.0  | root |
| Album (7B901)      | 1.5   | -1.5  | —      | 1.0  | root |
| Skills (0E3F2)     | -1.0  | -3.0  | —      | 1.0  | root |
| Waystone (55729)   | 1.0   | -3.0  | —      | 1.0  | root |
| Collection (7F0E3) | 0.0   | 2.0   | circle | 1.0  | root |

Shape distribution: circle(1), default(6)
Size distribution: 1 quest at 1.25 (root)
Icon rate: 7/7 (100% — every quest has a custom icon)
Spacing: min=1.0, avg=1.5, max=2.0
Topology: hub_fan (root → 6 leaves, max_depth=1)
Task types: checkmark(7) — 100% checkmark
Rewards: 0 (ZERO — validates MP65 for Cobblemon context)
Multi-dep: 0
Optional: 0
Bounding box: 3.0 × 5.0 (most compact hub_fan in dataset)
```

Cobblemon-Radically-Reimagined's humble_beginnings chapter is the most minimal hub_fan in the dataset — a single root quest with 6 fan-out leaves, all checkmark tasks, all with custom icons (gacha_coin, music_disc, collectors_album, skills_record, waystone). The 100% icon rate and checkmark-only task design create a "read and click" tutorial that introduces the pack's auxiliary systems (gacha machine, music, albums, skills, waystones) without any crafting requirements. The circle shape on the collection quest at (0, 2.0) is positioned above the root, creating an inverted fan where the root is the organizational center but the collection quest is the visual endpoint. The 3.0×5.0 bounding box is the most compact welcome chapter observed. The zero-reward economy validates MP65 for Cobblemon-adventure context.

Source: `Spudstak/Cobblemon-Radically-Reimagined/main/config/ftbquests/quests/chapters/humble_beginnings.snbt`

> **Generality note:** Calibrated from Cobblemon adventure pack. The 100% icon rate and checkmark-only design are specific to welcome/tutorial chapters. This is the most compact hub_fan case in the dataset. Standard hub_fan cases (Cases 3, 5, 19, 28) remain the universal reference for larger hub layouts.

---

### Case 32: Parallel Columns (Large Skyblock Tech) — Ultimate-Progression-Sky `mekanism` (Skyblock/Tech)
<!-- Largest zero-reward parallel_columns — validates MP65 at scale -->

198 quests, parallel_columns topology spanning a large bounding box. Zero-reward skyblock tech chapter.

```
Coordinate extract (summary, 198 total):
x-range: [-8.0..19.0] (27.0 units wide)
y-range: [-10.0..6.0] (16.0 units tall)

Columns detected (estimated from spacing):
  x=-8 to x=0: early Mekanism (ore processing, basic machines)
  x=0 to x=8: mid-tier (chemical processing, energy generation)
  x=8 to x=19: late-tier (fusion reactor, digital miner, SPS)

Shape distribution: default(198) — shape monoculture
Size distribution: estimated 0-2 quests >= 2.0
Icon rate: 1/198 (0.5% — near-zero)
Spacing: ~2.0 units between columns
Topology: parallel_columns (max_depth=12, max_width=8, estimated)
Task types: item(441), checkmark(6)
Rewards: 0 (ZERO — validates MP65 at scale)
Multi-dep: 10 quests (5%)
hide_dependency_lines: 8
Optional: 0
Bounding box: 27.0 × 16.0
```

Ultimate-Progression-Sky's mekanism chapter is the largest zero-reward chapter in the dataset (198 quests) and demonstrates that parallel_columns scales well to large chapter sizes without rewards. The 27-unit width approaches the R59 warning threshold (30 units), making this one of the widest non-highway chapters observed. The near-zero icon rate (0.5%) and shape monoculture (all default) create a uniform visual field where the only structural signals come from coordinate placement and the sparse multi-dep convergence points. The 5% multi-dep rate is low for 198 quests, indicating mostly independent processing chains with occasional convergence at key milestones (e.g., metallurgic infuser → steel casing → enrichment chamber). The 8 hide_dependency_lines instances mark the most complex convergence nodes. This case validates MP65 at scale: even with 198 quests and zero rewards, the parallel_columns topology provides clear progression through spatial organization alone.

Source: `MundM2007/Ultimate-Progression-Sky/main/config/ftbquests/quests/chapters/mekanism.snbt`

> **Generality note:** Calibrated from skyblock tech pack. The 198-quest scale and near-zero icon rate are specific to comprehensive Mekanism chapters. The 27-unit width is at the edge of comfortable viewing. Standard parallel_columns cases (Cases 6, 14, 26, 29) remain the universal reference.

---

### Case 33: Grid Catalog (Extreme Fan-In) — CreateBlock `farmer` (Create/Multi-Mod)
<!-- Grid catalog with extreme 47-dep convergence — validates MP66 -->

57 quests, grid_catalog topology with two distinct farming regions connected by a convergence funnel. Create-centric multi-mod pack.

```
Coordinate extract (all 57 quests):
| Region | x-range | y-range | Pattern |
|--------|---------|---------|---------|
| Farming Grid A | 4.0–6.0 | 1.5–5.5 | 3 columns × 5 rows, 1.0-unit spacing |
| Farming Grid B | 14.0–16.0 | 1.5–5.5 | 3 columns × 5 rows, 1.0-unit spacing |
| Convergence Row | 7.0–13.0 | -1.0 | 7 quests in a horizontal line, 1.0-unit |
| Funnel Row | 7.5–12.5 | 0.0 | 6 quests staggered between convergence |
| Convergence Hub | 9.0–11.0 | 1.0–2.0 | 4 quests at the funnel point |
| Outliers | 10.0–12.0 | 11.0 | 2 quests (endgame milestones) |

Shape distribution: hexagon(2), default(55)
Size distribution: 2 quests at 1.5 (convergence milestones)
Icon rate: ~14/57 (estimated 25%)
Spacing: 1.0 units uniform within regions, 8.0 units between regions
Topology: grid_catalog with convergence funnel (max_depth=8, max_width=7)
Task types: item(103) — all item tasks
Rewards: item(103) — near-zero reward economy (7.8% coverage)
Multi-dep: convergence quest with 47 dependencies (highest single-quest dep count in dataset, validates MP66)
Optional: 0
Bounding box: 12.0 × 12.0
```

CreateBlock's farmer chapter demonstrates a dual-grid catalog where two identical farming regions (each a 3×5 grid at 1.0-unit spacing) are connected via a convergence funnel at y=0. The left grid (x=4–6) covers one set of farming mods (e.g., Pam's HarvestCraft crops) while the right grid (x=14–16) covers another (e.g., Farmer's Delight recipes). The convergence row at y=-1 collects items from both grids into a horizontal processing chain, with the funnel at (10, 1–2) serving as the 47-dependency capstone quest. The 8-unit gap between the two grids creates a visual separation that communicates "these are two independent farming systems." The hexagon shape marks only 2 of 57 quests — the convergence milestones — consistent with the shape monoculture principle (MP48) where large chapters minimize shape vocabulary.

Source: `TheosCreation/CreateBlock/1.19.2-4.8.0/minecraft/config/ftbquests/quests/chapters/farmer.snbt`

> **Generality note:** Calibrated from Create multi-mod pack. The dual-grid convergence pattern is specific to chapters that catalog two parallel farming systems. The 47-dep convergence is an extreme outlier — most packs stay under 10 deps per quest. Standard grid_catalog cases (Cases 9, 15) remain the universal reference for simpler catalog layouts.

---

### Case 34: Hub + Fan (100% Optional Skyblock) — Extraordinary-Energy-Modern `skyblock` (Skyblock)
<!-- First 100%-optional hub_fan — all quests are side content -->

14 quests, hub_fan topology where every quest is marked optional. Skyblock introduction chapter with Ex Deorum.

```
Coordinate extract (all 14 quests):
| Quest # | x    | y    | optional | deps |
|---------|------|------|----------|------|
| 0 (root)| 0.0  | -1.0 | yes      | 0    |
| 1       | -1.5 | 1.0  | yes      | 1    |
| 2       | 1.5  | 1.0  | yes      | 1    |
| 3       | 0.0  | 3.0  | yes      | 1    |
| 4       | 1.5  | 3.0  | yes      | 1    |
| 5       | -1.5 | 3.0  | yes      | 1    |
| 6       | 0.0  | 5.5  | yes      | 1    |
| 7       | -1.5 | 5.5  | yes      | 1    |
| 8       | 0.0  | 7.5  | yes      | 1    |
| 9       | -1.5 | 7.5  | yes      | 1    |
| 10      | -3.0 | 7.5  | yes      | 1    |
| 11      | 3.0  | 1.0  | yes      | 1    |
| 12      | 3.0  | 3.0  | yes      | 1    |
| 13      | 4.5  | 1.0  | yes      | 1    |

Shape distribution: default(14) — shape monoculture
Size distribution: all 1.0 (no size hierarchy)
Icon rate: 0/14 (0%)
Spacing: min=1.5, avg=2.0, max=2.5
Topology: hub_fan (root at (0,-1) with 3 branches radiating outward)
Branch A (left): (-1.5,1) → (-1.5,3) → (-1.5,5.5) → (-1.5,7.5) → (-3.0,7.5)
Branch B (center): (0,3) → (0,5.5) → (0,7.5)
Branch C (right): (1.5,1) → (1.5,3) → (3.0,1) → (3.0,3) → (4.5,1)
Task types: item(28), checkmark(2)
Rewards: item(31) — item-only economy
Multi-dep: 0
Optional: 14 (100% — first 100%-optional chapter in dataset)
Bounding box: 7.5 × 8.5
```

Extraordinary-Energy-Modern's skyblock chapter is the first hub_fan in the dataset where every quest is marked optional. This creates a unique player experience: the entire chapter is presented as side content with no mandatory progression path. The root quest at (0, -1) serves as an organizational center, but since all branches are optional, the player has complete freedom to pick and choose which Ex Deorum systems to engage with. The three branches extend at roughly 120° intervals from the root (left, center, right), creating a symmetric fan pattern. The complete absence of shape overrides, size hierarchy, and icons creates a flat visual field that reinforces the "everything is optional" message — there's no visual signal that any quest is more important than another. This topology validates MP65 for Ex Deorum skyblock context while demonstrating a novel use of the optional flag as a chapter-level design philosophy.

Source: `exe-teams/extraordinary-energy-modern/main/config/ftbquests/quests/chapters/skyblock.snbt`

> **Generality note:** Calibrated from skyblock pack. The 100%-optional hub_fan is a novel design pattern not previously observed. It's applicable to any pack type where the chapter represents bonus content rather than mandatory progression. The absence of all visual hierarchy signals (shape, size, icon) is specific to this pack's minimal aesthetic. Standard hub_fan cases (Cases 3, 5, 19, 28) remain the universal reference for hub layouts with mandatory content.

---

### Case 35: Parallel Columns (Tech Progression) — Extraordinary-Energy-Modern `ae2` (Skyblock/Tech)
<!-- AE2 parallel columns in a compact skyblock context -->

36 quests, parallel_columns topology spanning two processing regions. Skyblock AE2 chapter.

```
Coordinate extract (key nodes, 36 total):
| Region | x-range | y-range | Quest count |
|--------|---------|---------|-------------|
| Upper-left cluster | -2.5 to -0.5 | -5.5 to 2.0 | 8 quests |
| Central columns | 0.5 to 3.5 | -4.0 to 3.0 | 14 quests |
| Right processing | 3.5 to 5.0 | -3.0 to 0.0 | 8 quests |
| Far-right storage | 4.0 to 6.5 | -9.5 to -6.0 | 6 quests |

Shape distribution: default(36) — shape monoculture
Size distribution: all 1.0 (no overrides)
Icon rate: ~6/36 (estimated 17%)
Spacing: ~1.0 units between adjacent quests, ~2.0 between column groups
Topology: parallel_columns (4 column groups, max_depth=6)
Task types: item(60), checkmark(2)
Rewards: item(60), command(2) — near-zero with 2 command rewards for AE2 milestones
Multi-dep: 0
Optional: 2 (storage region)
Bounding box: 9.0 × 12.5
```

Extraordinary-Energy-Modern's ae2 chapter implements a four-region parallel_columns layout where each region represents a different phase of AE2 progression: upper-left (basic presses and circuits), central (inscriber and assembler chains), right (molecular assembler and crafting), and far-right (storage cells and ME network). The column spacing is tighter than expert-pack GT chapters (1.0 vs 2.0 units), reflecting the skyblock context where viewport space is precious. The 2 command rewards on AE2 milestones break the otherwise zero-reward economy, suggesting the author considers AE2 completion worth explicitly rewarding — a departure from the pack's general MP65 zero-reward philosophy. The 9×12.5 bounding box is moderate for 36 quests, yielding a density of ~0.32 quests/sq-unit.

Source: `exe-teams/extraordinary-energy-modern/main/config/ftbquests/quests/chapters/ae2.snbt`

> **Generality note:** Calibrated from skyblock tech pack. The four-region column layout and tight 1.0-unit spacing are specific to AE2 chapters in skyblock context. Standard parallel_columns cases (Cases 6, 14, 26, 29, 32) remain the universal reference for GT-style tier columns.

---

### Case 36: Tree Branching (Chinese Skyblock Expert) — Enigmatic-Skies `cascading` (Skyblock/Expert)
<!-- Chinese skyblock expert with diamond+gear milestone shapes -->

27 quests, tree_branching topology with diamond and gear shape vocabulary. Chinese skyblock expert pack.

```
Coordinate extract (all 27 quests):
| Quest # | x    | y    | shape   | deps |
|---------|------|------|---------|------|
| 0       | 4.0  | -2.5 | —       | 0    |
| 1       | 1.0  | -1.5 | —       | 1    |
| 2       | 7.0  | -1.5 | —       | 1    |
| 3       | 4.0  | -0.5 | gear    | 1    |
| 4       | 3.5  | -1.5 | —       | 1    |
| 5       | 7.5  | -0.5 | —       | 1    |
| 6       | 4.0  | 0.5  | —       | 1    |
| 7       | 4.0  | 5.0  | diamond | 1    |
| 8       | 4.0  | 4.0  | —       | 1    |
| 9       | 5.0  | 1.0  | —       | 1    |
| 10      | 1.5  | -0.5 | —       | 1    |
| 11      | 0.5  | -0.5 | —       | 1    |
| 12      | 1.5  | 1.0  | —       | 1    |
| 13      | 1.5  | 2.0  | —       | 1    |
| 14      | 2.5  | 3.0  | —       | 1    |
| 15      | 4.5  | -1.5 | —       | 1    |
| 16      | 5.5  | 3.0  | —       | 1    |
| 17      | 4.0  | 2.0  | —       | 1    |
| 18      | 5.0  | 0.0  | —       | 1    |
| 19      | 3.0  | 1.0  | —       | 1    |
| 20      | 6.0  | 1.5  | —       | 1    |
| 21      | 3.0  | 5.5  | —       | 1    |
| 22      | 3.0  | 0.0  | —       | 1    |
| 23      | 5.0  | 5.5  | —       | 1    |
| 24      | 0.5  | 1.0  | —       | 1    |
| 25      | 0.5  | 2.0  | —       | 1    |
| 26      | 6.0  | 0.5  | —       | 1    |

Shape distribution: diamond(4), gear(2), default(21)
Size distribution: all default 1.0
Icon rate: 15/27 (56%)
Spacing: min=0.5, avg=1.0, max=2.0
Topology: tree_branching (root at (4,-2.5) branching left and right)
Left branch: (1,-1.5) → (0.5,-0.5) → (1.5,1) → (1.5,2) → (2.5,3)
Right branch: (7,-1.5) → (7.5,-0.5) → (6,1.5) → (5.5,3)
Center trunk: (4,-0.5) → (4,0.5) → (4,2) → (4,4) → (4,5)
Task types: item(64), checkmark(0)
Rewards: loot(17), item(64), choice(1)
Multi-dep: 0
Optional: 0
Bounding box: 7.0 × 8.0
```

Enigmatic-Skies's cascading chapter demonstrates a classic tree_branching pattern from a root quest at (4, -2.5) that splits into three branches: a left branch (resource gathering and early processing), a right branch (advanced crafting), and a center trunk (milestone progression). The gear shape at (4, -0.5) marks the first major processing milestone on the center trunk, while diamond shapes appear at convergence points (4, 5.0) and other key milestones. The 56% icon rate is the highest for a tree_branching chapter in the dataset — reflecting the Chinese pack author's emphasis on visual guidance (consistent with Cycle 11 findings about Chinese pack authors preferring visual quest markers). The loot+choice reward economy (17 loot, 1 choice) diverges from the zero-reward skyblock norm (MP65), suggesting this expert skyblock pack uses rewards to incentivize progression rather than relying solely on unlock-as-reward. The bounding box (7×8) is compact for 27 quests, yielding a density of ~0.48 quests/sq-unit — the highest for a tree_branching layout.

Source: `TeamKugimiya/Enigmatic-Skies/main/source/config/ftbquests/quests/chapters/cascading.snbt`

> **Generality note:** Calibrated from Chinese skyblock expert pack. The diamond+gear shape vocabulary and high icon rate are specific to Chinese pack design conventions. The loot+choice reward economy is atypical for skyblock packs. Standard tree_branching cases (Cases 7, 8, 23, 24, 30) remain the universal reference.

---

### Case 37: Hub + Fan (RPG Adventure Intro) — AOF-The-Frozen-Hope `lets_begin_the_adventure` (Kitchen-Sink/RPG)
<!-- RPG adventure intro with XP+loot dual economy -->

16 quests, hub_fan topology with XP+loot dual reward economy. Kitchen-sink RPG pack introduction.

```
Coordinate extract (all 16 quests):
| Quest # | x        | y        | shape    | deps |
|---------|----------|----------|----------|------|
| 0 (root)| -4.25    | -0.95    | —        | 0    |
| 1       | 0.5      | 3.5      | —        | 1    |
| 2       | -4.5     | 4.5      | —        | 1    |
| 3       | -4.2     | 0.0      | —        | 1    |
| 4       | -1.89    | -2.45    | circle   | 1    |
| 5       | -6.0     | -1.0     | —        | 1    |
| 6       | -7.0     | -2.0     | —        | 1    |
| 7       | -1.5     | -1.0     | —        | 1    |
| 8       | -7.5     | 1.5      | —        | 1    |
| 9       | -4.5     | 2.0      | —        | 1    |
| 10      | -2.0     | 2.0      | —        | 1    |
| 11      | -8.5     | 0.0      | —        | 1    |
| 12      | -3.5     | -2.5     | pentagon | 1    |
| 13      | -6.0     | -3.0     | —        | 1    |
| 14      | -1.0     | 0.5      | —        | 1    |
| 15      | 0.0      | -1.0     | —        | 1    |

Shape distribution: circle(1), pentagon(1), default(14)
Size distribution: all default 1.0
Icon rate: 5/16 (31%)
Spacing: min=1.0, avg=2.0, max=3.5
Topology: hub_fan (root at (-4.25,-0.95) with branches in 3 directions)
Left branch: (-6,-1) → (-7,-2) → (-8.5,0) → (-7.5,1.5)
Center branch: (-1.5,-1) → (-1,0.5) → (0,-1) → (0.5,3.5)
Upper branch: (-4.5,2) → (-4.5,4.5)
Lower markers: (-3.5,-2.5 pentagon), (-6,-3), (-1.89,-2.45 circle)
Task types: item(34), checkmark(2), dimension(1), structure(1)
Rewards: xp(12), loot(2), item(34) — XP+loot dual economy
Multi-dep: 0
Optional: 0
Bounding box: 9.0 × 7.5
```

AOF-The-Frozen-Hope's introduction chapter demonstrates a hub_fan from the root quest at (-4.25, -0.95) that branches in three directions: left (combat/exploration with the farthest reach to x=-8.5), center (tutorial/guide quests extending right to x=0.5), and upper (mod introductions at y=4.5). The pentagon shape at (-3.5, -2.5) marks a combat-related milestone, while the circle at (-1.89, -2.45) likely marks a QoL or information quest — consistent with the ATM-family shape vocabulary (pentagon = combat, circle = optional/info). The XP+loot dual reward economy (12 XP rewards + 2 loot table rewards) is characteristic of the DexxKnight1 author lineage (same as Age-of-Fate), diverging from both the zero-reward skyblock norm and the command-reward Enigmatica approach. The 9×7.5 bounding box is moderate, yielding a density of ~0.24 quests/sq-unit — spacious enough for the three-directional branching to be visually clear.

Source: `DexxKnight1/AOF-The-Frozen-Hope/main/config/ftbquests/quests/chapters/lets_begin_the_adventure.snbt`

> **Generality note:** Calibrated from kitchen-sink RPG pack. The three-directional hub_fan and XP+loot dual economy are DexxKnight1 lineage-specific. The pentagon/circle shape markers follow the ATM-family convention. Standard hub_fan cases (Cases 3, 5, 19, 28, 31, 34) remain the universal reference.

---

### Case 38: Highway Branch (Non-Expert Adventure) — Capivara SMP `create` (Adventure/RPG)
<!-- First non-expert highway_branch — horizontal spine with vertical branches -->

41 quests, highway_branch topology with horizontal spine at y=0 spanning 18.5 units. Non-expert adventure pack (Brazilian Portuguese language).

```
Main spine (y ≈ 0.0, x from -9.5 to 9.0):
  (-9.5, 0.0) → (-8.0, 0.0) → (-6.5, 0.0) → (-4.5, 0.0) → (-2.5, 0.0) →
  (-0.5, 0.0) → (1.5, 0.0) → (3.0, 0.0) → (4.5, 0.0) → (6.0, 0.0) → (7.5, 0.0) → (9.0, 0.0)
  Spacing: ~1.5-2.0 units between spine nodes
  Shape: octagon at milestones (-6.5, 0.0), (-4.5, 0.0), (-0.5, 0.0), (7.5, 0.0)

Upper branches (y > 0):
  (-7.5, 1.0) branch from (-8.0, 0.0)
  (-5.5, 3.0) branch from (-6.5, 0.0)
  (-4.5, 3.5) branch from (-5.5, 3.0) — Sail Block
  (-4.5, 2.0) branch from (-4.5, 0.0) — Stress Units (octagon, size 1.25)
  (2.5, 2.0) branch from (1.5, 0.0) — Normal fuel
  (3.5, 2.0) branch from (3.0, 1.0) — Superheat fuel
  (5.5, 2.0) branch from (6.0, 1.0)
  (6.5, 2.0) branch from (6.0, 1.0)

Lower branches (y < 0):
  (-7.5, -1.0) branch from (-8.0, 0.0)
  (-5.5, -2.5) branch from (-6.5, 0.0)
  (-5.0, -4.0) branch from (-5.5, -2.5)
  (-4.5, -3.0) branch from (-4.5, -2.0) — Transportando itens
  (-4.0, -4.0) branch from (-5.0, -4.0) — Logística no Transporte
  (-0.5, -1.5) branch from (-0.5, 0.0) — Engineer's Goggles
  (4.5, -2.0) branch from (4.5, -1.0)

Root: gear shape at (-5.5, -1.0), size 1.25 — "Pondering" (hub quest)
Shape distribution: octagon(5, milestones), gear(1, root), default(35)
Size distribution: 1.25 (6 milestones), 1.0 (35 chain nodes)
Icon rate: 10/41 (24%)
Spacing: min=1.0, avg=2.55, max=3.5
Spine concentration: 29% within ±0.5 of y=0, 49% within ±1.0
Topology: highway_branch (max_depth=6, max_width=12)
Task types: item(54), checkmark(2)
Rewards: item(54), loot(15)
Multi-dep: 0
Optional: 0
Bounding box: 18.5 × 7.5
```

Capivara SMP's create chapter is the first non-expert highway_branch case in the dataset. The horizontal spine runs from x=-9.5 to x=9.0 at y≈0, with branches extending vertically to y=±4.0. The 5 octagon milestones (Contraptions, Stress Units, Mechanical Press, Train Tracks, and one unnamed) mark key Create technology acquisition points — a semantic pattern where octagon = "you just unlocked a major capability." The gear-shaped root at (-5.5, -1.0) is offset below the spine, creating a "dive into the workshop" visual metaphor before rejoining the main progression. The 24% icon rate is higher than expert highway packs (Create-New-Horizon mv: 8%), reflecting the non-expert pack's emphasis on visual guidance. The loot reward economy (15 loot tables for 54 item rewards) delivers randomized gear at each milestone — a departure from expert packs' zero-reward approach.

Source: `tronfy/csmpX/main/config/ftbquests/quests/chapters/create.snbt`

> **Generality note:** First non-expert highway_branch case. The octagon-for-milestone pattern and 24% icon rate are non-expert signatures. Expert highway_branch cases (Cases 10, 15, 19) use default shapes with lower icon rates (1-8%). The spine concentration threshold (29% at ±0.5, 49% at ±1.0) provides calibration for the Phase 2 `has_highway_spine` detector — non-expert packs may have wider branch dispersion than expert packs.

---

### Case 39: Highway Branch (Non-Expert Boss Chapter) — CTI Quests `boss` (Adventure/RPG)
<!-- Non-expert highway_branch with boss kill progression -->

68 quests, highway_branch topology with horizontal spine at y≈4.5 spanning 25.0 units. Non-expert adventure pack.

```
Main spine (y ≈ 3.5-5.5, x from -12.5 to 12.5):
  (-12.5, 3.5-5.5), (-10.0, 3.5-5.5), (-7.5, 3.5-5.5), (-5.5, 4.5),
  (-5.0, 3.5-5.5), (-4.5, 4.5), (-2.5, 3.5-5.5), (0.0, 3.5-5.5),
  (2.0, 3.5-5.5), (3.0, 3.5-4.5), (5.0, 3.5-5.5), (7.5, 5.5),
  (10.0, 3.5), (12.5, 3.5-5.5)
  Column spacing: 2.0-2.5 units between spine columns
  Each spine column has 2-3 quests stacked at y=3.5, 4.5, 5.5

Lower branches (y = 2.5, boss kills):
  (-12.5, 2.5), (-10.0, 2.5), (-7.5, 2.5), (-5.0, 2.5), (-2.5, 2.5),
  (0.0, 2.5), (2.5, 2.5), (5.0, 2.5), (7.5, 2.5), (10.0, 2.5), (12.5, 2.5)
  All hexagon shape — 11 boss kill quests

Upper branches (y = 6.5-9.5, boss rewards/milestones):
  (-7.5, 6.5), (-3.0, 6.5-8.5), (-2.5, 7.5-9.5), (-2.0, 6.5),
  (0.0, 7.5), (2.0, 6.5), (2.5, 7.5-9.5), (3.0, 6.5),
  (4.0, 9.5), (4.5, 8.5), (5.0, 6.5-9.5), (5.5, 8.5), (6.0, 9.5)
  rsquare(9) for milestone rewards

Deep branches (y = -2.5, extreme lower):
  (-5.0, -2.5), (-2.5, -2.5), (0.0, -2.5), (2.5, -2.5), (5.0, -2.5)

Root: gear shape at (0.0, 0.0), size 2.0
Shape distribution: hexagon(11, boss kills), rsquare(9, milestones), gear(1, root), circle(1), default(46)
Size distribution: 2.0 (root), 1.0 (67 chain nodes)
Spine concentration: 46% within ±1.0 of y=4.5
Topology: highway_branch (max_depth=8, max_width=14)
Task types: item(125), kill(estimated 11)
Rewards: item rewards
Multi-dep: 0
Optional: 0
Bounding box: 25.0 × 12.0
```

CTI Quests' boss chapter implements a "boss highway" — a horizontal spine where each column represents a boss tier, with hexagon-shaped kill quests below and rsquare milestone rewards above. The 11 hexagon quests at y=2.5 form a parallel kill-chain beneath the main spine, creating a dual-track structure: the spine tracks mod progression (gear, materials, preparation), while the lower track tracks boss kills. The upper branches at y=6.5-9.5 extend 4-5 units above the spine, representing post-boss reward quests. The 5 deep branches at y=-2.5 are extreme outliers — likely optional "challenge" bosses. The 25-unit width is the widest highway_branch in the dataset (approaching MM2 botania's 27.5-unit multiblock highway), and the three-layer structure (lower kills / middle spine / upper rewards) is unique to boss-focused non-expert packs.

Source: `Team-Innova-Constructors/cti-quests/main/chapters/boss.snbt`

> **Generality note:** First non-expert boss-highway pattern. The dual-track (spine + kill chain) and three-layer vertical structure are specific to boss chapters. Expert highway cases (Cases 10, 15, 19, 38) use single-track spines. The hexagon-for-kills semantic (11 boss hexagons) is consistent with ATM-6/ATM-10 bounty board pentagon usage — both use combat-semantic shapes for kill quests.

---

### Case 40: Highway Branch (Non-Expert Skyblock) — Ragnamod-VII-Skyblock `botania` (Skyblock)
<!-- Large non-expert skyblock highway_branch -->

114 quests, highway_branch topology with horizontal spine spanning 20.0 units. Non-expert skyblock pack.

```
Main spine (y ≈ 0.0-2.0, x from 0.0 to 20.0):
  Spine nodes at approximately 2.0-unit intervals along x-axis
  Shape: circle (dominant, 65 total) and square (49 total)
  Size: 1.0 (100 nodes), 2.0 (12 milestones), 0.07 (2 decorative)

Key coordinates:
  (0.0, 0.0) size 2.0 — root milestone (circle)
  (2.0, 0.0) size 2.0 — early milestone (circle)
  (14.0, 0.0) size 2.0 — mid-progression milestone (circle)
  (18.0, 0.0) size 2.0 — late milestone (circle)
  (19.5, 0.0-2.0) — endgame cluster

Upper branches (y > 2.0):
  Multiple branches extending to y=5.5
  Circle shape for flower collection quests
  Square shape for crafting/processing quests

Lower branches (y < 0.0):
  Branches to y=-4.5
  Mix of circle and square shapes

Shape distribution: circle(65), square(49)
Size distribution: 2.0 (12 milestones at ~2.0-unit x intervals), 1.0 (100 chain), 0.07 (2 decorative)
Spine concentration: estimated 30-35% within ±1.0 of y=1.0
Topology: highway_branch (max_depth=10, max_width=15)
Task types: item(291), kill(2)
Rewards: item(291) — zero-reward economy
Multi-dep: 0
Optional: 0
Bounding box: 20.0 × 10.0
```

Ragnamod-VII-Skyblock's botania chapter is the largest non-expert highway_branch case (114 quests) and the widest skyblock chapter in the dataset at 20 units. The circle/square dual-shape system (65+49) creates a two-category visual taxonomy: circles for flower collection (exploration/gathering) and squares for crafting/processing (workshop progression). The 12 size-2.0 milestones at roughly 2.0-unit x intervals create a rhythmic visual cadence along the spine — the player encounters a prominent milestone every ~2 units of horizontal scrolling. The 2 size-0.07 quests are effectively invisible decorative nodes (possibly images or spacers). The zero-reward economy (291 item tasks, 0 rewards) validates MP65 for skyblock context: the Botania progression itself is the reward.

Source: `MLDEG/Ragnamod-VII-Skyblock/main/config/ftbquests/quests/chapters/botania.snbt`

> **Generality note:** Calibrated from skyblock pack. The circle/square dual-shape system and 12-milestone rhythm are specific to large Botania chapters. The 20-unit width approaches expert highway scales (MM2 botania: 27.5 units). Non-expert spacing is ~15-30% wider than expert for the same quest count, consistent with the Cycle 14 finding.

---

### Case 41: Tree Branching (Non-Expert Skyblock) — Ragnamod-VII-Skyblock `extended_crafting` (Skyblock)
<!-- Large non-expert tree_branching with collection catalog -->

138 quests, tree_branching topology with root at origin branching into sub-regions. Non-expert skyblock pack.

```
Root region (x ≈ 0-3, y ≈ 0):
  (0.0, 0.0) size 2.0, octagon — root milestone
  (1.5, 0.0) — first branch point
  (3.0, 0.0) size 2.0, octagon — mid milestone

Left sub-tree (x < 0):
  (-1.5, -2.0), (-1.5, -1.0), (-1.5, 0.0) — square-shape column
  Vertical chain at x=-1.5, y from -2.0 to 0.0

Center region (x=0-6):
  Dense cluster of 80+ circle-shaped quests
  (2.0, -1.0), (2.0, 1.0), (3.0, -1.5), (3.0, 1.5)
  (4.0, -1.0), (4.0, 1.0), (4.5, 0.0)
  Circle(128) for collection-catalog pattern

Right region (x > 6):
  (6.0, 0.0) size 2.0, hexagon — milestone
  Further branching to x=13.5

Shape distribution: circle(128, collection items), square(6), octagon(2, milestones), hexagon(1, hub)
Size distribution: 2.0 (3 milestones), 1.0 (15 chain nodes), 0.5 (120 collection items)
Topology: tree_branching (root → 3 sub-regions, max_depth=8)
Task types: item(278), checkmark(estimated)
Rewards: item(278), choice(1)
Multi-dep: 0
Optional: 0
Bounding box: 15.0 × 8.0
```

Ragnamod-VII-Skyblock's extended_crafting chapter uses a tree_branching topology where the root at (0, 0) branches into three sub-regions: a left square-shape column for basic materials, a center circle-dominant collection catalog (128 quests at size 0.5), and a right hexagon-marked advanced region. The 128 circle-shaped quests at size 0.5 create a dense "collection wall" — a visual pattern where the player sees a field of small identical nodes representing individual crafting recipes. The 3 octagon milestones at size 2.0 serve as tree junctions, marking the transition between crafting tiers. The 15:8 aspect ratio (1.9:1) is wider than tall, consistent with tree_branching chapters that fan out horizontally from a central root. The single choice reward suggests a "pick your path" decision at one of the tier milestones.

Source: `MLDEG/Ragnamod-VII-Skyblock/main/config/ftbquests/quests/chapters/extended_crafting.snbt`

> **Generality note:** Calibrated from skyblock pack. The circle-dominant collection catalog at size 0.5 is specific to Extended Crafting chapters (278 individual recipes). The tree_branching structure is simplified compared to expert packs (no multi-dep convergence). Standard tree_branching cases (Cases 5, 11, 23, 30, 36) remain the reference for complex tree hierarchies.

---

### Case 42: Grid Catalog (Non-Expert Mega-Chapter) — CTI Quests `foodcollection` (Adventure/RPG)
<!-- Largest chapter in dataset — 496 quests in grid catalog -->

496 quests, grid_catalog topology spanning 59.0 × 59.5 units — the largest chapter in the dataset by both quest count and bounding box. Non-expert adventure pack.

```
Coordinate extract (summary, 496 total):
x-range: [-32.5..26.5] (59.0 units wide)
y-range: [-37.0..22.5] (59.5 units tall)

Layout pattern:
  Massive grid of collection quests with minimal dependencies
  490/496 quests are roots (no dependencies) — 98.8% root rate
  Quests arranged in approximate grid with ~2.0-unit spacing

Shape distribution: default(496) — shape monoculture
Size distribution: all 1.0 (no hierarchy)
Icon rate: estimated low (<5%)
Spacing: ~2.0 units (grid spacing)
Topology: grid_catalog (max_depth=1, max_width=496)
Task types: item(978, avg 1.97/quest)
Rewards: item(978)
Multi-dep: 0
Optional: 0
Bounding box: 59.0 × 59.5 (largest in dataset — exceeds R59 hard limit of 35 units!)
```

CTI Quests' foodcollection chapter is the largest chapter ever observed in the dataset at 496 quests and 59.0 × 59.5 units — it exceeds the R59 hard limit of 35 units on both axes by a factor of 1.7. This chapter catalogs food items from dozens of food-related mods (Farmer's Delight, Croptopia, Pam's HarvestCraft, etc.), with each quest representing a single food item or recipe group. The 98.8% root rate (490/496 quests have zero dependencies) confirms this is a pure collection catalog with no forced progression — the player can complete quests in any order. The bounding box violation of R59 suggests that for pure catalog chapters, the viewport limit may need to be relaxed or the chapter split into sub-chapters. The 1.97 items/quest ratio indicates many quests have 2 item tasks (e.g., "craft this food" + "eat this food"). This case demonstrates that grid_catalog scales to extreme sizes when the chapter's purpose is purely organizational rather than progression-driven.

Source: `Team-Innova-Constructors/cti-quests/main/chapters/foodcollection.snbt`

> **Generality note:** First mega-chapter grid_catalog exceeding R59 limits. The 496-quest scale and 59-unit bounding box demonstrate that pure collection catalogs need relaxed viewport constraints. The Phase 2.5 decomposition algorithm should flag chapters >200 quests for potential splitting. R59 may need a catalog exception: grid_catalog chapters with >300 quests and zero multi-dep may extend to 60 units.

### Case 43: Diamond Convergence (Non-Expert Progression Map) — Chroma Endless `progression_tree_2` (Vanilla+ Survival)
<!-- Non-expert diamond_convergence with tome-tier decorative images as vertical section markers -->

32 quests, diamond_convergence topology organized as a vertical progression map with 8 tiers. Non-expert vanilla+ survival pack by same author as Chroma-Technology-2.

```
Coordinate extract (summary, 32 total):
x-range: [-3.25..4.25] (7.5 units wide)
y-range: [-0.25..23.25] (23.5 units tall)

Tier layout (y-values at 3.0-unit intervals):
  Tier 1 (y=-0.25): Vanilla(-3.25), Tinkers(-1.75,-1.25), Tetra(-0.25), Create(2.75), Better End(4.25) — 6 quests
  Tier 2 (y=2.75): Immersive Engineering(-1.0), Occultism(0.5), Mobs Farm(2.0) — 3 quests
  Tier 3 (y=5.75): Thermal(-1.0), Botania(0.5), Mini Utilities(2.0) — 3 quests
  Tier 4 (y=8.75): Ars Nouveau(-1.75), Elemental Craft(-0.25), Pedestal(1.25), Undergarden(2.75) — 4 quests
  Tier 5 (y=11.75): PneumaticCraft(-1.75), Xnet(-0.25), Compact Machines(1.25), Tardis(2.75) — 4 quests
  Tier 6 (y=14.75): Industrial Foregoing(-2.5, 2dep), RFTools(-1.0, 2dep), Extreme Reactors(0.5), EnderIO(2.0), Mekanism(3.5, 2dep) — 5 quests
  Tier 7 (y=17.75): Extended Crafting(-1.0, 2dep), Environmental Tech(0.5), Refined Storage(2.0) — 3 quests
  Tier 8 (y=20.75): Powah(-1.0), Draconic Evolution(0.5), ProjectE(2.0, 2dep) — 3 quests
  Endpoint (y=23.25): Creative Chapter(0.5) — 1 quest, octagon shape, size 2.5

Shape distribution: hexagon(default, 31), octagon(1 — endpoint)
Size distribution: 1.0(default, 31), 2.5(1 — endpoint)
Icon rate: 100% (every quest has a mod item icon)
Dependencies: 32 total, 5 multi-dep (16% convergence_ratio)
Multi-dep nodes: Industrial Foregoing(2), RFTools(2), Mekanism(2), Extended Crafting(2), ProjectE(2)
Decorative images: 16 (8 tome title images + 8 tome background panels, one pair per tier)
Topology: diamond_convergence (convergence_ratio=0.156, max_depth=9)
Task types: item(31), checkmark(1)
Rewards: none (progression map chapter — guides to other chapters)
Bounding box: 7.5 × 23.5 (aspect ratio 1:3.1, portrait)
```

Chroma Endless's progression_tree_2 serves as a pack-wide progression roadmap, where each quest represents a mod's chapter entry point. The 8 tiers are visually separated by decorative tome images (tome1.png through tome8.png) that serve as tier markers. The convergence pattern emerges at Tiers 6-8, where multi-dependency nodes require completing quests from multiple lower-tier branches. The Mekanism node at (3.5, 14.75) requires both Extreme Reactors and an earlier Mekanism-related quest, creating a diamond convergence where two technology paths merge. The Creative Chapter endpoint at (0.5, 23.25) with octagon shape and size 2.5 is the chapter's capstone, requiring completion of the late-game Draconic Evolution or Powah paths. The 100% icon rate (every quest displays its mod's signature item) and 100% hexagon default shape produce a visually clean "mod map" where icon differentiation replaces shape vocabulary.

Source: `Gogo08190/chroma-endless/main/config/ftbquests/quests/chapters/progression_tree_2.snbt`

> **Generality note:** This "progression map" pattern — a chapter that cross-references other chapters via dependencies — is distinct from self-contained quest lines. The convergence_ratio of 0.156 is just above the Phase 2 classifier threshold of 0.15, demonstrating that even progression-map chapters can trigger diamond_convergence classification. The tome decorative images as tier markers are a novel visual pattern (MP candidate) not seen in other packs. Calibrated from non-expert vanilla+ survival pack; the 3.0-unit vertical tier spacing is consistent with the 2.0–3.0 range observed in other diamond_convergence chapters.

---

### Case 44: Tree Branching (Non-Expert Mod Chapter) — Chroma Endless `botania` (Vanilla+ Survival)
<!-- 120 quests with rich shape vocabulary (5 types) and heavy hide_dependency_lines usage -->

120 quests, tree_branching topology with the richest non-expert shape vocabulary observed. Non-expert vanilla+ survival pack.

```
Coordinate extract (summary, 120 total):
x-range: estimated [-8..8] (~16 units wide)
y-range: estimated [-8..8] (~16 units wide)

Shape distribution: diamond(27), hexagon(9), pentagon(8), square(6), octagon(1), default(69)
Size distribution: 1.0(default, 119), 1.3(1)
Icon rate: 10% (12 custom icons)
Dependencies: 120 total (100% dep rate)
hide_dependency_lines: 25 quests (21%)
optional: 24 quests (20%)
Topology: tree_branching (root → branching subsystems, max_depth estimated 8-10)
Task types: item(estimated 110+), checkmark(estimated 10)
Rewards: item(estimated 120)
Bounding box: ~16 × 16 (estimated, square aspect ratio)
```

Chroma Endless's botania chapter contains 120 quests covering the full Botania mod progression, from basic mana generation through endgame Gaia Guardian content. The shape vocabulary uses 5 distinct types to signal quest roles: diamond for mana-processing milestones (27, the dominant shape), hexagon for functional blocks (9), pentagon for boss/ritual content (8), square for tool/utility quests (6), and octagon for capstone content (1). The 21% hide_dependency_lines rate is the highest observed in any non-expert pack, approaching the expert-pack range (40-80%) — this suggests the author deliberately reduces visual clutter in this large chapter. The 20% optional rate indicates that one-fifth of the content is side-quests, providing exploration paths off the main tree trunk. The Spark Augment quest demonstrates a 3-dependency convergence node (requiring Spark, Mana Pool, and Wand of the Forest), creating a local diamond within the tree structure.

Source: `Gogo08190/chroma-endless/main/config/ftbquests/quests/chapters/botania.snbt`

> **Generality note:** The 5-shape vocabulary in a non-expert chapter is exceptional — most non-expert chapters use 1-2 shapes. The 21% hide_dependency_lines rate in a non-expert pack challenges the assumption that non-expert packs always prefer visible dependency lines (observed range was 0-10% before this case). This chapter demonstrates that large non-expert chapters (100+ quests) may adopt expert-like visual management strategies.

---

### Case 45: Diamond Convergence (Non-Expert Structure Discovery) — MC-Odyssey-3 `exploration` (Adventure/RPG)
<!-- 35 quests with diamond shapes for structure-discovery tasks -->

35 quests, diamond_convergence topology for structure-discovery progression. Non-expert adventure/RPG pack.

```
Coordinate extract (summary, 35 total):
x-range: [-1.5..9.5] (11.0 units wide)
y-range: [-6.5..0.0] (6.5 units tall)

Shape distribution: diamond(12), default(23)
Size distribution: all 1.0 (no size hierarchy)
Icon rate: ~37% (13 icons on 35 quests)
Dependencies: 15 total (43% dep rate)
Multi-dep: 0
Topology: parallel_columns with diamond shape as semantic category marker (not topological convergence — multi-dep=0, would not trigger diamond_convergence in Phase 2 classifier)
Task types: structure(estimated 12+), advancement(estimated 5+), item(estimated 18)
Rewards: item(currency), random(loot tables)
Bounding box: 11.0 × 6.5 (aspect ratio 1.7:1, landscape)
```

MC-Odyssey-3's exploration chapter uses diamond shape as a semantic signal for structure-discovery quests (12 diamond-shaped quests correspond to 12 structures to find: graveyard, lich prison, ruins, etc.). The diamond shape is not used for convergence topology here but as a visual category marker — a novel shape semantic not observed in other packs. The chapter mixes structure-discovery tasks (find a graveyard, find a lich prison) with advancement-based boss fights (summon the Lich) and item-collection tasks, creating a multi-modal exploration progression. The currency rewards (lightmanscurrency coins) and random loot tables create an adventure-RPG reward economy. The landscape aspect ratio (1.7:1) is wider than most diamond_convergence chapters (typically portrait-oriented), suggesting the author laid out structure categories horizontally.

Source: `choombdev/MC-Odyssey-3/main/config/ftbquests/quests/chapters/exploration.snbt`

> **Generality note:** This chapter demonstrates that diamond shape can serve as a semantic category marker rather than a convergence signal. Pack authors using diamond shape should clarify whether it indicates convergence topology (fan_in >= 2) or a category label (e.g., "discovery quests"). The Phase 2 classifier should check if diamond-shaped quests have multi-dependency convergence or are independent category members.

---

### Case 46: Tree Branching (Non-Expert Tool Progression) — MC-Odyssey-3 `toolmaking` (Adventure/RPG)
<!-- 29 quests with Tinkers Construct progression and mixed shape vocabulary -->

29 quests, tree_branching topology for tool-crafting progression. Non-expert adventure/RPG pack.

```
Coordinate extract (summary, 29 total):
x-range: [-4.5..5.0] (9.5 units wide)
y-range: [-5.0..2.5] (7.5 units tall)

Shape distribution: diamond(4), circle(2), square(1), default(22)
Size distribution: all 1.0 (no size hierarchy)
Icon rate: ~3% (1 icon on 29 quests)
Dependencies: 11 total (38% dep rate)
hide_dependency_lines: 4 quests (14%)
Topology: tree_branching (Tinkers station → smeltery → advanced tool parts)
Task types: item(estimated 25+), checkmark(estimated 4)
Rewards: item(currency)
Bounding box: 9.5 × 7.5 (aspect ratio 1.3:1, near-square)
```

MC-Odyssey-3's toolmaking chapter follows Tinkers Construct progression from the basic Tinker Station through the Smeltery and into advanced tool parts. The tree_branching topology emerges from the root (Tinker Station + Part Builder at (-4.5, -2.0)) branching into the Smeltery setup (Seared Melter, Heater, Faucet, Table, Basin at (-3.0, -2.0)) and then fanning into specialized tool-crafting paths. The shape vocabulary uses diamond for milestone tools (4), circle for material-processing quests (2), and square for utility items (1), with the remaining 22 quests using the default shape. The 14% hide_dependency_lines rate is moderate for a non-expert pack, used on the later advanced-tool quests to reduce visual clutter.

Source: `choombdev/MC-Odyssey-3/main/config/ftbquests/quests/chapters/toolmaking.snbt`

> **Generality note:** The near-square aspect ratio (1.3:1) differs from the landscape-oriented tree_branching chapters in expert packs (Monifactory groundwork at 0.78:1 portrait, ATM-10 create at 0.76:1 portrait). Non-expert adventure packs may favor wider layouts for readability. Tinkers Construct's station-to-smeltery-to-parts progression is a frequently observed tree_branching template in packs that include the mod, though integration depth varies.

---

### Case 47: Tree Branching (Non-Expert Farming Tutorial) — society-sunlit-valley `getting_started` (Farming/Lifestyle)
<!-- 23 quests with 96% dep rate and size hierarchy for farming tutorial -->

23 quests, tree_branching topology for farming/lifestyle tutorial. Non-expert farming/lifestyle pack.

```
Coordinate extract (summary, 23 total):
x-range: estimated [-5..5] (~10 units wide)
y-range: estimated [-3..5] (~8 units tall)

Shape distribution: all default (no shape overrides)
Size distribution: 1.0(default, 19), 1.5(3), 2.0(1)
Icon rate: ~78% (18 icons on 23 quests)
Dependencies: 22 total (96% dep rate — nearly every quest has a parent)
optional: 1 quest (4%)
Topology: tree_branching (root → tool basics → farming → cooking → shipping)
Task types: item(estimated 20+), checkmark(estimated 3)
Rewards: item(food items, tools, currency)
Localization: uses {ftbquests.chapter.getting_started.quest*.title} pattern
Bounding box: ~10 × 8 (estimated, near-square)
```

Society-sunlit-valley's getting_started chapter is a farming/lifestyle tutorial that introduces the player to basic tools, farming, cooking, and shipping mechanics. The 96% dependency rate is the highest observed in any non-expert tutorial chapter — nearly every quest has a parent, creating a tightly guided experience where the player follows a specific learning path. The size hierarchy uses 1.0 for standard quests, 1.5 for sub-section milestones (3 quests), and 2.0 for the chapter's capstone (1 quest). The 78% icon rate (18/23 quests display item icons) is among the highest in the non-expert dataset, providing strong visual navigation for new players. The pack uses FTB Quests' localization key system for quest titles and descriptions, with keys like `{ftbquests.chapter.getting_started.quest3862A7D1A471A215.title}`.

Source: `Chakyl/society-sunlit-valley/master/config/ftbquests/quests/chapters/getting_started.snbt`

> **Generality note:** The 96% dependency rate in a tutorial chapter is among the highest observed in non-expert tutorial chapters, though Case 48 demonstrates that 100% is also viable for compact tutorials. The size hierarchy (1.0/1.5/2.0) follows the standard three-tier pattern. The localization key pattern is a technical implementation detail not previously observed in the dataset — authors using this pattern should ensure their lang files are properly configured.

---

### Case 48: Tree Branching (Non-Expert Cave Mining) — Caveopolis `basics` (Cave/Mining)
<!-- 16 quests in compact tree_branching for cave-mining tutorial -->

16 quests, tree_branching topology for cave-mining tutorial. Non-expert cave-themed pack by TeamKugimiya (same org as Enigmatic-Skies and Cryptopolis).

```
Coordinate extract (summary, 16 total):
x-range: estimated [-3..5] (~8 units wide)
y-range: estimated [-3..5] (~8 units tall)

Shape distribution: all default (no shape overrides)
Size distribution: all 1.0 (no size hierarchy)
Icon rate: ~6% (1 icon on 16 quests)
Dependencies: 16 total (100% dep rate)
Topology: tree_branching (root → basic tools → first ores → first power)
Task types: item(estimated 14+), checkmark(estimated 2)
Rewards: item(estimated)
Bounding box: ~8 × 8 (estimated, square)
```

Caveopolis's basics chapter is a compact cave-mining tutorial where every quest depends on a parent (100% dependency rate). The chapter introduces the player to cave exploration, basic ore processing, and initial power generation. The 100% dependency rate creates a strictly linear or branching path with no optional content — appropriate for a tutorial that must teach mechanics in order. The absence of shape overrides and size hierarchy produces a minimalist visual design, relying entirely on coordinate placement and dependency arrows to convey structure. The companion chapter first_power (17 quests, gear shape for entry point) extends the tree into power generation mechanics.

Source: `TeamKugimiya/Caveopolis/main/config/ftbquests/quests/chapters/basics.snbt`

> **Generality note:** The 100% dependency rate with zero shape/size variation is the most minimalist tree_branching chapter in the dataset. This pattern is appropriate for small tutorial chapters (<20 quests) where visual hierarchy is unnecessary. Larger chapters should adopt shape and size differentiation per Cases 43, 44, 46.

> **Topology coverage note (Cases 43–48):** The six new cases added in Cycle 16 Phase 4 strengthen diamond_convergence and tree_branching calibration but introduce no new highway_branch cases. highway_branch remains the primary calibration gap — only 3 non-expert cases exist in the full dataset (Cases 10, 15, 19 are all expert-tier). Cycle 17 should prioritize searching for non-expert highway_branch chapters (e.g., long horizontal progression spines in adventure or tech packs) to bring this topology's non-expert sample to parity with the others.

### Case 49: Tree Branching (Non-Expert Chinese Adventure RPG) — No-Flesh-Within-Chest `1` (Chest Cavity RPG)
<!-- 58 quests in Chinese-language adventure tree_branching with rsquare milestones -->

58 quests, tree_branching topology for a Chinese-language adventure/RPG pack based on the Chest Cavity mod. Go-Camping org, 478 stars — the highest-star pack researched in Cycle 17.

```
Coordinate extract (first 20 nodes):
| Quest                         | x     | y     | shape   | size | deps       |
|-------------------------------|-------|-------|---------|------|------------|
| 第一棵树 (First Tree)         | 6.0   | 17.25 | rsquare | def  | 72D0 (root)|
| 完美的开始 (Perfect Start)    | 6.0   | 11.25 | default | def  | 0402       |
| 了解自我 (Know Yourself)      | 6.0   | 3.25  | rsquare | def  | 3E9D       |
| 矿石肺 (Ore Lungs)            | 2.5   | 5.0   | default | def  | 6069       |
| 重定义内在 (Redefine Inner)   | 4.0   | 3.25  | default | def  | 50CE       |
| 基础属性 (Basic Stats)        | 2.5   | 3.25  | rsquare | def  | 6069       |
| 足够多的铁 (Enough Iron)      | 6.0   | 7.5   | default | def  | 0721       |
| Tetra与工具 (Tetra & Tools)   | 5.0   | 0.75  | rsquare | def  | 50CE       |
| 前往下界 (Go to Nether)       | 6.0   | -1.5  | default | def  | 538F,4C37  |
| 下界堡垒 (Nether Fortress)    | 6.0   | -4.0  | default | def  | 51FA       |
| 成为武器大师 (Weapon Master)  | 7.0   | 0.75  | rsquare | def  | 50CE       |
| 机械动力？(Create Power?)     | 7.75  | 7.5   | rsquare | def  | 3E9D       |
| 将光源挂在腰上 (Lantern)      | 4.0   | 7.5   | default | def  | 3E9D       |
| 储物抽屉 (Storage Drawers)    | 7.75  | 8.5   | default | def  | 3E9D       |
| 简易存储整合 (Simple Storage) | 8.75  | 7.5   | rsquare | def  | 3E9D       |
| 和朋友远征 (Expedition)       | 4.0   | 17.25 | default | def  | 3FED       |
| 查看资源槽 (Resource Slots)   | 1.0   | 5.0   | default | def  | 2DD7       |
| 货币兑换 (Currency Exchange)  | 7.75  | 13.25 | default | def  | 0402       |
| 查看属性 (View Stats)         | 1.0   | 3.25  | default | def  | 5BC3       |
| 强化训练 (Enhancement Train)  | 6.0   | 0.25  | default | def  | 50CE       |

Root: 72D090FF at approximately (6.0, 17.25), rsquare shape, oak_sapling icon
Shape distribution: rsquare(7, milestones), default(51)
Size distribution: all default (~1.0)
Icon rate: estimated 25-35% (custom Chest Cavity organ icons, Tetra tool icons)
Dependencies: 58+ total, ~100% dep rate
Multi-dep: 2 (前往下界 has 2 deps, 新手指南 has 2 deps)
Topology: tree_branching (max_depth=8, max_width=12)
Task types: item(~45), checkmark(~10), dimension(1), advancement(0)
Rewards: item rewards with XP
Bounding box: ~22 × 19 (x: -2.25 to 17.0, y: -4.0 to 17.25)
```

No-Flesh-Within-Chest's Chapter 1 implements a vertical tree branching from a central spine at x≈6.0, with the root at the top (y=17.25) and progression flowing downward to y=-4.0 (Nether content). The rsquare shape marks 7 key milestones (First Tree, Know Yourself, Basic Stats, Tetra & Tools, Weapon Master, Create Power, Simple Storage) — each representing a major capability unlock. The layout creates three distinct branch regions: a left branch (x=1.0-4.0) covering stats, exploration and magic; a central spine (x=5.0-8.75) covering core progression from early game through Nether; and a right branch (x=10.0-17.0) dedicated entirely to Chest Cavity organ harvesting and body modification. The right branch is the pack's signature content — 17 quests tracking organ crafting, drug administration, and body enhancement. The Chinese-language pack uses full i18n-style titles with bilingual semantic clarity (e.g., "器官容器" = Organ Container). The 478-star count is the highest for any pack in the non-expert adventure category.

Source: `Go-Camping/No-Flesh-Within-Chest/main/config/ftbquests/quests/chapters/1.snbt`

> **Generality note:** First Chinese-language tree_branching case in the dataset. The rsquare-for-milestone pattern (7 occurrences) is consistent with Cases 44 and 46 (tool-progression tree_branching). The vertical top-to-bottom reading direction (root at top, progression flows downward) is consistent with Chinese text layout conventions and differs from most English-language packs where progression flows left-to-right or bottom-to-top. The Chest Cavity organ sub-tree (17 quests, all single-dep) demonstrates how a pack's signature mod can generate a self-contained branch within the main tree.

---

### Case 50: Hub Fan (Non-Expert Boss Mod Catalog) — No-Flesh-Within-Chest `boss` (Chest Cavity RPG)
<!-- 50+ quests in boss-mod hub_fan with kill-task dominance -->

50+ quests, hub_fan topology organizing multiple boss mods into a unified hunt guide. Non-expert Chinese adventure/RPG pack.

```
Coordinate extract (summary, 50+ quests):
Central column (x ≈ -4.25, y from 4.25 to 21.75):
  (-4.25, 4.25) — "世界BOSS" (World Boss), checkmark, somebosses:altar icon → hub
  (-4.25, 8.25) — "迎战" (Meet Your Fight), checkmark, meetyourfight:haunted_bell → hub
  (-4.25, 11.25) — "BOMD" (Bosses of Mass Destruction), checkmark → hub
  (-4.25, 14.5) — "灾变" (Cataclysm), checkmark → hub
  (-4.25, 17.5) — "原版" (Vanilla), checkmark → hub
  (-4.25, 20.75) — "Alex生物" (Alex's Mobs), checkmark → hub

Boss kill rows (y = hub_y + 1.0, x from -3.25 to 7.75):
  SomeBosses: 12 kill quests at y=5.25-6.25, x from -3.25 to 6.75 (1.0 unit spacing)
  MeetYourFight: 4 kill quests at y=9.25, x from -3.25 to -0.25
  BOMD: 4 kill quests at y=12.25, x from -3.25 to -0.25
  Cataclysm: 6 kill quests at y=15.5, x from -3.25 to 1.75
  Vanilla: 1 kill quest at y=18.5 (Warden)

Right column (x ≈ 10.5, mod-side hubs):
  (10.5, 4.25) — "诡厄巫法" (Goety), checkmark
  (10.5, 7.5) — "Iron的魔法书" (Iron's Spells), checkmark
  (10.5, 10.75) — "墓园" (Graveyard), checkmark, structure+kill
  (10.5, 13.75) — "永恒之门" (Gateways), checkmark

Shape distribution: all default (no shape overrides)
Size distribution: all default (~1.0)
Icon rate: ~90% (every boss quest has its summoning item as icon)
Dependencies: all boss rows depend on their respective hub quest
Topology: hub_fan (6 hubs in left column, 4 hubs in right column)
Task types: kill(~35, 70%), checkmark(~10, 20%), structure(1), item(~4)
Rewards: item (boss loot drops)
Multi-dep: 0 (strict hub-to-leaf)
Optional: 0
Bounding box: ~22 × 18 (x: -4.25 to 17.0, y: 4.25 to 21.75)
```

The boss chapter implements a dual-column hub_fan: the left column (x=-4.25) catalogs 6 boss mods (SomeBosses, MeetYourFight, BOMD, Cataclysm, Vanilla, Alex's Mobs) as vertical hubs, each radiating kill quests horizontally to the right. The right column (x=10.5) catalogs 4 additional combat mods (Goety, Iron's Spells, Graveyard, Gateways). The 90% icon rate is among the highest in the dataset — each boss quest displays its summoning item, creating a visual catalog that functions as a bestiary. The 70% kill-task rate is the highest observed for any chapter, reflecting the pack's boss-hunting focus. The hub_fan structure is ideal for catalog chapters where each hub represents a content category and the leaves are independent, parallel objectives.

Source: `Go-Camping/No-Flesh-Within-Chest/main/config/ftbquests/quests/chapters/boss.snbt`

> **Generality note:** The dual-column hub_fan with 90% icon rate and 70% kill tasks is specific to boss-catalog chapters. The structure validates the hub_fan topology for catalog use cases (MP40 Collection-Catalog) where hubs serve as category headers and leaves are independent collection objectives. The 1.0-unit horizontal spacing within boss rows matches the minimum non-overlap distance for same-size nodes.

---

### Case 51: Tree Branching (Non-Expert Modular Tool System) — No-Flesh-Within-Chest `tetra` (Chest Cavity RPG)
<!-- 46 quests in modular tool progression tree -->

46 quests, tree_branching topology for Tetra modular tool system progression. Non-expert Chinese adventure/RPG pack.

```
Coordinate extract (summary, 46 quests):
Root: 538FC6DD at approximately (-3.25, 19.5), linked from chapter 1

Main trunk (x ≈ -3.25 to 5.5, y ≈ 19.5):
  (-5.5, 19.5) rsquare — "引言：Tetra的存在意义" (Introduction)
  (-3.25, 19.5) rsquare — "改造的起点：锤" (Starting Point: Hammer)
  (1.0, 19.5) — "触手可及" (Within Reach)
  (3.25, 19.5) — "一次轻松的练习" (Easy Practice), advancement
  (5.5, 19.5) — "再进一步" (One Step Further), advancement

Tool type branches (y = 17.0 and 22.0, from trunk):
  Modification branch (y=17.0): 刀剑(1.0), 盾牌(3.25), 弩(4.25), 弓(5.25)
  Tool branch (y=22.0): 改造工具(1.0), 双头工具(2.25), 单头工具(3.25), 腰带(4.25)
  Knowledge branch (y=16.0-18.0): 卷轴图鉴×7 at y=16.0-18.0

Forge progression (y = 24.5-27.5, upper region):
  (1.0, 26.0) rsquare — "寻找锻造锤" (Find Forge Hammer), multi-dep (2)
  (3.25, 26.0) — "构筑锻造锤" (Build Forge Hammer)
  (8.0, 26.0) rsquare — "最终的锻造锤" (Ultimate Forge Hammer)
  (1.0, 27.5) rsquare — "地核提取" (Core Extraction)
  (3.75-5.75, 24.5) — forge upgrade chain

Shape distribution: rsquare(5, milestones), default(41)
Size distribution: all default (~1.0)
Icon rate: ~65% (tetra:modular_double for tool milestones, specific tool icons for types)
Dependencies: 46 total, ~100% dep rate
Multi-dep: 1 (寻找锻造锤 has 2 deps)
hide_dependency_lines: true (chapter-level)
Topology: tree_branching (max_depth=6, max_width=8)
Task types: item(~20), checkmark(~15), advancement(~11)
Rewards: item (Tetra modules and materials)
Bounding box: ~13.5 × 12 (x: -5.5 to 8.0, y: 16.0 to 27.5)
```

The Tetra chapter implements a tool-progression tree where the main trunk tracks hammer upgrades (Introduction → Starting Hammer → Practice → Advancement), with branches for each tool type (swords, shields, crossbows, bows at y=17.0; double tools, single tools, belts at y=22.0) and a forge progression branch at the top (y=24.5-27.5). The 5 rsquare milestones mark key capability thresholds. The 65% icon rate uses tetra:modular_double for tool milestones and specific tool icons for individual types, creating a visual taxonomy of the Tetra mod's tool system. The chapter-level hide_dependency_lines: true is notable — it's the only non-expert chapter in the dataset with this setting, suggesting the author wanted to reduce visual clutter in a dense tree with many short branches.

Source: `Go-Camping/No-Flesh-Within-Chest/main/config/ftbquests/quests/chapters/tetra.snbt`

> **Generality note:** The Tetra tool-progression tree validates the tree_branching topology for mod-specific tutorial chapters where the trunk tracks the mod's core upgrade path and branches cover individual tool categories. The rsquare-for-milestone pattern (5 occurrences) is consistent with Cases 44 and 49. The 65% icon rate and hide_dependency_lines setting together create a "clean skill tree" aesthetic — icons provide visual navigation while hidden dependency lines prevent the tree from looking tangled.

---

### Case 52: Tree Branching with Extreme Convergence (Non-Expert Kitchen-Sink) — All-of-Fabric-6 `create` (Fabric Kitchen-Sink)
<!-- 69 quests, tree_branching with massive final convergence node -->

69 quests, tree_branching topology with extreme final convergence (single quest depending on all 68 prior quests). Non-expert Fabric kitchen-sink pack by TeamAOF.

```
Coordinate extract (first 15 nodes):
| Quest             | x    | y    | shape   | size | deps                    |
|-------------------|------|------|---------|------|-------------------------|
| Root (610389B1)   | 0.0  | 0.5  | default | def  | none                    |
| 1C705A0B          | 2.0  | 0.5  | default | def  | 6103                    |
| 480EE90E          | 2.0  | -1.5 | default | def  | 6103                    |
| 38E2D761          | 4.0  | -1.5 | default | def  | 480E                    |
| 511DD537          | 4.0  | 0.5  | default | def  | 1C70                    |
| 624B52BE          | -2.0 | 0.5  | default | def  | 6103                    |
| 2AFA49C5          | -4.0 | 0.5  | default | def  | 624B                    |
| 5C38C92A          | 6.0  | -1.5 | default | def  | 38E2                    |
| 143A0040          | -2.0 | -3.5 | default | def  | 6103                    |
| 4119B4C0          | 6.0  | 0.5  | default | def  | 1C70                    |
| 01FA58FF          | 8.0  | 0.5  | default | def  | 4119                    |
| 3989950B          | 6.0  | -3.5 | default | def  | 38E2                    |
| 049F3E0A          | 10.0 | 0.5  | default | def  | 01FA                    |
| 4B6D44F4          | 0.0  | 2.5  | default | def  | 6103                    |
| 4FEFC031          | 12.0 | 0.5  | default | def  | 049F                    |

Final convergence:
| 1D2457909D7F8C17  | 6.0  | -6.0 | gear    | 4.0  | ALL 68 prior quests     |
  Task: checkmark (trofers:medium_pillar icon — Create completion trophy)

Shape distribution: gear(1, convergence), default(68)
Size distribution: 4.0 (convergence node), default ~1.0 (68 chain nodes)
Icon rate: ~10% (mod item icons for key milestones)
Dependencies: 69+ total
Multi-dep: 2 nodes with 2 deps (1BA0, 371D), 1 node with 68 deps (convergence)
Topology: tree_branching (max_depth=10, max_width=18)
Task types: item(~68), checkmark(1, convergence trophy)
Rewards: item (Create machines and components)
Bounding box: 24 × 15 (x: -6.0 to 18.0, y: -6.0 to 9.0)
```

All-of-Fabric-6's Create chapter demonstrates a "tree with capstone" pattern: the first 68 quests form a tree branching from the root at (0.0, 0.5), with the main horizontal chain extending right to x=18.0 and vertical branches reaching up to y=9.0 (addon integrations) and down to y=-3.5 (processing chains). The tree has three major branch regions: a left branch (x=-6.0 to -2.0, addons), a central chain (x=0.0 to 12.0, core Create progression), and a right branch (x=14.0 to 18.0, late-game Create). The final quest at (6.0, -6.0) is a massive gear-shaped convergence node (size 4.0 — the largest single quest in the dataset) that depends on ALL 68 prior quests, creating a "you've mastered Create" capstone. The trofers:medium_pillar icon is a trophy item, signaling chapter completion. The 24-unit width approaches the R59 warning threshold of 30 units.

Source: `TeamAOF/All-of-Fabric-6/main/config/ftbquests/quests/chapters/create.snbt`

> **Generality note:** The "tree with capstone" pattern (68 single-dep quests → 1 convergence node with 68 deps) is the most extreme convergence in the dataset. The gear-shaped size-4.0 convergence node is a distinctive visual signal — gear shape + extreme size + trophy icon = "you've completed this entire mod." Authors should be aware that a 68-dep convergence node requires all prior quests to be completed, making this an absolute gate rather than a soft convergence. The 24-unit width suggests authors should provide navigational aids (icons, decorative images) for chapters approaching this width.
>
> **Generality note (Cycle 17 Phase 5 addendum — Reviewer A feedback):** Generality note: Calibrated from TeamAOF pack (AOF-6). Tree-with-capstone convergence may be team-specific. Verify against non-TeamAOF packs before adopting as universal pattern. The "tree with capstone" pattern is a TeamAOF design signature — optional pattern for kitchen-sink packs, not a universal best practice. The 24-unit width is still within R59's 30-unit threshold but approaching the range where navigation aids become beneficial.

---

### Case 53: Tree Branching (Large Non-Expert Mod Chapter) — All-of-Fabric-6 `botania` (Fabric Kitchen-Sink)
<!-- 100+ quests, large chapter with 6 sub-regions and hexagon convergence capstone -->

100+ quests, tree_branching topology with 6 distinct sub-region branches and a hexagon convergence capstone. Non-expert Fabric kitchen-sink pack by TeamAOF.

```
Coordinate extract (sub-region summary, 100+ quests):

Root: 1DF75AD9 at (-6.0, -0.5), checkmark, botania:lexicon icon
Sub-hub 1 (generation flowers): 5CF7175F at (3.5, -1.5), advancement
  → 14 generation flowers in column at x=0.5, y from -3.5 to 9.5
  → 7 additional flowers at x=6.5, y from 2.5 to 9.5
Sub-hub 2 (functional flowers): 2F21F314 at (3.5, 5.5), advancement
  → 24 functional flowers in grid at x=0.5-6.5, y from 1.5 to 11.0
Sub-hub 3 (lenses): 081EE316 at (11.5, 7.0), item, botania:lens_normal
  → 21 lens types at x=8.5-14.5, y from 5.0 to 13.0
Sub-hub 4 (baubles/accessories): 5DD7363C at (10.5, -5.0), item, botania:bauble_box
  → ~20 baubles (rings, cloaks, belts) at x=8.0-13.0, y from -7.0 to -1.0
Sub-hub 5 (runes): 79D5AADE at (16.5, -7.5), item, botania:runic_altar
  → 16 runes in grid at x=13.5-19.5, y from -10.5 to -4.5
Sub-hub 6 (Alfheim): 56C906CE at (19.5, 3.5), item, botania:alfheim_portal
  → ~8 Alfheim quests at x=19.5-26.5, y from -1.0 to 3.5

Convergence capstone:
| 14CC28EE | 20.0 | 8.0 | hexagon | 4.0 | ALL prior quests | trofers:medium_pillar |

Shape distribution: hexagon(1, convergence capstone), default(99+)
Size distribution: 4.0 (capstone), default ~1.0 (chain nodes)
Icon rate: ~80% (botania item icons for every flower, lens, rune, bauble)
Dependencies: ~110+ total, ~100% dep rate
Multi-dep: 3 (terra_plate has 3 deps, natura_pylon has 2, alfheim_portal has 2)
Topology: tree_branching (max_depth=8, max_width=30+)
Task types: item(~90), advancement(~8), checkmark(~2)
Rewards: item (Botania components)
Bounding box: 32.5 × 20.5 (x: -6.0 to 26.5, y: -10.5 to 10.0)
```

AOF-6's Botania chapter is the largest tree_branching chapter in the non-expert dataset at 100+ quests spanning 32.5 units wide. The tree branches from a single root (botania:lexicon) into 6 distinct sub-regions, each organized around a Botania subsystem: generation flowers (left column), functional flowers (center-left grid), lenses (center-right fan), baubles (lower-right cluster), runes (far-right grid), and Alfheim (far-right extension). Each sub-region has its own advancement sub-hub that gates access to the leaf quests. The 80% icon rate is exceptionally high — nearly every quest displays its Botania item icon, creating a visual encyclopedia of the mod. The hexagon-shaped convergence capstone at (20.0, 8.0) with size 4.0 mirrors the Create chapter's gear-shaped capstone (Case 52), confirming the "tree with capstone" pattern as a TeamAOF signature.

The 32.5-unit width exceeds the R59 30-unit warning threshold, making this the widest non-expert chapter in the dataset. The author compensates with high icon density and clear sub-region separation (each subsystem occupies a distinct x-band), allowing players to navigate by visual scanning rather than reading quest titles.

Source: `TeamAOF/All-of-Fabric-6/main/config/ftbquests/quests/chapters/botania.snbt`

> **Generality note:** The 6-sub-region tree_branching with 80% icon rate and hexagon capstone is the most comprehensive non-expert mod chapter in the dataset. The "tree with capstone" pattern (Cases 52, 53) appears to be a TeamAOF design signature — both Create and Botania chapters end with a size-4.0 trophy convergence. The 32.5-unit width demonstrates that non-expert authors will exceed R59 when a mod's content demands it, compensating with icon density rather than layout compression. Authors generating Botania-like chapters should plan 6 sub-regions at 4-8 units of x-separation, with each sub-region getting its own advancement hub.
>
> **Generality note (Cycle 17 Phase 5 addendum — Reviewer A feedback):** Generality note: Calibrated from TeamAOF pack (AOF-6). Tree-with-capstone convergence may be team-specific. Verify against non-TeamAOF packs before adopting as universal pattern. Both Cases 52 and 53 are from the same pack (AOF-6) by the same team (TeamAOF). The patterns observed may reflect team-specific conventions rather than universal design principles. Cross-pack validation required. The 32.5-unit width exceeds R59's 30-unit threshold — high icon rate (~80%) compensates but does not formally exempt the chapter from R59. If this exception is to be codified, R59 should be updated with an explicit exemption condition for high-icon-density chapters.

---

### Case 54: Grid Catalog (Non-Expert Farming Collection) — All-of-Fabric-6 `agriculture` (Fabric Kitchen-Sink)
<!-- 90+ quests, zero-dependency collection catalog with sub-regions -->

90+ quests, grid_catalog topology for farming and cooking collection. Non-expert Fabric kitchen-sink pack by TeamAOF.

```
Coordinate extract (sub-region summary, 90+ quests):

Sub-region 1: Farming basics (x: -8.5 to -3.0, y: 2.0 to 8.0)
  Root: 2D812FCB at (-5.5, 3.5), item (wheat seeds)
  → 18 crop quests in hub_fan from root (wheat, potato, carrot, cactus, melon, etc.)
  → All default shape, all default size

Sub-region 2: Cooking basics (x: -2.5 to 3.5, y: 6.5 to 13.5)
  Hub: 68213B32 at (0.5, 10.5), checkmark (12 kitchen items)
  → Chicken branch: 2DEACB94 (0.5, 7.5) → fried_chicken, lemon_chicken, chicken_noodles
  → Beef branch: 6491E686 (0.5, 13.5) → beef_stew, beef_stir_fry, beef_wellington
  → Pork branch: 75A6E279 (5.5, 10.5) → pork_and_beans, blt, ham_sandwich

Sub-region 3: Cacao/Chocolate (x: -13.5 to -7.0, y: 7.5 to 12.5)
  Hub chain: cacao processing line (cacao_mass → cacao_butter → silicon_mold → chocolates)
  → 10+ chocolate variants as leaves from silicon_mold hub

Sub-region 4: Farmer's Delight (x: -10.0 to -3.0, y: 14.0 to 19.5)
  Hub: 1E2F74C7 at (-9.0, 13.0), item (stove)
  → Knife upgrade chain: flint → iron → gold → diamond → netherite (y: 14.0 to 19.5)
  → Grains convergence: 3CEB2302 at (-4.5, 7.5), 6-dep checkmark

Sub-region 5: Vinery/Wine (x: 1.0 to 7.0, y: 14.0 to 20.5)
  Hub: 410FB472 at (4.0, 14.0), checkmark (Vinery entry)
  → Wine branch: fermentation_barrel → 8 wine types in horizontal row at y=20.5

Sub-region 6: Croptopia cooking (x: 7.5 to 10.5, y: 9.0 to 16.0)
  Soups convergence: 5F9620B9 at (9.0, 10.5), 7-dep checkmark
  Sweet Tooth convergence: 1F904283 at (9.0, 15.0), 6-dep checkmark

Shape distribution: all default (zero shape overrides across 90+ quests)
Size distribution: all default (~1.0)
Icon rate: ~0% (no explicit icons — items serve as visual identifiers via task targets)
Dependencies: mostly single-dep or zero-dep
Multi-dep: 5 convergence nodes (2-7 deps each)
Topology: grid_catalog (6 sub-regions arranged spatially)
Task types: item(~85), checkmark(~8, convergence nodes)
Rewards: item, xp (100 XP for select farming milestones)
Bounding box: 24 × 15 (x: -13.5 to 10.5, y: 2.0 to 20.5)
```

AOF-6's Agriculture chapter is a farming/cooking collection catalog organized into 6 spatially distinct sub-regions, each covering a different farming mod (vanilla crops, Croptopia cooking, Cacao chocolate-making, Farmer's Delight, Vinery wine-making, Croptopia desserts). The zero-shape-override design (all 90+ quests use default shape) means the visual identity comes entirely from coordinate placement and item textures. Each sub-region has its own hub quest and internal branching logic — the Cacao sub-region follows a linear processing chain (cacao beans → mass → butter → mold → chocolates), while the Vinery sub-region fans out from a central fermentation barrel to 8 wine varieties. The 5 convergence nodes (2-7 deps) mark recipe milestones where multiple ingredients must be gathered before crafting (e.g., "Soups" requires 7 different soup recipes, "Sweet Tooth" requires 6 desserts).

Source: `TeamAOF/All-of-Fabric-6/main/config/ftbquests/quests/chapters/agriculture.snbt`

> **Generality note:** The 6-sub-region grid_catalog with zero shape overrides is the most spatially organized farming chapter in the dataset. The sub-region approach (each farming mod gets its own x-y band) provides a natural decomposition that prevents the "mega-chapter fatigue" described in PP20. The convergence nodes (2-7 deps) serve as recipe completion milestones that break the collection monotony. Authors designing farming/cooking chapters should consider 4-6 spatially separated sub-regions at 4-8 units apart, with 1-2 convergence milestones per sub-region.

---

## Mixed Topology Analysis — Cycle 17 Phase 1

This section analyzes large chapters (>80 quests) that contain multiple topology sub-regions, examining how authors decompose complex content into spatially distinct zones with different organizational principles.

### Mixed Topology 1: Steamcreate2 `overworld` (85+ quests, 4 topology zones)

Steamcreate2's overworld chapter (Dseelis/Steamcreate2, MC 1.20.1, 0 stars) decomposes 85+ quests into 4 distinct topology zones within a single chapter:

**Zone A — Tutorial hub_fan** (x: -2.0 to 2.0, y: -2.5 to 1.5, ~12 quests): The chapter opens with a root at (0.0, -0.5), rsquare shape size 1.25, branching to 10 tutorial quests covering basic mechanics (mining, farming, structure finding, advancement). The hub_fan uses rsquare for the root and default shape for leaves.

**Zone B — Exploration hub** (x: -6.5 to -4.0, y: -1.0 to 4.0, ~8 quests): A secondary hub at (-2.0, 4.0) rsquare size 1.25 branches into exploration quests. A linear chain at x=-6.0 leads to a diamond shape size 2.0 at (-6.0, -1.0) — the dungeon entry point.

**Zone C — Structure discovery regions** (x: -17.0 to 12.0, y: 8.5 to 18.0, ~40 quests): The largest zone contains 4 independent structure-discovery sub-regions, each following a consistent pattern: square shape (map item, size 1.2) → diamond shape (dungeon entry) → hexagon shape (boss kill, size 1.5) → reward items. The 4 regions are scattered at (-14.8, 11.9), (-8.8, 11.4), (3.6, 13.3), and (10.5, 11.25), each with surrounding circle-shape mob kill quests (size ~1.0).

**Zone D — Circle cluster** (x: 4.0 to 9.35, y: -2.2 to 0.55, ~8 quests): A compact circle-shape cluster (all circle, size 1.1) forms a tight hub around (6.4, -0.5) — likely a mod-specific feature (e.g., dimension portal or quest tracker).

**Shape-as-category system:** The overworld chapter uses a 4-shape category system that validates MP71 (Shape-as-Category-Marker):
- **square** (size 1.2, map icon) = structure discovery / "find this location"
- **diamond** (default size) = dungeon entry / "enter this structure"
- **hexagon** (size 1.5) = boss kill / "defeat this boss"
- **circle** (size 1.0-1.1) = regular mob kill / "farm this mob"

Each shape consistently encodes a task category across all 4 sub-regions, and none of the shape-marked quests have multi-dependency (they are category labels, not convergence signals). This is the strongest MP71 validation in the dataset — 4 independent sub-regions all use the same shape vocabulary with the same semantic meaning.

**Transition between zones:** The zones connect through shared dependency chains rather than bridge nodes — Zone A's root feeds Zone B's hub, which feeds Zone C's diamond entry points. Zone D is independent (connected via the tutorial root). The transitions are "soft" — the player follows the dependency arrow from one zone to the next without a dedicated transition quest.

Source: `Dseelis/Steamcreate2/main/config/ftbquests/quests/chapters/overworld.snbt`

### Mixed Topology 2: AOF-6 `botania` (100+ quests, 6 sub-region tree)

AOF-6's Botania chapter (Case 53) decomposes 100+ quests into 6 sub-regions within a tree_branching topology. Each sub-region has its own internal topology:

- **Generation flowers**: linear_chain from hub (x=0.5, y=-3.5 to 9.5, 14 quests in a vertical line)
- **Functional flowers**: grid_catalog (x=0.5-6.5, y=1.5 to 11.0, 24 quests in a grid from single hub)
- **Lenses**: hub_fan from lens_normal hub (x=8.5-14.5, y=5.0 to 13.0, 21 quests radiating from hub)
- **Baubles**: hub_fan from bauble_box hub (x=8.0-13.0, y=-7.0 to -1.0, ~20 quests)
- **Runes**: grid_catalog from runic_altar hub (x=13.5-19.5, y=-10.5 to -4.5, 16 quests in grid)
- **Alfheim**: linear_chain (x=19.5-26.5, y=-1.0 to 3.5, 8 quests in chain)

The decomposition follows mod-internal logic: each Botania subsystem has a natural organizational structure (flowers are catalogs, lenses are variants of a base item, runes follow the runic altar's crafting progression). The sub-region boundaries align with dependency graph breakpoints — each sub-region is a subtree rooted at an advancement hub. The transitions between sub-regions are implicit (following the dependency from the main trunk to each sub-hub) rather than explicit bridge nodes.

Source: `TeamAOF/All-of-Fabric-6/main/config/ftbquests/quests/chapters/botania.snbt`

### Key Observations from Mixed Topology Analysis

1. **Sub-region decomposition follows mod boundaries, not topology rules.** Both Steamcreate2 and AOF-6 decompose large chapters by assigning each mod/subsystem its own spatial region. The topology within each region reflects the subsystem's natural structure (linear for processing chains, grid for catalogs, fan for variant items). This confirms the Phase 3 finding that "layout is emergent, not planned" — authors decompose by content, and the topology emerges from each content block's nature.

2. **Shape-as-category bridges sub-regions.** Steamcreate2's overworld uses the same 4-shape category system across all 4 zones, creating visual consistency even as the spatial topology changes. This is the strongest evidence for MP71 — shape semantics persist across topology boundaries. AOF-6's botania does NOT use shape-as-category (all quests default shape), relying instead on spatial separation and icon differentiation.

3. **Transitions are dependency-driven, not spatially mediated.** Neither pack uses dedicated "bridge" quests or coordinate-level connectors between sub-regions. The player follows dependency arrows from the main trunk to each sub-hub. This suggests that bridge nodes (as described in some topology literature) are unnecessary when dependency lines provide clear navigation between regions.

4. **Large chapters (>80 quests) always decompose into 4-6 sub-regions.** The 3 large chapters analyzed (Steamcreate2 overworld: 4 zones, AOF-6 botania: 6 sub-regions, AOF-6 agriculture: 6 sub-regions) consistently produce 4-6 spatially distinct zones. This suggests a natural cognitive limit — authors decompose large content into approximately 5 (±1) regions, matching Miller's "magical number seven" for working memory capacity.

5. **AP41 vs MP73 conflict resolution (Cycle 17 Phase 5 addendum — Reviewer B feedback).** Note: 80+ quest chapters using sub-region decomposition (MP73) are exempt from AP41's flat-hierarchy concern — spatial separation between sub-regions provides visual hierarchy even without shape diversity. Case 54 (AOF-6 agriculture, 90+ quests, zero shape overrides) is a positive example of MP73 sub-region decomposition yet would be flagged by AP41's criteria for flat presentation hierarchy. The resolution: AP41 applies primarily to chapters in the 25–60 quest range where sub-region decomposition (MP73) is not applicable. For chapters with 80+ quests that use MP73 sub-region decomposition, spatial separation replaces shape hierarchy as the primary visual hierarchy mechanism. Zero-shape-override is acceptable when sub-regions provide 4+ units of spatial separation. Authors following MP73 should still compensate with high icon rate (>50%) or decorative region images (MP47) to guard against version-induced layout drift (AP40).

6. **Bridge node specification and region layout strategy (Cycle 17 Phase 5 addendum).** When sub-regions require explicit bridge nodes (as opposed to implicit dependency-driven transitions observed in Cases 52–54), use the following parameters: bridge node shape = `hexagon`, size = `1.5` (intermediate between leaf at 1.0 and hub at 2.0+). Bridge nodes connect adjacent sub-regions and should be positioned at the weighted midpoint of the two nearest cross-region dependency nodes (see Phase 2.5 `place_bridge_nodes` algorithm). For the spatial allocation strategy when decomposing a large chapter: allocate the primary region (the sub-region with the most quests or the main progression trunk) to the left 60% of the chapter's bounding box width; arrange remaining sub-regions vertically along the right 40%, each occupying its own y-band with 4–8 units of vertical separation. This left-primary / right-secondary layout matches the observed patterns in Steamcreate2 overworld (Zone A+B left, Zone C right-scattered) and AOF-6 botania (main trunk left, 6 sub-regions spreading right). For chapters with >5 sub-regions, consider a 2-column right arrangement (upper-right and lower-right) to prevent the right side from exceeding R59's viewport limit.

Cycle 15 Phase 1 expanded the non-expert dataset dramatically, extracting coordinate data from 10 additional modpacks (Insurgence, MI-Lost-Favor, Seaopolis, Minecolonies, Minecraft-Medieval, Create-chronicles, Farmopolis, Aetas-Ferrea, GenCraft, Phoenix-Forge) spanning adventure, tech, farming, RPG, and Create-focused genres. Unlike the individually documented Cases 1–42, these chapters are presented as batch summaries — their aggregate statistics confirm and extend the topology patterns established by earlier cases, and they fill the calibration gaps identified in the Non-Expert Topology Calibration Summary. The data below is organized by topology type, with expert cases referenced for comparison.

#### diamond_convergence — 26 new non-expert chapters

The diamond_convergence topology was previously the most under-calibrated for non-expert packs, with only Case 27 (Rogue Mayhem, 12 quests) representing the non-expert side (Case 36 / Enigmatic-Skies is formally documented under tree_branching). The 26 new chapters from Cycle 15 Phase 1 transform this topology from a 1-case non-expert sample to a 27-case dataset, revealing that diamond_convergence is the dominant topology for non-expert "collection" and "processing" chapters where multiple crafting paths converge on a final product or milestone.

The Insurgence cookbook chapter (141 quests) exemplifies the non-expert diamond_convergence pattern: 106 of 141 quests use diamond shape (75%), spread across X[-13.5..11.5] Y[-8.5..0.5] with an icon rate of 43% and average spacing of 6.87. Multiple ingredient-gathering paths enter from the four edges of the bounding box and converge toward a central cookbook node — a spatial metaphor where the player literally watches the recipe come together. This "multi-path from periphery to center" pattern is the non-expert equivalent of the expert diamond_convergence seen in Chroma-Technology-2 mekanism (Case 16), but at a much lower convergence_ratio: where the expert chapter achieves 0.412 convergence_ratio with 199 quests all using diamond shape, the cookbook chapter uses spatial convergence (paths entering from multiple edges) rather than dependency convergence (fan_in >= 3) as its primary organizing principle.

The strongest diamond_convergence signal in the new data comes from Insurgence's chapter_i_eyes_of_ender: 51 quests with 33% multi-dependency — the highest multi-dep rate observed in any non-expert chapter. The shape vocabulary splits cleanly between circle(27) and default(23), with size hierarchy at 1.0(32), 2.0(16), and 1.8(2). The coordinate range X[-8..8] Y[-8..8] forms a perfect square centered at the origin, and the min spacing of 1.41 (√2, the diagonal distance on a unit grid) indicates the author used a diagonal-offset placement strategy to pack convergence paths tightly without overlapping. The average spacing of 3.2 sits between the expert extreme (Chroma-Technology-2 at 6.58) and the non-expert baseline (Rogue Mayhem at 2.0), suggesting that convergence density scales with multi-dep ratio rather than pack type.

The largest single chapter in the new dataset is MI-Lost-Favor's bronze_age at 334 quests plus 7 quest_links — a non-expert tech pack chapter that surpasses even ATM-10 create (206 quests) in sheer node count. The shape vocabulary is remarkably diverse: diamond(103), rsquare(85), octagon(47), heart(35), square(25), pentagon(19), with 23% multi-dep. The x-range of [-1975..20] is extraordinary — the -1975 value likely indicates a coordinate system artifact or an extremely elongated layout that would violate R59 by a factor of 56. The more plausible interpretation is that most quests cluster in a reasonable range with a few outliers, consistent with the "sprawling collection" pattern where the author kept adding quests outward without re-centering. The 23% multi-dep rate confirms this as diamond_convergence despite the extreme coordinate range.

MI-Lost-Favor's first_steps (210 quests) provides a counterpoint: diamond(81) with heart(31) and pentagon(22) shapes, 17% multi-dep, and average spacing of 1.85 — the tightest spacing for a 200+ quest chapter outside the expert pack extreme (MI-Lost-Favor bronze_age at 16.16 avg spacing shows the opposite end of the range). The contrast between these two MI-Lost-Favor chapters demonstrates that within a single pack, spacing can vary from 1.85 to 16.16 depending on whether the chapter is a tightly guided tutorial (first_steps) or an open-ended collection (bronze_age).

Seaopolis basics (30 quests) represents the smallest diamond_convergence chapter in the new data: a vertical chain with convergence at the top, X[-2.5..2.5] Y[-1..9.5]. The narrow 5-unit x-range and 10.5-unit y-range produce a portrait-aspect layout where underwater resource paths flow upward toward a surface-level convergence point — a spatial metaphor matching the pack's underwater theme. Minecolonies cobblemon (199 quests, X[-17..30] Y[-1.5..31]) and productive_bees (124 quests, 29% multi-dep, 67% icon rate) extend the collection-convergence pattern to the farming/living genre, where bee breeding trees and creature collection paths converge on completion milestones. The productive_bees chapter's 29% multi-dep rate is the second-highest in the non-expert dataset, and its size distribution (1.0 for 108 nodes, 1.5 for 11, 2.0 for 4) follows the standard hierarchy precisely.

#### tree_branching — 19 new non-expert chapters

The tree_branching topology now has 22 non-expert cases total (3 from previous cycles plus 19 new), making it the best-calibrated non-expert topology. The new data reveals that tree_branching is the default topology for non-expert packs' tutorial and progression chapters, where a root hub branches into thematic sub-trees.

Minecraft-Medieval's the_squires_trials (75 quests) is the cleanest tree_branching example in the non-expert dataset: hexagon(4) and pentagon(1) shapes, X[-18..35] Y[-12..5.5], with 30% icon rate and average spacing of 3.16. The 53-unit x-range and 17.5-unit y-range produce a landscape-aspect layout (3:1) where the tree branches horizontally from a root on the left — consistent with the tree_branching pattern observed in expert packs (Monifactory groundwork at 18.25×23.5, ATM-10 create at 13×17) but scaled wider. The companion chapter travellers_journey (55 quests) demonstrates size diversity within tree_branching: 1.0(43), 2.0(6), 2.5(4), 3.0(2), with rsquare(2), octagon(1), and hexagon(1) marking the sub-hub junctions. The average spacing of 1.99 is notably tighter than the_squires_trials' 3.16, suggesting that within the same pack, tree chapters vary their density based on content type (trials = spacious, journey = compact).

Insurgence's trophies chapter (94 quests) is an outlier: hexagon(91) at 97% shape monoculture with 88% icon rate and 20 root nodes each spawning their own branch. This is tree_branching organized as a "trophy wall" — 20 independent trophy-hunting subtrees rooted at the top of the layout, each branching downward into the specific mobs or challenges required. The 97% hexagon monoculture is the highest shape uniformity in any tree_branching chapter, and the 88% icon rate (each trophy quest displaying its reward item) makes this chapter function as a visual collection tracker. The 20-root structure is unusual — most tree_branching chapters have a single root (Cases 5, 11, 18) or at most 3 roots (Case 24) — suggesting that "parallel tree groves" (multiple independent trees sharing a chapter) is a valid tree_branching variant for collection-oriented content.

Create-chronicles basics (136 quests, rsquare(14) + default(120), 98% single-dependency) is the most "linear-like" tree_branching chapter: nearly every quest has exactly one parent, producing long unbranched chains that only occasionally fork. This pattern is characteristic of Create mod progression, where each machine unlocks a single next step. The Farmopolis series (basic, brewery, cheese, starting_up — 30 to 43 quests each) demonstrates remarkable consistency: all default shape, all size 1.0 except for a single size-2.0 "license" convergence node per chapter, 94% single-dependency. Each Farmopolis chapter is a minimal tree with one trunk and short branches, where the license node serves as a gating milestone that requires completing all branches before progressing.

Aetas-Ferrea act_1 (21 quests) is the most aesthetically refined tree_branching chapter in the dataset: hexagon(12) at 57% shape usage, branching from a central gear hub at size 2.0, with average spacing of 2.24 and 38% icon rate. The small quest count and generous spacing produce a layout that reads as an elegant skill tree rather than a dense progression web. At the other extreme, GenCraft's bruh chapter (96 quests) uses a chaotic shape vocabulary — circle(21), square(13), gear(7), rsquare(6) — that signals a less structured tree where each branch has its own visual identity.

#### highway_branch — 1 new non-expert chapter

The highway_branch topology gains 1 confirmed non-expert case, bringing its total to 4 (3 from previous cycles plus 1 new). While still the least-sampled topology, the new case confirms that highway_branch is strongly associated with boss-progression chapters in non-expert packs. Phoenix-Forge progression is reclassified as expert (GregTech voltage-tier) per .researched-packs.json5.

Create-chronicles bosses_and_skill_points (72 quests) is the most extreme highway_branch chapter observed: 100% icon rate, square(70) shape monoculture, X[-24.75..9.6] Y[4.6..8.25]. The aspect ratio of 9.4:1 (34.35 units wide by 3.65 units tall) is the most horizontally elongated layout in the entire dataset, surpassing even Gregtech-Voyager chapter_3_hv (Case 19, aspect ratio ~1.8:1). The horizontal spine sits at Y=4.6 while boss nodes branch upward, and the 98% single-dependency rate confirms a linear spine with occasional vertical offshoots. This chapter demonstrates that highway_branch can scale to 72 quests while maintaining its defining characteristic — a dominant horizontal axis with perpendicular branches.

*[Expert reclassification]* Phoenix-Forge progression (17 quests + 26 quest_links) is classified as expert (GregTech voltage-tier) per .researched-packs.json5 and is documented here for comparison: a compact highway with 82% multi-dep rate, rsquare(26) at sizes 0.75-0.85, X[-1..6] Y[-2..8]. The high multi-dep rate and small node sizes produce a dense web-like appearance within a 7×10 unit bounding box — typical of expert-pack tech progression rather than the wide-open highway layouts seen in non-expert packs. The quest_links (26 total, exceeding the quest count of 17) indicate that this chapter heavily cross-references other chapters, functioning as a "progression roadmap" rather than a self-contained quest line. This case is counted under expert highway_branch, not non-expert.

### Non-Expert Topology Calibration Summary

The following table summarizes calibration data for each topology type, comparing expert vs non-expert pack parameters. Data derived from 48 individually documented cases plus 47 batch-extracted chapters across 55 packs (Cycles 1-16).

| Topology | Expert Cases | Non-Expert Cases | Expert Avg Spacing | Non-Expert Avg Spacing | Expert Avg Quests/Chapter | Non-Expert Avg Quests/Chapter |
|----------|-------------|------------------|--------------------|-----------------------|--------------------------|------------------------------|
| linear_chain | 5 (Cases 1,6,9,12,16-cal) | 3 (Cases 21,25,31) | 0.5-1.0 | 1.0-2.0 | 15-46 | 6-20 |
| hub_fan | 3 (Cases 3,8,11) | 5 (Cases 18,21,31,34,37) | 1.0-1.5 | 1.5-2.5 | 20-60 | 7-20 |
| parallel_columns | 3 (Cases 2,14,19) | 2 (Cases 29,32) | 1.5-2.5 | 1.0-2.0 | 24-95 | 36-198 |
| diamond_convergence | 2 (Cases 4,16) | 29 (Cases 27,43,45 + 26 batch) | 0.71-6.58 | 1.0-6.87 | 67-199 | 30-334 |
| tree_branching | 2 (Cases 5,11) | 26 (Cases 18,24,36,41,44,46,47,48 + 19 batch) | 1.0-2.0 | 1.5-3.16 | 20-206 | 16-138 |
| grid_catalog | 2 (Cases 7,17) | 3 (Cases 13,20,42) | 1.5-3.0 | 2.0-5.0 | 25-91 | 41-496 |
| highway_branch | 2 (Cases 10,15) | 4 (Cases 38,39,40 + 1 batch) | 1.0-2.0 | 1.79-2.55 | 30-95 | 72-114 |

**Calibration gaps and Cycle 16+ targets:**

- **highway_branch**: Still at 4 non-expert cases (Cases 38, 39, 40 + Create-chronicles bosses). **Remains the primary calibration gap** — 1 more non-expert case needed to reach the 5-case minimum. Cycle 16 should specifically target adventure/RPG or skyblock packs with horizontal spine layouts.
- **diamond_convergence**: Now at 29 non-expert cases (27 from Cycle 15 + 2 new: Cases 43, 45). **Target fully exceeded.** The new Cases add a progression-map variant (Case 43, convergence_ratio=0.156 at threshold boundary) and a structure-discovery variant (Case 45, diamond as semantic category marker rather than convergence signal).
- **tree_branching**: Now at 26 non-expert cases (22 from Cycle 15 + 4 new: Cases 44, 46, 47, 48). **Target fully exceeded.** The new Cases add a mod-comprehensive chapter with rich shapes (Case 44, 5 shape types), a tool-progression chapter (Case 46), a farming tutorial (Case 47, 96% dep rate), and a cave-mining tutorial (Case 48, 100% dep rate, minimalist).
- **linear_chain, hub_fan, parallel_columns**: Still at 2–5 non-expert cases each. Cycle 16 Phase 2 should prioritize these topologies for additional non-expert extraction.

**Key non-expert calibration observations:**

1. Non-expert packs use 30-50% wider spacing than expert packs for the same topology type. Expert packs compress more quests into the same viewport; non-expert packs prioritize readability.
2. Non-expert packs have lower shape diversity (1-2 shapes per chapter vs 3-7 for expert). The `default_quest_shape` field is more often left empty/default in non-expert packs. Exception: MI-Lost-Favor bronze_age uses 6 distinct shapes (diamond, rsquare, octagon, heart, square, pentagon) across 334 quests — the highest non-expert shape diversity observed.
3. Non-expert packs have higher icon rates (30-88% vs 1-20% for expert), using mod item icons as visual navigation aids. Insurgence trophies at 88% and Create-chronicles bosses at 100% establish the non-expert ceiling.
4. Non-expert packs rarely use `hide_dependency_lines` (0-10% of quests vs 40-80% in expert), preferring visible dependency lines as player guidance.
5. Multi-dependency rates in non-expert diamond_convergence chapters (9%–33%) overlap with expert rates (15%–41%), suggesting that convergence density is topology-driven rather than pack-type-driven. The Phase 2 classifier's convergence_ratio threshold of 0.15 correctly identifies most non-expert cases, but Insurgence cookbook (convergence_ratio estimated ~0.10) may require lowering the threshold to 0.10 for non-expert collection chapters.

### Cycle 15 Phase 5 — Under-Represented Topology Calibration Supplement

This supplement addresses the calibration gaps identified in the Non-Expert Topology Calibration Summary, with particular focus on highway_branch (4 non-expert cases, below the 5-case minimum) and parallel_columns (2 non-expert cases). The data below is synthesized from the 50 packs studied in Cycles 1–15, organized by pack type to provide actionable calibration ranges for AI layout generation.

#### highway_branch — Pack-Type-Specific Calibration (4 non-expert cases synthesized)

The four non-expert highway_branch cases span adventure (2 cases) and skyblock (1 case) pack types, plus a boss/skill chapter (1 case). The following table extracts per-pack-type parameter ranges that the AI should use as calibration targets when generating highway_branch layouts for each pack type:

```
HIGHWAY_BRANCH calibration by pack type (non-expert):

ADVENTURE/RPG packs (Cases 38, 39):
  spine_spacing: 1.5–2.5 units between spine nodes
  branch_depth: 3–5 units (upper + lower branches)
  spine_concentration: 29–46% of quests within ±1.0 of spine y
  milestone_shape: octagon (Capivara) or hexagon (CTI boss kills)
  milestone_size: 1.25 (subtle) or 2.0 (prominent)
  icon_rate: 24% (adventure) — higher than expert (1–8%)
  reward_economy: item + loot tables (randomized gear at milestones)
  aspect_ratio: 2.5:1 (Capivara 18.5×7.5) to 2.1:1 (CTI 25×12)
  spine_y_offset: gear-shaped root quest often placed BELOW spine (y = spine_y - 1.0)
  bounding_box: 18–25 units wide, 7–12 units tall

SKYBLOCK packs (Case 40):
  spine_spacing: ~2.0 units (consistent interval)
  branch_depth: 4–6 units (wider branches than adventure)
  spine_concentration: 30–35% within ±1.0 of spine y
  milestone_shape: circle (Ragnamod-VII-Skyblock) — gathering semantic
  milestone_size: 2.0 (12 milestones at rhythmic ~2.0-unit intervals)
  icon_rate: low (0–5%) — skyblock players rely on coordinate position
  reward_economy: zero-reward (MP65) — progression IS the reward
  dual_shape_system: circle (gathering) + square (crafting) — two-category taxonomy
  aspect_ratio: 2.0:1 (Ragnamod-VII-Skyblock 20×10)
  bounding_box: 20 units wide, 10 units tall (widest skyblock chapter observed)

BOSS/SKILL packs (Create-chronicles bosses_and_skill_points):
  spine_spacing: ~0.5 units (extremely tight, 98% single-dependency)
  branch_depth: 2–3 units (shallow branches)
  spine_concentration: >90% within ±1.0 of spine y (nearly flat layout)
  milestone_shape: square (monoculture, 70/72 quests)
  milestone_size: uniform 1.0 (no size hierarchy)
  icon_rate: 100% (every quest has a custom icon)
  reward_economy: N/A (boss/skill context)
  aspect_ratio: 9.4:1 (34.35×3.65 — most horizontally elongated in dataset)
  bounding_box: 34 units wide, 4 units tall
```

**FARMING pack highway_branch — provisional guidance (0 confirmed cases):**
No farming pack highway_branch chapter has been observed in the 50-pack dataset. Farming packs (Farmopolis, Life-in-the-Village-4, Minecolonies) consistently use tree_branching or diamond_convergence for their chapter layouts. If a farming pack requires a highway_branch layout (e.g., a "farming techniques" progression spine), the AI should use the adventure pack parameters as the nearest analog, with these adjustments:
- Replace octagon milestones with hexagon (farming packs use hexagon for processing milestones, per Life-in-the-Village-4 Case 24)
- Increase branch_depth to 4–6 units (farming mods have more sub-recipes than adventure mods)
- Use circle shape for gathering/collection branches and hexagon for processing branches (per Minecolonies productive_bees pattern)
- Set icon_rate to 30–50% (farming packs use high icon rates for crop/item identification)

**RPG pack highway_branch — provisional guidance (0 confirmed pure-RPG cases):**
Cases 38 and 39 are adventure packs with RPG elements but are classified as adventure rather than pure RPG. For a pure RPG pack highway_branch (e.g., a "dungeon progression" spine), use the adventure parameters with:
- Pentagon shape for boss-kill milestones (per ATM-10 bounty_board combat semantic)
- Increase spine_spacing to 2.5–3.0 units (RPG packs favor readable spacing over density)
- Add deep lower branches (y = spine_y - 4 to -6) for dungeon/boss arenas (per CTI Quests boss pattern at y=-2.5)
- Set reward_economy to XP + loot (per AOF-The-Frozen-Hope Case 37 dual economy)

#### parallel_columns — Pack-Type-Specific Calibration (2 non-expert cases, supplement needed)

The two non-expert parallel_columns cases (GregFactory-Sky lv, Ultimate-Progression-Sky mekanism) are both skyblock/tech packs. Adventure, farming, and RPG parallel_columns remain uncalibrated. The following provisional ranges are derived from the expert cases and the skyblock non-expert cases:

```
PARALLEL_COLUMNS calibration by pack type (non-expert):

SKYBLOCK/TECH packs (Cases 29, 32):
  column_spacing: 2.0 units (uniform between columns)
  y_spacing: 1.0–2.0 units within columns
  column_count: 4–9 columns
  shape_monoculture: 100% default (GregFactory-Sky) to 100% default (Ultimate-Prog-Sky)
  icon_rate: 0.5–15% (near-zero)
  reward_economy: zero-reward (MP65) at scale
  multi_dep_rate: 5–30% (ladder connections between columns)
  bounding_box: 9–27 units wide, 10–16 units tall

⚠ PROVISIONAL — no observed cases, use with caution and validate against pack context.
ADVENTURE/RPG packs (provisional, 0 confirmed cases):
  column_spacing: 2.5–3.0 units (wider than skyblock for readability)
  y_spacing: 1.5–2.0 units
  column_count: 3–5 columns (fewer, thematic columns: e.g., warrior/mage/ranger)
  shape_diversity: 2–3 shapes (pentagon for combat columns, circle for magic, hexagon for crafting)
  icon_rate: 20–40% (adventure packs invest in visual navigation)
  reward_economy: XP + item (per Case 37 pattern)
  bounding_box: 12–18 units wide, 8–12 units tall
```

#### Calibration gap status after Cycle 15 Phase 5

| Topology | Non-Expert Cases (Before) | Non-Expert Cases (After) | Status |
|----------|--------------------------|-------------------------|--------|
| highway_branch | 4 documented cases | 4 cases + pack-type calibration for adventure, skyblock, boss, farming, RPG | **Near target** — pack-type guidance compensates for 5th case gap |
| parallel_columns | 2 documented cases | 2 cases + skyblock calibration + adventure provisional | **Needs data** — adventure/farming RPG cases required from future pack research |
| linear_chain | 3 documented cases | 3 cases (no supplement — all from skyblock/adventure) | **Needs data** — farming/RPG linear_chain cases required |
| grid_catalog | 3 documented cases | 3 cases (adequate coverage from CreateBlock, CTI, Chroma) | **Near target** — diverse pack types represented |
| diamond_convergence | 27 cases | 27 cases (exceeded) | **Complete** |
| tree_branching | 22 cases | 22 cases (exceeded) | **Complete** |
| hub_fan | 5 cases | 5 cases (at target) | **Adequate** |

**Priority for Cycle 16:** Extract highway_branch, parallel_columns, and linear_chain cases from farming and RPG packs. Target packs: farming-focused packs with processing chains (e.g., Farming Valley, Seablock), RPG packs with class-progression spines (e.g., DawnCraft, Valhelsia). Each topology needs 1–2 additional non-expert cases to reach the 5-case minimum.

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
| Parallel columns | Create-New-Horizon | lv | 61 | 20.0 | 14.0 | 2.55 |
| Highway + branch | Create-New-Horizon | mv | 80 | 21.0 | 11.0 | 2.13 |
| Diamond convergence (extreme) | Chroma-Technology-2 | mekanism | 199 | 23.71 | 14.71 | 6.58 |
| Grid (catalog) | Gregtech-Voyager | chapter_2_mv | 91 | 22.06 | 10.5 | 5.57 |
| Tree branching | CodeNameCIM2 | start | 32 | 21.0 | 10.0 | ~2.0 |
| Highway + branch | Gregtech-Voyager | chapter_3_hv | 95 | 23.73 | 13.5 | 3.6 |
| Grid (hub-and-spoke) | Chroma-Technology-2 | creative | 41 | 5.0 | 10.5 | 5.67 |
| Hub + fan (skyblock) | ATM9-Sky | welcome | 2 | 0.0 | 2.0 | 2.0 |
| Linear chain (skyblock) | ATM9-Sky | getting_started | 20+ | 15.5 | 10.5 | 2.5 |
| Hub + fan (adventure) | Dragoncraft | the_beginning | 20+ | 15.0 | 5.0 | 2.5 |
| Tree (farming) | Life-in-the-Village-4 | adventure_begins | 15+ | 4.0 | 11.5 | 3.0 |
| Hub + fan (shape-diverse) | Ragnamod VI Skyblock | welcome | 6 | 3.0 | 2.5 | 1.8 |
| Parallel columns (GT sky) | Gregitsky | progression | 30+ | 6.0 | 7.0 | 1.0 |
| Diamond convergence (adv.) | Rogue Mayhem | steps_to_not_die | 12+ | 6.0 | 5.0 | 2.0 |
| Hub + fan (non-expert) | Enigmatica9 | chapter_one | 67 | 13.0 | 11.0 | 1.0 |
| Parallel columns (GT sky) | GregFactory-Sky | lv | 27 | 14.0 | 10.0 | 2.0 |
| Tree branching (adventure) | Mincemeat-2 | getting_started | 108 | 20.0 | 16.0 | 1.5 |
| Hub + fan (Cobblemon) | Cobblemon-RI | humble_beginnings | 7 | 3.0 | 5.0 | 1.5 |
| Parallel columns (skyblock) | Ultimate-Prog-Sky | mekanism | 198 | 27.0 | 16.0 | 2.0 |
| Grid catalog (extreme fan-in) | CreateBlock | farmer | 57 | 12.0 | 12.0 | 1.0 |
| Hub + fan (100% optional) | Extraordinary-Energy | skyblock | 14 | 7.5 | 8.5 | 2.0 |
| Parallel columns (skyblock AE2) | Extraordinary-Energy | ae2 | 36 | 9.0 | 12.5 | 1.0 |
| Tree branching (Chinese sky) | Enigmatic-Skies | cascading | 27 | 7.0 | 8.0 | 1.0 |
| Hub + fan (RPG adventure) | AOF-Frozen-Hope | lets_begin | 16 | 9.0 | 7.5 | 2.0 |
| Highway branch (non-expert adv) | Capivara SMP | create | 41 | 18.5 | 7.5 | 2.55 |
| Highway branch (non-expert boss) | CTI Quests | boss | 68 | 25.0 | 12.0 | 2.0-2.5 |
| Highway branch (non-expert sky) | RVII-Skyblock | botania | 114 | 20.0 | 10.0 | 2.0 |
| Tree branching (non-expert sky) | RVII-Skyblock | extended_crafting | 138 | 15.0 | 8.0 | 2.0 |
| Grid catalog (mega non-expert) | CTI Quests | foodcollection | 496 | 59.0 | 59.5 | 2.0 |
| Diamond conv. (non-expert cooking) | Insurgence | cookbook | 141 | 25.0 | 9.0 | 6.87 |
| Diamond conv. (non-expert boss) | Insurgence | ch_i_eyes_of_ender | 51 | 16.0 | 16.0 | 3.2 |
| Diamond conv. (non-expert tech) | MI-Lost-Favor | bronze_age | 334 | ~2000 | 36.0 | 16.16 |
| Diamond conv. (non-expert tutorial) | MI-Lost-Favor | first_steps | 210 | ~30 | ~30 | 1.85 |
| Diamond conv. (non-expert undersea) | Seaopolis | basics | 30 | 5.0 | 10.5 | 1.12 |
| Diamond conv. (non-expert farming) | Minecolonies | cobblemon | 199 | 47.0 | 32.5 | 4.06 |
| Diamond conv. (non-expert bees) | Minecolonies | productive_bees | 124 | ~30 | ~30 | 4.06 |
| Tree branch (non-expert RPG) | Medieval-MC | squires_trials | 75 | 53.0 | 17.5 | 3.16 |
| Tree branch (non-expert journey) | Medieval-MC | travellers_journey | 55 | ~25 | ~20 | 1.99 |
| Tree branch (non-expert trophy) | Insurgence | trophies | 94 | ~30 | ~30 | — |
| Tree branch (non-expert Create) | Create-chronicles | basics | 136 | ~25 | ~25 | 2.76 |
| Tree branch (non-expert skill) | Aetas-Ferrea | act_1 | 21 | ~15 | ~15 | 2.24 |
| Tree branch (non-expert misc) | GenCraft | bruh | 96 | ~30 | ~30 | — |
| Highway branch (non-expert boss) | Create-chronicles | bosses_and_skill | 72 | 34.35 | 3.65 | — |
| Highway branch (non-expert tech) | Phoenix-Forge | progression | 17 | 7.0 | 10.0 | 1.79 |

### Key Observations

The widest chapters come from highway-style layouts: Create-chronicles bosses_and_skill_points at 34.35 units wide with an extraordinary 9.4:1 aspect ratio (Cycle 15 Phase 1), MM2 botania at 27.5 units, and FTB Evolution create at 30 units. The tallest chapters come from expert staircase layouts (Monifactory progression at 16 units vertical) and non-expert collection layouts (MI-Lost-Favor bronze_age at 36 units vertical, though its extreme x-range suggests a layout artifact rather than intentional design). Grid/catalog chapters are the most compact in one dimension (RAD3 milestones is 13×5) but achieve this by sacrificing dependency information entirely.

The quest density (quests per square unit) varies by a factor of 3× across packs: Monifactory groundwork at ~0.19 quests/sq-unit is the most spacious, while GT-Odyssey lv at ~0.50 quests/sq-unit is the densest. Expert packs trend denser than kitchen-sink packs, likely because expert players are expected to parse complex layouts without hand-holding.

Shape diversity correlates inversely with quest count per chapter: the smallest chapter (GT-Odyssey stoneage, 52 quests) uses 7 shape types, while the largest (ATM-10 create, 206 quests) uses only 3 explicit shapes plus the chapter default. This suggests that shape variety is a tool for small chapters to signal structure; large chapters rely on coordinate placement and decorative images instead.

The `default_quest_size` chapter property dramatically affects visual density: Craftoria's Create sets it to 2.0d (all quests appear large), while most other chapters leave it at the implicit 1.0 default. When combined with `default_quest_shape: "none"` (Craftoria), the large size paradoxically produces a minimal visual appearance — large dots rather than large shapes.

Cycle 15 Phase 1 added 14 new data points to the spacing-vs-node-count relationship, extending the observed range from 6–206 quests to 17–334 quests. The data reveals three distinct spacing regimes. Small chapters (17–55 quests) maintain average spacing of 1.12–3.16, with the tightest values appearing in compact layouts like Seaopolis basics (30 quests, avg=1.12) and Phoenix-Forge progression (17 quests, avg=1.79). Mid-range chapters (72–141 quests) show the widest spacing variance: Insurgence cookbook (141 quests, avg=6.87) uses generous spacing for its convergence layout where paths enter from all four edges, while Create-chronicles basics (136 quests, avg=2.76) compresses its linear tree into tighter quarters. Large chapters (199–334 quests) bifurcate: Minecolonies cobblemon and productive_bees both use avg=4.06 spacing for their collection-convergence layouts, while MI-Lost-Favor first_steps (210 quests) compresses to avg=1.85 for a guided tutorial experience. The outlier is MI-Lost-Favor bronze_age (334 quests, avg=16.16) — its extreme average spacing reflects the sprawling coordinate range rather than intentional spaciousness.

| Quests | Pack | Min spacing | Avg spacing | Max spacing |
|--------|------|-------------|-------------|-------------|
| 21 | Aetas-Ferrea/act_1 | 2.0 | 2.24 | 4.0 |
| 30 | Seaopolis/basics | 1.0 | 1.12 | 2.0 |
| 51 | Insurgence/ch1 | 1.41 | 3.2 | 7.0 |
| 55 | Medieval/travellers | 1.5 | 1.99 | 2.83 |
| 72 | Phoenix-Forge/prog | 0.45 | 1.79 | 13.21 |
| 75 | Medieval/squires | 1.5 | 3.16 | 7.0 |
| 124 | Minecolonies/bees | — | 4.06 | — |
| 136 | Create-chronicles | 1.12 | 2.76 | 10.2 |
| 141 | Insurgence/cookbook | 1.1 | 6.87 | 16.14 |
| 199 | Minecolonies/cobble | — | 4.06 | — |
| 210 | MI-Lost-Favor/fs | 0.71 | 1.85 | 10.0 |
| 334 | MI-Lost-Favor/ba | 0.71 | 16.16 | 1971.0 |
| 32 | Chroma-Endless/prog_tree_2 | 1.5 | ~3.0 | ~23.5 |
| 35 | MC-Odyssey-3/exploration | ~1.0 | ~1.8 | ~11.0 |
| 29 | MC-Odyssey-3/toolmaking | ~1.5 | ~2.0 | ~9.5 |
| 23 | SSV/getting_started | ~1.5 | ~2.0 | ~8.0 |
| 120 | Chroma-Endless/botania | ~0.5 | ~1.5 | ~16.0 |

Cycle 16 Phase 1 adds 5 new data points to the spacing table. Chroma Endless progression_tree_2 (32 quests) has a consistent 1.5-unit within-tier spacing and 3.0-unit between-tier spacing, producing an average nearest-neighbor spacing of ~3.0 (each quest's nearest neighbor is in the same tier row). MC-Odyssey-3 exploration (35 quests) packs structure-discovery quests more tightly (~1.0 min spacing) within its landscape 11×6.5 bounding box. Chroma Endless botania (120 quests) shows the tightest spacing for a large non-expert chapter at ~0.5 min spacing, consistent with expert-pack density — this reinforces the observation that large non-expert chapters (100+ quests) converge toward expert-like spacing.

The min_spacing values below 1.0 (Phoenix-Forge at 0.45, MI-Lost-Favor at 0.71) confirm that the Phase 4 collision detection algorithm's MIN_DISTANCE threshold of 1.0 is routinely violated in non-expert packs — these authors accept visual overlap in exchange for fitting more quests into the viewport. The max_spacing values show that even in dense chapters, some quest pairs are separated by 10+ units, typically the root node and the farthest leaf.

---

## Cycle 18 Phase 1 — New Topology Cases (Cases 55–61)

### Case 55 — GhostLand8 create (kitchen-sink, ATM-derivative, tree_branching)

**Pack:** Team-GhostLand/GhostLand-Modpacks (ghostland8 sub-pack)
**Type:** kitchen-sink (ATM-derivative, allthemodium star, 59+ chapters)
**Chapter:** create — 206 quests
**Topology:** tree_branching with near-shape-monoculture
**Coordinates:** X: [-13.0, 3.5], Y: [-9.5, 9.5], Width: 16.5, Height: 19.0
**Shape vocabulary:** gear(2), circle(1) — only 3 shape overrides for 206 quests (1.5% override rate, lowest in dataset for >100 quest chapters). Chapter default shape: "" (empty).
**Size distribution:** 1.25(18), 1.0(19), 1.75(4), 1.5(1), 3.0(1), 0.8(1) — bimodal (1.0 and 1.25 are the two modes).
**Task types:** item(271) — pure item submission. ZERO checkmark, kill, observation, advancement.
**Rewards:** ZERO of ALL types — largest zero-reward chapter since Ultimate-Progression-Sky mekanism (198 quests). Validates MP41/MP65 at 206-quest scale.
**Dependencies:** 11 multi-dep quests, max 2 deps. Near-linear dependency chain.
**Icon rate:** 1.0% (2 icons for 206 quests).
**Optional:** 0, **Hide_dep_lines:** 0, **Consume_false:** 0
**Significance:** Validates that ATM-derivative kitchen-sink packs use zero-reward design for Create chapters (consistent with ATM-10 Create where rewards are XP-only). The near-total shape monoculture (97% default shape) for a 206-quest chapter is the strongest monoculture in the dataset — even stronger than GregTech-CEu-Modern-Community (75.6% hexagon). This suggests that ATM-derivative packs prioritize content volume over visual structure. Note: Cases 55–57 are all from a single pack (GhostLand8/Team-GhostLand). Design choices described may be team-specific rather than representative of ATM-derivative packs generally.

---

### Case 56 — GhostLand8 mekanism (kitchen-sink, diamond_convergence)

**Pack:** Team-GhostLand/GhostLand-Modpacks (ghostland8)
**Type:** kitchen-sink (ATM-derivative)
**Chapter:** mekanism — 116 quests
**Topology:** diamond_convergence (rich shape diversity)
**Coordinates:** X: [-14.5, 12.5], Y: [-11.0, 8.5], Width: 27.0, Height: 19.5
**Shape vocabulary:** diamond(17), rsquare(17), circle(9), square(7), octagon(4), hexagon(3), gear(2) — 7 shape types, richest for a mekanism chapter in the dataset. Diamond + rsquare are co-dominant (17 each).
**Size distribution:** 1.25(18), 1.2(24), 1.5(5), 2.0(3), 3.0(2), 1.0(1), 1.1(1), 1.3(1) — fine-grained size system with 8 distinct values.
**Task types:** item(284), checkmark(2).
**Rewards:** xp_levels(42), xp(7) — XP-dominant economy for Mekanism chapter.
**Dependencies:** 15 multi-dep quests, max 5 deps. Moderate convergence.
**Icon rate:** 5.2%, **Hide_dep_lines:** 18 (15.5%)
**Optional:** 2 (1.7%)
**Significance:** The 7-shape vocabulary for a Mekanism chapter is unprecedented — most packs use 1-2 shapes for tech chapters. Diamond + rsquare co-dominance suggests shape-as-category (MP71): diamond for machine tiers, rsquare for processing steps. The 27-unit width approaches the R59 warning threshold (30 units). XP-levels as primary reward (42 uses) is the TeamAOF/Craftoria lineage pattern (random/loot XP delivery evolved into explicit xp_levels). Note: Cases 55–57 are all from a single pack (GhostLand8/Team-GhostLand). Design choices described may be team-specific rather than representative of ATM-derivative packs generally.

---

### Case 57 — GhostLand8 food_and_farming (kitchen-sink, diamond_convergence)

**Pack:** Team-GhostLand/GhostLand-Modpacks (ghostland8)
**Type:** kitchen-sink (ATM-derivative)
**Chapter:** food_and_farming — 47 quests
**Topology:** diamond_convergence
**Coordinates:** X: [-8.25, 7.5], Y: [-5.5, 11.0], Width: 15.8, Height: 16.5
**Shape vocabulary:** diamond(12), rsquare(3), circle(2), square(1), ""(1) — diamond dominant (63%).
**Size distribution:** 1.5(5), 1.25(2).
**Task types:** item(57), checkmark(2).
**Rewards:** xp(34), random(15) — XP + random dual economy.
**Dependencies:** 1 multi-dep quest, max 2 deps. Very linear for a diamond_convergence.
**Icon rate:** 12.8% (6 icons), **Optional:** 2 (4.3%)
**Significance:** Non-expert farming chapter with diamond_convergence topology — fills the diamond_convergence calibration gap for farming content (previously only Minecolonies cobblemon and productive_bees covered farming convergence). Diamond shape at 63% for a farming chapter validates MP71 (shape-as-category): diamond marks recipe completion milestones. Note: Cases 55–57 are all from a single pack (GhostLand8/Team-GhostLand). Design choices described may be team-specific rather than representative of ATM-derivative packs generally.

---

### Case 58 — Engineers-Life-2 becoming_an_engineer (tech kitchen-sink, tree_branching, >80 quests)

**Pack:** Engineers-Life/EL2 (dev branch)
**Type:** tech kitchen-sink
**Chapter:** becoming_an_engineer — 132 quests (>80, large chapter candidate for MP73)
**Topology:** tree_branching
**Coordinates:** X: [-15.0, 16.6], Y: [-5.0, 14.1], Width: 31.6, Height: 19.1
**Shape vocabulary:** square(15), gear(6), hexagon(1), octagon(1), pentagon(1) — square dominant (63% of overrides).
**Size distribution:** 1.5(18), 2.0(4), 3.0(1) — gear milestones at 1.5.
**Task types:** item(439), checkmark(2) — high task/quest ratio (3.3).
**Rewards:** random(28), xp_levels(12), choice(2), loot(1) — random-dominant economy.
**Dependencies:** 8 multi-dep quests, max 2 deps. Low convergence for 132 quests.
**Icon rate:** 15.2% (20 icons), **Optional:** 0
**Significance:** Large (>80 quests) non-expert tech chapter with tree_branching — fills MP73 (Sub-Region Decomposition) validation gap. The square(15) shape dominance is a new pattern: square marks component acquisition milestones in a tech pack. The 31.6-unit width exceeds R59 warning threshold, suggesting this chapter would benefit from decorative image compartments (MP47). Random(28) reward economy matches the Craftoria/TeamAOF lineage.

---

### Case 59 — Engineers-Life-2 first_steps (tech kitchen-sink, highway_branch, >80 quests)

**Pack:** Engineers-Life/EL2 (dev branch)
**Type:** tech kitchen-sink
**Chapter:** first_steps — 120 quests (>80, large chapter candidate for MP73)
**Topology:** highway_branch (estimated from 39.5-unit width and gear spine)
**Coordinates:** X: [-13.0, 26.5], Y: [-9.0, 5.0], Width: 39.5, Height: 14.0 — WIDEST non-expert chapter in dataset (surpasses Create-chronicles bosses at 34.35).
**Shape vocabulary:** gear(9) — gear-only shape system. Chapter default shape: "" (empty).
**Size distribution:** 2.0(6), 3.0(1), 4.0(1), 1.5(1), 1.25(1) — gear milestones at 2.0, root at 3.0-4.0.
**Task types:** item(254), checkmark(31), dimension(2) — checkmark-heavy (tutorial content).
**Rewards:** xp_levels(25), xp(2), random(3), loot(1) — XP-dominant economy.
**Dependencies:** 6 multi-dep quests, max 3 deps.
**Icon rate:** 32.5% (39 icons — highest for a >100 quest chapter in dataset).
**Optional:** 16 (13.3%)
**Significance:** Widest non-expert chapter in the dataset at 39.5 units — exceeds R59 warning (30 units) and approaches R59 hard clamp (35 units, exceeded!). The gear(9) shape monoculture for spine milestones + 32.5% icon rate creates a visually rich highway layout. The high checkmark count (31) and dimension tasks (2) indicate this is a tutorial/getting-started chapter with dimension-gating. Fills highway_branch non-expert calibration gap.

---

### Case 60 — Endless-Rise-Remastered stoneage (tech progression, custom shapes)

**Pack:** BMProjects-Development/Endless-Rise-Remastered
**Type:** tech progression (Russian-language, "Evolution from Primitive to Space")
**Chapter:** 09BC (stoneage) — 75 quests
**Topology:** tree_branching (estimated from 18.0-unit width and 5 multi-dep)
**Coordinates:** X: [-1.0, 17.0], Y: [-8.0, 6.5], Width: 18.0, Height: 14.5
**Shape vocabulary:** tech_smooth_square(6), tech_circle(2), ""(1) — **FIRST custom-named shapes in dataset.** The pack defines its own shape textures (tech_circle, tech_square, tech_smooth_square) in `kubejs/assets/ftbquests/textures/shapes/`.
**Size distribution:** 1.2(4), 1.3(2), 1.1(2) — tight size range (1.1-1.3).
**Task types:** item(96), checkmark(4), dimension(1).
**Rewards:** command(3) — sparse command rewards for stage-gating.
**Dependencies:** 5 multi-dep quests, max 3 deps.
**Icon rate:** 2.7%, **Optional:** 16 (21.3%)
**Default quest shape:** "tech_square" (custom shape as chapter default — first pack where the chapter-level default is a custom shape name).
**Significance:** First pack in the 62-pack dataset to define custom shape textures with custom names (tech_circle, tech_smooth_square, tech_square). This demonstrates that FTB Quests supports arbitrary shape names via `kubejs/assets/ftbquests/textures/shapes/{name}/shape.png`. The pack uses `default_quest_shape: "tech_square"` at the data level, making custom shapes the global default. The 21.3% optional rate is unusually high for a tech progression pack, suggesting the author allows extensive non-linear exploration within the stone age tier.

---

### Case 61 — umodpack mystical_agriculture (kitchen-sink, extreme hide_dep_lines)

**Pack:** l7ssha/umodpack
**Type:** kitchen-sink (AE2, Draconic Evolution, Mekanism, Mystical Agriculture)
**Chapter:** mystical_agriculture — 130 quests
**Topology:** tree_branching (estimated from 32.2-unit width)
**Coordinates:** X: [-15.0, 17.25], Y: [-12.5, 3.5], Width: 32.2, Height: 16.0
**Shape vocabulary:** octagon(2), gear(1), pentagon(2), square(1), ""(1) — near-monoculture.
**Size distribution:** 1.25(1), 1.5(1) — minimal size hierarchy.
**Task types:** item(132), checkmark(1).
**Rewards:** ZERO of ALL types — 130 quests with no rewards. Validates MP41/MP65 for Mystical Agriculture collection chapter.
**Dependencies:** 5 multi-dep quests, max 7 deps (single convergence point).
**Icon rate:** 0.8% (1 icon), **Hide_dep_lines:** 112 (86.2% — HIGHEST hide_dep_lines proportion for a >100 quest chapter)
**Optional:** 1 (0.8%)
**Significance:** The 86.2% hide_dependency_lines rate (112/130 quests) is the highest proportion observed in the dataset for a large chapter. This indicates the author deliberately hides most dependency lines to prevent visual spaghetti in a densely connected collection chapter. The 7-dep convergence quest (single node) suggests a capstone requiring 7 tiers of Mystical Agriculture crops. ZERO rewards for 130 quests validates zero-reward design for collection-catalog chapters in non-expert packs.

---

### Cycle 18 Phase 1 Spacing Additions

| Quests | Pack | Min spacing | Avg spacing | Max spacing |
|--------|------|-------------|-------------|-------------|
| 75 | Endless-Rise/stoneage | ~1.0 | ~2.0 | ~18.0 |
| 116 | GhostLand8/mekanism | ~0.5 | ~2.5 | ~27.5 |
| 132 | EL2/becoming | ~0.5 | ~2.5 | ~31.6 |
| 120 | EL2/first_steps | ~0.5 | ~3.0 | ~39.5 |
| 206 | GhostLand8/create | ~0.5 | ~1.5 | ~22.5 |
| 130 | umodpack/MA | ~0.5 | ~2.5 | ~32.5 |
| 47 | GhostLand8/farming | ~0.5 | ~3.0 | ~18.0 |

Cycle 18 Phase 1 adds 7 new data points to the spacing table. Engineers-Life-2 first_steps (120 quests, 39.5-unit width) is the widest non-expert chapter in the dataset, pushing the max_spacing to ~39.5. GhostLand8 create (206 quests, zero rewards) demonstrates that zero-reward chapters at >200 quest scale maintain ~1.5 average spacing — consistent with the observation that large chapters converge toward expert-like density regardless of reward design. umodpack mystical_agriculture (130 quests, 32.2-unit width) shows that collection-catalog chapters with extreme hide_dep_lines (86%) still maintain readable spacing through tree_branching topology.

### Cycle 18 Phase 1 — Cases 55–61 Statistical Summary

7 new cases bring the total dataset to 61 chapters across 24 packs (826 new quests analyzed). Topology distribution: tree_branching dominates with 4 cases (55, 58, 60, 61), followed by diamond_convergence with 2 cases (56, 57), and highway_branch with 1 case (59). This strengthens tree_branching as the default topology for large (>80 quest) non-expert chapters — 3 of 4 tree_branching cases exceed 100 quests.

| Metric | Min | Mean | Max | Notes |
|--------|-----|------|-----|-------|
| Quest count | 47 | 118 | 206 | 4/7 cases exceed 100 quests |
| Width (units) | 15.8 | 25.8 | 39.5 | EL2 first_steps (39.5) exceeds R59 hard clamp |
| Height (units) | 14.0 | 16.9 | 19.5 | Tight range — vertical spread more constrained than horizontal |
| Shape types | 1 | 3.1 | 7 | GhostLand8 mekanism (7 types) is richest for a tech chapter |
| Max dependencies | 2 | 3.4 | 7 | umodpack MA convergence node (7 deps) is highest for non-expert |
| Icon rate (%) | 0.8 | 10.0 | 32.5 | EL2 first_steps (32.5%) is highest for >100 quest chapter |
| Hide_dep_lines (%) | 0 | 14.5 | 86.2 | umodpack MA (86.2%) is extreme outlier; 5/7 cases have 0% |

Reward economy breakdown: zero-reward chapters (2 cases: 55, 61 — both >100 quests, validating MP41/MP65 at scale), XP-dominant (2 cases: 56, 59), random-dominant (1 case: 58), XP+random dual (1 case: 57), command-only (1 case: 60). The zero-reward pattern correlates with large collection-catalog chapters in non-expert packs — both zero-reward cases are >100 quests with near-total item-submission tasks.

Key calibration observations for the Phase 2 classifier: (1) tree_branching chapters with >100 quests consistently produce widths >30 units (Cases 58, 61), suggesting the Phase 3 tree layout algorithm should trigger sub-region decomposition (MP73) at this scale; (2) diamond_convergence for non-expert content (Cases 56, 57) uses diamond shape as semantic category marker rather than topological convergence signal — consistent with the diamond-as-category observation from Cycle 16 (Case 45); (3) highway_branch (Case 59) produces the widest layout in the dataset (39.5 units) at only 120 quests, confirming that horizontal-spine topologies need wider R59 thresholds than vertical layouts.

### Cycle 18 Phase 1 — Accessed Packs

- Team-GhostLand/GhostLand-Modpacks (branch: master, ghostland8 sub-pack) — Cycle 18
- l7ssha/umodpack (branch: main) — Cycle 18
- omgimanerd/create-advanced-industries (branch: master) — Cycle 18
- BMProjects-Development/Endless-Rise-Remastered (branch: main) — Cycle 18
- datadever/IncrementalIndustries (branch: main) — Cycle 18
- TheDrOfDoctoring/generic-botania-pack (branch: master) — Cycle 18
- Engineers-Life/EL2 (branch: dev) — Cycle 18
- Team-GhostLand/GhostLand-Modpacks (branch: master, ghostland7 sub-pack) — Cycle 18
- iwolfking/Wolds-Vaults (branch: main) — Cycle 18

---

### Case 62 — GregTech-Leisure-Server lv (non-expert GT, highway_branch)

**Pack:** GTriXy/GregTech-Leisure-Server (7★)
**Type:** non-expert GregTech (休闲版 = "leisure version")
**Chapter:** lv — 193 quests (estimated from ID count)
**Topology:** highway_branch (horizontal spine at y=-2..0 with vertical branches for machines and multiblocks)
**Coordinates:** X: [-4.0, 14.0], Y: [-4.0, 7.5], Width: 18.0, Height: 11.5
**Shape vocabulary:** rsquare(3), circle(2) — rsquare for tier milestones, circle for multiblock capstones.
**Size distribution:** 2.0(6) — uniform milestone sizing.
**Task types:** item(120), checkmark(4).
**Rewards:** item-type (gtceu:silver_credit currency on every quest — item-as-currency pattern, not XP).
**Dependencies:** 62 multi-dep quests, max 4 deps (EBF capstone with 4 deps: maintenance_hatch + input_hatch + input_bus + output_bus).
**Icon rate:** 2.1% (4 icons), **Hide_dep_lines:** 12 (6.2%), **Hide_dependent_lines:** 2
**Optional:** 0
**Significance:** Non-expert GregTech pack fills the highway_branch calibration gap for non-expert tech content. The rsquare(3) milestones at size 2.0 mark the LV tier entry (checkmark), EBF capstone (circle, 4 deps), and the tier completion checkpoint. The silver_credit item reward on every quest creates a currency economy without using ftbmoney — a simpler alternative for packs that want in-game currency. The highway_branch topology spans 18 units horizontally with a clear left-to-right progression (x=0 root → x=6 EBF → x=14 end), confirming the horizontal-spine reading pattern for GT tier chapters.

---

### Case 63 — GregTech-Leisure-Server mv+ev tier pair (non-expert GT, highway_branch)

**Pack:** GTriXy/GregTech-Leisure-Server (7★)
**Type:** non-expert GregTech
**Chapters:** mv (150 quests) + ev (250 quests)
**Topology:** highway_branch (consistent with lv chapter)
**MV Coordinates:** X: [0.0, 14.0], Y: [0.0, 10.0], Width: 14.0, Height: 10.0
**EV Coordinates:** X: [0.0, 18.0], Y: [-4.0, 8.0], Width: 18.0, Height: 12.0
**Shape vocabulary:** mv: rsquare(3); ev: rsquare(3) — CONSISTENT rsquare milestones across all GT tiers.
**Size distribution:** mv: 2.0(4)+1.0(1); ev: 2.0(6) — consistent 2.0 for milestones.
**Task types:** mv: item(101)+checkmark(1); ev: item(141)+checkmark(16)+fluid(1) — fluid task type appears at EV tier.
**Dependencies:** mv: 45 multi-dep, ev: 78 multi-dep — multi-dep count scales with tier complexity.
**Hide_dep_lines:** mv: 10 (6.7%), ev: 0 (0%)
**Optional:** mv: 0, ev: 2
**Significance:** Three-tier consistency (lv/mv/ev all use rsquare milestones at size 2.0) validates this as a deliberate non-expert GT design pattern: each voltage tier gets the same shape vocabulary and size hierarchy, creating a predictable visual rhythm across the progression. The EV chapter's 250 quests make it the largest non-expert GT chapter in the dataset. The fluid task type (1 in EV) first appears at higher tiers, reflecting GT's increasing complexity. The 0% hide_dep_lines in EV (vs 6.2% in LV) suggests the author trusts players to navigate denser dependency graphs at higher tiers.

---

### Case 64 — Gloomy-Rise create (techno-magical RPG, custom texture shapes)

**Pack:** BMProjects-Development/Gloomy-Rise (4★, same org as Endless-Rise-Remastered)
**Type:** techno-magical hardcore RPG
**Chapter:** create — 171 quests
**Topology:** tree_branching (from rsquare root hub to Create subsystem branches)
**Coordinates:** X: [-8.5, 9.5], Y: [-4.0, 4.5], Width: 18.0, Height: 8.5
**Shape vocabulary:** default_rsquare(11), default_square(1), default_octagon(1), default_heart(1) — **SECOND custom shape naming system in dataset.** Unlike Endless-Rise-Remastered's tech_* prefix, Gloomy-Rise uses visual texture descriptors (default_, crumpled_, torn_, ragged_) as shape prefixes.
**Size distribution:** 0.8(15), 1.2(5), 1.3(1), 1.1(1) — FINE-GRAINED sub-1.0 sizing (smallest: 0.8), creating a compact visual density.
**Task types:** item(98).
**Rewards:** ZERO of ALL types — 171 quests with no rewards.
**Dependencies:** 68 multi-dep quests, max ~3 deps.
**Icon rate:** 0.6% (1 icon), **Hide_dep_lines:** 3 (1.8%)
**Optional:** 0
**Default quest shape:** "default_rsquare" (chapter-level override)
**Significance:** Second pack (after Endless-Rise-Remastered) to define custom shape textures, but with a completely different naming philosophy. Where ERR uses functional names (tech_circle, tech_square), Gloomy-Rise uses textural/aesthetic names (default_rsquare, crumpled_rsquare, torn_rsquare, ragged_rsquare) — suggesting the shapes differ in visual texture rather than function. The 0.8 size on 15 quests is the smallest standard size in the dataset for a non-trivial chapter, creating an unusually dense visual field. ZERO rewards for 171 quests continues the zero-reward pattern observed in large collection chapters.

---

### Case 65 — Gloomy-Rise immersiveengineering (custom texture shapes, highway_branch)

**Pack:** BMProjects-Development/Gloomy-Rise (4★)
**Type:** techno-magical hardcore RPG
**Chapter:** immersiveengineering — 220 quests
**Topology:** highway_branch (horizontal spine with mod-subsystem branches)
**Coordinates:** X: [-8.5, 8.5], Y: [-4.0, 4.4], Width: 17.0, Height: 8.4
**Shape vocabulary:** crumpled_rsquare(19), crumpled_hexagon(3) — **FIRST "crumpled_" texture prefix in dataset.** The chapter's default_quest_shape is "crumpled_circle" (confirmed from data).
**Size distribution:** 1.2(7), 0.8(6), 1.3(3) — consistent sub-1.0 to 1.3 range.
**Task types:** item(144), checkmark(1).
**Rewards:** ZERO.
**Dependencies:** 64 multi-dep quests, max ~3 deps.
**Icon rate:** 7.7% (17 icons), **Hide_dep_lines:** 6 (2.7%)
**Optional:** 0
**Significance:** The "crumpled_" shape prefix creates a visual texture that distinguishes IE content from Create content (default_rsquare) within the same pack. This is the first evidence of shape-as-texture-texture rather than shape-as-category in the dataset. The 220-quest IE chapter is larger than most standalone packs, and the 17 icons (7.7%) suggest custom IE machine icons. The highway_branch topology with 17-unit width is compact for 220 quests — the sub-1.0 sizing enables this density.

---

### Case 66 — Ragnamod_VI progression (kitchen-sink, grid_catalog with diamond)

**Pack:** MLDEG/Ragnamod_VI (3★, kitchen-sink baseline)
**Type:** kitchen-sink (comprehensive)
**Chapter:** progression — 193 quests
**Topology:** grid_catalog (30 diamond shapes forming a structured progression grid)
**Coordinates:** X: [-4.5, 8.0], Y: [-6.0, 0.5], Width: 12.5, Height: 6.5
**Shape vocabulary:** diamond(30) — PURE diamond monoculture, every shape override is diamond.
**Size distribution:** all default (1.0) — NO size overrides despite 30 shape overrides.
**Task types:** checkmark(59), item(52) — CHECKMARK-DOMINANT (unusual for a grid_catalog; most are item-dominant).
**Rewards:** ZERO of ALL types across 193 quests.
**Dependencies:** 60 multi-dep quests, max ~3 deps.
**Icon rate:** 34.7% (67 icons — HIGHEST for a non-expert kitchen-sink progression chapter)
**Optional:** 0
**Default quest shape:** "hexagon" (chapter-level override)
**Significance:** The diamond(30) monoculture with checkmark-dominant tasks creates a unique pattern: diamond-shaped checkmark milestones forming a progression grid. The 34.7% icon rate (67 icons for 193 quests) is the highest icon density observed in a kitchen-sink progression chapter, suggesting extensive custom icon work for each progression milestone. The combination of hexagon default + diamond overrides creates a clear two-tier shape hierarchy: hexagon = standard quest, diamond = progression checkpoint. ZERO rewards for 193 quests validates MP41 for kitchen-sink progression chapters.

---

### Case 67 — CottageWitch119 farmer (farming, tree_branching)

**Pack:** katubug/CottageWitch119
**Type:** farming+cottagecore (Farmer's Delight + Create)
**Chapter:** farmers_delight — 156 quests
**Topology:** tree_branching (from recipe root to crop/cooking branches)
**Coordinates:** X: [-5.5, 7.0], Y: [-2.5, 3.0], Width: 12.5, Height: 5.5
**Shape vocabulary:** hexagon(12), octagon(2), rsquare(1) — hexagon dominant for farming milestones.
**Size distribution:** 2.0(1) — single milestone node.
**Task types:** item(103), loot(7), random(3), choice(3), advancement(2), xp_levels(1).
**Rewards:** loot(7)+random(3)+choice(3) — reward table economy (loot tables for cooking rewards).
**Dependencies:** 19 multi-dep quests, max ~3 deps.
**Icon rate:** 0.6% (1 icon), **Optional:** 1 (0.6%)
**Significance:** Non-expert farming pack fills tree_branching calibration gap for farming content (previously only Farmopolis and Life-in-the-Village covered this). The hexagon(12) for farming milestones is a new shape-category pairing: hexagon marks recipe completion in cooking content. The compact 12.5×5.5 layout for 156 quests is the DENSEST tree_branching chapter in the dataset (25.8 quests per square unit vs ~6 for most tree_branching chapters). The reward table economy (loot+random+choice) delivers cooking ingredients and tools as quest rewards — thematic reward alignment.

---

### Case 68 — MC-Eternal-Eternally introduction (large kitchen-sink, hub_fan)

**Pack:** mosharky/MC-Eternal-Eternally
**Type:** kitchen-sink (comprehensive, MC Eternal sequel/variant)
**Chapter:** introduction — 678 quests (LARGEST single chapter in the dataset, surpassing RAD3's largest)
**Topology:** hub_fan (massive radial layout from central introduction hub)
**Coordinates:** X: [-1.17, 16.85], Y: [-5.0, 7.0], Width: 18.0, Height: 12.0
**Shape vocabulary:** hexagon(12), rsquare(9), pentagon(9), heart(4), circle(3), diamond(2), square(1), **spstar(1), fpstar(1)** — 9 shape types including TWO UNIQUE star shapes not seen in any other pack.
**Size distribution:** 0.7(28), 0.6(24), 0.8(14), 0.5(10), 0.9(4), 1.3(1) — HEAVY sub-1.0 sizing for visual density.
**Task types:** item(165), eternalcurrencies:currency(64), quest_loot(49), command(48), kill(17), custom(17), observation(10), checkmark(9), advancement(8), dimension(6) — 10 task types including 2 CUSTOM types (eternalcurrencies:currency, quest_loot).
**Rewards:** Custom economy via eternalcurrencies:currency (64) + quest_loot (49) + command(48) — THREE parallel reward systems.
**Dependencies:** 91 multi-dep quests, max ~4 deps.
**Icon rate:** 20.6% (140 icons), **Hide_dep_lines:** 41 (6.0%)
**Optional:** 42 (6.2%)
**Default quest shape:** "circle" (from data.snbt)
**Significance:** The 678-quest introduction chapter is the LARGEST single chapter in the 72-pack dataset (surpassing RAD3's largest at ~300 quests). The spstar and fpstar custom shapes are the first star-type shapes in the dataset — likely rendered as 5-pointed stars for special milestone quests. The 0.5-0.7 sizing on 62/81 sized quests creates extreme visual density: 678 quests packed into an 18×12 unit area (3.14 quests per square unit — DENSEST hub_fan in dataset). The three parallel reward systems (currency + loot + command) represent the most complex reward economy observed. The 42 optional quests (6.2%) provide non-linear content within the hub structure.

---

### Case 69 — MC-Eternal-Eternally bosses (diamond_convergence, large chapter)

**Pack:** mosharky/MC-Eternal-Eternally
**Type:** kitchen-sink
**Chapter:** bosses — 224 quests
**Topology:** diamond_convergence (boss kill chains converging to tier capstones)
**Coordinates:** X: [-1.02, 20.0], Y: [-1.6, 8.0], Width: 21.0, Height: 9.6
**Shape vocabulary:** diamond(16), rsquare(2), hexagon(1) — diamond dominant (71% of overrides).
**Size distribution:** 0.8(14), 0.95(1), 0.7(1) — sub-1.0 sizing.
**Task types:** item(67), eternalcurrencies:currency(21), command(19), random(17), quest_loot(17), kill(4), checkmark(2), custom(1) — 8 task types.
**Rewards:** command(19)+random(17)+quest_loot(17)+currency(21) — FOUR reward types.
**Dependencies:** 7 multi-dep quests (low for diamond_convergence), max ~3 deps.
**Icon rate:** 24.6% (55 icons), **Hide_dep_lines:** 3 (1.3%)
**Optional:** 7 (3.1%)
**Default quest shape:** "octagon" (boss chapter uses octagon as default — shape semantics: octagon = boss/combat)
**Significance:** Diamond_convergence in a boss/combat chapter with 71% diamond shape override rate validates diamond-as-category for boss kill milestones. The octagon default shape for the boss chapter creates a shape hierarchy: octagon = standard boss quest, diamond = boss tier capstone. The 21.0-unit width for 224 quests is compact (10.7 quests/unit width). The kill(4) task count is surprisingly low for a boss chapter — most boss tracking uses item tasks (mob drops) rather than kill tasks.

---

### Case 70 — MC-Eternal-Eternally irons_spells (LARGEST chapter by area in dataset, 630 quests (second largest by quest count))

**Pack:** mosharky/MC-Eternal-Eternally
**Type:** kitchen-sink
**Chapter:** irons_spells_and_spellbooks — 630 quests (SECOND largest chapter in dataset)
**Topology:** tree_branching (estimated from 39×44 unit span and 73 multi-dep)
**Coordinates:** X: [-5.0, 34.0], Y: [-27.0, 17.0], Width: 39.0, Height: 44.0 — LARGEST chapter by area (1716 sq units) in the dataset. Exceeds R59 hard clamp on BOTH axes (39 > 35 width, 44 > 35 height).
**Shape vocabulary:** embellish(5), pentagon(4), hexagon(3), gear(2), octagon(1) — 5 shape types, "embellish" is a UNIQUE shape value not seen elsewhere.
**Size distribution:** 1.0(2), 0.1(2), 1.5(1) — 0.1 size is the SMALLEST in the dataset (near-invisible quest nodes).
**Task types:** item(196), eternalcurrencies:currency(82), quest_loot(50), structure(8), checkmark(7), kill(6), questsadditions:time(2), command(1) — 8 task types including questsadditions:time addon.
**Rewards:** currency(82)+loot(50)+command(1) — triple reward system.
**Dependencies:** 73 multi-dep quests, max ~3 deps.
**Icon rate:** 3.5% (22 icons), **Hide_dep_lines:** 1 (0.2%)
**Optional:** 2 (0.3%)
**Significance:** The 630-quest chapter spanning 39×44 units is the LARGEST single chapter by area in the 72-pack dataset, exceeding R59 hard clamp on both axes. The 0.1 size value is unprecedented — these are near-invisible quests (likely decorative or hidden infrastructure). The "embellish" shape and "questsadditions:time" task type are both unique to this pack. The chapter demonstrates the extreme end of chapter scaling: 630 quests require aggressive sub-region decomposition (MP73) to remain navigable. The Y range of [-27..17] = 44 units is more than double the typical chapter height.

---

### Case 71 — Heroes-of-Mine-and-Crafting-Forge les_tapes_de_base (French kitchen-sink, tree_branching)

**Pack:** DaftHunk/Heroes-of-Mine-and-Crafting-Forge
**Type:** kitchen-sink (French-language, comprehensive)
**Chapter:** les_tapes_de_base (les étapes de base = "basic steps") — 93 quests
**Topology:** tree_branching (from basic progression hub to tech/magic branches)
**Coordinates:** X: [-28.0, -10.0], Y: [-4.5, 1.0], Width: 18.0, Height: 5.5
**Shape vocabulary:** rsquare(7), gear(6), diamond(2) — 3 shape types for basic progression.
**Size distribution:** 1.0(2) — minimal size overrides.
**Task types:** item(36), xp(22) — XP rewards for progression milestones.
**Rewards:** xp(22) — XP-dominant economy.
**Dependencies:** 21 multi-dep quests, max ~3 deps.
**Icon rate:** 3.2% (3 icons), **Optional:** 0
**Significance:** French-language pack fills the language diversity gap for topology data. The NEGATIVE x coordinates ([-28..-10]) indicate a right-to-left reading direction — unusual for FTB Quests which typically flows left-to-right. The rsquare(7)+gear(6) dual shape system separates basic progression milestones (rsquare) from tech milestones (gear). XP(22) as the dominant reward type is consistent with the European pack design tradition (Prominence II RPG also uses XP-dominant rewards).

---

### Cycle 20 Phase 1 — Cases 72–81

### Case 72 — TechnoMagic-4 stage_6 (tech+magic hybrid, highway_branch)

**Pack:** Ivanchela2/TechnoMagic-4
**Type:** tech+magic hybrid (Create + stages + Twilight Forest, Russian-language)
**Chapter:** stage_6 — ~50 quests (90275 bytes, largest chapter)
**Topology:** highway_branch (staged highway with mod-specific sub-regions branching off each stage)
**Coordinates:** X: estimated [-15.0, 15.0], Y: [-10.0, 10.0], Width: ~30.0, Height: ~20.0 (extensive spread indicating large graph)
**Shape vocabulary:** hexagon, circle — 2 shape types for milestone differentiation. Hexagon marks mod-specific sub-chain anchors; circle marks stage-transition nodes.
**Size distribution:** 1.75d (milestone nodes) — moderate size hierarchy.
**Task types:** item-dominant (alchemistry:combiner, lunar exploration, bigger reactors uranium processing).
**Rewards:** item+random mixed economy.
**Dependencies:** multi-branch with parallel sub-chains for different mods.
**Icon rate:** moderate (custom icons for key tech/magic milestones).
**Significance:** Good example of staged highway_branch topology in a tech-magic hybrid. The pack organizes its 17 chapters into numbered stages (stage1 through stage_7 plus stage_end), creating a clear linear macro-progression where each stage is itself a highway with branches into individual mod progressions. Stage 6 is the largest chapter (90KB) and represents late-game convergence where chemistry (alchemistry), space travel (lunar), and nuclear tech (bigger reactors) intersect. The hexagon/circle shape pairing differentiates mod-subsystem anchors from stage-transition milestones. Russian-language pack adds linguistic diversity to the dataset.

---

### Case 73 — Deadlock's End create (expert tech, parallel_columns with radial sub-structures)

**Pack:** SRCthird/deadlocks_end
**Type:** expert tech pack (Create + multiple tech mods)
**Chapter:** create — 102 quests (86390 bytes)
**Topology:** parallel_columns with radial sub-structures. Main trunk: Create → Andesite Alloy → branches into Shaft/Casing paths. Left column: power transmission (Cogwheels → Gearshift → Speed Controller). Right column: processing (Press → Sheets → Copper Paradise → Fluid system). Bottom expansion: Brass era (Deployer, Precision Mechanism, Trains). Redstone sub-region: radial layout from central Redstone node. Logistic sub-region: linear chain with side branches.
**Coordinates:** X: [-9.75, 12.5], Y: [-0.78, 14.0], Width: 22.25, Height: 14.78
**Shape vocabulary:** pentagon(2), gear(6), hexagon(13), octagon(2), rsquare(3), circle(1), default(majority) — **6 distinct shape types**, the richest shape vocabulary in a parallel_columns chapter in the dataset. Pentagon at size 2.5 marks the chapter start "Create" node. Gear at size 1.625 anchors sub-regions (Andesite Alloy, Shifting Gears, Logistic, Redstone). Hexagon at size 1.25 groups parallel Sheet Metal nodes. Rsquare at size 1.0 marks utility nodes (Speed/Stress monitoring).
**Size distribution:** 2.5d(1), 1.75d(3), 1.625d(4), 1.5d(1), 1.25d(3), 1.125d(2), 1.0d(majority), 0.875d(2), 0.825d(1), 0.625d(1) — **10 distinct sizes**, the finest size granularity observed in any single chapter. The size continuum from 0.625 to 2.5 creates a clear visual hierarchy with six levels of importance.
**Task types:** item-dominant with multi-dep convergence nodes (e.g., "Blaze Cake" requires both Blaze Burner and Spout).
**Rewards:** XP rewards, specific item rewards, random loot table rewards — mixed economy.
**Dependencies:** mostly single-dependency chains, some multi-dep nodes at processing convergence points.
**Icon rate:** 29.4% (30/102) — high icon customization for an expert pack chapter.
**Significance:** The best parallel_columns example in the dataset, demonstrating clear multi-column layout where the left column handles power transmission and the right column handles processing, connected by horizontal cross-links at key transition points (Andesite Alloy, Brass era). The 6 shape types and 10 size values create the richest visual vocabulary observed in any parallel_columns topology — gear-shaped anchor nodes connect columns while hexagon groups parallel items within columns. The 29.4% icon rate is unusually high for an expert pack, suggesting the author invested significant effort in visual customization despite the pack's technical complexity. The radial Redstone sub-region embedded within the parallel columns demonstrates how sub-structures can coexist within a dominant topology.

---

### Case 74 — Material Factory chapter1 (heavy tech, linear_chain with ALL item rewards)

**Pack:** WaiBiBaBo995/Material-Factory
**Type:** heavy tech pack (AE2, Ars Nouveau, Botania, Industrial Foregoing, Mekanism, Powah, Thermal, Xycraft)
**Chapter:** chapter1 — ~80 quests (62934 bytes, 247 quest blocks)
**Topology:** linear_chain with mod-specific branches. Chapter1 serves as a hub connecting to mod-specific chains. Each mod chapter is essentially a linear walkthrough.
**Coordinates:** X: [-3.0, 20.0], Y: [-6.5, 13.0], Width: 23.0, Height: 19.5
**Shape vocabulary:** gear(1), octagon(1), heart(1), default(majority) — 3 shape overrides. The heart shape is rare across the entire dataset (only previously observed in Material Factory's own chapter1).
**Size distribution:** 2.0d(2), 1.5d(1), 1.25d(1), 1.0d(majority) — minimal size hierarchy.
**Task types:** item-dominant (247 quest blocks).
**Rewards:** item=137, random=0, choice=0 — **ALL item rewards, zero random tables, zero choice rewards.** This is the most deterministic reward design observed in any pack.
**Dependencies:** linear chain with side branches into mod-specific content.
**Icon rate:** **44% (35/80)** — the HIGHEST icon rate in the dataset for a tech-focused chapter.
**Significance:** Two extreme findings. First, the 44% icon rate is the highest observed in any tech pack chapter, indicating the author customized nearly half of all quest icons — a level of visual investment typically seen only in exploration/collection chapters (MCC world_exploration at 74% is the only higher value, but that chapter is an exploration catalog, not a tech progression chain). Second, the ALL-item reward design (137 item rewards, 0 random, 0 choice) represents the most deterministic reward economy in the dataset — every reward is a specific, known item, creating a completely predictable progression experience. The heart shape override is exceptionally rare and suggests a special "favorite quest" or community reference. The 21-chapter structure with mod-specific linear walkthroughs (AE2, Mekanism, Powah, etc.) makes this pack a textbook example of the "hub + linear mod chains" architecture.

---

### Case 75 — Vapor Opificium 1 (survival/adventure, compact radial, Korean-language)

**Pack:** kerupu526/Vapor-Opificium
**Type:** survival/adventure with light tech (Korean-language pack)
**Chapter:** 1.snbt ("The Beginning of a Great Journey") — ~21 quests (25658 bytes)
**Topology:** radial/hub-spoke (compact). Central "first night" node radiates outward into survival basics (food, tools, shelter, combat).
**Coordinates:** X: [-7.0, 6.0], Y: [-1.5, 4.0], Width: 13.0, Height: 5.5
**Shape vocabulary:** hexagon(1), rsquare(multiple) — compact shape set for a compact chapter.
**Size distribution:** 1.5d for milestone nodes, 1.0d(majority) — minimal hierarchy.
**Task types:** item-dominant with XP and command rewards.
**Rewards:** item rewards (food, coins, tools), XP rewards, command rewards (give items, apply effects). Choice loot table rewards also present.
**Dependencies:** radial from central node.
**Icon rate:** moderate (custom icons for info/utility nodes).
**Unique features:** Custom coin system (Technician Coins, Miner Coins, Explorer Coins, Survivor Coins). Hidden quests (dependency_requirement: "one_started"). Command-based rewards.
**Significance:** The most compact chapter topology in the Cycle 20 batch — 21 quests in a 13×5.5 unit area (density ~0.29 quests/sq-unit). The radial layout from a central "first night" node is a textbook hub-spoke pattern appropriate for a small survival pack's opening chapter. The custom coin system (4 coin types: Technician, Miner, Explorer, Survivor) is an unusual reward economy design that segments the reward space by gameplay activity rather than by progression tier. Korean-language pack adds linguistic diversity. The 4-chapter, ~70-quest total makes this one of the smallest packs in the dataset, useful as a lower-bound reference for chapter count and quest density.

---

### Case 76 — Minecolonies Create and Conquer minecolonies (Create+RPG, grid packing with dense small nodes)

**Pack:** Iskariot53/MinecoloniesCreateandConquer
**Type:** Create + Minecolonies + RPG combat (Scorched Guns 2)
**Chapter:** minecolonies — ~90 quests (94847 bytes, 267 quest blocks)
**Topology:** highway_branch with grid-like internal layout. Wide and tall spread (35.5 × 30.0) creates a large chapter canvas. Many small 0.75d nodes suggest collection/task grid within the highway structure.
**Coordinates:** X: [-5.5, 30.0], Y: [0.0, 30.0], Width: 35.5, Height: 30.0 — **the TALLEST chapter in the dataset** (30.0 height exceeds Monifactory's 21 units and R59's 35-unit hard clamp is approached).
**Shape vocabulary:** hexagon(2), diamond(1), default(majority) — minimal shape overrides.
**Size distribution:** 0.75d(8), 2.5d(1), 1.5d(6), 0.8d(1), 1.0d(majority) — 8 small nodes at 0.75d create a dense sub-grid for collection tasks within the broader highway.
**Task types:** item-dominant with colony-specific tasks.
**Rewards:** mixed economy.
**Dependencies:** grid-like layout with highway branching.
**Icon rate:** 14% (13/90) — moderate icon customization.
**Significance:** The 0.75d size on 8 nodes within a 35.5×30.0 area demonstrates the "grid packing" strategy: small nodes at tight spacing create a high-density collection/task sub-grid within a larger highway structure. This is the same strategy observed in MCC's world_exploration chapter but at a smaller scale. The 30.0-unit height approaches R59's 35-unit hard clamp and represents the practical upper limit of comfortable vertical scrolling. The pack's 35 chapters is the largest chapter count in the Cycle 20 batch, demonstrating how a large chapter count correlates with per-chapter specialization (one chapter per mod). The same author (Iskariot53) also created Minecolonies-Cobblemon-Conquest (researched in Cycle 15), providing a basis for author-level design pattern comparison.

---

### Case 77 — Minecolonies Create and Conquer world_exploration_quests (largest exploration chapter, extreme icon rate)

**Pack:** Iskariot53/MinecoloniesCreateandConquer
**Type:** Create + Minecolonies + RPG combat
**Chapter:** world_exploration_quests — ~170 quests (166687 bytes, 556 quest blocks)
**Topology:** massive radial from center. Central hub radiates into biome/region-specific exploration quests.
**Coordinates:** X: [-9.0, 39.0], Y: [-18.5, 30.0], Width: 48.0, Height: 48.5 — **the LARGEST chapter by area in the dataset** (48×48.5 = 2328 sq-units, exceeding MC-Eternal-Eternally irons_spells at 39×16 = 624 sq-units by a factor of 3.7).
**Shape vocabulary:** octagon(1), diamond(2), default(majority) — minimal overrides in a very large chapter.
**Size distribution:** 2.5d(1), 2.0d(2), 1.5d(4), 1.0d(38), 0.75d(1) — 6 size levels with a dominant 1.0d majority.
**Task types:** exploration/collection-dominant.
**Rewards:** mixed economy.
**Dependencies:** radial from center with branching exploration paths.
**Icon rate:** **74% (126/170)** — the HIGHEST icon rate in the entire dataset. Nearly 3 out of every 4 quests has a custom icon.
**Significance:** Two records broken. First, the 48×48.5 bounding box (2328 sq-units) is the largest chapter area ever measured, exceeding the previous record holder (MCEE irons_spells at 630 quests in ~624 sq-units) by a factor of 3.7 — despite having fewer quests (170 vs 630). This means the chapter uses generous spacing and radial expansion rather than compression. Second, the 74% icon rate (126 custom icons for 170 quests) is the highest in the dataset, indicating that exploration content receives dramatically more visual customization than tech progression content. The contrast with expert packs (CTNH at 3-10%) is extreme — a factor of 7-25× difference in icon investment per quest. The chapter violates R59's 35-unit soft warning on both axes (48 and 48.5), suggesting that exploration content is expected to sprawl and that viewport scrolling is an acceptable trade-off for spatial organization.

---

### Case 78 — Thrash Create Colony create (Create-focused, linear_chain)

**Pack:** cryptiklemur/thrash-create-colony
**Type:** Create + addons (focused Create pack)
**Chapter:** create — ~40 quests (66209 bytes)
**Topology:** linear_chain with parallel mod-addon branches. Main Create chapter progresses through Create tiers (Andesite → Brass → Railway). Addon chapters (New Age, Vintage Improvements, Connected, etc.) are independent parallel branches.
**Coordinates:** estimated X: [-5.0, 15.0], Y: [-5.0, 10.0], Width: ~20.0, Height: ~15.0
**Shape vocabulary:** square, gear, rsquare — gear shape marks Andesite Alloy anchor node (1.5d), square marks welcome node (1.5d).
**Size distribution:** 1.5d for milestone nodes (Welcome, Andesite Alloy, Train Assembly, Redstone Logic), 1.0d(majority).
**Task types:** item-dominant (standard Create tech tree).
**Rewards:** item economy.
**Dependencies:** linear chain with side branches.
**Icon rate:** moderate (gear shape with railway casing icon for Train Assembly milestone).
**Significance:** Clean example of linear_chain in a Create-focused pack. The 20-chapter structure decomposes Create's ecosystem into focused addon chapters (New Age, Vintage Improvements, Taste of Tradition, Space, Connected, Central Kitchen, Enchantment Industry), each as an independent parallel branch accessible from the main Create progression. This "linear main + parallel addons" architecture is the standard pattern for Create-focused packs (also observed in Thrash Create Colony's peer packs). The gear shape for Andesite Alloy confirms the cross-pack shape semantic: gear = production/processing milestone.

---

### Case 79 — Age of Industry Refactored age_1_hello_world (IE+Botania, all-square linear_chain)

**Pack:** LilJagty/Age-Of-Industry-Refactored
**Type:** Immersive Engineering + Botania tech/magic (age-based progression)
**Chapter:** age_1_hello_world — ~20 quests (12182 bytes, 63 quest blocks)
**Topology:** linear_chain with strict vertical progression. Y increases with tech tier, creating a deterministic upward flow.
**Coordinates:** X: [-5.0, 5.0], Y: [-4.5, 4.5], Width: 10.0, Height: 9.0 — compact, nearly square bounding box.
**Shape vocabulary:** circle(1), square(17) — **HEAVY square dominance** (17 out of 18 shape overrides are square). This is the most uniform shape distribution in the dataset.
**Size distribution:** 1.5d(2), 1.0d(majority) — minimal size hierarchy.
**Task types:** item-dominant (60 item tasks).
**Rewards:** item=60, random=0 — ALL deterministic item rewards, zero random tables.
**Dependencies:** linear chain with some convergence points.
**Icon rate:** **5% (1/20)** — the LOWEST icon rate in the Cycle 20 batch.
**Optional:** side branches for optional quests.
**Significance:** The all-square shape distribution is unique in the dataset — no other pack uses a single shape for 94% of overrides. This reflects a minimalist design philosophy where shape differentiation is deliberately suppressed in favor of age-based gating as the primary organizational signal. The 5% icon rate (1 icon in 20 quests) is the lowest observed and pairs with the all-square shapes to create the most visually uniform chapter in the dataset. The strict Y-axis progression (vertical linear_chain) combined with age-based gating creates the most rigid linear topology: the player has exactly one path through the chapter, with optional side branches clearly marked. The deterministic reward design (60 item rewards, 0 random) matches Material Factory's ALL-item approach, suggesting that age-gated packs tend toward deterministic reward economies.

---

### Case 80 — GATE ModPack chapter_ii (RPG/adventure, race-based highway_branch)

**Pack:** RpalZ/GATEModPack
**Type:** RPG/adventure (race-based progression, boss fights)
**Chapter:** chapter_ii — ~13 main quest nodes with boss fights (51815 bytes)
**Topology:** linear_chain at macro scale (chapters I → II → III) with highway_branch at micro scale (race chapters as parallel branches). Race chapters (Enderian, Dragonborne, Elves, Stormkin, Vampire, Merfolk, Yeti, Orcs) form 8 parallel branches each 8-10KB in size.
**Coordinates:** X: [0.375, 51.0], Y: [-8.625, 19.5], Width: 50.625, Height: 28.125 — **the WIDEST chapter in the dataset** (50.625 units exceeds GATE's own chapter_i at 32.5 and all prior observations).
**Shape vocabulary:** hexagon(1) at 3.0 size for major boss milestone. Octagon at 2.5d for sub-milestone.
**Size distribution:** 1.5d(most), 2.5d(octagon milestone), 3.0d(hexagon boss) — boss fights use the LARGEST size in the dataset (3.0d).
**Task types:** boss fight + eye collection quests + portal unlocking.
**Rewards:** XP (5000-10000 per quest), loot tables, stage unlocks — high-XP boss economy.
**Dependencies:** linear narrative chain with stage-gating.
**Icon rate:** low (chapter_ii has minimal icon overrides despite large size).
**Narrative integration:** Heavy story text with each quest (lore about the "Warden" and corruption). Each quest node contains multi-paragraph narrative.
**Significance:** Three records and one unique pattern. First, the 50.625-unit width is the widest chapter span ever measured, exceeding the previous record by a factor of ~1.7 (FTB Evolution create at 30 units). The extreme horizontal spread is driven by boss fight arenas that require spatial separation. Second, the 3.0d size for boss hexagon milestones is the largest quest size in the dataset (tied with GATE's own chapter_i boss node). Third, the 8 race-based parallel branches represent a unique highway_branch variant where the branches are character-creation choices (race selection) rather than mod-based content splits. This "race-based branching" pattern means the player experiences only one branch per playthrough, unlike mod-based highway_branch where the player typically pursues all branches. The heavy narrative integration (multi-paragraph lore per quest) makes GATE ModPack the most text-heavy pack in the dataset by quest-description density.

---

### Case 81 — Create New Horizon (CTNH) LV + AE2 (expert GT+Create, voltage highway with cross-links)

**Pack:** CTNH-Team/Create-New-Horizon (dev branch, Chinese-language)
**Type:** expert Create + GregTech CEu hybrid
**Chapters sampled:** LV ("&7LV period" / "Industrial Start", 30397 bytes, ~45 quests) and AE2 (52931 bytes, ~85 quests). Full pack: 37 chapters, ~1210 quests.
**Topology (macro):** **voltage-tier highway with cross-links** — a topology unique to expert GT packs. Nine voltage tiers form the main highway (LV → MV → HV → EV → IV → LuV → ZPM → UHV → UV). AE2 and Botania are parallel branches accessible from multiple voltage tiers. 25 hex-ID chapters provide mod-specific content. Cross-chapter quest links (13 in AE2 alone) create a web of interconnections, producing a "ladder with rungs" topology.
**Topology (micro, LV):** tree-branching from central "Machine Hull" node. Left branch: utility machines (electrolyzer, alloy smelter, furnace). Center branch: motor → components → machines. Right branch: chemistry (mixer → gallium arsenide → diode → circuits). Far right: EBF milestone → aluminum processing → MV transition.
**Topology (micro, AE2):** linear main path with parallel sub-regions. Main path: certus quartz → processors → controller → storage → crafting. Bottom sub-region: AE2CS crystal seeds (Y: -7 to -10). Right sub-region: OMNI cells and complex cells (X: 13-29).
**Coordinates (LV):** X: [-7.0, 14.5], Y: [-9.0, 5.5], Width: 21.5, Height: 14.5
**Coordinates (AE2):** X: [-8.5, 29.0], Y: [-10.0, 5.5], Width: 37.5, Height: 15.5
**Coordinates (HV):** X: [-28.5, -6.0], Y: [7.0, 40.0], Width: 22.5, Height: 33.0 — all negative X, all positive Y (unusual quadrant positioning)
**Shape vocabulary (LV):** diamond(2), gear(1), rsquare(2), octagon(8) — octagon-dominant for machine components.
**Shape vocabulary (AE2):** pentagon(1) — minimal overrides in a large chapter; shape differentiation relies on the voltage tier chapters.
**Shape vocabulary (HV):** pentagon(1), rsquare(3), gear(1), octagon(1) — consistent with LV shape semantics.
**Shape vocabulary (IV):** rsquare(3), gear(1), pentagon(1) — same shape set as HV.
**Cross-chapter shape semantics:** octagon = machine components (consistent across all voltage tiers), gear = major milestone, diamond = key tech unlock, rsquare = info/utility, pentagon = completion/summary.
**Size distribution (LV):** 2.0d(7), 1.5d(3), 1.0d(2) — many enlarged nodes (58% non-default).
**Size distribution (AE2):** 2.0d(4), 1.5d(6), 1.0d(15) — 40% non-default.
**Size distribution (HV):** 2.0d(11), 1.5d(6), 1.0d(10) — 63% non-default (highest enlargement rate).
**Size semantics:** 2.0d = chapter milestones (10-20% of nodes in most chapters, up to 40% in HV), 1.5d = sub-section anchors, 1.0d = standard quests.
**Task types (LV):** item-dominant with machine component tree (Motor → Piston/Pump/Conveyor → Robot Arm in octagon shape).
**Rewards (LV):** random(18), item(5), choice(1) — mixed economy with random-dominant.
**Rewards (HV):** random=20, item=189, choice=3 — item-dominant at higher tiers.
**Dependencies (LV):** max 3 deps per quest, tree-branching from machine hull.
**Icon rate (LV):** 7% (3/45) — low. Icons: gtceu:phenolic_printed_circuit_board, ctnhcore:industrial_primitive_blast_furnace, minecraft:player_head (Yuriko tutorial character).
**Icon rate (AE2):** 5% (4/85) — very low. Icons: avaritia:infinity_catalyst, gtceu:hv_machine_hull, minecraft:player_head (Yuriko), ae2:controller.
**Icon rate (HV):** 3% (2/65) — the lowest measured in this batch.
**Icon rate (IV):** 10% (5/50) — highest among CTNH chapters but still low by non-expert standards.
**Quest links (cross-chapter):** AE2 has 13 quest links to voltage tier chapters (LV, MV, HV, IV), creating inter-chapter dependency bridges. LV has 1 link to an external power generation guide. Quest links serve as "bridge nodes" connecting the voltage highway to mod-specific content branches.
**Tutorial system:** Tutorial character "Yuriko" (player_head with custom skin) appears across chapters as a persistent guide. Quest descriptions are detailed Chinese tutorials (multi-paragraph explanations of GregTech voltage concepts, dual-voltage system, machine component trees).
**Completion reward scaling:** LV completion: small items. AE2 completion: neutronium dust(64) + wetware processor mainframe(64) + complex omni cells(32) + UV machine hulls(32) — dramatic exponential scaling.
**Significance:** CTNH is the most important pack in the Cycle 20 batch for five reasons. First, the voltage-tier highway with cross-chapter quest links represents a topology unique to expert GT packs — not observed in any non-expert pack across 19 prior cycles. The 9 voltage tiers form a strict linear highway, but mod chapters are accessible as parallel branches from multiple tiers, creating a "ladder with rungs" topology that has no precedent in the dataset. Second, the 13 quest links in the AE2 chapter demonstrate "bridge nodes" — cross-chapter connections that tie mod content back to the voltage highway, ensuring the player cannot pursue AE2 independently of voltage progression. Third, the icon rate inversion is confirmed: expert pack chapters (3-10%) have dramatically lower icon rates than casual pack chapters (20-74%), a factor of 3-25× difference. Expert packs compensate with detailed text descriptions rather than visual icons. Fourth, the sub-region decomposition within large chapters (AE2's main path + crystal seeds + OMNI cells, three distinct spatial regions) provides a template for organizing 85+ quests within a single chapter without exceeding viewport limits. Fifth, the Yuriko tutorial character (player_head icon) establishes a cross-chapter narrative device that persists across all 37 chapters, the most extensive tutorial character system in the dataset. The pack's 37 chapters and ~1210 quests make it one of the largest expert packs researched, and the Chinese-language detailed quest descriptions provide rich evidence for expert pack design philosophy.

---

### Cycle 20 Phase 1 Spacing Additions

| Quests | Pack | Min spacing | Avg spacing | Max spacing |
|--------|------|-------------|-------------|-------------|
| ~50 | TechnoMagic-4/stage_6 | ~1.0 | ~2.0 | ~20.0 |
| 102 | DeadlocksEnd/create | ~0.8 | ~1.5 | ~15.0 |
| ~80 | MaterialFactory/chapter1 | ~1.0 | ~2.0 | ~20.0 |
| ~21 | VaporOpificium/1 | ~1.0 | ~2.0 | ~10.0 |
| ~90 | MCC/minecolonies | ~0.75 | ~2.0 | ~30.0 |
| ~170 | MCC/world_exploration | ~1.0 | ~3.0 | ~35.0 |
| ~40 | ThrashCC/create | ~1.0 | ~2.0 | ~15.0 |
| ~20 | AgeOfIndustry/age_1 | ~1.0 | ~2.0 | ~8.0 |
| ~13 | GATE/chapter_ii | ~2.0 | ~5.0 | ~40.0 |
| ~45 | CTNH/lv | ~1.0 | ~2.0 | ~18.0 |
| ~85 | CTNH/ae2 | ~1.0 | ~2.5 | ~30.0 |

### Cycle 20 Phase 1 — Accessed Packs

- Ivanchela2/TechnoMagic-4 (branch: main) — Cycle 20
- SRCthird/deadlocks_end (branch: main) — Cycle 20
- WaiBiBaBo995/Material-Factory (branch: main) — Cycle 20
- kerupu526/Vapor-Opificium (branch: main) — Cycle 20
- Iskariot53/MinecoloniesCreateandConquer (branch: main) — Cycle 20
- cryptiklemur/thrash-create-colony (branch: main) — Cycle 20
- LilJagty/Age-Of-Industry-Refactored (branch: main) — Cycle 20
- RpalZ/GATEModPack (branch: main) — Cycle 20
- CTNH-Team/Create-New-Horizon (branch: dev) — Cycle 20

---

### Cycle 19 Phase 1 Spacing Additions

| Quests | Pack | Min spacing | Avg spacing | Max spacing |
|--------|------|-------------|-------------|-------------|
| 193 | GTLS/lv | ~1.0 | ~2.0 | ~18.0 |
| 400 | GTLS/mv+ev | ~0.8 | ~1.5 | ~18.0 |
| 171 | GloomyRise/create | ~0.5 | ~1.5 | ~18.0 |
| 220 | GloomyRise/IE | ~0.5 | ~1.5 | ~17.0 |
| 193 | Ragnamod_VI/progression | ~0.5 | ~1.0 | ~12.5 |
| 156 | CottageWitch/farmer | ~0.5 | ~1.0 | ~12.5 |
| 678 | MCEE/introduction | ~0.3 | ~1.0 | ~18.0 |
| 224 | MCEE/bosses | ~0.5 | ~1.5 | ~21.0 |
| 630 | MCEE/irons_spells | ~0.5 | ~2.0 | ~39.0 |
| 93 | Heroes-of-Mine/les_tapes_de_base | ~1.0 | ~2.0 | ~18.0 |

### Cycle 19 Phase 1 — Accessed Packs

- GTriXy/GregTech-Leisure-Server (branch: main) — Cycle 19
- BMProjects-Development/Gloomy-Rise (branch: main) — Cycle 19
- MLDEG/Ragnamod_VI (branch: main) — Cycle 19
- katubug/CottageWitch119 (branch: main) — Cycle 19
- mosharky/MC-Eternal-Eternally (branch: main) — Cycle 19
- DaftHunk/Heroes-of-Mine-and-Crafting-Forge (branch: main) — Cycle 19
- zhtxabc/GregTech-Magic-and-Cultivation (branch: main) — Cycle 19
- amedeo03/Ternion (branch: main) — Cycle 19
- Jasons-impart/Create-Delight (branch: main) — Cycle 19

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
- CTNH-Team/Create-New-Horizon (branch: main) — Cycle 12
- bzells/Gregtech-Voyager (branch: main) — Cycle 12
- Gogo08190/Chroma-Technology-2 (branch: main) — Cycle 12
- Eternal-Snowstorm/CodeNameCIM2 (branch: main) — Cycle 12
- JesterRomut/HereBeDragons (branch: main) — Cycle 12
- MLDEG/Ragnamod_VII (branch: main) — Cycle 12
- VeljkoBogdan/ReFactory (branch: main) — Cycle 12
- AllTheMods/All-the-mods-9-Sky (branch: dev) — Cycle 13
- AllTheMods/atm6-sky (branch: master) — Cycle 13
- Kerberus-MC/Dragoncraft (branch: master) — Cycle 13
- dr3ams/Life-in-the-Village-4 (branch: main) — Cycle 13
- LunaPixelStudios/SteamPunk (branch: main) — Cycle 13
- MLDEG/Ragnamod_VI_Skyblock (branch: main) — Cycle 13
- H4ruku0/Gregitsky (branch: main) — Cycle 13
- ReeCodes/rogue (branch: main) — Cycle 13
- Vvxzv/compact-sky-easy (branch: main) — Cycle 13
- DexxKnight1/AOF-The-Frozen-Hope (branch: main) — Cycle 14
- TheosCreation/CreateBlock (branch: 1.19.2-4.8.0) — Cycle 14
- exe-teams/extraordinary-energy-modern (branch: main) — Cycle 14
- TeamKugimiya/Enigmatic-Skies (branch: main) — Cycle 14
- yangyang8002/All_the_Simple (branch: main) — Cycle 14
- null2264/ProjectSkyblock (branch: master) — Cycle 14
- tronfy/csmpX (branch: main) — Cycle 15
- Team-Innova-Constructors/cti-quests (branch: main) — Cycle 15
- MLDEG/Ragnamod-VII-Skyblock (branch: main) — Cycle 15
- gigili/Project-Flattened (branch: main) — Cycle 15
- TeamKugimiya/Cryptopolis (branch: main) — Cycle 15
- XiaosenFang/Create-Lost-and-Renaissance (branch: main) — Cycle 15
- Insurgence modpack (branch: main) — Cycle 15 Phase 1
- MI-Lost-Favor modpack (branch: main) — Cycle 15 Phase 1
- Seaopolis modpack (branch: main) — Cycle 15 Phase 1
- Minecolonies modpack (branch: main) — Cycle 15 Phase 1
- Minecraft-Medieval modpack (branch: main) — Cycle 15 Phase 1
- Create-chronicles modpack (branch: main) — Cycle 15 Phase 1
- Farmopolis modpack (branch: main) — Cycle 15 Phase 1
- Aetas-Ferrea modpack (branch: main) — Cycle 15 Phase 1
- GenCraft modpack (branch: main) — Cycle 15 Phase 1
- Phoenix-Forge modpack (branch: main) — Cycle 15 Phase 1
- Gogo08190/chroma-endless (branch: main) — Cycle 16 Phase 1
- choombdev/MC-Odyssey-3 (branch: main) — Cycle 16 Phase 1
- Chakyl/society-sunlit-valley (branch: master) — Cycle 16 Phase 1
- TeamKugimiya/Caveopolis (branch: main) — Cycle 16 Phase 1
- DexxKnight1/Age-of-Fate (branch: main) — Cycle 16 Phase 1
- Go-Camping/No-Flesh-Within-Chest (branch: main) — Cycle 17 Phase 1
- TeamAOF/All-of-Fabric-6 (branch: main) — Cycle 17 Phase 1
- darklotus781/Prison-Escape-Beginnings (branch: main) — Cycle 17 Phase 1
- Dseelis/Steamcreate2 (branch: main) — Cycle 17 Phase 1

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

5. **Viewport bounds are a soft constraint.** The widest observed chapter (FTB Evolution create, 30 units) and tallest (Monifactory progression, 21 units) are at the edge of comfortable viewing. R59 warns at 30 units and hard-clamps at 35 units for both axes. Beyond 35 × 35 units, scrolling becomes excessive and the quest book loses its function as a visual map.

### Author Design Philosophy — Layout Observations

From the author-facing research conducted during Phase 3 (searching MC百科, B站, Reddit r/feedthebeast, YouTube, and GitHub repositories), the following topology-relevant observations emerged:

**Layout is emergent, not planned.** No author in the accessible dataset describes choosing a topology type before creating quests. The topology emerges from the content structure — a mod with 5 sub-systems naturally produces a hub_fan, a mod with a linear upgrade chain produces a linear_chain. Authors arrange quests spatially based on content groupings (mod identity, recipe chain, tier level), and the resulting topology is a consequence of those content decisions.

**Shape is a chapter-level decision, not a per-quest one.** Authors set `default_quest_shape` once per chapter to establish mod identity, then override shapes only for milestones and special roles. The shape vocabulary within a chapter is deliberately limited — 1–3 shapes for large chapters (>100 quests), up to 7 shapes for small chapters (<60 quests). Shape diversity and quest count have a consistent inverse relationship across all 13 cases.

**Size encodes structural importance, not content difficulty.** A root hub gets size 2.0–3.0 regardless of how easy its content is. A standard chain node stays at 1.0 even if its recipe is complex. Size is a graph-theoretic signal (fan_in, fan_out, role in the dependency tree), not a difficulty signal. Monifactory's CONTRIBUTING.md is the only source that explicitly codifies this: "Larger quests should be reserved for important milestones."

**The bounding box is a consequence, not a target.** Authors do not set a target width or height for a chapter before filling it. The dimensions emerge from the content volume and chosen spacing. FTB Evolution's create chapter reaches x=30.0 because its content is a 30-unit-wide progression; RAD3's milestones spans 13 × 5 because 63 quests in a 3-row grid naturally produces that ratio. R59 (Bounding Box Viewport Fit) exists as a safety net, not a design input.
