# SKILL.md Cycle 11 Update Draft

> **Status:** Draft | **Cycle:** 11 | **Date:** 2026-07-12
> **Author:** Phase 5 Writing Agent
> **Purpose:** Precise insertion points for topology-aware guidance in SKILL.md Steps 2/3/4/5. Each section below specifies the exact location and content to add.

---

## Update 1: Step 2 (Interview) — Add topology selection as mandatory question

**Location:** In the Step 2 "Work the branches in dependency order" section, after the "Structure" branch (which covers chapter count, spine, capstone) and before the "Rewards & difficulty" branch.

**Anchor text (find this in SKILL.md):**
> `- **Rewards & difficulty:** reward philosophy (generous items vs cosmetic/lore), ...`

**Insert BEFORE that line:**

```markdown
- **Topology selection — MANDATORY:** "你希望这个 chapter 使用什么布局拓扑？" Seven options (load `reference/design/topology-coordinates.md` §Phase 2 for visual examples):
  - **linear_chain** — 深度线性链（教程章、单 mod 配方链）
  - **hub_fan** — 中心 hub 辐射分支（多子系统 mod 如 Mekanism）
  - **parallel_columns** — 并行纵列（赏金板、多材料并行升级）
  - **diamond_convergence** — 菱形汇聚（多路线汇聚到 capstone）
  - **tree_branching** — 树状分支（大型专家包主进度线）
  - **grid_catalog** — 网格目录（里程碑/成就收集章）
  - **highway_branch** — 水平主干+垂直分支（多结构 mod 如 Botania）
  Ask per-chapter, not per-book — different chapters in the same pack typically use different topologies. Recommend based on the chapter's content structure: a mod with N sub-systems → hub_fan; a linear upgrade path → linear_chain; a collection trophy case → grid_catalog. The topology choice drives coordinate assignment in Step 3 and validation rules in Step 5.
```

**Rationale:** Currently Step 2 has no explicit topology question. The topology emerges implicitly from content decisions, but the Cycle 11 research showed that making it explicit improves layout quality. The seven topology types from `topology-coordinates.md` Phase 2 now cover all observed real-world patterns.

---

## Update 2: Step 3 (Scaffold) — Add topology-aware layout guidance

**Location:** In Step 3, after the paragraph that begins "Layout (the generator's `auto` layout follows the same convention)" and before the paragraph "IDs are computed automatically".

**Anchor text (find this in SKILL.md):**
> `Layout (the generator's `auto` layout follows the same convention): main path left-to-right ...`

**Insert AFTER the layout paragraph (the one ending with "...`size: 1.0`."):**

```markdown
**Topology-aware layout (Cycle 11):** If a topology was selected in Step 2, read `reference/design/topology-coordinates.md` §Phase 3 to choose the coordinate assignment strategy matching the topology type. Use the constraint formulas (spacing, hub radius, column gap) from §Layer 2 to calculate initial coordinates. Key formulas by topology:
  - linear_chain: `y_spacing = clamp(1.5 * density_factor, 1.0, 2.5)` with optional x-zigzag
  - hub_fan: `hub_radius = clamp(3.0 + fan_out * 0.4 + max_leaves * 0.5, 3.5, 8.0)` — note the 31% deviation from original formula when sub-hubs have leaves
  - parallel_columns: `column_x_gap = clamp(2.0 + width * 0.5, 2.0, 4.0)`
  - highway_branch: x-spine at 2.0 spacing, branches at 1.5 vertical offset
  - grid_catalog: `columns = ceil(sqrt(quest_count))`, 1.5×2.5 spacing
  - tree_branching: recursive subtree layout with `total_width=16.0`
  - diamond_convergence: sin-curve spread `x_spread = 3.0 + path_length * 0.5`

Do NOT attempt collision detection during scaffold — that is reserved for R58 validation in Step 5.
```

**Rationale:** Step 3 currently has generic "auto" layout guidance. The topology-specific formulas give the AI concrete parameters for each layout type. The collision detection note prevents the AI from wasting tokens on Phase 4's iterative algorithm.

---

## Update 3: Step 4 (Polish) — Add topology rule checking guidance

**Location:** In Step 4, after the "Reasoning Gate 3: Dependency Chain Sanity" section and before "7. Show a focused summary".

**Anchor text (find this in SKILL.md):**
> `Gate 3 is **advisory, not blocking** — it surfaces structural observations ...`

**Insert AFTER the Gate 3 paragraph:**

```markdown
**Topology layout check (per chapter, after all nodes are polished):** Load `reference/design/progression-rules.md` §Section B and check R55–R64 for the chapter's chosen topology. Priority checks:
  - **R55** Topology-Progression Mode Alignment — does the chapter's `progression_mode` match the topology? Note the R41 early-game override: tutorial chapters (depth ≤ 3, ≤ 15 quests) may use `flexible` with `linear_chain` without triggering a warning.
  - **R57** Hub Node Size Dominance — if hub_fan or tree_branching, verify hub size > max child size.
  - **R60** Topology-Shape Vocabulary Coherence — shape count within the topology's guideline range.
  These are advisory at generation time (Step 4); the formal checks run in Step 5.
```

**Rationale:** Step 4 currently has Gates 1-3 covering items, rewards, and dependencies, but no topology-specific checks. Adding a lightweight per-chapter topology scan catches obvious mismatches before Step 5.

---

## Update 4: Step 5 (Verify) — Add topology validation pipeline

**Location:** In Step 5, after the paragraph "The whole-book validation runs the full progression-rules pipeline (R1–R32..." and before the summary printout.

**Anchor text (find this in SKILL.md):**
> `The whole-book validation runs the full progression-rules pipeline (R1–R32, distributed across the modular reference files — see `reference/design/module-index.md` for routing) ...`

**Replace with (the original paragraph plus the topology extension):**

```markdown
The whole-book validation runs the full progression-rules pipeline (R1–R32, distributed across the modular reference files — see `reference/design/module-index.md` for routing) — item reachability across the complete dependency graph, reward continuity across all chapters, teaching order for every chapter, description consistency for every quest, command safety, team progression consistency, and chapter-level QA heuristics. The Step 4 per-node checks are a generation-time subset; Step 5 catches cross-quest and cross-chapter issues that only become visible once the full graph exists.

**Topology validation (R55–R64 — Cycle 11 addition):** After the core R1–R32 pipeline, run the topology-aware layout rules from `reference/design/progression-rules.md` §Section B. Load `reference/design/topology-coordinates.md` for the classification algorithm and coordinate data. Execution order:
  1. **R58** (P0) Collision-Free Adjacent Nodes — all-pairs distance check. This is the primary layout invariant; overlapping quests are the most basic layout failure.
  2. **R55** (P1) Topology-Progression Mode Alignment — verify each chapter's topology matches its progression_mode. Apply R41 override for early-game chapters.
  3. **R56** (P1) Depth-Axis Monotonicity — deeper quests should appear further along the primary axis.
  4. **R59** (P1) Bounding Box Viewport Fit — chapter fits within 35×30 unit viewport.
  5. **R61** (P1) Convergence Point Visual Prominence — convergence nodes at visual terminus.
  6. **R57** (P2) Hub Node Size Dominance — hub size hierarchy.
  7. **R62** (P2) Parallel Column Spacing Uniformity.
  8. **R63** (P2) Grid Catalog Aspect Ratio.
  9. **R64** (P2) Decorative Image Topology Alignment.
  10. **R60** (P3) Topology-Shape Vocabulary Coherence.

Print topology validation results as part of the summary:
```
📐 Topology validation: {pass/warn/error}
   Chapters checked: {N} | Topology types: {list}
   R58 collisions: {count} | R55 alignment: {count} | R59 viewport: {count}
```
```

**Rationale:** Step 5's verification pipeline currently references only R1-R32. The topology rules R55-R64 are equally important for layout quality and should be part of the standard validation pass. The P0/P1/P2 ordering matches Section C's execution priority.

---

## Update 5: Module Index reference in SKILL.md

**Location:** In the "Micro-level authoring patterns" paragraph, the last sentence references `module-index.md`.

**Anchor text (find this in SKILL.md):**
> `See `reference/design/module-index.md` for the full routing table.`

**Insert AFTER that sentence:**

```markdown
For topology-aware layout rules (R55–R64), coordinate algorithms, and real case data from 13 chapters across 9 packs, load `reference/design/topology-coordinates.md` and `reference/design/progression-rules.md` §Section B.
```

**Rationale:** The module-index.md routing table already includes topology-coordinates.md and will be updated to include progression-rules.md (Task 4). This explicit reference in SKILL.md ensures the AI knows to load these files for topology work.

---

## Application Notes

- All five updates are independent and can be applied in any order.
- Updates 1 and 2 are the highest priority — they directly affect the interview and scaffold flow.
- Updates 3 and 4 are medium priority — they add validation checks that improve output quality.
- Update 5 is lowest priority — it's a navigation aid.
- None of the updates conflict with existing SKILL.md content; they are purely additive.
- The topology selection question (Update 1) should be asked per-chapter during the Structure branch, not as a global pack-level question.
