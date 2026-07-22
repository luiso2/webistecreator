import re, colorsys

def _hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(rgb):
    return '#' + ''.join(f'{max(0,min(255,round(c))):02x}' for c in rgb)

def _shift(rgb, dh, ds, dl):
    r, g, b = [c/255 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.03:
        return rgb  # near-gray: leave untouched
    h = (h + dh/360.0) % 1.0
    s = max(0.0, min(1.0, s + ds/100.0))
    l = max(0.0, min(1.0, l + dl/100.0))
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return (r2*255, g2*255, b2*255)

HEX_RE = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
RGBA_RE = re.compile(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)')
BADGE_RE = re.compile(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', re.S)

def recolor(html, dh, ds=0, dl=0):
    token = '@@BADGE_PROTECTED@@'
    m = BADGE_RE.search(html)
    assert m, 'merktop badge block not found'
    badge_block = m.group(0)
    html = html.replace(badge_block, token, 1)

    def hex_repl(m2):
        rgb = _hex_to_rgb(m2.group(0))
        return _rgb_to_hex(_shift(rgb, dh, ds, dl))
    def rgba_repl(m2):
        r, g, b, a = int(m2.group(1)), int(m2.group(2)), int(m2.group(3)), m2.group(4)
        nr, ng, nb = _shift((r, g, b), dh, ds, dl)
        if a is not None:
            return f'rgba({round(nr)}, {round(ng)}, {round(nb)}, {a})'
        return f'rgb({round(nr)}, {round(ng)}, {round(nb)})'

    html = HEX_RE.sub(hex_repl, html)
    html = RGBA_RE.sub(rgba_repl, html)
    html = html.replace(token, badge_block)
    return html
