# Hardcore Pack Progression Constraints (Draft R36-R37)

> **Status:** HIGH-RISK DRAFT — needs more pack data before promotion to active rules
> **Date:** 2026-07-08
> **Source:** Phase 3 Cycle 5 cross-pack comparison (NFwC vs Era of Black Death)

## Context

Cross-pack comparison of the two hardcore/combat packs in the dataset reveals design constraints that may warrant formal rules. However, with only 2 data points (NFwC and Era of Black Death), these patterns may be pack-specific rather than universal.

## Draft R36 — Hardcore Pack Zero-Optional Constraint

> **BLOCKED: insufficient data, contradicted by Prominence II**
> Only 2 data points (NFwC + Era of Black Death). Prominence II is a combat/RPG pack that uses optional content extensively, directly contradicting the zero-optional hypothesis. Cannot promote to active rule without 3+ supporting data points that are not contradicted by counter-examples.

**Observation:** NFwC uses ZERO optional quests across all sampled chapters. Era of Black Death uses low optional rates. Both are combat-focused packs where every quest is mandatory.

**Hypothesis:** Hardcore/combat packs enforce zero optionality because:
1. Every quest is a skill check — skipping content means skipping practice
2. Boss progression requires all prior combat experience
3. The pack's difficulty IS the content — optionality undermines the challenge

**Draft rule:** For packs classified as `hardcore` or `combat`, flag `optional: true` quests as INFO — optional content may undermine the pack's difficulty curve.

**Risk:** This may be over-generalization. Some combat packs (Prominence II) use optional content for side activities. The zero-optional pattern may be NFwC-specific rather than genre-universal.

**Counter-evidence:** Prominence II (RPG/combat, ~335 quests) uses optional content for side activities — contradicting the "zero optional for combat packs" hypothesis. This single counter-example is sufficient to block promotion until more data is available.

**Verification needed:** More hardcore/combat packs with public configs (RLCraft, DawnCraft, Vault Hunters 3). **Currently BLOCKED — do not use for validation until unblocked.**

## Draft R37 — Kill Task Density Calibration

**Observation:** NFwC boss chapter has 65% kill density (38/58 quests). Era of Black Death distributes kill tasks across 17 chapters. Craftoria bosses chapter has 31% kill density.

> **Revision (Cycle 5 review B): Boss vs Mob distinction required.**
> Kill density alone is insufficient — a chapter with 10 boss kills (value: 1) is fundamentally different from a chapter with 10 mob grinds (value: 50). The rule must distinguish between these two types.

**Kill task classification by `value` field:**

| Type | `value` range | Design meaning | Density concern |
|---|---|---|---|
| Boss kill | `value: 1` (or `value: 1-3`) | Unique encounter, progression milestone | Low — each is a distinct experience |
| Elite kill | `value: 3-5` | Mini-boss or rare mob | Medium — acceptable in combat packs |
| Mob grind | `value: >= 5` (typically 5-100) | Repetitive farming | High — flag if density > 30% |

**Revised draft rule:** For each chapter, calculate kill density separately for boss kills (value <= 3) and mob grinds (value >= 5). Flag chapters where **mob grind density** exceeds the pack-type guideline as WARNING. Boss kill density is informational only.

**Hypothesis:** Kill task density should correlate with the pack's combat focus:
- Hardcore/combat packs: 30-65% kill density acceptable (boss + mob combined)
- RPG packs: 10-20% kill density (bosses and milestones)
- Kitchen-sinks: 0-5% kill density (isolated to boss chapters)
- Expert/Create packs: 0% kill density

**Draft rule:** For each chapter, calculate kill_tasks / total_quests. Flag chapters where kill density exceeds the pack-type guideline as WARNING.

**Risk:** Kill density is a design choice, not a quality metric. High density in a combat pack is intentional. The rule should be informational, not blocking.

**Verification needed:** More combat/RPG packs to establish baseline ranges.

## Stage-Based Progression Implementation (Draft Observation)

**Observation:** Cabricality implements stage-based progression through chapter naming (stage_1 through stage_5 + stage_4a branching variant). The `stage_4a` chapter represents a branching variant where the player can choose between two paths at stage 4.

**How it maps to FTB Quests:**
1. Each stage is a separate chapter with `order_index` defining sequence
2. `dependency_requirement: "one_completed"` enables branching within stages (1-4 per chapter)
3. Cross-stage dependencies are cross-chapter references (R22 validates these)
4. `hide: true` on stage-opening quests hides them until previous stage is complete

**No new rule needed:** The existing rules (R4 Stage Boundary, R7 Optional-Gate-Mandatory, R22 Cross-Chapter Dependency) already cover stage-based progression. Cabricality's implementation is a clean application of existing patterns.

## Dual-Task Automation Verification Scope (MP35 Validation)

**Observation:** MP35 was identified in Cabricality (Phase 1 Cycle 5). Phase 3 cross-pack comparison confirms:
- Cabricality stage_1: consume_items: false = 20, checkmark = 18
- Cabricality stage_3: consume_items: false = 44, checkmark = 26
- Cabricality stage_4: consume_items: false = 29, checkmark = 25

**Question:** Does MP35 exist in any other pack?

**Check:** Create: Delight (the closest comparison) uses `consume_items: false` on some quests but NOT paired with an "automated" checkmark. Create: Astral uses `min_tasks: 1` for alternative paths but not dual-task verification. No other pack in the 25-pack dataset uses the dual-task pattern.

**Conclusion:** MP35 remains single-source. It should stay marked as "single-source" until a second pack validates it. The Cabricality team explicitly cites Create: Above and Beyond as inspiration — if Above and Beyond's config becomes accessible, it could serve as validation.

## Currency-as-Reward Scope (MP36 Validation)

**Observation:** MP36 was identified from 2 packs (GT-O, NFwC). Phase 3 confirms:
- GT-O: copper_coin rewards in stoneage chapter, shop chapter as currency sink
- NFwC: lightmanscurrency coins throughout, 42 references in boss chapter
- TWR: frostedheart:insight as progression currency (different implementation, same concept)

**Validation status:** 3 packs now exhibit currency-like reward patterns, but with different implementations:
1. GT-O: item-type currency (copper_coin) with dedicated shop chapter
2. NFwC: item-type currency (lightmanscurrency) with trade stations
3. TWR: custom-type currency (frostedheart:insight) with skill/progression system

**Conclusion:** MP36 is validated by 2 packs (GT-O, NFwC) using standard item-type currency. TWR's insight system is a variant that extends the concept to custom reward types. MP36 can be upgraded to "multi-source" confidence.
