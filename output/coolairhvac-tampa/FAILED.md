# FAILED: coolairhvac-tampa

**Business**: Cool Air HVAC Services LLC (owner: Michael Armando Talocco)
**Niche**: aire acondicionado / HVAC residencial
**City**: Tampa, FL (New Tampa / Tampa Palms area, zip 33647)
**Fecha**: 2026-08-14
**Status**: failed

## Motivo

Menos de 5 fotos reales y propias del negocio tras busqueda exhaustiva, incluyendo verificacion
en vivo de su ficha de Google Maps (no solo espejos de terceros). Cumple con solidez los demas
criterios: sin website propio, rating alto, contacto verificado en multiples fuentes
independientes.

## Verificacion (research NO degradado)

1. **Google Maps EN VIVO** (`scripts/gmaps_verify.js`, renderizado real con Playwright y el fix
   de TLS del proxy documentado en FORGE-BRIEF): ficha confirmada, **rating 5.0**, negocio
   abierto ("Open - Closes 11:30 PM"), categoria "HVAC contractor", telefono
   +1 813-373-3200 coincide. El panel de fotos muestra unicamente el boton **"Add a photo"**
   (sin conteo numerico de fotos ni seccion de fotos de resenas): senal directa de Google de que
   el negocio no tiene NINGUNA foto propia ni de clientes en su ficha.
2. **Sin website propio**: confirmado. coolairhvac.com pertenece a una empresa de Winnipeg,
   Canada, sin relacion; coolairhvacservices.com, coolairhvacservicesllc.com y
   coolairhvactampa.com no resuelven. La ficha de Google Maps no lista campo de website.
3. **Instagram** (@coolairhvacservices, 937 seguidores, 343 publicaciones, cuenta activa):
   probable mejor fuente de fotos reales de trabajo, pero **bloqueado**: `curl` recibe 302 a
   login inmediato; `scripts/ig_scrape_fixed.js` (Playwright + fix TLS) devuelve
   `net::ERR_HTTP_RESPONSE_CODE_FAILURE` de forma consistente en 2 intentos espaciados (no es un
   timeout, Instagram esta devolviendo un codigo de error a la IP de este entorno).
4. **Facebook**: no se encontro pagina propia identificable para este negocio.
5. **Nextdoor**: HTML descargado sin bloqueo. Se extrajeron y verificaron con `file` todas las
   imagenes referenciadas: **solo 1 foto real utilizable** (dos furgonetas blancas rotuladas
   "Cool Air HVAC Services LLC" con el telefono visible, estacionadas en una entrada
   residencial). El resto de imagenes de esa pagina son un cover de stock generico (rejilla de
   A/C con luz azul), el logotipo, y un flyer promocional con texto superpuesto sobre la misma
   foto de las furgonetas (descartado por regla de curaduria visual).
6. **BBB (A+ acreditado desde 2025) y BuildZoom**: sin galeria de fotos.

**Total de fotos reales utilizables confirmadas: 1 de 5 minimas.** No se fabrico ninguna imagen
ni dato. Reseñas verbatim (Nextdoor, no confirmadas como espejo exacto de Google) y datos de
contacto quedan documentados en caso de que una sesion futura con acceso a Instagram (login o
IP residencial) pueda completar el research de fotos y reabrir este candidato bajo un slug
nuevo si corresponde.

## Datos verificados (para referencia, no descartar como candidato en el futuro sin releer esto)
- Telefono: (813) 373-3200
- Licencia FL DBPR: CAC1816237, activa desde 2009
- Rating Google (en vivo): 5.0
- Email publico: no encontrado
