import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const root = join(dirname(fileURLToPath(import.meta.url)), '../..');

test('verification-loop remains source-only with acceptance-linked evidence', async () => {
  const files = ['src/content/docs/index.mdx', 'src/content/docs/catalogue.md', 'public/llms.txt'];
  for (const file of files) {
    const text = await readFile(join(root, file), 'utf8');
    assert.match(text, /verification-loop/);
    assert.match(text, /verification-loop-first-use\.md/);
    assert.match(text, /verification\.md/);
    assert.match(text, /v0\.5\.0/);
    assert.match(text, /permission/);
  }
});

test('canonical guides link to product-owned routes as absolute URLs', async () => {
  const files = ['quickstart.md', 'catalogue.md', 'host-setup.md', 'authoring.md', 'provenance-refresh.md', 'limits.md'];
  for (const file of files) {
    const source = await readFile(join(root, 'src/content/docs', file), 'utf8');
    assert.doesNotMatch(source, /\]\((?:\/|\.\.?\/)(?:quickstart|catalogue|host-setup|authoring|provenance-refresh|limits|downloads)\//, `${file} route links should be canonical URLs, not root-relative filesystem-like paths`);
  }
});

test('claim-check is current-source and unreleased, separate from the stable release', async () => {
  const [home, catalogue, map] = await Promise.all([
    readFile(join(root, 'src/content/docs/index.mdx'), 'utf8'),
    readFile(join(root, 'src/content/docs/catalogue.md'), 'utf8'),
    readFile(join(root, 'public/llms.txt'), 'utf8'),
  ]);
  for (const text of [home, catalogue, map]) {
    assert.match(text, /claim-check/);
    assert.match(text, /published/i);
    assert.match(text, /claim-check-first-use\.md/);
  }
  assert.match(home, /npx skills@1\.7\.6 add https:\/\/github\.com\/tugrulguner\/skillpot\/tree\/044213fd00343e94b4d389c3ca2c0f2909feb79f --skill claim-check/);
  assert.match(catalogue, /seventeen current-source bundles/);
  assert.match(catalogue, /npx skills@1\.7\.6 add https:\/\/github\.com\/tugrulguner\/skillpot\/tree\/044213fd00343e94b4d389c3ca2c0f2909feb79f --skill claim-check/);
  assert.match(map, /claim-check-first-use\.md/);
  assert.match(map, /Published v0\.5\.0 contains seventeen skills/);
  assert.doesNotMatch(map, /Published v0\.5\.0 contains eleven skills/);
});

test('benchmark-audit is a source-only inspection workflow, separate from stable ten', async () => {
  const [home, catalogue, map] = await Promise.all([
    readFile(join(root, 'src/content/docs/index.mdx'), 'utf8'),
    readFile(join(root, 'src/content/docs/catalogue.md'), 'utf8'),
    readFile(join(root, 'public/llms.txt'), 'utf8'),
  ]);
  for (const text of [home, catalogue, map]) {
    assert.match(text, /benchmark-audit/);
    assert.match(text, /benchmark-audit-first-use\.md/);
    assert.match(text, /benchmark-audit\.md/);
    assert.match(text, /inspection-only/i);
    assert.match(text, /does not run benchmarks|without benchmark or model execution/i);
  }
  assert.match(home, /seventeen skills/);
  assert.match(catalogue, /seventeen current-source bundles/);
  assert.match(map, /Published v0\.5\.0 contains seventeen skills/);
});

test('released decision brief is discoverable with the v0.5.0 clone', async () => {
  const [home, catalogue] = await Promise.all(['index.mdx', 'catalogue.md'].map((f) => readFile(join(root, 'src/content/docs', f), 'utf8')));
  assert.match(home, /Published v0\.5\.0 includes \*\*decision-brief/);
  assert.match(catalogue, /decision-brief/);
  assert.match(catalogue, /Published v0\.5\.0 contains seventeen skills/);
  assert.doesNotMatch(catalogue, /reviewed, unreleased/);
  assert.match(home, /npx skills@1\.7\.6 add https:\/\/github\.com\/tugrulguner\/skillpot\/tree\/044213fd00343e94b4d389c3ca2c0f2909feb79f --skill claim-check/);
});

test('agent map selects the latest published ten-skill snapshot', async () => {
  const map = await readFile(join(root, 'public/llms.txt'), 'utf8');
  assert.match(map, /releases\/tag\/v0\.5\.0/);
  assert.match(map, /decision-brief/);
  assert.match(map, /Published v0\.5\.0 contains seventeen skills/);
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
    assert.match(text, /v0\.5\.0/);
    assert.doesNotMatch(text, /not included in published v0\.3\.0/);
  }
  assert.match(catalogue, /Published v0\.5\.0 contains seventeen skills/);
  assert.match(home, /npx skills@1\.7\.6 add https:\/\/github\.com\/tugrulguner\/skillpot\/tree\/044213fd00343e94b4d389c3ca2c0f2909feb79f --skill claim-check/);
});

test('docs preserve experimental scope and runtime boundaries after publication', async () => {
  const [home, catalogue, limits] = await Promise.all(['index.mdx', 'catalogue.md', 'limits.md'].map((f) => readFile(join(root, 'src/content/docs', f), 'utf8')));
  assert.match(home, /v0\.5\.0/);
  assert.match(home, /experimental/);
  assert.match(catalogue, /seven imported public guidance files/);
  assert.match(limits, /not an agent runtime/);
});
