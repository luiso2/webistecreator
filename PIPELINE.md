# SITEFORGE: Pipeline de demos premium para cold outreach

> Fuente de verdad del pipeline. La ejecutan: (a) el comando local `/siteforge`, (b) la rutina cloud diaria `siteforge-daily`.
> Origen: pipeline probado 2026-07-15 con 5 head spas de Miami (ver `data/processed.json`).

## Entrada
Uno de:
- **Handle/nombre**: un Instagram handle o nombre de negocio (modo directo; aqui SI se aceptan negocios con website propio, con angulo rediseño).
- **Descubrimiento**: encontrar `daily_count` negocios NUEVOS segun `config.json` que cumplan rating >= `min_rating`, reseñas >= `min_reviews`, NO esten en `data/processed.json` y (con `require_no_website: true`) NO tengan website propio.
- **Búsqueda filtrada del panel**: un item con `request.type: "discovery"`, `niche`, `location`, `count` (1-3) y `require_no_website: true`. Busca SOLO dentro de la ubicación solicitada, por ejemplo `electricistas` en `España`; no cae a `config.json`, a otro país ni a negocios con website propio.

## Descubrimiento: como encontrar negocios SIN website (GOOGLE PRIMERO)
Buscar "mejor <nicho> en <ciudad>" NO funciona: los que rankean ahi ya tienen SEO y website. Fuentes en ORDEN DE PRIORIDAD:
1. **GOOGLE (fuente principal)**: fichas de Google Maps/Google Business por zona (`<nicho> en <area>` en Google, revisando el local pack y maps): buscar fichas SIN campo website (Google muestra "Add website" o el boton de website apunta a booking de terceros). Google es la columna vertebral de la gestion: de ahi salen rating, numero de reseñas, telefono, horarios, fotos del negocio y las reseñas verbatim que van al site y al registro. Barrer las `extra_areas` del config, no solo el centro.
2. **Directorios de booking**: paginas de categoria/ciudad de Booksy, perfiles `*.glossgenius.com`, `book.squareup.com`, Fresha, Vagaro, Mangomint. Un negocio cuyo UNICO link publico es su plataforma de booking es candidato ideal (verificar su ficha de Google igual: rating/reviews minimos).
3. **Instagram local**: hashtags y geotags del nicho (#headspamiami, #lashesmiami, etc.) y perfiles de negocio con solo linktree/wa.me/booking en la bio, sin dominio propio (cruzar con su ficha de Google).
Verificacion OBLIGATORIA antes de aceptar un candidato: probar `<negocio>.com` y variantes, revisar links de bio de IG y el dominio del email. Si tiene website propio: DESCARTAR sin gastar cupo (solo anotarlo en el reporte como descartado con su URL). Los negocios con website SOLO se procesan si llegan por la cola del panel o por comando directo.
Si el nicho principal no da candidatos: bajar en orden por `fallback_niches` y ampliar por `extra_areas`. Si aun asi no hay: reportar honestamente "0 nuevos" con la lista de descartados. NUNCA rellenar el cupo con negocios con website.

## Fase 1: Research (un agente por negocio, en paralelo)
Recolectar SOLO datos reales, nunca inventar:
1. Buscar el negocio: Google/web. Identificar: Instagram (handle + url), pagina de booking (GlossGenius / Booksy / Square / Mangomint / Fresha / Vagaro / WhatsApp), Yelp, Facebook, y **si tiene website propio**.
   **OBLIGATORIO (leccion betynailsrp)**: revisar SIEMPRE el `external_url` de la bio de Instagram (el endpoint web_profile_info lo devuelve). Suele ser el booking (square.site, *.glossgenius.com, Booksy) o un linktree/poplme que hay que abrir y extraer sus links. NUNCA declarar "sin menu verificable" sin haber seguido ese link. Nota: subdominios de plataforma (square.site, glossgenius.com) NO cuentan como website propio.
2. **CHECK CRITICO DE WEBSITE PROPIO** (leccion MaRe): probar dominios obvios (`<negocio>.com`, el dominio del email si lo tienen, links en bio). Si tiene website propio, marcar `has_own_site: true`; el angulo del outreach cambia a "propuesta de rediseño" y NUNCA afirmar "no tienen website".
3. Servicios: menu COMPLETO con nombres exactos, precios y duraciones desde la pagina de booking (los payloads/JSON-LD de Booksy y las APIs de Mangomint son las fuentes mas fiables).
4. Imagenes Y VIDEOS: descargar 6-14 fotos REALES del negocio. **Si el input es un handle de Instagram, el media sale PRIORITARIAMENTE de su feed de IG**: `instagram.com/api/v1/users/web_profile_info/?username=X` con header `x-ig-app-id: 936619743392459` devuelve `edge_owner_to_timeline_media`:
   - Fotos: `display_url` de cada nodo. Los nodos `GraphSidecar` (carruseles) traen `edge_sidecar_to_children` con MAS fotos por post: expandirlas (son la mejor fuente de volumen).
   - **Videos: los nodos `is_video: true` traen `video_url`: descargar 1-3 como `ig-N.mp4`** (verificar con `file` que es MP4) y usar su `display_url` como poster. En el site van como tiles de galeria: `<video muted loop playsinline autoplay preload="metadata" poster="...">` con la clase `ig-video` y un JS con IntersectionObserver que los reproduce SIEMPRE en viewport (silenciados) y los pausa fuera; click/tap alterna play-pausa (ese control manual cubre la accesibilidad; NO desactivarlos por prefers-reduced-motion o los usuarios con Reduce Motion del sistema veran solo la imagen fija). Patron de referencia: output/betynailsrp.
   - Complementar con galeria del booking y fotos de Google Maps (`lh3.googleusercontent.com`). curl con UA de Chrome. Verificar cada archivo con `file` (JPEG/PNG/WebP >15KB, MP4) y borrar los rotos. Si IG bloquea: maximo 2 intentos y pasar a las otras fuentes.
5. Reviews: 3-5 quotes reales de Google con nombre, verbatim, idioma original.
6. Brand: colores/estetica real (logo, decoracion, feed) para derivar la paleta.
7. Contacto: email publico. PROFUNDIZAR (la mayoria de negocios sin website tampoco publican email, buscar en TODAS estas fuentes antes de rendirse): business_email del endpoint web_profile_info de IG, mailto en la pagina de booking, JSON/payload del venue en Booksy/GlossGenius/Square (a veces expone email), pagina de linktree/poplme/beacons de la bio (abrirla SIEMPRE), seccion About de su pagina de Facebook, y dominio propio si existe. Registrar tambien telefono y hours.
8. **Idioma principal** del negocio (captions de IG, reseñas, menu): registrar `language: "es" | "en"` en data.json y en el registro. Define el idioma por defecto del site bilingue y el idioma del dm_message.
Salida: `output/<slug>/data.json` + `output/<slug>/assets/raw/*`.

## Fase 2: Build (un agente por negocio)
- Leer `DESIGN.md` + el template ejemplar: `templates/dark/index.html` (base oscura, ejemplar Mizu) o `templates/light/index.html` (base clara, ejemplar Amani). Elegir base segun el brand real del negocio.
- Misma estructura SIEMPRE (nav glass, hero con rating real, strip de confianza, experiencia, ritual 4 pasos, servicios con precios reales, galeria, testimonios, ubicacion con mapa embed, CTA final, footer): solo cambian paleta, fotos, textos y datos.
- **PERFORMANCE OBLIGATORIA (leccion bety 2026-07-17: el site congelaba el navegador)**: redimensionar TODAS las imagenes de galeria/hero a max 1000px de ancho (sips -Z 1000, calidad ~82) antes del build; NUNCA `will-change` en masa (solo en 2-4 elementos que animan de verdad); videos con `preload="metadata"`; maximo 2-3 animaciones infinitas simultaneas de imagenes grandes.
- Copiar `templates/assets/tailwind.js` a `output/<slug>/assets/tailwind.js` y referenciarlo LOCAL (`<script src="assets/tailwind.js">`): el CDN de Tailwind no soporta SRI/CORS.
- CTA de reserva SIEMPRE al canal real del negocio. Boton flotante: WhatsApp si ese es su canal, si no icono de calendario al booking.
- JSON-LD `HealthAndBeautyBusiness` (o el tipo que aplique) con datos reales.
- PROHIBIDO: em-dash (verificar `grep -c "—" = 0`), datos inventados, superlativos sin prueba.
- Footer: "Powered by Merktop" -> https://merktop.com.

## Fase 3: Verificacion + PUERTA DE CALIDAD (gate, no saltar NUNCA)
Chequeos mecanicos:
- Toda ruta de imagen referenciada existe en disco.
- HTML completo (`<!DOCTYPE html>` ... `</html>`), em-dash = 0, JSON-LD parsea.
- Responsive: sin overflow horizontal a 390px (si hay browser disponible; si no, revisar que no haya widths fijos).
- Marcadores del design system presentes: `text-shine`, `orb`, `glass`, `btn-3d`, `reveal`, `Playfair`, `merktop-badge`, `data-es` (bilingue), `assets/tailwind.js`.

Puerta de calidad (leccion Sandra 2026-07-16: el site salio "con template" pero degradado):
1. **PROHIBIDO `<details>`/acordeones y cualquier control colapsable** para el menu de servicios. Menus grandes (20+ servicios): seccion de destacados con 3-4 cards glass grandes + "menu completo" agrupado por categoria en bloques glass con grid de filas servicio+precio, todo visible. Se puede resumir una categoria con "y N mas" + CTA al booking, jamas colapsar.
2. **Curaduria de imagenes**: usar las mejores disponibles (interiores, tratamientos, resultados). Selfies o retratos del dueño NUNCA como tiles de galeria: solo como avatar pequeño en la seccion de experiencia. Fotos borrosas o con clutter se descartan. Si quedan menos de 5 buenas, mejor menos secciones con buenas fotos que rellenar con malas.
   - **Curaduria VISUAL obligatoria (leccion Iconic 2026-07-17)**: antes de elegir tiles, MIRAR cada foto (contact sheet o una por una), no elegir por nombre de archivo. En galeria SOLO resultados terminados: ojos abiertos, cliente favorecida, buena luz. PROHIBIDO en galeria: ojos cerrados a medio procedimiento, piel irritada, POV del artista con cafe, capturas con texto/caption encima, posters de reels casuales. Esas tomas solo sirven (a veces) en la seccion de experiencia como ambiente.
   - **Copy de titulares**: los headings de seccion se ADAPTAN del ejemplar, nunca se inventan frases literales de estado tipo "All 26 services, fully visible" o "Your appointment is close by". Si un heading suena a descripcion de UI y no a copy de marca, esta mal.
3. **Contraste**: ink oscuro legible sobre base clara (tipo #33261f), text-shine en rangos profundos, banda final oscura como el ejemplar. Nada lavado tono-sobre-tono.
4. **Fidelidad al ejemplar**: el build EMPIEZA copiando la estructura del template ejemplar y editandola. Escribir el HTML desde cero es una violacion del pipeline aunque el resultado "se parezca".
5. **Formato (revisado 2026-07-29)**: que el negocio no sea salon/spa NO lo descarta. Un negocio local sin citas reservables (exportacion de vehiculos, detailing, landscaping, cleaning, handyman, food truck, fotografia) se construye con la VARIANTE ADAPTADA: las secciones cuyo dato el negocio no publica se omiten o se sustituyen, nunca se rellenan. Resenas -> 3 razones reales; precios -> "se cotiza, escribenos"; direccion -> foto real en vez de mapa; booking -> CTA al canal real (WhatsApp/DM/telefono). Tabla completa y criterios en FORGE-BRIEF seccion 0.b; referencia viva: `output/prestigeautocargo/content.json`.
   `failed` se reserva para cuando faltan los MINIMOS: menos de 5 fotos reales propias, ningun canal de contacto publico, no poder describir el negocio sin inventarlo, o ecommerce/mayorista puro que necesitaria catalogo con carrito (precedente: @myspabeautysupply). El liston es "¿puedo construirlo sin fabricar un solo dato?", no "¿es un salon?".

## Fase 4: Deploy (Cloudflare Workers static assets)
- Por negocio: `wrangler.jsonc` = `{"name": "<slug>-<nicho>", "compatibility_date": "<reciente>", "assets": {"directory": ".", "html_handling": "auto-trailing-slash"}}` y `.assetsignore` con `wrangler.jsonc` y `data.json`.
- `npx wrangler deploy -c output/<slug>/wrangler.jsonc` (local: OAuth ya logueado; cloud: requiere env `CLOUDFLARE_API_TOKEN`).
- Verificar: pagina 200, `data.json` 404, HTML live identico al local (reintentar 1 vez por propagacion).
- Si no hay credenciales de deploy (caso rutina cloud): guardar el site en `output/`, marcar `pending_deploy` en el registro y commitear al repo. El deploy real lo hace la siguiente sesion local (`/siteforge pendientes`), que usa el OAuth de wrangler ya logueado en la Mac: no se necesita API token nuevo.

## Fase 5: Outreach (SIEMPRE con aprobacion humana por lote)
- El pipeline REDACTA los borradores; el envio requiere aprobacion explicita del usuario para ese lote concreto:
  - En sesion interactiva (`/siteforge`): presentar los borradores y esperar el OK del usuario antes de enviar.
  - En la rutina cloud: NUNCA enviar al negocio; adjuntar los borradores al reporte diario para que el usuario los apruebe.
- Solo si hay email publico del negocio. Sender: `Michael Vargas <michael@go.merktop.com>` (NUNCA merktop.com directo), reply-to `jose@merktop.com`, tag `campaign=siteforge`.
- Angulo segun `has_own_site`: false -> "les construi un website de muestra"; true -> "propuesta alternativa de diseño premium".
- Estructura probada: saludo con nombre si se conoce, 1 linea de como los encontre (su rating real), el link del demo, que no toca su operacion de reservas, oferta de dejarlo en su dominio o retirarlo sin compromiso. Corto, espanol (o el idioma del negocio), sin em-dash, firmado Michael Vargas / Merktop.
- Idempotency-Key: `siteforge-<slug>-<fecha>`. Verificar `last_event: delivered`.
- Sin email publico: registrar `outreach: pending_manual` con telefono/IG para WhatsApp o DM manual.
- **dm_message (SIEMPRE, para todo negocio)**: version corta del outreach para DM/WhatsApp (max ~450 chars), en el IDIOMA PRINCIPAL del negocio, con el link del demo incluido, angulo segun has_own_site. Guardarlo en el registro (`dm_message`) e incluirlo como `dm` en el POST de done al panel. El panel lo usa para el boton "DM" (copia + abre el hilo de Instagram) y "WhatsApp" (texto pre-llenado via wa.me).

## Fase 6: Registro y reporte
- Actualizar `data/processed.json`: `{slug, name, city, ig, url_demo, has_own_site, email, outreach: sent|pending_manual|skipped, thumb, fecha}`. `thumb` = URL absoluta de la og:image del site (miniatura de la tarjeta en el panel). NUNCA reprocesar un slug ya registrado (idempotencia).
- **Reflejar en el panel (obligatorio tras cada negocio construido)**: POST a `https://siteforge-panel.odd-forest-9504.workers.dev/api/public/registry-upsert` con `{slug, name, city, ig, url_demo, has_own_site, email, phone, language, dm_message, thumb, fecha}` (JSON). El endpoint es publico con validacion server-side; asi los demos aparecen en la UI al instante sin credenciales.
- Reporte al usuario (email a jose@merktop.com via Resend): negocios procesados, URLs live, emails enviados/entregados, pendientes manuales, errores.

## Panel (siteforge-panel)
- UI live: https://siteforge-panel.odd-forest-9504.workers.dev (worker `ui/`, KV `SITEFORGE_KV`, auth por hash SHA-256 del access key; el key vive SOLO en `~/Desktop/siteforge/.env` local y en el localStorage del navegador del usuario).
- API con key (header `x-sf-key`): GET `/api/state` (registry + queue), POST `/api/queue` con `{input}` para un negocio puntual o `{request:{type:"discovery", niche, location, count}}` para encontrar 1-3 negocios sin website, POST `/api/queue/done` {id}, POST `/api/registry` (array completo).
- API publica (autorizada por el usuario 2026-07-16, para que la rutina cloud trabaje sin credenciales): GET `/api/public/queue` (items pending: id/input/request/created) y POST `/api/public/queue/done` {id, slug?, name?, url_demo?, sites?}. `sites` admite los 1-3 resultados `{slug,name,url_demo,dm?}` de una búsqueda filtrada; url_demo se valida server-side contra *.odd-forest-9504.workers.dev.

## Forja de la cola (rutinas siteforge-queue)
- Los slots de forja se ejecutan cada ~7 min. Cada uno lee `/api/public/queue`; si hay un item, debe llamar inmediatamente `POST /api/public/queue/claim {id}`. Solo procesa si recibe `200`; un `409` indica que otra forja ya lo tomó. Esto evita trabajo duplicado y hace que el siguiente pedido disponible se inicie en el próximo slot. Un item sin avance vuelve a estar disponible tras **12 min** (auto-rescate).
- MODO RAPIDO (objetivo ~7 min/negocio): reclamar UN solo item al comenzar su research, no un lote entero. Usar los dossiers y `research_ig.py` antes de investigar manualmente; research time-boxed (~3 min cuando existe dossier o IG): menu con precios publicados, 4-8 imagenes verificadas, 3 reseñas verbatim y check de website propio. Nunca rellenar con datos inventados.
- Progreso en vivo: reportar etapas research/build/verify/commit a `/api/public/queue/progress` (el panel muestra temporizador y barra).
- Procesa hasta 3 items por pasada si el tiempo de la rutina alcanza (los pedidos manuales SI pueden tener website propio: angulo rediseño). Tras cerrar cada uno, entonces reclama el siguiente. Dedupe contra `data/processed.json` y `data/queue_done.json` antes de procesar.
- **Item `request.type: "discovery"`**: leer el filtro estructurado, buscar candidatos del `niche` exclusivamente en `location`, y verificar website propio antes de gastar el cupo. `require_no_website` es siempre true: un dominio propio descarta al candidato, mientras que Booksy, GlossGenius, Google Business, Facebook, Instagram o WhatsApp no cuentan como website propio. Construir hasta `count` candidatos válidos, hacer el upsert del registro por CADA uno y cerrar el id padre UNA vez con `sites: [{slug,name,url_demo,dm}, ...]`. Si no se encuentra ninguno dentro del filtro, cerrar como failed con un motivo; nunca ampliar el país, cambiar el nicho ni llenar con negocios que ya tienen web.
- Al terminar cada item: actualiza registro (url_demo = https://siteforge-demos.odd-forest-9504.workers.dev/<slug>/), agrega el id a `data/queue_done.json`, commit + push, y marca done en `/api/public/queue/done` con slug/name/url_demo.
- Reporte por email a jose@merktop.com SOLO si proceso algo.

## Deploy automatico de demos (Workers Builds)
- El worker `siteforge-demos` (config `demos/wrangler.jsonc`) sirve TODO `output/` como assets: cada site queda en `/<slug>/`.
- El Tailwind runtime se sirve una sola vez desde `/_shared/tailwind.js`. El worker reescribe las referencias historicas al responder el HTML y `output/.assetsignore` excluye las copias por sitio. No quitar esa reescritura ni volver a publicar `**/assets/tailwind.js`: son cientos de copias identicas que ralentizan cada deploy.
- El repo esta conectado a Cloudflare Workers Builds: cada push a main redeploya `siteforge-demos` automaticamente (deploy command: `npx wrangler deploy -c demos/wrangler.jsonc`). Asi la rutina cloud publica demos sin credenciales.
- Los workers "bonitos" por negocio (`<slug>-demo.*.workers.dev`) se deployan en la sesion local de aprobacion antes del outreach.

## Limites de seguridad
- Maximo `daily_count` segun `config.json` (actualmente 20) negocios nuevos por corrida.
- Nunca enviar email sin `delivered` check; nunca dos emails al mismo negocio (registry).
- Si una fase falla 2 veces para un negocio, marcarlo `failed` con motivo y seguir con el resto (anti-bucle).
