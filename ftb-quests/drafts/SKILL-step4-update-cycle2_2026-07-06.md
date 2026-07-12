# SKILL.md Step 4 & Step 5 — Draft Update (Cycle 2 Integration)

**日期：** 2026-07-06
**基础：** SKILL.md (current main) + Cycle 1 草稿 (SKILL-step4-update_2026-07-05.md)
**整合来源：** Cycle 2 成果——Execution Priority Table (progression-rules.md)、ATM Signature 标注 (micro-patterns.md Scope Annotation Table)、AP14-AP16 (anti-patterns.md)、R28-R29 (progression-rules.md §8)、MP Decision Tree 草稿、Review C 实用性审查

---

## 一、Step 4 完整替换文本

> **替换范围：** 从 `### Step 4 — Polish one node at a time (the loop)` 开始，到 `### Step 5 — Whole-book verify & balance` 之前结束。以下内容完整替换该区间。

---

### Step 4 — Polish one node at a time (the loop)

**Anti-囫囵 rule:** do NOT write the tasks/rewards for the whole book at once. Iterate over the outline nodes — but **scale the loop to the book**: ≤~20 quests → one node at a time with per-node sign-off (steps 1–7 below); ~20–100 → batch by chapter (co-author a chapter's nodes in the spec, regenerate + validate once per chapter, sign off per chapter); >~100 → batch by chapter and skip per-node sign-off, revisiting only quests the validator flags. The incremental merge + `content_hash` still protect untouched quests across a batch. This is where the user 打磨 each task.

#### Context loading before the first node

Before the first node, load three reference slices — not the full documents, but the slices relevant to generation:

1. **AI-generation anti-patterns** — `reference/design/anti-patterns.md §AP9–AP11` (the three risks specific to AI-generated quest configs: hallucination cascade, style homogenization, narrative inconsistency). These inform every step below. Also load §AP14–AP16 summary (system safety: custom task black box, command reward side effects, quest state migration) — a few lines each, not the full case studies.

2. **Progression rules — Step 4 subset** — `reference/design/progression-rules.md §执行优先级表` (the Execution Priority Table, ~30 lines) and `§0` (the builtin lookup tables: `BUILTIN_DIMENSION_MAP`, `BUILTIN_TOOL_TIER_MAP`, `BUILTIN_ORE_REQUIREMENTS`, `estimate_recipe_depth_heuristic`). Do NOT load the full rule definitions for R1–R29; the Step 4 subset uses only the L1 builtin tables and the priority table's P0/P1/P2 classification. The full rules load in Step 5.

3. **Micro-pattern decision table** — use the simplified decision table below (not the full `micro-patterns.md`). The decision table covers task combination (MP1–MP5), reward bridging (MP14–MP18), and extended types (MP27–MP32). Part 2 (dependency topologies MP6–MP10) and Part 5 (stage marking MP19–MP23) were already decided in Step 2 outline — they don't need re-loading here.

#### MP selection decision table (per-node reference)

When generating each quest, select applicable patterns by walking this table top-to-bottom. A quest matches one entry from the Task Combination layer and may stack entries from the Reward Bridging layer. Layer 2 (dependency topology) and Layer 5 (stage marking) are inherited from the Step 2 outline — don't re-decide them here.

**Layer 1 — Task combination (pick one):**

- `tasks.count == 1 AND task.type == "item"` → **MP1** Single-Item Gate (the default — 90%+ of quests)
- `tasks.count >= 2 AND all tasks are "item" type AND quest is a convergence node (deps >= 3 from different mods)` → **MP2** Multi-Item Synthesis Bundle. *Not* a checklist — only use when the quest represents a cross-system crafting convergence. Three iron ingots + two planks is two MP1 quests, not one MP2.
- `task.type in ("checkmark", "stat", "observation")` → **MP3** Acknowledgement Gate (tutorial/teaching quest with a longer description)
- `task.type in ("kill", "stat") AND quest is part of an escalation chain (marked in outline)` → **MP4** Escalation Ladder. *ATM Signature — see the ATM filter note below.*
- `tasks include both "dimension" and "item" types` → **MP5** Dimension + Item Composite. Verify R1 (item from that dimension) passes.

**Layer 4 — Reward bridging (stack as applicable):**

- `reward item appears as a task item in a downstream dependent quest` → **MP14** Material Bridge (the strongest forward pull)
- `reward is a tool-type item (pickaxe, wrench, guide book, machine block)` → **MP15** Tool Reward
- `pack_type == "kitchen-sink"` → **MP16** XP Drip (add `{ type: "xp", xp: 10 }` as baseline). *ATM Signature — see the ATM filter note below.* Expert and create packs do not use XP drip.
- `quest is a catalog hub AND most cell quests have no reward` → **MP17** Hub Concentration
- `quest is a branch point AND reward determines the downstream path` → **MP18** Choice Reward (expert/RPG meaningful choice)

**Layer 6 — Extended types (pick as applicable):**

- `task.type == "fluid"` → **MP27** Fluid Task Gate (fluid amount should be a multiple of the producing machine's output)
- `task.type == "forge_energy"` → **MP28** Energy Threshold Gate (calibrate against best available generator at this stage)
- `reward.type == "command"` → **MP29** Command Reward — **must pass R28 Command Reward Safety Scan** before writing; see AP15 for idempotency and permission hazards
- `pack uses gamestage gating` → **MP30** Gamestage Bridge (each stage grant must have a matching stage check)
- `task.type == "structure"` → **MP31** Structure Discovery Gate (verify the target structure exists in world gen)
- `quest has min_tasks modifier` → **MP32** min_tasks Modifier (overlap with MP9 at the task level; see Create: Astral's alternative recipe paths)

#### ATM Signature filter

Five micro-patterns are marked as **ATM Signature** in the Scope Annotation Table (micro-patterns.md): MP4 (Escalation Ladder), MP16 (XP Drip), MP20 (Shape-as-Tier Signal), MP21 (Dimension-as-Stage-Gate), MP22 (Material-Tier Spine). Their core evidence comes entirely from AllTheMods packs (ATM-8/9/10/10-Sky). The concepts (escalation, XP rewards, shape semantics, dimension gating, material tiers) are transferable, but the specific implementations are ATM design choices, not universal best practices.

**Filtering rule:** if the current pack is not an ATM-series pack (not authored by AllTheMods, not explicitly modeled on ATM design philosophy), these five patterns are **reference only** — do not apply them by default. Specifically:

- MP4 Escalation Ladder: only use if the pack has a mob-grind or repeatable-activity gameplay loop
- MP16 XP Drip: only use if the pack's reward philosophy is "generous" (ATM-style); skip for expert, create, or minimalist packs
- MP20 Shape-as-Tier Signal: only use if the chapter plan already calls for rich shape vocabulary (most non-ATM packs use 1–2 shapes)
- MP21 Dimension-as-Stage-Gate: applicable when dimension travel is the primary progression axis (most non-ATM packs use chapter groups or voltage tiers instead)
- MP22 Material-Tier Spine: only for ATM-style kitchen-sinks with a vertical material tier across dimensions

Similarly, `hide_dependency_lines` is an ATM preference (ATM-10 uses it 438 times), not a universal anti-clutter lever. Narrative and expert packs prefer `hide_until_deps_visible` for progressive reveal. Use `hide_dependency_lines` only when the layout family is kitchen-sink/ATM or when the chapter has high visual complexity (hub with >3 dependents, long cross-column lines).

For each quest, record the selected MP patterns in a brief inline note in the spec (e.g., `// MP1 + MP14 + MP15`) — this helps the Step 5 reviewer understand the design intent and catches misapplied patterns.

---

For each node:

1. **Pick one quest** (main-line order; side branches after their fork point). Say which one you're polishing.

2. **Co-author its content** — grill per the Step 2 interview discipline: ONE question with your recommended answer, wait for the user, then the next (task type + target + count → reward type + payload → description text). **Never dump a list of questions.** "帮我设计" → draft the content yourself, user approves/edits; "我要指定每个任务" → ask per task. Resolve mod mechanics / reward effects by checking the codebase or asking — never guess. Before writing a task/reward item, confirm its id is in `.ftbq-cache/items.json5` `all_item_ids` or `existing_quests.json5` `known_item_ids` (Step 1); if it isn't listed, ask the user to confirm it in JEI/EMI — **never invent an item id** (see "Verify, don't fabricate"). For a **collection quest / many-item batch**, resolve all the display names → ids in one call with `lookup_item.py <packroot> <name>…` (see "Batch item-id lookup") and write tasks from those results — don't grep `all_item_ids` N times. When writing the description text, follow **Quest text & description writing style** (near the top of this skill) — natural, concise prose, not label-value 要素式 checklists; the quest UI already shows the item/count/reward, so spend the description on the *why* and *how*.

   **Mandatory item reachability reasoning (before finalizing each task).** Before you commit an `ftbquests:item` task to the spec, you **must** answer this question — silently, as an internal check — and surface the result to the user if it fails:

   > 「玩家此刻怎么拿到这个？」

   Walk the quest's ancestor chain (the `depends_on` path back to the chapter root) and check the task item against the **Step 4 Execution Priority subset** from `reference/design/progression-rules.md §执行优先级表`:

   - **R1 Dimension-Reachability (L1 only):** check the item against `BUILTIN_DIMENSION_MAP` (§0). If the item is in the map and its dimension is not in the ancestor chain's unlocked dimensions, this is a **P1 item cross-tier** violation — stop and surface it. If the item is not in the map, mark `[unverified:dimension]` and continue.
   - **R2 Tool-Tier (L1 only):** check against `BUILTIN_TOOL_TIER_MAP` and `BUILTIN_ORE_REQUIREMENTS` (§0). If the item requires a tool/mining level that no ancestor provides, this is a **P2 item cross-tier** violation — mark `[unverified:tool_tier]` and surface it.
   - **R3 Recipe Depth (L1 heuristic):** run `estimate_recipe_depth_heuristic` (§0) on the item id. If the estimated recipe depth exceeds the quest's dependency depth + 2 (the ALLOWANCE), flag as **P2 potential depth mismatch** — mark `[unverified:recipe_depth]`.
   - **R4 Stage Boundary (degraded):** check whether the item appears as a task or reward in any already-generated ancestor quest. If the item only appears in later chapters' tasks (not yet generated), flag as **P2 potential stage boundary violation** — mark `[unverified:stage]`.

   When an L1 check **hits** (the item is in the builtin table and fails the check), this is a generation-blocking finding: fix the task item, adjust the dependency chain, or get explicit user confirmation before writing. When L1 **misses** (the item is not in any builtin table), the `[unverified]` tag is a deferred check — it will be resolved in Step 5 when the full graph is available. The goal is to catch the three hardest progression errors (item cross-tier, sequence inversion, reward disconnection) at generation time, not after a validate-and-fix round-trip.

   For pack-specific items not covered by the L1 tables, reason from the ancestor quests' rewards and the mod's known recipe ladder. If you cannot confirm reachability, mark `[unverified:progression]` and surface it to the user before writing.

   **Mandatory reward bridge reasoning (after drafting each reward).** Once you have a reward drafted, you **must** answer this question:

   > 「这个奖励引导玩家去做什么？」

   - **R10 (reverse / backward check):** does the reward item appear as a task item in any already-generated quest that depends on this one's ancestors? More practically: when generating the *next* quest, check whether its task items match this quest's rewards (the Material Bridge pattern, MP14). If the reward is an item that no downstream quest requires and it isn't a recognized universal bridge type (tool reward MP15, XP drip MP16), it's a dead-end reward (AP6) — redesign it so the player has a clear next step.
   - **R28 Command Reward Safety:** if the reward type is `command`, execute the R28 safety scan **before** writing it to the spec: check the command string against `FORBIDDEN_COMMANDS` (ERROR — block write), `HIGH_RISK_COMMANDS` (WARNING — surface to user), and `IDEMPOTENCY_RISK` (INFO — note for the user). See `reference/design/progression-rules.md §R28` for the exact regex patterns. Command rewards are the single highest-risk reward type (AP15) — prefer standard reward types (`item`, `xp`, `loot`) whenever possible.
   - **Dead-end reward detection:** if the reward is a material item and no dependent quest in the outline lists it as a task, flag AP6 risk and suggest either (a) changing the reward to a bridge item that a downstream quest needs, or (b) adding a dependent quest that uses it. For terminal quests (capstone, chapter leaf with no dependents) this check doesn't apply.

   The formal rules are R10–R13 in `reference/design/progression-rules.md §3`; at generation time you're doing the same reasoning by hand, one reward at a time, using backward matching (task → ancestor reward) because forward matching (reward → dependent task) requires quests that haven't been generated yet. The Step 5 whole-book pass runs the forward check.

3. **Update ONLY that quest** in `quests.spec.json5` (fill its `tasks`/`rewards`) and its `quest_desc` / `quest_subtitle` in the **primary locale's** lang file. Leave every other quest's empty `tasks: []` untouched. Translate to secondary locales in a dedicated pass after the primary is settled (Step 4 done) — don't block each node's sign-off on every locale; the generator's lang is add-only per locale, so mirror the primary's keys. If no translator, ship the primary and flag secondaries for the user/pack team. In the spec, references use `name` (within a chapter) or `<chapter>/<quest>` (across chapters); raw 16-hex tokens pass through for existing-pack linkage (see "Task linkage" below).

4. **Regenerate** — `python scripts/generate_quests.py <output_dir>`. The incremental merge keeps every other quest pristine (content_hash match → no-op) and re-emits only the quest you touched; in-game position edits to other quests are preserved regardless of mode. The ID-uniqueness check runs pre-emit, so a name clash fails fast before any file is written.

5. **Verify that one quest** — `python scripts/validate_quests.py <output_dir>/quests/` (fast; diagnostics carry `file:line:col`), then preview JUST that quest instead of reading the whole chapter file:
   ```bash
   python scripts/quest_detail.py <output_dir> <chapter>/<quest>
   ```
   It resolves the quest by name (via the spec's pack + the id formula) and prints only that quest's id/shape/deps/tasks/rewards/lang — token-saving vs. reading the whole chapter.

6. **AI generation self-check (per node).** After the quest passes validation and before presenting the summary, review it for the three AI-specific anti-patterns (`reference/design/anti-patterns.md §AP9–AP11`):
   - **Description-item consistency (R23).** Does the `quest_desc` mention any item ID that doesn't appear in this quest's tasks or rewards? Conversely, does the description fail to explain a task item that the player needs context for? The static rule in `reference/design/progression-rules.md §6` catches ID-level mismatches; at generation time, read the description you just wrote and confirm every named item matches the config, and every config item has a reason to be there. **R23 is P0 — a description-item mismatch blocks the spec write.**
   - **Style drift (AP10).** Compare this quest's description structure to the last 2–3 quests you polished. Are they all following the same template ("Obtain [item]. This is needed for [next step].")? Vary the description mode — how-to, lore, tip, challenge — so the chapter doesn't read like a form letter. Reward amounts and shape vocabulary should vary too (`reference/design/anti-patterns.md §AP10` for detection heuristics).
   - **Narrative continuity (AP11).** If this quest's description makes a forward reference ("you'll need this for the next quest") or a difficulty claim ("the hardest craft so far"), verify the referenced quest actually exists and matches. Check that the tone (casual / technical / lore-heavy) is consistent with the chapter's established voice — a tonal lurch between adjacent quests breaks the player's trust in the book as a guide.
   - **Custom task safety (AP14).** If this quest uses a `custom` task type, verify that (a) the custom task handler's type ID is explicitly provided by the user (not invented by the agent — AP14's black-box risk), (b) the quest description explicitly states what the player needs to do (since the quest UI won't show it), and (c) the quest is flagged as `[unverified:custom_task]` for Step 5a load-test verification. AI should **never proactively create custom tasks** — only use them when the pack author explicitly requests and provides the handler details.

7. **Show a focused summary** of just that quest (id, tasks, rewards, lang title/desc, selected MP patterns) and ask: keep & continue, or revise? Only advance to the next node when the user is happy with this one.

**Chapter-level teaching order check.** After all quests in a chapter are polished (or after a chapter batch), step back and verify the chapter's internal teaching sequence. The two patterns to confirm are Teach-Then-Do (`reference/design/micro-patterns.md §MP11`) and Tier Escalation (`reference/design/micro-patterns.md §MP12`): for each mod mechanic the chapter covers, a teaching quest (checkmark/stat task + long description explaining the concept) should appear *before* the doing quest (item task requiring the player to apply what was taught); and within a material or tool tier, quests should escalate from cheapest/simplest to most expensive/complex. The formal rules R14–R17 (`reference/design/progression-rules.md §4`) detect inversions statically; at generation time, read the chapter's quest list in dependency order and confirm that no doing-quest precedes its teaching-quest, and no high-tier quest appears before a lower-tier one. If you find an inversion, reorder the `depends_on` chain in the outline and update the spec before moving to the next chapter. This is also the moment to check for AP9 hallucination cascade (`reference/design/anti-patterns.md §AP9`) across the whole batch — scan every item ID introduced during this chapter's generation against `items.json5` one more time, rather than trusting that each per-node check was sufficient.

**Incremental dependency graph check.** After all quests in a chapter are polished, perform a quick structural check on the chapter's dependency graph:

- **R5 (incremental cycle detection):** walk the chapter's `depends_on` graph (which should be a DAG from the Step 2 outline) and verify no cycle was introduced during generation. The outline should already be acyclic, but manual edits during the Step 4 loop can accidentally introduce cycles — especially when adding cross-references or re-ordering quests. If a cycle is found, identify the offending edge and ask the user to break it.
- **R6 (local unreachable check):** verify every non-root quest in the chapter has at least one dependency path to a root quest (a quest with no dependencies). Flag any quest whose dependencies all point to optional or secret quests without a non-optional bypass — this is the mandatory-quest-blocked-by-optional-gate pattern (R7).
- **R7 (optional-gate-mandatory, chapter-wide recheck):** confirm no mandatory quest depends solely on optional quests. This was checked per-node in step 2, but the chapter-level view can reveal chains where an optional quest is an indirect prerequisite (A mandatory → B optional → C optional, making A unreachable if B is skipped).

**Batching by chapter:** fill all of a chapter's quests' `tasks`/`rewards` in `quests.spec.json5`, then run `generate_quests.py` once + `validate_quests.py` once; use `generate_quests.py --dry-run` to preview the batch before committing. Run `quest_detail.py` per node only for quests that fail validation or that you want to spot-check. When batching, the mandatory item reachability and reward bridge reasoning (step 2) apply to each quest as you write it into the spec; the AI self-check (step 6) and the chapter-level teaching order check run once after the whole batch is written.

Re-run modes:

```bash
python scripts/generate_quests.py <output_dir>                  # default: overwrite skill-owned, preserve user-added
python scripts/generate_quests.py <output_dir> --mode preserve  # keep ALL on-disk edits
python scripts/generate_quests.py <output_dir> --mode ask       # prompt per conflict
python scripts/generate_quests.py <output_dir> --adopt          # first run on an existing pack
```

**Before `--mode ask` / `--adopt` on an existing pack**, check blast radius first: the manifest + validator catch quest dependency chains; if CodeGraph is available, also run `codegraph_impact` on the target quest files — it adds cross-file references (lang keys, `quest_links`) the manifest misses. Either source finding affected quests the other missed is a signal to stop and confirm with the user.

Reward tables (`reward_tables[]`), quest links (`quest_links[]`), and chapter images (`images[]`) can be authored whenever their owning quest comes up in the loop — add them to the spec and regenerate the same way. The `@<chapter>/<quest>.subkey` lang placeholders (subkeys: `title`, `quest_subtitle`, `quest_desc`, `chapter_subtitle`) are rewritten to `quest.<HEX>.subkey` on generate; with `format: "snbt"` the generator emits **inline** `title`/`subtitle`/`description` on the quest/chapter objects (the 1.20.1 variant — the only SNBT variant it emits; the 2021.1 SNBT+lang variant is adopt-only, see the CRITICAL detection rule).

---

## 二、Step 5 验证增强（替换 Step 5 中的相应段落）

> **替换范围：** 在 `### Step 5 — Whole-book verify & balance` 中，替换从 "The whole-book validation runs the full progression-rules pipeline" 段落开始到 "Dev testing" blockquote 之前的文本。

The whole-book validation runs the full progression-rules pipeline — all 29 rules (R1–R29, `reference/design/progression-rules.md`) plus 16 anti-patterns (AP1–AP16, `reference/design/anti-patterns.md`). The Step 4 per-node checks are a generation-time subset using only local data and L1 builtin tables; Step 5 catches cross-quest and cross-chapter issues that only become visible once the full graph exists. The Execution Priority Table (`progression-rules.md §执行优先级表`) classifies every rule into Step 4 (generation-time), Step 5 (whole-book), or external-script categories; Step 5 runs all rules classified as Step 5 plus a re-run of the Step 4 rules on the full data.

After the `validate_quests.py` command block and before the "Dev testing" blockquote, perform these additional whole-book checks:

**Full-graph structural checks (run after the validator passes):**

- **R5 — Circular Dependency Detection (complete DFS):** run a full DFS cycle detection across the entire book's dependency graph, including cross-chapter references. The Step 4 incremental check only caught cycles within the chapter being generated; Step 5 catches cycles that span chapters (e.g., chapter A's quest depends on chapter B's quest, which transitively depends back on chapter A). Report any cycle found with the full path.

- **R6 — Unreachable Quest Detection (complete reachability):** for every non-root quest in the book, verify at least one dependency path exists from a root quest (no dependencies) to this quest, where no step in the path is blocked by an optional-gate-mandatory pattern (R7) or an undiscoverable secret. Flag quests whose only paths go through optional or secret prerequisites.

- **R10 — Reward Bridge Verification (forward check):** for every non-terminal quest (a quest that has dependents), check whether its reward items appear as task items in at least one dependent quest. This is the forward-direction check that Step 4 couldn't do (Step 4 only did the backward check: task → ancestor reward). Flag dead-end rewards (AP6) where a quest's reward item is never required by any downstream quest and isn't a recognized universal bridge type.

- **R28 — Command Reward Safety Scan (full sweep):** if any quest in the book has a command reward, run the complete R28 scan (FORBIDDEN_COMMANDS, HIGH_RISK_COMMANDS, IDEMPOTENCY_RISK, {p} placeholder check, cross-dimension check) from `progression-rules.md §R28`. This catches command rewards that were added during batch generation and may have been missed by the per-node check, or command rewards from existing pack content that the `--adopt` / `--mode preserve` flow brought in.

- **AP14 — Custom Task Black Box check:** for every quest with a `custom` task type, verify that the quest is flagged `[unverified:custom_task]` (meaning the user confirmed the handler exists) and that the quest description explicitly states what the player needs to do. Downgrade R6/R20 to INFO for quests containing custom tasks — their completability cannot be statically verified. If a custom task quest is non-optional and has mandatory dependents, flag as WARNING: a black-box quest gating mandatory progression is an AP14 + AP3 risk.

- **AP16 — Quest State Migration (update scenarios only):** when running in `--adopt` or `--mode preserve` on an existing pack, check for stale dependency references — quest IDs that exist in the on-disk config's `dependencies` arrays but no longer correspond to any quest in the generated or preserved output. This is the update-compatibility check that catches the "deleted quest leaves dangling reference" failure mode.

---

## 三、设计理由 (Design Rationale)

### 为什么将强制推理步骤嵌入 Step 2（co-author）而非独立章节

三硬伤的推理步骤（物品可达性、奖励桥接）被嵌入现有的 step 2 co-author 段落中，而不是创建一个独立的 "Mandatory Checks" 章节。这遵循 SKILL.md 的现有模式——物品 ID 验证在 step 2 的段落中、教学顺序检查在 chapter-level 段落中——而不是创建一个容易被跳过的独立清单。嵌入式检查是写作流程的自然门控，不是额外负担。

### 为什么 Step 4 只执行规则子集

Execution Priority Table 将 29 条 R 规则分为三类：Step 4 生成时检查（局部数据即可）、Step 5 验证时检查（需要完整依赖图）、外部脚本（需要运行时数据）。Step 4 试图执行所有规则会导致每个规则都做得不彻底——因为完整图数据在逐节点生成时不可用。只执行 P0/P1 级的局部检查（R23、R7、R22、R28 的直接检查 + R1-R4 的 L1 降级版 + R5/R6 的增量版 + R10 的反向检查），其余推迟到 Step 5，这比试图在 Step 4 执行所有规则更可靠。

### 为什么 R10 在 Step 4 做反向检查、Step 5 做前向检查

Step 4 按依赖顺序生成（root → leaves），生成 quest A 时，依赖 A 的 quest B 还没有生成，所以无法做 "reward → dependent task" 的前向检查。但可以做反向检查：生成 quest B 时，检查 B 的 task 物品是否出现在 B 的祖先 quest 的 reward 中。这覆盖了 R10 的一半逻辑（"task 是否有祖先 reward 支撑"）。Step 5 在所有 quest 生成完毕后运行前向检查（"reward 是否有下游 task 消费"），覆盖另一半。两个方向的检查互补，不重复。

### Context window 分段加载策略

三个参考文档合计约 58,000 tokens（micro-patterns.md ~18k, progression-rules.md ~30k, anti-patterns.md ~10k），加上 SKILL.md 本体 ~15k 和 items.json5，总计可能超过 100k tokens。分段加载策略基于 Review C 的建议：

- **Step 4 加载：** MP Part 1（task 组合 MP1-MP5）+ Part 4（reward 桥接 MP14-MP18）+ Part 7（extended type MP27-MP30）+ Part 8（Cycle 2 新增 MP31-MP32）+ 本草稿中的简化决策表 + R Execution Priority Table 的 Step 4 部分 + R §0 内置映射表 + AP9-AP11 摘要 + AP14-AP16 摘要。总计约 8,000–12,000 tokens。
- **Step 5 加载：** MP Part 6（MP24-MP26，作为 R 规则的索引）+ R 全部（完整规则定义）+ AP 全部（完整案例）。总计约 40,000 tokens，但 Step 5 是一次性运行，不需要同时持有 Step 4 的生成上下文。
- **Step 2 加载：** MP Part 2（dependency topologies MP6-MP10）+ Part 5（stage marking MP19-MP23）+ design-guide.md §principles。这些在 Step 2 outline 阶段需要，Step 4 不需要重新加载。

### ATM Signature 过滤的必要性

五个 ATM Signature 模式（MP4/MP16/MP20/MP21/MP22）的核心证据全部来自 AllTheMods 系列包。在 15 个审计包中，只有 ATM-8/9/10/10-Sky 使用了这些模式的具体实现形态。如果将 ATM 的做法作为通用最佳实践推广，non-ATM 包会被迫采用不适合其设计哲学的设计模式——例如 expert 包被建议加 XP drip（MP16），或者 narrative 包被建议用 hide_dependency_lines 替代 hide_until_deps_visible。过滤规则确保 ATM 模式只在适用的上下文中被默认使用。

### Step 5 增强的选择逻辑

Step 5 新增的五个检查（R5 完整 DFS、R6 完整可达性、R10 前向检查、R28 全量扫描、AP14 黑盒检查）都满足两个条件：(1) 需要完整依赖图数据（Step 4 无法完整执行），(2) 失败后果严重（循环依赖死锁、不可达 quest、奖励断链、command 安全漏洞、黑盒 quest 阻塞 mandatory 进度）。AP16 检查仅在 update 场景（`--adopt` / `--mode preserve`）中执行，因为新 pack 不存在状态迁移问题。

### Cycle 1 草稿的整合方式

Cycle 1 草稿（SKILL-step4-update_2026-07-05.md）的核心内容——item reachability reasoning、reward bridge reasoning、chapter-level teaching order check、AI self-check (step 6)、cross-reference update recommendations——已经整合到当前 SKILL.md 中（2026-07-05 的六个 cross-reference 修改）。本次 Cycle 2 草稿在此基础上增加了：

1. **强制推理问题的显式化：** 将 "internally answer this question" 升级为带有具体检查步骤的 mandatory reasoning（查 L1 映射表 → 判断 P0/P1/P2 级别 → 决定 block 还是标记 unverified）
2. **Execution Priority Table 的嵌入：** Step 4 检查哪些规则、为什么只检查这些，由 Priority Table 而非 agent 自行判断
3. **R28 Command Reward Safety：** 新增 P0 级检查，因为 command reward 是 AI 生成中最高风险的 reward 类型
4. **ATM Signature 过滤：** 防止 ATM 特有的设计模式被误用到 non-ATM 包
5. **MP Decision Table：** 将 Review C 指出的 "缺乏显式决策树" 问题解决，agent 在 Step 4 有明确的模式选择参考
6. **AP14 检查：** 防止 AI 主动创建 custom task（黑盒风险）
7. **Step 5 全图检查增强：** R5/R6/R10/R28/AP14/AP16 的全图级别执行

Cycle 1 草稿中的 "Sync Copy Report" 和 "Cross-Reference Update Recommendations" 部分不再需要——它们描述的六个 cross-reference 修改已经应用到当前 SKILL.md。

---

## 四、与现有 SKILL.md 的关系

### 不需要修改的 SKILL.md 段落

以下段落已经包含了 Cycle 1 草稿的整合内容，不需要再次修改：

- `## Quest text & description writing style` — 已包含 "AI-specific style risks" 段落（AP10/AP11 引用）
- `## CRITICAL — read before generating` / `## ABSOLUTE RULE` — 已包含 "Generation-time progression checks" 段落（R1-R4, R10-R13, R14-R17 引用）
- `## Design principles` — 已包含 "Anti-patterns to design against" 段落（AP1-AP11 引用）
- `## Quest progression, arrangement & authoring logic` — 已包含 "Micro-level authoring patterns" 段落（MP 引用和加载时机）
- `## Sources` — 已包含 "Progression validation framework" 段落（R1-R23, MP1-MP30, AP1-AP11 引用）

### 需要修改的 SKILL.md 段落

仅两个段落需要替换：

1. **Step 4**（从 `### Step 4` 到 `### Step 5` 之前）— 用本文档第一部分替换
2. **Step 5 的 "whole-book validation" 段落**（从 "The whole-book validation runs the full progression-rules pipeline" 到 "Dev testing" blockquote 之前）— 用本文档第二部分替换

### Sources 段落追加

在现有 Sources 段落末尾追加：

```
**Cycle 2 progression framework update** (2026-07-06): progression-rules.md expanded to 29 rules (R1–R29, adding R24–R26 suggestion/necessity/version checks and R28–R29 safety/team checks); anti-patterns.md expanded to 16 anti-patterns (AP1–AP16, adding AP12–AP13 task-system mechanism defects and AP14–AP16 system safety/compatibility); micro-patterns.md expanded to 32 micro-patterns + 7 player-perspective patterns (MP1–MP32 + PP1–PP7, adding MP31–MP32 structure/min_tasks patterns and PP7 mod-unification trap). Execution Priority Table classifies all 29 rules into Step 4 (generation-time) / Step 5 (whole-book) / external-script categories. ATM Signature annotation marks 5 patterns (MP4, MP16, MP20, MP21, MP22) as ATM-series-specific. MP Decision Tree provides per-node pattern selection guidance.
```

---

## 五、Sync Copy 状态

| Path | Status |
|---|---|
| `C:\Users\Adm\.codex\skills\ftb-quests\` | **EXISTS** — needs sync after SKILL.md is updated |

One sync copy requires updating after the Step 4/5 replacement is applied.
