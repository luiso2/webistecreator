#!/usr/bin/env python3
"""Deriva una paleta de acento nueva a partir de un esqueleto v2, rotando el tono (hue)
de todos los colores no neutros en HSL y preservando saturacion/luminosidad exactas.
Mantiene intacta la estructura de contraste del esqueleto (ink oscuro, bg claro/oscuro,
sombras) porque un tono casi neutro (saturacion baja) apenas cambia al rotar el hue.

Uso como libreria:
    from _palette_shift import shift_html_palette
    h = open('templates/light-v2/index.html', encoding='utf-8').read()
    h, mapping = shift_html_palette(h, hue_delta_deg=-150)  # grados a sumar al hue (0-360)
    open('output/<slug>/index.html', 'w', encoding='utf-8').write(h)

No toca el oro del merktop-badge (#D4A84B y sus rgba) ni grises/blancos/negros puros
(saturacion muy baja ya excluida naturalmente, pero #D4A84B se protege explicitamente
por si cae cerca de otro tono en saturacion).
"""
import colorsys
import re

PROTECTED_HEX = {"#d4a84b"}  # merktop-badge, nunca cambia


def _hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (max(0, min(255, round(r))), max(0, min(255, round(g))), max(0, min(255, round(b))))


def _shift_rgb(rgb, hue_delta_deg):
    r, g, b = (c / 255.0 for c in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + hue_delta_deg / 360.0) % 1.0
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def shift_html_palette(html, hue_delta_deg):
    """Devuelve (html_nuevo, mapping) protegiendo el bloque .merktop-badge."""
    badge_m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', html, flags=re.S)
    badge_block = None
    if badge_m:
        badge_block = badge_m.group(0)
        html = html.replace(badge_block, '@@BADGE@@', 1)

    mapping = {}

    # 1. Hex de 6 digitos
    hexes = sorted(set(re.findall(r'#[0-9a-fA-F]{6}', html)), key=len, reverse=True)
    for hx in hexes:
        lhx = hx.lower()
        if lhx in PROTECTED_HEX:
            continue
        rgb = _hex_to_rgb(hx)
        new_rgb = _shift_rgb(rgb, hue_delta_deg)
        new_hex = _rgb_to_hex(*new_rgb)
        mapping[hx] = new_hex
        html = html.replace(hx, new_hex)

    # 2. rgba(R,G,B  (prefijo; no tocamos el alpha)
    rgba_prefixes = sorted(set(re.findall(r'rgba\((\d+),(\d+),(\d+)', html)))
    for r, g, b in rgba_prefixes:
        rgb = (int(r), int(g), int(b))
        if _rgb_to_hex(*rgb).lower() in PROTECTED_HEX:
            continue
        new_rgb = _shift_rgb(rgb, hue_delta_deg)
        old_prefix = f'rgba({r},{g},{b}'
        new_prefix = f'rgba({new_rgb[0]},{new_rgb[1]},{new_rgb[2]}'
        mapping[old_prefix] = new_prefix
        html = html.replace(old_prefix, new_prefix)

    if badge_block:
        html = html.replace('@@BADGE@@', badge_block, 1)

    return html, mapping


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print('Uso: python3 scripts/_palette_shift.py <template.html> <hue_delta_deg> <out.html>')
        sys.exit(2)
    src, delta, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    html = open(src, encoding='utf-8').read()
    html, mapping = shift_html_palette(html, delta)
    open(out, 'w', encoding='utf-8').write(html)
    for k, v in mapping.items():
        print(k, '->', v)
