# Reviewer A — 通用性审查 · Cycle 17

> **审查员:** A (通用性质疑)
> **审查对象:** Cycle 17 新增条目 — Cases 49-54, MP72, MP73, R106-R116, AP41
> **审查日期:** 2026-07-17

---

## Cases (topology-coordinates.md)

### Case 49 — No-Flesh-Within-Chest `1` (Tree Branching, Chinese Adventure RPG) — 质疑

**质疑 1: Generality note 中关于"中文包从上到下阅读方向"的断言缺乏跨包验证。**
Generality note 声称"vertical top-to-bottom reading direction (root at top, progression flows downward) is consistent with Chinese text layout conventions and differs from most English-language packs where progression flows left-to-right or bottom-to-top." 此断言有两个问题:

(a) 已有英文包中也存在 top-to-bottom 布局。例如 ATM-10 basic_tools (Case 13) 的 grid_catalog 就是垂直布局。将"垂直布局"归因于"中文阅读习惯"是一种过度归因——这可能是个案作者偏好，而非文化规范。

(b) 本数据集目前只有 1 个中文 tree_branching 案例 (Case 49)。将单一案例的布局方向上升为"中文包惯例"在统计上不成立。需要至少 2-3 个额外的中文 tree_branching 案例来验证这一文化关联。

**建议修改:** 将 generality note 中的"consistent with Chinese text layout conventions"改为"a possible cultural convention observed in 1 Chinese pack; requires validation from additional Chinese-language packs to confirm."

---

### Case 50 — No-Flesh-Within-Chest `boss` (Hub Fan, Boss Catalog) — 通过

Generality note 准确标注了"specific to boss-catalog chapters"，且 hub_fan 用于 catalog 组织是一个功能性发现（hub = 分类标题, leaf = 独立目标），这一模式在不同包类型的 boss 章节中均可成立。90% icon rate 和 70% kill-task rate 是该章节类型的内容驱动结果，而非文化或包类型特异性。

无反例——ATM-10 的 mob hunt 章节虽然不使用完全相同的 hub_fan 结构，但其 catalog 性质一致。

---

### Case 51 — No-Flesh-Within-Chest `tetra` (Tree Branching, Modular Tool) — 质疑

**质疑 1: Generality note 中"validates tree_branching for mod-specific tutorial chapters"的结论过宽。**
该结论仅基于 1 个案例 (No-Flesh-Within-Chest tetra)。虽然 Tetra 工具进阶确实产生了树状分支，但其他 mod-specific 章节未必如此。例如，Create 章节在多个包中（Case 52, AOF-6; ATM-10 create）采用的是 linear_chain 或 diamond_convergence 拓扑，而非 tree_branching。说"tree_branching 是 mod tutorial 章节的自然拓扑"过于泛化。

**质疑 2: hide_dependency_lines: true 被称为"only non-expert chapter"。**
Generality note 声称这是数据集中唯一一个设置 hide_dependency_lines 的非 expert 章节。但 Cycle 15 批量提取的 47 个章节中是否逐一检查了此字段？如果批量数据中未记录此字段，该断言可能是错误的否定。

**建议修改:** (1) 将"validates tree_branching for mod-specific tutorial chapters"改为"validates tree_branching for tool-progression mods where the mod has a clear upgrade trunk (hammer → tool types → forge)." (2) 移除或弱化"only non-expert chapter with hide_dependency_lines"的断言，改为"one of the few observed non-expert chapters with this setting."

---

### Case 52 — AOF-6 `create` (Tree Branching + Extreme Convergence) — 建议修改

**质疑 1: "Tree with capstone" 模式被标注为 TeamAOF 签名——但 generality note 随后建议通用作者使用此模式。**
Generality note 中明确标注"The 'tree with capstone' pattern appears to be a TeamAOF design signature"，但随后写道"Authors should be aware that a 68-dep convergence node requires all prior quests to be completed." 这里存在逻辑矛盾：如果该模式是一个团队的签名风格，向通用作者推荐时应明确标注其为"可选风格"而非"推荐实践"。

**质疑 2: 24-unit width 与 R59 (30-unit warning threshold) 的关系。**
Generality note 提到"24-unit width suggests authors should provide navigational aids"——但 R59 的阈值是 30 units，24 units 在阈值之内。这是否意味着 Cycle 17 在暗示 R59 的阈值应该下调？如果是，应明确说明；如果不是，不应将 24-unit width 作为警示。

**建议修改:** (1) 明确将"tree with capstone"标注为"TeamAOF design signature — optional pattern for kitchen-sink packs, not a universal best practice." (2) 对 24-unit width 的建议添加"still within R59 threshold but approaching the range where navigation aids become beneficial."

---

### Case 53 — AOF-6 `botania` (Large Tree Branching + Capstone) — 质疑

**质疑 1: 32.5-unit width 超出 R59 阈值但 generality note 的态度过于宽容。**
Generality note 写道"non-expert authors will exceed R59 when a mod's content demands it, compensating with icon density rather than layout compression." 这实质上将 R59 阈值定义为"可突破的软限制"，但 R59 的原始定义并未提供"高 icon rate 可以豁免宽度限制"的例外条款。如果这一例外成立，应在 R59 中添加明确的 exemption 条件，而非在一个 Case 的 generality note 中隐含修改规则。

**质疑 2: 该案例与 Case 52 均来自同一个包 (AOF-6) 和同一个团队 (TeamAOF)。**
两个案例不能算作独立验证。MP72 的 generality note 本身已承认这可能是"TeamAOF design signature"，但 Case 53 的 generality note 在讨论 6-sub-region 模式时没有重申这一限制。

**建议修改:** 在 generality note 中明确标注"Both Cases 52 and 53 are from the same pack (AOF-6) by the same team (TeamAOF). The patterns observed may reflect team-specific conventions rather than universal design principles. Cross-pack validation required."

---

### Case 54 — AOF-6 `agriculture` (Grid Catalog, Farming) — 通过

Generality note 的建议（4-6 sub-regions, 4-8 units apart, 1-2 convergence milestones per sub-region）是基于 3 个独立大章节（Steamcreate2 overworld + AOF-6 botania + AOF-6 agriculture）的一致性观察，且与 Miller's working memory 理论吻合。虽然 3 个案例中 2 个来自同一团队，但 Steamcreate2 是独立来源，增加了可信度。

无反例——grid_catalog 的 sub-region 分解在 farming 包中是功能性需求（不同农作物模组需要不同空间区域），而非文化偏好。

---

## Micro-Patterns (micro-patterns.md)

### MP72 — Tree-with-Capstone Convergence — 质疑

**质疑 1: 仅有 2 个案例（均来自 AOF-6 / TeamAOF），且 Player Validation 状态为 [Needs-Validation]——这是否足以作为正式 micro-pattern 收录？**
MP72 的证据基础是所有新 micro-pattern 中最薄弱的：仅有 2 个案例，均来自同一个包的同一个团队，且没有任何玩家反馈验证。文件本身已承认这一点并标注了 [Needs-Validation]，但问题在于：为什么在证据如此薄弱的情况下仍然将其提升为正式编号的 micro-pattern (MP72)，而非暂存为"待验证观察"？

**质疑 2: "capstone has dependencies on ALL prior quests (fan_in = N-1)" 的模式与 AP37 (Convergence Claustrophobia) 存在张力。**
AP37 明确指出 10+ dependencies 的 convergence quest 会造成 bookkeeping 负担。MP72 的 68-dep 和 100-dep capstone 是 AP37 描述的极端情况。虽然 MP72 提到"checkmark task"可以缓解，但这是否意味着 MP72 实际上在推荐一种"可控的 AP37 违规"？如果是，应在 MP72 中明确标注与 AP37 的张力和缓解策略。

**质疑 3: 该模式是否仅适用于 kitchen-sink 包的 mod-completion 场景？**
MP72 的 applicable conditions 写明"Large mod-specific chapters (50+ quests) in non-expert kitchen-sink packs"，但 generality 应进一步质疑：在 expert 包中（如 Monifactory, GregTech-Odyssey），mod 章节通常不需要"你已完成此 mod"的终章信号，因为 expert 包的进度是按电压等级/时代而非按 mod 划分的。在 adventure 包中，章节通常按维度/地区而非 mod 划分。因此 MP72 的实际适用范围可能比标注的更窄——它可能是"kitchen-sink pack mod-chapter completion signal"的同义词。

**建议修改:** (1) 将 MP72 状态降级为 [Candidate] 而非正式编号，直到至少 2 个非 TeamAOF 包提供验证。 (2) 添加与 AP37 的显式张力说明："TENSION with AP37: MP72's N-1 dependency capstone is the extreme case of convergence. The checkmark task type is mandatory to avoid AP37's item-resubmission bookkeeping burden. Authors should NOT use item-submission tasks for MP72 capstones." (3) 在 applicable conditions 中明确排除 expert 包和非 kitchen-sink 包类型。

---

### MP73 — Sub-Region Decomposition for Large Chapters — 建议修改

**质疑 1: "4-6 sub-regions" 的数字基于 Miller's 7±2 理论，但实际观察范围是 4-6（中位数 5），这与 Miller's 7±2 (范围 5-9) 并不完全吻合。**
如果认知限制是 7±2，为什么所有观察到的包都在 4-6 范围内而非 5-9？可能的解释是：(a) 4-6 是更保守的实际操作范围，(b) 样本量太小（3 个章节）不能排除巧合。MP73 将 4-6 作为硬性建议写入 applicable conditions，但应该要么使用 Miller's 理论的完整范围 (5-9)，要么承认 4-6 是基于有限样本的经验观察。

**质疑 2: Indirectly-Validated 的论证逻辑是"4 个 anti-pattern 都指向 MP73 解决的问题"——但这验证的是问题的存在，而非 MP73 的解决方案。**
AP28 说"mega-chapter without structural compensation is bad"——这验证了"需要 structural compensation"。但 MP73 提出的是特定的解决方案（4-6 sub-regions with specific x-y separation）。AP28 的存在不能自动验证 MP73 的特定参数。Craftoria 的 Create chapter 使用了 8 colored toolbox compartments（8 个 sub-regions），超出了 MP73 的 4-6 范围，且被认为是正面案例（AP28 引用）。

**建议修改:** (1) 将 sub-region 数量建议从"4-6"扩展为"4-8"以涵盖 Craftoria Create 的 8-region 案例。 (2) 将验证状态从 [Indirectly-Validated] 改为 [Partially-Validated — problem confirmed, specific parameters need calibration].

---

## Progression Rules (progression-rules.md)

### R106 — Dimensional Progression Naturalism — 质疑

**质疑 1: 该规则的核心来源是 MC百科 thread-21004 和 SevTech Ages——一个中文社区文章和一个特定包。**
"Dimension transitions should feel earned" 是一个合理的设计理想，但 R106 的 implementation check 将"at least 3 same-dimension prerequisites"作为硬性阈值。这个"3"从哪来？thread-21004 并未指定具体数字。如果某个包的维度门控只需要 2 个前置任务（例如"击败 Wither + 获得 Nether Star"），但这两个任务本身就需要大量下界探索，那么 2 个前置可能已经足够"自然"。

**质疑 2: 该规则对非维度包（single-dimension packs, skyblock packs）完全不适用。**
R106 的 applicable when 已标注"2+ dimension-adding mods"，但 skyblock 包（如 SkyFactory, StoneBlock）可能有 2+ dimensions 但维度不是进度主轴。Generality note 应明确排除 skyblock 和 single-dimension 包。

**建议修改:** (1) 将"3 same-dimension prerequisites"改为"a meaningful number of same-dimension prerequisites (recommended >= 3, but 2 may suffice if each prerequisite requires substantial engagement)." (2) 添加"Does not apply to skyblock packs where dimension transitions are trivial (portal-only gating) or single-dimension packs."

---

### R107 — Olive-Shaped Equipment Distribution — 质疑

**质疑 1: "橄榄形"分布仅适用于有明确装备分层的包。**
R107 来源于 MC百科 thread-21004 的冒险/RPG 包设计文章。在冒险包中，装备分层（铁 → 钻石 → 下界合金 → mod 装备）是核心体验。但在以下包类型中，"装备分层"本身就不是核心机制:
- **Farming/lifestyle 包**（如 Life-in-the-Village）：没有"装备"概念，工具只是效率差异。
- **Create-focused 包**（如 Create-chronicles）：进度按机器解锁而非装备升级。
- **Pure magic 包**：法术系统可能不遵循"两头少中间多"的分布。

**质疑 2: Severity 为 INFO 但 implementation check 的逻辑可能导致大量假阳性。**
许多非冒险包的装备分布天然不是橄榄形——例如 ATM-10 (kitchen-sink) 可能在每个 tier 都提供大量装备选项，因为每个 mod 都引入自己的装备。将这些标记为 INFO 可能产生噪音。

**建议修改:** (1) 在 applicable when 中添加"Primarily applicable to adventure/RPG and expert packs with clear equipment tiers. May produce false positives in kitchen-sink and farming packs." (2) 考虑将 implementation check 改为比较"distinct equipment options per tier"而非"total equipment items per tier"，以区分 meaningful variety 和 mod-stacking bloat。

---

### R108 — Gear-to-Mob Cross-Dimension Scaling — 建议修改

**质疑 1: DPS/HP 比值的阈值 (3× 和 0.3×) 缺乏实证校准。**
R108 设定"source best DPS > 3x target basic mob HP"为 trivialize 阈值，"source best DPS < 0.3x target basic mob HP"为 difficulty spike 阈值。这些阈值是推测性的——没有从实际包的战斗数据中校准。不同 mod 的战斗系统差异巨大：Tetra 的 DPS 计算方式与 Mekanism 完全不同，Mekanism 的 MekaSuit 可以吸收几乎所有伤害（使 0.3x 阈值无意义）。

**质疑 2: 该规则假设"basic mob"有统一的 HP/damage 定义。**
不同维度 mod 的"basic mob"差异很大：下界有 piglin (8 HP) 和 wither skeleton (20 HP)，这两者相差 2.5 倍。用哪个作为"basic mob"基准？

**建议修改:** (1) 标注 3x/0.3x 阈值为"initial heuristic, requires calibration from combat data across 3+ packs with dimension transitions." (2) 建议以"dimension's first 3-5 hostile mob types, median HP"作为 basic mob 基准。

---

### R109 — Forced Anti-Skip Material Binding — 通过

该规则的通用性成立：world-generation manipulation 防止 cross-tier 是一个跨包类型的通用原则。Expert 包（GregTech 系列）、semi-gated 包（SevTech Ages）和 adventure 包（维度限定资源）都需要此规则。

Applicable when 已正确限定为"Expert/semi-gated packs with dimension-gated resources"，排除了不需要此规则的 kitchen-sink 和 farming 包。

无反例——所有已知的维度限定资源包都使用了某种形式的 world-generation 限制。

---

### R110 — Mid-Game Density Priority — 质疑

**质疑 1: "Mid-game should occupy the majority of playtime"是一个通用理想，但 implementation check 的百分比阈值（40%/30%）缺乏校准。**
R110 设定"mid-game quest count < 40% of total"为 under-dense 阈值。但不同包类型的理想分布差异很大：
- **Tutorial-heavy 包**（FTB University）：early game 可能占 30-40% 因为需要教玩家大量 mod 机制。
- **Endgame-focused expert 包**（GregTech New Horizons）：late game 可能占 30-40% 因为最终 tier 的合成链极长。
- **Adventure 包**：可能没有明确的"mid-game"概念——进度是按维度/区域而非早/中/晚期划分。

**质疑 2: 该规则与 R111 (Anti-Forced-Lifespan) 存在内在张力（已在 Tension 8 中记录），但 R110 的 implementation check 并未提供区分"合理的 mid-game density"和"forced lifespan"的方法。**

**建议修改:** 在 implementation check 中添加包类型上下文："For tutorial-heavy packs, early-game > 30% may be intentional. For expert packs with nested crafting, late-game > 30% may be intentional. Flag only when the distribution deviates significantly from the pack's genre norms."

---

### R111 — Anti-Forced-Lifespan Extension — 质疑

**质疑 1: "3+ consecutive quests requiring same task type with increasing quantities"作为 forced lifespan 的信号——但这在 tech 包中是标准进度模式。**
例如 Mekanism 包的 ore processing 链：1x ore → 2x clump → 4x shard → 8x crystal。每个步骤都是"same task type (processing) with increasing quantities"，但这不是 forced lifespan——这是 Mekanism 的核心玩法循环。类似地，Create 包的 processing 链天然是"same task type, increasing quantity"。

**质疑 2: 该规则的来源是中文社区文章对"强行延长游戏时间"的批评，但这篇文章讨论的是高难度 long-lifespan 包（1000+ hours）。将这个标准应用到"100+ hour estimated playtime"的包可能导致过度检测。**

**建议修改:** (1) 在 implementation check 的"quantity escalation"检测中添加豁免："If the escalating-quantity quests introduce a NEW processing mechanic at each layer (e.g., crush → smelt → dissolve → crystallize), this is NOT forced lifespan — it is a natural tech-progression chain. Flag only when the same EXACT operation is repeated at increasing scale." (2) 将 applicable when 的阈值从"100+ hour"提高到"500+ hour"或"expert packs only"。

---

### R112 — Vanilla Enhancement Layering — 质疑

**质疑 1: "每个 mod introduction quest 前应存在 vanilla equivalent"——这对许多 mod 不适用。**
R112 建议检查"whether a vanilla equivalent task exists earlier in the dependency chain"。但以下常见 mod 没有 vanilla equivalent:
- **Applied Energistics / Refined Storage**：没有 vanilla 存储系统能与之对应。
- **FTB Quests**：进度系统本身不是 vanilla 概念。
- **Waystones / Xaero's Minimap**：QoL mod 没有 vanilla 对应。
- **Botania**：虽然建立在 vanilla 花草之上，但其魔法系统远超 vanilla 范畴。

Implementation check 已承认"some mods have no vanilla equivalent"，但并未提供区分"有 vanilla equivalent 的 mod"和"无 vanilla equivalent 的 mod"的方法。如果不加区分地应用，将产生大量 INFO 噪音。

**质疑 2: SevTech Ages 和 FTB University 作为正面案例——但这两个包的设计哲学截然不同。**
SevTech Ages 使用 vanilla advancement 作为 gate，逐层揭示 mod。FTB University 使用"school system"教学。两者都"build on vanilla knowledge"，但实现方式完全不同。将它们归入同一规则模糊了实现差异。

**建议修改:** (1) 添加一个 vanilla-equivalent 的分类标准："Only flag if the mod REPLACES a vanilla mechanic (e.g., modded furnace replacing vanilla furnace, modded sword replacing vanilla sword). Mods that ADD new mechanics (storage systems, magic, quest books) do not require a vanilla foundation." (2) 考虑将 R112 拆分为两个子规则：R112a (replacement mods need vanilla foundation) 和 R112b (addition mods need introductory tutorial quest)。

---

### R113 — Multi-Dimensional State Synchronization — 质疑

**质疑 1: "stage transition 应影响至少 2 个 game systems"——但这个阈值对 non-expert 包不现实。**
R113 的 applicable when 标注"Expert/semi-gated packs using Game Stages"。但即使在这个范围内，并非所有 stage transition 都需要影响 2+ systems。一个小的 stage 升级（例如解锁一种新的 ore）可能只需要 1 个 system change (ore generation)，而不需要同时改变 mobs、recipes、dimensions 等。要求每次 transition 都影响 2+ systems 可能导致作者为了"满足规则"而添加无意义的变化。

**质疑 2: SevTech Ages 是唯一的正面案例。**
虽然规则引用了 CSDN 文章和 MC百科 thread-21004，但实际实现多系统同步 stage transition 的包只有 SevTech Ages。其他使用 Game Stages 的包（如 Enigmatica 系列）的 stage transition 通常只影响 recipes 和 items（1-2 systems），并未达到 R113 描述的理想状态。

**建议修改:** (1) 将"fewer than 2 systems"的阈值改为"a single trivial change (e.g., only one recipe unlock with no world change)"。 (2) 添加："For minor stage transitions (unlocking a single mod or material), 1-2 affected systems is acceptable. Major era transitions (new dimension, new tier) should affect 3+ systems."

---

### R114 — Quest-to-Stage Reward Bridge — 通过

该规则是 Game Stages 生态系统的操作基础设施。任何使用 Game Stages 的包都必须通过某种方式将 quest completion 与 stage granting 连接——R114 描述的 bridge pattern 是唯一可行的实现方式（MC百科 post/2163 和 post/1938 均确认）。

没有反例——不使用 quest-to-stage bridge 的 Game Stages 包将完全无法运作。

Severity 分级 (ERROR for expert, WARNING for semi-gated) 合理。

---

### R115 — Container-Level Recipe Locking — 通过

该规则针对特定技术场景（expert packs + Recipe Stages + automation mods），applicable when 已精确限定。setContainerStages 是 Recipe Stages mod 文档中明确记载的功能，其必要性来自 automation mod 的 bypass 风险——这是一个真实的技术问题。

无反例——expert packs 使用 automation mods 时，如果不配置 container locking，必然存在 bypass 风险。

---

### R116 — Advancement-As-Progression-Gate Pattern — 质疑

**质疑 1: 该规则实质上是 SevTech Ages 的个案描述，而非跨包通用规则。**
R116 的所有来源和实现细节都指向 SevTech Ages。虽然它提到了 MC百科 class/3668 (8 packs using advancement book)，但这 8 个包是否使用了 SevTech 的"multi-dimensional state synchronization"模式？如果它们只是用 advancement book 作为 UI 展示而非作为 progression gate，则不能算作 R116 的验证。

**质疑 2: R116 与 R113 高度重叠。**
R116 的 implementation check 要求的 4 个元素（custom advancement, ore visibility, recipe visibility, mob spawn）中，3 个与 R113 的 "systems affected" 列表重叠。R116 是否是 R113 的一个"implementation variant"而非独立规则？

**建议修改:** (1) 将 R116 降级为 R113 的 implementation variant note，或合并为"R113 with advancement-based trigger"。 (2) 如果保持独立，需要至少 2 个非 SevTech 包使用相同模式的验证。

---

## Anti-Patterns (anti-patterns.md)

### AP41 — Flat Presentation Hierarchy — 建议修改

**质疑 1: Craftoria #231 Powah chapter 是核心案例——但这是一个 ~40 quest 的章节。**
AP41 的 applicable range 标注为"30-80 quests"。Craftoria Powah 章节在低端（~40 quests）。在高端（80 quests），许多包使用 hub_fan 或 tree_branching 拓扑来自然创建层次结构——这些拓扑本身防止了 flat hierarchy。因此 AP41 的实际上限可能不是 80 quests 而是 50-60 quests。超过这个规模，大多数作者已经采用了结构性拓扑。

**质疑 2: "throws everything at you" 的问题是否真的是 presentation 问题，还是 reward pacing 问题？**
Craftoria #231 的完整投诉是"I feel like the quests in the Powah tab kinda just throws everything at you"以及"you go through 3 tiers of reactors with no relevant quest rewards"。后者是一个 reward pacing 问题（AP38 Convergence Over-Reward 的变体），而非 presentation hierarchy 问题。AP41 是否将两个不同的问题（visual flatness + reward drought）合并为一个 anti-pattern？

**质疑 3: Fix (2) 建议"hide_until_deps_visible on at least the second half"——但这可能过度隐藏。**
在 30-quest 章节中对 15+ quests 使用 hide_until_deps_visible 可能导致另一个问题：玩家无法提前规划（看不到后续需要什么资源）。PP16 (Guided Non-Linearity) 描述的理想是"guided but not linear"——过度隐藏破坏了"guided"的"non-linear"部分。

**建议修改:** (1) 将 applicable range 从"30-80 quests"收窄为"25-60 quests"。 (2) 添加 cross-reference 说明 AP41 与 reward pacing 问题的区别："Note: if the player complaint is specifically about reward pacing (no relevant rewards for multiple tiers), classify as AP38 variant rather than AP41." (3) Fix (2) 修改为"hide_until_deps_visible on quests beyond the first major milestone (typically 30-40% into the chapter), not a flat 50%."

---

## 审查统计

| 类别 | 通过 | 质疑 | 建议修改 |
|------|------|------|----------|
| Cases 49-54 | 2 (Case 50, Case 54) | 3 (Case 49, Case 51, Case 53) | 1 (Case 52) |
| Micro-Patterns MP72-73 | 0 | 1 (MP72) | 1 (MP73) |
| Progression Rules R106-R116 | 3 (R109, R114, R115) | 7 (R106, R107, R108, R110, R111, R112, R113) | 0 |
| Anti-Patterns AP41 | 0 | 0 | 1 (AP41) |
| **合计** | **5** | **11** | **3** |

**审查通过数: 5**
**质疑数: 11**
**建议修改数: 3**

---

## 总结

Cycle 17 的核心通用性问题集中在三个方面:

1. **TeamAOF 集中偏差 (Cases 52-53, MP72):** 3 个案例和 1 个 micro-pattern 均来自同一个团队 (TeamAOF) 的同一个包 (AOF-6)。虽然数据质量高，但不能作为跨包通用性的证据。MP72 (Tree-with-Capstone) 尤其需要关注——它是 [Needs-Validation] 状态，证据来自单一来源，且与 AP37 (Convergence Claustrophobia) 存在未记录的张力。

2. **中文社区来源过度泛化 (R106-R112):** R106-R116 被标记为"International Author Design Philosophy"，但 R106-R111 的主要来源是 MC百科 thread-21004 和 post/4382——两篇中文社区文章。将特定中文社区作者的设计哲学上升为"international design philosophy"是一种过度泛化。这些原则可能在冒险/RPG 包中成立，但在 kitchen-sink、farming、Create-focused 等包类型中可能不适用或需要显著修改。

3. **Implementation check 阈值缺乏校准 (R106, R108, R110, R111):** 多个新规则的 implementation check 包含具体数值阈值（3 prerequisites, 3x DPS ratio, 40% mid-game, 100+ hours），但这些阈值均未经过跨包数据校准。建议将所有未校准阈值标注为"initial heuristic"并在后续 cycle 中收集校准数据。
