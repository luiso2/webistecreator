#!/usr/bin/env python3
"""Genera un site derivando el esqueleto v2 a partir de un content.json.

Uso: python3 scripts/derive.py <slug>          (lee output/<slug>/content.json)

POR QUE: cada negocio traia su propio build_<slug>.py de ~18 KB (el de hoy, 45 KB), y
medido sobre uno real solo el 25% era contenido: el otro 75% eran las MISMAS anclas del
esqueleto reescritas a mano una y otra vez. Cada reescritura es una oportunidad de romper
un ancla y de gastar iteraciones. Aqui la mecanica vive UNA vez y por negocio solo se
escribe el contenido.

El content.json es 100% texto del negocio: si un dato no existe (precios, resenas,
direccion), simplemente no se pone y la seccion se adapta. Nunca se inventa.
Ver output/prestigeautocargo/content.json como ejemplo completo.
"""
import colorsys
import json
import os
import re
import sys

ESQUELETOS = {'dark-v2': 'templates/dark-v2/index.html', 'light-v2': 'templates/light-v2/index.html'}
ACCENT_REF = {'light-v2': 'a04a72', 'dark-v2': 'd4a84b'}


def _hex_to_rgb(hx):
    hx = hx.lstrip('#')
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    r, g, b = (max(0, min(255, round(c))) for c in rgb)
    return '%02x%02x%02x' % (r, g, b)


def _shift(rgb, hue_delta, sat_mult, light_mult):
    r, g, b = (c / 255.0 for c in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + hue_delta / 360.0) % 1.0
    s = max(0.0, min(1.0, s * sat_mult))
    l = max(0.0, min(1.0, l * light_mult))
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return (r2 * 255, g2 * 255, b2 * 255)


def aplicar_paleta(h, base, paleta):
    """Rota TODOS los colores del esqueleto (menos el badge Merktop) al hue pedido,
    ANTES de derivar el contenido (los anchors de derive() son texto, no color: no colisiona)."""
    target_hue = paleta['hue']
    sat_mult = paleta.get('sat_mult', 1.0)
    light_mult = paleta.get('light_mult', 1.0)

    m = re.search(r'\.merktop-badge \{.*?@keyframes mkPulse[^\n]*\n', h, flags=re.S)
    assert m, 'no se encontro el bloque merktop-badge'
    badge_block = m.group(0)
    h = h.replace(badge_block, '@@BADGE@@', 1)

    ref_rgb = _hex_to_rgb(ACCENT_REF[base])
    ref_h, _, _ = colorsys.rgb_to_hls(*(c / 255.0 for c in ref_rgb))
    hue_delta = target_hue - ref_h * 360.0

    hexes = sorted(set(re.findall(r'#([0-9a-fA-F]{6})', h)))
    hex_map = {hx.lower(): _rgb_to_hex(_shift(_hex_to_rgb(hx), hue_delta, sat_mult, light_mult)) for hx in hexes}
    h = re.sub(r'#([0-9a-fA-F]{6})', lambda mo: '#' + hex_map[mo.group(1).lower()], h)

    def rgba_repl(mo):
        r, g, b = int(mo.group(1)), int(mo.group(2)), int(mo.group(3))
        alpha = mo.group(4)
        nr, ng, nb = (round(c) for c in _shift((r, g, b), hue_delta, sat_mult, light_mult))
        return f'rgba({nr},{ng},{nb}{alpha})' if alpha is not None else f'rgb({nr},{ng},{nb})'

    h = re.sub(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(,\s*[\d.]+\s*)?\)', rgba_repl, h)
    return h.replace('@@BADGE@@', badge_block, 1)

# Anclas literales que SI difieren entre esqueletos (texto propio de cada negocio origen:
# pureartistry en dark-v2, lashbloom en light-v2). Las anclas genericas (nav, servicios "ritual",
# bloque de opiniones, contacto cards, book-float, etc.) son identicas en ambos esqueletos y
# viven directo en el cuerpo de construir() sin pasar por este dict.
BASES = {
    'dark-v2': {
        'booksy': 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando',
        'ig': 'https://www.instagram.com/pure.artistrysk/',
        'handle': '@pure.artistrysk',
        'pre_mono': 'PA',
        'pre_word': 'Pure Artistry',
        'logo_nav': '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
        'nav_brand': '<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
        'foot_mark': '<span class="foot-mark" aria-hidden="true">Pure Artistry</span>',
        'proceso_h2': '<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
        'hero_eyebrow': 'data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio',
        'hero_script': 'data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>\n        <h1',
        'hero_h1': '<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
        'hero_rating': 'data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy',
        'hero_img_re': r'<img src="assets/raw/bk-1\.jpg" alt=".*?" class="blur-up w-full h-full object-cover" />',
        'hero_tarjeta': '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Silk Press</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>',
        'marquee_viejas': ['Silk Press', 'Loc Retwist', 'Knotless Braids', 'K-Tip Extensions', 'Keratin', 'Orlando, FL'],
        'nosotros_img1_re': r'<img src="assets/raw/bk-2\.jpg" alt="Clienta con look terminado.*?loading="lazy" />',
        'nosotros_img2_re': r'<img src="assets/raw/bk-6\.jpg" alt="Twists recien terminados.*?loading="lazy" />',
        'nosotros_h2': '<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
        'nosotros_avatar_re': r'<img src="assets/raw/bk-2\.jpg" alt="Pure Artistry, estilista".*?loading="lazy" />',
        'nosotros_avatar_pie': '<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
        'proceso_pasos': [
            ('data-es="Reserva online" data-en="Book online">Book online</h3>', r'data-es="Eliges tu servicio en Booksy.*?</p>'),
            ('data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>', r'data-es="Tu tipo de cabello.*?</p>'),
            ('data-es="Manos a la obra" data-en="The work">The work</h3>', r'data-es="Del silk press de 2 horas.*?</p>'),
            ('data-es="El toque final" data-en="The finish">The finish</h3>', r'data-es="Sales con el acabado.*?</p>'),
        ],
        'galeria_h2': '<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
        'contacto_h2a': '<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
        'cta_final_script': 'data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
        'cta_final_h2': '<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
        'footer_logo': '<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />',
        'footer_brand': '<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
        'footer_address': '80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806',
        'footer_ig_hover': 'hover:text-[#e9c3ab]',
        'book_float_stroke': '#1c1408',
    },
    'light-v2': {
        'booksy': 'https://booksy.com/en-us/519855_lash-bloom-llc_brows-lashes_15961_west-palm-beach',
        'ig': 'https://www.instagram.com/_lashbloom/',
        'handle': '@_lashbloom',
        'pre_mono': 'LB',
        'pre_word': 'Lash Bloom',
        'logo_nav': '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(160,74,114,0.35)]" />',
        'nav_brand': '<span class="font-display text-xl tracking-[0.1em] uppercase">Lash <span class="text-[color:var(--accent-deep)]">Bloom</span></span>',
        'foot_mark': '<span class="foot-mark" aria-hidden="true">Lash Bloom</span>',
        'proceso_h2': '<span data-es="Tu cita, pestaña" data-en="Your visit, lash">Your visit, lash</span> <span class="text-shine" data-es="por pestaña" data-en="by lash">by lash</span>',
        'hero_eyebrow': 'data-es="West Palm Beach, FL · Lash Studio" data-en="West Palm Beach, FL · Lash Studio">West Palm Beach, FL · Lash Studio',
        'hero_script': 'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>\n        <h1',
        'hero_h1': '<span data-es="Pestañas clásicas, híbridas" data-en="Classic, hybrid and volume">Classic, hybrid and volume</span><br /><span data-es="y volumen, hechas para " data-en="lashes, made to ">lashes, made to </span><span class="text-shine" data-es="florecer" data-en="bloom">bloom</span>',
        'hero_rating': 'data-es="5.0 · 86 reseñas en Booksy" data-en="5.0 · 86 reviews on Booksy">5.0 · 86 reviews on Booksy',
        'hero_img_re': r'<img src="assets/raw/bk-6\.jpg" alt="Clienta feliz con su set de pestañas terminado en Lash Bloom" class="blur-up w-full h-full object-cover" />',
        'hero_tarjeta': '<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>\n            <p class="font-display text-lg">Volume Full Set</p>\n            <p class="text-sm text-[color:var(--ink-60)]" data-es="$155 · 1h 50min" data-en="$155 · 1h 50min">$155 · 1h 50min</p>',
        'marquee_viejas': ['Classic Set', 'Hybrid Set', 'Volume Set', 'Mega Volume', 'Bottom Lashes', 'West Palm Beach, FL'],
        'nosotros_img1_re': r'<img src="assets/raw/hero-1\.jpg" alt="El suite de Lash Bloom.*?loading="lazy" />',
        'nosotros_img2_re': r'<img src="assets/raw/about-2\.jpg" alt="Rincon del estudio.*?loading="lazy" />',
        'nosotros_h2': '<span data-es="Un suite zen" data-en="A zen suite">A zen suite</span><br /><span class="text-shine" data-es="hecho para relajarte" data-en="made to unwind in">made to unwind in</span>',
        'nosotros_avatar_re': r'<img src="assets/raw/logo\.jpg" alt="Lash Bloom" class="blur-up w-10 h-10.*?loading="lazy" />',
        'nosotros_avatar_pie': '<span class="text-sm font-light">Yesi · <span class="text-[color:var(--ink-40)]" data-es="Artista licenciada" data-en="Licensed lash artist">Licensed lash artist</span></span>',
        'proceso_pasos': [
            ('data-es="Reserva online" data-en="Book online">Book online</h3>', r'data-es="Eliges tu set o tu relleno.*?</p>'),
            ('data-es="Mapeo del ojo" data-en="Eye mapping">Eye mapping</h3>', r'data-es="Forma del ojo.*?</p>'),
            ('data-es="Aplicación zen" data-en="The zen part">The zen part</h3>', r'data-es="Te recuestas.*?</p>'),
            ('data-es="Plan de relleno" data-en="Fill plan">Fill plan</h3>', r'data-es="Sales con tu relleno.*?</p>'),
        ],
        'galeria_h2': '<span data-es="Miradas" data-en="Real">Real</span> <span class="text-shine" data-es="reales" data-en="lashes">lashes</span>',
        'contacto_h2a': '<span data-es="Visítanos en" data-en="Visit us in">Visit us in</span> <span class="text-shine">West Palm Beach</span>',
        'cta_final_script': 'data-es="Pestañas que florecen contigo." data-en="Lashes that bloom with you.">Lashes that bloom with you.</p>',
        'cta_final_h2': '<span data-es="Tu mirada nueva" data-en="Your new lashes">Your new lashes</span> <span class="text-shine" data-es="te está esperando" data-en="are waiting">are waiting</span>',
        'footer_logo': '<img src="assets/raw/logo.jpg" alt="Lash Bloom" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(240,190,215,0.35)]" loading="lazy" />',
        'footer_brand': '<span class="font-display text-lg tracking-[0.1em] uppercase">Lash Bloom</span>',
        'footer_address': '4580 Cresthaven Blvd, West Palm Beach, FL 33415',
        'footer_ig_hover': 'hover:text-[#f0bed7]',
        'book_float_stroke': '#faf2f6',
    },
}


class Deriva:
    def __init__(self, html):
        self.h = html

    def rep(self, viejo, nuevo, n=1):
        assert viejo in self.h, 'ANCLA ROTA: ' + viejo[:110]
        self.h = self.h.replace(viejo, nuevo, n)

    def rep_todos(self, viejo, nuevo):
        assert viejo in self.h, 'ANCLA ROTA: ' + viejo[:110]
        self.h = self.h.replace(viejo, nuevo)

    def rx(self, patron, nuevo):
        assert re.search(patron, self.h, re.S), 'REGEX SIN MATCH: ' + patron[:110]
        self.h = re.sub(patron, lambda _: nuevo, self.h, count=1, flags=re.S)


def t(nodo, lang):
    """Texto visible: el del idioma principal del site."""
    return nodo.get(lang) or nodo.get('es') or nodo.get('en') or ''


def attrs(nodo):
    es = (nodo.get('es') or nodo.get('en') or '').replace('"', '&quot;')
    en = (nodo.get('en') or nodo.get('es') or '').replace('"', '&quot;')
    return f'data-es="{es}" data-en="{en}"'


def span(nodo, lang, clase=''):
    c = f' class="{clase}"' if clase else ''
    return f'<span{c} {attrs(nodo)}>{t(nodo, lang)}</span>'


# --------------------------------------------------------------- plantillas de bloque
TARJETA_SERVICIO = """<div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal"{estilo}>
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" {tag_attrs}>{tag}</p>
          <h3 class="font-display text-2xl leading-snug mb-3" {titulo_attrs}>{titulo}</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" {texto_attrs}>{texto}</p>
          <div class="mt-auto">{precio}
            <a href="{cta_url}" target="_blank" rel="noopener" class="{boton} rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" {cta_attrs}>{cta}</a>
          </div>
        </div>"""

PRECIO = """
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">{precio}</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">{duracion}</p></div>"""

TILE = ('<div class="frame zoomable {clases} img-reveal"{delay}>'
        '<span class="tile-cap" {cap_attrs}>{cap}</span>'
        '<img src="assets/raw/{img}" alt="{alt}" class="blur-up w-full h-full object-cover"{lazy} /></div>')

CARD_RAZON = """<div class="glass glass-hover rounded-3xl p-8 reveal"{delay}>
          {icono}
          <h3 class="font-display text-xl mb-3" {titulo_attrs}>{titulo}</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" {texto_attrs}>{texto}</p>
        </div>"""

TESTIMONIO = """<figure class="glass glass-hover rounded-3xl p-8 reveal"{delay}>
          <p class="stars text-sm mb-4">★★★★★</p>
          <blockquote class="text-[color:var(--ink-60)] font-light leading-relaxed mb-5">"{quote}"</blockquote>
          <figcaption class="text-sm"><span class="font-medium">{autor}</span> <span class="text-[color:var(--ink-40)]">· {fuente}</span></figcaption>
        </figure>"""

CARD_CONTACTO = """<div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal"{delay}>
            {icono}
            <div>
              <p class="font-medium mb-1" {titulo_attrs}>{titulo}</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" {texto_attrs}>{texto}</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="{url}"{blank}>{enlace}</a>
            </div>
          </div>"""

ICONOS = {
    'whatsapp': '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z"/>',
    'instagram': '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
    'tiktok': '<path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5"/>',
    'mapa': '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    'calendario': '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    'escudo': '<path d="M12 2 4 6v6c0 5 3.4 9.2 8 10 4.6-.8 8-5 8-10V6Z"/><path d="m9 12 2 2 4-4"/>',
    'telefono': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/>',
    'facebook': '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    'email': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
}


def svg(nombre, clases, tam=20, stroke='1.8'):
    return (f'<svg class="{clases}" width="{tam}" height="{tam}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-linejoin="round">{ICONOS.get(nombre, ICONOS["instagram"])}</svg>')


def construir(slug):
    ruta_content = f'output/{slug}/content.json'
    c = json.load(open(ruta_content, encoding='utf-8'))
    lang = c.get('lang', 'es')
    base = c.get('base', 'dark-v2')
    h = open(ESQUELETOS[base], encoding='utf-8').read()
    d = Deriva(h)
    V = BASES[base]  # anclas literales propias del esqueleto elegido

    CTA = c['cta_url']
    IG = c['ig_url']
    HANDLE = c['ig_handle']
    BOOKSY = V['booksy']
    IG_VIEJO = V['ig']

    # 1. globales
    d.rep_todos(BOOKSY, CTA)
    d.rep_todos(IG_VIEJO, IG)
    d.rep_todos(V['handle'], HANDLE)

    # 2. head
    hd = c['head']
    d.rx(r'<title>.*?</title>', f'<title>{hd["title"]}</title>')
    d.rx(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{hd["description"]}" />')
    d.rx(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{hd["og_title"]}" />')
    d.rx(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{hd["og_description"]}" />')
    d.rx(r'<meta property="og:image" content=".*?" />', f'<meta property="og:image" content="{hd["og_image"]}" />')
    d.rx(r'<link rel="icon" type="image/jpeg" href=".*?" />', f'<link rel="icon" type="image/jpeg" href="{hd["icon"]}" />')
    d.rx(r'<script type="application/ld\+json">.*?</script>',
         '<script type="application/ld+json">\n  ' + json.dumps(c['jsonld'], ensure_ascii=False, indent=2) + '\n  </script>')

    # 3. idioma
    if lang == 'es':
        d.rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
        d.rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

    # 4. marca (preloader, nav, footer)
    b = c['brand']
    d.rep(f'<span class="pre-mono">{V["pre_mono"]}</span>', f'<span class="pre-mono">{b["mono"]}</span>')
    d.rep(f'<span class="pre-word">{V["pre_word"]}</span>', f'<span class="pre-word">{b["name"]}</span>')
    d.rep(V['logo_nav'],
          f'<img src="{b["logo"]}" alt="{b["name"]}" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />')
    d.rep(V['nav_brand'],
          f'<span class="font-display text-base sm:text-xl tracking-[0.04em] sm:tracking-[0.1em] uppercase whitespace-nowrap">{b["nav_a"]} <span class="text-[color:var(--accent-deep)]">{b["nav_b"]}</span></span>')
    d.rep(V['foot_mark'],
          f'<span class="foot-mark" aria-hidden="true">{b["footmark"]}</span>')

    # 5. nav labels
    for viejo, nuevo in c.get('nav', {}).items():
        par = {'experiencia': ('La Experiencia', 'The Experience'), 'metodo': ('El Método', 'The Method'),
               'servicios': ('Servicios', 'Services'), 'galeria': ('Galería', 'Gallery'),
               'opiniones': ('Opiniones', 'Reviews'), 'ubicacion': ('Ubicación', 'Location')}[viejo]
        ancla = f'data-es="{par[0]}" data-en="{par[1]}">{par[0]}'
        d.rep_todos(ancla, f'{attrs(nuevo)}>{t(nuevo, lang)}')

    # 6. CTA del nav
    cta_nav = c['cta_label']
    d.rep(f'{ICONOS["calendario"]}</svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
          f'{ICONOS[c.get("cta_icono", "whatsapp")]}</svg>\n          <span {attrs(cta_nav)}>{t(cta_nav, lang)}</span>')
    d.rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
          f'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" {attrs(cta_nav)}>{t(cta_nav, lang)}</a>')

    # 7. hero
    hero = c['hero']
    d.rep(V['hero_eyebrow'],
          f'{attrs(hero["eyebrow"])}>{t(hero["eyebrow"], lang)}')
    d.rep(V['hero_script'],
          f'{attrs(hero["script"])}>{t(hero["script"], lang)}</p>\n        <h1')
    d.rep(V['hero_h1'],
          f'{span(hero["h1_a"], lang)}<br />{span(hero["h1_b"], lang)}{span(hero["h1_shine"], lang, "text-shine")}')
    d.rx(r'<p class="reveal max-w-xl text-\[color:var\(--ink-60\)\] font-light leading-relaxed mb-8" style="transition-delay:240ms" data-es=".*?</p>',
         f'<p class="reveal max-w-xl text-[color:var(--ink-60)] font-light leading-relaxed mb-8" style="transition-delay:240ms" {attrs(hero["parrafo"])}>{t(hero["parrafo"], lang)}</p>')

    # linea de prueba social: con rating (hay resenas) o con la senal que haya
    if hero.get('rating'):
        d.rep(V['hero_rating'],
              f'{attrs(hero["rating"])}>{t(hero["rating"], lang)}')
    else:
        d.rx(r'<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">.*?</div>',
             f'''<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          {svg(hero.get("senal_icono", "instagram"), "text-[color:var(--accent-deep)]", 18)}
          <span class="text-sm text-[color:var(--ink-60)]" {attrs(hero["senal"])}>{t(hero["senal"], lang)}</span>
        </div>''')

    d.rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
          f'{span(c["cta_label"], lang)}')
    d.rx(V['hero_img_re'],
         f'<img src="assets/raw/{hero["imagen"]}" alt="{hero["imagen_alt"]}" class="blur-up w-full h-full object-cover" />')
    tarj = hero['tarjeta']
    d.rep(V['hero_tarjeta'],
          f'''<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" {attrs(tarj["tag"])}>{t(tarj["tag"], lang)}</p>
            <p class="font-display text-lg">{tarj["destacado"]}</p>
            <p class="text-sm text-[color:var(--ink-60)]" {attrs(tarj["pie"])}>{t(tarj["pie"], lang)}</p>''')

    # 8. strip
    def _count_span(count_val, texto_val):
        """data-decimals evita que el contador anime 4.9 -> 5 (redondeo por defecto a 0 decimales)."""
        dec = len(str(count_val).split('.')[1]) if '.' in str(count_val) else 0
        dec_attr = f' data-decimals="{dec}"' if dec else ''
        return f'<span data-count="{count_val}"{dec_attr}>{texto_val}</span>'

    celdas = []
    for i, s in enumerate(c['strip']):
        delay = f' style="transition-delay:{i * 90}ms"' if i else ''
        val = (_count_span(s["count"], s["valor"]) if s.get('count') else s['valor'])
        clase = 'font-display text-2xl text-shine' if s.get('count') else 'font-display text-2xl'
        celdas.append(f'<div class="reveal"{delay}><p class="{clase}">{val}</p>'
                      f'<p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" {attrs(s["etiqueta"])}>{t(s["etiqueta"], lang)}</p></div>')
    d.rx(r'<div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">.*?</div>\s*</section>',
         '<div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">\n      '
         + '\n      '.join(celdas) + '\n    </div>\n  </section>')

    # 9. marquee (4 copias de cada palabra: 2 marquees x 2 secuencias)
    VIEJAS = V['marquee_viejas']
    for viejo, nuevo in zip(VIEJAS, c['marquee']):
        a = f'<span class="marquee-word">{viejo}</span>'
        assert d.h.count(a) == 4, f'se esperaban 4 copias de {viejo}, hay {d.h.count(a)}'
        d.h = d.h.replace(a, f'<span class="marquee-word">{nuevo}</span>')

    # 10. nosotros
    n = c['nosotros']
    d.rx(V['nosotros_img1_re'],
         f'<img src="assets/raw/{n["imagen_1"]}" alt="{n["imagen_1_alt"]}" class="blur-up w-full h-full object-cover" loading="lazy" />')
    d.rx(V['nosotros_img2_re'],
         f'<img src="assets/raw/{n["imagen_2"]}" alt="{n["imagen_2_alt"]}" class="blur-up w-full h-full object-cover" loading="lazy" />')
    d.rep('data-es="La experiencia" data-en="The experience">La experiencia', f'{attrs(n["eyebrow"])}>{t(n["eyebrow"], lang)}')
    d.rep(V['nosotros_h2'],
          f'{span(n["h2_a"], lang)}<br />{span(n["h2_shine"], lang, "text-shine")}')
    d.rx(r'<p class="reveal text-\[color:var\(--ink-60\)\] font-light leading-relaxed mb-5" style="transition-delay:160ms" data-es=".*?</p>',
         f'<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-5" style="transition-delay:160ms" {attrs(n["parrafo_1"])}>{t(n["parrafo_1"], lang)}</p>')
    d.rx(r'<p class="reveal text-\[color:var\(--ink-60\)\] font-light leading-relaxed mb-9" style="transition-delay:220ms" data-es=".*?</p>',
         f'<p class="reveal text-[color:var(--ink-60)] font-light leading-relaxed mb-9" style="transition-delay:220ms" {attrs(n["parrafo_2"])}>{t(n["parrafo_2"], lang)}</p>')
    mini = []
    for m in n['stats']:
        mini.append(f'<div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">'
                    + (_count_span(m["count"], m["valor"]) if m.get('count') else m['valor'])
                    + f'</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" {attrs(m["etiqueta"])}>{t(m["etiqueta"], lang)}</p></div>')
    d.rx(r'<div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">.*?</div>\s*</div>\s*<div class="reveal flex flex-wrap gap-4"',
         '<div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">\n          '
         + '\n          '.join(mini) + '\n        </div>\n        <div class="reveal flex flex-wrap gap-4"')
    d.rx(V['nosotros_avatar_re'],
         f'<img src="assets/raw/{n["avatar"]}" alt="{n["avatar_alt"]}" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />')
    d.rep(V['nosotros_avatar_pie'],
          f'<span class="text-sm font-light">{n.get("avatar_nombre", b["name"])} · <span class="text-[color:var(--ink-40)]" {attrs(n["avatar_pie"])}>{t(n["avatar_pie"], lang)}</span></span>')

    # 11. proceso
    pr = c['proceso']
    d.rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso',
          f'{attrs(pr["eyebrow"])}>{t(pr["eyebrow"], lang)}')
    d.rep(V['proceso_h2'],
          f'{span(pr["h2_a"], lang)} {span(pr["h2_shine"], lang, "text-shine")}')
    # Los patrones de parrafo TIENEN que llegar hasta </p>: el texto visible repite el mismo
    # texto que data-en, asi que un .*? que corte al final del atributo deja el texto viejo
    # pegado detras (bug real: "...movemos el papeleo.">From the 2-hour silk press...").
    VIEJOS_PASOS = V['proceso_pasos']
    for pasoc, (v_tit, v_par) in zip(pr['pasos'], VIEJOS_PASOS):
        d.rep(v_tit, f'{attrs(pasoc["titulo"])}>{t(pasoc["titulo"], lang)}</h3>')
        d.rx(v_par, f'{attrs(pasoc["texto"])}>{t(pasoc["texto"], lang)}</p>')

    # 12. servicios
    sv = c['servicios']
    d.rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
          f'{span(sv["h2_a"], lang)} {span(sv["h2_shine"], lang, "text-shine")}')
    d.rx(r'<p class="reveal mt-5 text-sm text-\[color:var\(--ink-60\)\] font-light" style="transition-delay:160ms" data-es=".*?</p>',
         f'<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" {attrs(sv["nota"])}>{t(sv["nota"], lang)}</p>')
    cards = []
    for i, s in enumerate(sv['cards']):
        estilo = (' style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);"'
                  if i == 0 else f' style="transition-delay:{i * 110}ms"')
        precio = PRECIO.format(precio=s['precio'], duracion=s.get('duracion', '')) if s.get('precio') else ''
        cards.append(TARJETA_SERVICIO.format(
            estilo=estilo, tag=t(s['tag'], lang), tag_attrs=attrs(s['tag']),
            titulo=t(s['titulo'], lang), titulo_attrs=attrs(s['titulo']),
            texto=t(s['texto'], lang), texto_attrs=attrs(s['texto']),
            precio=precio, cta_url=CTA, boton='btn-3d' if i == 0 else 'btn-ghost',
            cta=t(sv['cta'], lang), cta_attrs=attrs(sv['cta'])))
    d.rx(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
         '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">\n        '
         + '\n        '.join(cards) + '\n      </div>\n      ')
    d.rx(r'<p class="reveal text-center text-xs text-\[color:var\(--ink-40\)\] font-light mt-8">.*?</p>',
         f'<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span {attrs(sv["pie"])}>{t(sv["pie"], lang)}</span></p>')

    # 13. galeria
    g = c['galeria']
    d.rep(V['galeria_h2'],
          f'{span(g["h2_a"], lang)} {span(g["h2_shine"], lang, "text-shine")}')
    CLASES = ['col-span-2 aspect-[16/9]', 'aspect-[3/4]', 'aspect-[3/4]',
              'aspect-[3/4] lg:mt-10', 'aspect-[3/4]', 'aspect-[3/4] lg:mt-10']
    DELAYS = ['', ' style="transition-delay:90ms"', ' style="transition-delay:150ms"',
              ' style="transition-delay:120ms"', ' style="transition-delay:210ms"', ' style="transition-delay:300ms"']
    tiles = [TILE.format(clases=CLASES[i], delay=DELAYS[i], cap=t(x['caption'], lang),
                         cap_attrs=attrs(x['caption']), img=x['img'], alt=x['alt'],
                         lazy='' if i == 0 else ' loading="lazy"')
             for i, x in enumerate(g['tiles'][:6])]
    d.rx(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
         '<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">\n        '
         + '\n        '.join(tiles) + '\n      </div>\n    </div>\n  </section>')

    # 14. prueba social: testimonios reales o razones (si no hay resenas verificables)
    sp = c['social_proof']
    if sp['modo'] == 'testimonios':
        bloques = [TESTIMONIO.format(delay='' if i == 0 else f' style="transition-delay:{i * 110}ms"',
                                     quote=x['quote'], autor=x['autor'], fuente=x['fuente'])
                   for i, x in enumerate(sp['items'][:3])]
        sub = (f'<p class="reveal mt-5 text-sm text-[color:var(--ink-60)]" style="transition-delay:160ms">'
               f'<span class="stars">★★★★★</span> &nbsp;<span {attrs(sp["subtitulo"])}>{t(sp["subtitulo"], lang)}</span></p>')
    else:
        bloques = [CARD_RAZON.format(delay='' if i == 0 else f' style="transition-delay:{i * 110}ms"',
                                     icono=svg(x.get('icono', 'escudo'), 'text-[color:var(--accent-deep)] mb-5', 26, '1.6'),
                                     titulo=t(x['titulo'], lang), titulo_attrs=attrs(x['titulo']),
                                     texto=t(x['texto'], lang), texto_attrs=attrs(x['texto']))
                   for i, x in enumerate(sp['items'][:3])]
        sub = (f'<p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" '
               f'{attrs(sp["subtitulo"])}>{t(sp["subtitulo"], lang)}</p>')
    d.rx(r'<!-- OPINIONES -->.*?<!-- UBICACION -->', f'''<!-- PRUEBA SOCIAL ({sp['modo']}) -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" {attrs(sp['eyebrow'])}>{t(sp['eyebrow'], lang)}</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms">{span(sp['h2_a'], lang)} {span(sp['h2_shine'], lang, 'text-shine')}</h2>
        {sub}
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        {chr(10).join('        ' + x for x in bloques).strip()}
      </div>
      <div class="text-center mt-10 reveal">
        <a href="{sp.get('cta_url', IG)}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" {attrs(sp['cta'])}>{t(sp['cta'], lang)}</a>
      </div>
    </div>
  </section>

  <!-- UBICACION -->''')

    # 15. contacto (con mapa si hay direccion verificada, con foto si no)
    ct = c['contacto']
    d.rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>', f'{attrs(ct["eyebrow"])}>{t(ct["eyebrow"], lang)}</p>')
    d.rep(V['contacto_h2a'],
          f'{span(ct["h2_a"], lang)} <span class="text-shine">{ct["h2_shine"]}</span>')
    tarjetas = []
    for i, x in enumerate(ct['cards']):
        tarjetas.append(CARD_CONTACTO.format(
            delay=f' style="transition-delay:{140 + i * 60}ms"',
            icono=svg(x.get('icono', 'instagram'), 'mt-1 shrink-0 text-[color:var(--accent-deep)]'),
            titulo=t(x['titulo'], lang), titulo_attrs=attrs(x['titulo']),
            texto=t(x['texto'], lang), texto_attrs=attrs(x['texto']),
            url=x['url'], enlace=x['enlace'],
            blank='' if x['url'].startswith('tel:') else ' target="_blank" rel="noopener"'))
    if ct.get('mapa'):
        derecha = (f'<div class="frame map-frame reveal min-h-[380px]" style="transition-delay:180ms">\n'
                   f'        <iframe title="{ct["mapa"]["titulo"]}" src="{ct["mapa"]["src"]}" '
                   f'class="w-full h-full min-h-[380px]" style="border:0" loading="lazy" '
                   f'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>\n      </div>')
    else:
        # sin direccion publica NO se pone un mapa inventado: va una foto real
        derecha = (f'<div class="frame zoomable img-reveal min-h-[380px] h-full max-h-[560px] lg:max-h-none" '
                   f'style="transition-delay:180ms">\n        <img src="assets/raw/{ct["imagen"]}" '
                   f'alt="{ct["imagen_alt"]}" class="blur-up w-full h-full object-cover" loading="lazy" />\n      </div>')
    d.rx(r'<div class="space-y-4">.*?</div>\s*</div>\s*<div class="frame map-frame reveal min-h-\[380px\]" style="transition-delay:180ms">.*?</div>',
         '<div class="space-y-4">\n          ' + '\n          '.join(tarjetas) + '\n        </div>\n      </div>\n      ' + derecha)

    # 16. CTA final
    cf = c['cta_final']
    d.rep(V['cta_final_script'],
          f'{attrs(cf["script"])}>{t(cf["script"], lang)}</p>')
    d.rep(V['cta_final_h2'],
          f'{span(cf["h2_a"], lang)} {span(cf["h2_shine"], lang, "text-shine")}')
    d.rx(r'<p class="reveal text-\[color:var\(--ink-60\)\] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" data-es=".*?</p>',
         f'<p class="reveal text-[color:var(--ink-60)] font-light mb-10 max-w-xl mx-auto" style="transition-delay:180ms" {attrs(cf["parrafo"])}>{t(cf["parrafo"], lang)}</p>')
    d.rep('class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
          f'class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" {attrs(c["cta_label"])}>{t(c["cta_label"], lang)}</a>')
    # boton secundario "Seguir en Instagram": texto configurable via social_cta para negocios sin
    # Instagram real (ig_url reusado para Google/Facebook/etc), default identico al de siempre.
    social_cta = c.get('social_cta', {'es': 'Seguir en Instagram', 'en': 'Follow on Instagram'})
    d.rep('class="btn-ghost rounded-full px-10 py-4 text-sm" data-es="Seguir en Instagram" data-en="Follow on Instagram">Seguir en Instagram</a>',
          f'class="btn-ghost rounded-full px-10 py-4 text-sm" {attrs(social_cta)}>{t(social_cta, lang)}</a>')

    # 17. footer
    ft = c['footer']
    d.rep(V['footer_logo'],
          f'<img src="{b["logo"]}" alt="{b["name"]}" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />')
    d.rep(V['footer_brand'],
          f'<span class="font-display text-lg tracking-[0.1em] uppercase">{b["name"]}</span>')
    d.rx(r'<p class="text-sm text-\[color:var\(--ink-40\)\] font-light leading-relaxed" data-es=".*?</p>',
         f'<p class="text-sm text-[color:var(--ink-40)] font-light leading-relaxed" {attrs(ft["descripcion"])}>{t(ft["descripcion"], lang)}</p>')
    d.rep(f'<p>{V["footer_address"]}</p>', f'<p>{ft["linea_contacto"]}</p>')
    d.rx(r'data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy',
         f'{attrs(ft["enlace_contacto"])}>{t(ft["enlace_contacto"], lang)}')
    ig_hover = V['footer_ig_hover']
    # etiqueta de la red social en el footer: "Instagram" por defecto (compat con todo content.json
    # existente, que siempre trae ig_url de instagram.com), pero configurable via social_label para
    # negocios sin Instagram real donde ig_url/ig_handle se reusan para Facebook, tel:, etc.
    # (nunca se relabela un enlace de Facebook como "Instagram": seria un dato falso en la pagina).
    social_label = c.get('social_label', 'Instagram')
    extra = ''.join(f'\n        <p><a href="{x["url"]}" target="_blank" rel="noopener" class="{ig_hover}">{x["texto"]}</a></p>'
                    for x in ft.get('social_extra', []))
    d.rep(f'<p><a href="{IG}" target="_blank" rel="noopener" class="{ig_hover}">Instagram · {HANDLE}</a></p>',
          f'<p><a href="{IG}" target="_blank" rel="noopener" class="{ig_hover}">{social_label} · {HANDLE}</a></p>{extra}')
    d.rep(f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {V["pre_word"]}.</p>',
          f'<p class="text-xs text-[color:var(--ink-40)]">© 2026 {b["name"]}.</p>')

    # 18. boton flotante
    d.rx(r'<a href="[^"]*" target="_blank" rel="noopener" class="book-float" aria-label="[^"]*">\s*<svg.*?</svg>\s*(?:<span class="book-float-label".*?</span>\s*)?</a>',
         f'<a href="{CTA}" target="_blank" rel="noopener" class="book-float" aria-label="{t(c["cta_label"], lang)}">\n'
         f'    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{V["book_float_stroke"]}" stroke-width="2" '
         f'stroke-linecap="round" stroke-linejoin="round">{ICONOS[c.get("cta_icono", "whatsapp")]}</svg>\n'
         f'    <span class="book-float-label" {attrs(c["cta_label"])}>{t(c["cta_label"], lang)}</span>\n  </a>')

    out_h = d.h
    if c.get('paleta'):
        out_h = aplicar_paleta(out_h, base, c['paleta'])

    salida = f'output/{slug}/index.html'
    open(salida, 'w', encoding='utf-8').write(out_h)
    return salida


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    slug = sys.argv[1]
    if not os.path.exists(f'output/{slug}/content.json'):
        print(f'FAIL: falta output/{slug}/content.json')
        sys.exit(1)
    salida = construir(slug)
    print(f'{slug}: derivado -> {salida}')
    print('Siguiente: python3 scripts/publish.py', slug, '--lang <es|en> --forbid "..."')


if __name__ == '__main__':
    main()
