## 审查员 B -- 完备性质疑 (Cycle 4 新增/修改内容)

审查日期: 2026-07-07
审查范围: R33 (Reward Table Reference Integrity), MP34 (Loot Table Reward 统一模型), Reward Economy 谱系, Shape 语义 pack-specific 结论, Dependency depth 分析
审查方法: 逐规则质疑边界情况、降级策略、跨规则交互、数据完整性
来源文件: mod-reward-design.md, mod-dependency-graph.md, mod-item-reachability.md, mod-teaching-pacing.md, mod-description-trust.md, mod-system-safety.md, reward-table-rules-R33-R35_2026-07-07.md

---

### 一、R33 -- Reward Table Reference Integrity

#### 完备性评级: C (遗漏显著边界情况)

R33 当前仅验证 `table_id` 是否指向一个**存在的文件**。这是必要但不充分的条件。从"玩家 claim 了 quest 但 reward 行为异常"这个核心问题出发，至少遗漏了以下 5 个边界情况：

#### 遗漏 1: Reward table 存在但 rewards 数组为空

```
// 存在的 reward table 文件，但 rewards 为空
{
    id: "0414572B7C36F04F"
    loot_size: 1
    rewards: []
}
```

R33 通过（table_id 存在），但玩家 claim 后什么也得不到。这与 table_id 不存在的后果完全一致（silent reward failure），但 R33 无法检测。

**建议:** R33 应增加 `rewards.length == 0` 检查，触发 WARNING: "Reward table {id} exists but has empty rewards array — players will receive nothing."

#### 遗漏 2: Reward table 所有 weight (count) 为 0

```
{
    id: "0414572B7C36F04F"
    loot_size: 1
    rewards: [
        { count: 0, item: { count: 1, id: "minecraft:diamond" } }
        { count: 0, item: { count: 1, id: "minecraft:emerald" } }
    ]
}
```

FTB Quests 的 reward table 使用 weighted random selection。当所有 weight 为 0 时，行为是 implementation-defined：可能 crash，可能返回 null，可能随机选一个。无论哪种结果，对玩家都是意外。

**建议:** R33 增加 `sum(rewards[*].count) == 0` 检查，触发 ERROR: "Reward table {id} has zero total weight — random selection behavior is undefined."

#### 遗漏 3: loot_size 为 0 或负数

`loot_size` 控制每次 claim 时 roll 的次数。当前文档中 Craftoria 使用 `loot_size: 1`，E10 使用 `loot_size: 4`。但如果 `loot_size: 0`：
- 0 次 roll = 不产出任何物品 = silent failure
- 负数 roll 的行为完全不可预测

R33 不检查 loot_size 的有效性。

**建议:** R33 增加 `loot_size <= 0` 检查，触发 WARNING: "Reward table {id} has loot_size={value} — no items will be rolled."

#### 遗漏 4: Reward table 内的 item ID 不存在

R33 验证 table_id → file 的存在性，但不验证 table 内部的 item ID 是否在包的 mod list 中有效。如果 reward table 引用了被移除 mod 的物品：
- 最好的情况：该 reward entry 被跳过
- 最坏的情况：claim 时 crash 或 NPE

这与 R1-R4 (item reachability) 和 R26 (version consistency) 是同一类问题的 reward-table 变体，但现有规则只检查 quest task/reward 中直接引用的 item，不检查 reward table 内部的 item。

**建议:** R33 增加 table 内 item ID 的交叉验证：`for entry in table.rewards: if entry.item.id not in pack_item_registry: WARNING`。这与 R23 的 item ID 验证是同构的，可复用检测逻辑。

#### 遗漏 5: Reward table 被多个 quest 共享时的意外耦合

文档显示 MI:Foundation Botania 的 4 个 choice reward 全部引用同一个 `table_id: 1606690661312817740L`。这意味着：
- 修改这个 table 会同时影响 4 个 quest 的 reward pool
- 如果某个 quest 的进度阶段需要不同的 reward pool，共享 table 会导致 reward 与 quest 难度不匹配（违反 R12 Reward Value Progression）

R33 不检测 table 的共享程度，也不检查共享 table 在不同进度阶段的适用性。

**建议:** R33 增加 table 引用计数统计。当同一 table 被 >3 个不同 chapter 的 quest 引用时，触发 INFO: "Table {id} shared across {n} chapters — verify reward pool is appropriate for all referencing quest tiers." 这不需要强制修改，只是一个 authoring awareness 提醒。

#### 降级策略评估

当 reward_tables 目录不存在或不可访问时，R33 应如何降级？当前文档没有说明。

**建议:** 明确降级行为：如果 `reward_tables/` 目录不存在且包内有 random/loot/choice reward → ERROR（这些 reward type 必须依赖 table 文件）。如果目录存在但为空 → 对所有 table_id 引用触发 ERROR。

---

### 二、MP34 -- Loot Table Reward 统一模型

#### 完备性评级: B (覆盖主要场景，少量边界未处理)

MP34 的核心贡献——random/loot/choice 底层共享同一 reward table 系统——是一个重要的架构洞察，Phase 1 Cycle 4 的错误理解已被正确修正。以下是遗漏的边界情况：

#### 遗漏 1: SNBT 格式的版本兼容性

Cycle 4 的三个审计包 (Craftoria, E10, MI:Foundation) 都使用 SNBT 格式。但 FTB Quests 的历史版本中：
- 1.16.5 及更早版本使用 JSON 格式（`quests.json`）
- 1.18.2+ 迁移到 SNBT（每个 quest/table 一个 `.snbt` 文件）
- 1.20.1+ 的 SNBT 格式可能包含新字段（如 `use_title`）

MP34 的文档中出现了 `use_title: true`（E10 示例），但没有说明这是哪个版本引入的字段。如果 skill 为 1.18.2 包生成包含 `use_title` 的 reward table，该字段是否会被忽略或导致解析错误？

**建议:** 在 MP34 中标注 reward table 格式的最低版本要求。`use_title` 等新字段应标注 `[1.20.1+]`。这与 R26 (Quest-Mod Version Consistency) 的精神一致。

#### 遗漏 2: Reward table 的 ID 生成规则

文档示例中 table ID 是 long 型（如 `0414572B7C36F04F`），与 quest ID 使用相同的格式。但没有说明：
- ID 是随机生成的还是按规则计算的？
- 文件名与内部 `id` 字段必须匹配吗？（FTB Quests 按文件名查找还是按 id 字段查找？）
- ID 碰撞时会发生什么？（两个 table 使用同一个 ID）

如果 skill 生成新的 reward table，它需要知道正确的 ID 生成方式。

**建议:** 在 MP34 中补充 ID 生成规则：FTB Quests 使用随机 long ID，文件名（去掉 `.snbt`）必须与 `id` 字段一致。生成时应使用 `SecureRandom.nextLong()` 或等价的随机生成，确保不与现有 ID 碰撞。

#### 遗漏 3: Choice reward 的 UX 约束

`type: "choice"` 让玩家从 table 的所有 entry 中选一个。如果 table 有 50 个 entry（高 weight diversity），choice UI 需要显示 50 个选项——这对玩家是 overwhelming 的。

文档中提到 MI:Foundation 每个 chapter 使用 2-6 个 choice reward，但没有说明 choice table 的 entry 数量上限。

**建议:** MP34 增加 UX 约束建议：choice reward 引用的 table 建议 entry 数量 <= 8（一屏可显示），最多不超过 16。超过时建议拆分为多个 table 或使用 nested choice（先选 category，再选具体 item）。

#### 遗漏 4: Loot type 的 "manual open" 与 autoclaim 的交互

`type: "loot"` 给玩家一个 loot crate icon，需要手动打开。但如果 quest 同时设置了 `autoclaim: true`，会发生什么？
- Autoclaim 自动完成 quest 并 claim rewards
- Loot type reward 期望手动交互
- 两者冲突：autoclaim 是否会跳过 loot reward？还是自动"打开" crate？

这是一个 UX 层面的矛盾，类似于 AP13 (Premature Item Submission)——系统行为与玩家预期不一致。

**建议:** MP34 增加一条注意事项：`type: "loot"` reward 不应与 `autoclaim: true` 组合使用。如果组合使用，触发 R34 的 WARNING。

---

### 三、Reward Economy 谱系

#### 完备性评级: B (覆盖主要场景，少量边界未处理)

三-pack 对比数据清晰地描绘了三种 reward economy 原型：
- **Random-dominant** (Craftoria): 21-92% random rewards
- **Loot-dominant** (E10): 10-39% loot rewards
- **Item-only** (MI:Foundation): ~100% item rewards

以下是遗漏的分析维度：

#### 遗漏 1: 混合型 reward economy 的合理性判定

一个大型 kitchen-sink 包内可能有意在不同 chapter 使用不同的 reward 模式：
- Tech chapters: item-only（确定性材料桥 MP14）
- Magic chapters: loot-dominant（随机性增加神秘感）
- Exploration chapters: random-dominant（惊喜奖励）

R34 (Reward Type Consistency) 会对这种**有意的混合**触发 INFO 提示。这不是 bug，但 R34 需要区分"有意混合"和"无意漂移"。

**建议:** R34 增加 chapter-level 分析维度：如果每个 chapter 内部的 reward type 一致（chapter 内 >90% 同类型），但 chapter 间不同，则 INFO 消息应调整为 "Pack uses chapter-specific reward economies ({list}). Verify this is intentional." 而非 "Pack mixes random and loot types."

#### 遗漏 2: Reward economy 的 progression arc

文档分析了 reward economy 的静态快照，但没有讨论 reward economy 随游戏进化的**动态模式**。一个常见的设计 arc 是：
- Early game: item-only（教玩家基础 mechanic，确定性 reward）
- Mid game: 引入 random/loot（增加 variability）
- Late game: choice reward（让玩家自选 endgame 装备）

如果包的 reward economy 不遵循任何 arc（随机分布），可能是 authoring 缺乏规划。

**建议:** 在 reward economy 分析中增加 progression arc 检测：按 chapter order_index 排列，观察 dominant reward type 是否呈现有序过渡（item → random → choice）。无序分布触发 INFO。这是一个 P3 级别的 nice-to-have 分析。

#### 遗漏 3: Repeatable quest 对 reward economy 的影响

`repeatable: true` 的 quest 可以无限次 claim reward。如果 repeatable quest 有 random reward，玩家可以反复刷 reward table——这是 AP8 (Reward Inflation) 的 amplified variant。

Reward economy 分析应该区分 one-time reward 和 repeatable reward 的经济影响。一个 repeatable quest 的 random reward table 如果有高价值 entry，可以彻底破坏经济平衡。

**建议:** 在 reward economy 分析中增加 repeatable quest 的特殊标注：repeatable + random/loot reward → WARNING: "Repeatable quest with random reward — verify table cannot be farmed for economy-breaking items."

---

### 四、Shape 语义 pack-specific 结论

#### 完备性评级: B (覆盖主要场景，少量边界未处理)

"Shape semantics are pack-specific" 这一结论得到了 21-pack 数据的支持。ATM 系列用 hexagon，MI:Foundation 用 diamond，Craftoria/E10 不用 shape。但以下边界情况值得探讨：

#### 遗漏 1: All-default 包的隐含 shape 层级系统

E10 的 "ZERO shape definitions" 可能掩盖了一个事实：E10 可能通过**其他视觉维度**表达层级。具体来说：
- **Quest size**: 大 size 的 quest 在视觉上是 milestone（R30 已部分检测）
- **Quest position**: 章节中心位置的 quest 可能是 hub（MP7/MP8）
- **Icon 差异**: Milestone quest 可能使用 mod-specific icon 而非常规 item icon

对于 all-default 包，R35 (Shape Semantics Consistency) 的分析基础不存在——没有 shape 变化可供分析。但 R35 应该意识到这种 "null result" 的含义，而不是简单地报告 "all default, nothing to check."

**建议:** R35 增加 all-default 包的特殊路径：当 >95% quest 使用 default shape 时，切换为 size-based 层级分析——检查 size 分布是否呈现有意义的 tier 结构（e.g. 多数 quest size=1.0, milestone size=2.0+）。如果 size 也全为 default，则报告 INFO: "Pack uses no visual hierarchy signals (shape or size). Consider adding visual markers for milestone quests."

#### 遗漏 2: Shape 的跨包 "accidental collision"

如果 skill 为 ATM 系列包生成 quest 时使用了 `diamond` shape（因为 diamond 在 MI:Foundation 中是 milestone shape），这在 ATM 包中会是一个"语义错误"——ATM 的 milestone shape 是 hexagon，diamond 在 ATM 中可能没有特殊含义或可能有不同含义。

R35 检查 pack 内部一致性，但不检查生成时是否"借用了"其他包的 shape 语义。

**建议:** 在 R35 的执行逻辑中，当生成新 quest 时，明确约束 shape 选择范围为该包已有的 shape vocabulary。如果包现有 quest 中从未使用过 diamond shape，新生成的 quest 也不应使用 diamond，除非用户在 Step 2 interview 中明确声明。

#### 遗漏 3: Shape 与 quest_link 的交互

FTB Quests 支持 `quest_link` task type，允许一个 quest 链接到另一个 chapter 的 quest。如果被链接的 quest 使用了 source chapter 不常见的 shape，这在视觉上可能不协调。

这与 Cycle 3 Review B 的 "nested chapters (quest_link)" 边界情况相同——quest_link 使用稀少，严重性极低。

**建议:** 维持 "known limitation" 状态，不处理。

---

### 五、Dependency Depth 分析

#### 完备性评级: C (遗漏显著边界情况)

R9 (Dependency Depth Reasonableness) 按 chapter 独立计算 max depth，这是正确的起点，但遗漏了一个对玩家体验至关重要的维度：

#### 遗漏 1: 跨 chapter 的有效深度 (Effective Depth)

R9 的 `MAX_DEPTH` 阈值按 chapter 独立应用。但考虑以下场景：

```
Chapter 1 (Getting Started): max_depth = 6  ← R9 通过 (kitchen-sink limit 8)
Chapter 2 (Iron Age): root depends_on Chapter 1 capstone, max_depth = 5  ← R9 通过
Chapter 3 (Steel Age): root depends_on Chapter 2 capstone, max_depth = 5  ← R9 通过
```

每个 chapter 单独看 depth 合理。但从玩家角度，Chapter 3 最后一个 quest 的**有效深度**是 6 + 5 + 5 = 16。这是 Monifactory expert pack 的典型模式（invisible chapter 链 + visible chapter 链叠加），但 R9 完全看不到。

**建议:** R9 增加 book-level effective depth 分析：

```
for each quest Q:
    effective_depth = Q.depth + max(ancestor_chain_cross_chapter_depth)
    if effective_depth > MAX_EFFECTIVE_DEPTH[pack_type]:
        INFO: "Quest has effective depth {effective_depth} across {n} chapters"
```

`MAX_EFFECTIVE_DEPTH` 可以设为 `MAX_DEPTH * 3`（允许最多 3 个 chapter 的链式深度叠加）。超过时触发 INFO（非 WARNING，因为跨 chapter 深度可能是有意设计）。

#### 遗漏 2: Chapter ordering 作为隐式依赖的 depth 膨胀

R22 只检查**显式**的跨 chapter dependency 引用。但 MP19 (Chapter-as-Stage) 描述了一种隐式依赖：chapter ordering (`order_index`) 暗示了进度顺序，即使没有显式 dependency wire。

当 pack author 依赖 chapter ordering 作为隐式 gating 时：
- 玩家**感知到** Chapter 2 在 Chapter 1 之后
- 但 quest book 的数据层面，Chapter 2 的 root quest 没有 dependency
- R9 将 Chapter 2 视为独立 chapter，不计算 Chapter 1 的深度

这导致 "effective depth 分析" 在这个场景中也无法工作——因为没有数据层面的 cross-chapter dependency 可供追踪。

**建议:** 在 effective depth 分析中增加一个 optional 模式：当 pack 声明使用 "strict chapter ordering" 时（Step 2 interview 中可询问），将 `order_index` 差异视为隐式 dependency，计算 effective depth。这需要 pack author 在 Step 2 中显式声明 "chapters are strictly ordered"。

#### 遗漏 3: Invisible chapter 对 depth 的放大效应

Monifactory 使用 invisible chapters (MP23) 作为 routing logic，visible chapters 的 quest 通过 cross-chapter dependency 引用 invisible chapter 的 quest。这 creates 一个 "depth tax"——visible quest 的 depth 被 invisible chapter 的内部 depth 隐式放大。

```
Visible Chapter A: quest at depth 3
  └── depends_on Invisible Chapter X: quest at depth 4
        └── depends_on Visible Chapter B: quest at depth 5
```

Visible Chapter A 的 quest 实际 effective depth = 3 + 4 + 5 = 12，但 R9 只看 Chapter A 的 max_depth = 3。

R9 的现有逻辑理论上可以追踪 cross-chapter dependency（包括 invisible chapter），但 invisible chapter 的 depth 被 R9 的 per-chapter 分析忽略——因为 R9 不会为 invisible chapter 生成 WARNING（invisible chapter 不直接面向玩家）。

**建议:** R9 增加 invisible chapter depth propagation：当 visible quest 依赖 invisible chapter 的 quest 时，将 invisible quest 的 depth 加到 visible quest 的 effective depth 中。这是遗漏 1 的特化场景，但值得单独强调，因为 invisible chapter 是 expert pack 中 depth 膨胀的主要来源。

#### 遗漏 4: Diamond pattern (MP9) 对 depth 的 "compression" 效应

MP9 (Diamond: A→{B,C}→D) 中，D 的 depth 是 max(depth(B), depth(C)) + 1，不是 depth(B) + depth(C) + 1。这意味着 diamond pattern **压缩**了有效深度——玩家可以选择较短的路径到达 D。

但当 B 和 C 的难度差异很大时（B 是 5 分钟任务，C 是 2 小时任务），depth 数值不反映实际时间投入。R9 只看 depth 数值，可能认为 diamond 后的 depth 合理，但玩家实际经历的时间可能远超预期。

**建议:** 这是 depth-as-time-proxy 的固有局限，不建议修改 R9。但在 R9 的 WARNING 消息中增加提示：depth 是拓扑距离，不反映任务复杂度或时间投入。对于 diamond pattern，建议用 `max(task_count * avg_time_per_task)` 估算时间投入。这是一个 P3 级别的 nice-to-have。

---

### 六、跨规则交互检查

以下是 Cycle 4 新增规则与现有规则的潜在冲突或重叠：

| 规则对 | 关系 | 分析 |
|---|---|---|
| R33 vs R10 (Reward-to-Dependent Bridge) | 互补 | R33 验证 table_id 存在性；R10 验证 reward item 是否桥接到后续 quest。Random/loot reward 因为产出 item 不确定，R10 无法做有效的 forward check——这应在 R10 中明确标注。 |
| R33 vs R12 (Reward Value Progression) | 依赖 | R12 需要估算 reward value。对于 random/loot reward，value 是 weighted average of table entries。R12 当前未说明如何处理随机 reward 的 value 估算。R33 的 table 数据可以为 R12 提供输入。 |
| R34 vs AP8 (Reward Inflation) | 间接关联 | R34 检查 reward type 一致性；AP8 检查 reward 时间分布。一个包可能 reward type 一致（全是 random）但仍有 inflation（early random table 有太高价值 entry）。两者检测不同维度。 |
| R35 vs R30 (Visual Hierarchy) | 重叠 | R35 检查 shape 一致性；R30 检查 shape/size 与语义角色的一致性。R35 的 "shape consistency within chapter" 与 R30 的 "milestone shape count <= 2 per chapter" 有重叠。建议 R35 作为 R30 的补充而非独立规则——R35 检测 pack-level shape vocabulary 漂移，R30 检测 chapter-level visual hierarchy。 |

---

### 七、遗漏的全局维度

以下是 Cycle 4 新增内容中完全没有涉及的维度：

#### 1. Reward table 的运行时性能

当一个 reward table 有 200+ entries 且 `loot_size: 10` 时，每次 claim 需要 10 次 weighted random selection from 200 entries。在 claim-all 场景下（50 quests 同时 claim），这是 500 次 random selection——可能导致 tick lag。

这与 AP15 (Command Reward Side Effect) 的 "claim-all storm" 是同构问题，但在 reward table 层面。

**建议:** MP34 增加 performance note：单个 reward table 建议 entries <= 50，loot_size <= 5。超过时考虑 table 拆分或 item grouping。

#### 2. Reward table 的可测试性

Quest config 的静态分析可以验证 table_id 存在性和格式正确性，但无法验证：
- Random seed 分布是否合理（是否有 entry 的 weight 太低以至于几乎不可能被 roll 到）
- Loot crate 的 UI 是否正确显示（loot type 的 crate icon 是否正确）
- Choice UI 是否在合理数量的 entry 下正常渲染

这些需要 in-game testing，类似于 AP12 (NBT Insensitivity) 需要运行时验证。

**建议:** MP34 中标注：reward table 的 runtime behavior 需要 in-game playtesting 验证。R32 (Chapter QA Coverage) 的 Signal 1 (dead-end detection) 可以部分覆盖——如果一个 quest 的 reward 是 table-based 且 table 为空，该 quest 在 R32 中会被标记为 "no reward, no dependent"。

#### 3. Localization (lang file) 对 reward table 的影响

Reward table 可以包含 `title` 字段用于 UI 显示。如果 title 使用 lang key（如 `reward_table.0414572B7C36F04F.title`）但 lang file 中没有对应条目，UI 显示原始 key 而非可读名称。

这与 Cycle 3 Review B 建议的 R35 (Lang File Key Consistency) 相关。

**建议:** 在 lang file 检查中增加 reward table title 的 key 验证。优先级低 (P3)。

---

### 八、总结

| 审查项 | 评级 | 遗漏数 | 最高严重遗漏 |
|---|---|---|---|
| R33 -- Reward Table Reference Integrity | **C** | 5 | 空 rewards 数组 / 全零 weight（silent failure 与 broken reference 等效）|
| MP34 -- Loot Table Reward 统一模型 | **B** | 4 | Autoclaim + loot type 冲突（UX 矛盾）|
| Reward Economy 谱系 | **B** | 3 | Repeatable quest 对 economy 的放大效应（AP8 amplified）|
| Shape 语义 pack-specific | **B** | 3 | All-default 包的隐含 size-based 层级（R35 对 null result 无处理）|
| Dependency depth 分析 | **C** | 4 | 跨 chapter effective depth 完全未覆盖（R9 per-chapter 盲区）|

**最高优先级行动 (按严重性排序):**

1. **R33 扩展为 "Reward Table Integrity"** -- 不仅检查 table_id 存在性，还检查 rewards 数组非空、total weight > 0、loot_size > 0、item ID 有效性。这是 P1 级别，因为空 table / 零 weight 与 broken reference 对玩家的影响完全一致：silent reward failure。

2. **R9 增加 book-level effective depth** -- 当前 per-chapter depth 分析在跨 chapter dependency 场景下给出 false sense of security。至少应计算 cross-chapter chain 的 effective depth，并在 invisible chapter 参与时传播 depth。

3. **R35 增加 all-default 包降级路径** -- 当 shape 全为 default 时，切换为 size-based 层级分析。否则 R35 对 E10 这类包完全无用。

4. **R34 增加 chapter-level 粒度** -- 区分 "pack-level 有意混合"（每 chapter 内部一致）和 "chapter-level 无意漂移"（同一 chapter 内混合 random 和 loot）。

5. **MP34 补充 autoclaim + loot 冲突** -- `type: "loot"` + `autoclaim: true` 的交互行为需要明确文档化，并在 R34 或 R33 中检测。

6. **Reward economy 增加 repeatable quest 特殊标注** -- Repeatable + random reward 是 economy-breaking 的高风险组合。
