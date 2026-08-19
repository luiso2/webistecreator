# Outreach draft: Spiceisles Painting, Inc. (spiceislespaintingpompano)

**Angulo**: dominio propio inactivo desde 2022 (leccion "website propio roto" de
FORGE-BRIEF seccion 0.b). spiceislespainting.com SI esta registrado a nombre del negocio
(confirmado por el nombre del sitio en el HTML) pero responde con la plantilla estandar de
Webflow "churned-site": titulo "Inactive Business", texto "SpiceIslesPainting.com is no
longer active" y comentario HTML "Last Published: Thu Mar 03 2022". La ficha de Google Maps
confirma por separado que no hay website enlazado ("Add website"). El angulo NO es "no tienen
website" (seria inexacto: si tuvieron uno) sino "su sitio anterior dejo de funcionar hace
años, aqui uno nuevo real con sus fotos actuales", que suele ser mejor gancho todavia segun
el propio pipeline.
**Idioma**: ingles (nombre y ficha del negocio en ingles, perfil BBB y Facebook en ingles,
condado de Broward FL sin senal de contenido en espanol en ninguna fuente revisada; "Spice
Isles" es el apodo caribeno de Grenada y sugiere el origen del dueno, Carson Modeste, no el
idioma de operacion del negocio).
**Canal sugerido**: telefono (754) 213-7643 (unico canal de contacto publico verificado; no
se encontro email tras busqueda exhaustiva en WebSearch, BBB, Facebook y el directorio
hub.biz).

---

## Mensaje (email, pendiente de canal: no hay email publico verificado, ver notas)

Subject: Your old website (spiceislespainting.com) plus a free new sample site

Hi, this is Michael with Merktop. I came across Spiceisles Painting while looking at
top-rated painting contractors around Pompano Beach. Your 4.9 rating on Google, from 12
reviews, stood out.

I also noticed spiceislespainting.com is still registered to your business, but it has not
been active since 2022. So I put together a free sample site using your real project photos
to show what a working one could look like today:

https://siteforge-demos.odd-forest-9504.workers.dev/spiceislespaintingpompano/

This does not change anything about how you operate today. If you like it, I can move it to
your domain and set it up properly. If it is not useful, no problem at all, just let me know
and I will take it down.

Best,
Michael Vargas
Merktop

---

## dm_message (DM/WhatsApp/SMS, max 450 caracteres)

Hi! I found Spiceisles Painting on Google (4.9 rating, 12 reviews) and noticed your old site
(spiceislespainting.com) hasn't been active since 2022, so I built a free new sample site
with your real project photos: https://siteforge-demos.odd-forest-9504.workers.dev/spiceislespaintingpompano/
No strings attached, happy to put it on your domain or take it down. Michael Vargas, Merktop.

(386 caracteres)

---

## Notas de contacto

- Telefono publicado en Google Maps y coincidente con el perfil BBB: (754) 213-7643.
- Direccion verificada en dos fuentes independientes (Google Maps y BBB): 2051 NE 25th St,
  Pompano Beach, FL 33064.
- Dominio propio: spiceislespainting.com SI resuelve (HTTP 200) pero muestra la plantilla de
  "sitio inactivo" de Webflow desde marzo 2022. No se trato como descarte automatico
  ("has_own_site funcional") siguiendo la regla explicita de FORGE-BRIEF seccion 0.b para
  dominios que responden pero no cargan contenido real: el angulo de outreach se ajusto en
  consecuencia (ver arriba). Esta decision queda documentada en detalle en
  `output/spiceislespaintingpompano/data.json` (bloque `website_check`).
- No se encontro email publico tras busqueda exhaustiva: WebSearch directo, perfil de BBB
  (bbb.org, business id 90596520), pagina de Facebook (facebook.com/spiceislespainting,
  bloqueada por login de Meta) y el directorio hub.biz (spiceisles-painting.hub.biz, que solo
  trae una direccion y telefono antiguos y desactualizados en North Lauderdale, no usados en
  el site). El outreach queda `pending_manual` solo con telefono.
- Instagram: no se encontro cuenta propia verificable. El bloque social del site reutiliza el
  enlace a Google Maps (social_label "Google Maps"), igual que el patron de
  abbotttreesolutionssopchoppy; se agrego ademas el enlace de Facebook confirmado como
  `social_extra` en el footer.
- Perfil BBB: rating "F" por "failure to have a required competency license" (no accreditado).
  Este dato NO se uso en el copy del site: no se afirma "licenciado y asegurado" en ninguna
  parte, precisamente porque no se pudo verificar una licencia vigente. Se documenta aqui solo
  como contexto de research, no para el mensaje de outreach.
- Nombres del perfil BBB (President Carson Modeste, Vice President Glenton Daley) no se
  usaron en el site por no venir confirmados en la ficha de Google Maps ni en fuentes propias
  del negocio; se guardan en data.json como contexto de research unicamente.
