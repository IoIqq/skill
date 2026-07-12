## 审查员 B -- 完备性质疑 (Cycle 3 新增内容)

审查日期: 2026-07-07
审查范围: progression-rules.md §9 (R30-R32), anti-patterns.md (AP17/AP18), micro-patterns.md (MP33/MP34)
审查方法: 逐规则质疑边界情况、跨规则重叠、task/reward type 覆盖冲突

---

### 一、直接修正 (已写入源文件)

#### Fix 1: R31 `r.value` 属性不存在 (BUG)

**位置:** `progression-rules.md` R31 伪代码, 原 line 1527
**问题:** `total_xp = sum(r.value for r in xp_rewards if hasattr(r, 'value'))` -- XP reward 的实际字段名是 `xp_levels` (对 xp_levels 类型) 或 `xp` (对 xp 类型), 不存在 `value` 属性。`hasattr(r, 'value')` 始终为 False, `total_xp` 始终为 0, WARNING 消息显示 `value=0`, 完全无意义。
**修正:** 改为 `getattr(r, 'xp_levels', getattr(r, 'xp', 0))`, 按 FTB Quests 实际 reward schema 取值。
**验证:** Craftoria #289 的示例配置 `{ type: "xp_levels", xp_levels: 5 }` 确认字段名是 `xp_levels`, 不是 `value`。

#### Fix 2: R31 milestone shape 列表缺少 `diamond`

**位置:** `progression-rules.md` R31 伪代码, 原 line 1529
**问题:** milestone 检测的 shape 列表 `("gear", "pentagon", "hexagon")` 缺少 `diamond`。ATM-10 AllTheModium chapter 的 `default_quest_shape: "diamond"` (MP20 Shape-as-Tier Signal), 是明确的 milestone shape。此外 `hexagon` 在 ATM-10 中既用于 milestone (Mekanism/Ars Nouveau) 也用于 cross-link navigation nodes, 存在歧义。
**修正:** 改为 `("gear", "pentagon", "hexagon", "diamond")` 并标注 hexagon 歧义。

#### Fix 3: R31 flat XP 误报 (中等严重性)

**位置:** `progression-rules.md` R31 伪代码, WARNING 触发条件
**问题:** R31 的 reward type filter 同时匹配 `xp_levels` 和 `xp`, 但 WARNING 消息说 "xp_levels rewards create wildly inconsistent value"。flat XP (`xp` type, e.g. `{ type: "xp", xp: 100 }`) 不受 claim timing 影响 -- 100 XP 始终是 100 XP。当前代码会对仅含 flat XP 的 routine quest 也触发 WARNING, 产生 false positive。
**修正:** 在 WARNING 触发条件前添加 `has_xp_levels` guard, 仅当 quest 含有 `xp_levels` 类型 reward (非 flat xp) 时才触发 WARNING。

#### Fix 4: R32 Signal 4 catalog chapter 误报 (中等严重性)

**位置:** `progression-rules.md` R32 伪代码, Signal 4
**问题:** Signal 4 (`optional_count == 0 and len(quests) > 10`) 对 catalog chapter 产生 false positive。Create: Delight 的 Mouse_Chef (304 quests, 大多是 independent island MP10) 不使用 `optional` flag -- 这些 quest 本身就是独立可选内容。Signal 4 会误报为 "100% mandatory chapters often indicate untested content"。
**修正:** 在 Signal 4 前添加 catalog chapter 检测: 如果 >70% 的 quest 是 independent islands (无 dependencies 且无 dependents), 则跳过 Signal 4。

---

### 二、R30-R32 边界情况质疑

#### R30 -- Quest Visual Hierarchy & Size Consistency

**边界 1: optional 优先级遮蔽 milestone 检测**

R30 的分类逻辑:
```
if Q.optional:        → optionals
elif dependents >= 3: → milestones
else:                 → routines
```

如果一个 quest 同时是 `optional: true` 且有 >= 3 dependents, 它被分入 optionals, 不参与 milestone size 比较。理论上 optional quest 不应有 >= 3 dependents (R29 已覆盖), 但如果发生 (e.g. 一个 optional hub 解锁多条 side-content), R30 的 milestone check 会完全跳过它。

**严重性:** 低。R29 应捕获底层问题。R30 跳过此类 quest 是合理的防御行为。
**建议:** 无需修改。但在 R30 文档中添加一行注释说明此优先级。

**边界 2: multi-group packs 的跨 chapter 视觉一致性**

R30 按 chapter 独立运行。在 ATM-10 (10 groups, 64 chapters) 中, 同一 group 内的多个 chapter (e.g. "Getting Started" group 含 3 个 chapter) 各自的 milestone size 标准可能不一致。Chapter A 的 milestone size=2.0, Chapter B 的 milestone size=1.5 -- 两者各自通过 R30, 但 group-level 视觉不一致。

**严重性:** 低。这属于 "nice to have" 的跨 chapter 一致性, 非功能性问题。
**建议:** 在 R30 末尾添加一条可选的 group-level check: "If pack has chapter groups with 2+ chapters, compare milestone sizes across chapters within the same group."

**边界 3: nested chapters (quest_link)**

FTB Quests 支持 `quest_link` task type, 允许一个 quest 链接到另一个 chapter 的 quest。R30 按 chapter 分类 quest, 但通过 quest_link 被引用的 quest 在语义上属于 "父" chapter 的进度流。R30 不检查 linked quest 的视觉属性是否与父 chapter 一致。

**严重性:** 极低。quest_link 使用稀少 (Monifactory raw data 中出现但非主流)。
**建议:** 不处理。记录为 "known limitation"。

#### R31 -- XP-Level Reward Relativity

**边界 1 (已修正):** `r.value` 属性名错误, 见 Fix 1。

**边界 2: milestone 误分类**

R31 的 milestone 检测使用 4 个 OR 条件:
1. `len(dependents) >= 3`
2. `is_capstone(Q, chapter)`
3. `Q.size > chapter_median_size * 1.5`
4. `Q.shape in ATM shapes`

在小 chapter (5-8 quests) 中, 一个有 2 个 dependent 的 quest 不会被标记为 milestone (条件 1 不满足), 但如果它的 size 等于 median (条件 3 不满足) 且 shape 是默认的 (条件 4 不满足), 则被误分类为 routine。该 quest 上的 xp_levels reward 会触发 WARNING, 但实际上它可能是一个 "minor milestone"。

**严重性:** 低。WARNING 消息本身是有用的提醒, 即使对 minor milestone 触发也不算误报 -- 它提醒作者审视 xp_levels 在此位置是否合理。
**建议:** 可考虑将 dependent 阈值从 3 降为 2, 但当前 3 的阈值更保守 (减少 noise), 可接受。

**边界 3: `xp` (flat XP) vs `xp_levels` (XP levels) 区分**

R31 的 reward type filter 同时匹配 `xp_levels` 和 `xp`。但 `xp` (flat XP points) 不受 "claim timing" 问题影响 -- 100 XP 始终是 100 XP, 与玩家等级无关。R31 的 WARNING 消息建议 "using flat XP (xp_points) instead of XP levels", 但代码本身对两种类型一视同仁地触发 WARNING。

**严重性:** 中。flat XP 不应触发 "value drift" WARNING。
**建议:** 在 WARNING 触发条件中添加: `if any(r.type in ("ftbquests:xp_levels", "xp_levels") for r in xp_rewards)` -- 仅当存在 xp_levels (非 flat xp) 时才触发 WARNING。Flat xp 可安全跳过。

#### R32 -- Chapter QA Coverage Heuristic

**边界 1: catalog chapter 的 Signal 4 误报**

Signal 4: `optional_count == 0 and len(quests) > 10` → INFO。但 catalog chapter (如 Create: Delight 的 Mouse_Chef, 304 quests, 大多是 independent island MP10) 天然不使用 `optional` flag -- 这些 quest 本身就是全部可选的 (无 dependency, 无顺序)。Signal 4 对 catalog chapter 会产生 false positive。

**严重性:** 中。一个 304-quest catalog chapter 会触发 "100% mandatory chapters often indicate untested content" 的 INFO, 这是误导。
**建议:** 在 Signal 4 中添加 catalog chapter 排除: 如果 chapter 中 >70% 的 quest 是 independent islands (无 dependencies 且无 dependents), 则跳过 Signal 4。

**边界 2: `is_capstone` 未定义**

R32 Signal 1 (dead-end) 排除 capstone: `not is_capstone(Q, C)`, 但 R32 伪代码中未定义 `is_capstone` 的实现。R13 使用 `len(Q.dependencies) >= 5`, R30 使用 `is_capstone(Q, C)` 也无内联定义。

**严重性:** 低。`is_capstone` 可作为共享 utility function 定义一次, 但当前各规则引用它时未统一语义。
**建议:** 在 progression-rules.md 的 §0 (降级策略与内置映射) 或新小节中添加:
```
def is_capstone(Q, chapter):
    return len(Q.dependencies) >= 5 or Q.size == max(q.size for q in chapter.quests)
```

---

### 三、AP17/AP18 与其他 AP 的重叠检查

| 对比 | 重叠程度 | 分析 |
|---|---|---|
| AP17 vs AP8 (Reward Inflation) | 互补, 非重叠 | AP8 = "太早给太多"; AP17 = "给的值不可预测"。一个关于时间, 一个关于方差。文档已正确标注关系。 |
| AP17 vs AP6 (Dead-End Reward) | 无重叠 | AP6 = reward 不连接后续 quest; AP17 = reward 价值随等级漂移。完全不同的问题。 |
| AP18 vs AP6 (Dead-End Reward) | 部分互补 | AP6 是单 quest 级别的 dead-end; AP18 是 chain 级别的 reward desert。已在 anti-patterns.md 中标注。 |
| AP18 vs AP8 (Reward Inflation) | 互补 | AP8 = "给太多"; AP18 = "给太少"。已在 anti-patterns.md 中标注为 complement。 |
| AP17 vs AP15 (Command Side Effect) | 无重叠 | 完全不同的 reward 类型和问题域。 |
| AP18 vs AP4 (Wrong Gating) | 间接关联 | AP4 的过度 gating 可能导致 reward desert (被阻挡的 quest 也无法领取 reward), 但根因不同。Craftoria #231 同时触发 AP4 + AP18 证明了关联性, 但两者捕获不同维度。 |

**结论:** AP17/AP18 与现有 AP 无实质性重叠。文档中的 cross-reference 已充分标注关系。无需调整。

---

### 四、MP33/MP34 状态

#### 关键发现: MP33/MP34 未被添加到 micro-patterns.md

前两轮 Review B (2026-07-05, 2026-07-06) 分别提出了 MP33 和 MP34:

| 编号 | 提议名称 | 提议来源 | 当前状态 |
|---|---|---|---|
| MP33 | Advancement Gate (advancement task/reward 桥接) | review-b-completeness_2026-07-05.md, review-b-completeness_2026-07-06.md | **未添加 -- Deferred** |
| MP34 | Location Discovery Gate / Team-Aware Reward Design | review-b-completeness_2026-07-05.md (team reward), review-b-completeness_2026-07-06.md (location) | **未添加 -- Deferred** |

`.research-lessons.md` 明确记录: "MP33-MP34: Not yet in micro-patterns.md... No player feedback specifically discusses these as patterns -- they appear as incidental task/reward types rather than distinct design decisions worth their own micro-pattern. **Deferred.**"

#### MP33 必要性再评估

`AdvancementTask` 在 FTB Quests 源码中存在 (`AdvancementTask.java`), 且在以下场景有意义:
- RPG/adventure 包使用 datapack advancement 做进度 (Finality Genesis 有 `advancement` task type)
- Expert 包的 invisible infrastructure 可能使用 advancement 替代 gamestage

但 Cycle 3 的 23 个审计包中, advancement task 使用率极低 (Finality Genesis 中出现但非主要模式), 且无玩家反馈将其识别为设计问题。**维持 Deferred 决定合理。**

#### MP34 必要性再评估

两个 MP34 候选:
1. **Location Discovery Gate** (dimension + x/y/z/radius): FTB Quests 有 `LocationTask` 类, 但 23 个包中无实际使用数据。纯理论模式。
2. **Team-Aware Reward Design**: R29 已覆盖团队进度一致性, 但 reward 分配细节 (谁获得 material bridge 的物品) 确实没有专门的 micro-pattern。

**建议:** MP34 (Team-Aware Reward) 值得重新考虑。R29 在 progression-rules.md 中以 WARNING/INFO 级别检测了 team 场景下的 material bridge 和 fan-in, 但 micro-patterns.md 缺少一个 "how to do it right" 的正向模式。建议添加 **MP33 -- Team-Aware Reward Distribution**: 在 team mode 下, material bridge reward 应使用 `autoclaim: false` 或 `team_reward: true` (如果 FTB Quests 支持) 确保所有团队成员获得物品。

---

### 五、MP33/MP34 的 task/reward type 覆盖冲突

由于 MP33/MP34 不存在, 不存在与现有 MP 的冲突。但以下是覆盖缺口:

| Task/Reward Type | 现有 MP 覆盖 | 缺口 |
|---|---|---|
| `advancement` task | 无专门 MP (R14 间接涉及) | 缺少 "advancement task 如何与 datapack 联动" 的指导 |
| `location` task | 无 | 完全未覆盖, 但使用率极低 |
| `loot` reward (`random` type) | 无专门 MP (MP8 示例中出现) | 缺少 "loot table reward 的 idempotency 和 value 估算" 指导 |
| `command` reward | MP29 (Command Reward) | 已覆盖, 但 MP29 未提及 AP15 的 claim-all storm 风险 |

---

### 六、§9 QA Standards 完整性检查

§9 当前包含 R30 (视觉层级), R31 (XP 奖励), R32 (QA 覆盖)。作为 "QA & Formatting Standards" 章节, 以下维度是否应纳入:

#### 应该考虑的新规则

| 候选规则 | 覆盖的维度 | 现有规则是否已覆盖 | 建议 |
|---|---|---|---|
| **R33 -- Description Spell/Typo Check** | description 文本中的拼写错误、typo | R23 只检查 item ID 的存在性, 不检查自然语言文本 | **建议添加。** AI 生成的 description 中 typo 是高频问题。可用 dictionary lookup + common typo list (e.g. "recieve" → "receive", "seperate" → "separate") 实现, Step 4 P2 级别。 |
| **R34 -- Dependency Graph Visualization Advisory** | 建议作者使用 graphviz/mermaid 可视化依赖图 | R5/R6 做图遍历检测, 但不建议可视化 | **建议作为 INFO 提示, 非独立规则。** 在 R5/R20 的 WARNING 消息中添加: "Consider visualizing this chapter's dependency graph for manual review." |
| **R35 -- Lang File Key Consistency** | `quest.<id>.quest_desc` lang key 与实际 quest ID 的一致性 | R18 检查 `lang_has_key()`, 但仅检查存在性 | **建议添加。** 当 quest ID 变更 (AP16 场景) 但 lang key 未同步更新时, description 变为空。可在 Step 5 P2 级别检测 orphan lang keys 和 missing keys。 |
| **Quest Icon Audit** | quest icon 是否与 task item 一致 | R30 提到 icon 字段但无检查 | **不建议添加。** Icon 通常是 task item 的自动推断, 手动 icon 设置的错误率低且影响小。 |
| **Quest Title Length/Uniqueness** | title 不为空且不与同 chapter 其他 quest 重复 | 无覆盖 | **低优先级。** 可在 R32 添加 Signal 5: "duplicate quest titles within chapter" 作为 QA signal。 |

#### §9 结构建议

当前 §9 有三条规则 (R30-R32), 分属两个维度:
- 呈现层: R30 (视觉), R31 (reward 一致性)
- 测试覆盖层: R32 (QA heuristic)

如果添加 R33 (typo) 和 R35 (lang key), §9 将扩展为四条规则, 覆盖三个维度:
- 呈现层: R30, R31
- 文本质量层: R33
- 测试覆盖层: R32, R35

建议将 §9 标题从 "QA & Formatting Standards" 扩展为 "QA, Formatting & Text Quality Standards" 以反映新增维度。

---

### 七、总结

| 类别 | 发现数 | 严重性分布 |
|---|---|---|
| 直接修正 (已修复) | 4 | 1 BUG (R31 `r.value`), 2 误报 (R31 flat xp, R32 catalog), 1 遗漏 (R31 shape list) |
| R30-R32 边界情况 | 4 | 4 低 (optional 优先级, multi-group, nested chapters, milestone 阈值) |
| AP17/AP18 重叠 | 0 实质重叠 | 全部为互补关系, 已正确标注 |
| MP33/MP34 状态 | 1 关键 | 未添加到文件中; MP34 (team reward) 值得重新考虑 |
| §9 覆盖缺口 | 3 建议 | R33 (typo check) 价值最高, R35 (lang key) 次之, dependency visualization 可作提示嵌入现有规则 |

**最高优先级行动:**
1. ~~修正 R31 `r.value` bug~~ (已完成)
2. ~~修正 R31 milestone shape list~~ (已完成)
3. ~~修正 R31 flat xp 误报~~ (已完成)
4. ~~修正 R32 Signal 4 catalog 误报~~ (已完成)
5. 决定 MP33/MP34: 正式添加 MP33 (Team-Aware Reward Distribution) 或明确维持 Deferred
6. 评估 R33 (description typo check) 是否值得作为 Cycle 3 新增规则
7. 统一 `is_capstone()` 函数定义 (R13/R30/R31/R32 共享)
