## Reviewer C — 实用性审查 · Cycle 17

审查范围：topology-coordinates.md (Cases 49-54, Mixed Topology Analysis, Phase 4 碰撞检测)、micro-patterns.md (MP72, MP73)、progression-rules.md (R106-R116)、SKILL.md (Step 3/4 引用检查)

---

### SKILL.md 引用完整性 — 不可执行

**问题：** SKILL.md 的 Step 3 和 Step 4 **完全没有引用** R106-R116、MP72、MP73 或 Cycle 17 的任何新增内容。`grep` 搜索 "R106"、"R110"、"MP72"、"MP73"、"Cycle 17"、"Section G"、"International" 全部返回空结果。module-index.md 同样没有路由条目。

这意味着即使 reference 文件中的规则写得再好，AI agent 在执行 Step 3/Step 4 时也**不会被引导去加载它们**。这是 Cycle 17 最关键的实用性缺陷——规则存在于 reference 中但不在 agent 的执行路径上。

**改进建议：**
- SKILL.md Step 3 需要增加一行：`For chapters exceeding 80 quests, load reference/design/topology-coordinates.md §Phase 2.5 and §MP73 for sub-region decomposition guidance.`
- SKILL.md Step 4 的 "Progression architecture check" 段落（已有 R101-R105）需要追加 R106-R116 的适用条件路由，或在 Step 5 的 whole-book pass 中增加 `R106–R116` 的检查触发条件。
- module-index.md 需新增 Section G 的路由条目。

---

### R106 — Dimensional Progression Naturalism — 部分可执行

**评估：**
- **可执行部分：** "For each dimension-gating quest, verify that at least 3 other quests in the current dimension must be completed before the gate quest becomes available." 这是一个明确的阈值判断（≥3 same-dimension prerequisites），AI 可以直接数 `depends_on` 链中的同维度 quest 数量。
- **不可执行部分：** "the dimension transition itself feels earned rather than arbitrary" — "feels earned" 是一个主观判断，AI 没有玩家体验模型。虽然 implementation check 将其操作化为 ≥3 前置任务的计数检查，但规则描述中的动机设计意图超出了 AI 的判断能力。
- **严重度分类合理：** WARNING 级别适当，不阻断生成。

**判定：部分可执行。** 计数检查可执行，动机评估不可执行。

---

### R107 — Olive-Shaped Equipment Distribution — 部分可执行

**评估：**
- **可执行部分：** "Count the number of distinct equipment items at each tier. If mid-tier count < early-tier count OR mid-tier count < late-tier count, flag as INFO." 这是一个清晰的数值比较。
- **不可执行部分：** AI agent 无法自主判断什么是"equipment items"——需要用户声明哪些物品属于装备（武器/护甲/工具），且"tier"的定义需要 L2 级数据（stage_map）。如果用户没有提供 stage 数据，AI 需要自己推断 tier 边界，这涉及到对 mod 物品功能的理解。
- **严重度分类合理：** INFO 级别正确——过于模糊的规则不应阻断生成。

**判定：部分可执行。** 有 L2 数据时完全可执行；无 L2 数据时 AI 无法确定 tier 边界。

---

### R108 — Gear-to-Mob Cross-Dimension Scaling — 不可执行

**评估：**
- **核心问题：** "Compare the DPS/damage/armor values of the source dimension's best equipment against the target dimension's basic mob HP/damage." — AI agent **完全无法获取** 这些数据。FTB Quests 配置不包含 DPS 值、怪物 HP、护甲值。这些信息存在于 mod 的 Java 源码或 game data 中，不在 quest config 的可达范围内。
- **阈值明确但数据不可达：** "source best DPS > 3x target basic mob HP" 和 "< 0.3x" 是清晰的判断标准，但前提是 AI 能拿到 DPS 和 HP 数据，这在当前的 toolchain 中不可能。
- **Fallback 缺失：** 规则没有提供当 DPS/HP 数据不可用时的降级策略（如使用物品 tier heuristic）。

**判定：不可执行。** 需要添加 L1 heuristic fallback（如基于物品名称的 tier 推断）或明确标注为 "requires user-provided balance data"。

---

### R109 — Forced Anti-Skip Material Binding — 部分可执行

**评估：**
- **可执行部分：** "check world-generation configs to verify that the material's ore generation is restricted to its intended dimension." 如果 pack 提供了 world-gen config 文件（如 Datapack 的 ore generation JSON），AI 可以解析并检查维度限制。
- **不可执行部分：** AI 无法独立确定一个物品的"intended dimension"——这需要 mod 知识或用户提供。规则假设了 stage-resource mapping 的存在（`stage_available_resources`），但如果 Step 2 没有收集到这些数据（许多 pack 不提供），检查就无法执行。
- **与 R101 的重叠：** R109 是 R101 的世界生成层，两者在检查对象上有大量重叠。AI 执行 R101 时已经在检查 stage 锁定，R109 额外要求检查 world-gen config 是一个不同的文件路径，但逻辑上可以合并。

**判定：部分可执行。** 有 world-gen config + stage data 时可执行；否则降级为询问用户。

---

### R110 — Mid-Game Density Priority — 可执行

**评估：**
- **核心问题回答：** "AI 怎么知道当前是'中期'？" — 规则给出了明确的操作性定义：
  - early-game = "chapters 1-2 or first 20% of dependency depth"
  - mid-game = "chapters 3-N-1 or middle 60%"
  - late-game = "last chapter or final 20%"
- **阈值清晰：** "mid-game quest count < 40% of total → flag INFO"、"early-game > 30% → flag INFO"。
- **数据可达：** quest count 和 dependency depth 都可以从 `existing_quests.json5` 或生成的 spec 中直接计算。

**判定：可执行。** 这是 Cycle 17 中实用性最好的规则之一。定义清晰、阈值明确、数据可达。

---

### R111 — Anti-Forced-Lifespan Extension — 可执行

**评估：**
- **可执行检查 1：** "ratio of unique task types to total quests" — 可直接计算。
- **可执行检查 2：** "if 3+ consecutive quests in a chain require the same task type with increasing quantities (e.g., 10 iron → 50 iron → 200 iron)" — 可执行。AI 可以扫描 dependency chain 中连续 quest 的 task type 和 count 值，检测是否存在类型相同且数量递增的序列。
- **"quantity escalation" 阈值：** 规则说的是 "increasing quantities"，但没有给出具体的递增比例阈值。10→50→200 是 5x→4x 递增，但 10→12→15 算不算？建议添加最小递增倍率（如 ≥2x）。

**判定：可执行。** 检测逻辑清晰，但 quantity escalation 的递增阈值可以更精确。

---

### R112 — Vanilla Enhancement Layering — 部分可执行

**评估：**
- **可执行部分：** "For each mod-introduction quest, check whether a vanilla equivalent task exists earlier in the dependency chain." AI 可以检查 quest 的 ancestor chain 中是否存在使用 vanilla 物品（`minecraft:*` namespace）的 task。
- **不可执行部分：** "vanilla equivalent" 的判断——什么是 AE2 的 ME Controller 的 "vanilla equivalent"？AI 无法自动判断一个 mod 机器的 vanilla 对应物是什么。只有当 mod-introduction quest 本身包含 vanilla 物品 task 时，检查才是可操作的。
- **降级合理：** "This is informational because some mods have no vanilla equivalent." INFO 级别正确。

**判定：部分可执行。** namespace 检查可执行；语义等价判断不可执行。

---

### R113 — Multi-Dimensional State Synchronization — 部分可执行

**评估：**
- **可执行部分：** "count the number of game systems affected" 的 6 个维度（recipes/dimensions/ores/mobs/villagers/UI）是明确的检查项。
- **不可执行部分：** AI 无法从 quest config 中自动判断一个 stage transition 影响了多少个 game system——这些信息存在于 KubeJS scripts、CraftTweaker scripts、Game Stages configs 中，不在 FTB Quests 的 quest config 范围内。除非 AI 能读取 `/scripts/` 和 `/config/gamestages/`，否则只能依赖用户声明。
- **降级策略：** 可以检查 quest reward 中是否包含 `gamestage` 类型的 reward，如果包含则检查该 quest 的描述中是否提及多个系统变化。但这是文本分析，不是系统计数。

**判定：部分可执行。** 检查框架清晰，但数据源超出 quest config 范围。

---

### R114 — Quest-to-Stage Reward Bridge — 可执行

**评估：**
- **核心检查完全可执行：** "verify that the quest has a command reward that grants the appropriate game stage" — AI 可以检查 chapter-final quest 的 rewards 中是否包含 `type: "ftbquests:command"` 且 `command` 字段包含 `gamestage add`。
- **stage name 匹配：** "verify that the stage name in the command reward matches the stage name used in Recipe Stages/Item Stages configs" — 如果 AI 能读取 `/config/recipestages/` 则可以执行；否则只能检查 command reward 的存在性。
- **严重度分级合理：** ERROR (expert) / WARNING (semi-gated) 区分合理。

**判定：可执行。** command reward 检查是纯 config 解析，完全在 AI 能力范围内。

---

### R115 — Container-Level Recipe Locking — 部分可执行

**评估：**
- **可执行部分：** "If the pack includes Recipe Stages and any automation crafting mod" — AI 可以从 modlist 中检测 Recipe Stages 和 AE2/RS/Create 的存在。
- **不可执行部分：** "verify that setContainerStages or setPackageStages is configured" — 需要读取 KubeJS/CraftTweaker scripts 或 Recipe Stages config，这在当前 toolchain 中不在标准检查范围内。
- **降级策略可行：** AI 可以从 modlist 判断风险存在（有 Recipe Stages + 自动化 mod），然后发出 WARNING 并建议用户检查 config。

**判定：部分可执行。** 风险检测可执行（基于 modlist），config 验证不可执行。

---

### R116 — Advancement-As-Progression-Gate Pattern — 部分可执行

**评估：**
- **适用条件窄：** 仅适用于 "Packs that use vanilla advancements as the primary progression system"，大多数 FTB Quests pack 不适用。
- **可执行部分：** 4 个检查元素（custom advancement、ore visibility、recipe visibility、mob spawns）是明确的 checklist。
- **不可执行部分：** 与 R113 相同——这些变化发生在 KubeJS/GameStages 层面，不在 quest config 范围内。

**判定：部分可执行。** 适用范围窄，且在适用时数据源超出 quest config。

---

### MP72 — Tree-with-Capstone Convergence — 可执行

**评估：**
- **Step 2 可执行：** "Design the first N-1 quests as a tree_branching layout" + "capstone quest has dependencies on ALL prior quests" — 这是明确的 outline 设计指令，AI 可以直接执行。
- **Step 4 可执行：** "capstone shape (gear or hexagon) and size 3.0-4.0" + "task type is checkmark" — 明确的参数值。
- **Step 5 可执行：** "check capstone dep count matches quest count - 1" — 简单的数值验证。
- **Coordinate template 可执行：** `Main tree: x=[-6..18], y=[-3..9]` + `Capstone: (6.0, -6.0)` — 给出了具体的坐标范围。
- **[Needs-Validation] 标注适当：** 只有 TeamAOF 单一来源，需要更多验证才能作为通用模式推荐。

**判定：可执行。** 参数明确、步骤清晰、coordinate template 具体。

---

### MP73 — Sub-Region Decomposition for Large Chapters — 可执行

**评估：**
- **触发条件明确：** "80+ quests" — 简单计数判断。
- **分解步骤可执行：** "4-6 sub-regions" + "4-8 units of separation" + "each sub-region has its own hub quest" — 所有参数都有数值范围。
- **子拓扑选择可执行：** "Processing chains → linear_chain" / "Collection catalogs → grid_catalog" / "Variant items → hub_fan" — 明确的映射规则。
- **Coordinate template 可执行：** 给出了 6 个 sub-region 的具体 x/y 范围示例。
- **[Indirectly-Validated] 标注合理：** 虽然没有直接的玩家正面评价，但 4 个 anti-pattern 源（post/2494, Craftoria #231, PP20, AP28）的收敛验证是有说服力的。

**判定：可执行。** 这是 Cycle 17 中实用性第二好的条目。

---

### Cases 49-54 — 可执行（作为参考数据）

**评估：**
- Cases 49-54 是**参考案例数据**，不是规则。它们为 AI 提供 layout 参考（坐标范围、shape 分布、icon rate 等），当 AI 需要生成类似内容时可以参考。
- **Case 49 (No-Flesh-Within-Chest ch1):** 提供了中文 tree_branching 的垂直 top-to-bottom 布局模式，rsquare-for-milestone 模式（7 occurrences），bounding box 22x19。AI 可以参考但不需要"执行"。
- **Case 50 (boss chapter):** dual-column hub_fan 模式，90% icon rate，70% kill task rate——这些参数可以作为 boss-catalog 章节的模板。
- **Case 51 (tetra):** tool-progression tree，rsquare-for-milestone（5 occurrences），hide_dependency_lines: true——参数具体。
- **Case 52 (AOF-6 create):** "tree with capstone" 模式，68-dep convergence node，gear shape size 4.0——直接支撑 MP72。
- **Case 53 (AOF-6 botania):** 6 sub-region tree，100+ quests，32.5-unit width（超出 R59）——直接支撑 MP73。
- **Case 54 (AOF-6 agriculture):** 6 sub-region grid_catalog，zero shape overrides，5 convergence nodes——直接支撑 MP73。

**判定：可执行（参考数据）。** 数据完整，格式一致，可直接作为 layout 模板参考。

---

### Mixed Topology Analysis — 可执行（作为参考框架）

**评估：**
- 4 个 Key Observations 提供了分解决策的操作性指导：
  1. "Sub-region decomposition follows mod boundaries" — 告诉 AI 按什么切分（mod/subsystem）。
  2. "Shape-as-category bridges sub-regions" — 告诉 AI 保持 shape 语义一致性。
  3. "Transitions are dependency-driven" — 告诉 AI 不需要设计 bridge quest。
  4. "4-6 sub-regions" — 认知上限，Miller's law 验证。
- Steamcreate2 overworld 案例（4 zones）和 AOF-6 botania（6 sub-regions）提供了可参考的分解示例。

**判定：可执行。** 作为 Phase 2.5 的补充分析框架，提供了 AI 可操作的分解策略。

---

### Phase 4 碰撞检测算法 — 可执行

**评估：**
- **算法完整性：** Cycle 17 已经将 Phase 4 从 "LLM 不可执行" 升级为完整的可执行伪代码：
  - `resolve_collisions` — 主循环，3 轮迭代
  - `find_collisions` — O(n^2) 碰撞检测（n<300 可接受）
  - `classify_priority` — hub/mid/leaf 分类（基于 fan_in + fan_out ≥ 3 阈值）
  - `group_by_y_row` — y 行分组（tolerance=0.3）
  - `dependency_direction` — 单位向量计算
  - `reassign_coordinates` — 坐标缩放（spacing *= 1.1）
- **终止条件明确：** Success（空列表）/ Partial success（碰撞减少）/ Stagnation（2 轮无减少 → 缩放）/ Hard failure（3 轮 + 1 缩放后仍有碰撞 → emit warning + hide_dependency_lines）
- **与 Phase 1-3 的集成合约完整：** 输入（Phase 3 坐标 + Phase 1 图结构）、输出（修正后坐标 → Phase 5）、副作用（hide_dependency_lines → Phase 6）
- **碰撞易发拓扑排序：** hub_fan > diamond_convergence > tree_branching > highway_branch > others — 给出了预期碰撞频率。

**关键改进点：** 这不再是"标注为不可执行"的算法。伪代码足够详细，如果未来实现为 Python 脚本（`resolve_collisions.py`），可以直接翻译。但**当前 AI agent 需要在生成过程中手动模拟执行**这个算法——这对 LLM 来说是可行的（逐步移动坐标），但容易出错（数值精度、多轮迭代的跟踪）。

**判定：可执行（作为伪代码）。** 建议实现为 Python 脚本以消除 LLM 手动模拟的出错风险。

---

### Phase 2.5 大章分解算法 — 可执行

**评估：**
- **触发阈值明确：** `quest_count > 80` — 简单计数。
- **modularity_split 算法完整：** Newman's greedy modularity optimization，有完整伪代码，包括：
  - ΔQ 计算公式：`2 * (e_ij - a_i * a_j)`
  - 最小社区大小参数：`min_component_size=15`
  - 小社区合并策略：merge into nearest neighbor with most cross-edges
- **5 种分解模式明确：**
  - Pattern 1 (Monolithic): max_region > 80% → skip decomposition
  - Pattern 2 (Dual-Region): 35-50% × 2 → primary/secondary 60/40
  - Pattern 3 (Quadrant): ~25% × 4 → 2×2 grid
  - Pattern 4 (Fragmented): max_region < 5% → parallel columns
  - Pattern 5 (Compartment): 4-10 regions × 10-25% → equidistant
- **Bridge node 坐标公式精确：** weighted midpoint + perpendicular offset for close regions
- **空间分配策略表完整：** 每种 pattern 的 primary width、secondary layout、bridge count expectation

**判定：可执行。** 算法完整，阈值明确，模式分类有决策条件。与 Phase 4 一样，建议实现为 Python 脚本。

---

### R106 vs R111 冲突检查 — 无冲突

**评估：** R106（维度转换自然感）和 R111（反强制延长寿命）不冲突。R106 关注的是维度间的转换动机，R111 关注的是后期任务类型多样性。执行 R106 不会导致违反 R111。

### R107 vs R111 冲突检查 — 已识别张力

**评估：** 文档已经识别了这个张力（Tension 8），并给出了解决方案：quality vs. quantity。R107 指的是有意义的选项种类，R111 针对的是重复内容的膨胀。这是互补关系而非冲突。

### R110 vs R112 冲突检查 — 已识别张力

**评估：** 文档已经识别了（Tension 9）：R112 建议渐进引入 mod，R110 建议尽快进入中期。解决方案是 parallel introduction——同时引入多个 mod。合理。

### R106 vs R101 冲突检查 — 已识别张力

**评估：** 文档已经识别了（Tension 7）：naturalism vs. enforcement。解决方案是 complementary——自然感作为设计意图，enforcement 作为安全网。合理。

---

## 最终结果

### 可执行率统计

| 条目 | 判定 | 说明 |
|------|------|------|
| SKILL.md 引用完整性 | 不可执行 | Step 3/4 未路由到 Cycle 17 任何新规则 |
| R106 | 部分可执行 | 计数检查 OK，动机评估不可 |
| R107 | 部分可执行 | 需 L2 tier 数据 |
| R108 | 不可执行 | DPS/HP 数据不可达 |
| R109 | 部分可执行 | 需 world-gen config |
| R110 | **可执行** | 定义、阈值、数据均可达 |
| R111 | **可执行** | 检测逻辑清晰 |
| R112 | 部分可执行 | namespace 检查 OK |
| R113 | 部分可执行 | 数据源超出 quest config |
| R114 | **可执行** | command reward 检查完全可达 |
| R115 | 部分可执行 | modlist 风险检测 OK |
| R116 | 部分可执行 | 适用范围窄 |
| MP72 | **可执行** | 参数、步骤、坐标模板完整 |
| MP73 | **可执行** | 触发条件、分解策略完整 |
| Cases 49-54 | **可执行** | 参考数据完整 |
| Mixed Topology Analysis | **可执行** | 分解框架可操作 |
| Phase 4 碰撞检测 | **可执行** | 伪代码完整 |
| Phase 2.5 大章分解 | **可执行** | 算法完整 |

**可执行率：** 8/18 完全可执行 + 8/18 部分可执行 + 2/18 不可执行

- 完全可执行：**44%**（8/18）
- 部分可执行：**44%**（8/18）——在这些情况下，核心逻辑可执行但缺少降级策略或数据源
- 不可执行：**11%**（2/18）

如果将"部分可执行"视为 0.5，则加权可执行率 = (8 + 4) / 18 = **67%**

### 不可执行条目列表

1. **SKILL.md 引用完整性** — Cycle 17 所有新规则均未在 Step 3/Step 4 中路由
2. **R108 (Gear-to-Mob Cross-Dimension Scaling)** — DPS/HP 数据在 quest config toolchain 中不可达，且缺少 L1 heuristic fallback

### 最关键的 3 个改进建议

**1. [最高优先] 在 SKILL.md 中建立 Cycle 17 规则的引用路由**
在 Step 3 添加 Phase 2.5 + MP73 的加载指令，在 Step 4 的 "Progression architecture check" 段落后追加 R106-R116 的适用条件路由（参考 R101-R105 的现有格式），在 Step 5 的 whole-book pass 中增加 Section G 的检查触发。没有路由的规则等于不存在的规则。

**2. [高优先] 为 R108 添加 L1 heuristic fallback**
当 DPS/HP 数据不可用时（即所有情况），降级为：(a) 基于物品 namespace + 名称的 tier 推断（如 `netherite`/`dragon`/`end` 关键词 → late-tier），(b) 基于 BUILTIN_TOOL_TIER_MAP 的装备等级比较（如果两个维度的装备都在 builtin table 中），(c) 如果两者都不在表中，标记 `[unverified:combat_balance]` 并 surface to user。

**3. [高优先] 为所有"部分可执行"规则添加显式降级路径**
R107/R109/R112/R113/R115/R116 的共同问题是：当理想数据源不可用时，规则没有说明应该怎么做。每条规则需要增加一个 "Degradation" 段落，格式如：
```
**Degradation path (when L2 data unavailable):**
- Fall back to [具体 L1 heuristic]
- If L1 also unavailable, mark [unverified:XXX] and surface to user
- Severity downgrades from WARNING to INFO
```

---

*Reviewer C · Cycle 17 Phase 4 · 2026-07-17*
