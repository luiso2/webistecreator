# Outreach draft: J&J Paradise Bakery (jj-paradise-bakery-cape-coral)

- **Estado**: `draft` (email candidato encontrado, verificado en una sola fuente, ver abajo)
- **Para**: jjparadisebakery@gmail.com (candidato, ver verificacion)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-jj-paradise-bakery-cape-coral-2026-08-06
- **Angulo**: sin website propio (`has_own_site: false`) -> "les construi un sitio de muestra"
- **Idioma**: espanol (panaderia cubana, letrero propio dice "Hablamos Espanol"; los quotes de
  reseñas usadas en el site estan en ingles, su idioma original, sin traducir, tal como pide DESIGN.md)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/jj-paradise-bakery-cape-coral/
- **Telefono verificado**: (239) 341-0007 (coincide en Yahoo Local, Wanderlog, joe.coffee, Leisure
  Dock, mymenuweb y en el letrero fotografiado de la puerta del negocio)
- **Facebook**: facebook.com/JJparadisebakery/ (pagina publica, no accesible por scraping en esta
  sesion por el muro de login de Facebook)
- **Direccion**: 111 Del Prado Blvd N #9, Cape Coral, FL 33909

## Verificacion de rating (sin acceso a Google Maps en vivo esta sesion)
Google Maps en vivo no fue accesible (WebFetch solo devuelve el shell de la SPA sin datos, curl
directo tambien bloqueado). El numero se reconstruyo cruzando varias fuentes que replican datos de
Google/Yelp:
- **RestaurantGuru**: 4.6 sobre 267 reseñas (via snippet de busqueda, la pagina en si respondio 503
  Cloudflare al fetch directo).
- **Wanderlog** (fetch exitoso, agregador que suele espejar Google Places): 4.5 sobre 385 reseñas.
- **joe.coffee** (fetch exitoso, mismo patron 4.5/385, posible misma fuente subyacente que Wanderlog).
- **Yelp / local.yahoo.com**: 4.5 sobre 19 reseñas (numero de Yelp especificamente, plataforma
  distinta y de menor volumen que Google).
- **Restaurantji**: 135 reseñas (fuente y metodologia sin confirmar, mencionado solo por referencia).
Con el rating consistente en 4.5 en tres fuentes independientes (Wanderlog, joe.coffee, Yelp) y el
conteo de reseñas variando 19 a 385 segun la plataforma, el site usa **"4.5 · 260+ reseñas"** como
cifra conservadora (por debajo del conteo mas bajo de un agregador multi-plataforma, RestaurantGuru
con 267), y el registro documenta el rango completo aqui en vez de citar un numero de Google no
verificado en vivo.

## Chequeo de website propio
- Se probaron `jjparadisebakery.com`, `jandjparadisebakery.com`, `jjparadisebakerycapecoral.com`,
  `jandjparadisebakerycapecoral.com`, `jandjbakery.com`, `paradisebakerycapecoral.com`: ninguno
  resuelve (timeout DNS).
- `jjbakery.com` resuelve pero es un negocio distinto (404 en su ruta raiz, app .NET generica, sin
  contenido de panaderia).
- `jjparadise.com` resuelve pero es un dominio no relacionado (respuesta vacia tras redirect a
  `www.jjparadise.com`, sin contenido de panaderia visible).
- El unico "sitio" indexado, `jj-paradise-bakery.weeblyte.com`, se verifico como agregador de
  terceros: pie "Powered by Weeblyte", JSON-LD generico `FoodEstablishment`, enlace "Suggest an Edit"
  en vez de panel de dueño. No es el sitio del negocio.
- Conclusion: `has_own_site: false`.

## Verificacion de email (candidato, una sola fuente)
- El email `jjparadisebakery@gmail.com` aparece publicado en **Leisure Dock**
  (leisuredock.com/directory-restaurants/listing/jj-paradise-bakery/), junto al mismo telefono
  (239) 341-0007 y la misma direccion exacta del negocio. Es un directorio que republica datos de
  fichas de Google Business (probablemente el campo de email de contacto de la ficha).
- A favor de que sea real: el email usa el nombre exacto del negocio (`jjparadisebakery@`), NO el
  dominio de un directorio clon (a diferencia del caso Arahi's, donde el email descartado era
  `arahisbakery.shop@gmail.com`, atado al dominio de la copia, una señal clara de que pertenecia al
  operador del clon y no al negocio).
- En contra: es la UNICA fuente que lo muestra en esta sesion; no se pudo confirmar de forma cruzada
  en una segunda fuente independiente ni en el "About" de la propia pagina de Facebook del negocio
  (bloqueada por el muro de login de Facebook, igual que en el precedente de Arahi's).
- Conclusion: `outreach: draft`. Se recomienda enviar como intento de bajo riesgo (no es un patron de
  clon) pero sin el nivel de certeza de un email confirmado en canal propio del negocio.

## Subject (referencia)
Un sitio de muestra gratis para J&J Paradise Bakery

## Cuerpo (referencia)

```
Hola,

Encontre J&J Paradise Bakery buscando panaderias cubanas en Cape Coral. Una calificacion de 4.5,
con reseñas que hablan de pastelitos que "saben caseros" y un trato amable en el mostrador, es una
carta de presentacion seria.

Note que J&J Paradise Bakery no tiene un sitio web propio (lo unico que aparece en Google son
paginas de directorio de terceros, no un sitio hecho por ustedes), asi que les construi uno de
muestra, sin costo y sin compromiso:

https://siteforge-demos.odd-forest-9504.workers.dev/jj-paradise-bakery-cape-coral/

Usa sus fotos reales, su direccion, su telefono y reseñas reales de sus clientes. No toca para nada
su operacion actual: no es su pagina oficial, no reemplaza nada, y el boton principal solo llama a
su telefono.

Si les gusta la direccion, puedo transferirles los archivos o ayudarles a apuntar su propio dominio.
Si no es para ustedes, lo entiendo, lo bajo sin ningun problema.

Cualquier ajuste (colores, fotos, texto) lo hago con gusto antes de que decidan.

Saludos,
Michael Vargas
Merktop
```

---

## Version corta para DM / WhatsApp (dm_message)

```
Hola! Soy Michael, de Merktop. Vi J&J Paradise Bakery en Cape Coral (4.5 en resenas, pastelitos y
croquetas que la gente ama) y les hice un sitio de muestra gratis con sus fotos y su direccion
reales: https://siteforge-demos.odd-forest-9504.workers.dev/jj-paradise-bakery-cape-coral/ No toca
su operacion, solo suma un boton de llamada. Si les gusta, se los transfiero sin costo. Si no, lo
bajo sin problema. Michael Vargas, Merktop.
```

(433 caracteres, en español por ser el idioma principal del negocio, sin em-dash.)
