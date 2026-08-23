#!/usr/bin/env python3
"""Job corto para Railway: descubre candidatos y arranca hasta N forjas.

Railway Cron debe terminar al completar el trabajo. El worker permanente
(`main.py`) puede seguir procesando la misma cola; el claim atómico evita que
ambos construyan el mismo negocio.
"""
from __future__ import annotations

import base64
import json
import os
import re
import time
import urllib.error
from pathlib import Path

import main as forge
from scripts.maps_discover import discover


ROOT = Path(__file__).resolve().parent
CONFIG_PATHS = [ROOT / "config.json", ROOT.parent / "config.json"]
# Railway ya tenía instalaciones antiguas con PANEL_KEY; aceptar ambos nombres
# evita que el descubrimiento automático se quede silenciosamente desactivado.
PANEL_KEY = (os.environ.get("SITEFORGE_UI_KEY") or os.environ.get("PANEL_KEY") or "").strip()


def _int_env(name: str, default: int, minimum: int = 0, maximum: int = 100) -> int:
    try:
        value = int(os.environ.get(name, str(default)))
    except (TypeError, ValueError):
        value = default
    return max(minimum, min(value, maximum))


DISCOVERY_TARGET = _int_env("DISCOVERY_TARGET", 12, minimum=1, maximum=20)
DISCOVERY_CANDIDATES = _int_env("DISCOVERY_CANDIDATES", 50, minimum=5, maximum=50)
CRON_MAX_BUILDS = _int_env("CRON_MAX_BUILDS", 1, minimum=0, maximum=3)
DISCOVERY_ROTATION_MINUTES = _int_env("DISCOVERY_ROTATION_MINUTES", 15, minimum=5, maximum=360)


def _config() -> dict:
    for path in CONFIG_PATHS:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    return {}


def _lists(config: dict) -> tuple[list[str], list[str]]:
    niches = []
    override_niches = os.environ.get("DISCOVERY_NICHES", "").strip()
    if override_niches:
        niches = [x.strip() for x in override_niches.split(",") if x.strip()]
    else:
        if config.get("niche"):
            niches.append(str(config["niche"]))
        niches.extend(str(x) for x in config.get("fallback_niches", []) if x)
    locations = []
    override_locations = os.environ.get("DISCOVERY_LOCATIONS", "").strip()
    if override_locations:
        locations = [x.strip() for x in override_locations.split(",") if x.strip()]
    else:
        locations.extend(str(x) for x in config.get("extra_areas", []) if x)
        if config.get("city"):
            locations.insert(0, str(config["city"]))
    if not niches:
        niches = ["handyman", "remodeling contractor", "HVAC contractor", "moving company"]
    if not locations:
        locations = ["Miami, FL", "Hialeah, FL", "Orlando, FL", "Tampa, FL"]
    return niches, locations


def _rotation(niches: list[str], locations: list[str]) -> tuple[str, str]:
    # Railway cron usa UTC. La combinación cambia por intervalo corto y no
    # necesita una base de datos ni un archivo mutable para mantener el cursor.
    slot = int(time.time() // (DISCOVERY_ROTATION_MINUTES * 60))
    niche = niches[slot % len(niches)]
    location = locations[(slot // len(niches)) % len(locations)]
    return niche, location


def _github_json(path: str) -> object:
    url = f"https://api.github.com/repos/{forge.GH_REPO}/contents/{path}?ref=main"
    headers = {
        "Authorization": f"Bearer {forge.GH_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    try:
        payload = forge.http(url, headers=headers, timeout=60)
        return json.loads(base64.b64decode(payload["content"]).decode("utf-8"))
    except Exception as exc:
        print(f"  no se pudo leer {path} desde GitHub: {exc}", flush=True)
        return []


def _known() -> set[str]:
    known: set[str] = set()
    processed = _github_json("data/processed.json")
    if isinstance(processed, list):
        for item in processed:
            for value in (item.get("slug"), item.get("name"), item.get("ig")):
                if value:
                    known.add(re.sub(r"[^a-z0-9]", "", str(value).lower().lstrip("@")))
    # El registro del panel es más reciente que processed.json: una forja publica
    # allí antes de que cualquier snapshot histórico llegue a GitHub.
    if PANEL_KEY:
        try:
            state = forge.http(
                f"{forge.PANEL}/api/state",
                headers={"x-sf-key": PANEL_KEY},
                timeout=30,
            )
            for item in state.get("registry", []) if isinstance(state, dict) else []:
                for value in (item.get("slug"), item.get("name"), item.get("ig")):
                    if value:
                        known.add(re.sub(r"[^a-z0-9]", "", str(value).lower().lstrip("@")))
        except Exception as exc:
            print(f"  no se pudo leer el registro del panel: {exc}", flush=True)
    queue = forge.panel("/api/public/queue") or {}
    for item in queue.get("pending", []):
        value = item.get("input")
        if value:
            raw = str(value).lower()
            known.add(re.sub(r"[^a-z0-9]", "", raw))
            # Los items directos se guardan como "Nombre (Ciudad)"; guardar
            # también el nombre aislado evita que el siguiente slot lo vuelva
            # a encolar con otra ciudad o puntuación.
            match = re.match(r"^(.*?)\s*\([^)]*\)\s*$", raw)
            if match:
                known.add(re.sub(r"[^a-z0-9]", "", match.group(1)))
    return known


def _enqueue(candidate: dict, location: str) -> dict | None:
    name = str(candidate.get("name") or "").strip()
    if not PANEL_KEY:
        print("  falta SITEFORGE_UI_KEY: no se puede encolar un candidato", flush=True)
        return None
    try:
        return forge.http(
            f"{forge.PANEL}/api/queue",
            {
                "input": f"{name} ({location})",
                "candidate": {
                    "name": name,
                    "slug": candidate.get("slug"),
                    "location": location,
                    "niche": candidate.get("niche"),
                    "phone": candidate.get("phone"),
                    "maps_url": candidate.get("maps_url"),
                },
            },
            headers={"x-sf-key": PANEL_KEY},
            timeout=45,
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:240]
        print(f"  queue rechazo {name}: HTTP {exc.code} {detail}", flush=True)
    except Exception as exc:
        print(f"  queue fallo {name}: {exc}", flush=True)
    return None


def _claim(item: dict) -> dict | None:
    try:
        return forge.http(f"{forge.PANEL}/api/public/queue/claim", {"id": item["id"]})
    except urllib.error.HTTPError as exc:
        if exc.code == 409:
            print(f"  otro worker ya reclamó {item.get('input')}", flush=True)
        else:
            print(f"  claim HTTP {exc.code} para {item.get('input')}", flush=True)
    except Exception as exc:
        print(f"  claim fallo para {item.get('input')}: {exc}", flush=True)
    return None


def main() -> int:
    config = _config()
    niches, locations = _lists(config)
    niche, location = _rotation(niches, locations)
    try:
        min_rating = max(0.0, min(float(config.get("min_rating", 4.5)), 5.0))
    except (TypeError, ValueError):
        min_rating = 4.5
    try:
        min_reviews = max(0, int(config.get("min_reviews", 10)))
    except (TypeError, ValueError):
        min_reviews = 10
    print(f"discovery cron: {niche} en {location}", flush=True)
    known = _known()
    pending_count = sum(1 for item in (forge.panel("/api/public/queue") or {}).get("pending", []))
    free_slots = max(0, 20 - pending_count)
    target = min(DISCOVERY_TARGET, free_slots)
    if target == 0:
        print("cola llena o sin capacidad disponible; no se buscan candidatos nuevos", flush=True)
        return 0
    try:
        candidates = discover(niche, location, DISCOVERY_CANDIDATES, min_rating, min_reviews)
    except Exception as exc:
        print(f"discovery fallo: {exc}", flush=True)
        return 1
    selected = []
    for candidate in candidates:
        keys = {
            re.sub(r"[^a-z0-9]", "", str(candidate.get("slug", "")).lower()),
            re.sub(r"[^a-z0-9]", "", str(candidate.get("name", "")).lower()),
        }
        if keys & known:
            continue
        selected.append(candidate)
        known.update(keys)
        if len(selected) >= target:
            break
    print(f"candidatos nuevos: {len(selected)} de {len(candidates)}", flush=True)
    queued: list[dict] = []
    for candidate in selected:
        result = _enqueue(candidate, location)
        if result and result.get("item"):
            queued.append(result["item"])
            print(f"  encolado: {candidate['name']} ({candidate.get('score', 0)})", flush=True)

    # El worker permanente suele reclamar estos items. Si no está activo, este
    # job construye uno para que la automatización siga funcionando por sí sola.
    for item in queued[:CRON_MAX_BUILDS]:
        claimed = _claim(item)
        if not claimed or not claimed.get("item"):
            continue
        try:
            forge.procesar_nombre(claimed["item"])
        except Exception as exc:
            print(f"  build cron fallo: {exc}", flush=True)
            claimed_item = claimed.get("item") or {}
            forge.terminar(
                claimed_item.get("id", item["id"]),
                token=claimed_item.get("claim_token"),
                failed=True,
                motivo=f"Excepción en cron: {str(exc)[:180]}",
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
