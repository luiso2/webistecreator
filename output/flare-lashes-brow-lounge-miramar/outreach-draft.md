# Outreach draft: Flare Lashes & Brow Lounge (flare-lashes-brow-lounge-miramar)

- **Estado**: pending_manual (sin email publico encontrado; NO enviar nada sin aprobacion explicita del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-flare-lashes-brow-lounge-miramar-2026-08-07
- **Angulo**: sin website propio (has_own_site: false)
- **Idioma**: ingles (idioma principal del negocio: descripcion y reseñas en Fresha e Instagram en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/flare-lashes-brow-lounge-miramar/
- **Telefono verificado**: (323) 507-4978 (numero de contacto publicado por el propio negocio en su ficha de Fresha)
- **Canal disponible**: sin email publico. Registrado como `outreach: pending_manual` con telefono (323) 507-4978 y su Instagram @flarelashesandbrows (874 seguidores, cuenta activa, 313 posts) para DM o WhatsApp manual.

## Verificacion de rating y reseñas
- Fuente real: **Fresha** (ficha de reservas del negocio), NO Google. Google Maps no fue accesible en modo lectura estatica durante esta investigacion.
- Extraido directo del payload `__NEXT_DATA__` de la pagina de Fresha (SSR, sin necesidad de scraping de terceros): `rating: 5`, `reviewsTotal.value: 201`, desglose `rating5Total: 197`, `rating4Total: 4` (o sea, 201 reseñas, 197 de 5 estrellas y 4 de 4 estrellas, promedio 5.0 redondeado).
- El sitio construido dice explicitamente "5.0 en Fresha" / "5.0 on Fresha" en todo el copy, nunca "Google", para no atribuir mal la fuente.

## Chequeo de website propio
- `flarelashesandbrowlounge.com`, `flarelashesandbrows.com`, `flarelashesbrowlounge.com` y `flarelashbrowlounge.com`: las 4 variantes fallan en resolver (sin DNS, confirmado independientemente con `getent hosts` ademas del proxy de red).
- Bio y perfil de Instagram (@flarelashesandbrows): sin dominio propio, solo Fresha como canal de reserva.
- Fresha no expone ningun campo de website propio para esta ficha.
- Conclusion: `has_own_site: false`.

## Menu de servicios (verificado, extraido directo del payload de Fresha)
15 servicios confirmados en 3 categorias (Facial Care, Face Massage, Eyelash Extensions), con nombre, precio y duracion exactos. Fresha reporta `serviceCount: 21` en sus metadatos pero solo 15 aparecen con datos completos en el payload publico; el sitio y el registro solo usan los 15 verificados, nunca se completo el resto por adivinanza.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- **Fresha**: revisado el payload completo `__NEXT_DATA__` de la ficha (`location.owner`, `location.employeeProfiles`, etc). Sin campo de email publico en ningun nodo.
- **Instagram** (`web_profile_info`, header `x-ig-app-id`): bloqueado por rate-limit de Instagram desde esta red 3 veces seguidas ("Please wait a few minutes"). Se recurrio al microservicio dedicado (`ig_photos.py` / IP alterna) que SI trajo las fotos del feed, pero ese servicio no expone `business_email` (solo URLs de imagenes). No se confirmo ni descarto un business_email de IG con certeza.
- **Bio de Instagram**: sin link externo/linktree visible en las busquedas realizadas (no se encontro un linktr.ee ni beacons.ai asociado).
- **Facebook**: no se encontro una pagina de Facebook propia del negocio en las busquedas realizadas.
- **Busqueda web dirigida** ("Flare Lashes and Brow Lounge" email/contact/Facebook, variantes con linktree): ningun resultado con email publico.
- Conclusion: sin email publico verificable tras busqueda exhaustiva por los canales disponibles en esta sesion. `email: null`. Queda pendiente reintentar el endpoint directo de IG (web_profile_info) en otra ventana horaria por si el rate-limit se libera, ya que ese es el unico canal no cerrado del todo.

## Subject (para cuando haya un canal de email)
A sample website for Flare Lashes & Brow Lounge (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi,

I'm Michael, from Merktop. I came across Flare Lashes & Brow Lounge and saw your 5.0 rating from 201 reviews on Fresha, so I took a closer look at your lash work.

I noticed your only online presence is Instagram and your Fresha booking page, no website of your own, so I went ahead and built you a sample one with your real services, real prices and real photos:

https://siteforge-demos.odd-forest-9504.workers.dev/flare-lashes-brow-lounge-miramar/

Two things worth knowing:
- It does not touch your booking at all. Every appointment still goes straight to your Fresha page, exactly like today.
- It is bilingual (English and Spanish), ready for more of Miramar to find you.

If you like it, I can put it on your own domain and we can tweak it together. If it is not for you, I will take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message, 431 caracteres)

Hi! I'm Michael, from Merktop. I saw Flare Lashes & Brow Lounge has a 5.0 rating from 201 reviews on Fresha, so I built you a sample website with your real services, prices and photos: https://siteforge-demos.odd-forest-9504.workers.dev/flare-lashes-brow-lounge-miramar/ It does not touch your Fresha booking at all. If you like it, I can put it on your own domain, if not I will take it down, no pressure either way.
