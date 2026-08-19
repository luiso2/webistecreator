# FAILED: anibalandsonhandyman

**Negocio**: Anibal & Son, handyman (Kendall/Sunset, Miami, FL 33173; el input de la tarea traia
"Homestead, FL" como ciudad de registro, pero la ficha de Google Maps con el Place ID/CID exacto
del input resuelve a Miami, no Homestead).
**Fecha**: 2026-08-19
**Fase donde falla**: Research (fase 1) / puerta minima de fotos, ANTES de intentar el build.

## Motivo

Menos de 5 fotos reales y propias del negocio (regla dura de PIPELINE.md: "menos de 5 fotos reales
propias" fuerza `failed`). Tras research exhaustivo en todas las fuentes accesibles desde este
entorno, el total de fotos reales, verificadas y utilizables del negocio es **0**.

## Research que SI se completo y verifico

- `NODE_PATH=/opt/node22/lib/node_modules node scripts/gmaps_detail.js "<mapsUrl>"`: nombre "Anibal
  & Son", categoria "Handyman/Handywoman/Handyperson", rating **4.7** (coincide con el input),
  direccion **11295 SW 88th St, Miami, FL 33173, United States**, telefono **+1 786-343-4622**,
  horario parcial (Wednesday 7 AM a 7 PM, unico dia visible sin sesion), `website: null`, `photos: []`,
  `reviewSamples: []`, conteo de resenas no expuesto en el DOM de la vista limitada.
- `NODE_PATH=/opt/node22/lib/node_modules node scripts/gmaps_photocycle.js "<mapsUrl>" 30`: devolvio
  3 URLs `lh3.googleusercontent.com`. Se descargaron las 3 con curl (UA Chrome) y se inspeccionaron
  visualmente una por una (herramienta Read sobre cada imagen): son un icono generico de letra "G"
  sobre fondo azul, la foto de perfil personal de un reviewer (una pintura de un Buda, sin ninguna
  relacion con el negocio) y un icono generico de letra "S" sobre fondo verde. Las 3 son
  avatares/fotos de perfil de cuentas de Google, NO fotos del trabajo del negocio. Se descartaron y
  se borraron de `assets/raw` (la carpeta queda vacia).
- Website propio: confirmado que NO existe. `website: null` en la ficha; 4 dominios candidatos
  (`anibalandson.com`, `anibalandsonhandyman.com`, `anibalson.com`, `anibalandsonllc.com`) no
  resuelven; 3 microsites gratuitos de Google (`*.business.site`) responden 404;
  `handymananibal.com` es un sitio de contenido/afiliado generico no relacionado.
- Yelp: existe un listado indexado (`yelp.com/biz/anibal-and-son-miami`) que segun el snippet SI
  tendria fotos y resenas, pero el acceso directo esta **bloqueado (HTTP 403 Forbidden vía
  WebFetch)**. No se pudo recuperar ninguna foto ni cita verbatim verificable, solo resumenes de
  servicios parafraseados por el buscador (no citables).
- Facebook: aparece un perfil personal "Anibal Son" (`facebook.com/anibal.son.14`, inaccesible tras
  el muro de login de Facebook, no verificable) y una pagina distinta de nombre parecido
  "Handyman Sons", sin coincidencia de telefono confirmada. Ningun perfil se pudo verificar como
  propio de este negocio.
- Instagram: sin cuenta que coincida con el negocio (solo personas homonimas y handymen no
  relacionados de Miami).
- Email: no encontrado en ninguna fuente accesible.

## Nota importante: negocio duplicado en el repo

Este mismo negocio (mismo Place ID/CID de Google: `0x88d9c1468ce4bca7:0x534f82132390186f`, misma
direccion, mismo telefono, mismo rating) ya fue investigado en una sesion anterior bajo el slug
`output/anibal-son-homestead/` y llego a la MISMA conclusion (0 fotos reales, FAILED). Esta corrida,
bajo el slug pedido `anibalandsonhandyman` y con una mapsUrl de input con sufijo ligeramente
distinto (mismo CID, distinto `16s`/`19s`), confirma de forma independiente el mismo resultado.

## Siguiente paso recomendado

Si en una sesion futura hay acceso a Yelp sin bloqueo (para abrir su galeria de fotos, que segun el
listado indexado SI existe), o si el dueno provee 5+ fotos reales de trabajos terminados
directamente, este negocio es facilmente construible: rating solido (4.7), telefono verificado,
categoria clara y algunos servicios mencionados en el listado de Yelp (cabinet painting/staining,
handyman contractor, sheds & outdoor storage, art installation). Tambien conviene resolver antes de
reintentar: (a) la discrepancia de ciudad Homestead (input) vs Miami (direccion real verificada), y
(b) el numero de resenas real (33 segun input, no confirmable de forma independiente en esta
corrida), y (c) deduplicar contra `output/anibal-son-homestead/` si ambos slugs siguen existiendo.

No se contacto al negocio por ningun canal. No se escribio content.json ni HTML. No se corrio
derive.py ni gate.py (no aplica sin contenido que derivar).
