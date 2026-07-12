# FTB Quests Design Reference — Module Index

> 本索引是模块化参考系统的路由表。AI agent 根据当前工作场景加载对应模块。

## Modules

| Module | Core Question | Lines | Step 2 | Step 4 | Step 5 |
|---|---|---|---|---|---|
| [shared-builtin-tables.md](shared-builtin-tables.md) | L1 内置映射表 | ~153 | — | ✔ | ✔ |
| [mod-item-reachability.md](mod-item-reachability.md) | 玩家拿得到这个物品吗？ | ~304 | — | ✔ | ✔ |
| [mod-dependency-graph.md](mod-dependency-graph.md) | 任务怎么连接？图健康吗？ | ~386 | ✔ (partial) | — | ✔ |
| [mod-reward-design.md](mod-reward-design.md) | 奖励什么？引导去哪？ | ~409 | ✔ (philosophy) | ✔ | ✔ |
| [mod-teaching-pacing.md](mod-teaching-pacing.md) | 教学在测试之前吗？ | ~202 | ✔ (partial) | ✔ (review) | ✔ |
| [mod-description-trust.md](mod-description-trust.md) | 描述文本准确吗？ | ~147 | ✔ (AP1-AP8 bg) | ✔ (AP9-11) | ✔ |
| [mod-system-safety.md](mod-system-safety.md) | 配置安全/兼容吗？ | ~157 | — | ✔ (§R28 only) | ✔ |
| [mod-atm-signature.md](mod-atm-signature.md) | ATM 专属还是通用？ | ~115 | ✔ (if kitchen-sink) | — | — (unless ATM) |
| [topology-coordinates.md](topology-coordinates.md) | Quest 坐标怎么算？ | ~920 | ✔ (layout planning) | ✔ (coordinate assignment) | — |
| [progression-rules.md](progression-rules.md) | 拓扑布局规则校验 (R55–R64) | ~560 | ✔ (R55 topology-mode) | ✔ (R55/R57 advisory) | ✔ (R55–R64 full pipeline) |
| [micro-patterns.md](micro-patterns.md) | 新增微观模式 (MP46+) | ~90 | ✔ | ✔ | ✔ |

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
| 定义 questbook 角色（companion/tutorial/incentive） | mod-reward-design |
| 检查 quest 移植适配 | mod-dependency-graph |
| 评估 collection 维护成本 | mod-description-trust |
| 判断零奖励设计安全性 | mod-reward-design |
| 排列 quest 的 x/y 坐标 | topology-coordinates |
| 选择 chapter 拓扑类型 (线性/hub/并行/树/菱形/网格) | topology-coordinates |
| 检查布局碰撞和间距 | topology-coordinates |
| 校验拓扑-进度模式对齐 (R55) | progression-rules |
| 运行 R55-R64 拓扑布局校验管线 | progression-rules |
| 检查 R58 碰撞检测 (验证阶段) | progression-rules |
| 解决 R41 与 R55 早期章节冲突 | progression-rules |
| 检查奖励架构与角色匹配 (R51) | mod-reward-design |
| 检查 dependency_requirement 分布 (R52) | mod-dependency-graph |
| 不确定加载哪个 | 本文件 |

## Step Loading Plan

### Step 2 (采访 + 大纲)
1. 加载本文件（module-index）了解全局
2. 加载 mod-dependency-graph（拓扑设计）
3. 加载 mod-teaching-pacing（阶段/教学设计）
4. 加载 mod-reward-design（仅 philosophy 部分，~50行）
5. 加载 mod-description-trust（AP1-AP8 背景知识）
6. 如果是 kitchen-sink 包：加载 mod-atm-signature
7. 加载 mod-reward-design §R46（questbook 角色声明 — Step 2 必选决策，决定 R47/R50 适用性）
8. 加载 mod-reward-design §R51（奖励架构对齐 — 使用 R46 角色名称检查 reward model 匹配度，Cycle 10 新增）
9. 加载 progression-rules §R55（拓扑-进度模式对齐 — 选择拓扑类型时检查与 progression_mode 的兼容性，注意 R41 早期章节覆盖规则）

### Step 4 (逐节点生成)
1. 加载 shared-builtin-tables（L1 映射表）
2. 加载 mod-item-reachability（每节点物品检查）
3. 加载 mod-reward-design（每节点 reward 设计）
4. 加载 mod-description-trust §AP9-AP11（AI 生成风险，~50行）
5. 加载 mod-system-safety §R28（Command Reward Safety — P0 级 Step 4 规则，command 安全扫描必须在生成时执行；其余规则仍在 Step 5 加载）
6. 章节批量审查时：加载 mod-teaching-pacing R14-R17
7. 加载 mod-teaching-pacing §R47（companion delegation advisory — INFO 级别，不阻断写入）
8. 章节完成后：加载 progression-rules §R55, §R57（拓扑-模式对齐 + Hub 尺寸优势 — advisory 级别，不阻断写入）

### Step 5 (全书验证)
按管线顺序加载全部模块：
item-reachability → dependency-graph → reward-design → teaching-pacing → description-trust → system-safety → **progression-rules**（R55-R64 拓扑校验管线）

## Three Hard Problems Coverage

| 硬伤 | Primary Module | Patterns | Anti-Patterns | Rules |
|---|---|---|---|---|
| 物品跨级 | mod-item-reachability | MP1, MP5, MP13, MP31, MP33, MP36 | AP1(item), AP22(config-drift), PP7 | R1-R4, R16, R24, R48 |
| 顺序倒置 | mod-dependency-graph + mod-teaching-pacing | MP6-MP12, MP19, MP23, MP35, MP37, MP39, MP40 | AP2, AP4, AP5, AP13 | R5-R9, R14-R17, R35, R47, R52 |
| 奖励断链 | mod-reward-design | MP14-MP18, MP29, MP34, MP36, MP38, MP41 | AP6, AP8, AP17(+MP44 note), AP18 | R10-R13, R28, R31, R33(S4 invariant), R34, R46, R49, R50, R51, R54 |

> **Cycle 5 MP35-MP38 cross-reference note:**
> MP35-MP38 are currently archived only in `micro-patterns.archive.md` (not yet redistributed to module files).
> Their primary module affinities are:
> - **MP35** (Dual-Task Automation) → `mod-teaching-pacing` (teach-then-do variant) + `mod-item-reachability` (consume_items interaction)
> - **MP36** (Currency-as-Reward) → `mod-reward-design` (reward bridging variant) + `mod-item-reachability` (item type)
> - **MP37** (Progress Catalog) → `mod-dependency-graph` (chapter topology) — **NOTE: must include `optional: true` (PP4 prevention)**
> - **MP38** (Reward Perception Split) → `mod-reward-design` (kitchen-sink reward philosophy) — **NOTE: single-source validation, see confidence note in archive**
> - **Case Study** (Profession Chapter) → **[TWR-specific]** — decomposable as MP7+MP10+MP18; not a generalizable pattern

## Cross-Reference Map

| From | To | Relationship |
|---|---|---|
| mod-item-reachability R1 | shared-builtin-tables BUILTIN_DIMENSION_MAP | L1 data source |
| mod-item-reachability R2 | shared-builtin-tables BUILTIN_TOOL_TIER_MAP | L1 data source |
| mod-reward-design R28 | mod-system-safety AP15 | Rule definition → Safety analysis |
| mod-reward-design R33 | mod-dependency-graph R22 | table_id integrity (generator invariant, Step 4) → cross-reference validation |
| mod-reward-design MP16 | mod-atm-signature MP16 | Universal concept → ATM implementation |
| mod-dependency-graph MP7/MP8 | mod-atm-signature | hide_dependency_lines → ATM preference |
| mod-description-trust AP1 | mod-item-reachability AP1(item) | Full coverage → Item variant |
| mod-description-trust R24 | mod-item-reachability R24 | Cross-ref → Primary rule |
| mod-reward-design R34 | mod-reward-design MP34 | Distribution report validates reward table type consistency |
| mod-dependency-graph R35 | mod-dependency-graph Shape Semantics | Shape consistency check uses pack-level shape table |
| mod-reward-design R46 | mod-reward-design R47, R50 | Questbook role declaration → downstream rule applicability |
| mod-dependency-graph R48 | mod-description-trust AP1 | Quest port drift is a systematic source of AP1/AP2/AP4 |
| mod-reward-design R50 | mod-reward-design R46 | Zero-reward safety depends on questbook role declaration |
| mod-reward-design R51 | mod-reward-design R46 | Role taxonomy unification — R51 MUST use R46's role names (Companion/Tutorial/Incentive Catalog) |
| mod-reward-design R51 | mod-reward-design R50 | R51 is alignment check; R50 is full safety check — both must pass for zero-reward packs |
| mod-dependency-graph R52 | mod-teaching-pacing R41 | R52 (dependency_requirement skew) + R41 (progression_mode) — doubly gate-oriented when both strict |
| mod-reward-design R54 | mod-reward-design R33 | R54 (semantic naming) complements R33 (structural integrity); R33 is P1, R54 is P3 |
| mod-description-trust AP22 | mod-dependency-graph R48 | Config-drift staleness (AP22) is a systematic source of port drift (R48) descriptions |
| mod-reward-design R31 | mod-reward-design AP17/MP44 | MP44-AP17 interaction: skill-tree packs mitigate AP17's xp_levels concern; annotated in R31 sub-gate |
| progression-rules R55 | mod-teaching-pacing R41 | R55 topology-mode alignment vs R41 early-game flexible — conflict resolution defined in R55 |
| progression-rules R58 | topology-coordinates Phase 4 | R58 collision detection is validation-only; Phase 4 algorithm is reference, not executable by LLM |
| progression-rules R55 | topology-coordinates Phase 2 | R55 uses classify_topology() output — highway_branch added as 7th type in Cycle 11 Phase 5 |

## Companion Files (unchanged)

| File | Purpose |
|---|---|
| design-guide.md | Strategic thinking, field findings, layouts |
| reward-economy.md | Balance principles |
| difficulty-curve.md | Phase breakdown |
| tech-progression.md | Mod progression orientation |
