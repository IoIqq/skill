# R27 — Description-Recipe Accuracy (DRAFT)

> **Status:** High-risk draft. Requires JEI/EMI runtime data to implement. Not included in active progression-rules.md until toolchain support is available.
> **Category:** Suggestion & Necessity (§7) — would extend AP1 coverage to the recipe-instruction dimension
> **Severity:** WARNING (when JEI data available) / INFO (heuristic fallback)

## What it checks

Whether quest `description` instructions about **how to craft/process an item** match the actual recipe mechanics. This covers cases where the description says "smelt in a furnace" but the item actually requires a blast furnace, or "combine X and Y in a mixer" but the recipe actually requires X, Y, and Z.

This is the "hard half" of AP1 (Description-Reality Mismatch) that R23 cannot cover:
- **R23** checks: does the item ID mentioned in description exist and match task/reward items?
- **R27** would check: are the crafting *instructions* in the description actually correct?

## Why it's hard

1. **Requires recipe data.** To verify "smelt iron ore → iron ingot", the checker needs to know the actual recipe for iron ingot (furnace recipe, input = iron ore, output = iron ingot). This data comes from JEI/EMI dumps or mod source code.
2. **Natural language parsing.** Descriptions use varied phrasing: "put it in the furnace", "smelt the ore", "process in a blast furnace at high temperature", "combine in a crafting table". Mapping these to structured recipe queries is an NLP problem.
3. **Multi-step recipes.** Some descriptions cover multi-step crafting chains. Verifying the entire chain requires recursive recipe expansion.

## Proposed implementation (when JEI/EMI data available)

```
# L3 data: recipe_data from JEI/EMI dump
# recipe_data[item_id] = {
#     "type": "smelting" | "crafting" | "machine" | ...,
#     "machine": "minecraft:furnace" | "mekanism:metallurgic_infuser" | ...,
#     "inputs": [...],
#     "outputs": [...]
# }

MACHINE_KEYWORDS = {
    "furnace": "minecraft:furnace",
    "blast furnace": "minecraft:blast_furnace",
    "smoker": "minecraft:smoker",
    "crafting table": "minecraft:crafting_table",
    "mixer": "create:mixer",
    "press": "create:mechanical_press",
    "crusher": "create:crushing_wheel",
    "infuser": "mekanism:metallurgic_infuser",
    "enrichment": "mekanism:enrichment_chamber",
    "chemical": "mekanism:chemical_infuser",
    "assembler": "oritech:assembler",
    "pulverizer": "thermal:pulverizer",
    "smelter": "thermal:induction_smelter",
}

for each quest Q:
    if not Q.description:
        continue
    desc_text = " ".join(Q.description)

    for item_task in Q.tasks:
        if item_task.type not in ("ftbquests:item", "item"):
            continue

        item_id = item_task.item.id
        if item_id not in recipe_data:
            continue

        actual_recipe = recipe_data[item_id]

        # Check: does description mention a machine that differs from actual?
        for keyword, machine_id in MACHINE_KEYWORDS.items():
            if keyword in desc_text.lower():
                if actual_recipe["machine"] and machine_id != actual_recipe["machine"]:
                    WARNING: "Quest {Q.name} description says '{keyword}'
                              but {item_id} actually requires
                              {actual_recipe['machine']}."
                    break

        # Check: does description mention input items that don't match recipe?
        mentioned_inputs = extract_mentioned_items(desc_text)
        actual_inputs = set(r["id"] for r in actual_recipe.get("inputs", []))
        wrong_inputs = mentioned_inputs - actual_inputs - {item_id}
        if wrong_inputs and actual_inputs:
            for wi in wrong_inputs:
                if wi in items_json5_all_ids:
                    INFO: "Quest {Q.name} description mentions '{wi}' as input
                           for {item_id}, but recipe uses: {actual_inputs}."
```

## Source evidence (from real issues)

1. **FTB Architect's Exodus #12549** — "Dominant Spark Augment is needed on the spark above the plate. This is incorrect: the plate will pull from mana pools with sparks without that augment." Description gives wrong crafting instruction for Botania's Terrestrial Agglomeration Plate.

2. **FTB Architect's Exodus #12569** — "Nature's Aura Guide Incorrectly States Where to Collect Aura." Description gives wrong location for a game mechanic.

3. **FTB Architect's Exodus #12557** — "Guideme shows wrong y level for emerald spawn." Description gives wrong numerical parameter.

4. **Create: Astral #618** — "Pressmarine Shards incorrectly states prismarine is used to automate veridium." Description mentions a crafting relationship that doesn't exist.

All four cases involve description text that gives incorrect instructions about game mechanics or crafting processes — R23 catches the item ID mismatch but not the instruction correctness.

## Activation criteria

This rule can be promoted from draft to active when:
1. The skill toolchain gains access to recipe data (JEI/EMI dump or mod source parsing)
2. A basic NLP mapping from description keywords to recipe machine types is implemented
3. The false-positive rate is validated below 10% on existing pack configs

## Related rules
- R23 — Description-Item Consistency (text matching, already active)
- R24 — Suggestion-Reachability (suggested items reachable, already active)
- R26 — Quest-Mod Version Consistency (hardcoded numbers, already active)
- R27 would complete the AP1 coverage triangle: text (R23) + suggestion (R24) + instruction (R27)
