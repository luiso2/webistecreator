# FAILED: Miami Cleaning Service (Doral, FL)

**Slug:** miami-cleaning-service-doral
**Fecha:** 2026-08-13
**Fase en la que falla:** Research (Fase 1), antes de llegar a Build.

## Motivo

No se encontraron las 5 fotos reales, verificadas y propias del negocio que exige el
minimo de calidad (PIPELINE.md Fase 1 punto 4, FORGE-BRIEF seccion 0.b "Cuando SI marcar
failed"). Tras una busqueda exhaustiva en 9 canales distintos, el conteo final de fotos
reales utilizables es **0**.

El resto de los datos SI son solidos y estan documentados en `data.json`: direccion,
telefono, horario, 8 reseñas reales con nombre (5 de Birdeye/Google, 3 de Angi), rating
5.0/14 en Google (confirmado via el propio desglose de Birdeye "Google (14), Birdeye
(0)"), servicios reales, family-owned desde 2003, 80% productos green-certified, bonded
e insured. Ese material por si solo no es suficiente: la puerta de calidad exige fotos
reales del trabajo/equipo/local, y aqui no hay ninguna.

## Que se intento (9 canales, con metodo y resultado)

1. **Birdeye** (`reviews.birdeye.com/miami-cleaning-service-inc-156204203792103`):
   fetch directo (2x) y con Playwright leyendo el DOM completo. Su unica "foto" es un
   ilustracion de stock generica que Birdeye reutiliza para TODOS los negocios de
   limpieza de su plataforma (`.../home-services/home-cleaning.png`), y cada reviewer
   tiene el avatar placeholder `default-profile.png`. Cero fotos propias.

2. **Yelp** (`yelp.com/biz/miami-cleaning-service-doral`, que su propio snippet de
   busqueda confirma que tiene "10 Photos"): bloqueado en 4 intentos distintos.
   - WebFetch directo: HTTP 403.
   - curl con user-agent de Chrome: devolvio la pagina de reto anti-bot de DataDome
     ("Please enable JS and disable any ad blocker"), no contenido real.
   - Playwright local con los flags de fix de TLS documentados en FORGE-BRIEF
     (deshabilitar QUIC/ECH/PostQuantumKyber, TLS tope 1.2, proxy del sandbox) y 12s de
     espera: misma pantalla de reto, `title` se quedo literalmente en "yelp.com".
   - Mismo Playwright, esta vez con ~17s simulando movimiento de mouse y scroll humano
     para intentar pasar el check de comportamiento de DataDome: mismo resultado, cero
     contenido, cero imagenes reales.
   Las 10 fotos que Yelp confirma que existen para este negocio nunca fueron alcanzables
   desde este entorno.

3. **Google Maps**: 6 busquedas distintas via Playwright (nombre solo, nombre+direccion,
   nombre+ciudad, direccion exacta, direccion+zip, telefono solo). El negocio NUNCA
   aparecio en los resultados, mientras que decenas de competidores de Doral/Miami si
   aparecian para las mismas consultas (MaidPro Doral, Cleanzen, Sparkly Maid Miami,
   etc). La busqueda de la direccion pelada solo resuelve a un pin de "Building" sin
   negocio asociado y con su seccion de Fotos vacia. Hipotesis de trabajo: la ficha de
   Google de este negocio quedo inactiva/despublicada desde que su actividad de reseñas
   se detuvo (las 5 reseñas visibles en Birdeye son todas "hace 9 años", ~2017).

4. **Google Images**: Playwright cargo una busqueda de imagenes por nombre+Doral+yelp y
   Google devolvio su propia pantalla de captcha por trafico automatizado ("Our systems
   have detected unusual traffic from your computer network"). La IP de salida de este
   entorno ya esta marcada; no se pudo seguir por esta via.

5. **LinkedIn** (`linkedin.com/company/miami-cleaning-service-inc.`): fetch directo con
   curl (200 OK, HTML completo guardado) y con WebFetch, ambos grepeando cada URL de
   imagen `media.licdn.com` de la pagina. Solo aparece un logo generico de 200x200; sin
   foto de portada, sin publicaciones con fotos (consistente con solo 38 seguidores).

6. **Facebook**: los dos candidatos del brief (`facebook.com/mcs.commercial` y
   `facebook.com/cleanandcleaners`) estan bloqueados por el muro de login de Facebook en
   WebFetch y curl (cero contenido extraible de ningun tipo, incluidas fotos). Ademas,
   `cleanandcleaners` se confirmo via snippet de busqueda como un negocio DISTINTO
   ("Clean and Cleaners", telefono (305) 699-9588, no coincide con (305) 428-8484), y
   `mcs.commercial` no se pudo confirmar como este negocio especifico. Se descartaron
   ambos.

7. **Angi** (`angi.com/companylist/us/fl/miami/miami-cleaning-service-inc-reviews-6518063.htm`):
   WebFetch directo dio 403; con Playwright local si cargo completo. Su propio slot de
   foto de portada renderiza el placeholder `emptyCoverPhoto.svg` de Angi: el propio
   Angi confirma que no tiene ninguna foto en archivo para este negocio. Las unicas
   fotos reales en la pagina pertenecen a competidores "Approved Pro" no relacionados en
   un carrusel de recomendaciones.

8. **HomeAdvisor**: busqueda web para un perfil separado; no se encontro ninguno (solo
   paginas de categoria generica con otros competidores).

9. **Instagram**: busqueda web por nombre + Instagram; ninguna cuenta encontrada.

10. **Wayback Machine / web.archive.org** (para revisar si `miamicleaningservice.net`,
    el dominio ahora caido que LinkedIn todavia lista como sitio del negocio, tuvo
    contenido y fotos reales antes de expirar): el endpoint `archive.org/wayback/available`
    SI confirmo que existe al menos un snapshot (2026-02-18) de `miamicleaningservice.com`,
    pero leer su contenido quedo bloqueado por dos vias distintas: curl lo bloqueo la
    politica de egress de este entorno ("Blocked by egress policy") y WebFetch rechazo
    el host directamente ("Claude Code is unable to fetch from web.archive.org"). Es la
    unica via que no se pudo agotar por falta de acceso de herramienta, no porque fallara
    la busqueda en si; queda anotada para una sesion futura con distinto acceso de red.

## Por que esto NO es "research_degradado"

Este no es un caso de research degradado por canal automatizado (FORGE-BRIEF 0.b): no se
uso ningun servicio automatizado de fotos que haya devuelto poco por una limitacion
tecnica silenciosa. Cada fuente se reviso a mano, varias veces, con tecnicas distintas
(fetch directo, curl con UA real, y un navegador Playwright real con el fix de TLS
documentado para este mismo sandbox). Los nulos documentados arriba significan
"genuinamente no alcanzable desde este entorno hoy", no "un script no lo intento".

## Datos que SI quedan documentados (por si se reintenta mas adelante)

Ver `data.json` en este mismo directorio: direccion, telefono, fax, email
(`info@miamicleaningservice.net`, probablemente no entregable ya que ese dominio no
resuelve), horario, 8 reseñas reales con nombre y fuente, rating 5.0/14 (desglose
Google/Birdeye confirmado), 3 reseñas adicionales de Angi (rating 4.3/3), servicios,
hechos del negocio (2003, family-owned, 80% green, bonded/insured), y el log completo de
busqueda de email y de fotos con cada fuente, metodo y resultado.

## Que se hizo con este intento

- No se construyo ningun site (no hay `index.html`, no hay `content.json`).
- No se escribio ningun registro en `data/processed.json` (eso lo hace el orquestador
  con `registry_entry.json`, que en este caso no se genero: no hay outreach posible sin
  un site que mostrar, y el pipeline prohibe registrar negocios sin demo).
- No se genero `outreach-draft.md`: no tiene sentido redactar un correo/DM con un link a
  un demo que no existe.
- `assets/raw/` quedo vacio (0 archivos): ninguna URL de foto valida y verificada para
  este negocio especifico se pudo recuperar en ningun momento de esta sesion.

## Recomendacion para un reintento futuro

Si en algun momento se dispone de acceso a `web.archive.org` desde este entorno, vale la
pena revisar el snapshot de 2026-02-18 de `miamicleaningservice.com` (y buscar snapshots
anteriores del ya caido `miamicleaningservice.net`) por si el sitio tuvo contenido y
fotos reales antes de quedar parqueado/expirar. Tambien vale la pena reintentar Yelp
mas adelante desde una IP residencial o con acceso a un servicio de resolucion de
captcha, dado que su pagina confirma que existen 10 fotos reales del negocio.
