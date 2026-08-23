#!/usr/bin/env python3
"""Descubre negocios locales con Google Maps, sin construir ni enviar outreach.

El descubrimiento es deliberadamente conservador: solo devuelve fichas que
parecen coincidir con el nicho, tienen señales de demanda/contacto y no exponen
un website propio. La construcción y la validación de fotos ocurren después en
la forja de Railway.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright
try:
    # `cron.py` importa este archivo como `scripts.maps_discover`.
    from .maps_common import is_own_website
except ImportError:  # ejecución directa: python scripts/maps_discover.py
    from maps_common import is_own_website

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
CHROME = (
    os.environ.get("CHROME_PATH")
    or shutil.which("chromium")
    or shutil.which("chromium-browser")
    or shutil.which("google-chrome")
)
ARGS = [
    "--no-sandbox",
    "--disable-gpu",
    "--disable-quic",
    "--disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcb",
    "--ssl-version-max=tls1.2",
]
if os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"):
    ARGS.append(f"--proxy-server={os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')}")

def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:64]


def _number(value: str | None, suffix: str | None = None) -> int | None:
    if not value:
        return None
    normalized = value.replace(",", "").strip()
    try:
        number = float(normalized)
    except ValueError:
        digits = re.sub(r"\D", "", normalized)
        return int(digits) if digits else None
    multiplier = {"k": 1_000, "m": 1_000_000}.get((suffix or "").lower(), 1)
    return int(number * multiplier)


def _parse_rating_reviews(labels: list[str]) -> tuple[float | None, int | None]:
    """Extrae valores tanto de labels separadas como de la label combinada de Maps."""
    rating = None
    reviews = None
    for label in labels:
        rating_match = re.search(r"(?<!\d)([0-5](?:[.,]\d)?)\s*(?:stars?|estrellas?)", label, re.I)
        if rating_match and rating is None:
            rating = float(rating_match.group(1).replace(",", "."))
        reviews_match = re.search(
            r"([\d,.]+)\s*([km])?\s*(?:Google\s+)?(?:reviews?|rese(?:n|ñ)as?)",
            label,
            re.I,
        )
        if reviews_match and reviews is None:
            reviews = _number(reviews_match.group(1), reviews_match.group(2))
    return rating, reviews


def _rating_reviews(page) -> tuple[float | None, int | None]:
    values = []
    labels = page.locator('[aria-label]')
    for i in range(min(labels.count(), 160)):
        values.append(labels.nth(i).get_attribute("aria-label") or "")
    return _parse_rating_reviews(values)


def _first_attr(page, selectors: list[str], attr: str) -> str | None:
    for selector in selectors:
        locator = page.locator(selector).first
        if locator.count():
            value = locator.get_attribute(attr)
            if value:
                return value.strip()
    return None


def _detail(
    page,
    href: str,
    fallback_name: str,
    location: str,
    niche: str,
    min_rating: float,
    min_reviews: int,
) -> dict | None:
    try:
        page.goto(href, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(1800)
    except Exception:
        return None

    body = page.locator("body").inner_text(timeout=6000)
    if re.search(r"permanently closed", body, re.I):
        return None
    title_locator = page.locator("h1").first
    title = title_locator.text_content() if title_locator.count() else None
    title_text = (title or '').strip()
    # Maps puede usar "Results" como h1 al abrir una ficha desde una búsqueda
    # automatizada. Nunca convertimos ese texto genérico en el nombre del negocio.
    if not title_text or title_text.lower() in {'results', 'google maps'}:
        title_text = fallback_name
    name = title_text.strip()
    if not name:
        return None
    rating, reviews = _rating_reviews(page)
    if rating is None or reviews is None:
        summary = re.search(r"\b([0-5](?:[.,]\d))\s*\n\s*\(?([\d,]+)\)?", body[:4000])
        if summary:
            rating = rating if rating is not None else float(summary.group(1).replace(",", "."))
            reviews = reviews if reviews is not None else _number(summary.group(2))
    website = _first_attr(
        page,
        ['a[aria-label^="Website:" i]', 'a[data-item-id="authority"]'],
        "href",
    )
    address = _first_attr(page, ['button[aria-label^="Address:" i]'], "aria-label")
    phone = _first_attr(page, ['button[aria-label^="Phone:" i]'], "aria-label")
    address = re.sub(r"^Address:\s*", "", address or "", flags=re.I).strip() or None
    phone = re.sub(r"^Phone:\s*", "", phone or "", flags=re.I).strip() or None
    if is_own_website(website):
        return None
    # Si Maps no expone estas señales no podemos justificar que el candidato
    # tenga demanda suficiente; es mejor dejarlo para otra búsqueda que crear
    # un demo de baja calidad por datos incompletos.
    if rating is None or reviews is None:
        return None
    if rating < min_rating:
        return None
    if reviews < min_reviews:
        return None
    score = 4.0  # no website propio es la condición principal
    if rating is not None:
        score += min(rating - 4.0, 1.0) * 3
    if reviews is not None:
        score += min(reviews / 100.0, 2.0)
    if phone:
        score += 1.5
    if address:
        score += 1.0
    terms = set(re.findall(r"[a-z0-9]+", niche.lower()))
    name_terms = set(re.findall(r"[a-z0-9]+", name.lower()))
    score += min(len(terms & name_terms), 2) * 0.5
    return {
        "name": name,
        "slug": slugify(name),
        "location": location,
        "niche": niche,
        "maps_url": page.url,
        "website": None,
        "profile_url": website,
        "address": address,
        "phone": phone,
        "rating": rating,
        "reviews": reviews,
        "score": round(score, 3),
    }


def discover(
    niche: str,
    location: str,
    limit: int = 20,
    min_rating: float = 4.5,
    min_reviews: int = 10,
) -> list[dict]:
    query = f"{niche} in {location}"
    candidates: list[tuple[str, str]] = []
    seen_urls: set[str] = set()
    with sync_playwright() as pw:
        launch = {"headless": True, "args": ARGS}
        if CHROME:
            launch["executable_path"] = CHROME
        browser = pw.chromium.launch(**launch)
        search = browser.new_page(
            user_agent=UA,
            locale="en-US",
            viewport={"width": 1400, "height": 1000},
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        try:
            search_urls = [
                "https://www.google.com/maps/search/" + urllib.parse.quote(query) + "?hl=en",
                "https://www.google.com/maps/search/?api=1&hl=en&query=" + urllib.parse.quote_plus(query),
            ]
            for search_url in search_urls:
                search.goto(search_url, wait_until="domcontentloaded", timeout=25000)
                try:
                    search.locator('a.hfpxzc, a[href*="/maps/place/"]').first.wait_for(
                        state="attached", timeout=6500
                    )
                except PlaywrightTimeoutError:
                    continue
                feed = search.locator('div[role="feed"]').first
                if feed.count():
                    for _ in range(2):
                        feed.evaluate("node => { node.scrollTop = node.scrollHeight; }")
                        search.wait_for_timeout(450)
                links = search.locator("a.hfpxzc")
                if not links.count():
                    links = search.locator('a[href*="/maps/place/"]')
                for i in range(min(links.count(), limit * 3)):
                    link = links.nth(i)
                    href = link.get_attribute("href")
                    if not href:
                        continue
                    href = urllib.parse.urljoin("https://www.google.com", href)
                    if href in seen_urls:
                        continue
                    seen_urls.add(href)
                    label = link.get_attribute("aria-label") or ""
                    if not label:
                        try:
                            label = link.locator("xpath=..").inner_text(timeout=1000).splitlines()[0]
                        except Exception:
                            label = ""
                    candidates.append((href, label.strip()))
                if candidates:
                    break

            detail = browser.new_page(
                user_agent=UA,
                locale="en-US",
                viewport={"width": 1400, "height": 1000},
                extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
            )
            results: list[dict] = []
            seen_names: set[str] = set()
            for href, label in candidates:
                item = _detail(detail, href, label, location, niche, min_rating, min_reviews)
                if not item:
                    continue
                key = re.sub(r"[^a-z0-9]", "", item["name"].lower())
                if key in seen_names:
                    continue
                seen_names.add(key)
                results.append(item)
                if len(results) >= limit:
                    break
            results.sort(key=lambda x: x["score"], reverse=True)
            return results
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--min-rating", type=float, default=4.5)
    parser.add_argument("--min-reviews", type=int, default=10)
    args = parser.parse_args()
    try:
        results = discover(
            args.niche,
            args.location,
            max(1, min(args.limit, 50)),
            max(0, min(args.min_rating, 5)),
            max(0, args.min_reviews),
        )
    except (PlaywrightTimeoutError, OSError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc), "results": []}, ensure_ascii=False))
        raise SystemExit(2)
    print(json.dumps({"query": f"{args.niche} in {args.location}", "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
