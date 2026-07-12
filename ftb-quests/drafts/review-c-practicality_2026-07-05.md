# 审查报告 C — 实用性审查

**审查员：** C（实用性审查员）
**日期：** 2026-07-05
**审查对象：** micro-patterns.md、anti-patterns.md、progression-rules.md
**审查角度：** AI 在 Step 4（逐节点生成）时能否实际使用这些模式和规则

---

## 一、核心发现：外部数据依赖是最大瓶颈

三份文档中存在一个系统性的实用性问题：**大量规则和模式依赖 AI 无法自行获取的外部数据**。这些数据来自 JEI/EMI 配方系统、mod 源码、或用户的整合包设计意图——而 AI 在 Step 4 的执行上下文中均无法访问。

以下逐条列出受影响的规则/模式及其降级策略的合理性评估。

---

## 二、逐条质疑

### 质疑 1：R1 Dimension-Reachability 需要 item_dimension_map，但该映射表不存在

- **涉及规则：** R1（Dimension-Reachability Check）
- **实用性问题：** 伪代码引用了 `item_dimension_map`——将每个物品映射到其唯一可获取维度。文档建议"由用户在 Step 2 定义，或从包的 recipe 数据推断"。但：
  1. Step 2 的 interview 流程（见 SKILL.md）没有收集此映射的环节——Step 2 收集的是主题、mod 列表、章节结构、奖励哲学。
  2. "从包的 recipe 数据推断"需要解析 JEI/EMI 配方——AI 没有此能力。
  3. 没有此映射，R1 的伪代码完全无法执行。
- **建议改进：**
  1. 在 Step 2 增加一个"维度物品清单"收集环节，让用户提供每个维度的标志性物品（10-20 个即可，不需要穷举）。
  2. 或将 R1 降级为仅检查已知维度物品（如 `minecraft:blaze_rod` → Nether 这类硬编码常识），对未知物品标记 `[unverified:dimension]` 并跳过。
  3. 提供一个可增量构建的 `item_dimension_map.json5` 模板，让 cache 系统（`.ftbq-cache/`）在 Step 1 时预填常见维度物品。

### 质疑 2：R2 Tool-Tier Item Reachability 需要 tool_requirement_map，来源不明

- **涉及规则：** R2（Tool-Tier Item Reachability）
- **实用性问题：** 伪代码引用 `tool_requirement_map`（每个物品的最低采集工具等级 / 最低加工机器等级）。文档坦承"需要从 JEI/EMI recipe 数据推断，或由用户在 Step 2 提供"，并说"如果映射缺失，规则跳过该物品并标记 `[unverified:tool_tier]`"。但：
  1. 降级策略导致绝大多数物品被跳过——在一个有 200+ mod 的 kitchen-sink 包中，可能 95% 的物品都没有映射数据。R2 实质上成为空设规则。
  2. mining level 数据理论上可从 mod 的 block tag 推断（`minecraft:needs_iron_tool` 等），但文档未提及此可行路径。
- **建议改进：**
  1. 增加一个 `extract_tool_tiers.py` 脚本（或扩展现有 `extract_items.py`），从 mod jar 的 block tags 和 item tags 推断 mining level 和 machine tier。
  2. 对无法推断的物品，降级为 INFO 而非跳过——告知用户"此物品的工具需求未验证"比静默跳过更有用。

### 质疑 3：R3 Recipe-Chain Depth 需要 recipe_chain_depth，完全不可获取

- **涉及规则：** R3（Recipe-Chain Depth vs Dependency-Depth）
- **实用性问题：** 这是最严重的数据依赖问题。`recipe_chain_depth` 需要递归展开每个物品的完整合成树并计算最大深度——这是 JEI/EMI 的核心功能，AI 完全无法做到。文档说"对于没有 recipe 数据的物品，规则跳过并标记 `[unverified:recipe_depth]`"。但在实际使用中，**几乎所有非 vanilla 物品都没有 recipe 数据**，导致 R3 几乎永远处于跳过状态。
  1. `ALLOWANCE` 的默认值 2 是凭空设定的——对于 expert pack（合成链深度可达 15+），余量 2 毫无意义。
  2. 即使有部分数据，"quest 依赖链应该至少和物品合成链一样长"这个核心假设在 kitchen-sink 包中不成立——ATM-10 的 `flexible` 模式下 quest chain 可以很短。
- **建议改进：**
  1. 将 R3 从"自动执行的检查规则"降级为"Step 2 interview 中的设计讨论点"——让 AI 和用户讨论关键物品的合成深度，而非试图自动检测。
  2. 或者提供一个 recipe-depth 的粗估 heuristic：物品 tier（从 mod namespace + 物品名称推断）→ 粗估深度（basic=1, advanced=3, elite=5, endgame=8）。这比没有数据好。

### 质疑 4：R4 Pack-Type Stage Boundary 需要 item_stage_map，定义缺失

- **涉及规则：** R4（Pack-Type Stage Boundary）
- **实用性问题：** 伪代码引用 `item_stage_map` 和 `stage_definition`，需要用户在 Step 2 提供。但 Step 2 的 interview 流程不包含收集阶段物品映射的环节。四种包类型的 stage 逻辑描述得很清楚（kitchen-sink / expert / skyblock / RPG），但没有可执行的数据源。
- **建议改进：**
  1. 在 Step 2 的 Structure 分支中增加一个"阶段分界"子问题，让用户定义每个 chapter/chapter group 对应的阶段编号。
  2. 物品的阶段归属可以用 heuristic 推断：物品所在的 chapter → 该 chapter 的阶段。对跨 chapter 引用的物品做交叉检查即可，无需穷举映射。

### 质疑 5：R11 Reward-Target Accuracy 需要 NLP 解析 description

- **涉及规则：** R11（Reward-Target Accuracy / Wrong Tool Detection）
- **实用性问题：** 伪代码中有 `extract_tool_from_description(dep_quest.description)` 和 `tool_category_map`。两个问题：
  1. `tool_category_map`（所有 wrench 的跨 mod 列表）需要人工维护或从 mod 数据推断——没有现成来源。
  2. `extract_tool_from_description` 是一个自然语言处理函数——description 是自由文本，AI 需要从"用 Oritech wrench 连接管道"中提取出"需要 oritech:wrench"。这在 AI 生成 description 时是可行的（因为 AI 知道自己写了什么），但在检查其他 quest 的 description 时不可靠。
- **建议改进：**
  1. 用结构化标注替代 NLP：在 spec 中为每个 quest 增加一个可选的 `required_tools: ["oritech:wrench"]` 字段，AI 生成时自动填入，检查时直接读取。
  2. `tool_category_map` 可以硬编码 5-10 个常见工具类别（wrench、hammer、guide_book），覆盖 90% 的场景。

### 质疑 6：R12/R13 Reward Value 需要 estimate_value，定价模型不存在

- **涉及规则：** R12（Reward Value Progression）、R13（Capstone Reward Magnitude）
- **实用性问题：** `estimate_value(r)` 是伪代码中的核心函数，但文档只说"简单模型：物品 rarity × count。复杂模型：从 mod 的 tier 数据推断"。没有一个可执行的价值评估模型。
  1. 不同 mod 的物品价值不可比较——1 个 Mekanism 的 osmium ingot 和 1 个 AE2 的 fluix crystal 价值完全不同，但没有统一的定价标准。
  2. R13 的"capstone 价值应 ≥ 3x chapter 平均"这个阈值在没有准确定价的情况下会产生大量 false positive/negative。
- **建议改进：**
  1. 提供一个粗粒度的价值 tier 表（common=1, uncommon=5, rare=20, epic=100），由 AI 在生成 reward 时标注每个 reward 的 tier。R12/R13 基于标注而非推断运行。
  2. 或者将 R12/R13 降级为 INFO 级别的 heuristic 提醒，不做硬检查。

### 质疑 7：R14 Teach-Then-Do 的 find_related_teaching 匹配逻辑不明确

- **涉及规则：** R14（Teach-Then-Do Ordering）
- **实用性问题：** 伪代码中 `find_related_teaching(doing_quest, teaching_quests)` 的"Related"判定有三条：(1) 同 mod namespace、(2) description 提到 task item、(3) 依赖链相邻。这三条的优先级和组合逻辑未定义。
  1. 条件 (1) 太宽泛——一个 Mekanism chapter 中可能有 20 个 teaching quest 和 50 个 doing quest，全部同 namespace。
  2. 条件 (2) 又是 NLP 问题。
  3. 条件 (3) 要求 teaching quest 已经是 doing quest 的祖先——如果已经是祖先，顺序本来就正确，不需要检查。如果不是祖先，则条件 (3) 不成立。这导致条件 (3) 只在不需要检查时成立。
- **建议改进：**
  1. 简化匹配逻辑：只检查同 chapter 内的 teaching quest 和 doing quest 是否满足 dependency_depth(teaching) < dependency_depth(doing)，不做精细匹配。如果 chapter 内所有 teaching quest 都在所有 doing quest 之前（按 depth），则通过；否则 warning。
  2. 或者在 spec 中增加 `teaches: ["doing_quest_name"]` 标注，让 AI 在 Step 4 生成时建立显式关联。

### 质疑 8：R15 Complexity Escalation 的复杂度公式过于粗糙

- **涉及规则：** R15（Complexity Escalation Within Chapter）
- **实用性问题：** `estimate_complexity(task) = recipe_depth * log(count + 1)`。两个问题：
  1. `recipe_depth` 再次需要外部数据（同 R3）。
  2. 即使忽略 recipe_depth，只用 count，"64 个铁锭比 1 个铁锭复杂"这个假设在 quest 设计语境中不总是成立——收集 64 个铁锭可能只是一个 grind 步骤，而合成 1 个 control circuit 是真正的复杂度。
- **建议改进：**
  1. 将复杂度估算简化为可观测指标：task count（多 task = 复杂）、item count（高 count = grind 但不是复杂）、quest dependency depth（深 = 后期 = 预期更复杂）。不需要 recipe_depth。
  2. 将阈值从 `0.3` 改为更宽松的值，或将此规则固定为 INFO 级别。

### 质疑 9：R17 Tool-Reward-Before-Use 的 is_tool() 判定不明确

- **涉及规则：** R17（Tool-Reward-Before-Use Ordering）
- **实用性问题：** 伪代码中 `is_tool(r.item.id)` 没有定义。什么算"工具"？在 Minecraft 中，pickaxe 是工具，但 Mekanism 的 metallurgic infuser 呢？AE2 的 charger 呢？Patchouli guide book 呢？
  1. 如果 is_tool 只覆盖 vanilla 工具（pickaxe、axe、hoe、shovel），覆盖率太低。
  2. 如果扩大到所有"耐久物品"，false positive 太高。
- **建议改进：**
  1. 提供一个硬编码的常见工具 ID 列表（50-100 个），涵盖 vanilla + 常见 mod 工具。
  2. 或者在 spec 中标注 `reward_is_tool: true`，让 AI 生成时自行标记。

### 质疑 10：MP24 Tier-Reachability Check 和 MP26 Reward-Continuity Check 是检测信号而非可执行规则

- **涉及模式：** MP24、MP25、MP26
- **实用性问题：** 这三个 micro-pattern 被描述为"Anti-Pattern Detection Signals"，但它们的检测逻辑依赖与 R1-R3 相同的外部数据。MP24 说"trace the item's crafting recipe (from JEI/EMI or the mod's recipe data)"——AI 做不到。MP26 说"check if any of its rewards appear as task items in any of its dependent quests"——这个可行，但只是 R10 的重复。
  1. MP24/MP25/MP26 和 R1-R22 之间存在大量内容重叠，但 MP 版本更模糊、R 版本更具体。AI 应该参考哪个？
- **建议改进：**
  1. 明确 MP24/MP25/MP26 的定位：它们是 anti-patterns.md 和 progression-rules.md 之间的桥梁概念，不应被 AI 直接执行。AI 应直接参考 R1-R22。
  2. 在 micro-patterns.md 中为 MP24/MP25/MP26 添加明确的指引："此检测信号在 progression-rules.md 中已有对应的可执行规则（R1/R14/R10），请参考后者。"

### 质疑 11：PP2 Backward Shortcut 过于抽象，AI 无法在逐节点生成时应用

- **涉及模式：** PP2（The Backward Shortcut）
- **实用性问题：** PP2 说"在 milestone quest 的 reward 中包含一个 efficiency loop back to earlier content"——例如给一个自动化早期手动流程的机器。这个建议在战略层面是正确的，但在 Step 4 逐节点生成时：
  1. AI 需要知道"之前的哪些内容可以被优化"——这需要回顾已完成的所有 quest。
  2. AI 需要知道"什么物品/机器可以优化之前的流程"——这需要 mod 机制知识。
  3. 即使知道了这两点，AI 还需要确认该优化物品在当前阶段可获得。
- **建议改进：**
  1. 将 PP2 从"逐节点设计规则"重新定位为"Step 2 战略设计原则"——在规划 milestone quest 时考虑 backward shortcut，而非在生成每个节点时检查。
  2. 在 Step 2 的 outline 中标注哪些节点是 milestone，并在 milestone 节点的 reward 设计时提示 AI 考虑 backward shortcut。

### 质疑 12：micro-patterns.md 的 Part 1-3 混合了节点级和章节级决策

- **涉及模式：** MP1-MP13 整体
- **实用性问题：** micro-patterns.md 的 Part 1（Task Combination）、Part 2（Dependency Topology）、Part 3（Quest-Internal Pacing）混合了两种不同粒度的决策：
  1. **节点级**（MP1 Single-Item Gate、MP2 Multi-Item Synthesis、MP3 Acknowledgement Gate）：AI 在 Step 4 设计单个 quest 的 task 时可以直接使用。
  2. **章节级**（MP6 Linear Chain、MP7 Fan-Out、MP8 Fan-In、MP12 Tier Escalation）：这些需要在 Step 2 outline 阶段就决定，Step 4 逐节点生成时已无法改变。
  3. AI 在 Step 4 加载 micro-patterns.md 时，会被章节级模式分散注意力，而真正需要的节点级模式被淹没在大量文本中。
- **建议改进：**
  1. 将 micro-patterns.md 拆分为两个文件：`node-patterns.md`（MP1-MP5、MP14-MP18——Step 4 使用）和 `chapter-patterns.md`（MP6-MP13、MP19-MP23——Step 2 使用）。
  2. 或在每个 pattern 头部添加明确的 "Phase" 标签：`Phase: Step 2 (outline)` 或 `Phase: Step 4 (node generation)`。
  3. 在 SKILL.md 的 Step 4 指引中明确引用 node-patterns 而非整个 micro-patterns.md。

### 质疑 13：anti-patterns.md 是面向人类的设计文档，AI 无法直接执行

- **涉及规则：** AP1-AP8 全部
- **实用性问题：** anti-patterns.md 的定位是"错误 + 后果"的人类可读描述，文档自己也承认这一点（"anti-patterns.md 是 WHY，progression-rules.md 是 HOW"）。但从 AI 实用性的角度：
  1. AP1（Description-Reality Mismatch）完全没有对应的 progression-rule——文档明确说"不在本规则集中——description 内容验证需要运行时"。这意味着 AP1 这个"最严重的 anti-pattern"在 AI 的自动检查中完全不可覆盖。AI 在 Step 4 生成 description 时只能靠"绝不脑补"原则（SKILL.md 的 ABSOLUTE RULE）来预防，但无法自动检测。
  2. AP2-AP8 都有对应的 R 规则，但 AP 文档本身不包含可执行逻辑——AI 需要同时参考两份文档。
- **建议改进：**
  1. 为 AP1 增加一个弱化的静态检查：R23 — Description-Item Consistency Check——检查 description 中提到的物品 ID（用正则提取 `<modid>:<name>` 格式）是否存在于 `items.json5` 的 `all_item_ids` 中。这无法捕获"描述说 Shadowflame Goo 但任务要 Shadowpulse Goo"（因为两者可能都是有效 ID），但至少能捕获"描述引用了不存在的物品"。
  2. 在 SKILL.md 中明确 AI 在 Step 4 的参考文档优先级：progression-rules.md > micro-patterns.md（node-level）> anti-patterns.md。anti-patterns.md 作为背景知识在 Step 2 加载一次即可。

### 质疑 14：R21 Hidden Quest Signpost 的 mentions_unlock 不可靠

- **涉及规则：** R21（Hidden Quest Signpost）
- **实用性问题：** `mentions_unlock(dep.description)` 需要检测 description 中是否有"unlocks""opens""reveals"等措辞。这是另一个 NLP 问题：
  1. 多语言环境下，中文 description 用"解锁""开启""揭示"——关键词列表需要覆盖多语言。
  2. 即使关键词匹配，语义也不确定——"这个 quest 不会解锁任何新内容"也包含"解锁"。
- **建议改进：**
  1. 用结构化标注替代 NLP：在 spec 中增加 `signpost_for: ["hidden_quest_name"]` 字段，AI 在生成 visible quest 时标注它引导哪些 hidden quest。
  2. 或简化为：如果 hidden quest 的 dependency 是 visible 且 non-secret 的，就视为有 signpost（dependency 本身就是 signpost）。不检查 description 内容。

### 质疑 15：三份文档的总体积过大，按需加载边界不清晰

- **涉及文档：** 全部三份
- **实用性问题：** micro-patterns.md（540 行）+ anti-patterns.md（200 行）+ progression-rules.md（860 行）= 约 1600 行。AI 在 Step 4 的 context window 已经很紧张（需要容纳 SKILL.md 主体 + spec 数据 + 用户对话），一次性加载三份文档会消耗大量 token。
  1. SKILL.md 已有按需加载的指引（"Load it when you need..."），但 micro-patterns.md 和 progression-rules.md 没有被 SKILL.md 明确引用为"Step 4 加载"还是"Step 2 加载"。
  2. progression-rules.md 是 Step 5（整体验证）使用的，不是 Step 4 使用的——但文档没有明确说明。
- **建议改进：**
  1. 在 SKILL.md 的 Protocol 部分增加明确的文档加载表：
     - Step 2：design-guide.md §principles、micro-patterns.md Part 2+5（chapter-level）、anti-patterns.md（背景知识）
     - Step 4：micro-patterns.md Part 1+4（node-level）、design-guide.md §writing-style
     - Step 5：progression-rules.md（全部）、anti-patterns.md（对照检查）
  2. 或在每份文档头部添加 "Load phase" 标注。

---

## 三、伪代码可直接实现性评估

对 progression-rules.md 中 22 条规则的伪代码，按"可直接实现 / 需少量补充 / 需大量工作 / 不可执行"四级评估：

| 可直接实现（仅依赖 quest 图数据） | 需少量补充（需要硬编码表或简单 heuristic） | 需大量工作（需要外部数据源） | 不可执行（需要 NLP 或 JEI/EMI） |
|---|---|---|---|
| R5 Circular Dependency | R8 Dep Requirement Consistency | R1 Dimension-Reachability | R11 extract_tool_from_description |
| R6 Unreachable Quest | R9 Depth Reasonableness | R2 Tool-Tier Reachability | R14 find_related_teaching |
| R7 Optional-Gate-Mandatory | R18 Description Coverage | R3 Recipe-Chain Depth | R21 mentions_unlock |
| R20 Chapter Completion | R22 Cross-Chapter Dependency | R4 Stage Boundary | |
| R10 Reward Bridge（部分） | R16 Dimension-Explore-Then-Craft | R12/R13 estimate_value | |
| | R15 Complexity（如简化） | R17 is_tool | |

**统计：** 4 条可直接实现，5 条需少量补充，8 条需大量工作，3+ 条不可执行。

可直接实现的 4 条（R5/R6/R7/R20）恰好是最高优先级的规则——这不是巧合，结构性检查本来就只依赖图数据。但 Step 5 验证的核心价值（物品可达性 R1-R4、奖励连贯性 R10-R13）大多落在"需大量工作"类别。

---

## 四、AI 在 Step 4 逐节点生成时的实际可用性

SKILL.md 的 Step 4 流程是"选择一个节点 → 共同创作内容 → 更新 spec → 重新生成 → 验证 → 确认"。在这个循环中，AI 需要的是：

1. **"这个 quest 应该用几个 task？"** → MP1/MP2 可以回答，但需要 AI 判断当前节点是"standard step"还是"synthesis point"。这个判断需要 chapter-level 上下文——如果 AI 只看到当前节点，无法判断。
   - **改进：** 在 Step 2 的 outline 中标注 synthesis nodes（例如 `synthesis: true`），Step 4 直接读取。

2. **"这个 quest 应该用什么 dependency topology？"** → MP6-MP10 可以回答，但这是 Step 2/Step 3 已经决定的（outline + skeleton）。Step 4 时 topology 已经固定。
   - **改进：** 确保 micro-patterns.md 中 topology 模式明确标注为 "Phase: Step 2/3"。

3. **"这个 quest 的 reward 应该是什么？"** → MP14-MP18 可以回答，且是 Step 4 直接需要的。这五个模式的描述足够具体，可以直接转化为生成逻辑。
   - **评价：** 这是三份文档中实用性最好的部分。

4. **"这个 quest 通过了哪些验证规则？"** → R1-R22 中，Step 4 能用的只有 R5/R6/R7/R10/R18/R20/R22（仅需 quest 图数据的规则）。R1-R4 在 Step 4 无法使用。
   - **改进：** 在 Step 4 循环中只运行可执行的规则子集，将不可执行的规则延迟到 Step 5 并要求用户提供外部数据。

---

## 五、总体评估

**评估结果：需修改**

三份文档的设计质量很高——模式提取有据可依，规则定义逻辑清晰，anti-pattern 分析深入。但从 AI 实用性的角度，存在一个系统性的 gap：**文档假设了一个不存在的数据基础设施**。

核心问题不是单条规则的缺陷，而是一个架构层面的遗漏：**SKILL.md 的 toolchain（scripts/）和 reference/design/ 之间缺少一个"外部数据收集层"**。toolchain 负责从 mod jar 提取结构化数据（items.json5、mods.json5），reference/design 负责设计知识。但对于 JEI/EMI 配方数据、维度-物品映射、工具等级映射、阶段定义等——这些既不在 toolchain 的提取范围内，也不在 design docs 的知识范围内——目前是一个空白。

**建议的修改优先级（从高到低）：**

1. **【P0 — 阻塞性】** 为 R1-R4 设计可工作的降级策略。当前"跳过 + 标记 unverified"等于让最有价值的规则（物品可达性）失效。建议：硬编码常见维度/工具/阶段映射，仅对未知物品降级。
2. **【P0 — 阻塞性】** 在 SKILL.md Step 2 interview 中增加外部数据收集环节（维度物品、阶段定义、工具等级），或在 scripts/ 中增加提取脚本。
3. **【P1 — 重要】** 拆分 micro-patterns.md 为 node-level 和 chapter-level 两份文档（或在每个 pattern 头部标注 Phase），并在 SKILL.md 的 Protocol 中添加文档加载表。
4. **【P1 — 重要】** 将 R11/R14/R21 中的 NLP 函数替换为结构化标注或简化的 heuristic。
5. **【P2 — 改进】** 为 R12/R13 提供粗粒度的价值 tier 表。
6. **【P2 — 改进】** 将 anti-patterns.md 的加载时机明确为 Step 2（背景知识），并在 SKILL.md 中标注。
7. **【P3 — 优化】** 为 R17 提供硬编码的常见工具 ID 列表。
8. **【P3 — 优化】** 简化 R15 的复杂度公式，去除 recipe_depth 依赖。

---

## 六、总结

这三份文档在"what to check"和"why it matters"上做得很好，但在"how to check without external data"上存在实质性缺口。progression-rules.md 的 22 条规则中，只有约 40% 可以在当前 toolchain 下直接执行；其余 60% 依赖不存在的数据源，且降级策略不够具体。

**最关键的修改：** 要么扩展 toolchain 以提供缺失的数据（extract_tool_tiers.py、item_stage_map 收集），要么为每条依赖外部数据的规则设计一个"最小可行检查"版本（用硬编码常识 + heuristic 替代完整检查）。两者选其一即可，但不能留空白。
