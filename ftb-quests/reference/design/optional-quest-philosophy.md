# Optional Quest Design Philosophy

Empirical analysis of optional quests across ATM10 chapters (2026-07-04).

## What Makes a Quest Optional?

Optional quests in ATM10 serve three primary purposes:

1. **Alternative paths**: Show multiple ways to achieve the same goal
2. **Side content**: Introduce mods/mechanics that aren't essential for progression
3. **Quality of life**: Offer convenience items or shortcuts

## Design Patterns

### Pattern 1: Alternative Crafting Paths

**Example from Star chapter:**
- Uranium Quad Fuel Rods (Modern Industrialization)
- Blaze Burner (Create)
- Both are optional fuel sources for the Philosopher's Fuel

**Quest text style:**
```
"Or you can just use a Blaze Burner... but come on that's no fun!"
```

**Key characteristics:**
- Explains the alternative exists
- Uses humor to acknowledge the choice
- Doesn't gate progression

### Pattern 2: Multiple Requirements, Choose Your Path

**Example from Star chapter:**
- 256M Portable Item Cell (MEGA Cells)
- Blastproof Casing (Modern Industrialization)
- Quest text: "We'll need either 2 256M Portable Item Cells, 2 Blastproof Casings, or a mix of both"

**Key characteristics:**
- Shows flexibility in requirements
- Lets players use mods they prefer
- Reduces grinding by offering alternatives

### Pattern 3: Weapon/Tool Variants

**Example from AllTheModium chapter:**
- AllTheModium Bow
- AllTheModium Crossbow
- AllTheModium Shield
- AllTheModium Trident

**Key characteristics:**
- All are weapon variants
- Player chooses based on playstyle
- `hide_dependency_lines: true` to visually separate

## Visual Design

### Size and Shape
- **Size**: 1.25d (slightly larger than default 1.0d)
- **Shape**: Always circle (visually unobtrusive)
- **Reason**: Signals "this is extra content" without drawing too much attention

### Dependency Lines
- **Pattern**: Often use `hide_dependency_lines: true`
- **Reason**: Optional content shouldn't clutter the main flow
- **Exception**: When the optional quest is a direct alternative to a required quest

### Positioning
- **Pattern**: Placed near related required quests
- **Reason**: Context matters - player should see the option when relevant
- **Example**: Weapon variants placed after the main weapon quest

## Rewards

### Modest but Meaningful
- **Typical reward**: 1 XP level
- **Reason**: Acknowledges effort without making the quest essential
- **Anti-pattern**: Large rewards that force players to complete optional content

### No Unique Items
- **Pattern**: Optional quests never reward unique items
- **Reason**: If the item is unique, the quest isn't truly optional
- **Exception**: Convenience items (like the AllTheModium weapons)

## Quest Text Style

### Acknowledging Choice
Optional quests often use phrases like:
- "Or you can just use X..."
- "If repetitive crafting makes you hate Minecraft..."
- "You'll need either X, Y, or a mix of both"

### Humor and Personality
- "but come on that's no fun!"
- "Yes, stains matter apparently"
- Shows the author's voice while respecting player choice

### Clear Purpose
- Explains what the alternative achieves
- Shows how it fits into the larger goal
- Doesn't oversell the option

## When to Use Optional Quests

### Good Use Cases
1. **Multiple valid approaches**: When there are 2+ ways to craft something
2. **Mod preferences**: When players might prefer different mods for the same task
3. **Convenience items**: Tools that make life easier but aren't essential
4. **Side mechanics**: Introducing mods that aren't part of the main progression

### Bad Use Cases
1. **Essential content**: If it's required for progression, it's not optional
2. **Unique rewards**: If the reward is unique, players feel forced to complete it
3. **Hidden requirements**: If other quests depend on it, it's not truly optional
4. **Large rewards**: Big rewards make "optional" feel like a lie

## Implementation Checklist

When designing an optional quest:

- [ ] Is this truly optional? (No other quests depend on it)
- [ ] Does it offer a real choice? (Alternative path, not just extra content)
- [ ] Is the reward modest? (1 XP level, not game-changing items)
- [ ] Is the text clear about the choice? (Explains alternatives)
- [ ] Is it visually distinct? (Size 1.25d, circle shape)
- [ ] Should dependency lines be hidden? (Usually yes, unless it's a direct alternative)

## Examples from ATM10

### Good: Uranium Quad Fuel Rods
- **Purpose**: Alternative fuel source for Philosopher's Fuel
- **Text**: "Or you can just use a Blaze Burner... but come on that's no fun!"
- **Reward**: 1 XP level
- **Why it works**: Clear alternative, modest reward, humorous text

### Good: Weapon Variants (AllTheModium)
- **Purpose**: Choose your preferred weapon type
- **Text**: Explains each weapon's unique properties
- **Reward**: The weapon itself (convenience item)
- **Why it works**: Player choice based on playstyle, no unique mechanics

### Good: 256M Portable Item Cell vs Blastproof Casing
- **Purpose**: Multiple ways to craft the Improbable Probability Device
- **Text**: "We'll need either 2 256M Portable Item Cells, 2 Blastproof Casings, or a mix of both"
- **Reward**: 1 XP level each
- **Why it works**: Flexibility, respects player preferences, reduces grinding

## Anti-Patterns

### 1. Fake Optional
**Problem**: Quest is marked optional but other quests depend on it
**Solution**: Check dependency graph before marking optional

### 2. Reward Traps
**Problem**: Large rewards make players feel forced to complete "optional" content
**Solution**: Keep rewards modest (1 XP level max)

### 3. Hidden Alternatives
**Problem**: Alternative paths exist but aren't explained
**Solution**: Quest text should clearly explain all options

### 4. Visual Clutter
**Problem**: Too many optional quests clutter the main flow
**Solution**: Use `hide_dependency_lines: true` and keep optional quests to <10% of chapter

## Statistics

### ATM10 Optional Quest Usage
- **AllTheModium**: 5 optional (9.3%)
- **Star**: 6 optional (7.1%)
- **Main Questline**: 5 optional (13.9%)
- **Twilight**: 4 optional (7.1%)
- **Food**: 2 optional (5.7%)
- **Mekanism**: 2 optional (2.2%)
- **Ars**: 7 optional (5.4%)

### Pattern: 2-14% of Quests
- **Low end (2%)**: Tech chapters with linear progression
- **High end (14%)**: Main questline with multiple paths
- **Sweet spot (5-10%)**: Most chapters

## Summary

Optional quests in ATM10 are:
- **Truly optional**: No dependencies, modest rewards
- **Clear choices**: Text explains alternatives
- **Visually distinct**: Size 1.25d, circle shape, often hidden dependency lines
- **2-14% of content**: Enough to offer variety without clutter
- **Player-respecting**: Acknowledge choice, don't force completion

**Key principle**: Optional quests should feel like genuine choices, not hidden requirements or reward traps.
