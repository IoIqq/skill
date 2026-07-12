# FTB Quests — Micro-Patterns [ARCHIVED]

> **ARCHIVED:** This file has been superseded by the modular system.
> Content redistributed to: `mod-item-reachability.md`, `mod-dependency-graph.md`, `mod-teaching-pacing.md`, `mod-reward-design.md`, `mod-system-safety.md`, `mod-atm-signature.md`.
> Kept for git history reference. See `module-index.md` for the current structure.

---

## Section Navigation & Load Phase

| Section | Content | SKILL.md Step | Scope |
|---|---|---|---|
| Part 1: Task Combination (MP1–MP5) | 单 quest 的 task 组合公式 | Step 4 (node generation) | 节点级 |
| Part 2: Dependency Topology (MP6–MP10) | 相邻 quest 的依赖拓扑 | Step 2 (outline) / Step 3 (skeleton) | 章节级 |
| Part 3: Quest-Internal Pacing (MP11–MP13) | quest 内部节奏 | Step 2 (outline) / Step 4 (node) | 混合 |
| Part 4: Reward Bridging (MP14–MP18) | reward 桥接模式 | Step 4 (node generation) | 节点级 |
| Part 5: Stage Marking (MP19–MP23) | 阶段标记模式 | Step 2 (outline) | 章节级 |
| Part 6: Anti-Pattern Detection (MP24–MP26) | 反面模式检测信号 | Step 5 (validation) | 参考 progression-rules |
| Part 7: Extended Patterns (MP27–MP30) | 补充类型模式 (fluid/energy/command/gamestage) | Step 4 (node generation) | 节点级 |
| Part 8: Cycle 2 Patterns (MP31–MP32) | Cycle 2 新增模式 (structure/min_tasks) | Step 4 (node generation) | 节点级 |
| Part 9: Cycle 3 Patterns (MP33–MP34) | Cycle 3 新增模式 (advancement/loot table) | Step 4 (node generation) | 节点级 |
| Player-Perspective (PP1–PP7) | 玩家体验模式 | Step 2 (背景知识) | 规划阶段 |
| Scope Annotation Table | 全模式适用范围速查 | — | 参考 |

> **注意：** Part 2 和 Part 5 的模式需要在 Step 2/3 确定章节结构时就决定，Step 4 逐节点生成时已无法改变。Step 4 应重点参考 Part 1、Part 4、Part 7 和 Part 9。Part 6（MP24–MP26）是 anti-patterns.md 和 progression-rules.md 之间的桥梁概念，AI 应直接参考 R 规则而非 MP 检测信号。

---

Cross-pack micro-level design patterns extracted from real FTB Quests configurations. These complement the macro-level layout templates (§atm-layout-patterns) and pack-type patterns (§pack-type-patterns) in the design guide by addressing the **quest-granularity** decisions: how tasks combine within a single quest, how adjacent quests wire together, and how rewards bridge the player from one step to the next.

## Summary of findings

The study analyzed quest configs from **23 shipped modpacks** spanning kitchen-sink (ATM-10 4,601 quests / 64 chapters, ATM-9 ~2,300 quests / 67 chapters, ATM-8 ~1,000 quests / 32 chapters, ATM-11, All-the-Mons ~2,400 quests / 73 chapters, Craftoria ~unknown quests), Create-focused (Create: Delight Remake 2,295 quests, Mechanomania 395 quests, Create: Astral ~650 quests / 12 chapters, Create Skylands), expert (Monifactory ~248 quests / 14 chapters with raw data, Enigmatica 9 Expert 22 chapters with raw data, Enigmatica 10 issue-tracker data), skyblock (ATM9-Sky, All-the-mods-10-Sky ~2,860 quests / 52 chapters, FTB Skies 2 issue-tracker data), magic (Arcana ~550 quests / 42 chapters), RPG (Prominence II, Finality Genesis 35 chapters / 8 groups, Era of Black Death 17 chapters / 5 groups), and ARPG (Craft to Exile Dissonance 12 chapters / act-based) genres. Three macro-level patterns from the design guide (F1 guidance-vs-gating, F2 convergence-in-crafting, P6 item-task dominance) hold across all packs; the micro-patterns below fill the gap between those principles and the actual per-quest authoring decisions.

The single most transferable insight is that **task multiplicity within a quest signals a synthesis point, not a checklist** — across all packs, quests with 2+ item tasks appear at crafting-chain convergence nodes (the ATM Star component quest has 12 item tasks; AE2's starter quest has 2 — charger AND inscriber). Conversely, 90%+ of quests carry exactly 1 task, making "one quest = one thing to do" the universal baseline. Deviating from this baseline should be a deliberate signal to the player that "this quest requires you to bring multiple things together." Cycle 3 reinforces this: Era of Black Death uses strict 1-task-per-quest across all 17 chapters, while Monifactory and Finality Genesis use multi-task quests at synthesis points.

The second key finding is that **dependency topology correlates with pack genre**, not with pack size. Kitchen-sinks use shallow fan-out (depth 3–5) with `flexible` progression; expert packs use deep chains (depth 8–18) with `default`/`linear` progression; and RPG/adventure packs use the widest task-type diversity (7+ types) with dependency-gated image reveals as the primary progression UX. Cycle 3 confirms: Finality Genesis (`progression_mode: "default"`, locked) and Craft to Exile Dissonance (act-based linear chains) both use locked progression, while the ATM kitchen-sink series consistently uses `flexible`.

The third key finding (from Cycle 2 Phase 2 player feedback cross-validation) is that **the mod-unification trap** — where multiple mods provide items with the same display name but different namespaces — is a pervasive source of quest errors that static analysis struggles to detect. It manifests as both description-reality mismatches (AP1) and dead-end rewards (AP6/PP6), and requires the quest author to know which mod's variant is canonical for each recipe chain.

The fourth key finding (Cycle 3, expanded Cycle 6) is that **expert packs converge on command rewards as invisible infrastructure** rather than gamestage tasks in visible chapters. Monifactory's `dependency_chain` chapter uses 26 gamestage tasks + 26 command rewards as dedicated routing, while all 13 visible chapters have zero gamestage tasks. E9E goes further: 56 command rewards in `chapter_one` alone (83% of reward sections) but zero gamestage tasks in visible chapters. The visible quest book stays clean; the invisible logic runs through command rewards. Cycle 6 Phase 3 reveals a **3-generation command reward evolution lineage**: E6 (MC 1.16.5, 455 commands as `/execute at @p run loot spawn` vanilla loot delivery) → E9E (MC 1.19.2, 56 commands as `/gamestage add` progression routing) → E10 (MC 1.21, 0 commands, 28 native reward tables). Command rewards evolved from a workaround for missing native loot table support (Gen 1) to a progression routing tool (Gen 2) to obsolescence (Gen 3). This validates MP29 (Command Reward) and MP23 (Invisible Infrastructure) with 4-source data (Monifactory + E9E + E6 + E10).

The fifth key finding (Cycle 3 Phase 2) is that **high-quality expert packs can have zero quest design complaints on their public issue trackers.** Enigmatica 10 — a high-profile MC 1.21.1 expert pack — has no quest-related issues among ~20 recent GitHub issues, while comparable packs (Craftoria, Monifactory, FTB official packs) have multiple. This negative evidence suggests that effective quest QA processes (playtesting, internal review) can eliminate the common AP1–AP8 failures before players encounter them. The contrast with FTB Architect's Exodus (11+ quest issues in its first months) and Craftoria (6+ quest design issues) highlights that quest quality is not inherent to the pack genre but depends on authoring discipline.

The sixth key finding (Cycle 3 Phase 3) is that **FTB Quests natively supports two under-utilized pattern types** — advancement tasks and reward tables — that serve distinct design roles not covered by existing patterns. Advancement tasks (MP33, observed in Enigmatica 10) bridge the vanilla advancement system with the quest book's dependency graph as silent auto-completing checkpoints. Reward tables (MP34, observed in Craftoria) provide weighted randomized rewards across multiple loot tiers, adding excitement and variety on top of deterministic reward bridges (MP14–MP18). Both are native FTB Quests features requiring no KubeJS scripting, yet fewer than half of the audited packs use them in a patterned way.

---

## Scope Annotation Table — Pattern Applicability by Pack Type

The following table maps every micro-pattern to its applicable pack types, the SKILL.md phase where it's most relevant, and the data-source confidence level. Patterns marked "single-source" were observed in only one pack and should be applied with caution — they may be kitchen-sink-specific or ATM-specific rather than universally transferable.

**Pack type legend:** `all` = all audited pack types | `kitchen-sink` = ATM-style broad-scope packs | `expert` = GregTech/Monifactory-style gated packs | `skyblock` = resource-constrained starts | `story` = RPG/narrative/adventure packs | `create` = Create-focused packs

| Pattern | pack_types | Phase | Source confidence |
|---|---|---|---|
| MP1 Single-Item Gate | all | Step 4 | High (15 packs) |
| MP2 Multi-Item Synthesis | all | Step 4 | High (15 packs) |
| MP3 Acknowledgement Gate | all | Step 4 | High (15 packs) |
| MP4 Escalation Ladder | all | Step 4 | † ATM Signature — High (ATM-10, ATM-9, ATM-10-Sky) |
| MP5 Dimension + Item Composite | kitchen-sink, story, skyblock | Step 4 | High (8+ packs) |
| MP6 Linear Chain | all | Step 2 | High (15 packs) |
| MP7 Fan-Out | all | Step 2 | High (15 packs) |
| MP8 Fan-In / Convergence | all | Step 2 | High (15 packs) |
| MP9 Diamond (pick-and-rejoin) | expert, story | Step 2 | High (Monifactory, Create: Delight, Create: Astral) |
| MP10 Independent Island | kitchen-sink, create | Step 2 | High (8+ packs) |
| MP11 Teach-Then-Do | all | Step 2 + Step 4 | High (8+ packs) |
| MP12 Tier Escalation | all | Step 2 | High (8+ packs) |
| MP13 Explore-Then-Craft | kitchen-sink, story, skyblock | Step 2 | High (ATM-10, ATM-9, ATM-10-Sky) |
| MP14 Material Bridge | all | Step 4 | High (15 packs) |
| MP15 Tool Reward | all | Step 4 | High (15 packs) |
| MP16 XP Drip | kitchen-sink (ATM-style generous) | Step 4 | † ATM Signature — High (ATM-10, ATM-9, ATM-8); Monifactory "varies" (no concrete XP drip data) |
| MP17 Hub Concentration | create | Step 2 | Medium (Create: Delight primary; kitchen-sink removed — no evidence in ATM-10) |
| MP18 Choice Reward | expert, story | Step 4 | Medium (3 packs) |
| MP19 Chapter-as-Stage | all | Step 2 | High (15 packs) |
| MP20 Shape-as-Tier Signal | kitchen-sink (ATM-style) | Step 2 | † ATM Signature — High within ATM series; Low outside (curated packs use 3-8% explicit shape) |
| MP21 Dimension-as-Stage-Gate | kitchen-sink, story | Step 2 | † ATM Signature — High (ATM-10, ATM-9); no independent kitchen-sink validation |
| MP22 Material-Tier Spine | kitchen-sink | Step 2 | † ATM Signature — High (ATM-10, ATM-9, ATM-8, ATM-10-Sky); not observed in non-ATM kitchen-sinks |
| MP23 Invisible Infrastructure | expert | Step 2 | High (Monifactory + E9E, multi-source Cycle 3) |
| MP24 Tier-Reachability Check | all | Step 5 | → See R1/R2 |
| MP25 Dependency-Order Check | all | Step 5 | → See R14 |
| MP26 Reward-Continuity Check | all | Step 5 | → See R10 |
| MP27 Fluid Task Gate | kitchen-sink, expert, create | Step 4 | Medium (tech packs) |
| MP28 Energy Threshold Gate | kitchen-sink, expert, create | Step 4 | Medium (tech packs) |
| MP29 Command Reward (invisible logic) | expert, story, kitchen-sink (legacy) | Step 4 | High (Monifactory + E9E + E6 + E10, 4-source Cycle 3+6) |
| MP30 Gamestage Bridge | expert | Step 2 + Step 4 | Medium (Monifactory primary, validated by E9E command pattern) |
| MP31 Structure Discovery Gate | skyblock, kitchen-sink, story | Step 4 | Medium (ATM-10-Sky, ATM-9, All-the-Mons) |
| MP32 min_tasks Modifier (partial completion) | create | Step 4 | Low (Create: Astral only, single-source; kitchen-sink removed — no evidence in 15-pack audit) |
| MP33 Advancement Gate (vanilla advancement checkpoint) | expert (verified) | Step 4 | Low (Enigmatica 10 only, 3 cases; `all` removed — not observed in ATM-10, Create: Delight, Monifactory) |
| MP34 Loot Table Reward (randomized reward via reward tables) | all | Step 4 | Medium (Craftoria + AoF3, multi-source Cycle 4+6) |
| PP1–PP7 Player-Perspective | all | Step 2 | High (player feedback) |

> **† ATM Signature Patterns:** MP4, MP16, MP20, MP21, MP22 的核心证据全部来自 AllTheMods 团队的包（ATM-8/9/10/10-Sky），其具体实现形态是 ATM 设计哲学的体现而非 FTB Quests 的通用模式。概念（escalation, XP reward, shape semantics, dimension gating, material tiers）是通用的，但案例全是 ATM 做法。Non-ATM 包作者阅读时应意识到这一点。
>
> **Single-source patterns (需更多数据确认):** MP32 (Create: Astral min_tasks), MP33 (Enigmatica 10 advancement gate). MP4, MP13, MP20, MP21, MP22 were single-source in Cycle 1 but are now validated across the ATM series (ATM-8, ATM-9, ATM-10, ATM-10-Sky). MP23 and MP29 were single-source in Cycle 1 but are now validated across Monifactory + E9E in Cycle 3 and further with E6 + E10 in Cycle 6 (4-source). MP34 was single-source (Craftoria only) in Cycle 4 but is now validated by AoF3 (16 reward tables) in Cycle 6 — TeamAOF reward table lineage confirmed (AoF3→Craftoria).

---

## Part 1: Task Combination Formulas

How tasks within a single quest combine — and what the combination signals to the player.

### MP1 — Single-Item Gate (the universal baseline)

**Applicable when:** designing any standard progression step in any pack genre. This is the default — 90%+ of quests across all audited packs.

**Implementation:** One `item` task with `count: 1` (or the recipe's output count). No `consume_items`, no `only_from_crafting`. The quest title names the item; the description explains *why* the player wants it and *how* to get it. Shape inherits the chapter's `default_quest_shape`.

The single-task quest is the atomic unit of FTB quest design. It works because the quest UI already shows the item icon, count, and completion status — the quest author's job is context, not enumeration. When a mod has 20 recipes to teach, that's 20 single-task quests, not one 20-task quest.

**Real case (ATM-10, AllTheModium chapter):** The first quest in the AllTheModium chapter requires one `minecraft:netherite_ingot` — a simple gate that says "you need netherite before you can start working with AllTheModium." The quest is a `gear` shape `size: 2.0` at `(0, 0)` (the chapter root), with a single task and a single reward (the AllTheModium guide book). Every subsequent AllTheModium quest builds on this root.

```
# ATM-10 allthemodium.snbt — root quest
{
    shape: "gear"
    size: 2.0d
    tasks: [{ id: "0AB9BED5E5144BAC", item: { count: 1, id: "minecraft:netherite_ingot" }, type: "item" }]
    rewards: [{ id: "3B12B107212D8F38", item: { count: 1, id: "patchouli:guide_book" }, type: "item" }]
    x: 0.0d
    y: 0.0d
}
```

**Source:** [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) `config/ftbquests/quests/chapters/allthemodium.snbt`

### MP2 — Multi-Item Synthesis Bundle

**Applicable when:** a quest represents a crafting convergence point where multiple components from different sources must be brought together. This is the exception, not the rule — used deliberately to signal "this is a synthesis step."

**Implementation:** 2–12+ `item` tasks within one quest. Each task is a distinct component. The quest is typically larger than normal (`size: 1.5–2.0`), uses a distinctive shape (often `hexagon` or the chapter's milestone shape), and has a rich reward (the assembled product, or XP levels + a next-step material). Do NOT set `consume_items: true` on individual tasks — the crafting table already consumed them.

The key insight is that multi-item tasks signal **cross-mod or cross-system synthesis** to the player. When they see a quest with 6 item icons, they know "I need to pull from 6 different mods/systems." This is a visual affordance, not a mechanical necessity.

**Real case (ATM-10, ATM Star chapter):** The cauldron component quest has 12+ item tasks, each from a different mod (Forbidden & Arcanus runes, arcane crystals, polished darkstone, quantum injector, etc.). The quest uses `hexagon` shape, `hide_dependent_lines: true`, and rewards the player with dust_obsidian, steel_ingots, souls, and 5 XP levels — materials for the NEXT synthesis step.

```
# ATM-10 achapter_2r_6the_atm_star.snbt — cauldron component
{
    shape: "hexagon"
    tasks: [
        { count: 4L, item: { count: 4, id: "forbidden_arcanus:rune_block" }, type: "item" }
        { item: { count: 1, id: "forbidden_arcanus:quantum_injector" }, type: "item" }
        { count: 5L, item: { count: 5, id: "forbidden_arcanus:arcane_crystal_block" }, type: "item" }
        # ... 9 more item tasks from forbidden_arcanus
    ]
    rewards: [
        { count: 10, item: { count: 1, id: "mekanism:dust_obsidian" }, type: "item" }
        { count: 5, item: { count: 1, id: "alltheores:steel_ingot" }, type: "item" }
        { count: 5, item: { count: 1, id: "forbidden_arcanus:soul" }, type: "item" }
        { type: "xp_levels", xp_levels: 5 }
    ]
}
```

**Source:** [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) `config/ftbquests/quests/chapters/achapter_2r_6the_atm_star.snbt`

**Quantified:** Across ATM-10's 64 chapters, the ATM Star chapter has the highest multi-task density (107 item tasks across ~30 quests ≈ 3.6 tasks/quest average). Mekanism chapter: 284 item tasks / ~90 quests ≈ 3.2 tasks/quest. Basic Tools chapter: 83 item tasks / ~50 quests ≈ 1.7 tasks/quest. Standard mod chapters hover at 1.0–1.2. The gradient is clear: **more tasks per quest = more synthesis expected**.

### MP3 — Acknowledgement Gate (Checkmark / Stat / Observation)

**Applicable when:** the player needs to read a tutorial or witness a mechanic before proceeding. The task is not "do something" but "acknowledge you've read this."

**Implementation:** A single `checkmark` task (click-to-complete), or a `stat` task with `value: 1` on `minecraft:play_time` (auto-completes after 1 tick), or an `observation` task (auto-completes when the player looks at the relevant block/entity). The quest has a long `description` (the actual tutorial text) and a `subtitle` with the key takeaway. The reward is the tool or item needed for the next quest.

This pattern separates **teaching** from **doing**. A tutorial quest with a checkmark task says "read this, then move on." The next quest's item task says "now apply what you learned." Mixing the tutorial text into the item quest makes it easy to skip; separating them forces the player to at least open the acknowledgement quest before the next one unlocks.

**Real case (Create: Delight Remake, Feast_Afoot chapter):** The humidity-system tutorial uses a `stat: minecraft:play_time value: 1` task with a `title: "湿度系统"` and a multi-line description explaining the 5-tier humidity mechanic. The subtitle color-codes the tiers (`&4干旱&r、&6干燥&r、&a一般&r、&9湿润&r、&1潮湿`). The reward is the hygrometer tool the player needs for the next farming quest.

```
# Create: Delight Remake — Feast_Afoot humidity tutorial
{
    description: [
        "种子有对应&9湿度需求&r，&4偏移1级减慢生长&r，&4偏移2级&r及以上时&4大幅减慢生长甚至无法生长&r"
        "不同生物群系有不同&e自然湿度&r，且&e随季节变化&r"
    ]
    icon: "eclipticseasons:hygrometer"
    shape: "rsquare"
    tasks: [{ id: "...", stat: "minecraft:play_time", title: "湿度系统", type: "stat", value: 1 }]
    rewards: [{ id: "...", item: "eclipticseasons:hygrometer", type: "item" }]
}
```

**Source:** Create: Delight Remake `config/ftbquests/quests/chapters/Feast_Afoot.snbt` (data from reference §20g)

### MP4 — Escalation Ladder (Kill / Stat progression)

**Applicable when:** a skill or activity needs repeated practice with increasing difficulty. Common in combat-training lines, farming automation, or boss-progression arcs.

**Implementation:** A chain of quests where each has the same `type` but an escalating `value`. For kill quests: `value: 5` → `value: 10` → `value: 25` → `value: 50` → `value: 100`. Each quest `depends_on` the previous. Rewards also escalate (common drops → rare drops → XP levels → loot table rolls). Use `hide_until_deps_visible: true` on all but the first quest so the chain progressively reveals.

The escalation ladder teaches the player through repetition with increasing stakes. The first quest is easy (5 zombies = go fight some zombies), the last is a serious grind (100 zombies = build a mob farm). The dependency chain makes the progression visible and gated.

**Real case (ATM-10, Bounty Board chapter):** 87 kill tasks across the chapter, organized as escalating ladders per mob type. The zombie ladder: 5→10→25→50→100 kills, each depending on the previous. The first quest (`value: 5`) has `hide_until_deps_visible: false` (always visible); subsequent quests have `hide_until_deps_visible: true` (progressive reveal). Rewards escalate from 5 rotten_flesh + 10 XP → random loot table + 25 XP → rare drops + 50 XP.

```
# ATM-10 bounty_board.snbt — zombie kill ladder (first 2 steps)
{
    id: "2B05A29C62676EB2"
    hide_until_deps_visible: false
    tasks: [{ entity: "minecraft:zombie", type: "kill", value: 5L }]
    rewards: [
        { count: 5, item: { count: 1, id: "minecraft:rotten_flesh" }, type: "item" }
        { type: "xp", xp: 10 }
    ]
    x: -7.0d, y: -2.5d
}
{
    dependencies: ["2B05A29C62676EB2"]
    id: "444ACE285311ECB4"
    hide_until_deps_visible: true
    tasks: [{ entity: "minecraft:zombie", type: "kill", value: 10L }]
    rewards: [
        { exclude_from_claim_all: true, table_id: 487623848494439020L, type: "random" }
        { type: "xp", xp: 25 }
    ]
    x: -7.0d, y: -4.0d
}
```

**Source:** [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) `config/ftbquests/quests/chapters/bounty_board.snbt`

> **† ATM Signature:** Escalation Ladder 的具体形态（kill-count bounty board, 5→10→25→50→100 递增）主要来自 ATM 系列。Concept（activity + escalating value）是通用的，但实现需要包内有 mob-grind 或重复性活动的 gameplay loop。纯 tech/expert 包通常不使用此模式，Create 系列也无 escalation ladder 的证据。Non-ATM 包使用时应确认包内确实有可重复的 grind activity。

### MP5 — Dimension + Item Composite

**Applicable when:** a quest gates both exploration AND crafting — the player must reach a new dimension AND bring back something from it. Common for dimension-gated progression (Nether, End, Twilight Forest, etc.).

**Implementation:** Two tasks in one quest: one `dimension` task (enter the dimension) and one `item` task (obtain the dimension-specific material). Both must be completed (AND logic, the default). The dimension task auto-completes on entry; the item task requires the player to actually do something while there.

This composite says "go there AND come back with proof." It's stronger than either task alone: a dimension-only quest could be completed by accidentally falling in; an item-only quest could be completed by trading. The composite ensures the player actually explored.

**Real case (ATM-10, welcome chapter):** The root quest uses a `dimension: "minecraft:overworld"` task (the player enters the Overworld = the quest completes immediately). This is a degenerate case — dimension-only for the "welcome, you arrived" moment. More complex composites appear in chapters like Twilight Forest where dimension + item tasks gate boss progression.

**Quantified across packs:** Prominence II uses 7 task types including dimension and biome extensively — dimension tasks appear in 34 quests in Create: Delight and are a core RPG gating mechanism. ATM-10 uses dimension tasks sparingly (mostly in the welcome and dimension-specific chapters). The frequency is genre-dependent: RPG > adventure > skyblock > kitchen-sink > expert.

---

## Part 2: Dependency Local Topologies

The shapes formed by 3–10 adjacent quests and their `dependencies` wires. These are the local building blocks that compose into the chapter-level layout templates.

### MP6 — Linear Chain (the tutorial spine)

**Applicable when:** teaching a strictly sequential process where each step depends on the previous one completing. Skyblock tutorials, mod progression ladders, and narrative arcs.

**Implementation:** Quest A has no dependencies (the chain root). B `depends_on: [A]`. C `depends_on: [B]`. And so on. Each quest has exactly one dependency (except the root). The chain is laid out horizontally (x-step 0.5–1.0 for ATM-style, 3.5 for narrative-style) along y=0.

The linear chain is the simplest topology but the strongest for forced progression. In `linear` progression mode, each quest is locked until the previous one completes — the player has no choice but to follow the chain. In `flexible` mode, the chain is a suggestion (passive tasks count), but the visual dependency still pulls the player left-to-right.

**Real case (ATM9-Sky, getting_started_2):** Dependency depth **18** — the deepest of any chapter analyzed. The skyblock tutorial is inherently sequential: sieve → hammer → crook → ore processing → first ingot → first tool → first machine → ... Each step requires the previous step's output. The chapter uses `progression_mode: "default"` (locked), so the player cannot skip ahead.

**Quantified:** Linear chains dominate in expert packs (Monifactory: depth 8–15 per chain; ATM6-Expert: forced main line) and skyblock tutorials (ATM9-Sky: depth 18). In kitchen-sinks, linear chains appear within sub-sections of a chapter but are broken by fan-out at tier boundaries. ATM-10's main questline has chains of 4–6 before fanning out.

### MP7 — Fan-Out (the hub-and-spoke)

**Applicable when:** a single prerequisite unlocks multiple independent paths. The player can then pick which path to pursue, or pursue all of them in parallel.

**Implementation:** Hub quest H has no dependencies (or depends on a chain root). Quests A, B, C, D all `depend_on: [H]`. H is visually distinct (larger `size`, distinctive `shape`). A–D are independent of each other (no deps among siblings). H uses `hide_dependency_lines: true` if it has >3 dependents (to avoid line clutter). A–D are arranged in a symmetric fan around H on the y-axis.

> **Scope note:** Heavy use of `hide_dependency_lines` is an ATM-series design preference. In curated packs (3-8% explicit shape/line settings), dependency lines are typically left visible as navigation aids. This is an ATM design preference, not a universal best practice — non-ATM packs should evaluate whether hiding lines improves readability or obscures navigation.

The fan-out signals "you've unlocked this area; now explore in any order." In kitchen-sinks, fan-out is the dominant topology — the hub is a tier-gate quest, the spokes are the mod features at that tier. In expert packs, fan-out appears at tier boundaries where the player can choose which machine line to build first.

**Real case (ATM-10, Ars Nouveau chapter):** The Ars Nouveau chapter has 130 quests arranged in a vertical tiered cascade (Template 2 from design guide). Each tier has a gate quest (high fan-out of 15–30 to the tier's content quests). The gate quest uses `gear` or `hexagon` shape `size: 1.5–2.0`; the content quests are default `circle` or `rsquare`. `hide_dependency_lines` on the gate quest keeps the visual clean.

**Real case (Create: Delight Remake, Mouse_Chef catalog):** The category hub (e.g., "cake" block, `rsquare size: 4.0`) `depends_on` ALL 18 cake-variant cells. This is actually a **fan-in** (see MP8) — the hub is the capstone, not the root. But the cells themselves are independent islands (MP10) with no deps among siblings, creating a flat grid.

**Quantified:** In ATM-10's AE2 chapter (73 quests), the root quest fans out to 4–6 starter quests, each of which fans out to 2–4 sub-quests. Maximum single-hub fan-out observed: 30 (Ars Nouveau tier-gate). Typical kitchen-sink fan-out: 3–8 per hub.

### MP8 — Fan-In / Convergence (the capstone gather)

**Applicable when:** multiple independent paths must all be completed before a synthesis quest unlocks. The endgame capstone, a multi-component crafting quest, or a "prove you've mastered everything" milestone.

**Implementation:** Quests A, B, C, D are independent (or have their own sub-trees). Quest Z `depends_on: [A, B, C, D]` (all must complete). Z is the chapter's largest node (largest `size`, most distinctive `shape`). Z typically has `hide_dependent_lines: true` (hides lines FROM Z to its dependents, not the lines TO Z) and a synthesis reward.

> **Scope note:** As with MP7, heavy use of `hide_dependent_lines` on convergence nodes is an ATM-series design preference, not a universal best practice. Curated packs typically leave dependency lines visible for navigation clarity.

The fan-in is the opposite of fan-out: instead of "one unlocks many," it's "many unlock one." It signals convergence — "bring everything together." The ATM Star's final quest has 10 dependencies (one per component sub-tree root).

**Real case (ATM-10, ATM Star chapter):** The capstone quest (ATM Star craft) has `dependencies: [10 hex IDs]` — one for each component sub-tree. It uses `pentagon shape size: 2.0`, `hide_dependent_lines: true`, and rewards 50 ATM Star Shards + a Patrick Star + 50 XP levels. The 10 dependencies represent 10 independent crafting chains, each sourcing items from different mods.

```
# ATM-10 ATM Star — capstone convergence
{
    dependencies: [
        "71B72958B9F80355" "38BFF6F845EA479E" "149C260C10B34BB0"
        "203C91B992BA8CF9" "427BBEB1F24E9DEE" "14C27D44D3C8EDF5"
        "235273F7C9A9B0D0" "66BAC2B478F9B119" "7A066DD274F970C2"
        "1FC1588A131B6A4A"
    ]
    hide_dependent_lines: true
    shape: "pentagon"
    size: 2.0d
    tasks: [{ item: { count: 1, id: "allthetweaks:atm_star" }, type: "item" }]
    rewards: [
        { count: 50, item: { count: 1, id: "allthetweaks:atm_star_shard" }, type: "item" }
        { item: { count: 1, id: "allthetweaks:patrick_star" }, type: "item" }
        { type: "xp_levels", xp_levels: 50 }
    ]
}
```

**Source:** [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) `config/ftbquests/quests/chapters/achapter_2r_6the_atm_star.snbt`

### MP9 — Diamond (the pick-and-rejoin)

**Applicable when:** the player faces a genuine choice between two paths, and both paths lead to the same next step. "Pick one of these two upgrades; both unlock the next tier."

**Implementation:** Quest A is the decision point. B and C both `depend_on: [A]` and are independent of each other. Quest D `depends_on: [B, C]` — BUT with `dependency_requirement: "one_completed"` (only one of B or C needs completing). This creates a diamond shape: A→{B,C}→D, where the middle is a choice.

In kitchen-sinks, diamonds are rare (the pack wants the player to explore everything, not choose). In expert packs, diamonds appear at branching points where the player picks one machine line or one material path. The `dependency_requirement: "one_completed"` field is what makes this a choice rather than a requirement to do both.

**Real case (Monifactory):** Uses `dependency_requirement: "one_completed"` for voltage-tier branching — the player can pick one machine line to prove mastery before unlocking the next tier. The diamond shape is a fundamental expert-pack building block.

**Quantified:** In Create: Delight Remake, `one_started` appears 63 times and `one_completed` 44 times — the pack uses branching extensively for alternative recipe paths. In Mechanomania, only 1 `one_completed` appears across 395 quests (near-linear). ATM-10 defaults to `"all"` for most deps (the kitchen-sink wants breadth, not choice).

### MP10 — Independent Island (the catalog cell)

**Applicable when:** a quest stands alone with no dependencies — it's part of a catalog or collection where order doesn't matter.

**Implementation:** No `dependencies` field at all. The quest is always visible and always completable. It uses the chapter's default shape and a small `size` (1.0–2.0). In catalog layouts, islands are arranged in a grid; in kitchen-sinks, they're marked `optional: true`.

Independent islands are the building blocks of recipe catalogs and reference collections. Each island is a self-contained unit — the player can do them in any order, skip any of them, or do all of them. The capstone hub (MP8) then optionally depends on all islands to create a "completion" metric.

**Real case (Create: Delight Remake, Mouse_Chef):** 304 quests, of which only 46 have dependencies. The remaining 258 are independent islands — recipe cells arranged in a grid around category hubs. Each cell is a `size: 2.0` default-circle with one `item` task ("obtain this dish") and no dependencies.

**Real case (Arcana, Iron Spells chapter):** 17 root quests — one per magic school (fire, ice, lightning, etc.) starting simultaneously with no dependencies. Each root is an independent island that fans into its own sub-tree. This is the highest root count of any chapter analyzed.

---

## Part 3: Quest-Internal Pacing

How the order of tasks and quests within a chapter guides the player's experience. This is about the *sequence* — what the player does first, second, third — within and across quests.

### MP11 — Teach-Then-Do Sequencing

**Applicable when:** a mod mechanic needs explanation before the player can apply it. The chapter teaches a concept, then tests it.

**Implementation:** Two adjacent quests in a dependency chain. Quest 1 is a **teaching** quest: `checkmark` or `stat` task, long `description` text explaining the mechanic, `subtitle` with the key takeaway, reward is the tool/item needed to practice. Quest 2 `depends_on` Quest 1 and is a **doing** quest: `item` task requiring the player to craft/use what was just taught, minimal description, reward is the next-step material or XP.

This pattern is visible in the Feast_Afood chapter (Create: Delight): tutorial quests (humidity system, soil types, seasonal planting) are followed by practical quests (grow specific crops under specific conditions). The teaching quest uses `rsquare` shape; the doing quest uses default `circle` — the shape difference visually separates "read this" from "do this."

**Real case (ATM-10, Mekanism chapter):** The Mekanism chapter is a Decorated Freeform layout (Template 5) with extensive image assets. The first quests in each sub-section are text-heavy (explaining what a machine does, showing screenshots of the GUI), followed by item-task quests that require the player to actually build and use the machine. The progression within each sub-section follows: introduction (checkmark) → first craft (item) → first use (checkmark/observation) → advanced recipe (item) → automation tip (checkmark).

### MP12 — Tier Escalation Within a Chapter

**Applicable when:** a chapter covers a mod with multiple tiers of the same thing (tools, armor, machines, materials). Each tier is more expensive than the last.

**Implementation:** Within a chapter, quests are ordered by tier from cheapest/simplest to most expensive/complex. The first tier quest has a low-count item task (`count: 1`), simple reward (10 XP). Each subsequent tier increases the count or complexity. The final tier quest has the largest `size`, most distinctive `shape`, and richest reward.

ATM-10's AllTheModium chapter exemplifies this: the diamond-shape quests progress from AllTheModium (Overworld, netherite pick) → Vibranium (Nether, ATM pick) → Unobtainium (End, vibranium pick). Each tier is a column of rsquare/octagon pairs at increasing y-values, and the tier-gate between columns requires the previous tier's tool.

**Real case (ATM-10, AllTheModium chapter):** The tier spine uses `default_quest_shape: "diamond"` (material identity). Within each tier column, quests alternate between `rsquare` (at y=-1) and `octagon` (at y=+1) — the shape alternation signals "tool variant" vs "armor variant" of the same tier. `hexagon` cross-link nodes point back to the root, creating navigation shortcuts. The convergence at the final tier uses `size: 2.0` (vs the standard 1.0) to signal "this is the endgame product."

### MP13 — Explore-Then-Craft (Dimension-Gated Pacing)

**Applicable when:** a crafting recipe requires materials from a specific dimension or biome. The player must first travel, then craft.

**Implementation:** Quest A is a `dimension` or `biome` task (go there). Quest B `depends_on: [A]` and is an `item` task requiring materials found in that dimension. Quest C `depends_on: [B]` and requires crafting the materials into a product. The chain is: travel → gather → craft.

This pacing creates a natural rhythm: the player explores a new area, gathers resources while there, then returns home to craft. The dimension task auto-completes (just enter the dimension), but the item task requires actual effort in that dimension.

**Real case (ATM-10, main questline):** The main questline progresses through dimensions: Overworld → Nether → End → Twilight Forest → other mod dimensions. Each dimension transition has a `dimension` task followed by dimension-specific item tasks. The Warden kill quest in the AllTheModium chapter requires entering the Deep Dark (a dimension-adjacent mechanic) and killing the Warden, which rewards an AllTheModium ingot — replacing a grind with a boss fight.

---

## Part 4: Reward Bridging Patterns

How rewards connect one quest to the next, creating a flow that pulls the player forward rather than leaving them stranded after completion.

### MP14 — Material Bridge (reward IS the next quest's ingredient)

**Applicable when:** the reward of Quest N is a material needed for Quest N+1. This is the strongest forward-pull — the player has the ingredient in their inventory and the next quest immediately lights up.

**Implementation:** Quest N's reward is an item that appears as a task in Quest N+1. The reward count matches (or slightly exceeds) the next quest's requirement. Quest N+1 `depends_on: [N]`, so completing N both gives the player the material AND unlocks the quest that needs it.

This is the most natural bridging pattern and appears across all pack genres. In kitchen-sinks, the material bridge is often a mod's signature intermediate (e.g., Mekanism's osmium ingot → next quest needs osmium ingot). In expert packs, the bridge is tighter (the reward count exactly matches the next recipe's input count, no waste).

**Real case (ATM-10, AE2 chapter):** The root quest rewards 10 XP. The second quest (depends on root) requires obtaining a charger AND inscriber, and rewards 3 iron_ingots + 50 XP. The third quest (depends on second) requires a meteorite compass, and rewards 4 sky_stone_blocks + 100 XP. Each reward is a material or XP boost that facilitates the next step.

```
# ATM-10 AE2 chapter — reward escalation chain
# Quest 1 (root): reward = 10 XP
# Quest 2 (depends on 1): task = charger + inscriber, reward = 3 iron + 50 XP
# Quest 3 (depends on 2): task = meteorite compass, reward = 4 sky_stone + 100 XP
```

**Source:** [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) `config/ftbquests/quests/chapters/applied_energistics_2.snbt`

### MP15 — Tool Reward (reward unlocks the next activity)

**Applicable when:** a new tool, machine, or ability is needed for the next section. The reward is not a consumable material but a durable tool that changes how the player interacts with the world.

**Implementation:** The reward is a tool item (a pickaxe, a wrench, a guide book, a machine block). The next quest's task requires using that tool. The reward is often `count: 1` (one tool is enough) and the quest description mentions what the tool does and why the player will need it.

Tool rewards are common at section boundaries — the "here's your new tool, now go use it" transition. They're especially important in expert packs where a new machine tier unlocks an entire new set of recipes.

**Real case (Create: Delight Remake, Feast_Afoot):** Tutorial quests reward the tool needed for the next practical quest — the hygrometer (humidity measurement), the watering can (crop irrigation), the cooking pot (recipe crafting). Each tool reward immediately precedes a quest that requires using that tool.

**Real case (ATM-10, AllTheModium root):** The root quest rewards the AllTheModium guide book (`patchouli:guide_book`). This is both a tool (reference for all AllTheModium recipes) and a signal ("you're now in the AllTheModium zone; here's your manual").

### MP16 — XP Drip (small XP on every quest)

**Applicable when:** the pack wants a steady sense of progression without item-economy inflation. Every quest gives a small XP reward as a baseline; milestone quests give larger XP or XP-level rewards.

**Implementation:** Every quest in the chapter includes `{ type: "xp", xp: 10 }` as a secondary reward alongside the primary reward. Hub/milestone quests give `{ type: "xp", xp: 50 }` or `{ type: "xp_levels", xp_levels: 5 }`. The XP is not enough to "buy" progression but enough to feel like steady advancement.

ATM-10 uses XP drip extensively: the welcome chapter gives 10 XP per quest, the Mekanism chapter uses 10/50/100 XP tiers, and the ATM Star capstone gives 50 XP levels. The philosophy is explicit (Discussion #3539): generosity is density — many small rewards, not a few big ones.

**Quantified:** ATM-10 has 6,915 total rewards across 4,601 quests = 1.5 rewards per quest. The majority are `item` + `xp` pairs. Create: Delight follows a similar pattern (item×803, xp×195 = ~1,000 rewards for 2,295 quests ≈ 0.43 rewards/quest, but the rich chapters like Mouse_Chef concentrate rewards on hubs). Mechanomania is the counter-example: only 43 total rewards for 395 quests (0.11 rewards/quest — the "sparse" lane).

> **† ATM Signature:** XP Drip 的 generous reward philosophy（每 quest 给 XP + item）是 ATM 系列的设计签名。Expert 包的 reward 系统不以 XP drip 为核心（Monifactory 的 reward 更侧重 machine unlock 和 stage progression）。Create 系列明确不使用 XP drip（Create: Delight 0.43 rewards/quest, Mechanomania 0.11 rewards/quest）。Scope 已从 `kitchen-sink, expert` 修正为 `kitchen-sink`，再进一步限定为 `kitchen-sink (ATM-style generous)`——XP drip 不是所有 kitchen-sink 的通用模式，而是 ATM-style generous reward philosophy 的特定做法（排除 sparse reward 或 random-dominant 经济的 kitchen-sink 包）。

### MP17 — Hub Concentration (sparse cells, rich hubs)

**Applicable when:** designing a catalog or grid layout where most quests are simple items but a few hubs represent completion milestones. The hubs carry the rewards; the cells carry only the satisfaction of completion.

**Implementation:** Cell quests (the majority) have no rewards or a minimal single-item reward. Hub quests (the minority) have rich rewards: multiple items, XP, random loot, or choice rewards. The hub `depends_on` ALL its cells, so completing the hub means completing the entire category.

This pattern prevents reward inflation in large catalogs. If every cell gave a reward, a 300-quest catalog would give 300 rewards — overwhelming the player. Concentrating rewards on hubs (12 hubs for 300 cells) gives 12 meaningful reward moments instead.

**Real case (Create: Delight Remake, Mouse_Chef):** 304 cells have only item×29 + xp×52 (sparse). The 12 category hubs have coin rewards (netherite_coin) and checkmark tasks. The ratio is roughly: 1 reward per 4 cells, with the hubs carrying the most valuable rewards.

> **Scope note (Cycle 7):** `kitchen-sink` 已从 pack_types 中删除。ATM-10（kitchen-sink）不使用 hub concentration 模式——其 reward 分布更均匀（XP drip philosophy, 1.5 rewards/quest），不存在「sparse cells, rich hubs」的明显分化。Hub concentration 的核心证据仅来自 Create: Delight 的 Mouse_Chef catalog chapter。pack_types 从 `create, kitchen-sink` 修正为 `create`。

### MP18 — Choice Reward (branch-point fork)

**Applicable when:** the player reaches a branching point where they must pick one of several paths. The reward IS the choice — pick one of several items, each leading to a different sub-tree.

**Implementation:** A quest with a `choice` reward (or multiple `item` rewards with `autoclaim` disabled). The quest description explains the options and what each path leads to. After the choice, the selected item becomes the task for the chosen path's first quest. The unchosen paths remain locked (their first quests depend on having the specific item).

This is rare in kitchen-sinks (the philosophy is "do everything") but appears in expert packs and RPG packs where meaningful choices are part of the genre.

**Real case (Create: Delight Remake):** `choice` rewards appear 13 times across 2,295 quests — used at key branching points where the player picks one of several machine upgrade paths. Mechanomania uses `choice` rewards 3 times (its only non-item reward type).

---

## Part 5: Stage Marking Patterns

How pack authors signal "you are now in a new stage" — through chapter structure, dependency chains, visual cues, or item tiers.

### MP19 — Chapter-as-Stage (the dominant model)

**Applicable when:** the pack has distinct phases (early-game, mid-game, late-game, endgame) or distinct topics (tech, magic, exploration, combat). Each phase/topic is a separate chapter.

**Implementation:** Chapter ordering via `order_index` defines the suggested sequence. Chapter `icon` represents the stage's theme (a mod's signature item, a dimension's icon, a tier's material). Chapter `title` names the stage ("Chapter 3: The Nether", "Mekanism: Advanced Tier"). All quests within a chapter are at the same stage; cross-stage progression is cross-chapter.

This is the dominant model across all packs. The variation is in how strict the chapter ordering is: kitchen-sinks use `flexible` progression (chapters are suggestions), expert packs use `linear` (chapters are locked until previous chapter completes), and RPG packs use dependency-gated reveals (chapters appear as the player explores).

**Quantified:** ATM-10 has 64 chapters in 10 groups. Create: Delight has 41 chapters in 6 groups. Mechanomania has 18 chapters in 3 groups. Monifactory has 5 chapters (but with invisible routing chapters). The chapter count correlates with pack scope, not complexity — a 5-chapter expert pack can have more design depth than a 64-chapter kitchen-sink.

### MP20 — Shape-as-Tier Signal

**Applicable when:** within a chapter, different quest shapes represent different tiers, categories, or difficulty levels. The shape vocabulary carries semantic meaning.

**Implementation:** Assign one shape per tier/category within the chapter. Set `default_quest_shape` at the chapter level to the dominant shape. Override individual quests to signal tier transitions. The mapping should be consistent across the pack: if `diamond` = "material/tier" in one chapter, use it the same way in all chapters.

ATM-10 has the richest shape vocabulary of any pack analyzed: Mekanism=`hexagon` (energy/hive), Create=`gear` (machinery), AllTheModium=`diamond` (material/tier), basic_armor=`rsquare` (armor/special), welcome=`pentagon` (milestone). ~47% of ATM-10 quests set an explicit shape vs ~3–8% in curated packs — kitchen-sinks are shape-rich by design.

> **† ATM Signature:** Shape-as-Tier 是 ATM 系列的视觉设计签名。~47% explicit shape usage 是 ATM 独有的；curated packs 仅 3-8%。对于不使用丰富 shape 词汇的包，此模式不适用。Scope 已从 `kitchen-sink, expert` 修正为 `kitchen-sink (ATM-style)`，因为 expert 包（如 Monifactory）的 shape usage 未被验证。

**Real case (ATM-10, AllTheModium):** Within the diamond-default chapter, tier-gate quests use `gear` or `hexagon` shape `size: 1.5–2.0`. Tool variants use `rsquare` at y=-1; armor variants use `octagon` at y=+1. Cross-link navigation nodes use `hexagon`. The shape tells the player what KIND of quest this is without reading the title.

### MP21 — Dimension-as-Stage-Gate

**Applicable when:** progression requires traveling to new dimensions. Each dimension represents a new stage, and the dimension entry itself is the gate.

**Implementation:** A `dimension` task at the beginning of a dimension's section. The task auto-completes when the player enters the dimension. All subsequent quests in that section depend on the dimension task. The dimension task has no dependencies itself (or depends on a prerequisite from the previous dimension — e.g., "craft a Nether portal" quest).

This creates a natural stage boundary: the player can't see or access the Nether quests until they've actually entered the Nether. It's a soft gate (the player can enter the Nether at any time) combined with quest-gating (the quests only unlock when they do).

**Real case (ATM-10, welcome chapter):** The root quest is a `dimension: "minecraft:overworld"` task — the very first thing the player does is "set foot in the overworld." This is the simplest possible stage gate and the most universal. More complex dimension gates appear in the Twilight Forest, Undergarden, and Bumblezone chapters.

> **† ATM Signature:** Dimension-as-Stage-Gate 的核心证据来自 ATM 系列（ATM-10 welcome chapter + 各 dimension-specific chapters）。Concept（dimension entry = progression gate）是通用的，但 ATM 的具体实现（每个 dimension 对应一个 welcome quest + dimension-locked content chapters）是其设计签名。尚无独立的 non-ATM kitchen-sink 包验证此模式。

### MP22 — Material-Tier Spine (cross-chapter progression)

**Applicable when:** a material hierarchy spans multiple dimensions or chapters, and the tier progression is the pack's backbone.

**Implementation:** A chain of quests across chapters, each requiring the previous tier's output. The chain typically follows: base material (Chapter A) → refined material (Chapter B) → alloy material (Chapter C) → endgame product (capstone chapter). Each tier quest's reward includes the tool needed to harvest the next tier's ore.

The material-tier spine is ATM's signature endgame pattern: AllTheModium (Overworld/Deep Dark, netherite pick) → Vibranium (Nether, ATM pick) → Unobtainium (End, vibranium pick) → ATM Star (capstone). Three dimensions, three tiers, one pick-per-tier gate.

> **† ATM Signature:** Material-Tier Spine（三金属跨维度 endgame）是 ATM 的标志性 endgame 设计。AllTheModium → Vibranium → Unobtainium 的三金属 spine 在非 ATM 的 kitchen-sink 包中未被观察到。Non-ATM 包可能有完全不同的 endgame 材料体系（或根本没有 material-tier spine）。

**Real case (ATM-10):** The AllTheModium tier spine is implemented as a dedicated chapter (`allthemodium.snbt`, `default_quest_shape: "diamond"`, 54 quests). The chapter uses Template 3 (Parallel Material Columns) with 3–4 columns (tools, armor, weapons, utilities). Each column progresses through AllTheModium → Vibranium → Unobtainium. `hexagon` cross-link nodes connect columns at tier boundaries. `hide_dependency_lines` on 31/54 quests — the heaviest usage of any analyzed chapter.

### MP23 — Invisible Infrastructure (expert-pack stage routing)

**Applicable when:** an expert pack needs complex stage-gating logic (gamestages, cross-mod state, internal triggers) that should be invisible to the player.

**Implementation:** Create `always_invisible: true` chapters that contain the routing logic. These chapters use `gamestage` tasks, `command` rewards, and cross-chapter dependency wires to manage progression state. The visible chapters are clean and focused on content; the invisible chapters run the machinery.

This pattern separates the player-facing UX from the pack-author-facing logic. The player never sees the invisible chapters; they only experience the clean progression through visible content. It's the FTB Quests equivalent of a backend service.

**Real case (Monifactory):** Uses `always_invisible` chapters as backend infrastructure for gamestage progression, internal triggers, and cross-mod state management. ~11% of quests are in invisible chapters. The visible book is a clean tech-tree UI; the invisible book runs the voltage-tier gating system.

**Source:** Design guide §pack-type-patterns, Monifactory audit data.

---

## Part 6: Anti-Pattern Detection Signals

These are micro-level indicators that a quest configuration likely has one of the "three hard problems" (item tier mismatch, sequence inversion, or reward disconnection). Use them as validation checks.

### MP24 — Tier-Reachability Check (prevents item-tier mismatch)

**Applicable when:** validating that every item task's required item is obtainable at the quest's stage in the progression.

**Signal:** A quest at dependency depth N requires an item whose crafting chain requires materials from dependency depth > N. This is the "item cross-tier" problem — the quest asks for something the player can't have yet.

**Detection heuristic:** For each item task, trace the item's crafting recipe (from JEI/EMI or the mod's recipe data). If any ingredient's source quest is at a greater dependency depth than the current quest, flag it. In practice, this requires cross-referencing the quest dependency graph with the mod recipe graph.

**Real-world mitigation:** ATM-10 avoids this by using `flexible` progression mode — the player can work on any quest in any order, so "can't have it yet" doesn't apply. Expert packs like Monifactory avoid it by carefully designing the dependency chain to match the recipe chain (every prerequisite quest is wired before the quest that needs its output).

### MP25 — Dependency-Order Check (prevents sequence inversion)

**Applicable when:** validating that tutorial/teaching quests come before application/doing quests.

**Signal:** An item task quest that requires a complex crafted item appears at a lower dependency depth than the checkmark/tutorial quest that explains how to craft it. The player encounters the "do this" quest before the "here's how" quest.

**Detection heuristic:** For each chapter, identify teaching quests (checkmark/stat/observation tasks with long descriptions) and doing quests (item tasks). If any doing quest has a lower dependency depth than its corresponding teaching quest, flag it. The correspondence is typically by topic (same mod, same item category).

### MP26 — Reward-Continuity Check (prevents reward disconnection)

**Applicable when:** validating that rewards guide the player toward the next quest rather than leaving them stranded.

**Signal:** A quest's reward is neither a material needed by any of its dependent quests (MP14 material bridge), nor a tool needed for the next section (MP15 tool reward), nor XP (MP16 baseline). The reward is a "dead end" — it doesn't connect to anything the player will do next.

**Detection heuristic:** For each quest, check if any of its rewards appear as task items in any of its dependent quests. If not, and the reward is not XP/loot/choice, flag it as a potential disconnection. Cosmetic rewards (decorative items, trophies) are acceptable exceptions — they're rewards for completion, not progression guides.

---

## Part 7: Extended Type Patterns (Supplementary Task/Reward Types)

These patterns address task and reward types not covered by MP1–MP18. They focus on the highest-risk types — the ones where design mistakes are most common and most damaging. Not all 15 task types or 13 reward types need dedicated patterns; many are straightforward variants of the item-task model. The patterns below cover types that have fundamentally different design considerations from item tasks.

### MP27 — Fluid Task Gate (tank-and-pipe progression)

**Applicable when:** a quest requires the player to collect a specific volume of fluid. Common in tech packs where Mekanism, Thermal Expansion, Immersive Engineering, or Create use fluid processing as a core mechanic.

**Implementation:** A single `fluid` task with `fluid: "<modid>:<fluid_name>"` and `amount: <mB>`. The task icon shows the fluid; the description explains how to produce it (which machine, which input fluid, what temperature). The reward is typically the next machine in the processing chain, or a bucket/tank for the player to keep.

Fluid tasks differ from item tasks in three important ways: (1) fluids require infrastructure (tanks, pipes, pumps) — the quest should assume the player has this infrastructure or provide it as a prior reward; (2) fluid amounts are continuous (1000mB = 1 bucket), so the `amount` value should align with the machine's output rate (don't ask for 500mB when the machine outputs 1000mB per operation); (3) some fluids are dangerous to handle (lava, toxic chemicals) — the description should warn about this.

**Design considerations:** The fluid amount should be a multiple of the producing machine's per-operation output. If a Mekanism chemical infuser produces 1000mB of enriched redstone per operation, the task should ask for 1000mB (1 operation), 2000mB (2 operations), or 5000mB (5 operations) — not 1500mB (1.5 operations, which wastes half a bucket). For early-game fluid tasks, keep amounts low (1000–4000mB); for late-game, scale to 16000–64000mB.

**pack_types:** kitchen-sink, expert, create
**Phase:** Step 4 (node generation)

---

### MP28 — Energy Threshold Gate (power infrastructure pacing)

**Applicable when:** a quest requires the player to store a specific amount of energy (FE/RF/EU) in a block or item. Used to gate progression behind power infrastructure — the player must build generators and energy storage before advancing.

**Implementation:** A `forge_energy` task with `value: <FE>` on a specific energy container block. The task auto-completes when the block reaches the specified energy level. The description should explain how much power the player needs and suggest appropriate generators. The reward is typically a higher-tier machine or an energy-related upgrade.

Energy tasks are unique because they test *infrastructure*, not *items*. The player doesn't craft something and submit it — they build a power system and let it charge. This means the quest should come AFTER the player has access to generators (check dependency chain), and the energy threshold should be achievable with the generators available at this stage. A 100,000 FE threshold is unreasonable if the player only has hand-crank generators producing 50 FE/tick; it's reasonable if they have a gas-burning generator producing 500 FE/tick.

**Design considerations:** Calibrate the energy threshold against the best available generator at this progression stage. Target 2–5 minutes of active generation for early-game thresholds, 5–15 minutes for mid-game, and 15–30 minutes for late-game. If the threshold requires more than 30 minutes of generation, consider whether this is an intentional grind gate or an oversight. Always mention the recommended generator in the description.

**pack_types:** kitchen-sink, expert, create
**Phase:** Step 4 (node generation)

---

### MP29 — Command Reward (server-side invisible logic)

**Applicable when:** a quest needs to trigger a server-side action that isn't achievable through standard reward types — granting a gamestage, teleporting the player, applying a potion effect, running a KubeJS script, modifying the world state, or (legacy MC ≤1.16.5) delivering loot via vanilla loot tables.

**Implementation:** A `command` reward with `command: "/<command>"` and optional `player: "{p}"` (the completing player). The command runs server-side when the quest is claimed. Common commands: `/gamestage add {p} <stage_name>` (unlock a gamestage), `/effect give {p} <effect> <duration> <amplifier>` (temporary buff), `/tp {p} <x> <y> <z>` (teleportation), `/give {p} <item> <count>` (item grant when item rewards aren't flexible enough), `/execute at @p run loot spawn ~ ~1 ~ loot <namespace>:<table>` (legacy loot delivery, MC ≤1.16.5), `/packmode <mode>` (GreedyCraft pack-mode switching).

Command rewards are the most powerful and most dangerous reward type. They execute with server-level permissions, meaning a poorly written command can crash the server, give the player operator-level items, or corrupt world state. The `{p}` placeholder is replaced with the completing player's name — always use `{p}` rather than hardcoding a player name.

**Safety rules:** (1) Never use command rewards that grant operator permissions (`/op`, `/gamemode creative`). (2) Test every command in a single-player world before including it in a quest. (3) Prefer standard reward types when possible — use `item` rewards instead of `/give`, use `xp` rewards instead of `/xp`. Command rewards should be reserved for actions that standard types can't express. (4) When using `/gamestage add`, verify the stage name against the pack's gamestage configuration — a typo creates a silent failure (the command runs but the stage doesn't exist).

**Enigmatica command reward lineage (Cycle 6 Phase 3):** E6 (MC 1.16.5): 455 command rewards ALL using `/execute at @p run loot spawn ~ ~1 ~ loot enigmatica:chests/quest_*` — vanilla loot table delivery as workaround for missing native FTB loot tables. E9E (MC 1.19.2): 56 command rewards shifted to `/gamestage add {p}` — progression routing. E10 (MC 1.21): 0 command rewards, 28 native reward tables — the workaround is no longer needed. **On FTB Quests 26.x+, always prefer `type: "loot"` or `type: "random"` for loot delivery.**

**pack_types:** expert, story, kitchen-sink (legacy MC ≤1.16.5)
**Phase:** Step 4 (node generation)
**Source confidence:** Multi-source (Monifactory + E9E Cycle 3; E6 + E10 Cycle 6)

---

### MP30 — Gamestage Bridge (invisible progression state)

**Applicable when:** an expert pack uses Game Stages to gate content invisibly — the player can't see the gating mechanism, but content unlocks as they progress through the quest book. This pattern connects the visible quest book to the invisible stage system.

**Implementation:** A pair of mechanisms: (1) a `gamestage` reward (or `command` reward with `/gamestage add`) on a visible quest that grants a new stage when completed; (2) a `gamestage` task (or KubeJS event listener) on a visible quest that requires a specific stage to be completable. The invisible infrastructure chapter (MP23) manages the stage routing; the visible quests simply check "has the player reached this stage?"

The gamestage bridge creates a progression system where the player sees clean, focused visible chapters but the actual gating logic runs through stages. When the player completes "Build your first MV machine" (visible quest, Mekanism chapter), the quest rewards the `mv_tier` gamestage. When the player opens the next chapter, the chapter's root quest has a `gamestage: mv_tier` task — it auto-completes because the player already has the stage, and the chapter content unlocks.

**Design considerations:** (1) Stage names should be descriptive and consistent (e.g., `lv_tier`, `mv_tier`, `hv_tier`, not `stage_1`, `stage_2`, `stage_3`). (2) Every stage grant must have a corresponding stage check — granting a stage that nothing checks is dead code. (3) Every stage check must have a corresponding stage grant — checking a stage that nothing grants creates an unfinishable quest. (4) Document all stages in a central reference (the invisible infrastructure chapter's description, or a separate stages.md file).

**pack_types:** expert
**Phase:** Step 2 (outline) + Step 4 (node generation)

---

## Part 8: Cycle 2 Patterns (Extended Task Types & Modifiers)

Patterns discovered in Cycle 2 research across 6 additional packs (ATM-9, ATM-10-Sky, ATM-8, All-the-Mons, Create: Astral, Arcana raw data). These complement MP1–MP30 by covering task types and quest modifiers not prevalent in Cycle 1's dataset.

### MP31 — Structure Discovery Gate (find-a-structure progression)

**Applicable when:** a quest requires the player to locate a specific generated structure in the world. Common in skyblock packs (where structures are rare and gated), kitchen-sink packs (as exploration gates), and RPG packs (as dungeon entry points).

**Implementation:** A `structure` task with `structure: "<namespace>:<structure_name>"`. The task auto-completes when the player enters the structure's bounding box. The description should explain what the structure looks like, what dimension it generates in, and what tools help locate it (e.g., Nature's Compass, Eye of Ender). The reward is typically a key item from the structure or the material needed to exploit it.

Structure tasks differ from dimension tasks (MP5, MP21) in that dimensions are broad (enter the Nether = auto-complete) while structures are specific (find a Fortress within the Nether). This specificity makes structure tasks stronger progression gates — the player must actively search, not just travel.

**Real case (ATM-10-Sky, chapter_2_the_cool_parts):** Uses `structure: "minecraft:fortress"` as a progression gate, requiring the player to locate a Nether Fortress before accessing Blaze Rod quests. The structure task auto-completes on entry, and the reward includes blaze rods and XP.

**Real case (All-the-Mons, catch_em_all):** 23 quests use `structure` tasks to locate prehistoric structures (fossil sites, ancient cities), each requiring the player to physically find and enter the structure before the quest completes.

**Design considerations:** (1) Structure availability depends on world generation — if the pack uses custom terrain generation (skyblock, void world), verify that the target structure actually generates. (2) Provide a fallback: if the structure is rare, include a description note about alternative ways to find it (Nature's Compass, trader, etc.). (3) Don't chain multiple structure tasks in a single quest — each structure search is a separate expedition.

**pack_types:** skyblock, kitchen-sink, story
**Phase:** Step 4 (node generation)

### MP32 — min_tasks Modifier (partial completion threshold)

**Applicable when:** a quest has many tasks but the player only needs to complete a subset to pass. This is a deliberate design choice for "show breadth, require depth" scenarios — the quest lists 10 possible items, but only requires the player to obtain 3 of them.

**Implementation:** Set `min_tasks: <N>` on a quest where the `tasks` array contains more than N items. The quest completes when any N tasks are done, not all of them. This creates a "pick your path" feel within a single quest — the player can choose which 3 of 10 items to obtain based on what's easiest for their current situation.

This is related to `dependency_requirement: "one_completed"` (MP9 diamond) but operates at the task level rather than the dependency level. `min_tasks` is a quest-level modifier that says "do N of these M tasks," while `one_completed` is a dependency-level modifier that says "complete 1 of these N prerequisite quests."

**Real case (Create: Astral, chapter_3):** Multiple quests use `min_tasks: 1` with 2 tasks — the player needs to complete either task to pass. This is used for alternative recipe paths: "craft this item via method A OR method B." The chapter also uses `min_deps: 1` similarly for alternative prerequisites.

**Design considerations:** (1) Keep the gap between `min_tasks` and total tasks small (1–3) — if a quest has 10 tasks and only requires 2, the other 8 feel like padding. (2) Use `min_tasks` when the tasks are genuinely equivalent alternatives (two recipes for the same item, two ways to reach the same goal), not when they're a checklist with a lowered bar. (3) Always make `min_tasks` visible in the quest description — the player needs to know "you only need 3 of these 5" to make informed choices.

**pack_types:** create
**Phase:** Step 4 (node generation)

> **与 MP9 的功能重叠：** MP32 在功能上与 MP9 (Diamond / pick-and-rejoin) 重叠。文档自身已承认这一点："This is related to `dependency_requirement: 'one_completed'` (MP9 diamond) but operates at the task level rather than the dependency level." `min_tasks` 是 quest-level 的"选 N 完成"机制，而 `one_completed` 是 dependency-level 的"选 1 完成"机制。当 MP9 已经满足设计需求时，不需要额外使用 MP32。此外，`kitchen-sink` scope 标注缺乏数据支撑——15 个包中无 kitchen-sink 包使用 `min_tasks` 的证据。MP32 可视为 MP9 的 task-level 变体，而非一个独立的设计模式。

---

## Part 9: Cycle 3 Patterns (Advancement Gate & Loot Table Reward)

Patterns identified in Cycle 3 research across Enigmatica 10 (expert, MC 1.21.1) and Craftoria (kitchen-sink, MC 1.21.1). These cover task and reward types that are FTB Quests native features but were not prevalent enough in Cycles 1–2's datasets to warrant dedicated patterns. Cycle 3's deeper analysis of issue-tracker data and config-level reward structures revealed their distinct design roles.

### MP33 — Advancement Gate (vanilla advancement as progression checkpoint)

**Applicable when:** a quest needs to gate progression behind a vanilla advancement milestone — entering a dimension, killing a boss, obtaining a rare item, or completing any achievement the vanilla advancement system tracks. This is distinct from a custom task (AP14): the `advancement` task type is natively supported by FTB Quests and requires no KubeJS handler.

**Implementation:** An `advancement` task with `advancement: "<namespace>:<advancement_path>"` that auto-completes when the player earns the specified vanilla advancement. The quest acts as a silent checkpoint — the player earns the advancement through normal gameplay, and the quest detects it without requiring item submission or manual click-through. The reward is typically the tool, material, or gamestage needed for the next section.

Advancement tasks differ from item tasks (MP1) in a crucial way: they verify that the player *achieved* something, not that they *submitted* something. An item task consumes the item; an advancement task checks the player's advancement record. This means the player keeps whatever items they earned while achieving the advancement — the quest doesn't tax them. It also means the quest can't be cheesed by trading or loot drops: the advancement must be earned through the intended path.

**Real case (Enigmatica 10):** Uses `advancement` tasks across at least 3 quests in its visible chapter structure. The advancement tasks serve as dimension-gate and boss-kill checkpoints — the player enters the Nether (earns the `minecraft:nether/root` advancement), and the quest auto-completes, unlocking the Nether-dependent content. This pattern bridges the vanilla advancement system with the quest book's dependency graph without requiring the player to submit proof.

**Design considerations:** (1) Verify the advancement ID exists in the pack's advancement data — custom mod advancements may use non-standard namespaces. (2) Advancement tasks auto-complete, which means the player may not notice the quest completing if they earn the advancement during normal gameplay. Pair with a visible reward (item drop, XP burst) so the player gets feedback. (3) For gamestage-gated packs, advancement tasks can serve as the trigger that grants a gamestage — the advancement completes, the reward is a `command` or `gamestage` reward that opens the next tier (MP29 + MP30). This creates a clean three-step chain: achieve advancement → auto-complete quest → grant stage. (4) Unlike `custom` tasks (AP14), advancement tasks are safe for AI generation because the type is natively supported and the advancement ID can be verified against the pack's advancement data.

**pack_types:** expert (verified)
**Phase:** Step 4 (node generation)

> **Scope note (Cycle 7):** `all` 已从 pack_types 修正为 `expert (verified)`。虽然 `advancement` task type 是 FTB Quests 原生功能，但「使用 advancement task 作为进度检查点」这一设计决策仅在 Enigmatica 10 中观察到（3 cases）。ATM-10（4,601 quests）、Create: Delight（2,295 quests）、Monifactory（248 quests）的审计数据中均未出现 advancement task 的系统性使用。置信度从 Medium 降为 Low。

---

### MP34 — Loot Table Reward (randomized reward via reward tables)

**Applicable when:** a quest's reward should be randomized — a loot chest, a boss drop, a "pick one of many possible items" moment. Reward tables (`reward_tables[]` in the quest file) let the author define weighted random pools with multiple tiers, avoiding the deterministic reward pattern of standard `item` rewards.

**Implementation:** Define a `reward_tables[]` entry in the chapter or book data with one or more pools, each containing weighted item entries. The quest's reward uses `type: "random"` (or `type: "loot"`) with a `table_id` referencing the table. When the player claims the reward, FTB Quests rolls the table and grants one of the weighted outcomes. Multiple tiers can be expressed as separate pools with different rarity weights.

Loot table rewards differ from standard item rewards (MP14, MP15) in that the outcome is not predetermined. This creates excitement and replayability — the player doesn't know exactly what they'll get. But it also introduces balance risk: a player might roll a rare high-tier item early, or roll a low-tier item repeatedly. The table's weights should be calibrated so that even the worst roll is useful at the quest's progression stage.

**Real case (Craftoria):** Uses `reward_tables[]` across at least 2 quest chains with multiple loot quality tiers. The tables define pools with common (iron, copper), uncommon (gold, diamond), and rare (netherite, mod-specific items) entries, weighted so that common drops are frequent but rare drops are possible. This multi-tier approach gives every reward claim a moment of excitement ("what did I get?") while keeping the expected value within the pack's reward economy.

**Design considerations:** (1) Every tier in the loot table should be useful at the quest's stage — don't include endgame items in a mid-game table unless the pack's economy is designed for early windfalls. (2) Loot table rewards avoid AP8 (Reward Inflation) when calibrated correctly: the expected value per claim is bounded by the table's weights, so the pack can't accidentally over-reward by giving too many deterministic items. (3) Loot tables complement MP14–MP18 (reward bridging): deterministic bridges (material, tool) ensure the player always has the next step's ingredient; loot tables add variety and excitement on top of that baseline. A quest can have both a deterministic item reward (the bridge) and a random table reward (the bonus). (4) The `table_id` is a decimal **long** (not hex) — in the spec, use `table: "<name>"` and let the generator resolve it. (5) Test the table's worst-case and best-case outcomes: if the worst roll leaves the player unable to progress, add a guaranteed baseline reward alongside the table roll.

**pack_types:** all
**Phase:** Step 4 (node generation)

> **与 MP14–MP18 的互补关系：** MP34 提供的随机性是 reward bridging 的补充而非替代。MP14 (Material Bridge) 和 MP15 (Tool Reward) 是确定性桥接——奖励就是下一步需要的东西。MP34 (Loot Table Reward) 是随机性增值——在确定性桥接之上增加变化和惊喜。一个好的设计通常是：确定性奖励保底（MP14/MP15），随机奖励加码（MP34）。两者共存于同一 quest 的 reward 数组中。

---

### MP35 — Dual-Task Automation Verification

**Applicable when:** the pack requires players to build actual automation (e.g. Create contraptions) rather than hand-crafting items. Each quest uses two tasks: an item task with `consume_items: false` (prove you can make it) AND a checkmark task labeled "automated" (confirm you built a machine to produce it).

**Implementation:** Quest has two tasks: (1) `type: "item"` with `consume_items: false` — the item is displayed but not consumed, serving as a "prove it exists" check; (2) `type: "checkmark"` with title like "Automated" — the player clicks to confirm they built automation. The combination forces the player to both produce the item AND acknowledge they did so through automation, not hand-crafting.

This pattern is specific to Create-focused expert packs where automation is the core gameplay loop. The `consume_items: false` field is critical — it means the item stays in the player's inventory, allowing them to use it for further processing. The checkmark serves as an honor-system verification that the player built a Create contraption.

**Real case (Cabricality, stage_1 and stage_3):** Nearly every quest uses this dual-task structure. stage_1: 27 item tasks + 18 checkmark tasks with `consume_items: false` heavy (20 instances). stage_3: 54 item tasks + 26 checkmark tasks with 44 `consume_items: false`. stage_4: 33 item tasks + 25 checkmark tasks with 29 `consume_items: false`. The checkmark title uses i18n key `{contraption.cabricality.automated}`.

**Design considerations:** (1) This pattern only works in packs where automation is the central mechanic — using it in a kitchen-sink would be unnecessarily restrictive. (2) The honor system relies on player integrity; determined players can click the checkmark without building automation. (3) The `consume_items: false` flag is essential — consuming items would defeat the purpose by forcing the player to re-craft for each quest. (4) Pair with descriptive text explaining WHY automation is expected.

**pack_types:** create (expert), expert
**Phase:** Step 4 (node generation)
**Source confidence:** single-source (Cabricality only — no evidence in non-Create expert packs)

> **Scope note (Cycle 7):** pack_types 从 `create` 进一步限定为 `create (expert), expert`。MP35 的核心证据仅来自 Cabricality（Create-centric expert pack），而 Create: Delight（2,295 quests）、Mechanomania（395 quests）、Create: Astral（~650 quests）均不使用此模式。此模式本质上是 Cabricality 的特定设计理念（荣誉制度确认自动化），不是 Create 包的通用做法。验证置信度: 低。

---

### MP36 — Currency-as-Reward (universal exchange medium)

**Applicable when:** the pack has an in-game currency or trading system, and quest rewards should bridge to ANY purchasable item rather than a specific next-quest ingredient. The reward is a currency item (coins, credits) that the player spends at shops, trade stations, or trading systems.

**Implementation:** Standard `type: "item"` reward with a currency item ID (e.g. `gtocore:copper_coin`, `lightmanscurrency:coin_iron`, `lightmanscurrency:coin_gold`). The currency item is not consumed by any quest task — it's accumulated and spent at the player's discretion through the pack's economy system.

Distinct from MP14 (Material Bridge): currency doesn't bridge to a specific recipe, it bridges to a shop. Distinct from MP16 (XP Drip): currency is an item, not XP, and has purchasing power tied to the pack's trade system. Similar to MP16 in concept — a universal baseline reward — but implemented through item-type rewards.

**Real case (GregTech-Odyssey):** Uses `gtocore:copper_coin` as early-game currency rewards. Players accumulate coins to spend at the shop chapter's trading system. The shop chapter has no dependencies and serves as a currency sink.

**Real case (No-Flesh-Within-Chest):** Uses `lightmanscurrency:coin_iron` and `coin_gold` as rewards throughout the main chapters. 42 lightmanscurrency references in the boss chapter alone. Combined with `wares:delivery_agreement` trade contracts, creating a multi-layer economy.

**Design considerations:** (1) Currency rewards need a corresponding currency sink (shop, trade station) to have value. Without a sink, currency accumulates uselessly. (2) Calibrate currency amounts against shop prices — inflation devalues the reward. (3) Currency is genre-appropriate for packs with trading systems (expert, RPG, hardcore); avoid in pure kitchen-sinks without shops. (4) Currency rewards can coexist with MP14 material bridges on the same quest.

**pack_types:** expert, hardcore, rpg
**Phase:** Step 4 (node generation)
**Source confidence:** multi-source (2 packs: GregTech-Odyssey, NFwC)

---

### MP37 — Progress Catalog Chapter (visual milestone tracker)

**Applicable when:** the pack has many voltage tiers, tech stages, or milestone items, and the player needs a at-a-glance view of their overall progress. A dedicated chapter with no dependencies, no rewards, and all quests displayed as a visual catalog of every milestone item.

**Implementation:** A chapter where every quest has: no `dependencies`, no `rewards`, `optional: true` **(mandatory — without this, catalog quests count toward chapter completion % and trigger PP4 Completionist's Dilemma)**, and a single `item` task for a milestone item (e.g. every circuit across all voltage tiers). The chapter is purely a visual tracker — the player can see which items they've produced and which remain. Quest titles label the tier/stage. The chapter icon is distinct (e.g. a progress-related item).

**Mandatory fields checklist:**
- `optional: true` — excludes quests from chapter completion percentage (PP4 prevention)
- `dependencies: []` or omitted — catalog quests are always available
- `rewards: []` or omitted — catalog is tracking only, no progression reward

**Real case (GregTech-Odyssey, progress chapter):** A dedicated chapter listing all circuit items across all voltage tiers. No dependencies, no rewards. Serves as the player's visual progress map — "I've made LV circuits but not MV yet." Combined with the pack's 14 voltage-tier chapters, the progress chapter gives a bird's-eye view of the entire tech tree.

**Design considerations:** (1) Progress catalog chapters are complementary to, not a replacement for, the main progression chapters. (2) All quests should be completable at any time (no gating) — the catalog reflects what the player HAS done, not what they CAN do. (3) Consider using a distinctive shape or color to differentiate catalog quests from progression quests. (4) Works best in expert packs with 10+ tiers/stages; overkill for kitchen-sinks with 3-4 stages.

**pack_types:** expert
**Phase:** Step 2 (chapter design)
**Source confidence:** single-source (GregTech-Odyssey only)

---

### Case Study — Profession Chapter (TWR-specific, decomposable as MP7+MP10+MP18)

> **Status:** Case study, not a generalizable micro-pattern. Observed only in TheWinterRescue. The design can be decomposed as MP7 (Fan-Out from tier gate to profession branches) + MP10 (Independent Island per profession chapter) + MP18 (Choice Reward at role selection). Use those patterns directly rather than referencing this case study.

**Applicable when:** the pack has multiple playstyle paths (combat, farming, mining, research) and the author wants to give each role dedicated quest content. Each profession gets its own chapter with thematically appropriate tasks and rewards.

**Implementation:** Multiple chapters, each named after a profession or role (e.g. "A Day of Hunter", "A Day of Farmer", "A Day of Miner"). Each chapter contains quests themed around that profession's activities. Profession chapters are typically optional side content, complementing the main tier-based progression. They may use distinct shapes, icons, or reward types to differentiate from main chapters.

**Real case (TheWinterRescue):** 9 profession chapters: hunter, farmer, miner, researcher, fuel_engineer, generator_engineer, siberian_chef, tundra_traveller, craftsman. Each chapter provides thematic role-based content alongside the main tier chapters (t0-t3). Combined with the pack's 21-55% optional rate, profession chapters give players extensive non-linear exploration within tiers.

**Design considerations:** (1) Profession chapters should be genuinely optional — never gate main progression behind them. (2) Each profession chapter should teach skills relevant to that role, not duplicate main-progression content. (3) Reward profession chapters with role-specific tools or materials, not generic items. (4) The number of profession chapters should reflect the pack's mod diversity — don't create 9 profession chapters if only 3 mods support distinct playstyles.

**pack_types:** expert, story
**Phase:** Step 2 (chapter design)
**Source confidence:** single-source (TheWinterRescue only) — insufficient data for generalization; decomposable into MP7+MP10+MP18

---

## Cross-Pack Comparison Table

| Pack | Genre | Quests | Task diversity | Avg tasks/quest | Dominant dep topology | Progression | Reward density |
|---|---|---|---|---|---|---|---|
| ATM-10 | Kitchen-sink | 4,601 | 3–4 types | 1.2 | Fan-out (depth 3–5) | `flexible` | 1.5/quest |
| ATM-9 | Kitchen-sink | ~2,300 | 4–5 types | 1.1 | Fan-out (depth 3–5) | `flexible` | 1.7/quest |
| ATM-8 | Kitchen-sink | ~1,000 | 3–4 types | 1.25 | Fan-out (depth 3–4) | `flexible` | 1.7/quest |
| All-the-Mons | Kitchen-sink + Cobblemon | ~2,400 | 5–6 types | 1.1 | Fan-out + islands | `flexible` | 1.2/quest |
| Create: Delight | Create + culinary | 2,295 | 9 types | 1.1 | Fan-out + islands | `flexible` | 0.43/quest |
| Mechanomania | Create (minimal) | 395 | 7 types | 1.0 | Linear (depth 1–2) | `flexible` | 0.11/quest |
| Create: Astral | Create + space | ~650 | 6–7 types | 1.5 | Fan-out + linear | `flexible` | 1.0/quest |
| Monifactory | Expert/GregTech | 248 | 5+ types | 1.5–2.0 | Deep chain (depth 8–15) | `default`/`linear` | varies |
| ATM9-Sky | Skyblock | ~500 | 4–5 types | 1.1 | Deep chain (depth 18) | `default` | ~1.0/quest |
| ATM-10-Sky | Skyblock | ~2,860 | 7–8 types | 1.2 | Fan-out + linear | `flexible` | 1.7/quest |
| Arcana | Magic | ~550 | 3–4 types | 1.1 | Fan-out (17 roots) | varies | 2.0/quest |
| Prominence II | RPG | ~335 | 7 types | 1.3 | Mixed + image-gated | varies | varies |
| Create Skylands | Create + skyblock | ~100 | 2–3 types | 1.0 | Linear | `linear` | ~0.01/quest |
| Enigmatica 9E | Expert | 22 ch | 4–5 types (item, checkmark, observation, advancement, command) | 1.3–2.1 | Deep chain + command-heavy | `default` | varies |
| Monifactory (raw) | Expert/GregTech | 14 ch | 4 types (item, checkmark, dimension, gamestage) | 1.5–2.4 | Deep chain + quest_links | `default` | ~0.5–0.9/quest |
| Finality Genesis | Create + adventure + RPG | 35 ch | 9+ types (item, checkmark, kill, dimension, structure, observation, biome, advancement) | 1.3–1.4 | Mixed linear + fan-out | `default` | ~0.5–1.0/quest |
| Era of Black Death | Combat + RPG | 17 ch | 4 types (item, checkmark, kill, dimension) | 1.0 | Fan-out + linear | varies | ~1.0–2.0/quest |
| Craft to Exile Dissonance | ARPG + story | 12 ch | 3 types (item, kill, dimension) | 1.25 | Linear chain (act-based) | N/A | item-only (zero XP) |
| Enigmatica 10 | Expert | ~? | 4–5 types (est.) | ~1.3 (est.) | Deep chain (est.) | `default` (est.) | unknown — zero quest complaints on issue tracker |
| Craftoria | Kitchen-sink | ~? | 5–7 types (est.) | ~1.2 (est.) | Fan-out + linear | `linear` (confirmed by #607) | xp_levels-heavy (AP17) |
| FTB Skies 2 | Skyblock | ~? | 5+ types (est.) | ~1.2 (est.) | Deep chain | `default` (est.) | varies |
| GregTech-Odyssey | Expert/GregTech | 40 ch | 6+ types (item, checkmark, structure, observation, dimension, kill) | ~2.0 | Deep chain (109 multi-dep in MV) | `default` | ~1.0/quest + currency |
| No-Flesh-Within-Chest | Hardcore/combat | 18 ch | 5 types (item, checkmark, kill, structure, dimension) | ~1.5 | Linear chain + boss fan-out | `default` | ~0.85/quest + currency |
| TheWinterRescue | Expert/survival | 15 ch | 3 types (item, checkmark, frostedheart:insight) | ~1.8 | Linear + profession branches | `default` | ~0.83/quest + insight |
| Cabricality | Expert/Create | 14 ch | 2 types (item, checkmark) | ~1.1 | Linear + stage branching | `default` | ~0.59/quest (ZERO rewards on many) |
| ATM-6 | Kitchen-sink | 25 ch | 6 types (item, checkmark, kill, dimension, observation, advancement) | ~1.4 | Fan-out (depth 3-5) | `flexible` | ~1.25/quest (xp+random dominant) |
| Enigmatica 6 | Kitchen-sink | ~30 ch | 4 types (item, checkmark, kill, advancement) | ~1.7 | Fan-out + chain | `flexible` | ~0.63/quest (command-dominant: 455 cmd) |
| All-of-Fabric-3 | Kitchen-sink (Fabric) | 23 ch | 4 types (item, checkmark, kill, advancement) | ~1.8 | Fan-out + linear | `flexible` | ~0.66/quest (random-dominant: 363) |
| GreedyCraft | Kitchen-sink (multi-mode) | 3×15+ ch | 2 types (item, checkmark) sampled | ~1.0 | Unknown (JSON format) | varies | reward tickets + massive XP |

---

## Player-Perspective Patterns (Phase 2)

Patterns discovered from **player feedback, bug reports, and experience discussions** rather than config-level analysis. These complement the config-perspective patterns (MP1–MP26) above by capturing what players actually notice and care about — the experiential layer that raw config data doesn't reveal.

### PP1 — The Trust Contract (description accuracy)

**What players notice:** The quest description is the pack author's voice. When it accurately describes game mechanics, the player trusts the entire quest book as a guidance system. When it lies — even once — the player starts second-guessing every subsequent description.

**Pattern:** High-quality packs maintain a "trust contract" where every `description` string is verified against in-game reality. The description is not just flavor text; it's the primary tutorial channel. cesspit.net's analysis of expert packs observes that "this HUGE questbook, with more than 2000 quests, was at the same time a great guide to erase the problem of guessing" crafting combinations — the quest book IS the tutorial, and its accuracy determines whether the player can learn from it.

**Config implication:** The `description` field is free-form text with no validation against tasks or rewards. Every description should be treated as a claim that will be tested by the player. Verify: (1) item names match display names, (2) crafting instructions match JEI/EMI recipes, (3) claimed rewards match the `rewards` array, (4) mechanic descriptions match actual mod behavior. Re-verify after mod updates.

**Source:** cesspit.net analysis; FTB Evolution issue #6447 (dozens of description-reality mismatches documented by a single player)

### PP2 — The Backward Shortcut (reward unlocks efficiency, not just progress)

**What players notice:** The best reward moments don't just give the player something new — they give the player a way to do something they already did, but faster. After reaching a milestone, the player unlocks a shortcut that optimizes their earlier work.

**Pattern:** Well-paced expert packs follow a loop: "you have to work hard to get to a milestone. Afterward, it also goes back, because sometimes you open new ways to get the same resources in much less time and effort." The reward is not just forward progression but backward optimization — the new machine processes the old ore 10× faster, the new tool mines the old material instantly.

**Config implication:** When designing rewards for milestone quests (tier-gate convergence, capstone components), include at least one reward that creates an efficiency loop back to earlier content. This can be: (a) a machine that automates an earlier manual process, (b) a tool that speeds up an earlier gathering task, (c) an alternative recipe that uses more abundant materials. This is a stronger reward than raw materials because it compounds over time.

**Source:** cesspit.net — "you simply unlock backward-facing shortcuts that let you 'optimize' what you've done up to that point"

### PP3 — The Invisible Wall (unreachable content without explanation)

**What players notice:** When a quest is visible but grayed out with no indication of what's needed to unlock it, the player feels stuck. When a quest is hidden entirely (via `hide_until_deps_visible`) with no signpost, the player doesn't even know content exists.

**Pattern:** Players tolerate gating — they accept that some content is locked behind prerequisites. What they don't tolerate is gating without feedback. A locked quest that shows its dependencies (via dependency lines) tells the player "go do these first." A locked quest with `hide_dependency_lines: true` AND no visible path to it tells the player nothing — it's an invisible wall.

**Config implication:** For every quest with `hide_until_deps_visible: true`, ensure at least one of: (a) its dependency quest is visible and its description mentions what it unlocks, (b) a visible "signpost" quest nearby hints at the hidden content, (c) the hidden quest's discovery trigger is something the player will naturally encounter. Never combine `hide_until_deps_visible: true` with `hide_dependency_lines: true` on the same quest — the player has no signal that content exists.

**Source:** FTB Evolution issue #6447 ("There's a permanently hidden quest"); Phase 1 data on `hide_until_deps_visible` usage patterns

### PP4 — The Completionist's Dilemma (100% requires impossible content)

**What players notice:** The chapter completion percentage. When it stalls below 100% and the player has completed every visible quest, they know something is broken. This is especially damaging in the first chapter — the "Getting Started" chapter is the player's first impression of the pack's quality.

**Pattern:** Chapter completion tracking counts ALL quests in the chapter, including `secret`, `always_invisible`, and unreferenced quests. If any quest in the chapter is unfinishable (missing item, broken dependency, permanently hidden), the chapter can never reach 100%. Perfectionist players will spend hours searching for the missing quest before giving up.

**Config implication:** (1) The `optional: true` flag excludes a quest from completion percentage calculation — use it for placeholder or future content. (2) Test every chapter for 100% completability by completing all non-optional quests and verifying the percentage. (3) If a quest is intentionally secret, make its discovery trigger something the player will naturally encounter during normal progression. (4) The starter chapter MUST be 100% completable — it's the pack's quality handshake.

**Source:** FTB Evolution issue #6447 ("It isn't possible to complete the 'Getting Started' chapter, even if you complete every quest")

### PP5 — The Context Void (quests without "why")

**What players notice:** When a quest shows only an item icon and a task count with no description, the player completes it mechanically — "get 4 iron ingots" — without understanding the item's role in the pack's progression. The quest book becomes a shopping list.

**Pattern:** Players need three pieces of information per quest: WHAT (the item — shown by the task icon), HOW (how to obtain it — the description), and WHY (what it leads to — the description or the reward). When the description is empty, the player gets WHAT from the icon but must figure out HOW and WHY themselves. For experienced players who know the mod, this is tolerable. For new players, it's a wall.

**Config implication:** The minimum viable description is one sentence that combines HOW and WHY: "Smelt iron ore in a furnace — you'll need this for your first set of tools." This sentence costs nothing to write but transforms the quest from a checklist item into a learning moment. For recipe-catalog packs that intentionally minimize hand-holding, at least provide the item's role: "Iron is the base material for most early-game tools and machines."

**Cycle 3 validation (expert pack variant):** Monifactory #2359 — "[Feature]: Better Tutorialisation of Basic Mechanics" — a player explicitly requests that quests introducing key GregTech features provide more information. The Infiniter Water quest is singled out: the Aqueous Accumulator requires configuration (pump setup, water source adjacency) that the quest doesn't mention, causing players to waste ~30 minutes before realizing the mechanic exists. The player's framing — "give missions that introduce key features to Gregtech some more information about their mechanics" — directly maps to PP5's WHAT/HOW/WHY framework. In expert packs, PP5 is amplified because the questbook IS the tutorial (MP23/MP30): there's no alternative in-game guidance for GregTech-specific mechanics.

**Source:** FTB Evolution issue #6447 ("None of the quests have text — new players might not know why they'd want so much diversity"); cesspit.net (quest book as guide); [Omicron-Industries/Monifactory #2359](https://github.com/Omicron-Industries/Monifactory/issues/2359)

### PP6 — The Wrong Tool Reward (reward-target mismatch)

**What players notice:** When a quest rewards a tool or item that seems relevant but is actually the wrong one for the pack's specific mod combination, the player is confused. "Why did I get an Immersive Engineering hammer? The next quest needs an Oritech wrench."

**Pattern:** This is a specific variant of the reward disconnection (MP26) that occurs when the pack uses multiple mods that have overlapping tool categories. The reward author picks a tool from the "wrong" mod — one that's thematically appropriate but mechanically useless for the actual next step. This is particularly common in kitchen-sink packs where 5+ mods might each provide a "wrench" or "hammer" tool.

**Config implication:** When rewarding a tool, verify that the specific tool ID matches what the next quest's description or task requires. Don't assume "a wrench is a wrench" — in a multi-mod pack, each mod's wrench is a distinct item with distinct recipes. The reward should be the exact tool the player needs for the next quest, not a thematic equivalent.

**Source:** FTB Evolution issue #6447 ("rewards the immersive engineering hammer, rather than the Oritech wrench")

### PP7 — The Mod-Unification Trap (same name, wrong mod)

**What players notice:** The player obtains the item the quest asks for — same display name, same icon — but the quest doesn't accept it. Or the quest does accept it, but the item doesn't work in the next recipe. The player has "steel dust" but the quest needs `modern_industrialization:steel_dust`, not `ftbmaterials:steel_dust`. Two mods provide items with the same name, and the wrong one was used — either in the task or the reward.

**Pattern:** In kitchen-sink packs with 200+ mods, multiple mods often provide functionally overlapping items: steel dust, electrum ingot, arcane crystal dust, bronze gear. Ore-dictionary / tag unification tries to collapse these into a single canonical item, but it doesn't always succeed — some items have the same display name but different namespaces and different recipe compatibility. When a quest task or reward references the wrong variant, the player hits a wall: "I have exactly what the quest asks for, and it won't accept it" or "the quest accepted it but the item doesn't work in the machine."

**Config implication:** When authoring item tasks and rewards in multi-mod packs: (1) Always use the full `modid:item_name` identifier, not just the display name. (2) For common intermediates (ingots, dusts, plates, gears), verify which mod's variant is the "canonical" one for the pack's recipe chains — typically the mod whose processing chain the quest is teaching. (3) When rewarding an item that the next quest needs, verify that the reward's namespace matches the next quest's task namespace. (4) Test with all mod variants present in the pack — an item that's unique in a 50-mod pack might have 3 duplicates in a 200-mod pack.

**Real case (FTB Skies 2, #11432):** The Steam Blast Furnace quest rewards `ftbmaterials:steel_dust` — but the MI steam blast furnace the player just built requires `modernindustrialization:steel_dust` (uncooked). Same display name "Steel Dust," different mod, incompatible recipes. The player crafted the blast furnace, received the reward, and then discovered the reward was useless for the machine they just built.

**Real case (FTB Evolution, #6447 items 25/37/54-57):** Multiple items suffer from the unification trap: "Placing silver and gold in a Modern Industrialization alloy smelter produces an unusable form of electrum" (#25); "There are recipes for two kinds of netherite dust" (#37); "There are two recipes for uranium blocks" (#57); "The occultism crusher produces a FTB variant of arcane crystal dust that has no practical uses" (#68). In each case, the same display name maps to different items with different recipe compatibility.

**Relationship to existing patterns:** PP7 is a specific player-experience variant of AP6 (Dead-End Reward) and AP1 (Description-Reality Mismatch). It's distinguished by its root cause: the mismatch isn't a wrong item entirely, but a wrong *variant* of a correct item. The quest author knew they needed "steel dust" but picked the wrong mod's steel dust. This makes it harder to detect through static analysis (R10/R11) because the item ID is valid — it's just not the *right* valid item ID.

**Source:** [FTBTeam/FTB-Modpack-Issues #11432](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/11432), [FTBTeam/FTB-Modpack-Issues #6447](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447) items 25/37/54-57/68

---

## Sources

Packs with **confirmed config access** (configs read directly from GitHub or local audit):

1. **ATM-10** (AllTheMods/ATM-10 on GitHub, MC 1.21.1, NeoForge) — 64 chapters, full config access via raw GitHub URLs. Source: https://github.com/AllTheMods/ATM-10/tree/main/config/ftbquests/quests
2. **Create: Delight Remake** (1.20.1, Forge, FTB Quests 2001.4.17) — 41 chapters, 2,295 quests, SNBT inline. Audited 2026-06-29, data in reference §20.
3. **Mechanomania** (1.21.1, NeoForge, FTB Quests 2101.1.21) — 18 chapters, 395 quests, SNBT + lang files. Audited 2026-06-29, data in reference §20.
4. **ATM-9** (AllTheMods/ATM-9 on GitHub, MC 1.20.1, Forge) — 67 chapters, 9 chapter groups, config access via GitHub API. Source: https://github.com/AllTheMods/ATM-9/tree/main/config/ftbquests/quests
5. **All-the-mods-10-Sky** (AllTheMods, MC 1.21.1, NeoForge) — 52 chapters, 4 chapter groups, config access via GitHub API. Source: https://github.com/AllTheMods/All-the-mods-10-Sky/tree/main/config/ftbquests/quests
6. **ATM-8** (AllTheMods/ATM-8 on GitHub, MC 1.19.2, Forge) — 32 chapters, config access via GitHub API. Source: https://github.com/AllTheMods/ATM-8/tree/main/config/ftbquests/quests
7. **All-the-Mons** (AllTheMods, MC 1.21.1, NeoForge) — 73 chapters, ATM10 + Cobblemon variant, config access via GitHub API. Source: https://github.com/AllTheMods/All-the-Mons/tree/main/config/ftbquests/quests
8. **Create: Astral** (Laskyyy/Create-Astral on GitHub, Fabric 1.18.2) — 12 chapters, 1 chapter group, config access via GitHub API. Source: https://github.com/Laskyyy/Create-Astral/tree/main/config/ftbquests/quests

Packs with **structure data from design guide audit** (config structure verified, quantitative data from prior audit):

9. **Monifactory** (GregTech CEu successor, 1.20.1) — 5 chapters / 248 quests, expert web layout. Data from design guide §pack-type-patterns.
10. **ATM9-Sky** (AllTheMods, skyblock, 1.20.1) — skyblock tutorial patterns. Data from design guide §pack-type-patterns.
11. **Arcana** (AllTheMods, magic-focused, MC 1.20.1, NeoForge) — 42 chapters, GitHub API access confirmed. Data from design guide §pack-type-patterns + raw GitHub. Source: https://github.com/AllTheMods/Arcana
12. **Prominence II** (RPG/adventure, 1.20.1) — 335 quests, 7 chapter groups, dependency-gated images. Data from design guide §pack-type-patterns.
13. **Create Skylands** — age-based chapters, linear progression, minimal rewards. Data from design guide §pack-type-patterns.
14. **Enigmatica 9: Expert** (1.19.2) — dual normal/expert chapters. CurseForge: https://www.curseforge.com/minecraft/modpacks/enigmatica9expert
15. **ATM-11** (kitchen-sink, mentioned in design guide).

Packs **searched but not obtained** (no public config access):

- **GregTech New Horizons** — uses BetterQuesting (1.7.10 era), not FTB Quests. Config format incompatible.
- **Divine Journey 2** — uses BetterQuesting (1.12.2). GitHub: https://github.com/Divine-Journey-2/main (config/betterquesting, not ftbquests).
- **Project Ozone 3** — uses BetterQuesting (1.12.2).
- **SkyFactory 4** — no public GitHub repo with quest configs found.
- **Create: Above and Beyond** — no public repo found with accessible configs.

Packs with **issue-tracker player feedback data** (Cycle 3 Phase 2, no config access but rich issue data):

16. **Enigmatica 10** (EnigmaticaModpacks/Enigmatica10, MC 1.21.1, NeoForge) — Expert pack. ~20 recent issues, ZERO quest design complaints. Negative evidence: effective QA process. https://github.com/EnigmaticaModpacks/Enigmatica10/issues
17. **Monifactory** (Omicron-Industries/Monifactory, MC 1.20.1) — Expert/GregTech pack. ~10 quest-related issues: tutorialisation debt (#2359), Yeta Wrench description omission (#1545), quest typos (#2546), quest crash (#2598). Low complaint volume overall. https://github.com/Omicron-Industries/Monifactory/issues
18. **Craftoria** (TeamAOF/Craftoria, MC 1.21.1, NeoForge) — Kitchen-sink pack. 8+ quest design issues: gating complaints (#231, #607, #352), xp_levels reward relativity (#289), NBT quest failure (#666), content requests (#440, #629). Richest new source for reward economy and gating issues. Uses `linear` progression mode (confirmed by #607). https://github.com/TeamAOF/Craftoria/issues

Packs with **Cycle 6 Phase 1 config access** (GitHub raw data, quantitative analysis):

19. **ATM-6** (AllTheMods/ATM-6, MC 1.16.5, Forge) — 25 chapters, ~1674 quests. Full SNBT access. Source: https://github.com/AllTheMods/ATM-6/tree/main/config/ftbquests/quests/chapters
20. **Enigmatica 6** (EnigmaticaModpacks/Enigmatica6, MC 1.16.5, Forge) — 23+ chapters, ~858 quests sampled. Full SNBT access. Source: https://github.com/EnigmaticaModpacks/Enigmatica6/tree/main/config/ftbquests/quests/chapters
21. **All-of-Fabric-3** (TeamAOF/All-of-Fabric-3, MC 1.16.5, Fabric) — 23 chapters, ~615 quests. Full SNBT access. Source: https://github.com/TeamAOF/All-of-Fabric-3/tree/main/config/ftbquests/quests/chapters
22. **GreedyCraft** (TCreopargh/GreedyCraft, MC 1.12.2, Forge) — 3 quest modes × 15+ chapters. JSON format (not SNBT). Source: https://github.com/TCreopargh/GreedyCraft/tree/main/config/ftbquests

---

## Part 10: Cycle 7 Patterns (MP38) — Player Feedback Cross-Validation

### MP38 — Reward Perception Split (kitchen-sink generosity debate)

**Pattern:** In kitchen-sink packs with `flexible` progression mode, generous quest rewards (high-tier items, large XP, rare materials) create a **perception split** among players. One camp views generous rewards as progression-breaking inflation ("arbitrary progression steps are skipped for no reason"); the other views them as genre-appropriate design ("only giving away ATM Stars would truly ruin progression"). The split is rooted in different player expectations: players who approach kitchen-sinks as structured progression experiences (like expert packs) feel the rewards undermine the journey; players who approach them as sandbox toolboxes welcome the generous starting resources.

**Applicable when:** designing reward economy for kitchen-sink packs. Expert packs with `linear`/`default` progression don't face this split because gating prevents early access regardless of rewards. The split only emerges in `flexible` mode where rewards can genuinely bypass intended progression paths.

**Implementation要点:** (1) For kitchen-sinks with `flexible` mode, cap early-game quest rewards to materials the player would obtain within 1-2 hours of normal play — don't reward items that bypass multiple tiers of progression. (2) Reserve truly progression-breaking rewards (dimension-access items, endgame tools) for late-game capstone quests. (3) Use choice rewards (MP18) at key branch points so the player controls which progression path the reward supports, rather than receiving items that shortcut paths they haven't chosen. (4) Document the pack's reward philosophy in the quest book's introduction chapter so players know what to expect.

**Real case (ATM-10 Discussion #3539):** Player xiaoxiao921 argues "the quest book gives way too many rewards that break balance" — specifically, early Dragon Eggs, Ender Chests, and Ultimate Universal Cables bypass intended progression. The mining dimension allows 3 players to craft ore sight charms for only 4 nuggets, circumventing allthemodium scarcity. The poster summarizes: "arbitrary progression steps being are skipped for no reason." Collaborator TheBedrockMaster disagrees: "because it is a kitchen sink pack, only giving away ATM Stars would truly ruin progression." This is the clearest documentation of the reward perception split in the dataset.

**Verification source:** [AllTheMods/ATM-10 Discussion #3539](https://github.com/AllTheMods/ATM-10/discussions/3539), cesspit.net progression philosophy analysis

**验证置信度**: 中等 — 单一 GitHub Discussion (ATM-10 #3539) + cesspit.net 理论支撑。需第二个 kitchen-sink 包的 reward debate 数据交叉验证。

---

### MP43 — NPC Questline Economy Gate (quest-unlock-trading pattern)

**Pattern:** The pack provides NPCs (non-player characters) with individual backstories and questlines. Completing an NPC's questline unlocks access to that NPC's trading functions, creating a quest-gated economy. The player must invest time in quest completion before gaining access to economic resources, turning quest progress into an economic currency. This creates a dual-purpose quest system: quests provide both progression guidance AND economic access.

**Applicable when:** designing packs with NPC-based economy or trading systems. The pattern is most effective when (1) NPCs offer items that are difficult or impossible to obtain through crafting alone, (2) NPC quests are thematically connected to their trading inventory, and (3) the quest-to-trade unlock creates a natural progression flow rather than an arbitrary gate.

**Implementation要点:** (1) Each NPC should have a distinct personality and backstory expressed through quest descriptions — this transforms economic gates into narrative experiences. (2) Quest requirements should thematically match the NPC's specialty (e.g., a blacksmith NPC requires metalworking items). (3) The trading inventory should scale with quest completion — early quests unlock basic trades, later quests unlock advanced items. (4) Use FTB Quests `command` rewards to trigger NPC unlock scripts via KubeJS or Game Stages. (5) Ensure at least one NPC is accessible from the start to provide an early-game economic lifeline.

**Real case (DeceasedCraft):** 8+ NPCs with independent backstories and questlines. Completing an NPC's questline unlocks their trading functions ("完成任务即可解锁贸易功能"). The NPC system is integrated with the pack's zombie apocalypse theme — NPCs are survivors who trade essential supplies in exchange for quest completion proving the player's capability.

**Verification source:** [MC百科 modpack/409343](https://www.mcmod.cn/modpack/diff/0-409343.html) (DeceasedCraft), [mcshuo.com/resource/515](https://www.mcshuo.com/resource/515)

**验证置信度**: 低 — 单一来源 (DeceasedCraft)，无玩家反馈验证。需第二个 NPC questline 包交叉验证。

---

### MP44 — XP Investment Feedback Loop (quest-XP-skill tree cycle)

**Pattern:** Quest XP rewards feed into a custom skill tree or attribute system that enhances the player's capabilities. This creates a positive feedback loop: completing quests → earning XP → investing in skills → gaining power → completing harder quests → earning more XP. The XP serves dual purpose: vanilla level progression AND custom skill investment. This transforms XP from a throwaway reward (MP16 XP Drip) into a strategic resource that the player actively manages.

**Applicable when:** the pack includes a custom skill tree, attribute system, or XP-based progression mechanic. The pattern requires (1) a meaningful skill tree with impactful choices, (2) quest XP rewards that are a significant portion of total XP income, and (3) skills that tangibly affect gameplay (not just cosmetic bonuses).

**Implementation要点:** (1) Balance quest XP rewards so that quest completion provides ~30-50% of total XP income — enough to matter but not enough to make natural gameplay XP irrelevant. (2) Design the skill tree with meaningful branching choices that align with different playstyles (combat, crafting, exploration). (3) Use `xp_levels` reward type (not raw XP) for larger milestone rewards, and raw `xp` for incremental drip rewards. (4) Ensure the first few skill tree nodes are reachable within the first 1-2 hours of play to establish the feedback loop early. (5) AP17 (XP-Level Relativity) applies — ensure XP reward amounts remain meaningful across the full progression curve.

**Real case (DeceasedCraft + RAD3):** DeceasedCraft features a "自定义技能树以匹配多种战斗风格" (custom skill tree for various combat styles) where XP from quests feeds character development. Players use "经验值升级强化角色" (XP to level up and strengthen the character). RAD3 has a "被动技能树" (passive skill tree) for attribute enhancement alongside its 7545 quests. Both packs create XP-as-investment rather than XP-as-drip-reward.

**Verification source:** [mcshuo.com/resource/515](https://www.mcshuo.com/resource/515) (DeceasedCraft), [MC百科 modpack/1090](https://www.mcmod.cn/modpack/1090.html) (RAD3)

**验证置信度**: 低 — 2 个来源 (DeceasedCraft + RAD3)，均无玩家反馈验证。XP→skill tree 循环的概念在 RPG 游戏中普遍存在，但在 FTB Quests 整合包中作为设计模式的验证尚不充分。

---

### MP45 — Bilingual Quest Authoring (dual-language quest content)

**Pattern:** The pack's quest descriptions are authored in two languages simultaneously (typically the author's native language + English), rather than being translated after the fact. This ensures both language versions are first-class content, not afterthoughts. The bilingual approach expands the pack's potential audience while maintaining quality in both languages. This is distinct from community-driven translation patches (which are MP45-adjacent but not the same pattern).

**Applicable when:** the pack author is bilingual or has a bilingual team, and targets both a native-language community and the international English-speaking community. The pattern is most valuable for packs with deep recipe modifications (like KubeJS expert packs) where accurate quest descriptions are critical — machine translation of complex mod terminology produces poor results.

**Implementation要点:** (1) Use FTB Quests' built-in i18n support with `translation_key` fields rather than hardcoded bilingual text in descriptions. (2) Maintain parallel language files (e.g., `zh_cn.json` and `en_us.json`) with the same key structure. (3) Author both languages simultaneously during quest creation, not as a post-hoc translation pass — this catches terminology issues early. (4) For mod-specific terminology, create a shared glossary that both language versions reference. (5) Test both language versions with native speakers — bilingual authors may miss subtle issues in their weaker language. (6) GTM Community Pack #99 shows the demand: a Japanese translator requested i18n keys for quest descriptions, indicating the pack lacked translation infrastructure.

**Real case (Tree of Life + Path of Truth):** Tree of Life explicitly supports "语言支持：简体中文（zh_cn）、英语（en_us，测试中）" with English still in testing phase. Path of Truth has bilingual content reflecting its Chinese authorship and international aspirations. Both packs are Chinese-authored expert packs where accurate quest descriptions are essential due to deep recipe modifications.

**Verification source:** [MC百科 modpack/1272](https://www.mcmod.cn/modpack/1272.html) (Tree of Life), [MC百科 modpack/826](https://www.mcmod.cn/modpack/826.html) (Path of Truth), [GregTechCEu/GTCP-Modern #99](https://github.com/GregTechCEu/GregTech-Modern-Community-Pack/issues/99) (i18n demand)

**验证置信度**: 低 — 2 个来源 (Tree of Life + Path of Truth)，均为中国作者包，无玩家反馈验证。i18n 需求在 GTM #99 中被间接验证。

---

## Cycle 7 — Player Feedback Cross-Validation Summary

The following table summarizes which patterns from the 33-pack dataset received validation, challenge, or remained untested from Cycle 7 player feedback research.

### Patterns validated by player feedback

| Pattern | Validation evidence | Source |
|---|---|---|
| AP1 Description-Reality Mismatch | Monifactory #2359 (description omissions for GT covers, Smart Item Filter, Lossless Cables), E10 "MI quest description issue" | Monifactory, E10 issue trackers |
| AP4 Wrong Gating | Craftoria #231 (Powah), #607 (Iron's Spells, "should use flexible instead of linear"), #352 (optional-but-mandatory) | Craftoria issue tracker |
| AP5 Empty Quest Description | Monifactory #2359 (Aqueous Accumulator confusion, "spend way more time than needed, only to realise like 30 minutes later") | Monifactory issue tracker |
| AP8 Reward Inflation | ATM-10 #3539 (Dragon Egg, Ender Chests, Ultimate Cables "break balance") — validates inflation IS a player concern in kitchen-sinks | ATM-10 discussion |
| AP17 XP-Level Relativity | Craftoria #289 — detailed analysis of dozens of quests, "+3 XP Levels can range from 27 to many thousands" | Craftoria issue tracker |
| AP18 Reward Desert | Craftoria #231 — "go through 3 tiers of reactors with no relevant quest rewards, inconsistent with other progression" | Craftoria issue tracker |
| MP6 Linear Chain | Craftoria #231 player explicitly requests "restructure to be more linear" for learnability — validates linear chains as pedagogical tool | Craftoria issue tracker |
| MP14 Material Bridge | Indirectly validated — reward deserts (AP18) called out specifically when material bridges are missing | Craftoria #231 |
| MP16 XP Drip | Indirectly validated — xp_levels inconsistency (AP17) called out as contrast to consistent XP rewards | Craftoria #289 |
| MP23 Invisible Infrastructure | Monifactory invisible routing works well — player complaints are about visible tutorialisation, NOT invisible infrastructure | Monifactory #2359 |
| cesspit.net "Backward Shortcut" (PP2) | Re-validated: "unlock backward-facing shortcuts that let you optimize what you've done" described as core expert pack satisfaction | cesspit.net |

### Patterns challenged or corrected by player feedback

| Pattern | Challenge | Correction |
|---|---|---|
| Enigmatica 10 "zero quest complaints" | E10 actually has ~6 quest issues (Mekanism progression blocker, Occultism candle/chalice acceptance, wrong rewards, MI description) | Previous research overstated E10's cleanliness. Complaint volume is still lower than comparable packs, but "zero" was inaccurate. |
| AP8 "always bad" assumption | ATM-10 collaborator defends generous rewards as genre-appropriate for kitchen-sinks | AP8 severity depends on pack type and progression mode. In `flexible` kitchen-sinks, generosity is debated; in `linear` expert packs, it's unambiguously harmful. |
| "optional: true" as safe flag | Craftoria #352 shows optional-marked quests can be hard prerequisites | R7 (Optional-Gate-Mandatory) already detects this; AP19 now documents the player-experience dimension. |

### Patterns not yet validated from player perspective

| Pattern | Reason |
|---|---|
| or_tasks: true (flexible task completion) | No player discussions found about this mechanic |
| dependency-linked images (Prominence II) | Visual presentation rarely discussed in text-based feedback |
| Stage-based architecture (ModularTech) | ModularTech not widely discussed in player communities |
| hide_dependency_lines impact | Players discuss visual clutter indirectly (AP20) but don't reference the specific flag |
| Blessed-Or-Cursed zero-reward design | Pack has minimal community visibility (14 GitHub stars) |
| MP35 Dual-Task Automation (Cabricality) | Remains single-source from Cycle 6; no player feedback found |

### Player feedback priority ranking (by discussion frequency)

1. **Reward economy** (most discussed) — AP8, AP17, AP18, MP38 all validated from player reports
2. **Gating/progression blocking** — AP4, AP19 heavily reported in Craftoria
3. **Tutorial quality** — AP5 validated in Monifactory, the highest-quality expert pack
4. **Item acceptance bugs** (AP1 variant) — E10, Monifactory
5. **Visual presentation** — AP20 only one report (Craftoria Powah)
6. **Dependency visualization** — not directly discussed by players
