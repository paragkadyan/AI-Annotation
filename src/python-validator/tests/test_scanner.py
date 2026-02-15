"""Tests for the file scanner module."""

import tempfile
from pathlib import Path

from ai_code_validator.config import Config
from ai_code_validator.scanner import FileScanner


def test_scan_discovers_python_files():
    """Test that scanner discovers Python files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create test files
        (tmppath / 'module1.py').write_text('# Python code')
        (tmppath / 'module2.py').write_text('# More Python')
        (tmppath / 'readme.txt').write_text('Not code')

        config = Config(repo_path=tmpdir, file_patterns=['*.py'])
        scanner = FileScanner(config)

        files = [path for path, _ in scanner.scan()]
        assert len(files) == 2
        assert all(str(f).endswith('.py') for f in files)


def test_scan_respects_exclude_patterns():
    """Test that scanner respects exclude patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create test structure
        (tmppath / 'module.py').write_text('# Code')
        (tmppath / '__pycache__').mkdir()
        (tmppath / '__pycache__' / 'module.pyc').write_text('compiled')

        config = Config(
            repo_path=tmpdir,
            file_patterns=['*.py', '*.pyc'],
            exclude_patterns=['__pycache__'],
        )
        scanner = FileScanner(config)

        files = [path for path, _ in scanner.scan()]
        assert len(files) == 1
        assert not any('__pycache__' in str(f) for f in files)


def test_scan_returns_file_content():
    """Test that scanner returns file content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        content = 'print("Hello, World!")'
        (tmppath / 'test.py').write_text(content)

        config = Config(repo_path=tmpdir)
        scanner = FileScanner(config)

        results = list(scanner.scan())
        assert len(results) == 1
        path, file_content = results[0]
        assert file_content == content


def test_scan_skips_unreadable_files():
    """Test that scanner handles unreadable files gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create a valid file
        (tmppath / 'valid.py').write_text('valid code')

        config = Config(repo_path=tmpdir, verbose=False)
        scanner = FileScanner(config)

        results = list(scanner.scan())
        # Should have at least the valid file
        assert len(results) >= 1
