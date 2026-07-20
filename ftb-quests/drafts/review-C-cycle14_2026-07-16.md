# 审查员 C — 实用性审查 (Cycle 14)

**审查日期:** 2026-07-16
**审查范围:** PP13, PP14, AP36, AP37, R82-R90
**审查方法:** 对照 SKILL.md 中 AI agent 的 Step 2/Step 4/Step 5 工作流程，评估每条规则/模式的可自动执行性

---

## 审查结论

| ID | 名称 | 评级 | 理由摘要 |
|---|---|---|---|
| PP13 | Reward-Type Contract | **SEMI-EXECUTABLE** | 奖励类型统计可自动化，但"contract"是否被打破需理解玩家交互预期 |
| PP14 | Progression-as-Reward Social Contract | **NON-EXECUTABLE** | "可感知的进度效果"需要游戏内知识，config 中无法判断 |
| AP36 | Reward-Type Roulette | **EXECUTABLE** | 纯统计检查：按 chapter 聚合奖励类型，阈值明确 |
| AP37 | Convergence Claustrophobia | **SEMI-EXECUTABLE** | 依赖数量可数，但"是否需要回溯"需要物品消费链知识 |
| R82 | Backward Design Convergence | **SEMI-EXECUTABLE** | 可检查 terminal quest 奖励是否流向最终 chapter，但"贡献 endgame"定义模糊 |
| R83 | Weak Lock Permeability | **NON-EXECUTABLE** | 判断 hard_lock/weak_lock/no_lock 需要 mod 机制知识 |
| R84 | Mid-Game Mechan Density | **EXECUTABLE** | 纯图论：计算 chapter 深度分布百分比，阈值明确 |
| R85 | Dual-Direction Reward Principle | **SEMI-EXECUTABLE** | forward 方向可查（奖励物品是否出现在下游 task），backward 方向不可查 |
| R86 | Description-as-Pathway Clarity | **EXECUTABLE** | 检查 gate quest 是否有空 description，按 pack type 调整 severity |
| R87 | Anti-Nerf Progression Respect | **NON-EXECUTABLE** | 需要知道哪些 dimension/biome 施加 debuff，无 builtin 数据源 |
| R88 | Reward-Type Contract Enforcement | **EXECUTABLE** | AP36/PP13 的形式化版本，阈值和排除项精确定义 |
| R89 | Progression-as-Reward Viability | **SEMI-EXECUTABLE** | 条件 1(空描述)和条件 3(连续 5+)可查，条件 2(解锁新内容)和 4(类型匹配)需人工 |
| R90 | Convergence Item Backtracking Safety | **SEMI-EXECUTABLE** | 可数 fan-in 数量和依赖距离，但"home chapter"定位需要合成链知识 |

**统计:** EXECUTABLE 3/12 (25%) | SEMI-EXECUTABLE 6/12 (50%) | NON-EXECUTABLE 3/12 (25%)

---

## 详细审查

### PP13 — Reward-Type Contract

- **实用性评级:** SEMI-EXECUTABLE
- **信息需求:**
  - Chapter 内每个 quest 的 reward type（spec 中已有）
  - 哪些 quest 是 tutorial quest（可从 task type 推断 — checkmark/stat task + 短 description）
  - 哪些 quest 是 chapter capstone（可从 dependency graph 推断 — fan-in 最高的 quest）
  - Loot reward 与 item reward 的 Claim All 不兼容性（已文档化为系统事实）
- **歧义点:**
  - "one primary reward delivery mechanism" — 多"primary"算 primary？如果一个 chapter 有 20 个 command reward和 3 个 item reward，command 是 primary 吗？还是任何非例外类型的混入都算违规？
  - "explicitly communicating the difference in quest descriptions" — 什么样的 description 文本算"明确沟通"？agent 无法判断描述是否充分解释了差异。
  - XP 作为"universally understood"例外的前提条件是 tutorial quest，但 PP13 没有定义 tutorial quest 的精确判定标准。
- **执行成本:**
  - Step 5 阶段：低（1-2 个推理步骤 — 按 chapter 聚合 reward type，计数 distinct types，检查是否 > 2）
  - Step 4 阶段：极低（写入奖励时检查当前 chapter 已有奖励类型是否一致）
- **建议:**
  - 增加精确定义："primary = 占 chapter 非 XP 奖励 80%+ 的类型"
  - 将"explicitly communicating"替换为可检查条件：如"description 中包含 'Note: this reward uses a different claim mechanism' 或类似关键词"
  - 定义 tutorial quest 的判定条件：`task.type in [checkmark, stat] AND description.length < 100 words`

---

### PP14 — Progression-as-Reward Social Contract

- **实用性评级:** NON-EXECUTABLE
- **信息需求:**
  - 每个 quest 完成后解锁了什么（recipe、dimension、ability） — **需要游戏内知识，config 中不可用**
  - 解锁效果是否"immediately perceivable"（5 分钟内可感知） — **纯主观判断**
  - Quest 是否仅 gate 后续 quest 而无即时回报 — 需要知道 quest 完成后的实际游戏效果
  - Stage map 和 stage_available_resources（Step 2 收集的 L2 数据） — 仅在用户提供时可用
- **歧义点:**
  - "immediately perceivable" — 5 分钟是真实时间还是游戏内时间？对于不同经验水平的玩家差异极大。
  - "visible progression effect" — 解锁一个配方算"visible"吗？如果玩家不知道这个配方有什么用呢？
  - "merge it with the next quest" — 这是设计建议，不是可检查规则。agent 在 Step 4 生成时无法判断何时应该 merge。
- **执行成本:**
  - 即使尝试部分检查也需要大量推理步骤（分析每个 quest 的 unlocks → 评估 perceivability → 判断是否需要 merge），且结论不可靠。
- **建议:**
  - 降级为 Step 2 设计指导原则（interview 阶段提醒用户考虑 zero-reward 的可行性），而非 Step 4/5 的自动检查规则。
  - 如果要保留自动检查能力，提取一个可执行的子规则："zero-reward quest 的 description 必须显式命名至少一个 unlock（recipe/dimension/ability 关键词）" — 这可以通过文本检查实现。
  - 将 "merge" 建议转化为 INFO 级别提示："连续 3+ 个 zero-reward quest 且无 branching — 考虑合并"。

---

### AP36 — Reward-Type Roulette

- **实用性评级:** EXECUTABLE
- **信息需求:**
  - 每个 quest 的 reward type 列表（spec 中已有）
  - Chapter 级别的 reward type 分布（简单聚合）
  - Pack type（kitchen-sink vs expert — Step 2 已确定）
  - Loot reward 与 item reward 的 Claim All 不兼容（系统事实，已文档化）
- **歧义点:**
  - "ONE primary reward delivery mechanism" — 与 PP13 相同的歧义，但 AP36 提供了更精确的阈值（"more than two distinct reward types"）
  - "never mix loot + item" — 绝对化表述，但 Fix (4) 又说"unless quest descriptions explicitly warn" — 到底是不允许还是允许带条件？
  - 对于 team pack 的"document in author wiki"建议 — agent 无法检查 wiki 存在性
- **执行成本:**
  - Step 5：低（1 个推理步骤 — groupby chapter, count distinct reward types, apply thresholds）
  - Step 4：极低（写入奖励时检查与 chapter 已有奖励类型是否一致）
  - 可嵌入现有的 R34 (reward type distribution) 检查流程，无额外基础设施需求
- **建议:**
  - 将 PP13 和 AP36 合并为一条可执行规则（R88 已经是这个方向），用 R88 的精确阈值取代 PP13/AP36 的散文描述
  - 统一 Fix (3) 和 Fix (4) 的矛盾：明确 loot+item 混合是 `WARNING` 无论 description 如何（因为 Claim All 是系统级问题，不受 description 影响）
  - 删除 team pack 的 wiki 建议（agent 不可执行）或改为"在 spec 的 chapter 注释中记录 reward-type policy"

---

### AP37 — Convergence Claustrophobia

- **实用性评级:** SEMI-EXECUTABLE
- **信息需求:**
  - Convergence quest 的依赖数量（spec 中可数 — `depends_on` 长度）
  - 每个依赖 quest 的 task item（spec 中已有）
  - 这些 item 是否已被消耗/可重新获取 — **需要游戏内知识**
  - 依赖 quest 是否使用了 `hide_dependency_lines`（spec 中可查）
  - Convergence quest 自身的 task item 是否是 prerequisite reward 的合成产物 — **需要合成表知识**
- **歧义点:**
  - "10+ dependencies" — 阈值明确
  - "forensic exercise" — 主观描述，不影响检查
  - "comprehensive checklist in quest description" — 可检查 description 是否包含物品列表（文本匹配），但判断列表是否"comprehensive"需要知道实际需要哪些物品
  - "items from quests that required items from other quests" — 多层嵌套的检测需要完整的合成链图，远超 spec 信息范围
- **执行成本:**
  - 可执行部分（fan-in 计数 + hide_dep_lines 检查）：低（1-2 推理步骤）
  - 不可执行部分（回溯距离评估）：需要跨 chapter 合成链知识，成本高且不可靠
- **建议:**
  - 将可执行部分提取为独立子规则：
    - "fan-in >= 10 的 convergence quest → INFO: 检查 description 是否包含物品清单"
    - "fan-in >= 10 且所有依赖都 hide_dependency_lines → WARNING: 最终汇聚路径对玩家不可见"
  - 将不可执行部分（R90 的"home chapter"距离计算）标记为 `[requires-L2-data]`，仅在用户提供 stage map 时执行
  - 将 Fix (2) "design convergence task to require only new items" 作为 Step 2 设计指导而非 Step 4 检查规则

---

### R82 — Backward Design Convergence

- **实用性评级:** SEMI-EXECUTABLE
- **信息需求:**
  - 每个 chapter 的 terminal quests（无 chapter-internal dependents 的 quest） — **可从 dependency graph 推断**
  - Terminal quest 的 reward item 是否出现在 final chapter 的 task item 中 — **可检查但需要明确"final chapter"定义**
  - Tool/ability 是否被 final chapter 间接依赖 — **需要合成链知识**
- **歧义点:**
  - "final chapter" — 是依赖深度最大的 chapter？还是用户指定的 endgame chapter？pack 可能有多个"endgame" chapter。
  - "contributes to endgame" — 直接提供物品（可查）vs 提供工具/能力（不可查）vs 教学内容（不可查）
  - "decorative chapter" 在 kitchen-sink 中标记为 INFO — 但 kitchen-sink 的 chapter 本来就大多是独立的，这条规则对 kitchen-sink 基本无意义
- **执行成本:**
  - 中等（3-5 推理步骤 — 识别 terminal quests → 提取 reward items → 扫描 final chapter tasks → 匹配）
  - 需要在 Step 5 全书验证阶段执行，不适合 Step 4 逐节点
- **建议:**
  - 明确 "final chapter" = "dependency depth 最大的 chapter 或用户通过 `endgame_chapters: [...]` 指定的 chapter"
  - 缩小检查范围：只检查 direct item match（reward item 出现在 final chapter task 中），放弃 tool/ability 的间接检查
  - Kitchen-sink pack 中标记为 `INFO — decorative chapter` 而非 `WARNING`，当前定义已正确

---

### R83 — Weak Lock Permeability

- **实用性评级:** NON-EXECUTABLE
- **信息需求:**
  - Stage gate 的位置（哪个 quest 是 stage gate） — 可从 dependency graph + stage_map 推断
  - Gate 类型（hard_lock/weak_lock/no_lock） — **需要知道是否存在 bypass 路径**
  - Bypass 的成本（5-10x resources） — **需要合成表和经济知识**
  - 是否有 Game Stages / Dimension Stages / Item Stages mod — **需要 modlist 知识**
- **歧义点:**
  - "weak lock" 的核心概念清晰（有 bypass 但成本高），但"成本高"的量化标准（5-10x）是相对于什么基准？
  - "hard_lock in kitchen-sink context may cause player frustration" — 这是设计判断，不是可自动检测的事实
  - 将 gate 分类为 hard/weak/no 需要理解 mod 机制 — 例如一个 item task 可能是 hard lock（只有特定 mod 产出该物品）也可能是 weak lock（物品可通过 villager trade 获取）
- **执行成本:**
  - 无法自动执行。即使用户提供了 stage map，agent 也无法判断 bypass 路径的存在和成本。
- **建议:**
  - 降级为 Step 2 interview 指导问题："你的 stage gate 是硬锁（Game Stages 强制）还是软锁（可绕过但成本高）？"
  - 如果保留为验证规则，改为纯 config 检查："stage gate quest 是否标记了 lock_type 属性？" — 但这需要 spec 格式扩展
  - 当前 R83 的最大价值是作为 pack reviewer 的 checklist，而非 AI agent 的自动验证规则

---

### R84 — Mid-Game Mechan Density

- **实用性评级:** EXECUTABLE
- **信息需求:**
  - 每个 chapter 的 dependency depth（从 dependency graph 计算）
  - Pack 的 total depth range（max depth - min depth）
  - Chapter 总数和各阶段分布百分比
- **歧义点:**
  - "classify each chapter as early_game, mid_game, or late_game based on dependency depth" — 分界点未精确定义。前 15% depth = early？前 25%？
  - "unusual pacing distribution" — 阈值已给出（early > 25%, late > 30%），但 25% 是按 chapter 数还是按 quest 数？
- **执行成本:**
  - 低（2-3 推理步骤 — 计算每 chapter 的 normalized depth → 分类 → 计算分布百分比 → 对比阈值）
  - 纯图论计算，不需要任何游戏内知识
- **建议:**
  - 精确定义分类标准："early_game = normalized_depth <= 0.20, mid_game = 0.20 < normalized_depth <= 0.75, late_game = normalized_depth > 0.75"
  - 明确百分比计算基于 chapter 数（不是 quest 数）
  - 考虑增加 quest-weighted 版本作为可选检查："按 quest 数加权的分布"可能更能反映实际玩家体验

---

### R85 — Dual-Direction Reward Principle

- **实用性评级:** SEMI-EXECUTABLE
- **信息需求:**
  - Forward 方向：reward item 是否出现在 dependent quest 的 task 中 — **可检查（同 R10）**
  - Backward 方向：reward item 是否"improves"已完成 quest 的生产链 — **需要理解"improve"的含义**
  - 是否处于 mid-game 或 late-game（前 20% 排除） — **可从 depth 计算**
- **歧义点:**
  - "backward_only" — "reward item upgrades an already-completed quest's production chain" 中 "upgrades" 的定义不明确。是替代配方？更快的生产？自动化升级？
  - "dual_direction" 要求同时 forward 和 backward — agent 如何判断一个物品"improves backward"？例如奖励一台粉碎机，它能加速已有矿石处理链 — 但 agent 不知道粉碎机是"升级"
  - "dead_end" 的定义与 R10 的 dead-end 检测重复，可能导致同一问题被两条规则分别报告
- **执行成本:**
  - Forward 方向：低（复用 R10 的 reward-to-dependent bridge 检查）
  - Backward 方向：不可自动执行，需要合成链知识
  - 整体：中等（如果只执行 forward 方向 + dead_end 检测）
- **建议:**
  - 将 backward 方向标记为 `[requires-L2-data]` — 仅在用户提供合成路线信息时检查
  - 保留 forward 和 dead_end 检查作为可执行部分（与 R10 合并去重）
  - 将"backward-facing utility"作为 Step 4 co-authoring 阶段的提示问题："这个奖励是否能改善玩家已有的生产线？"而非自动检查

---

### R86 — Description-as-Pathway Clarity

- **实用性评级:** EXECUTABLE
- **信息需求:**
  - Quest 是否有 gate dependency（completion unlocks new content） — **可从 dependency graph 推断（quest 有 dependents 且是唯一的 prerequisite）**
  - Quest description 是否为空或过短 — **可直接检查**
  - Pack type（expert/semi-gated vs kitchen-sink） — **Step 2 已确定**
  - Description 中是否包含 hardcoded numbers — **可通过正则匹配**
- **歧义点:**
  - "gate dependency" 的精确定义 — 是所有有 dependents 的 quest 都是 gate？还是只有"唯一 prerequisite"的 quest 才算？
  - "no description" — 是 `description: ""` 还是包括 `description: "TBD"` 等 placeholder？
  - Expert pack 的判定标准 — 用户声明即可还是需要其他指标？
- **执行成本:**
  - 低（1-2 推理步骤 — 识别 gate quests → 检查 description 长度 → 按 pack type 分配 severity）
  - 可嵌入现有的 R18 (Description Coverage) 检查流程
- **建议:**
  - 定义 "gate quest" = "至少有一个 dependent 且该 dependent 没有其他 prerequisite 的 quest"（bottleneck quest）
  - 定义 "no description" = `description 字段缺失或长度 < 10 characters`
  - 增加 placeholder 检测：`description matches /^(TBD|TODO|WIP|placeholder)/i`

---

### R87 — Anti-Nerf Progression Respect

- **实用性评级:** NON-EXECUTABLE
- **信息需求:**
  - 哪些 dimension/biome 施加 debuff（Cold Sweat 温度、Blue Skies 装备限制、Twilight Forest 进度屏障） — **需要 mod 机制知识，无 builtin 数据源**
  - Quest 是否处于 stage transition（unlock 新 dimension） — **可从 task type = dimension 推断**
  - 是否有 debuff mitigation item 作为 reward 或在 immediately-available follow-up quest 中 — **需要知道 mitigation item 是什么**
- **歧义点:**
  - "known debuff mechanics" — "known" by whom? Agent 的知识库可能不包含所有 mod 的 debuff 信息
  - "immediately-available follow-up quest" — 多"immediately"算 immediately？下一个 dependent quest？还是同一 chapter 的任何 quest？
  - 将 Blue Skies 的设备限制移除（Path of Truth 案例）是 modpack 的 KubeJS 修改 — agent 无法知道这个修改存在
- **执行成本:**
  - 即使尝试部分检查也需要维护一个 debuff dimension/biome 列表，且该列表会随 mod 版本变化
- **建议:**
  - 降级为 Step 2 interview 问题："你的 pack 中有哪些 dimension 有特殊限制（装备禁用、温度、氧气等）？"
  - 如果要保留自动检查能力，创建一个 `BUILTIN_DEBUFF_DIMENSIONS` 表（类似 `BUILTIN_DIMENSION_MAP`），但初始版本可能只覆盖 3-5 个常见 mod
  - 将 R87 的 "implementation check" 改为：当 quest 有 dimension task 且目标 dimension 在 BUILTIN_DEBUFF_DIMENSIONS 中时，检查 reward 或下一个 quest 是否提供 mitigation — 其他 dimension 标记 `[unverified:debuff]`

---

### R88 — Reward-Type Contract Enforcement

- **实用性评级:** EXECUTABLE
- **信息需求:**
  - 每个 quest 的 reward type（spec 中已有）
  - Chapter 级别的 reward type 分布（简单聚合）
  - Pack type（expert vs kitchen-sink — Step 2 已确定）
  - XP 作为 universal bridge 的排除规则（已定义）
- **歧义点:**
  - "more than two distinct reward types (excluding XP)" — 精确且无歧义
  - "mixes loot_crate rewards with item rewards" — 精确且无歧义（Claim All 不兼容的系统级事实）
  - Expert vs kitchen-sink 的 severity 差异已明确定义
- **执行成本:**
  - 低（1-2 推理步骤 — 与 AP36 相同的 groupby + count 操作）
  - 可作为 R34 (reward type distribution) 的扩展嵌入现有验证流程
- **建议:**
  - R88 是 PP13 + AP36 的最佳可执行形式。建议将 R88 作为 Step 5 的正式检查规则，PP13/AP36 作为背景知识文档
  - 增加对 `random` 和 `choice` 混合的检测（E10 #517 的具体场景 — 同一 chapter 中 random 和 choice 混用）
  - 考虑增加 spec 级别的 reward-type policy 声明：`chapters[].reward_policy: "command" | "loot" | "item" | "mixed"` — 如果声明了非 mixed 但实际混用，触发 WARNING

---

### R89 — Progression-as-Reward Viability

- **实用性评级:** SEMI-EXECUTABLE
- **信息需求:**
  - Quest 是否有 zero rewards — **可直接检查**
  - Quest description 是否为空（condition 1） — **可直接检查**
  - Quest 是否 unlock 新内容（condition 2） — **需要游戏内知识**
  - 连续 zero-reward quest 数量（condition 3） — **可从 dependency chain 计算**
  - Pack type（condition 4 — kitchen-sink/adventure vs narrative/GT/expert） — **Step 2 已确定**
- **歧义点:**
  - Condition 2 "unlocks at least one new crafting recipe, dimension, or ability" — 如何从 config 判断？unlock 可能通过 Game Stages 而非 quest reward 实现
  - Condition 3 "sequence of 5+ zero-reward quests" — 是 linear chain 还是包括 branching？如果 5 个 zero-reward quest 是并行的怎么办？
  - Condition 4 的 pack type 判定 — narrative/GT/expert 不是互斥分类，一个 pack 可能同时是 expert 和 skyblock
- **执行成本:**
  - Conditions 1, 3, 4：低（各 1 推理步骤）
  - Condition 2：不可自动执行
- **建议:**
  - 将 condition 2 标记为 `[requires-user-confirmation]` — agent 在 Step 4 co-authoring 时询问："这个 zero-reward quest 完成后玩家会解锁什么新内容？"
  - 精确定义 condition 3："linear chain 中连续 5+ zero-reward quest"（不包含 branching）
  - 增加 R50 (zero-reward safety) 的交叉引用 — R89 的 conditions 1-4 与 R50 的 3 safety conditions 有重叠，应统一

---

### R90 — Convergence Item Backtracking Safety

- **实用性评级:** SEMI-EXECUTABLE
- **信息需求:**
  - Convergence quest 的 fan-in 数量（spec 中可数 — `depends_on` 长度 >= 10）
  - 每个 required item 的 "home chapter" — **需要合成链知识**
  - Convergence quest chapter 与 farthest home chapter 的距离 — **需要 home chapter**
  - Required item 的 crafting chain 是否依赖 optional quest — **需要合成链 + optional 标记**
- **歧义点:**
  - "home chapter" — 一个物品可能在多个 chapter 中都有相关 quest。是 primary crafting chain 所在的 chapter？还是第一次出现该物品的 chapter？
  - "distance exceeds 3 chapters" — 按什么排序？Dependency depth 还是 chapter order_index？
  - "depends on any quest the player could have skipped" — 需要知道 crafting chain 中每个 item 的来源 quest 是否 optional — 这需要完整的 item→quest→optional 映射
- **执行成本:**
  - Fan-in 检测：低（1 推理步骤）
  - Home chapter 距离：高（需要跨 chapter 合成链分析，且数据不可用）
  - Optional dependency 检查：高（需要 item→quest 映射）
- **建议:**
  - 将可执行部分（fan-in >= 10 detection）作为 Step 5 的 INFO 级别提示
  - 将 home chapter 距离标记为 `[requires-L2-data]`
  - 替代方案：检查 convergence quest 的 description 是否包含所需物品列表（类似 AP37 Fix (1)） — 这是可执行的退避检查
  - 将 "depends on skippable content" 检查改为：检查 convergence quest 的 dependency chain 中是否有 optional quest — 这可以从 dependency graph + optional 标记推断，不需要合成链知识

---

## 综合评估与建议

### 1. 整体可执行性分布

Cycle 14 新增内容的可执行性明显低于 Cycle 11-13 的 topology 规则（R55-R64 几乎全部 EXECUTABLE）。这是因为 Cycle 14 的规则主要关注**玩家体验层面**（reward psychology, progression satisfaction, author intent），而非**config 结构层面**（coordinates, shapes, dependency counts）。

| 类别 | EXECUTABLE | SEMI-EXECUTABLE | NON-EXECUTABLE |
|---|---|---|---|
| Micro-patterns (PP13-PP14) | 0 | 1 | 1 |
| Anti-patterns (AP36-AP37) | 1 | 1 | 0 |
| Progression rules (R82-R90) | 2 | 4 | 3 |

### 2. 关键发现

**发现 1：R88 是 PP13 + AP36 的最佳可执行形式。** PP13 和 AP36 用散文描述了同一问题，R88 将其转化为精确的阈值检查。建议将 R88 作为 Step 5 的正式验证规则，PP13/AP36 作为设计背景文档。

**发现 2：R83/R87/R89-condition-2 共享同一瓶颈 — mod 机制知识不可用。** 这三条规则都需要知道"某个 mod 做了什么"才能判断，而 agent 的知识来源（verification ladder）止步于 item ID 和 field 验证。建议为这三条规则创建统一的 `[requires-mod-mechanics]` 标签，并在 Step 2 interview 中收集必要的 mod 机制信息。

**发现 3：R82/R85/R90 的 forward-direction 检查可复用现有 R10 基础设施。** 这三条规则都涉及"reward item 是否流向下游 task"的检查 — 这正是 R10 (Reward-to-Dependent Bridge) 的核心逻辑。建议将 forward-direction 检查统一为 R10 的扩展，而非独立实现。

**发现 4：多条规则的 kitchen-sink vs expert 区分依赖 Step 2 的 pack_type 声明。** R83/R84/R88/R89/R90 都按 pack type 调整 severity。当前 Step 2 interview 没有显式收集 `pack_type` 字段 — 它从 theme/tone 推断。建议增加显式的 `pack_type: "kitchen-sink" | "expert" | "skyblock" | "adventure" | "farming" | "narrative"` 声明。

### 3. 执行成本汇总

| 规则 | 额外推理步骤 (Step 5) | 是否需要新基础设施 |
|---|---|---|
| R84 | 2-3 | 否（复用 depth 计算） |
| R86 | 1-2 | 否（复用 description 检查） |
| R88 | 1-2 | 否（复用 R34 reward type 统计） |
| R82 | 3-5 | 需定义 "final chapter" |
| R85 | 2-3 (forward only) | 否（复用 R10） |
| R89 | 2-3 (conditions 1,3,4) | 否 |
| R90 | 1 (fan-in only) | 否 |
| R83 | N/A | 需要 mod 机制数据库 |
| R87 | N/A | 需要 debuff dimension 列表 |
| PP14 | N/A | 需要 game-stage unlock 映射 |

**总额外推理步骤（可执行部分）：** Step 5 增加约 12-18 个推理步骤，相对于现有 R1-R32 + R55-R64 的约 50-80 个步骤，增加约 20-25% 的验证开销。可接受。

### 4. 对 SKILL.md 的修改建议

如果要将 Cycle 14 可执行规则集成到 SKILL.md 工作流中：

1. **Step 2 interview:** 增加显式 `pack_type` 声明（发现 4）
2. **Step 4 per-node:** 无新增检查 — Cycle 14 规则均为 chapter-level 或 book-level，不适合逐节点
3. **Step 5 whole-book verify:** 增加 R84/R86/R88 三个 EXECUTABLE 检查，约 4-7 个额外推理步骤
4. **Step 5 advisory:** 增加 R82/R85(forward)/R89(partial)/R90(fan-in) 四个 SEMI-EXECUTABLE 的 INFO 级别提示
5. **Reference docs:** 将 PP14/R83/R87 降级为 "design philosophy" 参考文档，不进入验证 pipeline
