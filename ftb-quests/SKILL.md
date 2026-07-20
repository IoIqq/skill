---
name: ftb-quests
description: >
  Generate FTB Quests configuration files (JSON5 on current main, SNBT on
  1.20.1 — format detected from the pack's files, not the MC version) for Minecraft modpacks.
  Triggers on: "FTB任务", "FTB quests", "任务配置", "quest config", "任务线",
  "生成任务", "create quests", any request related to FTB Quests mod configuration.
  Interviews the user about their modpack, then generates complete quest chapters,
  tasks, rewards, and localization that load correctly in current FTB Quests.
user-invocable: true
argument-hint: "整合包名称或项目路径 (optional)"
---

# FTB Quests Configuration Generator

Generate FTB Quests configs that **actually load**. The format is precise and easy to get wrong, so follow the rules below exactly. Full field/type reference and a worked example live in `reference/ftb-quests-reference.md` — read it when you need exact field names, type-specific parameters, or must target an older `.snbt` modpack.

## Why this skill exists

Hand-writing FTB Quests configs is tedious — hex IDs, coordinates, dependency chains, per-version format quirks. This skill automates interview → design → generate → write → verify, and is grounded in the **current** FTB Quests source (JSON5 on-disk format).

## Language — match the user

**Conduct all natural-language interaction in the user's language.** If the user writes in Chinese, run the entire interview, recommendations, balance review, summaries, and explanations in Chinese; if in English, use English. Mirror whatever language the user is using in the conversation, and switch if they switch.

This governs **how you talk to the user** — questions, suggested answers, the Step 5 summary, error explanations. It does **not** decide the language of the *generated quest text*: titles/descriptions in `lang/<locale>/` follow the `locales` settled in the Step 2 interview (ask if unclear). A Chinese conversation that produces an English-locale pack is fine, and vice versa — confirm the target locale rather than assuming it equals the chat language.

---

## Quest text & description writing style

Quest text is what the player actually reads. The field/ID machinery elsewhere in this skill exists to *deliver* that text — so write it like a modpack author talking to a player, not like a config file labeling itself. **Default to natural, concise prose; avoid label-value "element-style" (要素式) checklists.** This applies in Step 4 when you author `quest_subtitle` / `quest_desc` and chapter subtitles, for every quest.

**The three text slots render at different zoom levels — don't put the same thing in all three:**

| Slot | Where it shows | Length | Job |
|---|---|---|---|
| `title` | Always visible on the node + header | ≤ ~4 words | Name the thing — the item, mob, biome, or step. Short and evocative. |
| `quest_subtitle` | One line under the title, on hover | 1 line (~8–12 words) | The action in plain language: what to do, or what it unlocks. |
| `quest_desc` | Only when the quest is opened | 1–4 short sentences (~40–80 words; more for teaching quests) | Context, the *why*, a concrete example, a hint. The only place for detail. |

**Write prose, not label-value (要素式) checklists.** The quest UI already shows the item + count + reward; spend the description on the *why* and *how*, not restating them. Full rules + ATM9 example + 7 style rules + localization note: `reference/design/design-guide.md §writing-style` — load it before the first Step-4 node.

**Length budget.** Title ≤ 4 words. Subtitle = 1 line. Description ~2–4 sentences for a normal quest (system-teaching quests may run 2–3 short paragraphs); past ~5 sentences you're padding — move the excess into a linked "how this works" quest or chapter subtitle.

**AI-specific style risks.** When generating many quests in sequence, watch for style homogenization (AP10) and narrative inconsistency (AP11) — both are documented in `reference/design/mod-description-trust.md §AP9–AP11`. Step 4's self-check step catches these per-node; vary description mode (how-to / lore / tip / challenge) and reward structure across the chapter.


---


## CRITICAL — read before generating

**Pick the format by MC version:** 1.20.1 = SNBT with inline text; current `main` (MC 1.21.x, FTB Quests 26.x) = JSON5 with lang files. The MC version picks the format; detect from the actual files to be sure.

| Serialization | Localization | Observed in |
|---|---|---|
| **SNBT** (`.snbt`, no commas, TAB, `0.0d`/`1L` suffixes, `#` comments) | **inline** `title:`/`description:` on the quest object | MC 1.20.1 packs (Create: Delight Remake, FTB Quests 2001.4.17) |
| **JSON5** (`.json5`, commas, bare numbers) | **lang files** (`lang/<locale>/quests.json5`) | current `main` (MC 1.21.x, FTB Quests 26.x) |

Set `format: "json5"` (default) or `format: "snbt"` in the spec; default is `json5`. Full SNBT details in reference §12; the mistakes that silently fail:

- ❌ "No commas between fields" — **wrong for JSON5**. JSON5 uses commas (trailing OK). SNBT uses **no commas**.
- ❌ Type suffixes `0.0d` / `1b` / `1L` — **wrong for JSON5**. Use plain numbers `0.0`, `16`, `true`/`false`. SNBT **requires** the suffixes (`x: 0.0d`, `count: 4L`).
- ❌ **Type-name style mismatch.** SNBT packs use **SHORT** type ids — `type: "item"`, `type: "command"`, `type: "checkmark"`, `type: "dimension"` (no `ftbquests:` prefix). JSON5 uses the **prefixed** form `type: "ftbquests:item"`. The generator emits the right style per `format`; when hand-editing SNBT, use short names to match real packs.
- ❌ `item: "minecraft:oak_log"` (bare string) — **dropped on load in JSON5**; items/icons must be objects `{ id: "minecraft:oak_log", count: 1 }`. **But in SNBT a bare string is valid** — shipped packs use `item: "sophisticatedbackpacks:backpack"` and reward-table entries `{ item: "ae2:logic_processor" }` and they load fine. (1.20.1 SNBT item objects use capital `Count` + `tag: {...}`.)
- ❌ Putting the item quantity *inside* the `item` object for tasks **or rewards** — FTB Quests reads the SIBLING `count` field (`ItemTask`/`ItemReward`); the object `count` is always `1` and is ignored. Write `item: { id: "minecraft:apple", count: 1 }, count: 3`. The generator lifts a buried count to the sibling, but get this right in the spec.
- ❌ An `ftbquests:xp` task without `points` — `XPTask.readData` throws on load. Always set `points: true` (XP points) or `false` (XP levels). The generator defaults `points: true`.
- ❌ A 16-hex id whose top digit is `8`-`F` — `Long.parseLong(hex, 16)` throws and FTB Quests silently regenerates a random id, breaking every dependency referencing it. The generator masks the top bit (§9); never hand-write an `8`-`F` id.
- ⚠️ Inline `title:` / `description:` on quest objects — **ignored on the JSON5/lang-file format** (text lives in `lang/<locale>/quests.json5` keyed `quest.<HEX>.title` / `.quest_desc` / `.quest_subtitle`), **required on the SNBT+inline format**. Detect which of the two you are targeting before writing text.

**Correct JSON5 example:**
```json5
{
  id: "1111111111111111",
  x: 0.0,
  y: 0.0,
  shape: "circle",
  dependencies: [],
  tasks: [
    {
      id: "2222222222222222",
      type: "ftbquests:item",
      item: { id: "minecraft:oak_log", count: 1 },
      count: 4,
      consume_items: true,
    },
  ],
}
```

> **Detection rule:** In Step 1, check existing files — the on-disk format is the source of truth, not the MC version:
> - `.json5` with commas → `format: "json5"`, text in `lang/<locale>/quests.json5` (current `main`).
> - `.snbt` (no commas, `0.0d` suffixes) **and** quest objects have inline `title:`/`description:` → `format: "snbt"`, text inline (1.20.1 classic).
> - `.snbt` **with NO inline text but a `lang/<locale>.snbt` file** of `quest.<HEX>.title` keys → the 1.21.1 SNBT+lang variant. **Not supported for generation** (the generator emits inline SNBT only); use `--adopt`/`--mode preserve` and don't try to emit it.
>
> Default to `json5` for brand-new packs unless the user names 1.20.1 or hands you an existing SNBT pack. The validator auto-detects the on-disk format; the generator takes `format` from the spec.

---

## ⛔ ABSOLUTE RULE — 严禁脑补（ZERO HALLUCINATION）

**This is a non-negotiable, hard-stop rule. Violation invalidates the entire output.**

**You MUST NOT invent, guess, assume, or hallucinate ANY of the following:**

| Category | Forbidden examples | What to do instead |
|---|---|---|
| **物品 ID** | "应该是 `create:brass_ingot` 吧" / guessing a mod's namespace | 查 `items.json5` `all_item_ids` 或 `lookup_item.py`；查不到就问用户 |
| **物品配方 / 合成路线** | "用铁锭和木板合成" / inventing a crafting recipe | 问用户在 JEI/EMI 确认；或标记 `[unverified:recipe]` |
| **任务内容 / task 设计** | 编造"收集 16 个铜齿轮"而不确定该物品存在 | 先确认每个涉及的 item ID 存在，再写 task |
| **Mod 机制 / 交互** | "Mekanism 的化学灌注器需要 AE2 的福鲁伊克斯水晶" | 问用户确认该交互确实存在；不要假设跨 mod 联动 |
| **进度 / 阶段顺序** | "这个阶段玩家已经有钻石了" / assuming what's available at a point | 问用户该整合包的进度设计；不要推测玩家在某阶段拥有什么 |
| **方块 / 实体 / 流体 ID** | 猜测 `minecraft:copper_block` 存在（某版本可能没有） | 同物品 ID，查 source 或问用户 |
| **奖励内容 / reward 物品** | 编造奖励物品而不确认其存在 | 同物品 ID 验证流程 |
| **数量 / 数值** | "这个机器需要 64 个" / guessing stack sizes, energy values, damage | 问用户确认具体数值 |
| **FTB Quests 字段 / 类型** | 编造不存在的 type 或 field | 查 `reference/ftb-quests-reference.md` |

**核心原则：宁可空着问用户，不可瞎猜写进 spec。** 任何无法从 verification ladder 验证的内容，必须：
1. 标记 `[unverified:<category>]`（如 `[unverified:recipe]`、`[unverified:item_id]`、`[unverified:progression]`、`[unverified:dimension]`、`[unverified:tool_tier]`、`[unverified:recipe_depth]`、`[unverified:reward_bridge]`）
2. 立即告知用户该内容未经验证
3. 等待用户确认后再写入 spec

**Verification ladder（从强到弱）：**

1. **Existing pack's quests** → `index_quests.py` writes `.ftbq-cache/existing_quests.json5` with a top-level `known_item_ids` list — every resource location referenced by an existing quest *actually loaded in this pack*. Author against this set when extending a pack (strongest source).
2. **Mod jars' lang files** → `extract_items.py` writes `.ftbq-cache/items.json5` with `all_item_ids` derived from each mod's `assets/<modid>/lang/en_us.json` keys (`item.<modid>.<name>` → `<modid>:<name>`), plus `.ftbq-cache/item_names.json5` (name↔id, en+zh) for resolving display names → ids in bulk via `lookup_item.py`. Strongest source for a brand-new pack. **Best-effort:** not every registered item has a lang key; treat as a candidate set, not a complete registry.
3. **Format / field / type behavior** → `reference/ftb-quests-reference.md` (verified against the FTB Quests Java source).
4. **Recipes & mod mechanics** → ask the user to confirm in JEI/EMI (you can't see in-game recipes); for cross-mod interactions, verify a shared recipe/gate actually exists before writing the quest.
5. **Final catch** → the Step 5a in-game load-test (`/ftbquests reload`, no chat errors) is the last verifier for anything still `[unverified]`.

**Generation-time progression checks.** Beyond item-ID verification, Step 4 enforces three **mandatory reasoning gates** per node: Gate 1 (item reachability — can the player get this item at this point?), Gate 2 (reward bridge — does this reward lead somewhere?), and Gate 3 (dependency chain sanity — is this quest's local graph structure reasonable?). Each gate requires an explicit one-line reasoning output before the task/reward is written to the spec; unanswered gates block the write (Gates 1–2) or surface a warning (Gate 3). The reasoning uses builtin lookup tables from `reference/design/shared-builtin-tables.md` and rules R1–R4 from `reference/design/mod-item-reachability.md`, R5(incremental)/R6(local)/R7 from `reference/design/mod-dependency-graph.md`, R10(reverse)/R28/R31 from `reference/design/mod-reward-design.md`, R14–R17/R18 from `reference/design/mod-teaching-pacing.md`, R22/R23 from `reference/design/mod-description-trust.md`; anti-pattern context from `reference/design/mod-description-trust.md §AP9–AP11`. See `reference/design/module-index.md` for the full routing table. These gates are embedded in the Step 4 per-node loop, not a separate checklist — see Step 4 for the gate definitions and pass/fail criteria.

**In Step 4, before writing a task/reward item:** confirm its id is in `items.json5` `all_item_ids` or `existing_quests.json5` `known_item_ids`; if not, ask the user — don't guess. For a **batch** (many items, e.g. a collection quest), resolve all names in one call via `lookup_item.py` (see "Batch item-id lookup") instead of grepping per item.

**File mutation discipline — read before you write.** Every file modification must be preceded by a fresh read of the target file's current state. Never edit from memory or from a stale context window. The specific protocol:

1. **Before editing any quest config file** (`chapters/*.json5`, `lang/*/quests.json5`, `quests.spec.json5`): read the file first with `Read` or `cat`, confirm the current content matches your expectation, then edit. If the file has changed since you last read it (another session, manual edit, generator re-run), re-read and reconcile before writing.
2. **Before editing SKILL.md or any reference document**: read the full file, identify the exact section to modify, and use targeted edits (`Edit` tool with precise `old_string` match) rather than rewriting the entire file. A full-rewrite risks losing content you didn't intend to change.
3. **Before creating a new file in a project**: check whether a file with that name already exists (`ls` or `Glob`). If it does, read it first and decide whether to append, merge, or replace — never silently overwrite.
4. **Batch operations**: when modifying multiple files in one pass (e.g., generating quests for a whole chapter), read each file before writing. The generator's `--mode preserve` and `content_hash` mechanism protect untouched quests, but you must still verify the output (`validate_quests.py` + `quest_detail.py`) rather than assuming success.
5. **Data-before-design**: before designing a quest that references a specific mod mechanic, item, recipe, or interaction, gather evidence from the strongest available source (verification ladder above). The order is: existing pack config > mod jar lang files > official mod documentation > community wiki > ask the user. Never write quest content based solely on general knowledge of a mod — mods change between versions, and your training data may be outdated.

This discipline applies to ALL file operations in this skill — not just quest configs, but also SKILL.md updates, reference document edits, and script modifications.

**Self-check before every spec write:** "这个值是我从 verification ladder 查到的，还是我脑子里编的？" 如果是后者 → **停，问用户。**

---

## Design principles — strategic input to the interview (summary)

The full reasoning — F1–F3 (foundational model), P1–P7 (reusable patterns), the thinking-in-order, and the four questions — lives in `reference/design/design-guide.md §principles`. **Load it before Step 2.** It is distilled from a full-file ATM10 audit (figures + provenance in `§field-findings` and `Sources` below) and refines every capstone mention in this skill: the audited model is **in-chapter + item-task-gated** (the capstone + components live in one self-contained chapter; cross-mod breadth is via each component's item task, not cross-chapter `depends_on`).

**Four questions to answer before designing any pack** (the interview's trunk — full reasoning in §principles):

1. What is my single convergence point, and which systems must it touch?
2. Does cross-system gating live in `depends_on`, or in item/recipe requirements?
3. Is the middle parallel (pick-a-lane) or forced (linear)?
4. What's the portable spine vs. the pack-type-specific opener?

**Anti-patterns to design against.** Eleven recurring design mistakes are distributed across the modular reference files — from description-reality mismatch (AP1, the most damaging, in `reference/design/mod-description-trust.md`) through circular dependency deadlock (AP2, in `reference/design/mod-dependency-graph.md`) to the three AI-generation-specific risks (AP9–AP11, in `reference/design/mod-description-trust.md`). Load `reference/design/module-index.md` to find which module contains each anti-pattern. Load AP1–AP8 as background knowledge before Step 2; keep AP9–AP11 in mind during Step 4 generation.

## Quest progression, arrangement & authoring logic

Where the layout section (later in this skill) handles *spatial* arrangement (x/y, no crossing lines), this handles the *logical* arrangement — what depends on what, what order the player meets things, and the thinking behind the spine. Get the logical spine right in Step 2 (the outline) before any spatial layout; coordinates can't rescue a confused dependency graph.

**Four proven spine models — pick one (or layer them) in Step 2:**

| Spine model | Shape | Best for | Real reference |
|---|---|---|---|
| **Linear** | One chain, each quest depends on the previous | Tutorial chapters, a single mod's recipe ladder, skyblock "get→craft→automate" openers | most packs' Chapter 1 |
| **Nonlinear / parallel-mod-lines** | One chapter per mod, independent; a final capstone depends on a representative quest from each | Kitchen-sink packs where mods don't share a recipe chain | **ATM9 / ATM10** (intro + per-mod chapters → ATM Star) |
| **Themed / stage** | Chapters keyed to a theme / age / celestial body; each chapter unlocks the next *context* (dimension, age, planet), not just the next item | Story / explore packs, expert progression | **Create: Astral** (chapters per celestial body; space travel is the spine, not the endgame) |
| **Tier-gated material spine** | A vertical material tier (tier-N needs a tier-(N-1) pick) across dimensions, converging into one capstone item | Endgame identity for any pack | **ATM** AllTheModium → Vibranium → Unobtainium → ATM Star |

Most real books layer these: a Linear Chapter 1, then Parallel-mod-lines for the middle, then a Tier-gated capstone. That's the ATM shape, and a strong default for a kitchen-sink.

**Authoring thinking (Step-2 decisions that make or break a book):**

1. **Decide the spine before the tasks** — that's what the Step 2 outline is for (names + wiring, no tasks). A spine-first book reads coherently; a quest-by-quest book ends up a pile.
2. **One chapter = one mod OR one theme, not both.** Kitchen-sink = one chapter per mod (player picks what to learn); story/expert = themed chapters ("The Nether", "Steam Age") pulling from several mods. Mixing confuses the mental model.
3. **Teach each mod's intended progression, don't invent one** — walk the mod's native recipe ladder (ore → ingot → part → machine → upgrade).
4. **The capstone touches every system** (see `reference/design/design-guide.md §principles` F3) — ATM's Star sources one component per major mod; if your capstone uses 3 of 20 mods, players ignore the other 17.
5. **Reward philosophy + pacing up front.** Pick guide-first (roadmap, minimal rewards — Divine Journey 2 / Create: Astral) vs reward-driven (generous — ATM) and commit (lesson 2 / `reference/design/reward-economy.md`). Pacing follows the difficulty curve (`reference/design/difficulty-curve.md`): tutorial → early (16–64 stacks) → mid (1–2 hr bottlenecks) → late (multi-blocks, bosses) → endgame; every ~3rd quest an alternative path.
6. **`progression_mode` is a per-chapter switch**: `default` (quest locks until dep done — strict order) vs `flexible` (any order, deps hide not lock). ATM ships `flexible` (issue #1136) so passive tasks (advancements/stats/biome visits) count; use `default` when order *is* the lesson.

**Micro-level authoring patterns** — the 34 micro-patterns are distributed across the modular reference files: task combination formulas (MP1–MP5) in `reference/design/mod-item-reachability.md`, dependency topologies (MP6–MP10) in `reference/design/mod-dependency-graph.md`, quest-internal pacing (MP11–MP13) and stage marking (MP19–MP23) in `reference/design/mod-teaching-pacing.md`, reward bridging (MP14–MP18) in `reference/design/mod-reward-design.md`. Load `mod-item-reachability` and `mod-reward-design` before Step 4 node generation; load `mod-dependency-graph` and `mod-teaching-pacing` before Step 2 outline design. See `reference/design/module-index.md` for the full routing table. For topology-aware layout rules (R55–R64), coordinate algorithms, and real case data from 13 chapters across 9 packs, load `reference/design/topology-coordinates.md` and `reference/design/progression-rules.md` §Section B.

**Linear vs nonlinear — the dependency wiring:**
- **Linear:** `dependency_requirement: "all"`, each quest depends on the prior — one path, no choices. Good for teaching a forced sequence.
- **Nonlinear:** quests in a chapter share *no* deps among themselves (craft in any order); a capstone at the end depends on all of them (`"all"`), or on one-per-branch (`"one"` for "any path"). Good for catalogs and parallel mod lines.
- **Branching:** a hub fans into N alternatives — `dependency_requirement: "one"` (do any one) or `"all"` (do all). See the culinary capstone-hub pattern for the many-to-one variant.

---

## Mod synergy & cross-mod quest design

A modpack is more than mods-in-a-folder — it's the *connections* between them. The best packs make cross-mod interaction the actual content. Design quests that teach and require those connections; don't just list each mod in isolation.

**Four patterns of mod synergy** (cross-mod crafting chain, cross-mod gating, capstone synthesis, deep integration) — build quests around them; full descriptions + the "don't fake synergy" caveat live in `reference/design/design-guide.md §synergy-patterns`. Load it when designing cross-mod content.

**Representing synergy in the spec:**
- **Item task from multiple mods:** an `ftbquests:item` task holds one item; for "make this cross-mod component," the task item is the *output* and the description walks the inputs. For "prove you've used both mods," use **two tasks** on one quest (`tasks: [ {item: modA:…}, {item: modB:…} ]`, `dependency_requirement: "all"`) — completing it proves the player touched both.
- **Cross-chapter dependency:** mod B's chapter gates after mod A's key quest — `depends_on: ["<modA_chapter>/<key_quest>"]` (or the raw hex for an existing pack). Cleanest signal that "mod B assumes you know mod A."
- **`quest_links[]` (hexagon, size 2.0):** display the same quest in two chapters when it belongs to both (a machine that's both "Mekanism" and "AE2"). Links, not duplicates (reference §18).
- **KubeJS `custom` tasks/rewards:** when synergy can't be expressed as an item ("has the player actually run the integrated Create + Tinkers pipeline?"), use `type: "ftbquests:custom"` and point at the pack's KubeJS script for the check. Most deep-integration packs lean on this.
- **Don't fake synergy the mods don't have.** If two mods don't actually interact (no shared recipe, no gating), don't manufacture a cross-mod quest — it'll task the player for something they can't do. Verify the interaction in JEI / EMI or the mods' configs before writing the quest (Step 4's "never guess" rule).

---

## Protocol

The steps below are a recommended flow — skip or merge them as the task warrants. The format rules (the "CRITICAL" section above and "Format gotchas") are the one thing to follow exactly; everything else is adaptable.

### Fast paths (when the full interview is overkill)

- **Small job (≤~5 quests, or a quick addition to an existing pack):** skip the Step 2 interview and Step 3 skeleton. Run Step 1 (detect format + index), then co-author the quests directly in `quests.spec.json5` with the user — names, tasks, rewards, and lang in one pass — then regenerate, validate (Step 5), and load-test (Step 5a). The outline→scaffold ceremony doesn't pay off for a handful of quests.
- **You already have a complete spec** (the user handed you one, or you wrote it in a prior session): skip Steps 1–4. Run `python scripts/generate_quests.py <output_dir> --spec <your.spec.json5>` and jump straight to Step 5 (verify) → Step 5a (load-test) → Step 5b (deploy). If the spec targets an existing pack, confirm its `format:` matches what Step 1 would detect (SNBT vs JSON5) so you don't emit the wrong format.

### Step 1 — Index & detect

If the user gave a project path, work in this order — **build the caches before you brief**:

1. **Detect the target format** from one existing file (commas? `0.0d` suffixes? inline titles? item form?). Mirror it exactly, and note existing quests' id format, shapes, dependency style, and lang conventions. (Existing configs live at `config/ftbquests/quests/**/*.{json5,snbt}`.)
2. **Build the caches** the briefing reads — run all three once (skip one if its cache is already fresh):
   ```bash
   python scripts/extract_mods.py <packroot>      # -> .ftbq-cache/mods.json5 (modid/name/version/side/loader per jar)
   python scripts/extract_items.py <packroot>     # -> .ftbq-cache/items.json5 (verified ids) + .ftbq-cache/item_names.json5 (name→id index, en+zh — see "Batch item-id lookup")
   python scripts/index_quests.py <packroot>      # -> .ftbq-cache/existing_quests.json5 (id/chapter/shape/deps/task+reward types + known_item_ids per existing quest)
   ```
   `index_quests.py` parses modern JSON5 with the string-aware parser; legacy `.snbt` gets a best-effort pass marked `format: snbt` (lower detail); its top-level `known_item_ids` lists every item id referenced by existing quests (verified-loaded). `extract_items.py` is best-effort (not every registered item has a lang key); it also writes `item_names.json5` — a lightweight name→id index from the lang values it reads anyway (en_us + zh_cn where shipped). `lookup_item.py` resolves batch names against it (see "Batch item-id lookup" below). Re-run a builder whenever its source changes (new/removed jars, or the existing pack's quests change).
3. **Orient from one command, not from file reads:**
   ```bash
   python scripts/pack_briefing.py <packroot>
   ```
   This prints a compact summary (format, mod count + names, chapters + per-chapter quest count, task/reward type frequencies, audit verdict) curated server-side from `.ftbq-cache/` — **do not read `mods.json5` / `existing_quests.json5` / chapter files raw for orientation**. A missing cache is flagged with the builder to run (step 2). See "Token discipline".
4. **Index via CodeGraph (if the toolchain is available).** If you can call the CodeGraph MCP tools (`codegraph_explore` / `codegraph_query` / `codegraph_impact`) or a `codegraph` CLI, register the modpack folder as the project and index it. The value is the **quest config files** (cross-file dependency chains across chapters, lang-key references, `quest_links` mirrors — beyond what `index_quests.py` captures) + **session memory** (`memory_load`/`memory_search` surfaces prior theme/reward/gating decisions to pre-fill the Step 2 interview). Use `codegraph_explore` for "what references quest X?" and `codegraph_impact` for blast-radius before editing. **Preferred over the Python-only path when available.** If absent (the common case), the Python caches + validator's `E_DEP_MISSING`/`E_DEP_CYCLE`/fuzzy hints cover the same ground.

Open Step 2 with what you indexed: "Detected N mods — suggested chapters: …. Existing pack has M quests across K chapters; your new content can gate after / reward from / branch off any of them." If the existing-quests cache is empty (brand-new pack), skip linkage — there's nothing to link to.

If no existing project: default to **modern JSON5** and skip ahead. If there's a `mods/` folder, still run `extract_mods.py` to drive the chapter suggestions; if there's no pack at all, take the modlist from the user in Step 2.

### Batch item-id lookup (收集任务 / many item tasks)

When a node (or a batch of nodes) needs **many item ids at once** — a collection quest ("collect 铁锭×64, 橡木原木×32, …"), a reward table, a recipe-catalog chapter — do **not** grep `all_item_ids` once per item. The name index built in Step 1 (`extract_items.py` → `.ftbq-cache/item_names.json5`) maps display names → ids in bulk; resolve them in one call and reuse the result for the whole batch:

```bash
python scripts/lookup_item.py <packroot> 铁锭 橡木原木 木棍        # names → ids, one pass
python scripts/lookup_item.py <packroot> "Copper Ingot" --partial  # surface every mod's copper
python scripts/lookup_item.py <packroot> --reverse minecraft:iron_ingot   # id → known names
```

The index is **en_us (universal) + zh_cn (where the jar ships it)** from each mod jar's lang values, plus the user-verified Chinese names `audit_index.py` already harvested from your existing quest descriptions (`&e<id><中文名>&r`) — merged live at query time, no second scan. It is built once (Step 1) and persisted; rebuild only when mods change (re-run `extract_items.py`). This is the "read the game source once, reuse next time" path: the source jars are scanned once per build, the index is queried thereafter.

**Ambiguity is surfaced, not guessed.** Many mods ship the same display name (e.g. "Copper Ingot" in minecraft / create / immersiveengineering); `lookup_item.py` prints every candidate id with its mod prefix — pick by the chapter's mod, or ask the user. **Never silently pick one** (禁止脑补). If a name isn't in the index at all, it returns `NOT FOUND` + suggestions — ask the user to confirm it in JEI/EMI rather than inventing the id. Best-effort caveat (from `extract_items.py`): not every registered item has a lang key, and a few lang keys describe variants rather than discrete ids — the Step 5a load-test is still the final verifier.

### Step 2 — Mainline interview (agree on the arc, not the tasks)

Goal of this step: settle the **spine** of the book — theme, mods, structure, reward philosophy, linkage — and end with an **outline** the user approves before ANY task or reward is designed. Do NOT design individual tasks/rewards here; that is Step 4's per-node loop. Resolving the dependencies *between* decisions one-by-one (theme → mods → structure → rewards) is still the method; the deliverable is now a reviewed node list, not a full spec.

> **Interview discipline — grill, don't dump.** Ask the user ONE question at a time, each with your recommended answer, and wait for their reply before the next. Walk the decision tree branch-by-branch (theme → mods → structure → rewards → linkage), resolving one dependency before moving to the next. **Never post a questionnaire / list of questions and wait** — that abdicates your role as the designer. This is the grill-me method; it applies here (Step 2, the arc) AND in Step 4 (each node's content). Before asking, check the Step 1 index + existing quests/lang: if a question can be answered by exploring the codebase, explore it yourself instead of asking. Skip any branch already settled by what you indexed.

**Ask when you don't understand** — if a mod's mechanics, a task/reward type's behavior, a format quirk, or any requirement is ambiguous, ask the user to clarify instead of guessing. Surface your uncertainty rather than papering over it — a wrong assumption about a mod's recipe or a reward's effect silently breaks the generated quests.

Work the branches in dependency order:
- **Theme & tone:** theme (tech / magic / adventure / skyblock / kitchen-sink), tone (tutorial / lore / humorous), language(s) — name the primary (authoring) locale + any secondaries; secondaries are translated in a post-Step-4 pass, not per node.
- **Mods:** which mods get chapters (auto-detect from mod list), which to exclude (library/utility mods), mod-specific mechanics to highlight.
  - Magic/tech mod progression patterns + per-mod bottleneck orientation: `reference/design/tech-progression.md` (**orientation only — verify in JEI/EMI**, see the never-guess rule).
- **Structure:** ~chapter count, connected vs independent, a main storyline + optional sides, ~quests per chapter. When the Theme branch picked **kitchen-sink** (ATM-series style), the spine + capstone is the backbone to settle here — don't leave kitchen-sink chapters as flat quest buckets:
  - Per-chapter spine — each mod/system chapter carries its own short through-line chain (e.g. ATM's AllTheModium line). (recommend: one spine per chapter; it's what makes a kitchen-sink pack navigable)
  - Capstone convergence — one endgame node the whole book converges on (ATM Star / Gregstar style)? (recommend: yes for ATM-series). The capstone chapter is **self-contained** (model: Design principles F1/F2).
  - Non-kitchen-sink endgame — linear/expert packs end on a final boss or goal quest, not a convergence capstone; don't force one onto a pack without a convergence shape.
  Evidence: see `reference/design/design-guide.md §field-findings` (ATM9/ATM10).
- **Topology selection — MANDATORY:** "你希望这个 chapter 使用什么布局拓扑？" Seven options (load `reference/design/topology-coordinates.md` §Phase 2 for visual examples):
  - **linear_chain** — 深度线性链（教程章、单 mod 配方链）
  - **hub_fan** — 中心 hub 辐射分支（多子系统 mod 如 Mekanism）
  - **parallel_columns** — 并行纵列（赏金板、多材料并行升级）
  - **diamond_convergence** — 菱形汇聚（多路线汇聚到 capstone）
  - **tree_branching** — 树状分支（大型专家包主进度线）
  - **grid_catalog** — 网格目录（里程碑/成就收集章）
  - **highway_branch** — 水平主干+垂直分支（多结构 mod 如 Botania）
  Ask per-chapter, not per-book — different chapters in the same pack typically use different topologies. Recommend based on the chapter's content structure: a mod with N sub-systems → hub_fan; a linear upgrade path → linear_chain; a collection trophy case → grid_catalog. The topology choice drives coordinate assignment in Step 3 and validation rules in Step 5.
- **Rewards & difficulty:** reward philosophy (generous items vs cosmetic/lore), `consume_items` philosophy, special reward types (commands / loot tables / XP), expert/hardcore gating.
  - **Dominant reward type (审查 C 补充):** If the pack uses reward tables (`random`/`loot`/`choice`), settle the dominant type here — one pack, one dominant presentation style. Craftoria uses `random` (auto-roll), E10 uses `loot` (loot crate), MI:Foundation uses `item` (deterministic). Mixing is allowed but should be deliberate, not accidental (R34 reports the distribution). Ask: "你的整合包偏好哪种奖励呈现方式？自动抽取 (random)、战利品箱 (loot)、还是玩家选择 (choice)？" with the recommendation based on pack genre.
- **Questbook role (R46) — MANDATORY:** "你的任务书主要扮演什么角色？" Four options:
  - **伴生导航 (companion)** — 任务书给方向，EMI/field guide 给细节（如 TFG Modern）
  - **教程系统 (tutorial)** — 任务书是主要教学工具（如 Monifactory、E9E）
  - **激励目录 (incentive_catalog)** — 任务书主要发奖励驱动玩家（如 ATM 系列）
  - **混合模式 (hybrid)** — 不同章节扮演不同角色（如 ATM-10 大部分是激励目录，某些章节充当教程）。If hybrid, ask which chapters use which role.
  This declaration determines R47 and R50 applicability downstream.
- **Collection-catalog check (R49) — CONDITIONAL:** When the user mentions collection/catalog chapters during structure discussion, ask: "这个 catalog 涵盖哪些 mod？这些 mod 的内容是否已稳定，还是仍在频繁更新？" If > 3 actively developed mods or estimated > 200 quests, warn about maintenance cost and recommend: (a) limiting scope to stable-content mods, (b) using tag-based tasks (`itemfilters:tag` or `ftbfiltersystem:smart_filter`) that auto-include new items, or (c) splitting into smaller sub-chapters.
- **Zero-reward safety (R50) — CONDITIONAL:** When the user indicates zero or near-zero reward design, confirm 3 safety conditions:
  1. "是否有替代进度货币？" (voltage tiers, badges, skill systems, Game Stages, achievement unlocks). **If the user doesn't know, proactively suggest alternatives** based on the pack's mod list — e.g. "你的包有 Game Stages，可以用 stage 解锁作为进度货币" or "GregTech 包天然有电压等级作为进度标志".
  2. "任务书角色是否为 companion 或 catalog？" (from R46)
  3. "包是否有强内在游戏循环？" (crafting/collection/combat/exploration)
  All three must be yes for safe zero-reward design. If any condition fails, recommend adding at least minimal XP or cosmetic rewards.
- **Stage definitions（阶段定义收集）：** When the pack type is expert, story, or skyblock, the following questions are mandatory; kitchen-sink packs may ask optionally:
  1. **Stage division（stage_map skeleton）：** "你的整合包有明确的阶段划分吗？例如'石器→铁器→钻石→下界→末地'或'ULV→LV→MV→HV→EV'？请列出阶段名称和顺序。"
  2. **Stage key resources（stage_available_resources）：** "每个阶段有哪些关键可获得资源？请每阶段列出 5–10 个代表性物品 ID。"
  3. **Game Stages integration（if applicable）：** "你的包是否使用 Game Stages 或类似的阶段锁定模组？如果是，请提供 stage name 列表及其解锁的内容摘要（物品/维度/配方）。"

  Collected data serves as L2-level data source for the following rules:
  - R42（Stage-Internal Item Reachability）：use `stage_available_resources` to check whether crafting-chain leaf nodes fall within the current stage's reachable resource set.
  - R44（Reward-Stage Matching）：use `stage_map` to judge whether a reward item skips stages.
  - R43（Stage-Quest Causal Chain Acyclic）：use the stage→quest mapping to detect Stage-Quest cross-cycles.
  - R4（Stage Boundary）：use stage definitions to judge whether items are placed in the correct stage range.

  If the user does not provide L2 data, the above rules degrade to L1 heuristic or INFO-level reporting.
- **Linkage (only if Step 1 found existing quests):** how does the new content connect to the pack's existing quests? Grill one question at a time, codebase-first — show what the index found before asking. Branches:
  - Gate after — should new quests require completing an existing quest first? (recommend: yes, if the new chapter uses mods the existing book unlocks)
  - Reward from — should completing existing quests reward into the new line, or vice versa? (recommend: only if the two share a progression resource)
  - Branch off — does the new line split from an existing quest as an optional side, or stand alone? (recommend: branch off when the themes overlap; stand alone when they don't)
  - Avoid duplicating — does an existing quest already teach/require the same thing? (recommend: skip or rephrase the new task to avoid a dead duplicate)
  Record the chosen existing quests by their 16-hex ID (from the cache) and reference them in `depends_on` — see "Task linkage" below.

Keep going until every branch is resolved to shared understanding — the four buckets above are the trunk, not the whole tree. If a sub-decision is still open (layout style, dependency gating, boss/key placement, lang coverage), drill into it.

**Adaptive depth:**
- "帮我设计" / high-level ask → propose the outline yourself; the user approves/edits.
- "我要指定每个任务" / granular → still agree the outline first, then co-author each node in Step 4.

**Deliverable — the outline (approve before scaffolding):** before leaving Step 2, write `<output_dir>/outline.json5` and show it to the user for sign-off — one chapter list, each with its quest **nodes** in main-line order and the `depends_on` chain, plus where side branches fork. Only names + wiring; **no tasks, no rewards, no descriptions.** For a kitchen-sink capstone, the capstone chapter is **self-contained** (see the example below + Design principles F1/F2).

```json5
{
  pack: "create-astral",
  arc: "place a cogwheel → automate oak → first machine",
  chapters: [{
    name: "getting_started",
    nodes: [
      { name: "punch_wood", depends_on: [] },
      { name: "first_plank", depends_on: ["punch_wood"] },
      { name: "manual_craft", depends_on: ["first_plank"] },
    ],
  }],
}
```

```json5
// kitchen-sink: capstone chapter is SELF-CONTAINED — capstone + components in-chapter;
// cross-mod breadth is via each component's item TASK, not cross-chapter depends_on (see `reference/design/design-guide.md §principles` F1/F2).
{
  pack: "atm-style",
  arc: "per-mod chapters teach each mod → capstone chapter pulls one component per mod",
  chapters: [
    { name: "allthemodium", nodes: [                 // a per-mod chapter (teaches the mod)
      { name: "find_ore", depends_on: [] },
      { name: "alloy_pendant", depends_on: ["find_ore"] },
    ]},
    { name: "mekanism", nodes: [                     // another per-mod chapter
      { name: "first_osmium", depends_on: [] },
      { name: "metabolics", depends_on: ["first_osmium"] },
    ]},
    { name: "endgame", nodes: [                      // capstone chapter — self-contained
      { name: "dragon_soul", depends_on: [] },        // task: items from the dragon-content mods
      { name: "singularity", depends_on: [] },        // task: items from AE2
      { name: "atm_star", depends_on: ["dragon_soul", "singularity"] },  // capstone, in-chapter
    ]},
  ],
}
```

Get an explicit "yes" (or edits) before Step 3. If the user changes the arc later, update the outline and re-confirm — do not silently diverge.

### Step 3 — Scaffold the skeleton (structure only, no task content yet)

Turn the approved outline into a **skeleton spec**: every node becomes a quest with `name`, `depends_on`, `shape`, and **empty** `tasks: []` / `rewards: []`. Add title-only lang (chapter + quest titles; descriptions come in Step 4). Generate it so the bare tree appears in-game — the user walks the spine and confirms structure before any task is written.

Layout (the generator's `auto` layout follows the same convention): main path left-to-right (`x` +1.0/step, `y` flat), side branches offset (`y` ±1.0), spacing ~1.0, `size: 1.0`. Shapes: main = `circle`, optional = `square`, boss/key = `hexagon`/`diamond`. Wire `dependencies` by `name`; default `dependency_requirement: "all"` (`"one"` for choose-N).

**Topology-aware layout (Cycle 11):** If a topology was selected in Step 2, read `reference/design/topology-coordinates.md` §Phase 3 to choose the coordinate assignment strategy matching the topology type. Use the constraint formulas (spacing, hub radius, column gap) from §Layer 2 to calculate initial coordinates. Key formulas by topology:
  - linear_chain: `y_spacing = clamp(1.5 * density_factor, 1.0, 2.5)` with optional x-zigzag
  - hub_fan: `hub_radius = clamp(3.0 + fan_out * 0.4 + max_leaves * 0.5, 3.5, 8.0)` — note the 31% deviation from original formula when sub-hubs have leaves
  - parallel_columns: `column_x_gap = clamp(2.0 + width * 0.5, 2.0, 4.0)`
  - highway_branch: x-spine at 2.0 spacing, branches at 1.5 vertical offset
  - grid_catalog: `columns = ceil(sqrt(quest_count))`, 1.5×2.5 spacing
  - tree_branching: recursive subtree layout with `total_width=16.0`
  - diamond_convergence: sin-curve spread `x_spread = 3.0 + path_length * 0.5`

Do NOT attempt collision detection during scaffold — that is reserved for R58 validation in Step 5.

**Topology template selection — read before assigning coordinates.** Before placing the first quest node in any chapter, load `reference/design/topology-coordinates.md` and walk through its Phase 2 classification algorithm to confirm (or revise) the topology type selected in Step 2. The topology type determines which coordinate assignment strategy from Phase 3 applies — each of the seven types has its own algorithm and spacing regime, and picking the wrong one produces layouts that fight the chapter's intended player experience. Choose by the chapter's content structure, not by aesthetics:

- **linear_chain** — a linear tutorial or single-mod recipe chain (few branches, depth ≥ 6), with zigzag x-amplitude
- **hub_fan** — a mod with multiple independent subsystems (fan_out ≥ 5 from one root), with radial placement using the trigonometric lookup table (§Phase 3)
- **parallel_columns** — several parallel upgrade paths with no cross-dependencies, with uniform column gaps
- **diamond_convergence** — many paths converging on a capstone, with sin-curve spread
- **tree_branching** — a hierarchical tree (hub → sub-hubs → leaves, depth ≥ 4), with recursive subtree layout
- **grid_catalog** — a flat collection or achievement catalog (few dependencies, quest count ≥ 20), with square-root column count
- **highway_branch** — a long horizontal progression with vertical side branches, with 2.0-unit spine spacing

The shape decision tree in §Phase 2 classifies by `max_depth`, `max_width`, convergence ratio, and hub presence — run the thresholds against the chapter's outline before committing to a topology, and cross-reference `reference/design/progression-rules.md` §Section B (R55–R64) to confirm the chosen topology is compatible with the chapter's `progression_mode` (R55) and will produce collision-free initial spacing (R58's spacing formulas, not its runtime check). For chapters exceeding 80 quests, also check Phase 2.5's large-chapter decomposition — a single topology may not capture the internal structure, and splitting into sub-regions with independent topologies produces better layouts.

**Cycle 16 addendum — classifier refinements and new patterns.** Three updates from Cycle 16 research (6 new topology cases, 2 new micro-patterns) to keep in mind during scaffold:
1. **Shallow tree detection.** The Phase 2 classifier now includes a `tree_branching` condition for shallow-but-deep structures: `elif max_depth >= 3 and max_width <= max_depth and convergence_ratio < 0.1` → classify as `tree_branching` even when `max_depth` is below the usual threshold of 4. This catches chapters that are deep and narrow without a prominent hub — see `reference/design/topology-coordinates.md` §Phase 2 for the full decision tree.
2. **Preliminary micro-patterns MP70 and MP71.** Two new micro-patterns — MP70 (Tome-Tier Progression Map) and MP71 (Shape-as-Category-Marker) — are documented in `reference/design/micro-patterns.md` §Part 17 but remain **[Preliminary]** (single-source, no player feedback validation). When referencing them in layout decisions or chapter descriptions, mark as experimental and note that broader pack adoption is needed before they can be treated as established patterns.
3. **Diamond shape as category marker (Case 45).** MC-Odyssey-3's `exploration` chapter demonstrates a novel use of `diamond` shape: not as a convergence signal (the topological `diamond_convergence` meaning) but as a semantic category marker for structure-discovery quests (12 diamond-shaped quests = 12 structures to find, with zero multi-dependency convergence). When a chapter uses diamond shapes on independent quests with no fan-in, classify as `parallel_columns` rather than `diamond_convergence` — the shape encodes category identity, not topological convergence. See `reference/design/topology-coordinates.md` Case 45 for full data.

**Cycle 17 addendum — large-chapter decomposition and new topology patterns.** Six new topology cases (Cases 49–54), two new micro-patterns (MP72, MP73), and reading-direction research from Chinese-language packs:

1. **Large-chapter decomposition trigger (>80 quests).** When a chapter exceeds 80 quests, load `reference/design/topology-coordinates.md` §Mixed Topology Analysis and §Phase 2.5 before assigning coordinates. A single topology type rarely captures the internal structure of a 80+ quest chapter — authors consistently decompose into 4–6 spatially distinct sub-regions, each with its own internal topology (MP73, [Indirectly-Validated]). The decomposition follows mod/subsystem boundaries, not topology rules.
2. **MP72 — Tree-with-Capstone Convergence [Needs-Validation — TeamAOF-only].** A tree of N single-dependency quests followed by one capstone quest with `dependencies` on ALL prior quests (fan_in = N−1). Observed in AOF-6 Create (68-dep gear convergence, Case 52) and AOF-6 Botania (100+-dep hexagon convergence, Case 53). The capstone's task MUST be `checkmark` type to avoid AP37 convergence claustrophobia at this scale. Shape: gear or hexagon, size 3.0–4.0. **Scope restriction:** both data points come from TeamAOF/AOF-6 — this pattern may be team-specific. Do not apply to non-kitchen-sink packs without explicit author intent. Cross-validate against non-TeamAOF packs before adopting as universal pattern.
3. **MP73 — Sub-Region Decomposition for Large Chapters [Indirectly-Validated].** Chapters with 80+ quests decompose into 4–6 sub-regions (Miller's 7±2 working memory limit) at 4–8 units of x-y separation, each with its own hub quest and internal topology. Processing chains → linear_chain; collection catalogs → grid_catalog; variant items → hub_fan. Validated indirectly by 4 anti-pattern sources (AP28, Craftoria #231, PP20, post/2494) that penalize mega-chapters lacking structural compensation. Note: 80+ quest chapters using sub-region decomposition (MP73) are exempt from AP41's flat-hierarchy concern — spatial separation between sub-regions provides visual hierarchy even without shape diversity.
4. **Topology type distribution (Cases 49–54).** The 6 new cases span 3 topology types: tree_branching (4 cases: 49, 51, 52, 53), hub_fan (1 case: 50), grid_catalog (1 case: 54). tree_branching dominates non-expert mod-tutorial and progression chapters; hub_fan appears in boss-catalog organization; grid_catalog in farming/collection chapters.
5. **Reading direction for Chinese-language packs (Lesson 86).** Chinese tree_branching chapters (Case 49, No-Flesh-Within-Chest) use vertical top-to-bottom reading direction (root at top, progression flows downward), consistent with Chinese text layout conventions. This differs from most English-language packs where progression flows left-to-right. When generating for a Chinese-language pack, consider top-to-bottom as the default primary axis. This observation is based on 1 Chinese tree_branching case; additional Chinese packs are needed to confirm whether this is a cultural convention or individual author preference.

IDs are computed automatically by the generator from quest names — you write `name: "punch_wood"`, it owns the 16-hex ID (formula in reference §9; uniqueness is guaranteed pre-emit, see Step 4). Renaming a quest without `--mode ask` creates a new ID and breaks player progress; `reconcile_renames` maps old → new and preserves the original ID via the manifest's `aliases`.

Skeleton spec (Step 4 fills one quest's `tasks`/`rewards` at a time):

```json5
{
  pack: "create-astral",
  format: "json5",              // "json5" (main) | "snbt" (1.20.1 inline — detect, §12)
  default_locale: "en_us", locales: ["en_us"],
  data: { default_reward_team: false, default_consume_items: true },
  chapters: [{
    name: "getting_started", group: "", order_index: 0,
    default_quest_shape: "circle", layout: { mode: "auto" },
    quests: [
      { name: "punch_wood", depends_on: [], shape: "circle", tasks: [], rewards: [] },
      { name: "first_plank", depends_on: ["punch_wood"], shape: "circle", tasks: [], rewards: [] },
    ],
  }],
}
```

Title-only lang (descriptions are added per-node in Step 4):

```json5
{
  "@getting_started.title": "Getting Started",
  "@getting_started.chapter_subtitle": ["Welcome!"],
  "@getting_started/punch_wood.title": "Punching Wood",
  "@getting_started/first_plank.title": "First Plank",
}
```

Then generate the skeleton — the generator writes a clean `<output_dir>/quests/` tree (`data.*`, `chapters/*.json5`, `lang/*/quests.json5`, `.ftbq-cache/manifest.json5`); `quests.spec.json5` stays at `<output_dir>` root, never deployed. Same spec → byte-identical output; lang is add-only after first run (existing rewritten keys are never overwritten). With `format: "snbt"` the output is `.snbt` with no `lang/` (text inline) — see §12.

```bash
python scripts/generate_quests.py <output_dir>
```

### Step 4 — Polish one node at a time (the loop)

**Anti-囫囵 rule:** do NOT write the tasks/rewards for the whole book at once. Iterate over the outline nodes — but **scale the loop to the book**: ≤~20 quests → one node at a time with per-node sign-off (steps 1–7 below); ~20–100 → batch by chapter (co-author a chapter's nodes in the spec, regenerate + validate once per chapter, sign off per chapter); >~100 → batch by chapter and skip per-node sign-off, revisiting only quests the validator flags. The incremental merge + `content_hash` still protect untouched quests across a batch. This is where the user 打磨 each task.

Before the first node, load `reference/design/mod-description-trust.md §AP9–AP11` (AI-generation anti-patterns) as background context — these three risks (hallucination cascade, style homogenization, narrative inconsistency) are specific to AI-generated quest configs and inform every step below.

**Mandatory progression reasoning — every task and reward must pass a reachability and guidance test before it is written.** Step 4 embeds two reasoning gates into the per-node loop so that reachability and reward continuity are checked at generation time, not only after the whole book exists. For every `ftbquests:item` task you are about to write, you must answer "玩家此刻怎么拿到这个？" — verify that the task item is obtainable at the current progression stage, cross-referencing the stage-resource mapping and item-tier rules in `reference/design/progression-rules.md` §Item Reachability (R1–R4, R42); if the item requires an advanced crafting chain whose prerequisites span multiple prior quests, confirm those prerequisite quests already exist in the outline or have been generated earlier in this chapter. For every reward, you must answer "这个奖励引导玩家去做什么？" — verify that the reward functions as a material bridge or universal bridge into downstream content, following the reward-to-task linking constraints in `reference/design/progression-rules.md` §Reward Continuity (R10–R13, R44, R45); rewards should not be dead-end items (AP6) that the player has no in-book reason to use. The gates below (Gate 1 for tasks, Gate 2 for rewards) formalize these two questions with pass/fail criteria and lookup-table fast-paths; a third gate (Gate 3, dependency chain sanity) runs after the per-node anti-pattern checks. The reasoning is mandatory even when the fast-path auto-passes, and the formal whole-graph validation in Step 5 (R1–R32, R55–R64) catches anything the per-node check misses.

For each node:

1. **Pick one quest** (main-line order; side branches after their fork point). Say which one you're polishing.

2. **Co-author its content** — grill per the Step 2 interview discipline: ONE question with your recommended answer, wait for the user, then the next (task type + target + count → reward type + payload → description text). **Never dump a list of questions.** "帮我设计" → draft the content yourself, user approves/edits; "我要指定每个任务" → ask per task. Resolve mod mechanics / reward effects by checking the codebase or asking — never guess. Before writing a task/reward item, confirm its id is in `.ftbq-cache/items.json5` `all_item_ids` or `existing_quests.json5` `known_item_ids` (Step 1); if it isn't listed, ask the user to confirm it in JEI/EMI — **never invent an item id** (see "Verify, don't fabricate"). Before modifying any existing quest's tasks/rewards in the spec, re-read the spec file to confirm the quest's current state — do not edit from a stale outline or memory of a previous session. For a **collection quest / many-item batch**, resolve all the display names → ids in one call with `lookup_item.py <packroot> <name>…` (see "Batch item-id lookup") and write tasks from those results — don't grep `all_item_ids` N times. When writing the description text, follow **Quest text & description writing style** (near the top of this skill) — natural, concise prose, not label-value 要素式 checklists; the quest UI already shows the item/count/reward, so spend the description on the *why* and *how*.

   **Reasoning Gate 1: Task Item Reachability** — *mandatory before writing each `ftbquests:item` task to the spec.*

   For every item task, produce the following one-line reasoning **out loud** (in your working notes, not in the spec):

   > How does the player get [item_id] at this point? → [answer]

   Walk through the three checks below. Each check has a fast-path (L1 builtin table hit) and a slow-path (L1 miss → reasoning from context).

   | Check | L1 fast-path (item is in builtin table) | L1 miss (item NOT in builtin table) |
   |---|---|---|
   | **R1 Dimension** | Look up `BUILTIN_DIMENSION_MAP` (`reference/design/shared-builtin-tables.md §0`). If the item's dimension is NOT in the ancestor chain's unlocked dimensions → **GATE FAIL: P1 cross-tier**. Stop and surface to user. | Reason from the quest's ancestor rewards and the mod's context. If unsure → mark `[unverified:dimension]` and continue. |
   | **R2 Tool tier** | Look up `BUILTIN_TOOL_TIER_MAP` + `BUILTIN_ORE_REQUIREMENTS`. If the required tool/mining level exceeds what ancestors provide → **GATE FAIL: P2 cross-tier**. Stop and surface to user. | Reason from the mod's known tool progression. If unsure → mark `[unverified:tool_tier]` and continue. |
   | **R3 Recipe depth** | Run `estimate_recipe_depth_heuristic` on the item id. If estimated depth > quest dependency depth + 2 → **GATE FAIL: P2 depth mismatch**. Mark `[unverified:recipe_depth]` and surface. | Use **name-tier heuristic** as fallback: items containing `ingot`/`dust`/`gear`/`nugget` ≈ depth 1–2; `machine`/`circuit`/`processor`/`controller` ≈ depth 3–4; `multiblock`/`fusion`/`singularity` ≈ depth 5+. Mark `[unverified:recipe_depth]`. |

   **R42 Stage-Internal Item Reachability (additional check):** After the three checks above, each task item must additionally answer:

   > 玩家此刻怎么拿到这个？——引用 `reference/design/mod-item-reachability.md` R42（Stage-Internal Item Reachability）

   If the pack has L2 stage data (the `stage_map` and `stage_available_resources` collected in Step 2), check whether the item's crafting-chain leaf nodes fall within the current stage's reachable resource set. If no L2 data is available, fall back to the R1 (dimension) + R4 (stage boundary) L1 heuristic combination, and mark `[unverified:stage_recipe]`.

   Note: this is a semantic reinforcement of Gate 1, not a change to its pass/fail logic. Gate 1 already implicitly covers R1/R2/R3; this extension explicitly adds the R42 stage-internal resource reachability perspective.

   **Gate verdict:**
   - **PASS** (all checks pass or are deferred `[unverified]`) → write the task to the spec.
   - **FAIL** (any L1 hit returns P1/P2 violation) → do NOT write the task. Instead: (a) suggest an alternative item the player CAN reach, (b) suggest adjusting the dependency chain to unlock the required dimension/tool, or (c) ask the user to confirm they want this item here despite the gap. Only proceed with explicit user approval, and note the override in the spec comment: `// Gate 1 override: user confirmed [item] despite [reason]`.

   **Batch fast-path:** for collection quests with many item tasks, run Gate 1 once per batch. Resolve all item ids via `lookup_item.py` first, then run the three checks on each. Items that are vanilla or well-known (in the L1 tables) auto-pass; only flag items that fail or miss. Don't produce individual reasoning lines for items that trivially pass (e.g., `minecraft:oak_log` in the first quest).

   **Scope note:** Gate 1 applies only to `ftbquests:item` tasks. Non-item tasks (`checkmark`, `stat`, `advancement`, `dimension`, `biome`, `kill`, `structure`, `observation`, `xp`, `custom`) are exempt from item reachability — they have no item to check. For `ftbquests:fluid` tasks, apply the same gate logic substituting the fluid's source mod and production method for "dimension/tool/recipe depth".

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

   **R45 Reward Guidance Bridging (additional check — chapter-level):** After the four categories above, each reward must additionally answer:

   > 这个奖励引导玩家去做什么？——引用 `reference/design/mod-reward-design.md` R45（Reward Guidance Bridging）

   If the current quest is the chapter's capstone (the quest with the most dependents), check whether its reward includes an item or gamestage unlock needed by the next chapter's entry quest (a virtual bridge item). If the reward bridges neither an item nor a stage, flag it as a chapter-level dead-end risk.

   Note: this is a semantic reinforcement of Gate 2. Gate 2 already checks reward bridging at the quest level (R10); this extension raises the perspective to the chapter level (R45), ensuring chapter-to-chapter transitions have explicit reward guidance.

   **Backward matching (Step 4 practical note):** because Step 4 generates in dependency order (root → leaves), you often can't do a forward check (reward → dependent task) since dependent quests may not exist yet. Use **backward matching** instead: when generating quest B, check whether B's task items match any ancestor quest's rewards. The formal forward check runs in Step 5 (R10).

   **R28 Command reward safety (sub-gate):** if the reward type is `command`, this gate additionally requires passing the R28 Command Reward Safety Scan before writing — check against `FORBIDDEN_COMMANDS` (ERROR — block write), `HIGH_RISK_COMMANDS` (WARNING — surface to user), and `IDEMPOTENCY_RISK` (INFO — note). See `reference/design/mod-reward-design.md §R28`. Command rewards are the highest-risk reward type (AP15) — prefer `item`, `xp`, `loot` whenever possible.

   **R31 XP-level pre-check (sub-gate):** if the reward type is `xp_levels`, check whether this quest is a milestone/capstone (high fan-in, distinctive shape). Non-milestone `xp_levels` rewards drift in value with player level (AP17). If not a milestone, suggest flat `xp` instead or surface the risk to the user.

   **Batch fast-path:** when batching a chapter, run Gate 2 once per reward as you write the spec. The dead-end detection (AP6) is most effective after the full chapter's tasks are written — do a quick chapter-level dead-end sweep after the batch (alongside the teaching order check).

3. **Update ONLY that quest** in `quests.spec.json5` (fill its `tasks`/`rewards`) and its `quest_desc` / `quest_subtitle` in the **primary locale's** lang file. Leave every other quest's empty `tasks: []` untouched. Translate to secondary locales in a dedicated pass after the primary is settled (Step 4 done) — don't block each node's sign-off on every locale; the generator's lang is add-only per locale, so mirror the primary's keys. If no translator, ship the primary and flag secondaries for the user/pack team. In the spec, references use `name` (within a chapter) or `<chapter>/<quest>` (across chapters); raw 16-hex tokens pass through for existing-pack linkage (see "Task linkage" below).

4. **Regenerate** — `python scripts/generate_quests.py <output_dir>`. The incremental merge keeps every other quest pristine (content_hash match → no-op) and re-emits only the quest you touched; in-game position edits to other quests are preserved regardless of mode. The ID-uniqueness check runs pre-emit, so a name clash fails fast before any file is written.

5. **Verify that one quest** — `python scripts/validate_quests.py <output_dir>/quests/` (fast; diagnostics carry `file:line:col`), then preview JUST that quest instead of reading the whole chapter file:
   ```bash
   python scripts/quest_detail.py <output_dir> <chapter>/<quest>
   ```
   It resolves the quest by name (via the spec's pack + the id formula) and prints only that quest's id/shape/deps/tasks/rewards/lang — token-saving vs. reading the whole chapter.

6. **AI generation self-check (per node).** After the quest passes validation and before presenting the summary, review it for the three AI-specific anti-patterns (`reference/design/mod-description-trust.md §AP9–AP11`):
   - **Description-item consistency (R23).** Does the `quest_desc` mention any item ID that doesn't appear in this quest's tasks or rewards? Conversely, does the description fail to explain a task item that the player needs context for? The static rule in `reference/design/mod-description-trust.md` catches ID-level mismatches; at generation time, read the description you just wrote and confirm every named item matches the config, and every config item has a reason to be there.
   - **Style drift (AP10).** Compare this quest's description structure to the last 2–3 quests you polished. Are they all following the same template ("Obtain [item]. This is needed for [next step].")? Vary the description mode — how-to, lore, tip, challenge — so the chapter doesn't read like a form letter. Reward amounts and shape vocabulary should vary too (`reference/design/mod-description-trust.md §AP10` for detection heuristics).
   - **Narrative continuity (AP11).** If this quest's description makes a forward reference ("you'll need this for the next quest") or a difficulty claim ("the hardest craft so far"), verify the referenced quest actually exists and matches. Check that the tone (casual / technical / lore-heavy) is consistent with the chapter's established voice — a tonal lurch between adjacent quests breaks the player's trust in the book as a guide.
   - **Companion delegation (R47).** If `questbook_role == "companion"` and the description contains recipe patterns ("X + Y → Z", "put X in Y", "smelt X to get Y"), note as INFO — consider delegating recipe details to EMI/JEI. Reverse: if `questbook_role == "tutorial"` and the description says "check EMI/JEI for the recipe" or similar delegation language, flag as WARNING — tutorial mode should teach, not delegate to external tools.

   **Reasoning Gate 3: Dependency Chain Sanity** — *lightweight scan after the per-node anti-pattern checks pass.*

   Before presenting the summary (step 7), quickly scan this quest's local dependency context:

   | Check | Condition | Action |
   |---|---|---|
   | **Chain depth** | Count the longest `depends_on` path from this quest back to a chapter root. If depth exceeds the pack-type threshold (`kitchen-sink: 8`, `expert: 20`, `skyblock: 20`, `rpg: 12`, `create: 10` — from R9) or, more practically, exceeds the depth of neighboring quests by 3+ | **WARN** — note in summary: "Chain depth N exceeds threshold / neighbors by M. Consider a shortcut dependency or restructure." |
   | **Fan-out** | Count this quest's direct dependents. If > 5 (hub pattern) | **INFO** — note: "Hub with N dependents. Consider `hide_dependency_lines` (kitchen-sink) or `hide_until_deps_visible` (narrative) to reduce visual clutter." |
   | **Orphan risk** | This quest has no dependents AND no `optional: true` AND is not the last quest in the chapter | **WARN** — note: "Dead-end quest with no dependents and not marked optional. Either add a dependent, mark as optional, or verify it's intentionally a leaf." |
   | **Diamond rejoin** | This quest depends on multiple quests that themselves share a common ancestor (rejoin after fan-out) | **INFO** — note: "Diamond pattern detected. Verify `dependency_requirement` is correct (`all` = must do all branches, `one` = any branch suffices)." |

   Gate 3 is **advisory, not blocking** — it surfaces structural observations in the step 7 summary for the user to decide. Unlike Gates 1 and 2, it does not prevent writing to the spec. The formal versions of these checks (R5, R6, R7, R9) run in Step 5 with the full graph available.

   **Topology layout check (per chapter, after all nodes are polished):** Load `reference/design/progression-rules.md` §Section B and check R55–R64 for the chapter's chosen topology. Priority checks:
   - **R55** Topology-Progression Mode Alignment — does the chapter's `progression_mode` match the topology? Note the R41 early-game override: tutorial chapters (depth ≤ 3, ≤ 15 quests) may use `flexible` with `linear_chain` without triggering a warning.
   - **R57** Hub Node Size Dominance — if hub_fan or tree_branching, verify hub size > max child size.
   - **R60** Topology-Shape Vocabulary Coherence — shape count within the topology's guideline range.
   These are advisory at generation time (Step 4); the formal checks run in Step 5.

7. **Show a focused summary** of just that quest (id, tasks, rewards, lang title/desc) and ask: keep & continue, or revise? Only advance to the next node when the user is happy with this one.

**Chapter-level teaching order check.** After all quests in a chapter are polished (or after a chapter batch), step back and verify the chapter's internal teaching sequence. The two patterns to confirm are Teach-Then-Do (`reference/design/mod-teaching-pacing.md §MP11`) and Tier Escalation (`reference/design/mod-teaching-pacing.md §MP12`): for each mod mechanic the chapter covers, a teaching quest (checkmark/stat task + long description explaining the concept) should appear *before* the doing quest (item task requiring the player to apply what was taught); and within a material or tool tier, quests should escalate from cheapest/simplest to most expensive/complex. The formal rules R14–R17 (`reference/design/mod-teaching-pacing.md`) detect inversions statically; at generation time, read the chapter's quest list in dependency order and confirm that no doing-quest precedes its teaching-quest, and no high-tier quest appears before a lower-tier one. If you find an inversion, reorder the `depends_on` chain in the outline and update the spec before moving to the next chapter. This is also the moment to check for AP9 hallucination cascade (`reference/design/mod-description-trust.md §AP9`) across the whole batch — scan every item ID introduced during this chapter's generation against `items.json5` one more time, rather than trusting that each per-node check was sufficient.

**Progression architecture check (Cycle 16 — author design practice rules R101–R105).** After the teaching order check, run the following architecture-level validations. These rules derive from author interviews and Chinese pack-making community design wisdom (Cycle 16 Phase 3); they are advisory at generation time and formal in Step 5's whole-book pass:
- **R101 Multi-Layer Stage Enforcement.** If the pack uses stage-framework mods (Game Stages, Item Stages, Recipe Stages, Ore Stages, Dimension Stages, TinkerStages), verify that stage boundaries are enforced at multiple layers — not only quest-book `depends_on` but also recipe gating and item access. A single-layer lock is fragile; defense-in-depth is the author-consensus best practice for expert and semi-gated packs. See `reference/design/progression-rules.md` §R101 for implementation details.
- **R102 Era-Based Architecture.** If the pack has more than 10 chapters, check whether chapters are grouped into eras (2–5 related chapters forming a coherent progression phase with introduction, escalation, and capstone). Era-based organization prevents both item cross-tier and sequence inversion at the structural level. See `reference/design/progression-rules.md` §R102 for implementation details.
- **R103 Tutorial Anchor.** Verify that the first quest in each chapter (especially Chapter 1) satisfies the anchor conditions: no dependencies (it's the entry point), a description long enough to orient a new player, and at least one starter reward that teaches the reward economy. The tutorial anchor is the quest the player returns to when confused — it should be designed as a permanent reference, not a throwaway. See `reference/design/progression-rules.md` §R103 for implementation details.
- **R104 Crafting Variety.** For each stage or era, check whether more than 60% of the quests use the same crafting method (e.g., all shaped crafting, all machine processing). If so, flag as mechanical monotony risk — the author-design-practice consensus is that variety within a stage prevents the repetitive grinding that leads to player attrition. See `reference/design/progression-rules.md` §R104 for implementation details.
- **R105 60% Accessibility.** Verify that a casual player following the main quest line can access at least 60% of the pack's content without pursuing side quests or optional challenges. If the accessible content falls below this floor, the pack's late-game is gated behind a completionist wall. This is a design-intent metric (player experience), not a QA coverage metric. See `reference/design/progression-rules.md` §R105 for implementation details.

**Progression architecture check (Cycle 17 — international author design practice rules R106–R116).** After the Cycle 16 architecture check, run the following additional validations. These 11 rules derive from both Chinese pack-making community design philosophy (MC百科 thread-21004, post/4382) and international pack analysis (SevTech Ages, AOF-6, Craftoria); they are advisory at generation time and formal in Step 5's whole-book pass. Not all rules apply to every pack — route by pack type:

- **kitchen-sink packs:** R107 (olive-shaped equipment distribution), R110 (mid-game density priority), R112 (vanilla enhancement layering)
- **expert packs:** R109 (forced anti-skip material binding), R115 (container-level recipe locking), R101 (multi-layer stage enforcement, from Cycle 16)
- **adventure/RPG packs:** R106 (dimensional progression naturalism), R108 (gear-to-mob cross-dimension scaling), R113 (multi-dimensional state synchronization)
- **farming/lifestyle packs:** R110 (mid-game density priority), R111 (anti-forced-lifespan extension), R112 (vanilla enhancement layering)
- **all pack types:** R114 (quest-to-stage reward bridge — if using Game Stages), R116 (advancement-as-progression-gate — if using vanilla advancements as progression system)

Rule details and implementation checks: `reference/design/progression-rules.md` §Section G (R106–R116). Key notes:
- **R106** requires ≥3 same-dimension prerequisites before a dimension-gating quest. Does not apply to skyblock or single-dimension packs.
- **R108 L1 heuristic fallback:** When DPS/HP data is unavailable (the common case — FTB Quests config does not contain combat stats), degrade to: (a) namespace keyword tier inference — items containing `netherite`/`dragon`/`end` → late-tier, `iron`/`diamond` → mid-tier, `wood`/`stone` → early-tier; (b) `BUILTIN_TOOL_TIER_MAP` equipment tier comparison (if both dimensions' equipment is in the builtin table); (c) if neither heuristic resolves, mark `[unverified:combat_balance]` and surface to user. The 3×/0.3× DPS thresholds are initial heuristics requiring calibration from combat data across 3+ packs.
- **R109** is the world-generation enforcement layer of the item cross-tier defense (complementing R101's runtime locking and R115's container locking). Check world-gen configs when available; otherwise ask user.
- **R114** is the critical link between FTB Quests and Game Stages ecosystem — verify that chapter-final quests have `command` rewards granting the appropriate game stage. ERROR severity for expert packs, WARNING for semi-gated.
- **R115** applies only to expert packs with Recipe Stages + automation mods (AE2, RS, Create). Risk detection from modlist is fully executable; config verification requires reading `/scripts/` or `/config/recipestages/`.

Three new tensions from Cycle 17 (documented in `reference/design/progression-rules.md`):
- **Tension 7:** R106 (naturalism) vs. R101 (multi-layer enforcement) — resolved as complementary: naturalism as design intent, enforcement as safety net.
- **Tension 8:** R107 (olive-shaped distribution) vs. R111 (anti-forced-lifespan) — resolved as quality vs. quantity: R107 targets meaningful equipment variety, R111 targets repetitive content inflation.
- **Tension 9:** R112 (vanilla enhancement layering) vs. R110 (mid-game density) — resolved by parallel introduction: introduce multiple mods simultaneously to maintain mid-game density while building on vanilla foundations.

**Batching by chapter:** fill all of a chapter's quests' `tasks`/`rewards` in `quests.spec.json5`, then run `generate_quests.py` once + `validate_quests.py` once; use `generate_quests.py --dry-run` to preview the batch before committing. Run `quest_detail.py` per node only for quests that fail validation or that you want to spot-check. When batching:
- **Gate 1 (Item Reachability)** and **Gate 2 (Reward Bridge)** apply per-quest as you write it into the spec — produce the one-line reasoning for each task item and each reward. Use the batch fast-path: items that are vanilla or in L1 tables auto-pass; only produce explicit reasoning lines for items that fail or miss.
- **Gate 3 (Dependency Chain Sanity)** and the **chapter-level teaching order check** run once after the whole batch is written — scan the entire chapter's dependency graph at that point.
- The AI self-check (step 6) runs per-node during the batch, but AP10 (style drift) and AP18 (reward desert) are most effective as a chapter-level sweep after the batch.

Re-run modes:

```bash
python scripts/generate_quests.py <output_dir>                  # default: overwrite skill-owned, preserve user-added
python scripts/generate_quests.py <output_dir> --mode preserve  # keep ALL on-disk edits
python scripts/generate_quests.py <output_dir> --mode ask       # prompt per conflict
python scripts/generate_quests.py <output_dir> --adopt          # first run on an existing pack
```

**Before `--mode ask` / `--adopt` on an existing pack**, check blast radius first: the manifest + validator catch quest dependency chains; if CodeGraph is available, also run `codegraph_impact` on the target quest files — it adds cross-file references (lang keys, `quest_links`) the manifest misses. Either source finding affected quests the other missed is a signal to stop and confirm with the user.

Reward tables (`reward_tables[]`), quest links (`quest_links[]`), and chapter images (`images[]`) can be authored whenever their owning quest comes up in the loop — add them to the spec and regenerate the same way. The `@<chapter>/<quest>.subkey` lang placeholders (subkeys: `title`, `quest_subtitle`, `quest_desc`, `chapter_subtitle`) are rewritten to `quest.<HEX>.subkey` on generate; with `format: "snbt"` the generator emits **inline** `title`/`subtitle`/`description` on the quest/chapter objects (the 1.20.1 variant — the only SNBT variant it emits; the 1.21.1 SNBT+lang variant is adopt-only, see the CRITICAL detection rule).

### Step 5 — Whole-book verify & balance

Per-node validation already ran inside the Step 4 loop; this is the final whole-book pass once every node is polished. Run the validation script (the quests root is `<output_dir>/quests/`):
```bash
python scripts/validate_quests.py <output_dir>/quests/
python scripts/validate_quests.py <output_dir>/quests/ --strict       # also: --fix (autofix), --json (CI)
```
If the script is unavailable, see reference §15 for the full diagnostics catalog and self-check against it.

The whole-book validation runs the full progression-rules pipeline (R1–R32, distributed across the modular reference files — see `reference/design/module-index.md` for routing) — item reachability across the complete dependency graph, reward continuity across all chapters, teaching order for every chapter, description consistency for every quest, command safety, team progression consistency, and chapter-level QA heuristics. The Step 4 per-node checks are a generation-time subset; Step 5 catches cross-quest and cross-chapter issues that only become visible once the full graph exists.

**Topology validation (R55–R64 — Cycle 11 addition):** After the core R1–R32 pipeline, run the topology-aware layout rules from `reference/design/progression-rules.md` §Section B. Load `reference/design/topology-coordinates.md` for the classification algorithm and coordinate data. Execution order:
  1. **R58** (P0) Collision-Free Adjacent Nodes — all-pairs distance check. This is the primary layout invariant; overlapping quests are the most basic layout failure.
  2. **R55** (P1) Topology-Progression Mode Alignment — verify each chapter's topology matches its progression_mode. Apply R41 override for early-game chapters.
  3. **R56** (P1) Depth-Axis Monotonicity — deeper quests should appear further along the primary axis.
  4. **R59** (P1) Bounding Box Viewport Fit — chapter fits within 35×30 unit viewport.
  5. **R61** (P1) Convergence Point Visual Prominence — convergence nodes at visual terminus.
  6. **R57** (P2) Hub Node Size Dominance — hub size hierarchy.
  7. **R62** (P2) Parallel Column Spacing Uniformity.
  8. **R63** (P2) Grid Catalog Aspect Ratio.
  9. **R64** (P2) Decorative Image Topology Alignment.
  10. **R60** (P3) Topology-Shape Vocabulary Coherence.

Print topology validation results as part of the summary:
```
Topology validation: {pass/warn/error}
   Chapters checked: {N} | Topology types: {list}
   R58 collisions: {count} | R55 alignment: {count} | R59 viewport: {count}
```

> **Dev testing — scope it.** When you change skill code (scripts/, ftbq/) during a session, avoid running the full test suite on every iteration. Run only the test module(s) that cover what you touched — see the "Test → source map" in `CONTRIBUTING.md`. Reserve the full suite for pre-push / pre-release / shared-surface changes (the JSON5 parser, the canonical emitter, the `generate()` signature).

Then print a summary (in the user's language — see "Language — match the user"):
```
✅ Generated FTB Quests config (modern JSON5):
   📚 N chapters   📋 N quests   🎯 N tasks   🎁 N rewards   🎲 N reward tables   🌐 N lang entries
   Output: {dir}/quests/   (clean, copy-ready)
   New pack: copy <output_dir>/quests/ into <packroot>/config/ftbquests/quests/
   Existing pack: python scripts/generate_quests.py <output_dir> --deploy <packroot> --yes
                  (merges additive files, backs up overwritten originals — see Step 5b)
   then in-game /ftbquests editing_mode
   If titles appear blank: you're on the inline-text (older .snbt) version — see reference §12.
```

**Questbook role stats (R46) — always print after summary:**
```
📖 Questbook role: {declared_role}
📊 Reward density: {total_rewards / total_quests}
📋 Optional rate: {optional / total}
⚠️ Role consistency: {consistent/inconsistent — flag if reward_density contradicts declared role}
```

**Port drift indicators (R48) — print only when detected:**
```
🔀 Suspected ported quests: {count}
   - Foreign mod references in descriptions: {n}
   - Item namespaces not in modlist: {n}
   - Reward distribution outliers (>2σ from R34): {n}
   Review recommended before release.
```

**Catalog maintenance (R49) — print only when any chapter has >200 quests:**
```
📦 Large catalog chapter "{name}": {n} quests covering {m} mods
   Maintenance risk: {low/moderate/high} — consider tag-based tasks for auto-inclusion
```

**Zero-reward safety (R50) — print only when reward_density < 0.05:**
```
🚫 Zero/near-zero reward design detected.
   ☐ Alternative progression currency: {yes/no — list if yes}
   ☐ Questbook role: {companion/catalog/other}
   ☐ Strong intrinsic gameplay loop: {yes/no — list type}
   Result: {SAFE / WARNING — missing conditions: ...}
```

**Balance review (optional):** after the summary, offer to re-grill the user about pacing against the generated config — early quests too trivial/grindy? (recommend 3-5 min/quest first hour); rewards scale with effort? (~2× time-value); choke points? (every 3rd quest an alternative path); mod progression natural? (unlock when players want them).

### Step 5a — Load-test in-game (the static validator can't catch runtime failures)

`validate_quests.py` is static — it catches schema/dependency errors but NOT runtime load failures: a KubeJS `custom` task pointing at a missing script, an item id the registry rejects, a reward-table ref that doesn't resolve. Before deploying to a live pack, load-test:

1. Copy the generated `<output_dir>/quests/` into a throwaway test profile (or the target pack in a backup profile).
2. Launch the game, run `/ftbquests reload` (or open the quest book).
3. Confirm the book opens with no chat errors, chapter/quest counts match the Step 5 summary, and a sample quest's task triggers + its reward grants.
4. Flag every `custom` / KubeJS-scripted task and reward as "needs in-game verification" — they can't be statically validated.

If the user can't launch, at minimum have them `/reload` and screenshot the book; treat any scripted task as unverified until they do.

### Step 5b — Deploy to game folder (merge into an existing pack)

For a **brand-new pack**, just copy `<output_dir>/quests/` into `<packroot>/config/ftbquests/quests/` — the folder is clean and copy-ready, and file names are unchanged so it's easy to find what landed where.

For an **existing pack**, avoid blind-copying — that would clobber `data.json5`, `chapter_groups.json5`, the lang file's other-quest keys, and any same-named chapter. Use the built-in deploy instead: it detects every overwrite, merges additive files, and backs up originals:

```bash
python scripts/generate_quests.py <output_dir> --deploy <packroot> --spec <output_dir>/quests.spec.json5  # preview (writes nothing)
python scripts/generate_quests.py <output_dir> --deploy <packroot> --yes                                   # apply after the ⚠️ OVERWRITE block; --quests-dir targets a custom dir
```

What `--deploy` does (full table in reference §16):
- **NEW** files → copied verbatim (names unchanged).
- **`data.json5` / `chapter_groups.json5` / lang** → **merged** so the skill's content and the pack's existing content coexist in one file — new + original together, as you asked. The pack's other-quest lang keys are preserved; this is the regression a blind copy would have destroyed.
- **`chapters/<name>.json5`** that already exists → **backed up** then replaced wholesale (the skill's chapter wins). The original lands at `<target>/.ftbq-backup/<ts>/chapters/<name>.json5` — same name, same relative path, so it's trivial to find next to its replacement.
- **`.ftbq-cache/manifest.json5`** → backed up + replaced (skill memory; scanner-safe).

The ⚠️ **OVERWRITE** block in the report is the prominent highlight for every file that touches a modpack original — review it before adding `--yes`. Backups live under `<target>/.ftbq-backup/<timestamp>/` (dot-prefixed, so FTB Quests' scanner skips it — same reason `.ftbq-cache/` is safe; reference §14), with a `BACKUP_INDEX.json5` listing what was backed up and why. To roll back, restore from that folder. `--no-backup` skips backups (dangerous, irreversible).

Need **quest-level** merge (keep an individual pack quest inside a chapter the skill also owns)? That's a different path: point `generate_quests.py` at the pack's quests folder directly with `--adopt` / `--mode ask` — the manifest then distinguishes skill-owned vs user-added quests quest-by-quest. `--deploy` is intentionally file-level and predictable.

**Remember the run (if CodeGraph memory is available):** capture this session's decisions — theme/tone/locales, reward & `consume_items` philosophy, gating, any renames/ID aliases, and anything the user corrected you on — so the next run on this modpack pre-fills the Step 2 interview instead of re-asking. Skip if the memory toolchain is absent; nothing about generation depends on it.

---

## Special workflow — DLC vs installed audit (optional)

When the task is **comparing a DLC source pack against an installed pack** (a diff/audit task, not generation), load `reference/audit-workflow.md` and follow its resume-first flow (`scripts/audit_diff.py` resumes from a cached `audit_report.json5` when both packs are fresh). This is outside the main generation Protocol.

## Quest layout patterns (spatial arrangement & anti-clutter)

**Measured best practices** (from 4 large chapters in a polished Create-series pack) for arranging quests so dependency lines don't cross. Apply whenever you assign `x`/`y` — via `layout: { mode: "auto" }` or by hand.

### Three layout families — pick one per chapter, don't mix

| Family | When to use | Aspect | Spine | Hub handling |
|---|---|---|---|---|
| **Narrative/progression** | Story-driven chapter with a main path + branches | ~2:1 (wider than tall) | Horizontal line at `y=0`, x-step 3.5 | Vertical fan-out sub-trees |
| **Kitchen-sink/ATM** | Per-mod chapter in a kitchen-sink pack (ATM-style) | 1:1 to 3:1 | Compact grid, x-step 0.5–1.0 | `hide_dependency_lines` over spatial separation |
| **Reference/catalog** | Lookup grid of variants/tiers (no story order) | ~1:1 (square) | None — uniform grid | Adjacent-cell deps only |

The **kitchen-sink/ATM family** has 5 sub-templates (Compact Horizontal Spine, Vertical Tiered Cascade, Parallel Material Columns, Radial Hub, Decorated Freeform), plus **2 cross-genre templates** (Hexagonal Expert Web for GregTech/expert packs, Narrative World Map for RPG/adventure packs) — full parameters, coordinate examples, and a selection decision tree in `reference/design/design-guide.md §atm-layout-patterns`. Genre-specific authoring patterns (expert gating, skyblock openers, magic spell-trees, RPG map reveals, Create age-based chapters) in `§pack-type-patterns`. Key difference from narrative: tighter grid (0.5-unit vs 3.5-unit x-step), `hide_dependency_lines` as the primary anti-clutter lever (vs `hide_until_deps_visible` for narrative), and shape (not size) as the main semantic encoder.

### Narrative layout — fan-out model

The horizontal-spine + vertical-fan-out cluster model (x-step 3.5, hub/step alternation, inverted-funnel dependents within ~2.5 hub radius, shared y-lanes) lives in `reference/design/design-guide.md §layout-reasoning` — load it when assigning x/y by hand.

### Clutter-reduction flags — depends on your layout family

| Flag | What it does | Narrative packs | Kitchen-sink/ATM packs |
|---|---|---|---|
| `hide_until_deps_visible: true` | Quest (and its lines) stay **hidden** until its dependencies are visible/complete | **Primary lever** — on most branch/leaf quests in chapters >~30 quests (~25% of quests in a polished 80-quest chapter) | Rare — used only on gating/secret quests (~3% of ATM10) |
| `hide_dependency_lines: true` | Hides only the dependency *lines* (quest stays visible) | Surgically on specific crossing edges | **Primary lever** — ATM10 uses ×438; on hubs with >3 dependents and long cross-column lines |
| `hide_dependent_lines: true` | Hides lines from this quest TO its dependents | Same as above (surgical) | Same — rare, surgical use |
| `secret: true` | Quest is hidden until discovered | Hidden/bonus quests; pair with `rsquare` shape, `size: 1.5` | Rare (ATM10 uses ×0); kitchen-sinks prefer `optional` (×553) |

**Rule of thumb:** narrative/story chapters → `hide_until_deps_visible` first. Kitchen-sink/catalog chapters → `hide_dependency_lines` first. Both can coexist in the same book (different chapters, different families).

### Shape & size = semantic encoding (read importance at a glance)

| Shape | Meaning | Typical size | ATM usage pattern |
|---|---|---|---|
| `gear` | Create machine milestone (big moments) | 2.0 | Hub/section leader (avg 1.75) |
| `square` | Stat/advancement-based sub-hub | 2.0 | Sub-hub, variant grouping |
| `circle` | Small intermediate step | 1.0 | Default — leaf/intermediate (most common) |
| `rsquare` | Secret or special optional | 1.5 | Recipe cells, optional content (ATM: 26% of explicit shapes) |
| `pentagon` | A tier/variant in a parallel set | 1.0 | Capstone convergence node (ATM Star `size 5.0`) |
| `hexagon` | Cross-chapter `quest_links` only | 2.0 | Mid-tier connector, cross-link (ATM: 4%) |
| `diamond` | Special/one-off | 1.0–1.5 | Material-tier identity (ATM Allthemodium `default_quest_shape`) |
| `octagon` | — | 1.0–1.5 | Major branch point (ATM: ~3%, used as tier-gate hub) |

**Size distribution (ATM9/ATM10 combined, 883 quests):** default (1.0) ~70%, 1.2–1.25 ~15%, 1.5 ~5%, 2.0+ ~2%. Kitchen-sinks use size more conservatively than curated packs (Create: Delight peaks at 2.0 for hubs).

### Side quests & secrets — push to the periphery

Place secrets/schematics/links at chapter margins (large |y| or far x); full guidance in `reference/design/design-guide.md §layout-reasoning`.

### Anti-patterns to avoid

The 7 anti-patterns (long diagonals, stacking, crossing lines, unbounded fan-out, all-lines-visible, y-scatter, mixing families) live in `reference/design/design-guide.md §layout-reasoning`.

### Coordinate conventions

- Coordinates are **per-chapter-local** (negative used freely; chapter sits at any global offset). Typical 80-quest narrative bounds: x ~29, y ~15 (aspect ~2:1). y-step between branch rows: 2.5–3.0 (narrative), 0.5–1.5 (catalog). x-step 3.5 and hub radius ≤2.5 are in the narrative section above.

### Chapter grouping & visual hierarchy (what the player sees)

Tabs (`chapter_groups`), icons, semantic color, progressive-reveal UX — full guidance in `reference/design/design-guide.md §layout-reasoning`. Quick: group ~5–8 chapters/tab; every chapter gets an `icon`; `hide_until_deps_visible` is the progressive-reveal lever above ~30 quests/chapter; `quest_links` (hexagon) for cross-listing, not duplicates.

---

## Field findings from shipped modpacks

The empirical evidence behind the design rules — Create: Delight Remake + Mechanomania audits, lessons 1–5, the culinary/recipe-catalog patterns, the ATM9/ATM10 kitchen-sink research, lessons 6–14, and the ATM10 deep-dive — lives in `reference/design/design-guide.md §field-findings`. **Load it when you need "what do shipped packs actually do?"** (shape/size/anti-clutter flag usage, reward densities, task-type frequencies, spine models measured on real books). Two-sentence digest: Create: Delight (1.20.1, SNBT inline, 2,295 quests) is the large-polished-layout + rich-reward reference; Mechanomania (1.21.1, SNBT+lang, 395 quests) is the minimalist reference. ATM10 (1.21.1, 4,601 quests / 64 chapters) grounds the kitchen-sink/capstone model.

## Token discipline

This skill is invoked by an LLM, so every file read and every line of script output is token spend. Prefer the compact, server-curated commands over reading raw files:

| You want to… | Run this | NOT this |
|---|---|---|
| Orient on a pack (start of any conversation) | `python scripts/pack_briefing.py <packroot>` | reading `mods.json5` / `existing_quests.json5` / chapter files raw |
| Get the DLC-vs-installed audit verdict (new conversation) | `python scripts/audit_diff.py <dlc_pack>` (auto-resumes if fresh) | re-reading both packs' quest files |
| Verify one quest after polishing it (Step 4 loop) | `python scripts/quest_detail.py <output_dir> <chapter>/<quest>` | reading the whole chapter file |
| Look up an exact field/type (rare) | read only the named reference § (e.g. §7) | reading all of `reference/ftb-quests-reference.md` |
| Look up a verified item id (before writing a task) | grep `.ftbq-cache/items.json5` `all_item_ids` / `existing_quests.json5` `known_item_ids` | guessing the id from the mod name |
| Resolve N item names → ids in one pass (collection quest / many-item batch) | `python scripts/lookup_item.py <packroot> <name>…` | N× grep `all_item_ids` / guessing ids from the mod name |

Rules of thumb:
- **Caches are the source of truth, not the files.** `.ftbq-cache/` (`mods.json5`, `items.json5`, `item_names.json5`, `existing_quests.json5`, `audit_index.json5`, `audit_report.json5`, `manifest.json5`) holds the structured digest. Read a cache via the briefing/diff/lookup commands, not the raw file.
- **Read raw quest files ONLY when authoring a specific quest's content** in the Step 4 loop — and even then, `quest_detail.py` gives you the one quest without the rest of the chapter.
- **One command's curated output beats several file reads.** If a script can answer it, run the script.
- **Reference doc is sectioned (§7, §9, §12…) on purpose** — read the section you need, not the whole file.

## Task & reward types (quick reference — full details: reference §7)

**Tasks:** `ftbquests:item` · `fluid` · `forge_energy` (Forge) · `xp` · `kill` · `advancement` · `stat` · `location` · `dimension` · `biome` · `structure` · `observation` · `gamestage` · `checkmark` · `custom`

**Rewards:** `ftbquests:item` · `xp` · `xp_levels` · `command` · `loot` · `random` · `choice` · `all_table` · `advancement` · `toast` · `gamestage` · `custom` · `currency` (off by default)

**Shapes:** `circle square diamond pentagon hexagon octagon heart gear rsquare rdiamond puzzle shield` (default `circle`)

**Format gotchas to remember:**
- `loot`/`random`/`choice`/`all_table` rewards reference a reward table via `table_id` (a decimal **long**, not hex) — in the spec use `table: "<name>"`; see reference §17.
- Command rewards run as the **player** (not op) unless `permission_level` (1-4); FTB Quests substitutes `{p}`/`{x}`/`{y}`/`{z}`/`{team}`/`{quest}`… in the command string. For a literal player target, **`@p`/`@a` selectors also work** (shipped packs use `command: "/say Hi, @p!"`) — use `{p}` when you need the name substituted into a non-selector context.
- `gamestage` is the type id for both stage tasks and rewards (not `stage`).
- Reward-table `hide_tooltip`/`use_title` default to **true** when absent — emit them explicitly (the generator does, defaulting to `false`).

## Task linkage — depend on existing pack quests

`depends_on` normally references skill-generated quests by `name` (within a chapter) or `<chapter>/<quest>` (across chapters). It also accepts **raw 16-hex IDs** for quests this skill did **not** generate — hand-written chapters, another tool's output, a community book indexed in Step 1. A hex token is passed through to `dependencies` verbatim, so a new quest can gate after existing pack content without the skill re-owning that quest's ID:

```json5
{
  name: "first_create_quest",
  depends_on: ["getting_started", "A1B2C3D4E5F60718"],  // name → resolved; hex → passed through
  tasks: [ /* … */ ],
}
```

Rules:
- A token is treated as an external hex ID only if it is exactly 16 hex characters `[0-9A-Fa-f]`. Don't name a skill quest with a 16-hex-looking name — it would be misread as an external reference.
- Use the exact ID from the Step 1 cache (`.ftbq-cache/existing_quests.json5`), uppercased. The generator normalizes case, but the cache is the source of truth.
- If the referenced existing quest is later deleted from the pack, the validator's `E_DEP_MISSING` catches it — re-run Step 1 and drop the stale hex from `depends_on`.

---

## Integration

- **KubeJS custom tasks/rewards:** `type: "ftbquests:custom"` referencing the pack's KubeJS scripts for the logic.
- **Recipe viewing:** tasks auto-integrate with JEI/REI/EMI; `default_quest_disable_jei` in `data.json5` hides a pack from recipe viewers.

## Format mismatch / unknown version

If the detected format does not match any pattern described here (neither modern JSON5 nor legacy SNBT):
1. Tell the user the format appears to be from a newer or unrecognised FTB Quests version.
2. Suggest checking the [`FTBTeam/FTB-Quests`](https://github.com/FTBTeam/FTB-Quests) repo for recent format changes.
3. Fall back to the closest matching format and clearly note what was assumed.
4. If `manifest.json` or `mods/` is missing, ask the user to confirm the mod list manually instead of guessing.

---

## Sources
Format verified against FTB Quests source 2026-06-25: [`FTBTeam/FTB-Quests`](https://github.com/FTBTeam/FTB-Quests) (`main` MC `26.1.x` JSON5 + `1.20.1/main` SNBT), [`FTBTeam/FTB-Library`](https://github.com/FTBTeam/FTB-Library) (SNBT), [`marhali/json5-java`](https://github.com/marhali/json5-java). The 1.20.1 SNBT format (§12) is implemented in `ftbq/snbt.py` (emitter+parser), confirmed against the Java source (`BaseQuestFile`/`Quest`/`ItemTask`/`ItemReward`/`XPTask`/`RewardTable`/`QuestLink`/`ChapterImage`); reward tables (§17), quest links (§18), chapter images (§19), top-bit ID mask (§9), item-count/XP-`points`/command-placeholder corrections (§7) likewise confirmed. Generator/manifest (§13/§14), validator diagnostics (§15), deploy layout (§16) in reference.

**Empirical data** audited 2026-06-29 (reference §20) against Create: Delight Remake (1.20.1) + Mechanomania (1.21.1) — ground the field-findings layout/reward lessons. **ATM-series data** researched 2026-06-30 from `AllTheMods/ATM-9` + `AllTheMods/ATM-10` repos, `alltheguides`, Discussion `#3539`, ATM9's KubeJS lang, plus Create: Astral, FTBTeam issue #1136, r/feedthebeast — ground the kitchen-sink / progression sections in this skill and the synergy / text-style / ATM10 deep-dive content in `reference/design/design-guide.md` (lessons 6–14). **ATM10 file audit** (4,601 quests / 64 chapters, parsed via `ftbq/snbt.py`) grounds `reference/design/design-guide.md §principles` (F1–F3, P1–P7). **ATM9/ATM10 layout audit** 2026-07-05 (12 chapters / 883 quests, 6 per pack) — ground `reference/design/design-guide.md §atm-layout-patterns` Templates 1–5 (kitchen-sink layout templates with measured spacing, shape-role correlations, and grid parameters). **Cross-genre pack audit** 2026-07-05 (8 additional packs, ~40 chapters / ~2,800 quests: Monifactory, ATM6-Expert, ATM9-Sky, Arcana, Prominence II RPG, Create: Astral, Create Skylands, Enigmatica 9, ATM-11) — ground Templates 6–7 (Hexagonal Expert Web, Narrative World Map) and `§pack-type-patterns` (expert gating, skyblock openers, magic spell-trees, RPG map reveals, Create age-based chapters).

**Progression validation framework** developed 2026-07-05, now organized as modular reference files (see `reference/design/module-index.md` for the full index): 32 rules (R1–R32), 34 micro-patterns (MP1–MP30 + PP1–PP6), and 11 anti-patterns (AP1–AP11) distributed across `mod-item-reachability.md`, `mod-dependency-graph.md`, `mod-reward-design.md`, `mod-teaching-pacing.md`, `mod-description-trust.md`, `mod-system-safety.md`, `mod-atm-signature.md`, and `shared-builtin-tables.md`. Grounded in the same 11-pack audit corpus as the design guide, plus cesspit.net expert-pack analysis, FTBTeam/FTB-Modpack-Issues #6447 player feedback, GTNH/E2E Extended design documents, and awesome-packdev community toolchain references.
