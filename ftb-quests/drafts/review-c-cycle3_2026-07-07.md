## 审查员 C — 实用性审查 (Cycle 3: R30-R32)

> **审查日期：** 2026-07-07
> **审查范围：** progression-rules.md §9 (R30-R32) + 执行优先级表, SKILL.md 工作流
> **核心问题：** Cycle 3 新增的三条规则在 AI agent 的实际工作流中能否被执行？

---

### 一、R30 — Quest Visual Hierarchy & Size Consistency

#### 质疑：agent 在 Step 4 生成时能检查 size/shape 一致性吗？

**短回答：部分可以，但完整检查需要 Step 5。**

**数据分析：**

R30 的检查需要三类数据：

| 数据 | 局部可用性 | 说明 |
|---|---|---|
| `Q.size`, `Q.shape`, `Q.optional` | 完全局部 | 当前 quest 自身的字段，生成时即可访问 |
| `find_dependents(Q)` — 有多少 quest 依赖 Q | 需要完整依赖图 | 下游 quest 尚未生成（Step 4 按依赖顺序生成，下游在后面） |
| `is_capstone(Q, C)` — 是否为 chapter capstone | 可用 outline 推断 | Step 2 outline 已标注 capstone/convergence 节点 |
| 同 chapter 所有 quest 的 size 集合 | 部分可用 | 只有已生成的 quest 可见，未生成的不可见 |

**Step 4 能做的（简化版 Check 1）：**

agent 在 Step 4 生成 quest 时，已经拥有 Step 2 的 approved outline，其中标注了 capstone 和 convergence 节点。因此：
- agent 知道当前 quest 是否是 milestone（从 outline 的角色标注）
- agent 可以比较当前 quest 的 size 与同 chapter **已生成** quest 的 size
- 如果当前 quest 是 routine 但 size > 已生成的 milestone 的 size，可以立即 WARNING

**Step 4 做不到的：**

- 无法计算 `max_routine_size`（需要所有 routine quest 的 size）
- 无法执行 Check 3（milestone shape 一致性——需要所有 milestone 的 shape 集合）
- 后生成的 quest 无法与先生成的 quest 做反向比较

**实用价值评估：**

R30 的实用价值在三条新规则中最低。原因：
1. **视觉层级是 cosmetic 问题**——不影响游戏逻辑或玩家进度。一个 size 不一致的 quest book 仍然可以正常游玩，只是视觉信号有误导。
2. **agent 的 size/shape 选择已有 SKILL.md 约束**——SKILL.md 的 "Shape & size = semantic encoding" 表已经规定了各角色的默认 size 和 shape（circle/1.0 为 routine，gear/2.0 为 milestone 等）。如果 agent 遵循此表，R30 的大多数违规不会发生。
3. **Monifactory 的 "Larger quests for milestones" 标准** 是显式设计哲学，但不是所有包都遵循——ATM 系列用 shape（而非 size）作为主要语义编码器（ATM9/10 数据：default size 1.0 占 70%，size 变化极少）。

**建议：** R30 保持 P3 合理。Step 4 的简化版检查（outline 已知的 milestone vs 当前 quest）已经足够捕捉严重违规。Step 5 的完整版是 nice-to-have，但不应占用太多 validation budget。

---

### 二、R31 — XP-Level Reward Relativity

#### 质疑：agent 怎么知道玩家的当前等级？xp_levels 的具体值怎么验证？

**短回答：agent 不需要知道玩家等级。R31 检查的是结构位置，不是具体数值。**

**规则的真正检查对象：**

R31 不检查 "xp_levels 的值是否合理"——它检查 "xp_levels reward 是否放在了正确的位置"。具体逻辑：

```
IF quest has xp_levels reward
AND quest is NOT a milestone (dependents < 3, not capstone, not milestone shape)
THEN WARNING: xp_levels on routine quest creates value drift
```

所有输入数据都是结构性的：
- `r.type in ("ftbquests:xp_levels", ...)` — reward 类型，纯字符串匹配
- `find_dependents(Q)` — 下游依赖数。**Step 4 可用**：按依赖顺序生成时，当前 quest 的 dependents 中已生成的部分可以计数；未生成的部分可以通过 outline 中的 `depends_on` 反向推算（outline 中哪些 quest 声明了 `depends_on: [当前quest]`）
- `is_capstone(Q, C)` — 从 outline 已知
- `Q.shape` — 当前 quest 自身的字段

**为什么不需要玩家等级：**

R31 的核心洞察来自 Craftoria #289：xp_levels reward 的价值随玩家领取时的等级漂移。这个漂移不是"在某个等级时值多少"的问题——而是"同一个 reward 在不同时间点价值不一致"的问题。解决方案不是调整数值，而是限制 xp_levels 的出现位置：只放在 milestone/capstone 上，因为玩家通常会在固定时间点领取 milestone reward（漂移最小），而 routine quest 的领取时间不可预测（漂移最大）。

**xp_levels 具体值的处理：**

规则代码中的 `total_xp = sum(r.value for r in xp_rewards)` 只是用于 WARNING 消息的信息展示，不参与判断逻辑。判断逻辑只看 "有/没有 xp_levels reward" + "是不是 milestone"。agent 不需要验证 xp_levels 的数值是否合理——那是 R12 (Reward Value Progression) 的职责范围。

**实用价值评估：**

R31 是三条新规则中实用性最高的：
1. **完全可在 Step 4 执行**——数据完全局部（reward 类型 + outline 角色）
2. **检查逻辑简单**——二值判断（milestone vs routine），无灰度
3. **有明确的 Craftoria issue 作为实证支持**——#289 是唯一公开记录此问题的来源，但问题描述具体且可信
4. **修复建议具体可操作**——WARNING 消息直接给出三个替代方案（移到 milestone、换 item reward、用 flat XP）

**建议：** R31 正确定位为 Step 4 P2。无需改动。

---

### 三、R32 — Chapter QA Coverage Heuristic

#### 质疑：这是 meta 规则，agent 能在生成后执行吗？

**短回答：能执行，但与已有规则存在显著重叠，独立价值存疑。**

**R32 的四个信号与已有规则的覆盖重叠：**

| R32 信号 | 检查内容 | 已有规则覆盖 | 重叠度 |
|---|---|---|---|
| Signal 1: Dead-end | 无 reward + 无 dependent + 非 optional + 非 capstone | **R10** (reward bridge) + **R6** (unreachable quest) | 高——R10 已经标记 dead-end reward，R6 标记不可达 quest。R32 的额外信息是"无 reward 且无 dependent"的组合，但单独无 reward 的 quest 不一定是 bug（可能是 acknowledgement gate） |
| Signal 2: Empty description | >30% quest 的 description < 20 字符 | **R18** (description coverage) | 极高——R18 逐 quest 检查 description 缺失，R32 只是把同样的检查聚合成 chapter-level 比例。R32 的阈值 (30%) 比 R18 (any missing) 更宽松，实际上不会发现 R18 遗漏的问题 |
| Signal 3: Dependency orphan | quest 的所有 dependency 都来自外部 chapter + 无内部前驱 | **R22** (cross-chapter dependency) + **R6** (unreachable) | 中高——R22 检查悬空引用，R6 检查不可达。R32 的额外信号是"全部外部依赖 + 无内部前驱"的组合，但这在 cross-chapter bridge quest 中是正常的 |
| Signal 4: Completion sanity | >10 quest 的 chapter 有 0 个 optional | **R20** (chapter completion testability) + **R9** (dependency depth) | 中——R20 检查结构可完成性，R32 的 Signal 4 只是提示"全部 mandatory 可能不合理"，是启发式而非硬检查 |

**R32 的独立价值：**

R32 的理论贡献是将多个信号组合成一个 "chapter 是否经过 playtesting" 的综合判断。单条 warning 不代表问题，多条同时触发是强烈的"未经测试"信号。

但实际上：
- 如果 R5/R6/R10/R18/R20/R22 都已经执行并通过，R32 几乎不可能触发新的 warning
- 如果上述规则中有未修复的 violation，R32 只是重复标记同样的问题
- R32 最有价值的场景是：所有单项规则都通过，但组合起来暗示 chapter 缺乏整体设计审查。这是一个 **人类审查者** 的判断，不是 agent 能自动化执行的

**Step 5 执行可行性：**

技术上可行——所有数据在 Step 5 可用（完整 chapter 结构、跨 chapter 依赖图）。但 agent 执行 R32 的 token 成本约等于运行一次 R6 + R10 + R18 + R22 的总和，而产出的新信息接近零。

**建议：** R32 可以保留为 Step 5 P3，但应在规则文本中明确其与 R6/R10/R18/R22 的重叠关系，让 agent 在 Step 5 可以选择性地只运行 R32 中不与已有规则重叠的部分（实际上只剩 Signal 4：全 mandatory chapter 的 heuristic 提示）。

---

### 四、R30/R32 的 P3 优先级问题

#### 质疑：P3 规则会不会被永远跳过？

**发现两个层面的问题：**

**1. 工作流遗漏（已修正）：**

SKILL.md 的 Step 5 描述中，progression-rules 的执行范围标注为 **"R1–R23"**（第 434 行），而不是 R1–R32。这意味着即使 agent 按照 SKILL.md 的指示执行 Step 5，R24–R32 都不在执行计划中。

同样，SKILL.md 的 Step 4 "Generation-time progression checks"（第 132 行）列出的 Step 4 规则为 "R1–R4, R10–R13, R14–R17"，遗漏了 R28（Step 4 P0, command safety）和 R31（Step 4 P2, XP-level relativity）。

**已执行小修正：**
- Step 5 范围：R1–R23 → R1–R32
- Step 4 范围：补充 R28、R31

**2. P3 永远跳过的风险：**

progression-rules.md 的设计原则明确指出：

> "Step 4 只做 3-5 个关键局部检查（P0 级 ERROR + P1 级 WARNING），其余推迟到 Step 5 全量分析。"

这个设计是合理的——Step 4 不应被过多的检查拖慢。但 Step 5 本身的执行也存在优先级梯度：

| 优先级 | 执行概率 | 说明 |
|---|---|---|
| P0 (R5/R6/R20/R22) | ~100% | 结构性问题，不修复则 quest book 不可用 |
| P1 (R7/R10/R11/R14/R16/R29) | ~90% | 重要但非致命，agent 通常会执行 |
| P2 (R1-R4 full/R8/R9/R12/R13/R15/R19) | ~60% | 有价值但耗时，budget 紧张时可能跳过 |
| P3 (R17/R21/R24-R26/AP10/AP11/**R30/R32**) | ~20% | 低优先级，大多数 session 不会到达 |

R30 和 R32 作为 P3 中的最后两条（执行优先级表中排名 #30 和 #31），在实际工作流中确实面临被永远跳过的风险。

**但这不一定是问题：**

- R30（视觉层级）：SKILL.md 的 Shape & size 表已经编码了视觉层级的默认值，agent 遵循此表即隐式满足 R30。显式检查的增量价值有限。
- R32（QA 覆盖）：如上分析，与已有规则高度重叠。如果 P0–P2 规则都已执行，R32 的增量检出接近零。

**建议：** 保持 R30/R32 为 P3。与其提高它们的优先级（会挤占更重要规则的执行预算），不如确保 P0–P2 规则的完整执行。R30/R32 的价值主要在人工审查阶段——它们是"checklist for human playtesters"而非"automated agent checks"。

---

### 五、总结与建议

| 规则 | 实用性评级 | 关键发现 | 建议 |
|---|---|---|---|
| **R30** | 中 | Step 4 可做简化检查（outline 已知 milestone），完整检查需 Step 5。但 SKILL.md 的 shape/size 表已隐式约束了大多数违规 | 保持 P3，Step 4 简化版已够用 |
| **R31** | 高 | 不需要玩家等级。检查结构位置而非数值。完全可在 Step 4 执行 | 保持 Step 4 P2。已修正 SKILL.md 遗漏 |
| **R32** | 低 | 与 R6/R10/R18/R22 高度重叠。独立价值主要作为"playtesting checklist"供人类审查者使用 | 保持 P3，考虑在规则文本中标注重叠关系 |

**已执行的修正：**

1. **SKILL.md 第 132 行**：Step 4 规则引用从 `R1–R4, R10–R13, R14–R17` 扩展为 `R1–R4, R5(增量), R6(局部), R7, R10(反向), R14–R17, R18, R22, R23, R28, R31`，补全了遗漏的 Step 4 规则。
2. **SKILL.md 第 434 行**：Step 5 范围从 `R1–R23` 修正为 `R1–R32`，将 Cycle 3 新增规则纳入执行范围。
