## 审查员 B -- 完备性质疑 (Cycle 5 新增模式)

审查日期: 2026-07-08
审查范围: MP35 (Dual-Task Automation), MP36 (Currency-as-Reward), MP37 (Progress Catalog), MP38 (Profession Chapter), Draft R36 (Hardcore Zero-Optional), Draft R37 (Kill Task Density)
审查方法: 逐模式/规则质疑边界情况、跨模式交互、数据完整性、与现有规则的覆盖冲突
来源文件: micro-patterns.archive.md, hardcore-progression-rules-R36-R37_2026-07-08.md, mod-reward-design.md, mod-teaching-pacing.md, mod-dependency-graph.md, review-b-completeness_2026-07-05.md (B5 consume_items), review-b-completeness_2026-07-07.md (Cycle 4 B)

---

### 一、MP35 -- Dual-Task Automation Verification

#### 完备性评级: B (覆盖主要场景，存在可量化的边界遗漏)

MP35 的核心贡献——`consume_items: false` + checkmark "automated" 双任务结构——精确描述了 Cabricality 的 automation 验证范式。但以下边界情况未覆盖：

#### 遗漏 1: Fluid/Energy task 的 automation 验证完全缺失

MP35 明确限定于 `type: "item"` + `type: "checkmark"` 组合。但 Create 包的 automation 不仅限于物品制作——Create contraptions 同样产出流体（fluid processing）和传输能量。一个要求玩家建造自动流体处理装置的 quest 可能需要 `type: "fluid"` task + checkmark，而非 item task。

现有 MP27 (Fluid Task Gate) 和 MP28 (Energy Threshold Gate) 分别描述了 fluid task 和 energy task 的设计原则，但没有与 automation 验证交叉。Cabricality 本身的 task diversity 极低（仅 2 种: item + checkmark），因此这个问题在 Cabricality 中不存在。但 MP35 如果推广到其他 Create 包（如 Create: Above and Beyond），fluid/energy automation 验证就是直接的边界情况。

**严重性:** 中。当前 MP35 为 single-source（仅 Cabricality），但文档中 "Applicable when: the pack requires players to build actual automation" 的表述暗示了更广泛的适用性。

**建议:** MP35 增加一个 "Extension variants" 小节，明确说明：(1) fluid task + checkmark 的 automation 验证（"prove you automated this fluid processing chain"）；(2) energy task + checkmark 的 automation 验证（"prove you built a power generation system"）。标注为 "theoretical — no pack data validates these variants yet." 同时限定主模式的 scope 为 item-only，避免过度推广。

#### 遗漏 2: `only_from_crafting` 与 `consume_items: false` 的组合语义未覆盖

MP1 (Single-Item Gate) 明确提到 "No `consume_items`, no `only_from_crafting`"。MP2 (Multi-Item Synthesis) 警告 "Do NOT set `consume_items: true`"。但 MP35 仅处理 `consume_items: false`，未提及 `only_from_crafting` 字段。

在 Create 包的上下文中，`only_from_crafting: true` 是一个更强的 automation 约束——它要求物品**必须通过合成获得**，排除了 loot drops、交易、或其他非合成来源。这与 MP35 的 "prove you built automation" 语义高度一致，但 MP35 没有说明是否应同时设置 `only_from_crafting: true`。

**严重性:** 低-中。Cabricality 的数据中未观察到 `only_from_crafting` 使用（可能为 FTB Quests 不支持此字段或 Cabricality 未使用），但这是一个语义相关的字段，MP35 应该明确其与 `consume_items: false` 的关系。

**建议:** MP35 增加一条说明："`only_from_crafting` 字段（如果 FTB Quests 版本支持）可作为 `consume_items: false` 的补充约束，进一步限制物品来源。两者的组合语义：`consume_items: false` = '证明物品存在'；`only_from_crafting: true` = '证明物品是合成的而非交易的'。"

#### 遗漏 3: 与 Review B Cycle 1 B5 (`consume_items` 通用语义) 的关系未标注

Review B (2026-07-05) 的 B5 挑战明确指出 `consume_items` 语义缺乏通用模式。MP35 解决了 `consume_items: false` 的一个特化场景（automation verification），但 B5 的核心问题——`consume_items: true` vs `consume_items: false` 的通用决策框架——仍未被覆盖。

具体来说：
- `consume_items: true` + unique item = 永久销毁风险（B5 已识别）
- `consume_items: false` + resource sink = 可重复利用漏洞（B5 已识别）
- MP35 覆盖了 `consume_items: false` + checkmark 的组合，但这是三个场景中的一个

**严重性:** 低。MP35 不需要解决 B5 的全部问题，但应标注其与 B5 的关系，避免读者误以为 MP35 已完全覆盖 `consume_items` 语义。

**建议:** MP35 增加 cross-reference 注释："MP35 is a specialized application of `consume_items: false`. For the broader consume vs. retain decision framework, see Review B Cycle 1 B5 (pending). This pattern does not address `consume_items: true` misuse."

#### 遗漏 4: Observation task 作为 automation 验证的替代方案未提及

MP3 (Acknowledgement Gate) 描述了三种 "acknowledge" task type: checkmark, stat, observation。MP35 仅使用 checkmark。但在某些场景中，`observation` task（auto-completes when player looks at the block/entity）可能比 checkmark 更适合 automation 验证——例如 "observe your mechanical harvester running" 自动完成了 "我建造了自动化" 的证明，无需 honor system。

**严重性:** 低。Observation task 的使用取决于具体 mod 是否支持相关 block/entity 的 observation，不是所有 automation 都有对应的 observable entity。

**建议:** MP35 Design considerations 增加一条："(5) Consider `observation` tasks as a stronger alternative to checkmark for automation verification — observing a running machine auto-confirms the automation exists without relying on the honor system. Availability depends on mod support for observation targets."

---

### 二、MP36 -- Currency-as-Reward

#### 完备性评级: B (覆盖主要场景，currency inflation 和 R10 交互遗漏)

MP36 正确区分了 currency reward 与 MP14 (Material Bridge) 和 MP16 (XP Drip) 的关系，3-pack 验证（GT-O, NFwC, TWR insight）提升了 confidence。但以下边界情况值得关注：

#### 遗漏 1: Currency inflation 的量化框架完全缺失

MP36 Design consideration (2) 提到 "Calibrate currency amounts against shop prices — inflation devalues the reward"，但这只是一条定性建议。缺少的是：

1. **累计通胀计算框架:** 如果包有 200 个 quest，每个 quest 给 10 copper coins，player 最终获得 2000 coins。如果 shop 中 best item 定价 100 coins，player 可以轻松购买所有商品——currency 失去意义。
2. **Currency sink 的消耗速率:** MP36 提到需要 "corresponding currency sink (shop, trade station)"，但不评估 sink 的消耗速率是否匹配 currency 的产出速率。
3. **Mid-game currency transition:** GT-O 使用 copper_coin 作为 early-game currency。如果 mid-game 引入 silver_coin (1 silver = 100 copper)，early currency 如何处理？是否需要兑换机制？

这与 AP8 (Reward Inflation) 是同一类问题的 currency 变体，但 AP8 聚焦于 item reward 的时间分布，不直接覆盖 currency 的供需平衡。

**严重性:** 中-高。Currency inflation 是 MP36 的核心风险，当前只有一条定性建议而无量化框架。

**建议:** MP36 Design considerations 增加量化框架："(2) Currency inflation check: Calculate total currency output across all quests (sum of all currency rewards). Compare against shop prices: if total_output > 5x the most expensive shop item, the economy is over-inflated — reduce per-quest amounts or add more expensive sinks. Target: total currency earned across the entire pack should be 1.5-3x the cost of all purchasable items combined."

#### 遗漏 2: R10 (Reward-to-Dependent Bridge) 对 currency reward 的处理不完整

R10 的伪代码中有 `if not is_tool/reward/currency/loot: INFO` 的排除逻辑，将 currency reward 排除在 bridge 检查之外。但排除条件写的是 "currency"，而 MP36 的实现是 `type: "item"` reward with a currency item ID。R10 如何识别一个 item reward 是 "currency" 而非普通 material bridge？

如果 R10 的实现仅检查 reward type 字段（`type == "item"`），则所有 currency reward 都会被当作普通 item reward 处理，触发 "Reward has no dependent bridge" 的 false positive——因为 currency item 不出现在 dependent quest 的 task 中（它被 shop 消耗而非后续 quest 消耗）。

**严重性:** 中。这会导致 R10 对所有使用 MP36 的 quest 产生 false positive，降低规则的信噪比。

**建议:** R10 增加 currency item 识别机制：维护一个 `currency_item_ids` 列表（在 Step 2 interview 中收集，或从 shop chapter 的配置中推断），当 item reward 的 ID 在此列表中时，跳过 bridge 检查并标注 "currency bridge (shop-mediated)."

#### 遗漏 3: TWR insight 的 custom reward type 推广性

MP36 验证纳入了 TWR 的 `frostedheart:insight` custom reward type，但标注 "different implementation, same concept"。问题在于：custom reward types 是 mod-specific 的（需要 companion mod 注册），FTB Quests 的原生 type 系统不包含 `frostedheart:insight`。MP36 的 "Implementation" 小节只描述了 `type: "item"` 的 currency，但 TWR 的 insight 使用 `type: "frostedheart:insight"` 字段。

如果 MP36 试图同时覆盖 item-type currency 和 custom-type currency，其 "Implementation" 描述需要扩展。如果不覆盖 custom-type，则 TWR 不应作为 MP36 的验证数据点——它是一个 related but distinct pattern。

**严重性:** 低。MP36 的 draft 中已将 GT-O 和 NFwC 作为主数据点（两者都是 item-type），TWR 作为 variant 提及。但如果读者将 TWR 视为 MP36 的标准实现之一，会对 custom reward type 的生成产生错误期望。

**建议:** MP36 明确区分两个层级：(1) "Standard currency" = item-type reward with currency item ID（GT-O, NFwC），AI 可生成；(2) "Custom-type currency" = mod-registered reward type（TWR insight），AI 不可生成（需要 companion mod 支持）。Implementation 小节只描述 standard currency，custom-type 作为 "Related pattern" 注释。

#### 遗漏 4: Currency reward 与 team mode 的交互

Draft team-multiplayer-patterns_2026-07-06.md 讨论了 `consume_items: true` 在 team mode 下的行为（每个成员需要贡献材料），但没有讨论 currency reward 在 team mode 下的分配问题。如果 quest 给 10 coins 作为 reward：

- 在个人模式下：10 coins 给完成任务的玩家
- 在 team mode 下：10 coins 是给完成任务的玩家还是所有团队成员？
- 如果 TWR 的 insight 使用 `team_reward: true` 字段（已在 mod-reward-design.md 中确认），这是否意味着 currency reward 在 team mode 下需要特殊处理？

**严重性:** 低。Team mode 是一个可选的 pack 配置，大多数包不使用。但 TWR 数据中的 `team_reward: true` 字段证明了这个维度存在。

**建议:** MP36 Design considerations 增加一条："For team-mode packs: currency rewards may need `team_reward: true` (if the reward type supports it) to ensure all team members receive the currency. Without team sharing, the completing player accumulates currency while teammates get nothing."

---

### 三、MP37 -- Progress Catalog Chapter

#### 完备性评级: C (遗漏关键边界情况——completion percentage 交互)

MP37 描述了一个 dependency-free + reward-free 的 chapter 用作 visual progress tracker。这个概念清晰且有明确的设计意图，但遗漏了一个对玩家体验有直接影响的关键问题：

#### 遗漏 1: `optional` flag 与 completion percentage 的交互——最严重的遗漏

MP37 的 implementation 描述了 "no dependencies, no rewards, single item task" 的 quest，但**没有提及 `optional` flag**。这对 completion percentage 有直接影响：

- FTB Quests 的 chapter completion = `completed_non_optional / total_non_optional * 100%`
- `optional: true` 的 quest 不计入 completion 分母
- 如果 MP37 catalog quest 设为 `optional: false`（默认），它们全部计入分母
- 一个有 100 个 catalog quest 的 progress chapter，玩家完成 60 个 → 60% completion
- 这个 60% 会显示在 chapter list 中，给 completionist 玩家造成 "这个 chapter 没完成" 的焦虑

PP4 (Completionist's Dilemma) 已经识别了这个问题："The `optional: true` flag excludes a quest from completion percentage calculation." MP37 的 catalog quest 天然应该是 `optional: true`（它们是 tracker，不是 progression requirement），但 MP37 文档没有说明这一点。

**严重性:** 高。这是整个审查中严重性最高的遗漏——MP37 如果不设置 `optional: true`，会直接触发 PP4，使 chapter completion percentage 成为一个持续的不完整指示器。GT-O 的 progress chapter 如果有 50 个 voltage-tier milestone quests，玩家完成一半后看到 50% completion，这与 progress tracker 的 "at-a-glance" 设计意图矛盾——tracker 应该反映"你已经做了什么"，而不是"你还差多少没做"。

**建议:** MP37 Implementation 必须增加 `optional: true` 作为 mandatory field："Every quest in a progress catalog chapter MUST set `optional: true`. These quests are progress trackers, not progression requirements. Without `optional: true`, the chapter completion percentage will stall below 100% and trigger PP4 (Completionist's Dilemma). The catalog's purpose is to reflect what the player HAS done, not to gate progression."

#### 遗漏 2: Catalog quest 的 `hide_until_deps_visible` 与 "any time completable" 矛盾

MP37 Design consideration (2) 说 "All quests should be completable at any time (no gating) — the catalog reflects what the player HAS done, not what they CAN do." 但如果 pack 的其他部分使用了 `hide_until_deps_visible`，而 catalog quest 引用了被隐藏 quest 的依赖关系，catalog quest 也可能被隐藏。

此外，catalog quest 的 item task 可能需要 late-game 物品（e.g. OPV circuit in GT-O）。虽然 task 本身 "completable at any time"（只要玩家有物品就可以提交），但**物品的可达性**取决于游戏进度。Design consideration (2) 的 "no gating" 应该更精确地定义为 "no quest-book gating (no dependencies)"，而非 "no progression gating"。

**严重性:** 低-中。这是一个措辞精确性问题，不会导致功能性错误，但可能导致 AI 生成时误解 catalog 的设计意图。

**建议:** 将 Design consideration (2) 修改为："All quests should have no quest-book dependencies — they are completable as soon as the player obtains the required item, regardless of quest progression. Note: the required item may still be gated behind progression (e.g. a late-game circuit), so 'completable at any time' means 'no quest-level gating,' not 'obtainable at any time.'"

#### 遗漏 3: Catalog quest 的 description 策略未指定

MP37 的 Implementation 只描述了 task 和 reward（no dependencies, no rewards, single item task），但没有说明 description 应该如何处理。对于一个 progress catalog quest：

- **选项 A:** 空 description（纯 tracker，无需教学——但违反 R18 Description Coverage）
- **选项 B:** 简短 description 标注 tier/stage（"LV Circuit — first voltage tier"）
- **选项 C:** 详细 description 说明如何获取该 milestone item（但这是主 progression chapter 的职责）

R18 (Description Coverage) 会对无 description 的非 catalog-cell quest 触发 WARNING。MP37 catalog quest 是否应被 R18 的 catalog-cell 豁免覆盖？当前 R18 豁免条件是 "`rsquare`/`circle` shape, size <= 2.0, catalog chapter, single task"。MP37 catalog quest 可能使用不同的 shape（如 hexagon 标注 tier），不在豁免范围内。

**严重性:** 低。R18 的 WARNING 是 INFO 级别的软检查，不会阻止生成。但 MP37 应该明确 description 策略以避免歧义。

**建议:** MP37 Implementation 增加 description 指导："Progress catalog quests should have a brief description identifying the tier/stage and which main-progression chapter produces this item (e.g. 'LV Circuit — see LV chapter for crafting instructions'). This satisfies R18 while avoiding duplication of crafting tutorials."

#### 遗漏 4: Catalog chapter 与 R20 (Chapter Completion Testability) 的交互

R20 检查每个 chapter 的 non-optional quest 是否可全部完成。如果 MP37 catalog quest 是 non-optional 且要求 late-game item，R20 需要验证该 item 在 pack 中是可达的。如果 item 因 mod 更新变为不可达（R1/R2 检测范围），整个 catalog chapter 变为 unfinishable。

如果按遗漏 1 的建议将 catalog quest 设为 `optional: true`，R20 会自动跳过它们——这是正确的行为。但如果 pack author 忘记设置 optional，R20 + MP37 的组合会产生 ERROR。

**严重性:** 低（前提是遗漏 1 被修复）。如果 catalog quest 是 optional，R20 不检查它们。如果不是 optional，R20 正确地标记了问题。

**建议:** MP37 Design considerations 增加 R20 交叉引用："Progress catalog chapters must use `optional: true` on all quests. R20 (Chapter Completion Testability) will flag non-optional catalog quests as unfinishable if their required items become unreachable."

---

### 四、MP38 -- Profession Chapter

#### 完备性评级: C (核心概念区分不足)

MP38 描述了一个有趣的设计概念——role-based side content chapters，但其与现有模式的区分不够清晰，存在以下问题：

#### 遗漏 1: Profession chapter 与 side chapter 的操作性区分标准缺失

MP38 的描述是 "multiple playstyle paths (combat, farming, mining, research) and the author wants to give each role dedicated quest content." 但 "side chapter" 是一个更广泛的概念——任何 non-main-progression chapter 都是 side content。MP38 需要回答：一个 combat-themed side chapter 和一个 "Hunter profession chapter" 的区别是什么？

从 TheWinterRescue 的数据来看，profession chapters 的特征是：
- **平行结构:** 9 个 profession chapter 同时可用（无先后顺序）
- **主题一致性:** 每个 chapter 严格围绕一个 role
- **命名模式:** "A Day of [Profession]" 的统一命名

但这些特征也适用于任何 well-organized side content。缺少的是：profession chapter 独有的**结构性**特征——例如，profession chapters 是否与 main tier chapters 有特定的 dependency 关系？是否共享 reward economy？是否有 cross-profession 的 convergence point？

**严重性:** 中。如果 profession chapter 只是 "well-themed side chapter" 的同义词，MP38 作为独立模式的必要性值得质疑。

**建议:** MP38 需要明确 profession chapter 的操作性定义。建议添加："A profession chapter is distinguished from generic side content by three criteria: (1) **Parallel availability** — all profession chapters are simultaneously accessible from the same tier point; (2) **Role exclusivity** — each chapter's tasks are thematically restricted to one playstyle (no cross-role content); (3) **Optional by design** — profession chapters never gate main progression (R7 Optional-Gate-Mandatory applies in reverse: main progression must never depend on profession chapters)." 如果无法满足这三条，则该 chapter 是 generic side content 而非 profession chapter。

#### 遗漏 2: Profession chapter 之间的 cross-dependency 未讨论

TheWinterRescue 有 9 个 profession chapter。如果 "Miner" profession 的某个 quest 需要 "Fuel Engineer" profession 产出的物品，就产生了 cross-profession dependency。这与 profession chapter 的 "role exclusivity" 原则矛盾。

MP38 没有说明 profession chapters 之间是否应该有 dependencies，也没有讨论如果出现 cross-profession item dependency 应该如何处理。

**严重性:** 低-中。TheWinterRescue 的数据中未观察到 cross-profession dependencies（每个 chapter 3 types: item, checkmark, frostedheart:insight），但这是一个潜在的设计陷阱。

**建议:** MP38 Design considerations 增加一条："(5) Avoid cross-profession dependencies — each profession chapter should be completable independently. If two professions need the same item, provide it as a reward in both chapters or source it from the main progression, not from another profession chapter."

#### 遗漏 3: Profession chapter 与 main progression 的 reward economy 平衡

如果 profession chapters给予比 main progression 更好的 reward（因为它们是 side content，author 可能倾向于给更好的 reward 来吸引玩家），AP8 (Reward Inflation) 风险增加。如果 profession chapter 的 reward 太弱，玩家没有动力去做。

MP38 Design consideration (3) 说 "Reward profession chapters with role-specific tools or materials, not generic items"，但没有讨论 reward value 的平衡。一个 "Hunter" profession chapter 如果 reward 一把比 main progression 同期 weapon 更强的 bow，main progression 的 combat quests 就被 trivialized。

**严重性:** 低。这是 reward economy 的通用平衡问题，不特定于 profession chapters。但 MP38 应该至少提及这个风险。

**建议:** MP38 Design considerations 修改 (3) 为："Reward profession chapters with role-specific tools or materials. Calibrate reward value against main progression at the same tier — profession rewards should complement, not outshine, main progression rewards (see R12 Reward Value Progression)."

#### 遗漏 4: Single-source 风险与推广性

MP38 仅有 TheWinterRescue 一个数据点。9 个 profession chapters 是 TWR 的设计选择，可能反映的是 TWR author 的偏好而非 FTB Quests 的通用设计模式。其他 expert/survival 包（如 Enigmatica 系列、Monifactory）不使用 profession chapters——它们通过 chapter-per-mod 或 chapter-per-voltage-tier 来组织内容。

**严重性:** 低。Single-source 标注已在文档中标明。但 MP38 的 pack_types 标注为 `expert, story`——如果只有一个 expert 包使用，`story` 标注缺乏数据支撑。

**建议:** 将 pack_types 修正为 `expert`（移除 `story`），直到有 story/RPG 包使用 profession chapters 的证据。标注 "single-source (TheWinterRescue only)" 已足够，但 pack_types 应与数据一致。

---

### 五、Draft R36 -- Hardcore Zero-Optional

#### 完备性评级: C (关键反例已存在但未被充分处理)

#### 遗漏 1: Prominence II 反例的处理不足

Draft R36 文档自身已识别了反例："Some combat packs (Prominence II) use optional content for side activities." 但 draft rule 仍然表述为 "For packs classified as `hardcore` or `combat`, flag `optional: true` quests as INFO."

问题在于：Prominence II 是一个 RPG 包，拥有 7 task types（包括 kill, dimension, biome 等），其 optional content 是有意设计的 side activities（fishing, farming, exploration）——这些不是 combat 内容，也不应该被 flag。Draft R36 的 rule 如果实施，会对 Prominence II 的所有 optional quest 产生 false positive。

R36 的核心假设——"hardcore/combat packs enforce zero optionality"——被 Prominence II 证伪。更准确的表述应该是："**Pure combat hardcore** packs（如 NFwC, Era of Black Death）趋向 zero optionality，而 **hybrid RPG/combat** packs（如 Prominence II）正常使用 optional content。"

**严重性:** 高。Draft rule 如果按当前表述实施，会对 hybrid packs 产生系统性 false positive。

**建议:** (1) 将 R36 的 pack classification 从 `hardcore, combat` 细化为 `hardcore-pure` (纯 combat，无 side activities) vs `hardcore-hybrid` (combat + side activities)。仅对 `hardcore-pure` flag optional quests。(2) 或者更保守地，将 R36 降级为 "observation" 而非 "draft rule"——2 个数据点（NFwC, Era of Black Death）不足以支撑即使是 INFO 级别的自动化规则。(3) 明确列出 verification packs: RLCraft, DawnCraft, Vault Hunters 3 的数据需要在此 rule 被 promotion 前获取。

#### 遗漏 2: "Optional" 的多重语义未区分

R36 的 rule flag `optional: true` quests，但 "optional" 在不同包中有不同的语义：

1. **True side content optional:** 完全可选的 side activity（Prominence II 的 fishing quests）——flag 为 INFO 合理
2. **Difficulty-variant optional:** 同一目标的多种路径，其中一条标记为 optional（alternative easy mode）——flag 可能不合理
3. **Placeholder optional:** 未完成的 quest 标记为 optional 等待后续更新——这是 AP3 的缓解策略，flag 合理
4. **Completion-tracking optional:** 标记为 optional 以从 completion percentage 中排除（MP37 的正确实现）——flag 不合理

R36 不区分这四种 optional 语义，对所有 `optional: true` 一视同仁地 flag。

**严重性:** 中。即使对 hardcore-pure packs，flagging completion-tracking optionals（type 4）也会产生 noise。

**建议:** 如果 R36 被 promotion，增加 optional 分类启发式："When flagging optional quests in hardcore packs, classify them: (a) independent island with no dependents = likely side content; (b) has dependents = likely placeholder or variant; (c) progress catalog quest = intentional exclusion. Only flag type (a) as INFO."

#### 遗漏 3: Zero-optional 与 R7 (Optional-Gate-Mandatory) 的交互

R7 检查 mandatory quest 是否依赖 optional quest——这是所有包类型都适用的 P0/P1 规则。如果一个 hardcore pack 确实实现了 zero-optional（NFwC 已确认），则 R7 对该包永远不触发——因为没有 optional quest 可以 gate mandatory quest。

这本身不是问题，但意味着 R7 对 zero-optional packs 的检测价值为零。如果 R36 的 rule 被实施，它与 R7 在 hardcore packs 上的关系是：R36 确保 zero-optional 状态，R7 因为 zero-optional 而不需要工作。两者不冲突，但 R36 的存在使得 R7 对这类包变得冗余。

**严重性:** 低。这是观察性笔记，不影响功能。

**建议:** 在 R36 的文档中注明："In zero-optional hardcore packs, R7 (Optional-Gate-Mandatory) is structurally inapplicable — there are no optional quests to gate mandatory content."

---

### 六、Draft R37 -- Kill Task Density

#### 完备性评级: C (核心遗漏——boss vs mob 的 kill density 本质不同)

#### 遗漏 1: Boss kill vs mob grind 的密度等价性——最关键的遗漏

R37 的 calibration 将所有 kill tasks 视为等同：`kill_tasks / total_quests`。但 kill task 的设计意图和玩家时间投入因 entity type 而有本质差异：

| Kill type | 示例 | 单次时间 | 重复性 | 设计意图 |
|---|---|---|---|---|
| **Boss kill** | Wither, Ender Dragon, mod bosses | 5-30 min | 一次性 skill check | 进度里程碑 |
| **Elite kill** | Named mobs, mini-bosses | 2-5 min | 低重复 | 装备检查 |
| **Mob grind** | Zombies, Skeletons, Spiders | 30s-2 min/kill | 高重复 (kill 50) | 资源 farming |
| **Swarm kill** | Bee swarms, slime chunks | 1-5 min | 中等 | 区域清理 |

NFwC boss chapter 的 65% kill density（38/58 quests）是 **38 个独立 boss fights**——每个都是独特的 skill check，提供不同的战斗体验。如果另一个 chapter 也有 65% kill density 但全部是 "kill 50 zombies" × 38 quests，玩家的体验是无尽的 grinding 而非 boss progression。

R37 的 density metric 将这两种完全不同的体验视为等价，这导致 metric 的解释力大幅下降。

**严重性:** 高。Boss kill density 和 mob grind density 对玩家体验的影响截然不同，将它们合并为一个 metric 产生误导。

**建议:** R37 应区分两种 kill density：(1) **Boss kill density**: kill tasks with `value: 1` (one kill of a unique/boss entity) — high density (30-65%) is acceptable because each fight is a unique experience. (2) **Grind kill density**: kill tasks with `value >= 5` (multiple kills of common mobs) — high density (>20%) in a single chapter indicates excessive grinding. 实现方式：检查 kill task 的 `entity` 字段是否匹配已知 boss entity 列表，或检查 `value` 字段（`value: 1` = boss, `value >= 5` = grind）。

#### 遗漏 2: Kill density calibration 的 chapter-level vs book-level 区分

R37 的 calibration 按 chapter 独立计算密度。但考虑以下场景：

- Chapter A (Boss Rush): 10 quests, 8 kill tasks = 80% density
- Chapter B (Boss Rush 2): 10 quests, 8 kill tasks = 80% density
- Chapter C (Boss Rush 3): 10 quests, 8 kill tasks = 80% density

每个 chapter 的 density 都在 hardcore 范围（30-65%）之上。但如果这三个 chapter 是连续的（order_index 相邻），玩家面临 24 个连续 boss fight 而没有任何 crafting/exploration 间歇——这是 R19 (Bottleneck Spacing) 的 kill-task 变体。

R37 只关注单 chapter 密度，不关注连续 kill-heavy chapters 的累积效应。

**严重性:** 中。连续高 kill density chapters 会产生 "combat fatigue"——玩家连续数小时只做战斗，缺乏 variety。

**建议:** R37 增加 book-level analysis："When 2+ consecutive chapters (by order_index) each exceed 30% kill density, flag as INFO: 'Consecutive kill-heavy chapters detected — consider interleaving non-combat content for variety.' This complements R19 (Bottleneck Spacing) at the chapter level."

#### 遗漏 3: Expert/Create packs 的 "0% kill density" 过于绝对

R37 对 Expert/Create packs 给出的范围是 "0% kill density"。但 Create 包可能有少量 kill tasks 用于特定目的：

- Create: Astral 有 6-7 task types，可能包含 kill tasks（数据中未明确排除）
- Finality Genesis（Create + adventure + RPG）有 9+ task types 包括 kill tasks
- Era of Black Death（Combat + RPG）有 kill tasks 但被分类为 RPG

"0%" 作为 guideline 过于绝对。更准确的表述是 "0-2% — kill tasks are exceptional and used only for specific mod-integration moments (e.g. 'defeat a mob using Create weapons')."

**严重性:** 低。Guideline 的过度严格不会导致 false positive 在实际中造成问题（expert packs 确实很少使用 kill tasks），但措辞应该准确。

**建议:** 将 Expert/Create 的范围修改为 "0-2% — exceptional only." 并增加注释："Create-focused packs may use kill tasks to demonstrate Create weapon effectiveness or mob farm automation — these are teaching moments, not combat progression."

#### 遗漏 4: Kill task 的 reward 经济未被纳入 density calibration

R37 只计算 kill task 的数量比例，不考虑 kill task 的 reward 经济影响。NFwC boss chapter 的 38 kill tasks 伴随 42 lightmanscurrency references——每个 boss kill 都给 currency reward，player 通过 boss grinding 积累货币。如果 kill density 高且 reward 丰富，boss grinding 可能成为最优化策略，trivialize 其他获取 currency 的方式。

这与 MP36 (Currency-as-Reward) 和 AP8 (Reward Inflation) 交叉：high kill density + currency reward = 潜在的 economy-breaking grind loop。

**严重性:** 低-中。这是 kill density 与 reward economy 的交互效应，R37 作为纯 structural metric 不需要完全覆盖 reward economy，但应该标注交叉风险。

**建议:** R37 Design considerations 增加一条交叉引用："High kill density combined with currency rewards (MP36) can create an economy-breaking grind loop. Cross-check with R12 (Reward Value Progression) and AP8 (Reward Inflation) when kill density exceeds 30% and currency rewards are present."

---

### 七、跨模式/跨规则交互检查

以下是 Cycle 5 新增模式与现有模式/规则的潜在冲突或重叠：

| 模式/规则对 | 关系 | 分析 |
|---|---|---|
| MP35 vs B5 (consume_items 通用语义) | 部分覆盖 | MP35 解决了 `consume_items: false` 的 automation 特化场景，但 B5 的 `consume_items: true` 风险和 resource-sink 漏洞仍未覆盖。MP35 不应被视为 B5 的解决方案。 |
| MP35 vs MP27/MP28 (Fluid/Energy Gate) | 未交叉 | MP27/MP28 描述 fluid/energy task 的设计原则，MP35 描述 automation 验证。两者的交叉（fluid/energy automation verification）完全空白。 |
| MP36 vs R10 (Reward-to-Dependent Bridge) | 冲突 | R10 的 currency 排除依赖 item reward type 识别，但 MP36 的 currency 是 `type: "item"` — 无法从 type 字段区分 currency 和 material bridge。 |
| MP36 vs AP8 (Reward Inflation) | 未交叉 | AP8 聚焦 item reward 的时间分布，不覆盖 currency reward 的通胀问题。Currency inflation 是 AP8 的 currency 变体。 |
| MP37 vs PP4 (Completionist's Dilemma) | 潜在冲突 | MP37 catalog quest 如果不设 `optional: true`，直接触发 PP4。这是本次审查中严重性最高的单点遗漏。 |
| MP37 vs R18 (Description Coverage) | 未交叉 | R18 的 catalog-cell 豁免可能不覆盖 MP37 catalog quest（shape/size 条件可能不匹配）。 |
| MP37 vs R20 (Chapter Completion Testability) | 间接关联 | Non-optional MP37 catalog quest 会被 R20 检查可达性。如果 item 不可达，R20 ERROR。 |
| MP38 vs R7 (Optional-Gate-Mandatory) | 互补 | R7 防止 mandatory 依赖 optional。MP38 的 profession chapters 必须是 optional 且不 gate main progression — R7 的 reverse application。 |
| R36 vs R7 (Optional-Gate-Mandatory) | 冗余 | Zero-optional packs 中 R7 结构性不适用。 |
| R37 vs R19 (Bottleneck Spacing) | 未交叉 | R19 检测 consecutive bottleneck quests，但不特化 kill tasks。Consecutive kill-heavy chapters 是 R19 的 kill-task 变体。 |

---

### 八、遗漏的全局维度

#### 1. MP35-38 的 single-source 风险汇总

| 模式 | 数据源 | 验证状态 | 建议 |
|---|---|---|---|
| MP35 Dual-Task Automation | Cabricality only | Single-source | 维持 single-source 标注。验证需要 Create: Above and Beyond config。 |
| MP36 Currency-as-Reward | GT-O + NFwC (TWR variant) | Multi-source (2+1) | 可升级为 multi-source。Standard currency (GT-O, NFwC) 充分验证。 |
| MP37 Progress Catalog | GT-O only | Single-source | 维持 single-source。这是一个 niche 模式，适用范围窄。 |
| MP38 Profession Chapter | TWR only | Single-source | 维持 single-source。pack_types 应从 `expert, story` 修正为 `expert` only。 |

#### 2. Cycle 5 模式与 Step 2/Step 4 的映射

| 模式 | 当前 Phase | 建议 Phase | 分析 |
|---|---|---|---|
| MP35 | Step 4 (node generation) | Step 4 | 正确——dual-task 是 per-quest 决策 |
| MP36 | Step 4 (node generation) | Step 4 | 正确——currency reward 是 per-quest 决策 |
| MP37 | Step 2 (chapter design) | Step 2 | 正确——catalog chapter 是 chapter-level 决策 |
| MP38 | Step 2 (chapter design) | Step 2 | 正确——profession chapter 是 chapter-level 决策 |

#### 3. Cycle 5 模式的 Scope Annotation Table 更新建议

当前 micro-patterns.archive.md 的 Scope Annotation Table 止于 MP34。MP35-38 需要添加：

| Pattern | pack_types | Phase | Source confidence |
|---|---|---|---|
| MP35 Dual-Task Automation | create, expert | Step 4 | Low (Cabricality only, single-source) |
| MP36 Currency-as-Reward | expert, hardcore, rpg | Step 4 | Medium (GT-O + NFwC multi-source, TWR variant) |
| MP37 Progress Catalog | expert | Step 2 | Low (GT-O only, single-source) |
| MP38 Profession Chapter | expert | Step 2 | Low (TWR only, single-source) |

---

### 九、总结

| 审查项 | 评级 | 遗漏数 | 最高严重遗漏 |
|---|---|---|---|
| MP35 -- Dual-Task Automation | **B** | 4 | Fluid/energy automation 验证完全缺失（scope 限定不足） |
| MP36 -- Currency-as-Reward | **B** | 4 | Currency inflation 无量化框架（定性建议不足以指导校准） |
| MP37 -- Progress Catalog | **C** | 4 | `optional: true` 未标注为 mandatory（直接触发 PP4） |
| MP38 -- Profession Chapter | **C** | 4 | 与 generic side chapter 的操作性区分标准缺失 |
| Draft R36 -- Hardcore Zero-Optional | **C** | 3 | Prominence II 反例处理不足（hybrid packs false positive） |
| Draft R37 -- Kill Task Density | **C** | 4 | Boss kill vs mob grind 的 density 等价性（metric 解释力不足） |

**最高优先级行动 (按严重性排序):**

1. **MP37 增加 `optional: true` 作为 mandatory field** -- 这是唯一的 HIGH 严重性遗漏。MP37 catalog quest 如果不设 optional，直接触发 PP4 (Completionist's Dilemma)，使 progress tracker chapter 变成一个持续的 "未完成" 指示器。修复成本极低（一行文档修改），影响面大。

2. **R37 区分 boss kill density 和 mob grind density** -- HIGH 严重性。不区分的 metric 会产生根本性误导：38 个 boss fights (NFwC) 和 38 个 "kill 50 zombies" quests 对玩家体验完全不同。建议通过 `value` 字段区分（`value: 1` = boss, `value >= 5` = grind）。

3. **R36 细化 pack classification 或降级为 observation** -- MEDIUM-HIGH 严重性。当前 "hardcore or combat" 分类会误 flag hybrid packs (Prominence II)。2 个数据点不足以支撑自动化规则。

4. **R10 增加 currency item 识别机制** -- MEDIUM 严重性。MP36 的 currency reward 是 `type: "item"`，R10 无法区分 currency 和 material bridge，导致 false positive。

5. **MP35 增加 fluid/energy extension variants** -- MEDIUM 严重性。当前 scope 暗示更广泛适用性但仅覆盖 item task。明确限定或扩展。

6. **MP36 增加 currency inflation 量化框架** -- MEDIUM 严重性。定性建议 "calibrate against shop prices" 不足以指导实际校准。需要 total output vs total sink cost 的比较框架。

7. **MP38 明确操作性定义和 pack_types 修正** -- LOW-MEDIUM 严重性。与 generic side chapter 的区分需要三条操作性标准。pack_types 中 `story` 缺乏数据支撑。
