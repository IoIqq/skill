# ATM Layout Modules — Composable Building Blocks

**Source:** 841 quests from 21 ATM9/ATM10 chapters (2026-07-04).  
**Philosophy:** Mix-and-match these 8 atomic modules to compose any chapter layout.

---

## Module 1: Spacing Grid

ATM uses a **quantized coordinate system**. Never place quests at arbitrary coordinates; snap to this grid:

| Unit | Purpose |
|------|---------|
| `1.0` | Tight grouping within a subsystem |
| `2.0–2.5` | Standard spacing between related quests |
| `3.5` | Gap between subsystems |
| `4.5` | Chapter-level section separator |
| `0.71` (√2/2) | Diagonal adjacency (minimum) |

**Y-lane convention:** Values are integers or half-integers (`-2.0, -1.5, ..., 0.0, 0.5, ...`). Quests sharing a y-value form a horizontal "swim lane."

---

## Module 2: Shape Vocabulary

Shapes carry **semantic meaning** — players learn to read them at a glance.

| Shape | Meaning | Use for |
|-------|---------|---------|
| `circle` | default | Ordinary steps (fallback when `default_quest_shape=""`) |
| `square` | check | Checkmark tasks, collection proofs |
| `diamond` | milestone | Boss kills, tier achievements |
| `hexagon` | hub | Branch points, multi-path junctions |
| `gear` | Create | Create mod machines only |
| `rsquare` | optional | `optional: true` side quests |
| `octagon` | endgame | Final boss, capstone components |
| `heart` | easter egg | Rarely; pure decoration |

**Frequency from 841 nodes:** rsquare(237) > diamond(154) > circle(149) > gear(103) > square(102) > hexagon(65) > octagon(27)

---

## Module 3: Size Hierarchy

Size = visual weight. Three tiers cover 99% of cases:

| Tier | Size range | What it signals |
|------|-----------|-----------------|
| Leaf | `0.8–1.0` | Ordinary quest node (76% of all nodes) |
| Hub | `1.2–1.5` | Subsystem entry, small milestone (18%) |
| Boss | `2.0–5.0` | Chapter boss, capstone, ATM Star (5%) |

**ATM Star** is the single `5.0` node across all 841 quests — reserve extreme sizes for one-of-a-kind.

---

## Module 4: Dependency Topologies

Four patterns. Compose them freely within a chapter.

**A. Linear Chain** — `fan_out≤1, fan_in≤1`  
`Q1→Q2→Q3` — tutorials, single recipe ladders.

**B. Fan-out Tree** — `fan_out=5–80`  
One hub → many leaves. Use `hide_dependency_lines: true` on the hub to suppress visual spaghetti.  
ATM9 `basic_tools` fans out 80 quests from one node.

**C. Convergence Star** — `fan_in=5–12, roots=50–90%`  
Many independent quests → one center node. Endgame chapters.  
ATM10 `chapter_2_the_star`: 90 roots converge on a single `size=5.0` node.

**D. Independent Grid** — `roots≥78%, fan_out≤2`  
No meaningful deps. Collectibles, bounties, catalogs.

---

## Module 5: Flag Strategies

| Flag | When to use | ATM9 intensity | ATM10 intensity |
|------|-------------|----------------|-----------------|
| `hide_dependency_lines: true` | Fan-out hubs, dense areas | **Heavy** (73/144 in Botania) | Light (0–31/chapter) |
| `hide_until_deps_visible: true` | Long chains, post-boss reveals | **Heavy** (56/144 in Botania) | Light (0–17/chapter) |
| `invisible: true` | Trigger-only tasks | 0–5/chapter | 0–5/chapter |
| `optional: true` | Side quests, easter eggs | 1–7/chapter | 2–9/chapter |

**Rule:** ATM uses `default_hide_dependency_lines: false` globally, then applies `hide_dependency_lines` **per-quest**. Never set the chapter default to `true`.

---

## Module 6: Canvas Sizing

Quest count → canvas dimensions (all coordinates are per-chapter-local):

| Quests | Aspect (w:h) | X span | Y span | Layout family |
|--------|-------------|--------|--------|---------------|
| 2–10 | any | 0–16 | 6–10 | Portal |
| 30–60 | 2.5–3.5 | 25–26 | 7–10 | Ribbon |
| 50–100 | 0.8–1.5 | 14–23 | 13–21 | Dense Mesh |
| 100–150 | 0.9–1.8 | 23–37 | 20–31 | Large Mesh / Convergence |

---

## Module 7: Image Types

Four categories. Images are decorative — they never block gameplay.

| Type | Identifying features | Placement |
|------|---------------------|-----------|
| **Logo** | `w≈5, h≈5, rotation≈8°` | Chapter center top, `y≈-4.5` |
| **Title banner** | `w=4–7, h=1–2`, src contains "title" | Above subsystem clusters |
| **Decorative SVG** | `w=2–4, h=2–4, rotation=20–22°` | Canvas edges, between quest clusters |
| **Separator** | `w=1–2, h=10+`, `rotation=45°` | Vertical dividers between subsystems |

**Extreme case:** ATM10 Create uses 116 images (76 decorative cogs at `rotation=22°`) to build visual theming.

---

## Module 8: Progression Defaults

Universal across all 21 ATM chapters:
- `progression_mode: "flexible"` — player picks order within tiers
- `default_hide_dependency_lines: false` — per-quest control, never global

---

## Composition Recipes

Mix modules to build chapter types:

| Recipe | Modules |
|--------|---------|
| **Welcome** | M1(tight) + M2(rsquare) + M7(logo) + M8 |
| **Tech Mesh** | M1(2.0 step) + M2(gear/hex) + M3(leaf+hub) + M4(B) + M5(light) + M6(large) + M7(decorative) |
| **Ribbon** | M1(3.5 step) + M2(diamond) + M4(A) + M5(medium) + M6(wide) |
| **Convergence** | M1(4.5 step) + M2(square→octagon) + M3(leaf→boss) + M4(C) + M6(large) |
| **Tall Spine** | M1(1.0 step vertical) + M4(B, fan_out=80) + M5(hide lines on leaves) + M6(tall) |
| **Catalog** | M1(4.5 grid) + M2(rsquare) + M4(D) + M6(medium) |

---

*Source: 841 quests from 21 ATM9/ATM10 chapters, parsed 2026-07-04.*
