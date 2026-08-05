# Outreach draft: Exclusive Art Tattoo Studio (exclusive-art-tattoo-orlando)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (bio de Instagram, pagina de booking Porter del artista, y perfil de Facebook revisados; ver seccion "Busqueda de email" abajo para el detalle completo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-exclusive-art-tattoo-orlando-2026-08-05
- **Angulo**: sin website propio (los 5 dominios candidatos investigados previamente no resuelven DNS; solo Booksy e Instagram)
- **Idioma**: ingles (idioma principal del negocio)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/exclusive-art-tattoo-orlando/
- **Canal disponible**: sin email publico confirmado. Registrado como `outreach: pending_manual` con telefono +1 (678) 326-6510 (encontrado en la bio de Instagram) y su Instagram @chris_deuce_allen para DM/WhatsApp manual.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- Booksy: campo telephone/email no publicado en el payload del venue.
- Bio de Instagram (@chris_deuce_allen, renderizada con Playwright / chrome fijo por el problema de TLS del proxy): solo expone telefono (678-326-6510) y un link de booking (web.getporter.io/artist/inkaholic-deuce), sin campo de email.
- Pagina de booking Porter (web.getporter.io/artist/inkaholic-deuce): renderizada con Playwright, solo muestra un formulario de nombre para agendar, sin email visible ni en el HTML ni en el DOM renderizado. Nota: esa pagina de Porter lista una direccion en Douglasville, GA, distinta a la de Orlando: el artista aparentemente atiende ambas ubicaciones (bio dice "Celebrity Artist Atlanta-Orlando"), pero el negocio de este research es especificamente el de Orlando (Booksy, direccion y reviews verificados ahi).
- Facebook del same_as de Booksy (facebook.com/deuce.mcfly.3): redirige a login sin acceso publico al About.
- Busqueda web de "Exclusive Art Tattoo" + Orlando + email/phone: sin resultado adicional (solo referencias a Booksy y otros estudios de Orlando sin relacion).
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Subject (para cuando haya un canal de email)
A sample website for Exclusive Art Tattoo Studio (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi Chris,

I'm Michael, from Merktop. I found Exclusive Art Tattoo Studio on Booksy and a perfect 5.0 from 65 reviews caught my eye, so I took a closer look at your black and grey, lettering and color work.

I noticed you don't have your own website, just Booksy and Instagram, so I went ahead and built you a sample one with your real sizing menu, real reviews and real photos of your work:

https://siteforge-demos.odd-forest-9504.workers.dev/exclusive-art-tattoo-orlando/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Booksy, exactly like today.
- It's bilingual (English and Spanish), ready for both sides of your Orlando client base.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you, I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi Chris! I'm Michael, from Merktop. I saw Exclusive Art Tattoo has a perfect 5.0 from 65 reviews on Booksy, so I built you a sample website with your real work, prices and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/exclusive-art-tattoo-orlando/ It doesn't touch your Booksy booking at all. If you like it, I can put it on your own domain, if not I will take it down, no pressure either way.
