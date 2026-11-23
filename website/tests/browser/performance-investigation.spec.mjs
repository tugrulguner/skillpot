import { test, expect } from '@playwright/test';

for (const width of [1280, 390]) {
  test(`performance-investigation source-only discovery ${width}`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    const paragraph = page.locator('p').filter({ hasText: 'Performance-investigation 0.1.0' });
    await expect(paragraph).toContainText('current source-only');
    await expect(paragraph).toContainText('not in stable v0.5.0');
    await expect(paragraph).toContainText('investigation.md');
    await expect(paragraph).toContainText('benchmark-audit');
    await expect(paragraph).toContainText('eleven-file bundle passed isolated installation');
    await paragraph.scrollIntoViewIfNeeded();
    await page.evaluate(() => document.fonts.ready);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    await paragraph.screenshot({ path: testInfo.outputPath(`performance-investigation-${width}.png`) });
    const link = paragraph.getByRole('link', { name: 'first-use guide', exact: true });
    await expect(link).toHaveAttribute('href', 'https://github.com/tugrulguner/skillpot/blob/main/docs/performance-investigation-first-use.md');
  });
}
