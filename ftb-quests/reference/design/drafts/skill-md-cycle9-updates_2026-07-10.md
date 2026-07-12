# SKILL.md Cycle 9 Proposed Modifications (Phase 5 Draft)

> **Status:** HIGH-RISK DRAFT — not yet applied to SKILL.md
> **Source:** Phase 4 Cycle 9 Reviewer C practicality assessment
> **Date:** 2026-07-10
> **Reviewer recommendation:** All 5 rules AI-heuristic, no new Gate needed, 3 additive modifications

---

## Modification 1 — Step 2 Interview (R46 + R49 + R50)

**Location:** Step 2 interview flow, after "Rewards & difficulty" branch
**Risk:** Low (additive — adds questions, doesn't change existing flow)

Add the following as a new branch at the end of Step 2's reward philosophy discussion:

```
**Questbook role (R46) — MANDATORY:**
"你的任务书主要扮演什么角色？"
- 伴生导航 (companion) — 任务书给方向，EMI/field guide 给细节
- 教程系统 (tutorial) — 任务书是主要教学工具
- 激励目录 (incentive_catalog) — 任务书是奖励分配器

This declaration determines R47 and R50 applicability.

**Collection-catalog check (R49) — CONDITIONAL:**
When user mentions collection/catalog chapters:
"这个 catalog 涵盖哪些 mod？这些 mod 的内容是否已稳定，还是仍在频繁更新？"
If > 3 actively developed mods or estimated > 200 quests → warn about maintenance cost.

**Zero-reward safety (R50) — CONDITIONAL:**
When user indicates zero or near-zero reward design:
Confirm 3 safety conditions:
(1) "是否有替代进度货币（电压等级、徽章、技能系统、Game Stages）？"
(2) "questbook 角色是否为 companion 或 catalog？"
(3) "包是否有强内在游戏循环（合成/收藏/战斗/探索）？"
All three must be yes for safe zero-reward design.
```

---

## Modification 2 — Step 4 Per-Node Self-Check (R47)

**Location:** Step 4 step 6 (AI generation self-check), after existing R23/AP10/AP11 checks
**Risk:** Low (INFO level, doesn't block generation)

Add as a new sub-check:

```
**Companion delegation (R47).** If `questbook_role == "companion"` and the
description contains recipe patterns ("X + Y → Z", "put X in Y", "smelt X
to get Y"), note as INFO — consider delegating to EMI/JEI. Reverse: if
`questbook_role == "tutorial"` and description says "check EMI/JEI for the
recipe", WARNING — tutorial mode should teach, not delegate.
```

---

## Modification 3 — Step 5 Summary Extensions (R46/R48/R49/R50)

**Location:** Step 5 summary output, after existing reward distribution report
**Risk:** Low (additive reporting, doesn't change validation logic)

Add conditionally-triggered report blocks:

```
**Questbook role stats (R46) — ALWAYS:**
📖 Questbook role: {declared_role}
📊 Reward density: {rewards/quests}
📋 Optional rate: {optional/total}
⚠️ Role consistency: {consistent/inconsistent} (if reward_density contradicts declared role)

**Port drift indicators (R48) — CONDITIONAL (when detected):**
🔀 Suspected ported quests: {count}
   - Foreign mod references: {n}
   - Foreign item namespaces: {n}
   - Reward outliers: {n}
   Review recommended before release.

**Catalog maintenance (R49) — CONDITIONAL (when chapter quests > 200):**
📦 Catalog chapter "{name}": {n} quests covering {m} mods
   Maintenance cost: {low/medium/high} based on mod update frequency

**Zero-reward safety (R50) — CONDITIONAL (when reward_density < 0.05):**
🚫 Zero-reward design detected. Safety check:
   ☐ Alternative progression currency: {yes/no}
   ☐ Questbook role: {companion/catalog/other}
   ☐ Strong intrinsic gameplay loop: {yes/no}
   Result: {SAFE / WARNING — missing conditions: ...}
```

---

## Implementation Notes

- **No new Gate** for Step 4 — Reviewer C confirmed R48's key checks are already covered by Gate 1 + R22/R23
- **R46 is the only mandatory addition** to Step 2; R49 and R50 are conditional triggers
- **All modifications are additive** — no existing flow is changed or removed
- **Recommended implementation order:** R46 (mandatory) → R50 (conditional) → R49 (conditional) → R47 (advisory) → Step 5 summary (last)
