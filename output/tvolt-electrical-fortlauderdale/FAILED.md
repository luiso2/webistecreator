# FAILED: tvolt-electrical-fortlauderdale

**Business**: T-Volt Electrical Contracting / T-Volt, Inc. (contacto en directorios: Wesley Tole Jr.)
**Niche**: electricista / electrical contractor
**City**: Fort Lauderdale, FL (3808 Davie Blvd)
**Fecha**: 2026-08-14
**Status**: failed

## Motivo

Doble problema, ninguno de los dos resuelto tras busqueda exhaustiva:

1. **Fotos contaminadas con otro negocio**: las 8 fotos de "trabajo" encontradas en el
   directorio voolt.pro bajo el nombre T-Volt fueron inspeccionadas visualmente una por una; al
   menos una muestra a un trabajador con una camiseta que dice claramente
   "...OLE ELECTRIC...INCORPORATED", es decir, es personal de **Tole Electric Inc**, un negocio
   DISTINTO que aparece en el mismo directorio con nombre parecido ("T-Volt" / "Tole"). Esto
   invalida las 7 fotos restantes como fuente confiable (mismo directorio, mismo patron de
   mezcla): solo el logo (asset de marca, no foto de trabajo) se puede dar por autentico.
   **0 fotos de trabajo verificadas como propias de T-Volt.**
2. **Rating/resenas de Google no verificables en vivo**: el dato usado (4.5 estrellas, 23
   resenas de Google) proviene solo de un espejo de Birdeye, sin confirmacion directa en Google
   Maps. Se intento verificar con `scripts/gmaps_verify.js` (Playwright + fix TLS) con las
   variantes "T-Volt Electrical Contracting, 3808 Davie Blvd, Fort Lauderdale FL" y
   "T-Volt Inc Electrical Contracting Fort Lauderdale": ambas busquedas aterrizaron en una lista
   de negocios electricistas CERCANOS pero de nombre distinto (Master Volt Electric, Thunder
   Volt Electric Company, All Volts Electric Inc., Tole Electric Inc., Voltology Electric), sin
   que ninguno coincidiera exactamente con "T-Volt". No se pudo confirmar que T-Volt tenga una
   ficha de Google Maps propia y distinguible de estos negocios de nombre similar. Dado el
   precedente de esta misma corrida (un negocio que Birdeye reportaba 4.9/29 resenas resulto
   tener en vivo 3.7 y estar permanentemente cerrado), un dato de rating no verificado en vivo
   no es lo bastante solido para construir sobre el.

**Sin website propio**: esto SI se confirmo solido (tvoltelectricfortlauderdale.com y variantes
obvias no resuelven en DNS).

No se fabrico ningun dato ni foto. Se descarta el candidato completo por la combinacion de
ambos problemas; no se reintenta bajo el mismo nombre sin una fuente de fotos y de rating en
vivo verificadas de forma independiente.

## Datos verificados (para referencia)
- Telefono: (954) 792-4535
- Direccion: 3808 Davie Blvd, Fort Lauderdale, FL 33312
- Facebook: facebook.com/tvoltelectric/ (existencia confirmada, contenido bloqueado por
  login-wall incluso via Playwright con el fix de TLS)
- Email publico: no encontrado
