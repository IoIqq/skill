# mod-reward-design

> **Core question:** 奖励什么？它引导玩家去哪？
> **Lines:** ~290 | **Step 2 load:** partial | **Step 4 load:** yes | **Step 5 load:** yes

## Quick Reference

| ID | Title | Phase | Severity | Pack types |
|---|---|---|---|---|
| MP14 | Material Bridge | Step 4 | -- | all |
| MP15 | Tool Reward | Step 4 | -- | all |
| MP16 | XP Drip | Step 4 | -- | kitchen-sink |
| MP17 | Hub Concentration | Step 2 | -- | create, kitchen-sink |
| MP18 | Choice Reward | Step 4 | -- | expert, story |
| MP29 | Command Reward | Step 4 | -- | expert, story |
| MP34 | Loot Table Reward | Step 4 | -- | all |
| AP6 | Dead-End Reward | Step 2/4 | High | all |
| AP8 | Reward Inflation | Step 2 | High | all |
| AP17 | XP-Level Reward Relativity | Step 2/4 | Medium | all |
| AP18 | Reward Desert in Long Chains | Step 2/4 | Medium | all |
| R10 | Reward-to-Dependent Bridge | Step 4/5 | P1 | all |
| R11 | Reward-Target Accuracy | Step 5 | P1 | all |
| R12 | Reward Value Progression | Step 5 | P2 | all |
| R13 | Capstone Reward Magnitude | Step 5 | P2 | all |
| R28 | Command Reward Safety Scan | Step 4 | P0 | all |
| R31 | XP-Level Reward Relativity | Step 4 | P2 | all |
| PP2 | Backward Shortcut | Step 2 | -- | all |
| PP6 | Wrong Tool Reward | Step 4 | -- | all |

---

## Patterns

### MP14 — Material Bridge

Reward IS the next quest's ingredient. Quest N rewards an item; Quest N+1 (depends_on N) requires that item as a task. Reward count matches or slightly exceeds the next quest's requirement. The most natural bridging pattern — appears across all pack genres.

In kitchen-sinks the bridge is often a mod's signature intermediate (e.g. Mekanism osmium ingot). In expert packs the bridge is tighter: reward count exactly matches the next recipe's input count, no waste. ATM-10 AE2 chapter: Quest 1 rewards 10 XP; Quest 2 (charger + inscriber) rewards 3 iron + 50 XP; Quest 3 (meteorite compass) rewards 4 sky_stone + 100 XP — each reward facilitates the next step.

**Source:** ATM-10 `applied_energistics_2.snbt`.

### MP15 — Tool Reward

Reward unlocks the next activity. The reward is a durable tool (pickaxe, wrench, guide book, machine block), not a consumable. Next quest's task requires using that tool. Count is typically 1. Common at section boundaries — "here's your new tool, now go use it."

Create: Delight Feast_Afoot: tutorial quests reward hygrometer, watering can, cooking pot — each immediately precedes a quest requiring that tool. ATM-10 AllTheModium root rewards the Patchouli guide book (reference for all subsequent recipes).

### MP16 — XP Drip

Small XP on every quest as baseline; milestone quests give larger XP or XP-level rewards. The XP is not enough to "buy" progression but enough to feel steady advancement.

> **ATM Signature:** ATM-10 uses 10/50/100 XP tiers extensively (6,915 rewards / 4,601 quests = 1.5/quest). Expert packs (Monifactory) and Create packs (0.43 and 0.11 rewards/quest) do not center their reward economy on XP drip. For ATM-specific implementation data, see `mod-atm-signature`.

**Universal concept:** A small consistent reward alongside primary item rewards prevents "reward desert" feelings in long chains. Even non-XP-drip packs benefit from a baseline reward on every quest — the type (XP, material, currency) varies by genre.

### MP17 — Hub Concentration

Sparse cells, rich hubs. Cell quests (majority) have no rewards or minimal single-item rewards. Hub quests (minority) have rich rewards: multiple items, XP, random loot, or choice rewards. Hub depends_on ALL its cells.

Prevents reward inflation in large catalogs. Create: Delight Mouse_Chef: 304 cells have item×29 + xp×52 (sparse); 12 category hubs carry the most valuable rewards. Ratio: ~1 reward per 4 cells.

### MP18 — Choice Reward

Branch-point fork — reward IS the choice. Quest with a `choice` reward (or multiple `item` rewards with autoclaim disabled). Description explains options. After the choice, selected item becomes the task for the chosen path's first quest.

Rare in kitchen-sinks ("do everything" philosophy). Appears in expert and RPG packs. Create: Delight uses 13 `choice` rewards across 2,295 quests at key branching points.

### MP29 — Command Reward

Server-side invisible logic. `command` reward with `command: "/<command>"` and `player: "{p}"`. Runs server-side when quest is claimed. Common commands: `/gamestage add {p} <stage>`, `/effect give`, `/tp`, `/give`.

**Safety rules (basics):** (1) Never use `/op`, `/gamemode creative`. (2) Test every command in single-player first. (3) Prefer standard reward types — use `item` instead of `/give`, `xp` instead of `/xp`. (4) Verify gamestage names against config — typos create silent failures. Full safety scan defined in R28 below.

Monifactory's `dependency_chain` chapter uses 26 gamestage tasks + 26 command rewards as dedicated routing. E9E: 56 command rewards in `chapter_one` alone (83% of reward sections). Visible quest book stays clean; invisible logic runs through command rewards.

### MP34 — Loot Table Reward

Randomized reward via reward tables. `reward_tables[]` entry with weighted pools; quest reward uses `type: "random"` with `table_id`. When claimed, FTB Quests rolls the table.

**Complementary to MP14-MP18:** Deterministic bridges (material, tool) ensure the player always has the next step's ingredient; loot tables add variety and excitement on top. A quest can have both. Every tier in the loot table should be useful at the quest's stage. Calibrate worst-case roll to still provide progression value.

`table_id` is a decimal **long** — in the spec, use `table: "<name>"` and let the generator resolve.

---

## Anti-Patterns

### AP6 — Dead-End Reward

Reward has no connection to anything the player does next. Not a material bridge, not a tool, not XP or currency. It's a trophy sitting in the inventory.

**Root cause:** Reward chosen for thematic reasons ("this quest is about forestry, reward is a sapling") rather than progression reasons ("reward is the charcoal the next quest needs").

**Fix:** For every reward ask: does it help with the NEXT quest? If not, replace with material bridge (MP14), tool reward (MP15), XP (MP16), or choice reward (MP18). Cosmetic rewards only on truly optional quests.

**Variant — Mod-Unification Trap (PP7):** Reward is "steel dust" but from the wrong mod namespace (FTB Materials vs Modern Industrialization). Same display name, incompatible recipes. Cross-ref PP7 in mod-teaching-pacing.

### AP8 — Reward Inflation

Early quests give generous rewards; mid-game "runs out" of meaningful rewards. Player's chest overflows from early quest rewards; late-game quests offer things the player doesn't need.

**Root cause:** Reward curve not planned as a whole-book economy. Each chapter's author chose rewards independently.

**Fix:** Plan reward economy at book level. Define tiers (early/mid/late/endgame). Early: tools + small quantities (1-4 items). Mid: moderate stacks (8-16). Late: rare materials or unique items. Use XP drip (MP16) as universal baseline. Reserve richest rewards for capstones (MP8). Cap per-chapter reward budgets.

### AP17 — XP-Level Reward Relativity

`xp_levels` rewards create wildly inconsistent value depending on player level at claim time. +3 XP Levels can be worth 27 XP (low level) or thousands (high level). Players hoard unclaimed rewards and batch-claim at high levels.

**Root cause:** Minecraft's XP curve is exponential. Fixed level reward = variable actual XP.

**Fix:** Use raw `xp` (fixed point value) for routine quests. Reserve `xp_levels` for milestone/capstone quests only. If `xp_levels` must be used on routine quests, pair with `exclude_from_claim_all: true`.

**Source:** Craftoria #289 — dozens of quests across multiple chapters affected.

### AP18 — Reward Desert in Long Chains

Player progresses through multiple tiers without receiving any relevant rewards. After 3 tiers of reactors: no reward items, no XP, no materials. Quest book becomes a pure checklist with no incentive.

**Root cause:** Chain designed as pure gating without interleaving rewards.

**Fix:** Every 2-3 quests in a chain should have at least one relevant reward (MP14, MP15, or MP16). After a tier transition, reward a material or efficiency upgrade. For chains >5 quests without branching, place a milestone reward at the midpoint.

**Source:** Craftoria #231 — Powah chapter "throws everything at you" with 3 tiers and no rewards between them.

---

## Rules

### R10 — Reward-to-Dependent Bridge

**Step 4 priority:** P1 (reverse check)
**Step 5 priority:** P1 (forward check)

Checks whether quest rewards appear in dependent quests' tasks. For each quest Q with item rewards: does any dependent quest require that reward item as a task? Tolerances: terminal quests (no dependents) skip; XP/loot/choice rewards skip; tool rewards and currency rewards are universal bridges.

```
for each quest Q:
    dependents = find_dependents(Q)
    if not dependents: continue
    for reward in item_rewards(Q):
        if reward_id not in any dependent's tasks:
            if not is_tool/reward/currency/loot:
                INFO: "Reward {reward_id} has no dependent bridge."
```

Step 4 runs reverse check (task -> ancestor reward). Step 5 runs full forward check.

### R11 — Reward-Target Accuracy (Wrong Tool Detection)

**Step 5 priority:** P1

When a quest rewards a tool (wrench, hammer, guide book), checks if it's the tool the dependent quest actually needs. Uses `tool_category_map` to group same-function tools by mod.

```
if reward.item.id in tool_category_map:
    needed_tool = extract_from_dependent_description()
    if needed_tool in same category but different mod:
        WARNING: "Wrong tool variant rewarded."
```

This catches "IE hammer vs Oritech wrench" — the multi-mod kitchen-sink problem where 5 mods each provide their own wrench.

### R12 — Reward Value Progression

**Step 5 priority:** P2

Checks whether reward value increases with quest difficulty (dependency_depth). For each chapter, sorts quests by depth, estimates reward value (rarity x count), flags significant drops (>50% decrease at higher depth).

Soft check (INFO level) because value estimation is imprecise and some quests intentionally give low rewards (acknowledgement gates).

### R13 — Capstone Reward Magnitude

**Step 5 priority:** P2

Capstone quests (dependencies >= 5) should have reward value >= 3x the chapter average. Capstone is the chapter's climax — reward should be memorable.

ATM-10 ATM Star: 50 ATM Star Shards + Patrick Star + 50 XP levels. The richest reward in the entire pack, on the hardest quest.

### R28 — Command Reward Safety Scan

**Step 4 priority:** P0

Static analysis of command reward strings. Three tiers:

**FORBIDDEN (ERROR):** `/op`, `/deop`, `/gamemode creative|spectator`, `/stop`, `/kick`, `/ban`, `/whitelist`

**HIGH-RISK (WARNING):** `/fill`, `/setblock`, `/clone`, `/clear`, `/kill`, high-amplifier effects (>=5), `/summon.*wither`, `/execute`

**IDEMPOTENCY RISK (INFO):** `/give`, `/tp`, `/playsound` — re-claiming duplicates the effect.

Additional checks: (1) Commands affecting a player must use `{p}` placeholder — hardcoded names break multiplayer. (2) Coordinate-based commands (`/tp`, `/setblock`, `/fill`) should specify target dimension explicitly.

This rule runs at Step 4 (per-node) because command strings are local data. FORBIDDEN commands block spec write.

### R31 — XP-Level Reward Relativity

**Step 4 priority:** P2

Checks if `xp_levels` rewards appear only on milestone quests. Non-milestone quests with `xp_levels` trigger WARNING: reward value drifts with player level, creating inconsistent economy.

Milestone detection heuristic: dependents >= 3, OR capstone, OR size > 1.5x chapter median, OR shape in (gear, pentagon, hexagon, diamond).

---

## Player-Perspective

### PP2 — Backward Shortcut

Best reward moments don't just give something new — they give a way to do something already done, but faster. After reaching a milestone, the player unlocks an efficiency loop back to earlier content.

**Config implication:** Milestone rewards should include at least one backward-optimizing element: a machine that automates an earlier manual process, a tool that speeds up earlier gathering, or an alternative recipe using more abundant materials. Stronger than raw materials because it compounds over time.

### PP6 — Wrong Tool Reward

Reward is a tool that seems relevant but is from the wrong mod for the pack's specific combination. "Why did I get an IE hammer? Next quest needs an Oritech wrench."

**Config implication:** When rewarding a tool, verify the specific tool ID matches what the next quest's description or task requires. In multi-mod packs, each mod's wrench is a distinct item with distinct recipes. Don't assume "a wrench is a wrench."

---

## Cross-References

| This module's ID | Related in other modules | Relationship |
|---|---|---|
| MP14 Material Bridge | mod-teaching-pacing R17 | Tool reward often bridges alongside material bridge |
| MP15 Tool Reward | mod-teaching-pacing R17 | Tool-Reward-Before-Use ordering rule |
| MP16 XP Drip | mod-atm-signature | ATM-specific implementation data lives there |
| MP29 Command Reward | mod-teaching-pacing MP23 | Invisible Infrastructure uses command rewards heavily |
| AP6 Dead-End Reward | mod-teaching-pacing PP5 | Dead-end rewards worsen the Context Void |
| AP8 Reward Inflation | mod-teaching-pacing MP19 | Chapter-as-Stage defines budget boundaries |
| AP18 Reward Desert | mod-teaching-pacing R19 | Bottleneck Spacing detects reward deserts |
| R10 Bridge | mod-teaching-pacing R14 | Teach-Then-Do ordering affects reward flow direction |
| R28 Command Safety | mod-safety-systems | Full AP15 side-effect analysis lives there |
| PP6 Wrong Tool | mod-teaching-pacing PP5 | Both stem from insufficient mod-awareness |
