# Outreach draft: Oliva Auto Tech / Mecánico a Domicilio (Hialeah / Miami-Dade, FL)

## Datos de contacto
- Nombre: Oliva Auto Tech (listado en Google como "Mecanico a domicilio .Oliva auto tech inc.")
- Dirección: ninguna (negocio 100% móvil, sin tienda fija). Zona de servicio confirmada en su Google Business Profile: Hialeah, Miami, Medley, Kendall, Miramar, West Miami, Miami Beach, South Miami, Coral Gables, Miami Springs.
- Teléfono: (786) 277-2886 / +17862772886
- Instagram / Facebook: no encontrado (ver data.json, `ig_source`)
- Email: no encontrado (ver data.json, `email_notes`)
- Rating: 5.0 en Google, 150 reseñas (listado VERIFICADO por el dueño)
- has_own_site: false (ver `own_site_check` en data.json: se descartó un dominio similar, mecanicoadomiciliomiami.com, por pertenecer a OTRO negocio con teléfono distinto)
- Canal real de contacto: llamada o SMS directo al (786) 277-2886
- Demo: https://siteforge-demos.odd-forest-9504.workers.dev/oliva-auto-tech-hialeah/

## Ángulo (has_own_site: false)
"Te construimos un sample site gratis": el negocio no tiene ningún sitio de marketing propio, solo su ficha de Google (verificada) con 150 reseñas excelentes. El ángulo es mostrarles una muestra ya lista con sus fotos reales de trabajos a domicilio, sus reseñas reales y su teléfono, sin tocar nada de lo que ya tienen funcionando.

## Fuentes revisadas para email y redes (Fase 1, puntos 2 y 7)
- Google Business Profile verificado (business.google.com/v/mecanico-a-domicilio-oliva-auto-tech-inc/06354463599312181789/ce2a/_): sin campo de website, sin email, solo botón de llamada y "Contact us".
- Se probaron los dominios obvios olivaautotech.com, oliva-autotech.com y olivaautotechinc.com: ninguno resuelve (sin DNS).
- mecanicoadomicilio.com: redirige a una página de reventa de dominios (HugeDomains), sin relación con el negocio.
- mecanicoadomiciliomiami.com: sí existe y es un mecánico móvil real, pero es un NEGOCIO DISTINTO (teléfono (786) 998-1315, sin mención de "Oliva", base declarada en Miramar/Miami Gardens). Se descartó explícitamente como el mismo negocio antes de concluir "sin sitio propio".
- WebSearch del teléfono exacto "786-277-2886" no devolvió ningún sitio propio ni directorio adicional.
- No se encontró perfil de Instagram ni Facebook propio tras varias búsquedas con el nombre del negocio.

Conclusión: email = null, canal de contacto = teléfono o SMS directo. Registrar como `pending_manual`.

## Borrador de email (español, idioma principal del negocio)

```
Asunto: Un sitio web de muestra para Oliva Auto Tech

Hola equipo de Oliva Auto Tech,

Soy Michael Vargas, de Merktop. Los encontré buscando mecánicos a domicilio en Hialeah y Miami-Dade, y vi que tienen 5.0 estrellas con 150 reseñas en Google, con clientes que llevan hasta 20 años confiando en el servicio.

Noté que no tienen una página web propia (solo su ficha de Google), así que les armé un sitio de muestra gratis usando sus fotos reales de trabajos a domicilio y sus reseñas reales de Google:

https://siteforge-demos.odd-forest-9504.workers.dev/oliva-auto-tech-hialeah/

Esto no cambia en nada cómo trabajan hoy ni su ficha de Google. Es solo una muestra de cómo se vería un sitio propio para Oliva Auto Tech.

Si les gusta, se lo dejamos en su propio dominio sin costo adicional. Si no les sirve, simplemente respondan "no" y no los vuelvo a contactar.

Saludos,
Michael Vargas
Merktop
```

## dm_message (versión corta, máximo 450 caracteres, español, sin em-dash)

```
Hola! Soy Michael, de Merktop. Vi a Oliva Auto Tech en Google (5.0 estrellas, 150 reseñas) como mecanico a domicilio en Hialeah y Miami-Dade, y como no tienen pagina web propia les arme un demo gratis con sus fotos y reseñas reales: https://siteforge-demos.odd-forest-9504.workers.dev/oliva-auto-tech-hialeah/ No cambia como trabajan hoy. Si les gusta se los dejamos en su propio dominio, o lo bajamos sin compromiso.
```

(Conteo de caracteres: 417, dentro del límite de 450.)

## Notas de idioma
Idioma principal del site: español (el propio negocio eligió publicar su nombre en español en Google, "Mecánico a domicilio", apuntando directamente al mercado hispanohablante de Hialeah/Miami-Dade; las reseñas con texto están en inglés, pero el bilingüe ES/EN está incluido en el demo con español por defecto). El email y el dm_message van en español por ser el idioma principal detectado.

## Pendiente / notas para revisión humana
- Sin email público ni Instagram/Facebook propio confirmado: el único canal de contacto es llamada o SMS al (786) 277-2886.
- No se encontró WhatsApp Business confirmado para este número: el CTA del demo usa llamada/SMS en vez de wa.me para no asumir un canal no verificado. Si el equipo de Merktop confirma que el número sí tiene WhatsApp, se puede actualizar el CTA antes de desplegar.
- Negocio 100% móvil sin tienda fija: la sección de ubicación del demo usa una foto real de un trabajo a domicilio en vez de un mapa embebido de Google, siguiendo la variante adaptada de PIPELINE.md para negocios sin dirección pública exacta.
- Una reseña (autor "SERO1969") menciona por nombre a "Oscar" como el mecánico; no se usó ese nombre en el copy del site por no poder confirmarlo como el nombre oficial/público del dueño, pero puede ser útil para personalizar el saludo si el equipo humano lo confirma antes de enviar.
