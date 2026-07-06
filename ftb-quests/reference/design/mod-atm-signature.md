# Module: ATM Signature Patterns — ATM 专属还是通用？

> ⚠️ **适用范围警告：** 以下模式的核心证据全部来自 AllTheMods 系列包（ATM-8/9/10/10-Sky）。
> 概念可借鉴，但实现细节反映 ATM 的设计哲学。非 ATM 包作者使用前请验证适用性。

## Quick Reference

| ID | 名称 | 概念通用性 | 实现专属度 | 阶段 |
|---|---|---|---|---|
| MP4 | Escalation Ladder | 通用概念 | ATM kill-count 实现 | Step 4 |
| MP16 | XP Drip | 通用概念 | ATM generous reward 实现 | Step 4 |
| MP20 | Shape-as-Tier Signal | 通用概念 | ATM 47% shape 实现 | Step 2 |
| MP21 | Dimension-as-Stage-Gate | 通用概念 | ATM welcome quest 实现 | Step 2 |
| MP22 | Material-Tier Spine | 部分通用 | ATM 三金属 spine | Step 2 |

---

## Patterns

### MP4 — Escalation Ladder（Kill/Stat 递增）

**概念：** 同一活动类型的 quest chain，每个 quest 的 `value` 递增（5 → 10 → 25 → 50 → 100），reward 也同步升级。dependency chain 让 progression 可见且 gated。

**ATM 实现（Bounty Board）：** ATM-10 的 bounty_board chapter 有 87 个 kill task，按 mob type 组织为 escalation ladder。zombie ladder：5→10→25→50→100 kills，每个依赖前一个。第一个 quest `hide_until_deps_visible: false`（始终可见），后续 `true`（progressive reveal）。reward 从 5 rotten_flesh + 10 XP 升级到 random loot table + 25 XP + rare drops + 50 XP。

```
# ATM-10 bounty_board — zombie ladder 前两步
{ hide_until_deps_visible: false
  tasks: [{ entity: "minecraft:zombie", type: "kill", value: 5L }]
  rewards: [{ item: "minecraft:rotten_flesh", count: 5 }, { type: "xp", xp: 10 }] }
{ dependencies: ["2B05A29C..."]
  hide_until_deps_visible: true
  tasks: [{ entity: "minecraft:zombie", type: "kill", value: 10L }]
  rewards: [{ type: "random", table_id: 487623... }, { type: "xp", xp: 25 }] }
```

**数据：** ATM-10（87 kill tasks）、ATM-9（类似 bounty board）、ATM-10-Sky（skyblock 变体）。纯 tech/expert 包通常不使用此模式，Create 系列无 escalation ladder 证据。

#### Non-ATM Applicability
Escalation ladder 的**概念**（activity + escalating value）完全通用，但实现需要包内有 **可重复的 grind activity**——mob grind、farming、mining 等。RPG 包可用 boss-kill escalation（1→3→5 boss kills）。Expert 包通常不需要，因为 progression 由 recipe chain 自然递增。Create 包可能用 automation throughput escalation（100→500→2000 items processed）。关键判断：包内是否有 mob-grind 或类似 loop？有则适用，没有则跳过。

---

### MP16 — XP Drip（每 quest 给 XP）

**概念：** 每个 quest 给少量 XP 作为 baseline reward，milestone quest 给更多 XP 或 XP levels。steady progression sense without item-economy inflation。

**ATM 实现：** ATM-10 全面使用 XP drip——welcome chapter 每 quest 10 XP，Mekanism chapter 按 10/50/100 XP tier 递增，ATM Star capstone 给 50 XP levels。设计哲学 explicit（Discussion #3539）：generosity is density——许多小 reward，而非少数大 reward。

**数据量化：** ATM-10 有 6,915 rewards / 4,601 quests = 1.5 rewards/quest。ATM-9 为 1.7/quest，ATM-8 为 1.7/quest。Create: Delight 为 0.43/quest，Mechanomania 为 0.11/quest——XP drip 与 ATM 的 generous philosophy 绑定，非 ATM 包明确不使用。

#### Non-ATM Applicability
XP drip 是**设计哲学选择**而非技术模式。Kitchen-sink 包如果追求 generous feel 可借鉴 10-50-100 XP tier 结构。Expert 包的 reward 系统不以 XP 为核心（Monifactory 侧重 machine unlock 和 stage progression），XP drip 与 expert philosophy 冲突。Create 包数据明确不支持（0.11–0.43 rewards/quest）。**判断标准：** 你的包追求"reward density"还是"earned milestone"？前者用 XP drip，后者不用。

---

### MP20 — Shape-as-Tier Signal

**概念：** chapter 内不同 quest shape 代表不同 tier/category/difficulty。shape vocabulary 承载语义信息，玩家无需读 title 就能识别 quest 类型。

**ATM 实现：** ATM-10 拥有所有审计包中最丰富的 shape vocabulary：Mekanism=`hexagon`（energy/hive）、Create=`gear`（machinery）、AllTheModium=`diamond`（material/tier）、basic_armor=`rsquare`（armor/special）、welcome=`pentagon`（milestone）。~47% 的 ATM-10 quests 设置 explicit shape，而 curated packs 仅 3–8%。这是 ATM 的视觉设计签名。

**数据：** AllTheModium chapter 内 `default_quest_shape: "diamond"`，tier-gate quest 用 `gear` 或 `hexagon` size 1.5–2.0。tool variant 用 `rsquare` at y=-1，armor variant 用 `octagon` at y=+1。shape 告诉玩家 quest KIND without reading title。

#### Non-ATM Applicability
Shape-as-tier 的概念（视觉编码 = 语义信息）通用，但 ATM 的 **47% explicit shape** 用法是其独有的设计投入。大多数 curated/expert 包用 3-8% shape override，依赖 default shape 统一性。非 ATM 包如果要用此模式：(1) 限制 shape vocabulary 到 2-3 种（如 milestone=`hexagon`、routine=default）；(2) 跨 chapter 保持一致映射；(3) 不要追求 ATM 级别的 shape richness——它的维护成本很高。**判断标准：** 你的包有 >20 chapters 且需要跨 chapter 视觉一致性吗？有则投资 shape vocabulary，没有则用 default shape + milestone 例外即可。

---

### MP21 — Dimension-as-Stage-Gate

**概念：** 进度需要到达新 dimension，dimension entry 本身是 gate。dimension task auto-complete on entry，后续 quest 依赖它解锁。

**ATM 实现：** ATM-10 welcome chapter 的 root quest 是 `dimension: "minecraft:overworld"`——玩家做的第一件事就是"踏入 overworld"。更复杂的 dimension gate 出现在 Twilight Forest、Undergarden、Bumblezone chapters——每个 dimension 对应一个 welcome quest + dimension-locked content。

**数据：** ATM-10、ATM-9、ATM-10-Sky 均使用 dimension gates。尚无独立 non-ATM kitchen-sink 包验证此模式。RPG/adventure 包（Prominence II）使用 dimension tasks 但方式不同（dimension 与 biome、structure 混合使用，不是独立的 stage gate）。

#### Non-ATM Applicability
Dimension-as-gate 的概念完全通用——任何有 dimension progression 的包都可以用 `dimension` task 做 stage boundary。ATM 的独特之处在于 **每个 dimension 都有一个 welcome quest 作为 chapter root**——这是一种系统化的组织方式。非 ATM 包可以：(1) 在 dimension 入口处放一个 dimension task（最简实现）；(2) 将 dimension gate 与 dimension-specific chapter 绑定（ATM 做法）；(3) 用 dimension task 作为 cross-chapter dependency 的 anchor（expert 做法）。**判断标准：** 你的包有 dimension progression 吗？有则 dimension task 是自然 gate，无则跳过。

---

### MP22 — Material-Tier Spine（跨维度材料主线）

**概念：** 材料 hierarchy 跨越多个 dimension/chapter，tier progression 是包的 backbone。每级 reward 包含采集下一级 ore 所需的 tool。

**ATM 实现：** AllTheModium（Overworld/Deep Dark, netherite pick）→ Vibranium（Nether, ATM pick）→ Unobtainium（End, vibranium pick）→ ATM Star（capstone）。三个 dimension，三个 tier，one pick-per-tier gate。

实现在 dedicated chapter（`allthemodium.snbt`，`default_quest_shape: "diamond"`，54 quests）。3-4 columns（tools, armor, weapons, utilities），每个 column 独立升级。`hexagon` cross-link nodes 在 tier boundary 连接 columns。`hide_dependency_lines` 在 31/54 quests 上——所有审计 chapter 中最重的使用。

**数据：** ATM-10、ATM-9、ATM-8、ATM-10-Sky 均有三金属 spine。non-ATM kitchen-sink 包中**未观察到**类似 spine。

#### Non-ATM Applicability
Material-tier spine 的**概念**（材料等级作为 progression backbone）在 expert 包中以不同形式存在——GregTech 的 voltage tier（Monifactory LV→MV→HV→EV→...）本质上就是 material-tier spine。但 ATM 的实现（三金属跨维度）是 ATM 独有。非 ATM 包的适配方式：(1) Expert 包已有 voltage tier 或 tech age 作为 spine，不需要额外 material spine；(2) RPG 包可用 weapon/armor tier（wood→iron→diamond→netherite）作为 spine；(3) Skyblock 包可用 resource processing tier（sieve→hammer→crook→machine）作为 spine。**关键：** 你的包需要一个跨 chapter 的 progression backbone 吗？如果需要，选择一个与你包 genre 匹配的 spine 类型——ATM 的三金属 spine 只是其中一种实现。

---

## Cross-References

| 相关模块 | 关系 |
|---|---|
| `mod-reward-design` | MP4/MP16 的通用 reward 概念在该模块；ATM 实现数据在此模块 |
| `mod-description-trust` | ATM 47% shape 意味着描述中引用 shape 语义时需注意一致性 |
| `mod-system-safety` | R30 Visual Hierarchy 参考 MP20 的 shape vocabulary 做 milestone 判定 |
| `mod-item-reachability` | MP22 material-tier spine 的跨维度物品可达性由 R1/R2 覆盖 |

---

## Sources

- AllTheMods/ATM-10（4,601 quests / 64 chapters，full config access）
- AllTheMods/ATM-9（~2,300 quests / 67 chapters）
- AllTheMods/ATM-8（~1,000 quests / 32 chapters）
- AllTheMods/All-the-mods-10-Sky（~2,860 quests / 52 chapters）
- Scope Annotation Table（micro-patterns.md，† ATM Signature 标注）
