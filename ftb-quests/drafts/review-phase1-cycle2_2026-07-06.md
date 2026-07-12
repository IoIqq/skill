# Review: Phase 1 Cycle 2 — Structural Issues (Draft)

**Reviewer:** Phase 1 Cycle 2 审查子 agent
**Date:** 2026-07-06
**Scope:** `.researched-packs.json5`, `micro-patterns.md`, `.research-lessons.md`

---

## Issue 1: Create: Astral 双条目导致计数膨胀 [中等]

**现状:** `.researched-packs.json5` 中 Create: Astral 出现两次：
- Cycle 1 条目 (line 69-76): `"name": "Create: Astral"`, `"source": "design-guide audit"`, `"configUrl": null`
- Cycle 2 条目 (line 140-148): `"name": "Create: Astral (raw data)"`, `"source": "GitHub"`, `"configUrl": "https://github.com/Laskyyy/Create-Astral"`

**影响:** 这种双条目方式是"17 packs"计数错误的直接成因。如果按"研究事件"而非"独立包"计数：11 (Cycle 1) + 5 (Cycle 2 新包) + 1 (Create: Astral raw data) = 17。但 Sources section 实际列出 15 个独立包。

**建议方案:**
- **方案 A（推荐）:** 更新 Cycle 1 条目的 `source` 和 `configUrl` 字段，将 `cycle` 保留为 1 但添加 `"upgradedIn": 2` 字段。删除 Cycle 2 的重复条目。
- **方案 B:** 保留双条目但在 notes 中明确标注 "SAME PACK as Cycle 1 entry — raw data upgrade, not a new pack"，并在所有计数中排除重复。

**不修正的原因:** 双条目保留了研究历史（何时获得了 raw data access），这对 future cycles 可能有价值。方案选择应由 skill 维护者决定。

---

## Issue 2: Arcana 条目未反映 Cycle 2 数据升级 [小]

**现状:** `.research-lessons.md` 的 Cycle 2 section 明确记录了 Arcana 的 raw data 升级：
> "Arcana — now has GitHub API access (AllTheMods/Arcana, 42 chapters). mainquestline_part_1 sampled (48 quests, 54 tasks, 96 rewards)"

但 `.researched-packs.json5` 中 Arcana 的 Cycle 1 条目仍然显示：
- `"source": "design-guide audit"`
- `"configUrl": null`

**影响:** 包注册表中的 Arcana 元数据与实际数据质量不一致。未来 agent 读取 JSON5 时会认为 Arcana 仅有 design-guide 级别的数据，而实际上已有 GitHub raw config 访问。

**建议:** 更新 Arcana 条目为 `"source": "GitHub"`, `"configUrl": "https://github.com/AllTheMods/Arcana"`，并添加 `"upgradedIn": 2` 标注。

---

## Issue 3: "17 packs" 计数错误 [已修正]

**问题:** `micro-patterns.md` 和 `.research-lessons.md` 中多处引用"17 shipped modpacks"和"High (17 packs)"，但 Sources section 仅列出 15 个独立包。

**修正记录:**
- `micro-patterns.md` line 26: "17 shipped modpacks" → "15 shipped modpacks"
- `micro-patterns.md` Scope Annotation Table: 9 处 "High (17 packs)" → "High (15 packs)"
- `.research-lessons.md` line 221: "all 17 packs" → "all 15 packs"
- `.research-lessons.md` line 252: "3 of 17 packs" → "3 of 15 packs"
- `.research-lessons.md` line 275: "11→17 packs" → "11→15 packs"

**根本原因:** 双条目计数（Create: Astral × 2）加上 Arcana raw data upgrade 被当作独立研究事件计数。

---

## 验证：独立包计数

以下是 Sources section 列出的 15 个独立包（按获取方式分类）：

**确认 config 访问 (8):**
1. ATM-10, 2. Create: Delight Remake, 3. Mechanomania, 4. ATM-9, 5. All-the-mods-10-Sky, 6. ATM-8, 7. All-the-Mons, 8. Create: Astral

**Design guide 审计数据 (7):**
9. Monifactory, 10. ATM9-Sky, 11. Arcana, 12. Prominence II, 13. Create Skylands, 14. Enigmatica 9 Expert, 15. ATM-11

**合计: 15 unique packs** (16 entries in JSON5 due to Create: Astral dual entry)
