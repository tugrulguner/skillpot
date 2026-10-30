import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

test('current-source skill excerpt is not attributed to the older published collection', async () => {
  const component = await readFile(new URL('../../src/components/SkillExcerpt.astro', import.meta.url), 'utf8');
  assert.match(component, /blob\/main\/skills\/intpot-python\/SKILL\.md/);
  assert.doesNotMatch(component, /blob\/v0\.2\.0\/skills\/intpot-python\/SKILL\.md/);
  assert.match(component, /published collection/);
  assert.match(component, /current source/);
});
