# Phase 3 Cycle 8 — 审查结论 + 修改摘要

## 审查结论

### 可编码性评估

Phase 3 Cycle 8 提出了 8 条候选进度校验规则（PR1-PR8），审查按"是否真的可以编码为自动化检查"逐条评估：

| 候选规则 | 可编码性 | 审查结论 | 理由 |
|---|---|---|---|
| PR1 奖励-阶段匹配 | 高 | **通过 — 编码为 R44** | stage_tag 映射 + 数值比较，伪代码完整可实现 |
| PR2 教学-实践顺序 | 中 | **部分通过 — 由 R14 覆盖** | R14（Teach-Then-Do Ordering）已实现核心检查逻辑。PR2 的"复杂系统识别"（description > 200 字符阈值）是 R14 的增强方向，不单独建规则 |
| PR3 阶段过渡平滑 | 中 | **未编码 — 人类审查项** | 需要 DPS/效率数值比较，依赖外部游戏平衡数据，FTB Quests 配置层无法获取。已作为"人类审查项"写入阶段划分四维模型 |
| PR4 阶段内物品可达性 | 高 | **通过 — 编码为 R42** | recipe tree 遍历 + stage resource table 查询，伪代码完整可实现 |
| PR5 Stage-Quest 因果链无环 | 高 | **通过 — 编码为 R43** | 扩展依赖图 + 拓扑排序，与 R5 形成分层环检测 |
| PR6 弱锁设计 | 低 | **未编码 — 人类审查项** | "非预期路径"识别需要深层 mod 交互知识，无法从 FTB Quests 配置推断。已作为设计策略写入 mod-item-reachability.md |
| PR7 奖励引导衔接 | 高 | **通过 — 编码为 R45** | chapter capstone reward ∩ next chapter entry task 集合运算，伪代码完整可实现 |
| PR8 多人共享进度奖励去重 | 中 | **未编码 — 记录为未来方向** | "进度是否共享"需要从 pack 配置推断，FTB Quests 的 team/progression 设置复杂。当前作为 R44 的附带说明提及 |

**总结：** 8 条候选规则中 4 条（PR1/PR4/PR5/PR7）编码为自动化检查规则（R42-R45），1 条（PR2）由现有 R14 覆盖，3 条（PR3/PR6/PR8）标记为人类审查项或未来方向。

### 来源可靠性评估

**一手来源（高可靠）：**
- GitHub Issues（Monifactory #2359, #28）—— 来自实际包的 issue tracker，由包维护者或活跃玩家提出，反映真实设计问题
- GitHub Discussions（ATM-10 #3539）—— 包含包协作者（TheBedrockMaster）和玩家（xiaoxiao921）的直接对话，双方观点均有记录
- **评估：** 这些来源代表实际项目中的设计争论，可靠性最高。但需注意：GitHub 讨论中的个人观点不一定代表团队共识。TheBedrockMaster 作为 ATM-10 协作者的观点权重高于普通玩家，但仍非官方声明

**二手来源（中可靠）：**
- MC百科文章（mcmod.cn/post/4382.html, bbs.mcmod.cn/thread-21004-1-1.html, mcmod.cn/post/1416.html）—— 中文社区成员撰写的设计思路总结，包含作者个人观点和实践经验
- CSDN 文档（wenku.csdn.net/doc/6amfp2j2im）—— 对 FTB Quest + GameStages 集成模式的技术描述
- **评估：** 这些是社区经验总结而非 FTB Team 官方文档。技术描述部分（Game Stages 架构、集成模式）可通过代码验证，设计建议部分（弱锁策略、三段式生命周期）代表作者个人设计哲学。可信度中等，作为设计参考而非权威标准

**通用来源（低特异性）：**
- Meegle 通用任务设计原则（meegle.com）—— 通用游戏设计理论，非 Minecraft/FTB Quests 特化
- **评估：** 提供理论框架（风险与奖励平衡、有意义的奖励），但缺乏 modpack 领域的具体验证。作为理论支撑使用，不作为独立证据

**未获取的来源（影响完整性）：**
- Reddit 帖子正文（3 篇）因反爬机制未能抓取
- Bilibili 文章（Vazkii 整合包制作）因 JS 渲染未能完整抓取
- GTNH 中文维基阶段页面因 Cloudflare 阻断未能访问
- **影响评估：** 缺失的来源主要影响阶段划分和 Expert 包设计策略的覆盖度，核心规则候选（PR1-PR8）的来源不受影响

### 一致性审查

**无冲突的规则：**

| 新规则 | 对应现有规则 | 关系 |
|---|---|---|
| R42 (PR4) | R1 (Dimension-Reachability), R4 (Stage Boundary) | 细化补充：R1 检查物品维度可达，R4 检查物品阶段归属，R42 检查物品合成链在阶段内的完整可达性。三者形成递进关系，无冲突 |
| R43 (PR5) | R5 (Circular Dependency Detection) | 分层补充：R5 检测 quest 层面的环，R43 检测 Stage-Quest 交叉层面的环。R43 是 R5 的超集扩展，无冲突 |
| R44 (PR1) | R12 (Reward Value Progression), R37 (Capstone-Only Progression Break) | 互补：R12 检查奖励价值递增趋势，R37 定义不同包类型的安全阈值，R44 检查单个奖励是否越级。三者从不同角度覆盖奖励安全性，无冲突 |
| R45 (PR7) | R10 (Reward-to-Dependent Bridge) | 层级扩展：R10 在 quest 级别检查奖励-依赖桥接，R45 在 chapter 级别检查完成奖励-下一章入口的桥接。无冲突 |

**无冲突的设计概念：**
- 弱锁策略（PR6）与 R1-R4 的严格可达性检查互补而非矛盾：R1-R4 保证正常路径可达，弱锁策略描述非正常路径的设计哲学
- 四维阶段模型与现有 MP19（Chapter-as-Stage）一致：MP19 描述章节结构，四维模型描述阶段划分的设计维度
- 教学快速推入策略与 R14（Teach-Then-Do）和 R41（Early-Game Flexible）形成三层框架，互相支撑

**潜在张力（已解决）：**
- R44 的 stage+1 阈值 vs R37 的 kitchen-sink capstone-only 阈值：通过差异化严重度解决（expert ERROR / kitchen-sink WARNING），R44 描述中明确引用 R37 的阈值逻辑
- progression_mode 对 R9 阈值的影响：在阶段划分模型的 progression_mode 段落中明确说明，R9 的 MAX_DEPTH 阈值需要考虑 progression_mode

---

## 已执行的修改

### mod-item-reachability.md

**风险等级：低风险（追加新段落和新规则）**

1. **扩展 Game Stages 章节**（Patterns 区域）：
   - 新增"Game Stages 闭环集成的技术架构"段落：描述 1.12.2 标准工具链（Game Stages + Item Stages + Recipe Stages + CrT）、现代版本演进（1.20+ KubeJS 替代）、闭环核心模式（任务完成 → Stage 激活 → 配方解锁）、多维联动设计（时间/空间/资源/社会四维度）
   - 新增"弱锁策略：允许跳关但奖励孤立化"段落：描述弱锁设计哲学、与 R1-R4 的互补关系、Item Stages/Recipe Stages 实现方式、可编码性低的标注（人类审查项）

2. **新增 R42 规则**（Rules 区域）：
   - 标题：Stage-Internal Item Reachability（合成链阶段内可达性）
   - 完整伪代码：构建合成树 → 遍历叶子节点 → 检查维度/阶段/资源可达性
   - 与 R1/R4 的关系说明
   - Quick Reference 表格新增 R42 行

### mod-dependency-graph.md

**风险等级：低风险（追加新段落和新规则）**

1. **新增 R43 规则**（Rules 区域）：
   - 标题：Stage-Quest Causal Chain Acyclic（Stage-Quest 因果链无环）
   - 完整伪代码：构建扩展依赖图（含 Stage 节点）→ 添加 Quest→Stage 激活边和 Stage→Quest 解锁边 → 环检测
   - 与 R5 的关系说明（分层环检测）
   - Quick Reference 表格新增 R43 行

2. **新增"阶段划分的四维模型"段落**：
   - 描述时间/空间/资源/社会四个维度
   - 阶段划分基本原则（3-7 阶段、解锁边界、后期复用早期系统）
   - 三段式生命周期
   - 阶段过渡平滑原则（人类审查项）

3. **新增"progression_mode 对阶段结构的设计影响"段落**：
   - linear vs flexible 对依赖图拓扑的影响
   - 与 R9 阈值设置的交互关系

### mod-reward-design.md

**风险等级：低风险（追加新段落和新规则）**

1. **新增 R44 规则**（Rules 区域）：
   - 标题：Reward-Stage Matching（奖励-阶段匹配）
   - 完整伪代码：stage_tag 比较 + 包类型差异化阈值
   - 与 R12/R37 的关系说明
   - 人类审查项标注（挑战绕过检查）
   - ATM-10 典型案例
   - Quick Reference 表格新增 R44 行

2. **新增 R45 规则**（Rules 区域）：
   - 标题：Reward Guidance Bridging（奖励引导衔接）
   - 完整伪代码：capstone rewards ∩ next chapter entry tasks 集合运算
   - 与 R10/MP14 的关系说明
   - 人类审查项标注（跨模组扫荡性机制）
   - Quick Reference 表格新增 R45 行

3. **新增"ATM-10 奖励跨级争议"段落**：
   - xiaoxiao921 vs TheBedrockMaster 的完整争论梳理
   - 厨房水槽 vs Expert 的安全阈值分水岭分析
   - 与 R37/R44 的关系

### mod-teaching-pacing.md

**风险等级：低风险（追加新段落）**

1. **新增"早期教学快速推入策略"段落**：
   - 描述时间窗口问题
   - 前 3-5 个任务的设计要求
   - 与 R14/R41 的三层教学框架关系

2. **新增"Monifactory #2359：教学不足的典型失败案例"段落**：
   - LunatiK-ExpiX 的 issue 详述
   - Aqueous Accumulator 30 分钟浪费案例
   - AP5 vs 教学不足的区别分析
   - FTB Quests 多任务类型的教学组合方案
   - 与 MP11/R14/MP23 的关系

---

## 未执行的修改

| 候选规则 | 原因 | 建议 |
|---|---|---|
| PR2 教学-实践顺序（独立规则） | 与现有 R14 功能重叠。PR2 的"复杂系统识别"（description > 200 chars 阈值）是 R14 的潜在增强方向，但不需要独立规则 | 未来可作为 R14 的增强补丁：增加"复杂物品"注册表，自动识别需要教学的物品 |
| PR3 阶段过渡平滑 | 需要 DPS/效率数值数据，FTB Quests 配置层无法获取。伪代码依赖外部游戏平衡数据库 | 作为人类审查项保留。如果未来有包提供阶段挑战数据（如怪物 HP/DPS 表），可升级为自动化检查 |
| PR6 弱锁设计 | "非预期路径"需要深层 mod 交互知识，无法从配置推断 | 作为设计策略写入 mod-item-reachability.md。可编码性低，保持为人类审查项 |
| PR8 多人共享进度奖励去重 | "进度是否共享"需要复杂的 pack team/progression 配置解析 | 记录为未来方向。当前 R44 的描述中提及多人场景但未编码独立规则 |
| D5 可选内容设计策略 | 发现内容（optional: true 的应用规则、KS vs Expert 的可选定义差异）与现有 R7（Optional-Gate-Mandatory）和 AP19（Optional-but-Mandatory Mislabel）高度重叠 | 不写入。现有规则已覆盖核心检查逻辑。包类型差异已在 R7 的描述中通过 pack_type 参数体现 |

---

## 新增规则编号分配

| 新规则编号 | 候选来源 | 标题 | 所在模块 |
|---|---|---|---|
| R42 | PR4 | Stage-Internal Item Reachability（合成链阶段内可达性） | mod-item-reachability.md |
| R43 | PR5 | Stage-Quest Causal Chain Acyclic（Stage-Quest 因果链无环） | mod-dependency-graph.md |
| R44 | PR1 | Reward-Stage Matching（奖励-阶段匹配） | mod-reward-design.md |
| R45 | PR7 | Reward Guidance Bridging（奖励引导衔接） | mod-reward-design.md |

**编号连续性说明：** 现有规则序列为 R1-R41。新增 R42-R45 延续序列。所有新规则的编号已在对应模块文件的 Quick Reference 表格中注册。
