import { test, expect } from '@playwright/test';

for (const width of [1280, 390]) {
  test(`verification-loop source-only discovery and keyboard navigation ${width}`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/catalogue/');
    await expect(page.getByRole('heading', { name: 'Verification loop — published in v0.5.0', exact: true })).toBeVisible();
    await expect(page.locator('body')).toContainText('seventeen current-source bundles');
    await page.goto('/');
    const paragraph = page.locator('p').filter({ hasText: 'Published verification-loop' });
    await expect(paragraph).toContainText('verification.md');
    await expect(paragraph).toContainText('Without execution permission it plans only');
    await expect(paragraph).toContainText('repairs require permission');
    const link = page.getByRole('link', { name: 'verification-loop first-use guide', exact: true });
    const destination = 'https://github.com/tugrulguner/skillpot/blob/main/docs/verification-loop-first-use.md';
    await expect(link).toHaveAttribute('href', destination);
    for (let step = 0; step < 100; step++) {
      await page.keyboard.press('Tab');
      if (await link.evaluate(element => element === document.activeElement)) break;
    }
    await expect(link).toBeFocused();
    await paragraph.screenshot({ path: testInfo.outputPath(`verification-loop-${width}.png`) });
    await page.route(destination, route => route.abort());
    const navigation = page.waitForRequest(destination);
    await page.keyboard.press('Enter');
    expect((await navigation).url()).toBe(destination);
    // This proves navigation intent, not availability of an unmerged destination.
  });
}
