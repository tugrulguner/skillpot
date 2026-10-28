import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/browser',
  fullyParallel: false,
  workers: 1,
  timeout: 30000,
  outputDir: 'test-results',
  reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:4587', headless: true, trace: 'retain-on-failure' },
  webServer: { command: 'npm run preview -- --port 4587', url: 'http://127.0.0.1:4587', reuseExistingServer: false, timeout: 30000 },
});
