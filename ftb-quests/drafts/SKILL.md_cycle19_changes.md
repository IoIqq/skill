# SKILL.md Cycle 19 Addendum — Proposed Changes (Phase 5 Review)

**Date:** 2026-07-19
**Status:** DRAFT — pending user approval before applying to SKILL.md
**Risk level:** HIGH (modifies core workflow Steps 3, 4, and 5)

---

## Change B1: Step 3 — topology-coordinates.md reference update

**Location:** Step 3 (Scaffold the skeleton)
**Insertion point:** After the existing Cycle 17 addendum (line 405 in current SKILL.md), before the "IDs are computed automatically..." paragraph (line 407).

**Text to insert:**

```
**Cycle 19 addendum — topology expansion, textural naming, and sub-1.0 sizing.** Ten new topology cases (Cases 62–71), two new micro-patterns (MP76, MP77), and one new anti-pattern (AP47). Key updates for scaffold:

1. **Topology reference now covers 71 real-world cases.** `reference/design/topology-coordinates.md` has been expanded with 10 new cases spanning all seven topology types. When selecting a topology in Step 3, walk through the Phase 2 classifier thresholds against the chapter's outline as before, but also check the new cases for closer analogues — the expanded dataset improves coverage for under-represented pack archetypes (adventure/RPG, skyblock, farming/lifestyle).
2. **MP76 — Textural Shape Naming [Validated].** Custom shape textures (e.g., `tech_circle`, `tech_square`, `tech_smooth_square`, `magic_rune`) are now recognized as a semantic layer on top of the topological shape vocabulary. When a pack registers custom shape textures at the chapter level (via `default_quest_shape` or per-quest `shape`), the texture name encodes thematic intent beyond the topology type. During scaffold, if the pack uses custom shape textures, record the texture name in the spec's `shape` field and note the thematic category in the chapter outline comment. See `reference/design/micro-patterns.md` §MP76 for the validated texture-name catalog.
3. **MP77 — Sub-1.0 Size Compression for High-Density Chapters [Validated].** Chapters exceeding 60 quests within a bounded viewport (R59's 35×30 unit limit) may use `size` values below 1.0 (typically 0.6–0.8) to maintain collision-free spacing without exceeding the viewport. This is a controlled exception to the default `size: 1.0` convention — apply only when: (a) the chapter exceeds 60 quests, AND (b) the Phase 3 coordinate assignment produces collisions at size 1.0 that R58 cannot resolve within the R59 bounding box. Document the compressed size in the chapter-level spec comment. See `reference/design/micro-patterns.md` §MP77 for the sizing formula and calibration data.
4. **AP47 — R59 Double-Axis Violation.** A new anti-pattern: when a chapter exceeds the R59 bounding box limit on BOTH axes simultaneously (width > 35 AND height > 30), indicating uncontrolled growth in two dimensions. This is distinct from a single-axis overshoot (which R59 already catches as P1). Double-axis violation indicates a fundamental topology mismatch — the chapter needs either decomposition (MP73) or a topology type change, not just spacing compression. Severity: ERROR. See `reference/design/progression-rules.md` §AP47.
```

---

## Change B2: Step 4 — progression verification reasoning step update

**Location:** Step 4 (Polish one node at a time — the loop)
**Insertion point:** After the Cycle 17 tensions block (line 584 in current SKILL.md), before the "**Batching by chapter:**" paragraph (line 586).

**Text to insert:**

```
**Progression architecture check (Cycle 19 — three-hard-problem defense rules R125–R130).** After the Cycle 17 architecture check, run the following additional validations. These 6 rules derive from Cycle 19 Phase 3 research across 12+ platforms (MC百科, Bilibili, CSDN, GitHub, Reddit, cesspit.net, klpbbs.com, mczfw.com, FTB Docs, awesome-packdev); they are advisory at generation time and formal in Step 5's whole-book pass. Route by pack type:

- **all packs:** R126 (quest task detection alignment — ERROR severity, binary check), R128 (backward-facing shortcut principle — INFO, design guidance)
- **kitchen-sink packs:** R125 (reward progression-trivialization — WARNING, with scarcity-list defense), R127 (cross-dimension item usability — WARNING), R130 (item-as-currency consistency — WARNING, only if pack uses currency economy)
- **expert packs:** R125 (reward progression-trivialization — stricter threshold, capability rewards must be restrained), R129 (quest-as-stage-trigger integration — INFO, only if using Game Stages)
- **semi-gated packs:** R125 (moderate threshold), R129 (if using stage framework)
- **adventure/dimension packs:** R127 (cross-dimension item usability — priority check, multi-dimension chapters)

Key notes:
- **R125 mandatory per-reward reasoning:** Every reward must answer "这个奖励会导致进度琐碎化吗？" before writing to spec. Three-level trivialization check: (1) Does the reward nullify a deliberately-crafted scarcity system? (scarcity-list check — if the pack defines scarce resources, rewards that trivialize their acquisition are WARNING); (2) Is the reward a capability item (unlocks a new ability dimension) rather than a utility item (improves existing ability)? Capability rewards require stricter gating even in kitchen-sink packs; (3) Does the reward's time-value ratio exceed the chapter's median by >3×? (outlier detection). The ATM-10 ore-sight-charm case (4-nugget reward instantly locates allthemodium) is the canonical example of scarcity nullification. See `reference/design/progression-rules.md` §R125.
- **R127 mandatory per-task reasoning:** Every task item must answer "这个物品在当前维度/阶段可用吗？" Cross-dimension item usability is a hidden reward-disconnection vector: food from non-Twilight dimensions cannot be eaten in the Twilight Forest; equipment may be nerfed in cross-dimension contexts. When a quest rewards an item that works in dimension A but the next quest takes place in dimension B, verify the item is usable in dimension B. If dimension context is unknown, mark `[unverified:cross_dimension]`. See `reference/design/progression-rules.md` §R127.
- **R130 currency economy check:** Packs using item-as-currency (e.g., GT silver_credit, Lightman's Currency coins) must verify three consistency conditions: (1) supply-demand balance — total currency rewarded across the quest book ≥ total shop-quest costs (deficit = progression wall; surplus = inflation); (2) dual identity — if the currency item is also a crafting material, flag the spend-vs-craft tension; (3) external obtainability — if currency is farmable outside the quest book, the economy is bypassable. Pack authors using `ftbmoney` are exempt from R130 (ftbmoney has no dual-identity or external-farming risk). See `reference/design/progression-rules.md` §R130.
- **R126 is ERROR severity, not WARNING.** Quest task detection alignment is binary — either the quest triggers correctly or it doesn't. Three root causes to check: (1) item unification collision (multiple mods register the same item, quest detects the wrong one); (2) NBT sensitivity mismatch (quest expects NBT-tagged item but task is NBT-agnostic, or vice versa); (3) trigger timing lag (task checks before the player's action registers). The FTB Skies #3248 case (harvesting flax incorrectly completed a cobblestone quest) is the canonical example. See `reference/design/progression-rules.md` §R126.
- **R128 is INFO-level design guidance.** The backward-facing shortcut principle ("each progression step should open fresh avenues while supplying shortcuts to optimize what you've done") is a design philosophy, not a verifiable config check. Include as a design consideration when authoring reward descriptions. See `reference/design/progression-rules.md` §R128.
- **R129 applies only to stage-framework packs.** Quest-as-stage-trigger integration verifies that quest completion commands correctly activate game stages, and that stage-conditional quest visibility matches the intended progression. Only relevant when the pack uses Game Stages, Item Stages, or similar. See `reference/design/progression-rules.md` §R129.

Three new tensions from Cycle 19 (documented in `reference/design/progression-rules.md`):
- **Tension 13:** Reward generosity (kitchen-sink) vs. reward restraint (expert) — resolved as pack-type-dependent: utility rewards free in kitchen-sink, capability rewards restrained; expert enforces zero-reward strictly.
- **Tension 14:** Quest-as-canonical-trigger (R129) vs. organic exploration (R123) — resolved as audience-dependent: expert = quest as gate; kitchen-sink = quest as guide.
- **Tension 15:** Item-as-currency simplicity (R130) vs. ftbmoney abstraction — resolved as economy-importance-dependent: minor economy = item currency; core economy = ftbmoney.
```

---

## Change B3: Step 5 — whole-book validation update

**Location:** Step 5 (Whole-book verify & balance)
**Insertion point:** After the topology validation execution order (line 625 in current SKILL.md, after "R60 (P3) Topology-Shape Vocabulary Coherence"), before the "Print topology validation results" block (line 627).

**Text to insert:**

```
**Cycle 19 validation extensions (R125–R130):** After the topology validation, run the following Cycle 19 checks as part of the whole-book pass. These formalize the generation-time advisory checks from Step 4's Cycle 19 architecture block:

- **R126 Task Detection Alignment (ERROR — new in Step 5 pipeline):** For every `ftbquests:item` task in the book, verify: (1) the task's `item` field matches the pack's unification target (if KubeJS unification scripts exist in `/scripts/`, check that the quest's item ID is the canonical ID, not an alias); (2) the task's `match_nbt` field (if present) is consistent with the item's NBT usage in recipes; (3) no two tasks in the same quest have overlapping item-match conditions that could cause false-positive completion. This check was not possible at Step 4 per-node time because item unification and cross-task overlap require the full graph. Print results as:
  ```
  R126 detection alignment: {pass/error}
     Tasks checked: {N} | Unification collisions: {count} | NBT mismatches: {count} | Overlapping conditions: {count}
  ```

- **R129 Quest-as-Stage-Trigger Integration (INFO — new in Step 5 pipeline):** For packs using stage-framework mods, verify: (1) every stage-boundary quest has a `command` reward granting the correct game stage; (2) every `stage`-conditional quest's `visibility` field matches the stage granted by its ancestor quest; (3) no stage is granted by two independent quest paths (redundant trigger). Only runs when the pack's modlist includes Game Stages, Item Stages, or TinkerStages. Print results as:
  ```
  R129 stage-trigger integration: {pass/info}
     Stage grants checked: {N} | Missing grants: {count} | Visibility mismatches: {count} | Redundant triggers: {count}
  ```

- **R125 Reward Trivialization Sweep (WARNING):** Whole-book scan of all rewards against the pack's scarcity list (if defined). Aggregate check: count how many rewards trivialize scarce resources. If >10% of scarce resources are trivialized by rewards, escalate from per-reward WARNING to chapter-level WARNING. This is the formal version of Step 4's per-reward R125 reasoning.

- **R130 Currency Consistency Audit (WARNING):** For packs with item-as-currency, compute total currency rewarded vs. total shop-quest costs across the entire book. Print supply-demand ratio. Flag deficit (<0.8×) or surplus (>2.0×) as WARNING. This whole-book audit catches cumulative imbalances that individual per-reward checks miss.
```

---

## Change B4: Standalone Cycle 19 addendum

**Location:** End of Step 4's progression architecture section (after the Cycle 19 rules block from B2 and tensions), or as a top-level addendum note following the existing Cycle 16/17/18 patterns.

**Text to insert:**

```
**Cycle 19 addendum: R125–R130 新增。AP47 新增。MP76–MP77 新增。Cases 62–71 新增。T13–T15 新增。**
three-hard-problem 防御框架：R125 (reward trivialization) + R126 (detection alignment) + R127 (cross-dimension usability) + R128 (backward shortcuts) + R129 (stage triggers) + R130 (currency consistency)。六规则形成三层防御：generation-time per-node 推理（R125/R127 每个 reward/task 必答）、chapter-level advisory（R128/R129/R130 设计指导）、whole-book formal validation（R126 ERROR + R125/R130 aggregate sweep）。
详见 `reference/design/progression-rules.md` R125–R130。

新增 anti-pattern: AP47 (R59 double-axis violation — chapter exceeds bounding box on both axes, indicating fundamental topology mismatch)。
新增 micro-patterns: MP76 (textural shape naming — custom shape textures as semantic layer), MP77 (sub-1.0 size compression for high-density chapters >60 quests)。
新增 topology cases: Cases 62–71 (10 new cases spanning all seven topology types, improving coverage for adventure/RPG, skyblock, and farming/lifestyle archetypes)。
新增 tension pairs: T13 (reward generosity vs. restraint), T14 (quest-as-trigger vs. organic exploration), T15 (item-currency vs. ftbmoney)。

R125 scarcity list 是 novel defense mechanism（无现有工具支持，需自定义验证脚本）。R126 检测对齐填补了此前完全未覆盖的 detection-level failure domain（FTB Skies #3248）。R130 item-as-currency 三重一致性检查（供需平衡、双重身份、外部可得性）首次将经济系统纳入 quest validation 范围。
```

---

## Implementation notes

These four changes (B1, B2, B3, B4) are additive — they append new content without modifying existing text. The existing Cycle 16, Cycle 17, and Cycle 18 addenda remain untouched. The new Cycle 19 addendum follows the same structural pattern as prior cycle addenda.

**Key differences from Cycle 18 draft:**
- Cycle 19 adds a Step 5 validation update (B3) that Cycle 18 did not have — this is because R126 (task detection alignment) and R129 (stage-trigger integration) require the full graph and cannot run at Step 4 per-node time.
- Cycle 19 introduces mandatory per-node reasoning questions in Step 4 (R125 per-reward, R127 per-task, R130 per-economy-pack) that extend the existing Gate 1/Gate 2 framework rather than creating new gates.
- MP77 (sub-1.0 sizing) is the first micro-pattern that modifies the scaffold's coordinate assignment behavior, requiring Step 3 awareness.

**Reviewer cross-references to apply when reviews are conducted:**
- R125 scarcity list implementation gap (noted in Phase 4 gaps) — B2 text acknowledges this as a novel mechanism without tooling support
- R126 item unification dependency on KubeJS scripts — B3 text specifies "if KubeJS unification scripts exist"
- R130 currency audit requires whole-book parsing — B3 text positions this as a Step 5 whole-book check
- AP47 double-axis violation is a new severity class (ERROR for layout) — B1 text documents the remediation path (decomposition or topology change)

**Estimated line counts for insertion:**
- B1: ~12 lines (Step 3, after line 405)
- B2: ~28 lines (Step 4, after line 584)
- B3: ~20 lines (Step 5, after line 625)
- B4: ~10 lines (Step 4 standalone addendum)
- Total: ~70 lines of new content
