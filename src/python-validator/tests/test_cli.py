"""Tests for the CLI module."""

import tempfile
from pathlib import Path

from ai_code_validator.cli import main


def test_cli_with_valid_annotations(capsys, monkeypatch):
    """Test CLI with valid annotations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create a file with valid annotation
        (tmppath / 'test.py').write_text('''
# START_AI_GENERATED_CODE
# TOOL_NAME: GPT-4
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: user-1
# ACTION: GENERATED
def example():
    pass
# END_AI_GENERATED_CODE
''')

        monkeypatch.setattr('sys.argv', ['cli', '--repo-path', tmpdir])
        result = main()

        captured = capsys.readouterr()
        assert result == 0
        assert '✅' in captured.out or 'valid' in captured.out


def test_cli_with_invalid_annotations(capsys, monkeypatch):
    """Test CLI with invalid annotations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create a file with invalid annotation (missing TOOL_NAME)
        (tmppath / 'test.py').write_text('''
# START_AI_GENERATED_CODE
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: user-1
# ACTION: GENERATED
# END_AI_GENERATED_CODE
''')

        monkeypatch.setattr('sys.argv', ['cli', '--repo-path', tmpdir])
        result = main()

        captured = capsys.readouterr()
        assert result == 1
        assert '❌' in captured.out or 'FAILED' in captured.out or 'error' in captured.out.lower()


def test_cli_json_output(capsys, monkeypatch):
    """Test CLI JSON output format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        (tmppath / 'test.py').write_text('''
# START_AI_GENERATED_CODE
# TOOL_NAME: Copilot
# DATE: 2025-02-15T10:30:00Z
# AUTHOR_ID: user-1
# ACTION: GENERATED
# END_AI_GENERATED_CODE
''')

        monkeypatch.setattr(
            'sys.argv',
            ['cli', '--repo-path', tmpdir, '--output-format', 'json'],
        )
        main()

        captured = capsys.readouterr()
        assert '"valid"' in captured.out
        assert '"errors"' in captured.out
        assert '"summary"' in captured.out


def test_cli_custom_file_patterns(capsys, monkeypatch):
    """Test CLI with custom file patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create different file types
        (tmppath / 'test.py').write_text('# Python')
        (tmppath / 'test.js').write_text('// JavaScript')

        monkeypatch.setattr(
            'sys.argv',
            ['cli', '--repo-path', tmpdir, '--file-patterns', '*.js'],
        )
        result = main()

        captured = capsys.readouterr()
        # Should only scan .js files and find no errors (they don't have annotations)
        assert result == 0
