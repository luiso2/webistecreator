# FAILED: anibal-son-homestead

**Negocio**: Anibal & Son, handyman (input: Homestead, FL; direccion real verificada: Miami, FL 33173)
**Fecha**: 2026-08-14
**Fase donde falla**: Research (fase 1) / puerta de calidad de imagenes, ANTES de intentar el build.

## Motivo

Menos de 5 fotos reales y propias del negocio (regla dura de PIPELINE.md fase 3 punto 5: "menos
de 5 fotos reales propias" es uno de los minimos que fuerzan `failed`). Tras una busqueda
exhaustiva en TODAS las fuentes disponibles, el conteo de fotos reales, verificadas y no-stock
especificas de este negocio es **0**.

## Paso 1: filtro de website propio (PASADO, no es el motivo del fallo)

- `gmaps_detail.js` corrido 5 veces contra la ficha exacta del input (mismo Place ID
  `0x88d9c1468ce4bca7:0x534f82132390186f`): `website: null` las 5 veces.
- Dominios candidatos probados con curl (UA Chrome): `anibalandson.com`, `www.anibalandsonllc.com`
  no resuelven (DNS/conexion rechazada por el proxy de salida, mismo patron que el precedente
  `jacksonville-handyman-llc`).
- `handymananibal.com` (encontrado en una busqueda general por "Anibal" + BBB) tampoco resuelve
  (DNS `ENOTFOUND`) y por su copy generico ("trusted since 2013... nationwide") es evidentemente
  contenido de afiliado no relacionado con este negocio.
- 4 variantes de microsite gratuito de Google (`anibalandson.business.site`,
  `anibal-and-son.business.site`, `anibalson.business.site`, `anibalsonhandyman.business.site`):
  las 4 responden HTTP 404.
- BBB (busqueda directa por nombre + Miami, FL): "No results for 'Anibal & Son' in 'Miami, FL'".
- Conclusion: `has_own_site = false`, confirmado. Esto NO es el motivo del fallo.

## Paso 2: research de fotos (motivo del fallo)

Fuentes revisadas, una por una, con resultado:

1. **Google Maps EN VIVO** (Playwright, misma ficha exacta del input): corrido con
   `gmaps_detail.js` x5, `gmaps_verify.js` x1, y un script de diagnostico propio que hace scroll
   profundo del panel lateral (10 iteraciones) y vuelca TODOS los `<img>` del DOM. Resultado
   consistente en las 7 corridas: la ficha muestra literalmente "Add a photo" (el negocio nunca
   subio ninguna foto), y el unico `<img>` de contenido (no logo/mapa) es
   `https://maps.gstatic.com/tactile/pane/result-no-thumbnail-1x.png`, el placeholder generico de
   Google para fichas sin foto de portada. Tampoco aparece un tab de resenas en el DOM (por lo
   que tampoco hay fotos subidas por clientes en resenas visibles en esta vista).
2. **Yelp** (`yelp.com/biz/anibal-and-son-miami`, listado real confirmado via WebSearch): acceso
   directo BLOQUEADO en 4 intentos distintos: `WebFetch` (403 Forbidden) en `yelp.com` y
   `m.yelp.com`; `curl` con UA de Chrome (403) y UA de iPhone Safari (403); `scripts/yelp_scrape_fixed.js`
   con Playwright + flags anti-deteccion, 2 corridas (pagina carga con title/body vacios,
   consistente con un challenge tipo PerimeterX antes del render). Wayback Machine no tiene
   snapshot guardado de esta URL. Solo se pudo recuperar texto indexado por el buscador (categorias
   de servicio y resumenes parafraseados de resenas de terceros), sin ninguna foto ni cita
   verbatim con autor verificable.
3. **Facebook**: sin pagina de negocio confirmada. Varias busquedas dirigidas (nombre + "Facebook
   handyman", `site:facebook.com` con variantes) solo devuelven perfiles personales no
   relacionados o negocios de handyman homonimos/distintos en Miami (ninguno coincide en telefono
   o direccion).
4. **Instagram**: sin cuenta confirmada. Las busquedas devuelven solo cuentas personales de otras
   personas llamadas Anibal o negocios de handyman no relacionados.
5. **BBB**: sin perfil (ver Paso 1).
6. **Nextdoor**: sin pagina de negocio confirmada para este nombre exacto.
7. **HomeAdvisor / Angi / Houzz / Thumbtack**: sin listado encontrado en ninguna de las 4
   plataformas para este negocio especifico.

## Que SI se pudo verificar (research no descartado, solo el build)

- Nombre exacto: Anibal & Son.
- Categoria: Handyman/Handywoman/Handyperson (Google Maps, en vivo).
- Rating: 4.7, confirmado en 5/5 corridas en vivo contra la ficha exacta (coincide con el input).
- Numero de resenas: el input trae 33, pero esta vista "limitada" de Google Maps (sin sesion) no
  renderiza el conteo de resenas en el DOM para esta ficha (ni en aria-label ni en texto plano),
  algo inusual; no se pudo re-verificar el numero exacto de forma independiente con las
  herramientas de este entorno.
- Telefono: `+1 786-343-4622` (ficha de Google Maps en vivo, first-party). Nota: un snippet de
  Yelp indexado por el buscador muestra un numero ligeramente distinto, `(786) 343-4706`; la
  discrepancia no se pudo resolver porque el acceso directo a Yelp esta bloqueado.
- Direccion: `11295 SW 88th St, Miami, FL 33173` (Kendall/Sunset, Miami-Dade no incorporado).
  **Discrepancia con el input**: la tarea traia "Homestead, FL" como ciudad, pero la ficha de
  Google Maps con el Place ID EXACTO dado en el input, y el listado de Yelp encontrado por nombre
  y telefono, ambos apuntan a Miami, no a Homestead. Ademas esa direccion corresponde a un
  complejo de apartamentos residencial (unidades listadas en Rent.com, ApartmentGuide, RE/MAX,
  Zillow, Corcoran, Homes.com), consistente con un handyman movil operando desde su domicilio, sin
  local comercial. Precedente identico ya documentado en este repo:
  `output/miami-handyman-homestead/FAILED.md` (mismo patron: input dice Homestead, la ficha real
  de Google Maps es Miami).
- `has_own_site`: confirmado `false`.
- Email: no publico, no encontrado en ninguna fuente accesible.

Ninguno de estos datos es el problema. El problema es exclusivamente el minimo de fotos: con 0
fotos reales disponibles, cualquier galeria/hero/about tendria que rellenarse con la imagen
placeholder de Google o con contenido no verificado, ambos prohibidos por las reglas de curacion
visual y de no invencion de datos.

## Siguiente paso recomendado

Si en una sesion futura hay acceso a Yelp sin bloqueo (para ver su galeria de fotos, que segun el
listado indexado SI existe pero no se pudo abrir), o si el dueno puede enviar 5+ fotos reales de
trabajos terminados directamente, este negocio es facilmente construible: tiene rating solido
(4.7), telefono verificado, categoria clara (handyman) y algunos servicios mencionados en el
listado de Yelp (cabinet painting/staining, handyman plumber, sheds & outdoor storage, art
installation). Tambien conviene resolver antes de reintentar: (a) la discrepancia de ciudad
Homestead vs Miami, y (b) el numero de resenas real (33 segun input, no confirmable en esta
corrida).

No se contacto al negocio por ningun canal. No se hizo build, gate, ni deploy.
