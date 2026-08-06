# Outreach Draft: JJ Elite Auto Detailing (jj-elite-auto-detailing-kissimmee)

Status: DRAFT ONLY. Not sent. Requires explicit user approval before send, per PIPELINE.md Fase 5.

- Sender: Michael Vargas <michael@go.merktop.com> (never merktop.com directly)
- Reply-to: jose@merktop.com
- Tag: campaign=siteforge
- To: jjeliteautodetailing@gmail.com (public email, confirmed in the business's own Facebook "About" section, fetched 2026-08-06; also matches every third-party directory listing found)
- Idempotency-Key: siteforge-jj-elite-auto-detailing-kissimmee-2026-08-06
- Angle: has_own_site = false -> "les construí un website de muestra"
- Language: Spanish (site/registry language = es; the business's own Facebook description opens in Spanish "Servicio de detallados de autos..." and 2 of the 3 named Google reviews used on the site are in Spanish; Kissimmee/Osceola has a large Hispanic population, consistent with prior demos in the area)

---

**Subject:** Un sitio de muestra para JJ Elite Auto Detailing

Hola equipo de JJ Elite Auto Detailing,

Los encontré revisando detailing de autos en Kissimmee: 4.8 estrellas en Google con 20 reseñas es una marca real, y como no vi un website propio, les construí uno de muestra con sus fotos y servicios reales:

https://siteforge-demos.odd-forest-9504.workers.dev/jj-elite-auto-detailing-kissimmee/

No toca nada de cómo trabajan hoy: el botón de contacto va directo a su teléfono, (407) 837-3951, y todo el contenido sale de su propio Instagram (@jj_elite_auto_detailing_llc). Los precios no están publicados porque ustedes tampoco los publican, cada trabajo sigue cotizándose como siempre.

Si les gusta, los ayudo a ponerlo en su propio dominio. Si no, lo retiro sin compromiso, solo avísenme.

Saludos,
Michael Vargas
Merktop
https://merktop.com

---

## dm_message (para el botón DM/WhatsApp del panel, máx 450 caracteres)

Hola! Soy Michael, de Merktop. Vi que JJ Elite Auto Detailing tiene 4.8 estrellas en Google (20 reseñas) pero sin website propio, así que les construí uno de muestra con sus fotos y servicios reales: https://siteforge-demos.odd-forest-9504.workers.dev/jj-elite-auto-detailing-kissimmee/ No cambia nada de cómo trabajan hoy. Si les gusta, se lo dejamos en su propio dominio; si no, lo retiro sin problema.

(cuenta de caracteres: 404, dentro del límite de 450)

## Nota de entrega y research

- **Rating/reseñas**: 4.8 estrellas / 20 reseñas, atribuidas explícitamente a Google via desglose de Birdeye ("Google (20), Birdeye (0)"), confirmado en vivo en `https://reviews.birdeye.com/jj-elite-auto-detailing-169940407656883` (fetch 2026-08-06). Segunda fuente cruzada: agregador PreferredMechanic (`preferredmechanic.com/mobile-auto-detailing-experts/kissimmee-osceola-fl/`, leído via proxy lector) muestra 14 reseñas para el mismo negocio (conteo distinto, mismo signo positivo); se documenta la discrepancia honestamente y se usa la cifra de Birdeye (con desglose explícito por fuente) como la más confiable, igual que el precedente de formato usado en el registro.
- **Email**: `jjeliteautodetailing@gmail.com` confirmado en la sección "About" de la página de Facebook del negocio (`facebook.com/p/JJ-Elite-Auto-Detailing-Llc-100086464881715/`, fetch 2026-08-06), que también lista el mismo teléfono (407) 837-3951 y "Website: None provided".
- **Teléfono**: (407) 837-3951, confirmado en la misma página de Facebook About.
- **Dirección / tipo de local**: NO es un local visitable. Tres fuentes dan direcciones distintas para el mismo negocio: Birdeye/Google Business muestra "4126 Wellington Woods Cir, Kissimmee, FL 34741" (que corresponde a un complejo de apartamentos, la misma dirección aparece asociada a otra LLC no relacionada); el registro activo de Sunbiz (Florida Division of Corporations, documento L22000276805, EIN 92-1988608, activo desde 2022-06-17) da como dirección principal actual "553 Viceroy Ct, Kissimmee, FL 34758" (actualizada 2025-05-11); Facebook About da "Caroll, Kissimmee, FL" (calle truncada). La reseña verbatim de Giovanni LaCognata confirma el modelo: "he's honest, accommodating and comes to you". Conclusión: negocio móvil/a domicilio sin local público. Se omitió el mapa del site y se usó una foto real en su lugar; el JSON-LD y el footer solo listan ciudad/estado, sin calle, para no publicar una dirección residencial ambigua.
- **Instagram**: @jj_elite_auto_detailing_llc, 250 seguidores, 182 publicaciones (confirmado por búsqueda web 2026-08-06; el fetch directo del perfil fue bloqueado por rate limit de Instagram, 429). El servicio `ig_photos.py` (Railway) sí completó la descarga de fotos del feed sin bloqueo.
- **Fotos**: 12 descargadas del feed público de Instagram vía `scripts/ig_photos.py`, curadas visualmente (contact sheet `_sheet.jpg`): 9 utilizables (autos reales antes/después de detailing: Ferrari, GTR, camionetas, parrillas, rines), 3 descartadas por mala iluminación/encuadre (bk-4, bk-5, bk-6, casi negras o mal encuadradas). Las 9 quedaron en `output/jj-elite-auto-detailing-kissimmee/assets/raw/` y se verificaron con PIL (gate.py) que decodifican correctamente.
- **Reseñas verbatim**: 3, todas de Google (vía Birdeye, fetch directo 2026-08-06): Giovanni LaCognata (inglés, completa), Sandra Marin (español) y Javier Aponte (español/inglés mezclado). Se optó por mostrar solo estas 3 porque son las únicas con autor y texto completo verificable; hay una cuarta reseña de 1 estrella sin autor visible en la página que no se usó ni se ocultó de forma engañosa, solo no tenía texto disponible para mostrar.
- **has_own_site**: false. Verificado probando 3 dominios candidatos por DNS (`jjeliteautodetailing.com`, `jjeliteautodetailingllc.com`, `jj-elite-auto-detailing.com`: los tres devuelven `ENOTFOUND`, no existen), más el campo explícito "Website: None provided" en Facebook About y ausencia de dominio propio en Sunbiz o en resultados de búsqueda.
- **Idioma**: español, elegido por code-switching real en la descripción pública de Facebook ("Servicio de detallados de autos, ceramic coating, interior detailing, paint correction and more!") y por 2 de 3 reseñas nombradas en español.
