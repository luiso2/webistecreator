#!/usr/bin/env node
/* Research completo de UNA ficha de Google Maps a partir de su URL (de maps_discover.py).
   Uso: node scripts/_research_place.js "<maps_url>"

   v2 (2026-11-18): fix de fotos. El boton "N Photos" abre un LIGHTBOX de una sola foto
   (modo panoramico !3m8!1e2...), no el grid: el codigo viejo scrolleaba el body y solo
   encontraba las 2 imagenes que ya estaban en el DOM (hero + 1 thumbnail), SIEMPRE las
   mismas sin importar el negocio. El fix usa el boton "Next photo" del lightbox para
   recorrer la galeria real. Tambien dedupea reviews por data-review-id (antes se repetia
   el primer nodo) y expande "See more" antes de leer el texto para no cortar la cita. */
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
  if (!url) { console.error('Uso: node scripts/_research_place.js "<maps_url>"'); process.exit(2); }
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, locale: 'en-US', viewport: { width: 1400, height: 1000 } });
  const out = { url, name: null, rating: null, reviews: null, address: null, phone: null,
    hours: [], website: null, photos: [], reviewSamples: [] };
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(2500);
    out.name = await page.evaluate(() => { const h1 = document.querySelector('h1'); return h1 ? h1.textContent.trim() : null; });
    const rr = await page.evaluate(() => {
      const imgEls = Array.from(document.querySelectorAll('[role="img"][aria-label]'));
      const starEl = imgEls.find(e => /^\d\.\d\s*stars?\s*$/i.test(e.getAttribute('aria-label') || ''));
      const revEl = imgEls.find(e => /^\d[\d,]*\s*reviews?$/i.test(e.getAttribute('aria-label') || ''));
      return {
        rating: starEl ? starEl.getAttribute('aria-label').match(/[\d.]+/)[0] : null,
        reviews: revEl ? revEl.getAttribute('aria-label').match(/[\d,]+/)[0].replace(/,/g, '') : null,
      };
    });
    out.rating = rr.rating; out.reviews = rr.reviews;
    const websiteEl = await page.$('a[aria-label^="Website:" i], a[data-item-id="authority"]');
    out.website = websiteEl ? (await websiteEl.getAttribute('href')) : null;
    const phoneEl = await page.$('button[aria-label^="Phone:" i]');
    out.phone = phoneEl ? (await phoneEl.getAttribute('aria-label')).replace(/^Phone:\s*/i, '').trim() : null;
    const addrEl = await page.$('button[aria-label^="Address:" i]');
    out.address = addrEl ? (await addrEl.getAttribute('aria-label')).replace(/^Address:\s*/i, '').trim() : null;
    const hoursAria = await page.evaluate(() => Array.from(document.querySelectorAll('[aria-label*="Copy open hours" i], [aria-label*="Copy closed hours" i]')).map(e => e.getAttribute('aria-label').replace(/, Copy (open|closed) hours/i, '')));
    out.hours = hoursAria;

    // FOTOS: abrir el boton "N Photos" (lightbox de 1 foto), recorrer con "Next photo".
    const photoBtn = await page.locator('button:has-text("Photos")').first();
    if (await photoBtn.count()) {
      await photoBtn.click({ force: true }).catch(() => {});
      await page.waitForTimeout(2200);
      const nextBtn = page.locator('button[aria-label*="Next" i]').first();
      const seen = new Set();
      for (let i = 0; i < 24; i++) {
        const imgs = await page.$$eval('img', els => els.map(e => e.src).filter(s => s && s.includes('googleusercontent')));
        for (const u of imgs) { const base = u.split('=')[0]; if (!seen.has(base)) { seen.add(base); out.photos.push(base + '=w1600-h1200-k-no'); } }
        if (await nextBtn.count()) { await nextBtn.click({ force: true }).catch(() => {}); await page.waitForTimeout(550); } else break;
      }
      // volver a la URL original (goBack puede quedar atrapado en el historial del lightbox)
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 }).catch(() => {});
      await page.waitForTimeout(1500);
    }

    const reviewsTab = await page.$('button[role="tab"][aria-label*="Reviews" i]');
    if (reviewsTab) {
      await reviewsTab.click().catch(() => {});
      await page.waitForTimeout(1800);
      for (let i = 0; i < 16; i++) { await page.mouse.wheel(0, 1700); await page.waitForTimeout(500); }
      await page.evaluate(() => {
        document.querySelectorAll('button[aria-label="See more"], button.w8nwRe').forEach(b => { try { b.click(); } catch (e) {} });
      });
      await page.waitForTimeout(800);
      out.reviewSamples = await page.evaluate(() => {
        const nodes = Array.from(document.querySelectorAll('div[data-review-id]'));
        const byId = new Map();
        for (const n of nodes) {
          const id = n.getAttribute('data-review-id');
          if (byId.has(id)) continue;
          const author = n.querySelector('button[aria-label]')?.getAttribute('aria-label') || null;
          const allSpans = Array.from(n.querySelectorAll('span'));
          const text = allSpans.map(s => s.textContent).filter(t => t && t.length > 25).sort((a, b) => b.length - a.length)[0] || null;
          const starEl = n.querySelector('span[role="img"][aria-label*="star" i]');
          const stars = starEl ? starEl.getAttribute('aria-label') : null;
          if (text) byId.set(id, { author, text, stars });
        }
        return Array.from(byId.values()).slice(0, 20);
      });
    }
  } catch (e) {
    out.error = e.message.split('\n')[0];
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}
main();
