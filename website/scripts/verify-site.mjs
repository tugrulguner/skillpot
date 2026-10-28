import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const origin = process.argv[2] || 'https://skillpot.modepot.io';
const routes = ['', 'quickstart/', 'catalogue/', 'host-setup/', 'authoring/', 'provenance-refresh/', 'limits/'];
const assets = ['assets/skillpot-lockup.png', 'assets/skillpot-mark.svg', 'assets/skillpot-workflow.png', 'llms.txt', 'robots.txt', 'sitemap.xml', ...['quickstart','catalogue','host-setup','authoring','provenance-refresh','limits'].map(p => `downloads/${p}.md`)];
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
for (const route of routes) {
  const response = await fetch(new URL('/' + route, origin), { signal: AbortSignal.timeout(15000) });
  if (!response.ok) throw new Error(`${route || '/'}: HTTP ${response.status}`);
  const actual = await response.text();
  const expected = await readFile(`dist/${route}index.html`, 'utf8');
  if (digest(actual) !== digest(expected)) throw new Error(`${route || '/'} does not match this built artifact`);
}
for (const path of assets) {
  const response = await fetch(new URL('/' + path, origin), { signal: AbortSignal.timeout(15000) });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  if (digest(Buffer.from(await response.arrayBuffer())) !== digest(await readFile(`dist/${path}`))) throw new Error(`${path} byte mismatch`);
}
console.log(`Verified ${routes.length} pages and ${assets.length} assets/downloads at ${origin} against this exact build.`);
