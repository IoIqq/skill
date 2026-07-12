# 审查员 A — 通用性质疑

**审查日期：** 2026-07-06
**审查范围：** micro-patterns.md (32 MP + 7 PP), anti-patterns.md (13 AP), progression-rules.md (26 R)
**核心问题：** 这些模式和规则真的跨包适用吗？

---

## 0. 数据集分布基线

在进行逐条审查之前，必须先明确数据集的组成偏差：

| 包系列/类型 | 包数量 | 占比 | 包含的包 |
|---|---|---|---|
| **ATM 系列** | 6 | 40% | ATM-8, ATM-9, ATM-10, ATM-10-Sky, ATM-11, All-the-Mons |
| **Create 系列** | 4 | 27% | Create: Delight, Mechanomania, Create: Astral, Create Skylands |
| **Expert** | 2 | 13% | Monifactory, Enigmatica 9 Expert |
| **Magic** | 1 | 7% | Arcana |
| **RPG** | 1 | 7% | Prominence II |
| **Skyblock (非 ATM)** | 1 | 7% | Create Skylands (兼属 Create) |

ATM + Create 合计占 10/15 = **67%**。这意味着：
- 任何在 ATM 全系列中观察到的模式，会被计为"4-6 个包验证"，但实际上可能只反映 **一个设计团队 (AllTheMods)** 的惯例。
- Create 系列 4 个包中有 3 个体量偏小（395 / 650 / 100 quests），Create: Delight（2,295 quests）是唯一的重量级 Create 数据源。
- Magic 和 RPG 各只有 1 个包，无法区分"该类型的通用模式"和"该包的特有选择"。
- **真正独立的设计团队** 只有：AllTheMods、Create: Delight 作者、Create: Astral 作者 (Laskyyy)、Mechanomania 作者、Monifactory 团队、Arcana/Prominence II 作者。6 个独立团队，其中 AllTheMods 贡献了 40% 的数据。

---

## 1. 确认通用（有充分跨包数据支撑）

以下模式/规则在 **3 个以上独立设计团队** 的包中均有观察到，可以合理地称为"通用"。

### Micro-Patterns

| Pattern | Scope 标注 | 实际验证范围 | 判定 |
|---|---|---|---|
| **MP1** Single-Item Gate | all | 15 个包全部使用，90%+ quests 为单 task | **确认通用** — 数据充分，跨所有包类型 |
| **MP3** Acknowledgement Gate | all | Create: Delight (湿度教程) + ATM-10 (Mekanism 教程) + Monifactory (教程链) + Prominence II | **确认通用** — 教学型 quest 在所有包类型中都存在 |
| **MP6** Linear Chain | all | 15 个包全部使用，expert/skyblock 尤其深 | **确认通用** — 最基础的依赖拓扑 |
| **MP7** Fan-Out | all | ATM-10 (Ars Nouveau 130 quests), Create: Delight (Mouse_Chef), Monifactory (tier 边界), Arcana (17 roots) | **确认通用** — 跨 4 个独立团队验证 |
| **MP8** Fan-In / Convergence | all | ATM-10 (ATM Star 10 deps), Create: Delight (category hubs), Monifactory (convergence nodes) | **确认通用** — capstone 是跨类型设计概念 |
| **MP11** Teach-Then-Do | all | Create: Delight (Feast_Afoot) + ATM-10 (Mekanism) + Monifactory (教程→实践) | **确认通用** — 3 个独立团队 |
| **MP14** Material Bridge | all | ATM-10 (AE2 chain) + Create: Delight (工具链) + Monifactory (tight bridge) + 概念跨所有包 | **确认通用** — reward 引导是基本设计需求 |
| **MP15** Tool Reward | all | Create: Delight (hygrometer/watering can) + ATM-10 (guide book) + Monifactory (machine unlocks) | **确认通用** — 跨所有包类型 |
| **MP19** Chapter-as-Stage | all | 15 个包全部使用 chapter 组织内容 | **确认通用** — FTB Quests 的基本组织单元 |

### Anti-Patterns

| AP | Scope | 实际验证范围 | 判定 |
|---|---|---|---|
| **AP1** Description-Reality Mismatch | 通用 | FTB Evolution (#6447), Architect's Exodus (5+ issues), Create: Astral (#613, #618), FTB Skies 2, StoneBlock 4 | **确认通用** — 跨 5+ 个不相关包，是最普遍的投诉 |
| **AP2** Circular Dependency Deadlock | 通用 | FTB Evolution (cross-mod), FTB Skies 2 (within-mod Productive Bees) | **确认通用** — 跨 mod 和单 mod 两个变体均有验证 |
| **AP3** Unfinishable Chapter | 通用 | FTB Evolution (Getting Started 不可完成) | **部分确认** — 仅 1 个包有直接证据，但问题机制适用于所有包 |
| **AP4** Wrong Gating | 通用 | FTB Evolution (5+ 个 gating 问题), 概念上适用所有使用 `dependency_requirement` 的包 | **确认通用** — 机制层面适用所有包 |
| **AP5** Empty Description | 通用 | FTB Evolution (Industrial Foregoing chapter), cesspit.net 分析 | **确认通用** — 新玩家体验问题是跨类型的 |
| **AP7** Hidden Quest Trap | 通用 | FTB Evolution (永久隐藏 quest), Create: Delight (72 次使用 hide_until_deps_visible) | **确认通用** — 机制层面适用所有使用渐进式揭示的包 |
| **AP8** Reward Inflation | 通用 | cesspit.net 分析 (expert pack), 概念上适用所有包 | **确认通用** — reward 经济是跨类型问题 |

### Progression Rules

| Rule | Scope | 判定 |
|---|---|---|
| **R5** Circular Dependency Detection | 通用 | **确认通用** — 标准图算法，适用任何有 `dependencies` 的包 |
| **R6** Unreachable Quest Detection | 通用 | **确认通用** — 图连通性检查，不依赖包类型 |
| **R7** Optional-Gate-Mandatory | 通用 | **确认通用** — `optional` + `dependencies` 的语义问题跨所有包 |
| **R8** Dependency Requirement Consistency | 通用 | **确认通用** — `dependency_requirement` 字段适用所有包 |
| **R10** Reward-to-Dependent Bridge | 通用 | **确认通用** — reward 连贯性检查适用所有包 |
| **R18** Description Coverage | 通用 | **确认通用** — `description` 字段存在于所有 quest |
| **R20** Chapter Completion Testability | 通用 | **确认通用** — 纯图结构检查 |
| **R22** Cross-Chapter Dependency Validity | 通用 | **确认通用** — 引用完整性检查 |
| **R23** Description-Item Consistency | 通用 | **确认通用** — 纯文本匹配，不依赖包类型 |

### Player-Perspective Patterns

| Pattern | Scope | 判定 |
|---|---|---|
| **PP1** Trust Contract | all | **确认通用** — 描述准确性对所有包都重要 |
| **PP3** Invisible Wall | all | **确认通用** — gating 反馈问题跨所有包类型 |
| **PP4** Completionist's Dilemma | all | **确认通用** — 章节完成度是 FTB Quests 的内置机制 |
| **PP5** Context Void | all | **确认通用** — 新手体验问题跨所有包 |
| **PP7** Mod-Unification Trap | all (多 mod 包) | **确认通用** — 但严格来说只适用 200+ mod 的 kitchen-sink；5-mod 包几乎不会遇到 |

---

## 2. 过度泛化（需要缩小适用范围）

### MP2 — Multi-Item Synthesis Bundle
- **当前标注：** `all`，High confidence (15 packs)
- **实际证据：** 主案例来自 ATM-10 ATM Star (12 tasks, hexagon)。次要引用：AE2 starter (2 tasks)。量化数据 (tasks/quest 梯度) 全部来自 ATM-10。
- **问题：** "15 packs" 的 confidence 标注暗示 15 个包都有 multi-item synthesis quest。但文档中只有 ATM-10 提供了量化证据 (ATM Star 3.6 tasks/quest, Mekanism 3.2)。其他包虽然 *可能* 有 multi-task quest，但没有提供具体案例或数据。Create: Delight 的 Mouse_Chef 明确是 "1 task per cell" (304 quests, 大部分 1 task)。Mechanomania 平均 1.0 tasks/quest。
- **建议修正：** Scope 保持 `all`（概念确实通用），但 Source confidence 改为 **"High (ATM-10 quantified; concept validated in expert packs)"**。标注 "15 packs" 具有误导性。

### MP4 — Escalation Ladder
- **当前标注：** `all`，High confidence (ATM-10, ATM-9, ATM-10-Sky)
- **实际证据：** 唯一的详细案例来自 ATM-10 Bounty Board (87 kill tasks, zombie ladder 5→10→25→50→100)。confidence 来源全部是 ATM 系列包。
- **问题：** 三个验证源全是 AllTheMods 团队的包。Bounty Board 是 ATM 系列的特色功能（kill-count grind），不能代表所有包的设计选择。Prominence II (RPG) 有 kill quest 但未提供 escalation ladder 的具体数据。Create 系列和 Expert 包完全没有 escalation ladder 的证据。
- **建议修正：**
  - Scope: `all` → **`kitchen-sink, story`**
  - Confidence: "High (ATM-10, ATM-9, ATM-10-Sky)" → **"Medium (ATM series primary; concept applicable to combat/grind packs)"**
  - 添加注释：Escalation Ladder 需要包内有 mob-grind 或重复性活动的 gameplay loop，纯 tech/expert 包通常不使用。

### MP12 — Tier Escalation Within a Chapter
- **当前标注：** `all`，High confidence (8+ packs)
- **实际证据：** 主案例来自 ATM-10 AllTheModium (diamond 形状, 3-tier column)。"8+ packs" 未具体列出是哪些。
- **问题：** Tier escalation 的核心案例全部围绕 AllTheModium 三金属 (AllTheModium → Vibranium → Unobtainium) 的 tier 系统。这是 ATM 系列的 signature 设计。Expert 包 (Monifactory) 确实有 tier escalation 但以 voltage-tier 跨 chapter 而非 within-chapter 实现。Create 系列的 tier 是 speed/efficiency 而非 material。RPG 的 tier 是 level/ability。
- **建议修正：** Scope 保持 `all`（tier 概念确实通用），但 confidence 改为 **"High (ATM-10 primary case; concept cross-validated in expert and RPG packs)"**。明确标注 "within-chapter material tier" 的具体形态主要来自 ATM。

### MP16 — XP Drip
- **当前标注：** `kitchen-sink, expert`
- **实际证据：** ATM-10 (10/50/100 XP tiers, 6,915 rewards/4,601 quests = 1.5/quest), ATM-9 (1.7/quest), ATM-8 (1.7/quest), Monifactory (varies)
- **问题：** XP drip 的量化数据几乎全部来自 ATM 系列。Monifactory 被标注为 "varies" 但未给出具体 XP drip 数据。Create: Delight 的 reward density 只有 0.43/quest，Mechanomania 0.11/quest — 这两个包的 reward 哲学明显不是 "XP drip"。Scope 标注 `kitchen-sink, expert` 可能过于宽泛。
- **建议修正：**
  - Scope: `kitchen-sink, expert` → **`kitchen-sink`** (ATM 型 generous reward 哲学)
  - 添加注释：Expert 包的 reward 哲学差异大 — Monifactory 的 reward 系统不以 XP drip 为核心。Create 系列明确不使用 XP drip (Create: Delight 0.43/quest, Mechanomania 0.11/quest)。

### MP9 — Diamond (pick-and-rejoin)
- **当前标注：** `expert, story`，High confidence (Monifactory, Create: Delight, Create: Astral)
- **实际证据：** Monifactory (voltage-tier branching), Create: Delight (`one_started` ×63, `one_completed` ×44), Create: Astral
- **问题：** Scope 标注 `expert, story`，但实际验证主要来自 Create 系列 (2/3 来源)。Monifactory 只有定性描述 ("uses one_completed for voltage-tier branching") 无量化数据。RPG/story 包完全没有 diamond 的证据。`story` 标注缺乏数据支撑。
- **建议修正：**
  - Scope: `expert, story` → **`expert, create`**
  - 添加注释：Diamond pattern 在 Create 系列中的使用频率远高于 expert 包 (`one_started` ×63 in Create: Delight vs Monifactory 定性描述)。Story/RPG 包缺乏证据。

### R9 — Dependency Depth Reasonableness
- **当前标注：** 通用 (pack-type specific thresholds)
- **实际证据：** 阈值来自 Cross-Pack Comparison Table：kitchen-sink max 8 (ATM 系列), expert max 20 (Monifactory + ATM9-Sky), create max 10 (Create packs)
- **问题：** kitchen-sink 的 max depth 8 仅基于 ATM 系列数据 (typical 3-5, max observed 6)。如果有一个非 ATM 的 kitchen-sink 使用 depth 10 的 chain，这个阈值就不成立。RPG 的 max 12 只有 Prominence II 一个数据点。
- **建议修正：** 标注为 **"参考值，基于有限样本"**。建议阈值表格增加 "validated packs" 列：kitchen-sink (ATM-8/9/10), expert (Monifactory, ATM9-Sky), create (4 packs), rpg (Prominence II only — low confidence)。

### R12 — Reward Value Progression
- **当前标注：** 通用
- **实际证据：** 规则逻辑引用了 ATM-10 的 XP drip (10/50/100 tiers) 和 cesspit.net 分析。
- **问题：** `estimate_value()` 函数完全是假设性的。不同包的 reward 价值体系差异巨大：ATM 用 XP + material，Create 用 coin + checkmark，expert 用 machine unlock。一个统一的 "value score" 无法跨包比较。规则标注为 INFO level 是合理的，但暗示它可以跨包工作则需要更多验证。
- **建议修正：** 保持 INFO level。添加注释："`estimate_value` 需要按包类型定制 — 无法用统一公式跨包比较 reward 价值"。

### R15 — Complexity Escalation Within Chapter
- **当前标注：** 通用
- **实际证据：** 引用 MP12 (ATM-10 AllTheModium) 作为来源。
- **问题：** "complexity" 的定义 (`recipe_depth * log(count + 1)`) 高度依赖 recipe depth 数据，而 recipe depth 在没有 JEI/EMI 数据时只能靠 heuristic 估算 (R3 的 L1, ±2 级误差)。这意味着 R15 的准确性受限于 R3 的数据质量。对于 expert 包（合成链 15+ 步），±2 级误差使规则几乎不可用。
- **建议修正：** 添加前提条件："R15 的有效性依赖 R3 的数据质量。无 L2/L3 数据时，R15 降级为纯 heuristic 提醒"。

---

## 3. 应降级或移除

### MP32 — min_tasks Modifier (partial completion)
- **当前标注：** `create, kitchen-sink`，Low confidence (Create: Astral only, single-source)
- **问题：**
  1. **唯一数据来源是 Create: Astral** — 一个 650-quest 的 Fabric 1.18.2 包。一个包的一个章节中使用的 `min_tasks: 1` 不足以支撑一个编号模式。
  2. **功能上与 MP9 (Diamond) 重叠。** 文档自己承认："This is related to `dependency_requirement: 'one_completed'` (MP9 diamond) but operates at the task level rather than the dependency level." 一个 task-level 变体不值得独立 MP 编号。
  3. **`kitchen-sink` scope 标注完全无数据支撑。** 15 个包中没有任何 kitchen-sink 包使用 `min_tasks` 的证据。
  4. **实际设计价值低。** `min_tasks` 是 FTB Quests 的一个边缘功能，在 15 个包的数万 quest 中仅出现于 Create: Astral 的几个 quest。
- **建议：** **降级为 MP9 的注释变体**，而非独立 MP。在 MP9 (Diamond) 条目下添加："Task-level variant: `min_tasks: N` on a quest with M > N tasks achieves a similar 'pick your path' effect within a single quest (observed in Create: Astral)."

### MP31 — Structure Discovery Gate
- **当前标注：** `skyblock, kitchen-sink, story`，Medium confidence (ATM-10-Sky, ATM-9, All-the-Mons)
- **问题：**
  1. **三个来源包全属 AllTheMods 团队。** ATM-10-Sky (skyblock), ATM-9 (kitchen-sink), All-the-Mons (kitchen-sink + Cobblemon)。这不是三个独立验证 — 是同一设计团队在三种包类型中的同一思路。
  2. **包类型差异使 pattern 语义模糊。** Skyblock 中 structure task 是稀缺资源门（Fortress 在 skyblock 中很难找到），kitchen-sink 中是探索门（结构存在但需要定位），RPG 中是剧情入口点。三种使用场景的设计意图完全不同，强行统一为一个 pattern 失去精确性。
  3. **Prominence II (唯一的 RPG 包) 没有被引用为 structure task 的证据**，尽管 RPG 包最可能使用 structure discovery。文档提到 "RPG packs (as dungeon entry points)" 作为适用场景但无实际数据。
  4. **与 MP5 (Dimension + Item Composite) 和 MP21 (Dimension-as-Stage-Gate) 的概念边界不清。** Structure task 是 dimension task 的细化版本（"进入 Nether" vs "在 Nether 中找到 Fortress"），文档自己也承认这一点。
- **建议：**
  - 保持为独立 MP（概念上有区分价值），但 **缩小 scope**: `skyblock, kitchen-sink, story` → **`skyblock, kitchen-sink`** (story 缺乏证据)
  - Confidence 改为 **"Low (all 3 sources from AllTheMods team; no independent RPG validation)"**
  - 添加待验证项："需要非 ATM 的 RPG/skyblock 包数据确认 structure task 的使用模式"

### MP20 — Shape-as-Tier Signal
- **当前标注：** `kitchen-sink, expert`，High confidence (ATM-10, ATM-9, ATM-8, ATM-10-Sky)
- **问题：** 4 个验证源 **全部是 ATM 系列**。shape-as-tier 是 AllTheMods 的设计签名 — 文档自己说 "~47% of ATM-10 quests set an explicit shape vs ~3-8% in curated packs"。其他包几乎不使用 shape 语义。Create: Delight 使用 shape 区分 catalog vs narrative (rsquare vs circle) 但不是 tier 信号。Monifactory 的 shape 使用未被提及。
- **建议：**
  - Scope: `kitchen-sink, expert` → **`kitchen-sink (ATM-style)`**
  - Confidence 改为 **"High within ATM series; Low outside (curated packs use 3-8% explicit shape)"**
  - 添加注释：Shape-as-tier 是 ATM 系列的视觉设计签名，不是 FTB Quests 的通用设计模式。对于不使用丰富 shape 词汇的包，此模式不适用。

### MP22 — Material-Tier Spine
- **当前标注：** `kitchen-sink`
- **问题：** Scope 正确标注为 kitchen-sink，但 confidence 来源 (ATM-10, ATM-9, ATM-8, ATM-10-Sky) 全部是 ATM 系列。Material-tier spine (AllTheModium → Vibranium → Unobtainium) 是 **ATM 的标志性 endgame 设计**，不是 kitchen-sink 类型的通用特征。一个非 ATM 的 kitchen-sink 包可能完全没有三金属 tier spine。
- **建议：** 添加注释 **"ATM series signature pattern; not observed in non-ATM kitchen-sinks"**。或考虑与 MP21 (Dimension-as-Stage-Gate) 合并为 "ATM Signature Patterns" 小节。

### MP10 — Independent Island
- **当前标注：** `kitchen-sink, create`，High confidence (8+ packs)
- **问题：** 主案例是 Create: Delight Mouse_Chef (258/304 quests = independent islands) 和 Arcana (17 root quests)。"8+ packs" 未具体列出。Independent island 更准确地说是 **catalog layout 的固有属性**，而非一个需要编号的"模式"。任何使用 grid/catalog 布局的 chapter 自然会有 independent islands。
- **建议：** 保持 MP 编号但标注为 **"Layout primitive rather than a design choice — any catalog chapter produces islands by default"**。

### AP3 — Unfinishable Chapter
- **当前标注：** 通用
- **问题：** 直接证据 **仅来自 FTB Evolution issue #6447 一个包**。虽然机制上适用所有包，但只有一个实际案例不足以称为"最常见 anti-pattern"。
- **建议：** 保持为 AP（问题严重性足够），但标注 **"Single-pack evidence; mechanism universally applicable"**。

### AP12 — Task-Item NBT Insensitivity
- **当前标注：** 通用 (anti-patterns.md 中作为机制缺陷呈现)
- **问题：**
  1. **唯一案例来自 Create: Astral #566** — fluid cell quests 接受任何 fluid cell 而不检查 NBT。
  2. **这是 Create mod 特有问题还是 FTB Quests 通用问题？** 需要区分两层：(a) FTB Quests 的 item task 默认不检查 NBT — 这是 **FTB Quests mod 层面的行为**，适用所有包；(b) fluid cell 是 Create mod 的物品 — NBT 敏感的 fluid container 在 Create 包中最常见，但在有 Mekanism (gas tanks) 或 Thermal (fluid cells) 的 tech kitchen-sink 中同样存在。
  3. **结论：机制层面是通用的**（FTB Quests 的 NBT 匹配行为适用所有包），**但实际触发概率与 mod 组合高度相关**。纯 vanilla+少数 mod 的包几乎不会遇到；有 3+ 个 fluid-processing mod 的 tech 包风险最高。
- **建议：**
  - 保持为 AP，但 **scope 精细化**：从"通用"改为 **"tech packs with NBT-bearing fluid containers (Mekanism, Thermal, Create)"**
  - 添加注释："Root cause is FTB Quests' item task NBT matching behavior (universal), but practical impact is limited to packs with NBT-sensitive items (tech-focused)"
  - 关联到 progression-rules 的 AP 映射表中已正确标注 "无对应规则（需要运行时 NBT 匹配验证，非静态分析可检测）" — 这是正确的

### `hide_dependency_lines` 的处理
- **文档中的现状：** `hide_dependency_lines` 在多个 MP 中被引用为实现细节（MP7 Fan-Out: "uses `hide_dependency_lines: true` if >3 dependents"；MP8 Fan-In: "typically has `hide_dependent_lines: true`"；MP22: "hide_dependency_lines on 31/54 quests"），但**没有被提取为独立模式或 anti-pattern**。
- **Scope Annotation Table 中：** 文档在 MP22 的注释中将 `hide_dependency_lines` 描述为 "ATM 系列设计签名" — "~47% of ATM-10 quests set an explicit shape vs ~3-8% in curated packs"。但这说的是 shape 而非 hide_dependency_lines 本身。
- **问题：** `hide_dependency_lines` 在 ATM-10 中使用频率远高于其他包（AllTheModium 31/54, Ars Nouveau tier gates, ATM Star capstone）。但文档在 MP7 和 MP8 中将它作为通用实现建议 ("uses `hide_dependency_lines: true` if >3 dependents")，没有标注这是 ATM 特有的做法。
- **建议：** 在 MP7 和 MP8 的实现描述中 **添加 scope 注释**："Note: heavy use of `hide_dependency_lines` is an ATM-series design signature. In curated packs (3-8% explicit shape/line settings), dependency lines are typically left visible as navigation aids."

---

## 4. 应降级为 "ATM Signature" 分类的模式组

以下模式虽然各有编号，但它们的 **核心证据全部来自 AllTheMods 团队的包**，更准确地说是"ATM 设计哲学"的体现，而非 FTB Quests 的通用模式。建议将它们归入一个 **"ATM Signature Patterns"** 小节（类似已有的 "Part 8: Cycle 2 Patterns"），明确标注为单一设计团队的惯例：

| Pattern | 核心证据来源 | 独立验证 |
|---|---|---|
| MP4 Escalation Ladder | ATM-10 Bounty Board | 无 (仅 ATM 系列) |
| MP16 XP Drip | ATM-10/9/8 reward density | Monifactory "varies" (无具体数据) |
| MP20 Shape-as-Tier Signal | ATM-10 shape vocabulary | 其他包 3-8% shape 使用率 |
| MP21 Dimension-as-Stage-Gate | ATM-10 welcome + dimension chapters | 无独立 kitchen-sink 验证 |
| MP22 Material-Tier Spine | ATM AllTheModium spine | 无 (ATM 独有 endgame) |

这 5 个模式的 **概念** 是通用的（escalation, XP reward, shape semantics, dimension gating, material tiers），但**具体实现形态**高度 ATM 化。当一个 non-ATM 包作者阅读这些模式时，他看到的案例全是 ATM 的做法，可能误以为这是"标准做法"。

---

## 5. 缺失的包类型覆盖

### 完全缺失的包类型

| 包类型 | 缺失程度 | 影响 |
|---|---|---|
| **Tech-focused (非 kitchen-sink)** | 完全缺失 | 纯 tech 包（如 FTB Interactions Remastered, FTB OceanBlock）的设计模式未被覆盖。Interactions Remastered 在 issue tracker 中有出现 (#12217) 但未进行系统审计 |
| **Hardcore/生存挑战** | 完全缺失 | Hardcore 包的 quest 设计可能完全不同（reward = 生存资源, gating = 生存能力）。RLCraft, SevTech: Ages of the Sky 等未纳入 |
| **Adventure/探索 (非 RPG)** | 完全缺失 | 纯 adventure 包（以探索/剧情为核心，非 RPG 战斗）的代表缺失 |
| **Mini-game/社交** | 完全缺失 | 以小游戏或社交互动为核心的包完全未覆盖 |
| **1.7.10/1.12.2 经典 expert** | 完全缺失 | GTNH 和 Divine Journey 2 使用 BetterQuesting 而非 FTB Quests，但它们的 expert-pack 设计哲学（voltage-tier gating, age-based progression）被引用为 progression-rules 的来源。这意味着 R4 (Stage Boundary) 和 R9 (Depth Reasonableness) 的 expert 阈值来自一个 **不同 quest 系统** 的包 |

### 严重不足的包类型

| 包类型 | 现有代表 | 不足程度 |
|---|---|---|
| **Magic** | Arcana (1 包) | 严重不足 — 无法区分 "magic pack 通用模式" 和 "Arcana 的设计选择"。Arcana 的 17-root fan-out 可能是该包独有的 |
| **RPG/Adventure** | Prominence II (1 包) | 严重不足 — Prominence II 的 dependency-gated image reveals 和 7 task types 被多次引用为 RPG 特征，但只有 1 个数据点 |
| **Expert** | Monifactory + E9E (2 包) | 不足 — Monifactory 是唯一的深度审计 expert 包。E9E 只有结构数据 (dual chapters)。Expert 阈值（depth 8-20, voltage-tier）本质上是 Monifactory 一个包的阈值 |

### 数据集偏斜的量化影响

1. **ATM 系列占 40% 的包但贡献了 ~60% 的量化数据。** ATM-10 单独贡献了 4,601 quests 的详细审计数据（占 15 包总 quests 的 ~25%）。大多数量化比较表（tasks/quest, reward density, shape usage, dependency depth）以 ATM-10 为主角。

2. **Create: Delight 是 Create 系列的唯一重量级数据源。** Mechanomania (395 quests) 和 Create Skylands (~100 quests) 太小，Create: Astral (~650 quests) 中等。当文档说 "Create 系列使用 X 模式" 时，通常意味着 "Create: Delight 使用 X 模式"。

3. **Player feedback 数据高度集中在 FTB Evolution (#6447)。** AP1 的 12+ 个案例中，7 个来自 FTB Evolution, 5 个来自 Architect's Exodus, 2 个来自 Create: Astral。一个包的问题清单驱动了整个 anti-pattern 体系。

---

## 6. 对 Scope Annotation Table 的逐行审计

Scope Annotation Table 声称某些模式适用于 "all" pack types。以下是这些标注的可靠性评估：

| Pattern | 标注 | 非 ATM 非 Create 验证 | 标注可信度 |
|---|---|---|---|
| MP1 (all) | 所有包都有 single-item quests | ATM, Create, Expert, Magic, RPG 全部验证 | **高** |
| MP2 (all) | 多 task synthesis | 仅 ATM-10 有量化数据 | **中** — 概念通用但证据偏斜 |
| MP3 (all) | checkmark/stat tutorial | Create: Delight + ATM-10 + Monifactory | **高** |
| MP6 (all) | linear chain | 所有包都有 | **高** |
| MP7 (all) | fan-out | ATM, Create, Expert, Magic 验证 | **高** |
| MP8 (all) | fan-in | ATM, Create, Expert 验证 | **高** |
| MP11 (all) | teach-then-do | Create + ATM + Expert 验证 | **高** |
| MP12 (all) | tier escalation | 主要 ATM-10 AllTheModium | **中低** — "all" 过于宽泛 |
| MP14 (all) | material bridge | ATM + Create + Expert 验证 | **高** |
| MP15 (all) | tool reward | ATM + Create + Expert 验证 | **高** |
| MP19 (all) | chapter-as-stage | 所有包都用 chapter | **高** |
| MP24 (all) | tier-reachability check | 规则逻辑通用 | **高** |
| MP25 (all) | dependency-order check | 规则逻辑通用 | **高** |
| MP26 (all) | reward-continuity check | 规则逻辑通用 | **高** |
| PP1-PP7 (all) | player experience | 来自玩家反馈，非包特有 | **高** |

**结论：** 在 16 个标注为 "all" 的条目中，MP2 和 MP12 的证据基础不足以支撑 "all" 标注。其余 14 个的 "all" 标注合理。

---

## 7. 特别关注项回应

### MP31 (Structure Discovery Gate) — 来自 ATM-10-Sky 和 All-the-Mons
**这两个包类型差异大，pattern 真的通用吗？**

不通用。ATM-10-Sky 使用 structure task 作为 **资源稀缺性门** — skyblock 世界中 Fortress 很难找到，structure task 确保玩家确实找到了。All-the-Mons 使用 structure task 作为 **探索激励** — Cobblemon 整合包鼓励玩家探索世界寻找宝可梦栖息地。两者的设计意图不同：
- Skyblock: "你必须找到这个结构才能继续"（gate）
- Cobblemon: "去找到这个化石遗址来获取特殊宝可梦"（incentive）

将它们归为同一个 pattern 模糊了设计意图的差异。建议将 skyblock 和 kitchen-sink 的 structure task 用法分开描述，或至少在 "Design considerations" 中明确区分两种使用动机。

### MP32 (min_tasks Modifier) — 仅来自 Create: Astral
**它真的值得一个 MP 编号吗？**

不值得。理由见上方 "应降级或移除" 部分。建议降级为 MP9 的注释变体。

### `hide_dependency_lines` — 被标注为 "ATM 系列设计签名"
**MP 文档中有没有还把它当通用模式推荐？**

有。在 MP7 (Fan-Out) 的实现描述中写道："H uses `hide_dependency_lines: true` if it has >3 dependents (to avoid line clutter)" — 这被呈现为一个通用实现建议，而非 ATM 特有做法。在 MP8 (Fan-In) 中写道："Z typically has `hide_dependent_lines: true`" — 同样是通用化的 ATM 做法。

但 Scope Annotation Table 中 **没有** 将 `hide_dependency_lines` 作为独立模式推荐 — 它只是 MP7/MP8/MP22 实现细节的一部分。问题在于这些实现细节被当作通用最佳实践呈现，而实际上它们是 ATM 的设计偏好。

### AP12 (NBT Insensitivity) — 来自 Create: Astral
**这是 Create mod 特有问题还是 FTB Quests 通用问题？**

见上方 "应降级或移除" 部分。机制层面是 FTB Quests 通用的（item task 默认不检查 NBT），但实际触发概率取决于包中是否有 NBT-sensitive 物品。Create 的 fluid cell 是最常见的触发场景，但 Mekanism 的 gas tank 和 Thermal 的 fluid cell 同样适用。建议 scope 精细化为 "tech packs with NBT-bearing items"。

---

## 8. 总结与建议

### 核心发现

1. **ATM 系列过度代表是最严重的通用性威胁。** 15 个包中 6 个来自同一团队，且 ATM-10 单独贡献了最大单一数据集 (4,601 quests)。约 5 个 MP (MP4, MP16, MP20, MP21, MP22) 的核心证据全部来自 ATM 系列。

2. **Create: Delight 是 Create 系列的代理。** 当文档说 "Create 系列使用 X" 时，实际上通常只有 Create: Delight 一个包有足够数据。

3. **Magic 和 RPG 各只有 1 个包。** 任何标注为适用于 magic 或 story 类型的模式，实际上只有一个数据点。

4. **经典 expert 包 (GTNH, DJ2) 使用不同 quest 系统。** 它们的 expert-pack 设计哲学被引用但无法直接验证 FTB Quests 的对应规则。

5. **Player feedback 数据集中在 FTB Evolution (#6447) 一个 issue。** AP1 的大部分案例来自单一玩家对单一包的审计。

### 建议的结构性改进

1. **添加 "ATM Signature Patterns" 分类**，将 MP4, MP16, MP20, MP21, MP22 归入，明确标注为 AllTheMods 设计团队的惯例。
2. **MP32 降级为 MP9 变体注释**，移除独立编号。
3. **MP31 拆分为 skyblock 和 kitchen-sink 两个变体描述**。
4. **Scope Annotation Table 增加 "independent teams validated" 列**，标注每个模式被多少个独立设计团队（非同一组织的包）验证过。
5. **progression-rules.md 的 expert 阈值 (R4, R9) 标注来源为 Monifactory 单包**，建议 expert 包作者根据自己的包调整阈值。
6. **`hide_dependency_lines` 在 MP7/MP8 的实现描述中添加 ATM-signature 注释**。
7. **下一轮数据收集应优先覆盖**：非 ATM kitchen-sink (如 FTB OceanBlock, FTB Presents)、非 Create tech pack (如 FTB Interactions Remastered)、第二个 magic/RPG 包。
