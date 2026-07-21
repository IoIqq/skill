# FTB Quests Toolchain Reference

All scripts live in `scripts/`. Run from the skill root or with the skill on PYTHONPATH. Every script supports `--help`.

## Cache builders (Step 1)

Run once per pack, re-run whenever the source changes (new/removed jars, quest edits).

```bash
python scripts/extract_mods.py <packroot>      # -> .ftbq-cache/mods.json5 (modid/name/version/side/loader per jar)
python scripts/extract_items.py <packroot>     # -> .ftbq-cache/items.json5 (all_item_ids from mod lang files)
                                               # -> .ftbq-cache/item_names.json5 (name→id index, en_us + zh_cn)
python scripts/index_quests.py <packroot>      # -> .ftbq-cache/existing_quests.json5 (id/chapter/shape/deps/task+reward
                                               #     types per quest + top-level known_item_ids)
```

- `extract_items.py` is best-effort: not every registered item has a lang key. Treat `all_item_ids` as a candidate set, not a complete registry.
- `index_quests.py` parses modern JSON5 with the string-aware parser; legacy `.snbt` gets a best-effort pass marked `format: snbt` (lower detail). Its top-level `known_item_ids` lists every item id referenced by existing quests (verified-loaded in this pack).

## Orientation

```bash
python scripts/pack_briefing.py <packroot>
```
Prints a compact summary (format, mod count + names, chapters + per-chapter quest count, task/reward type frequencies, audit verdict) curated from `.ftbq-cache/`. **Do not read `mods.json5` / `existing_quests.json5` / chapter files raw for orientation.** A missing cache is flagged with the builder to run.

## Batch item-id lookup

When a node needs many item ids at once (collection quest, reward table, recipe catalog), resolve all names in ONE call:

```bash
python scripts/lookup_item.py <packroot> 铁锭 橡木原木 木棍        # names → ids, one pass
python scripts/lookup_item.py <packroot> "Copper Ingot" --partial  # surface every mod's copper
python scripts/lookup_item.py <packroot> --reverse minecraft:iron_ingot   # id → known names
```

The index merges en_us (universal) + zh_cn (where shipped) from each mod jar's lang values, plus user-verified Chinese names harvested by `audit_index.py` from existing quest descriptions (`&e<id><中文名>&r`). Built once in Step 1, persisted; rebuild only when mods change.

**Ambiguity is surfaced, not guessed.** Many mods ship the same display name (e.g. "Copper Ingot" in minecraft / create / immersiveengineering); the tool prints every candidate id with its mod prefix — pick by the chapter's mod, or ask the user. Never silently pick one. If a name isn't in the index, it returns `NOT FOUND` + suggestions — ask the user to confirm in JEI/EMI.

## Generator

```bash
python scripts/generate_quests.py <output_dir>                  # default: overwrite skill-owned, preserve user-added
python scripts/generate_quests.py <output_dir> --mode preserve  # keep ALL on-disk edits (content_hash protection)
python scripts/generate_quests.py <output_dir> --mode ask       # prompt per conflict
python scripts/generate_quests.py <output_dir> --adopt          # first run on an existing pack
python scripts/generate_quests.py <output_dir> --dry-run        # preview without writing
python scripts/generate_quests.py <output_dir> --spec <path>    # use a specific spec file
```

Behavior:
- Reads `quests.spec.json5` at `<output_dir>` root (never deployed).
- Writes a clean `<output_dir>/quests/` tree: `data.*`, `chapters/*.json5`, `lang/*/quests.json5`, `.ftbq-cache/manifest.json5`.
- Same spec → byte-identical output. Lang is add-only after first run (existing rewritten keys are never overwritten).
- With `format: "snbt"` the output is `.snbt` with no `lang/` (text inline) — reference §12.
- IDs are computed from quest names (reference §9); uniqueness is checked pre-emit, so a name clash fails fast before any file is written.
- Incremental merge: content_hash match → no-op; only the quest you touched is re-emitted. In-game position edits to other quests are preserved regardless of mode.
- `@<chapter>/<quest>.subkey` lang placeholders (subkeys: `title`, `quest_subtitle`, `quest_desc`, `chapter_subtitle`) are rewritten to `quest.<HEX>.subkey` on generate.

**Before `--mode ask` / `--adopt` on an existing pack**, check blast radius first: the manifest + validator catch quest dependency chains; if CodeGraph is available, also run `codegraph_impact` on the target quest files. Either source finding affected quests the other missed is a signal to stop and confirm with the user.

## Validator

```bash
python scripts/validate_quests.py <output_dir>/quests/
python scripts/validate_quests.py <output_dir>/quests/ --strict   # stricter thresholds
python scripts/validate_quests.py <output_dir>/quests/ --fix      # autofix what's safe
python scripts/validate_quests.py <output_dir>/quests/ --json     # machine-readable (CI)
```
Diagnostics carry `file:line:col`. Full catalog: reference §15. Runs the R1–R32 pipeline + topology rules R55–R64.

## Single-quest inspector

```bash
python scripts/quest_detail.py <output_dir> <chapter>/<quest>
```
Resolves the quest by name (via the spec's pack + the id formula) and prints only that quest's id/shape/deps/tasks/rewards/lang. Token-saving vs. reading the whole chapter file.

## Deploy (Step 5b)

```bash
python scripts/generate_quests.py <output_dir> --deploy <packroot> --spec <output_dir>/quests.spec.json5  # preview (writes nothing)
python scripts/generate_quests.py <output_dir> --deploy <packroot> --yes                                   # apply
python scripts/generate_quests.py <output_dir> --deploy <packroot> --yes --quests-dir <custom_dir>         # custom target
python scripts/generate_quests.py <output_dir> --deploy <packroot> --yes --no-backup                       # DANGEROUS, irreversible
```

What `--deploy` does (full table: reference §16):
- **NEW** files → copied verbatim (names unchanged).
- **`data.json5` / `chapter_groups.json5` / lang** → **merged** so skill content and pack content coexist. The pack's other-quest lang keys are preserved.
- **`chapters/<name>.json5`** that already exists → **backed up** then replaced wholesale. Original lands at `<target>/.ftbq-backup/<ts>/chapters/<name>.json5`.
- **`.ftbq-cache/manifest.json5`** → backed up + replaced.

The ⚠️ OVERWRITE block in the report highlights every file that touches a modpack original — review before adding `--yes`. Backups live under `<target>/.ftbq-backup/<timestamp>/` (dot-prefixed so FTB's scanner skips it), with a `BACKUP_INDEX.json5`. To roll back, restore from that folder.

Need **quest-level** merge (keep an individual pack quest inside a skill-owned chapter)? Use `--adopt` / `--mode ask` pointed at the pack's quests folder directly — the manifest then distinguishes skill-owned vs user-added quests quest-by-quest. `--deploy` is intentionally file-level.

## Audit (DLC vs installed)

```bash
python scripts/audit_diff.py <dlc_pack>          # auto-resumes from cached audit_report.json5 when fresh
python scripts/audit_index.py <packroot>         # builds .ftbq-cache/audit_index.json5
```
For comparing a DLC source pack against an installed pack (diff/audit, not generation). Full workflow: `reference/audit-workflow.md`.

## ID utilities

```bash
python scripts/hash_id.py <quest_name>           # compute the 16-hex id for a quest name (top-bit masked)
python scripts/scan_ids.py <packroot>            # scan a pack for id collisions / top-bit violations
```

## Dev testing

When changing skill code (scripts/, ftbq/), run only the test module(s) covering what you touched — see the "Test → source map" in `CONTRIBUTING.md`. Reserve the full suite for pre-push / pre-release / shared-surface changes (JSON5 parser, canonical emitter, `generate()` signature).
