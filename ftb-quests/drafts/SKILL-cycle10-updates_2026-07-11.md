# SKILL.md Cycle 10 Updates Draft

> **Status:** DRAFT — not yet applied to SKILL.md
> **Date:** 2026-07-11
> **Source:** Cycle 10 Phase 4 review (3 reviewers), Phase 5 integration plan
> **Risk level:** HIGH — core workflow modifications; requires Phase 6 sign-off before applying

---

## Overview

Phase 4 reviewers evaluated 9 new items (R51-R54, AP21, AP22, MP43-MP45) from a 54-pack research corpus. Consensus: 4 items are PRACTICAL/ADAPTIVE and ready for integration; 5 are THEORETICAL/SKIP. Three conflict resolutions are required.

### Integration Summary

| Item | Verdict | Integration Target | Priority |
|---|---|---|---|
| R51 Reward Architecture Role Alignment | PRACTICAL | Step 2 (after R46) | HIGH — resolves terminology conflict |
| AP22 Config-Drift Description Staleness | ADAPTIVE | Quest text writing section | MODERATE |
| R52 Unlock Leniency Declaration | ADAPTIVE | Step 5 summary | MODERATE |
| R54 Named Reward Table Semantic Match | ADAPTIVE | Step 5 check | MODERATE |
| R53 Task Complexity Utility Proportionality | SKIP | — | Requires recipe graph data |
| MP43 NPC Questline Economy Gate | THEORETICAL | — | Design reference only |
| MP44 XP Investment Feedback Loop | THEORETICAL | — | Conflicts with AP17 |
| MP45 Bilingual Authoring | PRACTICAL (limited) | — | Only for bilingual packs |
| AP21 Version-Maturity Mismatch | SKIP | — | Beyond agent control |

---

## Modification 1: R51 — Reward Architecture Role Alignment

### Location
**Step 2**, insert immediately after the existing R46 questbook role bullet (after the line "This declaration determines R47 and R50 applicability downstream.")

### Rationale
Phase 4 Reviewer A identified that R46 and R51 use **incompatible role taxonomies**. R46 uses "Companion / Tutorial System / Incentive Catalog" while R51 uses "Companion / Guide / Hybrid." This creates contradictory instructions at Step 2. The fix unifies terminology and cross-references R50's safety conditions.

### Existing text (anchor point — line ~280 in SKILL.md)
```
  This declaration determines R47 and R50 applicability downstream.
```

### Insert AFTER that line:

```markdown
- **Reward architecture alignment (R51) — MANDATORY after R46:** Check that the reward model matches the declared questbook role. Use the SAME role names declared in R46:

  | Declared role (from R46) | Expected reward model | Deviation triggers |
  |---|---|---|
  | **Companion (伴生导航)** | Zero rewards OR XP-only | Item rewards → INFO: "Consider delegating to EMI/JEI instead" |
  | **Tutorial System (教程系统)** | XP drip + occasional milestone items | Zero rewards → WARNING: "Tutorial packs need reward feedback to reinforce learning" |
  | **Incentive Catalog (激励目录)** | Generous item rewards per quest | Zero rewards → WARNING: "Incentive catalog without incentives" |
  | **Hybrid (混合模式)** | Per-chapter alignment — each chapter's role is checked individually | Per-chapter role not declared → WARNING: "Hybrid mode requires per-chapter role assignment" |

  **IMPORTANT — R50 interaction:** A Companion pack with zero rewards passes R51 ("zero rewards are OK for companion") but must ALSO pass R50 (Zero-Reward Safety: alternative currency + companion/catalog role + intrinsic loop). R51 validates role-reward alignment; R50 validates the broader zero-reward safety conditions. Both must pass for safe zero-reward design.

  **Tolerance:** Up to 10% of quests may deviate from the expected reward model without triggering a warning (accommodates special milestone events and intentional exceptions).
```

### Conflict Resolution Notes
1. **R51↔R46 terminology unified:** "Guide" → "Incentive Catalog"; "Hybrid" retained as R46's fourth option with per-chapter requirement.
2. **R51↔R50 overlap resolved:** Explicit cross-reference added; R51 is the alignment check, R50 is the safety check.
3. **10% tolerance added:** Reviewer A noted R51 had no deviation tolerance for special events.

---

## Modification 2: AP22 — Config-Drift Description Staleness

### Location
**Quest text & description writing style** section, insert after the existing AP10/AP11 mention (after the line ending "…and reward structure across the chapter.")

### Rationale
Phase 4 reviewers classified AP22 as ADAPTIVE. When quest configs are modified (item counts changed, dependencies rewired, rewards swapped) but descriptions still reference the old configuration, the quest book loses trustworthiness. This is especially relevant for the generator's `--mode preserve` workflow where user edits to configs may not update descriptions.

### Existing text (anchor point — line ~46 in SKILL.md)
```
**AI-specific style risks.** When generating many quests in sequence, watch for style homogenization (AP10) and narrative inconsistency (AP11) — both are documented in `reference/design/mod-description-trust.md §AP9–AP11`. Step 4's self-check step catches these per-node; vary description mode (how-to / lore / tip / challenge) and reward structure across the chapter.
```

### Insert AFTER that paragraph:

```markdown
**Config-drift staleness (AP22).** When a quest's config changes — item count adjusted, reward swapped, dependency rewired, task type changed — but the description still references the old configuration, the description becomes actively misleading. This is the most common source of AP1 (description-reality mismatch) in maintained packs. Watch for it in three scenarios:
1. **Post-edit drift:** User or `--mode ask` edit changes a quest's tasks/rewards, but the description from a prior generation still describes the original config. After any config edit, re-read the description and confirm it matches the current config.
2. **Batch-regeneration drift:** `generate_quests.py --mode preserve` protects untouched quests' configs but does NOT update descriptions to reflect changes elsewhere (e.g., a reward table was renamed, a linked quest was removed). Run the Step 6 description-item consistency check (R23) after any batch regeneration.
3. **Port drift (R48 interaction):** Quests ported from another pack inherit descriptions referencing the source pack's config. The port drift indicators (R48) in Step 5 flag these systematically.
Trigger threshold: any config change to `tasks[]`, `rewards[]`, `dependencies[]`, or `count` on a quest that has a non-empty `quest_desc` should prompt a description review.
```

---

## Modification 3: R52 — Unlock Leniency Declaration

### Location
**Step 5**, insert into the statistics summary block, after the existing "Zero-reward safety (R50)" block (after the line ending "Result: {SAFE / WARNING — missing conditions: ...}").

### Rationale
Phase 4 reviewers classified R52 as ADAPTIVE. The `dependency_requirement` field (`one_started` vs `all_completed`) is fully checkable from config data. The declaration helps players understand the pack's progression philosophy. Reviewer B noted the 70% threshold triggers for only 1/54 packs (DeceasedCraft), so genre-convention exceptions are added.

### Existing text (anchor point — line ~577 in SKILL.md)
```
   Result: {SAFE / WARNING — missing conditions: ...}
```

### Insert AFTER the R50 zero-reward safety block (after the closing ```):

```markdown
**Unlock leniency declaration (R52) — print when detected:**
```
🔓 Dependency requirement distribution:
   all_completed: {count} ({pct}%)  |  one_started: {count} ({pct}%)
   {if skew >70% toward one type}:
   ⚠️ Skewed toward {dominant_type} ({pct}%).
   {if expert pack and all_completed >70%}: ✅ Consistent with expert pack convention.
   {if kitchen-sink and one_started >70%}: ✅ Consistent with kitchen-sink convention.
   {if NOT genre-default}: Consider adding a leniency declaration to the questbook introduction:
     "This pack {allows alternative paths / requires full completion / mixes both approaches}."
   {also check per-chapter}: Chapter "{name}" has {pct}% {type} skew — consider chapter-level note.
```

The declaration is advisory (INFO-level), not blocking. Genre-default packs (expert + all_completed, kitchen-sink + one_started/flexible) receive an affirmative note rather than a request to declare.

### Interaction with R41
R41 (Early-Game Flexible Mode) operates on `progression_mode` (linear/flexible), while R52 operates on `dependency_requirement` (one_started/all_completed). When `progression_mode: "default"` (linear) AND `dependency_requirement: "all_completed"` dominate, the pack is doubly gate-oriented — R52's output should note this combination.

---

## Modification 4: R54 — Named Reward Table Semantic Match

### Location
**Step 5**, insert into the validation section. Add as a new check after the existing whole-book validation paragraph (after "description consistency for every quest, command safety, team progression consistency, and chapter-level QA heuristics").

### Rationale
Phase 4 reviewers classified R54 as ADAPTIVE. It complements R33 (Reward Table Reference Integrity — structural check) by adding a semantic layer: does the table's name match its contents? The TIER_KEYWORDS dictionary is coarse but sufficient for flagging obvious mismatches.

### Existing text (anchor point — line ~533 in SKILL.md)
```
The whole-book validation runs the full progression-rules pipeline (R1–R32, distributed across the modular reference files — see `reference/design/module-index.md` for routing) — item reachability across the complete dependency graph, reward continuity across all chapters, teaching order for every chapter, description consistency for every quest, command safety, team progression consistency, and chapter-level QA heuristics. The Step 4 per-node checks are a generation-time subset; Step 5 catches cross-quest and cross-chapter issues that only become visible once the full graph exists.
```

### Replace with:

```markdown
The whole-book validation runs the full progression-rules pipeline (R1–R32, distributed across the modular reference files — see `reference/design/module-index.md` for routing) — item reachability across the complete dependency graph, reward continuity across all chapters, teaching order for every chapter, description consistency for every quest, command safety, team progression consistency, chapter-level QA heuristics, **and reward table semantic naming (R54)**. The Step 4 per-node checks are a generation-time subset; Step 5 catches cross-quest and cross-chapter issues that only become visible once the full graph exists.
```

### Then add to the Step 5 summary output block (after the R52 block from Modification 3):

```markdown
**Reward table semantic check (R54) — print only when issues detected:**
```
🏷️ Reward table semantic check:
   {for each reward table}:
   Table "{name}": {item_count} items, estimated tier: {early/mid/late/endgame}
   {if name implies different tier than contents}: ⚠️ Name-content mismatch: "{name}" suggests {name_tier} but contents are {content_tier}.
   {if name is generic (table1, test, default, rewards)}: ⚠️ Generic table name "{name}" — consider a descriptive name.
   {if intentional mystery name (mystery, random, unknown)}: ℹ️ Opaque name "{name}" — assumed intentional.
   {if table has <3 or >30 items}: ℹ️ Table size advisory: "{name}" has {n} items.
```

The check uses a tier-keyword heuristic (TIER_KEYWORDS: early = "wooden/stone/iron/basic", mid = "steel/gold/diamond/advanced", late = "netherite/draconic/quantum", endgame = "creative/infinity/avaritia") plus mod namespace as a fallback proxy. Tables with intentional opaque names ("mystery_box," "random_reward") are exempted. R54 is P3 priority (advisory); R33 (structural integrity) remains P1.

---

## Modification 5: MP44-AP17 Contradiction Annotation

### Location
**Step 4**, in the R31 XP-level pre-check sub-gate (line ~469 in SKILL.md).

### Rationale
Phase 4 Reviewer C identified that MP44 (XP Investment Feedback Loop) recommends `xp_levels` for milestone rewards feeding a skill tree, while AP17 warns against `xp_levels` due to value volatility with player level. The contradiction needs an explicit annotation at the point where the agent encounters `xp_levels` rewards.

### Existing text (anchor point — line ~469 in SKILL.md)
```
   **R31 XP-level pre-check (sub-gate):** if the reward type is `xp_levels`, check whether this quest is a milestone/capstone (high fan-in, distinctive shape). Non-milestone `xp_levels` rewards drift in value with player level (AP17). If not a milestone, suggest flat `xp` instead or surface the risk to the user.
```

### Replace with:

```markdown
   **R31 XP-level pre-check (sub-gate):** if the reward type is `xp_levels`, check whether this quest is a milestone/capstone (high fan-in, distinctive shape). Non-milestone `xp_levels` rewards drift in value with player level (AP17). If not a milestone, suggest flat `xp` instead or surface the risk to the user. **MP44-AP17 interaction note:** MP44 (XP Investment Feedback Loop) recommends `xp_levels` for milestone rewards when the pack has a skill tree that absorbs XP as an investment currency — the skill tree mitigates AP17's value-drift concern because players spend XP before it devalues. If the pack has a skill tree or similar XP-sink mechanic, `xp_levels` milestone rewards are acceptable even for non-capstone quests; note this as an MP44 exception to AP17.
```

---

## Non-Integrations (documented for completeness)

### R53 — Task Complexity Utility Proportionality (SKIP)
**Reason:** Requires recipe graph data (downstream fan-out per item) that the skill currently lacks. The heuristic fallback (name-tier estimation) has unknown accuracy for 80%+ of items. Three critical exceptions (tutorial quests, consumable items, catalog quests) are needed before safe integration. Defer to a cycle that adds recipe graph analysis.

### MP43 — NPC Questline Economy Gate (THEORETICAL)
**Reason:** NPC quests are a niche pattern (only 2/54 packs use NPC gating). No bounds on quests-per-NPC or price calibration available. Useful as design reference only.

### MP44 — XP Investment Feedback Loop (THEORETICAL, annotated)
**Reason:** Contradicts AP17 on `xp_levels`. The contradiction is annotated in-place (Modification 5) rather than integrating MP44 as a standalone pattern. Full integration requires a skill-tree detection mechanism.

### AP21 — Version-Maturity Mismatch (SKIP)
**Reason:** Determining whether a pack's quest content implies a maturity level different from its stated version is beyond the agent's control — it requires human editorial judgment about content tone and difficulty.

### MP45 — Bilingual Authoring (PRACTICAL, limited scope)
**Reason:** Only relevant for bilingual packs. The existing SKILL.md language section already handles locale selection. MP45's main contribution — "author both simultaneously, not translate after" — is a process recommendation that doesn't change agent behavior. Translation drift (bilingual AP22) is noted in Modification 2's AP22 integration.

---

## Implementation Order (for Phase 6)

1. **Modification 1 (R51)** — highest priority, resolves the R46/R51 terminology conflict that actively confuses the Step 2 flow.
2. **Modification 5 (MP44-AP17 annotation)** — lowest effort, highest immediate value (prevents contradictory guidance at Step 4).
3. **Modification 2 (AP22)** — moderate priority, strengthens description accuracy checking.
4. **Modification 4 (R54)** — moderate priority, adds Step 5 semantic checking.
5. **Modification 3 (R52)** — lowest priority, advisory output only.

## Testing Notes

- Modification 1 (R51) should be tested against ATM-10 (hybrid role, multiple reward models) and Mechanomania (companion role, zero rewards) to verify the role-reward matrix produces correct verdicts.
- Modification 3 (R52) should be tested against DeceasedCraft (97% one_started — triggers) and Monifactory (expert, all_completed — genre-default exception).
- Modification 4 (R54) should be tested against Craftoria (uses named reward tables extensively) and ATM-10 (uses reward tables with loot crate pattern).
- Modification 5 (MP44-AP17) should be tested against a skill-tree pack (if available) to verify the exception logic.
