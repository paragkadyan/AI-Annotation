/**
 * Main extension entry point.
 * Activates the AI Code Annotator extension and registers commands.
 */

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { AnnotationHandler } from './annotationHandler';
import { EditorListener } from './editorListener';
import { PromptManager } from './promptManager';

let disposables: vscode.Disposable[] = [];

/**
 * Read empid from .env file
 */
function getEmpidFromEnv(): string {
  try {
    // Try to find .env file in workspace root
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
      return '';
    }

    const envPath = path.join(workspaceFolder.uri.fsPath, '.env');
    if (fs.existsSync(envPath)) {
      const envContent = fs.readFileSync(envPath, 'utf-8');
      const lines = envContent.split('\n');
      for (const line of lines) {
        if (line.startsWith('EMPID=') || line.startsWith('empid=')) {
          const value = line.split('=')[1]?.trim();
          if (value) {
            return value;
          }
        }
      }
    }
  } catch (error) {
    console.error('Error reading .env file:', error);
  }

  return '';
}

/**
 * Get AI tool metadata from settings or environment
 */
function getToolMetadata(): { toolName: string; toolVersion?: string } {
  const config = vscode.workspace.getConfiguration('ai-annotator');
  const toolName = config.get<string>('defaultTool', 'GitHub Copilot');
  const toolVersion = config.get<string>('defaultToolVersion', '');

  return {
    toolName,
    toolVersion: toolVersion || undefined,
  };
}

export function activate(context: vscode.ExtensionContext) {
  console.log('AI Code Annotator extension is now active');

  // Register the mark AI-generated command
  const markCommand = vscode.commands.registerCommand(
    'ai-annotator.markAIGenerated',
    async () => {
      await handleMarkAIGenerated();
    }
  );

  disposables.push(markCommand);

  // Register text change listener
  const editorListenerDisposable = EditorListener.register(
    async (editor, range, content) => {
      await handleInsertedCode(editor, range, content);
    }
  );

  disposables.push(editorListenerDisposable);

  // Add all disposables to context
  disposables.forEach((d) => context.subscriptions.push(d));
}

/**
 * Handle the manual "Mark as AI-Generated" command.
 * Uses .env empid and settings for tool metadata.
 */
async function handleMarkAIGenerated(): Promise<void> {
  const editor = vscode.window.activeTextEditor;

  if (!editor) {
    vscode.window.showErrorMessage('No active editor. Please open a file first.');
    return;
  }

  const selection = editor.selection;
  if (selection.isEmpty) {
    vscode.window.showErrorMessage('No code selected. Please select code to annotate.');
    return;
  }

  // Get empid from .env file
  const authorId = getEmpidFromEnv();
  if (!authorId) {
    vscode.window.showErrorMessage(
      'EMPID not found in .env file. Please add EMPID=<your-id> to your .env file.'
    );
    return;
  }

  // Get tool metadata from settings
  const { toolName, toolVersion } = getToolMetadata();

  // Create metadata with auto-detected values
  const metadata = {
    toolName,
    toolVersion,
    date: new Date().toISOString(),
    authorId,
    action: 'GENERATED' as const,
  };

  // Validate metadata
  const validationErrors = AnnotationHandler.validateMetadata(metadata);
  if (validationErrors.length > 0) {
    PromptManager.showValidationError(validationErrors);
    return;
  }

  // Show confirmation with auto-detected values
  const confirmed = await PromptManager.confirmAnnotation(toolName, authorId);
  if (!confirmed) {
    return;
  }

  // Wrap the code
  AnnotationHandler.wrapWithAnnotation(editor, metadata);
}

/**
 * Handle code insertions detected by the editor listener.
 * Auto-detects with settings and .env file.
 */
async function handleInsertedCode(
  editor: vscode.TextEditor,
  range: vscode.Range,
  content: string
): Promise<void> {
  // Check if this looks like pasted code (multiple lines)
  const lineCount = content.split('\n').length;

  if (lineCount < 2) {
    return; // Too short, probably not AI-generated code
  }

  // Ask user if code was AI-generated
  const isAIGenerated = await PromptManager.promptForAIConfirmation();

  if (!isAIGenerated) {
    return;
  }

  // Get empid from .env file
  const authorId = getEmpidFromEnv();
  if (!authorId) {
    vscode.window.showWarningMessage(
      'EMPID not found in .env file. Skipping annotation. Add EMPID=<your-id> to .env'
    );
    return;
  }

  // Get tool metadata from settings
  const { toolName, toolVersion } = getToolMetadata();

  // Create metadata with auto-detected values
  const metadata = {
    toolName,
    toolVersion,
    date: new Date().toISOString(),
    authorId,
    action: 'GENERATED' as const,
  };

  // Validate metadata
  const validationErrors = AnnotationHandler.validateMetadata(metadata);
  if (validationErrors.length > 0) {
    vscode.window.showErrorMessage(`Annotation error: ${validationErrors.join(', ')}`);
    return;
  }

  // Show confirmation with auto-detected values
  const confirmed = await PromptManager.confirmAnnotation(toolName, authorId);
  if (!confirmed) {
    return;
  }

  // Create a selection for the inserted text
  const selection = new vscode.Selection(range.start, range.end);
  editor.selection = selection;

  // Wrap the code
  AnnotationHandler.wrapWithAnnotation(editor, metadata);
}

export function deactivate() {
  disposables.forEach((d) => d.dispose());
  disposables = [];
}
