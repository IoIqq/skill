# FTB Quests — Authoritative Reference

Deep reference for generating FTB Quests configs. Verified against `FTBTeam/FTB-Quests` source (current `main`, MC `26.1.x`) on 2026-06-19. See also the memory note `[[ftb-quests-format]]`.

> **Read this if:** you need exact field names, type-specific parameters, a full worked example, or must target an older `.snbt` modpack. The main `SKILL.md` has the essential templates.

---

## 1. JSON5 syntax (modern format) — the rules that break things

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

## 3. `data.json5` (required)

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
- `default_autoclaim_rewards`: one of `"default"`, `"enabled"`, `"disabled"`.
- `emergency_items`: optional list of item objects (`emergency_items: [{ id:"minecraft:bread", count:1 }]`).
- `version`: use `13` (current quest-file `VERSION`; a lower value may trigger migration on load).

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
  quest_links: [ /* optional: { id, linked_quest } */ ],
  images: [ /* optional chapter background images */ ],
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

| `type` | Key fields | Notes |
|--------|-----------|-------|
| `ftbquests:item` | `item: {id,count:1}`, `count` (qty, omit if 1), `consume_items`, `only_from_crafting`, `match_components` (`"fuzzy"`/`"strict"`), `task_screen_only` | Most common. Item object's `count` is always 1; real quantity is the sibling `count`. |
| `ftbquests:fluid` | `fluid` (object/id), `amount` (long, mB) | |
| `ftbquests:forge_energy` | `value` (long, FE) | Forge builds only (not in `common`). |
| `ftbquests:xp` | `value` (long, XP points) | Spend player XP. |
| `ftbquests:kill` | `entity` (entity id string), `value` (count) | |
| `ftbquests:advancement` | `advancement` (id), `criterion` (optional criterion name) | |
| `ftbquests:stat` | `stat` (stat id), `value` (long) | Vanilla statistics. |
| `ftbquests:location` | `dimension`, `x`, `y`, `z` (doubles), optional `ignore`/range | Visit coords. |
| `ftbquests:dimension` | `dimension` (resource id) | Enter a dimension. |
| `ftbquests:biome` | `biome` (resource id) | Visit a biome. |
| `ftbquests:structure` | `structure` (structure id) | Find a structure. |
| `ftbquests:observation` | `timer` (ticks), `observe` (`"observe"`/`"detect`") | Look at / hold on something. |
| `ftbquests:gamestage` | `stage` (string) | Requires GameStages mod. (Type id is `gamestage`, **not** `stage`.) |
| `ftbquests:checkmark` | *(none)* | Manual toggle quest. |
| `ftbquests:custom` | `title`/`icon` optional + custom data | KubeJS / scripted. |

### 7b. Rewards

| `type` | Key fields | Notes |
|--------|-----------|-------|
| `ftbquests:item` | `item: {id,count}` (count IN object = qty given), `team` (bool), `exclude_from_claim_all` | Item reward's real count lives in the object. |
| `ftbquests:xp` | `xp` (long, points) | |
| `ftbquests:xp_levels` | `xp_levels` (int) | |
| `ftbquests:command` | `command` (string, the command; `@player`/`{player}` placeholder supported) | Runs as the server/op. |
| `ftbquests:loot` | `loot_size`, `table` (references a reward_table file) | Loot crate from a table. |
| `ftbquests:random` | `table` | One random reward from a table. |
| `ftbquests:choice` | `table` | Player picks one from a table. |
| `ftbquests:all_table` | `table` | Give every reward in a table. |
| `ftbquests:advancement` | `advancement` (id) | Grant an advancement. |
| `ftbquests:toast` | `description` (string) | Show a toast/notification. |
| `ftbquests:gamestage` | `stage` (string) | Grant a game stage. |
| `ftbquests:custom` | custom data | KubeJS / scripted. |
| `ftbquests:currency` | — | Disabled by default; needs an economy integration. |

`table` references a `reward_tables/<filename>.json5` by the RewardTable's id/string.

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

> **Legacy packs:** older FTB Quests (`.snbt`) stores text INLINE as `title: "..."` and `description: ["..."]` inside the quest object. If a generated pack shows blank titles in-game, you are on the inline version — move the text back into the object and drop the lang files.

---

## 9. ID generation

Every quest/task/reward/chapter needs a stable 16-char uppercase hex `id` (e.g. `1A2B3C4D5E6F7890`). For deterministic, collision-free generation, hash a stable path and take 16 hex chars of the digest, uppercased:

```
id = md5("<packslug>/<chapter>/<object>/<name>").hex()[0:16].upper()
```
Rules: must be unique within the whole quest book; dependency ids in `dependencies: [...]` must exactly match the target quest's `id`. A 16-hex slice of an MD5 of distinct strings collides with negligible probability; if you regenerate, keep names stable so ids stay stable.

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
          item: { id: "minecraft:apple", count: 2 },
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

## 12. Legacy SNBT format (older modpacks, ≤1.20 / early-1.21)

If an existing pack uses `.snbt` files (Minecraft `TagParser`-style), generate in that dialect:

- Extension `.snbt`; location `config/ftbquests/quests/chapters/*.snbt`.
- **No commas** — whitespace/newlines separate fields.
- Type suffixes: bytes `1b`/`0b`, shorts `1s`, ints `1`, longs `1L`, doubles `0.0d`, floats `0.0f`.
- Items commonly as strings `item: "minecraft:oak_log"` or legacy objects `{ id:"minecraft:oak_log", Count:1b }`; quantity via `Count` (byte) or a `count` field depending on version.
- **Text INLINE**: `title: "..."`, `subtitle: "..."`, `description: ["line1", "line2"]` directly in the quest object — no separate lang files.
- Quest ids are hex strings; dependency format identical in spirit.

When porting old→new, inline text moves into lang files, item strings become `{id,count}` objects, and all `0.0d`/`1b` suffixes are dropped.
