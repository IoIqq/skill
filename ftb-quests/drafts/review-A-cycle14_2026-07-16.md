# 审查员 A -- 通用性审查 (Cycle 14)

**审查员:** A (通用性质疑)
**日期:** 2026-07-16
**审查范围:** Cycle 14 Phase 2 (PP13, PP14, AP36, AP37) + Phase 3 (R82-R90)
**数据源:** micro-patterns.md (PP13-PP14), anti-patterns.md (AP36-AP37), progression-rules.md (R82-R90), .researched-packs.json5 (84+ 包反例搜索)

---

## 审查结论

| 模式/规则 | 评级 | 理由摘要 |
|-----------|------|----------|
| PP13 Reward-Type Contract | **PASS** | 有 Enigmatica 4 代进化链 + FTB 官方系统级证据，pack-type 调制已在 R88 中实现 |
| PP14 Progression-as-Reward Social Contract | **PASS** | 8+ zero-reward 包支撑，明确限定 skyblock/expert/narrative，反例在适用范围外 |
| AP36 Reward-Type Roulette | **PASS** | PP13 的执行面镜像，Enigmatica lineage 标准化历程提供纵向证据 |
| AP37 Convergence Claustrophobia | **WEAK** | 仅 1 个极端案例(CreateBlock farmer 47-dep)驱动，10-dep 阈值缺乏实证校准 |
| R82 Backward Design Convergence | **PASS** | 通用设计原则，severity 按包类型正确调制 |
| R83 Weak Lock Permeability | **PASS** | 两端证据(Path of Truth hard-lock vs post/4382 weak-lock)均已覆盖 |
| R84 Mid-Game Mechan Density | **WEAK** | 仅 2 个包直接支撑比例公式(15/60-70/15-25)，文化采样偏差 |
| R85 Dual-Direction Reward Principle | **PASS** | expert 包核心设计洞察，R10 的自然延伸 |
| R86 Description-as-Pathway Clarity | **PASS** | 5+ 独立来源汇聚，expert vs kitchen-sink 分级合理 |
| R87 Anti-Nerf Progression Respect | **PASS** | 原理跨类型适用，具体实现按维度 debuff 机制调制 |
| R88 Reward-Type Contract Enforcement | **PASS** | PP13 的规则化实现，有明确阈值(2 types excl XP)和包类型分级 |
| R89 Progression-as-Reward Viability Conditions | **PASS** | 4 条 viability 条件明确，zero-reward 包样本充足(8+) |
| R90 Convergence Item Backtracking Safety | **WEAK** | 3-chapter 距离阈值缺乏实证校准，依赖 2 个 GT 包的有机整合经验 |

**汇总:** PASS = 10, WEAK = 3, FAIL = 0

---

## 详细审查

### PP13 -- Reward-Type Contract (consistent reward mechanics within a chapter)

- **通用性评级:** PASS
- **支撑包数:** 5 (Enigmatica6, Enigmatica9E, Enigmatica9, Enigmatica10, ATM-10) + FTB 官方系统级证据
- **跨类型适用性:** 该模式的核心主张——玩家会在章节内前 3-5 个任务中习得奖励交互模式并期望一致性——是跨类型的认知行为。pack-type 差异(专家包要求严格一致 vs 厨房水槽包容多样性)已在 R88 中通过 severity 调制正确处理。
- **反例搜索:**
  - Craftoria: random-dominant + item rewards 混合——但 random 和 item 在 Claim All 流程中兼容(都是 passively receivable)，不构成 contract violation。
  - ATM-10: 混合多种 reward type——但 R88 已明确 kitchen-sink 中 reward-type variety 为 INFO 而非 WARNING，TheBedrockMaster 的辩护("it's not like you can all of a sudden beat the game")印证了厨房水槽的多样性容忍度。
  - Magic-Superlative: ftbmoney:money(86.4%) + item(88.9%)——双轨奖励系统，但 ftbmoney 作为货币系统与 item rewards 在交互模型上兼容(都是被动接收)。
  - 未找到明确违反 PP13 且玩家未察觉的案例。E10 #517 证明即使是单一异常(choice among random)也被玩家立即识别为 bug。
- **文化偏差:** 直接证据偏英文包(Enigmatica lineage, ATM-10, FTB dev team)。中文包中未找到直接的玩家 reward-type 投诉。但这可能是中文社区缺乏公开 issue tracker 而非设计差异。
- **建议:** 无需修改。证据充分，pack-type 分级合理。可考虑在未来 cycle 中补充中文包的 reward-type 一致性数据(如 GregTech-Odyssey 的 copper_coin currency rewards 是否章节内一致)。

---

### PP14 -- Progression-as-Reward Social Contract (skyblock and expert context)

- **通用性评级:** PASS
- **支撑包数:** 8+ zero-reward 包: TFG Modern(25ch), TFG Vintage(13ch, 1086q), FTB-Cobblemon-Quests(5ch, 1307q), GregTech-CEu-Modern(32ch, 1282q, 最大 zero-reward 包), GregFactory-Sky(14ch), Cobblemon-Radically-Reimagined(25+ch), Ultimate-Progression-Sky(25+ch, Mekanism 198q 单章最大), Blessed-Or-Cursed(3ch, 154q 近零奖励)
- **跨类型适用性:** 明确限定为 skyblock/expert/narrative 包。条件 4(genre alignment)明确排除 kitchen-sink 和 adventure 包。这不是通用性缺陷而是正确的适用范围声明。
- **反例搜索:**
  - kitchen-sink 包(ATM-10, Craftoria, Enigmatica10)均有丰富奖励——但在 PP14 适用范围之外，不构成反例。
  - Magic-Superlative(magic-focused, 92.7% reward density)证明非 expert/skyblock 包需要 tangible rewards——与 PP14 的 genre alignment 条件一致。
  - GregFactory Sky 的"不完整的任务"反馈和"无人问津"评价验证了条件 2(mechanical unlock)和条件 3(pacing ceiling)的重要性——当 zero-reward 设计不完整时，contract 崩溃。
  - Extraordinary Energy Modern(100% 好评但"无人问津")验证了条件 1(narrative density)的挑战——zero-reward 设计要求更高的 authoring 投入。
- **文化偏差:** 证据中英文均衡。中文包: GregFactory Sky, Extraordinary Energy Modern, MC百科 thread-21004。英文包: TFG lineage, FTB-Cobblemon-Quests, Ultimate-Progression-Sky。MC百科的"玩家在每个世界的收获都是正反馈的"与英文 expert 包的 zero-reward 设计哲学高度一致。
- **建议:** 无需修改。8+ 包的样本量充足，4 条 viability 条件定义精确，适用范围声明正确。

---

### AP36 -- Reward-Type Roulette (the inconsistent chapter)

- **通用性评级:** PASS
- **支撑包数:** 5 (与 PP13 共享证据基础: E6, E9E, E9, E10 + ATM-10)
- **跨类型适用性:** AP36 是 PP13 的执行面镜像——PP13 描述玩家期望，AP36 描述违反后果。fix 建议(1 chapter = 1 primary reward type)在 expert 和 kitchen-sink 包中均适用，仅 severity 不同(WARNING vs INFO)。
- **反例搜索:**
  - Craftoria Create chapter: 100 random + 108 total rewards——高度一致的 random-dominant，符合 AP36 建议。
  - Enigmatica10: loot-dominant(29+27+26+21+...)——标准化后的 reward type 一致性证明了 AP36 fix 的有效性。
  - ATM-6: xp(282) + xp_levels(45) + random(91) + loot(1)——多类型混合，但 XP 已被 AP36/PP13 排除为 universal bridge，random+loot 混合仅 1 例(loot)。不构成反例。
  - 未找到明确"reward-type 一致但玩家仍报告体验问题"的案例——AP36 的因果链(reward-type 不一致 → 交互节奏破坏)成立。
- **文化偏差:** 与 PP13 相同，证据偏英文。但 Enigmatica lineage 跨越 4 个 MC 版本(1.16.5→1.19.2→1.20.1→1.21)的纵向进化数据提供了独特的标准化历程证据。
- **建议:** 无需修改。AP36 与 PP13 的关系(模式/反模式对)逻辑自洽，fix 建议具有可操作性。

---

### AP37 -- Convergence Claustrophobia (the submission marathon)

- **通用性评级:** WEAK
- **支撑包数:** 1 极端案例(CreateBlock farmer, 47 deps) + 间接证据
- **跨类型适用性:** 原理层面(fan-in 大会计负担)跨类型适用，但严重性调制(expert WARNING / kitchen-sink INFO)缺乏实证支撑。
- **样本量问题:** AP37 的核心驱动案例是 CreateBlock farmer(47 deps, MP66/MP69 记录的极端值)。虽然 Star-Technology(657 multi-dep, 32.1%), Path-of-Truth(22 multi-dep), Chroma-Technology-2 Mekanism(199q, diamond convergence) 展示了 multi-dep 的普遍存在，但"multi-dep 普遍存在"不等于"玩家因此受挫"。AP37 缺少直接的玩家反馈证据证明 convergence bookkeeping 是一个被广泛感知的痛点。
- **反例搜索:**
  - CreateBlock farmer 47-dep: 唯一的极端案例。fan-in 47 在全数据集中是异常值，不是典型值。
  - Star-Technology 657 multi-dep: 分布在 2049 个任务中(32.1%)——multi-dep 是常态但每个具体 convergence 点的 fan-in 未报告为极端。
  - ATM-10 basic_power: tree_branching with fan-in convergence——未报告 player bookkeeping 问题。
  - Monifactory progression: diagonal staircase with convergence——被视为正面案例。
  - 关键问题: AP37 假设 convergence 点会导致 item backtracking，但没有验证这个假设在 10-dep(而非 47-dep)时是否成立。"10+ dependencies"的阈值缺乏校准。
- **文化偏差:** MC百科 thread-21004 "过多的套娃只会让玩家厌烦" 提供了中文作者视角的原理支撑，但这是一篇冒险包设计文章，不是对 convergence bookkeeping 问题的直接报告。证据的文化覆盖面有限。
- **建议:**
  1. 在 AP37 中标注"弱证据"——当前仅由 1 个极端案例驱动。
  2. 将"10+ dependencies"阈值降级为建议值而非硬性规则，并注明该阈值来自 CreateBlock farmer 极端案例的保守推断。
  3. 补充验证: 在未来 cycle 中搜索 GitHub issues 或 MC百科/MineBBS 中关于"convergence bookkeeping"或"需要回头找材料"的玩家投诉，以验证 AP37 是否是一个广泛感知的痛点还是仅存在于极端场景。
  4. 考虑将 AP37 的 fix 建议(5)——"add a preparation quest before capstone"——标注为可选而非必要，因为在多数 10-15 dep 的 convergence 中，玩家可能不需要额外的 storage 辅助。

---

### R82 -- Backward Design Convergence (author-interview rule)

- **通用性评级:** PASS
- **支撑包数:** 4+ (MC百科 post/6155 冒险包设计, cesspit.net expert 分析, CosmicFrontiers 17-tier, Nova Engineering HyperNet)
- **跨类型适用性:** 反向设计是通用游戏设计原则。INFO severity 适当——不强制执行，仅标记"decorative chapter"供作者参考。expert 包中 dead-end chapter 更有问题，kitchen-sink 中更可接受——已在 flag 文本中体现。
- **反例搜索:**
  - ATM-10(64 chapters): 多个章节可能是"decorative"——但 R82 是 INFO 级别，允许 decorative chapters 存在。
  - RAD3(32ch, 7545q): 大量内容章节——但 adventure+RPG 包中 side content chapters 是 genre 特征，R82 正确标记为 INFO。
  - 未找到明确"反向设计导致问题"的案例——原理层面健全。
- **文化偏差:** 证据中英文均衡(cesspit.net = 英文, MC百科 post/6155 = 中文)。设计哲学本身不依赖文化背景。
- **建议:** 无需修改。

---

### R83 -- Weak Lock Permeability (author-interview rule)

- **通用性评级:** PASS
- **支撑包数:** 3+ (MC百科 post/4382 weak lock 理论, Path of Truth hard-lock 实践, CosmicFrontiers gradual scaling)
- **跨类型适用性:** 三种 lock 类型(hard_lock / weak_lock / no_lock)覆盖了全谱。severity 调制(expert WARNING / kitchen-sink INFO)正确——kitchen-sink 中的 hard_lock 被标记为 frustration 风险。
- **反例搜索:**
  - TFG Modern: linear progression_mode + voltage-tier hard locks——expert 包正确使用 hard_lock。
  - ATM-10: flexible progression_mode + no_lock——kitchen-sink 正确使用 no_lock。
  - Skylore: gamestage in non-expert pack——挑战了 gamestage 作为 hard_lock 的 expert-only 假设，但 Skylore 是 skyblock(接近 expert 的 gated 环境)，R83 的 pack-type 分级仍可覆盖。
  - DeceasedCraft: one_started(97%) 最宽松解锁——验证了 no_lock 在非 expert 包中的可行性。
- **文化偏差:** 证据主要来自中文社区(MC百科, Path of Truth)。但 weak lock 概念与西方 game design 中的"soft gate"概念等价，仅术语来源不同。
- **建议:** 无需修改。三种 lock 类型的分类框架具有通用性。

---

### R84 -- Mid-Game Mechan Density (author-interview rule)

- **通用性评级:** WEAK
- **支撑包数:** 2 (MC百科 post/4382 比例公式, Nova Engineering: World pacing 验证)
- **样本量问题:** 15%/60-70%/15-25% 的章节分布比例仅来自 MC百科 post/4382 一篇文章的建议，加上 Nova Engineering 一个包的实践验证。这个比例公式在 84+ 个包的数据集中未经系统性验证。
- **反例搜索:**
  - ATM-10(64ch): 如果 early = tutorial+tools(~10ch, 15.6%), mid = mod chapters(~44ch, 68.8%), late = endgame+bosses(~10ch, 15.6%)——符合比例。但这是事后拟合，不是设计时的有意遵循。
  - RAD3(32ch): 大量 exploration/side content chapters——late_game 可能超过 30%。
  - Ragnamod_VII(31ch): 大量 mod-specific chapters——分布未验证。
  - 核心问题: 没有对 84+ 个包进行系统性的 early/mid/late 分类统计来验证这个比例公式是否真的是"好包"的特征。
- **文化偏差:** 比例公式来自中文社区文章，可能反映中文 expert 包的设计偏好。西方 kitchen-sink 包(如 ATM 系列)的前重后轻结构可能不符合此公式但仍然成功。
- **建议:**
  1. 标注为"启发式参考"而非"比例规则"。当前 INFO severity 已适当降低了强制性。
  2. 在未来 cycle 中对 84+ 个包进行 early/mid/late 章节分类统计，验证比例公式是否与玩家评价(stars, 好评率)相关。
  3. 考虑将"early_game > 25%"和"late_game > 30%"的 flag 条件放宽为"early_game > 30%"和"late_game > 35%"，以容纳更多样的节奏设计。

---

### R85 -- Dual-Direction Reward Principle (author-interview rule)

- **通用性评级:** PASS
- **支撑包数:** 3 (cesspit.net expert 分析, E2E Extended v1.83.0 release notes, ATM-10 counter-example)
- **跨类型适用性:** 双向奖励是 expert 包设计的核心洞察——forward-only 在 mid-game 标记为 INFO(dead-end 在 mid/late-game 为 WARNING)。kitchen-sink 中 forward-only 更可接受，这与 R88 的 pack-type 分级一致。
- **反例搜索:**
  - ATM-10: generous rewards 可能都是 forward-only——但 R85 正确将 kitchen-sink 中的 forward-only 降为 INFO。
  - Craftoria: random rewards(不保证 forward 或 backward utility)——但 random 奖励的期望价值本身就包含了"可能有用"的赌注心理。
  - Magic-Superlative: ftbmoney 作为通用货币，方向性由玩家选择决定——这是 dual-direction 的极端形式(玩家自行决定 forward/backward allocation)。
- **文化偏差:** cesspit.net 为英文来源，E2E Extended 为英文。原理不依赖文化背景。
- **建议:** 无需修改。R85 是 R10(Reward-to-Dependent Bridge)的自然延伸，backward-facing component 补充了 previously forward-only 的分析维度。

---

### R86 -- Description-as-Pathway Clarity (author-interview rule)

- **通用性评级:** PASS
- **支撑包数:** 5+ (MC百科 post/4382 视觉组织, GTNH README quest text, Path of Truth FAQ, MC百科 post/6155 教程引导, E2E Extended description correction)
- **跨类型适用性:** expert 包中 description 是 primary navigation(WARNING)，kitchen-sink 中是 quality-of-life(INFO)。分级正确。
- **反例搜索:**
  - GregFactory Sky: 0% icon rate + 无 description 报告——但 R86 在 expert 包中标记为 WARNING，该包的低 engagement("无人问津")间接验证了 R86 的必要性。
  - ATM-10: 大量 quests 可能无 description——但 kitchen-sink 中 INFO severity 适当。
  - Blessed-Or-Cursed: 3ch, 154q, guide chapter uses "rich i18n text (10+ text lines per quest)"——正面案例，验证了 description-rich 设计在 adventure 包中的重要性。
- **文化偏差:** 证据中英文高度均衡。中文: MC百科 post/4382, Path of Truth, MC百科 post/6155。英文: GTNH README, E2E Extended。
- **建议:** 无需修改。5+ 独立来源的汇聚证据使 R86 成为 Cycle 14 中通用性最强的规则之一。

---

### R87 -- Anti-Nerf Progression Respect (author-interview rule)

- **通用性评级:** PASS
- **支撑包数:** 3 (MC百科 post/4382 anti-nerf 原则, CosmicFrontiers gradual scaling, Path of Truth Blue Skies mod removal)
- **跨类型适用性:** 跨类型适用——任何包含 dimension/biome debuff 的包都受此规则约束。fix 建议(provide debuff mitigation item)在 expert 和 kitchen-sink 中均可操作。
- **反例搜索:**
  - Fear-Nightfall: horror+adventure with Cold Sweat integration——debuff 是核心游戏体验，但 R87 正确要求 mitigation item 而非移除 debuff。
  - SteamPunk: Cold Sweat + Thin Air survival mechanics——same as above，debuff-as-feature 不等于 anti-nerf violation。
  - Society-Sunlit-Valley: farming pack without combat debuffs——R87 不适用(无 debuff mechanics)。
- **文化偏差:** MC百科 post/4382 + CosmicFrontiers + Path of Truth 均为中文来源。但 anti-nerf 原则与西方 game design 中的"respect player investment"原则等价。
- **建议:** 无需修改。

---

### R88 -- Reward-Type Contract Enforcement (validates PP13)

- **通用性评级:** PASS
- **支撑包数:** 5 (与 PP13/AP36 共享: E6, E9E, E9, E10, ATM-10)
- **跨类型适用性:** 明确分级: expert WARNING(>2 types excl XP) / kitchen-sink INFO。loot+item Claim All 不兼容为 WARNING regardless of pack type——这是系统级约束(FTB dev desht 确认)，不受 pack type 影响。
- **反例搜索:**
  - Craftoria: random + item 混合——但 random 和 item 在 Claim All 中兼容，不触发 R88 的 Claim All 不兼容 flag。
  - RAD3: item + xp + command + choice + random + loot_crate(6 types!)——作为 kitchen-sink，R88 标记为 INFO。6 types 在 7545 quests 中分散于 32 章，每章内部可能仍一致。
  - Prominence II RPG: XP-dominant(68.5%)——XP 被排除在计数外，不构成 violation。
- **文化偏差:** 与 PP13 相同。
- **建议:** 无需修改。"2 types excluding XP"的阈值合理，Claim All 不兼容 flag 基于 FTB 官方开发者声明。

---

### R89 -- Progression-as-Reward Viability Conditions (validates PP14)

- **通用性评级:** PASS
- **支撑包数:** 8+ zero-reward 包 (与 PP14 共享: TFG Modern, TFG Vintage, FTB-Cobblemon-Quests, GregTech-CEu-Modern, GregFactory-Sky, Cobblemon-Radically-Reimagined, Ultimate-Progression-Sky, Blessed-Or-Cursed)
- **跨类型适用性:** 4 条 viability conditions 明确限定了适用范围。condition 4(genre alignment)排除了 kitchen-sink/adventure。conditions 1-3(narrative density, mechanical unlock, pacing ceiling)在 zero-reward 包中均可验证。
- **反例搜索:**
  - GregFactory Sky: zero rewards + "不完整的任务"——违反 condition 2(mechanical unlock)，被 R89 正确标记为 WARNING。
  - Extraordinary Energy Modern: zero rewards + 100% 好评——满足 conditions 1-4，被 R89 正确标记为 INFO(合法 zero-reward design)。
  - GregTech-CEu-Modern(1282q, 最大 zero-reward 包): 满足 condition 2(每 quest 推进 GT progression)但 condition 1(narrative density)可能不满足——需要验证 description 质量。
- **文化偏差:** 证据中英文均衡。zero-reward 设计哲学在中文 GT 社区(GregFactory Sky, Extraordinary Energy Modern)和英文 GT 社区(TFG, GregTech-CEu)中均有实践。
- **建议:** 无需修改。4 条 conditions 提供了可操作的 checklist。

---

### R90 -- Convergence Item Backtracking Safety (validates AP37)

- **通用性评级:** WEAK
- **支撑包数:** 2 (CosmicFrontiers organic mod integration, GTNH progression-point allocation)
- **样本量问题:** "3 chapters in expert packs or 5 chapters in kitchen-sink packs"的距离阈值仅来自 CosmicFrontiers 和 GTNH 两个 GT 包的设计经验。这个阈值未经跨类型验证。
- **反例搜索:**
  - CreateBlock farmer(47 deps): convergence 可能跨越 10+ 章节——R90 会正确标记为 WARNING。但这是 AP37 的同一个极端案例。
  - Monifactory: convergence points 通常在同一 chapter group 内——符合 R90 阈值。
  - Star-Technology(657 multi-dep, 32.1%): 分布在 24 章中，具体 convergence 点的 backtracking 距离未验证。
  - 核心问题: 与 AP37 相同——缺乏"moderate convergence(10-20 deps)导致 backtracking 问题"的实证证据。R90 的阈值基于 2 个 GT 包的有机整合经验外推到所有 convergence 场景。
- **文化偏差:** CosmicFrontiers(MC百科中文) + GTNH(英文 GitHub)。覆盖均衡但样本量太小。
- **建议:**
  1. 标注 3-chapter / 5-chapter 距离阈值为"来自 GT 包经验的启发式参考"。
  2. 在未来 cycle 中对所有 10+ dep convergence quests进行 home-chapter 距离统计，验证阈值是否与 player frustration 相关。
  3. 考虑补充"convergence item 的可自动化程度"维度——如果 backtracking item 可以通过自动化农场大量生产(如 GregTech 的 ore processing chain)，则 backtracking 的 pain 大幅降低。

---

## 综合发现

### 证据强度分布

Cycle 14 新增内容的证据强度呈现明显的分层:

1. **强证据(5+ 包):** PP13, PP14, AP36, R82, R83, R86, R88, R89 — 这些模式/规则有多个独立数据源支撑，且 pack-type 分级经过反例验证。
2. **中等证据(3-4 包):** R85, R87 — 原理层面健全，但直接数据点略少。severity 调制合理弥补了样本量不足。
3. **弱证据(1-2 包):** AP37, R84, R90 — 由极端案例或单一来源驱动。阈值/比例公式缺乏系统性验证。

### 文化偏差评估

Cycle 14 Phase 3 的 author-interview 规则(R82-R90)显著偏向中文社区来源(MC百科 post/4382, post/6155, modpack pages)。这不是设计缺陷——中文 modpack 社区(MC百科, MineBBS, 苦力怕论坛)在 FTB Quests 设计方法论上有丰富的公开讨论文献，而英文社区的类似讨论主要分散在 private Discord channels 和 GitHub issues 中。

但审查员建议: 在未来 cycle 中补充英文 expert 包作者的设计哲学声明(如 Monifactory 的 GitHub wiki, Craftoria TeamAOF Discord logs, E2E Extended CurseForge description)以平衡文化采样。

### 与已有规则的交叉验证

Cycle 14 新增内容正确建立了与已有规则的交叉引用:
- R88 ↔ PP13 ↔ AP36: reward-type 一致性(模式/规则/反模式三位一体)
- R89 ↔ PP14 ↔ AP37: progression-as-reward 及其失败模式
- R85 ↔ R10 ↔ R45: 奖励方向性(forward + backward + bridging)
- R86 ↔ R18 ↔ R69: 描述质量从 INFO 到 WARNING 的 expert 包升级

这种三位一体(模式/反模式/规则)的结构在 Cycle 14 中首次系统性实现，是知识架构的显著进步。AP37/R90 是唯一的弱链——需要在后续 cycle 中补充 convergence bookkeeping 的实证数据。

### 无 FAIL 评级

Cycle 14 没有 FAIL 级别的模式/规则。所有新增内容至少在其声明的适用范围内有合理证据支撑。3 个 WEAK 评级均源于样本量不足而非适用范围错误——这些模式/规则的原理是合理的，但阈值和比例公式需要更多数据校准。
