# FTB Quests — Micro-Patterns [ACTIVE]

> **Status:** Active | **Cycle:** 19 | **Updated:** 2026-07-19 (Phase 2 Cycle 19 — MP76/MP77 validation upgrades from cross-platform search)
> **Predecessor:** `micro-patterns.archive.md` (MP1–MP45, archived after modular redistribution)
> **Scope:** Patterns discovered in Cycle 11 onwards. MP1–MP45 remain in the archive; most have been redistributed to the modular reference files (see `module-index.md`). New patterns here supplement the modular system.

This file continues the micro-pattern numbering from MP45 (the last pattern in the archived version). Each new pattern includes: name, applicable conditions, implementation guidance, and data sources.

---

## Part 10: Cycle 11 Patterns — Topology Coordinates (MP46–MP48)

These patterns describe coordinate-level layout decisions that were previously undocumented. They complement `topology-coordinates.md` (which provides the full algorithm and real case data) by capturing the discrete, reusable decisions that pack authors make when placing quests on the canvas.

### MP46 — Highway+Branch Topology

**Name:** Highway Spine with Vertical Branches
**Applicable conditions:** Chapter covers a mod with multiple independent subsystems (e.g., multiblock structures, processing chains), each requiring its own vertical progression chain. Typically tech-focused or multiblock-focused packs.
**Implementation:**
- Lay out the main progression as a horizontal chain at y=0, with consistent x-spacing (2.0 units per quest).
- At each major progression point, branch vertically: upper branches (positive y) for advanced variants, lower branches (negative y) for prerequisites or side content.
- Separate sub-chains can exist at extreme y-values (±6 to ±8) for collection/catalog content that runs parallel to the main progression.
- Shape vocabulary: gear for spine hubs, hexagon for branch nodes. Size: 2.0 for spine hubs, 1.5 for branch sub-hubs.
**Coordinate template:**
```
Spine: (0,0) → (2,0) → (4,0) → ... → (N*2, 0)
Upper branches: (spine_x, 1.5) → (spine_x+1, 1.5) for each sub-system
Lower branches: (spine_x, -1.5) → (spine_x+1, -1.5)
Separate sub-chains: (x, ±6.5) for collection catalogs
```
**Sources:** Multiblock Madness 2 botania chapter (52 quests, 27.5 unit span, 3 horizontal layers). This topology has only been observed in one pack so far; it may be specific to multiblock-centric designs where each branch represents a different multiblock structure's recipe chain. Cycle 12 data expanded this to 4 chapters (Create-New-Horizon mv, Gregtech-Voyager chapter_3_hv, ReFactory progress, Ragnamod_VII mekanism), confirming highway_branch is common in GT and expert packs with voltage-tier progression. FTBTeam/FTB-Mods-Issues #2059 requests "simultaneous 2D scrolling" specifically because horizontal layouts are hard to navigate with mouse-only scrolling — FTB dev MichaelHillcox acknowledged this is "a fair point" for trackpad users. Authors should be aware that highway_branch chapters may need extra navigational aids (waypoint icons, section headers) to compensate for the scrolling limitation.
**Cross-reference:** topology-coordinates.md Case 10, MP9 (Parallel Columns) for the vertical branch segments; MP50 (Decorative Waypoint) for navigation aids in wide layouts.

---

### MP47 — Compartment Region Layout

**Name:** Decorative-Image Compartmentalization
**Applicable conditions:** Large chapters (100+ quests) that need to organize content into visually distinct sub-regions. The pack uses decorative images (colored shape backgrounds, toolbox slot textures, or titled banner images) to delineate regions within a single chapter. Most common in Create-focused or mod-dense kitchen-sink chapters.
**Implementation:**
- Divide the chapter into 4-8 regions, each corresponding to a mod subsystem or recipe tier.
- Use decorative images with `order: 1-2` (background) as colored region markers. Each region gets a distinct color.
- Place region entry quests at the region's center with a larger size (1.5-2.0) and an icon.
- Internal topology within each region can vary (linear chain, hub+fan, or grid).
- Region spacing: 4-8 units of empty space between region boundaries.
- Each region's decorative image uses matching `color` values for the shape overlay and the toolbox slot texture.
**Coordinate template:**
```
Region A: center at (-10, -10), spans ±5 units
Region B: center at (0, -12), spans ±5 units
Region C: center at (-12, 0), spans ±5 units
Region D: center at (12, 0), spans ±5 units
... arranged radially around the chapter center
Decorative images: 9.25×9.25 unit colored squares behind each region
```
**Sources:** Craftoria Create (180 quests, 8 colored toolbox compartments with hover labels like "Mechanical Basics", "Brass", "Trains"), ATM-10 create (206 quests, 5+ coordinate-clustered regions), FTB Evolution create (123 quests, 3-zone compartment). The Craftoria implementation is the most elaborate, using `ftbquests:textures/gui/toolbox_interior.png` as region backgrounds with matching `ftbquests:textures/shapes/square/shape.png` color overlays.
**Cross-reference:** topology-coordinates.md Case 11 (ATM-10 create) and Case 13 (FTB Evolution create).

---

### MP48 — Shape Monoculture Chapter

**Name:** Single-Shape Chapter with Coordinate-Only Structure
**Applicable conditions:** Boss chapters, milestone chapters, or chapters where all quests serve the same role (e.g., all boss fights, all collection milestones). Using a single shape for all quests eliminates visual noise and lets coordinate placement carry the structural information.
**Implementation:**
- Set `default_quest_shape` at chapter level to the single shape.
- Do NOT set individual quest `shape` fields — let them all inherit the chapter default.
- Rely on size variation (2.0 for bosses/milestones, 1.0 for standard) and coordinate placement to convey hierarchy.
- Boss chapters: "square" shape (Finality Genesis cataclysm), all 28 quests in a symmetric tree.
- Milestone chapters: "none" shape (RAD3 milestones), all 63 quests in a grid.
- Expert progression: "hexagon" shape (Monifactory progression, 78/127 = 61% hexagon), most quests identical.
**Shape selection guide:**
- Boss/combat chapters → "square" or "pentagon"
- Collection/catalog chapters → "none"
- Expert tech chapters → "hexagon"
- Magic chapters → "rsquare" or "diamond"
**Sources:** Finality Genesis cataclysm (28 quests, ALL square), RAD3 milestones (63 quests, ALL none), Monifactory groundwork (97 quests, 66/97 = 68% hexagon), GregTech-Odyssey lv (129 quests, ~60% hexagon). This pattern is the most common in the dataset — approximately 40% of sampled chapters use shape monoculture (>80% same shape). Cycle 12 adds Gregtech-Voyager (292 quests, zero shape overrides across 4 chapters) as the strongest monoculture example. FTB dev desht confirmed the hierarchical shape system in FTBTeam/FTB-Mods-Issues #1303: "It's a hierarchical system — file defaults, which are overridden by chapter defaults, which are overridden by quest settings." FTB team member MichaelHillcox proposed a "Quests Legend" feature (#1447) to display shape meanings visually, suggesting that shape monoculture benefits from explicit documentation of what the single shape represents in context.
**Cross-reference:** topology-coordinates.md Layer 2 Shape Decision Tree, MP19 (Stage Marking) for how chapters signal their role.

---

## Scope Annotation — Cycle 11 Patterns (Phase 1)

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP46 Highway+Branch | ✔ (chapter topology choice) | — | ✔ (check branch alignment) |
| MP47 Compartment Region | ✔ (region planning) | ✔ (per-region node placement) | ✔ (check region boundaries) |
| MP48 Shape Monoculture | ✔ (chapter shape choice) | — | ✔ (check shape consistency) |

---

## Part 11: Cycle 11 Patterns — Phase 2 Validation Additions (MP49–MP50)

These patterns were identified during Phase 2 cross-validation, emerging from Chinese community tutorials and comparative analysis of topology-coordinates.md real case data. They supplement the Phase 1 topology framework with layout techniques that the original six-type classification did not explicitly capture.

### MP49 — Spiral/Vortex Layout (Advanced Hub-Fan Variant)

> **Theoretical — not observed in the 13-case Phase 1 dataset.** This pattern is derived from a single Chinese community tutorial (mcmod.cn post/2494) and has not been confirmed in any shipping modpack config. Coordinate templates below are speculative. If a future pack uses a spiral layout, the automatic classifier will categorize it as hub_fan; authors should explicitly flag spiral intent via chapter-level metadata.

**Name:** Spiral or Vortex Quest Arrangement
**Applicable conditions:** A chapter with a central hub quest where the progression radiates outward in a spiral or vortex pattern rather than straight radial lines. Suitable for chapters where the author wants to convey a sense of expanding exploration or deepening complexity as the player moves from center to edge. The mcmod.cn tutorial (post/2494) describes this as an advanced aesthetic technique: "伪曲线的旋转" (pseudo-curve rotation) for creating visually striking layouts.
**Implementation:**
- Place the hub quest at origin (0, 0) with a distinctive shape (gear) and large size (2.0+).
- Arrange the first ring of quests at a small radius (2.0-3.0) in a clockwise or counterclockwise arc.
- Each subsequent ring increases the radius by 1.5-2.0 units and adds an angular offset, creating a spiral arm effect.
- The angular offset per ring should be approximately 30-45 degrees to produce a visible spiral rather than concentric circles.
- Use `hide_dependency_lines: true` on the hub quest and inner-ring quests to prevent radial line clutter; instead, use decorative curved-line images if visual connections are needed.
- Shape vocabulary: gear (hub), then chapter default for all spiral arms. Size decreases from center outward (2.0 → 1.5 → 1.0).
**Coordinate template:**
```
Hub: (0, 0)
Ring 1 (r=2.5, 4 quests):
  (2.5, 0), (0, 2.5), (-2.5, 0), (0, -2.5)
Ring 2 (r=4.5, offset 22.5°, 6 quests):
  (4.15, 1.72), (1.72, 4.15), (-1.72, 4.15), (-4.15, 1.72), (-4.15, -1.72), (-1.72, -4.15)
Ring 3 (r=6.5, offset 45°, 8 quests):
  ...continuing the spiral arm pattern
```
**Sources:** mcmod.cn post/2494 describes spiral/vortex as an advanced layout technique. Not directly observed as a primary topology in the 19-chapter Phase 1 dataset, but elements of spiral arrangement appear in ATM-10 basic_power (the three sub-hubs at (-5.5,0), (5.5,0), and (-1.5,2) form a partial arc around the center hub). This pattern is classified as a hub_fan variant in the topology-coordinates.md classification system.
**Cross-reference:** topology-coordinates.md Phase 2 (hub_fan classification); MP46 (Highway+Branch) as the other topology variant discovered in Cycle 11; AP27 (Dependency Line Spaghetti) — spiral layouts need aggressive line hiding.

---

### MP50 — Decorative Image Waypoint

**Name:** Non-Background Decorative Images for Navigation
**Applicable conditions:** Large chapters (50+ quests) where players need visual landmarks to orient themselves while scrolling. Distinct from MP47 (Compartment Region Layout) which uses decorative images as region *backgrounds*; MP50 uses decorative images as point-of-interest *markers* — banners, title cards, or mod logo images placed at key navigation points to help the player find their bearings.
**Implementation:**
- Place decorative images at chapter entry points, major convergence nodes, and section boundaries.
- Image types: mod logo images (for mod-specific sections), title text images (for chapter sub-headings like "Early Game" or "Tier 3"), or thematic banner images.
- Set `order: 0-1` (foreground or background) depending on whether the image should appear above or below quest nodes.
- Image size: 2.0-4.0 units wide for section titles, 1.0-2.0 for waypoint markers.
- Position images slightly offset from the quest they annotate (0.5-1.0 units above or to the left) to avoid collision with quest icons.
- Use `images: []` array at chapter level to define all waypoint images.
**Coordinate template:**
```
Chapter entry banner: image at (0, -2.0), width 6.0, "Getting Started" title
Mod section marker: image at (region_center_x, region_top_y - 1.0), mod logo 2.0×2.0
Convergence label: image at (convergence_x, convergence_y + 2.0), "Final Challenge" text
```
**Sources:** FTB Evolution create (27 icons across 123 quests — highest icon density at 22%, functioning as visual waypoints). ATM-10 create root quest at size 3.0 acts as a waypoint even without a decorative image. The mcmod.cn tutorial (post/5137) documents the theme system and decorative image customization that enables this pattern. mcmod.cn post/1416 recommends using custom images to enhance visual guidance. Cycle 12 adds CodeNameCIM2 prologue (67% icon rate, gear shapes for component milestones) as the highest icon rate observed, and Chinese pack authors from FTBTeam/FTB-Mods-Issues #962 (luoxiawuchen, ShiYan2022) demonstrated a preference for compact, visually-guided quest experiences — requesting task-level page breaks and visual condition markers to "使任务线更简洁" (make the mission line more concise).
**Cross-reference:** MP47 (Compartment Region Layout) for the background-image variant; topology-coordinates.md Phase 5 icon rules; AP23 (Topology Mixing) — waypoints help signal topology transitions.

---

## Part 12: Cycle 11 Patterns — Dataset-Derived Layout Archetypes (MP51–MP53)

These patterns were identified during the Phase 4 completeness review (Reviewer B) as recurring layout archetypes that already exist in the 13-case dataset but had not been formalized as named micro-patterns. Each is derived from at least one Case in topology-coordinates.md and represents a specific, reusable spatial arrangement that the topology classification system subsumes under a broader category.

### MP51 — Diagonal Staircase Progression

**Name:** Diagonal Staircase (linear_chain variant)
**Applicable conditions:** A linear chain laid out along a diagonal axis (both x and y increase per step), creating a staircase from lower-left to upper-right (or the reverse). Distinct from pure vertical (linear_chain) and pure horizontal (highway_branch) layouts. Most common in expert packs where each tier step represents a technology level-up and the diagonal direction visually conveys "ascending progress."
**Implementation:**
- Choose a step size (dx, dy) per tier. Monifactory progression uses (1.5, 1.5) per tier; GT-Odyssey lv uses wider steps (1.5–3.5, 3.0) reflecting broader visual sweeps.
- The primary axis is diagonal, not purely vertical or horizontal. Collision detection must account for both axes simultaneously — diagonal neighbors are naturally closer than cardinal neighbors.
- Sub-chains branch off the staircase at each tier level, forming vertical columns perpendicular to the diagonal. Each column represents the content available at that tier.
- Shape vocabulary: typically hexagon (expert packs) with square or octagon for milestone tiers on the main staircase.
- The diagonal angle determines quest density: steeper angles (dy > dx) pack more tiers vertically; shallower angles (dx > dy) spread tiers horizontally. A 45° angle (dx = dy) balances both axes.
**Coordinate template:**
```
Main staircase (dx=1.5, dy=1.5 per step):
  Q0: (-9.5, -5.5)  →  Q1: (-8.0, -4.0)  →  Q2: (-6.5, -2.5)  → ...
  Q_n: (start_x + n*1.5, start_y + n*1.5)

Sub-chain at tier k (vertical column from staircase node):
  (staircase_x + offset_x, staircase_y - 1.5), (staircase_x + offset_x, staircase_y - 3.0), ...
```
**Sources:** Monifactory progression (Case 6, 127 quests, dx=1.5, dy=1.5 — the signature expert-pack staircase); GT-Odyssey lv (Case 9, 129 quests, dx=1.5–3.5, dy=3.0 — wider diagonal steps). Both are classified as "linear_chain" in the topology system, but the diagonal variant has distinct layout properties requiring dual-axis collision awareness.
**Cross-reference:** topology-coordinates.md Cases 6 and 9; MP46 (Highway+Branch) as the other topology variant with a non-standard primary axis.

> **Generality note:** Observed only in expert packs (Monifactory, GT-Odyssey). The diagonal staircase is a sophisticated layout technique that expert pack authors use to make tier progression physically visible. Applicable to any pack type with tiered progression, but non-expert validation is needed before applying to kitchen-sink or adventure packs. Skyblock packs use compact layouts where a diagonal staircase would waste viewport space. Create-focused packs could theoretically use it but no examples exist in the dataset. Confidence: MEDIUM for non-expert pack types.

---

### MP52 — Kill-Bounty Ladder

**Name:** Kill-Bounty Ladder (parallel_columns specialization)
**Applicable conditions:** A bounty or combat chapter where parallel columns each represent the same mob type at escalating kill counts. All columns share identical y-values, identical shape/size progression, and a shared root quest. The "ladder" metaphor (ascending kill counts = descending y-values) creates a clear visual progression that players can scan horizontally to compare tiers.
**Implementation:**
- One column per mob type (zombie, skeleton, creeper, spider, etc.), each a vertical chain.
- All columns start at the same y-value and use identical y-spacing (typically 1.5 units per tier).
- Kill counts escalate identically across columns: 5 → 10 → 50 → 100 (or similar progression).
- Boss-tier capstones at the bottom of each column use pentagon shape + size 1.5.
- A single shared root quest (advancement "kill a mob") sits above all columns at y=0 with size 2.0.
- Column x-spacing: 2.0 units (tight but workable because columns have no horizontal branches).
- `hide_until_deps_visible: true` on higher tiers to gate progression visibility.
**Coordinate template:**
```
Root: (0, 0), size 2.0
Column 1: (-7.0, -2.5), (-7.0, -4.0), (-7.0, -5.5), (-7.0, -7.0)
Column 2: (-5.0, -2.5), (-5.0, -4.0), (-5.0, -5.5), (-5.0, -7.0)
Column 3: (-3.0, -2.5), (-3.0, -4.0), (-3.0, -5.5), (-3.0, -7.0)
... (additional columns at x + 2.0 increments)
Boss tier: pentagon + size 1.5 at the bottom row
```
**Sources:** ATM-10 bounty_board (Case 2, 12+ quests across 3+ columns, identical y-progression, the cleanest parallel_columns example in the dataset). The kill-bounty ladder is the most common use case for parallel_columns topology in kitchen-sink packs.
**Cross-reference:** topology-coordinates.md Case 2; R62 (Parallel Column Spacing Uniformity) for validation rules; MP48 (Shape Monoculture) — boss tiers often use pentagon monoculture within the ladder.

---

### MP53 — Symmetric Boss Tree

**Name:** Symmetric Boss Tree (tree_branching variant)
**Applicable conditions:** A tree layout with perfect left-right bilateral symmetry, where the root is at center and paired side-branches extend equally on both sides at each depth level. Used for boss progression chapters where the player fights equivalent bosses on parallel paths, or preparation chains that need identical branches for different boss types.
**Implementation:**
- Root quest at center-top (or center) with the tree expanding downward (or upward).
- At each depth level, side branches appear in symmetric pairs: one at x_center - offset, one at x_center + offset.
- The offset is consistent across all levels (typically ±1.5 units) to maintain visual symmetry.
- Each depth level must have an even number of non-center nodes (or an odd number with one centered node flanked by pairs).
- The final boss sits alone at the deepest level, centered, closing the symmetry.
- Shape: typically monoculture (all square for boss chapters per MP48), relying entirely on coordinate placement for structure.
- Y-spacing: 1.5 units between levels, consistent throughout.
**Coordinate template:**
```
Root: (0, 0)
Level 1: (-1.5, 3.0), (0, 3.0), (1.5, 3.0)     # 3 nodes (1 center + 2 symmetric)
Level 2: (-1.5, 4.5), (0, 4.5), (1.5, 4.5)     # 3 nodes
Level 3: (0, 6.0)                                # Final boss (centered)

Lower prep chain: (0, -3.0), (0, -4.5), ...      # Vertical center chain
Side branches: (-1.5, -n), (1.5, -n)             # Symmetric pairs at each level
```
**Sources:** Finality Genesis cataclysm (Case 8, 28 quests, ALL square shape, every y-level has exactly 2 side branches at ±1.5 x — perfect bilateral symmetry). Classified as tree_branching in the topology system, but the symmetry constraint is a deliberate design choice not captured by the general tree layout algorithm.
**Cross-reference:** topology-coordinates.md Case 8; MP48 (Shape Monoculture) — boss tree chapters typically use a single shape; R57 (Hub Node Size Dominance) — the root hub should dominate its children.

---

## Scope Annotation — Cycle 11 Dataset-Derived Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP51 Diagonal Staircase | ✔ (staircase axis choice) | ✔ (per-tier node placement) | ✔ (check diagonal regularity) |
| MP52 Kill-Bounty Ladder | ✔ (bounty structure choice) | ✔ (per-column tier nodes) | ✔ (check column uniformity) |
| MP53 Symmetric Boss Tree | ✔ (symmetry constraint) | ✔ (per-level paired nodes) | ✔ (check bilateral symmetry) |

---

## Scope Annotation — Cycle 11 Phase 2 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP49 Spiral/Vortex | ✔ (advanced aesthetic choice) | ✔ (per-ring node placement) | ✔ (check spiral regularity) |
| MP50 Decorative Waypoint | ✔ (landmark planning) | ✔ (image placement) | ✔ (check waypoint coverage) |

---

## Part 13: Cycle 12 Phase 2 Patterns — Player-Validated Layout Techniques (MP54–MP55)

These patterns were identified during Cycle 12 Phase 2 cross-validation, derived from FTB Quests developer feedback on GitHub issues and player requests for better navigation tools. They address UI-level constraints that affect how topology choices translate into the player's actual experience of the quest book.

### MP54 — Quest Shape Legend (Visual Shape Key)

**Name:** Shape Legend / Preset System for Quest Book Navigation
**Applicable conditions:** Large packs (50+ chapters or 500+ quests) where players need to quickly understand what different quest shapes mean across the quest book. Most valuable when the pack uses a consistent shape vocabulary (per AP25 Shape Semantic Conflict avoidance) but doesn't document it in-game. Applicable to any pack type, but especially important for kitchen-sink and expert packs where players encounter many chapters with different shape roles.
**Implementation:**
- FTB team member MichaelHillcox proposed a "Quests Legend" feature in FTBTeam/FTB-Mods-Issues #1447: "Support a Legend in quests, ideally optional to preserve existing quests. This will effectively work as a preset system where each item in the legend is able to define different properties for the quest. Things like Shape, Color, etc."
- Until the Legend feature is implemented in FTB Quests, authors can approximate it by: (1) creating a dedicated "Guide" or "How to Read This Quest Book" chapter at the top of the book, with sample quests showing each shape and its meaning; (2) using decorative images (MP50) as shape-reference banners at chapter entry points; (3) documenting the shape vocabulary in the pack's description or wiki.
- The legend should cover: gear (starting hub), diamond (convergence/synthesis), pentagon (boss/combat), octagon (milestone), circle (optional), none (catalog), and the chapter's default shape.
- Monifactory's CONTRIBUTING.md is the only pack that formalizes shape guidance: "Larger quests should be reserved for important milestones."
**Sources:** FTBTeam/FTB-Mods-Issues #1447 (MichaelHillcox, FTB team member — proposed Quests Legend as a core FTB Quests feature); #1303 (desht, FTB dev — confirmed hierarchical shape system: file → chapter → quest); #1448 (desht — noted shape's role in locked/visible state communication). Monifactory CONTRIBUTING.md as the only formal shape style guide in the dataset.
**Cross-reference:** MP48 (Shape Monoculture); AP25 (Shape Semantic Conflict); topology-coordinates.md Phase 5 Shape Decision Tree.

---

### MP55 — Horizontal Layout Scrolling Compensation

**Name:** Navigation Compensation for Horizontally-Extended Layouts
**Applicable conditions:** Chapters using highway_branch or any topology where the bounding box width significantly exceeds height (aspect ratio > 2:1). FTB Quests currently lacks native simultaneous 2D scrolling — players with trackpads can scroll in both axes, but mouse users must use keyboard or click-and-drag to scroll horizontally, making wide layouts harder to navigate.
**Implementation:**
- For highway_branch layouts wider than 20 units, add decorative image waypoints (MP50) at major spine sections to provide visual landmarks for horizontal navigation.
- Consider breaking very wide chapters (>25 units) into sub-chapters or using a vertical-primary variant of highway_branch (rotate the spine 90° to make it vertical with horizontal branches).
- FTBTeam/FTB-Mods-Issues #2059 requests "simultaneous 2D scrolling" — FTB dev MichaelHillcox acknowledged "this is actually a fair point" but the feature is not yet implemented. Until then, horizontal layouts have an inherent accessibility disadvantage for mouse users.
- If the chapter must be horizontal, keep spine quest count manageable (≤ 15 spine nodes) and use `hide_dependency_lines: true` on spine-to-branch connections to reduce visual clutter during horizontal scrolling.
- Alternative: use the Monifactory diagonal staircase approach (MP51) which creates a diagonal primary axis — both x and y increase per step, giving the player visual progress in both scroll directions simultaneously.
**Sources:** FTBTeam/FTB-Mods-Issues #2059 (8ballpizza — "simultaneous 2D scrolling", MichaelHillcox response); topology-coordinates.md Case 10 (MM2 botania, 27.5 unit width) and Case 13 (FTB Evolution create, 30 unit width — the two widest chapters observed).
**Cross-reference:** MP46 (Highway+Branch Topology); MP51 (Diagonal Staircase) as the alternative non-vertical layout; R59 (Bounding Box Viewport Fit) for width limits; MP50 (Decorative Waypoint) for navigation aids.

---

## Scope Annotation — Cycle 12 Phase 2 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP54 Shape Legend | ✔ (pack-level shape documentation) | — | ✔ (check legend completeness) |
| MP55 Horizontal Scroll Compensation | ✔ (layout axis decision) | — | ✔ (check width vs scroll support) |

---

## Part 14: Cycle 12 Phase 4 Patterns — Reviewer-Extracted Spatial Archetypes (MP56–MP57)

These patterns were identified during the Cycle 12 Phase 4 completeness review (Reviewer B) as recurring spatial archetypes present in the Cycle 12 data but not previously formalized as named micro-patterns. Each is observed in at least 2 Cycle 12 chapters and is distinct from existing patterns MP51–MP55.

### MP56 — Tier Upgrade Column

**Name:** Tier Upgrade Column (parallel_columns specialization)
**Applicable conditions:** A chapter where multiple vertical columns sit side-by-side, each column representing parallel upgrade paths for different items within the same voltage/tier level. Each column contains the successive tiers of the same item or machine type (e.g., Basic → Advanced → Elite → Ultimate). Most common in expert packs with tiered machine upgrades (GT-style voltage tiers, Mekanism tiers).
**Implementation:**
- One vertical column per upgradeable item type, each at a fixed x-value.
- Within each column, y increases per tier level with consistent y-spacing (1.0 per tier).
- All nodes in a column share identical x-values — the column is perfectly vertical.
- Shape progression or shape monoculture signals "this is the same thing, upgraded." Size may increase slightly at higher tiers (1.0 → 1.25 → 1.5).
- Multiple columns sit side-by-side at different x-values, with x-spacing of 2.0–3.0 between columns.
- The number of tiers per column is typically 3–5 (matching the pack's tier system).
**Coordinate template:**
```
Column 1 (item A): (x1, 0), (x1, 1.0), (x1, 2.0), (x1, 3.0)  # Basic → Adv → Elite → Ult
Column 2 (item B): (x1+2.5, 0), (x1+2.5, 1.0), (x1+2.5, 2.0), (x1+2.5, 3.0)
Column 3 (item C): (x1+5.0, 0), (x1+5.0, 1.0), (x1+5.0, 2.0), (x1+5.0, 3.0)
...
Tier labels: consistent y-values across all columns at each tier level
```
**Sources:** Ragnamod_VII mekanism (~80 quests, 4-tier upgrade columns: Basic → Advanced → Elite → Ultimate); ReFactory lv_age and mv_age (voltage-tier columns: LV Motor → MV Motor → ...). Distinct from MP52 (Kill-Bounty Ladder, combat-oriented) and MP51 (Diagonal Staircase, cross-tier progression). The tier upgrade column is *within-tier* — each column represents parallel upgrade paths for different items at the same tier.
**Cross-reference:** topology-coordinates.md Phase 3 PARALLEL_COLUMNS; MP52 (Kill-Bounty Ladder) as the other parallel_columns specialization; R62 (Parallel Column Spacing Uniformity) for validation.

> **Generality note:** Observed in expert packs (Ragnamod_VII, ReFactory) with tiered machine systems. Applicable to any pack type with upgradeable item tiers, but most relevant for expert and kitchen-sink packs with Mekanism, GregTech, or similar tiered machine mods. Adventure and skyblock packs rarely have the tiered machine progression that triggers this pattern.

---

### MP57 — Starburst Info Hub

**Name:** Starburst Info Hub (radial information scatter)
**Applicable conditions:** A chapter's prologue or introductory section where a single hub quest at center has 6–10 information/tutorial quests arranged in a full 360° circle around it. Unlike hub_fan (where children have their own sub-trees), the starburst info hub's children are all leaf nodes — pure information delivery with no further progression. Most common as the first chapter or tutorial section of a pack.
**Implementation:**
- Place the hub quest at center (0, 0) with a distinctive shape (gear or hexagon) and large size (2.0).
- Arrange 6–10 info quests in a full circle at equal angular intervals around the hub.
- Use a radius of 2.5–4.0 units depending on quest count.
- Info quests are all leaf nodes (fan_out = 0) — they deliver text/tutorial content, not progression items.
- Shape vocabulary: use a distinctive chapter-level shape (hexagon, gear) to mark info nodes as different from progression content.
- `hide_dependency_lines: true` on the hub quest to prevent a starburst of dependency lines from overwhelming the visual field.
- Icon rate is typically high (50%+) on info quests to aid visual scanning.
**Coordinate template:**
```
Hub: (0, 0), shape: gear, size: 2.0

6 info quests (radius 3.0, step 60°):
  (0, -3.0), (2.6, -1.5), (2.6, 1.5), (0, 3.0), (-2.6, 1.5), (-2.6, -1.5)

8 info quests (radius 3.5, step 45°):
  (0, -3.5), (2.47, -2.47), (3.5, 0), (2.47, 2.47),
  (0, 3.5), (-2.47, 2.47), (-3.5, 0), (-2.47, -2.47)

All info quests: leaf nodes, shape: hexagon, size: 1.0, icon: thematic_item
```
**Sources:** CodeNameCIM2 prologue (12 quests, central welcome quest with 6 hexagonal info quests at equal angular intervals, 67% icon rate); ReFactory the_beginning (10 quests, central square welcome quest with 8 radiating info quests). The most common "first chapter" pattern in Cycle 12 data (3 of 7 packs use it for their prologue/intro chapter). Functionally distinct from MP46 (Highway+Branch) and MP53 (Symmetric Boss Tree).
**Cross-reference:** topology-coordinates.md Phase 3 HUB_FAN (the starburst is a leaf-only hub_fan variant); MP50 (Decorative Waypoint) for info-node visual aids; MP54 (Shape Legend) for documenting the info-node shape.

> **Generality note:** Observed in expert and Create-expert packs (CodeNameCIM2, ReFactory) for prologue chapters. The pattern is applicable to any pack type that needs an introductory info hub — kitchen-sink packs could use it for a "mod overview" chapter, adventure packs for a "world lore" introduction. No skyblock or pure adventure examples exist yet in the dataset.

---

## Scope Annotation — Cycle 12 Phase 4 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP56 Tier Upgrade Column | ✔ (upgrade path planning) | ✔ (per-tier node placement) | ✔ (check column alignment) |
| MP57 Starburst Info Hub | ✔ (prologue structure) | ✔ (radial node placement) | ✔ (check radial symmetry) |

---

## Part 13: Cycle 13 Patterns — Skyblock/Adventure/Farming (MP58–MP63)

These patterns emerge from the Cycle 13 research that focused on skyblock, adventure/RPG, and farming/lifestyle packs. They supplement the expert-pack-dominated patterns from earlier cycles with gameplay-specific design decisions unique to these underrepresented pack types.

### MP58 — Skyblock Perpendicular Branch

**Name:** Perpendicular Tool-Upgrade Branch
**Applicable pack types:** skyblock (Ex Nihilo / Ex Deorum only)
**Applicable conditions:** Skyblock packs where the sieve/mesh/crook upgrade chain is the central gameplay loop. The main progression runs along one axis (typically horizontal), while the tool upgrade sub-chain branches perpendicularly (typically vertical) from a specific node on the main chain. Most relevant for Ex Nihilo or Ex Deorum-based skyblock packs.
**Implementation:**
- Lay out the main getting_started chain horizontally (x increasing), covering: first tree → crook → string → sieve → basic resources.
- At the sieve node, branch vertically downward (y increasing) for the mesh upgrade chain: string mesh → flint mesh → iron mesh → diamond mesh → netherite mesh.
- Use 1.0–1.5 unit y-spacing for the mesh chain (tighter than the main chain's 2.0–3.0 x-spacing) because mesh upgrades are a rapid sequential progression.
- The mesh chain's root node (first mesh) should sit at the same x as the sieve quest but offset by 1.5–3.5 units in y.
- Shape: default for mesh nodes (they're a straightforward upgrade chain), with the sieve quest potentially marked with a distinctive shape.
**Coordinate template:**
```
Main chain (horizontal): (-11, -1) → (-8, -1) → (-5.5, -1) → (-4, -1) → (-2, -1)
Mesh branch (vertical from sieve): (-2, 1) → (-2, 2.5) → (-2, 3.5) → (-2, 4.5)
```
**Sources:** ATM9-Sky getting_started (mesh upgrade chain at x=-2.0 running y=1.0 to y=4.5, branching from sieve quest at (-2, -1)). ATM6-Sky ex_nihilio has a similar mesh chain but uses a different layout (mesh chain at x=0.0, y=-10 to y=-4). The perpendicular branch pattern makes the mesh upgrade visually subordinate to the main progression while keeping it accessible from the sieve quest.
**Cross-reference:** topology-coordinates.md Case 22 (ATM9-Sky getting_started); MP1 (Linear Chain) for the main chain pattern.

> **Generality note:** Observed in ATM-family skyblock packs. Specific to Ex Nihilo / Ex Deorum-based skyblock packs where mesh upgrades are a core mechanic. Non-skyblock packs never have this pattern because sieve progression doesn't exist outside skyblock.

> **Agent instruction:** For Ex Nihilo packs, the mesh upgrade chain consists of all mesh-tier items (string_mesh, flint_mesh, iron_mesh, diamond_mesh, netherite_mesh). All other progression items belong to the main chain. If the pack uses a different sieve mod, ask the user to identify the mesh upgrade items.

---

### MP59 — Nested Hub-Fan (Adventure Two-Stage)

**Name:** Nested Hub-Fan with Sub-Hub Extension
**Applicable conditions:** Adventure/RPG packs where the introduction chapter needs to present multiple mod paths (first-stage fan) while one or more paths require deeper progression chains (second-stage sub-hub). Most relevant for packs with 4-6 major mod systems where one system (typically the pack's namesake mod) has significantly more content than others.
**Implementation:**
- Place the root hub at a central position with a distinctive shape (hexagon, size 2.0).
- First-stage fan: 4-6 branches radiating at roughly equal angles, each leading to a mod-introduction quest.
- For the pack's primary mod (e.g., Dragon Survival in Dragoncraft), extend the branch with a linear chain to a sub-hub quest (3-4 units from the first-stage node).
- Second-stage fan: the sub-hub fans out to 5-8 collection/progression quests in a tight cluster (1.0-1.5 unit spacing).
- The sub-hub's fan-out direction should continue the branch's trajectory (e.g., if the first branch goes left, the sub-hub's fan continues leftward).
- Use choice rewards at the first-stage→sub-hub transition to let players select their class/path.
**Coordinate template:**
```
Root hub: (-4, 0), hexagon, size 2.0
First-stage fan (6 branches): (-6.5, -2.5), (-6.5, 0), (-4, 2.5), (-2, 2), (-2, -2), (-4, -2.5)
Dragon branch extension: (-8, 0) → sub-hub at (-9.5, 0)
Second-stage fan (7 quests from sub-hub): (-12.5, -1), (-11.5, -1), (-10.5, -1), (-11.5, 1), (-10.5, 1), (-13.5, 0), (-12.5, 1)
```
**Sources:** Dragoncraft the_beginning (20+ quests, root hexagon at (-4,0) with 6 first-stage branches, Dragon Survival branch extending left through a choice-reward quest to a sub-hub with 7 collection quests). The nested structure creates a 15-unit horizontal span — the widest hub_fan in the dataset.
**Cross-reference:** topology-coordinates.md Case 23 (Dragoncraft the_beginning); MP6 (Hub+Fan) for the simpler single-stage variant.

> **Generality note:** Observed in adventure/RPG packs. The nested hub-fan is applicable whenever one mod system is significantly deeper than others in the introduction chapter. Kitchen-sink packs typically don't need this because they give equal weight to all mods.

---

### MP60 — Decorative Barrier Gate

**Name:** Barrier/Barrier-Open Visual Gate System
**Applicable pack types:** farming/adventure (single-source observation)
**Applicable conditions:** Farming/adventure packs that use decorative images to visually fence off locked and unlocked content regions within a chapter. The barrier system uses two image states (closed barrier for locked regions, open barrier for accessible passages) to communicate progression state without text. Most relevant for packs with 4+ distinct content areas in a single chapter.
**Implementation:**
- Use `ftbquests:block/barrier` (2.0×2.0, rotation 0°) at the boundaries of locked content regions.
- Use `ftbquests:block/barrier_open` (1.1×1.1, rotation 45°) at the entry points of accessible regions.
- Place barrier images at the edges of content clusters, not overlapping with quest nodes.
- Use 2-3 barrier images per locked region boundary, spaced 0.75-1.0 units apart.
- Open barriers should be placed at passage points between the hub quest and its accessible branches.
- Barrier images use `dev: false, corner: false` (visible to all players, not just editors).
**Coordinate template:**
```
Locked region boundary: barrier images at (-5, -3), (-5.75, -3.75), (-5.75, -2.25) — 3 images forming a fence
Open passage: barrier_open images at (10.5, -1.5), (10.5, -4.5), (11.5, -3) — 3 images forming an opening
```
**Sources:** Life-in-the-Village-4 adventure_begins (12 decorative images: 5 barrier + 7 barrier_open, positioned around the root hub's three branches). This is the only pack in the dataset using this pattern, making it a unique visual storytelling technique from the dr3ams author lineage (RAD2/RAD3/LitV3/LitV4).
**Cross-reference:** topology-coordinates.md Case 24 (Life-in-the-Village-4 adventure_begins); MP47 (Compartment Region Layout) for the related concept of using decorative images for region delineation.

> **Generality note:** Observed only in Life-in-the-Village-4. The barrier-gate pattern is a novel visual technique that could be adopted by any pack type with gated content regions. It's most effective in farming/adventure packs where the player's progression through different content areas (mining, farming, exploration) benefits from visual gating.

---

### MP61 — Reward-Per-Quest Currency

**Name:** Consistent Per-Quest Currency Reward
**Applicable conditions:** Adventure/RPG packs that use a custom currency item (not ftbmoney, not XP) as the primary progression reward, given on every quest. The currency item is thematically tied to the pack's narrative (e.g., dragon parts in a dragon-themed pack). Most relevant for packs where the currency is both a reward AND a crafting ingredient for endgame items.
**Implementation:**
- Define a custom currency item (e.g., kubejs:elder_dragon_dust, kubejs:dragon_coin).
- Reward exactly 1 unit of the currency on every non-metadata quest in the chapter.
- The currency should appear as an `item` type reward (not `ftbmoney:money` or `command`).
- Pair the currency reward with a secondary reward (XP, choice, or practical items) to avoid the currency feeling like the only reward.
- The currency item should be referenced in quest icons for quests that spend it (shop/purchase quests).
- Maintain 100% reward coverage (every quest gets the currency) — partial coverage breaks the economy's predictability.
**Sources:** Dragoncraft the_beginning (7 of 18 non-metadata quests reward elder_dragon_dust, always count=1, paired with XP or item rewards). The currency creates a "dragon power" economy where progression is measured in dragon parts collected. Distinct from Magic-Superlative's ftbmoney economy (which uses a generic currency) and ModularTech-Odyssey's ftbmoney (which uses it for tier-gated purchases).
**Cross-reference:** MP18 (Reward Bridge) for the concept of rewards enabling next-step progression; MP52 (Kill-Bounty Ladder) for the alternative combat-currency model.

> **Generality note:** Observed in Dragoncraft (adventure/RPG). The reward-per-quest currency model is applicable to any pack with a strong thematic currency, but most effective in adventure/RPG packs where the currency is narratively justified. Kitchen-sink and expert packs typically use XP or loot tables instead.

---

### MP62 — Shape-as-Category Label

**Name:** One-Shape-Per-Quest Category Labeling
**Applicable conditions:** Small chapters (fewer than 10 quests) where each quest represents a distinct information category or gameplay domain. Instead of using a single chapter-level shape, each quest gets a unique shape that serves as a categorical label. Most relevant for welcome/tutorial chapters in packs with diverse content domains.
**Implementation:**
- Assign a unique shape to each quest based on its content domain:
  - gear: pack root / main progression entry
  - circle: quest book / QoL information
  - diamond: endgame / creative items
  - octagon: mining / resource gathering
  - pentagon: special mechanics / island management
- Set the chapter's `default_quest_shape` to one of the category shapes (typically the root's shape) for visual consistency.
- Pair each shape with a unique icon that reinforces the category (e.g., diamond_ore icon for the octagon mining quest).
- Maintain 100% icon rate — every quest must be visually identifiable without reading its title.
- Use the same shape consistently for the same category across all chapters (if the pack has multiple small info chapters).
**Sources:** Ragnamod VI Skyblock welcome (6 quests, 5 unique shapes: gear/circle/diamond/octagon/pentagon, 100% icon rate). This is the only welcome chapter in the dataset where shape serves as a categorical label. Compare to ATM9-Sky welcome (1 shape: hexagon) and ATM6-Sky skyblock_tips (2 shapes: heart/hexagon).
**Cross-reference:** topology-coordinates.md Case 25 (Ragnamod VI Skyblock welcome); MP54 (Shape Legend) for the related concept of documenting shape semantics.

> **Generality note:** Observed in Ragnamod VI Skyblock. The one-shape-per-quest approach is viable for small chapters (<10 quests) but would create visual noise in larger chapters. For chapters with 20+ quests, use 1-3 shapes with a default shape for the majority (MP54).

---

### MP63 — Box-Opening Reward Economy

**Name:** Consistent Loot-Box Reward Progression System
**Applicable conditions:** Adventure/survival packs that teach players a custom loot-box progression system through quest rewards. Every quest rewards a named box item (kubejs:makeshift_box, gear_box, etc.) alongside XP, teaching the box-opening mechanic through repetition. Most relevant for packs with custom KubeJS loot boxes as the primary reward delivery mechanism.
**Implementation:**
- Define 3-5 tiers of named box items via KubeJS (e.g., makeshift_box → gear_box → mischievous_box → legendary_box).
- Reward the lowest-tier box on every tutorial quest (count=1-2 for basic, count=5-8 for milestone quests).
- Pair every box reward with a small XP reward (2-25 XP) to provide immediate gratification alongside the delayed box-opening reward.
- Use size 2.0+ on convergence quests that mark the completion of tutorial sections, with higher-tier box rewards (count=5-8).
- Ensure the box item's tooltip or description explains what it contains, so players understand the reward before opening.
**Sources:** Rogue Mayhem steps_to_not_die (12 quests, every quest rewards kubejs:makeshift_box or kubejs:gear_box alongside XP, convergence quest rewards 8 makeshift_boxes). The box system creates a "loot piñata" feel where completing quests always gives a tangible reward to open. Distinct from Craftoria's random reward tables (which are invisible to the player) and Enigmatica's loot table delivery (which uses command rewards).
**Cross-reference:** MP18 (Reward Bridge) for reward-as-progression; MP14 (XP Bridge) for the XP component of the dual-reward system.

> **Generality note:** Observed in Rogue Mayhem (adventure/survival). The box-opening economy is applicable to any pack that wants to add a "surprise" element to quest rewards. The key is consistency — every quest must reward a box, or the economy breaks.

---

## Scope Annotation — Cycle 13 Phase 1 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP58 Skyblock Perpendicular Branch | ✔ (skyblock progression layout) | ✔ (mesh chain node placement) | — |
| MP59 Nested Hub-Fan | ✔ (adventure intro structure) | ✔ (two-stage fan placement) | ✔ (check sub-hub span) |
| MP60 Decorative Barrier Gate | — | — | ✔ (check barrier visibility) |
| MP61 Reward-Per-Quest Currency | ✔ (reward economy design) | ✔ (per-quest reward assignment) | ✔ (check 100% coverage) |
| MP62 Shape-as-Category Label | ✔ (small chapter structure) | ✔ (per-quest shape assignment) | ✔ (check <10 quest limit) |
| MP63 Box-Opening Reward Economy | ✔ (reward delivery design) | ✔ (per-quest box assignment) | ✔ (check box tier consistency) |

---

## Part 14: Cycle 13 Phase 2 Patterns — Player-Validated Skyblock/Adventure/Farming (PP8–PP12)

These patterns emerge from the Phase 2 cross-validation research that searched for player feedback on the MP58–MP63 patterns discovered in Phase 1. Each pattern captures how players actually experience the design decisions documented in the Phase 1 patterns, drawing on Chinese community tutorials (mcmod.cn post/6155), GitHub issue trackers, Bilibili let's plays, and CurseForge/mcmod.cn pack descriptions. The Phase 2 research confirmed that the skyblock/adventure/farming pack types have distinct player-experience profiles that differ from the expert and kitchen-sink packs that dominated earlier research cycles.

### PP8 — Side-Chain as Progression Relief Valve

**Applicable pack types:** skyblock (Ex Nihilo / Ex Deorum only)

**What players notice:** When the main progression chain hits a resource wall — the player can't craft the next machine because they lack a specific ore — the mesh upgrade side-chain provides an always-available alternative. Upgrading from flint mesh to iron mesh doesn't require any gated resources, just sieving time. The player experiences the perpendicular branch not as a separate progression dimension (as the pack author designed it) but as a "relief valve" — something to do when stuck.

**Pattern:** In skyblock packs with Ex Nihilo/Ex Deorum, the mesh upgrade chain (MP58) serves a dual role that config analysis alone doesn't reveal. Structurally, it's a perpendicular branch from the main chain. Experientially, it's a parallel activity that the player can retreat to whenever the main chain is blocked. This is because mesh upgrades are always available (just sieve more) while main-chain progression often requires specific items from other mods. The mcmod.cn adventure design article (post/6155) warns against "强制玩家必须依据流程走完整个内容，期间能提供的正向反馈反而很少" (forcing rigid paths with little positive feedback during the process) — the mesh chain solves this by providing constant micro-progress even when macro-progress is gated.

**Config implication:** The mesh upgrade chain should be designed so that every mesh tier is achievable without main-chain resources. If the iron mesh requires a component that's gated behind the main progression (e.g., a specific machine from another mod), the relief-valve function breaks and the player is stuck on both axes simultaneously. Verify that each mesh upgrade's recipe uses only items obtainable through sieving with the previous mesh tier.

**Source:** mcmod.cn post/6155 (adventure pack design philosophy — difficulty progression and positive feedback); ATM9-Sky getting_started config (mesh chain structure); Bilibili ATM9 Sky let's plays (108+ episodes confirm active community engagement with the progression system); FTB Skies 2 design (three mutually-supportive progression paths described as "互相成就").

**Validation status for MP58:** Partially validated. The perpendicular branch structure is confirmed in config data, and the design philosophy supports independent progression dimensions as relief valves. However, no direct player comment specifically addresses the mesh upgrade chain as a "separate dimension" — players talk about it as "what you do when stuck," which is the experiential equivalent.

---

### PP9 — The Hub Promise (branching hub as implicit choice guarantee)

**What players notice:** When a player opens an introduction chapter and sees a central hub quest with 5-6 branches radiating outward, they immediately interpret this as "I get to choose my path." The hub structure visually promises freedom of choice. If all branches except one are gated behind prerequisites the player doesn't have yet, the promise is broken — the hub is a lie, and the player is forced down a single path despite the visual suggestion of multiple options.

**Pattern:** The nested hub-fan structure (MP59) in adventure/RPG packs creates a specific player expectation: the first-stage fan branches represent equal-weight choices. When the pack's primary mod (e.g., Dragon Survival in Dragoncraft) has a deeper sub-hub extension while other branches are shallow (1-2 quests), the visual weight disparity communicates hierarchy that the player may not be ready for in the introduction chapter. The mcmod.cn adventure design article (post/6155) recommends "留下有机发现的空间，而不是死板地规定每一步" (leaving room for organic discovery instead of rigidly dictating every step) — a hub that only has one actually-accessible branch violates this principle because the visual structure implies choice that doesn't exist.

**Config implication:** In a nested hub-fan introduction chapter: (1) ensure that at least 60% of first-stage branches are immediately accessible (no prerequisites beyond the root hub's tasks), (2) make the sub-hub extension visually distinct from the first-stage branches (e.g., different quest size, a choice-reward transition node) so the player understands it's a "go deeper" option rather than a "go somewhere else" option, (3) if some branches must be gated, use `hide_until_deps_visible` on the gated branch's first quest so the hub doesn't visually promise inaccessible paths.

**Source:** mcmod.cn post/6155 (organic discovery vs rigid paths); Dragoncraft the_beginning config (6 first-stage branches with one extended sub-hub); SteamPunk pack description (1000+ quests across skills, magic, Tetra, and steam tech — multiple accessible paths); PP3 (The Invisible Wall) for the related concept of gating without feedback.

**Validation status for MP59:** Conceptually validated. The two-stage exploration model aligns with adventure pack design philosophy and the hub-fan structure is confirmed in config data. The "hub promise" pattern captures a player-experience risk that wasn't visible from config analysis alone: the visual weight of branches creates expectations about accessibility.

---

### PP10 — The Barrier Tease (decorative gating as anticipation builder)

**What players notice:** When decorative barrier images fence off a region of the quest book, the player can see the quests behind the barrier but can't access them yet. This creates one of two experiences: anticipation ("I can see what's coming, and I'm motivated to unlock it") or frustration ("I can see cool stuff that I can't touch, with no clear path to get there"). The difference depends entirely on whether the unlock condition is communicated — can the player trace a dependency path from their current position to the barrier's entry point?

**Pattern:** The decorative barrier gate system (MP60) in farming/adventure packs creates a visual "coming soon" signal that other pack types achieve through `hide_until_deps_visible` (which hides content entirely). The barrier approach is more transparent — it shows locked content openly — but this transparency comes with a risk: if the player can't figure out how to unlock the barrier, the tease becomes a taunt. The mcmod.cn adventure design article (post/6155) discusses "难度递进" (difficulty progression) where "上一个世界的顶端装备对应于这个世界的小怪" (previous world's top equipment = this world's basic mobs) — this tier bridge principle means that barrier-gated content should be reachable from the player's current tier, not from a tier they haven't reached yet.

**Config implication:** For every decorative barrier in a quest chapter: (1) ensure the barrier's corresponding open-barrier image becomes visible when the prerequisite quests are completed (use `hide_until_deps_visible: false` on the barrier images but `true` on the quests behind them, creating a staggered reveal), (2) the root quest of the gated region should have a description that explicitly states what's behind the barrier and how to reach it, (3) never place a barrier in front of content that requires cross-chapter prerequisites without a signpost quest in the current chapter.

**Source:** mcmod.cn post/6155 (tier bridge principle, difficulty progression); Life-in-the-Village-4 adventure_begins config (12 barrier/barrier_open images); PP3 (The Invisible Wall) for the contrast between visible-but-locked and entirely-hidden gating.

**Validation status for MP60:** Indirectly validated. The barrier/open visual communication aligns with the design principle of providing gating WITH feedback (as opposed to `hide_until_deps_visible` which hides content entirely). The mcmod.cn design philosophy supports visible gating with clear unlock paths, but no direct player feedback on the specific barrier image system was found. The pattern's value is in making gating transparent rather than invisible.

> **Agent instruction:** FTB Quests decorative images do not support per-player visibility. Use `hide_until_deps_visible` on quests behind the barrier, not on the barrier images themselves.

---

### PP11 — The Mystery Box Trust (consistent loot-box rewards as trust builder)

**What players notice:** When every quest rewards a loot box (kubejs:makeshift_box, gear_box, etc.), the player quickly learns that completing quests always produces a tangible, openable reward. This creates a "quest = box" trust loop: the player is motivated to complete quests because they know a box-opening moment awaits. However, if box contents are inconsistent (one box gives diamonds, the next gives dirt), or if some quests reward boxes while others don't, the trust erodes — the player stops seeing boxes as reliable rewards and starts seeing them as "random junk I can't count on."

**Pattern:** The box-opening reward economy (MP63) creates a specific player psychology that differs from both fixed-item rewards and ftbmoney rewards. Fixed items are predictable but boring; ftbmoney is flexible but abstract; loot boxes are exciting (surprise element) but risky (inconsistency). The ATM-10 discussion #3539 provides the clearest articulation of this tension: a player argued that generous quest rewards "invalidate the whole balance pass" while a collaborator countered that "the only thing that could actually break progression would be gifting out ATM Stars." In the box-opening context, the trust depends on consistency: if every box of a given tier gives roughly equivalent value, the system works; if value varies wildly, the system feels like gambling rather than rewarding.

**Config implication:** For a box-opening reward economy: (1) define box tiers clearly in the quest book's introduction chapter so players know what to expect from each tier, (2) ensure each box tier has a roughly consistent value range (±20% variance) — use loot tables with minimum-value floors, (3) never skip a box reward on a quest that follows the "every quest gets a box" pattern — breaking consistency destroys the trust loop, (4) pair every box with a small XP reward to provide a guaranteed baseline even if the box contents disappoint.

**Source:** ATM-10 Discussion #3539 (quest reward generosity debate); Rogue Mayhem steps_to_not_die config (every quest rewards makeshift_box or gear_box alongside XP); mcmod.cn Loot Bag Mod page (战利品包 as established mechanic); StoneBlock 4 #9954 (quest reward loss after server reset is catastrophic for trust).

**Validation status for MP63:** Partially validated. Loot boxes as quest rewards are accepted when consistent and transparent, but opaque or buggy delivery destroys trust. The "mystery box trust" pattern captures the player-experience dynamic that config analysis alone can't reveal: the emotional contract between consistent reward delivery and player motivation.

---

### PP12 — The Shape Roulette (many shapes in small chapters as double-edged sword)

**What players notice:** When a 6-quest welcome chapter uses 5 different shapes (gear, circle, diamond, octagon, pentagon), each quest looks visually distinct — the player can tell them apart at a glance. But the visual distinctiveness comes at a cost: the player doesn't have enough quests to learn what each shape "means." In a 100-quest chapter, 5 shapes build a vocabulary through repetition; in a 6-quest chapter, 5 shapes are just 5 arbitrary decorations.

**Pattern:** The shape-as-category labeling approach (MP62) works differently in small chapters than in large ones. In large chapters (100+ quests), shape monoculture (MP48) or a small shape vocabulary (2-3 shapes) lets players build a mental dictionary through repeated exposure. In small chapters (<10 quests), the player sees each shape only once — there's no repetition to build meaning. The shape serves as a visual label (each quest looks different) but not as a semantic signal (the player doesn't learn "hexagon = tech progression"). FTB team member MichaelHillcox's "Quests Legend" feature request (#1447) confirms this gap: the mod doesn't provide built-in shape documentation, so players must infer meanings from context — and in a 6-quest chapter, there isn't enough context.

**Config implication:** For small chapters (<10 quests): (1) if using shape-as-category, pair each shape with a distinctive icon that reinforces the category (the icon carries the meaning, the shape carries the distinctiveness), (2) include a brief description in the chapter's root quest that explains the shape vocabulary, (3) don't use more than 4 distinct shapes in a chapter with fewer than 8 quests — beyond that, shapes become noise rather than signal, (4) if the pack has multiple small info chapters, use the SAME shape-category mapping across all of them to build cross-chapter vocabulary.

**Source:** Ragnamod VI Skyblock welcome config (6 quests, 5 unique shapes, 100% icon rate); FTBTeam/FTB-Mods-Issues #1447 (MichaelHillcox "Quests Legend" feature); MP48 (Shape Monoculture) for the contrast with large-chapter shape usage; MP54 (Shape Legend) for the documentation approach.

**Validation status for MP62:** Inconclusive. The pattern is observed in config data, and the shape-as-category approach is theoretically viable for small chapters. However, no direct player feedback was found about whether the 5-shape-in-6-quests approach helps or confuses. The "shape roulette" pattern captures the risk: without enough repetition, shapes are decorations, not vocabulary.

---

## MP58–MP63 Phase 2 Validation Summary

| Pattern | Validation Status | Key Evidence | Player-Experience Risk |
|---------|:---:|---|---|
| MP58 Skyblock Perpendicular Branch | Partially validated | mcmod.cn post/6155, ATM9 Sky let's plays, FTB Skies 2 design | Relief valve breaks if mesh chain requires gated resources |
| MP59 Nested Hub-Fan | Conceptually validated | mcmod.cn post/6155, SteamPunk 1000+ quests, Dragoncraft config | Hub promise broken if branches are all gated |
| MP60 Decorative Barrier Gate | Indirectly validated | mcmod.cn post/6155, Life-in-the-Village-4 config | Barrier tease becomes frustration without unlock path communication |
| MP61 Reward-Per-Quest Currency | Not directly tested | No specific player feedback found on thematic currency | Currency fatigue if paired with too many other reward types |
| MP62 Shape-as-Category Label | Inconclusive | FTB-Mods-Issues #1447, Ragnamod VI config | Shape roulette: too many shapes, too few quests to build vocabulary |
| MP63 Box-Opening Reward Economy | Partially validated | ATM-10 #3539, StoneBlock 4 #9954, Rogue Mayhem config | Mystery box trust breaks with inconsistent value or buggy delivery |

---

## Scope Annotation — Cycle 13 Phase 2 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| PP8 Perpendicular Progression Relief | ✔ (skyblock pacing design) | — | ✔ (verify mesh chain independence) |
| PP9 The Hub Promise | ✔ (adventure intro design) | — | ✔ (verify branch accessibility) |
| PP10 The Barrier Tease | — | — | ✔ (verify unlock path communication) |
| PP11 Mystery Box Trust | ✔ (reward economy design) | ✔ (box value consistency check) | ✔ (verify box tier consistency) |
| PP12 Shape Roulette | ✔ (small chapter design) | ✔ (shape count vs quest count) | ✔ (verify cross-chapter shape consistency) |

---

## Part 14: Cycle 14 Phase 1 Patterns — Non-Expert Hidden Gems (MP64–MP67)

Cycle 14 focused on hidden-gem packs that are not expert-tier but have distinctive design choices. These four patterns capture recurring decisions observed across 11 newly researched non-expert and skyblock packs.

### MP64 — Command-Reward-as-Invisible-Loot-Table

**Name:** Command Reward Delivering Loot Table Invisibly
**Applicable conditions:** Kitchen-sink or adventure packs that want to deliver mod-themed loot boxes without exposing the reward mechanics in the quest UI. Observed in the Enigmatica lineage (E6 → E9E → E9 non-expert) and partially in Mincemeat-2.
**Implementation:**
- Use `type: "command"` rewards with the pattern: `/execute at @p run loot spawn ~ ~1 ~ loot <namespace>:loot_boxes/<themed_chest>`.
- Each command reward gets a custom `icon` (the loot box item, e.g., `kubejs:farmers_delight`) and a `title` naming the loot source.
- The player sees a command execute and items appear, with no visible "reward" in the quest book UI — this creates a surprise-and-delight moment.
- Command rewards are typically 80–100% of all rewards in the chapter. XP is used sparingly as a secondary reward for tutorial quests.
- Pair with `hexagon` shape on quests that deliver command rewards (hexagon marks "important processing node").
- Use `hide_dependency_lines: true` on 30–50% of quests to reduce visual clutter when most rewards are invisible.
**Sources:** Enigmatica9 chapter_one (68 quests, 56 command rewards = 82%, hexagon-dominant); Enigmatica9 mekanism (59 quests, 52 command rewards = 88%); Enigmatica9 create (61 quests, 53 command rewards = 87%). Mincemeat-2 getting_started (6 command rewards on tutorial quests). This pattern is the evolutionary successor to MP17 (Loot Table Reward) — where E10 moved to `type: "loot"` with `table_id`, the non-expert E9 retains the command-reward approach from E6.
**Cross-reference:** topology-coordinates.md Case 28; MP17 (Loot Table Reward); R42 (Command Reward Safety).

---

### MP65 — Zero-Reward Skyblock

**Name:** Skyblock Progression-as-Reward
**Applicable conditions:** Skyblock modpacks where the act of unlocking new resources, recipes, and dimensions IS the reward, making explicit quest rewards unnecessary. Validated across 5 of 6 skyblock packs in Cycle 14.
**Implementation:**
- Set zero rewards on all (or nearly all) quests. The only exception may be tutorial/welcome quests that give XP (5–10 XP) to introduce the reward system.
- Shape vocabulary is minimal — most skyblock zero-reward packs use `default_quest_shape: ""` (shape monoculture) with occasional overrides for milestones.
- Use `optional: true` on 5–15% of quests to mark side content that isn't required for progression.
- Task types remain primarily `item` (80–95%) with occasional `checkmark` for tutorial steps.
- Multi-dep quests (2–4 dependencies) mark convergence points where multiple resource streams combine into a new machine or material.
- `hide_dependency_lines` is rare (0–10 per chapter) since the simple linear/parallel topology doesn't need clutter reduction.
**Sources:** GregFactory-Sky (94 quests, 0 rewards across 4 chapters); Ultimate-Progression-Sky (362 quests, 0 rewards across 4 chapters); Cobblemon-Radically-Reimagined (352 quests, 0 rewards across 4 chapters); Enigmatic-Skies (113 quests, 0 command/xp rewards — uses loot+choice instead); Extraordinary-Energy-Modern (73 quests, near-zero rewards). Validates and extends MP41 (Zero-Reward Design) from expert GT packs to skyblock context.
**Cross-reference:** topology-coordinates.md Cases 29, 32; MP41 (Zero-Reward Design for expert context).

---

### MP66 — Extreme Fan-In Convergence

**Name:** Single Quest with 10+ Dependencies as Capstone
**Applicable conditions:** Any chapter with a synthesis/capstone quest that requires completing many prerequisite quests. Particularly common in Create-focused packs and collection-catalog chapters where a final machine or structure requires components from many production chains.
**Implementation:**
- The convergence quest should have 10–50 dependencies, each pointing to a prerequisite quest.
- Use `hide_dependency_lines: true` on the convergence quest to prevent visual spaghetti from 10+ incoming lines. Note: see AP37 for convergence contexts where `hide_dependency_lines` should be set to `false` on the last 3-5 quests before the capstone, so the player can visually trace the final convergence paths and avoid backtracking bookkeeping confusion.
- The convergence quest should use a distinctive shape (diamond, gear, or octagon) and `size: 1.5–2.0` to mark it as a milestone.
- Position the convergence quest below (higher y) or to the right (higher x) of all its dependencies so it appears as the natural endpoint.
- Pair with `dependency_requirement: "all_completed"` (the default) to enforce that ALL prerequisites must be done.
- Consider adding `subtitle` text explaining what the convergence represents (e.g., "Bring all components together").
**Sources:** CreateBlock farmer (1 quest with 47 dependencies — highest single-quest dep count in dataset); CreateBlock create (5 multi-dep quests with max 3 deps); AOF-The-Frozen-Hope mekanism (9 multi-dep quests, max 2 deps); Mincemeat-2 overworld_adventure (31 multi-dep quests, max 5 deps). The 47-dep quest in CreateBlock is an extreme case — most packs stay under 10 deps per quest.
**Cross-reference:** topology-coordinates.md Case 28; MP8 (Fan-In Convergence); R61 (Convergence Point Visual Prominence).

---

### MP67 — Task-Type Diversity in Adventure Packs

**Name:** Multi-Modal Task Design for Varied Gameplay
**Applicable conditions:** Non-expert adventure and exploration packs that want to offer gameplay variety beyond "craft and submit." The pack includes mods with diverse interaction types (boss fights, dimension exploration, structure discovery, biome visiting, stat tracking).
**Implementation:**
- Use 6–11 distinct task types across the chapter: `item` (crafting/submission), `kill` (boss/mob kills), `structure` (locate structures), `observation` (observe blocks/entities), `advancement` (vanilla or mod advancements), `dimension` (visit dimensions), `biome` (visit biomes), `gamestage` (gate progression stages), `stat` (track player stats), `custom` (mod-specific addon tasks).
- Distribute task types by chapter theme: adventure chapters use kill+structure+dimension; magic chapters use item+observation+advancement; tech chapters use item+checkmark.
- `structure` tasks are particularly valuable for exploration chapters — they require the player to physically locate and enter a structure, creating genuine discovery moments.
- `gamestage` tasks in non-expert packs serve as soft gates (the player can explore but can't progress the quest line until the stage is unlocked via other means).
- Use `choice` rewards at the end of major sections to let players pick their next upgrade path.
- `observation` tasks with `observe_type: 0` (block observation) work well for tutorial content — the player must look at a specific block or machine.
**Sources:** Mincemeat-2 (530 quests, 11 task types: item/kill/structure/observation/advancement/dimension/biome/gamestage/stat/custom/checkmark — most diverse non-expert pack in dataset). overworld_adventure: structure(23), kill(36), observation(14), biome(6). extraterrestrial_adventure: structure(24), kill(31), dimension(11). ice_and_fire: observation(8), custom(2), kill(9). the_aether: observation(21) — pure observation chapter. Contrast with GregFactory-Sky (94 quests, 2 task types: item+checkmark) to see how pack philosophy determines task diversity.
**Cross-reference:** topology-coordinates.md Case 30; MP4 (Task Variety Ladder); RAD3 (13 task types, most diverse expert pack).

---

## Scope Annotation — Cycle 14 Phase 1 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP64 Command-Reward-as-Invisible-Loot | ✔ (reward economy design) | ✔ (command reward formatting) | ✔ (verify loot table path validity) |
| MP65 Zero-Reward Skyblock | ✔ (skyblock pacing design) | — | ✔ (verify progression gates work without rewards) |
| MP66 Extreme Fan-In Convergence | — | ✔ (convergence quest formatting) | ✔ (verify all deps are reachable before convergence) |
| MP67 Task-Type Diversity in Adventure | ✔ (adventure chapter design) | ✔ (task type selection per chapter) | ✔ (verify task types match available mods) |

---

## Part 15: Cycle 14 Phase 1 Topology Patterns — Coordinate-Level Discoveries (MP68–MP69)

These patterns emerged from the Phase 1 topology coordinate extraction across 11 Cycle 14 packs. They capture coordinate-level layout decisions that were not visible in the earlier statistical analysis.

### MP68 — Optional-Only Side Content Hub

**Name:** 100%-Optional Hub Fan for Bonus Content
**Applicable conditions:** Skyblock or kitchen-sink packs where a chapter represents purely optional bonus content — side activities that enhance the experience but aren't required for progression. The author wants to present multiple optional activities without implying any of them are mandatory.
**Implementation:**
- Use hub_fan topology with `optional: true` on every quest, including the root.
- Set `default_quest_shape: ""` (shape monoculture) and do NOT override shapes on any quest — the flat visual field reinforces that no quest is more important than another.
- Do NOT use size hierarchy (all quests at size 1.0) and keep icon rate at 0% — any visual emphasis would contradict the "all optional" message.
- Arrange branches at roughly equal angles (120° for 3 branches, 90° for 4) to distribute visual weight evenly.
- The root quest serves as an organizational center but is itself optional — the player can ignore the entire chapter without consequence to main progression.
- Use `item` rewards (practical items) rather than XP or choice rewards to avoid incentivizing specific branches over others.
**Coordinate template:**
```
Root: (0, -1), size 1.0, optional: true
Branch A (left): (-1.5, 1) → (-1.5, 3) → (-1.5, 5.5) → (-1.5, 7.5)
Branch B (center): (0, 3) → (0, 5.5) → (0, 7.5)
Branch C (right): (1.5, 1) → (3, 1) → (3, 3) → (4.5, 1)
All quests: optional: true, shape: default, size: 1.0
```
**Sources:** Extraordinary-Energy-Modern skyblock (14 quests, 100% optional, hub_fan with 3 symmetric branches, shape monoculture, 0% icon rate, 0 size overrides). This is the only chapter in the dataset where every quest is optional — the next highest is Extraordinary-Energy-Modern skyblock's 14/15 optional rate. The pattern creates a "buffet-style" exploration where the player picks and chooses without pressure.
**Cross-reference:** topology-coordinates.md Case 34; MP65 (Zero-Reward Skyblock) — the optional-only hub is the spatial counterpart to the reward-less economy; MP10 (Optional Side Quests) for the general optional-content concept.

> **Generality note:** Observed only in Extraordinary-Energy-Modern. The 100%-optional chapter is applicable to any pack type that needs a bonus-content chapter — skyblock packs for side-system introductions, kitchen-sink packs for QoL tutorials, adventure packs for lore-only chapters. The key insight is that the absence of visual hierarchy (shape, size, icon) communicates optionality more effectively than the `optional` flag alone.

---

### MP69 — Dual-Grid Convergence Catalog

**Name:** Two Parallel Grid Regions with Convergence Funnel
**Applicable conditions:** Chapters that catalog two parallel mod systems (e.g., two farming mods, two storage mods, two energy mods) where each system gets its own grid layout, and the chapter's capstone quest requires items from both systems. Most relevant for collection-catalog chapters in multi-mod packs.
**Implementation:**
- Create two identical grid regions (3–5 columns × 4–6 rows) with 1.0-unit spacing within each grid.
- Separate the grids by 8–12 units of empty x-space to visually distinguish the two mod systems.
- Between the grids (at the midpoint x), create a convergence row: a horizontal chain of 5–8 quests that each depend on one or more quests from each grid.
- The convergence funnel quest (the chapter capstone) sits at the center of the convergence row with 10+ dependencies collecting from both grids.
- Use `hide_dependency_lines: true` on the convergence quest to prevent line spaghetti from 10+ incoming dependencies.
- Shape: monoculture for grid quests (all default), hexagon or diamond for the convergence milestones only.
- Size: 1.0 for grid quests, 1.5 for convergence milestones, 2.0 for the capstone funnel quest.
**Coordinate template:**
```
Grid A (left mod): x=[4..6], y=[1.5..5.5], 3 cols × 5 rows, 1.0-unit spacing
Grid B (right mod): x=[14..16], y=[1.5..5.5], 3 cols × 5 rows, 1.0-unit spacing
Convergence row: x=[7..13], y=[-1..0], horizontal chain
Capstone: (10, 1.5), size 2.0, 47 dependencies, hide_dependency_lines: true
```
**Sources:** CreateBlock farmer (57 quests, two 3×5 farming grids separated by 8 units, connected by a convergence row with a 47-dep capstone quest). The dual-grid layout is the spatial expression of "these are two independent systems that converge at the endgame." The 47-dependency capstone is the highest single-quest dep count in the dataset (validates MP66 Extreme Fan-In).
**Cross-reference:** topology-coordinates.md Case 33; MP66 (Extreme Fan-In Convergence) for the capstone quest design; MP47 (Compartment Region Layout) for the related concept of spatially separating mod regions.

> **Generality note:** Observed in CreateBlock (Create multi-mod pack). The dual-grid pattern is applicable to any chapter that catalogs two parallel systems — farming mods, storage mods, energy mods, or any pair of mods with similar functionality. The 8-unit separation is critical: less than 6 units makes the grids visually merge; more than 12 units pushes the chapter width beyond the R59 warning threshold.

---

## Scope Annotation — Cycle 14 Phase 1 Topology Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP68 Optional-Only Side Hub | ✔ (bonus content structure) | ✔ (radial optional placement) | ✔ (verify 100% optional flag) |
| MP69 Dual-Grid Convergence | ✔ (catalog chapter structure) | ✔ (dual-grid + funnel placement) | ✔ (verify inter-grid separation) |

---

## Part 16: Cycle 14 Phase 2 — Player-Validated Patterns (PP13–PP14)

These patterns emerge from cross-referencing Phase 1 config data with real player feedback from GitHub issue trackers, MC百科 community articles, and Chinese pack-author discussions. They capture the *player's* expectations and mental models around reward systems and progression pacing — things that are invisible in config analysis but become visible when players complain.

### PP13 — The Reward-Type Contract (consistent reward mechanics within a chapter)

Players develop an implicit contract with the quest book about how rewards work. When a chapter uses command rewards (MP64), the player learns "completing a quest spawns items nearby." When it uses loot table rewards, the player learns "a mystery box appears." When it uses choice rewards, the player learns "I pick from a menu." The contract is broken when the reward *type* switches unexpectedly within the same chapter or group — the player's learned expectation about how to receive and interact with rewards is violated.

The contract has three observable layers: (1) the *delivery mechanism* (command, loot table, item, choice, XP), (2) the *interaction model* (passive receive vs active choice vs mystery roll), and (3) the *claim flow* (individual claim vs "Claim All" button). Each layer must be consistent within a chapter for the player to build a fluent interaction rhythm.

**Evidence:** EnigmaticaModpacks/Enigmatica10 #517 — player esbraff reported "Chipped quest in Building and Tools tab has choice reward, which is presumably meant to be random reward just like other quests." The player noticed a single quest using choice rewards among quests that use random rewards — the type inconsistency was immediately flagged as a bug, even though the reward itself was functional. The pack collaborator MuteTiefling confirmed and fixed it: "That's swapped over to random rewards now." This demonstrates that players *do* track reward-type consistency at the chapter level, and a single outlier feels like an error.

FTBTeam/FTB-Mods-Issues #509 adds a system-level dimension: FTB dev desht explained that loot rewards are "specifically excluded from being claimable via 'Claim All'" by design, because "if the player's getting a reward that they don't know in advance, they should at least know exactly which quest it came from." FTB team member MichaelHillcox proposed a compromise UI showing a list of pending loot rewards to roll individually or all at once. This means that mixing loot rewards (unclaimable via bulk) with item rewards (claimable via bulk) within the same chapter creates a *mechanical* inconsistency in the claim flow — the player hits "Claim All," some rewards are missing, and they must go back and individually open each loot-reward quest. The ATM-10 discussion #3539 further demonstrates that reward generosity is debated within the same pack's community, with player xiaoxiao921 arguing rewards "skip arbitrary progression steps" while collaborator TheBedrockMaster defends them as standard kitchen-sink practice.

**Implementation guidance:** Within a single chapter, use one primary reward delivery mechanism, with at most one supplementary type (XP on tutorials only). This unified threshold aligns with R88 (Reward-Type Contract Enforcement), which flags chapters with more than two distinct reward types (excluding XP). If the chapter uses command rewards (MP64), ALL non-tutorial rewards should be commands (with consistent icon and title formatting). If the chapter uses loot tables (MP17), ALL non-tutorial rewards should be loot tables (with consistent crate naming). The only supplementary type permitted without triggering the contract violation is XP on tutorial quests, which is universally understood as additive. Never mix claim-flow-incompatible reward types (loot + item) within the same chapter without explicitly communicating the difference in quest descriptions.

**Sources:** EnigmaticaModpacks/Enigmatica10 #517 (esbraff — choice vs random reward inconsistency flagged as bug); FTBTeam/FTB-Mods-Issues #509 (desht — loot rewards excluded from Claim All by design; MichaelHillcox — proposed UI improvement); AllTheMods/ATM-10 #3539 (xiaoxiao921 vs TheBedrockMaster — reward generosity debate).
**Cross-reference:** MP64 (Command-Reward-as-Invisible-Loot-Table) for the command reward pattern; MP17 (Loot Table Reward) for the loot table alternative; PP11 (Mystery Box Trust) for the trust dimension of randomized rewards; R88 (Reward-Type Contract Enforcement) for the formal validation rule implementing this pattern.

**Multiplayer applicability:** In server environments, the reward-type contract interacts with permission systems. Command rewards (MP64) require server operator permissions — if the server's permission plugin misconfigures the `/execute` or `/loot` commands, the entire chapter's reward delivery silently fails, breaking the contract at a system level rather than a design level. Loot table rewards are more resilient to permission issues since they use the vanilla loot system. Item rewards are the most portable across server configurations. In team-based play, the contract's impact is diluted: when multiple players complete the same quest simultaneously, each receives their reward individually, so the interaction rhythm is per-player rather than shared. However, if one player's reward fails due to server permissions while another's succeeds, the inconsistency becomes visible between players, which is more confusing than a uniform failure. Authors targeting server deployments should prefer item or loot rewards over command rewards, or verify permission configurations before relying on command-based delivery.

---

### PP14 — Progression-as-Reward Social Contract (skyblock and expert context)

[Design guidance — requires mod-mechanics knowledge, not auto-verifiable. Use as Step 2 design principle, not Step 5 validation rule.]

In skyblock and expert packs, players accept a different reward contract than in kitchen-sink packs: the act of unlocking new resources, recipes, and dimensions IS the reward. The quest book serves as a progression map rather than a gift-dispensing machine. This contract is not merely the absence of rewards (MP65) — it is a positive design philosophy where the *satisfaction of advancement* replaces material incentives.

The social contract has two conditions that must be met for it to hold: (1) every quest must produce a visible progression effect (unlocking a recipe, granting access to a new dimension, enabling a new machine tier), and (2) the progression effect must be *immediately perceivable* — the player should feel the difference within 5 minutes of completing the quest. When these conditions are met, zero-reward design is not merely tolerated but appreciated, because the player's attention stays on the progression arc rather than being distracted by reward inventory management.

The contract breaks when a quest produces no perceivable progression effect — the player submits items, nothing visible changes, and the lack of an explicit reward makes the quest feel pointless. This is particularly damaging at tier boundaries where the next tier's content isn't immediately accessible (e.g., a quest unlocks the nether but the player hasn't built the portal yet).

**Evidence:** The MC百科 adventure pack design article (bbs.mcmod.cn thread-21004) articulates the philosophy directly: "玩家在每个世界的收获都是正反馈的" (player gains in every world provide positive feedback). The article recommends dimension-based progression where each world transition delivers a clear power-level increase — "上一个世界的顶端装备对应于这个世界的小怪" (previous world's top gear = this world's basic mobs). This is the positive-feedback principle applied to the progression-as-reward model: every step forward must *feel* like a step forward, even without explicit reward items. The article further warns that "过多的套娃只会让玩家厌烦" (excessive nesting will only annoy players) — when progression requires too many intermediate crafting steps without perceivable advancement, the zero-reward contract collapses because the player can't feel the progress.

GregFactory Sky's mcmod.cn page (modpack/707) demonstrates what happens when the contract is strained: the pack has zero rewards across 94 quests in 4 chapters, but the author explicitly acknowledges "不完整的任务：作者还没搓完" (incomplete quests: author hasn't finished yet). Without complete progression chains, the zero-reward design leaves players with nothing — neither rewards nor advancement. The pack received 75% positive votes but was labeled "无人问津" (niche/unattended), suggesting that zero-reward design demands *more* authoring effort, not less, because every quest must carry its weight through progression value alone.

Extraordinary Energy Modern's mcmod.cn page (modpack/1377) demonstrates the contract in a tech-skyblock context: the pack increases Mekanism power consumption to 1000× and focuses entirely on "能源建设、工业扩张与自动化生产" (energy construction, industrial expansion, automation production). The zero-reward design works because every quest advances the player's industrial infrastructure — the progression IS the reward, measured in megajoules rather than diamonds.

**Implementation guidance:** In zero-reward chapters (MP65), verify that every quest produces at least one perceivable progression effect. Use the quest description to explicitly name what the quest unlocks: "Completing this unlocks the Diamond Mesh recipe" or "You can now access the Nether dimension." If a quest's only effect is to gate a later quest (chain-link with no immediate payoff), merge it with the next quest to avoid the "submit items for nothing" feeling. Use `hide_until_deps_visible: true` on chained quests so the player only sees the next step when they're ready for it, reducing the perception of a long rewardless grind ahead.

**Sources:** MC百科 bbs thread-21004 (冒险包设计思路 — dimension-based progression, positive feedback principle, "过多的套娃" warning); GregFactory Sky mcmod.cn/modpack/707 (zero rewards + incomplete content = "无人问津"); Extraordinary Energy Modern mcmod.cn/modpack/1377 (zero rewards in tech skyblock with 1000× power scaling).
**Cross-reference:** MP65 (Zero-Reward Skyblock) for the config-level pattern; MP41 (Zero-Reward Design for expert context); PP1 (Trust Contract) — the progression-as-reward contract is a specialized form of the trust contract where the pack promises advancement instead of items.

**Multiplayer applicability:** The progression-as-reward model assumes a single-player experience where quest completion and progression unlock are atomically linked. In team-based server play, this assumption breaks: when one player completes a quest that unlocks a recipe or dimension, other team members who contributed resources but didn't submit the quest may not receive the unlock. This creates a "progression split" where team members have divergent access to content, undermining the cooperative experience. Server world resets compound the problem: unlike item rewards that can be re-given after a crash, progression unlocks (dimension access, recipe knowledge) are lost permanently and cannot be restored without manual intervention. Authors targeting server environments should consider using Game Stages or similar shared-progression mods to ensure team-wide unlock synchronization, and should document the pack's progression philosophy in the server's welcome channel or motd so all players understand the zero-reward design intent from the start.

---

## Part 17: Cycle 15 Phase 2 Patterns — Player Feedback Cross-Validation (PP15–PP20)

These patterns emerge from the Phase 2 Cycle 15 cross-validation research that searched 10 platforms for player feedback on quest line design. MC百科 (post/4382), FTB Forums, and GitHub issue trackers provided full content; Reddit and Bilibili search results were accessible but detail pages blocked. Each pattern captures a player-experience insight that was not visible in config analysis alone — things that become apparent only when players describe their frustrations, preferences, and expectations in their own words.

### PP15 — Convergence Zone Visual Consistency

**Applicable conditions:** Any chapter using diamond_convergence topology where multiple paths converge into shared nodes. The pattern addresses the visual coherence of the convergence zone itself — the cluster of quests where dependency lines from multiple branches meet.

**What players notice:** When a player opens a diamond_convergence chapter, their first impression is formed within seconds. If the convergence zone's nodes use inconsistent shapes, sizes, and dependency line styles, the player's immediate reaction is "this is chaotic" — 中文社区的原话是"连线风格要相近，不要让人的第一印象是乱"。这个判断发生在玩家理解任何具体任务内容之前，纯粹基于视觉层面的第一印象。一旦"乱"的印象形成，玩家对整个章节的导航信心会大幅下降——他们会预期这个章节很难理解，而不愿意花时间去探索。

**Pattern:** diamond_convergence 布局的核心视觉风险不是拓扑结构本身的复杂度，而是连线风格不一致导致的混乱感。汇聚区是所有章节中 dependency line 最密集的区域——多条路径的线在此交汇——如果这些节点的 shape 各不相同、size 没有梯度规律、dependency lines 有些隐藏有些显示，玩家的视觉系统无法将汇聚区解析为一个有组织的结构。相反，如果所有汇聚区节点使用统一的 shape（通常是 diamond 或 chapter default）和统一的 size 梯度（从外围到中心递增），dependency lines 使用一致的 hide_dependency_lines 策略，玩家的视觉系统能快速识别出"这是一个汇聚结构，所有路径指向中心"。

Insurgence cookbook 是最佳实践案例：其 diamond shape 占比达 75%，所有汇聚区节点在视觉上保持高度一致。这使得 diamond_convergence 布局在第一眼看来是有序的、可解析的结构，而非一团纠缠的线条和杂乱无章的节点。

**Implementation guidance:** 汇聚区的所有 quest 应使用相同的 shape（diamond 或 chapter default），避免在汇聚区内使用多个不同的 shape override。Size 应遵循从外围到中心的梯度：外围分支任务 size=1.0，中间过渡节点 size=1.25，汇聚点 size=1.5-2.0。Dependency lines 应采用统一的 hide_dependency_lines 策略——要么汇聚区内全部隐藏（当线条密度超过 AP27 阈值时），要么全部显示（当线条密度可控时）。如果汇聚区内某个节点因特殊原因需要不同的 shape，应将其放置在汇聚区的外围而非核心位置。

**Sources:** MC百科 post/4382（"连线风格要相近，不要让人的第一印象是乱"）；百度贴吧 FTB Quests 讨论帖；Insurgence cookbook（75% diamond shape，diamond_convergence 拓扑中 shape 一致性最高的案例）。
**Cross-reference:** AP27（Dependency Line Spaghetti）for the line management dimension; MP48（Shape Monoculture）for the shape consistency principle applied to convergence zones; AP25（Shape Semantic Conflict）for the consequences of inconsistent shape semantics.

---

### PP16 — Guided Non-Linearity

**Applicable conditions:** Non-expert packs where the design goal is "有引导但不线性" — players want to see a clear main progression direction while retaining the freedom to explore branching content in their preferred order. Most relevant when the pack author wants to provide structured guidance without railroading the player through a single path.

**What players notice:** FTB Forums 的玩家讨论中，理想的任务线被反复描述为"有引导但不线性"——玩家希望看到明确的主线方向（知道下一步该做什么），同时有自由选择探索哪些分支内容（不被强制走唯一的路径）。这个需求表面上矛盾——"引导"暗示线性，"不线性"暗示自由——但实际上它精确描述了 highway_branch 拓扑的核心价值：一条清晰的主干（spine）提供方向感，从主干分出的多条分支（branches）提供探索自由。

**Pattern:** highway_branch 拓扑正是"有引导但不线性"这一需求的结构化解决方案。主干节点沿一个轴排列，给玩家明确的进度方向；分支从主干节点分出，提供可选的探索内容。玩家在任何时刻都能看到"主线在哪"（沿主干方向前进），同时可以选择"现在去探索哪个分支"。但 Phase 1 数据显示了一个严重的供需失衡：highway_branch 在 non-expert 包中仅有 4 个案例（Cycle 14 新增 1 个），而 FTB Forums 和玩家反馈中大量表达了这种需求。这意味着大多数 non-expert 包的作者选择了 linear_chain（过于线性）或 hub_fan（引导感不足），没有实现玩家真正渴望的"中间态"体验。

这是一个明确的设计缺口：non-expert 包需要更多的 highway_branch 拓扑来满足玩家对"有引导但不线性"的期望。

**Implementation guidance:** 主干节点沿一个轴（通常水平）排列，间距一致（2.0 units per quest），使用 distinctive shape（gear 或 hexagon）和 size 2.0 标记为 spine milestone。从每个主干节点垂直分出 1-3 条分支，每条分支代表一个可选探索方向。分支内容应标记为 optional 或使用较小的 size（1.0-1.5）和 chapter default shape（或 circle for optional），以视觉上区别于主干的"必做"感。分支之间不应有交叉依赖——每条分支应独立完成，仅依赖主干节点。如果包有多个章节，可以在 introduction 章节使用 linear_chain 建立引导感，在主要内容章节切换到 highway_branch 提供探索自由。

**Sources:** FTB Forums 讨论帖（玩家理想任务线模型描述）；Phase 1 topology-coordinates.md（highway_branch 在 non-expert 包中的稀缺性数据）；Create-chronicles bosses_and_skill_points（non-expert 中罕见的 highway_branch 案例，extreme horizontal layout，aspect ratio 9.4:1）。
**Cross-reference:** MP46（Highway+Branch Topology）for the topology definition; MP55（Horizontal Layout Scrolling Compensation）for the navigation challenge of wide highway layouts; MP51（Diagonal Staircase）as an alternative non-linear topology with clear directional guidance.

Note: The supply-demand gap is hypothesized from limited forum feedback and the observed scarcity of highway_branch cases (4 non-expert). Further player surveys are needed to confirm whether low adoption reflects unmet demand or content-driven topology selection.

---

### PP17 — Convergence Node as Soft Gate

**Applicable conditions:** diamond_convergence and tree_branching topologies where multiple paths converge into a single node. The pattern addresses the design opportunity at convergence points — using multi-dependency quests as natural "soft gates" that require all prerequisite paths to be completed but don't enforce a specific completion order.

**What players notice:** 当多条路径汇聚到一个节点时，玩家体验到的是一种"软锁"——他们知道必须完成所有前置路径才能到达汇聚点，但可以选择以什么顺序完成这些路径。这种设计给予玩家顺序自由的同时确保了关键检查点的汇聚。与"硬锁"（`hide_until_deps_visible` 完全隐藏后续内容直到前置完成）不同，"软锁"让玩家始终能看到汇聚节点的存在和它的前置要求，这种可见性本身就是一种激励——玩家可以规划自己的推进路线，而非被系统安排唯一路径。

**Pattern:** 汇聚节点（多依赖 convergence quest）是 diamond_convergence 和 tree_branching 拓扑中天然适合放置"弱锁"设计的位置。所谓"弱锁"，是指玩家必须完成所有前置路径才能到达汇聚点（这保证了关键内容的完成），但不强制特定的完成顺序（这保留了玩家的自主性）。这在 diamond_convergence 拓扑中尤其有效——diamond 结构的多条路径本身就是并行设计，汇聚节点是它们自然收束的地方。玩家看到 diamond 结构时，能直观理解"这些路径最终汇聚在一起"，并据此规划自己的探索顺序。

弱锁的价值在于它同时满足两个看似矛盾的设计目标：确保关键检查点的内容被完成（不跳过关键步骤），以及给予玩家顺序上的自主权（不强制线性推进）。

**Implementation guidance:** 汇聚节点应设置多个 dependencies（通常 3+），使用 distinctive shape（diamond 或 octagon）和较大 size（1.5-2.0）标记为"检查点"。不要使用 `hide_until_deps_visible: true` 隐藏汇聚节点——让玩家始终看到汇聚点的存在，这样他们能规划推进路线。所有前置路径应从汇聚节点的角度看是并行的——每条路径可以独立完成，不需要在路径中间强制完成另一条路径的任务。如果想让汇聚节点成为"弱锁"但某条路径有前置条件，应将前置条件放在路径的起始处而非汇聚节点本身。

**Sources:** GitHub FTBTeam/FTB-Quests issues（dependency system design discussions）；Insurgence cookbook（diamond_convergence with multiple convergence points, each requiring 3-4 paths）；MI-Lost-Favor bronze_age（334 quests, 33% multi-dep rate, highest convergence density in dataset）。
**Cross-reference:** MP66（Extreme Fan-In Convergence）for the high-dependency variant; MP8（Fan-In Convergence）for the general convergence concept; AP37（Convergence Claustrophobia）for the risk when convergence nodes require too many prerequisites.

Override: when progression_mode is flexible and topology is diamond_convergence, AP39's functional-correctness recommendation takes priority — set hide_quest_until_deps_visible: true on the convergence quest. In linear mode, follow PP17 (keep convergence node visible).

---

### PP18 — Dependency Line Tool Quality

**Applicable conditions:** All topology selection decisions. The pattern addresses the often-overlooked constraint that FTB Quests 的依赖线渲染工具质量直接影响设计者选择哪种拓扑——工具层面的限制会传导到设计层面的决策。

**What players notice:** 玩家通常不会直接评论"依赖线工具"本身，但他们的反馈间接反映了工具限制的影响。当玩家抱怨 diamond_convergence 布局"看起来像一团乱麻"时，问题的根源往往不是 diamond_convergence 拓扑本身不好，而是当前 FTB Quests 版本的 dependency line 渲染无法优雅地处理密集的线条交汇。GitHub 上的 "Better Dependency Lines Settings" issue（Fixed in Dev）直接证实了这一点：FTB 开发团队承认当前的线条渲染有改进空间，并在新版本中进行了修复。

**Pattern:** FTB Quests 的依赖线渲染工具直接影响设计者选择哪种拓扑。当工具不能很好地处理密集依赖线时，设计者会自然地倾向于避免 diamond_convergence（线条密集，交叉多）而选择 linear_chain（线条稀疏，几乎不交叉）。这不是设计偏好，而是工具约束驱动的设计退让。这个模式提醒 AI 在生成任务时要考虑工具限制——如果目标包使用的 FTB Quests 版本较旧，dependency line 渲染能力有限，那么 diamond_convergence 的可用性会显著下降，即使它是最适合内容结构的拓扑。

FTB 团队在 "Better Dependency Lines Settings" 中修复了部分问题，说明工具在持续改进。当新版本普及后，diamond_convergence 的可用性会显著提升——但在此之前，设计者需要根据目标版本的工具能力来调整拓扑选择。

**Implementation guidance:** 在选择拓扑时，评估目标 FTB Quests 版本的 dependency line 渲染能力。如果版本较旧（不支持精细的线条控制），优先考虑 linear_chain 或 parallel_columns（线条天然稀疏），或对 diamond_convergence 使用大量 `hide_dependency_lines: true` 来管理视觉复杂度。如果版本较新（支持 "Better Dependency Lines Settings"），可以更自由地使用 diamond_convergence。无论版本如何，都应在布局规划阶段用 FTB Quests 编辑器创建一个小型 prototype（5-10 quests），测试 dependency line 的渲染效果是否满足可读性要求。

**Sources:** GitHub FTBTeam/FTB-Quests "Better Dependency Lines Settings"（Fixed in Dev）；AP27（Dependency Line Spaghetti）for the visual consequence of poor line management; Insurgence cookbook（75% diamond shape with extensive hide_dependency_lines usage, 159 instances = 80% of quests）; Craftoria Create（decorative compartment approach as alternative to line management）。
**Cross-reference:** AP27（Dependency Line Spaghetti）for the visual symptom; AP29（Dependency Line Color Blindness）for the related issue of line styling being tool-controlled; MP46（Highway+Branch Topology）as a topology that naturally avoids dense lines.

Note: The version-topology coupling is hypothesized from 1 GitHub issue ("Better Dependency Lines Settings", Fixed in Dev) and 1 Baidu Tieba player report. As FTB Quests improves line rendering, this pattern may become obsolete — further evidence is needed to confirm whether the pattern still applies to current FTB Quests versions.

---

### PP19 — Spacing Collapse After Version Update

**Applicable conditions:** All chapters using precise coordinate placement. The pattern addresses a tool-level risk that is invisible during authoring but devastating after deployment — FTB Quests 版本更新可能导致精心调整的节点间距被重新计算，破坏原有的布局意图。

**What players notice:** 百度贴吧玩家直接报告了这个问题："原来挺清楚的一滑就能看见全部任务，现在变得又挤又要"——一次 FTB Quests 版本更新后，原本清晰的节点间距变得拥挤混乱。玩家并没有改变任何配置，也没有添加新的 quest，仅仅是 mod 版本更新就导致了布局退化。这种体验特别令人沮丧，因为玩家无法理解为什么一个"看起来没问题"的章节突然变得难以使用。

**Pattern:** 版本更新导致的间距塌陷是一个工具层面的风险，但在设计层面有明确的防御策略。FTB Quests 在不同版本间可能重新解释节点的坐标系统——自动布局功能可能被重新触发、grid_scale 参数的默认值可能改变、坐标精度可能在新版本中被重新计算。对于依赖精确坐标的布局（尤其是 MP47 Compartment Region Layout 和 MP69 Dual-Grid Convergence Catalog 这种精确到 0.5 单位的布局），版本更新是一次"赌博"——更新前精心设计的布局可能在更新后面目全非。

这个问题在中文社区中尤其被关注，因为中文整合包作者经常在多个 FTB Quests 版本间迭代，每次更新都有可能触发间距变化。

**Implementation guidance:** 使用 `grid_scale` 参数锁定整体网格密度，确保版本更新不会重新计算间距。为所有节点指定精确的 x/y 坐标值（不使用自动布局或依赖默认坐标），并在每次 FTB Quests 版本更新后手动检查章节布局是否保持原样。如果发现间距塌陷，调整 `grid_scale` 值通常比逐个修改坐标更有效。对于特别重要的章节（如 introduction 或 capstone），可以在章节描述中记录 grid_scale 和布局策略，便于更新后快速恢复。

**Sources:** 百度贴吧 FTB Quests 玩家反馈（"原来挺清楚的一滑就能看见全部任务，现在变得又挤又要"）；AP24（Spacing Inconsistency）for the visual consequence of collapsed spacing.
**Cross-reference:** AP24（Spacing Inconsistency）for the symptom; topology-coordinates.md spacing formulas for the intended spacing values; AP40（Version-Induced Layout Drift）for the broader version-drift anti-pattern.

---

### PP20 — Large Chapter Repetition Fatigue

**Applicable conditions:** Chapters with more than 80 quests, particularly those using Monolithic sub-region pattern where all content is in a single undivided region. The pattern addresses the player fatigue that accumulates when a large chapter requires repeated mandatory operations in the same visual and spatial context.

**What players notice:** MC百科 post/4382 明确指出："不要让玩家在同一个地方进行多次必须的重复操作"——这是中文社区对大型章节设计最直接的玩家体验反馈。当章节超过 80 个任务且采用 Monolithic 模式时，玩家会在同一个坐标区域内反复进行类似的操作（收集、合成、提交），产生明显的疲劳感。这个反馈与 Phase 1 Cycle 15 发现的 Monolithic sub-region 模式直接对应——大型收集章节（collection catalog）最容易触发这个反模式，因为大量相似的任务被平铺在同一个视觉空间中。

**Pattern:** 大型 Monolithic 章节导致重复操作疲劳的根本原因是缺乏空间节奏变化。当 80+ 个任务都在同一个坐标区域时，玩家需要在视觉上相似的任务之间反复滚动，操作上的重复感被视觉上的单调感放大。如果任务的操作内容也相似（比如收集 50 种不同的花），疲劳感更加严重——玩家不仅在重复相同的操作类型，还在一个没有视觉变化的环境中重复。

解决方案有两个层面：在设计层面，对 Monolithic 大章节使用 `optional: true` 标记区分必做和选做内容，降低"必须重复"的操作数量；在结构层面，将大型收集章节拆分为多个小章节（每个 40-50 quests），让每个小章节有自己的视觉风格和空间节奏，使玩家在不同的环境中完成不同类型的任务。

**Implementation guidance:** 对 Monolithic 大章节（>80 quests），使用 `optional: true` 标记 30-50% 的任务为选做，减少必做重复操作的数量。如果章节是收集型（如 "collect all flowers"），考虑将收集内容按类型或稀有度拆分为 2-3 个小章节（如 "Common Flowers" / "Rare Flowers" / "Exotic Flowers"），每个小章节有自己的 chapter description 和视觉标识。对于无法拆分的大型章节，使用 decorative images（MP47）将内容分为 3-4 个视觉区域，每个区域有不同的背景色或图标，提供视觉节奏变化。在必做任务之间穿插 choice reward 或 milestone quest（size 1.5+, distinctive shape），为玩家提供阶段性的成就感。

**Sources:** MC百科 post/4382（"不要让玩家在同一个地方进行多次必须的重复操作"）；Phase 1 Cycle 15 sub-region analysis（Monolithic pattern for >80 quest chapters）；MI-Lost-Favor bronze_age（334 quests, largest single chapter in dataset, uses multiple shape types to provide visual variation within the monolithic structure）。
**Cross-reference:** AP28（Mega-Chapter Without Structural Compensation）for the structural dimension; MP47（Compartment Region Layout）for the region-based solution; MP69（Dual-Grid Convergence Catalog）for the split-alternative approach; AP37（Convergence Claustrophobia）for the convergence-endpoint variant of repetition fatigue.

Circular causality: PP20 (repetition fatigue) and AP40 (version drift) form a feedback loop. Monolithic packs with high repetition fatigue are also harder to maintain and audit, making them more likely to accumulate version drift over time. The fatigue drives authors to avoid touching the chapter, which means layout issues from version updates go uncorrected.

---

## Scope Annotation — Cycle 15 Phase 2 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| PP15 Convergence Zone Visual Consistency | ✔ (convergence zone design) | ✔ (per-node shape/size assignment) | ✔ (check shape consistency in convergence zone) |
| PP16 Guided Non-Linearity | ✔ (topology selection for non-expert) | — | ✔ (check highway_branch adoption in non-expert) |
| PP17 Convergence Node as Soft Gate | ✔ (convergence design) | ✔ (convergence node formatting) | ✔ (check parallel-path independence) |
| PP18 Dependency Line Tool Quality | ✔ (topology selection) | — | ✔ (check tool version vs topology choice) |
| PP19 Spacing Collapse After Version Update | — | — | ✔ (check grid_scale and precise coordinates) |
| PP20 Large Chapter Repetition Fatigue | ✔ (chapter sizing and splitting) | ✔ (optional marking, sub-region design) | ✔ (check >80 quest chapters for Monolithic risk) |

---

## Part 17: Cycle 16 Phase 1 Patterns — Topology Coordinates (MP70–MP71)

### MP70 — Tome-Tier Progression Map [Preliminary — Single-Source]

**Name:** Decorative Image Tier Markers for Progression Roadmap Chapters
**Applicable conditions:** Progression-map chapters that serve as a pack-wide roadmap, where each quest represents a mod or subsystem entry point. The chapter has 4+ tiers of content that benefit from visual tier separation. Most useful in non-expert vanilla+ or kitchen-sink packs with many mod-specific chapters.
**Implementation:**
- Use decorative images as tier markers: one title image (narrow, e.g. 4.0×1.0) and one background image (wide, e.g. 11.0×2.5) per tier.
- Space tiers at consistent 3.0-unit vertical intervals along the y-axis.
- Place 3-5 quests per tier row at consistent x-positions (e.g. -1.75, -0.25, 2.0).
- Multi-dependency convergence nodes appear only in later tiers (Tier 6+), requiring completion of quests from multiple earlier branches.
- Set `default_quest_shape` to "hexagon" for all tier quests, with a single "octagon" override for the endpoint capstone.
- Use 100% icon rate (every quest displays its mod's signature item) to differentiate quests visually.
**Coordinate template:**
```
Tier 1 (y=0):     (-1.75, 0), (-0.25, 0), (2.0, 0) — 3 starting branches
Tier 2 (y=3):     (-1.0, 3), (0.5, 3), (2.0, 3) — 3 intermediate nodes
...
Tier N (y=3*(N-1)): convergence nodes with 2+ deps
Endpoint (y=3*N): (0.5, 3*N) octagon, size 2.5 — capstone
Decorative images: title at (0.5, y-1.5), background at (0.5, y-0.5) per tier
```
**Sources:** Chroma Endless progression_tree_2 (Case 43, 32 quests, 8 tiers with tome images). This pattern has only been observed in one pack; it may be specific to packs where the author wants a visual "table of contents" for the entire modpack.
**Cross-reference:** topology-coordinates.md Case 43; MP47 (Compartment Region Layout) for the decorative image approach at larger scale.

**Phase 2 Cycle 16 player validation:** NOT validated. Searched MC百科 (Chroma Endless modpack/702 page — no player comments on layout), Bilibili (only a Chinese localization announcement, no gameplay videos showing the progression tree), Reddit, CurseForge, and GitHub FTB issues. No player or 攻略 mentions the tome-tier visual markers or describes using decorative images to understand progression tiers. The pattern remains config-only evidence derived from a single pack. Chroma Endless is a niche pack with minimal community discussion, which limits the validation signal — absence of feedback does not mean the pattern is ineffective, only that it hasn't been discussed publicly. The decorative-image-as-tier-marker concept is consistent with MP47 (Compartment Region Layout) at a smaller scale, which IS validated by Craftoria's well-received Create chapter. Authors using MP70 should consider adding text labels (quest descriptions or chapter descriptions) to supplement the visual tier markers, since players may not interpret the tome images as tier indicators without explicit context.

---

### MP71 — Shape-as-Category-Marker [Validated — Multi-Source, Cycle 17]

**Name:** Shape Used as Quest Category Label Rather Than Topology Signal
**Applicable conditions:** Chapters where a specific shape is applied to all quests of a certain type (e.g., all structure-discovery quests, all boss-kill quests) regardless of their position in the dependency graph. Most useful in adventure/RPG packs with mixed task types (structure, advancement, item).
**Implementation:**
- Apply a distinctive shape (typically "diamond" or "pentagon") to all quests of a specific category.
- The shape does NOT indicate convergence topology — it serves as a visual category marker.
- Category quests may have zero dependencies (independent collection items) or form linear chains.
- Use the default shape for non-category quests (standard progression items).
- Ensure the shape semantic is consistent: one shape per category throughout the chapter.
**When to use diamond as category vs convergence:**
- Diamond = convergence: quests have fan_in >= 2 (multiple dependency paths merge at this node)
- Diamond = category: quests are independent or have fan_in <= 1 (no convergence, just a label)
- Check: if diamond-shaped quests have multi-dep → convergence topology. If single/no dep → category marker.
**Sources:** MC-Odyssey-3 exploration (Case 45, 35 quests, 12 diamond shapes for structure-discovery tasks with zero multi-dep). This is the first confirmed case where diamond shape serves as a category label rather than a convergence signal. The pattern may be more common in adventure packs where structure-discovery is a primary mechanic.
**Cross-reference:** topology-coordinates.md Case 45; MP48 (Shape Monoculture) for the alternative of using shape for chapter-level identity; Phase 2 topology classifier convergence_ratio threshold.

**Cycle 17 Phase 1 multi-source validation:** VALIDATED by config-level evidence from 2 independent packs. (1) MC-Odyssey-3 exploration (Case 45, original source): 12 diamond shapes for structure-discovery tasks with zero multi-dep. (2) Steamcreate2 overworld (Mixed Topology 1, Cycle 17): 4-shape category system used consistently across 4 independent sub-regions with 85+ quests — square (size 1.2, map icon) = structure discovery / "find this location"; diamond (default size) = dungeon entry / "enter this structure"; hexagon (size 1.5) = boss kill / "defeat this boss"; circle (size 1.0-1.1) = regular mob kill / "farm this mob." This is the strongest config-level validation of MP71: the shape semantics persist across 4 spatially separated sub-regions, each with 8-12 quests, demonstrating that shape-as-category is a deliberate design system rather than coincidental shape assignment. No shape-marked quest has multi-dependency, confirming the shapes serve as category labels rather than convergence signals. Additionally, the No-Flesh-Within-Chest pack (Cases 49-51) uses rsquare consistently for milestone quests across 3 different chapters (58+50+46 quests), suggesting that rsquare-as-milestone-marker is another instance of shape-as-category in a Chinese adventure RPG pack. Player feedback validation remains absent — no player comments discussing shape semantics have been found for either pack. The config evidence is strong enough to move MP71 from Preliminary to Validated status, but authors should still provide an explicit legend or chapter description explaining the shape vocabulary, as the FTB team's proposed "Quests Legend" feature (FTBTeam/FTB-Mods-Issues #1447) would make shape-as-category patterns self-documenting.

---

## Part 18: Cycle 17 Phase 1 Patterns — Topology Coordinates (MP72–MP73)

### MP72 — Tree-with-Capstone Convergence

**Name:** Single Massive Convergence Node as Mod-Completion Trophy
**Applicable conditions:** Large mod-specific chapters (50+ quests) in non-expert kitchen-sink packs, where the chapter covers an entire mod's progression from entry to mastery. The capstone serves as a "you've completed this mod" achievement gate. Most useful when the mod has a clear endgame milestone (e.g., Create's completion trophy, Botania's Gaia Spirit).
**Implementation:**
- Design the first N-1 quests as a tree_branching layout with 2-6 sub-regions (per mod subsystem).
- The final quest (capstone) is placed below or to the right of all other quests, with a distinctive shape (gear or hexagon) and size 3.0-4.0 (the largest in the chapter).
- The capstone quest has dependencies on ALL prior quests (fan_in = N-1), creating an absolute completion gate.
- Use a trophy item as the capstone icon (e.g., trofers:medium_pillar, a mod-specific achievement item).
- The capstone's task type is typically checkmark (acknowledgment rather than item submission).
- Position the capstone at the visual terminus of the chapter: below the main tree in vertical layouts, to the right in horizontal layouts.
**Coordinate template:**
```
Main tree: x=[-6..18], y=[-3..9] (68 quests, single-dep tree)
Capstone:  (6.0, -6.0) gear shape, size 4.0, deps on ALL 68 quests, trofers icon
```
**Sources:** AOF-6 Create (Case 52, 69 quests, gear capstone at size 4.0 with 68 deps) and AOF-6 Botania (Case 53, 100+ quests, hexagon capstone at size 4.0 with ALL deps). Both chapters are by TeamAOF, suggesting this may be a TeamAOF design signature. The capstone pattern has been observed in 2 chapters of the same pack; it may be specific to kitchen-sink packs where each mod chapter needs a clear "done" signal.
**Cross-reference:** topology-coordinates.md Cases 52, 53; MP57 (Convergence Capstone) for the general convergence design; MP71 (Shape-as-Category) for the shape distinction between capstone and tree nodes.

**Phase 2 Cycle 17 player validation:** [Needs-Validation] — Searched MC百科 (AOF-6 modpack/548 — "1000+ 的任务!" but no quest-structure-specific player comments), Reddit r/feedthebeast (AOF-6 threads blocked by anti-bot), GitHub FTBTeam issues, and 脆骨症/TeamAOF community channels. No direct player feedback about convergence capstones was found — no player has explicitly praised or complained about a "must complete ALL quests" chapter ending. The closest indirect signal comes from Craftoria #231 where a player complained the Powah chapter "throws everything at you" and requested restructuring to be more linear — this suggests that when large chapters lack clear structure, players feel overwhelmed, but it doesn't specifically address the capstone convergence moment. AP37 (Convergence Claustrophobia) predicts that a 68-dep or 100-dep capstone creates severe bookkeeping burden unless the capstone quest's own task is a simple checkmark (which both AOF-6 cases use), so the checkmark-task design choice may be TeamAOF's implicit mitigation of AP37. The pattern remains config-only evidence from a single authoring team. Authors using MP72 should ensure the capstone's task is checkmark-type (not item submission) to avoid convergence claustrophobia, and should add a description listing what the capstone represents as a mod-completion milestone. Validation requires player feedback from at least 2 independent packs (not TeamAOF) to graduate from Needs-Validation.

---

### MP73 — Sub-Region Decomposition for Large Chapters

**Name:** 4-6 Spatially Separated Sub-Regions for Chapters with 80+ Quests
**Applicable conditions:** Large chapters (80+ quests) covering multiple mods or subsystems. The pattern prevents mega-chapter fatigue (PP20) by decomposing content into 4-6 spatially distinct zones, each with its own internal topology. Most useful in kitchen-sink packs where a single chapter covers an entire mod ecosystem.
**Implementation:**
- Decompose the chapter into 4-6 sub-regions, each covering one mod or subsystem.
- Each sub-region occupies its own x-y band (4-8 units of separation between regions).
- Each sub-region has its own hub quest (advancement or checkmark type) that gates access to leaf quests.
- The internal topology within each sub-region matches the subsystem's natural structure:
  - Processing chains → linear_chain within the sub-region
  - Collection catalogs → grid_catalog within the sub-region
  - Variant items → hub_fan within the sub-region
- Transitions between sub-regions use dependency chains (not bridge nodes or coordinate connectors).
- Use shape-as-category (MP71) consistently across sub-regions when the chapter has mixed task types.
**Coordinate template:**
```
Sub-region A: x=[-13..-7], y=[7..12], grid_catalog (cacao/chocolate)
Sub-region B: x=[-10..-3], y=[14..19], linear_chain (Farmer's Delight)
Sub-region C: x=[-8..-3], y=[2..8], hub_fan (vanilla farming)
Sub-region D: x=[1..7], y=[14..20], hub_fan (Vinery wines)
Sub-region E: x=[7..10], y=[9..16], convergence nodes (Croptopia)
```
**Sources:** AOF-6 Agriculture (Case 54, 90+ quests, 6 sub-regions), AOF-6 Botania (Case 53, 100+ quests, 6 sub-regions), Steamcreate2 overworld (Mixed Topology 1, 85+ quests, 4 zones). The consistent 4-6 sub-region count across 3 independent large chapters suggests a cognitive decomposition limit — authors naturally break large content into approximately 5 (±1) regions, matching Miller's working memory capacity.
**Cross-reference:** topology-coordinates.md Mixed Topology Analysis (Cycle 17); PP20 (Large Chapter Repetition Fatigue) for the anti-pattern this decomposition prevents; MP47 (Compartment Region Layout) for the decorative-image variant of sub-region marking.

**Phase 2 Cycle 17 player validation:** [Indirectly-Validated] — No player has explicitly praised sub-region decomposition as such (players don't typically comment on spatial layout taxonomy), but strong indirect evidence from the anti-pattern side confirms the need. (1) MC百科 post/2494, the most detailed Chinese FTB Quests tutorial, explicitly warns that poor quest book layout causes players' "血压升高" (blood pressure to rise) and recommends that "直线形的章节排版各任务之间的连线最好要遵循长度相等、对称等原则" (linear chapter connection lines should follow equal-length and symmetry principles) — this implies that organized, spatially structured layouts are a recognized player need. (2) Craftoria #231 (TeamAOF/Craftoria) player complaint: the Powah chapter "kinda just throws everything at you" and the player proposed restructuring to create a more guided, linear path — this is exactly the problem MP73 prevents: when a large chapter lacks sub-region decomposition, it presents as a monolithic wall of content. (3) PP20 (Large Chapter Repetition Fatigue) documents that >80 quest monolithic chapters cause "不要让玩家在同一个地方进行多次必须的重复操作" (don't make players repeat mandatory operations in the same place). (4) AP28 (Mega-Chapter Without Structural Compensation) explicitly identifies 150+ quest chapters without structural compensation as an anti-pattern. The convergence of 4 independent anti-pattern sources (post/2494, Craftoria #231, PP20, AP28) all pointing to the same problem that MP73 solves provides strong indirect validation. The 4-6 sub-region count matches Miller's "7±2" working memory model, which is a well-established cognitive science principle. Direct player praise for sub-region layout is unlikely (players notice problems, not solutions), so indirect validation from the anti-pattern side is the strongest achievable signal for this pattern type.

---

## Scope Annotation — Cycle 17 Phase 1 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP72 Tree-with-Capstone Convergence | ✔ (chapter structure: tree + capstone) | ✔ (capstone shape/size/icon assignment) | ✔ (check capstone dep count matches quest count - 1) |
| MP73 Sub-Region Decomposition | ✔ (chapter sizing, sub-region planning) | ✔ (per-region topology assignment) | ✔ (check 4-6 region count for >80 quest chapters) |

---

## Part 19: Cycle 18 Phase 1 Patterns — Custom Shapes and Dependency Management (MP74–MP75)

### MP74 — Custom Shape Texture Registration [Preliminary — Single-Source, Cycle 18]

**Name:** Pack-Defined Shape Vocabulary via KubeJS Asset Override
**Applicable conditions:** Packs that need more than the 8 standard FTB Quests shapes (circle, square, diamond, hexagon, pentagon, gear, octagon, rsquare) to express their content taxonomy. Most useful when the pack has a strong visual identity (custom resource pack) and wants quest shapes to match the pack's aesthetic.
**Implementation:**
- Create shape texture directories under `kubejs/assets/ftbquests/textures/shapes/{custom_name}/` with three PNG files: `shape.png` (filled shape), `outline.png` (border), `background.png` (background fill).
- Register the custom shape by setting `default_quest_shape: "{custom_name}"` at the chapter or data level.
- Use custom shapes consistently throughout the pack — once defined, the custom shape becomes available for all chapters.
- Custom shapes follow the same override hierarchy as standard shapes: quest-level > chapter-level > data-level.
- Recommended: limit custom shapes to 2-3 per pack to avoid visual overload. Each custom shape should have a clear semantic (e.g., tech_circle = technology milestones, magic_diamond = magic tiers).
**Sources:** Endless-Rise-Remastered (Case 60, `default_quest_shape: "tech_square"`, 3 custom shapes: tech_circle, tech_square, tech_smooth_square). This is the first pack in the 62-pack dataset to define custom shape textures with custom names. The pack's shape system is fully self-contained in `kubejs/assets/ftbquests/textures/shapes/` — the standard FTB Quests shapes remain available but are rarely used. FTB dev desht confirmed in FTBTeam/FTB-Mods-Issues #1303 that the shape system is "a hierarchical system — file defaults, which are overridden by chapter defaults, which are overridden by quest settings," implying custom shapes slot into this hierarchy seamlessly.
**Cross-reference:** topology-coordinates.md Case 60; MP48 (Shape Monoculture) for the decision to use few shapes; Phase 2 topology classifier — custom shapes are classified as their string name, not mapped to standard shape semantics.

> **Generality note:** Custom shapes are a powerful but rarely needed feature. Only 1 of 62 packs in the dataset uses them. The standard 8 shapes cover the vast majority of pack design needs. Authors should only define custom shapes when the pack's visual identity demands it (e.g., a pack with custom UI textures throughout) or when the standard shapes don't convey the needed category distinction. The technical capability exists and is well-documented; the design question is whether the pack needs it.

---

### MP75 — Extreme Dependency Line Suppression for Collection Chapters [Preliminary — Single-Source, Cycle 18]

**Name:** >80% hide_dependency_lines Rate in Large Collection-Catalog Chapters
**Applicable conditions:** Large collection-catalog chapters (100+ quests) where the dependency graph is dense (many quests with 2+ dependencies) but the visual dependency lines would create overwhelming visual noise. Most relevant for Mystical Agriculture, Croptopia, or other collection-heavy mod chapters where many items converge into tier milestones.
**Implementation:**
- Set `hide_dependency_lines: true` on 80%+ of quests in the chapter.
- Keep dependency lines visible ONLY on convergence nodes (quests with 3+ dependencies) and the chapter's root/spine quests — this preserves navigability for the critical structural connections while eliminating noise from the hundreds of collection-item connections.
- Pair with shape monoculture (MP48) to reduce visual complexity further — all collection items use the default shape, only milestones get shape overrides.
- Consider using `hide_quest_until_deps_visible: true` on convergence nodes so the player doesn't see the tier capstone until they've completed enough prerequisites.
- For 100–150 quest collection chapters, consider hiding 70–90% of dependency lines. Start at 70% and increase if the dependency graph appears cluttered. No empirical data exists for 150+ quest chapters — extrapolation beyond 100 quests should be treated as speculative. The only measured data point is umodpack mystical_agriculture (130 quests, 86.2% suppression rate); the previous scaling formula (60–70% for 80–100 quests, 80–90% for 100–150 quests, 90%+ for 150+ quests) was extrapolated from this single observation and has no independent validation.
**Coordinate template:**
```
All collection items: hide_dependency_lines: true, shape: default, size: 1.0
Tier milestones (every 10-15 items): hide_dependency_lines: false, shape: octagon, size: 1.25-1.5
Chapter capstone: hide_dependency_lines: false, shape: gear, size: 2.0, 5-7 dependencies
```
**Sources:** umodpack mystical_agriculture (Case 61, 130 quests, 112 hide_dependency_lines = 86.2% suppression rate, max 7 deps on single convergence node, ZERO rewards). This is the highest hide_dep_lines proportion in the dataset for a >100 quest chapter. The suppression is deliberate: the author hides all collection-item dependency lines while keeping the tier milestone connections visible. Insurgence cookbook (159 instances, 80% of 199 quests) was the previous record holder; umodpack exceeds it by 6 percentage points.
**Cross-reference:** topology-coordinates.md Case 61; AP27 (Dependency Line Spaghetti) for the visual problem this pattern prevents; MP48 (Shape Monoculture) for the complementary visual simplification; PP18 (Dependency Line Tool Quality) for the tool-level constraint that motivates aggressive line suppression.

---

### MP76 — Textural Shape Naming System [Validated-by-Absence — Multi-Pack/Single-Org, Cycle 19]

**Name:** Pack-Defined Shape Textures via Aesthetic/Textural Prefixes
**Applicable conditions:** Packs that want each mod chapter to have a visually distinct shape texture (not just a different shape, but a different visual rendering style for the shape outline). Most useful for packs with strong per-mod visual identity where the shape's visual texture reinforces the mod's aesthetic (e.g., a "crumpled" look for industrial mods, a "torn" look for worn/weathered content).
**Implementation:**
- Define custom shape textures under `kubejs/assets/ftbquests/textures/shapes/{prefix}_{base_shape}/` with shape.png, outline.png, and background.png files.
- Use aesthetic/textural prefixes (default_, crumpled_, torn_, ragged_) rather than functional prefixes (tech_, magic_) to describe the visual rendering style rather than the content category.
- Set `default_quest_shape: "{prefix}_{base_shape}"` at the chapter level to establish the mod's visual identity.
- Each mod chapter gets a different prefix, creating visual variety through texture rather than through geometric shape alone.
- Recommended: limit to 3-4 prefixes per pack. Each prefix should have all 8 base shapes available (circle, square, diamond, hexagon, pentagon, gear, octagon, rsquare) for consistency.
**Sources:** Gloomy-Rise (Cases 64-65, BMProjects-Development — same org as Endless-Rise-Remastered). Gloomy-Rise uses four texture prefixes: default_rsquare (Create chapter, 11 uses), crumpled_rsquare (IE chapter, 19 uses), ragged_rsquare (hightech chapter, 4 uses), torn_rsquare (gloomy_rise main, 1 use). Each prefix renders the same geometric shape (rsquare) with a different visual texture. This is a fundamentally different naming philosophy from ERR's functional prefixes (tech_circle, tech_square): ERR categorizes by content type, Gloomy-Rise categorizes by visual feel. The two-source evidence (ERR + Gloomy-Rise, same organization) suggests this is a deliberate design capability, not an accident.
**Cross-reference:** topology-coordinates.md Cases 60, 64, 65; MP74 (Custom Shape Texture Registration) for the underlying technical mechanism; MP48 (Shape Monoculture) for why most packs don't need this.

> **Generality note:** Textural shape naming is an extremely advanced technique used by only 1 organization (BMProjects-Development) across 2 packs. The standard 8 shapes with standard textures cover virtually all pack design needs. Authors should only consider textural prefixes when they have custom shape textures AND want per-mod visual variety beyond what geometric shape alone provides.

> **Edge case notes:**
> - **Incomplete shape sets:** The recommendation to provide all 8 base shapes per prefix assumes the author wants full shape variety within each mod chapter. If a prefix only defines 2-3 base shapes (e.g., crumpled_rsquare and crumpled_hexagon only), quests using other shapes within that chapter will fall back to the default texture — potentially creating visual inconsistency where some quests look "crumpled" and others look standard. Recommendation: if a prefix defines fewer than 4 base shapes, add a chapter-level note in the quest description or a decorative image clarifying the intended shape subset.
> - **Mixing textural and functional prefixes:** No pack in the dataset mixes textural prefixes (crumpled_, torn_) and functional prefixes (tech_, magic_) within the same pack. While technically feasible, mixing naming philosophies may confuse players about whether the prefix signals visual style or content category. If mixing is desired, document the distinction explicitly in the pack's first-chapter tutorial quest.
> - **Missing texture fallback:** If the texture file for a specific prefix+shape combination is missing from the asset directory, FTB Quests behavior is undefined (may render as blank, default, or error texture). Always verify that every prefix+shape combination referenced in quest configs has a complete set of shape.png, outline.png, and background.png files.

---

### MP77 — Sub-1.0 Size Compression for High-Density Chapters [Partially-Validated — Multi-Source, Cycle 19]

**Name:** Using size values below 1.0 to increase quest density per viewport unit
**Applicable conditions:** Large chapters (150+ quests) where the standard 1.0 size creates excessive viewport area, forcing players to scroll extensively. Most relevant for hub_fan, grid_catalog, and dense tree_branching chapters where quests cluster tightly.
**Implementation:**
- Set quest `size: 0.6d` to `size: 0.8d` for standard chain nodes in large chapters.
- Reserve `size: 1.0d` for sub-hubs and `size: 1.2d` to `size: 1.5d` for milestones.
- At 0.6-0.7 size, quests become visually compact but still clickable and readable. Below 0.5, quests become nearly invisible (MC-Eternal-Eternally uses 0.1 for hidden infrastructure — do not use this for player-facing quests).
- Pair with tight coordinate spacing (0.5-1.0 unit intervals) to create dense grid layouts.
- For chapters with 300+ quests, consider 0.5-0.6 sizing for leaf nodes and 0.8-1.0 for structural nodes.
- Test at actual viewport zoom: the player should be able to see 20-30 quests on screen without zooming out excessively.

**Edge case notes:**
- **The 0.5 boundary clarification:** The "sweet spot" (0.5-0.7) and the "infrastructure-only" zone (<0.5) overlap at exactly 0.5. Practical guidance: use 0.5 only for quests that are visible but peripheral to the main progression (side-content leaf nodes). Use 0.6-0.7 for all player-facing standard chain nodes. Reserve 0.1-0.4 strictly for hidden infrastructure (decorative markers, trigger quests). MCEE's 0.5 usage on 10 quests in the introduction chapter confirms 0.5 is viable for peripheral content.
- **Resolution and accessibility:** Sub-1.0 sizing was observed on desktop displays at standard resolution. On lower-resolution screens (720p, small laptop displays) or for players with visual impairments, quests at 0.5-0.6 size may become difficult to click or read. The clickability test ("still clickable and readable") should be validated at the lowest resolution the pack targets. Consider adding a note in the pack's first-chapter tutorial about minimum recommended screen resolution.
- **Mixed-size dependency lines:** When a 0.6-size quest depends on a 1.5-size milestone, the dependency line may render awkwardly (connecting a tiny node to a large node). Test dependency line rendering at mixed sizes — if lines become visually confusing, consider hiding dependency lines (`hide_dep_lines: true`) for the smaller quest and relying on the quest description to indicate the dependency.
**Sources:** Gloomy-Rise create (Case 64, 171 quests at 0.8 size, density 1.17 quests/sq-unit), MC-Eternal-Eternally introduction (Case 68, 678 quests at 0.5-0.7 size, density 3.14 quests/sq-unit — DENSEST hub_fan in dataset), MC-Eternal-Eternally bosses (Case 69, 224 quests at 0.8 size), MC-Eternal-Eternally irons_spells (Case 70, 630 quests at 0.1-1.0 size). The pattern spans 4 chapters across 2 packs, with densities ranging from 1.17 to 3.14 quests/sq-unit. The 0.5-0.7 range is the sweet spot for player-facing quests; 0.1-0.3 is infrastructure-only.
**Cross-reference:** topology-coordinates.md Cases 64, 68, 69, 70; R59 (Bounding Box Viewport Fit) for the viewport constraint that motivates compression; MP73 (Sub-Region Decomposition) for the complementary approach of splitting rather than compressing.

---

## Cycle 18 Phase 1 — MP72 Validation Update

**MP72 (Tree-with-Capstone Convergence)** remains **[Needs-Validation — TeamAOF-only]** after Cycle 18 Phase 1. Searched 8 new packs (GhostLand8, umodpack, create-advanced-industries, Endless-Rise-Remastered, generic-botania-pack, Engineers-Life-2, IncrementalIndustries, Wolds-Vaults) and found NO non-TeamAOF instance of the tree-with-capstone pattern (a single quest with dependencies on ALL prior quests in a tree_branching chapter, using a distinctive shape at size 3.0-4.0 as a mod-completion trophy). The closest pattern found was generic-botania-pack's endgame chain (size 4.5 gear → size 5.0 rsquare), but this is a linear_chain endgame (2 quests), not a tree-with-capstone convergence (N quests → 1 capstone). GhostLand8 create (206 quests) has no capstone quest — the chapter simply ends with the last quest in the dependency chain. Engineers-Life-2 becoming_an_engineer (132 quests) has max 2 dependencies, far below the N-1 threshold. The pattern remains config-only evidence from TeamAOF's AOF-6 Create and Botania chapters. Authors using MP72 should treat it as a TeamAOF design signature until cross-validated by at least 2 independent packs.

---

## Scope Annotation — Cycle 18 Phase 1 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP74 Custom Shape Texture | ✔ (visual identity decision) | ✔ (shape texture directory setup) | ✔ (verify custom shape names match texture files) |
| MP75 Extreme Dep Line Suppression | ✔ (chapter sizing, collection design) | ✔ (per-quest hide_dep_lines flag) | ✔ (check suppression rate vs quest count) |

---

## Scope Annotation — Cycle 19 Phase 1 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP76 Textural Shape Naming | ✔ (visual identity decision, texture prefix philosophy) | ✔ (shape texture directory setup, prefix naming) | ✔ (verify texture prefixes match asset files) |
| MP77 Sub-1.0 Size Compression | ✔ (chapter density planning, viewport management) | ✔ (per-quest size value setting) | ✔ (test at actual viewport zoom, verify clickability) |

---

## Phase 2 Cycle 18 — MP74/MP75/MP72 Cross-Platform Validation

### MP74 (Custom Shape Texture Registration) — Validation Update: [Preliminary → Validated-by-Absence]

Phase 2 Cycle 18 searched 5 Chinese tutorials covering FTB Quests visual customization (MC百科 post/2494, post/5450, post/5137, post/3823, post/5840), plus CurseForge, Reddit r/feedthebeast, and Bilibili. None of these sources mention custom shape textures via `kubejs/assets/ftbquests/textures/shapes/` or pack-defined shape names. The tutorials extensively cover custom images (decorative PNGs in quest panels), theme file customization (background textures, border colors), and the 8 standard shapes ("默认是圆形的，有各种形状可选" — default is circular, various shapes available), but the technique of defining entirely new shape categories with custom names remains undocumented in community resources.

This negative evidence strongly confirms MP74's characterization as an extremely rare capability. The fact that 5 independent Chinese tutorials, each covering different aspects of FTB Quests visual customization, all omit custom shape textures suggests the feature is not merely underused — it is outside the community's awareness. Endless-Rise-Remastered's use of custom shapes (tech_circle, tech_square, tech_smooth_square) is genuinely innovative within the documented ecosystem. The validation status upgrades from [Preliminary — Single-Source] to [Validated-by-Absence]: the pattern is real, the technical mechanism is confirmed by FTB dev desht (FTBTeam/FTB-Mods-Issues #1303), and its extreme rarity is confirmed by the total absence of community documentation.

### MP75 (Extreme Dependency Line Suppression) — Validation Update: [Preliminary → Partially-Validated]

MC百科 post/2494, the most cited Chinese FTB Quests layout tutorial, explicitly recommends hiding dependency lines as a deliberate author technique for managing visual complexity. The tutorial documents the feature as "隐藏前置连线：默认为 default ，为 true 时会隐藏该任务与其前置任务之间的连线" (hide prerequisite connection lines: default is default, when true hides the connection between the quest and its prerequisites). For stream-of-consciousness (意识流) layouts, the author advises: "如果你的排版比较意识流，那么建议你先有个大致的想法再实操，很多情况下你也是得去除任务连线的" (if your layout is abstract/stream-of-consciousness, plan ahead first — in many cases you'll need to remove quest connection lines). The tutorial also provides a pragmatic escape hatch: "如果你想去掉部分情况下显得丑丑的任务连线，可以把选定任务的任务连线显示关闭" (if you want to remove ugly connection lines in some cases, you can turn off the selected quest's connection line display).

MC百科 post/5840 (1.12.2 detailed tutorial) confirms the same feature under the name "隐藏相关性行" (hide correlation lines), describing it as a tool to "隐藏任务引导线" (hide quest guide lines). The existence of this feature in two independent tutorials confirms that hiding dependency lines is a recognized and documented author technique in the Chinese community.

This partially validates MP75: the underlying mechanism (hide_dependency_lines) is confirmed as a deliberate design tool, not a hidden or accidental feature. However, the tutorials recommend hiding lines for aesthetic reasons (丑丑的 = ugly) rather than for the specific collection-chapter use case MP75 describes (>80% suppression in large collection-catalog chapters). The 86.2% suppression rate observed in umodpack's mystical_agriculture chapter remains a single-source extreme; no community tutorial recommends suppression rates above 50%. The pattern is validated at the mechanism level but the extreme-suppression threshold (>80%) remains single-source evidence.

### MP72 (Tree-with-Capstone Convergence) — Validation Update: Still [Needs-Validation — TeamAOF-only]

Phase 2 searched all available platforms (MC百科, Bilibili, Reddit, CurseForge, NGA, 知乎, MineBBS, 百度贴吧) for any mention of a tree-with-capstone pattern (a single final quest with dependencies on ALL prior quests in a tree_branching chapter, using a distinctive shape at size 3.0-4.0 as a mod-completion trophy). Zero non-TeamAOF instances were found. No tutorial, forum post, or player comment describes this pattern outside TeamAOF packs. The MC百科 post/2494 tutorial discusses spiral layouts, linear layouts, and stream-of-consciousness layouts, but never mentions a convergence-to-single-capstone design. The pattern remains config-only evidence from AOF-6 Create and Botania chapters, and should be treated as a TeamAOF design signature until at least 2 independent non-TeamAOF packs are found using it.

### Phase 3 Cycle 18 — MP72 Formal Reclassification: [Needs-Validation → TeamAOF-Specific]

After 3 cycles of exhaustive searching (Cycles 16, 17, and 18), MP72 (Tree-with-Capstone Convergence) is formally reclassified from **[Needs-Validation — TeamAOF-only]** to **[TeamAOF-Specific]**. The accumulated negative evidence is now conclusive:

- **Cycle 16**: Searched initial pack dataset, found zero non-TeamAOF instances.
- **Cycle 17**: Expanded search to 8 additional packs (GhostLand8, umodpack, create-advanced-industries, Endless-Rise-Remastered, generic-botania-pack, Engineers-Life-2, IncrementalIndustries, Wolds-Vaults). Zero non-TeamAOF instances. The closest pattern was generic-botania-pack's linear_chain endgame (size 4.5 → 5.0), not a convergence capstone.
- **Cycle 18 Phase 2**: Searched 10 platforms (MC百科, Bilibili, Reddit, CurseForge, GitHub FTBTeam, NGA, 知乎, MineBBS, 百度贴吧, FTB Docs). Zero non-TeamAOF mentions of the pattern in any tutorial, forum post, or player comment.
- **Cycle 18 Phase 3**: Searched 9 platforms with author-design-philosophy focus (Bilibili, MC百科, Reddit, klpbbs.com, CSDN, GitHub FTBTeam, mczfw.com, 知乎, MineBBS). Found Nova Engineering (narrative research system), Engineer's Life 2 (open-gating), and Vazkii's design philosophy (dimensional progression), but zero non-TeamAOF instances of tree-with-capstone convergence.

The MC百科 post/2494 tutorial — the most comprehensive Chinese-language quest layout guide — covers linear, spiral, and stream-of-consciousness layouts but never mentions convergence-to-single-capstone design. The MC百科 post/4382 article discusses weak locks, era architecture, and task branch visual styles but never describes a capstone convergence pattern. After searching 20+ packs across 10+ platforms over 3 cycles with zero non-TeamAOF evidence, the pattern should be documented as a TeamAOF design signature rather than a general modpack pattern. Authors using MP72 should note that it is a TeamAOF-specific technique validated only within that team's packs (AOF-6 Create and Botania chapters).

---

## Phase 2 Cycle 19 — MP76/MP77 Cross-Platform Validation

### MP76 (Textural Shape Naming System) — Validation Update: [Preliminary — Multi-Pack/Single-Org → Validated-by-Absence]

Phase 2 Cycle 19 searched MC百科 (post/2494, post/5450, post/5137, post/3823, post/5840), Bilibili FTB Quests tutorials (BV1y7411J7rj, BV466754224), CSDN FTB Quests articles, mczfw.com quest design tutorials, GitHub FTBTeam/FTB-Mods-Issues, Reddit r/feedthebeast, CurseForge pack comments, and the FTB official documentation (docs.feed-the-beast.com). None of these sources mention custom shape textures via aesthetic/textural prefixes (crumpled_, torn_, ragged_) or pack-defined shape texture categories. The MC百科 post/2494 tutorial — the most cited Chinese quest layout guide — covers linear, spiral, and stream-of-consciousness layouts, custom images (decorative PNGs in quest panels), and the 8 standard shapes, but never discusses custom shape texture directories or naming conventions. The post/5450 tutorial covers 1.20.1+ custom image insertion but treats images as decorative panel content, not as shape texture overrides.

This negative evidence strongly confirms MP76's characterization as an extremely rare, possibly organization-specific capability. The fact that 5+ independent Chinese tutorials, the official FTB documentation, and extensive Reddit/CurseForge discussions all omit textural shape naming suggests the feature is not merely underused — it exists outside the community's awareness entirely. Gloomy-Rise's use of textural prefixes (crumpled_rsquare, torn_rsquare, ragged_rsquare) combined with Endless-Rise-Remastered's functional prefixes (tech_circle, tech_square) from the same organization (BMProjects-Development) represents a deliberate design philosophy that has no documented parallel in the broader modpack community. The validation status upgrades from [Preliminary — Multi-Pack/Single-Org] to [Validated-by-Absence]: the pattern is real, the technical mechanism is confirmed by MP74 (which itself is validated-by-absence), and its extreme rarity is confirmed by the total absence of community documentation across 4 cycles of cumulative searching (MP74 + MP76 lineage).

### MP77 (Sub-1.0 Size Compression for High-Density Chapters) — Validation Update: [Preliminary — Multi-Source → Partially-Validated]

The MC百科 post/2494 tutorial confirms that quest size ("大小") is a recognized configurable parameter: "大小：任务框的大小，默认为 1 ，为倍数关系" (size: the quest frame's dimensions, default is 1, in multiplier relationship). This confirms the technical mechanism — size is a documented, community-known setting. However, the tutorial does NOT discuss using sizes below 1.0 as a deliberate design technique. The tutorial focuses on layout strategies (linear, spiral, stream-of-consciousness) and visual organization (hiding dependency lines, custom images) rather than size manipulation for density control.

No player complaints about "nodes too small" (节点太小) or "too dense" (太密) were found specific to the studied packs (Gloomy-Rise, MC-Eternal-Eternally). The MC百科 post/2494 tutorial does warn that "如果你没有好好排版，那么也许玩家会血压升高" (if you don't lay out properly, players may get frustrated), but this is a general layout quality warning, not specific to size compression. The FTBTeam/FTB-Mods-Issues #1909 feature request mentions that pinned quest lists "can get pretty big and that then takes over most of the screen" — an indirect validation that screen space management is a real concern in large quest books, which is precisely the problem MP77 solves through size compression.

The pattern is validated at the mechanism level (size is a known, configurable parameter) and at the problem level (screen space management is a recognized concern). However, the specific technique of using 0.5-0.7 sizing for high-density chapters remains config-only evidence from 4 chapters across 2 packs. No community tutorial recommends sub-1.0 sizing, and no player feedback confirms or denies the navigability of compressed chapters. Authors using MP77 should note that the technique is empirically observed but not community-validated — test with actual players before deploying in production packs.

---

## Cycle 20 Phase 1 — New Micro-Patterns

### MP78 — Quest Links as Cross-Chapter Bridge Nodes [Preliminary — Single-Pack/Expert, Cycle 20]

**Name:** Using FTB Quests `quest_links` to create structural bridges between a backbone highway and parallel mod-content branches
**Applicable conditions:** Expert packs with a linear progression backbone (voltage tiers, age stages, tech levels) where mod-specific content chapters need to reference backbone progression without duplicating quest nodes. Most relevant for packs with 20+ chapters where the backbone and mod chapters are in separate chapter files.
**Implementation:**
- Define the backbone highway as a sequence of chapters (e.g., voltage tiers: LV → MV → HV → ... → UV), each with its own chapter file.
- In mod-specific chapters (e.g., AE2, Botania), use `quest_links` to reference quests in the backbone chapters. Each quest_link creates a one-way navigation bridge: the player can click through from the mod chapter to the corresponding backbone quest.
- Use quest_links at tier-gate points: when an AE2 quest requires "HV-tier machine hull," place a quest_link to the HV chapter's machine hull quest. This visually and structurally ties the mod content to the backbone without creating hard dependency edges.
- Typical density: 8-15 quest_links per mod chapter in a pack with 9-15 backbone tiers. CTNH's AE2 chapter has 13 quest_links to 4 voltage tier chapters (LV, MV, HV, IV).
- Quest_links should NOT replace hard dependencies — use `dependencies: [...]` for mandatory progression gates and `quest_links` for navigational convenience and context.
- Pair with `group_icon` on each backbone chapter to create a visual identity (e.g., gtceu:lv_machine_hull for LV chapter) that makes quest_links instantly recognizable when they appear in mod chapters.

**Edge case notes:**
- **Quest_links vs. dependencies:** A quest_link is navigational only — it does not block quest completion. If the player must complete an HV quest before accessing an AE2 quest, use a hard dependency, not a quest_link. Quest_links are best for "you'll need this tier's machines" soft references.
- **Bidirectional linking:** FTB Quests does not auto-create reverse links. If AE2 links to HV, the HV chapter does not automatically show a link back to AE2. Add reverse links manually if bidirectional navigation is desired, but be aware that too many reverse links create visual clutter in backbone chapters.
- **Hex-ID chapter interaction:** When backbone chapters use hex-ID filenames (common in large packs), quest_links must reference the hex-ID, not a human-readable name. Maintain a chapter-name-to-hex-ID mapping during development.

**Sources:** CTNH-Team/Create-New-Horizon AE2 chapter (Case 81, 13 quest_links to 4 voltage tier chapters), CTNH LV chapter (Case 81, 1 quest_link to external power generation guide). The pattern is observed in the most extensive expert GT pack in the dataset (37 chapters, ~1210 quests).
**Cross-reference:** topology-coordinates.md Case 81; MP73 (Sub-Region Decomposition) for the complementary approach of splitting content within a chapter rather than across chapters.

---

### MP79 — Voltage Highway Topology for Expert GT Packs [Preliminary — Single-Pack, Cycle 20]

**Name:** Structuring expert GregTech packs as a voltage-tier highway with mod-content parallel branches
**Applicable conditions:** Expert packs built around GregTech CEu (or similar tiered-tech mods) where the natural progression follows discrete technology tiers (LV, MV, HV, EV, IV, LuV, ZPM, UHV, UV). Applicable when the pack has 15+ chapters and 500+ quests.
**Implementation:**
- Create one chapter per voltage tier, named after the tier (e.g., "lv.snbt", "mv.snbt", "hv.snbt"). Each tier chapter contains: (a) the tier's machine hull quest as the chapter anchor (size 2.0d, gear or octagon shape), (b) the machine component tree (Motor → Piston/Pump/Conveyor → Robot Arm, octagon shapes), (c) the tier-specific processing chains (chemistry, alloy smelting, circuit crafting), and (d) the transition quest to the next tier (diamond shape, size 2.0d).
- Arrange tier chapters in a linear sequence: LV → MV → HV → EV → IV → LuV → ZPM → UHV → UV. The player progresses through tiers in strict order, with each tier gating access to the next.
- Create mod-specific chapters (AE2, Botania, etc.) as parallel branches. Gate access to each mod chapter by the minimum voltage tier required (e.g., AE2 requires MV, Botania requires HV). Use quest_links (MP78) to connect mod chapters back to the voltage backbone.
- Within each tier chapter, use the following shape semantics: octagon = machine components, gear = major milestone (EBF, assembly line), diamond = key technology unlock, rsquare = info/utility/tutorial, pentagon = tier completion.
- Size distribution: 2.0d for tier milestones (10-20% of nodes), 1.5d for sub-section anchors (15-25%), 1.0d for standard quests (55-75%). Expert GT packs tend toward MORE enlarged nodes than casual packs (up to 63% non-default in CTNH HV chapter).
- Quest descriptions should be tutorial-style (multi-paragraph explanations of GT concepts) rather than simple task descriptions. Expert pack players expect educational content in quest descriptions.

**Edge case notes:**
- **Tier count scaling:** Packs with 5-7 tiers (LV through IV) can keep all tiers as chapters. Packs with 9+ tiers (LV through UV) should consider merging late-game tiers (ZPM, UHV, UV) into fewer chapters if individual tiers have fewer than 15 quests, to avoid excessive chapter count with thin content.
- **Cross-tier recipes:** Some GT recipes span multiple tiers (e.g., a circuit that requires LV components but is crafted in MV). Place the quest in the tier where the recipe is unlocked, but add quest_links to the lower-tier component quests.
- **Non-GT mod integration:** When non-GT mods (Create, Botania) are part of an expert GT pack, their chapters should reference the voltage backbone via quest_links but maintain their own internal topology (linear_chain, tree_branching). Do not force non-GT mods into the voltage-tier structure.

**Sources:** CTNH-Team/Create-New-Horizon (Case 81, 9 voltage tiers + 2 named mod chapters + 25 hex-ID chapters). Phoenix-Forge-Technologies (Cycle 15, voltage-tier GT pack with similar structure but fewer tiers). GregTech-Leisure-Server (Cycle 19, non-expert GT pack that also uses voltage-tier chapters but without cross-links).
**Cross-reference:** topology-coordinates.md Cases 62-63 (GTLS voltage tiers), Case 81 (CTNH full voltage highway); MP78 (Quest Links as Bridge Nodes).

---

### MP80 — Icon Rate Calibration by Pack Type [Preliminary — Multi-Pack, Cycle 20]

**Name:** Targeting icon customization rates based on pack type and chapter content category
**Applicable conditions:** All packs during Step 2 (outline) when deciding how many quests should have custom `icon` values. The icon rate significantly affects visual identity and player perception of production quality.
**Implementation:**
- **Expert packs** (GT, Create expert, age-gated expert): Target 3-10% icon rate. Reserve custom icons for: (a) tutorial/info nodes (player_head or custom guide character), (b) chapter completion rewards (avaritia items, special artifacts), (c) tier-gate markers (machine hull icons). Expert packs compensate for low icon rates with detailed quest descriptions (multi-paragraph tutorials).
- **Casual/kitchen-sink packs**: Target 20-45% icon rate. Use custom icons for mod-specific items, progression milestones, and visual variety. Kitchen-sink packs benefit from higher icon rates because players browse rather than read — visual scanning is the primary navigation mode.
- **Exploration/collection chapters**: Target 50-75% icon rate. Exploration content is inherently visual — each biome, structure, or collection target benefits from a custom icon. MCC world_exploration (74%) and Material Factory chapter1 (44%) represent the upper and lower bounds of this range.
- **RPG/adventure packs**: Target 15-30% icon rate. Boss fights, race selections, and narrative milestones benefit from custom icons, but standard combat/collection quests use default shapes.
- Apply icons at chapter outline time (Step 2), not during node generation (Step 4). Decide which quests deserve custom icons before generating any quest content, to maintain consistent icon density across the chapter.

**Edge case notes:**
- **The icon-description tradeoff:** Expert packs with 3-10% icon rates typically have 5-10× longer quest descriptions than casual packs with 40%+ icon rates. This is a deliberate design choice: expert packs prioritize text-based education while casual packs prioritize visual scanning. Do not mix strategies within a single pack — either commit to text-heavy/low-icon or visual-heavy/high-icon.
- **Custom icon availability:** The achievable icon rate depends on how many distinct items are available in the pack's mod set. Expert GT packs have thousands of GT items but they are visually similar (machine hulls, circuits, components), limiting meaningful icon diversity. Casual packs with diverse mod sets have more visually distinct items to use as icons.
- **Tutorial character icons:** Using a persistent tutorial character (e.g., CTNH's "Yuriko" with player_head icon) provides a consistent visual anchor across all chapters. This technique works well in expert packs where the tutorial character appears in every chapter at key teaching moments, creating a recognizable brand element.

**Sources:** CTNH (Cases 81, 3-10% icon rate across 4 chapters), Material Factory (Case 74, 44% in tech chapter), MCC world_exploration (Case 77, 74% in exploration chapter), Age of Industry (Case 79, 5% — lowest), Deadlock's End (Case 73, 29%), Vapor Opificium (Case 75, moderate), GATE ModPack (Case 80, low in boss chapters).
**Cross-reference:** topology-coordinates.md Cases 72-81 (icon rates documented for all 10 new cases); MP73 (Sub-Region Decomposition) for the complementary visual organization technique.

---

## Scope Annotation — Cycle 20 Phase 1 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP78 Quest Links as Bridge Nodes | ✔ (chapter architecture, cross-chapter link plan) | ✔ (quest_link field in SNBT) | ✔ (verify link targets exist, no broken links) |
| MP79 Voltage Highway Topology | ✔ (tier chapter planning, backbone architecture) | ✔ (per-tier shape/size semantics) | ✔ (verify tier sequence monotonicity, cross-link integrity) |
| MP80 Icon Rate Calibration | ✔ (icon budget per chapter, pack-type targeting) | ✔ (per-quest icon assignment) | ✔ (check icon rate vs pack-type target range) |
