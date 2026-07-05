# Quest Text Writing Guide

Empirical analysis of 491 quests across 6 ATM10 chapters (2026-07-04).

## Text Field Specifications

### Title
- **Length**: Median 2 words, mean 2.4 words
- **Range**: 1-9 words (90th percentile: 4 words)
- **Purpose**: Instant recognition of quest content
- **Pattern**: Usually the item/machine name, occasionally with 1 descriptor

**Examples from ATM10:**
- `Metallurgic Infuser` (2 words)
- `Enrichment Chamber` (2 words)
- `Thermal Evaporation Plant` (3 words)
- `Shard, to Clump, to Dust, to Ingot` (8 words - process description)

### Subtitle
- **Usage**: Only 25.9% of quests have subtitles
- **Length**: Median 3 words, mean 3.6 words
- **Range**: 1-11 words
- **Purpose**: Brief context or secondary information
- **Pattern**: Often describes function, tier, or category

**Examples from ATM10:**
- `Tier 1 Ore Processing`
- `Basic Power Gen`
- `The Starting Machine`
- `Really Only Good For 2 Things` (humorous)

### Description
- **Structure**: 86.1% of quests have 1 paragraph, 7.3% have 2 paragraphs
- **Length per paragraph**: Median 35 words, mean 42.8 words
- **Range**: 0-235 words per paragraph
- **Outliers**: Up to 45 paragraphs for complex multi-step tutorials (1 quest)

**Pattern**: Single paragraph for most quests. Multi-paragraph for:
- Complex builds (thermal evaporation plant, multiblocks)
- Step-by-step tutorials (ore processing tiers)
- Detailed explanations (machine configs, upgrade systems)

## Color Code Usage

### Frequency (from 491 quests)
```
&r (reset)      38.2%  - Reset formatting after colored text
&l (bold)        7.5%  - Emphasis on key terms
&e (yellow)      7.5%  - Highlights, important items
&6 (gold)        6.4%  - Primary items, machines, concepts
&b (aqua)        5.5%  - Secondary items, fluids, chemicals
&f (white)       5.1%  - Reset to white text
&5 (purple)      4.6%  - Magic, rare items, special tiers
&c (red)         4.4%  - Warnings, danger, input slots
&a (green)       4.1%  - Success, output slots, positive
&d (pink)        3.6%  - Decorative, special effects
```

### Color Code Patterns

**Machine names**: `&6&lMachine Name&r` (gold + bold, then reset)
- Example: `&6&lHeat Generator&r`

**Tier names**: `&a&lBasic&r`, `&c&lAdvanced&r`, `&b&lElite&r`, `&d&lUltimate&r`
- Green → Red → Aqua → Pink progression

**Item names**: `&eItem Name&r` (yellow, then reset)
- Example: `&eBasic Control Circuit&r`

**Chemicals/fluids**: `&4Redstone&r`, `&bOxygen&r`, `&eChlorine&r`
- Color matches the chemical's in-game color

**Slots in GUI**: Color-coded by function
- `&4Red&r` = Input slots
- `&9Blue&r` = Output slots
- `&aLight Green&r` = Energy slots
- `&eYellow&r` = Infuse type slots

**Warnings**: `&4Warning text&r` (red)
- Example: `&4Make sure to connect Pipes first!&r`

## Images and Pagebreaks

### Images
- **Usage**: Only 6.5% of quests have images
- **Chapter variation**:
  - AllTheModium: 31.5% (visual guide for complex builds)
  - Mekanism: 13.0% (machine setups, ore processing diagrams)
  - Create/AE2/Twilight/Star: 0-1.8% (minimal)
- **Purpose**: Show complex multiblock structures, GUI layouts, process diagrams

### Pagebreaks
- **Usage**: Only 1.0% of quests use pagebreaks
- **Pattern**: Used for very long tutorials (23-45 paragraphs)
- **Example**: Mekanism machine config tutorial (multi-page guide)

## Writing Patterns

### Pattern 1: Simple Item Quest (most common)
```
Title: &6&lMachine Name&r
Description: [&5&lMod Name&r &5Machines&r do X. \\n\\nExplain how it works.]
```

**Characteristics**:
- Title: 2-3 words, gold + bold
- Description: 1 paragraph, 30-50 words
- No subtitle
- No images

### Pattern 2: Tier/Upgrade Quest
```
Title: &a&lBasic Tier&r
Subtitle: The Starting Tier
Description: [&a&lBasic Tier&r is the simplest tier. \\n\\nMade from &4Redstone&r, &aBasic Control Circuits&r, and &7Iron&r.]
```

**Characteristics**:
- Title: Tier name with color code
- Subtitle: Brief context
- Description: 1 paragraph explaining what the tier is and how to get it

### Pattern 3: Process Tutorial (multi-paragraph)
```
Title: &dEnrich &fthen &6Smelt&r
Subtitle: Tier 1 Ore Processing
Description: [
  "The very first and simplest &lOre Processing&r is just 2 &5Machines&r! \\n\\n..."
  "{image:atm:textures/questpics/mek/mek_tier1_1.png width:150 height:50 align:center}"
]
```

**Characteristics**:
- Title: Process description (3-8 words)
- Subtitle: Tier/category label
- Description: 2+ elements (text + image)
- Image shows the process/setup

### Pattern 4: Complex Build Guide (rare)
```
Title: &6&lThermal Evaporation Plant&r
Description: [
  "Paragraph 1: Overview of what it does"
  "{@pagebreak}"
  "Paragraph 2: Base layer instructions"
  "{image:...}"
  "Paragraph 3: Wall instructions"
  "{image:...}"
  "Paragraph 4: Top layer instructions"
  "{image:...}"
]
```

**Characteristics**:
- Title: Build name (2-3 words)
- Description: 10+ paragraphs with images
- Uses `{@pagebreak}` to split into pages
- Step-by-step with visual aids

## Recommendations

### Title Writing
1. **Keep it short**: 2-4 words ideal, max 9 words
2. **Use the item/machine name**: Players recognize names instantly
3. **Add color codes**: `&6&l` for primary items, `&5&l` for magic/rare
4. **Reset formatting**: Always end with `&r`

### Subtitle Writing
1. **Use sparingly**: Only 25% of quests need subtitles
2. **Keep it brief**: 3-4 words ideal, max 11 words
3. **Add context**: Tier, category, or brief function
4. **Be consistent**: Use same pattern across similar quests

### Description Writing
1. **Default to 1 paragraph**: 86% of quests use single paragraph
2. **Aim for 35-50 words**: Median is 35 words per paragraph
3. **Use color codes**: Highlight key items with `&e`, `&6`, `&b`
4. **Explain the "what" and "how"**: What it does, how to use it
5. **Reset formatting**: Use `&r` after colored text

### When to Use Multiple Paragraphs
- **Complex builds**: Multiblocks, large structures (5-12 paragraphs)
- **Step-by-step tutorials**: Ore processing, automation (3-6 paragraphs)
- **Detailed explanations**: Machine configs, upgrade systems (2-4 paragraphs)

### When to Use Images
- **Complex builds**: Show the structure (AllTheModium: 31.5% usage)
- **GUI layouts**: Show where slots are (Mekanism: 13% usage)
- **Process diagrams**: Show ore processing flow (Mekanism tier guides)

### When to Use Pagebreaks
- **Very long tutorials**: 10+ paragraphs (1% of quests)
- **Multi-page guides**: Complex multiblock builds with multiple steps

## Anti-Patterns

1. **Overusing subtitles**: 75% of quests don't need them
2. **Long titles**: Max 9 words, but 2-4 is ideal
3. **Wall of text**: 86% of quests use 1 paragraph; don't write essays
4. **No color codes**: ATM10 uses colors extensively for readability
5. **Forgetting `&r`**: Always reset formatting after colored text
6. **Too many images**: Only 6.5% of quests have images; use sparingly
7. **Overusing pagebreaks**: Only 1% of quests need them; most fit on one page

## Chapter-Specific Patterns

### Tech Chapters (Mekanism, Create)
- **Titles**: Machine names (2-3 words)
- **Subtitles**: Tier labels, function descriptions (25-38% usage)
- **Descriptions**: Single paragraph, 30-50 words
- **Images**: Machine setups, process diagrams (13% usage)

### Progression Chapters (AllTheModium, ATM Star)
- **Titles**: Item/tier names (2-3 words)
- **Subtitles**: Rare (0-20% usage)
- **Descriptions**: Short paragraphs, 20-40 words
- **Images**: Visual guides for complex builds (31.5% in AllTheModium)

### Exploration Chapters (Twilight Forest)
- **Titles**: Location/boss names (2-3 words)
- **Subtitles**: Occasional context (34.5% usage)
- **Descriptions**: Single paragraph, 25-35 words
- **Images**: Rare (1.8% usage)

### Storage/Logistics (AE2)
- **Titles**: Component names (2 words)
- **Subtitles**: Frequent context (54.8% usage)
- **Descriptions**: Short paragraphs, 20-30 words
- **Images**: None (0% usage)

## Summary

ATM10 quest text is **concise, color-coded, and functional**:
- **Titles**: 2-4 words, item/machine names with color codes
- **Subtitles**: Optional (25% usage), 3-4 words for context
- **Descriptions**: 1 paragraph (86%), 35-50 words, explain what/how
- **Color codes**: Extensive use for readability (&6 for primary, &e for highlights)
- **Images**: Rare (6.5%), used for complex builds/tutorials
- **Pagebreaks**: Very rare (1%), only for multi-page guides

**Key principle**: Most quests are simple item/machine introductions. Complex tutorials are the exception, not the rule.
