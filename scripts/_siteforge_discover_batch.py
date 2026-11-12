#!/usr/bin/env python3
"""Corre maps_discover.discover() sobre varias combinaciones niche+location,
dedup contra data/processed.json y contra un pool existente, y ACUMULA en JSON."""
import json
import re
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from maps_discover import discover

COMBOS = json.loads(sys.argv[1])  # [[niche, location, limit], ...]
OUT = sys.argv[2]

def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

processed = json.load(open("data/processed.json"))
seen_names = set(norm(p.get("name", "")) for p in processed)
seen_phones = set()
for p in processed:
    ph = re.sub(r"\D", "", p.get("phone") or "")
    if ph:
        seen_phones.add(ph[-10:])

pool = []
if os.path.exists(OUT):
    try:
        prev = json.load(open(OUT))
        pool = prev.get("pool", [])
    except Exception:
        pool = []
for r in pool:
    seen_names.add(norm(r["name"]))
    ph = re.sub(r"\D", "", r.get("phone") or "")
    if ph:
        seen_phones.add(ph[-10:])

errors = []
for niche, location, limit in COMBOS:
    try:
        results = discover(niche, location, limit=limit, min_rating=4.5, min_reviews=10)
    except Exception as e:
        errors.append({"niche": niche, "location": location, "error": str(e)})
        print(f"[{niche} / {location}] ERROR: {e}", file=sys.stderr)
        continue
    added = 0
    for r in results:
        if norm(r["name"]) in seen_names:
            continue
        ph = re.sub(r"\D", "", r.get("phone") or "")
        if ph and ph[-10:] in seen_phones:
            continue
        pool.append(r)
        seen_names.add(norm(r["name"]))
        if ph:
            seen_phones.add(ph[-10:])
        added += 1
    print(f"[{niche} / {location}] -> {len(results)} results, {added} new", file=sys.stderr)
    json.dump({"pool": pool, "errors": errors}, open(OUT, "w"), ensure_ascii=False, indent=2)

print(f"TOTAL pool: {len(pool)}  errors: {len(errors)}", file=sys.stderr)
