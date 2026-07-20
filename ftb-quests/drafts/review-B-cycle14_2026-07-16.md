# 审查员 B — 完备性审查 (Cycle 14)

**审查日期:** 2026-07-16
**审查范围:** PP13, PP14, AP36, AP37, R82-R90
**审查方法:** 边界情况分析、交互效应检测、遗漏维度扫描、极端值测试

---

## 审查结论

| 模式/规则 | 结论 | 关键问题数 |
|-----------|------|-----------|
| PP13 Reward-Type Contract | GAPS | 4 |
| PP14 Progression-as-Reward | GAPS | 5 |
| AP36 Reward-Type Roulette | GAPS | 3 |
| AP37 Convergence Claustrophobia | GAPS | 4 |
| R82 Backward Design Convergence | GAPS | 2 |
| R83 Weak Lock Permeability | GAPS | 3 |
| R84 Mid-Game Mechan Density | GAPS | 3 |
| R85 Dual-Direction Reward Principle | GAPS | 2 |
| R86 Description-as-Pathway Clarity | COMPLETE | 1 |
| R87 Anti-Nerf Progression Respect | GAPS | 2 |
| R88 Reward-Type Contract Enforcement | GAPS + CONFLICT | 4 |
| R89 Progression-as-Reward Viability | GAPS + CONFLICT | 4 |
| R90 Convergence Item Backtracking | GAPS | 3 |

**总结论:** GAPS — 存在系统性遗漏，主要集中在多人游戏/服务器维度、规则间阈值不一致、以及极端包规模下的适用性问题。无阻断性冲突，但 R88/R89 与已有规则存在条件集合重叠和严重度不一致。

---

## 详细审查

### PP13 — Reward-Type Contract

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **章节间过渡任务:** PP13 规定章节内使用"exactly one primary reward delivery mechanism"，但未处理跨章节边界的过渡。当 Chapter A 使用 command rewards 而 Chapter B 使用 loot tables 时，玩家在章节边界处仍会经历与章节内部相同的"reward-type surprise"。PP13 的范围局限于单章节，但玩家体验是连续的。
  2. **跨章节任务链:** 当一个任务链跨越多个章节时（通过 R22 cross-chapter dependency），奖励类型应该跟随链还是跟随章节？PP13 未给出指导。
  3. **服务器权限问题:** MP64 的 command reward 模式依赖 `/execute at @p run loot spawn` 命令。在权限配置不当的服务器上，command rewards 可能静默失败，导致整个章节的奖励传递机制崩溃。PP13 推荐"all commands"但未考虑命令执行的可靠性前提。
  4. **奖励策略演进中的中间态:** Enigmatica 谱系的证据 (E6→E9E→E9→E10) 显示奖励类型在包更新过程中会变化。PP13 未讨论在策略迁移期间（部分任务已迁移、部分未迁移）的临时不一致是否可接受。

- **与已有规则的冲突:**
  - MP67 (Task-Type Diversity) 推荐"Use choice rewards at the end of major sections to let players pick their next upgrade path"，但 PP13 规定 choice rewards 仅可用于"a single chapter capstone"。MP67 暗示每个 major section 结尾都可用 choice reward，PP13 限制为整个章节仅一个。这是**实质性冲突**——同一份参考文档中的两条指导给出了相互矛盾的 choice reward 使用频率建议。

- **建议:**
  1. 补充章节间过渡指导：建议同一 pack 内相邻章节使用相同奖励类型，或在章节入口任务中明确标注类型变化。
  2. 补充服务器环境前提条件：command reward 一致性需以服务器权限正确配置为前提。
  3. 与 MP67 协调 choice reward 频率——要么修订 PP13 允许多个 section-end choice rewards，要么修订 MP67 限制为仅 capstone。

---

### PP14 — Progression-as-Reward Social Contract

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **"5 分钟感知"规则的模糊边界:** PP14 要求"immediately perceivable — the player should feel the difference within 5 minutes"。但许多进度解锁是"延迟感知"的——例如解锁一个配方但玩家当前缺少合成材料，或解锁一个维度但玩家需要先建造传送门。PP14 承认了传送门案例但未提供系统性解决方案。
  2. **多人游戏中的进度分裂:** 在团队服务器中，只有完成任务的玩家获得进度解锁。如果团队分工（一人做任务、一人采集资源），未做任务的玩家无法感知进度奖励。PP14 的"progression IS the reward"模型假设单人体验。
  3. **零奖励章节与有奖励章节的混合:** 当一个 skyblock pack 同时包含零奖励章节和有奖励章节时（PP14 引用的 Extraordinary Energy Modern 是纯零奖励，但很多包是混合的），玩家在两种合同间切换时可能产生认知混乱。PP14 未讨论混合模式。
  4. **"合并任务"建议的副作用:** PP14 建议对"chain-link with no immediate payoff"的任务进行合并。但如果任务链已经很长（10+ 任务的线性链），合并会使任务过于复杂（描述过长、任务项过多），引入新的可读性问题。
  5. **服务器世界重置:** 在服务器崩溃或重置后，所有"进度解锁"丢失（维度访问、配方解锁等）。与物品奖励不同，进度奖励无法通过重新给予物品来恢复。PP14 未考虑进度丢失的灾难性。

- **与已有规则的冲突:**
  - **条件集合重叠:** R50 (3个安全条件: 替代货币、questbook角色、内在循环) 与 PP14 (2个条件: 可见进度、即时感知) 与 R89 (4个条件: 叙事密度、机械解锁、节奏上限、类型对齐) 三套条件覆盖同一概念但标准不同。一个包可能满足 PP14 的 2 个条件但不满足 R50 的 3 个条件——哪套是权威的？
  - MP65 说"Use optional: true on 5-15% of quests to mark side content"。但 PP14 说"every quest must produce a visible progression effect"。optional 任务可能没有进度效果（纯粹的附加内容），违反 PP14 的"every quest"要求。

- **建议:**
  1. 统一条件集合：建议 R89 的 4 个条件作为权威标准（最完整），PP14 引用 R89 而非独立定义条件。
  2. 补充"延迟感知"处理指导：对于解锁配方/维度但玩家无法立即使用的任务，建议在任务描述中明确说明"完成此任务后需要做什么"来补偿延迟。
  3. 补充多人游戏注意事项，至少标注为已知限制。

---

### AP36 — Reward-Type Roulette

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **主动开发中的迁移期:** AP36 的 fix 说"before authoring a chapter, decide on ONE primary reward delivery mechanism"。但许多包在多个更新版本中逐步迁移奖励类型（如 Enigmatica 谱系）。迁移期间的不一致是不可避免的，AP36 未提供迁移策略（如"先迁移整个章节，不要逐任务迁移"）。
  2. **FTB Quests 版本更新导致的被动不一致:** FTBTeam #509 记录了 FTB Quests 自身的 Claim All 行为变化。当 mod 更新改变了特定奖励类型的行为时，之前一致的章节可能变得不一致。AP36 未讨论这种外部因素导致的不一致。
  3. **自定义奖励类型:** 通过 KubeJS 或其他脚本 mod 实现的自定义奖励类型不在 AP36 的分类体系中（command/loot/item/choice）。自定义奖励的一致性问题未被覆盖。

- **与已有规则的冲突:**
  - R88 的阈值(">2 distinct reward types")与 AP36 的建议("ONE primary mechanism")存在阈值差异。AP36 暗示 1 是目标，R88 在 >2 时才触发警告。这意味着 2 种奖励类型的章节在 R88 看来是可接受的，但在 AP36 看来仍有改进空间。中间地带（2 种类型）的指导模糊。
  - R34 (Reward Type Distribution Report) 是 INFO 级别，AP36/R88 将同一观察提升到 WARNING。严重度提升的理由未明确说明——是玩家投诉证据 (E10 #517) 证明了提升的必要性？如果是，应在 R34 中添加注释说明在何种条件下 INFO 升级为 WARNING。

- **建议:**
  1. 补充迁移策略指导。
  2. 在 AP36 和 R88 之间统一阈值——建议 R88 改为">1 primary type (excluding XP) triggers INFO, >2 triggers WARNING"以覆盖 AP36 关注的中间地带。
  3. 补充自定义奖励类型的适用性说明。

---

### AP37 — Convergence Claustrophobia

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **"仅需新物品"与叙事目的的冲突:** AP37 fix (2) 建议"Design the convergence quest's own task to require only NEW items"。但 capstone 任务的叙事目的通常是"将所有组件汇聚"——如果只需新物品，就失去了" synthesis（综合）"的叙事满足感。AP37 未提供兼顾叙事和便利性的折中方案。
  2. **存储基础设施的影响:** AP37 假设玩家需要"backtrack"获取物品。但如果玩家已经建设了 AE2/Refined Storage 等存储系统，所需物品可能已经在系统中。AP37 未考虑存储基础设施对回溯负担的影响。对于已自动化的玩家，AP37 描述的"forensic exercise"可能根本不存在。
  3. **多玩家分工:** 在团队游戏中，不同玩家可以同时收集不同组件。AP37 描述的"submission marathon"是单人体验——在 3-5 人团队中，47 个依赖的收敛任务可能只需每人负责 10-15 个组件。
  4. **极端收敛（47+ deps）的修复可行性:** AP37 为 20+ deps 建议"preparation quest"，为 10+ deps 建议"comprehensive checklist"。但 CreateBlock farmer 有 47 个依赖——一份 47 项的 checklist 本身就是信息过载。AP37 未设置收敛上限或建议分层收敛（sub-convergence → final convergence）。

- **与已有规则的冲突:**
  - MP66 推荐 `hide_dependency_lines: true` 防止视觉混乱，但 AP37 指出这使回溯问题更严重（玩家看不到哪些前置任务汇入收敛点）。AP37 fix (4) 建议最后 3-5 个任务使用 `hide_dependency_lines: false`。这是一个**直接张力**——视觉清晰度和信息可达性之间的权衡。虽然 AP37 提供了局部解决方案（仅对最后几个任务取消隐藏），但未更新 MP66 以反映这一限制。MP66 应在推荐 hide_dependency_lines 时添加例外说明。

- **建议:**
  1. 补充分层收敛设计模式：对于 30+ deps，建议拆分为 2-3 个 sub-convergence（每个 10-15 deps），再由最终 capstone 汇聚 sub-convergences。
  2. 补充存储/自动化上下文的适用性说明。
  3. 在 MP66 中添加 convergence 任务的 hide_dependency_lines 例外说明。
  4. 设置推荐收敛上限（如 30 deps），超过时强制建议分层设计。

---

### R82 — Backward Design Convergence

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **无终局的包类型:** R82 假设存在一个"final chapter"作为 backward design 的锚点。但沙盒/生活/收藏类包可能没有终局——玩家的"终局"是自选的。R82 的"every chapter should contribute to endgame"在无终局包中无法应用。
  2. **多结局/分支终局:** 具有多条主线的包（如 FTB Skies 2 的三条路径）没有单一的"final chapter"。每个章节可能只贡献于其中一条终局路线。R82 的检查逻辑需要适配多终局结构。

- **与已有规则的冲突:**
  - R46 (Questbook Role Declaration): 如果 questbook role 是 "catalog"，装饰性章节是预期行为，不应被标记为 INFO。R82 的"decorative chapter"标记与 R46 的 role 声明可能产生冲突。建议在 R82 中添加条件："当 questbook_role != 'catalog' 时才触发 decorative chapter 标记。"

- **建议:**
  1. 补充对无终局包类型的适用性说明（标记为 N/A 或降级为纯建议）。
  2. 扩展检查逻辑以支持多终局结构。

---

### R83 — Weak Lock Permeability

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **知识型绕过:** R83 定义了三种锁类型 (hard_lock, weak_lock, no_lock)，但遗漏了"knowledge_lock"——门可以通过知识而非物品绕过（如知道一个秘密配方、发现一个隐藏结构）。这种锁在冒险包中很常见。
  2. **多人经济中的绕过成本:** R83 定义 weak lock 的绕过成本为"5-10x more resources"。但在多人服务器中，绕过物品可以在玩家间交易，成本被分摊或被市场经济稀释。"5-10x"在单人环境中是重负，在繁荣的服务器经济中可能微不足道。
  3. **绕过比正途更便宜:** R83 的 weak lock 三条件之三是"the intended path is more efficient than the bypass"。但如果玩家发现了作者未预料到的绕过路线（利用 mod 交互），绕过可能比正途更高效。R83 未处理这种"意外 weak lock inversion"。

- **与已有规则的冲突:**
  - R4 (Stage Boundary) 在 expert 包中是 ERROR 级别。R83 建议 expert 包使用 hard_lock 或 weak_lock。但如果一个 expert 包的 stage gate 被分类为 weak_lock（有绕过路径），R4 可能将绕过路径上的物品标记为"stage boundary violation"。两个规则的交互需要明确：weak lock 的绕过物品是否豁免 R4 检查？

- **建议:**
  1. 添加 knowledge_lock 作为第四种锁类型。
  2. 补充多人经济环境下绕过成本的适用性说明。
  3. 明确 weak lock 绕过物品与 R4 stage boundary 检查的交互规则。

---

### R84 — Mid-Game Mechan Density

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **极小章节数:** R84 的百分比启发式 (15%/60-70%/15-25%) 假设 10+ 章节。当包只有 3-5 个章节时，一个章节同时占 33%——无法有意义地分类为 early/mid/late。R84 未设置最小章节数阈值。
  2. **非线性进度包:** 对于 hub_fan 或 flexible 模式的包，玩家可以按任意顺序完成章节，"early/mid/late"分类基于依赖深度但可能不反映实际游玩顺序。R84 的分类假设线性进度。
  3. **侧内容章节:** R84 要求将每个章节分类为 early/mid/late，但侧内容/可选章节不属于任何一类。R84 未处理 optional-only 章节（MP68）的分类。

- **与已有规则的冲突:**
  - R55 (Topology-Progression Mode Alignment) 将拓扑类型与进度模式对齐。R84 基于依赖深度分类 early/mid/late。如果一个"mid-game"章节使用 grid_catalog 拓扑（R55 要求 flexible 模式），而 flexible 模式下依赖深度不反映实际游玩顺序，R84 的分类就变得不可靠。两个规则的前提假设不同。

- **建议:**
  1. 添加最小章节数阈值（如 ≥6 章节才适用百分比启发式）。
  2. 补充 optional-only 章节的处理方式（排除出百分比计算或单独分类）。
  3. 在 flexible 模式包中，将依赖深度分类标注为"author-intended order"而非"actual play order"。

---

### R85 — Dual-Direction Reward Principle

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **早期游戏无法 backward-facing:** R85 说"For each quest reward in chapters beyond the first 20% of the quest book"——正确排除了前 20%。但"first 20%"是按章节数还是按依赖深度？如果有 50 个章节但前 10 个章节只有 5% 的总依赖深度，"20% 章节数"和"20% 进度深度"差异很大。
  2. **横向奖励:** R85 分类为 forward/backward/dual/dead_end，但遗漏了"lateral"——奖励解锁平行内容（既非前进也非后退，如解锁一个装饰系统或一个迷你游戏）。横向奖励不是 dead_end，但也不是 forward 或 backward。

- **与已有规则的冲突:**
  - R12 (Reward Value Progression) 期望奖励价值递增。backward-facing 奖励的"价值"可能低于 forward-facing 奖励（优化已有产线 vs 开启新内容），但 R85 认为 dual_direction 是理想状态。R12 和 R85 可能对同一奖励给出不同的评估——R12 说"价值不够高"，R85 说"方向正确"。

- **建议:**
  1. 明确"first 20%"的度量方式（建议按依赖深度而非章节数）。
  2. 添加 lateral 奖励分类，并将其标记为 INFO 而非 WARNING。

---

### R86 — Description-as-Pathway Clarity

- **完备性评级:** COMPLETE
- **遗漏的边界情况:**
  1. **描述长度与清晰度:** R86 检查描述的存在性（有/无），但未检查描述的质量。一个 500 字的描述可能比 50 字的更不清晰。然而，自动化检查描述清晰度在技术上困难，当前仅检查存在性是合理的简化。这不是遗漏而是有意识的范围限制。

- **与已有规则的冲突:** 无。R86 与 R18、R69 的关系是严重度升级（expert 包中从 INFO 提升到 WARNING），逻辑一致。

- **建议:** 未来可考虑补充描述长度上限建议（如 expert 包 gate quest 描述不超过 200 字）。

---

### R87 — Anti-Nerf Progression Respect

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **叙事性临时 debuff:** R87 标记所有"stage transition without debuff mitigation"为 WARNING。但某些包有意设计临时 debuff 作为叙事元素（如"你被传送到了一个陌生维度，需要找到回家的路"）。这种 debuff 不是 nerf 而是故事驱动。R87 未区分"mechanical nerf"和"narrative challenge"。
  2. **可选的高难度区域:** R87 假设维度/生物群系的 debuff 是必经之路。但如果高难度区域是可选的（玩家选择进入），debuff 就是风险-收益权衡的一部分，不需要缓解。R87 未区分必选和可选的 stage transition。

- **与已有规则的冲突:**
  - R16 (Dimension-Explore-Then-Craft) 要求玩家在探索维度后再合成该维度的物品。R87 要求在维度入口处提供 debuff mitigation 物品。如果 mitigation 物品需要从新维度中采集材料合成，R16 和 R87 形成循环依赖——"先探索再合成"vs"先有缓解再探索"。需要明确优先级。

- **建议:**
  1. 添加 optional_transition 条件：仅对必选 transition 触发 WARNING，对可选 transition 降级为 INFO。
  2. 解决 R16 和 R87 的潜在循环依赖——建议 mitigation 物品来自前一个维度的材料，而非新维度。

---

### R88 — Reward-Type Contract Enforcement

- **完备性评级:** GAPS + CONFLICT
- **遗漏的边界情况:**
  1. **XP 作为主货币:** R88 排除 XP ("excluding XP, which is a universal bridge")。但在有技能树 mod（如 Skillable、Reskillable）的包中，XP 是主要进度货币而非补充奖励。R88 的 XP 排除在这些包中会导致误判。
  2. **自定义奖励类型:** KubeJS 或 Task Library 等 mod 添加的自定义奖励类型不在 R88 的检测范围内。
  3. **章节间类型过渡:** R88 检测章节内的一致性，但不检测章节间的一致性。如果 Chapter 1 用 command, Chapter 2 用 loot, Chapter 3 用 item，玩家在每次章节过渡时都会经历类型切换。R88 对此视而不见。
  4. **evolutionary reward types:** 某些包有意随进度变化奖励类型（如早期手动物品奖励→中期自动化 loot crate，反映玩家基础设施的进步）。R88 会将这种有意设计标记为违规。

- **与已有规则的冲突:**
  - **CONFLICT — R34 严重度不一致:** R34 (Reward Type Distribution Report) 对同一观察使用 INFO 级别。R88 对 expert 包使用 WARNING 级别。严重度提升的判定标准未文档化。如果 R34 的 INFO 报告发现问题且包是 expert 类型，是否自动升级为 R88 的 WARNING？还是 R88 独立检查？两条规则的分工不明确。
  - **CONFLICT — PP13 阈值不一致:** PP13 说"exactly one primary reward delivery mechanism"（目标 = 1）。R88 在 ">2 distinct reward types" 时才触发 WARNING（容忍 = 2）。1 primary + 1 例外 = 2 types 在 PP13 看来需要 justification（仅两种例外被允许），但在 R88 看来完全无需标记。中间地带的指导模糊。
  - **CONFLICT — capstone choice reward:** PP13 允许"a single choice reward on a chapter capstone"作为例外。R88 未明确排除 capstone choice reward。如果章节有 1 primary type + 1 capstone choice = 2 types，R88 不标记（≤2）。但如果有 1 primary + 1 capstone choice + 1 tutorial XP = 3 types (excl. XP = 2 types)，仍在 R88 容忍范围内。逻辑上可自洽，但需要明确说明 capstone choice 是否计入 R88 的类型计数。

- **建议:**
  1. 明确 R34 和 R88 的分工：R34 做全量统计（INFO），R88 做阈值判断（WARNING）。建议在 R88 中添加注释："R88 基于 R34 的统计数据，当 R34 报告的类型数超过阈值时触发 R88 WARNING。"
  2. 统一 PP13 和 R88 的阈值：建议 R88 改为 ">1 primary type (excluding XP and single capstone choice) triggers WARNING for expert packs"。
  3. 补充 XP-as-primary-currency 的条件检测。
  4. 补充 evolutionary reward types 的识别和豁免逻辑。

---

### R89 — Progression-as-Reward Viability Conditions

- **完备性评级:** GAPS + CONFLICT
- **遗漏的边界情况:**
  1. **条件 3 的阈值过于保守:** R89 将"5+ zero-reward quests in sequence"标记为 pacing risk。但 PP14 的证据包 GregFactory Sky 有 94 个连续零奖励任务，Extraordinary Energy Modern 有 73 个。这些包的零奖励设计被认为是正确的。5 的阈值对 expert/skyblock 包过于保守——建议按包类型调整阈值（expert: 15+, kitchen-sink: 3+）。
  2. **条件 1 (narrative density) 的例外:** 某些 expert 包使用极简描述（如 GregTech 包的配方导向描述）而非叙事文本。这些包不满足"narrative density"条件但零奖励设计仍然有效——因为配方解锁本身就是足够的反馈。R89 的条件 1 偏向叙事包，对技术 expert 包不公平。
  3. **进度解锁的 bug 风险:** R89 检查条件 2 (mechanical unlock) 的存在性，但不检查解锁是否实际生效。如果一个任务的"reward"是解锁一个配方，但该配方因 mod 版本问题无法合成，R89 会认为条件满足但实际上玩家的 progression-as-reward 体验已崩溃。
  4. **新玩家引导:** R89 不检查玩家是否被告知"this pack uses progression-as-reward"。新玩家可能不知道零奖励是有意的哲学选择而非遗漏。建议在包的首个章节或 questbook 介绍中标注奖励哲学。

- **与已有规则的冲突:**
  - **CONFLICT — 三套条件集合:** R50 (3 conditions) vs PP14 (2 conditions) vs R89 (4 conditions)。R50 在 PACK 级别运作（reward_density < 0.05），R89 在 QUEST 级别运作。PP14 是概念性模式。三者之间的关系应该是：PP14 定义概念，R50 做 pack 级安全检查，R89 做 quest 级详细检查。但当前文档未明确这种层次关系，可能导致同一包在不同规则下得到矛盾评估。
  - **条件 4 (genre alignment) vs R46 (Questbook Role):** R89 条件 4 说"zero-reward does not work in kitchen-sink or adventure packs"。但 R46 允许 questbook_role 为 "catalog" 的包使用零奖励。一个 kitchen-sink pack 的 questbook role 可能是 "catalog"——此时 R89 条件 4 说"不工作"而 R50 条件 2 说"questbook_role = catalog is safe"。直接冲突。

- **建议:**
  1. 明确层次关系：PP14 (概念) → R50 (pack 级检查) → R89 (quest 级检查)。在 R89 开头添加说明。
  2. 按包类型调整条件 3 的阈值。
  3. 修订条件 4 以兼容 R46：将"kitchen-sink packs"改为"kitchen-sink packs with questbook_role != 'catalog'"。
  4. 补充条件 1 的技术包变体："narrative density OR formula-unlock density"。

---

### R90 — Convergence Item Backtracking Safety

- **完备性评级:** GAPS
- **遗漏的边界情况:**
  1. **"3 章节距离"度量的粒度问题:** R90 使用"3 chapters in expert packs or 5 chapters in kitchen-sink packs"作为回溯距离阈值。但章节大小差异巨大——3 个 mega-chapter（100+ quests each）的距离远大于 3 个 mini-chapter（5 quests each）。R90 应考虑章节规模或改用依赖深度距离。
  2. **跨模组合物品:** R90 分析每个物品的"home chapter"。但跨模物品（如一个配方同时需要 mod A 和 mod B 的材料）可能没有单一的 home chapter——它的合成链跨越多个章节。R90 的"farthest home chapter"计算可能被跨模物品扭曲。
  3. **自动化摊销:** R90 不检查玩家是否已经自动化了物品的生产。对于已自动化的物品，"backtracking"只需从存储系统取物，成本接近零。R90 的 WARNING 对这些物品是误报。
  4. **可跳过内容依赖的误报:** R90 检查"convergence item depends on skippable content"。但如果玩家实际完成了该可选内容，WARNING 是误报。R90 无法在生成时知道玩家选择——这本质上是运行时检查而非生成时检查。

- **与已有规则的冲突:**
  - AP37 fix (2) 建议"design convergence tasks to require only NEW items"。R90 检查"home chapter distance"。两个规则的方法不同但目标相同——减少回溯负担。然而它们可能给出矛盾建议：一个来自近距离章节的物品可能仍是"re-submission"（AP37 警告），而一个来自远距离章节的物品可能是"new item"（R90 不警告但 AP37 可能警告）。两条规则需要协调其建议范围。

- **建议:**
  1. 将"3 章节距离"改为"依赖深度距离"或使用加权距离（考虑章节规模）。
  2. 补充跨模物品的处理说明。
  3. 将"depends on skippable content"从 WARNING 降级为 INFO（因为是运行时条件）。

---

## 系统性发现

### 发现 1: 多人游戏/服务器维度系统性遗漏

PP13, PP14, AP37, R83, R87, R90 均未充分考虑多人游戏和服务器环境。这不是个别遗漏而是系统性盲区——当前模式体系主要基于单人体验设计。建议在下一个 cycle 中添加一个统一的"Multiplayer Applicability"注解层，而非逐条修补。

### 发现 2: 零奖励条件的三重重叠

PP14 (2 conditions) + R50 (3 conditions) + R89 (4 conditions) 对同一概念定义了三套不同标准。这是最紧迫需要解决的问题——建议在下一次 SKILL.md 更新中明确层次关系并消除冲突。

### 发现 3: 阈值不一致

PP13/R88 的奖励类型阈值 (1 vs 2)、R89 的连续零奖励阈值 (5 vs 证据中的 73-94)、R84 的百分比启发式 (不适用于 <10 章节) 存在多处阈值与实际证据或实践不匹配的情况。建议系统性审查所有数值阈值的经验基础。

### 发现 4: MP66/AP37 的 hide_dependency_lines 张力

MP66 推荐对收敛任务隐藏依赖线，AP37 指出这加剧了回溯问题。虽然 AP37 fix (4) 提供了局部解决方案，但 MP66 本身未被更新以反映这一限制。这是**文档同步问题**——反模式的修复建议需要回传到被限制的模式中。
