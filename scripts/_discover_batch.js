#!/usr/bin/env node
/* Batch discovery: multiple niche+location queries in one browser session.
 * Input: JSON array on argv[1] (path to file) [{niche, location}]
 * Output: JSON {combo: [{name,mapsUrl,rating,reviews,hasWebsiteButton,websiteHref,address,phone}]}
 * Filters: rating>=minRating, reviews>=minReviews, hasWebsiteButton=false.
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
  throw new Error('No chrome binary found');
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

const MIN_RATING = parseFloat(process.env.MIN_RATING || '4.5');
const MIN_REVIEWS = parseInt(process.env.MIN_REVIEWS || '10', 10);

async function searchOne(page, niche, location) {
  const query = `${niche} in ${location}`;
  await page.goto(`https://www.google.com/maps/search/${encodeURIComponent(query)}`, {
    waitUntil: 'domcontentloaded', timeout: 25000,
  });
  await page.waitForTimeout(2800);
  const feed = await page.$('div[role="feed"]');
  if (feed) {
    for (let i = 0; i < 5; i++) {
      await page.evaluate(() => { const f = document.querySelector('div[role="feed"]'); if (f) f.scrollTop = f.scrollHeight; });
      await page.waitForTimeout(1000);
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
      const phoneMatch = text.match(/\+1\s?\d{3}[-\s]?\d{3}[-\s]?\d{4}/);
      items.push({
        name,
        mapsUrl: linkEl.href,
        rating: ratingMatch ? ratingMatch[1] : null,
        reviews: ratingMatch ? ratingMatch[2].replace(/,/g, '') : null,
        hasWebsiteButton: !!websiteBtn,
        websiteHref: websiteBtn ? (websiteBtn.href || null) : null,
        phone: phoneMatch ? phoneMatch[0] : null,
        rawText: text.slice(0, 260),
      });
    }
    return items;
  });
  return results;
}

async function main() {
  const inputFile = process.argv[2];
  if (!inputFile) { console.error('Uso: node _discover_batch.js <combos.json>'); process.exit(2); }
  const combos = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 }, locale: 'en-US' });
  const out = {};
  for (const combo of combos) {
    const key = `${combo.niche} | ${combo.location}`;
    try {
      const raw = await searchOne(page, combo.niche, combo.location);
      const filtered = raw.filter(r => {
        if (r.hasWebsiteButton) return false;
        const rating = parseFloat(r.rating);
        const reviews = parseInt(r.reviews, 10);
        if (!rating || isNaN(reviews)) return false;
        return rating >= MIN_RATING && reviews >= MIN_REVIEWS;
      }).map(r => ({ ...r, niche: combo.niche, location: combo.location }));
      out[key] = filtered;
      process.stderr.write(`OK ${key}: ${raw.length} raw, ${filtered.length} no-website candidates\n`);
    } catch (e) {
      out[key] = { error: e.message };
      process.stderr.write(`ERR ${key}: ${e.message}\n`);
    }
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}

main();
