# FTB Quests — Progression Rules [ARCHIVED]

> **ARCHIVED:** This file has been superseded by the modular system.
> Content redistributed to: `shared-builtin-tables.md`, `mod-item-reachability.md`, `mod-dependency-graph.md`, `mod-reward-design.md`, `mod-teaching-pacing.md`, `mod-description-trust.md`, `mod-system-safety.md`.
> Kept for git history reference. See `module-index.md` for the current structure.

---

## Section Navigation & Load Phase

| Section | Content | SKILL.md Step | Load timing |
|---|---|---|---|
| §执行优先级表 | 每条规则的执行阶段标注 | — | 始终参考 |
| §0 降级策略与内置映射 | Fallback strategy & builtin lookup tables | Step 4/5 | 与规则同步加载 |
| §1 Item Reachability (R1–R4) | 物品可达性检查 | Step 4 (局部) / Step 5 (全局) | 分阶段执行 |
| §2 Dependency Integrity (R5–R9) | 依赖图结构健康 | Step 4 (增量) / Step 5 (全图) | 分阶段执行 |
| §3 Reward Continuity (R10–R13) | 奖励连贯性检查 | Step 4 (反向) / Step 5 (前向) | 分阶段执行 |
| §4 Teaching Order (R14–R17) | 教学顺序检查 | Step 5 (validation) | 整体验证阶段 |
| §5 Pacing (R18–R22) | 进度节奏检查 | Step 4 (R18/R22) / Step 5 (其余) | 分阶段执行 |
| §6 Description Consistency (R23) | 描述-物品一致性 | Step 4 (node generation) | 逐节点生成时 |
| §7 Suggestion & Necessity (R24–R26) | 建议可达性 / 任务必要性 / 版本一致性 | Step 4 (局部) / Step 5 (全局) | 分阶段执行 |
| §8 Safety & Team (R28–R29) | Command reward 安全 / 团队进度一致性 | Step 4 (R28) / Step 5 (R29) | 分阶段执行 |
| §9 QA & Formatting Standards (R30–R32) | Quest 视觉层级 / XP 奖励相对性 / Chapter QA 覆盖 | Step 4 (R31) / Step 5 (R30/R32) | 分阶段执行 |
| §执行优先级 | 规则执行顺序 | — | 参考 |
| §AP 映射表 | Anti-pattern ↔ Rule 对应 | — | 参考 |

> **注意：** 本文档规则按两阶段模型执行。**Step 4（逐节点生成）** 运行仅需局部数据的规则子集（R7/R18/R22/R23 的直接检查 + R1-R4 的 L1 降级版 + R5/R6 的增量版 + R10 的反向检查 + R28 的 command 安全扫描 + R31 的 XP 奖励检查）。**Step 5（整体验证）** 运行需要完整依赖图的规则（全量 R5/R6/R20 + 前向 R10/R11 + 统计类 R9/R12/R13/R15/R19 + R29 团队一致性 + R30 视觉层级 + R32 QA 覆盖）。**外部脚本** 处理需要运行时数据的规则（AP12 NBT/AP13 状态机/隐式循环）。参见下方 §执行优先级表。

---

进度校验规则。本文档定义了 AI 在生成 quest 配置时自动执行的检查逻辑，用于捕获三类核心问题——物品跨级、顺序倒置、奖励断链——以及它们的衍生形态。每条规则都足够具体，可以转化为 `validate_quests.py` 中的一个检查函数。

## Summary

这份规则集来自对 18 个已发布整合包的配置审计（ATM-10、ATM-9、ATM-8、ATM-10-Sky、Create: Delight Remake、Mechanomania、Monifactory、Arcana、All-the-Mons、Create: Astral、Prominence II、Create Skylands、Enigmatica 9 Expert、GTNH、FTB Interactions Remastered、Craftoria、Enigmatica 10、FTB Architect's Exodus），以及来自 cesspit.net 的深度 expert-pack 分析、FTBTeam/FTB-Modpack-Issues 的 60+ 条玩家反馈审计（覆盖 FTB Evolution、Architect's Exodus、StoneBlock 4、Skies 2、Interactions Remastered）、E2E Extended 和 GTNH 的 README 设计文档、awesome-packdev 社区的工具链梳理、Laskyyy/Create-Astral 的 issue tracker 设计讨论、Omicron-Industries/Monifactory 的 CONTRIBUTING.md quest book 格式标准、以及 TeamAOF/Craftoria 和 EnigmaticaModpacks/Enigmatica10 的 issue tracker 设计反馈。

规则分为七类。第一类 **Item Reachability** 检查任务物品在当前阶段是否可获得——这是玩家最容易感知的问题，一个要求 netherite ingot 的任务出现在玩家还没进 Nether 的阶段，体验立刻崩塌。第二类 **Dependency Integrity** 检查依赖图的结构性健康——循环依赖、不可达 quest、optional gate  mandatory content。第三类 **Reward Continuity** 检查 reward 是否引导玩家走向下一步——dead-end reward 是 quest book 丧失引导力的主因。第四类 **Teaching Order** 检查教学顺序——先教后做、先简单后复杂、先工具后使用。第五类 **Pacing** 检查节奏合理性——reward 通胀、bottleneck 密度、描述覆盖率。第六类 **Suggestion & Necessity** 检查描述文本中「建议」的物品是否同样可达、任务要求是否过度严格、quest 文本是否跟随 mod 版本更新——这些是前五类规则的语义补充，覆盖了 description 作为「引导文本」而非「配置数据」时的独有问题。第七类 **QA & Formatting Standards** (R30–R32) 检查 quest book 的呈现层和测试覆盖层——视觉层级是否反映进度语义、XP 等级奖励是否随玩家等级漂移、chapter 是否通过基本 QA 启发式检查——覆盖了「quest 看起来对不对」和「quest 书被测试过吗」两个常被忽视的维度。

这七类规则共同构成一个静态校验管线。它们在 `generate_quests.py` 的 Step 5 整体验证阶段运行，对 spec 和生成的配置执行非破坏性检查，将结果分为 error（必须修复）、warning（建议修复）、info（可忽略但值得知道）三级。

---

## 执行优先级表（Execution Priority Table）

每条规则按执行阶段分类。Step 4 的规则在逐节点生成时同步检查，失败时立即提醒；Step 5 的规则在所有 quest 生成完毕后运行全图分析；外部脚本规则需要运行时数据或 JEI/EMI 配方图，无法由 AI agent 直接执行。

### Step 4 — 生成时检查（嵌入 per-node 循环）

生成每个 quest 时同步执行，数据在生成当前节点时已可用。失败行为按严重性分级。

| 优先级 | 规则 | 检查类型 | 失败行为 |
|---|---|---|---|
| **P0** | R23 Description-Item Consistency | 纯文本匹配 | ERROR — 阻止写入 spec |
| **P0** | R7 Optional-Gate-Mandatory | 局部依赖检查 | ERROR — 阻止写入 spec |
| **P0** | R22 Cross-Chapter Dependency Validity | 引用存在性 | ERROR — 阻止写入 spec |
| **P0** | R28 Command Reward Safety Scan | 命令字符串模式匹配 | ERROR (危险命令) / WARNING (高风险命令) |
| **P1** | R18 Description Coverage | 结构检查 | WARNING — 提醒用户 |
| **P1** | R10 (反向) Task→Ancestor Reward Bridge | 向后匹配 | WARNING — 提醒用户 |
| **P1** | R1 Dimension-Reachability (L1 only) | 内置映射检查 | `[unverified:dimension]` |
| **P1** | R16 Dimension-Explore-Then-Craft (向后) | ancestor dim task 检查 | WARNING |
| **P1** | R5 Circular Dependency (增量版) | 新节点 DFS | ERROR — 提醒用户修改 depends_on |
| **P1** | R6 Unreachable Quest (局部版) | dependency 存在性 | WARNING |
| **P2** | R17 Tool-Reward-Before-Use (反向) | ancestor tool reward 检查 | INFO |
| **P2** | R2 Tool-Tier (L1 only) | 内置映射检查 | `[unverified:tool_tier]` |
| **P2** | R3 Recipe Depth (L1 heuristic) | 名称启发式 | `[unverified:recipe_depth]` |
| **P2** | R4 Stage Boundary (降级版) | ancestor reward 向后检查 | `[unverified:stage]` |
| **P2** | R24 Suggestion-Reachability (L1 only) | 正则 + L1 | `[unverified:suggestion]` |
| **P2** | R31 XP-Level Reward Relativity | reward 类型检查 | WARNING |
| **P3** | AP10/AP11 self-check | 与最近 2-3 quest 比较 | INFO — style drift 提醒 |

### Step 5 — 验证时检查（全图分析）

所有 quest 生成完毕后运行，需要完整的依赖图数据。

| 优先级 | 规则 | 检查类型 |
|---|---|---|
| **P0** | R5 Circular Dependency Detection (完整 DFS) | 图遍历 |
| **P0** | R6 Unreachable Quest Detection (完整可达性) | 图遍历 |
| **P0** | R20 Chapter Completion Testability | 图遍历 |
| **P1** | R7 Optional-Gate-Mandatory (全局复查) | 全量检查 |
| **P1** | R10 Reward-to-Dependent Bridge (前向检查) | 全量匹配 |
| **P1** | R11 Reward-Target Accuracy | 全量匹配 + tool_category_map |
| **P1** | R14 Teach-Then-Do Ordering | 全量 depth 比较 |
| **P1** | R16 Dimension-Explore-Then-Craft (全量) | 全量检查 |
| **P1** | R29 Team Progression Consistency | 团队进度共享一致性 |
| **P2** | R1/R2/R3/R4 (完整 L1+L2 检查) | 全量 + 用户 L2 数据 |
| **P2** | R8 Dependency Requirement Consistency | LCA 分析 |
| **P2** | R9 Dependency Depth Reasonableness | chapter-level 统计 |
| **P2** | R12 Reward Value Progression | chapter-level 统计 |
| **P2** | R13 Capstone Reward Magnitude | chapter-level 统计 |
| **P2** | R15 Complexity Escalation | chapter-level 排序 |
| **P2** | R19 Bottleneck Spacing | chapter-level 序列分析 |
| **P3** | R17 Tool-Reward-Before-Use (全量) | 全量匹配 |
| **P3** | R21 Hidden Quest Signpost | 全量可见性分析 |
| **P3** | R24/R25/R26 (完整检查) | 全量 + L2/L3 数据 |
| **P3** | AP10 Style Homogenization | batch 统计 |
| **P3** | AP11 Batch Narrative Inconsistency | NLP + 交叉引用 |
| **P3** | R30 Quest Visual Hierarchy & Size Consistency | chapter-level size/shape 比较 |
| **P3** | R32 Chapter QA Coverage Heuristic | chapter-level 结构统计 |

### 外部脚本 — 需要运行时数据或工具链

以下规则/模式无法由 AI agent 在 Step 4 或 Step 5 中执行，需要外部工具或运行时测试。

| 规则/模式 | 所需外部工具 |
|---|---|
| R5 隐式循环（recipe graph） | `validate_quests.py` + JEI/EMI recipe graph export |
| R25 完整替代路径分析 | JEI/EMI 数据 + custom analysis script |
| R26 完整版本一致性 | packwiz lock file / modrinth API / CurseForge API |
| AP1 recipe 验证（"熔炉"vs"高炉"） | Step 5a in-game load-test |
| AP12 NBT Insensitivity | Step 5a in-game load-test |
| AP13 Premature Submission | Step 5a in-game load-test |
| PP7 Mod-Unification | `extract_items.py` 增加 duplicate display name 检测 |

> **设计原则：** Step 4 只做 3-5 个关键局部检查（P0 级 ERROR + P1 级 WARNING），其余推迟到 Step 5 全量分析。这比试图在 Step 4 执行所有规则但每个都做得不彻底要可靠得多。

---

## 0. 降级策略与内置映射

### 数据依赖总览

R1–R4（Item Reachability）是校验管线中价值最高但数据依赖最重的规则。审查发现，在没有外部数据（JEI/EMI 配方、mod 源码）的情况下，这些规则的降级策略过于保守——绝大多数物品被标记为 `[unverified]` 并跳过，使规则实质上成为空设。

为解决此问题，每条规则采用**三层数据策略**：

| 层级 | 数据源 | 覆盖范围 | 何时可用 |
|---|---|---|---|
| **L1 — 内置映射** | 下文硬编码的常识表 | ~20–50 个跨包常见物品 | 始终可用，无需任何外部数据 |
| **L2 — 用户/Step 2 提供** | 用户在 Step 2 interview 中定义的映射 | 包特有的关键物品 | 用户提供后可用 |
| **L3 — JEI/EMI 推断** | 从配方数据自动推断 | 全部物品 | 需要 toolchain 支持 |

规则执行时按 L1 → L2 → L3 优先级查找数据。L1 命中时直接检查，无需外部数据。仅当 L1 和 L2 都未命中时才降级为 `[unverified]`。这意味着即使没有任何外部数据，R1–R4 也能对 20–50 个最常见的 vanilla 和跨包物品执行有意义的检查。

每条规则的数据依赖标注格式：

```
**数据依赖：** ⚠️ 需要外部数据（L2/L3）才能完整运行 | ✅ 内置映射（L1）可独立检查常见物品 | 未知物品降级为 [unverified:xxx]
```

### 内置维度映射表（R1 L1）

以下维度-物品映射来自 vanilla Minecraft 游戏机制和常见 mod 的标志性物品。这些映射在所有包类型中稳定成立，不需要 JEI/EMI 验证。

```
BUILTIN_DIMENSION_MAP = {
    # === Vanilla ===
    "minecraft:blaze_rod":              "minecraft:the_nether",
    "minecraft:blaze_powder":           "minecraft:the_nether",
    "minecraft:ghast_tear":             "minecraft:the_nether",
    "minecraft:nether_wart":            "minecraft:the_nether",
    "minecraft:quartz":                 "minecraft:the_nether",
    "minecraft:nether_star":            "minecraft:the_nether",
    "minecraft:ancient_debris":         "minecraft:the_nether",
    "minecraft:netherite_scrap":        "minecraft:the_nether",
    "minecraft:netherite_ingot":        "minecraft:the_nether",
    "minecraft:ender_pearl":            "minecraft:the_end",
    "minecraft:ender_eye":              "minecraft:the_end",
    "minecraft:dragon_egg":             "minecraft:the_end",
    "minecraft:dragon_breath":          "minecraft:the_end",
    "minecraft:elytra":                 "minecraft:the_end",
    "minecraft:shulker_shell":          "minecraft:the_end",
    "minecraft:chorus_fruit":           "minecraft:the_end",
    # === Common mod dimensions ===
    "twilightforest:liveroot":          "twilightforest:twilight_forest",
    "twilightforest:naga_scale":        "twilightforest:twilight_forest",
    "twilightforest:carminite":         "twilightforest:twilight_forest",
    "the_bumblebee:bee_stinger":        "the_bumblezone:the_bumblezone",  # if present
    "undergarden:cloggrum_ingot":       "undergarden:undergarden",
    # === ATM series signature ===
    "allthemodium:allthemodium_ingot":  "minecraft:overworld",   # deep dark variant
    "allthemodium:vibranium_ingot":     "minecraft:the_nether",
    "allthemodium:unobtainium_ingot":   "minecraft:the_end",
}
```

### 内置工具等级映射表（R2 L1）

以下工具等级来自 vanilla mining level 体系和常见 mod 的工具 tier 设计。Mining level 遵循 vanilla tag 体系（`minecraft:needs_iron_tool` 等），可从 block tag 推断。

```
BUILTIN_TOOL_TIER_MAP = {
    # === Vanilla mining levels (0=wood, 1=stone, 2=iron, 3=diamond, 4=netherite) ===
    "minecraft:wooden_pickaxe":     0,
    "minecraft:stone_pickaxe":      1,
    "minecraft:iron_pickaxe":       2,
    "minecraft:diamond_pickaxe":    3,
    "minecraft:netherite_pickaxe":  4,
    # === Common mod tool tiers ===
    "allthemodium:allthemodium_pickaxe":   5,
    "allthemodium:vibranium_pickaxe":      6,
    "allthemodium:unobtainium_pickaxe":    7,
    "mekanism:atomic_disassembler":        5,
    # === Machine tiers (rough: 1=basic, 2=advanced, 3=elite, 4=ultimate) ===
    "mekanism:metallurgic_infuser":        1,
    "mekanism:enrichment_chamber":         1,
    "mekanism:chemical_infuser":           2,
    "mekanism:electrolytic_separator":     1,
    "mekanism:fission_reactor_casing":     4,
    "mekanism:induction_casing":           3,
    "create:mechanical_press":             1,
    "create:mixer":                        1,
    "create:crushing_wheel":               1,
}

# Ores that require specific mining levels
BUILTIN_ORE_REQUIREMENTS = {
    "minecraft:diamond_ore":          2,   # iron+
    "minecraft:deepslate_diamond_ore":2,
    "minecraft:ancient_debris":       3,   # diamond+
    "minecraft:emerald_ore":          2,
    "minecraft:gold_ore":             2,
    "allthemodium:allthemodium_ore":  4,   # netherite+
    "allthemodium:vibranium_ore":     5,   # ATM pick+
    "allthemodium:unobtainium_ore":   6,   # vibranium pick+
}
```

### 内置合成深度估算启发式（R3 L1）

对于没有 JEI/EMI 配方数据的物品，使用物品名称和 mod namespace 推断粗略的合成深度。这远不如实际配方展开准确，但比完全跳过（`[unverified]`）好——至少能捕捉到明显的深度不匹配。

```
def estimate_recipe_depth_heuristic(item_id: str) -> int:
    """
    粗估合成深度。返回值为估算深度，-1 表示无法估算。
    这不是精确的配方展开，而是一个基于命名约定的 heuristic。
    """
    namespace, name = item_id.split(":", 1) if ":" in item_id else ("minecraft", item_id)

    # Tier keyword → rough depth
    tier_keywords = {
        # depth 1: raw material, basic smelt/craft
        "ingot": 1, "nugget": 1, "gem": 1, "dust": 1, "ore": 0,
        "planks": 1, "stick": 1, "coal": 0,
        # depth 2: simple machine/component
        "plate": 2, "gear": 2, "rod": 2, "wire": 2, "circuit": 2,
        # depth 3: advanced component
        "processor": 3, "controller": 3, "module": 3, "cell": 3,
        "enriched": 3, "alloy": 2, "crystal": 2,
        # depth 5: elite assembly
        "assembly": 5, "reactor": 5, "core": 5, "frame": 4,
        "fusion": 6, "quantum": 6, "antimatter": 7,
        # depth 8+: endgame
        "star": 8, "creative": 10, "singularity": 8,
    }
    for keyword, depth in tier_keywords.items():
        if keyword in name:
            return depth
    return -1  # unknown → still degrades to [unverified:recipe_depth]
```

这个 heuristic 的误差范围约 ±2 级深度。对于 kitchen-sink 包（`ALLOWANCE` 默认 2），这已经足够捕捉「合成链 5 步深但 quest chain 只有 1 步」这类严重不匹配。对于 expert 包（合成链深度可达 15+），建议用户在 Step 2 提供关键物品的精确深度。

---

## 1. Item Reachability（物品可达性）

这类规则回答一个核心问题：**任务要求的物品，玩家在到达这个 quest 时是否已经能够获取？**

### R1 — Dimension-Reachability Check

**数据依赖：** ✅ 内置映射（L1）可独立检查 ~20 个常见 vanilla/mod 维度物品 | ⚠️ L2/L3 覆盖更多 mod 物品 | 未知物品降级为 `[unverified:dimension]`

**检查什么：** 每个 `ftbquests:item` task 引用的物品，是否来自一个当前 quest 依赖链已经解锁的维度。输入字段：quest 的 `dependencies`（递归展开到所有祖先 quest）、task 的 `item.id`、以及维度-物品映射表（优先使用 §0 `BUILTIN_DIMENSION_MAP`，用户 L2 映射可覆盖或扩展内置表）。

**怎么检查：** 首先加载 `BUILTIN_DIMENSION_MAP`（§0），再叠加用户在 Step 2 提供的 L2 映射。然后对每个 quest Q 执行以下判断：

```
for each quest Q:
    reachable_dimensions = union of dimensions unlocked by Q's ancestor chain
        (a "dimension" task in any ancestor unlocks that dimension;
         the Overworld is always reachable)
    for each item_task in Q.tasks:
        item_dim = (L2_dimension_map or BUILTIN_DIMENSION_MAP).get(item_task.item.id)
        if item_dim is not None and item_dim not in reachable_dimensions:
            ERROR: "Quest {Q.name} requires {item_task.item.id} from
                    dimension {item_dim}, but no ancestor unlocks it."
        elif item_dim is None:
            # L1 + L2 both miss → degrade gracefully
            INFO: "[unverified:dimension] {item_task.item.id} — no dimension mapping available."
```

「维度解锁」的判定依据有两种：(1) 祖先 quest 链中存在一个 `type: "ftbquests:dimension"` task 指向该维度；(2) 包的 gamestage 配置中该 quest 的祖先链包含对应 stage。如果两者都没有，则该维度视为未解锁。

对于 kitchen-sink 包（`progression_mode: "flexible"`），此规则降级为 warning——因为 flexible 模式下玩家可以自由探索，维度锁定是 soft gate。对于 expert/linear 包（`progression_mode: "default"` 或 `"linear"`），此规则为 error。

**违反了会怎样：** 玩家在无法进入的维度中寻找任务物品，要么完全卡住（linear 包），要么被迫跳出 quest book 的指导自行探索（flexible 包），quest book 作为引导系统的可信度下降。

**来源：** ATM-10 的 AllTheModium tier spine 设计——AllTheModium（Overworld）→ Vibranium（Nether）→ Unobtainium（End），每个维度由前一级的镐解锁（design guide §principles P2）；FTB Evolution issue #6447 中"heart of the sea requires red chalk"的 circular deadlock 案例表明，维度/物品可达性是玩家投诉的首要触发点。

---

### R2 — Tool-Tier Item Reachability

**数据依赖：** ✅ 内置映射（L1）覆盖 vanilla mining level + 常见 mod 工具/机器 | ⚠️ L2/L3 覆盖包特有的 ore/machine tier | 未知物品降级为 `[unverified:tool_tier]`

**检查什么：** 任务要求的物品是否需要特定工具等级才能采集或加工，而该工具在 quest 的祖先链中尚未获得。输入字段：task 的 `item.id`、工具等级映射（优先使用 §0 `BUILTIN_TOOL_TIER_MAP` + `BUILTIN_ORE_REQUIREMENTS`，L2 映射可扩展）、以及 quest 祖先链中已获得工具的集合。

**怎么检查：** 加载 `BUILTIN_TOOL_TIER_MAP` 和 `BUILTIN_ORE_REQUIREMENTS`（§0），叠加用户 L2 映射。然后：

```
for each quest Q:
    available_tools = collect all tool/machine rewards from Q's ancestors
                      + items craftable from ancestors' reward chains
    for each item_task in Q.tasks:
        required_tool = (L2_tool_map or BUILTIN_TOOL_TIER_MAP).get(item_task.item.id)
        required_mining = (L2_ore_map or BUILTIN_ORE_REQUIREMENTS).get(item_task.item.id)
        if required_tool is not None and required_tool not in available_tools:
            WARNING: "Quest {Q.name} requires {item_task.item.id} which needs
                      {required_tool}, but no ancestor provides it."
        elif required_mining is not None:
            available_mining = max(mining_level(t) for t in available_tools) if available_tools else 0
            if required_mining > available_mining:
                WARNING: "Quest {Q.name} requires {item_task.item.id} (mining level {required_mining}),
                          but best available pick is level {available_mining}."
        elif required_tool is None and required_mining is None:
            # L1 + L2 both miss → degrade
            INFO: "[unverified:tool_tier] {item_task.item.id} — no tool requirement data."
```

此规则的难点在于 `tool_requirement_map` 的构建——它需要从 JEI/EMI recipe 数据推断，或由用户在 Step 2 提供。静态分析器只能使用已有的映射数据；如果映射缺失，规则跳过该物品并标记 `[unverified:tool_tier]`。

**违反了会怎样：** 玩家看到了任务物品，知道它是什么，但无论怎么尝试都无法获取——因为挖掘它需要的镐还没解锁，或者加工它需要的机器还造不出来。这是 expert pack 中最常见的「卡关」原因。

**来源：** GTNH README 明确描述"using the tiers (basically ages of technology) from GregTech and allocates content of other mods to a fitting point"——每个物品被分配到其对应的 GregTech 电压等级，玩家必须按等级推进（GTNH GitHub README）；ATM-10 AllTheModium 章节的镐-等级锁定链（design guide §field-findings）；cesspit.net 描述的 expert pack 公式"you have to work hard to get to a specific goal"——目标之所以有意义，是因为工具等级确实是门槛。

---

### R3 — Recipe-Chain Depth vs Dependency-Depth

**数据依赖：** ✅ 内置启发式（L1）可粗估 ~30 类物品的合成深度 | ⚠️ 精度 ±2 级，expert 包建议 L2 补充 | 无法估算的物品降级为 `[unverified:recipe_depth]`

**检查什么：** 任务物品的合成链深度是否超过了 quest 在依赖图中的深度。输入字段：quest 的 `dependency_depth`（从 root 到该 quest 的最长路径长度）、task 的 `item.id`、合成深度映射（优先使用 §0 `estimate_recipe_depth_heuristic`，L2 精确数据可覆盖）。

**怎么检查：** 合成链深度指一个物品从最原始原料到最终成品需要经过多少个合成步骤。规则判断：

```
for each quest Q:
    quest_depth = dependency_depth(Q)  # longest path from any root to Q
    for each item_task in Q.tasks:
        # L2 exact data first, then L1 heuristic, then degrade
        recipe_depth = L2_recipe_depth.get(item_task.item.id)
        if recipe_depth is None:
            recipe_depth = estimate_recipe_depth_heuristic(item_task.item.id)  # §0
        if recipe_depth >= 0 and recipe_depth > quest_depth + ALLOWANCE:
            WARNING: "Quest {Q.name} (depth {quest_depth}) requires
                      {item_task.item.id} (recipe depth {recipe_depth}).
                      The crafting chain may be deeper than the quest chain."
        elif recipe_depth < 0:
            # Heuristic couldn't estimate → degrade
            INFO: "[unverified:recipe_depth] {item_task.item.id} — no depth estimate available."
```

`ALLOWANCE` 是一个可配置的余量（默认 2），因为合成链中某些步骤可能是 trivial 的（smelting、simple crafting）。此规则的核心假设是：**quest 依赖链应该至少和物品合成链一样长**——每经过一个合成步骤，应该有一个对应的 quest 教玩家如何完成它。注意此 heuristic 在 expert 包中精度较低（合成链深度可达 15+，而 heuristic 最大覆盖约 depth 8），expert 包建议在 Step 2 提供关键物品的精确深度。

**违反了会怎样：** 玩家面对一个需要 5 步合成的物品，但 quest chain 只有 2 步深度——中间 3 步没有任何 quest 教过玩家怎么做。玩家被迫自行查阅 JEI/EMI，quest book 失去了教学引导的功能。

**来源：** micro-patterns MP24（Tier-Reachability Check）首次提出这个检测信号；cesspit.net 的 expert pack 分析指出"the recipes have many cross dependencies, so that you'll need to progress in 'x'"——合成链的交叉依赖是 expert pack 的核心 gating 机制，quest chain 必须覆盖它；Monifactory 的 voltage-tier 系统通过 `always_invisible` 章节做 gamestage 路由，确保每个合成步骤都有对应的 stage gate（micro-patterns MP23）。

---

### R4 — Pack-Type Stage Boundary

**数据依赖：** ⚠️ 需要用户在 Step 2 提供 `item_stage_map` 和 `stage_definition` 才能完整运行 | ✅ 无 L2 数据时可降级为跨 chapter 引用交叉检查（仅检查物品是否出现在更早 chapter 的 reward 中） | 无法判定的物品降级为 `[unverified:stage]`

**检查什么：** 根据包类型（kitchen-sink / expert / skyblock / RPG），每个 quest 应该处于正确的阶段区间。输入字段：quest 所在 chapter 的 `order_index`、chapter 的 `group`、以及阶段定义（用户在 Step 2 提供）。

**怎么检查：** 不同包类型有不同的阶段分界逻辑：

- **Kitchen-sink（ATM 型）**：阶段由 chapter group 定义（"Getting Started" → "Tech" → "Magic" → "Endgame"）。检查：capstone chapter 的任务物品不应出现在早期 chapter 的任务中。
- **Expert（GregTech/Monifactory 型）**：阶段由 voltage tier 或 GregTech age 定义。检查：高 voltage tier 物品不应出现在低 tier chapter 中。
- **Skyblock**：阶段由资源获取方式定义（sieve → crook → ore processing → automation）。检查：需要自动化的物品不应出现在手动阶段。
- **RPG/Adventure**：阶段由维度或 story arc 定义。检查：后期维度的物品不应出现在前期 chapter。

```
for each quest Q:
    quest_stage = determine_stage(Q.chapter, Q.chapter_group, pack_type)
    for each item_task in Q.tasks:
        item_stage = (L2_stage_map or {}).get(item_task.item.id)
        if item_stage is not None and item_stage > quest_stage:
            ERROR: "Quest {Q.name} is in stage {quest_stage} but requires
                      {item_task.item.id} from stage {item_stage}."
        elif item_stage is None:
            # Fallback: cross-chapter reference check (no external data needed)
            # Check if this item appears as a task in an earlier chapter —
            # if so, it's probably stage-appropriate; if only in later chapters, suspicious
            earlier_usage = any(
                item_task.item.id in [t.item.id for t in q.tasks]
                for ch in all_chapters if ch.order_index < Q.chapter.order_index
                for q in ch.quests
            )
            later_only = not earlier_usage and any(
                item_task.item.id in [t.item.id for t in q.tasks]
                for ch in all_chapters if ch.order_index > Q.chapter.order_index
                for q in ch.quests
            )
            if later_only:
                INFO: "[unverified:stage] {item_task.item.id} appears only in later chapters.
                       Possible stage boundary violation in {Q.name}."
```

`item_stage_map` 和 `stage_definition` 需要用户在 Step 2 提供，或从已有配置推断（对 `--adopt` 模式）。

**违反了会怎样：** 阶段系统失去意义——玩家在「石器时代」chapter 中需要「电力时代」的物品，整个 gating 设计崩塌。对 expert pack 来说这尤其致命，因为 expert pack 的核心体验就是「按阶段推进」。

**来源：** SevTech: Ages 的 age-based gating 系统（每个 age 是一个明确的阶段，高级物品在低 age 不可见/不可用）；E2E Extended README 描述的 "gated players must learn about the mod to make the most of it while waiting for the next mod to unlock"；Monifactory 的 voltage-tier gating（design guide §pack-type-patterns）。

---

## 2. Dependency Integrity（依赖完整性）

这类规则检查依赖图的结构性健康——是否有环、是否有孤立节点、依赖关系是否语义正确。

### R5 — Circular Dependency Detection

**检查什么：** quest 依赖图中是否存在循环（A depends_on B，B depends_on A，或更长的环）。输入字段：所有 quest 的 `dependencies` 数组。

**怎么检查：** 标准的有向图环检测算法（DFS + 三色标记）：

```
function detect_cycles(all_quests):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {quest.id: WHITE for quest in all_quests}
    cycles = []

    function dfs(quest_id, path):
        color[quest_id] = GRAY
        path.append(quest_id)
        for dep_id in get_dependencies(quest_id):
            if color[dep_id] == GRAY:
                # Found a cycle: extract it from path
                cycle_start = path.index(dep_id)
                cycles.append(path[cycle_start:])
            elif color[dep_id] == WHITE:
                dfs(dep_id, path)
        path.pop()
        color[quest_id] = BLACK

    for quest in all_quests:
        if color[quest.id] == WHITE:
            dfs(quest.id, [])

    return cycles
```

此规则还需要处理**跨章节引用**——当 `dependencies` 包含另一个 chapter 的 quest ID（或 raw hex ID）时，环检测必须跨越整个 book，不能只在单 chapter 内运行。

此外，需要区分**显式环**（在 `dependencies` 数组中直接可见）和**隐式环**（通过 recipe graph 产生的——quest A 要求 mod X 的物品，该物品的 recipe 需要 mod Y 的物品，而 mod Y 的 quest 又要求 mod X 的物品）。显式环由上述算法检测；隐式环需要 `recipe_dependency_graph` 数据，标记为 warning 而非 error。

**违反了会怎样：** 玩家面对一个 Catch-22——需要 A 才能得到 B，需要 B 才能得到 A。在 `default` progression 模式下两个 quest 都永远不解锁；在 `flexible` 模式下两个 quest 都可见但都无法完成。这是 FTB Evolution issue #6447 中记录的最严重的进度问题之一。

**来源：** AP2（Circular Dependency Deadlock）；FTB Evolution issue #6447 的 "red chalk → torch flower seeds → heart of the sea → red chalk" 案例；validator 已有 `E_DEP_CYCLE` 诊断码。

---

### R6 — Unreachable Quest Detection

**检查什么：** 是否存在永远无法解锁的 quest——所有路径都被 optional/secret 前置阻挡，或前置条件在当前包配置中不可满足。输入字段：所有 quest 的 `dependencies`、`optional`、`secret`、`always_invisible` 标志、以及 `dependency_requirement`。

**怎么检查：**

```
for each quest Q:
    if Q has no dependencies:
        Q is reachable (root quest)
        continue

    all_paths = find_all_dependency_paths(Q)  # all paths from any root to Q
    if all_paths is empty:
        ERROR: "Quest {Q.name} has no path from any root — unreachable."
        continue

    for each path in all_paths:
        path_feasible = True
        for each quest P in path:
            if P.optional and no non-optional path bypasses P:
                path_feasible = False  # blocked by optional gate
            if P.secret and no discovery_trigger exists:
                path_feasible = False  # blocked by undiscoverable secret
        if path_feasible:
            break  # at least one feasible path exists

    if not any(path_feasible for path in all_paths):
        ERROR: "Quest {Q.name} is unreachable — all paths blocked by
                optional/secret gates without bypass."
```

特殊处理：如果一个 mandatory quest 的唯一前置是一个 `optional: true` 的 quest，这是一个 error。如果前置是 `secret: true` 且没有可触发的发现条件（biome visit、item pickup、boss kill），这也是 error。

**违反了会怎样：** 玩家完成所有可见 quest 后发现 chapter 完成度永远不到 100%（AP3 Unfinishable Chapter），或者某个 mandatory quest 永远不解锁（AP4 Wrong Gating 的极端形式）。

**来源：** AP3（Unfinishable Chapter）；FTB Evolution issue #6447 中"It isn't possible to complete the 'Getting Started' chapter"；PP4（Completionist's Dilemma）。

---

### R7 — Optional-Gate-Mandatory Check

**检查什么：** mandatory（non-optional）quest 是否依赖于 optional quest。输入字段：quest 的 `optional` 标志、quest 的 `dependencies`、以及被依赖 quest 的 `optional` 标志。

**怎么检查：**

```
for each quest Q:
    if Q.optional:
        continue  # optional depending on optional is fine
    for each dep_id in Q.dependencies:
        dep_quest = get_quest(dep_id)
        if dep_quest.optional:
            # Check if there's an alternative path
            if Q.dependency_requirement == "all":
                ERROR: "Mandatory quest {Q.name} depends on optional quest
                        {dep_quest.name} with requirement 'all'."
            elif Q.dependency_requirement in ("one_completed", "one_started"):
                # Check if at least one non-optional dep exists
                non_optional_deps = [d for d in Q.dependencies
                                     if not get_quest(d).optional]
                if not non_optional_deps:
                    ERROR: "Mandatory quest {Q.name} has only optional
                            dependencies even with 'one_completed'."
```

**违反了会怎样：** 跳过 optional 内容的玩家发现 mandatory 进度被卡住——他们必须回去做之前选择跳过的内容。这在 kitchen-sink 包中尤其令人沮丧，因为 flexible 模式的哲学是「做你想做的」。

**来源：** AP4（Wrong Gating）；FTB Evolution issue #6447 中"The mandatory boss catcher quest is gated behind the optional Hephaestus Forge: Tier 4 quest"。

---

### R8 — Dependency Requirement Consistency

**检查什么：** `dependency_requirement` 字段的值是否与依赖结构的语义匹配。输入字段：quest 的 `dependency_requirement`（"all" / "one_completed" / "one_started"）、`dependencies` 数组的结构。

**怎么检查：**

```
for each quest Q:
    deps = Q.dependencies
    if len(deps) <= 1:
        continue  # single dep, requirement doesn't matter

    # Check: if deps are parallel alternatives, "all" is probably wrong
    dep_depths = [dependency_depth(d) for d in deps]
    if max(dep_depths) - min(dep_depths) <= 1:
        # Deps are at similar depth = likely parallel alternatives
        # Check if deps share a common parent (fan-out siblings)
        common_parent = find_common_ancestor(deps)
        if common_parent is not None:
            if Q.dependency_requirement == "all":
                INFO: "Quest {Q.name} requires ALL of {len(deps)} sibling
                       quests. If these are alternatives, consider
                       'one_completed'."

    # Check: if "one_completed" but only one dep exists
    if Q.dependency_requirement in ("one_completed", "one_started") and len(deps) == 1:
        WARNING: "Quest {Q.name} uses 'one_completed' with a single
                  dependency — redundant, 'all' is equivalent."
```

**违反了会怎样：** AP4 的温和版本——玩家被要求完成所有并行选项而不是选择一个，增加了不必要的 grind，但不至于完全卡住。

**来源：** AP4（Wrong Gating）；FTB Evolution issue #6447 中"The early energy generation quest requires all three generators, rather than just one"；micro-patterns MP9（Diamond / pick-and-rejoin）的 `dependency_requirement: "one_completed"` 设计。

---

### R9 — Dependency Depth Reasonableness

**检查什么：** quest chain 的深度是否在包类型的合理范围内。输入字段：chapter 内所有 quest 的 `dependency_depth`、pack_type。

**怎么检查：**

```
MAX_DEPTH = {
    "kitchen-sink": 8,     # ATM-10 typical: 3-5, max observed: 6
    "expert": 20,          # Monifactory typical: 8-15, ATM9-Sky: 18
    "skyblock": 20,        # ATM9-Sky: 18
    "rpg": 12,             # Prominence II typical: 5-8
    "create-focused": 10,  # Create packs typical: 3-6
}

for each chapter C:
    max_depth = max(dependency_depth(q) for q in C.quests)
    if max_depth > MAX_DEPTH[pack_type]:
        WARNING: "Chapter {C.name} has depth {max_depth}, exceeding
                  {pack_type} guideline of {MAX_DEPTH[pack_type]}.
                  Consider splitting into sub-chapters."
```

**违反了会怎样：** 过深的 chain 意味着玩家在一条线上被强制走太远，缺乏选择和喘息的空间。在 expert pack 中这可以接受（深度是设计意图），但在 kitchen-sink 中这是设计失误。

**来源：** Cross-pack comparison table（micro-patterns）——kitchen-sink depth 3-5，expert depth 8-18，skyblock tutorial depth 18；design guide §field-findings。

---

## 3. Reward Continuity（奖励连贯性）

这类规则检查 reward 是否有效地引导玩家走向下一步——reward 是 quest book 的「拉力」，断链意味着玩家完成 quest 后不知道接下来做什么。

### R10 — Reward-to-Dependent Bridge

**检查什么：** quest 的 reward 是否出现在其直接后继 quest（依赖它的 quest）的 task 中。输入字段：quest 的 `rewards`（item 类型）、所有以该 quest 为 dependency 的后继 quest 的 `tasks`。

**怎么检查：**

```
for each quest Q:
    dependents = find_dependents(Q)  # quests that list Q in their dependencies
    if not dependents:
        continue  # terminal quest (capstone or leaf) — no bridge needed

    item_rewards = [r for r in Q.rewards if r.type in ("ftbquests:item", "item")]
    if not item_rewards:
        continue  # XP-only or cosmetic reward — skip

    for reward in item_rewards:
        reward_id = reward.item.id
        reward_count = reward.count

        found_in_dependent = False
        for dep_quest in dependents:
            for task in dep_quest.tasks:
                if task.type in ("ftbquests:item", "item"):
                    if task.item.id == reward_id:
                        found_in_dependent = True
                        break

        if not found_in_dependent:
            # Check if it's a known "universal" reward type
            if is_tool_reward(reward_id) or is_currency_reward(reward_id):
                continue  # tools and currencies are universal bridges
            if is_xp_reward(reward) or is_loot_reward(reward):
                continue  # XP and loot don't need item-level bridging

            INFO: "Quest {Q.name} rewards {reward_id} x{reward_count},
                   but no dependent quest requires it as a task.
                   Consider a material bridge (MP14) or tool reward (MP15)."
```

此规则的容忍度设计很重要：terminal quest（capstone、leaf）不需要 bridge；XP/loot/choice reward 不需要 item-level bridge；tool reward 和 currency reward 是 universal bridge。规则只在 reward 是一个「看起来应该有用但实际没有后继任务需要它」的物品时触发。

**违反了会怎样：** AP6（Dead-End Reward）——玩家完成 quest 后获得一个物品，但不知道该用它做什么。inventory 中堆积了大量「dead-end」物品，quest book 丧失了引导力。

**来源：** AP6（Reward That Doesn't Bridge）；micro-patterns MP14（Material Bridge）、MP15（Tool Reward）；FTB Evolution issue #6447 中 "rewards the immersive engineering hammer, rather than the Oritech wrench"——reward 给了错误的工具。

> **规则优先级 (Cycle 7):** **R10 > R12**。Material bridge 是功能性需求（reward 必须引导玩家到下一步），reward value progression 是美学需求（reward 价值应递增）。当两者冲突时（例如 depth-2 quest 奖励高价值 bridge material 而 depth-3 quest 奖励低价值 XP），R10 的 bridge 完整性优先于 R12 的价值递增。R12 的 WARNING 应添加 material bridge 例外：如果 reward 满足 R10 bridge 条件，即使价值递减也不触发 R12。

---

### R11 — Reward-Target Accuracy (Wrong Tool Detection)

**检查什么：** 当 quest 奖励一个工具（wrench、hammer、guide book）时，该工具是否是后继 quest 实际需要的工具。输入字段：quest 的 `rewards`（item 类型的工具类物品）、后继 quest 的 description 和 task 中引用的工具。

**怎么检查：** 此规则需要一个 `tool_category_map`——将同一功能的工具按 mod 分组（例如所有 wrench：`immersiveengineering:hammer`、`oritech:wrench`、`mekanism:configurator`、`create:wrench`）。然后：

```
for each quest Q:
    for each reward in Q.rewards:
        if reward.item.id in tool_category_map:
            tool_category = tool_category_map[reward.item.id]
            dependents = find_dependents(Q)
            for dep_quest in dependents:
                # Check if dependent quest needs a tool from the same category
                needed_tool = extract_tool_from_description(dep_quest.description)
                if needed_tool and needed_tool in tool_category:
                    if needed_tool != reward.item.id:
                        WARNING: "Quest {Q.name} rewards {reward.item.id}
                                  ({tool_category} type), but dependent quest
                                  {dep_quest.name} needs {needed_tool}
                                  (same category, different mod)."
```

这是 R10 的特化版本，专门处理「wrench 给错了 mod」这种 multi-mod pack 中极常见的问题。

**违反了会怎样：** PP6（Wrong Tool Reward）——玩家获得一个看似有用的工具，但它是错的。在 multi-mod kitchen-sink 中，5 个 mod 各有自己的 wrench，给错一个等于没给。

**来源：** PP6（Wrong Tool Reward）；FTB Evolution issue #6447 中 "Making Multiblocks with Machine Cores rewards the immersive engineering hammer, rather than the Oritech wrench (which is a task under 'Basic Logistics')"。

---

### R12 — Reward Value Progression

**检查什么：** reward 的价值是否随 quest 难度递增，而非随机或递减。输入字段：quest 的 `dependency_depth`、quest 所在 chapter 的 `order_index`、`rewards` 中物品的估算价值。

**怎么检查：** 为每个 reward 估算一个「价值分」（value score）。简单模型：物品 rarity × count。复杂模型：从 mod 的 tier 数据推断。然后检查价值是否随进度递增：

```
for each chapter C:
    quest_rewards = []
    for each quest Q in C.quests (sorted by dependency_depth):
        total_value = sum(estimate_value(r) for r in Q.rewards)
        quest_rewards.append((Q.dependency_depth, total_value))

    # Check: later quests should generally have higher-value rewards
    for i in range(1, len(quest_rewards)):
        prev_depth, prev_value = quest_rewards[i-1]
        curr_depth, curr_value = quest_rewards[i]
        if curr_depth > prev_depth and curr_value < prev_value * 0.5:
            INFO: "Quest at depth {curr_depth} has significantly lower reward
                   value ({curr_value}) than quest at depth {prev_depth}
                   ({prev_value}). Reward may feel underwhelming."
```

这是一个 soft check（INFO level），因为 reward 价值估算本身不精确，且某些 quest 故意给 low reward（tutorial 阶段的「acknowledgement」quest）。

**违反了会怎样：** AP8（Reward Inflation）的逆向版本——玩家在高难度 quest 中获得比低难度 quest 更差的 reward，动力丧失。或者更常见的情况是，early game 给了太多高价值 reward（inflation），导致 mid-game 的 reward 显得寒酸。

**来源：** AP8（Reward Inflation）；cesspit.net 描述的 reward pacing 原则——"you have to work hard to get to a milestone"之后 reward 应该匹配 effort；ATM-10 的 XP drip 设计（10/50/100 XP tiers，随深度递增，micro-patterns MP16）。

> **规则优先级 (Cycle 7):** **R10 > R12**（交叉引用）。当 reward 满足 R10 的 material bridge 条件时（reward item 出现在 dependent quest 的 task 中），即使其价值高于后续 reward，也不应触发 R12 的 WARNING。R12 仅对 non-bridge reward（XP、currency、cosmetic item）执行价值递增检查。Material bridge 是功能性的，value progression 是美学性的。

---

### R13 — Capstone Reward Magnitude

**检查什么：** capstone quest（fan-in convergence 节点，dependencies ≥ 5）的 reward 是否匹配其地位。输入字段：quest 的 `dependencies`（count ≥ 5 视为 capstone）、`rewards` 的价值总和、同 chapter 其他 quest 的平均 reward 价值。

**怎么检查：**

```
for each quest Q:
    if len(Q.dependencies) >= 5:  # capstone heuristic
        capstone_value = sum(estimate_value(r) for r in Q.rewards)
        chapter_avg = average(sum(estimate_value(r) for r in q.rewards)
                             for q in Q.chapter.quests if q != Q)
        if capstone_value < chapter_avg * 3:
            WARNING: "Capstone quest {Q.name} ({len(Q.dependencies)} deps)
                      has reward value {capstone_value}, less than 3x the
                      chapter average ({chapter_avg}). Consider a more
                      impactful reward."
```

**违反了会怎样：** 玩家完成了整章最难、耗时最长的 quest，获得的 reward 和普通 quest 差不多。capstone 是 chapter 的高潮时刻，reward 应该 memorable。

**来源：** ATM-10 ATM Star capstone reward = 50 ATM Star Shards + Patrick Star + 50 XP levels（micro-patterns MP8）；design guide §principles P4 描述的「generosity is density」哲学。**验证（Phase 3 Cycle 3）：** Craftoria #289 发现 xp_levels reward 在非 milestone quest 上导致价值随玩家等级漂移——这是 R12 的变体，R31 将其编码为专项检查。

---

## 4. Teaching Order（教学顺序）

这类规则检查 quest chain 内的教学顺序是否合理——先教后做、先简单后复杂、先理论后实践。

### R14 — Teach-Then-Do Ordering

**检查什么：** 教学 quest（checkmark/stat/observation task + 长 description）是否出现在应用 quest（item task 需要用到教学内容）之前。输入字段：quest 的 `tasks` 类型、`description` 长度、quest 的 `dependency_depth`。

**怎么检查：** 首先识别 chapter 内的「教学 quest」和「应用 quest」：

```
teaching_quests = [q for q in chapter.quests
                   if any(t.type in ("ftbquests:checkmark", "checkmark",
                                     "ftbquests:stat", "stat",
                                     "ftbquests:observation", "observation")
                          for t in q.tasks)
                   and len(q.description) > TEACHING_DESC_THRESHOLD]

doing_quests = [q for q in chapter.quests
                if any(t.type in ("ftbquests:item", "item") for t in q.tasks)]

# For each doing quest, check if there's a related teaching quest
for doing_quest in doing_quests:
    related_teaching = find_related_teaching(doing_quest, teaching_quests)
    # "Related" = same mod namespace, or teaching quest mentions the item
    if related_teaching:
        if dependency_depth(related_teaching) > dependency_depth(doing_quest):
            ERROR: "Teaching quest {related_teaching.name} (depth {depth})
                    appears AFTER doing quest {doing_quest.name} (depth {depth}).
                    The player encounters 'do this' before 'here's how'."
```

「Related」的判定：教学 quest 和对应应用 quest 通常 (1) 属于同一个 mod namespace，(2) 教学 quest 的 description 中提到了应用 quest 的 task item，或 (3) 它们在依赖链中相邻（教学 quest 是应用 quest 的直接或间接祖先——这是正确顺序；反过来则是倒置）。

**违反了会怎样：** MP25（Dependency-Order Check / Sequence Inversion）——玩家先遇到「合成这个物品」的任务，然后才看到「这是如何合成」的教学。教学失去了意义，因为玩家在阅读时已经知道了要做什么（或者已经被卡住过）。

**来源：** MP25（Dependency-Order Check）；MP11（Teach-Then-Do Sequencing）描述了正确模式——Create: Delight 的 Feast_Afoot chapter 用 checkmark/stat 教学 quest 先行，item task 实践 quest 跟进；ATM-10 Mekanism chapter 的 "introduction (checkmark) → first craft (item) → first use (observation) → advanced recipe (item)" 序列。

---

### R15 — Complexity Escalation Within Chapter

**检查什么：** chapter 内的 quest 是否按复杂度递增排列——简单物品先于复杂物品、低 count 先于高 count、基础机器先于 multiblock。输入字段：chapter 内 quest 的排列顺序（由 `dependency_depth` 和 `order_index` 决定）、task 的 `item.id` 和 `count`、外部 `item_complexity` 映射。

**怎么检查：**

```
for each chapter C:
    quests_ordered = sort(C.quests, by=[dependency_depth, order_index])
    prev_complexity = 0
    for quest in quests_ordered:
        for task in quest.tasks:
            if task.type in ("ftbquests:item", "item"):
                complexity = estimate_complexity(task)
                # Complexity = recipe_depth * log(count + 1)
                if complexity < prev_complexity * 0.3:
                    # Significant complexity drop — possible inversion
                    INFO: "Quest {quest.name} has complexity {complexity},
                           significantly lower than previous ({prev_complexity}).
                           Check if ordering is intentional."
                prev_complexity = max(prev_complexity, complexity)
```

`estimate_complexity` 综合考虑 (1) recipe depth（合成步骤数），(2) item count（64 个铁锭比 1 个铁锭复杂），(3) 物品 tier（netherite 比 iron 复杂）。此规则是 heuristic——复杂度下降可能是有意的（bottleneck 之后的 recovery quest），所以只报 INFO。

**违反了会怎样：** 玩家在 chapter 中途遇到一个突然变简单的 quest，感觉节奏被打断。更严重的是反向情况：chapter 开头就要求一个高复杂度物品，吓退新玩家。

**来源：** MP12（Tier Escalation Within a Chapter）——ATM-10 AllTheModium 章节从 AllTheModium（Overworld）→ Vibranium（Nether）→ Unobtainium（End）的复杂度递增；difficulty-curve.md 的 phase breakdown。

---

### R16 — Dimension-Explore-Then-Craft Ordering

**检查什么：** 需要先到达某个维度的 quest，其 dimension task 是否在 item task 之前。输入字段：quest 的 `tasks`（是否同时包含 dimension 和 item task），或者 quest chain 中 dimension quest 和 item quest 的顺序。

**怎么检查：** 两种检查模式：

模式 A（同一 quest 内）——一个 quest 同时有 dimension task 和 item task 时，这是合理的（MP5 Composite）。但如果 quest 只有 item task 且该物品只存在于某个维度，而 dimension task 在另一个 quest 中：

```
for each quest Q:
    for each item_task in Q.tasks:
        item_dim = item_dimension_map.get(item_task.item.id)
        if item_dim and item_dim != "minecraft:overworld":
            # Check if any ancestor quest has a dimension task for item_dim
            has_dim_ancestor = any(
                any(t.type in ("ftbquests:dimension", "dimension")
                    and getattr(t, 'dimension', None) == item_dim
                    for t in ancestor.tasks)
                for ancestor in get_all_ancestors(Q)
            )
            if not has_dim_ancestor:
                WARNING: "Quest {Q.name} requires {item_task.item.id} from
                          {item_dim}, but no ancestor has a dimension task
                          for {item_dim}. Consider adding one (MP13)."
```

模式 B（quest chain 顺序）——dimension quest 应该在 item quest 之前：

```
for each quest Q:
    if Q has a dimension task for dimension D:
        for each dependent_quest in find_dependents(Q):
            if dependent_quest has an item task requiring items from D:
                pass  # Correct order: dimension first, then item
    # Reverse: item quest at lower depth than dimension quest
    for each item_quest in chapter.quests:
        for each task in item_quest.tasks:
            task_dim = item_dimension_map.get(task.item.id)
            if task_dim:
                dim_quests = [q for q in chapter.quests
                             if has_dimension_task(q, task_dim)]
                if dim_quests and min(depth(dq) for dq in dim_quests) > depth(item_quest):
                    WARNING: "Item quest {item_quest.name} (depth {depth})
                              precedes dimension quest for {task_dim}
                              (depth {min_depth}). Consider MP13 ordering."
```

**违反了会怎样：** MP13（Explore-Then-Craft）的反面——玩家被要求合成一个来自 Nether 的物品，但 quest chain 中没有先去 Nether 的步骤。玩家可能不知道要去 Nether，或者不知道物品在 Nether 中获取。

**来源：** MP13（Explore-Then-Craft / Dimension-Gated Pacing）——"travel → gather → craft" 的正确顺序；MP5（Dimension + Item Composite）；MP21（Dimension-as-Stage-Gate）。

---

### R17 — Tool-Reward-Before-Use Ordering

**检查什么：** 当 quest A 奖励一个工具，quest B 需要使用该工具时，B 是否 depends_on A。输入字段：quest A 的 `rewards`（工具类物品）、quest B 的 `tasks`（需要该工具的物品）、以及 B 的 `dependencies`。

**怎么检查：**

```
for each quest A:
    tool_rewards = [r for r in A.rewards
                    if r.type in ("ftbquests:item", "item")
                    and is_tool(r.item.id)]
    for tool_reward in tool_rewards:
        # Find quests that need this tool
        for quest B in all_quests:
            if B == A:
                continue
            needs_tool = any(
                task.item.id == tool_reward.item.id
                for task in B.tasks
                if task.type in ("ftbquests:item", "item")
            ) or tool_reward.item.id in extract_tools_from_description(B.description)

            if needs_tool:
                if A.id not in get_all_ancestors(B):
                    WARNING: "Quest {A.name} rewards tool {tool_reward.item.id},
                              and quest {B.name} needs it, but {B.name} does not
                              depend on {A.name}."
```

**违反了会怎样：** 玩家在需要某个工具的 quest 处卡住，不知道该去哪里获取这个工具。工具 reward 和工具需求之间的断链比材料断链更严重——材料可以通过 mining/crafting 获取，但工具通常需要特定的 quest reward 或 quest chain。

**来源：** MP15（Tool Reward）；FTB Evolution issue #6447 中"the Oritech wrench is a task under 'Basic Logistics'"但 reward 给了错误的工具（AP6/PP6）；Create: Delight Feast_Afoot 中 tutorial quest reward hygrometer → 下一个 quest 使用 hygrometer 的正确顺序。

---

## 5. Pacing（进度节奏）

这类规则检查 quest book 的整体节奏——reward 通胀/通缩、bottleneck 密度、描述覆盖率。

### R18 — Description Coverage

**检查什么：** 非 catalog/recipe-cell 类型的 quest 是否都有 description。输入字段：quest 的 `description`（或 lang 文件中对应的 `quest.<HEX>.quest_desc`）、quest 的 shape 和 chapter 类型。

**怎么检查：**

```
for each quest Q:
    has_desc = bool(Q.description) or lang_has_key(f"quest.{Q.id}.quest_desc")
    is_catalog_cell = (Q.shape in ("rsquare", "circle")
                       and Q.size <= 2.0
                       and is_catalog_chapter(Q.chapter)
                       and len(Q.tasks) == 1)

    if not has_desc and not is_catalog_cell:
        WARNING: "Quest {Q.name} has no description. Unless this is a
                  catalog cell, add at least a one-sentence context
                  (HOW + WHY)."
```

Catalog chapter 的 recipe cell 允许无 description（Create: Delight 的 Mouse_Chef 304 个 cell 大多无 description，这是设计选择）。但非 catalog 的 quest 必须有 description——这是 AP5（Empty Quest Description / Silent Node）的自动检测。

**违反了会怎样：** AP5——quest book 变成一个无意义的 checklist，玩家看到「obtain osmium ingot」但不知道为什么需要它、怎么获得它。对新玩家尤其致命。

**来源：** AP5（Empty Quest Description）；PP5（Context Void）；FTB Evolution issue #6447 中 "None of the quests have text (new players might not know why they'd want so much diversity)"；cesspit.net 的 "this HUGE questbook, with more than 2000 quests, was at the same time a great guide to erase the problem of guessing"——有 description 的 quest book 和没有 description 的 quest book 体验天差地别。**验证（Phase 3 Cycle 3）：** Monifactory CONTRIBUTING.md 明确要求所有 quest 有 substantive description，R32 将此标准编码为 chapter-level 覆盖率检查。

---

### R19 — Bottleneck Spacing

**检查什么：** 高难度 quest（bottleneck）之间是否有足够的「喘息空间」。输入字段：quest 的 task 复杂度估算、quest chain 顺序。

**怎么检查：** 定义 bottleneck 为 task count ≥ 3 或 item count ≥ 64 或 recipe depth ≥ 5 的 quest。检查连续 bottleneck 之间是否有至少 2 个普通 quest：

```
for each chapter C:
    quests_ordered = sort(C.quests, by=[dependency_depth, x, y])
    bottleneck_streak = 0
    for quest in quests_ordered:
        if is_bottleneck(quest):
            bottleneck_streak += 1
            if bottleneck_streak >= 3:
                WARNING: "Chapter {C.name} has {bottleneck_streak} consecutive
                          bottleneck quests ending at {quest.name}. Players need
                          recovery quests between hard challenges."
        else:
            bottleneck_streak = 0
```

**违反了会怎样：** 玩家连续面对高难度挑战，没有喘息的空间。difficulty-curve.md 描述的 ideal curve 不是直线上升——它有锯齿形的「challenge → recovery → challenge」节奏。

**来源：** difficulty-curve.md 的 "Bottleneck Task Design" 部分——"Always provide alternative paths or hints in description"；cesspit.net 的 backward shortcut 模式——milestone 之后应该给玩家一个优化之前内容的机会，而不是立刻面对下一个 bottleneck。**验证（Phase 3 Cycle 3）：** Craftoria #231 记录了 Powah chapter「throws everything at you」with 3 tiers of reactors and no rewards between them——这是 R19 的经典 reward desert 案例，R32 将其纳入 QA 覆盖检查。

---

### R20 — Chapter Completion Testability

**检查什么：** 每个 chapter 的所有 non-optional quest 是否可以通过一条明确的路径全部完成。输入字段：chapter 内所有 quest 的 `optional`、`secret`、`always_invisible` 标志、以及依赖图。

**怎么检查：**

```
for each chapter C:
    required_quests = [q for q in C.quests
                       if not q.optional and not q.always_invisible]

    # Check: can all required quests be completed?
    # A quest is completable if all its deps are in required_quests or already completable
    completable = set()
    changed = True
    while changed:
        changed = False
        for q in required_quests:
            if q.id in completable:
                continue
            deps = q.dependencies
            if not deps or all(d in completable for d in deps):
                completable.add(q.id)
                changed = True

    incomplete = [q for q in required_quests if q.id not in completable]
    if incomplete:
        ERROR: "Chapter {C.name} has {len(incomplete)} non-optional quests
                that cannot be completed: {[q.name for q in incomplete]}.
                Their dependencies reference quests outside the completable set."
```

这是 R6（Unreachable Quest）的 chapter-level 版本，专门检测 AP3（Unfinishable Chapter）。特殊规则：starter chapter（`order_index == 0`）的此检查升级为 error + 优先修复——这是玩家看到的第一个 chapter，必须 100% 可完成。

**违反了会怎样：** PP4（Completionist's Dilemma）——玩家完成所有可见 quest 后 chapter 完成度不到 100%。FTB Evolution 的 starter chapter 就有这个问题，给玩家的第一印象极差。

**来源：** AP3（Unfinishable Chapter）；PP4（Completionist's Dilemma）；FTB Evolution issue #6447 中 "It isn't possible to complete the 'Getting Started' chapter, even if you complete every quest"。

---

### R21 — Hidden Quest Signpost

**检查什么：** 每个使用 `hide_until_deps_visible: true` 的 quest 是否有可见的 signpost 引导玩家发现它。输入字段：quest 的 `hide_until_deps_visible`、其 `dependencies` 中 quest 的可见性。

**怎么检查：**

```
for each quest Q:
    if not Q.hide_until_deps_visible:
        continue

    # Check: is at least one dependency visible and descriptive?
    has_visible_signpost = False
    for dep_id in Q.dependencies:
        dep = get_quest(dep_id)
        if not dep.hide_until_deps_visible and not dep.secret:
            # Visible dependency — when player completes it, Q appears
            if dep.description and mentions_unlock(dep.description):
                has_visible_signpost = True
                break

    # Check: is there a nearby visible quest that hints at Q?
    if not has_visible_signpost:
        nearby_visible = [q for q in Q.chapter.quests
                         if not q.hide_until_deps_visible
                         and distance(q, Q) < 3.0
                         and q.description]
        if nearby_visible:
            has_visible_signpost = True

    if not has_visible_signpost:
        WARNING: "Quest {Q.name} uses hide_until_deps_visible but has no
                  visible signpost. Players may never discover it.
                  Add a visible dependency with a hint, or a nearby
                  signpost quest."
```

`mentions_unlock` 检查 description 中是否有类似「unlocks」「opens」「reveals」的措辞——提示玩家完成这个 quest 会解锁新内容。

**违反了会怎样：** AP7（Hidden Quest Trap）——整条 quest branch 永远不被玩家发现。在 narrative pack 中可能 softlock 剧情理解；在 expert pack 中可能隐藏关键 tutorial。

**来源：** AP7（Hidden Quest Trap）；PP3（Invisible Wall）；FTB Evolution issue #6447 中 "There's a permanently hidden quest"；Phase 1 数据——Create: Delight 使用 `hide_until_deps_visible` 72 次（配合 visible hub 做 signpost），Mechanomania 0 次，ATM-10 ~3%。

---

### R22 — Cross-Chapter Dependency Validity

**检查什么：** 跨 chapter 的 dependency 引用是否指向存在的 quest。输入字段：quest 的 `dependencies` 中引用的跨 chapter quest ID 或 name。

**怎么检查：**

```
for each quest Q:
    for dep_ref in Q.dependencies:
        if is_cross_chapter_ref(dep_ref):
            target = resolve_ref(dep_ref)
            if target is None:
                ERROR: "Quest {Q.name} depends on {dep_ref} which does not
                        exist in any chapter."
            elif target.chapter.order_index > Q.chapter.order_index:
                WARNING: "Quest {Q.name} (chapter {Q.chapter.order_index})
                          depends on {target.name} (chapter {target.chapter.order_index})
                          which is in a LATER chapter. This creates a
                          backward dependency."
```

向后依赖（引用后面 chapter 的 quest）通常意味着设计错误——前面的 chapter 要求后面 chapter 的内容才能完成，这与 chapter ordering 的语义矛盾。

**违反了会怎样：** 玩家在前面的 chapter 中看到一个被锁住的 quest，它的 dependency 指向一个还没看到的 chapter。在 `default` 模式下这个 quest 永远不解锁（因为后面的 chapter 还没解锁）；在 `flexible` 模式下它显示为一个灰色节点，让玩家困惑。

**来源：** validator 已有 `E_DEP_MISSING` 诊断码；SKILL.md 的 "Task linkage" 部分描述了跨 chapter 引用的正确方式。

---

## 6. Description Consistency（描述一致性）

### R23 — Description-Item Consistency Check

**数据依赖：** ✅ 可独立运行（仅依赖 quest 文本和 `items.json5`，无需 JEI/EMI）

**检查什么：** quest 的 `description` 文本中提到的物品 ID 是否与同一 quest 的 `tasks` 和 `rewards` 中实际使用的物品 ID 一致。这是 AP1（Description-Reality Mismatch）的部分静态覆盖——无法验证描述中的合成指南是否正确（需要 JEI 数据），但可以捕获最简单的不匹配：描述说 "Shadowflame Goo" 但任务要求 "Shadowpulse Goo"。

**怎么检查：**

```
import re

# Match patterns like "modid:item_name" or "&emodid:item_name&r" in description text
ITEM_ID_PATTERN = re.compile(r'(?:&e)?([a-z0-9_.-]+:[a-z0-9_./-]+)(?:&r)?')

for each quest Q:
    # Extract item IDs mentioned in description
    desc_text = " ".join(Q.description) if Q.description else ""
    mentioned_ids = set(ITEM_ID_PATTERN.findall(desc_text))

    # Collect item IDs from tasks and rewards
    task_ids = set()
    for task in Q.tasks:
        if task.type in ("ftbquests:item", "item") and hasattr(task, 'item'):
            task_ids.add(task.item.id)
    reward_ids = set()
    for reward in Q.rewards:
        if reward.type in ("ftbquests:item", "item") and hasattr(reward, 'item'):
            reward_ids.add(reward.item.id)

    all_config_ids = task_ids | reward_ids

    # Check 1: description mentions an item ID that's not in tasks/rewards
    orphan_mentions = mentioned_ids - all_config_ids
    for mid in orphan_mentions:
        if mid in items_json5_all_ids:
            # Valid item ID but not in this quest's config — possible mismatch
            WARNING: "Quest {Q.name} description mentions '{mid}' but it doesn't
                      appear in tasks or rewards. Check if description is accurate."
        else:
            # Item ID doesn't exist at all — likely hallucination or typo
            ERROR: "Quest {Q.name} description references '{mid}' which is not
                    a valid item ID. Possible hallucination or typo."

    # Check 2: task/reward uses an item not mentioned in description
    # (only flag if description exists and is substantive — skip for catalog cells)
    if desc_text and len(desc_text) > 20:
        unmentioned = all_config_ids - mentioned_ids
        # Only flag if >50% of task items are unmentioned (some are fine as icons)
        if len(unmentioned) > len(all_config_ids) * 0.5:
            INFO: "Quest {Q.name} has {len(unmentioned)} task/reward items not
                   mentioned in description. Consider explaining their role."
```

此规则有三层检查精度：(1) 捕获描述中引用了不存在的物品 ID（ERROR — 可能是 AI 幻觉或拼写错误）；(2) 捕获描述中提到了一个有效物品但该物品不在当前 quest 的 tasks/rewards 中（WARNING — 描述可能写错了物品名）；(3) 提示 quest 的 task 物品大多没在描述中提及（INFO — 描述可能不够完整）。

这无法捕获 AP1 的所有形态——描述说"在熔炉中烧炼"但实际需要高炉，或者描述给出了错误的合成配方——这些需要 JEI/EMI 运行时验证。但它能捕获 AI 生成中最常见的错误：编造不存在的物品 ID 或在描述中引用错误的物品名称。

**违反了会怎样：** AP1（Description-Reality Mismatch）——玩家按照描述中的物品名去搜索，发现找不到该物品，或者提交后发现任务要求的其实是另一个物品。quest book 作为引导系统的可信度崩塌。

**来源：** AP1（Description-Reality Mismatch）；AP9（Hallucination Cascade）；B3（AP1 无对应规则）审查建议；FTB Evolution issue #6447 中 "The Ore of the Eclipse Quest talks about Shadowflame Goo, but asks for Shadowpulse Goo"。

---

## 7. Suggestion & Necessity（建议可达性与任务必要性）

这类规则检查 description 作为「引导文本」时的独有问题——当描述建议、推荐或暗示玩家使用某些物品时，这些物品是否同样可达；任务要求是否过度严格（存在替代路径但被忽略）；以及 quest 文本是否跟随 mod 版本更新。

### R24 — Suggestion-Reachability Check

**数据依赖：** ⚠️ 需要 L1 维度映射 + L2 用户映射才能完整运行 | ✅ 可降级为仅检查 description 中提到的物品 ID 是否存在于祖先 quest 的 reward 或 task 中 | 无法判定的物品降级为 `[unverified:suggestion]`

**检查什么：** 当 quest 的 `description` 使用「建议使用」「推荐使用」「你可以用」「try using」「suggested gear」等引导性措辞提到一个物品时，该物品是否在 quest 的祖先链中已经可获得。这和 R1（Dimension-Reachability）不同——R1 检查的是 task 要求的物品，R24 检查的是 description 文本中**建议**的物品。玩家阅读描述后如果按建议行动却发现物品不可获得，信任受损程度不亚于 task 本身不可达。

**怎么检查：**

```
SUGGESTION_PATTERNS = [
    r'suggest(?:ed|ion)?\s+(?:to\s+)?use',
    r'recommend(?:ed)?\s+(?:to\s+)?use',
    r'you\s+(?:can|could|may)\s+use',
    r'try\s+using',
    r'best\s+(?:tool|weapon|gear|armor)\s+(?:for|is)',
    r'建议使用', r'推荐使用', r'可以用', r'最好使用',
]

for each quest Q:
    if not Q.description:
        continue
    desc_text = " ".join(Q.description)

    # Extract suggested item IDs
    mentioned_ids = set(ITEM_ID_PATTERN.findall(desc_text))  # reuse R23 pattern
    suggested_ids = set()
    for pattern in SUGGESTION_PATTERNS:
        for match in re.finditer(pattern, desc_text, re.IGNORECASE):
            # Look for item IDs in surrounding context (±50 chars)
            context = desc_text[max(0, match.start()-50):match.end()+50]
            suggested_ids.update(ITEM_ID_PATTERN.findall(context))

    if not suggested_ids:
        continue

    # Check reachability of suggested items
    reachable_items = collect_all_reward_and_task_items(Q's ancestors)
    for sid in suggested_ids:
        if sid in reachable_items:
            continue  # suggestion is reachable — OK
        # Check L1/L2 dimension map
        item_dim = (L2_dimension_map or BUILTIN_DIMENSION_MAP).get(sid)
        if item_dim and item_dim not in reachable_dimensions(Q):
            WARNING: "Quest {Q.name} suggests using {sid} from {item_dim},
                      but {item_dim} is not yet unlocked. Players following
                      the guide will be stuck."
        elif sid not in reachable_items:
            INFO: "[unverified:suggestion] {Q.name} suggests {sid} which is
                   not in any ancestor's rewards/tasks. Verify accessibility."
```

此规则对 kitchen-sink 包保持 INFO 级别（flexible 模式下玩家可以自行探索），对 expert/linear 包升级为 WARNING。

**违反了会怎样：** 玩家按照 quest 描述中的建议去准备装备，发现建议的物品还无法获得——描述在引导玩家走一条死路。这比 R1（task 物品不可达）更隐蔽，因为 task 物品不可达至少会在提交时被系统拒绝，而「建议」物品不可达只会让玩家浪费时间。

**来源：** FTB Architect's Exodus #12601 — "Malum's runes are not craftable before killing Hel, but are suggested for use"：quest 建议使用 Malum 符文，但符文需要 Rune Workbench → Hallowed Gold → Gold，而 Gold 在当前阶段还不可获得。FTB Architect's Exodus #12549 — Botania quest 描述错误地声称需要 Dominant Spark Augment（该物品需要 Pixie Dust → Alfheim Portal → Terrasteel，而 Terrasteel 是下一个 quest 的目标），形成 R14 + R1 + R24 三重违规。

---

### R25 — Task-Item Necessity Check

**数据依赖：** ⚠️ 需要了解 quest task 的 item 是否有替代获取路径（需要 JEI/EMI 或 L2 映射）| ✅ 无 L2 时可降级为启发式检查：当 description 明确提到替代方案但 task 仍要求特定物品时触发

**检查什么：** quest 的 task 要求一个物品，但包的合成/获取路径中该物品并非唯一途径——任务要求过于严格，排斥了合理的替代方案。这是 R8（Dependency Requirement Consistency）在物品层面的对应：R8 检查依赖关系是否要求了不必要的 quest，R25 检查 task 是否要求了不必要的物品。

**怎么检查：**

```
for each quest Q:
    for each item_task in Q.tasks:
        if item_task.type not in ("ftbquests:item", "item"):
            continue

        # Check if description mentions alternatives
        desc_text = " ".join(Q.description) if Q.description else ""
        alternatives_mentioned = extract_alternative_items(desc_text, item_task.item.id)
        # e.g., "you can also get X from bastions" → bastion loot is an alternative

        if alternatives_mentioned:
            for alt_item in alternatives_mentioned:
                if alt_item != item_task.item.id and is_valid_item(alt_item):
                    INFO: "Quest {Q.name} description mentions alternative
                           '{alt_item}' but task requires specifically
                           '{item_task.item.id}'. Consider accepting both
                           or making the alternative a separate optional task."

        # Check: is the task item achievable via the quest's stated method?
        # If description says "obtain from X" but X is blocked by stage,
        # and the task item has another path that IS available, this is
        # overly restrictive
        if item_task.consume_items == True:
            # Consuming task — the item is destroyed on submission
            # Check if the item is commonly obtained via multiple paths
            obtain_paths = estimate_obtain_paths(item_task.item.id)
            if len(obtain_paths) > 1 and is_overly_restrictive(Q, obtain_paths):
                INFO: "Quest {Q.name} consumes {item_task.item.id} which has
                       {len(obtain_paths)} obtain paths. Ensure all paths are
                       viable or clarify which path the quest expects."
```

`is_overly_restrictive` 是一个启发式函数：当 quest 的 dependency chain 只解锁了一条获取路径，但物品有其他可行路径时返回 true。这需要 L2/L3 数据才能准确判断，无外部数据时仅做 INFO 级别提示。

**违反了会怎样：** 玩家发现 quest 要求的物品可以通过另一条更简单的路径获得，但 quest 不认——或者 quest 要求了一个特定来源的物品，而描述中提到的替代来源不被 quest 系统承认。这在 expert 包中尤其令人沮丧，因为替代路径往往是玩家已经探索过的。

**来源：** FTB Architect's Exodus #12463 — "empowered netherite quest shouldn't require ancient debris"：empowered netherite 可以通过 bastions 获得（不需要 ancient debris），但 quest 要求 specifically ancient debris path。FTB StoneBlock 4 #11885 — "Antimatter quest required both paths"：quest 设为 `dependency_requirement: "all"` 但两条路径的 quest 都是 optional，形成了 optional-gate-mandatory 的经典 R7 + R8 违规，同时暗示 task 物品要求过于严格（R25 的物品层面体现）。

---

### R26 — Quest-Mod Version Consistency

**数据依赖：** ⚠️ 需要 mod 版本号 + changelog 数据（从 packwiz/modrinth 或 CurseForge API 获取）| ✅ 无版本数据时降级为纯文本启发式：检测 description 中的硬编码数值（count、level、tier）是否与已知 mod 默认值一致

**检查什么：** quest description 中引用的具体数值（物品 stack size、machine processing limit、energy capacity、acceleration card limit 等）是否仍然与 mod 当前版本一致。当 mod 更新改变了一个数值但 quest 文本没有同步更新，玩家按照旧数值操作会失败。

**怎么检查：**

```
HARDCODED_NUMBER_PATTERN = re.compile(
    r'(\d+)\s*(?:stack|limit|capacity|max|slots?|cards?|tier|level|upgrades?)',
    re.IGNORECASE
)

for each quest Q:
    if not Q.description:
        continue
    desc_text = " ".join(Q.description)

    for match in HARDCODED_NUMBER_PATTERN.finditer(desc_text):
        number = int(match.group(1))
        context = desc_text[max(0, match.start()-30):match.end()+30]

        # Extract the mod/item being referenced
        referenced_item = extract_referenced_item(context, Q.tasks)
        if referenced_item:
            # L2 check: compare with known mod values
            known_value = L2_mod_values.get(referenced_item, {}).get('limit')
            if known_value is not None and known_value != number:
                WARNING: "Quest {Q.name} states limit of {number} for
                          {referenced_item}, but mod value is {known_value}.
                          Quest text may be outdated."
            elif known_value is None:
                # No mod data — log for manual review
                INFO: "[manual-review] Quest {Q.name} mentions '{context.strip()}'
                       — verify this value matches the current mod version."
```

此规则主要作为 heuristic reminder——在包更新 mod 后提醒检查 quest 文本中的硬编码数值。完整的检查需要 packwiz lock file 或 modrinth API 的版本对比数据。

**违反了会怎样：** 玩家按照 quest 描述中的数值操作（例如放入 2 张 acceleration card），但 mod 更新后 limit 已变为 3（或者反过来），导致操作失败。这种问题在长期维护的包中反复出现——mod 更新频率远高于 quest 文本更新频率。

**来源：** FTB StoneBlock 4 #12328 — "Update Circuit Fabricator quest to reflect updated acceleration cards limit"：Circuit Fabricator 的 acceleration card limit 从 2 更新为 3，但 quest 文本没有同步，导致 "confusion"。FTB Evolution #12417 — "Link to Oritech's Particle Accelerator Wiki has changed"：quest 描述中的 wiki 链接失效。这些不是 AP1（description 说的是错的）而是 AP1 的时间维度变体——description 曾经是对的，但 mod 更新后变成了错的。

---

## 8. Safety & Team（安全与团队协作）

这类规则检查 command reward 的安全性和多人/团队模式下的进度一致性——两个在单人场景下不存在但在实际 modpack 部署中极为重要的问题。

### R28 — Command Reward Safety Scan

**数据依赖：** ✅ 可独立运行（纯正则匹配 command 字符串，无需外部数据）

**检查什么：** quest 的 `command` reward 中的命令字符串是否包含高风险或危险模式。输入字段：quest 的 `rewards`（`command` 类型）的 `command` 字段。

**怎么检查：**

```
# 危险命令 — 绝对禁止，ERROR 级别
FORBIDDEN_COMMANDS = [
    r'/op\b', r'/deop\b',
    r'/gamemode\s+(creative|spectator)',
    r'/stop\b', r'/kick\b', r'/ban\b',
    r'/whitelist\b',
]

# 高风险命令 — WARNING 级别，需要人工审查
HIGH_RISK_COMMANDS = [
    r'/fill\b',          # 可能覆盖玩家建筑
    r'/setblock\b',      # 同上
    r'/clone\b',         # 同上
    r'/clear\b',         # 清空玩家背包
    r'/kill\b',          # 杀死实体/玩家
    r'/effect\s+give.*\s([5-9]|\d{2,})\b',  # 高等级 effect amplifier
    r'/summon\b.*wither', # 召唤危险实体
    r'/execute\b',       # 嵌套执行，可能产生意外副作用
]

# 幂等性风险 — INFO 级别，提醒作者注意重复执行问题
IDEMPOTENCY_RISK = [
    r'/give\b',          # 重复执行会重复给物品
    r'/tp\b',            # 重复执行会重复传送
    r'/playsound\b',     # 重复执行会重复播放声音
]

for each quest Q:
    for each reward in Q.rewards:
        if reward.type not in ("ftbquests:command", "command"):
            continue
        cmd = reward.command

        # Check forbidden commands
        for pattern in FORBIDDEN_COMMANDS:
            if re.search(pattern, cmd, re.IGNORECASE):
                ERROR: "Quest {Q.name} command reward contains forbidden
                        command '{pattern}'. This command must not be used
                        as a quest reward."

        # Check high-risk commands
        for pattern in HIGH_RISK_COMMANDS:
            if re.search(pattern, cmd, re.IGNORECASE):
                WARNING: "Quest {Q.name} command reward contains high-risk
                          command '{pattern}'. Review for potential side
                          effects (world modification, entity damage, etc.)."

        # Check idempotency risks
        for pattern in IDEMPOTENCY_RISK:
            if re.search(pattern, cmd, re.IGNORECASE):
                INFO: "Quest {Q.name} command reward '{pattern}' is not
                       idempotent — re-claiming this quest will execute
                       the command again. Consider if this is acceptable."

        # Check {p} placeholder usage
        if '{p}' not in cmd and any(
            kw in cmd for kw in ['give', 'effect', 'tp', 'teleport', 'title']
        ):
            WARNING: "Quest {Q.name} command reward '{cmd}' affects a player
                      but doesn't use {p} placeholder. Hardcoded player names
                      will break in multiplayer."

        # Check cross-dimension commands
        if any(kw in cmd for kw in ['/tp', '/setblock', '/fill', '/clone']):
            if not re.search(r'(?:in|at)\s+\w+:\w+', cmd):
                INFO: "Quest {Q.name} coordinate-based command '{cmd}' doesn't
                       specify a target dimension. The command will execute in
                       the player's current dimension, which may not be intended."
```

此规则在 Step 4 逐节点生成时即可执行——command 字符串是 quest 配置的局部属性，不依赖依赖图或外部数据。FORBIDDEN_COMMANDS 触发时阻止写入 spec（ERROR）；HIGH_RISK_COMMANDS 和幂等性检查为 WARNING/INFO 级别。

**违反了会怎样：** AP15（Command Reward Side Effect）——command reward 的副作用可能导致物品重复、世界破坏、服务器崩溃或安全漏洞。这是 AI 生成 quest 配置时最危险的错误类型之一，因为 command 以服务器权限执行。

**来源：** AP15（Command Reward Side Effect）；MP29（Command Reward）的基本安全规则；Review B (Completeness Audit) 对 command reward 执行语义的分析。

---

### R29 — Team Progression Consistency

**数据依赖：** ⚠️ 需要用户在 Step 2 声明目标包是否支持多人/团队模式 | ✅ 无团队模式声明时降级为 INFO 提醒

**检查什么：** 当目标包支持 FTB Teams 多人模式时，quest 的 reward 分配模式和 dependency 结构是否与团队进度共享机制一致。输入字段：quest 的 `rewards`、`dependencies`、`optional` 标志、以及包的 `team_mode` 声明（用户在 Step 2 提供）。

**怎么检查：**

```
for each quest Q:
    if not pack_config.team_mode:
        continue  # solo-only pack, skip

    # Check 1: Material bridge in team mode
    # When a quest rewards an item that the next quest needs,
    # verify the reward distribution works for teams
    for reward in Q.rewards:
        if reward.type in ("ftbquests:item", "item"):
            dependents = find_dependents(Q)
            for dep_quest in dependents:
                for task in dep_quest.tasks:
                    if task.item.id == reward.item.id:
                        # Material bridge detected — check team compatibility
                        INFO: "Quest {Q.name} → {dep_quest.name} has a material
                               bridge ({reward.item.id}). In team mode, verify:
                               does the reward go to all team members or only
                               the submitter? If only the submitter, other team
                               members may lack the material for {dep_quest.name}."

    # Check 2: Fan-in convergence in team mode
    # MP8 convergence nodes with many dependencies may be trivially
    # completed by team division of labor
    if len(Q.dependencies) >= 5:
        INFO: "Quest {Q.name} is a fan-in convergence ({len(Q.dependencies)} deps).
               In team mode, team members can divide sub-trees — verify this
               is the intended design (team synthesis vs individual grind)."

    # Check 3: Optional path divergence
    # If team members can pick different optional paths, check that
    # mandatory content doesn't require a specific optional choice
    if Q.optional:
        mandatory_dependents = [
            dq for dq in find_dependents(Q)
            if not dq.optional
        ]
        if mandatory_dependents:
            WARNING: "Optional quest {Q.name} has mandatory dependents
                      {[dq.name for dq in mandatory_dependents]}.
                      In team mode, if one member skips this optional quest,
                      other members' mandatory progression may be blocked."
```

此规则在 Step 5 全图验证时执行——它需要完整的依赖图和 reward 分配数据。当目标包不支持团队模式时，整个规则跳过。当团队模式启用但缺乏详细信息时，降级为 INFO 级别的提醒。

**违反了会怎样：** 团队模式下的 quest 体验可能出现「搭便车」问题（一个成员完成所有 quest，其他成员被动获得进度）、材料分配不均（material bridge 只对提交者生效）、或 optional path 分歧导致 mandatory 进度被卡住。这些问题的根源是 quest 设计没有考虑多人场景的特殊性。

**来源：** Review B (Completeness Audit) — FTB Teams 多人进度共享机制分析；PP8（The Free Rider Problem，待补充）的团队教学模式。

---

## §9 QA & Formatting Standards (R30–R32)

本节规则来自对知名整合包作者设计哲学的直接研究——Monifactory 的 CONTRIBUTING.md 提供了最详尽的 quest book 格式与测试标准，Craftoria 的 issue tracker 揭示了 XP 奖励设计的隐患，Enigmatica 10 的零投诉现象暗示了 playtesting 流程的有效性。这些规则不检查物品可达性或依赖图健康，而是检查 quest 配置的「呈现层」——视觉层级、奖励一致性、以及 chapter 级别的完成度信号。它们是前五类规则（R1–R22）和第六至八类规则（R23–R29）的补充，覆盖了「quest 看起来对不对」和「quest 书被测试过吗」这两个常被忽视但直接影响玩家体验的维度。

### R30 — Quest Visual Hierarchy & Size Consistency

**数据依赖：** ✅ 无外部依赖——仅需 quest 的 `size`、`shape`、`optional`、`icon` 字段 | ✅ 所有数据在 Step 4 生成时可用

**检查什么：** quest 的视觉属性（size、shape、icon）是否与其在进度图中的语义角色一致。Monifactory 的 CONTRIBUTING.md 明确要求「Larger quests should be reserved for important milestones」，ATM-10 的数据也显示 capstone quest 的 size 始终大于同 chapter 的 routine quest（参见 MP20 Shape-as-Tier Signal）。当 routine quest 的 size 大于 milestone quest 时，视觉层级反转，玩家会误判进度重点。

**怎么检查：**

```
for each chapter C:
    quests = get_quests(C)
    if len(quests) < 3:
        continue  # too few quests for meaningful hierarchy

    # Classify quests by role
    milestones = []  # capstone, convergence, or high-dependency quests
    routines = []    # standard progression quests
    optionals = []   # optional/side quests

    for Q in quests:
        if Q.optional:
            optionals.append(Q)
        elif len(find_dependents(Q)) >= 3 or is_capstone(Q, C):
            milestones.append(Q)
        else:
            routines.append(Q)

    if not milestones or not routines:
        continue  # need both types for comparison

    # Check 1: Milestone size > routine size
    max_routine_size = max(Q.size for Q in routines)
    for M in milestones:
        if M.size < max_routine_size:
            WARNING: "Chapter {C.name}: milestone quest {M.name} (size={M.size})
                      is smaller than routine quest(s) with size={max_routine_size}.
                      Monifactory CONTRIBUTING.md states: 'Larger quests should be
                      reserved for important milestones.' Consider increasing
                      {M.name}'s size or decreasing routine quest sizes."

    # Check 2: Optional quests should not be larger than milestones
    max_milestone_size = max(M.size for M in milestones)
    for O in optionals:
        if O.size > max_milestone_size:
            INFO: "Chapter {C.name}: optional quest {O.name} (size={O.size})
                   is larger than the largest milestone (size={max_milestone_size}).
                   Optional content should use smaller or equal sizes to avoid
                   visual confusion about main progression path."

    # Check 3: Shape consistency within role
    milestone_shapes = set(M.shape for M in milestones if M.shape)
    if len(milestone_shapes) > 2 and len(milestones) >= 4:
        INFO: "Chapter {C.name}: milestone quests use {len(milestone_shapes)}
               different shapes ({milestone_shapes}). Consistent milestone shapes
               help players identify progression-critical quests at a glance.
               Consider standardizing to 1-2 milestone shapes per chapter."
```

此规则在 Step 5 全图验证时执行——它需要 chapter 内所有 quest 的 size/shape 数据用于比较。Step 4 生成时可执行 Check 1 的简化版（与同 chapter 已生成的 quest 比较）。

**违反了会怎样：** 玩家看到大 quest 以为是里程碑、看到小 quest 以为是支线，但实际进度方向相反。Monifactory 的 CONTRIBUTING.md 将 visual hierarchy 列为 quest book 设计的首要格式标准。ATM-10 的数据（MP20 Shape-as-Tier Signal）显示 ATM 系列在 64 个 chapter 中保持了稳定的 shape-size 语义映射——这种一致性不是偶然的，而是 deliberate design decision。

**来源：** Omicron-Industries/Monifactory CONTRIBUTING.md（"Larger quests should be reserved for important milestones"）；ATM-10 配置审计（MP20 Shape-as-Tier Signal，4,601 quests 的稳定 shape vocabulary）。

### R31 — XP-Level Reward Relativity

**数据依赖：** ✅ 无外部依赖——仅需 quest 的 `rewards` 字段和 reward 类型 | ✅ 所有数据在 Step 4 生成时可用

**检查什么：** 使用 `xp_levels`（经验等级）作为 reward 的 quest 是否仅出现在 milestone/chapter-ending 位置。Craftoria #289 明确记录了「Various quests have 'add xp level' rewards incentivising claiming them as late as possible」——当 XP 等级奖励出现在 routine quest 上时，reward 的实际价值完全取决于玩家领取时的等级，导致 reward 价值极度不一致。早期领取 = 高价值（等级低时升级快），晚期领取 = 低价值（等级高时升级慢）。

**怎么检查：**

```
for each quest Q:
    xp_rewards = [r for r in Q.rewards
                  if r.type in ("ftbquests:xp_levels", "xp_levels",
                                "ftbquests:xp", "xp")]

    if not xp_rewards:
        continue  # no XP rewards, skip

    # Determine if this is a milestone quest
    dependents = find_dependents(Q)
    # Note: shape-based milestone detection is ATM-series specific
    # (gear/pentagon/hexagon are ATM milestone shapes). Non-ATM packs
    # may use different shapes or none. Size comparison within chapter
    # is a more universal milestone indicator.
    chapter_median_size = median(q.size for q in get_chapter(Q).quests)
    is_milestone = (
        len(dependents) >= 3 or
        is_capstone(Q, get_chapter(Q)) or
        Q.size > chapter_median_size * 1.5 or  # universal: larger than typical
        Q.shape in ("gear", "pentagon", "hexagon", "diamond")  # † ATM-specific; hexagon is ambiguous (milestone vs cross-link nav)
    )

    # Only xp_levels rewards are affected by value drift; flat xp is consistent
    has_xp_levels = any(
        r.type in ("ftbquests:xp_levels", "xp_levels") for r in xp_rewards
    )

    if not is_milestone and has_xp_levels:
        total_xp = sum(
            getattr(r, 'xp_levels', getattr(r, 'xp', 0))
            for r in xp_rewards
        )
        WARNING: "Quest {Q.name} uses xp_levels reward (value={total_xp})
                  but is not a milestone quest ({len(dependents)} dependents).
                  Craftoria #289 documented that xp_levels rewards on routine
                  quests create wildly inconsistent value depending on player
                  level at claim time. Consider: (a) moving XP rewards to
                  milestone/capstone quests only, (b) replacing with fixed
                  item rewards, or (c) using flat XP (xp_points) instead of
                  XP levels for consistent value."

    # Check for mixed reward types
    non_xp_rewards = [r for r in Q.rewards
                      if r.type not in ("ftbquests:xp_levels", "xp_levels",
                                        "ftbquests:xp", "xp")]
    if xp_rewards and non_xp_rewards and not is_milestone:
        INFO: "Quest {Q.name} mixes xp_levels with item rewards on a
               non-milestone quest. The xp_levels portion will be valued
               differently by players at different progression stages,
               creating an inconsistent reward experience."
```

此规则在 Step 4 生成时即可执行（仅需当前 quest 的 reward 数据和已生成的 dependents），Step 5 可运行全量复查。

**违反了会怎样：** 同一个 XP 等级奖励，在 30 级时领取相当于 3 个钻石的价值，在 80 级时领取可能连 1 个铁锭都不值。这不是 reward inflation 或 reward desert，而是 reward 价值随玩家状态漂移——更隐蔽，也更难被包作者在测试时发现（因为测试时玩家通常在一个固定等级）。Craftoria 的 #289 issue 是目前唯一公开记录此问题的来源。

**来源：** TeamAOF/Craftoria #289（"Various quests have 'add xp level' rewards incentivising claiming them as late as possible"）。

### R32 — Chapter QA Coverage Heuristic

**数据依赖：** ✅ 无外部依赖——基于 chapter-level 的图结构统计 | ✅ 所有数据在 Step 5 可用

**检查什么：** 每个 chapter 是否满足基本的「可被 playtest 过」的结构性指标。这条规则不检查 quest 内容是否正确（那是 R1–R29 的工作），而是检查 chapter 是否存在典型的「未经测试」症状。Enigmatica 10 在 GitHub issue tracker 上的零 quest 投诉现象（参见 Phase 2 Cycle 3 研究）暗示了系统性 playtesting 的有效性——而 FTB Architect's Exodus 在上线数周内就积累了 16+ quest 问题，形成了鲜明对比。

**怎么检查：**

```
for each chapter C:
    quests = get_quests(C)
    if len(quests) < 5:
        continue  # too small for meaningful QA analysis

    # Signal 1: Dead-end detection (quests with no rewards and no dependents)
    # A quest that gives nothing and leads nowhere is likely untested
    dead_ends = []
    for Q in quests:
        if (not Q.rewards and
            not find_dependents(Q) and
            not Q.optional and
            not is_capstone(Q, C)):
            dead_ends.append(Q)

    if dead_ends:
        WARNING: "Chapter {C.name} has {len(dead_ends)} dead-end quest(s)
                  that are neither optional nor capstones: {[q.name for q in dead_ends[:5]]}.
                  These quests give no reward and lead to no subsequent quest.
                  Typical sign of untested quest chains where the author forgot
                  to add rewards or connect to the next quest."

    # Signal 2: Description coverage (quests with empty or very short descriptions)
    # Monifactory CONTRIBUTING.md emphasizes detailed quest descriptions
    empty_desc_ratio = sum(
        1 for Q in quests
        if not Q.description or len(Q.description.strip()) < 20
    ) / len(quests)

    if empty_desc_ratio > 0.3:
        WARNING: "Chapter {C.name} has {empty_desc_ratio:.0%} of quests with
                  empty or minimal descriptions (<20 chars). Monifactory's
                  CONTRIBUTING.md requires substantive descriptions for all
                  quests. High empty-desc ratio suggests the chapter was not
                  thoroughly reviewed."

    # Signal 3: Dependency orphan detection (quests with dependencies
    # pointing outside the chapter AND no incoming dependencies from within)
    orphans = []
    for Q in quests:
        if Q.dependencies:
            all_external = all(
                get_chapter(dep) != C for dep in Q.dependencies
                if dep in all_quests  # skip invalid refs (R22 covers those)
            )
            no_internal_incoming = not any(
                get_chapter(dep) == C
                for dep in find_direct_predecessors(Q)
            )
            if all_external and no_internal_incoming:
                orphans.append(Q)

    if len(orphans) >= 3:
        INFO: "Chapter {C.name} has {len(orphans)} quests that depend entirely
               on external chapters with no internal predecessor. These may be
               correct cross-chapter bridges, but are also typical of chapters
               that were designed in isolation without playtesting the full
               progression flow."

    # Signal 4: Completion sanity check
    # Verify the chapter can theoretically be 100% completed
    # (R20 covers structural testability; this checks for obvious blockers)
    # Exclude catalog chapters where quests are naturally independent islands
    independent_islands = sum(
        1 for Q in quests
        if not Q.dependencies and not find_dependents(Q)
    )
    is_catalog = (independent_islands / len(quests)) > 0.7

    optional_count = sum(1 for Q in quests if Q.optional)
    if optional_count == 0 and len(quests) > 10 and not is_catalog:
        INFO: "Chapter {C.name} has {len(quests)} quests with 0 marked optional.
               For a chapter this size, some optional side content is expected.
               100% mandatory chapters often indicate untested content that
               hasn't been reviewed for what's core vs what's supplementary."
```

此规则在 Step 5 全图验证时执行——它需要完整的 chapter 结构和跨 chapter 依赖数据。

**违反了会怎样：** 单条 warning 不代表 chapter 有问题，但多条 warning 同时触发是强烈的「未经 playtesting」信号。Enigmatica 10 之所以在 GitHub 上零 quest 投诉，最合理的解释是团队在发布前进行了系统性 playtesting，消除了 dead-end、empty description、orphan dependency 等基础问题。相比之下，FTB Architect's Exodus 在上线初期的 16+ quest issue 中，大多数（dead-end rewards、wrong descriptions、broken dependencies）都属于 R32 的检测范畴。这条规则的设计目标不是替代 playtesting，而是提供一组「最低限度 QA 检查」——如果连这些静态检查都没通过，chapter 几乎肯定没有经过充分测试。

**来源：** EnigmaticaModpacks/Enigmatica10（零 quest 投诉现象，Phase 2 Cycle 3 研究）；Omicron-Industries/Monifactory CONTRIBUTING.md（quest description 标准）；FTBTeam/FTB-Modpack-Issues（FTB Architect's Exodus 的 16+ quest issue 作为反面教材）。

---

## 规则执行优先级

校验管线按以下优先级执行，高优先级规则的 error 可能使低优先级规则的判断失效：

1. **R5** — Circular Dependency Detection（环不解决，其他图遍历都不可靠）
2. **R6** — Unreachable Quest Detection（不可达 quest 不参与其他检查）
3. **R20** — Chapter Completion Testability（结构性健康）
4. **R22** — Cross-Chapter Dependency Validity（悬空引用）
5. **R7** — Optional-Gate-Mandatory（gating 正确性）
6. **R1** — Dimension-Reachability（物品可达性第一关）
7. **R2** — Tool-Tier Item Reachability（物品可达性第二关）
8. **R4** — Pack-Type Stage Boundary（阶段一致性）
9. **R3** — Recipe-Chain Depth vs Dependency-Depth（深度一致性）
10. **R14** — Teach-Then-Do Ordering（教学顺序第一关）
11. **R16** — Dimension-Explore-Then-Craft Ordering（教学顺序第二关）
12. **R17** — Tool-Reward-Before-Use Ordering（教学顺序第三关）
13. **R15** — Complexity Escalation（复杂度递增）
14. **R10** — Reward-to-Dependent Bridge（reward 连贯性第一关）
15. **R11** — Reward-Target Accuracy（reward 连贯性第二关）
16. **R12** — Reward Value Progression（reward 节奏）
17. **R13** — Capstone Reward Magnitude（capstone reward）
18. **R8** — Dependency Requirement Consistency（dependency 语义）
19. **R9** — Dependency Depth Reasonableness（深度合理性）
20. **R18** — Description Coverage（描述覆盖率）
21. **R23** — Description-Item Consistency（描述-物品一致性，AP1 部分覆盖）
22. **R24** — Suggestion-Reachability（建议可达性，AP1 描述引导覆盖）
23. **R26** — Quest-Mod Version Consistency（版本一致性，AP1 时间维度覆盖）
24. **R25** — Task-Item Necessity（任务必要性，R8 物品层面补充）
25. **R19** — Bottleneck Spacing（bottleneck 密度）
26. **R21** — Hidden Quest Signpost（隐藏 quest 引导）
27. **R28** — Command Reward Safety Scan（command 安全扫描，Step 4 P0）
28. **R29** — Team Progression Consistency（团队进度一致性，Step 5 P1）
29. **R31** — XP-Level Reward Relativity（XP 等级奖励相对性，Step 4 P2）
30. **R30** — Quest Visual Hierarchy & Size Consistency（quest 视觉层级，Step 5 P3）
31. **R32** — Chapter QA Coverage Heuristic（chapter QA 覆盖启发式，Step 5 P3）

---

## 与 anti-patterns.md 的关系

本文档和 anti-patterns.md 是同一问题的两面：

| anti-patterns.md | progression-rules.md |
|---|---|
| AP1 Description-Reality Mismatch | **R23**（部分覆盖：description-item ID 文本匹配）+ **R24**（建议可达性）+ **R26**（版本一致性）|
| AP2 Circular Dependency Deadlock | **R5**（显式环）+ **R3**（recipe chain 深度对比） |
| AP3 Unfinishable Chapter | **R6** + **R20** |
| AP4 Wrong Gating | **R7** + **R8** + **R25**（物品层面的过度限制） |
| AP5 Empty Quest Description | **R18** |
| AP6 Dead-End Reward | **R10** + **R11** |
| AP7 Hidden Quest Trap | **R21** |
| AP8 Reward Inflation | **R12** + **R13** |
| AP9 Hallucination Cascade | **R23**（物品 ID 存在性验证）+ **R26**（版本一致性）+ SKILL.md `items.json5` 检查 |
| AP10 Style Homogenization | 无对应规则（需要 batch-level 统计分析，非单 quest 检查） |
| AP11 Batch Narrative Inconsistency | 无对应规则（需要跨 quest 文本一致性分析，建议 Step 5 人工审查） |
| AP12 Task-Item NBT Insensitivity | 无对应规则（需要运行时 NBT 匹配验证，非静态分析可检测） |
| AP13 Premature Item Submission | 无对应规则（FTB Quests mod 层面的状态机问题，需要确保任务物品在 quest 解锁后才可获得） |
| AP14 Custom Task Black Box | **R6/R20** 降级处理（含 custom task 的 quest 降级为 INFO，无法静态验证可完成性） |
| AP15 Command Reward Side Effect | **R28**（Command Reward Safety Scan，静态分析 command 字符串） |
| AP16 Quest State Migration | **R22** 扩展（更新场景下的 stale dependency reference 检测） |
| AP17 XP-Level Reward Relativity | **R31**（XP 等级奖励相对性检查）+ **R12**（reward value progression） |
| AP18 Reward Desert in Long Chains | **R19**（bottleneck spacing）+ **R13**（capstone reward magnitude）+ **R32**（QA 覆盖启发式） |

anti-patterns.md 是「错误 + 后果」的人类可读描述；progression-rules.md 是「检查条件 + 判断逻辑」的机器可执行版本。两者配合使用：anti-patterns 解释 WHY，progression-rules 定义 HOW。R23 + R24 + R26 共同覆盖了 AP1 的三个维度——静态文本匹配（R23）、引导性建议的可达性（R24）、以及时间维度上的版本一致性（R26）。AP1 的第四个维度——description 中给出的合成指南是否正确（例如"在熔炉中烧炼"但实际需要高炉）——仍然需要 JEI/EMI 运行时验证，建议作为 Step 5 的 heuristic 提醒。AP10、AP11、AP12 和 AP13 目前无法完全自动化——AP10/AP11 需要 batch 生成后的整体审查，AP12 需要运行时 NBT 验证，AP13 需要 quest 解锁时间与物品可获得时间的交叉分析。建议作为 Step 5 的 heuristic 提醒而非硬检查。

---

## Sources

1. **cesspit.net** — "Minecraft Is Not What You Think, or: How I Learned to Stop Worrying and Love the Expert Pack." Expert pack 进度公式、backward shortcut reward 模式、quest book 作为引导系统的质量标准。 https://cesspit.net/drupal/node/2832/

2. **FTBTeam/FTB-Modpack-Issues #6447** — "List of Observations in FTB Evolution (WIP)." 单玩家对 FTB Evolution 的 73+ 问题审计，涵盖 description mismatch、circular dependency、gating error、hidden quest、wrong tool reward。 https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447

3. **GTNH (GT New Horizons)** — GitHub README。Tech-tier gating 哲学（"using the tiers from GregTech and allocates content of other mods to a fitting point"）、3500+ quest 引导系统、age-based 进度设计。 https://github.com/GTNewHorizons/GT-New-Horizons-Modpack

4. **Enigmatica 2: Expert Extended** — GitHub README。Non-linear progression 哲学、custom ore processing 设计、balance 调优方法。 https://github.com/Krutoy242/Enigmatica2Expert-Extended

5. **awesome-packdev (Modern-Modpacks)** — Packdev 工具链集合，包含 Game Stages、Item Stages、Packmode 等 gating 工具的分类和说明。 https://github.com/Modern-Modpacks/awesome-packdev

6. **ATM-10 (AllTheMods/ATM-10)** — 4,601 quests / 64 chapters 的配置审计数据。Kitchen-sink flexible progression、capstone convergence、material-tier spine、XP drip reward 系统。 https://github.com/AllTheMods/ATM-10

7. **Create: Delight Remake** — 2,295 quests 的配置审计数据。Rich branching（one_started×63, one_completed×44）、teach-then-do 教学顺序、catalog vs narrative 设计分离。

8. **Mechanomania** — 395 quests 的配置审计数据。Minimalist 设计参考（零 hide_until_deps_visible、sparse reward）。

9. **Monifactory** — 248 quests 的结构审计数据。Voltage-tier gating、invisible routing chapters、deep dependency chains（depth 8-15）。

10. **ATM9-Sky** — Skyblock 配置审计数据。Tutorial depth 18（最深 chain）、resource-acquisition opener。

11. **Phase 1 micro-patterns.md** — 32 个微观模式（MP1-MP26 + PP1-PP6），提供 task 组合、dependency 拓扑、reward 桥接、stage 标记的量化数据。

12. **Phase 2 anti-patterns.md** — 8 个反面模式（AP1-AP8），提供 progression-rules 规则的人类可读对应。

13. **design-guide.md §principles** — F1-F3 foundational model、P1-P7 reusable patterns。Gating vs guidance 分离、in-chapter capstone 模型。

14. **difficulty-curve.md** — Phase breakdown（tutorial → early → mid → late → endgame）、bottleneck task 设计原则。

15. **reward-economy.md** — Reward tier 设计、progression/convenience/celebration/cosmetic reward 分类、anti-patterns。

16. **FTBTeam/FTB-Modpack-Issues（Phase 3 Cycle 2 审计）** — 30+ 条 type:Quest 标签 issue，覆盖 FTB Architect's Exodus（#12601, #12571, #12569, #12557, #12549, #12548, #12540, #12535, #12463, #12459, #12458）、FTB StoneBlock 4（#12328, #11885, #11880, #11730）、FTB Skies 2（#12004）、FTB Interactions Remastered（#12217）、FTB Evolution（#12428, #12418, #12417, #12400）。 https://github.com/FTBTeam/FTB-Modpack-Issues

17. **Laskyyy/Create-Astral Issues** — 4 条 quest 相关 issue（#689 quest registration, #642 dependency ordering, #618 description accuracy, #566 NBT insensitivity），提供了 Create-focused 包的设计反馈。 https://github.com/Laskyyy/Create-Astral/issues

18. **ATM-9 / ATM-10-Sky / All-the-Mons / Arcana** — AllTheMods 组织下 4 个包的 GitHub 仓库审计（README 仅含 bug report 指引，无 CONTRIBUTING.md 或 quest design wiki），确认 ATM 系列的设计哲学主要通过代码而非文档传达。

19. **Omicron-Industries/Monifactory CONTRIBUTING.md** — 最详尽的公开 quest book 格式标准。明确规定：「Larger quests should be reserved for important milestones」、WCAG AAA 色彩可及性标准、主进度 chapter 的 top-to-bottom flow 布局、noun highlight 仅在首次出现时应用、quest link 跨 chapter 引用规范。贡献者必须「test the basic functionality of every mod」并跨难度模式验证配置一致性。 https://github.com/Omicron-Industries/Monifactory/blob/main/CONTRIBUTING.md

20. **TeamAOF/Craftoria Issues** — 8 条 quest 相关 issue，最关键的是 #289（xp_levels reward 价值随玩家等级漂移）和 #231（Powah chapter 的 reward desert）。还包含 #607（linear→flexible gating 建议）、#352（optional-but-mandatory Mekanism quest）、#666（NBT sensitivity issue，验证 AP12）。 https://github.com/TeamAOF/Craftoria/issues

21. **EnigmaticaModpacks/Enigmatica10 Issues** — 零 quest 设计投诉（~20 issue 均为 Bug/Suggestion/Translation 标签），作为「有效 QA/playtesting 消除基础 quest 问题」的负面证据。#507 暗示 Expert 变体正在规划中。 https://github.com/EnigmaticaModpacks/Enigmatica10/issues

22. **AllTheMods/ATM-10 Discussion #3539** — "The Quest Book gives way too many rewards that break balance." TheBedrockMaster（ATM collaborator）明确提出 Capstone-Only Progression Break 原则："It is a kitchen sink pack, the only thing that could actually break progression would be gifting out ATM Stars." Utility items（Ender Chest, Universal Cables）不视为 progression-breaking。 https://github.com/AllTheMods/ATM-10/discussions/3539

23. **TeamAOF/Craftoria Issues #231, #607** — #231 记录了 Powah chapter 的 reward desert（3 tiers of reactors with no rewards）和 quest 重构请求。#607 提出 Iron's Spells 的 early gating 应从 crying obsidian 改为 basic table，推荐 `flexible` mode 用于"cleaner early game progression"。 https://github.com/TeamAOF/Craftoria/issues

24. **GregTech-Odyssey #1602** — HV tier 需要 400+ MV motors + 37 multiblock blocks + platline setup，但 quest book 没有 prepare players for the effort jump。玩家报告"easily running out of motivation"。建议增加 degraded pattern distributor 作为 intermediate reward。

25. **Monifactory #2359** — Tutorialisation debt：Aqueous Accumulator 不提及 pump configuration，玩家浪费 30 分钟才发现机制。AP5 在 expert pack 中的量化后果。

---

## Cycle 7 Phase 3 — Author-Interview-Derived Rules (R36-R41)

以下六条规则从整合包作者的设计文档、issue tracker 讨论和 GitHub discussion 中提炼。它们补充而非替代 R1-R35，侧重于作者在访谈中明确表达的设计理由（WHY），而不只是从配置数据中推断的统计规律。

### R36 -- Dependency Root Isolation

**Step 5 priority:** P2 (WARNING)
**Data dependency:** None (pure graph structure)

**Constraint:** Every quest must have at least one dependency, unless it is located in a designated root/hub chapter. Monifactory calls this the `dependencies` chapter; ATM-10 concentrates roots in each chapter group's opener chapter. A quest without dependencies in a standard progression chapter becomes an unpredictable orphan -- the player may stumble upon it accidentally or miss it entirely, and the quest book cannot control when it appears.

**Detection:**

```
ROOT_CHAPTERS = user-provided or ["dependencies", "getting_started", "welcome"]

for each quest Q:
    if not Q.dependencies:
        if Q.chapter.name not in ROOT_CHAPTERS:
            WARNING: "Quest {Q.name} has no dependencies but is not in a
                      designated root chapter. Add a dependency or move
                      to a root chapter."
```

**Why this matters (author rationale):** Monifactory CONTRIBUTING.md explicitly states "All quests should have at least one dependency except the quests in the 'dependencies' chapter" and the initial Genesis task. This ensures every quest has a defined entry point in the progression graph. A rootless quest in a non-root chapter is essentially a hidden quest without the `hide_until_deps_visible` flag -- it's visible but has no narrative or progression context.

**Validated against:** Monifactory (strict compliance -- all visible chapter quests have dependencies, roots concentrated in `dependencies` chapter). ATM-10 (roots concentrated in chapter group openers). Mechanomania and Cabricality have sporadic rootless quests in non-root chapters -- likely intentional catalog design but worth flagging.

**Source:** Omicron-Industries/Monifactory CONTRIBUTING.md (https://github.com/Omicron-Industries/Monifactory/blob/main/CONTRIBUTING.md)

---

### R37 -- Capstone-Only Progression Break (Reward Safety Tiers by Pack Type)

**Step 5 priority:** P2 (INFO for kitchen-sink, WARNING for expert)
**Data dependency:** Item tier estimation (L1 heuristic + L2 user data)

**Constraint:** In kitchen-sink packs (`progression_mode: "flexible"`), only capstone-tier items (ATM Star, Creative items, endgame-only items) constitute a true progression break when given as quest rewards. Utility items (Ender Chest, Universal Cable, basic machines) are sandbox tools, not progression items. In expert packs (`progression_mode: "linear"` or `"default"`), ANY gated item given early is a progression break.

**Detection:**

```
CAPSTONE_ITEMS = {
    "allthemodium:atm_star", "allthemodium:patrick_star",
    "minecraft:creative_mode_item",  # placeholder for any creative item
    # L2: user-provided capstone items
}

for each quest Q:
    for reward in Q.rewards:
        if reward.type in ("ftbquests:item", "item"):
            if reward.item.id in CAPSTONE_ITEMS:
                if not is_capstone(Q):
                    WARNING: "Capstone-tier reward {reward.item.id} on
                              non-capstone quest {Q.name}."
            elif pack_mode == "expert":
                item_stage = estimate_item_stage(reward.item.id)
                quest_stage = determine_stage(Q.chapter)
                if item_stage > quest_stage:
                    WARNING: "Expert pack: utility reward {reward.item.id}
                              (stage {item_stage}) on quest in stage
                              {quest_stage}. Even utility items can
                              break progression in linear mode."
```

**Why this matters (author rationale):** TheBedrockMaster (ATM-10 collaborator) in Discussion #3539: "It is a kitchen sink pack, the only thing that could actually 'break progression' would be gifting out ATM Stars." He specifically defends Ender Chests and Universal Cables as non-progression-breaking: "I don't see how being rewarded an Ender Chest would break balance or progression in a pack like this." This principle formalizes the kitchen-sink reward safety threshold: pack authors should document what constitutes a capstone item and only gate those.

**Validated against:** ATM-10 (rewards include Ender Chests, diamonds, and high-tier cables on routine quests -- defended as genre-appropriate). Expert packs (Monifactory, GT-O) never give gated materials early -- confirms the pack-type split.

**Source:** AllTheMods/ATM-10 Discussion #3539 (https://github.com/AllTheMods/ATM-10/discussions/3539)

---

### R38 -- Tier Transition Milestone Reward

**Step 5 priority:** P2 (WARNING)
**Data dependency:** Tier/chapter ordering + effort estimation

**Constraint:** When a quest chain crosses a technology tier boundary (e.g., MV to HV in GregTech, Basic to Hardened in Mekanism, Iron to Diamond in vanilla), the first quest at the new tier must include at least one reward that helps bridge the effort gap. This can be: (a) a material reward that partially satisfies new-tier crafting requirements, (b) a tool reward that speeds up new-tier processing, (c) an efficiency upgrade for an earlier-tier process. Chains crossing tier boundaries without intermediate rewards are AP18 (Reward Desert) amplified by effort spikes.

**Detection:**

```
for each quest Q:
    for dep_id in Q.dependencies:
        dep_quest = get_quest(dep_id)
        if tier_of(Q) > tier_of(dep_quest):
            # This quest crosses a tier boundary
            has_bridge_reward = any(
                r.type in ("ftbquests:item", "item")
                and estimate_item_stage(r.item.id) >= tier_of(Q)
                for r in Q.rewards
            )
            has_xp_reward = any(
                r.type in ("ftbquests:xp", "xp",
                           "ftbquests:xp_levels", "xp_levels")
                for r in Q.rewards
            )
            if not has_bridge_reward and not has_xp_reward:
                WARNING: "Quest {Q.name} crosses tier boundary
                          ({tier_of(dep_quest)} -> {tier_of(Q)})
                          but has no tier-appropriate reward.
                          Consider adding a material bridge,
                          tool reward, or XP to help players
                          bridge the effort gap."
```

**Why this matters (author rationale):** Craftoria #231 documents the Powah chapter going through "3 tiers of reactors with no relevant quest rewards" -- the player explicitly requests restructuring because the lack of rewards at tier transitions makes learning feel like a grind rather than guided progression. GregTech-Odyssey #1602 reports that the HV tier requires massive material investment with no rewards bridging the gap from MV, and suggests adding a degraded pattern distributor as an intermediate reward. The player explicitly states "even for an expert, being asked to make so many motors at HV is easy to make the player burn out."

**Validated against:** Craftoria #231 (Powah 3-tier reward desert), GregTech-Odyssey #1602 (HV effort spike without bridge), ATM-10 Mekanism chapter (tier transitions consistently reward intermediate materials).

**Source:** TeamAOF/Craftoria #231, GregTech-Odyssey #1602

> **报告冗余注意 (Cycle 7):** R38 与 R10（Reward Bridge）和 R19（Bottleneck Spacing）在 tier-transition quest 上存在三重覆盖。同一个 tier-transition quest 缺少 bridge reward 可能同时触发 R10（INFO: reward has no bridge）、R38（WARNING: tier transition without bridge reward）、R19（WARNING: bottleneck streak）。建议执行优先级：**R38 作为 R10 在 tier boundary 的增强版取代 R10 报告**——当 quest 跨越 tier boundary 时，R38 报告而 R10 静默；R19 独立报告（关注连续 bottleneck 的 pacing 问题，与 reward 维度正交）。

---

### R39 -- Guide Quest Deduplication

**Step 5 priority:** P3 (INFO)
**Data dependency:** Cross-chapter quest content analysis

**Constraint:** A "guide" or "help" quest (one that explains a mechanic without requiring progression items) should appear in at most one chapter. If the same mechanic needs referencing from multiple chapters, use quest links (cross-chapter references) rather than duplicating the quest. Monifactory's CONTRIBUTING.md states: "No quest should be needed in more than one 'Guides and Help' chapter."

**Detection:**

```
guide_quests = [q for q in all_quests
                if is_guide_quest(q)]  # checkmark/stat task + long desc + no item task

for each guide_quest in guide_quests:
    referenced_chapters = set()
    for Q in all_quests:
        if guide_quest.id in Q.quest_links or guide_quest.id in Q.dependencies:
            referenced_chapters.add(Q.chapter.name)
    if len(referenced_chapters) > 1:
        INFO: "Guide quest {guide_quest.name} is referenced from
               {len(referenced_chapters)} chapters: {referenced_chapters}.
               Consider using quest links from a single canonical location
               rather than duplicating."
```

`is_guide_quest` heuristic: quest has only checkmark/stat/observation tasks, description > 100 chars, and no item tasks. Alternatively, the quest is in a chapter named "guides", "help", "tutorial", or similar.

**Why this matters (author rationale):** Monifactory CONTRIBUTING.md explicitly forbids guide duplication: "No quest should be needed in more than one 'Guides and Help' chapter." This prevents maintenance burden (updating the guide in one place but not another) and player confusion (seeing slightly different versions of the same explanation in different chapters).

**Validated against:** Monifactory (strict compliance -- guide quests centralized in the `tutorials` chapter). ATM-10 (some duplication exists -- e.g., energy system explanations appear in multiple mod chapters, but this is mitigated by each explanation being mod-specific rather than generic).

**Source:** Omicron-Industries/Monifactory CONTRIBUTING.md

---

### R40 -- Effort Preview in Description (Tier Transition Context)

**Step 4 priority:** P2 (INFO)
**Step 5 priority:** P3 (INFO)
**Data dependency:** Chapter-level effort statistics

**Constraint:** Quest descriptions at technology tier transitions must include an effort preview -- a brief statement about the scale of work required at the new tier. This addresses the #1 cause of player burnout at tier boundaries: the surprise effort spike. The description should mention approximate resource requirements, new infrastructure needs, or time investment.

**Detection:**

```
EFFORT_KEYWORDS = [
    r'\d+\s*(?:items?|blocks?|ingots?|motors?|plates?)',
    r'multiblock', r'infrastructure', r'automation',
    r'significant', r'substantial', r'major investment',
    r'time.?consuming', r'prepare', r'stockpile',
    r'大量', r'需要较多', r'准备', r'自动化',
]

for each quest Q:
    for dep_id in Q.dependencies:
        dep_quest = get_quest(dep_id)
        if tier_of(Q) > tier_of(dep_quest):
            # Tier transition quest
            desc_text = " ".join(Q.description) if Q.description else ""
            has_effort_preview = any(
                re.search(pattern, desc_text, re.IGNORECASE)
                for pattern in EFFORT_KEYWORDS
            )
            if not has_effort_preview:
                INFO: "Quest {Q.name} crosses a tier boundary but its
                       description lacks an effort preview. Consider
                       adding: resource count estimates, new infrastructure
                       requirements, or approximate time investment."
```

**Why this matters (author rationale):** GregTech-Odyssey #1602 explicitly states the quest book doesn't prepare players for the HV effort spike: "even for an expert, being asked to make so many motors at HV is easy to make the player burn out." Monifactory #2359 quantifies the cost of missing context: players waste 30 minutes figuring out pump configuration for the Aqueous Accumulator because the description doesn't mention it. When descriptions don't set expectations, players calibrate effort against the previous tier and feel blindsided by the jump.

**Validated against:** GregTech-Odyssey #1602 (HV effort spike), Monifactory #2359 (30-minute tutorialisation debt), Craftoria #781 (AE2 chapter delegates all guidance to external guide without pack-specific context).

**Source:** GregTech-Odyssey #1602, Monifactory #2359

---

### R41 -- Early-Game Flexible Progression Mode

**Step 5 priority:** P2 (INFO for early-game linear chains)
**Data dependency:** Chapter order index + progression_mode

**Constraint:** The first N chapters of a pack (default N=3, configurable in Step 2) should use `flexible` progression mode rather than `linear`, even if the pack's overall mode is `linear`. Early-game linear gating forces new players into a single path before they understand the pack's scope, increasing bounce rate. The early chapters should serve as an orientation period where players can explore freely before committing to the pack's progression structure.

**Detection:**

```
FLEXIBLE_THRESHOLD = 3  # first 3 chapters should be flexible

for each chapter C:
    if C.order_index < FLEXIBLE_THRESHOLD:
        if C.progression_mode == "linear":
            INFO: "Chapter {C.name} (order_index={C.order_index}) uses
                   'linear' progression mode in the early game. Consider
                   'flexible' mode for the first {FLEXIBLE_THRESHOLD}
                   chapters to allow new players orientation freedom.
                   Linear gating is more effective after players understand
                   the pack's scope."
```

**Why this matters (author rationale):** Craftoria #607 explicitly recommends switching to `flexible` mode for Iron's Spells early gating because the crying obsidian requirement creates an unnecessary bottleneck before players understand the mod's mechanics. The issue states that flexible mode "allows for cleaner early game progression." This principle aligns with the game design concept of "onboarding" -- early content should teach and orient, not gate and restrict. Expert packs that use linear mode throughout (Monifactory, GT-O) mitigate this by having invisible routing chapters handle the gating logic while visible chapters remain flexible.

**Validated against:** Craftoria #607 (flexible mode recommendation for early gating), ATM-10 (all chapters use flexible mode), Monifactory (visible chapters are flexible, invisible chapters handle linear gating via MP23).

**Source:** TeamAOF/Craftoria #607 (https://github.com/TeamAOF/Craftoria/issues/607)

---

## Updated Execution Priority Table (with R36-R41)

The new rules fit into the existing priority framework as follows:

### Step 4 additions

| Priority | Rule | Check type | Failure behavior |
|---|---|---|---|
| **P2** | R40 Effort Preview (tier transition) | Keyword scan | INFO -- remind author |

### Step 5 additions

| Priority | Rule | Check type |
|---|---|---|
| **P2** | R36 Dependency Root Isolation | Graph scan |
| **P2** | R37 Capstone-Only Progression Break | Tier estimation |
| **P2** | R38 Tier Transition Milestone Reward | Cross-tier + reward check |
| **P2** | R41 Early-Game Flexible Mode | Chapter mode check |
| **P3** | R39 Guide Quest Deduplication | Cross-chapter reference scan |

### Updated AP mapping

| Anti-pattern | New rule coverage |
|---|---|
| AP4 Wrong Gating | **R41** (early-game flexible mode reduces hard-gating friction) |
| AP5 Empty Description | **R40** (effort preview is a specific description requirement) |
| AP8 Reward Inflation | **R37** (capstone-only progression break clarifies what counts as "too generous") |
| AP18 Reward Desert | **R38** (tier transition rewards specifically address cross-tier deserts) |

### Updated rule execution priority (full list, R1-R41)

32. **R36** -- Dependency Root Isolation (dependency graph hygiene, Step 5 P2)
33. **R37** -- Capstone-Only Progression Break (reward safety tiers, Step 5 P2)
34. **R38** -- Tier Transition Milestone Reward (cross-tier bridging, Step 5 P2)
35. **R39** -- Guide Quest Deduplication (content maintenance, Step 5 P3)
36. **R40** -- Effort Preview in Description (tier transition context, Step 4 P2)
37. **R41** -- Early-Game Flexible Progression Mode (onboarding design, Step 5 P2)

---

## Cycle 10 Phase 3 Additions (R51–R54)

Rules extracted from author design philosophy research across 54 packs, cesspit.net expert pack analysis, and MC百科 modpack descriptions.

---

### R51: Reward Architecture Role Alignment (奖励架构角色对齐)

**Category:** Reward Continuity
**Severity:** WARNING
**Phase:** Step 2 (pack planning)

**Rule:** When a pack declares its questbook role (R46), the reward architecture must align with that role. Mismatches between declared role and actual reward distribution indicate either an undeclared role change or an architectural inconsistency.

**Role-Reward Alignment Matrix:**

| Questbook Role | Expected Reward Model | Safe Deviation |
|---|---|---|
| **Companion** (Path of Truth, GTM Community) | Zero rewards OR XP-only | None — item rewards introduce redundancy |
| **Guide** (ATM-10, RAD3) | Item rewards with material bridges | XP-only chapters if declared |
| **Hybrid** | Mixed, but per-chapter declaration required | N/A — declaration IS the requirement |

**Detection:**

```
ROLE_REWARD_MAP = {
    "companion": {"zero": OK, "xp_only": OK, "item": WARNING},
    "guide":     {"zero": WARNING, "xp_only": INFO, "item": OK},
    "hybrid":    {"any": CHECK_CHAPTER_DECLARATION},
}

for each pack P:
    declared_role = P.questbook_role  # from R46
    actual_reward_model = classify_rewards(P.all_quests)

    if actual_reward_model not in ROLE_REWARD_MAP[declared_role].safe:
        WARNING: "Pack '{P.name}' declares '{declared_role}' role but uses
                 '{actual_reward_model}' reward model. Expected:
                 {ROLE_REWARD_MAP[declared_role].safe}. Either update
                 the role declaration or adjust reward architecture."
```

**Why this matters (author rationale):** cesspit.net's expert pack analysis shows that the questbook itself IS the reward in companion-mode packs: "a great guide to erase the problem of guessing recipes, and a clear path." Adding item rewards to a companion-mode pack creates player confusion about whether the questbook is a guide or a progression gate. GTCEu's intrinsic satisfaction model ("每一步都伴随着成就感") further validates that engineering accomplishment, not item collection, drives engagement in expert packs.

**Validated against:** GTM Community Pack (1282 quests, zero rewards, companion role), ATM-10 (generous rewards, guide role), Path of Truth (zero rewards, companion role), RAD3 (105 reward tables, guide role).

**Source:** cesspit.net "Minecraft Is Not What You Think" (node/2832), CSDN GTCEu article, Phase 2 zero-reward analysis (R50).

---

### R52: Unlock Leniency Declaration (解锁宽严声明)

**Category:** Dependency Integrity
**Severity:** INFO
**Phase:** Step 5 (full-graph validation)

**Rule:** When a pack's `dependency_requirement` distribution is skewed (>70% one_started OR >70% all_completed), the pack description or questbook introduction should explicitly state the unlock philosophy. Silent skew suggests an unconscious design choice that may confuse players.

**Leniency Spectrum:**

| dependency_requirement | Player experience | Author obligation |
|---|---|---|
| **one_started majority (>70%)** | Freedom-oriented. Multiple paths through tech tree. Quest completion is additive. | Declare: "This pack allows alternative progression paths" |
| **all_completed majority (>70%)** | Gate-oriented. Must complete all prerequisites. Quest completion IS the gate. | Declare: "This pack requires completing all prerequisites before advancing" |
| **Mixed (30-70% either)** | Variable per chapter. | Chapter-level declaration recommended |

**Detection:**

```
SKEW_THRESHOLD = 0.70

total_quests = count(P.all_quests)
one_started_count = count(q for q in P.all_quests
                         if q.dependency_requirement == "one_started")
all_completed_count = count(q for q in P.all_quests
                           if q.dependency_requirement == "all_completed")

one_started_ratio = one_started_count / total_quests
all_completed_ratio = all_completed_count / total_quests

if one_started_ratio > SKEW_THRESHOLD:
    if not P.has_unlock_declaration("one_started"):
        INFO: "Pack '{P.name}' uses one_started for {one_started_ratio:.0%}
               of quests (freedom-oriented design) but has no explicit
               unlock philosophy statement. Consider adding a questbook
               introduction explaining the multi-path approach."

elif all_completed_ratio > SKEW_THRESHOLD:
    if not P.has_unlock_declaration("all_completed"):
        INFO: "Pack '{P.name}' uses all_completed for {all_completed_ratio:.0%}
               of quests (gate-oriented design) but has no explicit
               unlock philosophy statement. Consider adding a questbook
               introduction explaining the prerequisite requirement."
```

**Why this matters (author rationale):** DeceasedCraft uses 97% one_started — the most extreme leniency in the 54-pack dataset — but no author statement exists explaining this choice. Players encountering this pack may not understand whether quests are optional alternatives or mandatory gates. Conversely, Monifactory/GTNH use strict all_completed (expert pack convention) but also lack explicit declarations, relying on genre expectation. Making the choice explicit prevents player confusion and helps the pack attract its intended audience.

**Validated against:** DeceasedCraft (97% one_started, no declaration — negative validation), Monifactory/GTNH (strict all_completed, implicit genre convention), ATM-10 (mixed, chapter-variable).

**Source:** DeceasedCraft config analysis (Phase 1), Monifactory CONTRIBUTING.md (Phase 1).

---

### R53: Task Complexity Utility Proportionality (任务复杂度效用正比)

**Category:** Pacing / Task Design
**Severity:** INFO (per-node) / WARNING (statistical)
**Phase:** Step 4 (per-node generation) + Step 5 (statistical validation)

**Rule:** The number of tasks per quest should be proportional to the item's utility frequency in the pack's progression. High-demand items (used in many downstream recipes) justify multi-task synthesis quests; single-use items should use single-task quests.

**Complexity-Utility Matrix:**

| Downstream fan-out | Recommended task count | Quest type |
|---|---|---|
| **0-1 recipes** (single-use) | 1 task | Simple fetch/craft |
| **2-3 recipes** (moderate use) | 1-2 tasks | Standard quest |
| **4+ recipes** (high demand) | 2-4+ tasks | Synthesis quest |

**Detection:**

```
# Step 4 (per-node)
SIMPLE_THRESHOLD = 2  # tasks
COMPLEX_MIN_FANOUT = 3  # downstream recipes

for each quest Q being generated:
    task_count = len(Q.tasks)
    item_id = Q.primary_item  # the main item being crafted/collected

    # Estimate utility frequency from known recipe graph
    fanout = count_downstream_recipes(item_id)

    if task_count > COMPLEX_THRESHOLD and fanout <= 1:
        INFO: "Quest '{Q.name}' has {task_count} tasks but its primary
               item '{item_id}' is used in only {fanout} downstream
               recipe(s). Consider simplifying to 1 task, as single-use
               items 'should be craftable in one step' (cesspit.net)."

# Step 5 (statistical)
MISMATCH_THRESHOLD = 0.20  # 20% of quests

mismatched = [q for q in P.all_quests
              if q.task_count > 2 and q.primary_fanout <= 1]

if len(mismatched) / len(P.all_quests) > MISMATCH_THRESHOLD:
    WARNING: "Pack '{P.name}' has {len(mismatched)} quests ({ratio:.0%})
              with high task complexity (3+) for low-utility items
              (fanout <= 1). Systematic complexity-utility mismatch
              suggests over-engineering of simple progression steps."
```

**Why this matters (author rationale):** cesspit.net's "Get It Right" blog post establishes the clearest design principle found in this research: "everything that's constantly on demand can be as convoluted as you like" versus "everything that has single uses should have be craftable in one step." This directly maps to quest task design — a quest with 4 tasks for an item used once creates unnecessary friction, while a quest with 4 tasks for a core component used in 10+ downstream recipes is justified synthesis.

**Validated against:** ATM-10 (ATM Star chapter: 3.6 tasks/quest for high-fanout items; standard mod chapters: 1.0-1.2 tasks/quest for low-fanout items — Phase 1 data). Path of Truth (14 custom task types for high-complexity progression items).

**Source:** cesspit.net "Get It Right" (node/3014), Phase 1 task-count-per-quest analysis.

---

### R54: Named Reward Table Semantic Match (命名奖励表语义匹配)

**Category:** Reward Continuity / Reward Table Design
**Severity:** WARNING
**Phase:** Step 5 (reward audit)

**Rule:** When a pack uses named reward tables (FTB Quests `reward_tables/` directory), table names must semantically match their content pool. A table named "early_tools" should contain early-game tools, not endgame items. The FTB Quests tool does NOT enforce meaningful naming — creators can "随便取个名" (just pick any name) — making this a pack author responsibility.

**Naming Convention Recommendation:**

| Format | Example | Suitable for |
|---|---|---|
| `{tier}_{category}` | `lv_circuits`, `ev_materials` | Expert packs with tiered progression |
| `{source}_{type}` | `nether_loot`, `boss_drops` | Adventure packs with location-based rewards |
| `{stage}_{purpose}` | `earlygame_starter`, `endgame_capstone` | Any pack with clear stage divisions |

**Detection:**

```
TIER_KEYWORDS = {
    "early": ["wood", "stone", "iron", "create"],
    "mid":   ["steel", "gold", "diamond", "mekanism"],
    "late":  ["netherite", "nbt", "draconic", "avaritia"],
    "endgame": ["creative", "atm_star", "ultimate"],
}

for each reward_table RT in P.reward_tables:
    table_name = RT.name.lower()
    table_items = RT.items

    # Estimate intended tier from name
    intended_tier = match_tier_keywords(table_name)

    # Estimate actual tier from items
    actual_tiers = [estimate_item_tier(item) for item in table_items]
    dominant_tier = mode(actual_tiers)

    if intended_tier and dominant_tier and intended_tier != dominant_tier:
        WARNING: "Reward table '{RT.name}' implies tier '{intended_tier}'
                  but contains predominantly '{dominant_tier}' items.
                  Consider renaming to '{dominant_tier}_{category}' or
                  reviewing the item pool."

    # Check for generic/meaningless names
    if table_name in ["table1", "table2", "test", "default", "rewards"]:
        INFO: "Reward table '{RT.name}' uses a generic name. Consider
               a descriptive name following {tier}_{category} format."
```

**Why this matters (author rationale):** RAD3 uses 105 named reward tables — the most complex reward architecture in the 54-pack dataset. The FTB Quests tutorial (mcmod.cn/post/1416) confirms that naming is entirely optional and unguided: "随便取个名" (just pick any name). Without naming discipline, loot crate rewards become opaque to players — they can't anticipate what a "Table_47" crate might contain. Semantic naming makes the reward system transparent and helps players make informed decisions about which quests to prioritize.

**Validated against:** RAD3 (105 named tables, naming convention unverified), ATM-9 (reward tables use descriptive names like "refined_storage_base_materials" — positive validation from Gitee mirror).

**Source:** RAD3 config analysis (Phase 1), FTB Quests tutorial (mcmod.cn/post/1416), ATM-9 reward table naming patterns.

---

## Updated Execution Priority Table (with R51-R54)

The new rules fit into the existing priority framework as follows:

### Step 2 additions

| Priority | Rule | Check type | Failure behavior |
|---|---|---|---|
| **P2** | R51 Reward Architecture Role Alignment | Role-reward cross-reference | WARNING — reward mismatch |

### Step 4 additions

| Priority | Rule | Check type | Failure behavior |
|---|---|---|---|
| **P3** | R53 Task Complexity Utility Proportionality (per-node) | Task count vs estimated utility | INFO — complexity mismatch |

### Step 5 additions

| Priority | Rule | Check type | Failure behavior |
|---|---|---|---|
| **P2** | R52 Unlock Leniency Declaration | dependency_requirement statistics | INFO — no declaration found |
| **P3** | R53 Task Complexity Utility Proportionality (statistical) | Task count vs downstream fan-out | WARNING — systematic mismatch |
| **P3** | R54 Named Reward Table Semantic Match | Name-content keyword analysis | WARNING — semantic mismatch |

### Updated AP mapping (with R51-R54)

| Anti-pattern | New rule coverage |
|---|---|
| AP8 Reward Inflation | **R51** (role alignment prevents over-rewarding in companion packs), **R54** (named tables should match content) |
| AP14 Random Loot Table Confusion | **R54** (semantic naming makes loot tables predictable) |
| AP20 Quest Tab Overwhelm | **R52** (unlock leniency declaration forces author to think about freedom vs gating) |

### Updated rule execution priority (full list, R1-R54)

38. **R51** -- Reward Architecture Role Alignment (role-reward consistency, Step 2 P2)
39. **R52** -- Unlock Leniency Declaration (dependency_requirement transparency, Step 5 P2)
40. **R53** -- Task Complexity Utility Proportionality (task design, Step 4 P3 / Step 5 P3)
41. **R54** -- Named Reward Table Semantic Match (reward table naming, Step 5 P3)
