# FORGE-BRIEF: guia unica de la forja (rutinas siteforge-queue)

> Condensado operativo de PIPELINE.md + DESIGN.md para que una corrida de forja lea UN solo archivo.
> Si un caso no esta cubierto aqui, PIPELINE.md y DESIGN.md son la fuente de verdad.

## 0. Arranque paralelo (primer minuto, OBLIGATORIO)
Si el item de la cola es SOLO un nombre, un handle o "nombre + ciudad": es un encargo directo del usuario; hacer el discovery completo de ESE negocio (encontrar su Booksy/booking, verificar website propio, IG) y construirlo con la maxima prioridad, mismo pipeline.
**PASO 1 (segundos, SIEMPRE primero)**: `python3 scripts/booksy_dossier.py <booksy_url> <slug>`.
Un solo comando extrae TODO a `output/<slug>/data.json`: nombre, tipo schema, direccion, geo, rating,
numero de reseñas, menu COMPLETO con precios y duraciones, horarios, staff, IG, telefono si esta
publicado, hasta 12 reseñas VERBATIM con autor, idioma (es/en) y candidatos a website propio.
Ademas descarga las fotos validadas y genera `output/<slug>/_sheet.jpg` para la curacion visual.
Dossiers por plataforma (todos escriben `data.json` + fotos + `_sheet.jpg` en segundos):
- Booksy: `scripts/booksy_dossier.py <url> <slug>` (menu+precios+duraciones+staff+IG+telefono+RESEÑAS verbatim+rating). La mejor fuente.
- GlossGenius (`<slug>.glossgenius.com`): `scripts/glossgenius_dossier.py <url> <slug>` (menu+fotos+TELEFONO+EMAIL+IG+about+flag has_own_site). NO trae reseñas (estan en Google) -> usar variante SIN-testimonios (ver abajo). Fotos suelen ser STOCK: curar fuerte.
- Fresha (`fresha.com/a/<slug>`): `scripts/fresha_dossier.py <url> <slug>` (rating+reviewsCount+telefono+servicios+RESEÑAS si las hay+galeria). Galeria chica (3-6 fotos): si <5 reales, complementar con IG o failed.
- Square (`<slug>.square.site`), Setmore, Acuity (`<slug>.as.me`), Vagaro, JaneApp: NO tienen dossier (Square bloquea curl). Research manual: seguir el external_url de la bio de IG y sacar fotos+menu del IG real.
Si el item no trae URL: UNA busqueda para encontrar su pagina de booking.
PROHIBIDO gastar rondas de WebFetch/subagentes en menu, precios, reseñas o fotos cuando el dossier
ya los trae: construir DIRECTO desde data.json.

**Beauty Square / My Suite (salon suites Miami)**: `data/beautysquare_tenants.txt` lista ~43 tenants (negocios independientes, casi todos SIN website propio) con su URL de plataforma. Al procesar uno: usar el dossier de su plataforma; si es Square/Vagaro/Acuity/Setmore/JaneApp, sacar fotos reales del IG del negocio (la plataforma no da fotos buenas).

**Variante SIN-testimonios** (para GlossGenius y cualquier negocio sin reseñas verificables): en vez de la seccion OPINIONES con rating/estrellas/quotes, poner una seccion "Por que <negocio>" con 3 cards de especialidades reales (derivadas del about/servicios), NUNCA inventar reseñas ni rating. Quitar del hero/strip/experiencia todo `data-count` de rating y `★`. Sitio de referencia ya construido: `output/royaltrends/index.html` (GlossGenius, locs) y `output/olguitashairstudio/index.html` (GlossGenius, color). Derivar de esos, no de pureartistry, cuando no haya reseñas.

**PASO 2 (en paralelo con la curacion, lo unico que el script no resuelve)**:
- (a) Website propio: probar con curl los `website_candidates` del dossier + 1-2 busquedas
  (`"<nombre>" <ciudad> website`). Subdominios de plataforma NO cuentan. Si existe: `has_own_site: true`.
- (b) Email publico: bio de IG / linktree / About de Facebook. Si no aparece en ~2 min: null y seguir.

**IG media: SOLO como rescate** cuando el _sheet.jpg muestre stock, graficos con texto o menos de
5 fotos reales utilizables (leccion Paintbox). `web_profile_info` esta ROTO (400): no intentarlo.
Time-box total del research: ~3 min. La velocidad recorta el research, JAMAS la calidad del build.

## 1. Checks criticos de research
- **Website propio** (leccion MaRe): probar `<negocio>.com`, dominio del email, links de bio. Si existe: `has_own_site: true` y el angulo cambia a "propuesta de rediseño" (NUNCA afirmar "no tienen website"). Subdominios de plataforma (square.site, glossgenius.com) NO cuentan como website propio.
- NUNCA inventar servicios, precios, duraciones ni resenas. Si tras busqueda exhaustiva no hay UN dato verificable de precios ni resenas (solo feed de IG y citas por DM): marcar `failed` con motivo detallado (precedente @salaslash_ 2026-07-18), no fabricar.

## 2. Build (derivacion anclada desde esqueleto v2: el metodo probado en batches 1-3)
- EMPEZAR COPIANDO `templates/dark-v2/index.html` o `templates/light-v2/index.html` segun el brand real; derivarlo con UN script Python de transformacion anclada. Escribir HTML desde cero o editar a mano esta PROHIBIDO. **La receta completa (orden de operaciones, regexes de secciones, proteccion del badge, cambio de idioma, gotchas) esta en `templates/SKELETONS-V2.md`: leerla ANTES de construir.**
- Fotos: el dossier del paso 1 ya descargo la galeria validada y genero `output/<slug>/_sheet.jpg`. LEER el sheet (curacion VISUAL obligatoria) antes de elegir hero/experiencia/galeria. Si el sheet muestra stock o graficos con texto: rescatar fotos reales de IG (regla de rescate de la seccion 0) o marcar failed.
- Estructura fija heredada del esqueleto: nav glass, hero con rating real, strip con contadores, experiencia, metodo 4 pasos, servicios en 4 cards (card 2 destacada), galeria 1 ancho + 5 tiles con tile-cap, opiniones VERBATIM, ubicacion con mapa embed, CTA final, footer "Powered by Merktop" -> https://merktop.com.
- Copiar `templates/assets/tailwind.js` a `output/<slug>/assets/tailwind.js` y `templates/.assetsignore-template` a `output/<slug>/.assetsignore`.
- **Bilingue obligatorio**: `data-es`/`data-en` en todo texto traducible + toggle ES|EN en nav + localStorage + navigator.language. `lang` del html = idioma principal. NO se traducen: nombres exactos de servicios, precios, nombre del negocio, quotes de resenas.
- **Performance (leccion bety: congelaba el navegador)**: imagenes de galeria/hero max 1000-1300px (sips -Z), `will-change` SOLO en 2-4 elementos que animan de verdad, videos `preload="metadata"`, max 2-3 animaciones infinitas de imagenes grandes simultaneas.
- Videos IG en galeria: `<video muted loop playsinline autoplay preload="metadata" poster>` clase `ig-video` + IntersectionObserver que reproduce en viewport y pausa fuera; click alterna play-pausa. NO desactivarlos por prefers-reduced-motion (el control manual cubre accesibilidad). Referencia: output/betynailsrp.
- CTA de reserva SIEMPRE al canal real. JSON-LD del tipo que aplique con datos reales.

## 3. Puerta de calidad (gate, no saltar NUNCA)
1. **Imagenes**: toda ruta referenciada existe en disco Y NINGUNA es de 0 bytes: verificar con `file` que cada una decodifica (leccion bety: 4 archivos vacios = tiles en blanco en el site live).
2. **Curaduria VISUAL** (leccion Iconic): MIRAR cada foto antes de elegirla (contact sheet), no elegir por nombre. En galeria SOLO resultados terminados: ojos abiertos, cliente favorecida, buena luz. PROHIBIDO: ojos cerrados a medio procedimiento, piel irritada, POV con cafe, capturas con texto/caption encima, selfies o retratos del dueno (dueno = solo avatar pequeno en experiencia). Menos fotos buenas > rellenar con malas.
3. **Copy de titulares**: adaptados del ejemplar, nunca frases de estado tipo "All 26 services, fully visible" o "Your appointment is close by". Si suena a descripcion de UI, esta mal.
4. **PROHIBIDO `<details>`/acordeones**: menus grandes = 3-4 destacados en cards glass + categorias completas visibles en bloques glass con grid servicio+precio.
5. **Contraste**: ink oscuro legible, text-shine en rangos profundos, banda final oscura. Nada lavado.
6. **Correr `python3 scripts/gate.py <slug> --lang <es|en> --forbid "<leftovers del esqueleto>"` y NO avanzar hasta GATE OK.** El script verifica em-dash 0, assets existentes que decodifican, JSON-LD valido, todos los markers v2+v3, applyLang/<html lang> coherentes y leftovers. En --forbid van SIEMPRE: nombre/artista/ciudad/calle/booksy-id del esqueleto y 2-3 palabras del nicho anterior (adaptar tile-caps a los servicios reales y el foot-mark al nombre de la marca).
7. Responsive: sin overflow horizontal a 390px (sin widths fijos).
8. Si el negocio no encaja en el formato (ecommerce, mayorista, sin servicios reservables): `failed` con motivo, no forzar un demo pobre.

## 4. Registro, panel y reporte
- `data/processed.json`: {slug, name, city, ig, url_demo: https://siteforge-demos.odd-forest-9504.workers.dev/<slug>/, has_own_site, email, phone, outreach: pending_manual|draft, status: staging, language, dm_message, thumb, fecha}. `thumb` = URL ABSOLUTA de la og:image del site (url_demo + ruta de la imagen del og:image del index.html): el panel la usa como miniatura de la tarjeta. NUNCA reprocesar un slug registrado.
- **dm_message** (SIEMPRE): version corta del outreach para DM/WhatsApp, max 450 chars, idioma principal, link del demo, angulo segun has_own_site.
- Ids procesados -> `data/queue_done.json` (failed: con motivo). Commit + push a main. Si el push es rechazado: `git pull --rebase`; si `data/processed.json` queda en conflicto, fusionar POR SLUG (base = `git show origin/main:data/processed.json`, agregar solo los slugs propios que falten via `git show REBASE_HEAD:data/processed.json`), NUNCA escoger un lado entero; `git add` + `git rebase --continue` + push. El push publica los demos solo (Workers Builds).
- Verificacion live tras el push: `curl` del demo con User-Agent de navegador (python-urllib recibe 403 de Cloudflare) hasta obtener 200; los assets nuevos pueden dar 404 por 1-2 min de propagacion: reintentar antes de diagnosticar. Confirmar que el HTML live = local y que el thumb decodifica.
- Panel publico: GET /api/public/queue, POST /api/public/queue/progress {id, stage: research|build|verify|commit}, POST /api/public/queue/done {id, slug, name, url_demo, dm}. Ademas, por CADA negocio construido: POST /api/public/registry-upsert con {slug, name, city, ig, url_demo, has_own_site, email, phone, language, dm_message, thumb, fecha} para que aparezca en la UI al instante. Item FALLIDO: POST done con {id, failed: true, motivo: "<resumen corto del porque>"} para que el panel lo muestre en rojo con su motivo.
- PROHIBIDO contactar negocios por cualquier canal. Reporte unico por Resend a jose@merktop.com solo si se proceso algo; con email publico incluir boton mailto "ENVIAR ESTE CORREO (1 tap)" pre-llenado.

## 5. Reglas duras
Sin em-dash en ningun output. Nunca inventar datos. Una fase falla 2 veces -> failed con motivo y seguir. Nunca procesar el mismo negocio dos veces. Maximo 3 items por pasada.
