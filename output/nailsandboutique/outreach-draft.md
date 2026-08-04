# Outreach draft: Nails and Boutique (nailsandboutique)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico encontrado. Canal de contacto: Instagram DM (@nails_and_boutique, 8.4K seguidores). Sin telefono publico, sin Facebook.
- **De**: Michael Vargas <michael@go.merktop.com> (no usable todavia, no hay email; queda para si aparece uno)
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-nailsandboutique-2026-08-04
- **Angulo**: no tiene website propio (has_own_site: false) -> "le arme un sitio de muestra"
- **Idioma**: ingles (idioma principal del negocio: mayoria de resenas y captions en ingles, con excepciones puntuales en espanol)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/nailsandboutique/

## Cuerpo (usar como base para Instagram DM)

Hi Rosalia,

I'm Michael, from Merktop. I found Nails and Boutique on Booksy and saw your perfect 5.0 across 39 reviews, clients keep saying you never disappoint and bring their vision to life.

I noticed you don't have your own website yet, just Instagram and Booksy, so I built you a sample one with your real photos, your full menu with the prices you publish on Booksy, and your verified reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/nailsandboutique/

Two important things:
- It does not touch your operation or your bookings at all, the book button still goes straight to your Booksy.
- It is bilingual (English and Spanish) with a small toggle in the corner.

If you like it, we would gladly put it on your own domain and refine it together. If not, no problem, I will take it down, no strings attached.

Best,
Michael Vargas
Merktop · merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi Rosalia! I'm Michael, from Merktop. Found Nails and Boutique on Booksy, a perfect 5.0 with 39 reviews and clients raving about your attention to detail. Since you don't have a website, I built a sample one with your real photos, full menu and prices: https://siteforge-demos.odd-forest-9504.workers.dev/nailsandboutique/ It does not touch your Booksy bookings. If you like it we put it on your own domain, if not I take it down, no problem.

## Nota de canal

No se encontro email publico ni telefono publico tras revisar: la pagina de Booksy en vivo (WebFetch directo, campo telefono muestra "Not displayed on page"), el payload/JSON del venue en Booksy (booksy_dossier.py, phone: null), el perfil de Instagram @nails_and_boutique (dos intentos via WebFetch, ambos HTTP 429; per FORGE-BRIEF el endpoint web_profile_info de IG es conocido por fallar), busqueda general en Google (sin resultados de email/telefono propios), y busqueda especifica de una pagina de Facebook del negocio (no se encontro ninguna, solo otros negocios de nombre similar). Se probaron ademas 3 dominios propios candidatos (nailsandboutiquemiami.com, nailsandboutique.com, nailsandboutiquemiami.net): ninguno resuelve, confirmando has_own_site: false. Por ahora outreach queda `pending_manual` via Instagram DM (@nails_and_boutique). No se contacto al negocio bajo ninguna circunstancia durante este research.
