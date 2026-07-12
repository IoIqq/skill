## 审查员 C — 实用性质疑

> **审查日期：** 2026-07-06
> **审查范围：** progression-rules.md (26R), micro-patterns.md (32MP+7PP), anti-patterns.md (13AP), SKILL.md
> **核心问题：** AI agent 在 Step 4 生成 quest 配置时，真的能执行这些规则和模式吗？

---

### 一、可直接执行的规则/模式（无需工作流改动）

以下规则/模式在 Step 4 逐节点生成时可以被 agent 直接执行，因为它们所需的数据在生成当前节点时已经可用。

#### 1.1 规则（R）

| 规则 | 可执行原因 | 备注 |
|---|---|---|
| **R7 — Optional-Gate-Mandatory** | 只需要检查当前 quest 的直接 `dependencies` 中被依赖 quest 的 `optional` 标志。这些被依赖的 quest 要么是已有 pack 的 quest（Step 1 已索引），要么是当前生成批次中已经生成完毕的 quest。 | 完全局部检查，无需全局图遍历。 |
| **R18 — Description Coverage** | 纯结构检查：当前 quest 是否有 `description`？是否为 catalog cell？只涉及当前 quest 自身的字段。 | 逐节点即可判断。 |
| **R22 — Cross-Chapter Dependency Validity** | 检查 `dependencies` 中引用的 quest ID 是否存在。已有 pack 的 quest 在 Step 1 的 `existing_quests.json5` 中；当前批次内的 quest 在 outline 中。悬空引用可以被立即发现。 | 向后依赖（引用后面 chapter 的 quest）需要 outline 中的 chapter `order_index`，这在 Step 2 已确定。 |
| **R23 — Description-Item Consistency** | 纯正则匹配：从 `quest_desc` 提取 item ID，与当前 quest 的 `tasks`/`rewards` 中的 item ID 交叉比对。加上 `items.json5` 的存在性检查。无需任何外部数据。 | SKILL.md Step 4 的 step 6 已内置此检查。 |

#### 1.2 模式（MP）

| 模式 | 可执行原因 |
|---|---|
| **MP1 — Single-Item Gate** | 默认模式，90%+ 的 quest 都是这个模式。agent 在设计每个 quest 时默认使用。 |
| **MP2 — Multi-Item Synthesis** | 当 quest 是 synthesis/convergence 节点时（outline 中已经标注），agent 在 Step 4 为其添加 2+ item tasks。决策在 Step 2 outline 中已经做出。 |
| **MP3 — Acknowledgement Gate** | agent 在需要教学的节点处选择 checkmark/stat/observation task 类型。节点级决策。 |
| **MP4 — Escalation Ladder** | chain 结构在 Step 2 outline 中已经确定，Step 4 按 chain 递增 value 即可。 |
| **MP5 — Dimension + Item Composite** | 当一个 quest 同时需要维度探索和物品获取时，添加 dimension + item 双 task。节点级。 |
| **MP14 — Material Bridge** | 每个 reward 的 item 出现在下游 quest 的 task 中。agent 在生成当前 quest 时已经知道下游 quest 的 task（因为按依赖顺序生成，下游尚未生成，但可以反向检查：当前 quest 的 task 是否匹配祖先的 reward）。**注意：这只能做"向后检查"（当前 task 是否匹配祖先 reward），不能做"向前检查"（当前 reward 是否匹配下游 task）。** |
| **MP15 — Tool Reward** | 工具类 reward 的添加。节点级决策。 |
| **MP16 — XP Drip** | 每个 quest 加一个 XP reward。机械性添加，无决策成本。 |
| **MP27 — Fluid Task Gate** | 当 task 是流体时使用 `fluid` task 类型。节点级。 |
| **MP28 — Energy Threshold Gate** | 当 task 是能量阈值时使用 `forge_energy` task 类型。节点级。 |
| **MP29 — Command Reward** | 当 reward 需要服务端逻辑时使用 `command` reward 类型。节点级。 |
| **MP31 — Structure Discovery Gate** | 当 task 是发现结构时使用 `structure` task 类型。节点级。 |

---

### 二、需要工作流调整才能执行的

以下规则/模式在理论上可行，但在当前 SKILL.md 的 Step 4 工作流中存在具体障碍。每个条目都标注了 **当前障碍** 和 **建议的 SKILL.md 修改**。

#### 2.1 数据覆盖不足类（R1-R4）

##### R1 — Dimension-Reachability

**当前障碍：**
- L1 内置映射表 `BUILTIN_DIMENSION_MAP` 覆盖约 20-25 个物品（~17 个 vanilla + ~5 个 common mod + ~3 个 ATM signature）。
- 一个典型 kitchen-sink modpack 有 200-500 个 mod，每个 mod 贡献数十到数百个物品。L1 覆盖率 <1%。
- L2 依赖用户在 Step 2 提供 `dimension_map`，但 SKILL.md 的 Step 2 采访流程中 **没有明确要求用户提供维度-物品映射**。用户通常不会主动提供这种结构化数据。
- 对于 L1 和 L2 都未覆盖的物品，降级为 `[unverified:dimension]`，但降级后 **R1 实质上不做任何检查**——因为几乎所有 mod 物品都是 `[unverified]`。

**agent 的实际降级行为：**
1. Agent 在生成 quest 时，对 task 中的每个物品检查 `BUILTIN_DIMENSION_MAP`。
2. 如果物品是 vanilla 的 blaze_rod 或 netherite_ingot，能直接判断维度。
3. 如果物品是 `mekanism:osmium_ingot` 或 `create:brass_ingot`（不在 L1 中），agent 无法确定其维度来源，只能标记 `[unverified:dimension]`。
4. Agent 可以基于物品名称中的关键词做启发式推断（例如含 "nether" 的物品大概率来自 Nether），但这不在当前规则定义中。

**建议的 SKILL.md 修改：**
- Step 2 采访中增加一个明确的分支："你的整合包是否有维度锁定机制？如果有，请提供关键维度-物品映射（至少 20 个关键物品）。"
- 在 L1 映射表中增加 **命名空间启发式规则**：`if "nether" in item_name or "blaze" in item_name → likely the_nether`。这能将 L1 的有效覆盖从 ~25 个精确映射扩展到 ~100-200 个启发式映射。
- 将 R1 的降级行为从 `[unverified]`（跳过）改为 `[heuristic]`（基于命名推断的弱检查），并在 Step 5 验证时报告所有 `[heuristic]` 条目供人工审查。

##### R2 — Tool-Tier Item Reachability

**当前障碍：**
- `BUILTIN_TOOL_TIER_MAP` 覆盖约 12 个工具 + 8 个机器。`BUILTIN_ORE_REQUIREMENTS` 覆盖约 7 个矿石。
- 一个包含 Mekanism + Create + Immersive Engineering + Thermal 的包至少有 50+ 种工具/机器和 30+ 种矿石。覆盖率 <30%。
- 关键问题：agent 在 Step 4 生成一个 quest 时，需要知道 "祖先链中已经获得了哪些工具/机器"。这要求 agent 在生成过程中维护一个 `available_tools` 集合，并随每个 quest 的 reward 更新。SKILL.md 的 Step 4 流程 **没有明确要求 agent 维护这个状态**。

**建议的 SKILL.md 修改：**
- Step 4 的 per-node 循环中增加一个 "ancestor inventory" 追踪步骤：在生成每个 quest 之前，从 outline 的 `depends_on` 链和已生成 quest 的 reward/task 数据中收集 `available_tools` 和 `available_items` 集合。
- 将 `BUILTIN_TOOL_TIER_MAP` 扩展为 **工具类别映射**（`tool_category_map`），按功能分组而非按 tier 排序：所有 wrench 类工具归为一组，所有 pickaxe 归为一组。这能同时服务于 R2 和 R11（Wrong Tool Detection）。

##### R3 — Recipe-Chain Depth vs Dependency-Depth

**当前障碍：**
- `estimate_recipe_depth_heuristic` 基于物品名称中的关键词（"ingot"=1, "plate"=2, "processor"=3 等）估算合成深度。
- 误差范围 ±2 级。对于 kitchen-sink 包（ALLOWANCE=2），这意味着只有 **recipe_depth - quest_depth > 4** 时才会触发 WARNING——这只能捕捉极端不匹配。
- 对于 expert 包（合成链深度可达 15+），heuristic 的最大有效覆盖约 depth 8（"fusion"=6, "quantum"=6, "antimatter"=7, "creative"=10）。expert 包的核心问题恰恰在 depth 8-15 区间，heuristic 完全覆盖不到。
- 更根本的问题：agent 在生成时 **不知道 quest 的 `dependency_depth`**，因为 depth 依赖于整个依赖图。在逐节点生成时，只有已生成部分的 depth 是可计算的。

**建议的 SKILL.md 修改：**
- Step 3 scaffold 阶段应该 **预计算每个 quest 的 `dependency_depth`** 并写入 skeleton spec。这在 outline 确定后就能计算（depth = 从 root 到该 quest 的最长路径），不需要 tasks/rewards 数据。
- Step 4 在生成每个 quest 时，从 skeleton spec 中读取其 `dependency_depth`，用于 R3 的实时检查。

##### R4 — Pack-Type Stage Boundary

**当前障碍：**
- 需要用户在 Step 2 提供 `item_stage_map` 和 `stage_definition`。
- SKILL.md 的 Step 2 采访流程中 **没有明确的步骤要求用户提供阶段定义**。虽然 "Pacing" 和 "difficulty" 分支提到了阶段概念，但没有要求产出一个结构化的 `stage_definition`。
- 无 L2 数据时降级为 "cross-chapter reference check"：检查物品是否出现在更早 chapter 的 task 中。这需要所有 chapter 的数据，在 Step 4 逐节点生成时不可用（后面的 chapter 还没生成）。

**建议的 SKILL.md 修改：**
- Step 2 增加一个 "Stage Definition" 分支：根据 pack_type 自动生成一个默认 stage_definition（kitchen-sink: chapter group → stage; expert: voltage tier → stage; skyblock: resource acquisition method → stage），用户确认或修改。
- Step 4 的降级策略改为：**对于当前 quest 的 task 物品，检查该物品是否出现在当前 chapter 或已生成 chapter 的 ancestor quest 的 reward 中**。这是纯向后检查，在 Step 4 可行。

#### 2.2 图遍历依赖类（R5-R9）

##### R5 — Circular Dependency Detection

**当前障碍：**
- 标准 DFS 三色标记算法需要 **完整的依赖图**。
- Step 4 是逐节点生成的：生成 quest A 时，quest B、C、D 可能还没有生成。agent 无法在生成 A 时检测到 A→B→C→A 的循环，因为 B 和 C 还不存在。
- SKILL.md 的 Step 4 流程按 outline 的 main-line 顺序生成，这在一定程度上避免了 **显式循环**（因为 outline 中的 `depends_on` 关系已经是 DAG），但 **无法检测隐式循环**（通过 recipe graph 产生的循环——quest A 要求 mod X 的物品，该物品的 recipe 需要 mod Y 的物品，而 mod Y 的 quest 又要求 mod X 的物品）。

**关键问题：** agent 真的能在 Step 4 做图遍历吗？

答案是：**部分可以**。agent 可以维护一个 "已生成 quest 的依赖图" 并在每次添加新 quest 时增量检查循环。但这要求：
1. Agent 在内存中维护整个已生成部分的图结构。
2. 每次生成新 quest 后，对新节点执行增量 DFS。
3. 这在 context window 中是可行的（quest 数量通常 <100 per chapter），但 SKILL.md **没有指示 agent 这样做**。

**建议的 SKILL.md 修改：**
- Step 4 的 per-node 循环中增加一个 "incremental cycle check" 步骤：生成新 quest 后，检查新 quest 的 `depends_on` 链是否通过任何已生成 quest 形成回到新 quest 的回路。
- Step 5 验证时运行完整的 DFS 环检测（包括跨 chapter 引用）。
- 对于隐式循环（recipe graph 循环），标注为 `[unverified:implicit_cycle]` 并建议在 Step 5a load-test 中验证。

##### R6 — Unreachable Quest Detection

**当前障碍：**
- 需要 "所有从 root 到 Q 的路径" 的可达性分析。
- 在 Step 4 中，agent 只能确认当前 quest 的直接 `depends_on` 是否指向存在的 quest。无法确认整个路径是否可达（因为中间节点可能还没有生成完毕）。
- 特殊规则（mandatory quest 的唯一前置是 optional quest）可以在 Step 4 做局部检查。

**建议的 SKILL.md 修改：**
- Step 4 做局部检查：当前 quest 的每个 dependency 是否存在且已生成（或已有 pack 中的 quest）。
- Step 5 做全局可达性分析。

##### R8 — Dependency Requirement Consistency

**当前障碍：**
- 需要计算每个 dependency 的 `dependency_depth` 和 common ancestor。
- `dependency_depth` 可以在 Step 3 scaffold 阶段预计算（同 R3 建议）。
- "common ancestor" 需要对依赖图做 LCA（Lowest Common Ancestor）计算——这在逐节点生成时不可行。

**建议的 SKILL.md 修改：**
- Step 3 预计算 `dependency_depth`。
- Step 4 做简化检查：当一个 quest 有 >1 个 dependency 时，检查它们的 depth 差异。如果差异 ≤1 且 `dependency_requirement == "all"`，发出 INFO 提示 "这些依赖可能是并行选项，考虑 one_completed"。
- 完整 LCA 分析推迟到 Step 5。

##### R9 — Dependency Depth Reasonableness

**当前障碍：**
- 需要 chapter 内所有 quest 的 max depth。
- 在 Step 4 中，只有已生成的 quest 的 depth 可知。

**建议：** Step 3 预计算，Step 5 全局检查。Step 4 不做此检查。

#### 2.3 前向引用类（R10-R17）

这类规则的核心困难是 **生成顺序问题**：agent 按依赖顺序生成（root → leaves），生成 quest A 时，A 的下游依赖（依赖 A 的 quest B、C）还没有生成。

##### R10 — Reward-to-Dependent Bridge

**当前障碍：**
- 规则要求：quest A 的 reward 物品应出现在 A 的后继 quest（依赖 A 的 quest）的 task 中。
- 生成顺序问题：agent 先设计了 quest A 的 reward，此时 quest B（依赖 A）还没有设计 task。agent **无法知道 B 需要什么物品**。
- **但反向检查是可行的**：生成 quest B 时，B 的 task 物品应该出现在 B 的祖先 quest 的 reward 中。这个检查可以在 Step 4 做。

**建议的 SKILL.md 修改：**
- 将 R10 在 Step 4 的执行方向从 "向前检查"（reward → dependent task）改为 **"向后检查"**（task → ancestor reward）：生成每个 quest 时，检查其 task 物品是否匹配某个祖先 quest 的 reward。如果不匹配，标记为 potential dead-end 并提醒用户。
- Step 5 做完整的 "向前检查"（reward → dependent task），因为此时整个图已经生成完毕。

##### R11 — Reward-Target Accuracy (Wrong Tool Detection)

**当前障碍：**
- 需要 `tool_category_map`（按功能分组的工具映射），当前不存在。
- 需要知道后继 quest 需要什么工具，存在与 R10 相同的生成顺序问题。
- 需要从 description 文本中提取工具引用（NLP 任务），agent 可以做但精度有限。

**建议：**
- 在 Step 2 采访中要求用户提供 `tool_category_map`（至少覆盖 pack 中主要 mod 的工具类别）。
- Step 4 做反向检查（同 R10）：生成 quest B 时，检查 B 的 description 中提到的工具是否匹配某个祖先 reward 的工具。
- Step 5 做完整的前向检查。

##### R12 — Reward Value Progression

**当前障碍：**
- 需要为每个 reward 估算 "价值分"。SKILL.md 没有定义价值估算模型。
- 需要 chapter 内所有 quest 的 reward 数据。
- `estimate_value` 函数在 progression-rules.md 中只有粗略描述（"rarity × count"），没有具体实现。

**建议：**
- Step 4 不做此检查。
- Step 5 实现一个简化的价值模型：item count × tier_weight（vanilla=1, mod common=2, mod rare=5, endgame=10），检查 reward 价值是否随 dependency_depth 单调递增（允许局部波动）。

##### R13 — Capstone Reward Magnitude

**当前障碍：**
- 需要 chapter average reward value。
- 需要识别 capstone quest（dependencies ≥ 5）。capstone 的识别可以在 outline 阶段做（Step 2 已经确定了 convergence 节点）。

**建议：**
- Step 2 outline 中标记 capstone 节点。
- Step 4 生成 capstone 时，使用一个启发式规则："capstone 的 reward 至少包含 3 种不同类型的 reward（item + XP + loot/choice）"，作为 magnitude 的 proxy。
- Step 5 做精确的价值比较。

##### R14 — Teach-Then-Do Ordering

**当前障碍：**
- 需要识别 chapter 内的 "teaching quest" 和 "doing quest"。
- 在 Step 4 逐节点生成时，teaching quest 可能还没有生成（如果按 outline 顺序生成，teaching quest 通常在 doing quest 之前，但不总是如此）。

**建议的 SKILL.md 修改：**
- Step 2 outline 中标注每个 mod mechanic 的 "teaching quest" 和对应的 "doing quest"。
- Step 3 scaffold 中确保 teaching quest 的 `dependency_depth` < doing quest 的 `dependency_depth`。
- Step 4 在生成 doing quest 时，检查其依赖链中是否存在对应的 teaching quest。

##### R15 — Complexity Escalation Within Chapter

**当前障碍：**
- 需要 chapter 内所有 quest 按 dependency_depth 排序。
- 需要每个 quest 的 complexity 估算（recipe_depth × log(count + 1)）。
- 在 Step 4 中，只有已生成 quest 的数据。

**建议：** Step 5 全局检查。Step 4 不做此检查。

##### R16 — Dimension-Explore-Then-Craft Ordering

**当前障碍：**
- 需要知道 item 的维度来源（同 R1 的数据依赖问题）。
- 需要检查 ancestor quest 是否有对应的 dimension task。这在 Step 4 **可以做到**——因为 ancestor 已经生成。

**建议：** 在 Step 4 执行，但受限于 R1 的数据覆盖率。对于 L1/L2 未覆盖的物品，降级为 `[unverified]`。

##### R17 — Tool-Reward-Before-Use Ordering

**当前障碍：**
- 需要 `is_tool()` 函数来判断一个物品是否为工具。SKILL.md 没有提供工具判定标准。
- 需要知道 quest B 是否 "需要" 某个工具。这可以从 B 的 task 物品或 description 中推断。

**建议：**
- 在 L1 映射表中增加一个 `TOOL_ITEMS` 集合（常见工具物品 ID 列表）。
- Step 4 做反向检查：生成 quest B 时，如果 B 的 task 物品是一个工具，检查 B 的祖先链中是否有 quest 奖励了这个工具。

#### 2.4 节奏与统计类（R19-R21）

##### R19 — Bottleneck Spacing

**当前障碍：**
- 需要 chapter 内 quest 按 dependency_depth 排序后的序列。
- 需要定义 "bottleneck"（task count ≥ 3, item count ≥ 64, recipe depth ≥ 5）。
- 在 Step 4 中，只有已生成部分的数据。

**建议：** Step 5 全局检查。Step 4 不做此检查。

##### R20 — Chapter Completion Testability

**当前障碍：**
- 需要 chapter 内所有 non-optional quest 的完整依赖图。
- 这是 R6 的 chapter-level 版本，同样需要完整图数据。

**建议：** Step 5 全局检查。Step 4 只做局部检查（每个 quest 的 deps 是否存在）。

##### R21 — Hidden Quest Signpost

**当前障碍：**
- 需要检查 `hide_until_deps_visible` 的 quest 是否有可见的 signpost。
- "可见 signpost" 的判定需要检查 dependency quest 的 description 文本（是否包含 "unlocks"/"reveals" 等关键词）。
- 在 Step 4 中，如果 dependency quest 已经生成，可以检查其 description。如果还没生成，无法检查。

**建议：**
- Step 4 做局部检查：当前 quest 使用 `hide_until_deps_visible` 时，检查其 dependency quest（如果已生成）的 description 是否有 signpost 文本。
- Step 5 做全局检查。

#### 2.5 外部数据依赖类（R24-R26）

##### R24 — Suggestion-Reachability

**当前障碍：**
- 需要从 description 文本中识别 "建议使用" 类措辞，并提取上下文中的 item ID。
- 需要 L1 维度映射 + L2 用户映射（同 R1）。
- NLP 提取部分 agent 可以做到（正则匹配 `SUGGESTION_PATTERNS`），但 item ID 的可达性判断受限于数据覆盖。

**建议：**
- Step 4 做文本提取（正则匹配）+ L1 检查。
- 无法确认的 suggestion 标记为 `[unverified:suggestion]`。
- Step 5 做完整的可达性分析。

##### R25 — Task-Item Necessity

**当前障碍：**
- 需要了解 quest task 的物品是否有替代获取路径。
- 这需要 JEI/EMI 配方数据（L3），当前架构下完全不可用。
- 降级策略（检查 description 中是否提到替代方案但 task 不接受）可以在 Step 4 做。

**建议：**
- Step 4 只做降级的文本检查：如果 description 提到 "or"/"alternative"/"also" 等词且指向不同物品，提示 task 可能过于严格。
- 完整的替代路径分析需要外部工具（`validate_quests.py` + JEI 数据），标注为 "future work"。

##### R26 — Quest-Mod Version Consistency

**当前障碍：**
- 需要 mod 版本号 + changelog 数据。
- 当前 SKILL.md 的 Step 1 从 `extract_mods.py` 获取了 mod 版本号，但没有 changelog 数据。
- 降级策略（检测 description 中的硬编码数值）可以在 Step 4 做。

**建议：**
- Step 4 做文本提取（正则匹配硬编码数值）并标记为 `[manual-review]`。
- 完整版本一致性检查需要 packwiz/modrinth API 集成，标注为 "future work"。

#### 2.6 MP 模式选择机制缺陷

##### 缺乏显式决策树

**当前障碍：**
micro-patterns.md 的 Scope Annotation Table 标注了每个 MP 的适用 pack_type 和加载时机（Step 2/Step 4），但 **没有提供一个显式的决策树** 告诉 agent "在什么条件下选择哪个 MP"。

例如：
- 当一个 quest 需要多个物品时，应该用 MP2（Multi-Item Synthesis）还是拆成多个 MP1（Single-Item Gate）？
  - 文档说 "2+ item tasks appear at crafting-chain convergence nodes"，但没有定义 "convergence node" 的判定标准。
- 当一个 quest 是 branching point 时，应该用 MP9（Diamond）还是 MP7（Fan-Out）？
  - 文档说 MP9 需要 `dependency_requirement: "one_completed"`，但何时选择 "one_completed" vs "all" 是由 R8 决定的，而 R8 本身就需要全图数据。

**建议的 SKILL.md 修改：**
- 在 Step 4 的 per-node 循环中增加一个 "pattern selection" 步骤，包含一个简化的决策表：

```
IF quest is chapter root AND no deps → MP1 (Single-Item Gate, default)
IF quest is synthesis/convergence node (deps ≥ 3 from different mods) → MP2 (Multi-Item Synthesis)
IF quest is tutorial/teaching → MP3 (Acknowledgement Gate) + MP11 (Teach-Then-Do)
IF quest has kill/stat task with escalating chain → MP4 (Escalation Ladder)
IF quest involves dimension-gated item → MP5 (Dimension + Item Composite) + MP13 (Explore-Then-Craft)
IF quest reward is material → MP14 (Material Bridge)
IF quest reward is tool → MP15 (Tool Reward)
IF pack_type is kitchen-sink → MP16 (XP Drip) on every quest
IF quest is branching point → MP9 (Diamond) with one_completed
IF quest is capstone → MP8 (Fan-In) + MP13 (Capstone reward)
```

##### Context Window 容量问题

**当前障碍：**
- micro-patterns.md 全文约 737 行（~18,000 tokens）。
- progression-rules.md 全文约 1297 行（~30,000 tokens）。
- anti-patterns.md 全文约 324 行（~10,000 tokens）。
- 三者合计约 58,000 tokens。
- Step 4 还需要加载 SKILL.md（~630 行，~15,000 tokens）、items.json5（可能很大）、当前 chapter 的 outline 和已生成 quest 数据。
- **总计可能超过 100,000 tokens**，超出大多数模型的 context window 限制。

**建议的 SKILL.md 修改：**
- **严格分段加载**：Step 4 只加载 Part 1 (MP1-MP5, ~100 行)、Part 4 (MP14-MP18, ~60 行)、Part 7 (MP27-MP30, ~50 行) 和 Part 8 (MP31-MP32, ~30 行)。Step 2 加载 Part 2 (MP6-MP10) 和 Part 5 (MP19-MP23)。Step 5 加载 Part 6 (MP24-MP26, 作为 R 规则的索引)。
- **按需加载 R 规则**：Step 4 只加载 §0（降级策略）和 §执行优先级中标注为 "Step 4 子集" 的规则（R5/R6/R7/R10/R18/R20/R22 的局部版本）。Step 5 加载完整文档。
- **压缩 anti-patterns.md**：Step 4 只加载 AP9-AP11 的摘要（每个 AP 3-5 行），不加载完整案例。

---

### 三、无法在当前架构下执行的

以下规则/模式在当前 SKILL.md 的 5 步工作流中 **根本无法执行**，需要外部工具、运行时数据或架构级改动。

#### 3.1 需要完整 recipe graph 的规则

| 规则/模式 | 原因 | 替代方案 |
|---|---|---|
| **R5 隐式循环检测**（通过 recipe graph） | 需要 mod 的完整配方依赖图来检测 quest A 的物品 → mod X 配方 → mod Y 物品 → quest B → mod X 物品的循环。当前 items.json5 只包含物品 ID 列表，不包含配方数据。 | 外部工具：`validate_quests.py` + JEI/EMI 数据导出。或在 Step 5a load-test 中通过游戏内测试发现。 |
| **R25 完整替代路径分析** | 需要了解物品的所有获取路径（合成、掉落、交易、loot table）。当前架构无此数据。 | 标注为 "manual review" 或 "future toolchain"。 |
| **R3 expert 包深度分析** | expert 包的合成链深度可达 15+，`estimate_recipe_depth_heuristic` 的最大有效覆盖约 depth 8。 | 在 Step 2 中要求 expert 包用户提供关键物品的精确 recipe depth（L2 数据）。 |

#### 3.2 需要运行时验证的模式

| 模式 | 原因 | 替代方案 |
|---|---|---|
| **AP12 — Task-Item NBT Insensitivity** | 需要在游戏中测试 quest task 是否错误地接受不含正确 NBT 的物品。静态分析无法模拟 FTB Quests 的 NBT 匹配逻辑。 | Step 5a load-test：手动测试 NBT-bearing 物品的 quest 提交行为。 |
| **AP13 — Premature Item Submission** | 需要分析 quest 解锁时间与物品可获得时间的交叉关系。这是 FTB Quests 状态机的运行时行为，非静态配置可检测。 | Step 5a load-test：在 quest 解锁前获取 task 物品，观察 quest 状态。 |
| **AP1 的 recipe 维度**（"在熔炉中烧炼"但实际需要高炉） | 需要 JEI/EMI 配方数据来验证 description 中的合成指南是否正确。 | Step 5a load-test + 人工审查。在 Step 4 中标记 `[unverified:recipe]` 供人工检查。 |

#### 3.3 需要 batch-level 统计分析的模式

| 模式 | 原因 | 替代方案 |
|---|---|---|
| **AP10 — Style Homogenization** | 需要计算 chapter 内所有 description 的长度标准差、开头短语频率、reward 结构重复率。这是统计性检测，不是单 quest 检查。 | Step 5 增加一个 batch 统计 pass：计算 description 长度 std dev、reward 结构 entropy、shape 分布。如果 std dev < 10 chars 或 >70% reward 结构相同，触发 WARNING。 |
| **AP11 — Batch Narrative Inconsistency** | 需要跨 quest 的 description 一致性分析：forward reference 是否指向正确的 quest、difficulty claim 是否一致、tone 是否连贯。 | Step 5 增加一个 NLP pass：提取所有 forward reference（"next quest"、"you'll need this"），验证被引用的 quest 是否存在且匹配。tone 一致性需要人工审查。 |

#### 3.4 需要跨 mod 知识的检测

| 模式 | 原因 | 替代方案 |
|---|---|---|
| **PP7 — Mod-Unification Trap** | 需要知道多个 mod 是否提供同名物品、哪个 mod 的变体是 pack 的 canonical 版本。items.json5 只列出所有 item ID，不标注哪些 ID 是 "same display name, different mod"。 | Step 1 的 `extract_items.py` 可以增加一个 "duplicate display name" 检测：当多个 mod 的物品有相同的 display name 时，记录到一个 `duplicate_names.json5` 中。Step 4 在生成 task/reward 时查询此文件，提示用户选择正确的 mod 变体。 |

---

### 四、建议的执行优先级

#### 4.1 Step 4 生成时应检查的规则（嵌入 per-node 循环）

这些规则可以在生成每个 quest 时 **同步检查**，失败时立即提醒用户：

| 优先级 | 规则 | 检查类型 | 失败行为 |
|---|---|---|---|
| **P0** | R23 Description-Item Consistency | 纯文本 | ERROR — 阻止写入 spec |
| **P0** | R7 Optional-Gate-Mandatory | 局部依赖检查 | ERROR — 阻止写入 spec |
| **P0** | R22 Cross-Chapter Dependency Validity | 引用存在性 | ERROR — 阻止写入 spec |
| **P1** | R18 Description Coverage | 结构检查 | WARNING — 提醒用户 |
| **P1** | R10 (反向) Task→Ancestor Reward Bridge | 向后匹配 | WARNING — 提醒用户 |
| **P1** | R1 Dimension-Reachability (L1 only) | 内置映射检查 | `[unverified:dimension]` |
| **P1** | R16 Dimension-Explore-Then-Craft | 向后检查 ancestor dim task | WARNING |
| **P2** | R17 Tool-Reward-Before-Use (反向) | 向后检查 ancestor tool reward | INFO |
| **P2** | R2 Tool-Tier (L1 only) | 内置映射检查 | `[unverified:tool_tier]` |
| **P2** | R3 Recipe Depth (L1 heuristic) | 名称启发式 | `[unverified:recipe_depth]` |
| **P2** | R4 Stage Boundary (降级版) | 向后检查 ancestor reward | `[unverified:stage]` |
| **P2** | R24 Suggestion-Reachability (L1 only) | 正则 + L1 | `[unverified:suggestion]` |
| **P3** | AP10/AP11 self-check | 与最近 2-3 quest 比较 | INFO — style drift 提醒 |

#### 4.2 Step 5 验证时应检查的规则（全图分析）

这些规则需要完整的依赖图数据，必须在所有 quest 生成完毕后运行：

| 优先级 | 规则 | 检查类型 |
|---|---|---|
| **P0** | R5 Circular Dependency Detection (完整 DFS) | 图遍历 |
| **P0** | R6 Unreachable Quest Detection (完整可达性) | 图遍历 |
| **P0** | R20 Chapter Completion Testability | 图遍历 |
| **P1** | R7 Optional-Gate-Mandatory (全局复查) | 全量检查 |
| **P1** | R10 Reward-to-Dependent Bridge (前向检查) | 全量匹配 |
| **P1** | R11 Reward-Target Accuracy | 全量匹配 + tool_category_map |
| **P1** | R14 Teach-Then-Do Ordering | 全量 depth 比较 |
| **P1** | R16 Dimension-Explore-Then-Craft (全量) | 全量检查 |
| **P2** | R1/R2/R3/R4 (完整 L1+L2 检查) | 全量 + 用户 L2 数据 |
| **P2** | R8 Dependency Requirement Consistency | LCA 分析 |
| **P2** | R9 Dependency Depth Reasonableness | chapter-level 统计 |
| **P2** | R12 Reward Value Progression | chapter-level 统计 |
| **P2** | R13 Capstone Reward Magnitude | chapter-level 统计 |
| **P2** | R15 Complexity Escalation | chapter-level 排序 |
| **P2** | R19 Bottleneck Spacing | chapter-level 序列分析 |
| **P3** | R17 Tool-Reward-Before-Use (全量) | 全量匹配 |
| **P3** | R21 Hidden Quest Signpost | 全量可见性分析 |
| **P3** | R24/R25/R26 (完整检查) | 全量 + L2/L3 数据 |
| **P3** | AP10 Style Homogenization | batch 统计 |
| **P3** | AP11 Batch Narrative Inconsistency | NLP + 交叉引用 |

#### 4.3 需要外部脚本检查的规则

这些规则无法由 AI agent 在 Step 4 或 Step 5 中执行，需要外部工具或运行时测试：

| 规则/模式 | 所需外部工具 |
|---|---|
| **R5 隐式循环** | `validate_quests.py` + JEI/EMI recipe graph export |
| **R25 完整替代路径** | JEI/EMI 数据 + custom analysis script |
| **R26 版本一致性** | packwiz lock file / modrinth API / CurseForge API |
| **AP1 recipe 验证** | Step 5a in-game load-test |
| **AP12 NBT Insensitivity** | Step 5a in-game load-test |
| **AP13 Premature Submission** | Step 5a in-game load-test |
| **PP7 Mod-Unification** | `extract_items.py` 增加 duplicate display name 检测 |

---

### 五、SKILL.md 修改建议

#### 5.1 Step 2 采访流程修改

**增加 Stage Definition 分支：**
```
在 "Rewards & difficulty" 分支之后，增加：
- "你的整合包是否有明确的阶段划分？（维度解锁、voltage tier、resource acquisition stage 等）"
- 如果是 kitchen-sink：自动使用 chapter group → stage 映射。
- 如果是 expert：要求用户提供 voltage tier 或 age 定义。
- 如果是 skyblock：使用 resource acquisition method → stage 映射。
- 产出：`stage_definition` 写入 outline.json5。
```

**增加 Tool Category Map 分支：**
```
在 "Mods" 分支中，增加：
- "你的整合包中，哪些 mod 提供同功能的工具变体？（例如 wrench: IE hammer / Oritech wrench / Mekanism configurator / Create wrench）"
- 产出：`tool_category_map` 写入 outline.json5。
```

**增加 Dimension Map 收集：**
```
在结构讨论后，增加：
- "你的整合包中，哪些关键物品受维度锁定？请提供至少 20 个 dimension-item 映射。"
- 如果用户无法提供，使用 L1 内置映射表 + 命名空间启发式。
- 产出：`dimension_map` 写入 outline.json5。
```

#### 5.2 Step 3 Scaffold 修改

**增加 `dependency_depth` 预计算：**
```
在生成 skeleton spec 时，为每个 quest 计算 dependency_depth 并写入 spec：
{
  name: "first_plank",
  depends_on: ["punch_wood"],
  shape: "circle",
  dependency_depth: 1,  // 预计算
  tasks: [],
  rewards: []
}
```
这使得 Step 4 在生成每个 quest 时可以直接读取其 depth，用于 R3、R8、R15 等规则的实时检查。

**增加 capstone 标记：**
```
在 outline 中由用户确认的 convergence 节点，在 skeleton spec 中标记：
{
  name: "atm_star",
  depends_on: [...],
  is_capstone: true,
  dependency_depth: 5,
  tasks: [],
  rewards: []
}
```

#### 5.3 Step 4 Per-Node 循环修改

**增加 "ancestor inventory" 追踪（解决 R1/R2/R10/R16/R17 的数据可用性问题）：**
```
在 Step 4 的 step 1 ("Pick one quest") 之前，增加：
0. 维护 ancestor_inventory：
   - 从当前 quest 的 depends_on 链向上遍历，收集所有祖先 quest 的：
     - reward items（物品 ID + count）
     - task items（物品 ID）
     - dimension tasks（解锁的维度）
     - tool rewards（解锁的工具）
   - 这个集合在每次生成新 quest 时增量更新。
```

**增加 "pattern selection" 决策步骤（解决 MP 选择机制缺陷）：**
```
在 Step 4 的 step 2 ("Co-author its content") 开始时，增加：
2a. 根据当前 quest 的结构特征选择 MP 模式：
    - deps == 0 且为 chapter root → MP1 default
    - 多物品 synthesis 节点 → MP2
    - teaching/tutorial 节点 → MP3 + MP11
    - kill/stat 递增链 → MP4
    - 维度 + 物品复合 → MP5 + MP13
    - branching point → MP9
    - capstone → MP8
    将选择的模式记录在 quest 的注释中，用于 Step 5 的一致性检查。
```

**修改 R10 检查方向（解决前向引用问题）：**
```
将 Step 4 的 step 2 中的 reward bridge reasoning 从：
"reward 物品是否出现在下游 quest 的 task 中？"
改为：
"当前 quest 的 task 物品是否出现在祖先 quest 的 reward 中？"
这是反向检查，在 Step 4 可行。
前向检查（reward → dependent task）推迟到 Step 5。
```

**增加 incremental cycle check（解决 R5 的生成时检测问题）：**
```
在 Step 4 的 step 4 ("Regenerate") 之后，增加：
4a. Incremental cycle check：
    - 将新生成的 quest 加入已生成图。
    - 从新 quest 的 depends_on 出发，DFS 检查是否存在回到新 quest 的回路。
    - 如果检测到循环，ERROR 并提示用户修改 depends_on。
```

#### 5.4 Step 5 验证修改

**增加 batch-level 统计检查（解决 AP10/AP11）：**
```
在 Step 5 的 validate_quests.py 之后，增加：
5c. Batch statistics audit：
    - Description 长度标准差（< 10 chars → AP10 WARNING）
    - Reward 结构重复率（> 70% 相同 → AP10 WARNING）
    - Shape 分布 entropy（过于单一 → AP10 INFO）
    - Forward reference 验证（description 中的 "next quest" / "you'll need" 是否指向正确的 quest → AP11 WARNING）
    - Tone 一致性抽检（相邻 quest 的 description 风格是否有显著跳跃 → AP11 INFO）
```

**增加 duplicate display name 检查（解决 PP7）：**
```
在 Step 5 中增加：
5d. Mod-unification audit：
    - 从 items.json5 或 extract_items.py 的输出中，识别具有相同 display name 但不同 mod namespace 的物品。
    - 对每个 quest 的 task/reward item ID，检查是否存在同名不同 mod 的物品。
    - 如果存在，WARNING 并提示用户确认使用了正确的 mod 变体。
```

#### 5.5 文档加载策略修改

**在 SKILL.md 中明确分段加载指令：**
```
Step 2 加载：
  - design-guide.md §principles (全文)
  - micro-patterns.md Part 2 (MP6-MP10) + Part 5 (MP19-MP23) + PP1-PP7
  - anti-patterns.md AP1-AP8 (摘要)

Step 4 加载：
  - micro-patterns.md Part 1 (MP1-MP5) + Part 4 (MP14-MP18) + Part 7 (MP27-MP32)
  - progression-rules.md §0 (降级策略与内置映射)
  - anti-patterns.md AP9-AP11 (摘要，每个 3-5 行)

Step 5 加载：
  - progression-rules.md 全文
  - anti-patterns.md 全文
  - micro-patterns.md Part 6 (MP24-MP26, 作为 R 规则索引)
```

---

### 六、特别关注问题的回答

#### Q1: R1-R4 的降级策略覆盖了约 20-50 个常见物品。典型 modpack 有数百个物品。覆盖不到的物品怎么办？

**回答：** 当前设计中，覆盖不到的物品降级为 `[unverified:xxx]`，意味着 R1-R4 **对这些物品不做任何检查**。这实质上使 R1-R4 在非 vanilla 场景下成为空设规则。

改进方向：
1. **扩展 L1**：增加命名空间启发式规则（"nether"→nether, "end"→end, 等），能将有效覆盖从 ~25 个扩展到 ~100-200 个。
2. **强化 L2 收集**：Step 2 中明确要求用户提供关键物品映射，而非等待用户主动提供。
3. **降级行为升级**：将 `[unverified]` 改为 `[heuristic]`，利用 LLM 的常识做弱推断（"mekanism:osmium_ingot 大概率是 overworld 矿石"），并在 Step 5 中汇总所有 `[heuristic]` 供人工审查。

#### Q2: R5 (循环依赖检测) 需要完整的依赖图。agent 在生成时是逐 quest 生成的，怎么检测跨 quest 的循环？

**回答：** 完整的 DFS 环检测 **在 Step 4 不可行**。但增量检测是可行的：

- 每次生成新 quest Q 后，从 Q 的 `depends_on` 出发，在已生成的子图中做 DFS，检查是否存在回到 Q 的路径。
- 这能检测到所有 **涉及当前 quest 的循环**，但无法检测不涉及当前 quest 的历史循环（这些在 Step 5 中捕获）。
- 对于 outline 级别的循环（Step 2 的 `depends_on` 就已经形成环），应该在 Step 2 结束时做一次 outline-level 的环检测。

**建议：** Step 2 outline 完成后立即运行一次 outline-level 环检测；Step 4 每次生成新 quest 后做增量检测；Step 5 做完整检测。三层覆盖。

#### Q3: R10 (reward-to-dependent bridge) 要求 reward 的物品出现在下游 quest 的 task 中。但 agent 可能先设计了 quest A 的 reward，还没设计 quest B 的 task。顺序问题怎么解决？

**回答：** 这是 **生成顺序问题** 的典型体现。解决方案是 **反转检查方向**：

- **Step 4（生成时）：** 生成 quest B 时，检查 B 的 task 物品是否出现在 B 的某个祖先 quest 的 reward 中。这是向后检查，数据已可用。
- **Step 5（验证时）：** 全图生成完毕后，正向检查每个 quest 的 reward 是否出现在至少一个后继 quest 的 task 中。
- **Step 2（规划时）：** 在 outline 中标注每个 quest 的 "bridge role"（material bridge / tool bridge / XP baseline / terminal），确保 reward 设计在 Step 4 之前就有明确意图。

#### Q4: MP 的 Scope Annotation Table 标注了加载时机（Step 2/Step 4），但 agent 在 Step 4 的 context window 能容纳多少内容？2355 行全部加载是否可行？

**回答：** **不可行。** 详细估算：

| 组件 | 估计 tokens |
|---|---|
| SKILL.md | ~15,000 |
| micro-patterns.md (Part 1+4+7+8, Step 4 子集) | ~6,000 |
| progression-rules.md (§0 + Step 4 子集) | ~4,000 |
| anti-patterns.md (AP9-AP11 摘要) | ~1,500 |
| items.json5 (item ID 列表，~500 mods) | ~5,000-15,000 |
| 当前 chapter outline + 已生成 quest 数据 | ~3,000-10,000 |
| 当前 quest 的 co-author 对话历史 | ~2,000-5,000 |
| **总计** | **~36,500-56,500** |

这在 128K context window 的模型中是可行的，但在 32K 或更小的模型中会溢出。如果加载完整文档（micro-patterns 全文 + progression-rules 全文 + anti-patterns 全文），额外增加约 ~40,000 tokens，**总计将达到 76,500-96,500 tokens**，接近甚至超过许多模型的实际可用 context。

**建议：** 严格执行分段加载，Step 4 只加载必要的 Part 1+4+7+8 和 §0。将完整的 R 规则和 MP 模式留给 Step 5 验证阶段。

---

### 七、总结：当前架构的可行性评分

| 类别 | 数量 | 可直接执行 | 需工作流调整 | 无法执行 |
|---|---|---|---|---|
| **R 规则 (26)** | 26 | 4 (15%) | 18 (69%) | 4 (15%) |
| **MP 模式 (32)** | 32 | 12 (38%) | 15 (47%) | 5 (16%) |
| **PP 模式 (7)** | 7 | 2 (29%) | 3 (43%) | 2 (29%) |
| **AP (13)** | 13 | 3 (23%) | 5 (38%) | 5 (38%) |

**核心发现：**
1. **85% 的 R 规则需要工作流调整或无法在当前架构下执行。** 只有 4 条规则（R7/R18/R22/R23）可以在 Step 4 直接执行，无需任何改动。
2. **最大的障碍是数据覆盖（L1 映射表太小）和生成顺序（前向引用不可用）。** 这两个问题影响了 R1-R4、R10-R17 共 12 条规则。
3. **MP 模式的执行状况较好，** 因为 MP 主要是 "设计公式" 而非 "检查规则"。但缺乏显式决策树使得 agent 选择 MP 的过程依赖于隐式判断，容易遗漏或误选。
4. **AP 的不可执行率最高（38%），** 因为 AP 中包含了多个需要运行时验证或 batch 统计分析的模式（AP10-AP13）。
5. **Context window 是实际瓶颈。** 即使所有规则都可以通过分段加载解决，Step 4 的实际可用 context 也只能容纳约 50% 的参考文档。

**最终建议：** SKILL.md 应该将 "规则执行" 从 "生成时同步检查" 模型转向 **"生成时做 3-5 个关键检查 + 验证时做全量分析"** 的两阶段模型。Step 4 只执行 P0/P1 优先级的 ~10 个局部检查；其余推迟到 Step 5。这比试图在 Step 4 执行所有规则但每个都做得不彻底要可靠得多。
