# FAILED: steelroofingsystems

**Business**: Steel Roofing Systems, LLC (managing member: Steve Smith)
**Niche**: metal roofing contractor
**Address**: 3049 Drane Field Rd, Ste 6, Lakeland, FL 33811
**Fecha**: 2026-08-19
**Status**: failed

## Motivo

Menos de 5 fotos reales y propias del negocio tras busqueda exhaustiva en todas las fuentes
disponibles (Google Maps en vivo con recorrido completo del carrusel, dominio propio, Facebook,
Instagram, y una decena de directorios). Cumple con solidez los demas criterios (sin website
propio confirmado tres veces, rating alto, contacto verificado), pero el minimo duro de fotos no
se alcanza.

## Verificacion de "sin website propio" (re-verificada de forma independiente, 3 fuentes)

1. **Google Maps en vivo** (`scripts/gmaps_detail.js` sobre la URL de ficha dada): campo
   `website: null`, y el HTML crudo de la ficha muestra literalmente el boton **"Add website"**
   (no "Visit website"), confirmando que Google no tiene ningun dominio asociado al negocio.
2. **Dominio obvio `steelroofingsystems.com`**: responde HTTP 200, pero el body es un redirect
   JS a `/lander` que carga `img1.wsimg.com/parking-lander` con `window._trfd.push({ap:"parking"})`:
   es una **pagina de parking/venta de dominio** (GoDaddy/wsimg), no un sitio operado por el
   negocio. Variantes (`steelroofingsystemsfl.com`, `.net`, `steelroofingsystemsllc.com`,
   `steelroofinglakeland.com`, `steel-roofing-systems.com`, `steelroofingfl.com`) no resuelven.
3. **Yellow Pages** lista `http://steelroofingsystems.localsearch.com` como "Website": es una
   microsite generada por la plataforma de directorio (localsearch.com/Yellow Pages), no un
   dominio propio del negocio. No cuenta como website propio (misma categoria que Booksy/
   GlossGenius: subdominio de plataforma de terceros).

Conclusion: `has_own_site: false` confirmado de forma independiente 3 veces, sin contradiccion.

## Busqueda de fotos reales (el bloqueante)

1. **Google Maps, recorrido completo del carrusel** (`scripts/gmaps_photocycle.js`, 25 pasos de
   flecha + verificacion visual por screenshot del panel lateral de fotos): el negocio tiene
   **solo 3 fotos en total** en su ficha de Google. Descargadas y verificadas con `file` (las 3
   decodifican como JPEG validos, ninguna vacia ni rota):
   - Foto 1: exterior del galpon/oficina con el letrero "Steel Roofing Systems, LLC", una
     camioneta y un empleado de camisa azul cargando material en un trailer junto a la puerta.
     **Usable** (una sola).
   - Foto 2: primer plano de un techo metalico instalado sobre un cobertizo pequeno, junto a una
     casa con techo de shingle viejo al fondo. Atribuida a un usuario de Google ("Michael H.",
     marzo 2024) en el panel de fotos, no a la cuenta del negocio: no se puede verificar con
     certeza que sea trabajo ejecutado por Steel Roofing Systems (podria ser una foto de un
     cliente satisfecho o una contribucion no relacionada). **Usable con reserva** (una sola).
   - Foto 3: una tarjeta de presentacion de "Steel Roofing Systems, LLC" y un informe de
     ingenieria (Force Engineering & Testing, Florida Product Approval) sobre unos papeles.
     Util para confirmar datos (dueno Steve Smith, fax (863) 701-7401, eslogan "Good Pricing -
     Lots of Colors to Choose From") pero **PROHIBIDA en galeria** por regla de curaduria visual
     (documento/tarjeta fotografiada, no una foto de trabajo real).
   Total de fotos de trabajo utilizables en galeria: **2 de 5 minimas** (o 1 si se descarta la
   foto de procedencia dudosa).
2. **Dominio propio**: descartado como fuente (pagina de parking, sin contenido).
3. **Facebook**: busqueda directa por nombre exacto y variantes de URL
   (`facebook.com/SteelRoofingSystems`, `facebook.com/steelroofingsystemsllc`) y
   `site:facebook.com "Steel Roofing Systems" Lakeland`: **ninguna pagina de Facebook propia
   identificada** para este negocio.
4. **Instagram**: busqueda por nombre y handles obvios (`@steelroofingsystems`): **ninguna
   cuenta identificada**. Se intento tambien `scripts/ig_scrape_fixed.js` como control de
   entorno (no como fuente, al no haber handle): fallo con
   `net::ERR_HTTP_RESPONSE_CODE_FAILURE` incluso contra un handle valido conocido
   (`instagram`), confirmando que es un bloqueo de entorno/proxy y no evidencia de nada sobre
   el negocio; de cualquier forma no habia handle que intentar.
5. **Directorios revisados sin fotos de trabajo real**: Yelp (bloqueado 403 a WebFetch directo,
   sin acceso a su galeria), YellowPages, BizProfile.net, LeadSmart Inc, AsphaltRoofingNationwide,
   Roof.info, Nextdoor (solo 1 imagen tipo logo, sin fotos de trabajo), BBB (perfil no
   localizado bajo ese nombre exacto), Angi/Thumbtack (solo listados de categoria, sin perfil
   propio con galeria).
6. **DBPR / licencia**: no se localizo un numero de licencia CCC/CGC publico verificable para
   el negocio (solo referencias genericas de "Force Engineering" a Florida Product Approval de
   paneles, sin numero de licencia de contratista). No se fabrico ningun numero de licencia.

## Conclusion

Con 1-2 fotos reales verificables de trabajo (contra el minimo de 5) y research NO degradado
(todas las fuentes cargaron con normalidad, no hay senal de bloqueo parcial que sugiera datos
ocultos), el negocio no alcanza el minimo duro de imagenes. No se fabrico ningun dato, foto,
resena ni numero de licencia. Se marca `failed` en vez de rellenar la galeria con la foto de la
tarjeta de presentacion o con imagenes de otra entidad relacionada al mismo dueno
("STEVESMITH METAL ROOFING AND SHINGLES LLC", hallada en una busqueda pero de razon social
distinta y sin confirmar que sea el mismo negocio).

## Datos verificados (para referencia, por si una sesion futura con acceso a mas fuentes reabre
## este candidato bajo el mismo o nuevo slug)
- Nombre legal: Steel Roofing Systems, LLC (constituida 2005-07-25, activa)
- Managing member: Steve Smith
- Direccion: 3049 Drane Field Rd, Ste 6, Lakeland, FL 33811 (direccion postal: 4643 South Pipkin Rd, Lakeland, FL 33811)
- Telefono: +1 863-701-7170 · Fax: (863) 701-7401
- Categoria Google: Roofing contractor
- Rating Google: 4.9 (42 reseñas confirmadas en la ficha del encargo; una busqueda web independiente mostro 38, variacion normal por fecha de consulta)
- Horario conocido: martes 7:30 AM a 4:30 PM
- Website propio: NO (dominio parkeado, sin FB/IG identificados)
- Email publico: no localizado en ninguna fuente revisada
- Eslogan visible en tarjeta: "Good Pricing - Lots of Colors to Choose From"
