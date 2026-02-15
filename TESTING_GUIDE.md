# Quick Testing Guide

## Python Validator CLI - Quick Test

The validator is fully functional. Test it directly without installation:

### Test Valid Annotations
```bash
cd C:\Users\parag\OneDrive\Desktop\code\AI-Annotation

python -c "
import sys
sys.path.insert(0, 'src/python-validator/src')

from pathlib import Path
from ai_code_validator.parser import AnnotationParser

parser = AnnotationParser()
file_path = Path('tests/valid_annotations.py')
content = file_path.read_text()
blocks, errors = parser.validate_file(file_path, content)

print(f'Result: {\"PASS\" if len(errors) == 0 else \"FAIL\"}')
print(f'Valid blocks: {len(blocks)}')
print(f'Errors: {len(errors)}')
"
```

### Test Invalid Annotations
```bash
python -c "
import sys, json
sys.path.insert(0, 'src/python-validator/src')

from pathlib import Path
from ai_code_validator.parser import AnnotationParser
from ai_code_validator.reporter import ResultReporter

parser = AnnotationParser()
reporter = ResultReporter()

file_path = Path('tests/invalid_annotations.py')
content = file_path.read_text()
blocks, errors = parser.validate_file(file_path, content)

result = reporter.generate_result(errors, 1)
print(json.dumps(json.loads(reporter.report_json(result)), indent=2))
"
```

---

## VS Code Extension - Manual Testing

### Setup
1. **Navigate to extension directory**:
   ```bash
   cd src/vscode-extension
   npm install
   ```

2. **Open in VS Code**:
   ```bash
   code .
   ```

3. **Launch Debug Extension**:
   - Press **F5** or go to Run → Start Debugging
   - A new VS Code window opens with the extension loaded

### Test 1: Keyboard Shortcut
1. In the debug VS Code window, create a new file (Ctrl+N)
2. Set language to Python (Ctrl+K, M)
3. Paste this code:
   ```python
   def hello():
       return "world"
   ```
4. Select all code (Ctrl+A)
5. Press **Ctrl+Shift+A** (Windows/Linux) or **Cmd+Shift+A** (Mac)
6. Fill in the prompts:
   - AI Tool Name: `GitHub Copilot`
   - Tool Version: `1.0` (optional - just press Enter to skip)
   - Developer ID: `dev-001`
7. Code should be wrapped with annotations!

### Test 2: Auto-Detect on Paste
1. In the debug window, open `tests/valid_annotations.py`
2. Copy the `fibonacci` function (lines 3-9)
3. Create a new Python file
4. Paste the code
5. Extension should ask: "Was this code generated using AI?"
6. Select "Yes" and provide metadata
7. Code gets wrapped automatically!

### Test 3: Manual Command
1. Select code in editor
2. Open Command Palette (Ctrl+Shift+P)
3. Type: `Mark Selected Code as AI-Generated`
4. Select the command
5. Provide metadata in dialogs

---

## Pre-Commit Hook Testing

### Setup
```bash
# Install pre-commit framework
pip install pre-commit

# Navigate to repo root
cd C:\Users\parag\OneDrive\Desktop\code\AI-Annotation

# Install git hooks
pre-commit install
```

### Test
1. Create a test commit with unannotated AI code
2. Try to commit - hook should block it
3. Annotate the code properly
4. Re-commit - should succeed

---

## GitHub Actions Testing

The workflow runs automatically on:
- Push to branches: `main`, `develop`
- Pull requests to branches: `main`, `develop`

To test manually:
```bash
git push origin main
# Check GitHub Actions tab in repository
```

---

## Test Files Provided

Located in `tests/` directory:

1. **valid_annotations.py**
   - 2 valid Python annotation blocks
   - Demonstrates correct format
   - Expected result: ✅ PASS

2. **valid_annotations.js**
   - 2 valid JavaScript annotation blocks
   - Shows JavaScript comment syntax
   - Expected result: ✅ PASS

3. **invalid_annotations.py**
   - 5 invalid annotation blocks with different errors:
     * Missing TOOL_NAME
     * Invalid DATE format
     * Missing AUTHOR_ID
     * Wrong ACTION value
     * Missing END marker
   - Expected result: ❌ FAIL (with detailed errors)

---

## Expected Results

### Python Validator
```
Files: 3 scanned
Valid blocks: 4 found
Errors: 5 detected
Result: FAIL (1 file with errors)
```

### VS Code Extension
- Should prompt for metadata after detecting multi-line insertions
- Should wrap code with proper comment syntax for each language
- Should preserve original code indentation

### Pre-Commit
- Should reject commits with unannotated AI code
- Should allow commits with properly annotated code
- Should allow commits with no AI code

---

## Troubleshooting

### Python Validator Issues
- **ImportError**: Make sure you're in the repo root and using the correct sys.path
- **File not found**: Check file paths are relative to repo root

### VS Code Extension Issues
- **Extension doesn't load**: Check F5 output for errors
- **Command not found**: Close and reopen the debug window (F5)
- **No prompts**: Code might be too short (needs 2+ lines)

### Pre-Commit Issues
- **Hook doesn't run**: Run `pre-commit install` again
- **Need to reinstall validator**: `pip install -e src/python-validator`

---

## Next: Integration Testing

After manual testing, integrate with:
1. Real development workflow
2. Team pre-commit hooks
3. GitHub Actions CI/CD
4. Code review process
