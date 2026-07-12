# Mod Dependency Graph

> **Core question:** 任务怎么连接的，图结构健康吗？
> **Lines:** ~303 | **Step 4 load:** yes | **Step 5 load:** full

## Quick Reference

| ID | 标题 | Phase | 严重度 | 包类型 |
|---|---|---|---|---|
| MP6 | Linear Chain | Step 2 | -- | all |
| MP7 | Fan-Out | Step 2 | -- | all |
| MP8 | Fan-In / Convergence | Step 2 | -- | all |
| MP9 | Diamond (pick-and-rejoin) | Step 2 | -- | expert, story |
| MP10 | Independent Island | Step 2 | -- | kitchen-sink, create |
| MP32 | min_tasks Modifier | Step 4 | -- | create, kitchen-sink |
| AP2 | Circular Dependency Deadlock | Step 5 | ERROR | all |
| AP3 | Unfinishable Chapter | Step 5 | ERROR | all |
| AP4 | Wrong Gating | Step 4/5 | ERROR | all |
| AP19 | Optional-but-Mandatory Mislabel | Step 4/5 | ERROR | all |
| AP20 | Quest Tab Overwhelm | Step 2 | WARNING | kitchen-sink, create |
| R5 | Circular Dependency Detection | S4/S5 | ERROR | all |
| R6 | Unreachable Quest Detection | S4/S5 | ERROR | all |
| R7 | Optional-Gate-Mandatory | S4/S5 | ERROR | all |
| R8 | Dependency Requirement Consistency | S5 | INFO | all |
| R9 | Dependency Depth Reasonableness | S5 | WARNING | all |
| R20 | Chapter Completion Testability | S5 | ERROR | all |
| R22 | Cross-Chapter Dependency Validity | S4 | ERROR | all |
| R35 | Shape Semantics Consistency | S5 | P3 (INFO) | all |
| R36 | Dependency Root Isolation | S5 | P2 (WARNING) | all |
| R39 | Guide Quest Deduplication | S5 | P3 (INFO) | expert, kitchen-sink |
| R43 | Stage-Quest Causal Chain Acyclic | S4/S5 | ERROR | expert, story |
| R48 | Quest Port Drift Adaptation Checklist | S4/S5 | P1 (WARNING/ERROR) | all |
| PP3 | Invisible Wall | Step 2 | WARNING | all |
| PP4 | Completionist's Dilemma | Step 2 | ERROR | all |

---

## Patterns

### MP6 -- Linear Chain (the tutorial spine)

**Applicable when:** teaching a strictly sequential process. Skyblock tutorials, mod progression ladders, narrative arcs.

**Implementation:** A has no deps (root). B `depends_on: [A]`. C `depends_on: [B]`. Each quest has exactly one dependency (except root). Laid out horizontally.

Strongest topology for forced progression. In `linear` mode, each quest locks until previous completes. In `flexible`, chain is a suggestion.

**Real case (ATM9-Sky, getting_started_2):** Depth **18** -- deepest of any chapter. Inherently sequential: sieve -> hammer -> crook -> ore processing -> first ingot -> first tool.

**Quantified:** Dominates expert packs (Monifactory: depth 8-15) and skyblock tutorials (ATM9-Sky: 18). Kitchen-sinks use chains of 4-6 before fan-out at tier boundaries.

---

### MP7 -- Fan-Out (the hub-and-spoke)

**Applicable when:** single prerequisite unlocks multiple independent paths.

**Implementation:** Hub H fans out to A, B, C, D which `depend_on: [H]`. H visually distinct. Siblings independent.

> **Note:** `hide_dependency_lines` is ATM-series preference. See `mod-atm-signature`.

**Real case (ATM-10, Ars Nouveau):** 130 quests, tier-gates fan out 15-30. Typical: 3-8 per hub.

**Real case (NFwC boss chapter, Phase 3 Cycle 5):** 58 quests with 38 kill tasks (65% kill density — highest observed). Single root quest fans out to 21+ independent boss kill quests, all with `hide_dependency_lines: true` (42/58 quests). ZERO optional quests. The boss chapter is a flat catalog of independent boss fights — each kill quest is independent (no inter-boss dependencies). Custom `kubejs:textures/task/collection_*.png` images serve as visual tier separators (collection_1, collection_2). Lightmanscurrency coin rewards (42 references) incentivize boss grinding. This is the purest fan-out in the dataset: one root → many independent leaves with zero convergence.

---

### MP8 -- Fan-In / Convergence (the capstone gather)

**Applicable when:** multiple paths must all complete before synthesis quest. Capstone, multi-component crafting.

**Implementation:** A, B, C, D independent. Z `depends_on: [A, B, C, D]`. Z is chapter's largest node with synthesis reward.

> **Note:** `hide_dependent_lines` on convergence is ATM-series preference. See `mod-atm-signature`.

**Real case (ATM-10, ATM Star):** `dependencies: [10 hex IDs]`, `pentagon size: 2.0`, rewards 50 Shards + Patrick Star + 50 XP levels.

---

### MP9 -- Diamond (the pick-and-rejoin)

**Applicable when:** genuine choice between two paths, both lead to same next step.

**Implementation:** A is decision. B, C `depend_on: [A]`. D `depends_on: [B, C]` with `dependency_requirement: "one_completed"`. Diamond: A->{B,C}->D.

Kitchen-sinks rarely use (want breadth). Expert packs use at branching points.

**Real case (Monifactory):** `one_completed` for voltage-tier branching. Create: Delight: `one_started` x63, `one_completed` x44. ATM-10 defaults to `"all"`.

---

### MP10 -- Independent Island (the catalog cell)

**Applicable when:** quest stands alone, no dependencies. Catalog/collection where order doesn't matter.

**Implementation:** No `dependencies`. Always visible/completable. Default shape, small size. Grid in catalogs; `optional: true` in kitchen-sinks.

**Real case:** Create: Delight Mouse_Chef: 258/304 quests are islands. Arcana Iron Spells: 17 roots, one per magic school.

### MP32 -- min_tasks Modifier (partial completion threshold)

**Applicable when:** quest has many tasks but player only needs a subset. "Show breadth, require depth."

**Implementation:** Set `min_tasks: <N>` on quest with >N tasks. Quest completes when any N done. Related to MP9 but at task level rather than dependency level.

**Real case (Create: Astral, chapter_3):** `min_tasks: 1` with 2 tasks for alternative recipe paths.

> **Note:** MP32 functionally overlaps MP9 at task level. Can be viewed as MP9's task-level variant.

### dependency_requirement 完整选项参考 (FTB Quests 标准功能)

当 quest 有多个 `dependencies` 时，`dependency_requirement` 控制前置任务之间的逻辑关系。FTB Quests 提供四个选项：`all_completed`（默认，所有前置任务必须完成）、`all_started`（所有前置任务必须已开始）、`one_completed`（任一前置任务完成即可）、`one_started`（任一前置任务开始即可）。前两者是"与"关系，后两者是"或"关系。

另有 `min_required_dependencies` 数值字段提供精确控制。当设置为 >0 时，`dependency_requirement` 的语义被覆盖，变为"完成 N 个"关系。例如 `min_required_dependencies: 2` 要求至少完成 2 个前置任务，无论 `dependency_requirement` 设置为何值。这在需要"从 M 个并行路径中选择 N 个完成"的场景中有用——比 `all_completed` 宽松，比 `one_completed` 严格。

配套配置项还包括：`optional`（可选任务，不影响 chapter 完成度）、`hide`（隐藏任务直到前置可见）、`hide_details_until_startable`（隐藏详情直到可开始）、`tasks_ignore_dependencies`（任务忽略依赖关系，允许在解锁前提交物品）、`progression_mode`（任务推进方式：linear 锁定 / flexible 建议）和 `require_sequential_tasks`（线性任务，要求按顺序完成多任务）。

Real case: Monifactory 使用 `one_completed` 实现电压等级分支。Create: Delight 使用 `one_started` x63 和 `one_completed` x44 构建分支系统。ATM-10 默认使用 `all_completed` 维持线性进度。

[Phase 2 Cycle 8 - FTB Quests zh_cn 翻译 PR https://github.com/FTBTeam/FTB-Mods-Issues/issues/1296]

---

## Anti-Patterns

### AP2 -- Circular Dependency Deadlock (Catch-22)

**Symptom:** Needs A to get B, needs B to get A. Neither obtainable.

**Root cause:** Two mods' chains interlock in a cycle. Can be explicit (`dependencies` cycle) or implicit (recipe-graph cycle not visible in dependencies).

**Fix:** Break cycle via quest reward, loot table, or alternative recipe.

**Real case (FTB Evolution #6447):** red chalk -> torch flowers -> heart of the sea -> red chalk. Cross-mod deadlock.
**Within-mod (FTB Skies 2 #9084):** Productive Bees: need gene to craft egg, need bee to get gene. Harder to detect.

### AP3 -- Unfinishable Chapter

**Symptom:** All visible quests done, but chapter completion <100%.

**Root cause:** Quest is `always_invisible`/`secret` without trigger, gated behind unreachable condition, or references nonexistent item.

**Fix:** (1) Validate completability. (2) Secret quests need discoverable triggers. (3) Placeholder: `optional: true`. (4) Test 100% on non-optional quests.

**Real case (FTB Evolution #6447):** "It isn't possible to complete the 'Getting Started' chapter."

### AP4 -- Wrong Gating (Over-Restrictive Dependencies)

**Symptom:** Requires ALL when should require ONE. Gated behind optional. Mandatory when should be optional.

**Root cause:** `dependency_requirement: "all"` when should be `"one_completed"`. Or `dependencies` includes optional quests.

**Fix:** (1) Branch alternatives: `"one_completed"`. (2) Never gate mandatory behind optional. (3) Audit: sequential = `"all"`, parallel = `"one_completed"`.

**Real case (FTB Evolution #6447):** "early energy generation requires all three generators." "mandatory boss catcher gated behind optional Hephaestus Tier 4."
**Cycle 3:** Craftoria #231 Powah over-restrictive. Craftoria #352 optional-but-mandatory.

## Rules

### R5 -- Circular Dependency Detection

**Step 4 priority:** P1 (增量版 -- 新节点 DFS, ERROR)
**Step 5 priority:** P0 (完整 DFS 全图遍历, ERROR)
**数据依赖:** 无需外部数据（纯图结构）

**检查什么：** quest 依赖图中是否存在循环。

```
function detect_cycles(all_quests):
    # Standard DFS + 3-color marking (WHITE/GRAY/BLACK)
    # GRAY node encountered during DFS = cycle found
    # Extract cycle from path[path.index(dep_id):]
    # Must span entire book (cross-chapter refs included)
    return cycles
```

需区分**显式环**（`dependencies` 中直接可见, ERROR）和**隐式环**（recipe graph 产生, WARNING, 需外部脚本）。

**违反了会怎样：** Catch-22 -- 最严重的进度问题之一。
**来源：** AP2；FTB Evolution #6447 red chalk 案例。

### R6 -- Unreachable Quest Detection

**Step 4 priority:** P1 (局部版 -- dependency 存在性, WARNING)
**Step 5 priority:** P0 (完整可达性, ERROR)
**数据依赖:** 无需外部数据

**检查什么：** 是否存在永远无法解锁的 quest。

```
for each quest Q:
    if no deps: continue  # root -- reachable
    if not any(path_feasible for path in find_all_paths(Q)):
        ERROR: "unreachable -- all paths blocked"
```

特殊：mandatory 唯一前置是 `optional` = ERROR。前置是 `secret` 且无发现触发 = ERROR。

**违反了会怎样：** Chapter 完成度 <100%（AP3），或 mandatory quest 永不解锁（AP4）。
**来源：** AP3；FTB Evolution #6447；PP4。

### R7 -- Optional-Gate-Mandatory Check

**Step 4 priority:** P0 (ERROR -- 阻止写入 spec)
**Step 5 priority:** P1 (全局复查)
**数据依赖:** 无需外部数据

**检查什么：** mandatory quest 是否依赖 optional quest。

```
for each quest Q:
    if Q.optional: continue
    for dep in Q.dependencies:
        if get_quest(dep).optional:
            if requirement == "all": ERROR
            elif no non-optional deps exist: ERROR
```

**违反了会怎样：** 跳过 optional 的玩家被 mandatory 卡住。
**来源：** AP4；FTB Evolution "mandatory boss catcher gated behind optional Tier 4"。

### R8 -- Dependency Requirement Consistency

**Step 4 priority:** -- (不在 Step 4 执行)
**Step 5 priority:** P2 (LCA 分析)
**数据依赖:** 无需外部数据

**检查什么：** `dependency_requirement` 是否与依赖语义匹配。

```
for each quest Q:
    if len(deps) <= 1: continue
    if deps at similar depth and share common parent:
        if requirement == "all": INFO: "siblings require ALL, consider one_completed"
    if requirement in ("one_completed", "one_started") and len(deps) == 1:
        WARNING: "redundant one_completed with single dep"
```

**违反了会怎样：** AP4 温和版 -- 被要求完成所有并行选项而非选择一个。
**来源：** AP4；FTB Evolution "requires all three generators"；MP9。

### R9 -- Dependency Depth Reasonableness

**Step 4 priority:** -- (不在 Step 4 执行)
**Step 5 priority:** P2 (chapter-level 统计)
**数据依赖:** 无需外部数据

```
MAX_DEPTH = {"kitchen-sink": 8, "expert": 20, "skyblock": 20, "rpg": 12, "create": 10}
for each chapter C:
    if max_depth > MAX_DEPTH[pack_type]:
        WARNING: "depth exceeds {pack_type} guideline"
```

**违反了会怎样：** 过深 chain = 缺乏选择和喘息。Expert 可接受，kitchen-sink 是设计失误。

> **Book-level effective depth (审查 B 补充):** R9 目前只检查单 chapter 内的 dependency depth。跨 chapter 的依赖链——例如 chapter A 末尾 quest 依赖 chapter B 的 quest，后者又依赖 chapter C 的 quest——对玩家来说实际深度是各 chapter depth 之和。一条跨 3 个 chapter、每 chapter depth 5 的链，玩家体感为 depth 15。Step 5 的完整验证应额外计算 book-level effective depth：沿 `depends_on` 跨 chapter 引用累加深度，超过 `MAX_DEPTH[pack_type] * 1.5` 时 WARNING。这个扩展检查需要跨 chapter 数据，目前作为 R9 的增强方向记录，未纳入基础实现。

**来源：** Cross-pack comparison；design guide。

### R20 -- Chapter Completion Testability

**Step 4 priority:** -- (不在 Step 4 执行)
**Step 5 priority:** P0 (ERROR)
**数据依赖:** 无需外部数据

**检查什么：** 每个 chapter 的 non-optional quest 是否可全部完成。

```
for each chapter C:
    required = non-optional, non-invisible quests
    iteratively add to completable set where all deps satisfied
    if incomplete: ERROR: "can't be completed"
```

Starter chapter（`order_index == 0`）升级为优先修复。
**违反了会怎样：** PP4 -- 完成所有可见 quest 后 <100%。
**来源：** AP3；PP4；FTB Evolution #6447。

### R22 -- Cross-Chapter Dependency Validity

**Step 4 priority:** P0 (ERROR -- 阻止写入 spec)
**Step 5 priority:** -- (已在 Step 4 逐节点处理)
**数据依赖:** 无需外部数据

**检查什么：** 跨 chapter 的 dependency 引用是否指向存在的 quest。

```
for each quest Q:
    for dep_ref in Q.dependencies:
        if is_cross_chapter_ref(dep_ref):
            target = resolve_ref(dep_ref)
            if target is None: ERROR: "depends on nonexistent {dep_ref}"
            elif target.chapter > Q.chapter:
                WARNING: "backward dependency to later chapter"
```

**违反了会怎样：** 前面 chapter 要求后面 chapter 的内容，与 chapter ordering 语义矛盾。
**来源：** validator `E_DEP_MISSING`；SKILL.md Task linkage。

**Visual line variant (ATM-10 #4192):** "Chapter 3 quest missing a connecting line" — the dependency data exists in config but the visual line between "infinity range booster" and "nexium emitter" doesn't render. This is a rendering-layer issue rather than a data integrity issue, but from the player's perspective it creates the same confusion as a missing dependency: no visual cue that the quests are connected. R22 can verify the data layer; the visual layer requires in-game testing.

---

### PP3 -- The Invisible Wall

**Pattern:** Players tolerate gating but not gating without feedback. A locked quest with visible deps says "go do these first." With `hide_dependency_lines: true` AND no visible path = invisible wall.

**Config implication:** For every `hide_until_deps_visible: true` quest, ensure: (a) dependency is visible and mentions unlock, (b) signpost quest nearby, (c) discovery trigger is naturally encountered. Never combine `hide_until_deps_visible` with `hide_dependency_lines` on same quest.
**Source:** FTB Evolution #6447 "permanently hidden quest."

### PP4 -- The Completionist's Dilemma

**Pattern:** Chapter completion counts ALL quests including `secret`/`always_invisible`. If any is unfinishable, chapter never hits 100%. Especially damaging in first chapter.

**Config implication:** (1) `optional: true` for placeholders. (2) Test 100% completability. (3) Secret triggers must be naturally encountered. (4) Starter chapter MUST be 100% completable.
**Source:** FTB Evolution #6447 "Getting Started chapter not completable."

---

### R36 -- Dependency Root Isolation

**Step 5 priority:** P2 (WARNING)
**Data dependency:** None (pure graph structure)

**What it checks:** Every quest must have at least one dependency unless it is in a designated root/hub chapter. A rootless quest in a standard progression chapter is an unpredictable orphan -- visible but with no narrative or progression entry point.

```
ROOT_CHAPTERS = user-provided or ["dependencies", "getting_started", "welcome"]

for each quest Q:
    if not Q.dependencies:
        if Q.chapter.name not in ROOT_CHAPTERS:
            WARNING: "Quest {Q.name} has no dependencies but is not in a
                      designated root chapter."
```

**Source:** Monifactory CONTRIBUTING.md -- "All quests should have at least one dependency except the quests in the 'dependencies' chapter."
**Validated:** Monifactory (strict compliance), ATM-10 (roots in chapter group openers).

### R39 -- Guide Quest Deduplication

**Step 5 priority:** P3 (INFO)
**Data dependency:** Cross-chapter quest content analysis

**What it checks:** A guide/help quest (explains a mechanic without requiring progression items) should appear in at most one chapter. Multiple references from different chapters should use quest links, not duplication.

```
guide_quests = [q for q if is_guide_quest(q)]
for each guide_quest in guide_quests:
    referenced_chapters = chapters that reference this guide
    if len(referenced_chapters) > 1:
        INFO: "Guide quest referenced from {len} chapters.
               Consider quest links from a single canonical location."
```

**Source:** Monifactory CONTRIBUTING.md -- "No quest should be needed in more than one 'Guides and Help' chapter."
**Validated:** Monifactory (centralized in `tutorials` chapter), ATM-10 (mod-specific explanations mitigate duplication).

### R43 -- Stage-Quest Causal Chain Acyclic (Stage-Quest 因果链无环)

**Step 4 priority:** P2 (增量版 -- 新增节点时检查)
**Step 5 priority:** P1 (完整 Stage-Quest 交叉图遍历, ERROR)
**数据依赖:** L2 (用户提供的 Stage 定义和 Quest-Stage 映射)

**检查什么：** FTB Quest 完成 → Game Stage 激活 → 配方/物品解锁 的因果链必须是无环有向图。R5 检测 quest 依赖层面的循环（A quest depends on B quest depends on A），R43 检测 Stage-Quest 交叉层面的循环：任务 T 的完成通过 command reward 激活 Stage A，Stage A 解锁的物品 X 又是任务 T 的前置依赖链中的需求。这种交叉环在纯 quest 依赖图中不可见，只有将 Stage 作为节点纳入依赖图后才能发现。[Phase 3 Cycle 8 - wenku.csdn.net/doc/6amfp2j2im]

```
# Build extended dependency graph including Stage nodes
extended_graph = new DirectedGraph()

# Add quest nodes and their dependencies
for each quest Q:
    extended_graph.add_node(Q.id, type="quest")
    for dep in Q.dependencies:
        extended_graph.add_edge(dep, Q.id)

# Add stage nodes and quest->stage activation edges
for each quest Q:
    for cmd_reward in Q.command_rewards:
        if cmd_reward.activates_stage(stage_name):
            extended_graph.add_node(stage_name, type="stage")
            extended_graph.add_edge(Q.id, stage_name)

# Add stage->quest unlock edges (stage gates quest availability)
for each quest Q:
    required_stage = Q.required_stage or Q.chapter.required_stage
    if required_stage:
        extended_graph.add_edge(required_stage, Q.id)

# Cycle detection on extended graph
cycles = detect_cycles(extended_graph)
if cycles:
    for cycle in cycles:
        ERROR: "Stage-Quest circular dependency: {cycle.path}"
```

**Optional quest 循环严重度分级 [Phase 4 Cycle 8 - 审查员B]：** R43 的循环检测应区分 mandatory 和 optional quest。如果循环路径上的所有 quest 均为 optional，降级为 WARNING——可选任务的自环不影响主线进度，跳过该 optional quest 的玩家不受影响。如果循环路径上存在 mandatory quest，保持 ERROR——主线死锁，玩家无法绕过。这一分级与 R7（Optional-Gate-Mandatory）的精神一致：optional quest 的问题严重度天然低于 mandatory quest。

```
# Optional quest severity differentiation [Phase 4 Cycle 8 - 审查员B]
for cycle in cycles:
    cycle_quests = [node for node in cycle.path if node.type == "quest"]
    all_optional = all(get_quest(q.id).optional for q in cycle_quests)
    if all_optional:
        WARNING: "Stage-Quest circular dependency (all optional): {cycle.path}
                  — does not block main storyline"
    else:
        ERROR: "Stage-Quest circular dependency (mandatory involved): {cycle.path}"
```

**违反了会怎样：** 死锁——玩家需要 Stage A 解锁物品 X 来完成任务 T，但任务 T 完成后才激活 Stage A。这种死锁在 FTB Quests 配置层面不可见（quest 之间的 `dependencies` 没有环），只有在 Game Stages 集成后才会暴露。Expert pack 中使用 command reward + gamestage task 的组合时尤其容易出现。

**来源：** FTB Quest 与 GameStages 结合文章（wenku.csdn.net/doc/6amfp2j2im）；CrT-Game Stages 教程（mcmod.cn/post/1015.html）

### R48 — Quest Port Drift Adaptation Checklist (任务移植适配检查)

**Step 4 priority:** P1 (WARNING per unmet condition, ERROR if 3+ conditions unmet on same quest)
**Step 5 priority:** P1 (full audit across all quests)
**数据依赖:** L1 (target pack modlist), optionally L2 (source pack identity for tier comparison)

**检查什么：** 当 quest 内容从一个整合包移植到另一个包时——无论是显式的（从源包的 config 复制粘贴）还是隐式的（以模板包为起点）——必须执行五项适配检查。Quest Port Drift 是一种 meta-anti-pattern，系统性地产生 AP1（描述-现实不匹配）、AP2（依赖链错误）和 AP4（错误门控）。TFG Modern 的案例表明，即使被承认的移植债务也可能持续数年未被解决。

**五项适配条件：**
```
for each quest Q marked/heuristically detected as ported:
    # 1. 描述准确性 — 描述是否针对目标包的配方进行了验证？
    if not description_verified_against_target_pack_recipes(Q):
        WARNING: "Ported quest description not verified against target pack recipes"

    # 2. 依赖链有效性 — 依赖引用的 quest 是否存在于目标包中？
    for dep in Q.dependencies:
        if dep not in target_pack_quest_ids:
            ERROR: "Ported quest depends on {dep} which doesn't exist in target pack"
        elif get_quest(dep).chapter != Q.chapter and not cross_chapter_intentional:
            WARNING: "Ported dependency crosses chapter boundary — verify intentional"

    # 3. 物品 ID 存在性 — 任务和奖励中的物品 ID 是否在目标包的模组列表中？
    for task in Q.item_tasks:
        if task.item.id not in target_pack_item_registry:
            ERROR: "Ported task references {task.item.id} not in target pack"
    for reward in Q.item_rewards:
        if reward.item.id not in target_pack_item_registry:
            WARNING: "Ported reward references {reward.item.id} not in target pack"

    # 4. 奖励经济对齐 — 奖励是否符合目标包的奖励哲学？
    if source_pack.reward_philosophy != target_pack.reward_philosophy:
        if Q.has_rewards and target_pack.questbook_role == "companion":
            WARNING: "Ported quest has rewards but target pack uses zero-reward design"
        elif not Q.has_rewards and target_pack.questbook_role == "incentive_catalog":
            WARNING: "Ported quest has no rewards but target pack uses incentive design"

    # 5. 进度层级对齐 — 任务在源包和目标包中的层级是否一致？
    if Q.source_tier != Q.target_tier:
        WARNING: "Ported quest was tier {source} in source pack, placed at tier {target}
                  in target pack. Verify gating is appropriate."

    # 6. NBT 数据兼容性 (Phase 4 Review addition)
    for task in Q.item_tasks:
        if task.item has nbt_data:
            if not nbt_compatible_with_target_pack(task.item.nbt, target_pack):
                WARNING: "Ported task has NBT data ({nbt_keys}) that may not
                          exist in target pack's mod configuration"

    # 7. i18n 键存在性 (Phase 4 Review addition)
    if Q.title_key or Q.description_key:
        if Q.title_key not in target_pack_lang_file:
            ERROR: "Ported quest references i18n key {Q.title_key} not in target pack"
        if Q.description_key not in target_pack_lang_file:
            ERROR: "Ported quest references i18n key {Q.description_key} not in target pack"

    # 8. Gamestage 名称对齐 (Phase 4 Review addition)
    for task in Q.tasks:
        if task.type == "gamestage":
            if task.stage not in target_pack_gamestage_registry:
                ERROR: "Ported gamestage task references '{task.stage}' not in target pack"
```

**移植 quest 检测启发式方法：** FTB Quests 没有 `ported: true` 元数据。可以通过以下信号检测移植 quest：(a) 描述文本引用了目标包模组列表中不存在的模组名称；(b) 物品 ID 的 namespace 不在目标包 modlist 中；(c) 奖励结构与包的主要模式（R34 分布）显著不同；(d) 描述的语言/风格与相邻 quest 不一致（AP10 变体）；(e) i18n 键前缀与目标包惯用前缀不同（如源包用 `tfg.quests.*` 但目标包用 `craftoria.quests.*`）。

**实际案例 (TFG Modern)：** 贡献者 WaterMelwin 在 #4230 中确认 "the quests are just ported from that modpack"（可能是 GregTech Community Pack）。Lollovader 在 #3656 中确认 LV+ quests "temporarily taken from another modpack just to give players a baseline for progression"，并指出奖励文本是 "a side effect of the copying"。这导致系统性的 AP1（#457 Steam extractor 描述不匹配，#3860 建议不可获得的物品）和 AP4（#344 Create 门控变更未反映在 questbook 中）。

**来源：** TFG Modern #4230, #416, #344, #3860; Phase 3 Cycle 9

### 阶段划分的四维模型

从多个来源的交叉分析中浮现出一个阶段划分的四维框架，不是每个包都使用全部四个维度，但大多数成功的阶段系统至少在两个维度上保持一致：

**时间维度**——玩家通过积累经验、探索、击败 Boss 推进阶段节点。这是最基础的维度，对应 FTB Quests 的 `order_index` 和 `dependency_depth`。所有包都至少使用时间维度。

**空间维度**——阶段标签控制生物群系动态解锁与当前时代对应的新结构。例如 Electric Age 解锁漂浮实验室，Stone Age 只有基础村庄。这对应 R1 和 R16 检查的维度可达性，但增加了阶段条件——不是"维度是否永远可达"，而是"维度在当前阶段是否已解锁"。[Phase 3 Cycle 8 - wenku.csdn.net/doc/6amfp2j2im]

**资源维度**——矿石生成率、稀有度和深层分布受当前阶段标签主动调控。冒险包通过"修改材料的生成世界"实现这一点：强力资源只在适当维度生成。这对应 R42 检查的合成链阶段内可达性。[Phase 3 Cycle 8 - bbs.mcmod.cn/thread-21004-1-1.html]

**社会维度**——村庄升级、村民职业变换和交易刷新率随阶段同步演化。这是最少被使用的维度，但在以交易为核心的包中（如以村民经济为主线的 skyblock）成为进度骨架。

阶段划分的基本原则是：每个阶段应有明确的"解锁边界"（什么新可用、什么新区域、什么新材料），阶段数建议在 3-7 个之间，后期阶段不应引入全新的独立系统而应复用和组合早期系统。阶段之间的过渡应保证"上阶段顶级装备 = 下阶段入门挑战"——这条原则的可编码性中等，需要为每个阶段定义"顶级物品集合"和"初期挑战"并比较 DPS/效率值，目前作为人类审查项。三段式生命周期（早期钩住玩家快速推进、中期引入跨模组机制延长寿命、后期复用早期系统防止反高潮）是该模型在时间维度上的具体化。[Phase 3 Cycle 8 - mcmod.cn/post/4382.html]

### progression_mode 对阶段结构的设计影响

`progression_mode` 字段（`linear` vs `flexible`）不仅控制任务解锁方式，还深刻影响整个依赖图的拓扑结构。`linear` 模式下，任务按依赖链严格锁定，依赖图倾向于深链（depth 8-20）和少分支——Monifactory 的 `dependency_chain` chapter 深度达到 15，GT-O 的电压等级章节深度 8-15。`flexible` 模式下，所有任务默认可见可完成，依赖图倾向于宽浅结构——ATM-10 的多数章节深度不超过 8，大量 fan-out 和 independent island。

阶段划分与 `progression_mode` 的交互决定了玩家体验：Expert pack 在 `linear` 模式下使用细粒度阶段（Monifactory 的 15 个电压等级），每个阶段有明确的解锁边界；Kitchen-sink pack 在 `flexible` 模式下使用粗粒度阶段（ATM-10 的 10 个 chapter group），阶段边界是建议性的而非强制的。R9（Dependency Depth Reasonableness）的阈值设置需要考虑 `progression_mode` 的影响——`linear` 模式下 depth 15 是合理的，`flexible` 模式下同样的 depth 可能意味着过度线性化。[Phase 3 Cycle 8 - mcmod.cn/post/4382.html, wenku.csdn.net/doc/6amfp2j2im]

---

## Cross-References

| 目标模块 | 关系 |
|---|---|
| mod-item-reachability | R1/R2/R3/R4 检查物品可达性（依赖图结构是前置条件） |
| shared-builtin-tables | R1-R4 的 L1 降级数据（间接依赖） |
| mod-reward-bridging | R10/R11 检查 reward 桥接（fan-in/fan-out 的 reward 设计） |
| mod-atm-signature | MP7/MP8 的 hide_dependency_lines 设计偏好详解 |
| mod-description-trust | PP3 与 R21 Hidden Quest Signpost 的交叉 |

## Shape Semantics — Pack-Specific, Not Universal

**Phase 3 Cycle 4 finding (21-pack dataset):** Shape semantics are determined at the pack level, not by any universal standard. Each pack establishes its own shape vocabulary during initial design.

| Pack | Dominant shape | Secondary | Semantic role |
|---|---|---|---|
| ATM series (ATM-8/9/10/10-Sky) | hexagon | rsquare, circle | Tier markers, 8 types |
| MI:Foundation | diamond (32-56/ch) | gear (machines), octagon (milestones), heart (food) | 6 types |
| Craftoria (tech chapters) | none/default | hexagon in MI chapters | Minimal shape usage |
| Enigmatica 10 | all default | — | ZERO shape definitions |
| Monifactory | hexagon | — | Tier markers |
| GregTech-Odyssey | hexagon (38 in LV) | diamond (10), gear (9), octagon (6) | 6+ types, voltage-tier semantics |
| No-Flesh-Within-Chest | nearly zero | rsquare (7 in ch1 only) | Minimal — combat-focused |
| TheWinterRescue | gear (15-20/ch) | hexagon (14) | Gear=survival craft, hexagon=milestone |
| Cabricality | circle (20 in stage_3) | hexagon (3), square (3) | Circle=automation milestone |

**Config implication:** When generating quests for an existing pack, inherit the pack's established shape vocabulary from `default_quest_shape` and existing chapter patterns. When creating a new pack, define shape semantics in Step 2 interview and document them for consistency. R35 checks intra-pack shape consistency.

### R35 — Shape Semantics Consistency Within Pack

**Step 5 priority:** P3 (INFO)
**Data dependency:** Full book scan with shape statistics

**What it checks:** Validates that shape usage within a pack is internally consistent — shapes used as tier markers should be used consistently across chapters.

```
for each pack:
    shape_usage = aggregate shape counts per chapter
    dominant_shapes = shapes appearing in >50% of chapters
    
    for each chapter:
        for each shape in chapter:
            if shape not in dominant_shapes and shape count > 3:
                INFO: "Shape '{shape}' used unusually in this chapter ({count}x)
                       but rare across pack. Verify intentional."
```

**Pack-level shape patterns (from 25-pack dataset):**

| Pack | Dominant shape(s) | Secondary | Unique |
|---|---|---|---|
| ATM series (6/8/9/10/10-Sky) | hexagon | rsquare, circle | 8 types |
| MI:Foundation | diamond | gear, octagon | heart |
| Craftoria (tech chapters) | none/default | — | hexagon in MI chapters |
| Enigmatica 10 | all default | — | ZERO shape definitions |
| Monifactory | hexagon | — | — |
| GregTech-Odyssey | hexagon | diamond, gear, octagon | 6+ types, voltage-tier |
| No-Flesh-Within-Chest | nearly zero | rsquare (ch1 only) | Minimal — combat-focused |
| TheWinterRescue | gear (15-20/ch) | hexagon (14) | Gear=survival craft, hexagon=milestone |
| Cabricality | circle (20 in stage_3) | hexagon, square | Circle=automation milestone |

**Key conclusion:** Shape semantics are **pack-specific**, not universal. Diamond in MI:Foundation serves the same tier-marker role as hexagon in ATM series, but the shapes are different. There are no universal tier markers.

**All-default fallback (审查 B 补充):** Some packs (notably E10) use **zero** explicit shape definitions — every quest is the default `circle`. In this case R35's shape-consistency check has no variance to detect, and the pack has implicitly chosen "shape is not a semantic channel." When `dominant_shapes` is empty (all default), R35 falls back to a **size-based hierarchy analysis**:

```
if all shapes are default:
    size_usage = aggregate size values per chapter
    distinct_sizes = unique size values across pack
    
    if len(distinct_sizes) <= 2:
        INFO: "Pack uses no shape semantics and minimal size variation.
               Shape/size is not a semantic channel — this is valid."
    else:
        size_clusters = group quests by size
        for cluster in size_clusters:
            if cluster.count > 10 and cluster.size not in (1.0, 1.5, 2.0):
                INFO: "Unusual size {cluster.size} used {cluster.count}x —
                       may indicate an undocumented semantic role."
```

This fallback recognizes that size can serve as a lightweight hierarchy marker even when shapes carry no meaning — E10's hubs are slightly larger than leaf nodes despite using all-default shapes.

**Source:** Cross-pack comparison across 25+ packs (Cycles 4–5).
