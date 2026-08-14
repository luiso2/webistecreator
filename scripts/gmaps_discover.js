#!/usr/bin/env node
/*
 * Discovery: lista resultados de un search de Google Maps con deteccion de
 * "tiene website propio" por item (via DOM, no por texto ambiguo).
 * Uso: node scripts/gmaps_discover.js "<niche> in <city>, FL" [maxScrolls=6]
 * Output: JSON array [{name, rating, reviews, category, address, hasWebsiteButton, mapsUrl}]
 */
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
  '--no-sandbox',
  '--disable-gpu',
  ...(PROXY ? [`--proxy-server=${PROXY}`] : []),
  '--disable-quic',
  '--disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcbAlpn',
  '--ssl-version-max=tls1.2',
];

async function main() {
  const query = process.argv[2];
  const maxScrolls = parseInt(process.argv[3] || '6', 10);
  if (!query) {
    console.error('Uso: node scripts/gmaps_discover.js "<niche> in <city>, FL" [maxScrolls]');
    process.exit(2);
  }
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 } });
  const out = [];
  try {
    await page.goto(`https://www.google.com/maps/search/${encodeURIComponent(query)}`, {
      waitUntil: 'domcontentloaded',
      timeout: 25000,
    });
    await page.waitForTimeout(3000);
    const feed = await page.$('div[role="feed"]');
    if (feed) {
      for (let i = 0; i < maxScrolls; i++) {
        await page.evaluate(() => {
          const f = document.querySelector('div[role="feed"]');
          if (f) f.scrollTop = f.scrollHeight;
        });
        await page.waitForTimeout(1200);
      }
    }
    const results = await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('div[role="feed"] > div > div[jsaction]'));
      const items = [];
      const seen = new Set();
      for (const card of cards) {
        const linkEl = card.querySelector('a.hfpxzc');
        if (!linkEl) continue;
        const name = linkEl.getAttribute('aria-label') || '';
        if (!name || seen.has(name)) continue;
        seen.add(name);
        const text = card.innerText || '';
        const ratingMatch = text.match(/(\d\.\d)\(([\d,]+)\)/) || text.match(/(\d\.\d)\s*\n?\(([\d,]+)\)/);
        const websiteBtn = card.querySelector('a[aria-label^="Website:" i], a[data-value="Website"]');
        const hasWebsiteButton = !!websiteBtn;
        const websiteHref = websiteBtn ? websiteBtn.href || websiteBtn.getAttribute('aria-label') : null;
        items.push({
          name,
          mapsUrl: linkEl.href,
          rating: ratingMatch ? ratingMatch[1] : null,
          reviews: ratingMatch ? ratingMatch[2].replace(/,/g, '') : null,
          hasWebsiteButton,
          websiteHref,
          rawText: text.slice(0, 300),
        });
      }
      return items;
    });
    out.push(...results);
  } catch (e) {
    console.error('ERROR', e.message);
  }
  await browser.close();
  console.log(JSON.stringify({ query, count: out.length, results: out }, null, 1));
}

main();
