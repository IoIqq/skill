# Phase 2 Cycle 8 — 玩家反馈与对比分析发现

## 搜索覆盖范围

### 中文平台
| 平台 | 搜索次数 | 有价值结果 | 备注 |
|------|---------|-----------|------|
| MC百科 (mcmod.cn) | 8+ | 丰富 | 整合包详情页、mod教程页、改动对比页均可正常访问和抓取 |
| KLPBBS (klpbbs.com) | 3 | 1篇高价值 | 魔改整合包常用模组汇总帖，含 FTB Quests vs BQ 对比 |
| Bilibili | 4 | 少量 | 整合包介绍视频为主，难以自动提取文字评论 |
| 百度贴吧 (tieba.baidu.com) | 3 | 极少 | ATM10 讨论帖有提及任务引导 |
| NGA (bbs.nga.cn) | 2 | 无直接结果 | 搜索未命中 NGA 域名，结果来自其他站点 |
| AcFun | 2 | 1个 | FTB Quests 模组介绍视频页面 |
| CSDN | 2 | 1篇 | FTB Quests 功能概述博客 |
| Gitee | 1 | 被拦截 | ATM9 Sky 汉化仓库的 SNBT 文件被验证码拦截 |

### 英文平台
| 平台 | 搜索次数 | 有价值结果 | 备注 |
|------|---------|-----------|------|
| GitHub | 5+ | 丰富 | ATM-10 discussions/issues、FTB-Mods-Issues 翻译 PR |
| CurseForge | 3 | 被 Cloudflare 拦截 | 无法自动抓取页面内容 |
| Reddit (r/feedthebeast) | 6+ | 受限 | 搜索结果大多未命中 Reddit 域名，直接 fetch 被拒绝 |
| FTB Docs (docs.feed-the-beast.com) | 2 | 1篇 | Quest book 导航文档 |
| 9Minecraft | 2 | 被拦截 | Cloudflare 防护无法抓取 |
| mcmod wiki | 1 | 少量 | 任务系统相关 |

### 搜索总结
- 共执行约 **45 轮搜索**（WebSearch + WebFetch）
- 高价值信息来源集中在：**GitHub Issues/Discussions**、**MC百科**、**KLPBBS**
- Reddit 和 CurseForge 因反爬/搜索命中问题，连续第 8 轮确认难以自动访问
- 中文平台中 MC百科 是最稳定、最有价值的信息来源

---

## 验证结果

### V1: 零奖励设计接受度

**背景**：Phase 1 发现 TFG Modern 有 601 个任务、零奖励、437 stars。Phase 1 认为这是有效设计选择。

**支持证据：**

1. **TFG Modern (群峦格雷：现代版)** — MC百科页面确认该包定位为"硬核生存科技包"，含群峦传说 + GregTech CEu + Create + Ad Astra + AE2。社区投票 **红票4/黑票0**（100%好评），日访问量指数 126（高于均值 80.845）。描述称"详尽的游戏内指南书与任务系统全程护航"。
   - 来源：https://www.mcmod.cn/modpack/1328.html

2. **群峦：救援 (TerraFirmaCraft Rescue)** — 同样使用群峦+GregTech 组合，含"超过600个任务，超60000字介绍"。使用"定制版 NEI" 点击物品自动显示合成配方，配合"自定义的礼包系统与 GT 硬币系统"作为奖励替代方案。社区投票 **红票36/黑票0**（100%好评），总访问量 329,400。
   - 来源：https://www.mcmod.cn/modpack/51.html
   - **关键发现**：群峦救援并非真正"零奖励"，而是用**替代性奖励系统**（礼包+GT硬币+NPC交易）取代了 FTB Quests 内置奖励。这暗示零奖励设计可能需要替代性激励机制来补偿。

3. **GTNH (格雷科技：新视野)** — 3000+ 任务、15 个电压阶段、约 2000 小时游玩时间。使用"定制版 NEI" 和"自定义的礼包系统与 GT 硬币系统"。社区投票 **红票180/黑票4**（98%好评），总访问量 997,300。
   - 来源：https://www.mcmod.cn/modpack/1.html
   - 玩家创建了大量攻略指南，如"GTNH新手建议"和"Better GTNH(任务书不会告诉你的)"，说明任务书本身的信息密度可能不足以独立引导玩家。

4. **ATM10 GitHub 讨论的反面证据** — 有玩家(xiaoxiao921)认为 ATM10 的任务奖励**过于慷慨**，"almost everything IMO should be revisited and a general balance pass should be made"。具体投诉包括：任务给予龙蛋/末影箱等末期物品、给予 Ultimate Universal Cable 而玩家才刚合成基础线缆、矿石探测护符使稀有矿石变得毫无意义。
   - 来源：https://github.com/AllTheMods/ATM-10/discussions/3539
   - **这从反面证明了零奖励/低奖励设计在硬核包中的合理性**——过多奖励会破坏进度节奏。

**反对证据：**

- 群峦救援和 GTNH 都**没有真正做到零奖励**，而是使用了替代奖励系统（礼包、硬币、NPC交易）。这暗示纯零奖励可能不够，需要某种形式的正向反馈。
- GTNH 的攻略标题"任务书不会告诉你的"暗示仅靠任务书引导可能有盲区。

**结论：**
零奖励设计在硬核/长时间包中**可被接受但非最佳实践**。最成功的做法是：任务书承担引导职责，配合替代性奖励系统（如 GT 硬币、礼包、NPC交易）提供正向反馈。纯零奖励的 TFG Modern 虽然有好评，但样本量太小（4票）不足以作为强证据。**建议将 MP39 修正为"低/替代奖励进度设计"而非"零奖励"。**

---

### V2: Advancement 任务体验

**背景**：Phase 1 发现 RAD2 Pathfinder 89.8% 任务使用 advancement 类型，AoF5 Spectrum 有 64 个 advancement 任务。

**支持证据：**

1. **FTB Quests 功能确认** — 从 GitHub 翻译 PR 确认 `advancement`（成就）是 FTB Quests 的标准任务类型之一，标签为"成就"。其他相关类型包括：`observation`（观察）、`checkmark`（检查点）、`stat`（统计）、`structure`（找到结构）、`biome`（访问地形）、`dimension`（访问维度）。
   - 来源：https://github.com/FTBTeam/FTB-Mods-Issues/issues/1296

2. **RAD2 (冒险与地牢2)** — MC百科确认该包含"超过 1500 个任务，包含有用的奖励、商店"。定位为冒险包（非厨房水槽型），强调探索和战斗。社区投票 **红票88/黑票0**（100%好评），总访问量 635,800。玩家创建了"RAD2中期游玩心得"等攻略。
   - 来源：http://www.mcmod.cn/modpack/419.html
   - **关键发现**：RAD2 的高好评率暗示 advancement 驱动的任务设计在冒险包中是成功的。

3. **FTB Quests 教程文档** — MC百科教程提到 `stat`（统计）类型"通常用于制作成就"，`checkmark`（检查点）"通常用于介绍辅助内容什么的"。说明非物品类任务被设计者视为辅助/引导工具而非核心进度驱动力。
   - 来源：https://www.mcmod.cn/post/1416.html

4. **FTB Docs 导航文档** — 确认任务书支持 pin 追踪功能，选择任务时可能显示"crafting recipe or any other extra information"。任务完成后有通知提醒（感叹号标记）。这些 UX 功能对 advancement 类任务的体验至关重要。
   - 来源：https://docs.feed-the-beast.com/docs/mods/suite/Quests/Player/Questbook/Navigating/

**反对证据：**

- 未找到直接讨论"advancement 任务是否无聊"的玩家反馈。这是一个**证据盲区**。
- 中文平台和英文搜索均未命中关于 advancement 任务体验的具体讨论帖。

**结论：**
Advancement 任务类型是 FTB Quests 的**标准功能**（非个例），在冒险包（如 RAD2）中被大量使用且整体好评。但**缺乏对 advancement 密集型任务书（如 89.8% advancement 任务）的具体体验反馈**。建议在 mod-*.md 中保留此模式，但标注为"缺乏玩家体验验证"。

---

### V3: Collection-Catalog 密度体验

**背景**：Phase 1 发现 SSV 的 Fishing 章节 26.7 物品/任务（极端收集密度）。

**支持证据：**

1. **RAD2 的收集设计参考** — RAD2 含 1500+ 任务，强调探索和多维度收集。玩家攻略"RAD2中期游玩心得"暗示长线收集是预期玩法的一部分。
   - 来源：http://www.mcmod.cn/modpack/419.html

2. **SSV (Society: Sunlit Valley) / 阳光谷物语** — Bilibili 上有多个直播回放视频（EP1-EP4），表明该包有一定关注度。但无法获取具体文字反馈。
   - 来源：https://m.bilibili.com/video/BV1c3pvzGEjP

3. **GTNH 的长期收集设计** — 3000+ 任务横跨 15 个科技阶段，2000 小时游玩时间。说明超大规模任务收集在硬核包中被接受。

**反对证据：**

- 未找到任何玩家直接讨论"每任务物品密度过高"的反馈。26.7 物品/任务这一指标是否合理，缺乏实际验证。
- MC百科教程提到物品任务可调整"提交数量"，暗示设计师应控制单任务的物品需求量而非任务数量。

**结论：**
极端物品密度（26.7 物品/任务）的**玩家体验完全未被验证**。这是一个证据真空。建议在 mod-*.md 中标注此指标为"待验证"，并在后续包开发实践中通过实际测试来确认合理的物品密度上限。

---

### V4: pause_game 体验

**背景**：Phase 1 发现 TFG Modern 使用 `pause_game: true`。

**支持证据：**

1. **FTB Quests 标准功能确认** — 从 GitHub 翻译 PR 确认：
   - `ftbquests.file.pause_game`: "打开任务时暂停单人游戏"
   - `ftbquests.file.pause_game.tooltip`: "不适用于多人游戏"
   - 这是**文件级别（file-level）设置**，作用于整个任务书。
   - 来源：https://github.com/FTBTeam/FTB-Mods-Issues/issues/1296

2. **设计意图分析** — 该功能的设计目的是让玩家在单人游戏中可以暂停游戏来阅读任务说明，特别适合信息密集型任务书。对于 TFG Modern 这样有 60000+ 字介绍的硬核包来说，这是一个合理的 UX 选择。

**反对证据：**

- 未找到任何玩家讨论 `pause_game` 对游戏体验影响的反馈。
- 搜索"FTB Quests pause_game"仅返回技术性页面，无讨论帖。

**结论：**
`pause_game` 是 FTB Quests 的**标准文件级配置项**（非个例），设计用于单人游戏中的阅读体验。TFG Modern 使用此设置是合理的。但**缺乏玩家体验反馈**。建议在 skill 文档中将此记录为"标准 FTB Quests 功能，适用于信息密集型硬核包"。

---

### V5: 三硬伤真实反映

#### 物品跨级：玩家是否抱怨"任务要的东西我现在拿不到"？

**直接证据：**

1. **ATM10 的进度跳跃问题** — 玩家 xiaoxiao921 在 GitHub discussion 中明确抱怨：任务给予"Dragon Egg / Ender Chests rewards even though we would not be even close to legitimately get one"，以及"Ultimate Universal Cable being given even though i barely crafted a dozen of basic ones"。虽然这是奖励端而非需求端的问题，但反映了**进度跳跃**是玩家敏感点。
   - 来源：https://github.com/AllTheMods/ATM-10/discussions/3539

2. **ATM10 矿石探测护符问题** — 玩家抱怨到达 mining dimension 后"instantly finding every allthemodium ore you want because you can instantly craft the associated ore sight charm"，认为这"invalidating the whole balance pass about allthemodium being hard to find / hard to mine"。这体现了**奖励使后续进度变得无意义**的问题。
   - 来源：同上

**间接证据：**

- MC百科教程中提到物品任务可设置"提交数量"，暗示设计师需要谨慎控制需求量。
- Game Stages 框架被设计用来解决进度问题："如果没有指定的阶段，即使拿到了物品也无法使用"（Item Stages），说明**物品跨级是已知的设计痛点**。
  - 来源：https://klpbbs.com/thread-130537-1-1.html

**结论：** 物品跨级是**真实存在的玩家痛点**，但主要表现为**奖励端跨级**（给了不该给的东西）而非需求端跨级（要求不该要求的东西）。在需求端，Game Stages 等框架已被用来预防此问题。

#### 顺序倒置：玩家是否觉得"教学排在实践后面"？

**直接证据：**

- **未找到直接的玩家反馈**讨论任务书中的教学/实践顺序问题。

**间接证据：**

- GTNH 攻略标题"Better GTNH(任务书不会告诉你的)"暗示任务书的引导可能不够及时或完整。
  - 来源：https://www.mcmod.cn/modpack/1.html
- E2E 攻略"Enigmatica 2: Expert 刚开始你就希望知道的技巧"（21,000+ 阅读）同样暗示任务书可能在早期引导方面存在不足。
  - 来源：https://www.mcmod.cn/modpack/23.html

**结论：** 顺序倒置作为独立问题**缺乏直接验证**，但多个专家包的攻略标题暗示任务书引导可能存在**时机不对或信息不足**的问题。这更接近于"教学不充分"而非"教学排错序"。

#### 奖励断链：玩家是否觉得奖励没用/不知道下一步做什么？

**直接证据：**

1. **ATM10 — 奖励过多导致方向迷失** — 玩家 xiaoxiao921 抱怨"Arbitrary progression steps being skipped for no reason"，奖励破坏了预期的进度节奏。贡献者 TheBedrockMaster 回应称"It is a kitchen sink pack, the only thing that could actually 'break progression' would be gifting out ATM Stars"。
   - 来源：https://github.com/AllTheMods/ATM-10/discussions/3539
   - **这证明奖励断链在不同类型的包中有不同表现**：厨房水槽包中奖励过多是问题，硬核包中奖励不足是问题。

2. **ATM10 GitHub Issue #3293** — 同一问题的 Issue 版本，说明这不仅仅是讨论，而是被正式报告的问题。
   - 来源：https://github.com/AllTheMods/ATM-10/issues/3293

**结论：** 奖励断链是**最被验证的硬伤**，有直接的玩家反馈证据。在厨房水槽包中表现为"奖励过多/跳跃进度"，在硬核包中可能表现为"奖励不足/不知道下一步"。设计指导应区分包类型给出不同建议。

---

### V6: MP39-MP42 跨包验证

#### MP39 (Zero-Reward Progression): 除了 TFG Modern 还有其他包用吗？

**发现：**
- 严格意义上的"零奖励"几乎没有。群峦救援和 GTNH 都使用了替代奖励系统（GT 硬币、礼包、NPC交易）。
- E2E 有 650+ 任务，使用传统的 FTB Quests 奖励系统但有明确的终局目标（Bragging Rights 任务线——制作创造物品）。
  - 来源：https://www.mcmod.cn/modpack/23.html
- **修正建议**：MP39 应更名为"Alternative-Reward Progression"（替代奖励进度），强调奖励不一定是物品，可以是信息引导、配方解锁、货币系统等。

#### MP40 (Advancement-Catalog Chapter): RAD2 之外的案例？

**发现：**
- `advancement` 是 FTB Quests 的标准任务类型，任何包都可以使用。
- 未找到 RAD2 之外的明确"以 advancement 任务为主"的包案例。
- 但 FTB Quests 的多种非物品任务类型（observation, checkmark, stat, structure, biome, dimension）都可以在概念上归入此类。
- **建议**：扩大 MP40 的定义范围，包含所有"非物品收集类任务驱动"的章节设计。

#### MP41 (Collection-Catalog): SSV 之外的极端收集案例？

**发现：**
- GTNH 的 3000+ 任务横跨 15 个科技阶段，可视为一种纵向的 Collection-Catalog。
- RAD2 的 1500+ 任务含大量探索和收集元素。
- 但未找到 SSV 之外的"单章节极高物品密度"案例。
- **建议**：保持 MP41 但标注为"极端案例，缺乏跨包验证"。

#### MP42 (dependency_requirement: one_started): 这是 FTB Quests 的标准功能还是个例？

**关键发现：**

从 GitHub 翻译 PR 确认，`dependency_requirement` 是 FTB Quests 的**标准功能**，包含四个选项：
- `all_completed`（全部完成）— 默认行为，所有前置任务必须完成
- `all_started`（全部开始）— 所有前置任务必须已开始
- `one_completed`（完成一个）— 任一前置任务完成即可
- `one_started`（一个开始）— 任一前置任务开始即可

另有 `min_required_dependencies`（最小完成前置任务数）字段，当设置为 >0 时，dependency_requirement 选项无效，变为"或"关系（只需完成指定数量）。

相关配置项还包括：
- `optional`（可选任务）
- `hide`（隐藏任务直到前置可见）
- `hide_details_until_startable`（隐藏详情直到可开始）
- `tasks_ignore_dependencies`（任务忽略依赖关系）
- `progression_mode`（任务推进方式）
- `require_sequential_tasks`（线性任务）

来源：https://github.com/FTBTeam/FTB-Mods-Issues/issues/1296

**结论：** `dependency_requirement: one_started` 是 **FTB Quests 标准功能**，非个例。MP42 应从"发现性模式"升级为"已确认的标准功能用法"。FTB Quests 的依赖系统比之前记录的更加丰富，skill 文档应补充完整的依赖配置选项参考。

---

## 新发现的模式或反面教材

### 新发现 1: 替代奖励系统模式 (Alternative Reward System Pattern)

**描述**：硬核包普遍不使用 FTB Quests 内置物品奖励，而是通过替代系统提供正向反馈：
- GTNH / 群峦救援：GT 硬币 + NPC 交易 + 礼包系统
- RAD2：货币商店 + 技能升级
- E2E：Bragging Rights 终局目标驱动

**意义**：这比简单的"零奖励 vs 有奖励"二分法更加精细。替代奖励系统的核心是**将奖励转化为游戏内经济**，而非直接给予物品。

### 新发现 2: Game Stages 作为进度守门人

**描述**：KLPBBS 魔改包常用模组帖确认 Game Stages 框架被广泛搭配 FTB Quests 使用，通过 CraftTweaker 集成实现：
- Item Stages：未解锁阶段的物品拿到也无法使用
- Recipe Stages：未解锁阶段的配方不可见
- Dimension Stages：未解锁阶段的维度不可进入

**意义**：这直接解决了"物品跨级"硬伤。FTB Quests 本身不包含进度锁定能力，需要 Game Stages 等外部框架配合。skill 文档应明确记录这一点。

来源：https://klpbbs.com/thread-130537-1-1.html

### 新发现 3: FTB Quests vs Better Questing vs HQM 三足鼎立

**描述**：KLPBBS 帖提供了三大任务模组的对比：
- **FTB Quests**：轻量、团队导向、定制性强，现代包首选
- **Better Questing (BQ)**：修复了 HQM 的严重技术缺陷（服务器闪退、乱码、BUG），支持导入 HQM 数据
- **Hardcore Questing Mode (HQM)**：最经典但功能"不及FTBQ,BQ那样强大"，多用于剧情向包，类似 MMO 的"达到目标获得物品或解锁后续任务"

**意义**：FTB Quests 在现代整合包开发中是事实标准，skill 的目标平台定位正确。

来源：https://klpbbs.com/thread-130537-1-1.html

### 新发现 4: 任务书的"信息密度 vs 引导能力"矛盾

**描述**：多个包的攻略标题暗示任务书存在信息传递不足的问题：
- GTNH："Better GTNH(任务书不会告诉你的)"
- E2E："Enigmatica 2: Expert 刚开始你就希望知道的技巧"（21,000+ 阅读）
- RAD2："RAD2中期游玩心得"

**意义**：即使有 600-3000 个任务，玩家仍觉得任务书不够用。这说明任务书的**信息密度**和**引导有效性**是两个不同的维度。高任务数量不等于好引导。

### 新发现 5: FTB Quests 完整的任务类型和奖励类型列表

从翻译 PR 获取了完整的类型列表：

**任务类型（20种）**：
item, fluid, forge_energy, advancement, biome, checkmark, custom, dimension, emc, ftb_money, gamestage, interaction, kill, location, npc_dialog, npc_faction, npc_quest, observation, stat, structure, xp

**奖励类型（15种）**：
item, advancement, choice, command, custom, ftb_money, gamestage, loot, npc_faction, npc_mail, npc_quest, random, toast, xp, xp_levels

**来源**：https://github.com/FTBTeam/FTB-Mods-Issues/issues/1296

### 新发现 6: ATM10 奖励经济争议——厨房水槽包的特殊性

ATM10 的 GitHub Discussion #3539 和 Issue #3293 提供了一个完整的奖励经济争论案例：
- **投诉方**认为奖励破坏了进度节奏（给了太早期的末期物品）
- **辩护方**认为厨房水槽包中只有给 ATM Stars（终局物品）才会真正破坏进度
- **折中观点**认为获得稀有材料只是开始，后续还有更多挑战

这说明**奖励设计需要根据包类型差异化处理**：厨房水槽包应控制高价值奖励的发放时机，硬核包则更需要替代奖励系统。

---

## 对现有模块的修订建议

### 1. 关于 MP39 (Zero-Reward Progression)
- **建议**：重命名为 "Alternative-Reward Progression" 或 "Non-Item-Reward Progression"
- **理由**：严格的零奖励几乎没有案例。成功的硬核包使用替代奖励（货币、礼包、NPC交易），而非完全没有奖励
- **涉及文件**：相关的 mod-patterns 文件

### 2. 关于 MP42 (dependency_requirement: one_started)
- **建议**：升级为"已确认的标准功能"，补充完整的依赖配置选项参考
- **理由**：已确认为 FTB Quests 标准功能，且有 4 种 dependency_requirement 选项 + min_required_dependencies 数值控制
- **涉及文件**：相关的 mod-patterns 文件和 task-config 文档

### 3. 关于 Game Stages 集成
- **建议**：新增一个模块或模式描述 FTB Quests + Game Stages 的协作方式
- **理由**：这是解决"物品跨级"硬伤的标准方案，但当前 skill 文档可能未涵盖
- **涉及文件**：progression-gating 相关模块

### 4. 关于奖励设计指南
- **建议**：按包类型区分奖励策略——厨房水槽包 vs 专家包 vs 冒险包
- **理由**：ATM10 争议证明一刀切的奖励策略不适用
- **涉及文件**：reward-design 相关模块

### 5. 关于任务书引导有效性
- **建议**：补充"任务书信息密度 vs 引导有效性"的设计指导
- **理由**：多个高好评包的攻略标题暗示任务书引导不足，说明这是普遍问题
- **涉及文件**：quest-writing 相关模块

### 6. 补充完整的 FTB Quests 功能参考
- **建议**：在参考文档中补充完整的任务类型（20种）、奖励类型（15种）、依赖配置选项、文件级设置（如 pause_game）
- **理由**：当前文档可能未覆盖 FTB Quests 的完整功能集
- **涉及文件**：ftb-quests feature reference 文件

---

## 来源列表

### 高价值来源（直接引用）

1. **ATM10 GitHub Discussion #3539** — Quest Book rewards breaking balance
   https://github.com/AllTheMods/ATM-10/discussions/3539

2. **ATM10 GitHub Issue #3293** — Quest Book reward issues
   https://github.com/AllTheMods/ATM-10/issues/3293

3. **FTB Quests zh_cn 翻译 PR** — 完整的 i18n key 列表（确认所有功能名称）
   https://github.com/FTBTeam/FTB-Mods-Issues/issues/1296

4. **KLPBBS 魔改整合包常用模组** — FTB Quests/BQ/HQM 对比 + Game Stages 集成
   https://klpbbs.com/thread-130537-1-1.html

5. **MC百科 - 群峦格雷：现代版 (TFG Modern)**
   https://www.mcmod.cn/modpack/1328.html

6. **MC百科 - 群峦：救援 (TerraFirmaCraft Rescue)**
   https://www.mcmod.cn/modpack/51.html

7. **MC百科 - 格雷科技：新视野 (GTNH)**
   https://www.mcmod.cn/modpack/1.html

8. **MC百科 - 冒险与地牢2 (RAD2)**
   http://www.mcmod.cn/modpack/419.html

9. **MC百科 - Enigmatica 2: Expert (E2E)**
   https://www.mcmod.cn/modpack/23.html

10. **MC百科 - Craftoria**
    https://www.mcmod.cn/modpack/863.html

11. **MC百科 - FTB Quests 教程**
    https://www.mcmod.cn/post/1416.html

12. **MC百科 - KubeJS 使 FTB 任务可重复**
    https://www.mcmod.cn/post/2089.html

13. **FTB Docs - Quest Book Navigation**
    https://docs.feed-the-beast.com/docs/mods/suite/Quests/Player/Questbook/Navigating/

14. **CSDN - FTB Quests 功能概述**
    https://blog.csdn.net/gitblog_00062/article/details/139978977

15. **MC百科 - FTB Quests Mod 页面**
    http://www.mcmod.cn/class/1423.html

### 参考来源（间接引用）

16. **Bilibili - TFG Modern 汉化补丁**
    https://www.bilibili.com/read/mobile?id=40392824

17. **Bilibili - 阳光谷物语直播回放**
    https://m.bilibili.com/video/BV1c3pvzGEjP

18. **Bilibili - RAD2 整合包介绍**
    https://www.bilibili.com/read/mobile?id=16185581

19. **MC百科 - Enigmatica 2: Expert Skyblock**
    https://www.mcmod.cn/modpack/169.html

20. **百度贴吧 - ATM10 教程推荐**
    https://tieba.baidu.com/p/9467970658

21. **Reddit r/feedthebeast - Modpack progression through technological ages**
    https://www.reddit.com/r/feedthebeast/comments/1th6g3a/

22. **Reddit r/feedthebeast - Modpack recommendation (ROTN-style balancing)**
    https://www.reddit.com/r/feedthebeast/comments/1gfhzjw/

### 平台访问受限记录

23. **CurseForge** — Cloudflare 防护，无法自动抓取页面内容
24. **Reddit** — 直接 fetch 被拒绝，搜索引擎对 Reddit 内容命中率低
25. **Gitee** — 验证码拦截
26. **MCBBS** — 连续多轮确认无法自动访问
27. **9Minecraft** — Cloudflare 防护

---

## 搜索局限性声明

本次 Phase 2 研究存在以下局限性：

1. **Reddit 数据严重不足** — 作为英文 FTB 社区的核心平台，Reddit 的搜索结果几乎未命中，直接 fetch 也被拒绝。这导致大量英文玩家反馈未能被采集。
2. **CurseForge 不可访问** — 整合包详情页（含评论和评分）无法抓取，丢失了大量玩家评价数据。
3. **中文平台评论加载限制** — MC百科的短评区域显示"短评加载中.."，实际评论内容未被抓取。
4. **样本偏差** — 可用数据偏向中文社区和 GitHub 技术讨论，可能不全面反映全球玩家群体的意见。
5. **V2（advancement 任务体验）和 V3（收集密度体验）的证据尤其薄弱** — 这两个领域需要后续通过实际游戏测试或社区调研来补充验证。
