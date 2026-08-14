# FAILED: national-general-cleaning-miami-lakes

**Business**: National General Cleaning Corp (owners Addiel Franco Cardoso / Daysi Cubas Mesa
per Sunbiz, activo desde 2016)
**Niche**: commercial / facility cleaning
**City**: Miami Lakes, FL (7345 Fairway Dr Apt 508, Miami Lakes, FL 33014)
**Fecha**: 2026-08-14
**Status**: failed (override editorial post-build, ver motivo)

## Motivo

El agente de research+build completo el sitio y **paso el gate mecanico** (`scripts/gate.py`:
GATE OK, cero em-dash, todos los marcadores v2+v3, JSON-LD valido, los 6 assets decodifican con
`file`). Sin embargo, en la revision editorial final (Fase 3 punto 2 de PIPELINE.md, curaduria
VISUAL obligatoria: "MIRAR cada foto antes de elegirla") se determino que el set de fotos NO
alcanza el nivel premium exigido, pese a cumplir el conteo minimo de 5:

- De las 5 fotos usadas, **3 son recortes de una sola imagen compuesta de Instagram** (un post
  "antes/durante/despues" de una bodega), cada recorte de apenas **155x237px**: al desplegarse en
  los tiles grandes del sistema de diseño (el tile ancho de galeria es `col-span-2 aspect-[16/9]`,
  tipicamente 700-900px de ancho en desktop) esa resolucion nativa se ve visiblemente pixelada/
  borrosa, justo el "demo degradado" que el pipeline prohibe explicitamente.
- Una cuarta foto (`about-2.jpg`, 150x150, portada de un Highlight de Instagram) trae un texto
  "Before" en rojo incrustado en el pixel: tecnicamente permitido solo en la seccion Experiencia
  (no en galeria) por una lectura literal de la regla, pero en la practica es un grafico de
  marketing, no una foto limpia, y refuerza la sensacion de material reciclado/de baja fidelidad.
- Solo 2 fotos son realmente distintas y de calidad aceptable: la foto de Google Maps (675x900,
  maquina fregadora de pisos, buena resolucion pero encuadre poco atractivo/cables visibles) y el
  post de Instagram del que salen los otros 3 recortes.

En la practica el negocio solo tiene **2 fotos reales de trabajo disponibles en todo internet**
(1 en Google Maps, 1 post de Instagram fragmentado en 3), no 5 fotos distintas. Estirar/recortar
esas 2 fuentes hasta llegar al numero 5 cumple la letra del minimo duro pero no su espiritu
("La CALIDAD PREMIUM de cada site es innegociable: un demo degradado quema el lead"). Se prefiere
NO publicar este demo antes que arriesgar la primera impresion del negocio con una galeria
pixelada, seguiendo el mismo principio que ya aplica el pipeline en sentido contrario ("menos
fotos buenas que rellenar con malas").

El archivo `index.html` construido (que SI paso el gate mecanico) fue eliminado de este directorio
para evitar que un push accidental lo deje accesible via el worker de demos. Se conserva
`data.json` (research completo, muy solido: telefono, direccion, dueños, Instagram, Facebook,
rating 5.0/50 confirmados) para una futura corrida, condicionado a que el negocio suba fotos
nuevas a Google Maps/Instagram o abra acceso a Facebook/Yelp.

## Datos verificados (para referencia si se reintenta)
- Telefono: +1 786-718-2426
- Direccion: 7345 Fairway Dr Apt 508, Miami Lakes, FL 33014
- Rating/reseñas: 5.0 / 50 en Google (sin quotes verbatim recuperables, Maps oculta el texto de
  reseñas sin sesion iniciada)
- has_own_site: false (nationalgeneralcleaning.com / nationalgeneralcleaningcorp.com no resuelven;
  su "website" listado en BBB, national-general-cleaning-corp.business.site, da HTTP 404)
- Instagram: https://www.instagram.com/nationalgeneralcleaning/ (12 posts visibles, solo 1 es
  contenido real de trabajo; el resto es personal/comida/familia)
- Facebook: https://www.facebook.com/p/National-General-Cleaning-Corp-100063885917602/ (muro de
  login, no se pudo leer contenido)
- Email publico: no encontrado

No se fabrico ningun dato ni foto en ningun momento del proceso.
