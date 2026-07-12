# MP 选择决策表（Micro-Pattern Selection Decision Tree）

**草稿日期：** 2026-07-06
**来源：** Review C（实用性审查）§2.6 — "缺乏显式决策树"
**状态：** 草稿，待整合到 SKILL.md Step 4 per-node 循环

---

## 背景

micro-patterns.md 的 Scope Annotation Table 标注了每个 MP 的适用 pack_type 和加载时机（Step 2/Step 4），但没有提供一个显式的决策树告诉 AI agent "在什么条件下选择哪个 MP"。这导致 agent 在 Step 4 逐节点生成时依赖隐式判断来选择 MP 模式，容易遗漏或误选。

本文档提供一个简化的决策表，嵌入 SKILL.md Step 4 的 per-node 循环中。Agent 在生成每个 quest 时，按以下决策表选择适用的 MP 模式，并将选择记录在 quest 的注释中。

---

## 决策表：按 quest 结构特征选择 MP

### 第一层：Task 组合模式（节点级，Step 4）

根据 quest 的 task 数量和类型选择 task 组合公式：

```
IF quest.tasks.count == 1 AND task.type == "item"
    → MP1 (Single-Item Gate) — 默认模式，90%+ 的 quest

IF quest.tasks.count >= 2 AND all tasks are "item" type
    → MP2 (Multi-Item Synthesis Bundle)
    条件：quest 是 synthesis/convergence 节点（outline 中标注，deps >= 3 from different mods）
    注意：不要仅仅因为 quest 需要多个物品就用 MP2。MP2 是"跨系统合成"的信号，
          不是"多物品 checklist"。如果一个 quest 需要 3 个铁锭 + 2 个木板，
          那不是 MP2 — 那是两个独立的 MP1 quest。

IF quest.task.type in ("checkmark", "stat", "observation")
    → MP3 (Acknowledgement Gate)
    场景：tutorial/teaching quest，description 较长，教玩家一个 mechanic

IF quest.task.type == "kill" OR quest.task.type == "stat"
    AND quest 是递增链的一部分（outline 中标注为 escalation chain）
    → MP4 (Escalation Ladder) † ATM Signature
    注意：需要包内有 mob-grind 或重复性活动的 gameplay loop

IF quest.tasks 同时包含 "dimension" 和 "item" 类型
    → MP5 (Dimension + Item Composite)
    条件：物品来自该维度（R1 检查通过）
```

### 第二层：Dependency 拓扑模式（章节级，Step 2/3）

这些模式在 Step 2 outline 阶段确定，Step 4 生成时按 outline 执行：

```
IF quest 是 chain 的一部分（每个 quest 恰好 1 个 dependency，被 0-1 个 quest 依赖）
    → MP6 (Linear Chain)

IF quest 是 hub（0 个 dependency，被 3+ 个 quest 依赖）
    → MP7 (Fan-Out)
    scope note: hide_dependency_lines 是 ATM 偏好，非 ATM 包保持默认可见

IF quest 是 convergence（2+ 个 dependency，依赖来自独立 sub-tree）
    → MP8 (Fan-In / Convergence)
    scope note: hide_dependent_lines 是 ATM 偏好

IF quest 是 branch point（1 个 dependency，被 2+ 个独立 quest 依赖，
    且这些 quest 的下游汇聚到同一个 convergence node）
    → MP9 (Diamond / pick-and-rejoin)
    需要设置 dependency_requirement: "one_completed" 或 "one_started"

IF quest 是 independent（0 个 dependency，也不被其他 quest 依赖）
    → MP10 (Independent Island)
    注意：这是 catalog layout 的固有属性，不是主动的设计选择
```

### 第三层：Quest 内部节奏（混合，Step 2 + Step 4）

```
IF quest 是 teaching quest (MP3) AND 有直接的 doing quest 依赖于它
    → MP11 (Teach-Then-Do Sequencing)
    确保 teaching quest 的 dependency_depth < doing quest

IF chapter 内有同一 mod 的多 tier 内容
    → MP12 (Tier Escalation Within a Chapter)
    确保 quest 按 tier 从低到高排列

IF quest 涉及维度探索 + 物品获取（MP5）AND 两者分属不同 quest
    → MP13 (Explore-Then-Craft)
    确保 dimension quest 在 item quest 之前（R16 检查）
```

### 第四层：Reward 桥接模式（节点级，Step 4）

```
IF quest.reward 的物品出现在下游 quest 的 task 中
    → MP14 (Material Bridge) — 最强的前向拉力

IF quest.reward 是工具类物品（pickaxe, wrench, guide book, machine block）
    → MP15 (Tool Reward) — "here's your new tool, now go use it"

IF pack_type == "kitchen-sink"
    → MP16 (XP Drip) † ATM Signature
    每个 quest 加 { type: "xp", xp: 10 } 作为 baseline reward
    注意：expert 包和 create 包不使用 XP drip

IF quest 是 catalog hub（MP8 变体）AND 大部分 cell quest 无 reward
    → MP17 (Hub Concentration)
    reward 集中在 hub 上，cell 只给 satisfaction

IF quest 是 branch point AND reward 决定下游路径
    → MP18 (Choice Reward)
    适用于 expert/RPG 包的 meaningful choice 场景
```

### 第五层：Stage 标记模式（章节级，Step 2）

```
每个 chapter → MP19 (Chapter-as-Stage) — 默认组织方式

IF pack_type == "kitchen-sink" AND chapter 使用丰富 shape 词汇
    → MP20 (Shape-as-Tier Signal) † ATM Signature
    scope: 仅 ATM-style kitchen-sink，curated packs 不适用

IF progression 通过维度旅行分阶段
    → MP21 (Dimension-as-Stage-Gate) † ATM Signature

IF 跨 chapter 存在材料 tier spine
    → MP22 (Material-Tier Spine) † ATM Signature
    scope: 仅 ATM 系列

IF expert pack 需要不可见的 gating 基础设施
    → MP23 (Invisible Infrastructure)
    使用 always_invisible chapters 管理 gamestage 路由
```

### 第六层：Extended Type 模式（节点级，Step 4）

```
IF quest.task.type == "fluid"
    → MP27 (Fluid Task Gate)
    注意流体 amount 应为 producing machine 输出量的整数倍

IF quest.task.type == "forge_energy"
    → MP28 (Energy Threshold Gate)
    calibrate threshold against best available generator at this stage

IF quest.reward.type == "command"
    → MP29 (Command Reward)
    必须通过 R28 (Command Reward Safety Scan) 检查
    注意 AP14/AP15 的安全规则

IF pack 使用 gamestage gating
    → MP30 (Gamestage Bridge)
    确保每个 stage grant 有对应的 stage check

IF quest.task.type == "structure"
    → MP31 (Structure Discovery Gate)
    验证目标结构在世界生成中存在

IF quest 有 min_tasks 设置
    → MP32 (min_tasks Modifier)
    注意：与 MP9 功能重叠，视为 MP9 的 task-level 变体
```

---

## 决策表：按 pack_type 过滤可用 MP

以下表格标注每个 pack_type 下哪些 MP 是核心（必须考虑）、可选（视情况使用）、或不适用：

| MP | kitchen-sink | expert | skyblock | create | story/RPG |
|---|---|---|---|---|---|
| MP1 Single-Item Gate | 核心 | 核心 | 核心 | 核心 | 核心 |
| MP2 Multi-Item Synthesis | 核心 | 核心 | 可选 | 可选 | 可选 |
| MP3 Acknowledgement Gate | 核心 | 核心 | 核心 | 核心 | 核心 |
| MP4 Escalation Ladder † | 核心 | 不适用 | 可选 | 不适用 | 可选 |
| MP5 Dimension + Item | 核心 | 可选 | 核心 | 不适用 | 核心 |
| MP6 Linear Chain | 核心 | 核心 | 核心 | 核心 | 核心 |
| MP7 Fan-Out | 核心 | 核心 | 可选 | 可选 | 可选 |
| MP8 Fan-In | 核心 | 核心 | 可选 | 可选 | 可选 |
| MP9 Diamond | 可选 | 核心 | 可选 | 核心 | 可选 |
| MP10 Independent Island | 可选 | 不适用 | 不适用 | 核心 | 可选 |
| MP11 Teach-Then-Do | 核心 | 核心 | 核心 | 核心 | 核心 |
| MP12 Tier Escalation | 核心 | 核心 | 可选 | 可选 | 可选 |
| MP13 Explore-Then-Craft | 核心 | 可选 | 核心 | 不适用 | 核心 |
| MP14 Material Bridge | 核心 | 核心 | 核心 | 核心 | 核心 |
| MP15 Tool Reward | 核心 | 核心 | 核心 | 核心 | 核心 |
| MP16 XP Drip † | 核心 | 不适用 | 可选 | 不适用 | 不适用 |
| MP17 Hub Concentration | 可选 | 不适用 | 不适用 | 核心 | 不适用 |
| MP18 Choice Reward | 不适用 | 核心 | 不适用 | 可选 | 核心 |
| MP19 Chapter-as-Stage | 核心 | 核心 | 核心 | 核心 | 核心 |
| MP20 Shape-as-Tier † | 核心 | 不适用 | 不适用 | 不适用 | 不适用 |
| MP21 Dimension-as-Stage † | 核心 | 可选 | 核心 | 不适用 | 可选 |
| MP22 Material-Tier Spine † | 核心 | 不适用 | 不适用 | 不适用 | 不适用 |
| MP23 Invisible Infrastructure | 不适用 | 核心 | 不适用 | 不适用 | 可选 |
| MP27 Fluid Task Gate | 核心 | 核心 | 可选 | 核心 | 不适用 |
| MP28 Energy Threshold Gate | 核心 | 核心 | 可选 | 可选 | 不适用 |
| MP29 Command Reward | 可选 | 核心 | 不适用 | 不适用 | 核心 |
| MP30 Gamestage Bridge | 不适用 | 核心 | 不适用 | 不适用 | 可选 |
| MP31 Structure Discovery Gate | 核心 | 可选 | 核心 | 不适用 | 可选 |
| MP32 min_tasks Modifier | 不适用 | 不适用 | 不适用 | 核心 | 不适用 |

---

## 待决问题

1. **Context Window 限制：** 完整决策表 + micro-patterns.md 在 Step 4 的 context window 中可能过大（Review C 估算约 58,000 tokens）。建议 SKILL.md Step 4 只加载本决策表的精简版（第一层 + 第四层），其余层在 Step 2 加载。

2. **多 MP 叠加：** 一个 quest 可能同时匹配多个 MP（例如一个 quest 既是 MP5 + MP14 + MP16）。决策表需要明确叠加规则：第一层（task 组合）选一个，第四层（reward 桥接）可叠加多个，第二/五层（拓扑/stage）已在 Step 2 确定。

3. **ATM Signature 过滤：** 对于 non-ATM 包，† 标记的 MP 应在决策表中灰显或标注为"参考但不默认使用"。

4. **优先级冲突：** 当一个 quest 同时满足 MP2 和 MP1 的条件时，应优先使用 MP1（除非 quest 确实是 convergence node）。决策表需要更精确的优先级排序。

---

## Sources

- Review C (Practicality Audit) §2.6 — "缺乏显式决策树"
- Review A (Universality Audit) §4 — "ATM Signature Patterns" 分类
- micro-patterns.md Scope Annotation Table — 全模式适用范围
