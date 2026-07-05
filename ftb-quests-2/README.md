# FTB Quests Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Minecraft](https://img.shields.io/badge/Minecraft-1.20%2B-green.svg)](https://www.minecraft.net/)
[![FTB Quests](https://img.shields.io/badge/FTB%20Quests-Modern%20JSON5-blue.svg)](https://github.com/FTBTeam/FTB-Quests)

A Claude Code skill that generates **FTB Quests** configuration files for Minecraft modpacks — correct for the **modern JSON5 on-disk format** used by current FTB Quests.

> Format verified against the FTB Quests source on 2026-06-19
> ([`FTBTeam/FTB-Quests`](https://github.com/FTBTeam/FTB-Quests) `main`, MC `26.1.x`,
> [`FTBTeam/FTB-Library`](https://github.com/FTBTeam/FTB-Library),
> [`marhali/json5-java`](https://github.com/marhali/json5-java)).

## Features

- **Smart format detection**: Automatically detects whether your modpack uses modern JSON5 or legacy SNBT format
- **Interview-driven**: Asks about your modpack theme, mods, structure, and rewards before generating
- **Complete output**: Generates `data.json5`, chapter files, and localization files (English + Chinese)
- **Validation included**: Built-in validation script checks JSON5 syntax, ID uniqueness, and lang file consistency
- **Balance review**: Optional difficulty pacing interview to ensure smooth progression

## What it gets right

The skill handles the parts that are easy to get wrong by hand:

- **JSON5, not SNBT**: Commas between fields, plain numbers (`0.0` not `0.0d`), `true`/`false` (not `1b`)
- **Items as objects**: `item: { id: "...", count: N }`, never bare strings
- **Item-task count gotcha**: Required quantity is a *sibling* `count` field, not the item's count
- **Text in lang files**: Modern FTB Quests ignores inline titles
- **Deterministic IDs**: Uses `md5("<pack>/<chapter>/<obj>/<name>")` for stable regeneration

## Installation

### Option 1: Clone directly (recommended)

`ash
# Linux/macOS
git clone https://github.com/IoIqq/ftb-quests-skills.git ~/.claude/skills/ftb-quests

# Windows (PowerShell)
git clone https://github.com/IoIqq/ftb-quests-skills.git C:\Users\<you>\.claude\skills\ftb-quests
`

### Option 2: Manual download

1. Download the [latest release](https://github.com/IoIqq/ftb-quests-skills/releases)
2. Extract to `~/.claude/skills/ftb-quests/` (or `C:\Users\<you>\.claude\skills\ftb-quests\` on Windows)

## Usage

In any Claude Code session, ask for FTB Quests work:

- `帮我生成 FTB 任务线` (Chinese)
- `Create FTB quests for my modpack` (English)
- `Generate quest config` (any language)

The skill will:
1. Detect your modpack format (if existing quests are present)
2. Interview you about theme, mods, structure, and rewards
3. Generate complete quest configuration files
4. Validate the output before handing off

### Example workflow

```
You: 帮我用 FTB Quests 生成一个科技整合包的任务线

Claude: [Asks about theme, mods, chapter count, reward philosophy...]
[Generates data.json5, chapters/*.json5, lang/en_us/quests.json5]
[Runs validation script]
✅ Generated 3 chapters, 12 quests, 18 tasks, 15 rewards
```

## Requirements

- **Claude Code** or compatible skill system
- **Python 3.6+** (for validation script)
- **Modpack folder** with `mods/` directory or `manifest.json` (optional — works for new packs too)
- **In-game**: `/ftbquests editing_mode` to load generated quests

## Project structure

```
ftb-quests/
├── SKILL.md                                    # Workflow and format rules
├── reference/
│   └── ftb-quests-reference.md                 # Exhaustive field reference
├── scripts/
│   └── validate_quests.py                      # Validation script
├── README.md                                   # This file
├── CONTRIBUTING.md                             # Contribution guidelines
├── CHANGELOG.md                                # Version history
└── LICENSE                                     # MIT license
```

## Validation

Run the validation script on generated quest configs:

`ash
python scripts/validate_quests.py /path/to/your/modpack/config/ftbquests/quests/
`

Checks:
- JSON5 syntax (comments, trailing commas)
- ID uniqueness (16-char uppercase hex)
- Dependency references exist
- Item fields are objects (not bare strings)
- Lang file has title entries for all quests/chapters

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting issues, suggesting features, or submitting pull requests.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

- [FTB Team](https://github.com/FTBTeam) for FTB Quests mod
- [marhali](https://github.com/marhali) for json5-java library
- [Anthropic](https://www.anthropic.com/) for Claude Code