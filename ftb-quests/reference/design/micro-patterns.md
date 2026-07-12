# FTB Quests — Micro-Patterns [ACTIVE]

> **Status:** Active | **Cycle:** 11 | **Updated:** 2026-07-12
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
**Sources:** Multiblock Madness 2 botania chapter (52 quests, 27.5 unit span, 3 horizontal layers). This topology has only been observed in one pack so far; it may be specific to multiblock-centric designs where each branch represents a different multiblock structure's recipe chain.
**Cross-reference:** topology-coordinates.md Case 10, MP9 (Parallel Columns) for the vertical branch segments.

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
**Sources:** Finality Genesis cataclysm (28 quests, ALL square), RAD3 milestones (63 quests, ALL none), Monifactory groundwork (97 quests, 66/97 = 68% hexagon), GregTech-Odyssey lv (129 quests, ~60% hexagon). This pattern is the most common in the dataset — approximately 40% of sampled chapters use shape monoculture (>80% same shape).
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
**Sources:** FTB Evolution create (27 icons across 123 quests — highest icon density at 22%, functioning as visual waypoints). ATM-10 create root quest at size 3.0 acts as a waypoint even without a decorative image. The mcmod.cn tutorial (post/5137) documents the theme system and decorative image customization that enables this pattern. mcmod.cn post/1416 recommends using custom images to enhance visual guidance.
**Cross-reference:** MP47 (Compartment Region Layout) for the background-image variant; topology-coordinates.md Phase 5 icon rules; AP23 (Topology Mixing) — waypoints help signal topology transitions.

---

## Scope Annotation — Cycle 11 Phase 2 Patterns

| Pattern | Step 2 (outline) | Step 4 (node) | Step 5 (validation) |
|---------|-------------------|---------------|---------------------|
| MP49 Spiral/Vortex | ✔ (advanced aesthetic choice) | ✔ (per-ring node placement) | ✔ (check spiral regularity) |
| MP50 Decorative Waypoint | ✔ (landmark planning) | ✔ (image placement) | ✔ (check waypoint coverage) |
