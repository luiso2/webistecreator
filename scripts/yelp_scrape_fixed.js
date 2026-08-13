#!/usr/bin/env node
/* Scrapes a public Yelp business page for photo URLs, business hours, and review text,
 * using the same TLS-fix launch pattern as ig_scrape_fixed.js (proxy sandbox issue).
 * Usage: node scripts/yelp_scrape_fixed.js <yelp_biz_url>
 */
const { chromium } = require('playwright');

const CHROME_PATH = process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1234/chrome-linux64/chrome';
const PROXY = process.env.HTTPS_PROXY || process.env.https_proxy || '';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';

const FIX_ARGS = [
  '--no-sandbox',
  '--disable-gpu',
  ...(PROXY ? [`--proxy-server=${PROXY}`] : []),
  '--disable-quic',
  '--disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcbAlpn',
  '--ssl-version-max=tls1.2',
  '--disable-blink-features=AutomationControlled',
];

async function main() {
  const url = process.argv[2];
  if (!url) {
    console.error('Usage: node yelp_scrape_fixed.js <yelp_biz_url>');
    process.exit(2);
  }
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1280, height: 2400 } });
  let ok = false;
  let lastErr = '';
  for (let i = 0; i < 4 && !ok; i++) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
      ok = true;
    } catch (e) {
      lastErr = e.message.split('\n')[0];
      await new Promise((r) => setTimeout(r, 1500));
    }
  }
  if (!ok) {
    console.error('FAILED to load page after retries:', lastErr);
    await browser.close();
    process.exit(1);
  }
  try {
    for (let i = 0; i < 6; i++) {
      await page.mouse.move(200 + i * 50, 300 + i * 30, { steps: 10 });
      await page.waitForTimeout(1500);
      await page.mouse.wheel(0, 200);
      await page.waitForTimeout(1500);
    }
  } catch (e) {}
  await page.waitForTimeout(8000);
  const title = await page.title();
  const bodyText = await page.evaluate(() => document.body.innerText);
  const imgs = await page.$$eval('img', (els) =>
    els.map((e) => ({ src: e.src, alt: e.alt, width: e.naturalWidth, height: e.naturalHeight }))
  );
  await browser.close();
  console.log(JSON.stringify({ url, title, bodyTextLen: bodyText.length, bodyText, images: imgs }, null, 2));
}

main().catch((e) => {
  console.error('ERROR:', e.message);
  process.exit(1);
});
