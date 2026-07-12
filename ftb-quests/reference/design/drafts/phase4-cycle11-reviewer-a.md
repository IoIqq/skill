# Phase 4 审查员 A — 通用性审查（Cycle 11）

> 审查对象：Cycle 11 新增的所有模式和规则
> 审查角度：通用性——这些发现真的跨包适用吗？还是只基于 ATM 系列 / 少数包的数据？
> 审查文件：topology-coordinates.md, micro-patterns.md, anti-patterns.md, progression-rules.md

---

## 一、数据集基础问题（影响所有 Cycle 11 产出）

### 1.1 样本覆盖率

13 个案例覆盖 9 个包，占 57 包数据集的 16%。更严重的是案例分布不均：

| 包 | 案例数 | 占比 | 包类型 |
|---|---|---|---|
| ATM-10 | 5（basic_tools, bounty_board, basic_power, allthemodium, create） | 38% | kitchen-sink |
| Monifactory | 2（groundwork, progression） | 15% | expert |
| GregTech-Odyssey | 2（lv, stoneage） | 15% | expert |
| RAD3 | 1（milestones） | 8% | adventure |
| Finality Genesis | 1（cataclysm） | 8% | boss/adventure |
| MM2 | 1（botania） | 8% | multiblock |
| FTB Evolution | 1（create） | 8% | kitchen-sink/FTB official |
| Craftoria | 仅在文字中引用，无独立案例 | — | kitchen-sink |
| ATM-9 | 仅在汇总表中引用，无独立案例 | — | kitchen-sink |

**关键缺失：**
- 没有 skyblock 包的案例（如 SkyFactory、Stoneblock）
- 没有纯 adventure/story 包的案例（如 SevTech: Ages、RLCraft）
- 没有 create 专精包的案例（如 Create: Above and Beyond、Create: Astral）
- ATM-9 和 Craftoria 被引用但无独立案例坐标提取
- 19 个章节中 ATM-10 独占 5 个（26%），加上 ATM-9 则 ATM 系列占 31%

**影响：** 所有声称"跨包"的公式和规则都需要在此覆盖率背景下重新评估。

---

## 二、topology-coordinates.md 审查

### 2.1 六种拓扑类型分类

**通用性评分：ADAPTIVE — 基本框架合理，但穷尽性存疑**

**问题 1：是否穷尽？存在第 7 种类型吗？**

Case 10（MM2 botania）的 "Highway+Branch" 布局明显不同于现有六种类型：
- 它有一条 27.5 单位长的水平主轴（不是 linear_chain 的短链，不是 hub_fan 的辐射结构）
- 主轴上有 14 个节点等距排列（类似 parallel_columns 的等距，但方向是水平而非垂直）
- 三条独立的水平子链分布在不同 y 层级（不像 tree_branching 的层级递归）
- 文档自身承认"This topology is unique to multiblock-focused packs"

MP46 已将 Highway+Branch 正式命名为独立微模式，但拓扑分类系统没有更新。这是一个逻辑矛盾：如果它是一种独特的布局模式，它应该是第 7 种拓扑类型；如果它被归入现有类型，那它被归入了哪一种？Phase 2 的分类函数中没有任何分支会产生 "highway_branch" 结果。

MP49（Spiral/Vortex）被标注为 hub_fan 变体，但：
- 它完全没有在 13 个真实案例中被观察到
- 它来自单一中文教程（mcmod.cn post/2494）的理论描述
- 它的坐标模板是纯理论推导

**问题 2：分类函数的阈值来源不明**

```
if max_depth >= 6 and max_width <= 3: return "linear_chain"
elif has_hub and max_width >= 4: return "hub_fan"
elif max_width >= 3 and convergence_ratio < 0.1: return "parallel_columns"
elif convergence_ratio >= 0.15: return "diamond_convergence"
```

- max_depth >= 6 的阈值从何而来？5 深度的链不算 linear_chain 吗？
- convergence_ratio 的 0.1 和 0.15 两个阈值从何而来？
- has_hub 的 fan_out >= 5 阈值——为什么不是 4 或 6？
- grid_catalog 的 `max_depth <= 2 and len(quests) >= 20`——20 个任务的阈值来源？

这些阈值看起来是从 19 个章节中逆向工程出来的"刚好能区分所有样本"的数值，但它们对未见过的包是否稳健完全未知。

**建议修正：**
1. 将 Highway+Branch 正式添加为第 7 种拓扑类型，更新分类函数
2. 在每个分类阈值旁标注来源（如"基于 13 案例中 linear_chain 类型的最小 max_depth 值"）
3. 对 Spiral/Vortex，明确标注为"理论类型，未在真实数据中验证"
4. 添加 else 分支的语义：当前 default fallback 是 linear_chain，这对不符合任何类型的混合结构可能产生误导

---

### 2.2 布局算法（Phase 1-6）

**通用性评分：ADAPTIVE — 算法框架有价值但参数需标注为初步值**

**Phase 1（依赖图分析）：** 通用性良好。fan_in/fan_out/depth 是纯图论概念，不依赖特定包。

**Phase 2（拓扑分类）：** 问题见上方 2.1。

**Phase 3（坐标分配）：**
- LINEAR_CHAIN 的 `x_amplitude = 0.5` zigzag——仅 ATM-10 basic_tools 一个案例使用此模式。其他 linear_chain 案例（Monifactory progression 用 staircase Δx=1.5，GT-Odyssey stoneage 用混合链）并不使用 0.5 amplitude。
- HUB_FAN 的 `angle_step = 360 / len(children) if len(children) <= 8 else 45`——为什么是 8？为什么 else 是 45°？仅基于 ATM-10 basic_power（fan_out=3）一个案例。
- DIAMOND_CONVERGENCE 的 `sin(progress * PI)` 曲线——理论上优美，但没有验证过是否匹配 ATM-10 allthemodium 的真实坐标分布。
- TREE_BRANCHING 的 `total_width=16.0`——为什么是 16？Monifactory groundwork 跨 18.25 单位，ATM-10 create 跨 13 单位。16 是这两个数的中间值吗？
- GRID_CATALOG 的 `y_spacing = 2.5`——仅 RAD3 milestones（y=2.5）一个案例。

**Phase 4（碰撞检测）：**
- `MIN_DISTANCE = 1.0, PREFERRED_DISTANCE = 1.5`——合理，但 diagonal_bonus = 0.85 仅基于 ATM-10 basic_tools 的 zigzag。
- "10 adjustment passes"——为什么 10 次够用？没有分析过 worst case。

**Phase 5（视觉属性）：**
- Shape decision tree 的优先级顺序——基于 9 个包的观察汇总，合理但非权威。
- `"none"` shape 用于 grid_catalog——仅 RAD3 milestones 和 Craftoria create 两个案例。

**Phase 6（最终输出）：**
- viewport clamp `[-15.0, 35.0]` 和 `[-15.0, 15.0]`——x 上限 35 来自 FTB Evolution 的 x=30.0 + 5 余量。但 y clamp `[-15.0, 15.0]`（30 单位高）与 Monifactory progression 的 y 范围 [-8.5, 12.5]（21 单位）和 GT-Odyssey lv 的 16 单位高度相比，余量过大。这个 clamp 值在不同包之间差异很大。
- `hide_dependency_lines` 阈值 `local_density > 8`——仅基于 ATM-10 allthemodium 和 GT-Odyssey stoneage 两个案例。

**建议修正：**
1. 所有硬编码参数（0.5 amplitude, 8 children threshold, 16.0 total_width, 10 passes, 0.85 diagonal_bonus）旁标注 "preliminary, based on N cases"
2. Phase 3 的每种拓扑坐标分配策略标注其主要数据来源包
3. Phase 6 的 viewport clamp 改为可配置参数而非硬编码值

---

### 2.3 约束公式（Layer 2）

**通用性评分：ADAPTIVE — 公式结构合理，参数需更透明的来源标注**

**间距公式：**
```
y_spacing = clamp(base_spacing * density_factor, min_spacing, max_spacing)
density_factor = 1.0 - (quest_count - 50) * 0.005 if quest_count > 50
```
- 0.005 衰减率：50→150 任务时从 1.0 降到 0.5，使 spacing 从 1.5 降到 1.0。这个衰减率从何而来？文中说"This formula produces: 1.5 spacing for 30-quest, 1.25 for 100-quest, 1.0 for 150-quest"，但验证数据：
  - Monifactory groundwork（97 任务）使用 1.5-2.0 spacing，而公式预测 ~1.27
  - GT-Odyssey lv（129 任务）使用 1.5-2.0 spacing，而公式预测 ~1.1
  - 两个最大案例都不符合公式预测

**列间距公式：**
`column_x_gap = clamp(2.0 + column_quest_width * 0.5, 2.0, 4.0)`
- 仅 ATM-10 bounty_board（2.0）和 MM2 botania（2.0）两个数据点
- `column_quest_width` 含义不明——是单个任务的宽度还是列中任务数？

**Hub 半径公式：**
`hub_radius = clamp(3.0 + fan_out_count * 0.4, 3.5, 7.0)`
- ATM-10 basic_power：fan_out=3 → 预测 4.2，实际 5.5（偏差 31%）
- 文中自己也承认"the pack uses 5.5 for extra clearance"——公式与数据不匹配

**Size 公式：**
```
quest_size = clamp(base_size * role_multiplier, 1.0, 3.0)
```
- role_multiplier 的各值（root_hub: 2.0, convergence_3plus: 1.5-2.0, etc.）是描述性的（"我们观察到这些值"）还是规范性的（"你应该用这些值"）？文中混淆了两者。

**建议修正：**
1. 间距公式的 density_factor 衰减率需要用更多数据点验证，当前至少两个案例（Monifactory groundwork, GT-O lv）与预测不符
2. Hub 半径公式要么修正系数（0.4 → ~0.8 以匹配 basic_power 的 5.5），要么明确标注"此公式产生保守估计，实际应乘以 clearance_factor（~1.3）"
3. 所有公式添加 "Validated against: [列出具体案例]" 标注

---

### 2.4 13 个真实案例

**通用性评分：PRACTICAL — 数据本身有价值，但选择偏差需承认**

案例质量高，坐标提取方法透明。但：
- 5/13 来自 ATM-10（同一包的不同章节），存在包内同质性风险
- 没有反面案例（布局糟糕的包），所有案例都是"好的布局"
- 缺少 quest count < 6 或 > 206 的极端案例
- 缺少纯 magic、纯 adventure 章节

**建议修正：**
1. 添加 "Selection Bias Note" 段落，承认案例选择的局限性
2. 在 19 chapters from 9 packs 的描述中补充：占完整数据集（57 packs）的 16%，且 ATM-10 独占 5 个案例
3. 标注哪些包的哪些章节被排除以及排除原因（如果有）

---

## 三、micro-patterns.md 审查（MP46-MP50）

### 3.1 MP46 — Highway+Branch Topology

**通用性评分：SKIP — 样本量不足（N=1），不应作为通用模式**

- 仅基于 MM2 botania（52 quests, 27.5 unit span）一个案例
- 文中自身承认："This topology has only been observed in one pack so far; it may be specific to multiblock-centric designs"
- 坐标模板完全来自单一案例的逆向推导
- 如果这是一种真实存在的通用模式，需要在至少 3 个不同包中观察到

**建议修正：**
1. 将 MP46 从 Active 降级为 "Provisional — single-case observation"
2. 添加 TODO：需要在其他 multiblock 包（如 MBT、Enigmatica）中验证
3. 考虑将 Highway+Branch 升级为第 7 种拓扑类型（如果获得更多数据支持）

---

### 3.2 MP47 — Compartment Region Layout

**通用性评分：ADAPTIVE — 有 3 个数据点但偏向 create 章节**

- 三个来源：Craftoria Create、ATM-10 create、FTB Evolution create
- 注意：三个全是 Create mod 相关章节！这不是跨模组、跨主题验证，而是同一模组（Create）在三个不同包中的布局一致性
- 没有非 Create 章节的 compartment region 案例
- 实施指南中提到的 `ftbquests:textures/gui/toolbox_interior.png` 是 Craftoria 特有的资源路径

**建议修正：**
1. Applicable conditions 中补充："Most commonly observed in Create-focused chapters; applicability to non-Create chapters is unverified"
2. 将 "8 colored toolbox compartments" 描述从通用指南降级为 Craftoria 特定实现
3. 添加开放问题："non-Create 章节是否有使用 decorative image 分区的案例？"

---

### 3.3 MP48 — Shape Monoculture Chapter

**通用性评分：PRACTICAL — 跨包验证最充分的新模式**

- 4 个数据点：Finality Genesis cataclysm（ALL square）、RAD3 milestones（ALL none）、Monifactory groundwork（68% hexagon）、GT-Odyssey lv（~60% hexagon）
- 跨 4 个不同包、3 种包类型（boss/adventure, adventure, expert, expert）
- "approximately 40% of sampled chapters use shape monoculture"——这个比例基于 19 个章节，约 7-8 个章节，虽然绝对数量不大但占比有意义
- Shape selection guide（boss→square, catalog→none, expert→hexagon, magic→rsquare）中 magic→rsquare 仅基于 Finality Genesis ars_nouveau 一章

**建议修正：**
1. 保留 PRACTICAL 评级，但 magic→rsquare 标注为"单案例推断"
2. "40% of sampled chapters" 改为 "approximately 40% of the 19 sampled chapters (N≈8)"

---

### 3.4 MP49 — Spiral/Vortex Layout

**通用性评分：SKIP — 零真实数据支撑，纯理论模式**

- 文中自身承认："Not directly observed as a primary topology in the 19-chapter Phase 1 dataset"
- 唯一来源是 mcmod.cn post/2494 一篇教程的理论描述
- "elements of spiral arrangement appear in ATM-10 basic_power"——这是过度解读。basic_power 的 3 个 sub-hub 形成的是三角形而非螺旋
- 坐标模板完全虚构，没有任何真实坐标验证
- 分类为 "hub_fan variant" 是合理的降级，但作为独立模式列入文档过早

**建议修正：**
1. 将 MP49 从 Active 降级为 "Theoretical — not observed in dataset"
2. 坐标模板标注为"推测性模板，未经真实数据验证"
3. 添加 TODO：在实际包中搜索螺旋布局案例（可能需要检查 radial 布局的章节）
4. 考虑从 Active 文件移至 Archive 或 Theory 区，直到有真实数据支撑

---

### 3.5 MP50 — Decorative Image Waypoint

**通用性评分：SKIP — 概念模糊，与其他模式边界不清**

- MP50 与 MP47 的区分（"point-of-interest markers" vs "region backgrounds"）在实践中是否清晰？FTB Evolution create 的 27 个 icons 是 quest icons（任务图标），不是 decorative images（装饰图片）。文中将 quest icon density 和 decorative image waypoint 混为一谈
- "ATM-10 create root quest at size 3.0 acts as a waypoint even without a decorative image"——这承认了 waypoint 功能不一定需要 decorative image 来实现
- mcmod.cn post/5137 描述的是主题系统（theme system），不是 waypoint 模式
- mcmod.cn post/1416 推荐"custom images"是泛泛建议，不构成模式证据

**建议修正：**
1. 将 MP50 与 MP47 合并，或明确两者的判别标准（如"MP47 uses images as region backgrounds covering 50%+ of chapter area; MP50 uses images as point markers covering <10% of area"）
2. 移除 FTB Evolution create 的 icon density 数据作为 MP50 证据——quest icons 和 decorative images 是不同的 FTB Quests 功能
3. 降级为 "Provisional" 直到找到明确的 decorative-image-as-waypoint 案例

---

## 四、anti-patterns.md 审查（AP23-AP27）

### 4.1 AP23 — Topology Mixing

**通用性评分：PRACTICAL — 问题描述准确，修复建议可行**

- 对问题的描述（多拓扑类型混合无视觉分隔导致认知混乱）是合理的通用原则
- Craftoria Create 作为正面案例充分证明了"正确做法"
- 修复建议（decorative images、spacing gaps、shape monoculture）都是可操作的
- 唯一问题：没有反面案例（真正因为 topology mixing 而让玩家投诉的包）

**建议修正：**
1. 补充一个反面案例（如果有社区反馈提到"章节布局混乱"的 issue/discussion）
2. 或者明确标注："This anti-pattern is derived from layout analysis principles, not from specific player complaints"

---

### 4.2 AP24 — Spacing Inconsistency

**通用性评分：ADAPTIVE — 原则正确但阈值缺乏验证**

- "spacing variance within a chain exceeds 30% of the mean"——30% 阈值从哪来？这不是一个从数据中推导的值，而是一个工程经验值。
- mcmod.cn post/2494 的"长度相等、对称等原则"是泛泛的美学建议，不是量化标准
- Monifactory groundwork 作为正面案例（"consistent 1.5-2.0 spacing within clusters"）——但它自身在 cluster 间使用 4-8 units spacing，这在 cluster 内部（1.5-2.0）和 cluster 间（4-8）产生了 300%+ 的 variance。这是否违反了自己的规则？

**建议修正：**
1. 明确 "30% variance" 是 within-chain（同一链内相邻任务），不是 between-region（区域间）
2. 30% 阈值标注为"建议值，未经玩家测试验证"
3. 补充说明 cluster 间的大间距不算 spacing inconsistency（因为它是有意为之的 section break）

---

### 4.3 AP25 — Shape Semantic Conflict

**通用性评分：PRACTICAL — 问题真实存在，修复建议合理**

- Shape semantic conflict 是一个逻辑上必然存在的问题——当多个作者贡献不同章节时，没有统一 style guide 就会产生冲突
- topology-coordinates.md 的 Shape Decision Tree 提供了明确的 baseline
- 唯一问题：文档说 "gear for root hubs, diamond for convergence, pentagon for combat/boss" 是 "empirical consensus across 9 packs"，但实际上不同包有差异：
  - ATM-10 用 diamond 作为 default_quest_shape（所有非特殊任务都是 diamond）
  - Monifactory 用 hexagon 作为 default
  - Finality Genesis 用 square 作为全部
  - "diamond" 在 ATM-10 中是默认形状而非"convergence"信号

**建议修正：**
1. 在 Shape Decision Tree 中明确区分"当 diamond 是章节默认形状时"vs"当 diamond 是特殊覆盖时"的不同语义
2. 承认 shape semantics 在不同包之间确实存在差异，不存在真正的"universal consensus"，只有"common tendencies"

---

### 4.4 AP26 — Node Collision

**通用性评分：PRACTICAL — 基础几何事实，但参数需来源标注**

- 碰撞检测是布局的基础需求，通用性无可争议
- 问题在于具体参数：
  - `minimum_center_distance = 1.0`——这是基于 size=1.0 的任务。size=2.0 的任务需要更大距离，规则中也提到了，但 effective_radius 的计算方式（`size * 0.5` 或 `size * 0.35 for "none"`）来源不明
  - `diagonal_bonus = 0.85`——仅基于 ATM-10 basic_tools 的 zigzag（对角距离 ≈0.71）
  - "0.71 units is the minimum observed in shipping packs"——这是从 19 个章节中观察到的最小值，但更多章节可能产生更小的值

**建议修正：**
1. effective_radius 的计算方式标注为"推测值，需要游戏内截图验证"
2. diagonal_bonus 标注为"基于单一案例的经验值"

---

### 4.5 AP27 — Dependency Line Spaghetti

**通用性评分：PRACTICAL — 问题描述和修复建议都有充分支撑**

- mcmod.cn post/2494 的 "意识流" 警告是有社区共识的
- ATM-10 allthemodium（22/67 hide_dep_lines）和 ATM-10 basic_power（root hide_dependent_lines）提供了正面案例
- density threshold "8 quests in 3-unit radius" 的来源是 ATM-10 allthemodium + GT-Odyssey stoneage 两个案例
- 修复建议（density-based hiding, hub aggressive hiding, long-cross hiding）全部可操作

**建议修正：**
1. density threshold "8 in 3-unit radius" 标注为 "based on 2 packs; other packs may have different density tolerance"
2. 考虑将此阈值参数化，允许不同包类型使用不同值

---

## 五、progression-rules.md 审查（R55-R64）

### 5.1 R55 — Topology-Progression Mode Alignment

**通用性评分：ADAPTIVE — 映射关系合理但有未覆盖的组合**

- TOPOLOGY_MODE_ALIGNMENT 映射表看起来是手工设计的（基于设计推理而非数据统计），例如：
  - "linear_chain works best with default or linear"——合理，linear chain 天生暗示顺序推进
  - "grid_catalog only appropriate under flexible"——合理，grid 没有顺序概念
  - "diamond_convergence works with either"——合理
- 未覆盖的组合：
  - `linear_chain` + `flexible` 被列为不兼容，但 ATM-10（flexible 模式）有多个 linear_chain 章节（basic_tools）。这是否意味着 ATM-10 违反了 R55？还是 R55 的映射不完整？
  - `parallel_columns` + `default` 被列为不兼容，但 ATM-10 bounty_board（3 列 parallel columns）的 progression_mode 是什么？如果 ATM-10 是 flexible，这个案例不冲突；但如果某些包用 default + parallel columns，R55 会误报

**建议修正：**
1. 对每个映射关系标注其推理来源（"empirical" vs "design reasoning"）
2. 验证 ATM-10 basic_tools（linear_chain in flexible pack）是否构成反例
3. 添加 "soft" 级别——某些组合不推荐但可行（如 linear_chain + flexible 在 short chains 中可接受）

---

### 5.2 R56 — Depth-Axis Monotonicity

**通用性评分：PRACTICAL — 原则正确，容差值合理**

- 深度应沿主轴单调递增是一个通用的布局原则，适用于所有有方向性拓扑
- 1.0-unit tolerance 在 ATM-10 basic_tools（zigzag x ±0.5）和 Monifactory progression（完美单调）中都成立
- 仅适用于 3/6 拓扑类型（linear_chain, tree_branching, diamond_convergence），其他 3 种不适用是合理的（hub_fan 没有单主轴，parallel_columns 的各列独立，grid_catalog 无深度概念）
- 唯一问题：diamond_convergence 的 primary_axis 在伪代码中被设为 "x"，但 ATM-10 allthemodium 的 diamond 实际上是 x 和 y 同时展开的（upper branch: y=3.0-4.5, x=3.5-14; lower branch: y=-2.5, x=3.5-21; convergence: y=-5.0）。简单的 "x" 或 "y" 分类可能不够。

**建议修正：**
1. 对 diamond_convergence，考虑允许双轴检查（x 和 y 都应满足单调性，或至少主轴满足）
2. 1.0 tolerance 旁标注来源

---

### 5.3 R57 — Hub Node Size Dominance

**通用性评分：PRACTICAL — 有充分跨包验证**

- 3 个正面案例：ATM-10 basic_power（3-tier hierarchy）、Monifactory groundwork（3-tier）、ATM-10 create（root 3.0 dominates all）
- 规则逻辑简单清晰：hub.size > max(child.size)
- convergence 节点的检查（INFO 级别）比 hub 的检查（WARNING 级别）弱——这是合理的，因为 convergence 节点不一定需要视觉主导

**建议修正：**
1. 不需要修正，这是 Cycle 11 新增规则中通用性最好的之一

---

### 5.4 R58 — Collision-Free Adjacent Nodes

**通用性评分：ADAPTIVE — 核心逻辑正确但 effective_radius 计算不完整**

- effective_radius 定义：`size * 0.5 (or size * 0.35 for shape "none")`
- 问题：只定义了两种 effective_radius（标准 shape 和 "none"），但 FTB Quests 有 8+ 种 shape（hexagon, diamond, square, circle, pentagon, gear, octagon, rsquare）。不同 shape 的视觉大小不同——circle 的 effective_radius 可能比 hexagon 大（circle 外接圆 vs hexagon 内切圆），gear 因为有齿可能更大
- MIN_GAP = 0.25 的来源不明

**建议修正：**
1. 为每种 shape 定义 effective_radius 系数，或标注 "0.5 is a conservative estimate for all polygonal shapes; circle may need 0.55, gear may need 0.6"
2. 添加 "effective_radius values are approximate and need in-game visual verification"

---

### 5.5 R59 — Bounding Box Viewport Fit

**通用性评分：ADAPTIVE — 方向正确但阈值基于有限数据**

- MAX_WIDTH = 35.0 基于 FTB Evolution create 的 x=30.0 + 5 margin
- MAX_HEIGHT = 30.0 基于 Monifactory progression 的 16 units + 14 margin——这个 margin 太大了，几乎是观测值的 2 倍
- MM2 botania（27.5 宽）和 FTB Evolution create（30 宽）是两个最宽案例。如果有一个 40 单位宽的包（尚未观察到），R59 会报 WARNING，但这可能完全是合理的
- 这本质上是一个"尚未见过的数据可能超出现有边界"的问题

**建议修正：**
1. MAX_HEIGHT 从 30.0 改为 25.0（观测最大值 16 + 合理余量 9），或将 MAX_WIDTH 和 MAX_HEIGHT 都改为"基于观测最大值的 1.5 倍"的动态计算
2. 标注 "these bounds are based on the 13-case sample; packs with unusual layouts may legitimately exceed them"
3. 将 WARNING 级别保持为 WARNING（不升级为 ERROR），允许合法超出

---

### 5.6 R60 — Topology-Shape Vocabulary Coherence

**通用性评分：ADAPTIVE — 框架有洞察力但 min/max 值偏武断**

- TOPOLOGY_SHAPE_GUIDELINES 中的 min_shapes/max_shapes 值来源：
  - linear_chain max_shapes=3——ATM-10 basic_tools 用 1 种（diamond default），Monifactory progression 用 2 种（hex+square）。3 已经宽于观测
  - hub_fan min_shapes=2——合理，至少需要区分 hub 和 leaf
  - grid_catalog max_shapes=2——RAD3 milestones 用 1 种（none）。如果某个 grid 用 3 种 shape，这真的有问题吗？
- "shape diversity inversely correlates with quest count" 是一个有趣的发现，但它是一个描述性统计还是一个规范性规则？如果是描述性的，min/max 不应该太严格

**建议修正：**
1. 将 INFO 级别保持（已是 INFO），不升级为 WARNING
2. max_shapes 旁标注 "based on observed maximum for this topology type + 1"
3. 添加说明 "shape count guidelines are soft targets; exceeding them produces visual noise but not broken functionality"

---

### 5.7 R61 — Convergence Point Visual Prominence

**通用性评分：ADAPTIVE — 原则正确但 80% 阈值和单轴分类过于简化**

- 80% 阈值：convergence 节点应该在至少 80% 的父节点的"下游"。这个 80% 从何而来？为什么不 75% 或 90%？
- 仅验证了 ATM-10 allthemodium 一个案例
- ATM-10 allthemodium 的 convergence quest at (10.5, -5.0)：
  - 上分支 parents: y ≈ 3.0-4.5, x ≈ 3.5-14
  - 下分支 parents: y ≈ -2.5, x ≈ 3.5-21
  - convergence y=-5.0 < 下分支 y=-2.5（更下方 ✓）
  - convergence x=10.5 在上分支 x 范围内（3.5-14）但不在下分支 x 范围外（3.5-21）
  - 如果用 "x >= p.x" 检查：10.5 只大于约一半的 parents' x——可能不满足 80%
  - 如果用 "y >= p.y" 检查：-5.0 低于所有 parents——100% 满足

这个案例说明 80% 阈值可能需要同时考虑双轴，而不是简单的 is_horizontal / is_vertical 二选一。

**建议修正：**
1. 80% 标注为"建议值"
2. 对 diamond_convergence，考虑用双轴联合检查而非单轴
3. 补充更多 convergence 案例验证此规则

---

### 5.8 R62 — Parallel Column Spacing Uniformity

**通用性评分：SKIP — 适用范围过窄，当前仅一个验证案例**

- 仅适用于 parallel_columns 拓扑
- 仅 ATM-10 bounty_board 一个主要案例（"the cleanest parallel_columns example"）
- COLUMN_SPACING_TOLERANCE = 0.5 的来源不明
- y-start range > 1.0 的 INFO 级别检查——仅基于一个案例中 y-start 完全一致的事实

**建议修正：**
1. 规则保留但标注 "Validated against: ATM-10 bounty_board only"
2. 添加 TODO：在其他有 parallel columns 的包中验证（如 mob grinding chapters, resource collection chapters）

---

### 5.9 R63 — Grid Catalog Aspect Ratio

**通用性评分：SKIP — 仅一个验证案例，阈值缺乏支撑**

- 仅 RAD3 milestones（13.0 × 5.0, aspect 2.6:1）一个案例
- MIN_ASPECT_RATIO = 1.0 和 MAX_ASPECT_RATIO = 3.0 仅基于"2.6:1 在范围内"的反向推理
- 如果一个 grid_catalog 章节有 4:1 的宽高比（如 40 quests 在 2 行 × 20 列），R63 会报 WARNING——但这可能完全是合理的 trophy case 布局

**建议修正：**
1. 标注 "Validated against: RAD3 milestones only"
2. 考虑扩大 MAX_ASPECT_RATIO 到 4.0（允许更宽的 grid）
3. 或改为基于 quest_count 的动态比例：`max_aspect = min(3.0, quest_count / 10)`

---

### 5.10 R64 — Decorative Image Topology Alignment

**通用性评分：SKIP — 仅 Craftoria Create 一个验证案例**

- 整个规则基于 Craftoria Create 的 8 个 toolbox compartment 设计
- 30% unassigned threshold 的来源不明
- 此规则的前提条件（"chapter uses decorative images as compartments"）在 13 个案例中只出现了一次（Craftoria Create）
- 大多数包不使用 decorative images 做 compartmentalization——R64 对它们完全不适用

**建议修正：**
1. 标注 "Applicable only to packs using decorative-image compartmentalization; validated against Craftoria Create only"
2. 30% threshold 标注为"建议值"
3. 考虑添加：当 decorative images 存在但不起 compartment 作用时（纯装饰），R64 应自动 skip

---

## 六、交叉问题汇总

### 6.1 ATM-10 过度依赖

以下所有规则/模式的主要验证数据来自 ATM-10：
- 拓扑分类的 5/13 案例
- Hub radius formula（basic_power）
- Spacing formula（bounty_board）
- Collision detection（basic_tools zigzag）
- hide_dependency_lines threshold（allthemodium）
- Shape decision tree priority（多个章节）
- R55 mapping（ATM-10 flexible mode）
- R61 convergence（allthemodium）
- R62 parallel columns（bounty_board）

如果 ATM-10 的布局方式是 outlier 而非 norm（ATM-10 是 300+ mods 的超大型 kitchen-sink 包），大量规则可能不适用于其他包类型。

### 6.2 Create 章节偏向

- MP47 Compartment Region 的 3 个案例全是 Create 章节
- R64 Decorative Image Alignment 的唯一案例是 Craftoria Create
- "decorative image" 相关的所有分析都偏向 Create mod 生态

### 6.3 Expert 包偏向

- 间距公式的密度因子主要参考 Monifactory 和 GT-Odyssey
- Shape monoculture 的 4 个案例中 2 个是 expert 包
- Size hierarchy 的主要案例是 expert 包

### 6.4 缺失的包类型

以下包类型完全没有布局数据：
- Skyblock（SkyFactory, Stoneblock, Project Ozone）
- Pure adventure/story（SevTech: Ages, RLCraft, DawnCraft）
- Create 专精（Create: Above and Beyond, Create: Astral）——注意这与 kitchen-sink 中的 Create 章节不同
- Lite/minimalist 包（<20 mods）

---

## 七、总结论

### 需要修正的项目（按优先级排序）

**P0 — 必须修正（影响正确性）：**

1. **拓扑类型不穷尽**：Highway+Branch 应添加为第 7 种类型或显式标注为"已知未分类类型"
2. **Hub radius formula 与数据不匹配**：basic_power 实际 5.5 vs 公式预测 4.2，偏差 31%
3. **Spacing formula density_factor 衰减率与两个最大案例矛盾**：Monifactory groundwork 和 GT-Odyssey lv 的实际间距高于公式预测

**P1 — 应当修正（影响通用性声明的可信度）：**

4. **MP46 Highway+Branch** 从 Active 降级为 Provisional（N=1）
5. **MP49 Spiral/Vortex** 从 Active 降级为 Theoretical（N=0）
6. **MP50 Decorative Waypoint** 从 Active 降级为 Provisional 或与 MP47 合并
7. **R62、R63、R64** 标注为"单案例验证"
8. **所有硬编码阈值** 旁标注来源和验证案例数

**P2 — 建议改进（提升质量）：**

9. 添加数据集偏差声明（ATM-10 占比、Create 章节偏向、缺失包类型）
10. R58 effective_radius 补充更多 shape 类型的系数
11. R55 topology-mode mapping 添加 ATM-10 basic_tools 反例分析
12. R61 convergence 检查改为双轴联合判断
13. AP24 spacing inconsistency 的 30% 阈值添加来源标注
14. 所有公式的 "Validated against" 列表

### 不需要修正的项目

- **R57 Hub Node Size Dominance** — 通用性最好的新规则
- **AP23 Topology Mixing** — 原则正确，修复建议可行
- **AP27 Dependency Line Spaghetti** — 有多源支撑
- **MP48 Shape Monoculture** — 跨包验证最充分的新模式
- **Phase 1 Dependency Graph Analysis** — 纯图论，通用性无可争议
- **R56 Depth-Axis Monotonicity** — 原则正确，容差合理

### 整体评价

Cycle 11 的拓扑坐标研究是 FTB Quests 知识体系中的重要进展——它首次将布局设计从"感觉"提升到了可量化的层面。然而，当前版本的通用性声明超出了数据支撑的范围。13 个案例、9 个包、16% 覆盖率的数据集适合产生**假说和初步模式**，但不足以确立**通用规则和公式**。

建议在所有公式和阈值旁标注 confidence level：
- **HIGH**（3+ 包验证）：Shape Decision Tree, Size Hierarchy, Collision Min Distance
- **MEDIUM**（2 包验证）：Spacing Formula, Hub Radius, hide_dep_lines Threshold
- **LOW**（1 包验证）：Diagonal Bonus, Column Spacing, Viewport Bounds, all topology-specific rules
- **THEORETICAL**（0 包验证）：Spiral Layout, Grid Aspect Ratio bounds

这种标注能让使用者（AI 和人类）在应用这些规则时校准其信心水平。
