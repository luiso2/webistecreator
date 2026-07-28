# Outreach draft - Isa Nails (isa-nails-hollywood)

## Datos de contacto
- Negocio: Isa Nails
- Artista: Isabel Garcia (manicurista con licencia)
- Direccion: 3251 Hollywood Blvd, Suite 447, Hollywood, FL 33021 (segun Booksy; ver nota de discrepancia con letrero fisico "Suite 132" en data.json)
- Booksy (reservas reales, venue 879004): https://booksy.com/en-us/879004_isa-nails_nail-salon_15645_hollywood
- Instagram: @isanailsig (https://www.instagram.com/isanailsig/) (handle confirmado via el campo oficial `instagramLink` del propio payload de Booksy del venue 879004)
- Telefono: NO ENCONTRADO publico (Booksy no expone el telefono real del negocio en su payload; el numero visible en el HTML es generico de la plataforma Booksy, no del negocio)
- Email publico: NO ENCONTRADO tras busqueda profunda (payload de Booksy sin campo email, sin Facebook encontrado, bio de Instagram inaccesible por bloqueo de API en este entorno, sin website propio del que extraer dominio)
- Idioma principal: en (descripcion oficial del negocio en Booksy en ingles; 7 de las ultimas 10 reseñas en ingles, 3 en espanol)
- Rating: 4.9 · 68 reseñas en Booksy
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/isa-nails-hollywood/
- has_own_site: false (isanails.com pertenece a un salon de unas NO relacionado en Rauenberg/Wiesloch, Alemania; isanailssalon.com es un dominio no relacionado de apuestas en chino; isanailshollywood.com, isanailsfl.com, isanailshollywoodfl.com, isanailsig.com, isabelgarcianails.com e isa-nails.com no resuelven; Booksy payload website=null)

## Estado de outreach
`outreach: pending_manual`: no hay email publico verificado y no hay telefono publico verificado. Canal recomendado: DM de Instagram (@isanailsig) o mensaje directo via Booksy. El borrador de email queda listo mas abajo por si en el futuro se confirma un email.

---

## Borrador de email (para cuando/si haya email; idioma principal: en)

**To:** (sin confirmar)
**From:** Michael Vargas <michael@go.merktop.com>
**Reply-To:** jose@merktop.com
**Subject:** A free sample website for Isa Nails

Hi Isabel,

I came across Isa Nails on Booksy and had to reach out, a 4.9 rating across 68 reviews is great, and clients keep mentioning how much attention to detail you put into every Russian manicure and pedicure.

I noticed the studio does not have its own website yet, so I put together a free sample site using your real photos, services and reviews. You can see it here:

https://siteforge-demos.odd-forest-9504.workers.dev/isa-nails-hollywood/

A few things worth knowing:
- It does not touch your Booksy setup at all. Clients would still book exactly the way they do now.
- If you like it, I would be happy to put it on your own domain for a flat setup fee.
- If it is not for you, no problem at all, I will simply take it down. Zero obligation either way.

Let me know what you think.

Warm regards,
Michael Vargas
Merktop

---

## dm_message (max 450 caracteres, para DM de Instagram, idioma principal: en)

Hi! Found Isa Nails on Booksy, 4.9 across 68 reviews, love the Russian manicure and pedicure work. Since you do not have your own website yet, I built a free sample site with your real photos, services and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/isa-nails-hollywood/ It does not touch your Booksy setup. Happy to put it on your own domain or take it down, zero obligation. Michael Vargas, Merktop.

(418 caracteres)

---

## Notas para revision humana
- Dedup: existe un negocio llamado "Lucelly Isaza Nails + Beauty Studio" (@lucelly_isaza_nails) en Doral, en el registro `data/processed.json`, pero es un negocio distinto (Doral vs Hollywood, nombre distinto: Isaza vs Isa Nails). No hay duplicado real con "Isa Nails" en Hollywood.
- Homonimos: existe otro negocio "Isa Nails And Wax" (@isanails_and_wax) en 4921 Sheridan St, Suite 12, Hollywood FL (Booksy id 1579446, 5.0 con solo 6 reseñas), que NO es el mismo negocio que este (direccion, id de Booksy y volumen de reseñas distintos). Este demo es exclusivamente para "Isa Nails" (venue 879004, 3251 Hollywood Blvd Suite 447, 4.9/68 reseñas), que coincide con el brief asignado.
- La direccion tiene una particularidad: el campo `location.address` del payload de Booksy trae un texto combinado que menciona tanto "Suite 447" como "Suite 132" (con emojis de check). Una foto real del directorio de suites del edificio muestra un letrero fisico "Salon Suite 132" con las tarjetas de presentacion de iSaNAILS. Se uso Suite 447 en el site por ser el dato estructurado oficial de Booksy (y por coincidir con el brief), documentando la discrepancia en `data.json`. Se recomienda verificar en persona o por telefono antes de cualquier impresion fisica (tarjetas, flyers) que use esta direccion.
- Instagram: el handle @isanailsig se confirmo por el campo oficial `instagramLink` del payload de Booksy, no por busqueda libre (hay varios negocios de uñas con "Isa" en el nombre en otras ciudades). El contenido del perfil de Instagram no se pudo scrapear en este entorno (la API `web_profile_info` devolvio HTTP 400 por un error de esquema interno de Instagram), asi que toda la galeria (13 fotos reales) se obtuvo del payload propio de Booksy (`__NUXT_DATA__`) del venue 879004: logo, foto de portada, fotos del negocio, fotos de inspiracion y fotos de cada servicio.
- Telefono: no se encontro ningun telefono publico verificable para este negocio especifico (Google, Fresha, Booksy). El site omite cualquier boton de llamada y usa Booksy + Instagram como unicos canales de contacto, siguiendo la regla de "no rellenar datos no encontrados".
- Verificar en un navegador real (no headless) el efecto de scroll-reveal del hero y el mapa embed de Google (en este sandbox sin internet no cargaron, pero el HTML y la URL son correctos).
- Si en algun momento se confirma un email o telefono real del negocio, usar el borrador de arriba tal cual (o actualizar el CTA de llamada).
