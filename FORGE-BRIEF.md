# FORGE-BRIEF: guia unica de la forja (rutinas siteforge-queue)

> Condensado operativo de PIPELINE.md + DESIGN.md para que una corrida de forja lea UN solo archivo.
> Si un caso no esta cubierto aqui, PIPELINE.md y DESIGN.md son la fuente de verdad.

## RUTA RAPIDA: solo con el Instagram (2026-07-29, la via por defecto)
Cuando el encargo es un handle de IG, estos 3 comandos hacen todo lo mecanico. Lo unico que
pone el agente es el JUICIO: mirar el contact sheet y escribir el contenido.

```
.venv-pw/bin/python scripts/research_ig.py <handle> [slug]   # ~7s: fotos+logo+bio+telefono+email+has_own_site+sheet
#  -> MIRAR output/<slug>/_sheet.jpg y escribir output/<slug>/content.json (solo textos)
python3 scripts/derive.py <slug>                             # ~0.03s: genera el index.html
python3 scripts/publish.py <slug> --lang es --forbid "..."   # gate + CSS + deploy + verifica 200 + registra
```

- `research_ig.py` abre Instagram UNA sola vez (antes eran 4 pasadas, ~22s y 4x el riesgo de
  rate limit) y descarga las fotos en paralelo. Escribe `output/<slug>/data.json`.
- `content.json` es SOLO contenido: la mecanica de anclas vive en `derive.py`. Los antiguos
  `build_<slug>.py` (18 KB de media, 75% andamiaje repetido) ya no hacen falta.
  Ejemplo completo y comentado: `output/prestigeautocargo/content.json`.
- Si el negocio no tiene resenas verificables: `"social_proof": {"modo": "razones", ...}`.
  Si no tiene direccion publica: omitir `contacto.mapa` y poner `contacto.imagen` (NUNCA un
  mapa inventado). Si no tiene precios publicos: omitir `precio` en las cards.
- `publish.py` NO registra el negocio si el demo no responde 200 (evita tarjetas fantasma) y
  nunca pisa un registro con outreach `sent` o `skip_duplicate`. No envia ningun mensaje.
- Antes de aprobar un lote de outreach: `python3 scripts/dedup_check.py` (mismo negocio bajo
  dos slugs = dos cold emails al mismo dueno, rompe la regla dura #3).

Los scripts de abajo (booksy_dossier, glossgenius_dossier, fresha_dossier) siguen siendo la
mejor fuente cuando el negocio SI tiene pagina de booking: dan menu, precios y resenas reales,
que el IG no da. La ruta rapida es para el caso "solo tengo el Instagram".

## 0.a A QUIEN buscar: priorizar por NECESIDAD de website (2026-08-12)

El liston para elegir un negocio no es "que facil es sacarle el research", es **cuanto le
cambia la vida tener un website**. Entre una manicurista y un carpintero, el carpintero lo
necesita mucho mas, y hasta ahora se estaba construyendo justo al reves.

**Por que** (dos razones, las dos comprobables):
1. **Los de belleza YA tienen un sustituto de website**: su perfil de Booksy, Vagaro o
   GlossGenius es una pagina publica con fotos, servicios, precios, resenas y reserva online.
   Un demo les aporta poco por encima de eso. Un carpintero, un plomero o un handyman no
   tienen nada equivalente: su unica presencia suele ser un Facebook viejo o nada.
2. **El cliente los busca en sitios distintos**: los servicios del hogar se buscan en Google
   con intencion de contratar ya (de cada 4 personas que buscan un contratista desde el movil,
   3 contactan un negocio ese mismo dia), mientras que belleza se descubre dentro de las
   plataformas de booking. Sin website, el contratista no existe en la busqueda que importa.

**Dato del propio registro (2026-08-12, 642 negocios)**: los oficios del hogar publican
telefono el 82% de las veces (14 de 17) y las unas solo el 29% (49 de 168). O sea que ademas
de necesitarlo mas, son mas faciles de contactar por SMS y WhatsApp, que es el canal que de
verdad tenemos (solo 128 de 642 tienen email).

**Estado a corregir**: el registro esta 77% en belleza (unas 26%, spa 22%, pelo 21%, lash 8%)
y solo 3% en oficios del hogar. `config.json` ya invierte la prioridad.

| Prioridad | Nichos | Por que |
|-----------|--------|---------|
| ALTA | handyman, carpinteria, plomeria, electricista, HVAC, roofing, pintura, pressure washing, pisos, cerrajeria, pest control, landscaping, cleaning, mudanzas | Sin plataforma sustituta, se buscan en Google, ticket alto, el cliente necesita ver trabajos y credenciales antes de dejarlos entrar en su casa |
| MEDIA | detailing y taller mecanico, pet grooming, food truck, reposteria, catering, fotografia, tattoo | Presencia en redes pero sin pagina propia; ticket medio y la decision se piensa |
| BAJA (saturado) | nail salon, lash & brow, barberia, hair salon, facial/skincare | Ya cubiertos de sobra y su Booksy/GlossGenius hace de website. Solo si el usuario lo pide por nombre |

**Research de los nichos de ALTA**: no tienen Booksy ni GlossGenius, asi que los dossiers de
plataforma no sirven. Las fuentes son Google Maps (nombre, telefono, rating, resenas, fotos),
Facebook Business e Instagram. Para las fotos, `research_ig.py` sigue valiendo si tienen IG;
si no, las fotos de Google Maps del propio negocio. Si no hay 5 fotos reales de SU trabajo:
`failed`, igual que siempre (no valen fotos de stock de herramientas).

## 0.c Reclamar de UNO en uno (2026-08-14, obligatorio)

PROHIBIDO marcar varios items de la cola como `processing` al arrancar. El caso real: una
corrida reclamo 5 items a las 14:59, construyo 2 y murio al cumplir su hora; los otros 3
quedaron "en proceso" fantasma hora y media, invisibles para las forjas siguientes.

Regla: se reporta `research` de UN item SOLO al empezar a trabajar ESE item. Los demas se
quedan `pending`, visibles para cualquier otra forja concurrente. Al terminar un item (done
o failed), recien entonces se toma el siguiente. Ademas, reportar progress al cambiar de
etapa (research -> build -> verify -> commit): reclamar con `POST /api/public/queue/claim {id}`
antes de investigar; si devuelve `409`, tomar el siguiente. El panel rescata como huerfano todo
item sin senales por **12 minutos**, y un item que trabaja de verdad cambia de etapa mas seguido.

## 0. Arranque paralelo (primer minuto, OBLIGATORIO)
### Pedido filtrado desde el panel (nicho + país o zona, sin website)

Si el item de `/api/public/queue` trae `request.type: "discovery"`, NO es un negocio directo. El
objeto es la fuente de verdad, por ejemplo:

```json
{"type":"discovery","niche":"electricistas","location":"España","count":3,"require_no_website":true}
```

Buscar solo ese nicho en esa ubicación. Verificar que cada candidato no tenga website propio
antes de hacer research o build; Booksy, GlossGenius, Google Business, Facebook, Instagram y
WhatsApp no cuentan como website propio. No usar `config.json` como fallback, no salir de España
ni rellenar el cupo con un negocio que ya tiene web. Construir hasta `count` candidatos válidos,
hacer `registry-upsert` por cada uno y cerrar el id del pedido UNA vez con:

```json
{"id":"...","sites":[{"slug":"...","name":"...","url_demo":"https://siteforge-demos.odd-forest-9504.workers.dev/<slug>/","dm":"..."}]}
```

Si ninguno cumple el filtro, marcar el pedido `failed` con el motivo. El progreso puede usar
`note` para indicar, por ejemplo, `2/3 candidatos válidos`.

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
- **Servicio de fotos IG en Railway (todo-en-la-nube, 2026-07-20)**: `ig_photos.py` llama a `https://ig-photo-service-production.up.railway.app/ig?u=<user>&key=igsvc_pub_2026` (Railway corre Playwright y SI llega a IG; la forja cloud llega a Railway aunque no a IG). Es intermitente por gating de IP datacenter -> el script cae a Playwright LOCAL si el servicio trae <5 fotos (IP residencial, confiable). Para la forja cloud (sin IP residencial) el servicio con reintentos es lo que hay; espaciar (1/7min) ayuda.
- **Fotos reales de CUALQUIER negocio (la via rapida, 2026-07-20)**: `.venv-pw/bin/python scripts/ig_photos.py <ig_username> <slug>` baja en ~13s las fotos del perfil publico de IG via Playwright headless (navegador real, ejecuta JS, SIN login, SIN riesgo de ban, SIN contaminacion). Resuelve el paso de fotos de los tenants Square/GlossGenius/Acuity (sus plataformas dan menu pero no fotos). Curar el _sheet.jpg (descartar covers de reels y graficos con texto). Complementar fotos ya bajadas: pasar start_index. IG rate-limitea BURSTS por IP (rapido seguido = 0 fotos), NO los espaciados: la forja construye ~1 negocio/7min, cadencia que se queda bajo el limite. El script AUTO-INSTALA Playwright+chromium si falta, asi corre en la nube de la forja, no solo local.
- **Leccion 2026-08-02 (root cause del "Playwright no conecta" en la forja cloud)**: el sandbox de la rutina cloud usa un proxy que re-termina TLS; el binario `headless_shell` que Playwright lanza por defecto manda un ClientHello moderno (QUIC/HTTP3, Encrypted Client Hello, PostQuantumKyber) que ese proxy no completa (`net::ERR_CONNECTION_RESET`, visible con TODOS los hosts https, no solo IG). Curl SI funciona porque negocia TLS 1.2 clasico. Fix confirmado: lanzar el binario `chrome` COMPLETO (no headless_shell, ruta tipica `/opt/pw-browsers/chromium-<version>/chrome-linux64/chrome`) con flags `--disable-quic --disable-features=QUIC,EncryptedClientHello,PostQuantumKyber,UseDnsHttpsSvcbAlpn --ssl-version-max=tls1.2` (mas `--proxy-server=$HTTPS_PROXY` si aplica). Con eso Instagram carga con normalidad (perfil, fotos, bio) igual que en local. Script listo: `node scripts/ig_scrape_fixed.js <ig_username>` (usa el modulo `playwright` global de npm, no necesita `.venv-pw`) imprime JSON `{username, title, images:[{src,alt,width,height}]}`; descargar cada `src` con `curl -A "<chrome UA>" -H "Referer: https://www.instagram.com/" -o archivo.jpg "<url>"` (las URLs de scontent.cdninstagram.com son firmadas: hace falta el query string completo + Referer, si no dan 403). Antes de asumir "IG bloqueado" en una corrida cloud, probar este metodo primero.
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

## 0.b Variante adaptada: negocios fuera del formato salon/spa (2026-07-29)

El esqueleto nacio para salon/spa, pero el sistema visual sirve para cualquier negocio local.
Un negocio SIN citas reservables (exportacion de vehiculos, detailing, landscaping, cleaning,
handyman, food truck, fotografia) NO se descarta por eso: se construye adaptando las secciones
cuyo dato no existe.

**La linea que no se cruza**: OMITIR una seccion porque el negocio no publica ese dato esta
BIEN. RELLENARLA con datos plausibles esta PROHIBIDO (regla dura #1). Cada objecion clasica
tiene su adaptacion ya probada:

| No hay | NO hacer | SI hacer |
|--------|----------|----------|
| Resenas verificables | inventar quotes o rating | `social_proof.modo: "razones"`: 3 cards de especialidades reales derivadas del about |
| Precios publicados | poner precios "desde $X" | cards sin `precio` + nota "cada operacion se cotiza, escribenos" |
| Direccion publica | mapa de la ciudad como si fuera su local | omitir `contacto.mapa` y poner `contacto.imagen` (foto real) |
| Booking online | inventar un flujo de reserva | CTA al canal real (WhatsApp, DM, telefono) |
| Menu por sesion | fabricar servicios | cards = lo que el negocio SI dice que hace, con sus palabras |

**ANTES de marcar failed por falta de datos: comprobar `research_degradado` en data.json.**
Si es `true`, el research salio por un canal que NO ve la bio (el servicio de Railway solo
devuelve URLs de fotos) o trajo menos de 5 fotos. Sus null significan "no se pudo ver", NO
"el negocio no lo publica". Descartar con ese research produce falsos negativos: reintentar
desde una maquina con Playwright e IP residencial, y si no la hay, dejar el item PENDIENTE
para la siguiente sesion local en vez de marcarlo failed.
Precedente (2026-07-29): @beezualstudios se descarto por "research insuficiente" con 1 foto
(un flyer no usable) obtenida por el servicio. El mismo perfil por Playwright local daba 12
fotos, 11 de ellas material real de trabajo, 1,095 seguidores y 24 posts: era construible.

**Website propio roto**: si `website_candidates_rotos` trae algo (dominio que responde 525,
403, 500...), el negocio SI tiene dominio pero no carga. No es "no tienen website": el angulo
es "su web no esta cargando", que suele ser mejor gancho todavia.

**Cuando SI marcar `failed`** (faltan los minimos, no el formato, y con research NO degradado):
- menos de 5 fotos reales y propias del negocio (stock, graficos con texto o fotos de otras
  cuentas NO cuentan), o
- ningun canal de contacto publico, o
- no se puede describir a que se dedica sin inventarlo (bio vacia y feed ambiguo), o
- es ecommerce/mayorista puro donde el sitio tendria que ser un catalogo con carrito.

**Precedente**: `output/prestigeautocargo/` (exportacion de vehiculos, Miami). La cola lo habia
marcado `failed` el 2026-07-25 por "no encaja en el formato", con el argumento de que construirlo
obligaria a fabricar servicios, precios y resenas. La adaptacion resuelve justo eso: se
construyo sin fabricar ninguno de los tres. Su `content.json` es la referencia de esta variante.

## 1. Checks criticos de research
- **Website propio** (leccion MaRe): probar `<negocio>.com`, dominio del email, links de bio. Si existe: `has_own_site: true` y el angulo cambia a "propuesta de rediseño" (NUNCA afirmar "no tienen website"). Subdominios de plataforma (square.site, glossgenius.com) NO cuentan como website propio.
- NUNCA inventar servicios, precios, duraciones ni resenas. Si tras busqueda exhaustiva no hay UN dato verificable de precios ni resenas (solo feed de IG y citas por DM): marcar `failed` con motivo detallado (precedente @salaslash_ 2026-07-18), no fabricar.

## 2. Build (derivacion anclada desde esqueleto v2: el metodo probado en batches 1-3)
- EMPEZAR COPIANDO `templates/dark-v2/index.html` o `templates/light-v2/index.html` segun el brand real; derivarlo con UN script Python de transformacion anclada. Escribir HTML desde cero o editar a mano esta PROHIBIDO. **La receta completa (orden de operaciones, regexes de secciones, proteccion del badge, cambio de idioma, gotchas) esta en `templates/SKELETONS-V2.md`: leerla ANTES de construir.**
- Fotos: el dossier del paso 1 ya descargo la galeria validada y genero `output/<slug>/_sheet.jpg`. LEER el sheet (curacion VISUAL obligatoria) antes de elegir hero/experiencia/galeria. Si el sheet muestra stock o graficos con texto: rescatar fotos reales de IG (regla de rescate de la seccion 0) o marcar failed.
- Estructura heredada del esqueleto: nav glass, hero con rating real, strip con contadores, experiencia, metodo 4 pasos, servicios en 4 cards (card 2 destacada), galeria 1 ancho + 5 tiles con tile-cap, opiniones VERBATIM, ubicacion con mapa embed, CTA final, footer "Powered by Merktop" -> https://merktop.com.
- Lo FIJO es el sistema visual (motion, tipografia, glass, paleta, markers). Las secciones cuyo dato el negocio no publica se ADAPTAN, nunca se rellenan: ver "Variante adaptada".
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
8. Si el negocio no encaja en el formato de salon/spa, NO es motivo automatico de `failed`: aplicar la variante adaptada (seccion 0.b). `failed` se reserva para cuando faltan los datos MINIMOS (menos de 5 fotos reales propias, ningun canal de contacto publico, o no poder describir el servicio sin inventarlo).

## 4. Registro, panel y reporte
- `data/processed.json`: {slug, name, city, ig, url_demo: https://siteforge-demos.odd-forest-9504.workers.dev/<slug>/, has_own_site, email, phone, outreach: pending_manual|draft, status: staging, language, dm_message, thumb, fecha}. `thumb` = URL ABSOLUTA de la og:image del site (url_demo + ruta de la imagen del og:image del index.html): el panel la usa como miniatura de la tarjeta. NUNCA reprocesar un slug registrado.
- **dm_message** (SIEMPRE): version corta del outreach para DM/WhatsApp, max 450 chars, idioma principal, link del demo, angulo segun has_own_site.
- Ids procesados -> `data/queue_done.json` (failed: con motivo). Commit + push a main. Si el push es rechazado: `git pull --rebase`; si `data/processed.json` queda en conflicto, fusionar POR SLUG (base = `git show origin/main:data/processed.json`, agregar solo los slugs propios que falten via `git show REBASE_HEAD:data/processed.json`), NUNCA escoger un lado entero; `git add` + `git rebase --continue` + push. El push publica los demos solo (Workers Builds).
- Verificacion live tras el push: `curl` del demo con User-Agent de navegador (python-urllib recibe 403 de Cloudflare) hasta obtener 200; los assets nuevos pueden dar 404 por 1-2 min de propagacion: reintentar antes de diagnosticar. Confirmar que el HTML live = local y que el thumb decodifica.
- Panel publico: GET /api/public/queue, POST /api/public/queue/progress {id, stage: research|build|verify|commit}, POST /api/public/queue/done {id, slug, name, url_demo, dm}. Ademas, por CADA negocio construido: POST /api/public/registry-upsert con {slug, name, city, ig, url_demo, has_own_site, email, phone, language, dm_message, thumb, fecha} para que aparezca en la UI al instante. Item FALLIDO: POST done con {id, failed: true, motivo: "<resumen corto del porque>"} para que el panel lo muestre en rojo con su motivo.
- PROHIBIDO contactar negocios por cualquier canal. Reporte unico por Resend a jose@merktop.com solo si se proceso algo; con email publico incluir boton mailto "ENVIAR ESTE CORREO (1 tap)" pre-llenado.

## 5. Reglas duras
Sin em-dash en ningun output. Nunca inventar datos. Una fase falla 2 veces -> failed con motivo y seguir. Nunca procesar el mismo negocio dos veces. Maximo 3 items por pasada.
