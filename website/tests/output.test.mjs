import assert from 'node:assert/strict';
import { access, readFile, mkdtemp, mkdir, writeFile, unlink, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

const dist = new URL('../dist/', import.meta.url).pathname;
const routes = ['index.html', 'quickstart/index.html', 'catalogue/index.html', 'host-setup/index.html', 'authoring/index.html', 'provenance-refresh/index.html', 'limits/index.html', '404.html'];
const downloads = ['quickstart', 'catalogue', 'host-setup', 'authoring', 'provenance-refresh', 'limits'];

test('static build emits each required page and generated Markdown download', async () => {
  for (const route of routes) await access(join(dist, route));
  for (const name of downloads) {
    const page = await readFile(join(dist, `${name}/index.html`), 'utf8');
    const markdown = await readFile(join(dist, `downloads/${name}.md`), 'utf8');
    assert.match(page, new RegExp(`/downloads/${name}\\.md`), `${name} page exposes its Markdown download`);
    assert.ok(markdown.startsWith('# '), `${name} download has a heading`);
    assert.ok(markdown.length > 100, `${name} download contains substantive content`);
  }
});

test('homepage uses canonical identity, selected-install command, and honest planned label', async () => {
  const html = await readFile(join(dist, 'index.html'), 'utf8');
  assert.match(html, /https:\/\/skillpot\.modepot\.io/);
  assert.match(html, /git clone --branch v0\.2\.0 --depth 1/);
  assert.match(html, /Planned direction—not a released workflow/);
  assert.match(html, /https:\/\/github\.com\/tugrulguner\/skillpot/);
  assert.match(html, /eight skills/);
  assert.doesNotMatch(html, /href="[^"]*playground/i);
});

test('canonical metadata and supporting assets are emitted', async () => {
  const html = await readFile(join(dist, 'index.html'), 'utf8');
  assert.match(html, /<link[^>]+rel="canonical"[^>]+href="https:\/\/skillpot\.modepot\.io\//);
  for (const asset of ['assets/skillpot-lockup.svg', 'assets/skillpot-mark.svg', 'assets/skillpot-workflow.png', 'robots.txt', 'sitemap.xml', 'llms.txt']) await access(join(dist, asset));
  assert.match(await readFile(join(dist, '404.html'), 'utf8'), /404|not found/i);
});

async function missingLocalTargets(root, html, route) {
  const missing = [];
  for (const match of html.matchAll(/(?:href|src)="([^"#][^"]*)"/g)) {
    const url = new URL(match[1].replaceAll('&amp;', '&'), `https://skillpot.modepot.io${route}`);
    if (url.origin !== 'https://skillpot.modepot.io') continue;
    const path = decodeURIComponent(url.pathname).replace(/^\//, '');
    // Astro emits the error document as 404.html, not 404/index.html.
    const emitted = path === '404/' ? '404.html' : (path.endsWith('/') || !path ? path + 'index.html' : path);
    try { await access(join(root, emitted)); }
    catch { missing.push(url.pathname); }
  }
  return missing;
}

test('every emitted page link and image targets an actual local artifact', async () => {
  for (const route of routes) {
    const html = await readFile(join(dist, route), 'utf8');
    const publicRoute = route === 'index.html' ? '/' : '/' + route.replace(/index\.html$/, '');
    assert.deepEqual(await missingLocalTargets(dist, html, publicRoute), [], route);
  }
});

test('link guard accepts a real guide and rejects its removed Markdown download', async () => {
  const root = await mkdtemp(join(tmpdir(), 'skillpot-link-guard-'));
  try {
    await mkdir(join(root, 'downloads'));
    await writeFile(join(root, 'downloads/guide.md'), '# Guide\n');
    const html = '<a href="/downloads/guide.md">Download</a>';
    assert.deepEqual(await missingLocalTargets(root, html, '/guide/'), []);
    await unlink(join(root, 'downloads/guide.md'));
    assert.deepEqual(await missingLocalTargets(root, html, '/guide/'), ['/downloads/guide.md']);
  } finally { await rm(root, {recursive:true, force:true}); }
});
