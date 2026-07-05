# Quest Book Design Taxonomy — Beyond ATM

**Evolved from:** ATM9/ATM10 deep-dive + research across GTNH, Divine Journey 2, SevTech: Ages, Enigmatica Expert, Create: Astral, and community discussions (2026-07-04).

---

## The Five Axes of Quest Design

Every quest book makes decisions along five independent axes. Understanding these axes lets you deliberately choose your pack's identity instead of defaulting to one style.

### Axis 1: Progression Enforcement

How strictly does the pack control what players can access?

| Level | Mechanism | Example | Player Experience |
|-------|-----------|---------|-------------------|
| **Open** | No gates, quests are optional | ATM9/10 | "Do whatever you want, quests are a guide" |
| **Suggested** | Quests recommended but not required | Enigmatica Normal | "Follow the path or explore, both work" |
| **Gated** | Recipes/items locked behind quest completion | Divine Journey 2, E6 Expert | "Must complete X to unlock Y" |
| **Hidden** | Content literally invisible until unlocked | SevTech: Ages, GTNH (ores) | "The world reveals itself as you progress" |

**Key insight:** ATM chose "Open" deliberately — kitchen sinks celebrate player freedom. Expert packs choose "Gated" or "Hidden" to enforce a curated experience. Neither is "better" — they serve different audiences.

**ProgressiveStages mod** (1.21.1 NeoForge) enables "Hidden" style on modern Minecraft:
```
🪨 stone_age → ⚙️ iron_age → 💎 diamond_age → 🔮 netherite_age
```
Lock items, recipes, blocks, entities, dimensions, fluids, and entire mods behind stages.

---

### Axis 2: Chapter Organization

How is content grouped?

| Model | Structure | Example | Mental Model |
|-------|-----------|---------|--------------|
| **Per-Mod** | One chapter per mod | ATM9/10 | "I want to learn Mekanism" |
| **Themed/Age** | Chapters by era or theme | SevTech, Create: Astral | "I'm in the Bronze Age" / "I'm going to Mars" |
| **Voltage Tier** | Chapters by tech level | GTNH, Enigmatica Expert | "I need to reach IV tier" |
| **Story Arc** | Chapters follow narrative | Story packs | "What happens next?" |
| **Hybrid** | Mix of above | Most packs | Varies |

**Key insight:** Per-mod organization respects that players think in mods. Themed organization respects that players think in experiences. Voltage tier organization respects that expert packs think in power levels. Choose based on your pack's identity.

**Create: Astral's hybrid:** Chapters are themed around celestial bodies (Moon, Mars, Mercury), but each chapter integrates multiple mods through Create's crafting systems. Space travel is the spine, not the endgame.

---

### Axis 3: Quest Purpose

What role do quests play?

| Purpose | Description | Example | Reward Philosophy |
|---------|-------------|---------|-------------------|
| **Guide** | Show what's possible, suggest paths | ATM, Enigmatica Normal | Generous (incentivize following) |
| **Gate** | Block progression until completed | DJ2, E6 Expert | Minimal (progression IS the reward) |
| **Teach** | Explain complex mechanics step-by-step | GTNH | Informational (quest text = manual) |
| **Challenge** | Test skill, provide difficulty spikes | Expert packs | Cosmetic/lore (satisfaction of completion) |
| **Catalog** | Document all items/recipes | ATM Bounty Board, GTNH reference pages | None (pure reference) |

**Key insight:** Most packs mix purposes, but the **primary purpose** shapes everything else. ATM's primary = Guide. DJ2's primary = Gate. GTNH's primary = Teach. SevTech's primary = Gate (hidden content).

---

### Axis 4: Cross-Mod Integration

How do mods interact?

| Model | Mechanism | Example | Player Experience |
|-------|-----------|---------|-------------------|
| **Independent** | Mods don't interact, just coexist | Basic kitchen sinks | "Pick one mod and stick with it" |
| **Item-Task** | Quest requires items from multiple mods | ATM Star components | "I need Mekanism + AE2 + Ars Nouveau" |
| **Recipe-Chain** | Mod X's output is Mod Y's input | DJ2, E6 Expert | "Must automate X to craft Y" |
| **Gamestages** | Entire mods locked behind progression | SevTech, ProgressiveStages | "Can't even see Mekanism until IV tier" |
| **Deep Integration** | KubeJS scripts create cross-mod systems | GTNH, CraftTweaker packs | "Mods feel like one unified system" |

**Key insight:** ATM uses "Item-Task" to preserve freedom (you can gather Star components in any order). Expert packs use "Recipe-Chain" to enforce sequence (you MUST automate Mekanism before you can craft AE2 processors). GTNH uses "Deep Integration" so thoroughly that mods feel like one game.

---

### Axis 5: Writing Voice

How does the quest text communicate?

| Voice | Tone | Example | Audience |
|-------|------|---------|----------|
| **Humorous** | Jokes, self-aware, conversational | ATM9/10 | Casual players, newcomers |
| **Technical** | Precise, instructional, no fluff | GTNH, DJ2 | Experienced players, completionists |
| **Minimal** | Few words, let visuals speak | SevTech, some expert packs | Players who hate reading |
| **Narrative** | Story-driven, lore-heavy | Story packs | Immersion-focused players |
| **Mixed** | Varies by chapter/author | Most large packs | Broad audience |

**Key insight:** ATM's humor is deliberate accessibility — 500 mods is intimidating, so jokes lower the barrier. GTNH's technical voice matches its audience (players willing to spend 2000 hours). Choose voice based on your target player, not personal preference.

---

## The Modpack Archetypes

Combining the five axes produces distinct archetypes. Each archetype serves a specific audience.

### 1. Kitchen Sink (ATM9/10, FTB Infinity)

**Axes:** Open progression, Per-mod chapters, Guide purpose, Item-task integration, Humorous voice

**Philosophy:** "Here's everything, explore at your own pace. We'll give you a map and a destination."

**Strengths:**
- Appeals to broadest audience
- High replayability (different paths each playthrough)
- Low barrier to entry

**Weaknesses:**
- Can feel aimless without strong endgame goal
- Mods may not integrate (just coexist)
- "Mod dump" criticism

**Key design decisions:**
- ATM Star as convergence point (gives direction without forcing compliance)
- AllTheModium as custom spine (extends progression beyond Netherite)
- Generous rewards (incentivize following optional quests)
- Per-mod chapters (respect player's mental model)

---

### 2. Expert Pack (DJ2, Enigmatica Expert, Omnifactory)

**Axes:** Gated progression, Voltage-tier chapters, Gate purpose, Recipe-chain integration, Technical voice

**Philosophy:** "Follow our carefully designed path. Each step builds on the previous. You'll master every system."

**Strengths:**
- Curated experience (no dead ends, no OP shortcuts)
- Deep mod integration (mods feel like one game)
- Satisfying progression (earn every advancement)

**Weaknesses:**
- High barrier to entry (can feel grindy early)
- Low replayability (one "correct" path)
- Alienates casual players

**Key design decisions:**
- Expensive recipes (force automation, not manual crafting)
- Cross-mod recipe chains (Mekanism output → AE2 input)
- Minimal rewards (progression IS the reward)
- Strict gating (can't skip ahead)

**Divine Journey 2 specifics:**
- 1600+ quests, 30 chapters
- "Tightly-tailored journey through a wide variety of mods"
- "Progression is carefully structured to ensure a curated experience"
- Dimensions gated behind tech milestones, further tech gated by exploration materials
- ~500 hours to complete, 1000+ for completionists

---

### 3. Hidden Progression (SevTech: Ages)

**Axes:** Hidden progression, Themed/age chapters, Gate purpose, Gamestages integration, Minimal voice

**Philosophy:** "The world transforms as you progress. You don't know what you don't know until you unlock it."

**Strengths:**
- Unique experience (world literally changes)
- Strong sense of discovery
- Prevents sequence breaking completely

**Weaknesses:**
- Can feel restrictive
- Hard to plan ahead (don't know what's coming)
- Requires custom mod support (gamestages, hidden items)

**Key design decisions:**
- 6 ages: Stone → Bronze → Middle → Industrial → Modern → Futuristic
- Ores invisible until unlocked (can't even see diamond ore in Stone Age)
- Items/recipes hidden until relevant age
- New mobs appear as you progress
- Vanilla advancements as progression (not FTB Quests)

---

### 4. Themed Journey (Create: Astral)

**Axes:** Gated progression, Themed chapters (celestial bodies), Guide + Gate purpose, Deep integration, Technical voice

**Philosophy:** "Journey through space, with each planet teaching new mechanics."

**Strengths:**
- Strong narrative arc (space travel as spine)
- Clear objectives (reach the next planet)
- Thematic coherence (everything fits the space theme)

**Weaknesses:**
- Narrower appeal (only space-themed players)
- Less replayability (one path through the solar system)
- Requires heavy custom content (planets, structures)

**Key design decisions:**
- Chapters per celestial body (Earth → Moon → Mars → Mercury)
- Space travel unlocked early (not endgame)
- All mods integrated into Create's crafting systems
- Custom planets with unique generation, structures, mobs
- 12 chapters total (6 main, 3 sub, 1 FAQ, 1 endgame, 1 ???)

---

### 5. Reference Bible (GTNH)

**Axes:** Hidden progression (ores), Voltage-tier chapters, Teach purpose, Deep integration, Technical voice

**Philosophy:** "The quest book IS the manual. Everything you need to know is here."

**Strengths:**
- Self-contained (no wiki needed)
- Extremely thorough (2000+ quests)
- Respects player intelligence (skip quests for veterans)

**Weaknesses:**
- Extremely long (1600-2500 hours)
- High barrier to entry (requires reading comprehension)
- Can feel overwhelming

**Key design decisions:**
- 15+ voltage tiers (Stone → LV → MV → HV → ... → UXV)
- Each tier = one chapter with optional exploration quests
- **"Skip quests"** — hold items to bypass grind quests (brilliant for veterans)
- Quest book explains every mod, every recipe chain, every mechanic
- Ore generation in 3x3 chunk veins (forces exploration, not strip mining)
- 10+ years of development, still being improved

**GTNH's "Skip Quests" innovation:**
```
Trigger: Rubber Skip → Hold 128 rubber bars → Bypasses wire-wrap quest
Trigger: Platline Iridium Skip → Hold 64 Iridium Dust → Bypasses EV quest
```
This lets veterans skip tedious parts while newcomers learn every step. **Best practice for long packs.**

---

## Community Wisdom — What Makes a Good Quest Book?

Distilled from Reddit r/feedthebeast, FTB forums, YouTube comments, and GitHub discussions.

### The Four Pillars (community consensus)

**1. Clear progression path**
> "GTNH has the best quest book and progression of any pack hands down."
> "Questlines that lead you through the pack's progression."

Players want to know: "What do I do next?" A good quest book answers this unambiguously.

**2. Teaching without hand-holding**
> "The quest book is word heavy and content dense. Failure to read and understand will result in a frustratingly bad time." (GTNH wiki)
> "I find the quest book not to be of use due to me having autism and I tend to not understand quest books sometimes unless there REALLY in-depth." (Enigmatica 6 Expert player)

Balance: explain enough, but don't do everything for the player. GTNH's approach — explain every step, but require the player to execute — is the gold standard.

**3. Satisfaction on completion**
> "Agrarian Skies 2 is the exemplar quest book. Design of HQM makes it feel very satisfying to complete a quest."
> "The amount of quests and longevity of a pack depends on the number of mechanics that are introduced."

Quests should feel rewarding, not like chores. Rewards, visual feedback, and sense of progress all contribute.

**4. Information completeness**
> "This HUGE questbook, with more than 2000 quests, was at the same time a great guide to erase the problem of guessing recipes, and a clear path."
> "GTNH quest book easily contains 100% of the information needed to complete the game."

A good quest book is self-contained. Players shouldn't need to Google recipes or watch YouTube tutorials for basic progression.

---

### Common Complaints (what to avoid)

**1. "Quest book gives too many rewards that break balance"** (ATM10 Discussion #3539)
- ATM's response: "It is a kitchen sink pack, the only thing that could actually 'break progression' would be gifting out ATM Stars."
- **Lesson:** In kitchen sinks, rewards don't break balance because mods themselves are already OP. In expert packs, rewards must be minimal to preserve gating.

**2. "Quests are optional but the pack is impossible without following them"**
- **Lesson:** Be honest about whether quests are required. If they're optional, the pack should be completable without them. If they're required, make that clear.

**3. "I can't tell where the quest line starts and ends"** (ATM10 To The Sky criticism)
- **Lesson:** Visual clarity matters. Players should be able to glance at a chapter and understand the progression flow. Use layout templates (Ribbon, Mesh, Convergence) to make this obvious.

**4. "Grindy quests that don't teach anything"**
- **Lesson:** Every quest should have a purpose. "Collect 64 iron" is only good if it teaches something (ore processing, automation) or gates something important. Pure busywork frustrates players.

**5. "Quest text is too long / too short"**
- **Lesson:** Match length to purpose. Teaching quests need detail. Simple item-collection quests need brevity. ATM's three-tier text model (title ≤4 words, subtitle = 1 line, description = 2-4 sentences) is a good default.

---

## Evolution — What ATM Gets Right (and Wrong)

### ATM's strengths (learn from these)

1. **ATM Star as convergence** — Gives 500 mods a unified purpose without forcing compliance
2. **Per-mod chapters** — Respects player's mental model ("I want to learn X")
3. **Flexible progression** — Trusts the player, appropriate for kitchen sinks
4. **Humorous writing** — Lowers barrier to entry for 500-mod intimidation
5. **AllTheModium spine** — Extends progression beyond vanilla ceiling
6. **Generous rewards** — Incentivizes following optional quests
7. **Item-task integration** — Preserves freedom while teaching cross-mod crafting

### ATM's weaknesses (improve on these)

1. **Weak cross-mod integration** — Most mods just coexist, not interact
2. **"Mod dump" perception** — Critics say "just a folder of mods with quests"
3. **No skip quests** — Veterans must re-do every quest (GTNH solved this)
4. **Inconsistent writing quality** — Some chapters are excellent, others are sparse
5. **No hidden content** — Everything visible from start (can feel overwhelming)

### How to evolve beyond ATM

**For kitchen sinks:**
- Add "skip quests" for veterans (GTNH model)
- Increase cross-mod integration (not just Star components)
- Consider ProgressiveStages for optional hidden content

**For expert packs:**
- Use ATM's three-tier text model (title/subtitle/description) for clarity
- Add ATM Star-style convergence for satisfying endgame
- Use ATM's layout templates for visual clarity

**For any pack:**
- Be explicit about your quest philosophy (open/gated/hidden)
- Match writing voice to target audience
- Ensure every quest has a clear purpose
- Make progression visually obvious (layout templates)

---

## Practical Decision Tree — Choosing Your Quest Philosophy

```
START: What's your pack's identity?
│
├─ "Kitchen sink, player freedom" → ATM model
│  ├─ 200+ mods? → Per-mod chapters
│  ├─ Clear endgame? → Convergence item (ATM Star)
│  ├─ Want to guide without forcing? → Flexible + generous rewards
│  └─ Want to appeal to newcomers? → Humorous writing
│
├─ "Expert, curated experience" → DJ2/E6E model
│  ├─ Want deep integration? → Recipe chains + voltage tiers
│  ├─ Want to enforce sequence? → Gated progression + gamestages
│  ├─ Want to teach thoroughly? → Technical writing + detailed descriptions
│  └─ Want to prevent shortcuts? → Expensive recipes + minimal rewards
│
├─ "Hidden discovery" → SevTech model
│  ├─ Want world to transform? → Hidden ores/items/mobs by age
│  ├─ Want strong narrative? → Themed chapters + story progression
│  ├─ Want to prevent sequence breaking? → Gamestages for everything
│  └─ Want minimalist text? → Let visuals speak
│
├─ "Themed journey" → Create: Astral model
│  ├─ Want clear objectives? → Chapters per destination/era
│  ├─ Want thematic coherence? → All mods fit the theme
│  ├─ Want journey to BE the game? → Unlock travel early, not endgame
│  └─ Want deep integration? → Custom content + mod interplay
│
└─ "Reference bible" → GTNH model
   ├─ Want self-contained? → Explain everything in quest text
   ├─ Want to respect veterans? → Skip quests for grind
   ├─ Want extreme length? → 15+ tiers, 2000+ quests
   └─ Want to be the gold standard? → 10+ years of iteration
```

---

## The Meta-Lesson

**There is no "best" quest philosophy.** Each archetype serves a specific audience:

- **Kitchen sink (ATM)** → Casual players, newcomers, "do whatever" players
- **Expert (DJ2/E6E)** → Experienced players, completionists, automation lovers
- **Hidden (SevTech)** → Discovery-focused players, anti-sequence-breaking players
- **Themed (Create: Astral)** → Narrative-focused players, space/theme enthusiasts
- **Reference (GTNH)** → Hardcore players, "read the manual" types, 2000+ hour commitments

**The best quest book is the one that matches your pack's identity and your target audience's expectations.** Don't try to be everything to everyone — pick an archetype and commit.

---

## Practical Techniques — Proven Patterns from Shipped Packs

### 1. Cross-Chapter Navigation via Clickable Links

ATM embeds JSON text components in quest descriptions for one-click chapter jumping:
```
{ "text": "INDUSTRIAL FOREGOING QUESTLINE", "color": "#55FF55",
  "underlined": true,
  "clickEvent": { "action": "change_page", "value": "193F91842D2ED7D9" } }
```
This appears as a green underlined link in the quest popup. When a quest says "you need Industrial Foregoing for this," clicking the link jumps to that chapter. **Use this instead of `quest_links[]` (hexagon) for most cross-chapter references.** Hexagons are for displaying the SAME quest in two chapters; clickable text is for navigation hints.

### 2. Inline Images in Quest Descriptions

ATM uses `{image:...}` syntax to embed images directly in quest text:
```
{image:atm:textures/questpics/allthemodium/all_city.png width:200 height:100 align:center}
```
- **AllTheModium chapter:** 18 inline images (armor previews, location screenshots)
- **ATM Star chapter:** 12 inline images + 1 `{@pagebreak}` for multi-page descriptions
- **Common sizes:** `width:100 height:100` (items), `width:200 height:100` (screenshots)
- **Alignment:** `align:center` (most common), `align:1` (right-aligned)

**Use for:** armor previews, structure build guides, recipe screenshots, location maps. **Don't use for:** pure decoration (use `images[]` array instead).

### 3. Hidden Copyright Quest (AllRightsReserved Pattern)

ATM places one invisible quest per chapter containing a copyright notice:
```
invisible: true
tasks: [{ type: "checkmark", title: "AllRightsReserved" }]
description: "This Quest has been authored by AllTheMods Staff..."
```
This is invisible to players but protects intellectual property. **Include one per chapter for any commercial pack.**

### 4. Reward Tables — Three Naming Models

ATM's 51 reward tables follow three naming patterns:

| Model | Pattern | Example | When to use |
|-------|---------|---------|-------------|
| **Mod-specific** | `{ModName}: {Category}` | `Powah: Nitro`, `AE2: Basic Rewards` | When rewards are items from one mod |
| **Rarity tier** | `Reward: {Tier}` | `Reward: Common`, `Reward: Legendary` | When rewards are generic loot by quality |
| **Functional** | `{Description}` | `Logs & Saplings`, `1x1 Wooden Drawers` | When rewards serve a specific gameplay purpose |

**ATM's dominant model:** 42/51 (82%) are mod-specific. This matches the per-mod chapter philosophy.

### 5. min_width — Controlling Quest Popup Size

ATM uses `min_width: 300` on quests with long descriptions or inline images. Default popup width is ~250px.
- **min_width: 250** — Standard quests
- **min_width: 300** — Quests with images or multi-paragraph descriptions
- **min_width: 350** — Quests with build guides or complex instructions

### 6. Optional Quests — Side Content Within Chapters

ATM marks non-essential quests as `optional: true`:
- **ATM Star:** 9 optional (7% of chapter)
- **Ars Nouveau:** 7 optional (5%)
- **AllTheModium:** 5 optional (9%)

**Pattern:** ~5–10% of quests per chapter are optional side content. Use for: alternative crafting paths, bonus rewards, "nice to have" items. **Don't use for:** core progression steps.

### 7. GTNH's "Skip Quest" System

GTNH lets veterans bypass grind quests by holding specific items:
```
Trigger: Rubber Skip → Hold 128 rubber bars → Bypasses wire-wrap quest
Trigger: Platline Iridium Skip → Hold 64 Iridium Dust → Bypasses EV quest
```
This is brilliant for long packs (2000+ hours) where replaying early content is tedious. **Consider for any pack >100 hours.** Implementation: use `checkmark` tasks with item-holding conditions, or KubeJS custom tasks.

### 8. Quest Text Formatting Codes

ATM uses Minecraft color codes extensively (1,339 codes in ATM Star chapter alone):
| Code | Effect | Usage frequency |
|------|--------|----------------|
| `&6` | Gold | Mod names, important items |
| `&a` | Green | Tips, positive actions |
| `&c` | Red | Warnings, dangerous items |
| `&d` | Pink | Magic items, special materials |
| `&l` | Bold | Emphasis (182 uses in ATM Star) |
| `&o` | Italic | Poetic/flavor text (11 uses) |
| `&9` | Blue | Tech items, AE2 references |
| `&5` | Purple | Rare/epic items |

**Rule:** Use `&6` for mod names, `&a` for tips, `&c` for warnings. Bold (`&l`) for key terms only — overuse makes everything look the same.

---

*Sources: ATM9/ATM10 GitHub (841 quests), GTNH wiki, Divine Journey 2 reviews, SevTech CurseForge, Create: Astral wiki, Reddit r/feedthebeast discussions, FTB forums, YouTube creator feedback, ProgressiveStages mod documentation. Compiled 2026-07-04.*
