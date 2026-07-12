# Review A: Cycle 3 Universality Audit

**Reviewer:** A (Generalizability)
**Date:** 2026-07-07
**Scope:** Cycle 3 additions to micro-patterns.md (MP33/MP34), anti-patterns.md (AP17/AP18), progression-rules.md (R30/R31/R32)

---

## 1. Critical: MP33 (Advancement Gate) and MP34 (Loot Table Reward) Missing

**Severity:** BLOCKER

MP33 和 MP34 在 `micro-patterns.md` 文件中**完全不存在**。文件内容止于 MP32 (min_tasks Modifier)，Section Navigation 表的最后一行是 "Part 8: Cycle 2 Patterns (MP31-MP32)"，没有 Part 9 或任何 Cycle 3 新增 micro-pattern 的条目。Scope Annotation Table 同样止于 MP32。全目录搜索（包括所有 reference/design/*.md 文件）均未找到 "MP33"、"MP34"、"Advancement Gate" 或 "Loot Table Reward" 的任何引用。

**Conclusion:** 这两个模式从未被写入文件。审查请求中描述的来源数据（Enigmatica 10 3 cases for MP33, Craftoria for MP34）无法评估，因为内容本身缺失。

**Recommendation:** 在 micro-patterns.md 中补充 MP33 和 MP34 之前，无法进行通用性审查。需要先完成内容编写。

---

## 2. AP17 -- XP-Level Reward Relativity (Craftoria single-source)

**Question:** 是 Craftoria 特有问题还是通用问题？

**Verdict:** **通用问题，single-source 不影响通用性。**

AP17 的根因是 Minecraft 原版的指数级 XP 曲线——每升一级所需 XP 递增，导致固定等级奖励的实际价值随玩家等级漂移。这是游戏引擎层面的机制，与包类型、mod 组合或设计哲学无关。**任何**使用 `xp_levels` reward 类型的包都受此影响。

Craftoria #289 是目前唯一在 issue tracker 上系统性记录此问题的来源，但这是因为：
1. 大多数玩家默默忍受或自行优化领取时机，不会提交 issue
2. 其他包（ATM-10 的 50 XP levels ATM Star capstone, skyblock 包的等级奖励）同样使用 xp_levels 但未被投诉
3. Craftoria 的这位玩家恰好做了详尽的代码搜索和跨 chapter 审计

**Direct fix applied:** 已在 anti-patterns.md 的 AP17 条目中添加 Generalizability note，明确标注此模式的通用性源于 Minecraft XP 机制而非包特有设计。

**No further action needed.** AP17 的 scope 无需限制。

---

## 3. AP18 -- Reward Desert in Long Chains (Craftoria single-source)

**Question:** 是 Craftoria 特有问题还是通用问题？

**Verdict:** **通用问题，single-source 不影响通用性，但应补充间接证据。**

Reward desert（长链无奖励）是 reward pacing 失败的一种形态，与 AP8（Reward Inflation）互补。任何使用 deep linear chain（depth 5+）的包都面临此风险：

- Expert packs（Monifactory depth 8-15, E9E depth 8+）天然面临 reward desert 风险
- Skyblock tutorials（ATM9-Sky depth 18）如果中间 quest 无 reward 也会出现
- cesspit.net 的分析隐含了 reward desert 的反面："you have to work hard to get to a milestone" 之后必须有 reward payoff

Craftoria #231 的 Powah chapter 案例恰好是最明确的公开记录，但问题本身不限于 Craftoria 或 Powah 类 mod。

**Direct fix applied:** 已在 anti-patterns.md 的 AP18 条目中添加 Generalizability note，引用了 cesspit.net 的间接证据和其他包类型的潜在风险。

**No further action needed.** AP18 的 scope 无需限制。

---

## 4. R30 -- Quest Visual Hierarchy & Size Consistency

**Question:** size/shape 规则在非 ATM 包适用吗？

**Verdict:** **Size 规则通用；Shape 规则需要 pack-type 条件判断。**

R30 包含三个子检查：

| Check | 通用性 | 说明 |
|---|---|---|
| Check 1: milestone size > routine size | **通用** | "重要节点应该视觉上更大" 是普适设计原则。Monifactory CONTRIBUTING.md 明确要求 "Larger quests should be reserved for important milestones"，但这不是 Monifactory 特有的——ATM-10 的 capstone quest 也始终大于 routine quest。 |
| Check 2: optional < milestone size | **通用** | 与 Check 1 同理。 |
| Check 3: Shape consistency within role | **ATM-biased** | "milestone quests use 4+ different shapes" 的检查仅在 shape-rich 包（ATM ~47% explicit shape）中有意义。Curated packs（3-8% explicit shape）通常不设置 shape，所以 milestone_shapes 集合自然很小或为空，此检查不会触发。 |

**Assessment:** Check 3 的代码逻辑已包含 `len(milestones) >= 4` 的阈值条件，在 milestone 数量少于 4 的 chapter 中自动跳过。对于不使用 shape 词汇的包，此检查基本无害。但文档中的 Monifactory CONTRIBUTING.md 引用可能给 non-ATM/non-Monifactory 包作者造成误导——让他们以为需要建立 shape vocabulary。

**Recommendation (no direct fix needed):** R30 的触发条件设计已足够合理（`if len(milestones) > 2`），shape 检查在实际中极少在非 ATM 包上触发。但建议在 R30 的 "违反了会怎样" 段落中添加一句说明："对于不使用丰富 shape 词汇的包（大多数 non-ATM 包），Check 3 通常不会触发——size 是更通用的视觉层级工具。"

---

## 5. R31 -- XP-Level Reward Relativity

**Question:** milestone 判定逻辑是否有 ATM bias？

**Verdict:** **已修复——原代码有 ATM shape bias，添加了 size-based 通用 fallback。**

原代码的 milestone 判定：
```python
Q.shape in ("gear", "pentagon", "hexagon")  # common milestone shapes
```

这三个 shape 全部来自 ATM 系列（ATM-10 Mekanism=gear, welcome=pentagon, Ars Nouveau=hexagon）。对于不使用这些 shape 的包（即大多数 non-ATM 包），此条件永远为 false，导致里程碑判定完全依赖 `len(dependents) >= 3` 和 `is_capstone()` 两个条件。这可能漏掉一些通过 size 或独特 shape 标记的里程碑 quest。

**Direct fix applied:** 已在 progression-rules.md 中修改 R31 的 milestone 判定逻辑：
1. 添加 `Q.size > chapter_median_size * 1.5` 作为通用 size-based 里程碑检测
2. 将 ATM shapes 标注为 `# ATM-specific shapes`
3. 添加注释说明 shape-based 检测的 ATM-specificity

修复后的判定顺序：dependents count -> capstone detection -> size comparison (universal) -> shape (ATM fallback)。

---

## 6. R32 -- Chapter QA Coverage Heuristic

**Question:** 是否太具体（仅适用于有 CONTRIBUTING.md 的包）？

**Verdict:** **信号本身通用；文档引用偏 Monifactory。**

R32 的四个信号分析：

| Signal | 通用性 | 说明 |
|---|---|---|
| Signal 1: Dead-end detection | **通用** | "无 reward 且无后继的 non-optional quest" 是任何包的 untested 信号。 |
| Signal 2: Description coverage (>30% empty) | **通用** | 空描述比例是 quest 质量的通用指标。文档引用 Monifactory CONTRIBUTING.md 的 "substantive descriptions" 要求作为基准，但 30% 阈值本身是合理的——即使不参考任何 CONTRIBUTING.md，30%+ 空描述也说明 chapter 未经充分审查。 |
| Signal 3: Dependency orphans | **通用** | 跨 chapter 孤立 quest 是结构问题，与包类型无关。 |
| Signal 4: 0% optional in large chapter | **通用** | 大型 chapter（10+ quests）全部 mandatory 是 untested 信号。 |

**Assessment:** R32 的四个信号都是基于图结构的通用启发式，不依赖特定包的 CONTRIBUTING.md。Monifactory CONTRIBUTING.md 的引用仅出现在 Signal 2 的 WARNING 文本中作为 benchmark 参考——即使没有这个引用，30% 阈值仍然合理。

Enigmatica 10 的零投诉现象和 FTB Architect's Exodus 的 16+ issue 对比提供了独立的验证——这两个包都没有 CONTRIBUTING.md（或至少不以 quest 格式标准著称），但它们的 quest 质量差异恰好被 R32 的信号所捕获。

**Recommendation (no direct fix needed):** R32 的通用性没有问题。唯一建议是将 Signal 2 的 WARNING 文本中的 Monifactory 引用改为更通用的表述（"High-quality packs typically require substantive descriptions"），但这不影响规则的执行逻辑，优先级较低。

---

## Summary Table

| Item | Source | Generalizable? | Action taken |
|---|---|---|---|
| MP33 (Advancement Gate) | Enigmatica 10 (3 cases) | **CANNOT REVIEW -- content missing from file** | BLOCKER: must be written first |
| MP34 (Loot Table Reward) | Craftoria | **CANNOT REVIEW -- content missing from file** | BLOCKER: must be written first |
| AP17 (XP-Level Relativity) | Craftoria #289 | **Yes** -- Minecraft XP mechanic is universal | Added generalizability note |
| AP18 (Reward Desert) | Craftoria #231 | **Yes** -- deep chain pacing is universal | Added generalizability note |
| R30 (Visual Hierarchy) | Monifactory + ATM-10 | **Size: yes. Shape: ATM-biased but harmless** | Recommend adding scope note to docs |
| R31 (XP-Level Relativity) | Craftoria #289 | **Yes, but milestone detection had ATM bias** | Fixed: added size-based universal fallback |
| R32 (QA Coverage) | Enigmatica 10 + Monifactory | **Yes** -- structural signals are pack-agnostic | No fix needed |

---

## Action Items for Next Cycle

1. **[BLOCKER]** 编写 MP33 (Advancement Gate) 和 MP34 (Loot Table Reward) 并添加到 micro-patterns.md，包括 Scope Annotation Table 条目、Section Navigation 更新、以及 pack_types / Phase / Source confidence 标注。
2. **[LOW]** R30 的 "违反了会怎样" 段落添加 shape-check 的 ATM-scope 说明。
3. **[LOW]** R32 Signal 2 的 WARNING 文本中将 Monifactory 引用替换为通用表述。
4. **[INFO]** AP17/AP18 虽然单源（Craftoria），但通用性论证充分，不需要更多数据源。后续如有其他包的 issue tracker 数据可补充为 validation。
