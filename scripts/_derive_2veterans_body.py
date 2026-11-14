import re

SLUG = 'output/2-veterans-handyman-service/index.html'
h = open(SLUG, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    cnt = h.count(a)
    assert cnt == n, f'NO (found {cnt}, need {n}): {a[:120]!r}'
    h = h.replace(a, b, n)

PHONE_DISPLAY = '(754) 266-7735'
PHONE_TEL = '+17542667735'
FB_URL = 'https://www.facebook.com/2veteranshandymanservice/'
GREV_URL = 'https://www.google.com/search?q=2+Veterans+Handyman+Service+Cape+Coral+FL+reviews'
MAPS_DIR_URL = 'https://www.google.com/maps?q=1806+Southwest+22nd+Terrace,+Cape+Coral,+FL+33991'
MAPS_EMBED = 'https://www.google.com/maps?q=1806+Southwest+22nd+Terrace,+Cape+Coral,+FL+33991&output=embed'

# ---------- PRELOADER ----------
rep('<span class="pre-mono">PA</span>', '<span class="pre-mono">2V</span>')
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">2 Veterans Handyman</span>')

# ---------- NAV ----------
rep(
'''        <img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(63,152,103,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>''',
'''        <img src="assets/hero-chandelier-install.jpg" alt="2 Veterans Handyman Service" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(63,152,103,0.35)]" />
        <span class="font-display text-xl tracking-[0.1em] uppercase">2 <span class="text-[color:var(--accent-deep)]">Veterans</span></span>'''
)
rep(
'''        <a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>
        </a>''',
f'''        <a href="tel:{PHONE_TEL}" class="btn-3d rounded-full px-5 py-2.5 text-sm hidden sm:inline-flex items-center gap-2">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span data-es="Llama para cotizar" data-en="Call for a quote">Call for a quote</span>
        </a>'''
)
rep(
'''        <a href="https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando" target="_blank" rel="noopener" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>''',
f'''        <a href="tel:{PHONE_TEL}" class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Llama para cotizar" data-en="Call for a quote">Call for a quote</a>'''
)

open(SLUG, 'w', encoding='utf-8').write(h)
print('PRELOADER+NAV OK, length', len(h))
