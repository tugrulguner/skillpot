import { test, expect } from '@playwright/test';

for (const width of [1280, 390]) {
  test(`experiment-design source-only discovery and keyboard navigation ${width}`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/catalogue/');
    await expect(page.getByRole('heading', { name: 'Experiment design — published in v0.5.0', exact: true })).toBeVisible();
    await expect(page.locator('body')).toContainText('current source has eighteen bundles');
    await page.goto('/');
    const paragraph = page.locator('p').filter({ hasText: 'Published experiment-design' });
    await expect(paragraph).toContainText('experiment.md');
    await expect(paragraph).toContainText('Inspection/planning only');
    await expect(paragraph).toContainText('No experiments, benchmarks or models are run');
    const link = page.getByRole('link', { name: 'experiment-design first-use guide', exact: true });
    const destination = 'https://github.com/tugrulguner/skillpot/blob/main/docs/experiment-design-first-use.md';
    await expect(link).toHaveAttribute('href', destination);
    for (let step = 0; step < 100; step++) {
      await page.keyboard.press('Tab');
      if (await link.evaluate(element => element === document.activeElement)) break;
    }
    await expect(link).toBeFocused();
    await paragraph.screenshot({ path: testInfo.outputPath(`experiment-design-${width}.png`) });
    await page.route(destination, route => route.abort());
    const navigation = page.waitForRequest(destination);
    await page.keyboard.press('Enter');
    expect((await navigation).url()).toBe(destination);
    // This proves navigation intent, not availability of an unmerged destination.
  });
}
