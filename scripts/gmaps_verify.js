#!/usr/bin/env node
/*
 * Verifica en vivo una ficha de Google Maps: rating, resenas, website declarado y fotos.
 *
 * POR QUE (2026-08-14): las corridas anteriores daban por bloqueado Google Maps (SPA solo-JS,
 * curl/WebFetch no lo renderizan) y se apoyaban en espejos de terceros (Birdeye, agregadores)
 * para rating/resenas. Esos espejos a veces desincronizan: en esta corrida encontramos un
 * negocio que Birdeye reportaba 4.9/29 resenas y en Google Maps EN VIVO resulto tener 3.7 y
 * "Permanently closed". Este script aplica el mismo fix de TLS que scripts/ig_scrape_fixed.js
 * (el proxy de la sandbox no completa el handshake QUIC/ECH del chromium headless_shell por
 * defecto; lanzar el binario "chrome" completo con QUIC/ECH/Kyber desactivados y TLS 1.2 si
 * funciona) para renderizar Maps de verdad.
 *
 * Uso: node scripts/gmaps_verify.js "<nombre negocio, ciudad FL>" > resultado.json
 * Output: { query, title, ratingLive, reviewCountLive, statusLine, websiteOnMaps, photos[] }
 *
 * Limitaciones conocidas:
 * - La busqueda por texto libre puede aterrizar en una lista de resultados cercanos en vez
 *   del panel de un solo negocio si el nombre no matchea exacto: revisar "title" y "rawSnippet"
 *   antes de confiar en el resultado. Buscar con nombre + calle exacta ayuda a evitar esto.
 * - El panel de Maps SIN sesion iniciada normalmente muestra como maximo la foto principal del
 *   negocio (no el album completo): si el negocio no subio ninguna foto propia y no tiene
 *   fotos de resenas, photos[] queda vacio o con 1 solo elemento (senal real de "sin fotos en
 *   Google", no un fallo del script: el propio panel muestra "Add a photo" / "Add photos &amp;
 *   videos" en ese caso, visible en rawSnippet).
 * - "websiteOnMaps" con un dominio que NO resuelve via curl es el caso "website propio roto"
 *   de FORGE-BRIEF (el negocio SI reclamo un dominio, aunque no cargue): tratar como
 *   has_own_site true, angulo "su web no esta cargando", NO como candidato sin website.
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
  if (!query) {
    console.error('Uso: node scripts/gmaps_verify.js "<nombre negocio, ciudad FL>"');
    process.exit(2);
  }
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 } });
  const out = { query, title: null, ratingLive: null, reviewCountLive: null, statusLine: null, websiteOnMaps: null, photos: [] };
  try {
    await page.goto(`https://www.google.com/maps/search/${encodeURIComponent(query)}`, {
      waitUntil: 'domcontentloaded',
      timeout: 25000,
    });
    await page.waitForTimeout(3500);
    const firstResult = await page.$('a.hfpxzc');
    if (firstResult) {
      await firstResult.click();
      await page.waitForTimeout(3000);
    }
    out.resolvedUrl = page.url();
    out.title = await page.title();
    const bodyText = await page.evaluate(() => document.body.innerText);
    out.rawSnippet = bodyText.slice(0, 700);

    const rm = bodyText.match(/(\d\.\d)\s*\(([\d,]+)\)/);
    if (rm) {
      out.ratingLive = rm[1];
      out.reviewCountLive = rm[2];
    }
    if (/Permanently closed/i.test(bodyText)) out.statusLine = 'PERMANENTLY_CLOSED';
    else if (/Temporarily closed/i.test(bodyText)) out.statusLine = 'TEMPORARILY_CLOSED';
    else if (/\bClosed ·|\bOpen ·|\bOpen 24 hours/i.test(bodyText)) out.statusLine = 'OPEN_LISTED';

    const websiteMatch = bodyText.match(/\n([a-z0-9-]+\.[a-z]{2,}(?:\.[a-z]{2,})?)\n/i);
    if (websiteMatch && !/google\.com|business\.site/i.test(websiteMatch[1])) out.websiteOnMaps = websiteMatch[1];

    await page.evaluate(() => {
      const btn =
        document.querySelector('button[aria-label*="Photo of"]') ||
        document.querySelector('button[jsaction*="heroHeaderImage"]') ||
        document.querySelector('div[jsaction*="heroHeaderImage"] img');
      if (btn) btn.click();
    });
    await page.waitForTimeout(2000);
    for (let i = 0; i < 6; i++) {
      await page.mouse.wheel(0, 1800);
      await page.waitForTimeout(500);
    }
    const imgs = await page.$$eval('img', (els) => els.map((e) => e.src).filter((s) => s && s.includes('googleusercontent')));
    const seen = new Set();
    for (const u of imgs) {
      const base = u.split('=')[0];
      if (!seen.has(base)) {
        seen.add(base);
        out.photos.push(base + '=w1200-h900-k-no');
      }
    }
  } catch (e) {
    out.error = e.message.split('\n')[0];
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}

main();
