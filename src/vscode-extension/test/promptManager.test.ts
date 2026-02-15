/**
 * Tests for the prompt manager.
 */

import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';
import { PromptManager } from '../../src/promptManager';

suite('PromptManager', () => {
  let sandbox: sinon.SinonSandbox;

  setup(() => {
    sandbox = sinon.createSandbox();
  });

  teardown(() => {
    sandbox.restore();
  });

  suite('collectMetadata', () => {
    test('should return null when user cancels at tool name', async () => {
      sandbox.stub(vscode.window, 'showInputBox').resolves(undefined);

      const result = await PromptManager.collectMetadata('', '');
      assert.strictEqual(result, null);
    });

    test('should collect all metadata fields', async () => {
      sandbox.stub(vscode.window, 'showInputBox')
        .onFirstCall().resolves('GPT-4')
        .onSecondCall().resolves('1.0')
        .onThirdCall().resolves('dev-001');

      const result = await PromptManager.collectMetadata('', '');

      assert.ok(result);
      assert.strictEqual(result!.toolName, 'GPT-4');
      assert.strictEqual(result!.toolVersion, '1.0');
      assert.strictEqual(result!.authorId, 'dev-001');
      assert.strictEqual(result!.action, 'GENERATED');
    });

    test('should handle empty tool version', async () => {
      sandbox.stub(vscode.window, 'showInputBox')
        .onFirstCall().resolves('Claude')
        .onSecondCall().resolves('')
        .onThirdCall().resolves('author-1');

      const result = await PromptManager.collectMetadata('', '');

      assert.ok(result);
      assert.strictEqual(result!.toolVersion, undefined);
    });
  });
});
