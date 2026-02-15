"""File scanner for discovering code files in repositories."""

from pathlib import Path
from typing import Generator

from .config import Config


class FileScanner:
    """Scans repository for code files matching configured patterns."""

    def __init__(self, config: Config):
        """Initialize scanner with configuration.

        Args:
            config: Configuration object with paths and patterns
        """
        self.config = config

    def scan(self) -> Generator[tuple[Path, str], None, None]:
        """Scan repository and yield (file_path, content) tuples.

        Yields:
            Tuples of (absolute_file_path, file_content)
        """
        if not self.config.repo_path.exists():
            raise FileNotFoundError(f"Repository path not found: {self.config.repo_path}")

        for file_path in self._discover_files():
            try:
                content = file_path.read_text(encoding='utf-8')
                yield file_path, content
            except (UnicodeDecodeError, PermissionError) as e:
                if self.config.verbose:
                    print(f"Warning: Could not read file {file_path}: {e}")
                continue

    def _discover_files(self) -> Generator[Path, None, None]:
        """Discover all code files in repository matching patterns.

        Yields:
            Absolute file paths matching configured patterns
        """
        for path in self.config.repo_path.rglob('*'):
            # Skip excluded paths
            if self.config.should_exclude_path(path):
                continue

            # Only process files, not directories
            if not path.is_file():
                continue

            # Check if file matches any pattern
            if self._matches_patterns(path):
                yield path

    def _matches_patterns(self, file_path: Path) -> bool:
        """Check if file path matches any configured pattern.

        Args:
            file_path: Path to check

        Returns:
            True if file matches any pattern
        """
        name = file_path.name
        for pattern in self.config.file_patterns:
            if self._simple_match(name, pattern):
                return True
        return False

    @staticmethod
    def _simple_match(filename: str, pattern: str) -> bool:
        """Simple glob-style pattern matching.

        Args:
            filename: File name to match
            pattern: Pattern (e.g., '*.py')

        Returns:
            True if filename matches pattern
        """
        # Convert simple glob patterns to match
        if pattern == '*':
            return True

        if pattern.startswith('*.'):
            # Pattern like '*.py'
            extension = pattern[2:]
            return filename.endswith(f'.{extension}')

        # Exact match
        return filename == pattern
