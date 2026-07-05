# FTB Quests — Authoritative Reference

Deep reference for generating FTB Quests configs. Verified against `FTBTeam/FTB-Quests` source on 2026-06-25 — current `main` (MC `26.1.x`, JSON5) **and** `1.20.1/main` (SNBT). The 1.20.1 SNBT format is documented in §12 (emitter/parser: `ftbq/snbt.py`); reward tables (§17), quest links (§18), chapter images (§19), the top-bit ID mask (§9), and the item-count / XP-`points` / command-placeholder corrections in §7 were all confirmed against the Java source. See also the memory note `[[ftb-quests-format]]`.

> **Read this if:** you need exact field names, type-specific parameters, a full worked example, or must target an older `.snbt` modpack. The main `SKILL.md` has the essential templates.

---

## 1. JSON5 syntax (current `main`) — the rules that break things

> This section is the **JSON5** format (current `main`, MC `26.1.x`). For **SNBT** (`.snbt`, used by both 1.20.1-inline and 1.21.1+lang packs — see §12), the rules are nearly the opposite (no commas, TAB, suffixed numbers, `#` comments, **short** type ids, bare-string items allowed).

Modern FTB Quests serializes via the `de.marhali:json5` library with default options. Every file **must** parse as JSON5:

| Rule | Correct | Wrong (legacy SNBT) |
|------|---------|---------------------|
| Separator | commas between members, trailing comma OK | "no commas" |
| Numbers | plain `0.0`, `16`, `-5` | `0.0d`, `16L`, `1b` |
| Booleans | `true` / `false` | `1b` / `0b` |
| Indentation | 2 spaces (pretty) | — |
| Keys | unquoted if valid identifier; quoted if contains `.`/space/digit-first (`"quest.ABC.title"`) | — |
| Strings | double-quoted `"text"` (single quotes also parse) | — |
| Comments | `//` and `/* */` allowed | — |
| Items | objects `{ id:"minecraft:x", count:N }` | bare string `"minecraft:x"` |

A file with no commas, or `1b`-style suffixes, or a bare-string item, will either fail to load or silently lose data.

---

## 2. Minimal pack layout

```
config/ftbquests/quests/
├── data.json5              # required, file-level settings
├── chapters/
│   └── <filename>.json5    # one per chapter
└── lang/
    └── en_us/
        └── quests.json5    # all text for this locale
```

`chapter_groups.json5` and `reward_tables/` are **only needed if** you use multiple chapter tabs or loot/choice/random/all_table rewards. For a single-group pack, chapters use `group: ""` (the implicit default group) and `chapter_groups.json5` can be omitted.

---

## 3. `data.json5` / `data.snbt` (required)

The file-level settings. Named `data.json5` for `format: "json5"` (current `main`) or `data.snbt` for `format: "snbt"` (1.20.1 & 1.21.1, §12); the settings below apply to both. `version` is `13` in both branches.

```json5
{
  version: 13,
  default_reward_team: false,
  default_consume_items: false,
  default_autoclaim_rewards: "default",
  default_quest_shape: "circle",
  default_quest_disable_jei: false,
  emergency_items_cooldown: 300,
}
```

All file-level settings (from `BaseQuestFile.writeData`; the generator's `data` block is emitted verbatim, so put any of these there):

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `version` | int | — | Quest-file `VERSION`. Use `13` (current); a lower value may trigger migration on load. |
| `default_reward_team` | bool | false | Rewards go to the team (not the claiming player). |
| `default_consume_items` | bool | false | Default for item tasks' `consume_items` Tristate when omitted. |
| `default_autoclaim_rewards` | string | `"default"` | One of `"default"`, `"enabled"`, `"disabled"`, `"no_clear"`. |
| `default_quest_shape` | string | `"circle"` | Inherited by quests/chapters that omit `shape`. |
| `default_quest_disable_jei` | bool | false | Hide this pack from JEI/REI/EMI recipe viewers. |
| `emergency_items` | list of item objs | — | Optional; the "emergency items" button grants these. `emergency_items: [{ id:"minecraft:bread", count:1 }]`. |
| `emergency_items_cooldown` | int | 300 | Cooldown (seconds) between emergency-item claims. |
| `drop_loot_crates` | bool | false | Loot crates drop from mobs (uses `EntityWeight`). |
| `disable_gui` | bool | false | Hide the in-game quest book GUI. |
| `grid_scale` | double | 0.5 | Zoom/scale of the quest grid. |
| `pause_game` | bool | false | Pause the game while the quest GUI is open (singleplayer). |
| `lock_message` | string | `""` | Shown when a locked quest/chapter is clicked. |
| `progression_mode` | string | `"linear"` | `default` / `linear` / `flexible` — file-level progression gating. **Note: the loader defaults an absent value to `"linear"`.** |
| `detection_delay` | int | 20 | Ticks between task-progress detection passes. |
| `show_lock_icons` | bool | false | Draw lock icons on incomplete quests. |
| `drop_book_on_death` | bool | false | Drop the quest book item on death. |
| `hide_excluded_quests` | bool | false | Hide quests excluded via `Excludable`. |
| `fallback_locale` | string | `"en_us"` | Locale used when a key has no entry in the player's locale. |
| `verify_on_load` | bool | false | Validate the quest book on load. |

---

## 4. `chapter_groups.json5` (multi-tab packs only)

```json5
{
  chapter_groups: [
    {
      id: "A1B2C3D4E5F60001",
      // title/subtitle for this group come from lang: chapter_group.<id>.title
    },
  ],
}
```
The default group is implicit (never written here). A chapter opts into a non-default group via `group: "A1B2C3D4E5F60001"`; `group: ""` = default.

---

## 5. Chapter object (inside `chapters/<filename>.json5`)

Top-level of each chapter file is one object:

```json5
{
  id: "0123456789ABCDEF",
  group: "",                       // "" = default group
  order_index: 0,                   // display order of chapters within group
  filename: "getting_started",      // matches the file name (without .json5)
  default_quest_shape: "circle",     // required
  default_quest_size: 1.0,          // optional, only if != 1.0
  default_min_width: 0,             // optional, only if > 0
  default_hide_dependency_lines: false,
  progression_mode: "default",      // optional: "default" | "linear" | "flexible"
  always_invisible: false,
  autofocus_id: "",                  // hex id of a quest to focus on open
  // visibility flags (all optional, default false):
  hide_quest_details_until_startable: false,
  hide_quest_until_deps_visible: false,
  hide_quest_until_deps_complete: false,
  hide_text_until_complete: false,
  default_repeatable_quest: false,
  require_sequential_tasks: false,

  quests: [ /* quest objects */ ],
  quest_links: [ /* optional: { id, linked_quest, x, y, shape?, size? } — §18 */ ],
  images: [ /* optional chapter background images — §19 */ ],
}
```
**Note:** chapter `title`/`subtitle`(=description) are NOT inline — see §8 Localization.

---

## 6. Quest object (member of a chapter's `quests[]`)

```json5
{
  id: "1111111111111111",
  x: 0.0,
  y: 0.0,
  shape: "circle",                 // optional, overrides chapter default
  size: 1.0,                        // optional, only if != 0
  icon_scale: 1.0,                  // optional, only if != 1.0
  min_width: 0,                     // optional, only if > 0
  guide_page: "",                   // optional, a Patchouli guide page id
  dependencies: ["2222222222222222"], // hex ids of prerequisite quests
  dependency_requirement: "all",    // "all" (default) | "one"
  min_required_dependencies: 0,      // optional, only if > 0
  max_completable_dependents: 0,    // optional, gating
  optional: false,                  // quest is optional (side quest)
  invisible: false,                 // hidden until conditions
  invisible_until_tasks: 0,         // show after N tasks of dependents done
  repeat_cooldown: 0,               // optional, repeatable cooldown in ticks, only if > 0
  progression_mode: "default",      // optional
  ignore_reward_blocking: false,
  hide_lock_icon: false,
  // Tristate-style visibility flags (true/false/omit):
  hide_dependency_lines: false,
  hide_dependent_lines: false,
  hide_until_deps_visible: false,
  hide_until_deps_complete: false,
  hide_text_until_complete: false,
  hide_details_until_startable: false,
  require_sequential_tasks: false,

  tasks: [ /* task objects */ ],
  rewards: [ /* reward objects */ ],
}
```
`x`/`y` are doubles and **required**. Quest `title`/`subtitle`/`description` are NOT inline — see §8.

---

## 7. Task & Reward type reference

All tasks: `{ id, type, …type-specific… }`. All rewards: `{ id, type, …type-specific… }`. **No inline `title`** (use lang).

### 7a. Tasks

> **Item quantity is the sibling `count`, not the object count.** `ftbquests:item` tasks read the SIBLING `count` field and ignore the count inside `item` (always `1`). Write `item: "minecraft:apple", count: 3` — the generator lifts any count buried in the object to the sibling.
> **`ftbquests:xp` requires `points`.** `XPTask.readData` throws if `points` is absent (the quest book fails to load). The generator defaults `points: true`; set `points: false` to count XP levels instead of points.

| `type` | Key fields | Notes |
|--------|-----------|-------|
| `ftbquests:item` | `item: {id,count:1}`, `count` (qty, sibling, omit if 1), `consume_items`, `only_from_crafting`, `match_components` (`"fuzzy"`/`"strict"`), `task_screen_only` | Most common. `consume_items` / `only_from_crafting` are **Tristate**: `true`/`false`/omitted (= inherit chapter `default_consume_items`). `match_components`: `none`(omit)/`fuzzy`/`strict`. |
| `ftbquests:fluid` | `fluid` (FluidStack object — fluid *and* mB amount together) | No separate `amount` field. |
| `ftbquests:forge_energy` | `value` (long, FE), `max_input` (long, default 1000) | Forge builds only (not in `common`). |
| `ftbquests:xp` | `value` (long), `points` (bool, **required**) | `points:true` → XP points; `false` → XP levels. |
| `ftbquests:kill` | `entity` (entity id) or `entityTypeTag` (tag id), `value` (count), `custom_name`, `nbt_filter` | Kill N of an entity type/tag; optionally filter by custom name or NBT. |
| `ftbquests:advancement` | `advancement` (id), `criterion` (optional) | |
| `ftbquests:stat` | `stat` (stat id), `value` (long) | Vanilla statistics. |
| `ftbquests:location` | `dimension`, `x`, `y`, `z` (doubles), `ignore_dimension` (bool) | Visit coords; `ignore_dimension` lets the check pass in any dimension. |
| `ftbquests:dimension` | `dimension` (resource id) | Enter a dimension. |
| `ftbquests:biome` | `biome` (resource id) | Visit a biome. |
| `ftbquests:structure` | `structure` (structure id) | Find a structure. |
| `ftbquests:observation` | `timer` (ticks), `observation_type` (enum: `"BLOCK"`/`"ENTITY"`/…), `to_observe` (block/entity id) | Look at / hold crosshair on something for `timer` ticks. |
| `ftbquests:gamestage` | `stage` (string), `team_stage` (bool) | Requires GameStages mod. (Type id is `gamestage`, **not** `stage`.) |
| `ftbquests:checkmark` | *(none)* | Manual toggle quest. |
| `ftbquests:custom` | `title`/`icon` optional + custom data | KubeJS / scripted. |

Task-level (base `Task`): `optional_task` (bool — a single optional task within an otherwise required quest).

### 7b. Rewards

> **Item reward quantity is the sibling `count`.** `ItemReward.claim` reads the SIBLING `count` field (default 1) and ignores the count inside `item` (always `1`). Write `item: "minecraft:apple", count: 3`. (This mirrors item tasks — both use a sibling `count` with an object count of `1`.)
> **Command rewards run as the PLAYER by default** (not op). Set `permission_level` (1-4) to elevate. FTB Quests substitutes `{p}`/`{x}`/`{y}`/`{z}`/`{team}`/`{quest}`… in the command string; `@p`/`@a` selectors also work in selector-accepting commands (shipped packs use `command: "/say Hi, @p!"`).
> **`loot`/`random`/`choice`/`all_table` reference a table via `table_id`** — a decimal *long* (the numeric value of the table's id), not a hex string. See §17.

| `type` | Key fields | Notes |
|--------|-----------|-------|
| `ftbquests:item` | `item: {id,count:1}`, `count` (qty, sibling, omit if 1), `random_bonus`, `only_one`, `team`, `exclude_from_claim_all` | `random_bonus` adds 0..N extra; `only_one` skips granting if the player already has one. |
| `ftbquests:xp` | `xp` (long, points) | |
| `ftbquests:xp_levels` | `xp_levels` (int) | |
| `ftbquests:command` | `command` (string), `permission_level` (0-4), `silent` (bool), `feedback_message` (string) | Runs as the player unless `permission_level>0` elevates. Placeholders: `{p}` (name), `{x}`/`{y}`/`{z}` (coords), `{chapter}`, `{quest}`, `{team}`, `{team_id}`, `{long_team_id}`, `{member_count}`, `{online_member_count}`. `silent` suppresses output. |
| `ftbquests:loot` | `table_id` (long) | Loot crate from a table (includes an "empty" chance). §17. |
| `ftbquests:random` | `table_id` (long) | One random reward from a table. §17. |
| `ftbquests:choice` | `table_id` (long) | Player picks one from a table. §17. |
| `ftbquests:all_table` | `table_id` (long) | Give every reward in a table. §17. |
| `ftbquests:advancement` | `advancement` (id), `criterion` (optional) | Grant an advancement. |
| `ftbquests:toast` | `description` (string) | Show a toast/notification. |
| `ftbquests:gamestage` | `stage` (string), `remove` (bool) | Grant a stage (`remove: true` revokes it instead). |
| `ftbquests:custom` | custom data | KubeJS / scripted. |
| `ftbquests:currency` | — | Disabled by default; needs an economy integration. |

Reward-level (base `Reward`): `auto` (autoclaim: `default`/`enabled`/`disabled`/`no_clear`), `exclude_from_claim_all`, `ignore_reward_blocking`, `disable_reward_screen_blur`.

In the **spec**, reference a reward table by name (`table: "common_loot"`) or by raw 16-hex id (`table: "0123…"`) for an external table; the generator resolves it to the decimal `table_id` long the on-disk format expects.

### Quest shapes
`circle` `square` `diamond` `pentagon` `hexagon` `octagon` `heart` `gear` `rsquare` `rdiamond` `puzzle` `shield` (default `circle`). Visually distinguish: main path = `circle`, optional/side = `square`, boss/key = `hexagon`/`diamond`.

---

## 8. Localization (modern: text lives in lang files)

Modern FTB Quests stores all quest/chapter text in `lang/<locale>/`, keyed by object — inline `title`/`description` fields are **ignored**. Key format:

```
<objectType>.<objectId16hex>.<subkey>
```
- `objectType`: `quest` | `chapter` | `task` | `reward` | `chapter_group` | `quest_link` | `reward_table`.
- `subkey`: `title` (string) · `quest_subtitle` (string) · `quest_desc` (**list**) · `chapter_subtitle` (**list** = the chapter's description).
- Keys contain dots → **always quote them**.

Fallback locale is `en_us` (always provide an `en_us` set; other locales are overrides).

`lang/en_us/quests.json5`:
```json5
{
  // Chapter text
  "chapter.0123456789ABCDEF.title": "Getting Started",
  "chapter.0123456789ABCDEF.chapter_subtitle": ["Welcome to the pack!"],

  // Quest text
  "quest.1111111111111111.title": "Punching Wood",
  "quest.1111111111111111.quest_subtitle": "Gather wood to begin",
  "quest.1111111111111111.quest_desc": ["Punch a tree and collect 4 oak logs.", "Logs are the start of everything."],

  // Optional: custom task/reward titles (otherwise the type auto-generates a label)
  "task.2222222222222222.title": "Collect 4 Oak Logs",
}
```
Add `lang/zh_cn/quests.json5` with the same keys for Chinese, etc. `loadAndCombine` walks the whole locale folder, so a single file per locale works (or split by chapter — your choice).

> **Legacy / SNBT packs come in two flavors (§12):** the 1.20.1 classic build stores text INLINE as `title: "..."` and `description: ["..."]` inside the quest object (no `lang/`). The 1.21.1 build (FTB Quests 2101.1.21) also serializes `.snbt` but uses **this same lang-file model** — except the lang file is one flat `lang/<locale>.snbt` per locale (not `lang/<locale>/quests.json5`), and quest objects carry no inline text. If a generated SNBT pack shows blank titles in-game, either you are on the inline variant but put text in lang (→ move text back onto the quest object, drop `lang/`), or you are on the lang-file variant but left text inline (→ move text into `lang/<locale>.snbt`, key it `quest.<HEX>.title`). Detect which from an existing pack's files before generating.

---

## 9. ID generation

Every quest/task/reward/chapter needs a stable 16-char uppercase hex `id` (e.g. `1A2B3C4D5E6F7890`). For deterministic, collision-free generation, hash a stable path, take 16 hex chars of the digest, then **mask the top bit** and uppercase:

```
raw = md5("<packslug>/<chapter>/<object>/<name>").hex()[0:16]
id  = "%016X" % (int(raw, 16) & 0x7FFFFFFFFFFFFFFF)
```

**Why the mask?** FTB Quests stores ids as signed 64-bit `long`s and generates its own with `Math.abs(random.nextLong())` — always in `[0, Long.MAX_VALUE]` (top hex digit 0-7). On load it parses a hex-string id with `Long.parseLong(hex, 16)`, which **throws** for any magnitude above `Long.MAX_VALUE` (top digit 8-F); the loader swallows that exception and hands the object a *brand-new random id*, silently breaking every `dependencies` / `linked_quest` / image `dependency` reference to it (those resolve to id `0` and get dropped). Clearing the top bit keeps every generated id within `Long.MAX_VALUE` so it round-trips. This also keeps `table_id` (the decimal long a `random`/`loot`/`choice`/`all_table` reward emits — §17) inside Java `long` range.

Rules: ids must be unique within the whole quest book; dependency ids in `dependencies: [...]` must exactly match the target quest's `id`. Distinct strings hash to distinct ids with negligible probability; keep names stable across regenerations so ids stay stable. Reward-table entry ids use `md5("<pack>/<table>/table_reward/<entry>/<entry>")`, quest links `md5("<pack>/<chapter>/quest_link/<name>/<name>")`, chapter images `md5("<pack>/<chapter>/image/<name>/<name>")` — all masked the same way.

---

## 10. Common patterns

- **Linear main path:** each quest depends on the previous; `shape: "circle"`; `x` increments by ~1.0, `y` constant.
- **Branching:** a quest with 2+ dependents (children on different `y`); set `dependency_requirement: "all"` (default) so the parent must complete.
- **Optional side quests:** `optional: true`, `shape: "square"`, not on the dependency path of required quests.
- **Gating / choose-one:** set `dependency_requirement: "one"` so any one dependency unlocks; or `min_required_dependencies: N` to need N of M.
- **Expert mode:** gate entire chapters behind a `checkmark`/`gamestage` task; mark quests `invisible: true` until `invisible_until_tasks`.
- **Repeatable:** set the chapter's `default_repeatable_quest: true`, or per-quest `repeat_cooldown: <ticks>`.
- **Sequential tasks:** chapter `require_sequential_tasks: true` (or per-quest) so tasks must be done in order.
- **Multiblock / machine gating:** use `ftbquests:item` with `only_from_crafting: true` for crafted-only checks, or `ftbquests:forge_energy`/`ftbquests:fluid` for throughput.
- **Hide dependency lines:** `hide_dependency_lines: true` on a quest (or chapter `default_hide_dependency_lines: true`) to declutter.

---

## 11. Full worked example (modern JSON5)

**`config/ftbquests/quests/data.json5`**
```json5
{
  version: 13,
  default_reward_team: false,
  default_consume_items: true,
  default_autoclaim_rewards: "default",
  default_quest_shape: "circle",
  default_quest_disable_jei: false,
  emergency_items_cooldown: 300,
}
```

**`config/ftbquests/quests/chapters/getting_started.json5`**
```json5
{
  id: "0123456789ABCDEF",
  group: "",
  order_index: 0,
  filename: "getting_started",
  default_quest_shape: "circle",
  quests: [
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
      rewards: [
        {
          id: "3333333333333333",
          type: "ftbquests:item",
          item: { id: "minecraft:apple", count: 1 },
          count: 2,
        },
      ],
    },
    {
      id: "4444444444444444",
      x: 1.5,
      y: 0.0,
      shape: "circle",
      dependencies: ["1111111111111111"],
      tasks: [
        {
          id: "5555555555555555",
          type: "ftbquests:item",
          item: { id: "minecraft:crafting_table", count: 1 },
          consume_items: true,
        },
      ],
      rewards: [
        {
          id: "6666666666666666",
          type: "ftbquests:item",
          item: { id: "minecraft:wooden_pickaxe", count: 1 },
        },
        {
          id: "7777777777777777",
          type: "ftbquests:xp_levels",
          xp_levels: 5,
        },
      ],
    },
  ],
}
```

**`config/ftbquests/quests/lang/en_us/quests.json5`**
```json5
{
  "chapter.0123456789ABCDEF.title": "Getting Started",
  "chapter.0123456789ABCDEF.chapter_subtitle": ["The first steps of your adventure."],
  "quest.1111111111111111.title": "Punching Wood",
  "quest.1111111111111111.quest_subtitle": "Gather wood to begin",
  "quest.1111111111111111.quest_desc": ["Punch a tree and collect 4 oak logs."],
  "quest.4444444444444444.title": "Tools of the Trade",
  "quest.4444444444444444.quest_desc": ["Craft a crafting table.", "You'll get a starter pickaxe and some XP!"],
}
```

**`config/ftbquests/quests/lang/zh_cn/quests.json5`**
```json5
{
  "chapter.0123456789ABCDEF.title": "新手入门",
  "chapter.0123456789ABCDEF.chapter_subtitle": ["冒险的第一步。"],
  "quest.1111111111111111.title": "砍树",
  "quest.1111111111111111.quest_subtitle": "收集木头开始旅程",
  "quest.1111111111111111.quest_desc": ["撸树并收集 4 个原木。"],
  "quest.4444444444444444.title": "必备工具",
  "quest.4444444444444444.quest_desc": ["合成一个工作台。", "你会获得一把初始镐和一些经验！"],
}
```

---

## 12. SNBT format — 1.20.1 and 1.21.1

FTB Quests for MC 1.20.1 (`FTBTeam/FTB-Quests` branch `1.20.1/main`, `VERSION = 13`) serializes via `dev.ftb.mods.ftblibrary.snbt.SNBT`, **not** JSON5. Files are `data.snbt`, `chapters/*.snbt`, `reward_tables/*.snbt`, `chapter_groups.snbt` — text is **inline** on the quest/chapter object in the classic 1.20.1 build. Verified against the Java source 2026-06-25 (`SNBT`, `SNBTBuilder`, `SNBTUtils`, `SNBTParser`, `BaseQuestFile`, `Quest`, `QuestObjectBase`, `ItemTask`, `ItemReward`, `XPTask`, `RewardTable`, `QuestLink`, `ChapterImage`).

To target 1.20.1, set `format: "snbt"` in `quests.spec.json5` (§13). The generator emits `.snbt` via `ftbq/snbt.py`; the validator parses and checks it; the deployer merges/backs it up. Default for a brand-new pack is `json5` (current `main`).

> **Version split is TWO axes, not one** (revised 2026-06-29 after auditing shipped packs). Serialization and localization vary independently:
>
> | Serialization | Localization | Where |
> |---|---|---|
> | SNBT (`.snbt`, no commas, TAB, `0.0d`/`1L` suffixes) | inline `title:`/`description:` | 1.20.1 classic (Create: Delight Remake, FTB Quests 2001.4.17) |
> | SNBT | **lang files** `lang/<locale>.snbt` keyed `quest.<HEX>.title` — quest objects carry NO inline text | **1.21.1** (Mechanomania, FTB Quests 2101.1.21) |
> | JSON5 (`.json5`, commas, bare numbers) | lang files `lang/<locale>/quests.json5` | current `main` (MC `26.1.x`) |
>
> **"1.21+ = JSON5" is false** — FTB Quests 2101.1.21 on MC 1.21.1 still serializes SNBT (with lang files). The JSON5 switch landed later on `main`. Detect from the files (§ below), not the MC version. The skill supports all three; `spec.format` selects `"json5"` or `"snbt"`, and the presence/absence of inline text vs a `lang/` dir decides the localization model.

### 12a. SNBT syntax (vs JSON5)

| Rule | SNBT (1.20.1 & 1.21.1) | JSON5 (current `main`) |
|------|---------------|---------------|
| Comments | `#` or `//` at line start | `//` / `/* */` |
| Separator | **no commas** (newlines/whitespace) | commas (trailing OK) |
| Indent | **TAB** | 2 spaces |
| Numbers | suffixed: `1L` (long), `1.0d` (double), `1.0f` (float), `1b` (byte), `1s` (short), `1` (int) | bare (`1`, `1.0`) |
| Booleans | `true` / `false` | `true` / `false` |
| Strings | double-quoted, 6 escapes (`\"` `\\` `\t` `\b` `\n` `\r` `\f`) | double-quoted |
| Keys | unquoted if all chars in `[A-Za-z0-9._-+∞]`, else quoted | unquoted if identifier |
| Items | `{ id:"…", count:N }` (count is an **int**, lowercase) | `{ id:"…", count:N }` |
| Empty | `{ }` / `[ ]`; a single-element list is inline `[v]` | `{}` / `[]` |

### 12b. Field → NBT type (the suffixes that matter)

A field's NBT type is fixed by each `writeData`; the generator emits the right suffix per field (resolved from the value's dotted path in `ftbq/snbt.py`). A wrong suffix silently loads as the wrong tag type.

| Field | Type | Suffix | Source |
|-------|------|--------|--------|
| `id` (any object) | string | quoted | `putString("id", getCodeString())` |
| `ItemTask.count` | long | `N L` | `putLong` (only if >1) |
| `XPTask.value` (and `EnergyTask`/`FluidTask` value) | long | `N L` | `putLong` |
| `ItemReward.count` | int | bare | `putInt` (only if >1) |
| `random_bonus`, `min_required_dependencies`, `loot_size`, `order`, `color`, `alpha` | int | bare | `putInt` |
| `x`, `y`, `size`, `icon_scale`, `width`, `height`, `rotation`, `default_quest_size` | double | `N.Nd` | `putDouble` |
| `empty_weight`, `weight` | float | `N.Nf` | `putFloat` |
| booleans (`optional`, `points`, `hide_tooltip`, `dev`, `corner`, …) | boolean | `true`/`false` | `putBoolean` |
| `dependencies` | string list | `["hex1", "hex2"]` | `ListTag` of `getCodeString()` |

### 12c. IDs and the top-bit mask

`id` is a **hex string** (`id: "1A2B3C4D5E6F7A8B"`, 16 uppercase hex). On load, `readID` → `parseCodeString` → `Long.parseLong(hex, 16)` throws for a leading digit 8-F, so the **top-bit mask in `ftbq.ids` (§9) is still required for 1.20.1**. Dependencies reference ids by the same hex string.

### 12d. Text model — inline OR lang files (two SNBT variants)

SNBT packs come in **two localization flavors** (see the version-split table in §12):

1. **Inline (1.20.1 classic).** `title`, `subtitle`, and `description` live **inline** on the quest/chapter object. Quest `subtitle` is a string; chapter `subtitle` is a **list**; `description` is always a list. No `lang/` directory.
2. **Lang files (1.21.1, FTB Quests 2101.1.21).** Quest objects carry **no** `title`/`subtitle`/`description` at all. Text lives in **one flat `lang/<locale>.snbt` file per locale** (e.g. `lang/en_us.snbt`, `lang/zh_cn.snbt`), keyed exactly like the JSON5 lang model: `quest.<HEXID>.title`, `quest.<HEXID>.quest_subtitle`, `quest.<HEXID>.quest_desc` (list), `chapter.<HEXID>.title`, `chapter.<HEXID>.chapter_subtitle`, `chapter_group.<HEXID>.title`. The lang file is itself SNBT (one `key: "value"` per line, no commas). This is the same localization model as JSON5, just serialized as SNBT.

**Type ids are SHORT in SNBT** — both flavors. Real packs write `type: "item"`, `type: "fluid"`, `type: "xp"`, `type: "kill"`, `type: "advancement"`, `type: "stat"`, `type: "dimension"`, `type: "biome"`, `type: "structure"`, `type: "observation"`, `type: "checkmark"`, `type: "custom"`, `type: "command"`, `type: "loot"`, `type: "random"`, `type: "choice"`, `type: "all_table"`, `type: "xp_levels"` — **no `ftbquests:` prefix**. (The prefixed `ftbquests:item` form is the JSON5 convention.) The §7 tables show the prefixed form because that is the canonical registry id; when hand-writing or emitting SNBT, drop the prefix.

**Bare-string items are valid in SNBT.** Both `item: { id: "minecraft:oak_log", count: 1 }` (object) and `item: "minecraft:oak_log"` (bare string) load; shipped packs use bare strings freely in rewards and reward-table entries (`{ item: "ae2:logic_processor" }`). (In JSON5 a bare string is dropped — object form only.) Item-object shape is MC-version-dependent: **1.20.1** uses capital `Count` + `tag: { ... }` (NBT); **1.21.1** uses lowercase `count` + `components: { ... }` (data components).

```snbt
{
  id: "6A42C15CE3485849"
  x: 0.0d
  y: 0.0d
  title: "Punch Wood"
  subtitle: "Hit a tree with your fist"
  description: [
    "Break wood by holding"
    "left mouse."
  ]
  tasks: [ { id: "T1", type: "item",
    item: { id: "minecraft:oak_log", count: 1 }, count: 4L } ]
}
```

### 12e. Worked example (1.20.1 SNBT)

`data.snbt`:
```snbt
{
  version: 13
  default_reward_team: false
  default_consume_items: false
  default_autoclaim_rewards: "default"
  default_quest_shape: "circle"
  default_quest_disable_jei: false
  emergency_items_cooldown: 300
}
```

`chapters/intro.snbt` (item task `count: 4L`, xp `value: 30L`, random reward `table_id` = the table's decimal long, quest link, image):
```snbt
{
  id: "422BD87811D48987"
  filename: "intro"
  group: ""
  order_index: 0
  default_quest_shape: "circle"
  title: "Getting Started"
  subtitle: ["A short intro"]
  quests: [
    {
      id: "5722EB1632505E60"
      x: 0.0d
      y: 0.0d
      shape: "circle"
      dependencies: [ ]
      title: "Punch Wood"
      tasks: [
        {
          id: "686B342EBB660248"
          type: "item"
          item: { id: "minecraft:oak_log", count: 1 }
          count: 4L
        }
      ]
      rewards: [
        { id: "1E8B030698628385", type: "random",
          table_id: 7307199375195515355 }
      ]
    }
  ]
  quest_links: [
    { id: "2A2A2A2A2A2A2A2A", linked_quest: "5722EB1632505E60",
      x: 5.0d, y: 0.0d }
  ]
  images: [
    { id: "3B3B3B3B3B3B3B3B",
      image: "minecraft:textures/block/oak_log.png",
      x: 0.0d, y: 0.0d, width: 1.0d, height: 1.0d, rotation: 0.0d }
  ]
}
```

`reward_tables/starter_loot.snbt` (entry `weight: 2.0f`, table `empty_weight: 1.0f`):
```snbt
{
  id: "656E54BA88B859DB"
  rewards: [
    { id: "1F9057DFD12B4C09",
      item: { id: "minecraft:stick", count: 1 }, weight: 2.0f }
  ]
  empty_weight: 1.0f
  loot_size: 1
  hide_tooltip: false
  use_title: false
}
```

When porting 1.20.1 (SNBT inline) → 1.21.1 (SNBT + lang) → current `main` (JSON5 + lang): the first hop moves inline text into `lang/<locale>.snbt` (`quest.<HEX>.title`) and drops the inline fields but **keeps** `.snbt` + suffixes + short type names; the second hop then converts `.snbt`→`.json5`, `lang/<locale>.snbt`→`lang/<locale>/quests.json5`, drops all type suffixes, and switches type ids to the `ftbquests:`-prefixed form. The skill's `format` field selects serialization; the presence of inline text vs a `lang/` dir selects the localization model.

---

## 13. Spec format (`quests.spec.json5`)

The LLM-authored source of truth. One file describes the entire quest book at a high level; `scripts/generate_quests.py` reads it and emits the on-disk pack under a clean `<output_dir>/quests/` subfolder (`data.json5`, `chapter_groups.json5`, every `chapters/*.json5`, every `lang/<locale>/quests.json5`, plus `.ftbq-cache/manifest.json5`). `quests.spec.json5` stays at `<output_dir>` root and is never deployed. The spec is what you EDIT; the generated files are what the game LOADS. See §16 for deploying that `quests/` folder into a live pack. With `format: "snbt"` (§12) the output is `data.snbt` / `chapters/*.snbt` / `reward_tables/*.snbt` / `chapter_groups.snbt`; text is **inline** for the 1.20.1 classic variant and lives in `lang/<locale>.snbt` for the 1.21.1 variant (the generator picks the model from whether the spec carries inline text vs `locales` blocks).

Design intent: keep the LLM-facing surface small and intent-shaped (names, dependencies, text), and let the generator handle hex IDs, lang-key rewriting, layout math, and JSON5 serialization. Item conveniences (bare strings, sibling `count`) exist so prompts read naturally.

### 13a. Top-level fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `pack` | string | yes | — | Pack slug. Feeds md5 ID generation (`md5("<pack>/<chapter>/<object>/<name>")`). **Changing `pack` regenerates every ID** — treat it as immutable once players are in. |
| `format` | string | no | `"json5"` | `"json5"` (current `main`) or `"snbt"` (1.20.1 inline **or** 1.21.1 + lang — see §12). Selects the on-disk serialization: `json5` emits `.json5` + `lang/<locale>/quests.json5`; `snbt` emits `.snbt`. **Generator limitation:** the `snbt` emitter currently produces the 1.20.1 **inline-text** variant only (no `lang/`); it does not yet emit the 1.21.1 SNBT+`lang/<locale>.snbt` variant — for an existing 1.21.1-style pack, use `--adopt` / `--mode preserve` so its lang files are not clobbered. The manifest stays `.json5` either way (skill-internal). |
| `default_locale` | string | no | `"en_us"` | Primary locale; lang placeholders without an override resolve here. |
| `locales` | list of strings | no | `[default_locale]` | All locales the generator should emit `lang/<locale>/quests.json5` for. The default locale is added implicitly if absent. |
| `data` | object | no | `{}` | Emitted as `data.json5` verbatim. Common members: `version`, `default_reward_team`, `default_consume_items`, `default_quest_disable_jei`, `default_autoclaim_rewards`, `emergency_items_cooldown`. See §3. |
| `chapter_groups` | list of `{name, order_index}` | no | `[]` | If non-empty, the generator emits `chapter_groups.json5` and resolves each chapter's `group` field to the matching group's hex ID. If empty, all chapters live in the implicit default group. |
| `chapters` | list of chapter objects | yes | — | The actual quest book. Order in the list is irrelevant; chapter `order_index` controls display order. |
| `reward_tables` | list of reward-table objects | no | `[]` | Weighted reward pools emitted as `reward_tables/<name>.json5` (§17). `loot`/`random`/`choice`/`all_table` rewards reference them by name via `table`. |

### 13b. Chapter fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | yes | — | Unique within the spec. Feeds md5 (`md5("<pack>/<name>")`) and becomes the chapter file's stem (`chapters/<name>.json5`). Also the prefix for `@<chapter>/...` lang placeholders. |
| `group` | string | no | `""` | References a `chapter_groups[].name`. `""` = implicit default group. |
| `order_index` | int | no | `0` | Display order within the group. |
| `default_quest_shape` | string | no | `"circle"` | Inherited by quests that omit `shape`. |
| `layout` | `{mode: "auto"\|"manual"}` | no | `{mode: "auto"}` | `auto`: x/y are computed from the dependency DAG — `x = depth * 1.5`, siblings are spread on `y` around `0` (e.g. `[-1.5, 0, 1.5]` for three siblings). `manual`: every quest in the chapter must set explicit `x` and `y`; the generator errors if any are missing. |
| `quests` | list of quest objects | yes | — | Quests in this chapter. |
| `quest_links` | list of `{name, linked_quest, x?, y?, shape?, size?}` | no | `[]` | Mirrors of quests (usually from another chapter) placed in this chapter. `linked_quest` is a `name`/`<chapter>/<quest>` ref or raw 16-hex (§18). |
| `images` | list of chapter-image objects | no | `[]` | Background images (§19). |

Any chapter field not listed above is passed through verbatim to the emitted chapter object — useful for `progression_mode`, `hide_quest_until_deps_complete`, `always_invisible`, `autofocus_id`, `default_quest_size`, etc. (see §5 for the full FTB Quests chapter surface). `name` and `layout` are spec-only directives and are NOT emitted.

### 13c. Quest fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | yes | — | Unique within the chapter. Feeds md5 (`md5("<pack>/<chapter>/<name>")`). Also the suffix for `@<chapter>/<name>.<subkey>` lang placeholders. |
| `shape` | string | no | chapter's `default_quest_shape` | See §7 for valid shapes. |
| `optional` | bool | no | `false` | Side-quest flag. |
| `depends_on` | list of strings | no | `[]` | Each entry is either a sibling quest's `name` (same chapter) or `<chapter>/<quest>` for cross-chapter deps. The generator resolves these to hex IDs and writes them to the emitted quest's `dependencies` array. |
| `dependency_requirement` | `"all"` \| `"one"` | no | `"all"` | Passes through to the emitted quest. |
| `x`, `y` | float | only when `layout.mode == "manual"` | — | Manual position. Ignored under `auto` (the generator computes them). |
| `tasks` | list of task objects | no | `[]` | See 13d. |
| `rewards` | list of reward objects | no | `[]` | See 13d. |

Any quest field not listed above is passed through verbatim — `repeat_cooldown`, `invisible`, `min_required_dependencies`, etc.

### 13d. Task and reward fields

Tasks and rewards share the same shape in the spec.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | yes | — | Unique within the parent quest. Feeds md5 (`md5("<pack>/<chapter>/<quest>/<name>")`). |
| `type` | string | yes | — | An FTB Quests type id, e.g. `"ftbquests:item"`, `"ftbquests:checkmark"`, `"ftbquests:xp_levels"`. See §7. |
| `item` | string OR object | depends on type | — | **Convenience:** a bare string `"minecraft:oak_log"` is normalized by the generator to `{ id: "minecraft:oak_log", count: 1 }`. Use the bare form by default; reach for the object form only when you need NBT/component data. |
| `count` | int | no | — | For item TASKS **and REWARDS**, `count` is a SIBLING field representing the quantity (the inner item-object `count` is always `1` — FTB Quests reads only the sibling, `ItemTask`/`ItemReward`). Write `item: "minecraft:apple", count: 3`; if the spec buries the count in the object, the generator lifts it to the sibling. |

All other fields (`consume_items`, `only_from_crafting`, `match_components`, `team`, `xp`, `xp_levels`, `command`, `stage`, etc.) are passed through unchanged.

### 13e. Lang placeholder convention

Inside the spec you reference text via placeholders that the generator rewrites to canonical lang keys (§8). Placeholders may appear anywhere a string is expected on chapters/quests (`title`, `subtitle`, `description`):

| Placeholder shape | Rewritten to |
|-------------------|--------------|
| `"@<chapter_name>.<subkey>"` | `"chapter.<HEX>.<subkey>"` |
| `"@<chapter_name>/<quest_name>.<subkey>"` | `"quest.<HEX>.<subkey>"` |

Subkeys:
- `title` — string, chapter or quest title.
- `quest_subtitle` — string, single-line quest blurb.
- `quest_desc` — list of strings, each entry is one line of the quest's body text.
- `chapter_subtitle` — list of strings, the chapter's description block.

The generator reads the placeholder, computes the target object's hex ID, and writes both the rewritten reference (where applicable) and the lang-file entries under `lang/<locale>/quests.json5`. Localized strings are sourced from a parallel `locales: { en_us: { ... }, zh_cn: { ... } }` block on the spec object whose keys mirror the placeholder paths.

---

## 14. Manifest format (`.ftbq-cache/manifest.json5`)

The manifest is the generator's memory of what it owns. It lives in `.ftbq-cache/` inside the quests root (i.e. `<output_dir>/quests/.ftbq-cache/manifest.json5` — FTB Quests' chapter scanner skips dot-prefixed directories, so this never leaks into the loaded book) and tracks every skill-owned object — chapter, quest, task, reward — so subsequent runs of `generate_quests.py` can distinguish three states for each object on disk:

1. **Pristine** — content_hash matches the manifest entry → safe to overwrite.
2. **User-edited** — object exists with the manifest's ID but content_hash differs → preserve, warn (`E_MANIFEST_HASH_MISMATCH`), prompt under `--mode ask`.
3. **User-added** — object exists on disk with no manifest entry → leave alone; generator never touches non-owned objects.

A missing manifest forces a cold regenerate; a corrupt manifest is a hard error.

### 14a. Top-level fields

| Field | Type | Description |
|-------|------|-------------|
| `schema` | int | Manifest schema version. Currently `1`. Bump on breaking layout changes. |
| `pack` | string | Must match the spec's `pack`. A mismatch aborts generation — switching pack slugs is a destructive operation that invalidates every ID. |
| `generated_at` | string | ISO-8601 UTC timestamp of the last generation run. |
| `generator_version` | string | Version string of `generate_quests.py` that wrote this manifest. |
| `spec_hash` | string | `"sha256:<hex>"` fingerprint of `quests.spec.json5` at generation time. Used by `validate_quests.py` to flag "spec changed since last generate". |
| `entries` | list of entry objects | One per skill-owned object. See 14b. |

### 14b. Entry fields

Every entry has a `kind` ∈ `chapter` \| `quest` \| `task` \| `reward`. Fields present depend on `kind`.

| Field | Kinds | Description |
|-------|-------|-------------|
| `kind` | all | Object kind. |
| `id` | all | The 16-char uppercase hex ID. |
| `name` | all | Slug from the spec — the `name` field that fed the md5. |
| `chapter` | quest, task, reward | Parent chapter's spec `name`. |
| `quest` | task, reward | Parent quest's spec `name`. |
| `file` | chapter, quest | Chapter file path (relative to the quests root, e.g. `chapters/getting_started.json5`). For quests this is the file the quest LIVES in; for chapters it's the chapter's own file. |
| `content_hash` | all | `"sha256:<hex>"` of the object's canonical-JSON serialization with every `id` field stripped recursively. See 14c. |
| `x`, `y` | quest | Last-emitted position. Stored separately from `content_hash` so manual nudges in the JSON5 don't read as content drift; the generator detects position-only changes and either preserves them (auto layout) or reconciles them (manual layout). |
| `aliases` | quest | List of past `name`s that resolved to the same hex ID after a rename. Lets `generate --mode ask` say "`old_name` was renamed to `new_name`" and preserve player progress (since the hex ID hasn't changed — only the slug used for diffing). |

### 14c. Content-hash recipe

The hash MUST be computed identically in `generate_quests.py` and `validate_quests.py`, otherwise every validation run flags drift. The recipe:

1. Start with the object's plain-Python form (the dict you'd pass to `json.dumps`).
2. For quest entries only, drop `x` and `y` (position is tracked separately).
3. Recursively drop every `id` field — including nested IDs on tasks/rewards inside a quest, on quests inside a chapter, etc. This makes the hash invariant under ID regeneration.
4. JSON-serialize with `json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)`.
5. Take the sha256 of the UTF-8 bytes, hex-encode, prefix with `"sha256:"`.

Reference implementation:

```python
import hashlib, json

def content_hash(obj: dict, *, kind: str) -> str:
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if k != "id"}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    canonical = strip(obj)
    if kind == "quest":
        canonical.pop("x", None)
        canonical.pop("y", None)
    payload = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
```

Any change to this function is a breaking manifest-schema change — bump `schema` and migrate.

---

## 15. Validator diagnostics catalog

`scripts/validate_quests.py` walks the on-disk pack and the manifest and emits one diagnostic per finding. Diagnostics use a stable code so CI rules can pin specific severities. It auto-detects the format (SNBT if `data.snbt` or any `.snbt` chapter/table exists, else JSON5) and parses accordingly — `ftbq.json5` for `.json5`, `ftbq.snbt` for `.snbt`. The structural checks (ids, dependencies, reward tables, manifest, coord dups, bare-string items) run identically for both; the two JSON5-only checks (`E_TYPE_SUFFIX`, `E_INLINE_TEXT_MODERN`) are skipped for SNBT (suffixes are legal and inline text is expected there — §12). Output format:

```
chapters/start.json5:42:7: error: dependency '0123456789ABCDEF' not found Did you mean 'ABCDEF0123456789'? [E_DEP_MISSING]
```

Columns: `<file>:<line>:<col>: <severity>: <message> [<CODE>]`. Line/col are omitted (`<file>: ...`) when the finding has no precise position (e.g. `E_DIR_MISSING`).

| Code | Severity | When triggered | Hint provided | Autofixable |
|------|----------|----------------|---------------|-------------|
| `E_PARSE` | error | A `.json5` (or `.snbt`) file fails to parse. | Line/col from the JSON5 lexer (JSON5); `1:1` for SNBT (parser doesn't track position). | no |
| `E_FILE_MISSING` | error | `data.json5` (or `data.snbt` for 1.20.1) is absent. | — | no |
| `E_DIR_MISSING` | error | `chapters/` directory is absent. | — | no |
| `E_FILENAME_MISMATCH` | error | Chapter's `filename` field differs from the file's stem. | "rename file or change field" | yes — rewrites the field to match the stem (file rename is destructive, so the autofix prefers the field). |
| `E_FILE_FIELD_MISSING` | error | Chapter is missing `filename` or `default_quest_shape`. | — | no |
| `E_ID_MISSING` | error | A chapter/quest/task/reward/reward-table (or table entry) has no `id`. | — | no |
| `E_ID_FORMAT` | error | An `id` is not a 16-char uppercase hex string. | — | no |
| `E_ID_DUP` | error | The same ID appears in two places (location of the duplicate is included in the message). | — | no |
| `E_DEP_MISSING` | error | A dependency ID is not found anywhere in the book. | `Did you mean 'XXX'?` from `difflib.get_close_matches(target, all_ids, n=1, cutoff=0.7)`. | no |
| `E_DEP_CYCLE` | error | The dependency graph contains a cycle. | The cycle path is printed (`A -> B -> C -> A`). | no |
| `E_TABLE_MISSING` | warning | A `loot`/`random`/`choice`/`all_table` reward's `table_id` does not match any reward table in the book. | `may reference an external table` | no |
| `E_ITEM_BARE_STRING` | error | A task/reward has `item: "minecraft:foo"` instead of an object — modern format requires `{id, count}`. | `replace with { id: "...", count: 1 }` | yes |
| `E_TYPE_SUFFIX` | error | A number carries a `d`/`b`/`L` suffix (SNBT leaked into JSON5). **JSON5-only** — not raised for `format: "snbt"` (suffixes are legal there). | `remove the trailing 'X'` | yes |
| `E_INLINE_TEXT_MODERN` | warning | A quest has inline `title`/`description`/`subtitle` — the modern JSON5 format ignores these. **JSON5-only** — not raised for `format: "snbt"` (inline text is required there). | `move text to lang/<locale>/quests.json5` | no |
| `E_LANG_MISSING_TITLE` | warning | A chapter or quest has no `*.title` lang entry in the primary locale. NOT raised for tasks/rewards (they don't render titles unless customized). | — | no |
| `E_LANG_ORPHAN` | warning | A lang key references an ID that doesn't exist in the book. | — | no |
| `E_COORD_DUP` | warning | Two quests share the same `(x, y)` in the same chapter. | — | no |
| `E_MANIFEST_HASH_MISMATCH` | warning | A skill-owned object's on-disk `content_hash` differs from the manifest entry — represents a user edit since last generation. | — | no |
| `E_MANIFEST_DANGLING` | warning | A manifest entry refers to an object that no longer exists on disk. | — | no |
| `E_MANIFEST_DUP_ID` | error | The same ID appears in two manifest entries. | — | no |

Severity policy: `error` blocks generation and exits non-zero; `warning` reports but allows the run to proceed. `--strict` promotes warnings to errors. Autofixable diagnostics are applied when the validator is invoked as `validate_quests.py --fix`; non-autofixable ones always require manual intervention.

---

## 16. Deploy & output layout

### 16a. Output layout

`generate_quests.py <output_dir>` writes a clean, copy-ready tree:

```
<output_dir>/
├── quests.spec.json5                 ← LLM source (NOT deployed)
└── quests/                           ← copy this into the pack
    ├── data.json5
    ├── chapter_groups.json5          (only if spec.chapter_groups non-empty)
    ├── chapters/<name>.json5         (one per chapter)
    ├── lang/<locale>/quests.json5    (one per locale; @placeholders rewritten in place)
    └── .ftbq-cache/manifest.json5    (skill memory; scanner-safe)
```

For a brand-new pack, copy `quests/` whole into `<packroot>/config/ftbquests/quests/`. For an existing pack, use `--deploy` (§16b) — a blind copy would clobber the pack's `data.json5`, `chapter_groups.json5`, other-quest lang keys, and any same-named chapter. File names never change during deploy, so a replaced file is trivial to find next to its backup.

With `format: "snbt"` (§12) the tree is `data.snbt` / `chapter_groups.snbt` / `chapters/<name>.snbt` / `reward_tables/<name>.snbt` / `.ftbq-cache/manifest.json5`. The generator emits the 1.20.1 **inline-text** variant, so there is no `lang/` in the output; a hand-authored 1.21.1-style pack additionally carries `lang/<locale>.snbt` (the generator does not yet emit that variant — see §13a limitation). The deployer (`ftbq/deploy.py`) classifies, parses, merges, and backs up `.snbt` files by the same logic as `.json5` (dispatch is by extension); the skill-internal `manifest.json5` and `BACKUP_INDEX.json5` stay JSON5 in either format.

### 16b. `--deploy` — safe merge into a live pack

```
python scripts/generate_quests.py <output_dir> --deploy <packroot> [--yes] [--no-backup]
python scripts/generate_quests.py <output_dir> --quests-dir <dir> [--yes]   # explicit target
```

`--deploy` (or `--quests-dir`) runs AFTER generation, copying `<output_dir>/quests/` into `<packroot>/config/ftbquests/quests/` (or the explicit dir). Without `--yes` it prints the overwrite report and writes nothing — a preview. With `--yes` it applies. The logic lives in `ftbq/deploy.py`; `--dry-run` cannot be combined with `--deploy` (nothing would be generated to deploy).

Each source game file is classified against the target:

| Action | When | What happens |
|--------|------|--------------|
| `new` | file absent in target | copied verbatim (name unchanged) |
| `unchanged` | present with identical signature | skipped, no backup |
| `merge` | present + kind ∈ {`data`, `chapter_groups`, `lang`} | merged; original backed up first |
| `replace` | present + kind ∈ {`chapter`, `manifest`} | original backed up, then overwritten with the skill's bytes |

Signatures are `sha256` over `canonical_json(plain)` (keeps `id`, sorts keys) — so whitespace/key-order differences don't read as overwrites, and a no-op re-deploy reports nothing changed. Files under `.ftbq-cache/` (except `manifest.json5`), under `.ftbq-backup/`, and `quests.spec.json5` are never deployed.

### 16c. Merge rules (new + original together)

- `data.json5` — deep merge: nested dicts merge recursively, source overrides target on collisions. The pack's keys are kept; the skill's keys are added.
- `chapter_groups.json5` — union of `chapter_groups[]` by `id`; the source overrides a same-`id` group, the target's other groups are kept (target order preserved).
- `lang/<locale>/quests.json5` — flat key union (`{**target, **source}`). The skill's keys are `quest/chapter.<skill-hex>.*` and only belong to skill-owned objects, so overriding them is correct; **the pack's lang keys for quests the skill does not own are preserved** — the regression a blind copy would have destroyed.

### 16d. Backup layout (`.ftbq-backup/<ts>/`)

Before any merge or replace, the target original is copied to a co-located, dot-prefixed mirror that preserves the relative path verbatim:

```
<target>/.ftbq-backup/<UTC-timestamp>/
├── chapters/<name>.json5          (same name, same relative path as the replacement)
├── data.json5
├── lang/<locale>/quests.json5
└── BACKUP_INDEX.json5
```

`BACKUP_INDEX.json5` records `backed_up_at`, `source_root`, `target_root`, and one entry per backed-up file: `rel_path`, `kind`, `reason` (`merge`|`replace`), `backup_path`, `original_signature`, `replaced_by_signature`. To roll back, delete the new files and restore from this folder. `--no-backup` skips backups entirely (irreversible).

`.ftbq-backup/` is dot-prefixed, so FTB Quests' chapter scanner skips it (same reason `.ftbq-cache/` is safe, §14) — backups never leak into the loaded book.

### 16e. The overwrite report

The report groups files into 🆕 NEW, ⚠️ OVERWRITE (merge + replace — the prominent highlight for files touching modpack originals), and ✅ UNCHANGED, with per-file stats (`+N keys, keeps K, overrides M` for merges; `quest-ID overlap: N` for chapter replaces):

```
📦 FTB Quests deploy plan
   source: <output_dir>/quests
   target: <packroot>/config/ftbquests/quests

🆕 NEW (1, safe to add):
   .ftbq-cache/manifest.json5

⚠️  OVERWRITE — REPLACES modpack originals (backup → .ftbq-backup/<ts>/):
   chapters/intro.json5    (full replace; quest-ID overlap: none)
   data.json5              (merge: +2 keys, keeps 1, overrides 1)
   lang/en_us/quests.json5 (merge: +0 keys, keeps 1, overrides 0)

📊 1 new, 3 overwrite (backed up), 0 unchanged
   Re-run with --yes to apply.
```

### 16f. Deploy vs `--adopt` / `--mode ask`

`--deploy` is **file-level**: whole files are merged (additive kinds) or backed-up-then-replaced (chapters/manifest). It does not merge individual quests across a chapter-name collision — the skill's chapter wins wholesale, with the original backed up.

For **quest-level** merge (keep an existing pack quest inside a chapter the skill also owns), point `generate_quests.py` at the pack's quests folder directly with `--adopt` (first run: mark everything on disk as user-added) or `--mode ask` / `--mode preserve` (subsequent runs: the manifest distinguishes skill-owned vs user-added vs user-edited quests, §14). That path needs the manifest in the live folder; `--deploy` copies it there as part of the manifest replace.

`reward_tables/<name>.json5` files deploy like chapters: NEW files are copied verbatim, a same-named table in the target is backed up then replaced. They are never merged (a table is one object).

---

## 17. Reward tables

A reward table is a weighted pool of rewards, stored as `reward_tables/<name>.json5` and referenced by `loot`/`random`/`choice`/`all_table` rewards. The skill generates them from the spec's top-level `reward_tables` list (§13a) and resolves a reward's `table: "<name>"` to the on-disk `table_id`.

> **`table_id` is a decimal *long*, not a hex string.** FTB Quests reads it as a number (`RandomReward.readData` → `getLong`). It is the numeric value of the table's 16-hex `id` (e.g. an id of `"0123456789ABCDEF"` → `table_id: 81985529216486895`). The generator computes this via `int(hex_id, 16)` (top-bit-masked, so it always fits a Java `long`, §9).

### 17a. Spec shape

```json5
reward_tables: [{
  name: "common_loot",          // → reward_tables/common_loot.json5
  empty_weight: 0,              // optional; >0 adds a "nothing" chance
  loot_size: 1,                 // optional; roll multiplier (default 1)
  hide_tooltip: false,          // optional; ABSENT reads as true → tooltip hidden
  use_title: false,             // optional; ABSENT reads as true → table title forced
  rewards: [                    // each entry = a reward + a weight
    { name: "diamond", type: "ftbquests:item", item: "minecraft:diamond", weight: 10 },
    { name: "gold",    type: "ftbquests:item", item: "minecraft:gold_ingot", count: 2, weight: 5 },
    { name: "buff",    type: "ftbquests:command", command: "/effect give {p} minecraft:speed 30 1", weight: 1 },
  ],
  // optional:
  loot_crate: { /* LootCrate block — item/drop settings; passthrough */ },
  loot_table_id: "minecraft:gameplay/fishing",  // optional; back the table with a vanilla loot table
}]
```

### 17b. On-disk file (`reward_tables/<name>.json5`)

```json5
{
  id: "<16hex>",                // reward_table_id(pack, name)
  rewards: [
    {
      id: "<16hex>",            // table_reward_id(pack, table, entry)
      // type omitted for item rewards (implicit); present for everything else
      item: { id: "minecraft:diamond", count: 1 },
      weight: 10,               // omitted when == 1
    },
  ],
  empty_weight: 0,              // only if > 0
  loot_size: 1,
  hide_tooltip: false,          // emitted explicitly (absent → true trap)
  use_title: false,
  // loot_crate / loot_table_id only if set
}
```

### 17c. The `hide_tooltip` / `use_title` trap

`RewardTable.readData` defaults an **absent** `hide_tooltip` to `true` (tooltip hidden) and `use_title` to `true` (the table's title is forced onto the reward). To show players the list of possible rewards, you must emit `hide_tooltip: false` explicitly. The generator always emits both fields (defaulting to `false` = show tooltip, don't force a title) so the intent is unambiguous; set them `true` in the spec for mystery/loot-crate tables.

### 17d. Referencing a table from a reward

In the spec, a `loot`/`random`/`choice`/`all_table` reward uses `table`:

```json5
rewards: [{ name: "rng", type: "ftbquests:random", table: "common_loot" }]
```

`table` is either a skill table **name** (resolved to the decimal `table_id`) or a raw **16-hex id** for an external table (passed through as the decimal long). The generator drops `table` and writes `table_id`. The validator flags a `table_id` matching no table in the book with `E_TABLE_MISSING` (§15; a warning — it may be an external table).

---

## 18. Quest links

A quest link (`quest_links[]` on a chapter) displays a quest from another chapter at a position in this chapter — a "mirror" that shares the original's title, icon, and completion. On-disk shape (`QuestLink.writeData`):

```json5
quest_links: [
  {
    id: "<16hex>",              // quest_link_id(pack, chapter, name)
    linked_quest: "<16hex>",   // the mirrored quest's id
    x: 3.0, y: -1.0,           // required
    shape: "square",           // optional; omit to inherit the chapter default
    size: 1.0,                 // optional; omit when 1
  },
]
```

In the spec, `linked_quest` is a `name`/`<chapter>/<quest>` ref (resolved to hex) or a raw 16-hex id (external quest, passed through). `x`/`y` are required on disk (the generator defaults them to `0.0`).

---

## 19. Chapter images

A chapter background image (`images[]` on a chapter). On-disk shape (`ChapterImage.writeData`):

```json5
images: [
  {
    id: "<16hex>",             // image_id(pack, chapter, name)
    image: "minecraft:textures/gui/presets/isles.png",  // required: texture path / item id
    x: 0.0, y: 0.0,            // required
    width: 4.0, height: 2.0,   // required
    rotation: 90.0,            // required; degrees, -180..180
    color: 16777215,           // optional int (RGB); omit = white
    alpha: 128,                // optional 0-255; omit = 255
    order: 1,                  // optional z-order; omit = 0
    click: "/say hi",          // optional; command run on click
    dev: true,                 // optional; editors-only (hidden in play)
    corner: true,              // optional; align to corner vs center
    dependency: "<16hex>",     // optional; show only after this quest completes
  },
]
```

In the spec, `dependency` is a `name`/`<chapter>/<quest>` ref (resolved to hex) or a raw 16-hex id. The generator emits `x`/`y`/`width`/`height`/`rotation`/`image` always (they're required on disk) and the optional fields only when set.

---

## 20. Empirical findings from shipped modpacks

Audited 2026-06-29 against two shipped Create-series packs. (A third pack the user named — 命运齿轮FOM, MC 1.21.1 — has **no FTB Quests installed at all**; it is a pure Create + JEI pack with only `ftblibrary-client.snbt` present. Excluded from the audit.) These measurements are the evidence behind the §12 version-split revision and the SKILL.md "Field findings" section; cite them when justifying layout/reward recommendations.

### 20a. The two SNBT variants (evidence for §12)

| Pack | MC | Loader | FTB Quests | Serialization | Text model |
|---|---|---|---|---|---|
| Create: Delight Remake | 1.20.1 | Forge | 2001.4.17 | SNBT | **inline** (`title:`/`description:` on the quest object); no `lang/` |
| Mechanomania | 1.21.1 | NeoForge | 2101.1.21 | SNBT | **lang files** (`lang/<locale>.snbt`, `quest.<HEX>.title`); quest objects carry **no** inline text (0 title / 0 description / 0 subtitle across all quests) |

`data.snbt` defaults observed: both set `default_quest_shape: "circle"`, `default_consume_items: false`, `default_reward_team: false`, `progression_mode: "flexible"`, `version: 13`. Create: Delight additionally sets `pause_game: true`, `show_lock_icons: true`, `title: "机械动力：齿轮盛宴"`, and a custom pack `icon`. Mechanomania ships `lang/en_us.snbt` + `lang/zh_cn.snbt` + `lang/th_th.snbt`.

### 20b. Scale & layout

**Create: Delight Remake** — 41 chapters, **2,295 quests**. Largest chapters: Mouse_Chef (304), Animal_Companions (183), Difficulty_System (126), Masterful_Machinery (99), Ingredient_Essence (98). Six `chapter_groups` with colored titles (`&2伟大工程师`, `&b外星工程师`, `&e超级大厨`, `&5Tetra•模块化工具`, `&6世界之旅`, `&d生活小技巧！`). Coordinate example (Introduction): hub `hexagon` `size: 4.0` at `(0, 0)` → dependent `pentagon` `size: 2.0` at `(4, -4)` (fan-out, x-step ~4, big hub on the spine).

**Mechanomania** — 18 chapters, **395 quests**. Largest: create2 (81), create1 (67), lifestyle (44), touhoulittlemaid (42), l2complements (33). Three `chapter_groups` (Overworld slow-life, The End combat, Other Mods). Coordinate example (lifestyle): `diamond` cluster fanning around a hub with **fractional** coords `(-4.25, -1.5)`, `(-5.0, -0.75)`, `(-4.25, 0.0)`, `(-3.5, -0.75)` — symmetric x-spread, lines don't cross.

### 20c. Shape, size & anti-clutter flag usage

| Metric | Create: Delight Remake | Mechanomania |
|---|---|---|
| Quests w/ explicit shape | ~8 % (rest default `circle`) | ~8 % |
| Explicit shapes (count) | square 266, rsquare 114, hexagon 51, gear 32, pentagon 32, circle 12, octagon 5, diamond 8 | diamond 12, gear 7, rsquare 7, heart 2, square 3, pentagon 1, hexagon 1 |
| Sizes | 1.0×79, 1.5×211, 1.75×55, 2.0×280, 3.0×5, 4.0×16, 6.0×1, 1.25×10 | 1.5×45, 2.0×7, 3.0×4 |
| `hide_until_deps_visible` | 72 | 0 |
| `hide_dependent_lines` | 17 | 0 |
| `secret` | 12 | 0 |
| `dependency_requirement` | `one_started` 63, `one_completed` 44, `all_started` 6 | `one_completed` 1 (rest default `all` → near-linear) |

Both packs set `default_quest_shape: ""` (empty) on every chapter, inheriting `circle` from `data`. Takeaway: `hide_until_deps_visible` is worth the bookkeeping above ~50 quests/chapter (Create: Delight uses it in its big chapters); a small pack (Mechanomania, max chapter 81, total 395) can ship with none and still read cleanly.

### 20d. Task & reward type frequencies

| | Create: Delight Remake | Mechanomania |
|---|---|---|
| **Tasks** | item 2185, checkmark 170, kill 163, observation 106, advancement 87, dimension 34, stat 31, biome 8, structure 5 | item 399, checkmark 29, kill 11, advancement 11, dimension 2, observation 2, structure 1 |
| **Rewards** | item 803, xp 195, **custom 116**, random 85, xp_levels 22, choice 13, all_table 5, command 5, loot 2 | item 40, choice 3 (no xp/command/loot/custom/random — minimalist) |

### 20e. Advanced authoring features seen in the wild

1. **`{image:}` in descriptions** — `description: [ "…", "{image:createdelight:textures/images_for_readme/document_qr_code.png width:100 height:100 align:center}" ]` embeds an image inline.
2. **In-text placeholder resolver** — `{item.modid:name}`, `{block.modid:name}`, `{dimension.modid:name}`, `{entity.modid:name}`, `{effect.modid:name}` auto-render the **localized Minecraft name** (so one `en_us` file + `zh_cn` override covers hundreds of mod items). Usable in both lang-file and inline text. Plus `&6`/`&r`/`&d`-style formatting codes.
3. **Clickable JSON-text subtitle (cross-quest navigation)** — `subtitle: "{ \"text\":\"季节系统\", \"underlined\":\"true\", \"color\":\"blue\", \"clickEvent\":{ \"action\":\"change_page\", \"value\":\"1E7A476EE0C13AD1\" } }"` — clicking jumps the book to that quest id.
4. **Custom (KubeJS) rewards with `tags`** — `{ id, auto: "enabled", tags: ["rank_1"], team_reward: false, type: "custom" }`; KubeJS reads the tag to fire logic. Used 116× in Difficulty_System for rank progression. (`auto` values seen: `"enabled"`, `"no_toast"`.)
5. **Command reward as a gamerule toggle** — a Settings chapter of `silent: true` command-reward quests, e.g. `title: "死亡不掉落"` (keep inventory).
6. **Command rewards use `@p`/`@a` selectors** — `command: "/say Hi, @p!"`. (`{p}` is FTB's own name substitution; selectors work in any selector-accepting command.)
7. **Reward table (SNBT) shape** — `{ icon: "ae2:engineering_processor", id, loot_size: 1, order_index: 15, rewards: [ { item: "ae2:logic_processor" }, … ], title: "处理器" }`. Bare-string items; the observed tables omit `empty_weight`/`hide_tooltip`/`use_title`.
8. **`dependencies` reference the parent by raw 16-hex id** as the normal hand-authored style — `dependencies: ["55C42BCE0E399B3D"]` (both packs). The skill's `name`-based wiring is a generator convenience; when hand-editing, use the hex.
9. **Chapter/task fields observed** — chapter: `autofocus_id`, `default_hide_dependency_lines`, `filename`, `group`, `icon` (string OR object), `order_index`, `quest_links`, `images`. Task: `disable_toast`, `task_screen_only`, `icon`, `title` (inline title on tasks is valid in SNBT; the §7 "no inline task title" rule is JSON5-only).
10. **Item-object shape is MC-version-dependent** — 1.20.1: `{ Count: 1, id: "…", tag: {…} }` (capital `Count`, NBT `tag`); 1.21.1: `{ count: 1, id: "…", components: {…} }` (lowercase `count`, data `components`). Both also accept a bare string `item: "modid:item"`.

### 20f. Localization workflow for the SNBT + lang-file variant (Mechanomania)

Quest `.snbt` objects carry only structural fields (`id`, `x`, `y`, `shape`, `size`, `dependencies`, `tasks`, `rewards`) — no `title`/`description`. `lang/<locale>.snbt` is a **flat** SNBT file, one `"key": value` per line (keys are quoted because they contain dots); `quest_desc` and `chapter_subtitle` values are SNBT lists. Because the `{item.*}`/`{block.*}` placeholders resolve client-side to localized names, a single `en_us` lang file plus a `zh_cn` override suffices even when the book references hundreds of mod items — there is no need to hand-translate every item name into the quest text.

### 20g. Culinary chapter patterns (Create: Delight Remake, 超级大厨 group)

The food-focused pack is the richest source of catalog-layout patterns. The 超级大厨 group (`7D0A1432AAAD0EBA`) plus two food-adjacent dimension chapters, measured:

| Chapter | Quests | Layout (x×y range → w×h, aspect) | Shapes (explicit) | Deps | Tasks | Rewards |
|---|---|---|---|---|---|---|
| Mouse_Chef | 304 | −52..14 × −22..48 → 66×70, 0.94 (square) | rsquare×12 (size 4.0), circle×1 | 46/304 | item×325, checkmark×11 | item×29, xp×52 |
| Ingredient_Essence | 98 | −78.5..−65 × −20..−7 → 13.5×13, 1.04 | none | 4/98 | item×102 | item×6, xp×32 |
| Feast_Afoot | 88 | −8.5..9.5 × −9..9.5 → 18×18.5, 0.97 | hexagon×1, rsquare×16, square×3, circle×1 | 85/88 | item×108, checkmark×7, stat×4, observation×4 | item×40, xp×16 |
| Youkais_Homecoming | 74 | −4.5..18.5 × −15..26 → 23×41, 0.56 (tall) | square×72, rsquare×1 | 72/74 | item×50, checkmark×23, kill×14, advancement×10 | item×71, random×19, xp_levels×17, all_table×5, choice×5, command×2 (29 table_id refs) |
| Candyland | 42 | −4.5..7 × −6..11.5 → 11.5×17.5, 0.66 | none | 40/42 | item×56, advancement×6, kill×2 | item×22, choice×1 |
| Bumble_Zone | 24 | −2..13 × −3..3 → 15×6, 2.50 | none | 23/24 | item×21, dimension×1, biome×1, observation×1, checkmark×1 | item×6, xp×23 |

Across all six: `only_from_crafting: true` = **0**, `consume_items: true` = **0** (only 1 in Youkais). Food tasks are "obtain the dish", never "craft-only" or "consume".

**The capstone-hub catalog (Mouse_Chef `cake` block, quoted from disk):**
```snbt
# category hub — depends on ALL 18 cake-variant cells, hides their lines, coin reward
{
  dependencies: [ "50AD608C64782ED9", "67E1EA2F2C985376", /* …16 more… */ ]
  hide_dependency_lines: true
  icon: "minecraft:cake"
  id: "4E3082C7AC773F5B"
  shape: "rsquare"
  size: 4.0d
  subtitle: "你已经是一个合格的蛋糕大师了（赞赏脸）"
  tasks: [ { id: "2BDDC2B78E5D9DAC", type: "checkmark" } ]
  title: "cakeeeeeeee"
  rewards: [ { id: "…", item: "createdelightcore:netherite_coin", type: "item" } ]
  x: -40.0d
  y: -22.0d
}
# one of the 18 cells — independent, no deps, size 2.0 default circle, "obtain cake"
{
  id: "690FB96658B4BB38"
  size: 2.0d
  tasks: [ { id: "601BF3ACBDEF8288", item: "minecraft:cake", type: "item" } ]
  x: -37.0d
}
```

**The tutorial-explainer quest (Feast_Afoot humidity system, quoted from disk):**
```snbt
{
  description: [
    "种子有对应&9湿度需求&r，&4偏移1级减慢生长&r，&4偏移2级&r及以上时&4大幅减慢生长甚至无法生长&r"
    "不同生物群系有不同&e自然湿度&r，且部分&e随季节变化&r"
  ]
  icon: "eclipticseasons:hygrometer"
  shape: "rsquare"
  size: 1.0d
  subtitle: "湿度有&e五级&r，为&4干旱&r、&6干燥&r、&a一般&r、&9湿润&r、&1潮湿"
  tasks: [ { id: "…", stat: "minecraft:play_time", title: "湿度系统", type: "stat", value: 1 } ]
  rewards: [ { id: "…", item: "eclipticseasons:hygrometer", type: "item" } ]
}
```

**Description formatting in food chapters.** `&e<phrase>&r` is yellow-highlighted *prose* (e.g. `&e自然湿度&r`, `&e五级&r`), **not** an item-id link — a pack-wide grep for `&e<modid:item>…&r` returns **0 matches** across all 41 chapters. Stable per-tier colors (`&4`/`&6`/`&a`/`&9`/`&1`) carry the meaning. True item-name rendering uses the `{item.modid:name}` placeholder resolver (§20e.2) in lang-file packs; inline-text packs (Create: Delight) just name the item in prose or set it as the quest `icon`.

**Design takeaways** (mirrored in SKILL.md "Culinary / recipe-catalog quest lines"): (1) split system-tutorial chapter (linear, text-heavy, `stat`/`checkmark` acknowledgement + tool reward) from recipe-catalog chapter (square grid, no text); (2) catalog = `rsquare size 4.0` capstone hub depending on all cells with `hide_dependency_lines: true`, cells independent `size 2.0` default-circle `item` tasks; (3) `item` "obtain" not "craft" (`only_from_crafting`/`consume_items` stay false); (4) rewards concentrated on hubs + explainers, sparse on cells; (5) color-code tiers; (6) scatter big catalogs to remote coordinate offsets.

