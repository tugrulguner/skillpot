import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtemp, mkdir, rm, writeFile, readFile, readdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = fileURLToPath(new URL('.', import.meta.url));
const capture = join(dir, 'capture.mjs');
async function run(output, overrides = {}, signalAfterMs = 0) {
  return await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [capture], { cwd: dir, env: { ...process.env, ...overrides, SKILLPOT_OUTPUT: output }, stdio: 'ignore' });
    let killTimer;
    if (signalAfterMs) killTimer = setTimeout(() => child.kill('SIGTERM'), signalAfterMs);
    const timer = setTimeout(() => { child.kill('SIGKILL'); reject(new Error('Capture child did not exit within 25 seconds')); }, 25000);
    child.on('close', (code, signal) => { clearTimeout(timer); clearTimeout(killTimer); resolve({ code, signal }); });
  });
}
async function freshOutput() { const root = await mkdtemp(join(tmpdir(), 'skillpot-capture-')); return { root, output: join(root, 'run') }; }
async function assertFailedManifest(output) {
  const m = JSON.parse(await readFile(join(output, 'capture.json'), 'utf8'));
  assert.equal(m.status, 'failed');
  assert.ok(m.error);
  return m;
}

test('fails without output directory and never launches capture', async () => {
  const env = { ...process.env }; delete env.SKILLPOT_OUTPUT;
  const { code } = await new Promise(resolve => { const p = spawn(process.execPath, [capture], { cwd: dir, env, stdio: 'ignore' }); p.on('close', code => resolve({ code })); });
  assert.notEqual(code, 0);
});

test('refuses existing destination without modifying it', async () => {
  const { root, output } = await freshOutput(); await mkdir(output); await writeFile(join(output, 'keep.txt'), 'original');
  try { assert.notEqual((await run(output)).code, 0); assert.equal(await readFile(join(output, 'keep.txt'), 'utf8'), 'original'); assert.deepEqual(await readdir(output), ['keep.txt']); }
  finally { await rm(root, { recursive: true, force: true }); }
});

test('missing dependency fault closes server and writes explicit failed manifest', async () => {
  const { root, output } = await freshOutput();
  try { assert.notEqual((await run(output, { SKILLPOT_TEST_FAULT: 'missing-dependency' })).code, 0); const m = await assertFailedManifest(output); assert.match(m.error, /dependency unavailable/); }
  finally { await rm(root, { recursive: true, force: true }); }
});

test('missing browser fault closes server and writes explicit failed manifest', async () => {
  const { root, output } = await freshOutput();
  try { assert.notEqual((await run(output, { SKILLPOT_TEST_FAULT: 'missing-browser' })).code, 0); const m = await assertFailedManifest(output); assert.match(m.error, /absent-browser-executable/); }
  finally { await rm(root, { recursive: true, force: true }); }
});

test('unreachable application fault closes browser and server with no success manifest', async () => {
  const { root, output } = await freshOutput();
  try { assert.notEqual((await run(output, { SKILLPOT_TEST_FAULT: 'unreachable-app' })).code, 0); const m = await assertFailedManifest(output); assert.equal(m.status, 'failed'); assert.equal(m.result, null); }
  finally { await rm(root, { recursive: true, force: true }); }
});

test('failed UI action fault records failure and cleans up browser/context/server', async () => {
  const { root, output } = await freshOutput();
  try { assert.notEqual((await run(output, { SKILLPOT_TEST_FAULT: 'failed-ui-action' })).code, 0); const m = await assertFailedManifest(output); assert.match(m.error, /Absent add-row button/); assert.deepEqual(m.states.map(s => s.name), ['app-ready']); }
  finally { await rm(root, { recursive: true, force: true }); }
});

test('SIGTERM interruption gracefully closes resources and records partial capture as failed', async () => {
  const { root, output } = await freshOutput();
  try { assert.notEqual((await run(output, {}, 2500)).code, 0); const m = await assertFailedManifest(output); assert.match(m.error, /SIGTERM/); assert.equal(m.status, 'failed'); }
  finally { await rm(root, { recursive: true, force: true }); }
});
