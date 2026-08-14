# FAILED: fixitfelixnorthlauderdale (Fix it Felix LLC, North Lauderdale FL)

**Status**: `failed`
**Fecha**: 2026-08-14
**Motivo**: menos de 5 fotos reales propias utilizables (minimo del pipeline). Solo se
consiguio **1** foto real verificada (instalacion de inodoro, foto de Google Maps
proporcionada). Todas las demas fuentes de imagenes fallaron o no aportaron fotos reales
adicionales.

## Negocio verificado (research SI completado, solo fallo la parte de imagenes)
- Nombre: Fix it Felix LLC (Local Handyman Services, Repairs, Installations)
- Direccion (Sunbiz/bizprofile, coincide): 617 SW 78th Ter, North Lauderdale, FL 33068
- Registered agent / dueno: Felix M. Perez (Sunbiz doc L15000011281, activo desde 2015-01-20)
- Telefono: +1 954-348-1105 (confirmado via busqueda cruzada: coincide en snippet de LinkedIn
  "Felix Perez - Fix-it-Felix LLC")
- Rating/reviews Google: 5.0 / 22 (dato provisto, no re-verificable en vivo porque Maps es
  una SPA que esta forja no puede renderizar sin API key; el research original del usuario
  ya lo confirmo)
- has_own_site: false (ver seccion "check de dominio propio" abajo)
- Email: NO encontrado en ninguna fuente publica (ver detalle abajo). Seria null.

## Check de dominio propio (paso 1, completado)
Se probaron variantes de dominio:
- `fixitfelixservices.com` -> 200, pero es OTRO negocio homonimo: "Fix It Felix Handyman
  Services", licenciado y con sede en **Tennessee**, telefono (423) 403-6307. No relacionado.
- `fixitfelixhandyman.com` -> timeout / conexion rechazada, sin evidencia de relacion.
- `fix-it-felix.com` -> hace 301 redirect a `fixitfelixhvac.com`, que es un negocio de HVAC
  en **Denton, TX**, telefono (817) 909-1906. No menciona North Lauderdale, Florida ni
  954-348-1105. NO es el mismo negocio (verificado por telefono/ciudad).
  - Nota rara: el directorio `expertise.com` (listado de handymen en Pompano Beach) enlaza
    "Fix It Felix LLC" (5.0 estrellas, coincide el rating) a `https://www.fix-it-felix.com/`,
    pero esa URL hoy sirve el negocio de HVAC de Texas. Es casi seguro un error/dato viejo del
    directorio (o el dominio cambio de manos), no un website activo de este negocio: el
    contenido EN VIVO del dominio no tiene ningun dato de Florida. Se registra como hallazgo
    para que un humano lo revise, pero NO se cuenta como "tiene website propio".
  - `fixitfelixllc.com`, `fixitfelixflorida.com`, `fixitfelixnorthlauderdale.com`: no resuelven
    (502 / dominio no registrado).
- Existen ADEMAS multiples negocios homonimos "Fix It Felix" / "Fix-It-Felix" en otros estados
  no relacionados con este: Roanoke VA (handyman), Northlake TX (HVAC), Riverside CA (plomeria),
  Saint Louis MO (contratista general), Topeka KS (handyman), Hayward CA (handyman, Thumbtack),
  Libertyville IL (HomeAdvisor), Alice TX y Tucson AZ (auto), Miami FL (reparacion de celulares,
  fixitfelix.repair). Ninguno tiene el telefono 954-348-1105 ni la direccion de North Lauderdale.
- Conclusion: el negocio de North Lauderdale NO tiene website propio activo verificable.

## Intentos de fotos reales (paso 4, exhaustivo)
1. **Google Maps**: se descargo la unica foto provista
   (`assets/raw/gmaps-1.jpg`, instalacion de inodoro terminada) con curl + UA de Chrome.
   Verificada con `file` (JPEG real, 900x1200) y curada visualmente: es una foto de trabajo
   real y utilizable. No se encontro forma de enumerar mas fotos de la ficha de Google (Maps
   es una SPA; sin Places API key no hay endpoint estatico que liste el resto de fotos de la
   ficha; se probo el CID en decimal via `google.com/maps?cid=`, solo devuelve el shell JS sin
   contenido).
2. **Instagram** (`fix_it_felix_llc`), 2 intentos via `scripts/ig_photos.py`:
   - Intento 1: el microservicio cloud devolvio 1 "foto" -> resulto ser la imagen generica de
     marketing/login-wall de Instagram (mismo tarjetero de ejemplos con personas irrelevantes),
     no contenido real del perfil. Fallback local (Playwright) instalado y ejecutado: mismo
     resultado (1 URL, misma imagen de login-wall).
   - Intento 2: identico resultado (bk-2.jpg, misma imagen de login-wall).
   - Diagnostico: se verifico el servicio contra una cuenta publica masiva de control
     (`natgeo`) y devolvio tambien solo 1 URL de un recurso estatico de UI
     (`static.cdninstagram.com/rsrc.php/...`), NO fotos reales. Esto confirma que el
     microservicio esta degradado/caido HOY de forma general (no es un bloqueo especifico a
     esta cuenta), asi que un tercer intento no habria cambiado el resultado. Ambas imagenes
     descartadas y borradas (no son fotos reales del negocio).
3. **Facebook** (`facebook.com/FixitFelixLLC`): pared de login en la pagina completa (no
   accesible sin sesion) y en `mbasic.facebook.com` (redirect 302 a login). Se probo el
   endpoint publico no autenticado `graph.facebook.com/FixitFelixLLC/picture?type=large`, que
   SI devolvio una imagen (200x200): un logo tipo clipart/caricatura de un manitas generico
   (stock, no una foto real de trabajo ni del dueno). Se descarto para galeria (no es foto
   real de trabajo; a lo sumo serviria como icono de marca, pero no cuenta para el minimo de
   5 fotos reales).
4. **Directorios/terceros probados sin exito** (403, sin fotos, o sin resultados para ESTE
   negocio especifico): Yelp (`fix-it-felix-north-lauderdale-2`, 403 anti-bot), Manta.com (403),
   ZoomInfo (403), RocketReach (403), D&B (403), BBB (no hay perfil para North Lauderdale, solo
   para los homonimos de VA/TX/CA/MO), Thumbtack (no se encontro perfil de este negocio
   especifico, solo el homonimo de Hayward CA), HomeAdvisor/Angi (sin perfil para North
   Lauderdale), bizprofile.net y Sunbiz.org (solo datos de registro, sin fotos ni email),
   LinkedIn de Felix Perez (bloqueado, error 999 anti-bot), picuki.com / imginn.com / gramho.com
   (visores de terceros de Instagram, todos bloqueados con 403/502).
5. **Wayback Machine**: bloqueado por politica de egress del entorno (403 en toda solicitud a
   `web.archive.org`, tanto WebFetch como curl), asi que no se pudo confirmar historicamente si
   `fix-it-felix.com` alguna vez sirvio contenido de este negocio.

## Email (paso 2, exhaustivo, sin resultado)
Buscado en: Sunbiz.org (solo registered agent, sin email), bizprofile.net (sin email),
Facebook About (bloqueado por login), Instagram bio/business_email (bloqueado, servicio
degradado hoy), Manta/ZoomInfo/RocketReach/D&B (403), busquedas directas de patrones de
gmail asociados al negocio o al dueno: sin resultado. **email: null** (verdadero, no
inventado).

## Resultado
Con 1 sola foto real utilizable (minimo del pipeline: 5), el negocio NO se puede construir
sin rellenar la galeria con fotos que no son de este negocio. Se marca `failed` y no se
avanza a build (content.json / derive.py / gate.py). No se toco `data/processed.json`.

Si en una corrida futura el microservicio de Instagram vuelve a funcionar, o aparece un
perfil de Thumbtack/Angi propio con fotos, este negocio es buen candidato para reintentar:
tiene telefono publico, direccion verificada, dueno identificado y rating excelente (5.0),
solo falta el material fotografico minimo.
