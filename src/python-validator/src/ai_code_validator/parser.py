"""Parser and validator for AI-generated code annotations."""

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class AnnotationError:
    """Represents a validation error in an annotation block."""

    file_path: Path
    line_number: int
    message: str


@dataclass
class AnnotationBlock:
    """Represents a valid AI-generated code annotation block."""

    file_path: Path
    start_line: int
    end_line: int
    tool_name: str
    tool_version: Optional[str]
    date: str
    author_id: str
    action: str


class AnnotationParser:
    """Parses and validates AI-generated code annotation blocks."""

    START_MARKER = 'START_AI_GENERATED_CODE'
    END_MARKER = 'END_AI_GENERATED_CODE'

    # Metadata field patterns
    METADATA_PATTERN = re.compile(r'^\s*(?:#|//|--|\*)??\s*(\w+):\s*(.+?)\s*$')

    def __init__(self):
        """Initialize parser."""
        pass

    def validate_file(self, file_path: Path, content: str) -> tuple[list[AnnotationBlock], list[AnnotationError]]:
        """Validate all annotation blocks in a file.

        Args:
            file_path: Path to file being validated
            content: File content

        Returns:
            Tuple of (valid_blocks, errors)
        """
        blocks = []
        errors = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]

            # Look for start marker
            if self.START_MARKER in line:
                start_line = i + 1  # Line numbers are 1-indexed
                # Find end marker
                end_line = None
                metadata = {}

                j = i + 1
                while j < len(lines):
                    content_line = lines[j]

                    if self.END_MARKER in content_line:
                        end_line = j + 1
                        break

                    # Try to parse metadata lines
                    match = self.METADATA_PATTERN.match(content_line)
                    if match:
                        key, value = match.groups()
                        metadata[key] = value.strip()

                    j += 1

                # Validate the block
                if end_line is None:
                    errors.append(AnnotationError(
                        file_path=file_path,
                        line_number=start_line,
                        message='START_AI_GENERATED_CODE marker found but no matching END_AI_GENERATED_CODE',
                    ))
                else:
                    block_errors = self._validate_block(
                        file_path, start_line, end_line, metadata
                    )
                    if block_errors:
                        errors.extend(block_errors)
                    else:
                        block = AnnotationBlock(
                            file_path=file_path,
                            start_line=start_line,
                            end_line=end_line,
                            tool_name=metadata.get('TOOL_NAME', ''),
                            tool_version=metadata.get('TOOL_VERSION'),
                            date=metadata.get('DATE', ''),
                            author_id=metadata.get('AUTHOR_ID', ''),
                            action=metadata.get('ACTION', ''),
                        )
                        blocks.append(block)

                i = end_line if end_line else j
            else:
                i += 1

        return blocks, errors

    def _validate_block(
        self, file_path: Path, start_line: int, end_line: int, metadata: dict
    ) -> list[AnnotationError]:
        """Validate a single annotation block.

        Args:
            file_path: Path to file
            start_line: Line number of START marker
            end_line: Line number of END marker
            metadata: Extracted metadata dictionary

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check required fields
        required_fields = ['TOOL_NAME', 'DATE', 'AUTHOR_ID', 'ACTION']
        for field in required_fields:
            if field not in metadata or not metadata[field].strip():
                errors.append(AnnotationError(
                    file_path=file_path,
                    line_number=start_line,
                    message=f'Missing or empty required field: {field}',
                ))

        # Validate DATE format (ISO 8601)
        if 'DATE' in metadata and metadata['DATE'].strip():
            if not self._is_valid_iso_date(metadata['DATE'].strip()):
                errors.append(AnnotationError(
                    file_path=file_path,
                    line_number=start_line,
                    message=f'Invalid DATE format: {metadata["DATE"]} (expected ISO 8601)',
                ))

        # Validate ACTION field
        if 'ACTION' in metadata and metadata['ACTION'].strip():
            if metadata['ACTION'].strip() != 'GENERATED':
                errors.append(AnnotationError(
                    file_path=file_path,
                    line_number=start_line,
                    message=f'Invalid ACTION value: {metadata["ACTION"]} (expected GENERATED)',
                ))

        # Validate AUTHOR_ID is not empty
        if 'AUTHOR_ID' in metadata:
            if not metadata['AUTHOR_ID'].strip():
                errors.append(AnnotationError(
                    file_path=file_path,
                    line_number=start_line,
                    message='AUTHOR_ID cannot be empty',
                ))

        return errors

    @staticmethod
    def _is_valid_iso_date(date_str: str) -> bool:
        """Check if a string is a valid ISO 8601 date.

        Args:
            date_str: Date string to validate

        Returns:
            True if valid ISO 8601 format
        """
        try:
            # Try parsing common ISO 8601 formats
            datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
