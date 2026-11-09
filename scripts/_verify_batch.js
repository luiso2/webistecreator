#!/usr/bin/env node
/* Verifica en detalle (ficha individual, no lista) si cada candidato tiene website propio.
 * Input: JSON array en argv[1] (path) [{name, mapsUrl, niche, location, rating, reviews, phone}]
 * Output: mismo array + {verified_website, verified_has_own_site, verified_address, verified_phone}
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

const PROFILE_HOSTS = new Set(['facebook.com','instagram.com','booksy.com','glossgenius.com','vagaro.com',
  'fresha.com','styleseat.com','treatwell.com','mindbodyonline.com','setmore.com','square.site','squareup.com',
  'yelp.com','google.com','googleusercontent.com','linktr.ee','beacons.ai','whatsapp.com','wa.me',
  'tripadvisor.com','yellowpages.com','mapquest.com','angi.com','homeadvisor.com','thumbtack.com','houzz.com',
  'porch.com','nextdoor.com']);

function isOwnWebsite(href) {
  if (!href) return false;
  try {
    const u = new URL(href.includes('://') ? href : `https://${href}`);
    let host = u.hostname.toLowerCase();
    if (host.startsWith('www.')) host = host.slice(4);
    if (!host) return true;
    for (const p of PROFILE_HOSTS) {
      if (host === p || host.endsWith(`.${p}`)) return false;
    }
    return true;
  } catch (e) { return true; }
}

async function verifyOne(page, item) {
  await page.goto(item.mapsUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(1800);
  const website = await page.evaluate(() => {
    const sels = ['a[aria-label^="Website:" i]', 'a[data-item-id="authority"]'];
    for (const s of sels) {
      const el = document.querySelector(s);
      if (el) return el.href || null;
    }
    return null;
  });
  const address = await page.evaluate(() => {
    const el = document.querySelector('button[aria-label^="Address:" i]');
    return el ? el.getAttribute('aria-label').replace(/^Address:\s*/i, '') : null;
  });
  const phone = await page.evaluate(() => {
    const el = document.querySelector('button[aria-label^="Phone:" i]');
    return el ? el.getAttribute('aria-label').replace(/^Phone:\s*/i, '') : null;
  });
  const bodyText = await page.locator('body').innerText().catch(() => '');
  const permanentlyClosed = /permanently closed/i.test(bodyText);
  return {
    verified_website: website,
    verified_has_own_site: isOwnWebsite(website),
    verified_address: address,
    verified_phone: phone,
    permanently_closed: permanentlyClosed,
  };
}

async function main() {
  const inputFile = process.argv[2];
  if (!inputFile) { console.error('Uso: node _verify_batch.js <candidates.json>'); process.exit(2); }
  const items = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA, viewport: { width: 1400, height: 1000 }, locale: 'en-US' });
  const out = [];
  for (const item of items) {
    try {
      const v = await verifyOne(page, item);
      out.push({ ...item, ...v });
      process.stderr.write(`${v.verified_has_own_site ? 'HAS-SITE' : 'OK-no-site'} ${item.name}\n`);
    } catch (e) {
      out.push({ ...item, verify_error: e.message });
      process.stderr.write(`ERR ${item.name}: ${e.message}\n`);
    }
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
}

main();
