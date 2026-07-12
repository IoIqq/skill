# Phase 4 Cycle 11 — Reviewer B: Completeness Audit

> **Reviewer:** B (Completeness)
> **Cycle:** 11 | **Date:** 2026-07-12
> **Scope:** topology-coordinates.md, micro-patterns.md (MP46-50), anti-patterns.md (AP23-27), progression-rules.md (R55-R64)
> **Methodology:** Systematic boundary testing, constraint formula coverage analysis, cross-rule conflict detection, pattern/anti-pattern gap enumeration, hybrid topology coverage verification.

---

## Completeness Score: 7 / 10

The Cycle 11 additions are well-researched and grounded in real data from 9 packs / 19 chapters. The core algorithms, formulas, and rules are internally coherent for the "normal" case (20-130 quests per chapter, single-topology or clearly compartmentalized multi-region). However, several edge cases fall outside the covered parameter space, one topology variant (Highway+Branch) exists as a micro-pattern but not in the classification algorithm, two rule pairs have partial semantic overlap that could produce contradictory diagnostics, and the pattern/anti-pattern sets each miss 2-3 common layout archetypes observed in the dataset itself.

---

## 1. Boundary Case Omissions

### 1.1 Extreme Large Chapters (>200 quests)

**Status: Partially covered**

ATM-10 create (206 quests) is in the dataset, but the spacing formula's density_factor bottoms out at min_spacing for any chapter above ~150 quests:

```
density_factor = 1.0 - (quest_count - 50) * 0.005
For quest_count = 150: density_factor = 0.5, y_spacing = clamp(0.75, 1.0, 2.5) = 1.0
For quest_count = 200: density_factor = 0.25, y_spacing = clamp(0.375, 1.0, 2.5) = 1.0
For quest_count = 300: density_factor = -0.25, y_spacing = clamp(-0.375, 1.0, 2.5) = 1.0
```

The formula produces meaningful gradation only between 50-150 quests. Below 50 it's constant at 1.5; above 150 it's constant at 1.0. **The formula is effectively a step function with a smooth transition band, not a continuous scaling.** For a hypothetical 300-quest chapter (plausible for large expert packs), the spacing would be identical to a 150-quest chapter, but the bounding box would be 2x larger.

**Missing:** No upper bound on quest count. No guidance on when a chapter should be split into sub-chapters based on quest count alone (R9 limits dependency depth, not quest count). No degradation strategy for chapters exceeding the viewport despite optimal spacing.

**Recommendation:** Add a `quest_count_soft_limit` and `quest_count_hard_limit` per topology type. For linear_chain, suggest splitting at >100 quests. For grid_catalog, suggest splitting at >200 quests. For tree_branching and hub_fan, suggest sub-region decomposition at >150 quests.

### 1.2 Extreme Small Chapters (<5 quests)

**Status: Not explicitly addressed**

The topology classification algorithm's conditions assume meaningful depth and width values:
- `max_depth >= 6` for linear_chain requires at least 7 quests in a chain
- `max_width >= 4` for hub_fan requires at least 5 quests
- `len(quests) >= 20` for grid_catalog explicitly excludes small chapters

For a 2-quest chapter (root + single dependent), the classification would fall through to the `else: return "linear_chain"` default. This is correct behavior but undocumented. A 3-quest chapter with one root and two leaves (fan_out=2) would also default to linear_chain, even though the topology is technically a minimal hub_fan.

**Missing:** No minimum quest count for topology classification to be meaningful. No "micro-chapter" guidance for chapters with <5 quests.

**Recommendation:** Add an explicit early-return for chapters with <5 quests: classify as linear_chain (or hub_fan if fan_out >= 2), skip most R55-R64 validation (R58 collision and R59 bounding box still apply), and note that visual hierarchy is trivially satisfied at this scale.

### 1.3 Single-Quest Chapters

**Status: Not addressed**

A chapter with exactly 1 quest has no dependencies, no topology, no spacing concerns, and no convergence. The classify_topology function would set max_depth=0, max_width=1, and fall through to linear_chain. R56-R64 would either skip or pass trivially. This is harmless but should be explicitly documented as a degenerate case.

### 1.4 Empty Chapters

**Status: Not addressed**

An empty chapter (0 quests) would crash the classify_topology function (max() of empty sequence). The algorithm should guard against this.

---

## 2. Constraint Formula Coverage

### 2.1 Viewport Bounds Asymmetry

**Observation:** The viewport clamp is x in [-15.0, 35.0] and y in [-15.0, 15.0]. This gives 50 units of horizontal space but only 30 units of vertical space. The asymmetry is justified by FTB Quests' wider-than-tall viewport, but the y upper bound of 15.0 is potentially too restrictive.

**Evidence:** Monifactory progression's HV-EV cluster reaches y=12.5, and the main staircase reaches y=10.5. With the y clamp at 15.0, there's only 2.5 units of headroom above the tallest observed chapter. If a future chapter needs 18 units of vertical space (plausible for a deep expert pack), the clamp would truncate it.

The R59 rule sets MAX_HEIGHT=30.0, which corresponds to y in [0, 30] or [-15, 15] — matching the clamp. But the R59 warning triggers at 30 units, while the clamp hard-limits at 30 units. **The warning and the clamp are the same value, meaning a chapter that triggers the R59 warning would simultaneously be hard-clamped, potentially overlapping quests at the boundary.**

**Recommendation:** Separate the R59 warning threshold (30 units) from the hard clamp (35 units for y, matching the x headroom pattern of 35 vs 30 for x). Or increase MAX_HEIGHT to 35 to match MAX_WIDTH.

### 2.2 Hub Radius Formula vs. Large Fan-Out

**Observation:** `hub_radius = clamp(3.0 + fan_out_count * 0.4, 3.5, 7.0)`. For fan_out=10 (a hub with 10 branches), radius = 3.0 + 4.0 = 7.0, hitting the upper bound. For fan_out=15, radius would be 9.0 but is clamped to 7.0. At radius 7.0 with 15 children, the angular spacing is 24 degrees, and adjacent children are separated by `2 * 7.0 * sin(12 degrees) = 2.9` units — acceptable. But grandchildren extending outward by 2.0 units from their parents would be at radius 9.0, potentially outside the viewport for a centered hub.

**Missing:** No formula adjustment for hubs with fan_out > 10. No guidance on when to split a high-fanout hub into sub-hubs.

### 2.3 Column Spacing Formula vs. Many Columns

**Observation:** `column_x_gap = clamp(2.0 + column_quest_width * 0.5, 2.0, 4.0)`. For 10 parallel columns at 2.0 spacing, total width = 20 units (within viewport). At 4.0 spacing, total width = 40 units (exceeds MAX_WIDTH=35). The formula caps at 4.0 but doesn't account for the number of columns.

**Missing:** A constraint linking column count, column spacing, and viewport width: `column_count * column_x_gap <= MAX_WIDTH - 2*PADDING`.

### 2.4 Collision Detection Iteration Limit

**Observation:** The collision resolution algorithm runs for max 10 iterations. For a dense 200-quest chapter, 10 iterations of pairwise push-apart may not converge. The algorithm doesn't check whether all collisions are resolved after the loop; it simply returns the current state.

**Missing:** A post-loop verification step that reports unresolved collisions. A fallback strategy (e.g., increase spacing globally, or switch to grid arrangement) when iterations don't converge.

---

## 3. Rule Conflicts (R55-R64 vs R1-R54)

### 3.1 R35 vs R60 — Shape Semantics Tension

**Severity: LOW (INFO-level overlap, not contradictory)**

R35 (Shape Semantics Consistency Within Pack) enforces pack-level shape uniformity: "shapes used as tier markers should be used consistently across chapters." R60 (Topology-Shape Vocabulary Coherence) enforces chapter-level topology-driven shape diversity: "hub_fan topologies benefit from at least 3 distinct shapes."

**Conflict scenario:** A pack uses hexagon as the dominant shape across all chapters (R35 compliance). A new hub_fan chapter needs at least 2-3 shapes per R60. If the author adds gear for the hub and rsquare for leaves (departing from the pack's hexagon-only norm), R35 would flag this as unusual shape usage while R60 would approve it.

**Resolution:** R60's topology-specific guidance should take precedence over R35's pack-level consistency within the chapter where the topology demands it. R35 should add an exception: "chapters whose topology type requires shape diversity per R60 are exempt from the dominant-shape check." This is not currently stated.

### 3.2 R30 vs R57 — Visual Hierarchy Overlap

**Severity: LOW (redundant, not contradictory)**

R30 (Quest Visual Hierarchy & Size Consistency) checks that milestones are larger than routine quests. R57 (Hub Node Size Dominance) checks that hubs are larger than their direct children. These use different definitions of "important node":
- R30: milestone = fan_out >= 3 OR is_capstone (fan_in >= 5 per R13's heuristic)
- R57: hub = fan_out >= 3; convergence = fan_in >= 3

A convergence node with fan_in=4 would trigger R57's convergence check (be at least as large as parents) but NOT R30's milestone check. Conversely, a capstone with fan_in=5 and fan_out=0 would trigger R30 but not R57.

**No direct contradiction** but the overlap creates confusion about which rule is authoritative for size hierarchy. R30 is P3/INFO while R57 is P2/WARNING, so R57 takes priority in execution but R30's milestone definition is broader.

**Recommendation:** R57 should reference R30 and explicitly state: "R57 covers hub-to-child and convergence-to-parent size relationships; R30 covers the broader milestone-vs-routine relationship. Both may apply to the same quest."

### 3.3 R41 vs R55 — Early-Game Progression Mode Tension

**Severity: MEDIUM (potentially contradictory guidance)**

R41 (Early-Game Flexible Progression Mode, INFO) recommends flexible progression mode for early-game chapters to give new players freedom. R55 (Topology-Progression Mode Alignment, WARNING) constrains which topology types are compatible with flexible mode:

```
"linear_chain": ["default", "linear"],       # flexible NOT allowed
"tree_branching": ["default", "linear"],      # flexible NOT allowed
```

**Conflict scenario:** An early-game tutorial chapter uses linear_chain topology (a step-by-step introduction to the pack's core mods). R41 recommends flexible mode for this early-game chapter. R55 warns that linear_chain + flexible is a bad combination because "flexible mode lets players skip ahead past the chain's intended sequence."

**Both rules are correct in isolation** but their intersection creates a dilemma: should early-game tutorials use linear topology (good for teaching) + default mode (good for gating), or linear topology + flexible mode (good for player freedom)?

**Recommendation:** R41 should add an exception: "early-game chapters that use linear_chain topology for tutorial purposes should use `default` progression mode despite the early-game flexible recommendation — tutorial sequencing is more important than player freedom in the first 1-2 chapters." Alternatively, R55 should allow linear_chain + flexible with a softer warning when the chapter is marked as a tutorial.

### 3.4 R13 vs R61 — Convergence Threshold Mismatch

**Severity: LOW (different thresholds, not contradictory)**

R13 (Capstone Reward Magnitude) uses fan_in >= 5 as the capstone heuristic. R61 (Convergence Point Visual Prominence) uses fan_in >= 2 as the convergence threshold. A quest with fan_in=3 is a convergence point for R61 (visual prominence check) but NOT a capstone for R13 (reward magnitude check).

This means a moderate convergence node (fan_in=3) would be checked for visual placement but not for reward adequacy. This is arguably correct — not every convergence is a capstone — but the threshold gap creates a gray zone where fan_in 2-4 convergence nodes receive layout scrutiny without reward scrutiny.

**Recommendation:** Document the threshold gap explicitly. Consider adding a "minor convergence" category for fan_in 2-4 that triggers a softer R13 check (e.g., "reward should be at least 1.5x chapter average" instead of 3x).

---

## 4. Missing Anti-Patterns (AP23-27 Gaps)

### 4.1 AP-MISSING-1: Size Inflation (the "everything is huge" chapter)

**Symptom:** All or most quests in a chapter use size 2.0+, making it impossible to distinguish important quests from routine ones. The size hierarchy that players rely on for visual scanning is flattened at the top.

**Evidence:** Craftoria Create sets `default_quest_size: 2.0d` at chapter level, making ALL 123 quests large. This is mitigated by `default_quest_shape: "none"` (rendering as dots), but without the "none" shape mitigation, size inflation would be a severe anti-pattern.

**Why it's not covered:** AP26 covers node collision (spatial overlap) but not size inflation (hierarchy collapse). R57 checks hub-vs-child size but only for hubs with fan_out >= 3. A chapter where ALL quests are size 2.0 with no hubs would pass R57 but still have the size inflation problem.

**Recommendation:** Add AP28 — Size Hierarchy Collapse: triggered when >70% of quests in a chapter share the same size value AND that value is >= 1.5.

### 4.2 AP-MISSING-2: Orphan Region (decorative image with no quests)

**Symptom:** A decorative image defines a visual compartment, but no quests are placed inside it. The player sees an empty "drawer" or "panel" that looks like a bug — did the author forget to fill it? Is there content that's not loading?

**Evidence:** R64 checks the reverse (quests outside compartments) but not the complementary case (compartments without quests). Both are misalignment symptoms.

**Recommendation:** Extend R64 or add AP28 to also check: for each decorative image region, count quests inside; if zero, flag as "empty compartment — verify intentional."

### 4.3 AP-MISSING-3: Extreme Aspect Ratio Chapter

**Symptom:** A chapter's bounding box is extremely elongated — e.g., 2 units wide but 25 units tall (12.5:1 ratio), or 30 units wide but 2 units tall (15:1 ratio). The player must scroll extensively in one direction while the other axis is barely used.

**Evidence:** R63 covers grid_catalog aspect ratio (1:1 to 3:1) but only for grid topology. A linear_chain chapter with 20 quests in a single vertical column at x=0, y_spacing=1.5 would span 0 x 30 units — a 0:30 aspect ratio. R59 would catch the 30-unit height but not the extreme narrowness.

**Recommendation:** Add a general aspect ratio check to R59 or as a new rule: chapter bounding box aspect ratio should be between 1:5 and 5:1 (i.e., neither dimension should be more than 5x the other).

---

## 5. Missing Micro-Patterns (MP46-50 Gaps)

### 5.1 MP-MISSING-1: Diagonal Staircase Progression

**Description:** A linear chain laid out along a diagonal axis (e.g., dx=1.5, dy=1.5 per step), creating a staircase from lower-left to upper-right. Distinct from pure vertical (linear_chain) and pure horizontal (highway) layouts.

**Evidence:** Monifactory progression uses this as its signature layout (Case 6 in topology-coordinates.md: dx=1.5, dy=1.5 per tier). GT-Odyssey lv uses a wider diagonal step (dx=1.5-3.5, dy=3.0). Both are classified as "linear_chain" in the topology system, but the diagonal variant has distinct layout properties: it uses both axes simultaneously, requires different collision detection considerations, and produces a distinctive visual signature.

**Why it matters:** The diagonal staircase is the signature layout of expert packs. It deserves its own micro-pattern with coordinate template, spacing guidance, and sub-chain branching rules.

**Recommendation:** Add MP51 — Diagonal Staircase: a linear_chain variant where the primary axis is diagonal rather than purely vertical or horizontal. Include the step-size formula, sub-chain attachment points, and the relationship between diagonal angle and quest density.

### 5.2 MP-MISSING-2: Kill-Bounty Ladder

**Description:** Parallel columns where each column represents the same mob type at escalating kill counts (kill 5, kill 10, kill 50, kill 100), with boss-tier capstones at the bottom.

**Evidence:** ATM-10 bounty_board (Case 2 in topology-coordinates.md). This is classified as parallel_columns but has specific properties: all columns share identical y-values, identical shape/size progression, and a shared root quest. The "ladder" metaphor (ascending kill counts = descending y) is a reusable pattern.

**Recommendation:** Add MP52 — Kill-Bounty Ladder: a specialized parallel_columns pattern for bounty/combat chapters. Include the shared-root, identical-y, escalating-count template.

### 5.3 MP-MISSING-3: Symmetric Boss Tree

**Description:** A tree layout with perfect left-right symmetry, where the root is at center-top and paired side-branches extend equally on both sides at each depth level. Used for boss progression chapters where the player fights equivalent bosses on parallel paths.

**Evidence:** Finality Genesis cataclysm (Case 8 in topology-coordinates.md): every y-level has exactly 2 side branches at +-1.5 x, creating a mirror-symmetric tree. This is classified as tree_branching but the symmetry constraint is a specific design choice not captured by the general tree algorithm.

**Recommendation:** Add MP53 — Symmetric Boss Tree: a tree_branching variant with enforced bilateral symmetry. Include the coordinate template and the constraint that each depth level must have an even number of nodes.

---

## 6. Topology Algorithm — Hybrid/Mixed Coverage

### 6.1 Highway+Branch Not in Classification System

**Status: GAP**

MP46 (Highway+Branch) is documented as a micro-pattern but is NOT one of the six topology types in classify_topology(). MM2 botania (Case 10, 52 quests, 27.5 unit span) would be classified as... what? Let's trace the algorithm:

```
max_depth = moderate (spine depth ~14, branch depth ~2)
max_width = 14 (the spine at y=0 has 14 quests)
convergence_ratio = low (few merge points)
has_hub = yes (gear hubs at several spine nodes)
has_grid = no (dependencies exist)

→ has_hub and max_width >= 4 → "hub_fan"???
```

This is wrong. MM2 botania is a horizontal spine with vertical branches — it's not a hub-fan. The algorithm would misclassify it because the spine's length creates a large max_width, and the gear hubs trigger has_hub.

**Impact:** R55-R64 rules that are topology-specific would apply the wrong rule set. R62 (Parallel Column Spacing Uniformity) would not trigger because the classification isn't parallel_columns. R57 (Hub Node Size Dominance) would trigger for spine nodes that aren't really hubs in the traditional sense.

**Recommendation:** Either (a) add "highway_branch" as a 7th topology type in classify_topology(), or (b) add a pre-classification step that detects horizontal spines (max_width >> max_depth, most quests at y=0) and routes to a highway-specific handler.

### 6.2 Sub-Region Detection Not Implemented

**Status: GAP**

The document states: "The six topology types are not mutually exclusive — a 200-quest chapter can contain multiple sub-regions, each with its own topology. The classification above applies per-region, not just per-chapter." However, no algorithm is provided for detecting sub-regions or splitting a chapter into regions before classification.

The Phase 3 coordinate assignment algorithm takes a single topology type as input. If a chapter has 3 sub-regions (each with different topologies), the algorithm would need to:
1. Detect the sub-regions (clustering algorithm on quest coordinates)
2. Classify each sub-region independently
3. Apply per-region coordinate assignment

None of these steps are implemented.

**Recommendation:** Add a Phase 1.5 — Sub-Region Detection algorithm that uses coordinate clustering (e.g., DBSCAN or simple distance-based grouping with a 4-unit gap threshold) to identify sub-regions before topology classification.

### 6.3 Spiral/Vortex (MP49) Classification

**Status: Partially covered**

MP49 describes spiral/vortex as a "hub_fan variant" but the classify_topology() function has no way to distinguish a spiral from a standard hub_fan. Both have has_hub=true and similar max_width. The only difference is the angular arrangement of children, which the classification algorithm doesn't analyze.

Since MP49 is described as speculative (not directly observed as a primary topology in the dataset), this is acceptable for now. But if a future pack uses a spiral layout, the algorithm would classify it as hub_fan and apply radial coordinate assignment, which would destroy the spiral pattern.

**Recommendation:** Document that MP49 layouts should be explicitly flagged by the author (e.g., via a chapter-level metadata field) since the automatic classifier cannot detect them.

---

## 7. Minor Gaps and Observations

### 7.1 hide_dependency_lines Density Threshold

The threshold of 8 quests within 3-unit radius is derived from ATM-10 allthemodium and GT-Odyssey stoneage. But the threshold is a single fixed value. For chapters with very small quests (size 0.75 or "none" shape with effective radius 0.35), 8 quests in a 3-unit radius may not be visually cluttered. For chapters with large quests (size 2.0+), 4 quests in a 3-unit radius might already be spaghetti.

**Recommendation:** Scale the density threshold by average quest size: `density_threshold = 8 * (1.0 / avg_quest_size)`.

### 7.2 Quarter-Grid Snapping Precision

The finalize_layout phase snaps to quarter-grid (0.25 precision). But the collision detection algorithm uses floating-point distances, which after snapping might create new collisions (two quests at distance 1.01 might snap to positions at distance 0.99).

**Recommendation:** Run a post-snap collision verification and adjust any new collisions by moving one quest to the next quarter-grid position.

### 7.3 Decorative Image Coordinate System

R64 checks quests against decorative image bounding boxes using `img.x, img.y, img.width, img.height`. But the document doesn't specify whether decorative image coordinates use the same coordinate system as quest coordinates. In FTB Quests, image coordinates and quest coordinates may use different origins or scales. This needs verification.

### 7.4 Cross-Reference: AP23 and MP47

AP23 (Topology Mixing) prescribes MP47 (Compartment Region Layout) as the fix. But MP47 requires 100+ quests to be applicable. For chapters with 50-99 quests that mix topologies, AP23's fix #1 (use MP47) is not available. AP23 fix #3 says "pick ONE topology type" for chapters <50 quests, leaving the 50-99 range without clear guidance.

**Recommendation:** Add a mid-range option: for 50-99 quest chapters with mixed topologies, use spacing gaps (4-8 units) and shape changes to signal transitions, even without decorative images.

---

## 8. Summary of Findings

### Omissions by Severity

| Severity | Count | Items |
|----------|-------|-------|
| **HIGH** | 2 | Highway+Branch not in classification system (#6.1); Sub-region detection not implemented (#6.2) |
| **MEDIUM** | 4 | R41 vs R55 early-game tension (#3.3); Spacing formula dead zone for >150 quests (#1.1); Viewport warning = clamp threshold (#2.1); Column count vs viewport width unconstrained (#2.3) |
| **LOW** | 8 | R35 vs R60 shape tension (#3.1); R30 vs R57 overlap (#3.2); R13 vs R61 threshold gap (#3.4); Small chapter edge cases (#1.2, #1.3, #1.4); Missing anti-patterns (#4.1-4.3); Missing micro-patterns (#5.1-5.3) |

### Improvement Recommendations (Priority Order)

1. **Add "highway_branch" as 7th topology type** or add a pre-classification spine detector. This is the most significant gap — a documented topology variant (MP46, Case 10) cannot be correctly classified.

2. **Implement sub-region detection** (Phase 1.5) using coordinate clustering. The document acknowledges multi-topology chapters but provides no algorithm for handling them.

3. **Resolve R41 vs R55 tension** by adding a tutorial exception to R41 or a tutorial softening to R55's linear_chain + flexible restriction.

4. **Extend spacing formula** to produce meaningful values for >150 quest chapters, or add explicit quest-count-based chapter splitting guidance.

5. **Separate R59 warning threshold from hard clamp** — warning at 30 units, clamp at 35 units for both axes.

6. **Add 3 missing anti-patterns:** Size Hierarchy Collapse, Orphan Region, Extreme Aspect Ratio.

7. **Add 3 missing micro-patterns:** Diagonal Staircase, Kill-Bounty Ladder, Symmetric Boss Tree.

8. **Add column-count constraint** linking column count, spacing, and viewport width in the parallel_columns formula.

9. **Add post-snap collision verification** to catch collisions introduced by quarter-grid rounding.

10. **Scale hide_dependency_lines density threshold** by average quest size.

---

## 9. Conclusion

The Cycle 11 topology system is a significant achievement — it brings rigorous, data-driven layout guidance to a domain (quest book spatial design) that was previously governed entirely by author intuition. The six topology types, coordinate algorithms, and constraint formulas cover the majority of observed layouts well.

However, the system has two structural gaps that limit its completeness:

1. **The classification algorithm is single-output** (one topology per chapter) while the documentation acknowledges multi-topology chapters. Without sub-region detection, the system cannot handle its own stated use case for large chapters.

2. **The Highway+Branch topology** (MP46, MM2 botania) exists as a documented pattern but not as a classification category, meaning the system would misclassify real-world examples of this topology.

The R55-R64 rule set is internally consistent and well-integrated with R1-R54, with only one medium-severity tension (R41 vs R55 on early-game progression mode) and several low-severity overlaps that are redundant rather than contradictory.

**Final verdict:** The Cycle 11 additions are production-ready for the common case (single-topology chapters with 10-150 quests) but need the structural gaps addressed before they can handle the full diversity of real-world quest book layouts. The 7/10 score reflects strong coverage of the core use cases with identifiable gaps at the edges.
