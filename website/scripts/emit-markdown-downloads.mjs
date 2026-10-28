import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const source = join(root, 'src/content/docs');
const out = join(root, 'dist/downloads');
const pages = ['quickstart', 'catalogue', 'host-setup', 'authoring', 'provenance-refresh', 'limits'];
await mkdir(out, { recursive: true });
for (const page of pages) {
  const raw = await readFile(join(source, `${page}.md`), 'utf8');
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) throw new Error(`Missing frontmatter or content for ${page}`);
  const title = match[1].match(/^title:\s*(.+)$/m)?.[1];
  if (!title || !match[2].trim()) throw new Error(`Incomplete canonical Markdown source: ${page}`);
  await writeFile(join(out, `${page}.md`), `# ${title}\n\n${match[2].trim()}\n`);
}
console.log(`Emitted ${pages.length} Markdown downloads from canonical docs.`);
