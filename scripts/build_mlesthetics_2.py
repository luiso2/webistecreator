import re

SLUG = "ml-esthetics-pompano-beach"
PATH = f"output/{SLUG}/index.html"
h = open(PATH, encoding="utf-8").read()


def rep(a, b, n=1):
    global h
    assert a in h, "NO ANCHOR: " + a[:160]
    h = h.replace(a, b, n)


BOOK = "https://booksy.com/en-us/1680270_ml-esthetics_brows-lashes_15649_pompano-beach"

# ---------------------------------------------------------------------------
# 12. SERVICIOS (4 destacados + menu completo categorizado, sin acordeones)
# ---------------------------------------------------------------------------
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Elige tu" data-en="Choose your">Choose your</span> <span class="text-shine" data-es="tratamiento" data-en="treatment">treatment</span>')
rep('data-es="Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Lash Bloom on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Lash Bloom en Booksy. Reserva con confirmación inmediata.</p>',
    'data-es="Precios publicados por ML Esthetics en Booksy. Reserva con confirmación inmediata." data-en="Prices as published by ML Esthetics on Booksy. Booking confirms instantly.">Prices as published by ML Esthetics on Booksy. Booking confirms instantly.</p>')

services_grid = re.search(
    r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
    h, flags=re.S)
assert services_grid
NEW_SERVICES = f'''<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Pestañas y Cejas" data-en="Lashes &amp; Brows">Lashes &amp; Brows</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lash Lift" data-en="Lash Lift">Lash Lift</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Curvatura y elevación de tus pestañas naturales, sin extensiones, para una mirada abierta que dura semanas." data-en="A curl and lift for your natural lashes, no extensions, for an open-eyed look that lasts for weeks.">A curl and lift for your natural lashes, no extensions, for an open-eyed look that lasts for weeks.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$80</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:110ms; border-color: rgba(138,74,82,0.4); box-shadow: 0 18px 50px rgba(51,36,34,0.14);">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Favorito del estudio" data-en="Studio favorite">Studio favorite</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Microblading" data-en="Microblading">Microblading</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Trazos finos, hebra por hebra, para cejas de aspecto natural que se mantienen de 1 a 2 años. También disponible en powder brows y ombre." data-en="Fine, hair-like strokes for natural-looking brows that last 1 to 2 years. Also available as powder brows and ombre.">Fine, hair-like strokes for natural-looking brows that last 1 to 2 years. Also available as powder brows and ombre.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$450</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-3d rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:220ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Maquillaje Permanente" data-en="Permanent Makeup">Permanent Makeup</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Lip Blush" data-en="Lip Blush">Lip Blush</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Pigmento semipermanente que define el contorno y devuelve color natural a tus labios, sin necesidad de labial diario." data-en="Semi-permanent pigment that defines your lip line and brings back natural color, no daily lipstick required.">Semi-permanent pigment that defines your lip line and brings back natural color, no daily lipstick required.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$450</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
        <div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal" style="transition-delay:330ms">
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="Faciales" data-en="Facials">Facials</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="Facial Descongestionante" data-en="Detoxing Facial">Detoxing Facial</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="Limpieza profunda para renovar tu piel, con extracción y productos pensados para tu tipo de piel." data-en="A deep cleanse to refresh your skin, with extractions and products suited to your skin type.">A deep cleanse to refresh your skin, with extractions and products suited to your skin type.</p>
          <div class="mt-auto">
            <div class="flex items-baseline gap-3 mb-5"><p class="font-display text-3xl text-shine">$60</p><p class="text-xs text-[color:var(--ink-40)] uppercase tracking-wide">1h</p></div>
            <a href="{BOOK}" target="_blank" rel="noopener" class="btn-ghost rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Reservar" data-en="Book">Book</a>
          </div>
        </div>
      </div>
      '''
h = h[:services_grid.start()] + NEW_SERVICES + h[services_grid.end():]

# Nota + Menu completo categorizado (41 servicios reales de Booksy, sin acordeones)
old_note = '<p class="reveal text-center text-xs text-[color:var(--ink-40)] font-light mt-8"><span data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span></p>'
assert old_note in h

def row(es, en, price, dur=None):
    p = f'${price}'
    d = f' &middot; {dur}' if dur else ''
    return (f'<div class="flex items-center justify-between gap-4 py-2.5 border-b border-[color:var(--accent-ghost)] last:border-0">'
            f'<span class="text-sm font-light" data-es="{es}" data-en="{en}">{en}</span>'
            f'<span class="text-sm text-[color:var(--ink-60)] whitespace-nowrap">{p}{d}</span></div>')

CATS = [
    ("Lifts &amp; Lamination", "Lifting y Laminado",
     [("Korean Lash Lift", "Korean Lash Lift", 90, None),
      ("Lash Lift", "Lash Lift", 80, None),
      ("Eyelash Lift + Tint", "Eyelash Lift + Tint", 85, "45min"),
      ("Brow Lamination", "Brow Lamination", 80, None),
      ("Brow Lamination and Tint", "Brow Lamination and Tint", 90, None),
      ("Eyebrow &amp; Lash Lamination + Tint", "Eyebrow &amp; Lash Lamination + Tint", 150, None)]),
    ("Brow Shaping &amp; Tint", "Diseño y Tinte de Cejas",
     [("Brow Waxing and Shaping", "Brow Waxing and Shaping", 30, "15min"),
      ("Brow Tint", "Brow Tint", 35, "20min"),
      ("One Wax Session on Both Eyebrows", "One Wax Session on Both Eyebrows", 15, "20min")]),
    ("Permanent Makeup &middot; Brows", "Maquillaje Permanente &middot; Cejas",
     [("Powder Brows / Microshading", "Powder Brows / Microshading", 450, None),
      ("Nano Brows", "Nano Brows", 450, None),
      ("Ombre Powder Brows", "Ombre Powder Brows", 450, None),
      ("Microblading", "Microblading", 450, None),
      ("Color Correction", "Color Correction", 350, None),
      ("Ombre Powder Brows Touch-Up (6-12 Weeks)", "Ombre Powder Brows Touch-Up (6-12 Weeks)", 200, None),
      ("Microblading Touch-Up (6-12 Weeks)", "Microblading Touch-Up (6-12 Weeks)", 150, None)]),
    ("Permanent Makeup &middot; Lips &amp; Eyes", "Maquillaje Permanente &middot; Labios y Ojos",
     [("Lip Blush", "Lip Blush", 450, None),
      ("Lip Blush Touch-Up", "Lip Blush Touch-Up", 150, None),
      ("Eyeliner Touchup", "Eyeliner Touchup", 125, "1h"),
      ("Eyeliner Top and Bottom", "Eyeliner Top and Bottom", 300, None),
      ("Eyeliner Permanent Makeup", "Eyeliner Permanent Makeup", 250, None),
      ("Eyeliner with Shading", "Eyeliner with Shading", 300, None),
      ("Hyaluron Pen Lip Filler (Needle Free)", "Hyaluron Pen Lip Filler (Needle Free)", 600, None)]),
    ("Facials", "Faciales",
     [("Detoxing Facial", "Detoxing Facial", 60, "1h"),
      ("Bacial", "Bacial", 100, None),
      ("Nanoneedling Facial", "Nanoneedling Facial", 150, None),
      ("Kids Facial", "Kids Facial", 50, None),
      ("Chemical Peel Facial", "Chemical Peel Facial", 120, "30min")]),
    ("Scar &amp; Stretch Mark Camouflage", "Camuflaje de Cicatrices y Estrías",
     [("1x1 in Area Scar Camouflage", "1x1 in Area Scar Camouflage", 250, None),
      ("2x2 in Area Scar Camouflage", "2x2 in Area Scar Camouflage", 350, None),
      ("3x3 in Scar Camouflage", "3x3 in Scar Camouflage", 450, None),
      ("Medium Area", "Medium Area", 600, None),
      ("Large Area", "Large Area", 1000, None),
      ("XL Area Scar or Stretch Mark Camouflage", "XL Area Scar or Stretch Mark Camouflage", 1500, None),
      ("Vitiligo", "Vitiligo", 100, None)]),
    ("Waxing", "Depilación",
     [("One Full Face Waxing", "One Full Face Waxing", 35, "20min"),
      ("One Upper Lip Wax", "One Upper Lip Wax", 10, "10min"),
      ("One Large Area", "One Large Area", 50, None)]),
    ("Other", "Otros",
     [("Saline Tattoo Removal", "Saline Tattoo Removal", 200, None),
      ("Additional Session", "Additional Session", 50, None)]),
]

cards = []
for i, (en_title, es_title, items) in enumerate(CATS):
    rows = "\n            ".join(row(es, en, price, dur) for en, es, price, dur in items)
    delay = f' style="transition-delay:{(i % 4) * 90}ms"' if i else ''
    cards.append(f'''        <div class="glass rounded-3xl p-6 sm:p-7 reveal"{delay}>
          <h4 class="font-display text-lg mb-4 text-[color:var(--accent-deep)]" data-es="{es_title}" data-en="{en_title}">{en_title}</h4>
          <div>
            {rows}
          </div>
        </div>''')

FULL_MENU = f'''<div class="mt-16">
        <div class="text-center max-w-2xl mx-auto mb-10">
          <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-4" data-es="Menú completo" data-en="Full menu">Full menu</p>
          <h3 class="reveal font-display text-3xl sm:text-4xl leading-tight" data-es="Los 41 servicios de ML Esthetics" data-en="All 41 ML Esthetics services">All 41 ML Esthetics services</h3>
        </div>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
{chr(10).join(cards)}
        </div>
      </div>
      '''

new_note = old_note.replace(
    'data-es="Programa de lealtad para clientas frecuentes. Menú completo y disponibilidad en Booksy." data-en="Loyalty program for regulars. Full menu and availability on Booksy.">Loyalty program for regulars. Full menu and availability on Booksy.</span>',
    'data-es="Precios publicados por ML Esthetics en Booksy en julio 2026. Sujetos a cambio, confirma en tu reserva." data-en="Prices as published by ML Esthetics on Booksy as of July 2026. Subject to change, confirm at booking.">Prices as published by ML Esthetics on Booksy as of July 2026. Subject to change, confirm at booking.</span>'
)
h = h.replace(old_note, new_note + '\n      ' + FULL_MENU, 1)
print("SERVICIOS done")

open(PATH, "w", encoding="utf-8").write(h)
print("PART 2 saved,", len(h))
