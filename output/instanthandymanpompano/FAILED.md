# FAILED: Instant Handyman (Pompano Beach / Wilton Manors, FL)

**Slug:** instanthandymanpompano
**Fecha:** 2026-08-14
**Fase en la que falla:** Research (Fase 1), antes de llegar a Build.

## Motivo

No se encontraron las 5 fotos reales, verificadas y propias del negocio que exige el
minimo de calidad (PIPELINE.md Fase 1 punto 4, FORGE-BRIEF seccion 0.b "Cuando SI marcar
failed"). Tras agotar los canales razonables disponibles en este entorno, el conteo final
de fotos reales, propias y utilizables es **1** (`assets/raw/gmaps-1.jpg`, la unica foto
que trae la ficha de Google Maps: un ventilador de techo recien instalado).

El resto de los datos del negocio SI son solidos: telefono (267) 752-9639 corroborado en
vivo contra la ficha de Google Maps y contra el listado de Yelp (mismo telefono, mismo
nombre), rating 5.0 con 22 reseñas, horario Vie-Sab-Lun-Mar-Mie-Jue 8AM-8PM (Dom cerrado),
sin sitio web propio (confirmado tanto por dominios probados como por el propio panel de
Google Maps, que muestra "Add website" como campo faltante), y una LLC activa en Sunbiz
(Instant Handyman LLC, L22000064039, formada 2022-02-07). Ese material por si solo no
basta: la puerta de calidad exige fotos reales del trabajo, y aqui solo hay una.

## Que se intento (7 canales)

1. **Google Maps ficha** (la URL exacta del brief): descargada con curl la foto ya dada
   (exito, `gmaps-1.jpg`). Ademas se cargo la ficha completa con Playwright usando los
   flags de fix de TLS documentados en FORGE-BRIEF (deshabilitar QUIC/ECH/PostQuantumKyber,
   TLS tope 1.2, proxy del sandbox), se hizo click en la foto hero y en candidatos de "See
   more photos", se hizo scroll repetido, y se re-escaneo el DOM por cualquier `<img>` de
   `lh3.googleusercontent.com`. Resultado: la MISMA foto unica en distintos tamaños, nunca
   una foto adicional. Un screenshot de pantalla completa confirma que el propio panel de
   Google muestra "Add missing information -> Add a photo" (Google mismo confirma que solo
   tiene esa foto en archivo) y "You're seeing a limited view of Google Maps... Sign in"
   para ver mas (bloqueado por login, sin credenciales disponibles).

2. **Yelp** (`yelp.com/biz/instant-handyman-wilton-manors`, que el propio snippet de
   busqueda confirma que tiene "40 Photos" para este negocio, mismo telefono que la
   ficha de Google): bloqueado en 4 intentos distintos.
   - curl con user-agent de Chrome: HTTP 403.
   - curl con headers adicionales (Accept, Accept-Language, Referer de Google): HTTP 403.
   - curl con user-agent movil (m.yelp.com): HTTP 403.
   - Playwright local con los flags de fix de TLS: pantalla explicita de PerimeterX
     "You have been blocked", con ID de bloqueo visible en el screenshot guardado.
   Las 40 fotos que Yelp confirma que existen para este negocio nunca fueron alcanzables
   desde este entorno. Siguiendo la instruccion de la tarea ("no insistas mucho"), no se
   siguio intentando mas alla de estos 4 metodos.

3. **Thumbtack**: busqueda web especifica por "Instant Handyman" en Pompano Beach y en
   Wilton Manors, mas un WebFetch directo de la pagina de categoria de Pompano Beach. No
   se encontro ningun perfil de este negocio bajo ese nombre en ninguna de las dos
   ciudades.

4. **Instagram / Facebook**: busqueda web combinando nombre + ciudad + telefono (varias
   consultas). Ninguna cuenta encontrada con un match solido. Una pagina generica de
   Facebook "FL Handyman | Pompano Beach FL" aparecio en resultados pero es un negocio
   distinto (nombre distinto, sin match de telefono), descartada sin usar.

5. **Google Images / knowledge panel de busqueda normal** (fuera de Maps): un fetch
   directo con curl devolvio solo un stub que requiere JS; un intento con Playwright
   (navegador real) choco con el propio reCAPTCHA de trafico automatizado de Google
   ("Our systems have detected unusual traffic from your computer network"),
   screenshoteado para el registro. No se pudo seguir sin resolver un captcha.

6. **Registro de la LLC en Sunbiz** (via el espejo publico bisprofiles.com): confirma
   formacion 2022-02-07, estado activo, agente registrado Amine Zayi, direccion en
   Oakland Park. No trae fotos ni email.

7. **Wayback Machine** para la URL de Yelp: la API `archive.org/wayback/available` SI
   respondio en este entorno (a diferencia de otras sesiones donde ese host esta
   bloqueado por politica de egress), pero confirma que no existe ningun snapshot
   archivado de esa pagina de Yelp.

## Por que esto NO es "research_degradado"

No se uso ningun servicio automatizado de fotos que haya devuelto poco por una limitacion
tecnica silenciosa (no aplica research_ig.py ni ig_photos.py: no hay Instagram
confirmado de este negocio). Cada fuente se reviso a mano, con metodos distintos (curl
con varios user-agents/headers, WebFetch, y un navegador Playwright real con el fix de
TLS documentado para este mismo sandbox, incluyendo screenshots guardados como evidencia).
El propio panel de Google Maps confirma activamente que solo tiene 1 foto en archivo
("Add a photo" como campo faltante); no es un caso de "no se pudo ver", es "Google mismo
dice que no hay mas fotos ahi", combinado con que la fuente que SI tiene mas (Yelp, 40
fotos) esta bloqueada por proteccion anti-bot que no se pudo superar.

## Datos que SI quedan documentados (por si se reintenta mas adelante)

Ver `data.json` en este mismo directorio: telefono, rating, reseñas (conteo y temas
recurrentes ya dados en el brief), horario, LLC de Sunbiz, confirmacion de que no tiene
sitio web propio, log completo de busqueda de email (ninguno encontrado) y el log
completo de intentos de fotos con cada fuente, metodo y resultado.

## Que se hizo con este intento

- No se construyo ningun site (no hay `content.json`, no hay `index.html`).
- No se toco `data/processed.json`.
- No se genero `outreach-draft.md`: no tiene sentido redactar un mensaje con un link a
  un demo que no existe.
- `assets/raw/` quedo con 1 solo archivo (`gmaps-1.jpg`), la unica foto real verificada
  encontrada para este negocio.
- No se contacto al negocio por ningun canal.

## Recomendacion para un reintento futuro

Si en algun momento se dispone de una IP residencial, una sesion de Google ya
autenticada, o acceso a un servicio de resolucion de captcha, vale la pena reintentar
Yelp (confirma 40 fotos reales del negocio) y la vista completa (con login) de la ficha
de Google Maps antes de descartar definitivamente este negocio: los demas datos
(telefono, rating, reseñas, LLC activa, sin sitio propio) ya estan solidos y listos para
construir en cuanto aparezcan 4 fotos mas.
