# Quest Reward Economics — Empirical Patterns from ATM9/ATM10

**Source:** 794 quests analyzed across 11 ATM chapters (2026-07-04).

## Key Findings

### 1. Reward Density Spectrum

Reward density = % of quests that give rewards. ATM packs span the full spectrum:

| Density Range | Example Chapters | Design Intent |
|---------------|------------------|---------------|
| **0%** | Welcome | Tutorial/intro only, no economy needed |
| **20-40%** | AllTheModium (22%), Ars Nouveau (42%) | Gated progression, rewards are milestones |
| **60-80%** | Create (66%), Twilight (64%), Food (80%) | Moderate encouragement, balanced flow |
| **80-96%** | Star (80%), Mekanism ATM9 (96%), AE2 (92%) | High engagement, reward-driven progression |

**Pattern:** Higher reward density → more "game-like" feel. Lower density → more "textbook/tutorial" feel.

### 2. XP Scaling Patterns

XP scaling = late-game average XP / early-game average XP.

| Scaling | Example | Interpretation |
|---------|---------|----------------|
| **0-1.5x** | AE2 (1.27x), Ars Nouveau (1.16x) | Flat rewards, no inflation |
| **2-3x** | Twilight (1.64x), Main (2.03x), Mekanism ATM9 (2.14x) | Gentle scaling, feels natural |
| **4-6x** | Star (4.43x), Food (6.12x) | Moderate inflation, late-game feels rewarding |
| **9x+** | AllTheModium (9.5x) | Heavy gating, rewards are rare but large |

**Anti-pattern:** Avoid scaling >10x unless the pack is explicitly gated (like AllTheModium's tier system).

### 3. Reward Type Strategies

ATM packs use three distinct strategies:

#### Strategy A: Pure XP (No Items)
- **Example:** ATM10 Create (0 items, 0 XP, but rewards present)
- **When to use:** When items would break balance or clutter inventory
- **Implementation:** Give XP only, or use `command` rewards for special items

#### Strategy B: XP + Items (Balanced)
- **Example:** ATM10 Mekanism (605 XP + 717 items across 90 quests)
- **When to use:** Most tech/magic packs, moderate pacing
- **Ratio:** ~1:1 XP-to-items (by count)

#### Strategy C: XP + Items + Random Rewards
- **Example:** ATM10 AE2 (6220 XP + 14 items + 65 random rewards)
- **When to use:** High-engagement packs, casino-like feel
- **Pattern:** Random rewards appear in 70-90% of quests

### 4. Item Reward Quantities

| Avg Items/Quest | Example | Feel |
|-----------------|---------|------|
| **0-1** | Ars Nouveau (0.1), AE2 (0.2) | Token rewards, symbolic |
| **1-3** | Main (2.1), Twilight (3.5), Star (3.7) | Moderate, useful |
| **5-8** | Create (5.9), Mekanism (8.0) | Generous, progression-enabling |

**Pattern:** Create gives 5.9 items/quest because it's a crafting-heavy pack where you NEED those items to progress. Mekanism gives 8.0 items/quest to bootstrap complex automation.

## Design Principles

### Principle 1: Match Density to Chapter Purpose

| Chapter Type | Target Density | Rationale |
|--------------|----------------|-----------|
| Tutorial/Welcome | 0-20% | No economy yet, just learning |
| Mod Introduction | 60-80% | Encourage exploration, moderate pacing |
| Progression/Gating | 20-40% | Rewards are milestones, not incentives |
| Endgame/Convergence | 80-96% | High engagement, reward grind |

### Principle 2: Control Inflation with Scaling

- **Flat (1-1.5x):** Use for packs where late-game tasks aren't harder, just longer (AE2 storage expansion)
- **Gentle (2-3x):** Use for most packs, feels natural (Twilight boss progression)
- **Moderate (4-6x):** Use when late-game is genuinely harder (Star endgame, Food late-game)
- **Heavy (9x+):** Use ONLY for explicitly gated packs (AllTheModium tier system)

**Rule of thumb:** If a player can skip late-game quests without penalty, keep scaling <3x. If late-game is mandatory, scaling 4-6x is acceptable.

### Principle 3: Choose Reward Types by Pack Style

| Pack Style | Reward Mix | Example |
|------------|------------|---------|
| Kitchen Sink | XP + Items (balanced) | ATM10 Mekanism |
| Expert/Gated | XP only or XP + rare items | AllTheModium (22% density, 9.5x scaling) |
| Tutorial/Teaching | Items only, no XP | Create (pure items, no XP) |
| Casino/Engagement | XP + Items + Random (70%+) | AE2, ATM9 Mekanism |

### Principle 4: Item Quantities Should Match Crafting Needs

- **0-1 items/quest:** Use when items are symbolic (trophies, achievements)
- **1-3 items/quest:** Use when items are useful but not critical
- **5-8 items/quest:** Use when items are REQUIRED for next quest (bootstrap automation)

**Anti-pattern:** Don't give 1 iron ingot when the next quest needs 64. Match quantities to actual needs.

### Principle 5: Random Rewards Are Engagement Tools

- Use random rewards in 70%+ of quests for high-engagement chapters
- Use random rewards in 30-50% of quests for moderate pacing
- Use random rewards in <20% of quests for serious/tutorial packs

**Pattern:** ATM9 Mekanism uses random rewards in 70% of quests (68/97). This creates a "slot machine" feel that keeps players clicking.

## Empirical Benchmarks

### ATM9 Mekanism (High Engagement)
- 97 quests, 95.9% reward density
- 42.1 XP/quest average, 2.14x scaling
- 70.1% random rewards
- **Feel:** Casino-like, high engagement, moderate inflation

### ATM10 Create (Tutorial/Crafting)
- 90 quests, 65.6% reward density
- 0 XP, 5.9 items/quest
- 0% random rewards
- **Feel:** Generous, practical, no inflation

### ATM10 AllTheModium (Gated)
- 54 quests, 22.2% reward density
- 194.4 XP/quest average, 9.5x scaling
- 0% random rewards
- **Feel:** Milestone-based, heavy gating, rare but large rewards

### ATM10 AE2 (Endgame/Engagement)
- 73 quests, 91.8% reward density
- 85.2 XP/quest average, 1.27x scaling
- 89% random rewards
- **Feel:** High engagement, flat XP, casino-like

## Anti-Patterns to Avoid

1. **Inflation without gating:** 10x XP scaling but no mandatory late-game quests → feels pointless
2. **Generous items, no XP:** Give players XP for effort, even if items are generous
3. **Low density, low scaling:** 20% density + 1x scaling → feels stingy
4. **High density, high scaling:** 90% density + 9x scaling → inflation spiral, late-game feels broken
5. **Random rewards everywhere, no control:** 90% random but no `exclude_from_claim_all` → inventory clutter

## Implementation Checklist

When designing rewards for a chapter:

- [ ] Choose target reward density based on chapter purpose (0-96%)
- [ ] Choose XP scaling based on difficulty curve (1-9x)
- [ ] Choose reward type strategy (XP only / XP+items / XP+items+random)
- [ ] Set item quantities based on crafting needs (0-8 per quest)
- [ ] Decide random reward percentage (0-90%)
- [ ] Test: Does the chapter feel stingy, balanced, or generous?
- [ ] Test: Does late-game feel earned or inflated?
- [ ] Test: Do item rewards match the next quest's requirements?
