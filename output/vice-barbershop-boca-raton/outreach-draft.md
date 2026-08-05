# Outreach draft: Vice Barbershop (vice-barbershop-boca-raton)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-vice-barbershop-boca-raton-2026-08-05
- **Angulo**: sin website propio (`vicebarbershop.com`, `vicebarbershopboca.com`, `vicebarbershopfl.com`, `viceboca.com` verificados; ver seccion "Chequeo de website propio")
- **Idioma**: ingles (idioma principal del negocio, reseñas en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/vice-barbershop-boca-raton/
- **Canal disponible**: sin email publico confirmado. Registrado como `outreach: pending_manual` con telefono (561) 480-0287 y su Instagram @vicebarbershop para DM/WhatsApp manual.

## Chequeo de website propio
- `vicebarbershopboca.com`, `vicebarbershopfl.com`, `viceboca.com`, `vicebarbershopbocaraton.com`: sin DNS, no existen.
- `vicebarbershop.com`: SI resuelve (200 OK), pero es un negocio DISTINTO y sin relacion: una barbería en 3345 Boulevard Sainte-Anne, Quebec, QC G1E 3K9, Canada (confirmado via su propio JSON-LD embebido, addressLocality "Quebec", addressCountry "CA"). No cuenta como website propio de este negocio en Boca Raton.
- `website_candidates` en data.json (extraido de Booksy): vacio.
- Conclusion: `has_own_site: false`.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- data.json (extraido del payload de Booksy): sin campo de email.
- Pagina de Booksy (HTML crudo, curl): sin `mailto:`.
- Bio de Instagram (@vicebarbershop, 408 seguidores, 59 posts): endpoint `web_profile_info` devolvio 401/429 (rate limit) en 3 intentos con distintos user-agents; WebFetch directo a instagram.com/vicebarbershop/ devolvio 429 dos veces. No se pudo confirmar `business_email` ni `external_url` por bloqueo de la plataforma.
- Fresha (listado de terceros, no oficial del negocio): "Business Email: Not listed" explicito en la pagina.
- Yelp: bloqueado (403) al fetch directo.
- Busqueda de "Vice Barbershop" + Boca Raton + Facebook: no aparecio ninguna pagina de Facebook del negocio en los resultados.
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Subject (para cuando haya un canal de email)
A sample website for Vice Barbershop (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi there,

I'm Michael, from Merktop. I found Vice Barbershop on Booksy and a 4.9 rating across 136 reviews caught my eye, so I took a closer look at your fades, beard work and hair designs (and the tattoo work too).

I noticed you don't have your own website, just Booksy and Instagram, so I went ahead and built you a sample one with your real menu, real reviews and real photos of your work:

https://siteforge-demos.odd-forest-9504.workers.dev/vice-barbershop-boca-raton/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Booksy, exactly like today.
- It's bilingual (English and Spanish), ready for both sides of your Boca Raton client base.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you, I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi! I'm Michael, from Merktop. I saw Vice Barbershop has a 4.9 rating across 136 reviews on Booksy, so I built you a sample website with your real work, prices and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/vice-barbershop-boca-raton/ It doesn't touch your Booksy booking at all. If you like it, I can put it on your own domain, if not I will take it down, no pressure either way.
