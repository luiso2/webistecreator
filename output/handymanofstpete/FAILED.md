# FAILED: Handyman of St.Pete (handymanofstpete)

**Motivo exacto**: solo 1 foto real y utilizable encontrada tras busqueda exhaustiva. El
minimo duro del pipeline (PIPELINE.md fase 3) es 5 fotos reales propias; con menos, el build
se marca `failed` en vez de rellenar con imagenes que no son del negocio.

## Que se encontro
- **Google Maps (ficha)**: `place_id ChIJKUQo9kQW24gRP5A7V0Sht_A`. La ficha dada en el input
  trae exactamente 1 URL de foto real (`lh3.googleusercontent.com/gps-cs-s/...`), descargada
  y verificada (`assets/raw/gmaps-1.jpg`, PNG real 1242x699, 1.0MB, exterior de bar/pergola
  terminado, foto de proyecto autentica). El fetch estatico de la pagina de la ficha no
  expuso ninguna otra foto (solo el avatar placeholder `default-user`), consistente con que
  la ficha de Google solo tiene esa 1 foto subida.
- **Sitio propio**: descartado. `handymanofstpete.com` y `stpetehandymanservices.com` no
  resuelven. `handymanstpete.com` es una pagina de parking de dominio (GoDaddy/WSIMG lander).
  `stpetehandyman.com` es un sitio real pero de OTRO negocio (telefono (727) 273-6440, no
  coincide con +1 239-293-2806).
- **Thumbtack**: sin perfil bajo el nombre exacto "Handyman of St.Pete". El unico resultado
  cercano ("St Pete Handyman", veterano de la Marina) es un negocio distinto sin telefono
  publico verificable.
- **Instagram**: existe `@handymanstpete` (Jacob Leverett, "THE HANDYMAN of St. Pete", LLC
  registrada en Sunbiz como "Handyman St Pete LLC" en Gulfport FL) pero NO se pudo confirmar
  como el mismo negocio (el endpoint `web_profile_info` de IG devolvio 401/rate-limit en los
  2 intentos permitidos). No se uso, tal como indica la instruccion de la tarea.
- **Facebook**: pagina "St. Pete Handyman" (100087945195537) existe pero esta bloqueada
  detras de login; no se pudo verificar telefono ni extraer fotos.
- **Directorios** (Yelp, Angi, BBB, Nextdoor, Sunbiz/bizprofile.net, MeetAHandyman.com):
  ningun listado bajo el nombre exacto "Handyman of St.Pete"; solo negocios homónimos
  distintos (Handyman Services Of St. Pete LLC / Curtis Bozeman, St. Pete Handy, St. Pete
  Handyman / Chris Gann, Jake From St. Pete LLC, TruBlue Handyman Services of St Pete, Ace
  Handyman Services St Pete).
- **Email**: no encontrado en ninguna fuente (sin sitio propio, sin red social confirmada,
  sin ficha en directorios con contacto).

## Conclusion
El negocio parece existir solo como ficha de Google Business Profile (rating 4.6, 60
reseñas, telefono +1 239-293-2806), sin presencia web, social o de directorio confirmable
que aporte mas material fotografico real. No se puede construir el site sin caer por debajo
del minimo de 5 fotos reales o sin inventar datos. Ver `data.json` para el detalle completo
de la investigacion.

**STATUS: failed**
