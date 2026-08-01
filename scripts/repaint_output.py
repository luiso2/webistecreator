#!/usr/bin/env python3
"""Recolorea EN SITIO un output/<slug>/index.html ya derivado por derive.py.

derive.py (content.json -> HTML) copia el CSS del esqueleto tal cual: dos negocios
en la misma base (dark-v2/light-v2) salen con el MISMO acento de color si nadie
corre un paso de paleta aparte (DESIGN.md exige paleta derivada de la marca real).
Reutiliza la misma logica HSL de scripts/palette_shift.py pero opera sobre el
archivo YA derivado (protege badge Merktop) en vez de reescribir desde el template,
asi no se pierde el contenido que derive.py ya escribio.

Uso: python3 scripts/repaint_output.py <slug> <base:light-v2|dark-v2> <target_hue_deg> [sat_mult] [light_mult]
"""
import re
import sys
import colorsys

ACCENT_REF = {"light-v2": "a04a72", "dark-v2": "d4a84b"}


def hex_to_rgb(hx):
    hx = hx.lstrip("#")
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    r, g, b = (max(0, min(255, round(c))) for c in rgb)
    return "%02x%02x%02x" % (r, g, b)


def shift_color(rgb, hue_delta, sat_mult, light_mult):
    r, g, b = (c / 255.0 for c in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + hue_delta / 360.0) % 1.0
    s = max(0.0, min(1.0, s * sat_mult))
    l = max(0.0, min(1.0, l * light_mult))
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return (r2 * 255, g2 * 255, b2 * 255)


def main():
    slug, base, target_hue = sys.argv[1], sys.argv[2], float(sys.argv[3])
    sat_mult = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    light_mult = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    path = f"output/{slug}/index.html"
    h = open(path, encoding="utf-8").read()

    m = re.search(r"\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n", h, flags=re.S)
    assert m, "no se encontro el bloque merktop-badge"
    badge_block = m.group(0)
    h = h.replace(badge_block, "@@BADGE@@", 1)

    ref_rgb = hex_to_rgb(ACCENT_REF[base])
    ref_h, _, _ = colorsys.rgb_to_hls(*(c / 255.0 for c in ref_rgb))
    hue_delta = target_hue - ref_h * 360.0

    hexes = sorted(set(re.findall(r"#([0-9a-fA-F]{6})", h)))
    hex_map = {hx.lower(): rgb_to_hex(shift_color(hex_to_rgb(hx), hue_delta, sat_mult, light_mult)) for hx in hexes}
    h = re.sub(r"#([0-9a-fA-F]{6})", lambda mo: "#" + hex_map[mo.group(1).lower()], h)

    def rgba_repl(mo):
        r, g, b = int(mo.group(1)), int(mo.group(2)), int(mo.group(3))
        alpha = mo.group(4)
        nr, ng, nb = (round(c) for c in shift_color((r, g, b), hue_delta, sat_mult, light_mult))
        return f"rgba({nr},{ng},{nb}{alpha})" if alpha is not None else f"rgb({nr},{ng},{nb})"

    h = re.sub(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(,\s*[\d.]+\s*)?\)", rgba_repl, h)
    h = h.replace("@@BADGE@@", badge_block, 1)
    open(path, "w", encoding="utf-8").write(h)
    print(f"REPAINT OK: {path} (hue_delta={hue_delta:.1f} from {base} ref {ACCENT_REF[base]}, {len(hex_map)} hex remapped)")


if __name__ == "__main__":
    main()
