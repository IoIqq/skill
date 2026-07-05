# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — Minecraft 1.20.1 (SNBT) support

- **`format: "snbt"`** — the skill now generates for MC 1.20.1 and earlier,
  which serialize via `dev.ftb.mods.ftblibrary.snbt.SNBT` (`.snbt` files),
  not JSON5. `data.snbt` / `chapters/*.snbt` / `reward_tables/*.snbt` /
  `chapter_groups.snbt`, **no lang files** (text is inline). `load_spec`
  accepts `snbt` (previously hard-rejected). The JSON5 (1.21+) path is
  untouched — zero regression to existing packs.
- **`ftbq/snbt.py`** — a canonical SNBT emitter (`dumps_snbt` /
  `dump_file_snbt`) mirroring `canonical.py`'s path-tracking + per-path
  key-order contract, plus a focused `SNBTParser` port (`parse_snbt` /
  `parse_snbt_file`). Per-field NBT type suffixes (`ItemTask.count`→`N L`,
  `XPTask.value`→`N L`, `x/y/size`→`N.Nd`, `weight`/`empty_weight`→`N.Nf`,
  `id`→quoted hex string) resolved from the value's dotted path, verified
  against each 1.20.1 `writeData`.
- **Generator** — the emit layer (`_emit_chapter_file` / `_emit_data_file` /
  `_emit_chapter_groups` / `_emit_reward_table_file` / `merge_chapter` /
  `merge_reward_table`) is parametrized by format; SNBT skips lang emission
  and passes `title`/`subtitle`/`description` through inline. The manifest
  records `format` and `.snbt` file paths (the manifest itself stays
  `.json5` — skill-internal, FTB Quests' scanner skips it).
- **Validator** — `BookModel.format` auto-detected from the on-disk
  extension; `load_book`/`_load_dir` dispatch `ftbq.json5` vs `ftbq.snbt`;
  SNBT books skip `lang/`. The JSON5-only checks `E_TYPE_SUFFIX` (suffixes
  are legal SNBT) and `E_INLINE_TEXT_MODERN` (inline text is required in
  SNBT) are skipped for `format: "snbt"`; structural checks (ids, deps,
  reward tables, manifest, coord dups, bare-string items) run unchanged via
  a Node-tree wrap of the parsed SNBT.
- **Deploy** — `_classify` / `scan_root` / `_load` / `_emit_merged` handle
  `.snbt` by extension (merge helpers are dict-based, unchanged). The
  skill-internal `manifest.json5` / `BACKUP_INDEX.json5` stay JSON5.
- **Reference §12** rewritten as a full, source-verified 1.20.1 SNBT
  section (syntax table, field→type table, inline text, `id` hex-string +
  top-bit mask, worked example); §1/§3/§13/§15/§16 and `SKILL.md` updated
  for the version split.
- **51 new tests** (`test_snbt_emit`, `test_snbt_parse`,
  `test_snbt_generate`, `test_snbt_validate`, +`test_deploy`/`test_id_stability`
  cases). Suite now 221 tests.

### Added — Reward tables, quest links & chapter images (source-verified)

- **Reward table generation** — the skill can now author the
  `reward_tables/<name>.json5` files that `loot`/`random`/`choice`/
  `all_table` rewards depend on (previously these reward types were
  documented but ungeneratable, so the referenced tables were missing).
  New spec top-level `reward_tables` list; `rewards[]` entries carry a
  `weight`; `empty_weight`/`loot_size`/`hide_tooltip`/`use_title`/
  `loot_crate`/`loot_table_id` supported. `ftbq/ids.py` gains
  `reward_table_id` + `table_reward_id`.
- **`table_id` resolution** — a `random`/`loot`/`choice`/`all_table`
  reward references a table by `table: "<name>"` (or raw 16-hex for an
  external table); the generator resolves it to the decimal **long**
  `table_id` FTB Quests reads (`RandomReward.readData` → `getLong`).
  `ftbq/ids.py` gains `hex_to_long`.
- **Quest links** (`quest_links[]` on a chapter) — mirrors of a quest
  from another chapter at a position; `linked_quest` resolves name→hex
  (or passes a raw hex through). `ftbq/ids.py` gains `quest_link_id`.
- **Chapter background images** (`images[]` on a chapter) — full
  `ChapterImage` field set (`image`/`x`/`y`/`width`/`height`/`rotation`/
  `color`/`alpha`/`order`/`click`/`dev`/`corner`/`dependency`); `dependency`
  resolves name→hex. `ftbq/ids.py` gains `image_id`.
- **Chapter field passthrough** — `_build_chapter` now passes spec
  fields like `progression_mode`, `always_invisible`, `autofocus_id`,
  `default_quest_size` through to the emitted chapter (previously
  dropped). `name`/`layout` remain spec-only.
- **Validator: reward tables** — loads `reward_tables/*.json5`, indexes
  table + entry ids, and adds `E_TABLE_MISSING` (warning) when a
  `table_id` matches no table. Reward-table id/entry-id format and
  manifest hash-mismatch checks added; `_load_dir` shared by chapters
  and reward tables.
- **Deploy: reward tables** — `reward_tables/*.json5` deploy like
  chapters (NEW copied verbatim; same-named backed up then replaced).
- **Reference §17/§18/§19** — full reward-table, quest-link, and
  chapter-image documentation with on-disk shapes, plus the
  `hide_tooltip`/`use_title` absent→true trap and the `table_id`-is-a-
  decimal-long note.
- **49 new tests** (`test_reward_tables`, `test_quest_links_images`,
  `test_task_reward_fields`, +`test_ids`/`test_validator`/`test_deploy`
  cases). Suite now 170 tests.

### Fixed — correctness bugs that broke generated packs

- **ID top-bit mask** — `make_id` now masks the md5 digest's top bit
  (`& 0x7FFFFFFFFFFFFFFF`) so every id parses back cleanly in FTB Quests.
  ~50% of previously-generated ids had a top hex digit of 8-F, which
  `Long.parseLong(hex, 16)` throws on; `readID` swallowed the exception
  and regenerated a random id, silently breaking every `dependencies` /
  `linked_quest` / image `dependency` reference to it. This also keeps
  `table_id` decimals within Java `long` range. (Reference §9.)
- **Item reward/task quantity** — FTB Quests reads the SIBLING `count`
  field (`ItemTask`/`ItemReward`); the count inside the `item` object is
  ignored. The generator previously buried the reward count in the
  object, so an `item: {id:"apple", count:2}` reward granted **1**. It
  now lifts any object count to the sibling `count` (object count = 1),
  for both tasks and rewards. (Reference §7/§11/§13d.)
- **`ftbquests:xp` missing `points`** — `XPTask.readData` throws
  (`orElseThrow`) if `points` is absent, failing the whole book load.
  The generator now defaults `points: true`. (Reference §7a.)

### Changed — field reference corrections (source-verified)

- **Command reward** — placeholders are `{p}`/`{x}`/`{y}`/`{z}`/
  `{chapter}`/`{quest}`/`{team}`/`{team_id}`/`{long_team_id}`/
  `{member_count}`/`{online_member_count}` (not `@player`/`{player}`),
  and the reward runs as the **player** unless `permission_level` (1-4)
  elevates; `silent` and `feedback_message` documented. (§7b.)
- **Observation task** — fields are `observation_type` (enum:
  `BLOCK`/`ENTITY`/…) + `to_observe` + `timer`, not `observe`. (§7a.)
- **Location task** — `ignore_dimension`, not `ignore`. (§7a.)
- **kill / energy / gamestage tasks** — added `entityTypeTag`/
  `custom_name`/`nbt_filter`, `max_input`, `team_stage`; `fluid` is a
  single FluidStack object (no separate `amount`); task-level
  `optional_task`; `consume_items`/`only_from_crafting` are Tristate;
  `match_components` values `none`/`fuzzy`/`strict`. (§7a.)
- **item / gamestage rewards** — added `random_bonus`/`only_one`,
  `remove`; reward-base `auto`/`exclude_from_claim_all`/
  `ignore_reward_blocking`/`disable_reward_screen_blur`. (§7b.)
- **`data.json5`** — documented the full setting set (`drop_loot_crates`,
  `disable_gui`, `grid_scale`, `pause_game`, `lock_message`,
  `progression_mode`, `detection_delay`, `show_lock_icons`,
  `drop_book_on_death`, `hide_excluded_quests`, `fallback_locale`,
  `verify_on_load`, `emergency_items`), noting the absent→`"linear"`
  default for `progression_mode`. (§3.)

### Added — Safe deploy & clean output layout

- **Clean `quests/` output subfolder** — `generate_quests.py` now writes
  every game file under `<output_dir>/quests/` (a clean, copy-ready tree);
  `quests.spec.json5` stays at `<output_dir>` root and is never deployed.
  Copy `quests/` whole into `<pack>/config/ftbquests/quests/` for a new
  pack.
- **`--deploy <pack_root>`** (and `--quests-dir <dir>`) — safely merges the
  generated `quests/` folder into a live pack instead of blind-copying:
  additive files (`data.json5`, `chapter_groups.json5`, lang) are **merged**
  so new content and the pack's existing content coexist in one file;
  same-named chapters and the manifest are **backed up then replaced**.
  File names never change.
- **Overwrite report** — `--deploy` prints a ⚠️ OVERWRITE block flagging
  every file that touches a modpack original; writes nothing until `--yes`.
- **`.ftbq-backup/<timestamp>/` mirror** — overwritten originals are backed
  up at the same relative path inside a dot-prefixed folder (FTB's scanner
  skips it, same as `.ftbq-cache/`), with a `BACKUP_INDEX.json5` audit
  trail. `--no-backup` skips it (irreversible).
- **`ftbq/deploy.py`** — shared core module with the deploy logic
  (`scan_root`, `plan`, `apply`, `render_report` + merge helpers),
  depending only on `ftbq.*`. Documented in reference §16.
- **19 new tests** (`tests/test_deploy.py`) covering new/unchanged/merge/
  replace, the lang-merge regression, backup index, name preservation, and
  the `--yes` gate. Existing generator tests updated for the `quests/`
  subfolder. Total suite now 140 tests.

### Added — C3 hybrid architecture

- **`scripts/extract_mods.py`** — parses every `mods/*.jar` in a modpack
  (NeoForge / Forge / Fabric / legacy mcmod) and writes
  `.ftbq-cache/mods.json5` with per-mod metadata. Step 1.5 of the
  interview reads this cache so chapter suggestions don't depend on the
  user hand-listing mods.
- **`scripts/generate_quests.py`** — code-driven generator that owns
  IDs, coordinates, dependency wiring and the manifest, while the LLM
  owns titles, descriptions, task and reward content via
  `quests.spec.json5` and `lang/<locale>/quests.json5` placeholders.
  Same spec → byte-identical output.
- **Incremental merge** (`--mode {overwrite,preserve,ask}`) — re-runs
  classify each on-disk quest as pristine, content-edited,
  position-edited, user-added, or skill-deleted, and respect user edits
  according to the mode. Position edits are always preserved.
- **`--adopt`** flag — first run on an existing pack marks every
  on-disk quest as user-added; the generator only adds new content
  going forward.
- **Rename detection** — when a quest's `name` disappears from the spec,
  the generator prompts for the new name and preserves the original hex
  ID via the manifest's `aliases` field, so player progress is not lost.
- **`.ftbq-cache/manifest.json5`** — content-hash registry of every
  skill-owned object. Stored in a hidden directory so the FTB Quests
  scanner skips it.
- **`ftbq/` shared core** — string-aware JSON5 lexer/parser with
  line/col tracking (`json5.py`), deterministic md5 ID + content_hash
  helpers (`ids.py`), and a canonical JSON5 emitter with sorted keys
  and 1-decimal floats (`canonical.py`). Used by both generator and
  validator.

### Changed — validator rewrite

- **`scripts/validate_quests.py`** — replaced the 134-line regex
  stripper with a structured `Lexer → Parser → Validator → Reporter →
  Fixer` pipeline. Every diagnostic now carries `file:line:col`,
  severity, code, and an optional fix hint.
- **18 diagnostic codes** (`E_PARSE` through `E_MANIFEST_DUP_ID`) —
  replaces the previous boolean output. See reference §15.
- **Fuzzy ID hints** — when a dependency target is missing, the
  validator suggests the closest known ID via `difflib`.
- **`--json`** flag — machine-readable diagnostics for CI integration.
- **`--fix`** flag — autofixes `E_ITEM_BARE_STRING`, `E_TYPE_SUFFIX`,
  and `E_FILENAME_MISMATCH` in place.
- **`--strict`** flag — promotes warnings to non-zero exit.
- **`--manifest`** flag — adds manifest consistency checks
  (`E_MANIFEST_HASH_MISMATCH`, `E_MANIFEST_DANGLING`,
  `E_MANIFEST_DUP_ID`).
- **Bug fixed** — the old regex `re.sub(r'//.*', '', ...)` would eat
  `//` inside string literals, silently corrupting URLs and paths. The
  new tokenizer is string-aware.
- **Bug fixed** — old validator emitted spurious
  `E_LANG_MISSING_TITLE` warnings on tasks and rewards. Modern FTB
  Quests doesn't render those titles, so the warning is now restricted
  to chapters and quests.

### Changed — workflow

- **SKILL.md restructured** — new Step 1.5 (extract mod metadata),
  Step 4 split into 4a (LLM authors spec + lang) and 4b (run generator),
  Step 5 updated with new validator flags.
- **Reference doc** — added §13 (spec format), §14 (manifest format),
  §15 (validator diagnostics catalog).

### Changed — interview (grill-me integration)

- **Step 2 reframed as a relentless grilling** — the interview now walks
  each branch of the design tree and resolves dependencies between
  decisions one-by-one (theme → mods → structure → rewards), asks one
  question at a time with a recommended answer, and answers anything
  the indexed project / mod cache already settles by exploring the
  codebase instead of asking. Absorbs the `grill-me` skill's
  interviewing approach so `ftb-quests` is self-contained.
- **Balance review** — now explicitly continues the same relentless,
  branch-by-branch grilling against the generated config, re-reading
  quest files before asking.

### Added — context & memory (codegraph-context integration)

- **Step 0 — Load context & memory (optional)** — when the CodeGraph /
  Memory toolchain is installed, loads prior-session memory for the
  modpack and pre-fills the Step 2 interview with remembered decisions;
  otherwise degrades gracefully to Step 1 indexing + validator
  dependency analysis. Absorbs the `codegraph-context` skill's
  "load the brain before working" approach so `ftb-quests` stays
  portable and self-contained.
- **Step 6 — Remember the decisions (optional)** — captures theme,
  reward philosophy, gating, and renames to memory after generation
  when the toolchain is present; nothing depends on it otherwise.
- **Impact analysis** — the "never edit blind" discipline is applied
  via the manifest + validator (`E_DEP_MISSING` / `E_DEP_CYCLE` /
  fuzzy hints) before any modification of an existing pack.

### Added — match the user's language

- **Conversational language follows the user** — the interview,
  recommendations, balance review, Step 5 summary, and error
  explanations are conducted in the user's language (Chinese in,
  Chinese out; English in, English out), switching when the user
  switches. The language of the *generated* quest text remains
  governed by the `locales` settled in the Step 2 interview, kept
  independent of the chat language.

### Changed — deeper codegraph-context integration

- **`activeSkills` on `memory_load`** — Step 0 now passes
  `activeSkills: ["ftb-quests"]` so recall is biased toward memories
  this skill wrote (theme, reward philosophy, gating, renames).
- **Cortex confirmation printout** — Step 0 prints a structured summary
  (codegraph stats, memories loaded + top confidence, recent sessions,
  index date) so the user can see what context was loaded; omits any
  line whose source is unavailable.
- **`codegraph_impact` for blast radius** — the "never edit blind"
  discipline now also runs `codegraph_impact` on target quest files
  when the toolchain is present, complementing the manifest + validator
  with graph-level cross-file references.
- **Re-analyze triggers** — Step 0 lists when to re-run `analyze`
  mid-session (mods/ set changed, quest files renamed/added/deleted,
  contradictory impact results, structural spec refactor), with the
  small-edit carve-out (single title/task-count tweak needs none).
- **Integration section expanded** — documents the full coverage
  (session registration, freshness, memory + history, impact,
  confirmation, end-of-session decay) and the deliberate skip of the
  5-layer `load_project_context.sh` briefing (modpacks are jars +
  configs, so the code graph is low-value).

### Added — task linkage to existing pack quests

- **`scripts/index_quests.py`** — indexes a modpack's existing FTB
  Quests (hand-written, other tools, community books) into
  `.ftbq-cache/existing_quests.json5`: per-quest 16-hex `id`, chapter,
  title (resolved from `lang/`), shape, dependencies, task/reward
  types, and referenced mod namespaces. Modern JSON5 parsed with the
  string-aware parser; legacy `.snbt` gets a best-effort pass marked
  `format: snbt`. The CodeGraph "analyze → index → query" approach
  applied to quest files.
- **Step 1.7 — Index existing pack quests** — runs the indexer before
  the interview so generated content can link to the pack's existing
  quest landscape instead of landing as an abrupt, disconnected chunk.
- **Step 2 "Linkage" branch** — grills the user one question at a time
  (codebase-first: shows what the index found) about gating after,
  rewarding from, branching off, or avoiding duplication of existing
  quests.
- **`depends_on` accepts raw 16-hex IDs** — a token that is exactly 16
  hex chars references an existing (non-skill) quest and is passed
  through to `dependencies` verbatim, uppercased, instead of being
  resolved against the skill-owned name index. Lets new quests depend
  on pack content the skill did not generate without re-owning its ID.
- **`tests/test_linkage.py`** — 10 tests: hex-passthrough (mixed/lowercase/
  15- and 17-char rejection), the `_is_external_hex_id` helper,
  end-to-end generation with a mixed dep, and the indexer (lang titles,
  missing dir, dedupe). Suite now 121 tests, all green.

### Changed — scoped dev testing

- **Don't run the full suite on every iteration** — CONTRIBUTING.md now
  documents a "change what you touched" testing policy with a Test →
  source map (e.g. `ftbq/json5.py` → `test_json5_parser.py`,
  `scripts/index_quests.py` → the `test_indexer_*` cases in
  `test_linkage.py`). Targeted module runs keep feedback under a second.
- **Full suite reserved for** pre-push / pre-release, shared-surface
  changes (JSON5 parser, canonical emitter, `generate()` signature,
  `conftest.py`), and CI (which already runs `pytest tests/ -v`).
- **SKILL.md Step 5** carries a "scope it" pointer to the map;
  READMEs now state the 121-test count with the scoped-run note.

### Tests

- 111 unit tests across 8 files: `test_json5_parser`, `test_canonical`,
  `test_ids`, `test_extract_mods`, `test_id_stability`, `test_layout`,
  `test_incremental`, `test_validator`. All green.
- CI workflow (`.github/workflows/validate.yml`) replaces the broken
  `pyjson5`-based check with `pytest` across Python 3.11 / 3.12 / 3.13
  plus CLI smoke tests.

## [1.0.0] - 2026-06-19

### Added

- Initial release of FTB Quests skill
- SKILL.md with complete workflow protocol
- Reference documentation (`reference/ftb-quests-reference.md`)
- Support for modern JSON5 format (MC 26.1.x)
- Legacy SNBT format detection and generation
- Smart format detection from existing quest files
- Interview-driven quest generation workflow
- Complete task and reward type reference
- Full worked example with English and Chinese localization
- MIT License

### Format Support

- Modern JSON5 (FTB Quests 2025+, MC 26.1.x)
- Legacy SNBT (older modpacks, <=1.20 / early-1.21)
- Auto-detection based on existing files

### Features

- Chapter and quest generation with deterministic IDs
- Localization file generation (en_us, zh_cn)
- Dependency chain wiring
- Item task/reward object formatting
- Adaptive interview depth based on user preference
- Integration guidance for KubeJS, JEI/REI/EMI

[Unreleased]: https://github.com/IoIqq/ftb-quests-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/IoIqq/ftb-quests-skills/releases/tag/v1.0.0