# SKILL.md Step 4 & Step 5 -- Draft Update (Cycle 3 Integration)

**Date:** 2026-07-07
**Base:** SKILL.md (current main) + Cycle 2 draft (SKILL-step4-update-cycle2_2026-07-06.md)
**Integration sources:** Cycle 3 findings -- R30-R32 (QA standards, progression-rules.md Phase 3 Cycle 3), MP33-MP34 (Advancement Gate + Loot Table Reward, micro-patterns.md Part 9), AP17-AP18 (XP-Level Relativity + Reward Desert, anti-patterns.md Phase 2 Cycle 3), Reviewer C scope correction (Step 5 = R1-R32)

---

## Changes from Cycle 2 draft (delta summary)

The Cycle 2 draft (2026-07-06) established the Step 4 mandatory reasoning, MP decision table, ATM Signature filter, and Step 5 full-graph checks against R1-R29 + AP1-AP16. Cycle 3 introduces four categories of additions:

1. **MP33 + MP34 added to the MP decision table** (Layer 6 -- Extended types). Advancement Gate and Loot Table Reward are now available during Step 4 node generation.
2. **R30-R32 added to Step 5 validation** (QA & Formatting Standards). R30 (Visual Hierarchy), R31 (XP-Level Reward Relativity), R32 (Chapter QA Coverage Heuristic) run as part of the whole-book pass.
3. **AP17 + AP18 added to Step 5 anti-pattern sweep.** XP-Level Reward Relativity and Reward Desert in Long Chains are now checked during the full-book pass.
4. **Rule count updated from R1-R29 to R1-R32.** Reviewer C's scope correction confirms Step 5 covers all 32 rules; Step 4 continues to use only the P0/P1/P2 subset.

Everything else from the Cycle 2 draft (mandatory item reachability reasoning, mandatory reward bridge reasoning, AI self-check step 6, chapter-level teaching order check, incremental dependency graph check, batching, ATM Signature filter, context loading strategy) remains unchanged and is carried forward verbatim.

---

## Section 1: Step 4 complete replacement text

> **Replacement scope:** from `### Step 4 -- Polish one node at a time (the loop)` to the line before `### Step 5 -- Whole-book verify & balance`. The following text replaces that entire range.

---

### Step 4 -- Polish one node at a time (the loop)

**Anti-囫囵 rule:** do NOT write the tasks/rewards for the whole book at once. Iterate over the outline nodes -- but **scale the loop to the book**: <=~20 quests -> one node at a time with per-node sign-off (steps 1-7 below); ~20-100 -> batch by chapter (co-author a chapter's nodes in the spec, regenerate + validate once per chapter, sign off per chapter); >~100 -> batch by chapter and skip per-node sign-off, revisiting only quests the validator flags. The incremental merge + `content_hash` still protect untouched quests across a batch. This is where the user polishes each task.

#### Context loading before the first node

Before the first node, load three reference slices -- not the full documents, but the slices relevant to generation:

1. **AI-generation anti-patterns** -- `reference/design/anti-patterns.md SSAP9-AP11` (the three risks specific to AI-generated quest configs: hallucination cascade, style homogenization, narrative inconsistency). These inform every step below. Also load SSAP14-AP16 summary (system safety: custom task black box, command reward side effects, quest state migration) and SSAP17-AP18 summary (XP-level reward relativity, reward desert in long chains) -- a few lines each, not the full case studies.

2. **Progression rules -- Step 4 subset** -- `reference/design/progression-rules.md SSExecution Priority Table` (the Execution Priority Table, ~30 lines) and `SS0` (the builtin lookup tables: `BUILTIN_DIMENSION_MAP`, `BUILTIN_TOOL_TIER_MAP`, `BUILTIN_ORE_REQUIREMENTS`, `estimate_recipe_depth_heuristic`). Do NOT load the full rule definitions for R1-R32; the Step 4 subset uses only the L1 builtin tables and the priority table's P0/P1/P2 classification. The full rules load in Step 5.

3. **Micro-pattern decision table** -- use the simplified decision table below (not the full `micro-patterns.md`). The decision table covers task combination (MP1-MP5), reward bridging (MP14-MP18), and extended types (MP27-MP34). Part 2 (dependency topologies MP6-MP10) and Part 5 (stage marking MP19-MP23) were already decided in Step 2 outline -- they don't need re-loading here.

#### MP selection decision table (per-node reference)

When generating each quest, select applicable patterns by walking this table top-to-bottom. A quest matches one entry from the Task Combination layer and may stack entries from the Reward Bridging layer. Layer 2 (dependency topology) and Layer 5 (stage marking) are inherited from the Step 2 outline -- don't re-decide them here.

**Layer 1 -- Task combination (pick one):**

- `tasks.count == 1 AND task.type == "item"` -> **MP1** Single-Item Gate (the default -- 90%+ of quests)
- `tasks.count >= 2 AND all tasks are "item" type AND quest is a convergence node (deps >= 3 from different mods)` -> **MP2** Multi-Item Synthesis Bundle. *Not* a checklist -- only use when the quest represents a cross-system crafting convergence. Three iron ingots + two planks is two MP1 quests, not one MP2.
- `task.type in ("checkmark", "stat", "observation")` -> **MP3** Acknowledgement Gate (tutorial/teaching quest with a longer description)
- `task.type in ("kill", "stat") AND quest is part of an escalation chain (marked in outline)` -> **MP4** Escalation Ladder. *ATM Signature -- see the ATM filter note below.*
- `tasks include both "dimension" and "item" types` -> **MP5** Dimension + Item Composite. Verify R1 (item from that dimension) passes.

**Layer 4 -- Reward bridging (stack as applicable):**

- `reward item appears as a task item in a downstream dependent quest` -> **MP14** Material Bridge (the strongest forward pull)
- `reward is a tool-type item (pickaxe, wrench, guide book, machine block)` -> **MP15** Tool Reward
- `pack_type == "kitchen-sink"` -> **MP16** XP Drip (add `{ type: "xp", xp: 10 }` as baseline). *ATM Signature -- see the ATM filter note below.* Expert and create packs do not use XP drip.
- `quest is a catalog hub AND most cell quests have no reward` -> **MP17** Hub Concentration
- `quest is a branch point AND reward determines the downstream path` -> **MP18** Choice Reward (expert/RPG meaningful choice)

**Layer 6 -- Extended types (pick as applicable):**

- `task.type == "fluid"` -> **MP27** Fluid Task Gate (fluid amount should be a multiple of the producing machine's output)
- `task.type == "forge_energy"` -> **MP28** Energy Threshold Gate (calibrate against best available generator at this stage)
- `reward.type == "command"` -> **MP29** Command Reward -- **must pass R28 Command Reward Safety Scan** before writing; see AP15 for idempotency and permission hazards
- `pack uses gamestage gating` -> **MP30** Gamestage Bridge (each stage grant must have a matching stage check)
- `task.type == "structure"` -> **MP31** Structure Discovery Gate (verify the target structure exists in world gen)
- `quest has min_tasks modifier` -> **MP32** min_tasks Modifier (overlap with MP9 at the task level; see Create: Astral's alternative recipe paths)
- `task.type == "advancement"` -> **MP33** Advancement Gate (verify the advancement ID exists in the pack's advancement data; pair with a visible reward for player feedback; can chain with MP29 + MP30 for gamestage-gated packs)
- `reward uses reward_tables[] or type: "random"/"loot"` -> **MP34** Loot Table Reward (calibrate weights so worst roll is still useful at this stage; complements MP14/MP15 deterministic bridges; avoids AP8 when weights are bounded)

#### ATM Signature filter

Five micro-patterns are marked as **ATM Signature** in the Scope Annotation Table (micro-patterns.md): MP4 (Escalation Ladder), MP16 (XP Drip), MP20 (Shape-as-Tier Signal), MP21 (Dimension-as-Stage-Gate), MP22 (Material-Tier Spine). Their core evidence comes entirely from AllTheMods packs (ATM-8/9/10/10-Sky). The concepts (escalation, XP rewards, shape semantics, dimension gating, material tiers) are transferable, but the specific implementations are ATM design choices, not universal best practices.

**Filtering rule:** if the current pack is not an ATM-series pack (not authored by AllTheMods, not explicitly modeled on ATM design philosophy), these five patterns are **reference only** -- do not apply them by default. Specifically:

- MP4 Escalation Ladder: only use if the pack has a mob-grind or repeatable-activity gameplay loop
- MP16 XP Drip: only use if the pack's reward philosophy is "generous" (ATM-style); skip for expert, create, or minimalist packs
- MP20 Shape-as-Tier Signal: only use if the chapter plan already calls for rich shape vocabulary (most non-ATM packs use 1-2 shapes)
- MP21 Dimension-as-Stage-Gate: applicable when dimension travel is the primary progression axis (most non-ATM packs use chapter groups or voltage tiers instead)
- MP22 Material-Tier Spine: only for ATM-style kitchen-sinks with a vertical material tier across dimensions

Similarly, `hide_dependency_lines` is an ATM preference (ATM-10 uses it 438 times), not a universal anti-clutter lever. Narrative and expert packs prefer `hide_until_deps_visible` for progressive reveal. Use `hide_dependency_lines` only when the layout family is kitchen-sink/ATM or when the chapter has high visual complexity (hub with >3 dependents, long cross-column lines).

For each quest, record the selected MP patterns in a brief inline note in the spec (e.g., `// MP1 + MP14 + MP15` or `// MP33 + MP14 + MP34`) -- this helps the Step 5 reviewer understand the design intent and catches misapplied patterns.

---

For each node:

1. **Pick one quest** (main-line order; side branches after their fork point). Say which one you're polishing.

2. **Co-author its content** -- grill per the Step 2 interview discipline: ONE question with your recommended answer, wait for the user, then the next (task type + target + count -> reward type + payload -> description text). **Never dump a list of questions.** "帮我设计" -> draft the content yourself, user approves/edits; "我要指定每个任务" -> ask per task. Resolve mod mechanics / reward effects by checking the codebase or asking -- never guess. Before writing a task/reward item, confirm its id is in `.ftbq-cache/items.json5` `all_item_ids` or `existing_quests.json5` `known_item_ids` (Step 1); if it isn't listed, ask the user to confirm it in JEI/EMI -- **never invent an item id** (see "Verify, don't fabricate"). For a **collection quest / many-item batch**, resolve all the display names -> ids in one call with `lookup_item.py <packroot> <name>...` (see "Batch item-id lookup") and write tasks from those results -- don't grep `all_item_ids` N times. When writing the description text, follow **Quest text & description writing style** (near the top of this skill) -- natural, concise prose, not label-value checklists; the quest UI already shows the item/count/reward, so spend the description on the *why* and *how*.

   **Mandatory item reachability reasoning (before finalizing each task).** Before you commit an `ftbquests:item` task to the spec, you **must** answer this question -- silently, as an internal check -- and surface the result to the user if it fails:

   > "The player needs this item right now -- how do they get it?"

   Walk the quest's ancestor chain (the `depends_on` path back to the chapter root) and check the task item against the **Step 4 Execution Priority subset** from `reference/design/progression-rules.md SSExecution Priority Table`:

   - **R1 Dimension-Reachability (L1 only):** check the item against `BUILTIN_DIMENSION_MAP` (SS0). If the item is in the map and its dimension is not in the ancestor chain's unlocked dimensions, this is a **P1 item cross-tier** violation -- stop and surface it. If the item is not in the map, mark `[unverified:dimension]` and continue.
   - **R2 Tool-Tier (L1 only):** check against `BUILTIN_TOOL_TIER_MAP` and `BUILTIN_ORE_REQUIREMENTS` (SS0). If the item requires a tool/mining level that no ancestor provides, this is a **P2 item cross-tier** violation -- mark `[unverified:tool_tier]` and surface it.
   - **R3 Recipe Depth (L1 heuristic):** run `estimate_recipe_depth_heuristic` (SS0) on the item id. If the estimated recipe depth exceeds the quest's dependency depth + 2 (the ALLOWANCE), flag as **P2 potential depth mismatch** -- mark `[unverified:recipe_depth]`.
   - **R4 Stage Boundary (degraded):** check whether the item appears as a task or reward in any already-generated ancestor quest. If the item only appears in later chapters' tasks (not yet generated), flag as **P2 potential stage boundary violation** -- mark `[unverified:stage]`.

   When an L1 check **hits** (the item is in the builtin table and fails the check), this is a generation-blocking finding: fix the task item, adjust the dependency chain, or get explicit user confirmation before writing. When L1 **misses** (the item is not in any builtin table), the `[unverified]` tag is a deferred check -- it will be resolved in Step 5 when the full graph is available. The goal is to catch the three hardest progression errors (item cross-tier, sequence inversion, reward disconnection) at generation time, not after a validate-and-fix round-trip.

   For pack-specific items not covered by the L1 tables, reason from the ancestor quests' rewards and the mod's known recipe ladder. If you cannot confirm reachability, mark `[unverified:progression]` and surface it to the user before writing.

   **Mandatory reward bridge reasoning (after drafting each reward).** Once you have a reward drafted, you **must** answer this question:

   > "What does this reward lead the player to do next?"

   - **R10 (reverse / backward check):** does the reward item appear as a task item in any already-generated quest that depends on this one's ancestors? More practically: when generating the *next* quest, check whether its task items match this quest's rewards (the Material Bridge pattern, MP14). If the reward is an item that no downstream quest requires and it isn't a recognized universal bridge type (tool reward MP15, XP drip MP16), it's a dead-end reward (AP6) -- redesign it so the player has a clear next step.
   - **R28 Command Reward Safety:** if the reward type is `command`, execute the R28 safety scan **before** writing it to the spec: check the command string against `FORBIDDEN_COMMANDS` (ERROR -- block write), `HIGH_RISK_COMMANDS` (WARNING -- surface to user), and `IDEMPOTENCY_RISK` (INFO -- note for the user). See `reference/design/progression-rules.md SSR28` for the exact regex patterns. Command rewards are the single highest-risk reward type (AP15) -- prefer standard reward types (`item`, `xp`, `loot`) whenever possible.
   - **R31 XP-Level Reward Relativity (pre-check):** if the reward type is `xp_levels`, check whether this quest is a milestone/capstone node. Non-milestone `xp_levels` rewards create value that drifts with player level (AP17, from Craftoria #289). If the quest is not a milestone, suggest replacing `xp_levels` with a flat `xp` reward, or surface the AP17 risk to the user.
   - **Dead-end reward detection:** if the reward is a material item and no dependent quest in the outline lists it as a task, flag AP6 risk and suggest either (a) changing the reward to a bridge item that a downstream quest needs, or (b) adding a dependent quest that uses it. For terminal quests (capstone, chapter leaf with no dependents) this check doesn't apply.

   The formal rules are R10-R13 in `reference/design/progression-rules.md SS3`; at generation time you're doing the same reasoning by hand, one reward at a time, using backward matching (task -> ancestor reward) because forward matching (reward -> dependent task) requires quests that haven't been generated yet. The Step 5 whole-book pass runs the forward check.

3. **Update ONLY that quest** in `quests.spec.json5` (fill its `tasks`/`rewards`) and its `quest_desc` / `quest_subtitle` in the **primary locale's** lang file. Leave every other quest's empty `tasks: []` untouched. Translate to secondary locales in a dedicated pass after the primary is settled (Step 4 done) -- don't block each node's sign-off on every locale; the generator's lang is add-only per locale, so mirror the primary's keys. If no translator, ship the primary and flag secondaries for the user/pack team. In the spec, references use `name` (within a chapter) or `<chapter>/<quest>` (across chapters); raw 16-hex tokens pass through for existing-pack linkage (see "Task linkage" below).

4. **Regenerate** -- `python scripts/generate_quests.py <output_dir>`. The incremental merge keeps every other quest pristine (content_hash match -> no-op) and re-emits only the quest you touched; in-game position edits to other quests are preserved regardless of mode. The ID-uniqueness check runs pre-emit, so a name clash fails fast before any file is written.

5. **Verify that one quest** -- `python scripts/validate_quests.py <output_dir>/quests/` (fast; diagnostics carry `file:line:col`), then preview JUST that quest instead of reading the whole chapter file:
   ```bash
   python scripts/quest_detail.py <output_dir> <chapter>/<quest>
   ```
   It resolves the quest by name (via the spec's pack + the id formula) and prints only that quest's id/shape/deps/tasks/rewards/lang -- token-saving vs. reading the whole chapter.

6. **AI generation self-check (per node).** After the quest passes validation and before presenting the summary, review it for the AI-specific anti-patterns (`reference/design/anti-patterns.md SSAP9-AP11`):
   - **Description-item consistency (R23).** Does the `quest_desc` mention any item ID that doesn't appear in this quest's tasks or rewards? Conversely, does the description fail to explain a task item that the player needs context for? The static rule in `reference/design/progression-rules.md SS6` catches ID-level mismatches; at generation time, read the description you just wrote and confirm every named item matches the config, and every config item has a reason to be there. **R23 is P0 -- a description-item mismatch blocks the spec write.**
   - **Style drift (AP10).** Compare this quest's description structure to the last 2-3 quests you polished. Are they all following the same template ("Obtain [item]. This is needed for [next step].")? Vary the description mode -- how-to, lore, tip, challenge -- so the chapter doesn't read like a form letter. Reward amounts and shape vocabulary should vary too (`reference/design/anti-patterns.md SSAP10` for detection heuristics).
   - **Narrative continuity (AP11).** If this quest's description makes a forward reference ("you'll need this for the next quest") or a difficulty claim ("the hardest craft so far"), verify the referenced quest actually exists and matches. Check that the tone (casual / technical / lore-heavy) is consistent with the chapter's established voice -- a tonal lurch between adjacent quests breaks the player's trust in the book as a guide.
   - **Custom task safety (AP14).** If this quest uses a `custom` task type, verify that (a) the custom task handler's type ID is explicitly provided by the user (not invented by the agent -- AP14's black-box risk), (b) the quest description explicitly states what the player needs to do (since the quest UI won't show it), and (c) the quest is flagged as `[unverified:custom_task]` for Step 5a load-test verification. AI should **never proactively create custom tasks** -- only use them when the pack author explicitly requests and provides the handler details.
   - **Reward desert check (AP18, pre-check).** If this quest is part of a linear chain of 3+ consecutive quests, check whether the chain has any rewards at all between them. A streak of unrewarded quests in a linear chain creates a "reward desert" (AP18, from Craftoria #231 Powah chapter). If the chain has 3+ quests with no rewards, flag the risk and suggest adding at least an XP drip or minor item reward to break the desert.

7. **Show a focused summary** of just that quest (id, tasks, rewards, lang title/desc, selected MP patterns) and ask: keep & continue, or revise? Only advance to the next node when the user is happy with this one.

**Chapter-level teaching order check.** After all quests in a chapter are polished (or after a chapter batch), step back and verify the chapter's internal teaching sequence. The two patterns to confirm are Teach-Then-Do (`reference/design/micro-patterns.md SSMP11`) and Tier Escalation (`reference/design/micro-patterns.md SSMP12`): for each mod mechanic the chapter covers, a teaching quest (checkmark/stat task + long description explaining the concept) should appear *before* the doing quest (item task requiring the player to apply what was taught); and within a material or tool tier, quests should escalate from cheapest/simplest to most expensive/complex. The formal rules R14-R17 (`reference/design/progression-rules.md SS4`) detect inversions statically; at generation time, read the chapter's quest list in dependency order and confirm that no doing-quest precedes its teaching-quest, and no high-tier quest appears before a lower-tier one. If you find an inversion, reorder the `depends_on` chain in the outline and update the spec before moving to the next chapter. This is also the moment to check for AP9 hallucination cascade (`reference/design/anti-patterns.md SSAP9`) across the whole batch -- scan every item ID introduced during this chapter's generation against `items.json5` one more time, rather than trusting that each per-node check was sufficient.

**Incremental dependency graph check.** After all quests in a chapter are polished, perform a quick structural check on the chapter's dependency graph:

- **R5 (incremental cycle detection):** walk the chapter's `depends_on` graph (which should be a DAG from the Step 2 outline) and verify no cycle was introduced during generation. The outline should already be acyclic, but manual edits during the Step 4 loop can accidentally introduce cycles -- especially when adding cross-references or re-ordering quests. If a cycle is found, identify the offending edge and ask the user to break it.
- **R6 (local unreachable check):** verify every non-root quest in the chapter has at least one dependency path to a root quest (a quest with no dependencies). Flag any quest whose dependencies all point to optional or secret quests without a non-optional bypass -- this is the mandatory-quest-blocked-by-optional-gate pattern (R7).
- **R7 (optional-gate-mandatory, chapter-wide recheck):** confirm no mandatory quest depends solely on optional quests. This was checked per-node in step 2, but the chapter-level view can reveal chains where an optional quest is an indirect prerequisite (A mandatory -> B optional -> C optional, making A unreachable if B is skipped).

**Batching by chapter:** fill all of a chapter's quests' `tasks`/`rewards` in `quests.spec.json5`, then run `generate_quests.py` once + `validate_quests.py` once; use `generate_quests.py --dry-run` to preview the batch before committing. Run `quest_detail.py` per node only for quests that fail validation or that you want to spot-check. When batching, the mandatory item reachability and reward bridge reasoning (step 2) apply to each quest as you write it into the spec; the AI self-check (step 6) and the chapter-level teaching order check run once after the whole batch is written.

Re-run modes:

```bash
python scripts/generate_quests.py <output_dir>                  # default: overwrite skill-owned, preserve user-added
python scripts/generate_quests.py <output_dir> --mode preserve  # keep ALL on-disk edits
python scripts/generate_quests.py <output_dir> --mode ask       # prompt per conflict
python scripts/generate_quests.py <output_dir> --adopt          # first run on an existing pack
```

**Before `--mode ask` / `--adopt` on an existing pack**, check blast radius first: the manifest + validator catch quest dependency chains; if CodeGraph is available, also run `codegraph_impact` on the target quest files -- it adds cross-file references (lang keys, `quest_links`) the manifest misses. Either source finding affected quests the other missed is a signal to stop and confirm with the user.

Reward tables (`reward_tables[]`), quest links (`quest_links[]`), and chapter images (`images[]`) can be authored whenever their owning quest comes up in the loop -- add them to the spec and regenerate the same way. The `@<chapter>/<quest>.subkey` lang placeholders (subkeys: `title`, `quest_subtitle`, `quest_desc`, `chapter_subtitle`) are rewritten to `quest.<HEX>.subkey` on generate; with `format: "snbt"` the generator emits **inline** `title`/`subtitle`/`description` on the quest/chapter objects (the 1.20.1 variant -- the only SNBT variant it emits; the 1.21.1 SNBT+lang variant is adopt-only, see the CRITICAL detection rule).

---

## Section 2: Step 5 complete replacement text

> **Replacement scope:** from `### Step 5 -- Whole-book verify & balance` to the line before `### Step 5a -- Load-test in-game`. The following text replaces that entire range.

---

### Step 5 -- Whole-book verify & balance

Per-node validation already ran inside the Step 4 loop; this is the final whole-book pass once every node is polished. Run the validation script (the quests root is `<output_dir>/quests/`):
```bash
python scripts/validate_quests.py <output_dir>/quests/
python scripts/validate_quests.py <output_dir>/quests/ --strict       # also: --fix (autofix), --json (CI)
```
If the script is unavailable, see reference SS15 for the full diagnostics catalog and self-check against it.

The whole-book validation runs the full progression-rules pipeline -- all 32 rules (R1-R32, `reference/design/progression-rules.md`) plus 18 anti-patterns (AP1-AP18, `reference/design/anti-patterns.md`). The Step 4 per-node checks are a generation-time subset using only local data and L1 builtin tables; Step 5 catches cross-quest and cross-chapter issues that only become visible once the full graph exists. The Execution Priority Table (`progression-rules.md SSExecution Priority Table`) classifies every rule into Step 4 (generation-time), Step 5 (whole-book), or external-script categories; Step 5 runs all rules classified as Step 5 plus a re-run of the Step 4 rules on the full data.

> **Dev testing -- scope it.** When you change skill code (scripts/, ftbq/) during a session, avoid running the full test suite on every iteration. Run only the test module(s) that cover what you touched -- see the "Test -> source map" in `CONTRIBUTING.md`. Reserve the full suite for pre-push / pre-release / shared-surface changes (the JSON5 parser, the canonical emitter, the `generate()` signature).

After the `validate_quests.py` command block and before the summary printout, perform these additional whole-book checks:

**Full-graph structural checks (run after the validator passes):**

- **R5 -- Circular Dependency Detection (complete DFS):** run a full DFS cycle detection across the entire book's dependency graph, including cross-chapter references. The Step 4 incremental check only caught cycles within the chapter being generated; Step 5 catches cycles that span chapters (e.g., chapter A's quest depends on chapter B's quest, which transitively depends back on chapter A). Report any cycle found with the full path.

- **R6 -- Unreachable Quest Detection (complete reachability):** for every non-root quest in the book, verify at least one dependency path exists from a root quest (no dependencies) to this quest, where no step in the path is blocked by an optional-gate-mandatory pattern (R7) or an undiscoverable secret. Flag quests whose only paths go through optional or secret prerequisites.

- **R10 -- Reward Bridge Verification (forward check):** for every non-terminal quest (a quest that has dependents), check whether its reward items appear as task items in at least one dependent quest. This is the forward-direction check that Step 4 couldn't do (Step 4 only did the backward check: task -> ancestor reward). Flag dead-end rewards (AP6) where a quest's reward item is never required by any downstream quest and isn't a recognized universal bridge type.

- **R28 -- Command Reward Safety Scan (full sweep):** if any quest in the book has a command reward, run the complete R28 scan (FORBIDDEN_COMMANDS, HIGH_RISK_COMMANDS, IDEMPOTENCY_RISK, {p} placeholder check, cross-dimension check) from `progression-rules.md SSR28`. This catches command rewards that were added during batch generation and may have been missed by the per-node check, or command rewards from existing pack content that the `--adopt` / `--mode preserve` flow brought in.

- **AP14 -- Custom Task Black Box check:** for every quest with a `custom` task type, verify that the quest is flagged `[unverified:custom_task]` (meaning the user confirmed the handler exists) and that the quest description explicitly states what the player needs to do. Downgrade R6/R20 to INFO for quests containing custom tasks -- their completability cannot be statically verified. If a custom task quest is non-optional and has mandatory dependents, flag as WARNING: a black-box quest gating mandatory progression is an AP14 + AP3 risk.

- **AP16 -- Quest State Migration (update scenarios only):** when running in `--adopt` or `--mode preserve` on an existing pack, check for stale dependency references -- quest IDs that exist in the on-disk config's `dependencies` arrays but no longer correspond to any quest in the generated or preserved output. This is the update-compatibility check that catches the "deleted quest leaves dangling reference" failure mode.

**QA & formatting standards checks (run after structural checks pass):**

- **R30 -- Quest Visual Hierarchy & Size Consistency:** for every quest, check that its `size` and `shape` match its semantic role in the dependency graph. Milestone/capstone quests (high fan-in, distinctive shape) should have `size >= 1.5`; routine intermediate quests should have `size: 1.0` and the chapter's default shape; optional/side quests should be visually smaller or differently shaped. Flag quests where the size/shape contradicts the quest's importance -- e.g., a routine item quest with `size: 2.0 hexagon` (over-signaling) or a capstone convergence quest with `size: 1.0 circle` (under-signaling). Source: Monifactory CONTRIBUTING.md "Larger quests should be reserved for important milestones" + ATM-10 MP20 Shape-as-Tier Signal.

- **R31 -- XP-Level Reward Relativity:** scan all quests with `xp_levels` rewards. For each, check whether the quest is a milestone/capstone (high fan-in, distinctive shape, convergence point). If a non-milestone quest uses `xp_levels`, flag as WARNING: the reward's real value depends entirely on the player's level at claim time (AP17, from Craftoria #289), creating inconsistent experiences across playthroughs. Suggest replacing with flat `xp` for non-milestone quests, or moving the `xp_levels` reward to the nearest downstream milestone.

- **R32 -- Chapter QA Coverage Heuristic:** for each chapter, compute four "untested" indicators that suggest the chapter may not have been playtested (derived from the Enigmatica 10 zero-complaint phenomenon, the Monifactory CONTRIBUTING.md testing standards, and the FTB Architect's Exodus counter-example):
  1. **Dead-end quest ratio:** percentage of non-terminal quests whose rewards don't bridge to any dependent quest's tasks (R10 failures). Threshold: >15% is WARNING.
  2. **Empty description ratio:** percentage of quests with no `quest_desc` or only boilerplate text. Threshold: >25% is WARNING (Monifactory CONTRIBUTING.md requires substantive descriptions).
  3. **Dependency orphan count:** quests that depend only on optional or secret quests without a non-optional path. Threshold: >0 is WARNING.
  4. **Zero-optional rate:** chapters with 0 `optional: true` quests across 30+ quests may lack side content and exploration space. Threshold: INFO.

  If a chapter triggers 2+ of these 4 indicators, flag the chapter as `[untested: likely]` and recommend a focused playtest pass before deployment. This is the generation-time counterpart to the Enigmatica 10 QA process that produced zero quest design complaints -- systematic checking before the player ever sees the content.

Then print a summary (in the user's language -- see "Language -- match the user"):
```
Generated FTB Quests config (modern JSON5):
   N chapters   N quests   N tasks   N rewards   N reward tables   N lang entries
   Output: {dir}/quests/   (clean, copy-ready)
   New pack: copy <output_dir>/quests/ into <packroot>/config/ftbquests/quests/
   Existing pack: python scripts/generate_quests.py <output_dir> --deploy <packroot> --yes
                  (merges additive files, backs up overwritten originals -- see Step 5b)
   then in-game /ftbquests editing_mode
   If titles appear blank: you're on the inline-text (older .snbt) version -- see reference SS12.
   QA coverage: N/M chapters passed R32 heuristic (see above for flagged chapters).
```

**Balance review (optional):** after the summary, offer to re-grill the user about pacing against the generated config -- early quests too trivial/grindy? (recommend 3-5 min/quest first hour); rewards scale with effort? (~2x time-value); choke points? (every 3rd quest an alternative path); mod progression natural? (unlock when players want them). Also flag any AP17 (xp_levels on non-milestones) or AP18 (reward deserts in linear chains) findings from the QA checks above.

---

## Section 3: Sources paragraph append

> **Action:** append the following paragraph at the end of the existing `## Sources` section in SKILL.md. Do not delete or modify the existing Sources text.

**Cycle 3 progression framework update** (2026-07-07): progression-rules.md expanded to 32 rules (R1-R32, adding R30-R32 QA & formatting standards: visual hierarchy/size consistency, XP-level reward relativity, chapter QA coverage heuristic); anti-patterns.md expanded to 18 anti-patterns (AP1-AP18, adding AP17 XP-level reward relativity from Craftoria #289 and AP18 reward desert in long chains from Craftoria #231); micro-patterns.md expanded to 34 micro-patterns + 7 player-perspective patterns (MP1-MP34 + PP1-PP7, adding MP33 Advancement Gate from Enigmatica 10 and MP34 Loot Table Reward from Craftoria). Step 5 now validates all 32 rules including the new R30-R32 QA standards. Step 4's MP decision table includes MP33 and MP34 in the extended types layer. R31 pre-check added to Step 4 reward bridge reasoning. AP18 pre-check added to Step 4 AI self-check (step 6).

---

## Section 4: Design rationale

### Why MP33 and MP34 are in the Step 4 decision table, not just Step 5

MP33 (Advancement Gate) and MP34 (Loot Table Reward) are task/reward types that the agent must *choose* during generation -- they are not detectable after the fact by structural validation. A quest that should use an advancement task but uses an item task instead is not a "broken" quest (the validator won't flag it), but it misses the design intent (auto-completing checkpoint, no item tax). Similarly, a quest that should use a loot table but gives a deterministic item reward is valid but misses the excitement and AP8-avoidance benefits. These patterns must be selected at generation time (Step 4), not checked at validation time (Step 5).

### Why R31 gets a Step 4 pre-check but R30 and R32 are Step 5 only

R31 (XP-Level Reward Relativity) has a cheap per-node check: "is this quest a milestone, and does it use `xp_levels`?" This can be answered with local data (the quest's shape/size and its reward type) during Step 4. R30 (Visual Hierarchy) requires comparing the quest's size/shape against the full chapter's semantic structure -- which quests are milestones, which are routine -- and that comparison is only reliable after the entire chapter exists. R32 (QA Coverage Heuristic) is inherently chapter-wide (dead-end ratio, empty description ratio, orphan count) and cannot be meaningfully computed per-node.

### Why AP18 gets a Step 4 pre-check

AP18 (Reward Desert in Long Chains) was observed in Craftoria #231 where the Powah chapter has 3 tiers of reactors with no rewards between them. This is detectable during generation: when writing the Nth consecutive quest in a linear chain with no reward, the agent can flag the risk and suggest a break. The pre-check is a heuristic (3+ consecutive unrewarded quests in a linear chain) rather than a formal count, because the chain's full extent may not be known until the chapter is complete. Step 5 runs the formal check.

### Reviewer C scope correction

Reviewer C noted that the Cycle 2 draft referenced "R1-R29" in Step 5, but the progression-rules.md now contains 32 rules (R1-R32). This draft corrects the scope to R1-R32. The new rules R30-R32 are classified as Step 5 (whole-book) in the Execution Priority Table because they require full-graph or chapter-wide data. They do not change the Step 4 subset except for R31's pre-check (which uses only local data).

### Context window update

The Cycle 3 additions are compact: MP33 and MP34 add ~2 lines each to the decision table; R30-R32 add ~15 lines to Step 5; AP17-AP18 add ~3 lines each to the anti-pattern summaries. The total context window impact is approximately +500 tokens for Step 4 loading and +1,500 tokens for Step 5 loading -- well within the existing budget established by the Cycle 2 draft.

---

## Section 5: Sync copy status

| Path | Status |
|---|---|
| `C:\Users\Adm\.codex\skills\ftb-quests\` | **EXISTS** -- needs sync after SKILL.md is updated |

One sync copy requires updating after the Step 4/5 replacement is applied.
