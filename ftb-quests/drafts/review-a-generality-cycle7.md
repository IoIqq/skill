# 审查员 A — 通用性审查报告 (Cycle 7)

> **审查范围:** micro-patterns.archive.md, anti-patterns.archive.md, progression-rules.archive.md, 及 6 个 mod-*.md 模块 + module-index.md
> **审查角度:** 每个模式/规则是否真正「通用」，还是仅基于有限样本的过度泛化

---

## 需要降低通用性声明的条目

### 1. MP32 — min_tasks Modifier（partial completion threshold）

**现状:** 标注为 `create, kitchen-sink`，但实际仅有 Create: Astral 一个数据源（single-source）。文档自身已承认与 MP9 功能重叠。

**问题:** `kitchen-sink` 的包类型标注缺乏数据支撑——文档明确指出「15 个包中无 kitchen-sink 包使用 `min_tasks` 的证据」。此模式本质上是一个 FTB Quests 配置字段（`min_tasks`）的用法说明，而非独立的设计模式。

**建议:** 降级为 MP9 的 task-level 变体注释，不再作为独立 pattern 列出。或删除 `kitchen-sink` 包类型标注。

---

### 2. MP35 — Dual-Task Automation Verification

**现状:** 标注为 `create` 包类型，但仅有 Cabricality 一个数据源。

**问题:** 此模式是 Cabricality 的特定设计理念（荣誉制度确认自动化），不是 Create 包的通用做法。Create: Delight（2,295 quests）、Mechanomania（395 quests）、Create: Astral（~650 quests）均不使用此模式。将单一包的荣誉制度设计泛化为整个 `create` 类型的模式，证据不足。

**建议:** 明确标注为 single-source case study，而非通用 create 模式。

---

### 3. MP37 — Progress Catalog Chapter

**现状:** 标注为 `expert`，但仅有 GregTech-Odyssey 一个数据源。

**问题:** Monifactory（expert 包，248 quests）、Enigmatica 9E（expert，22 chapters）、Cabricality（expert，14 chapters）均不使用专门的 progress catalog chapter。这是 GT-O 的特定 UX 选择，不是 expert 包的通用做法。

**建议:** 降级为 GT-O case study，或至少标注为 single-source。

---

### 4. MP38 — Reward Perception Split

**现状:** 标注为 `kitchen-sink`，验证来源仅为 ATM-10 Discussion #3539 + cesspit.net 理论。

**问题:** 只有一个 GitHub Discussion 的实证数据。cesspit.net 提供理论支撑但不提供第二个 kitchen-sink 包的玩家分歧证据。Craftoria（另一个 kitchen-sink）的 issue tracker 中未见类似的 reward generosity 争论——Craftoria 的问题集中在 gating 和 reward desert，而非「给太多」。

**建议:** 文档已自行标注「验证置信度: 中等」，但仍以正式 pattern 身份列入。建议降级为「待验证假设」，等待第二个 kitchen-sink 包的玩家分歧数据。

---

### 5. MP33 — Advancement Gate

**现状:** 标注为 `all`（所有包类型），但实际仅 Enigmatica 10 有 3 个案例。

**问题:** `all` 标注暗示这是一个跨包类型的通用模式，但证据仅来自一个 expert 包。虽然 `advancement` task type 是 FTB Quests 原生功能，但「使用 advancement task 作为进度检查点」这一设计决策并非所有包类型都采用。ATM-10（4,601 quests）、Create: Delight（2,295 quests）、Monifactory（248 quests）的审计数据中均未出现 advancement task 的系统性使用。

**建议:** 包类型从 `all` 降级为 `expert, kitchen-sink`（待验证），confidence 从 Medium 降为 Low。

---

### 6. MP4 — Escalation Ladder

**现状:** 标注为 `all`（在 Scope Annotation Table 中），但文档自身标注 † ATM Signature。

**问题:** 87 个 kill task 的 bounty board 仅在 ATM 系列中观察到。「纯 tech/expert 包通常不使用此模式，Create 系列无 escalation ladder 证据」——这直接与 `all` 标注矛盾。此模式的前提是包内有「可重复的 grind activity」，大多数 expert 和 Create 包不满足此条件。

**建议:** 包类型从 `all` 修正为 `kitchen-sink, rpg`。mod-atm-signature.md 已做此修正，但 micro-patterns.archive.md 的 Scope Annotation Table 仍标注 `all`。

---

### 7. MP36 — Currency-as-Reward

**现状:** 标注为 `expert, hardcore, rpg`，但仅有 2 个数据源（GregTech-Odyssey + NFwC）。

**问题:** 虽然两个包独立使用 currency reward，但它们的实现高度依赖特定的 mod（`gtocore:copper_coin`、`lightmanscurrency:coin_*`）。这不是一个设计模式，而是特定 mod 提供的经济系统的用法说明。此外，标注的 `hardcore` 和 `rpg` 包类型没有任何数据支撑——NFwC 归类为 hardcore/combat，GT-O 归类为 expert，没有 RPG 包使用 currency reward 的证据。

**建议:** 包类型修正为 `expert`（GT-O）和 `hardcore/combat`（NFwC），删除无证据的 `rpg`。明确标注为「特定 mod 经济系统的集成方式」而非通用设计模式。

---

### 8. AP17 — XP-Level Reward Relativity

**现状:** 标注为 `all`，但仅有 Craftoria #289 一个实证来源。文档包含一段「Generalizability note」试图论证通用性。

**问题:** Generalizability note 的论证——「根因是 Minecraft 原版的指数级 XP 曲线——这是游戏机制层面的通用问题」——在逻辑上成立，但忽略了关键事实：大多数包根本不使用 `xp_levels` reward type。ATM-10（6,915 rewards）绝大多数使用 `xp`（raw），不使用 `xp_levels`。Monifactory 不使用 XP reward 作为核心经济。Create: Delight 和 Mechanomania 的 reward 密度极低。此 AP 仅在「大量使用 xp_levels reward 的包」中才有实际意义，而这是一种特定于某些包的设计选择。

**建议:** 适用条件从「all」精确化为「使用 `xp_levels` reward type 的包」。在 Quick Reference 表中添加前置条件列。

---

### 9. R41 — Early-Game Flexible Mode

**现状:** 标注为 `all`，来源仅为 Craftoria #607。

**问题:** 此规则假设「前 N 个 chapter 应使用 flexible mode」是通用最佳实践，但这与大量包的设计意图冲突。ATM9-Sky 的 tutorial 使用 `default`（locked）mode——这是有意为之，因为 skyblock tutorial 必须强制顺序。Expert 包通常全包使用 `default`/`linear`。R41 的建议仅适用于「整体使用 linear 但早期过于严格」的包，而非所有包。

**建议:** 适用条件修正为「整体 progression_mode 为 linear 且新手体验被报告为过于严格的包」。标注为 single-source。

---

### 10. R40 — Effort Preview in Description

**现状:** 标注为 `expert, kitchen-sink`，来源为 GregTech-Odyssey #1602 + Monifactory #2359。

**问题:** 两个数据源都是 expert GregTech 包。此规则的核心场景是「voltage tier 转换时的 effort spike」——这是 GregTech 特有的 progression 结构。对于不使用 tier-based progression 的包（RPG、skyblock、Create），「effort preview」的需求和形式完全不同。

**建议:** 包类型修正为 `expert`（删除 `kitchen-sink`）。明确标注为 GregTech-style tier transition 的特定需求。

---

### 11. MP17 — Hub Concentration

**现状:** 标注为 `create, kitchen-sink`，confidence 为「Medium (Create: Delight primary)」。

**问题:** 核心证据来自 Create: Delight 的 Mouse_Chef chapter（304 cells + 12 hubs）。ATM-10（kitchen-sink）不使用 hub concentration 模式——它的 reward 分布更均匀（XP drip philosophy）。将 Create: Delight 的特定 catalog 设计泛化为 `kitchen-sink` 类型的通用模式，证据不足。

**建议:** 包类型修正为 `create`（删除 `kitchen-sink`），或标注为「Create catalog 专属」。

---

### 12. MP20 — Shape-as-Tier Signal

**现状:** mod-atm-signature.md 已正确标注为 ATM Signature，但 mod-dependency-graph.md 的 R35（Shape Semantics Consistency）仍假设 shape 具有跨包语义角色。

**问题:** R35 的检测逻辑假设「shapes used as tier markers should be used consistently across chapters」，但 25-pack dataset 显示大多数包（Enigmatica 10、Craftoria、Cabricality）使用 ZERO 或近零的 explicit shape。对于这些包，R35 的检测完全无意义。虽然文档包含了「all-default fallback」逻辑，但这实际上是把「不使用 shape 语义」也变成了一种需要检测的「模式」——过度工程化。

**建议:** R35 应仅在检测到包有 >=3 种 explicit shape 时才激活。对于 all-default 包，跳过检测而非执行 fallback 分析。

---

## 需要更精确适用条件的条目

### 1. MP16 — XP Drip

**现有条件:** `kitchen-sink`（已从 `kitchen-sink, expert` 修正）。

**问题:** 即使修正后的 `kitchen-sink` 也不够精确。ATM 系列的 XP drip（1.5-1.7 rewards/quest）与 All-of-Fabric-3（0.66 rewards/quest，random-dominant）和 Craftoria（xp_levels-heavy）的 reward 经济完全不同。XP drip 不是 kitchen-sink 的通用模式，而是 ATM-style generous kitchen-sink 的特定模式。

**建议条件:** `kitchen-sink (ATM-style generous reward philosophy)` — 明确排除使用 sparse reward 或 random-dominant 经济的 kitchen-sink 包。

---

### 2. MP29 — Command Reward

**现有条件:** `expert, story, kitchen-sink (legacy MC ≤1.16.5)`。

**问题:** 文档的 Cycle 6 Phase 3 数据揭示了一个关键的版本断裂：MC 1.21+ (FTB Quests 26.x) 的原生 `type: "loot"` 完全替代了 command-as-loot workaround。但文档仍以 MP29 作为正式 pattern 呈现，未在主声明中区分版本。对于 MC 1.21+ 的新包，command reward 的使用场景大幅缩窄（仅剩 gamestage routing 和特殊 effect）。

**建议条件:** 增加 MC 版本维度：`expert (MC ≤1.20, gamestage routing)`, `kitchen-sink (MC ≤1.16.5, loot delivery workaround)`, `all (MC ≤1.20, special effects only)`。对于 MC 1.21+，command reward 应标注为「不推荐，优先使用 type: loot/random」。

---

### 3. AP13 — Premature Item Submission

**现有条件:** 标注为 `all`，但仅有 FTB StoneBlock 4 #11285 一个案例。

**问题:** 此 AP 描述的是 FTB Quests 的一个状态机行为（允许 locked quest 接收 item submission），但仅有一个 skyblock 包的 energy cell quest 报告了此问题。其他 22+ 个被审计的包均未报告此问题，暗示这可能是特定配置（energy/fluid task 的累积型 tracking）而非通用风险。

**建议条件:** 精确化为「使用 energy/fluid 累积型 task 且 task item 在 quest unlock 前可自然获得的配置」。对于纯 item task（大多数 quest），此 AP 不适用。

---

### 4. R36 — Dependency Root Isolation

**现有条件:** 标注为 `all`，来源为 Monifactory CONTRIBUTING.md。

**问题:** 此规则假设「每个 quest 应有至少一个 dependency，除非在 designated root chapter」。但 Create: Delight 的 Mouse_Chef chapter 有 258 个 independent island quests——这是 MP10 (Independent Island) 的设计意图，不是错误。R36 会对 catalog-style chapter 产生大量 false positive。

**建议条件:** 增加例外：「catalog 或 collection 类型的 chapter（>50% quests 为 independent island）排除在此规则之外」。

---

### 5. R39 — Guide Quest Deduplication

**现有条件:** 标注为 `expert, kitchen-sink`，来源为 Monifactory CONTRIBUTING.md。

**问题:** 「guide quest 不应出现在多个 chapter」的规则假设包有一个集中的 tutorial chapter——这是 expert 包的做法。Kitchen-sink 包通常将每个 mod 的教程放在该 mod 的专属 chapter 中，不存在「跨 chapter guide 重复」的问题。R39 对 kitchen-sink 包的适用性存疑。

**建议条件:** 从 `expert, kitchen-sink` 修正为 `expert`。

---

### 6. R18 — Description Coverage

**现有条件:** 标注为 `all`，排除条件为 catalog cell（`rsquare`/`circle` shape, size <= 2.0, catalog chapter, single task）。

**问题:** 排除条件过于具体——它硬编码了 Create: Delight 的 catalog cell 特征（`rsquare` shape）。其他使用 catalog 设计的包可能使用不同的 shape（如 Cabricality 全部使用默认 shape）。排除条件应基于 chapter 类型（catalog/collection）而非 shape+size 组合。

**建议条件:** 排除条件改为「catalog chapter（chapter 中 >70% quests 为 independent island + single task）中的 quest」，不依赖 shape/size 特征。

---

### 7. R9 — Dependency Depth Reasonableness

**现有条件:** `MAX_DEPTH = {"kitchen-sink": 8, "expert": 20, "skyblock": 20, "rpg": 12, "create": 10}`。

**问题:** 这些阈值是从有限数据集中归纳的硬编码值。ATM9-Sky 的 depth 18 在 `skyblock: 20` 以内，但 Create Skylands（也是 skyblock）使用线性 progression 且 depth 更低。`rpg: 12` 仅基于 Prominence II 和 Finality Genesis 两个包，样本不足以建立通用阈值。

**建议条件:** 阈值应标注为「从当前数据集归纳的参考值，非硬性限制」，并鼓励用户在 Step 2 interview 中提供自己的 depth 期望。

---

### 8. AP20 — Quest Tab Overwhelm

**现有条件:** `kitchen-sink, create`，来源为 Craftoria #231。

**问题:** 仅有 Craftoria 的 Powah chapter 一个案例。「info-dump chapter」的问题本质上是 gating (AP4) + presentation 的复合问题，而非独立的 anti-pattern。Create: Delight（2,295 quests）和 Mechanomania（395 quests）的 catalog 设计也可能被误判为「overwhelm」，但它们的 flat catalog 是有意为之（MP10 Independent Island）。

**建议条件:** 增加前提条件：「chapter 同时存在 AP4（wrong gating）和 reward desert（AP18）时，AP20 的 overwhelm 效应被放大。独立的 flat catalog（MP10）不触发 AP20。」

---

## 重叠/矛盾的模式

### 1. MP32 vs MP9 — 功能重叠（task-level vs dependency-level choice）

**重叠:** MP32（`min_tasks` modifier）和 MP9（Diamond + `one_completed`）实现相同的设计意图——「从多个选项中选择一个」。文档自身承认此重叠：「MP32 functionally overlaps MP9 at task level」。

**建议:** 合并为 MP9，在 MP9 文档中增加「task-level 变体：使用 `min_tasks` 字段」的实现说明。

---

### 2. MP24/MP25/MP26 vs R 规则 — 桥梁概念已被规则替代

**重叠:** MP24（Tier-Reachability Check）→ R1/R2，MP25（Dependency-Order Check）→ R14，MP26（Reward-Continuity Check）→ R10。文档标注「→ See R1/R2」等，但仍在 Scope Annotation Table 中作为独立 pattern 列出。

**建议:** 从 Scope Annotation Table 中删除 MP24/MP25/MP26 的独立条目，在对应 R 规则中增加一行注释「前身为 MP24/25/26 桥梁概念」。

---

### 3. PP5 vs AP5 — 同一问题的双重视角

**重叠:** PP5（Context Void, player-perspective）和 AP5（Empty Quest Description, author-perspective）描述同一问题：quest 缺少描述导致玩家无法理解。PP5 在 mod-teaching-pacing.md 中有独立的「expert pack amplification」段落；AP5 在同一模块中也有「expert pack amplification」段落。两处内容高度重复。

**建议:** 保留 AP5 作为主条目（包含检测规则和修复方案），PP5 作为 AP5 的「player-experience 影响」段落内联到 AP5 中，而非独立 pattern。

---

### 4. PP6 vs AP6 — Wrong Tool Reward vs Dead-End Reward

**重叠:** PP6（Wrong Tool Reward）是 AP6（Dead-End Reward）的特定变体——reward 是工具但来自错误的 mod。文档自身承认此关系。但 PP6 有独立的「Config implication」段落，与 AP6 的修复建议重复。

**建议:** PP6 降级为 AP6 的一个 variant 段落（已有「Variant — Mod-Unification Trap (PP7)」的先例），不再作为独立 player-perspective pattern。

---

### 5. PP7 vs AP6 + AP1 — 复合问题被拆为独立 pattern

**重叠:** PP7（Mod-Unification Trap）文档自身承认「PP7 is a player-experience variant of AP6 and AP1」。它同时是 AP6（reward 是 wrong variant）和 AP1（description 提到 wrong variant）的复合体现。

**建议:** 保留 PP7 作为 AP6 和 AP1 的「mod-unification variant」交叉引用，但不作为独立的 top-level pattern。这已在文档中部分实现（AP6 下有「Variant — Mod-Unification Trap (PP7)」），但 PP7 仍独立存在于 micro-patterns.md 的 Player-Perspective 部分。

---

### 6. AP19 vs AP4 — Optional-but-Mandatory vs Wrong Gating

**重叠:** AP19（Optional-but-Mandatory Mislabel）是 AP4（Wrong Gating）的 metadata 变体。文档承认：「This is a metadata variant of AP4」。AP4 的 root cause 是 `dependency_requirement` 设置错误；AP19 的 root cause 是 `optional` flag 设置错误。两者的修复方案（R7 Optional-Gate-Mandatory check）完全相同。

**建议:** AP19 合并为 AP4 的一个 sub-variant，共享 R7 检测规则。

---

### 7. R31 vs AP17 — 规则与反面模式的冗余

**重叠:** R31（XP-Level Reward Relativity）是 AP17 的检测规则版本。两者的描述、根因、修复方案完全相同。R31 在 mod-reward-design.md 中有独立条目；AP17 在同一文件中也有独立条目。

**建议:** 保留 AP17 作为 anti-pattern 定义，R31 作为其检测规则。在 R31 中删除重复的描述文本，改为「see AP17 for full analysis」。

---

### 8. R24 在两个模块中重复定义

**重叠:** R24（Suggestion-Reachability Check）在 mod-item-reachability.md 和 mod-description-trust.md 中都有完整的伪代码和描述。mod-description-trust.md 版本增加了 cross-reference note 指向 mod-item-reachability，但两者仍各自维护独立的完整定义。

**建议:** mod-description-trust.md 中的 R24 应仅保留 cross-reference 和 description-trust 特有的扩展（空间约束检测），完整定义仅在 mod-item-reachability.md 中维护。

---

## 建议保留为「通用」的模式

以下模式/规则在 5+ 个包中观察到，跨越多种包类型，且有充分的 issue tracker 或 config audit 证据支撑其通用性：

### Anti-Patterns（高置信度）

| ID | 名称 | 验证包数 | 证据强度 |
|---|---|---|---|
| AP1 | Description-Reality Mismatch | 12+ packs | 最强——跨所有包类型、所有 MC 版本 |
| AP2 | Circular Dependency Deadlock | 4 packs | 强——cross-mod + within-mod 变体均确认 |
| AP3 | Unfinishable Chapter | 3+ packs | 强——FTB Evolution + 多个 FTB official packs |
| AP4 | Wrong Gating | 5+ packs | 强——FTB Evolution, Craftoria, multiple FTB packs |
| AP5 | Empty Quest Description | 5+ packs | 强——FTB Evolution, Monifactory, Craftoria, NFwC, GT-O |
| AP6 | Dead-End Reward | 4+ packs | 强——FTB Evolution, FTB Skies 2, Craftoria |
| AP8 | Reward Inflation | 3+ packs | 中强——ATM-10, cesspit.net, expert packs |
| AP12 | NBT Insensitivity | 2 packs | 中——Create: Astral + Craftoria（但根因是 FTB Quests 机制，通用性成立） |
| AP14 | Custom Task Black Box | 架构层面 | 强——基于 FTB Quests 源码分析 |
| AP15 | Command Reward Side Effect | 3+ packs | 强——Monifactory, GT-O, 架构层面 |
| AP16 | Quest State Migration | 架构层面 | 强——所有 modpack 更新的通用风险 |
| AP19 | Optional-but-Mandatory | 2 packs | 中——Craftoria + 文档中多个 AP4 案例隐含此问题 |

### Micro-Patterns（高置信度）

| ID | 名称 | 验证包数 | 证据强度 |
|---|---|---|---|
| MP1 | Single-Item Gate | 23+ packs | 最强——90%+ quests across all packs |
| MP2 | Multi-Item Synthesis | 15+ packs | 强——ATM Star, Mekanism, capstone quests |
| MP3 | Acknowledgement Gate | 8+ packs | 强——Create: Delight, ATM-10, Monifactory |
| MP5 | Dimension + Item Composite | 8+ packs | 强——genre-dependent frequency, 但跨包确认 |
| MP6 | Linear Chain | 15+ packs | 最强——所有包类型 |
| MP7 | Fan-Out | 15+ packs | 最强——所有包类型 |
| MP8 | Fan-In / Convergence | 15+ packs | 最强——所有包类型 |
| MP9 | Diamond | 5+ packs | 强——Monifactory, Create: Delight, Create: Astral |
| MP10 | Independent Island | 8+ packs | 强——Create: Delight, Arcana, catalog chapters |
| MP11 | Teach-Then-Do | 8+ packs | 强——Create: Delight, ATM-10, Monifactory |
| MP12 | Tier Escalation | 8+ packs | 强——ATM-10, expert packs, RPG packs |
| MP14 | Material Bridge | 15+ packs | 最强——所有包类型 |
| MP15 | Tool Reward | 15+ packs | 强——所有包类型 |
| MP19 | Chapter-as-Stage | 23+ packs | 最强——dominant model across all packs |
| MP23 | Invisible Infrastructure | 4 packs | 强——Monifactory, E9E, GT-O（两种实现方式）|
| MP29 | Command Reward | 4+ packs | 强——但需注意 MC 版本断裂 |

### Rules（高置信度）

| ID | 名称 | 适用范围 | 证据强度 |
|---|---|---|---|
| R1 | Dimension-Reachability | all | 强——基于游戏机制 |
| R2 | Tool-Tier Reachability | all | 强——基于游戏机制 |
| R5 | Circular Dependency Detection | all | 最强——纯图算法 |
| R6 | Unreachable Quest Detection | all | 最强——纯图算法 |
| R7 | Optional-Gate-Mandatory | all | 强——多个 issue tracker 确认 |
| R10 | Reward-to-Dependent Bridge | all | 强——跨包验证 |
| R14 | Teach-Then-Do Ordering | all | 强——跨包验证 |
| R18 | Description Coverage | all | 强——Monifactory CONTRIBUTING.md 要求 |
| R20 | Chapter Completion Testability | all | 强——基于 FTB Quests 机制 |
| R22 | Cross-Chapter Dependency Validity | all | 最强——纯引用完整性检查 |
| R23 | Description-Item Consistency | all | 强——基于 FTB Quests 的 free-form description 机制 |
| R28 | Command Reward Safety Scan | all | 强——基于 command execution 的安全风险 |
| R33 | Reward Table Reference Integrity | all | 强——generator invariant |
| PP1 | Trust Contract | all | 强——cesspit.net + 多个 issue tracker |
| PP4 | Completionist's Dilemma | all | 强——基于 FTB Quests completion tracking 机制 |

### Player-Perspective Patterns（高置信度）

| ID | 名称 | 验证来源 | 证据强度 |
|---|---|---|---|
| PP1 | Trust Contract | cesspit.net + 12+ packs | 最强 |
| PP2 | Backward Shortcut | cesspit.net + expert pack community | 强 |
| PP3 | Invisible Wall | FTB Evolution + 多包 | 强 |
| PP4 | Completionist's Dilemma | FTB Evolution + 基于 FTB Quests 机制 | 强 |

---

## 总结与建议

### 核心发现

1. **Anti-patterns 的通用性远高于 micro-patterns。** AP1-AP8 描述的是「错误」——无论什么包类型都会犯的错误，通用性自然更高。Micro-patterns 描述的是「设计选择」——高度依赖包类型、mod 组合和设计哲学。

2. **ATM Signature 标注机制运作良好，但 Scope Annotation Table 未同步更新。** mod-atm-signature.md 正确地隔离了 ATM 专属模式（MP4/16/20/21/22），但 micro-patterns.archive.md 的 Scope Annotation Table 仍将 MP4 标注为 `all`。

3. **Single-source patterns 过多。** MP32、MP35、MP37、MP38、Case Study（Profession Chapter）均为 single-source。虽然文档多处标注了此事实，但它们仍以正式 pattern 身份存在于系统中，可能在 Step 2/4 加载时被 AI agent 误用为通用规则。

4. **模式间的重叠关系需要整理。** 至少 8 对重叠/矛盾的模式对已被识别。PP5/AP5、PP6/AP6、PP7/AP6+AP1 的重叠尤其显著——同一问题被拆为 2-3 个独立条目，增加了加载成本和误判风险。

5. **Rules 的适用条件比 patterns 更需要精确化。** R36、R39、R41 的 `all` 标注会在特定包类型中产生 false positive。R9 的硬编码阈值缺乏足够的数据支撑。

### 建议的优先级行动

1. **立即修复:** 同步 Scope Annotation Table 与 mod-atm-signature.md 的 ATM Signature 标注（MP4 从 `all` 改为 `kitchen-sink`）。
2. **短期:** 合并 PP5/AP5、PP6/AP6、AP19/AP4，减少 pattern 总数。
3. **中期:** 为每个 single-source pattern 添加明确的「不作为通用规则加载」标记。
4. **长期:** 建立 pattern confidence 等级系统（High/Medium/Low/Single-source），在 Step 2/4 加载时根据 confidence 决定是否呈现。
