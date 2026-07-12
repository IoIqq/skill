# Drafts: Deferred Items

> **Date:** 2026-07-07 (updated 2026-07-08)
> **Status:** R33, R34, R35 have been archived to module files:
> - R33 → `mod-reward-design.md` (generator invariant)
> - R34 → `mod-reward-design.md` (distribution report)
> - R35 → `mod-dependency-graph.md` (shape semantics consistency)

## Deferred: step4-quickref.md (审查 C P2-8)

> **Status:** DEFERRED — high risk, needs careful content selection before execution.
> **Suggestion:** Review C noted that Step 4 currently loads ~877 lines of module files and suggested creating a ~200-line condensed reference (`step4-quickref.md`) to reduce token cost.
> **Why deferred:** Selecting which content to condense vs. omit requires careful analysis of what Step 4 actually uses at generation time. Incorrect omission could cause the generator to miss critical rules. This should be done as a dedicated revision pass, not bundled with rule corrections.
> **Candidate content for quickref:** R28 command safety (verbatim), R31 milestone heuristic, R10 bridge check pseudocode, R33 generator contract (summarized), AP9-AP11 one-line summaries, item reachability builtin tables.
> **Estimated savings:** ~600 lines / generation session if the quickref replaces full module loads.
