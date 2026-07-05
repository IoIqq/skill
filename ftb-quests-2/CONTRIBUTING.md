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

Before submitting:
- Test generated quest files in-game with `/ftbquests editing_mode`
- Run the validation script: `python scripts/validate_quests.py <test_dir>`
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