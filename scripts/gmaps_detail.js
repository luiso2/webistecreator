#!/usr/bin/env node
/*
 * Abre la ficha individual de Google Maps (por mapsUrl exacto) y extrae:
 * rating, reviews count, phone, address, hours, website (si tiene), fotos, y
 * hasta 8 reseñas verbatim (autor + texto + idioma aproximado).
 * Uso: node scripts/gmaps_detail.js "<mapsUrl>"
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
  '--no-sandbox', '--disable-gpu',
  ...(PROXY ? [`--proxy-server=${PROXY}`] : []),
  '--disable-quic',
  '--disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcbAlpn',
  '--ssl-version-max=tls1.2',
];

async function main() {
  const url = process.argv[2];
  if (!url) { console.error('Uso: node scripts/gmaps_detail.js "<mapsUrl>"'); process.exit(2); }
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 } });
  const out = { url, name: null, rating: null, reviews: null, category: null, address: null,
    phone: null, hours: null, website: null, photos: [], reviewSamples: [] };
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(4500);
    let bodyText = await page.evaluate(() => document.body.innerText);
    if (!/\d\.\d/.test(bodyText)) {
      await page.waitForTimeout(2500);
      bodyText = await page.evaluate(() => document.body.innerText);
    }
    out.rawSnippet = bodyText.slice(0, 900);
    // scroll el panel lateral (main) para forzar el render de secciones lazy (resenas, hours, mentions)
    await page.evaluate(() => {
      const main = document.querySelector('div[role="main"]');
      if (main) main.scrollTop = 400;
    });
    await page.waitForTimeout(1200);

    out.name = await page.evaluate(() => {
      const h1 = document.querySelector('h1');
      return h1 ? h1.textContent.trim() : null;
    });
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
    const serviceMentions = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('[aria-label*="mentioned in" i]'))
        .map(e => e.getAttribute('aria-label')).slice(0, 12);
    });
    out.serviceMentions = serviceMentions;
    const hoursAria = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('[aria-label*="Copy open hours" i], [aria-label*="Copy closed hours" i]'))
        .map(e => e.getAttribute('aria-label').replace(/, Copy (open|closed) hours/i, ''));
    });
    out.hours = hoursAria;
    const websiteEl = await page.$('a[aria-label^="Website:" i], a[data-item-id="authority"]');
    out.website = websiteEl ? (await websiteEl.getAttribute('href')) : null;
    const phoneEl = await page.$('button[aria-label^="Phone:" i]');
    out.phone = phoneEl ? (await phoneEl.getAttribute('aria-label')).replace(/^Phone:\s*/i, '').trim() : null;
    const addrEl = await page.$('button[aria-label^="Address:" i]');
    out.address = addrEl ? (await addrEl.getAttribute('aria-label')).replace(/^Address:\s*/i, '').trim() : null;
    if (/permanently closed/i.test(bodyText)) out.status = 'PERMANENTLY_CLOSED';

    // fotos
    await page.evaluate(() => {
      const btn = document.querySelector('button[aria-label*="Photo of" i]') ||
        document.querySelector('div[jsaction*="heroHeaderImage"] img');
      if (btn) btn.click();
    });
    await page.waitForTimeout(1500);
    for (let i = 0; i < 5; i++) { await page.mouse.wheel(0, 1600); await page.waitForTimeout(400); }
    const imgs = await page.$$eval('img', els => els.map(e => e.src).filter(s => s && s.includes('googleusercontent')));
    const seen = new Set();
    for (const u of imgs) {
      const base = u.split('=')[0];
      if (!seen.has(base)) { seen.add(base); out.photos.push(base + '=w1600-h1200-k-no'); }
    }
    // intentar abrir pestana de resenas desde la pagina actual
    const reviewsTab = await page.$('button[role="tab"][aria-label*="Reviews" i]');
    if (reviewsTab) {
      await reviewsTab.click();
      await page.waitForTimeout(1800);
      for (let i = 0; i < 5; i++) { await page.mouse.wheel(0, 1600); await page.waitForTimeout(500); }
      out.reviewSamples = await page.evaluate(() => {
        const nodes = Array.from(document.querySelectorAll('div[data-review-id]'));
        return nodes.slice(0, 12).map(n => {
          const author = n.querySelector('button[aria-label]')?.getAttribute('aria-label') || null;
          const allSpans = Array.from(n.querySelectorAll('span'));
          const text = allSpans.map(s => s.textContent).filter(t => t && t.length > 25).sort((a,b)=>b.length-a.length)[0] || null;
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
