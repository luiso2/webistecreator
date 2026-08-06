# Outreach draft: Beauty Blossom Spa (beauty-blossom-spa-west-palm-beach)

- **Estado**: draft (email publico encontrado y verificado, ver abajo)
- **Para**: BBSpabyAmparo@gmail.com
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-beauty-blossom-spa-west-palm-beach-2026-08-06
- **Angulo**: sin website propio (`has_own_site: false`) -> "te construi un website de muestra"
- **Idioma**: ingles (idioma principal del negocio: listado de Booksy, banner promocional propio y reseñas, todos en ingles; el nombre de la dueña sugiere origen hispanohablante pero su material publico es en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/beauty-blossom-spa-west-palm-beach/
- **Telefono verificado**: (561) 267-8871 (coincide en Booksy, banner promocional propio y mencion de TikTok)
- **Instagram**: @beautyblossomspa
- **TikTok**: @bbspabyamparo
- **Direccion**: 6305 S Dixie Hwy, West Palm Beach, FL 33405

## Verificacion de rating
- El dato inicial (5.0 estrellas, 16 reseñas, fuente agregador citando Google) se re-verifico en
  esta sesion via `medspanear.me/florida/west-palm-beach/` (directorio que replica fichas de Google
  Business), que muestra el mismo direccion y telefono exactos ((561) 267-8871, 6305 S Dixie Hwy) y
  confirma "5.0 stars with 16 reviews". Una segunda busqueda web independiente arrojo la misma cifra
  ("5-star rating from 16 reviews") sin llegar a abrir Google Maps en vivo (JS no accesible por
  WebFetch en esta sesion), asi que el numero se cita como reportado de fuentes que replican datos de
  Google, no leido directamente del widget de Maps.
- Por separado, el propio listado de Booksy del negocio (JSON-LD, fuente primaria distinta) muestra
  5.0 con 2 reseñas nativas de Booksy (menor volumen, plataforma distinta): "Juana N." y "Cynthia T.",
  ambas usadas verbatim en el site con su fuente correctamente atribuida a Booksy. El badge de rating
  del hero cita el numero de Google (16) porque es la fuente que declara DESIGN.md para el badge
  principal; las 2 quotes visibles en el site se atribuyen honestamente a Booksy, no a Google.

## Chequeo de website propio
- Probados `beautyblossomspa.com`, `www.beautyblossomspa.com`, `beautyblossomspa.net` y
  `beautyblossomspa.co` por curl: los 4 fallan la conexion TLS (dominio no resuelve), consistente con
  que ninguno esta registrado o activo.
- El JSON-LD de Booksy no expone ningun `website_candidates` (campo vacio).
- Un directorio agregador (medspanear.me) muestra explicitamente "Website: Not provided" para esta
  ficha.
- El unico enlace externo publico conocido es Booksy (plataforma de terceros, no cuenta como sitio
  propio) y su Instagram/TikTok/Facebook.
- Conclusion: `has_own_site: false`.

## Verificacion de email (encontrado y confirmado en fuente propia)
- El email `BBSpabyAmparo@gmail.com` (dado como dato inicial) se CONFIRMO de forma independiente en
  esta sesion: aparece impreso, junto al mismo telefono (561) 267-8871 y el mismo @beautyblossomspa
  de Instagram, en un banner promocional propio del negocio ("BOOK NOW") que forma parte de su propia
  galeria de fotos en Booksy (archivo descargado y verificado visualmente, luego descartado de la
  galeria final del site por ser un grafico con texto superpuesto, no una foto real de servicio).
- Es una direccion Gmail, no un dominio propio: no cambia la conclusion de `has_own_site: false`.
- No se encontro un email adicional o alternativo en Facebook, TikTok o el JSON-LD de Booksy (campo
  de telefono tambien vacio ahi; el telefono real se confirmo por las mismas fuentes cruzadas).
- Conclusion: `outreach: draft`, email verificado por fuente propia del negocio, listo para envio
  manual tras aprobacion del usuario.

## Subject (referencia)
A sample website for Beauty Blossom Spa (it's ready)

## Cuerpo (referencia)

Hi Amparo,

I'm Michael, from Merktop. I found Beauty Blossom Spa while looking at aesthetic medicine and med
spas in West Palm Beach, your 5.0 rating caught my eye, and I took a closer look at your treatments.

I noticed you don't have your own website yet, just your Booksy booking page and Instagram, so I
went ahead and built you a sample one with your real treatments, prices and photos:

https://siteforge-demos.odd-forest-9504.workers.dev/beauty-blossom-spa-west-palm-beach/

Two things worth knowing:
- It doesn't touch your booking at all. Every appointment still goes straight to your Booksy page,
  exactly like today.
- It's bilingual (English and Spanish), so more of West Palm Beach can read it.

If you like it, I can put it on your own domain and we can tweak it together. If it's not for you,
I'll take it down, no hard feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Version corta para DM / WhatsApp (dm_message)

Hi Amparo! I'm Michael from Merktop. I found Beauty Blossom Spa, saw your 5.0 rating on Google, and
built you a sample website with your real treatments, photos and reviews:
https://siteforge-demos.odd-forest-9504.workers.dev/beauty-blossom-spa-west-palm-beach/ It does not
touch your Booksy booking at all. Like it, keep it on your own domain, no cost to try. If not, no
pressure, I will take it down.

(402 caracteres, dentro del limite de 450)
