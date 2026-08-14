# FAILED: Same Day Handyman & Painter (samedayhandymanpainterftlauderdale)

**Status**: `failed`. Motivo: menos de 5 fotos reales propias del negocio (minimo del pipeline,
PIPELINE.md fase 3.5). No se construyo el site.

## Verificacion de sitio propio (paso 1)
Sin website propio confirmado. Se probaron variantes de dominio
(samedayhandymanpainter.com/.net/.org, samedayhandymanandpainter.*,
samedayhandymanpainterftlauderdale.*, samedayhandymanpainterfl.*,
same-day-handyman-painter.*, samedayhandymanpainterllc.*): ninguna resuelve.
WebSearch tampoco encontro un sitio propio. `has_own_site: false`.

## Busqueda de fotos reales (exhaustiva, todas las fuentes fallaron)
1. **Google Maps**: unica foto provista por el research previo
   (`gps-cs-s/AHRPTWku...`). Descargada a `assets/raw/gmaps-1.jpg` (1361x773, EXIF
   "software=Picasa"). **Al revisarla visualmente es un stock de un cinturon de
   herramientas generico** (martillo, llave inglesa, alicates, lapices de carpintero),
   no una foto real de un trabajo, vehiculo o local de este negocio especifico. No
   sirve como foto curada del negocio.
2. **SalamApp** (`thesalamapp.com/all-states/33081ce5-...`, unico perfil online
   encontrado con nombre+direccion+telefono exactos): el listado muestra una galeria
   de "12 fotos", pero al descargar el HTML crudo y extraer las imagenes reales
   (`b25591_3352e742a2e5467aad7df422106fc278`, `b25591_2790fd3a23db403793dbf2c3c1c62723`,
   `b25591_bc3841f1dee44abf840a9a1b33591002`, mas el avatar `506b69_e841381f...`), se
   verifico que **son imagenes de plantilla genericas de SalamApp**: las MISMAS tres
   imagenes (identicos hashes) aparecen tambien en el perfil de "Z family auto"
   (un taller mecanico sin ninguna relacion), otro negocio cualquiera del directorio.
   Confirmado comparando `output/.../salamapp.html` vs una segunda descarga del
   perfil de Z family auto: hashes identicos. No son fotos reales de Same Day Handyman
   & Painter, son el placeholder de la plantilla Wix del directorio. Descartadas.
3. **Thumbtack**: WebSearch de "Same Day Handyman Painter Fort Lauderdale thumbtack"
   y variantes no devolvio ningun perfil de Thumbtack para este negocio (solo
   negocios distintos con nombres similares en la misma ciudad).
4. **Instagram / Facebook**: sin match solido de nombre+ciudad+telefono en ninguna
   busqueda. No se encontro cuenta.
5. **Yelp, BBB, Nextdoor, Sunbiz**: sin listado propio de este negocio (Nextdoor
   devuelve resultados de OTROS handyman de la zona; BBB no lo tiene; Sunbiz no
   tiene una LLC que calce con el nombre).

## Resultado
0 fotos reales verificadas y curadas visualmente (la unica disponible es un stock
generico de herramientas, no del negocio). Muy por debajo del minimo de 5. Consistente
con la nota del research: "con solo 2 temas de resenas este negocio tiene poca huella
online, probablemente termine en failed".

## Otros datos de contacto (por si se reintenta mas adelante)
- Telefono: +1 645-202-0766 (nota: area code 645 no es un area code estandar de
  EE.UU. asignado; posible numero VoIP/reenvio, sin poder confirmarlo mas).
- Email: no encontrado en ninguna fuente (SalamApp no publica email, sin sitio
  propio, sin IG/FB, sin perfil de booking).
- Direccion: 401 NW 33rd Terrace, Fort Lauderdale, FL 33311 (confirmada en Google
  Maps y en SalamApp, coincide).

No se construyo `content.json` ni `index.html`. No se toco `data/processed.json`.
