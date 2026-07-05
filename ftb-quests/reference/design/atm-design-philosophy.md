# ATM Quest Design Philosophy — Why ATM Works

**Empirical basis:** 841 quest nodes, 21 chapters (ATM9 + ATM10), 4,601 total quests in ATM10, 2026-07-04 analysis.  
**Purpose:** Understand the **why** behind ATM's design choices, not just the **what**.

---

## 1. The Kitchen Sink Paradox — Freedom vs Guidance

**The problem:** Kitchen sink packs have 400–500 mods. Without structure, players feel lost. With too much structure, players feel railroaded.

**ATM's solution:** **Flexible progression with a convergence point.**

### Why `progression_mode: "flexible"` everywhere?

ATM uses `"flexible"` in 100% of chapters (21/21 analyzed). This is the opposite of expert packs like Divine Journey 2 or Omnifactory, which use `"default"` to enforce strict order.

**The reasoning:**
- Kitchen sink = player choice is the core value proposition
- `"default"` mode would contradict the pack's identity ("all the mods, your way")
- `"flexible"` lets players skip mods they don't enjoy while still following the quest book
- The ATM Star provides **long-term direction** without forcing short-term compliance

**Trade-off:** Flexible mode means players can "break progression" by jumping to late-game mods early. ATM accepts this — see Discussion #3539:

> *"It is a kitchen sink pack, the only thing that could actually 'break progression' would be gifting out ATM Stars."* — TheBedrockMaster (ATM Collaborator)

**Design principle:** In kitchen sinks, **trust the player**. Gate only the endgame, not the journey.

---

## 2. The Per-Mod Chapter Model — Why Not Themed Chapters?

ATM uses **one chapter per mod** (Create, Mekanism, Ars Nouveau, etc.), not themed chapters like "Power Generation" or "The Nether."

### Why per-mod chapters?

**Reason 1: Mods are the mental model.**  
Players think "I want to learn Mekanism" or "I want to try Botania." Themed chapters force them to hunt across multiple chapters for one mod's progression.

**Reason 2: Mod progression is self-contained.**  
Each mod has its own internal tech tree (Mekanism: ore → ingot → machine → reactor). Per-mod chapters respect this natural progression without artificial mixing.

**Reason 3: Parallel play.**  
Players can work on Create, AE2, and Botania simultaneously without the quest book forcing them to finish one before starting another.

**Reason 4: Scalability.**  
Adding a new mod = adding a new chapter. No need to restructure the entire quest book.

### When ATM breaks the rule

ATM does have **themed chapters** for:
- **Basic Tools / Basic Armor / Basic Power** — Vanilla progression (wood → stone → iron → diamond)
- **Main Questline** — The "tutorial" spine (Getting Started → Nether → End → AllTheModium)
- **Chapter 2: The ATM Star** — The convergence point (cross-mod requirements)

**Pattern:** Use per-mod chapters for **mid-game exploration**, themed chapters for **early-game guidance** and **late-game convergence**.

---

## 3. The ATM Star as Convergence — Why It Works

The ATM Star is the endgame goal that requires components from 20+ mods. This is the **single most important design decision** in ATM.

### Why a convergence point?

**Problem:** Kitchen sinks without an endgame feel endless. Players quit when they run out of things to do, not when they've "beaten" the pack.

**Solution:** The ATM Star gives the entire playthrough **direction**. Every mod becomes a stepping stone toward something tangible.

**Evidence from quest text** (ATM Star chapter):

> *"You have created the ATM Star, that means you have beat the modpack! So what's next?"* — Quest "ATM Star" (05850541675B2493)

The pack explicitly frames the Star as "beating" the modpack, giving players a clear win condition.

### Why require components from so many mods?

**Reason 1: Breadth over depth.**  
Forcing deep progression in one mod (e.g., "build a Mekanism fusion reactor") would alienate magic players. Requiring components from 20+ mods lets players choose their path.

**Reason 2: Cross-mod integration.**  
The Star's recipe requires items that combine multiple mods (e.g., "Ars Nouveau + AllTheModium = alloy blocks"). This teaches players that mods interact.

**Reason 3: Replayability.**  
Different playthroughs can focus on different mods to gather Star components. No two runs are identical.

### The convergence chapter structure

ATM10's "Chapter 2: The ATM Star" has:
- **90 root nodes** (71% of quests are independent)
- **127 total quests**
- **Convergence on one node** (the Star itself, size=5.0)

**Topology:** Mostly independent quests (one per mod component) → converge on the Star. This is the **Convergence Star** layout pattern (Template 4).

**Anti-clutter strategy:** Minimal flags (3 hide_dep_lines, 0 hide_until_visible). The chapter is the map — hiding dependencies would obscure the path to the endgame.

---

## 4. The AllTheModium Spine — Custom Mod as Progression Backbone

AllTheModium is a custom mod added by the ATM team. It introduces three new ore tiers:
- **Allthemodium** (requires Netherite pickaxe)
- **Vibranium** (requires Allthemodium pickaxe)
- **Unobtainium** (requires Vibranium pickaxe)

### Why add a custom ore tier?

**Problem:** Vanilla progression ends at Netherite. With 500 mods, players need a **new ceiling** to work toward.

**Solution:** AllTheModium extends the material tier ladder:
```
Wood → Stone → Iron → Diamond → Netherite → Allthemodium → Vibranium → Unobtainium
```

**Evidence from quest text** (Main Questline Part 1):

> *"The next step of progression is to make an Iron Pickaxe. This pickaxe can mine some of the rarer ores in the game, including Diamond!"* — Quest "An Iron Pick" (698A959C9E449592)

> *"To mine Allthemodium you'll need a Pickaxe that is Netherite Tier or higher!"* — Quest "Allthemodium Ingot" (201EE3566D4D3123)

The quest text explicitly frames AllTheModium as the **next tier after Netherite**, continuing the familiar material progression.

### Why three tiers instead of one?

**Reason 1: Pacing.**  
One tier would be a single jump. Three tiers create a **mini-progression arc** within the endgame.

**Reason 2: Dimension gating.**  
Each tier unlocks a new dimension:
- Allthemodium → Mining Dimension (dedicated ore dimension)
- Vibranium → The Other (adventure dimension with Piglin Villages)
- Unobtainium → The Beyond (void dimension)

**Reason 3: Recipe complexity.**  
Alloys combine tiers:
- Allthemodium + Vibranium → Alloy (requires Powah energizing)
- Vibranium + Unobtainium → Alloy (requires Industrial Foregoing)
- Allthemodium + Unobtainium → Alloy (requires Ars Nouveau)

This forces players to engage with multiple mods to reach the top tier.

### The AllTheModium chapter structure

ATM10's AllTheModium chapter has:
- **54 quests**
- **Aspect ratio 3.57** (very wide, horizontal ribbon)
- **31 hide_dep_lines** (57% of quests hide dependencies)

**Layout:** Horizontal Ribbon (Template 3) with heavy flag usage. The ribbon is long (x: 0 to 25), so hiding branch lines reduces visual clutter.

**Shape strategy:** `diamond` as default (milestones), with `hexagon` for dimension hubs and `square` for tool/armor sets.

---

## 5. Generous Rewards — Why ATM Gives So Much

ATM quests give **a lot** of rewards: XP, items, loot tables, random rewards. Discussion #3539 questions whether this "breaks balance."

### Why generous rewards?

**Reason 1: Kitchen sinks are not about balance.**  
Expert packs (Omnifactory, Divine Journey 2) gate progression tightly. Kitchen sinks celebrate abundance. Rewards match the pack's identity.

**Reason 2: Quests are optional guidance.**  
Since quests are optional, rewards incentivize following them. Without rewards, players would ignore the quest book entirely.

**Reason 3: Modded Minecraft is already "broken."**  
With 500 mods, balance is impossible. Mekanism can generate infinite power. AE2 can autocraft anything. Quest rewards are a drop in the bucket.

**Evidence from community discussion:**

> *"I think getting the ATM Ore in this modpack is just a start 🤔"* — shoucandanghehe (GitHub Discussion #3539)

The community understands that quest rewards are **not the bottleneck**. The ATM Star is the real challenge.

### Reward structure patterns

**Early-game quests** (Main Questline Part 1):
- Small XP (10–50)
- Useful items (torches, cooked beef, ore dusts)
- Loot tables (random gear)

**Mid-game quests** (per-mod chapters):
- Moderate XP (50–100)
- Mod-specific resources (AE2 processors, Mekanism ingots)
- Reward tables themed to the mod ("Powah: Nitro", "AE2: Advanced Rewards")

**Late-game quests** (ATM Star components):
- Large XP (100–500)
- Rare items (Nether Stars, Antimatter Pellets)
- No rewards for the Star itself (the Star IS the reward)

**Design principle:** Rewards scale with effort, but never gate progression. The ATM Star requires **crafting**, not quest completion.

---

## 6. Writing Voice — Accessibility and Humor

ATM's quest text is **conversational, humorous, and accessible**. This is a deliberate choice.

### Examples from quest text

**Humor:**
> *"I'm going to assume you've been out mining, right? It is MINEcraft after all."* — Quest "The Metal Age" (051E0C85E7B71CE0)

> *"Personally, I hate having to run to a block just to craft. That's where the Crafting Table on a Stick comes in!"* — Quest "Crafting, but on a Stick" (378BF828DC931F0C)

**Self-awareness:**
> *"The recipe may look confusing but trust me it is pretty easy."* — Quest "Universal Wireless Terminal" (75EE965CBA598FEA)

> *"I don't even know what to say for this. I'm getting lost looking through the recipes."* — Quest "Large Advanced Motor" (17598C171E610752)

**Teaching through questions:**
> *"Now that you have all this lava what will you do with it? More early game power!"* — Quest "Lava Power" (346860B8EBC4C28C)

**Acknowledging difficulty:**
> *"Only the hardest Structure in Vanilla Minecraft. So of course that's where you'll have to look for Allthemodium!"* — Quest "Ancient City" (111E4ACF7D570EE8)

### Why this voice?

**Reason 1: Accessibility.**  
ATM targets both new and experienced players. Humor makes the quest book feel less intimidating.

**Reason 2: Personality.**  
Kitchen sinks are often criticized as "mod dumps." The writing voice gives ATM a distinct identity.

**Reason 3: Community.**  
The quest text reads like a friend explaining the pack, not a manual. This matches ATM's Discord-centric community.

**Design principle:** Quest text should feel like a conversation, not a textbook.

---

## 7. No Cross-Chapter Dependencies — The Self-Contained Model

ATM chapters are **mostly independent**. The Main Questline gates AllTheModium, and AllTheModium gates the ATM Star, but most per-mod chapters have no cross-chapter dependencies.

### Why no cross-chapter deps?

**Reason 1: Parallel play.**  
Players can work on Create, AE2, and Botania simultaneously. Cross-chapter deps would force sequential play.

**Reason 2: Mod isolation.**  
Each mod chapter teaches one mod in isolation. Forcing players to jump between chapters would break the learning flow.

**Reason 3: Scalability.**  
Adding a new mod chapter doesn't require updating dependencies in other chapters.

### How ATM achieves cross-mod integration

Instead of cross-chapter dependencies, ATM uses **item tasks**:

**Example:** The ATM Star chapter requires items from 20+ mods. The quest text explains which mod to use, but the task itself is just "submit this item."

**Example:** AllTheModium chapter requires Ars Nouveau for alloys. The quest text says:

> *"A Magic Mod how fancy! Ars Nouveau is the Mod we'll be using to craft together Unobtainium and Allthemodium!"* — Quest "Ars Nouveau" (762581CAE5F5DDC1)

The quest **links to the Ars Nouveau chapter** via a clickable link in the text, but doesn't enforce it via dependencies.

**Design principle:** Use item tasks and quest text for cross-mod integration, not dependency chains. This preserves player freedom while still guiding them.

---

## 8. Balancing Freedom and Guidance

ATM's quest design walks a tightrope:
- **Too much freedom** → players feel lost
- **Too much guidance** → players feel railroaded

### How ATM balances this

**Early game:** Strong guidance via Main Questline Part 1 (linear chain: wood → stone → iron → diamond → netherite)

**Mid game:** Freedom via per-mod chapters (choose your path)

**Late game:** Convergence via ATM Star (clear endgame goal)

**AllTheModium:** Hybrid model (linear tier progression, but multiple ways to gather each tier)

### The "optional but incentivized" model

Quests are optional, but:
1. Rewards make following them worthwhile
2. The quest book is the only way to track progress toward the ATM Star
3. Quest text teaches mod mechanics that players would otherwise miss

**Evidence from YouTube tutorials:**

> *"The quests are indeed optional but we're going to follow through a lot of the quests in this playthrough because it's just a really good way to progress through the pack, get to know some of the mods."* — ATM 10 Let's Play Episode 1

Players understand that quests are **optional guidance**, not mandatory gates.

---

## 9. Design Principles — The ATM Way

### Principle 1: Trust the Player

Don't gate progression. Let players skip mods they don't enjoy. The ATM Star is the only hard gate.

### Principle 2: Mods Are the Mental Model

Organize by mod, not by theme. Players think "I want to learn Mekanism," not "I want to learn power generation."

### Principle 3: Convergence Without Coercion

The ATM Star gives direction without forcing compliance. Players can gather components in any order.

### Principle 4: Generosity Over Scarcity

Kitchen sinks celebrate abundance. Rewards match the pack's identity.

### Principle 5: Conversation, Not Textbook

Quest text should feel like a friend explaining the pack, not a manual.

### Principle 6: Item Tasks Over Dependencies

Use item submission for cross-mod integration, not dependency chains. This preserves freedom.

### Principle 7: Custom Spine for Custom Ceilings

AllTheModium extends the material tier ladder beyond Netherite, giving players a new progression arc.

### Principle 8: Layout Matches Function

- Early game: Linear chain (Main Questline)
- Mid game: Per-mod chapters (Square Dense Mesh or Horizontal Ribbon)
- Late game: Convergence star (ATM Star)
- Resources: Flat catalog (Bounty Board, Gregstar)

---

## 10. ATM vs Expert Packs — A Philosophical Divide

| Aspect | Kitchen Sink (ATM) | Expert Pack (DJ2, Omnifactory) |
|--------|-------------------|-------------------------------|
| **Progression mode** | `flexible` (player choice) | `default` (strict order) |
| **Chapter organization** | Per-mod | Themed / tiered |
| **Endgame** | Convergence item (ATM Star) | Final boss / creative item |
| **Rewards** | Generous (incentivize quests) | Minimal (gate progression) |
| **Cross-mod deps** | Item tasks only | Heavy dependency chains |
| **Writing voice** | Humorous, accessible | Technical, precise |
| **Player trust** | High (skip what you want) | Low (enforce sequence) |

**Design principle:** Kitchen sinks and expert packs serve different audiences. ATM's design choices are **not wrong** — they're optimized for a different player type.

---

## 11. Lessons for Pack Authors

### When to use ATM's model:
- Your pack has 200+ mods
- You want to appeal to both new and experienced players
- You value player freedom over strict progression
- You have a clear endgame goal (convergence item)

### When to avoid ATM's model:
- Your pack is <100 mods (too small for per-mod chapters)
- You want to tell a story (use themed chapters instead)
- You want to enforce a specific progression (use expert mode)
- Your mods have strong interdependencies (use cross-chapter deps)

### Key takeaways:
1. **Start with the endgame.** The ATM Star shapes everything else.
2. **Organize by mod.** Players think in mods, not themes.
3. **Trust the player.** Gate only the endgame, not the journey.
4. **Write like a friend.** Humor and accessibility > technical precision.
5. **Use item tasks for integration.** Dependencies force sequence; items preserve freedom.

---

*Source: 841 quests from 21 ATM9/ATM10 chapters, GitHub Discussions #3539, community guides, YouTube tutorials, 2026-07-04.*
