# START_AI_GENERATED_CODE
# TOOL_NAME: GitHub Copilot
# TOOL_VERSION: 1.0
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def fibonacci(n):
    """Calculate fibonacci sequence."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
# END_AI_GENERATED_CODE


def manually_written_function():
    """This function was written manually, not annotated."""
    return "manual code"


# START_AI_GENERATED_CODE
# TOOL_NAME: GPT-4
# DATE: 2025-02-16T14:45:30Z
# AUTHOR_ID: jane.smith
# ACTION: GENERATED
def sort_custom(items):
    """Sort items by custom logic."""
    return sorted(items, key=lambda x: x['priority'])
# END_AI_GENERATED_CODE
