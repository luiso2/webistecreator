# SITEFORGE: Pipeline de demos premium para cold outreach

> Fuente de verdad del pipeline. La ejecutan: (a) el comando local `/siteforge`, (b) la rutina cloud diaria `siteforge-daily`.
> Origen: pipeline probado 2026-07-15 con 5 head spas de Miami (ver `data/processed.json`).

## Entrada
Uno de:
- **Handle/nombre**: un Instagram handle o nombre de negocio (modo directo; aqui SI se aceptan negocios con website propio, con angulo rediseño).
- **Descubrimiento**: encontrar `daily_count` negocios NUEVOS segun `config.json` que cumplan rating >= `min_rating`, reseñas >= `min_reviews`, NO esten en `data/processed.json` y (con `require_no_website: true`) NO tengan website propio.

## Descubrimiento: como encontrar negocios SIN website
Buscar "mejor <nicho> en <ciudad>" NO funciona: los que rankean ahi ya tienen SEO y website. Buscar donde viven los que no tienen:
1. **Directorios de booking**: paginas de categoria/ciudad de Booksy, perfiles `*.glossgenius.com`, `book.squareup.com`, Fresha, Vagaro, Mangomint. Un negocio cuyo UNICO link publico es su plataforma de booking es el candidato ideal.
2. **Instagram local**: hashtags y geotags del nicho (#headspamiami, #lashesmiami, etc.) y perfiles de negocio con solo linktree/wa.me/booking en la bio, sin dominio propio.
3. **Google Maps por zonas**: fichas sin campo website (Google muestra "Add website") en las `extra_areas` del config, no solo el centro.
Verificacion OBLIGATORIA antes de aceptar un candidato: probar `<negocio>.com` y variantes, revisar links de bio de IG y el dominio del email. Si tiene website propio: DESCARTAR sin gastar cupo (solo anotarlo en el reporte como descartado con su URL). Los negocios con website SOLO se procesan si llegan por la cola del panel o por comando directo.
Si el nicho principal no da candidatos: bajar en orden por `fallback_niches` y ampliar por `extra_areas`. Si aun asi no hay: reportar honestamente "0 nuevos" con la lista de descartados. NUNCA rellenar el cupo con negocios con website.

## Fase 1: Research (un agente por negocio, en paralelo)
Recolectar SOLO datos reales, nunca inventar:
1. Buscar el negocio: Google/web. Identificar: Instagram (handle + url), pagina de booking (GlossGenius / Booksy / Square / Mangomint / Fresha / Vagaro / WhatsApp), Yelp, Facebook, y **si tiene website propio**.
2. **CHECK CRITICO DE WEBSITE PROPIO** (leccion MaRe): probar dominios obvios (`<negocio>.com`, el dominio del email si lo tienen, links en bio). Si tiene website propio, marcar `has_own_site: true`; el angulo del outreach cambia a "propuesta de rediseño" y NUNCA afirmar "no tienen website".
3. Servicios: menu COMPLETO con nombres exactos, precios y duraciones desde la pagina de booking (los payloads/JSON-LD de Booksy y las APIs de Mangomint son las fuentes mas fiables).
4. Imagenes: descargar 6-14 fotos REALES del negocio (galeria del booking, fotos de Google Maps `lh3.googleusercontent.com`, covers de reels de IG via `instagram.com/api/v1/users/web_profile_info/?username=X` con header `x-ig-app-id: 936619743392459`). curl con UA de Chrome. Verificar cada archivo con `file` (JPEG/PNG/WebP, >15KB) y borrar los rotos. Instagram directo: maximo 2 intentos.
5. Reviews: 3-5 quotes reales de Google con nombre, verbatim, idioma original.
6. Brand: colores/estetica real (logo, decoracion, feed) para derivar la paleta.
7. Contacto: email publico (business_email de IG, mailto en booking, dominio propio), telefono, hours.
8. **Idioma principal** del negocio (captions de IG, reseñas, menu): registrar `language: "es" | "en"` en data.json y en el registro. Define el idioma por defecto del site bilingue y el idioma del dm_message.
Salida: `output/<slug>/data.json` + `output/<slug>/assets/raw/*`.

## Fase 2: Build (un agente por negocio)
- Leer `DESIGN.md` + el template ejemplar: `templates/dark/index.html` (base oscura, ejemplar Mizu) o `templates/light/index.html` (base clara, ejemplar Amani). Elegir base segun el brand real del negocio.
- Misma estructura SIEMPRE (nav glass, hero con rating real, strip de confianza, experiencia, ritual 4 pasos, servicios con precios reales, galeria, testimonios, ubicacion con mapa embed, CTA final, footer): solo cambian paleta, fotos, textos y datos.
- Copiar `templates/assets/tailwind.js` a `output/<slug>/assets/tailwind.js` y referenciarlo LOCAL (`<script src="assets/tailwind.js">`): el CDN de Tailwind no soporta SRI/CORS.
- CTA de reserva SIEMPRE al canal real del negocio. Boton flotante: WhatsApp si ese es su canal, si no icono de calendario al booking.
- JSON-LD `HealthAndBeautyBusiness` (o el tipo que aplique) con datos reales.
- PROHIBIDO: em-dash (verificar `grep -c "—" = 0`), datos inventados, superlativos sin prueba.
- Footer: "Powered by Merktop" -> https://merktop.com.

## Fase 3: Verificacion (gate, no saltar)
- Toda ruta de imagen referenciada existe en disco.
- HTML completo (`<!DOCTYPE html>` ... `</html>`), em-dash = 0, JSON-LD parsea.
- Responsive: sin overflow horizontal a 390px (si hay browser disponible; si no, revisar que no haya widths fijos).

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
- Actualizar `data/processed.json`: `{slug, name, city, ig, url_demo, has_own_site, email, outreach: sent|pending_manual|skipped, fecha}`. NUNCA reprocesar un slug ya registrado (idempotencia).
- Reporte al usuario (email a jose@merktop.com via Resend): negocios procesados, URLs live, emails enviados/entregados, pendientes manuales, errores.

## Panel (siteforge-panel)
- UI live: https://siteforge-panel.odd-forest-9504.workers.dev (worker `ui/`, KV `SITEFORGE_KV`, auth por hash SHA-256 del access key; el key vive SOLO en `~/Desktop/siteforge/.env` local y en el localStorage del navegador del usuario).
- API con key (header `x-sf-key`): GET `/api/state` (registry + queue), POST `/api/queue` {input}, POST `/api/queue/done` {id}, POST `/api/registry` (array completo).
- API publica (autorizada por el usuario 2026-07-16, para que la rutina cloud trabaje sin credenciales): GET `/api/public/queue` (solo items pending: id/input/created) y POST `/api/public/queue/done` {id, slug?, name?, url_demo?} (url_demo se valida server-side contra *.odd-forest-9504.workers.dev).

## Forja de la cola (rutinas siteforge-queue y siteforge-queue-b)
- DOS rutinas cloud desfasadas (minutos :22 y :52): espera maxima ~30 min. Cada una lee `/api/public/queue`; si no hay pendientes TERMINA de inmediato (sin email, sin commit). Los items "processing" no aparecen como pendientes (asi las dos forjas no chocan); si un item queda en processing sin avance por 90 min, el panel lo devuelve a la cola (auto-rescate).
- MODO RAPIDO (objetivo ~10 min/negocio): paralelizar con subagentes si estan disponibles; research time-boxed (~8 min): menu con precios publicados, 4-8 imagenes verificadas, 3 reseñas verbatim, check de website propio. Nunca rellenar con datos inventados.
- Progreso en vivo: reportar etapas research/build/verify/commit a `/api/public/queue/progress` (el panel muestra temporizador y barra).
- Procesa hasta 3 items por pasada (los pedidos manuales SI pueden tener website propio: angulo rediseño). Dedupe contra `data/processed.json` y `data/queue_done.json` antes de procesar.
- Al terminar cada item: actualiza registro (url_demo = https://siteforge-demos.odd-forest-9504.workers.dev/<slug>/), agrega el id a `data/queue_done.json`, commit + push, y marca done en `/api/public/queue/done` con slug/name/url_demo.
- Reporte por email a jose@merktop.com SOLO si proceso algo.

## Deploy automatico de demos (Workers Builds)
- El worker `siteforge-demos` (config `demos/wrangler.jsonc`) sirve TODO `output/` como assets: cada site queda en `/<slug>/`.
- El repo esta conectado a Cloudflare Workers Builds: cada push a main redeploya `siteforge-demos` automaticamente (deploy command: `npx wrangler deploy -c demos/wrangler.jsonc`). Asi la rutina cloud publica demos sin credenciales.
- Los workers "bonitos" por negocio (`<slug>-demo.*.workers.dev`) se deployan en la sesion local de aprobacion antes del outreach.

## Limites de seguridad
- Maximo `daily_count` (default 3) negocios nuevos por corrida.
- Nunca enviar email sin `delivered` check; nunca dos emails al mismo negocio (registry).
- Si una fase falla 2 veces para un negocio, marcarlo `failed` con motivo y seguir con el resto (anti-bucle).
