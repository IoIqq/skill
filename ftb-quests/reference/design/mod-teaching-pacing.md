# mod-teaching-pacing

> **Core question:** 章节在测试之前教学了吗？节奏对吗？
> **Lines:** ~280 | **Step 2 load:** yes | **Step 4 load:** partial | **Step 5 load:** yes

## Quick Reference

| ID | Title | Phase | Severity | Pack types |
|---|---|---|---|---|
| MP3 | Acknowledgement Gate | Step 4 | -- | all |
| MP11 | Teach-Then-Do | Step 2 + Step 4 | -- | all |
| MP12 | Tier Escalation | Step 2 | -- | all |
| MP19 | Chapter-as-Stage | Step 2 | -- | all |
| MP23 | Invisible Infrastructure | Step 2 | -- | expert |
| AP5 | Empty Quest Description | Step 2/4 | Medium | all |
| AP13 | Premature Item Submission | Step 4 | Medium | all |
| R14 | Teach-Then-Do Ordering | Step 5 | P1 | all |
| R15 | Complexity Escalation | Step 5 | P2 | all |
| R17 | Tool-Reward-Before-Use | Step 4/5 | P2/P3 | all |
| R18 | Description Coverage | Step 4 | P1 | all |
| R19 | Bottleneck Spacing | Step 5 | P2 | all |
| R21 | Hidden Quest Signpost | Step 5 | P3 | all |
| PP5 | Context Void | Step 2 | -- | all |

---

## Patterns

### MP3 — Acknowledgement Gate

The task is not "do something" but "acknowledge you've read this." A `checkmark` task (click-to-complete), `stat` task with `value: 1` on `minecraft:play_time` (auto-completes after 1 tick), or `observation` task. Quest has a long `description` (the actual tutorial text) and a `subtitle` with the key takeaway. Reward is the tool or item needed for the next quest.

Separates **teaching** from **doing**. A tutorial quest with a checkmark task says "read this, then move on." The next quest's item task says "now apply what you learned." Mixing tutorial text into the item quest makes it easy to skip; separating them forces the player to at least open the acknowledgement quest.

**Real case (Create: Delight, Feast_Afoot):** Humidity-system tutorial uses `stat: minecraft:play_time value: 1` with multi-line description explaining the 5-tier humidity mechanic. Subtitle color-codes the tiers. Reward: the hygrometer tool needed for the next farming quest.

### MP11 — Teach-Then-Do Sequencing

Two adjacent quests in a dependency chain. Quest 1 is **teaching**: checkmark/stat task, long description explaining the mechanic, subtitle with key takeaway, reward is the tool/item needed to practice. Quest 2 depends_on Quest 1 and is **doing**: item task requiring the player to craft/use what was taught, minimal description, reward is the next-step material or XP.

Visible in Create: Delight Feast_Afoot (tutorial quests followed by practical quests) and ATM-10 Mekanism chapter (introduction checkmark -> first craft item -> first use observation -> advanced recipe item -> automation tip checkmark).

Shape difference signals intent: teaching quest uses `rsquare`; doing quest uses default `circle`.

### MP12 — Tier Escalation Within a Chapter

Quests ordered by tier from cheapest/simplest to most expensive/complex. First tier has low-count item task (`count: 1`), simple reward. Each subsequent tier increases count or complexity. Final tier has largest `size`, most distinctive `shape`, richest reward.

ATM-10 AllTheModium: progresses from AllTheModium (Overworld, netherite pick) -> Vibranium (Nether, ATM pick) -> Unobtainium (End, vibranium pick). Each tier is a column of rsquare/octagon pairs at increasing y-values.

### MP19 — Chapter-as-Stage

Each phase or topic is a separate chapter. Chapter ordering via `order_index` defines suggested sequence. Chapter `icon` represents the theme. All quests within a chapter are at the same stage; cross-stage progression is cross-chapter.

**Dominant model across all packs.** Variation is in strictness: kitchen-sinks use `flexible` (suggestions), expert packs use `linear` (locked), RPG packs use dependency-gated reveals.

ATM-10: 64 chapters in 10 groups. Create: Delight: 41 chapters in 6 groups. Monifactory: 5 visible chapters + invisible routing chapters. Chapter count correlates with pack scope, not complexity.

### MP23 — Invisible Infrastructure

Expert packs need complex stage-gating logic (gamestages, cross-mod state, internal triggers) that should be invisible to the player. Create `always_invisible: true` chapters containing routing logic with `gamestage` tasks, `command` rewards, and cross-chapter dependency wires.

Separates player-facing UX from pack-author-facing logic. Player never sees invisible chapters; only experiences clean progression through visible content.

**Real case (Monifactory):** ~11% of quests in invisible chapters. Visible book is a clean tech-tree UI; invisible book runs the voltage-tier gating system. E9E: 56 command rewards in `chapter_one` alone but zero gamestage tasks in visible chapters.

---

## Anti-Patterns

### AP5 — Empty Quest Description (the Silent Node)

Quest has no description — just an item icon and a task. Player sees WHAT (the task item) but not WHY or HOW. Quest book becomes a meaningless checklist.

**Root cause:** Quests auto-generated or bulk-authored without filling in `description`. Recipe catalog approach without context.

**Fix:** Every quest must have at least a one-sentence description answering: (1) what this item does, (2) how to obtain it, (3) what it leads to. For recipe-catalog packs: at minimum include the item's role ("Osmium is Mekanism's base metal").

Catalog chapter recipe cells are an acceptable exception — `rsquare`/`circle` shape, size <= 2.0, single task, catalog chapter context. R18 encodes this exception.

**Expert pack amplification:** For GregTech expert packs where the questbook IS the tutorial system (MP23), missing descriptions have outsized impact — players have no other in-game guidance. Monifactory #2359 explicitly requests "better tutorialisation of basic mechanics."

### AP13 — Premature Item Submission

Player obtains items for a quest's task before the quest is formally unlocked. When the quest finally unlocks, items have been consumed or quest state is corrupted — tasks show "100%" but aren't checked, rewards can't be claimed.

**Root cause:** Quest system allows items to be submitted to locked quests. Player crafts or picks up matching item while quest is still locked; quest system auto-detects and "submits" it.

**Fix:** (1) Design task items to be unobtainable before quest unlocks — gate behind prerequisite chain. (2) Ensure quest system handles pre-submission correctly. (3) For energy/fluid tasks, ensure tracking starts only after quest unlocks. (4) Provide recovery mechanism (repeatable quest, admin command).

Distinct from AP3 (Unfinishable Chapter) — the quest IS reachable in theory; it's the submission timing that corrupts it. Related to R14 because the root cause is often items becoming available before the teaching chain reaches them.

---

## Rules

### R14 — Teach-Then-Do Ordering

**Step 5 priority:** P1

Teaching quests (checkmark/stat/observation + long description) must appear before application quests (item task needing the taught content). Identifies teaching quests by task type + description length threshold. Identifies doing quests by item tasks. Compares dependency_depth: if teaching quest depth > doing quest depth, the order is inverted.

```
teaching = [q for q if checkmark/stat/observation + long desc]
doing = [q for q if item task]
for each doing_quest:
    related_teaching = find_by_same_mod_namespace(doing_quest)
    if depth(related_teaching) > depth(doing_quest):
        ERROR: "Teach quest after doing quest."
```

"Related" determined by: same mod namespace, teaching description mentions the doing quest's task item, or adjacency in dependency chain.

### R15 — Complexity Escalation Within Chapter

**Step 5 priority:** P2

Quests within a chapter should increase in complexity — simple items before complex, low count before high, basic machines before multiblocks. Sorts quests by dependency_depth, estimates complexity (recipe_depth x log(count+1)), flags significant drops (<30% of previous max).

Soft check (INFO level) — complexity drops can be intentional (recovery quests after bottlenecks). The dangerous direction is the reverse: chapter opening with high-complexity items that scare new players.

### R17 — Tool-Reward-Before-Use Ordering

**Step 4 priority:** P2 (reverse check)
**Step 5 priority:** P3 (full scan)

When quest A rewards a tool and quest B needs that tool, B must depends_on A (directly or transitively). Tool rewards include wrenches, hammers, guide books, machine blocks — items classified as "tool" in item registries.

More critical than material bridges — materials can be mined/crafted, but tools typically require specific quest rewards or quest chains. A broken tool-reward chain leaves the player unable to interact with the next mechanic entirely.

Step 4 runs reverse check (does this quest's tool requirement appear as an ancestor's reward?). Step 5 runs full forward scan.

### R18 — Description Coverage

**Step 4 priority:** P1

Non-catalog quests must have descriptions. Catalog cells exempted: `rsquare`/`circle` shape, size <= 2.0, catalog chapter, single task. Everything else: WARNING if no description or description < 20 chars.

```
if not has_desc and not is_catalog_cell:
    WARNING: "Quest has no description. Add HOW + WHY."
```

This is AP5's automated detection. Monifactory CONTRIBUTING.md requires substantive descriptions for all quests.

### R19 — Bottleneck Spacing

**Step 5 priority:** P2

High-difficulty quests (bottlenecks) need breathing room between them. Bottleneck defined as: task count >= 3, OR item count >= 64, OR recipe depth >= 5. Consecutive bottleneck streaks >= 3 trigger WARNING — players need recovery quests between hard challenges.

Ideal difficulty curve is not a straight line but a sawtooth: challenge -> recovery -> challenge. Cesspit.net's backward shortcut (PP2 in mod-reward-design) embodies this: milestone rewards give efficiency loops back, creating natural recovery.

Craftoria #231 Powah chapter: 3 tiers of reactors with no rewards between them — classic bottleneck streak + reward desert (AP18) combination.

### R21 — Hidden Quest Signpost

**Step 5 priority:** P3

Every quest with `hide_until_deps_visible: true` must have a visible signpost. Checks: (1) at least one dependency quest is visible AND its description mentions unlocking new content, OR (2) a nearby visible quest (distance < 3.0) has a description hinting at hidden content.

```
if Q.hide_until_deps_visible:
    has_signpost = any visible dep with "unlock/reveal" in desc
                or any nearby visible quest with description
    if not has_signpost:
        WARNING: "Hidden quest with no discovery path."
```

Never combine `hide_until_deps_visible: true` with `hide_dependency_lines: true` on the same quest — player has zero signal that content exists. Limit `hide_until_deps_visible` to truly secret/bonus content; don't use on main-progression quests.

---

## Player-Perspective

### PP5 — Context Void

Quest shows only an item icon and a task count with no description. Player completes mechanically — "get 4 iron ingots" — without understanding the item's role. Quest book becomes a shopping list.

**Three information needs per quest:** WHAT (item — shown by task icon), HOW (obtain method — description), WHY (what it leads to — description or reward). When description is empty, player gets WHAT from icon but must figure out HOW and WHY alone.

**Minimum viable description:** One sentence combining HOW and WHY: "Smelt iron ore in a furnace — you'll need this for your first set of tools." Costs nothing to write, transforms checklist item into learning moment.

**Expert pack amplification (Monifactory #2359):** Player explicitly requests better tutorialisation. The Aqueous Accumulator quest doesn't mention pump configuration — player wastes ~30 minutes before discovering the mechanic. In expert packs where the questbook IS the tutorial (MP23), PP5 is amplified because there's no alternative in-game guidance.

---

## Cross-References

| This module's ID | Related in other modules | Relationship |
|---|---|---|
| MP3 Acknowledgement Gate | mod-reward-design MP15 | Acknowledgement gate often rewards the tool for the next quest |
| MP11 Teach-Then-Do | mod-reward-design MP14 | Doing quest's reward should bridge to the next teaching cycle |
| MP19 Chapter-as-Stage | mod-reward-design AP8 | Chapter boundaries define reward budget tiers |
| MP23 Invisible Infrastructure | mod-reward-design MP29 | Command rewards power the invisible routing |
| AP5 Empty Description | mod-reward-design AP6 | Dead-end rewards + empty descriptions compound player confusion |
| R14 Teach-Then-Do | mod-reward-design R10 | Teaching order affects reward bridge direction |
| R17 Tool-Reward-Before-Use | mod-reward-design MP15/R11 | Tool reward pattern + wrong tool detection |
| R18 Description Coverage | mod-reward-design R28 | Both are Step 4 P0/P1 checks that run per-node |
| R19 Bottleneck Spacing | mod-reward-design AP18 | Bottleneck streaks cause reward deserts |
| R21 Hidden Signpost | mod-reward-design MP17 | Hub concentration relies on visible hubs as signposts |
| PP5 Context Void | mod-reward-design PP6 | Wrong tool reward + no description = maximum confusion |
