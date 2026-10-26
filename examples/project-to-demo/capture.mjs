import { createServer } from 'node:http';
import { readFile, mkdir, stat, writeFile, copyFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { resolve, join } from 'node:path';

const here = fileURLToPath(new URL('.', import.meta.url));
const sourcePaths = ['capture.mjs', 'index.html', 'transform.mjs'];
const sha256 = async path => createHash('sha256').update(await readFile(path)).digest('hex');
const timeout = (promise, ms, label) => new Promise((resolve, reject) => { const timer = setTimeout(() => reject(new Error(`${label} timed out after ${ms}ms`)), ms); Promise.resolve(promise).then(value => { clearTimeout(timer); resolve(value); }, error => { clearTimeout(timer); reject(error); }); });

const fault = process.env.SKILLPOT_TEST_FAULT ?? '';
const interruptAfter = Number(process.env.SKILLPOT_TEST_INTERRUPT_MS ?? 0);
const out = process.env.SKILLPOT_OUTPUT ? resolve(process.env.SKILLPOT_OUTPUT) : '';
const started = new Date().toISOString();
const states = [];
let server, browser, context, page, stopping = false, status = 'failed', result = null, errorText = null, version = null, source = {};
let serverUrl = null, rawPath = null, ownsOutput = false;

async function manifest() {
  if (!ownsOutput) return;
  const payload = { status, started, finished: new Date().toISOString(), playwright: version, node: process.version, source, result, states, raw: rawPath, error: errorText };
  await writeFile(join(out, 'capture.json'), `${JSON.stringify(payload, null, 2)}\n`).catch(error => { status = 'failed'; process.exitCode = 1; process.stderr.write(`Cannot save capture manifest: ${error.message}\n`); });
}
function cleanupFailed(error) { status = 'failed'; errorText ??= String(error); process.exitCode = 1; }
async function cleanup() {
  if (context) { const c = context; context = null; await timeout(c.close(), 10000, 'browser context close').catch(cleanupFailed); }
  if (browser) { const b = browser; browser = null; await timeout(b.close(), 10000, 'browser close').catch(cleanupFailed); }
  if (server?.listening) await timeout(new Promise(resolveClose => server.close(resolveClose)), 5000, 'server close').catch(cleanupFailed);
  await manifest();
}
async function interrupt(signal) {
  if (stopping) return;
  stopping = true; status = 'failed'; errorText ??= `Interrupted by ${signal}`;
  await cleanup(); process.exitCode = 1;
}
process.on('SIGINT', () => void interrupt('SIGINT'));
process.on('SIGTERM', () => void interrupt('SIGTERM'));

async function main() {
  if (!out) throw new Error('Set SKILLPOT_OUTPUT to a new output directory.');
  try { await stat(out); throw new Error(`Output already exists; refusing to overwrite: ${out}`); } catch (e) { if (e.code !== 'ENOENT') throw e; }
  await mkdir(out, { recursive: false });
  ownsOutput = true;
  await mkdir(join(out, 'raw')); await mkdir(join(out, 'frames'));
  for (const name of sourcePaths) source[name] = await sha256(join(here, name));
  const require = createRequire(import.meta.url);
  let chromium;
  try { chromium = require(fault === 'missing-dependency' ? 'skillpot-deliberately-missing-playwright' : 'playwright').chromium; version = require('playwright/package.json').version; }
  catch (e) { throw new Error(`Playwright dependency unavailable: ${e.message}`); }
  server = createServer(async (req, res) => {
    try {
      if (fault === 'unreachable-app') { res.writeHead(503); res.end('Controlled unavailable application'); return; }
      const path = req.url === '/' ? 'index.html' : req.url.slice(1);
      if (!['index.html', 'transform.mjs'].includes(path)) throw new Error('not found');
      const body = await readFile(join(here, path));
      res.writeHead(200, { 'content-type': path.endsWith('.mjs') ? 'text/javascript; charset=utf-8' : 'text/html; charset=utf-8' }); res.end(body);
    } catch { res.writeHead(404); res.end('Not found'); }
  });
  server.listen(0, '127.0.0.1');
  await timeout(new Promise((resolveListen, reject) => { server.once('listening', resolveListen); server.once('error', reject); }), 5000, 'server startup');
  serverUrl = `http://127.0.0.1:${server.address().port}/`;
  browser = await timeout(chromium.launch({ headless: true, ...(fault === 'missing-browser' ? { executablePath: join(out, 'absent-browser-executable') } : {}) }), 15000, 'browser launch');
  context = await browser.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: join(out, 'raw'), size: { width: 1280, height: 720 } } });
  page = await context.newPage();
  page.setDefaultTimeout(5000);
  const transition = async (name, action) => { const at = Date.now(); await timeout(action(), 8000, name); states.push({ name, elapsedMs: Date.now() - at, timestamp: new Date().toISOString() }); };
  await page.goto(serverUrl, { waitUntil: 'networkidle', timeout: 4000 });
  await page.getByRole('heading', { name: 'Group rows into records' }).waitFor();
  states.push({ name: 'app-ready', timestamp: new Date().toISOString() });
  await page.screenshot({ path: join(out, 'frames/01-empty.png') });
  await page.waitForTimeout(3000);
  const item = page.getByRole('textbox', { name: 'Item' });
  await transition('first-row-input', async () => {
    await page.getByRole('textbox', { name: 'Identifier' }).pressSequentially('demo-1', { delay: 70 });
    await item.pressSequentially('apples', { delay: 45 });
    await page.getByRole('button', { name: fault === 'failed-ui-action' ? 'Absent add-row button' : 'Add row' }).click();
  });
  await page.getByText('Item: apples').waitFor();
  await page.screenshot({ path: join(out, 'frames/02-one-row.png') });
  await page.waitForTimeout(6000);
  await transition('second-row-input', async () => { await item.pressSequentially('pears', { delay: 45 }); await page.getByRole('button', { name: 'Add row' }).click(); });
  if (await page.locator('[data-row]').count() !== 2) throw new Error('Expected exactly two visible input rows.');
  await page.screenshot({ path: join(out, 'frames/03-two-rows.png') });
  await page.waitForTimeout(8000);
  await transition('group-rows-click', () => page.getByRole('button', { name: 'Group rows' }).click());
  await page.locator('#output pre').waitFor({ state: 'visible' });
  const actual = await page.locator('#output pre').innerText();
  result = JSON.parse(actual);
  if (JSON.stringify(result) !== JSON.stringify([{ id: 'demo-1', items: ['apples', 'pears'] }])) throw new Error(`Unexpected actual UI output: ${actual}`);
  const bounds = await page.locator('#output').boundingBox();
  if (!bounds || bounds.y + bounds.height > 720) throw new Error('Actual output is clipped by the recording viewport');
  await page.screenshot({ path: join(out, 'frames/04-grouped-output.png') });
  await page.waitForTimeout(12000);
  if (stopping) throw new Error('Capture interrupted.');
  const video = await page.video();
  const temp = await video.path();
  await context.close(); context = null;
  rawPath = join(out, 'raw/capture.webm');
  await copyFile(temp, rawPath);
  if (stopping) throw new Error('Capture interrupted before completion.');
  status = 'success';
  await manifest();
  console.log(JSON.stringify({ status, playwright: version, node: process.version, result, raw: rawPath, states }));
}

let signalTimer;
try {
  if (interruptAfter > 0) signalTimer = setTimeout(() => process.kill(process.pid, 'SIGTERM'), interruptAfter);
  await main();
} catch (error) {
  status = 'failed'; errorText ??= String(error?.stack ?? error);
  process.stderr.write(`${JSON.stringify({ status, error: errorText })}\n`);
  process.exitCode = 1;
} finally {
  clearTimeout(signalTimer);
  await cleanup();
}
