# FAILED: The Bucks With Trucks (thebuckswithtruckstampa)

**Motivo**: menos de 5 fotos reales verificables (minimo del pipeline). Solo se pudo
confirmar y descargar **1** foto real del negocio en toda la busqueda.

## Verificacion sin website propio (paso 1)
- Probados: `thebuckswithtrucks.com`, `www.thebuckswithtrucks.com`, `thebuckswithtruckstampa.com`,
  `bwtmoving.com`, `bucks-with-trucks.com`, `thebuckswithtruckstampa.net`: ninguno resuelve
  (exit 000 / sin conexion).
- Ficha de Google Maps EN VIVO (via `scripts/gmaps_verify.js`, render real con Playwright):
  confirma `5.0` rating, categoria "Handyman/Handywoman/Handyperson", direccion
  `3406 Ellenwood Ln, Tampa, FL 33618`, telefono `+1 813-751-7569`, y el boton
  **"Add website"** (sin sitio propio declarado en Maps). Confirmado: no tiene website propio.

## Busqueda de fotos reales (paso 4, exhaustiva)
1. **Google Maps**: la unica foto disponible es la ya provista por el research
   (`lh3.googleusercontent.com/gps-cs-s/AHRPTWm2...`), descargada como
   `assets/raw/gmaps-1.jpg` (JPEG valido, 720x960, verificado con `file`). El render en vivo
   de la ficha muestra literalmente **"Add a photo"** junto al listado, es decir Google
   confirma que el negocio no tiene mas fotos propias ni fotos de reseñas cargadas.
2. **Thumbtack**: sin perfil localizable ("The Bucks With Trucks Tampa thumbtack" no devuelve
   ningun perfil de este negocio en Thumbtack, solo resultados genericos de la categoria
   movers/food trucks).
3. **Facebook** (`facebook.com/TheBucksWithTrucks/`): pagina real localizada, pero tanto la
   version desktop como `mbasic.facebook.com` redirigen a un muro de login sin sesion
   (`facebook.com/login/?next=...`); Playwright headless confirma 0 imagenes accesibles sin
   autenticacion. No se pudo extraer ninguna foto real de ahi.
4. **Instagram**: `@buckswithtrucks` SI existe, pero es un negocio de landscaping en Vancouver,
   Canada (sin relacion de nombre+ciudad+telefono con el negocio de Tampa). Descartado por la
   regla de match solido del paso 3 de la tarea.
5. **Otros directorios revisados sin fotos propias**: `handyman-usa.nears.me` (perfil generado
   por agregador, solo texto generico de plantilla + los mismos datos de Google, sin fotos
   propias), BBB, YellowPages, Manta, MapQuest, Bark.com, Nextdoor (sin listing propio
   localizable), LinkedIn ("Jordan Hall - Bucks Handyman Extraordinaire" es una persona
   distinta en New Port Richey, sin relacion confirmada con este negocio).

## Otros datos recolectados (para si se reintenta mas adelante)
- Email publico: **no encontrado** (ninguna fuente arriba expone un correo).
- Telefono: `+1 813-751-7569` (confirmado en vivo).
- Direccion: `3406 Ellenwood Ln, Tampa, FL 33618` (confirmada en vivo).
- Rating/reseñas: `5.0` / `14` (confirmado en vivo).
- IG/FB: Facebook page real existe pero sin acceso publico a contenido/fotos; sin IG propio
  confirmado.

## Resultado
Con 1 sola foto real verificable, el minimo de 5 fotos del pipeline no se alcanza y no hay
fuente adicional disponible sin credenciales/login. Status: **failed**. No se construyo
`content.json` ni `index.html`. `data/processed.json` no fue tocado.
