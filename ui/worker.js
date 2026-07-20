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
      // El demo DEBE estar live antes de registrar la tarjeta: sin esto, una forja podia
      // crear tarjetas fantasma que dan 404 (incidente 2026-07-20). La forja ya espera el
      // 200 antes de hacer upsert, asi que esto solo rechaza registros de demos inexistentes.
      try {
        const probe = await fetch(body.url_demo, { method: 'GET', cf: { cacheTtl: 0 } });
        if (!probe.ok) return json({ error: `demo no live (HTTP ${probe.status}); no se registra la tarjeta` }, 422);
      } catch (e) {
        return json({ error: 'no se pudo verificar el demo; no se registra' }, 422);
      }
      const S = (v, max) => (typeof v === 'string' ? stripUnsafe(v.slice(0, max)) : undefined);
      const limpio = {
        slug,
        name: S(body.name, 120) || slug,
        city: S(body.city, 80),
        ig: S(body.ig, 60),
        url_demo: body.url_demo,
        has_own_site: body.has_own_site === true,
        email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email || '') ? S(body.email, 120) : null,
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
        registry[idx] = { ...actual, ...Object.fromEntries(Object.entries(limpio).filter(([, v]) => v !== undefined)) };
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
        const [registry, queue, crm] = await Promise.all([
          env.SITEFORGE_KV.get('registry', 'json'),
          env.SITEFORGE_KV.get('queue', 'json'),
          env.SITEFORGE_KV.get('crm', 'json'),
        ]);
        // El CRM (cliente cerrado / descartado) vive en su propia llave: ninguna
        // sincronizacion del registro desde el repo o la forja lo puede pisar.
        const map = crm || {};
        const reg = (registry || []).map(b => (map[b.slug]
          ? { ...b, crm_status: map[b.slug].status, crm_at: map[b.slug].at }
          : b));
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
        if (!['client', 'declined', 'pending'].includes(status)) return json({ error: 'status invalido' }, 400);
        const crm = (await env.SITEFORGE_KV.get('crm', 'json')) || {};
        if (status === 'pending') {
          delete crm[slug];
        } else {
          crm[slug] = { status, at: new Date().toISOString() };
        }
        await env.SITEFORGE_KV.put('crm', JSON.stringify(crm));
        const clientes = Object.values(crm).filter(c => c.status === 'client').length;
        return json({ ok: true, slug, status, clientes });
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
        let queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
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
        // Anti-duplicado: registry (sincronizado desde el repo) + log propio del panel
        const sentLog = (await env.SITEFORGE_KV.get('sent_log', 'json')) || {};
        if (biz.outreach === 'sent' || sentLog[slug]) {
          return json({ error: 'ya se le envio email a este negocio', sent_at: sentLog[slug] || biz.fecha }, 409);
        }

        const en = (biz.language || 'es') === 'en';
        const redesign = !!biz.has_own_site;
        const subject = en
          ? (redesign ? `A premium redesign concept for ${biz.name}` : `A sample website for ${biz.name}`)
          : (redesign ? `Una propuesta de rediseño premium para ${biz.name}` : `Un website de muestra para ${biz.name}`);
        const lines = en
          ? [
              `Hi ${biz.name} team!`,
              redesign
                ? `I'm Michael, from Merktop (Miami). I found your business on Google and put together an alternative premium design concept for your site, built with your real photos, services and reviews:`
                : `I'm Michael, from Merktop (Miami). I found your business on Google, saw you don't have your own website yet, and went ahead and built you a sample one with your real photos, services and reviews:`,
              biz.url_demo,
              `It doesn't touch your booking flow at all. If you like it, we can put it on your own domain and adjust it together. If not, I'll take it down, no strings attached.`,
              `Michael Vargas\nMerktop · https://merktop.com`,
            ]
          : [
              `Hola equipo ${biz.name}!`,
              redesign
                ? `Soy Michael, de Merktop (Miami). Encontre su negocio en Google y prepare una propuesta alternativa de diseño premium para su sitio, construida con sus fotos, servicios y reseñas reales:`
                : `Soy Michael, de Merktop (Miami). Encontre su negocio en Google, vi que todavia no tienen website propio y me anime a construirles uno de muestra con sus fotos, servicios y reseñas reales:`,
              biz.url_demo,
              `No toca para nada su sistema de reservas. Si les gusta, lo dejamos en su propio dominio y lo ajustamos juntos. Si no, lo retiro sin compromiso.`,
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
