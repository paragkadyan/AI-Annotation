# Getting Started - First Steps

Welcome to the AI Code Annotator system! Here's what to do right now.

---

## 📖 Read These First (5 minutes)

1. **README.md** - Understand the system
2. **QUICK_REFERENCE.md** - See the annotation format
3. **IMPLEMENTATION_SUMMARY.md** - Know what you got

---

## 🚀 Test It Right Now (15 minutes)

### Open a terminal in the repo root:

```bash
cd c:\Users\parag\OneDrive\Desktop\code\AI-Annotation
```

### Test Python Validator

```bash
python -c "
import sys
sys.path.insert(0, 'src/python-validator/src')

from pathlib import Path
from ai_code_validator.parser import AnnotationParser
from ai_code_validator.reporter import ResultReporter

parser = AnnotationParser()
reporter = ResultReporter()

# Test valid file
file_path = Path('tests/valid_annotations.py')
content = file_path.read_text()
blocks, errors = parser.validate_file(file_path, content)

print(f'Valid Python annotations: {len(blocks)} blocks found')
print(f'Errors: {len(errors)}')
print()

# Test invalid file
file_path = Path('tests/invalid_annotations.py')
content = file_path.read_text()
blocks, errors = parser.validate_file(file_path, content)

print(f'Invalid Python annotations: {len(errors)} errors detected')
for err in errors[:3]:
    print(f'  - Line {err.line_number}: {err.message}')
"
```

### Expected Output
```
Valid Python annotations: 2 blocks found
Errors: 0

Invalid Python annotations: 5 errors detected
  - Line 1: Missing or empty required field: TOOL_NAME
  - Line 11: Invalid DATE format: 2025/02/15 (expected ISO 8601)
  - Line 21: Missing or empty required field: AUTHOR_ID
```

✅ **System is working!**

---

## 🔧 Install Components

### Install Python Validator

```bash
cd src/python-validator
pip install -e .
```

Test it:
```bash
ai-code-validator --help
```

### Load VS Code Extension

1. Open VS Code
2. Open folder: `src/vscode-extension`
3. Press **F5** to launch debug extension
4. A new VS Code window opens with extension loaded
5. Try the keyboard shortcut:
   - Select some code
   - Press **Ctrl+Shift+A** (Windows/Linux) or **Cmd+Shift+A** (Mac)
   - Fill in the prompts
   - Code gets wrapped! ✅

### Install Pre-Commit Hook

```bash
pip install pre-commit
pre-commit install
```

Test it:
```bash
pre-commit run --all-files
```

---

## 📚 Next: Read Documentation

Once you've seen it working, read these in order:

1. **TESTING_GUIDE.md** - Detailed testing procedures
2. **docs/ANNOTATION_FORMAT.md** - Understand the annotation format
3. **docs/ARCHITECTURE.md** - How the system works
4. **CONTRIBUTING.md** - Development guidelines

---

## 💡 Key Files to Know

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `QUICK_REFERENCE.md` | Developer cheat sheet |
| `TESTING_GUIDE.md` | How to test everything |
| `TEST_RESULTS.md` | Test validation report |
| `docs/ANNOTATION_FORMAT.md` | Format specification |
| `DELIVERY_MANIFEST.md` | Complete file inventory |

---

## ❓ Common Questions

**Q: How do I annotate code in VS Code?**

A:
1. Press Ctrl+Shift+A (Windows/Linux) or Cmd+Shift+A (Mac)
2. Or paste code → extension asks if it's AI-generated
3. Provide: Tool name, optional version, your ID
4. Code gets wrapped automatically

**Q: How do I validate a repo?**

A:
```bash
ai-code-validator --repo-path /path/to/repo
```

**Q: What's the annotation format?**

A: See `QUICK_REFERENCE.md` or `docs/ANNOTATION_FORMAT.md`

**Q: How does pre-commit work?**

A: It runs automatically before commits and rejects unannotated AI code

---

## 🎯 Your Next 30 Minutes

- [ ] Read README.md (5 min)
- [ ] Run the Python validator test (5 min)
- [ ] Load VS Code extension and press F5 (5 min)
- [ ] Test annotation on sample code (10 min)
- [ ] Install pre-commit hook (5 min)

---

## 🚨 If Something Doesn't Work

1. Check **TESTING_GUIDE.md** → Troubleshooting section
2. Check file paths are correct
3. Make sure Python 3.11+ installed: `python --version`
4. Make sure VS Code 1.85+: Check Help → About

---

## 📞 Need Help?

- Extension not loading? → Check VS Code output panel (Ctrl+`)
- Validator errors? → Add `--verbose` flag
- Date parsing issues? → Use ISO 8601: `2025-02-15T10:30:00Z`
- Pre-commit problems? → Run `pre-commit install` again

---

## ✅ You're Ready!

The system is production-ready. Start using it:

1. ✅ Install validator + extension
2. ✅ Test with sample files
3. ✅ Set up pre-commit hook
4. ✅ Configure VS Code settings
5. ✅ Start annotating AI code

**That's it!** The rest is documented in the files above.

---

Last Updated: 2025-02-15
