"""CLI entry point for the AI Code Validator."""

import argparse
import sys
from pathlib import Path

from .config import Config, DEFAULT_EXCLUDE_PATTERNS, DEFAULT_FILE_PATTERNS
from .parser import AnnotationParser
from .reporter import ResultReporter
from .scanner import FileScanner


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Validate AI-generated code annotations in a repository',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Validate current directory
  python -m ai_code_validator

  # Validate specific path
  python -m ai_code_validator --repo-path /path/to/repo

  # Output as JSON
  python -m ai_code_validator --output-format json

  # Custom file patterns
  python -m ai_code_validator --file-patterns "*.py,*.js,*.ts"

  # Exclude patterns
  python -m ai_code_validator --exclude-patterns "build,dist,.git"
        ''',
    )

    parser.add_argument(
        '--repo-path',
        default='.',
        help='Root path of repository to scan (default: current directory)',
    )

    parser.add_argument(
        '--output-format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)',
    )

    parser.add_argument(
        '--file-patterns',
        help='Comma-separated file patterns to scan (default: *.py,*.js,*.ts,...)',
        default=None,
    )

    parser.add_argument(
        '--exclude-patterns',
        help='Comma-separated patterns to exclude (default: .git,__pycache__,node_modules,...)',
        default=None,
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output',
    )

    args = parser.parse_args()

    # Create configuration
    config = Config.from_cli_args(args)

    if config.verbose:
        print(f'Scanning repository: {config.repo_path}', file=sys.stderr)
        print(f'File patterns: {", ".join(config.file_patterns)}', file=sys.stderr)
        print(f'Excluded patterns: {", ".join(config.exclude_patterns)}', file=sys.stderr)
        print('', file=sys.stderr)

    # Scan files
    scanner = FileScanner(config)
    parser_instance = AnnotationParser()
    reporter = ResultReporter(verbose=config.verbose)

    try:
        files_scanned = 0
        all_errors = []

        for file_path, content in scanner.scan():
            files_scanned += 1
            _, errors = parser_instance.validate_file(file_path, content)
            all_errors.extend(errors)

            if config.verbose and errors:
                print(f'Errors in {file_path}:', file=sys.stderr)
                for error in errors:
                    print(f'  Line {error.line_number}: {error.message}', file=sys.stderr)

        # Generate and print result
        result = reporter.generate_result(all_errors, files_scanned)
        reporter.print_result(result, format=args.output_format)

        # Exit with appropriate code
        return 0 if result.valid else 1

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        if config.verbose:
            import traceback
            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
