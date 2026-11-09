#!/usr/bin/env node
/* Custom deeper detail scrape for Anthony Tree Care: address, hours, reviews, photos. */
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
  throw new Error('No se encontro el binario de chrome (fijar CHROME_PATH)');
}

const CHROME_PATH = findChrome();
const PROXY = process.env.HTTPS_PROXY || process.env.https_proxy || '';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const FIX_ARGS = [
  '--no-sandbox', '--disable-gpu',
  ...(PROXY ? [`--proxy-server=${PROXY}`] : []),
  '--disable-quic',
  '--disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcbAlpn',
  '--ssl-version-max=tls1.2',
];

async function main() {
  const url = process.argv[2];
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 } });
  const out = { url, address: null, hours: null, reviewSamples: [], allButtons: [], photoCount: null, photoUrls: [] };
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(5000);

    // address: look at all buttons with data-item-id="address"
    out.address = await page.evaluate(() => {
      const el = document.querySelector('button[data-item-id="address"]');
      if (el) return el.getAttribute('aria-label') || el.textContent;
      return null;
    });

    // all data-item-id buttons for debugging
    out.allButtons = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('button[data-item-id], a[data-item-id]')).map(e => ({
        id: e.getAttribute('data-item-id'), label: e.getAttribute('aria-label')
      }));
    });

    // hours: click "See more hours" / open hours table
    try {
      const hoursBtn = await page.$('div[jsaction*="openhours"], button[aria-label*="hours" i]');
      if (hoursBtn) { await hoursBtn.click(); await page.waitForTimeout(800); }
    } catch (e) {}
    out.hoursTable = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll('table tr'));
      return rows.map(r => r.textContent.trim()).filter(Boolean);
    });

    // photo count text
    out.photoCountText = await page.evaluate(() => {
      const m = document.body.innerText.match(/(\d+)\s*Photos/i);
      return m ? m[0] : null;
    });

    // click photos button to open gallery
    const photoBtn = await page.$('button[aria-label*="Photo of" i]') || await page.$('button[jsaction*="heroHeaderImage"]');
    if (photoBtn) { await photoBtn.click(); await page.waitForTimeout(1500); }
    // scroll gallery a lot to load many images
    for (let i = 0; i < 25; i++) { await page.mouse.wheel(0, 2000); await page.waitForTimeout(300); }
    const imgs = await page.$$eval('img', els => els.map(e => e.src).filter(s => s && s.includes('googleusercontent')));
    const seen = new Set();
    for (const u of imgs) {
      const base = u.split('=')[0];
      if (!seen.has(base)) { seen.add(base); out.photoUrls.push(base + '=w1600-h1200-k-no'); }
    }

    // go to reviews tab
    const reviewsTab = await page.$('button[role="tab"][aria-label*="Reviews" i]');
    if (reviewsTab) {
      await reviewsTab.click();
      await page.waitForTimeout(2000);
      for (let i = 0; i < 12; i++) { await page.mouse.wheel(0, 1800); await page.waitForTimeout(500); }
      out.reviewSamples = await page.evaluate(() => {
        const nodes = Array.from(document.querySelectorAll('div[data-review-id]'));
        return nodes.map(n => {
          const author = n.querySelector('button[aria-label]')?.getAttribute('aria-label') || null;
          const allSpans = Array.from(n.querySelectorAll('span'));
          const text = allSpans.map(s => s.textContent).filter(t => t && t.length > 20).sort((a,b)=>b.length-a.length)[0] || null;
          const starEl = n.querySelector('span[role="img"][aria-label*="star" i]');
          const stars = starEl ? starEl.getAttribute('aria-label') : null;
          return { author, text, stars };
        }).filter(r => r.text);
      });
    }
  } catch (e) {
    out.error = e.message.split('\n')[0];
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}
main();
