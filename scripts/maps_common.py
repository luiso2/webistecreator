"""Reglas compartidas para clasificar enlaces públicos de Google Maps."""

from __future__ import annotations

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
