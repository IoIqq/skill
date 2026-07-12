# FTB Quests — Anti-Patterns [ACTIVE]

> **Status:** Active | **Cycle:** 11 | **Updated:** 2026-07-12
> **Predecessor:** `anti-patterns.archive.md` (AP1–AP22, archived after modular redistribution)
> **Scope:** Topology and layout anti-patterns discovered from Cycle 11 Phase 2 onwards. AP1–AP22 remain in the archive; their core lessons have been redistributed to the modular reference files (see `module-index.md`). New patterns here supplement the modular system.

This file continues the anti-pattern numbering from AP22 (the last pattern in the archived version). The archive covers config-level errors (AP1–AP8), AI-generation risks (AP9–AP11), quest-system mechanism defects (AP12–AP13), system safety (AP14–AP16), reward economy (AP17–AP18), gating and presentation (AP19–AP20), and meta-level trust failures (AP21–AP22). The patterns below focus on **topology and spatial layout** — the layer where coordinate placement, shape semantics, and dependency line rendering converge into the player's visual experience of the quest book.

Topology anti-patterns are distinct from the config-level patterns in the archive because they don't produce broken quests — they produce broken *navigability*. A quest with correct items, rewards, and dependencies can still be functionally useless if the player can't find it, can't tell what it connects to, or can't parse the chapter's visual structure at a glance. The mcmod.cn community tutorial (post/2494) puts it bluntly: neglecting layout design causes players' "血压升高" (blood pressure to rise), and if you cannot maintain a clean, symmetrical structure, you should hide the connection lines entirely rather than subject players to a frustrating and messy interface.

---

## AP23 — Topology Mixing (the identity-crisis chapter)

**Symptom:** A single chapter uses multiple topology types without clear regional separation. The left half of the chapter is a linear chain, the center suddenly becomes a hub-fan, and the right side is a loose grid — but there are no decorative images, spacing gaps, or visual boundaries to signal the transition. The player scrolls through the chapter and can't build a mental model of how the content is organized.

**Root cause:** The pack author designed each section of the chapter independently, choosing the topology that suited each section's content, but didn't establish regional boundaries or visual transitions between them. In FTB Quests config terms, the quests within the same chapter use different layout strategies without corresponding decorative images (`images: []`), color-coded toolbox textures, or intentional empty-space buffers to delineate the regions. The `default_quest_shape` at chapter level may be set to a single value, but individual quests override it inconsistently, further blurring the visual identity.

**Consequence:** Players can't predict what the next scroll will reveal. In a well-structured chapter, the topology type sets expectations: a linear chain promises sequential progression, a hub-fan promises branching choices, a grid promises a catalog to browse. When topologies mix without signaling, the player's navigation strategy keeps failing — they expect a linear next-step but find a radial burst, or they expect a catalog but encounter a chain. This is the spatial equivalent of AP20 (Quest Tab Overwhelm): AP20 concerns information density; AP23 concerns structural incoherence.

The Craftoria Create chapter demonstrates the *correct* approach to multi-topology design: it uses 8 colored toolbox compartments (`ftbquests:textures/gui/toolbox_interior.png` as region backgrounds) to delineate regions, each with its own internal topology. The decorative images function as visual walls that tell the player "you are entering a new section." Without these boundaries, the same layout would be disorienting.

**Fix:** (1) If a chapter needs multiple topology types, divide it into visually distinct regions using decorative images, color-coded backgrounds, or at minimum 4-8 units of empty space between regions (as documented in MP47 Compartment Region Layout). (2) Set each region's entry quest to a distinctive shape and size (2.0+) so the player can orient themselves. (3) If the chapter is small enough that regions aren't viable (< 50 quests), pick ONE topology type and stick with it — use MP48 Shape Monoculture to maintain visual consistency. (4) Test by scrolling through the chapter at normal speed: if you can't predict the layout type of the next visible area, the topology boundaries need strengthening.

**Source:** Phase 1 topology-coordinates.md cross-pack comparison; MP47 (Compartment Region Layout) as the correct alternative; Craftoria Create chapter as a positive example of multi-region design.

---

## AP24 — Spacing Inconsistency (the uneven rhythm)

**Symptom:** Adjacent quests within the same chain or region have wildly different spacing — one pair is 0.5 units apart (nearly overlapping), while the next pair is 4.0 units apart (creating an empty void). The visual rhythm of the chapter is erratic: dense clusters alternate with sparse gaps, and the player can't tell whether a gap means "end of section" or "author forgot to adjust the coordinates."

**Root cause:** The pack author placed quests manually without following a consistent spacing formula, or added quests incrementally over time without re-adjusting the surrounding layout. In FTB Quests config terms, the x/y coordinates of adjacent quests show high variance in inter-quest distance. The topology-coordinates.md spacing formulas (vertical spacing = 1.5 base, column gap = 2.0, hub radius = 3.0 + fan_out × 0.4) provide the intended ranges, but these are not enforced by the FTB Quests editor — the author must maintain consistency manually.

**Consequence:** Players interpret spacing as a semantic signal. Tight spacing (1.0-1.5 units) suggests closely related quests in the same chain; wide spacing (3.0+ units) suggests a section break or transition. When spacing is inconsistent within a chain, the player misreads the structure: they think a wide gap means "new section" and stop looking for the continuation, or they think a tight cluster means "these are all related" when in fact the quests belong to different chains that happen to be placed close together. The mcmod.cn tutorial (post/2494) explicitly advises that linear layouts should follow "长度相等、对称等原则" (equal-length, symmetry principles) to make quest lines visually beautiful — violating this principle creates the anti-pattern.

**Fix:** (1) Apply the spacing formulas from topology-coordinates.md Layer 2 consistently within each region: vertical chain spacing should be constant (e.g., always 1.5), column gap should be constant (e.g., always 2.0), and hub radius should follow the formula. (2) Use section breaks (4+ units of empty space) only at intentional transitions — between sub-chains, between topology regions, or before capstone quests. (3) After placing quests, audit the spacing variance: if the standard deviation of inter-quest distance within a chain exceeds 30% of the mean, re-adjust. (4) For incrementally-authored chapters, run a "spacing normalization" pass after each major addition: select all quests in a chain and re-distribute them with equal spacing.

**Source:** topology-coordinates.md spacing formulas; mcmod.cn post/2494 layout advice ("长度相等、对称等原则"); Monifactory groundwork (positive example — consistent 1.5-2.0 spacing within clusters, 4-8 units between clusters).

---

## AP25 — Shape Semantic Conflict (the lying shape)

**Symptom:** The same shape means different things in different chapters of the same pack. In Chapter A, "hexagon" means "standard tech progression quest" and "pentagon" means "boss fight." In Chapter B, "hexagon" is used for optional side quests and "pentagon" is used for crafting milestones. The player learns the shape vocabulary from the first chapter, then has that vocabulary invalidated when they reach the second chapter.

**Root cause:** Different chapters were authored independently (possibly by different team members in a multi-author pack) without a shared shape style guide. Each author chose shapes based on personal preference rather than following the pack-level shape decision tree documented in topology-coordinates.md Layer 2. In FTB Quests config terms, the `shape` field on individual quests overrides the chapter's `default_quest_shape`, and different chapters use different override patterns.

**Consequence:** Shape semantics are the quest book's visual grammar. When shape meanings are consistent, the player can glance at a quest's shape and immediately know its role: "that's a boss (pentagon)," "that's a starting hub (gear)," "that's optional (circle)." When shapes conflict across chapters, the player loses this at-a-glance reading ability and must read every quest's title and description to understand its role. This is particularly damaging in large packs (100+ chapters) where the player relies on shape as a fast-scanning heuristic.

The topology-coordinates.md shape decision tree (Layer 2) documents the empirical consensus across 9 packs: gear for root hubs, diamond for convergence, pentagon for combat/boss, octagon for milestones, circle for optional, none for catalog entries. Packs that follow this convention consistently (Monifactory, ATM-10) produce chapters that are visually parseable even by new players. Packs that deviate without documentation create the semantic conflict.

**Fix:** (1) Establish a pack-level shape style guide before authoring begins. The guide should map each shape to exactly one semantic role, following the topology-coordinates.md decision tree as a baseline. (2) Document the shape guide in the pack's author wiki or in a comment at the top of the `defaultchapter.snbt` template. (3) When multiple authors contribute chapters, review each chapter's shape usage against the style guide during PR review. (4) If a chapter's content doesn't fit the standard shape vocabulary (e.g., a chapter with no boss fights and no optional quests), use Shape Monoculture (MP48) — set all quests to the chapter default and let coordinate placement carry the structure. (5) Never reassign a shape's meaning mid-pack: if "pentagon" means "boss" in Chapter 1, it must mean "boss" everywhere.

**Source:** topology-coordinates.md Layer 2 Shape Decision Tree; MP20 (Shape-as-Tier Signal) from micro-patterns archive; cross-pack shape comparison showing consistent semantic mapping in Monifactory, ATM-10, and GregTech-Odyssey.

---

## AP26 — Node Collision (the overlapping icons)

**Symptom:** Two or more quests are placed so close together that their icons overlap in the quest book UI. The player sees a jumbled mess of icons and can't click on the quest they want. In extreme cases, three or four quests occupy the same pixel area, making it impossible to select any individual one without zooming in or using the quest list sidebar.

**Root cause:** Quest coordinates were assigned without collision detection, or a batch operation (e.g., bulk-moving quests after a layout restructure) placed multiple quests at the same or nearly-identical coordinates. In FTB Quests config terms, two quests have `x` and `y` values that differ by less than the minimum center-to-center distance (1.0 units for standard-size quests, adjusted for `size` values). The FTB Quests editor allows free placement without snap-to-grid or collision warnings, so overlaps can happen silently during manual authoring.

The topology-coordinates.md collision detection algorithm (Layer 1, Phase 4) defines `MIN_DISTANCE = 1.0` and `PREFERRED_DISTANCE = 1.5`, with a diagonal bonus of 0.85 for diagonal neighbors. These values were derived from the empirically observed minimum spacing across all 19 chapters sampled — no shipping pack has quests closer than ~0.71 units apart (the diagonal step in ATM-10 basic_tools), and most stay above 1.0.

**Consequence:** Overlapping quests are a usability catastrophe. The player can't click the quest they want, can't read the overlapping icons, and may not even realize there are multiple quests at that location. For quests with `hide_until_deps_visible: true`, a collision with a visible quest can make the hidden quest's appearance point overlap with the visible one, so the player never notices the new quest appeared. This is a pure authoring error — the quest data is correct, but the spatial rendering is broken.

**Fix:** (1) Run the collision detection algorithm from topology-coordinates.md (Layer 1, Phase 4) after every batch of quest placements. The algorithm iterates up to 10 times, pushing overlapping quests apart along the axis of least constraint. (2) Enforce `minimum_center_distance = 1.0` for all quest pairs, adjusted upward for quests with `size > 1.0` (a size-2.0 quest needs 1.5 units of clearance from its center). (3) Snap coordinates to a quarter-grid (0.25 precision) or half-grid (0.5 precision) to prevent accidental near-overlaps from floating-point imprecision. (4) For hub-fan layouts where radial placement can cause outer-ring overlaps, increase the hub radius using the formula `hub_radius = clamp(3.0 + fan_out * 0.4, 3.5, 7.0)` to ensure leaves have sufficient spacing. (5) Test by opening the chapter in-game and attempting to click every quest — if any quest is unclickable due to overlap, adjust coordinates.

**Source:** topology-coordinates.md Phase 4 collision detection algorithm; ATM-10 basic_tools (positive example — 0.71 diagonal step is the minimum observed in shipping packs); hub radius formula from Layer 2.

---

## AP27 — Dependency Line Spaghetti (the tangled web)

**Symptom:** The dependency lines connecting quests form a dense, crossing web that obscures the chapter's structure rather than clarifying it. Lines cross over unrelated quests, loop back across the chapter, and converge in tangled knots around hub quests. The player can't trace a single dependency path from start to end without their eye following the wrong line.

**Root cause:** The chapter has many cross-dependencies (quests depending on quests in distant regions of the layout), and `hide_dependency_lines` was not used selectively to reduce visual clutter. In FTB Quests config terms, `hide_dependency_lines: true` is either not used at all (all lines visible) or used inconsistently (some hubs have it, some don't). The topology-coordinates.md finalize_layout phase sets a density threshold: when local density exceeds ~8 quests in a 3-unit radius, `hide_dependency_lines` should be activated. Without this heuristic, dense chapters produce the spaghetti effect.

The mcmod.cn tutorial (post/2494) explicitly warns against this: if the layout is "意识流" (stream-of-consciousness / highly abstract), disable line displays to prevent ugly visual clutter. The tutorial further advises that even for structured layouts, individual connection lines should be hidden when they contribute to visual noise. The tutorial also recommends specific layout styles — linear with equal spacing, spiral/vortex for advanced aesthetics — that naturally minimize line crossings through geometric regularity.

**Consequence:** Dependency lines are the quest book's visual syntax tree. When they're clear, the player can see the chapter's structure at a glance: "this chain leads there, that branch goes here, these three converge at the capstone." When they're spaghetti, the player loses this structural overview and must rely on opening each quest individually to check its dependencies. The quest book's role as a *navigation map* collapses — it becomes a pile of disconnected nodes rather than a connected graph. This is particularly damaging in diamond_convergence and tree_branching topologies, where the visual beauty of the converging paths is a key part of the player's sense of progress.

ATM-10 allthemodium demonstrates the correct approach: 22 of 67 quests use `hide_dependency_lines: true`, concentrated in the dense central cluster, while the sparse outer branches keep their lines visible. This selective hiding preserves the visual structure where it matters (the convergence paths) while reducing clutter where density is high.

**Fix:** (1) Apply the density-based heuristic from topology-coordinates.md: for each quest, count quests within a 3-unit radius; if the count exceeds 8, set `hide_dependency_lines: true`. (2) For hub quests with fan_out >= 5, always set `hide_dependency_lines: true` — the radial lines from a high-fanout hub create the worst spaghetti. (3) For long cross-chapter dependencies (lines that would stretch across the entire layout), use `hide_dependency_lines: true` and instead indicate the dependency in the quest description text. (4) Prefer topologies that minimize line crossings: linear chains and parallel columns naturally have zero crossings; diamond convergence and tree branching have predictable, non-crossing patterns; hub-fan is the most prone to crossings and needs aggressive line hiding. (5) If the chapter's topology inherently produces many crossings (e.g., a complex diamond with 5+ convergence points), consider whether the chapter should be split into sub-chapters with cleaner internal topology.

**Source:** topology-coordinates.md Phase 6 `hide_dependency_lines` heuristic; mcmod.cn post/2494 ("若布局为意识流, 隐藏前置连线"); ATM-10 allthemodium (22/67 hide_dep_lines as positive example); ATM-10 basic_power root (`hide_dependent_lines: true` on the central hub).

---

## Cross-Reference Index

| Anti-Pattern | Related Archive APs | Related MPs | Topology Layer |
|---|---|---|---|
| AP23 Topology Mixing | AP20 (Tab Overwhelm) | MP47 (Compartment Region) | Phase 2 (classification) |
| AP24 Spacing Inconsistency | — | — | Phase 3 (coordinates), Layer 2 (constraints) |
| AP25 Shape Semantic Conflict | AP10 (Style Homogenization) | MP20 (Shape-as-Tier Signal), MP48 (Shape Monoculture) | Phase 5 (shape assignment) |
| AP26 Node Collision | — | — | Phase 4 (collision detection), Layer 2 (min distance) |
| AP27 Dependency Line Spaghetti | AP20 (Tab Overwhelm) | — | Phase 6 (finalize layout) |

---

## Sources

1. **mcmod.cn post/2494** — "1.16的详细FTB任务教程" (Detailed FTB Quests tutorial for 1.16). Chinese community tutorial covering quest layout design, node movement, dependency line management, and visual arrangement principles. Key advice: linear layouts should follow "长度相等、对称等原则" (equal-length, symmetry principles); abstract/stream-of-consciousness layouts should hide dependency lines entirely. https://www.mcmod.cn/post/2494.html

2. **mcmod.cn post/1416** — "FTB任务系统教程" (FTB Quests system tutorial). Foundational Chinese tutorial on quest system configuration, grouping, and visual customization. Emphasizes chapter grouping to keep the "任务列表分明" (quest list distinct and clear). https://www.mcmod.cn/post/1416.html

3. **mcmod.cn post/5840** — "1.12.2超详细的创建ftb任务介绍" (Ultra-detailed FTB quest creation guide for 1.12.2). Documents X/Y coordinate controls, size adjustments, default quest shape templates, and the `hide_dependency_lines` setting ("隐藏相关性行"). https://www.mcmod.cn/post/5840.html

4. **mcmod.cn post/5137** — "如何更改FTB任务的主题和背景" (How to change FTB Quests themes and backgrounds). Advanced visual customization tutorial covering theme files, background images, and tint/border parameters. Notes that theme file errors can crash the game. https://www.mcmod.cn/post/5137.html

5. **mcmod.cn post/6155** — "关于制作冒险类整合包的一些心得分享" (Thoughts on making adventure modpacks). Discusses progression pacing, the dangers of "水槽包" (kitchen-sink packs) with unclear flow, and the importance of phased thematic organization. https://www.mcmod.cn/post/6155.html

6. **topology-coordinates.md** — Phase 1 output documenting 6 topology types with layout algorithms, spacing formulas, shape decision trees, collision detection rules, and 13 real case coordinate extractions from 9 packs. The primary reference for all spatial layout decisions. See `reference/design/topology-coordinates.md`.

7. **Craftoria #231** — "Restructure Powah quests to be more linear." Player feedback that the Powah chapter "throws everything at you" with overwhelming visual presentation. Cited in AP20 (archive) and validated here as evidence that poor topology presentation directly impacts player experience. https://github.com/TeamAOF/Craftoria/issues/231
