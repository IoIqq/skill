# SKILL.md Cycle 18 Addendum — Proposed Changes (Phase 5 Review)

**Date:** 2026-07-18
**Status:** DRAFT — pending user approval before applying to SKILL.md
**Risk level:** HIGH (modifies core workflow Steps 3 and 4)

---

## Change B1: Step 3 — topology-coordinates.md reference update

**Insertion point:** After the existing Cycle 17 addendum (line ~406 in current SKILL.md), before the "IDs are computed automatically..." paragraph.

**Text to insert:**

```
**Cycle 18 addendum — topology expansion and trading-bypass defense.** Seven new topology cases (Cases 55–61), 8 new progression rules (R117–R124), and MP72 formal reclassification to TeamAOF-Specific. Key updates for scaffold:

1. **Topology reference is now comprehensive.** `reference/design/topology-coordinates.md` covers 61 real-world cases across 6 topology types (linear_chain, hub_fan, parallel_columns, tree_branching, diamond_convergence, grid_catalog) plus highway_branch. The document includes complete layout algorithms, constraint formulas, and calibrated coordinate data for each type. When selecting a topology in Step 3, walk through the Phase 2 classifier thresholds against the chapter's outline, then use the Phase 3 coordinate assignment strategy matching the selected type.
2. **Cases 55–57 same-pack caveat.** Three new GhostLand8 cases (create: 206 quests, mekanism: 116 quests, food_and_farming: 47 quests) provide the largest single-pack sample in the dataset. However, all three come from one team (Team-GhostLand) — design choices may be team-specific rather than representative of ATM-derivative packs generally. Cross-validate against independent packs before adopting GhostLand8 patterns as universal.
3. **New calibration extremes.** Engineers-Life-2 first_steps (120 quests, 39.5-unit width) is the widest non-expert chapter — exceeds R59 hard clamp. umodpack mystical_agriculture (130 quests, 86.2% hide_dep_lines) sets the extreme-suppression record. Endless-Rise-Remastered stoneage (75 quests) introduces custom shape textures (tech_circle, tech_square, tech_smooth_square) — first pack where the chapter-level default quest shape is a custom shape name.
```

---

## Change B2: Step 4 — progression verification reasoning step update

**Insertion point:** After the existing Cycle 17 progression architecture check block (line ~584 in current SKILL.md), before the "Three new tensions from Cycle 17" paragraph.

**Text to insert:**

```
**Progression architecture check (Cycle 18 — trading bypass defense and author process rules R117–R124).** After the Cycle 17 architecture check, run the following additional validations. These 8 rules derive from Cycle 18 Phase 3 research across 9 platforms (MC百科, klpbbs.com, Bilibili, Reddit, CSDN, GitHub, mczfw.com, 知乎, MineBBS); they are advisory at generation time and formal in Step 5's whole-book pass. Route by pack type:

- **all packs:** R117 (villager trade progression gating — check item-submission tasks against L1 heuristic fallback for commonly tradeable items), R124 (author playtesting reminder — include as output note when generating complete packs)
- **expert packs:** R119 (tech-level continuous scale — requires custom mod/scripting framework, not standard FTB Quests), R115 (container-level recipe locking, from Cycle 17)
- **semi-gated packs:** R117 (trade gating + Profession Lock verification), R118 (acquisition-method verification layer)
- **kitchen-sink packs:** R122 (flow clarity — verify primary spine exists for >50 mod packs), R123 (open-gating compensatory defense — if pack uses open-gating philosophy)
- **adventure/dimension packs:** R121 (equipment tier transition smoothness — use vanilla tier order as proxy for mod items)

Key notes:
- **R117 L1 heuristic fallback:** When villager trading tables are not inspectable (the common case), flag these item categories as `POTENTIAL_TRADING_BYPASS`: enchanted books, emeralds/emerald blocks, glass/stained glass, crops (wheat, carrots, potatoes, beetroot), books/paper/maps. Every task item must answer "玩家此刻怎么拿到这个？" — if the item is in the L1 fallback list and the pack uses any stage gating, surface a WARNING.
- **R10 reward-to-dependent bridge:** Every reward must answer "这个奖励引导玩家去做什么？" — if the answer is unclear, mark as WARNING and list in the output summary. This check was already in Step 4's mandatory progression reasoning (Gate 2); Cycle 18 reinforces it as a required output annotation.
- **R119/R120 are design guidance, not executable checks.** R119 (continuous tech level) requires a custom mod like Nova Engineering's HyperNet. R120 (narrative research) requires 100+ original content pieces. Both are documented as design possibilities for reference, not recommendations for typical packs.
- **R121 uses vanilla tier proxy.** Combat balance data is not in quest config — use vanilla tier order (wood < stone < iron < diamond < netherite) as proxy for mod items when evaluating equipment tier transitions.
- **R124 severity downgraded to INFO.** Author playtesting is an author process requirement, not a verifiable config check. Include as a reminder in the output footer when generating complete packs.
```

---

## Change B3: Standalone Cycle 18 addendum

**Insertion point:** At the end of Step 4's progression architecture section (after the Cycle 18 rules block from B2), or as a top-level addendum note similar to existing Cycle 16/17 patterns.

**Text to insert:**

```
**Cycle 18 addendum: R117–R124 新增。AP42–AP46 新增。MP72 重分类为 TeamAOF-Specific。**
trading bypass 防御框架：R117 (trade gating) + R118 (acquisition verification) + R123 (open-gating defense)。三规则形成分层防御：expert 包用 R117+R118 强制阻断，semi-gated 包用 R117 限制关键物品，open-gating 包用 R123 补偿防御。
详见 `reference/design/progression-rules.md` R117–R124。

新增 anti-patterns: AP43 (unplaytested release), AP44 (kitchen-sink overwhelm), AP45 (reward timing mismatch), AP46 (quest narrative disconnection)。
新增 micro-patterns: MP74 (custom shape texture registration, Validated-by-Absence), MP75 (extreme dependency line suppression, Partially-Validated)。
新增 tension pairs: T10 (streamlining vs. variety), T11 (narrative vs. traditional progression), T12 (open-gating freedom vs. integrity)。

MP75 缩放公式已降级为推测性指导（审查修正 A1）：仅 umodpack mystical_agriculture (130 quests, 86.2%) 为实测数据点，150+ quests 的缩放无经验数据支撑。
```

---

## Implementation notes

These three changes (B1, B2, B3) are additive — they append new content without modifying existing text. The existing Cycle 16 and Cycle 17 addenda remain untouched. The new Cycle 18 addendum follows the same structural pattern as prior cycle addenda.

**Reviewer cross-references applied:**
- A1 (MP75 formula downgrade) → reflected in B3 text
- A2 (R117 L1 fallback) → reflected in B2 text
- A3 (R119/R121/R124 design guidance) → reflected in B2 text
- A4 (Cases 55-57 same-pack risk) → reflected in B1 text
- A5 (R119/R120 prerequisites) → reflected in B2 text
- A6 (R124 deliberate bypass) → reflected in B2 text (R124 severity note)
