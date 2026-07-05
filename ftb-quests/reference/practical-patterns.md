# FTB Quests 1.20.1 — Practical Patterns

Ready-to-use SNBT templates, debugging guide, and deployment checklist.

---

## Quest Templates

### 1. Simple Item Quest

```snbt
{
	id: "1234567890ABCDEF"
	x: 0.0d
	y: 0.0d
	size: 1.0d
	shape: "circle"
	dependencies: []
	title: "First Iron Ingot"
	subtitle: "Smelt your first iron"
	description: ["Iron is the backbone of early game. Smelt iron ore in a furnace to get started."]
	tasks: [
		{
			id: "234567890ABCDEF1"
			type: "item"
			item: "minecraft:iron_ingot"
			count: 1L
			consume_items: false
		}
	]
	rewards: [
		{
			id: "34567890ABCDEF12"
			type: "item"
			item: "minecraft:coal"
			count: 8L
		}
	]
}
```

### 2. Collection Quest (Multiple Items)

```snbt
{
	id: "A1B2C3D4E5F60001"
	x: 3.5d
	y: 0.0d
	size: 1.5d
	shape: "square"
	dependencies: ["1234567890ABCDEF"]
	title: "Starter Kit"
	subtitle: "Gather basic resources"
	description: ["Collect these essentials to build your first base."]
	tasks: [
		{ id: "B1C2D3E4F5060001", type: "item", item: "minecraft:oak_log", count: 64L }
		{ id: "C1D2E3F405060001", type: "item", item: "minecraft:cobblestone", count: 128L }
		{ id: "D1E2F30405060001", type: "item", item: "minecraft:iron_ingot", count: 32L }
	]
	rewards: [
		{ id: "E1F2030405060001", type: "xp", xp: 50L }
	]
}
```

### 3. Tutorial / Info Quest (Checkmark)

```snbt
{
	id: "F102030405060001"
	x: -3.5d
	y: 0.0d
	size: 1.25d
	shape: "circle"
	dependencies: []
	title: "Using JEI"
	subtitle: "Learn the recipe viewer"
	description: [
		"JEI shows all recipes in the game.",
		"Press R on an item to see recipes.",
		"Press U to see what it's used in.",
		"Bookmark items with A for quick access."
	]
	tasks: [
		{ id: "0102030405060001", type: "checkmark" }
	]
	rewards: [
		{ id: "1102030405060001", type: "item", item: "minecraft:book", count: 1L }
	]
}
```

### 4. Boss / Kill Quest

```snbt
{
	id: "2102030405060001"
	x: 7.0d
	y: 0.0d
	size: 2.0d
	shape: "diamond"
	dependencies: ["A1B2C3D4E5F60001"]
	title: "Dragon Slayer"
	subtitle: "Defeat the Ender Dragon"
	description: ["The Ender Dragon guards the End. Prepare well before this fight."]
	tasks: [
		{ id: "3102030405060001", type: "kill", entity: "minecraft:ender_dragon", count: 1L }
	]
	rewards: [
		{ id: "4102030405060001", type: "item", item: "minecraft:elytra", count: 1L }
		{ id: "5102030405060001", type: "xp_levels", xp_levels: 10L }
	]
}
```

### 5. Dimension / Biome Visit Quest

```snbt
{
	id: "6102030405060001"
	x: 10.5d
	y: 2.5d
	size: 1.5d
	shape: "pentagon"
	dependencies: ["2102030405060001"]
	title: "The Nether"
	subtitle: "Enter the Nether dimension"
	description: ["Build a nether portal with obsidian and flint & steel."]
	tasks: [
		{ id: "7102030405060001", type: "dimension", dimension: "minecraft:the_nether" }
	]
	rewards: [
		{ id: "8102030405060001", type: "item", item: "minecraft:blaze_rod", count: 8L }
	]
}
```

### 6. Convergence Capstone

```snbt
{
	id: "5102030405060002"
	x: 0.0d
	y: 0.0d
	size: 5.0d
	shape: "octagon"
	dependencies: ["6102030405060001", "9102030405060001", "A1B2C3D4E5F60001", "2102030405060001"]
	dependency_requirement: "all"
	title: "The Ultimate Artifact"
	subtitle: "Craft the pack's endgame item"
	description: ["You've mastered every system. Now combine them into one legendary item."]
	tasks: [
		{ id: "6102030405060002", type: "item", item: "mymod:ultimate_artifact", count: 1L }
	]
	rewards: [
		{ id: "7102030405060002", type: "xp_levels", xp_levels: 100L }
		{ id: "8102030405060002", type: "command", command: "/give @p minecraft:elytra{Enchantments:[{id:\"minecraft:unbreaking\",lvl:5}]}", permission_level: 2 }
	]
}
```

---

## Chapter Template

```snbt
{
	filename: "getting_started"
	group: ""
	order_index: 0
	icon: { id: "minecraft:book" }
	default_quest_shape: "circle"
	progression_mode: "default"
	default_hide_dependency_lines: false
	images: []
	quests: [
		{
			id: "0000000000000001"
			x: 0.0d
			y: 0.0d
			size: 2.0d
			shape: "hexagon"
			title: "Welcome!"
			subtitle: "Start your journey"
			description: ["Welcome to the pack! This chapter teaches the basics."]
			tasks: [ { id: "0000000000000002", type: "checkmark" } ]
			rewards: [ { id: "0000000000000003", type: "item", item: "minecraft:bread", count: 16L } ]
		}
		{
			id: "0000000000000004"
			x: 3.5d
			y: 0.0d
			size: 1.0d
			shape: "circle"
			dependencies: ["0000000000000001"]
			title: "First Tool"
			subtitle: "Craft a wooden pickaxe"
			description: ["Punch a tree for wood, craft planks, then make a pickaxe."]
			tasks: [ { id: "0000000000000005", type: "item", item: "minecraft:wooden_pickaxe", count: 1L } ]
			rewards: [ { id: "0000000000000006", type: "item", item: "minecraft:cobblestone", count: 32L } ]
		}
	]
}
```

---

## Localization (1.20.1 Inline)

In 1.20.1, text is **inline** in the quest object — no separate lang file:

```snbt
{
	title: "Quest Title"
	subtitle: "One-line description"
	description: [
		"First paragraph.",
		"Second paragraph with &6gold highlights&r."
	]
}
```

**Color codes:** `&0`-`&9`, `&a`-`&f` for color. `&l` bold, `&o` italic, `&r` reset.

| Code | Color | Common use |
|------|-------|------------|
| `&6` | Gold | Important items, primary emphasis |
| `&e` | Yellow | Highlights, tips |
| `&a` | Green | Positive, success |
| `&c` | Red | Danger, warnings |
| `&9` | Blue | Info, secondary |
| `&r` | Reset | End formatting |

**Item placeholders:** `{item.modid:name}` auto-renders localized item name.

---

## Debugging Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Quests don't appear | Invalid ID (top digit 8-F) | Use 0-7 as first hex char |
| Quests don't appear | Missing `id`/`x`/`y`/`tasks` | Add required fields |
| Quests don't appear | Commas in SNBT | Remove all commas |
| Dependencies missing | Referenced quest doesn't exist | Check dependency ID |
| Dependencies missing | Circular dependency | Run `--strict` validator |
| Rewards don't give items | Count inside item object | Move count to sibling field |
| Rewards don't give items | Invalid item ID | Verify in JEI/EMI |
| Text doesn't appear | Text in lang file (wrong for 1.20.1) | Move text inline |
| Shape not rendering | Invalid shape name or wrong case | Use lowercase names from reference |
| Chapter not in group | `group` mismatch | Use `group: ""` for single-group packs |

**Count field rule:** `count` is a SIBLING of `item`, not inside the item object.
```snbt
# Correct
tasks: [ { type: "item", item: "minecraft:apple", count: 3L } ]
# Wrong — count inside object is ignored
tasks: [ { type: "item", item: { id: "minecraft:apple", count: 3L } } ]
```

---

## Pre-Deployment Checklist

### Structure
- [ ] All IDs: 16 hex chars, first char 0-7
- [ ] All dependencies reference existing quests
- [ ] No circular dependencies
- [ ] Required fields present on every quest

### Content
- [ ] All item IDs verified in pack (check `.ftbq-cache/items.json5`)
- [ ] Count is sibling field (not inside item object)
- [ ] Task types match quest purpose
- [ ] Rewards scaled to quest difficulty

### Text
- [ ] Titles ≤4 words
- [ ] Descriptions 2-4 sentences
- [ ] Text inline (1.20.1)
- [ ] Color codes use `&r` to reset

### Layout
- [ ] No crossing dependency lines
- [ ] `hide_until_deps_visible` for chapters >30 quests
- [ ] Secret quests: `secret: true` + `shape: "rsquare"`

### Testing
- [ ] `validate_quests.py --strict` passes
- [ ] In-game `/ftbquests reload` — no chat errors
- [ ] Sample quests: tasks trigger, rewards grant
- [ ] Custom/KubeJS tasks verified in-game
