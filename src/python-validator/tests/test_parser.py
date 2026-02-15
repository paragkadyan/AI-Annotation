"""Tests for the annotation parser module."""

from pathlib import Path

from ai_code_validator.parser import AnnotationParser


def test_parse_valid_annotation_block():
    """Test parsing a valid annotation block."""
    content = '''
# START_AI_GENERATED_CODE
# TOOL_NAME: GitHub Copilot
# TOOL_VERSION: 1.0
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: dev-001
# ACTION: GENERATED
def example():
    pass
# END_AI_GENERATED_CODE
'''
    parser = AnnotationParser()
    blocks, errors = parser.validate_file(Path('test.py'), content)

    assert len(errors) == 0
    assert len(blocks) == 1
    assert blocks[0].tool_name == 'GitHub Copilot'
    assert blocks[0].author_id == 'dev-001'
    assert blocks[0].action == 'GENERATED'


def test_parse_missing_end_marker():
    """Test error when END marker is missing."""
    content = '''
# START_AI_GENERATED_CODE
# TOOL_NAME: GPT-4
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: user-123
# ACTION: GENERATED
def incomplete():
    pass
'''
    parser = AnnotationParser()
    blocks, errors = parser.validate_file(Path('test.py'), content)

    assert len(blocks) == 0
    assert len(errors) == 1
    assert 'no matching END_AI_GENERATED_CODE' in errors[0].message


def test_parse_missing_required_fields():
    """Test error when required metadata fields are missing."""
    content = '''
# START_AI_GENERATED_CODE
# TOOL_NAME: Claude
# END_AI_GENERATED_CODE
'''
    parser = AnnotationParser()
    blocks, errors = parser.validate_file(Path('test.py'), content)

    assert len(blocks) == 0
    assert len(errors) > 0
    # Should complain about missing DATE and AUTHOR_ID
    assert any('DATE' in e.message for e in errors)


def test_parse_invalid_date_format():
    """Test error when DATE format is invalid."""
    content = '''
# START_AI_GENERATED_CODE
# TOOL_NAME: GPT
# DATE: 2025/02/15
# AUTHOR_ID: user-1
# ACTION: GENERATED
# END_AI_GENERATED_CODE
'''
    parser = AnnotationParser()
    blocks, errors = parser.validate_file(Path('test.py'), content)

    assert len(blocks) == 0
    assert any('DATE' in e.message and 'Invalid' in e.message for e in errors)


def test_parse_invalid_action():
    """Test error when ACTION is not GENERATED."""
    content = '''
# START_AI_GENERATED_CODE
# TOOL_NAME: Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: user-1
# ACTION: MODIFIED
# END_AI_GENERATED_CODE
'''
    parser = AnnotationParser()
    blocks, errors = parser.validate_file(Path('test.py'), content)

    assert len(blocks) == 0
    assert any('ACTION' in e.message for e in errors)


def test_parse_multiple_blocks():
    """Test parsing multiple annotation blocks in one file."""
    content = '''
# START_AI_GENERATED_CODE
# TOOL_NAME: Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: user-1
# ACTION: GENERATED
def func1():
    pass
# END_AI_GENERATED_CODE

# Some manual code

# START_AI_GENERATED_CODE
# TOOL_NAME: GPT-4
# DATE: 2025-02-16T10:30:00Z
# AUTHOR_ID: user-2
# ACTION: GENERATED
def func2():
    pass
# END_AI_GENERATED_CODE
'''
    parser = AnnotationParser()
    blocks, errors = parser.validate_file(Path('test.py'), content)

    assert len(errors) == 0
    assert len(blocks) == 2
    assert blocks[0].tool_name == 'Copilot'
    assert blocks[1].tool_name == 'GPT-4'
