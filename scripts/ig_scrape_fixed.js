#!/usr/bin/env node
/*
 * Scrapes public Instagram profile photos in environments where the proxy's TLS
 * termination cannot complete a handshake with Chromium's default TLS ClientHello.
 *
 * Root cause (found 2026-08-02): Playwright's default chromium.launch() uses the
 * bundled headless_shell binary, whose modern TLS stack (QUIC/HTTP3 advertisement,
 * Encrypted Client Hello, post-quantum Kyber hybrid key exchange) the intercepting
 * proxy cannot parse, so it resets the connection (net::ERR_CONNECTION_RESET,
 * net_error -101/-202). curl and the full "chrome" binary both negotiate a plain
 * TLS 1.2 handshake fine. Fix: launch the FULL chrome binary (not headless_shell)
 * with QUIC/ECH/PostQuantumKyber disabled and TLS capped at 1.2.
 *
 * Usage: node scripts/ig_scrape_fixed.js <ig_username> > manifest.json
 * Output: JSON array of {url, alt, width, height} for images found in the profile
 * grid (feed photos are typically ~640px, highlight/profile-pic thumbnails ~150px).
 * Download each url with: curl -A "<chrome UA>" -H "Referer: https://www.instagram.com/" -o file.jpg "<url>"
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
  const username = process.argv[2];
  if (!username) {
    console.error('Usage: node ig_scrape_fixed.js <ig_username>');
    process.exit(2);
  }
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: FIX_ARGS });
  const page = await browser.newPage({ userAgent: UA });
  let ok = false;
  let lastErr = '';
  for (let i = 0; i < 4 && !ok; i++) {
    try {
      await page.goto(`https://www.instagram.com/${username}/`, { waitUntil: 'domcontentloaded', timeout: 20000 });
      ok = true;
    } catch (e) {
      lastErr = e.message.split('\n')[0];
      await new Promise((r) => setTimeout(r, 1500));
    }
  }
  if (!ok) {
    console.error('FAILED to load profile after retries:', lastErr);
    await browser.close();
    process.exit(1);
  }
  await page.waitForTimeout(5000);
  const imgs = await page.$$eval('img', (els) =>
    els
      .map((e) => ({ src: e.src, alt: e.alt, width: e.naturalWidth, height: e.naturalHeight }))
      .filter((x) => x.src.includes('cdninstagram') || x.src.includes('fbcdn'))
  );
  const title = await page.title();
  await browser.close();
  console.log(JSON.stringify({ username, title, images: imgs }, null, 2));
}

main().catch((e) => {
  console.error('ERROR:', e.message);
  process.exit(1);
});
