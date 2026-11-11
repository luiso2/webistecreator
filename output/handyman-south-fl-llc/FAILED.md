# FAILED: handyman-south-fl-llc

**Negocio**: Handyman South Fl LLC, Aventura, FL
**Telefono**: +1 954-706-2159
**Direccion (Google)**: 3155 NE 184th St Apt 8102, Aventura, FL 33160
**Rating**: 4.9 (24 resenas en Google, verificado en vivo hoy via Playwright directo a la ficha)
**Fecha**: 2026-11-11
**Fase donde falla**: Research (fase 1, minimo de imagenes), antes del build.

## Motivo

Menos de 5 fotos reales y propias del negocio (regla dura de PIPELINE.md fase 3 punto 5 /
FORGE-BRIEF seccion 0.b). Este es el TERCER intento de research independiente sobre este mismo
negocio: dos sesiones previas (`output/handyman-south-fl-aventura/`, `output/handymansouthflaventura/`)
ya habian marcado `failed` por el mismo motivo exacto. Mi research de hoy, hecho desde cero con
herramientas propias, confirma la misma conclusion.

## Verificacion de website propio (negativo)

- `curl -I` sobre `handymansouthfl.com`, `handymansouthflllc.com`, `handyman-south-fl.com`,
  `handymansouthfl.net`: DNS no resuelve en ningun caso.
- `handymansouthflorida.com` resuelve pero redirige a una landing generica sin ningun dato
  (telefono, direccion) que lo conecte con este negocio.
- `southflhandyman.com` resuelve pero es OTRO negocio confirmado (Top 2 Bottom Home Improvement
  LLC DBA South Fl Handyman, Pembroke Pines, telefono distinto).
- `has_own_site: false` confirmado.

## Busqueda de canales y fotos (todas las fuentes agotadas)

1. **Google Maps** (fuente principal, `node scripts/gmaps_detail.js` con Playwright headless
   directo a la URL exacta de la ficha): confirma rating 4.9/24, telefono, direccion, horario,
   `website: null`. La ficha declara textualmente `"Photos\n2 Photos"`. Las 2 URLs de foto que
   devuelve el listener de red decodifican al MISMO archivo (md5 identico): un bano remodelado.
   Sumando la foto adicional (piso instalado, distinta) que una sesion previa habia capturado por
   separado, el total de fotos reales y DISTINTAS confirmadas en Google Maps es **2**.
2. **Instagram**: sin handle publicado en ninguna fuente cruzada. Sesiones previas ya probaron
   5 handles candidatos razonables contra `web_profile_info` sin éxito (401/rate-limit). Sin un
   handle real que scrapear, `ig_scrape_fixed.js` no tiene nada que buscar.
3. **Facebook**: el unico link encontrado en research previo (`facebook.com/61582323060899`) solo
   devuelve el muro de login de Facebook via WebFetch, sin poder confirmar que pertenezca a este
   negocio (nombre, telefono y fotos no verificables).
4. **Thumbtack, Yelp, BBB, Nextdoor, HomeAdvisor/Angi/Porch/HomeGuide, Sunbiz**: sin perfil
   encontrable para este nombre exacto + telefono + direccion (confirmado por sesiones previas y
   por mi propia busqueda de hoy, incluyendo `WebSearch "954-706-2159" handyman` y
   `WebSearch "Handyman South Fl" LLC sunbiz Aventura`, ambas sin resultado util).
5. **Email publico**: no aparece en ninguna fuente. `null`.

## Por que no es `research_degradado`

El research de HOY se hizo con acceso directo a un navegador headless real (Playwright vía
`scripts/gmaps_detail.js`, el mismo patron que usa `gmaps_discover.js`) contra la URL EXACTA de la
ficha de Maps dada en el brief, no via un servicio de terceros que solo devuelva URLs sin contexto.
El conteo de "2 Photos" es literal, visible en el `rawSnippet` capturado de la pagina. No aplica la
excepcion de research degradado de FORGE-BRIEF 0.b.

## Conclusion

Negocio real, con buen rating (4.9/24) y datos de contacto verificados (telefono, direccion,
horario), pero sin ningun canal digital propio (sin website, sin IG confirmable, sin FB
confirmable, sin email publico) y con solo 2 fotos reales y distintas disponibles en su unica
fuente visual publica (Google Maps). Por debajo del minimo de 5 fotos reales que exige el pipeline
para construir sin fabricar contenido visual (rellenar galeria/hero/about con 2 fotos repetidas o
con grafica generica tipo stock esta prohibido). Se marca `failed`, igual que las dos sesiones
previas sobre este mismo negocio.

## Si se reintenta en el futuro

Si el negocio puede enviar 5+ fotos reales de trabajos terminados directamente (o si abren una
cuenta de Instagram/Facebook con fotos de trabajos), es facilmente construible: tiene rating solido,
telefono verificado y una historia real de servicio sin necesitar inventar nada mas que las fotos.
