/**
 * TypeScript interfaces and types for the AI Code Annotator extension.
 */

export interface AnnotationMetadata {
  toolName: string;
  toolVersion?: string;
  date: string;
  authorId: string;
  action: 'GENERATED';
}

export interface AnnotationBlock {
  startLine: number;
  endLine: number;
  metadata: AnnotationMetadata;
}

export interface AnnotationConfig {
  authorId: string;
  defaultTool?: string;
}

export enum SupportedLanguage {
  Python = 'python',
  JavaScript = 'javascript',
  TypeScript = 'typescript',
  Java = 'java',
  Cpp = 'cpp',
  CSharp = 'csharp',
  Go = 'go',
  Ruby = 'ruby',
  Php = 'php',
  Swift = 'swift',
  Kotlin = 'kotlin',
  Sql = 'sql',
  Haskell = 'haskell',
  Matlab = 'matlab',
  Shell = 'shell',
}

export interface CommentStyle {
  lineComment: string;
  blockCommentStart?: string;
  blockCommentEnd?: string;
}

export const LANGUAGE_COMMENT_STYLES: Record<string, CommentStyle> = {
  python: { lineComment: '#' },
  javascript: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  typescript: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  java: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  cpp: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  c: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  csharp: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  go: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  ruby: { lineComment: '#' },
  php: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  swift: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  kotlin: { lineComment: '//', blockCommentStart: '/*', blockCommentEnd: '*/' },
  sql: { lineComment: '--' },
  haskell: { lineComment: '--', blockCommentStart: '{-', blockCommentEnd: '-}' },
  matlab: { lineComment: '%' },
  shell: { lineComment: '#' },
};
