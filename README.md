# AI Code Annotator

A developer tooling system for **explicitly marking, tracking, and validating AI-generated code** in software repositories for legal compliance, auditability, and governance.

## 🎯 Core Philosophy

**Explicit over Implicit** | **Compliance over Convenience** | **Deterministic over Heuristic**

This system does **NOT** attempt to detect Copilot or AI usage automatically. Instead, it **enforces explicit developer declaration** and provides **automated validation** to ensure all AI-generated code carries mandatory metadata annotations.

## ✨ Key Features

- **VS Code Extension**: Simple prompt-based annotation workflow during development
- **Python Validator CLI**: Comprehensive scanning and validation of code repositories
- **Pre-Commit Integration**: Prevents commits with unannotated AI-generated code
- **GitHub Actions CI/CD**: Automated validation in your pipeline
- **Language Support**: Python, JavaScript, TypeScript, Java, C++, Go, Ruby, PHP, and more
- **Zero False Positives**: Only validates actual annotation blocks, no heuristics
- **Audit-Ready**: Machine-readable JSON output for compliance reporting

## 🏗️ How It Works

### Annotation Format

All AI-generated code must be wrapped with mandatory metadata annotations:

```python
# START_AI_GENERATED_CODE
# TOOL_NAME: GitHub Copilot
# TOOL_VERSION: 1.0
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def example_function():
    return "This code was AI-generated"
# END_AI_GENERATED_CODE
```

### Validation Rules

Each annotation block must have:
- ✅ `START_AI_GENERATED_CODE` and `END_AI_GENERATED_CODE` markers
- ✅ `TOOL_NAME` - Name of the AI tool used (required, non-empty)
- ✅ `DATE` - ISO 8601 timestamp (e.g., `2025-02-15T10:30:00Z`)
- ✅ `AUTHOR_ID` - Developer identifier (required, non-empty)
- ✅ `ACTION` - Must equal `GENERATED` (required)
- ℹ️ `TOOL_VERSION` - Optional version of the AI tool

## 🚀 Quick Start

### 1. Install VS Code Extension

```bash
# From the src/vscode-extension directory
npm install
npm run compile
```

Then load the extension in VS Code for development or package it for distribution.

### 2. Install Python Validator

```bash
cd src/python-validator
pip install -e .
```

### 3. Test the Validator

```bash
# Validate current directory
ai-code-validator

# JSON output for CI/CD
ai-code-validator --output-format json

# Validate specific path
ai-code-validator --repo-path /path/to/repo
```

### 4. Set Up Pre-Commit Hook

```bash
pip install pre-commit
pre-commit install
```

Now the validator runs automatically before each commit.

### 5. Configure VS Code Extension

In VS Code settings, add your author ID:

```json
{
  "ai-annotator.authorId": "your-dev-id",
  "ai-annotator.defaultTool": "GitHub Copilot"
}
```

## 📖 Usage Guide

### Using the Extension

#### Manual Annotation (Keyboard Shortcut)
1. Select code in VS Code
2. Press **Ctrl+Shift+A** (Windows/Linux) or **Cmd+Shift+A** (Mac)
3. Enter the AI tool name, version (optional), and confirm
4. Code is automatically wrapped with annotations

#### Auto-Detection for Pasted Code
1. Paste multi-line code block into editor
2. Extension asks: "Was this code generated using AI?"
3. Select **Yes** to provide metadata
4. Code is wrapped with annotations

### Running the Validator

```bash
# Basic validation (text output)
ai-code-validator

# JSON output (for CI/CD pipelines)
ai-code-validator --output-format json

# Validate specific files only
ai-code-validator --file-patterns "*.py,*.js,*.ts"

# Exclude patterns
ai-code-validator --exclude-patterns "build,dist,.git"

# Verbose output
ai-code-validator --verbose
```

### Pre-Commit Integration

The validator automatically runs before commits. If validation fails, commit is prevented:

```bash
# To bypass in emergencies (not recommended)
git commit --no-verify
```

## 🔧 Configuration

### Validator Configuration

Options can be passed via CLI arguments:

```bash
ai-code-validator \
  --repo-path . \
  --file-patterns "*.py,*.js,*.ts" \
  --exclude-patterns "build,node_modules,.git" \
  --output-format json \
  --verbose
```

### VS Code Settings

Set in VS Code settings JSON:

```json
{
  "ai-annotator.authorId": "your-developer-id",
  "ai-annotator.defaultTool": "GitHub Copilot",
  "ai-annotator.defaultToolVersion": "1.0"
}
```

### Pre-Commit Configuration

The `.pre-commit-config.yaml` file is already configured to:
- Run the validator on Python, JavaScript, and TypeScript files
- Fail commits if validation errors are found
- Support custom exclude patterns

## 📊 Validator Output

### Text Output (Default)

```
❌ AI code annotation validation FAILED

Summary:
  Total files scanned: 42
  Files with errors: 3
  Total errors: 5

Errors:
  src/module1.py:15
    → Missing or empty required field: AUTHOR_ID
  src/module2.py:28
    → Invalid DATE format: 2025/02/15 (expected ISO 8601)
  src/module3.ts:42
    → START_AI_GENERATED_CODE marker found but no matching END_AI_GENERATED_CODE
```

### JSON Output (For CI/CD)

```json
{
  "valid": false,
  "errors": [
    {
      "file": "src/module1.py",
      "line": 15,
      "message": "Missing or empty required field: AUTHOR_ID"
    }
  ],
  "summary": {
    "total_files": 42,
    "files_with_errors": 3,
    "total_errors": 5
  }
}
```

## 🤖 GitHub Actions Integration

The system automatically runs on every push and pull request. Failed validations will block PR merges.

View the workflow in `.github/workflows/validate-ai-code.yml`.

## ⚠️ Limitations & Design Decisions

### What This System Does NOT Do

- ❌ Does **NOT** auto-detect Copilot or AI tool usage
- ❌ Does **NOT** use heuristics to guess if code is AI-generated
- ❌ Does **NOT** modify code without explicit user request
- ❌ Does **NOT** block non-AI code or manual code

### Design Decisions

1. **Explicit Declaration Only**: Developers decide what to annotate
2. **No Auto-Detection**: Heuristics are unreliable and create false positives
3. **Language-Aware Comments**: Uses appropriate syntax for each language
4. **ISO 8601 Dates**: Standard timestamp format for consistency
5. **Deterministic Validation**: No guessing, clear pass/fail rules

## 📦 Project Structure

```
AI-Annotation/
├── src/
│   ├── vscode-extension/       # VS Code extension (TypeScript)
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── extension.ts
│   │   │   ├── annotationHandler.ts
│   │   │   ├── editorListener.ts
│   │   │   ├── promptManager.ts
│   │   │   └── types.ts
│   │   └── test/
│   │
│   └── python-validator/       # Python validator (CLI tool)
│       ├── pyproject.toml
│       ├── src/ai_code_validator/
│       │   ├── cli.py
│       │   ├── scanner.py
│       │   ├── parser.py
│       │   ├── reporter.py
│       │   └── config.py
│       └── tests/
│
├── .github/workflows/          # CI/CD
│   └── validate-ai-code.yml
├── .pre-commit-config.yaml     # Pre-commit hooks
├── README.md                   # This file
├── CONTRIBUTING.md             # Development guide
└── docs/
    ├── ARCHITECTURE.md         # Technical architecture
    └── ANNOTATION_FORMAT.md    # Specification details
```

## 🧪 Testing

### Python Validator Tests

```bash
cd src/python-validator
pip install -e ".[dev]"
pytest
```

### VS Code Extension Tests

```bash
cd src/vscode-extension
npm install
npm test
```

## 🛠️ Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Development setup
- Building from source
- Running tests
- Submitting changes

## 📋 Annotation Specification

See [docs/ANNOTATION_FORMAT.md](./docs/ANNOTATION_FORMAT.md) for detailed specification of:
- Annotation block syntax
- Metadata field requirements
- Language-specific comment styles
- Validation rules

## 🏛️ Architecture

See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) for:
- Component overview
- Extension workflow
- Validator algorithm
- CI/CD integration

## 📄 License

MIT License - See [LICENSE](./LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📞 Support

For issues, questions, or feature requests, please open a GitHub issue.

---

**Remember**: Explicit declaration of AI-generated code is a compliance and governance practice. This system helps you maintain it automatically.