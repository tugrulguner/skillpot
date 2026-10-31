import { test, expect } from '@playwright/test';
import { readFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
const widths = [1280, 768, 390, 320];
const themes = ['light', 'dark', 'auto'];
for (const width of widths) for (const theme of themes) {
  test(`home and first use ${width} ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: width <= 390 ? 844 : 900 });
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto('/');
    await page.locator('starlight-theme-select select').first().selectOption(theme);
    await expect(page.locator('html')).toHaveAttribute('data-theme', theme === 'auto' ? 'dark' : theme);
    await expect(page.locator('h1')).toHaveCount(1);
    const wordmark = await page.locator('.site-title span').evaluate(e => {
      const r = e.getBoundingClientRect();
      const parent = e.closest('.title-wrapper').getBoundingClientRect();
      return r.left >= parent.left && r.right <= parent.right && r.right <= innerWidth;
    });
    expect(wordmark).toBe(true);
    await expect(page.getByRole('button', { name: 'Search', exact: true })).toBeVisible();
    const action = page.locator('.actions .primary');
    await expect(action).toBeVisible();
    const bounds = await action.boundingBox();
    expect(bounds.y + bounds.height).toBeLessThanOrEqual(page.viewportSize().height);
    expect(bounds.height).toBeGreaterThanOrEqual(44);
    await expect(page.locator('.art img')).toHaveJSProperty('complete', true);
    expect(await page.locator('.art img').evaluate(e => e.naturalWidth)).toBeGreaterThan(0);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    const socials = page.locator('.creator-row a');
    await expect(socials).toHaveText(['Created by Tugrul Guner', 'GitHub', 'LinkedIn', 'X']);
    for (const social of await socials.all()) {
      const result = await social.evaluate(e => {
        const r = e.getBoundingClientRect(), s = getComputedStyle(e);
        return { size: s.fontSize, weight: s.fontWeight, height: r.height, hit: e.contains(document.elementFromPoint(r.x + r.width/2, r.y + r.height/2)) };
      });
      expect(result.size).toBe('15px'); expect(result.weight).toBe('400');
      expect(result.height).toBeGreaterThanOrEqual(44); expect(result.hit).toBe(true);
    }
    if (width <= 768) {
      await page.getByRole('button', { name: 'Menu', exact: true }).click();
      await expect(page.locator('#family-menu-panel')).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(page.locator('#family-menu-panel')).toBeHidden();
    } else await expect(page.locator('.family-resources').first().getByRole('link', {name:'ModePot',exact:true})).toBeVisible();
    await page.screenshot({ path: info.outputPath(`home-${width}-${theme}.png`), fullPage: true });
    await page.locator('.creator-row').screenshot({ path: info.outputPath(`creator-${width}-${theme}.png`) });
    await expect(page.locator('footer a[rel="next"]')).toHaveAttribute('href', '/quickstart/');
    await action.focus(); await page.keyboard.press('Enter');
    await expect(page).toHaveURL(/\/quickstart\/$/);
    await expect(page.locator('h1')).toHaveText('Quick start');
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: info.outputPath(`quickstart-${width}-${theme}.png`), fullPage: true });
  });
}
test('Auto follows live OS theme changes and explicit choice persists', async ({ page }) => {
  await page.emulateMedia({ colorScheme:'light' }); await page.goto('/');
  const select = page.locator('starlight-theme-select select').first();
  await select.selectOption('auto'); await expect(page.locator('html')).toHaveAttribute('data-theme','light');
  await page.emulateMedia({ colorScheme:'dark' }); await expect(page.locator('html')).toHaveAttribute('data-theme','dark');
  await select.selectOption('light'); await page.reload(); await expect(page.locator('html')).toHaveAttribute('data-theme','light');
});
test('generated HTML, Markdown, routes and real source excerpt agree', async ({ page, request }) => {
  for (const route of ['quickstart','catalogue','host-setup','authoring','provenance-refresh','limits']) {
    await page.goto(`/${route}/`); await expect(page.locator('h1')).toHaveCount(1);
    const response = await request.get(`/downloads/${route}.md`); expect(response.status()).toBe(200);
    const canonical = await readFile(new URL(`../../src/content/docs/${route}.md`, import.meta.url),'utf8');
    const downloaded = await response.text(); expect(downloaded).toContain(canonical.split(/\n---\n/)[1].trim());
    const main = page.locator('.sl-markdown-content');
    expect(await main.locator('a[href]').count()).toBeGreaterThan(0);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `https://skillpot.modepot.io/${route}/`);
  }
  await page.goto('/');
  await expect(page.locator('.install code')).toHaveText('git clone --branch v0.3.0 --depth 1 https://github.com/tugrulguner/skillpot.git skillpot-source');
  const source = await readFile(new URL('../../../skills/intpot-python/SKILL.md', import.meta.url),'utf8');
  await expect(page.locator('.skill-excerpt code')).toHaveText(source.split('\n').slice(0,7).join('\n'));
  await expect(page.locator('.overview strong').filter({hasText:'Intpot:'})).toHaveCount(1);
  const missing = await request.get('/missing-page/'); expect(missing.status()).toBe(404);
  const verified = execFileSync(process.execPath, ['scripts/verify-site.mjs', 'http://127.0.0.1:4587'], {encoding:'utf8', timeout:30000});
  expect(verified).toContain('Verified 7 pages and 12 assets/downloads');
});

test('mobile search opens and finds the canonical catalogue', async ({ page }) => {
  await page.setViewportSize({width:320,height:844}); await page.goto('/');
  await page.getByRole('button',{name:'Search',exact:true}).click();
  await expect(page.getByRole('dialog',{name:'Search'})).toBeVisible();
  await page.getByRole('textbox',{name:'Search',exact:true}).fill('Intpot');
  await expect(page.getByRole('dialog',{name:'Search'}).getByRole('link').first()).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog',{name:'Search'})).toBeHidden();
});

test('guide links stay on the current origin and Markdown clicks save the actual file', async ({ page }) => {
  await page.goto('/host-setup/');
  await expect(page.getByRole('heading', {name:'Troubleshooting without changing your setup', exact:true})).toBeVisible();
  const catalogue = page.locator('.sl-markdown-content').getByRole('link', {name:'task-first catalogue', exact:true});
  await expect(catalogue).toHaveAttribute('href', '/catalogue/');
  await catalogue.click();
  await expect(page).toHaveURL('http://127.0.0.1:4587/catalogue/');
  const received = page.waitForEvent('download');
  await page.getByRole('link', {name:'Download this guide as Markdown', exact:true}).click();
  const download = await received;
  expect(download.suggestedFilename()).toBe('catalogue.md');
  const bytes = await readFile(await download.path(), 'utf8');
  expect(bytes).toBe(await readFile(new URL('../../dist/downloads/catalogue.md', import.meta.url), 'utf8'));
});
