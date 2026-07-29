# Outreach draft - Sunny Nails (sunny-nails-north-miami-beach)

## Datos de contacto
- Negocio: Sunny Nails by Mairi
- Direccion: 16215 Biscayne Blvd, Suite 108, North Miami Beach, FL 33160
- Telefono: (786) 712-4679 (confirmado en letrero real de la tienda y en directorio nailmastersusa.com)
- Booksy (reservas reales, contractor 1237239): https://booksy.com/en-us/1237239_sunny-nails_nail-salon_15892_north-miami-beach
- Instagram: @sunny_nails_by_mairi (https://www.instagram.com/sunny_nails_by_mairi/) (handle confirmado via el campo `instagramLink` del propio payload de Booksy del venue 1237239, address exacta coincide; el contenido del perfil no se pudo scrapear por bloqueo de red del entorno)
- Email publico: NO ENCONTRADO tras busqueda profunda (payload de Booksy del venue y del contractor sin campo email, sin Facebook encontrado, bio de IG inaccesible por bloqueo de red, directorio nailmastersusa.com sin email)
- Idioma principal: en (bilingue real: la propia descripcion de Booksy dice "We speak both English and Spanish"; mayoria de reviews en ingles)
- Rating: 5.0 · 51 reseñas en Booksy
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/sunny-nails-north-miami-beach/
- has_own_site: false (sunnynailsnmb.com, sunnynailsnorthmiamibeach.com, sunnynailsbymairi.com, sunnynails-nmb.com y sunnynailsmiami.com no resuelven; Booksy tiene `website: null`)

## Estado de outreach
`outreach: pending_manual`: no hay email publico verificado. Canal recomendado: DM de Instagram (@sunny_nails_by_mairi) o WhatsApp/llamada al (786) 712-4679. El borrador de email queda listo mas abajo por si en el futuro se confirma un email (ej. si lo comparten al contactarlos, o aparece en un formulario de contacto).

---

## Borrador de email (para cuando/si haya email; idioma principal: en)

**To:** (sin confirmar)
**From:** Michael Vargas <michael@go.merktop.com>
**Reply-To:** jose@merktop.com
**Subject:** A free sample website for Sunny Nails by Mairi

Hi Mairi,

I came across Sunny Nails on Booksy and had to reach out, a perfect 5.0 rating across 51 reviews is rare, and North Miami Beach clients keep mentioning how attentive and detailed your work is (the Russian hard gel manicures especially).

I noticed the salon does not have its own website yet, so I put together a free sample site using your real photos, services and reviews. You can see it here:

https://siteforge-demos.odd-forest-9504.workers.dev/sunny-nails-north-miami-beach/

A few things worth knowing:
- It does not touch your Booksy setup at all. Clients would still book exactly the way they do now.
- If you like it, I would be happy to put it on your own domain for a flat setup fee.
- If it is not for you, no problem at all, I will simply take it down. Zero obligation either way.

Let me know what you think.

Warm regards,
Michael Vargas
Merktop

---

## dm_message (max 450 caracteres, para DM de Instagram o WhatsApp, idioma principal: en)

Hi! Found Sunny Nails on Booksy, a perfect 5.0 across 51 reviews, love the Russian hard gel manicures. Since you do not have your own website yet, I built a free sample site with your real photos, services and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/sunny-nails-north-miami-beach/ It does not touch your Booksy setup. Happy to put it on your own domain or take it down, zero obligation. Michael Vargas, Merktop.

(432 caracteres)

---

## Notas para revision humana
- Ojo con negocios homonimos: existen muchisimos "Sunny Nails" en otras ciudades/estados en Instagram (Cambridge MA, Rockaway Park, Oakville, etc.) y hasta otro perfil "@sunny_nails_official" que NO corresponde a este local. El handle usado (@sunny_nails_by_mairi) se confirmo por el campo oficial `instagramLink` del propio backend de Booksy para el negocio con la direccion exacta 16215 Biscayne Blvd, 108, North Miami Beach, no por busqueda libre.
- El negocio tiene DOS IDs en Booksy para la misma direccion: 1237240 (ficha del "venue"/local, sin servicios ni reseñas online) y 1237239 (perfil de la contratista Mairim, con el menu completo, horario, staff y reseñas). El site y todos los CTA de reserva usan el 1237239, que es el que realmente permite reservar online.
- El entorno de esta sesion no tuvo acceso de red a Instagram (bloqueado / ERR_CONNECTION_RESET tanto por Playwright como por la API web_profile_info), asi que no se pudieron descargar fotos ni bio desde IG directamente. Toda la galeria (17 fotos reales, logo, portadas, inspiracion y fotos de reseñas) se obtuvo del payload propio de Booksy (`__NUXT_DATA__`) del contractor 1237239, que resulto mucho mas rico que el HTML/JSON-LD superficial de la pagina.
- Verificar en un navegador real (no headless) el efecto de scroll-reveal del hero y el mapa embed de Google (en este sandbox sin internet no cargaron, pero el HTML y la URL son correctos).
- Si en algun momento se confirma un email real del negocio, usar el borrador de arriba tal cual.
