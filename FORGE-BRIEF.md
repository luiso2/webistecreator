# FORGE-BRIEF: guia unica de la forja (rutinas siteforge-queue)

> Condensado operativo de PIPELINE.md + DESIGN.md para que una corrida de forja lea UN solo archivo.
> Si un caso no esta cubierto aqui, PIPELINE.md y DESIGN.md son la fuente de verdad.

## 0. Arranque paralelo (primer minuto, OBLIGATORIO)
Si el item de la cola es SOLO un nombre, un handle o "nombre + ciudad": es un encargo directo del usuario; hacer el discovery completo de ESE negocio (encontrar su Booksy/booking, verificar website propio, IG) y construirlo con la maxima prioridad, mismo pipeline.
Por cada item pendiente, lanzar EN PARALELO subagentes (Task/Agent):
- (a) Menu y precios: pagina de booking (Booksy/GlossGenius/Square/Fresha/Vagaro/Mangomint; sus payloads JSON-LD/venue son la fuente mas fiable). SEGUIR SIEMPRE el `external_url` de la bio de IG (suele ser el booking o un linktree que hay que abrir). NUNCA declarar "sin menu verificable" sin seguir ese link.
- (b) Media del feed de IG: `instagram.com/api/v1/users/web_profile_info/?username=X` con header `x-ig-app-id: 936619743392459`. Fotos de `display_url`; expandir carruseles (`edge_sidecar_to_children`, mejor fuente de volumen); 1-3 videos de nodos `is_video` (`video_url` como ig-N.mp4, poster = display_url). Verificar CADA archivo con `file` (JPEG/PNG/WebP >15KB, MP4) y borrar rotos. Si IG bloquea: 2 intentos max, pasar a booking y fotos de Google Maps (lh3.googleusercontent.com, curl con UA de Chrome).
- (c) Ficha de Google: rating, numero de resenas, telefono, horarios, 3-5 resenas VERBATIM con nombre e idioma original.
- (d) Email profundo + idioma: business_email de IG, mailto del booking, payload del venue, linktree/beacons de la bio, About de Facebook, dominio propio. Registrar tambien telefono. Idioma principal (captions/resenas/menu) -> `language: es|en`.
Mientras, el agente principal copia el template ejemplar y prepara el esqueleto. Time-box del research: ~8 min. La velocidad recorta el research, JAMAS la calidad del build.

## 1. Checks criticos de research
- **Website propio** (leccion MaRe): probar `<negocio>.com`, dominio del email, links de bio. Si existe: `has_own_site: true` y el angulo cambia a "propuesta de rediseño" (NUNCA afirmar "no tienen website"). Subdominios de plataforma (square.site, glossgenius.com) NO cuentan como website propio.
- NUNCA inventar servicios, precios, duraciones ni resenas. Si tras busqueda exhaustiva no hay UN dato verificable de precios ni resenas (solo feed de IG y citas por DM): marcar `failed` con motivo detallado (precedente @salaslash_ 2026-07-18), no fabricar.

## 2. Build (derivacion anclada desde esqueleto v2: el metodo probado en batches 1-3)
- EMPEZAR COPIANDO `templates/dark-v2/index.html` o `templates/light-v2/index.html` segun el brand real; derivarlo con UN script Python de transformacion anclada. Escribir HTML desde cero o editar a mano esta PROHIBIDO. **La receta completa (orden de operaciones, regexes de secciones, proteccion del badge, cambio de idioma, gotchas) esta en `templates/SKELETONS-V2.md`: leerla ANTES de construir.**
- Fotos: `python3 scripts/booksy_gallery.py <booksy_url> <slug>` descarga la galeria, valida cada imagen y genera `output/<slug>/_sheet.jpg`. LEER el sheet (curacion VISUAL obligatoria) antes de elegir hero/experiencia/galeria. Si la galeria de Booksy es stock/graficos con texto: rescatar fotos reales de IG (ver seccion 0b) o marcar failed.
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
