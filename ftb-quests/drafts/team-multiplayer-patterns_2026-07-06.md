# 团队/多人模式设计模式（Team & Multiplayer Patterns）

**草稿日期：** 2026-07-06
**来源：** Review B（完备性审查）§未覆盖的场景 — "多人/团队场景，影响: 高"
**状态：** 草稿，待整合到 micro-patterns.md（新增 PP8）和 SKILL.md Step 2 采访流程

---

## 背景

FTB Quests 的核心卖点之一是团队任务（"designed for teams, allowing you and your friends to complete quests together"），FTB Teams 提供团队系统，quest 完成可以按团队共享。然而，三份设计文档（micro-patterns.md, anti-patterns.md, progression-rules.md）的设计语境默认是单人玩家，团队/多人场景完全零覆盖。

本文档梳理团队模式下 quest 设计的独有问题，提出新增的 Player-Perspective Pattern (PP8) 和相关的设计考量，为后续整合到主文档做准备。

---

## 1. 团队进度共享模式

FTB Teams 允许团队成员共享 quest 进度。当一个成员完成 item task 时，所有团队成员的任务进度都更新。这对现有 MP 模式的含义：

### MP1 (Single-Item Gate) 在团队模式下

**单人语义：** "玩家需要提交 N 个物品来完成任务。"
**团队语义：** "团队中任何一个成员提交 N 个物品即完成。"

这意味着 quest 的经济性改变了：团队可以分工收集材料。一个需要 64 个 iron ingot 的 quest，在单人模式下是一个 moderate grind；在 4 人团队模式下，每人只需收集 16 个。quest 的 `count` 值在团队模式下可能需要调高，或者接受"团队效率"作为多人模式的固有奖励。

**设计考量：** 如果 quest 的 `count` 值是为单人设计的（例如 64），团队模式下可能过于轻松。反之，如果为团队设计（例如 256），单人模式下可能过于 grind。建议：
- 在 quest description 中注明预期人数，或
- 使用 `consume_items: true` 确保团队模式下每个成员都需要贡献

### MP8 (Fan-In / Convergence) 在团队模式下

**单人语义：** "玩家需要完成所有 10 个 component sub-tree，然后合成 capstone。"
**团队语义：** "10 个 component sub-tree 可以由 10 个团队成员分别完成。Capstone quest 是'团队合成'而非'个人合成'。"

这对 ATM Star 类的 capstone quest 有深远影响。单人模式下，ATM Star 是 endgame grind 的巅峰——一个人收集 10 个 mod 的组件。团队模式下，这变成了一个分工协作项目——每人负责一个 mod 线。设计体验完全不同。

**设计考量：** Capstone quest 的描述应该考虑两种场景：
- 单人："This is the ultimate challenge — bring together components from 10 different mods."
- 团队："Assign each team member a component sub-tree to work on in parallel."

### MP14 (Material Bridge) 在团队模式下

**单人语义：** "Quest N 的 reward 物品是 Quest N+1 的 task 物品，玩家完成 N 后自动拥有 N+1 的材料。"
**团队语义：** "Reward 是每个团队成员都获得，还是只有提交者获得？"

这取决于 FTB Teams 的 reward 分配设置。如果只有提交者获得 reward item，其他团队成员没有下一步的材料——material bridge 失效。这是一个关键的设计陷阱。

**设计考量：**
- 在 team-relevant quest 的 description 中注明："Each team member should claim this reward individually" 或 "Only the submitting player receives the reward item"
- 或者使用 `{p}` 相关的 command reward 来确保每个成员都获得材料

---

## 2. 团队模式下的 Anti-Patterns

### AP-Team-1: The Free Rider Problem（搭便车问题）

**Symptom:** 一个玩家完成所有 quest，其他团队成员被动获得进度。Quest book 对搭便车者没有教学价值——他们看到 quest 完成了但从未真正理解 mod 的 mechanic。

**Root cause:** FTB Teams 的进度共享机制对所有 team member 统一更新。当 Player A 完成一个 checkmark task（tutorial quest），Player B 也自动"完成"了——但 Player B 可能从未打开过 quest book 阅读 tutorial text。

**Consequence:** 团队中只有一个人真正理解 modpack 的 progression system。其他成员在游戏后期遇到困难时缺乏基础知识，因为他们跳过了所有的教学内容。

**Fix:** 
- 对于关键 tutorial quest，使用个人化的 task type（例如要求每个成员分别提交一个物品，而非 checkmark）
- 在 quest description 中注明"每个团队成员都应阅读此教程"
- 使用 `consume_items: true` 确保每个成员都需要实际贡献材料

### AP-Team-2: The Divergent Path Problem（路径分歧问题）

**Symptom:** 团队中不同成员选择了不同的 optional path（MP9 Diamond），导致 mandatory quest 的 dependency 条件在某些成员看来已满足、在另一些成员看来未满足。

**Root cause:** `dependency_requirement: "one_completed"` 在团队模式下可能意味着"团队中任何一个人完成了一个选项即可"。如果 Player A 选择了 Path X，Player B 选择了 Path Y，两人的进度共享后 convergence quest 的状态可能不一致。

**Consequence:** 团队成员之间的进度不同步，某些 quest 对部分成员解锁但对其他成员仍然锁定。

**Fix:**
- 在 Diamond pattern (MP9) 的 description 中注明团队模式下的选择策略
- 考虑在团队模式下将 `one_completed` 改为 `all`（要求所有路径都完成）

### AP-Team-3: The Offline Member Problem（离线成员问题）

**Symptom:** 团队成员离线时，在线成员完成 quest，离线成员的进度和奖励处理不确定。

**Root cause:** FTB Quests 的 auto-claim 机制在成员重新上线时补发离线期间的奖励。但 command reward（MP29）在离线状态下执行可能失败（AP15），material bridge（MP14）的物品可能在离线成员的 inventory 中堆积而未被使用。

**Consequence:** 离线成员上线后发现 inventory 中有一堆不明所以的物品（quest rewards），但不知道这些物品是干什么用的——因为他们在离线期间错过了所有 tutorial quest。

---

## 3. 团队模式对 Progression Rules 的影响

### R5 (Circular Dependency) 在团队模式下

循环依赖可能被"分工"打破：成员 A 做 chain 1，成员 B 做 chain 2，两人交换物品。这在单人模式下是一个 deadlock（AP2），但在团队模式下可能是可行的——只要两个成员能互相交易物品。

**规则调整：** 当 `team_mode` 启用时，R5 对跨 mod 的隐式循环降级为 INFO（提醒但不阻止），因为团队分工可能提供解决路径。

### R7 (Optional-Gate-Mandatory) 在团队模式下

如果团队中不同成员选择不同的 optional path，是否影响 mandatory quest 的解锁？这取决于 FTB Teams 的进度共享粒度：
- 如果共享粒度是 quest-level（完成/未完成），则一个成员完成 optional quest 就解锁了所有成员的 mandatory dependent。
- 如果共享粒度是 task-level，则可能需要每个成员的 task 都完成。

**规则调整：** R7 在团队模式下需要额外检查——mandatory quest 的所有 dependency 中，是否至少有一个是 non-optional 的（确保不依赖任何特定成员的选择）。

---

## 4. 建议的新增模式

### PP8 — The Free Rider Problem（团队搭便车问题）

**What players notice:** "My friend completed all the quests and I just got progress for free. I don't understand any of the mods in this pack."

**Pattern:** FTB Teams 的进度共享机制使团队成员可以"搭便车"——一个活跃成员完成所有 quest，其他成员被动获得进度。这对 quest book 的教学功能是一个威胁：搭便车者从未阅读过 tutorial description，从未亲手做过 teach-then-do 的实践环节，但他们的 quest book 显示"已完成"。

**Config implication:** 对于支持团队模式的包：
1. 关键 tutorial quest 使用 `consume_items: true`，确保每个成员都需要贡献材料
2. 在教学 quest 的 description 中加入"Team note: every member should read this" 的提示
3. 对于需要理解的 mechanic（不是简单的物品收集），考虑使用 personal task（每个成员独立完成的 task）而非 shared progress

**Source:** Review B (Completeness Audit) — "多人/团队场景完全空白"；FTB Quests 官方描述 "designed for teams"

---

## 5. SKILL.md 整合建议

当 SKILL.md Step 2 检测到目标包支持多人/团队时（通过用户声明或 FTB Teams 配置检测），应：

1. **在 Step 2 采访中增加团队模式问题：**
   - "你的整合包是否支持多人团队模式？"
   - "如果是，FTB Teams 的进度共享粒度是 quest-level 还是 task-level？"
   - "Reward 分配是每个成员都获得，还是只有提交者获得？"

2. **在 Step 4 per-node 循环中增加团队考量：**
   - 对于 material bridge (MP14) quest，标注 reward 分配模式
   - 对于 tutorial quest (MP3/MP11)，标注 "team note"
   - 对于 convergence quest (MP8)，标注团队分工建议

3. **在 Step 5 验证中增加 R29 (Team Progression Consistency) 检查：**
   - Material bridge 在团队模式下的 reward 分配
   - Fan-in convergence 的团队分工可行性
   - Optional path 分歧对 mandatory 进度的影响

---

## 6. 与 R29 的关系

R29（Team Progression Consistency，已写入 progression-rules.md）提供了团队模式下的自动化检查逻辑。本文档（team-multiplayer-patterns）提供了人类可读的设计考量和 anti-pattern 描述。两者的关系与 micro-patterns.md（设计公式）和 anti-patterns.md（错误后果）的关系一致：本文档解释 WHY 团队模式需要特殊处理，R29 定义 HOW 检测问题。

---

## 7. 待决问题

1. **FTB Teams 的进度共享粒度：** 需要确认 FTB Teams 在不同版本中的共享机制（quest-level vs task-level vs per-player）。不同版本的 FTB Teams 可能有不同的行为。

2. **Reward 分配机制：** FTB Teams 的 reward 分配设置（全员 vs 提交者）在不同版本中是否有变化？是否有 per-quest 的覆盖选项？

3. **PP8 的编号：** 当前 PP 系列有 PP1-PP7。新增 PP8 是否会与未来的 Cycle 3 模式冲突？建议预留 PP8-PP10 给团队相关模式。

4. **团队规模的考量：** 2 人团队和 10 人团队的 quest 设计需求可能完全不同。是否需要按团队规模分层建议？

5. **竞争性多人模式：** 本文档只覆盖了合作性团队模式。如果包设计了竞争性 quest（"第一个完成 X 的玩家获得奖励"），需要额外的模式覆盖。

---

## Sources

- Review B (Completeness Audit) — §"未覆盖的场景：多人/团队"，影响评级：高
- FTB Quests 官方描述 — "designed for teams, allowing you and your friends to complete quests together"
- FTB Teams documentation — 进度共享和 reward 分配机制
- R29 (Team Progression Consistency) — progression-rules.md §8
