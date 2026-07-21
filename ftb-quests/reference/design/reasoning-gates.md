# Reasoning Gates — Step 4 Per-Node Mandatory Checks

Three gates embedded in the Step 4 per-node loop. Gates 1–2 are **blocking** (FAIL prevents writing to the spec). Gate 3 is **advisory** (surfaces warnings in the summary). The formal whole-graph versions of these checks run in Step 5 (R1–R32, R55–R64) with the full dependency graph available.

Load `reference/design/shared-builtin-tables.md` for the L1 lookup tables used by Gate 1 fast-paths.

---

## Gate 1 — Task Item Reachability

*Mandatory before writing each `ftbquests:item` task to the spec.*

For every item task, produce this one-line reasoning **out loud** (working notes, not the spec):

> How does the player get [item_id] at this point? → [answer]

Walk the three checks. Each has a fast-path (L1 builtin table hit) and a slow-path (L1 miss → reason from context).

| Check | L1 fast-path (item in builtin table) | L1 miss (item NOT in builtin table) |
|---|---|---|
| **R1 Dimension** | Look up `BUILTIN_DIMENSION_MAP` (`shared-builtin-tables.md §0`). If the item's dimension is NOT in the ancestor chain's unlocked dimensions → **GATE FAIL: P1 cross-tier**. Stop, surface to user. | Reason from the quest's ancestor rewards and mod context. If unsure → mark `[unverified:dimension]`, continue. |
| **R2 Tool tier** | Look up `BUILTIN_TOOL_TIER_MAP` + `BUILTIN_ORE_REQUIREMENTS`. If required tool/mining level exceeds what ancestors provide → **GATE FAIL: P2 cross-tier**. Stop, surface to user. | Reason from the mod's known tool progression. If unsure → mark `[unverified:tool_tier]`, continue. |
| **R3 Recipe depth** | Run `estimate_recipe_depth_heuristic` on the item id. If estimated depth > quest dependency depth + 2 → **GATE FAIL: P2 depth mismatch**. Mark `[unverified:recipe_depth]`, surface. | Use **name-tier heuristic** as fallback: `ingot`/`dust`/`gear`/`nugget` ≈ depth 1–2; `machine`/`circuit`/`processor`/`controller` ≈ depth 3–4; `multiblock`/`fusion`/`singularity` ≈ depth 5+. Mark `[unverified:recipe_depth]`. |

**R42 Stage-Internal Item Reachability (additional):** after the three checks, each task item additionally answers:

> 玩家此刻怎么拿到这个？——引用 `mod-item-reachability.md` R42

If the pack has L2 stage data (`stage_map` + `stage_available_resources` from Step 2), check whether the item's crafting-chain leaf nodes fall within the current stage's reachable resource set. Without L2 data, fall back to the R1 + R4 L1 heuristic combination and mark `[unverified:stage_recipe]`. This is a semantic reinforcement of Gate 1, not a change to its pass/fail logic.

**Gate verdict:**
- **PASS** (all checks pass or deferred `[unverified]`) → write the task to the spec.
- **FAIL** (any L1 hit returns P1/P2 violation) → do NOT write. Instead: (a) suggest an alternative item the player CAN reach, (b) suggest adjusting the dependency chain to unlock the required dimension/tool, or (c) ask the user to confirm they want this item here despite the gap. Only proceed with explicit user approval; note the override: `// Gate 1 override: user confirmed [item] despite [reason]`.

**Batch fast-path:** for collection quests with many item tasks, run Gate 1 once per batch. Resolve all item ids via `lookup_item.py` first, then run the three checks on each. Vanilla/well-known items (in L1 tables) auto-pass; only flag items that fail or miss. Don't produce individual reasoning lines for trivially-passing items (e.g. `minecraft:oak_log` in the first quest).

**Scope:** Gate 1 applies only to `ftbquests:item` tasks. Non-item tasks (`checkmark`, `stat`, `advancement`, `dimension`, `biome`, `kill`, `structure`, `observation`, `xp`, `custom`) are exempt — they have no item to check. For `ftbquests:fluid` tasks, apply the same logic substituting the fluid's source mod and production method.

---

## Gate 2 — Reward Bridge

*Mandatory before writing each reward to the spec.*

For every reward, produce this one-line reasoning **out loud**:

> This reward leads the player to: [answer]

Classify into one of four categories:

| Category | Condition | Verdict |
|---|---|---|
| **Material bridge (MP14)** | The reward item appears as a task item in at least one dependent quest in the outline, or in a quest generated later in this chapter. | **PASS** — strongest forward pull. Write. |
| **Universal bridge** | Recognized universal bridge type: tool reward (MP15 — pickaxe, wrench, guide book, machine block), XP drip (MP16 — only for kitchen-sink/ATM-style generous packs), or currency from a known currency mod (`lightmanscurrency`, `gtocore` coins). | **PASS** — write. |
| **Terminal reward** | This quest is a capstone, chapter leaf, or has no dependent quests in the outline. The reward is the endpoint, not a bridge. | **PASS** — write. Mark: `// Gate 2: terminal reward (no dependents)`. |
| **Dead-end risk (AP6)** | Material item, no dependent quest requires it as a task, not a universal bridge, not terminal. | **GATE FAIL** — do NOT write. Instead: (a) redesign as a material bridge to a downstream quest, (b) add a dependent quest that uses this item, or (c) if the user insists, mark `[unverified:reward_bridge]` + note: `// Gate 2 override: user accepted dead-end reward`. |

**R45 Reward Guidance Bridging (chapter-level additional):** after the four categories, each reward additionally answers:

> 这个奖励引导玩家去做什么？——引用 `mod-reward-design.md` R45

If the current quest is the chapter's capstone (most dependents), check whether its reward includes an item or gamestage unlock needed by the next chapter's entry quest (a virtual bridge item). If it bridges neither an item nor a stage, flag as chapter-level dead-end risk. This is a semantic reinforcement of Gate 2 raised to the chapter level, ensuring chapter-to-chapter transitions have explicit reward guidance.

**Backward matching (practical note):** Step 4 generates in dependency order (root → leaves), so forward checks (reward → dependent task) often can't run because dependents don't exist yet. Use **backward matching**: when generating quest B, check whether B's task items match any ancestor quest's rewards. The formal forward check runs in Step 5 (R10).

**R28 Command reward safety (sub-gate):** if the reward type is `command`, additionally pass the R28 Command Reward Safety Scan before writing — check `FORBIDDEN_COMMANDS` (ERROR — block write), `HIGH_RISK_COMMANDS` (WARNING — surface to user), `IDEMPOTENCY_RISK` (INFO — note). See `mod-reward-design.md §R28`. Command rewards are the highest-risk type (AP15) — prefer `item`, `xp`, `loot` whenever possible.

**R31 XP-level pre-check (sub-gate):** if the reward type is `xp_levels`, check whether this quest is a milestone/capstone (high fan-in, distinctive shape). Non-milestone `xp_levels` rewards drift in value with player level (AP17). If not a milestone, suggest flat `xp` instead or surface the risk.

**Batch fast-path:** when batching a chapter, run Gate 2 once per reward as you write the spec. Dead-end detection (AP6) is most effective after the full chapter's tasks are written — do a quick chapter-level dead-end sweep after the batch.

---

## Gate 3 — Dependency Chain Sanity

*Lightweight advisory scan after the per-node anti-pattern checks pass, before presenting the summary.*

| Check | Condition | Action |
|---|---|---|
| **Chain depth** | Longest `depends_on` path from this quest back to a chapter root exceeds the pack-type threshold (`kitchen-sink: 8`, `expert: 20`, `skyblock: 20`, `rpg: 12`, `create: 10` — from R9), or exceeds neighboring quests' depth by 3+ | **WARN** — "Chain depth N exceeds threshold / neighbors by M. Consider a shortcut dependency or restructure." |
| **Fan-out** | Direct dependents > 5 (hub pattern) | **INFO** — "Hub with N dependents. Consider `hide_dependency_lines` (kitchen-sink) or `hide_until_deps_visible` (narrative) to reduce visual clutter." |
| **Orphan risk** | No dependents AND no `optional: true` AND not the last quest in the chapter | **WARN** — "Dead-end quest with no dependents and not marked optional. Add a dependent, mark optional, or verify it's intentionally a leaf." |
| **Diamond rejoin** | Depends on multiple quests that share a common ancestor (rejoin after fan-out) | **INFO** — "Diamond pattern detected. Verify `dependency_requirement` is correct (`all` = must do all branches, `one` = any branch suffices)." |

Gate 3 is **advisory, not blocking** — it surfaces structural observations in the step-7 summary for the user to decide. The formal versions (R5, R6, R7, R9) run in Step 5 with the full graph.

---

## AI Generation Self-Check (per node, after validation, before summary)

Review the quest for the three AI-specific anti-patterns (`mod-description-trust.md §AP9–AP11`):

- **Description-item consistency (R23).** Does `quest_desc` mention any item ID not in this quest's tasks/rewards? Conversely, does it fail to explain a task item the player needs context for? Confirm every named item matches the config and every config item has a reason to be there.
- **Style drift (AP10).** Compare this quest's description structure to the last 2–3 quests. All following the same template ("Obtain [item]. This is needed for [next step].")? Vary the description mode — how-to, lore, tip, challenge. Reward amounts and shape vocabulary should vary too.
- **Narrative continuity (AP11).** If the description makes a forward reference ("you'll need this for the next quest") or difficulty claim ("the hardest craft so far"), verify the referenced quest exists and matches. Check tone consistency with the chapter's established voice.
- **Companion delegation (R47).** If `questbook_role == "companion"` and the description contains recipe patterns ("X + Y → Z"), note as INFO — consider delegating to EMI/JEI. Reverse: if `questbook_role == "tutorial"` and the description says "check EMI/JEI for the recipe", flag WARNING — tutorial mode should teach, not delegate.

---

## Chapter-Level Checks (after all nodes in a chapter are polished)

**Teaching order.** Confirm Teach-Then-Do (`mod-teaching-pacing.md §MP11`) and Tier Escalation (§MP12): for each mod mechanic, a teaching quest (checkmark/stat task + explanatory description) appears *before* the doing quest (item task applying it); within a material/tool tier, quests escalate cheapest → most expensive. Formal rules R14–R17 detect inversions statically; at generation time, read the chapter's quest list in dependency order and confirm no doing-quest precedes its teaching-quest and no high-tier quest appears before a lower-tier one. If you find an inversion, reorder `depends_on` in the outline and update the spec before the next chapter.

**AP9 hallucination cascade sweep.** After the batch, scan every item ID introduced during this chapter's generation against `items.json5` one more time — don't trust that each per-node check was sufficient.

**Progression architecture (Cycle 16, R101–R105).** Advisory at generation time, formal in Step 5:
- **R101** Multi-layer stage enforcement (Game Stages / Item Stages / Recipe Stages — defense in depth, not single-layer `depends_on`).
- **R102** Era-based architecture (>10 chapters → group into 2–5-chapter eras with intro/escalation/capstone).
- **R103** Tutorial anchor (first quest: no deps, orienting description, starter reward teaching the reward economy).
- **R104** Crafting variety (>60% same crafting method in a stage → mechanical monotony risk).
- **R105** 60% accessibility (casual main-line player reaches ≥60% of pack content).

Details: `progression-rules.md` §R101–R105.

**Progression architecture (Cycle 17, R106–R116).** Route by pack type:
- kitchen-sink: R107 (olive-shaped equipment distribution), R110 (mid-game density), R112 (vanilla enhancement layering)
- expert: R109 (forced anti-skip material binding), R115 (container-level recipe locking), R101
- adventure/RPG: R106 (dimensional progression naturalism, ≥3 same-dimension prerequisites before a dimension gate), R108 (gear-to-mob cross-dimension scaling; L1 heuristic fallback when DPS/HP data unavailable — namespace keyword tier inference + `BUILTIN_TOOL_TIER_MAP`; else `[unverified:combat_balance]`), R113 (multi-dimensional state synchronization)
- farming/lifestyle: R110, R111 (anti-forced-lifespan extension), R112
- all types: R114 (quest-to-stage reward bridge — chapter-final quests grant game stages; ERROR for expert, WARNING for semi-gated), R116 (advancement-as-progression-gate)

Details + tensions 7–9: `progression-rules.md` §Section G.

**Topology layout check (per chapter).** Load `progression-rules.md` §Section B, check R55–R64 for the chapter's chosen topology. Priority: R55 (topology-progression mode alignment; R41 early-game override: tutorial chapters depth ≤3, ≤15 quests may use `flexible` + `linear_chain`), R57 (hub size > max child size), R60 (shape count within topology's guideline range). Advisory at generation time; formal in Step 5.
