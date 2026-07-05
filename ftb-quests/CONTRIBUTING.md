# Contributing to FTB Quests Skill

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Issues

Before creating an issue:
- Check existing issues to avoid duplicates
- Test with the latest version of the skill
- Provide clear reproduction steps if applicable

When reporting:
- Use the issue templates when available
- Include your Minecraft version, FTB Quests version, and modpack details
- Attach generated quest files if they fail to load
- Describe expected vs actual behavior

### Suggesting Features

- Explain the use case and why it's valuable
- Provide examples of how the feature would be used
- Consider edge cases and potential conflicts with existing functionality

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Guidelines

### Code Style

- Follow existing code style in the repository
- Use 2-space indentation for JSON5 files
- Keep comments concise and helpful
- Use meaningful variable and function names

### Testing

**Don't run the whole suite for every change.** Target the tests that cover what you touched — the full suite is for CI and pre-release, not for every iteration. Picking the right module keeps the feedback loop under a second.

Run just the relevant module(s):

```bash
python -m pytest tests/test_<module>.py -v          # one module
python -m pytest tests/test_a.py tests/test_b.py -v # several
python -m pytest tests/test_<module>.py::test_name  # a single test
```

**Test → source map** (pick by what you changed):

| You changed… | Run |
|---|---|
| `ftbq/json5.py` (lexer/parser) | `test_json5_parser.py` |
| `ftbq/canonical.py` (emitter) | `test_canonical.py` |
| `ftbq/snbt.py` (SNBT emitter/parser, 1.20.1) | `test_snbt_emit.py` + `test_snbt_parse.py` |
| `ftbq/ids.py` (md5 ID / content hash / id mask / `reward_table_id` / `hex_to_long` / `quest_link_id` / `image_id`) | `test_ids.py` + `test_id_stability.py` |
| `scripts/extract_mods.py` | `test_extract_mods.py` |
| `scripts/extract_items.py` (item ids + name→id index) | `test_extract_items.py` |
| `scripts/index_quests.py` | `test_linkage.py` (the `test_indexer_*` cases) |
| `scripts/generate_quests.py` — dep resolution, hex passthrough | `test_linkage.py` + `test_id_stability.py` |
| `scripts/generate_quests.py` — auto_layout / coordinates | `test_layout.py` |
| `scripts/generate_quests.py` — incremental merge / `--adopt` / renames | `test_incremental.py` |
| `scripts/generate_quests.py` — reward tables / `table_id` resolution | `test_reward_tables.py` |
| `scripts/generate_quests.py` — quest_links / chapter images / chapter passthrough | `test_quest_links_images.py` |
| `scripts/generate_quests.py` — item count lift / `ftbquests:xp` `points` default | `test_task_reward_fields.py` |
| `scripts/generate_quests.py` — `format: "snbt"` emit layer / inline text | `test_snbt_generate.py` + `test_snbt_emit.py` |
| `ftbq/deploy.py` or `generate_quests.py --deploy` | `test_deploy.py` |
| `scripts/generate_quests.py` — output layout (`quests/` subfolder) | `test_incremental.py` + `test_id_stability.py` + `test_layout.py` |
| `scripts/validate_quests.py` (incl. reward tables / `E_TABLE_MISSING` / SNBT) | `test_validator.py` + `test_snbt_validate.py` |
| `ftbq/audit.py` (audit index / freshness / diff / item-pattern extraction) | `test_audit.py` |
| `ftbq/ids.py` — `IdRegistry` / `_validate_unique_ids` (id uniqueness) | `test_id_uniqueness.py` |
| `scripts/audit_index.py` or `scripts/audit_diff.py` (CLIs) | `test_audit.py` (the `test_cli_*` cases) |
| `scripts/pack_briefing.py` or `scripts/quest_detail.py` (token-saving CLIs) | `test_briefing.py` |
| `scripts/lookup_item.py` (batch name→id lookup) | `test_lookup_item.py` |
| `lang/` rewriting or placeholder logic | `test_id_stability.py::test_lang_placeholders_rewritten_to_hex` |

**When you must run the full suite:**
- before pushing a release tag,
- after touching `ftbq/__init__.py` or `conftest.py` (shared import surface),
- after a change that could ripple across modules (e.g. the JSON5 parser, the canonical emitter, the SNBT emitter/parser, or the `generate()` entry point's signature),
- in CI (the workflow already does `pytest tests/ -v`).

If a targeted run is green but you're unsure of the blast radius, run the full suite once before pushing — not on every save. The validator script is a separate, faster check for generated output:

```bash
python scripts/validate_quests.py <test_dir>
```

Before submitting, also:
- Test generated quest files in-game with `/ftbquests editing_mode`
- Verify both English and Chinese localization work

### Documentation

- Update README.md if you change user-facing behavior
- Add inline comments for complex logic
- Update reference documentation for new fields or features
- Keep examples current and accurate

## What to Contribute

### High Priority

- Bug fixes for JSON5 generation issues
- Support for new FTB Quests versions
- Additional task/reward types
- Improved format detection

### Medium Priority

- Better error messages and debugging
- Performance optimizations
- Additional language support
- Documentation improvements

### Low Priority

- Cosmetic changes
- Minor refactoring without clear benefit
- Features that add significant complexity

## Questions?

Feel free to open an issue with the "question" label, or reach out to the maintainers directly.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.