# Cycle 8 Phase 1 Findings — Detailed Pack Analysis Notes

Date: 2026-07-09
Packs researched: 6 new (39 total)
Quests analyzed: ~1,289 across 6 packs

## TerraFirmaGreg Modern (TFG-Modern)

**Most significant finding: COMPLETELY ZERO rewards across all sampled chapters (601 quests).**

This is unprecedented in the 39-pack dataset. Even packs previously noted for low rewards (Cabricality, Blessed-Or-Cursed) have SOME rewards in certain chapters. TFG Modern has literally nothing — no XP, no items, no command, no loot, no random, no choice, no ftbmoney. The quest book is a pure progress tracker.

Design philosophy interpretation: In TFC+GregTech, the progression IS the reward. Unlocking Steam Age after Stone Age is motivation enough. The 437-star popularity suggests players accept this philosophy.

**Heart shape = food semantic:**
- Stone Age: 13 heart shapes (food/cooking quests)
- Steam Age: 20 heart shapes
- LV: 26 heart shapes
- Total: 59 heart shapes across 3 chapters
- MI:Foundation uses heart for food too (1-2 per chapter) but at much lower scale
- This validates heart = food/cooking as a cross-pack shape semantic

**dependency_requirement: "one_completed" usage:**
- 44 occurrences across Stone Age (14), Steam Age (9), LV (21)
- This is the highest one_completed density observed
- Means: within each chapter, many quests have branching paths (choose 1 of N options to advance)
- Combined with linear progression_mode: the pack is linear BETWEEN chapters but flexible WITHIN chapters

**pause_game: true:**
- Only pack in dataset with this setting
- Pauses single-player when quest UI is open
- Significant for TFC packs where mobs can kill you while reading quests
- TFG Modern is the only pack that considers this a safety feature

## ATM-7

**Completes the ATM series: ATM-6 (1.16.5) → ATM-7 (1.18.2) → ATM-8 (1.19.2) → ATM-9 (1.20.1) → ATM-10 (1.21)**

**Mekanism chapter diamond anomaly:**
- 43 diamond shapes in Mekanism chapter
- ATM-6/8/9/10 use hexagon as primary shape across all chapters
- ATM-7 Mekanism uses diamond instead — possibly a different quest designer or Mekanism-specific tier marking
- This is the first ATM chapter where diamond > hexagon

**Kill ladder confirmed across 5 ATM generations:**
- ATM-6: 5→10→50→100
- ATM-7: 5→10→25→50→100 (same pattern)
- ATM-8/9/10: same pattern
- 5 generations, consistent escalation

**Create chapter extreme density:**
- 4 quests, 63 item tasks = 15.75 items/quest
- This is incomplete/unusual — most ATM Create chapters have 30-60 quests
- May indicate the chapter was still under development when the repo was last updated

## RAD2 (Roguelike Adventures and Dungeons 2)

**Pathfinder chapter — Advancement-Catalog design:**
- 49 quests, 44 advancement tasks (89.8%)
- 45 choice rewards + 45 table_ids (every quest has a choice reward from a table)
- 64 XP + 44 XP_levels rewards
- Design pattern: "Complete this achievement → choose your reward"
- First chapter in dataset where advancement is the PRIMARY task type

**dependency_requirement: "one_started" — first in dataset:**
- Found in Features & Mechanics chapter
- "one_started" means the dependency only needs to be IN-PROGRESS, not completed
- Use case: "Start any exploration path, then come back to read the mechanics guide"
- Distinct from "one_completed" (requires full completion)

**ftbmoney economy:**
- 207 ftbmoney:money rewards across 4 chapters
- Primary reward currency alongside choice rewards
- Consistent with adventure/RPG packs using currency economies (NFwC, ModularTech)

## Society: Sunlit Valley

**Farming/cottagecore pack — completely unique type in dataset:**
- Stardew Valley-inspired
- 30 chapters covering: crops, fishing, villagers, building, transportation, etc.
- progression_mode: linear (even for a lifestyle pack)

**Collection-Catalog chapters:**
- Fishing: 3 quests, 80 item tasks = 26.7 items/quest
- Crops: 23 quests, 92 item tasks = 4.0 items/quest
- Design: submit every fish type / every crop type as collection milestones
- shape: "none" dominant (171/171) — intentional lack of visual categorization

**stat task type — first in dataset:**
- Used in Crops and Fishing chapters
- Tracks player statistics (e.g., total fish caught, crops harvested)
- Provides an alternative to item submission for collection-type progression

## All-of-Fabric-5

**AoF lineage: AoF3 (1.16.5) → AoF5 (1.19.2) → Craftoria (1.21.1)**

**Spectrum chapter — advancement-heavy magic:**
- 18 quests, 64 advancement tasks (!), 63 item tasks
- Advancement is the DOMINANT task type (more than item!)
- 10 command rewards for spell/ritual setup
- 13 hide_dependency_lines (72%)
- This is unusual: a magic mod chapter using vanilla/mod advancements as primary gates

**MI chapter — zero rewards:**
- 87 quests, 229 item tasks, ZERO rewards of any type
- Consistent with TFG Modern's zero-reward design for tech chapters
- Suggests TeamAOF's approach: tech chapters are self-rewarding (you get machines)

## Create-Skyline

**Insufficient data:**
- Only 3 chapters, 2 of which are empty (199 bytes = just the chapter header)
- Chapter 6: 14 quests, minimal data
- progression_mode: linear, default_quest_shape: circle
- May be an incomplete/early-stage pack

## Summary of New Micro-Patterns

| Pattern | Description | Source | Validation Status |
|---|---|---|---|
| MP39 Advancement-Catalog | Chapter with 60%+ advancement tasks + choice rewards from tables | RAD2 Pathfinder | **Validated** (Cycle 9: RAD2 twilight_forest/nether_exploration, Skylore captain, AoF5 Spectrum) |
| MP40 Collection-Catalog | Extreme item density (4+/quest) for collection themes, shape:none | SSV Fishing/Crops | **Validated** (Cycle 9: SSV building_shop 372 items, Skylore chef 220 items, CTX2 fishing 33 items) |
| MP41 Zero-Reward Design | ALL quests across ALL chapters have zero rewards | TFG Modern | **Validated** (Cycle 9: TFG Vintage 1086q, Cobblemon 1307q — 3 sources total, not expert-only) |
| MP42 Stat Task Collection | type: "stat" for tracking player statistics as quest gates | SSV Crops/Fishing | **Validated** (Cycle 9: SSV pantry + relics — 4 stat tasks total, still SSV-specific) |

## Assumptions Challenged

1. "Expert packs have near-zero optionality" → TFG Modern has 12-22% optional (expert with choice)
2. "Command rewards are expert-only" → AoF5 (kitchen-sink) uses 11 commands in magic chapters
3. "shape: none means no shape semantic" → SSV uses shape:none as INTENTIONAL cottagecore design
4. "Game Stages are expert-only" → Skylore (skyblock, non-expert) uses `type: "gamestage"` (Cycle 9)
5. "Zero-reward is TFG-specific" → Cobblemon (1307q, non-expert, non-TFG) also zero-reward (Cycle 9)
6. "consume_items: false = dual-task automation (MP35)" → Cobblemon uses 29 consume_false as "showcase" without dual-task pattern (Cycle 9)

## Three Hard Problems (PP) Assessment

- **PP1 Item Cross-Tier**: Not observed in Cycle 8 packs. TFG Modern's linear progression makes cross-tier unlikely.
- **PP2 Sequence Inversion**: Not observed. All packs have clear teach-before-do ordering.
- **PP3 Reward Disconnection**: N/A for TFG Modern (zero rewards). RAD2 ftbmoney economy avoids disconnection by using universal currency.
