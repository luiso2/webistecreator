#!/usr/bin/env python3
"""Utilidad de paleta: rota TODOS los colores del esqueleto v2 (menos el badge Merktop)
por el mismo delta de hue en HSL, tomando como referencia el accent principal.
Uso: python3 scripts/palette_shift.py <light-v2|dark-v2> <slug> <target_hue_deg> [sat_mult] [light_mult]
Escribe output/<slug>/index.html a partir de templates/<base>/index.html.
"""
import re
import sys
import colorsys

ACCENT_REF = {
    "light-v2": "a04a72",
    "dark-v2": "d4a84b",
}


def hex_to_rgb(hx):
    hx = hx.lstrip("#")
    return tuple(int(hx[i : i + 2], 16) for i in (0, 2, 4))


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
    base = sys.argv[1]
    slug = sys.argv[2]
    target_hue = float(sys.argv[3])
    sat_mult = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    light_mult = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0

    src = f"templates/{base}/index.html"
    dst = f"output/{slug}/index.html"

    h = open(src, encoding="utf-8").read()

    m = re.search(r"\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n", h, flags=re.S)
    assert m, "no se encontro el bloque merktop-badge"
    badge_block = m.group(0)
    h = h.replace(badge_block, "@@BADGE@@", 1)

    ref_rgb = hex_to_rgb(ACCENT_REF[base])
    ref_h, _, _ = colorsys.rgb_to_hls(*(c / 255.0 for c in ref_rgb))
    ref_h_deg = ref_h * 360.0
    hue_delta = target_hue - ref_h_deg

    # todos los hex de 6 digitos presentes (fuera del badge)
    hexes = sorted(set(re.findall(r"#([0-9a-fA-F]{6})", h)))
    hex_map = {}
    for hx in hexes:
        rgb = hex_to_rgb(hx)
        new_rgb = shift_color(rgb, hue_delta, sat_mult, light_mult)
        hex_map[hx.lower()] = rgb_to_hex(new_rgb)

    def hex_repl(mo):
        return "#" + hex_map[mo.group(1).lower()]

    h = re.sub(r"#([0-9a-fA-F]{6})", hex_repl, h)

    # todos los rgb()/rgba() de 3 componentes presentes
    def rgba_repl(mo):
        r, g, b = int(mo.group(1)), int(mo.group(2)), int(mo.group(3))
        alpha = mo.group(4)
        new_rgb = shift_color((r, g, b), hue_delta, sat_mult, light_mult)
        nr, ng, nb = (round(c) for c in new_rgb)
        if alpha is not None:
            return f"rgba({nr},{ng},{nb}{alpha})"
        return f"rgb({nr},{ng},{nb})"

    h = re.sub(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(,\s*[\d.]+\s*)?\)",
        rgba_repl,
        h,
    )

    h = h.replace("@@BADGE@@", badge_block, 1)

    import os

    os.makedirs(f"output/{slug}", exist_ok=True)
    open(dst, "w", encoding="utf-8").write(h)
    print(f"PALETTE OK: {dst} (hue_delta={hue_delta:.1f} from {base} ref {ACCENT_REF[base]})")
    print(f"  {len(hex_map)} hex colors remapped, badge protected")


if __name__ == "__main__":
    main()
