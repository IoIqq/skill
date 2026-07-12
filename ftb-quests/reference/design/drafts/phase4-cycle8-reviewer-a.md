# Phase 4 审查员 A — 通用性审查

> 审查对象：Cycle 8 Phase 2/3 新增的模式和规则
> 审查角度：通用性——这些发现真的跨包适用吗？

---

## 审查通过（无通用性问题）

### R44 — Reward-Stage Matching（奖励-阶段匹配）
- 审查结论：通过，通用性充分
- 理由：R44 已在设计中内置了包类型差异化——expert 包为 ERROR、kitchen-sink 包为 WARNING，并显式引用 R37 的 capstone-only 安全阈值。核心逻辑（奖励物品等级不应超过任务阶段 +1）是所有包类型都适用的设计原则，差异仅在于违反时的严重度。证据来源包括 ATM-10（kitchen-sink）和 Craftoria/GT-O（expert），覆盖了两个主要包类型。伪代码中的 `pack_type` 分支已正确处理了通用性。

### R45 — Reward Guidance Bridging（奖励引导衔接）
- 审查结论：通过，通用性充分
- 理由：R45 检查的是纯 quest book 结构（章节 capstone 奖励与下一章入口任务的交集），不依赖任何特定模组、Game Stages 框架或 MC 版本。这是 MP14（Material Bridge）从 quest 级别到 chapter 级别的自然提升，MP14 本身已验证为跨包通用（"appears across all pack genres"）。伪代码仅使用 `dependencies`、`item_tasks`、`item_rewards` 等 FTB Quests 标准字段。唯一限制是"capstone quest"的识别（依赖数最多的 quest），这在所有包类型中都合理。来源引用了 mcmod.cn 和 Meegle 的通用设计原则，不偏向特定包类型。

### dependency_requirement 四种选项（含 min_required_dependencies）
- 审查结论：通过，这是 FTB Quests 的功能事实
- 理由：四个选项（`all_completed`、`all_started`、`one_completed`、`one_started`）从 GitHub 翻译 PR（FTBTeam/FTB-Mods-Issues #1296）直接确认，是 FTB Quests 模组的标准 API。`min_required_dependencies` 是同一定义文件中的标准字段。Real cases 覆盖了 Monifactory（expert）、Create: Delight（create）、ATM-10（kitchen-sink）三种包类型。这是功能文档而非设计推断，不存在通用性问题。

### R43 — Stage-Quest Causal Chain Acyclic（Stage-Quest 因果链无环）
- 审查结论：通过，适用范围已在 Quick Reference 中标注
- 理由：R43 在 Quick Reference 中已标注 `expert, story` 包类型，这是正确的——只有使用 Game Stages + command reward 路由的包才存在 Stage-Quest 交叉环的风险。不使用 Game Stages 的包（大部分 kitchen-sink）根本不会触发此规则。伪代码中包含 `if cmd_reward.activates_stage(stage_name)` 的前置条件，不满足时规则自动跳过。R43 作为 R5 的扩展层设计合理——R5 是通用的（all），R43 是条件触发的（expert, story）。

### R42 — Stage-Internal Item Reachability（合成链阶段内可达性）
- 审查结论：通过，适用范围已在 Quick Reference 中标注
- 理由：R42 在 Quick Reference 中已标注 `expert, story, skyblock`，排除了 kitchen-sink。这是合理的——kitchen-sink 包通常不设置严格的阶段资源锁定，物品可达性问题由 R1-R4 覆盖。R42 专门检查"合成树叶子节点在当前阶段可达资源集合内"的问题，这只在有明确阶段划分的包中有意义。伪代码中 `stage_available_resources[current_stage]` 需要 L2 数据，无数据时降级为 INFO，实现了优雅退化。

### 信息密度观察（任务书的信息密度与引导能力矛盾）
- 审查结论：通过，这是观察性结论而非规则
- 理由：该段落明确指出"信息密度和引导有效性是两个独立的维度"，这是一个描述性发现而非规范性规则。证据来自 GTNH、E2E、RAD2 三个高好评包的攻略标题模式——这些包覆盖 expert（GTNH、E2E）和冒险（RAD2）类型。该段落没有提出新规则，而是对 PP5 Context Void 的维度扩展说明，PP5 本身已验证为跨包通用（Quick Reference: "all"）。观察性结论不承担通用性规则的举证责任。

---

## 需要修正（通用性不足）

### MP39 — Alternative-Reward Progression（替代奖励进度）
- 问题：**Quick Reference 标注的包类型为 `expert, kitchen-sink`，但证据全部来自 expert/hardcore 包。**
  - 四个证据源：TerraFirma Rescue（硬核生存）、GTNH（硬核 expert）、RAD2（冒险 expert）、E2E（expert）——全部是高难度包。
  - ATM-10 作为"反面教材"出现，但它证明的是"直接物品奖励在 kitchen-sink 中引发争议"，不是"替代奖励在 kitchen-sink 中有效"。
  - Phase 2 审查草稿自身已承认："实际验证集中在硬核包。厨房水槽包中是否存在替代奖励系统尚未观察到。"
  - 将 kitchen-sink 列入适用范围缺乏证据支撑。
- 建议修正：
  1. Quick Reference 表中 MP39 的 Pack types 从 `expert, kitchen-sink` 改为 `expert`
  2. MP39 正文开头添加一句：`Kitchen-sink 包中替代奖励系统的案例尚未在已研究的 39 个包中观察到。ATM-10 的争议说明 kitchen-sink 包的奖励设计问题存在，但替代方案是否适用仍待验证。`
  3. 将"待验证假设"（Phase 2 草稿中的第 5 条）升级为显式 TODO 标注在模式描述末尾

### Game Stages 段落（mod-reward-design.md 和 mod-item-reachability.md 中的三处新增）
- 问题：**Game Stages 的证据来源严重偏向 expert/魔改包，且存在版本特异性，但段落行文暗示通用适用性。**
  - KLPBBS 魔改包常用模组汇总是中文社区 expert/魔改包的资源，其"广泛使用"的结论不能外推到 kitchen-sink、create、story 包。
  - 在已研究的包中，明确使用 Game Stages 的只有 Monifactory（expert）和 E9E（expert）。GT-O（同为 expert）使用了完全不同的 dependency-implicit 方案（零 command rewards）。Craftoria、ATM-10、E10、MI:Foundation 等 kitchen-sink/create 包均未使用 Game Stages。
  - Game Stages 的版本兼容性存在问题：1.12.2 是黄金期，1.16.5 仍可用，1.20+ 被 KubeJS 逐渐替代。段落中虽有一句"现代版本中 KubeJS + FTB Quests 原生阶段管理逐渐替代了 Game Stages 生态"，但未充分警告读者这不是一个跨版本通用的方案。
  - mod-item-reachability.md 中的"Game Stages 闭环集成的技术架构"段落详细描述了 1.12.2 工具链细节，但这些细节对 1.21 的包生成可能完全过时。
- 建议修正：
  1. mod-reward-design.md 的 "Game Stages 作为 Command Reward 的搭档" 段落开头添加适用范围声明：`此段落主要适用于 expert/魔改包。Kitchen-sink、create、story 包通常不使用 Game Stages。`
  2. mod-item-reachability.md 的 "Game Stages 作为物品可达性的外部守门人" 段落添加版本警告：`注意：Game Stages 在 MC 1.12.2-1.16.5 时期是标准方案，1.20+ 逐渐被 KubeJS 替代。生成 1.20+ 包时应确认目标包实际使用的阶段锁定方案。`
  3. mod-item-reachability.md 的 "Game Stages 闭环集成的技术架构" 段落标题改为 "Game Stages 闭环集成的技术架构（MC 1.12.2-1.16.5 为主）"，并在段末添加：`1.20+ 的 KubeJS 阶段管理方案在概念上延续了"阶段即守门人"模式，但具体 API 和集成方式不同，需要单独调研。`

### R44 — Reward-Stage Matching 的 `stage_map` 数据依赖
- 问题：**R44 的伪代码依赖 `stage_map.get(reward.item.id)` 来确定物品的阶段归属，但这个映射数据从哪里来？**
  - 对于 expert 包（GregTech 系列），电压等级物品有明确的阶段归属，`stage_map` 可以从模组数据构建。
  - 对于 kitchen-sink 包，物品可能属于多个模组的多个"阶段"，`stage_map` 的构建远不如 expert 包清晰。ATM-10 有 300+ 模组，一个 Mekanism 物品应该属于什么"阶段"？包作者可能根本没有定义阶段。
  - 当 `stage_map` 不存在时，R44 退化为 `estimate_stage(reward.item.id)`——这个估算函数的准确性在 kitchen-sink 包中极低。
- 建议修正：
  1. R44 伪代码中添加无数据降级路径：`if not stage_map: INFO: "[no-stage-data] reward-stage matching skipped — pack has no stage definitions"`
  2. 正文中明确：`R44 在 expert 包中效果最佳（阶段定义清晰），在 kitchen-sink 包中严重依赖 L2 用户数据。无阶段定义的 kitchen-sink 包中 R44 退化为 INFO 级别报告。`

---

## 需要标注适用范围

### 四维阶段模型（时间/空间/资源/社会）
- 实际适用范围：**这是一个理论分析框架，不是实际包的设计做法。** 在已研究的 39 个包中，没有任何一个包显式使用了全部四个维度。大多数包仅使用时间维度（章节顺序 = 阶段），expert 包额外使用资源维度（电压等级控制矿石获取），社会维度仅在以村民经济为核心的 skyblock 包中有零星体现。空间维度（阶段控制生物群系/结构生成）是最少被验证的——文中引用的 CSDN 文章描述的是理论设计而非实际包实现。
- 建议标注：在四维模型段落开头添加：`这是一个从多来源交叉分析中提炼的理论框架，用于指导阶段设计的思考维度。实际包中通常只使用 1-2 个维度（时间 + 资源最常见），四维全部使用的案例尚未在已研究的包中发现。`

### 弱锁策略（允许跳关但奖励孤立化）
- 实际适用范围：**这是一个设计哲学主张，证据主要来自 mcmod.cn 的一篇社区文章，以及 TFG Modern 的提及。** 弱锁策略在概念上有吸引力（承认玩家创造力、提供"偷鸡爽感"），但：
  - 在已研究的 39 个包中，明确实现弱锁的包数量未知。弱锁的实现依赖 Game Stages 的 Item Stages/Recipe Stages，而已确认使用 Game Stages 的只有 Monifactory 和 E9E。
  - Monifactory 和 E9E 是否真的实现了"弱锁"（允许跳关但孤立化奖励）还是"强锁"（完全阻止跳关）需要进一步验证。Monifactory 的 `dependency_chain` chapter 使用 26 个 gamestage command rewards 路由电压阶段，这更像是"强锁"（严格按电压等级解锁）。
  - 文中已正确标注"可编码性较低——目前只能作为人类审查项"，但未标注"实际采用此策略的包数量未知"。
- 建议标注：添加 `注意：弱锁策略作为设计哲学在中文社区文章中被提倡，但在已研究的包中明确实现弱锁（而非强锁）的案例数量待确认。Monifactory 和 E9E 使用 Game Stages 但更接近"强锁"模式。弱锁的实现需要包作者刻意设计"非预期获取路径"并配置下游 Stage 锁定，这对作者的设计能力要求较高。`

### 教学快速推入策略
- 实际适用范围：**概念通用，但具体做法（"前 3-5 个任务"）可能偏向 expert/hardcore 包。**
  - 策略的核心洞察——"早期教学必须在玩家热情最高的时间窗口内完成"——对所有包类型都成立。
  - 但"前 3-5 个任务应包含明确的教学文本，介绍包的核心差异化机制"这个具体建议，主要适用于有"核心差异化机制"的 expert 包（如 GTNH 的电压系统、群峦救援的 GT 货币系统）。Kitchen-sink 包（ATM-10）的早期任务更多是 vanilla 引导，不需要特别"推入"。
  - 证据来源是 mcmod.cn/post/4382.html（中文社区 expert 包设计文章）和 Monifactory #2359（expert 包教学不足 issue）。
  - 文中已正确将此策略定位为与 R14/R41 形成"三层教学框架"，R14 和 R41 的适用范围标注为 `all`，但快速推入策略本身未标注包类型偏向。
- 建议标注：在段落末尾添加 `此策略对 expert/hardcore 包最为关键（核心机制复杂、教学缺失代价高）。Kitchen-sink 和 create 包的早期教学需求较低，快速推入的紧迫度也较低。`

### Game Stages 闭环集成（mod-item-reachability.md）
- 实际适用范围：**MC 1.12.2-1.16.5 的 expert 包。**
  - 闭环模式"任务完成 → Stage 激活 → 物品/配方/维度解锁 → 下一个任务"是 expert 包的标准做法，但在已研究的包中只有 Monifactory 和 E9E 明确使用。
  - GT-O 作为同为 GregTech expert 的包，选择了完全不同的 dependency-implicit 方案（不使用 Game Stages），说明即使是 expert 包内部，Game Stages 闭环也不是唯一做法。
  - 1.20+ 版本中 KubeJS 逐渐替代 Game Stages，闭环模式的实现方式会变化。
- 建议标注：在"Game Stages 闭环集成的技术架构"段落末尾添加：`此闭环模式在已研究的包中由 Monifactory 和 E9E 实现。GT-O 使用不同的方案（dependency-implicit，无 Game Stages），说明 Game Stages 闭环是 expert 包的一种可行方案而非标准做法。1.20+ 包应评估 KubeJS 替代方案的可行性。`

### progression_mode 对阶段结构的设计影响（mod-dependency-graph.md）
- 实际适用范围：**概念通用，但文中引用的具体数据偏向 expert。**
  - `linear` 模式的例子全部是 expert 包（Monifactory depth 15、GT-O depth 8-15），`flexible` 模式的例子是 ATM-10（kitchen-sink）。这反映了现实——expert 包倾向 linear、kitchen-sink 倾向 flexible——但也可能给读者造成"linear = expert, flexible = kitchen-sink"的二元印象。
  - 实际上，create 包（Create: Delight）使用 flexible 但有深度链（depth 18），story 包可能使用 linear 但深度较浅。progression_mode 与包类型不是严格绑定的。
- 建议标注：在段落末尾添加：`注意：progression_mode 和包类型之间是相关性而非确定性关系。Create 包可以使用 linear，expert 包可以使用 flexible（GT-O 的 visible chapters 使用 hide_quest_until_deps_visible 实现了类似 flexible 的体验）。选择 progression_mode 应基于包的教学策略而非包类型标签。`

---

## 总结

| 类别 | 数量 | 关键发现 |
|---|---|---|
| 审查通过 | 6 | R44、R45、dependency_requirement、R43、R42、信息密度观察 |
| 需要修正 | 3 | MP39 包类型标注过宽、Game Stages 段落缺适用范围声明和版本警告、R44 无数据降级路径缺失 |
| 需要标注 | 5 | 四维模型（理论框架非实践）、弱锁策略（实际采用数未知）、教学快速推入（偏向 expert）、Game Stages 闭环（非唯一方案）、progression_mode（非二元绑定） |

**核心发现：** Cycle 8 新增内容的主要通用性风险不是"规则本身不适用于其他包"，而是**"描述文本的暗示范围大于证据支撑范围"**。具体表现为：

1. **expert 包证据被泛化为通用模式**：MP39 的 kitchen-sink 标注、Game Stages 段落缺少包类型限定、弱锁策略缺少实际采用数据。
2. **特定 MC 版本的做法被描述为 timeless 模式**：Game Stages 1.12.2 工具链的详细描述未标注版本时效性。
3. **理论框架与实际做法的边界模糊**：四维模型读起来像是包的常见做法，但实际上是分析框架。

这些修正不涉及规则逻辑的错误——R42-R45 的伪代码和检测逻辑都是正确的。问题集中在**描述文本的措辞和适用范围标注**上，属于文档层面的修正，不影响规则的可实现性。
