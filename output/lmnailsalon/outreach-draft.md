# Borrador de outreach: LM Nail Salon (lmnailsalon)

> Fase 5 del pipeline. Requiere aprobacion humana antes de enviarse. NO tiene email publico
> (verificado en profundidad: web_profile_info de IG, bio_links, Booksy, Facebook), asi que el
> envio real sera por WhatsApp o DM de Instagram usando el `dm_message` de abajo, no por correo.

## Contacto disponible
- Email: no publico (null). Fuentes revisadas: payload completo de Booksy (`help.us@booksy.com` es
  el soporte de Booksy, no del negocio), `web_profile_info` de Instagram (`business_email: null`,
  `business_phone_number: null`), bio_links de IG (solo WhatsApp), Facebook de Leidy Mora
  (`facebook.com/profile.php?id=100094975904817`, bloqueado a scraping sin login).
- WhatsApp real (de `external_url` -> `wa.link/fkt040` -> `wa.me`): **+1 786 865 9531**
- Instagram: **@lm.nailsalon** (5,488 seguidores)
- Booksy: https://booksy.com/en-us/1337752_lm-nailsalon_nail-salon_15643_fort-lauderdale

## Borrador de email (para cuando/si aparezca un email, o para adaptar a mensaje largo de WhatsApp)

**Para:** (sin email publico, pendiente)
**Asunto:** Un sitio de muestra para LM Nail Salon

Hola Leidy,

Te escribo porque encontre LM Nail Salon buscando nail salons en Fort Lauderdale con excelente
reputacion, y tu 5.0 perfecto en 65 resenas de Booksy realmente se destaca.

Note que tu unico enlace publico es WhatsApp, asi que te arme un sitio de muestra con tus
servicios, precios reales y fotos de tu trabajo, para que veas como se veria LM Nail Salon con
una pagina propia: https://siteforge-demos.odd-forest-9504.workers.dev/lmnailsalon/

No toca en nada tu forma de reservar citas: el boton principal sigue llevando directo a tu
WhatsApp, tal como lo tienes hoy. Es solo una muestra de diseno, sin compromiso.

Si te gusta, lo dejamos funcionando en tu propio dominio (lmnailsalon.com o el que prefieras). Si
no es para ti, lo retiramos sin problema y ninguna molestia de por medio.

Cualquier duda, con gusto la resuelvo.

Saludos,
Michael Vargas
Merktop

## dm_message (WhatsApp / Instagram DM, espanol, maximo 450 caracteres)

Hola Leidy! Soy Michael de Merktop. Vi tu 5.0 perfecto en Booksy (65 resenas) y te arme un sitio
de muestra para LM Nail Salon con tus servicios, precios y fotos reales, sin tocar tu forma de
reservar (el boton sigue yendo a tu WhatsApp): https://siteforge-demos.odd-forest-9504.workers.dev/lmnailsalon/
Si te gusta lo dejamos en tu dominio, si no lo retiramos sin problema. Que te parece?

*(longitud: 366 caracteres)*

## Notas para el envio
- `outreach: pending_manual` (sin email publico). Angulo: `has_own_site: false` -> "les construi
  un sitio de muestra".
- Enviar por WhatsApp (+1 786 865 9531) o DM de Instagram (@lm.nailsalon) tras aprobacion humana.
- Idempotency-Key sugerido si se automatiza: `siteforge-lmnailsalon-2026-07-22`.
