#!/usr/bin/env python3
"""Build an adapted v2 demo from a Google Maps data.json.

Direct-name queue items do not always have Instagram. This builder keeps the same
tested skeleton and uses Google Maps as the public proof/contact channel instead of
inventing an Instagram handle or a booking flow.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / "contenido_script.py").exists():
    sys.path.insert(0, str(ROOT))
else:
    sys.path.insert(0, str(ROOT / "railway-forge"))
from contenido_script import construir  # noqa: E402


def bilingual(es: str, en: str | None = None) -> dict:
    return {"es": es, "en": en or es}


def walk_replace(value, replacements):
    if isinstance(value, str):
        for old, new in replacements:
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [walk_replace(x, replacements) for x in value]
    if isinstance(value, dict):
        return {k: walk_replace(v, replacements) for k, v in value.items()}
    return value


def main(slug: str):
    root = ROOT / "output" / slug
    data = json.loads((root / "data.json").read_text(encoding="utf-8"))
    photos = data.get("fotos", [])
    if len(photos) < 5:
        # The builder is deliberately strict. A caller may provide additional verified
        # listing photos, but it must never silently fill a gallery with invented assets.
        raise SystemExit(f"need at least 5 verified photos, got {len(photos)}")
    selected = {"hero": photos[0], "nosotros": [photos[1], photos[2]],
                "galeria": (photos[3:9] + photos[1:3])[:6],
                "contacto": photos[1], "logo": photos[0]}
    name = data.get("name") or slug.replace("-", " ").title()
    city = "Hialeah, FL"
    address = data.get("address") or city
    phone = data.get("phone")
    maps_url = data.get("maps_url") or f"https://www.google.com/maps/search/{name.replace(' ', '+')}+{city.replace(' ', '+')}"
    # Niche detection uses the public name/query only. No fake social handle is passed.
    facts = {**data, "slug": slug, "nombre": name, "ciudad": city,
             "nicho": name, "ig": slug, "idioma_principal": "en",
             "has_own_site": bool(data.get("website"))}
    content, _dm, _nicho = construir(facts, selected)
    replacements = [
        ("Instagram", "Google Maps"),
        ("instagram", "maps"),
        ("@" + slug, "Google Maps"),
        (f"https://www.google.com/maps/search/{slug}/", maps_url),
        (f"https://www.instagram.com/{slug}/", maps_url),
        (f"https://ig.me/m/{slug}", f"tel:+{re.sub(r'\\D', '', phone or '')}" if phone else maps_url),
    ]
    content = walk_replace(content, replacements)
    # Facts that the generic social template cannot infer.
    content["lang"] = "en"
    content["cta_url"] = f"tel:+{re.sub(r'\D', '', phone)}" if phone else maps_url
    content["cta_icono"] = "telefono" if phone else "mapa"
    content["cta_label"] = bilingual("Llamar ahora" if phone else "Ver en Google Maps", "Call now" if phone else "See us on Google Maps")
    content["ig_url"] = maps_url
    content["ig_handle"] = "Google Maps"
    content["social_label"] = "Google Maps"
    content["social_cta"] = bilingual("Ver ficha en Google Maps", "See listing on Google Maps")
    content["brand"]["name"] = name
    content["brand"]["footmark"] = name
    content["head"]["title"] = f"{name} · {city}"
    content["head"]["description"] = f"{name}: servicios locales en {city}. Información, fotos y contacto verificados en Google Maps."
    content["head"]["og_title"] = f"{name} · {city}"
    content["head"]["og_description"] = f"{name} en {city}. Fotos públicas y contacto directo."
    content["jsonld"].update({
        "name": name, "description": f"{name}, negocio local en {city}.",
        "sameAs": [maps_url], "image": f"assets/raw/{photos[0]}",
        "address": {"@type": "PostalAddress", "streetAddress": address, "addressLocality": "Hialeah", "addressRegion": "FL", "addressCountry": "US"},
    })
    if phone:
        content["jsonld"]["telephone"] = phone
    if data.get("rating") and data.get("reviews"):
        content["jsonld"]["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": str(data["rating"]), "reviewCount": str(data["reviews"])}
        content["hero"]["rating"] = bilingual(f"{data['rating']} · {data['reviews']} reseñas en Google", f"{data['rating']} · {data['reviews']} reviews on Google")
        content["strip"][0] = {"valor": str(data["rating"]), "count": str(data["rating"]), "etiqueta": bilingual("Calificación en Google", "Google rating")}
        content["strip"][1] = {"valor": str(data["reviews"]), "count": str(data["reviews"]), "etiqueta": bilingual("Reseñas en Google", "Google reviews")}
    content["hero"]["senal_icono"] = "mapa"
    content["hero"]["senal"] = bilingual("Ficha pública en Google Maps", "Public Google Maps listing")
    content["hero"]["parrafo"] = bilingual(
        f"{name} atiende a clientes en {city}. Consulta la ficha pública, mira las fotos reales y contacta directamente.",
        f"{name} serves customers in {city}. Check the public listing, see real photos and contact the business directly.")
    content["hero"]["tarjeta"]["destacado"] = phone or "Google Maps"
    content["hero"]["tarjeta"]["pie"] = bilingual(city, city)
    # No Instagram claims in the adapted non-beauty variant.
    content["nosotros"]["parrafo_2"] = bilingual(
        "La ficha pública de Google Maps reúne las fotos y la información de contacto disponibles.",
        "The public Google Maps listing collects the available photos and contact information.")
    content["social_proof"]["subtitulo"] = bilingual(
        "No publicamos reseñas que no podamos respaldar. Estas razones se basan en el oficio y la información visible en la ficha.",
        "We do not publish reviews we cannot back up. These reasons use the trade and information visible on the listing.")
    content["social_proof"]["cta"] = bilingual("Ver ficha y fotos en Google Maps", "See listing and photos on Google Maps")
    for item in content["social_proof"]["items"]:
        item["texto"] = walk_replace(item["texto"], [("feed", "ficha pública"), ("Instagram", "Google Maps")])
    content["contacto"]["h2_a"] = bilingual("Visítanos desde", "Reach us from")
    content["contacto"]["h2_shine"] = "Hialeah"
    content["contacto"]["cards"] = ([{
        "icono": "telefono", "titulo": bilingual("Teléfono", "Phone"),
        "texto": bilingual("La vía más rápida para consultar disponibilidad.", "The fastest way to ask about availability."),
        "url": content["cta_url"], "enlace": phone,
    }] if phone else []) + [{
        "icono": "mapa", "titulo": bilingual("Google Maps", "Google Maps"),
        "texto": bilingual(f"Dirección pública: {address}.", f"Public address: {address}."),
        "url": maps_url, "enlace": "Ver ficha pública" if not phone else address,
    }]
    content["footer"]["descripcion"] = bilingual(f"{name} en {city}. Información pública y contacto directo.", f"{name} in {city}. Public information and direct contact.")
    content["footer"]["linea_contacto"] = address
    content["footer"]["enlace_contacto"] = bilingual(f"Teléfono · {phone}" if phone else "Google Maps", f"Phone · {phone}" if phone else "Google Maps")
    (root / "content.json").write_text(json.dumps(content, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.copy(ROOT / "templates" / ".assetsignore-template", root / ".assetsignore")
    print(json.dumps({"slug": slug, "name": name, "niche": _nicho, "photos": photos}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: build_maps_site.py <slug>")
    main(sys.argv[1])
