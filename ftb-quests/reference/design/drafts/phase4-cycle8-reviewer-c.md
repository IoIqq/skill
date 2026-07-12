# Phase 4 审查员 C — 实用性审查

> **审查日期：** Phase 4 Cycle 8
> **审查视角：** AI agent 在生成 FTB Quests 配置时能否实际执行这些规则？
> **审查范围：** R44, R45, MP39, R43, dependency_requirement, R42, Game Stages, 弱锁, 教学推入, shared-builtin-tables

---

## 可直接执行（AI 可判断）

### R45 — Reward Guidance Bridging（奖励引导衔接）

- **AI 判断方法：** 纯 quest book 结构分析。AI 在 Step 5 拥有完整的章节和任务数据：(1) 用 `find_capstone_quest(C)` 找到章节收尾任务（依赖数最多的 quest）；(2) 提取其 `item_rewards` 的物品 ID 集合；(3) 找到下一章的入口任务（无依赖或依赖全部在本章内的 quest）；(4) 提取其 `item_tasks` 的物品 ID 集合；(5) 检查两个集合的交集。无需任何外部数据。
- **建议 Step 集成：** Step 5（全量正向检查）。反向检查可在 Step 4 章节末尾执行。
- **预计推理步骤：** 5 步（找 capstone → 提取奖励 → 找入口任务 → 提取需求 → 比较交集）
- **误报率：** 低。仅在"章节完成奖励与下一章入口任务无交集且入口任务非空"时触发 WARNING。例外情况：(1) 章节间通过跨章节 `depends_on` 而非物品桥接；(2) 下一章入口任务全部是 `checkmark`/`stat` 类型（无物品需求）。建议增加例外条款：如果下一章入口任务全部为非物品类型，跳过检查。
- **SKILL.md 现状：** 已在 SKILL.md 的 Quick Reference 表中引用。Step 5 的验证脚本应包含此检查。

### R28 — Command Reward Safety Scan（命令奖励安全扫描）

- **AI 判断方法：** 纯字符串模式匹配。对 `command` 类型奖励的命令字符串，逐一比对 FORBIDDEN（`/op`, `/gamemode creative` 等）、HIGH-RISK（`/fill`, `/summon.*wither` 等）和 IDEMPOTENCY_RISK（`/give`, `/tp` 等）三个列表。完全本地数据，无需外部信息。
- **建议 Step 集成：** Step 4（已集成为 Gate 2 子门）。每生成一个 command reward 立即检查。
- **预计推理步骤：** 2 步（提取命令字符串 → 模式匹配三个列表）
- **误报率：** 极低。FORBIDDEN 列表是绝对禁止项，无误报空间。HIGH-RISK 为 WARNING 级别，允许用户覆盖。
- **SKILL.md 现状：** 已完整集成在 Step 4 Gate 2 的子门中。

### R34 — Reward Type Distribution Report（奖励类型分布报告）

- **AI 判断方法：** 遍历所有 quest 的所有 reward，统计 `type` 字段分布，计算主导类型占比。纯计数操作，无需外部数据。
- **建议 Step 集成：** Step 5（全量统计）。
- **预计推理步骤：** 3 步（遍历计数 → 找最大值 → 比较 50% 阈值）
- **误报率：** 低。INFO 级别报告 + WARNING 仅在无主导类型时触发。部分包故意混合类型（如 AoF3），WARNING 是合理的提醒而非错误判定。

### R5/R6/R7 — 依赖图结构检查（循环、不可达、可选门控必选）

- **AI 判断方法：** 纯图结构算法。R5 用 DFS 三色标记法检测循环；R6 从根节点做可达性遍历；R7 检查 mandatory quest 的 dependency 列表中是否包含 optional quest。全部无需外部数据。
- **建议 Step 集成：** R5/R6 在 Step 4（增量版，每新节点局部检查）+ Step 5（全量版）。R7 在 Step 4（P0 ERROR，阻止写入）。
- **预计推理步骤：** R5: 3 步/节点（DFS 遍历 → 检查 GRAY 节点 → 提取循环路径）。R6: 2 步/节点（检查 dependency 存在性）。R7: 2 步/节点（遍历 deps → 检查 optional 标志）。

### dependency_requirement 完整选项参考

- **AI 判断方法：** 这是文档参考，不是检查规则。AI 在生成时根据拓扑结构选择正确的 `dependency_requirement` 值：线性链用 `all_completed`（默认），分支选择用 `one_completed`，并行路径选择 N 个用 `min_required_dependencies`。
- **建议 Step 集成：** Step 4（生成时直接应用）。SKILL.md 的 Step 2 大纲设计阶段需要理解此参考以规划拓扑。
- **预计推理步骤：** 1 步（判断当前节点的依赖语义 → 选择对应值）

### R33 — Reward Table Reference Integrity（奖励表引用完整性）

- **AI 判断方法：** 这是生成器构建不变量（generator construction invariant）。AI 在生成 `type: "random"` / `"loot"` / `"choice"` 奖励时，必须同时生成对应的 reward table 文件。检查逻辑：每写一个 table 引用 → 确认对应的 reward table 文件已在同一生成 pass 中创建。纯内部一致性检查。
- **建议 Step 集成：** Step 4（生成时强制执行）。Step 5 作为安全网复查。
- **预计推理步骤：** 2 步（写奖励时检查 table 引用 → 确认 reward table 文件已生成或生成之）

### R31 — XP-Level Reward Relativity

- **AI 判断方法：** 检查 `xp_levels` 类型奖励是否仅出现在里程碑任务上。里程碑判定启发式：dependents >= 3、capstone、size > 1.5x 章节中位数、shape 为 gear/pentagon/hexagon/diamond。纯 quest book 结构分析。
- **建议 Step 集成：** Step 4（已集成为 Gate 2 子门）。
- **预计推理步骤：** 3 步（检查奖励类型 → 判定是否里程碑 → 比较）

### MP39 — Alternative-Reward Progression（替代奖励进度）— 设计决策层面

- **AI 判断方法：** MP39 是一个设计模式而非校验规则。AI 在 Step 2 采访中确定奖励哲学（guide-first vs reward-driven vs alternative-reward），记录用户选择。在 Step 4 生成时，如果用户选择了"替代奖励"路线（货币、礼包、NPC 交易），则按此模式生成奖励。在 Step 5 可做一个轻量检查：如果声明了 alternative-reward 但实际生成了大量直接物品奖励，WARNING。
- **建议 Step 集成：** Step 2（采访中确定奖励哲学）。Step 5（一致性检查）。
- **预计推理步骤：** Step 2: 1 步（记录用户选择）。Step 5: 3 步（统计奖励类型 → 对比声明 → 判断一致性）。

---

## 需要简化为启发式

### R44 — Reward-Stage Matching（奖励-阶段匹配）

- **原始要求：** 任务奖励的物品等级不应超过该任务所在阶段 +1 级。需要 `determine_stage(Q.chapter)` 和 `stage_map.get(reward.item.id)`。
- **AI 无法执行的原因：** 核心障碍是**物品阶段映射（`stage_map`）不存在于内置表中**。`shared-builtin-tables.md` 提供了维度映射、工具等级映射和合成深度启发式，但没有"物品 → 阶段"映射。AI 无法从物品 ID 推断出该物品属于哪个游戏阶段——这需要 Game Stages 配置数据或 JEI/EMI 进度链分析，两者都超出 AI agent 的能力范围。
- **简化后的启发式：** 分两层执行——
  - **L1 可用部分（mod namespace + 关键词启发式）：** 复用 `estimate_recipe_depth_heuristic` 的输出作为阶段代理。合成深度 0-1 ≈ 早期，2-3 ≈ 中期，4-6 ≈ 后期，7+ ≈ 末期。章节阶段由 `order_index` 和章节总数推算（前 25% = 早期，25-50% = 中期，50-75% = 后期，后 25% = 末期）。如果 reward 物品的估算深度 > 章节阶段 +1 级，触发 WARNING（kitchen-sink）或 ERROR（expert）。
  - **L2 用户提供：** 在 Step 2 采访中要求用户提供阶段定义表（如 "LV = 蒸汽时代, MV = 电力时代, HV = 聚变时代"），或标记关键物品的阶段归属。
- **预期准确率：** L1 启发式约 60-70%（关键词匹配对 GregTech 电压等级物品有效，对通用 mod 物品精度较低）。L2 用户提供后可达 90%+。
- **误报率：** 中等。主要误报来源：(1) 合成深度启发式将 "circuit" 标为 depth 3 但实际包中可能是 depth 1 的基础物品；(2) 章节阶段推算假设均匀分布，但实际包的章节长度差异很大。建议增加例外条款：如果用户未提供 L2 数据，R44 降级为 INFO 级别而非 WARNING/ERROR。

### R42 — Stage-Internal Item Reachability（合成链阶段内可达性）

- **原始要求：** 任务物品的完整合成链中所有原材料叶子节点，必须在当前阶段可达维度中可获得。需要 `build_recipe_tree(item)` 和 `stage_available_resources`。
- **AI 无法执行的原因：** AI agent **无法构建合成树**。没有 JEI/EMI 工具链，AI 不知道一个物品的配方是什么、配方的材料又需要什么。`shared-builtin-tables.md` 的 L1 数据仅覆盖约 20-50 个 vanilla 和标志性 mod 物品，对于一个典型的 200+ mod 包覆盖率不足 5%。
- **简化后的启发式：** 退化为 R1 + R4 的组合检查——
  - **R1 维度检查（已有 L1 数据）：** 对任务物品本身检查维度来源。如果 `BUILTIN_DIMENSION_MAP` 命中且维度不可达 → ERROR。
  - **R4 阶段边界检查（L1 启发式）：** 用 `estimate_recipe_depth_heuristic` 估算物品深度，与章节阶段比较。
  - **L1 未命中时：** 标记 `[unverified:stage_recipe]`，交给用户在 Step 5a 游戏内验证。
- **预期准确率：** 约 30-40%（仅 vanilla + ATM 系列 + 少数标志性 mod 物品可检查）。大部分物品会降级为 `[unverified:stage_recipe]`。
- **误报率：** 低（因为大部分情况降级为 unverified 而非误判）。但漏报率极高——大量真正的阶段内不可达问题会被跳过。
- **建议改进方向：** 在 Step 2 采访中增加一个可选输入项："请提供本包关键阶段的可获得资源列表（至少列出每个阶段的 5-10 个关键材料）"。这可以将覆盖率提升到 20-30%。

### R43 — Stage-Quest Causal Chain Acyclic（Stage-Quest 因果链无环）

- **原始要求：** FTB Quest 完成 → Game Stage 激活 → 配方/物品解锁的因果链必须是无环有向图。需要构建包含 Stage 节点的扩展依赖图。
- **AI 部分可执行的原因：**
  - **可执行部分：** AI 可以解析 `command` reward 字符串中的 `/gamestage add {p} <stage_name>` 模式，提取出 `quest → stage` 激活边。AI 也可以解析 `gamestage` 类型 task 中的 stage name，提取出 `stage → quest` 需求边。
  - **不可执行部分：** `required_stage = Q.required_stage or Q.chapter.required_stage` — FTB Quests 原生没有 `required_stage` 字段，阶段需求是通过 Game Stages 外部模组实现的。AI 无法知道一个 stage 解锁了哪些物品/配方/维度（这是 CraftTweaker/KubeJS 脚本的内容）。
- **简化后的启发式：** 仅检查 FTB Quests 配置层面可见的 Stage-Quest 交叉——
  1. 从所有 quest 的 `command` rewards 中提取 `/gamestage add {p} <stage>` → 构建 `quest → stage` 边
  2. 从所有 quest 的 `gamestage` tasks 中提取 `<stage>` → 构建 `stage → quest` 边
  3. 在 `quest + stage` 的双色图上运行 DFS 检测循环
  4. 仅检查这两类边的交叉循环；不检查 stage → item/recipe/dimension 的解锁边（不可见）
- **预期准确率：** 约 70-80%（对于使用 command reward + gamestage task 的包，如 Monifactory、E9E）。对于不使用 gamestage task 的包（如 GT-O 使用 dependency-implicit 方式），此检查无意义。
- **误报率：** 低。循环是结构性问题，一旦检测到基本就是真实的。但漏报存在——stage → item 解锁层面的循环不可见。

### R4 — Pack-Type Stage Boundary（包类型阶段边界）

- **原始要求：** 根据包类型，每个 quest 应处于正确的阶段区间。需要 `item_stage` 映射。
- **AI 无法执行的原因：** 与 R44 相同——缺少物品阶段映射。
- **简化后的启发式：** 同 R44 的 L1 启发式。此外，当无 L2 数据时，使用**跨章节引用交叉检查**：如果一个物品 ID 仅出现在后续章节的任务/奖励中，则当前章节可能是越界的。
- **预期准确率：** 跨章节交叉检查约 50-60%（假设同包作者的章节划分与阶段一致）。

### R3 — Recipe-Chain Depth vs Dependency-Depth

- **原始要求：** 任务物品的合成链深度不应超过 quest 依赖图深度 + ALLOWANCE(2)。需要 `recipe_depth`。
- **AI 部分可执行的原因：** `estimate_recipe_depth_heuristic` 提供基于物品名关键词的粗估，但误差 ±2 级，且仅覆盖能被关键词匹配的物品。
- **简化后的启发式：** 已内置在 `shared-builtin-tables.md` 中。对 L1 命中的物品执行检查；未命中的标记 `[unverified:recipe_depth]`。
- **预期准确率：** L1 命中时约 65-75%（关键词启发式对 GregTech 等有明确命名约定的 mod 效果好，对命名不规范的 mod 效果差）。L1 覆盖率约 20-30%。

### R2 — Tool-Tier Item Reachability

- **原始要求：** 任务物品需要的工具等级是否超过祖先链中可用的工具等级。需要 `BUILTIN_ORE_REQUIREMENTS` 和 `BUILTIN_TOOL_TIER_MAP`。
- **AI 部分可执行的原因：** L1 表覆盖了 vanilla 和 ATM 系列的工具/矿石等级。对 mod 物品的覆盖极低。
- **简化后的启发式：** 已内置。L1 命中时执行检查；未命中时降级。
- **预期准确率：** L1 命中时约 95%（vanilla 工具等级是稳定的）。覆盖率约 15-20%（仅 vanilla + ATM + Mekanism + Create 少量条目）。

### R1 — Dimension-Reachability

- **原始要求：** 任务物品是否来自祖先链已解锁的维度。需要 `BUILTIN_DIMENSION_MAP`。
- **AI 部分可执行的原因：** L1 表覆盖了 vanilla（Nether/End 物品约 15 个）+ 常见 mod 维度（Twilight Forest、Bumblezone、Undergarden）+ ATM 系列。
- **简化后的启发式：** 已内置。L1 命中时执行；未命中时降级。
- **预期准确率：** L1 命中时约 95%+（维度归属是稳定的游戏机制）。覆盖率约 20-40%（取决于包中 vanilla vs mod 物品比例）。

### 早期教学快速推入策略

- **原始要求：** 前 3-5 个任务应包含明确的教学文本，介绍包的核心差异化机制。
- **AI 部分可执行的原因：** AI 可以确保结构层面满足——前 N 个任务有描述（R18）、描述长度超过阈值、包含教学类任务类型（checkmark/stat）。但**内容质量**（是否真的传达了关键机制）需要人类判断。
- **简化后的启发式：**
  - **结构检查（AI 可执行）：** 前 N 个任务中至少有 1 个教学类型任务（checkmark/stat + 长描述）。描述长度 > 50 字符。
  - **内容检查（降级为人类审查）：** 教学文本是否覆盖了包的核心差异化机制？是否假设了玩家知道 mod 默认行为？
- **预期准确率：** 结构检查 100%（纯格式检查）。内容检查 0%（AI 无法判断教学质量）。
- **建议处理方式：** 在 Step 4 生成前 N 个任务时，AI 主动询问用户："这个包的核心差异化机制是什么？请列出 2-3 个玩家必须在前 30 分钟理解的机制。" 将用户的回答作为教学内容的素材。

---

## 无法执行（仅作为人类审查项）

### 弱锁策略（允许跳关但奖励孤立化）

- **无法执行的原因：** "弱锁"要求识别"非预期路径"——即通过非标准合成、怪物掉落、mod 交互等非任务书路径获得物品的可能性。这需要完整的 mod 交互知识（哪个怪物掉什么、哪个 mod 间交互产生什么物品），远超 AI agent 的能力。此外，"孤立化"的实现依赖 Game Stages 的 Item Stages 和 Recipe Stages 配置，这些配置在 CraftTweaker/KubeJS 脚本中，不在 FTB Quests 配置文件内。
- **建议处理方式：** 作为设计原则记录在 mod-item-reachability.md 中，供人类包作者在 Step 5a 游戏内测试时参考。在 Step 2 采访中提醒用户："如果你的包使用 Game Stages，请确认跳关获得的物品在下游用途上是否被 Stage 锁定。"

### Game Stages 运行时验证（Item/Recipe/Dimension Stages 的实际锁定效果）

- **无法执行的原因：** Game Stages 的三层锁定（Item Stages、Recipe Stages、Dimension Stages）由外部模组在游戏运行时执行，FTB Quests 配置文件无法表达这些锁定规则。AI 可以验证 FTB Quests 层面的 command reward 语法正确（`/gamestage add {p} <stage>` 格式合法），但无法验证：(1) stage name 是否在 Game Stages 配置中注册；(2) 该 stage 是否确实解锁了对应的物品/配方/维度；(3) CraftTweaker/KubeJS 脚本中的 stage→item 映射是否正确。
- **建议处理方式：** 在 Step 4 生成 command reward 时，要求用户提供 stage name 列表（在 Step 2 采访中收集）。对 stage name 做基本的格式检查（全小写、无空格、无特殊字符）。实际锁定效果在 Step 5a 游戏内测试。

### R44 的挑战绕过检查（"章节主题为困难采矿但奖励了自动寻矿符咒"）

- **无法执行的原因：** 需要理解章节的"主题"和奖励物品是否"绕过"了该主题。这需要对游戏机制的语义理解和主观判断，无法编码为自动化检查。
- **建议处理方式：** 在 Step 5 的 summary 中，对每个章节的 capstone 奖励列出物品 ID 和简要说明，让人类作者判断是否与章节主题一致。标记为 `[human-review:challenge_bypass]`。

### R42 的怪物生成限制检查

- **无法执行的原因：** R42 的完整执行需要知道"如果叶子节点需要击杀怪物获得，该怪物是否在当前可达区域生成"。怪物的生成位置、生成条件、战斗难度都不在 FTB Quests 配置中，AI 无法获取。
- **建议处理方式：** 在 Step 2 采访中，如果包使用怪物击杀作为进度门控（如 RPG 包），要求用户提供"怪物-维度-阶段"映射表。否则标记为人类审查项。

### PP7 — Mod-Unification Trap（同显示名不同 mod namespace）

- **部分可执行但建议人工：** AI 可以通过 `lookup_item.py` 发现同名物品来自不同 mod（工具已支持此功能）。但判断"哪个 mod 的变体是包的配方链规范"需要了解包的配方统一化配置（通常在 CraftTweaker/KubeJS 中），AI 无法自动判断。
- **建议处理方式：** 当 `lookup_item.py` 返回多个同名候选时，AI 列出所有候选并要求用户选择。这已经集成在 SKILL.md 的"禁止脑补"规则中。

---

## SKILL.md 集成建议

### Step 2 需要新增的检查项

#### 2A. 阶段定义收集（支持 R44, R42, R4, R43）

- **检查内容：** 在 Step 2 采访中增加"阶段定义"分支，收集：
  1. 包的阶段划分（如 "石器→铁器→钻石→下界→末地" 或 "ULV→LV→MV→HV→EV"）
  2. 每个阶段的关键可获得资源（每阶段 5-10 个物品 ID）
  3. 如果使用 Game Stages，收集 stage name 列表及其解锁的内容摘要
- **引用规则：** R44（L2 stage_map 数据源）、R42（L2 stage_available_resources 数据源）、R43（L2 stage→quest 映射数据源）
- **触发条件：** 包类型为 expert、story 或 skyblock 时强制询问；kitchen-sink 可选

#### 2B. 奖励哲学确认（支持 MP39, R34）

- **检查内容：** 确认包的主导奖励类型（item/xp/random/loot/choice）和是否存在替代奖励系统（货币、NPC 交易、礼包）
- **引用规则：** MP39、R34
- **触发条件：** 所有包类型
- **SKILL.md 现状：** 已在 Step 2 的 Rewards 分支中有部分覆盖（"Dominant reward type"）。建议增加 MP39 相关提问："你的包是否使用替代奖励系统（如货币、NPC 交易）代替直接物品奖励？"

### Step 4 需要新增的检查项

#### 4A. R44 L1 启发式检查（奖励阶段匹配）

- **检查内容：** 在 Gate 2（Reward Bridge）之后，增加 Gate 2.5（Reward Stage Match）。对每个物品奖励，使用 `estimate_recipe_depth_heuristic` 估算物品阶段，与章节阶段（由 `order_index` 推算）比较。超过 +1 级时：expert 包触发 ERROR，kitchen-sink 包触发 WARNING。
- **引用规则：** R44
- **触发条件：** 所有包类型，但 expert 包严格度更高

#### 4B. R43 增量 Stage-Quest 检查

- **检查内容：** 在生成包含 `command` reward（含 `/gamestage`）或 `gamestage` task 的 quest 时，增量检查新增的 `quest→stage` 和 `stage→quest` 边是否引入循环。
- **引用规则：** R43
- **触发条件：** 仅在 quest 包含 gamestage 相关的 command reward 或 task 时触发

### Step 5 需要新增的检查项

#### 5A. R45 全量章节桥接检查

- **检查内容：** 对每个章节（除最后一个），检查其 capstone 奖励是否与下一章入口任务有物品交集。无交集且入口任务有物品需求时触发 WARNING。
- **引用规则：** R45
- **触发条件：** 所有章节，除最后一个章节

#### 5B. R44 全量 L1+L2 检查

- **检查内容：** 如果用户在 Step 2 提供了 L2 stage_map，对所有物品奖励和任务物品执行完整的阶段匹配检查。未提供 L2 时仅执行 L1 启发式版本。
- **引用规则：** R44
- **触发条件：** 所有包类型

#### 5C. R43 全量 Stage-Quest 交叉图遍历

- **检查内容：** 从所有 quest 的 command rewards 和 gamestage tasks 中提取完整的 Stage-Quest 边，构建扩展图，运行 DFS 检测循环。
- **引用规则：** R43
- **触发条件：** 仅在包包含 gamestage command rewards 或 gamestage tasks 时（expert/story 包常见）

#### 5D. MP39 一致性检查

- **检查内容：** 如果用户在 Step 2 声明了替代奖励系统，检查实际生成的奖励中直接物品奖励的占比是否超过 50%。超过时 WARNING："声明了替代奖励系统，但直接物品奖励占比过高。"
- **引用规则：** MP39、R34
- **触发条件：** 仅在 Step 2 声明了 alternative-reward 时

---

## shared-builtin-tables.md 扩展建议

### 当前 L1 数据覆盖缺口

| 数据表 | 当前覆盖 | 缺口 | 建议扩展方向 |
|---|---|---|---|
| `BUILTIN_DIMENSION_MAP` | ~20 物品 (vanilla + TF + Bumblezone + Undergarden + ATM) | 缺少 AE2/Botania/Immersive Engineering 等常见 mod 的维度物品 | 可考虑增加，但需谨慎——mod 维度归属可能因包而异 |
| `BUILTIN_TOOL_TIER_MAP` | ~15 条目 (vanilla + ATM + Mekanism + Create) | 缺少 Tinkers' Construct、Immersive Engineering 等工具 tier | 扩展价值中等，tool tier 在不同包中可能不同 |
| `BUILTIN_ORE_REQUIREMENTS` | ~10 条目 (vanilla + ATM) | 覆盖面极窄 | 扩展价值低——矿石挖掘等级在不同包中一致（vanilla tag 体系），但 mod 矿石的等级不在 vanilla tag 中 |
| `estimate_recipe_depth_heuristic` | ~20 关键词 | 缺少 mod 特有命名（如 Mekanism 的 "enriched"、AE2 的 "press"、GregTech 的电压前缀） | **高优先级扩展**——增加 GregTech 电压命名（lv_/mv_/hv_/ev_ 前缀 → 对应深度）、Mekanism enriched/ingot → depth 映射、AE2 press/cell → depth 映射 |

### 建议新增：BUILTIN_STAGE_PROXY（阶段代理估算表）

为支持 R44 的 L1 执行，建议新增一个"物品 → 粗略阶段"映射表，作为 `stage_map` 的 L1 降级。与 `estimate_recipe_depth_heuristic` 不同，此表直接映射特定物品 ID 到阶段名称（而非深度数值）：

```
BUILTIN_STAGE_PROXY = {
    # Vanilla progression
    "minecraft:iron_ingot":       "early",
    "minecraft:diamond":          "mid",
    "minecraft:netherite_ingot":  "late",
    "minecraft:ender_pearl":      "late",
    "minecraft:dragon_egg":       "endgame",
    # ATM series
    "allthemodium:allthemodium_ingot":  "mid",
    "allthemodium:vibranium_ingot":     "late",
    "allthemodium:unobtainium_ingot":   "endgame",
    # Mekanism (rough)
    "mekanism:ingot_osmium":      "early",
    "mekanism:ingot_refined_glowstone": "mid",
    "mekanism:ingot_refined_obsidian":  "late",
    # GregTech voltage tiers (prefix-based, not item-specific)
    # Handled by estimate_recipe_depth_heuristic keyword match
}
```

这个表的精度低于 L2 用户提供的 stage_map，但可以让 R44 在无 L2 数据时仍然对 30-50 个常见物品执行有意义的阶段匹配检查。

---

## 总结：可执行性矩阵

| 规则 | 可执行性 | 主要瓶颈 | 建议处理方式 |
|---|---|---|---|
| R44 | 部分（L1 启发式） | 缺少 stage_map | L1 启发式 + Step 2 收集 L2 |
| R45 | 完全 | 无 | Step 5 直接执行 |
| MP39 | 设计决策 | 无（Step 2 采访） | Step 2 + Step 5 一致性检查 |
| R43 | 部分（command 解析） | 缺少 stage→item 解锁数据 | 增量 + 全量双色图 DFS |
| dependency_requirement | 完全（文档参考） | 无 | Step 4 生成时应用 |
| R42 | 极少 | 无法构建合成树 | 退化为 R1+R4 组合 + `[unverified]` |
| Game Stages | 语法层面可 | 运行时验证不可 | Step 2 收集 stage names + Step 4 语法检查 |
| 弱锁 | 不可 | 需要 mod 交互全貌 | 人类审查项 |
| 教学推入 | 结构层面可 | 内容质量不可 | 结构检查 + Step 2 收集教学素材 |
| shared-builtin-tables | 部分（覆盖不足） | L1 数据量有限 | 扩展关键词表 + 新增 BUILTIN_STAGE_PROXY |

**关键发现：** 审查范围内的规则可以分为三类——(1) 纯 quest book 结构分析（R45, R5/R6/R7, R28, R34），这些完全可以由 AI 执行，不需要任何外部数据；(2) 需要物品阶段/配方数据的检查（R44, R42, R43, R4, R3, R2, R1），AI 只能在 L1 内置表命中的范围内执行，大部分降级为 `[unverified]`，**提升覆盖率的关键手段是在 Step 2 采访中收集 L2 数据**；(3) 需要游戏运行时知识的检查（弱锁、Game Stages 运行时、挑战绕过），只能作为人类审查项。

**最重要的 SKILL.md 修改建议：** 在 Step 2 采访中增加"阶段定义"分支（收集 stage_map 和 stage names），这将直接提升 R44/R42/R43 的可执行覆盖率从 ~20-40% 到 ~60-80%。这是一个高投入产出比的改进——多问 3-5 个问题，换来 6 条规则的执行精度翻倍。
