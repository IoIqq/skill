# SKILL.md Step 4 — Reasoning Gate Upgrade (Cycle 7)

**Date:** 2026-07-08
**Base:** SKILL.md (current main, lines 376-425) + Cycle 3 draft (SKILL-step4-update-cycle3_2026-07-07.md, already integrated)
**Trigger:** Cycle 7 review findings — Reviewer C practicality audit (reasoning steps scored 5-8/10 executability), Reviewer A generality audit (L1 builtin tables cover ~25 items), Reviewer B completeness audit (11 per-node decision gaps)
**Goal:** Upgrade Step 4's item-reachability and reward-bridge reasoning from advisory prose to explicit, mandatory reasoning gates with structured pass/fail outputs. Add a third lightweight gate (dependency chain sanity) to the self-check step.

---

## Section A: Precise SKILL.md Edits (Edit-ready)

### Edit 1 — Replace "Item reachability reasoning" prose with Reasoning Gate 1

**Location:** SKILL.md Step 4, step 2 "Co-author its content" — the "Item reachability reasoning" paragraph.

**Old text (lines 388-389):**

```
   **Item reachability reasoning (before finalizing each task).** Before you commit an `ftbquests:item` task to the spec, answer this question internally: *"How does the player obtain this item at this point in the progression?"* Walk the quest's ancestor chain (the `depends_on` path back to the chapter root) and check whether the item's source dimension, tool tier, and recipe depth are all reachable from what the ancestors unlock. Use the builtin lookup tables in `reference/design/shared-builtin-tables.md` (dimension map, tool tier map, recipe depth heuristic) for common vanilla and cross-pack items; for pack-specific items, reason from the ancestor quests' rewards and the mod's known recipe ladder. If you cannot confirm reachability — the item comes from a dimension no ancestor opens, requires a tool no ancestor provides, or sits deeper in a recipe chain than the dependency depth allows — mark the task `[unverified:progression]` and surface it to the user before writing it. This is the generation-time counterpart to the Step 5 validation rules R1–R4 (`reference/design/mod-item-reachability.md`); catching the problem here avoids a round-trip through validate-and-fix.
```

**New text (replaces the above):**

```
   **Reasoning Gate 1: Task Item Reachability** — *mandatory before writing each `ftbquests:item` task to the spec.*

   For every item task, produce the following one-line reasoning **out loud** (in your working notes, not in the spec):

   > How does the player get [item_id] at this point? → [answer]

   Walk through the three checks below. Each check has a fast-path (L1 builtin table hit) and a slow-path (L1 miss → reasoning from context).

   | Check | L1 fast-path (item is in builtin table) | L1 miss (item NOT in builtin table) |
   |---|---|---|
   | **R1 Dimension** | Look up `BUILTIN_DIMENSION_MAP` (`reference/design/shared-builtin-tables.md §0`). If the item's dimension is NOT in the ancestor chain's unlocked dimensions → **GATE FAIL: P1 cross-tier**. Stop and surface to user. | Reason from the quest's ancestor rewards and the mod's context. If unsure → mark `[unverified:dimension]` and continue. |
   | **R2 Tool tier** | Look up `BUILTIN_TOOL_TIER_MAP` + `BUILTIN_ORE_REQUIREMENTS`. If the required tool/mining level exceeds what ancestors provide → **GATE FAIL: P2 cross-tier**. Stop and surface to user. | Reason from the mod's known tool progression. If unsure → mark `[unverified:tool_tier]` and continue. |
   | **R3 Recipe depth** | Run `estimate_recipe_depth_heuristic` on the item id. If estimated depth > quest dependency depth + 2 → **GATE FAIL: P2 depth mismatch**. Mark `[unverified:recipe_depth]` and surface. | Use **name-tier heuristic** as fallback: items containing `ingot`/`dust`/`gear`/`nugget` ≈ depth 1–2; `machine`/`circuit`/`processor`/`controller` ≈ depth 3–4; `multiblock`/`fusion`/`singularity` ≈ depth 5+. Mark `[unverified:recipe_depth]`. |

   **Gate verdict:**
   - **PASS** (all checks pass or are deferred `[unverified]`) → write the task to the spec.
   - **FAIL** (any L1 hit returns P1/P2 violation) → do NOT write the task. Instead: (a) suggest an alternative item the player CAN reach, (b) suggest adjusting the dependency chain to unlock the required dimension/tool, or (c) ask the user to confirm they want this item here despite the gap. Only proceed with explicit user approval, and note the override in the spec comment: `// Gate 1 override: user confirmed [item] despite [reason]`.

   **Batch fast-path:** for collection quests with many item tasks, run Gate 1 once per batch. Resolve all item ids via `lookup_item.py` first, then run the three checks on each. Items that are vanilla or well-known (in the L1 tables) auto-pass; only flag items that fail or miss. Don't produce individual reasoning lines for items that trivially pass (e.g., `minecraft:oak_log` in the first quest).

   **Scope note:** Gate 1 applies only to `ftbquests:item` tasks. Non-item tasks (`checkmark`, `stat`, `advancement`, `dimension`, `biome`, `kill`, `structure`, `observation`, `xp`, `custom`) are exempt from item reachability — they have no item to check. For `ftbquests:fluid` tasks, apply the same gate logic substituting the fluid's source mod and production method for "dimension/tool/recipe depth".
```

---

### Edit 2 — Replace "Reward bridge reasoning" prose with Reasoning Gate 2

**Location:** SKILL.md Step 4, step 2 "Co-author its content" — the "Reward bridge reasoning" paragraph.

**Old text (lines 390-391):**

```
   **Reward bridge reasoning (after drafting each reward).** Once you have a reward drafted, answer: *"What does this reward lead the player to do next?"* A well-bridged reward appears as a task item in a dependent quest (the material bridge pattern, `reference/design/mod-reward-design.md §MP14`), or is a universal bridge type (tool reward `§MP15`, XP drip `§MP16`). If the reward is an item that no downstream quest requires and it isn't a recognized universal bridge, it's a dead-end reward (`reference/design/mod-reward-design.md §AP6`) — redesign it so the player has a clear next step. For terminal quests (capstone, chapter leaf) this check doesn't apply. The formal rule is R10–R13 in `reference/design/mod-reward-design.md`; at generation time you're doing the same reasoning by hand, one reward at a time.
```

**New text (replaces the above):**

```
   **Reasoning Gate 2: Reward Bridge** — *mandatory before writing each reward to the spec.*

   For every reward, produce the following one-line reasoning **out loud** (in your working notes, not in the spec):

   > This reward leads the player to: [answer]

   Then classify the reward into one of four categories:

   | Category | Condition | Gate verdict |
   |---|---|---|
   | **Material bridge (MP14)** | The reward item appears as a task item in at least one dependent quest in the outline, OR in a quest that will be generated later in this chapter. | **PASS** — strongest forward pull. Write to spec. |
   | **Universal bridge** | The reward is a recognized universal bridge type: tool reward (MP15 — pickaxe, wrench, guide book, machine block), XP drip (MP16 — only for kitchen-sink/ATM-style generous packs), or currency from a known currency mod (`lightmanscurrency`, `gtocore` coins). | **PASS** — write to spec. |
   | **Terminal reward** | This quest is a capstone, chapter leaf, or otherwise has no dependent quests in the outline. The reward is the endpoint, not a bridge. | **PASS** — write to spec. Mark explicitly: `// Gate 2: terminal reward (no dependents)`. |
   | **Dead-end risk (AP6)** | The reward is a material item, no dependent quest requires it as a task, and it isn't a universal bridge type or terminal. | **GATE FAIL** — do NOT write to spec. Instead: (a) redesign the reward as a material bridge to a downstream quest, (b) add a dependent quest that uses this item, or (c) if the user insists on keeping it, mark `[unverified:reward_bridge]` and note the override: `// Gate 2 override: user accepted dead-end reward`. |

   **Backward matching (Step 4 practical note):** because Step 4 generates in dependency order (root → leaves), you often can't do a forward check (reward → dependent task) since dependent quests may not exist yet. Use **backward matching** instead: when generating quest B, check whether B's task items match any ancestor quest's rewards. The formal forward check runs in Step 5 (R10).

   **R28 Command reward safety (sub-gate):** if the reward type is `command`, this gate additionally requires passing the R28 Command Reward Safety Scan before writing — check against `FORBIDDEN_COMMANDS` (ERROR — block write), `HIGH_RISK_COMMANDS` (WARNING — surface to user), and `IDEMPOTENCY_RISK` (INFO — note). See `reference/design/mod-reward-design.md §R28`. Command rewards are the highest-risk reward type (AP15) — prefer `item`, `xp`, `loot` whenever possible.

   **R31 XP-level pre-check (sub-gate):** if the reward type is `xp_levels`, check whether this quest is a milestone/capstone (high fan-in, distinctive shape). Non-milestone `xp_levels` rewards drift in value with player level (AP17). If not a milestone, suggest flat `xp` instead or surface the risk to the user.

   **Batch fast-path:** when batching a chapter, run Gate 2 once per reward as you write the spec. The dead-end detection (AP6) is most effective after the full chapter's tasks are written — do a quick chapter-level dead-end sweep after the batch (alongside the teaching order check).
```

---

### Edit 3 — Add Reasoning Gate 3 to Step 6 (AI self-check)

**Location:** SKILL.md Step 4, step 6 "AI generation self-check (per node)" — append after the existing bullet points.

**Old text (end of step 6, line ~406):**

```
   - **Narrative continuity (AP11).** If this quest's description makes a forward reference ("you'll need this for the next quest") or a difficulty claim ("the hardest craft so far"), verify the referenced quest actually exists and matches. Check that the tone (casual / technical / lore-heavy) is consistent with the chapter's established voice — a tonal lurch between adjacent quests breaks the player's trust in the book as a guide.
```

**New text (append after the above bullet, before step 7):**

```
   - **Narrative continuity (AP11).** If this quest's description makes a forward reference ("you'll need this for the next quest") or a difficulty claim ("the hardest craft so far"), verify the referenced quest actually exists and matches. Check that the tone (casual / technical / lore-heavy) is consistent with the chapter's established voice — a tonal lurch between adjacent quests breaks the player's trust in the book as a guide.

   **Reasoning Gate 3: Dependency Chain Sanity** — *lightweight scan after the per-node anti-pattern checks pass.*

   Before presenting the summary (step 7), quickly scan this quest's local dependency context:

   | Check | Condition | Action |
   |---|---|---|
   | **Chain depth** | Count the longest `depends_on` path from this quest back to a chapter root. If depth exceeds the pack-type threshold (`kitchen-sink: 8`, `expert: 20`, `skyblock: 20`, `rpg: 12`, `create: 10` — from R9) or, more practically, exceeds the depth of neighboring quests by 3+ | **WARN** — note in summary: "Chain depth N exceeds threshold / neighbors by M. Consider a shortcut dependency or restructure." |
   | **Fan-out** | Count this quest's direct dependents. If > 5 (hub pattern) | **INFO** — note: "Hub with N dependents. Consider `hide_dependency_lines` (kitchen-sink) or `hide_until_deps_visible` (narrative) to reduce visual clutter." |
   | **Orphan risk** | This quest has no dependents AND no `optional: true` AND is not the last quest in the chapter | **WARN** — note: "Dead-end quest with no dependents and not marked optional. Either add a dependent, mark as optional, or verify it's intentionally a leaf." |
   | **Diamond rejoin** | This quest depends on multiple quests that themselves share a common ancestor (rejoin after fan-out) | **INFO** — note: "Diamond pattern detected. Verify `dependency_requirement` is correct (`all` = must do all branches, `one` = any branch suffices)." |

   Gate 3 is **advisory, not blocking** — it surfaces structural observations in the step 7 summary for the user to decide. Unlike Gates 1 and 2, it does not prevent writing to the spec. The formal versions of these checks (R5, R6, R7, R9) run in Step 5 with the full graph available.
```

---

### Edit 4 — Update batching paragraph to reference gates

**Location:** SKILL.md Step 4, "Batching by chapter" paragraph.

**Old text (line ~411):**

```
**Batching by chapter:** fill all of a chapter's quests' `tasks`/`rewards` in `quests.spec.json5`, then run `generate_quests.py` once + `validate_quests.py` once; use `generate_quests.py --dry-run` to preview the batch before committing. Run `quest_detail.py` per node only for quests that fail validation or that you want to spot-check. When batching, the item reachability and reward bridge reasoning (step 2) apply to each quest as you write it into the spec; the AI self-check (step 6) and the chapter-level teaching order check run once after the whole batch is written.
```

**New text (replaces the above):**

```
**Batching by chapter:** fill all of a chapter's quests' `tasks`/`rewards` in `quests.spec.json5`, then run `generate_quests.py` once + `validate_quests.py` once; use `generate_quests.py --dry-run` to preview the batch before committing. Run `quest_detail.py` per node only for quests that fail validation or that you want to spot-check. When batching:
- **Gate 1 (Item Reachability)** and **Gate 2 (Reward Bridge)** apply per-quest as you write it into the spec — produce the one-line reasoning for each task item and each reward. Use the batch fast-path: items that are vanilla or in L1 tables auto-pass; only produce explicit reasoning lines for items that fail or miss.
- **Gate 3 (Dependency Chain Sanity)** and the **chapter-level teaching order check** run once after the whole batch is written — scan the entire chapter's dependency graph at that point.
- The AI self-check (step 6) runs per-node during the batch, but AP10 (style drift) and AP18 (reward desert) are most effective as a chapter-level sweep after the batch.
```

---

### Edit 5 — Update "Generation-time progression checks" paragraph (line 132) for consistency

**Location:** SKILL.md line 132, the "Generation-time progression checks" paragraph in the ABSOLUTE RULE section.

**Old text:**

```
**Generation-time progression checks.** Beyond item-ID verification, Step 4 now also reasons about item *reachability* (can the player get this at this point?), reward *bridging* (does this reward lead somewhere?), and teaching *order* (does the chapter teach before it tests?). The reasoning uses builtin lookup tables from `reference/design/shared-builtin-tables.md` and rules R1–R4 from `reference/design/mod-item-reachability.md`, R5(增量)/R6(局部)/R7 from `reference/design/mod-dependency-graph.md`, R10(反向)/R28/R31 from `reference/design/mod-reward-design.md`, R14–R17/R18 from `reference/design/mod-teaching-pacing.md`, R22/R23 from `reference/design/mod-description-trust.md`; anti-pattern context from `reference/design/mod-description-trust.md §AP9–AP11`. See `reference/design/module-index.md` for the full routing table. These are embedded in the Step 4 per-node loop, not a separate checklist — see Step 4 for details.
```

**New text (replaces the above):**

```
**Generation-time progression checks.** Beyond item-ID verification, Step 4 enforces three **mandatory reasoning gates** per node: Gate 1 (item reachability — can the player get this item at this point?), Gate 2 (reward bridge — does this reward lead somewhere?), and Gate 3 (dependency chain sanity — is this quest's local graph structure reasonable?). Each gate requires an explicit one-line reasoning output before the task/reward is written to the spec; unanswered gates block the write (Gates 1–2) or surface a warning (Gate 3). The reasoning uses builtin lookup tables from `reference/design/shared-builtin-tables.md` and rules R1–R4 from `reference/design/mod-item-reachability.md`, R5(incremental)/R6(local)/R7 from `reference/design/mod-dependency-graph.md`, R10(reverse)/R28/R31 from `reference/design/mod-reward-design.md`, R14–R17/R18 from `reference/design/mod-teaching-pacing.md`, R22/R23 from `reference/design/mod-description-trust.md`; anti-pattern context from `reference/design/mod-description-trust.md §AP9–AP11`. See `reference/design/module-index.md` for the full routing table. These gates are embedded in the Step 4 per-node loop, not a separate checklist — see Step 4 for the gate definitions and pass/fail criteria.
```

---

### Edit 6 — Minor update to ABSOLUTE RULE's `[unverified]` protocol (line 120)

**Location:** SKILL.md line 120, the `[unverified:<category>]` marking list.

**Old text:**

```
1. 标记 `[unverified:<category>]`（如 `[unverified:recipe]`、`[unverified:item_id]`、`[unverified:progression]`）
```

**New text (replaces the above):**

```
1. 标记 `[unverified:<category>]`（如 `[unverified:recipe]`、`[unverified:item_id]`、`[unverified:progression]`、`[unverified:dimension]`、`[unverified:tool_tier]`、`[unverified:recipe_depth]`、`[unverified:reward_bridge]`）
```

---

## Section B: Design Principles (设计原则)

### 为什么从散文升级为 gate

当前 SKILL.md Step 4 的 item reachability 和 reward bridge 推理以散文段落形式存在——描述 agent 应该做什么，但没有结构化的 pass/fail 判定标准。这在实践中产生两个问题：

1. **可跳过性。** 散文式指令（"answer this question internally"）允许 agent 在 context window 压力大时默默跳过推理步骤，直接写入 spec。LLM 在面对长段落时倾向于提取关键行动（"写入 task"）而忽略前置条件（"先确认可达性"）。Gate 结构通过要求显式输出（"How does the player get [item]? → [answer]"）将推理从"思考"变为"行动"——行动可以被审计，思考不能。

2. **判定模糊。** 散文段落没有明确的"什么情况下停下来问用户 vs 什么情况下继续写"的边界。Gate 结构通过四级判定表（PASS / FAIL / deferred `[unverified]` / batch fast-path）消除了这个模糊性。Agent 不再需要自行判断"这个不确定是否足够不确定到要问用户"，而是按照 L1 命中/未命中路径执行。

Gate 结构与 SKILL.md 现有的 ABSOLUTE RULE 机制天然一致——ABSOLUTE RULE 的核心就是"不能确认就标记 `[unverified]` 并问用户"，Gate 将这个原则具体化到物品可达性和奖励桥接两个最高频的决策点。

### Gate 在 agent 执行流程中的作用方式

三个 gate 形成分层防线：
- **Gate 1 (Item Reachability)** — per-task，blocking。在每个 item task 写入 spec 前执行。L1 命中 → 立即判定；L1 未命中 → 标记 `[unverified]` 延迟到 Step 5。这是防止"物品跨级"硬伤的第一道防线。
- **Gate 2 (Reward Bridge)** — per-reward，blocking。在每个 reward 写入 spec 前执行。四分类判定（material bridge / universal bridge / terminal / dead-end）。这是防止"奖励断链"硬伤的第一道防线。
- **Gate 3 (Dependency Chain Sanity)** — per-node，advisory。在 self-check 步骤执行。不阻止写入，但在 step 7 summary 中显式标注结构异常。这是防止"顺序倒置"和图结构退化的轻量级防线，完整版在 Step 5 执行。

---

## Section C: Risk Assessment (风险评估)

### 1. 对 <=20 quest 小包的影响（per-node loop）

**Token 成本增量：每节点 +200–400 tokens。**

当前每个节点的推理散文约 150 tokens（阅读成本）。升级为 gate 后：
- Gate 1 的一行推理 + L1 查表：~80–120 tokens（物品在 L1 表中时 ~40 tokens，不在时 ~120 tokens）
- Gate 2 的一行推理 + 四分类：~60–100 tokens
- Gate 3 的轻量扫描：~60–80 tokens

对于 20 quest 的包，总额外 token 成本约 4,000–8,000 tokens（20 × 200–400）。这在 128K context window 中占比 <6%，影响可忽略。

**交互轮数增量：每包 +0–3 轮。**

Gate 1 FAIL 时会暂停问用户。对于设计良好的包（outline 合理、物品按阶段递进），大多数 item task 应 PASS 或被 deferred `[unverified]`。预期每 20 quest 的包有 0–3 个 Gate 1 FAIL 需要用户确认。Gate 2 FAIL（dead-end reward）更少见——大多数 reward 自然桥接或属于 universal bridge。

**结论：对小包影响可接受。** Gate 的 token 成本低于一次 validate-and-fix 循环的成本（~2,000 tokens），因此即使只捕获一个物品跨级错误就已经回本。

### 2. 对 >100 quest 大包 batch 模式的影响

**Token 成本增量：每章节 +800–2,000 tokens（批量优化后）。**

关键优化是 **batch fast-path**：
- Gate 1：collection quest 的 N 个 item task 共享一次 `lookup_item.py` 调用 + 批量 L1 查表。Vanilla 物品（在 L1 表中）auto-pass，不需要单独推理行。对于 50-quest chapter 中的 ~40 个 vanilla/well-known item tasks，auto-pass；只对 ~10 个 mod-specific items 产生显式推理行。
- Gate 2：批量写入 spec 时，每个 reward 仍需一行推理。但 material bridge 判定在 chapter 完成后可批量验证（一次扫描所有 reward→task 映射）。
- Gate 3：chapter 完成后一次性扫描，不需要 per-node 执行。

对于 100-quest 包（~5 chapters × 20 quests），总额外 token 成本约 10,000–20,000 tokens。这比 Step 5 的全量验证（~30,000 tokens）低，且被分散到 5 个 chapter batch 中。

**风险：batch 模式下 gate 可能被 agent 跳过。** 这是最大的实际风险。当 agent 在 batch 模式下快速填写 20 个 quest 的 spec 时，可能会省略 gate 推理行以提高效率。**缓解措施：** Gate 定义中明确"batch fast-path"只允许 vanilla/well-known 物品的 auto-pass，不允许整批跳过。每个 mod-specific item 仍需单独推理行。

### 3. "过度推理"风险

**简单物品是否需要推理？**

Gate 1 的 batch fast-path 设计直接解决此问题：
- `minecraft:oak_log` 在第一个 quest 中？→ L1 表命中，维度 = Overworld（无限制），工具 = 无（hand），深度 = 0。**Auto-pass**，不产生推理行。
- `minecraft:ender_pearl` 在第三个 quest 中？→ L1 表命中，维度 = The End。如果祖先链没有 End 维度 → **Gate FAIL**。这正是 gate 的价值。

**判定标准：** L1 表中的 ~25 个 vanilla + ATM 标志性物品走 fast-path（~40 tokens / item，大部分 auto-pass）。L1 未命中的 mod-specific 物品走 slow-path（~120 tokens / item，需要 reasoning）。这个分流确保简单物品不被过度推理，同时复杂物品得到充分检查。

**Gate 2 的"过度推理"风险更低。** 四分类判定（material bridge / universal bridge / terminal / dead-end）是离散的，不需要连续推理。Agent 只需确定 reward 属于哪个类别——这是一个快速分类操作，不是开放式分析。

**Gate 3 的 advisory 性质避免了过度阻塞。** Gate 3 永远不阻止写入，只在 summary 中标注。Agent 和用户都不会因为 Gate 3 而陷入"分析瘫痪"。

### 4. 与现有机制的一致性

- **ABSOLUTE RULE (line 101):** Gate 1/2 的 `[unverified:*]` 标记直接复用 ABSOLUTE RULE 的标记协议。Gate FAIL 时的"stop and ask user"是 ABSOLUTE RULE "宁可空着问用户，不可瞎猜写进 spec" 的具体执行。
- **Generation-time progression checks (line 132):** Edit 5 更新了该段落以引用三个 gate，保持一致性。
- **Verification ladder (lines 124-130):** Gate 的 L1 查表使用 verification ladder 的第 1-2 级数据源（existing_quests.json5 + items.json5），与现有流程一致。
- **Step 5 whole-book validation:** Gate 1/2 是 Step 5 R1-R4/R10 的 generation-time 子集，Gate 3 是 R5/R6/R9 的轻量版。Step 5 的全量检查仍然必要——它用完整图数据覆盖 gate 的 deferred `[unverified]` 项。

### 5. Reviewer C 发现的可执行性问题

Cycle 7 Reviewer C 评估 Step 4 推理步骤的可执行性为 5-8/10。本次 gate 升级直接回应了以下发现：

| Reviewer C 发现 | Gate 升级如何解决 |
|---|---|
| R3 `estimate_recipe_depth_heuristic` 是空函数 | Gate 1 增加了 **name-tier heuristic fallback**（物品名称关键词 → depth 估计），不再是空函数 |
| AP10/AP11 在大型 chapter 中 context 压力大 | Gate 3 将 AP10 的结构比较简化为具体的数值检查（depth / fan-out / orphan），降低 context 需求 |
| Reward bridge 可操作性最高 (8/10) | Gate 2 保留了 reward bridge 的高可操作性，并将其形式化为四分类判定表 |

### 6. 未覆盖的风险

- **Reviewer B 发现的 11 个 per-node 决策空白**（consume_items、repeatable、only_from_crafting 等）不在本次 gate 升级范围内。这些是 Step 2 interview 或 Step 4 co-author 流程的问题，不是推理 gate 的问题。建议在后续 cycle 中处理。
- **Reviewer A 发现的 single-source pattern 问题** 不影响 gate 结构本身（gate 不依赖 MP/AP 的通用性声明），但 ATM Signature filter 应在 Gate 2 的 "universal bridge" 分类中被尊重——MP16 XP Drip 只在 ATM-style 包中被视为 universal bridge。

---

## Section D: Summary of Affected Lines

| Edit | SKILL.md Location | Lines Affected | Nature |
|---|---|---|---|
| Edit 1 | Step 4, step 2 — "Item reachability reasoning" | ~388-389 | Replace prose with Gate 1 definition |
| Edit 2 | Step 4, step 2 — "Reward bridge reasoning" | ~390-391 | Replace prose with Gate 2 definition |
| Edit 3 | Step 4, step 6 — after AP11 bullet | ~406 | Append Gate 3 definition |
| Edit 4 | Step 4 — "Batching by chapter" paragraph | ~411 | Update to reference three gates |
| Edit 5 | ABSOLUTE RULE — "Generation-time progression checks" | ~132 | Update to reference gates |
| Edit 6 | ABSOLUTE RULE — `[unverified]` category list | ~120 | Add new `[unverified]` subcategories |

**Total new content:** ~120 lines of SKILL.md text (replacing ~10 lines of prose + ~4 lines of batching paragraph).
**Net line increase:** ~110 lines.
**Token impact on SKILL.md:** ~3,500 tokens added to the SKILL.md file itself.

---

## Section E: Sync Copy Status

| Path | Status |
|---|---|
| `C:\Users\Adm\.codex\skills\ftb-quests\` | **EXISTS** — needs sync after SKILL.md is updated |

One sync copy requires updating after the gate edits are applied.
