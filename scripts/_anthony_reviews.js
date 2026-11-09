#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

function findChrome() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
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
  throw new Error('no chrome');
}
const CHROME_PATH = findChrome();
const PROXY = process.env.HTTPS_PROXY || process.env.https_proxy || '';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const FIX_ARGS = ['--no-sandbox', '--disable-gpu', ...(PROXY ? [`--proxy-server=${PROXY}`] : []),
  '--disable-quic', '--disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcbAlpn', '--ssl-version-max=tls1.2'];

async function main() {
  const url = process.argv[2];
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 } });
  const out = { reviewSamples: [] };
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(5000);
    const reviewsTab = await page.$('button[role="tab"][aria-label*="Reviews" i]');
    if (reviewsTab) {
      await reviewsTab.click();
      await page.waitForTimeout(2500);
      for (let i = 0; i < 15; i++) { await page.mouse.wheel(0, 2000); await page.waitForTimeout(600); }
      // expand all truncated reviews
      await page.evaluate(() => {
        Array.from(document.querySelectorAll('button')).forEach(b => {
          if (/^More$/i.test((b.textContent || '').trim())) b.click();
        });
      });
      await page.waitForTimeout(800);
      out.reviewSamples = await page.evaluate(() => {
        const nodes = Array.from(document.querySelectorAll('div[data-review-id]'));
        return nodes.map(n => {
          const author = n.querySelector('button[aria-label]')?.getAttribute('aria-label') || null;
          const allSpans = Array.from(n.querySelectorAll('span'));
          const text = allSpans.map(s => s.textContent).filter(t => t && t.length > 20).sort((a,b)=>b.length-a.length)[0] || null;
          const starEl = n.querySelector('span[role="img"][aria-label*="star" i]');
          const stars = starEl ? starEl.getAttribute('aria-label') : null;
          const time = Array.from(n.querySelectorAll('span')).map(s=>s.textContent).find(t => /ago$/.test(t));
          return { author, text, stars, time };
        }).filter(r => r.text);
      });
    } else {
      out.noTab = true;
    }
  } catch (e) { out.error = e.message.split('\n')[0]; }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}
main();
