# FTB Quests — Anti-Patterns [ARCHIVED]

> **ARCHIVED:** This file has been superseded by the modular system.
> Content redistributed to: `mod-dependency-graph.md`, `mod-reward-design.md`, `mod-teaching-pacing.md`, `mod-description-trust.md`, `mod-system-safety.md`.
> Kept for git history reference. See `module-index.md` for the current structure.

---

## Section Navigation & Load Phase

| Section | Content | SKILL.md Step | Load timing |
|---|---|---|---|
| AP1–AP8 | 核心反面模式（配置/设计错误） | Step 2 (outline, 背景知识) | 规划阶段加载一次 |
| AP9–AP11 | AI 生成专属反面模式 | Step 4 (node generation) | 逐节点生成时参考 |
| AP12–AP13 | 任务系统机制缺陷 | Step 4 (node generation) | 逐节点生成时参考 |
| AP14–AP16 | 系统安全与兼容性 | Step 4 (node generation) | 逐节点生成时参考 |
| AP17–AP18 | Reward 经济与进度模式缺陷 | Step 2 (outline) / Step 4 | 规划阶段 + 生成时参考 |
| Sources | 数据来源 | — | 参考 |

> **注意：** anti-patterns.md 定位为「WHY」——解释每个错误的后果和成因。可执行的「HOW」（检测逻辑）在 `progression-rules.md` 中。Step 2 加载 AP1–AP8 和 AP17–AP18（reward 经济与进度模式）作为背景知识；Step 4 生成时重点参考 AP9–AP13（AI 生成专属风险和任务系统机制缺陷）以及 AP14–AP16（系统安全与兼容性风险）。

---

Common design mistakes in FTB Quests configurations, derived from real player feedback, bug reports, and pack-author retrospectives. Each anti-pattern documents what goes wrong, why, and how to fix it. The patterns are ordered by severity: the ones that halt player progression come first; the ones that merely annoy come last. AP9–AP11 address risks unique to AI-generated quest configurations. AP12–AP13 address quest-system mechanism defects that can arise regardless of authorship method.

## Summary

After analyzing player feedback across multiple platforms — GitHub issue trackers for FTB official packs, r/feedthebeast discussions, cesspit.net's in-depth analysis of expert-pack progression, and MC百科 community tutorials — eight recurring anti-patterns emerge. They cluster around the "three hard problems" identified in Phase 1 (item cross-tier, sequence inversion, reward disconnection), but the player-experience layer reveals dimensions the config-level signals alone miss: quest descriptions that lie, gating that creates circular deadlocks, chapters that are literally unfinishable, and hidden quests that strand players with no way forward.

The most damaging anti-pattern is not a missing dependency wire or a wrong reward — it's the **description-reality mismatch** (AP1). When a quest's text tells the player one thing but the game mechanics do another, the player loses trust in the entire quest book as a guidance system. As cesspit.net's analysis of expert-pack progression puts it: "good game design here doesn't even depend on the mod. It depends on… the questbook." When the questbook lies, the whole system collapses.

The second most damaging is the **circular dependency deadlock** (AP2), where two mods' progressions interlock in a way that makes both unreachable. This is distinct from the "item cross-tier" micro-pattern (MP24) — cross-tier is a one-directional overshoot; circular deadlock is a true loop where neither side can advance.

---

## AP1 — Description-Reality Mismatch

**Symptom:** The player reads the quest description, follows its instructions, and discovers the instructions are wrong. The quest asks for an item that doesn't exist under that name, references a mechanic that works differently, or claims a reward that isn't actually given.

**Root cause:** The quest author wrote the description based on an assumption about mod mechanics (or a different version of the mod) without verifying against the actual in-game behavior. In FTB Quests config terms, the `description` text is a free-form string that is never validated against the task/reward data — it's entirely the author's responsibility to keep it accurate.

**Consequence:** Players stop trusting quest descriptions and start ignoring them entirely. The quest book devolves from a guidance system into a checklist of opaque requirements. For new players who rely on the quest book as their primary tutorial, this is devastating — they're left Googling for answers the quest book should have provided.

**Fix:** Every quest description must be play-tested against the actual game mechanics before shipping. Specifically: (1) verify that every item name mentioned in the description matches the item's actual display name in the current mod version; (2) verify that any crafting instructions match the actual JEI/EMI recipe; (3) verify that any claimed rewards match the actual `rewards` array; (4) re-verify after mod updates that change recipes or item names.

**Real cases:**

From the FTB Evolution issue tracker (GitHub #6447), a player documented dozens of description-reality mismatches in a single modpack:

- "The Ore of the Eclipse Quest talks about Shadowflame Goo, but asks for Shadowpulse Goo. I don't think there's shadowflame goo in the pack." (Item name in description doesn't match the item in the task.)
- "The quest for xycraft extractors doesn't explain the orientation system" — the quest assumes the player knows a mechanic that isn't explained anywhere in the quest book, and the linked Reddit thread (r/direwolf20) shows players struggling with the same issue.
- "Making Multiblocks with Machine Cores" rewards the immersive engineering hammer, rather than the Oritech wrench (which is a task under "Basic Logistics")" — the reward is the wrong tool for the next quest.
- "The quest 'Empowered Crystal Blocks' says it provides a technology bundle, but it actually gives a choice reward" — the description promises one thing, the reward array delivers another.
- "Several quests in the Modern Industrialization chapter refer to EMI, rather than JEI" — the pack ships JEI but the quest text references a different recipe viewer.
- "The MI nuclear reactor can't explode, emit radiation, etc. This is buried in the middle of its guidebook entry — it would be nice if the quest mentioned this. The other nuclear reactors in this pack are both quite perilous." — the quest fails to warn the player about what's different about this reactor.
- "The Blood Essence quest doesn't mention that the deaths have to be player kills. Fun fact: when it rains pigs, and they go splat, it's entirely bloodless process…" — a critical mechanic is omitted from the description.

From the FTB Architect's Exodus issue tracker (GitHub, 2025–2026), five additional AP1 cases confirm this pattern persists across FTB official packs:

- #12549 — "Terrestrial Agglomeration Plate" quest states a Dominant Spark Augment is needed on the spark, but the plate actually pulls from mana pools with normal sparks. The augment also creates a circular prerequisite: it requires Pixie Dust from the Alfheim Portal, which requires Terrasteel — the goal of the *next* quest. (Description lies about mechanics AND the task has a circular dependency with the subsequent quest.)
- #12571 — "Slay Skol and Hati" quest text says "Prove to Jormungandr, which we killed a few realms earlier" — the task references the wrong boss entirely.
- #12458 — "Sentient Tools" quest states the Sentient Scythe "harvests souls" and equipment improves based on "souls in the Tartaric Gem" — the actual mechanic uses Demonic Will, not Souls. Wrong game-mechanic terminology.
- #12459 — "Bottle o' Lightning" quest only accepts 3 specific spells (2 Uncommon, 1 Common) when it should accept all 4 Common Lightning Spells. The description's claim and the task's acceptance criteria are both wrong.
- #12426 — "The Basics" quest asks for a stone pickaxe instead of a wooden one — the very second quest a new player sees has the wrong item.

From Create: Astral's issue tracker (GitHub, 2024–2025):

- #613 — "Automate Lapis!" quest wrongly states Asurine can be milled into Zinc. The actual recipe produces Lapis Lazuli. Description-recipe mismatch.
- #618 — "Pressmarine Shards" quest claims prismarine is "useful in automating veridium (for copper) later on" — no veridium recipe uses prismarine. The description fabricates a recipe relationship that doesn't exist.

**Cycle 2 validation:** AP1 remains the single most frequently reported anti-pattern across all data sources. In the recent FTB-Modpack-Issues stream (last 30 quest-related issues as of July 2026), at least 8 are AP1 variants. Create: Astral's issue tracker has 2 confirmed AP1 cases among its ~15 quest-related bugs. The pattern is consistent: the `description` field is free-form text with no validation against tasks, rewards, or actual mod mechanics, making it the primary failure point for quest quality.

**Cycle 3 validation:** AP1 continues to dominate with new variants. FTB Evolution #12609 — "Throwing Daggers" quest calls for 'raw spiritus' but the actual drop is 'spiritus essence', preventing quest completion and blocking the entire hellfire forge sub-chain. FTB Evolution #12584 — Enderman/Spectral/Glowstone Talisman descriptions say they're used for "Force of the Overworld" but the actual crafting target is "Force of the Explorer." Monifactory #1545 — the questbook doesn't warn that EnderIO's Yeta Wrench crouch-scroll mechanic is broken in the current mod version, forcing the player to rip out cabling instead of reconfiguring. This is an AP1 variant where the description fails to warn about a known mod bug. Across Cycle 3, AP1 is now validated in 7+ packs (FTB Evolution, Architect's Exodus, StoneBlock 4, Skies 2, Create: Astral, Monifactory, Craftoria).

**Source:** [FTBTeam/FTB-Modpack-Issues #6447](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447), [FTBTeam/FTB-Modpack-Issues #12549](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/12549), [Laskyyy/Create-Astral #613](https://github.com/Laskyyy/Create-Astral/issues/613), [Laskyyy/Create-Astral #618](https://github.com/Laskyyy/Create-Astral/issues/618), cesspit.net analysis

---

## AP2 — Circular Dependency Deadlock (Catch-22)

**Symptom:** The player needs item A to get item B, but also needs item B to get item A. Neither side of the loop is obtainable, and the quest book presents both as next steps. The player is softlocked.

**Root cause:** Two mods' progression chains interlock in a cycle. In FTB Quests config terms, this manifests as a `dependencies` cycle at the cross-mod level — quest X (mod A) depends on quest Y (mod B), and quest Y depends on quest X. It can also manifest without explicit `dependencies`: quest X requires an item from mod A's crafting chain, which requires an item from mod B's crafting chain, which requires the item from mod A. The `dependencies` array may not even contain the cycle — the cycle lives in the recipe graph.

**Consequence:** The player cannot progress in either mod line. In a `default` (locked) progression mode, the quests simply don't unlock. In `flexible` mode, the player can see the quests but can't complete them. Either way, the player is stuck.

**Fix:** Break the cycle by providing one side of the loop as a quest reward, a loot table drop, or an alternative recipe. If mod A needs mod B's output and mod B needs mod A's output, add a quest that rewards mod B's input material, or add a KubeJS script that provides an alternative crafting path for one of the items.

**Real case:**

From FTB Evolution issue #6447: "There's a catch 22 in the occultism progression — red chalk requires torch flowers, summoning torch flower seeds requires a heart of the sea, a heart of the sea requires red chalk. Unlike most of the occultism progression, this one doesn't benefit from possessed creature summoning. And, in the heavily modded world gen, finding sniffer eggs the vanilla way is time consuming."

This is a textbook circular deadlock: red chalk → torch flower seeds → heart of the sea → red chalk. None of the three items can be obtained without already having another one from the loop. The player must either find a sniffer egg (a rare vanilla mechanic in modded terrain) or the pack author must provide an alternative path.

From FTB Skies 2 issue #9084 (2025): A within-mod circular deadlock in Productive Bees — to craft a Beebee spawn egg, the player needs a Beebee type gene from the gene/incubator system. To get that gene, the player must already have a Beebee bee to "squash." No natural spawns, no breeding recipe, no quest reward, and no loot table provides the first Beebee. This creates a hard progression deadlock for the Uru bee chain. Unlike the FTB Evolution case (which was cross-mod), this deadlock lives entirely within a single mod's progression — making it harder to detect by cross-mod dependency auditing.

**Cycle 2 validation:** AP2 confirmed in both cross-mod (FTB Evolution) and within-mod (FTB Skies 2) variants. The within-mod variant is particularly insidious because it doesn't show up in cross-mod dependency graphs — the cycle is internal to one mod's recipe chain.

**Source:** [FTBTeam/FTB-Modpack-Issues #6447](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447), [FTBTeam/FTB-Modpack-Issues #9084](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/9084)

---

## AP3 — Unfinishable Chapter

**Symptom:** The player completes every visible quest in a chapter, but the chapter completion percentage never reaches 100%. There's a hidden quest, an invisible quest, or a quest with impossible requirements that blocks completion.

**Root cause:** A quest exists in the config but is either (a) `always_invisible: true` or `secret: true` and the player can't discover it, (b) gated behind a condition that's unreachable in the current pack configuration, or (c) has a task that references an item/mechanic that doesn't exist. In FTB Quests config terms, the quest object exists in the `.snbt`/`.json5` file but the player has no way to interact with it.

**Consequence:** Perfectionist players (and completion-tracking UI) report the chapter as incomplete. The player wastes time trying to find what they're missing, often resorting to reading the config files directly to find the hidden quest. This is a trust-breaking moment — the player realizes the quest book is lying about what's completable.

**Fix:** (1) Run a validation pass that checks every quest's tasks are completable with the current mod set. (2) Ensure that `secret` quests have a discoverable trigger (a biome visit, an item pickup, a boss kill). (3) If a quest is intentionally unfinishable (a placeholder or future content), exclude it from completion tracking with `optional: true` or move it to a separate "WIP" chapter. (4) Test that completing every non-optional quest in a chapter produces 100% completion.

**Real cases:**

From FTB Evolution issue #6447: "It isn't possible to complete the 'Getting Started' chapter, even if you complete every quest." — a player reports that the starter chapter, the very first thing a new player sees, cannot be 100% completed.

Also from the same issue: "There's a permanently hidden quest in 'The Traveler's Quest' Chapter." — a quest exists in the config but has no way to be discovered or completed by the player.

**Source:** [FTBTeam/FTB-Modpack-Issues #6447](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447)

---

## AP4 — Wrong Gating (Over-Restrictive Dependencies)

**Symptom:** A quest requires ALL of several prerequisites when it should only require ONE. Or a quest is gated behind an optional quest, making it unreachable for players who skip the optional content. Or a quest chain is marked as mandatory when it should be optional.

**Root cause:** The `dependency_requirement` field is set to `"all"` (the default) when it should be `"one_completed"` or `"one_started"`. Or the `dependencies` array includes quests from an optional branch that the player may have skipped. In FTB Quests config terms, the default `dependency_requirement: "all"` means every quest in the `dependencies` list must be completed — this is almost always wrong when the dependencies are parallel alternatives rather than sequential prerequisites.

**Consequence:** Players who follow a different path through the quest book find themselves locked out of content they should have access to. In expert packs with `default` (locked) progression, this is a hard block — the quest simply won't unlock. In kitchen-sinks with `flexible` progression, the quest remains grayed out, confusing the player about whether they've missed something.

**Fix:** (1) For branching paths where the player picks one of several alternatives, set `dependency_requirement: "one_completed"` on the convergence quest. (2) Never gate mandatory content behind optional quests — if quest A is `optional: true`, no non-optional quest should depend on it. (3) Audit every `dependencies` list: if the dependencies are sequential (B requires A's output), `"all"` is correct; if they're parallel (the player can do A or B or C), use `"one_completed"`. (4) For "prove you've explored" gates (e.g., enter a dimension), a single `dimension` task is sufficient — don't require completing multiple dimension quests.

**Real cases:**

From FTB Evolution issue #6447:

- "The early energy generation quest requires all three generators, rather than just one." — the player is forced to build three different power generators when the intent was probably "build any one of these to get started."
- "The biofuel generator/reactor quest is gated behind the mycelial reactor quest, and not distinguished from the mycelial generators." — a parallel option is locked behind another parallel option.
- "The mandatory boss catcher quest is gated behind the optional Hephaestus Forge: Tier 4 quest." — mandatory content is unreachable for players who skip the optional forge chain.
- "Every single generator from industrial foregoing is required (rather than optional) to complete the Generating Power chapter. None of the quests have text (new players might not know why they'd want so much diversity)." — the entire chapter is mandatory with no explanation of why.
- "The diesel/boosted diesel quest chains in Modern Industrialization aren't optional, but they aren't a mandatory (or even particularly useful) part of the mod's progression." — quests that should be optional are forced.

**Cycle 3 validation:** Craftoria #231 — "Restructure Powah quests to be more linear" — a player reports the Powah chapter "throws everything at you" with over-restrictive dependencies: the reactor quest has dependencies that "should definitely not" exist, and players can go through 3 tiers of reactors with no relevant quest rewards. This is AP4 combined with AP6 (dead-end progression) — the gating structure forces players through an unnecessarily broad set of prerequisites. Craftoria #607 — "Change questbook gating for Iron's Spells" — a player explicitly suggests the pack should use `flexible` instead of `linear` mode because the Iron's Spells gating locks the basic crafting table behind a crying-obsidian requirement that blocks early-game progression. Craftoria #352 — a Mekanism questline quest is marked `optional: true` but is required as a dependency for mandatory quests on both sides, creating a misleading optional-but-actually-mandatory situation.

**Source:** [FTBTeam/FTB-Modpack-Issues #6447](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447)

---

## AP5 — Empty Quest Description (the Silent Node)

**Symptom:** The player opens a quest and sees… nothing. No description, no context, no guidance. Just an item icon and a task. The player has no idea why they need this item, how to get it, or what it unlocks.

**Root cause:** The quest was auto-generated or bulk-authored without filling in the `description` field. This happens when a pack author creates hundreds of quests from recipe data (a "recipe catalog" approach) and doesn't write descriptions for each one. In FTB Quests config terms, the `description` field is either absent, empty (`description: []`), or contains only a placeholder.

**Consequence:** The quest book becomes a meaningless checklist. Players can see WHAT to do (the task item) but not WHY or HOW. For experienced players who already know the mod, this is merely annoying. For new players, it's a wall — they see "obtain osmium ingot" with no context about what osmium is, where to find it, or why they need it.

**Fix:** Every quest must have at least a one-sentence description that answers: (1) what this item does, (2) how to obtain it (crafting, mining, mob drop, etc.), and (3) what it leads to. For recipe-catalog quests where the pack philosophy is "minimal hand-holding," at minimum include a one-line description explaining the item's role ("Osmium is Mekanism's base metal — you'll need it for every machine in the mod.").

**Real case:**

From FTB Evolution issue #6447: "Every single generator from industrial foregoing is required (rather than optional) to complete the Generating Power chapter. None of the quests have text (new players might not know why they'd want so much diversity)." — an entire chapter of quests with no descriptions, forcing players to complete them without understanding why.

From the cesspit.net analysis: the author praises packs where "this HUGE questbook, with more than 2000 quests, was at the same time a great guide to erase the problem of guessing" crafting combinations. The implication is clear: packs WITHOUT that guidance leave players guessing.

**Cycle 3 validation:** Monifactory #2359 — "[Feature]: Better Tutorialisation of Basic Mechanics" — a player explicitly requests that quests introducing key GregTech features provide more information about their mechanics. The Infiniter Water quest is called out as "especially confusing" because the Aqueous Accumulator mechanic requires configuration that the quest doesn't explain, causing players to "spend way more time than needed, only to realise like 30 minutes later that you need to configure the pump." This is AP5 in an expert pack context — the quest exists and has a task, but the description fails to explain the mechanic the player needs to understand. For a GregTech expert pack where the questbook IS the tutorial system (MP23 Invisible Infrastructure), missing descriptions have outsized impact because players have no other in-game guidance.

**Source:** [FTBTeam/FTB-Modpack-Issues #6447](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447), [cesspit.net](https://cesspit.net/drupal/node/2832/)

---

## AP6 — Reward That Doesn't Bridge (the Dead-End Reward)

**Symptom:** The player completes a quest and receives a reward that has no connection to anything they'll do next. The reward item isn't used in any upcoming recipe, isn't a tool needed for the next section, and isn't XP or currency. It's a dead-end — a trophy that sits in the inventory.

**Root cause:** The reward was chosen for thematic reasons ("this quest is about forestry, so the reward is a sapling") rather than progression reasons ("this quest is about forestry, so the reward is the charcoal that the next quest needs"). In FTB Quests config terms, the `rewards` array contains an item that doesn't appear in any dependent quest's `tasks` array, and isn't XP/currency/loot.

**Consequence:** The player accumulates a pile of random items that clutter their inventory without contributing to progression. More importantly, the reward fails to perform its primary function: bridging the player from one quest to the next (as documented in MP14–MP18 of the micro-patterns). The player finishes the quest and thinks "now what?" instead of "oh, I have what I need for the next step."

**Fix:** For every quest reward, ask: "Does this reward help the player with the NEXT quest?" If not, replace it with: (a) a material that the next quest requires (MP14 material bridge), (b) a tool the next section needs (MP15 tool reward), (c) XP as a universal baseline (MP16 XP drip), or (d) a choice reward that lets the player pick their next direction (MP18 choice reward). Cosmetic rewards (trophies, decorative items) are acceptable ONLY on truly optional quests where progression bridging doesn't matter.

**Real case:**

From FTB Evolution issue #6447: "Making Multiblocks with Machine Cores rewards the immersive engineering hammer, rather than the Oritech wrench (which is a task under 'Basic Logistics')." — the reward is the WRONG tool. The player receives an IE hammer when they need an Oritech wrench for the next quest. This is a specific variant of the dead-end reward: the reward is a tool, but the wrong tool for the pack's actual progression.

Also from issue #6447: "'The Quantum Computer Structure' quest says the structure can be a 3x3, 4x4 or 5x5 square. Based off the number of structure blocks it requires, these are external dimensions. The guidebook says a 7x7x7 (external) is also valid. I haven't tested even dimensions, but the guidebook makes no reference to this restriction." — this is an information gap that could have been bridged by a reward of the guidebook item with the correct page reference.

From FTB Skies 2 issue #11432 (2025): The Steam Blast Furnace quest rewards the player with steel dust from the FTB Materials mod — but the machine the player just built (MI steam blast furnace) requires uncooked steel dust from the Modern Industrialization mod. Same item display name ("steel dust"), different mod namespace, incompatible recipes. This is the multi-mod unification variant of AP6: the reward is technically a "steel dust" but it's the wrong mod's steel dust for the next step.

**Cycle 2 validation:** AP6 confirmed with a new variant — the mod-unification trap. When multiple mods provide items with the same display name but different namespaces, the quest author can easily pick the wrong one. This is especially common for generic intermediates like "steel dust," "electrum ingot," or "arcane crystal dust."

**Source:** [FTBTeam/FTB-Modpack-Issues #6447](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447), [FTBTeam/FTB-Modpack-Issues #11432](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/11432)

---

## AP7 — Hidden Quest Trap (Progressive Reveal Without Signposts)

**Symptom:** The player completes a section of the quest book and moves on, unaware that there are more quests in that section — because `hide_until_deps_visible: true` keeps them hidden until their dependencies are met, and the dependencies require actions the player doesn't know to take. The quests exist but are permanently invisible.

**Root cause:** Overuse of `hide_until_deps_visible` without providing a visible signpost that leads the player to the hidden content. In FTB Quests config terms, a quest with `hide_until_deps_visible: true` remains invisible until its `dependencies` are in a "visible" state. If the dependency is a biome visit, a specific item pickup, or a dimension entry that the player has no reason to perform, the quest stays hidden forever.

**Consequence:** Players miss entire branches of content. In narrative packs where hidden quests contain story progression, this can softlock the player's understanding of the plot. In expert packs, hidden quests may contain critical tutorial information that the player needs but never sees.

**Fix:** (1) For every quest with `hide_until_deps_visible: true`, ensure that its dependency is something the player will naturally encounter during normal gameplay. (2) Add a visible "signpost" quest (with `hide_until_deps_visible: false`) that hints at the hidden content: "There's something interesting about the Swamp biome — explore it when you get a chance." (3) Limit `hide_until_deps_visible` to truly secret/bonus content; don't use it for main-progression quests. (4) Test by playing through the chapter without deliberately seeking hidden content — if you miss important quests, the reveal triggers need adjustment.

**Real case:**

From the micro-patterns Phase 1 research: `hide_until_deps_visible` usage varies dramatically across packs. Create: Delight uses it on 72 quests (for progressive recipe reveals); Mechanomania uses it on 0. ATM-10 uses it sparingly (~3% of quests). The packs that use it heavily (Create: Delight) pair it with visible hub quests that act as signposts; packs that don't pair it with signposts risk the trap.

From FTB Evolution issue #6447: "There's a permanently hidden quest in 'The Traveler's Quest' Chapter." — a quest that should be discoverable is instead permanently invisible due to misconfigured visibility settings.

**Source:** [FTBTeam/FTB-Modpack-Issues #6447](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447), Phase 1 micro-patterns quantitative data

---

## AP8 — Reward Inflation (Too Much Too Early)

**Symptom:** Early quests give generous rewards (stacks of diamonds, high-tier materials, large XP amounts), making the early game trivially easy. By mid-game, the pack has "run out" of meaningful rewards — everything the player needs is already in their chest from earlier quest rewards. Late-game quests offer rewards the player doesn't need.

**Root cause:** The reward curve was not planned as a whole-book economy. Each chapter's author independently chose rewards without coordinating with other chapters. In FTB Quests config terms, early chapters have `rewards` with high-value items and large `count` values, while late-game chapters offer the same or lower values — the relative value drops as the player's wealth increases.

**Consequence:** The player's sense of progression is front-loaded. Early game feels generous and exciting; mid-game feels stagnant ("I already have all of this"); late-game feels pointless ("why bother with the reward when I crafted this 20 quests ago?"). This is especially damaging in expert packs where the reward economy is supposed to pace the player's advancement.

**Fix:** (1) Plan the reward economy at the book level, not the chapter level. Define reward tiers (early, mid, late, endgame) and what each tier can give. (2) Early rewards should be tools and small material quantities (1–4 items); mid-game rewards can be moderate stacks (8–16); late-game rewards should be rare materials or unique items. (3) Use XP drip (MP16) as a universal baseline that scales with quest difficulty, not with chapter position. (4) Reserve the richest rewards for capstone quests and convergence points (MP8). (5) For kitchen-sink packs where each chapter is independent, cap per-chapter rewards at a "chapter budget" to prevent any single chapter from inflating the economy.

**Real case:**

From the cesspit.net analysis of expert-pack progression: "you have to work hard to get to a milestone. Afterward, it also goes back, because sometimes you open new ways to get the same resources in much less time and effort." The author describes a well-designed reward economy where milestones unlock backward-facing shortcuts — the reward for reaching a milestone is not just a shiny item, but a new efficiency path for earlier content. This is the opposite of inflation: it's deflationary, giving the player tools to optimize rather than raw materials to stockpile.

The same analysis notes that packs without this structure suffer from "making everything behind obsolete as it happens in many (not sandbox-y) games" — the early content becomes irrelevant because the rewards outpaced the difficulty curve.

**Source:** [cesspit.net — Minecraft Is Not What You Think](https://cesspit.net/drupal/node/2832/)

---

## AI-Generation Anti-Patterns (AP9–AP11)

The following three anti-patterns are specific to AI-generated quest configurations. They do not arise from human pack-author mistakes but from the systematic biases and failure modes of language models generating structured game content at scale. Each is a distinct risk that the existing AP1–AP8 framework does not address.

### AP9 — Hallucination Cascade (fabricated IDs that compound)

**Symptom:** An AI-generated quest references an item ID that doesn't exist in the pack (e.g., `mekanism:quantum_infuser` when the actual ID is `mekanism:antiprotonic_nucleosynthesizer`). A subsequent quest — generated in the same batch — then depends on that fabricated item, and a third quest rewards a "crafting recipe" for it. The hallucination cascades: one wrong ID spawns a chain of quests all built on fiction.

**Root cause:** AI language models generate text token-by-token without a verification step against the pack's actual item registry. The "never hallucinate" rule in SKILL.md prevents *intentional* fabrication, but subtler errors slip through: wrong item *counts* (AI guesses 64 when the recipe needs 16), wrong *dependency ordering* (AI assumes a mod's internal progression without verifying the actual recipe chain), wrong *mod interactions* (AI assumes mod A integrates with mod B when they don't). When generating a batch of 50+ quests, a single early hallucination can pollute the entire batch because subsequent quests build on the generated context.

**Consequence:** The player encounters quests that reference nonexistent items, broken recipes, or impossible dependencies. Unlike a human author's typo (which affects one quest), an AI hallucination propagates through the dependency chain, creating a cluster of broken quests that are individually plausible but collectively impossible.

**Fix:** (1) Every item ID in a generated quest must be verified against `items.json5` before the quest is finalized — not just at generation time but after each batch. (2) When generating dependent quests in the same batch, the AI should re-verify that all referenced items from earlier quests in the batch actually exist, rather than trusting its own prior output. (3) Add a "hallucination audit" step after batch generation: scan all item IDs in the batch against the pack's item registry, flag any that don't match, and regenerate only the affected quests.

**Related rules:** R23 (Description-Item Consistency) provides partial static detection. The core prevention is the generation-time `items.json5` check in SKILL.md.

---

### AP10 — Style Homogenization (every quest sounds the same)

**Symptom:** Every quest description in a chapter follows the same template: "Obtain [item]. This is needed for [next step]." Every reward is "10 XP + 1 item." Every quest uses the same shape and size. The chapter reads like it was generated by a form letter, not designed by someone who understands the mod.

**Root cause:** AI language models have strong priors toward uniform output. Without explicit variation guidance, the model converges on a single "safe" template and repeats it. This is not a hallucination — every quest is technically correct — but the lack of variety makes the quest book feel mechanical. Human authors naturally vary sentence structure, reward amounts, quest shapes, and description tone across a chapter. AI needs explicit instruction to do so.

**Consequence:** The quest book loses its pedagogical effectiveness. Players skim past descriptions because they all look the same. The reward economy becomes predictable (every quest = 10 XP), eliminating the surprise and delight of unexpected reward moments. The shape/size vocabulary — which should carry semantic meaning (MP20 Shape-as-Tier Signal) — becomes monotonous, making it impossible to visually distinguish quest types at a glance.

**Fix:** (1) Vary description structure: alternate between "how-to" descriptions (explaining crafting), "lore" descriptions (explaining the item's role in the mod's world), "tip" descriptions (sharing an automation hint or efficiency trick), and "challenge" descriptions (posing a question or goal). (2) Vary reward amounts using a tier system: routine quests = 5–10 XP, milestone quests = 25–50 XP, capstone quests = 50+ XP or XP levels. (3) Vary quest shapes within the chapter's shape vocabulary — not every quest should be the default `circle`. (4) After generating a batch, audit for repetition: if more than 60% of descriptions start with the same phrase, or if more than 80% of rewards are identical in structure, regenerate the most repetitive entries.

**Detection heuristic (for progression-rules):** Flag chapters where the standard deviation of description length is below 10 characters (all descriptions are the same length), or where more than 70% of quests share the exact same reward structure (same types, same count ranges).

---

### AP11 — Batch Narrative Inconsistency (cross-quest contradictions within a chapter)

**Symptom:** Quest 12 in a chapter says "you'll need this Osmium Ingot for the Enrichment Chamber in the next quest" — but Quest 13 (the "next quest") doesn't require an Osmium Ingot, it requires a Redstone Crystal. Or Quest 5 says "this is the hardest challenge in the chapter" but Quest 20 (generated later in the same batch) is demonstrably harder. Or Quest 8's description uses a casual, humorous tone while Quest 9's description (for a closely related mechanic) is dry and technical.

**Root cause:** When generating quests sequentially in a batch, each quest is generated with limited context of the previously generated quests. The AI's context window may not include the full text of all prior quests in the chapter, leading to contradictions in narrative promises, difficulty claims, and tonal consistency. This is especially likely when quests are generated in non-dependency order (e.g., generating all quests for a chapter alphabetically by mod feature, rather than in dependency sequence).

**Consequence:** The chapter feels disjointed — like it was written by multiple authors who didn't communicate. Forward references ("you'll need this for later") point to quests that don't actually use the item. Difficulty claims contradict each other. The tonal whiplash between adjacent quests breaks immersion. For narrative packs, this can confuse the player about the story progression.

**Fix:** (1) Generate quests in dependency order (root → leaves), so each quest has the full context of its ancestors. (2) After batch generation, perform a "narrative consistency" audit: for each quest that references "the next quest" or "you'll need this later," verify that the referenced quest actually exists and matches the description. (3) Establish a chapter-level tone guide (casual / technical / lore-heavy) in Step 2 and pass it as context to every quest generation call in the batch. (4) For difficulty claims, track the actual task complexity of generated quests and ensure claims like "hardest" or "easiest" match the data.

**Detection heuristic (for progression-rules):** For each quest description containing forward references (phrases like "next quest," "you'll need this," "later in this chapter"), extract the referenced item or quest and verify it matches a dependent quest's task. Flag mismatches as WARNING.

---

## AP12 — Task-Item NBT Insensitivity (the Permissive Gate)

**Symptom:** A quest task accepts an item regardless of its NBT data — meaning the player can complete the quest with a superficially similar but functionally different item. The quest asks for a "fluid cell containing refined obsidian" but accepts any fluid cell, even an empty one. The player "completes" the quest without actually doing what was intended.

**Root cause:** FTB Quests' item task system checks item identity (registry ID) but does not always validate NBT data by default. When a quest author creates an item task for an NBT-bearing item (fluid cells, enchanted books, configured machines, spawn eggs), the task may match the base item ID without checking the NBT tag that distinguishes the specific variant. In FTB Quests config terms, the task's `item` field matches on `id` but `nbt` comparison may not be configured or may be misconfigured.

**Consequence:** The player receives false completion signals — the quest appears done but the player hasn't actually obtained the intended fluid, enchantment, or machine configuration. This undermines the quest book's role as a progression guide: the player thinks they've mastered a mechanic when they've only held the container. For fluid tasks specifically, the player may never realize they needed a specific fluid because the quest accepted any fluid cell from their inventory.

**Fix:** (1) For fluid tasks, verify that the task configuration includes NBT matching or uses the `fluid` task type (which checks fluid identity directly) instead of an `item` task for a fluid container. (2) For items with meaningful NBT (enchanted books, configured machines, spawn eggs), test the task with variant items to ensure only the correct variant completes it. (3) If NBT matching is too fragile across mod versions, consider using a `checkmark` task with a description explaining the NBT requirement, paired with a reward that requires the actual configured item.

**Real case:**

From Create: Astral issue #566 (2024): "Fluid cell quests complete with any type of fluid cell instead of being NBT sensitive." A player reported that holding any fluid cell in inventory — regardless of what fluid it contained — would complete quests that asked for specific fluid-filled cells. The quests were designed to teach the player about fluid processing, but the NBT-insensitive task matching meant the player could skip the entire fluid mechanic and still pass.

**Source:** [Laskyyy/Create-Astral #566](https://github.com/Laskyyy/Create-Astral/issues/566)

**Cycle 3 validation:** Craftoria #666 — "PNC:R Empty PCB Quest doesn't function" — a player reports that having an empty PCB in their inventory doesn't complete the quest. The player suspects it's NBT-related, having tried both the pressure chamber recipe and the blast furnace recipe. This is the same NBT-insensitivity pattern as Create: Astral #566, now confirmed in a second pack. The PNC:R mod produces PCB items with NBT data that the quest task doesn't properly match, creating a false-negative completion failure (the opposite of Create: Astral's false-positive).

**Source (Cycle 3):** [TeamAOF/Craftoria #666](https://github.com/TeamAOF/Craftoria/issues/666)

---

## AP13 — Premature Item Submission (quest state corruption)

**Symptom:** The player obtains the items for a quest's task before the quest is formally unlocked (because the items are obtainable through normal gameplay before the quest chain reaches them). When the quest finally unlocks, the items have already been consumed or the quest state is corrupted — tasks show "100%" but aren't checked, rewards can't be claimed, and the quest is stuck in a broken intermediate state.

**Root cause:** The quest system allows items to be submitted to a quest's task tracker even when the quest is locked or its dependencies aren't met. This can happen when: (1) the player crafts or picks up an item that matches a locked quest's task, and the quest system auto-detects and "submits" it; (2) the player manually submits items to a quest before completing its prerequisites; (3) a mod update changes the quest's unlock conditions after items have already been submitted. The quest's internal state becomes inconsistent — the task progress shows completion, but the quest doesn't trigger its reward because the unlock conditions weren't satisfied at submission time.

**Consequence:** The player is stuck with a broken quest that appears complete but won't grant rewards or unlock dependent quests. This is particularly frustrating because the player followed the game's mechanics correctly — they obtained the required items — but the quest system's state machine didn't handle the out-of-order submission gracefully. The player has no obvious fix: they can't re-submit the items (they're consumed), can't claim the reward (quest not "officially" complete), and can't progress past this quest.

**Fix:** (1) Design quest task items to be unobtainable before the quest unlocks — gate the item behind the quest's prerequisite chain, or use custom items that only exist after the quest is unlocked. (2) If the item is naturally obtainable before the quest, ensure the quest system handles pre-submission correctly (test by obtaining the item before unlocking the quest). (3) For energy/fluid tasks that accumulate over time, ensure the task only starts tracking after the quest unlocks — not from the moment the block is placed. (4) Provide a recovery mechanism: a repeatable quest, a command reward, or an admin command that can reset a broken quest state.

**Real case:**

From FTB StoneBlock 4 issue #11285 (2025): A player working on the Tier 6 quests submitted the tasks for an energy cell quest before the quest was formally unlocked (while waiting for source jars to produce enough essence). The quest then showed a grey checkmark with tasks displaying "100%" but not individually checked, and the reward could not be claimed. The quest was stuck in a broken intermediate state — neither completable nor resettable by the player.

**Related patterns:** This is distinct from AP3 (Unfinishable Chapter) because the quest IS reachable and completable in theory — it's the submission timing that corrupts it. It's also related to R14 (Teach-Then-Do Ordering) because the root cause is often a quest whose task items become available before the teaching quest chain reaches them.

**Source:** [FTBTeam/FTB-Modpack-Issues #11285](https://github.com/FTBTeam/FTB-Modpack-Issues/issues/11285)

---

## System Safety & Compatibility Anti-Patterns (AP14–AP16)

The following anti-patterns address systemic risks that arise from the interaction between FTB Quests' mechanism design, AI-generated content, and modpack lifecycle management. Unlike AP1–AP13 which focus on per-quest design errors, AP14–AP16 concern architectural and operational risks that affect the quest system as a whole.

### AP14 — Custom Task Black Box (the unverifiable quest)

**Symptom:** A quest uses a `custom` task type (registered by KubeJS or another mod), and the quest system cannot verify whether the completion condition is achievable, fair, or even exists. The quest appears in the book, the player sees it, but neither the player nor any validation tool can determine what they actually need to do to complete it.

**Root cause:** `CustomTask` (`custom` type in FTB Quests source) delegates the completion logic entirely to external code. FTB Quests itself has no visibility into what the custom task checks — it only knows "completed" or "not completed." When AI generates a quest with a custom task, the AI cannot verify that the custom task's completion condition is actually implementable in the pack's mod set, because the condition is defined in external KubeJS scripts or mod code that the AI doesn't have access to.

**Consequence:** The quest becomes a black box — the player sees a requirement they can't understand from the quest UI alone, and must read external documentation or source code to figure out what to do. For AI-generated configs, this is worse: the AI may generate a custom task with a plausible-sounding type name that doesn't correspond to any registered custom task handler, resulting in a quest that is permanently uncompletable. The quest system won't error — it just silently never completes.

**Fix:** (1) AI should **never proactively create custom tasks** — only use them when the pack author explicitly requests and provides the custom task handler's type ID and completion criteria. (2) When a custom task is used, the quest description must explicitly state what the player needs to do (since the quest UI won't show it). (3) R6 (Unreachable Quest Detection) and R20 (Chapter Completion Testability) should downgrade to INFO for quests containing custom tasks — their completability cannot be statically verified. (4) Custom rewards have the same black-box problem — prefer standard reward types whenever possible.

**Related patterns:** This is the quest-system equivalent of AP9 (Hallucination Cascade) — AI generates something that looks right but is actually unverifiable. R28 (Command Reward Safety Scan) partially addresses the reward-side variant.

**Source:** Review B (Completeness Audit) — FTB Quests source code analysis: `CustomTask.java` + `CustomTaskClient.java` allow arbitrary completion logic with no built-in validation.

---

### AP15 — Command Reward Side Effect (idempotency, timing, and permission hazards)

**Symptom:** A command reward produces unintended side effects when executed: items are duplicated on re-claim, effects fail when the player is offline, teleportation sends the player to the wrong dimension, or a destructive command (`/fill`, `/setblock`) overwrites player builds. In the worst case, a command reward crashes the server or grants operator-level permissions.

**Root cause:** Command rewards (`command` type) execute server-side commands with full server permissions when a quest is claimed. MP29 documents basic safety rules (no `/op`, use `{p}` placeholder), but several failure modes remain unaddressed:

1. **Idempotency:** If a quest is unclaimed and re-claimed (admin operation, bug, or player mistake), the command executes again. `/give` duplicates items; `/gamestage add` is usually idempotent but not guaranteed; `/tp` re-teleports the player unexpectedly.

2. **Offline execution:** FTB Quests supports auto-claiming offline rewards. Commands like `/effect give`, `/tp`, or `/playsound` may fail or behave unexpectedly when the player is not online. `/tp` on an offline player could teleport them to spawn on next login.

3. **Claim-all storm:** When a player uses the "claim all" button, all pending command rewards execute in rapid succession. If 50 quests each have a command reward, 50 commands execute in one tick — potentially causing TPS drops, command block rate limiting, or unexpected interactions between commands.

4. **Destructive commands:** Commands like `/fill`, `/setblock`, `/clear`, `/kill` can modify the world or player inventory in irreversible ways. A `/fill` command near the player's coordinates could overwrite their build; `/clear` without arguments wipes the entire inventory.

5. **Cross-dimension commands:** Commands involving coordinates (`/tp`, `/setblock`) need explicit dimension specification — without it, they execute in the player's current dimension, which may not be the intended one.

**Consequence:** At minimum, the player receives duplicated items or confusing teleportation. At worst, a command reward corrupts world state, crashes the server, or causes data loss. The severity scales with the command's destructiveness and the server's command-rate-limiting configuration.

**Fix:** (1) Prefer standard reward types over command rewards whenever possible — use `item` rewards instead of `/give`, `xp` rewards instead of `/xp`, `stage` rewards instead of `/gamestage add`. (2) When command rewards are necessary, ensure idempotency: use `/gamestage add` (idempotent) instead of `/give` (non-idempotent). (3) Never use destructive commands (`/fill`, `/setblock`, `/clear`, `/kill`) as quest rewards. (4) Specify target dimension explicitly for coordinate-based commands. (5) Test command rewards with offline players and claim-all scenarios. (6) R28 (Command Reward Safety Scan) provides static analysis to flag high-risk command patterns.

**Related patterns:** MP29 (Command Reward) covers basic usage; this anti-pattern addresses the failure modes MP29's safety rules don't cover. R28 (Command Reward Safety Scan) is the detection rule.

**Source:** Review B (Completeness Audit) — analysis of command reward execution semantics in FTB Quests source code.

---

### AP16 — Quest State Migration (modpack update compatibility)

**Symptom:** After a modpack update adds, modifies, or removes quests, existing players' quest book state becomes inconsistent: new quests that depend on already-completed quests may auto-unlock prematurely, modified quest tasks show stale completion status, deleted quests leave dangling dependency references, and removed mod items cause cascading quest failures.

**Root cause:** FTB Quests tracks player progress by quest ID. When a modpack is updated, the quest configuration changes but existing players retain their saved progress. The mismatch between old progress and new configuration creates several failure modes:

1. **Quest addition:** New quests whose dependencies are already satisfied by the player's existing progress auto-unlock immediately — which may bypass intended gating if the new quest was meant to be gated behind other new content.

2. **Quest modification:** Changing a quest's task (e.g., swapping the required item) after a player has already completed it leaves the quest in a "completed but task doesn't match" state. FTB Quests typically does not retroactively un-complete quests, but the task data may show inconsistency.

3. **Quest deletion:** Deleting a quest removes it from the configuration but not from the player's saved progress. Other quests whose `dependencies` reference the deleted quest's ID may behave unpredictably — FTB Quests may ignore the missing dependency (effectively removing the gate) or report an error.

4. **Mod removal cascade:** Removing a mod invalidates all item/block/entity references in quest tasks and rewards. Every quest referencing that mod's content becomes broken simultaneously, potentially affecting dozens of quests across multiple chapters.

5. **Item ID migration:** Mod updates sometimes rename items (`mod:item_v1` → `mod:item_v2`) or change recipes. Quest tasks and rewards referencing old IDs become invalid, and descriptions referencing old mechanics become AP1 (Description-Reality Mismatch) instances.

**Consequence:** Players who update an in-progress modpack encounter a degraded quest experience: some quests are broken, some are trivially bypassed, some show confusing error states. The quest book's role as a progression guide collapses because the player can't trust which quests are valid and which are artifacts of the update.

**Fix:** (1) Maintain quest ID stability — never change a quest's ID once published. If a quest must be replaced, create a new quest with a new ID and mark the old one `optional: true` with a description noting it's deprecated. (2) When adding new quests, ensure their dependency chains include at least one new or uncompleted quest to prevent auto-unlock bypass. (3) When removing quests, update all `dependencies` references to the removed quest ID across the entire book. (4) When removing mods, audit all quest tasks/rewards referencing that mod and either replace them or remove the affected quests. (5) R22 (Cross-Chapter Dependency Validity) partially detects dangling references; for update scenarios, extend R22 to check for "stale" references (quest IDs that existed in a previous config version but no longer exist). (6) In `--adopt` mode, SKILL.md should preserve existing quest IDs whenever possible and flag any ID changes for manual review.

**Related patterns:** AP16 is the lifecycle variant of AP3 (Unfinishable Chapter) — instead of a chapter being unfinishable from the start, it becomes unfinishable after an update. R22 detects dangling references at generation time; AP16 addresses them at update time.

**Source:** Review B (Completeness Audit) — analysis of modpack update scenarios and quest state migration challenges.

---

## Reward Economy & Progression Pacing Anti-Patterns (AP17–AP18)

These anti-patterns address systemic reward design failures that emerge from the interaction between FTB Quests' reward mechanics and pack-level economy planning. Unlike AP6 (Dead-End Reward) which concerns individual reward quality, AP17–AP18 concern the aggregate reward economy across chapters and the pack as a whole.

### AP17 — XP-Level Reward Relativity (inconsistent reward value)

**Symptom:** Quests that reward XP levels (`xp_levels`) instead of raw XP (`xp`) create wildly inconsistent reward values depending on when the player claims them. A "+3 XP Levels" reward can be worth 27 XP (at low level) or thousands of XP (at high level). Players learn to hoard unclaimed quest rewards and batch-claim them at high levels to maximize value, which breaks the intended reward pacing.

**Root cause:** Minecraft's XP curve is exponential — the XP required for each level increases as the player's level rises. A fixed XP-level reward therefore delivers a variable amount of actual experience points depending on the player's current level. In FTB Quests config terms, the `xp_levels` reward type gives a fixed number of levels, not a fixed amount of experience. This creates a perverse incentive: the longer the player delays claiming, the more total XP they extract from the reward.

**Consequence:** The reward economy becomes exploitable rather than paced. Players who understand the mechanic hoard quest completions; players who don't are penalized for claiming early. The pack's intended reward curve — where early quests give small rewards and late quests give large ones — is inverted because early-game `xp_levels` rewards (claimed at low level) give trivially small amounts while late-game batch claims give enormous amounts. This undermines the reward pacing philosophy that AP8 (Reward Inflation) tries to prevent.

**Fix:** (1) Use raw XP rewards (`xp` type with a fixed point value) instead of XP levels (`xp_levels`) for routine quests. Raw XP is constant regardless of when it's claimed. (2) Reserve `xp_levels` for milestone/capstone quests where the variable value is an intentional design choice (e.g., "the endgame ATM Star quest gives 50 XP levels as a completion bonus"). (3) If `xp_levels` must be used on routine quests, pair it with `exclude_from_claim_all: true` to prevent batch-claiming exploitation. (4) Plan the XP economy at the book level: define the total XP budget and ensure the cumulative XP from all quests stays within the intended progression curve.

**Real case (Craftoria #289):** A player documented that dozens of quests across multiple chapters use `xp_levels` rewards, creating an exploitable system. The affected quests include all eleven "Gadgets against Grind" quests in the Gadgets chapter, the Completionist chapter's Artifacts/Relics quest, the Mekanism Thermal Evaporation Plant quest, and multiple AE2 chapter quests (Mysterious Cube, storage components, Crafting Co-processor, Network Tool, ME Controller, Toggle Bus, and processor quests). The player explicitly noted that "+3 XP Levels" can range from "as low as 27 [XP] or upwards of many thousands, solely based on the player's experience level." The player even provided the GitHub code search query (`repo:TeamAOF/Craftoria xp_levels`) to locate all affected quests.

**Generalizability note:** 虽然目前仅 Craftoria #289 明确记录了此问题，但 AP17 的根因是 Minecraft 原版的指数级 XP 曲线——这是游戏机制层面的通用问题，不限于特定包类型。任何使用 `xp_levels` reward 的包（包括 kitchen-sink、expert、skyblock）都存在此风险。Craftoria 恰好是第一个有玩家在 issue tracker 上系统性记录此问题的包，而非唯一受影响的包。

**Related patterns:** This is the reward-economy variant of AP8 (Reward Inflation). AP8 concerns giving too much too early; AP17 concerns giving an unpredictable amount at any time. MP16 (XP Drip) is the correct alternative — consistent small XP rewards that scale predictably.

**Source:** [TeamAOF/Craftoria #289](https://github.com/TeamAOF/Craftoria/issues/289)

---

### AP18 — Reward Desert in Long Chains (progression without payoff)

**Symptom:** The player progresses through multiple tiers or stages of a mod's progression chain without receiving any relevant quest rewards. After building three tiers of reactors, the player has accumulated no reward items, no XP, and no materials that help with the next tier. The quest book becomes a pure checklist with no incentive beyond "unlock the next quest."

**Root cause:** The quest chain was designed as a pure gating structure (each quest gates the next) without interleaving rewards between the gates. In FTB Quests config terms, intermediate quests in a long chain have empty `rewards` arrays or rewards that are irrelevant to the chain's progression. The author focused on the dependency topology (MP6 Linear Chain) but neglected the reward bridging (MP14–MP18).

**Consequence:** Players lose motivation mid-chain. The quest book's role as a progression guide fails because there's no positive reinforcement pulling the player forward — only the negative incentive of "you can't advance without this." In expert packs with deep chains (depth 8–15), a reward desert spanning 3+ quests creates a noticeable motivation gap. Players start skipping the quest book and progressing through the mod directly, which defeats the purpose of having quests.

**Fix:** (1) Ensure every 2–3 quests in a chain has at least one relevant reward — a material bridge (MP14), a tool reward (MP15), or XP (MP16). (2) After a tier transition (the player builds the next tier of machine), reward them with a material or efficiency upgrade that helps them use the new tier. (3) For long linear chains (>5 quests without branching), place a milestone reward at the midpoint. (4) Test by playing through the chain and noting how many quests pass without a meaningful reward — if the gap exceeds 3 quests, add intermediate rewards.

**Real case (Craftoria #231):** "Powah is sometimes a big task and you can go through 3 tiers of reactors with no relevant quest rewards which is inconsistent with a lot of the other progression of the pack." The player explicitly identifies the reward desert as an inconsistency — other mod chapters in Craftoria DO provide regular rewards, but the Powah chapter doesn't. The player also notes this makes the mod "less accessible to learn" because without rewards that guide the next step, the player has no signal about what to do next.

**Generalizability note:** Reward desert 是长 chain 设计的通用风险，不限于 Craftoria。任何使用 deep linear chain（depth 5+）的包——尤其是 expert pack（Monifactory depth 8-15）和 skyblock tutorial（ATM9-Sky depth 18）——都面临此问题。Craftoria #231 是目前唯一明确记录此问题的公开 issue，但 cesspit.net 的 expert-pack 分析中"you have to work hard to get to a milestone"的 reward pacing 原则暗示了 reward desert 是其反面——一个被广泛认知但少有 issue tracker 记录的设计失败模式。

**Related patterns:** This is the complement of AP8 (Reward Inflation) — AP8 gives too much too early; AP18 gives too little for too long. Both disrupt the reward economy. MP14 (Material Bridge) and MP16 (XP Drip) are the correct patterns to prevent reward deserts.

**Source:** [TeamAOF/Craftoria #231](https://github.com/TeamAOF/Craftoria/issues/231)

---

## Sources

1. **FTBTeam/FTB-Modpack-Issues #6447** — "List of Observations in FTB Evolution (WIP)." A player's exhaustive audit of quest design problems in FTB Evolution, including description mismatches, circular dependencies, gating errors, and missing content. https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447

2. **cesspit.net** — "Minecraft Is Not What You Think, or: How I Learned to Stop Worrying and Love the Expert Pack." In-depth analysis of expert-pack progression design, quest book quality, reward pacing, and what makes a good modpack experience. https://cesspit.net/drupal/node/2832/

3. **Reddit r/feedthebeast** — "It's 2025. Is a balanced, semi-gated pack with quests too much to ask?" Discussion about quest-gated progression expectations in modern modpacks. https://www.reddit.com/r/feedthebeast/comments/1ie08cv/

4. **Reddit r/feedthebeast** — "What makes a good modpack?" Community discussion about modpack quality factors including quest design. https://www.reddit.com/r/feedthebeast/comments/14afl7m/

5. **Reddit r/feedthebeast** — "Recommendation re: any modern modpacks that truly rework and balance like Terraria/ROTN." Discussion comparing quest-gated progression quality across packs. https://www.reddit.com/r/feedthebeast/comments/1gfhzjw/

6. **MC百科 (mcmod.cn)** — "论较高难度、较长寿命整合包的设计与开发" (On designing high-difficulty, long-lived modpacks). Chinese community tutorial on expert-pack design philosophy. https://www.mcmod.cn/post/4382.html

7. **Phase 1 micro-patterns** — Quantitative data from 11 shipped modpacks (4,601+ quests in ATM-10, 2,295 in Create: Delight, 395 in Mechanomania). See `micro-patterns.md` for the full dataset.

8. **FTBTeam/FTB-Modpack-Issues (2025–2026 stream)** — Ongoing issue tracker for FTB official packs (Architect's Exodus, StoneBlock 4, Skies 2). Rich source of AP1, AP2, AP6 cases across multiple packs. Key issues: #12549 (Botania quest text/task), #12571 (wrong boss name), #12458 (Souls vs Demonic Will), #12459 (wrong spell acceptance), #12426 (wrong pickaxe), #12463 (over-restrictive task), #12469 (unenchantable seashelf), #11432 (wrong steel dust), #11285 (premature submission), #9084 (Beebee deadlock), #12576 (structure too rare), #12474 (uncompletable Block Wands quest). https://github.com/FTBTeam/FTB-Modpack-Issues

9. **Laskyyy/Create-Astral issues (2024–2025)** — Issue tracker for Create: Astral modpack. Source of AP1 cases (#613 Asurine/Zinc mismatch, #618 prismarine/veridium mismatch) and AP12 case (#566 NBT-insensitive fluid cell tasks). Also contains dependency ordering bug (#689 Hephestus parts). https://github.com/Laskyyy/Create-Astral/issues

10. **Omicron-Industries/Monifactory (2024–2026)** — Issue tracker for Monifactory (GregTech CEu Modern expert pack, MC 1.20.1). Source of AP1 variant (#1545 Yeta Wrench quest description omission), AP5 case (#2359 tutorialisation debt in basic mechanics), and AP1 typo (#2546 Ammonia quest). Key insight: expert pack with very few quest design complaints overall, suggesting deep chains + invisible infrastructure (MP23) can coexist with quality quest design when tutorialisation is adequate. https://github.com/Omicron-Industries/Monifactory/issues

11. **TeamAOF/Craftoria (2024–2026)** — Issue tracker for Craftoria (MC 1.21.1, NeoForge kitchen-sink). Source of AP4 cases (#231 Powah gating, #607 Iron's Spells gating, #352 optional-but-mandatory), AP12 case (#666 PNC:R PCB NBT), AP17 case (#289 xp_levels reward relativity), and AP18 case (#231 reward desert). Richest new data source for reward economy and gating issues. https://github.com/TeamAOF/Craftoria/issues

12. **EnigmaticaModpacks/Enigmatica10 (2025–2026)** — Issue tracker for Enigmatica 10 (MC 1.21.1, NeoForge expert pack). Notable for having ZERO quest design complaints among ~20 recent issues (mostly Bug and Suggestion labels). This negative evidence — a high-profile expert pack with no quest-related issues — suggests the Enigmatica team's quest QA process is effective. https://github.com/EnigmaticaModpacks/Enigmatica10/issues
