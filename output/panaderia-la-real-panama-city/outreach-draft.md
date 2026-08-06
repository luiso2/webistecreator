# Outreach draft: Panaderia La Real (panaderia-la-real-panama-city)

- **Estado**: `pending_manual`. No se encontro email publico tras busqueda exhaustiva (ver abajo).
- **Para**: (sin email publico verificado, no enviar hasta confirmar uno)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-panaderia-la-real-panama-city-2026-08-06
- **Angulo**: sin website propio (`has_own_site: false`) -> "les construi un sitio de muestra"
- **Idioma**: español (nombre, marca y productos 100% en español; dueños con apellidos hispanos;
  ver nota de idioma abajo)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/panaderia-la-real-panama-city/
- **Telefono verificado**: (850) 215-0300 (coincide en Facebook, Yelp, Roadtrippers, Giftly, Apple
  Maps, Nextdoor y el registro de la LLC en Sunbiz)
- **Facebook**: facebook.com/panaderialareal/ (802 likes segun snippet de busqueda; pagina en si
  bloqueada por login-wall para lectura directa)
- **Instagram**: ninguna cuenta propia confirmada (ver chequeo abajo)
- **Direccion**: 1529 Lisenby Ave, Panama City, FL 32405

## Verificacion de rating

- El dato inicial (4.5, ~170-184 reseñas segun agregadores que dicen citar Google) se intento
  re-verificar en vivo contra Google Maps en esta sesion: TODOS los intentos (WebFetch a
  google.com/maps y google.com/search, curl directo) fueron bloqueados por el requisito de
  JavaScript/consentimiento de Google, sin datos de rating utilizables. No se pudo leer el widget
  de Maps en vivo.
- Dos agregadores que dicen citar "Google rating" son INCONSISTENTES entre si: Restaurant Guru
  reporta 4.5 con 184 reviews; Restaurantji reporta 4.6 con 79 reviews (81% 5 estrellas). Ninguno
  es fuente primaria verificable.
- Por separado, se verifico de forma independiente el rating PROPIO de Yelp (que es una fuente
  distinta a Google, con un conteo mucho menor): `local.yahoo.com` (mirror de datos Yelp) muestra
  4.0 estrellas / 14 reviews; Apple Maps muestra 4.1 / 14 reviews; `roadtrippers.com` renderiza la
  clase CSS `rt-yelp-rating-4` junto a la etiqueta "14 Yelp reviews". Los 3 coinciden en ~14
  reviews, confirmando que ese es el conteo INTERNO de Yelp, no el de Google (tal como advertia el
  brief inicial). Ese numero de Yelp NO se uso como si fuera de Google.
- Para el badge del hero se uso **4.5** (la cifra de Google mas repetida entre los agregadores) con
  un conteo conservador de **"70+"** reseñas (por debajo del minimo citado, 79, para no sobre-
  afirmar un numero que no se pudo confirmar en vivo). Esta limitacion queda documentada aqui y en
  `data.json` para que quede honesto en el registro.

## Chequeo de website propio

- `panaderialareal.com` no resuelve (WebFetch: `getaddrinfo ENOTFOUND panaderialareal.com`; curl vio
  el proxy: `502` con motivo `connect_rejected` / `gateway answered 502 to CONNECT`, consistente con
  dominio inexistente).
- Los unicos resultados web para el negocio son directorios/clones de terceros
  (`panaderialareal.restaurants-us.com`, `panaderia-la-real.restaurants-world.net`,
  `panaderia-la-real.wheree.com`, `panaderia-la-real.com-place.com`,
  `panaderia-la-real.weeblyte.com`), TODOS protegidos por Cloudflare (403/JS challenge) y con el
  mismo patron de contenido generico de agregador que el precedente `arahis-bakery-little-havana`:
  no son el sitio propio del negocio.
- El unico canal propio confirmado es la pagina de Facebook (facebook.com/panaderialareal/).
- Conclusion: `has_own_site: false`.

## Chequeo de Instagram (para evitar atribucion equivocada)

- Se encontraron varias cuentas de Instagram con el nombre "La Real Panaderia" / "Real Panaderia":
  `@realpanaderia.pty`, `@realpanaderia_panama`, `@larealpanaderia`, `@larealpanaderia2024`. Todas
  corresponden a panaderias llamadas "La Real" en **Panama, el pais** (sufijo `.pty`, slogan en
  jerga panameña "Pan como el de antes, pero con mas ñeque"), **no** al negocio de Panama City,
  Florida, USA. Se descartaron explicitamente: usar sus fotos o datos habria sido una atribucion
  incorrecta a un negocio distinto con el mismo nombre.
- No se encontro ninguna cuenta de Instagram propia confirmada para el negocio de Florida.

## Verificacion de email (sin resultado tras busqueda exhaustiva)

- Fuentes revisadas sin exito: Yelp (bloqueado directamente, mirrors no exponen email), Facebook
  About (login-walled, no accesible via WebFetch/curl ni via `graph.facebook.com` sin token de
  app), agregadores (restaurantguru, restaurantji, menupix, yellowpages, wheree, restaurants-us,
  restaurants-world, com-place, weeblyte: todos sin email publico o inaccesibles por Cloudflare),
  registro de la LLC en Sunbiz/OpenCorporates/bisprofiles.com (solo expone agente registrado con
  direccion postal, Florida no publica email de contacto en registros de LLC), giftly.com,
  nextdoor.com, snapchat place page.
- No existe dominio propio del que derivar un email tipo `info@dominio.com`.
- Conclusion: `outreach: pending_manual`, canal recomendado es **telefono** o **mensaje de
  Facebook**, usando el `dm_message` de abajo.

## Subject (referencia, para cuando se confirme un email)

Un sitio de muestra gratis para Panaderia La Real

## Cuerpo (referencia)

```
Hola,

Encontre Panaderia La Real buscando panaderias hispanas en Panama City. Un 4.5 de
calificacion en Google, con reseñas que hablan de empanadas caseras, pan dulce fresco y
precios accesibles, es una carta de presentacion seria.

Note que Panaderia La Real no tiene un sitio web propio (lo que se encuentra en Google son
paginas de directorio de terceros, no un sitio hecho por ustedes), asi que les construi
uno de muestra, sin costo y sin compromiso:

https://siteforge-demos.odd-forest-9504.workers.dev/panaderia-la-real-panama-city/

Usa fotos reales de su vitrina y su mostrador, su direccion, su telefono y reseñas reales
de sus clientes. No toca para nada su operacion actual: no es su pagina oficial, no
reemplaza nada.

Si les gusta la direccion, puedo transferirles los archivos o ayudarles a apuntar su
propio dominio. Si no es para ustedes, lo entiendo, lo bajo sin ningun problema.

Cualquier ajuste (colores, fotos, texto) lo hago con gusto antes de que decidan.

Saludos,
Michael Vargas
Merktop
```

## Version corta para DM / WhatsApp (dm_message)

```
Hola! Vi Panaderia La Real en Google (4.5, la gente ama las empanadas y el pan dulce) y les
construi un sitio de muestra, gratis, para que vean como se veria:
https://siteforge-demos.odd-forest-9504.workers.dev/panaderia-la-real-panama-city/ No toca su
operacion para nada. Si les gusta, se los transfiero sin costo. Si no, lo bajo sin
problema. Michael Vargas, Merktop.
```

(367 caracteres, en español segun el idioma principal del negocio, sin em-dash, dentro del
limite de 450.)
