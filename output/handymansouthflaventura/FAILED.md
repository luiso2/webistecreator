# FAILED: handymansouthflaventura

**Negocio**: Handyman South Fl LLC, Aventura, FL
**Telefono**: +1 954-706-2159
**Direccion (Google)**: 3155 NE 184th St Apt 8102, Aventura, FL 33160
**Rating**: 4.9 (24 resenas en Google, verificado en vivo hoy)
**Fecha**: 2026-08-14
**Fase donde falla**: Research (fase 1, imagenes) / puerta de calidad de fotos, ANTES de intentar el build.

## Motivo

Menos de 5 fotos reales y propias del negocio (regla dura de PIPELINE.md fase 3, punto 5: "menos
de 5 fotos reales propias" es uno de los MINIMOS que fuerzan `failed`). Tras una busqueda profunda
en TODAS las fuentes disponibles, el conteo de fotos reales, verificadas y propias de este negocio
es **1**, muy por debajo del liston de 5.

## Paso 1: verificacion de website propio (negativo, confirmado)

- `curl -I --max-time 8` sobre `handymansouthfl.com`, `handymansouthflllc.com`,
  `handymansouthflorida.com`, `southflhandyman.com`, `handyman-south-fl.com` (http y https):
  todos devuelven `exit 6` / `http_code=000` (fallo de resolucion DNS, ningun dominio existe).
- WebSearch por el nombre exacto + Aventura y por el telefono exacto `954-706-2159` no devuelve
  ningun dominio propio: solo listados de OTROS negocios de handyman de South Florida con nombres
  parecidos (sflhandyman.com, handymanservicesfl.com, usafloridahandyman.com, etc.), ninguno
  coincide en telefono ni direccion.
- `has_own_site: false` confirmado.

## Paso 2: busqueda de fotos (fuentes revisadas una por una)

1. **Google Maps**: unica fuente con foto real confirmada. Se descargo la foto de portada dada
   (`gmaps-1.jpg`, verificada con `file`: JPEG real 900x1200, contenido real: bano/ducha con
   azulejo terminado, trabajo verosimil de handyman/remodelacion). El HTML estatico de la ficha
   de Maps (via WebFetch, sin navegador headless disponible en este entorno) no expone mas URLs
   `lh3.googleusercontent.com` del carrusel de fotos: solo la unica URL ya provista en el brief.
2. **Thumbtack**: WebSearch por `"handyman south fl llc" thumbtack` no devuelve ningun perfil de
   este negocio especifico (solo negocios homonimos no relacionados: HandyPro, Barrantes Handyman,
   Uncle Mikes, etc.). Sin perfil, sin fotos.
3. **Yelp**: WebSearch por el nombre + Aventura no devuelve listado de Yelp para este negocio
   (aparecen "Handyman Well Done" y "Aventura Handyman", ambos negocios distintos con telefono y
   direccion diferentes).
4. **Facebook**: un unico resultado de video con texto "Handyman work. Aventura, FL..."
   (`facebook.com/61582323060899/videos/...`) parecia prometedor, pero al hacer WebFetch a la
   pagina del perfil solo devuelve el muro de login generico de Facebook (bloqueo sin
   autenticacion), sin poder confirmar que la pagina corresponda a este negocio (nombre,
   telefono o direccion no verificables). No se uso.
5. **Instagram**: se probaron 5 handles candidatos razonables
   (`handymansouthfl`, `handymansouthfl_llc`, `handyman_south_fl`, `handymansouthflllc`,
   `southflhandymanllc`) contra el endpoint `web_profile_info` con header `x-ig-app-id`: los 5
   devolvieron `401 require_login` (rate-limit/bloqueo del entorno), sin poder confirmar ninguna
   cuenta real. Ningun IG handle publicado en ninguna fuente cruzada.
6. **BBB**: sin perfil para este negocio (solo homonimos no relacionados en otras ciudades de FL).
7. **Nextdoor**: sin pagina de negocio encontrada para este nombre + direccion.
8. **HomeAdvisor / Angi / Porch / HomeGuide**: ninguno lista este negocio especifico (aparecen
   competidores de Aventura como Alex Handyman Services, Almighty Handyman, Khaleef Handyman,
   Evtech, ninguno coincide en telefono).
9. **Sunbiz.org**: no se pudo confirmar el expediente exacto de la LLC via WebSearch (sin acceso
   directo a la base de datos de busqueda interactiva desde este entorno), por lo que tampoco se
   pudo cruzar hacia un posible perfil de Facebook del dueno.

## Que SI se pudo verificar (research no descartado, solo el build)

- Nombre, telefono, direccion, rating (4.9) y numero de resenas (24) verificados en vivo contra
  la ficha de Google Maps dada en el brief.
- Temas reales de resenas (quick job, promptness, responsive, quality work, job) tal como los dio
  el brief, consistentes con un handyman residencial de trabajos rapidos.
- `has_own_site: false` confirmado de forma independiente (paso 1 arriba).
- Email: NO publico. Busqueda profunda (WebSearch general, Facebook About, Nextdoor, BBB, Yelp,
  Thumbtack, HomeAdvisor/Angi/Porch/HomeGuide, myfloridalicense.com/Sunbiz) sin resultado. `null`.
- 1 foto real y verificada (`assets/raw/gmaps-1.jpg`, bano remodelado con azulejo, foto de portada
  de la ficha de Google Maps).

Ninguno de estos datos es el problema. El problema es exclusivamente el minimo de fotos: el liston
del pipeline es "¿puedo construirlo sin fabricar un solo dato?", y con 1 sola foto real disponible
no se puede armar hero + about + galeria sin repetir la misma imagen o rellenar con contenido
generico, ambos prohibidos por las reglas de curacion visual (PIPELINE.md fase 3, punto 2).

## Siguiente paso recomendado

Si en una sesion futura hay acceso a un navegador headless (para forzar la carga del carrusel
completo de fotos de Google Maps, que puede tener mas fotos subidas por clientes o por el propio
negocio aunque no aparezcan en el HTML estatico) o si el negocio puede enviar 5+ fotos reales de
trabajos terminados directamente, este negocio es facilmente construible: tiene rating solido
(4.9/24), telefono verificado, sin website propio, y una historia real de servicio sin necesitar
inventar nada mas que las fotos.

**No se marca este research como `research_degradado`**: se comprobo activamente CADA fuente
disponible (Google Maps, Thumbtack, Yelp, Facebook, Instagram, BBB, Nextdoor, HomeAdvisor/Angi/
Porch/HomeGuide, Sunbiz) y cada una devolvio, de forma verificable, cero fotos reales adicionales
utilizables. Es un negocio genuinamente con presencia fotografica publica minima (solo 1 foto en
su ficha de Google), no un caso de research insuficiente.
