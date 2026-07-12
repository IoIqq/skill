# 审查员 C — 实用性审查报告 (Cycle 7)

> **审查视角：** AI agent 在实际生成任务配置时，能否有效执行这些规则和模式？
> **审查范围：** 12 个文件，涵盖 ~41 条规则 (R1-R41) + ~38 个模式 (MP1-MP38, PP1-PP7) + ~20 个反模式 (AP1-AP20) + 路由系统 + SKILL.md 工作流

---

## agent 无法执行的规则

### 完全不可执行（需外部运行时/API，config 无法判断）

| 规则 | 所需外部信息 | 当前降级方案 | 可行性评估 |
|---|---|---|---|
| **R26 完整版** (Quest-Mod Version Consistency) | modrinth/CurseForge API 查询 mod 当前版本的数值变更 | 文本启发式（检测 description 中的数字） | **低** — 启发式只能找到包含数字的描述，无法判断数字是否已过时。agent 没有 API 访问能力 |
| **AP12** (NBT Insensitivity) | 运行时 NBT 匹配验证（fluid cell 是否接受空 cell） | 标注为"外部脚本" | **不可执行** — agent 无法进行游戏内测试 |
| **AP13** (Premature Submission) | quest 系统状态机行为（物品在 quest 解锁前是否被自动提交） | 标注为"外部脚本" | **不可执行** — 需要实际测试 |
| **AP1 完整版** (recipe 层面："熔炉 vs 高炉") | JEI/EMI recipe 数据 | R23 仅捕获 ID 层面 | **不可执行** — agent 无法查看实际合成配方 |
| **R5 隐式循环** (recipe graph 产生的循环) | JEI/EMI recipe graph export | 标注为"外部脚本" | **不可执行** — agent 只能检测 `dependencies` 数组中的显式循环 |
| **R11** (Reward-Target Accuracy) | `tool_category_map` — 按功能分组的工具映射表 | 未在模块中定义此表 | **部分不可执行** — 模块引用了 `tool_category_map` 但从未定义内容或生成方式。agent 需知道"IE hammer 和 Oritech wrench 属于同类工具" |

### 严重降级（L1 覆盖不足，实际形同虚设）

| 规则 | L1 覆盖范围 | 实际降级后果 |
|---|---|---|
| **R1** (Dimension-Reachability) | ~25 个 vanilla + ATM 标志性物品 | 对于 200+ mod 的包，绝大多数 mod 物品标记 `[unverified:dimension]`。规则实质上只对 vanilla 物品有效 |
| **R2** (Tool-Tier) | ~20 个 vanilla + ATM + Mekanism 工具 | GregTech voltage tier、Create 机器等级完全不在 L1 中 |
| **R3** (Recipe-Chain Depth) | 无内置数据，`estimate_recipe_depth_heuristic` 未定义 | agent 只能标记 `[unverified:recipe_depth]`，规则形同虚设 |
| **R4** (Stage Boundary) | 无内置数据 | 完全依赖用户在 Step 2 提供 stage 定义。若用户未提供则几乎无效 |

### 建议替代方案

1. **R3 的 heuristic 需具体化：** 在 `shared-builtin-tables.md` 中添加基于 mod namespace 的粗略深度估计表（如 `mekanism:*` 基础物品 depth=1, 机器 depth=2, multiblock depth=4），或明确告知 agent 根据物品名称中的 tier 关键词（ingot, dust, gear, circuit, controller）估计深度。

2. **R11 的 `tool_category_map` 需定义：** 在 `shared-builtin-tables.md` 中添加工具分类表，或将 R11 降级为纯文本检查（从 dependent quest description 中提取工具名，与 reward display name 做模糊匹配）。

3. **R26 应明确为"Step 5a 人工验证"：** 改为"Step 4: 标记含硬编码数值的 description 为 `[unverified:version]`；Step 5a: 列出标记项，要求用户确认。"

4. **AP12/AP13 整合为 Step 5a checklist：** 在 SKILL.md Step 5a 中添加："检查是否有 fluid cell / enchanted book / configured machine 类 task，提醒用户进行 NBT 匹配和提前提交测试。"

---

## 过于抽象的模式

### 概念可理解但实现指引不足

| 模式 | 问题 | 建议 |
|---|---|---|
| **MP23 Invisible Infrastructure** | 描述了"不可见的 stage-gating 逻辑"需求，但 agent 无法自行设计 KubeJS gamestage 脚本。Monifactory 案例具体但无法泛化 | 添加决策树："有 gamestage mod？→ command reward + gamestage task；没有 → hide_quest_until_deps_visible + quest_links" |
| **MP30 Gamestage Bridge** | agent 无法知道哪些 gamestage 名是有效的（由 KubeJS 定义，不在 quest config 中） | 明确标注：agent 生成 gamestage task/reward 时必须要求用户提供 stage 名列表 |
| **PP2 Backward Shortcut** | "里程碑奖励应包含 backward-optimizing element" — 设计哲学，非可执行 config 规则 | 降级为 Step 2 interview 问题，或转化为可检测规则："capstone reward 中是否包含在 ancestor task 中出现过的 mod namespace 的物品？" |
| **MP17 Hub Concentration** | 记录了 Create: Delight 的 1:4 ratio，但 agent 逐节点生成时无法判断当前 quest 是 cell 还是 hub | 添加具体阈值："dependents >= 5 → hub，rewards >= 3 种类型；其余 → cell，rewards <= 1 种" |
| **R40 Effort Preview** | "tier transition 的 description 必须 effort preview"，但 agent 无法可靠判断什么构成 tier transition | 将触发条件从关键词扫描改为明确列表（如：chapter 边界、MV→HV、Basic→Advanced） |
| **MP38 Reward Perception Split** | guidance 是"cap early-game rewards to materials obtainable within 1-2 hours" — agent 无法判断什么物品满足此条件 | 合并入 R37/R12 的实现逻辑 |

### 停留在概念层面、缺乏 config 映射

| 模式 | 问题 |
|---|---|
| **AP15 Command Reward Side Effect** | 5 个 failure mode 描述完整，但修复停留在概念（"确保幂等性"）。agent 无法执行运行时测试 |
| **AP16 Quest State Migration** | 关于 modpack 更新场景，首次生成时无法预防。更适合作为 `--adopt` mode 指南 |
| **R41 Early-Game Flexible Mode** | "前 N 个 chapter 应该用 flexible" — 检查的是 chapter 属性而非 quest 属性，agent 在逐节点生成时无法控制 |

### 建议：重新分类不可执行模式

以下模式应从"生成时参考"移至"设计哲学背景"（仅 Step 2 interview 加载）：
- PP2 Backward Shortcut → 设计哲学
- AP15 的 failure mode 分析 → 背景知识（Step 4 仅保留 R28）
- AP16 → 仅在 `--adopt` mode 文档中引用
- MP38 → 合并入 R37

---

## 规则优先级冲突

### 已识别的冲突对

#### 冲突 1：R10 (Reward Bridge) vs R12 (Reward Value Progression)

- **R10** 要求：每个 reward item 应出现在 dependent quest 的 task 中（material bridge）
- **R12** 要求：reward value 应随 dependency depth 递增
- **冲突场景：** Quest A (depth 2) 奖励 1 个 osmium ingot（bridge 到 Quest B），Quest C (depth 3) 奖励 10 XP。R10 满意，R12 标记 WARNING（osmium 价值 > XP）。
- **建议优先级：** **R10 > R12**。Material bridge 是功能性需求，reward value 是美学需求。R12 应标注"material bridge 例外"。

#### 冲突 2：R7 (Optional-Gate-Mandatory) vs MP9 (Diamond pick-and-rejoin)

- **R7** prose：mandatory quest 不能依赖 optional quest
- **MP9** 使用：`dependency_requirement: "one_completed"` 配合 optional 路径
- **实际情况：** R7 的 pseudocode 已正确处理（`requirement == "one_completed"` 且有 non-optional dep → OK），但 prose description 过于绝对。
- **建议：** 更新 R7 prose 以匹配 pseudocode：明确区分 `"all"` 和 `"one_completed"` 两种 requirement。

#### 冲突 3：R9 (Depth Reasonableness) vs R19 (Bottleneck Spacing)

- **R9** 限制：kitchen-sink max depth = 8
- **R19** 要求：bottleneck quest 之间需 recovery quest
- **冲突场景：** depth 7 的 chapter 有 4 个连续 bottleneck。加 recovery quest 满足 R19 后 depth = 11，违反 R9。
- **建议优先级：** **R19 > R9**。玩家体验优先于数字限制。R9 应标注为 soft guideline，当 R19 需要额外节点时 R9 阈值上浮 50%。

#### 冲突 4：R18 (Description Coverage) vs AP10 (Style Homogenization)

- **R18** 要求：所有非 catalog quest 必须有 description (>= 20 chars)
- **AP10** 要求：description 长度标准差 > 10 chars
- **冲突本质：** 不是真正矛盾，而是"确保有内容" vs "确保内容多样"。但同时满足两者需要 agent 有 creativity guidance。
- **建议：** 在 AP10 修复建议中添加 4 种具体 description 模板（how-to / lore / tip / challenge），降低 agent 的创意负担。当前 AP10 只说"vary structure"但没给模板。

#### 冲突 5：R36 (Dependency Root Isolation) vs MP10 (Independent Island)

- **R36** 规定：非 root chapter 的 quest 必须有 dependency
- **MP10** 描述：独立 quest 在 catalog/collection 中正常
- **建议：** R36 应扩展 `ROOT_CHAPTERS` 以包含 catalog-type chapters，或添加条件 `if quest.chapter.type == "catalog": skip`。

---

## 模块路由问题

### 路由表整体评估

**清晰度：良好。** 8 个场景到 8 个模块的映射明确，agent 可快速判断单个场景的加载目标。

### 遗漏和歧义

#### 遗漏 1：复合场景未覆盖

路由表假设每个场景对应一个模块，但实际生成中 agent 常需同时处理多个关注点：
- "为 quest 选择 reward 并确保 bridge 到下一个 quest" → 同时涉及 `mod-reward-design` + `mod-dependency-graph`
- "确保 description 中的物品在 task 中一致" → 同时涉及 `mod-description-trust` + `mod-item-reachability`

**建议：** 添加复合场景路由：

| 我正在... | 加载模块组合 |
|---|---|
| 同时设计 task + reward + description（Step 4 常态） | mod-item-reachability + mod-reward-design + mod-description-trust §AP9-AP11 |
| 检查整体 chapter 质量 | mod-system-safety (R32) + mod-teaching-pacing (R14-R19) |

#### 遗漏 2：MP35-MP38 仍在 archive 中未分配

module-index 的 "Three Hard Problems Coverage" 表格引用 MP35-MP38，但标注 "not yet redistributed to module files"。agent 在 Step 4 需要 MP36 (Currency-as-Reward) 时须读取 archive 文件 — 而 archive 文件开头明确声明"ARCHIVED"。

**建议：** 立即将 MP35-MP38 分配到目标模块：
- MP35 (Dual-Task Automation) → `mod-teaching-pacing.md`
- MP36 (Currency-as-Reward) → `mod-reward-design.md`
- MP37 (Progress Catalog) → `mod-dependency-graph.md`
- MP38 (Reward Perception Split) → `mod-reward-design.md`（R37 已部分实现）

#### 歧义 1：mod-system-safety 的 Step 4 加载时机

module-index Step Loading Plan 将 `mod-system-safety` 标注为仅 Step 5 加载。但 R28 (Command Reward Safety) 是 **P0 级 Step 4 规则**。

**建议：** Step 4 Loading Plan 添加 "mod-reward-design §R28"（R28 的完整 pseudocode 已在 mod-reward-design 中），或加载 mod-system-safety §R28 子集。

#### 歧义 2：shared-builtin-tables 的 Step 2 条件加载

module-index 说 shared-builtin-tables 仅 Step 4/5 加载，但 Step 2 interview 讨论 stage/tier 定义时可能需要 L1 映射表作为参考。

**建议：** 添加条件加载："Step 2 讨论 stage/tier 定义时，加载 shared-builtin-tables 的 L1 映射表。"

---

## Step 4 推理步骤的可执行性

SKILL.md Step 4 包含三个强制推理步骤，逐一评估：

### 推理步骤 A：Item Reachability Reasoning

> "Walk the quest's ancestor chain and check whether the item's source dimension, tool tier, and recipe depth are all reachable from what the ancestors unlock."

**可执行性：中等 (6/10)**

| 子步骤 | 可行性 | 问题 |
|---|---|---|
| "Walk ancestor chain" | **可行** | `depends_on` 数据在 spec 中可用 |
| "source dimension" | **部分可行** | L1 覆盖 ~25 个 vanilla/ATM 物品。Mod 特有物品需要 agent 的 mod 知识（不可靠） |
| "tool tier" | **部分可行** | L1 覆盖 ~20 个工具。GregTech/Create 机器等级不在映射中 |
| "recipe depth" | **不可行** | `estimate_recipe_depth_heuristic` 未定义，agent 无法估计 |
| "reason from ancestor rewards" | **可行** | 可以从 ancestor reward 推断可用物品 |

**关键缺失：** R3 的 `estimate_recipe_depth_heuristic(id)` 是一个空函数。agent 在遇到 mod 特有物品时只能标记 `[unverified:recipe_depth]`，无法做有意义的深度估计。

**建议：** 在 SKILL.md 中添加 fallback 指引："当 L1/L2 均无数据时，根据物品名称中的 tier 关键词估计深度：ingot/dust/gear = depth 1-2, machine/circuit/controller = depth 3-4, multiblock/fusion = depth 5+。这是粗略估计，标记 `[unverified:recipe_depth]`。"

### 推理步骤 B：Reward Bridge Reasoning

> "What does this reward lead the player to do next?"

**可执行性：高 (8/10)**

| 子步骤 | 可行性 | 问题 |
|---|---|---|
| 检查 reward item 是否在 dependent quest task 中出现 | **可行** | spec 中有完整数据 |
| 识别 universal bridge types (tool/XP/currency) | **可行** | 有明确的类型列表 |
| 识别 dead-end reward | **可行** | "reward item 不在任何 dependent task 中" 是明确条件 |
| terminal quest 例外 | **可行** | "无 dependent 的 quest" 是明确条件 |

**关键优势：** 这是三个推理步骤中最具可操作性的，因为它完全基于 spec 内部数据。

**建议：** 添加 currency exception 的具体识别指引："如果 reward item 来自 `lightmanscurrency`、`gtocore` (coin items) 或自定义 currency mod，且包内有 shop/trade chapter，则跳过 dead-end check。"（此 exception 在 R10 的 cross-reference 中有提及，但 SKILL.md Step 4 未直接引用。）

### 推理步骤 C：AI Generation Self-Check (AP9/AP10/AP11)

> "Review for hallucination cascade, style homogenization, and batch narrative inconsistency."

**可执行性：中等 (5/10)**

| 子检查 | 可行性 | 问题 |
|---|---|---|
| **R23** (description-item 一致性) | **可行** | regex 匹配 + 文本比对，agent 可执行 |
| **AP10** (style drift) | **部分可行** | "与最近 2-3 quest 比较" 要求 agent 保持 context window。批量生成 chapter 时 context 可能不含前几个 quest 的完整文本 |
| **AP11** (narrative continuity) | **部分可行** | "验证 forward reference 是否匹配" — agent 需要知道 referenced quest 是否存在。但 batch 生成时后续 quest 可能还未写入 spec |

**关键问题：** AP10 和 AP11 的可行性高度依赖 agent 的 context window 是否包含同批次已生成 quest 的完整文本。在大型 chapter (50+ quests) 中，context 压力会导致 agent 无法有效比较。

**建议：**
1. AP10 改为章节级检查而非逐节点："Chapter 完成后，统计所有 description 长度标准差。若 < 10 chars，提示重新生成最相似的 entries。"
2. AP11 的 forward reference 检查改为两步：生成时标记所有 forward reference (`[forward_ref]`)，chapter 完成后批量验证。

### Chapter-level Teaching Order Check

> "Confirm that no doing-quest precedes its teaching-quest, and no high-tier quest appears before a lower-tier one."

**可执行性：中等 (6/10)**

- "教学 quest vs 实践 quest" 的分类依赖 task type + description length — 有明确 heuristic（checkmark/stat/observation + long desc = teaching）
- "同一 mod namespace" 的关联判定 — 可行但需要 agent 解析 item namespace
- "tier escalation" 的 tier 判定 — 需要 recipe depth 数据（回到 R3 的问题）

**建议：** 添加明确的分类规则："如果 quest 的 task type 是 checkmark/stat/observation 且 description >= 100 chars，分类为 teaching；如果 task type 是 item 且 count >= 1，分类为 doing。"

---

## 分层加载建议

### 当前问题：总量过大

完整规则/模式/反模式库存：
- **41 条规则** (R1-R41)
- **38 个模式** (MP1-MP38) + **7 个玩家视角** (PP1-PP7) = 45 个
- **20 个反模式** (AP1-AP20)

总计 **~106 个知识点**。agent 在单次生成中能有效应用的知识点约为 15-25 个（基于 LLM context window 和注意力衰减）。即使模块化加载，当前任何单个模块也包含 15-30 个知识点。

### 建议的三层加载架构

#### 第一层：硬约束（P0/P1，生成时必须遵守，~15 条）

这些规则阻止严重错误，应在 **每个 quest 生成时** 检查：

| 优先级 | 规则 | 检查类型 |
|---|---|---|
| P0 | R23 Description-Item Consistency | 文本匹配 |
| P0 | R7 Optional-Gate-Mandatory | 局部依赖 |
| P0 | R22 Cross-Chapter Dependency | 引用存在性 |
| P0 | R28 Command Reward Safety | 命令匹配 |
| P0 | R5 增量版 Circular Dependency | 新节点 DFS |
| P1 | R18 Description Coverage | 结构检查 |
| P1 | R10 反向版 Reward Bridge | 向后匹配 |
| P1 | R1 L1 版 Dimension-Reachability | 内置映射 |
| P1 | R16 Dimension-Explore-Then-Craft | ancestor 检查 |
| P1 | R6 局部版 Unreachable Quest | dependency 存在性 |

**加载方式：** 嵌入 SKILL.md Step 4 per-node loop，不需要额外加载模块文件。当前 SKILL.md 已部分实现（"Generation-time progression checks" 段落引用了这些规则），但建议在 SKILL.md 中直接嵌入伪代码而非引用外部模块。

#### 第二层：软约束（P2/P3，chapter 完成后批量检查，~20 条）

这些规则改善质量但不阻止严重错误，应在 **chapter batch 完成后** 统一检查：

| 优先级 | 规则 | 检查类型 |
|---|---|---|
| P2 | R10 前向版 Reward Bridge | 全量匹配 |
| P2 | R12 Reward Value Progression | chapter 统计 |
| P2 | R13 Capstone Reward Magnitude | chapter 统计 |
| P2 | R9 Dependency Depth | chapter 统计 |
| P2 | R15 Complexity Escalation | chapter 排序 |
| P2 | R19 Bottleneck Spacing | chapter 序列 |
| P2 | R31 XP-Level Relativity | reward 类型 |
| P3 | R17 Tool-Reward-Before-Use | 全量匹配 |
| P3 | R21 Hidden Quest Signpost | 可见性分析 |
| P3 | AP10 Style Homogenization | batch 统计 |
| P3 | AP11 Batch Narrative Inconsistency | NLP 交叉引用 |

**加载方式：** Step 4 chapter batch 完成后加载对应模块的相关章节。不需要逐节点加载。

#### 第三层：设计哲学（Step 2 interview 背景知识，~20 条）

这些模式/反模式影响整体设计决策，在 **Step 2 interview** 时一次性加载：

| 类型 | 内容 |
|---|---|
| 拓扑模式 | MP6-MP10 (Linear Chain, Fan-Out, Fan-In, Diamond, Island) |
| 阶段模式 | MP12 (Tier Escalation), MP19 (Chapter-as-Stage), MP21-MP22 (Dimension/Material Spine) |
| 奖励哲学 | AP8 (Reward Inflation), MP38 (Perception Split), PP2 (Backward Shortcut) |
| 信任模型 | AP1-AP8 背景知识, PP1 (Trust Contract) |
| ATM 签名 | MP4, MP16, MP20 (仅 kitchen-sink) |

**加载方式：** Step 2 interview 前加载 module-index + 相关模块的设计哲学部分。Step 4 不再加载。

### 建议的加载时机表

| 阶段 | 加载内容 | 预估 token |
|---|---|---|
| **Step 2 开始前** | module-index + mod-dependency-graph §Patterns + mod-teaching-pacing §Patterns + mod-reward-design §Philosophy (~50 lines) + mod-description-trust §AP1-AP8 summary | ~3,000 |
| **Step 4 per-node** | 第一层硬约束（嵌入 SKILL.md，不需额外加载） | 0 (已包含) |
| **Step 4 per-chapter batch** | shared-builtin-tables + mod-item-reachability §Rules + mod-reward-design §R28/R31 | ~2,000 |
| **Step 4 chapter 完成后** | 第二层软约束（mod-teaching-pacing §Rules + mod-reward-design §R10-R13 + mod-dependency-graph §R8-R9） | ~2,500 |
| **Step 5 全量验证** | 所有模块完整加载 | ~8,000 |

### 建议的优化措施

1. **将第一层硬约束直接嵌入 SKILL.md：** 当前 SKILL.md 通过引用外部模块来实现 Step 4 检查。建议在 SKILL.md Step 4 段落中直接嵌入 P0/P1 规则的伪代码（约 100 行），减少外部文件加载需求。这样 agent 在 per-node 循环中不需要加载任何模块文件。

2. **将 MP35-MP38 从 archive 分配到模块：** 消除 archive 引用带来的混乱。

3. **将不可执行的规则/模式降级：**
   - AP12, AP13 → Step 5a checklist（不是生成规则）
   - R26 完整版 → Step 5a checklist
   - PP2, MP38 → Step 2 背景知识（不是生成规则）
   - AP15 failure modes → 背景知识（R28 已覆盖可检测部分）
   - AP16 → `--adopt` mode 文档

4. **为 R3 和 R11 提供 fallback 实现：**
   - R3：添加基于名称关键词的 recipe depth 估计表
   - R11：添加 `tool_category_map` 的具体内容

5. **统一 R7 的 prose 和 pseudocode：** 消除 optional-gate-mandatory 规则中 prose 与逻辑的不一致。

---

## 总结

### 核心发现

1. **~30% 的规则在 agent 实际执行时严重降级或不可执行。** 主要集中在需要 JEI/EMI recipe 数据的规则（R1-R4 的完整版本、R5 隐式循环、AP1 recipe 层面）和需要运行时测试的规则（AP12, AP13）。当前的 L1 降级策略对 vanilla 物品有效，但对 mod 特有物品覆盖率不足。

2. **~15% 的模式过于抽象，agent 无法转化为具体 config。** 这些模式（PP2, MP23, MP30, MP38 等）是设计哲学而非可执行规则。应重新分类为"背景知识"。

3. **规则间存在 5 对优先级冲突，** 其中 R10 vs R12 和 R9 vs R19 在实际生成中会导致 agent 困惑。需要明确优先级排序。

4. **模块路由表清晰但有 4 处遗漏/歧义，** 最严重的是 mod-system-safety 的 Step 4 加载时机（R28 是 P0 Step 4 规则但模块标注为 Step 5 only）和 MP35-MP38 未从 archive 分配。

5. **Step 4 的三个推理步骤中，Reward Bridge 最具可操作性 (8/10)，Item Reachability 中等 (6/10)，AI Self-Check 最弱 (5/10)。** AI Self-Check 的可行性受限于 context window 压力。

6. **106 个知识点的总量超出 agent 单次生成能有效应用的范围。** 建议三层加载架构（硬约束 ~15 条嵌入 SKILL.md → 软约束 ~20 条 chapter 级加载 → 设计哲学 ~20 条 Step 2 一次性加载），将实际 per-node 检查缩减到 10-15 条。

### 优先级建议（按影响排序）

| 优先级 | 建议 | 影响 |
|---|---|---|
| **高** | 将 P0/P1 硬约束直接嵌入 SKILL.md Step 4，减少外部加载 | 提高 agent 执行效率和一致性 |
| **高** | 为 R3 和 R11 提供 fallback 实现（heuristic 表 + tool category 表） | 使两个当前"空函数"规则可执行 |
| **高** | 将 MP35-MP38 从 archive 分配到模块 | 消除引用混乱 |
| **中** | 明确规则优先级冲突的解决方式 | 减少 agent 困惑 |
| **中** | 修正 module-index 的 Step Loading Plan 歧义 | 确保加载时机正确 |
| **中** | 将不可执行的规则降级为 Step 5a checklist 或背景知识 | 减少无效规则对 agent 注意力的占用 |
| **低** | 为 AP10 添加具体 description 模板 | 降低 agent 创意负担 |
| **低** | 统一 R7 的 prose 和 pseudocode | 消除表述不一致 |
