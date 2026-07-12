# Draft: Reward Evolution Lineage — Feature Migration Pattern

> **Status:** DRAFT — conceptual pattern derived from cross-generational comparison. Not a single pack's pattern but an ecosystem-level observation.
> **Date:** 2026-07-08
> **Sources:** EnigmaticaModpacks/Enigmatica6, RCqaq/E9E, EnigmaticaModpacks/E10, TeamAOF/AoF3, TeamAOF/Craftoria

## Concept

When a mod (FTB Quests) adds native support for a feature that pack authors previously implemented via workarounds, the workaround pattern becomes deprecated. Tracking this evolution across pack generations reveals **design lineages** — consistent design philosophies that persist even as implementation methods change.

## Lineage 1: Enigmatica Command Reward Evolution

| Generation | Pack | MC Version | Command Rewards | Primary Use | Why |
|---|---|---|---|---|---|
| Gen 1 | E6 | 1.16.5 | 455 | `/execute at @p run loot spawn ~ ~1 ~ loot enigmatica:chests/quest_*` | FTB Quests lacked native weighted loot pools |
| Gen 2 | E9E | 1.19.2 | 56 (ch1 only) | `/gamestage add {p} <stage>` | Gamestage-based progression became primary |
| Gen 3 | E10 | 1.21 | 0 | `type: "loot"` (28 reward tables) | FTB Quests now natively supports weighted loot |

### Gen 1 Detail (E6 — MC 1.16.5)
- ALL 455 command rewards use `player_command: false` (server-side execution)
- Pattern: `/execute at @p run loot spawn ~ ~1 ~ loot enigmatica:chests/quest_*`
- Tiered loot: `quest_*_loot_rare`, `quest_*_loot_epic`, `quest_*_loot_legendary`
- Cross-chapter "delight" tables: `quest_scavengers_delight`, `quest_farmers_delight`, `quest_alchemists_delight`
- Per-chapter distribution: Botania (94), Create (10), Getting Started (2)
- This is vanilla loot table delivery disguised as command rewards — a creative workaround

### Gen 2 Detail (E9E — MC 1.19.2)
- 56 command rewards in `chapter_one` alone (83% of reward sections)
- Shifted from loot delivery to gamestage routing
- Uses `command` rewards with `{p}` placeholder for gamestage grants
- The invisible infrastructure chapter manages stage routing; visible chapters stay clean

### Gen 3 Detail (E10 — MC 1.21)
- 0 command rewards across all chapters
- 28 native reward tables in `config/ftbquests/quests/reward_tables/`
- `type: "loot"` with `table_id: <long>L` referencing FTB Quests internal tables
- The workaround is completely replaced by native functionality

## Lineage 2: TeamAOF Reward Table Evolution

| Generation | Pack | MC Version | Reward Tables | Dominant Type | Philosophy |
|---|---|---|---|---|---|
| Gen 1 | AoF3 | 1.16.5 (Fabric) | 16 | `random` (363) + `loot` (23) + `choice` (16) | "Loot crate pack" — massive random pools |
| Gen 2 | Craftoria | 1.21.1 (NeoForge) | 19 | `random` (21-92% per chapter) | Structured, chapter-specific tables |

### Gen 1 Detail (AoF3)
- 16 reward tables with evocative names: `low`, `medium`, `high`, `artifacts`, `foodsources`, `foodoringots`, `pristine_matter`, `slime`, `color_modules`, `dyes`, `endadv`, `essence`, `explorerer`, `genrewards`, `hats`
- Format: `item: "mod:id", weight: N` — simpler than Craftoria/E10 nested object format
- `loot_size: 6` (low) to `loot_size: 16` (high) — large roll counts
- Mixed XP within item pools: `{ xp: 1000, type: "xp", weight: 2 }` alongside item entries
- `hide_tooltip: true` on all tables
- Artifacts table uses NBT data (`cardinal_components`) for trinket configuration
- 363 random rewards across ~615 quests = 59% of all rewards are random

### Gen 2 Detail (Craftoria)
- 19 reward tables, more structured and chapter-specific
- Format: `item: { count: 1, id: "mod:id" }, count: N` — nested object format
- `loot_size: 1` — single roll per claim (more targeted rewards)
- Create chapter: 92.6% random rewards (100 random out of 108 total)
- Zero mixed XP in item pools — XP rewards are separate
- More conservative overall: fewer but more focused reward tables

### Design Philosophy Persistence
Despite implementation changes, both TeamAOF packs share a consistent design philosophy: **randomized reward delivery as the dominant reward type**. This "loot crate" approach distinguishes TeamAOF from other kitchen-sink teams (ATM uses XP drip, Enigmatica evolved from command-as-loot to native loot).

## Implications for Skill Development

1. **Version-aware reward generation:** When generating for MC ≤1.16.5 packs, consider that native FTB Quests loot tables may not be available. The `/execute at @p run loot spawn` pattern is a valid fallback but should be flagged as legacy.

2. **Team detection:** If generating for a TeamAOF pack, prefer `random`-dominant reward economy with chapter-specific reward tables (following AoF3→Craftoria lineage).

3. **Deprecation awareness:** MP29 command rewards for loot delivery should be flagged as legacy on FTB Quests 26.x+. The R28 safety scan should not flag `/execute at @p run loot spawn` as a FORBIDDEN command (it's a legitimate loot delivery pattern on older versions), but should flag it as a WARNING on newer versions with a suggestion to use `type: "loot"` instead.

4. **Lineage as a design signal:** A pack team's design philosophy persists across generations even when implementation changes. Tracking lineages helps predict what patterns a new pack from the same team will use.
