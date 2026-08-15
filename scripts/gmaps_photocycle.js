#!/usr/bin/env node
/*
 * Abre el visor de fotos de una ficha de Google Maps y lo recorre con ArrowRight
 * para sacar TODAS las fotos del negocio (no solo la principal, que es lo maximo
 * que gmaps_detail.js consigue en la vista sin sesion).
 * Uso: node scripts/gmaps_photocycle.js "<mapsUrl>" [maxSteps=20]
 * Output: JSON { count, photos: [url] }
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
  const maxSteps = parseInt(process.argv[3] || '20', 10);
  if (!url) { console.error('Uso: node scripts/gmaps_photocycle.js "<mapsUrl>" [maxSteps]'); process.exit(2); }
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 } });
  const seen = new Set();
  const out = [];
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(4000);
    await page.evaluate(() => {
      const btn = document.querySelector('button[aria-label*="Photo of" i]') ||
        document.querySelector('div[jsaction*="heroHeaderImage"] img') ||
        document.querySelector('button[jsaction*="heroHeaderImage"]');
      if (btn) btn.click();
    });
    await page.waitForTimeout(2000);

    const grab = async () => {
      const imgs = await page.$$eval('img', els => els.map(e => e.src).filter(s => s && s.includes('googleusercontent')));
      for (const u of imgs) {
        const base = u.split('=')[0];
        if (!seen.has(base)) { seen.add(base); out.push(base + '=w1600-h1200-k-no'); }
      }
    };
    await grab();
    for (let i = 0; i < maxSteps; i++) {
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(700);
      await grab();
    }
  } catch (e) {
    console.error('ERROR', e.message);
  }
  await browser.close();
  console.log(JSON.stringify({ count: out.length, photos: out }, null, 1));
}

main();
