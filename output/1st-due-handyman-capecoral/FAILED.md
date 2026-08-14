# FAILED: 1st-due-handyman-capecoral

**Motivo:** fotos insuficientes. Solo 1 foto real utilizable disponible tras agotar todas las fuentes permitidas.

## Detalle de la investigacion

### Negocio
- Nombre confirmado: 1st Due Handyman LLC
- Ciudad: Cape Coral, FL
- Categoria (Google Maps): Handyman/Handywoman/Handyperson
- Telefono: +1 239-788-4858
- Rating: 5.0 (confirmado 5 veces via gmaps_detail.js, corridas identicas)
- Resenas: numero no renderizable por la vista sin sesion de Google Maps en este entorno (el snippet crudo solo muestra "5.0" sin conteo entre parentesis en ninguna de las 5 corridas). El dato de discovery (17 resenas) no pudo re-verificarse de forma automatizada; no se muestra en ningun otro directorio publico indexado (BBB sin listado, sin perfil en Yelp/Houzz/Thumbtack/Nextdoor para este negocio especifico en Cape Coral).
- Website propio: CONFIRMADO que NO tiene (campo `website: null` en 5 corridas de gmaps_detail.js, la ficha muestra literalmente "Add website"; WebSearch no encontro dominio propio; los unicos resultados con nombres similares -capecoralhandymanllc.com, handymanservicecapecoral.com- son negocios DISTINTOS).

### Fotos (motivo del fail)
Fuentes agotadas en el orden que exige el pipeline:
1. **Google Maps**: gmaps_detail.js corrido 5 veces contra la ficha exacta (incluyendo variantes de URL: data= completa, @lat,lng, y /search/?api=1&query=). Ademas se corrio un probe adicional que clickea explicitamente el boton "Photo of 1st Due Handyman LLC" (equivalente a "See photos") y hace scroll extensivo dentro del visor de fotos. Resultado consistente: **exactamente 1 foto** en todas las corridas (`gps-cs-s/AHRPTWmi7uev4cV4SGmFkoWmSEjCiqTtm0NONNBizzl8axfUKCNlVBX4vFTw1iulj_nE-qyNS77Ygj6zTVgl5--LIB2Zg83Ysl6_Gkjo4Y0Yycuvxa5TkEHK2EsLGZfVXbZ4TeLDcCbn`). No hay galeria adicional que abrir: la ficha de Google solo tiene esa unica foto subida.
2. **Facebook**: existe una pagina publica (`facebook.com/p/1st-Due-Handyman-LLC-61552688461330/`), confirmada por WebSearch, pero el contenido (fotos, About, reviews) esta detras de un muro de login en este entorno: todas las variantes probadas (www.facebook.com directo, mbasic.facebook.com, User-Agent Googlebot, graph.facebook.com/<id>/picture publico) devolvieron 302 hacia `/login.php` o body vacio. No fue posible extraer ni una sola foto de Facebook.
3. **Instagram**: no se encontro handle publico confirmado. Se probaron variantes obvias (1stduehandyman, 1stduehandymanllc, 1st_due_handyman, firstduehandyman) via curl y via el endpoint `web_profile_info`; todas devolvieron redireccion a login o rate-limit (`require_login: true`), sin poder confirmar ni acceder a ningun perfil real.
4. **BBB**: busqueda directa en bbb.org por "1st Due Handyman" + Cape Coral, FL devolvio "No Results Found".
5. **Angi / Yelp / Houzz / Thumbtack / Nextdoor**: busquedas especificas (`site:yelp.com`, `site:houzz.com`, `site:thumbtack.com`, `site:nextdoor.com`, mas WebSearch general) no encontraron ningun perfil de este negocio especifico en Cape Coral, FL (solo negocios homonimos en otras ciudades: Naples FL, Harrisville PA, Centennial CO, Custer WI).

Con solo 1 foto real disponible (muy por debajo del minimo de 5 que exige PIPELINE.md fase 1), el sitio no se puede construir sin recurrir a fotos genericas/stock, lo cual esta prohibido y degradaria la calidad premium exigida. Se marca `failed` y no se continua al build ni al gate.

## No se investigo mas alla por
Se detuvo la investigacion en el punto en que las 5 fuentes permitidas (Maps, Facebook, Instagram, BBB, Angi/otros directorios) quedaron agotadas sin alcanzar el minimo de fotos, conforme a la regla dura del pipeline.
