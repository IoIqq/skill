# FTB Quests — Design Guide (on-demand)

Strategic input to the interview and authoring loop. **Load the section you need, when you need it** — this file is not loaded automatically:

- **Before Step 2 (interview)** → `§principles` (the thinking) + the spine models that stay inline in SKILL.md.
- **Before Step 4 (per-node authoring)** → `§writing-style`.
- **When assigning x/y (Step 3 skeleton / layout)** → `§layout-reasoning` + `§atm-layout-patterns` (7 templates covering kitchen-sink, expert, and RPG layouts).
- **For cross-mod quest design** → `§synergy-patterns`.
- **For empirical grounding / "what do shipped packs actually do?"** → `§field-findings`.
- **For genre-specific patterns** (expert gating, skyblock, magic, RPG, Create) → `§pack-type-patterns`.
- **For quest-level micro-patterns** (task combos, dependency topologies, reward bridges, stage markers) → modular reference files (see `module-index.md` for routing).

The capstone model referenced throughout is **in-chapter + item-task-gated** (see `§principles` F1/F2) — stated once there, not re-explained at every mention below.

---

## §principles — Foundational thinking (distilled from a deep ATM10 audit)

This gives the *thinking* behind the rules in SKILL.md — abstracted from a full-file ATM10 audit (2026-06-30; figures + provenance in the ATM10 deep-dive below) so you can apply ATM10's design logic to **any** pack, not just ATM. It refines every capstone mention in SKILL.md: the audited model is **in-chapter + item-task-gated**, not cross-chapter-dependency-gated (F1/F2 below).

### Foundational model

- **F1 — Guidance and gating are two mechanisms; decouple them.** A quest book does two jobs: *guide* (tell the player the next step) and *gate* (block them until ready). They don't have to live in the same place. ATM10's dependency graph is permissive (book-wide `flexible`; the capstone chapter has **zero** cross-chapter deps) — it's a *guide*. The actual *gate* is the capstone components' **item tasks** (each requires items from a different mod). Decide per-pack: does my dependency graph guide, gate, or both? Don't force one graph to do both — it makes the pack narrow and rigid.
- **F2 — In a kitchen-sink, convergence lives in the crafting chain, not the dependency graph.** ATM10 does NOT wire every mod chapter into the Star via `depends_on`. It drops the entire component tree into one self-contained capstone chapter; "you must touch every mod" is enforced by *what the components are made of* (items from 20+ mod namespaces), not by quest wires. Want cross-mod breadth? Design the item economy to require it — don't engineer it with dependency edges.
- **F3 — The capstone is the pack's table of contents; design it first.** ATM10's Star has 13 components, each a different mod's endgame product. The endgame goal *is* the list of systems the player should have engaged. Work backwards: pick the systems → one signature product per system → those are your capstone components → each component's chapter exists to feed it.

### Reusable patterns (measured on ATM10, portable anywhere)

- **P1 — Chapter `default_quest_shape` = mod identity.** Create=`gear`, Mekanism=`hexagon`, AllTheModium=`diamond`, basic_armor=`rsquare`, silent_gear=`none`. Pick a stable shape↔temperament mapping (gear=machinery, hexagon=energy/hive, diamond=material/gear-equip, rsquare=armor/special) and assign one per chapter; don't rainbow. (~47% of ATM10 quests set an explicit shape vs ~3–8% in curated packs — kitchen-sinks are shape-rich by design.)
- **P2 — Tier-spine chapter layout** (measured on ATM10's `allthemodium`): root `gear size 2.0` at the left → horizontal spine along +x → each tier is a symmetric `rsquare(y=−1)` + `octagon(y=+1)` pair → `hexagon` teleport/cross-link nodes all point back to the root → converge at the rightmost x on the alloy/end tool (`size 2.0`). Reuse for any tiered-material or tiered-tech chapter.
- **P3 — Capstone node visual grammar** (measured on ATM10's Star): origin `(0,0)`, the chapter's **largest** shape (`pentagon size 5.0`), with components fanning **radially** as its dependents (each component a sub-tree of 6–9). The endgame node is the visual center and the biggest thing on the canvas — make "everything converges here" legible at a glance.
- **P4 — Generosity is density, not exotic types.** ATM10 has **no** `custom`/`command`/`all_table`/`gamestage` rewards — only `item`/`xp`/`random`/`xp_levels`/`loot`/`choice`, but at **1.5 rewards/quest (6,915 total)**. You don't need KubeJS to be generous; pile standard rewards. Exotic reward types are a *style* choice, not a generosity prerequisite.
- **P5 — Anti-clutter for permissive books: hide lines, don't hide quests.** ATM10: `hide_dependency_lines` ×438 > `hide_until_deps_visible` ×127, `optional` ×553, `secret` ×0. In a flexible/many-doors book, declutter by trimming dependency *lines* and tagging side content `optional` — rarely hide whole quests. Reserve `hide_until_deps_visible` (progressive reveal) for forced-linear narrative chapters. (Refines SKILL.md's layout "hide_until_deps_visible is #1" — that holds for *narrative* chapters; ATM10 shows the *catalog/kitchen-sink* inverse.)
- **P6 — ~90% of tasks are `item` — design around the item economy.** 5,190/5,792 ATM10 tasks are item (craft/obtain); kill/checkmark/structure/biome/advancement/dimension are seasoning. Center your design on the item chain (what's produced where, what feeds what, where automation closes the loop); reach for other task types only to teach a non-item mechanic.
- **P7 — The opener foreshadows the capstone.** ATM10's `welcome` chapter's first node is the ATM Star icon (`pentagon size 3.0`, "set foot in the overworld"). Day 1 shows the destination. Don't make Chapter 1 only "punch wood" — anchor an early visual pointer to the endgame so the player has a north star.

### The thinking, in order

1. Pick the capstone and the systems it must touch (F3) → one signature product per system → those are the components.
2. Decide where the gate lives: dependency locks, or item/recipe requirements? (F1/F2 — default to "quest graph guides, items gate" for kitchen-sinks.)
3. Middle is parallel pick-a-lane or forced main line? (kitchen-sink → parallel + `flexible`; tutorial/expert → linear + `default`.)
4. Separate the portable spine (capstone + tier spine) from the pack-type-specific opener (skyblock = sieve/hammer loop, survival = mining/exploration). Write the opener for the pack type; keep the spine constant.

### Four questions to answer before designing any pack

1. What is my single convergence point, and which systems must it touch?
2. Does cross-system gating live in `depends_on`, or in item/recipe requirements?
3. Is the middle parallel (pick-a-lane) or forced (linear)?
4. What's the portable spine vs. the pack-type-specific opener?

Answer those four, then apply P1–P7 for shape, layout, rewards, anti-clutter, and task mix.

---

## §synergy-patterns — Cross-mod quest design

A modpack is more than mods-in-a-folder — it's the *connections* between them. The best packs make cross-mod interaction the actual content. Design quests that teach and require those connections; don't just list each mod in isolation. (How to *represent* these in the spec stays inline in SKILL.md's "representing synergy in the spec".)

**Four patterns of mod synergy — build quests around them:**

1. **Cross-mod crafting chain.** Mod A's output is mod B's ingredient, several steps deep. ATM9 (real description, verbatim): Refined Storage's *Regulator Upgrade* keeps a machine stocked; pair it with a *Crafting Upgrade* + a *crafter* holding the recipe, fed by a *Mystical Agriculture* essence farm → "your system keeps the furnace fueled" automatically. The quest teaches the whole loop (farming mod → storage mod → autocrafting mod), not any one mod. **Make the task item the *end* of a cross-mod chain, and walk the chain in the description** — one quest per link if the chain is long.
2. **Cross-mod gating.** You need mod A's machine to make mod B's component (or mod A's material to mine mod B's ore). ATM: AllTheModium pick → Vibranium → Unobtainium — the *gate* is a different mod's tool. Represent it as a dependency: the Vibranium quest `depends_on` the AllTheModium-pick quest. This makes mod order *meaningful*, not arbitrary.
3. **Capstone synthesis.** One endgame item whose recipe pulls one component from each major mod — the mod index as an item. ATM10's ATM Star = 13 components (Dragon Soul, Pulsating Black Hole, Singularity, Wither's Compass, …) + 3 alloys via Powah / Ars Nouveau / Industrial Foregoing. The Star chapter is a **self-contained** tree (the capstone model of F1/F2: zero cross-chapter `depends_on`; cross-mod breadth is in each component's **item task**, not dep wires). **Use this when you want players to engage every system; skip it for a focused single-mod pack.**
4. **Deep integration (one core crafting system).** Instead of each mod doing its own thing, fold mods into one core mod's crafting. Create: Astral routes Tinkers' liquid metals through Create mixers, Tech Reborn through sequenced assembly, everything through mechanical crafting — "all content works together" because it's all *one* recipe space. The quests then teach *that shared system* (filling, sequenced assembly, mechanical crafting) once, and every mod chapter reuses it. **This needs KubeJS recipe scripting** (the pack's job); your quests just describe the unified process.

**Don't fake synergy the mods don't have.** If two mods don't actually interact (no shared recipe, no gating), don't manufacture a cross-mod quest — it'll task the player for something they can't do. Verify the interaction in JEI / EMI or the mods' configs before writing the quest (Step 4's "never guess" rule).

---

## §field-findings — Empirical evidence from shipped modpacks

Grounds the rules in SKILL.md with measured data from real packs. Two Create-series packs audited 2026-06-29 (full numbers in `reference/ftb-quests-reference.md` §20):

- **Create: Delight Remake** (1.20.1, Forge, FTB Quests 2001.4.17) — 41 chapters, 2,295 quests, SNBT **inline**. The large polished layout reference: `hide_until_deps_visible`×72, `hide_dependent_lines`×17, `secret`×12, rich branching (`one_started`×63, `one_completed`×44); `hexagon`/`gear` hubs `size 4.0`/`3.0` on origin, fans to `(x:4, y:-4)`; ~92% default `circle`. **Rich rewards** (`item`×803, `xp`×195, `custom`(KubeJS)×116, `random`×85, +xp_levels/choice/all_table/command/loot); diverse tasks (`item`×2185, +checkmark/kill/observation/advancement/dimension/stat/biome/structure).
- **Mechanomania** (1.21.1, NeoForge, FTB Quests 2101.1.21) — 18 chapters, 395 quests, SNBT **+ lang files** (a 1.21.1 pack — adopt-only, not a generation target). **Minimalist**: **zero** `hide_until_deps_visible`/`hide_dependent_lines`/`secret` (only viable — small chapters), near-linear deps (1 override), **sparse rewards** (`item`×40, `choice`×3 only); ~97% default `circle`; a few `diamond`×12/`gear`/`rsquare`×7 mark milestones; fractional-coord fans (`x:-4.25, y:-0.75`).

### Lessons that adjust SKILL.md's rules

1. **`hide_until_deps_visible` is mandatory above ~50 quests/chapter, optional below ~20.** Create: Delight uses it on ~3% of a 2.7k-quest book (concentrated in the big chapters); Mechanomania (470 quests, max chapter 84) uses none and reads cleanly *only* because its chapters are small. Recommend the flag on most branch/leaf quests once a chapter exceeds ~30–50 nodes; a small chapter can skip it.
2. **Reward philosophy is a pack-level decision, not a per-quest one.** Pick a lane up front: **rich** (xp + custom/KubeJS + random/loot tables + command toggles, like Create: Delight) or **sparse** (item-only, like Mechanomania). Mixing wildly per quest feels incoherent.
3. **`default_quest_shape: ""` (empty) at chapter level = inherit `data`'s default.** Both packs set the chapter field to `""` and let `data.default_quest_shape: "circle"` propagate; only 3–8% of quests override the shape. Mirror this: set the default once in `data`, leave chapters at `""`, and reserve explicit shapes for milestones.
4. **Hand-authored `dependencies` reference the parent by raw 16-hex ID** (`dependencies: ["55C42BCE0E399B3D"]`), not by name. The skill's `name`-based wiring is a generator convenience; when hand-editing or linking to existing packs, use the hex.
5. **Two advanced authoring features appear in real packs** (documented in reference §20): `{image:<path> width:.. height:.. align:center}` to embed images inside `description`, and JSON-text-component `subtitle` strings with `"clickEvent": {"action":"change_page","value":"<HEXID>"}` for clickable cross-quest navigation. Plus the in-text placeholder resolver `{item.modid:name}` / `{block.*}` / `{dimension.*}` / `{entity.*}` / `{effect.*}` that auto-renders localized Minecraft names — usable wherever text is allowed, in both lang-file and inline models.

### Culinary / recipe-catalog quest lines

Create: Delight Remake's **超级大厨** group (the only food-focused pack audited) is the richest source of food-line patterns. Four chapters, measured (full data in reference §20g):

- **Mouse_Chef (304)** — the recipe catalog: 12 category hubs (`rsquare size 4.0`) each capstone ~18 independent recipe cells (`size 2.0`, `item` "obtain this dish"); the hub `depends_on` ALL cells + `hide_dependency_lines: true` (the catalog's anti-clutter lever, vs. `hide_until_deps_visible` for narrative). Only 46/304 have deps; square aspect ~66×70; `item`×325/`checkmark`×11; sparse rewards (item×29, xp×52 — the dish is the reward).
- **Ingredient_Essence (98)** — minimal raw-ingredient grid (no shapes/icons/desc, 4 deps) at a remote offset (x −78..−65).
- **Feast_Afoot (88)** — the text-heavy tutorial: color-coded tier descriptions (`subtitle: "湿度有&e五级&r，为&4干旱&r、&6干燥&r、&a一般&r、&9湿润&r、&1潮湿"`), trivial `stat: play_time value 1`/`checkmark` "you read this" task + tool reward; 85/88 have deps (linear, opposite of catalogs).
- **Youkais_Homecoming (74)** — the one reward-rich food chapter (`random`×19, `all_table`×5, 29 reward-table refs).

**The food-line design pattern (distilled):**

1. **Separate "how it works" from "the recipes".** Mechanic tutorials go in one text-heavy *linear* chapter (Feast_Afoot pattern); recipe enumeration in a separate *catalog* chapter with **no description text** (icon + dish name is the content). Mixing a tutorial into 300 recipe cells is unreadable.
2. **Recipe catalog = capstone-hub grid, not a narrative spine.** Category hub (`rsquare size 4.0`) capstones N independent cells (`size 2.0`); hub `depends_on` ALL + `hide_dependency_lines: true` + `checkmark` + coin reward; cells have no deps among themselves; ~1:1 aspect.
3. **Food tasks are `item` "obtain", not "craft".** `only_from_crafting`/`consume_items` both zero across all four chapters — dishes can be cooked/traded/gifted. Reserve `only_from_crafting` for when the recipe *is* the lesson.
4. **Sparse rewards on cells; concentrate on hubs + explainers.** Mouse_Chef's 304 cells give only item×29 + xp×52; the *hubs* carry the coin. The dish is the cell's reward — don't loot-spam.
5. **Color-code tiers.** Assign each tier a stable color (`&4`/`&6`/`&a`/`&9`/`&1`); `&e<phrase>&r` for key terms, not item-id links (use `{item.modid:name}` for item names).
6. **Scatter big catalogs to remote coords.** A 300-quest catalog needs ~66×70 units; offset it (e.g. x −40..−78) to avoid collision.

### Kitchen-sink / ATM-series quest lines

The **All The Mods (ATM)** series is the canonical "kitchen-sink" reference — the opposite end of the design spectrum from the curated Create-line packs above. Researched 2026-06-30 from the packs' GitHub repos, the `allthemods.github.io/alltheguides` translation docs, GitHub Discussion `AllTheMods/ATM-10#3539`, and ATM9's real lang file (`AllTheMods/ATM-9` → `kubejs/assets/kubejs/lang/en_us.json`). *Note: this is public-source research, not a local file audit like the Create/Mechanomania entries — counts are approximate where stated.*

- **ATM9/ATM10** — "as many stable mods as fit" kitchen-sinks whose endgame is one capstone: **craft the ATM Star** (ATM10 = 13 components + 3 alloys, each component sourcing items from a different mod). See the ATM10 deep-dive below for the full structure. **Chapter structure:** opener ("Chapter 1: The Beginning", issue #1136) → per-mod chapters → AllTheModium + ATM Star endgame chapter — the textbook kitchen-sink spine.
- **The AllTheModium material spine** — ATM's signature gate: AllTheModium (Overworld/Deep Dark, netherite pick) → Vibranium (Nether, ATM pick) → Unobtainium (End, vibranium pick), tier-locked across 3 dimensions, converging into the Star; killing the Warden grants a quest-reward ingot (a grind replaced by a boss kill). A strong, legible endgame spine for any kitchen-sink.
- **Generous by design; `flexible` progression; localization differs by version.** Generosity (Discussion #3539: *"…people seem to like these sort of rewards"*) — the only hard gate is the capstone. Book-wide `progression_mode: flexible` (issue #1136) so passive tasks count. ATM9 (1.20.1) localizes via **KubeJS lang** (`kubejs/.../lang/en_us.json`, `//n`, `atm9.quest.<chapter>.<sub>.<name>`); ATM10 via FTB native lang (an existing 1.21.1 pack — adopt, don't generate). **Text style** = natural prose (see §writing-style). **Cross-mod synergy is the content** — ATM9's own descriptions walk cross-mod loops (RS Regulator + Crafting Upgrade fed by a Mystical Agriculture farm → autocrafting); teach the *connections*, not mods in isolation.

**Counterpoint — Create: Astral** (Fabric 1.18.2): themed-chapter + deep-integration, the opposite of ATM's parallel mod lines. Chapters keyed to celestial bodies; space travel woven into the spine (not endgame-gated). Mods (Tinkers, Tech Reborn) folded into Create's *one* crafting space via KubeJS — quests teach the shared process once. Use for story/expert packs where the *journey* + *unified system* matter more than the mod list.

**Lessons that adjust SKILL.md's rules (kitchen-sink):**

6. **Kitchen-sink packs lean generous; gate only the capstone.** Don't tighten every ore/reward to expert-pack tightness in a kitchen-sink — that's not what players of the genre want. Reserve hard gating for the ATM-Star / creative-tier endgame item; let the rest flow.
7. **A material-tier spine across dimensions is a strong endgame spine.** One tier per dimension, pick-tier-locked, converging into one capstone item — legible to the player without any custom scripting.
8. **Quest text can localize via KubeJS lang (ATM9) OR FTB native lang (ATM10).** Both ship in real packs. On `--adopt`, detect which before writing text; an ATM9-style pack has *no* FTB lang file at all (text is in `kubejs/.../lang/`), so the generator's lang-add-only merge has nothing to merge into — match the pack's KubeJS scheme or ask.
9. **Write descriptions as natural prose (ATM9's verified style).** The single biggest text-quality lever — see §writing-style.
10. **Themed chapters beat per-mod chapters for story / expert packs.** Create: Astral keys chapters to celestial bodies and ties space travel into the spine — players remember the journey, not the mod list. Use per-mod chapters for kitchen-sink "learn what you want"; themed chapters for "experience this arc."
11. **Deep mod integration needs KubeJS recipe scripting; quests describe the unified system.** Create: Astral folds Tinkers / Tech Reborn into Create's crafting space via custom recipes — the quests teach the shared process (filling, sequenced assembly) once. If the pack integrates deeply, don't write per-mod crafting quests that ignore the shared system.

### ATM10 — deep-dive: design thinking

ATM10 (MC 1.21.1, NeoForge, ~500 mods, EMI) — the current ATM kitchen-sink. *Audited 2026-06-30 from the GitHub repo (4,601 quests / 64 chapters / 6,915 rewards, parsed via the skill's SNBT parser, 0 failures) + SiriusMC guide, r/allthemods, 100-days playthrough, Discussion #3539.*

**Structure:** numbered "main chapters" form a *suggested* spine + per-mod chapters, but the spine is a suggestion — the real organization is **by playstyle lane**, each self-contained (Tech: Mekanism→AE2; Magic: Ars Nouveau/Botania→Blood Magic/Mahou Tsukai; Exploration: Twilight Forest→Mining World + dimensions). Each lane is pickable and finishable on its own. **One forced convergence — the ATM Star:** every lane is optional except the endgame; the Star's 13 components each source items from a different mod (the capstone model of F1/F2: in-chapter + item-task-gated; the cross-mod gate is the crafting chain, not quest deps). **Pacing:** a multi-week arc (100-days run: first Allthemodium ~Day 25, Star started ~Day 50, Infinity Singularity ~Day 75); AllTheModium tier spine = mid-game identity, 8 Star components = late-game. **Portable capstone, pack-type opener:** ATM10: To The Sky reaches the same Star but reshapes Chapter 1 for skyblock (sieve/hammer/squeezer loop → raw ore → "Geores" → Allthemodium) vs survival's mining opener; tier spine + Star stay constant. **Generosity** is explicit philosophy (Discussion #3539: *"the only thing that could actually 'break progression' would be gifting out ATM Stars… people seem to like these sort of rewards"*). **Localization on `--adopt`:** the repo `.gitignore` excludes only the *consolidated* `lang/*.snbt`; the **split per-chapter lang** (`lang/<locale>/chapters/*.snbt`, 15 locales incl. en_us) IS committed — so GitHub has both chapter objects and text. An *installed* pack also has the consolidated lang on disk.

**ATM10 design lessons:**

12. **Converge only at the capstone in a kitchen-sink.** Let the middle be optional, pick-a-lane parallel paths; force cross-mod engagement only at the Star (the one item that *is* the index of the pack).
13. **Rewards and guidance aren't either/or** — ATM10 is a generous pack that also actively directs the player's next goal. "Generous + guiding" is a valid philosophy, not just guide-first-OR-reward-driven.
14. **Make the capstone + tier spine portable; write the opener for the pack type.** ATM10 vs ATM10: To The Sky share the Star and AllTheModium spine; only Chapter 1's resource chain differs (sieve-loop vs mining).

---

## §layout-reasoning — Spatial arrangement thinking

The *reasoning* behind SKILL.md's layout tables (two families, clutter flags, shape/size, coordinates — those stay inline as lookup). Apply whenever you assign `x`/`y` — via `layout: { mode: "auto" }` or by hand. Measured best practices from 4 large chapters in a polished Create-series pack for arranging quests so dependency lines don't cross.

### Narrative layout — the horizontal spine + fan-out cluster model

1. **Main path = horizontal line at `y=0`**, constant x-step **3.5** between spine nodes (smallest spacing where two `size: 2.0` nodes don't overlap; 2.0–3.0 for mixed sizes).
2. **Alternate hub/step on the spine** — `size: 2.0` `gear`/`square` milestones at every other slot (7.0 apart), `size: 1.0` steps between.
3. **Fan dependents vertically** (inverted-funnel): spread symmetrically across x around the hub (±1.0–1.5, not stacked in its column); step down in increasing |y| (nearest pair `y±1`, converge at `y±3`); left deps left, right deps right → lines never cross; hub radius ≤ ~2.5.
4. **Vertical lists only for parallel variants** (choose-one tiers); for distinct related items use the x-spread fan, never a stack.
5. **Align independent sub-trees on shared y-lanes** (e.g. 7 quests at `y=2.5` across different x) → tidy "tracks" not scatter.

### Side quests & secrets — push to the periphery

- **Secret quests** (`secret: true`, `rsquare`): place at large |y| or odd fractional coords at the chapter margins.
- **Long-description "build this" schematic quests** (`gear`/`checkmark`): push to outer edges (large |y| or far x) so their text doesn't crowd the spine.
- **Cross-chapter links** (`hexagon`, `size: 2.0`): decorative spots at chapter periphery.

### Anti-patterns to avoid

1. ❌ **Long diagonal dependency lines** — every dependent should be within ~2.5 units of its hub. If a dep stretches across the chapter, restructure.
2. ❌ **Stacking** — two quests at the exact same `(x,y)`. Use fractional coords to dodge if absolutely needed.
3. ❌ **Crossing lines** — left dependents left of hub, right ones right. For many-to-one merges, arrange sources in a ring around the target.
4. ❌ **Unbounded fan-out** — a hub with 10 dependents spread across 20 x-units. Split into sub-hubs or cluster within ~3-unit radius.
5. ❌ **All lines visible at once** in big chapters — use `hide_until_deps_visible` on branch/leaf quests.
6. ❌ **Random y-scatter** — align parallel sub-trees on shared y-lanes.
7. ❌ **Mixing layout families** — a chapter is either narrative (horizontal spine + fan-out) or catalog (uniform grid), never both.

### Chapter grouping & visual hierarchy (what the player sees)

Spatial layout is about *lines not crossing*; this is about the book as a UI — tabs, icons, color, and the progressive-reveal experience. A player who can't find the next thing won't do it, however good the wiring is.

- **Group chapters into tabs via `chapter_groups`** — a 40-chapter kitchen-sink as one flat list is unscannable; group into tabs ("Getting Started", "Tech", "Magic", "World", "Endgame") ~5–8 chapters each (reference §4). One group is fine for a small book.
- **Chapter title = the tab label; short and named** after the mod/dimension/age, not a slug (ATM9: numbered opener + mod-name titles; Create: Astral: celestial bodies). **Every chapter gets an `icon`** — the mod's signature item; a chapter with no icon looks unfinished.
- **Color is semantic, not decorative** — give each mod/theme a stable accent color ("blue = Refined Storage, green = farming"); don't rainbow.
- **Shape & size encode importance** (see SKILL.md's shape table); set `default_quest_shape` once in `data`, leave chapters at `""` to inherit (lesson 3), reserve explicit shapes for the ~5–8% milestones.
- **Progressive reveal is the UX** — `hide_until_deps_visible` makes the chapter *grow* as the player progresses (the biggest "feels alive" lever above ~30 quests/chapter; pair with `hide_dependency_lines` on many-to-one hubs); small chapters (<~20) can show everything. **Use `quest_links` (hexagon) for cross-listing**, not duplicate quests (reference §18). **`autofocus_quest_id`** centers the view on the next step in a long linear chapter.

---

## §atm-layout-patterns — Kitchen-sink layout templates (ATM9/ATM10)

The two families in §layout-reasoning (narrative horizontal spine + reference catalog grid) are measured on curated Create-series packs. Kitchen-sink packs (ATM9: 436 quests/6 chapters analyzed; ATM10: 443 quests/6 chapters) use a **different spatial grammar** — tighter grids, richer shape vocabulary, and more layout diversity per book. Five templates cover the observed patterns. Pick one per chapter; don't mix within a chapter (same rule as §layout-reasoning).

**How ATM spacing differs from narrative packs:** narrative chapters (Create: Delight) use x-step 3.5 between spine nodes; ATM chapters use x-step **0.5–1.0** (dominant 0.5 in ATM10, 1.0 in ATM9). The tighter grid is possible because ATM relies on `hide_dependency_lines` (×438 in ATM10) instead of spatial separation to declutter. When lines are invisible, nodes can be closer.

### Template 1: Compact Horizontal Spine (the ATM default)

**When:** any per-mod chapter in a kitchen-sink (the most common ATM layout).
**Measured on:** ATM10 AE2 (73 quests, aspect 2.6), ATM9 AE2 (70 quests, aspect 2.6), ATM10 welcome (6 quests).

```
Spine: y ≈ 0, x increments 0.5–1.0 per step
Branches: fan ±1.0–2.5 on y, within 2.0 of parent on x
Aspect: 2.0–3.0 (wider than tall)
Grid: 0.5-unit (96%+ coords are multiples of 0.5)
Shapes: chapter default_quest_shape for most; explicit shape only on hubs (~10–15%)
Sizes: default (1.0) for ~70%; 1.2–1.5 on hubs; 2.0+ rare
Anti-clutter: hide_dependency_lines on hubs with >3 dependents
```

The spine runs left-to-right along y=0. Short branches fan above/below. Unlike narrative chapters, there are no alternating hub/step sizes — most nodes are the same size, and shape (not size) carries the semantic weight. Dependency chains are shallow (depth 3–5); the chapter reads as a flat catalog with a gentle left-to-right pull.

**Coordinate example (ATM10 AE2, first 6 quests):**
```
(0.0, 0.0) → (0.5, 0.0) → (1.0, 0.0) → (1.5, -0.5) → (1.5, 0.5) → (2.0, 0.0)
```

### Template 2: Vertical Tiered Cascade

**When:** a mod with distinct tiers/stages that should be presented top-to-bottom (magic mods, skill trees).
**Measured on:** ATM10 Ars Nouveau (130 quests, aspect 0.93), ATM9 Ars Nouveau (130 quests, aspect 0.93), ATM9 Create (57 quests, aspect 1.1).

```
Spine: vertical, x ≈ 0, y increments −2.0 to −4.0 per tier
Tiers: horizontal bands of 5–15 quests at each y-level, spread ±5.0 on x
Aspect: 0.8–1.2 (near square or slightly tall)
Grid: 0.5-unit
Shapes: mix — tier entry point gets a distinct shape (gear/hexagon), rest default
Fan-out: high (15–30 from a single tier-gate hub)
Anti-clutter: hide_dependency_lines on the tier-gate hub; branches stay in their y-band
```

The chapter reads top-to-bottom: each tier is a horizontal band, and a single "gate" quest connects tier N to tier N+1. Within a tier, quests are independent (no deps among siblings). The gate quest has high fan-out (all quests in the next tier depend on it), making it a visual bottleneck.

**Shape-role mapping (Ars Nouveau):** tier-gate = `gear` or `hexagon` size 1.5–2.0; spell recipes = `rsquare` (default size); components = default `circle`. The shape tells the player "this is a milestone" vs "this is a recipe to try."

### Template 3: Parallel Material Columns

**When:** a chapter with 2–5 independent upgrade paths / material tiers that the player picks between.
**Measured on:** ATM10 Allthemodium (54 quests, aspect 3.6), ATM9 Allthemodium (30 quests, aspect 1.1).

```
Columns: 2–5 vertical chains side by side, each 0.5–1.5 apart on x
Within column: y-step 1.0–2.0, linear dependency chain
Cross-column deps: none or rare (only at convergence point, if any)
Aspect: 1.0–3.5 (varies by column count)
Grid: 0.5-unit
Shapes: each column can have its own shape identity (diamond for one material, rsquare for another)
Convergence: optional — if present, a single node at the far right depends on the last quest in each column
```

Each column is an independent upgrade path (e.g., Allthemodium tools → Allthemodium armor → Allthemodium weapons). The player picks which column to pursue. Columns are visually parallel, making the "pick your path" intent obvious. If there's a convergence node (alloy, endgame tool), it sits at the far right or center-bottom, with `hide_dependency_lines: true` on the long cross-column lines.

**ATM10 Allthemodium specifics:** `default_quest_shape: diamond` (material identity); 3–4 parallel columns; each column alternates `rsquare(y=-1)` / `octagon(y=+1)` pairs per tier; `hexagon` cross-link nodes point back to the root. `hide_dependency_lines` on 31/54 quests — the heaviest usage of any analyzed chapter.

### Template 4: Radial Hub (intro/convergence chapter)

**When:** a short intro chapter or a capstone convergence point where everything radiates from one center node.
**Measured on:** ATM9 An Introduction (52 quests), ATM10 welcome (6 quests).

```
Center: one large node at (0, 0), shape = pentagon/hexagon, size 2.0–3.0
Spokes: 4–8 branches radiating outward, each a short chain (2–5 quests)
Angle: branches evenly distributed (45°–90° apart)
Aspect: ~1.0 (square, radiates equally in all directions)
Grid: 0.5-unit
Anti-clutter: minimal (short chapter, <20 quests typical)
```

The center node is the chapter's "you are here" anchor. Branches radiate outward like spokes, each introducing a different topic. This is the opposite of the linear spine — instead of left-to-right progression, it's center-to-periphery exploration. Works best for short chapters (<20 quests); beyond that, the spoke lengths create visual imbalance.

**For capstone convergence (ATM Star style):** invert the direction — components are the spokes, the capstone is the center. Each spoke is a sub-tree of 6–9 nodes converging inward. The capstone is the chapter's largest node (`pentagon size 5.0` per P3).

### Template 5: Decorated Freeform (image-anchored layout)

**When:** a large, visually rich chapter where background images provide spatial structure (the most expensive layout to author, but the most polished-looking).
**Measured on:** ATM10 Create (90 quests, 116 images!), ATM10 Mekanism (90 quests, 26 images).

```
Layout: fractional coordinates (GCD 0.025–0.1), not grid-aligned
Images: chapter images[] array provides visual scaffolding (machine diagrams, recipe charts, mod logos)
Quests: positioned ON or NEAR their associated image
Aspect: varies freely
Shapes: mixed, driven by the image's visual hierarchy
Anti-clutter: hide_dependency_lines heavily; the image IS the visual organizer, not dependency lines
```

This is the most freeform template — coordinates are fractional, quests cluster around images rather than along a spine, and the dependency graph is secondary to the visual layout. The chapter's `images[]` array carries the spatial structure. Use this only when you have strong visual assets (mod screenshots, diagram textures) to anchor the layout; without images, it degenerates into random scatter (anti-pattern 6 from §layout-reasoning).

**When NOT to use:** small chapters (<30 quests), chapters without visual assets, or when you need the layout to be maintainable by hand (fractional coords are fragile to edit).

### Template 6: Hexagonal Expert Web (GregTech-style)

**When:** an expert-mode pack with deep, interlocking dependency chains where quests unlock through multi-path branching (not linear progression).
**Measured on:** Monifactory (GregTech CEu successor, 5 chapters / 248 quests), the most structurally complex pack analyzed.

```
Grid: 0.25-unit (finest precision of any pack studied)
Shapes: hexagon dominant (~74% of explicit shapes), gear for milestones
Dependency depth: 8–15 (vs ATM's 3–5)
Cross-chapter links: quest_links[] heavily used (43 in Monifactory — a chapter shows nodes from OTHER chapters)
Invisible infrastructure: always_invisible chapters for gamestage routing; ~11% of quests invisible
Anti-clutter: hide_until_deps_visible on branches, dependency_requirement: "one_completed" for branching
Aspect: varies freely (1.0–3.5); large spatial layouts (X-span up to 27.5)
```

This template is fundamentally different from kitchen-sink layouts because it's built around **forced progression gating** — the player cannot skip content. Deep dependency trees (depth 15), multi-path branching (`one_completed`, `min_required_dependencies`), and `gamestage` tasks create a web where every quest is a deliberate step in a carefully designed tech ladder. `quest_links` mirror quests across chapters so the player sees their progression context without navigating away.

**Key structural differences from ATM:**
- ATM: `flexible` progression, `hide_dependency_lines` for visual cleanliness, shape = mod identity
- Expert: `default`/`linear` progression, `hide_until_deps_visible` for progressive reveal, shape = difficulty tier
- ATM: item tasks + rewards as the primary interaction
- Expert: `gamestage` tasks for invisible gating, `command` rewards for automation, item-submission tasks (not just "obtain"). Note: `gamestage` tasks also appear in non-expert packs (e.g., Skylore skyblock) — the association is Game Stages mod-presence-dependent, not difficulty-dependent

**When to use:** expert/GregTech packs with enforced progression order, deep tech trees, and cross-mod dependencies. NOT for kitchen-sinks where the player picks their path.

### Template 7: Narrative World Map (RPG/adventure)

**When:** an RPG or adventure pack where quests are spatially mapped to a world map, story arc, or themed landscape.
**Measured on:** Prominence II RPG (5 chapters / 335 quests, main_story spanning 35×30 units), Create: Astral (celestial body chapters).

```
Layout: large spatial canvas (35+ × 30+ units), quests positioned to match an in-world geography
Images: chapter images with `dependency` field — images progressively REVEAL as quests complete
Progression: often linear within a story arc, but spatial arrangement follows the narrative geography
Aspect: 1.0–1.5 (roughly square, matching map proportions)
Shapes: varied — tied to quest type (combat = diamond, exploration = circle, boss = hexagon)
Anti-clutter: dependency-gated images (the map itself unfolds); hide_until_deps_visible on future content
```

The core insight: quests are positioned where they **happen** in the game world, not along an abstract progression axis. A "forest" quest sits in the forest region of the map image; a "dragon" quest sits in the End. Images with `dependency` fields create a **progressive cartography** — the map grows as the player explores.

**Dependency-gated images** (unique to this template): an `images[]` entry with `dependency: "<quest_hex>"` appears only after that quest completes. Multiple images can share one dependency, creating scene-change chains. This is the most powerful visual storytelling tool in FTB Quests.

**When to use:** RPG/adventure packs with a world map, story-driven packs where spatial metaphor matters, dimension-exploration packs. NOT for pure tech or kitchen-sink packs.

### Template selection decision tree

```
Expert/GregTech pack with deep forced progression?
  → Template 6 (Hexagonal Expert Web)

RPG/adventure with world-map spatial metaphor?
  → Template 7 (Narrative World Map)

Chapter has <20 quests + is intro/convergence?
  → Template 4 (Radial Hub)

Chapter has background images as visual anchors?
  → Template 5 (Decorated Freeform)

Chapter teaches a mod with distinct tiers/stages?
  → Template 2 (Vertical Tiered Cascade)

Chapter has 2–5 independent upgrade paths?
  → Template 3 (Parallel Material Columns)

Default for any per-mod chapter:
  → Template 1 (Compact Horizontal Spine)
```

### ATM vs narrative vs catalog vs expert — when to use which family

| Pack type | Primary family | Spacing | Anti-clutter lever | Progression |
|---|---|---|---|---|
| Curated Create-series (story/expert) | Narrative (§layout-reasoning) | x-step 3.5 | `hide_until_deps_visible` | `default` (locked) |
| Kitchen-sink (ATM-style) | ATM Templates 1–5 (this section) | x-step 0.5–1.0 | `hide_dependency_lines` | `flexible` |
| Expert/GregTech | Expert Template 6 (this section) | grid 0.25 | `hide_until_deps_visible` + invisible chapters | `default`/`linear` |
| RPG/adventure | Narrative Map Template 7 (this section) | freeform (map-driven) | dependency-gated images | varies |
| Recipe/food catalog | Catalog (reference §20g) | grid 2.0–3.0 | `hide_dependency_lines` on hubs | `flexible` |
| Skyblock | ATM Template 1 (compact) + linear opener | x-step 0.5–1.0 | `hide_until_deps_visible` (early game) | `default` |

---

## §pack-type-patterns — Design patterns by pack genre

Patterns discovered across 8 additional modpacks (Monifactory, ATM6-Expert, ATM9-Sky, Arcana, Prominence II, Create: Astral, Create Skylands, Enigmatica 9, ATM-11) that don't fit neatly into layout templates but are important authoring guidance.

### Expert pack patterns (Monifactory + ATM6-Expert + Enigmatica 9 Expert)

1. **Invisible routing chapters.** Monifactory uses `always_invisible` chapters as backend infrastructure — gamestage progression, internal triggers, cross-mod state — never shown to the player. The visible book is a clean UI; the invisible book runs the logic. Use when you need `gamestage` gating but don't want the player seeing the machinery.
2. **Cross-chapter quest_links as context mirrors.** Monifactory places 43 `quest_links` so a player in one chapter can see where a quest connects to another without navigating. `quest_links` are hexagonal (`shape: "hexagon"`) to visually distinguish them from "real" quests. Use for expert packs where cross-mod dependencies are frequent and players need to see the full picture.
3. **Dual normal/expert chapters.** Enigmatica 9 ships both `mekanism.snbt` (58 quests) and `mekanism_expert.snbt` (19 quests) in the same chapter group. Normal chapters are broader (more quests, more hand-holding); expert chapters are compressed (fewer quests, harder tasks, no tutorial text). Both share the same group tab. Use when one pack targets both audiences.
4. **`dependency_requirement: "one_completed"` for branching.** Expert packs use this for "complete ANY one of these paths to proceed" — Monifactory's voltage-tier system lets the player pick one machine line to prove mastery before unlocking the next tier. Kitchen-sinks use `"all"` by default; reach for `"one"` when the player has genuine alternatives.
5. **`min_required_dependencies: N` for partial gates.** "Complete 3 of 5 prerequisites" — not all, not any-one, but a minimum. Monifactory uses this for soft gates where breadth matters but full completion isn't required. A unique expert-pack tool; kitchen-sinks rarely need it.

### Skyblock pack patterns (ATM9-Sky)

1. **Tutorial IS the opener.** ATM9-Sky's `getting_started` + `getting_started_2` (139 quests combined) are the largest early chapters — the skyblock tutorial (sieve → hammer → crook → ore processing) IS the first chapter, not a separate prelude. In a skyblock, the resource-acquisition loop is the core mechanic, so the opener teaches it exhaustively. Contrast with ATM10 survival where the opener is just "walk around, look at the Star."
2. **`emergency_items` in `data.snbt`.** Skyblock packs set `emergency_items: [{ id: "minecraft:oak_sapling", count: 1 }, { id: "minecraft:lava_bucket", count: 1 }]` — a respawn button for void-death scenarios. Not needed for non-skyblock packs.
3. **Deeper early-game dependency chains.** ATM9-Sky's `getting_started_2` has depth **18** — the deepest of any chapter analyzed. Skyblock tutorials are inherently sequential (you can't skip from sieve to automation), so the opening chapter is a long chain, not a broad fan-out.

### Magic pack patterns (Arcana)

1. **One chapter per magic mod, each following the mod's internal tier system.** Arcana's Ars Nouveau chapter has 317 quests (vs ATM's 130) — magic mods have deeper spell trees than tech mods have recipe chains. Don't compress a magic mod into the same quest count as a tech mod; spell systems are inherently more branching.
2. **School-based parallel roots.** Iron Spells' chapter has **17 root quests** — one per magic school (fire, ice, lightning, etc.) starting simultaneously. This is the highest root count of any chapter analyzed. Each school is an independent path the player picks. Use `default_quest_shape: diamond` and one root per school, each fanning into its own sub-tree.
3. **Diamond-dominant shape palette.** Arcana uses diamond for 39% of quests (214/552) — a much higher proportion than any other pack. Diamond = "a specific spell/ritual to learn" in a magic context. When designing a magic pack, lean on diamond + rsquare over circle.

### RPG/adventure pack patterns (Prominence II)

1. **Theme-grouped chapters by playstyle, not by mod.** Prominence II has 7 chapter groups: Tutorials, Campaign, Realms, Combat & Gear, Magic, Tech, Eternal Knowledge. Each group contains 2–5 chapters. This is the opposite of ATM's per-mod grouping — the player thinks in terms of "what kind of content do I want?" not "which mod do I want to learn?"
2. **Dependency-gated image reveals.** Prominence II's `main_story` uses images with `dependency: "<quest_hex>"` so the world map progressively unfolds. This is the pack's primary UX lever — not `hide_until_deps_visible` on quests, but on the map itself. The visual metaphor of "exploring a map" matches the RPG genre.
3. **Rich task-type diversity.** Prominence II uses 7 task types (item, checkmark, kill, advancement, dimension, observation, biome) vs kitchen-sinks' 2–3. RPG packs need to verify the player actually went somewhere, fought something, explored a biome — not just crafted an item.
4. **Custom rewards for class/progression systems.** `type: "custom"` rewards trigger KubeJS scripts for class unlocks, skill points, or reputation gains. RPG packs lean on this more than tech packs because progression is often non-item (a class level, a reputation tier).

### Create-focused pack patterns (Create: Astral, Create Skylands)

1. **Age-based chapter naming mapping to Create tech tiers.** Create Skylands names chapters `stone_age`, `brasscast_iron_age` — directly mapping to Create's native progression tiers. This makes the chapter list itself a tech tree. Use when the pack is built around one mod's progression and the chapters ARE the tiers.
2. **`linear` progression mode (not `flexible`).** Both Create packs use `progression_mode: linear` — strict order, quest locks until dependencies done. Create's tech tree is inherently sequential (can't build a mechanical mixer before a cogwheel), so the quest book enforces the order the mod already implies. Contrast with ATM's `flexible` for kitchen-sinks.
3. **Minimal rewards.** Create Skylands has 1 total reward across 4 chapters. Create packs teach by unlocking the NEXT machine, not by giving items. The progression IS the reward. Don't force item rewards on a Create pack where the real reward is the next tech tier.

---

## §writing-style — Quest text & description writing style (full)

Quest text is what the player actually reads. The field/ID machinery elsewhere in the skill exists to *deliver* that text — so write it like a modpack author talking to a player, not like a config file labeling itself. **Default to natural, concise prose; avoid label-value "element-style" (要素式) checklists.** This applies in Step 4 when you author `quest_subtitle` / `quest_desc` and chapter subtitles, for every quest. (The 3-slot length table stays inline in SKILL.md at the point of use.)

**Write prose, not elements.** The anti-pattern is the label-value checklist (`目标：… / 数量：… / 作用：…`) — the quest UI already shows the item + count + reward, so restating them is noise; spend the description on the *why* and *how*. ✅ Natural prose (ATM9, paraphrased): *"The &9Regulator Upgrade&r lets you keep a set amount of items in a block or machine — say, keep 64 Coal in a Furnace. Pop it in the exporter and set it to 64, and your system keeps the furnace fueled."*

**Style rules (distilled from ATM9's real quest text — quote-verified 2026-06-30):** (1) second person, conversational ("you"/"your"); (2) one concrete example, not an abstract rule (a specific number + block beats generic); (3) color-code key terms — one stable color per concept (`&9Regulator Upgrade&r`, `&e…&r` for the single most important phrase, sparingly); (4) paragraph breaks (`\n\n`, or `//n` in ATM's KubeJS lang) for steps, not bullets; (5) a rhetorical question is a fine bridge — once; (6) end a teaching quest with the use-case; (7) titles name the thing (`Muncher`, `Ultimate Weapon!`), number ordered sub-lines (`Step 1:`, `Step 2:`).

**Length budget.** Title ≤ 4 words. Subtitle = 1 line. Description ~2–4 sentences for a normal quest; a *system-teaching* quest (the Feast_Afoot / ATM9-upgrade pattern) may run 2–3 short paragraphs — the one case where long text is warranted, and it's still prose. Past ~5 sentences on a normal quest you're padding — move the excess into a linked "how this works" quest or a chapter subtitle.

**When in doubt, write it the way you'd explain it to a friend over voice chat, then trim 20%.** The quest UI already shows the item, the count, and the reward — your text only needs to add the part the UI can't: context, the trick, and the reason to care.

> **Localization note.** These rules are locale-agnostic — write natural prose in whatever `locales` Step 2 settled. `\n\n` paragraph separators and `&`-color codes work in both the JSON5 lang model and inline SNBT. If you `--adopt` an ATM-style pack that localizes through KubeJS (`kubejs/assets/kubejs/lang/en_us.json`, `//n` newlines, `atm9.quest.<chapter>.desc.<name>` keys) rather than FTB's own lang, match its newline token and key scheme instead of introducing a second one. Item names render localized via `{item.modid:name}` placeholders in lang-file packs (or plain text inline) — prefer that over hand-typing translated names.
