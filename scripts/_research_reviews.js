#!/usr/bin/env node
/* Solo resenas verbatim de una ficha de Google Maps (carga limpia, sin pasar por fotos). */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

function findChrome() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  if (fs.existsSync('/opt/pw-browsers/chromium')) return '/opt/pw-browsers/chromium';
  const root = '/opt/pw-browsers';
  if (fs.existsSync(root)) {
    for (const dir of fs.readdirSync(root)) {
      if (!dir.startsWith('chromium-')) continue;
      for (const sub of ['chrome-linux/chrome', 'chrome-linux64/chrome']) {
        const p = path.join(root, dir, sub);
        if (fs.existsSync(p)) return p;
      }
    }
  }
  throw new Error('No se encontro el binario de chrome');
}
const CHROME_PATH = findChrome();
const PROXY = process.env.HTTPS_PROXY || process.env.https_proxy || '';
const FIX_ARGS = ['--no-sandbox', '--disable-gpu', ...(PROXY ? [`--proxy-server=${PROXY}`] : []),
  '--disable-quic', '--disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcbAlpn', '--ssl-version-max=tls1.2'];

async function main() {
  const url = process.argv[2];
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36', locale: 'en-US', viewport: { width: 1400, height: 1000 } });
  let out = { reviewSamples: [] };
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(2200);
    const reviewsTab = await page.$('button[role="tab"][aria-label*="Reviews" i]');
    if (reviewsTab) {
      await reviewsTab.click();
      await page.waitForTimeout(1800);
      for (let i = 0; i < 8; i++) { await page.mouse.wheel(0, 1700); await page.waitForTimeout(450); }
      out.reviewSamples = await page.evaluate(() => {
        const nodes = Array.from(document.querySelectorAll('div[data-review-id]'));
        return nodes.map(n => {
          const author = n.querySelector('button[aria-label]')?.getAttribute('aria-label') || null;
          const allSpans = Array.from(n.querySelectorAll('span'));
          const text = allSpans.map(s => s.textContent).filter(t => t && t.length > 25).sort((a, b) => b.length - a.length)[0] || null;
          const starEl = n.querySelector('span[role="img"][aria-label*="star" i]');
          const stars = starEl ? starEl.getAttribute('aria-label') : null;
          return { author, text, stars };
        }).filter(r => r.text);
      });
    }
  } catch (e) { out.error = e.message.split('\n')[0]; }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}
main();
