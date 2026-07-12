# Phase 4 Cycle 8 — 修正摘要

> **修正日期：** Phase 4 Cycle 8
> **审查来源：** 审查员 A（通用性）、审查员 B（完备性）、审查员 C（实用性）
> **修正执行：** Phase 4 写作子 agent

---

## 直接修改（低风险 + 中风险）

### 1. MP39 适用范围修正 — `mod-reward-design.md` [审查员A, P0]

- **Quick Reference 表：** `pack_types` 从 `expert, kitchen-sink` 改为 `expert`
- **描述段落：** 新增「适用范围」声明，说明 kitchen-sink 包中替代奖励系统的案例尚未在已研究的 39 个包中观察到
- **理由：** 四个证据源全部来自 expert/hardcore 包，ATM-10 仅证明 kitchen-sink 的奖励设计问题存在，不证明替代方案适用

### 2. R44 补充 reward_table 边界 — `mod-reward-design.md` [审查员B, P0]

- **新增段落：** `reward_table 边界说明`——当奖励是 `type: "random"` 或 `type: "loot"` 时，R44 无法直接检查 reward_table 内的物品
- **降级策略：** 检查 reward_table 是否在已知阶段内有定义（通过文件名推断），标记为启发式检查
- **严重度调整：** `random`/`loot` 类型统一降一级（expert: ERROR→WARNING, kitchen-sink: 保持 INFO）
- **新增伪代码：** reward_table heuristic extension
- **新增段落：** `无阶段数据降级`——当 stage_map 不存在时的降级路径（审查员A 补充）

### 3. R45 补充非物品奖励处理 — `mod-reward-design.md` [审查员B, P0]

- **新增段落：** `非物品奖励的引导价值`——gamestage 解锁、dimension 解锁、command 奖励视为"虚拟桥接项"
- **新增伪代码：** Virtual bridge items for non-item rewards
- **检查逻辑：** 当 capstone 奖励包含 gamestage 解锁时，检查解锁的 stage 是否在下一章被依赖

### 4. Game Stages 段落加适用范围声明 — `mod-reward-design.md` + `mod-item-reachability.md` [审查员A, P1]

三处 Game Stages 段落各新增适用范围声明和版本警告：

- **mod-reward-design.md `Game Stages 作为 Command Reward 的搭档`：** 新增声明"主要在 expert/hardcore 包中观察到"
- **mod-item-reachability.md `Game Stages 作为物品可达性的外部守门人`：** 新增声明 + 版本警告"1.12.2 工具链在 1.20+ 已过时"
- **mod-item-reachability.md `Game Stages 闭环集成的技术架构`：** 标题改为"（MC 1.12.2-1.16.5 为主）"，新增声明 + 段末补充 GT-O 替代方案和 KubeJS 1.20+ 替代

### 5. R42 补充 consume_items 交互 — `mod-item-reachability.md` [审查员B, P1]

- **新增段落：** `consume_items 交互说明`
- **核心逻辑：** `consume_items: true` 时物品被消耗，需要可重复获取途径；`consume_items: false` 时物品不消耗，只需一次性获取途径
- **新增伪代码：** consume_items interaction 分支
- **L1 降级：** 标记为 INFO 级人类审查项

### 6. R43 补充 optional quest 处理 — `mod-dependency-graph.md` [审查员B, P1]

- **新增段落：** `Optional quest 循环严重度分级`
- **核心逻辑：** optional quest 形成的 Stage-Quest 循环标记为 WARNING（不影响主线进度），mandatory quest 的循环保持 ERROR
- **新增伪代码：** Optional quest severity differentiation
- **一致性：** 与 R7（Optional-Gate-Mandatory）的精神一致

---

## 草稿修改（高风险 — 待 Phase 5 实施）

### 7. SKILL.md Step 2 新增阶段定义收集 [审查员C, P2]

- **草稿位置：** `drafts/phase4-cycle8-skill-edits.md` 修改 1
- **内容：** 在 Step 2 采访流程中新增 `Stage definitions` 分支，收集 stage_map、stage_available_resources、Game Stages 集成数据
- **触发条件：** expert/story/skyblock 包强制询问，kitchen-sink 可选
- **预期效果：** R42/R43/R44/R4 的 L2 数据覆盖率从 ~20-40% 提升到 ~60-80%

### 8. SKILL.md Step 4 新增强制推理步骤 [系统要求, P2]

- **草稿位置：** `drafts/phase4-cycle8-skill-edits.md` 修改 2
- **内容：** Gate 1 扩展 R42 引用（"玩家此刻怎么拿到这个？"），Gate 2 扩展 R45 引用（"这个奖励引导玩家去做什么？"）
- **Phase 5 实施计划：** 正式写入 SKILL.md 的 Step 4 Gate 1/2 部分

---

## 修改文件清单

| 文件 | 修改类型 | 修正项编号 |
|---|---|---|
| `mod-reward-design.md` | 直接修改 | 1, 2, 3, 4(部分) |
| `mod-item-reachability.md` | 直接修改 | 4(部分), 5 |
| `mod-dependency-graph.md` | 直接修改 | 6 |
| `mod-teaching-pacing.md` | 未修改 | — |
| `SKILL.md` | 未直接修改 | 7, 8（草稿） |
| `drafts/phase4-cycle8-skill-edits.md` | 新建草稿 | 7, 8 |
| `drafts/phase4-cycle8-corrections.md` | 本文件 | — |

## 未采纳的审查建议（Phase 5 考虑）

以下审查建议在评估后认为适合在 Phase 5 处理，不在本轮修正范围内：

- **审查员 B 新增规则 R46（Reward Table Cross-Stage Leakage）：** 需要独立的规则设计和全量 reward_table 数据，适合 Phase 5
- **审查员 B 新增规则 R47（Empty/Skeleton Chapter Detection）：** 简单但需要新增检测逻辑
- **审查员 B 新增规则 R48（Stage Definition Consistency）：** 需要 L2 Game Stages 配置数据
- **审查员 B R42 NBT 变体物品 / OreDict/Tag 匹配 / 怪物掉落物：** 均为 R42 的进一步细化边界，在 R42 的基础边界说明已就位后，适合后续迭代
- **审查员 B R44 同一物品在不同阶段的重复出现：** stage_map 应映射到物品的首次出现的最低阶段——这是一个合理的约定，但需要 L2 数据验证
- **审查员 B 规则交叉澄清（R42 vs R1/R4, R44 vs R10/R12, R43 vs R5/R8, R45 vs R10）：** 概念澄清有价值，但不影响当前实现，适合文档整理阶段
- **审查员 C shared-builtin-tables 扩展（BUILTIN_STAGE_PROXY）：** 需要新增数据表，适合 Phase 5
- **审查员 A 四维阶段模型 / 弱锁策略 / 教学快速推入 / progression_mode 标注：** 均为适用范围标注建议，风险较低，可在后续文档整理中添加
