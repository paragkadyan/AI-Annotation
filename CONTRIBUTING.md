# Contributing to AI Code Annotator

Thank you for your interest in contributing! This document provides guidelines and instructions for developing the AI Code Annotation system.

## Development Setup

### Prerequisites

- Node.js 18+ and npm (for VS Code extension)
- Python 3.11+ (for validators and scripts)
- Git
- VS Code (for extension development)

### Setting Up the Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/AI-Annotation.git
cd AI-Annotation

# Install Python validator in development mode
cd src/python-validator
pip install -e ".[dev]"
cd ../..

# Install VS Code extension dependencies
cd src/vscode-extension
npm install
cd ../..
```

## Project Structure

The project is organized as a monorepo:

- `src/vscode-extension/` - VS Code extension (TypeScript)
- `src/python-validator/` - Python validator CLI tool
- `.github/workflows/` - GitHub Actions CI/CD
- `docs/` - Detailed documentation

## Development Workflow

### Python Validator

**Location**: `src/python-validator/`

#### Running Tests

```bash
cd src/python-validator
pytest                          # Run all tests
pytest tests/test_parser.py   # Run specific test file
pytest tests/ -v              # Verbose output
pytest --cov                  # With coverage report
```

#### Running the CLI

```bash
python -m ai_code_validator --help
python -m ai_code_validator --repo-path .
python -m ai_code_validator --output-format json
```

#### Code Style

- Follow PEP 8
- Use type hints
- Keep functions focused and testable

### VS Code Extension

**Location**: `src/vscode-extension/`

#### Building

```bash
cd src/vscode-extension
npm run compile              # One-time build
npm run watch              # Watch mode for development
npm run esbuild            # Bundle for production
```

#### Running Tests

```bash
cd src/vscode-extension
npm test
```

#### Debugging

1. Open VS Code at `src/vscode-extension/`
2. Press **F5** to launch Debug Extension
3. Use breakpoints in the code
4. Check the extension host output

#### Code Style

- Use ESLint configuration in `.eslintrc.json`
- Format with Prettier
- Use TypeScript strict mode

## Making Changes

### Before You Start

1. Check existing issues and PRs to avoid duplicates
2. For new features, consider opening an issue for discussion first
3. Ensure you have a clear understanding of the expected behavior

### Commit Guidelines

- Use clear, descriptive commit messages
- Follow the format: `<type>: <description>`
  - `feat:` - New feature
  - `fix:` - Bug fix
  - `docs:` - Documentation
  - `test:` - Test additions/updates
  - `refactor:` - Code refactoring
  - `chore:` - Build/tooling changes

Example:
```
feat: add support for Kotlin language annotations
test: improve parser validation test coverage
docs: clarify annotation format specification
```

### Testing

All code changes should include tests:

**Python**:
```bash
cd src/python-validator
pytest tests/test_parser.py -v  # Run tests for your changes
pytest --cov                     # Ensure coverage
```

**TypeScript**:
```bash
cd src/vscode-extension
npm test
```

### Code Review Checklist

Before submitting a PR, ensure:
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] No breaking changes (or clearly documented)
- [ ] Documentation is updated
- [ ] Commit messages are clear

## Key Design Principles

Remember these when contributing:

1. **Explicit over Implicit**: Always require explicit user action
2. **Compliance over Convenience**: Don't skip validation for speed
3. **Deterministic over Heuristic**: Use clear rules, no guessing
4. **Simple over Complex**: Keep implementations straightforward
5. **Testable Code**: Make code easy to test

## Areas for Contribution

### High Priority

- [ ] Additional language support (e.g., Rust, Scala, Clojure)
- [ ] Configuration file support (`.ai-annotation-config.json`)
- [ ] IDE plugins for IntelliJ, Sublime Text
- [ ] Integration examples with various workflows

### Medium Priority

- [ ] Enhanced error messages with suggestions
- [ ] Annotation statistics/reporting
- [ ] Integration with git hooks workflows
- [ ] Performance optimizations for large repos

### Nice to Have

- [ ] Web dashboard for annotation statistics
- [ ] Custom annotation templates
- [ ] Slack/Teams notifications
- [ ] Multi-language documentation

## Reporting Issues

When reporting bugs:

1. Include your environment (OS, Python/Node version)
2. Provide a minimal reproduction case
3. Describe the expected vs. actual behavior
4. Include relevant error messages or logs

## Documentation

Help improve documentation by:

- Clarifying existing docs
- Adding examples
- Correcting errors
- Suggesting new sections

Documentation files to update:
- `README.md` - Main overview
- `docs/ARCHITECTURE.md` - Technical details
- `docs/ANNOTATION_FORMAT.md` - Annotation spec
- Code comments - For complex logic

## Release Process

(For maintainers)

```bash
# Ensure all tests pass
pytest
npm test

# Update version in package.json and pyproject.toml
# Create git tag
git tag v1.0.0
git push origin v1.0.0
```

## Questions?

- Open an issue with the `question` label
- Check existing documentation first
- Read through related code and tests

## Code of Conduct

Be respectful and inclusive. We're building tools for compliance and governance - let's model good practices in how we collaborate.

Thank you for contributing!
