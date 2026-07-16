const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8' },
  });

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
      const pending = queue.filter(q => q.status === 'pending').map(({ id, input, created }) => ({ id, input, created }));
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
      if (typeof body.name === 'string' && body.name.length <= 120) result.name = body.name;
      if (typeof body.url_demo === 'string' && DEMO_URL_RE.test(body.url_demo)) result.url_demo = body.url_demo;
      let queue = (await env.SITEFORGE_KV.get('queue', 'json')) || [];
      const exists = queue.some(q => q.id === body.id && (q.status === 'pending' || q.status === 'processing'));
      if (!exists) return json({ error: 'item no pendiente' }, 404);
      queue = queue.map(q => (q.id === body.id ? { ...q, status: 'done', done_at: new Date().toISOString(), result } : q));
      await env.SITEFORGE_KV.put('queue', JSON.stringify(queue));
      return json({ ok: true });
    }

    if (url.pathname.startsWith('/api/')) {
      if (!(await isAuthorized(req))) return json({ error: 'unauthorized' }, 401);

      if (url.pathname === '/api/state' && req.method === 'GET') {
        const [registry, queue] = await Promise.all([
          env.SITEFORGE_KV.get('registry', 'json'),
          env.SITEFORGE_KV.get('queue', 'json'),
        ]);
        return json({ registry: registry || [], queue: queue || [] });
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
