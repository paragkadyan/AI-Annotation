/**
 * Handles wrapping code blocks with AI-generated annotations.
 */

import * as vscode from 'vscode';
import { AnnotationMetadata, CommentStyle, LANGUAGE_COMMENT_STYLES } from './types';

export class AnnotationHandler {
  /**
   * Wrap selected code with annotation markers.
   */
  static wrapWithAnnotation(
    editor: vscode.TextEditor,
    metadata: AnnotationMetadata
  ): void {
    const selection = editor.selection;
    const selectedText = editor.document.getText(selection);

    if (!selectedText.trim()) {
      vscode.window.showErrorMessage('No code selected. Please select code to annotate.');
      return;
    }

    const languageId = editor.document.languageId;
    const commentStyle = this.getCommentStyle(languageId);

    if (!commentStyle) {
      vscode.window.showErrorMessage(
        `Language "${languageId}" is not currently supported for auto-annotation.`
      );
      return;
    }

    const annotation = this.generateAnnotation(selectedText, metadata, commentStyle);

    editor.edit((editBuilder) => {
      editBuilder.replace(selection, annotation);
    });

    vscode.window.showInformationMessage('Code annotated successfully!');
  }

  /**
   * Generate the complete annotation block with metadata.
   */
  private static generateAnnotation(
    code: string,
    metadata: AnnotationMetadata,
    commentStyle: CommentStyle
  ): string {
    const prefix = commentStyle.lineComment || '/*';
    const lines: string[] = [];

    // Determine indentation from first line of code
    const firstLine = code.split('\n')[0];
    const indent = this.getLeadingWhitespace(firstLine);

    // Start marker
    lines.push(`${indent}${prefix} START_AI_GENERATED_CODE`);

    // Metadata
    lines.push(`${indent}${prefix} TOOL_NAME: ${metadata.toolName}`);

    if (metadata.toolVersion) {
      lines.push(`${indent}${prefix} TOOL_VERSION: ${metadata.toolVersion}`);
    }

    lines.push(`${indent}${prefix} DATE: ${metadata.date}`);
    lines.push(`${indent}${prefix} AUTHOR_ID: ${metadata.authorId}`);
    lines.push(`${indent}${prefix} ACTION: ${metadata.action}`);

    // Code block
    lines.push(code);

    // End marker
    lines.push(`${indent}${prefix} END_AI_GENERATED_CODE`);

    return lines.join('\n');
  }

  /**
   * Get the comment style for a given language.
   */
  private static getCommentStyle(languageId: string): CommentStyle | undefined {
    return LANGUAGE_COMMENT_STYLES[languageId];
  }

  /**
   * Extract leading whitespace from a line for indentation preservation.
   */
  private static getLeadingWhitespace(line: string): string {
    const match = line.match(/^(\s*)/);
    return match ? match[1] : '';
  }

  /**
   * Validate that all required metadata fields are present and non-empty.
   */
  static validateMetadata(metadata: AnnotationMetadata): string[] {
    const errors: string[] = [];

    if (!metadata.toolName || !metadata.toolName.trim()) {
      errors.push('Tool name is required');
    }

    if (!metadata.authorId || !metadata.authorId.trim()) {
      errors.push('Author ID is required');
    }

    if (!metadata.date || !metadata.date.trim()) {
      errors.push('Date is required');
    }

    if (!this.isValidIsoDate(metadata.date)) {
      errors.push('Date must be in ISO 8601 format');
    }

    if (metadata.action !== 'GENERATED') {
      errors.push('Action must be set to GENERATED');
    }

    return errors;
  }

  /**
   * Check if a string is a valid ISO 8601 date.
   */
  private static isValidIsoDate(dateString: string): boolean {
    try {
      const date = new Date(dateString);
      // Check if valid date and matches ISO format
      return !isNaN(date.getTime()) && dateString.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
    } catch {
      return false;
    }
  }
}
