"""Tests for the result reporter module."""

from pathlib import Path

from ai_code_validator.parser import AnnotationError
from ai_code_validator.reporter import ResultReporter


def test_generate_valid_result():
    """Test generating a valid result."""
    errors = []
    reporter = ResultReporter()
    result = reporter.generate_result(errors, total_files_scanned=5)

    assert result.valid is True
    assert len(result.errors) == 0
    assert result.summary['total_files'] == 5
    assert result.summary['files_with_errors'] == 0


def test_generate_invalid_result():
    """Test generating an invalid result with errors."""
    errors = [
        AnnotationError(
            file_path=Path('file1.py'),
            line_number=10,
            message='Missing field',
        ),
        AnnotationError(
            file_path=Path('file2.py'),
            line_number=20,
            message='Invalid format',
        ),
    ]
    reporter = ResultReporter()
    result = reporter.generate_result(errors, total_files_scanned=10)

    assert result.valid is False
    assert len(result.errors) == 2
    assert result.summary['total_files'] == 10
    assert result.summary['files_with_errors'] == 2
    assert result.summary['total_errors'] == 2


def test_report_json_format():
    """Test JSON report format."""
    errors = [
        AnnotationError(
            file_path=Path('test.py'),
            line_number=5,
            message='Missing TOOL_NAME',
        ),
    ]
    reporter = ResultReporter()
    result = reporter.generate_result(errors, total_files_scanned=1)
    json_output = reporter.report_json(result)

    assert '"valid": false' in json_output
    assert '"errors"' in json_output
    assert 'test.py' in json_output
    assert 'Missing TOOL_NAME' in json_output


def test_report_text_format():
    """Test text report format."""
    errors = [
        AnnotationError(
            file_path=Path('test.py'),
            line_number=5,
            message='Invalid format',
        ),
    ]
    reporter = ResultReporter()
    result = reporter.generate_result(errors, total_files_scanned=1)
    text_output = reporter.report_text(result)

    assert '❌' in text_output
    assert 'test.py' in text_output
    assert 'Invalid format' in text_output
    assert 'Files with errors: 1' in text_output


def test_report_valid_result_text():
    """Test text report for valid result."""
    reporter = ResultReporter()
    result = reporter.generate_result([], total_files_scanned=5)
    text_output = reporter.report_text(result)

    assert '✅' in text_output
    assert 'valid' in text_output
    assert 'Total files scanned: 5' in text_output
