#!/usr/bin/env python3
"""Derivacion anclada: templates/dark-v2 -> output/prestigeautocargo.

PRESTIGE AUTO CARGO (@prestigeautocargo), Miami FL. Exportacion de vehiculos.
Datos VERIFICADOS (2026-07-29), nada inventado:
- Nombre y tagline: "PRESTIGE AUTO CARGO | Cumplimos Tu Sueno" (nombre del perfil de IG)
- Bio literal: "Especializado en exportacion de vehiculos" + telefono +1(786)923-6762
- IG: 6,536 seguidores / 89 publicaciones / 82 siguiendo (header del perfil, 2026-07-29)
- TikTok: link externo de la bio
- Sin website propio: prestigeautocargo .com/.net/.us no resuelven; prestigecargo.com esta en venta
- SIN resenas publicas verificables -> variante SIN-testimonios (FORGE-BRIEF seccion 0)
- SIN direccion publica -> nada de mapa embed inventado; esa columna lleva foto real
- SIN precios publicos -> las cards no llevan precio

Paleta: NO se toca (el logo del negocio es dorado sobre negro, ya coincide con dark-v2),
asi que tampoco hace falta proteger el badge Merktop.
"""
import re

RUTA = 'output/prestigeautocargo/index.html'
h = open(RUTA, encoding='utf-8').read()

WA = 'https://wa.me/17869236762'
IG = 'https://www.instagram.com/prestigeautocargo/'
TT = 'https://www.tiktok.com/@prestigeautocargo'
BOOKSY = 'https://booksy.com/en-us/121705_pure-artistry_hair-salon_134763_orlando'


def rep(a, b, n=1):
    global h
    assert a in h, 'ANCLA ROTA: ' + a[:120]
    h = h.replace(a, b, n)


def rx(patron, nuevo, flags=re.S):
    global h
    assert re.search(patron, h, flags=flags), 'REGEX SIN MATCH: ' + patron[:120]
    h = re.sub(patron, lambda _: nuevo, h, count=1, flags=flags)


# ---------------------------------------------------------------- 1. GLOBALES
rep(BOOKSY, WA, n=h.count(BOOKSY))
rep('https://www.instagram.com/pure.artistrysk/', IG, n=h.count('https://www.instagram.com/pure.artistrysk/'))
rep('@pure.artistrysk', '@prestigeautocargo', n=h.count('@pure.artistrysk'))

# ---------------------------------------------------------------- 2. HEAD
rep('<title>Pure Artistry · Hair Studio in Orlando, FL | Silk Press, Locs &amp; K-Tips | 5.0 on Booksy</title>',
    '<title>Prestige Auto Cargo · Exportación de vehículos desde Miami, FL | Cumplimos Tu Sueño</title>')
rep('<meta name="description" content="Pure Artistry, Orlando FL: silk press, loc retwists, knotless braids, K-Tip extensions and keratin treatments. 5.0 with 234 reviews on Booksy. Book online." />',
    '<meta name="description" content="Prestige Auto Cargo, Miami FL: especializados en exportación de vehículos. SUV, sedanes y deportivos gestionados de principio a fin. Escríbenos al +1 (786) 923-6762." />')
rep('<meta property="og:title" content="Pure Artistry · Hair Studio in Orlando, FL" />',
    '<meta property="og:title" content="Prestige Auto Cargo · Exportación de vehículos desde Miami" />')
rep('<meta property="og:description" content="Silk press, locs, braids and K-Tip extensions. 5.0 on Booksy. Book online." />',
    '<meta property="og:description" content="Especializados en exportación de vehículos. Cumplimos tu sueño." />')
rep('<meta property="og:image" content="assets/raw/bk-1.jpg" />',
    '<meta property="og:image" content="assets/raw/bk-8.jpg" />')
rep('<link rel="icon" type="image/jpeg" href="assets/raw/bk-2.jpg" />',
    '<link rel="icon" type="image/jpeg" href="assets/raw/logo.jpg" />')

# JSON-LD: AutomotiveBusiness. Sin address inventada, sin aggregateRating (no hay resenas
# publicas), sin precios. Solo lo que el perfil publica.
rx(r'<script type="application/ld\+json">.*?</script>', """<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "AutomotiveBusiness",
    "name": "Prestige Auto Cargo",
    "slogan": "Cumplimos Tu Sueño",
    "description": "Empresa de Miami, FL especializada en exportación de vehículos: SUV, sedanes y deportivos, con gestión de principio a fin.",
    "areaServed": { "@type": "City", "name": "Miami" },
    "address": { "@type": "PostalAddress", "addressLocality": "Miami", "addressRegion": "FL", "addressCountry": "US" },
    "telephone": "+1-786-923-6762",
    "image": "assets/raw/bk-8.jpg",
    "sameAs": ["https://www.instagram.com/prestigeautocargo/", "https://www.tiktok.com/@prestigeautocargo"]
  }
  </script>""")

# ---------------------------------------------------------------- 3. IDIOMA (ES principal)
rep('<html lang="en" class="scroll-smooth">', '<html lang="es" class="scroll-smooth">')
rep("applyLang(lang === 'es' ? 'es' : 'en');", "applyLang(lang === 'en' ? 'en' : 'es');")

# ---------------------------------------------------------------- 4. PRELOADER + NAV
rep('<span class="pre-word">Pure Artistry</span>', '<span class="pre-word">Prestige Auto Cargo</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />',
    '<img src="assets/raw/logo.jpg" alt="Prestige Auto Cargo" class="w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.35)]" />')
rep('<span class="font-display text-xl tracking-[0.1em] uppercase">Pure <span class="text-[color:var(--accent-deep)]">Artistry</span></span>',
    # tracking/tamano responsive: "Prestige Auto Cargo" es mas largo que el nombre del
    # esqueleto y a 390px partia en dos lineas dentro del nav.
    '<span class="font-display text-base sm:text-xl tracking-[0.04em] sm:tracking-[0.1em] uppercase whitespace-nowrap">Prestige <span class="text-[color:var(--accent-deep)]">Auto Cargo</span></span>')

# Labels del nav (desktop y movil comparten los mismos strings)
for viejo, es, en in [
    ('data-es="La Experiencia" data-en="The Experience">La Experiencia', 'Nosotros', 'About us'),
    ('data-es="El Método" data-en="The Method">El Método', 'Proceso', 'Process'),
    ('data-es="Opiniones" data-en="Reviews">Opiniones', 'Por qué Prestige', 'Why Prestige'),
    ('data-es="Ubicación" data-en="Location">Ubicación', 'Contacto', 'Contact'),
]:
    nuevo = f'data-es="{es}" data-en="{en}">{es}'
    rep(viejo, nuevo, n=h.count(viejo))

# CTA del nav: de "Reservar cita" a WhatsApp (icono de calendario -> icono de mensaje)
rep('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>\n          <span data-es="Reservar cita" data-en="Book now">Reservar cita</span>',
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z"/></svg>\n          <span data-es="Escríbenos" data-en="Message us">Escríbenos</span>')
rep('class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Reservar cita" data-en="Book now">Reservar cita</a>',
    'class="btn-3d rounded-full px-5 py-3 text-sm text-center mt-2" data-es="Escríbenos por WhatsApp" data-en="Message us on WhatsApp">Escríbenos por WhatsApp</a>')

# ---------------------------------------------------------------- 5. HERO
rep('data-es="Orlando, FL · Hair Studio" data-en="Orlando, FL · Hair Studio">Orlando, FL · Hair Studio',
    'data-es="Miami, FL · Exportación de vehículos" data-en="Miami, FL · Vehicle export">Miami, FL · Exportación de vehículos')
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>\n        <h1',
    'data-es="Cumplimos tu sueño." data-en="We deliver your dream.">Cumplimos tu sueño.</p>\n        <h1')
rep('<span data-es="Silk press, locs y" data-en="Silk press, locs and">Silk press, locs and</span><br /><span data-es="extensiones nivel " data-en="extensions at a ">extensions at a </span><span class="text-shine" data-es="celebridad" data-en="celebrity level">celebrity level</span>',
    '<span data-es="Tu próximo auto," data-en="Your next car,">Tu próximo auto,</span><br /><span data-es="exportado con " data-en="exported with ">exportado con </span><span class="text-shine" data-es="Prestige" data-en="Prestige">Prestige</span>')
rep('data-es="Silk press que aguanta el calor de Orlando, retwist e interlock de locs, knotless braids, K-Tips y microlinks. Una estilista que ha trabajado con atletas de la NBA y MLB, con 5.0 perfecto en 234 reseñas." data-en="Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.">Silk presses that survive the Orlando heat, loc retwists and interlocks, knotless braids, K-Tips and microlinks. A stylist trusted by NBA and MLB athletes, with a perfect 5.0 across 234 reviews.',
    'data-es="Especializados en exportación de vehículos desde Miami. SUV, sedanes y deportivos: nos ocupamos del proceso completo y te mantenemos informado en cada etapa, hasta que las llaves están en tus manos." data-en="Specialists in vehicle export out of Miami. SUVs, sedans and sports cars: we handle the full process and keep you posted at every stage, until the keys are in your hands.">Especializados en exportación de vehículos desde Miami. SUV, sedanes y deportivos: nos ocupamos del proceso completo y te mantenemos informado en cada etapa, hasta que las llaves están en tus manos.')

# Sin resenas publicas: fuera estrellas y rating del hero, entra la comunidad real de IG.
rep("""<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <span class="stars text-lg" aria-hidden="true">★★★★★</span>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="5.0 · 234 reseñas en Booksy" data-en="5.0 · 234 reviews on Booksy">5.0 · 234 reviews on Booksy</span>
        </div>""",
    """<div class="reveal flex items-center gap-3 mb-9" style="transition-delay:300ms">
          <svg class="text-[color:var(--accent-deep)]" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          <span class="text-sm text-[color:var(--ink-60)]" data-es="6,536 seguidores en Instagram" data-en="6,536 followers on Instagram">6,536 seguidores en Instagram</span>
        </div>""")

rep('<span data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</span>',
    '<span data-es="Escríbenos por WhatsApp" data-en="Message us on WhatsApp">Escríbenos por WhatsApp</span>')

# Imagen del hero: entrega real frente al Capitolio (bk-8) y card de contacto en vez de precio.
rep('<img src="assets/raw/bk-1.jpg" alt="Clienta con estilo terminado en el estudio de Pure Artistry, Orlando" class="blur-up w-full h-full object-cover" />',
    '<img src="assets/raw/bk-8.jpg" alt="Vehículo deportivo exportado por Prestige Auto Cargo, ya en su destino" class="blur-up w-full h-full object-cover" />')
rep("""<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Reserva online" data-en="Book online">Reserva online</p>
            <p class="font-display text-lg">Silk Press</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Desde $90 · 2h" data-en="From $90 · 2h">From $90 · 2h</p>""",
    """<p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-1" data-es="Atención directa" data-en="Direct line">Atención directa</p>
            <p class="font-display text-lg">+1 (786) 923-6762</p>
            <p class="text-sm text-[color:var(--ink-60)]" data-es="Miami, FL" data-en="Miami, FL">Miami, FL</p>""")

# ---------------------------------------------------------------- 6. STRIP DE CONFIANZA
rx(r'<div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">.*?</div>\s*</section>',
   """<div class="max-w-7xl mx-auto px-5 sm:px-8 py-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
      <div class="reveal"><p class="font-display text-2xl text-shine"><span data-count="6536">6,536</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Seguidores en Instagram" data-en="Followers on Instagram">Seguidores en Instagram</p></div>
      <div class="reveal" style="transition-delay:90ms"><p class="font-display text-2xl text-shine"><span data-count="89">89</span></p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Publicaciones de entregas" data-en="Posts of deliveries">Publicaciones de entregas</p></div>
      <div class="reveal" style="transition-delay:180ms"><p class="font-display text-2xl">SUV <span class="text-shine">&amp;</span> Sedán</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="También deportivos" data-en="Sports cars too">También deportivos</p></div>
      <div class="reveal" style="transition-delay:270ms"><p class="font-display text-2xl">Miami</p><p class="text-xs text-[color:var(--ink-40)] tracking-wide uppercase mt-1" data-es="Base de operaciones" data-en="Home base">Base de operaciones</p></div>
    </div>
  </section>""")

# ---------------------------------------------------------------- 7. MARQUEES (x2, 4 copias de cada palabra)
for viejo, nuevo in [
    ('<span class="marquee-word">Silk Press</span>', '<span class="marquee-word">Exportación de vehículos</span>'),
    ('<span class="marquee-word">Loc Retwist</span>', '<span class="marquee-word">SUV</span>'),
    ('<span class="marquee-word">Knotless Braids</span>', '<span class="marquee-word">Sedanes</span>'),
    ('<span class="marquee-word">K-Tip Extensions</span>', '<span class="marquee-word">Deportivos</span>'),
    ('<span class="marquee-word">Keratin</span>', '<span class="marquee-word">Cumplimos Tu Sueño</span>'),
    ('<span class="marquee-word">Orlando, FL</span>', '<span class="marquee-word">Miami, FL</span>'),
]:
    assert h.count(viejo) == 4, f'se esperaban 4 copias de {viejo}, hay {h.count(viejo)}'
    h = h.replace(viejo, nuevo)

# ---------------------------------------------------------------- 8. NOSOTROS (ex "La Experiencia")
rep('<img src="assets/raw/bk-2.jpg" alt="Clienta con look terminado en el sofa amarillo del estudio Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-11.jpg" alt="Entrega de llaves de un SUV a su nuevo dueño, Prestige Auto Cargo" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('<img src="assets/raw/bk-6.jpg" alt="Twists recien terminados en Pure Artistry" class="blur-up w-full h-full object-cover" loading="lazy" />',
    '<img src="assets/raw/bk-6.jpg" alt="Clientes de Prestige Auto Cargo junto a los vehículos disponibles" class="blur-up w-full h-full object-cover" loading="lazy" />')
rep('data-es="La experiencia" data-en="The experience">La experiencia',
    'data-es="Nosotros" data-en="About us">Nosotros')
rep('<span data-es="Una estilista," data-en="One stylist,">One stylist,</span><br /><span class="text-shine" data-es="manos de celebridad" data-en="celebrity hands">celebrity hands</span>',
    '<span data-es="Un equipo," data-en="One team,">Un equipo,</span><br /><span class="text-shine" data-es="un solo objetivo" data-en="one single goal">un solo objetivo</span>')
rep('data-es="Pure Artistry es el estudio privado de una estilista K-Tip specialist que ha peinado a atletas de la NBA y la MLB. Silk press, locs, trenzas y extensiones, todo en un suite uno-a-uno en el centro de Orlando." data-en="Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.">Pure Artistry is the private studio of a K-Tip specialist who has styled NBA and MLB athletes. Silk press, locs, braids and extensions, all in a one-on-one suite in downtown Orlando.',
    'data-es="Prestige Auto Cargo es una empresa de Miami especializada en exportación de vehículos. Trabajamos SUV, sedanes y deportivos, y acompañamos cada operación de principio a fin: nada de dejarte solo a mitad del proceso." data-en="Prestige Auto Cargo is a Miami company specialized in vehicle export. We handle SUVs, sedans and sports cars, and we walk you through every operation from start to finish: never left alone halfway.">Prestige Auto Cargo es una empresa de Miami especializada en exportación de vehículos. Trabajamos SUV, sedanes y deportivos, y acompañamos cada operación de principio a fin: nada de dejarte solo a mitad del proceso.')
rep('data-es="Sus clientas lo confirman: un silk press que dura dos semanas completas en el calor de Orlando. 5.0 perfecto en 234 reseñas verificadas de Booksy." data-en="Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.">Her clients confirm it: silk presses that last a full two weeks in the Orlando heat. A perfect 5.0 across 234 verified Booksy reviews.',
    'data-es="Nuestro trabajo está a la vista: cada entrega queda documentada en Instagram, donde 6,536 personas siguen las operaciones y las nuevas marcas que vamos sumando." data-en="Our work is out in the open: every delivery is documented on Instagram, where 6,536 people follow the operations and the new brands we keep adding.">Nuestro trabajo está a la vista: cada entrega queda documentada en Instagram, donde 6,536 personas siguen las operaciones y las nuevas marcas que vamos sumando.')

# Mini-stats de Nosotros (el esqueleto trae rating de Booksy; aqui van datos reales de IG)
rx(r'<div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">.*?</div>\s*</div>\s*<div class="reveal flex flex-wrap gap-4"',
   """<div class="reveal grid grid-cols-3 gap-4 mb-9" style="transition-delay:300ms">
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="6536">6,536</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Seguidores" data-en="Followers">Seguidores</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine"><span data-count="89">89</span></p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Publicaciones" data-en="Posts">Publicaciones</p></div>
          <div class="glass glass-hover rounded-2xl p-4 text-center"><p class="font-display text-xl text-shine">1:1</p><p class="text-[11px] text-[color:var(--ink-40)] uppercase tracking-wide mt-1" data-es="Atención directa" data-en="Direct contact">Atención directa</p></div>
        </div>
        <div class="reveal flex flex-wrap gap-4\"""")

rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry, estilista" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />',
    '<img src="assets/raw/bk-9.jpg" alt="Equipo de Prestige Auto Cargo junto a los vehículos" class="blur-up w-10 h-10 rounded-full object-cover ring-1 ring-[rgba(212,168,75,0.3)]" loading="lazy" />')
rep('<span class="text-sm font-light">Pure Artistry · <span class="text-[color:var(--ink-40)]" data-es="K-Tip Specialist" data-en="K-Tip Specialist">K-Tip Specialist</span></span>',
    '<span class="text-sm font-light">Prestige Auto Cargo · <span class="text-[color:var(--ink-40)]" data-es="Miami, FL" data-en="Miami, FL">Miami, FL</span></span>')

# ---------------------------------------------------------------- 9. PROCESO (ex "El Metodo")
rep('data-es="Tu cita, paso a paso" data-en="Your visit, step by step">Tu cita, paso a paso',
    'data-es="Tu vehículo, paso a paso" data-en="Your vehicle, step by step">Tu vehículo, paso a paso')
rep('<span data-es="Así se trabaja" data-en="How it works">How it works</span> <span class="text-shine" data-es="aquí" data-en="here">here</span>',
    '<span data-es="Así trabajamos" data-en="How we work">Así trabajamos</span> <span class="text-shine" data-es="contigo" data-en="with you">contigo</span>')
PASOS = [
    ('Escríbenos', 'Get in touch',
     'Nos cuentas qué vehículo buscas y a dónde va. Respondemos por WhatsApp, Instagram o teléfono, sin formularios ni intermediarios.',
     'Tell us what vehicle you are after and where it is going. We reply on WhatsApp, Instagram or by phone, no forms, no middlemen.'),
    ('Elegimos el vehículo', 'We pick the vehicle',
     'Revisamos juntos las marcas y modelos disponibles hasta dar con el que encaja con lo que buscas.',
     'We go through the available brands and models together until we land on the one that fits what you want.'),
    ('Gestión y envío', 'Paperwork and shipping',
     'Nos ocupamos de la documentación y de la logística de exportación. Tú sigues el avance, nosotros movemos el papeleo.',
     'We take care of the documentation and the export logistics. You follow the progress, we move the paperwork.'),
    ('Entrega', 'Handover',
     'El vehículo llega a destino y las llaves cambian de manos. Ese momento es el que publicamos en Instagram.',
     'The vehicle reaches its destination and the keys change hands. That moment is what we post on Instagram.'),
]
VIEJOS_PASOS = [
    ('data-es="Reserva online" data-en="Book online">Book online</h3>',
     'data-es="Eliges tu servicio en Booksy con precio y duración claros: silk press, retwist, braids o extensiones, y confirmas al instante." data-en="Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.">Pick your service on Booksy with clear price and duration: silk press, retwist, braids or extensions, and confirm instantly.'),
    ('data-es="Consulta capilar" data-en="Hair consult">Hair consult</h3>',
     'data-es="Tu tipo de cabello, su salud y el estilo que buscas definen la técnica: proteger tu cabello natural es la prioridad." data-en="Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.">Your hair type, its health and the style you want define the technique: protecting your natural hair comes first.'),
    ('data-es="Manos a la obra" data-en="The work">The work</h3>',
     'data-es="Del silk press de 2 horas a las knotless de 7: cada servicio recibe su tiempo completo, sin citas dobles ni apuros." data-en="From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.">From the 2-hour silk press to 7-hour knotless braids: every service gets its full time, no double booking, no rushing.'),
    ('data-es="El toque final" data-en="The finish">The finish</h3>',
     'data-es="Sales con el acabado que aguanta semanas y las indicaciones para cuidarlo en casa. Tu próxima cita queda agendada." data-en="You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.">You leave with a finish that lasts for weeks and the guidance to keep it that way at home. Next visit booked before you go.'),
]
for (t_es, t_en, p_es, p_en), (v_titulo, v_parrafo) in zip(PASOS, VIEJOS_PASOS):
    rep(v_titulo, f'data-es="{t_es}" data-en="{t_en}">{t_es}</h3>')
    rep(v_parrafo, f'data-es="{p_es}" data-en="{p_en}">{p_es}')

# ---------------------------------------------------------------- 10. SERVICIOS (sin precios: no hay publicados)
rep('data-es="Servicios" data-en="Services">Servicios</p>\n        <h2',
    'data-es="Servicios" data-en="Services">Servicios</p>\n        <h2')
rep('<span data-es="Elige tu" data-en="Choose your">Elige tu</span> <span class="text-shine">ritual</span>',
    '<span data-es="Lo que" data-en="What we">Lo que</span> <span class="text-shine" data-es="hacemos" data-en="do">hacemos</span>')
rep('data-es="Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata." data-en="Prices and durations as published by Pure Artistry on Booksy. Booking confirms instantly.">Precios y duraciones publicados por Pure Artistry en Booksy. Reserva con confirmación inmediata.',
    'data-es="Cada operación se cotiza según el vehículo y el destino. Escríbenos y te damos el detalle sin compromiso." data-en="Every job is quoted based on the vehicle and the destination. Message us and we will walk you through it, no strings attached.">Cada operación se cotiza según el vehículo y el destino. Escríbenos y te damos el detalle sin compromiso.')

TARJETA = """<div class="glass glass-hover rounded-3xl p-7 flex flex-col reveal"{estilo}>
          <p class="text-[11px] tracking-[0.25em] uppercase text-[color:var(--accent-deep)] mb-3" data-es="{tag_es}" data-en="{tag_en}">{tag_es}</p>
          <h3 class="font-display text-2xl leading-snug mb-3" data-es="{titulo_es}" data-en="{titulo_en}">{titulo_es}</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed mb-6" data-es="{texto_es}" data-en="{texto_en}">{texto_es}</p>
          <div class="mt-auto">
            <a href="{wa}" target="_blank" rel="noopener" class="{boton} rounded-full px-6 py-3 text-sm inline-flex items-center gap-2 w-full justify-center" data-es="Consultar" data-en="Ask about it">Consultar</a>
          </div>
        </div>"""
SERVICIOS = [
    dict(estilo=' style="border-color: rgba(212,168,75,0.4); box-shadow: 0 18px 50px rgba(0,0,0,0.35);"',
         tag_es='Nuestra especialidad', tag_en='Our specialty',
         titulo_es='Exportación de vehículos', titulo_en='Vehicle export',
         texto_es='Es a lo que nos dedicamos. Gestionamos la exportación de tu vehículo desde Miami y te acompañamos en cada etapa del proceso.',
         texto_en='This is what we do. We manage the export of your vehicle out of Miami and stay with you through every stage of the process.',
         boton='btn-3d'),
    dict(estilo=' style="transition-delay:110ms"',
         tag_es='Catálogo', tag_en='Catalog',
         titulo_es='SUV y camionetas', titulo_en='SUVs and trucks',
         texto_es='Los modelos que más nos piden. Consulta por las marcas disponibles: el catálogo se actualiza y publicamos las novedades en Instagram.',
         texto_en='The models we are asked for the most. Ask about available brands: the catalog changes and we post what is new on Instagram.',
         boton='btn-ghost'),
    dict(estilo=' style="transition-delay:220ms"',
         tag_es='Catálogo', tag_en='Catalog',
         titulo_es='Sedanes', titulo_en='Sedans',
         texto_es='Del auto familiar al ejecutivo. Te ayudamos a comparar opciones y a elegir según tu presupuesto y tu destino.',
         texto_en='From the family car to the executive one. We help you compare options and choose based on your budget and destination.',
         boton='btn-ghost'),
    dict(estilo=' style="transition-delay:330ms"',
         tag_es='Alta gama', tag_en='High end',
         titulo_es='Deportivos y eléctricos', titulo_en='Sports and electric',
         texto_es='También movemos vehículos de alta gama y eléctricos, con el mismo cuidado y la misma documentación en regla.',
         texto_en='We also move high-end and electric vehicles, with the same care and the same paperwork in order.',
         boton='btn-ghost'),
]
rx(r'<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">.*?</div>\s*(?=<p class="reveal text-center)',
   '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 items-stretch">\n        '
   + '\n        '.join(TARJETA.format(wa=WA, **s) for s in SERVICIOS)
   + '\n      </div>\n      ')

rep('<span data-es="También: virgin relaxers desde $150 y quick weave desde $140. Menú completo y disponibilidad en Booksy." data-en="Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.">Also: virgin relaxers from $150 and quick weaves from $140. Full menu and availability on Booksy.',
    '<span data-es="¿No ves el modelo que buscas? Escríbenos igual: sumamos marcas nuevas con frecuencia." data-en="Do not see the model you want? Message us anyway: we add new brands regularly.">¿No ves el modelo que buscas? Escríbenos igual: sumamos marcas nuevas con frecuencia.')

# ---------------------------------------------------------------- 11. GALERIA
rep('<span data-es="Trabajo" data-en="Real">Real</span> <span class="text-shine" data-es="real" data-en="hair">hair</span>',
    '<span data-es="Entregas" data-en="Real">Entregas</span> <span class="text-shine" data-es="reales" data-en="deliveries">reales</span>')
TILES = [
    ('bk-1.jpg', 'col-span-2 aspect-[16/9]', '', 'En ruta', 'On the road', 'Vehículos de Prestige Auto Cargo en ruta hacia el puerto'),
    ('bk-12.jpg', 'aspect-[3/4]', ' style="transition-delay:90ms"', 'Clientes', 'Clients', 'Clientes de Prestige Auto Cargo junto a sus vehículos'),
    ('bk-7.jpg', 'aspect-[3/4]', ' style="transition-delay:150ms"', 'Deportivos', 'Sports cars', 'Vehículo deportivo gestionado por Prestige Auto Cargo'),
    ('bk-3.jpg', 'aspect-[3/4] lg:mt-10', ' style="transition-delay:120ms"', 'El equipo', 'The team', 'Integrante del equipo de Prestige Auto Cargo'),
    ('bk-9.jpg', 'aspect-[3/4]', ' style="transition-delay:210ms"', 'Flota lista', 'Fleet ready', 'Flota de vehículos lista para exportación'),
    ('bk-5.jpg', 'aspect-[3/4] lg:mt-10', ' style="transition-delay:300ms"', 'Entrega', 'Handover', 'Entrega de un vehículo a sus nuevos dueños'),
]
rx(r'<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">.*?</div>\s*</div>\s*</section>',
   '<div class="grid grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">\n        '
   + '\n        '.join(
       f'<div class="frame zoomable {clases} img-reveal"{delay}><span class="tile-cap" data-es="{cap_es}" data-en="{cap_en}">{cap_es}</span>'
       f'<img src="assets/raw/{img}" alt="{alt}" class="blur-up w-full h-full object-cover"{"" if i == 0 else " loading=\"lazy\""} /></div>'
       for i, (img, clases, delay, cap_es, cap_en, alt) in enumerate(TILES))
   + '\n      </div>\n    </div>\n  </section>')

# ---------------------------------------------------------------- 12. POR QUE PRESTIGE (variante SIN-testimonios)
rx(r'<!-- OPINIONES -->.*?<!-- UBICACION -->', """<!-- POR QUE PRESTIGE (sin testimonios: el negocio no tiene resenas publicas verificables) -->
  <section id="opiniones" class="relative py-24 sm:py-32 grain">
    <span class="sec-num" aria-hidden="true">05</span>
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <p class="reveal text-xs tracking-[0.35em] uppercase text-[color:var(--accent-deep)] mb-5" data-es="Por qué Prestige" data-en="Why Prestige">Por qué Prestige</p>
        <h2 class="reveal font-display text-4xl sm:text-5xl leading-tight" style="transition-delay:80ms"><span data-es="Tres razones" data-en="Three reasons">Tres razones</span> <span class="text-shine" data-es="para escribirnos" data-en="to message us">para escribirnos</span></h2>
        <p class="reveal mt-5 text-sm text-[color:var(--ink-60)] font-light" style="transition-delay:160ms" data-es="Cada operación queda publicada en nuestro Instagram: puedes ver el trabajo antes de escribirnos." data-en="Every job ends up on our Instagram: you can see the work before you reach out.">Cada operación queda publicada en nuestro Instagram: puedes ver el trabajo antes de escribirnos.</p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5 items-stretch">
        <div class="glass glass-hover rounded-3xl p-8 reveal">
          <svg class="text-[color:var(--accent-deep)] mb-5" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 4 6v6c0 5 3.4 9.2 8 10 4.6-.8 8-5 8-10V6Z"/><path d="m9 12 2 2 4-4"/></svg>
          <h3 class="font-display text-xl mb-3" data-es="Especialistas, no improvisados" data-en="Specialists, not improvisers">Especialistas, no improvisados</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="La exportación de vehículos es nuestra única especialidad. No es un servicio más de una lista larga: es a lo que nos dedicamos todos los días." data-en="Vehicle export is our one specialty. It is not one more line on a long list: it is what we do every single day.">La exportación de vehículos es nuestra única especialidad. No es un servicio más de una lista larga: es a lo que nos dedicamos todos los días.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:110ms">
          <svg class="text-[color:var(--accent-deep)] mb-5" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z"/></svg>
          <h3 class="font-display text-xl mb-3" data-es="Hablas con nosotros, no con un bot" data-en="You talk to us, not a bot">Hablas con nosotros, no con un bot</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="Un número directo, +1 (786) 923-6762, y respuesta por WhatsApp o Instagram. Sin call center y sin formularios que nadie contesta." data-en="One direct number, +1 (786) 923-6762, and answers on WhatsApp or Instagram. No call center, no forms that nobody reads.">Un número directo, +1 (786) 923-6762, y respuesta por WhatsApp o Instagram. Sin call center y sin formularios que nadie contesta.</p>
        </div>
        <div class="glass glass-hover rounded-3xl p-8 reveal" style="transition-delay:220ms">
          <svg class="text-[color:var(--accent-deep)] mb-5" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
          <h3 class="font-display text-xl mb-3" data-es="Trabajo a la vista de todos" data-en="Work out in the open">Trabajo a la vista de todos</h3>
          <p class="text-sm text-[color:var(--ink-60)] font-light leading-relaxed" data-es="6,536 personas siguen nuestras entregas en Instagram. Las publicamos porque no tenemos nada que esconder: mira el feed antes de decidir." data-en="6,536 people follow our deliveries on Instagram. We post them because we have nothing to hide: check the feed before you decide.">6,536 personas siguen nuestras entregas en Instagram. Las publicamos porque no tenemos nada que esconder: mira el feed antes de decidir.</p>
        </div>
      </div>
      <div class="text-center mt-10 reveal">
        <a href="%s" target="_blank" rel="noopener" class="btn-ghost rounded-full px-7 py-3.5 text-sm inline-flex items-center gap-2" data-es="Ver las entregas en Instagram" data-en="See the deliveries on Instagram">Ver las entregas en Instagram</a>
      </div>
    </div>
  </section>

  <!-- UBICACION -->""" % IG)

# ---------------------------------------------------------------- 13. CONTACTO (ex UBICACION; sin mapa: no hay direccion publica)
rep('data-es="Visítanos" data-en="Visit us">Visítanos</p>', 'data-es="Contacto" data-en="Contact">Contacto</p>')
rep('<span data-es="Visítanos en" data-en="Visit us in">Visítanos en</span> <span class="text-shine">Orlando</span>',
    '<span data-es="Escríbenos desde" data-en="Reach us from">Escríbenos desde</span> <span class="text-shine">Miami</span>')
rx(r'<div class="space-y-4">.*?</div>\s*</div>\s*<div class="frame map-frame reveal min-h-\[380px\]" style="transition-delay:180ms">.*?</div>',
   """<div class="space-y-4">
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:140ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="WhatsApp y teléfono" data-en="WhatsApp and phone">WhatsApp y teléfono</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="La vía más rápida. Cuéntanos qué vehículo buscas y a dónde va, y te respondemos con el detalle." data-en="The fastest way. Tell us what vehicle you want and where it is going, and we will come back with the details.">La vía más rápida. Cuéntanos qué vehículo buscas y a dónde va, y te respondemos con el detalle.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="tel:+17869236762">+1 (786) 923-6762</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:200ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
            <div>
              <p class="font-medium mb-1" data-es="Instagram" data-en="Instagram">Instagram</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Ahí publicamos las entregas y las marcas nuevas que van entrando. También puedes escribirnos por DM." data-en="That is where we post deliveries and the new brands coming in. You can also reach us by DM.">Ahí publicamos las entregas y las marcas nuevas que van entrando. También puedes escribirnos por DM.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="%s" target="_blank" rel="noopener">@prestigeautocargo</a>
            </div>
          </div>
          <div class="glass glass-hover rounded-2xl p-6 flex items-start gap-4 reveal" style="transition-delay:260ms">
            <svg class="mt-1 shrink-0 text-[color:var(--accent-deep)]" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5"/></svg>
            <div>
              <p class="font-medium mb-1">TikTok</p>
              <p class="text-sm text-[color:var(--ink-60)] font-light" data-es="Los videos de cada operación, desde la selección del vehículo hasta la entrega final." data-en="Video from every job, from picking the vehicle to the final handover.">Los videos de cada operación, desde la selección del vehículo hasta la entrega final.</p>
              <a class="text-sm text-[color:var(--accent-deep)] underline underline-offset-4 decoration-[rgba(212,168,75,0.4)]" href="%s" target="_blank" rel="noopener">@prestigeautocargo</a>
            </div>
          </div>
        </div>
      </div>
      <div class="frame zoomable img-reveal min-h-[380px] h-full max-h-[560px] lg:max-h-none" style="transition-delay:180ms">
        <img src="assets/raw/bk-11.jpg" alt="Entrega de un vehículo exportado por Prestige Auto Cargo en Miami" class="blur-up w-full h-full object-cover" loading="lazy" />
      </div>""" % (IG, TT))

# ---------------------------------------------------------------- 14. CTA FINAL
rep('data-es="Tu cabello, tratado como arte." data-en="Your hair, treated like art.">Your hair, treated like art.</p>',
    'data-es="Cumplimos tu sueño." data-en="We deliver your dream.">Cumplimos tu sueño.</p>')
rep('<span data-es="Tu silla" data-en="Your chair">Your chair</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">is waiting</span>',
    '<span data-es="Tu auto" data-en="Your car">Tu auto</span> <span class="text-shine" data-es="te está esperando" data-en="is waiting">te está esperando</span>')
rep('data-es="Reserva online en segundos: tu silk press, tu retwist o esas knotless que llevas planeando." data-en="Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.">Book online in seconds: your silk press, your retwist, or those knotless braids you have been planning.',
    'data-es="Un mensaje y empezamos: dinos qué vehículo buscas y a dónde va. Te respondemos con el detalle, sin compromiso." data-en="One message and we start: tell us what vehicle you want and where it is going. We will come back with the details, no strings attached.">Un mensaje y empezamos: dinos qué vehículo buscas y a dónde va. Te respondemos con el detalle, sin compromiso.')
rep('class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Reservar en Booksy" data-en="Book on Booksy">Reservar en Booksy</a>',
    'class="btn-3d rounded-full px-10 py-4 text-sm inline-flex items-center gap-2" data-es="Escríbenos por WhatsApp" data-en="Message us on WhatsApp">Escríbenos por WhatsApp</a>')

# ---------------------------------------------------------------- 15. FOOTER
rep('<span class="foot-mark" aria-hidden="true">Pure Artistry</span>', '<span class="foot-mark" aria-hidden="true">Prestige</span>')
rep('<img src="assets/raw/bk-2.jpg" alt="Pure Artistry" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />',
    '<img src="assets/raw/logo.jpg" alt="Prestige Auto Cargo" class="w-9 h-9 rounded-full object-cover ring-1 ring-[rgba(232,207,150,0.35)]" loading="lazy" />')
rep('<span class="font-display text-lg tracking-[0.1em] uppercase">Pure Artistry</span>',
    '<span class="font-display text-lg tracking-[0.1em] uppercase">Prestige Auto Cargo</span>')
rep('data-es="Hair studio en el centro de Orlando, FL. Atención con cita previa." data-en="Hair studio in downtown Orlando, FL. By appointment only.">Hair studio in downtown Orlando, FL. By appointment only.',
    'data-es="Exportación de vehículos desde Miami, FL. Cumplimos tu sueño." data-en="Vehicle export out of Miami, FL. We deliver your dream.">Exportación de vehículos desde Miami, FL. Cumplimos tu sueño.')
rep('<p>80 W Grant St, Suite 111, Studio 156, Orlando, FL 32806</p>', '<p>Miami, FL, Estados Unidos</p>')
rep('data-es="Reservas online · Booksy" data-en="Online booking · Booksy">Reservas online · Booksy',
    'data-es="WhatsApp · +1 (786) 923-6762" data-en="WhatsApp · +1 (786) 923-6762">WhatsApp · +1 (786) 923-6762')
rep('<p><a href="%s" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · @prestigeautocargo</a></p>' % IG,
    '<p><a href="%s" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">Instagram · @prestigeautocargo</a></p>\n        <p><a href="%s" target="_blank" rel="noopener" class="hover:text-[#e9c3ab]">TikTok · @prestigeautocargo</a></p>' % (IG, TT))
rep('<p class="text-xs text-[color:var(--ink-40)]">© 2026 Pure Artistry.</p>',
    '<p class="text-xs text-[color:var(--ink-40)]">© 2026 Prestige Auto Cargo.</p>')

# Boton flotante: de calendario a WhatsApp
rep('<a href="%s" target="_blank" rel="noopener" class="book-float" aria-label="Reservar cita online">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>\n  </a>' % WA,
    '<a href="%s" target="_blank" rel="noopener" class="book-float" aria-label="Escribir por WhatsApp">\n    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1c1408" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z"/></svg>\n  </a>' % WA)

# Aria-labels sueltos del esqueleto
rep('aria-label="Abrir menú"', 'aria-label="Abrir menu"')

open(RUTA, 'w', encoding='utf-8').write(h)
print('prestigeautocargo: derivacion completa ->', RUTA)
