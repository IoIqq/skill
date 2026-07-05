const { chromium } = require('playwright');
const TARGET_URL = 'http://localhost:3001';
const USERNAME = 'admin';
const PASSWORD = 'ShengSheng@2026';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1200 } });
  await page.goto(TARGET_URL, { waitUntil: 'networkidle' });
  await page.fill('input[name="username"]', USERNAME);
  await page.fill('input[name="password"]', PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForSelector('#workspace-shell.is-ready');
  await page.click('.nav-chip[data-view="media"]');
  await page.waitForSelector('.workspace-panel[data-panel="media"].active');
  const grid = await page.locator('#media-grid').boundingBox();
  const first = await page.locator('#media-grid .media-card').first().boundingBox();
  const second = await page.locator('#media-grid .media-card').nth(1).boundingBox();
  console.log(JSON.stringify({ grid, first, second }, null, 2));
  await browser.close();
})();
