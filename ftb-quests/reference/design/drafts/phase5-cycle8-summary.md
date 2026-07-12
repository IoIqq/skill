# Phase 5 Cycle 8 — SKILL.md 修改摘要

> **日期：** 2026-07-08
> **状态：** 已完成
> **来源草稿：** `phase4-cycle8-skill-edits.md`
> **备份：** `drafts/SKILL.md_backup_phase5_cycle8.md`

---

## 修改 1：Step 2 新增「Stage definitions（阶段定义收集）」分支

**位置：** Step 2 采访流程，`Rewards & difficulty` 分支（含 Dominant reward type 子项）之后、`Linkage` 分支之前。

**内容：**
- 新增 `Stage definitions` 分支，收集三项 L2 级数据：
  1. **stage_map skeleton** — 阶段划分与顺序
  2. **stage_available_resources** — 每阶段关键可获得资源（5–10 个代表性物品 ID）
  3. **Game Stages integration** — 阶段锁定模组的 stage name 及解锁内容
- expert / story / skyblock 包强制询问；kitchen-sink 包可选
- 明确列出 L2 数据服务的四条规则：R42、R44、R43、R4
- 说明无 L2 数据时降级为 L1 启发式或 INFO 级报告

**影响：** Step 2 采访新增约 3–5 个问题，换取 R42/R43/R44/R4 的执行精度从 L1 启发式（~20–40%）提升到 L2 数据驱动（~60–80%）。

---

## 修改 2：Step 4 Gate 1 新增 R42 阶段内可达性检查

**位置：** Step 4 Gate 1，三检查表（R1/R2/R3）之后、Gate verdict 之前。

**内容：**
- 新增 **R42 Stage-Internal Item Reachability** additional check
- 每个 task item 必须额外回答：「玩家此刻怎么拿到这个？」
- 有 L2 数据时：检查合成链叶子节点是否在当前阶段可达资源集合内
- 无 L2 数据时：使用 R1 + R4 的 L1 启发式组合，标记 `[unverified:stage_recipe]`
- 明确标注：语义强化，不改变 gate 的 pass/fail 判定逻辑

---

## 修改 3：Step 4 Gate 2 新增 R45 chapter 级奖励引导检查

**位置：** Step 4 Gate 2，四分类表（Material bridge / Universal bridge / Terminal / Dead-end risk）之后、Backward matching 注释之前。

**内容：**
- 新增 **R45 Reward Guidance Bridging** additional check（chapter-level）
- 每个 reward 必须额外回答：「这个奖励引导玩家去做什么？」
- 当 quest 是章节 capstone 时，检查奖励是否包含下一章入口所需的物品或 gamestage 解锁（虚拟桥接项）
- 如果奖励既不桥接物品也不桥接阶段，标记为 chapter-level dead-end risk
- 明确标注：将 Gate 2 的视角从 quest 级别（R10）提升到 chapter 级别（R45）

---

## 修改统计

| 项目 | 数量 |
|---|---|
| 新增 Step 2 分支 | 1（Stage definitions） |
| 新增 Gate 1 additional check | 1（R42） |
| 新增 Gate 2 additional check | 1（R45） |
| 新增行数（约） | ~30 行 |
| 删除/替换行数 | 0 |
| 修改现有逻辑 | 无（均为语义强化追加） |

## 风险评估

- **风险等级：** 中（核心流程追加，不改变现有 gate 的 pass/fail 判定）
- **回滚方式：** 从 `drafts/SKILL.md_backup_phase5_cycle8.md` 恢复
- **后续步骤：** Step 5 全量验证中应加入 R45 的 chapter 级桥接检查（Phase 5 后续 cycle）
