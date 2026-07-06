# Mod Item Reachability

> **Core question:** 玩家此刻拿得到这个物品吗？
> **Lines:** ~304 | **Step 4 load:** yes | **Step 5 load:** full

## Quick Reference

| ID | 标题 | Phase | 严重度 | 包类型 |
|---|---|---|---|---|
| MP1 | Single-Item Gate | Step 4 | -- | all |
| MP5 | Dimension + Item Composite | Step 4 | -- | kitchen-sink, story, skyblock |
| MP13 | Explore-Then-Craft | Step 2 | -- | kitchen-sink, story, skyblock |
| MP31 | Structure Discovery Gate | Step 4 | -- | skyblock, kitchen-sink, story |
| MP33 | Advancement Gate | Step 4 | -- | all |
| PP7 | Mod-Unification Trap | Step 2 | WARNING | all |
| AP1 | Description-Reality Mismatch (item-identity) | Step 4 | ERROR | all |
| R1 | Dimension-Reachability | S4/S5 | ERROR/WARNING | all |
| R2 | Tool-Tier Item Reachability | S4/S5 | WARNING | all |
| R3 | Recipe-Chain Depth | S4/S5 | WARNING | all |
| R4 | Stage Boundary | S4/S5 | ERROR/INFO | all |
| R16 | Dimension-Explore-Then-Craft | S4/S5 | WARNING | kitchen-sink, story, skyblock |
| R24 | Suggestion-Reachability | S4/S5 | WARNING/INFO | all |

---

## Patterns

### MP1 -- Single-Item Gate (the universal baseline)

**Applicable when:** designing any standard progression step in any pack genre. This is the default -- 90%+ of quests across all audited packs.

**Implementation:** One `item` task with `count: 1` (or the recipe's output count). No `consume_items`, no `only_from_crafting`. The quest title names the item; the description explains *why* the player wants it and *how* to get it. Shape inherits the chapter's `default_quest_shape`.

The single-task quest is the atomic unit of FTB quest design. It works because the quest UI already shows the item icon, count, and completion status -- the quest author's job is context, not enumeration. When a mod has 20 recipes to teach, that's 20 single-task quests, not one 20-task quest.

**Real case (ATM-10, AllTheModium):** Root quest requires one `minecraft:netherite_ingot` -- a simple gate before AllTheModium content. `gear` shape `size: 2.0` at `(0, 0)`, single task + single reward (guide book).

**Design considerations:** Single-item gate is the baseline -- deviate only with deliberate intent. Multi-task quests signal synthesis.

---

### MP5 -- Dimension + Item Composite

**Applicable when:** a quest gates both exploration AND crafting -- the player must reach a new dimension AND bring back something from it. Common for dimension-gated progression (Nether, End, Twilight Forest, etc.).

**Implementation:** Two tasks in one quest: one `dimension` task (enter the dimension) and one `item` task (obtain the dimension-specific material). Both must be completed (AND logic, the default). The dimension task auto-completes on entry; the item task requires the player to actually do something while there.

This composite says "go there AND come back with proof." It's stronger than either task alone: a dimension-only quest could be completed by accidentally falling in; an item-only quest could be completed by trading. The composite ensures the player actually explored.

**Real case (ATM-10):** Root quest uses `dimension: "minecraft:overworld"` task. Twilight Forest uses dimension + item composites to gate boss progression.

**Design considerations:** Dimension and item tasks should be logically related. Frequency is genre-dependent: RPG > adventure > skyblock > kitchen-sink > expert.

---

### MP13 -- Explore-Then-Craft (Dimension-Gated Pacing)

**Applicable when:** a crafting recipe requires materials from a specific dimension or biome. The player must first travel, then craft.

**Implementation:** Quest A is a `dimension` or `biome` task (go there). Quest B `depends_on: [A]` and is an `item` task requiring materials found in that dimension. Quest C `depends_on: [B]` and requires crafting the materials into a product. The chain is: travel -> gather -> craft.

This pacing creates a natural rhythm: the player explores a new area, gathers resources while there, then returns home to craft. The dimension task auto-completes (just enter the dimension), but the item task requires actual effort in that dimension.

**Real case (ATM-10, main questline):** Dimension transitions: Overworld -> Nether -> End -> Twilight Forest. Each has a `dimension` task followed by dimension-specific item tasks.

**Design considerations:** Always ensure the dimension quest precedes the item quest in the dependency chain. R16 checks this automatically.

---

### MP31 -- Structure Discovery Gate (find-a-structure progression)

**Applicable when:** a quest requires locating a specific generated structure. Skyblock (structures rare/gated), kitchen-sink (exploration gates), RPG (dungeon entries).

**Implementation:** A `structure` task with `structure: "<namespace>:<structure_name>"`. Auto-completes when player enters the bounding box. Description should explain what the structure looks like, what dimension, and locating tools (Nature's Compass, Eye of Ender).

Differs from dimension tasks: dimensions are broad (enter Nether = auto-complete), structures are specific (find Fortress within Nether). Stronger gate -- player must actively search.

**Real case (ATM-10-Sky):** `structure: "minecraft:fortress"` gates Blaze Rod access. All-the-Mons uses 23 structure tasks for prehistoric sites.

**Design considerations:** (1) Verify structure generates in custom terrain (skyblock/void). (2) Provide fallback location hints. (3) Don't chain multiple structure tasks in one quest.

---

### MP33 -- Advancement Gate (vanilla advancement as progression checkpoint)

**Applicable when:** gating behind a vanilla advancement milestone (dimension entry, boss kill, rare item). Natively supported by FTB Quests, no KubeJS needed.

**Implementation:** An `advancement` task with `advancement: "<namespace>:<advancement_path>"`. Auto-completes when the player earns the advancement. Silent checkpoint -- no item submission required, player keeps earned items, can't be cheesed by trading.

**Real case (Enigmatica 10):** 3+ quests use advancement tasks as dimension-gate and boss-kill checkpoints -- entering the Nether earns `minecraft:nether/root`, quest auto-completes, unlocking Nether content.

**Design considerations:** (1) Verify advancement ID exists. (2) Pair with visible reward for feedback. (3) Can trigger gamestages: advancement -> auto-complete -> grant stage. (4) Unlike `custom` tasks (AP14), safe for AI generation.

---

## Anti-Patterns

### PP7 -- The Mod-Unification Trap (same name, wrong mod)

**What players notice:** Player obtains the item -- same display name, same icon -- but quest doesn't accept it, or the item doesn't work in the next recipe.

**Pattern:** In 200+ mod packs, multiple mods provide overlapping items (steel dust, electrum ingot). Tag unification doesn't always collapse them. When quest references the wrong variant: "I have exactly what the quest asks for, and it won't accept it."

**Config implication:** (1) Always use full `modid:item_name`. (2) Verify which mod's variant is canonical for the pack's recipe chains. (3) Verify reward namespace matches next quest's task namespace.

**Real case (FTB Skies 2 #11432):** Steam Blast Furnace rewards `ftbmaterials:steel_dust` -- but MI furnace requires `modernindustrialization:steel_dust`. Same name, wrong mod.

**Relationship:** PP7 is a player-experience variant of AP6 and AP1. Harder to detect via R10/R11 because the item ID is valid -- just not the *right* one. Needs `extract_items.py` duplicate display name check.

---

### AP1 -- Description-Reality Mismatch (item-identity variant)

**Symptom:** Description mentions item X, but the task requires item Y. "The Ore of the Eclipse Quest talks about Shadowflame Goo, but asks for Shadowpulse Goo."

**Root cause:** The `description` field is free-form text with no validation against task/reward data.

**Consequence:** Players stop trusting quest descriptions entirely.

**Detection:** R23 (Description-Item Consistency) catches ID-level mismatches via regex. R24 catches suggestion-reachability. R26 catches version drift. Full AP1 coverage (including recipe correctness) requires JEI/EMI runtime validation -- see `mod-description-trust` module for the complete AP1 analysis.

**Source:** FTB Evolution #6447; FTB Architect's Exodus #12549, #12571, #12458; Create: Astral #613, #618.

---

## Rules

### R1 -- Dimension-Reachability Check

**Step 4 priority:** P1 (L1 only -- 内置映射检查, `[unverified:dimension]`)
**Step 5 priority:** P2 (完整 L1+L2 检查)
**数据依赖:** L1 (shared-builtin-tables) / L2 / L3

**检查什么：** 每个 `ftbquests:item` task 引用的物品，是否来自一个当前 quest 依赖链已经解锁的维度。


```
for each quest Q:
    reachable_dims = union of dims unlocked by Q's ancestor chain
        (Overworld always reachable)
    for each item_task in Q.tasks:
        item_dim = (L2 or BUILTIN_DIMENSION_MAP).get(item_task.item.id)
        if item_dim and item_dim not in reachable_dims:
            ERROR: "requires {item} from unlocked {item_dim}"
        elif item_dim is None:
            INFO: "[unverified:dimension] {item}"
```

「维度解锁」判定：(1) 祖先 quest 链中存在 `type: "ftbquests:dimension"` task 指向该维度；(2) 包的 gamestage 配置中祖先链包含对应 stage。

Kitchen-sink 包（`progression_mode: "flexible"`）降级为 warning；expert/linear 包为 error。

**违反了会怎样：** 玩家在无法进入的维度中寻找任务物品，完全卡住或被迫跳出 quest book 自行探索，可信度下降。

**来源：** ATM-10 AllTheModium tier spine；FTB Evolution #6447 "heart of the sea requires red chalk"。

### R2 -- Tool-Tier Item Reachability

**Step 4 priority:** P2 (L1 only -- 内置映射检查, `[unverified:tool_tier]`)
**Step 5 priority:** P2 (完整 L1+L2 检查)
**数据依赖:** L1 (shared-builtin-tables) / L2 / L3

**检查什么：** 任务要求的物品是否需要特定工具等级才能采集或加工，而该工具在 quest 的祖先链中尚未获得。


```
for each quest Q:
    available_tools = collect tool/machine rewards from ancestors
    for each item_task in Q.tasks:
        required_mining = (L2 or BUILTIN_ORE_REQUIREMENTS).get(item_task.item.id)
        if required_mining:
            available_mining = max(mining_level(t) for t in available_tools) or 0
            if required_mining > available_mining:
                WARNING: "mining level {required_mining} > available {available_mining}"
        elif no data: INFO: "[unverified:tool_tier]"
```

**违反了会怎样：** 玩家看到任务物品但无论怎么尝试都无法获取 -- 挖掘它的镐还没解锁，加工它的机器还造不出来。Expert pack 中最常见的「卡关」原因。

**来源：** GTNH README；ATM-10 AllTheModium；cesspit.net。

### R3 -- Recipe-Chain Depth vs Dependency-Depth

**Step 4 priority:** P2 (L1 heuristic -- `[unverified:recipe_depth]`)
**Step 5 priority:** P2 (完整 L1+L2 检查)
**数据依赖:** L1 (shared-builtin-tables) / L2

**检查什么：** 任务物品的合成链深度是否超过了 quest 在依赖图中的深度。


```
for each quest Q:
    quest_depth = dependency_depth(Q)
    for each item_task in Q.tasks:
        recipe_depth = L2_recipe_depth.get(id) or estimate_recipe_depth_heuristic(id)
        if recipe_depth >= 0 and recipe_depth > quest_depth + ALLOWANCE:
            WARNING: "depth {quest_depth} but recipe depth {recipe_depth}"
        elif recipe_depth < 0: INFO: "[unverified:recipe_depth]"
```

`ALLOWANCE` 默认为 2。核心假设：**quest 依赖链应该至少和物品合成链一样长** -- 每经过一个合成步骤，应该有一个对应的 quest 教玩家如何完成。

Expert 包建议用户在 Step 2 提供关键物品的精确深度（heuristic 误差 +/-2 级）。

**违反了会怎样：** 玩家面对需要 5 步合成的物品，但 quest chain 只有 2 步深度 -- 中间 3 步没有任何 quest 教过。

**来源：** MP24；cesspit.net；Monifactory。

### R4 -- Pack-Type Stage Boundary

**Step 4 priority:** P2 (降级版 -- ancestor reward 向后检查, `[unverified:stage]`)
**Step 5 priority:** P2 (完整 L1+L2 检查)
**数据依赖:** L2 (user stage_definition) / 无 L2 时降级为跨 chapter 引用交叉检查

**检查什么：** 根据包类型，每个 quest 应该处于正确的阶段区间。

- **Kitchen-sink：** 阶段由 chapter group 定义。Capstone 物品不应出现在早期 chapter。
- **Expert：** 阶段由 voltage tier 或 GregTech age 定义。高 tier 物品不应出现在低 tier chapter。
- **Skyblock：** 阶段由资源获取方式定义。需要自动化的物品不应出现在手动阶段。
- **RPG：** 阶段由维度或 story arc 定义。

```
for each quest Q:
    quest_stage = determine_stage(Q.chapter, pack_type)
    for each item_task in Q.tasks:
        item_stage = (L2_stage_map or {}).get(item_task.item.id)
        if item_stage and item_stage > quest_stage:
            ERROR: "stage {quest_stage} but item from stage {item_stage}"
        elif item_stage is None:
            # Fallback: cross-chapter check
            if item only appears in later chapters:
                INFO: "[unverified:stage] possible boundary violation"
```

**违反了会怎样：** 阶段系统失去意义 -- 玩家在「石器时代」chapter 中需要「电力时代」的物品。对 expert pack 尤其致命。

**来源：** SevTech: Ages；E2E Extended；Monifactory。

### R16 -- Dimension-Explore-Then-Craft Ordering

**Step 4 priority:** P1 (向后 ancestor dim task 检查, WARNING)
**Step 5 priority:** P1 (全量检查)
**数据依赖:** L1 (shared-builtin-tables) / L2

**检查什么：** 需要先到达某个维度的 quest，其 dimension task 是否在 item task 之前。


```
for each quest Q:
    for each item_task in Q.tasks:
        item_dim = item_dimension_map.get(item_task.item.id)
        if item_dim and item_dim != "minecraft:overworld":
            if no ancestor has dimension task for item_dim:
                WARNING: "requires {item} from {item_dim} but no ancestor has dim task"
```

Mode B（chain 顺序）：dimension quest 应该在 item quest 之前。如果 item_quest depth < dim_quest depth，WARNING。

**违反了会怎样：** MP13 的反面 -- 玩家被要求合成来自 Nether 的物品，但 quest chain 中没有先去 Nether 的步骤。

**来源：** MP13；MP5；MP21。

### R24 -- Suggestion-Reachability Check

**Step 4 priority:** P2 (L1 only -- 正则 + L1, `[unverified:suggestion]`)
**Step 5 priority:** P3 (完整 L1+L2 检查)
**数据依赖:** L1 (shared-builtin-tables) / L2

**检查什么：** 当 quest 的 `description` 使用「建议使用」「推荐使用」等引导性措辞提到一个物品时，该物品是否在 quest 的祖先链中已经可获得。


```
SUGGESTION_PATTERNS = [r'suggest(?:ed|ion)?\s+use', r'recommend(?:ed)?\s+use',
    r'you\s+(?:can|could|may)\s+use', r'try\s+using',
    r'best\s+(?:tool|weapon|gear)\s+(?:for|is)', r'建议使用', r'推荐使用', r'可以用']

for each quest Q:
    suggested_ids = extract_ids_near_suggestion_patterns(desc_text)
    reachable_items = collect_all_reward_and_task_items(ancestors)
    for sid in suggested_ids:
        if sid not in reachable_items:
            item_dim = BUILTIN_DIMENSION_MAP.get(sid)
            if item_dim and item_dim not in reachable_dimensions(Q):
                WARNING: "suggests {sid} from unlocked {item_dim}"
            else:
                INFO: "[unverified:suggestion] {sid}"
```

Kitchen-sink 包保持 INFO 级别；expert/linear 包升级为 WARNING。

**违反了会怎样：** 描述引导玩家走死路。比 R1 更隐蔽 -- task 不可达会被系统拒绝，「建议」不可达只浪费时间。

**来源：** FTB Architect's Exodus #12601 (Malum runes)；#12549 (Botania Spark Augment)。

---

## Cross-References

| 目标模块 | 关系 |
|---|---|
| shared-builtin-tables | R1/R2/R3/R24 的 L1 数据源 |
| mod-dependency-graph | R5/R6 提供依赖图结构检查（物品可达性的前置条件） |
| mod-description-trust | AP1 完整版（本模块仅含 item-identity 变体） |
| mod-reward-bridging | R10/R11 检查 reward 是否正确桥接（与 PP7 的 wrong-tool 变体交叉） |
