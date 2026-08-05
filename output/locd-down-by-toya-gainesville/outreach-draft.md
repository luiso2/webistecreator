# Outreach draft: Loc'd Down By Toya (locd-down-by-toya-gainesville)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo para el detalle completo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-locd-down-by-toya-gainesville-2026-08-05
- **Angulo**: sin website propio (solo Booksy, Fresha y Facebook; los dominios candidatos no resuelven)
- **Idioma**: ingles (idioma principal del negocio)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/locd-down-by-toya-gainesville/
- **Canal disponible**: sin email publico confirmado. Registrado como `outreach: pending_manual` con telefono (352) 222-4092 y su Instagram @locd_down_by_toya para DM/WhatsApp manual.

## Busqueda de email (profundizada, PIPELINE fase 1 punto 7)
- Booksy: campo email no publicado en el payload del venue ni en el JSON-LD; solo telefono ausente tambien del payload (se confirmo por separado en la foto de tarjeta de negocio de su propia galeria de Booksy: 352-222-4092).
- Instagram (@locd_down_by_toya, sameAs del JSON-LD de Booksy): endpoint web_profile_info bloqueado por Instagram (error de esquema del lado de IG) y WebFetch directo devolvio 429 (rate limit) en dos intentos; sin acceso a business_email ni external_url por esta via.
- Facebook (facebook.com/p/Locd-Down-by-Toya-61565924082142/): la pagina redirige a un muro de login publico, sin acceso al About sin sesion.
- Fresha (fresha.com/lvp/locd-down-by-toya-northwest-23rd-avenue-gainesville-KkQkkR): lista telefono (352) 222-4092 y direccion, pero ningun email; el campo "Website" solo apunta a su subdominio de Booksy (healthylocswics.booksy.com), que no cuenta como sitio propio.
- Busqueda web de "Loc'd Down By Toya" + Gainesville + email: sin resultado adicional (Yelp, Yahoo Local y Booksy repiten los mismos datos de telefono/direccion, sin email).
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Subject (para cuando haya un canal de email)
A sample website for Loc'd Down By Toya (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi Toya,

I'm Michael, from Merktop. I found Loc'd Down By Toya on Booksy and a perfect 5.0 from 83 reviews caught my eye, so I took a closer look at your loc and braid work.

I noticed you don't have your own website, just Booksy, Fresha and Facebook, so I went ahead and built you a sample one with your real services and prices, real reviews and real photos of your work:

https://siteforge-demos.odd-forest-9504.workers.dev/locd-down-by-toya-gainesville/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Booksy, exactly like today.
- It's bilingual (English and Spanish), ready for more of Gainesville to find you.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you, I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi Toya! I'm Michael, from Merktop. I saw Loc'd Down By Toya has a perfect 5.0 from 83 reviews on Booksy, so I built you a sample website with your real services, prices and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/locd-down-by-toya-gainesville/ It doesn't touch your Booksy booking at all. If you like it, I can put it on your own domain, if not I will take it down, no pressure either way.
