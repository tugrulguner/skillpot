import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve, relative } from 'node:path';
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
const routes = new Map([['README.md', '/'], ['catalog/README.md', '/catalogue/'], ['docs/quickstart.md', '/host-setup/'], ['docs/skill-contract.md', '/authoring/'], ['docs/release-policy.md', '/provenance-refresh/']]);
await mkdir(resolve(site, 'src/content/docs'), { recursive: true });
for (const [slug, title, filename, start, end] of pages) {
  let text = await readFile(resolve(repo, filename), 'utf8');
  if (start) {
    const begin = text.indexOf(`## ${start}\n`), finish = text.indexOf(`## ${end}\n`, begin + 1);
    if (begin < 0 || finish < 0) throw new Error(`Missing canonical section ${filename}: ${start}`);
    text = text.slice(begin + `## ${start}\n`.length, finish).trim();
  } else text = text.replace(/^# [^\n]+\n/, '').trim();
  text = text.replace(/(!?\[[^\]\n]*\]\()([^\s)]+)([^)]*\))/g, (all, prefix, destination, suffix) => {
    if (/^(?:[a-z][a-z\d+.-]*:|#|\/\/)/i.test(destination)) return all;
    const [path, fragment] = destination.split('#');
    const target = relative(repo, resolve(dirname(resolve(repo, filename)), decodeURIComponent(path)));
    const route = routes.get(target);
    const url = route ? `https://skillpot.modepot.io${route}` : `https://github.com/tugrulguner/skillpot/blob/main/${target}`;
    return `${prefix}${url}${fragment ? '#' + fragment : ''}${suffix}`;
  });
  await writeFile(resolve(site, `src/content/docs/${slug}.md`), `---\ntitle: ${title}\ndescription: Canonical SkillPot ${title.toLowerCase()} guidance.\n---\n\n<!-- Generated from ${filename}; edit the repository source, not this file. -->\n\n${text}\n\n[Download this guide as Markdown](https://skillpot.modepot.io/downloads/${slug}.md).\n`);
}
console.log(`Generated ${pages.length} site guides from canonical repository documents.`);
