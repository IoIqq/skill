# Task Type Distribution — ATM10 Empirical Analysis

**Source:** 722 tasks across 10 ATM10 chapters (2026-07-04)

## Key Findings

### Overall Distribution (722 tasks)

| Task Type | Count | Percentage |
|-----------|-------|------------|
| `item` | 680 | 94.2% |
| `checkmark` | 21 | 2.9% |
| `advancement` | 8 | 1.1% |
| `dimension` | 7 | 1.0% |
| `structure` | 2 | 0.3% |
| `kill` | 2 | 0.3% |
| `productivebees:soul_lava` | 1 | 0.1% |
| `biome` | 1 | 0.1% |

**Pattern:** ATM10 is overwhelmingly item-focused (94.2%). This reflects its identity as a crafting/tech kitchen-sink pack.

### Distribution by Chapter Type

#### Tech Chapters (create, mekanism, ae2) — 337 tasks
- `item`: 97.9% (330 tasks)
- `checkmark`: 1.8% (6 tasks)
- `advancement`: 0.3% (1 task)

**Insight:** Tech chapters are almost pure item tasks. Players craft/automate items to progress.

#### Tutorial Chapter (welcome) — 7 tasks
- `checkmark`: 85.7% (6 tasks)
- `dimension`: 14.3% (1 task)

**Insight:** Tutorial chapters use checkmark tasks for "read this and acknowledge" style quests.

#### Progression Chapters (allthemodium, star, main) — 241 tasks
- `item`: 90.5% (218 tasks)
- `checkmark`: 2.9% (7 tasks)
- `dimension`: 2.5% (6 tasks)
- `advancement`: 1.7% (4 tasks)
- `structure`: 0.8% (2 tasks)
- `kill`: 0.8% (2 tasks)
- `productivebees:soul_lava`: 0.4% (1 task)
- `biome`: 0.4% (1 task)

**Insight:** Progression chapters have the most task variety. They mix item tasks with dimension/structure/kill/biome to create diverse gameplay.

#### Exploration Chapters (twilight, food) — 137 tasks
- `item`: 96.4% (132 tasks)
- `advancement`: 2.2% (3 tasks)
- `checkmark`: 1.5% (2 tasks)

**Insight:** Exploration chapters are mostly item-focused but use advancement tasks to track milestones (e.g., "defeat the Lich").

## Design Principles

### Principle 1: Default to Item Tasks

**Rule:** Start with `item` tasks as the default (94% of the time).

**Rationale:** ATM10 is a crafting pack. Most quests ask players to craft, collect, or automate items.

**Exception:** Tutorial chapters should use `checkmark` tasks (85% of the time).

### Principle 2: Match Task Type to Chapter Purpose

| Chapter Type | Primary Task | Secondary Tasks | Rationale |
|--------------|--------------|-----------------|-----------|
| Tech | `item` (98%) | `checkmark` (2%) | Craft/automate items |
| Tutorial | `checkmark` (86%) | `dimension` (14%) | Read and acknowledge |
| Progression | `item` (91%) | `dimension`, `structure`, `kill` (9%) | Mixed gameplay |
| Exploration | `item` (96%) | `advancement` (4%) | Collect items, track milestones |

### Principle 3: Use Special Task Types Sparingly

**Rule:** `dimension`, `structure`, `kill`, `biome` should each appear in <3% of tasks.

**Rationale:** These task types are "spice" — they add variety but shouldn't dominate. Overuse creates confusion.

**When to use:**
- `dimension`: When the quest is about reaching a new dimension (e.g., "Enter the Nether")
- `structure`: When the quest is about finding a specific structure (e.g., "Locate a Stronghold")
- `kill`: When the quest is about defeating a boss (e.g., "Kill the Ender Dragon")
- `biome`: When the quest is about exploring a specific biome (e.g., "Visit a Mushroom Island")
- `advancement`: When the quest is about reaching a vanilla milestone (e.g., "Get Diamonds")

### Principle 4: Checkmark Tasks for Information

**Rule:** Use `checkmark` tasks for "read this" or "acknowledge this" quests.

**Examples:**
- Tutorial: "Welcome to ATM10! (checkmark)"
- Mod introduction: "This mod adds X, Y, Z (checkmark)"
- Lore: "The ATM Star requires... (checkmark)"

**Anti-pattern:** Don't use checkmark tasks for actual gameplay. If the player needs to DO something, use an `item` task.

### Principle 5: Advancement Tasks for Vanilla Milestones

**Rule:** Use `advancement` tasks when the quest aligns with a vanilla Minecraft advancement.

**Examples:**
- "Get Diamonds" → `advancement: minecraft:story/mine_diamonds`
- "Enter the Nether" → `advancement: minecraft:story/enter_the_nether`
- "Defeat the Ender Dragon" → `advancement: minecraft:end/kill_dragon`

**Pattern:** ATM10 uses advancement tasks in 1.1% of quests, mostly in progression and exploration chapters.

## Implementation Guide

### When Generating a Chapter

1. **Identify chapter type:** Tech, Tutorial, Progression, or Exploration
2. **Set task distribution:**
   - Tech: 98% item, 2% checkmark
   - Tutorial: 86% checkmark, 14% dimension
   - Progression: 91% item, 9% mixed (dimension/structure/kill/biome)
   - Exploration: 96% item, 4% advancement
3. **For each quest:**
   - 90% of the time: use `item` task
   - 3% of the time: use `checkmark` task (if information/acknowledgment)
   - 2% of the time: use `dimension` task (if dimension-related)
   - 2% of the time: use `advancement` task (if vanilla milestone)
   - 1% of the time: use `structure`/`kill`/`biome` (if specific gameplay)
   - 2% of the time: use `checkmark` task (if tutorial/info)

### Example: Generating a Tech Chapter

```python
for quest in tech_quests:
    if random.random() < 0.98:
        task_type = "item"
        task_item = choose_relevant_item(quest)
    else:
        task_type = "checkmark"
        task_description = "Read this information"
```

### Example: Generating a Tutorial Chapter

```python
for quest in tutorial_quests:
    if random.random() < 0.86:
        task_type = "checkmark"
        task_description = quest.info_text
    else:
        task_type = "dimension"
        task_dimension = "minecraft:overworld"
```

## Anti-Patterns

1. **100% item tasks:** Even tech chapters have 2% checkmark tasks. Pure item tasks feel monotonous.
2. **Too many special tasks:** If >10% of tasks are dimension/structure/kill/biome, the chapter feels unfocused.
3. **Checkmark tasks for gameplay:** "Kill 10 zombies (checkmark)" is wrong. Use `kill` task.
4. **Advancement tasks for mod content:** Advancement tasks are for vanilla milestones only.
5. **Ignoring chapter type:** A tech chapter with 50% checkmark tasks is wrong. Match task distribution to chapter purpose.

## Comparison: ATM9 vs ATM10

(Note: ATM9 analysis pending. Expected differences:)
- ATM9 (expert pack): May have more `advancement` tasks for gating
- ATM9 (older version): May have different task type availability
- ATM9 (focused progression): May have less task variety overall

**TODO:** Analyze ATM9 task distribution when data is available.

## Empirical Benchmarks

### ATM10 Create (Tech)
- 99 tasks, 100% item
- **Feel:** Pure crafting/automation

### ATM10 Welcome (Tutorial)
- 7 tasks, 85.7% checkmark, 14.3% dimension
- **Feel:** Informational, "read this"

### ATM10 AllTheModium (Progression)
- 52 tasks, 78.8% item, 11.5% dimension, 5.8% checkmark, 3.8% structure
- **Feel:** Mixed gameplay, exploration + crafting

### ATM10 Twilight Forest (Exploration)
- 100 tasks, 97% item, 3% advancement
- **Feel:** Collect items, track boss kills via advancement

## Conclusion

ATM10's task distribution reflects its identity as a crafting-focused kitchen-sink pack:
- 94.2% item tasks (crafting/automation focus)
- 2.9% checkmark tasks (information/tutorial)
- 1.1% advancement tasks (vanilla milestones)
- 1.8% special tasks (dimension/structure/kill/biome for variety)

**Key takeaway:** Default to item tasks, but add 5-10% variety based on chapter type.
