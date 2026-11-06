import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const root = join(dirname(fileURLToPath(import.meta.url)), '../..');

test('canonical guides link to product-owned routes as absolute URLs', async () => {
  const files = ['quickstart.md', 'catalogue.md', 'host-setup.md', 'authoring.md', 'provenance-refresh.md', 'limits.md'];
  for (const file of files) {
    const source = await readFile(join(root, 'src/content/docs', file), 'utf8');
    assert.doesNotMatch(source, /\]\((?:\/|\.\.?\/)(?:quickstart|catalogue|host-setup|authoring|provenance-refresh|limits|downloads)\//, `${file} route links should be canonical URLs, not root-relative filesystem-like paths`);
  }
});

test('released decision brief is discoverable with the v0.4.1 clone', async () => {
  const [home, catalogue] = await Promise.all(['index.mdx', 'catalogue.md'].map((f) => readFile(join(root, 'src/content/docs', f), 'utf8')));
  assert.match(home, /Published v0\.4\.1 includes \*\*decision-brief/);
  assert.match(catalogue, /decision-brief/);
  assert.match(catalogue, /Published v0\.4\.1 contains ten skills/);
  assert.doesNotMatch(catalogue, /reviewed, unreleased/);
  assert.match(home, /git clone --branch v0\.4\.1 --depth 1/);
});

test('agent map selects the latest published ten-skill snapshot', async () => {
  const map = await readFile(join(root, 'public/llms.txt'), 'utf8');
  assert.match(map, /releases\/tag\/v0\.4\.1/);
  assert.match(map, /decision-brief/);
  assert.match(map, /Published v0\.4\.1 contains ten skills/);
  assert.doesNotMatch(map, /v0\.3\.0|v0\.2\.0/);
});

test('document actions uses the published release across discovery', async () => {
  const [home, catalogue, map] = await Promise.all([
    readFile(join(root, 'src/content/docs/index.mdx'), 'utf8'),
    readFile(join(root, 'src/content/docs/catalogue.md'), 'utf8'),
    readFile(join(root, 'public/llms.txt'), 'utf8'),
  ]);
  for (const text of [home, catalogue, map]) {
    assert.match(text, /document-actions/);
    assert.match(text, /v0\.4\.1/);
    assert.doesNotMatch(text, /not included in published v0\.3\.0/);
  }
  assert.match(catalogue, /Published v0\.4\.1 contains ten skills/);
  assert.match(home, /git clone --branch v0\.4\.1 --depth 1/);
});

test('docs preserve experimental scope and runtime boundaries after publication', async () => {
  const [home, catalogue, limits] = await Promise.all(['index.mdx', 'catalogue.md', 'limits.md'].map((f) => readFile(join(root, 'src/content/docs', f), 'utf8')));
  assert.match(home, /v0\.4\.1/);
  assert.match(home, /experimental/);
  assert.match(catalogue, /seven imported public guidance files/);
  assert.match(limits, /not an agent runtime/);
});
