# 审查员 B — 完备性审查报告 (Cycle 7)

## 规则边界遗漏

### R1 — Dimension-Reachability
- **跨维度物品流通未覆盖。** R1 假设物品的唯一来源是其原生维度，但忽略了：(1) 村民交易/Wandering Trader 可在 Overworld 获取 Nether/End 物品；(2) 跨 mod 替代配方（某 mod 在 Overworld 合成另一 mod 的 Nether 物品）；(3) mob 掉落物跨维度携带（Enderman 持有 Nether 方块）；(4) Create 跨维度物流。L1 映射表仅覆盖 ~20 个 vanilla/mod 物品，对 200+ mod 包覆盖率极低。
- **自定义维度缺失。** `BUILTIN_DIMENSION_MAP` 不含常见 mod 维度如 `ae2:spatial_storage`、`mekanism:dimension` 等。对于不使用 ATM 系列维度的包，L1 几乎无意义。
- **维度解锁判定不完整。** R1 定义「维度解锁」仅通过 `dimension` task 或 gamestage 判定，但许多包通过 `advancement` task 隐含解锁维度（如 `minecraft:nether/root` 成就 = 进入 Nether），R1 未考虑 advancement task 作为维度解锁信号。

### R2 — Tool-Tier Item Reachability
- **非采矿工具需求未覆盖。** R2 的 `BUILTIN_TOOL_TIER_MAP` 和 `BUILTIN_ORE_REQUIREMENTS` 仅关注 pickaxe mining level。完全忽略：(1) 钓鱼竿（fishing rod）需求；(2) 剪刀（shears）需求；(3) 桶（bucket）用于流体收集；(4) 专用 mod 工具如 Create 的 wrench、Mekanism 的 configurator。
- **机器加工需求不等于工具等级。** R2 将机器 tier 映射为 1-4 级，但实际加工链可能需要特定机器类型而非等级——一个 depth-1 的 enrichment chamber 无法执行 depth-2 的 chemical infusion，这不是等级问题而是机器类型问题。

### R3 — Recipe-Chain Depth
- **非合成加工链未覆盖。** `estimate_recipe_depth_heuristic` 仅基于物品名称关键词估算合成深度。完全忽略：(1) 被动加工（发酵、干燥、堆肥）；(2) mob 养殖链（breeding → drop → craft）；(3) 自动化加工（Create contraption 多步处理）；(4) 时间密集型加工（smelting 大量物品的燃料需求）。
- **Expert 包精度严重不足。** Heuristic 最大覆盖约 depth 8，误差 ±2，而 expert 包（Monifactory、GT-O）的合成链深度常达 15+。这意味着 R3 对 expert 包的核心价值场景几乎无法提供有意义的检查。

### R4 — Stage Boundary
- **多用途物品的阶段归属未定义。** 一个物品可能在 early-game 用于装饰（低阶段用途），在 late-game 用于合成（高阶段用途）。R4 的 `item_stage_map` 假设每个物品有唯一阶段，但现实中许多物品跨阶段使用。
- **跨 mod 替代路径导致阶段绕过。** 某物品在 mod A 是 late-game，但通过 mod B 的配方在 early-game 可获得。R4 基于单 mod 的阶段定义无法检测这种跨 mod 阶段绕过。

### R5 — Circular Dependency
- **隐式循环（recipe graph）无检测能力。** R5 明确标注隐式循环需要「外部脚本 + JEI/EMI recipe graph export」，但 SKILL.md 的工作流中没有集成此工具的步骤。隐式循环（AP2 的核心场景——red chalk → torch flower → heart of the sea → red chalk）恰恰是玩家最常遇到的 deadlock 类型。
- **单 mod 内部循环未覆盖。** FTB Skies 2 #9084 的 Productive Bees deadlock 完全在单 mod 内部，不涉及跨 mod 依赖，R5 的 cross-mod 审计无法捕获。

### R7 — Optional-Gate-Mandatory
- **Diamond pattern 中的 optional 路径未覆盖。** MP9 (Diamond) 中 `dependency_requirement: "one_completed"` 允许选择两条路径之一。如果其中一条路径包含 optional quest，另一条不包含，R7 的当前逻辑无法判定这是否合理——因为 requirement 是 "one"，optional dep 可以被绕过。

### R9 — Dependency Depth Reasonableness
- **MAX_DEPTH 阈值缺乏实证支撑。** kitchen-sink: 8, expert: 20, skyblock: 20, rpg: 12, create: 10 — 这些数值是经验值还是从数据中推导？ATM9-Sky 的 getting_started_2 深度为 18，远超 skyblock: 20 但接近边界。阈值应有明确的来源标注和置信区间。

### R10 — Reward-to-Dependent Bridge
- **Currency 例外检测脆弱。** R10 的 currency exception 依赖识别 `lightmanscurrency`、`gtocore` 等 mod namespace。但许多包使用自定义 currency mod 或 vanilla 物品（如 emerald）作为货币，R10 无法识别这些情况。
- **工具奖励桥接未覆盖。** R10 检查 item reward 是否出现在 dependent 的 task 中，但 tool reward（MP15）不会被 dependent 的 item task 引用——tool 是被使用而非被提交。R10 的 tool exception 仅简单跳过，没有验证 tool 是否在 dependent quest 的上下文中被需要。

### R23 — Description-Item Consistency
- **Display name vs item ID 鸿沟。** R23 通过正则匹配 `modid:item_name` 格式，但 quest description 通常使用 display name（"Osmium Ingot"）而非 item ID（`mekanism:ingot_osmium`）。description 用中文名时更无法匹配。R23 只能捕获直接写了 item ID 的场景，这是极少数情况。

### R28 — Command Reward Safety Scan
- **嵌套命令未覆盖。** `/execute ... run ...` 可以将危险命令隐藏在嵌套结构中。R28 的正则匹配可能漏掉 execute 链中的 `/fill`、`/setblock` 等。
- **`{p}` placeholder 之外的变量注入未检查。** 命令可能包含 `{x}`、`{y}`、`{z}`、`{team}`、`{quest}` 等 FTB Quests 变量，R28 仅检查 `{p}` 的使用。

---

## 规则间灰色地带

### R1/R16 维度检查重叠
R1 检查「task 物品是否来自已解锁维度」，R16 检查「需要维度物品的 quest 是否有 ancestor dimension task」。两者对同一问题的检查角度略有不同，但当一个 quest 需要 Nether 物品且无 ancestor dimension task 时，R1 和 R16 都会触发，产生冗余 WARNING。未定义哪个规则优先报告，或是否应该合并。

### R10/R11 Reward 检查边界
R10 检查 reward 是否桥接到 dependent（前向），R11 检查 tool reward 是否是正确的 tool（精度）。当一个 tool reward 没有被 dependent 使用时，是 R10 的 dead-end reward 还是 R11 的 wrong tool？两条规则的触发条件有交叉：如果 tool 类型正确但 dependent 不需要任何 tool，R10 应触发；如果 dependent 需要不同 tool，R11 应触发。但当前规则定义中没有明确分工。

### R19/AP18 瓶颈与奖励沙漠
R19 (Bottleneck Spacing) 检测连续高难度 quest，AP18 (Reward Desert) 检测长链无 reward。两者的触发场景高度重叠——连续 bottleneck 几乎必然伴随 reward desert。应明确：R19 是 AP18 的检测信号之一，还是独立的 pacing 规则？如果是前者，R19 应与 AP18 合并报告；如果是后者，需要定义 R19 在 reward 充足但 difficulty 连续时的独立价值。

### R37/R12 Reward 价值判断冲突
R37 (Capstone-Only Progression Break) 定义 kitchen-sink 中只有 capstone 物品才算 progression break，R12 (Reward Value Progression) 检查 reward 价值是否随 depth 递增。在 kitchen-sink 中，R37 认为 Ender Chest 不是 progression break，但 R12 可能因为其高价值而标记为异常。两条规则对「什么是过高的 reward」有不同的判定标准。

### R36/MP10 Rootless Quest 语义冲突
R36 (Dependency Root Isolation) 将非 root chapter 的 rootless quest 标为 WARNING。但 MP10 (Independent Island) 明确描述了 rootless quest 作为 catalog cell 的合法用途。Create: Delight 的 Mouse_Chef 章节有 258 个 rootless quest，全部是合法的 catalog cell。R36 的 `ROOT_CHAPTERS` 白名单不包含 catalog chapter，会对这些合法 quest 产生大量 false positive。

### R40/R18 描述质量检查层级
R18 (Description Coverage) 检查描述是否存在（P1 WARNING），R40 (Effort Preview) 检查 tier transition quest 的描述是否包含 effort preview（P2 INFO）。两者在 tier transition quest 上重叠——如果描述为空，R18 和 R40 都应触发。未定义检查优先级：是先检查 R18（存在性）再检查 R40（内容质量），还是并行检查？

### R41/R9 进度结构交互
R41 建议前 3 个 chapter 使用 flexible mode，R9 限制 dependency depth。在 flexible mode 下，depth 限制应更宽松（因为 flexible 不强制顺序），但 R9 的 `MAX_DEPTH` 不区分 progression_mode。一个 flexible chapter depth 8 和 linear chapter depth 8 的玩家体验完全不同，但 R9 一视同仁。

### R38/R10/R19 Tier Transition 三重覆盖
R38 (Tier Transition Milestone Reward)、R10 (Reward Bridge)、R19 (Bottleneck Spacing) 在 tier 边界 quest 上三者可能同时触发：R10 检查 reward 是否桥接，R38 检查 tier 边界是否有 bridge reward，R19 检查是否连续 bottleneck。对于同一个 tier-transition quest，三条规则给出的建议可能相互矛盾（R10 说 reward 未桥接，R38 说需要 tier-appropriate reward，R19 说需要 recovery quest）。

---

## SKILL.md 未覆盖的决策点

### Step 4 生成流程中的决策空白

1. **`consume_items` 策略。** SKILL.md 在 Step 2 interview 中提到「consume_items philosophy」，但 Step 4 per-node loop 没有规则指导何时设置 `consume_items: true` vs `false`。MP1 (Single-Item Gate) 说「No consume_items」，MP2 (Multi-Item Synthesis) 说「Do NOT set consume_items: true」，但 MP35 (Dual-Task Automation) 说 `consume_items: false` 是关键。缺少一个统一的 consume_items 决策框架。

2. **`repeatable` flag。** FTB Quests 支持 quest 重复完成。整个规则系统没有提及何时应将 quest 设为 repeatable——对于 mob grind quest (MP4 Escalation Ladder)、资源收集 quest、或 daily challenge quest，repeatable 是核心功能。

3. **Task type 选择决策树。** Step 4 提到「grill per task type + target + count」，但没有规则指导何时选择 `item` vs `fluid` vs `forge_energy` vs `kill` vs `advancement` vs `stat` vs `checkmark` vs `dimension` vs `biome` vs `structure` vs `observation`。MP1-MP5, MP27-MP33 覆盖了部分类型，但缺少一个统一的 task-type 选择决策树。

4. **`only_from_crafting` flag。** SKILL.md 的 design-guide.md §98 提到此字段，但 Step 4 没有规则指导何时使用。对于 teach-crafting quest 和 obtain-by-any-means quest，`only_from_crafting` 的选择至关重要。

5. **Auto-claim vs manual-claim reward 策略。** `exclude_from_claim_all` 在 AP17 中被提到用于防止 xp_levels 批量领取，但没有规则指导何时设置 reward 为 auto-claim vs manual-claim。这影响 claim-all 行为和 multiplayer 体验。

6. **Chapter `progression_mode` 选择。** R41 建议 early-game 用 flexible，但 Step 2 interview 中没有明确的决策分支帮助选择每个 chapter 的 progression_mode。整个包使用统一 mode 还是 per-chapter 设置？

7. **`quest_links` 使用策略。** SKILL.md 提到 quest_links (hexagon, size 2.0) 用于 cross-listing，但 Step 4 loop 没有规则指导何时创建 quest_link vs 直接依赖 vs 复制 quest。R39 (Guide Quest Deduplication) 建议用 quest_links 替代重复，但没有定义 quest_link 的创建条件。

8. **`chapter_groups` 分组策略。** SKILL.md 提到「group ~5-8 chapters/tab」，但没有规则指导如何将 chapters 分组。分组影响玩家的导航体验和 chapter ordering 语义。

9. **Chapter icon 选择。** 每个 chapter 需要一个 icon 物品，但没有规则指导选择标准——应选 mod 的 signature item、tier 的 material、还是 thematic item？

10. **多 locale 文本同步。** Step 4 提到「Translate to secondary locales in a dedicated pass」，但没有规则确保不同 locale 的 description 内容一致。翻译可能引入 AP1 变体（中文描述准确但英文描述过时）。

11. **`default_quest_shape` per-chapter 选择。** MP20 和 R35 讨论了 shape 语义一致性，但 Step 2/3 没有规则指导每个 chapter 的 `default_quest_shape` 选择。ATM 用 hexagon/gear/diamond 区分 chapter 类型，非 ATM 包需要自己的策略。

---

## 新规则 R36-R41 与现有规则的关系

### R36 (Dependency Root Isolation) vs R6 (Unreachable Quest)
- **重叠度：中等。** R6 检查 quest 是否可达（从 root 有路径），R36 检查 quest 是否有 dependency（非 root chapter）。一个 rootless quest 在非 root chapter 中是 R36 WARNING 但**不一定**是 R6 ERROR——它可能是可达的（因为 rootless = 无前置条件 = 始终可见/可完成）。R36 是图卫生规则（structural hygiene），R6 是功能可达性规则（functional reachability）。
- **冲突：无直接冲突，但有 false positive 风险。** MP10 (Independent Island) 的 catalog cell 是合法的 rootless quest，R36 会对它们产生 WARNING。建议 R36 增加 catalog chapter 的例外条件。

### R37 (Capstone-Only Progression Break) vs R12 (Reward Value Progression) + AP8 (Reward Inflation)
- **重叠度：高。** R37 定义 kitchen-sink 中什么算 progression break（只有 capstone items），R12 检查 reward 价值是否递增，AP8 警告 reward 过早过大。R37 实际上是对 AP8 的**pack-type 特化**——它缩小了 kitchen-sink 中 AP8 的触发范围。
- **冲突：潜在冲突。** R37 认为 Ender Chest 在 kitchen-sink 中不是 progression break（INFO），但 R12 可能因为其高市场价值而标记为 reward value 异常（WARNING）。需要明确：当 R37 和 R12 对同一 reward 有不同判定时，R37 的 pack-type 判定应优先。

### R38 (Tier Transition Milestone Reward) vs R10 (Reward Bridge) + R19 (Bottleneck Spacing)
- **重叠度：高。** R38 检查 tier 边界 quest 是否有 bridge reward，R10 检查所有 quest 的 reward 是否桥接，R19 检查连续 bottleneck。R38 是 R10 在 tier 边界的特化版本，加上 R19 的 effort spike 条件。
- **冲突：无直接冲突，但报告冗余。** 一个 tier-transition quest 缺少 bridge reward 会同时触发 R10 (INFO: reward has no bridge)、R38 (WARNING: tier transition without bridge reward)、R19 (WARNING: bottleneck streak)。建议 R38 作为 R10 的增强版在 tier boundary 取代 R10 报告，避免同一问题三次报告。

### R39 (Guide Quest Deduplication) vs R22 (Cross-Chapter Dependency Validity)
- **重叠度：低。** R22 检查跨 chapter dependency 引用是否指向存在的 quest（数据完整性），R39 检查 guide quest 是否在多个 chapter 中重复（内容维护）。两者检查的维度不同。
- **互补关系良好。** R22 确保引用不断裂，R39 确保内容不重复。无冲突。

### R40 (Effort Preview in Description) vs R18 (Description Coverage)
- **重叠度：中等。** R18 检查描述是否存在/足够长，R40 检查 tier transition 描述是否包含 effort preview。R40 是 R18 在 tier transition 场景的增强版。
- **冲突：无。** R40 是 INFO 级别，R18 是 WARNING 级别。当描述为空时 R18 触发，当描述存在但缺少 effort preview 时 R40 触发。层级清晰。

### R41 (Early-Game Flexible Mode) vs R9 (Dependency Depth)
- **重叠度：低。** R41 检查 chapter 的 progression_mode 设置，R9 检查 dependency depth。两者操作在不同维度。
- **潜在交互：** R41 建议 early-game 用 flexible mode，而 flexible mode 下 R9 的 MAX_DEPTH 阈值可能需要调整（flexible mode 下 depth 8 的玩家体验比 linear mode 下轻松得多）。当前 R9 不区分 progression_mode，这是一个需要补充的交互点。

### 总体评估
R36-R41 与 R1-R35 没有严重冲突。主要问题是**报告冗余**（R38/R10/R19 在 tier transition 上三重触发）和**false positive 风险**（R36 对 catalog cell 的误报）。建议在规则执行优先级表中明确：当多条规则对同一 quest 产生 WARNING 时，哪条规则的报告优先显示。

---

## 未覆盖的 FTB Quests 功能

### 1. Team Rewards (`default_reward_team`, `team_reward`)
- **覆盖状态：极弱。** R29 (Team Progression Consistency) 仅检查 team mode 下的 material bridge 分配问题。`default_reward_team` 在 SKILL.md 的 spec skeleton 中出现（`data: { default_reward_team: false }`），但没有规则指导何时设为 true。TheWinterRescue 的 `frostedheart:insight` 使用 `team_reward: true`，这是一个被观察到但未被规则化的模式。
- **缺失规则：** 当 pack 设计为 team-friendly 时，material bridge reward (MP14) 是否应该 team-shared？如果只有提交者获得 bridge material，其他 team members 无法完成后续 quest。

### 2. Repeating Quests / Repeatable Flag
- **覆盖状态：零。** `repeatable` 字段在整个规则系统中完全未提及。FTB Quests 允许 quest 重复完成（reset after completion），这对 mob grind (MP4)、daily challenge、resource farming 等场景至关重要。
- **缺失规则：** (1) 高价值 reward quest 如果 repeatable，可能导致 economy exploit（R12/R13 未考虑 repeatable 对 reward economy 的影响）。(2) AP13 (Premature Item Submission) 的修复建议提到「repeatable quest」作为 recovery mechanism，但没有规则指导如何设计 recovery quest。

### 3. Quest Chains with Timers
- **覆盖状态：零。** FTB Quests 支持 quest-level timer（限时完成任务）。Timer 在 speedrun pack、challenge chapter、event-based content 中常见，但整个规则系统和模式库中完全未提及。
- **缺失规则：** Timer 与 dependency chain 的交互——如果 timed quest 是 chain 中的一环，timer 失败是否阻塞后续 quest？Timer 与 `hide_until_deps_visible` 的交互——hidden quest 的 timer 何时开始计时？

### 4. Auto-claim Behavior (`autoclaim`, `exclude_from_claim_all`)
- **覆盖状态：部分。** AP17 提到 `exclude_from_claim_all` 用于防止 xp_levels 批量领取，但没有系统性的 auto-claim 策略规则。
- **缺失规则：** (1) 哪些 reward 类型应设为 auto-claim（XP drip）vs manual-claim（choice reward）？(2) claim-all storm 风险（AP15）——当 50 个 quest 都有 auto-claim command reward 时的 TPS 影响。(3) `exclude_from_claim_all` 应在哪些场景使用？

### 5. `consume_items` Task Flag
- **覆盖状态：矛盾。** MP1 说「No consume_items」，MP2 说「Do NOT set consume_items: true」，MP35 说「consume_items: false is critical」。但 Step 2 interview 提到需要决定「consume_items philosophy」，Step 4 没有对应的决策规则。
- **缺失规则：** 何时 `consume_items: true`（物品被 quest 消耗 = 提交给 quest）vs `false`（物品保留在背包 = 证明拥有）。这影响玩家的资源管理体验和 quest 的经济模型。

### 6. `only_from_crafting` Task Flag
- **覆盖状态：极少。** design-guide.md §98 提到 Create: Delight 不使用 `only_from_crafting`，但没有规则指导何时使用。
- **缺失规则：** 当 quest 目的是教 crafting recipe 时应设 `only_from_crafting: true`（必须亲手合成），当目的是证明拥有时可设 `false`（可以交易/拾取）。

### 7. Chapter Images (`images[]`)
- **覆盖状态：几乎为零。** SKILL.md 提到「chapter images (images[]) can be authored whenever their owning quest comes up in the loop」，但没有规则或模式指导何时、如何使用 chapter images。ATM-10 的 Mekanism chapter 使用 extensive image assets 作为教程辅助，这是一个被观察到但未被规则化的实践。

### 8. `min_tasks` / `min_deps` (Partial Completion)
- **覆盖状态：弱。** MP32 记录了 `min_tasks` 的用法，但标注为「Low confidence (Create: Astral only, single-source)」。`min_deps` 完全未被规则化。
- **缺失规则：** `min_tasks` 与 R14 (Teach-Then-Do) 的交互——如果 teaching quest 的 `min_tasks` 允许跳过部分教学内容，teach-then-do 顺序可能被绕过。

### 9. `always_invisible` Chapter Behavior
- **覆盖状态：部分。** MP23 (Invisible Infrastructure) 记录了 expert pack 的 invisible chapter 用法，但没有规则验证 invisible chapter 的正确性。
- **缺失规则：** (1) invisible chapter 的 quest 不应有 player-facing reward（如果有，reward 在 UI 中不可见但仍可领取）。(2) invisible chapter 的 dependency 引用应仅来自其他 invisible chapter 或明确的 stage-gate quest。(3) R20 (Chapter Completion Testability) 对 always_invisible chapter 的处理未定义。

### 10. Quest Shape `default_quest_shape` Inheritance
- **覆盖状态：部分。** R35 检查 shape 一致性，MP20 描述 shape-as-tier，但没有规则指导 `default_quest_shape` 的 per-chapter 选择。
- **缺失规则：** 当 pack 不使用 ATM 级别的 shape vocabulary 时（大多数包），`default_quest_shape` 应该统一为 `circle` 还是按 chapter 类型变化？

### 11. `hide_dependent_lines` vs `hide_dependency_lines`
- **覆盖状态：有描述但无决策规则。** SKILL.md 的 layout 部分描述了这两个 flag 的区别和用法，但没有规则指导何时使用哪个。ATM 大量使用两者（438 个 `hide_dependency_lines`），curated pack 几乎不用。
- **缺失规则：** (1) hub quest (fan-out > 3) 何时用 `hide_dependency_lines`？(2) convergence quest (fan-in > 3) 何时用 `hide_dependent_lines`？(3) 两者的组合使用条件。

### 12. `secret` Quest Design
- **覆盖状态：部分。** AP7 (Hidden Quest Trap) 和 R21 (Hidden Quest Signpost) 覆盖了 `hide_until_deps_visible` 的风险，但 `secret: true`（需要特定触发条件发现）的设计规则不足。
- **缺失规则：** secret quest 的发现触发条件设计——哪些触发条件是「自然遇到」的（biome visit），哪些需要刻意寻找（特定物品 pickup）？R21 仅检查是否有 signpost，不检查触发条件的自然性。

### 13. Cross-Chapter Quest Links (`quest_links[]`)
- **覆盖状态：弱。** SKILL.md 提到 quest_links 用于 cross-listing（hexagon, size 2.0），R39 建议用 quest_links 替代 guide quest 重复，但没有规则定义 quest_links 的创建条件、视觉规范、或最大密度。
- **缺失规则：** (1) 一个 quest 最多被 link 到几个 chapter？(2) quest_link 的 shape 是否必须为 hexagon？(3) quest_link 是否应继承目标 chapter 的 `default_quest_shape`？

---

## 总结

当前规则系统（R1-R41, MP1-MP38, AP1-AP20, PP1-PP7）覆盖了 FTB Quests 设计的核心三角——物品可达性、依赖完整性、奖励连贯性——但在以下维度存在系统性空白：

1. **FTB Quests 机制层**：repeatable、timer、team reward、auto-claim、consume_items/only_from_crafting 策略均缺少规则覆盖。这些是 FTB Quests 的原生功能，在生成流程中需要决策但没有规则指导。

2. **Expert 包精度**：R3 的 heuristic 对 expert 包（合成深度 15+）几乎无效，R1 的 L1 映射对 200+ mod 包覆盖率极低。需要更强的 L2/L3 数据管线或接受这些规则在 expert 场景下的降级行为。

3. **规则间报告冗余**：R38/R10/R19 在 tier transition 上的三重覆盖、R36/MP10 在 rootless quest 上的语义冲突，需要在执行优先级表中增加去重和仲裁逻辑。

4. **Step 4 决策点**：至少 11 个 per-node 决策点（consume_items、only_from_crafting、repeatable、task type、auto-claim、quest_links 等）缺少规则覆盖。这些决策在 Step 4 的 grill-me 流程中需要被问到，但当前没有规则告诉 AI 如何判断用户的选择是否合理。
