/**
 * Listens for code insertions in the editor and prompts for AI annotation.
 */

import * as vscode from 'vscode';

export class EditorListener {
  private static debounceTimer: NodeJS.Timeout | null = null;
  private static lastInsertions: Map<string, { range: vscode.Range; content: string }> = new Map();
  private static readonly MIN_LINES_THRESHOLD = 1; // Minimum lines to trigger prompt
  private static readonly DEBOUNCE_DELAY = 500; // Milliseconds

  /**
   * Register the listener for text insertions.
   */
  static register(
    onTextInsert: (
      editor: vscode.TextEditor,
      range: vscode.Range,
      content: string
    ) => Promise<void>
  ): vscode.Disposable {
    return vscode.workspace.onDidChangeTextDocument(async (event) => {
      const editor = vscode.window.activeTextEditor;

      if (!editor || editor.document !== event.document) {
        return;
      }

      // Debounce to avoid triggering on every keystroke
      if (this.debounceTimer) {
        clearTimeout(this.debounceTimer);
      }

      this.debounceTimer = setTimeout(() => {
        this.processChanges(event, editor, onTextInsert);
      }, this.DEBOUNCE_DELAY);
    });
  }

  /**
   * Process text document changes.
   */
  private static async processChanges(
    event: vscode.TextDocumentChangeEvent,
    editor: vscode.TextEditor,
    onTextInsert: (
      editor: vscode.TextEditor,
      range: vscode.Range,
      content: string
    ) => Promise<void>
  ): Promise<void> {
    for (const change of event.contentChanges) {
      // Only process additions, not deletions
      if (change.text.length === 0) {
        continue;
      }

      const lines = change.text.split('\n');
      const lineCount = lines.length;

      // Only trigger if multi-line insertion
      if (lineCount > this.MIN_LINES_THRESHOLD) {
        const range = new vscode.Range(change.range.start, change.range.end);
        const content = change.text;

        // Store insertion info
        const key = `${change.range.start.line}:${change.range.start.character}`;
        this.lastInsertions.set(key, { range, content });

        // Trigger callback
        await onTextInsert(editor, range, content);
      }
    }
  }

  /**
   * Get the last detected insertion.
   */
  static getLastInsertion(): {
    range: vscode.Range;
    content: string;
  } | null {
    if (this.lastInsertions.size === 0) {
      return null;
    }

    const lastKey = Array.from(this.lastInsertions.keys()).pop();
    if (!lastKey) {
      return null;
    }

    return this.lastInsertions.get(lastKey) || null;
  }

  /**
   * Clear stored insertions.
   */
  static clearInsertions(): void {
    this.lastInsertions.clear();
  }
}
