# Phase 4 Cycle 11 — Reviewer C: Practical Usability Review

> **Role:** Reviewer C — Practical Usability
> **Scope:** `topology-coordinates.md` (layout algorithm + constraint formulas) and `progression-rules.md` (R55–R64)
> **Core question:** Can an AI agent using the ftb-quests skill actually execute these algorithms and rules during quest generation?
> **Date:** 2026-07-12

---

## Usability Score: 6 / 10

The document pair is the most rigorous layout specification ever produced for this skill — the pseudocode is clear, the constraint formulas are well-bounded, and the real-case data is genuinely useful as calibration. However, several structural mismatches between "what the document describes" and "what an LLM agent can do in a single generation pass" reduce practical usability below what the theoretical quality deserves. The gap is fixable.

---

## 1. Layout Algorithm 6-Step Pseudocode — Executability Assessment

### Phase 1 (Dependency Graph Analysis): USABLE — 8/10

**What works:** Building an adjacency list, computing depth via BFS/DFS, and calculating fan-in/fan-out are all straightforward graph operations. An LLM can perform these on a quest list of any realistic size (up to ~200 quests per chapter).

**Problem:** The pseudocode says "BFS/DFS from root, depth[node] = max(depth[parent] + 1)" but doesn't specify which traversal to use or how to handle multi-root chapters (chapters with multiple independent root nodes). In practice, many real chapters have 2–3 roots (e.g., ATM-10 basic_power has a central root plus optional-side roots).

**Fix needed:** Add explicit handling for multi-root: "If multiple roots exist, compute depth independently from each root, then take the maximum depth for any node reachable from multiple roots."

### Phase 2 (Topology Classification): CONDITIONALLY USABLE — 6/10

**What works:** The classification decision tree is a clear if/elif chain with numeric thresholds. Given the Phase 1 outputs (depth, convergence, divergence), the computation is direct.

**Problems:**

1. **`has_grid` definition is fragile.** The condition `all quests have 0 or 1 dependencies AND max_width > max_depth * 0.5` would misclassify a linear chain with no dependencies as a grid. A 6-quest linear chain with 0 dependencies would have max_width=6, max_depth=0, and `6 > 0 * 0.5 = true`. The `has_grid` flag needs a minimum quest count (e.g., `len(quests) >= 20`) to avoid false positives on small chains.

2. **Region decomposition is not specified.** The document says "classification applies per-region, not just per-chapter" but never defines how to identify regions. The ATM-10 create chapter (Case 11) has 5 named regions, but the decomposition is described in terms of coordinate clustering — which means you need coordinates to identify regions, but you need the topology classification to assign coordinates. This is a circular dependency.

3. **Threshold values lack justification for edge cases.** What happens when `max_depth = 5` and `max_width = 4`? The first condition (`max_depth >= 6`) fails, the second (`has_hub and max_width >= 4`) catches it as hub_fan — but it might actually be a tree_branching. The fallback to linear_chain at the end is too aggressive; many ambiguous cases would default incorrectly.

**Fix needed:** (a) Add `len(quests) >= 15` guard to `has_grid`. (b) Define region decomposition as a pre-step (e.g., "group quests by connected component if the dependency graph is disconnected, or by mod-id prefix if available"). (c) Add a confidence score to classification — if multiple conditions are close to thresholds, flag as "ambiguous topology" and recommend the user choose.

### Phase 3 (Initial Coordinate Assignment): PARTIALLY USABLE — 5/10

**What works:** Each topology type has concrete coordinate formulas with real numbers. LINEAR_CHAIN, PARALLEL_COLUMNS, and GRID_CATALOG are directly computable — the AI can produce exact x/y values in one pass.

**Problems:**

1. **HUB_FAN requires trigonometric computation.** `cos(angle)` and `sin(angle)` are not reliable in LLM execution — the model frequently produces approximate or incorrect trigonometric values. For 8 children at 45-degree intervals, the AI would need to compute cos(−90°), cos(−45°), cos(0°), cos(45°), etc. While these are standard angles, less common fan counts (7, 11) produce non-standard angles where the AI will hallucinate coordinate values.

2. **DIAMOND_CONVERGENCE assumes exactly two paths.** The algorithm defines `left_path` and `right_path` with `get_path(root, convergence_node, side="left"/"right")`, but real diamond topologies often have 3+ divergent paths (e.g., ATM-10 allthemodium has upper branch, lower branch, and side explorations). The `get_path` function is undefined — which path does the AI choose when multiple paths exist between root and convergence?

3. **TREE_BRANCHING recursive layout is not LLM-friendly.** The `layout_subtree()` function is a standard tree-layout recursion, but LLMs struggle with recursive state tracking. For a tree with depth 5+ and variable branching factor, the AI will lose track of `available_width` subdivisions and produce overlapping subtrees. The `total_width=16.0` starting value is also arbitrary.

4. **Helper functions are undefined.** `find_hub()`, `find_parent()`, `normalize()`, `group_by_root()`, `find_root()`, `get_path()` — six helper functions are referenced but never defined. An LLM would need to invent implementations, introducing inconsistency.

**Fix needed:** (a) For HUB_FAN, provide a lookup table of pre-computed cos/sin values for common fan counts (3–12). (b) For DIAMOND_CONVERGENCE, generalize to N paths with a path-finding algorithm definition. (c) For TREE_BRANCHING, provide an iterative (non-recursive) version or a worked example with 3 levels. (d) Define all six helper functions inline.

### Phase 4 (Collision Detection): NOT DIRECTLY USABLE — 3/10

**The core problem:** This is an iterative relaxation algorithm — it runs up to 10 passes, adjusting coordinates each time. An LLM cannot execute iterative algorithms with mutable state. The model would need to:
1. Compute O(n^2) pairwise distances for all quests
2. Identify collisions
3. Apply push adjustments
4. Repeat up to 10 times

For a 50-quest chapter, that is 1,225 pair comparisons per iteration, up to 12,250 total. No LLM can perform this computation accurately in-context.

**What the AI will actually do:** Skip collision detection entirely, or perform one shallow pass and declare success. The result will be overlapping quests that the AI claims are collision-free.

**Fix needed:** This phase must be converted to a post-generation validation check (like R58), not an in-generation algorithm. The AI should assign coordinates in Phase 3, then check for collisions using R58's distance formula, and adjust manually only the specific pairs that collide. The iterative relaxation should be described as "what the validate-and-fix loop does" rather than "what the AI executes."

### Phase 5 (Shape, Size, Icon Assignment): USABLE — 8/10

**What works:** The shape decision tree is a priority-ordered if/elif chain that an LLM can follow directly. Each condition references values computed in Phase 1 (fan_in, fan_out, task_type, optional). The size formula is a simple lookup table. The icon rules are a clear needed/not-needed decision tree.

**Minor problem:** The condition `q.task_type == "kill"` requires knowing the task type before the task is designed. In the current SKILL.md flow, shape is assigned in Step 3 (scaffold) but task types are determined in Step 4 (content). This creates a forward dependency — the scaffold needs to know the task type to assign the correct shape.

**Fix needed:** Note that pentagon assignment for kill/combat quests should be deferred to Step 4, with a placeholder shape (chapter default) used in Step 3.

### Phase 6 (Final Output): USABLE — 9/10

**What works:** Quarter-grid snapping, viewport clamping, and density-based `hide_dependency_lines` are all simple arithmetic. The only issue is `count_quests_within_radius()` which requires O(n^2) computation, but for a single pass this is manageable for chapters under ~100 quests.

**Minor problem:** The viewport bounds `[-15.0, 35.0]` for x and `[-15.0, 15.0]` for y have an inconsistency — the x range allows 50 units while the y range allows only 30. The text says "FTB Evolution create reaches x=30.0" which is within bounds, but the asymmetric clamping is not explained.

---

## 2. Constraint Formulas — Computability Assessment

### Spacing Formula: DIRECTLY COMPUTABLE — 9/10

```
y_spacing = clamp(1.5 * density_factor, 1.0, 2.5)
density_factor = 1.0 if N <= 50, else 1.0 - (N - 50) * 0.005
```

This is a single arithmetic expression given quest count. The AI can compute it instantly. The examples (1.5 for 30 quests, 1.25 for 100, 1.0 for 150) are consistent and verifiable. No issues.

### Column Spacing: DIRECTLY COMPUTABLE — 9/10

```
column_x_gap = clamp(2.0 + column_quest_width * 0.5, 2.0, 4.0)
```

One variable (`column_quest_width`), one multiplication, one clamp. Trivial.

### Hub Radius: DIRECTLY COMPUTABLE — 9/10

```
hub_radius = clamp(3.0 + fan_out_count * 0.4, 3.5, 7.0)
leaf_distance = clamp(2.0 + leaf_count_per_branch * 0.5, 2.0, 4.0)
```

Direct computation from fan_out and leaf counts (available from Phase 1). No iteration needed.

### Size Formula: DIRECTLY COMPUTABLE — 8/10

The `role_multiplier` table is a clear lookup. The minor issue is that some roles ("convergence_3plus: 1.5–2.0", "milestone: 1.25–1.5") give ranges rather than fixed values, requiring the AI to pick a value within the range. This is fine for an LLM (it can choose based on context) but introduces variability — two runs might produce different sizes for the same quest.

**Fix needed:** Provide a default within each range (e.g., "convergence_3plus: 1.75 default, use 1.5 for small chapters, 2.0 for large chapters").

### Shape Priority Tree: DIRECTLY APPLICABLE — 8/10

The 8-level priority tree is clear and ordered. Same forward-dependency issue as Phase 5 (kill-task shape needs task type from Step 4).

**Verdict:** All constraint formulas are directly computable. This is the strongest part of the document — the formulas are parameterized by values that Phase 1 already provides, and they produce concrete numbers without iteration or optimization.

---

## 3. R55–R64 Rules — Programmability Assessment

### Fully Automatable (AI can check and report violations without human judgment):

| Rule | Automatability | Reason |
|------|---------------|--------|
| **R55** Topology-Progression Mode Alignment | **HIGH** | Pure lookup: classify topology, check mode against table. O(1). |
| **R57** Hub Node Size Dominance | **HIGH** | Compare hub.size vs max(child.size) for each hub. O(n). |
| **R58** Collision-Free Adjacent Nodes | **HIGH** | O(n^2) pairwise distance, but formula is clear. Manageable for n < 100. |
| **R59** Bounding Box Viewport Fit | **HIGH** | min/max over all coordinates. O(n). |
| **R62** Parallel Column Spacing Uniformity | **HIGH** | Group by root, compute column centers, check variance. O(n). |
| **R63** Grid Catalog Aspect Ratio | **HIGH** | width/height division. O(1) after min/max. |

### Partially Automatable (AI can check but needs judgment for edge cases):

| Rule | Automatability | Reason |
|------|---------------|--------|
| **R56** Depth-Axis Monotonicity | **MEDIUM-HIGH** | The 1.0-unit tolerance is clear, but "primary axis" determination (y for vertical, x for horizontal) requires knowing the layout direction — which depends on topology classification. If classification is wrong, the check gives false results. |
| **R60** Topology-Shape Vocabulary Coherence | **MEDIUM** | Counting distinct shapes is trivial. But the `required_roles` check ("hub" and "leaf" roles must have distinct shapes) requires the AI to determine which quests are hubs and which are leaves — this depends on the graph analysis, and the mapping between role names and graph properties is implicit. |
| **R61** Convergence Point Visual Prominence | **MEDIUM** | The 80% threshold is clear, but determining "horizontal vs vertical layout" from parent spread is fragile when parents are evenly distributed in both axes. |

### Requires Context (AI can check but result needs human interpretation):

| Rule | Automatability | Reason |
|------|---------------|--------|
| **R64** Decorative Image Topology Alignment | **LOW-MEDIUM** | Requires knowing decorative image bounding boxes, which are only available if the chapter already has images defined. In the generation flow, images are typically added AFTER quest layout, making this check impossible during initial generation. The 30% threshold is also arbitrary — is 29% orphaned quests acceptable but 31% not? |

**Overall rule assessment:** 6 of 10 rules are fully automatable. 3 are partially automatable with clear edge-case handling. 1 (R64) is difficult to apply during generation. This is a strong result — the rules are significantly more automatable than the layout algorithm itself.

---

## 4. Topology Classification — Can AI Choose Before Full Data Exists?

**The fundamental problem:** Topology classification (Phase 2) requires the complete dependency graph — all quests and all dependencies must be known. In the SKILL.md flow:

- **Step 2 (Interview):** The outline defines quest names and `depends_on` wiring. This IS the complete dependency graph.
- **Step 3 (Scaffold):** The skeleton assigns shapes and positions.

So topology classification CAN run at the Step 2→3 transition — after the outline is approved but before coordinates are assigned. The outline provides all quests and dependencies; classification computes the topology type; Phase 3 uses that type to assign coordinates.

**However, three practical issues arise:**

1. **The outline may be incomplete.** Step 2 says "only names + wiring; no tasks, no rewards, no descriptions." But the topology classification also uses `has_hub` (fan_out >= 5) and convergence_ratio — these depend on the full dependency structure. If the user adds more quests in Step 4 (which is allowed — the outline is a starting point, not a contract), the topology may change.

2. **Region decomposition is still unsolved.** The document says topology applies per-region, but regions are only identifiable after coordinate clustering. For large chapters (100+ quests), the AI must decide: classify the whole chapter, or decompose into regions first? No algorithm is given for region decomposition.

3. **The "default fallback" problem.** When the classification conditions don't match any topology clearly (the `else: return "linear_chain"` fallback), the AI will silently apply linear_chain layout to what might be a hub_fan or tree. This is the most dangerous failure mode — a misclassified topology produces a layout that looks wrong but doesn't trigger any validation error.

**Recommendation:** Add a Step 2.5 decision point where the AI presents the topology classification to the user for confirmation: "Based on the outline, this chapter's topology is hub_fan (1 root, 3 branches with 4–6 leaves each). Does this match your intent?" This converts classification from an automated guess to a user-confirmed choice.

---

## 5. SKILL.md Integration — Step 3/4/5 Usage Recommendations

### Current State

SKILL.md's Step 3 currently uses a simple layout model:
> "main path left-to-right (x +1.0/step, y flat), side branches offset (y +/-1.0), spacing ~1.0, size: 1.0"

This is topology-blind — it treats every chapter as a linear chain with branches. The new topology-coordinates module provides significantly more sophisticated layout but is not referenced anywhere in SKILL.md.

SKILL.md's Step 4 focuses on per-node content (tasks, rewards, descriptions) with three reasoning gates. Layout is not part of the per-node loop.

SKILL.md's Step 5 runs `validate_quests.py` which checks R1–R32 (from the modular files) but does not reference R55–R64.

### Recommended Integration

#### Step 2 (Interview) — Add topology discussion

After the outline is approved, before Step 3:
- Run Phase 1 (graph analysis) on the outline
- Run Phase 2 (topology classification) on each chapter
- Present the classification to the user: "Chapter X has topology type [type]. This means [brief description]. Confirm or override."
- Record the confirmed topology type in the outline: `{ name: "chapter_x", topology: "hub_fan", ... }`

This adds ~1 interaction turn per chapter but prevents misclassification.

#### Step 3 (Scaffold) — Replace simple layout with topology-aware layout

Current Step 3 layout instruction should be replaced with:

> "Assign coordinates using the topology-aware layout algorithm from `reference/design/topology-coordinates.md`:
> 1. Run Phase 1 (graph analysis) on the chapter's quests and dependencies
> 2. Use the confirmed topology type from Step 2 to select the Phase 3 coordinate strategy
> 3. Apply constraint formulas (spacing, hub radius, column gap) from Layer 2
> 4. Run Phase 5 (shape/size/icon assignment) using the decision tree
> 5. Run Phase 6 (snap to grid, viewport clamp, density check)
>
> Skip Phase 4 (collision detection) during scaffold — collision checking runs in Step 5 via R58."

The scaffold spec should include the computed `x`, `y`, `shape`, `size`, and optionally `icon` for each quest — replacing the current simple linear placement.

#### Step 4 (Content) — No major changes, but add shape override

Step 4's per-node loop should add one check:
- When the task type is determined (e.g., `kill`), check whether Phase 5's shape decision tree would assign a different shape than the scaffold's placeholder. If so, update the shape in the spec.
- When the reward type and size are finalized, check R57 (hub size dominance) for any hub quests whose children now have known sizes.

These are lightweight checks that don't disrupt the existing Step 4 flow.

#### Step 5 (Validation) — Add R55–R64 to the validation pipeline

Step 5 should run the following additional checks after the existing R1–R32 pipeline:

| Priority | Rule | When to run |
|----------|------|-------------|
| P0 | R58 Collision-Free | After all coordinates assigned |
| P1 | R55 Topology-Mode Alignment | After topology classification confirmed |
| P1 | R56 Depth-Axis Monotonicity | After coordinate assignment |
| P1 | R59 Bounding Box Viewport | After coordinate assignment |
| P1 | R61 Convergence Prominence | After coordinate assignment |
| P2 | R57 Hub Size Dominance | After size assignment |
| P2 | R62 Column Spacing Uniformity | If parallel_columns topology |
| P2 | R63 Grid Aspect Ratio | If grid_catalog topology |
| P2 | R64 Decorative Image Alignment | If chapter has decorative images |
| P3 | R60 Shape Vocabulary | After shape assignment |

The Step 5 summary should add a topology/layout section:
```
Layout: {topology_type} | Bounding box: {w}x{h} | Density: {quests/sq_unit}
Collision check: {pass/fail} ({n} overlaps) | Depth monotonicity: {pass/fail}
```

#### Step 5a (Load-test) — Add visual check

The load-test step should add: "Open the quest book and verify that the layout visually matches the intended topology — hub nodes are prominent, chains flow in the expected direction, and no quests overlap."

---

## 6. Specific Improvement Suggestions

### Critical (blocks practical use)

1. **Convert Phase 4 (collision detection) from an in-generation algorithm to a post-generation validation check.** The iterative relaxation cannot be executed by an LLM. R58 already provides the validation formula — Phase 4 should be deleted from the algorithm and replaced with a reference to R58.

2. **Define the six helper functions** (`find_hub`, `find_parent`, `normalize`, `group_by_root`, `find_root`, `get_path`). Each is 3–5 lines of pseudocode. Without definitions, the AI will invent inconsistent implementations.

3. **Add a pre-computed trigonometric lookup table** for HUB_FAN's radial placement. Provide cos/sin values for fan counts 3–12 at uniform angle steps. This eliminates the LLM's trigonometric hallucination risk.

4. **Resolve the region decomposition circular dependency.** Either: (a) define regions based on the dependency graph structure (connected components, or mod-id prefix grouping) BEFORE topology classification, or (b) drop the per-region classification claim and apply topology per-chapter only.

### Important (improves reliability)

5. **Add a confidence/fallback mechanism to topology classification.** When multiple classification conditions are close to thresholds (e.g., max_depth=5, which is near the 6-threshold for linear_chain), flag the classification as uncertain and recommend user confirmation.

6. **Fix the `has_grid` false positive** by adding a minimum quest count guard (`len(quests) >= 15`).

7. **Generalize DIAMOND_CONVERGENCE** to handle N paths (not just left/right). Provide a path-enumeration algorithm that works when 3+ branches diverge from root and converge at a single point.

8. **Provide default values within size ranges.** "convergence_3plus: 1.5–2.0" should become "convergence_3plus: 1.75 (default); 1.5 for chapters < 30 quests; 2.0 for chapters > 80 quests."

### Nice-to-have (polish)

9. **Add a worked example** that traces one complete chapter (e.g., a hypothetical 15-quest hub_fan chapter) through all 6 phases, showing the exact output at each step. This gives the AI a concrete template to follow.

10. **Provide an iterative (non-recursive) version of TREE_BRANCHING.** The current recursive `layout_subtree()` is correct algorithmically but difficult for an LLM to execute for trees deeper than 3 levels.

11. **Align the viewport bounds.** The x clamp `[-15.0, 35.0]` and y clamp `[-15.0, 15.0]` should be documented with their asymmetry explained (x allows more room because horizontal layouts are more common in the dataset).

---

## 7. Summary Verdict

### What works well

- **Constraint formulas (Layer 2)** are the document's strongest contribution. Every formula is directly computable from values available after graph analysis, uses simple arithmetic (no iteration/optimization), and provides bounded ranges rather than fixed values. An LLM can apply these reliably.

- **Real-case data (Layer 3)** is genuinely useful as calibration. The 13 cases span all 6 topology types with concrete coordinates, giving the AI a "what should the output look like" reference. The cross-pack comparison table is particularly valuable.

- **Rules R55–R64** are significantly more automatable than the layout algorithm itself. 6 of 10 are fully programmable, and the remaining 4 need only minor judgment calls. The rules correctly separate "generation-time checks" (R55, R57, R58) from "validation-time checks" (the rest).

- **The shape/size decision trees** (Phase 5, Layer 2) are clear, priority-ordered, and reference values that are already available from graph analysis. They integrate naturally into the existing Step 3 scaffold flow.

### What needs fixing before practical use

- **Phase 4 (collision detection) must be removed from the generation algorithm** and replaced with a reference to R58 validation. An LLM cannot execute iterative relaxation.

- **Topology classification needs a user confirmation step.** The classification is too important (it determines the entire layout strategy) to be an automated guess. Adding one interaction turn per chapter to confirm the topology type is a small cost for a large reliability gain.

- **Region decomposition must be defined or dropped.** The per-region classification claim is currently unsupported by any decomposition algorithm, creating a circular dependency with coordinate assignment.

- **Helper functions must be defined.** Six undefined functions in the pseudocode will cause the AI to invent inconsistent implementations across different generation sessions.

- **SKILL.md must be updated** to reference the new modules. Currently, Step 3 uses topology-blind linear layout, Step 4 has no layout awareness, and Step 5 doesn't check R55–R64. The integration recommendations in Section 5 above would bring the practical flow in line with the theoretical capability.

### Final assessment

The topology-coordinates and progression-rules documents represent a genuine advance in the skill's ability to produce well-laid-out quest configurations. The data quality is high, the formulas are sound, and the rules are well-designed for automation. However, the gap between "algorithm that a programmer could implement" and "algorithm that an LLM can execute in-context" is significant and must be closed before these documents deliver their theoretical value. The fixes are concrete and achievable — the most critical being the Phase 4 conversion, helper function definitions, and SKILL.md integration.

**Score: 6/10** — Strong theoretical foundation, needs practical adaptation for LLM execution. With the critical fixes applied, this would be an 8/10.
