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
| AP20 | Quest Tab Overwhelm (info-dump chapter) | Step 2 | Medium | kitchen-sink, create |
| R14 | Teach-Then-Do Ordering | Step 5 | P1 | all |
| R15 | Complexity Escalation | Step 5 | P2 | all |
| R17 | Tool-Reward-Before-Use | Step 4/5 | P2/P3 | all |
| R18 | Description Coverage | Step 4 | P1 | all |
| R19 | Bottleneck Spacing | Step 5 | P2 | all |
| R21 | Hidden Quest Signpost | Step 5 | P3 | all |
| R40 | Effort Preview in Description | Step 4/5 | P2 (INFO) | expert, kitchen-sink |
| R41 | Early-Game Flexible Mode | Step 5 | P2 (INFO) | all |
| R47 | Companion Tool Delegation | S4/S5 | P3 (INFO) | companion, tutorial |
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

**Cross-pack comparison (Phase 3 Cycle 5 — GT-O vs Monifactory):** GregTech-Odyssey uses **ZERO command rewards** in all sampled visible chapters (EV: 0 commands/82 item rewards, HV: 0 commands/94 item rewards), despite being a similar GregTech expert pack. GT-O achieves stage gating through `hide_quest_until_deps_visible: true` at chapter level + `quest_links` for cross-chapter references (3-6 per chapter in EV, more in HV) instead of command-based gamestage routing. Two viable invisible infrastructure approaches emerge: (1) **command-heavy** (Monifactory: 26 commands in dependency_chain, E9E: 56 commands) with explicit gamestage tasks in invisible chapters, and (2) **dependency-implicit** (GT-O: 0 commands in visible chapters) with visual gating via `hide_quest_until_deps_visible` and cross-chapter `quest_links`. GT-O's 14 voltage-tier chapters (ULV through OPV) use quest_links extensively (EV: 6 links, HV: multiple links with shape overrides) to reference quests across tiers without duplicating data. Both approaches produce clean player-facing UX but differ in implementation: command-heavy requires invisible chapters + gamestage tasks; dependency-implicit relies on FTB Quests' native dependency resolution.

---

## Anti-Patterns

### AP5 — Empty Quest Description (the Silent Node)

Quest has no description — just an item icon and a task. Player sees WHAT (the task item) but not WHY or HOW. Quest book becomes a meaningless checklist.

**Root cause:** Quests auto-generated or bulk-authored without filling in `description`. Recipe catalog approach without context.

**Fix:** Every quest must have at least a one-sentence description answering: (1) what this item does, (2) how to obtain it, (3) what it leads to. For recipe-catalog packs: at minimum include the item's role ("Osmium is Mekanism's base metal").

Catalog chapter recipe cells are an acceptable exception — `rsquare`/`circle` shape, size <= 2.0, single task, catalog chapter context. R18 encodes this exception.

**Expert pack amplification:** For GregTech expert packs where the questbook IS the tutorial system (MP23), missing descriptions have outsized impact — players have no other in-game guidance. Monifactory #2359 explicitly requests "better tutorialisation of basic mechanics."

**Insufficient-description variant (Craftoria #781):** Description exists but delegates all guidance to an external source ("the AE2 guide"). When the external source doesn't cover the specific pack context (how AE2 power works in a pack with 5+ energy systems), the delegation becomes an AP5 variant — the quest has words but no useful guidance.

**Missing-guidance variant (NFwC #333):** Quest chain lacks guidance for biome-dependent items (dyes, cactus, kelp) and tool prerequisites (wrench, speed controller). Players must rely on external knowledge or trial-and-error. The issue explicitly requests the quest book to "directly give these necessary items" rather than assuming biome availability. AP5 variant: not empty description but missing critical context about *where* to find prerequisite items in a seed-dependent world.

**Undocumented-prerequisite variant (GregTech-Odyssey #1440):** Stainless Steel 15 5ph requires an EV-level mixer with platline setup, but "No indication in questbook." The quest book shows the task but not the infrastructure chain needed to complete it. AP5 + PP5 compound in expert packs: the quest tells you WHAT but not HOW, and the HOW requires multi-step infrastructure that's not covered elsewhere.

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

**Signpost-adequacy variant (Architect's Exodus #12623):** After defeating Skol and Hati, player has no clear guidance about where to go next (Asgard to fight Maledictus). The quest scroll text exists but is triggered by consuming the twin's heart — a non-obvious action. Player: "Your just kinda left in the blank to go fight him but doesn't say where." Pack dev response confirms the guidance exists but players consistently miss it. PP5 variant: description exists but is insufficient — the signpost is present but not prominent enough.

**Chapter-coverage gap (Craftoria #781):** AE2 chapter's first quest references the AE2 in-game guide but omits critical information about power generation (vibrant chamber, Energy Acceptor, ME controller). Player: "if the AE2 guide is the answer, why do we have dozens of other quests?" This is a chapter-level PP5: the individual quests exist but the chapter as a whole has a guidance gap at the entry point.

**Cross-tier effort spike (GregTech-Odyssey #1602):** HV tier requires 400+ MV motors and 37 multiblock blocks, but the quest book doesn't prepare players for this massive effort jump from LV/MV. Player describes "easily running out of motivation" and "falling into a trap of working all day and getting nothing done." PP5 variant: the quest book shows the tasks but not the *scale* of work required, creating a context void at tier transitions in expert packs.

**Expert pack tool-gating void (NFwC #333):** Quest chain requires gold/redstone items that are biome/seed-dependent and assumes availability without guidance. The issue explicitly asks for "wrench and speed controller to be given directly" because the quest book doesn't explain where to find them in a world without chain mining. PP5 variant: the quest assumes a resource-gathering method that the quest book doesn't teach.

**任务书的信息密度与引导能力矛盾（跨包观察）：** 从多个高好评包的攻略标题中可以观察到一个反复出现的模式：GTNH 的玩家写了"Better GTNH（任务书不会告诉你的）"，E2E 的玩家写了"Enigmatica 2: Expert 刚开始你就希望知道的技巧"（MC百科 21,000+ 阅读），RAD2 的玩家写了"RAD2中期游玩心得"。这些包都有 600-3000 个任务和 98-100% 的好评率，说明问题不在于任务数量不够多。信息密度（任务数量、描述长度）和引导有效性（玩家是否真的能从任务书中学到所需知识）是两个独立的维度。高任务数量提供了覆盖面，但不保证在正确的时机以正确的方式传达了正确的信息。

[Phase 2 Cycle 8 - MC百科 GTNH https://www.mcmod.cn/modpack/1.html, E2E https://www.mcmod.cn/modpack/23.html, RAD2 http://www.mcmod.cn/modpack/419.html]

### R40 -- Effort Preview in Description (Tier Transition Context)

**Step 4 priority:** P2 (INFO)
**Step 5 priority:** P3 (INFO)
**Data dependency:** Chapter-level effort statistics

Quest descriptions at technology tier transitions must include an effort preview -- a statement about the scale of work required at the new tier. Addresses the #1 cause of player burnout at tier boundaries: the surprise effort spike. Description should mention resource counts, new infrastructure needs, or time investment.

**Detection heuristic:** Scan for effort keywords (multiblock, infrastructure, automation, N items/blocks, significant, prepare, stockpile, etc.) in descriptions of tier-transition quests.

**Why:** GregTech-Odyssey #1602 -- "even for an expert, being asked to make so many motors at HV is easy to make the player burn out." Monifactory #2359 -- 30 minutes wasted on pump configuration due to missing description context.

**Source:** GregTech-Odyssey #1602, Monifactory #2359

### R41 -- Early-Game Flexible Progression Mode

**Step 5 priority:** P2 (INFO for early-game linear chains)
**Data dependency:** Chapter order index + progression_mode

The first N chapters (default N=3, configurable) should use `flexible` progression mode even if the pack's overall mode is `linear`. Early-game linear gating forces new players into a single path before they understand the pack's scope. Early chapters should serve as orientation -- teach and orient, don't gate and restrict.

**Why:** Craftoria #607 recommends `flexible` mode for Iron's Spells early gating -- crying obsidian creates unnecessary bottleneck. "Flexible mode allows for cleaner early game progression." Expert packs (Monifactory, GT-O) mitigate by using invisible routing chapters for linear logic while visible chapters stay flexible.

**Source:** TeamAOF/Craftoria #607

### 早期教学快速推入策略

高难度包的早期教学面临一个独特的时间窗口问题：玩家的新奇感快速消退，惩罚性的时间门控在早期游戏中失败，因此必须在玩家热情最高的前几个任务中完成核心机制的教学并快速推入中期内容。具体做法是：前 3-5 个任务应包含明确的教学文本，介绍包的核心差异化机制——不是"提交 X 个物品"的纯操作任务，而是结合了独特机制、彩蛋或随机元素的引导性任务，让玩家在钩住的同时学会怎么玩。教学任务不应假设玩家知道模组的默认行为，每个关键机械原理都应该有对应的教学节点。[Phase 3 Cycle 8 - mcmod.cn/post/4382.html]

这个策略与 R14（Teach-Then-Do Ordering）和 R41（Early-Game Flexible Mode）形成三层教学框架：R41 保证早期不锁死路径（结构层），教学快速推入保证早期传达关键知识（内容层），R14 保证教学节点始终先于应用节点（顺序层）。三层共同作用的结果是：玩家在早期既不迷路（R41），也不无知（教学推入），也不会先做后学（R14）。

### R47 — Companion Tool Delegation (伴生工具委托)

**Step 4 priority:** P3 (INFO — 每节点检查)
**Step 5 priority:** P3 (INFO — 全量扫描)
**数据依赖:** 包 modlist（确定 recipe viewer 和文档 mod 是否在场）

**检查什么：** 当 questbook 以 companion 模式运行时（R46 声明），quest 描述不应重复配方查看器（EMI/JEI/HEI）或模组自身的游戏内文档（Patchouli guides、Ponder 系统）中已有的信息。检测描述中包含逐字配方信息（输入→输出模式、机器加工步骤）但配方查看器已经显示相同内容的情况。此规则是 AP5（空描述）的反面——AP5 标记过于稀疏的描述，R47 标记在 questbook 声明角色下过于冗余的描述。

```
if pack.questbook_role == "companion":
    for each quest Q:
        desc = Q.description
        if contains_recipe_pattern(desc):  # "X + Y = Z", "put X in Y to get Z"
            if recipe_viewer_available:  # EMI/JEI in pack
                INFO: "Description contains recipe info already shown in {viewer}.
                       Consider delegating to the recipe viewer."
        if references_ponder_system(desc) and mod_has_ponder:
            INFO: "Description explains a Ponder-able mechanic.
                   Consider referencing the Ponder entry instead."
```

此规则对 tutorial 模式的包反向适用：如果 `questbook_role == "tutorial"` 而描述委托给 EMI/JEI（"check EMI for the recipe"），标记为 WARNING——tutorial 模式应该教学，而非委托。

**设计哲学基础：** Pyritie/TFG Modern #3656 明确阐述了三通道信息架构：questbook 负责方向（direction），field guide 负责机制（mechanics），EMI 负责配方（recipes）。每个通道有特定的不重叠的角色。当 questbook 描述侵入其他通道的领域时，信息架构的一致性被破坏，玩家不确定在哪里查找什么信息。

**违反了会怎样：** 不是功能性错误，而是设计一致性问题。Companion 包中过于详细的描述增加了维护成本（配方变更需要同步更新 questbook 和 EMI），同时向玩家发送矛盾信号——如果 questbook 告诉你一切，为什么还需要 EMI？

**来源：** Pyritie/TFG Modern #3656; Phase 3 Cycle 9

**Scope note (Phase 4 Review):** R47 的正向检查仅适用于声明了 `questbook_role: companion` 的包（在 46 包数据集中约占 4%）。反向检查（tutorial 包不应委托）适用范围更广。R47 与 R46 强耦合——如果 R46 的角色声明不成立，R47 的正向检查失去前提。考虑将 R47 重构为更通用的"questbook 描述应与包的信息架构一致"规则，不依赖特定角色声明。

### Monifactory #2359：教学不足的典型失败案例

Monifactory Issue #2359 由 LunatiK-ExpiX 提出，标题直接指向问题核心——"Better Tutorialisation of Basic Mechanics"。该 issue 指出"教程化（Tutorialisation）在制作这个包时可能没有被充分考虑"，并给出了具体的失败场景：Infiniter Water 和 LV Pumps 任务几乎不提供如何使用物品的信息；Aqueous Accumulator 让玩家困惑，"可能导致他们花费超过需要的时间，30 分钟后才意识到需要配置泵"。这不是 AP5（空描述）——任务确实存在且包含物品要求，但描述中缺少了关键的操作指引：不是告诉你 WHAT（提交水泵），而是缺少 HOW（如何配置泵的输入输出）和 WHY（为什么需要配置泵而不是直接使用）。[Phase 3 Cycle 8 - github.com/Omicron-Industries/Monifactory/issues/2359]

该 issue 的解决方案提议是给介绍 Gregtech 关键特性的任务增加更多机械原理说明——这恰好对应 MP11（Teach-Then-Do）的设计模式：先有一个教学节点（checkmark 任务 + 详细描述水泵配置方法），再有一个应用节点（item 任务要求提交已配置的水泵）。在 expert pack 中，任务书就是教程系统（MP23），教学缺失意味着玩家完全没有游戏内引导。FTB Quests 的多种任务类型（物品、流体、能量、维度、统计、击杀、坐标、复选框）可以组合使用来实现教学效果：复选框任务用于纯教学节点（无需提交物品），文本面板插入背景故事或教学说明，维度任务在玩家访问特定领域时自动触发。教学节点应位于实践节点的前置依赖位置，这是 R14 的检查逻辑。[Phase 3 Cycle 8 - mcmod.cn/post/1416.html]

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
