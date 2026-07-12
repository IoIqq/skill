# Draft: Pack Mode Quest Book Pattern (MP38 candidate)

> **Status:** DRAFT — single-source (GreedyCraft only). Needs validation from other packs before formalizing as MP.
> **Date:** 2026-07-08
> **Source:** TCreopargh/GreedyCraft (MC 1.12.2, 168 stars)

## Pattern Description

A single modpack ships **multiple independent FTB Quests book instances** — one per "pack mode" (e.g., casual, expert, adventure) — sharing the same chapter structure and quest content, differentiated only by:

1. A **mode selector chapter** (first chapter) containing clickable quests that run `/packmode <mode>` to switch between books
2. **Book-level config differences** (e.g., `emergency_items_cooldown: "5m"` vs `"3m"`)
3. **Identical chapter content** across all modes (quest files share SHA hashes between modes)

## Implementation Details (GreedyCraft)

### Directory Structure
```
config/ftbquests/
├── casual/           # Casual mode quest book
│   ├── chapters/     # 16 chapter directories (same hashes as expert/adventure)
│   ├── file.snbt     # Book config (emergency_items_cooldown: "5m")
│   └── reward_tables/ # 4 reward tables (shared SHAs)
├── expert/           # Expert mode quest book
│   ├── chapters/     # 16 chapter directories (identical to casual)
│   ├── file.snbt     # Book config (identical to casual)
│   └── reward_tables/ # 4 reward tables (shared SHAs)
└── adventure/        # Adventure mode quest book
    ├── chapters/     # 16 chapter directories (mostly identical)
    ├── file.snbt     # Book config (emergency_items_cooldown: "3m")
    └── reward_tables/ # 4 reward tables (shared SHAs)
```

### Mode Selector Chapter
The first chapter (`4f1c7c7c`) is a "Pack Modes" chapter with:
- Background images showing all three mode icons
- A mode-highlight image that differs per book (casual_mode.png / expert_mode.png / adventure_mode.png)
- Clickable quests that run `/packmode <mode>` (with `player_command: true`) to switch the active pack mode

### Key Observations
- Quest files are **SHA-identical** between casual and expert modes (all non-selector quests)
- Adventure mode has minor differences (likely encoding/formatting, content is same)
- The "multi-mode" claim is **NOT** about different quest content per mode — it's about having separate FTB Quests book instances that the player can switch between via `/packmode`
- This is fundamentally a **Packmode** feature (from the Minecraft packmode mod) applied to quest books, not a quest book design pattern per se

## Design Assessment

**Strengths:**
- Player can choose difficulty without starting a new world
- Clean separation of mode-specific book configs

**Weaknesses:**
- Maintenance burden: 3 copies of the same quest data
- If quest content needs updating, all 3 copies must be updated
- SHA-identical files across modes means the "mode differentiation" is mostly cosmetic (the selector chapter + emergency cooldown)

## Is This Really a New Pattern?

**Phase 1 claimed:** "3 independent quest books" — this was an overstatement.
**Phase 3 correction:** This is 1 quest book replicated 3 times with a mode selector. The actual quest content is identical. The "multi-mode" is a packmode feature, not a quest design pattern.

**Decision:** This pattern is **NOT** recommended for formalization as MP38 unless:
1. Another pack is found that uses truly different quest content per mode (not just SHA-identical copies)
2. The pattern is generalized to "Packmode-Driven Quest Book Variation" where different modes can have meaningfully different quest chains

For now, document as a GreedyCraft-specific implementation note in the researched-packs registry.
