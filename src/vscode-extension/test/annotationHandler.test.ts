/**
 * Tests for the annotation handler.
 */

import * as assert from 'assert';
import { AnnotationHandler } from '../../src/annotationHandler';
import { AnnotationMetadata } from '../../src/types';

suite('AnnotationHandler', () => {
  const metadata: AnnotationMetadata = {
    toolName: 'GPT-4',
    toolVersion: '1.0',
    date: '2025-02-15T10:30:00Z',
    authorId: 'dev-001',
    action: 'GENERATED',
  };

  suite('validateMetadata', () => {
    test('should accept valid metadata', () => {
      const errors = AnnotationHandler.validateMetadata(metadata);
      assert.strictEqual(errors.length, 0);
    });

    test('should reject empty tool name', () => {
      const invalid = { ...metadata, toolName: '' };
      const errors = AnnotationHandler.validateMetadata(invalid);
      assert.ok(errors.some((e) => e.includes('Tool name')));
    });

    test('should reject empty author ID', () => {
      const invalid = { ...metadata, authorId: '' };
      const errors = AnnotationHandler.validateMetadata(invalid);
      assert.ok(errors.some((e) => e.includes('Author ID')));
    });

    test('should reject invalid date format', () => {
      const invalid = { ...metadata, date: 'not-a-date' };
      const errors = AnnotationHandler.validateMetadata(invalid);
      assert.ok(errors.some((e) => e.includes('Date')));
    });

    test('should reject non-GENERATED action', () => {
      const invalid = { ...metadata, action: 'MODIFIED' as any };
      const errors = AnnotationHandler.validateMetadata(invalid);
      assert.ok(errors.some((e) => e.includes('GENERATED')));
    });
  });
});
