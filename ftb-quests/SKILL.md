---
name: ftb-quests
description: >
  Generate, edit, and validate FTB Quests configuration files (JSON5 on current
  main, SNBT on 1.20.1 — format detected from the pack's files, not the MC version)
  for Minecraft modpacks. Use for ANY task involving quest configs: creating new
  quest lines, modifying/fixing existing quests, adjusting chapter layouts and
  coordinates, validating configs, or auditing packs. Triggers on: "FTB任务",
  "FTB quests", "任务配置", "quest config", "任务线", "生成任务", "create quests",
  "改任务", "修任务", "调整布局", "quest layout", "edit quest", "fix quest",
  "SNBT", "quests.json5", any request touching config/ftbquests/ files.
user-invocable: true
argument-hint: "整合包名称或项目路径 (optional)"
---

# FTB Quests Configuration Generator

Generate and edit FTB Quests configs that **actually load**. This file is the protocol — the routing table at the bottom tells you where every detail lives. Load only what the current step needs.

## Language — match the user

Conduct all interaction in the user's language. This governs how you talk, not the generated quest text (that follows the `locales` settled in the interview).

---

## Edit Mode — modifying existing quests (FAST PATH, read this first)

**If the user wants to change, fix, or adjust quests that already exist in a pack, use this path. Do NOT run the full 5-step generation protocol.**

1. **Orient** — confirm the pack path, then:
   ```bash
   python scripts/index_quests.py <packroot>      # builds .ftbq-cache/existing_quests.json5
   python scripts/pack_briefing.py <packroot>     # compact summary, NOT raw file reads
   ```
2. **Locate** — identify the target quest. Use `python scripts/quest_detail.py <output_dir> <chapter>/<quest>` to inspect one quest without reading the whole chapter. Read the current file state before any edit (never edit from memory).
3. **Modify** — edit the quest in `quests.spec.json5` (preferred) or directly in the config file. Rules:
   - Item IDs must come from `.ftbq-cache/items.json5` `all_item_ids` or `existing_quests.json5` `known_item_ids` — never invent one (Zero Hallucination below).
   - Coordinate/shape/size changes must follow the layout rules — load `reference/design/layout-quickref.md` before touching x/y/shape/size.
   - Dependency changes: check for cycles and orphans; run the validator after.
4. **Regenerate** — `python scripts/generate_quests.py <output_dir> --mode preserve` (protects all other quests via content_hash).
   *If no `quests.spec.json5` exists (hand-written pack or external tool output), skip this step — you edited the config file directly in step 3. Go straight to Validate.*
5. **Validate** — `python scripts/validate_quests.py <output_dir>/quests/` + re-run `quest_detail.py` on the touched quest. Confirm no new diagnostics. For direct config edits without an output_dir, point the validator at the pack's `config/ftbquests/` directory instead.

Skip the interview, skip the scaffold, skip the spine design. The user knows what they want changed — help them change it safely.

---

## CRITICAL — format detection (the one thing to get exactly right)

**Pick the format from the on-disk files, not the MC version:**

| Serialization | Localization | Observed in |
|---|---|---|
| **SNBT** (`.snbt`, no commas, TAB, `0.0d`/`1L` suffixes) | **inline** `title:`/`description:` on quest objects | MC 1.20.1 packs (FTB Quests 2001.x) |
| **JSON5** (`.json5`, commas, bare numbers) | **lang files** (`lang/<locale>/quests.json5`) | current `main` (MC 1.21.x, FTB Quests 26.x) |

Set `format: "json5"` (default) or `format: "snbt"` in the spec. Detection rule: check one existing file — commas + lang dir → json5; no commas + `0.0d` + inline titles → snbt (1.20.1 inline); `.snbt` with NO inline text but `lang/<locale>.snbt` → the 1.21.1 SNBT+lang variant, **adopt-only** (never generate it).

**Fatal errors that silently fail** (full list + correct examples: `reference/ftb-quests-reference.md` §1, §12):

- ❌ Commas in SNBT / missing commas in JSON5 — each format is the opposite of the other.
- ❌ Type suffixes (`0.0d`, `1L`) in JSON5, or bare numbers in SNBT.
- ❌ Type-name style: SNBT uses SHORT ids (`type: "item"`); JSON5 uses prefixed (`type: "ftbquests:item"`).
- ❌ Bare-string items in JSON5 (`item: "minecraft:oak_log"`) — dropped on load. Must be `{ id: "...", count: 1 }`. (Bare strings ARE valid in SNBT.)
- ❌ Item quantity inside the `item` object — FTB reads the SIBLING `count` field. Write `item: { id: "...", count: 1 }, count: 3`.
- ❌ `ftbquests:xp` task without `points` — throws on load. Always set `points: true|false`.
- ❌ 16-hex id with top digit `8`–`F` — `Long.parseLong` throws; FTB silently regenerates the id, breaking all dependencies. The generator masks the top bit; never hand-write `8`–`F` ids.
- ⚠️ Inline `title:`/`description:` — ignored in JSON5/lang format, required in SNBT+inline format.

---

## ⛔ ZERO HALLUCINATION — 严禁脑补

**You MUST NOT invent, guess, or assume:** item IDs, recipes/crafting routes, task content, mod mechanics, progression order, block/entity/fluid IDs, reward items, quantities, or FTB Quests fields/types.

**Core principle: 宁可空着问用户，不可瞎猜写进 spec.** Anything unverifiable gets marked `[unverified:<category>]` (e.g. `[unverified:recipe]`, `[unverified:item_id]`, `[unverified:progression]`), surfaced to the user, and only written after confirmation.

**Verification ladder (strongest → weakest):**
1. Existing pack's quests → `.ftbq-cache/existing_quests.json5` `known_item_ids` (verified-loaded in THIS pack)
2. Mod jars' lang files → `.ftbq-cache/items.json5` `all_item_ids` (best-effort: not every registered item has a lang key)
3. Format/field behavior → `reference/ftb-quests-reference.md`
4. Recipes & mod mechanics → ask the user to confirm in JEI/EMI
5. Final catch → Step 5a in-game load-test

Before writing any task/reward item: confirm its id is in the cache. For batches, resolve all names in one call via `python scripts/lookup_item.py <packroot> <name>…` — never grep per item, never guess.

**File mutation discipline:** read the target file's current state before EVERY edit. Never edit from memory or stale context. Check a file exists before creating it. Data before design: gather evidence before writing quest content that references mod mechanics.

**Self-check before every spec write:** "这个值是我从 verification ladder 查到的，还是我脑子里编的？" 后者 → **停，问用户。**

---

## Protocol (generation flow)

Skip or merge steps as the task warrants. The format rules above are the one thing to follow exactly.

### Fast paths

- **Small job (≤~5 quests):** skip Step 2 interview + Step 3 skeleton. Run Step 1, co-author directly in the spec, regenerate, validate, load-test.
- **Complete spec already exists:** skip Steps 1–4. Run `generate_quests.py`, jump to Step 5 → 5a → 5b.
- **Editing existing quests:** use Edit Mode above, not this protocol.

### Step 1 — Index & detect

Detect the format from one existing file. Build the caches, then orient from ONE command:
```bash
python scripts/extract_mods.py <packroot>      # -> .ftbq-cache/mods.json5
python scripts/extract_items.py <packroot>     # -> .ftbq-cache/items.json5 + item_names.json5
python scripts/index_quests.py <packroot>      # -> .ftbq-cache/existing_quests.json5
python scripts/pack_briefing.py <packroot>     # compact summary — do NOT read caches raw
```
Open Step 2 with what you indexed: "Detected N mods — suggested chapters: …. Existing pack has M quests across K chapters." Full script docs: `reference/toolchain.md`.

### Step 2 — Mainline interview (agree on the arc, not the tasks)

Settle the **spine**: theme, mods, structure, reward philosophy, linkage. End with an **outline** (`<output_dir>/outline.json5` — names + wiring only, no tasks/rewards) the user approves before anything is designed.

**Interview discipline — grill, don't dump.** ONE question at a time, each with your recommended answer, wait for the reply. Walk branches in dependency order: theme → mods → structure → rewards → linkage. Never post a questionnaire. Check the Step 1 index first — if a question is answerable from the codebase, answer it yourself.

Four questions every pack must answer: (1) What is the single convergence point, and which systems must it touch? (2) Does cross-system gating live in `depends_on` or in item/recipe requirements? (3) Is the middle parallel or forced-linear? (4) What's the portable spine vs. the pack-type-specific opener?

Full interview branches, per-branch questions, topology selection, questbook-role declaration, stage definitions: `reference/design/interview-protocol.md`. Design principles (F1–F3, P1–P7, spine models, anti-patterns AP1–AP11): `reference/design/design-guide.md §principles`.

### Step 3 — Scaffold the skeleton

Turn the approved outline into a skeleton spec: every node gets `name`, `depends_on`, `shape`, empty `tasks: []`/`rewards: []`. Title-only lang. Generate so the bare tree appears in-game for structure sign-off.

IDs are computed automatically from quest names (formula: reference §9). Renaming without `--mode ask` creates a new ID and breaks player progress.

**Topology-aware layout:** if a topology was selected in Step 2, load `reference/design/topology-coordinates.md` §Phase 2–3 for the classification algorithm and coordinate strategy matching the topology type (linear_chain / hub_fan / parallel_columns / diamond_convergence / tree_branching / grid_catalog / highway_branch). Do NOT do collision detection during scaffold — that's R58 in Step 5.

Skeleton spec format + lang placeholder convention: reference §13. Then: `python scripts/generate_quests.py <output_dir>`.

### Step 4 — Polish one node at a time

Iterate outline nodes in main-line order. Scale the loop: ≤~20 quests → per-node sign-off; 20–100 → batch by chapter; >100 → batch by chapter, skip per-node sign-off except for validator-flagged quests.

For each node: co-author content (grill one question at a time) → **pass the three reasoning gates** → update ONLY that quest in the spec → regenerate (incremental merge keeps others pristine) → validate + `quest_detail.py` → AI self-check (style drift, narrative continuity, description-item consistency) → focused summary, sign off.

**The three gates (mandatory — full procedures in `reference/design/reasoning-gates.md`):**
- **Gate 1 — Task Item Reachability:** before every `ftbquests:item` task, answer "玩家此刻怎么拿到这个？" Checks dimension (R1), tool tier (R2), recipe depth (R3), stage resources (R42). FAIL blocks the write.
- **Gate 2 — Reward Bridge:** before every reward, answer "这个奖励引导玩家去做什么？" Classify: material bridge / universal bridge / terminal / dead-end. Dead-end (AP6) blocks the write.
- **Gate 3 — Dependency Chain Sanity:** advisory scan of chain depth, fan-out, orphan risk, diamond rejoin. Surfaces warnings in the summary.

Chapter-level after each batch: teaching order check (Teach-Then-Do, Tier Escalation), AP9 hallucination sweep, progression architecture checks (R101–R116, routed by pack type — see `reference/design/progression-rules.md` §Section G).

Quest text style: natural concise prose, not label-value checklists. Title ≤4 words, subtitle 1 line, description 2–4 sentences. Full rules: `reference/design/design-guide.md §writing-style`.

### Step 5 — Whole-book verify & balance

```bash
python scripts/validate_quests.py <output_dir>/quests/            # + --strict / --fix / --json
```
Runs the full R1–R32 pipeline + topology rules R55–R64 (load `reference/design/progression-rules.md` §Section B for execution order). Print the summary (chapters/quests/tasks/rewards/lang counts, questbook-role stats, topology validation results). Diagnostics catalog: reference §15.

### Step 5a — Load-test in-game

Static validation can't catch runtime failures (missing KubeJS scripts, unregistered item ids, unresolved reward-table refs). Copy to a test profile → `/ftbquests reload` → confirm book opens with no chat errors → flag all `custom` tasks as needs-in-game-verification.

### Step 5b — Deploy to game folder

New pack: copy `<output_dir>/quests/` into `<packroot>/config/ftbquests/quests/`. Existing pack: use `--deploy` (merges additive files, backs up originals — never blind-copy). Full deploy rules + backup layout: reference §16 and `reference/toolchain.md`.

---

## Token discipline

| You want to… | Run this | NOT this |
|---|---|---|
| Orient on a pack | `pack_briefing.py <packroot>` | reading caches/chapter files raw |
| Verify one quest | `quest_detail.py <output_dir> <chapter>/<quest>` | reading the whole chapter |
| Resolve N item names → ids | `lookup_item.py <packroot> <name>…` | N× grep / guessing |
| Look up a field/type | read only the named reference § | reading all of the reference |
| DLC-vs-installed audit | `audit_diff.py <dlc_pack>` (auto-resumes) | re-reading both packs |

Caches are the source of truth, not the raw files. One command's curated output beats several file reads. The reference doc is sectioned on purpose — read the section you need.

---

## Task & reward types (quick reference — full details: reference §7)

**Tasks:** `ftbquests:item` · `fluid` · `forge_energy` · `xp` · `kill` · `advancement` · `stat` · `location` · `dimension` · `biome` · `structure` · `observation` · `gamestage` · `checkmark` · `custom`

**Rewards:** `ftbquests:item` · `xp` · `xp_levels` · `command` · `loot` · `random` · `choice` · `all_table` · `advancement` · `toast` · `gamestage` · `custom` · `currency`

**Shapes:** `circle square diamond pentagon hexagon octagon heart gear rsquare rdiamond puzzle shield` (default `circle`)

**Gotchas:** `loot`/`random`/`choice`/`all_table` reference a table via `table_id` (decimal long, not hex). Command rewards run as the player unless `permission_level` (1-4); `{p}`/`{x}`/`{y}`/`{z}`/`{team}`/`{quest}` are substituted; `@p`/`@a` selectors also work. `gamestage` is the type id for both tasks and rewards. Reward-table `hide_tooltip`/`use_title` default true when absent — emit explicitly.

**Task linkage to existing pack quests:** `depends_on` accepts raw 16-hex IDs (passed through verbatim) for quests this skill didn't generate. Use exact IDs from `.ftbq-cache/existing_quests.json5`, uppercased. A 16-hex-looking quest name is misread as an external reference — don't use one.

---

## Routing table — where every detail lives

| When you need to… | Load |
|---|---|
| Look up exact field names, types, spec format, manifest, deploy, reward tables, SNBT details | `reference/ftb-quests-reference.md` §N (sectioned — read only the § you need) |
| Run any script (extract/index/briefing/lookup/generate/validate/deploy/audit) | `reference/toolchain.md` |
| Design the interview: per-branch questions, topology selection, questbook role, stage definitions, outline format | `reference/design/interview-protocol.md` |
| Understand design principles: F1–F3, P1–P7, spine models, four questions, anti-patterns AP1–AP11, field findings, writing style, synergy patterns, layout reasoning | `reference/design/design-guide.md` (§principles, §writing-style, §synergy-patterns, §layout-reasoning, §field-findings, §atm-layout-patterns, §pack-type-patterns) |
| Apply reasoning Gates 1–3 (item reachability, reward bridge, dependency sanity) with full lookup procedures | `reference/design/reasoning-gates.md` |
| Assign/adjust x/y coordinates, classify topology, run collision detection, decompose large chapters | `reference/design/topology-coordinates.md` (§Phase 2 classification, §Phase 3 algorithms, §Mixed Topology) |
| Assign shape/size, pick clutter-reduction flags, choose a layout family | `reference/design/layout-quickref.md` |
| Run progression validation rules R1–R32, R42–R50, R55–R64, R101–R116 | `reference/design/progression-rules.md` (§routing by pack type; §Section B topology rules; §Section G architecture rules) |
| Find which module contains a rule/pattern/anti-pattern | `reference/design/module-index.md` |
| Look up builtin dimension/tool-tier/ore tables for Gate 1 fast-paths | `reference/design/shared-builtin-tables.md` |
| Item reachability rules R1–R4, R42 + task combination formulas MP1–MP5 | `reference/design/mod-item-reachability.md` |
| Dependency topology rules R5–R9 + micro-patterns MP6–MP10 | `reference/design/mod-dependency-graph.md` |
| Reward design rules R10–R13, R28, R31, R34, R44–R45 + bridging patterns MP14–MP18 | `reference/design/mod-reward-design.md` |
| Teaching pacing rules R14–R18 + quest-internal pacing MP11–MP13, stage marking MP19–MP23 | `reference/design/mod-teaching-pacing.md` |
| Description-trust rules R22–R23 + AI anti-patterns AP9–AP11 | `reference/design/mod-description-trust.md` |
| Command/system safety rules | `reference/design/mod-system-safety.md` |
| ATM-signature patterns (kitchen-sink capstone model) | `reference/design/mod-atm-signature.md` |
| Reward economy philosophy (guide-first vs reward-driven) | `reference/design/reward-economy.md` |
| Difficulty curve (tutorial → early → mid → late → endgame) | `reference/design/difficulty-curve.md` |
| Tech/magic mod progression orientation (verify in JEI/EMI!) | `reference/design/tech-progression.md` |
| DLC vs installed pack audit workflow | `reference/audit-workflow.md` |
| Micro-patterns catalog (MP1–MP73) | `reference/design/micro-patterns.md` |
| Anti-patterns catalog (AP1–AP41+) | `reference/design/anti-patterns.md` |

---

## Sources

Format verified against FTB Quests source 2026-06-25 (FTBTeam/FTB-Quests main + 1.20.1, FTB-Library, json5-java). Empirical data audited from Create: Delight Remake, Mechanomania, ATM9/ATM10 (4,601 quests / 64 chapters), plus 8 cross-genre packs (~2,800 quests). Progression framework: 32+ rules, 70+ micro-patterns, 40+ anti-patterns grounded in the same corpus.
