# Quick Reference Card

## For Developers Using the System

### Annotation Format (Quick)

```python
# START_AI_GENERATED_CODE
# TOOL_NAME: <tool name>
# TOOL_VERSION: <optional>
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: <your-id>
# ACTION: GENERATED
<your code>
# END_AI_GENERATED_CODE
```

### VS Code Extension

| Action | Shortcut |
|--------|----------|
| Quick Annotate | Ctrl+Shift+A (Windows/Linux) |
| Quick Annotate | Cmd+Shift+A (Mac) |
| Command Palette | Ctrl+Shift+P, then "Mark as AI-Generated" |

### Validator CLI

```bash
# Basic validation
python -m ai_code_validator

# JSON output (for CI/CD)
python -m ai_code_validator --output-format json

# Specific directory
python -m ai_code_validator --repo-path ./src

# Custom patterns
python -m ai_code_validator --file-patterns "*.py,*.js"

# Exclude directories
python -m ai_code_validator --exclude-patterns "build,node_modules"

# Verbose
python -m ai_code_validator --verbose
```

### Validator Configuration

#### Required Fields for Every Annotation Block

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| TOOL_NAME | Yes | Non-empty string | `GitHub Copilot` |
| DATE | Yes | ISO 8601 | `2025-02-15T10:30:00Z` |
| AUTHOR_ID | Yes | Non-empty string | `dev-001` |
| ACTION | Yes | Must be "GENERATED" | `GENERATED` |
| TOOL_VERSION | No | Any string | `1.0.0` |

### Supported Languages

| Language | Comment | Example |
|----------|---------|---------|
| Python | `#` | `# TOOL_NAME: ...` |
| JavaScript | `//` | `// TOOL_NAME: ...` |
| TypeScript | `//` | `// TOOL_NAME: ...` |
| Java | `//` | `// TOOL_NAME: ...` |
| C/C++ | `//` | `// TOOL_NAME: ...` |
| Go | `//` | `// TOOL_NAME: ...` |
| Ruby | `#` | `# TOOL_NAME: ...` |
| PHP | `//` | `// TOOL_NAME: ...` |
| Swift | `//` | `// TOOL_NAME: ...` |
| Kotlin | `//` | `// TOOL_NAME: ...` |
| SQL | `--` | `-- TOOL_NAME: ...` |
| Haskell | `--` | `-- TOOL_NAME: ...` |
| Shell | `#` | `# TOOL_NAME: ...` |
| MATLAB | `%` | `% TOOL_NAME: ...` |

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Missing TOOL_NAME" | Field empty or missing | Add: `# TOOL_NAME: Copilot` |
| "Invalid DATE format" | Wrong date format | Use ISO 8601: `2025-02-15T10:30:00Z` |
| "Missing AUTHOR_ID" | Field empty or missing | Add: `# AUTHOR_ID: dev-001` |
| "Invalid ACTION" | Not "GENERATED" | Change to: `# ACTION: GENERATED` |
| "No END marker" | Missing END marker | Add: `# END_AI_GENERATED_CODE` |

### Setup Instructions

#### 1. Install Validator
```bash
cd src/python-validator
pip install -e .
```

#### 2. Load VS Code Extension
```bash
cd src/vscode-extension
npm install
code .
# Then press F5 to launch debug
```

#### 3. Install Pre-Commit Hook
```bash
pip install pre-commit
pre-commit install
```

#### 4. Configure VS Code Settings
```json
{
  "ai-annotator.authorId": "your-dev-id",
  "ai-annotator.defaultTool": "GitHub Copilot"
}
```

### Pre-Commit Commands

```bash
# Install hooks (one-time)
pre-commit install

# Run manually
pre-commit run --all-files

# Bypass (emergency only)
git commit --no-verify
```

---

## For Project Leads

### Validation in CI/CD

GitHub Actions automatically validates on all pushes and PRs. View results in:
- Actions tab → `validate-ai-code` workflow
- PR comments with validation summary

### Policy Enforcement

Set branch protection rules to **require** validation success before merge:
1. Go to Settings → Branches
2. Add rule for `main`
3. Require status checks: `validate-ai-code`

### Audit Reporting

Get ISO 8601 audit trails:

```bash
# JSON output for processing
ai-code-validator --output-format json > audit_report.json
```

Result includes:
- Timestamp (from each annotation)
- Developer ID (AUTHOR_ID)
- AI Tool used
- Exact code location

---

## Troubleshooting

### Validator not finding files?

Check file patterns:
```bash
ai-code-validator --file-patterns "*.py,*.js,*.ts" --verbose
```

### Extension not prompting?

Requirements:
- Multi-line code insert (2+ lines)
- 500ms pause after insert
- Active VS Code editor

### Pre-commit hook not working?

Reinstall hooks:
```bash
pre-commit uninstall
pre-commit install
```

### Wrong date/author showing up?

Check VS Code settings:
```bash
# View current settings
code --user-data-dir
```

---

## Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Start here - overview and features |
| `TESTING_GUIDE.md` | How to test all components |
| `docs/ANNOTATION_FORMAT.md` | Detailed specification |
| `docs/ARCHITECTURE.md` | Technical details |
| `CONTRIBUTING.md` | Development guidelines |

---

## Key Points to Remember

✅ **Explicit**: Always confirm AI-generated code
❌ **NO Auto-Detection**: Never guess if code is AI-generated
✅ **Consistent Format**: Use exact metadata format
✅ **ISO 8601 Dates**: Always use timezone (Z or ±HH:MM)
✅ **Non-Empty Fields**: All required fields must have values
✅ **Deterministic**: Validation has clear pass/fail rules

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Validation passed - no errors |
| 1 | Validation failed - errors found |

---

## Real-World Example

### Scenario: You write code with GitHub Copilot

**Step 1**: Paste code into VS Code
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Step 2**: Extension asks "Was this AI-generated?"
→ Select: **Yes**

**Step 3**: Fill metadata
- Tool: `GitHub Copilot`
- Version: `1.0` (optional)
- Author: `dev-001`

**Step 4**: Code automatically becomes:
```python
# START_AI_GENERATED_CODE
# TOOL_NAME: GitHub Copilot
# TOOL_VERSION: 1.0
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
# END_AI_GENERATED_CODE
```

**Step 5**: Commit
→ Pre-commit validates → Commit succeeds ✅

**Step 6**: Pre-commit fails?
→ Add annotations → Commit succeeds ✅

---

Version: 1.0.0
Last Updated: 2025-02-15
