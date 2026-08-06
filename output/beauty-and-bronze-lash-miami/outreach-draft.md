# Outreach draft: Beauty and Bronze Lash Studio (beauty-and-bronze-lash-miami)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-beauty-and-bronze-lash-miami-2026-08-06
- **Angulo**: sin website propio (ver seccion "Chequeo de website propio")
- **Idioma**: ingles (idioma principal del negocio: bio de IG y menu de Fresha en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/beauty-and-bronze-lash-miami/
- **Telefono verificado**: (628) 800-1738 (campo `contactNumber` del payload propio de Fresha)
- **Canal disponible**: sin email publico confirmado. Registrado como `outreach: pending_manual` con telefono y su Instagram @beautynbronze para DM/llamada/mensaje de texto manual.

## Chequeo de website propio
- `beautyandbronze.com` responde 200 pero es un redirect JS a `/lander`, que a su vez es la pagina de "Access Denied" de un dominio EN VENTA en GoDaddy (`forsale.godaddy.com/forsale/beautyandbronze.com`). No es un sitio operativo del negocio.
- Variantes (`beautyandbronzelash.com`, `beautyandbronzelashstudio.com`, `beautynbronze.com`, `beautyandbronzelashmiami.com`): ninguna resuelve a un sitio real.
- `external_url` de la bio de Instagram (@beautynbronze, via `web_profile_info`): apunta directo a la pagina de reservas de Fresha, no a un dominio propio.
- Bio de IG, pagina de Fresha y busqueda web: sin mencion de dominio propio en ningun lado.
- Conclusion: `has_own_site: false`.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- IG `web_profile_info`: `business_email` y `business_phone_number` ambos `null`.
- Bio de IG: sin linktree/poplme, solo el link de Fresha.
- Payload de venue de Fresha (`__NEXT_DATA__` de la pagina de reservas): sin campo de email en ningun nivel del JSON.
- Sin pagina de Facebook propia encontrada tras busqueda (los resultados devuelven negocios homonimos no relacionados).
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Nota sobre el rating (Fresha, no Google)
- El rating y conteo de reseñas (5.0 · 210) se tomaron directo del payload propio de Fresha (`location.rating` y `location.reviewsTotal`), la fuente de reservas real del negocio, con reseñas verbatim verificadas (Vanessa M, Andrea G, Samuel H, entre otras).
- Se intento verificar el mismo dato directamente en la ficha de Google Maps del negocio, pero en este entorno Google Maps/Search bloquea el scraping sin ejecutar JavaScript (challenge anti-bot), por lo que no se pudo confirmar independientemente un rating de Google. El copy del site es honesto al respecto: dice "en Fresha" en vez de atribuirlo a Google.

## Subject (para cuando haya un canal de email)
A sample website for Beauty and Bronze Lash Studio (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi Drea,

I'm Michael, from Merktop. I came across Beauty and Bronze on Fresha and a 5.0 rating across 210 reviews caught my eye, so I took a closer look at your lash and brow work.

I noticed you don't have your own website, just Fresha and Instagram, so I went ahead and built you a sample one with your real menu, real reviews and real photos of your work:

https://siteforge-demos.odd-forest-9504.workers.dev/beauty-and-bronze-lash-miami/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Fresha, exactly like today.
- It's bilingual (English and Spanish), ready for both sides of your Brickell / Little Havana client base.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you, I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi Drea! I'm Michael, from Merktop. I saw Beauty and Bronze has a 5.0 rating across 210 reviews on Fresha, so I built you a sample website with your real services, prices and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/beauty-and-bronze-lash-miami/ It doesn't touch your Fresha booking at all. If you like it, I can put it on your own domain, if not I will take it down, no pressure either way.
