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

export default {
  async fetch(req, env) {
    const url = new URL(req.url);

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
