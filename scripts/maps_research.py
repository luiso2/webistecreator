#!/usr/bin/env python3
"""Research a direct-name queue item on live Google Maps and save local assets.

This is the name-input counterpart to research_ig.py. It uses the full Chrome binary
with the TLS flags required by the local proxy, records only data visible in the
public Maps listing, and downloads the listing's own public photos.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from playwright.sync_api import sync_playwright
from maps_common import is_own_website, safe_google_maps_url

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
CHROME = (os.environ.get("CHROME_PATH") or shutil.which("chromium") or
          shutil.which("chromium-browser") or shutil.which("google-chrome") or
          ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
           if os.path.exists("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") else None))
PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
ARGS = [
    "--no-sandbox", "--disable-gpu", "--disable-quic",
    "--disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcb",
    "--ssl-version-max=tls1.2",
]
if PROXY:
    ARGS.append(f"--proxy-server={PROXY}")

def slugify(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:64]


def clean_label(value: str | None, prefix: str) -> str | None:
    if not value:
        return None
    return re.sub(rf"^{re.escape(prefix)}\s*", "", value, flags=re.I).strip()


def research(query: str, out_slug: str, maps_url: str | None = None) -> dict:
    out = {"query": query, "name": None, "rating": None, "reviews": None,
           "address": None, "phone": None, "hours": [], "website": None,
           "photos": [], "reviewSamples": [], "maps_url": None}
    with sync_playwright() as pw:
        launch_args = {"headless": True, "args": ARGS}
        if CHROME:
            launch_args["executable_path"] = CHROME
        browser = pw.chromium.launch(**launch_args)
        page = browser.new_page(user_agent=UA, viewport={"width": 1400, "height": 1000})
        exact_url = safe_google_maps_url(maps_url)
        if maps_url and not exact_url:
            raise ValueError("maps_url no pertenece a Google Maps")
        if exact_url:
            # El descubridor ya abrió y verificó esta ficha. Reutilizar la URL exacta
            # evita otra búsqueda por nombre, ambigüedad y dos esperas de interfaz.
            page.goto(exact_url, wait_until="domcontentloaded", timeout=35000)
            page.wait_for_timeout(1200)
        else:
            page.goto("https://www.google.com/maps/search/" + urllib.parse.quote(query),
                      wait_until="domcontentloaded", timeout=35000)
            page.wait_for_timeout(2200)
            first = page.locator("a.hfpxzc").first
            if first.count():
                try:
                    first.scroll_into_view_if_needed(timeout=3000)
                    first.click(timeout=8000)
                except Exception:
                    # Maps can keep a hidden result in the DOM while the feed settles.
                    # Navigate to its href rather than aborting the whole research.
                    href = first.get_attribute("href")
                    if href:
                        page.goto(urllib.parse.urljoin("https://www.google.com", href),
                                  wait_until="domcontentloaded", timeout=35000)
                page.wait_for_timeout(2200)
        out["maps_url"] = page.url
        title = page.locator("h1").first.text_content() if page.locator("h1").count() else None
        # Google Maps puede dejar "Results" como h1 cuando la ficha se abrió
        # desde una búsqueda automatizada. Nunca propagamos ese título genérico
        # al demo: usamos el nombre solicitado como fallback verificable.
        fallback_name = query.split(',', 1)[0].strip().replace('-', ' ')
        title_text = (title or '').strip()
        if not title_text or title_text.lower() in {'results', 'google maps'}:
            title_text = fallback_name
        out["name"] = title_text
        # aria labels are more stable than Maps' class names.
        labels = page.locator('[role="img"][aria-label]')
        for i in range(min(labels.count(), 120)):
            label = labels.nth(i).get_attribute("aria-label") or ""
            if re.fullmatch(r"\d\.\d\s*stars?", label, re.I):
                out["rating"] = label.split()[0]
            elif re.fullmatch(r"[\d,]+\s*reviews?", label, re.I):
                out["reviews"] = re.sub(r"\D", "", label.split()[0])
        body = page.locator("body").inner_text()
        out["status"] = "PERMANENTLY_CLOSED" if re.search(r"permanently closed", body, re.I) else None
        for selector, key, prefix in [
            ('button[aria-label^="Phone:" i]', "phone", "Phone:"),
            ('button[aria-label^="Address:" i]', "address", "Address:"),
        ]:
            el = page.locator(selector).first
            if el.count():
                out[key] = clean_label(el.get_attribute("aria-label"), prefix)
        for selector in ['a[aria-label^="Website:" i]', 'a[data-item-id="authority"]']:
            el = page.locator(selector).first
            if el.count():
                out["website"] = el.get_attribute("href")
                break
        out["hours"] = page.locator('[aria-label*="Copy open hours" i], [aria-label*="Copy closed hours" i]').evaluate_all(
            "els => els.map(e => e.getAttribute('aria-label').replace(/, Copy (open|closed) hours/i, ''))"
        )
        # Open the public photo gallery, then gather canonical googleusercontent URLs.
        # Maps cambia el botón y los atributos de las imágenes con frecuencia. Capturar
        # src/srcset/data-src antes y después del click evita que un cambio de markup
        # convierta una ficha construible en "0 fotos".
        image_urls = page.locator("img").evaluate_all(
            """els => els.flatMap(e => [e.currentSrc, e.src, e.getAttribute('data-src'),
              ...(e.getAttribute('srcset') || '').split(',').map(x => x.trim().split(' ')[0])])
              .filter(Boolean)"""
        )
        btn = page.locator(
            'button[aria-label*="Photo of" i], button[aria-label*="See photos" i], '
            'button:has-text("See photos"), div[jsaction*="heroHeaderImage"] img, '
            'img[src*="googleusercontent.com"]'
        ).first
        if btn.count():
            try:
                btn.click(timeout=5000)
                page.wait_for_timeout(800)
                for _ in range(5):
                    page.mouse.wheel(0, 1600)
                    page.wait_for_timeout(220)
            except Exception:
                pass
        image_urls.extend(page.locator("img").evaluate_all(
            """els => els.flatMap(e => [e.currentSrc, e.src, e.getAttribute('data-src'),
              ...(e.getAttribute('srcset') || '').split(',').map(x => x.trim().split(' ')[0])])
              .filter(Boolean)"""
        ))
        seen = set()
        for url in image_urls:
            if 'googleusercontent.com' not in url:
                continue
            base = url.split("=")[0]
            if base not in seen and not any(x in base for x in ('/maps/api/', '/maps/vt/')):
                seen.add(base)
                out["photos"].append(base + "=w1600-h1200-k-no")
        # Review snippets are not used by the Maps template. Skip the extra tab
        # navigation on the fast path; opt in only for a debugging run.
        if os.environ.get("MAPS_INCLUDE_REVIEWS", "").lower() in {"1", "true", "yes"}:
            tab = page.locator('button[role="tab"][aria-label*="Reviews" i]').first
            if tab.count():
                try:
                    tab.scroll_into_view_if_needed(timeout=1800)
                    tab.click(timeout=3500)
                    page.wait_for_timeout(700)
                    out["reviewSamples"] = page.locator("div[data-review-id]").evaluate_all(
                        "els => els.slice(0, 8).map(n => ({author:n.querySelector('button[aria-label]')?.getAttribute('aria-label')||null, text:Array.from(n.querySelectorAll('span')).map(s=>s.textContent).filter(t=>t&&t.length>25).sort((a,b)=>b.length-a.length)[0]||null})).filter(x=>x.text)"
                    )
                except Exception:
                    out["reviewSamples"] = []
        browser.close()
    root = Path("output") / out_slug
    raw = root / "assets" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    downloaded = []
    def download_photo(entry):
        i, url = entry
        name = f"gmaps-{i}.jpg"
        target = raw / name
        try:
            # Las fotos son independientes: descargarlas en paralelo evita que
            # una URL lenta bloquee toda la galería.
            subprocess.run(["curl", "-L", "--fail", "--retry", "1", "--connect-timeout", "12",
                            "--max-time", "30", "-A", UA, "-e", "https://www.google.com/maps/",
                            "-o", str(target), url], check=False, timeout=35,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if target.exists() and target.stat().st_size > 15000:
                return name
            target.unlink(missing_ok=True)
        except Exception as exc:
            print(f"photo {i}: {exc}", file=sys.stderr)
        return None

    with ThreadPoolExecutor(max_workers=6) as pool:
        for name in pool.map(download_photo, list(enumerate(out["photos"][:16], 1))):
            if name:
                downloaded.append(name)
    out["fotos"] = downloaded
    out["has_own_site"] = is_own_website(out.get("website"))
    out["slug"] = out_slug
    (root / "data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("slug")
    parser.add_argument("--maps-url")
    args = parser.parse_args()
    result = research(args.query, args.slug, maps_url=args.maps_url)
    print(json.dumps({k: result.get(k) for k in ("name", "rating", "reviews", "address", "phone", "website", "maps_url", "fotos", "status")}, ensure_ascii=False, indent=1))
