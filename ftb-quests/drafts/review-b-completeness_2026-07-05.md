# Review B — Completeness Audit

**Reviewer role:** B (completeness challenger)
**Date:** 2026-07-05
**Scope:** micro-patterns.md, anti-patterns.md, progression-rules.md, SKILL.md

---

## Executive Summary

The three design documents form a strong conceptual triangle: micro-patterns describe *what good looks like*, anti-patterns describe *what bad looks like*, and progression-rules describe *how to detect bad automatically*. The internal logic is sound and the cross-referencing is mostly explicit. However, there are **significant coverage gaps** in task/reward type diversity, **one critical anti-pattern with no corresponding rule**, and a **near-total absence of AI-generation-specific safeguards**. Below I enumerate 15 specific challenges, ordered by severity.

---

## Challenge B1 — Task Type Coverage Gap (7 of 15 types unrepresented)

**What is missing:** FTB Quests supports 15 task types (per SKILL.md's quick reference): `item`, `fluid`, `forge_energy`, `xp`, `kill`, `advancement`, `stat`, `location`, `dimension`, `biome`, `structure`, `observation`, `gamestage`, `checkmark`, `custom`. Micro-patterns.md provides dedicated patterns for only **8 of them**: `item` (MP1, MP2), `checkmark` (MP3), `stat` (MP3), `observation` (MP3), `dimension` (MP5), `kill` (MP4), `biome` (briefly in MP5 quantified section).

The following task types have **zero micro-pattern coverage**:

| Missing type | Why it matters |
|---|---|
| `fluid` | Fluid tasks are central to tech packs (Mekanism, Thermal, Immersive Engineering). A "collect 1000mB of liquid ethylene" quest has fundamentally different design considerations than an item task (tank placement, pipe routing, pump power). No MP explains how to design a fluid-task quest. |
| `forge_energy` | Energy tasks ("store 10,000 FE") gate power infrastructure. No pattern addresses energy-threshold gating or how to calibrate energy values against progression stage. |
| `xp` (as task) | XP-collection tasks are distinct from XP rewards. No pattern covers when to use "collect XP" as a gate vs. a time-gate proxy. |
| `advancement` | Vanilla advancement tasks bridge FTB Quests with Minecraft's native advancement system. No pattern explains how to pair advancement tasks with item tasks, or when to prefer advancement over checkmark. |
| `location` | Location tasks (reach specific coordinates) are the RPG/adventure pack's primary exploration gate. Prominence II uses them extensively. Zero coverage. |
| `structure` | Structure-discovery tasks ("find a Village") are a key exploration pattern. Zero coverage despite being a native FTB Quests type. |
| `gamestage` | Gamestage tasks are the expert pack's invisible gating backbone. Monifactory uses them for voltage-tier progression. MP23 mentions invisible infrastructure chapters but provides no pattern for the gamestage task itself. |

**Suggested fix:** Add at least one micro-pattern per missing type, or group them into composite patterns (e.g., "MP27 — Energy Threshold Gate" for `forge_energy`, "MP28 — Advancement Bridge" for `advancement`, "MP29 — Location Discovery" for `location` + `structure`). At minimum, the types used by the 11 audited packs (`fluid`, `advancement`, `gamestage`, `location`) need patterns.

---

## Challenge B2 — Reward Type Coverage Gap (7 of 13 types unrepresented)

**What is missing:** FTB Quests supports 13 reward types: `item`, `xp`, `xp_levels`, `command`, `loot`, `random`, `choice`, `all_table`, `advancement`, `toast`, `gamestage`, `custom`, `currency`. Micro-patterns.md covers **6**: `item` (MP14, MP15, MP17), `xp`/`xp_levels` (MP16), `random` (MP4 escalation), `choice` (MP18), `loot` (briefly in MP4).

Missing reward types with no dedicated pattern:

| Missing type | Why it matters |
|---|---|
| `command` | Command rewards execute arbitrary server commands — extremely powerful, extremely dangerous. No pattern covers safety (permission levels, `{p}` placeholder), common use cases (`/give`, `/tp`, `/effect`), or the anti-pattern of giving op-level commands. This is a **safety gap**, not just a coverage gap. |
| `loot` / `all_table` | Loot table rewards are referenced in MP4 but never get a dedicated pattern. The reward table system (`reward_tables[]` definition, weight/rollover, `hide_tooltip`/`use_title`) is complex enough to warrant its own pattern. |
| `toast` | Toast rewards (non-item notification popups) are a unique UX tool. No pattern explains when to use a toast vs. a description vs. a subtitle. |
| `advancement` | Advancement rewards grant vanilla advancements. No pattern for the vanilla-advancement-as-reward pattern that some narrative packs use. |
| `gamestage` | Gamestage rewards are the flip side of gamestage tasks — they unlock content invisibly. MP23 discusses the infrastructure concept but never provides a pattern for the gamestage reward itself. |
| `custom` | Custom rewards (KubeJS-scripted) are the deep-integration pack's escape hatch. No pattern covers when to use custom rewards vs. composing standard types. |
| `currency` | Currency rewards (off by default, requires `default_reward_team` config) are never discussed as a pattern despite being a distinct economic model. |

**Suggested fix:** Add patterns for at least `command` (safety-critical), `loot`/`all_table` (reward table design), and `gamestage` (expert-pack infrastructure). The others can be briefer.

---

## Challenge B3 — AP1 (Description-Reality Mismatch) Has No Progression Rule

**What is missing:** The progression-rules.md mapping table explicitly states: "AP1 Description-Reality Mismatch — not in this rule set — description content validation requires runtime (JEI/EMI comparison), static checks cannot cover it." This is an acknowledged gap, but it is the **most damaging anti-pattern** (AP1 is ranked first by severity in anti-patterns.md). Leaving the #1 anti-pattern without any automated detection means the validator pipeline silently passes quests with lying descriptions.

**Why it matters:** The FTB Evolution issue #6447 documents dozens of description-reality mismatches in a single pack. AI-generated quests are *especially* prone to this because the AI can hallucinate item names, crafting recipes, or mod mechanics that don't match the actual game. The "never hallucinate" rule in SKILL.md mitigates the generation side, but does nothing for the validation side — if a description slips through with a subtle inaccuracy, no rule catches it.

**Suggested fix:** Add at least a **partial static check** — R23 "Description-Item Consistency": verify that item IDs mentioned in `description` text (parseable via `&e<id>&r` patterns or explicit item references) actually exist in the task/reward arrays and in `items.json5`. This catches the simplest mismatches (description says "Shadowflame Goo" but task asks for "Shadowpulse Goo") without needing runtime JEI data. Mark it as WARNING level. Full AP1 coverage requires runtime, but partial coverage is far better than zero.

---

## Challenge B4 — No AI-Generation-Specific Anti-Patterns

**What is missing:** All three documents are written for human pack authors. None address risks unique to AI-generated quest configs. Given that this skill's primary purpose is AI-driven generation, this is a critical omission.

**Specific AI risks not covered:**

1. **Hallucination cascade:** The "never hallucinate" rule in SKILL.md prevents item-id fabrication, but doesn't address subtler hallucinations — wrong item *counts* (AI guesses 64 when the recipe needs 16), wrong *dependency ordering* (AI assumes a mod's progression without verifying), wrong *mod interactions* (AI assumes mod A integrates with mod B when they don't).

2. **Style homogenization:** AI tends to produce uniform quest descriptions, identical reward structures, and monotonous pacing. No anti-pattern addresses "all quests sound the same" or "every reward is exactly 10 XP + 1 item." Human authors have natural variation; AI needs explicit guidance to vary.

3. **Batch consistency errors:** When generating 50+ quests in a batch, AI may create internal contradictions — quest 12 says "you'll need this for later" but quest 37 (the "later") was designed independently and doesn't actually use the item. No rule checks cross-quest narrative consistency.

4. **Over-reliance on item tasks:** AI naturally gravitates toward `item` tasks because they're the simplest to generate from recipe data. The task-type diversity gap (B1) becomes worse when AI is the author — without explicit guidance, AI will produce 95% item tasks and 5% checkmark tasks.

5. **Missing the "why" at scale:** PP5 (Context Void) addresses empty descriptions, but AI has the opposite risk — generating verbose descriptions that *sound* informative but contain no actionable content (the "AI slop" problem). No anti-pattern addresses "description is long but says nothing."

**Suggested fix:** Add an "AI-Generation Considerations" section to anti-patterns.md with at least AP9 (Hallucination Cascade), AP10 (Style Homogenization), and AP11 (Batch Narrative Inconsistency). Add corresponding progression-rules (R23–R25) that can partially detect these issues.

---

## Challenge B5 — `consume_items` Semantics Not Covered as a Pattern or Rule

**What is missing:** The `consume_items` field on item tasks is a critical design decision — it determines whether the player keeps or loses the submitted items. SKILL.md mentions `default_consume_items` as a pack-level setting, and micro-patterns MP1 explicitly says "no `consume_items`" for standard quests, and MP2 warns "do NOT set `consume_items: true` on individual tasks." But there is no dedicated pattern explaining when to consume vs. not consume, and no rule detecting misuse.

**Why it matters:** Setting `consume_items: true` on a quest that asks for a unique item (e.g., a boss drop) can permanently destroy the item if the player submits it and then needs it for another quest. Conversely, NOT consuming items on a resource-sink quest (e.g., "feed 64 cobblestone into the crusher") means the player can reuse the same cobblestone for every quest, trivializing the resource cost. This is a subset of the reward-disconnection problem but has distinct mechanics.

**Suggested fix:** Add MP30 — "Consume vs. Retain Decision" pattern, and add R23 — "Consume-Items Safety Check" (flag `consume_items: true` on unique/irreplaceable items; flag `consume_items: false` on resource-sink quests where the resource should be spent).

---

## Challenge B6 — Reward Table Design Has No Pattern

**What is missing:** Reward tables (`reward_tables[]` in the spec) are a complex subsystem — they define weighted random loot, choice pools, and all_table distributions. SKILL.md references them in the "Task & reward types" section and notes `table_id` is a decimal long. Micro-patterns MP4 uses a `random` reward with a `table_id`. But no micro-pattern explains how to *design* a reward table: how many entries, what weights, when to use `loot` vs. `random` vs. `choice` vs. `all_table`.

**Why it matters:** Reward tables are the primary mechanism for randomized rewards, which are important for replayability and engagement. AI generating quests without understanding reward tables will either avoid them entirely (always using deterministic `item` rewards) or misuse them (wrong `table_id` format, nonsensical weights).

**Suggested fix:** Add MP31 — "Reward Table Design" pattern covering: (1) when to use each table type (`loot` = one random pick, `random` = weighted random, `choice` = player picks one, `all_table` = give everything), (2) weight calibration, (3) `hide_tooltip`/`use_title` defaults.

---

## Challenge B7 — Quest Link (`quest_links`) Cross-Chapter Pattern Missing

**What is missing:** SKILL.md mentions `quest_links[]` as a mechanism for displaying the same quest in two chapters (hexagon, size 2.0). Micro-patterns MP20 mentions `hexagon` as the shape for cross-chapter links. But no micro-pattern explains the *design decision* of when to use a quest link vs. a cross-chapter dependency vs. duplicating the quest.

**Why it matters:** Quest links are a powerful but subtle feature — misuse creates confusion (the player sees the same quest in two places and doesn't know which is the "real" one) or broken dependencies (a link in chapter B depends on chapter A's quests, but the player hasn't visited chapter A). For AI generation, the lack of a pattern means AI will either never use links (missing useful cross-references) or use them incorrectly.

**Suggested fix:** Add MP32 — "Cross-Chapter Quest Link" pattern: when to use a link (quest genuinely belongs to two mods/themes), when to use a dependency (quest belongs to one chapter but gates another), and when to duplicate (never — use a link). Include the hexagon/size 2.0 convention.

---

## Challenge B8 — No Rule for `title`/`subtitle`/`description` Length or Quality

**What is missing:** SKILL.md specifies length budgets (title <= 4 words, subtitle = 1 line, description ~2-4 sentences). R18 checks for description *existence* but not *quality* or *length*. No rule detects: titles that are too long, subtitles that duplicate the title, descriptions that are a single word or exceed a reasonable maximum.

**Why it matters:** AI-generated text tends toward verbose or generic descriptions ("This quest requires you to obtain the item needed for progression" — technically present, functionally useless). R18 passes this as "has description." A quality check would flag it.

**Suggested fix:** Add R24 — "Description Quality Baseline": (1) flag descriptions < 10 characters (probably a placeholder), (2) flag descriptions > 300 words (probably AI-generated padding), (3) flag titles > 8 words (probably a sentence, not a title), (4) flag subtitle that is identical to title.

---

## Challenge B9 — Chapter Group and `order_index` Validation Missing

**What is missing:** R4 checks pack-type stage boundaries but assumes `order_index` and `group` are correct. No rule validates that `order_index` values are sequential without gaps, that `group` assignments are consistent (a tech chapter shouldn't be in the "Magic" group), or that chapter ordering matches the dependency graph (a chapter at `order_index: 5` shouldn't depend on a chapter at `order_index: 10`).

**Why it matters:** R22 catches backward cross-chapter dependencies at the quest level, but not at the chapter-group level. If a group is mislabeled or `order_index` has a gap (1, 2, 4, 5 — chapter 3 was deleted), the UI ordering breaks or the player sees chapters in the wrong sequence.

**Suggested fix:** Add R25 — "Chapter Ordering Integrity": (1) check `order_index` is sequential, (2) check group membership is consistent with chapter content (heuristic: chapter icon's mod namespace should match the group's theme), (3) check that no chapter's quests depend on a later chapter's quests (R22 does this per-quest, but a chapter-level summary would be more actionable).

---

## Challenge B10 — `optional` and `secret` Interaction Not Fully Specified

**What is missing:** R6 and R7 check optional-gating and unreachability. But the interaction between `optional`, `secret`, and `always_invisible` flags is not fully explored. Specifically:

- Can a quest be both `optional` and `secret`? What does that mean for completion tracking?
- Does `always_invisible: true` exclude a quest from completion percentage? (SKILL.md says `optional: true` does; is `always_invisible` the same?)
- If a `secret` quest depends on an `optional` quest, and the optional quest is skipped, is the secret quest permanently undiscoverable?

**Why it matters:** These flag combinations are the source of AP3 (Unfinishable Chapter). The rules check the symptoms (unreachable quests) but don't validate the flag combinations themselves.

**Suggested fix:** Add R26 — "Flag Combination Safety": enumerate valid/invalid combinations of `optional`, `secret`, `always_invisible`, and `hide_until_deps_visible`. Flag `secret + always_invisible` as suspicious (double-hidden). Flag `optional` quest as sole dependency of a `secret` quest.

---

## Challenge B11 — No Pattern for `advancement` Task-Reward Pairing

**What is missing:** Some packs use advancement tasks to bridge FTB Quests with vanilla Minecraft's advancement system (e.g., "complete the 'Acquire Hardware' advancement" as a quest). Some use advancement rewards to grant advancements (e.g., "completing this quest grants the 'Hot Stuff' advancement"). No micro-pattern covers this integration.

**Why it matters:** Advancement integration is a powerful tool for narrative packs and tutorial packs. Without a pattern, AI will ignore it entirely or misuse it (referencing advancement IDs that don't exist, or granting advancements that have no gameplay effect).

**Suggested fix:** Add MP33 — "Advancement Bridge" pattern: how to use `advancement` tasks to gate quest progression behind vanilla milestones, and how to use `advancement` rewards to grant vanilla achievements as quest completions. Include the caveat that advancement IDs must be verified against the pack's advancement data.

---

## Challenge B12 — Progression-Rules References External Documents Not in Scope

**What is missing:** progression-rules.md references `difficulty-curve.md` (R15, R19) and `reward-economy.md` (R12) as sources and design rationale. These documents are listed in the Sources section. However, if they are not part of the skill's reference directory, the AI cannot load them when executing the rules. The rules assume concepts from these documents (bottleneck definitions, reward tier classifications) without restating them.

**Why it matters:** If the AI executing these rules cannot access `difficulty-curve.md` or `reward-economy.md`, then R15's complexity estimation, R19's bottleneck definition, and R12's value progression logic are incomplete — the AI must guess at the thresholds and classifications.

**Suggested fix:** Either (1) ensure these documents are in the reference directory and referenced by SKILL.md, or (2) inline the critical definitions (bottleneck criteria, reward tier boundaries, complexity estimation formula) into progression-rules.md so the rules are self-contained.

---

## Challenge B13 — No Pattern for Multi-Player / Team Quest Dynamics

**What is missing:** FTB Quests supports team-based completion (`default_reward_team`, `team_progress`). None of the three documents address how quest design changes for multiplayer packs. Team-shared progression creates unique issues: one player completes a quest but the reward goes to the team chest (which another player already emptied), or a kill task counts kills from any team member (making it trivially easy).

**Why it matters:** If this skill is used to generate quests for a server pack, the team dynamics are invisible — no pattern or rule addresses them. The `consume_items` behavior differs in team mode (items are consumed from the submitting player, but rewards may go to the team).

**Suggested fix:** At minimum, add a note to anti-patterns.md (AP12 — "Team-Mode Reward Leakage") and a pattern to micro-patterns.md (MP34 — "Team-Aware Reward Design"). If multiplayer is out of scope, state it explicitly so the AI doesn't accidentally generate team-incompatible quests.

---

## Challenge B14 — No Rule for `exclude_from_claim_all` and `autoclaim` Semantics

**What is missing:** The `exclude_from_claim_all` flag (seen in MP4's random reward) and `autoclaim` behavior (mentioned in MP18 for choice rewards) affect how rewards are distributed. No rule validates their correct usage.

**Why it matters:** `exclude_from_claim_all: true` on a reward means it won't be granted when the player uses "Claim All" — this is important for random/loot rewards that should be individually claimed. If AI sets this incorrectly, players may miss rewards or get unwanted items in bulk.

**Suggested fix:** Add R27 — "Claim Behavior Consistency": flag `random`/`loot`/`choice` rewards without `exclude_from_claim_all: true` (these types usually should be individually claimed). Flag `item` rewards with `exclude_from_claim_all: true` (usually a mistake — item rewards should be claimable in bulk).

---

## Challenge B15 — Cross-Document Reference Integrity

**What is missing:** The three documents cross-reference each other and external documents. I verified the following reference chains:

| Reference | Status |
|---|---|
| micro-patterns → anti-patterns (MP24-26 → AP1-3) | OK |
| anti-patterns → micro-patterns (AP6 → MP14-18) | OK |
| progression-rules → anti-patterns (R5-R21 → AP1-AP8) | OK, with explicit AP1 gap noted |
| progression-rules → micro-patterns (R14 → MP11, R10 → MP14) | OK |
| micro-patterns → design-guide §atm-layout-patterns | **NOT IN SCOPE** — referenced but not reviewed |
| micro-patterns → design-guide §pack-type-patterns | **NOT IN SCOPE** |
| progression-rules → difficulty-curve.md | **NOT IN SCOPE** |
| progression-rules → reward-economy.md | **NOT IN SCOPE** |
| SKILL.md → all three documents | Indirect — SKILL.md references design-guide.md which presumably references these |

**The gap:** The three documents form a tight triangle, but they sit inside a larger web of design documents (design-guide.md, difficulty-curve.md, reward-economy.md, tech-progression.md, atm-layout-patterns, pack-type-patterns) that are referenced extensively but were not part of this review. If any of those external documents have stale or contradictory information, the three documents under review may inherit errors.

**Suggested fix:** Add a "Document Map" section to one of the three documents (or to SKILL.md) that lists all referenced documents, their roles, and their last-verified dates. This makes it trivial to spot orphaned references.

---

## Summary of Findings

| ID | Category | Severity | Priority |
|---|---|---|---|
| B1 | Task type coverage (7/15 missing) | HIGH | 1 |
| B2 | Reward type coverage (7/13 missing) | HIGH | 2 |
| B3 | AP1 has no corresponding rule | HIGH | 3 |
| B4 | No AI-generation-specific patterns | HIGH | 4 |
| B5 | `consume_items` semantics unpatterned | MEDIUM | 5 |
| B6 | Reward table design unpatterned | MEDIUM | 6 |
| B7 | Quest link cross-chapter pattern missing | MEDIUM | 7 |
| B8 | Title/subtitle/description quality rule missing | MEDIUM | 8 |
| B9 | Chapter group/order_index validation missing | MEDIUM | 9 |
| B10 | Flag combination safety not specified | LOW | 10 |
| B11 | Advancement task-reward pairing missing | LOW | 11 |
| B12 | External document dependency not self-contained | LOW | 12 |
| B13 | Multi-player/team dynamics not covered | LOW | 13 |
| B14 | Claim behavior rules missing | LOW | 14 |
| B15 | Cross-document reference integrity | INFO | 15 |

---

## Overall Assessment

**Verdict: NEEDS MODIFICATION (needs revision, not rewrite)**

**Rationale:** The three documents' core architecture is sound — the pattern/anti-pattern/rule triangle is the right model, the three-hard-problems framing is correct, and the cross-referencing is mostly explicit. The issues are coverage gaps, not structural flaws. No document needs to be rewritten from scratch; each needs targeted additions.

**Priority action plan:**

1. **Immediate (before next release):** B1 + B2 — add micro-patterns for the most commonly used missing task types (`fluid`, `advancement`, `gamestage`, `forge_energy`) and reward types (`command`, `loot`/`all_table`, `gamestage`). These are used by the audited packs and AI will encounter them.

2. **High priority:** B3 + B4 — add at least a partial static check for AP1 (description-item consistency), and add AI-generation-specific anti-patterns. These address the skill's core use case (AI-generated quests) where current documents are silent.

3. **Medium priority:** B5–B9 — add patterns/rules for `consume_items`, reward tables, quest links, description quality, and chapter ordering. These fill important but non-critical gaps.

4. **Low priority (can defer):** B10–B15 — flag combinations, advancement pairing, external document inlining, team dynamics, claim behavior, and reference map. These are edge cases or documentation hygiene.

**Estimated effort:** B1+B2 = ~8 new micro-patterns. B3 = 1 new rule. B4 = 3 new anti-patterns + 2 new rules. Total: ~14 document additions, no restructuring required.
