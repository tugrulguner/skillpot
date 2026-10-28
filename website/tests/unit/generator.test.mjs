import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, copyFile, symlink, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';
import test from 'node:test';

async function generate({readme, authoring}) {
  const root = await mkdtemp(join(tmpdir(), 'skillpot-generator-'));
  try {
    const site = join(root, 'website');
    await mkdir(join(site, 'scripts'), {recursive:true});
    await mkdir(join(root, 'docs')); await mkdir(join(root, 'catalog'));
    for (const name of ['sync-docs.mjs', 'doc-content.mjs']) {
      try { await copyFile(new URL(`../../scripts/${name}`, import.meta.url), join(site, 'scripts', name)); }
      catch (error) { if (name !== 'doc-content.mjs' || error.code !== 'ENOENT') throw error; }
    }
    await symlink(new URL('../../node_modules', import.meta.url).pathname, join(site, 'node_modules'), 'dir');
    await writeFile(join(root, 'README.md'), readme || '# Library\n\n## Quick start\nREAL INSTALL\n\n## Choose a workflow\nChoose.\n\n## Boundaries\nLimits.\n\n## Community and contributing\nCommunity.\n');
    for (const name of ['quickstart.md', 'skill-contract.md', 'release-policy.md']) await writeFile(join(root, 'docs', name), name === 'skill-contract.md' ? authoring || '# Authoring\nContract.\n' : '# Guide\nGuidance.\n');
    await writeFile(join(root, 'catalog/README.md'), '# Catalogue\nSkills.\n');
    execFileSync(process.execPath, [join(site, 'scripts/sync-docs.mjs')], {cwd:site});
    return Object.fromEntries(await Promise.all(['authoring', 'quickstart'].map(async name => [name, await readFile(join(site, 'src/content/docs', name + '.md'), 'utf8')])));
  } finally { await rm(root, {recursive:true, force:true}); }
}

test('generator preserves literal fenced and inline Markdown examples', async () => {
  const example = '```md\n[Example](../README.md)\n```\n\n`[Inline](../README.md)`';
  const output = await generate({authoring:'# Authoring\n\n' + example + '\n\n[Actual](../README.md)\n'});
  assert.ok(output.authoring.includes(example), 'examples must not be rewritten as navigation');
  assert.match(output.authoring, /\[Actual\]\(https:\/\/skillpot\.modepot\.io\/\)/);
});

test('generator finds actual section headings, not examples, with CRLF source', async () => {
  const readme = '# Library\n\n```md\n## Quick start\nNOT THE INSTALL\n## Choose a workflow\n```\n\n## Quick start\nREAL INSTALL\n\n## Choose a workflow\nChoose.\n\n## Boundaries\nLimits.\n\n## Community and contributing\nCommunity.\n'.replaceAll('\n', '\r\n');
  const output = await generate({readme});
  assert.match(output.quickstart, /REAL INSTALL/);
  assert.doesNotMatch(output.quickstart, /NOT THE INSTALL/);
});

test('reference definitions and angle-bracket paths retain usable canonical links', async () => {
  const output = await generate({authoring:'# Authoring\n\n[Setup][host]\n\n[host]: quickstart.md "Host setup"\n\n[Notice](<../assets/full notice.md> "Full notice")\n'});
  assert.match(output.authoring, /https:\/\/skillpot\.modepot\.io\/host-setup\//);
  assert.match(output.authoring, /https:\/\/github\.com\/tugrulguner\/skillpot\/blob\/main\/assets\/full%20notice.md/);
  assert.match(output.authoring, /"Host setup"/);
});

test('README fragments point to real site guides, not absent homepage sections', async () => {
  const output = await generate({authoring:'# Authoring\n\n[Install](../README.md#quick-start) and [Limits](../README.md#boundaries).\n'});
  assert.match(output.authoring, /\[Install\]\(https:\/\/skillpot\.modepot\.io\/quickstart\/\)/);
  assert.match(output.authoring, /\[Limits\]\(https:\/\/skillpot\.modepot\.io\/limits\/\)/);
});
