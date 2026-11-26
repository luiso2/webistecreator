# Outreach draft: Los Picositos (Fort Lauderdale, FL)

## Datos de contacto
- Nombre: Los Picositos (food truck mexicano / taqueria)
- Direccion: 1620 W State Rd 84, Fort Lauderdale, FL 33315
- Telefono: (954) 756-0946 / +19547560946
- Instagram: @lospicositosfoodtruck (https://www.instagram.com/lospicositosfoodtruck)
- Facebook: @LosPicositosFoodTruck (https://www.facebook.com/LosPicositosFoodTruck)
- Email: no confirmado (ver seccion "Email" abajo)
- Rating: 4.5 en Google, 29 resenas
- has_own_site: false
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/los-picositos-fort-lauderdale/

## Angulo (has_own_site: false)
"Te construimos un sample site gratis": el negocio no tiene website propio (solo ficha de Google y rotulacion con IG/FB en el propio truck), asi que el angulo es mostrarles una muestra ya lista con sus fotos y datos reales, sin pedirles nada por adelantado.

## Fuentes revisadas para email (Fase 1, punto 7)
- Ficha de Google Maps (search blob y endpoint de detalle /maps/preview/place): campo website = null, sin email publico.
- Rotulacion del propio food truck (foto en alta resolucion, assets/raw/card-photo.jpg origen): se alcanza a leer parcialmente "Lospicositosfood...@gmail.c..." pero un poste/tubo metalico de la estructura del truck tapa 3 a 5 caracteres entre "food" y "@gmail". Dado que el handle identico "LosPicositosFoodTruck" se usa en IG y FB, el email mas probable es lospicositosfoodtruck@gmail.com, pero esto es una INFERENCIA, no una lectura confirmada al 100%.
- WebSearch de "LosPicositosFoodTruck" + instagram/facebook/email: sin resultados utiles.
- WebFetch del perfil de Instagram: bloqueado por rate limit (429) en el momento de la consulta.
- DoorDash (doordash.com/store/34798939, listado que referencia este food truck en Fort Lauderdale): bloqueado (403) para extraer datos.
- Atly.com/location/LosPicositos: sin email ni telefono publicados, solo resenas resumidas sin nombres.
- No hay dominio propio que probar (ni lospicositos.com ni variantes, ya que no hay indicios de dominio en ninguna fuente).

Conclusion: email = null, canal de contacto = telefono / WhatsApp / Instagram / Facebook. Registrar como `pending_manual`.

## dm_message (version corta, WhatsApp/DM, espanol, sin em-dash, maximo 450 caracteres)

```
Hola! Soy Michael, de Merktop. Vi Los Picositos en Fort Lauderdale (4.5 en Google, 29 resenas) y como no tienen website propio les arme un demo gratis con sus fotos y resenas reales: https://siteforge-demos.odd-forest-9504.workers.dev/los-picositos-fort-lauderdale/ No toca su operacion del truck para nada. Si les gusta, se los dejamos en su propio dominio, o lo borramos sin compromiso. Saludos, Michael Vargas, Merktop.
```

(Conteo de caracteres: 393, dentro del limite de 450.)

## Borrador completo (email o mensaje largo, mismo contenido para WhatsApp/DM si se prefiere version extendida)

```
Hola equipo de Los Picositos,

Soy Michael Vargas, de Merktop. Encontre su food truck buscando negocios de comida latina en Fort Lauderdale y vi que tienen 4.5 de calificacion en Google con 29 resenas, ademas de los $2 Taco Tuesdays que se ven buenisimos en sus fotos.

Noté que todavia no tienen un website propio (solo su ficha de Google y su Instagram/Facebook), asi que les arme un sample site de muestra, sin costo, usando sus fotos reales, sus resenas y su informacion de contacto:

https://siteforge-demos.odd-forest-9504.workers.dev/los-picositos-fort-lauderdale/

Esto no toca en nada su operacion actual del truck, sus redes ni su ficha de Google. Es solo una muestra para que vean como se veria un website propio para Los Picositos.

Si les gusta, se los dejamos funcionando en su propio dominio (nosotros nos encargamos de la parte tecnica). Si no les interesa, lo retiramos sin ningun compromiso de su parte.

Cualquier duda, me pueden escribir por aqui mismo o llamarme.

Saludos,
Michael Vargas
Merktop
```

## Notas de idioma
Idioma principal del site: espanol (nombre del negocio, rotulacion y menu 100% en espanol; bilingue ES/EN incluido en el demo). El dm_message y el borrador de email van en espanol por ser el idioma principal detectado del negocio.

## Pendiente
- Verificar el email inferido (lospicositosfoodtruck@gmail.com) antes de usarlo para cualquier envio automatizado: no esta confirmado con certeza visual.
- Canal de contacto recomendado mientras tanto: WhatsApp/llamada al (954) 756-0946, o DM a @lospicositosfoodtruck en Instagram/Facebook.
