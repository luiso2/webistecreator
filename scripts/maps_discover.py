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

# Estos perfiles sí pueden aparecer enlazados como "Website" en Google Maps,
# pero no son un sitio propio del negocio. Dejarlos pasar mantiene el filtro
# alineado con el panel: Booksy/Facebook/Instagram/WhatsApp no cuentan como web.
PROFILE_HOSTS = {
    "facebook.com", "instagram.com", "booksy.com", "glossgenius.com", "vagaro.com",
    "fresha.com", "styleseat.com", "treatwell.com", "mindbodyonline.com", "setmore.com",
    "square.site", "squareup.com", "yelp.com", "google.com", "googleusercontent.com",
    "linktr.ee", "beacons.ai", "whatsapp.com", "wa.me", "tripadvisor.com",
    "yellowpages.com", "mapquest.com", "angi.com", "homeadvisor.com", "thumbtack.com",
    "houzz.com", "porch.com", "nextdoor.com", "wixsite.com", "wix.com", "squarespace.com",
    "weebly.com", "wordpress.com", "webflow.io", "godaddysites.com", "my.canva.site",
}


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:64]


def _number(value: str | None) -> int | None:
    if not value:
        return None
    digits = re.sub(r"\D", "", value)
    return int(digits) if digits else None


def is_own_website(href: str | None) -> bool:
    """True only for a normal domain owned by the business, not a profile page."""
    if not href:
        return False
    try:
        parsed = urllib.parse.urlparse(href if "://" in href else f"https://{href}")
        host = (parsed.hostname or "").lower().removeprefix("www.")
    except ValueError:
        return True
    if not host:
        return True
    return not any(host == profile or host.endswith(f".{profile}") for profile in PROFILE_HOSTS)


def _rating_reviews(page) -> tuple[float | None, int | None]:
    rating = None
    reviews = None
    labels = page.locator('[role="img"][aria-label]')
    for i in range(min(labels.count(), 160)):
        label = labels.nth(i).get_attribute("aria-label") or ""
        match = re.fullmatch(r"(\d(?:\.\d)?)\s*stars?", label, re.I)
        if match:
            rating = float(match.group(1))
        match = re.fullmatch(r"([\d,]+)\s*reviews?", label, re.I)
        if match:
            reviews = _number(match.group(1))
    return rating, reviews


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
    name = (title or fallback_name).strip()
    if not name:
        return None
    rating, reviews = _rating_reviews(page)
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
        search = browser.new_page(user_agent=UA, viewport={"width": 1400, "height": 1000})
        try:
            search.goto(
                "https://www.google.com/maps/search/" + urllib.parse.quote(query),
                wait_until="domcontentloaded",
                timeout=25000,
            )
            search.wait_for_timeout(2200)
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

            detail = browser.new_page(user_agent=UA, viewport={"width": 1400, "height": 1000})
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
