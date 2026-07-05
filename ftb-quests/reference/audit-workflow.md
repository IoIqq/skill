# FTB Quests — DLC vs installed audit (on-demand workflow)

Load this when the task is to **compare a DLC source pack against an installed pack** ("is the install identical to the DLC? what item IDs are referenced in descriptions?"). This is a diff/audit task, not generation — the skill's main Protocol doesn't cover it. Scripts: `scripts/audit_index.py` + `scripts/audit_diff.py` (+ `ftbq/audit.py`).

## The resume-first flow

Do NOT re-scan both packs from scratch every call. The audit index caches file checksums + description formatting patterns (the `&e`/`&<color>` highlight spans and any `&e<modid:item>…&r` item-id references — note: in the audited Create pack the `&e…&r` spans are highlighted *phrases*, not item-id links; true item-name references come via `{item.modid:name}` placeholders in lang-file packs) per pack, so only files that actually changed get re-audited. This is the CodeGraph `analyze → status → query` flow applied to the audit:

- **analyze** — `python scripts/audit_index.py <packroot>` writes `<quests>/.ftbq-cache/audit_index.json5` (per-file sha256/size/mtime, per-quest item-ID patterns, chapter/quest counts, a whole-pack `pack_hash`).
- **status** — `python scripts/audit_index.py <packroot> --status` re-stats every file and reports `fresh`/`stale` (+ changed paths) without rewriting. Exit `0` = fresh, `1` = stale.
- **query (+ resume)** — `python scripts/audit_diff.py <dlc_pack> <target_pack>` is the entry point a NEW conversation runs first. It **resumes by default**: if `.ftbq-cache/audit_report.json5` exists AND both indexes are fresh (on-disk files unchanged) AND the report's `pack_hash` still matches, it prints the SAVED verdict (Task A diff + Task B per-quest description formatting/item-reference patterns + per-pack chapter/quest counts) and exits — **no re-audit, no re-read of quest files**. Only when the report is missing or a pack changed does it re-audit that pack and rewrite the report. `--force` skips resume and always recomputes; `--json` is machine-readable; non-zero exit when the packs differ (CI-friendly "is the install identical?" gate).

The persisted `audit_report.json5` is the "record once, reuse across conversations" artifact — a new session reads it instead of re-scanning both packs.

Remember the pack pair so subsequent `/ftb-quests` calls don't re-ask the paths:

```bash
python scripts/audit_diff.py <dlc_pack> <target_pack> --remember   # first time: saves the pair
python scripts/audit_diff.py <dlc_pack>                             # resumes if fresh; --force recomputes; --json / --no-rebuild also available
```

## At the start of every new conversation touching this DLC

Run `audit_diff.py` (with the remembered pair or both paths) BEFORE doing any other audit yourself. If the output says `resumed from <date>`, the prior audit is still valid — **trust it and do NOT re-read the quest files or re-run a full scan**; proceed straight to the interview or the fix the report surfaces. Only if it says `fresh` (it re-audited because something changed) read the new verdict the same way. The pair lives inside the **DLC source's** `.ftbq-cache/` (the DLC folder is the canonical edit location; the target modpack is a deploy destination, not an edit location — don't write into it unless the user explicitly asks, same `--deploy` discipline as Step 5b).

Re-audit triggers: a file under either pack's `quests/` was added/removed/edited (mtime+size drift → the index goes stale → `audit_diff.py` re-audits that pack and rewrites the report). Tweaking a quest title in-place that doesn't touch the chapters/lang files needs no re-audit.

Open the audit with a one-line summary (in the user's language): "Audit (resumed/fresh): Task A identical / K files differ. Task B: P item-ID patterns across Q quests." Then proceed to the interview or the fix the audit surfaced.
