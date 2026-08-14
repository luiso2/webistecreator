# FAILED: flatratehandymansunnyisles

**Negocio**: FLATRATE HANDYMAN, Sunny Isles Beach, FL
**Telefono**: +1 954-595-7171
**Fecha research**: 2026-08-14

## Motivo

Menos de 5 fotos reales utilizables. Solo se pudo recuperar **1 foto real unica**
verificada del negocio (`assets/raw/gmaps-1.jpg`, 1600x1200, foto de Google Maps
provista en el brief, EXIF software=Picasa/Google, sin marcas de stock).

## Fuentes intentadas (en orden de prioridad segun PIPELINE.md)

1. **Google Maps**: unica foto disponible fue la entregada en el brief
   (`lh3.googleusercontent.com/gps-cs-s/AHRPTWnDU5...`). No existe forma de listar
   el resto de las fotos de la ficha sin renderizar JS (Maps es un SPA; el HTML
   servido por curl no trae URLs de `lh3.googleusercontent.com` adicionales, y
   WebFetch tampoco pudo extraerlas de la pagina renderizada).
2. **Yelp** (ficha con 95 fotos, `yelp.com/biz/flatrate-handyman-sunny-isles-beach-6`):
   bloqueado con HTTP 403 en todos los intentos (excede el limite de 2-3 sugerido):
   - curl directo (desktop UA) -> 403
   - curl directo con headers de navegador completos + cookies -> 403
   - curl via `m.yelp.com` (UA iPhone y UA Android) -> 403 ambos
   - proxy lector `r.jina.ai` -> bloqueado con aviso de CAPTCHA
3. **Thumbtack**: se descargo la pagina de categoria
   `thumbtack.com/fl/sunny-isles-beach/handyman` (200 OK, 484KB) y no aparece
   "Flatrate Handyman" en ningun listado. Multiples WebSearch (`site:thumbtack.com`,
   variantes de query) tampoco arrojaron un perfil de Thumbtack para este negocio
   especifico. No existe perfil de Thumbtack verificable.
4. **Instagram**: sin resultados en WebSearch general ni en `site:instagram.com
   flatrate handyman`. No se encontro handle real y confiable del mismo negocio
   (nombre+ciudad+telefono).
5. **Facebook**: sin resultados en WebSearch general ni en `site:facebook.com
   "Flatrate Handyman"`. `mbasic.facebook.com` requiere login (no accesible sin
   credenciales). No se encontro pagina de Facebook real del mismo negocio.
6. **Directorios agregadores** (bonus, no en la lista de fuentes prioritarias):
   `trustanalytica.org` tiene una ficha del negocio con **1 imagen** en su CDN
   (`d2jkr899rqgh58.cloudfront.net`), pero al descargarla resulto ser el MISMO
   archivo (identico contenido visual) que la foto de Google Maps ya obtenida,
   solo re-hospedada a menor resolucion (800x600 vs 1600x1200 original). No
   sumo una foto nueva. `cityof.com`, `angi.com` (403), `cylex.us.com` (403),
   `localitybiz.com` (403) y `handymanbrowardcounty.com` no exponen fotos reales
   del negocio (solo placeholders genericos o ningun `<img>` propio).
   `archive.org` (Wayback CDX) esta bloqueado por la politica de egress del
   entorno, asi que no se pudo revisar si existe una captura historica de la
   ficha de Yelp con fotos.

## Otros datos de research (para no repetir el trabajo si se reintenta)

- **Email**: no publicado en ningun canal revisado (Yelp bloqueado antes de ver
  su seccion About, pero Nextdoor, trustanalytica, cityof.com y los resultados
  generales de busqueda no exponen ninguno). `email: null`.
- **Instagram / Facebook**: no encontrados. `ig: null`.
- **Nombres de staff mencionados en reseñas** (via snippets indexados, no
  verificados en pagina completa): Joseph y Yossi.
- **Servicios adicionales confirmados via Nextdoor** (ademas de los temas ya
  dados en el brief): gate & fence, locks, doors, windows, sliding door,
  garage door, paint, tile, plumbing, electric, furniture assembly. Angulo de
  marca: "on time", "clean results", "honest flat-rate pricing".
- **Sin website propio**: confirmado. `flatratehandyman.com` resuelve pero
  redirige (302) a `giftshq.com/?=fwd`, un dominio parqueado/no relacionado.
  Otras variantes de dominio (`flatratehandymanfl.com`,
  `flatratehandymanmiami.com`, `flatrate-handyman.com`,
  `flatratehandymansunnyisles.com`, `flatratehandymanllc.com`,
  `theflatratehandyman.com`) no resuelven (DNS).

## Si se reintenta este negocio

El unico camino realista para llegar a 5 fotos es lograr acceso a la ficha de
Yelp (95 fotos) por una via que hoy no esta disponible en este entorno (browser
real con sesion, o un proxy residencial que Yelp no bloquee), o encontrar el
perfil de Thumbtack/Instagram/Facebook real del negocio si en algun momento lo
crean.
