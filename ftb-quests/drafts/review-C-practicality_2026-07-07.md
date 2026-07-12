# Review C -- Practicality Audit (Cycle 4)

> **Reviewer:** C (Practicality Reviewer)
> **Date:** 2026-07-07
> **Scope:** R33, MP34, R34 draft, 33-rule execution priority, Step 4 context budget
> **Method:** Simulate AI agent execution for each rule; assess cost/benefit; classify generation-time vs validation-time

---

## 0 -- Step 4 Context Budget Analysis

### File Line Counts (full files)

| Module File | Total Lines | Step 4 Load | Loaded Lines (est.) |
|---|---|---|---|
| shared-builtin-tables.md | 154 | Full | 154 |
| mod-item-reachability.md | 314 | Full | 314 |
| mod-reward-design.md | 307 | Full | 307 |
| mod-description-trust.md | 154 | AP9-AP11 only | ~50 |
| mod-teaching-pacing.md | 209 | R14-R17 (chapter batch) | ~52 |
| **Total** | **1,138** | | **~877** |

### Context Impact Assessment

**877 lines = ~11,000-13,000 tokens** (mixed Chinese/English, code blocks, tables). This is a conservative estimate; the actual count depends on tokenizer behavior with CJK characters and code blocks.

For comparison:
- A typical AI agent session (QoderWork/Codex) has a context window of 128K-200K tokens
- SKILL.md itself is ~630 lines = ~10,000 tokens
- Step 4 also requires: the spec file being edited (~200-500 lines), the outline, item caches, and the ongoing conversation history
- **Total estimated context pressure at Step 4:** ~35,000-50,000 tokens (modules + SKILL.md + spec + conversation)

**Verdict:** The 877-line module load is **within budget** but not trivial. It represents ~25% of the total context pressure during Step 4. The main risk is not the raw token count but the **cognitive load on the AI**: 877 lines containing 12 rules, 7 patterns, 5 anti-patterns, and 3 AI-specific risks. The AI must hold all of this in working memory while generating each quest node.

### Recommended Loading Optimizations

1. **Tiered loading by quest type.** Not every quest needs every module:
   - A simple `item` task quest: needs only R1-R4 (reachability) + MP14 (material bridge) + AP9-AP11 = ~400 lines
   - A quest with `command` reward: adds R28 = ~430 lines
   - A quest with `random`/`loot`/`choice` reward: adds MP34 + R33 = ~530 lines
   - **Recommendation:** Split mod-reward-design.md into a "core" section (MP14-MP18, AP6, R10, R28; ~150 lines) loaded always, and an "advanced" section (MP34, R33, R34; ~100 lines) loaded only when the quest uses reward table types.

2. **Lazy loading for R1-R4.** At generation time, the AI only needs the lookup tables (shared-builtin-tables) and the pseudocode. The full evidence/sourcing text (~150 lines of "why this matters" and "real cases") is needed for Step 5 validation but adds noise during generation. Consider a `mod-item-reachability-lite.md` (~120 lines) for Step 4.

3. **Pre-computed rule summaries.** Each module's Quick Reference table (already present) could be expanded to a 1-page "generation checklist" that the AI loads instead of the full module. Full module loaded only when a rule violation is suspected.

**Projected savings:** Tiered loading could reduce per-node context from ~877 to ~400-530 lines (~40% reduction).

---

## 1 -- R33: Reward Table Reference Integrity

### What the Rule Says

Every `table_id` in a `random`/`loot`/`choice` reward must reference an existing reward table file in `config/ftbquests/quests/reward_tables/`. Step 5 priority: P1 (ERROR).

### AI Execution Simulation

**Scenario:** User says "generate a Craftoria-style chapter with random rewards."

1. AI reads the spec and sees the quest needs `type: "random"` with a `table_id`.
2. To create a valid `table_id`, the AI must:
   a. Design the reward table content (which items, what weights, what `loot_size`)
   b. Generate a unique decimal long ID (e.g., `0414572B7C36F04F` converted to decimal)
   c. Write a `reward_tables/<id>.snbt` file with the correct format
   d. Reference that same ID in the quest's reward `table_id` field
3. **Problem:** The skill's SKILL.md mentions reward tables as a spec feature ("`reward_tables[]`... can be authored whenever their owning quest comes up in the loop"), but provides NO procedural guidance on HOW to generate a reward table file. There is no template, no ID generation formula for reward tables, no format specification in the Step 4 loop.

### Practicality Rating: D (should be restructured)

R33 as stated is a **post-generation validation rule** masquerading as a generation-time concern. The rule itself ("check the ID exists") is trivially executable. But the prerequisite ("the table file must exist") requires a generation workflow that the skill does not define.

### Execution Barriers

| Barrier | Severity | Detail |
|---|---|---|
| No reward table generation procedure | Critical | SKILL.md says reward tables "can be authored" but gives no step-by-step |
| No reward table format template | High | MP34 shows Craftoria/E10 examples but not a generator-ready template |
| ID collision risk | Medium | Reward table IDs use decimal longs; the generator's hex-based ID formula (reference section 9) is for quests, not tables |
| File creation outside the main loop | Medium | Writing `reward_tables/*.snbt` is a side-effect that the generate-and-validate loop doesn't explicitly handle |

### Generation vs Validation Classification

- **Generation-time:** The AI must CREATE the reward table file AND reference it. This is an authoring task, not a validation task. R33 is irrelevant here -- the AI cannot "violate" R33 if it creates both the table and the reference simultaneously.
- **Validation-time (Step 5):** R33 is meaningful here. After all files exist, a script can verify that every `table_id` points to a real file. This is the rule's natural home.

### Recommended Changes

1. **Downgrade R33 from "generation rule" to "Step 5 validation rule" only.** Remove any implication that the AI should check R33 during Step 4.
2. **Add a reward table generation procedure to SKILL.md Step 4.** When a quest uses `random`/`loot`/`choice`:
   - Determine table entries from the quest's context (stage-appropriate items)
   - Generate a table ID using the same formula as quest IDs (or a separate deterministic formula)
   - Add the table to `reward_tables[]` in the spec (already supported per SKILL.md line 423)
   - The generator writes the `.snbt` file; the quest's `table_id` references it
3. **Make R33 a generator-level invariant.** The `generate_quests.py` script should verify that every `table_id` in the spec maps to a `reward_tables[]` entry. If so, R33 is enforced by construction, not by post-hoc validation.

---

## 2 -- MP34: Loot Table Reward Unified Model

### What It Says

`random`, `loot`, and `choice` all use the **same FTB Quests internal reward table system** (`table_id` referencing `reward_tables/*.snbt`). The difference is purely player-facing UI (auto-roll vs manual open vs player picks).

### AI Execution Simulation

**Scenario:** AI is choosing a reward type for Quest 7 in a Create pack.

1. AI reads MP34 and learns that random/loot/choice are structurally identical.
2. AI must decide: which type to use?
   - MP34 says: "The choice between random, loot, and choice is a **player-experience decision**, not a data architecture decision."
   - MP34 also says: "Prefer one dominant type per pack for consistency (R34 checks this)."
3. AI checks the spec's reward philosophy (settled in Step 2 interview):
   - If user said "generous, ATM-style" -> probably `item` rewards (no table needed)
   - If user said "Craftoria-style randomness" -> `random`
   - If user said "E10-style loot crates" -> `loot`
4. **Does knowing they're structurally identical help?** Marginally. The AI already knows what type to use from the Step 2 interview. The unified-model insight saves the AI from thinking `loot` requires a different file format -- but this is a negative insight (preventing a mistake the AI might not have made).

### Practicality Rating: B (needs additional tooling to be actionable)

MP34 is valuable as **knowledge** (the unified system is a genuine discovery from Cycle 4), but it creates a practical problem: the AI now knows it needs to generate `reward_tables/*.snbt` files, and has no clear procedure for doing so.

### The Reward Table Authoring Problem

MP34 reveals that using `random`/`loot`/`choice` rewards requires authoring reward table files. This is a **non-trivial expansion of the skill's output scope**:

| Current Skill Output | New Requirement from MP34 |
|---|---|
| `chapters/*.json5` | Same |
| `lang/*/quests.json5` | Same |
| `data.json5` | Same |
| (none) | **`reward_tables/*.snbt`** (new file type) |

Each reward table file requires:
- A unique decimal long ID
- A list of weighted item entries (`count` = weight, `item.id` = item, `item.count` = stack size)
- Optional `loot_size` (number of rolls per claim)
- Optional `use_title`, `hide_tooltip`

For a 20-quest chapter with 8 random-reward quests, the AI might need 2-4 distinct reward tables. That's 2-4 additional files to design, format correctly, and cross-reference.

### Execution Barriers

| Barrier | Severity | Detail |
|---|---|---|
| Reward table design is a separate skill | High | Choosing items, weights, and roll counts is game design, not config generation |
| Weight calibration has no guidance | Medium | MP34 shows examples (count: 16 vs count: 2) but no formula for choosing weights |
| Stage-appropriate item selection | Medium | The AI must select items that are useful at the quest's progression stage -- this requires reachability reasoning applied to reward tables, not just tasks |

### Recommended Changes

1. **Add a reward table generation template to SKILL.md.** A concrete procedure:
   ```
   When a quest uses random/loot/choice reward:
   1. Determine the reward tier (early/mid/late) from quest depth
   2. Select 4-8 items from the mod's item pool at that tier
   3. Assign weights: common items weight=16-64, rare items weight=1-8
   4. Set loot_size=1 for routine, 2-4 for milestone
   5. Add to spec's reward_tables[] with a deterministic ID
   ```
2. **Scope the decision in Step 2.** The "reward philosophy" branch should explicitly ask: "Will this pack use reward tables (random/loot/choice rewards)? If yes, which dominant type?" This prevents the AI from discovering MP34 mid-generation and having to retrofit reward tables.
3. **Provide a generator-side reward table emitter.** `generate_quests.py` should handle `reward_tables[]` in the spec and write the `.snbt` files. If this is already supported, document it explicitly in SKILL.md.

---

## 3 -- R34 Draft: Reward Type Consistency

### What It Says

Detects mixed usage of `random` vs `loot` within the same pack. If both exist, INFO-level: "Consider standardizing."

### AI Execution Simulation

**Scenario:** AI is generating 20 quests in a chapter.

1. At quest 1, AI chooses `random` reward (because the Step 2 interview said "Craftoria-style").
2. At quest 7, AI is considering a `choice` reward for a branch point.
3. R34 says: mixing types within a pack is suspicious.
4. **Problem:** R34 checks at the **pack level**, but the AI is generating one **chapter** at a time. The AI has no way to know what other chapters use unless it reads them all.
5. **For self-generated packs:** The AI controls the entire book, so it can maintain consistency by design. R34 is unnecessary -- the AI just needs to follow the Step 2 decision.
6. **For extending existing packs:** The AI would need to scan existing chapters' reward types first. This is possible via `index_quests.py` cache (which tracks reward types), so R34 could be checked via: "Does `existing_quests.json5` show any `loot` rewards? If yes, my new `random` rewards create a mix."

### Practicality Rating: B (useful for extending existing packs, trivial for new packs)

### The Dominant Type Problem

R34's real value is forcing a decision: **what is this pack's dominant reward type?** Currently, the Step 2 interview asks about "reward philosophy" but does not ask "random vs loot vs choice vs item-dominant." This gap means:

- The AI might generate Quest 1-10 with `random` rewards
- Then generate Quest 11-20 with `loot` rewards (because context shifted)
- R34 would catch this post-hoc, but fixing it requires rewriting half the chapter

**The fix is upstream, not downstream:** settle the dominant type in Step 2.

### Execution Barriers

| Barrier | Severity | Detail |
|---|---|---|
| Pack-level scan needed for existing packs | Low | `index_quests.py` already tracks reward types |
| No enforcement mechanism during generation | Medium | R34 is INFO-level; AI might ignore it |
| Dominant type not settled in Step 2 | High | The root cause of type mixing is an unresolved decision |

### Recommended Changes

1. **Add "dominant reward type" as a Step 2 interview branch.** After reward philosophy, ask: "For randomized rewards, which type: `random` (auto-roll, Craftoria-style), `loot` (crate icon, E10-style), or `choice` (player picks, milestone only)?"
2. **Make R34 a generation-time constraint, not a validation rule.** Once the dominant type is settled in Step 2, the AI should use it for all table-based rewards. `choice` is allowed only for explicitly designated branch-point quests.
3. **For existing packs:** Add a Step 1 check: "What reward types does the existing pack use? Report dominant type and any exceptions." This is derivable from `index_quests.py` output.

---

## 4 -- 33-Rule Execution Priority

### The Core Problem

The skill defines R1-R33 (soon R1-R35) across 7 module files. An AI agent generating quests cannot execute all 33 rules per node. The rules need triage:

### Classification: Generation-Time vs Validation-Time

| Category | Rules | When Applied | AI Action |
|---|---|---|---|
| **Generation-time (must comply while writing)** | R10, R18, R23, R28, AP9 | Per-node, during spec writing | AI reasons about each item/reward as it writes; blocks spec write if violated |
| **Generation-time (reasoning check)** | R1-R4 (L1), R16, R17, R31 | Per-node, before finalizing | AI checks reachability mentally using builtin tables; marks `[unverified]` if unsure |
| **Validation-time (automated script)** | R5-R9, R11-R15, R19-R22, R24-R27, R29-R30, R32, R33, R34, R35 | After generation, via `validate_quests.py` | AI runs script, reads output, fixes flagged issues |
| **Background context (always loaded)** | AP1-AP8, AP10-AP11, MP1-MP34, PP1-PP7 | Continuous awareness | AI internalizes patterns; no explicit check needed |

### Current State Assessment

The SKILL.md Step 4 loop (lines 376-408) does a reasonable job of embedding generation-time rules:
- Step 4.2 mentions item reachability reasoning (R1-R4 L1)
- Step 4.2 mentions reward bridge reasoning (R10)
- Step 4.6 mentions AI self-check (R23, AP10, AP11)
- R28 is marked P0 and blocks spec write

**What's missing:**

1. **No explicit rule loading order.** The Step Loading Plan says "load these modules" but doesn't say "when generating a quest, apply rules in this order." The AI must figure out which of the 877 lines apply to the current quest.

2. **R17 (Tool-Reward-Before-Use) has no generation-time hook.** SKILL.md doesn't mention it in Step 4. The AI might generate a quest that rewards a tool in Quest 5 but needs that tool in Quest 3 (because Quest 3 was generated first in a non-linear chain). This is caught by Step 5 validation, but fixing it requires reordering quests.

3. **R31 (XP-Level Relativity) is per-node but not in the Step 4 loop.** If the AI puts `xp_levels` on a routine quest, it should catch this immediately, not after generating 20 quests.

4. **R34 (Reward Type Consistency) has no generation-time counterpart.** See Section 3 above.

### Recommended Priority Framework

```
P0 -- BLOCKS spec write (generation-time, hard stop):
  R23 (description-item consistency)
  R28 (command reward safety -- FORBIDDEN commands)
  AP9 (hallucination cascade -- unverified item IDs)

P1 -- CHECKS before finalizing node (generation-time, soft warning):
  R1-R4 L1 (dimension/tool/recipe/stage reachability)
  R10 (reward-to-dependent bridge)
  R16 (explore-then-craft ordering)
  R17 (tool-reward-before-use, reverse check)
  R18 (description coverage)
  R31 (XP-level relativity)

P2 -- VALIDATION script (post-generation, automated):
  R5-R9, R11-R15, R19-R22, R24-R27, R29-R30, R32-R35
```

This framework should be **explicit in SKILL.md** so the AI doesn't waste context trying to apply validation-time rules during generation.

---

## 5 -- Modular System Loading Assessment

### Step 4 Loading Plan vs Reality

The module-index.md Step 4 loading plan specifies 5 items:

| # | Load | Actual Lines | Needed Per Node? |
|---|---|---|---|
| 1 | shared-builtin-tables (full) | 154 | No -- only when quest involves dimension/tool items |
| 2 | mod-item-reachability (full) | 314 | No -- only R1-R4 pseudocode + L1 tables needed |
| 3 | mod-reward-design (full) | 307 | No -- MP14 + R10 + R28 sufficient for most quests |
| 4 | mod-description-trust AP9-AP11 | ~50 | Yes -- always relevant during generation |
| 5 | mod-teaching-pacing R14-R17 | ~52 | No -- only at chapter-batch review |

**Observation:** The loading plan loads 4 full modules + 2 partials (~877 lines). But for a typical single-node generation, the AI actually uses:
- L1 lookup tables from shared-builtin-tables (~60 lines of code/data)
- R1-R4 pseudocode from mod-item-reachability (~80 lines)
- MP14 + R10 + R28 from mod-reward-design (~60 lines)
- AP9-AP11 from mod-description-trust (~50 lines)
- **Total actually used: ~250 lines**

The remaining ~627 lines are **loaded but not actively used** during per-node generation. They provide context and background but compete with the spec file and conversation history for attention.

### Is This a Problem?

**For large-context models (128K+):** Not critical. 877 lines of well-structured markdown is manageable.

**For practical execution quality:** Yes. The more context the AI has to scan, the more likely it is to:
- Miss a relevant rule (attention dilution)
- Apply a validation-time rule during generation (wasted effort)
- Confuse pattern descriptions with actionable rules

### Recommended Loading Strategy

**Replace "load full module" with "load module summary + relevant sections."**

Create a `step4-quickref.md` file (~200 lines) containing:
1. L1 lookup tables (from shared-builtin-tables) -- verbatim
2. R1-R4 pseudocode (from mod-item-reachability) -- verbatim
3. MP14, R10, R28 summaries (from mod-reward-design) -- condensed
4. AP9-AP11 full text (from mod-description-trust) -- verbatim
5. P0/P1 rule checklist (from Section 4 above) -- new

Full modules loaded only when:
- A rule violation is suspected (load the relevant module to understand the fix)
- Chapter-batch review (load mod-teaching-pacing R14-R17)
- Step 5 validation (load all modules)

**Projected context savings:** ~677 lines per node (~77% reduction in module loading).

---

## Summary of Ratings

| Item | Rating | Justification |
|---|---|---|
| **R33 -- Reward Table Reference Integrity** | **D** | Validation-only rule; meaningless at generation time when tables don't exist yet. Should be enforced by generator construction, not post-hoc checking. |
| **MP34 -- Loot Table Reward Unified Model** | **B** | Valuable knowledge, but creates an authoring burden (reward table files) with no defined procedure. Needs a generation template. |
| **R34 -- Reward Type Consistency** | **B** | Useful for extending existing packs, trivial for new packs. Root cause is an unresolved Step 2 decision. Move the decision upstream. |
| **33-Rule Priority Framework** | **B-** | Current Step Loading Plan is insufficient for generation-time triage. Needs explicit P0/P1/P2 classification. |
| **Step 4 Context Budget** | **B+** | 877 lines is within budget but suboptimal. ~77% of loaded content is not actively used per node. Tiered loading recommended. |

---

## Actionable Recommendations (Priority Order)

1. **[Step 2] Add "dominant reward type" interview branch.** Resolves R34 upstream; prevents type-mixing during generation. Cost: ~5 lines in SKILL.md.

2. **[Step 4] Add reward table generation procedure.** When a quest uses random/loot/choice, the AI needs a concrete template for creating `reward_tables[]` entries. Cost: ~20 lines in SKILL.md + generator support verification.

3. **[Step 4] Create `step4-quickref.md`.** Condensed generation-time reference (~200 lines) replacing 877-line full module load. Cost: one-time authoring effort; saves ~677 lines per node invocation.

4. **[SKILL.md] Add explicit P0/P1/P2 rule classification.** Tell the AI which rules to check per-node vs defer to validation. Cost: ~15 lines in SKILL.md.

5. **[R33] Reclassify as generator-level invariant.** The `generate_quests.py` script should verify `table_id` -> `reward_tables[]` mapping at emission time. R33 becomes a construction guarantee, not a validation rule.

6. **[R34] For existing packs, add Step 1 reward type scan.** Report existing pack's dominant reward type from `index_quests.py` cache. Cost: ~3 lines in `pack_briefing.py` output.

---

## Appendix A: Per-Rule Generation/Validation Classification

| Rule | Title | Gen-Time? | Val-Time? | AI Can Execute? | Notes |
|---|---|---|---|---|---|
| R1 | Dimension-Reachability | Yes (L1) | Yes (full) | A (with L1 tables) | Needs shared-builtin-tables loaded |
| R2 | Tool-Tier Reachability | Yes (L1) | Yes (full) | A (with L1 tables) | Needs shared-builtin-tables loaded |
| R3 | Recipe-Chain Depth | Yes (heuristic) | Yes (full) | B (heuristic unreliable) | +/-2 depth error; mark [unverified] |
| R4 | Stage Boundary | Yes (fallback) | Yes (full) | B (needs stage map) | Cross-chapter fallback weak |
| R5 | Circular Dependency | No | Yes | A (script) | Structural; needs full graph |
| R6 | Orphan Quest | No | Yes | A (script) | Structural |
| R7 | Dependency Depth | No | Yes | A (script) | Structural |
| R8 | Cross-Chapter Dep | No | Yes | A (script) | Structural |
| R9 | Diamond Dependency | No | Yes | A (script) | Structural |
| R10 | Reward-to-Dep Bridge | Yes (reverse) | Yes (forward) | A (per-node reasoning) | Core generation-time rule |
| R11 | Reward-Target Accuracy | No | Yes | B (needs tool map) | Cross-mod tool detection |
| R12 | Reward Value Progression | No | Yes | C (imprecise) | Value estimation unreliable |
| R13 | Capstone Magnitude | No | Yes | C (imprecise) | Same as R12 |
| R14 | Teach-Then-Do | No | Yes | A (script) | Needs full chapter graph |
| R15 | Complexity Escalation | No | Yes | B (heuristic) | Soft check |
| R16 | Explore-Then-Craft | Yes (reverse) | Yes (full) | A (per-node reasoning) | Similar to R1 |
| R17 | Tool-Reward-Before-Use | Yes (reverse) | Yes (full) | A (per-node reasoning) | Needs tool reward tracking |
| R18 | Description Coverage | Yes | Yes | A (trivial check) | "Does desc exist and >20 chars?" |
| R19 | Bottleneck Spacing | No | Yes | A (script) | Needs full chain |
| R20 | -- | -- | -- | -- | (placeholder) |
| R21 | Hidden Quest Signpost | No | Yes | B (spatial check) | Needs coordinates |
| R22 | Cross-Reference Pattern | No | Yes | A (script) | Structural |
| R23 | Description-Item Consistency | Yes | Yes | A (regex + compare) | P0 generation-time |
| R24 | Suggestion-Reachability | Partial (L1) | Yes (full) | B (NLP extraction) | Regex near suggestion patterns |
| R25 | -- | -- | -- | -- | (placeholder) |
| R26 | Quest-Mod Version | No | Yes | C (needs version data) | No L1 fallback |
| R27 | -- | -- | -- | -- | (placeholder) |
| R28 | Command Reward Safety | Yes | Yes | A (string match) | P0 -- FORBIDDEN commands block |
| R29 | -- | -- | -- | -- | (placeholder) |
| R30 | -- | -- | -- | -- | (placeholder) |
| R31 | XP-Level Relativity | Yes | Yes | A (type check + milestone heuristic) | Simple check |
| R32 | Team Progression | No | Yes | A (script) | Structural |
| R33 | Reward Table Integrity | **No** | Yes | **D** | Tables don't exist at gen time |
| R34 | Reward Type Consistency | **Partial** | Yes | **B** | Needs Step 2 decision first |
| R35 | Shape Semantics | No | Yes | B (statistical) | Needs full pack data |

---

## Appendix B: Step 4 Context Budget Detail

### Full Loading (current plan)

```
SKILL.md (always in context)                        ~10,000 tokens
shared-builtin-tables.md (154 lines)                 ~1,800 tokens
mod-item-reachability.md (314 lines)                  ~4,200 tokens
mod-reward-design.md (307 lines)                      ~4,000 tokens
mod-description-trust.md AP9-AP11 (~50 lines)          ~700 tokens
mod-teaching-pacing.md R14-R17 (~52 lines)             ~700 tokens
                                                     ------------
Subtotal (modules):                                 ~11,400 tokens
Subtotal (SKILL.md + modules):                      ~21,400 tokens
```

### Additional Step 4 context

```
Spec file (quests.spec.json5, partial read)          ~2,000-5,000 tokens
Outline file                                          ~500-1,000 tokens
Item cache (items.json5, grep results)                ~500-2,000 tokens
Conversation history (per node)                      ~3,000-8,000 tokens
Generated quest content (per node)                    ~500-1,000 tokens
                                                     ------------
Subtotal (working context):                          ~6,500-17,000 tokens
```

### Total estimated per-node context

```
Minimum:  ~28,000 tokens
Typical:  ~35,000 tokens
Peak:     ~45,000 tokens
```

**Verdict:** Well within 128K context window. The constraint is not tokens but **attention allocation** -- 33 rules across 877 lines of module text, of which ~250 lines are actively used per node.

### With Tiered Loading (recommended)

```
step4-quickref.md (~200 lines)                       ~2,800 tokens
(Saves ~8,600 tokens from full module loading)
```

Total with optimization: ~22,000-33,000 tokens per node.

---

*End of Review C -- Practicality Audit (Cycle 4)*
