# Review A: Cycle 4 Universality Audit

**Reviewer:** A (Generalizability)
**Date:** 2026-07-07
**Scope:** Cycle 4 additions/modifications: R33, MP34 rewrite, Shape semantics conclusion, R34 draft, PP7 upgrade
**Data sources reviewed:** mod-reward-design.md, mod-dependency-graph.md, mod-item-reachability.md, module-index.md, reward-table-rules-R33-R35_2026-07-07.md, mod-atm-signature.md, previous review-a audits

---

## Audit Item 1: R33 -- Reward Table Reference Integrity

**Location:** mod-reward-design.md, lines 256-273

### Generalizability Rating: **B** (Most packs applicable, with exceptions)

### Evidence Base

R33 is derived from deep config analysis of **3 packs**: Craftoria (19 reward tables), MI:Foundation (29 tables), Enigmatica 10 (28 tables). These are all MC 1.21.x kitchen-sink/curated packs using the JSON5 format with `reward_tables/*.snbt` files.

### Universality Questions

**1. Does R33 apply to packs that don't use reward_tables at all?**

Yes, but vacuously. The rule only triggers when `reward.type in ("random", "loot", "choice")`. If a pack uses exclusively `item` and `xp` rewards (which is the case for many expert packs like Monifactory, and most Create packs), R33 never fires. The rule is self-scoping and harmless for packs without reward tables.

**2. Does the reward_tables system exist across all MC versions?**

This is the critical gap. The three source packs are all MC 1.21.x / FTB Quests 26.x using JSON5 on-disk format. The SKILL.md format detection (lines 56-59) establishes that MC 1.20.1 packs use SNBT format with FTB Quests 2001.4.17. The reward table file format (`config/ftbquests/quests/reward_tables/*.snbt`) has been observed in both JSON5 and SNBT packs -- the draft document shows SNBT-format reward table examples from both Craftoria and E10 (lines 90-115). However, the **existence** of the reward_tables directory in 1.20.1 SNBT packs has not been verified. Create: Delight (the primary 1.20.1 SNBT reference pack) does not appear in the reward table analysis at all, suggesting it may not use the system.

**3. Is this a kitchen-sink-only feature?**

The three source packs are all kitchen-sink or curated-kitchen-sink. Expert packs (Monifactory, E9E) tend to use deterministic `item` rewards for precise recipe gating. Create packs (Create: Delight, Mechanomania) have very low reward density (0.11-0.43/quest per mod-atm-signature.md) and likely don't invest in reward table authoring. RPG/adventure packs are unrepresented.

### Verdict

R33's **mechanism** (reference integrity check) is universally sound -- any pack that uses `table_id` references should validate them. The rule is self-scoping (only triggers on random/loot/choice types) and P1-severity is appropriate (silent reward failure is a real user impact). However, the **empirical validation** only covers 3 kitchen-sink packs on MC 1.21.x.

### Recommendations

1. **Add a scope note to R33:** "Validated on MC 1.21.x JSON5 packs (Craftoria, E10, MI:Foundation). Expected to apply to SNBT packs using the same FTB Quests reward table system, but SNBT-format reward tables have not been independently audited."
2. **Add a data-collection TODO:** Verify reward_tables directory existence and `table_id` referencing in at least one MC 1.20.1 SNBT pack (Create: Delight or a similar pack) before claiming cross-version validity.
3. **Consider adding a "skip" annotation:** "If the pack uses no `random`, `loot`, or `choice` rewards (common in expert and Create packs), R33 does not apply."
4. **The Pack types column in Quick Reference currently says "all"** -- this is technically correct (the rule won't harm non-users) but practically misleading. Consider changing to "all (relevant when reward_tables used)" or adding a footnote.

---

## Audit Item 2: MP34 Rewrite -- Loot Table Reward (unified system)

**Location:** mod-reward-design.md, lines 77-134

### Generalizability Rating: **B-** (Likely universal within JSON5; uncertain for SNBT)

### Evidence Base

The Cycle 4 correction states that `random`, `loot`, and `choice` all use the **same FTB Quests internal reward table system** (`table_id` -> `reward_tables/*.snbt`). This conclusion is drawn from config analysis of Craftoria, MI:Foundation, and Enigmatica 10 -- all MC 1.21.x / JSON5 format.

### Universality Questions

**1. Is the unified reward table system the same in SNBT (MC 1.20.1)?**

The draft document (reward-table-rules-R33-R35, lines 10-18) states the correction as if it applies universally: "Both `type: 'random'` and `type: 'loot'` reference the same internal FTB Quests reward table system." But all evidence comes from JSON5 packs. FTB Quests 2001.4.17 (the 1.20.1 version) may implement reward tables differently. The SNBT format uses different type identifiers (short form: `type: "item"` vs prefixed: `type: "ftbquests:item"` per SKILL.md line 65), which suggests the internal architecture may also differ.

**2. Is the previous incorrect claim ("loot references vanilla/mod loot table IDs directly") actually wrong for ALL versions?**

The previous claim might have been correct for an older FTB Quests version where `type: "loot"` did reference vanilla loot tables (e.g., `minecraft:chests/simple_dungeon`). FTB Quests has gone through significant refactoring between 1.20.1 and 1.21.x. The Cycle 4 correction may be over-correcting -- establishing the truth for 1.21.x and incorrectly back-projecting it to 1.20.1.

**3. Does the three-type taxonomy (random/loot/choice) exist in all versions?**

In older FTB Quests versions, `type: "loot"` might have had genuinely different semantics (referencing vanilla `LootTable` registry entries). The SNBT-format packs might use `loot` differently from JSON5 packs. Without checking a 1.20.1 pack's `loot` rewards, the unified-system claim is unverified.

### Verdict

The Cycle 4 correction is almost certainly **correct for MC 1.21.x / FTB Quests 26.x** (JSON5 format). But the document presents it as a universal truth about FTB Quests without version qualification. This is a significant risk because the skill generates configs for both formats (per SKILL.md line 4).

### Recommendations

1. **Add version qualification to the MP34 description:** "Confirmed for MC 1.21.x / FTB Quests 26.x (JSON5 format). In MC 1.20.1 / FTB Quests 2001.4.x (SNBT format), `type: 'loot'` may have different semantics -- verify against the target pack's config before assuming unified reward table system."
2. **Remove absolute language from the correction.** The phrase "factually wrong" (draft line 9) should be scoped: "wrong for MC 1.21.x JSON5 packs." The original claim may have been correct for the version it was written about.
3. **Flag as a testing priority:** Before generating `loot` rewards for a 1.20.1 SNBT pack, the skill should verify the pack's actual `loot` reward implementation rather than assuming the 1.21.x unified system.
4. **The cross-pack comparison table (lines 117-123) is valuable** but should explicitly note: "All three packs are MC 1.21.x / JSON5 format. No 1.20.1 SNBT pack was included in this analysis."

---

## Audit Item 3: Shape Semantics -- Pack-Specific Conclusion

**Location:** mod-dependency-graph.md, lines 307-319

### Generalizability Rating: **A** (the meta-conclusion is universal; the specific data is limited)

### Evidence Base

The conclusion "shape semantics are pack-specific, not universal" is based on a 21-pack dataset (per line 309) comparing ATM (hexagon), MI:Foundation (diamond), E10 (all default), Craftoria (minimal), and Monifactory (hexagon).

### Universality Questions

**1. Is the meta-conclusion correct?**

Yes. The observation that different packs assign different meanings to different shapes is **self-evidently true** from the data: ATM uses hexagon as tier marker, MI:Foundation uses diamond, E10 uses no shapes at all. This proves there is no universal shape standard. The meta-conclusion is robust regardless of sample size.

**2. Could there be finer-grained universality within pack series?**

The data table (line 313) explicitly shows that the **ATM series (ATM-8/9/10/10-Sky)** all use hexagon as dominant shape. This suggests intra-series consistency. The conclusion acknowledges this indirectly by listing "ATM series" as a single row, but doesn't explicitly state the sub-finding: "Shape semantics are consistent within the ATM series, and likely within other pack series, but not across series."

This is a missed nuance. The correct statement is:
- **Cross-pack:** No universal shape standard (A-grade conclusion)
- **Within-series:** Shape semantics likely consistent (B-grade -- only ATM series has enough data to verify)
- **Within-pack:** Shape semantics should be internally consistent (basis for R35 draft)

**3. Is "ZERO shape definitions" for E10 reliable?**

The claim that Enigmatica 10 has zero shape definitions is strong. If E10 is a large pack (28 reward tables suggests significant content), having truly zero shape overrides would be notable. This could also mean the data extraction missed default_quest_shape fields set at the chapter level.

### Verdict

The core conclusion is sound and universally applicable. The practical implication ("inherit the pack's established shape vocabulary") is good advice for any pack. The missed nuance about intra-series consistency is a minor gap.

### Recommendations

1. **Add the intra-series sub-finding:** "Within a pack series (e.g., ATM-8/9/10/10-Sky), shape semantics tend to be consistent. When generating for an existing series, use the series' established shape vocabulary."
2. **Soften "ZERO shape definitions" for E10:** Change to "E10 uses default shape throughout (no explicit per-quest shape overrides observed)" to be precise about what was measured.
3. **The config implication (line 319) is well-stated** and universally applicable. No change needed.
4. **Add a caveat about R35 (shape consistency check):** "R35 checks intra-pack consistency but cannot validate whether the chosen semantics are 'correct' -- only that they are applied uniformly."

---

## Audit Item 4: R34 Draft -- Reward Type Consistency Within Pack

**Location:** reward-table-rules-R33-R35_2026-07-07.md, lines 52-74

### Generalizability Rating: **C** (Specific interpretation of "consistency"; design choice, not error)

### Evidence Base

R34 is derived from 3 packs: Craftoria (99% `random`), E10 (99.6% `loot` with 2 `random` anomalies), MI:Foundation (item-dominant). The rule flags mixed `random` + `loot` usage as an authoring inconsistency.

### Universality Questions

**1. Is mixing `random` and `loot` actually a problem?**

This is the most questionable assumption in the Cycle 4 additions. R34 treats consistency as inherently desirable, but consider legitimate reasons for mixing:

- **Thematic chapters:** A tech chapter with deterministic item rewards + random bonus loot; an adventure chapter with loot crates as dungeon rewards. Different chapters, different reward philosophies, same pack.
- **Progression-based mixing:** Early-game uses `random` (low-stakes variety); endgame uses `loot` (player gets to open crates for rare items, adding excitement to high-value rewards).
- **Authorial intent:** The pack author may deliberately use `random` for "background" rewards and `loot` for "event" rewards within the same pack.

**2. Is the E10 malum chapter evidence actually an error?**

R34 cites E10's malum chapter having 2 `random` among all `loot` as "likely authoring error." But we also see in the MP34 description (line 131) a confirmed E10 bug where `choice` was used instead of `random`. The malum `random` instances might be: (a) intentional exceptions for specific quests, (b) copy-paste errors from another chapter, (c) a deliberate test that was never cleaned up. Without asking the pack author (MuteTiefling), this is speculation.

The fact that E10 had ONE confirmed reward-type bug (choice vs random, issue #517) does not prove that ALL reward-type inconsistencies in E10 are bugs. It proves the type confusion is possible, not that every instance is wrong.

**3. What about packs where different authors write different chapters?**

In large kitchen-sink packs, different chapters are often written by different contributors. Craftoria and E10 both have multiple contributors. "Inconsistency" might simply reflect different authors' preferences rather than a single author's drift. R34 implicitly assumes a single-author model.

### Verdict

R34's core assumption -- that reward type consistency is desirable -- is a **design opinion**, not a universal rule. It's a reasonable opinion (consistency generally improves player experience), but the rule overreaches by:
1. Flagging ALL mixing as INFO-level issues, even when deliberate
2. Not providing a mechanism to distinguish intentional mixing from authoring errors
3. Deriving its threshold from 3 packs that happen to each use one dominant type

### Recommendations

1. **Downgrade severity or add an opt-out:** R34 should either remain at INFO (it already is P2/INFO, which is acceptable) or add a configuration option to suppress it for packs that explicitly declare mixed reward strategies.
2. **Reframe the rule's purpose:** Change from "detects mixed usage...which suggests authoring inconsistency" to "reports reward type distribution -- significant outliers in a single chapter may indicate authoring drift." This shifts from "mixing is wrong" to "outliers are worth checking."
3. **Add chapter-level granularity:** Instead of pack-level mixing detection, flag individual chapters where the reward type differs from the pack's dominant type. This catches the E10 malum anomaly without flagging legitimate cross-chapter diversity.
4. **Add an escape hatch:** "If the pack deliberately uses different reward types for different chapter themes (e.g., tech chapters use `random`, adventure chapters use `loot`), this is a valid design choice and not an authoring error."
5. **The E10 #517 reference should be separated:** The confirmed choice-vs-random bug is evidence for R33 (wrong table_id) and R12 (correct reward type), not for R34 (mixing types across chapters). Don't conflate within-quest type errors with across-pack type diversity.

---

## Audit Item 5: PP7 Upgraded to Systematic Issue

**Location:** mod-item-reachability.md, lines 97-114

### Generalizability Rating: **B+** (Broadly applicable to multi-mod packs; question of responsibility)

### Evidence Base

PP7 was originally documented with FTB Skies 2 #11432. Cycle 4 added 4 more cases:
- ATM-10 #4210 (Refined Storage vs Extra Disks vs ExtraStorage)
- ATM-9 #2322 (IE ethanol vs ChemLib ethanol)
- Architect's Exodus #12614 (Tinker's Construct variants)
- The original FTB Skies 2 #11432 (FTB Materials vs Modern Industrialization steel dust)

That's **4 packs across 3 independent teams** (AllTheMods, FTB team, Architect's Exodus authors), covering kitchen-sink and curated pack types.

### Universality Questions

**1. Is this truly a "systematic issue" or a known limitation of modded Minecraft?**

The claim that PP7 is "systematic" (confirmed in 5+ packs) is accurate in terms of occurrence, but the question is whether it's:
- (a) A **pack author responsibility** that the skill should help detect, or
- (b) An **FTB Quests mod limitation** that should be fixed upstream, or
- (c) A **modpack platform issue** (Forge/Fabric tag unification failure)

The evidence suggests (a) is the current practical reality -- FTB Quests matches items by exact `modid:item_name`, not by tags. Pack authors must manually ensure namespace consistency. The skill detecting this is valuable regardless of who "should" fix it.

**2. Does the 5+ pack count represent true universality or kitchen-sink specificity?**

All 4 cited cases come from kitchen-sink or curated packs with 100+ mods. Small packs (5-20 mods, like focused Create packs) rarely have overlapping item namespaces. Expert packs typically have tight mod selections with clear role assignments per mod. The mod-unification trap is fundamentally a **mod-count problem**: the more mods, the more overlapping items.

However, even focused packs can encounter this when two mods provide the same material (e.g., a Create pack with both Create and Create: Additions providing similar intermediates). So the issue scales with mod overlap, not just mod count.

**3. Is "FTB Quests should handle mod unification" a valid counter-argument?**

Yes, partially. FTB Quests could support tag-based item matching (`#forge:dusts/steel` instead of `modernindustrialization:steel_dust`). Many task types in modern FTB Quests DO support tag matching. But the documented cases show that pack authors still use exact-ID matching (either by habit, lack of awareness, or because tag-based matching has other trade-offs). Until FTB Quests enforces or defaults to tag matching, PP7 remains a pack-author concern.

**4. Are the 5+ packs truly independent validation?**

ATM-10 and ATM-9 are from the same team (AllTheMods). FTB Skies 2 is from the FTB team. Architect's Exodus is independent. So we have 3 independent teams, which is adequate but not overwhelming. The pattern is well-established across the modded MC community though -- this is one of the oldest known issues in modpack authoring.

### Verdict

PP7's upgrade to "systematic" is justified by the evidence. The 4 cited cases span 3 independent teams and multiple Minecraft versions. The underlying mechanism (exact-ID matching in a multi-mod environment) is universal for kitchen-sink packs. The question of "whose responsibility" doesn't affect the rule's validity -- regardless of who should fix it, the skill detecting the issue is valuable.

### Recommendations

1. **The "systematic" upgrade is justified.** No change needed to the severity or scope.
2. **Add a mod-count threshold note:** "PP7 risk scales with mod count and namespace overlap. Packs with 50+ mods and overlapping material namespaces (common in kitchen-sink) are at highest risk. Focused packs with <20 mods rarely encounter this."
3. **Add a forward-looking note about tag-based matching:** "Some FTB Quests versions support tag-based item tasks (`#forge:ingots/steel`). Where available, tag-based matching eliminates PP7 entirely. Consider recommending tag-based tasks in the Step 2 interview for multi-mod packs."
4. **The "whose responsibility" question should be addressed explicitly:** "PP7 exists because FTB Quests matches items by exact namespace. While tag-based matching would eliminate this upstream, current practical mitigation is the pack author's responsibility. This rule helps detect the issue during quest generation."
5. **Cross-reference PP7 with PP6 (Wrong Tool Reward):** Both stem from mod-namespace confusion in multi-mod environments. PP6 focuses on tools (wrench variants), PP7 focuses on materials (dust/ingot variants). Consider merging their detection logic in Step 5.

---

## Summary Table

| Audit Item | Rating | Source Packs | Source Teams | Key Limitation | Action Priority |
|---|---|---|---|---|---|
| **R33** Reward Table Reference Integrity | **B** | Craftoria, E10, MI:Foundation | 3 teams | No SNBT/1.20.1 validation; vacuously applies to non-users | MEDIUM -- add version scope note |
| **MP34** Loot Table unified system | **B-** | Craftoria, E10, MI:Foundation | 3 teams | All evidence from JSON5/1.21.x; may not apply to SNBT/1.20.1 | HIGH -- add version qualification |
| **Shape semantics** pack-specific | **A** | 21-pack dataset | Multiple | Meta-conclusion robust; missed intra-series nuance | LOW -- add sub-finding |
| **R34** Reward Type Consistency | **C** | Craftoria, E10, MI:Foundation | 3 teams | Design opinion, not universal rule; legitimate mixing exists | HIGH -- reframe and add opt-out |
| **PP7** Mod-Unification systematic | **B+** | ATM-10, ATM-9, FTB Skies 2, Arch Exodus | 3 teams | Kitchen-sink specificity; mod-count dependent | LOW -- add threshold note |

---

## Cross-Cutting Findings

### Finding 1: Kitchen-Sink Dominance in Cycle 4 Data

All five Cycle 4 additions draw primarily or exclusively from kitchen-sink/curated packs:
- R33/MP34/R34: Craftoria, E10, MI:Foundation (all kitchen-sink or curated)
- Shape semantics: Adds ATM and Monifactory, but the new data is still kitchen-sink-heavy
- PP7: Adds ATM-10, ATM-9 (kitchen-sink), FTB Skies 2 (skyblock-kitchen-sink)

**Expert packs** (Monifactory, E9E) are notably absent from the reward-table analysis despite being referenced elsewhere in the skill. **Create packs** (Create: Delight, Mechanomania) are absent from both the reward-table and shape-semantics new data. **RPG/adventure** packs remain unrepresented.

This is consistent with the dataset skew identified in review-a-universality_2026-07-06.md (section 0): ATM + kitchen-sink packs dominate the quantitative data.

### Finding 2: MC 1.21.x / JSON5 Format Bias

The reward-table system analysis (R33, MP34, R34) is entirely based on MC 1.21.x / JSON5 format packs. The skill explicitly supports both JSON5 and SNBT formats (SKILL.md lines 54-97), but Cycle 4's new rules have no SNBT validation. This is a meaningful gap because:
- Reward table file paths might differ between versions
- `type: "loot"` semantics might differ in FTB Quests 2001.4.x vs 26.x
- SNBT-format packs may not have a `reward_tables/` directory at all

### Finding 3: Independence of Design Teams

Cycle 4's three primary source packs (Craftoria, E10, MI:Foundation) represent **3 independent authoring teams**, which is better than the ATM-series-only data that plagued earlier cycles (review-a-universality_2026-07-06.md section 4). However, all three are the same **pack type** (kitchen-sink/curated for MC 1.21.x). Independence of team does not equal independence of design philosophy -- three kitchen-sink authors may converge on similar patterns simply because the genre demands it.

---

## Action Items (Prioritized)

### HIGH Priority

1. **MP34 -- Add MC version qualification.** The unified reward table system claim must specify "confirmed for MC 1.21.x / FTB Quests 26.x" to prevent incorrect assumptions when generating for 1.20.1 SNBT packs. This is a correctness issue that could cause the skill to generate wrong configs.

2. **R34 -- Reframe from "inconsistency detection" to "distribution reporting."** The current framing assumes mixing is wrong. Add an opt-out for packs with deliberate mixed strategies, and shift detection from pack-level to chapter-level outliers.

### MEDIUM Priority

3. **R33 -- Add version scope note and SNBT verification TODO.** Less urgent than MP34 because R33 is self-scoping (harmless when not applicable), but the SNBT gap should be documented.

4. **Add data-collection priorities:** The next cycle should explicitly target:
   - At least one MC 1.20.1 SNBT pack for reward table validation
   - At least one expert pack (Monifactory or E9E) for reward economy comparison
   - At least one focused Create pack for reward density baseline

### LOW Priority

5. **Shape semantics -- Add intra-series consistency sub-finding.** A minor nuance gap that doesn't affect rule behavior.

6. **PP7 -- Add mod-count threshold note.** The systematic upgrade is justified; the note is for user guidance rather than rule correctness.

7. **R33 Quick Reference -- Change "all" to "all (relevant when reward_tables used)."** Cosmetic improvement to set correct expectations.
