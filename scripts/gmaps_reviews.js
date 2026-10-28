#!/usr/bin/env node
/*
 * Abre la pestana de reviews de una ficha de Google Maps y extrae autor + texto + estrellas
 * de hasta N resenas reales, con scroll para forzar el lazy-load.
 * Uso: node scripts/gmaps_reviews.js "<mapsUrl>" [max=12]
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
  const max = parseInt(process.argv[3] || '12', 10);
  if (!url) { console.error('Uso: node scripts/gmaps_reviews.js "<mapsUrl>" [max]'); process.exit(2); }
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, locale: 'en-US', viewport: { width: 1400, height: 1000 } });
  const out = { url, reviews: [] };
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2500);
    // boton de pestana "Reviews" (varios markups posibles)
    const tab = await page.$('button[aria-label*="Reviews" i]') || await page.$('button:has-text("Reviews")');
    if (tab) {
      await tab.click();
      await page.waitForTimeout(1800);
    }
    // el panel de resenas vive dentro de un div role=feed o similar; hacer scroll del panel
    for (let i = 0; i < 10; i++) {
      await page.mouse.wheel(0, 1800);
      await page.waitForTimeout(450);
    }
    await page.waitForTimeout(800);
    out.reviews = await page.evaluate((maxN) => {
      const nodes = Array.from(document.querySelectorAll('div[data-review-id]'));
      return nodes.slice(0, maxN).map(n => {
        const authorBtn = n.querySelector('button[aria-label]');
        const author = authorBtn ? authorBtn.getAttribute('aria-label') : null;
        const starEl = n.querySelector('span[role="img"][aria-label*="star" i]') || n.querySelector('[aria-label*="stars" i]');
        const stars = starEl ? starEl.getAttribute('aria-label') : null;
        const spans = Array.from(n.querySelectorAll('span'));
        const text = spans.map(s => s.textContent).filter(t => t && t.length > 20 && !/^\d/.test(t)).sort((a, b) => b.length - a.length)[0] || null;
        return { author, stars, text };
      }).filter(r => r.text);
    }, max);
  } catch (e) {
    out.error = e.message.split('\n')[0];
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}
main();
