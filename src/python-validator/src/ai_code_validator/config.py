"""Configuration management for the AI Code Validator."""

import os
from pathlib import Path
from typing import Set

DEFAULT_FILE_PATTERNS = [
    '*.py',
    '*.js',
    '*.jsx',
    '*.ts',
    '*.tsx',
    '*.java',
    '*.cpp',
    '*.c',
    '*.h',
    '*.hpp',
    '*.cs',
    '*.go',
    '*.rb',
    '*.php',
    '*.swift',
    '*.kt',
]

DEFAULT_EXCLUDE_PATTERNS = [
    '.git',
    '.gitignore',
    '__pycache__',
    'node_modules',
    '.venv',
    'venv',
    'env',
    'build',
    'dist',
    '.egg-info',
    'out',
    '.vscode',
    '.idea',
]


class Config:
    """Configuration holder for validator settings."""

    def __init__(
        self,
        repo_path: str = '.',
        file_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize configuration.

        Args:
            repo_path: Root repository path to scan
            file_patterns: File patterns to include (e.g., ['*.py', '*.js'])
            exclude_patterns: Directory/file patterns to exclude
            verbose: Enable verbose output
        """
        self.repo_path = Path(repo_path).resolve()
        self.file_patterns = file_patterns or DEFAULT_FILE_PATTERNS
        self.exclude_patterns = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS
        self.verbose = verbose

    @classmethod
    def from_cli_args(cls, args) -> 'Config':
        """Create Config from CLI arguments."""
        file_patterns = None
        if args.file_patterns:
            file_patterns = [p.strip() for p in args.file_patterns.split(',')]

        exclude_patterns = None
        if args.exclude_patterns:
            exclude_patterns = [p.strip() for p in args.exclude_patterns.split(',')]

        return cls(
            repo_path=args.repo_path,
            file_patterns=file_patterns,
            exclude_patterns=exclude_patterns,
            verbose=args.verbose,
        )

    def should_exclude_path(self, path: Path) -> bool:
        """Check if a path should be excluded from scanning."""
        parts = path.parts
        for pattern in self.exclude_patterns:
            if pattern in parts:
                return True
        return False
