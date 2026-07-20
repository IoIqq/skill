# Draft: Cycle 13 New Module References in SKILL.md

> **Date:** 2026-07-13
> **Target:** SKILL.md (multiple reference lists and module routing paragraphs)
> **Risk:** HIGH — updates multiple cross-reference points in SKILL.md; incorrect routing could cause agents to miss or mis-load genre-specific rules
> **Cycle:** 13

---

## Summary of Cycle 13 Additions to reference/design/

Cycle 13 Phase 3 added the following content to the modular reference system:

| New content | File | Scope |
|---|---|---|
| **R73–R81** (Genre-Specific Progression Rules) | `progression-rules.md` §Section B.3 | Skyblock (R73/R76/R79/R81), Adventure (R74/R77/R80), Farming (R75/R78), Cross-mod (R81) |
| **AP30–AP35** (Genre-Specific Anti-Patterns) | `anti-patterns.md` | Skyblock (AP30/AP35), Adventure (AP31/AP34), Farming (AP32/AP33) |
| **Cases 21–27** (Skyblock/Adventure/Farming layout data) | `topology-coordinates.md` | 7 new real-pack cases from ATM9-Sky, ATM6-Sky, Dragoncraft, Life-in-the-Village-4, Ragnamod_VII, Gregitsky, Rogue Mayhem |
| **Section B.3 execution priority table** | `progression-rules.md` §Section C | Step 4/Step 5 priority assignments for R73–R81 |

---

## Insertion Point 3A: Update "Generation-time progression checks" paragraph

**Location:** SKILL.md line ~132, the paragraph beginning "**Generation-time progression checks.**" This paragraph lists the rules referenced during Step 4 generation.

**Current text (excerpt):**
```
The reasoning uses builtin lookup tables from `reference/design/shared-builtin-tables.md` and rules R1–R4 from `reference/design/mod-item-reachability.md`, R5(incremental)/R6(local)/R7 from `reference/design/mod-dependency-graph.md`, R10(reverse)/R28/R31 from `reference/design/mod-reward-design.md`, R14–R17/R18 from `reference/design/mod-teaching-pacing.md`, R22/R23 from `reference/design/mod-description-trust.md`; anti-pattern context from `reference/design/mod-description-trust.md §AP9–AP11`. See `reference/design/module-index.md` for the full routing table.
```

**Replace with:**
```
The reasoning uses builtin lookup tables from `reference/design/shared-builtin-tables.md` and rules R1–R4 from `reference/design/mod-item-reachability.md`, R5(incremental)/R6(local)/R7 from `reference/design/mod-dependency-graph.md`, R10(reverse)/R28/R31 from `reference/design/mod-reward-design.md`, R14–R17/R18 from `reference/design/mod-teaching-pacing.md`, R22/R23 from `reference/design/mod-description-trust.md`; genre-specific rules R73–R81 from `reference/design/progression-rules.md §Section B.3` (activated by `pack_type`: skyblock → R73/R76/R79/R81, adventure → R74/R77/R80, farming → R75/R78, cross-mod → R81); anti-pattern context from `reference/design/mod-description-trust.md §AP9–AP11` and `reference/design/anti-patterns.md §AP30–AP35` (genre-specific anti-patterns). See `reference/design/module-index.md` for the full routing table.
```

---

## Insertion Point 3B: Update "Anti-patterns to design against" paragraph

**Location:** SKILL.md line ~161, the paragraph beginning "**Anti-patterns to design against.**"

**Current text (excerpt):**
```
**Anti-patterns to design against.** Eleven recurring design mistakes are distributed across the modular reference files — from description-reality mismatch (AP1, the most damaging, in `reference/design/mod-description-trust.md`) through circular dependency deadlock (AP2, in `reference/design/mod-dependency-graph.md`) to the three AI-generation-specific risks (AP9–AP11, in `reference/design/mod-description-trust.md`). Load `reference/design/module-index.md` to find which module contains each anti-pattern. Load AP1–AP8 as background knowledge before Step 2; keep AP9–AP11 in mind during Step 4 generation.
```

**Replace with:**
```
**Anti-patterns to design against.** Recurring design mistakes are distributed across the modular reference files — from description-reality mismatch (AP1, the most damaging, in `reference/design/mod-description-trust.md`) through circular dependency deadlock (AP2, in `reference/design/mod-dependency-graph.md`) to the three AI-generation-specific risks (AP9–AP11, in `reference/design/mod-description-trust.md`) and six genre-specific anti-patterns (AP30–AP35, in `reference/design/anti-patterns.md`: skyblock resource bottleneck AP30 + inflation AP35, adventure boss equipment mismatch AP31 + reward desync AP34, farming season-time conflict AP32 + incomplete shipment AP33). Topology/layout anti-patterns (AP23–AP29) also live in `reference/design/anti-patterns.md`. Load `reference/design/module-index.md` to find which module contains each anti-pattern. Load AP1–AP8 as background knowledge before Step 2; keep AP9–AP11 in mind during Step 4 generation; load AP30–AP35 when `pack_type` is skyblock, adventure, or farming (Step 4 Gate 2 genre extension).
```

---

## Insertion Point 3C: Update "Micro-level authoring patterns" paragraph

**Location:** SKILL.md line ~187, the paragraph beginning "**Micro-level authoring patterns**"

**Current text (excerpt, last sentence):**
```
For topology-aware layout rules (R55–R64), coordinate algorithms, and real case data from 13 chapters across 9 packs, load `reference/design/topology-coordinates.md` and `reference/design/progression-rules.md` §Section B.
```

**Replace with:**
```
For topology-aware layout rules (R55–R64), coordinate algorithms, and real case data from 37 chapters across 25 packs (incl. 7 skyblock/adventure/farming cases from Cycle 13), load `reference/design/topology-coordinates.md` and `reference/design/progression-rules.md` §Section B. For genre-specific progression rules (R73–R81) covering skyblock resource chains, adventure boss equipment pacing, farming seasonal timing, and cross-mod shortcut detection, load `reference/design/progression-rules.md` §Section B.3.
```

---

## Insertion Point 3D: Update Step 5 validation pipeline description

**Location:** SKILL.md line ~559, the paragraph beginning "The whole-book validation runs the full progression-rules pipeline"

**Current text (excerpt):**
```
The whole-book validation runs the full progression-rules pipeline (R1–R32, distributed across the modular reference files — see `reference/design/module-index.md` for routing) — item reachability across the complete dependency graph, reward continuity across all chapters, teaching order for every chapter, description consistency for every quest, command safety, team progression consistency, and chapter-level QA heuristics.
```

**Replace with:**
```
The whole-book validation runs the full progression-rules pipeline (R1–R81, distributed across the modular reference files — see `reference/design/module-index.md` for routing) — item reachability across the complete dependency graph, reward continuity across all chapters, teaching order for every chapter, description consistency for every quest, command safety, team progression consistency, chapter-level QA heuristics, cross-cutting progression integrity (R65–R72), and genre-specific checks (R73–R81: skyblock resource chain R73/multi-path R76/space R79, adventure boss equipment R74/transparency R77/narrative timing R80, farming season timing R75/peaceful alternatives R78, cross-mod shortcuts R81). Genre-specific rules activate only when `pack_type` matches their applicability conditions.
```

---

## Insertion Point 3E: Update Step 5 topology validation section

**Location:** SKILL.md line ~561, after "**Topology validation (R55–R64 — Cycle 11 addition):**"

**Add the following paragraph AFTER the topology validation priority list (after line ~572, the "R60 (P3) Topology-Shape Vocabulary Coherence" line) and BEFORE the "Print topology validation results" code block:**

```markdown

**Genre-specific validation (R73–R81 — Cycle 13 addition):** After the topology pipeline, run genre-specific rules when `pack_type` matches. These rules require external data (sieve config, boss tier map, seasonal crop config); rules marked `[EXTERNAL_TOOL_REQUIRED]` run via external validation tool or downgrade to INFO when data is unavailable:

| Priority | Rule | Pack type | External data required |
|---|---|---|---|
| P1 | R73 Skyblock Resource Chain Reachability | skyblock | Sieve config (SieveRegistry.json) |
| P1 | R74 Adventure Boss Equipment Threshold | adventure | Boss tier map (BOSS_TIER_MAP) |
| P1 | R78 Collection Quest Item Attainability | farming | Recipe/loot table data |
| P2 | R75 Farming Season-Quest Timing | farming | Seasonal crop config |
| P2 | R76 Skyblock Multi-Path Redundancy | skyblock | Multi-path resource mapping |
| P2 | R77 Boss Kill Prerequisite Transparency | adventure | — (description keyword scan) |
| P2 | R79 Skyblock Space Constraint Compatibility | skyblock | Multiblock dimension data |
| P2 | R80 Adventure Multi-Branch Unlock Timing | adventure | — (dependency depth scan) |
| P2 | R81 Multi-Mod Resource Shortcut Detection | all (2+ processing mods) | Cross-mod recipe data |

Print genre-specific validation results as part of the summary:
```
Genre-specific validation: {pass/warn/error}
   Pack type: {pack_type} | Rules activated: {list}
   External data available: {yes/no — list missing data}
   R73–R81 violations: {count} | AP30–AP35 flags: {count}
```
```

---

## Risk Assessment

| Risk | Level | Explanation |
|---|---|---|
| Behavioral change | **HIGH** | Updates 5 separate locations in SKILL.md; each change affects which reference files get loaded and when |
| Accuracy risk | **HIGH** | If rule numbers, case numbers, or pack-type mappings are wrong, agents will load wrong references or miss critical rules |
| Backward compatibility | **LOW** | All changes are additive (extending existing rule lists, adding new paragraphs) — no existing references are removed |
| Consistency risk | **MEDIUM** | The "R1–R32" pipeline description (3D) must be updated to "R1–R81" to match; if missed, the pipeline description contradicts the actual rule set |
| Token impact | **MEDIUM** | Step 5 now loads genre-specific rules, adding ~300 lines of reference for genre-matched packs; non-genre packs unaffected |

## Verification Checklist

Before applying these changes:
- [ ] Confirm R73–R81 rule numbers match `progression-rules.md` §Section B.3
- [ ] Confirm AP30–AP35 numbers match `anti-patterns.md`
- [ ] Confirm Cases 21–27 exist in `topology-coordinates.md` with the pack names listed
- [ ] Confirm `pack_type` is collected in Step 2 interview (dependency for genre activation)
- [ ] Confirm module-index.md Scenario → Module Routing table includes the new R73–R81 and AP30–AP35 entries (may need separate module-index.md update)
