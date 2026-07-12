# Phase 4 Cycle 8 — SKILL.md 修改草稿

> **风险等级：** 高风险（SKILL.md 核心流程修改）
> **来源：** 审查员 C 建议 + Phase 5 目标规划
> **状态：** 草稿，待 Phase 5 实施

---

## 修改 1：Step 2 新增「阶段定义收集」分支 [Phase 4 Cycle 8 - 审查员C]

### 修改位置

在 SKILL.md 的 Step 2 采访流程中，`Rewards & difficulty` 分支之后、`Linkage` 分支之前，新增一个 `Stage definitions` 分支。

### 新增内容

在 Step 2 采访的分支列表中添加以下内容：

```
- **Stage definitions（阶段定义收集）：** 当包类型为 expert、story 或 skyblock 时，强制询问以下内容；kitchen-sink 包可选：
  1. **阶段划分（stage_map 骨架）：** "你的整合包有明确的阶段划分吗？例如'石器→铁器→钻石→下界→末地'或'ULV→LV→MV→HV→EV'？请列出阶段名称和顺序。"
  2. **阶段关键资源（stage_available_resources）：** "每个阶段有哪些关键可获得资源？请每阶段列出 5-10 个代表性物品 ID。"
  3. **Game Stages 集成（如果适用）：** "你的包是否使用 Game Stages 或类似的阶段锁定模组？如果是，请提供 stage name 列表及其解锁的内容摘要（物品/维度/配方）。"
  
  收集到的数据将作为 L2 级数据源，供以下规则使用：
  - R44（Reward-Stage Matching）：用 stage_map 判断奖励物品是否越级
  - R42（Stage-Internal Item Reachability）：用 stage_available_resources 判断合成链叶子节点是否在当前阶段可达
  - R43（Stage-Quest Causal Chain Acyclic）：用 stage→quest 映射检测 Stage-Quest 交叉环
  - R4（Stage Boundary）：用阶段定义判断物品是否处于正确的阶段区间
  
  如果用户未提供 L2 数据，上述规则降级为 L1 启发式或 INFO 级别报告。
```

### 修改理由

审查员 C 的最高优先级建议。审查员 C 指出："提升覆盖率的关键手段是在 Step 2 采访中收集 L2 数据"——多问 3-5 个问题，换来 6 条规则（R42/R43/R44/R4/R3/R2）的执行精度从 ~20-40% 提升到 ~60-80%。这是一个高投入产出比的改进。

### 插入点参考

在 SKILL.md 的 Step 2 分支列表中，位于 `- **Rewards & difficulty:**` 和 `- **Linkage**` 之间。具体上下文：

```
- **Rewards & difficulty:** reward philosophy (generous items vs cosmetic/lore), `consume_items` philosophy, special reward types (commands / loot tables / XP), expert/hardcore gating.
  - **Dominant reward type (审查 C 补充):** ...（现有内容）...

[在此处插入 Stage definitions 分支]

- **Linkage (only if Step 1 found existing quests):** ...（现有内容）...
```

---

## 修改 2：Step 4 新增强制推理步骤 [Phase 4 Cycle 8 - 系统要求]

### 修改位置

在 SKILL.md 的 Step 4 per-node loop 中，现有 Gate 1（Task Item Reachability）和 Gate 2（Reward Bridge）之间，强化推理步骤的引用关系。

### 新增内容

在 Step 4 的 Gate 1 reasoning 部分增加对 R42 的显式引用，在 Gate 2 reasoning 部分增加对 R45 的显式引用：

```
**Reasoning Gate 1 扩展（R42 引用）：**

在 Gate 1 的 three checks 之后，每个 task item 必须额外回答一个可达性问题：

> 玩家此刻怎么拿到这个？——引用 mod-item-reachability R42（Stage-Internal Item Reachability）

如果包有 L2 阶段数据（Step 2 收集的 stage_map 和 stage_available_resources），检查该物品的合成链叶子节点是否在当前阶段可达资源集合内。如果无 L2 数据，使用 R1（维度）+ R4（阶段边界）的 L1 启发式组合，并标记 [unverified:stage_recipe]。

注意：这是对现有 Gate 1 的语义强化，不改变 gate 的通过/失败判定逻辑。Gate 1 已经隐含执行了 R1/R2/R3 检查，此扩展显式加入 R42 的阶段内资源可达性视角。

**Reasoning Gate 2 扩展（R45 引用）：**

在 Gate 2 的 four categories 之后，每个 reward 必须额外回答一个引导问题：

> 这个奖励引导玩家去做什么？——引用 mod-reward-design R45（Reward Guidance Bridging）

如果当前 quest 是章节的 capstone（依赖数最多的 quest），检查其奖励是否包含下一章入口任务所需的物品或 gamestage 解锁（虚拟桥接项）。如果奖励既不桥接物品也不桥接阶段，标记为 chapter-level dead-end risk。

注意：这是对现有 Gate 2 的语义强化。Gate 2 已经在 quest 级别检查奖励桥接（R10），此扩展将视角提升到 chapter 级别（R45），确保章节间的过渡有明确的奖励引导。
```

### Phase 5 实施计划

此修改属于 Phase 5 的核心目标。本轮 Phase 4 先以草稿形式记录修改内容和理由，Phase 5 将：
1. 将上述内容正式写入 SKILL.md 的 Step 4 Gate 1 和 Gate 2 部分
2. 确保 Gate 1 的 R42 引用与 Step 2 收集的 L2 阶段数据联动
3. 确保 Gate 2 的 R45 引用与 R45 的虚拟桥接项扩展联动（见 mod-reward-design.md 的 R45 修正）
4. 在 Step 5 全量验证中加入 R45 的 chapter 级别桥接检查

### 修改理由

Phase 5 的核心目标是让每个 task item 和每个 reward 都经过可达性和引导性的强制推理。当前 Gate 1 和 Gate 2 已经执行了类似的检查，但缺少对 R42（阶段内物品可达性）和 R45（chapter 级奖励引导）的显式引用。加入这两个引用后，Step 4 的推理链将覆盖从 quest 级别到 chapter 级别的完整保障。
