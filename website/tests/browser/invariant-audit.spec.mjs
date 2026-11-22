import { test, expect } from '@playwright/test';

for (const width of [1280, 390]) {
  test(`invariant-audit source-only discovery ${width}`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    const paragraph = page.locator('p').filter({ hasText: 'Invariant-audit 0.1.0' });
    await expect(paragraph).toContainText('current source-only');
    await expect(paragraph).toContainText('not in stable v0.5.0');
    await expect(paragraph).toContainText('invariant-audit.md');
    await expect(paragraph).toContainText('not formal proof');
    await expect(paragraph).toContainText('nine-file bundle passed isolated installation');
    await paragraph.scrollIntoViewIfNeeded();
    await page.evaluate(() => document.fonts.ready);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    await paragraph.screenshot({ path: testInfo.outputPath(`invariant-audit-${width}.png`) });
    const link = page.getByRole('link', { name: 'first-use guide', exact: true });
    await expect(link).toHaveAttribute('href', 'https://github.com/tugrulguner/skillpot/blob/main/docs/invariant-audit-first-use.md');
    await page.goto('/catalogue/');
    const heading = page.getByRole('heading', { name: 'Invariant-audit — current source only', exact: true });
    await expect(heading).toBeVisible();
    await expect(page.locator('body')).toContainText('nine-file bundle passed isolated installation');
  });
}
