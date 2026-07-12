# Module: Description Trust — 任务描述可信吗？

> **Core Question:** 玩家能否信任 quest description 作为引导系统？当描述文本与实际游戏机制脱节时，整本 quest book 的可信度瞬间崩塌。

## Quick Reference

| ID | 名称 | 类型 | 严重性 | 阶段 |
|---|---|---|---|---|
| AP1 | Description-Reality Mismatch | Anti-Pattern | **最高** | 全局 |
| AP9 | Hallucination Cascade | AI Anti-Pattern | High | Step 4 |
| AP10 | Style Homogenization | AI Anti-Pattern | Medium | Step 4/5 |
| AP11 | Batch Narrative Inconsistency | AI Anti-Pattern | Medium | Step 4/5 |
| R23 | Description-Item Consistency | Rule | P0 ERROR | Step 4 |
| R24 | Suggestion-Reachability | Rule | P2 INFO/WARN | Step 4/5 |
| R26 | Quest-Mod Version Consistency | Rule | P3 INFO | Step 4/5 |
| R49 | Collection-Catalog Maintenance Cost | Rule | P2 INFO/WARNING | Step 2/5 |
| PP1 | Trust Contract | Player Pattern | — | Step 2 |

---

## Anti-Patterns

### AP1 — Description-Reality Mismatch（完整版）

**症状：** 玩家按照 quest description 的指引操作，发现指引是错的。描述提到 "Shadowflame Goo" 但任务要求的是 "Shadowpulse Goo"；描述说"在熔炉中烧炼"但实际需要高炉；描述声称奖励一组物品但 `rewards` 数组给的是另一组。

**根因：** `description` 字段是 free-form text，FTB Quests **不会**将它与 `tasks`/`rewards` 数据做校验。author 基于对 mod 机制的假设写描述，没有在游戏内验证。mod 更新后 recipe 或物品名变了，描述没有同步。

**后果：** 玩家停止信任 quest descriptions，转而完全忽略它们。quest book 从引导系统退化为一个不透明的 checklist。对于依赖 quest book 作为主要教程的新玩家，这是毁灭性的。cesspit.net 的分析一针见血："this HUGE questbook, with more than 2000 quests, was at the same time a great guide to erase the problem of guessing"——当 questbook 撒谎时，整个系统崩塌。

**修复原则：** 每条 description 必须被视为一个**可验证的声明**：(1) 物品名匹配 display name；(2) 合成指引匹配 JEI/EMI recipe；(3) 声称的 reward 匹配 `rewards` 数组；(4) mod 更新后重新验证。

**实证案例（多包交叉验证）：**

AP1 是跨包、跨版本出现频率最高的反面模式，已在 14+ 个包中确认（含 Phase 2 Cycle 9 新增的 TFG Modern 和 TFG Vintage quest port drift 案例）：

- **FTB Evolution #6447** — 单玩家记录数十处不匹配："The Ore of the Eclipse Quest talks about Shadowflame Goo, but asks for Shadowpulse Goo"；"Making Multiblocks with Machine Cores rewards the immersive engineering hammer, rather than the Oritech wrench"；"The MI nuclear reactor can't explode, emit radiation, etc."但 quest 没提。
- **FTB Architect's Exodus** — #12549 Botania quest 声称需要 Dominant Spark Augment，但 plate 实际从 mana pool 抽取；#12458 "Sentient Tools" 把 Demonic Will 称为 Souls；#12426 新手第二个 quest 就要 stone pickaxe 而非 wooden。
- **Create: Astral** — #613 "Automate Lapis!" 说 Asurine 可以 mill 出 Zinc，实际产出 Lapis Lazuli；#618 声称 prismarine 用于 automate veridium，实际无此 recipe。
- **FTB Evolution Cycle 3** — #12609 "Throwing Daggers" 要求 'raw spiritus' 但实际掉落 'spiritus essence'，阻塞整条 hellfire forge 子链。
- **Monifactory #1545** — questbook 未警告 EnderIO Yeta Wrench 的 crouch-scroll 在当前版本损坏，玩家被迫手动拆线重连。

- **Monifactory #2667** — questbook states silicone rubber and SBR "can wrap any cable tier" but silicone rubber cannot wrap UEV cables and only works on cryococcus at UHV. Polyphenylene sulphide quest similarly inaccurate about "LuV+" coverage. AP1 + R26 temporal variant (description was correct when written, became wrong after mod recipe changes).
- **Finality Genesis #42** — "Introduction to Sophisticated Storage" quest requires spruce wood specifically but should accept any wood type. Description implies general crafting but task is overly specific. AP1 variant at the task-requirement level rather than text level.
- **ATM-10 #4208/#4199** — Loot Bag from Lunar Monstruosity became unobtainable after mod update changed boss loot table, but quest still requires it as a task item for the ATM Star altar. Description references a recipe that no longer exists. AP1 + AP3 compound: description-reality mismatch caused by mod update removing the recipe entirely.

- **GregTech-Odyssey #1548** — Large alchemy pot quest doesn't mention the 90% output cap. Players assume full output, plan production lines around expected yield, and discover 10% loss only at runtime. AP1 variant: description omission of a critical numeric constraint (R26 domain).
- **GregTech-Odyssey #1440** — Stainless Steel 15 5ph quest requires an EV-level mixer with 2 stacks of output space (only obtainable via processing plant with EV integral casing, which requires platline setup), but "No indication in questbook." AP1 + PP5 compound: description doesn't warn about prerequisite infrastructure.
- **NFwC #333** — Ender Dragon kill quest only triggers from "normal" kill method. Player uses bed explosion (a valid Minecraft kill method) but quest doesn't detect the kill, blocking progression. AP1 variant: description implies "defeat the Ender Dragon" but the actual detection condition is narrower.
- **NFwC #288** — Ember Liver quest description says "up to 8 levels of Strength" but actual organ effect gives up to 5 levels. Task text vs mod mechanic numerical mismatch. AP1 + R26: hardcoded number in description doesn't match mod's actual value.
- **TheWinterRescue #95** — Quill and Ink quest dependency is placed AFTER Electron Tubes and Bronze Steam Engine, but paper/ink are needed for common research that unlocks those quests. AP1 dependency-ordering variant: the quest's position in the graph contradicts the actual usage order.
- **TheWinterRescue #87** — Quest says "get copper gravel" but copper gravel has no usable recipe. AP1 + AP6 compound: description guides player to obtain an item that serves no purpose.

**Cycle 7 Phase 2 — Architect's Exodus issue flood (2026-06-28 to 2026-07-07):**

Architect's Exodus generated 19 quest-type issues in 3 weeks on FTB-Modpack-Issues, the highest per-pack issue density observed in the dataset. New AP1 variants confirmed:

- **#12458** — "Sentient Tools" quest confuses "Souls" with "Demonic Will" (mod terminology). AP1 terminology variant: wrong mod-specific term in description.
- **#12459** — "Bottle o' Lightning" quest asks for "basic lightning spell" but 2 of 3 accepted items are uncommon-tier spells. AP1 task-specification variant: task accepts items that don't match description's stated tier.
- **#12463** — "Empowered Netherite" quest requires ancient debris when empowered netherite is easily obtainable from bastions. AP1 **task-over-specificity** variant: required task item is unnecessarily restrictive, blocking valid alternative paths. New sub-variant.
- **#12571** — Wrong quest text for "Slay Skol and Hati" — description says "prove to Jormungandr, which we killed a few realms earlier." AP1 cross-quest reference error.
- **#12584** — Enderman, Spectral and Glowstone Talisman descriptions say "Force of the Overworld" but dependency lines correctly point to "Force of the Explorer." AP1 description-reference mismatch (description wrong, lines correct).
- **#12580** — Forsaken summoning altar has space requirements not mentioned in any quest or tooltip. Summoning consumes items even when it fails. AP1 description **omission of critical spatial constraint**. New sub-variant: spatial/mechanic requirements that exist in kube.js but are invisible to the player.
- **#12600** — Jormungandr summoning recipe missing from game. Quest references a recipe that doesn't exist in current version. AP1 + AP3 compound.
- **#12613** — Botania "Terrestrial Agglomeration Plate" quest requires "Spark Augment: Dominant" which can only be obtained AFTER constructing the portal. Quest is a prerequisite for the portal quest. AP3 sequence inversion (item gated behind content it unlocks). Already partially documented as #12549 but this is a new, cleaner case.
- **#12614** — Soul Stained Gear quest requires specific armor variant, should accept Tinker's Construct variants. AP1 task-over-specificity variant (same sub-variant as #12463).
- **#12623** — Maledictus boss: "you can only know you have to fight him if you go to Asgard." No quest directs the player there. AP1 omission + PP5 Context Void: critical navigation information missing from quest book.
- **#12535** — Ferrous Wroughaunt quest description guides player to use structure compass at a location where it doesn't work. AP1 location-reference error.
- **#12529** — Maledictus doesn't auto-spawn after beating prerequisite boss (Skol and Hati). Quest book implies spawn is automatic. AP1 implied-mechanic variant: description implies automatic trigger that doesn't fire.
- **#12428** — "pwoer" typo in MI Quantum Upgrade quest. AP1 trivial typo.

**Phase 2 Cycle 9 — TFG quest port drift (2026-07-10):**

TFG Modern 和 TFG Vintage 的 issue tracker 揭示了一种新的 AP1 系统性来源：**Quest Port Drift**（任务移植漂移）。TFG Modern 的 LV+ chapters 的 quests 从另一个包（可能是 GregTech Community Pack）移植，但未完全适配 TFG 的实际 recipe chains 和 progression，导致系统性 AP1/AP2/AP4：

- **TFG Modern #344** — Create mod gating was moved behind Steam tier, but questbook still shows old progression path. AP1 caused by progression restructure outpacing quest book updates.
- **TFG Modern #457** — Steam extractor quest description promises behavior that the mod doesn't implement. Classic description-behavior mismatch.
- **TFG Modern #3860** — Item Pipes Quest suggests pipes that are not obtainable at the player's current tier. AP4 variant: quest implies availability that doesn't exist.
- **TFG Modern #416** — Russian players reported quests displaying reward text from the source pack, while TFG intends zero rewards. AP1 variant: legacy reward text from ported content creates false expectations.
- **TFG Vintage #103** — Stone tools quests require items not obtainable through TFC's normal stone tool mechanics. AP1 variant caused by TFC-specific mechanics not matching quest expectations.
- **TFG Vintage #38** — Quest placed in wrong voltage tier chapter ("Квест в неправильной эре"). AP4 variant: quest position contradicts actual progression requirement.

Quest Port Drift is a meta-anti-pattern: systematic AP1/AP2/AP4 arising from copying quest content between packs without adaptation. TFG contributors explicitly acknowledge this ("the quests are just ported from that modpack") and track it as known technical debt.

**AI 生成的特殊风险：** AI 编写描述时倾向于"听起来合理"而非"经过验证"。当 AI 生成 50 个 quest 的批次时，描述中的合成指引可能基于训练数据中的旧版 mod 信息，而非当前包的实际 recipe。R23 可捕获物品 ID 层面的不匹配，但"熔炉 vs 高炉"这类机制层面的错误仍需 JEI/EMI 运行时验证。

---

### AP9 — Hallucination Cascade（AI 生成专属）

**症状：** AI 生成的 quest 引用了不存在的 item ID（如 `mekanism:quantum_infuser`，实际应为 `mekanism:antiprotonic_nucleosynthesizer`）。后续 quest 依赖这个虚构物品，第三个 quest 为它提供"合成 recipe"。幻觉级联：一个错误 ID 污染整批 quest。

**根因：** LLM 逐 token 生成，没有对包的 item registry 做验证。`items.json5` 检查可防止**有意的**虚构，但更微妙的错误会溜过去：错误的 count（AI 猜 64 而 recipe 需要 16）、错误的 dependency 顺序（AI 假设 mod 的内部 progression 而不验证实际 recipe chain）。

**后果：** 玩家遇到一组 individually plausible 但 collectively impossible 的 quest cluster。与人类 typo（影响一个 quest）不同，AI hallucination 通过 dependency chain 传播。

**修复：** (1) 每个 item ID 在写入 spec 前必须通过 `items.json5` 验证；(2) batch 生成后做"hallucination audit"——扫描所有 item ID，flag 不匹配项，只重新生成受影响的 quest。

---

### AP10 — Style Homogenization（AI 生成专属）

**症状：** 每个 quest description 都是同一个模板："Obtain [item]. This is needed for [next step]." 每个 reward 都是 "10 XP + 1 item"。每个 quest 都用相同的 shape 和 size。整章读起来像 form letter。

**根因：** LLM 有 strong prior toward uniform output。没有 explicit variation guidance，模型收敛到一个"safe"模板并反复使用。这不是 hallucination——每个 quest 技术上正确——但缺乏 variety 让 quest book 感觉机械。

**检测：** Flag chapters where description length 标准差 < 10 characters，或 > 70% quest 共享完全相同的 reward 结构。

**修复：** 交替使用 how-to / lore / tip / challenge 四种描述风格。reward 按 tier 分级：routine 5–10 XP、milestone 25–50 XP、capstone 50+ XP。

---

### AP11 — Batch Narrative Inconsistency（AI 生成专属）

**症状：** Quest 12 说"you'll need this Osmium Ingot for the Enrichment Chamber in the next quest"——但 Quest 13 不需要 Osmium Ingot。Quest 5 说"this is the hardest challenge"但 Quest 20 更难。相邻 quest 的语气在 casual 和 technical 之间跳跃。

**根因：** 顺序生成 quest 时，每个 quest 的 context window 可能不包含同批次前面 quest 的完整文本。forward reference（"next quest"、"you'll need this later"）指向与实际不符的内容。

**修复：** (1) 按 dependency 顺序生成（root → leaves），让每个 quest 有祖先的完整 context；(2) batch 后做 narrative consistency audit——提取所有 forward reference，验证引用的 quest 实际存在且匹配描述。

---

## Rules

### R23 — Description-Item Consistency Check

**执行阶段：** Step 4（P0 ERROR — 阻止写入 spec）

从 quest `description` 文本中提取所有 item ID 引用（正则匹配 `modid:item_name` 格式），与同一 quest 的 `tasks` 和 `rewards` 中的 item ID 做交叉比对。三层精度：

1. **ERROR** — 描述引用了不存在的 item ID（可能 AI hallucination 或 typo）
2. **WARNING** — 描述提到了一个有效 item 但该 item 不在当前 quest 的 tasks/rewards 中
3. **INFO** — task 物品 >50% 没在描述中提及

这是 AP1 的**部分**静态覆盖。能捕获"Shadowflame Goo vs Shadowpulse Goo"型名称错误，但无法捕获"熔炉 vs 高炉"型机制错误（需 JEI/EMI 运行时）。

---

### R24 — Suggestion-Reachability Check

**执行阶段：** Step 4（L1 降级）/ Step 5（全量）

> **Cross-Reference:** 此规则的物品可达性逻辑与 `mod-item-reachability` 模块中的 R1/R2 共享底层数据（`BUILTIN_DIMENSION_MAP`、`BUILTIN_TOOL_TIER_MAP`）。R24 的独特之处在于它检查的是 description **建议文本**而非 task 要求——玩家按建议准备装备却发现不可获得，信任损害不亚于 task 本身不可达。

检测 description 中使用引导性措辞（"建议使用"、"try using"、"best tool for"等）提到的物品，验证其在 quest 祖先链中是否已可获得。对 kitchen-sink（flexible）包保持 INFO 级别，对 expert/linear 包升级为 WARNING。

**实证：** FTB Architect's Exodus #12601 — Malum 符文建议在 killing Hel 之前使用，但符文的 crafting chain 需要 Hel 掉落的材料。#12580 — Forsaken summoning altar requires specific space dimensions (defined in kube.js) but no quest or tooltip mentions this. Player discovers requirement only after items are consumed by a failed summon. R24 extension: not just equipment suggestions but also spatial/mechanic prerequisites need reachability validation.

---

### R26 — Quest-Mod Version Consistency

**执行阶段：** Step 4（文本启发式）/ Step 5（需 mod 版本数据）

检测 description 中的硬编码数值（stack size、processing limit、acceleration card limit 等）是否仍与 mod 当前版本一致。mod 更新频率远高于 quest 文本更新——这是 AP1 的**时间维度变体**：description 曾经正确，但 mod 更新后变成了错的。

**实证：** FTB StoneBlock 4 #12328 — Circuit Fabricator 的 acceleration card limit 从 2 变为 3，quest 文本未同步。

---

### R49 — Collection-Catalog Maintenance Cost Assessment (收藏目录维护成本评估)

**执行阶段：** Step 2（设计决策 — INFO）/ Step 5（验证 — WARNING）

在采用 MP40（Collection-Catalog）设计 collection 章节之前，作者必须评估维护成本。Collection-catalog 章节为每个可收集物品创建一个 quest；当底层模组生态系统添加或移除物品时，每次变更都需要对应的 quest 更新。维护成本随以下因素增长：(1) catalog 中涵盖的模组数量，(2) 这些模组的更新频率，(3) catalog 物品来自稳定的还是活跃开发的模组。

```
for each collection_catalog_chapter C:
    mods_covered = unique_mod_namespaces(C.quest_tasks)
    update_frequency = estimate_update_frequency(mods_covered)  # from mod metadata

    high_churn_mods = [m for m in mods_covered if update_frequency > quarterly]
    if len(high_churn_mods) > 3:
        WARNING: "Collection-catalog chapter {C.name} covers {len(high_churn_mods)}
                  frequently-updated mods. Maintenance cost is high.
                  Consider: (a) limiting catalog to stable-content mods,
                  (b) using tag-based tasks that auto-include new items,
                  (c) accepting that this chapter will need regular updates."

    total_catalog_quests = len(C.quests)
    if total_catalog_quests > 200:
        INFO: "Chapter {C.name} has {total_catalog_quests} collection quests.
               Redeix/TFG warns: 'hundreds of quests = maintenance burden.'
               Ensure the pack team has committed to maintaining this chapter."
```

**与 AP1 (Description-Reality Mismatch) 的关联：** 当 collection-catalog 章节维护不足时，模组更新导致的物品变更会造成系统性 AP1：quest 要求的物品不再存在、描述引用的物品名称已更改、task 引用的物品 ID 无效。R49 的 WARNING 实际上是在预防未来的 AP1 爆发。Quest Port Drift（R48）与 collection-catalog 维护是同源问题——都源于游戏内容与 quest book 内容之间的异步。

**解释了 MP40 采用率差异：** 稳定内容包（SSV 的 Stardew 风格作物、Skylore 的烹饪）自由采用 MP40，而活跃开发的 expert 包（TFG Modern 的 TFC 食物系统）明确拒绝——Redeix 在 #4063 中直言 "hundreds and I'm not maintaining it when I add more"。200 quest 阈值源自 Redeix 的 "hundreds" 表述和观测数据：SSV building_shop（372 items/629 quests）和 Skylore chef（220 items/381 quests）均达到或超过此阈值。

**来源：** Redeix/TFG Modern #4063; Phase 3 Cycle 9

---

## Player Pattern

### PP1 — The Trust Contract

quest description 是 pack author 的声音。当它准确描述游戏机制时，玩家信任整本 quest book。当它撒谎——哪怕一次——玩家开始怀疑每一条后续描述。

高质量包维护一个"信任契约"：每条 description 都经过 game-mechanic 验证。description 不只是 flavor text，它是**主要教程渠道**。当 questbook 可靠时，玩家不需要跳出游戏查 wiki；当它不可靠时，wiki 变成了唯一可信源，quest book 沦为多余的一层。

**Cycle 7 validation:** Architect's Exodus generated 19 quest-type issues in 3 weeks (June 28 – July 7, 2026). Players explicitly describe trust erosion: "Maledictus was a bit of a leap" (#12623), "you can only know you have to fight him if you go to Asgard" — the quest book's failure to provide navigation information forces players to consult external sources. The "play scroll button that doesn't do anything" on the Maledictus quest further erodes trust in interactive quest elements.

**配置含义：** `description` 字段没有任何 validation。每条描述都应被当作一个 claim 来测试。mod 更新后必须 re-verify。

---

## Cross-References

| 相关模块 | 关系 |
|---|---|
| `mod-item-reachability` | R1/R2 提供物品可达性数据，R24 复用其底层映射 |
| `mod-reward-design` | AP6 Dead-End Reward 与 description 声称奖励不匹配属 AP1 变体 |
| `mod-system-safety` | R28 Command Reward Safety 的 command 文本可能出现在 description 中 |
| `mod-atm-signature` | ATM 系列 47% shape usage 意味着描述中引用 shape 语义时更需注意一致性 |
| `mod-dependency-graph` | R48 (Quest Port Drift) 是 AP1 的系统性来源——移植 quest 的描述未经目标包验证 |
| `mod-teaching-pacing` | R47 (Companion Tool Delegation) 与 AP5 互为反面——R47 检测描述过于冗余而非过于稀疏 |

---

## Sources

- FTBTeam/FTB-Modpack-Issues #6447（FTB Evolution，73+ 问题审计）
- FTBTeam/FTB-Modpack-Issues #12549, #12571, #12458, #12459, #12426（Architect's Exodus）
- FTBTeam/FTB-Modpack-Issues #12428, #12463, #12469, #12503, #12529, #12535, #12574, #12575, #12580, #12584, #12595, #12600, #12601, #12609, #12612, #12613, #12614, #12623（Architect's Exodus Cycle 7 Phase 2）
- FTBTeam/FTB-Modpack-Issues #12384, #12474（FTB StoneBlock 4 Cycle 7）
- Laskyyy/Create-Astral #613, #618
- Omicron-Industries/Monifactory #1545, #2667
- Project-Vyre/Finality-Genesis #42
- AllTheMods/ATM-10 #4208, #4199
- GregTech-Odyssey/GregTech-Odyssey #1548, #1440
- Go-Camping/No-Flesh-Within-Chest #333, #288
- TeamMoegMC/TheWinterRescue #95, #87
- TerraFirmaGreg-Team/Modpack-Modern #3656, #416, #344, #457, #3860, #4063, #4230（Quest Port Drift + 零奖励设计哲学 + 收藏目录维护成本, Phase 3 Cycle 9）
- Omicron-Industries/Monifactory CONTRIBUTING.md — 唯一公开的正式 quest 设计贡献指南（Phase 3 Cycle 9 验证 R35/R36/R39）
- AllTheMods/ATM-10 Discussion #3539 — 奖励跨级争议（已关闭，kitchen-sink 奖励安全阈值）
- cesspit.net — "Minecraft Is Not What You Think"
- MARYT-Studio/Blessed-Or-Cursed-Minecraft-Modpack — 3 issues (none quest-related)
- Saudade-Studio-RU/Magic-Superlative — 0 issues
- Project-ModularTech/ModularTech-Odyssey — 1 issue (not quest-related)
- sawich/MinecraftServerProminence2Config — 0 issues
