const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:8000';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();
  const issues = [];
  const warnings = [];

  // Capture console errors
  page.on('console', msg => {
    if (msg.type() === 'error') issues.push(`[JS Error] ${msg.text()}`);
    if (msg.type() === 'warning') warnings.push(`[JS Warning] ${msg.text()}`);
  });

  // Capture failed requests
  page.on('requestfailed', req => {
    issues.push(`[Failed Request] ${req.url()} - ${req.failure()?.errorText}`);
  });

  console.log('🔍 Loading page...');
  await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 15000 });
  console.log('✅ Page title:', await page.title());

  // Screenshot - Desktop
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.screenshot({ path: 'C:/tmp/desktop.png', fullPage: true });
  console.log('📸 Desktop screenshot saved');

  // Screenshot - Mobile
  await page.setViewportSize({ width: 375, height: 667 });
  await page.screenshot({ path: 'C:/tmp/mobile.png', fullPage: true });
  console.log('📸 Mobile screenshot saved');

  // Reset to desktop for checks
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto(TARGET_URL, { waitUntil: 'networkidle' });

  // Check images without alt text
  const imagesWithoutAlt = await page.$$eval('img', imgs =>
    imgs.filter(img => !img.alt || img.alt.trim() === '').map(img => img.src)
  );
  if (imagesWithoutAlt.length > 0) {
    warnings.push(`[Accessibility] ${imagesWithoutAlt.length} image(s) missing alt text: ${imagesWithoutAlt.slice(0, 3).join(', ')}`);
  }

  // Check for broken images
  const brokenImages = await page.$$eval('img', imgs =>
    imgs.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src)
  );
  brokenImages.forEach(src => issues.push(`[Broken Image] ${src}`));

  // Check for empty links
  const emptyLinks = await page.$$eval('a', links =>
    links.filter(a => !a.href || a.href === '#' || a.href === window.location.href + '#').map(a => a.textContent.trim() || '[no text]')
  );
  if (emptyLinks.length > 0) {
    warnings.push(`[Links] ${emptyLinks.length} link(s) with no destination: ${emptyLinks.slice(0, 3).join(', ')}`);
  }

  // Check meta tags
  const metaDesc = await page.$eval('meta[name="description"]', el => el.content).catch(() => null);
  if (!metaDesc) warnings.push('[SEO] Missing <meta name="description">');

  const titleTag = await page.title();
  if (!titleTag || titleTag.trim() === '') warnings.push('[SEO] Missing or empty <title> tag');

  // Check viewport meta
  const viewportMeta = await page.$('meta[name="viewport"]').catch(() => null);
  if (!viewportMeta) warnings.push('[Mobile] Missing <meta name="viewport">');

  // Check for mixed content (http resources on page)
  const httpResources = await page.evaluate(() => {
    const resources = performance.getEntriesByType('resource');
    return resources.filter(r => r.name.startsWith('http://')).map(r => r.name);
  });
  httpResources.forEach(url => warnings.push(`[Security] HTTP resource loaded: ${url}`));

  // Check forms have labels
  const unlabeledInputs = await page.$$eval('input:not([type="hidden"]):not([type="submit"]):not([type="button"])', inputs =>
    inputs.filter(input => {
      const id = input.id;
      const hasLabel = id && document.querySelector(`label[for="${id}"]`);
      const hasAriaLabel = input.getAttribute('aria-label') || input.getAttribute('aria-labelledby');
      const hasPlaceholder = input.placeholder;
      return !hasLabel && !hasAriaLabel && !hasPlaceholder;
    }).length
  );
  if (unlabeledInputs > 0) {
    warnings.push(`[Accessibility] ${unlabeledInputs} form input(s) without labels`);
  }

  // Check internal links on the page
  const links = await page.$$eval('a[href]', as => 
    as.map(a => a.href).filter(href => href.startsWith(window.location.origin) && !href.includes('#'))
  );
  const uniqueLinks = [...new Set(links)];
  console.log(`\n🔗 Checking ${uniqueLinks.length} internal link(s)...`);
  for (const link of uniqueLinks.slice(0, 10)) {
    try {
      const resp = await page.request.get(link, { timeout: 5000 });
      if (!resp.ok()) issues.push(`[Broken Link] ${link} returned ${resp.status()}`);
    } catch (e) {
      issues.push(`[Broken Link] ${link} - ${e.message}`);
    }
  }

  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('📋 AUDIT REPORT');
  console.log('='.repeat(50));

  if (issues.length === 0 && warnings.length === 0) {
    console.log('🎉 No issues found! Website looks good to publish.');
  } else {
    if (issues.length > 0) {
      console.log(`\n❌ ISSUES (${issues.length}) - Must fix before publishing:`);
      issues.forEach(i => console.log('  • ' + i));
    }
    if (warnings.length > 0) {
      console.log(`\n⚠️  WARNINGS (${warnings.length}) - Recommended to fix:`);
      warnings.forEach(w => console.log('  • ' + w));
    }
  }

  console.log('\n📸 Screenshots saved:');
  console.log('  • Desktop: C:/tmp/desktop.png');
  console.log('  • Mobile:  C:/tmp/mobile.png');

  await browser.close();
})();
