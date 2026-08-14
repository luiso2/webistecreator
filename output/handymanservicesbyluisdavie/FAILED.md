# FAILED: handymanservicesbyluisdavie

**Motivo:** fotos insuficientes. Solo 1 foto real utilizable disponible tras agotar todas las fuentes permitidas (minimo exigido por PIPELINE.md fase 1/3: 5).

## Negocio
- Nombre confirmado: Handyman Services by Luis LLC
- Ciudad: Davie, FL
- Direccion (Google Maps): 6620 SW 49th St, Davie, FL 33314
- Telefono: +1 954-673-6302
- Rating / resenas: 4.9 / 34 en Google (dato live suministrado en el brief; Birdeye, que espeja resenas de Google con cierto delay, muestra 4.8/40 a la fecha de esta corrida, consistente en identidad pero desfasado en conteo, normal en agregadores de terceros).
- Horarios Google: Fri-Sat-Mon-Tue-Wed-Thu 24h, domingo cerrado.
- Website propio: NO tiene. Se probaron 8 variantes de dominio obvias (handymanservicesbyluis.com, handymanservicesbyluisllc.com, handymanbyluis.com, luishandymanservices.com, handymanservicesluis.com, hsbyluis.com, handymanluisllc.com, servicesbyluis.com): las 8 devuelven 502/no resuelven (dominio inexistente). WebSearch de "Handyman Services by Luis Davie FL website" no devuelve ningun dominio propio, solo directorios de terceros (Birdeye, HomeGuide, HomeAdvisor, Angi, Houzz, genericos de la categoria en Davie). Confirmado `has_own_site: false`.

## Contacto (email)
Busqueda profunda agotada sin resultado, `email: null`:
- WebSearch directo (nombre + Davie + email/contacto): sin resultado.
- Birdeye (reviews.birdeye.com/handyman-services-by-luis-llc-167499643173095): perfil SIN reclamar por el negocio, sin email, sin telefono publicado, sin website, sin redes sociales listadas. HTML crudo verificado via curl: sin `__NEXT_DATA__` con datos de contacto adicionales, solo el cover generico de la categoria "home-services".
- myfloridalicense.com: sin registro para "Handyman Services by Luis" (esperado: handyman general no requiere licencia estatal en Florida para trabajos menores/no especializados).
- sunbiz.org (FL Division of Corporations): existe "HANDYMAN SERVICE BY LUIS LLC" (doc L20000056146, activa desde 2020) pero con domicilio principal en 9900 Altis Cir West, Hialeah Gardens, FL 33018, NO en Davie, y el nombre difere en singular/plural ("Service" vs "Services"). Direccion no coincide con la ficha de Google Maps de este negocio: se descarta como fuente de identidad/contacto para no mezclar entidades distintas. Sunbiz tampoco publica emails de todas formas.
- BBB: sin perfil encontrado para este negocio en Davie.
- Nextdoor: no se encontro una pagina de negocio con esta direccion exacta. Existen varias paginas "Luis Handyman Services" en Nextdoor pero todas corresponden a otras ciudades (Pembroke Pines/NYC placeholder, Hallandale Beach, Glendale Heights IL, Baltimore, San Diego), ninguna con la direccion de Davie.

## Redes sociales
- Instagram: no se encontro ningun handle publico verificable para este negocio.
- Facebook: se encontro "Luis Handyman Services and Remodeling" (facebook.com/p/Luis-Handyman-Services-and-Remodeling-61558820713085/), pero la pagina esta detras de un muro de login (curl y mbasic.facebook.com devuelven la pantalla de login, sin About ni fotos). Ademas, WebSearch cruzado ubica a ese negocio especifico en Hallandale Beach/Glendale Heights IL con telefono +1 630-674-4707, que NO coincide con el telefono de Handyman Services by Luis LLC (+1 954-673-6302). Se descarta por no-match de nombre+ciudad+telefono, tal como exige el pipeline.
- `ig: null`, `facebook: null`.

## Fotos (motivo del fail)
Fuentes agotadas en el orden que exige el pipeline:
1. **Google Maps**: se descargo la unica foto suministrada (`gps-cs-s/AHRPTWnK7uhaU3bdVw2gI4NsmLa-U4S13-9P7YqYwrzFSVBoN8zLo5Ljn0l8sI4obBabf9Qcrxwi39AKXMEEQsndZ-5yJWvrrxYqeRI9B9253Jfz9I7UmkAcY5B3ZP3rJGNEACbn2rtF0A`), verificada con `file` como JPEG real 1024x1024 valido (guardada en `assets/raw/gmaps-1.jpg`). Este entorno de ejecucion NO tiene acceso a un navegador headless (sin Playwright instalado, sin credencial de Google Maps API) para abrir el visor de fotos de la ficha y extraer el resto de la galeria: la SPA de Google Maps no sirve datos de fotos en el HTML estatico (verificado con curl, tanto la URL de `/maps/place/` como el endpoint `/maps/preview/place` devuelven solo el shell de la app o un mapa estatico generico, sin referencias `lh3.googleusercontent.com` ni `gps-cs-s` adicionales). Google Search estatico (curl) tampoco sirve resultados sin JS (redirige a `/httpservice/retry/enablejs`).
2. **Thumbtack**: se descargo la pagina completa de listado de handymen en Davie, FL (`thumbtack.com/fl/davie/handyman`, 492KB via curl) y se extrajeron todos los `businessName` presentes (Baypoint Property Care, Braga Remodeling, BuildTech Solutions LLC, Dmitrii, Eugene Soul Handyman, HBox, Millers Trades LLC, Rick Handyman, Ronvaz LLC, Stan Fix Pro): ningun perfil de "Luis" ni de "Handyman Services by Luis". No existe perfil de Thumbtack para este negocio especifico.
3. **Facebook**: bloqueado por muro de login (ver arriba); la unica pagina homonima encontrada no coincide en telefono/ciudad.
4. **Instagram**: sin handle verificable, no aplica `ig_photos.py`.
5. **Yelp**: bloqueado (403 Forbidden tanto via WebFetch como via curl con UA de Chrome, respuesta anti-bot de Yelp). No se encontro un listado de Yelp inequivoco para esta direccion exacta (el resultado generico "HANDYMAN SERVICES - Davie" en Yelp no se pudo abrir para confirmar identidad).
6. **BBB / HomeAdvisor / Angi / Houzz**: busquedas especificas por nombre + Davie, y por la direccion exacta "6620 SW 49th St", devuelven unicamente resultados de otros negocios homonimos "Luis Handyman..." en otras ciudades de EE.UU. (Bradenton FL, Texas, Columbus OH, Missouri City TX, Chantilly VA, St. Charles MO, Los Angeles CA, Antioch CA) o directorios genericos de Davie sin esta ficha especifica.

Con solo 1 foto real disponible (muy por debajo del minimo de 5 que exige PIPELINE.md fase 1/3), el sitio no se puede construir sin recurrir a fotos genericas/stock, lo cual esta prohibido y degradaria la calidad premium exigida. Se marca `failed` y no se continua al build, derive.py ni gate.py. No se toco `data/processed.json`. No se descargo mas de la unica imagen real (queda en `assets/raw/gmaps-1.jpg` como evidencia de research).

## Nota sobre idioma (para si se reabre el caso con mas fotos en el futuro)
Uno de los temas reales de resenas de Google es literalmente en espanol ("trabajo de calidad", 2 menciones), junto con un volumen fuerte de temas de calentadores tankless, trabajo electrico menor, limpieza y rapidez. Esto es indicio solido de clientela hispanohablante en Davie/Broward: si en el futuro aparecen mas fotos verificables (p.ej. si el negocio sube mas material a Google Maps, o reclama su perfil de Birdeye, o abre Instagram/Facebook propios), el idioma por defecto recomendado para el rebuild es `es`.

## No se investigo mas alla por
Se detuvo la investigacion en el punto en que las fuentes permitidas (Google Maps, Thumbtack, Facebook, Instagram, Yelp, BBB, HomeAdvisor/Angi/Houzz, sunbiz, myfloridalicense, Nextdoor) quedaron agotadas sin alcanzar el minimo de fotos, conforme a la regla dura del pipeline. No se contacto al negocio en ningun momento.
