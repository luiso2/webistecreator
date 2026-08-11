# Outreach draft: Xanzalyn Beauty & Dermacare (Coral Springs, FL)

Demo: https://siteforge-demos.odd-forest-9504.workers.dev/xanzalyn-beauty-dermacare-coral-springs/
Angulo: no tienen website propio (has_own_site: false) -> "les hicimos un website de muestra gratis".
Idioma principal del negocio: ingles (reseñas de Booksy y bio de staff en ingles).

## Estado del contacto (importante)
No se encontro email ni telefono publico tras busqueda profunda. Este borrador de email queda
listo para el dia que aparezca un canal (o para enviar manualmente por Instagram DM/Facebook
si el usuario decide contactar). outreach = pending_manual.

## Version email (para referencia futura, aunque hoy no hay email publico)

**Para:** (sin email publico verificado, dejar en blanco hasta encontrarlo)
**De:** Michael Vargas <michael@go.merktop.com>
**Reply-To:** jose@merktop.com
**Asunto:** A free sample website for Xanzalyn Beauty & Dermacare

Hi there,

I came across Xanzalyn Beauty & Dermacare on Booksy while looking at lash and skin studios in
Coral Springs, and the 5.0 rating across 47 reviews caught my eye.

I noticed you do not have your own website yet, so I put together a free sample site for you,
built around your real menu, reviews and photos:

https://siteforge-demos.odd-forest-9504.workers.dev/xanzalyn-beauty-dermacare-coral-springs/

It does not touch your Booksy booking at all, clients would still book exactly the way they do
today. If you like it, I am happy to hand it over on your own domain at no cost to look at it.
If it is not for you, no worries at all, just wanted to share it.

Best,
Michael Vargas
Merktop

## Version dm_message (Instagram DM / WhatsApp, ingles, 426 caracteres)

Hi! I found Xanzalyn Beauty & Dermacare on Booksy, love the 5.0 rating across 47 reviews. Noticed you do not have your own website yet, so I put together a free sample site for you: https://siteforge-demos.odd-forest-9504.workers.dev/xanzalyn-beauty-dermacare-coral-springs/ It does not touch your Booksy booking at all. Happy to hand it over on your own domain if you like it, no strings attached, or just ignore this if not.

## Notas de investigacion de contacto (canales revisados, ninguno publico un email o telefono)

- Booksy (booksy_dossier.py): JSON-LD del negocio sin campo telephone; sin website_candidates.
- Busqueda web dirigida ("Xanzalyn Beauty Dermacare Coral Springs phone/email", linktree/beacons):
  sin resultados con telefono o email.
- Facebook (facebook.com/people/Xanzalyn-Beauty-Dermacare/61556184945672): WebFetch devolvio
  solo nombre/ciudad la primera vez y bloqueo de navegador la segunda (About no accesible sin
  login). 2 intentos, sin exito.
- Instagram @browardlashes_facials y @xanzalyn (perfil alterno encontrado en la busqueda):
  scrape con Playwright (chrome fijo, flags anti-QUIC) devolvio muro de login en ambos intentos,
  no se pudo leer la bio ni el external_url. 2 intentos, sin exito.
- TikTok @xanzalyn_beautydermacare: pagina no renderizo contenido util via fetch simple.
- Direccion fisica SI verificada: 9399 W Atlantic Blvd, Suite 26, Coral Springs, FL 33071
  (coincide en Booksy y en resultados de busqueda independientes).
- Conclusion: research_degradado en el canal IG/Facebook por bloqueo de login, NO evidencia de
  que el negocio oculte el dato a proposito. email y phone quedan null, sin inventar. Si una
  sesion futura tiene acceso a Instagram con sesion iniciada o Playwright con IP residencial,
  vale la pena reintentar antes de descartar definitivamente.

## Website propio: confirmado que NO existe
xanzalynbeauty.com y xanzalyndermacare.com no resuelven (fallo de conexion consistente con
dominio inexistente, verificado via proxy). Sin sameAs a dominio propio en Booksy. has_own_site: false.
