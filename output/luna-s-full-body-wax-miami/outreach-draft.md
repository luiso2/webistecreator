# Outreach draft: Luna's Full Body Wax (Miami, FL)

## Estado
- **Resultado del pipeline: FAILED en Paso 2 (curaduria visual), antes de construir el site.** No se genero `content.json` ni demo.
- Sin website propio confirmado: su unico "sitio" es un Square Site de booking (`lunas-full-body-wax.square.site`), que por regla del pipeline NO cuenta como website propio (subdominio de plataforma de booking). Candidato valido "sin website propio" si se retoma en el futuro con mas fotos.
- Email publico: **no encontrado**. Busqueda realizada en `data.json` (phone/instagram/same_as), WebSearch `"Luna's Full Body Wax" Miami email contact`, WebFetch al Square Site de booking (pagina vacia/sin contenido indexable, sin mailto) y WebFetch a Instagram (HTTP 429, no accesible). Ningun resultado publico un email.
- Canal de contacto verificado: Instagram **@lunas_fullbodywax** (https://www.instagram.com/lunas_fullbodywax/) y telefono **(786) 792-7956** (verificado por el usuario via Google/Yelp; corroborado de forma independiente por WebSearch, que devolvio el mismo numero y la misma direccion "6840 SW 40th Street, Suite 212, Miami, FL 33155").
- Booking: Booksy (https://booksy.com/en-us/1385025_luna-s-full-body-wax_hair-removal_15889_miami).

## Motivo del fail (Paso 2, curaduria visual)
`booksy_dossier.py` + `booksy_gallery.py` solo devolvieron 5 archivos en `assets/raw/` (`bk-1.jpg` a `bk-5.jpg`). Tras abrir `_sheet.jpg` y revisar cada foto individualmente:

| Archivo | Contenido | Veredicto |
|---|---|---|
| bk-1.jpg | Interior real del local: camilla, pared verde, estanteria con productos, buena luz | Utilizable (unica foto de galeria valida) |
| bk-2.jpg | Retrato de la esteticista aplicando cera con una espatula, mirando a camara | Solo valido como avatar pequeno en "nosotros" (regla dura: dueno/artista nunca como tile de galeria); ademas resolucion muy baja (150x150) |
| bk-3.jpg | Primer plano de rostro de clienta, cejas, mirada hacia abajo | Borderline: no hay piel irritada evidente ni ojos cerrados a medio procedimiento, pero es un recorte facial muy intimo sin contexto de "resultado terminado" claro |
| bk-4.jpg | Collage/grafico de una campana "GET VACCINATED / WEAR A MASK" con personas no identificadas, sin relacion con el negocio | Descartada por completo (no es foto real del negocio) |
| bk-5.jpg | Placeholder generico ("B" sobre fondo verde azulado, tipo avatar por defecto de Booksy) | Descartada por completo (no es una foto real) |

Resultado: como maximo 2-3 fotos reales y utilizables del negocio (bk-1 en galeria, bk-2 solo como avatar, bk-3 borderline), muy por debajo del minimo de 5 fotos reales utilizables que exige el brief. Regla aplicada (PIPELINE.md fase 3 punto 5 y brief paso 2): "Si quedan MENOS DE 5 fotos reales utilizables en total: marca el negocio failed (motivo: fotos insuficientes) en vez de construir con material malo."

No se redacta borrador de email/DM con link de demo porque **no existe demo construido** para este negocio: seria enganoso ofrecer "les construimos un sitio de muestra" sin haberlo construido. Si en una corrida futura Booksy/Google Maps/Instagram exponen mas fotos reales del local o del trabajo terminado (idealmente 5+ resultados de depilacion/cejas con buena luz y clienta favorecida), el negocio puede reprocesarse desde el Paso 2.

## dm_message
`null` (no aplica: no hay demo que ofrecer).

## Notas
- NUNCA se contacto al negocio por ningun canal. Este documento es solo un registro de research para aprobacion humana.
- Rating real: 5.0 con 131 reseñas en Booksy (cumple rating>=4.5 y resenas>=10 del filtro de discovery); el negocio en si es un buen candidato, el bloqueo es puramente de material visual disponible hoy.
