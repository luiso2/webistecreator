# Outreach draft: Wildflower Wellness (wildflower-wellness)

- **Estado**: pending_manual (NO enviar email, no se encontro email publico)
- **Para**: sin email publico verificado (ver seccion abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-wildflower-wellness-2026-08-06
- **Angulo**: sin website propio (`has_own_site: false`)
- **Idioma**: ingles (idioma principal del negocio: bio de IG, reseñas y menu en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/wildflower-wellness/
- **Telefono verificado**: (352) 514-0234 (texto preferido, segun su propia bio: "As a micro spa, we're often with clients, so texting is the fastest way to reach us")
- **Instagram**: @wildflowerwellness.gnv
- **Canal disponible para outreach**: WhatsApp/SMS al (352) 514-0234 o DM en Instagram. Sin email, este borrador queda como referencia para el envio manual, no se manda.

## Verificacion de rating
- Reportado de forma consistente en 5.0 con aproximadamente 94 reseñas en multiples fuentes
  secundarias (agregadores tipo Vagaro/directorios de bienestar), no se extrajo directamente de
  Google Maps en vivo en esta sesion. Por eso el site y este borrador citan "5.0 rating" sin afirmar
  un numero exacto de reseñas de Google no verificado de primera mano.
- Reseñas verbatim reales confirmadas en su pagina de Vagaro (5 encontradas, nombre, fecha y texto
  original), usadas en el site: Elana R. (09 abr 2026), Natalie H. (29 mar 2026), Laura W. (16 ene
  2026), Jessica K. (09 nov 2025, sobre Cayman T.), Britt R. (30 mar 2024).

## Chequeo de website propio
- Probado `wildflower-wellness.life` (aparecio en resultados de busqueda con titulo "Wildflower
  Wellness | Holistic Massage & Esthetics | Gainesville"): el dominio NO resuelve (falla de DNS /
  502 en el tunel de conexion), confirmado con curl directo. No es un sitio propio activo.
- Vagaro (vagaro.com/wildflowerwellnessgainesville) es su canal de reservas real, confirmado como
  "Website" en un listado agregador (meditateflorida.com).
- Fresha tiene una ficha para este negocio pero es explicitamente "not currently affiliated with or
  partnered with Fresha": un listado de lead-gen no afiliado, no su canal.
- No se encontro ningun dominio propio activo ni pagina de Facebook dedicada verificable para este
  negocio especifico (varias paginas de Facebook con nombres similares "Wildflower Wellness" en
  otras ciudades, ninguna corresponde a Gainesville).
- Conclusion: `has_own_site: false`.

## Verificacion de email (busqueda profunda, sin resultado)
- IG web_profile_info (`i.instagram.com/api/v1/users/web_profile_info/?username=wildflowerwellness.gnv`):
  bloqueado por rate limit en 2 intentos (401, "please wait a few minutes"), segun regla del pipeline
  se paso a otras fuentes tras el segundo intento fallido.
- Vagaro: paginas principal, /photos, /gallery, /about y /services revisadas, sin mailto ni email
  visible en el HTML estatico.
- Fresha (listado no afiliado): sin email.
- meditateflorida.com (directorio): sin email.
- Facebook: no se encontro una pagina oficial dedicada a este negocio.
- Sunbiz/bizprofile.net (registro de la LLC): solo expone el agente registrado y direccion legal,
  no un email de contacto al publico, no se usa como email del negocio.
- Conclusion: sin email publico encontrado. `outreach: pending_manual`, contactar por texto/WhatsApp
  al (352) 514-0234 o DM a @wildflowerwellness.gnv.

## Subject (referencia, para cuando se use email si aparece)
A sample website for Wildflower Wellness (it's ready)

## Cuerpo (referencia)

Hi Alethea and Cayman,

I'm Michael, from Merktop. I found Wildflower Wellness while looking at holistic skincare and
massage spots in Gainesville, your 5.0 rating caught my eye, and I took a closer look at your work.

I noticed you don't have your own website, just your Vagaro booking page and Instagram, so I went
ahead and built you a sample one with your real services, reviews and photos:

https://siteforge-demos.odd-forest-9504.workers.dev/wildflower-wellness/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Vagaro page,
  exactly like today.
- It's bilingual (English and Spanish), so more of Gainesville can read it.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you,
I'll take it down, no hard feelings either way. Feel free to text me back at this same number if
that's easier.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi! I'm Michael from Merktop. I found Wildflower Wellness, saw your 5.0 rating, and built you a
sample website with your real services, reviews and photos:
https://siteforge-demos.odd-forest-9504.workers.dev/wildflower-wellness/ It does not touch your
Vagaro booking at all. Like it, keep it on your domain. If not, I will take it down, no pressure.
