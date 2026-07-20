# SKILL.md Update Draft — Cycle 12 Phase 5

## Summary
3 insertions proposed. No deletions. All low-risk additions within existing Step structure.

---

## Insertion 1: Step 3 — Topology Selection

**Location:** After the existing topology-aware layout block in Step 3 (after line 380: "Do NOT attempt collision detection during scaffold — that is reserved for R58 validation in Step 5."). Insert between the topology formulas block and the IDs paragraph.

**New text:**

```markdown
**Topology selection protocol (Cycle 12 — mandatory before coordinate assignment):**

Before assigning coordinates to any chapter's skeleton, you MUST:

1. **Read `reference/design/topology-coordinates.md`** — at minimum §Phase 2 (Topology Classification) to understand the seven topology types and their classification criteria (max_depth, max_width, convergence_ratio, divergence_ratio, has_hub, has_grid, has_highway_spine).

2. **Select the topology type that matches this chapter's content structure:**
   - **linear_chain** — tutorial chapters, single-mod recipe ladders, skyblock openers (deep and narrow dependency chains)
   - **hub_fan** — mods with multiple sub-systems radiating from a central mechanic (e.g., Mekanism, AE2)
   - **parallel_columns** — independent parallel progression lines (e.g., bounty boards, multi-material upgrade paths)
   - **diamond_convergence** — multiple paths that diverge then rejoin at a capstone or convergence quest
   - **tree_branching** — large expert-pack main progression with hub → sub-hub → leaves hierarchy
   - **grid_catalog** — collection/milestone chapters with minimal dependencies (flat tiling)
   - **highway_branch** — horizontal spine with vertical branches (e.g., Botania, multi-structure mods)

3. **Use the selected topology's coordinate template and spacing formulas** from §Phase 3 (Initial Coordinate Assignment). Apply the constraint formulas from §Layer 2 — do not invent custom spacing; the formulas are calibrated from 30 chapters across 16 packs.

4. **Calibrate parameters against real-world cases (Cycle 12 addition):** reference `topology-coordinates.md` Cases 14–20 for calibration data from expert, kitchen-sink, and mega-chapter packs:
   - **Case 14** (parallel_columns, Create-New-Horizon `lv`, 61 quests) — parallel processing chains with diamond/gear milestones, avg spacing 2.55
   - **Case 15** (highway_branch, Create-New-Horizon `mv`, 80 quests) — horizontal spine at y=12-17 with voltage-tier transitions
   - **Case 16** (diamond_convergence, Chroma-Technology-2 `mekanism`, 199 quests) — extreme convergence_ratio 0.412, min spacing 0.71
   - **Case 17** (grid_catalog, Gregtech-Voyager `chapter_2_mv`) — grid layout with independent x/y spacing parameters
   - **Case 18** (tree_branching, CodeNameCIM2 `start`) — recursive subtree layout with tier-gated branching
   - **Case 19** (highway_branch, Gregtech-Voyager `chapter_3_hv`) — expert-pack highway with voltage-tier scaling
   - **Case 20** (grid_catalog hub-and-spoke, Chroma-Technology-2 `creative`) — hub-and-spoke variant of grid catalog

   Match the chapter's quest count, topology type, and pack genre to the closest case, then use that case's spacing/shape/size parameters as the starting point. Adjust for pack-specific differences (expert packs use more shape variety; kitchen-sink packs use tighter spacing).
```

---

## Insertion 2: Step 4 — Mandatory Reasoning Steps

**Location:** Two sub-insertions, each extending an existing reasoning gate.

### 2a: Extend Gate 1 (Task Item Reachability)

**Location:** After the existing R42 additional check block in Gate 1 (after line 452: "Note: this is a semantic reinforcement of Gate 1, not a change to its pass/fail logic. Gate 1 already implicitly covers R1/R2/R3; this extension explicitly adds the R42 stage-internal resource reachability perspective."). Insert before the "**Gate verdict:**" line.

**New text:**

```markdown
   **R65–R67 Cross-Cutting Item Checks (Cycle 12 addition — mandatory reasoning):**

   Beyond R1–R4 and R42, each task item must additionally be evaluated against the three cross-cutting progression integrity rules from `reference/design/progression-rules.md` §Section B2. These rules defend against the "three hard problems" (item cross-tier, sequence inversion, reward disconnection) that recur across every pack archetype:

   - **R65 Tier-Bridge Equipment Sufficiency:** If this quest sends the player to a new dimension, biome, or combat zone (detected via `dimension`, `biome`, or `kill` tasks on this or ancestor quests), verify that the player's reachable equipment tier is sufficient to survive basic encounters there. Answer: "Does the player have tier-appropriate gear before entering [location]?" If the required equipment tier exceeds what ancestor quests provide by more than one tier level → mark `[unverified:tier_bridge]` and surface to user. Note: R65 is tagged `[EXTERNAL_TOOL_REQUIRED]` — without external mob-dimension-equipment mapping data, downgrade to INFO and note the data gap.

   - **R66 Cross-Branch Gate Independence:** If this quest's task item originates from a different progression branch than the current chapter (e.g., a tech-branch quest requiring a magic-branch item), check whether the item is from the other branch's early stage (depth ≤ 3) or a convergence point. Answer: "Is this cross-branch dependency on an early-stage item or at a convergence point?" If the item is deep in another branch (depth > 3) and this is not a capstone/convergence quest → **GATE FAIL: cross-branch gate**. Suggest making the dependency optional or relocating to a convergence point.

   - **R67 Weak Lock Bypass Detection:** If the pack uses stage gates and this quest's task item has multiple acquisition paths, check whether an alternate path bypasses the intended stage gate at trivially low cost (< 30% of intended path cost). Answer: "Can the player obtain this item through a path that skips the intended gate?" If yes and the bypass cost is < 30% → mark `[unverified:bypass]` and surface to user. Note: R67 is tagged `[EXTERNAL_TOOL_REQUIRED]` — without a complete recipe database (JEI/CraftTweaker export), downgrade to INFO and check only known bypasses from training data.

   These three checks are advisory at generation time (WARNING/INFO severity) — they surface potential issues in the step 7 summary for user review. The formal validation runs in Step 5 with the full graph and external data available.
```

### 2b: Extend Gate 2 (Reward Bridge)

**Location:** After the existing R45 additional check block in Gate 2 (after line 483: "Note: this is a semantic reinforcement of Gate 2. Gate 2 already checks reward bridging at the quest level (R10); this extension raises the perspective to the chapter level (R45), ensuring chapter-to-chapter transitions have explicit reward guidance."). Insert before the "**Backward matching**" paragraph.

**New text:**

   **R70, R72 Extended Reward Checks (Cycle 12 addition — mandatory reasoning):**

   Beyond the four Gate 2 categories and R45, each reward must additionally be evaluated against two cross-cutting progression rules from `reference/design/progression-rules.md` §Section B2:

   - **R70 Reward-to-Dependent Item Bridge:** Strengthen the Material Bridge (MP14) and Universal Bridge checks with item-level granularity. Answer: "Does at least one reward item directly appear as a task item in a dependent quest?" R10 checks that the *connection exists*; R70 checks that the *reward item itself* participates in the next step (as an ingredient, a tool, or a multi-block component). If no reward item bridges to any dependent quest's task requirement → flag as R70 dead-end risk (stronger signal than the existing AP6 dead-end check). For expert packs, extend `max_bridge_depth` to 2 (reward item may appear up to 2 dependency hops away).

   - **R72 Late-Game Reward Relevance:** If this quest is in the late-game stage (depth ≥ 80% of the chapter's or book's maximum chain depth), answer: "Is at least one reward relevant to subsequent content?" Late-game rewards must be either (a) a component of a subsequent quest's recipe chain, (b) a tool/machine enabling new capabilities, or (c) a prestige/capstone item serving as a meaningful completion marker. Generic rewards (XP, diamonds, currency) in late-game quests fail this check — as the FTB Quests tutorial notes, late-game XP rewards are "insignificant." If all rewards are generic and the quest has dependents → flag as R72 late-game reward drift.

   These checks are integrated into the existing Gate 2 flow: R70 runs as a stricter version of the four-category classification (strengthening dead-end detection), and R72 runs only for late-game quests (advisory, not blocking — surfaces in the step 7 summary).

---

## Insertion 3: Step 5 — Extended Validation

**Location:** After the topology validation results print block in Step 5 (after line 578: the closing triple-backtick of the topology validation summary). Insert between the topology validation print block and the "Dev testing — scope it" note.

**New text:**

```markdown
**Cross-cutting progression validation (R65–R72 — Cycle 12 addition):** After topology validation (R55–R64), run the cross-cutting progression integrity rules from `reference/design/progression-rules.md` §Section B2. These eight rules defend against the three hard problems that recur across every pack archetype: item cross-tier, sequence inversion, and reward disconnection.

Execution priority (from `progression-rules.md` §Section C):

| Priority | Rule | Name | Check type |
|----------|------|------|-----------|
| P1 | R65 | Tier-Bridge Equipment Sufficiency | equipment tier vs mob tier |
| P1 | R66 | Cross-Branch Gate Independence | cross-branch dependency depth |
| P1 | R68 | Mod First-Appearance Teaching Precedence | mod reference depth tracking |
| P1 | R70 | Reward-to-Dependent Item Bridge | reward item ∩ dependent requirement |
| P2 | R69 | Description-Trigger Alignment | description keyword scan |
| P2 | R72 | Late-Game Reward Relevance | reward relevance vs descendants |
| P3 | R71 | Recipe-Type Diversity Within Stage | recipe type distribution |

**EXTERNAL_TOOL_REQUIRED rules:** The following rules require external mod data (mob spawn tables, recipe databases, recipe-type classifications) that is not available during quest generation. They execute via external validation tools in Step 5. Without the required external data, downgrade each to INFO with the note "External data not available — check is incomplete":
  - **R65** (Tier-Bridge Equipment Sufficiency) — requires mob-dimension-equipment tier mapping
  - **R67** (Weak Lock Bypass Detection) — requires complete recipe database (JEI/CraftTweaker export) for all acquisition paths
  - **R71** (Recipe-Type Diversity Within Stage) — requires mod-specific recipe-type classifications (Create mixing, Mekanism chemical infuser, etc.)

**Anti-pattern checks (AP28–AP29 — Cycle 12 addition):** As part of the whole-book pass, scan for two layout anti-patterns from `reference/design/anti-patterns.md`:
  - **AP28 Mega-Chapter Without Structural Compensation:** For each chapter with 150+ quests, verify that at least two structural compensation strategies are present: decorative region images (MP47), selective `hide_dependency_lines` (on quests with local density > 8), size variation beyond default 1.0, or shape vocabulary beyond the chapter default. If no compensation → WARNING: "Mega-chapter '{name}' ({n} quests) lacks structural hierarchy. Apply compensation strategies or split into sub-chapters." Reference: Chroma-Technology-2 mekanism (199 quests, 80% hide_dep_lines) and Craftoria Create (180 quests, 8 decorative compartments) as positive examples.
  - **AP29 Dependency Line Color Blindness:** Verify that no chapter relies solely on dependency line color to distinguish progression modes (linear vs. flexible). Check whether shape and size carry the semantic distinction instead — linear quests using the chapter default shape, flexible quests using a distinct shape or size. If the only distinction is line color → WARNING: "Chapter '{name}' relies on dependency line color to distinguish progression modes. This distinction may be lost after mod updates or for players with color vision deficiency. Use shape/size as the primary indicator."

Print cross-cutting and anti-pattern validation results as part of the summary:
```
Cross-cutting validation (R65–R72): {pass/warn/error}
   R65 tier-bridge: {pass/warn/skip} | R66 cross-branch: {pass/warn} | R68 teaching: {pass/warn}
   R70 reward-bridge: {pass/warn} | R69 desc-align: {pass/info} | R72 late-game: {pass/warn}
   R71 recipe-diversity: {pass/warn/skip}
   EXTERNAL_TOOL_REQUIRED: {count} rules downgraded to INFO (missing external data)
Anti-pattern check (AP28–AP29): {pass/warn}
   AP28 mega-chapter: {pass/warn/count} | AP29 line-color: {pass/warn/count}
```
```

---

## Risk Assessment

- **All 3 insertions are pure additions** (no deletions, no restructuring of existing text) → **Low risk**
- **No changes to existing Step logic** — each insertion extends existing gates or adds post-existing-block content → **backward compatible**
- **Insertion 1** (Step 3 topology protocol) adds mandatory reading and calibration steps that reinforce the existing topology-aware layout block — no conflict with current formulas
- **Insertion 2** (Step 4 reasoning extensions) adds R65–R67 and R70/R72 checks to existing Gate 1 and Gate 2 flows — these are advisory at generation time (WARNING/INFO), not blocking, so they do not change the Gate verdict logic
- **Insertion 3** (Step 5 validation) adds R65–R72 and AP28–AP29 to the existing validation pipeline — positioned after topology validation (R55–R64), before the summary print, with explicit EXTERNAL_TOOL_REQUIRED annotations to prevent false failures when external data is unavailable
- **No new dependencies on files that don't exist** — all referenced files (`topology-coordinates.md`, `progression-rules.md`, `anti-patterns.md`) are confirmed present in `reference/design/`
- **Writing style** matches existing SKILL.md: structured tables for rule listings, prose for guidance, backtick code references, bold emphasis for key terms
