## 审查员 B -- 完备性质疑

审查日期: 2026-07-06
审查范围: micro-patterns.md (32 MP + 7 PP), anti-patterns.md (13 AP), progression-rules.md (26 R)
审查方法: 从 FTB Quests 源码 (FTBTeam/FTB-Quests GitHub main branch) 提取完整的 task type 和 reward type 注册列表，逐类型交叉比对三份设计文档的覆盖情况

---

### 已覆盖的 task/reward/dependency 类型

#### Task Types (源码 15 种, 已覆盖 10 种)

| Task Type | 源码类名 | 覆盖 MP/AP/R | 覆盖质量 |
|---|---|---|---|
| item | `ItemTask` | MP1, MP2, MP4, R1-R4, R10, R14-R17, R23, R25 | 优秀 -- 全面覆盖，是设计文档的核心 |
| checkmark | `CheckmarkTask` | MP3, MP11, R14 | 良好 -- 作为 acknowledgement 模式充分覆盖 |
| kill | `KillTask` | MP4 (Escalation Ladder) | 良好 -- 有专门的递增模式 |
| dimension | `DimensionTask` | MP5, MP13, MP16, MP21, R16 | 优秀 -- 多种复合模式和教学顺序规则 |
| structure | `StructureTask` | MP31 (Structure Discovery Gate) | 良好 -- Cycle 2 新增，有专门模式和设计建议 |
| fluid | `FluidTask` | MP27 (Fluid Task Gate) | 基本 -- 有专门模式但仅覆盖基础场景 (详见下文) |
| energy | `EnergyTask` | MP28 (Energy Threshold Gate) | 基本 -- 有专门模式但仅覆盖基础场景 (详见下文) |
| gamestage | `StageTask` | MP30 (Gamestage Bridge), MP23 | 良好 -- 有完整的游戏阶段桥接模式 |
| observation | `ObservationTask` | MP3 (Acknowledgement Gate), R14 | 基本 -- 作为 MP3 的子类型提及 |
| stat | `StatTask` | MP3, MP4, R14 | 良好 -- 用于 acknowledgement 和递增模式 |

#### Reward Types (源码 14 种, 已覆盖 4 种)

| Reward Type | 源码类名 | 覆盖 MP/AP/R | 覆盖质量 |
|---|---|---|---|
| item | `ItemReward` | MP14, MP15, R10, R11, R12, R13 | 优秀 -- 全面覆盖 |
| choice | `ChoiceReward` | MP18 (Choice Reward) | 良好 -- 有专门模式 |
| xp | `XPReward` | MP16 (XP Drip), R12 | 良好 -- 作为通用 baseline 覆盖 |
| xp_levels | `XPLevelsReward` | MP2, MP8 中作为复合 reward 出现 | 基本 -- 在示例中出现但无专门模式 |

#### Dependency Mechanisms (已覆盖 4/6)

| Mechanism | 覆盖情况 |
|---|---|
| `dependency_requirement: "all"` | R7, R8, MP9 -- 优秀 |
| `dependency_requirement: "one_completed"` | MP9 (Diamond), R8 -- 良好 |
| `dependency_requirement: "one_started"` | MP9, R8 -- 良好 |
| `optional: true` | R6, R7, AP4 -- 良好 |
| `hide_until_deps_visible` | AP7, R21, PP3 -- 良好 |
| `hide_dependency_lines` | MP7, MP8 中提及 -- 基本 |

---

### 未覆盖的 task/reward/dependency 类型

#### 未覆盖的 Task Types (5 种)

**1. AdvancementTask (`advancement`) -- 影响: 高**

源码中 `AdvancementTask.java` 存在，当玩家获得原版或 mod advancement 时自动完成。这是 FTB Quests 与原版 advancement 系统交互的唯一桥梁。

缺失原因分析: 15 个审计包中可能极少使用此 task type (kitchen-sink 和 expert 包倾向于用自己的 gating 系统而非依赖原版 advancement tree)，导致 Cycle 1/2 数据中未出现足够样本。

影响:
- Advancement task 允许 quest 进度与原版 advancement 树联动。当整合包使用 Datapack 自定义 advancement 时 (如 Prominence II 等 RPG 包)，这是关键的进度工具。
- Advancement task 的 "auto-complete on earn" 行为与 item/kill task 不同 -- 玩家无法主动提交，只能在游戏中自然触发。这意味着 quest 作者不能假设玩家会在特定时刻完成 advancement task。
- Advancement 和 GameStage 的配合 (先获得 advancement, 再由 advancement 触发 gamestage 变更) 是一个独特的设计空间。

建议:
- 新增 MP33 -- Advancement Gate (advancement 驱动的进度触发)。覆盖: advancement task 的 auto-complete 行为, 与 datapack advancement 的联动, 与 gamestage 的桥接模式。
- 新增 R27 -- Advancement Existence Check。验证: advancement task 引用的 advancement ID 在包的 datapack 中是否存在 (类似 R22 对跨 chapter 引用的检查)。
- 考虑在 AP 中新增: "Advancement 不可达" 反模式 -- advancement 的触发条件在包配置中无法满足 (例如 advancement 要求的结构不生成)。

**2. LocationTask (`location`) -- 影响: 中**

源码中 `LocationTask.java` 存在，当玩家到达特定 XYZ 坐标时自动完成。mcmod.cn 教程明确提到 "玩家到达后自动完成"。

缺失原因分析: 审计包中 location task 使用率极低 -- dimension task (MP5/MP21) 和 structure task (MP31) 覆盖了大部分 "到达某个地方" 的需求。Location task 的精确坐标要求在大多数包类型中不如 "到达维度" 或 "找到结构" 实用。

影响:
- 在 RPG/Adventure 包中, location task 有独特价值: "到达特定地标" (例如一座山顶, 一个隐藏的洞穴入口) 比 "进入维度" 更精确。
- 在 skyblock 包中, location task 可以检测玩家是否到达了某个特定平台 (例如资源岛)。
- Location task 的坐标验证需要考虑世界类型 -- void world 中 Y 坐标的含义与正常世界不同。

建议:
- 新增 MP34 -- Location Discovery Gate (精确坐标触发)。覆盖: 坐标格式 (dimension + x/y/z/radius), void world 特殊性, 与 structure task 的选型指南。
- 优先级: 中。仅在 story/RPG 包中有显著使用场景。

**3. CustomTask (`custom`) -- 影响: 中**

源码中 `CustomTask.java` + `CustomTaskClient.java` 存在，允许 KubeJS 或其他 mod 注册自定义任务逻辑。

影响:
- Custom task 的完成条件完全由外部代码定义, FTB Quests 本身不验证其合理性。这意味着 AI 生成 custom task 时没有内在约束 -- 任何逻辑都可以是 custom task。
- 在 expert 包 (Monifactory 风格) 中, custom task 常用于检测多方块结构搭建、机器运行状态等 mod 特有机制。
- Custom task 的 "可完成性" 完全取决于外部实现, 使得 R6 (Unreachable Quest) 和 R20 (Chapter Completion Testability) 无法自动验证。

建议:
- 新增 AP14 -- Custom Task Black Box (custom task 的不可验证性风险)。覆盖: custom task 的完成条件对 quest 系统不透明, 需要 pack author 额外验证, 生成时不应主动创建 custom task (因为 AI 无法验证其完成条件)。
- 新增一条规则或 R20 的特殊处理: 当 quest 包含 custom task 时, R6/R20 对该 quest 降级为 INFO (无法静态验证)。

**4. BiomeTask (`biome`) -- 影响: 低**

源码中 `BiomeTask.java` 存在，当玩家进入特定生物群系时自动完成。MP13 (Explore-Then-Craft) 提到了 biome 但没有将其作为独立 pattern。

影响:
- Biome task 是 dimension task (MP5/MP21) 的更精细版本 -- 不仅要求进入维度, 还要求进入特定生物群系。
- 在 skyblock 和 void world 包中, biome task 可能不可用 (取决于世界生成是否包含该 biome)。
- Biome ID 在 mod 更新时可能变更 (尤其是 biome 重命名/合并)。

建议:
- 在 MP13 或 MP21 中增加 biome task 作为 "dimension task 的精细化变体" 的说明段落即可, 不需要独立 MP。
- 新增 biome ID 验证到 R1 的扩展中 (biome 可达性检查 -- 类似维度可达性)。

**5. XPTask (`xp`) -- 影响: 低**

源码中 `XPTask.java` 存在，要求玩家拥有特定数量的 XP。这是一个 "提交型" task -- 玩家消耗 XP 来完成任务 (与 XP reward 相反)。

影响:
- XP task 在大多数包中极少使用, 因为 XP 在 Minecraft 中是一种流动性资源, 不适合作为进度门控。
- 在 expert 包中, XP task 可以用于 "消耗 N 级附魔经验" 的 gate -- 但这通常通过 enchanting table 间接实现。

建议:
- 在 MP16 (XP Drip) 中增加一段关于 XP task (消耗型) 与 XP reward (给予型) 的区别说明。优先级低。

---

#### 未覆盖的 Reward Types (10 种)

**6. CommandReward (`command`) -- 安全性覆盖不完整 -- 影响: 高**

MP29 覆盖了 command reward 的基本使用模式和安全规则 (4 条 safety rules), 但安全性覆盖不够深入:

MP29 已覆盖:
- 不要用 /op, /gamemode creative
- 用 {p} 代替硬编码玩家名
- 优先用标准 reward type
- gamestage 名称拼写验证

MP29 未覆盖:
- **执行时机问题**: command reward 在 quest claim 时执行 -- 如果玩家离线 claim (FTB Quests 支持 auto-claim 离线奖励), command 在玩家不在线时执行会怎样? `/effect give` 会失败吗? `/tp` 会把玩家传送到哪里?
- **多次执行问题**: 如果 quest 被 unclaim 再 reclaim (admin 操作或 bug), command 会重复执行。`/give` 会重复给物品, `/gamestage add` 通常是幂等的但不一定。
- **服务器性能问题**: 大量 command reward 同时执行 (例如 claim-all 按钮) 可能导致 TPS 下降。
- **Command 注入风险**: AI 生成 command 时可能意外包含恶意或危险的 command 片段。MP29 的 safety rules 只覆盖了 "不要给 op", 没有覆盖 "确保 command 字符串不会造成意外副作用" (例如 `/fill` 命令可能覆盖玩家建筑)。
- **跨维度 command 执行**: 如果 command 涉及坐标 (`/tp`, `/setblock`), 需要明确目标维度。

建议:
- 扩展 MP29 的安全规则, 增加: (a) 执行时机说明 (在线/离线), (b) 幂等性要求, (c) claim-all 批量执行的注意事项, (d) 禁止破坏性 command (/fill, /setblock 在玩家坐标附近)。
- 新增 AP15 -- Command Reward Side Effect (command reward 的副作用累积)。覆盖: 重复执行, 离线执行, claim-all 风暴。
- 新增 R28 -- Command Reward Safety Scan: 静态分析 command 字符串, 标记高风险 command (/fill, /setblock, /kill, /clear, /effect 高 amplifier) 为 WARNING, 标记 /op, /gamemode creative, /stop 为 ERROR。

**7. StageReward (`stage`) -- 影响: 高**

源码中 `StageReward.java` 存在, 专门用于授予/撤销 gamestage。MP30 覆盖了 gamestage 的 bridge 模式 (通过 command reward 的 `/gamestage add`), 但 stage reward 作为专门的 reward type 没有被单独提及。

影响:
- StageReward 比 command reward 的 `/gamestage add` 更安全 -- 不需要拼写 command 字符串, 不需要权限管理。
- StageReward 支持 `add` 和 `remove` 操作 -- `remove` 操作可以用于 "重置" 或 "降级" 场景, 这是一个未被探索的设计空间。
- StageReward 在 FTB Quests UI 中有专门的显示方式, 玩家可以直观看到获得了哪个 stage。

建议:
- 在 MP30 (Gamestage Bridge) 中明确推荐使用 `StageReward` 而非 `CommandReward + /gamestage add` 作为 stage 授予的首选方式。
- 记录 `stage remove` 的设计场景: 例如 "完成 expert 模式后移除 easy-mode stage, 解锁 expert 配方"。

**8. LootReward (`loot`) -- 影响: 中**

源码中 `LootReward.java` 存在, 使用原版战利品表 (loot table) 生成奖励。MP4 的示例中出现了 `random` reward (类似概念), 但 loot reward 没有专门模式。

影响:
- Loot reward 引用原版 loot table ID (例如 `minecraft:chests/end_city_treasure`), 如果 loot table 在包中被修改或不存在, reward 会给出意外物品或空奖励。
- Loot reward 的产出不可预测 -- 这在 "奖励即下一步材料" 的设计中是致命的 (MP14 Material Bridge 要求 reward 确定性)。
- Loot reward 适合 "惊喜奖励" 场景 (探索章节的宝箱, 击杀 boss 的额外掉落), 但需要确保产出不会打破经济平衡。

建议:
- 新增 MP35 -- Loot Table Reward (随机奖励的安全使用模式)。覆盖: loot table ID 验证, 与 R12 (Reward Value Progression) 的关系 (随机 reward 的价值波动范围), 适用场景 (探索/boss 奖励, 非进度关键材料)。
- 新增 R29 -- Loot Table Existence Check: 验证 loot reward 引用的 table ID 在包中是否存在。

**9. RandomReward (`random`) -- 影响: 中**

源码中 `RandomReward.java` 存在, 使用 FTB Quests 内置的权重随机系统。与 LootReward 不同, RandomReward 的权重和物品由 quest author 直接定义 (类似 weighted loot bag)。

影响:
- RandomReward 在 ATM-10 Bounty Board 中已有使用 (MP4 示例: `type: "random"`), 但没有作为独立 reward pattern 分析。
- Random reward 的概率分布需要与 quest 难度匹配 -- 高难度 quest 的随机 reward 应该有更高的期望值。
- Random reward 的 "claim-all" 行为: 如果 50 个 quest 都有 random reward, claim-all 会一次性 roll 50 次, 可能导致大量低价值物品涌入 inventory。

建议:
- 在 MP4 (Escalation Ladder) 中增加对 random reward 权重配置的说明 -- reward 期望值应随 ladder 递增。
- 优先级: 低。现有 MP4 示例已足够参考。

**10. AllTableReward (`all_table`) -- 影响: 低**

源码中 `AllTableReward.java` 存在, 给予 loot table 中的所有物品 (非随机, 全给)。这是一个较少使用的 reward type。

建议: 不需要独立 MP, 在 MP35 (如果创建) 中作为 LootReward 的变体提及即可。

**11. ToastReward (`toast`) -- 影响: 低**

源码中 `ToastReward.java` 存在, 显示一个 toast 通知 (非物品, 非 XP, 纯视觉反馈)。

影响:
- Toast reward 是一个 "零成本奖励" -- 不消耗任何资源, 仅给玩家一个视觉提示。适合 "恭喜完成" 的叙事型包。
- 在大多数包中 toast reward 的价值有限 -- 玩家更希望获得实质奖励。

建议: 不需要独立 MP。在 MP17 (Hub Concentration) 中提及: "对于无需实质奖励的完成提示, 考虑 toast reward 作为零成本替代"。

**12. AdvancementReward (`advancement`) -- 影响: 中**

源码中 `AdvancementReward.java` 存在, 完成 quest 时自动授予一个原版 advancement。这是 advancement task 的逆向 -- task 检测 advancement, reward 授予 advancement。

影响:
- AdvancementReward 可以 "跳过" 原版 advancement 树的某些步骤 -- 例如, quest 完成后直接授予 "The End?" advancement, 跳过实际的 dragon kill 要求。
- 与 advancement task 配合, 可以创建 "quest 链驱动 advancement 链" 的模式: Quest A 授予 advancement X, Quest B 的 task 检测 advancement X, Quest B 授予 advancement Y...
- 在 datapack 驱动的 RPG 包中, 这可以创建 "quest book 和 advancement tree 双轨进度" 的高级设计。

建议:
- 与 AdvancementTask 一起作为 MP33 (Advancement Gate) 的一部分覆盖。
- 新增 R30 -- Advancement Chain Consistency: 检查 advancement reward 授予的 advancement 是否被下游 advancement task 正确引用, 避免断链。

**13. CurrencyReward (`currency`) -- 影响: 低-中**

源码中 `CurrencyReward.java` 存在, 给予 FTB Quests 内置虚拟货币 (与 FTB Quests 的 Shop 功能配合)。

影响:
- Currency reward 需要 Shop 配置才能有意义 -- 如果包没有配置 Shop, currency reward 是无用的。
- 在有 Shop 的包中, currency reward 可以替代 item reward -- "给你 N 金币, 去 Shop 买你需要的东西", 这解决了 MP14 (Material Bridge) 的某些痛点 (reward 物品不是下一步需要的)。

建议:
- 新增简短说明: 当包配置了 FTB Quests Shop 时, currency reward 可以作为 material bridge 的替代 (MP14 变体)。优先级低。

**14. CustomReward (`custom`) -- 影响: 低**

源码中 `CustomReward.java` 存在, 允许 KubeJS 定义自定义 reward 逻辑。与 custom task 类似, 不可静态验证。

建议: 与 custom task 一起处理 -- 在 AP14 中覆盖, 并在 R20 中增加 custom reward 的特殊处理。

---

#### 未覆盖的 Dependency Mechanisms (2 种)

**15. Team-based dependency (`team_completed` 等) -- 影响: 高 (详见场景分析)**

FTB Quests 官方描述为 "designed for teams, allowing you and your friends to complete quests together"。FTB Teams 提供团队系统, quest 完成可以按团队共享。但三份设计文档完全没有涉及多人/团队场景。

详见下方 "未覆盖的场景 -- 多人/团队"。

**16. `dependency_requirement` 的完整值域 -- 影响: 低**

文档覆盖了 `all`, `one_completed`, `one_started`。FTB Quests 源码中可能还有其他值 (需要确认)。R8 的检查逻辑也只考虑了这三种。

建议: 在 R8 中增加对未知 `dependency_requirement` 值的 ERROR 级别检查 (防止拼写错误或已弃用值)。

---

### 未覆盖的场景

#### 1. 多人/团队场景 -- 影响: 高

FTB Quests 的核心卖点之一是团队任务, 但三份文档的设计语境默认是单人玩家。以下团队相关问题完全没有覆盖:

**a) 团队进度共享模式**
- FTB Teams 允许团队成员共享 quest 进度。当一个成员完成 item task 时, 所有团队成员的任务进度都更新。
- 设计影响: MP1 (Single-Item Gate) 在团队模式下意味着 "任何成员提交物品即完成" -- 这改变了 quest 的经济性 (团队可以分工收集材料)。
- MP8 (Fan-In / Convergence) 在团队模式下的含义: 10 个 component sub-tree 可以由 10 个团队成员分别完成。Capstone quest 是 "团队合成" 而非 "个人合成"。

**b) 团队奖励分配**
- Quest reward 是每个团队成员都获得, 还是只有提交者获得? 这取决于 quest 配置和 FTB Teams 设置。
- MP14 (Material Bridge) 在团队模式下可能失效: 如果只有提交者获得 reward item, 其他团队成员没有下一步的材料。
- R10 (Reward-to-Dependent Bridge) 的检查逻辑没有考虑 "reward 是否对所有团队成员可见"。

**c) 团队模式下的 anti-patterns**
- "搭便车" 问题: 一个玩家完成所有 quest, 其他玩家只是被动获得进度。Quest book 对搭便车者没有教学价值。
- 竞争模式: 如果 quest 是 "第一个 kill 100 zombies 的玩家获得奖励", 团队模式可能产生内部竞争。
- 离线成员: 团队成员离线时, 在线成员完成 quest, 离线成员的进度和奖励如何处理?

**d) 团队模式对 progression-rules 的影响**
- R5 (Circular Dependency): 在团队模式下, 循环依赖可能被 "分工" 打破 (成员 A 做 chain 1, 成员 B 做 chain 2, 两人交换物品)。
- R7 (Optional-Gate-Mandatory): 团队中不同成员选择不同的 optional path, 是否影响 mandatory quest 的解锁?

建议:
- 新增 Player-Perspective Pattern PP8 -- "The Free Rider Problem" (团队搭便车问题)。覆盖: 团队模式下 quest 的教学有效性, 如何设计 "每个成员都需要参与" 的 quest (例如使用 custom task 检测个人贡献)。
- 在 SKILL.md 的生成逻辑中, 当检测到目标包支持多人/团队时, 增加团队模式相关的设计考量提示。
- 新增 R31 -- Team Reward Distribution Check: 验证 team-relevant quest 的 reward 分配模式是否与团队进度共享模式匹配。

#### 2. Modpack 更新兼容性 -- 影响: 高

三份文档的上下文都是 "从头生成 quest 配置" (SKILL.md Step 2-5), 没有考虑 "更新已有 quest 配置" 的场景。然而在实际 modpack 维护中, quest 配置的更新兼容性是一个核心问题:

**a) Quest 新增**
- Modpack 更新后添加新 chapter/quest: 已有玩家的 quest book 状态如何更新? FTB Quests 使用 quest ID 跟踪进度, 新 ID = 新 quest (无问题)。
- 但新 quest 的依赖链如果引用了已有 quest, 已完成依赖 quest 的玩家是否自动解锁新 quest? (通常: 是的, 因为依赖已满足。)

**b) Quest 修改**
- 修改已有 quest 的 task (例如换物品): 已完成该 quest 的玩家是否被 "un-complete"? (FTB Quests 通常不会 retroactively un-complete, 但 task 状态可能不一致。)
- 修改 reward: 已 claim 的玩家不会再次获得新 reward。未 claim 的玩家获得新 reward。
- 修改 dependency: 可能导致已完成的 quest chain 不再逻辑自洽。

**c) Quest 删除**
- 删除已有 quest: 已完成的进度记录消失。其他 quest 的 dependencies 引用了被删 quest 的 ID 会导致什么? (FTB Quests 可能忽略不存在的 dep, 也可能报错。)
- R22 (Cross-Chapter Dependency Validity) 只检查跨 chapter 引用是否存在, 没有考虑 "引用曾经存在但被删除" 的情况。

**d) Mod 增减导致的级联变化**
- 移除一个 mod: 该 mod 的所有物品/方块/实体不存在了, 引用它们的 quest task/reward 全部失效。
- 更新一个 mod: 物品 ID 可能变更 (例如 `mod:item_v1` 变成 `mod:item_v2`), 配方可能变化 (AP1 的时间维度变体 -- R26 已部分覆盖)。

建议:
- 新增 AP16 -- Quest State Migration Problem (quest 状态迁移问题)。覆盖: 新增/修改/删除 quest 对已有玩家进度的影响, quest ID 稳定性要求, dependency 引用失效的处理。
- 新增 R32 -- Stale Dependency Reference Check: 检查 dependencies 中引用的 quest ID 是否存在于当前配置中 (R22 的扩展 -- R22 只检查跨 chapter, R32 检查所有引用)。注意: R22 实际上已经部分覆盖了这一点 ("which does not exist in any chapter"), 但 R32 应该明确覆盖 "update scenario" -- 当 SKILL.md 以 `--adopt` 模式读取现有配置时, 检测新配置与旧配置之间的 ID 差异。
- 在 SKILL.md 的 `--adopt` 模式说明中增加: "当更新已有 quest 配置时, 保持 quest ID 不变 (除非必须修改), 以维持玩家进度兼容性。"

#### 3. 流体任务的复杂模式 -- 影响: 中

MP27 覆盖了基础的 fluid task (收集特定体积的流体), 但没有覆盖以下复杂场景:

**a) 跨 mod 流体传输**
- Create 的 fluid 系统和 Mekanism 的 fluid 系统使用不同的管道/储罐, 流体 ID 可能相同但传输机制不同。
- Quest 要求 "收集 1000mB lava" 但没有说明用哪个 mod 的容器 -- 玩家用 Create 的 fluid tank 还是 Mekanism 的 dynamic tank?

**b) 流体温度/状态**
- 某些 mod 的流体有温度属性 (例如 Mekanism 的 heated/ superheated 蒸汽), 同一 fluid ID 在不同温度下是不同物品。
- FTB Quests 的 fluid task 是否检查温度/NBT? (AP12 -- NBT Insensitivity 的流体变体。)

**c) 流体自动化场景**
- Expert 包中, 流体任务通常是 "自动化这个流体生产链" 而非 "手动收集一桶流体"。MP27 没有覆盖 "流体生产链教学" 的设计模式 (teach-then-do 的流体版本)。

建议:
- 扩展 MP27: 增加 (a) 跨 mod 流体容器的兼容性说明, (b) 流体 NBT/温度问题 (引用 AP12), (c) 流体自动化教学模式。

#### 4. 能源任务的复杂模式 -- 影响: 中

MP28 覆盖了基础的 energy task (存储特定 FE), 但没有覆盖:

**a) 多能源系统**
- GregTech 使用 EU (Energy Units), Mekanism 使用 Joules (1J = 2.5 FE), IC2 使用 EU (不同于 GregTech 的 EU)。在包含多个能源系统的包中, energy task 检测的是哪个系统?
- Energy task 的 `value` 字段使用的单位是什么? (FTB Quests 通常使用 FE, 但 EU-based 包的换算可能不同。)

**b) 能源生产速率 vs 存储量**
- MP28 提到 "calibrate the energy threshold against the best available generator" -- 但没有覆盖 "发电速率" 作为独立门控维度。一个 quest 可能要求 "持续发电 1000 FE/t" 而非 "存储 100000 FE" -- 这是两种不同的基础设施测试。
- FTB Quests 的 energy task 检测的是存储量 (block 中的 FE 总量) 还是产率 (FE/t)? 通常只是存储量, 但 quest 描述可能误导玩家以为需要特定产率。

**c) 能源任务与能源消耗 quest 的关系**
- 与 XPTask 类似, 可以设计 "消耗 N FE" 的 quest (通过机器运行消耗), 而非 "存储 N FE"。FTB Quests 的 energy task 是否支持消耗型? (通常只检测存储量, 不支持消耗型。)

建议:
- 扩展 MP28: 增加 (a) 多能源系统的单位换算说明, (b) 存储量 vs 产率的区分, (c) 推荐在描述中明确 "你需要存储 X FE" 还是 "你需要能产生 X FE/t"。

#### 5. Chapter-Level 设置覆盖不完整 -- 影响: 低-中

三份文档覆盖了部分 chapter-level 设置:
- `progression_mode` (default/linear/flexible) -- R4 中提及
- `default_quest_shape` -- MP20 中提及
- `order_index` -- R4, R22 中提及
- `icon`, `title` -- MP19 中提及
- `group` -- R4 中提及 (chapter groups)

未覆盖的 chapter-level 设置:
- **Chapter-level `always_invisible`**: MP23 提到了 invisible chapter, 但没有讨论 "在什么条件下应该使用 invisible chapter vs invisible quest"。
- **Chapter-level `consume_items` 默认值**: 如果一个 chapter 的大部分 quest 需要 consume items (提交物品后消耗), 是否应该在 chapter 级别设置默认值而非逐 quest 配置?
- **Chapter description / subtitle**: Chapter 本身可以有描述文字, 用于介绍整个章节的主题和预期。三份文档没有覆盖 chapter-level description 的最佳实践。
- **Quest shape default vs override 策略**: MP20 讨论了 shape 的语义, 但没有给出 "什么时候应该设置 chapter default_quest_shape vs 逐 quest override" 的明确规则。

建议:
- 在 SKILL.md 的 Step 2 (outline) 中增加 chapter-level 配置的 checklist: icon, title, description, default_quest_shape, progression_mode, always_invisible, group。

---

### 建议新增的模式或规则

按优先级排序:

#### 高优先级 (影响核心功能或频繁出错)

| 编号 | 类型 | 名称 | 解决什么问题 |
|---|---|---|---|
| MP33 | Micro-Pattern | Advancement Gate | advancement task/reward 的双向联动模式, 与 datapack 和 gamestage 的交互 |
| AP14 | Anti-Pattern | Custom Task/Reward Black Box | custom task/reward 的不可验证性, AI 不应主动创建 |
| AP15 | Anti-Pattern | Command Reward Side Effect | command reward 的重复执行/离线执行/claim-all 风暴 |
| AP16 | Anti-Pattern | Quest State Migration | 更新/修改/删除 quest 对已有玩家进度的影响 |
| R27 | Rule | Advancement Existence Check | 验证 advancement task/reward 引用的 ID 在 datapack 中存在 |
| R28 | Rule | Command Reward Safety Scan | 静态分析 command 字符串的高风险模式 |
| R31 | Rule | Team Reward Distribution | 验证团队模式下的 reward 分配与进度共享一致性 |

#### 中优先级 (有明确使用场景但频率较低)

| 编号 | 类型 | 名称 | 解决什么问题 |
|---|---|---|---|
| MP34 | Micro-Pattern | Location Discovery Gate | 精确坐标触发的进度门控 (RPG/skyblock) |
| MP35 | Micro-Pattern | Loot Table Reward Pattern | 随机奖励的安全使用模式和 loot table ID 验证 |
| PP8 | Player-Perspective | The Free Rider Problem | 团队模式下 quest 的教学有效性 |
| R29 | Rule | Loot Table Existence Check | 验证 loot reward 引用的 table ID 存在 |
| R30 | Rule | Advancement Chain Consistency | advancement reward 和 advancement task 的链式一致性 |
| R32 | Rule | Stale Dependency Reference | 更新场景下的悬空依赖引用检测 |
| MP27-ext | 扩展 | Fluid Task Complex Patterns | 跨 mod 流体, NBT/温度, 自动化教学 |
| MP28-ext | 扩展 | Energy Task Complex Patterns | 多能源系统, 存储量 vs 产率 |
| MP29-ext | 扩展 | Command Reward Safety Extended | 执行时机, 幂等性, 破坏性命令禁止 |
| MP30-ext | 扩展 | StageReward vs CommandReward | 推荐 StageReward 作为首选, stage remove 场景 |

#### 低优先级 (特定场景或边缘情况)

| 编号 | 类型 | 名称 | 解决什么问题 |
|---|---|---|---|
| BiomeTask note | 补充 | Biome Task 变体说明 | 在 MP13/MP21 中增加 biome task 作为 dimension 的精细化变体 |
| XPTask note | 补充 | XP Task (消耗型) vs XP Reward | 在 MP16 中区分 |
| Toast note | 补充 | Toast Reward 零成本替代 | 在 MP17 中提及 |
| Currency note | 补充 | Currency Reward + Shop 模式 | 在有 Shop 配置时作为 material bridge 替代 |
| Chapter config | 补充 | Chapter-Level Config Checklist | 在 SKILL.md Step 2 中增加 |

---

### 覆盖度总结

| 维度 | 总数 (源码) | 已覆盖 | 部分覆盖 | 未覆盖 | 覆盖率 |
|---|---|---|---|---|---|
| Task Types | 15 | 10 | 2 (biome, xp) | 3 (advancement, custom, location) | 73% (完全) / 87% (含部分) |
| Reward Types | 14 | 4 | 4 (xp_levels, random, loot, stage) | 6 (command*, advancement, currency, custom, all_table, toast) | 29% (完全) / 57% (含部分) |
| Dependency Mechanisms | 6 | 5 | 0 | 1 (team) | 83% |
| Chapter-Level Settings | 7 | 5 | 1 (always_invisible) | 1 (chapter description) | 71% |
| Multiplayer/Team | 4 | 0 | 0 | 4 | 0% |
| Update Compatibility | 4 | 1 (R26 部分) | 1 (R22 部分) | 2 | 25% |

*注: command reward 有 MP29 覆盖但安全性不足, 标记为 "command*"

**最关键的三个缺口:**
1. **Reward Types 覆盖严重不足** -- 14 种 reward type 中只有 4 种有专门 pattern。Command, stage, loot, advancement 四种重要 reward type 缺乏充分的模式覆盖。
2. **多人/团队场景完全空白** -- FTB Quests 的核心卖点 (团队任务) 在三份文档中零覆盖。
3. **Modpack 更新兼容性几乎空白** -- 对于 `--adopt` 模式的实际使用场景, 缺乏 quest 状态迁移的指导。

**最关键的三个已有模式扩展需求:**
1. MP27 (Fluid Task) 需要扩展覆盖跨 mod 流体和 NBT 问题。
2. MP28 (Energy Task) 需要扩展覆盖多能源系统。
3. MP29 (Command Reward) 需要扩展安全规则覆盖执行时机和幂等性。
