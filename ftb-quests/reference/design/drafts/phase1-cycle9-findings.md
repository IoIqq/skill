# Phase 1 Cycle 9 — Detailed Pack Analysis Notes

> Date: 2026-07-09
> Packs researched: 7 new (46 total)
> Additional sampling: RAD2 (2 chapters), SSV (5 chapters)

## Raw quantification data

### TFG Vintage (TerraFirmaGreg-Team/Modpack-Vintage)

- Format: individual quest files in hash-based directories (same as TFG Modern)
- 13 chapters, 1086 total quests
- Chapter distribution: Primitive(239), Steam(63), LV(89), MV(55), HV(53), EV(51), IV(35), LuV(38), ZPM(11), UV(7), Space(116), AE2(155), DevTable(174)
- default_quest_shape: "circle" (all except DevTable: "hexagon")
- Primitive sampled quests: all item tasks with ForgeCaps NBT (TFC heat system: `tfc:item_heat` with ticks/heat), itemfilters:filter with Parent NBT
- dependency_requirement: "one_completed" observed in Primitive chapter
- Rewards: ZERO across all sampled quests (5 Primitive + 5 other)
- Full i18n: all titles use `{tfg.quests.*.era.title}` pattern

### CTX2 Resolution (mahjerion/Craft-to-Exile-2-Resolution)

- 13 chapters: act_i(219q), act_ii(59q), technology(14q), fishing(67q), foodstuffs(57q), colonization(79q), act_iii, act_iv, act_v, act_vi, christmas, storage, transportation
- 6 chapters sampled: 495 quests
- Task distribution: item(177), kill(42), gamestage-in-text(0 actual tasks)
- Reward distribution: command(47), random(7), choice(7), table_id(14)
- Shapes: square(4), heart(2), hexagon(1) — mostly default
- 8 reward_tables: rare_tier_1_armor_gear_bag, rare_tier_1_jewelry_gear_bag, rare_tier_2_gear_bag, soul_gear_bag, soul_gear_bag_ii, weapon_gear_bag, weapon_gear_bag_ii, wooden_planks
- Act I kill density: 26 kills / 219 quests = 11.9% (highest since CTX1 Dissonance prelude: 15 kills / 36 quests = 41.7%)
- ZERO optionality, ZERO consume_false, ZERO hide_dependency_lines

### Skylore (TeamAOF/skylore)

- 16 chapters total
- 5 chapters sampled: 888 quests
- Chapter themes: profession-based (Engineer, Chef, Captain, Doctor, etc.)
- Chef: 381 quests, 220 items = Collection-Catalog (0.58 items/quest)
- Captain: 140 quests, 7 advancement tasks
- Engineer: 152 quests, gamestage task (type: "gamestage", auto: "invisible", stage: "")
- Primary Orders: 194 quests, pentagon(3)+octagon(2)+hexagon(2)+diamond(1)
- Total rewards: command(48), xp(45), loot(49), choice(18), table_id(76)
- 60+ reward_tables
- dependency_requirement: one_completed (1 in primary_orders)

### Fear-Nightfall (LunaPixelStudios/Fear-Nightfall)

- 9 chapters: tutorial + 8 numbered/extended
- 5 chapters sampled: 299 quests
- Task types: item(168), checkmark(9), kill(1), dimension(1)
- Shapes: diamond(30), hexagon(18), square(9), octagon(4), circle(4), pentagon(1), rsquare(1) = 7 types
- Per-chapter shape dominance: ch_v diamond(16), ch_iii diamond(6)+square(5), ch_1 hexagon(6)+octagon(4)
- Rewards: 58 item-type sections. ZERO command/xp/random/loot/choice
- Custom icon: ftbquests:custom_icon with teraphobia:textures/fear_nightfall/logo.png
- Tutorial shapes: circle(4), square(1), rsquare(1)

### Cobblemon (Noa3/FTB-Cobblemon-Quests)

- 5 chapters (all sampled): 1307 quests
- adventure(102), battling(305), catching(300), progression(334), utility(266)
- Task types: item(473), checkmark(9). ZERO advancement/kill/dimension
- Rewards: ZERO of ALL types
- Shapes: hexagon(36), circle(30). Adventure/battling = hexagon, catching/progression/utility = circle
- consume_items: false: progression(17), utility(12) = 29 total
- Full i18n lang file present

### All-of-Create (qwek1/All-of-Create)

- 21 chapters total
- 6 chapters sampled: 761 quests
- Create: 433 quests, gear(13)+circle(3)+square(1), xp(111)+random(55)+table_id(55)
- New Age: 127 quests, heart(1)+gear(1), xp(36)+random(11)+table_id(11), consume_false(1)
- Blaze Burner Fuels: 83 quests, loot(6)+random(7)+table_id(15)
- Deep Dark: 41 quests, loot(4)+random(5)+table_id(9)
- Enchantment Industry: 50 quests, loot(13)+random(5)+table_id(18)
- Welcome: 27 quests, dependency_requirement: one_completed(1)
- 3 reward_tables: create, ingots, xp
- ZERO command rewards

### Medieval-MC (LunaPixelStudios/Medieval-MC)

- 4 versions: Fabric 1.19.2, 1.20.1, 1.21, Forge 1.16.5
- Fabric 1.21 sampled: 6 chapters, 320 quests
- Task types: item(118), checkmark(6), kill(4), dimension(1), observation(5)
- Rewards: choice(1)+table_id(1)+xp(1) = near-zero
- Shapes: circle(4), diamond(1)
- default_quest_shape: "" (all empty except oddities: "circle")
- hide_dependency_lines: 7
- Multi-version architecture: same chapter structure adapted per version

## RAD2 additional sampling

- twilight_forest: 552 quests, 183 item + 3 kill + 6 advancement + 1 dimension + 2 observation
  - Rewards: xp(15), choice(11), table_id(12), ftbmoney(19)
  - Shapes: square(1), hexagon(1)
- nether_exploration: 494 quests, 216 item + 1 kill + 1 checkmark + 2 advancement + 4 observation + 1 structure
  - Rewards: xp(13), choice(4), table_id(5), ftbmoney(31)
  - Shapes: octagon(4), rsquare(1), hexagon(1), diamond(1), circle(1)

## SSV additional sampling

- building_shop: 629 quests, 372 items
- pantry: 47 quests, 26 items, stat(1), shape:"none"(6)
- relics: 83 quests, 28 items, stat(1), octagon(1)
- villagers: 61 quests, 16 items, checkmark(6)
- welcome: 35 quests, 5 items, checkmark(11), command(5)
