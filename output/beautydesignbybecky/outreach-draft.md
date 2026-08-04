# Outreach draft: Beauty Design by Becky (beautydesignbybecky)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico encontrado. Canal de contacto: llamada/texto al +1 305-202-0909 (publico en Fresha) o Instagram DM (@beautydesignbybecky).
- **De**: Michael Vargas <michael@go.merktop.com> (no usable todavia, no hay email; queda para si aparece uno)
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-beautydesignbybecky-2026-08-04
- **Angulo**: no tiene website propio (has_own_site: false, verificado probando 5 variantes de dominio, todas sin DNS) -> "le arme un sitio de muestra"
- **Idioma**: ingles (idioma principal del negocio: bio propia de Rebeca en Fresha esta en ingles, Fresha detecta language=en, y la mayoria de sus 20 resenas con autor son en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/beautydesignbybecky/

## Cuerpo (usar como base para llamada, texto o Instagram DM)

Hi Becky,

I'm Michael, from Merktop. I found Beauty Design by Becky on Fresha and saw your perfect 5.0 across 63 reviews, clients keep saying you never miss and that your lashes always look full and natural.

I noticed you don't have your own website yet, just Instagram and Fresha, so I put together a sample one with your real photos, your full service menu with the prices you publish on Fresha, and your verified reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/beautydesignbybecky/

Two things worth knowing:
- It does not touch your booking at all, the book button still goes straight to your Fresha page.
- It's bilingual (English and Spanish) with a small toggle in the corner.

If you like it, we're happy to put it on your own domain and fine-tune it together. If not, no problem, I'll take it down, no strings attached.

Best,
Michael Vargas
Merktop · merktop.com

## Version corta para DM / WhatsApp / texto (dm_message)

Hi Becky! I'm Michael, from Merktop. Saw Beauty Design by Becky on Fresha, 5.0 with 63 reviews and clients raving about your lash work. Since you don't have your own website, I put together a sample one with your real photos, menu and prices: https://siteforge-demos.odd-forest-9504.workers.dev/beautydesignbybecky/ It doesn't touch your Fresha booking. Like it, we put it on your domain. If not, no problem, I'll take it down.

## Nota de canal
No se encontro email publico tras revisar: Fresha location.email (null en el payload estructurado), la pagina de Fresha completa buscando mailto/direcciones (ninguna real, solo un endpoint de Sentry no relacionado), y busqueda web general por el nombre del negocio + "facebook"/"contact" (solo aparecen otros negocios "Beauty by Becky" sin relacion, en otras ciudades). No se pudo extraer el texto de la bio de Instagram via Playwright (el metodo usado capturo imagenes del perfil pero no el bio/external_url; reintentar con scroll o el endpoint de bio arriesgaba rate-limit tras ya haber usado la cuota de IG en esta corrida). Outreach queda `pending_manual` via telefono +1 305-202-0909 (publico en Fresha, funciona tambien para SMS/WhatsApp) o Instagram DM (@beautydesignbybecky). No se contacto al negocio bajo ninguna circunstancia durante este research.
