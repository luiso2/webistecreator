# Outreach draft: TRILLION STUDIOS (North Miami Beach, FL)

## Datos de contacto
- Nombre: TRILLION STUDIOS (estudio de fotografia y video, renta por hora)
- Direccion: 2265 NE 164th St, Miami, FL 33160 (North Miami Beach City Center)
- Telefono: (305) 900-3231 / +13059003231
- Instagram: no encontrado (ver data.json, `ig_source`)
- Email: no encontrado (ver data.json, `email_notes`)
- Rating: 4.5 en Google, 16 resenas
- has_own_site: false (trillionstudios.com existe pero es una plantilla/portal de software sin relacion operativa real con el negocio; ver `own_site_check` en data.json)
- Canal de reserva real: Tagvenue (https://www.tagvenue.com/us/venues/miami/16216/trillion-studios), el mismo destino del boton "Book online" de su ficha de Google
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/trillion-studios-north-miami/

## ALERTA PARA REVISION HUMANA ANTES DE ENVIAR (leer antes de aprobar el lote)
Entre las 5 resenas con texto que devolvio Google, hay una de 1 estrella (autor "Maurice Exsinor") que acusa publicamente a la gerente del negocio de fraude, estafas y malversacion de fondos, y afirma que "los duenos del estudio lo saben y lo permiten". Es una alegacion grave y publica que no se puede verificar desde este research, pero que el equipo de Merktop deberia conocer antes de decidir si se envia el outreach a este negocio. El resto del research (rating 4.5/16, fotos reales, precios de Tagvenue, ausencia de website propio) es solido y honesto; esta nota es solo para la decision humana de proceder o no con el contacto.

## Angulo (has_own_site: false)
"Te construimos un sample site gratis": el negocio no tiene un sitio de marketing propio enlazado desde Google (su unico canal de reserva en linea es Tagvenue, una plataforma de terceros), asi que el angulo es mostrarles una muestra ya lista con sus fotos reales, su direccion, su telefono y su tarifa publica de $100/hora.

## Fuentes revisadas para email y redes (Fase 1, puntos 2 y 7)
- Ficha de Google Maps (gmaps_detail.js): campo website = null, boton "Add website" (no "Website"), sin email publico.
- Boton "Book online" de la ficha: extraido su href real con un script de Playwright (click + popup) -> apunta a tagvenue.com (plataforma de terceros, no cuenta como sitio propio).
- Listado de Tagvenue: solo expone un boton "Message host" dentro de la plataforma (host "Stanley Etienne"), sin email ni telefono alternativo.
- trillionstudios.com: responde 200 y usa la marca "TRILLION STUDIOS", pero es un portal de login para fotografos-vendedores ("Photographer Portal | Multi-Vendor Login"); su unica pagina de contenido real (/contact) muestra una direccion y telefono de plantilla en India (123 Creative Avenue, Chennai, Tamil Nadu), claramente no relacionados con el negocio real de Miami. El email que ahi aparece (support@trillionstudios.com) NO se uso por venir de una pagina que se determino como plantilla/producto de software, no el canal real del negocio.
- trillionstudiosmiami.com: no resuelve (conexion fallida).
- Instagram: instagram.com/trillionstudiosmiami/ e instagram.com/trillionstudios/ devolvieron HTTP 429 (limite de 2 intentos alcanzado). WebSearch no encontro ningun perfil de Instagram o Facebook propio.

Conclusion: email = null, canal de contacto = telefono o reserva en Tagvenue. Registrar como `pending_manual`.

## Borrador de email (ingles, idioma principal del negocio)

```
Subject: A sample website for TRILLION STUDIOS (North Miami Beach)

Hi TRILLION STUDIOS team,

My name is Michael Vargas, from Merktop. I came across TRILLION STUDIOS while looking at photo and video studios in North Miami Beach, and saw you're at 4.5 stars with 16 reviews on Google, with reviewers mentioning the space is a great fit for shoots and friendly to work with.

I noticed Google doesn't have a dedicated marketing website linked to your listing (just the Google Business page and the Tagvenue booking listing), so I put together a free sample site using your real photos, your public $100/hour rate from Tagvenue, and your contact details:

https://siteforge-demos.odd-forest-9504.workers.dev/trillion-studios-north-miami/

This does not touch your current booking flow on Tagvenue, your Google listing, or anything you already have running. It's just a preview of what a dedicated website could look like for TRILLION STUDIOS.

If you like it, we can put it on your own domain and handle all the technical setup. If it's not useful, just reply "no" and we won't follow up.

Best,
Michael Vargas
Merktop
```

## dm_message (version corta, maximo 450 caracteres, ingles, sin em-dash)

```
Hi TRILLION STUDIOS, I'm Michael from Merktop. Found you on Google (4.5 stars, 16 reviews) and saw you don't have a dedicated website linked, just the Tagvenue booking page. I built a free sample site with your real photos and rates: https://siteforge-demos.odd-forest-9504.workers.dev/trillion-studios-north-miami/ Does not touch your current booking at all. Happy to put it on your own domain, or remove it, no obligation either way.
```

(Conteo de caracteres: 398, dentro del limite de 450.)

## Notas de idioma
Idioma principal del site: ingles (todas las resenas con texto disponible, la ficha de Tagvenue y el mercado de renta de estudios de produccion en North Miami Beach son predominantemente angloparlantes). El bilingue EN/ES esta incluido en el demo. El email y el dm_message van en ingles por ser el idioma principal detectado.

## Pendiente
- Revisar la alerta de la resena de 1 estrella (seccion de arriba) antes de aprobar el envio del lote.
- Sin email publico verificado: el canal de contacto recomendado es llamada/mensaje al (305) 900-3231, o el boton "Message host" dentro de la ficha de Tagvenue.
- Si en el futuro se confirma un Instagram o Facebook propio del negocio, actualizar `ig` en el registro y considerar DM como canal adicional.
