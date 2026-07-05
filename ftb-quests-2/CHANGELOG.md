# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Validation script (`scripts/validate_quests.py`) for automated quest config checking
- Inline balance review protocol (grill-me style interview)
- Format mismatch / unknown version fallback guidance
- `.claude/` added to `.gitignore` to exclude dev artifacts

### Changed

- README.md streamlined to focus on installation and quick start
- Step 5 now prioritizes validation script over manual self-check

## [1.0.0] - 2026-06-19

### Added

- Initial release of FTB Quests skill
- SKILL.md with complete workflow protocol
- Reference documentation (`reference/ftb-quests-reference.md`)
- Support for modern JSON5 format (MC 26.1.x)
- Legacy SNBT format detection and generation
- Smart format detection from existing quest files
- Interview-driven quest generation workflow
- Complete task and reward type reference
- Full worked example with English and Chinese localization
- MIT License

### Format Support

- Modern JSON5 (FTB Quests 2025+, MC 26.1.x)
- Legacy SNBT (older modpacks, <=1.20 / early-1.21)
- Auto-detection based on existing files

### Features

- Chapter and quest generation with deterministic IDs
- Localization file generation (en_us, zh_cn)
- Dependency chain wiring
- Item task/reward object formatting
- Adaptive interview depth based on user preference
- Integration guidance for KubeJS, JEI/REI/EMI

[Unreleased]: https://github.com/IoIqq/ftb-quests-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/IoIqq/ftb-quests-skills/releases/tag/v1.0.0