# Outreach draft — Meri's Beauty Studio (Jacksonville, FL)

**Status:** pending_manual (no se encontro email publico tras busqueda profunda)

## Datos de contacto encontrados
- Telefono: (904) 654-6396 (visible en Booksy)
- Instagram: [@miss__meriss](https://www.instagram.com/miss__meriss/)
- Booksy: https://booksy.com/en-us/1126607_meris-beauty-studio-massage-waxing-sugaring-facials_massage_15697_jacksonville
- Direccion: 9825 San Jose Blvd, Suite 32, Jacksonville, FL 32257
- Email publico: **no encontrado**. Se intento:
  - `scripts/ig_contact.py miss__meriss` (2 intentos, `net::ERR_CONNECTION_RESET` ambas veces, sin bio ni links)
  - Payload de Booksy (solo aparece `help.us@booksy.com`, soporte de Booksy, no del negocio)
  - Busqueda de pagina de Facebook dedicada al negocio (no se encontro una que coincida con esta ubicacion; los resultados de "Meri's Beauty" en Facebook son otros negocios sin relacion)
  - Yelp (bloquea scraping, HTTP 403; datos de direccion/telefono/horario confirmados via WebSearch en su lugar)
  - Dominios propios probados: merisbeautystudio.com, merisbeautywax.com, merisbeautystudiojax.com, meribeautystudio.com — ninguno resuelve a un sitio del negocio (el ultimo es un dominio parqueado de OVHcloud sin relacion)
- **Canal recomendado para el primer contacto: DM de Instagram o llamada/SMS al telefono publicado.**

## Borrador de email (para cuando/si se consiga el email, o para adaptar a DM largo)

**Asunto:** A sample website for Meri's Beauty Studio

**Cuerpo:**

Hi Meri,

My name is Michael, I work with Merktop here in Florida. I came across Meri's Beauty Studio on Booksy: a perfect 5.0 with 50 reviews is hard to find, so I wanted to reach out.

Since I didn't see a website of your own, I put together a sample site for the studio, using your real services, prices and photos: https://siteforge-demos.odd-forest-9504.workers.dev/meris-beauty-studio-jacksonville/

It doesn't touch your Booksy booking at all, it's just a preview of what a dedicated website could look like. If you like it, I'm happy to hand it over on your own domain. If it's not for you, no problem, I'll take it down, no strings attached.

Would you be open to a quick look?

Best,
Michael Vargas
Merktop
https://merktop.com

## dm_message (DM de Instagram / WhatsApp, 395 caracteres)

Hi! I'm Michael from Merktop. I saw Meri's Beauty Studio on Booksy, 5.0 with 50 reviews, really impressive. Since you don't have your own website, I put together a sample one with your real services and photos: https://siteforge-demos.odd-forest-9504.workers.dev/meris-beauty-studio-jacksonville/ It doesn't touch your Booksy booking. Happy to hand over the domain, or take it down, no pressure.

## Notas
- Angulo: `has_own_site: false` → "les construi un sitio de muestra".
- Idioma: EN (resenas y marca en ingles, Jacksonville FL).
- NO se envio nada. Este archivo es solo el borrador para aprobacion humana.
