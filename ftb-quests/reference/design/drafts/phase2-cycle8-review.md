# Phase 2 Cycle 8 — 审查结论 + 修改摘要

## 审查结论

### 通用性审查

**V1 零奖励设计接受度 — 通用性评级：中等（偏向专家/硬核包）**

"替代奖励进度"模式（MP39）的四个证据来源均为专家/硬核包（群峦救援、GTNH、RAD2、E2E），ATM10 作为反面教材来自厨房水槽包。模式本身——"任务书承担引导职责，替代系统承担奖励反馈"——在概念上是通用设计原子，但实际验证集中在硬核包。厨房水槽包中是否存在替代奖励系统尚未观察到（ATM10 使用的是直接物品奖励，争议也集中于此）。结论：模式可写入模块文件，但应标注包类型偏向。

**V2 Advancement 任务体验 — 通用性评级：功能确认通用，体验验证不足**

`advancement` 作为 FTB Quests 标准任务类型已从 GitHub 翻译 PR 确认，这是全版本通用的功能事实。但"89.8% advancement 任务的体验如何"只有 RAD2 一个冒险包案例（且无直接玩家体验反馈）。结论：功能确认可写入，体验验证标注为"缺乏"。本次未执行模块修改（现有模块已包含 MP33 Advancement Gate）。

**V3 Collection-Catalog 密度体验 — 通用性评级：无法评估**

证据真空。26.7 物品/任务的密度指标是否合理完全没有玩家反馈。结论：降级为待验证假设，不写入模块文件。

**V4 pause_game 体验 — 通用性评级：功能确认通用**

从 GitHub 翻译 PR 确认 `pause_game` 是 FTB Quests 的标准文件级配置项。这是功能事实，通用适用。但缺乏玩家体验数据。结论：已有模块文件未专门讨论此配置项，考虑到证据薄弱（仅功能确认），暂不单独写入模块。

**V5 三硬伤 — 通用性评级：分项评估**

- 物品跨级（奖励端）：ATM10 玩家直接反馈，通用设计原子。已通过。
- 物品跨级（需求端）：间接证据（Game Stages 存在说明痛点已知），但无直接玩家投诉。间接通过。
- 顺序倒置：缺乏直接验证。攻略标题暗示"教学不充分"但非"教学排错序"。降级。
- 奖励断链：ATM10 GitHub Discussion + Issue 双重验证，最强证据。通用通过。

**V6 MP39-MP42 跨包验证 — 通用性评级：MP42 完全通用，MP39 修订合理**

MP42（dependency_requirement 四种选项）从 GitHub 翻译 PR 直接确认，是 FTB Quests 标准功能，完全通用。MP39 修订建议（"零奖励" → "替代奖励"）概念合理，证据偏向硬核包。MP40/MP41 仍缺乏跨包验证。

**新发现通用性评级：**

- 新发现 1（替代奖励系统）：多包验证（GTNH、群峦救援、RAD2、E2E），通用设计原子。
- 新发现 2（Game Stages 守门人）：KLPBBS 汇总确认广泛使用，通用集成模式。
- 新发现 3（三足鼎立）：市场定位确认，不影响模块规则。
- 新发现 4（信息密度矛盾）：观察性结论，跨多个高好评包一致，但非规则级发现。
- 新发现 5（完整类型列表）：功能事实，完全通用。
- 新发现 6（ATM10 奖励争议）：MP38/R37 已有覆盖，补充细节。

---

### 证据强度审查

**高可信度（玩家直接反馈）：**
- ATM10 GitHub Discussion #3539 — xiaoxiao921 的奖励过多投诉（V1、V5 奖励断链）
- ATM10 GitHub Issue #3293 — 同一问题的正式 Issue（V5 奖励断链）
- TheBedrockMaster 的厨房水槽奖励辩护（V1、V5）

**中可信度（攻略/社区推断）：**
- GTNH "Better GTNH（任务书不会告诉你的）"攻略标题 — 间接暗示任务书引导不足
- E2E "刚开始你就希望知道的技巧"（21,000+ 阅读）— 间接暗示早期引导不足
- MC百科社区投票数据 — 反映整体包满意度，非特定于任务/奖励设计

**低可信度（功能确认，非体验验证）：**
- GitHub 翻译 PR 对 FTB Quests 功能的确认（V2、V4、V6）
- KLPBBS 汇总帖对 Game Stages 集成的描述

**证据真空（降级为待验证假设）：**
- V3 Collection-Catalog 密度体验 — 完全无玩家反馈
- V2 advancement 密集型任务书的体验反馈 — 无直接讨论
- V4 pause_game 对游戏体验的影响 — 无讨论
- V5 顺序倒置作为独立问题 — 无直接验证

**相关性 vs 因果关系审查：**
- "RAD2 高好评 → advancement 任务设计成功"：这是相关性推断，非因果证明。RAD2 的好评可能来自冒险包本身的游戏设计而非 advancement 任务类型。已在审查中标注。
- "GTNH 攻略标题 → 任务书引导不足"：这是弱推断。攻略可能出于分享热情而非弥补不足。已在审查中以"暗示"措辞保留不确定性。

---

### 一致性审查

**MP39 替代奖励进度 vs 现有 MP38 Reward Perception Split：**
无矛盾。MP38 讨论厨房水槽包中奖励慷慨度的争议，MP39 描述专家包中替代奖励系统的设计模式。两者互补——MP38 说明"奖励过多会破坏进度"，MP39 说明"替代奖励是避免此问题的一种方案"。

**MP39 vs AP8 Reward Inflation：**
无矛盾。AP8 是反面模式（奖励通胀），MP39 是正面模式（替代奖励避免通胀）。

**MP39 vs R37 Capstone-Only Progression Break：**
一致性良好。R37 区分了厨房水槽包和专家包的奖励安全阈值，MP39 的 ATM10 反面教材直接使用了 R37 的证据源（TheBedrockMaster 的评论）。

**dependency_requirement 完整选项 vs R8 Dependency Requirement Consistency：**
无矛盾。R8 的伪代码只检查 `one_completed`/`one_started` 的特殊情况（单一依赖时的冗余使用）。新增的完整选项参考提供了四个选项的全貌，是对 R8 的上下文补充而非规则修改。

**Game Stages 守门人 vs mod-item-reachability R1-R4：**
一致性良好。新增内容明确说明 Game Stages 提供了 R1-R4 在 FTB Quests 配置层面无法检查的外部保障，是对现有规则体系的补充。

**信息密度观察 vs PP5 Context Void：**
一致性良好。PP5 讨论单个 quest 的描述缺失问题，新增观察将视角扩展到全书层面——即使有足量描述，引导有效性仍可能不足。是维度补充而非规则修改。

**MP29 Command Reward 的 Game Stages 补充 vs 现有内容：**
无矛盾。现有 MP29 已提到 gamestage command rewards 的使用（Monifactory 26 个、E9E 56 个），新增补充提供了外部框架（Game Stages 三层锁定）的上下文说明。

---

## 已执行的修改

### mod-reward-design.md

1. **新增 MP39 — Alternative-Reward Progression 模式**
   - 修改内容：在 MP38 之后新增完整的 MP39 模式描述，包含四个硬核包的证据基础、ATM10 作为反面教材的详细分析、替代奖励的设计优势说明
   - 风险等级：低（追加新段落）
   - 来源：MC百科 群峦：救援、GTNH、RAD2、E2E；ATM-10 GitHub Discussion #3539

2. **新增 Game Stages 作为 Command Reward 搭档的说明**
   - 修改内容：在 MP39 之后新增"Game Stages 作为 Command Reward 的搭档"段落，说明三层锁定机制（Item/Recipe/Dimension Stages）和 FTB Quests 通过 command reward 控制阶段解锁的集成方式
   - 风险等级：低（追加新段落）
   - 来源：KLPBBS 魔改整合包常用模组 https://klpbbs.com/thread-130537-1-1.html

3. **MP29 段落末尾补充 Game Stages 外部框架上下文**
   - 修改内容：在 GreedyCraft packmode variant 之后补充 Game Stages 作为 command reward 最常搭配的外部框架的说明
   - 风险等级：中（补充现有段落）
   - 来源：KLPBBS 魔改整合包常用模组 https://klpbbs.com/thread-130537-1-1.html

4. **Quick Reference 表新增 MP39 条目**
   - 修改内容：在 MP38 之后添加 `| MP39 | Alternative-Reward Progression | Step 2 | -- | expert, kitchen-sink |`
   - 风险等级：低
   - 来源：同 MP39

5. **Cross-References 表新增 MP39 交叉引用**
   - 修改内容：新增两行 MP39 交叉引用（→ mod-teaching-pacing MP23、→ mod-item-reachability）
   - 风险等级：低
   - 来源：同 MP39

### mod-dependency-graph.md

1. **新增 dependency_requirement 完整选项参考**
   - 修改内容：在 MP32 之后新增"dependency_requirement 完整选项参考 (FTB Quests 标准功能)"段落，包含四种选项（all_completed/all_started/one_completed/one_started）的完整说明、min_required_dependencies 的用途、配套配置项列表、三个包的 real case
   - 风险等级：低（追加新段落）
   - 来源：FTB Quests zh_cn 翻译 PR https://github.com/FTBTeam/FTB-Mods-Issues/issues/1296

### mod-item-reachability.md

1. **新增 Game Stages 作为物品可达性外部守门人**
   - 修改内容：在 MP33 之后新增"Game Stages 作为物品可达性的外部守门人"段落，说明 Game Stages 补足 FTB Quests 物品锁定缺陷的三层机制，以及与 R1-R4 规则的关系
   - 风险等级：低（追加新段落）
   - 来源：KLPBBS 魔改整合包常用模组 https://klpbbs.com/thread-130537-1-1.html

### mod-teaching-pacing.md

1. **新增任务书信息密度与引导能力矛盾的跨包观察**
   - 修改内容：在 PP5 最后一个变体（NFwC #333）之后新增跨包观察段落，引用 GTNH、E2E、RAD2 三个包的攻略标题说明信息密度和引导有效性是两个独立维度
   - 风险等级：低（追加新段落）
   - 来源：MC百科 GTNH、E2E、RAD2 页面

### mod-description-trust.md

- 未执行修改。Phase 2 Cycle 8 未发现与 mod-description-trust 直接相关的新证据。该模块的 AP1 实证案例已在 Cycle 7 Phase 2 中充分更新（Architect's Exodus 19 issues）。

---

## 未执行的修改（高风险或证据不足）

1. **V3 Collection-Catalog 密度体验** — 证据真空。26.7 物品/任务的密度指标是否合理完全没有玩家反馈。不写入任何模块。
2. **V2 advancement 密集型任务书体验** — 功能确认已存在（MP33），但"89.8% advancement 任务"的体验验证缺失。不修改现有 MP33 描述。
3. **V4 pause_game 配置项** — 功能确认但无玩家体验数据。不单独写入模块。
4. **V5 顺序倒置** — 缺乏直接验证。攻略标题暗示"教学不充分"但非"教学排错序"，不修改 R14 Teach-Then-Do Ordering 规则。
5. **MP40 扩展定义** — "扩大 MP40 定义范围包含所有非物品收集类任务驱动"的建议缺乏跨包验证，暂不执行。
6. **MP41 极端收集标注** — "保持 MP41 但标注为极端案例"的建议需要有对应的模块文件，当前模块体系中 MP41 未出现在五个模块文件中。
7. **新增 Game Stages 独立模块** — Phase 2 建议"新增一个模块描述 FTB Quests + Game Stages 的协作方式"。这属于高风险（新模块创建），且 Game Stages 相关内容已分散写入 mod-reward-design.md（MP29 补充 + MP39 搭档说明）和 mod-item-reachability.md（外部守门人），暂不创建独立模块。
8. **按包类型区分奖励策略指南** — Phase 2 建议"按包类型区分奖励策略"。MP39 已部分实现此目标（区分厨房水槽和专家包），但完整的差异化奖励策略指南需要更多包类型的数据支撑。

---

## 待验证假设（降级为假设的发现）

1. **V3 物品密度上限假设** — "26.7 物品/任务可能是极端值"这一推断需要实际游戏测试或社区调研来验证。建议：在后续包开发中设置不同密度（10/20/30 物品/任务）的对照章节，收集玩家反馈。

2. **V2 advancement 任务无聊度假设** — "大量 advancement 任务可能导致任务书枯燥"这一假设缺乏玩家体验反馈。建议：对 RAD2（89.8% advancement）和 ATM-10（低 advancement 占比）的玩家进行体验对比调研。

3. **V4 pause_game 对阅读体验的影响假设** — "pause_game 对信息密集型任务书有正面影响"这一假设仅基于功能推断，缺乏实际验证。建议：在 TFG Modern（使用 pause_game）的玩家中调研阅读体验。

4. **V5 顺序倒置假设** — "教学可能排在实践后面"这一假设从攻略标题间接推断，但证据不足以作为独立问题。建议：在 R14 Teach-Then-Do 规则的后续验证中特别关注是否存在教学晚于实践的案例。

5. **替代奖励系统跨包适用性假设** — MP39 的证据集中在硬核/专家包。替代奖励系统在厨房水槽包、冒险包、故事包中是否同样有效尚未验证。建议：在非专家包中寻找或设计替代奖励案例进行验证。

6. **Game Stages 跨版本兼容性假设** — KLPBBS 汇总帖描述的是特定 MC 版本的 Game Stages 集成方式。不同 MC 版本（1.16.5/1.19.2/1.20.1/1.21）的 Game Stages 实现可能有差异。建议：在生成不同版本的包时验证 Game Stages 集成方式。
