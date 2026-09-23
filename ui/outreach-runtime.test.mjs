import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';

// Use the workerd/esbuild versions shipped with this repo's pinned Wrangler installation.
const require = createRequire(realpathSync(new URL('../node_modules/wrangler/package.json', import.meta.url)));
const { Miniflare, convertV4MiniflareOptions = x => x } = require('miniflare');
const { build } = require('esbuild');

test('Workers runtime: durable RPC, authenticated routes, unsigned webhooks and permissions', async () => {
  const source = `
    import worker from './worker.js';
    export { QueueClaims, OutreachCampaign } from './worker.js';
    export default { async fetch(req, env, ctx) {
      if (new URL(req.url).pathname === '/test/rpc') {
        const {method, input} = await req.json();
        const campaign = env.OUTREACH_CAMPAIGN.getByName('permission-pilot-v1');
        if (method === 'status') return Response.json(await campaign.status());
        if (method === 'run') return Response.json(await campaign.run());
        if (method === 'consent') return Response.json(await campaign.consent(input));
        if (method === 'salesSave') return Response.json(await campaign.salesSave(input));
        if (method === 'salesList') return Response.json(await campaign.salesList());
        if (method === 'salesHistory') return Response.json(await campaign.salesHistory(input));
      }
      return worker.fetch(req, env, ctx);
    }};
  `;
  const bundle = await build({ stdin: { contents: source, resolveDir: fileURLToPath(new URL('.', import.meta.url)) }, bundle: true,
    write: false, format: 'esm', platform: 'neutral', external: ['cloudflare:*'] });
  const mf = new Miniflare(convertV4MiniflareOptions({ modules: true, script: bundle.outputFiles[0].text, compatibilityDate: '2026-08-22',
    kvNamespaces: ['SITEFORGE_KV'], durableObjects: { QUEUE_CLAIMS: { className: 'QueueClaims', useSQLite: true }, OUTREACH_CAMPAIGN: { className: 'OutreachCampaign', useSQLite: true } } }));
  try {
    const rpc = async (method, input) => (await mf.dispatchFetch('https://test.local/test/rpc', { method: 'POST', body: JSON.stringify({ method, input }) })).json();
    const kv = await mf.getKVNamespace('SITEFORGE_KV');
    await kv.put('registry', JSON.stringify([{ slug: 'test', name: 'Test', language: 'en', has_own_site: false, email: 'owner@example.com', url_demo: 'https://siteforge-demos.odd-forest-9504.workers.dev/test/' }]));
    assert.equal((await rpc('status')).total, 1);
    assert.equal((await rpc('run')).reason, 'provider_not_configured');
    const grant = await rpc('consent', { slug: 'test', email: 'owner@example.com', confirmed: true, source: 'inbound_request', evidence: 'Fixture request; not a real recipient' });
    assert.equal(grant.ok, true);
    assert.equal((await rpc('status')).blocked.email_provider_required, 1);
    const sale={slug:'test',revision:0,stage:'interested',channel:'email',language:'en',benefit:'contact',objection:'none',observation:'',note:'Fixture: owner asked about pricing.',confirmed:true};
    const results=await Promise.all([rpc('salesSave',sale),rpc('salesSave',sale)]);
    assert.equal(results.filter(r=>r.ok).length,1);
    assert.equal(results.filter(r=>r.conflict).length,1);
    assert.equal((await rpc('salesList')).sales.test.stage,'interested');
    assert.equal((await rpc('salesHistory','test')).length,1);
    for (const path of ['/api/outreach/sales', '/api/outreach/status', '/api/outreach/consent', '/api/outreach/inbox', '/api/outreach/read', '/api/send']) {
      const response = await mf.dispatchFetch(`https://test.local${path}`, { method: 'POST', body: '{}' });
      assert.equal(response.status, 401);
    }
    assert.equal((await mf.dispatchFetch('https://test.local/webhooks/telnyx', { method: 'POST', body: '{}' })).status, 401);
    assert.equal((await mf.dispatchFetch('https://test.local/unsubscribe/' + 'a'.repeat(64))).status, 404);
  } finally { await mf.dispose(); }
});
