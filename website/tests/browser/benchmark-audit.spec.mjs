import { test, expect } from '@playwright/test';

for (const width of [1280, 390]) {
  test(`benchmark-audit source-only discovery and keyboard navigation ${width}`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    const paragraph = page.locator('p').filter({ hasText: 'Current-source benchmark-audit' });
    await expect(paragraph).toContainText('benchmark-audit.md');
    await expect(paragraph).toContainText('Inspection-only');
    await expect(paragraph).toContainText('does not run benchmarks or models');
    const link = page.getByRole('link', { name: 'benchmark-audit first-use guide', exact: true });
    const destination = 'https://github.com/tugrulguner/skillpot/blob/main/docs/benchmark-audit-first-use.md';
    await expect(link).toHaveAttribute('href', destination);
    for (let step = 0; step < 80; step++) {
      await page.keyboard.press('Tab');
      if (await link.evaluate((element) => element === document.activeElement)) break;
    }
    await expect(link).toBeFocused();
    await paragraph.screenshot({ path: testInfo.outputPath(`benchmark-audit-${width}.png`) });
    // Verify the actual Enter navigation request without requesting an unmerged page
    // or claiming that an intercepted/aborted destination was served successfully.
    await page.route(destination, (route) => route.abort());
    const navigation = page.waitForRequest(destination);
    await page.keyboard.press('Enter');
    expect((await navigation).url()).toBe(destination);
  });
}
