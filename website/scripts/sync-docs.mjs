import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { canonicalBody, rewriteLinks } from './doc-content.mjs';
import { fileURLToPath } from 'node:url';
const site = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repo = resolve(site, '..');
const pages = [
  ['quickstart', 'Quick start', 'README.md', 'Quick start', 'Choose a workflow'],
  ['catalogue', 'Catalogue', 'catalog/README.md'],
  ['host-setup', 'Host setup', 'docs/quickstart.md'],
  ['authoring', 'Authoring reference', 'docs/skill-contract.md'],
  ['provenance-refresh', 'Provenance and refresh', 'docs/release-policy.md'],
  ['limits', 'Boundaries', 'README.md', 'Boundaries', 'Community and contributing'],
];
await mkdir(resolve(site, 'src/content/docs'), { recursive: true });
for (const [slug, title, filename, start, end] of pages) {
  const source = await readFile(resolve(repo, filename), 'utf8');
  const text = rewriteLinks(canonicalBody(source, filename, start, end), filename);
  await writeFile(resolve(site, `src/content/docs/${slug}.md`), `---\ntitle: ${title}\ndescription: Canonical SkillPot ${title.toLowerCase()} guidance.\n---\n\n<!-- Generated from ${filename}; edit the repository source, not this file. -->\n\n${text}\n\n[Download this guide as Markdown](https://skillpot.modepot.io/downloads/${slug}.md).\n`);
}
console.log(`Generated ${pages.length} site guides from canonical repository documents.`);
