# Outreach draft: Sandra's Sweet & Savory LLC (sandrassweetsavory)

- **Estado**: pending_approval (NO enviar sin OK explicito del usuario)
- **Para**: sandrasweetandsavory@aol.com (email publico, confirmado de forma independiente en una foto real de su propia tarjeta de producto, ver data.json). Canal alterno: Instagram DM (@sandrasweetandsavory) o telefono (239) 331-7784.
- **De**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-sandrassweetsavory-2026-08-04
- **Angulo**: no tiene website propio (has_own_site: false) -> "le arme un sitio de muestra"
- **Idioma**: ingles (idioma principal del negocio, confirmado por su Instagram, reseñas de Google y menu en ingles)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/sandrassweetsavory/

## Cuerpo (email en ingles)

Hi Sandra,

I'm Michael, from Merktop. I found Sandra's Sweet & Savory on Google and saw your 4.9 rating across 242 reviews, people are clearly obsessed with your Key Lime Pie (the dark chocolate-dipped version keeps coming up as someone's favorite thing they've ever tasted).

I noticed you don't have your own website yet, just Instagram and your Square ordering page, so I built you a sample one with your real photos, your real menu (Key Lime Pie, Chocolate Mousse Pie, scones, oatmeal bars, coffee drinks) and your real Google reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/sandrassweetsavory/

Two important things:
- It does not touch your Square ordering page at all, that stays exactly as it is.
- It is bilingual (English and Spanish) with a small toggle in the corner.

If you like it, happy to put it on your own domain and fine-tune it together. If not, no problem at all, I will take it down, no strings attached.

Best,
Michael Vargas
Merktop · merktop.com

## Version corta para DM / WhatsApp (dm_message, 447 caracteres)

Hi Sandra! I'm Michael, from Merktop. Found Sandra's Sweet & Savory on Google: 4.9 rating, 242 reviews, people love your Key Lime Pie and the chocolate-dipped version. You don't have a website yet, so I built a sample one with your real photos, menu and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/sandrassweetsavory/ It does not touch your Square page. Like it, we put it on your domain. If not, I remove it, no strings attached.

## Nota de canal

Email publico CONFIRMADO de forma independiente (no solo por un snippet de busqueda): una foto real de su propio feed de Instagram (assets/raw/bk-5.jpg, no usada en el site final) muestra la tarjeta impresa de su producto con el texto "Email: sandrasweetandsavory@aol.com". Esto coincide con lo hallado en una busqueda web previa, asi que se trata como email publico verificado, no como null.

Canal alterno si el email rebota: Instagram DM (@sandrasweetandsavory, 1,320 seguidores, perfil publico) o llamada/WhatsApp al (239) 331-7784. No se contacto al negocio bajo ninguna circunstancia durante este research.

## Aviso para el revisor humano

- **Horario**: fuentes en conflicto. El texto del propio sitio Square dice "Wednesday-Sunday 10am-3pm, cerrado lunes y martes". Una foto real de su Instagram (decal de vidrio en su tienda, bk-9.jpg) dice "NEW Business Hours: Mon-Thu 10am-4pm, Fri-Sat 10am-5pm, Sun 10am-4pm" (abierto los 7 dias). Se uso el horario del decal por ser la fuente mas reciente y fotografiada directamente en su local, pero vale la pena confirmar por telefono antes de enviar el outreach.
- **Reseñas**: los 4 quotes verbatim veniant del brief de discovery inicial; se corroboraron tematicamente via busqueda web (frases como "chi tea latte", "dark chocolate-dipped key lime pie" aparecen en resultados de busqueda sobre este negocio) pero no se pudieron re-verificar linea por linea contra Google Maps directamente (sin acceso a Maps API en este entorno). Revisar antes de un envio masivo.
- **Precios del menu**: solo se pudo confirmar un precio real (Chocolate Mousse Pie 5" = $7.50, via snippet de busqueda citando su propio listado). El catalogo completo de Square se renderiza con JS del lado del cliente y no se pudo scrapear; el resto de items del menu se muestran sin precio ("Ask in-store") para no inventar cifras.
- **Numero de reseñas**: las fuentes espejo (Yelp, RestaurantGuru, agregadores) dieron cifras entre 239 y 262 reseñas de Google. Se uso 242 (la cifra que mas se repitio), pero confirmar en Google Maps directo si es posible.
