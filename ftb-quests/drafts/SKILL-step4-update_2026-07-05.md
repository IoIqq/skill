# SKILL.md Step 4 — Draft Update (2026-07-05)

## Overview

This draft replaces the **Step 4** section in `SKILL.md` (lines 357–386, from `### Step 4 — Polish one node at a time (the loop)` to the end of that section just before `### Step 5 — Whole-book verify & balance`).

Three new reference documents are now available:

- `reference/design/micro-patterns.md` — 34 micro-patterns (MP1–MP30 + PP1–PP6)
- `reference/design/anti-patterns.md` — 11 anti-patterns (AP1–AP11, including 3 AI-specific)
- `reference/design/progression-rules.md` — 23 progression validation rules (R1–R23)

The update embeds four mandatory reasoning checks into the Step 4 per-node loop so that the three core design failures — item cross-tier, sequence inversion, reward disconnection — are caught during generation rather than after.

---

## Replacement Content (Step 4)

> **Instructions:** Replace everything from `### Step 4 — Polish one node at a time (the loop)` through the end of that section (up to but not including `### Step 5 — Whole-book verify & balance`) with the following.

---

### Step 4 — Polish one node at a time (the loop)

**Anti-囫囵 rule:** do NOT write the tasks/rewards for the whole book at once. Iterate over the outline nodes — but **scale the loop to the book**: ≤~20 quests → one node at a time with per-node sign-off (steps 1–7 below); ~20–100 → batch by chapter (co-author a chapter's nodes in the spec, regenerate + validate once per chapter, sign off per chapter); >~100 → batch by chapter and skip per-node sign-off, revisiting only quests the validator flags. The incremental merge + `content_hash` still protect untouched quests across a batch. This is where the user 打磨 each task.

Before the first node, load `reference/design/anti-patterns.md §AP9–AP11` (AI-generation anti-patterns) as background context — these three risks (hallucination cascade, style homogenization, narrative inconsistency) are specific to AI-generated quest configs and inform every step below.

For each node:

1. **Pick one quest** (main-line order; side branches after their fork point). Say which one you're polishing.

2. **Co-author its content** — grill per the Step 2 interview discipline: ONE question with your recommended answer, wait for the user, then the next (task type + target + count → reward type + payload → description text). **Never dump a list of questions.** "帮我设计" → draft the content yourself, user approves/edits; "我要指定每个任务" → ask per task. Resolve mod mechanics / reward effects by checking the codebase or asking — never guess. Before writing a task/reward item, confirm its id is in `.ftbq-cache/items.json5` `all_item_ids` or `existing_quests.json5` `known_item_ids` (Step 1); if it isn't listed, ask the user to confirm it in JEI/EMI — **never invent an item id** (see "Verify, don't fabricate"). For a **collection quest / many-item batch**, resolve all the display names → ids in one call with `lookup_item.py <packroot> <name>…` (see "Batch item-id lookup") and write tasks from those results — don't grep `all_item_ids` N times. When writing the description text, follow **Quest text & description writing style** (near the top of this skill) — natural, concise prose, not label-value 要素式 checklists; the quest UI already shows the item/count/reward, so spend the description on the *why* and *how*.

   **Item reachability reasoning (before finalizing each task).** Before you commit an `ftbquests:item` task to the spec, answer this question internally: *"How does the player obtain this item at this point in the progression?"* Walk the quest's ancestor chain (the `depends_on` path back to the chapter root) and check whether the item's source dimension, tool tier, and recipe depth are all reachable from what the ancestors unlock. Use the builtin lookup tables in `reference/design/progression-rules.md §0` (dimension map, tool tier map, recipe depth heuristic) for common vanilla and cross-pack items; for pack-specific items, reason from the ancestor quests' rewards and the mod's known recipe ladder. If you cannot confirm reachability — the item comes from a dimension no ancestor opens, requires a tool no ancestor provides, or sits deeper in a recipe chain than the dependency depth allows — mark the task `[unverified:progression]` and surface it to the user before writing it. This is the generation-time counterpart to the Step 5 validation rules R1–R4 (`reference/design/progression-rules.md §1`); catching the problem here avoids a round-trip through validate-and-fix.

   **Reward bridge reasoning (after drafting each reward).** Once you have a reward drafted, answer: *"What does this reward lead the player to do next?"* A well-bridged reward appears as a task item in a dependent quest (the material bridge pattern, `reference/design/micro-patterns.md §MP14`), or is a universal bridge type (tool reward `§MP15`, XP drip `§MP16`). If the reward is an item that no downstream quest requires and it isn't a recognized universal bridge, it's a dead-end reward (`reference/design/anti-patterns.md §AP6`) — redesign it so the player has a clear next step. For terminal quests (capstone, chapter leaf) this check doesn't apply. The formal rule is R10–R13 in `reference/design/progression-rules.md §3`; at generation time you're doing the same reasoning by hand, one reward at a time.

3. **Update ONLY that quest** in `quests.spec.json5` (fill its `tasks`/`rewards`) and its `quest_desc` / `quest_subtitle` in the **primary locale's** lang file. Leave every other quest's empty `tasks: []` untouched. Translate to secondary locales in a dedicated pass after the primary is settled (Step 4 done) — don't block each node's sign-off on every locale; the generator's lang is add-only per locale, so mirror the primary's keys. If no translator, ship the primary and flag secondaries for the user/pack team. In the spec, references use `name` (within a chapter) or `<chapter>/<quest>` (across chapters); raw 16-hex tokens pass through for existing-pack linkage (see "Task linkage" below).

4. **Regenerate** — `python scripts/generate_quests.py <output_dir>`. The incremental merge keeps every other quest pristine (content_hash match → no-op) and re-emits only the quest you touched; in-game position edits to other quests are preserved regardless of mode. The ID-uniqueness check runs pre-emit, so a name clash fails fast before any file is written.

5. **Verify that one quest** — `python scripts/validate_quests.py <output_dir>/quests/` (fast; diagnostics carry `file:line:col`), then preview JUST that quest instead of reading the whole chapter file:
   ```bash
   python scripts/quest_detail.py <output_dir> <chapter>/<quest>
   ```
   It resolves the quest by name (via the spec's pack + the id formula) and prints only that quest's id/shape/deps/tasks/rewards/lang — token-saving vs. reading the whole chapter.

6. **AI generation self-check (per node).** After the quest passes validation and before presenting the summary, review it for the three AI-specific anti-patterns (`reference/design/anti-patterns.md §AP9–AP11`):
   - **Description-item consistency (R23).** Does the `quest_desc` mention any item ID that doesn't appear in this quest's tasks or rewards? Conversely, does the description fail to explain a task item that the player needs context for? The static rule in `reference/design/progression-rules.md §6` catches ID-level mismatches; at generation time, read the description you just wrote and confirm every named item matches the config, and every config item has a reason to be there.
   - **Style drift (AP10).** Compare this quest's description structure to the last 2–3 quests you polished. Are they all following the same template ("Obtain [item]. This is needed for [next step].")? Vary the description mode — how-to, lore, tip, challenge — so the chapter doesn't read like a form letter. Reward amounts and shape vocabulary should vary too (`reference/design/anti-patterns.md §AP10` for detection heuristics).
   - **Narrative continuity (AP11).** If this quest's description makes a forward reference ("you'll need this for the next quest") or a difficulty claim ("the hardest craft so far"), verify the referenced quest actually exists and matches. Check that the tone (casual / technical / lore-heavy) is consistent with the chapter's established voice — a tonal lurch between adjacent quests breaks the player's trust in the book as a guide.

7. **Show a focused summary** of just that quest (id, tasks, rewards, lang title/desc) and ask: keep & continue, or revise? Only advance to the next node when the user is happy with this one.

**Chapter-level teaching order check.** After all quests in a chapter are polished (or after a chapter batch), step back and verify the chapter's internal teaching sequence. The two patterns to confirm are Teach-Then-Do (`reference/design/micro-patterns.md §MP11`) and Tier Escalation (`reference/design/micro-patterns.md §MP12`): for each mod mechanic the chapter covers, a teaching quest (checkmark/stat task + long description explaining the concept) should appear *before* the doing quest (item task requiring the player to apply what was taught); and within a material or tool tier, quests should escalate from cheapest/simplest to most expensive/complex. The formal rules R14–R17 (`reference/design/progression-rules.md §4`) detect inversions statically; at generation time, read the chapter's quest list in dependency order and confirm that no doing-quest precedes its teaching-quest, and no high-tier quest appears before a lower-tier one. If you find an inversion, reorder the `depends_on` chain in the outline and update the spec before moving to the next chapter. This is also the moment to check for AP9 hallucination cascade (`reference/design/anti-patterns.md §AP9`) across the whole batch — scan every item ID introduced during this chapter's generation against `items.json5` one more time, rather than trusting that each per-node check was sufficient.

**Batching by chapter:** fill all of a chapter's quests' `tasks`/`rewards` in `quests.spec.json5`, then run `generate_quests.py` once + `validate_quests.py` once; use `generate_quests.py --dry-run` to preview the batch before committing. Run `quest_detail.py` per node only for quests that fail validation or that you want to spot-check. When batching, the item reachability and reward bridge reasoning (step 2) apply to each quest as you write it into the spec; the AI self-check (step 6) and the chapter-level teaching order check run once after the whole batch is written.

Re-run modes:

```bash
python scripts/generate_quests.py <output_dir>                  # default: overwrite skill-owned, preserve user-added
python scripts/generate_quests.py <output_dir> --mode preserve  # keep ALL on-disk edits
python scripts/generate_quests.py <output_dir> --mode ask       # prompt per conflict
python scripts/generate_quests.py <output_dir> --adopt          # first run on an existing pack
```

**Before `--mode ask` / `--adopt` on an existing pack**, check blast radius first: the manifest + validator catch quest dependency chains; if CodeGraph is available, also run `codegraph_impact` on the target quest files — it adds cross-file references (lang keys, `quest_links`) the manifest misses. Either source finding affected quests the other missed is a signal to stop and confirm with the user.

Reward tables (`reward_tables[]`), quest links (`quest_links[]`), and chapter images (`images[]`) can be authored whenever their owning quest comes up in the loop — add them to the spec and regenerate the same way. The `@<chapter>/<quest>.subkey` lang placeholders (subkeys: `title`, `quest_subtitle`, `quest_desc`, `chapter_subtitle`) are rewritten to `quest.<HEX>.subkey` on generate; with `format: "snbt"` the generator emits **inline** `title`/`subtitle`/`description` on the quest/chapter objects (the 1.20.1 variant — the only SNBT variant it emits; the 1.21.1 SNBT+lang variant is adopt-only, see the CRITICAL detection rule).

---

## Cross-Reference Update Recommendations

The following existing sections in SKILL.md should have references to the three new documents added. Each recommendation specifies the section, the insertion point, and the text to add.

### 1. "Quest progression, arrangement & authoring logic" section (line ~147)

**Insertion point:** After paragraph 6 (`progression_mode` discussion), before the "Linear vs nonlinear" subsection.

**Add:**

```
**Micro-level authoring patterns** — the 34 micro-patterns in `reference/design/micro-patterns.md` cover per-quest decisions that complement the spine models above: task combination formulas (MP1–MP5), dependency topologies (MP6–MP10), quest-internal pacing (MP11–MP13), reward bridging (MP14–MP18), and stage marking (MP19–MP23). Load `§Part 1` and `§Part 4` before Step 4 node generation; load `§Part 2` and `§Part 5` before Step 2 outline design.
```

### 2. "CRITICAL — read before generating" / ABSOLUTE RULE section (line ~99)

**Insertion point:** After the "Verification ladder" numbered list (item 5 "Final catch"), before the "In Step 4, before writing a task/reward item" paragraph.

**Add:**

```
**Generation-time progression checks.** Beyond item-ID verification, Step 4 now also reasons about item *reachability* (can the player get this at this point?), reward *bridging* (does this reward lead somewhere?), and teaching *order* (does the chapter teach before it tests?). The reasoning uses builtin lookup tables and rules R1–R4, R10–R13, R14–R17 from `reference/design/progression-rules.md`; anti-pattern context from `reference/design/anti-patterns.md §AP9–AP11`. These are embedded in the Step 4 per-node loop, not a separate checklist — see Step 4 for details.
```

### 3. "Quest text & description writing style" section (line ~32)

**Insertion point:** After the "Length budget" paragraph, before the next `---` separator.

**Add:**

```
**AI-specific style risks.** When generating many quests in sequence, watch for style homogenization (AP10) and narrative inconsistency (AP11) — both are documented in `reference/design/anti-patterns.md §AP9–AP11`. Step 4's self-check step catches these per-node; vary description mode (how-to / lore / tip / challenge) and reward structure across the chapter.
```

### 4. "Step 5 — Whole-book verify & balance" section (line ~389)

**Insertion point:** After the `validate_quests.py` command block, before the "Dev testing" blockquote.

**Add:**

```
The whole-book validation runs the full progression-rules pipeline (R1–R23, `reference/design/progression-rules.md`) — item reachability across the complete dependency graph, reward continuity across all chapters, teaching order for every chapter, and description consistency for every quest. The Step 4 per-node checks are a generation-time subset; Step 5 catches cross-quest and cross-chapter issues that only become visible once the full graph exists.
```

### 5. "Design principles" section (line ~137)

**Insertion point:** After the "Four questions" list, before "Quest progression, arrangement & authoring logic."

**Add:**

```
**Anti-patterns to design against.** Eleven recurring design mistakes are cataloged in `reference/design/anti-patterns.md` — from description-reality mismatch (AP1, the most damaging) through circular dependency deadlock (AP2) to the three AI-generation-specific risks (AP9–AP11). Load AP1–AP8 as background knowledge before Step 2; keep AP9–AP11 in mind during Step 4 generation.
```

### 6. "Sources" section (line ~587)

**Insertion point:** At the end of the existing Sources section, before the final blank line.

**Add:**

```
**Progression validation framework** developed 2026-07-05: `reference/design/progression-rules.md` (23 rules, R1–R23), `reference/design/micro-patterns.md` (34 micro-patterns, MP1–MP30 + PP1–PP6), `reference/design/anti-patterns.md` (11 anti-patterns, AP1–AP11). Grounded in the same 11-pack audit corpus as the design guide, plus cesspit.net expert-pack analysis, FTBTeam/FTB-Modpack-Issues #6447 player feedback, GTNH/E2E Extended design documents, and awesome-packdev community toolchain references.
```

---

## Sync Copy Report

The following alternate-path copies were checked:

| Path | Status |
|---|---|
| `C:\Users\Adm\.claude\skills\ftb-quests\` | **Not found** |
| `C:\Users\Adm\.codex\skills\ftb-quests\` | **EXISTS** — needs sync after SKILL.md is updated |
| `C:\Users\Adm\.zcode\skills\ftb-quests\` | **Not found** |

One sync copy requires updating: `C:\Users\Adm\.codex\skills\ftb-quests\SKILL.md`. The three new reference documents under `reference/design/` should also be synced to that location if the Codex copy maintains its own `reference/` tree.

---

## Design Rationale

**Why embedded, not a separate section.** The four mandatory checks are woven into the existing numbered workflow (steps 2, 6, and the chapter-level paragraph) rather than placed as a standalone "Mandatory Checks" section. This follows the existing SKILL.md pattern where verification is part of the step it belongs to (item-ID checking is inside step 2's co-authoring paragraph, not in a separate "verify IDs" section). A standalone checklist would be easy to skip; embedding makes each check a natural gate in the authoring flow.

**Why generation-time, not just Step 5.** The progression-rules.md document positions all 23 rules as Step 5 (whole-book validation). But three rules — R1–R4 item reachability, R10–R13 reward continuity, R14–R17 teaching order — are most valuable when applied *during* generation, because fixing a problem at generation time avoids a validate-and-fix round-trip. The draft creates a generation-time subset of these rules, using the same builtin lookup tables, and defers the full graph-wide checks to Step 5 where the complete dependency graph is available.

**Why AP9–AP11 are loaded before the loop.** The three AI-specific anti-patterns (hallucination cascade, style homogenization, narrative inconsistency) are systematic biases that affect every node. Loading them once as background context before the loop starts is more efficient than referencing them per-node, and matches the existing pattern where `design-guide.md §principles` is loaded before Step 2.

**Token cost.** The additions add approximately 40 lines of prose to the SKILL.md body (the per-node checks are 2 paragraphs in step 2, 1 paragraph in step 6, and 1 chapter-level paragraph). The three reference documents are loaded selectively — only the relevant sections, not the full 2,052 combined lines — so the token impact per session is modest.
