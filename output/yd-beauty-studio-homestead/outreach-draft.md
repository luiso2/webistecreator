# Outreach draft: YD Beauty Studio (yd-beauty-studio-homestead)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sin email publico confirmado (ver seccion "Busqueda de email" abajo)
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-yd-beauty-studio-homestead-2026-08-05
- **Angulo**: sin website propio (ver seccion "Chequeo de website propio")
- **Idioma**: ingles (idioma principal del negocio, reseñas en ingles, `language: "en"` en data.json)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/yd-beauty-studio-homestead/
- **Canal disponible**: telefono verificado (786) 217-7006 (de su propia tarjeta de presentacion, foto `bk-1.jpg`) e Instagram @ydbeautystudio (653 seguidores) para llamada/SMS/DM manual.

## Chequeo de website propio
- `data.json`: `website_candidates` vacio.
- Busqueda web de "YD Beauty Studio" Homestead: unicos resultados son su ficha de Booksy, su Instagram (@ydbeautystudio, cuenta de Yaremis Decespedes) y el directorio de tenants de Cirque Salon Studios (el edificio de suites donde alquila el local, no un sitio propio).
- No aparecio ningun dominio propio (`ydbeautystudio.com` y variantes no se probaron por curl ya que ninguna busqueda arrojo indicio de dominio propio; el unico canal digital es Booksy + Instagram).
- Conclusion: `has_own_site: false`.

## Busqueda de telefono (profundizada, PIPELINE fase 1 punto 7)
- `data.json` (Booksy dossier): `phone: null`, Booksy no publica telefono en su ficha.
- Directorio de tenants de Cirque Salon Studios (`cirquesalonstudios.com/homestead-owners/`, edificio donde alquila la suite 209): listaba "(786) 765-8756" para YD Beauty Studio, PERO el mismo numero aparecia tambien para otro tenant distinto (Nation of Braids, suite 203) en la misma tabla: descartado por no confiable (probable error de copiado en esa pagina).
- **Fuente definitiva**: la propia tarjeta de presentacion del negocio, una de las 16 fotos verificadas descargadas (`assets/raw/bk-1.jpg`), muestra directamente: "YDBEAUTYSTUDIO · Hair, Nails, and much more · 786-217-7006 · 42 W Mowry Dr. Suite #209 · @ydbeautystudio". Coincide exactamente con la direccion y el handle de IG ya conocidos.
- `phone` actualizado en `data.json` a **(786) 217-7006** (primera fuente: material propio del negocio).

## Busqueda de email (profundizada)
- `data.json`: sin campo de email (Booksy no lo publica).
- Pagina de Booksy (WebFetch del HTML): sin `mailto:` ni email visible.
- Instagram @ydbeautystudio (curl directo + WebFetch): pagina no autenticada no expone `business_email` ni `external_url` (Instagram sirve el shell de SPA sin el JSON del perfil a bots); `web_profile_info` esta roto (400) segun leccion ya documentada en FORGE-BRIEF, no se intento.
- Facebook: no se encontro una pagina de Facebook confirmada para este negocio especifico (el ID de Facebook que aparecio en busqueda, "YD Beauty Studio on Reels", resulto pertenecer a un negocio distinto, "DM Beauty Studio-Quiropodia", verificado via WebFetch). La pagina `facebook.com/beautybyyd` no pudo verificarse (login wall).
- Directorio de tenants de Cirque Salon Studios: sin campo de email.
- Conclusion: sin email publico verificable tras busqueda exhaustiva. `email: null`.

## Subject (para cuando haya un canal de email)
A sample website for YD Beauty Studio (it's ready)

## Cuerpo (referencia, para email o como base del DM largo)

Hi Yaremis,

I'm Michael, from Merktop. I found YD Beauty Studio on Booksy and a perfect 5.0 rating across 23 reviews caught my eye, so I took a closer look at your balayage, color and cuts.

I noticed you don't have your own website, just Booksy and Instagram, so I went ahead and built you a sample one with your real menu, real reviews and real photos of your work:

https://siteforge-demos.odd-forest-9504.workers.dev/yd-beauty-studio-homestead/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Booksy, exactly like today.
- It's bilingual (English and Spanish), ready for both sides of your Homestead client base.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you, I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi Yaremis! I'm Michael, from Merktop. I saw YD Beauty Studio has a perfect 5.0 rating across 23 reviews on Booksy, so I built you a sample website with your real work, prices and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/yd-beauty-studio-homestead/ It doesn't touch your Booksy booking at all. If you like it, I can put it on your own domain, if not I will take it down, no pressure either way.
