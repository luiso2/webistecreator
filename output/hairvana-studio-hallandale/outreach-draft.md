# Outreach draft - Hairvana Studio (hairvana-studio-hallandale)

## Datos de contacto
- Negocio: Hairvana Studio (tambien conocido como Hairvana Beauty Studio)
- Estilista principal / dueña: Julissa Tejeda (Dominicana, mas de 30 años de experiencia), junto a Marisol y Johana
- Direccion: 960 W Hallandale Beach Blvd, Hallandale Beach, FL 33009
- Telefono: (954) 991-9976 (confirmado en el brief y verificado de forma independiente via Fresha)
- Booksy (reservas reales, venue 1169821): https://booksy.com/en-us/1169821_hairvana-studio_hair-salon_119743_hallandale-beach
- Instagram: @hairvanastudio (https://www.instagram.com/hairvanastudio/), ~1354 seguidores
- Email publico: NO ENCONTRADO tras busqueda profunda (ver notas en data.json: IG bloqueado 401 en 2 intentos, sin campo email en el payload de Booksy, sin Facebook encontrado, sin dominio propio del que derivar email)
- Idioma principal: en (9 de 10 reseñas completas en ingles, descripcion propia del negocio en ingles)
- Rating: 5.0 sobre 5 · 11 reseñas en Booksy (verificado via payload propio de Booksy). Yelp muestra 14 reseñas como referencia secundaria. La ficha de Google no se pudo verificar de forma independiente en este entorno (Google Maps y Yelp bloquearon el acceso directo con HTTP 403); no se uso ningun numero de "Google reviews" sin poder confirmarlo contra la ficha oficial.
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/hairvana-studio-hallandale/
- has_own_site: false (hairvanastudio.com y www.hairvanastudio.com devuelven HTTP 404, confirmado con curl directo; sin ningun otro dominio propio encontrado)

## Estado de outreach
`outreach: pending_manual`: no hay email publico verificado. Canal recomendado: DM de Instagram (@hairvanastudio) o mensaje directo via Booksy/telefono. El borrador de email queda listo mas abajo por si en el futuro se confirma un email.

---

## Borrador de email (para cuando/si haya email; idioma principal: en)

**To:** (sin confirmar)
**From:** Michael Vargas <michael@go.merktop.com>
**Reply-To:** jose@merktop.com
**Subject:** A free sample website for Hairvana Studio

Hi Julissa,

I came across Hairvana Studio on Booksy and had to reach out. A 5.0 rating across 11 reviews is great, and clients keep raving about the team, one review even said "the team is fun and attentive" and another that the stylists "are so professional and ethical."

I noticed the salon does not have its own website yet (hairvanastudio.com currently shows nothing), so I put together a free sample site using your real photos, services and reviews. You can see it here:

https://siteforge-demos.odd-forest-9504.workers.dev/hairvana-studio-hallandale/

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

Hi! Found Hairvana Studio on Booksy, 5.0 across 11 reviews, love the color and cut work from Julissa and the team. Since you do not have your own website yet, I built a free sample site with your real photos, services and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/hairvana-studio-hallandale/ It does not touch your Booksy setup. Happy to put it on your own domain or take it down, zero obligation. Michael Vargas, Merktop.

(441 caracteres)

---

## Notas para revision humana
- Rating mostrado en el site: 5.0 / 11 reseñas de Booksy, verificado programaticamente contra el payload __NUXT_DATA__ del venue 1169821 (no scraping visual, sino parseo del JSON estructurado). Yelp muestra 14 reseñas (title tag de la pagina, obtenido via WebSearch ya que el fetch directo dio HTTP 403) y se usa solo como referencia secundaria en el research, no en el site.
- Google Maps: se intento reiteradamente acceder a la ficha de Google (WebFetch a google.com/search y a Google Maps, ademas de curl directo a Yelp) y todos los intentos devolvieron HTTP 403 o paginas sin datos reales (shell de SPA sin contenido). No se pudo confirmar de forma independiente el rating/reseñas de Google en este entorno. Un resumen de un motor de busqueda menciono "4.4 de 5 con 25 reseñas" pero es una cifra de fuente ambigua (posible agregado multi-plataforma de un directorio tipo wheree.com) y no se uso por no poder verificarse contra la ficha oficial.
- Menu de servicios: los 23 servicios con precios y duraciones EXACTOS se extrajeron programaticamente del payload __NUXT_DATA__ de Booksy (formato devalue de Nuxt), resolviendo cada objeto de servicio y sus variantes. Esto es mas confiable que una lectura visual de la pagina.
- Fotos: Instagram bloqueo el endpoint web_profile_info en los 2 intentos permitidos por el pipeline (HTTP 401 "please wait a few minutes"). Se uso como fuente alternativa el propio payload de Booksy, que expone fotos reales de cada servicio (service_photos) ademas de la foto de portada del negocio y el logo. Se descargaron 29 fotos candidatas, se inspeccionaron una por una y se seleccionaron 8 para el site (1 hero, 2 de "nuestra historia", 5 de galeria) descartando collages con logo superpuesto, selfies con sonrisa a camara, tomas de proceso con la mano del estilista o texto ("Crop") superpuesto, fotos de producto de marca (Redken, Olaplex) y una infografia de precios de extensiones que no era una foto real de cliente.
- Equipo: no se encontraron fotos verificables de Julissa, Marisol o Johana especificamente identificadas como ellas (las fotos disponibles son de clientas, no del staff), asi que la seccion "El equipo" usa iniciales en un badge circular en vez de fotos, para no atribuir por error el rostro de una clienta a una estilista.
- Email: no se encontro ninguno tras busqueda profunda en todas las fuentes indicadas por el pipeline (ver data.json). Outreach queda en pending_manual, recomendando contacto por Instagram DM o telefono/Booksy.
- Direccion y telefono coinciden entre el brief original, el payload de Booksy y el fetch directo a Fresha, sin discrepancias.
- Horario: se uso el de Fresha (fetch directo, HTTP 200) por ser una ficha estructurada real; un resumen de busqueda anterior sugeria horas ligeramente distintas (posible ficha de Google desactualizada o de un directorio agregador), documentado en data.json.
