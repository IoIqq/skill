# Phase 3 Cycle 8 -- 作者访谈与进度规则发现

## 搜索覆盖范围

### 中文平台
| 平台 | 搜索策略 | 有价值内容 |
|------|---------|-----------|
| Bilibili | 整合包设计思路、任务设计、Vazkii访谈 | Vazkii整合包制作文章(无法完整抓取JS渲染)、科技向1.12.2整合包推荐文章(CAPTCHA阻断) |
| MC百科(mcmod.cn) | 整合包设计、任务系统、冒险包设计、高难度包开发 | **3篇高价值文章**：论较高难度较长寿命整合包的设计与开发、冒险包设计思路、FTB任务系统教程、物品阶段不止于物品阶段 |
| MC百科论坛(bbs.mcmod.cn) | 整合包制作总体思路 | 1篇：如何制作Minecraft整合包总体思路篇 |
| KLPBBS | 魔改整合包常用模组 | 少量相关内容 |
| 知乎 | 整合包任务设计 | 无直接作者访谈 |
| NGA | 整合包设计任务 | 少量相关内容 |
| CSDN | FTB Quests探索与挑战、FTB Quest与GameStages结合 | 2篇：FTB Quests概述、FTB Quest与GameStages结合的时代发展modpack |

### 英文平台
| 平台 | 搜索策略 | 有价值内容 |
|------|---------|-----------|
| Reddit r/feedthebeast | modpack author/design/progression | 多个帖子标题可见但无法抓取正文(Reddit反爬)：I made a modpack focused on progressing through technological ages、It's 2025 balanced semigated pack with quests、Sanctuary modpack、The five tiers of mod complexity |
| CurseForge | modpack descriptions | 部分包描述含设计说明 |
| Meegle | quest design best practices | 1篇通用任务设计原则文章 |

### GitHub
| 仓库 | 搜索结果 |
|------|---------|
| AllTheMods/ATM-10 | **1个高价值Discussion**：#3539 "The Quest Book gives way too many rewards that break balance and progression" |
| Omicron-Industries/Monifactory | **2个有价值Issue**：#28 Questbook Issues(202条评论)、#2359 Better Tutorialisation of Basic Mechanics |

### 总体评估
- 搜索关键词覆盖：~35组不同搜索组合
- 有价值内容源：~12个
- 成功抓取详细内容：~8个
- 核心发现来源：mcmod.cn(3篇) + CSDN(1篇) + GitHub(2个) + Meegle(1篇) + ATM-10 Discussion(1个)

---

## 作者设计思路发现

### D1: 物品可达性保证策略

#### 发现1：论较高难度较长寿命整合包 -- "弱锁"策略
- **来源**：mcmod.cn/post/4382.html
- **核心观点**：作者提出进度门控应该是"弱锁"(weak lock)，允许聪明玩家绕过预期序列获得"偷鸡的爽感"。但跳过进度的奖励应该是"孤立的、不稳定的或随机的"，确保玩家仍然自然参与核心进度循环。
- **原文关键句**：
  - "实现进度门控作为'弱锁'，允许聪明玩家绕过预期序列"
  - "跳过进度的奖励应该是孤立的、不稳定的或随机的"
- **可提炼的规则**：
  - 任务前置依赖应设计为"建议性"而非"绝对阻断"
  - 如果允许跳关获得物品，该物品应缺乏完整的后续利用链

#### 发现2：冒险包设计思路 -- 维度材料管控
- **来源**：bbs.mcmod.cn/thread-21004-1-1.html
- **核心观点**：通过控制材料生成世界和怪物生成世界来强制执行预期的难度曲线。强力资源只在适当维度生成。
- **原文关键句**："修改材料的生成世界，以及怪物的生成世界"
- **可提炼的规则**：
  - 任务要求的物品，其合成链中的原材料必须在当前可达维度可获得
  - 使用世界生成限制作为隐式进度门控

#### 发现3：FTB Quest与GameStages结合 -- 闭环进度系统
- **来源**：wenku.csdn.net/doc/6amfp2j2im
- **核心观点**："任务完成即激活新阶段"(completing a quest activates a new stage)是FTB Quest + GameStages集成的核心模式。任务完成后自动激活新的Game Stage，解锁对应的配方、维度和世界规则。
- **具体技术模式**：
  - 高级物品锁定在特定时代之后
  - 早期自动化工具(如AE2终端)被禁用以强制手动分类
  - 原版熔炉保持可用，但"只有当玩家达到Bronze_Age阶段并完成冶金学基础任务后，才会解锁模组双层熔炉"
  - 村庄铁匠随玩家时代进展动态升级交易选项
- **可提炼的规则**：
  - 任务完成 -> 触发Stage -> 解锁配方/物品 的因果链必须单向无环
  - Stage的解锁顺序应与任务依赖图严格一致

#### 发现4：ATM-10 Discussion #3539 -- 奖励物品可达性争议
- **来源**：github.com/AllTheMods/ATM-10/discussions/3539
- **核心观点**：xiaoxiao921指出任务奖励的ATM矿石视觉符咒(charm)让玩家跳过预期的采矿难度："just reaching the mining dimension with 3 players mean that you are instantly finding every allthemodium ore you want because you can instantly craft the associated ore sight charm for it"，这使得"allthemodium being hard to find / hard to mine"的平衡设计被完全绕过。
- **TheBedrockMaster反驳**："It is a kitchen sink pack, the only thing that could actually 'break progression' would be gifting out ATM Stars"
- **xiaoxiao921再回应**："Arbitrary progression steps being are skipped for no reason"
- **可提炼的规则**：
  - **奖励物品不能提供绕过其所在章节预期挑战的能力**
  - Kitchen Sink包中"破坏进度"的阈值高于Expert包，但仍需保持"任意进度步骤不被无意义跳过"

### D2: 教学顺序设计策略

#### 发现1：Monifactory Issue #2359 -- 教学不足的问题
- **来源**：github.com/Omicron-Industries/Monifactory/issues/2359
- **核心观点**：LunatiK-ExpiX指出"教程化(Tutorialisation)在制作这个包时可能没有被充分考虑"。具体例子：
  - "Infiniter Water"和"LV Pumps"任务几乎不提供如何使用物品的信息
  - Aqueous Accumulator让玩家困惑，"可能导致他们花费超过需要的时间，30分钟后才意识到需要配置泵"
- **提议的解决方案**：给介绍Gregtech关键特性的任务增加更多机械原理说明
- **可提炼的规则**：
  - **教学任务必须先于应用任务**：先解释机械原理，再要求玩家使用
  - 如果任务要求提交一个通过复杂机械获得的物品，任务描述应包含操作指引
  - 不要假设玩家知道模组的默认行为

#### 发现2：论较高难度包 -- 早期教学策略
- **来源**：mcmod.cn/post/4382.html
- **核心观点**：
  - **早期游戏**：用独特机制、彩蛋或随机元素钩住玩家，但快速推入中期。惩罚性的时间门控在早期失败，因为新奇感快速消退。
  - 确保开头感觉独特，避免让玩家从其他包获得"先入为主的想法"
- **可提炼的规则**：
  - 前3-5个任务应包含明确的教学文本，介绍包的核心差异化机制
  - 教学任务不应该是"提交X个物品"的纯操作任务

#### 发现3：FTB Quests系统设计 -- 任务类型作为教学工具
- **来源**：mcmod.cn/post/1416.html
- **核心观点**：FTB Quests支持多种任务类型(物品、流体、能量、维度、统计、击杀、坐标、复选框)，可以组合使用来实现教学效果：
  - 复选框任务可用于"显示辅助信息或指南"
  - 文本面板可插入"主标题、副标题和正文文本"来提供背景故事或教学说明
  - 维度任务在玩家"访问特定领域"时自动触发
- **可提炼的规则**：
  - 使用复选框任务 + 描述文本来做纯教学节点(无需提交物品)
  - 教学节点应位于实践节点的前置依赖位置

### D3: 奖励引导策略

#### 发现1：ATM-10 Discussion #3539 -- 奖励过多导致平衡崩坏
- **来源**：github.com/AllTheMods/ATM-10/discussions/3539
- **核心观点**：
  - xiaoxiao921认为"几乎一切IMO都应该被重新审视并做一次通用平衡"
  - 奖励Ender Chest在游戏早期没有意义
  - Ultimate Universal Cable在玩家"几乎没合成过一打基础线缆"时就被奖励
  - "进度是共享的，重复品可以OP"
- **可提炼的规则**：
  - **奖励应与当前进度阶段的实际需求匹配**
  - 不应在早期奖励后期物品(即使数量很少)
  - 多人游戏中需考虑共享进度对奖励价值的影响

#### 发现2：论较高难度包 -- 奖励与下一阶段的衔接
- **来源**：mcmod.cn/post/4382.html
- **核心观点**：
  - 奖励应该引导玩家进入下一个进度阶段
  - 中期应"引入跨模组的扫荡性机制"(如日夜维度交换)跨越整个任务章节
  - 混合冒险与科技/魔法，多样化合成方法以消除重复刷取
- **可提炼的规则**：
  - **奖励物品最好是下一个任务链的起始材料**
  - 避免奖励"万能物品"(可以替代多种材料的物品)

#### 发现3：Meegle通用任务设计原则
- **来源**：meegle.com/en_us/topics/game-design/quest-design
- **核心观点**：
  - 保持"风险与奖励的平衡"以激励玩家
  - 提供"有意义的奖励，如独特物品、能力或故事揭示"，作为"成功的有形衡量标准"
  - 挑战应"随玩家进度缩放"
- **可提炼的规则**：
  - 奖励的价值应与任务难度成正比
  - 独特/不可合成的物品是最有价值的奖励

### D4: 阶段划分原则

#### 发现1：FTB Quest + GameStages -- 时代演进模式
- **来源**：wenku.csdn.net/doc/6amfp2j2im
- **核心观点**："时代演进"(Ages-based progression)是核心设计模式，将语义阶段(Stone_Age, Bronze_Age, Electric_Age)组织成多维自演化世界模型：
  1. **时间维度**：玩家通过积累经验、探索、击败Boss推进时代节点
  2. **空间维度**：生物群系动态解锁与当前时代对应的新结构(如Electric Age的漂浮实验室)
  3. **资源维度**：矿石生成率、稀有度和深层分布受当前阶段标签主动调控
  4. **社会维度**：村庄升级、村民职业变换和交易刷新率随时代同步演化
- **可提炼的规则**：
  - 阶段划分可基于：科技等级 > 维度 > 材料等级 > Boss击杀
  - 每个阶段应有明确的"解锁边界"(什么新可用、什么新区域、什么新材料)

#### 发现2：冒险包设计思路 -- 四阶难度系统
- **来源**：bbs.mcmod.cn/thread-21004-1-1.html
- **核心观点**：
  - 怪物和装备应遵循四阶系统
  - 平滑过渡原则："上一个世界的顶端装备对应于这个世界的小怪"
  - 装备多样性应呈橄榄形(更多中端，更少低端/高端)以防同质化
  - 难度跨维度应线性缩放，确保"玩家在每个世界的收获都是正反馈的"
- **可提炼的规则**：
  - 阶段之间的过渡应保证"上阶段顶级 = 下阶段入门"
  - 阶段内物品/怪物难度应单调递增

#### 发现3：论较高难度包 -- 三段式生命周期
- **来源**：mcmod.cn/post/4382.html
- **核心观点**：
  - **早期**：钩住玩家，快速推进，避免惩罚性时间门控
  - **中期**：最关键阶段，引入跨模组机制，延长包寿命
  - **后期**：防止反高潮结局，避免简单配方链堆叠，回顾并重用早期模组，永不人为膨胀游戏时间
- **可提炼的规则**：
  - 阶段数建议：3-7个主要阶段
  - 后期阶段不应引入全新的独立系统，而应复用和组合早期系统

### D5: 可选内容设计策略

#### 发现1：FTB Quests系统设计 -- Group与可选任务
- **来源**：mcmod.cn/post/1416.html
- **核心观点**：
  - 使用Group选项将任务嵌套在父章节下，保持界面整洁
  - 任务依赖通过"Ctrl+左键选择前置，然后右键后续任务来链接"建立
  - 复选框任务"主要用于显示辅助信息或指南"
- **可提炼的规则**：
  - 可选任务不应作为主线任务的前置依赖
  - 可选任务的奖励应独立于主线(不影响主线进度)

#### 发现2：Meegle任务设计原则 -- 分支叙事
- **来源**：meegle.com/en_us/topics/game-design/quest-design
- **核心观点**：
  - 不使用严格门控，而是使用"分支叙事"和"多任务路径与结果"
  - 用户选择应"影响游戏结果"，个性化旅程并鼓励重玩性
- **可提炼的规则**：
  - optional: true 应用于真正的旁支内容
  - 如果可选任务奖励了主线需要的物品，则它实际上是必做的(设计矛盾)

#### 发现3：ATM-10 争议 -- Kitchen Sink包的可选定义
- **来源**：github.com/AllTheMods/ATM-10/discussions/3539
- **核心观点**：TheBedrockMaster认为"It is a kitchen sink pack"，只有赠送ATM Stars才会"破坏进度"。在KS包中，几乎所有内容都是"可选"的，进度破坏阈值远高于Expert包。
- **可提炼的规则**：
  - 包类型(KS vs Expert)决定了"可选"与"必做"的边界
  - Expert包：optional: true 严格限制，仅用于真正的旁支
  - KS包：大部分内容可设为optional，主线仅为核心路径

---

## 进度校验规则候选

### PR1: 奖励-阶段匹配规则
- **规则描述**：任务奖励的物品等级不应超过该任务所在阶段+1级。奖励不应提供绕过当前章节预期挑战的能力。
- **来源**：ATM-10 Discussion #3539 (xiaoxiao921的评论)
- **可编码性**：高
  - 为每个物品分配阶段标签(stage_tag)
  - 检查：reward.stage <= quest.chapter.stage + 1
  - 检查：reward不提供跳过当前章节挑战的能力(如：如果章节主题是"困难采矿"，奖励不应包含"自动寻矿符咒")
- **与现有规则的关系**：对应奖励经济审查员的R10-R13规则组

### PR2: 教学-实践顺序规则
- **规则描述**：如果任务B要求提交一个通过复杂机械/系统获得的物品，则必须存在前置任务A，其描述文本中包含该系统的使用教学。
- **来源**：Monifactory Issue #2359
- **可编码性**：中
  - 识别"复杂系统"(需要多步骤操作的模组机制)
  - 检查：对于每个提交复杂物品的任务，其前置中是否包含描述文本>200字符的教学节点
- **与现有规则的关系**：对应进度链审查员的R1-R4规则组(可达性)

### PR3: 阶段过渡平滑规则
- **规则描述**：上一阶段的顶级装备/物品应足以应对下一阶段初期的挑战。即阶段过渡不应出现"断崖"。
- **来源**：冒险包设计思路(bbs.mcmod.cn/thread-21004-1-1.html)
- **可编码性**：中
  - 为每个阶段定义"顶级物品集合"和"初期怪物/挑战"
  - 验证：上阶段顶级物品的DPS/效率 >= 下阶段初期怪物的HP/需求
- **与现有规则的关系**：新增规则，属于难度曲线校验

### PR4: 阶段内物品可达性规则
- **规则描述**：任务要求提交的物品，其完整合成链中的所有原材料必须在当前阶段可达维度中可获得。
- **来源**：冒险包设计思路 + FTB Quest与GameStages结合文章
- **可编码性**：高
  - 构建物品合成树(recipe_tree)
  - 构建阶段可达资源表(stage_available_resources)
  - 检查：quest.required_item的合成树中每个叶子节点 ∈ stage_available_resources[current_stage]
- **与现有规则的关系**：对应进度链审查员的R1(物品可达性)规则

### PR5: Stage-Quest因果链单向规则
- **规则描述**：FTB Quest完成 -> Game Stage激活 -> 配方解锁 的因果链必须是无环有向图。不允许出现循环依赖(如：需要Stage A解锁物品X来完成任务T，但任务T完成后才激活Stage A)。
- **来源**：FTB Quest与GameStages结合(wenku.csdn.net/doc/6amfp2j2im)
- **可编码性**：高
  - 构建Stage-Quest依赖图
  - 使用拓扑排序检测环
- **与现有规则的关系**：对应进度链审查员的R2(解锁顺序)规则

### PR6: 弱锁设计规则
- **规则描述**：如果允许跳关获得物品(通过非预期路径)，该物品应缺乏完整的后续利用链(即：不能直接用于更高级的合成)。
- **来源**：mcmod.cn/post/4382.html
- **可编码性**：低
  - 需要识别"非预期路径"(如通过蜜蜂产出的时间水晶)
  - 检查这些物品的下游用途是否被Stage正确门控
- **与现有规则的关系**：新增规则，属于防跨级机制

### PR7: 奖励引导衔接规则
- **规则描述**：章节完成奖励应包含下一章首个任务所需的关键材料或工具。
- **来源**：mcmod.cn/post/4382.html + Meegle通用设计原则
- **可编码性**：高
  - 获取chapter_N完成奖励列表
  - 获取chapter_N+1首个任务的物品需求
  - 检查：交集非空
- **与现有规则的关系**：对应奖励经济审查员的R12(奖励链完整性)规则

### PR8: 多人共享进度奖励去重规则
- **规则描述**：在支持多人共享进度的包中，奖励不应因多人重复完成而产生OP堆叠。
- **来源**：ATM-10 Discussion #3539 ("Progression is shared and duplicates can be op")
- **可编码性**：中
  - 检查奖励类型：如果奖励是一次性物品且进度共享，标记为需审查
  - 建议：使用消耗性奖励(经验、货币)替代一次性物品奖励
- **与现有规则的关系**：新增规则，属于多人场景特化

---

## 三硬伤预防机制

### 物品跨级预防

| 机制 | 来源 | 具体做法 |
|------|------|---------|
| Game Stages物品锁定 | CrT-Game Stages教程(mcmod.cn/post/1015.html) | 使用Recipe Stages锁定配方，Item Stages锁定物品可见性，Enchantment Stages锁定附魔 |
| 维度材料管控 | 冒险包设计思路 | 控制材料的生成世界，确保强力资源只在适当维度生成 |
| 弱锁+随机化奖励 | 论较高难度包 | 跳关获得的奖励应"孤立的、不稳定的或随机的" |
| 阶段配方解锁 | FTB Quest+GameStages文章 | "只有达到Bronze_Age阶段并完成冶金学基础任务后，才解锁双层熔炉" |

**可编码的检测逻辑**：
```
对每个任务T，检查其要求物品I的合成树：
1. 获取I的所有原材料叶子节点
2. 对每个叶子L，检查L是否在当前阶段可达：
   a. L的矿石是否在当前可达维度生成？
   b. L的配方是否已在前置Stage解锁？
   c. L是否需要通过击杀怪物获得？该怪物是否在当前可达区域？
3. 如果任何叶子不可达，标记为"物品跨级风险"
```

### 顺序倒置预防

| 机制 | 来源 | 具体做法 |
|------|------|---------|
| FTB Quests前置依赖链 | FTB任务系统教程 | Ctrl+左键建立前置，强制解锁顺序 |
| Stage拓扑排序 | CrT-Game Stages教程 | Stage无默认层级，所有依赖必须手动配置 |
| 教学节点前置 | Monifactory Issue #2359 | 确保教学任务在应用任务之前 |

**可编码的检测逻辑**：
```
构建任务依赖DAG：
1. 对每个任务T，检查其所有前置依赖pre[]
2. 对每个pre，检查pre的完成条件是否可在T的上下文中满足
3. 使用拓扑排序检测环
4. 检查教学节点是否位于实践节点之前(通过文本分析识别教学节点)
```

### 奖励断链预防

| 机制 | 来源 | 具体做法 |
|------|------|---------|
| 奖励-阶段匹配 | ATM-10 Discussion #3539 | 奖励不应超出当前阶段+1 |
| 奖励引导衔接 | 论较高难度包 | 奖励应是下一阶段的起始材料 |
| 奖励去重(多人) | ATM-10 Discussion #3539 | 共享进度下避免重复OP奖励 |

**可编码的检测逻辑**：
```
对每个任务T的奖励R[]：
1. 检查R的stage_tag <= T.chapter.stage + 1
2. 检查R是否是T.next_chapter任何任务的所需材料(奖励引导衔接)
3. 如果是最后一个章节的完成奖励，检查R是否与后续章节首任务有交集
4. 如果包支持多人共享进度，检查R是否会产生堆叠OP
```

---

## Game Stages 深度分析

### 技术架构
Game Stages模组生态系统包含以下组件(基于mcmod.cn/post/1015.html和mcmod.cn/post/2997.html的发现)：

1. **Game Stages核心**：提供阶段注册和玩家阶段管理API
   - 阶段名规则：全小写，无空格，可用中文
   - 阶段无默认层级关系，所有依赖手动配置
   - 玩家可同时持有多个阶段

2. **Item Stages**：锁定物品可见性和可用性
   - 可锁定：物品、流体(连同桶)、附魔
   - API：`ItemStages.stageEnchantByLevel(stage, enchantment)`
   - API：`ItemStages.stageRecipeCategory(stage, category)`

3. **Recipe Stages**：锁定配方合成权限
   - 通过配方ID绑定到阶段
   - 玩家未解锁阶段时无法合成对应物品

4. **CraftTweaker集成(CrT-Game Stages)**：脚本化控制
   - 最佳实践：使用进度(Achievement)或CrT控制玩家阶段(比服务器命令更适合)
   - 可扩展到：维度锁定、矿石生成、怪物生成、飞行、Waila/JourneyMap

### 与FTB Quests的集成模式

基于wenku.csdn.net/doc/6amfp2j2im的分析：

```
核心闭环：
[任务完成] --触发--> [新Stage激活] --解锁--> [配方/物品/维度] --需求--> [下一个任务]
```

**多维联动设计模式**(时代演进模型)：
- **时间维度**：经验积累 -> 阶段推进 -> 任务解锁
- **空间维度**：阶段标签 -> 生物群系结构生成 -> 探索任务
- **资源维度**：阶段标签 -> 矿石生成率/分布 -> 采集任务
- **社会维度**：阶段标签 -> 村庄升级/交易 -> 交易任务

### 1.12.2 vs 现代版本对比
- 1.12.2时代：Game Stages + Item Stages + Recipe Stages + CraftTweaker 是标准工具链
- 1.16+时代：FTB Quests自带的阶段管理更强大，Game Stages生态逐渐被替代
- 1.20+时代：KubeJS + FTB Quests原生阶段成为主流方案

---

## 来源列表

### 中文来源
1. [论较高难度、较长寿命整合包的设计与开发](https://www.mcmod.cn/post/4382.html) - MC百科
2. [冒险包设计思路](https://bbs.mcmod.cn/thread-21004-1-1.html) - MC百科论坛
3. [FTB任务系统教程](https://www.mcmod.cn/post/1416.html) - MC百科
4. [如何制作Minecraft整合包？总体思路篇](https://bbs.mcmod.cn/forum.php?action=printable&mod=viewthread&tid=18316) - MC百科论坛
5. [物品阶段不止于物品阶段！](https://www.mcmod.cn/post/2997.html) - MC百科
6. [CrT-Game Stages介绍篇](https://www.mcmod.cn/post/1015.html) - MC百科
7. [FTB Quest与GameStages结合：1.12.2时代发展modpack](https://wenku.csdn.net/doc/6amfp2j2im) - CSDN
8. [探索与挑战的无限可能：FTB Quests](https://blog.csdn.net/gitblog_00062/article/details/139978977) - CSDN
9. [植魔作者Vazkii：我是这样制作整合包的](https://www.bilibili.com/read/cv18734065) - Bilibili (JS渲染未能完整抓取)
10. [关于制作冒险类整合包的一些心得分享](https://www.mcmod.cn/post/6155.html) - MC百科 (抓取失败)
11. [我的世界任务书系统：FTB Quests模组树状图设计](https://www.mczfw.com/blog/19277.html) - MCZFW (抓取失败)

### 英文来源
12. [The Quest Book gives way too many rewards that break balance and progression](https://github.com/AllTheMods/ATM-10/discussions/3539) - GitHub ATM-10 Discussion #3539
13. [Better Tutorialisation of Basic Mechanics](https://github.com/Omicron-Industries/Monifactory/issues/2359) - GitHub Monifactory Issue #2359
14. [Questbook Issues](https://github.com/Omicron-Industries/Monifactory/issues/28) - GitHub Monifactory Issue #28
15. [I made a modpack focused on progressing through technological ages](https://www.reddit.com/r/feedthebeast/comments/1th6g3a/) - Reddit r/feedthebeast (正文未能抓取)
16. [It's 2025. Is a balanced semigated pack with quests](https://www.reddit.com/r/feedthebeast/comments/1ie08cv/) - Reddit r/feedthebeast (正文未能抓取)
17. [The five tiers of mod complexity](https://www.reddit.com/r/feedthebeast/comments/a252mt/) - Reddit r/feedthebeast (正文未能抓取)
18. [Quest Design Best Practices](https://www.meegle.com/en_us/topics/game-design/quest-design) - Meegle

### GitHub仓库
19. [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) - Discussions & Issues
20. [Omicron-Industries/Monifactory](https://github.com/Omicron-Industries/Monifactory) - Issues

---

## 附录：搜索限制与后续建议

### 未能获取的关键内容
1. **Reddit帖子正文**：所有Reddit帖子均因反爬机制无法通过WebFetch获取。建议后续使用Reddit API或手动访问。
2. **Bilibili文章**：JS渲染导致内容无法抓取。Vazkii整合包制作文章和科技向整合包推荐文章可能包含重要设计思路。
3. **MC百科论坛帖子**：部分帖子抓取失败(如mcmod.cn/post/6155.html)。
4. **GTNH中文维基阶段页面**：Cloudflare安全阻断。

### 建议的后续搜索
1. 手动访问Reddit r/feedthebeast搜索 "modpack design" "quest progression" 相关帖子
2. 使用YouTube搜索 "modpack quest design" 视频(有字幕的更易提取)
3. 访问MC百科的GTNH页面了解其阶段划分体系
4. 搜索CurseForge上E2E/E9E/Monifactory等Expert包的项目README或Wiki
5. 查找FTB Quests官方文档中关于阶段管理的最新说明
