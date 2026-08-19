#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
function findChrome() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const root = '/opt/pw-browsers';
  for (const dir of fs.readdirSync(root)) {
    if (!dir.startsWith('chromium-')) continue;
    for (const sub of ['chrome-linux/chrome', 'chrome-linux64/chrome']) {
      const p = path.join(root, dir, sub);
      if (fs.existsSync(p)) return p;
    }
  }
}
const CHROME_PATH = findChrome();
async function main() {
  const url = process.argv[2];
  const out = process.argv[3];
  const fullPage = process.argv[4] !== 'false';
  const browser = await chromium.launch({ headless: true, executablePath: CHROME_PATH, args: ['--no-sandbox','--disable-gpu'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const msgs = [];
  page.on('console', m => msgs.push(m.text()));
  page.on('pageerror', e => msgs.push('PAGEERROR: ' + e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
  await page.waitForTimeout(1000);
  const height = await page.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < height; y += 300) {
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await page.waitForTimeout(350);
  }
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(1000);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
  await page.screenshot({ path: out, fullPage });
  console.error('CONSOLE:', JSON.stringify(msgs.slice(0, 30)));
  await browser.close();
  console.log('saved', out);
}
main().catch(e => { console.error(e); process.exit(1); });
