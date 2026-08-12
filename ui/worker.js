const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8' },
  });

// Quita angle brackets y caracteres de control de texto que entra por endpoints publicos,
// como defensa en profundidad contra inyeccion (el front igual escapa todo al renderizar).
const stripUnsafe = s => String(s).replace(/[<>\x00-\x1F\x7F]/g, "");

// SHA-256 del access key (el key real vive solo en el .env local del usuario)
const KEY_HASH = 'b1e35fb9b55f29a4272b16173553f5f92b19b0b824ddb3d9789f28332bd4bf06';

async function isAuthorized(req) {
  const key = req.headers.get('x-sf-key') || '';
  if (!key) return false;
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(key));
  const hex = [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
  return hex === KEY_HASH;
}

// Solo se aceptan URLs de demo dentro de la cuenta Cloudflare del usuario
const DEMO_URL_RE = /^https:\/\/[a-z0-9-]+\.odd-forest-9504\.workers\.dev(\/[a-z0-9-]*\/?)?$/;

// Resuelve el token de Registrar aunque el nombre de la variable venga con espacios o una
// coma al final (typo comun al pegar el nombre en el dashboard de Cloudflare).
function cfRegistrarToken(env) {
  if (env.CF_REGISTRAR_TOKEN) return env.CF_REGISTRAR_TOKEN;
  for (const [k, v] of Object.entries(env)) {
    if (typeof v === 'string' && k.replace(/[\s,]+$/g, '') === 'CF_REGISTRAR_TOKEN') return v;
  }
  return null;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);

    // Endpoints publicos autorizados por el usuario (2026-07-16): permiten que la
    // rutina cloud procese la cola sin guardar credenciales. Solo exponen metadata
    // de la cola; agregar items y escribir el registro siguen requiriendo la key.
    if (url.pathname === '/api/public/queue' && req.method === 'GET') {
      const queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
      const STALE_MS = 90 * 60 * 1000; // procesando sin avance por 90 min = huerfano, vuelve a la cola
      const now = Date.now();
      const pending = queue
        .filter(q => q.status === 'pending' || (q.status === 'processing' && now - Date.parse(q.stage_at || q.created) > STALE_MS))
        .map(({ id, input, created }) => ({ id, input, created }));
      return json({ pending });
    }

    if (url.pathname === '/api/public/queue/progress' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      const STAGES = ['research', 'build', 'verify', 'commit'];
      if (!body.id || !STAGES.includes(body.stage)) return json({ error: 'id y stage validos requeridos' }, 400);
      let queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
      const item = queue.find(q => q.id === body.id && (q.status === 'pending' || q.status === 'processing'));
      if (!item) return json({ error: 'item no activo' }, 404);
      const now = new Date().toISOString();
      queue = queue.map(q => (q.id === body.id ? {
        ...q,
        status: 'processing',
        stage: body.stage,
        stage_at: now,
        started_at: q.started_at || now,
        note: typeof body.note === 'string' ? body.note.slice(0, 140) : q.note,
      } : q));
      await env.SITEFORGE_KV.put('queue', JSON.stringify(queue));
      return json({ ok: true });
    }

    if (url.pathname === '/api/public/queue/done' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      if (!body.id) return json({ error: 'id requerido' }, 400);
      const result = {};
      if (typeof body.slug === 'string' && /^[a-z0-9-]{1,40}$/.test(body.slug)) result.slug = body.slug;
      if (typeof body.name === 'string' && body.name.length <= 120) result.name = stripUnsafe(body.name);
      if (typeof body.url_demo === 'string' && DEMO_URL_RE.test(body.url_demo)) result.url_demo = body.url_demo;
      if (typeof body.dm === 'string' && body.dm.length <= 500) result.dm = stripUnsafe(body.dm);
      if (body.failed === true) {
        result.failed = true;
        if (typeof body.motivo === 'string') result.motivo = stripUnsafe(body.motivo.slice(0, 240));
      }
      let queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
      const exists = queue.some(q => q.id === body.id && (q.status === 'pending' || q.status === 'processing'));
      if (!exists) return json({ error: 'item no pendiente' }, 404);
      queue = queue.map(q => (q.id === body.id ? { ...q, status: 'done', done_at: new Date().toISOString(), result } : q));
      await env.SITEFORGE_KV.put('queue', JSON.stringify(queue));
      return json({ ok: true });
    }

    // Upsert publico de UN negocio al registro del panel (autorizado por el usuario 2026-07-19).
    // Permite que las corridas cloud reflejen sus demos sin credenciales. Defensas:
    // solo url_demo del dominio de demos, campos con tope, NUNCA pisa outreach 'sent',
    // y nunca borra: solo agrega o actualiza el slug que registra.
    if (url.pathname === '/api/public/registry-upsert' && req.method === 'POST') {
      let body;
      try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
      const slug = (body.slug || '').toString();
      if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
      if (typeof body.url_demo !== 'string' || !DEMO_URL_RE.test(body.url_demo)) return json({ error: 'url_demo invalida' }, 400);
      // Nota: no se verifica el demo con fetch aqui. Un Worker no puede hacer fetch fiable a
      // otro Worker de la MISMA cuenta workers.dev (da 404 aunque el demo este live), y el repo
      // es privado (raw github 404 sin token). La prevencion de tarjetas fantasma vive en la
      // forja (verifica 200 antes de upsert, ver FORGE-BRIEF) y en el chequeo client-side del panel.
      const S = (v, max) => (typeof v === 'string' ? stripUnsafe(v.slice(0, max)) : undefined);
      const limpio = {
        slug,
        name: S(body.name, 120) || slug,
        city: S(body.city, 80),
        ig: S(body.ig, 60),
        url_demo: body.url_demo,
        has_own_site: body.has_own_site === true,
        // undefined (no null): un upsert que viene sin email NO debe borrar el email que ya
        // se habia encontrado para ese negocio (el filtro de abajo descarta solo undefined).
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email || '') ? S(body.email, 120) : undefined,
        phone: S(body.phone, 30),
        outreach: 'pending_manual',
        status: 'staging',
        language: body.language === 'en' ? 'en' : 'es',
        dm_message: S(body.dm_message, 500),
        thumb: typeof body.thumb === 'string' && body.thumb.startsWith('https://') && body.thumb.includes('.odd-forest-9504.workers.dev') ? S(body.thumb, 300) : undefined,
        fecha: S(body.fecha, 12) || new Date().toISOString().slice(0, 10),
      };
      const registry = (await env.SITEFORGE_KV.get('registry', 'json')) || [];
      const idx = registry.findIndex(b => b.slug === slug);
      if (idx >= 0) {
        const actual = registry[idx];
        if (actual.outreach === 'sent') return json({ ok: true, skipped: 'ya contactado' });
        if (actual.outreach === 'skip_duplicate') return json({ ok: true, skipped: 'marcado como duplicado' });
        const nuevo = Object.fromEntries(Object.entries(limpio).filter(([, v]) => v !== undefined));
        // Un re-upsert refresca los datos del demo, pero NUNCA revierte el estado de outreach
        // que el panel ya haya avanzado (si no, una corrida cloud lo devolveria a contactable).
        delete nuevo.outreach;
        registry[idx] = { ...actual, ...nuevo };
      } else {
        if (registry.length >= 800) return json({ error: 'registro lleno' }, 429);
        registry.push(Object.fromEntries(Object.entries(limpio).filter(([, v]) => v !== undefined)));
      }
      await env.SITEFORGE_KV.put('registry', JSON.stringify(registry));
      return json({ ok: true, count: registry.length });
    }

    if (url.pathname.startsWith('/api/')) {
      if (!(await isAuthorized(req))) return json({ error: 'unauthorized' }, 401);

      if (url.pathname === '/api/state' && req.method === 'GET') {
        const [registry, queue, crm, colores, mensajes] = await Promise.all([
          env.SITEFORGE_KV.get('registry', 'json'),
          env.SITEFORGE_KV.get('queue', 'json'),
          env.SITEFORGE_KV.get('crm', 'json'),
          // Colores personalizados: se listan las llaves y se leen solo las que existen, para
          // que el panel marque el color activo de cada sitio sin una lectura por negocio.
          env.SITEFORGE_KV.list({ prefix: 'color:' })
            .then(l => Promise.all(l.keys.map(k =>
              env.SITEFORGE_KV.get(k.name, 'json').then(v => [k.name.slice(6), v]))))
            .then(pares => Object.fromEntries(pares.filter(([, v]) => v)))
            .catch(() => ({})),
          // Mensajes editados a mano, igual que los colores: una lista y luego solo los que hay.
          env.SITEFORGE_KV.list({ prefix: 'msg:' })
            .then(l => Promise.all(l.keys.map(k =>
              env.SITEFORGE_KV.get(k.name).then(v => [k.name.slice(4), v]))))
            .then(pares => Object.fromEntries(pares.filter(([, v]) => v)))
            .catch(() => ({})),
        ]);
        // El CRM (cliente cerrado / descartado) vive en su propia llave: ninguna
        // sincronizacion del registro desde el repo o la forja lo puede pisar.
        const map = crm || {};
        const reg = (registry || []).map(b => (map[b.slug]
          ? {
              ...b,
              crm_status: map[b.slug].status,
              crm_at: map[b.slug].at,
              contacted_at: map[b.slug].contacted_at || null,
              contacted_via: map[b.slug].via || null,
            }
          : b))
          .map(b => (colores[b.slug] ? { ...b, color: colores[b.slug] } : b))
          .map(b => (mensajes[b.slug] ? { ...b, msg_editado: mensajes[b.slug] } : b));
        return json({ registry: reg, queue: queue || [] });
      }

      // CRM: marcar un negocio como cliente cerrado / descartado / reabrir.
      // Accion directa del usuario autenticado; reversible; sin efectos externos.
      if (url.pathname === '/api/mark' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        const status = body.status;
        // 'contacted' = ya le escribi o lo llame, para no repetir el contacto. Es distinto de
        // 'client' (cerro) y de 'declined' (dijo que no): es el paso intermedio que faltaba.
        if (!['client', 'declined', 'contacted', 'pending'].includes(status)) return json({ error: 'status invalido' }, 400);
        const crm = (await env.SITEFORGE_KV.get('crm', 'json')) || {};
        if (status === 'pending') {
          delete crm[slug];
        } else {
          const via = ['llamada', 'whatsapp', 'dm', 'email', 'visita'].includes(body.via) ? body.via : null;
          crm[slug] = {
            status,
            at: new Date().toISOString(),
            ...(via ? { via } : {}),
            // conservar cuando se contacto por primera vez aunque luego cierre o descarte
            ...(crm[slug] && crm[slug].contacted_at ? { contacted_at: crm[slug].contacted_at }
                : (status === 'contacted' ? { contacted_at: new Date().toISOString() } : {})),
          };
        }
        await env.SITEFORGE_KV.put('crm', JSON.stringify(crm));
        const vals = Object.values(crm);
        return json({
          ok: true, slug, status,
          clientes: vals.filter(c => c.status === 'client').length,
          contactados: vals.filter(c => c.status === 'contacted').length,
        });
      }

      // Color del sitio: se guarda en el MISMO KV que lee el worker de demos, que lo inyecta
      // como <style> al servir. Por eso el cambio se ve al instante y no hace falta
      // reconstruir el sitio ni redeployar. Enviar sin `palette` lo devuelve a su color original.
      if (url.pathname === '/api/color' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        if (!body.palette) {
          await env.SITEFORGE_KV.delete('color:' + slug);
          return json({ ok: true, slug, palette: null });
        }
        // Mismo filtro que aplica el worker de demos: estos valores acaban dentro de un
        // <style>, asi que solo pasan formas de color conocidas.
        const OK = /^(#[0-9a-f]{3,8}|rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(?:,\s*(?:0|1|0?\.\d+)\s*)?\))$/i;
        const limpia = {};
        for (const t of ['deep', 'mid', 'soft', 'ghost']) {
          const v = (body.palette[t] || '').toString().trim();
          if (!OK.test(v)) return json({ error: `color invalido en "${t}"`, valor: v.slice(0, 40) }, 400);
          limpia[t] = v;
        }
        if (typeof body.nombre === 'string') limpia.nombre = stripUnsafe(body.nombre.slice(0, 40));
        await env.SITEFORGE_KV.put('color:' + slug, JSON.stringify(limpia));
        return json({ ok: true, slug, palette: limpia });
      }

      // Mensaje de outreach editado a mano para un negocio. Se guarda para que el texto que
      // se ajusto no se pierda al recargar el panel ni al cambiar de dispositivo: el DM de
      // Instagram hay que pegarlo a mano, asi que conviene tenerlo tal cual se dejo.
      if (url.pathname === '/api/mensaje' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        if (typeof body.texto !== 'string' || !body.texto.trim()) {
          await env.SITEFORGE_KV.delete('msg:' + slug);
          return json({ ok: true, slug, texto: null });
        }
        // Tope generoso: un DM largo cabe de sobra y evita que una escritura rara llene el KV.
        const texto = body.texto.slice(0, 1200);
        await env.SITEFORGE_KV.put('msg:' + slug, texto);
        return json({ ok: true, slug, largo: texto.length });
      }

      if (url.pathname === '/api/queue' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const input = (body.input || '').toString().trim();
        if (!input || input.length > 200) return json({ error: 'input requerido (max 200 chars)' }, 400);
        const queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
        if (queue.filter(q => q.status === 'pending').length >= 20) {
          return json({ error: 'cola llena (20 pendientes max)' }, 429);
        }
        const item = { id: crypto.randomUUID(), input, status: 'pending', created: new Date().toISOString() };
        queue.push(item);
        await env.SITEFORGE_KV.put('queue', JSON.stringify(queue));
        return json({ ok: true, item });
      }

      if (url.pathname === '/api/queue/done' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        // Sin este guard, un body sin id recorre la cola comparando contra undefined y responde
        // ok:true sin haber cerrado nada (falso positivo para el que llama).
        if (!body.id) return json({ error: 'id requerido' }, 400);
        let queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
        if (!queue.some(q => q.id === body.id)) return json({ error: 'item no encontrado' }, 404);
        queue = queue.map(q => (q.id === body.id ? { ...q, status: 'done', done_at: new Date().toISOString() } : q));
        await env.SITEFORGE_KV.put('queue', JSON.stringify(queue));
        return json({ ok: true });
      }

      // Envio de outreach POR ACCION DIRECTA del usuario autenticado en el panel
      // (cada envio = un click + confirmacion del dueno del panel; nunca automatico).
      if (url.pathname === '/api/send' && req.method === 'POST') {
        if (!env.RESEND_API_KEY) return json({ error: 'RESEND_API_KEY no configurada en el worker' }, 500);
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        const registry = (await env.SITEFORGE_KV.get('registry', 'json')) || [];
        const biz = registry.find(b => b.slug === slug);
        if (!biz) return json({ error: 'negocio no encontrado' }, 404);
        if (!biz.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(biz.email)) return json({ error: 'sin email publico valido' }, 400);
        if (!biz.url_demo || !DEMO_URL_RE.test(biz.url_demo)) return json({ error: 'url_demo invalida' }, 400);
        // Anti-duplicado: registry (sincronizado desde el repo) + log propio del panel.
        // El slug NO identifica al negocio: una segunda corrida puede derivar otro slug para el
        // mismo negocio (caso real 305esthetics / threezerofiveesthetics, mismo IG y email), y un
        // dedup solo por slug deja pasar un segundo email al mismo dueno (rompe la regla dura #3).
        // Por eso la identidad se chequea tambien por email y por handle de IG.
        const sentLog = (await env.SITEFORGE_KV.get('sent_log', 'json')) || {};
        if (biz.outreach === 'sent' || sentLog[slug]) {
          return json({ error: 'ya se le envio email a este negocio', sent_at: sentLog[slug] || biz.fecha }, 409);
        }
        if (biz.outreach === 'skip_duplicate') {
          return json({ error: 'este registro esta marcado como duplicado', duplicate_of: biz.duplicate_of || null }, 409);
        }
        const norm = v => (v || '').toString().trim().toLowerCase().replace(/^@/, '');
        const gemelo = registry.find(b => b.slug !== slug
          && (b.outreach === 'sent' || sentLog[b.slug])
          && ((biz.email && norm(b.email) === norm(biz.email)) || (biz.ig && norm(b.ig) === norm(biz.ig))));
        if (gemelo) {
          return json({
            error: 'ya se le envio email a este negocio bajo otro slug (mismo email o IG)',
            slug_contactado: gemelo.slug, sent_at: sentLog[gemelo.slug] || gemelo.fecha,
          }, 409);
        }

        const en = (biz.language || 'es') === 'en';
        const redesign = !!biz.has_own_site;
        // El asunto decide si se abre: va el nombre del negocio y un hecho concreto, no una
        // etiqueta de producto. "de muestra" se cayo a proposito: lee como plantilla o
        // borrador, y lo que se construyo lleva SUS fotos y SUS servicios.
        const subject = en
          ? (redesign ? `${biz.name}: a new version of your website` : `${biz.name}: your website is ready to look at`)
          : (redesign ? `${biz.name}: una version nueva de su pagina` : `${biz.name}: su website ya esta listo para verlo`);
        // Cierra en PREGUNTA: sin ella nada obliga a contestar. Y dice explicitamente que
        // verlo no cuesta, que es el freno que hace que no respondan.
        const lines = en
          ? [
              `Hi ${biz.name} team!`,
              redesign
                ? `I'm Michael, from Merktop (Miami). I found you on Google and rebuilt your site using your own photos, services and reviews, so the people who land on it actually book:`
                : `I'm Michael, from Merktop (Miami). I found you on Google, saw you didn't have your own website, and built you one with your real photos, services and reviews, so the people searching for you can find you and book:`,
              biz.url_demo,
              `It's already built and it costs you nothing to look at. It doesn't touch your booking flow at all, and if you don't like it I take it down today.`,
              en && redesign ? `Want me to walk you through it?` : `Want me to leave it up?`,
              `Michael Vargas\nMerktop · https://merktop.com`,
            ]
          : [
              `Hola equipo ${biz.name}!`,
              redesign
                ? `Soy Michael, de Merktop (Miami). Los encontre en Google y rearme su pagina con sus propias fotos, servicios y reseñas, para que quien llegue termine reservando:`
                : `Soy Michael, de Merktop (Miami). Los encontre en Google, vi que no tenian website propio y les arme uno con sus fotos, servicios y reseñas reales, para que quien los busque los encuentre y reserve:`,
              biz.url_demo,
              `Ya esta listo y no les cuesta nada verlo. No toca para nada su sistema de reservas, y si no les gusta lo bajo hoy mismo.`,
              redesign ? `¿Se la muestro?` : `¿Se los dejo activo?`,
              `Michael Vargas\nMerktop · https://merktop.com`,
            ];
        const text = lines.join('\n\n');
        const html = lines.map(p => `<p>${p.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(new RegExp(biz.url_demo.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')), `<a href="${biz.url_demo}">${biz.url_demo}</a>`).replace(/\n/g, '<br>')}</p>`).join('');

        const r = await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            authorization: `Bearer ${env.RESEND_API_KEY}`,
            'content-type': 'application/json',
            'Idempotency-Key': `siteforge-panel-${slug}`,
          },
          body: JSON.stringify({
            from: 'Michael Vargas <michael@go.merktop.com>',
            to: [biz.email],
            reply_to: 'jose@merktop.com',
            subject,
            text,
            html,
            tags: [{ name: 'campaign', value: 'siteforge' }],
          }),
        });
        const data = await r.json().catch(() => ({}));
        if (!r.ok) return json({ error: 'Resend fallo', detail: data }, 502);

        sentLog[slug] = new Date().toISOString();
        await env.SITEFORGE_KV.put('sent_log', JSON.stringify(sentLog));
        const updated = registry.map(b => (b.slug === slug ? { ...b, outreach: 'sent', resend_id: data.id || b.resend_id } : b));
        await env.SITEFORGE_KV.put('registry', JSON.stringify(updated));
        return json({ ok: true, id: data.id, to: biz.email, subject, lang: en ? 'en' : 'es' });
      }

      // ---- DOMINIOS (Cloudflare Registrar) ----
      // Checar disponibilidad + precio de un nombre en varios TLDs. Gratis, sin riesgo.
      if (url.pathname === '/api/domain/check' && req.method === 'POST') {
        const cfTok = cfRegistrarToken(env);
        if (!cfTok || !env.CF_ACCOUNT_ID) {
          return json({
            error: 'Falta CF_REGISTRAR_TOKEN en el worker',
            como_arreglarlo: 'npx wrangler secret put CF_REGISTRAR_TOKEN -c ui/wrangler.jsonc',
            nota: 'Ponerlo como SECRET, no como variable del dashboard: un deploy reemplaza las vars y la borra.',
          }, 500);
        }
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        // El punto que separa nombre y TLD es DATO, no suciedad: sanear a lo bruto con
        // replace(/[^a-z0-9-]/g,'') convertia "mibarberia.com" en "mibarberiacom" y buscaba
        // "mibarberiacom.com". Hay que parsear primero y limpiar despues.
        const crudo = (body.name || '').toString().toLowerCase().trim()
          .replace(/^https?:\/\//, '')   // pegar la URL entera tambien vale
          .replace(/^www\./, '')
          .replace(/[/?#].*$/, '')       // quitar path/query
          .replace(/\s+/g, '');          // "mi barberia" -> "mibarberia"
        const conTld = crudo.match(/^([a-z0-9][a-z0-9-]*)\.([a-z]{2,24}(?:\.[a-z]{2,24})?)$/);
        const base = (conTld ? conTld[1] : crudo).replace(/[^a-z0-9-]/g, '').replace(/^-+|-+$/g, '').slice(0, 50);
        if (!base) return json({ error: 'nombre invalido' }, 400);
        const pedido = conTld ? conTld[2] : null;
        // Si el usuario escribio un TLD concreto, ese va PRIMERO y siempre se consulta.
        const porDefecto = ['com', 'net', 'co', 'studio'];
        const listaTlds = Array.isArray(body.tlds) && body.tlds.length ? body.tlds : porDefecto;
        const tlds = [...new Set([...(pedido ? [pedido] : []), ...listaTlds])]
          .map(t => String(t).toLowerCase().replace(/[^a-z.]/g, '')).filter(Boolean).slice(0, 6);
        const domains = tlds.map(t => `${base}.${t}`);
        const r = await fetch(`https://api.cloudflare.com/client/v4/accounts/${env.CF_ACCOUNT_ID}/registrar/domain-check`, {
          method: 'POST',
          headers: { authorization: `Bearer ${cfTok}`, 'content-type': 'application/json' },
          body: JSON.stringify({ domains }),
        });
        const data = await r.json().catch(() => ({}));
        if (!r.ok) return json({ error: 'CF domain-check fallo', detail: data }, 502);
        const list = (data.result && data.result.domains) || data.result || [];
        // `base` y `buscados` vuelven al panel para que se vea QUE se busco de verdad:
        // si el texto se normaliza, el usuario tiene que poder notarlo.
        return json({ ok: true, base, buscados: domains, results: Array.isArray(list) ? list : [] });
      }

      // Comprar un dominio y montar el sitio en el. ACCION DE DINERO: requiere key + confirm:true,
      // tope diario y anti-duplicado. Nunca compra sin confirmacion explicita del precio.
      if (url.pathname === '/api/domain/buy' && req.method === 'POST') {
        const cfTok = cfRegistrarToken(env);
        if (!cfTok || !env.CF_ACCOUNT_ID) {
          return json({
            error: 'Falta CF_REGISTRAR_TOKEN en el worker',
            como_arreglarlo: 'npx wrangler secret put CF_REGISTRAR_TOKEN -c ui/wrangler.jsonc',
            nota: 'Ponerlo como SECRET, no como variable del dashboard: un deploy reemplaza las vars y la borra.',
          }, 500);
        }
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        if (body.confirm !== true) return json({ error: 'la compra requiere confirm:true' }, 400);
        const slug = (body.slug || '').toString();
        if (!/^[a-z0-9-]{1,40}$/.test(slug)) return json({ error: 'slug invalido' }, 400);
        const domain = (body.domain || '').toString().toLowerCase().trim();
        if (!/^[a-z0-9-]{1,63}\.[a-z]{2,20}$/.test(domain)) return json({ error: 'dominio invalido' }, 400);
        const registry = (await env.SITEFORGE_KV.get('registry', 'json')) || [];
        const biz = registry.find(b => b.slug === slug);
        if (!biz) return json({ error: 'negocio no encontrado en el registro' }, 404);
        // Guardas de dinero: tope diario + anti-duplicado
        const buys = (await env.SITEFORGE_KV.get('domain_buys', 'json')) || [];
        const today = new Date().toISOString().slice(0, 10);
        if (buys.filter(b => (b.at || '').slice(0, 10) === today).length >= 10) {
          return json({ error: 'tope diario de compras alcanzado (10). Reintenta manana.' }, 429);
        }
        if (buys.some(b => b.domain === domain)) return json({ error: 'ese dominio ya fue comprado' }, 409);
        const cf = (path, opts = {}) => fetch(`https://api.cloudflare.com/client/v4${path}`, {
          ...opts,
          headers: { authorization: `Bearer ${cfTok}`, 'content-type': 'application/json', ...(opts.headers || {}) },
        });
        // 1) re-check justo antes de registrar (recomendado por CF)
        const chk = await cf(`/accounts/${env.CF_ACCOUNT_ID}/registrar/domain-check`, { method: 'POST', body: JSON.stringify({ domains: [domain] }) }).then(r => r.json()).catch(() => ({}));
        const availList = (chk.result && chk.result.domains) || chk.result || [];
        const avail = (Array.isArray(availList) ? availList : []).find(d => (d.domain || d.name) === domain);
        if (avail && avail.registrable === false) return json({ error: 'el dominio ya no esta disponible', detail: avail }, 409);
        // 2) registrar el dominio (cobra al billing profile de la cuenta CF)
        const reg = await cf(`/accounts/${env.CF_ACCOUNT_ID}/registrar/registrations`, { method: 'POST', body: JSON.stringify({ domain_name: domain }) });
        const regData = await reg.json().catch(() => ({}));
        if (!reg.ok) return json({ error: 'registro fallo (revisa: registrant contact configurado, metodo de pago valido, acceso a la beta de Registrar API)', detail: regData }, 502);
        // 3) zone_id (el registro crea la zona en CF; puede tardar unos segundos)
        let zoneId = null;
        for (let i = 0; i < 4 && !zoneId; i++) {
          const zr = await cf(`/zones?name=${encodeURIComponent(domain)}`).then(r => r.json()).catch(() => ({}));
          zoneId = (zr.result && zr.result[0] && zr.result[0].id) || null;
          if (!zoneId) await new Promise(res => setTimeout(res, 1500));
        }
        // 4) montar: custom domain del worker de demos + mapa hostname->slug
        let attached = false;
        if (zoneId) {
          const ad = await cf(`/accounts/${env.CF_ACCOUNT_ID}/workers/domains`, {
            method: 'PUT',
            body: JSON.stringify({ hostname: domain, service: 'siteforge-demos', environment: 'production', zone_id: zoneId }),
          });
          attached = ad.ok;
        }
        await env.SITEFORGE_KV.put('domain:' + domain, slug);
        // 5) log de compra + actualizar el negocio
        buys.push({ domain, slug, at: new Date().toISOString() });
        await env.SITEFORGE_KV.put('domain_buys', JSON.stringify(buys));
        const updated = registry.map(b => (b.slug === slug ? { ...b, custom_domain: domain, live_url: `https://${domain}/` } : b));
        await env.SITEFORGE_KV.put('registry', JSON.stringify(updated));
        return json({
          ok: true, domain, slug, live_url: `https://${domain}/`, worker_attached: attached,
          note: attached ? 'Sitio montado. SSL puede tardar unos minutos.' : 'Dominio registrado y mapeado; el enlace del worker se completara al propagar la zona.',
        });
      }

      if (url.pathname === '/api/registry' && req.method === 'POST') {
        let body;
        try { body = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
        if (!Array.isArray(body)) return json({ error: 'se espera un array' }, 400);
        await env.SITEFORGE_KV.put('registry', JSON.stringify(body));
        return json({ ok: true, count: body.length });
      }

      return json({ error: 'not found' }, 404);
    }

    return env.ASSETS.fetch(req);
  },
};
