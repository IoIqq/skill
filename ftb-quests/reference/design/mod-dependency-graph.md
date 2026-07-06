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
| R5 | Circular Dependency Detection | S4/S5 | ERROR | all |
| R6 | Unreachable Quest Detection | S4/S5 | ERROR | all |
| R7 | Optional-Gate-Mandatory | S4/S5 | ERROR | all |
| R8 | Dependency Requirement Consistency | S5 | INFO | all |
| R9 | Dependency Depth Reasonableness | S5 | WARNING | all |
| R20 | Chapter Completion Testability | S5 | ERROR | all |
| R22 | Cross-Chapter Dependency Validity | S4 | ERROR | all |
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

## Cross-References

| 目标模块 | 关系 |
|---|---|
| mod-item-reachability | R1/R2/R3/R4 检查物品可达性（依赖图结构是前置条件） |
| shared-builtin-tables | R1-R4 的 L1 降级数据（间接依赖） |
| mod-reward-bridging | R10/R11 检查 reward 桥接（fan-in/fan-out 的 reward 设计） |
| mod-atm-signature | MP7/MP8 的 hide_dependency_lines 设计偏好详解 |
| mod-description-trust | PP3 与 R21 Hidden Quest Signpost 的交叉 |
