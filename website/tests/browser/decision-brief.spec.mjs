import { test, expect } from '@playwright/test';

test('new decision workflow stays source-only across discovery and downloads', async ({ page, request }, info) => {
  await page.goto('/');
  await expect(page.locator('.overview')).toContainText('decision-brief');
  await expect(page.locator('.overview')).toContainText('not included in published v0.3.0');
  await expect(page.locator('.install code')).toHaveText('git clone --branch v0.3.0 --depth 1 https://github.com/tugrulguner/skillpot.git skillpot-source');
  await page.goto('/catalogue/');
  const body = page.locator('.sl-markdown-content');
  await expect(body).toContainText('Current source contains nine skills');
  await expect(body).toContainText('reviewed, unreleased');
  await expect(body).toContainText('not included in published v0.3.0');
  await expect(body.getByRole('link', { name: 'decision-brief', exact: true })).toHaveAttribute('href', 'https://github.com/tugrulguner/skillpot/blob/main/skills/decision-brief/SKILL.md');
  for (const width of [1280, 390]) {
    await page.setViewportSize({ width, height: 900 });
    await body.getByRole('link', { name: 'decision-brief', exact: true }).scrollIntoViewIfNeeded();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: info.outputPath(`decision-catalogue-${width}.png`) });
  }
  const markdown = await request.get('/downloads/catalogue.md');
  expect(markdown.ok()).toBe(true);
  expect(await markdown.text()).toContain('not included in published v0.3.0');
  const map = await request.get('/llms.txt');
  expect(map.ok()).toBe(true);
  const text = await map.text();
  expect(text).toContain('decision-brief');
  expect(text).toContain('releases/tag/v0.3.0');
  expect(text).not.toContain('v0.2.0');
});

test('catalogue opens the pinned source-only first-use steps', async ({ page }, info) => {
  for (const width of [1280, 390]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/catalogue/');
    const guide = page.locator('.sl-markdown-content').getByRole('link', { name: 'source-only first-use guide', exact: true });
    await expect(guide).toHaveAttribute('href', '/host-setup/#try-decision-brief-from-reviewed-source');
    await guide.click();
    await expect(page).toHaveURL(/\/host-setup\/#try-decision-brief-from-reviewed-source$/);
    await expect(page.getByRole('heading', { name: 'Try decision-brief from reviewed source', exact: true })).toBeVisible();
    const content = page.locator('.sl-markdown-content');
    await expect(content).toContainText('4ca53963cafc8a9a3965808c485dc8c6ad502a66');
    await expect(content).toContainText('decision-brief-output/evidence.md');
    await expect(content).toContainText('not included in published v0.3.0');
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: info.outputPath(`decision-first-use-${width}.png`) });
  }
});
