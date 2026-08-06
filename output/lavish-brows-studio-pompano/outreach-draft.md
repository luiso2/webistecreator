# Outreach draft: Lavish Brows Studio & Academy (lavish-brows-studio-pompano)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-lavish-brows-studio-pompano-2026-08-06
- **Angulo**: sin website propio (ver seccion "Chequeo de website propio")
- **Idioma**: ingles (idioma principal del negocio: feed de IG, testimonios y menu de Square en ingles; bio nota "Se habla espanol" pero el contenido publico es en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/lavish-brows-studio-pompano/
- **Telefono verificado**: (561) 262-5002
- **Canal disponible**: sin email publico confirmado. Registrado como `outreach: pending_manual` con telefono (561) 262-5002 y su Instagram @lavishbrows___ (24.8K seguidores) para DM/WhatsApp/llamada manual.

## Verificacion de rating y reseñas en Google (gate obligatorio, hecho de forma independiente)
- El listado de Atly mostraba "8.9/10, 45 reseñas" citando Google como fuente, pero esa escala 8.9/10 no es la escala nativa de Google (5 estrellas) y no se acepto como prueba por si sola.
- Se ubico el `place_id` real del negocio (`ChIJU0vaskQD2YgRTGPTbzCWImA`, visible en la URL de imagen del listado de Atly) y se verifico independientemente:
  1. Se convirtio el hex del CID embebido en el place_id (`602296306fd3634c` = `6927264311627965260` en decimal).
  2. Se resolvio `search.google.com/local/reviews?placeid=ChIJU0vaskQD2YgRTGPTbzCWImA` y Google redirigio a una URL con `ludocid=6927264311627965260`, exactamente el mismo numero: confirma que el place_id pertenece a ESTE negocio.
  3. Se consulto DIRECTAMENTE el endpoint interno de Google Maps (`/maps/preview/place`) con ese place_id, dos veces por separado, y ambas devolvieron el nombre "Lavish Brows Studio & Academy", la direccion "2240 N Federal Hwy, Pompano Beach, FL 33062" y **rating 4.9** en el campo nativo de Google (escala de 5 estrellas), sin pasar por Atly.
  4. El mismo payload de Google confirma que el campo "website" de su ficha de Google Business apunta unicamente a `lavishbrowsbooking.square.site` (no a un dominio propio).
- El numero de reseñas (45) no se pudo re-extraer directamente del endpoint ligero de Google (no lo expone), asi que se mantiene el numero de Atly, pero YA CORROBORADO como perteneciente al place_id correcto de este negocio (no una cifra generica o de otro negocio). Con rating 4.9 y ~45 reseñas, el negocio pasa el filtro (>=4.5 estrellas, >=10 reseñas) con margen amplio.

## Chequeo de website propio
- Ficha de Google Business: campo "website" = `lavishbrowsbooking.square.site` unicamente (confirmado arriba).
- `lavishbrows.com` resuelve pero redirige a HugeDomains ("Buy this domain"): dominio en venta, no operado por el negocio.
- Variantes probadas (`lavishbrowspmu.com`, `lavishbrowsstudio.com`, `lavishbrowsacademy.com`, `lavishbrowsstudioandacademy.com`): las 4 fallan en conectar (sin DNS/servidor).
- Linktree de la bio de IG (`linktr.ee/lavishbrowspmu`) enlaza solo a Square booking, TikTok y un curso de Teachable (academia de PMU). Ningun dominio propio.
- Conclusion: `has_own_site: false`.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- Bio de Instagram (via Playwright, perfil publico): sin email visible, solo linktree.
- `linktr.ee/lavishbrowspmu`: sin email ni formulario propio (solo enlaces a Square y Teachable).
- Pagina de reservas de Square (renderizada con Playwright): sin mailto ni email en todo el texto de la pagina (politicas de deposito mencionan Zelle al mismo telefono, no un email).
- Pagina de Teachable del curso de PMU: sin email visible.
- Perfil de Facebook: bloqueado para lectura automatizada (login wall).
- Busqueda web dirigida ("Lavish Brows PMU" email, variantes @gmail.com): no arrojo ningun email para ESTE negocio especifico (existen otros negocios homonimos en otras ciudades con su propio email, no confundir).
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Subject (para cuando haya un canal de email)
A sample website for Lavish Brows Studio & Academy (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi Marlen,

I'm Michael, from Merktop. I came across Lavish Brows Studio & Academy and saw your 4.9 rating on Google, so I took a closer look at your ombre powder brows and your academy.

I noticed your only online presence is Instagram and your Square booking page, no website of your own, so I went ahead and built you a sample one with your real services, real prices and real photos:

https://siteforge-demos.odd-forest-9504.workers.dev/lavish-brows-studio-pompano/

Two things worth knowing:
- It does not touch your booking at all. Every appointment still goes straight to your Square page, exactly like today.
- It is bilingual (English and Spanish), ready for both sides of your Pompano Beach client base.

If you like it, I can put it on your own domain and we can tweak it together. If it is not for you, I will take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message, 445 caracteres)

Hi Marlen! I'm Michael, from Merktop. I saw Lavish Brows has a 4.9 rating on Google, so I built you a sample website with your real services, prices and photos: https://siteforge-demos.odd-forest-9504.workers.dev/lavish-brows-studio-pompano/ It does not touch your Square booking at all. If you like it, I can put it on your own domain, if not I will take it down, no pressure either way.
