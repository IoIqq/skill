# Step 2 Interview Protocol — Mainline Interview

Goal: settle the **spine** of the book — theme, mods, structure, reward philosophy, linkage — and end with an **outline** the user approves before ANY task or reward is designed. Do NOT design individual tasks/rewards here; that is Step 4's per-node loop.

## Interview discipline — grill, don't dump

Ask the user ONE question at a time, each with your recommended answer, and wait for their reply before the next. Walk the decision tree branch-by-branch (theme → mods → structure → rewards → linkage), resolving one dependency before moving to the next. **Never post a questionnaire / list of questions and wait** — that abdicates your role as the designer.

Before asking, check the Step 1 index + existing quests/lang: if a question can be answered by exploring the codebase, explore it yourself instead of asking. Skip any branch already settled by what you indexed.

**Ask when you don't understand** — if a mod's mechanics, a task/reward type's behavior, a format quirk, or any requirement is ambiguous, ask the user to clarify instead of guessing. Surface your uncertainty rather than papering over it.

**Adaptive depth:**
- "帮我设计" / high-level ask → propose the outline yourself; the user approves/edits.
- "我要指定每个任务" / granular → still agree the outline first, then co-author each node in Step 4.

---

## Branch 1 — Theme & tone

- Theme: tech / magic / adventure / skyblock / kitchen-sink / expert / story
- Tone: tutorial / lore / humorous
- Language(s): name the primary (authoring) locale + any secondaries. Secondaries are translated in a post-Step-4 pass, not per node.

## Branch 2 — Mods

- Which mods get chapters (auto-detect from the mod list in `.ftbq-cache/mods.json5`)
- Which to exclude (library/utility mods)
- Mod-specific mechanics to highlight
- Magic/tech mod progression patterns + per-mod bottleneck orientation: `reference/design/tech-progression.md` (**orientation only — verify in JEI/EMI**, never-guess rule)

## Branch 3 — Structure

- ~chapter count, connected vs independent, a main storyline + optional sides, ~quests per chapter
- When Theme picked **kitchen-sink** (ATM-series style), the spine + capstone is the backbone to settle here — don't leave kitchen-sink chapters as flat quest buckets:
  - **Per-chapter spine** — each mod/system chapter carries its own short through-line chain (e.g. ATM's AllTheModium line). Recommend: one spine per chapter; it's what makes a kitchen-sink pack navigable.
  - **Capstone convergence** — one endgame node the whole book converges on (ATM Star / Gregstar style)? Recommend: yes for ATM-series. The capstone chapter is **self-contained** (model: design-guide §principles F1/F2).
  - **Non-kitchen-sink endgame** — linear/expert packs end on a final boss or goal quest, not a convergence capstone; don't force one onto a pack without a convergence shape.
  - Evidence: `design-guide.md §field-findings` (ATM9/ATM10).

### Topology selection — MANDATORY

"你希望这个 chapter 使用什么布局拓扑？" Seven options (visual examples: `topology-coordinates.md §Phase 2`):

- **linear_chain** — 深度线性链（教程章、单 mod 配方链）
- **hub_fan** — 中心 hub 辐射分支（多子系统 mod 如 Mekanism）
- **parallel_columns** — 并行纵列（赏金板、多材料并行升级）
- **diamond_convergence** — 菱形汇聚（多路线汇聚到 capstone）
- **tree_branching** — 树状分支（大型专家包主进度线）
- **grid_catalog** — 网格目录（里程碑/成就收集章）
- **highway_branch** — 水平主干+垂直分支（多结构 mod 如 Botania）

Ask per-chapter, not per-book — different chapters in the same pack typically use different topologies. Recommend based on the chapter's content structure: a mod with N sub-systems → hub_fan; a linear upgrade path → linear_chain; a collection trophy case → grid_catalog. The topology choice drives coordinate assignment in Step 3 and validation rules in Step 5.

## Branch 4 — Rewards & difficulty

- Reward philosophy: generous items vs cosmetic/lore (guide-first like Divine Journey 2 / Create: Astral vs reward-driven like ATM). Pick and commit (`reference/design/reward-economy.md`).
- `consume_items` philosophy
- Special reward types: commands / loot tables / XP
- Expert/hardcore gating
- Pacing follows the difficulty curve (`reference/design/difficulty-curve.md`): tutorial → early (16–64 stacks) → mid (1–2 hr bottlenecks) → late (multi-blocks, bosses) → endgame; every ~3rd quest an alternative path.

### Dominant reward type (R34)

If the pack uses reward tables (`random`/`loot`/`choice`), settle the dominant type here — one pack, one dominant presentation style. Craftoria uses `random` (auto-roll), E10 uses `loot` (loot crate), MI:Foundation uses `item` (deterministic). Mixing is allowed but should be deliberate, not accidental. Ask: "你的整合包偏好哪种奖励呈现方式？自动抽取 (random)、战利品箱 (loot)、还是玩家选择 (choice)？" with the recommendation based on pack genre.

### Questbook role (R46) — MANDATORY

"你的任务书主要扮演什么角色？" Four options:

- **伴生导航 (companion)** — 任务书给方向，EMI/field guide 给细节（如 TFG Modern）
- **教程系统 (tutorial)** — 任务书是主要教学工具（如 Monifactory、E9E）
- **激励目录 (incentive_catalog)** — 任务书主要发奖励驱动玩家（如 ATM 系列）
- **混合模式 (hybrid)** — 不同章节扮演不同角色（如 ATM-10）。If hybrid, ask which chapters use which role.

This declaration determines R47 and R50 applicability downstream.

### Collection-catalog check (R49) — CONDITIONAL

When the user mentions collection/catalog chapters: "这个 catalog 涵盖哪些 mod？这些 mod 的内容是否已稳定，还是仍在频繁更新？" If > 3 actively developed mods or estimated > 200 quests, warn about maintenance cost and recommend: (a) limiting scope to stable-content mods, (b) tag-based tasks (`itemfilters:tag` or `ftbfiltersystem:smart_filter`) that auto-include new items, or (c) splitting into smaller sub-chapters.

### Zero-reward safety (R50) — CONDITIONAL

When the user indicates zero or near-zero reward design, confirm 3 safety conditions:
1. "是否有替代进度货币？" (voltage tiers, badges, skill systems, Game Stages, achievement unlocks). **If the user doesn't know, proactively suggest alternatives** based on the pack's mod list — e.g. "你的包有 Game Stages，可以用 stage 解锁作为进度货币" or "GregTech 包天然有电压等级作为进度标志".
2. "任务书角色是否为 companion 或 catalog？" (from R46)
3. "包是否有强内在游戏循环？" (crafting/collection/combat/exploration)

All three must be yes for safe zero-reward design. If any fails, recommend adding at least minimal XP or cosmetic rewards.

### Stage definitions — CONDITIONAL (mandatory for expert/story/skyblock; optional for kitchen-sink)

1. **Stage division (stage_map skeleton):** "你的整合包有明确的阶段划分吗？例如'石器→铁器→钻石→下界→末地'或'ULV→LV→MV→HV→EV'？请列出阶段名称和顺序。"
2. **Stage key resources (stage_available_resources):** "每个阶段有哪些关键可获得资源？请每阶段列出 5–10 个代表性物品 ID。"
3. **Game Stages integration (if applicable):** "你的包是否使用 Game Stages 或类似的阶段锁定模组？如果是，请提供 stage name 列表及其解锁的内容摘要（物品/维度/配方）。"

Collected data serves as L2-level data source for: R42 (stage-internal item reachability), R44 (reward-stage matching), R43 (stage-quest causal chain acyclic), R4 (stage boundary). If the user doesn't provide L2 data, these rules degrade to L1 heuristic or INFO-level reporting.

## Branch 5 — Linkage (only if Step 1 found existing quests)

How does the new content connect to the pack's existing quests? Grill one question at a time, codebase-first — show what the index found before asking:

- **Gate after** — should new quests require completing an existing quest first? (recommend: yes, if the new chapter uses mods the existing book unlocks)
- **Reward from** — should completing existing quests reward into the new line, or vice versa? (recommend: only if the two share a progression resource)
- **Branch off** — does the new line split from an existing quest as an optional side, or stand alone? (recommend: branch off when themes overlap; stand alone when they don't)
- **Avoid duplicating** — does an existing quest already teach/require the same thing? (recommend: skip or rephrase to avoid a dead duplicate)

Record the chosen existing quests by their 16-hex ID (from the cache) and reference them in `depends_on` — see SKILL.md "Task linkage".

---

## Deliverable — the outline (approve before scaffolding)

Before leaving Step 2, write `<output_dir>/outline.json5` and show it to the user for sign-off — one chapter list, each with its quest **nodes** in main-line order and the `depends_on` chain, plus where side branches fork. Only names + wiring; **no tasks, no rewards, no descriptions.**

```json5
{
  pack: "create-astral",
  arc: "place a cogwheel → automate oak → first machine",
  chapters: [{
    name: "getting_started",
    nodes: [
      { name: "punch_wood", depends_on: [] },
      { name: "first_plank", depends_on: ["punch_wood"] },
      { name: "manual_craft", depends_on: ["first_plank"] },
    ],
  }],
}
```

Kitchen-sink example — capstone chapter is SELF-CONTAINED (capstone + components in-chapter; cross-mod breadth is via each component's item TASK, not cross-chapter depends_on — design-guide §principles F1/F2):

```json5
{
  pack: "atm-style",
  arc: "per-mod chapters teach each mod → capstone chapter pulls one component per mod",
  chapters: [
    { name: "allthemodium", nodes: [
      { name: "find_ore", depends_on: [] },
      { name: "alloy_pendant", depends_on: ["find_ore"] },
    ]},
    { name: "mekanism", nodes: [
      { name: "first_osmium", depends_on: [] },
      { name: "metabolics", depends_on: ["first_osmium"] },
    ]},
    { name: "endgame", nodes: [
      { name: "dragon_soul", depends_on: [] },
      { name: "singularity", depends_on: [] },
      { name: "atm_star", depends_on: ["dragon_soul", "singularity"] },
    ]},
  ],
}
```

Get an explicit "yes" (or edits) before Step 3. If the user changes the arc later, update the outline and re-confirm — do not silently diverge.

---

## Linear vs nonlinear — the dependency wiring

- **Linear:** `dependency_requirement: "all"`, each quest depends on the prior — one path, no choices. Good for teaching a forced sequence.
- **Nonlinear:** quests in a chapter share *no* deps among themselves (craft in any order); a capstone at the end depends on all of them (`"all"`), or on one-per-branch (`"one"` for "any path"). Good for catalogs and parallel mod lines.
- **Branching:** a hub fans into N alternatives — `dependency_requirement: "one"` (do any one) or `"all"` (do all).

`progression_mode` is a per-chapter switch: `default` (quest locks until dep done — strict order) vs `flexible` (any order, deps hide not lock). ATM ships `flexible` so passive tasks (advancements/stats/biome visits) count; use `default` when order *is* the lesson.

## Mod synergy — representing cross-mod connections

Four patterns (cross-mod crafting chain, cross-mod gating, capstone synthesis, deep integration) — full descriptions + the "don't fake synergy" caveat: `design-guide.md §synergy-patterns`.

In the spec:
- **Item task from multiple mods:** the task item is the *output*; the description walks the inputs. For "prove you've used both mods," use **two tasks** on one quest (`dependency_requirement: "all"`).
- **Cross-chapter dependency:** `depends_on: ["<modA_chapter>/<key_quest>"]` (or raw hex for an existing pack).
- **`quest_links[]` (hexagon, size 2.0):** display the same quest in two chapters when it belongs to both. Links, not duplicates (reference §18).
- **KubeJS `custom` tasks/rewards:** when synergy can't be expressed as an item, use `type: "ftbquests:custom"` pointing at the pack's KubeJS script.
- **Don't fake synergy the mods don't have.** Verify the interaction in JEI/EMI or the mods' configs before writing the quest.
