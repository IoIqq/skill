# mod-reward-design

> **Core question:** 奖励什么？它引导玩家去哪？
> **Lines:** ~290 | **Step 2 load:** partial | **Step 4 load:** yes | **Step 5 load:** yes

## Quick Reference

| ID | Title | Phase | Severity | Pack types |
|---|---|---|---|---|
| MP14 | Material Bridge | Step 4 | -- | all |
| MP15 | Tool Reward | Step 4 | -- | all |
| MP16 | XP Drip | Step 4 | -- | kitchen-sink |
| MP17 | Hub Concentration | Step 2 | -- | create, kitchen-sink |
| MP18 | Choice Reward | Step 4 | -- | expert, story |
| MP29 | Command Reward | Step 4 | -- | expert, story, kitchen-sink (legacy MC ≤1.16.5) |
| MP34 | Loot Table Reward | Step 4 | -- | all |
| AP6 | Dead-End Reward | Step 2/4 | High | all |
| AP8 | Reward Inflation | Step 2 | High (expert) / Medium (kitchen-sink, debated) |
| MP38 | Reward Perception Split | Step 2 | -- | kitchen-sink |
| MP39 | Alternative-Reward Progression | Step 2 | -- | expert, collection |
| AP17 | XP-Level Reward Relativity | Step 2/4 | Medium | all |
| AP18 | Reward Desert in Long Chains | Step 2/4 | Medium | all |
| R10 | Reward-to-Dependent Bridge | Step 4/5 | P1 | all |
| R11 | Reward-Target Accuracy | Step 5 | P1 | all |
| R12 | Reward Value Progression | Step 5 | P2 | all |
| R13 | Capstone Reward Magnitude | Step 5 | P2 | all |
| R28 | Command Reward Safety Scan | Step 4 | P0 | all |
| R31 | XP-Level Reward Relativity | Step 4 | P2 | all |
| R33 | Reward Table Reference Integrity | Step 4 | P1 (generator invariant) | all |
| R34 | Reward Type Distribution Report | Step 5 | P2 (INFO/WARNING) | all |
| R37 | Capstone-Only Progression Break | Step 5 | P2 (INFO/WARNING) | kitchen-sink, expert |
| R38 | Tier Transition Milestone Reward | Step 5 | P2 (WARNING) | expert, kitchen-sink |
| R44 | Reward-Stage Matching | S4/S5 | ERROR/WARNING | all |
| R45 | Reward Guidance Bridging | S4/S5 | WARNING | all |
| R46 | Questbook Role Declaration | S2/S5 | P2 (INFO) | all |
| R50 | Zero-Reward Design Safety Conditions | S2/S5 | P2 (INFO) | expert, collection |
| PP2 | Backward Shortcut | Step 2 | -- | all |
| PP6 | Wrong Tool Reward | Step 4 | -- | all |

---

## Patterns

### MP14 — Material Bridge

Reward IS the next quest's ingredient. Quest N rewards an item; Quest N+1 (depends_on N) requires that item as a task. Reward count matches or slightly exceeds the next quest's requirement. The most natural bridging pattern — appears across all pack genres.

In kitchen-sinks the bridge is often a mod's signature intermediate (e.g. Mekanism osmium ingot). In expert packs the bridge is tighter: reward count exactly matches the next recipe's input count, no waste. ATM-10 AE2 chapter: Quest 1 rewards 10 XP; Quest 2 (charger + inscriber) rewards 3 iron + 50 XP; Quest 3 (meteorite compass) rewards 4 sky_stone + 100 XP — each reward facilitates the next step.

**Source:** ATM-10 `applied_energistics_2.snbt`.

### MP15 — Tool Reward

Reward unlocks the next activity. The reward is a durable tool (pickaxe, wrench, guide book, machine block), not a consumable. Next quest's task requires using that tool. Count is typically 1. Common at section boundaries — "here's your new tool, now go use it."

Create: Delight Feast_Afoot: tutorial quests reward hygrometer, watering can, cooking pot — each immediately precedes a quest requiring that tool. ATM-10 AllTheModium root rewards the Patchouli guide book (reference for all subsequent recipes).

### MP16 — XP Drip

Small XP on every quest as baseline; milestone quests give larger XP or XP-level rewards. The XP is not enough to "buy" progression but enough to feel steady advancement.

> **ATM Signature:** ATM-10 uses 10/50/100 XP tiers extensively (6,915 rewards / 4,601 quests = 1.5/quest). Expert packs (Monifactory) and Create packs (0.43 and 0.11 rewards/quest) do not center their reward economy on XP drip. For ATM-specific implementation data, see `mod-atm-signature`.

**Universal concept:** A small consistent reward alongside primary item rewards prevents "reward desert" feelings in long chains. Even non-XP-drip packs benefit from a baseline reward on every quest — the type (XP, material, currency) varies by genre.

### MP17 — Hub Concentration

Sparse cells, rich hubs. Cell quests (majority) have no rewards or minimal single-item rewards. Hub quests (minority) have rich rewards: multiple items, XP, random loot, or choice rewards. Hub depends_on ALL its cells.

Prevents reward inflation in large catalogs. Create: Delight Mouse_Chef: 304 cells have item×29 + xp×52 (sparse); 12 category hubs carry the most valuable rewards. Ratio: ~1 reward per 4 cells.

### MP18 — Choice Reward

Branch-point fork — reward IS the choice. Quest with a `choice` reward (or multiple `item` rewards with autoclaim disabled). Description explains options. After the choice, selected item becomes the task for the chosen path's first quest.

Rare in kitchen-sinks ("do everything" philosophy). Appears in expert and RPG packs. Create: Delight uses 13 `choice` rewards across 2,295 quests at key branching points.

### MP29 — Command Reward

Server-side invisible logic. `command` reward with `command: "/<command>"` and `player: "{p}"`. Runs server-side when quest is claimed. Common commands: `/gamestage add {p} <stage>`, `/effect give`, `/tp`, `/give`.

**Safety rules (basics):** (1) Never use `/op`, `/gamemode creative`. (2) Test every command in single-player first. (3) Prefer standard reward types — use `item` instead of `/give`, `xp` instead of `/xp`. (4) Verify gamestage names against config — typos create silent failures. Full safety scan defined in R28 below.

Monifactory's `dependency_chain` chapter uses 26 gamestage tasks + 26 command rewards as dedicated routing. E9E: 56 command rewards in `chapter_one` alone (83% of reward sections). Visible quest book stays clean; invisible logic runs through command rewards.

**Enigmatica command reward lineage (Cycle 6 Phase 3):**

Command rewards have a documented 3-generation evolution across the Enigmatica series:

| Generation | Pack | MC | Command rewards | Primary use | Pattern |
|---|---|---|---|---|---|
| Gen 1 | E6 | 1.16.5 | 455 | Loot table delivery | `/execute at @p run loot spawn ~ ~1 ~ loot enigmatica:chests/quest_*` |
| Gen 2 | E9E | 1.19.2 | 56 (ch1) | Gamestage routing | `/gamestage add {p} <stage>` |
| Gen 3 | E10 | 1.21 | 0 | (native loot tables) | `type: "loot"` with 28 reward_tables |

**Gen 1 detail (E6):** ALL 455 command rewards follow the pattern `/execute at @p run loot spawn ~ ~1 ~ loot enigmatica:chests/quest_*` with `player_command: false`. This is **vanilla loot table delivery disguised as command rewards** — the pack authors created custom vanilla loot tables (tiered as `quest_*_loot_rare`, `quest_*_loot_epic`, `quest_*_loot_legendary`) plus cross-chapter "delight" tables (`quest_scavengers_delight`, `quest_farmers_delight`, `quest_alchemists_delight`). Botania chapter alone: 94 command rewards (22 rare, 12 legendary, 8 epic). Create chapter: 10 command rewards. Getting_started: only 2. **Why:** On MC 1.16.5, FTB Quests lacked native weighted loot pool support. `/loot spawn` was a workaround.

**Deprecation note:** On FTB Quests 26.x (MC 1.21+), `type: "loot"` with native reward tables fully replaces the command-as-loot workaround. **Always prefer `type: "loot"` or `type: "random"` over command rewards for loot delivery on modern versions.** The E6 pattern is only relevant for MC 1.16.5 and earlier.

**GreedyCraft packmode variant:** GreedyCraft uses `command` rewards with `player_command: true` to run `/packmode <mode>` — a pack-mode selector quest that switches the entire quest book between casual/expert/adventure modes. This is a legitimate command reward use that has no standard reward type equivalent.

**Game Stages 作为外部框架 (Phase 2 Cycle 8 补充):** 在专家包中，command reward 最常搭配的外部框架是 Game Stages。KLPBBS 魔改包常用模组汇总确认 Game Stages 在魔改/专家包中被广泛使用，通过 CraftTweaker 集成实现物品（Item Stages）、配方（Recipe Stages）、维度（Dimension Stages）三个层面的进度锁定。FTB Quests 通过 command reward 控制阶段的解锁时机，Game Stages 确保游戏世界执行锁定。Monifactory 的 26 个 gamestage command rewards 路由电压阶段，E9E 的 56 个 command rewards 路由章节进度，形成"完成任务 → 解锁阶段 → 获得能力"的完整闭环。

### MP34 — Loot Table Reward

Randomized reward via FTB Quests internal reward tables. Pack authors define weighted item pools in `config/ftbquests/quests/reward_tables/*.snbt`. Quest rewards reference these tables via `table_id: <long>L`. Three presentation types share the same underlying system:

1. **`type: "random"`** — Auto-rolls the table when quest is claimed. Player receives a random item directly. Used extensively by Craftoria (35–120 random rewards per chapter, up to 92.6% of Create chapter rewards). 19 custom reward tables.

2. **`type: "loot"`** — Presents a loot crate icon to the player. Player opens it to receive a random item. Used extensively by Enigmatica 10 (7–29 loot rewards per chapter, 10–39% of rewards). 28 custom reward tables. Structurally identical to `random` — both use `table_id` referencing `reward_tables/*.snbt` files. The difference is purely in player-facing UI (manual open vs auto-roll).

3. **`type: "choice"`** — Player picks one item from the table's entries. Used by MI:Foundation (2–6 per chapter at milestones) and Craftoria (1–2 per chapter at branch points). Same `table_id` reference. MI:Foundation Botania: 4 choice rewards, all referencing `table_id: 1606690661312817740L`.

**Phase 3 Cycle 4 correction:** Previous description incorrectly stated that `type: "loot"` references "vanilla/mod loot table IDs directly." Deep config analysis confirms all three types use the **same FTB Quests internal reward table system**. E10 has 28 reward tables (not zero as previously reported). The reward table format supports weighted item pools with `count` fields and optional `loot_size` (number of items rolled per claim).

> **Version caveat (审查 A/B 修订):** The unified reward-table claim above is confirmed only on **FTB Quests 26.x (JSON5, MC 1.21.x)**. On MC 1.20.1 (FTB Quests 2001.4.17, SNBT format), `type: "loot"` **may** reference vanilla loot table IDs (e.g. `minecraft:chests/simple_dungeon`) rather than FTB Quests `reward_tables/*.snbt` files. This 1.20.1 SNBT behavior is **unverified** — if generating for a 1.20.1 pack, confirm in-game that `type: "loot"` rewards resolve against the intended source before shipping.

**Reward table format (Craftoria example):**
```
{
    id: "0414572B7C36F04F"
    loot_size: 1
    rewards: [
        { count: 16, item: { count: 1, id: "powah:capacitor_basic_tiny" } }
        { count: 64, item: { count: 1, id: "powah:dielectric_paste" } }
        { count: 2, item: { count: 1, id: "powah:energizing_rod_hardened" } }
    ]
}
```
The `count` field on each reward entry is the weight — higher count = more likely to be rolled.

**Reward table format (E10 example):**
```
{
    id: "00540CF744EBCDCA"
    loot_size: 4
    rewards: [
        { count: 8, item: { count: 1, id: "minecraft:cooked_cod" } }
        { count: 4, item: { count: 1, id: "minecraft:golden_carrot" } }
    ]
    use_title: true
}
```
`loot_size: 4` means 4 items rolled per claim. `use_title: true` shows the table's title in the UI.

**Reward table format (AoF3 example — MC 1.16.5 Fabric):**
```
{
    id: "2B7E24C56282D86D"
    order_index: 1
    title: "High"
    loot_size: 16
    hide_tooltip: true
    rewards: [
        { item: "minecraft:diamond_block", weight: 6 }
        { item: "techreborn:iridium_ingot", count: 12, weight: 2 }
        { xp: 1000, type: "xp", weight: 2 }
        { xp_levels: 5, type: "xp_levels", weight: 6 }
        { item: "tacocraft:golden_taco", weight: 15 }
    ]
}
```
AoF3 uses a simpler format: `item: "mod:id"` (string, not nested object) with `weight: N`. `loot_size: 16` rolls 16 items per claim — much larger pools than Craftoria/E10. 16 reward tables with evocative tier names (`low`, `medium`, `high`, `artifacts`, `foodsources`, `foodoringots`, `pristine_matter`, etc.). `hide_tooltip: true` on all tables. Some tables embed XP rewards within item pools (mixed `type: "xp"` and `type: "xp_levels"` entries alongside item entries) — a design not seen in Craftoria or E10.

**Cross-pack reward economy (3-pack deep analysis):**

| Pack | reward_tables | Dominant type | Random rewards/chapter | Item rewards/chapter |
|---|---|---|---|---|
| All-of-Fabric-3 | 16 | `random` (363 total) + `loot` (23) + `choice` (16) | 0-363 (pack-wide) | sparse |
| Craftoria | 19 | `random` (21-92% of rewards) | 0-120 | 4-268 |
| Enigmatica 10 | 28 | `loot` (10-39%) | 0-2 | 9-52 |
| MI:Foundation | 29 | `item` (100%) | 0-1 | 9-393 |
| GregTech-Odyssey | 10+ | `item`+`command`(2)+`choice`(1) | 0 | 82-94/ch (EV: 82, HV: 94) |
| No-Flesh-Within-Chest | 4 | `item` (100%) | 0 | 57-126/ch (boss: 42 lightmanscurrency refs) |
| TheWinterRescue | 2 | `item`+`choice`(1)+`frostedheart:tip`+`frostedheart:insight` | 0 | 35-85/ch + 32 insight rewards (t2) |
| Cabricality | 0 | `item` (100%) | 0 | 27-54/ch (ZERO on many quests) |

**Cycle 5 finding — Custom mod-specific reward types:** TheWinterRescue uses two custom reward types: (1) `frostedheart:tip` (with fields `auto: "invisible"`, `fh_tip: "jei"`) that provides mod-specific JEI hints — an **informational reward**; (2) `frostedheart:insight` (with fields `insight: N`, `team_reward: true`) that grants skill/insight points — a **progression currency reward**. 32 frostedheart:insight rewards in the t2 chapter alone. These are the first custom reward types observed in the dataset. The `auto: "invisible"` and `team_reward: true` fields control auto-claiming and team-sharing behavior respectively. Custom reward types are registered by companion mods and extend the standard type taxonomy (item/xp/xp_levels/command/random/loot/choice). Cross-pack Phase 3 Cycle 5 finding: TWR's insight system is functionally similar to NFwC's lightmanscurrency and GT-O's copper_coin — all three are pack-specific progression currencies implemented as item or custom-type rewards rather than xp.

**Cycle 5 Phase 3 finding — Currency-as-reward formalized (MP36):** Cross-pack comparison of GregTech-Odyssey and NFwC reveals a consistent pattern: both packs use item-type currency rewards (`gtocore:copper_coin`, `lightmanscurrency:coin_iron`/`coin_gold`) as universal exchange bridges. GT-O HV chapter: 0 command rewards, 94 item rewards (including currency). NFwC boss chapter: 42 lightmanscurrency references, 0 optional quests. This pattern is formally documented as MP36 in micro-patterns.md. Key distinction from MP14 (Material Bridge): currency bridges to a shop system, not a specific recipe. Key distinction from MP16 (XP Drip): currency is an item with purchasing power, not abstract experience points.

**Design implications:** All three types require upfront authoring investment (creating reward_tables). The choice between `random`, `loot`, and `choice` is a player-experience decision, not a data architecture decision. Prefer one dominant type per pack for consistency — R34 reports the pack's reward type distribution and flags packs where no single type dominates.

**Complementary to MP14-MP18:** Deterministic bridges (material, tool) ensure the player always has the next step's ingredient; loot tables add variety and excitement on top. A quest can have both. Every tier in the loot table should be useful at the quest's stage. Calibrate worst-case roll to still provide progression value.

`table_id` is a decimal **long** — in the spec, use `table: "<name>"` and let the generator resolve.

**Implementation error variant (E10 #517):** A quest was configured with a `choice` reward where a `random` reward was intended. Player reported: "Chipped quest in Building and Tools tab has choice reward, which is presumably meant to be random reward just like other quests." The pack author (MuteTiefling) confirmed and fixed it to random. This reveals that `random` vs `choice` vs `loot` reward type is an easy authoring mistake — all three present multiple options to the player but with fundamentally different mechanics (system rolls vs player chooses vs loot crate). R12 compliance requires the correct type.

**R33 validates:** Every `table_id` must reference an existing reward table file.

---

### MP38 — Reward Perception Split (kitchen-sink generosity debate)

Kitchen-sink packs with `flexible` progression face a unique reward design tension absent from expert packs. Generous rewards (high-tier items, large XP, rare materials) are simultaneously praised as genre-appropriate sandbox generosity and criticized as progression-breaking inflation. The split correlates with how individual players approach the pack: "structured progression" players feel rewards undermine the journey; "sandbox toolbox" players welcome generous starting resources.

**Design guidance:** (1) Cap early-game quest rewards to materials obtainable within 1-2 hours of normal play. (2) Reserve truly progression-breaking items (dimension-access, endgame tools) for late-game capstones. (3) Use choice rewards (MP18) at branch points so the player controls which path to shortcut. (4) Document the pack's reward philosophy in the quest book introduction.

**Severity is pack-type dependent:** AP8 (Reward Inflation) is unambiguously HIGH severity in expert packs with `linear` progression. In kitchen-sinks with `flexible`, the same behavior is debated — the ATM-10 collaborator defends it as "only giving away ATM Stars would truly ruin progression." This means the reward inflation rule should differentiate severity by pack type.

**Cycle 7 validation source:** [AllTheMods/ATM-10 Discussion #3539](https://github.com/AllTheMods/ATM-10/discussions/3539), [cesspit.net](https://cesspit.net/drupal/node/2832/)

### MP39 — Alternative-Reward Progression (替代奖励进度)

**适用范围：** 此模式的实际验证集中在 expert/hardcore 包，但 Cycle 9 发现零奖励设计也出现在非 expert 包中（Cobblemon, 1307 quests, 非 expert 非 TFG 系列）。替代奖励系统在 kitchen-sink 包中的案例仍未观察到。[Phase 4 Cycle 8 - 审查员A; Phase 1 Cycle 9 补充]

Hardcore and expert packs that avoid direct item rewards to protect progression pacing. The quest book carries the guidance role while an alternative system — currency, gift packages, NPC trading, shops — carries the positive-feedback role. This is not "zero rewards" but rewards routed through a different channel.

Evidence base: TerraFirma Rescue (MC百科 红票36/黑票0, 329,400 访问) uses GT coins + gift packages + NPC trading. GTNH (红票180/黑票4, 997,300 访问) uses the same GT coin + NPC trading ecosystem across 3000+ quests and 15 voltage tiers. RAD2 (红票88/黑票0, 635,800 访问) uses a currency shop with skill upgrades. E2E uses Bragging Rights completion targets as long-term motivation drivers. In each case the quest book handles the teaching and guiding while the alternative reward system handles the satisfying feedback loop.

The failed counter-example is ATM10, where a player (xiaoxiao921) complained that quest rewards included "Dragon Egg / Ender Chests rewards even though we would not be even close to legitimately get one" and "Ultimate Universal Cable being given even though i barely crafted a dozen of basic ones." The pack collaborator (TheBedrockMaster) defended with "It is a kitchen sink pack, the only thing that could actually 'break progression' would be gifting out ATM Stars." This demonstrates that reward generosity is perceived differently depending on pack type — the same items that feel generous in a kitchen-sink feel progression-breaking in an expert pack.

The design advantage of alternative rewards is not "whether to reward" but "how to reward." Currency can be spent on multiple options (unlike a fixed item that may be a dead-end). NPC trading gives the player agency in choosing when and what to exchange. Gift packages add randomness without the risk of giving a specific endgame item too early.

[Phase 2 Cycle 8 - MC百科 群峦：救援 https://www.mcmod.cn/modpack/51.html, GTNH https://www.mcmod.cn/modpack/1.html, RAD2 http://www.mcmod.cn/modpack/419.html, E2E https://www.mcmod.cn/modpack/23.html; ATM-10 GitHub Discussion #3539]

**Phase 2 Cycle 9 — Author testimony for MP41 Zero-Reward (2026-07-10):**

TFG Modern #3656 提供了 MP41 (Zero-Reward Progression) 的首个直接作者证言。包作者 Pyritie 明确声明任务书的两个角色："1) to give direction to people who don't know what to do, and 2) to aid discoverability of things that are otherwise pretty hidden. It's meant to be a companion to the field guide (and emi)." 作者拒绝了 linear checklist 设计（"we don't really want the quest book to become a linear checklist"），将任务书定位为导航工具而非奖励分配器。俄罗斯贡献者 Exzept1on 在评论中补充了哲学维度："Наград не будет, нужно иногда пострадать"（不会有奖励的，你需要有时受苦）。这将 MP41 从一个数据观察模式提升为有明确作者推理的文档化设计哲学：expert pack 的 struggle 本身就是体验的一部分，奖励会削弱这种体验。[Phase 2 Cycle 9 - TFG Modern GitHub #3656]

### Game Stages 作为 Command Reward 的搭档 (外部进度框架)

**适用范围：** Game Stages 集成主要在 expert/hardcore 包中观察到，但 Cycle 9 在非 expert 包中也发现了 gamestage 任务（Skylore skyblock, engineer chapter: `type: "gamestage"` + `auto: "invisible"`）。因此 gamestage 的使用取决于 Game Stages mod 是否在场，而非包难度等级。在已研究的 46 个包中，明确使用 Game Stages 的有 Monifactory（expert）、E9E（expert）、TFG Modern（expert）和 Skylore（skyblock，非 expert）。**但 Phase 2 Cycle 9 补充：** Skylore #101 表明该包 "is put on hold, and isn't finished"（contributor RobertasJ），其 `stage: ""` 空字符串可能是未配置的 placeholder 而非有意设计。"Game Stages 非 expert 专属" 的证据强度应视为 **unconfirmed — likely placeholder**，需要第二个非 expert 包验证。[Phase 4 Cycle 8 - 审查员A; Phase 1 Cycle 9 修正; Phase 2 Cycle 9 弱化]

FTB Quests 本身不包含物品/配方/维度的锁定能力。在专家包中，command reward 通常与 Game Stages 框架搭配使用，实现进度锁定。KLPBBS 魔改包常用模组汇总确认 Game Stages 被广泛搭配 FTB Quests 使用，通过 CraftTweaker 集成实现三层锁定：Item Stages（未解锁阶段的物品拿到也无法使用）、Recipe Stages（未解锁阶段的配方不可见）、Dimension Stages（未解锁阶段的维度不可进入）。FTB Quests 通过 `command` reward（如 `/gamestage add {p} <stage>`）控制阶段的解锁时机——任务书负责"何时解锁"，Game Stages 负责"锁定是否生效"。Monifactory 的 `dependency_chain` chapter 使用 26 个 command rewards 路由电压阶段，E9E 在 `chapter_one` 中使用 56 个 command rewards，形成完整的"完成任务 → 解锁阶段 → 获得能力"闭环。

[Phase 2 Cycle 8 - KLPBBS 魔改整合包常用模组 https://klpbbs.com/thread-130537-1-1.html]

---

## Anti-Patterns

### AP6 — Dead-End Reward

Reward has no connection to anything the player does next. Not a material bridge, not a tool, not XP or currency. It's a trophy sitting in the inventory.

**Root cause:** Reward chosen for thematic reasons ("this quest is about forestry, reward is a sapling") rather than progression reasons ("reward is the charcoal the next quest needs").

**Fix:** For every reward ask: does it help with the NEXT quest? If not, replace with material bridge (MP14), tool reward (MP15), XP (MP16), or choice reward (MP18). Cosmetic rewards only on truly optional quests.

**Variant — Mod-Unification Trap (PP7):** Reward is "steel dust" but from the wrong mod namespace (FTB Materials vs Modern Industrialization). Same display name, incompatible recipes. Cross-ref PP7 in mod-teaching-pacing.

### AP8 — Reward Inflation

Early quests give generous rewards; mid-game "runs out" of meaningful rewards. Player's chest overflows from early quest rewards; late-game quests offer things the player doesn't need.

**Root cause:** Reward curve not planned as a whole-book economy. Each chapter's author chose rewards independently.

**Fix:** Plan reward economy at book level. Define tiers (early/mid/late/endgame). Early: tools + small quantities (1-4 items). Mid: moderate stacks (8-16). Late: rare materials or unique items. Use XP drip (MP16) as universal baseline. Reserve richest rewards for capstones (MP8). Cap per-chapter reward budgets.

### AP17 — XP-Level Reward Relativity

`xp_levels` rewards create wildly inconsistent value depending on player level at claim time. +3 XP Levels can be worth 27 XP (low level) or thousands (high level). Players hoard unclaimed rewards and batch-claim at high levels.

**Root cause:** Minecraft's XP curve is exponential. Fixed level reward = variable actual XP.

**Fix:** Use raw `xp` (fixed point value) for routine quests. Reserve `xp_levels` for milestone/capstone quests only. If `xp_levels` must be used on routine quests, pair with `exclude_from_claim_all: true`.

**Source:** Craftoria #289 — dozens of quests across multiple chapters affected.

### AP18 — Reward Desert in Long Chains

Player progresses through multiple tiers without receiving any relevant rewards. After 3 tiers of reactors: no reward items, no XP, no materials. Quest book becomes a pure checklist with no incentive.

**Root cause:** Chain designed as pure gating without interleaving rewards.

**Fix:** Every 2-3 quests in a chain should have at least one relevant reward (MP14, MP15, or MP16). After a tier transition, reward a material or efficiency upgrade. For chains >5 quests without branching, place a milestone reward at the midpoint.

**Source:** Craftoria #231 — Powah chapter "throws everything at you" with 3 tiers and no rewards between them.

**Cross-tier reward desert (GregTech-Odyssey #1602):** HV tier requires massive material investment (400+ MV motors, 37 multiblock blocks, platline setup) with no rewards bridging the gap from MV. Player explicitly describes the "reward desert" feeling: "even for an expert, being asked to make so many motors at HV is easy to make the player burn out." The issue suggests adding a "degraded pattern distributor" as an intermediate reward to give players a tangible progression benefit before committing to full AE2 automation. AP18 variant at the voltage-tier boundary in expert GregTech packs.

---

## Rules

### R10 — Reward-to-Dependent Bridge

**Step 4 priority:** P1 (reverse check)
**Step 5 priority:** P1 (forward check)

Checks whether quest rewards appear in dependent quests' tasks. For each quest Q with item rewards: does any dependent quest require that reward item as a task? Tolerances: terminal quests (no dependents) skip; XP/loot/choice rewards skip; tool rewards and currency rewards are universal bridges.

> **Currency exception (Cycle 5 review C/B, MP36 interaction):** Currency rewards (e.g. `gtocore:copper_coin`, `lightmanscurrency:coin_iron`) are `type: "item"` — R10's algorithm cannot distinguish them from material bridge items. When a pack has a shop or trading system (MP36 Currency-as-Reward), currency items are spent at shops rather than submitted as quest tasks, so R10 would incorrectly flag them as dead-end rewards. **Exception:** If the reward item ID matches a known currency item (from the pack's currency registry or MP36 detection), skip the R10 dead-end check. Detection heuristic: currency items are typically from `lightmanscurrency`, `gtocore` (coin items), or custom pack-specific currency mods, AND the pack contains a shop/trade chapter or trading system.

```
for each quest Q:
    dependents = find_dependents(Q)
    if not dependents: continue
    for reward in item_rewards(Q):
        if reward_id not in any dependent's tasks:
            if not is_tool/reward/currency/loot:
                INFO: "Reward {reward_id} has no dependent bridge."
```

Step 4 runs reverse check (task -> ancestor reward). Step 5 runs full forward check.

### R11 — Reward-Target Accuracy (Wrong Tool Detection)

**Step 5 priority:** P1

When a quest rewards a tool (wrench, hammer, guide book), checks if it's the tool the dependent quest actually needs. Uses `tool_category_map` to group same-function tools by mod.

```
if reward.item.id in tool_category_map:
    needed_tool = extract_from_dependent_description()
    if needed_tool in same category but different mod:
        WARNING: "Wrong tool variant rewarded."
```

This catches "IE hammer vs Oritech wrench" — the multi-mod kitchen-sink problem where 5 mods each provide their own wrench.

### R12 — Reward Value Progression

**Step 5 priority:** P2

Checks whether reward value increases with quest difficulty (dependency_depth). For each chapter, sorts quests by depth, estimates reward value (rarity x count), flags significant drops (>50% decrease at higher depth).

Soft check (INFO level) because value estimation is imprecise and some quests intentionally give low rewards (acknowledgement gates).

### R13 — Capstone Reward Magnitude

**Step 5 priority:** P2

Capstone quests (dependencies >= 5) should have reward value >= 3x the chapter average. Capstone is the chapter's climax — reward should be memorable.

ATM-10 ATM Star: 50 ATM Star Shards + Patrick Star + 50 XP levels. The richest reward in the entire pack, on the hardest quest.

### R28 — Command Reward Safety Scan

**Step 4 priority:** P0

Static analysis of command reward strings. Three tiers:

**FORBIDDEN (ERROR):** `/op`, `/deop`, `/gamemode creative|spectator`, `/stop`, `/kick`, `/ban`, `/whitelist`

**HIGH-RISK (WARNING):** `/fill`, `/setblock`, `/clone`, `/clear`, `/kill`, high-amplifier effects (>=5), `/summon.*wither`, `/execute`

**IDEMPOTENCY RISK (INFO):** `/give`, `/tp`, `/playsound` — re-claiming duplicates the effect.

Additional checks: (1) Commands affecting a player must use `{p}` placeholder — hardcoded names break multiplayer. (2) Coordinate-based commands (`/tp`, `/setblock`, `/fill`) should specify target dimension explicitly.

This rule runs at Step 4 (per-node) because command strings are local data. FORBIDDEN commands block spec write.

### R31 — XP-Level Reward Relativity

**Step 4 priority:** P2

Checks if `xp_levels` rewards appear only on milestone quests. Non-milestone quests with `xp_levels` trigger WARNING: reward value drifts with player level, creating inconsistent economy.

Milestone detection heuristic: dependents >= 3, OR capstone, OR size > 1.5x chapter median, OR shape in (gear, pentagon, hexagon, diamond).

### R33 — Reward Table Reference Integrity (Generator Invariant)

**Step 4 priority:** P1 (ERROR — generator construction invariant)

> **Reclassification note (审查 C 修订):** Originally classified as a Step 5 post-hoc check. Review C pointed out that at generation time the reward table file does not yet exist — the generator must *create* it. R33 is therefore a **generator construction invariant**: whenever the generator writes a quest reward with `type: "random"`, `"loot"`, or `"choice"`, it must simultaneously emit the corresponding reward table file in `reward_tables/`. A post-hoc Step 5 scan remains useful for catching manually-introduced broken references, but the primary guarantee is at generation time.

**Generation-time contract:** For every quest reward referencing `table: "<name>"`, the generator must:
1. Resolve the table name to a `table_id` (decimal long).
2. Emit a reward table file at `config/ftbquests/quests/reward_tables/<id>.snbt` (or `.json5`) in the same generation pass.
3. Verify the emitted table file is non-empty and well-formed before finalizing.

**Edge cases to guard against (审查 B 补充):**
- **Empty `rewards` array** — a reward table with `rewards: []` produces no items; the generator should not emit such a table, and if encountered in an existing pack, flag as WARNING.
- **All-zero weights** — if every entry in `rewards` has `count: 0`, no item can be rolled; flag as WARNING.
- **`loot_size` <= 0** — zero or negative `loot_size` means no rolls per claim; flag as ERROR if <= 0.

**Step 5 residual check (legacy):** A full-book scan for dangling `table_id` references remains useful for packs edited by hand. The pseudocode from the original R33 applies at Step 5 as a safety net:

```
reward_table_ids = load_all_ids("reward_tables/")
for each quest Q:
    for reward in Q.rewards:
        if reward.type in ("random", "loot", "choice"):
            if reward.table_id not in reward_table_ids:
                ERROR: "table_id {reward.table_id} references non-existent table"
```

**Violations would cause:** Silent reward failure — player claims quest, gets nothing, no error message.

**Source:** Phase 3 Cycle 4 deep config analysis. Craftoria (19 tables), E10 (28 tables), MI:Foundation (29 tables) all use this system. Broken references are easy to introduce when copying quest configs between chapters.

### R34 — Reward Type Distribution Report

**Step 5 priority:** P2 (INFO — distribution report; WARNING only when no dominant type)
**Data dependency:** Full book scan

**What it reports:** Scans all quests across the entire book and computes the distribution of reward types (`item`, `xp`, `xp_levels`, `random`, `loot`, `choice`, `command`). Reports the breakdown to the author. Flags a WARNING when no single reward type exceeds 50% of total rewards, suggesting the pack may lack a coherent reward strategy.

```
type_counts = {}
for each quest Q:
    for reward in Q.rewards:
        if reward.type in ("random", "loot", "choice", "item", "xp"):
            type_counts[reward.type] += 1

total = sum(type_counts)
dominant = max(type_counts, key=type_counts.get)
dominant_pct = type_counts[dominant] / total * 100

INFO: "Reward type distribution: {type_counts breakdown}"

if dominant_pct < 50:
    WARNING: "No dominant reward type ({dominant} at {dominant_pct}%).
              Pack may lack a coherent reward strategy.
              Consider settling a dominant type in the Step 2 interview."
```

**Threshold rationale:** A 50% threshold allows for natural variety (XP drip + item rewards + occasional loot tables) while catching packs where the reward economy is genuinely scattered. Observed baselines from the dataset:

| Pack | Dominant type | Percentage | Secondary |
|---|---|---|---|
| Craftoria | `item` | ~60% | `random` ~30% |
| Enigmatica 10 | `item` | ~65% | `loot` ~25% |
| MI:Foundation | `item` | ~99% | `choice` ~1% |

**Root cause prevention:** The Step 2 interview includes a "dominant reward type" decision point so the generator knows the intended strategy before generating. R34 validates that the generated output matches the declared intent.

**Why it matters:** A pack without a dominant reward type feels inconsistent to players — they don't know what to expect from the next quest. This isn't an error (some packs deliberately mix), but it should be a conscious choice, not an accident.

**Source:** E10 malum chapter has 2 `type: "random"` among otherwise all `type: "loot"` — likely authoring drift rather than deliberate mixing. Cross-validated across 25+ packs in Cycles 4–5.

---

## Player-Perspective

### PP2 — Backward Shortcut

Best reward moments don't just give something new — they give a way to do something already done, but faster. After reaching a milestone, the player unlocks an efficiency loop back to earlier content.

**Config implication:** Milestone rewards should include at least one backward-optimizing element: a machine that automates an earlier manual process, a tool that speeds up earlier gathering, or an alternative recipe using more abundant materials. Stronger than raw materials because it compounds over time.

### PP6 — Wrong Tool Reward

Reward is a tool that seems relevant but is from the wrong mod for the pack's specific combination. "Why did I get an IE hammer? Next quest needs an Oritech wrench."

**Config implication:** When rewarding a tool, verify the specific tool ID matches what the next quest's description or task requires. In multi-mod packs, each mod's wrench is a distinct item with distinct recipes. Don't assume "a wrench is a wrench."

### R37 -- Capstone-Only Progression Break (Reward Safety Tiers by Pack Type)

**Step 5 priority:** P2 (INFO for kitchen-sink, WARNING for expert)
**Data dependency:** Item tier estimation (L1 heuristic + L2 user data)

In kitchen-sink packs (`progression_mode: "flexible"`), only capstone-tier items (ATM Star, Creative items, endgame-only items) constitute a true progression break when given as quest rewards. Utility items (Ender Chest, Universal Cable, basic machines) are sandbox tools. In expert packs, ANY gated item given early is a progression break.

**Why:** TheBedrockMaster (ATM-10): "It is a kitchen sink pack, the only thing that could actually break progression would be gifting out ATM Stars." This principle formalizes the pack-type-dependent reward safety threshold.

**Source:** AllTheMods/ATM-10 Discussion #3539

### R38 -- Tier Transition Milestone Reward

**Step 5 priority:** P2 (WARNING)
**Data dependency:** Tier/chapter ordering + effort estimation

When a quest chain crosses a technology tier boundary (MV to HV, Basic to Hardened, Iron to Diamond), the first quest at the new tier must include at least one tier-appropriate reward that helps bridge the effort gap. Material bridge, tool reward, or XP all qualify. Chains crossing tier boundaries without rewards are AP18 amplified by effort spikes.

**Why:** Craftoria #231 -- "3 tiers of reactors with no relevant quest rewards." GregTech-Odyssey #1602 -- HV effort spike without bridge reward, player reports burnout risk.

**Source:** TeamAOF/Craftoria #231, GregTech-Odyssey #1602

### R44 -- Reward-Stage Matching (奖励-阶段匹配)

**Step 4 priority:** P2 (L1 heuristic -- `[unverified:reward_stage]`)
**Step 5 priority:** P1 (完整 L1+L2 检查)
**数据依赖:** L1 (shared-builtin-tables) / L2 (用户提供的阶段-物品映射)

**检查什么：** 任务奖励的物品等级不应超过该任务所在阶段 +1 级。R12（Reward Value Progression）检查奖励价值是否随深度递增，R44 进一步检查奖励物品是否"越级"——即奖励了一个远超当前阶段的物品，使玩家可以绕过当前章节的预期挑战。R37（Capstone-Only Progression Break）定义了 kitchen-sink 和 expert 包的不同安全阈值，R44 在两个包类型中都执行，但阈值不同。[Phase 3 Cycle 8 - github.com/AllTheMods/ATM-10/discussions/3539]

```
for each quest Q:
    quest_stage = determine_stage(Q.chapter, pack_type)
    for reward in Q.item_rewards():
        reward_stage = stage_map.get(reward.item.id) or estimate_stage(reward.item.id)
        if reward_stage > quest_stage + 1:
            if pack_type == "expert":
                ERROR: "reward {reward.item.id} stage {reward_stage} > quest stage {quest_stage} + 1"
            else:
                WARNING: "reward {reward.item.id} stage {reward_stage} > quest stage {quest_stage} + 1"
        # Cross-challenge bypass check (human review item)
        if chapter_theme == "difficult_mining" and reward.provides("auto_mining"):
            INFO: "[human-review] reward bypasses chapter challenge theme"
```

**reward_table 边界说明 [Phase 4 Cycle 8 - 审查员B]：** R44 的上述伪代码仅检查 `type: "item"` 的确定性物品奖励。当奖励是 `type: "random"` 或 `type: "loot"` 时，R44 无法直接检查 reward_table 内的物品——因为 reward_table 是一个独立的加权池，玩家实际获得的物品是随机的。对此类奖励，R44 降级为启发式检查：检查 reward_table 是否在已知阶段内有定义（通过 `reward_tables/*.snbt` 的文件名推断该表的阶段归属），而非逐物品匹配。具体做法：将 reward_table 的阶段取其引用 quest 所在阶段的众数；如果 table 阶段 > quest 阶段 + 1，触发 WARNING。由于 `random` 和 `loot` 类型的实际获得物品是随机的，严重度统一降一级（expert 包从 ERROR 降为 WARNING，kitchen-sink 包保持 INFO）。`type: "choice"` 的奖励因玩家可主动选择，保持原严重度不变。这是启发式检查，非确定性检查。

```
# reward_table heuristic extension [Phase 4 Cycle 8 - 审查员B]
for reward in Q.rewards:
    if reward.type in ("random", "loot"):
        table = load_reward_table(reward.table_id)
        table_stage = estimate_table_stage(table)  # 基于引用该表的 quest 所在阶段的众数
        for entry in table.rewards:
            if entry.type == "item":
                entry_stage = stage_map.get(entry.item.id) or estimate_stage(entry.item.id)
                if entry_stage and entry_stage > table_stage + 1:
                    WARNING: "reward_table {table.id} contains {entry.item.id}
                              (stage {entry_stage}) exceeding table stage {table_stage} + 1"
```

**无阶段数据降级 [Phase 4 Cycle 8 - 审查员A]：** R44 在 expert 包中效果最佳（阶段定义清晰），在 kitchen-sink 包中严重依赖 L2 用户数据。当 `stage_map` 不存在时，R44 退化为 `estimate_stage()`（基于物品名关键词和合成深度启发式），精度约 60-70%。无阶段定义的 kitchen-sink 包中 R44 进一步退化为 INFO 级别报告：

```
if not stage_map:
    INFO: "[no-stage-data] reward-stage matching skipped — pack has no stage definitions"
```

Expert 包中阈值为严格的 stage+1（ERROR），kitchen-sink 包中降级为 WARNING 并参考 R37 的 capstone-only 安全阈值——TheBedrockMaster 主张"只有赠送 ATM Stars 才会真正破坏 kitchen-sink 进度"。额外的"挑战绕过检查"（如章节主题为"困难采矿"但奖励了"自动寻矿符咒"）可编码性低，标记为人类审查项。

**违反了会怎样：** ATM-10 的典型案例——任务奖励的 ATM 矿石视觉符咒让玩家跳过预期的采矿难度，"just reaching the mining dimension with 3 players means you are instantly finding every allthemodium ore you want"。Ender Chest 在游戏早期没有意义，Ultimate Universal Cable 在玩家"几乎没合成过一打基础线缆"时就被奖励。[Phase 3 Cycle 8 - xiaoxiao921, github.com/AllTheMods/ATM-10/discussions/3539]

**来源：** AllTheMods/ATM-10 Discussion #3539 (xiaoxiao921 的评论)

### R45 -- Reward Guidance Bridging (奖励引导衔接)

**Step 4 priority:** P2 (反向检查)
**Step 5 priority:** P1 (正向全量检查)
**数据依赖:** 无需外部数据（纯 quest book 结构分析）

**检查什么：** 章节完成奖励（即章节最后一个 quest 或 capstone quest 的奖励）应包含下一章首个任务所需的关键材料或工具。R10（Reward-to-Dependent Bridge）检查的是 quest 级别的奖励-依赖桥接，R45 专门检查 chapter 级别的衔接——确保章节之间的过渡有明确的"奖励引导"而非"断裂"。[Phase 3 Cycle 8 - mcmod.cn/post/4382.html, meegle.com/en_us/topics/game-design/quest-design]

```
for each chapter C:
    next_chapter = chapters[C.order_index + 1]
    if not next_chapter: continue  # last chapter

    # Get completion rewards (capstone or last quest)
    capstone = find_capstone_quest(C)  # quest with most dependencies
    if not capstone: continue
    completion_rewards = set(r.item.id for r in capstone.item_rewards())

    # Get next chapter's entry requirements
    entry_quests = [q for q in next_chapter.quests if not q.dependencies or
                    all(d in C.quests for d in q.dependencies)]
    entry_items = set()
    for q in entry_quests:
        entry_items.update(t.item.id for t in q.item_tasks())

    # Check overlap
    bridge = completion_rewards.intersection(entry_items)
    if not bridge and entry_items:
        WARNING: "Chapter {C.name} completion rewards do not bridge to {next_chapter.name} entry tasks"
```

**非物品奖励的引导价值 [Phase 4 Cycle 8 - 审查员B]：** R45 的上述伪代码仅检查 `item_rewards()` 的物品交集。如果 capstone 的奖励是纯 XP、xp_levels、command（如 gamestage 解锁）或 reward_table（随机奖励），`completion_rewards` 将为空集，导致 R45 误报"衔接断裂"。实际上 gamestage 解锁、dimension 解锁、command 奖励应被视为"虚拟桥接项"——它们虽然不是物品，但确实引导玩家进入下一阶段的内容。扩展后的检查逻辑如下：

```
# Virtual bridge items for non-item rewards [Phase 4 Cycle 8 - 审查员B]
completion_rewards = set(r.item.id for r in capstone.item_rewards())

# Gamestage 解锁视为虚拟桥接项
for cmd in capstone.command_rewards:
    if cmd.activates_stage(s):
        completion_rewards.add(f"stage:{s}")

# Dimension 解锁视为虚拟桥接项
for task_or_reward in capstone.dimension_rewards:
    completion_rewards.add(f"dimension:{task_or_reward.dimension}")

# 与下一章的阶段需求匹配
entry_stage_requirements = set()
for q in entry_quests:
    if q.required_stage:
        entry_stage_requirements.add(f"stage:{q.required_stage}")

stage_bridge = completion_rewards.intersection(entry_stage_requirements)
if stage_bridge:
    pass  # Stage-based bridging is valid even without item bridging
elif not bridge and entry_items:
    WARNING
```

当奖励包含 gamestage 解锁时，检查解锁的 stage 是否在下一章被依赖。如果下一章的入口任务有 `gamestage` 类型的 task 或章节标记了 `required_stage`，且该 stage 恰被 capstone 的 command reward 解锁，则视为衔接有效，不触发 WARNING。

奖励引导衔接的核心原则是"奖励物品最好是下一个任务链的起始材料"。这与 MP14（Material Bridge）在 quest 级别实现的效果一致，R45 将其提升到 chapter 级别。同时应避免奖励"万能物品"（可以替代多种材料的物品），因为万能物品消除了引导的方向性——玩家可以用它做任何事，而不是被引向下一个章节。中期阶段可以引入"跨模组的扫荡性机制"（如日夜维度交换）来跨越整个任务章节，这种宏观引导超出了 R45 的检查范围，属于人类审查项。[Phase 3 Cycle 8 - mcmod.cn/post/4382.html]

**违反了会怎样：** 章节完成后的奖励对下一阶段毫无帮助，玩家感觉"做了一整章的任务但什么都没得到"——这是 AP6（Dead-End Reward）在 chapter 级别的放大版。

**来源：** mcmod.cn/post/4382.html（论较高难度包）；Meegle 通用任务设计原则（meegle.com/en_us/topics/game-design/quest-design）

### R46 — Questbook Role Declaration (任务书角色声明)

**Step 2 priority:** 设计阶段必选决策
**Step 5 priority:** P2 (INFO — 验证声明一致性)
**数据依赖:** 无需外部数据（纯 quest book 统计分析）

**检查什么：** 每个包在 Step 2 设计访谈中必须声明其 questbook 的主要角色。数据集中观察到三种角色：(1) **Companion（伴生导航）** — questbook 提供方向和发现性辅助，将机制教学委托给 field guide 和配方查看器（TFG Modern, TFG Vintage）；(2) **Tutorial System（教程系统）** — questbook 是主要的教学机制，每个机械原理都需要一个 quest 节点（Monifactory, E9E, 多数 expert 包）；(3) **Incentive Catalog（激励目录）** — questbook 以奖励作为主要进度激励（ATM 系列, Craftoria）。角色声明决定下游设计选择：companion 包应有高 optional 率和零/低奖励；tutorial 包需要 MP11 Teach-Then-Do 序列的全面覆盖；incentive catalog 包需要 R12/R13/R34 合规的奖励经济计划。当未做声明时，包容易在角色之间漂移——描述假设 tutorial 模式而奖励假设 incentive 模式，造成不一致。

```
if pack.questbook_role == "companion":
    if reward_density > 0.5 per quest:
        WARNING: "Companion-mode pack has high reward density ({density}).
                  This contradicts the companion role."
    if optional_rate < 0.10:
        INFO: "Companion-mode pack has low optional rate ({rate}).
               Consider whether all quests are truly needed for direction."
elif pack.questbook_role == "tutorial":
    if description_coverage < 0.90:
        WARNING: "Tutorial-mode pack has {coverage}% description coverage.
                  Every mechanic needs documented guidance."
elif pack.questbook_role == "incentive_catalog":
    if not has_reward_economy_plan:
        WARNING: "Incentive-catalog pack without a reward economy plan.
                  R12/R13/R34 compliance requires upfront tier definitions."
```

**违反了会怎样：** 包在角色之间漂移，玩家不确定 questbook 的定位——是该认真阅读描述学习机制，还是快速跳过只看奖励？ATM-10 的 #3539 争论部分源于这种漂移：TheBedrockMaster 将 questbook 视为 incentive catalog（"only ATM Stars would break progression"），而 xiaoxiao921 将其视为 tutorial（"rewards should match progression stage"）。

**来源：** Pyritie/TFG Modern #3656; Monifactory CONTRIBUTING.md; Phase 3 Cycle 9

### R50 — Zero-Reward Design Safety Conditions (零奖励设计安全条件)

**Step 2 priority:** P2 (INFO — 设计决策指导)
**Step 5 priority:** P2 (INFO/WARNING — 验证零奖励安全性)
**数据依赖:** 全量 book 扫描（reward density 统计）+ pack type 分类

**检查什么：** 零奖励设计（MP41）在三个条件同时满足时是安全的。当任一条件缺失时，零奖励设计有玩家流失风险，因为 quest 完成没有正反馈循环。此规则将 Exzept1on 的"受苦就是体验"哲学形式化为可验证的安全条件。

**三个安全条件：**
```
zero_reward_safe = (
    has_alternative_progression_currency AND
    questbook_role in ("companion", "catalog") AND
    has_strong_intrinsic_gameplay_loop
)

# 条件 1: 存在替代进度货币（电压等级、徽章、技能等级——非 quest 奖励）
has_alternative_progression_currency = (
    pack_has_voltage_tiers OR     # GregTech expert packs
    pack_has_badge_system OR      # Cobblemon gym badges
    pack_has_skill_progression OR # RPG packs with leveling
    pack_has_stage_gating         # Game Stages-based progression
)

# 条件 2: Questbook 角色不是激励传递
questbook_role_safe = pack.questbook_role in ("companion", "catalog")

# 条件 3: 强内在游戏循环
has_strong_intrinsic_loop = (
    pack_type in ("expert", "collection") OR  # 合成/收藏本身有满足感
    pack_has_combat_loop OR                    # Pokemon, boss fights, dungeons
    pack_has_exploration_loop                  # 维度跳跃, 结构发现
)
```

当 `zero_reward_safe` 为 false 且包的奖励密度接近零时：
```
if pack.reward_density < 0.05 and not zero_reward_safe:
    WARNING: "Pack has near-zero rewards but lacks the conditions for safe zero-reward design.
              Missing: {missing_conditions}.
              Players may disengage without positive feedback from quest completion."
```

**负面对照 (ATM-10 #3539)：** ATM-10 的 `questbook_role == "incentive_catalog"` 且内在循环较弱（"try all the mods" 本身不够有满足感），使零奖励设计不适用。TheBedrockMaster 对慷慨奖励的辩护在 ATM-10 的设计上下文中是正确的——从 kitchen-sink 激励目录中移除奖励会严重损害玩家参与度。

**正面验证 (TFG Modern + Cobblemon)：** TFG Modern 满足全部三个条件（电压等级进度 + companion 角色 + GregTech 合成循环）。Cobblemon 同样满足（gym badges + catalog 角色 + Pokemon 收集/战斗循环）。两者都有 600-1300+ quests 且零奖励，玩家反馈未出现奖励不满（TFG #416 的抱怨实际上是因为移植内容显示奖励文本造成虚假期望，而非缺乏奖励本身）。

**来源：** Exzept1on/TFG Modern #3656; Cobblemon 1307-quest 零奖励验证; cesspit.net backward shortcut principle; ATM-10 #3539 negative control; Phase 3 Cycle 9

### ATM-10 奖励跨级争议：Kitchen-Sink 与 Expert 的分水岭

ATM-10 Discussion #3539 集中体现了奖励设计中"包类型决定安全阈值"的核心矛盾。玩家 xiaoxiao921 指出多个奖励跨级问题：ATM 矿石视觉符咒绕过了预期的采矿难度、Ender Chest 在游戏早期无意义、Ultimate Universal Cable 在玩家还没合成基础线缆时就被奖励。其核心论点是"almost everything IMO should be re-reviewed and a general balance pass done"。包协作者 TheBedrockMaster 反驳："It is a kitchen sink pack, the only thing that could actually 'break progression' would be gifting out ATM Stars。"这个争论的价值不在于谁对谁错，而在于它揭示了 R37 和 R44 的设计分水岭：Kitchen-sink 包中"破坏进度"的阈值远高于 Expert 包——前者只有 endgame capstone 物品（ATM Stars, Creative items）才算越级，后者任何超过 stage+1 的物品奖励都是越级。R44 通过差异化阈值（expert ERROR / kitchen-sink WARNING）将这一分水岭编码为自动化检查。[Phase 3 Cycle 8 - github.com/AllTheMods/ATM-10/discussions/3539]

---

## Cross-References

| This module's ID | Related in other modules | Relationship |
|---|---|---|
| MP14 Material Bridge | mod-teaching-pacing R17 | Tool reward often bridges alongside material bridge |
| MP15 Tool Reward | mod-teaching-pacing R17 | Tool-Reward-Before-Use ordering rule |
| MP16 XP Drip | mod-atm-signature | ATM-specific implementation data lives there |
| MP29 Command Reward | mod-teaching-pacing MP23 | Invisible Infrastructure uses command rewards heavily |
| MP39 Alternative-Reward | mod-teaching-pacing MP23 | Invisible Infrastructure routes stages alongside alternative rewards |
| MP39 Alternative-Reward | mod-item-reachability | Game Stages as external reachability gatekeeper |
| AP6 Dead-End Reward | mod-teaching-pacing PP5 | Dead-end rewards worsen the Context Void |
| AP8 Reward Inflation | mod-teaching-pacing MP19 | Chapter-as-Stage defines budget boundaries |
| AP18 Reward Desert | mod-teaching-pacing R19 | Bottleneck Spacing detects reward deserts |
| R10 Bridge | mod-teaching-pacing R14 | Teach-Then-Do ordering affects reward flow direction |
| R28 Command Safety | mod-safety-systems | Full AP15 side-effect analysis lives there |
| R33 Table Integrity | mod-dependency-graph R22 | Cross-reference pattern (table_id refs like cross-chapter deps) |
| PP6 Wrong Tool | mod-teaching-pacing PP5 | Both stem from insufficient mod-awareness |
