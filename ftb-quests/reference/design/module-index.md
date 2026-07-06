# FTB Quests Design Reference — Module Index

> 本索引是模块化参考系统的路由表。AI agent 根据当前工作场景加载对应模块。

## Modules

| Module | Core Question | Lines | Step 2 | Step 4 | Step 5 |
|---|---|---|---|---|---|
| [shared-builtin-tables.md](shared-builtin-tables.md) | L1 内置映射表 | ~153 | — | ✔ | ✔ |
| [mod-item-reachability.md](mod-item-reachability.md) | 玩家拿得到这个物品吗？ | ~304 | — | ✔ | ✔ |
| [mod-dependency-graph.md](mod-dependency-graph.md) | 任务怎么连接？图健康吗？ | ~303 | ✔ (partial) | — | ✔ |
| [mod-reward-design.md](mod-reward-design.md) | 奖励什么？引导去哪？ | ~235 | ✔ (philosophy) | ✔ | ✔ |
| [mod-teaching-pacing.md](mod-teaching-pacing.md) | 教学在测试之前吗？ | ~202 | ✔ (partial) | ✔ (review) | ✔ |
| [mod-description-trust.md](mod-description-trust.md) | 描述文本准确吗？ | ~147 | ✔ (AP1-AP8 bg) | ✔ (AP9-11) | ✔ |
| [mod-system-safety.md](mod-system-safety.md) | 配置安全/兼容吗？ | ~157 | — | — | ✔ |
| [mod-atm-signature.md](mod-atm-signature.md) | ATM 专属还是通用？ | ~115 | ✔ (if kitchen-sink) | — | — (unless ATM) |

## Scenario → Module Routing

| 我正在... | 加载这个模块 |
|---|---|
| 设计 quest 的 tasks（要什么物品） | mod-item-reachability |
| 连接 quests 之间的依赖 | mod-dependency-graph |
| 选择 quest 的 reward | mod-reward-design |
| 排列 quests 在 chapter 中的顺序 | mod-teaching-pacing |
| 写 quest 描述/副标题 | mod-description-trust |
| 检查 command 安全或 NBT 问题 | mod-system-safety |
| 为 ATM 风格 kitchen-sink 设计 | mod-atm-signature |
| 查维度/工具/矿石映射 | shared-builtin-tables |
| 不确定加载哪个 | 本文件 |

## Step Loading Plan

### Step 2 (采访 + 大纲)
1. 加载本文件（module-index）了解全局
2. 加载 mod-dependency-graph（拓扑设计）
3. 加载 mod-teaching-pacing（阶段/教学设计）
4. 加载 mod-reward-design（仅 philosophy 部分，~50行）
5. 加载 mod-description-trust（AP1-AP8 背景知识）
6. 如果是 kitchen-sink 包：加载 mod-atm-signature

### Step 4 (逐节点生成)
1. 加载 shared-builtin-tables（L1 映射表）
2. 加载 mod-item-reachability（每节点物品检查）
3. 加载 mod-reward-design（每节点 reward 设计）
4. 加载 mod-description-trust §AP9-AP11（AI 生成风险，~50行）
5. 章节批量审查时：加载 mod-teaching-pacing R14-R17

### Step 5 (全书验证)
按管线顺序加载全部模块：
item-reachability → dependency-graph → reward-design → teaching-pacing → description-trust → system-safety

## Three Hard Problems Coverage

| 硬伤 | Primary Module | Patterns | Anti-Patterns | Rules |
|---|---|---|---|---|
| 物品跨级 | mod-item-reachability | MP1, MP5, MP13, MP31, MP33 | AP1(item), PP7 | R1-R4, R16, R24 |
| 顺序倒置 | mod-dependency-graph + mod-teaching-pacing | MP6-MP12, MP19, MP23 | AP2, AP4, AP5, AP13 | R5-R9, R14-R17 |
| 奖励断链 | mod-reward-design | MP14-MP18, MP29, MP34 | AP6, AP8, AP17, AP18 | R10-R13, R28, R31 |

## Cross-Reference Map

| From | To | Relationship |
|---|---|---|
| mod-item-reachability R1 | shared-builtin-tables BUILTIN_DIMENSION_MAP | L1 data source |
| mod-item-reachability R2 | shared-builtin-tables BUILTIN_TOOL_TIER_MAP | L1 data source |
| mod-reward-design R28 | mod-system-safety AP15 | Rule definition → Safety analysis |
| mod-reward-design MP16 | mod-atm-signature MP16 | Universal concept → ATM implementation |
| mod-dependency-graph MP7/MP8 | mod-atm-signature | hide_dependency_lines → ATM preference |
| mod-description-trust AP1 | mod-item-reachability AP1(item) | Full coverage → Item variant |
| mod-description-trust R24 | mod-item-reachability R24 | Cross-ref → Primary rule |

## Companion Files (unchanged)

| File | Purpose |
|---|---|
| design-guide.md | Strategic thinking, field findings, layouts |
| reward-economy.md | Balance principles |
| difficulty-curve.md | Phase breakdown |
| tech-progression.md | Mod progression orientation |
