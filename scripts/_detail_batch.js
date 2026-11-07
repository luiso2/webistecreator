#!/usr/bin/env node
/* Batch detail scrape: multiple Maps place URLs in one browser session.
 * Input: JSON array on argv[1] (file) [{name, mapsUrl, niche, location, rating, reviews, phone}]
 * Output: JSON array with full detail (address, phone, hours, website, photos, reviewSamples) per item.
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

async function detailOne(page, url) {
  const out = { name: null, rating: null, reviews: null, address: null,
    phone: null, hours: [], website: null, photos: [], reviewSamples: [] };
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
  await page.waitForTimeout(2600);
  out.resolvedUrl = page.url();
  out.name = await page.evaluate(() => { const h1 = document.querySelector('h1'); return h1 ? h1.textContent.trim() : null; });
  const ratingReviews = await page.evaluate(() => {
    const imgEls = Array.from(document.querySelectorAll('[role="img"][aria-label]'));
    const starEl = imgEls.find(e => /^\d\.\d\s*stars?\s*$/i.test(e.getAttribute('aria-label') || ''));
    const revEl = imgEls.find(e => /^\d[\d,]*\s*reviews?$/i.test(e.getAttribute('aria-label') || ''));
    return {
      rating: starEl ? starEl.getAttribute('aria-label').match(/[\d.]+/)[0] : null,
      reviews: revEl ? revEl.getAttribute('aria-label').match(/[\d,]+/)[0].replace(/,/g, '') : null,
    };
  });
  out.rating = ratingReviews.rating;
  out.reviews = ratingReviews.reviews;
  out.hours = await page.evaluate(() => Array.from(document.querySelectorAll('[aria-label*="Copy open hours" i], [aria-label*="Copy closed hours" i]')).map(e => e.getAttribute('aria-label').replace(/, Copy (open|closed) hours/i, '')));
  const websiteEl = await page.$('a[aria-label^="Website:" i], a[data-item-id="authority"]');
  out.website = websiteEl ? (await websiteEl.getAttribute('href')) : null;
  const phoneEl = await page.$('button[aria-label^="Phone:" i]');
  out.phone = phoneEl ? (await phoneEl.getAttribute('aria-label')).replace(/^Phone:\s*/i, '').trim() : null;
  const addrEl = await page.$('button[aria-label^="Address:" i]');
  out.address = addrEl ? (await addrEl.getAttribute('aria-label')).replace(/^Address:\s*/i, '').trim() : null;
  const bodyText = await page.evaluate(() => document.body.innerText);
  if (/permanently closed/i.test(bodyText)) out.status = 'PERMANENTLY_CLOSED';

  const seen = new Set();
  const grab = async () => {
    const imgs = await page.$$eval('img', els => els.map(e => e.src).filter(s => s && s.includes('googleusercontent')));
    for (const u of imgs) { const base = u.split('=')[0]; if (!seen.has(base)) { seen.add(base); out.photos.push(base + '=w1600-h1200-k-no'); } }
  };
  await page.evaluate(() => {
    const btn = document.querySelector('button[aria-label*="Photo of" i]') ||
      document.querySelector('div[jsaction*="heroHeaderImage"] img') ||
      document.querySelector('button[jsaction*="heroHeaderImage"]');
    if (btn) btn.click();
  });
  await page.waitForTimeout(1500);
  await grab();
  for (let i = 0; i < 18; i++) {
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(450);
    await grab();
  }
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);

  const reviewsTab = await page.$('button[role="tab"][aria-label*="Reviews" i]');
  if (reviewsTab) {
    await reviewsTab.click();
    await page.waitForTimeout(1500);
    const scrollable = await page.evaluateHandle(() => {
      const candidates = Array.from(document.querySelectorAll('div[role="main"] div'));
      return candidates.find(d => d.scrollHeight > d.clientHeight + 200 && d.clientHeight > 300) || null;
    });
    for (let i = 0; i < 8; i++) {
      try { await page.evaluate(el => { if (el) el.scrollTop += 1200; }, scrollable); } catch (e) {}
      await page.waitForTimeout(450);
    }
    out.reviewSamples = await page.evaluate(() => {
      const nodes = Array.from(document.querySelectorAll('div[data-review-id]'));
      return nodes.slice(0, 12).map(n => {
        const author = n.querySelector('button[aria-label]')?.getAttribute('aria-label') || null;
        const allSpans = Array.from(n.querySelectorAll('span'));
        const text = allSpans.map(s => s.textContent).filter(t => t && t.length > 20).sort((a,b)=>b.length-a.length)[0] || null;
        const starEl = n.querySelector('span[role="img"][aria-label*="star" i]');
        const stars = starEl ? starEl.getAttribute('aria-label') : null;
        return { author, text, stars };
      }).filter(r => r.text);
    });
  }
  return out;
}

async function main() {
  const inputFile = process.argv[2];
  if (!inputFile) { console.error('Uso: node _detail_batch.js <items.json>'); process.exit(2); }
  const items = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 }, locale: 'en-US', extraHTTPHeaders: { 'Accept-Language': 'en-US,en;q=0.9' } });
  const out = [];
  for (const item of items) {
    try {
      const detail = await detailOne(page, item.mapsUrl);
      out.push({ ...item, detail });
      process.stderr.write(`OK ${item.name}: photos=${detail.photos.length} reviews=${detail.reviewSamples.length} addr=${detail.address ? 'y' : 'n'} website=${detail.website || 'none'}\n`);
    } catch (e) {
      out.push({ ...item, detail: null, error: e.message });
      process.stderr.write(`ERR ${item.name}: ${e.message}\n`);
    }
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}

main();
