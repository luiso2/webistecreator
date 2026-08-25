"""Reglas compartidas para clasificar enlaces públicos de Google Maps."""

from __future__ import annotations

import re
import urllib.parse


# Directorios, redes sociales y plataformas de reservas no cuentan como website
# propio. Un sitio hospedado en Wix/Squarespace/Webflow/etc. sí cuenta: aunque use
# un subdominio de la plataforma, el negocio ya dispone de una web funcional.
PROFILE_HOSTS = frozenset({
    "facebook.com", "instagram.com", "booksy.com", "glossgenius.com", "vagaro.com",
    "fresha.com", "styleseat.com", "treatwell.com", "mindbodyonline.com", "setmore.com",
    "square.site", "squareup.com", "yelp.com", "google.com", "googleusercontent.com",
    "linktr.ee", "beacons.ai", "whatsapp.com", "wa.me", "tripadvisor.com",
    "yellowpages.com", "mapquest.com", "angi.com", "homeadvisor.com", "thumbtack.com",
    "houzz.com", "porch.com", "nextdoor.com",
})

INSTAGRAM_RESERVED_PATHS = frozenset({
    "about", "accounts", "challenge", "developer", "direct", "directory", "emails",
    "explore", "legal", "p", "press", "privacy", "reel", "reels", "stories", "terms", "tv",
})


def _clean_instagram_handle(value: str) -> str | None:
    handle = value.strip().removeprefix("@")
    if not re.fullmatch(r"[A-Za-z0-9._]{1,30}", handle):
        return None
    if handle.startswith(".") or handle.endswith(".") or ".." in handle:
        return None
    if handle.lower() in INSTAGRAM_RESERVED_PATHS:
        return None
    return handle


def instagram_handle(value: str | None) -> str | None:
    """Extrae solo un handle o una URL directa de perfil de Instagram verificable."""
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    looks_like_url = bool(re.match(
        r"^(?:https?://)?(?:[a-z0-9-]+\.)*instagram\.com/", raw, re.I
    ))
    if not looks_like_url:
        if any(marker in raw for marker in ("://", "/", "?", "#")):
            return None
        return _clean_instagram_handle(raw)
    try:
        parsed = urllib.parse.urlparse(raw if "://" in raw else f"https://{raw}")
        host = (parsed.hostname or "").lower().removeprefix("www.")
        if parsed.scheme not in {"http", "https"}:
            return None
        if host != "instagram.com" and not host.endswith(".instagram.com"):
            return None
        parts = [urllib.parse.unquote(part) for part in parsed.path.split("/") if part]
    except (TypeError, ValueError):
        return None
    if parts and parts[0].lower() == "_u":
        parts = parts[1:]
    if len(parts) != 1:
        return None
    return _clean_instagram_handle(parts[0])


def is_own_website(href: str | None) -> bool:
    """Devuelve True para cualquier website real, incluido un constructor hospedado."""
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


def safe_google_maps_url(value: str | None) -> str | None:
    """Acepta únicamente una URL HTTPS ya resuelta dentro de Google Maps."""
    if not value:
        return None
    try:
        parsed = urllib.parse.urlparse(value)
    except ValueError:
        return None
    host = (parsed.hostname or "").lower().removeprefix("www.")
    if parsed.scheme != "https" or not (host == "google.com" or host.endswith(".google.com")):
        return None
    if not parsed.path.startswith("/maps/"):
        return None
    return value[:1200]
