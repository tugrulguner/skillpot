import { test, expect } from '@playwright/test';

test('released document actions and release-pinned first-use are discoverable', async ({ page, request }, info) => {
  for (const width of [1280, 390]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    await expect(page.locator('.overview')).toContainText('document-actions');
    await page.goto('/catalogue/');
    const content = page.locator('.sl-markdown-content');
    await expect(content).toContainText('Published v0.4.1 contains ten skills');
    await expect(content).toContainText('document-actions');
    await expect(content).toContainText('included in v0.4.1');
    const guide = content.getByRole('link', { name: 'document-actions first-use guide', exact: true });
    await expect(guide).toHaveAttribute('href', '/host-setup/#try-document-actions-from-pinned-source');
    await guide.scrollIntoViewIfNeeded();
    await page.screenshot({ path: info.outputPath(`document-actions-catalogue-${width}.png`) });
    await guide.click();
    await expect(page.getByRole('heading', { name: 'Try document-actions from pinned source', exact: true })).toBeVisible();
    await expect(page.locator('.sl-markdown-content')).toContainText('document-actions-output/questions.md');
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: info.outputPath(`document-actions-first-use-${width}.png`) });
  }
  const map = await request.get('/llms.txt');
  expect(map.ok()).toBe(true);
  expect(await map.text()).toContain('document-actions');
});
