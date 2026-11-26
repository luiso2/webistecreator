# Outreach draft: New Beginning Plumbing Inc (Jacksonville, FL)

## Datos de contacto
- Nombre: New Beginning Plumbing Inc
- Propietario: Dwayne Curtis Littlejohn (Contratista General licencia CGC1508110 + Contratista de Plomería)
- Direccion registrada: 8802 Corporate Square Court, Jacksonville, FL 32216
- Telefono: (904) 614-8815 / +19046148815
- Instagram/Facebook: no encontrados (ver data.json, `ig_source`)
- Email: no encontrado (ver data.json, `email_notes`)
- Rating: 4.8, 25 reseñas (fuente: Thumbtack, perfil verificado con licencia)
- has_own_site: false (dominios obvios no resuelven, sin Facebook/web propia encontrada; ver `own_site_check` en data.json)
- Canal de contacto real: telefono/mensaje de texto directo, cotizacion por llamada (sin reservas online)
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/new-beginning-plumbing-jacksonville/

## Nota para revision humana
El rating/reseñas usados (4.8, 25 reviews) provienen de Thumbtack, no de una lectura directa de Google Maps: las herramientas de este entorno no lograron renderizar Google Maps (requiere JavaScript; todos los intentos via curl devolvieron paginas vacias o bloqueadas). Thumbtack fue la fuente primaria mas profunda disponible (25 reviews agregadas, 5 verbatim con nombre, licencia CGC1508110 verificada, 91 fotos de proyectos de las que se descargaron y verificaron 11). Se recomienda que una sesion con acceso a Google Maps confirme el rating de Google antes de la aprobacion final del envio, aunque los datos ya superan comodamente los minimos de config.json (rating >= 4.5, reviews >= 10).

## Angulo (has_own_site: false)
"We built you a free sample website": el negocio no tiene ningun sitio de marketing propio ni perfil de Instagram/Facebook, solo su perfil de Thumbtack (plataforma de terceros) y su registro de contratista (BuildZoom). El angulo es mostrarle un demo ya listo con sus fotos reales de proyectos terminados, sus reseñas reales y su licencia, para que tenga una pagina propia a la que dirigir a clientes que lo buscan en Google.

## Fuentes revisadas para email y redes (Fase 1, puntos 2 y 7)
- Perfil de Thumbtack (fuente primaria, scrapeado directo via curl): JSON-LD con aggregateRating 4.8/25, 5 reviews verbatim, 91 fotos de galeria (11 descargadas), credenciales de licencia verificadas 9/1/2024. No expone email publico (solo mensajeria interna de la plataforma).
- HomeGuide y BuildZoom (resultados via WebSearch; los fetches directos a ambas URLs devolvieron HTTP 403 Forbidden, asi que solo se pudo leer el fragmento indexado, no la pagina completa): confirman direccion, telefono, y licencia CGC1508110, owner Dwayne Littlejohn / "Littlejohn, Dwayne Curtis". No muestran email ni redes sociales en los fragmentos indexados.
- Busqueda especifica `site:facebook.com "New Beginning Plumbing" Jacksonville`: cero resultados de Facebook.
- Busqueda del telefono (904) 614-8815 / 9046148815 en comillas: cero resultados fuera de los directorios ya revisados (ningun sitio propio asociado a ese numero).
- Dominios probados (todos sin resolucion DNS / connect_unreachable via proxy): newbeginningplumbing.com, newbeginningplumbinginc.com, newbeginningplumbingjax.com.

Conclusion: email = null, canal de contacto = telefono. Registrar como `pending_manual`.

## Borrador de email (ingles, idioma principal del negocio)

```
Subject: A free sample website for New Beginning Plumbing (Jacksonville)

Hi Dwayne,

My name is Michael Vargas, from Merktop. I came across New Beginning Plumbing while looking at licensed plumbing and general contractors in Jacksonville, and saw your 4.8 rating across 25 reviews, with clients specifically calling out how communicative and careful you are on every job.

I noticed you don't have a dedicated website or social media page linked anywhere, just your Thumbtack profile, so I put together a free sample site using your real project photos, your real reviews, and your CGC1508110 license:

https://siteforge-demos.odd-forest-9504.workers.dev/new-beginning-plumbing-jacksonville/

This doesn't touch your Thumbtack profile, your phone number, or anything you already have running. It's just a preview of what a dedicated website could look like for New Beginning Plumbing.

If you like it, we can put it on your own domain and handle all the technical setup. If it's not useful, just reply "no" and we won't follow up.

Best,
Michael Vargas
Merktop
```

## dm_message (version corta, maximo 450 caracteres, ingles, sin em-dash)

```
Hi Dwayne, I'm Michael from Merktop. Found New Beginning Plumbing on Thumbtack (4.8 rating, 25 reviews) and noticed you don't have your own website. I built a free sample site with your real project photos, reviews and CGC1508110 license: https://siteforge-demos.odd-forest-9504.workers.dev/new-beginning-plumbing-jacksonville/ Doesn't touch anything you have running. Happy to put it on your own domain, or take it down, no pressure either way.
```

(Conteo de caracteres: 445, dentro del limite de 450.)

## Notas de idioma
Idioma principal del site: ingles (las 5 reseñas verbatim recuperadas, el texto "About" del perfil de Thumbtack, y el mercado de Jacksonville FL para contratistas son predominantemente angloparlantes). El bilingue EN/ES esta incluido en el demo (toggle ES/EN en el nav). El email y el dm_message van en ingles por ser el idioma principal detectado.

## Pendiente
- Sin email publico verificado: el canal de contacto recomendado es llamada o mensaje de texto al (904) 614-8815.
- Sin Instagram/Facebook propio confirmado: si en el futuro se encuentra uno, actualizar `ig` en el registro.
- Confirmar rating/reviews directamente en Google Maps cuando haya una sesion con esa capacidad disponible (ver nota de revision humana arriba).
