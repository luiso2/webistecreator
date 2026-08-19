#!/usr/bin/env python3
"""Curacion y contenido SIN IA: reglas deterministicas + plantillas por nicho.

Decision del usuario (2026-08-18): la forja no usa ninguna API de IA. Que cubre cada pieza:

CURACION (deterministica sobre los alt-texts de Instagram, que traen mas señal de la que
parece): "text that says" delata flyers y capturas con caption; "Video/Photo by <autor>"
delata contenido de OTRA cuenta cuando el autor no se parece al negocio; "selfie" delata
retratos. Es la misma primera linea que ya usaba el prefiltro, ahora como unica linea.
Lo que se pierde sin ojos: detectar stock, fotos borrosas o material ajeno bien etiquetado.

CONTENIDO (plantillas bilingues por nicho con placeholders): el copy es generico por oficio
y VERAZ por construccion: ninguna plantilla contiene numeros, precios, resenas, zonas ni
credenciales; los unicos datos variables (nombre, ciudad, telefono, seguidores, posts)
vienen del research y se insertan solo si existen. Se pierde el sabor por-negocio ("30
anos de oficio de Carlos"), que era lo unico que de verdad aportaba la IA.
"""
import re

# ------------------------------------------------------------------ curacion
RE_AUTOR = re.compile(r'^(?:Video|Photo)\s+by\s+(.+?)\s+on\s', re.I)


def _norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def _mismo_autor(autor, negocio):
    # Solapamiento de 5-gramas: "Allandallplumbing" comparte "plumb" con "All & All
    # Plumbing". El primer intento comparaba prefijos y acusaba al propio negocio.
    a, n = _norm(autor), negocio
    if not a or not n:
        return True
    return any(a[i:i + 5] in n for i in range(max(1, len(a) - 4)))


def curar(hechos):
    """Devuelve (fotos_dict, None) o (None, motivo). Solo reglas, sin ojos.

    CALIBRADO contra feeds reales de oficios (2026-08-18): las fotos de trabajo llevan
    camisetas, vans y lonas con texto, asi que "text that says" NO puede ser descarte
    automatico (tumbaba 12/12 en un plomero perfectamente construible). Se descarta solo
    lo que el alt delata sin ambiguedad: texto SIN ningun objeto de escena (flyer puro),
    poster, selfies, disfraces/memes y contenido de otra cuenta. El resto pasa. Este
    curador es mas permisivo que unos ojos: es el costo aceptado de no usar vision.
    """
    fotos = hechos.get('fotos', [])
    caps = hechos.get('captions', [])
    negocio = _norm(hechos.get('nombre') or '') + _norm(hechos.get('ig', '').lstrip('@'))
    limpias, descartes = [], []
    for i, f in enumerate(fotos):
        alt = (caps[i] if i < len(caps) else '') or ''
        bajo = alt.lower()
        m = RE_AUTOR.match(alt)
        if m and not _mismo_autor(m.group(1), negocio):
            descartes.append((f, f'contenido de otra cuenta ({m.group(1)[:24]})')); continue
        if 'selfie' in bajo:
            descartes.append((f, 'selfie')); continue
        if any(k in bajo for k in ('poster', 'advertisement', 'costume', 'superman', 'meme')):
            descartes.append((f, 'grafico/disfraz/meme')); continue
        m2 = re.search(r'may be an image of (.+)', bajo, re.S)
        if m2:
            escena = re.sub(r"text that says\s*'[^']*'", '', m2.group(1)).replace(' and text', '')
            escena = re.sub(r'\btext\b\.?', '', escena).strip(' .,')
            if not escena:
                descartes.append((f, 'solo texto, sin escena (flyer)')); continue
        limpias.append(f)
    if len(limpias) < 5:
        det = '; '.join(f'{f}: {m}' for f, m in descartes[:4])
        return None, (f'Solo {len(limpias)} fotos pasan las reglas (liston 5). '
                      f'Descartadas {len(descartes)}: {det}')
    tiene_logo = bool(hechos.get('logo'))
    seleccion = {
        'hero': limpias[0],
        'nosotros': [limpias[1], limpias[2]],
        'galeria': (limpias[3:9] + limpias[1:3])[:6],
        'contacto': limpias[1],
        'logo': 'logo.jpg' if tiene_logo else limpias[0],
    }
    return seleccion, None


# ------------------------------------------------------------------ nichos
# Cada nicho: keywords de deteccion + hero + 4 cards de servicios + marquee + etiqueta.
# Regla de redaccion: NADA que afirme un hecho del negocio concreto. Verbos del oficio, si;
# promesas medibles, no.
def _b(es, en):
    return {'es': es, 'en': en}


NICHOS = {
 'plomeria': dict(
  kw=['plumb', 'plomer', 'drain', 'pipe', 'tuberia', 'destape'],
  etiqueta=_b('Plomería', 'Plumbing'),
  h1=(_b('La plomería de tu casa,', 'Your home plumbing,'), _b('en manos de ', 'handled by ')),
  marquee=['Plomería', 'Destapes', 'Fugas', 'Calentadores', 'Instalaciones', 'Florida'],
  cards=[
   (_b('Lo más pedido', 'Most requested'), _b('Fugas y destapes', 'Leaks and clogs'),
    _b('Localización y reparación de fugas, destape de drenajes y tuberías que vuelven a correr como deben.', 'Leak detection and repair, drain clearing, and pipes flowing the way they should.')),
   (_b('Instalación', 'Installs'), _b('Grifería y sanitarios', 'Fixtures'),
    _b('Instalación y reemplazo de llaves, lavamanos, inodoros y conexiones, con terminación limpia.', 'Faucets, sinks, toilets and connections installed or replaced, finished clean.')),
   (_b('Equipos', 'Equipment'), _b('Calentadores de agua', 'Water heaters'),
    _b('Diagnóstico, reparación e instalación de calentadores para que el agua caliente no falte.', 'Water heater diagnosis, repair and installation so hot water never runs out.')),
   (_b('Obra', 'Projects'), _b('Plomería de remodelación', 'Remodel plumbing'),
    _b('La plomería completa de tu baño o cocina nueva, hecha para pasar inspección.', 'Full plumbing for your new bath or kitchen, built to pass inspection.'))]),
 'electricista': dict(
  kw=['electric', 'iluminac', 'lighting', 'led', 'panel'],
  etiqueta=_b('Electricidad', 'Electrical'),
  h1=(_b('La electricidad de tu casa,', 'Your home electrical,'), _b('en manos de ', 'handled by ')),
  marquee=['Electricidad', 'Iluminación', 'Paneles', 'Tomacorrientes', 'Instalaciones', 'Florida'],
  cards=[
   (_b('Lo más pedido', 'Most requested'), _b('Reparaciones eléctricas', 'Electrical repairs'),
    _b('Tomacorrientes, interruptores, cortos y circuitos que fallan, resueltos con seguridad.', 'Outlets, switches, shorts and failing circuits, fixed safely.')),
   (_b('Iluminación', 'Lighting'), _b('Iluminación interior y exterior', 'Indoor and outdoor lighting'),
    _b('Lámparas, LED y luz de acento que cambian cómo se ve y se vive cada espacio.', 'Fixtures, LED and accent light that change how every space looks and feels.')),
   (_b('Paneles', 'Panels'), _b('Paneles y capacidad', 'Panels and capacity'),
    _b('Revisión y actualización de paneles para que la casa soporte lo que hoy se le conecta.', 'Panel checks and upgrades so the house handles everything you plug in today.')),
   (_b('Obra', 'Projects'), _b('Instalaciones nuevas', 'New installs'),
    _b('Cableado y puntos nuevos en remodelaciones y ampliaciones, hechos para pasar inspección.', 'New wiring and points for remodels and additions, built to pass inspection.'))]),
 'closets': dict(
  kw=['closet', 'cabinet', 'gabinete', 'woodwork', 'carpint', 'ebanist', 'madera'],
  etiqueta=_b('Closets y carpintería', 'Closets & millwork'),
  h1=(_b('Tu espacio, organizado', 'Your space, organized'), _b('a la medida por ', 'custom-built by ')),
  marquee=['Closets a medida', 'Carpintería', 'Gabinetes', 'Walk-ins', 'Diseño', 'Florida'],
  cards=[
   (_b('La especialidad', 'The specialty'), _b('Closets a medida', 'Custom closets'),
    _b('Walk-ins y closets diseñados para tu espacio real: cada zapato, bolso y prenda con su lugar.', 'Walk-ins and reach-ins designed for your actual space: every shoe, bag and garment in its place.')),
   (_b('Cocina', 'Kitchen'), _b('Gabinetes', 'Cabinets'),
    _b('Gabinetes a medida con herrajes de calidad y terminaciones que se sienten al abrir.', 'Custom cabinets with quality hardware and finishes you feel every time you open them.')),
   (_b('Hogar', 'Home'), _b('Muebles integrados', 'Built-ins'),
    _b('Centros de TV, oficinas en casa, lavanderías y bancos a medida que aprovechan cada rincón.', 'TV walls, home offices, laundries and benches that use every corner.')),
   (_b('Proceso', 'Process'), _b('Diseño y fabricación', 'Design and build'),
    _b('Medimos, diseñamos contigo y fabricamos: un solo responsable del plano a la entrega.', 'We measure, design with you and build: one team from drawing to handover.'))]),
 'pressure': dict(
  kw=['pressure', 'wash', 'lavado', 'softwash', 'roof clean'],
  etiqueta=_b('Pressure washing', 'Pressure washing'),
  h1=(_b('Tu propiedad, limpia', 'Your property, clean'), _b('otra vez gracias a ', 'again thanks to ')),
  marquee=['Pressure washing', 'Driveways', 'Techos', 'Fachadas', 'Pool decks', 'Florida'],
  cards=[
   (_b('Lo más pedido', 'Most requested'), _b('Driveways y aceras', 'Driveways and walkways'),
    _b('El concreto y los adoquines recuperan su color; la diferencia se ve desde la calle.', 'Concrete and pavers get their color back; you can see the difference from the street.')),
   (_b('Techos', 'Roofs'), _b('Techos y tejas', 'Roof cleaning'),
    _b('Lavado suave que quita las manchas oscuras sin castigar la teja.', 'Soft wash that lifts the dark stains without punishing the tile.')),
   (_b('Exteriores', 'Exteriors'), _b('Fachadas y cercas', 'Siding and fences'),
    _b('Paredes, cercas y screen enclosures libres de moho y salpicaduras de Florida.', 'Walls, fences and screen enclosures free of Florida mold and grime.')),
   (_b('Piscina', 'Pool'), _b('Pool decks y patios', 'Pool decks and patios'),
    _b('El área de la piscina limpia y sin resbalones, lista para usarse.', 'The pool area clean, slip-free and ready to enjoy.'))]),
 'pintura': dict(
  kw=['paint', 'pintur', 'pintor'],
  etiqueta=_b('Pintura', 'Painting'),
  h1=(_b('Tu casa, renovada', 'Your home, renewed'), _b('con la pintura de ', 'with paint by ')),
  marquee=['Pintura', 'Interiores', 'Exteriores', 'Gabinetes', 'Acabados', 'Florida'],
  cards=[
   (_b('Interiores', 'Interiors'), _b('Pintura interior', 'Interior painting'),
    _b('Paredes y techos con líneas limpias, preparación seria y un acabado que se nota.', 'Walls and ceilings with clean lines, real prep and a finish you can tell apart.')),
   (_b('Exteriores', 'Exteriors'), _b('Pintura exterior', 'Exterior painting'),
    _b('Protección y color para el sol y la lluvia de Florida, con materiales para exterior real.', 'Protection and color for Florida sun and rain, with true exterior-grade materials.')),
   (_b('Cocinas', 'Kitchens'), _b('Gabinetes renovados', 'Cabinet refinishing'),
    _b('El repintado que transforma la cocina sin cambiar los muebles.', 'The refinish that transforms the kitchen without replacing the cabinets.')),
   (_b('Detalle', 'Detail'), _b('Reparación y acabados', 'Repairs and finishes'),
    _b('Drywall, molduras y esos detalles que separan un trabajo correcto de uno impecable.', 'Drywall, trim and the details that separate a decent job from a flawless one.'))]),
 'landscaping': dict(
  kw=['landscap', 'lawn', 'jardin', 'garden', 'cesped', 'paisaj'],
  etiqueta=_b('Landscaping', 'Landscaping'),
  h1=(_b('Tu jardín, cuidado', 'Your yard, cared for'), _b('todo el año por ', 'year-round by ')),
  marquee=['Landscaping', 'Césped', 'Podas', 'Diseño', 'Mantenimiento', 'Florida'],
  cards=[
   (_b('Mantenimiento', 'Maintenance'), _b('Corte y cuidado del césped', 'Lawn care'),
    _b('Corte, bordes y limpieza con una frecuencia que mantiene el jardín siempre presentable.', 'Mowing, edging and cleanup on a schedule that keeps the yard presentable all the time.')),
   (_b('Plantas', 'Plants'), _b('Podas y siembras', 'Trimming and planting'),
    _b('Podas de arbustos y palmas, y siembras que le devuelven vida a los canteros.', 'Shrub and palm trimming, and planting that brings the beds back to life.')),
   (_b('Proyectos', 'Projects'), _b('Diseño de exteriores', 'Landscape design'),
    _b('Renovación de áreas verdes: piedra, mulch y plantas elegidas para el clima de Florida.', 'Outdoor makeovers: stone, mulch and plants chosen for Florida weather.')),
   (_b('Extras', 'Extras'), _b('Limpiezas y salidas puntuales', 'Cleanups and one-time visits'),
    _b('Limpiezas de temporada y trabajos puntuales cuando el jardín se salió de control.', 'Seasonal cleanups and one-time jobs when the yard got out of hand.'))]),
 'cleaning': dict(
  kw=['clean', 'limpieza', 'maid', 'janitorial'],
  etiqueta=_b('Limpieza', 'Cleaning'),
  h1=(_b('Tu espacio, impecable', 'Your space, spotless'), _b('gracias a ', 'thanks to ')),
  marquee=['Limpieza', 'Hogares', 'Oficinas', 'Deep cleaning', 'Move-out', 'Florida'],
  cards=[
   (_b('Hogares', 'Homes'), _b('Limpieza residencial', 'House cleaning'),
    _b('Limpieza regular o profunda, con el mismo cuidado que tendrías tú.', 'Regular or deep cleaning, with the same care you would put in yourself.')),
   (_b('Profunda', 'Deep'), _b('Deep cleaning', 'Deep cleaning'),
    _b('Cocinas, baños y esos rincones que la limpieza de rutina no alcanza.', 'Kitchens, baths and the corners routine cleaning never reaches.')),
   (_b('Mudanzas', 'Moves'), _b('Move-in / move-out', 'Move-in / move-out'),
    _b('La propiedad lista para entregar o estrenar, de puertas a zócalos.', 'The property ready to hand over or move into, doors to baseboards.')),
   (_b('Negocios', 'Business'), _b('Oficinas y locales', 'Offices and shops'),
    _b('Espacios de trabajo que reciben clientes limpios todos los días.', 'Workspaces that greet customers clean every single day.'))]),
 'handyman': dict(
  kw=['handyman', 'remodel', 'renovation', 'reparac', 'construc', 'drywall', 'roof', 'floor'],
  etiqueta=_b('Remodelación', 'Remodeling'),
  h1=(_b('Los arreglos de tu casa,', 'Your home projects,'), _b('resueltos por ', 'handled by ')),
  marquee=['Remodelación', 'Reparaciones', 'Baños', 'Cocinas', 'Pisos', 'Florida'],
  cards=[
   (_b('Lo más pedido', 'Most requested'), _b('Reparaciones del hogar', 'Home repairs'),
    _b('Esa lista de pendientes que nunca se arregla sola: puertas, drywall, herrajes, detalles.', 'The to-do list that never fixes itself: doors, drywall, hardware, details.')),
   (_b('Baños', 'Baths'), _b('Baños renovados', 'Bath remodels'),
    _b('De la ducha al piso: baños que se transforman con un solo equipo responsable.', 'From shower to floor: bathrooms transformed by one accountable crew.')),
   (_b('Cocinas', 'Kitchens'), _b('Cocinas', 'Kitchens'),
    _b('Gabinetes, encimeras y acabados que convierten la cocina en otra.', 'Cabinets, counters and finishes that make it a different kitchen.')),
   (_b('Superficies', 'Surfaces'), _b('Pisos y pintura', 'Floors and paint'),
    _b('Pisos nuevos y pintura con preparación seria, para un cambio que dura.', 'New floors and paint with real prep, for a change that lasts.'))]),
}
GENERICO = dict(
 kw=[], etiqueta=_b('Servicios', 'Services'),
 h1=(_b('Tu proyecto,', 'Your project,'), _b('en manos de ', 'handled by ')),
 marquee=['Servicio local', 'Calidad', 'Trato directo', 'Presupuesto claro', 'Florida', 'Confianza'],
 cards=[
  (_b('El oficio', 'The craft'), _b('Nuestro trabajo', 'What we do'),
   _b('Lo que publicamos en Instagram es lo que hacemos: mira el feed y júzganos por ahí.', 'What we post on Instagram is what we do: check the feed and judge us by it.')),
  (_b('Trato', 'Service'), _b('Atención directa', 'Direct service'),
   _b('Hablas con quien hace el trabajo, no con una central: acuerdos claros y sin intermediarios.', 'You talk to the person doing the work, not a call center: clear agreements, no middlemen.')),
  (_b('Presupuesto', 'Quotes'), _b('Cotización sin compromiso', 'No-strings quotes'),
   _b('Cuéntanos qué necesitas y te decimos qué lleva y cuánto cuesta antes de empezar.', 'Tell us what you need and we tell you what it takes and what it costs before starting.')),
  (_b('Cercanía', 'Local'), _b('Negocio local', 'Local business'),
   _b('De tu misma zona: llegamos rápido y respondemos después de entregar.', 'From your own area: quick to arrive and still answering after handover.'))])


def detectar_nicho(hechos):
    texto = ' '.join([hechos.get('bio_raw') or '', hechos.get('ig') or '',
                      hechos.get('nombre') or '', hechos.get('nicho') or '']).lower()
    for nombre, n in NICHOS.items():
        if any(k in texto for k in n['kw']):
            return nombre, n
    return 'generico', GENERICO


# ------------------------------------------------------------------ contenido
def _partir_nombre(nombre):
    palabras = (nombre or '').split()
    if len(palabras) <= 1:
        return nombre or '', ''
    mitad = max(1, len(palabras) // 2)
    return ' '.join(palabras[:mitad]), ' '.join(palabras[mitad:])


def construir(hechos, fotos):
    nicho_id, n = detectar_nicho(hechos)
    nombre = (hechos.get('nombre') or hechos.get('ig', '').lstrip('@') or hechos['slug']).strip()
    ciudad = (hechos.get('ciudad') or 'Florida').split('(')[0].strip().rstrip(',')
    handle = hechos.get('ig', '').lstrip('@') or hechos['slug']
    tel = hechos.get('phone') or hechos.get('telefono_publicado')
    seguidores, posts = hechos.get('followers'), hechos.get('posts')
    lang = hechos.get('idioma_principal', 'es')
    ig_url = f'https://www.instagram.com/{handle}/'
    if tel:
        digitos = re.sub(r'[^0-9]', '', tel)
        cta_url, cta_ic = f'tel:+{digitos if digitos.startswith("1") else "1"+digitos}', 'telefono'
        cta_label = _b('Llámanos o escríbenos', 'Call or text us')
    else:
        cta_url, cta_ic = f'https://ig.me/m/{handle}', 'instagram'
        cta_label = _b('Escríbenos por Instagram', 'Message us on Instagram')
    a, b_ = _partir_nombre(nombre)
    mono = ''.join(w[0] for w in nombre.split()[:2]).upper() or 'SF'
    et = n['etiqueta']

    strip = []
    if posts:
        strip.append({'valor': str(posts), 'count': re.sub(r'[^0-9]', '', str(posts)),
                      'etiqueta': _b('Publicaciones en Instagram', 'Posts on Instagram')})
    if seguidores:
        strip.append({'valor': str(seguidores),
                      'etiqueta': _b('Seguidores en Instagram', 'Followers on Instagram')})
    strip.append({'valor': et['es'], 'etiqueta': _b('El oficio', 'The trade')})
    strip.append({'valor': ciudad.split(',')[0], 'etiqueta': _b('Zona de trabajo', 'Service area')})
    while len(strip) < 4:
        strip.append({'valor': '1:1', 'etiqueta': _b('Trato directo', 'Direct contact')})
    strip = strip[:4]

    dm = (f"Hola {nombre}! Les armé un website con sus fotos reales de Instagram, para que quien "
          f"busque {et['es'].lower()} en {ciudad.split(',')[0]} los encuentre: "
          f"https://siteforge-demos.odd-forest-9504.workers.dev/{hechos['slug']}/ "
          "Ya está listo y no les cuesta nada verlo. Si no les gusta, lo bajo hoy mismo. ¿Se los dejo activo?")

    content = {
     'slug': hechos['slug'], 'base': 'dark-v2', 'lang': lang,
     'cta_url': cta_url, 'cta_icono': cta_ic, 'cta_label': cta_label,
     'ig_url': ig_url, 'ig_handle': f'@{handle}',
     'brand': {'name': nombre, 'nav_a': a, 'nav_b': b_ or et['es'], 'mono': mono,
               'footmark': a or nombre, 'logo': f"assets/raw/{fotos['logo']}"},
     'head': {
      'title': f"{nombre} · {et['es']} en {ciudad}",
      'description': f"{nombre}: {et['es'].lower()} en {ciudad}. Mira nuestro trabajo real y escríbenos.",
      'og_title': f"{nombre} · {et['es']}",
      'og_description': f"{et['es']} en {ciudad}. Trabajo real publicado en Instagram.",
      'og_image': f"assets/raw/{fotos['hero']}", 'icon': f"assets/raw/{fotos['logo']}"},
     'jsonld': {
      '@context': 'https://schema.org', '@type': 'HomeAndConstructionBusiness',
      'name': nombre, 'description': f"{et['es']} en {ciudad}.",
      'address': {'@type': 'PostalAddress', 'addressLocality': ciudad.split(',')[0],
                  'addressRegion': 'FL', 'addressCountry': 'US'},
      **({'telephone': tel} if tel else {}),
      'image': f"assets/raw/{fotos['hero']}", 'sameAs': [ig_url]},
     'nav': {'experiencia': _b('Nosotros', 'About us'), 'metodo': _b('Proceso', 'Process'),
             'opiniones': _b('Por qué elegirnos', 'Why choose us'), 'ubicacion': _b('Contacto', 'Contact')},
     'hero': {
      'eyebrow': _b(f"{ciudad} · {et['es']}", f"{ciudad} · {et['en']}"),
      'script': _b('Trabajo real, trato directo.', 'Real work, direct service.'),
      'h1_a': n['h1'][0], 'h1_b': n['h1'][1],
      'h1_shine': _b(a or nombre, a or nombre),
      'parrafo': _b(
       f"Somos {nombre}, {et['es'].lower()} en {ciudad}. Nuestro trabajo está publicado en Instagram: "
       "puedes ver cómo trabajamos antes de escribirnos, y hablas directo con quien hace el trabajo.",
       f"We are {nombre}, {et['en'].lower()} in {ciudad}. Our work is posted on Instagram: "
       "you can see how we work before reaching out, and you talk straight to the people doing the job."),
      'senal_icono': 'instagram',
      'senal': (_b(f'{seguidores} seguidores en Instagram', f'{seguidores} followers on Instagram')
                if seguidores else _b(f'Encuéntranos: @{handle}', f'Find us: @{handle}')),
      'imagen': fotos['hero'], 'imagen_alt': f"Trabajo de {nombre} en {ciudad}",
      'tarjeta': {'tag': _b('Atención directa', 'Direct line'),
                  'destacado': tel or f'@{handle}',
                  'pie': _b(ciudad, ciudad)}},
     'strip': strip,
     'marquee': n['marquee'],
     'nosotros': {
      'eyebrow': _b('Nosotros', 'About us'),
      'h2_a': _b('Un equipo,', 'One team,'), 'h2_shine': _b('un solo responsable', 'one accountable crew'),
      'parrafo_1': _b(
       f"{nombre} es un negocio local de {ciudad}. El que responde el mensaje es el mismo que llega "
       "a hacer el trabajo: sin centrales telefónicas ni intermediarios.",
       f"{nombre} is a local {ciudad} business. Whoever answers your message is who shows up to do "
       "the work: no call centers, no middlemen."),
      'parrafo_2': _b(
       "Nuestro trabajo está a la vista en Instagram: lo publicamos porque no tenemos nada que "
       "esconder. Mira el feed antes de decidir.",
       "Our work is out in the open on Instagram: we post it because we have nothing to hide. "
       "Check the feed before you decide."),
      'imagen_1': fotos['nosotros'][0], 'imagen_1_alt': f"Trabajo de {nombre}",
      'imagen_2': fotos['nosotros'][1], 'imagen_2_alt': f"Trabajo de {nombre} en {ciudad}",
      'stats': ([{'valor': str(posts), 'count': re.sub(r'[^0-9]', '', str(posts)),
                  'etiqueta': _b('Publicaciones', 'Posts')}] if posts else []) +
               ([{'valor': str(seguidores), 'etiqueta': _b('Seguidores', 'Followers')}] if seguidores else []) +
               [{'valor': '1:1', 'etiqueta': _b('Trato directo', 'Direct contact')},
                {'valor': ciudad.split(',')[0], 'etiqueta': _b('Zona', 'Area')}],
      'stats_fix':None, 'avatar': fotos['logo'], 'avatar_alt': f'Logo de {nombre}', 'avatar_pie': _b(ciudad, ciudad)},
     'proceso': {
      'eyebrow': _b('Tu proyecto, paso a paso', 'Your project, step by step'),
      'h2_a': _b('Así trabajamos', 'How we work'), 'h2_shine': _b('contigo', 'with you'),
      'pasos': [
       {'titulo': _b('Escríbenos', 'Get in touch'),
        'texto': _b('Cuéntanos qué necesitas; con una foto del espacio o del problema ya podemos orientarte.',
                    'Tell us what you need; a photo of the space or the problem is enough to point you right.')},
       {'titulo': _b('Presupuesto claro', 'Clear quote'),
        'texto': _b('Te decimos qué lleva el trabajo y cuánto cuesta antes de empezar, sin letra chica.',
                    'We tell you what the job takes and what it costs before starting, no fine print.')},
       {'titulo': _b('El trabajo', 'The job'),
        'texto': _b('Llegamos con todo lo necesario y lo ejecutamos con el cuidado que se ve en nuestro feed.',
                    'We arrive with everything needed and execute with the care you see on our feed.')},
       {'titulo': _b('Entrega', 'Handover'),
        'texto': _b('Revisamos juntos el resultado y dejamos el área limpia. Y guardas nuestro número para la próxima.',
                    'We walk the result together and leave the area clean. And you keep our number for next time.')}]},
     'servicios': {
      'h2_a': _b('Lo que', 'What we'), 'h2_shine': _b('hacemos', 'do'),
      'nota': _b('Cada trabajo se cotiza según lo que necesite. Escríbenos y te damos el detalle sin compromiso.',
                 'Every job is quoted on what it needs. Message us and we will walk you through it, no strings attached.'),
      'cta': _b('Consultar', 'Ask about it'),
      'cards': [{'tag': t, 'titulo': ti, 'texto': tx} for t, ti, tx in n['cards']],
      'pie': _b('¿No ves lo que necesitas? Escríbenos igual: si es de nuestro oficio, lo hacemos.',
                'Need something not listed? Message us anyway: if it is our trade, we do it.')},
     'galeria': {
      'h2_a': _b('Trabajos', 'Real'), 'h2_shine': _b('reales', 'work'),
      'tiles': [{'img': f, 'caption': et, 'alt': f'Trabajo de {nombre} en {ciudad}'}
                for f in fotos['galeria']]},
     'social_proof': {
      'modo': 'razones',
      'eyebrow': _b('Por qué elegirnos', 'Why choose us'),
      'h2_a': _b('Tres razones', 'Three reasons'), 'h2_shine': _b('para escribirnos', 'to message us'),
      'subtitulo': _b('Nuestro trabajo está publicado en Instagram: revísalo antes de decidir.',
                      'Our work is posted on Instagram: check it before you decide.'),
      'cta': _b('Ver el trabajo en Instagram', 'See the work on Instagram'),
      'items': [
       {'icono': 'escudo', 'titulo': _b('Trabajo a la vista', 'Work out in the open'),
        'texto': _b('Publicamos lo que hacemos. No te pedimos confianza ciega: mira cómo quedaron los anteriores.',
                    'We post what we do. We do not ask for blind trust: look at how the previous jobs turned out.')},
       {'icono': 'telefono', 'titulo': _b('El que responde es el que llega', 'Who answers is who shows up'),
        'texto': _b('Hablas directo con el equipo, acuerdas con el equipo, y el equipo hace el trabajo.',
                    'You talk to the crew, agree with the crew, and the crew does the work.')},
       {'icono': 'whatsapp', 'titulo': _b('Presupuesto antes de empezar', 'Quote before we start'),
        'texto': _b('Sabes qué lleva y cuánto cuesta antes del primer martillazo. Sin sorpresas a mitad de obra.',
                    'You know what it takes and what it costs before the first hammer swing. No mid-job surprises.')}]},
     'contacto': {
      'eyebrow': _b('Contacto', 'Contact'),
      'h2_a': _b('Escríbenos desde', 'Reach us from'), 'h2_shine': ciudad.split(',')[0],
      'imagen': fotos['contacto'], 'imagen_alt': f'Trabajo de {nombre}',
      'cards': ([{'icono': 'telefono', 'titulo': _b('Llámanos o escríbenos', 'Call or text'),
                  'texto': _b('La vía más rápida: cuéntanos qué necesitas y te respondemos con el detalle.',
                              'The fastest way: tell us what you need and we reply with the details.'),
                  'url': cta_url if tel else ig_url, 'enlace': tel or f'@{handle}'}] if tel else []) +
               [{'icono': 'instagram', 'titulo': _b('Instagram', 'Instagram'),
                 'texto': _b('Ahí publicamos el trabajo. También puedes escribirnos por DM.',
                             'Where the work gets posted. You can also reach us by DM.'),
                 'url': ig_url, 'enlace': f'@{handle}'},
                {'icono': 'mapa', 'titulo': _b('Zona de trabajo', 'Service area'),
                 'texto': _b(f'{ciudad} y alrededores.', f'{ciudad} and nearby.'),
                 'url': ig_url, 'enlace': ciudad}]},
     'cta_final': {
      'script': _b('Trabajo real, trato directo.', 'Real work, direct service.'),
      'h2_a': _b('Tu proyecto', 'Your project'), 'h2_shine': _b('empieza con un mensaje', 'starts with a message'),
      'parrafo': _b('Cuéntanos qué necesitas y te respondemos con ideas y presupuesto, sin compromiso.',
                    'Tell us what you need and we reply with ideas and a quote, no strings attached.')},
     'footer': {
      'descripcion': _b(f"{et['es']} en {ciudad}. Trabajo real publicado en Instagram.",
                        f"{et['en']} in {ciudad}. Real work posted on Instagram."),
      'linea_contacto': ciudad,
      'enlace_contacto': (_b(f'Llámanos · {tel}', f'Call or text · {tel}') if tel
                          else _b(f'DM · @{handle}', f'DM · @{handle}')),
      'social_extra': []},
    }
    content['nosotros']['stats'] = content['nosotros']['stats'][:3]
    content['nosotros'].pop('stats_fix', None)
    return content, dm, nicho_id
