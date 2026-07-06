# Module: System Safety — 配置安全、兼容、经过测试吗？

> **Core Question:** quest 配置在运行时是否安全？是否兼容 modpack 更新和多人团队模式？是否通过了基本 QA？这个模块覆盖了 quest 设计中"不爆炸"的底线——command reward 安全、NBT 敏感性、状态迁移、视觉层级和测试覆盖。

## Quick Reference

| ID | 名称 | 类型 | 严重性 | 阶段 |
|---|---|---|---|---|
| AP12 | Task-Item NBT Insensitivity | Anti-Pattern | High | 外部脚本 |
| AP14 | Custom Task Black Box | Anti-Pattern | High | Step 4 |
| AP15 | Command Reward Side Effect | Anti-Pattern | **Critical** | Step 4 |
| AP16 | Quest State Migration | Anti-Pattern | High | 更新场景 |
| R28 | Command Reward Safety Scan | Rule | P0 ERROR | Step 4 |
| R29 | Team Progression Consistency | Rule | P1 INFO/WARN | Step 5 |
| R30 | Quest Visual Hierarchy | Rule | P3 WARNING | Step 5 |
| R32 | Chapter QA Coverage Heuristic | Rule | P3 WARNING | Step 5 |

---

## Anti-Patterns

### AP12 — Task-Item NBT Insensitivity（the Permissive Gate）

**症状：** quest task 接受 item 时不检查 NBT data——player 可以用空 fluid cell 完成"装满 refined obsidian 的 fluid cell"任务。quest 显示完成，但玩家实际没做该做的事。

**根因：** FTB Quests 的 item task 默认按 item ID 匹配，不校验 NBT tag。对于有 NBT 数据的物品（fluid cells、enchanted books、configured machines、spawn eggs），task 可能匹配 base item 而忽略区分具体变体的 NBT。

**后果：** 玩家收到 false completion signal——quest 看起来完成了但实际 mechanic 被跳过。quest book 作为进度指南的角色被破坏。

**实证：**
- **Create: Astral #566** — fluid cell quest 接受任意 fluid cell，不管装了什么流体。
- **Craftoria #666** — PNC:R Empty PCB quest 不完成，疑为 NBT 匹配问题的 false-negative 变体（与 Create: Astral 的 false-positive 相反）。

**修复：** (1) fluid task 优先用 `fluid` task type 而非 `item` task + fluid container；(2) 对有 NBT 的物品用 test variant 验证 task 只接受正确变体；(3) 若 NBT 匹配太脆弱，改用 `checkmark` task + description 说明。

> **注意：** 此 AP 无法静态检测——需要运行时 NBT 匹配验证，属于外部脚本/Step 5a in-game load-test 范畴。

---

### AP14 — Custom Task Black Box（the Unverifiable Quest）

**症状：** quest 使用 `custom` task type（由 KubeJS 或 mod 注册），quest system 无法验证完成条件是否可实现、公平、或是否存在。

**根因：** `CustomTask` 将完成逻辑完全委托给外部代码。FTB Quests 只知道"完成"或"未完成"。AI 生成 custom task 时无法验证 handler 是否注册、completion condition 是否可实现。

**后果：** quest 成为 black box——玩家从 quest UI 看不到实际要求，必须读外部文档或源码。AI 生成的 custom task 可能使用 plausible-sounding type name 但没有对应 handler，导致永久不可完成。quest system 不会报错，只是默默不完成。

**修复：** (1) AI **永远不应主动创建 custom task**——仅在 pack author 明确提供 type ID 和 criteria 时使用；(2) description 必须明确说明玩家需要做什么；(3) R6/R20 对含 custom task 的 quest 降级为 INFO。

---

### AP15 — Command Reward Side Effect

**症状：** command reward 产生意外副作用：re-claim 时物品重复、离线玩家 effect 失败、`/tp` 传送错误维度、`/fill` 覆盖玩家建筑。最坏情况：crash server 或授予 operator 权限。

**根因：** command reward 以 server-level 权限执行。几个关键 failure mode：

1. **幂等性：** re-claim 时 `/give` 重复给物品；`/gamestage add` 通常幂等但不保证。
2. **离线执行：** auto-claim 离线 reward 时 `/tp`、`/effect` 行为不可预测。
3. **Claim-all storm：** "claim all" 让 50 个 command reward 在同一 tick 执行，TPS 暴跌。
4. **破坏性命令：** `/fill`、`/setblock`、`/clear`、`/kill` 可修改世界或清空背包。
5. **跨维度命令：** `/tp`、`/setblock` 需要 explicit dimension specification。

**修复：** (1) 优先用标准 reward 类型；(2) command reward 确保幂等；(3) **禁止** destructive commands；(4) 指定目标维度；(5) 测试 offline + claim-all 场景。

---

### AP16 — Quest State Migration（modpack 更新兼容）

**症状：** modpack 更新后，existing player 的 quest book 状态不一致：新 quest auto-unlock 跳过 gating、修改的 quest 显示 stale completion、删除的 quest 留下 dangling reference、移除的 mod 导致 cascading failure。

**根因：** FTB Quests 按 quest ID 追踪进度。更新后 config 变了但玩家存档不变。五种 failure mode：quest addition（auto-unlock bypass）、modification（stale task data）、deletion（dangling deps）、mod removal cascade（所有引用失效）、item ID migration（旧 ID 变 invalid）。

**修复：** (1) 维护 quest ID stability——published 后不改 ID；(2) 新 quest 的 dependency chain 至少包含一个新/未完成 quest；(3) 删除 quest 时更新所有 `dependencies` 引用；(4) 移除 mod 时审计所有引用该 mod 的 quest；(5) `--adopt` 模式保留 existing quest ID。

---

## Rules

### R28 — Command Reward Safety Scan

**执行阶段：** Step 4（P0 ERROR/P1 WARNING）

> **Cross-Reference:** 此规则的 rule 定义（完整 pseudocode 和 pattern 列表）在 `mod-reward-design` 模块中。本模块放置系统性安全分析——即 AP15 描述的 failure mode 如何被 R28 的检测逻辑覆盖。

纯正则匹配 command 字符串，三级检测：

- **FORBIDDEN（ERROR）** — `/op`、`/deop`、`/gamemode creative`、`/stop`、`/kick`、`/ban`、`/whitelist`。绝对禁止。
- **HIGH_RISK（WARNING）** — `/fill`、`/setblock`、`/clone`、`/clear`、`/kill`、高等级 `/effect`、`/summon wither`、`/execute`。需人工审查。
- **IDEMPOTENCY_RISK（INFO）** — `/give`、`/tp`、`/playsound`。重复执行有副作用，提醒 author。

额外检查：`{p}` placeholder 是否用于 player-targeted command（缺失时 multiplayer 会出问题）；coordinate-based command 是否指定了目标维度。

**系统性分析：** R28 能覆盖 AP15 的"禁止命令"和"高风险命令"两个 failure mode，但**无法**覆盖幂等性和 claim-all storm——这些是运行时行为，需要 in-game 测试。AI 生成时 R28 作为 Step 4 P0 规则立即拦截危险命令，是最关键的安全网。

---

### R29 — Team Progression Consistency

**执行阶段：** Step 5（P1 INFO/WARN）| 仅在 pack 声明支持 team mode 时激活

FTB Teams 多人模式下 quest 的 reward 分配和 dependency 结构是否与团队进度共享一致。三个检查维度：

1. **Material bridge 分配：** 当 quest A 奖励的物品是 quest B 的 task 时（MP14 material bridge），验证 team mode 下 reward 是否分给所有成员还是仅提交者。仅提交者获得时，其他成员无法完成后续 quest。
2. **Fan-in convergence 分工：** MP8 convergence 节点（≥5 deps）在 team mode 下可被成员分工完成——验证这是否为设计意图。
3. **Optional path 分歧：** optional quest 有 mandatory dependent 时，team 中一个成员跳过 optional 可能阻塞其他成员的 mandatory 进度。

---

### R30 — Quest Visual Hierarchy & Size Consistency

**执行阶段：** Step 5（P3 WARNING/INFO）

quest 的视觉属性（size、shape、icon）是否与其在进度图中的语义角色一致。Monifactory CONTRIBUTING.md 明确要求 "Larger quests should be reserved for important milestones"。三个检查：

1. **Milestone size > routine size：** capstone/high-dependency quest 的 size 不应小于同 chapter routine quest 的最大 size。
2. **Optional size ≤ milestone size：** optional quest 不应比 milestone 更大。
3. **Shape consistency：** milestone quest 使用 1-2 种 shape，不应在同 chapter内出现 3+ 种 milestone shape。

ATM-10 的数据（4,601 quests，64 chapters）显示稳定的 shape-size 语义映射——这不是偶然，是 deliberate design decision。

---

### R32 — Chapter QA Coverage Heuristic

**执行阶段：** Step 5（P3 WARNING/INFO）

每个 chapter 是否满足基本的"可被 playtest 过"的结构性指标。四个信号：

1. **Dead-end detection：** quest 无 reward、无 dependent、非 optional、非 capstone → 可能是忘了加 reward 或连接后续 quest。
2. **Description coverage：** >30% quest 的 description 为空或 <20 chars → 高"空描述"比例暗示未经 review。Monifactory CONTRIBUTING.md 要求所有 quest 有 substantive description。
3. **Dependency orphan：** quest 完全依赖外部 chapter 且无 internal predecessor → 可能是在隔离中设计而未 playtest 全流程。
4. **Completion sanity：** >10 quest 的 chapter 中 0 optional → 100% mandatory 常暗示未经 review 区分 core vs supplementary。

**实证对比：** Enigmatica 10 在 GitHub issue tracker 上零 quest 投诉（~20 issue 均为 Bug/Suggestion），暗示系统性 playtesting 消除了 R32 能检测的基础问题。FTB Architect's Exodus 上线数周内 16+ quest issue，大多属于 R32 检测范畴。

---

## Cross-References

| 相关模块 | 关系 |
|---|---|
| `mod-reward-design` | R28 的 rule 定义和 pseudocode 在该模块；MP29 Command Reward 的基础用法 |
| `mod-description-trust` | AP14 black box quest 的 description 尤其重要——UI 不显示 completion criteria 时 description 是唯一信息源 |
| `mod-item-reachability` | R30 的 milestone 判定可参考 fan-in convergence 数据（R6/R20 的图遍历结果） |
| `mod-atm-signature` | MP20 Shape-as-Tier Signal 提供了 ATM 的 shape vocabulary 基准，R30 据此评估非 ATM 包 |

---

## Sources

- Laskyyy/Create-Astral #566（AP12 NBT insensitivity）
- TeamAOF/Craftoria #666（AP12 PNC:R PCB NBT）
- TeamAOF/Craftoria #231（R32 Powah chapter 无 reward 无 playtesting）
- Omicron-Industries/Monifactory CONTRIBUTING.md（R30 visual hierarchy 标准）
- EnigmaticaModpacks/Enigmatica10 Issues（R32 零投诉负面证据）
- FTBTeam/FTB-Modpack-Issues（Architect's Exodus 16+ issue 作为反面教材）
