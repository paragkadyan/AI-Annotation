/**
 * Tests for the editor listener.
 */

import * as assert from 'assert';
import { EditorListener } from '../../src/editorListener';

suite('EditorListener', () => {
  suite('insertions tracking', () => {
    test('should clear insertions', () => {
      EditorListener.clearInsertions();
      const insertion = EditorListener.getLastInsertion();
      assert.strictEqual(insertion, null);
    });

    test('should return null when no insertions', () => {
      EditorListener.clearInsertions();
      const insertion = EditorListener.getLastInsertion();
      assert.strictEqual(insertion, null);
    });
  });
});
