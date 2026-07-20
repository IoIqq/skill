# FTB Quests — Anti-Patterns [ACTIVE]

> **Status:** Active | **Cycle:** 19 | **Updated:** 2026-07-19 (Phase 2 Cycle 19 — AP47 indirect evidence from GitHub #2059/#1909, 4 new sources)
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

## AP28 — Mega-Chapter Without Structural Compensation (the unbroken wall)

**Symptom:** A chapter with 150+ quests that presents as a monolithic, undifferentiated block of quest nodes. The player opens the chapter and sees a sea of icons stretching in every direction with no visual hierarchy, no decorative region markers, no hide_dependency_lines to reduce line clutter, and no size variation to indicate which quests are important. Navigating the chapter requires excessive scrolling in multiple directions, and the player cannot build a mental map of where content lives.

**Root cause:** The pack author created a single chapter for an entire mod's progression (or a cross-mod tier) without applying the structural compensation strategies that make large chapters navigable. In FTB Quests config terms, the chapter has 150+ quests but lacks: (1) decorative images for region delineation (MP47), (2) size variation beyond the default 1.0, (3) selective `hide_dependency_lines` usage, and (4) shape vocabulary beyond the chapter default. The topology-coordinates.md guidance explicitly recommends splitting chapters above certain thresholds: linear_chain at >100 quests, tree_branching or hub_fan at >150, grid_catalog at >200.

The Chroma-Technology-2 mekanism chapter (199 quests) demonstrates the *correct* approach to mega-chapter design: it uses 100% diamond shape with convergence_ratio=0.412 and 159 hide_dependency_lines (80% of quests) — the heavy line hiding compensates for the extreme density. The Craftoria Create chapter (180 quests) uses 8 colored toolbox compartments as region markers. Both approaches work because they apply structural compensation. A mega-chapter *without* these strategies is the anti-pattern.

**Consequence:** The player's cognitive load increases linearly with quest count when there's no structural hierarchy. At 150+ quests, the chapter exceeds the player's working memory capacity for spatial navigation — they can't remember which region they've already visited, can't predict where the next quest will be, and must resort to the quest list sidebar rather than using the visual map. This is the quest book equivalent of a "wall of text" — technically all the information is present, but the lack of structure makes it functionally unusable. Craftoria #231 (Reddit u/weirdchildren): "I feel like the quests in the Powah tab kinda just throws everything at you" — this complaint was about a much smaller chapter, illustrating that even moderate-size chapters without structure trigger the same response.

**Fix:** (1) If the chapter has 150+ quests and no structural compensation, split it into sub-chapters by progression tier, mod subsystem, or topology type. (2) If splitting is not viable, apply at least two of these compensation strategies: decorative region images (MP47), selective hide_dependency_lines (AP27 fix), size variation for key quests (MP48), or icon-heavy marking of milestones (MP50). (3) The minimum viable compensation for a mega-chapter is: hide_dependency_lines on all quests with local_density > 8 (per topology-coordinates.md Phase 6), plus size 2.0 on the chapter root and any convergence nodes. (4) Consider adding a chapter-level decorative image as a title banner so the player knows which section they're in when scrolling.

**Source:** topology-coordinates.md mega-chapter guidance (>200 quest split recommendation); Chroma-Technology-2 mekanism (199 quests with 80% hide_dep_lines — positive example); Craftoria Create (180 quests with 8 decorative compartments — positive example); TeamAOF/Craftoria #231 (player complaint about overwhelming quest presentation); CSDN GTNH guide (recommends limiting active trackers to <10 to prevent "任务面板卡顿" / quest panel lag with 3500+ quests).

**Phase 2 Cycle 16 player validation:** The mega-chapter navigation friction extends beyond the visual layout layer into the FTB Quests UI itself. The official FTB Docs Tips & Tricks page warns that the auto-pinning feature "may cause the list of quests to go off the screen" in large modpacks — a system-level acknowledgment that large quest chapters create navigation problems even with perfect coordinate layout. This adds a UI-layer dimension to AP28: even when the spatial layout is well-structured (decorative regions, hide_dependency_lines, size hierarchy), the quest list sidebar can overflow when players pin multiple quests from a mega-chapter. Authors of mega-chapters should be aware that the sidebar list length is proportional to the number of visible/pinned quests, and should consider whether splitting the chapter (reducing per-chapter quest count) solves both the spatial and the UI-list overflow simultaneously. Chroma Endless botania (120 quests, Case 44) with 21% hide_dependency_lines and 20% optional content demonstrates that non-expert mega-chapters can adopt expert-like visual management — but the UI-list overflow remains unaddressed by hide_dependency_lines alone.

---

## AP29 — Dependency Line Color Blindness (the invisible distinction)

**Symptom:** The quest book's dependency lines use colors or styles to distinguish between different progression modes (e.g., linear vs. flexible), but the distinction is lost when the FTB Quests mod version changes, the theme file is customized, or the player has color vision deficiency. The player relied on the color distinction to navigate, and its removal or invisibility leaves them unable to tell at a glance whether a quest follows strict linear progression or allows flexible completion order.

**Root cause:** FTB Quests historically rendered dependency lines in different colors for linear vs. flexible progression modes. In a 2024 update (commit 8537a764), FTB dev desht changed the line coloring system to use theme-based colors that don't distinguish between progression modes. Player MrHimera reported in FTBTeam/FTB-Mods-Issues #1183: "I have a lot of quests, both linear and flexible. And it was very convenient to distinguish them by eye, rather than poking and looking in the settings." The dev acknowledged the behavior was lost but was unsure of its importance.

The underlying issue is that the dependency line appearance is a *cosmetic* feature controlled by the mod, not by the pack author. Pack authors cannot guarantee that their intended visual distinctions will survive mod updates, theme changes, or accessibility needs. Relying on line color as the sole indicator of progression mode creates a fragile navigation system.

**Consequence:** Players who relied on line color to distinguish linear from flexible quests lose their primary navigation heuristic. This is especially damaging in packs that mix progression modes within a single chapter or group — the player can no longer tell whether completing quest A will unlock quest B (linear) or whether they can complete quest B independently (flexible) without opening each quest's settings. The information is still available (in the quest properties panel), but the at-a-glance reading is gone.

**Fix:** (1) Do not rely on dependency line color as the sole indicator of progression mode. Instead, use shape and size to signal the distinction: linear quests can use the chapter default shape, while flexible quests can use a distinct shape (e.g., circle for flexible side content). (2) Use `hide_dependency_lines: true` selectively on flexible quests to reduce visual noise — if a quest is flexible, its dependency lines are informational rather than navigational, and can be hidden without loss. (3) Document the pack's progression mode in the quest description text: "This quest can be completed independently" or "Complete this quest to unlock the next step." (4) If the pack uses a consistent progression mode per chapter (all linear or all flexible), state this in the chapter description so players know what to expect.

**Source:** FTBTeam/FTB-Mods-Issues #1183 (MrHimera — player feedback on losing linear/flexible line color distinction; desht — FTB dev response); FTBTeam/FTB-Quests commit 8537a764 (line coloring change); AP25 (Shape Semantic Conflict) — shape should carry semantic meaning, not line color.

**Phase 2 Cycle 16 player validation:** Full GitHub issue #1183 discussion retrieved. Key detail: player MrHimera described having "a lot of quests, both linear and flexible" and found it "very convenient to distinguish them by eye, rather than poking and looking in the settings." FTB dev desht acknowledged the importance and committed to restoring behavior in FTB Quests 2001.4.5, which "dims the connection lines for unavailable quests." This resolution partially addresses the anti-pattern — the new dimming behavior provides a visual cue for quest availability (locked vs. available) rather than progression mode (linear vs. flexible). Players who need the linear/flexible distinction should still use shape and size as primary indicators per the Fix section above. The issue also demonstrates that dependency line rendering is a *moving target* across FTB Quests versions — reinforcing AP40 (Version-Induced Layout Drift) and the principle that pack authors should not rely on cosmetic rendering features for critical navigation information.

---

## Cycle 13 Phase 2 Anti-Patterns — Skyblock/Adventure/Farming Specific (AP30–AP34)

The following anti-patterns emerge from the Cycle 13 Phase 2 research that specifically targeted skyblock, adventure/RPG, and farming/lifestyle pack types. Unlike the topology-focused AP23–AP29, these patterns address genre-specific gameplay failures that occur when the quest book's structure conflicts with the pack type's inherent gameplay rhythms. They were identified through cross-referencing config-level data (Cases 21–27) with player feedback from mcmod.cn post/6155 (adventure pack design philosophy), GitHub issue trackers, and pack description analysis.

---

## AP30 — Skyblock Resource Bottleneck Death Spiral (the sieve wall)

**Applicable pack types:** skyblock only

**Symptom:** The player reaches a quest that requires an item from a mod they haven't unlocked yet. The only way to obtain that item is through sieving, but the sieve mesh tier required to get the necessary ore drops is gated behind the very progression chain that's blocked. The player is stuck: they can't progress the main chain without sieving better drops, and they can't upgrade their mesh without resources from the main chain. The quest book shows the next step, but the next step is unreachable.

**Root cause:** The mesh upgrade chain (MP58) and the main progression chain share a resource dependency that creates a circular bottleneck. In skyblock packs, ALL resources ultimately come from sieving, so any gate that blocks mesh upgrades also blocks the entire resource pipeline. The pack author designed the mesh chain and the main chain as parallel progression tracks, but introduced a cross-dependency (e.g., iron mesh requires an iron machine frame that requires the main chain's tier 3 machine) that fuses the two tracks into a deadlock. The mcmod.cn adventure design article (post/6155) warns about players being tempted to "开创造破坏原有顺序" (open creative mode and break the intended sequence) — this is exactly what happens when the bottleneck is too severe.

**Consequence:** The player's only options are: (1) grind the current mesh tier for an extremely rare drop that bypasses the bottleneck (hours of repetitive sieving), (2) find an alternative mod path that provides the needed resource without the gated mesh (if one exists), or (3) abandon the pack. This is the skyblock equivalent of AP2 (Circular Dependency Deadlock from the archive), but it's more insidious because the deadlock is in the *resource economy*, not in the quest dependency graph — the quest config shows no circular dependency, but the underlying recipe graph creates one.

**Fix:** (1) Verify that every mesh upgrade's recipe uses only items obtainable through sieving with the *previous* mesh tier (PP8 config implication). (2) If a mesh upgrade requires a main-chain item, provide an alternative recipe using only sievable materials. (3) Test the progression by playing through the first 20 quests with only sieving as a resource source — if you hit a wall before quest 10, the bottleneck is too early. (4) Consider making mesh upgrades purely time-gated (increasingly expensive but always craftable) rather than progression-gated.

**Source:** mcmod.cn post/6155 (开创造破坏原有顺序 — players break sequence when blocked); ATM9-Sky getting_started config (mesh chain structure); PP8 (Perpendicular Progression Relief) for the correct pattern; AP2 (archive — Circular Dependency Deadlock) for the related concept.

---

## AP31 — Adventure Boss Equipment Mismatch (the tier bridge collapse)

**Symptom:** The quest book presents a boss fight quest, but the player's current equipment tier can't deal enough damage to the boss, survive the boss's attacks, or meet the boss's special requirements (e.g., fire resistance for a lava boss). The quests leading up to the boss provided armor and weapons, but those items are calibrated for the previous tier's mobs, not the boss. The player must grind resources outside the quest book to over-equip before attempting the boss.

**Root cause:** The adventure pack's tier bridge — the principle that "上一个世界的顶端装备对应于这个世界的小怪" (previous world's top equipment = this world's basic mobs) — breaks at the boss boundary. The pack author calibrated regular mob encounters for the quest-provided equipment but calibrated the boss for a higher tier that requires optional content or non-quest crafting chains to reach. In FTB Quests config terms, the boss quest has kill tasks for a high-HP entity but the preceding equipment quests reward items whose DPS/defense values are insufficient for the boss's stats. The dependency chain is correct (boss quest depends on equipment quests), but the power curve is discontinuous.

**Consequence:** The boss quest becomes a "wall" rather than a "capstone." Capstone quests should feel like a triumphant culmination of everything the player learned; wall quests feel like an arbitrary block. The player opens the boss quest, tries the fight, dies repeatedly, and then must leave the quest book to figure out what they're missing. This is especially damaging in adventure/RPG packs where combat is the core gameplay loop — if the boss fight isn't achievable with quest-provided gear, the quest book's role as a progression guide collapses. The mcmod.cn adventure design article (post/6155) specifically warns about "难度递进" (difficulty progression) and recommends that designers "restrict powerful gear in late-game zones to prevent effortless mowing" — but the inverse problem (boss too powerful for quest-provided gear) is equally damaging.

**Fix:** (1) Verify that the DPS/defense values of equipment rewarded in the 3-5 quests preceding a boss quest are sufficient to defeat the boss within a reasonable time (2-5 minutes). (2) If the boss requires special equipment (fire resistance, flight, etc.), ensure the quest chain provides or teaches that equipment before the boss quest. (3) Use the boss quest's description to explicitly state what equipment tier is needed: "You'll need at least diamond-tier armor and a fully upgraded Tetra sword to survive this fight." (4) Consider adding a pre-boss "preparation" quest that rewards a key consumable (strength potion, golden apples) to bridge any remaining power gap.

**Source:** mcmod.cn post/6155 (难度递进 — difficulty progression, tier bridge principle); Dragoncraft the_beginning config (boss quests with choice-reward equipment); PP9 (The Hub Promise) for the related concept of visual expectation vs accessibility.

---

## AP32 — Farming Season-Time Conflict (the impossible harvest)

**Applicable pack types:** farming/lifestyle with seasonal crop mods only

**Symptom:** A quest requires the player to harvest a specific crop, but the crop has a growth cycle that takes multiple in-game days or seasons, and the quest chain is linear — the next quest depends on this harvest, and the quest after that depends on the next one. The player plants the crop, waits for it to grow (real-time or season-time), and the entire quest chain pauses while they wait. If the pack uses a season mod (like Serene Seasons), the required crop might only grow in a specific season, and the player may need to wait weeks of in-game time (or use season-changing items that aren't yet available) to reach the right season.

**Root cause:** The quest chain treats farming tasks as instantaneous (like crafting tasks) when they're actually time-dependent. In FTB Quests config terms, the farming quest has an `item` task for a specific crop yield, and the next quest depends on its completion — but the quest system has no awareness of the crop's growth time or seasonal requirements. The pack author designed the chain as if "plant wheat, harvest wheat" were equivalent to "craft iron pickaxe," when in reality the wheat requires 7+ in-game days to mature and may only grow in spring. This conflict between linear quest dependencies and non-linear time requirements is unique to farming/lifestyle packs.

**Consequence:** The player's progression halts not because they lack skill or resources, but because they're waiting for a clock. This is the farming equivalent of being stuck at a loading screen — there's nothing to do except wait (or grind unrelated content). The quest book, which should be a guide through active gameplay, becomes a calendar that tells the player "come back later." For players who want to make progress in a single play session, this is deeply frustrating. The mcmod.cn adventure design article (post/6155) emphasizes maintaining positive feedback during progression — a multi-day crop wait with no alternative activities violates this principle.

**Fix:** (1) For farming quests, either: (a) provide a season-changing or time-accelerating item as a reward in a preceding quest, (b) set the quest's crop requirement to a fast-growing crop (1-2 in-game days) rather than a slow-growing one, (c) make the farming quest flexible (not blocking the main chain) so the player can pursue other quest lines while waiting. (2) If the pack uses Serene Seasons, ensure the quest chain doesn't require a spring crop in a chain that starts in autumn — either align the quest's expected season with the pack's starting season, or provide greenhouse/crop-ignoring-season items before the farming quest. (3) Consider rewarding bone meal or growth-accelerating items in preceding quests to reduce the wait time.

**Source:** mcmod.cn post/6155 (positive feedback during progression); Life-in-the-Village-4 quest structure (farming + adventure hybrid); AP30 (Resource Bottleneck) for the related concept of time-based vs resource-based progression walls.

---

## AP33 — Incomplete Quest Shipment (the empty promise chapter)

**Symptom:** The player opens a chapter in the quest book and finds a handful of quests with no descriptions, no rewards, or no tasks — placeholder content that was shipped before the author finished writing it. Or the chapter exists with a title and a few quests but the majority of the planned content is missing, leaving the player with an incomplete and confusing experience. The chapter's completion percentage stalls at a low value because the missing quests can never be completed.

**Root cause:** The pack shipped with quest content still in progress. In FTB Quests config terms, the chapter has quests with empty `description` fields, missing `tasks` arrays, or placeholder rewards. The pack author intended to complete the content in a future update but released the pack (or pushed an update) before the quest authoring was finished. GregFactory Sky explicitly acknowledges this: "不完整的任务：作者还没搓完" (incomplete quests: author hasn't finished yet). ATM6-Sky's v1.0 changelog states: "quests are not finished yet which is why there is a lack of quests, rewards and descriptions!" This is particularly common in small-team or solo-authored packs where quest authoring is the last step in development.

**Consequence:** The player encounters the empty chapter and forms a negative impression of the pack's quality. If the incomplete chapter is early in the progression (e.g., the first or second chapter), it's the pack's first impression — the same damage as AP4 (The Completionist's Dilemma) but worse because the incompleteness is obvious rather than hidden. Even if the author flags the chapter as "WIP" in the description, players who don't read descriptions (most players, per PP5) will see empty quests and assume the pack is broken. The ATM-10 discussion #3539 demonstrates that players actively monitor quest reward quality — an incomplete chapter with no rewards is immediately noticed.

**Fix:** (1) Never ship a chapter with incomplete content visible to players. If a chapter is WIP, either: (a) don't include it in the release, (b) set all its quests to `always_invisible: true` until they're complete, or (c) add a single visible "Coming Soon" quest at the chapter root that explains the status and hides the placeholder content. (2) For incomplete packs, use a clear versioning signal: "Quest Content: 60% Complete" in the pack description or a dedicated "Pack Status" chapter. (3) Verify that every shipped chapter has: (a) a non-empty description on every quest, (b) at least one task per quest, (c) at least one reward per non-optional quest. (4) Use the `optional: true` flag on placeholder quests so they don't affect completion percentage.

**Source:** GregFactory Sky mcmod.cn page ("不完整的任务：作者还没搓完"); ATM6-Sky v1.0 changelog ("quests are not finished yet"); ATM-10 Discussion #3539 (player monitoring of quest quality); PP4 (The Completionist's Dilemma) for the related concept of stalled completion percentage.

---

## AP34 — Quest Reward Desync After Server Reset (the phantom completion)

**Symptom:** After a server restart or crash, a quest that the player completed shows as completed in the tracker but the rewards were never delivered. Or the quest's NPC guide (echo/向导) asks the player to submit the quest item again, but the item was already consumed. The submit button is grayed out, the rewards are gone, and the player can't re-complete the quest because the system thinks it's already done. The player is stuck in a "phantom completion" state — the quest appears finished but the progression it should have unlocked is inaccessible.

**Root cause:** The quest system's completion state and the reward delivery mechanism are not atomically synchronized. When a server crashes between the "quest completed" event and the "reward delivered" event, the completion flag is saved but the reward delivery is lost. In FTB Quests config terms, the quest's `completed` state is persisted to disk before the reward items are spawned in the player's inventory or the command reward is executed. This is a server-side bug rather than a pack-authoring error, but it's more likely to affect packs with complex reward chains (multiple item rewards, command rewards, or custom KubeJS reward scripts) because there are more failure points between completion and delivery.

**Consequence:** The player loses both the submitted quest item AND the rewards. If the quest item was expensive to craft (a multiblock controller, a rare boss drop, a complex processed item), the loss is devastating — the player must re-craft the item but the quest won't accept it because the quest is already "completed." The StoneBlock 4 issue #9954 documents this exact scenario: "the quest item, Chronon generator, that i had submitted was still gone, but so were the rewards" and "clicking the submit button but its greyed out." This destroys player trust in the quest system (PP1 — The Trust Contract) because the quest book failed to honor its side of the completion contract.

**Fix:** (1) This is primarily a mod-level bug that needs a FTB Quests fix. Pack authors can mitigate by: (a) avoiding expensive single-item submissions as quest tasks — use items that are cheap to re-craft or provide a backup recipe, (b) providing quest rewards via command (`/give`) rather than direct item rewards when possible, because command execution is more robust against server crashes, (c) for critical progression items, add a fallback NPC or shop that provides the item if the quest reward is lost. (2) Server admins should configure automatic backups so that world state can be rolled back to before the crash. (3) Document the issue in the pack's known-issues list so players know to report it rather than assume the pack is broken.

> **Agent instruction:** This anti-pattern is a server-side mod bug and cannot be detected during quest generation. Apply mitigation as generation-time best practices: prefer command rewards for expensive item submissions.

**Source:** ftbteam/ftb-modpack-issues #9954 (StoneBlock 4 — quest item lost, rewards not delivered, submit button grayed out after server reset); PP1 (The Trust Contract) for the trust damage; PP11 (Mystery Box Trust) for the related concept of reward delivery reliability.

---

## AP35 — Skyblock Resource Inflation (the sieve overproduction)

**Applicable pack types:** skyblock only

**Symptom:** Sieve automation produces resources so quickly that the quest task list becomes meaningless. The player builds an automated sieve farm and, within one real-time hour, accumulates enough raw ore to complete 50 quest item submissions at once. The carefully paced quest progression — where each tier-gate quest was supposed to represent a meaningful milestone — collapses because the player can brute-force through every resource requirement without engaging with the intended pacing. The quest book's unlock-and-discover rhythm is replaced by a bulk-craft-and-submit marathon.

**Root cause:** The sieve drop rates and automation speed are calibrated independently from the quest progression pacing. The pack author designed quest item requirements assuming manual or semi-manual sieving (where obtaining 16 iron ore pieces takes 30+ minutes of active play), but the automation setup (auto-sieve from Ex Nihilo Auto Sieve, Applied Energistics integration, or similar) reduces this to seconds per batch. The resource economy was designed for scarcity but delivered in abundance. This is the mirror image of AP30 (Resource Bottleneck Death Spiral): AP30 occurs when resources are too scarce, AP35 occurs when resources are too plentiful.

**Consequence:** The quest book's role as a pacing mechanism is neutralized. Quests that were designed as tier gates (intended to represent days of sieving progress) become trivial checkboxes. The player experiences a "rush" through the early and mid-game content without the intended sense of incremental achievement. This is particularly damaging in skyblock packs where the sieve progression IS the core gameplay loop — if the sieve can be fully automated early, the entire resource economy flattens into a single undifferentiated grind session. The MC百科 adventure design article (post/6155) warns against "强制玩家必须依据流程走完整个内容" — but the inverse problem (no forcing at all, total freedom to rush) produces the same engagement failure: the player burns through content too fast to appreciate it.

**Fix:** (1) Design quest items that require sieve outputs from multiple mesh tiers — a quest requiring both iron-mesh and diamond-mesh products forces the player to progress through mesh upgrades even with automation, because higher-tier meshes require higher-tier resources to craft. (2) Gate automation behind quest progression: make the auto-sieve crafting recipe require an item from the sieve tutorial chain, so the player must manually sieve through the early game before unlocking automation. (3) Use `count` scaling on later quest submissions: if early quests require 4 ore pieces and later ones require 64, the automation investment pays off gradually rather than all at once. (4) Consider non-sieve resource requirements for mid-game quests — mob drops, crop products, or trading items that automation can't trivialize.

**Source:** AP30 (Skyblock Resource Bottleneck) as the mirror-image anti-pattern; PP8 (Side-Chain as Progression Relief Valve) for the principle that side activities should complement, not replace, main progression pacing; Ex Nihilo Creatio auto-sieve mechanics enabling bulk resource generation.

---

## Cycle 14 Phase 2 Anti-Patterns — Reward and Convergence Specific (AP36–AP37)

These anti-patterns emerge from the Cycle 14 Phase 2 cross-validation of reward systems (MP64, MP65) and convergence topologies (MP66, MP69). Unlike the topology-focused patterns above, they address the gap between what the quest book *promises* through its reward and dependency structure and what the player actually *experiences* when interacting with those systems.

---

## AP36 — Reward-Type Roulette (the inconsistent chapter)

**Symptom:** Within a single chapter, quests use a mixture of reward delivery mechanisms — some quests give command rewards that spawn items nearby, others give loot table rewards that require opening a mystery crate, a few give choice rewards that open a selection menu, and some give plain item rewards. The player can't predict what will happen when they complete a quest: will items appear? Will a crate drop? Will a menu pop up? The reward interaction becomes a surprise every time, and not the good kind.

**Root cause:** The pack author (or multiple authors on a team pack) selected reward types on a per-quest basis based on what was convenient at authoring time, without establishing a chapter-level reward-type policy. In FTB Quests config terms, the chapter contains a mix of `type: "command"`, `type: "loot"`, `type: "item"`, and `type: "choice"` rewards distributed across quests without a consistent pattern. The Enigmatica lineage demonstrates the evolution: E6 used 455 raw commands, E9E reduced to 56 commands per chapter with standardized formatting, E9 (non-expert) used 162 commands with consistent icons, and E10 migrated entirely to `type: "loot"` with `table_id`. Each generation standardized the reward type further — but intermediate stages (where some quests retained command rewards while others switched to loot tables) created the inconsistency.

**Consequence:** The reward-type inconsistency breaks the player's interaction rhythm. PP13 (Reward-Type Contract) documents that players learn the chapter's reward mechanism within the first 3-5 quests and expect consistency thereafter. When the mechanism changes unexpectedly, the player's muscle memory fails: they click "complete" expecting items to appear (command reward behavior), but instead a loot crate appears in their inventory requiring manual opening. Or they expect a choice menu but get a fixed item. Each surprise is a micro-friction that accumulates into frustration.

FTBTeam/FTB-Mods-Issues #509 reveals a system-level consequence: FTB dev desht confirmed that loot rewards are "specifically excluded from being claimable via 'Claim All'" by design. When a chapter mixes loot and item rewards, the "Claim All" button claims the item rewards but silently skips the loot rewards. The player sees an incomplete claim, must hunt down each loot-reward quest individually, and loses trust in the bulk-claim mechanism. FTB team member MichaelHillcox acknowledged this friction and proposed a UI improvement (showing pending loot rewards in a separate list), but as of the current FTB Quests version the inconsistency persists at the system level.

**Fix:** (1) Before authoring a chapter, decide on ONE primary reward delivery mechanism and stick with it for all non-tutorial quests. (2) If the chapter uses command rewards, every quest reward should be `type: "command"` with consistent icon and title formatting (MP64). If it uses loot tables, every reward should be `type: "loot"` with consistent table_id naming (MP17). (3) The only acceptable exceptions within a chapter are: XP rewards on tutorial quests (universally understood as supplementary), and a single choice reward on the chapter capstone quest (understood as a milestone celebration). (4) Never mix `type: "loot"` with `type: "item"` in the same chapter unless the quest descriptions explicitly warn about the different claim flows. (5) For team packs with multiple authors, document the reward-type policy in the pack's author wiki and enforce it during PR review.

**Source:** EnigmaticaModpacks/Enigmatica10 #517 (esbraff — "choice reward presumably meant to be random reward" flagged as bug; MuteTiefling — fixed to consistent random); FTBTeam/FTB-Mods-Issues #509 (desht — loot excluded from Claim All; MichaelHillcox — proposed UI fix); Enigmatica lineage reward evolution (E6=455cmd → E9E=56cmd/ch → E9=162cmd → E10=0cmd, migrated to loot tables).
**Cross-reference:** PP13 (Reward-Type Contract) for the player expectation; MP64 (Command-Reward-as-Invisible-Loot-Table) for the command pattern; MP17 (Loot Table Reward) for the loot table alternative; AP8 (Reward Inflation from archive) for the related economy concern.

---

## AP37 — Convergence Claustrophobia (the submission marathon)

[Evidence: WEAK — derived from 1 extreme case (CreateBlock farmer 47-dep). The 10+ deps threshold requires further calibration from additional convergence chapters in Cycle 15+.]

**Symptom:** The player reaches a convergence/capstone quest with 10+ dependencies and must submit items from all prerequisite quests before the capstone unlocks. But the prerequisite quests were completed over a long play period (hours or days), and the items they rewarded or required have been consumed, sold, or lost. The player must re-craft or re-obtain items from deep in the dependency chain, but the capstone quest doesn't tell them which specific items are needed — it only shows that 10+ quests must be "completed," and the player must open each prerequisite quest individually to check what it required. The convergence quest becomes a forensic exercise rather than a triumphant synthesis.

**Root cause:** The capstone quest uses `dependency_requirement: "all_completed"` with 10+ dependencies (MP66), but the prerequisite quests don't retain their submission items — once a quest is completed, the submitted items are consumed, and the player moves on. When the capstone quest itself requires additional items (a common pattern: "bring all components together"), the player must remember or look up what each prerequisite quest needed, then re-craft those items for the capstone's own submission task. The CreateBlock farmer chapter (47 dependencies, MP69) represents the extreme case: the player must have completed 47 prerequisite quests AND potentially re-obtain items from a farming chain that may have been dismantled or automated away.

The problem is amplified by `hide_dependency_lines: true` (which MP66 recommends to prevent visual spaghetti): when dependency lines are hidden, the player can't visually trace which prerequisite quests feed into the capstone, and must rely on memory or the quest list sidebar to navigate back.

**Consequence:** The convergence quest — which should be the chapter's triumphant climax — becomes its most frustrating moment. The player, who has been steadily progressing through the chapter, suddenly hits a wall of bookkeeping: tracking down 10-47 prerequisite quests, checking which items they needed, re-crafting consumed items, and managing inventory space for all the components. This is the opposite of the "positive feedback" principle from the MC百科 adventure design article (bbs.mcmod.cn thread-21004): "玩家在每个世界的收获都是正反馈的" — at the exact moment when the player expects the biggest payoff (the capstone), they get the biggest administrative burden.

The MC百科 article's warning that "过多的套娃只会让玩家厌烦" (excessive nesting will only annoy players) applies directly: when the convergence quest requires items from quests that required items from other quests (multi-level nesting), the re-obtainment chain becomes exponentially complex. A 47-dep convergence where each dep required 2 items means the player potentially needs to track down 94 items across the chapter's entire crafting tree.

**Fix:** (1) For convergence quests with 10+ dependencies, include a comprehensive checklist in the quest description listing every required item with quantities. Don't make the player hunt through 47 prerequisite quests to figure out what they need. (2) Design the convergence quest's own task to require only *new* items (a crafting result that combines prerequisite outputs) rather than re-submission of prerequisite items. The prerequisite quests' completion flags should be sufficient — the capstone's task items should be craftable from the prerequisite rewards. (3) If the convergence quest must require re-submission of prerequisite items, ensure those items are cheap to re-craft (single-step recipes) or provide a "re-craft" recipe in a preceding quest. (4) Consider using `hide_dependency_lines: false` on the last 3-5 quests before the capstone (even if earlier quests hide their lines), so the player can visually trace the final convergence paths. (5) For extreme convergence (20+ deps), add a "preparation" quest before the capstone that rewards a storage item (ender chest, backpack) to help the player manage the component inventory.

**Source:** CreateBlock farmer (47 dependencies, MP66/MP69); MC百科 bbs thread-21004 ("玩家在每个世界的收获都是正反馈的" — positive feedback principle; "过多的套娃只会让玩家厌烦" — excessive nesting warning); MP66 (Extreme Fan-In Convergence) for the config pattern; AP27 (Dependency Line Spaghetti) for the related visual navigation issue.
**Cross-reference:** MP66 (Extreme Fan-In Convergence); MP69 (Dual-Grid Convergence Catalog); PP14 (Progression-as-Reward Contract) — the convergence should be the biggest positive-feedback moment, not the biggest friction; AP27 (Dependency Line Spaghetti) for the visual navigation dimension; R90 (Convergence Item Backtracking Safety) for the formal validation rule implementing this anti-pattern's distance checks.

**Multiplayer applicability:** The convergence claustrophobia anti-pattern is primarily a single-player experience. In team-based server play (3-5 players), the bookkeeping burden distributes naturally: different team members can gather different components simultaneously, turning a 47-dependency "submission marathon" into a parallel operation where each player handles 10-15 components. This significantly reduces the per-player friction. However, the anti-pattern can *shift* rather than disappear in multiplayer: coordination overhead replaces bookkeeping overhead. Players must communicate which components are gathered, avoid duplicate effort, and synchronize submission timing. If the team uses shared storage (AE2, Refined Storage), convergence items may already be in the system — but only if the storage was set up before the convergence point. Authors targeting team play should consider adding a "preparation" quest before extreme convergence that teaches shared-storage organization, and should design convergence items to be stockpile-friendly (cheap to mass-produce) rather than unique (boss drops, quest-only items).

Confidence: The 10+ deps threshold and the claustrophobia pattern are derived from 1 extreme case (CreateBlock farmer, 47 deps). Additional convergence chapters with 10-30 deps are needed to calibrate the threshold and confirm that the friction scales linearly with dependency count.

---

## Cross-Reference Index

| Anti-Pattern | Related Archive APs | Related MPs | Topology Layer |
|---|---|---|---|
| AP23 Topology Mixing | AP20 (Tab Overwhelm) | MP47 (Compartment Region) | Phase 2 (classification) |
| AP24 Spacing Inconsistency | — | — | Phase 3 (coordinates), Layer 2 (constraints) |
| AP25 Shape Semantic Conflict | AP10 (Style Homogenization) | MP20 (Shape-as-Tier Signal), MP48 (Shape Monoculture) | Phase 5 (shape assignment) |
| AP26 Node Collision | — | — | Phase 4 (collision detection), Layer 2 (min distance) |
| AP27 Dependency Line Spaghetti | AP20 (Tab Overwhelm) | — | Phase 6 (finalize layout) |
| AP28 Mega-Chapter No Compensation | AP23 (Topology Mixing) | MP47 (Compartment), MP48 (Monoculture), MP50 (Waypoint) | Phase 2 (mega-chapter guidance) |
| AP29 Dependency Line Color Blindness | AP25 (Shape Semantic Conflict) | MP54 (Shape Legend) | Phase 6 (line rendering) |
| AP30 Skyblock Resource Bottleneck | AP2 (Circular Dependency) | MP58 (Perpendicular Branch), PP8 | Resource economy (recipe graph) |
| AP31 Adventure Boss Equipment Mismatch | — | MP59 (Nested Hub-Fan), PP9 | Combat balance (tier bridge) |
| AP32 Farming Season-Time Conflict | — | MP60 (Barrier Gate), PP10 | Time-dependent progression |
| AP33 Incomplete Quest Shipment | AP4 (Unfinishable Chapter) | PP5 (Context Void) | Pack release readiness |
| AP34 Quest Reward Desync | AP1 (Description-Reality) | PP1 (Trust Contract), PP11 | Server-side reward delivery |
| AP35 Skyblock Resource Inflation | AP30 (Resource Bottleneck, mirror) | MP58 (Perpendicular Branch), PP8 | Resource economy (automation pacing) |
| AP36 Reward-Type Roulette | AP8 (Reward Inflation) | MP64 (Command-Reward), MP17 (Loot Table), PP13 | Reward economy (type consistency) |
| AP37 Convergence Claustrophobia | AP27 (Line Spaghetti) | MP66 (Extreme Fan-In), MP69 (Dual-Grid), PP14, R90 (backtracking safety) | Convergence design (bookkeeping burden) |

---

## Sources

1. **mcmod.cn post/2494** — "1.16的详细FTB任务教程" (Detailed FTB Quests tutorial for 1.16). Chinese community tutorial covering quest layout design, node movement, dependency line management, and visual arrangement principles. Key advice: linear layouts should follow "长度相等、对称等原则" (equal-length, symmetry principles); abstract/stream-of-consciousness layouts should hide dependency lines entirely. https://www.mcmod.cn/post/2494.html

2. **mcmod.cn post/1416** — "FTB任务系统教程" (FTB Quests system tutorial). Foundational Chinese tutorial on quest system configuration, grouping, and visual customization. Emphasizes chapter grouping to keep the "任务列表分明" (quest list distinct and clear). https://www.mcmod.cn/post/1416.html

3. **mcmod.cn post/5840** — "1.12.2超详细的创建ftb任务介绍" (Ultra-detailed FTB quest creation guide for 1.12.2). Documents X/Y coordinate controls, size adjustments, default quest shape templates, and the `hide_dependency_lines` setting ("隐藏相关性行"). https://www.mcmod.cn/post/5840.html

4. **mcmod.cn post/5137** — "如何更改FTB任务的主题和背景" (How to change FTB Quests themes and backgrounds). Advanced visual customization tutorial covering theme files, background images, and tint/border parameters. Notes that theme file errors can crash the game. https://www.mcmod.cn/post/5137.html

5. **mcmod.cn post/6155** — "关于制作冒险类整合包的一些心得分享" (Thoughts on making adventure modpacks). Discusses progression pacing, the dangers of "水槽包" (kitchen-sink packs) with unclear flow, and the importance of phased thematic organization. https://www.mcmod.cn/post/6155.html

6. **topology-coordinates.md** — Phase 1 output documenting 6 topology types with layout algorithms, spacing formulas, shape decision trees, collision detection rules, and 13 real case coordinate extractions from 9 packs. The primary reference for all spatial layout decisions. See `reference/design/topology-coordinates.md`.

7. **Craftoria #231** — "Restructure Powah quests to be more linear." Player feedback that the Powah chapter "throws everything at you" with overwhelming visual presentation. Cited in AP20 (archive) and validated here as evidence that poor topology presentation directly impacts player experience. https://github.com/TeamAOF/Craftoria/issues/231

8. **FTBTeam/FTB-Mods-Issues #2059** — "simultaneous 2D scrolling." Feature request for horizontal+vertical scrolling in FTB Quests, directly relevant to highway_branch and wide chapter navigation. FTB dev MichaelHillcox acknowledged the request as fair. https://github.com/FTBTeam/FTB-Mods-Issues/issues/2059

9. **FTBTeam/FTB-Mods-Issues #1447** — "Quests Legend." FTB team member MichaelHillcox proposed a shape/color legend preset system for the quest book, demonstrating that shape semantics need explicit documentation. https://github.com/FTBTeam/FTB-Mods-Issues/issues/1447

10. **FTBTeam/FTB-Mods-Issues #1183** — "Dependency lines." Player MrHimera reported losing the linear/flexible line color distinction after a mod update, demonstrating the fragility of relying on cosmetic features for navigation. https://github.com/FTBTeam/FTB-Mods-Issues/issues/1183

11. **FTBTeam/FTB-Mods-Issues #503** — "Freeform dep line placement." Feature request for bezier curve dependency lines, with author adamico self-identifying as "OCD quest designer" wanting precise visual control. Dev desht acknowledged feasibility. https://github.com/FTBTeam/FTB-Mods-Issues/issues/503

12. **FTBTeam/FTB-Mods-Issues #962** — "Quest dependency improvements." Chinese pack authors (luoxiawuchen, ShiYan2022) requested task-level dependencies and page breaks to "使任务线更简洁" (make the mission line more concise), demonstrating Chinese pack author preference for compact, visually-guided quest experiences. https://github.com/FTBTeam/FTB-Mods-Issues/issues/962

13. **CSDN GTNH Quest Guide** — "GT New Horizons任务系统攻略：3500+任务高效完成路线图." Describes GTNH's 3500+ quest organization with color-coded difficulty tiers, F4 dependency graph view, and recommends limiting active trackers to <10 to prevent UI lag. https://blog.csdn.net/gitblog_00684/article/details/151525659

14. **ATM-10 Discussion #3539** — "The Quest Book gives way too many rewards that break balance." Player-collaborator debate about quest reward generosity in kitchen-sink packs. Player argues generous rewards "invalidate the whole balance pass"; collaborator counters "the only thing that could actually break progression would be gifting out ATM Stars." Key insight: reward acceptance depends on pack type context. https://github.com/AllTheMods/ATM-10/discussions/3539

15. **ftbteam/ftb-modpack-issues #9954** — "StoneBlock 4 my quest book and the echo of guidance." Player reports quest completion state desync after server reset: submitted item consumed, rewards not delivered, submit button grayed out. Demonstrates AP34 (Quest Reward Desync). https://github.com/ftbteam/ftb-modpack-issues/issues/9954

16. **GregFactory Sky mcmod.cn page** — GregTech skyblock pack with explicitly acknowledged incomplete quest content: "不完整的任务：作者还没搓完" (incomplete quests: author hasn't finished yet). 75% positive reception but very low engagement ("无人问津"). Demonstrates AP33 (Incomplete Quest Shipment). https://www.mcmod.cn/modpack/707.html

17. **ATM6-Sky mcmod.cn version page** — Developer changelog documenting incomplete quest content at v1.0: "quests are not finished yet which is why there is a lack of quests, rewards and descriptions!" Subsequent versions added "Huge update to the quests" (v1.0.7). Demonstrates the common pattern of quest content lagging behind pack release. https://www.mcmod.cn/modpack/version/198.html

18. **FTB Skies 2 mcmod.cn page** — Official design philosophy describes three progression paths (Divination, Cultivation, Exploration) that are "每条道路都是既是独一无二的也是互相成就的" (each path is both unique and mutually supportive). Validates the multi-path hub design as intentional and the perpendicular branch concept. https://www.mcmod.cn/modpack/1129.html

19. **SteamPunk pack description (minecraftxz.com)** — 1000+ quests across skills, magic, Tetra, and steam tech with survival mechanics. Validates the multi-path adventure pack structure that MP59 (Nested Hub-Fan) describes. https://m.minecraftxz.com/SteamPunk/

20. **EnigmaticaModpacks/Enigmatica10 #517** — "Possibly wrong quest rewards." Player esbraff reported that the Chipped quest used choice rewards while other quests used random rewards, flagging the inconsistency as a bug. Collaborator MuteTiefling confirmed and fixed to consistent random rewards. Demonstrates PP13 (Reward-Type Contract) and AP36 (Reward-Type Roulette). https://github.com/EnigmaticaModpacks/Enigmatica10/issues/517

21. **FTBTeam/FTB-Mods-Issues #509** — "Loot Rewards are not claimed by the 'Claim all rewards' button." FTB dev desht explained the intentional exclusion: "if the player's getting a reward that they don't know in advance, they should at least know exactly which quest it came from." MichaelHillcox proposed a compromise UI. Demonstrates the system-level friction of mixing loot and item reward types. https://github.com/FTBTeam/FTB-Mods-Issues/issues/509

22. **MC百科 bbs thread-21004** — "冒险包设计思路" (Adventure Pack Design Philosophy). Chinese pack-author article recommending dimension-based progression with tier bridge principle ("上一个世界的顶端装备对应于这个世界的小怪"), positive feedback at every stage ("玩家在每个世界的收获都是正反馈的"), and warnings against excessive nesting ("过多的套娃只会让玩家厌烦"). Core reference for PP14 and AP37. https://bbs.mcmod.cn/thread-21004-1-1.html

23. **Extraordinary Energy Modern mcmod.cn page** — Tech skyblock with 1000× Mekanism power scaling, zero-reward design focused on industrial progression. "能源建设、工业扩张与自动化生产." 100% positive but "无人问津" (niche). Demonstrates PP14 (Progression-as-Reward) in tech context. https://www.mcmod.cn/modpack/1377.html

24. **EnigmaticaModpacks/Enigmatica10 #151** — "Missing item drop from quests." Player calog3no reported quest reward items not appearing, with screenshot showing the "missing item drop" indicator. Demonstrates the fragility of reward delivery and the importance of reliable claim mechanisms. https://github.com/EnigmaticaModpacks/Enigmatica10/issues/151

---

## Cycle 15 Phase 2 Anti-Patterns — Convergence and Version Specific (AP38–AP40)

These anti-patterns emerge from the Cycle 15 Phase 2 cross-validation research that searched 10 platforms for player feedback. They address specific failure modes around convergence node reward design, flexible mode dependency handling, and version-induced layout degradation — issues that only become visible when player feedback and tool-level behavior are cross-referenced with config analysis.

---

## AP38 — Convergence Over-Reward (the reward dump point)

**Symptom:** The convergence node in a diamond_convergence topology becomes a "reward dumping ground" — the quest at the convergence point gives significantly more rewards than any of the individual branch quests leading to it. Players progressing through any single branch experience sparse rewards along the way, then arrive at the convergence node to find an outsized reward pile. The pacing feels uneven: long stretches of modest gains followed by a sudden windfall, rather than a steady progression of satisfying rewards.

**Root cause:** The pack author, recognizing that the convergence node is a milestone (all paths meet here), compensates with an outsized reward to "celebrate" the achievement. But this creates a pacing imbalance: the branches leading to the convergence are under-rewarded relative to the convergence node itself. In FTB Quests config terms, the convergence quest has `rewards` with significantly higher total value (more items, higher XP, rare loot) than any of the 3-5 branch quests that feed into it. The authoring logic seems reasonable — "big achievement deserves big reward" — but the player's experience is of uneven pacing rather than climactic celebration.

**Consequence:** The reward rhythm — the pattern of small, steady gains punctuated by occasional larger rewards — is the quest book's heartbeat. When the convergence node hoards the chapter's reward budget, the branches feel like a grind: the player is working toward the convergence without receiving adequate rewards along the way, and the convergence reward feels disconnected from their effort. This is particularly damaging in diamond_convergence because the player only traverses one branch at a time — they don't experience the "all paths completed" milestone until the very end, so the sparse branch rewards create a long drought before the convergence windfall. The MC百科 adventure design article's principle of "玩家在每个世界的收获都是正反馈的" (player gains in every world provide positive feedback) is violated: the branches lack positive feedback because their rewards are too sparse.

**Fix:** (1) Distribute the convergence node's excess rewards backward into the branch endpoints — the last quest of each branch before the convergence should receive a meaningful reward (not just the convergence node). (2) The convergence node itself should receive a symbolic reward (1 choice reward, a small XP bonus, or a cosmetic item) that celebrates the synthesis without creating a pacing cliff. (3) Apply the "reward per effort" principle: each branch quest should reward proportionally to its effort, and the convergence reward should be approximately equal to one branch-endpoint reward (not the sum of all branches). (4) If the convergence must have a large reward (e.g., it unlocks a new tier), frame it as a "gateway" reward (an item that enables new content) rather than a "windfall" reward (raw valuables) — gateway rewards don't disrupt pacing because they're invested rather than consumed.

**Source:** Phase 1 data analysis (diamond_convergence chapters show convergence-node reward spikes); player feedback on reward pacing in convergence topologies; MC百科 bbs thread-21004 (positive feedback principle — "玩家在每个世界的收获都是正反馈的").
**Cross-reference:** AP37 (Convergence Claustrophobia) for the bookkeeping dimension of convergence; AP36 (Reward-Type Roulette) for the related issue of reward-type consistency; PP13 (Reward-Type Contract) for the player expectation around reward delivery.

Tension with R13: When the convergence node is also the chapter capstone, resolve by making the capstone-convergence reward a gateway item (functional unlock, tool, or key) rather than a windfall (large quantity of raw materials). This satisfies R13's "capstone should feel significant" intent without creating the reward dump described by AP38.

Resolution: When both AP38 and R13 apply (convergence node = capstone), AP38's reward-pacing concern overrides R13's reward-size expectation — the resolution mechanism is a gateway reward that feels significant (satisfying R13) without being a windfall (avoiding AP38).

---

## AP39 — Flexible Mode Dependency Bypass (the phantom lock)

**Symptom:** A chapter using `progression_mode: "flexible"` has quests that appear unlocked and completable even though the player hasn't finished the prerequisites that should gate them. In diamond_convergence topologies, this is especially dangerous: if one branch's dependency check is bypassed due to the flexible mode's relaxed ordering, the convergence node at the diamond's center may unlock prematurely — before all paths are actually complete. The player sees the convergence quest as available, completes it, and skips the intended multi-path synthesis entirely.

**Root cause:** When `progression_mode` is set to `flexible` at the chapter or group level, FTB Quests relaxes the dependency checking logic. In flexible mode, quests can be completed in any order as long as their direct dependencies are satisfied — but certain edge cases in the dependency resolution can cause indirect dependencies to be treated as satisfied when they shouldn't be. In diamond_convergence topologies, this creates a specific failure: if Branch A depends on Quest A1 → A2 → A3, and Branch B depends on Quest B1 → B2 → B3, and the convergence depends on A3 and B3, the flexible mode may allow the convergence to unlock when only A3 is complete (because B3's dependency chain is evaluated differently in flexible mode). This is a mod-level behavior rather than a pack-authoring error, but it's triggered more frequently in diamond_convergence because of the multiple parallel dependency chains.

**Consequence:** The convergence node — which is supposed to be the chapter's climactic synthesis requiring all paths — unlocks prematurely. The player completes it without having experienced all the prerequisite content, undermining the diamond_convergence topology's core value proposition (parallel paths converging at a meaningful checkpoint). If the convergence quest rewards a key progression item (new tier access, rare crafting component), the player effectively skips a significant portion of the chapter's content. This is the flexible-mode equivalent of AP30 (Skyblock Resource Bottleneck): both create unintended shortcuts through the progression, but AP39 creates shortcuts by *relaxing* gates rather than by *blocking* paths.

**Fix:** (1) For diamond_convergence chapters using flexible mode, set `hide_quest_until_deps_visible: true` on the convergence quest — this ensures the player doesn't see the convergence node until ALL dependency paths are complete, preventing premature interaction even if the dependency check has edge cases. (2) Consider using `progression_mode: "linear"` on the convergence quest's parent group (even if the chapter is otherwise flexible) to enforce strict dependency ordering at the critical convergence point. (3) Add explicit cross-branch dependencies where narratively appropriate: if Branch B's final quest should require Branch A's midpoint quest, make that dependency explicit rather than relying on the convergence node to enforce it. (4) Test flexible-mode diamond_convergence chapters by completing only one branch and checking whether the convergence node is accessible — if it is, the dependency bypass is active and needs mitigation.

**Source:** GitHub FTBTeam/FTB-Quests issues (flexible mode dependency resolution edge cases); diamond_convergence topology analysis (multiple parallel dependency chains as trigger condition).
**Cross-reference:** AP37 (Convergence Claustrophobia) for the convergence-node design context; PP17 (Convergence Node as Soft Gate) for the correct usage of convergence nodes; AP2 (archive — Circular Dependency Deadlock) for the related concept of dependency resolution failures.

Priority: AP39 (functional correctness) overrides PP17 (visual preference) when both apply. If progression_mode is linear, prefer PP17's approach (visible convergence) as the bypass risk does not exist.

---

## AP40 — Version-Induced Layout Drift (the silent degradation)

**Symptom:** A chapter that looked perfect in the FTB Quests editor during authoring appears distorted after a mod version update. Node positions shift, spacing between quests collapses or expands unpredictably, and carefully arranged layouts — especially precise coordinate placements like compartment regions (MP47), dual-grid catalogs (MP69), or symmetric boss trees (MP53) — become visually disorganized. The player opens a chapter they've played before and finds it looks different, with nodes overlapping or spread too far apart. No one changed the quest config; the FTB Quests mod update did it silently.

**Root cause:** FTB Quests occasionally changes how it interprets node coordinates, grid scale, or auto-layout behavior between versions. When a pack updates its FTB Quests dependency (which happens regularly as packs track mod updates), the quest rendering engine may re-calculate node positions based on new defaults or updated coordinate interpretation logic. Layouts that relied on the previous version's behavior — particularly those using auto-layout features, default grid_scale values, or floating-point coordinates that were rounded differently in the old version — drift from their intended appearance. This is a tool-level issue rather than a pack-authoring error, but it has design-level consequences.

The百度贴吧 player report ("原来挺清楚的一滑就能看见全部任务，现在变得又挤又要") directly documents this: the layout degraded after a version update, and the player had no understanding of why or how to fix it.

**Consequence:** Layout drift is invisible to the pack author until a player reports it, because the author typically tests with a specific FTB Quests version. Once the pack is distributed and players use different FTB Quests versions (or the pack updates its mod dependencies), the layout silently degrades. This is particularly devastating for packs that invested significant effort in precise coordinate placement — the more carefully the layout was designed, the more visible the degradation. The player experience shifts from "this chapter is beautifully organized" to "this chapter is a mess" without any authoring change, eroding trust in the pack's quality. PP19 (Spacing Collapse After Version Update) documents the player-facing symptom; AP40 documents the systemic cause and defense strategy.

**Fix:** (1) Always use precise x/y coordinate values for every quest — never rely on auto-layout or default coordinate assignment. Precise coordinates are the strongest defense against version drift because they give the rendering engine no room for reinterpretation. (2) Set `grid_scale` explicitly at the chapter level to lock the overall density, preventing the rendering engine from using a different default scale after a version update. (3) After every FTB Quests version update (whether the pack updates its dependency or the player's client updates), visually audit at least 3 representative chapters (small, medium, large) for layout drift. (4) For packs targeting a wide range of FTB Quests versions, test with both the oldest and newest supported versions to identify coordinate interpretation differences. (5) Document the target FTB Quests version in the pack's metadata so players know which version the layout was designed for.

**Source:** 百度贴吧 FTB Quests 玩家反馈（"原来挺清楚的一滑就能看见全部任务，现在变得又挤又要"）；PP19 (Spacing Collapse After Version Update) for the player-experience dimension.
**Cross-reference:** PP19 (Spacing Collapse After Version Update) for the player-facing symptom; AP24 (Spacing Inconsistency) for the visual consequence of degraded spacing; topology-coordinates.md for the precise coordinate values that serve as defense; MP47 (Compartment Region Layout) and MP69 (Dual-Grid Convergence Catalog) for the layout types most vulnerable to version drift.

Circular causality: AP40 and PP20 (repetition fatigue) form a feedback loop. Packs with more layout investment (higher pattern complexity) have more to lose from version drift. The severity depends on which pattern the pack uses — Monolithic packs (Pattern 1) lose less from drift than Quadrant (Pattern 3) or Compartment (Pattern 5) packs with precise coordinate grids.

---

## Cycle 15 Cross-Reference Additions

| Anti-Pattern | Related Archive APs | Related MPs | Topology Layer |
|---|---|---|---|
| AP38 Convergence Over-Reward | AP8 (Reward Inflation) | MP66 (Extreme Fan-In), PP13 | Reward economy (convergence pacing) |
| AP39 Flexible Mode Dependency Bypass | AP2 (Circular Dependency) | PP17 (Soft Gate) | Dependency resolution (flexible mode) |
| AP40 Version-Induced Layout Drift | AP24 (Spacing Inconsistency) | MP47 (Compartment), MP69 (Dual-Grid), PP19 | Coordinate precision (version stability) |

---

## Cycle 15 Source Additions

25. **MC百科 post/4382** — "FTB任务设计进阶教程" (Advanced FTB Quests design tutorial). Chinese community article covering quest line design principles including "连线风格要相近，不要让人的第一印象是乱" (keep connection line styles similar, don't let the first impression be chaos) and "不要让玩家在同一个地方进行多次必须的重复操作" (don't make players repeat mandatory operations in the same place). Core reference for PP15 and PP20.

26. **FTB Forums discussions** — Player feedback threads discussing ideal quest line models. Players describe the ideal as "guided but not linear" — wanting clear main progression direction with branching exploration freedom. Core reference for PP16.

27. **GitHub FTBTeam/FTB-Quests "Better Dependency Lines Settings"** — Issue tracking improved dependency line rendering (Fixed in Dev). Confirms that tool-level line quality constrains topology choice. Core reference for PP18.

28. **FTB Docs — Quest Book Tips & Tricks** — Official FTB Quests player documentation. Warns that auto-pinning "may cause the list of quests to go off the screen" in large modpacks, providing a system-level acknowledgment that quest count creates UI overflow. Also documents the linked-quest navigation feature (clicking the link icon to jump between quest copies) and the dependency arrow navigation (left arrow for prerequisites, right arrow for dependents). Phase 2 Cycle 16 source for AP28 mega-chapter UI overflow. https://docs.feed-the-beast.com/mod-docs/mods/suite/Quests/Player/Questbook/Tips_Tricks/

---

## Cycle 17 Phase 2 Anti-Patterns — Presentation Pacing Specific (AP41)

This anti-pattern emerges from the Cycle 17 Phase 2 cross-validation research that searched 10+ platforms for player feedback on quest chapter structure. It addresses the failure mode where a chapter's quest presentation lacks internal pacing hierarchy — all quests appear simultaneously accessible without a clear main-path vs side-content distinction — even when the chapter's total quest count is moderate (30-80 quests, well below the AP28 mega-chapter threshold).

---

## AP41 — Flat Presentation Hierarchy (the "throws everything at you" chapter)

**Symptom:** The player opens a chapter and sees all quests at once with no visual distinction between the main progression path and side content. Every quest has the same size (1.0), the same shape (chapter default), and no `hide_until_deps_visible` gating. The chapter may have only 30-50 quests — not enough to trigger AP28 (Mega-Chapter) — but the player still feels overwhelmed because they cannot tell which quest to do first, which is the main path, and which is optional. The player's reaction, as documented in Craftoria #231, is that the chapter "kinda just throws everything at you" rather than guiding them through the process.

**Root cause:** The pack author made all quests visible and accessible from the start, treating the chapter as a flat list of objectives rather than a directed progression experience. In FTB Quests config terms, the chapter has no `hide_until_deps_visible: true` on any quest, all quests use the default `size: 1.0`, the `default_quest_shape` applies uniformly without distinctive shapes for the main path, and there are no decorative images or visual markers to signal "start here" or "this is the main path." The dependency graph may be correct (quests do unlock in order), but the visual presentation doesn't communicate the hierarchy — the player sees the entire chapter's content on first open and can't parse the intended sequence.

This differs from AP28 (Mega-Chapter Without Structural Compensation) in scale and mechanism: AP28 concerns 150+ quest chapters that are too large to navigate without structural aids; AP41 concerns moderate-size chapters (30-80 quests) that would be perfectly navigable if the author had applied progressive visual hierarchy. It also differs from AP23 (Topology Mixing): AP23 concerns structural incoherence from mixing topology types, while AP41 concerns flat visual hierarchy within a single topology type.

**Consequence:** The player's first impression of the chapter is confusion rather than curiosity. Instead of seeing a clear starting point and feeling motivated to explore, they see a wall of equally-weighted quest icons and feel overwhelmed. The MC百科 post/2494 tutorial captures this: poor layout causes "血压升高" (blood pressure to rise). The player may skip the chapter entirely and come back later (losing the intended pacing), or they may attempt quests in the wrong order (encountering difficulty spikes because they started a side quest before the main-path prerequisite). FTB Forums discussions confirm that players describe the ideal quest experience as "guided but not linear" — they want clear main-path direction with branching exploration freedom. A flat hierarchy removes both the guidance and the branching structure, leaving an undifferentiated blob.

The Craftoria Powah chapter complaint is the canonical example: the player proposed restructuring the Powah quests to be more linear, specifically requesting that the chapter "guide the player through the process" rather than presenting all content simultaneously. The player identified that the reactor progression in particular suffered — "you go through 3 tiers of reactors with no relevant quest rewards" — demonstrating that flat presentation combines with reward pacing issues to create a compounded negative experience.

**Fix:** (1) Apply size hierarchy to establish a visual main path: the chapter root and 2-3 key milestone quests should be size 1.5-2.0, while side content stays at 1.0. (2) Use `hide_until_deps_visible: true` on at least the second half of the chapter's quests, so the player initially sees only the starting quests and discovers new content as they progress. (3) Assign a distinctive shape to main-path quests (e.g., gear for hubs, diamond for convergence milestones) while keeping side content on the default shape. (4) Add at least one decorative image or text quest at the chapter start that serves as a "table of contents" — telling the player what the chapter covers and where to begin. (5) For chapters covering a mod with clear progression tiers (like Powah's reactor tiers), structure the chapter as a series of tier-gated sections where each tier's quests are hidden until the previous tier's milestone is complete — this creates a natural pacing rhythm even within a non-linear chapter.

**Source:** TeamAOF/Craftoria #231 (player u/weirdchildren — "I feel like the quests in the Powah tab kinda just throws everything at you"; proposed restructuring to linear path with guided progression); MC百科 post/2494 (poor layout causes "血压升高"; linear layouts should follow "长度相等、对称等原则"); FTB Forums discussions (ideal quest experience is "guided but not linear").
**Cross-reference:** AP28 (Mega-Chapter Without Structural Compensation) for the larger-scale variant; AP23 (Topology Mixing) for the structural incoherence variant; PP16 (Guided Non-Linearity) for the correct design principle; MP73 (Sub-Region Decomposition) for the spatial organization solution in larger chapters; R41 (Early-Game Flexible Mode) for the related principle of easing players into progression structure.

---

## Cycle 17 Cross-Reference Additions

| Anti-Pattern | Related Archive APs | Related MPs | Topology Layer |
|---|---|---|---|
| AP41 Flat Presentation Hierarchy | AP28 (Mega-Chapter), AP23 (Topology Mixing) | MP73 (Sub-Region), PP16 (Guided Non-Linearity) | Presentation pacing (visual hierarchy) |

---

## Cycle 17 Source Additions

29. **TeamAOF/Craftoria #231** — "Restructure Powah quests to be more linear." Player feedback that the Powah chapter "kinda just throws everything at you" with specific complaint about reactor tier progression having no relevant quest rewards. Proposed fix: restructure to linear path that "guides the player through the process." Core source for AP41. https://github.com/TeamAOF/Craftoria/issues/231

30. **MC百科 post/2494** — "1.16的详细FTB任务教程" (re-validated in Phase 2 Cycle 17). Chinese community tutorial with explicit layout design principles: poor layout causes "血压升高" (blood pressure rise), linear layouts should follow "长度相等、对称等原则" (equal-length, symmetry principles), and abstract/stream-of-consciousness layouts should hide dependency lines entirely. The author thanks the community for helping improve the guide and credits practical experience working on the "DTD" modpack. Re-validation confirms these principles remain the most cited Chinese-language quest layout guidance. https://www.mcmod.cn/post/2494.html

31. **MC百科 post/1015** — "[CrT-Game Stages]0-介绍篇" (CraftTweaker + Game Stages introduction tutorial). Chinese tutorial documenting the Game Stages ecosystem for multi-layer progression enforcement. Lists 7+ stage-locking extensions: Recipe Stages (locks crafting), Dimension Stages (blocks world travel), Item Stages (hides item usage/viewing), Mob Stages (prevents mob spawning), Ore Stages (replaces ore blocks), TinkerStages (limits tool creation), Waila Stages (hides UI overlays). Recommends using "进度或者是CrT来控制玩家的阶段" (advancements or CraftTweaker) rather than manual command assignment. Phase 2 Cycle 17 source for R101 config validation. https://www.mcmod.cn/post/1015.html

32. **MC百科 post/2997** — "物品阶段不止于物品阶段！" (Item Stages goes beyond item stages!). Advanced Chinese tutorial on Item Stages mod, documenting ability to lock enchantments by level, fluid+bucket pairs, and recipe IDs. Demonstrates the granularity of the Game Stages ecosystem for expert pack multi-layer enforcement. Phase 2 Cycle 17 source for R101. https://www.mcmod.cn/post/2997.html

33. **MC百科 post/1956** — "1.12.2使用CrT来控制物品和维度游戏阶段方法" (Using CrT to control item and dimension game stages). Chinese tutorial on integrating CraftTweaker with Game Stages for item and dimension locking. Phase 2 Cycle 17 supplementary source for R101. https://www.mcmod.cn/post/1956.html

34. **No Flesh Within Chest (脆骨症) MC百科 page** — Chinese adventure/RPG pack with 96% positive rating (313 red votes vs 12 black), 273.81万 total views. Quest book guided progression with "数十名强大的BOSS" (dozens of powerful bosses). Player engagement focuses heavily on build optimization (1507亿 DPS showcases, organ system builds) rather than quest book structure commentary. Phase 2 Cycle 17 source for Lesson 90 (boss-catalog validation). https://www.mcmod.cn/modpack/722.html

---

## Cycle 18 Phase 2 Anti-Patterns — Progression Integrity (AP42)

This anti-pattern emerges from the Cycle 18 Phase 2 cross-validation research that searched 10+ platforms for player feedback on quest progression integrity. It addresses the failure mode where vanilla Minecraft villager trading mechanics allow players to acquire quest-required items without following the intended progression path, effectively bypassing the quest book's gating logic.

---

## AP42 — Villager Trading Hall Bypass (the progression side door)

**Symptom:** A non-expert modpack's quest book requires the player to craft or obtain specific items (e.g., enchanted books, emerald-based goods, specific crops, or mob drops) to complete item-submission quests. However, the player can build a villager trading hall early in the game and acquire these same items through villager trades, bypassing the intended progression chain. The quest book considers the item submitted regardless of acquisition method, so the player "completes" the quest without engaging with the mod or recipe chain the quest was designed to teach. This is especially damaging when the bypassed quest gates access to subsequent chapters or key technologies.

**Root cause:** FTB Quests item-submission tasks check only whether the player possesses the required item, not how the item was acquired. In vanilla Minecraft, villagers can trade enchanted books (including high-level enchantments), emeralds, specific crops (farmer villagers), glass (cartographer villagers), and other items that overlap with quest requirements. When a pack includes villager trading without implementing counter-measures (Game Stages gating, Recipe Stages, Item Stages, or custom villager trade modifications), the trading hall becomes a universal item source that circumvents the quest book's intended progression. The pack author designed the quest dependencies assuming the player would follow the crafting chain, but the FTB Quests task system has no mechanism to enforce *how* an item was obtained — only *whether* it was obtained.

This differs from AP12 (Quest Reward Economy Inflation) in mechanism: AP12 concerns rewards being too generous, while AP42 concerns an *external* game mechanic (villager trading) providing quest-required items through an unintended path. It also differs from general "cheese" strategies because villager trading is a legitimate vanilla mechanic, not a bug or exploit — the player isn't cheating, they're using an available system that the pack author failed to account for.

**Consequence:** The player's progression experience becomes hollow. Instead of learning the Create mod's mechanical crafting system (because the quest required a specific gear), the player simply trades with a librarian villager for the enchanted book that the Create chapter's prerequisite required. Instead of building the Farmer's Delight cooking station (because the quest required a specific meal), the player buys it from a farmer villager. The quest book's pedagogical intent — teaching the player how to use the mod — is defeated. The MC百科 post/2494 tutorial emphasizes that quest progression should be "更直接、简化但旨在复杂" (more direct, simplified but intentionally complex), meaning the complexity should come from engaging with the mod's systems, not from finding alternative acquisition paths. When villager trading provides a shortcut, the "intended complexity" is lost.

The problem is amplified in kitchen-sink packs that include both villager-heavy mods (like FTB Team's own quest-dependent packs) and collection-focused chapters (like Mystical Agriculture). A player who builds a max-level trading hall can often acquire the seeds, enchanted books, or specialty items that the Mystical Agriculture chapter requires, without ever building the crop farm infrastructure the chapter was designed to teach. The existence of multiple villager-trading management mods (SimpleVillagers, VillagerTradeFix, Infinite Trading, TradeTweaks, custom villager trading datapacks) demonstrates that the community recognizes villager trading as a system that needs active management — yet pack authors frequently forget to configure villager trades to match their quest progression design.

**Fix:** (1) Use Game Stages or Recipe Stages to lock villager professions or specific trades behind quest progression milestones — this ensures the trading hall can only provide items the player has already earned the right to access. (2) Configure custom villager trades via datapack or mod (e.g., the Custom Villager Trades mod or datapack-based trade modification) to remove or modify trades that would provide quest-required items prematurely. (3) For item-submission quests where acquisition method matters, add a text description or observation task that requires the player to demonstrate engagement with the crafting process (e.g., "craft this item using the Create mod's mechanical press" as a prerequisite observation task before the item-submission quest unlocks). (4) In expert packs, use Item Stages to hide villager trade items from the player's inventory until the appropriate progression stage is reached. (5) At minimum, add a text quest at the start of the pack warning players that villager trading may bypass intended progression and recommending they avoid trading halls until they've completed the relevant quest chapters — this is the lowest-effort fix but also the least effective, as it relies on player self-restraint.

**Source:** Phase 2 Cycle 18 cross-platform search (MC百科, Bilibili, Reddit, CurseForge, GitHub FTBTeam). No single player complaint was found specifically using the term "villager trading bypass," but the pattern is strongly implied by: (a) the existence of 5+ villager-trading management mods in the ecosystem (SimpleVillagers, VillagerTradeFix, TradeTweaks, etc.), suggesting the community recognizes trading as a progression-relevant system; (b) MC百科 post/1015's Game Stages tutorial, which explicitly documents Item Stages as a mechanism to "hide item usage/viewing" — implying pack authors need this capability precisely because vanilla acquisition paths can bypass intended progression; (c) the Engineer's Life 2 MC百科 description emphasizing "更直接、简化但旨在复杂的进程" (more direct, simplified but intentionally complex progression) — the "intended complexity" is defeated when alternative acquisition paths exist; (d) AP12 (Quest Reward Economy Inflation) and PP11 (Progression Gate Integrity) establish the principle that quest progression integrity depends on controlling item access, and villager trading is the most common uncontrolled access path in non-expert packs.
**Cross-reference:** AP12 (Quest Reward Economy Inflation) for the reward-side variant of progression integrity failure; PP11 (Progression Gate Integrity) for the general principle; R101 (Game Stages Config Validation) for the enforcement mechanism; MC百科 post/1015 for Game Stages as the canonical solution; MP75 (Extreme Dependency Line Suppression) for a different kind of visual complexity management that also requires deliberate author intervention.

---

## Cycle 18 Phase 2 Cross-Reference Additions

| Anti-Pattern | Related Archive APs | Related MPs | Topology Layer |
|---|---|---|---|
| AP42 Villager Trading Bypass | AP12 (Reward Economy Inflation) | MP75 (Dep Line Suppression), PP11 (Gate Integrity) | Progression integrity (item acquisition path) |

---

## Cycle 18 Phase 2 Source Additions

35. **MC百科 post/5840** — "1.12.2超详细的创建ftb任务介绍" (Ultra-detailed FTB Quests creation guide for 1.12.2). Chinese community tutorial documenting the "隐藏相关性行" (hide correlation lines) feature for hiding quest guide lines, and the "默认任务模板" (default quest template) system for controlling group-level shape settings. Confirms that hiding dependency lines is a documented author technique. Phase 2 Cycle 18 source for MP75 validation. https://www.mcmod.cn/post/5840.html

36. **MC百科 post/2494** (Phase 2 Cycle 18 re-validation) — Re-read for MP74/MP75/MP72 validation. The tutorial's explicit mention of "隐藏前置连线" (hide prerequisite connection lines) and the recommendation to hide lines for "意识流" (stream-of-consciousness) layouts provides the strongest Chinese-community validation for MP75's mechanism. The total absence of any mention of custom shape textures (despite covering custom images, themes, and standard shapes) provides validated-by-absence evidence for MP74's extreme rarity. The absence of tree-with-capstone convergence from the layout strategy list (linear, spiral, stream-of-consciousness are covered) provides additional negative evidence for MP72's TeamAOF-only status. https://www.mcmod.cn/post/2494.html

37. **Engineer's Life 2 MC百科 page** — MC百科 modpack listing for Engineer's Life 2. Author describes the pack's progression philosophy as "更直接、简化但旨在复杂的进程" (more direct, simplified but intentionally complex progression), following the "KISS（保持简单、懒人）原则" (Keep It Simple, Stupid principle). Quest system includes "基于任务的进度系统，带有奖励和一些内容的解释" (task-based progression with rewards and content explanations). Minimal gating: "进度并没有被限制在某些东西后面...如果你有资源，你可以随时制作" (progression is not locked behind certain things... if you have the resources, you can craft anytime). This open-gating philosophy makes the pack vulnerable to AP42 (villager trading bypass) because the author explicitly chose not to enforce progression locks. Phase 2 Cycle 18 source for AP42 and Lesson 121. https://www.mcmod.cn/modpack/191.html

38. **MC百科 post/5450** — "[FTBQ]1.20.1+如何在FTBQ任务面板添加自定义图片" (How to add custom images to FTB Quests panel in 1.20.1+). Chinese tutorial covering custom image addition via resource pack method. Author explicitly warns against modifying the mod jar directly ("实测直接在源mod文件中添加内容会导致PCL2无法识别mod文件"). Covers custom decorative images but does NOT mention custom shape textures. Phase 2 Cycle 18 negative evidence source for MP74. https://www.mcmod.cn/post/5450.html

39. **MC百科 post/5137** — "如何更改FTB任务的主题和背景" (How to change FTB Quests themes and backgrounds). Chinese tutorial covering the `.txt` theme file system for quest book visual customization. Documents chapter-specific backgrounds, quest view backgrounds, and border color customization. Warns that "一旦写错任何地方都有很大的概率使游戏崩溃" (any mistake has a high probability of crashing the game). Does NOT mention custom shape textures. Phase 2 Cycle 18 negative evidence source for MP74. https://www.mcmod.cn/post/5137.html

---

## Cycle 18 Phase 3 Anti-Patterns — Author Process and Progression Coherence (AP43–AP46)

These anti-patterns emerge from the Cycle 18 Phase 3 research on author design philosophy and progression integrity. They address failure modes related to the author's development process, player overwhelm from mod choice, reward timing, and narrative coherence between quests.

---

## AP43 — Unplaytested Release (the "shipping without testing" pack)

**Symptom:** The pack has obvious progression issues in the first few chapters that would have been caught by even minimal author playtesting: broken crafting chains where a required item's recipe references a mod that isn't installed, tutorial quests that assume knowledge not yet taught, rewards that don't align with the next quest's requirements, and difficulty spikes that suggest the author never personally experienced the progression flow. Players encounter these issues within the first 1–2 hours and leave negative reviews citing the pack as "untested" or "broken."

**Root cause:** The author assembled the pack from mod lists and quest templates without personally playing through the quest line before release. The MC百科 post/4382 article captures the core principle: "不敢玩自己的整合包的作者一定不是一个好作者" (an author who doesn't dare play their own modpack is certainly not a good author), framing it as "己所不欲，勿施于人" (do not do unto others what you would not have them do unto you). The MC百科 post/6155 article independently states "作者应该亲自玩自己的整合包" (authors should personally play their own modpack). When authors skip this step, they rely on automated config checks (which catch syntax errors but not design issues) and player feedback (which comes too late to prevent the first-impression damage).

This differs from other anti-patterns because the root cause is not a design flaw in the pack's content but a process failure in the pack's development. The same pack, playtested by the author, would likely not have these issues because the author would experience the broken chains, confusing tutorials, and misaligned rewards firsthand.

**Consequence:** The pack's early player experience is catastrophic. Broken crafting chains strand the player without the ability to progress. Tutorial quests that skip foundational concepts leave the player confused about how the pack's mods work. Rewards that don't align with next steps make the quest book feel arbitrary rather than guiding. The combination of these issues creates a first impression that the pack was not designed with the player in mind, undermining trust in the author's other design decisions. R124 (Author Playtesting Requirement) formalizes the defense: the author must personally complete at least 60% of the quest line before initial release.

**Fix:** (1) Before release, the author must personally play through at least 60% of the quest line (aligning with R105's 60% accessibility principle), documenting any issues found. (2) Focus playtesting on the critical progression path (the primary spine), not side content — the first 3 chapters are the most important because they form the player's first impression. (3) After fixing issues found during playtesting, play through the fixed sections again to verify the fixes don't introduce new problems. (4) For large packs, recruit 2–3 beta testers to play through sections the author skipped, ensuring broader coverage.
**Source:** MC百科 post/4382 ("不敢玩自己的整合包的作者一定不是一个好作者", "己所不欲，勿施于人"); MC百科 post/6155 ("作者应该亲自玩自己的整合包").
**Cross-reference:** R124 (Author Playtesting Requirement), R105 (60% content accessibility), R32 (chapter QA coverage), Lesson 130 (playtesting as fundamental quality requirement).

---

## AP44 — Kitchen-Sink Overwhelm (the "too many mods, no direction" pack)

**Symptom:** The pack includes 100+ mods with quest chapters for many of them, but provides no clear indication of which mods the player should engage with first. The quest book presents all chapters as equally accessible from the start, with no visual hierarchy, no primary spine, and no guidance about which chapters are core progression vs. optional side content. The player opens the quest book and sees 15+ chapter tabs with no way to determine which one to click first. The MC百科 post/6155 article identifies this as the primary failure mode of "水槽包" (kitchen-sink packs): "流程和引导不够明晰" (flow and guidance are not clear enough).

**Root cause:** The pack author added quest chapters for every mod in the pack without establishing a primary progression direction. Each chapter is individually well-designed (the quests within it make sense), but the pack lacks a meta-level structure that tells the player how the chapters relate to each other. The author assumed that players would naturally identify the progression order based on mod complexity (simple mods first, complex mods later), but this assumption fails when the player is unfamiliar with the mods.

This differs from AP41 (Flat Presentation Hierarchy) in scope: AP41 concerns flat hierarchy within a single chapter (all quests look the same), while AP44 concerns flat hierarchy across the entire quest book (all chapters look the same). It also differs from AP28 (Mega-Chapter) in that AP44 is about too many chapters, not too many quests within one chapter.

**Consequence:** The player feels overwhelmed by choice and paralyzed by the number of options. Instead of feeling curious about the mods, they feel anxious about making the wrong choice. Many players respond by following an external guide rather than the quest book (undermining the quest book's purpose), or by quitting the pack entirely. The MC百科 post/6155 article notes that kitchen-sink packs with this problem cause players to "因为流程和引导不够明晰而退坑" (quit because flow and guidance are not clear enough), which is a preventable failure.

**Fix:** (1) Establish a primary progression spine: identify the 3–5 chapters that form the core progression and visually distinguish them from optional chapters (larger chapter icons, distinctive colors, or a "Main" vs "Side" label). (2) The first quest in the pack should explicitly tell the player which chapter to start with and why. (3) Use `hide_until_deps_visible: true` on chapters that should not be accessible until the player has completed earlier chapters. (4) Add a "table of contents" text quest at the start that lists the primary progression order and briefly describes each main chapter. (5) R122 (Kitchen-Sink Flow Clarity) formalizes this defense.
**Source:** MC百科 post/6155 ("水槽包" failure from "流程和引导不够明晰", players quitting due to unclear direction); MC百科 post/4382 (consistent visual styles for task branches).
**Cross-reference:** R122 (Kitchen-Sink Flow Clarity), AP41 (Flat Presentation Hierarchy), AP28 (Mega-Chapter), R105 (60% content accessibility), R41 (early-game flexible progression).

---

## AP45 — Quest Reward Timing Mismatch (the "reward that arrives too late or too early" quest)

**Symptom:** A quest rewards the player with an item that is either (a) already obsolete because the player has progressed past the point where it would be useful, or (b) not yet usable because the player hasn't reached the progression stage where the item becomes relevant. In case (a), the reward feels like a consolation prize — "I already have a better version of this." In case (b), the reward feels like clutter — "I can't use this yet, and by the time I can, I'll have found a better one." Both cases undermine the quest book's credibility as a progression guide: if the quest book can't even time its rewards correctly, why should the player trust its guidance?

**Root cause:** The quest author designed rewards based on what items are thematically related to the quest's content, without considering the player's progression state at the moment of quest completion. A quest that teaches the Create mod's mechanical press might reward a hand crank (useless if the player already built a mechanical press to complete the quest) or a precision mechanism (useless if the player hasn't unlocked the tech tier where precision mechanisms are craftable). The reward's thematic relevance is correct, but its temporal relevance is wrong.

This differs from AP12 (Quest Reward Economy Inflation) in mechanism: AP12 concerns rewards being too generous (inflation), while AP45 concerns rewards being temporally misaligned (arriving at the wrong progression point). The item might be perfectly balanced in value — it's just delivered at the wrong time.

**Consequence:** The player learns to ignore quest rewards, which undermines the entire reward economy. If rewards are consistently mistimed, the player stops checking what the quest gives and focuses solely on the quest's completion requirements. This transforms the quest book from a rewarding progression guide into a pure checklist — the player completes quests for the dependency unlock, not for the reward. The MC百科 post/4382 article's principle of providing "持续的正反馈" (continuous positive feedback) is violated: mistimed rewards break the positive feedback loop because the player doesn't feel rewarded.

**Fix:** (1) For each quest reward, ask: "At the moment the player completes this quest, is this item immediately useful, immediately preparatory, or neither?" If neither, replace the reward. (2) Use the reward-to-dependent bridge pattern (R10): the reward should be a component or tool that the player needs for the next quest in the dependency chain. (3) For rewards that are preparatory (useful later), add a quest description note explaining when and how the item will be useful — this converts "clutter" into "investment." (4) Test reward timing during playtesting (R124): the author should personally receive each reward and evaluate whether it feels useful at that moment.
**Source:** MC百科 post/4382 ("持续的正反馈" principle, reward balance); TeamAOF/Craftoria #231 (player complaint: "you go through 3 tiers of reactors with no relevant quest rewards" — the reward arrives after the player has already moved past the tier).
**Cross-reference:** R10 (reward-to-dependent bridge), R12 (reward value progression), AP12 (Quest Reward Economy Inflation), R124 (author playtesting), R45 (reward guidance bridging).

---

## AP46 — Quest Narrative Disconnection (the "series of unrelated tasks" chain)

**Symptom:** A quest chain's individual quests lack narrative connection to each other. Each quest feels like an isolated task: "craft this item," "kill this mob," "visit this place" — with no story, context, or explanation for why the player is doing these things in this order. The player completes the quests mechanically but feels no engagement with the progression. The MC百科 post/4382 article warns about this when it discusses the importance of quest descriptions: "什么提示要详细？什么提示要神秘？这都要靠你的经验" (what hints should be detailed? what hints should be mysterious? this depends on your experience) — implying that quest descriptions are a craft, not an afterthought.

**Root cause:** The pack author focused on the mechanical dependency structure (which items gate which quests) without investing in the narrative layer that connects quests into a coherent journey. This is particularly common in packs that prioritize technical accuracy (correct crafting chains, correct tool tiers) over player experience (why am I doing this? what's the story?). The Nova Engineering pack demonstrates the opposite approach: their "原创剧情化研究系统，贯穿发展全线" (original narrative-driven research system threading through the entire progression) ensures every task has narrative context that connects it to the overall story.

This differs from AP5 (Empty Quest Description) in scope: AP5 concerns individual quests with blank descriptions, while AP46 concerns chains of quests where even individually well-described quests lack narrative connection to each other. The problem is the gaps between quests, not the quests themselves.

**Consequence:** The player feels like they're checking items off a grocery list rather than progressing through an adventure. Without narrative connection, the quest chain's pedagogical intent is weakened: the player learns how to craft items but doesn't understand why those items matter in the pack's broader context. This leads to the "why should I care?" reaction that causes players to skip quest descriptions entirely and focus only on the mechanical requirements. R120 (Narrative-Driven Research Progression) formalizes the defense: a narrative thread connecting all progression tasks keeps the player engaged.

**Fix:** (1) Each quest's description should reference the previous quest's outcome ("Now that you've built the mechanical press...") and preview the next quest's purpose ("...which you'll need for the next step: creating precision mechanisms"). (2) At the chapter level, add a chapter introduction quest that establishes the narrative arc for the entire chapter. (3) Use text quests as narrative connectors between major quest milestones — these cost nothing to implement but provide crucial context. (4) For expert packs, consider Nova Engineering's approach: a narrative research system where each task has story context embedded in the research description.
**Source:** MC百科 post/4382 (quest description craft, "什么提示要详细？什么提示要神秘？"); Nova Engineering MC百科 modpack/784 ("原创剧情化研究系统，贯穿发展全线" as the positive example); MC百科 post/6155 (personal character growth as narrative driver for adventure packs).
**Cross-reference:** R120 (Narrative-Driven Research Progression), AP5 (Empty Quest Description), R82 (backward design, book-level arc), R18 (description coverage).

---

## AP47 — R59 Double-Axis Viewport Violation (the "chapter that doesn't fit on any screen" problem)

**Symptom:** A chapter's bounding box exceeds the R59 hard clamp (35 units) on BOTH the width and height axes simultaneously. The player cannot view the entire chapter at any reasonable zoom level — they must scroll both horizontally and vertically to navigate, creating a disorienting experience where the quest book loses its function as a visual map. MC-Eternal-Eternally's irons_spells chapter spans 39×44 units (1716 square units of viewport area), making it the largest chapter by area in the 72-pack dataset.

**Root cause:** The pack author added content incrementally without monitoring the chapter's growing bounding box. Each new branch extended the layout in whichever direction had space, eventually exceeding the viewport on both axes. This is particularly common in chapters that cover a large mod (like Iron's Spells with 630 quests) where the author resists splitting into sub-chapters because the mod is a single cohesive system.

**Consequence:** Players lose spatial orientation within the chapter. When a chapter fits on one screen, players can see the overall structure at a glance — where they've been, where they're going, and what branches are available. When the chapter exceeds the viewport on both axes, this spatial overview becomes impossible. Players must rely entirely on the dependency graph (scrolling from quest to quest) rather than the visual layout, defeating the purpose of the quest book as a visual progression map.

**Fix:** (1) Monitor chapter bounding box during development — warn at 30 units on either axis (R59 warning threshold), hard-clamp at 35 units. (2) For large-mod chapters (>200 quests), split into sub-chapters using MP73 (Sub-Region Decomposition): identify natural content breaks (e.g., spell schools, equipment tiers, boss progression) and create separate chapters for each sub-region. (3) If splitting is not feasible, use MP77 (Sub-1.0 Size Compression) to reduce the viewport footprint — size 0.5-0.7 can halve the effective bounding box. (4) Add decorative images as landmarks to help players orient within the large layout.
**Source:** MC-Eternal-Eternally irons_spells (Case 70, 630 quests, 39×44 units — exceeds R59 hard clamp on both axes). This is the first chapter in the dataset to violate R59 on both dimensions simultaneously. Previous R59 violators (EL2 first_steps at 39.5 wide, FTB Evolution create at 30 wide) only exceeded on one axis.

**Phase 2 Cycle 19 indirect evidence:** GitHub FTBTeam/FTB-Mods-Issues #2059, a feature request for "simultaneous 2D scrolling" in the quest tree UI, provides indirect validation of the viewport navigation problem that AP47 describes. The issue author explicitly states that "allowing simultaneous 2D scrolling in the quest tree UI would allow much easier and more natural navigation" without "having to hold left click and drag or use shift + scroll." FTB dev MichaelHillcox acknowledged this as "a fair point" for trackpad users, confirming that the current single-axis scrolling limitation is a real usability concern. While the issue does not cite any specific chapter, the navigation problem it describes — difficulty panning across a 2D quest layout — is precisely the player experience when a chapter exceeds the viewport on both axes (as in AP47). Additionally, GitHub FTBTeam/FTB-Mods-Issues #1909 notes that pinned quest lists "can get pretty big and that then takes over most of the screen" and "covers the map," requesting keybinds to hide overlays and "fold down" locked tasks to "limit visual clutter." These requests confirm that screen space management is a recognized concern in large quest books, and that players experience the quest book's spatial constraints as a real friction point. No player feedback specifically mentioning MCEE irons_spells was found on any platform (MC百科, Bilibili, Reddit, CurseForge, GitHub).
**Cross-reference:** R59 (Bounding Box Viewport Fit), MP73 (Sub-Region Decomposition), MP77 (Sub-1.0 Size Compression), AP28 (Mega-Chapter).

---

## Cycle 18 Phase 3 Cross-Reference Additions

| Anti-Pattern | Related Archive APs | Related MPs | Topology Layer |
|---|---|---|---|
| AP43 Unplaytested Release | AP5 (Empty Description) | R124 (Playtesting), R32 (QA Coverage) | Author process (quality assurance) |
| AP44 Kitchen-Sink Overwhelm | AP41 (Flat Presentation), AP28 (Mega-Chapter) | R122 (Flow Clarity), R105 (60% Accessibility) | Book-level navigation (chapter hierarchy) |
| AP45 Reward Timing Mismatch | AP12 (Reward Inflation) | R10 (Reward Bridge), R12 (Value Progression) | Quest reward (temporal alignment) |
| AP46 Quest Narrative Disconnection | AP5 (Empty Description) | R120 (Narrative Research), R82 (Backward Design) | Quest chain (narrative coherence) |

---

## Cycle 18 Phase 3 Source Additions

40. **MC百科 post/6155** — "关于制作冒险类整合包的一些心得分享" (Sharing insights on making adventure modpacks). Chinese community article covering adventure pack design philosophy: difficulty progression ("难度递进"), equipment tier bridging (previous tier's best gear matches current tier's basic mobs), kitchen-sink failure analysis ("水槽包" failure from "流程和引导不够明晰"), two methods for stage management (deep mod modification vs. thematic phase division), and the 60% content experience target. Core source for R121, R122, AP43, AP44. https://www.mcmod.cn/post/6155.html

41. **MC百科 post/4382** (Phase 3 Cycle 18 re-validation) — Re-read for author design philosophy principles. Key quotes re-validated: "不敢玩自己的整合包的作者一定不是一个好作者" (playtesting principle), "己所不欲，勿施于人" (golden rule), "弱锁" (weak lock philosophy), four-tier mob classification, equipment distribution ("两头少，中间多"), and consistent visual styles for task branches. Core source for R124, Tension 10, AP43, AP46. https://www.mcmod.cn/post/4382.html

42. **Nova Engineering MC百科 page** — MC百科 modpack listing for Nova Engineering: World (新星工程：世界). High-difficulty expert tech pack with 200+ mods, 100+ original multiblock machines, and a custom Tech Level system (1.0–14.0, five eras). Features a "原创剧情化研究系统，贯穿发展全线" (original narrative-driven research system). HyperNet wireless computing network avoids "漫长的等待" and "大量无用的前置研究". No anti-cheat mechanisms. Playtime 150–450 hours. Core source for R119, R120, Tension 11. https://www.mcmod.cn/modpack/784.html

43. **klpbbs.com thread-130537** — "[1.20.4-1.2.5]魔改整合包常用模组（226Mods）" (Common mods for expert modpacks). Comprehensive Chinese community list of 226 mods commonly used in expert modpacks, categorized by function. Includes Game Stages ecosystem (Item Stages, Recipe Stages, Dimension Stages, Ore Stages, TinkerStages), Tool Progression, Skillable/Reskillable, Triumph (custom advancements), Profession Lock, Custom NPCs, FTB Money, and Oxygen series for custom economies. Core source for R117 (Game Stages + Profession Lock as trading bypass defense). https://klpbbs.com/thread-130537-1-1.html

44. **Profession Lock MC百科 page** — MC百科 mod listing for Profession Lock. Prevents villager profession cycling by permanently locking a villager's profession and trades after workstation claiming. Author states the exploit "打破了沉浸感，让游戏变得更加简单" (breaks immersion and makes the game simpler). Fixes vanilla bugs MC-177505 and MC-146891. Core source for R117 (villager profession locking as anti-exploit defense). https://www.mcmod.cn/class/9288.html

45. **MC百科 thread-21004** (Phase 3 Cycle 18 re-validation) — Re-read for Vazkii's modpack design philosophy. Key principles re-validated: dimensional shifts as progression drivers, "一整条线" (single continuous line) for tech pack item elimination, four-tier mob classification, equipment distribution ("两头少，中间多"), crafting depth limit (1–2 nested layers), and continuous positive feedback. Core source for R121 (equipment tier transition), Tension 10 (streamlining vs. variety). https://bbs.mcmod.cn/thread-21004-1-1.html

---

## Phase 2 Cycle 19 Cross-Reference Additions

| Anti-Pattern | Related Archive APs | Related MPs | Topology Layer |
|---|---|---|---|
| AP47 R59 Double-Axis Violation | AP28 (Mega-Chapter) | MP73 (Sub-Region), MP77 (Size Compression), R59 (Viewport Fit) | Chapter viewport (spatial constraint) |

---

## Phase 2 Cycle 19 Source Additions

46. **GitHub FTBTeam/FTB-Mods-Issues #2059** — "[Feature Request]: simultaneous 2D scrolling". User requests two-dimensional scrolling in the quest tree UI, stating "allowing simultaneous 2D scrolling in the quest tree UI would allow much easier and more natural navigation" without "having to hold left click and drag or use shift + scroll." FTB dev MichaelHillcox acknowledged the limitation as "a fair point" for trackpad users. Indirect validation for AP47 (R59 Double-Axis Violation): the navigation friction described in this issue is precisely the experience when a chapter exceeds the viewport on both axes. https://github.com/FTBTeam/FTB-Mods-Issues/issues/2059

47. **GitHub FTBTeam/FTB-Mods-Issues #1909** — "FTB Quests Mod suggestions for UI improvements". Detailed feature request covering pinned quest list overflow ("the list can get pretty big and that then takes over most of the screen", "covers the map"), requests for keybind to hide overlay, "fold down" locked tasks to "limit visual clutter", chapter flagging for pinned quests, and manual reordering of pinned tasks. Confirms screen space management as a recognized player concern in large quest books. Indirect validation for AP47 and MP77 (Sub-1.0 Size Compression). https://github.com/FTBTeam/FTB-Mods-Issues/issues/1909

48. **MC百科 post/2494** (Phase 2 Cycle 19 re-validation) — Re-read for quest size parameter documentation. Key quote confirmed: "大小：任务框的大小，默认为 1 ，为倍数关系" (size: quest frame dimensions, default is 1, in multiplier relationship). Layout warning confirmed: "如果你没有好好排版，那么也许玩家会血压升高" (if you don't lay out properly, players may get frustrated). Tutorial covers linear, spiral, and stream-of-consciousness (意识流) layouts. Core validation source for MP77 (size as configurable parameter) and MP75 (hide_dependency_lines as deliberate author technique). https://www.mcmod.cn/post/2494.html

49. **GitHub FTBTeam/FTB-Modpack-Issues #6447** — "List of Observations in FTB Evolution (WIP)". Detailed issue cataloging missing chapters, broken progression, misleading prerequisites, text errors, and reward bugs in FTB Evolution. Includes "There's no chapter for occultism" (missing content), "the quest description and prerequisites seem misleading" (description quality), "The mandatory boss catcher quest is gated behind the optional Hephaestus Forge: Tier 4 quest" (progression gating error), and "None of the quests have text" in the Generating Power chapter (empty descriptions). Evidence for AP43 (Unplaytested Release), AP46 (Quest Narrative Disconnection), and AP5 (Empty Quest Description). https://github.com/FTBTeam/FTB-Modpack-Issues/issues/6447
