# Review A: Cycle 5 Universality Audit

**Reviewer:** A (Generalizability)
**Date:** 2026-07-08
**Scope:** Cycle 5 additions: MP35 Dual-Task Automation, MP36 Currency-as-Reward, MP37 Progress Catalog, MP38 Profession Chapter, Draft R36 Hardcore Zero-Optional, Draft R37 Kill Task Density
**Data sources reviewed:** micro-patterns.archive.md (MP35-MP38), hardcore-progression-rules-R36-R37_2026-07-08.md, mod-reward-design.md (MP36 cross-ref), module-index.md, review-a-universality_2026-07-07.md (format reference)

---

## Audit Item 1: MP35 -- Dual-Task Automation Verification

**Location:** micro-patterns.archive.md, lines 677-693

### Generalizability Rating: **C** (Narrow applicability, single-source)

### Evidence Base

MP35 is derived from **1 pack only**: Cabricality (expert/Create, 14 chapters). Phase 3 cross-pack comparison explicitly confirms: "No other pack in the 25-pack dataset uses the dual-task pattern." Create: Delight -- the closest comparison -- uses `consume_items: false` on some quests but **not** paired with an "automated" checkmark. Create: Astral uses `min_tasks: 1` for alternative paths but not dual-task verification.

### Universality Questions

**1. Is "automation verification" a general Create-pack design need?**

The underlying design question -- "how do you ensure the player built automation rather than hand-crafting?" -- is relevant to any Create-focused expert pack. But Cabricality's answer (dual-task: item + checkmark) is one of several possible solutions. Other Create packs solve this differently:
- Create: Delight uses tutorial quests + observation tasks to teach automation concepts without enforcing them
- Mechanomania uses linear progression with minimal rewards, making hand-crafting impractical at scale
- Create: Astral uses `min_tasks` for alternative recipe paths

The dual-task pattern is a **valid approach** to a **real design question**, but it is not the only approach, and no other pack has independently converged on it.

**2. Does the honor system undermine the pattern's value?**

The draft document acknowledges: "The honor system relies on player integrity; determined players can click the checkmark without building automation." This is a fundamental design weakness that limits the pattern's transferability. In hardcore packs where every task is a genuine skill check (see R36 draft), an honor-system checkmark would be antithetical to the design philosophy. In casual kitchen-sink packs, the automation expectation is unnecessary. The pattern only works in a narrow band: Create-focused expert packs with a trust-based player contract.

**3. Could this pattern appear in non-Create packs?**

The `pack_types` annotation says `create, expert`, but the expert half is unvalidated. An expert pack could theoretically use dual-task verification for any automation requirement (e.g., "build a mob farm AND verify it works"). However, no expert pack in the dataset does this. The pattern's `expert` scope annotation is aspirational, not evidence-based.

### Verdict

MP35 solves a Cabricality-specific problem with a Cabricality-specific solution. The design question (automation verification) is real for Create expert packs, but the specific implementation (item + checkmark with `consume_items: false`) has not been independently adopted by any other pack in a 25-pack dataset. The honor-system weakness further limits its applicability.

### Recommendations

1. **Keep the "single-source" annotation.** Do not promote to multi-source until a second pack validates the pattern.
2. **Narrow `pack_types` to `create` only.** The `expert` scope is unvalidated -- remove it until an expert (non-Create) pack demonstrates the pattern.
3. **Add a "related approaches" note:** "Other Create packs address automation verification differently: Create: Delight uses tutorial/observation tasks, Mechanomania relies on volume-based impracticality, Create: Astral uses `min_tasks` for alternative paths. MP35 is one of several approaches."
4. **Flag the honor-system limitation prominently.** The current "Design considerations" mention it as item (2) but should elevate it to a core caveat.

---

## Audit Item 2: MP36 -- Currency-as-Reward (Universal Exchange Medium)

**Location:** micro-patterns.archive.md, lines 696-712; mod-reward-design.md lines 128-133

### Generalizability Rating: **B** (Good cross-pack validation; definition scope needs tightening)

### Evidence Base

MP36 has **multi-source validation** across 3 packs:
1. GregTech-Odyssey: `gtocore:copper_coin` (item-type currency, dedicated shop chapter)
2. No-Flesh-Within-Chest: `lightmanscurrency:coin_iron`/`coin_gold` (item-type currency, trade stations, 42 references in boss chapter)
3. TheWinterRescue: `frostedheart:insight` (custom-type currency, skill/progression system, 32 insight rewards in t2 chapter)

GT-O and NFwC use standard `type: "item"` rewards with currency items. TWR extends the concept to `type: "frostedheart:insight"` custom rewards.

### Universality Questions

**1. Is the "currency item" definition too broad?**

This is the central concern. The draft document defines currency as: "a currency item (coins, credits) that the player spends at shops, trade stations, or trading systems." But the three validated implementations are fundamentally different:

- **GT-O copper_coin:** A literal coin item spent in a dedicated shop chapter. Classic currency.
- **NFwC lightmanscurrency:** A mod-backed currency system with `wares:delivery_agreement` trade contracts. Structured economy.
- **TWR frostedheart:insight:** A skill-point system where "currency" buys progression unlocks, not items.

These share the abstract concept of "accumulated reward with deferred spending," but the implementation details vary enormously. If the definition is broad enough to include all three, it risks including:
- XP (also accumulated and "spent" on enchanting)
- Any item that has a use in a later recipe (is an iron ingot "currency" for a machine recipe?)
- Loot table rolls (accumulated random rewards)

**2. Is the boundary between MP36 and MP14 (Material Bridge) clear?**

The draft says: "Distinct from MP14 (Material Bridge): currency doesn't bridge to a specific recipe, it bridges to a shop." This is a clean distinction for GT-O and NFwC. But TWR's `frostedheart:insight` blurs it -- insight points unlock specific skills, which is closer to "bridging to a specific unlock" than "bridging to a general shop."

The MP14/MP36 boundary is: **currency is fungible** (can buy many things), **material bridge is specific** (used for one recipe). This distinction holds for GT-O and NFwC but is strained by TWR.

**3. Does the scope `expert, hardcore, rpg` cover the right packs?**

The annotated pack types seem reasonable. Currency systems are most common in packs with:
- Deliberate economy design (expert)
- Survival/combat reward loops (hardcore)
- Role-playing commerce (RPG)

Kitchen-sink packs rarely need formal currency because the breadth of mods provides natural item-based trading. This scope is well-calibrated.

**4. Is the "corresponding currency sink" requirement too strong?**

The draft states: "Currency rewards need a corresponding currency sink (shop, trade station) to have value." This is correct and important -- currency without a sink is a dead-end reward (AP6). But it also means MP36 is **contingent on the pack having a shop system**, which is a significant design commitment, not just a quest pattern.

### Verdict

MP36 is a genuine cross-pack pattern with multi-source validation. The core concept (fungible reward item spent at a shop/sink) is clear and applicable to expert/hardcore/RPG packs. However, the inclusion of TWR's `frostedheart:insight` stretches the definition toward "any accumulated progression resource," which risks making MP36 a catch-all that overlaps with MP14, MP16, and even MP30 (Gamestage Bridge).

### Recommendations

1. **Tighten the definition to exclude custom-type rewards.** MP36 should cover `type: "item"` rewards where the item is a currency (coins, credits). TWR's `frostedheart:insight` is better classified as a custom reward type (noted in mod-reward-design.md's "Cycle 5 finding" section) rather than shoehorned into MP36.
2. **Add a clear fungibility test:** "An item is currency if it can be exchanged for multiple different items/services through a shop or trade system. If it unlocks one specific thing, it is a material bridge (MP14) or gamestage bridge (MP30), not currency."
3. **Keep the multi-source upgrade.** GT-O + NFwC provide sufficient validation with two independent implementations using the same reward type (`item`).
4. **Add a "currency sink required" precondition.** The draft already mentions this in Design Considerations, but it should be elevated to an applicability condition: "Only applicable when the pack has a functioning currency sink (shop chapter, trade station, or equivalent)."

---

## Audit Item 3: MP37 -- Progress Catalog Chapter (Visual Milestone Tracker)

**Location:** micro-patterns.archive.md, lines 716-727

### Generalizability Rating: **C** (Interesting idea, single-source, narrow applicability)

### Evidence Base

MP37 is derived from **1 pack only**: GregTech-Odyssey. The progress chapter lists all circuit items across all voltage tiers with no dependencies and no rewards -- a pure visual tracker.

### Universality Questions

**1. Is a "progress catalog chapter" a general pattern or a GT-O-specific design choice?**

The underlying need -- "the player wants to see their overall progress at a glance" -- is universal. But the solution (a dedicated chapter with no-dep, no-reward item tasks) is one of several approaches:
- Most expert packs rely on the dependency graph itself as a progress indicator (completed nodes are visually distinct)
- ATM-style packs use shape and size changes to mark completed tiers
- Some packs use Patchouli books or other in-game documentation for progress tracking
- FTB Quests' own chapter completion percentage serves as a progress indicator

A dedicated progress chapter is a **heavyweight solution** that adds significant authoring cost (every milestone item must be duplicated as a quest in the catalog chapter). It's appropriate for GT-O's 14 voltage tiers but excessive for packs with 3-6 tiers.

**2. Does the "10+ tiers" threshold hold?**

The draft says: "Works best in expert packs with 10+ tiers/stages; overkill for kitchen-sinks with 3-4 stages." GT-O's 14 voltage tiers are an outlier -- most expert packs have 3-8 tiers (Monifactory has ~5 voltage tiers, E9E has ~4 stages). If the pattern only makes sense at 10+ tiers, its applicability is very narrow.

**3. Could this pattern conflict with MP19 (Chapter-as-Stage)?**

MP19 establishes that chapters represent stages. MP37 adds a meta-chapter that **tracks** stages without being a stage itself. This creates a structural tension: the progress chapter is a chapter that doesn't follow the Chapter-as-Stage convention. For packs that strictly follow MP19, adding a progress catalog chapter would be an exception to the dominant model.

**4. Does the pattern create maintenance burden?**

Yes. Every milestone item exists in two places: the main progression chapter AND the progress catalog. If the pack adds a new tier, the author must update both. This duplication is a maintenance risk that the draft doesn't address.

### Verdict

MP37 is a creative solution to a real but narrow problem. The pattern's applicability is limited to expert packs with unusually many tiers (10+), and the maintenance burden of duplicating milestone items across chapters makes it a costly design choice. Most expert packs can achieve the same progress-tracking goal through the dependency graph's visual state or chapter completion percentages.

### Recommendations

1. **Keep the "single-source" annotation.** The pattern has not been validated by any other pack.
2. **Add a "maintenance burden" caveat to Design Considerations:** "Progress catalog chapters duplicate milestone items across two locations. If the pack adds or modifies tiers, both the main chapters and the catalog must be updated."
3. **Add alternative approaches:** "Progress tracking can also be achieved through: (a) the dependency graph's visual state (completed quests are visually distinct), (b) chapter completion percentages, (c) a Patchouli book or in-game documentation, (d) achievement tabs. Consider whether a dedicated progress chapter is the lightest-weight solution for your pack."
4. **Raise the tier threshold from "10+" to "8+" or remove the specific number.** The threshold is somewhat arbitrary; the real test is whether the pack has enough tiers that players lose track of progress.

---

## Audit Item 4: MP38 -- Profession Chapter (Role-Based Side Content)

**Location:** micro-patterns.archive.md, lines 730-744

### Generalizability Rating: **D** (Too niche to be a general pattern)

### Evidence Base

MP38 is derived from **1 pack only**: TheWinterRescue (TWR), which has 9 profession chapters: hunter, farmer, miner, researcher, fuel_engineer, generator_engineer, siberian_chef, tundra_traveller, craftsman. These complement the main tier chapters (t0-t3).

### Universality Questions

**1. Is "profession chapter" a generalizable quest design concept?**

The concept of "role-based side content" exists in many pack genres:
- RPG packs have class-based or skill-based quest lines
- Kitchen-sink packs have mod-focused chapters that could be seen as "professions" (tech chapter, magic chapter, farming chapter)
- Adventure packs have faction-based quest lines

But TWR's implementation is uniquely specific: 9 dedicated chapters, each named after a profession, running parallel to the main progression. This level of role-based structuring is TWR's signature design, not a general pattern.

**2. Does the pattern create unreasonable authoring expectations?**

TWR's 9 profession chapters represent a massive authoring investment. For a pattern to be "generalizable," it should be achievable by a typical pack author. Expecting authors to create 5-9 additional profession-themed chapters on top of their main progression is unrealistic for most packs. Even TWR's own 21-55% optional rate suggests that not all players engage with profession chapters -- the ROI on this authoring investment is debatable.

**3. Is the `pack_types: expert, story` scope justified?**

The `story` scope is unvalidated -- no story/RPG pack in the dataset uses profession chapters in TWR's format. RPG packs like Prominence II and Finality Genesis use class/skill systems, but these are implemented through game mechanics, not parallel quest chapters. The `expert` scope is validated only by TWR, which is a single pack.

**4. Is this just a special case of MP10 (Independent Island) or MP18 (Choice Reward)?**

Profession chapters could be decomposed into existing patterns:
- Each profession chapter is a fan-out branch from the main progression (MP7)
- The professions collectively represent optional side content (MP10 islands)
- The player's "choice" of profession is a large-scale version of MP18 (Choice Reward)

MP38 adds the concept of **thematic role-based grouping** on top of these existing patterns, but this grouping is primarily an organizational/aesthetic choice rather than a mechanically distinct pattern.

### Verdict

MP38 describes a specific pack's design signature rather than a transferable micro-pattern. TWR's 9 profession chapters are impressive worldbuilding, but the pattern is too niche, too authoring-intensive, and too decomposable into existing patterns (MP7 + MP10 + MP18) to warrant its own entry. It belongs in a "pack-specific design signatures" appendix, not in the general micro-pattern catalog.

### Recommendations

1. **Consider demoting MP38 to a case study or appendix entry** rather than a numbered micro-pattern. Alternatively, merge it into the Scope Annotation Table as a TWR-specific variant of MP7/MP10.
2. **If retained, narrow the scope to `expert (survival)` or add a "TWR signature" tag** similar to the ATM Signature tags on MP4, MP16, MP20, MP21, MP22.
3. **Add a "decomposition" note:** "Profession chapters can be understood as a combination of MP7 (fan-out from main progression) + MP10 (independent optional islands) + MP18 (role choice). The added value of MP38 is the thematic grouping convention."
4. **Remove the `story` pack type** until a story/RPG pack validates the pattern.

---

## Audit Item 5: Draft R36 -- Hardcore Pack Zero-Optional Constraint

**Location:** hardcore-progression-rules-R36-R37_2026-07-08.md, lines 12-25

### Generalizability Rating: **C** (Insufficient data; contradicted by existing evidence)

### Evidence Base

R36 is based on **2 packs**: NFwC (zero optional quests across all sampled chapters) and Era of Black Death (low optional rates). Both are combat-focused packs.

### Universality Questions

**1. Is zero optionality a hardcore-pack rule or a NFwC-specific choice?**

The draft itself acknowledges the counter-evidence: "Some combat packs (Prominence II) use optional content for side activities." Prominence II is an RPG/combat pack that explicitly uses optional content. This single counter-example undermines the "rule" framing.

The hypothesis -- "hardcore packs enforce zero optionality because every quest is a skill check" -- is a reasonable observation about NFwC's design philosophy. But a hypothesis with 1 confirming data point (NFwC), 1 partial confirming point (Era of Black Death, which has "low" not zero optional), and 1 contradicting point (Prominence II) is not ready for rule status.

**2. Does the rule's INFO severity make it harmless?**

The draft proposes INFO-level flagging: "flag `optional: true` quests as INFO." INFO-level rules are non-blocking, which reduces the harm of false positives. However, even INFO-level noise erodes trust in the validation system -- if every optional quest in a combat pack triggers an INFO warning that the author deliberately intended, the author will learn to ignore INFO messages.

**3. Is "hardcore" a well-defined pack type?**

The skill's pack type taxonomy (per module-index.md and design guide) includes: kitchen-sink, expert, skyblock, create, story, and hardcore. But "hardcore" is the least well-defined:
- NFwC is hardcore/combat
- Era of Black Death is combat/RPG
- Prominence II is RPG
- Craft to Exile Dissonance is ARPG/story

Are all of these "hardcore"? The boundary between "hardcore," "combat," and "RPG" is blurry. R36 needs a clear pack-type definition before it can be applied.

**4. Does "zero optional" actually correlate with quality?**

NFwC has zero optional quests and is well-regarded. But the absence of optional content might be a consequence of the pack's scope and authoring resources rather than a deliberate design constraint. A small team might simply not have the bandwidth to create optional side content. Correlation (zero optional + good pack) does not imply causation (zero optional -> good pack).

### Verdict

R36 is a premature rule. With only 2 data points (one strong, one partial) and 1 direct counter-example, the pattern is not established enough for even an INFO-level rule. The hypothesis is interesting and worth tracking as more data becomes available, but promoting it to a rule risks encoding NFwC's specific design philosophy as a universal hardcore-pack constraint.

### Recommendations

1. **Do NOT promote R36 to active rule status.** Keep it as a high-risk draft.
2. **Define "hardcore" pack type explicitly** before any rule can reference it. Current data has NFwC (hardcore), Era of Black Death (combat/RPG), and Prominence II (RPG) -- the boundaries are unclear.
3. **Collect more data points** before revisiting: RLCraft, DawnCraft, Vault Hunters 3 (as the draft suggests). Need at least 4-5 packs with confirmed zero-optional patterns to establish a trend.
4. **Reframe as a design observation rather than a rule:** "Observed: some combat-focused packs (NFwC) use zero optional quests, treating every quest as a mandatory skill check. This is a valid design philosophy but not a universal hardcore-pack requirement."

---

## Audit Item 6: Draft R37 -- Kill Task Density Calibration

**Location:** hardcore-progression-rules-R36-R37_2026-07-08.md, lines 27-40

### Generalizability Rating: **B-** (Reasonable calibration framework; needs finer pack-type granularity)

### Evidence Base

R37 is based on **3 packs**: NFwC boss chapter (65% kill density), Era of Black Death (kill tasks distributed across 17 chapters), and Craftoria bosses chapter (31% kill density).

### Universality Questions

**1. Are the proposed density ranges well-calibrated?**

The draft proposes:
- Hardcore/combat: 30-65%
- RPG: 10-20%
- Kitchen-sink: 0-5%
- Expert/Create: 0%

These ranges are directionally correct but have gaps:

**Problem 1: "Expert/Create: 0%" is too absolute.** Expert packs can have kill tasks -- Monifactory has `kill` tasks in its data (per the cross-pack comparison table, Monifactory has 5+ task types including structure and observation, and the raw data shows 4 types in the Monifactory raw row). A GregTech expert pack might include a "kill a Warden for a rare drop" quest. The 0% floor should be "0-2%" or "near-zero" rather than absolute zero.

**Problem 2: The RPG range (10-20%) is based on zero data points.** No RPG pack's kill density is actually measured in the draft. Era of Black Death is classified as "combat/RPG" but its kill distribution is described qualitatively ("distributed across 17 chapters") rather than quantitatively. The 10-20% range appears to be an estimate.

**Problem 3: "Kitchen-sink: 0-5%" has only Craftoria (31% in bosses chapter) as data.** Craftoria's boss chapter at 31% is far above the proposed 0-5% range, which means either: (a) the range is wrong, (b) Craftoria's boss chapter is an exception, or (c) Craftoria should be classified differently for this metric. The draft doesn't resolve this ambiguity.

**2. Does the rule need finer pack-type distinctions?**

Yes. The current four-tier system (hardcore/RPG/kitchen-sink/expert) misses important nuances:
- **Combat-focused kitchen-sinks** (All-the-Mons with Cobblemon) likely have higher kill density than tech-focused kitchen-sinks (ATM-10)
- **Boss-rush packs** (a hypothetical subgenre) would have 80%+ kill density
- **Adventure/exploration packs** might have kill tasks only at boss milestones

A more granular classification might be:
- Hardcore/combat-primary: 30-65%
- Combat-RPG hybrid: 15-30%
- RPG with combat elements: 5-20%
- Kitchen-sink (boss chapters only): 15-35%
- Kitchen-sink (overall): 2-8%
- Expert/Create/tech: 0-2%

**3. Is kill density a design quality metric or a design choice metric?**

The draft correctly notes: "Kill density is a design choice, not a quality metric." This is important. A chapter with 65% kill density in NFwC is **intentional and correct** for the pack's design. The rule should serve as calibration guidance ("is your kill density aligned with your pack's stated genre?") rather than a quality judgment ("your kill density is too high").

**4. Does the rule account for chapter-level vs. pack-level variation?**

A combat pack might have:
- Boss chapters: 50-65% kill density
- Crafting chapters: 0% kill density
- Exploration chapters: 10-20% kill density

The draft proposes chapter-level calculation (`kill_tasks / total_quests` per chapter), which is correct. But the pack-type guidelines (30-65% for hardcore) seem to describe pack-level averages, not per-chapter ranges. The rule needs to distinguish:
- Per-chapter kill density (for detecting outlier chapters)
- Per-pack kill density (for overall genre calibration)

### Verdict

R37 is a more promising rule than R36. The concept of kill-density calibration is useful for genre alignment, and the basic framework (calculate ratio, compare against genre benchmark, flag outliers) is sound. However, the proposed ranges need more data, the pack-type taxonomy needs finer granularity, and the rule should explicitly distinguish chapter-level from pack-level metrics.

### Recommendations

1. **Keep R37 as a draft but invest in data collection.** The framework is sound; the calibration numbers are not yet reliable.
2. **Expand the pack-type taxonomy** to at least 6 categories (see question 2 above). The current 4 categories are too coarse.
3. **Distinguish chapter-level vs. pack-level metrics** explicitly in the rule definition. Add: "Per-chapter kill density may vary significantly within a pack. Flag chapters that deviate from the pack's overall genre expectation by more than 2x."
4. **Change "Expert/Create: 0%" to "Expert/Create: 0-2%."** Absolute zero is too strict and will produce false positives.
5. **Add Craftoria boss chapter (31%) as a data point for kitchen-sink boss chapters** and create a separate "kitchen-sink boss chapter" category (15-35%).
6. **Reframe the rule's output from WARNING to INFO.** The draft already says "informational, not blocking," but the severity level should match this intent.

---

## Summary Table

| Audit Item | Rating | Source Packs | Source Teams | Key Limitation | Action Priority |
|---|---|---|---|---|---|
| **MP35** Dual-Task Automation | **C** | Cabricality (1 pack) | 1 team | Single-source; no independent validation in 25-pack dataset; honor-system weakness | MEDIUM -- narrow scope, add alternative approaches |
| **MP36** Currency-as-Reward | **B** | GT-O, NFwC, TWR (3 packs) | 3 teams | Definition stretched by TWR's custom type; MP14 boundary unclear | MEDIUM -- tighten definition, add fungibility test |
| **MP37** Progress Catalog | **C** | GT-O (1 pack) | 1 team | Single-source; narrow applicability (10+ tiers); maintenance burden | LOW -- keep single-source tag, add alternatives |
| **MP38** Profession Chapter | **D** | TWR (1 pack) | 1 team | Too niche; decomposable into MP7+MP10+MP18; authoring cost prohibitive | HIGH -- consider demotion to case study or appendix |
| **R36** Hardcore Zero-Optional | **C** | NFwC, Era of Black Death (2 packs) | 2 teams | Contradicted by Prominence II; "hardcore" undefined; premature | HIGH -- do NOT promote to active rule |
| **R37** Kill Task Density | **B-** | NFwC, Era of Black Death, Craftoria (3 packs) | 3 teams | Ranges need more data; pack-type taxonomy too coarse; chapter vs pack level unclear | MEDIUM -- refine ranges, expand taxonomy |

---

## Cross-Cutting Findings

### Finding 1: Cycle 5 Has a Severe Single-Source Problem

Of the 6 Cycle 5 additions, **4 are single-source** (MP35, MP37, MP38, and partially R36). This is worse than Cycle 3 (2 single-source out of 7 items) and Cycle 4 (0 pure single-source). The pattern suggests that Cycle 5 pushed into pack types (Create expert, hardcore, survival expert) where public config data is scarce.

The single-source patterns (MP35, MP37, MP38) share a common risk: they may be encoding **individual pack author design signatures** as **universal micro-patterns**. The ATM Signature tags (MP4, MP16, MP20, MP21, MP22) exist precisely because earlier cycles made this mistake and had to retroactively scope patterns. Cycle 5 should apply the same discipline upfront.

### Finding 2: Pack-Type Taxonomy Is Not Keeping Pace

Multiple Cycle 5 items expose inadequacies in the pack-type taxonomy:
- R36 needs a "hardcore" definition that doesn't exist
- R37 needs finer granularity than the current 4-tier system
- MP38's `expert, story` scope is unvalidated for `story`
- MP36's `expert, hardcore, rpg` grouping lumps together very different economy designs

The skill's pack-type taxonomy (kitchen-sink, expert, skyblock, create, story, hardcore) was adequate for Cycles 1-3 but is now too coarse for the specialized patterns being added. A taxonomy revision is overdue.

### Finding 3: Pattern Decomposition Should Be Preferred Over New Patterns

MP38 (Profession Chapter) is the clearest example, but the pattern applies more broadly: before creating a new micro-pattern, the skill should ask whether the observed design can be decomposed into existing patterns. MP38 = MP7 + MP10 + MP18. MP35's dual-task approach is a specific application of MP2 (Multi-Item Synthesis) with a checkmark variant. Creating new numbered patterns for every observed variation risks pattern bloat that makes the reference system harder to navigate without proportional value.

---

## Action Items (Prioritized)

### HIGH Priority

1. **R36 -- Block promotion to active rule.** The data is insufficient (2 packs, 1 counter-example) and the "hardcore" pack type is undefined. Keep as draft until 4+ data points confirm the trend.

2. **MP38 -- Evaluate demotion from numbered pattern.** The profession chapter concept is decomposable into existing patterns and too niche (1 pack, 9 chapters) to warrant its own MP number. Consider moving to a case study section or adding a "TWR Signature" tag analogous to ATM Signature tags.

### MEDIUM Priority

3. **MP36 -- Tighten the currency definition.** Add a fungibility test ("can buy multiple things through a shop") and exclude custom-type rewards (TWR's insight). Keep multi-source status based on GT-O + NFwC.

4. **MP35 -- Narrow scope to `create` only.** Remove the unvalidated `expert` scope annotation. Add a note about alternative automation-verification approaches used by other Create packs.

5. **R37 -- Refine kill-density ranges and taxonomy.** Expand to 6 pack-type categories, change expert/Create from "0%" to "0-2%", and distinguish chapter-level from pack-level metrics.

### LOW Priority

6. **MP37 -- Add alternative progress-tracking approaches.** The progress catalog is one of several solutions; document the alternatives so pack authors can choose the lightest-weight option.

7. **Pack-type taxonomy revision.** Begin planning a taxonomy expansion to address the gaps exposed by Cycle 5 (hardcore definition, combat-RPG hybrid, kitchen-sink sub-genres). This is a prerequisite for R36 and R37 promotion.
