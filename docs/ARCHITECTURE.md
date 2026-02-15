# Architecture Overview

This document describes the technical architecture of the AI Code Annotation system.

## System Components

```
┌─────────────────┐
│  VS Code Editor │
└────────┬────────┘
         │
         └─→ [AI Code Annotator Extension]
             ├─ EditorListener (detects insertions)
             ├─ PromptManager (user dialogs)
             ├─ AnnotationHandler (wraps code)
             └─ Extension main (command registration)
                     │
                     ├─ Generates annotations
                     │
                     │
┌────────────────────────────────────────┐
│     Git Repository with Code           │
│  (contains annotated and plain code)   │
└────────────────────────────────────────┘
         │
         └─→ [Pre-Commit Hook]
             └─→ Python Validator CLI
                 ├─ FileScanner (discovers files)
                 ├─ AnnotationParser (validates blocks)
                 ├─ ResultReporter (formats output)
                 └─ CLI (argument parsing)
                     │
                     ├─ Success → commit proceeds
                     └─ Failure → commit blocked

         └─→ [GitHub Actions CI/CD]
             └─→ Python Validator CLI
                 └─→ Generates JSON report
                     └─→ Comment on PR
```

## Component Details

### VS Code Extension

**Location**: `src/vscode-extension/`

#### Core Modules

**extension.ts** - Main entry point
- Activates on startup
- Registers commands
- Sets up event listeners
- Coordinates between components

**editorListener.ts** - Text change detection
- Monitors `onDidChangeTextDocument` events
- Debounces rapid changes (500ms default)
- Detects multi-line insertions
- Triggers prompt for AI confirmation

**promptManager.ts** - User interaction
- Shows confirmation dialogs
- Collects metadata input
- Validates input before proceeding
- Displays errors and confirmations

**annotationHandler.ts** - Code wrapping
- Generates annotation blocks
- Handles language-specific comments
- Preserves code indentation
- Validates metadata before wrapping

**types.ts** - TypeScript definitions
- `AnnotationMetadata` interface
- `CommentStyle` for each language
- Language enum definitions

#### Extension Flow

```
Code Inserted → EditorListener detects
    ↓
    → Debounce 500ms
    ↓
    → Is multi-line? No → Exit
    ↓ Yes
    ↓
    → Show: "Was this AI-generated?"
    ↓
    → User selects "No" → Exit
    ↓ User selects "Yes"
    ↓
    → Prompt for Tool Name
    ↓
    → Prompt for Tool Version (optional)
    ↓
    → Prompt for Author ID
    ↓
    → Validate metadata
    ↓ Valid
    ↓
    → Get comment style for language
    ↓
    → Wrap code with annotations
    ↓
    → Insert wrapped code into editor
    ↓
    → Show success message
```

### Python Validator

**Location**: `src/python-validator/`

#### Core Modules

**config.py** - Configuration management
- `Config` class holds settings
- File patterns (default: common languages)
- Exclude patterns (default: build dirs, .git, etc.)
- `from_cli_args()` factory method

**scanner.py** - File discovery
- `FileScanner` class
- Recursive directory traversal
- Pattern matching for file types
- Respects exclusion patterns
- Yields `(file_path, content)` tuples

**parser.py** - Annotation validation
- `AnnotationParser` class
- Detects `START_AI_GENERATED_CODE` blocks
- Extracts metadata fields
- `AnnotationBlock` dataclass for valid blocks
- `AnnotationError` dataclass for errors

**Validation Rules**:
- Both markers must exist
- All required fields present and non-empty
- DATE in ISO 8601 format
- ACTION must equal "GENERATED"
- Metadata lines are parsed from comments

**reporter.py** - Result formatting
- `ResultReporter` class
- Generates JSON output (machine-readable)
- Generates text output (human-readable)
- `ValidationResult` dataclass

**JSON Output Schema**:
```json
{
  "valid": true/false,
  "errors": [
    {
      "file": "path/to/file.py",
      "line": 10,
      "message": "error description"
    }
  ],
  "summary": {
    "total_files": 42,
    "files_with_errors": 3,
    "total_errors": 5
  }
}
```

**cli.py** - Command-line interface
- `main()` function as entry point
- Argument parser with options
- Error handling and exit codes
- Integration of all components

#### Validator Flow

```
Start → Parse CLI arguments
    ↓
    → Create Config from args
    ↓
    → Create FileScanner with Config
    ↓
    → Create AnnotationParser
    ↓
    → Create ResultReporter
    ↓
    → For each file from scanner:
    │   ├─ Read file content
    │   ├─ Validate with parser
    │   └─ Collect errors
    ↓
    → Generate ValidationResult
    ↓
    → Format and print output
    ↓
    → Exit with code:
    │   ├─ 0 if valid
    │   └─ 1 if errors
```

#### Error Detection Logic

```python
for line in file_content:
    if "START_AI_GENERATED_CODE" in line:
        # Find matching END marker
        # Extract metadata lines
        # Validate each field
        # Report errors for invalid fields
```

### Pre-Commit Integration

**File**: `.pre-commit-config.yaml`

- Defines local hook that runs validator
- Triggers on commit stage
- Only runs on modified files
- Blocks commit if validation fails

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-ai-code
        entry: python -m ai_code_validator.cli
        language: python
```

### GitHub Actions CI/CD

**File**: `.github/workflows/validate-ai-code.yml`

- Triggers on push and PR
- Sets up Python 3.11
- Installs and runs validator
- Parses JSON output
- Comments results on PR
- Fails workflow if validation fails

## Data Flow

### Annotation Creation

```
Developer → Pastes AI code in editor
    ↓
    ↓ [EditorListener]
    ↓ Detects multi-line insertion
    ↓
VS Code → Shows confirmation dialog
    ↓
Developer → Confirms it's AI-generated
    ↓
VS Code → Prompts for metadata
    ↓
Developer → Enters tool name, version, ID
    ↓
    ↓ [AnnotationHandler]
    ↓ Gets language comment style
    ↓ Wraps code with START/END markers
    ↓
VS Code → Replaces code block with wrapped version
    ↓
Repository → Now contains annotated code
```

### Annotation Validation

```
Developer → Attempts to commit
    ↓
    ↓ [Pre-Commit Hook]
    ↓ Runs validator on modified files
    ↓
    ↓ [FileScanner]
    ↓ Finds modified code files
    ↓
    ↓ [AnnotationParser]
    ↓ Scans for START/END markers
    ↓ Validates metadata fields
    ↓ Detects violations
    ↓
    ↓ [ResultReporter]
    ↓ Formats results
    ↓
Git → Shows validation result
    ├─ If valid → Commit succeeds
    └─ If invalid → Commit blocked
```

## Language Support

### Supported Languages

| Language | Comment Style | Example |
|----------|---------------|---------|
| Python | `#` | `# TOOL_NAME: ...` |
| JavaScript | `//` | `// TOOL_NAME: ...` |
| TypeScript | `//` | `// TOOL_NAME: ...` |
| Java | `//` | `// TOOL_NAME: ...` |
| C++ | `//` | `// TOOL_NAME: ...` |
| Go | `//` | `// TOOL_NAME: ...` |
| Ruby | `#` | `# TOOL_NAME: ...` |
| PHP | `//` | `// TOOL_NAME: ...` |
| Swift | `//` | `// TOOL_NAME: ...` |
| Kotlin | `//` | `// TOOL_NAME: ...` |
| SQL | `--` | `-- TOOL_NAME: ...` |
| Haskell | `--` | `-- TOOL_NAME: ...` |
| Shell | `#` | `# TOOL_NAME: ...` |
| MATLAB | `%` | `% TOOL_NAME: ...` |

### Adding New Languages

To add a new language in `types.ts`:

```typescript
LANGUAGE_COMMENT_STYLES['mylanguage'] = {
  lineComment: '// or # or --',
  blockCommentStart: '/* (optional)',
  blockCommentEnd: '*/ (optional)'
}
```

## Error Handling

### Python Validator

- **File read errors**: Logged, file skipped, continues scanning
- **Invalid annotation**: Error added to results
- **Missing markers**: Error with line number
- **Invalid metadata**: Specific field error message
- **Invalid date format**: ISO 8601 validation error

### VS Code Extension

- **No editor**: Error dialog shown
- **No selection**: Error dialog shown
- **Unsupported language**: Error dialog shown
- **Invalid metadata**: Prevents annotation
- **User cancellation**: Silently exits

## Testing Strategy

### Python Validator Tests

- **Unit tests**: Each component (scanner, parser, reporter)
- **Integration tests**: CLI with real files
- **Edge cases**: Missing markers, invalid dates, etc.
- **File system tests**: Temp directories for isolation

### VS Code Extension Tests

- **Unit tests**: Validation logic, metadata handling
- **Mock tests**: VS Code API interactions (sinon stubs)
- **Metadata tests**: Input validation
- **Comment style tests**: Language-specific formatting

## Performance Considerations

- **Debounce delay**: 500ms avoids excessive prompts during rapid typing
- **File scanning**: Lazy evaluation, processes one file at a time
- **Regex matching**: Simple string containment check, no complex patterns
- **Memory**: Stores only error info, not full file contents

## Security Considerations

- **No code execution**: Only parses/validates, never executes code
- **No network calls**: Fully offline operation
- **File permissions**: Respects read permissions, handles gracefully
- **Input validation**: All fields validated before use
- **No credential storage**: No auth tokens or secrets
