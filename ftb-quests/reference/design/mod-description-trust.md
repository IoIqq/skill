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
| PP1 | Trust Contract | Player Pattern | — | Step 2 |

---

## Anti-Patterns

### AP1 — Description-Reality Mismatch（完整版）

**症状：** 玩家按照 quest description 的指引操作，发现指引是错的。描述提到 "Shadowflame Goo" 但任务要求的是 "Shadowpulse Goo"；描述说"在熔炉中烧炼"但实际需要高炉；描述声称奖励一组物品但 `rewards` 数组给的是另一组。

**根因：** `description` 字段是 free-form text，FTB Quests **不会**将它与 `tasks`/`rewards` 数据做校验。author 基于对 mod 机制的假设写描述，没有在游戏内验证。mod 更新后 recipe 或物品名变了，描述没有同步。

**后果：** 玩家停止信任 quest descriptions，转而完全忽略它们。quest book 从引导系统退化为一个不透明的 checklist。对于依赖 quest book 作为主要教程的新玩家，这是毁灭性的。cesspit.net 的分析一针见血："this HUGE questbook, with more than 2000 quests, was at the same time a great guide to erase the problem of guessing"——当 questbook 撒谎时，整个系统崩塌。

**修复原则：** 每条 description 必须被视为一个**可验证的声明**：(1) 物品名匹配 display name；(2) 合成指引匹配 JEI/EMI recipe；(3) 声称的 reward 匹配 `rewards` 数组；(4) mod 更新后重新验证。

**实证案例（多包交叉验证）：**

AP1 是跨包、跨版本出现频率最高的反面模式，已在 7+ 个包中确认：

- **FTB Evolution #6447** — 单玩家记录数十处不匹配："The Ore of the Eclipse Quest talks about Shadowflame Goo, but asks for Shadowpulse Goo"；"Making Multiblocks with Machine Cores rewards the immersive engineering hammer, rather than the Oritech wrench"；"The MI nuclear reactor can't explode, emit radiation, etc."但 quest 没提。
- **FTB Architect's Exodus** — #12549 Botania quest 声称需要 Dominant Spark Augment，但 plate 实际从 mana pool 抽取；#12458 "Sentient Tools" 把 Demonic Will 称为 Souls；#12426 新手第二个 quest 就要 stone pickaxe 而非 wooden。
- **Create: Astral** — #613 "Automate Lapis!" 说 Asurine 可以 mill 出 Zinc，实际产出 Lapis Lazuli；#618 声称 prismarine 用于 automate veridium，实际无此 recipe。
- **FTB Evolution Cycle 3** — #12609 "Throwing Daggers" 要求 'raw spiritus' 但实际掉落 'spiritus essence'，阻塞整条 hellfire forge 子链。
- **Monifactory #1545** — questbook 未警告 EnderIO Yeta Wrench 的 crouch-scroll 在当前版本损坏，玩家被迫手动拆线重连。

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

**实证：** FTB Architect's Exodus #12601 — Malum 符文建议在 killing Hel 之前使用，但符文的 crafting chain 需要 Hel 掉落的材料。

---

### R26 — Quest-Mod Version Consistency

**执行阶段：** Step 4（文本启发式）/ Step 5（需 mod 版本数据）

检测 description 中的硬编码数值（stack size、processing limit、acceleration card limit 等）是否仍与 mod 当前版本一致。mod 更新频率远高于 quest 文本更新——这是 AP1 的**时间维度变体**：description 曾经正确，但 mod 更新后变成了错的。

**实证：** FTB StoneBlock 4 #12328 — Circuit Fabricator 的 acceleration card limit 从 2 变为 3，quest 文本未同步。

---

## Player Pattern

### PP1 — The Trust Contract

quest description 是 pack author 的声音。当它准确描述游戏机制时，玩家信任整本 quest book。当它撒谎——哪怕一次——玩家开始怀疑每一条后续描述。

高质量包维护一个"信任契约"：每条 description 都经过 game-mechanic 验证。description 不只是 flavor text，它是**主要教程渠道**。当 questbook 可靠时，玩家不需要跳出游戏查 wiki；当它不可靠时，wiki 变成了唯一可信源，quest book 沦为多余的一层。

**配置含义：** `description` 字段没有任何 validation。每条描述都应被当作一个 claim 来测试。mod 更新后必须 re-verify。

---

## Cross-References

| 相关模块 | 关系 |
|---|---|
| `mod-item-reachability` | R1/R2 提供物品可达性数据，R24 复用其底层映射 |
| `mod-reward-design` | AP6 Dead-End Reward 与 description 声称奖励不匹配属 AP1 变体 |
| `mod-system-safety` | R28 Command Reward Safety 的 command 文本可能出现在 description 中 |
| `mod-atm-signature` | ATM 系列 47% shape usage 意味着描述中引用 shape 语义时更需注意一致性 |

---

## Sources

- FTBTeam/FTB-Modpack-Issues #6447（FTB Evolution，73+ 问题审计）
- FTBTeam/FTB-Modpack-Issues #12549, #12571, #12458, #12459, #12426（Architect's Exodus）
- Laskyyy/Create-Astral #613, #618
- Omicron-Industries/Monifactory #1545
- cesspit.net — "Minecraft Is Not What You Think"
