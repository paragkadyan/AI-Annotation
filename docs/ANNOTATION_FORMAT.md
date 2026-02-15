# AI-Generated Code Annotation Format Specification

This document defines the precise format and requirements for annotating AI-generated code.

## Overview

All AI-generated code **must** be wrapped with mandatory metadata annotations. The annotation format is language-aware and uses appropriate comment syntax for each programming language.

## Annotation Block Structure

```
<OPENING COMMENT> START_AI_GENERATED_CODE
<OPENING COMMENT> TOOL_NAME: <tool name>
<OPENING COMMENT> TOOL_VERSION: <tool version>  [optional]
<OPENING COMMENT> DATE: <ISO 8601 timestamp>
<OPENING COMMENT> AUTHOR_ID: <developer ID>
<OPENING COMMENT> ACTION: GENERATED
<AI-GENERATED CODE HERE>
<OPENING COMMENT> END_AI_GENERATED_CODE
```

## Markers

### Start Marker

```
START_AI_GENERATED_CODE
```

- **Position**: First line of annotation block
- **Format**: Exact string match (case-sensitive)
- **Requirement**: Must appear in a comment line
- **Must be paired with**: `END_AI_GENERATED_CODE`

### End Marker

```
END_AI_GENERATED_CODE
```

- **Position**: Last line of annotation block
- **Format**: Exact string match (case-sensitive)
- **Requirement**: Must appear in a comment line
- **Requirement**: Must match a corresponding START marker

### Balance Requirement

- Every `START_AI_GENERATED_CODE` must have a matching `END_AI_GENERATED_CODE`
- Markers must not be nested
- Multi-block code must have separate start/end pairs
- Blocks may be consecutive

## Metadata Fields

### TOOL_NAME (Required)

**Description**: Name of the AI tool that generated the code

**Format**:
```
TOOL_NAME: <string>
```

**Requirements**:
- Must be present in every annotation block
- Must be non-empty (whitespace-only is invalid)
- Must be on a single line
- Examples: `GitHub Copilot`, `GPT-4`, `Claude`, `Gemini`

**Valid Examples**:
```
# TOOL_NAME: GitHub Copilot
// TOOL_NAME: GPT-4
-- TOOL_NAME: Claude 3 Opus
```

**Invalid Examples**:
```
# TOOL_NAME:           [empty value]
# TOOL_NAME          [missing colon]
# TOOL_NAME      [multiple values on next line]
  VALUE
```

### TOOL_VERSION (Optional)

**Description**: Version of the AI tool used

**Format**:
```
TOOL_VERSION: <version string>
```

**Requirements**:
- May be omitted if not applicable
- If present, must be non-empty
- Should follow semantic versioning (e.g., 1.0.0)
- May be any version format supported by the tool

**Valid Examples**:
```
# TOOL_VERSION: 1.0.0
# TOOL_VERSION: GPT-4 Turbo
// TOOL_VERSION: 2023.12.01
```

**Invalid Examples**:
```
# TOOL_VERSION:        [empty]
# TOOL_VERSION:
```

### DATE (Required)

**Description**: ISO 8601 timestamp of when code was generated

**Format**:
```
DATE: <ISO 8601 timestamp>
```

**Requirements**:
- Must be present in every annotation block
- Must be valid ISO 8601 format
- Must be non-empty
- Timezone is required (Z for UTC, or ±HH:MM offset)

**Valid Formats**:
```
2025-02-15T10:30:00Z
2025-02-15T10:30:00.123Z
2025-02-15T10:30:00+00:00
2025-02-15T10:30:00-05:00
2025-02-15T10:30:00.123456Z
```

**Validator Regex**:
```
\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}
```

**Valid Examples**:
```
# DATE: 2025-02-15T10:30:00Z
// DATE: 2025-02-15T10:30:00+00:00
-- DATE: 2025-02-16T14:45:30Z
```

**Invalid Examples**:
```
# DATE: 2025-02-15           [no time]
# DATE: 02/15/2025           [wrong format]
# DATE: 2025-02-15 10:30     [no T separator, no timezone]
# DATE: Feb 15, 2025         [word format]
```

### AUTHOR_ID (Required)

**Description**: Identifier of the developer who used the AI tool

**Format**:
```
AUTHOR_ID: <identifier>
```

**Requirements**:
- Must be present in every annotation block
- Must be non-empty (whitespace-only is invalid)
- Must be a single value (no spaces unless escaped)
- Should uniquely identify the developer
- Format is flexible - can be username, email, ID number, etc.

**Valid Examples**:
```
# AUTHOR_ID: dev-001
# AUTHOR_ID: john.doe
// AUTHOR_ID: john_doe@company.com
-- AUTHOR_ID: engineer-42
% AUTHOR_ID: user123
```

**Invalid Examples**:
```
# AUTHOR_ID:           [empty]
# AUTHOR_ID:    [whitespace only]
```

### ACTION (Required)

**Description**: Action taken on the code

**Format**:
```
ACTION: GENERATED
```

**Requirements**:
- Must be present in every annotation block
- Must be exactly `GENERATED` (case-sensitive, uppercase)
- No other values are currently allowed
- Future versions may support `MODIFIED`, `REVIEWED`, etc.

**Valid Examples**:
```
# ACTION: GENERATED
// ACTION: GENERATED
-- ACTION: GENERATED
```

**Invalid Examples**:
```
# ACTION: generated           [lowercase]
# ACTION: Generated           [mixed case]
# ACTION: MODIFIED            [not GENERATED]
# ACTION:                     [empty]
```

## Comment Styles

Each language has specific comment syntax. Metadata lines should use the appropriate comment syntax for the language.

### Line Comment Style Languages

These languages use line-comment prefixes:

```python
# Python
# TOOL_NAME: Copilot

// JavaScript
// TOOL_NAME: Copilot

# Ruby
# TOOL_NAME: Copilot

# Shell
# TOOL_NAME: Copilot

-- SQL
-- TOOL_NAME: Copilot

-- Haskell
-- TOOL_NAME: Copilot

% MATLAB
% TOOL_NAME: Copilot
```

### Block Comment Style Languages

These languages support block comments (not required):

```javascript
/* JavaScript/TypeScript - can use line OR block comments */
// TOOL_NAME: Copilot
// TOOL_VERSION: 1.0
// DATE: 2025-02-15T10:30:00Z
// AUTHOR_ID: dev-001
// ACTION: GENERATED
```

## Code Block Requirements

### Indentation

Original code indentation must be preserved:

```python
# START_AI_GENERATED_CODE
# TOOL_NAME: Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def function_name():
    if condition:
        do_something()
# END_AI_GENERATED_CODE
```

When code is inside other structures, maintain relative indentation:

```python
class MyClass:
    # START_AI_GENERATED_CODE
    # TOOL_NAME: Copilot
    # DATE: 2025-02-15T10:30:00Z
    # AUTHOR_ID: dev-001
    # ACTION: GENERATED
    def method(self):
        return "generated"
    # END_AI_GENERATED_CODE
```

### Empty Lines

Blank lines within the code block are preserved:

```python
# START_AI_GENERATED_CODE
# TOOL_NAME: Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def function():
    x = 1

    y = 2
    return x + y
# END_AI_GENERATED_CODE
```

## Complete Examples

### Python

```python
# START_AI_GENERATED_CODE
# TOOL_NAME: GitHub Copilot
# TOOL_VERSION: 1.0
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: john.doe
# ACTION: GENERATED
def fibonacci(n):
    """Calculate fibonacci sequence."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
# END_AI_GENERATED_CODE
```

### JavaScript

```javascript
// START_AI_GENERATED_CODE
// TOOL_NAME: GitHub Copilot
// TOOL_VERSION: 1.0
// DATE: 2025-02-15T10:30:00Z
// AUTHOR_ID: jane.smith
// ACTION: GENERATED
function sortArray(arr) {
  return arr.sort((a, b) => a - b);
}
// END_AI_GENERATED_CODE
```

### TypeScript

```typescript
// START_AI_GENERATED_CODE
// TOOL_NAME: GPT-4
// TOOL_VERSION: 4.0
// DATE: 2025-02-15T10:30:00Z
// AUTHOR_ID: dev-engineer
// ACTION: GENERATED
interface User {
  id: number;
  name: string;
  email: string;
}
// END_AI_GENERATED_CODE
```

### Java

```java
// START_AI_GENERATED_CODE
// TOOL_NAME: Copilot
// DATE: 2025-02-15T10:30:00Z
// AUTHOR_ID: java-dev-001
// ACTION: GENERATED
public class Calculator {
    public static int add(int a, int b) {
        return a + b;
    }
}
// END_AI_GENERATED_CODE
```

### SQL

```sql
-- START_AI_GENERATED_CODE
-- TOOL_NAME: Claude
-- DATE: 2025-02-15T10:30:00Z
-- AUTHOR_ID: data-engineer
-- ACTION: GENERATED
SELECT id, name, email
FROM users
WHERE created_at > '2025-01-01';
-- END_AI_GENERATED_CODE
```

## Multiple Blocks in One File

Different parts of code can be from different sources:

```python
def manually_written_function():
    return "manual"

# START_AI_GENERATED_CODE
# TOOL_NAME: GitHub Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def ai_generated_function():
    return "generated by AI"
# END_AI_GENERATED_CODE

def another_manual_function():
    return "also manual"

# START_AI_GENERATED_CODE
# TOOL_NAME: GPT-4
# DATE: 2025-02-15T10:35:00Z
# AUTHOR_ID: dev-002
# ACTION: GENERATED
def another_ai_function():
    return "different AI tool"
# END_AI_GENERATED_CODE
```

## Validation Rules

### Syntax Validation

1. ✅ Both START and END markers must be present
2. ✅ Markers must be in comment lines
3. ✅ All required metadata fields present
4. ✅ All non-empty fields validated
5. ✅ No mixing of metadata fields (each on one line)

### Semantic Validation

1. ✅ TOOL_NAME is non-empty string
2. ✅ TOOL_VERSION is non-empty string (if present)
3. ✅ DATE is valid ISO 8601
4. ✅ AUTHOR_ID is non-empty string
5. ✅ ACTION equals "GENERATED"
6. ✅ No nested annotation blocks

### Metadata Field Order

Fields are order-independent. Valid:

```
# TOOL_NAME: Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED

# or

# ACTION: GENERATED
# AUTHOR_ID: dev-001
# DATE: 2025-02-15T10:30:00Z
# TOOL_NAME: Copilot
```

## Anti-Patterns

### ❌ Don't Do This

**Missing markers:**
```python
# TOOL_NAME: Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def function():
    pass
# [Missing START and END markers]
```

**Empty metadata:**
```python
# START_AI_GENERATED_CODE
# TOOL_NAME:              [❌ empty]
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def function():
    pass
# END_AI_GENERATED_CODE
```

**Invalid date format:**
```python
# START_AI_GENERATED_CODE
# TOOL_NAME: Copilot
# DATE: 02/15/2025              [❌ wrong format]
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def function():
    pass
# END_AI_GENERATED_CODE
```

**Wrong action:**
```python
# START_AI_GENERATED_CODE
# TOOL_NAME: Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: MODIFIED               [❌ should be GENERATED]
def function():
    pass
# END_AI_GENERATED_CODE
```

## Future Considerations

- Additional ACTION values: `MODIFIED` (for AI-refined code)
- Nested blocks support potentially in future versions
- Custom metadata fields via configuration
- Annotation templates with defaults
