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
  const out = { photoUrls: [], clicked: null };
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(5000);
    // find the element with text matching "NNN Photos" and click it to open the full gallery grid
    const clicked = await page.evaluate(() => {
      const all = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
      const el = all.find(e => /\d+\s*Photos?$/i.test((e.textContent || '').trim()));
      if (el) { el.click(); return el.textContent.trim(); }
      return null;
    });
    out.clicked = clicked;
    await page.waitForTimeout(2500);
    out.urlAfterClick = page.url();

    // from the street-view-like image viewer, click "See more photos" to get the real grid gallery
    const smp = await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button[aria-label]')).find(b => b.getAttribute('aria-label') === 'See more photos');
      if (btn) { btn.click(); return true; }
      return false;
    });
    out.seeMorePhotosClicked = smp;
    await page.waitForTimeout(2000);
    // dismiss the "Sign-in to get the best of Google Maps" modal if it appears
    const dismissed = await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => (b.textContent || '').trim() === 'Dismiss');
      if (btn) { btn.click(); return true; }
      return false;
    });
    out.dismissed = dismissed;
    await page.waitForTimeout(800);

    const seen = new Set();
    function collect() {
      return page.evaluate(() => {
        const out = [];
        document.querySelectorAll('img').forEach(e => { if (e.src && e.src.includes('googleusercontent')) out.push(e.src); });
        document.querySelectorAll('*').forEach(e => {
          const bg = getComputedStyle(e).backgroundImage;
          if (bg && bg.includes('googleusercontent')) {
            const m = bg.match(/url\("?(https:\/\/[^")]+)"?\)/);
            if (m) out.push(m[1]);
          }
        });
        return out;
      });
    }
    out.nextClicks = 0;
    // scroll the left thumbnail sidebar (mouse positioned over it) to lazy-load many thumbnails
    await page.mouse.move(115, 400);
    for (let i = 0; i < 80; i++) {
      await page.mouse.wheel(0, 1400);
      await page.waitForTimeout(230);
      const found = await collect();
      for (const u of found) {
        const base = u.split('=')[0];
        if (!seen.has(base)) { seen.add(base); out.photoUrls.push(base + '=w1200-h1200-k-no'); }
      }
      if (i === 20 || i === 60) await page.screenshot({ path: `/tmp/claude-0/anthony_scroll_${i}.png` });
    }
    out.debugAllImgSrcCount = await page.evaluate(() => document.querySelectorAll('img').length);
    out.scrollableFound = await page.evaluate(() => {
      const els = Array.from(document.querySelectorAll('div'));
      const scrollable = els.filter(e => e.scrollHeight > e.clientHeight + 50 && e.clientHeight > 200);
      return scrollable.length;
    });
  } catch (e) { out.error = e.message.split('\n')[0]; }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}
main();
