"""Reporter for validation results in multiple formats."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from .parser import AnnotationError


@dataclass
class ValidationResult:
    """Overall validation result."""

    valid: bool
    errors: list[dict]
    summary: dict


class ResultReporter:
    """Generates validation reports in different formats."""

    def __init__(self, verbose: bool = False):
        """Initialize reporter.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose

    def generate_result(
        self,
        errors: list[AnnotationError],
        total_files_scanned: int,
    ) -> ValidationResult:
        """Generate validation result.

        Args:
            errors: List of validation errors
            total_files_scanned: Total number of files scanned

        Returns:
            ValidationResult object
        """
        is_valid = len(errors) == 0

        error_dicts = [
            {
                'file': str(error.file_path),
                'line': error.line_number,
                'message': error.message,
            }
            for error in errors
        ]

        # Count unique files with errors
        files_with_errors = len(set(error.file_path for error in errors))

        summary = {
            'total_files': total_files_scanned,
            'files_with_errors': files_with_errors,
            'total_errors': len(errors),
        }

        return ValidationResult(
            valid=is_valid,
            errors=error_dicts,
            summary=summary,
        )

    def report_json(self, result: ValidationResult) -> str:
        """Format result as JSON.

        Args:
            result: ValidationResult object

        Returns:
            JSON string
        """
        return json.dumps(
            {
                'valid': result.valid,
                'errors': result.errors,
                'summary': result.summary,
            },
            indent=2,
        )

    def report_text(self, result: ValidationResult) -> str:
        """Format result as human-readable text.

        Args:
            result: ValidationResult object

        Returns:
            Formatted text report
        """
        lines = []

        if result.valid:
            lines.append('✅ All AI code annotations are valid!')
        else:
            lines.append('❌ AI code annotation validation FAILED')

        lines.append('')
        lines.append(f"Summary:")
        lines.append(f"  Total files scanned: {result.summary['total_files']}")
        lines.append(f"  Files with errors: {result.summary['files_with_errors']}")
        lines.append(f"  Total errors: {result.summary['total_errors']}")

        if result.errors:
            lines.append('')
            lines.append('Errors:')
            for error in result.errors:
                lines.append(f"  {error['file']}:{error['line']}")
                lines.append(f"    → {error['message']}")

        return '\n'.join(lines)

    def print_result(self, result: ValidationResult, format: str = 'text') -> None:
        """Print result to stdout.

        Args:
            result: ValidationResult object
            format: Output format ('json' or 'text')
        """
        if format == 'json':
            print(self.report_json(result))
        else:
            print(self.report_text(result))
