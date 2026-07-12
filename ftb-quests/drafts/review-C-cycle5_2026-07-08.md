# Reviewer C — Cycle 5 Practicality Review

> **Reviewer C scope:** AI agent executability — can an AI agent actually *use* these patterns/rules during generation and validation?
> **Date:** 2026-07-08
> **Status:** FINAL

---

## Summary

Cycle 5 adds four micro-patterns (MP35–MP38) and two draft rules (R36–R37). The patterns are documented in the archived file and the module-index routes them, but none have been distributed to the modular reference files yet. Two patterns (MP35, MP37) are immediately usable with minor additions; one (MP36) requires a signal mechanism to be practical; one (MP38) is blocked by domain knowledge. Both draft rules are validation-stage only and don't affect generation.

---

## MP35 — Dual-Task Automation Verification

**Rating: B**

**Pattern summary:** Quest has two tasks: `item` with `consume_items: false` (prove it exists) + `checkmark` labeled "Automated" (honor-system confirm the player built a machine).

**How AI would apply it:**
During Step 4 node generation, when the chapter's theme is "automation verification" and the pack is Create-focused expert, the AI should generate dual-task quests instead of single-item tasks.

**Signal mechanism assessment:**
The SKILL.md Step 2 interview does not currently ask about automation verification. The agent has no trigger to decide "this pack wants dual-task automation." The signals needed are:

1. **Pack genre:** create + expert (both settled in Step 2 — available).
2. **Automation expectation:** does the pack author expect players to build machines, not hand-craft? (NOT currently asked in Step 2).
3. **consume_items philosophy:** already asked in Step 2 ("Rewards & difficulty" branch) — if the user says "keep items" or "don't consume," this is a strong MP35 signal.

**Execution gaps:**
- Step 2 interview needs one additional question: "Is this pack's core loop building automation (Create contraptions, factory lines)? If so, should quests verify automation through a checkmark task?"
- The `consume_items` philosophy branch already partially captures this signal — if the user says "don't consume," the AI should infer MP35 applicability for Create packs.
- The module-index routes MP35 to `mod-teaching-pacing.md` but the file does not contain it yet. Until distributed, the Step 4 loading plan won't surface it.
- Single-source (Cabricality only) — AI should apply conservatively and ask user confirmation before assuming this pattern.

**Recommendation:** Add a single question to the Step 2 "Rewards & difficulty" branch: "For Create-focused packs: should quests require proof of automation (dual-task: item + checkmark)?" If yes, MP35 becomes active for that pack's Step 4 generation. Distribute MP35 to `mod-teaching-pacing.md`.

---

## MP36 — Currency-as-Reward

**Rating: C**

**Pattern summary:** Quest rewards use a currency item (coins, credits) that the player spends at shops/trade stations, rather than bridging to a specific next-quest ingredient.

**How AI would apply it:**
During Step 4 reward design, the AI needs to know whether a given `item` reward is a currency (accumulate and spend) or a material bridge (MP14 — next quest's ingredient). The reward bridge reasoning step says: "What does this reward lead the player to do next?" For currency, the answer is "spend at a shop" — not "submit to the next quest."

**Signal mechanism assessment:**
There is currently NO reliable signal for the AI to distinguish currency from material bridge:

1. **Item ID alone is insufficient.** `gtocore:copper_coin` and `lightmanscurrency:coin_iron` have "coin" in the name, but `frostedheart:insight` does not. The AI cannot reliably infer currency status from namespace:name.
2. **Step 2 interview covers reward philosophy** but does not ask about in-game currency systems. The "Dominant reward type" question (added by Reviewer C) covers presentation style (random/loot/choice) but not currency vs material.
3. **The pack's mod list** could hint at currency (presence of `lightmanscurrency`, `gtocore`, `wares`) but the AI would need a lookup table mapping mods to currency items.

**Execution gaps:**
- Step 2 needs an additional question: "Does your pack have an in-game currency or trading system? If so, what is the currency item ID and where do players spend it?" This gives the AI the exact item ID and the sink context.
- The reward bridge reasoning (Step 4 step 2) needs a third branch: if the reward is a known currency item, the "next step" is "spend at shop chapter" rather than "submit to dependent quest." This exempts currency from the dead-end reward check (AP6/R10).
- MP36 must be registered as an exception to R10 (dead-end reward detection). Without this, Step 5 validation would flag every currency reward as a dead-end.
- The module-index routes MP36 to `mod-reward-design.md` but the file does not contain it yet.
- The `shared-builtin-tables.md` should add a `CURRENCY_ITEMS` table mapping known currency item IDs (similar to `BUILTIN_DIMENSION_MAP` and `BUILTIN_TOOL_TIER_MAP`), so the AI can recognize currency items from existing packs.

**Recommendation:** (1) Add Step 2 question about pack currency. (2) Register MP36 as R10 exception. (3) Add currency items to `shared-builtin-tables.md`. (4) Distribute MP36 to `mod-reward-design.md`. Without all four, the AI will either ignore MP36 or misclassify currency rewards as dead-ends.

---

## MP37 — Progress Catalog Chapter

**Rating: A**

**Pattern summary:** A dedicated chapter with no dependencies, no rewards, and one item task per milestone item — serves as a visual progress tracker across all tiers/stages.

**How AI would apply it:**
During Step 2 chapter design, the AI decides whether to include a progress catalog chapter. During Step 4 generation, the chapter's quests are trivially generated: one item task per milestone, no dependencies, no rewards.

**Signal mechanism assessment:**
This pattern is the most executable of the four:

1. **Pack genre signal:** expert packs with 10+ tiers/stages (settled in Step 2). The pattern's own design consideration says "Works best in expert packs with 10+ tiers/stages; overkill for kitchen-sinks with 3-4 stages."
2. **Input requirements:** the AI needs the complete list of milestone items across all tiers. This is naturally available from the Step 2 outline — the user already identifies which items mark tier progression.
3. **Generation complexity:** minimal. Each quest is `{ name: "<tier>_<item>", depends_on: [], tasks: [{ type: "item", item: <milestone_item> }], rewards: [] }`. No dependency wiring, no reward bridging, no teaching order concerns.

**Execution gaps:**
- Step 2 needs one additional question for expert packs: "Do you want a visual progress catalog chapter that lists all milestone items?" If yes, the AI collects the milestone item list during the chapter design phase.
- The Step 4 chapter-level teaching order check does not apply (no dependencies = no ordering constraint). The AI should skip the teaching-order check for catalog chapters.
- Step 5 validation: R10 (dead-end reward) does not apply because there are no rewards. R1–R4 (item reachability) technically still applies but is trivially satisfied (no gating). The validator should not flag catalog chapters for missing reward bridges.
- Single-source (GregTech-Odyssey only) — AI should present this as an option, not a default, for expert packs.

**Recommendation:** Add one optional Step 2 question for expert packs. Add a flag `catalog: true` to the chapter spec so the AI and validator know to skip reward-bridge and teaching-order checks. Distribute MP37 to `mod-teaching-pacing.md`.

---

## MP38 — Profession Chapter

**Rating: D**

**Pattern summary:** Multiple optional chapters, each themed around a profession/role (hunter, farmer, miner, researcher), with thematically appropriate tasks and rewards.

**How AI would apply it:**
During Step 2 chapter design, the AI would need to: (1) identify which professions exist in the pack, (2) determine which mods support each profession, (3) design quest content for each profession chapter using profession-specific items and mechanics.

**Signal mechanism assessment:**
This pattern has the highest execution barrier:

1. **Profession identification:** requires deep knowledge of the pack's mod list and how mods map to playstyles. For TheWinterRescue, the 9 professions (hunter, farmer, miner, researcher, fuel_engineer, generator_engineer, siberian_chef, tundra_traveller, craftsman) are pack-specific roles that emerge from the mod combination — not a generic template the AI can fill.
2. **Mod-per-profession mapping:** requires knowing which mods support "hunter" gameplay (combat mods, mob drops, weapons) vs "farmer" gameplay (agriculture mods, crop growth, animal husbandry). This mapping is pack-specific and requires mod knowledge the AI does not have independently.
3. **Task/reward design per profession:** each profession chapter needs items and mechanics relevant to that role. The AI would need to know that "siberian_chef" involves cooking mods, "fuel_engineer" involves energy/fuel mods, etc. This is deep mod-mechanic knowledge that violates the "never guess" rule if the AI tries to infer it.
4. **No structural shortcut:** unlike MP37 (trivially one-item-per-quest), MP38 chapters need genuine quest design — teaching order, reward bridging, dependency chains — all themed around the profession. This is as complex as a normal mod chapter, multiplied by the number of professions.

**Execution gaps:**
- The AI CANNOT generate profession chapters without the user providing: (a) the list of professions, (b) which mods map to each profession, (c) key items/mechanics for each profession. This is at minimum 3 additional Step 2 questions per profession.
- The "never guess" rule means the AI must ask the user to confirm every profession-to-mod mapping and every profession-specific item. For 9 professions, this is a significant interview overhead.
- Single-source (TheWinterRescue only) — the pattern may be too pack-specific to generalize. TheWinterRescue's profession system is deeply integrated with its custom mods (`frostedheart`); a generic "profession chapter" pattern may not transfer.
- Step 4 generation for profession chapters is no different from normal chapters (the same per-node loop applies), so no Step 4 changes are needed — but the Step 2 input requirements are substantial.

**Recommendation:** MP38 should remain in the archived file as a reference pattern, not promoted to the modular system until at least one additional pack validates it. If the user explicitly requests profession chapters, the AI should grill extensively in Step 2: one question per profession (which mods? which key items? what's the reward philosophy?). Do not add a generic Step 2 question — this pattern is opt-in only.

---

## Draft R36 — Hardcore Pack Zero-Optional Constraint

**Rating: B (for validation stage)**

**Rule summary:** For packs classified as `hardcore` or `combat`, flag `optional: true` quests as INFO — optional content may undermine the pack's difficulty curve.

**Application stage:** VALIDATION (Step 5), not generation (Step 4).

**Reasoning:**
- During generation (Step 4), the AI already follows the user's `optional` decisions from Step 2. The draft rule does not change generation behavior — it adds a post-generation check.
- During validation (Step 5), the rule is a simple scan: count `optional: true` quests in chapters of hardcore/combat packs, flag if > 0.
- The pack-type classification (`hardcore`, `combat`) must be settled in Step 2 and stored in the spec. Currently, pack genre is captured ("theme" branch) but not as a structured `pack_type` field.
- The draft acknowledges this may be over-generalization (Prominence II uses optional content in a combat pack). The INFO severity is appropriate — flagging, not blocking.

**Execution gaps:**
- Needs a `pack_type` field in the spec's `data` section to drive the check.
- The draft's risk assessment is honest: "may be NFwC-specific rather than genre-universal." Two data points are insufficient for a formal rule.
- The rule is simple to implement: `if pack_type in ['hardcore', 'combat'] and any quest has optional: true → INFO`.

**Recommendation:** Keep as draft. When promoted, add to `mod-dependency-graph.md` (optional-gate checks are R7's domain). Require `pack_type` field in spec.

---

## Draft R37 — Kill Task Density Calibration

**Rating: B (for validation stage)**

**Rule summary:** For each chapter, calculate kill_tasks / total_quests. Flag chapters where kill density exceeds the pack-type guideline as WARNING.

**Application stage:** VALIDATION (Step 5), not generation (Step 4).

**Reasoning:**
- During generation, the AI follows the user's task-type decisions per quest. The draft rule does not change what tasks are generated — it adds a post-generation density check.
- During validation, the rule is arithmetic: count `type: "kill"` tasks per chapter, divide by total quests, compare against pack-type thresholds (hardcore 30-65%, RPG 10-20%, kitchen-sink 0-5%, expert/Create 0%).
- The thresholds are based on only 2-3 data points per genre. The draft acknowledges this: "More combat/RPG packs to establish baseline ranges."

**Execution gaps:**
- The thresholds need more data before they're reliable. NFwC's 65% kill density in the boss chapter is intentional (it's a boss chapter); a blanket 30-65% guideline for hardcore may flag legitimate design choices.
- The rule needs the same `pack_type` field as R36.
- Implementation is simple: per chapter, count kill tasks, divide by quest count, compare against threshold table.
- The WARNING severity is appropriate — informational, not blocking.

**Recommendation:** Keep as draft. When promoted, add to `mod-teaching-pacing.md` (task-type distribution is pacing's domain). Calibrate thresholds with at least 3 more packs per genre before hardcoding ranges.

---

## Cross-Cutting Issues

### 1. Module-index routing vs. modular file content mismatch

The `module-index.md` Three Hard Problems table references MP35, MP37, MP38 (routed to `mod-teaching-pacing`) and MP36 (routed to `mod-reward-design`). However, **none of these patterns have been distributed to the modular files yet.** The module-index is ahead of the content.

**Impact:** The Step 4 loading plan loads modular files, not the archived file. An AI following the loading plan will never see MP35–MP38.

**Fix:** Distribute MP35, MP37, MP38 to `mod-teaching-pacing.md` and MP36 to `mod-reward-design.md` before they become active rules.

### 2. SKILL.md does not reference MP35–MP38

The SKILL.md's micro-pattern references stop at MP34 (in the "Micro-level authoring patterns" paragraph of the design principles section). MP35–MP38 are not mentioned in Step 4's per-node loop or the chapter-level check.

**Fix:** Update SKILL.md's pattern reference list to include MP35–MP38 with their modular file locations.

### 3. R36/R37 lack spec infrastructure

Both draft rules need a `pack_type` field in the spec, but the current spec schema (Step 3 skeleton) does not include it. The `data` section has `default_reward_team` and `default_consume_items` but no genre classifier.

**Fix:** Add `pack_type: "kitchen-sink" | "expert" | "skyblock" | "story" | "create" | "hardcore" | "rpg"` to the spec's `data` section. Set it during Step 2's theme branch.

---

## Rating Summary

| Pattern/Rule | Rating | Primary Barrier | Stage | Actionable? |
|---|---|---|---|---|
| **MP35** Dual-Task Automation | **B** | Missing Step 2 trigger question | Step 4 (generation) | Yes — add one interview question + distribute to module |
| **MP36** Currency-as-Reward | **C** | No signal to distinguish currency from material | Step 4 (generation) + Step 5 (validation) | Partially — needs 4 changes (Step 2 question, R10 exception, builtin table, module distribution) |
| **MP37** Progress Catalog | **A** | None — trivially executable | Step 2 (chapter design) + Step 4 (generation) | Yes — add one optional question + catalog chapter flag |
| **MP38** Profession Chapter | **D** | Requires extensive mod knowledge AI doesn't have | Step 2 (chapter design) | No — keep archived, opt-in only |
| **Draft R36** Zero-Optional | **B** | Needs `pack_type` field | Step 5 (validation) | Yes when promoted — simple scan |
| **Draft R37** Kill Density | **B** | Needs `pack_type` field + more baseline data | Step 5 (validation) | Yes when promoted — arithmetic check |

---

## Prioritized Action Items

1. **[HIGH] Distribute MP35/MP37/MP38 → `mod-teaching-pacing.md`, MP36 → `mod-reward-design.md`.** The module-index already routes them; the content must follow.
2. **[HIGH] Add MP36 as R10 exception.** Without this, Step 5 validation flags every currency reward as dead-end.
3. **[MEDIUM] Add `pack_type` field to spec schema.** Required for R36/R37 and useful for pack-genre-specific logic throughout the flow.
4. **[MEDIUM] Add Step 2 questions:** automation verification (MP35), in-game currency (MP36), progress catalog (MP37).
5. **[LOW] Update SKILL.md pattern reference list** to include MP35–MP38.
6. **[LOW] Add `CURRENCY_ITEMS` table to `shared-builtin-tables.md`.**
7. **[DEFER] Keep MP38 archived** until a second pack validates it.
8. **[DEFER] Keep R36/R37 as drafts** until 3+ more packs per genre establish baseline ranges.
