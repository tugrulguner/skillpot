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

test('unreleased decision brief is discoverable without changing the stable clone', async () => {
  const [home, catalogue] = await Promise.all(['index.mdx', 'catalogue.md'].map((f) => readFile(join(root, 'src/content/docs', f), 'utf8')));
  assert.match(home, /decision-brief/);
  assert.match(home, /not included in published v0\.3\.0/);
  assert.match(catalogue, /decision-brief/);
  assert.match(catalogue, /not included in published v0\.3\.0/);
  assert.match(home, /git clone --branch v0\.3\.0 --depth 1/);
});

test('agent map separates the latest published snapshot from new source', async () => {
  const map = await readFile(join(root, 'public/llms.txt'), 'utf8');
  assert.match(map, /releases\/tag\/v0\.3\.0/);
  assert.match(map, /decision-brief/);
  assert.match(map, /not included in published v0\.3\.0/);
  assert.doesNotMatch(map, /v0\.2\.0/);
});

test('docs scope release and experimental status without claiming a runtime', async () => {
  const [home, catalogue, limits] = await Promise.all(['index.mdx', 'catalogue.md', 'limits.md'].map((f) => readFile(join(root, 'src/content/docs', f), 'utf8')));
  assert.match(home, /v0\.3\.0/);
  assert.match(home, /experimental/);
  assert.match(catalogue, /seven imported public guidance files/);
  assert.match(limits, /not an agent runtime/);
});
