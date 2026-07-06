# Shared Builtin Tables (L1 Data)

> **Core question:** R1-R4 在没有外部数据时能做什么？
> **用途：** R1-R4 的内置降级映射表。被 mod-item-reachability 引用。
> **加载时机：** Step 4 开始时（与 mod-item-reachability 一起）
> **Lines:** ~153 | **Step 4 load:** yes | **Step 5 load:** yes

---

## 数据依赖总览

R1-R4（Item Reachability）是校验管线中价值最高但数据依赖最重的规则。在没有外部数据（JEI/EMI 配方、mod 源码）的情况下，每条规则采用**三层数据策略**：

| 层级 | 数据源 | 覆盖范围 | 何时可用 |
|---|---|---|---|
| **L1 — 内置映射** | 下文硬编码的常识表 | ~20-50 个跨包常见物品 | 始终可用，无需任何外部数据 |
| **L2 — 用户/Step 2 提供** | 用户在 Step 2 interview 中定义的映射 | 包特有的关键物品 | 用户提供后可用 |
| **L3 — JEI/EMI 推断** | 从配方数据自动推断 | 全部物品 | 需要 toolchain 支持 |

规则执行时按 L1 -> L2 -> L3 优先级查找数据。L1 命中时直接检查，无需外部数据。仅当 L1 和 L2 都未命中时才降级为 `[unverified]`。这意味着即使没有任何外部数据，R1-R4 也能对 20-50 个最常见的 vanilla 和跨包物品执行有意义的检查。

每条规则的数据依赖标注格式：

```
**数据依赖：** L1 (shared-builtin-tables) / L2 (user) / L3 (JEI/EMI)
```

---

## 内置维度映射表（R1 L1）

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
    "the_bumblebee:bee_stinger":        "the_bumblezone:the_bumblezone",
    "undergarden:cloggrum_ingot":       "undergarden:undergarden",
    # === ATM series signature ===
    "allthemodium:allthemodium_ingot":  "minecraft:overworld",
    "allthemodium:vibranium_ingot":     "minecraft:the_nether",
    "allthemodium:unobtainium_ingot":   "minecraft:the_end",
}
```

---

## 内置工具等级映射表（R2 L1）

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
    "minecraft:diamond_ore":          2,
    "minecraft:deepslate_diamond_ore":2,
    "minecraft:ancient_debris":       3,
    "minecraft:emerald_ore":          2,
    "minecraft:gold_ore":             2,
    "allthemodium:allthemodium_ore":  4,
    "allthemodium:vibranium_ore":     5,
    "allthemodium:unobtainium_ore":   6,
}
```

---

## 内置合成深度估算启发式（R3 L1）

对于没有 JEI/EMI 配方数据的物品，使用物品名称和 mod namespace 推断粗略的合成深度。这远不如实际配方展开准确，但比完全跳过（`[unverified]`）好。

```
def estimate_recipe_depth_heuristic(item_id: str) -> int:
    """
    粗估合成深度。返回值为估算深度，-1 表示无法估算。
    这不是精确的配方展开，而是一个基于命名约定的 heuristic。
    """
    namespace, name = item_id.split(":", 1) if ":" in item_id else ("minecraft", item_id)

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
    return -1  # unknown -> still degrades to [unverified:recipe_depth]
```

误差范围约 +/-2 级深度。对于 kitchen-sink 包（`ALLOWANCE` 默认 2），这已经足够捕捉「合成链 5 步深但 quest chain 只有 1 步」这类严重不匹配。对于 expert 包（合成链深度可达 15+），建议用户在 Step 2 提供关键物品的精确深度。

---

## Cross-References

| 引用方 | 引用内容 |
|---|---|
| mod-item-reachability | R1 使用 BUILTIN_DIMENSION_MAP, R2 使用 BUILTIN_TOOL_TIER_MAP + BUILTIN_ORE_REQUIREMENTS, R3 使用 estimate_recipe_depth_heuristic, R4 降级时交叉引用 |
