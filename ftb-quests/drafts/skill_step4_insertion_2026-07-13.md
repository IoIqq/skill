# Draft: Step 4 Genre-Specific Progression Validation Forced Reasoning

> **Date:** 2026-07-13
> **Target:** SKILL.md Step 4 (per-node loop)
> **Risk:** HIGH — adds mandatory reasoning gates that block spec writes; changes generation-time behavior for all pack types
> **Cycle:** 13 Phase 3

---

## Insertion Point 1A: After Gate 1's R42 additional check

**Location:** SKILL.md line ~458, after the paragraph beginning "Note: this is a semantic reinforcement of Gate 1..." and before "**Gate verdict:**" (line ~454).

**Insert the following text AFTER the R42 scope note paragraph and BEFORE the `**Gate verdict:**` line:**

```markdown
   **Genre-Specific Resource Chain Checks (Cycle 13 — R73–R81 activation):**

   When the pack's `pack_type` matches a genre below, Gate 1 additionally triggers the corresponding genre-specific rules from `reference/design/progression-rules.md` §Section B.3. These rules are EXTENSIONS of the R1–R4 + R42 checks, not replacements — they add genre-environment constraints that generic item reachability cannot capture.

   | pack_type | Rules activated | What to check per task item |
   |---|---|---|
   | **skyblock** | R73, R76, R79, R81 | (R73) Is the item's crafting chain origin a skyblock-native source — sievable, farmable, mob-drop, crystallization? Ask user for sieve config path. (R76) Is the item obtainable through ≥2 distinct skyblock resource paths, or is the required path documented in the description? (R79) If the item requires a multiblock structure, does the player have space-expansion access at this progression point? (R81) Do cross-mod processing chains create an unintended shortcut past the current stage gate? |
   | **adventure** / **rpg** | R74, R77, R80 | (R74) If the task is a boss `kill`, does the prerequisite chain provide equipment at tier ≥ boss_tier − 1? Ask user for boss tier mapping. (R77) Does the quest description include equipment recommendations or tactical hints for the boss fight? (R80) If this is a side-branch quest, does it depend on main-branch quests more than 3 hops past the divergence point? |
   | **farming** / **lifestyle** | R75, R78 | (R75) If the task requires a seasonal crop, is the crop's season reachable within the quest chain's expected timing? Ask user for seasonal crop config. (R78) In a non-combat pack, does every combat-only item have a peaceful acquisition alternative (trading, farming, crafting)? |

   **Execution protocol:** For each activated rule, produce a one-line reasoning in working notes:
   > Genre check [Rxx]: [item_id] → [pass/fail/defer with reason]

   If the rule requires external data not available during generation (sieve config, boss tier map, seasonal crop data), mark `[unverified:genre_<rule_id>]` (e.g., `[unverified:genre_R73]`) and continue — the formal check runs in Step 5 when the full graph and external tool outputs are available. If the rule fails on available data, apply the same Gate 1 FAIL protocol: do NOT write the task, suggest an alternative or ask the user.
```

---

## Insertion Point 1B: After Gate 2's R45 additional check

**Location:** SKILL.md line ~483, after the paragraph beginning "Note: this is a semantic reinforcement of Gate 2..." and before "**Backward matching (Step 4 practical note):**" (line ~485).

**Insert the following text AFTER the R45 note paragraph and BEFORE the `**Backward matching**` paragraph:**

```markdown
   **Genre-Specific Reward Anti-Pattern Checks (Cycle 13 — AP6/AP30–AP35 activation):**

   When the pack's `pack_type` matches a genre below, Gate 2 additionally checks rewards against the genre-specific anti-patterns from `reference/design/anti-patterns.md` (AP30–AP35) and the general dead-end anti-pattern AP6 from `reference/design/mod-reward-design.md`. These anti-patterns describe genre-environment reward failures that the four-category classification above cannot catch alone.

   | pack_type | Anti-patterns to check | Per-reward question |
   |---|---|---|
   | **all packs** | AP6 (Dead-End Reward) | Does this reward item appear as a task requirement in ANY downstream quest, or qualify as a universal bridge / terminal reward? If not → dead-end risk, apply Gate 2 FAIL protocol. |
   | **skyblock** | AP30 (Resource Bottleneck Death Spiral), AP35 (Resource Inflation) | (AP30) Does this reward create a circular bottleneck where the mesh upgrade needed to obtain the reward's item is gated behind the very chain this reward supports? (AP35) Will this reward's item be trivially mass-producible via automated sieving, making the quest's effort-reward balance collapse? |
   | **adventure** / **rpg** | AP31 (Boss Equipment Mismatch), AP34 (Reward Desync) | (AP31) If this reward is equipment for a boss fight, is the equipment tier calibrated to the NEXT boss's difficulty, not the previous one? (AP34) If this reward uses command delivery for an expensive item submission, is the command robust against server-crash desync? |
   | **farming** / **lifestyle** | AP32 (Season-Time Conflict), AP33 (Incomplete Shipment) | (AP32) If this reward is a season-dependent crop or season-changing item, does the timing align with the next quest's expected season? (AP33) If this quest is part of a WIP chapter, are all placeholder rewards flagged as optional or hidden? |

   **Execution protocol:** For each activated anti-pattern, produce a one-line reasoning in working notes:
   > AP check [APxx]: [reward_item] → [pass/fail/not_applicable]

   Anti-pattern checks are advisory (WARNING level) during generation — they surface risks in the Step 7 summary for the user to evaluate. The formal AP validation runs in Step 5 with full graph context. Exception: AP6 (dead-end reward) remains blocking at generation time per the existing Gate 2 FAIL protocol above.
```

---

## Risk Assessment

| Risk | Level | Explanation |
|---|---|---|
| Behavioral change | **HIGH** | Adds mandatory per-node reasoning for genre-specific packs; increases generation-time token spend per node |
| False positive risk | **MEDIUM** | Genre-specific rules require external data (sieve config, boss tiers) that may not be available; the `[unverified:genre_*]` fallback mitigates blocking but adds noise |
| Backward compatibility | **LOW** | Non-genre packs (kitchen-sink, expert without genre tag) are unaffected — the rules only activate when `pack_type` matches |
| Integration with existing gates | **LOW** | The insertions are additive extensions within existing Gate 1/Gate 2 structure, not structural changes |
| Testing impact | **MEDIUM** | Genre-specific packs need new test cases: skyblock sieve config mock, adventure boss tier mock, farming season config mock |

## Migration Note

This insertion references `pack_type` which is collected in Step 2 (the interview). If `pack_type` is not explicitly declared, the genre-specific rules do not activate. The Step 2 interview should be updated to always collect `pack_type` (currently optional for kitchen-sink packs). This is a dependency for the draft to function correctly.
