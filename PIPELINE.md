# SITEFORGE: Pipeline de demos premium para cold outreach

> Fuente de verdad del pipeline. La ejecutan: (a) el comando local `/siteforge`, (b) la rutina cloud diaria `siteforge-daily`.
> Origen: pipeline probado 2026-07-15 con 5 head spas de Miami (ver `data/processed.json`).

## Entrada
Uno de:
- **Handle/nombre**: un Instagram handle o nombre de negocio (modo directo).
- **Descubrimiento**: usar `config.json` (nicho + ciudad) para encontrar `daily_count` negocios NUEVOS que cumplan: rating >= `min_rating`, reseñas >= `min_reviews`, y que NO esten en `data/processed.json`.

## Fase 1: Research (un agente por negocio, en paralelo)
Recolectar SOLO datos reales, nunca inventar:
1. Buscar el negocio: Google/web. Identificar: Instagram (handle + url), pagina de booking (GlossGenius / Booksy / Square / Mangomint / Fresha / Vagaro / WhatsApp), Yelp, Facebook, y **si tiene website propio**.
2. **CHECK CRITICO DE WEBSITE PROPIO** (leccion MaRe): probar dominios obvios (`<negocio>.com`, el dominio del email si lo tienen, links en bio). Si tiene website propio, marcar `has_own_site: true`; el angulo del outreach cambia a "propuesta de rediseño" y NUNCA afirmar "no tienen website".
3. Servicios: menu COMPLETO con nombres exactos, precios y duraciones desde la pagina de booking (los payloads/JSON-LD de Booksy y las APIs de Mangomint son las fuentes mas fiables).
4. Imagenes: descargar 6-14 fotos REALES del negocio (galeria del booking, fotos de Google Maps `lh3.googleusercontent.com`, covers de reels de IG via `instagram.com/api/v1/users/web_profile_info/?username=X` con header `x-ig-app-id: 936619743392459`). curl con UA de Chrome. Verificar cada archivo con `file` (JPEG/PNG/WebP, >15KB) y borrar los rotos. Instagram directo: maximo 2 intentos.
5. Reviews: 3-5 quotes reales de Google con nombre, verbatim, idioma original.
6. Brand: colores/estetica real (logo, decoracion, feed) para derivar la paleta.
7. Contacto: email publico (business_email de IG, mailto en booking, dominio propio), telefono, hours.
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

## Fase 6: Registro y reporte
- Actualizar `data/processed.json`: `{slug, name, city, ig, url_demo, has_own_site, email, outreach: sent|pending_manual|skipped, fecha}`. NUNCA reprocesar un slug ya registrado (idempotencia).
- Reporte al usuario (email a jose@merktop.com via Resend): negocios procesados, URLs live, emails enviados/entregados, pendientes manuales, errores.

## Limites de seguridad
- Maximo `daily_count` (default 3) negocios nuevos por corrida.
- Nunca enviar email sin `delivered` check; nunca dos emails al mismo negocio (registry).
- Si una fase falla 2 veces para un negocio, marcarlo `failed` con motivo y seguir con el resto (anti-bucle).
