import test from 'node:test';
import assert from 'node:assert/strict';
import { cleanMessage, repairDemoSeparator } from './public/outreach-message.mjs';
import { DEMO_ORIGIN, eligibility, opener, verifyDemo, smsReady } from './outreach-policy.mjs';
import { OutreachEngine } from './outreach-engine.mjs';
import { boundedBody, verifyTelnyxWebhook } from './telnyx.mjs';

const version = 'a'.repeat(64);
const biz = { slug: 'test-shop', name: 'Test Shop', language: 'en', email: 'owner@example.com', phone: '+13055550100', has_own_site: false, url_demo: `${DEMO_ORIGIN}/test-shop/` };
const consent = { slug: biz.slug, email: biz.email, channel: 'email', evidence: 'Owner requested this preview in their inbound email', at: new Date().toISOString(), source: 'inbound_request', confirmed: true };
class Storage {
  data = new Map();
  async get(k) { return structuredClone(this.data.get(k)); }
  async put(k, v) { this.data.set(k, structuredClone(v)); }
  async list({ prefix }) { return new Map([...this.data].filter(([k]) => k.startsWith(prefix))); }
  async transaction(fn) { return fn(this); }
}
function fixture({ leads = [biz], provider, qaFailure } = {}) {
  const storage = new Storage();
  const state = { registry: leads, crm: {}, sent_log: {} };
  const requests = [];
  const assets = [`${DEMO_ORIGIN}/_siteforge/assets/test-shop/${version}/index.html`, `${DEMO_ORIGIN}/_siteforge/assets/test-shop/${version}/image.webp`];
  const env = { RESEND_API_KEY: 'test-only', SITEFORGE_KV: { get: async k => structuredClone(state[k]) }, QUEUE_CLAIMS: { getByName: () => ({ markOutreachSent: async () => {} }) } };
  const fetcher = async (url, options = {}) => {
    requests.push({ url, options });
    if (url.startsWith('https://api.')) return provider ? provider(url, options) : Response.json({ id: 'provider-id' });
    if (qaFailure) return new Response('missing', { status: 404 });
    if (url === biz.url_demo) return new Response(`<html><body>Test Shop<img src="${assets[1]}"></body></html>`, { headers: { 'content-type': 'text/html' } });
    if (url.includes('/manifests/')) return Response.json({ files: assets.map(url => ({ url, sha256: version })) });
    return new Response(null, { headers: { 'cache-control': 'public, immutable' } });
  };
  return { storage, state, env, requests, fetcher, engine: new OutreachEngine(storage, env, fetcher) };
}
const providerCalls = f => f.requests.filter(r => r.url.startsWith('https://api.') && r.options.method === 'POST');

test('new messages preserve line breaks and old URL + It gets repaired', () => {
  const text = `See this:\n\n${biz.url_demo}\n\nIt is your preview.`;
  assert.equal(cleanMessage(text), text);
  assert.equal(repairDemoSeparator(text.replaceAll('\n', ''), biz.url_demo), `See this:${biz.url_demo}\n\nIt is your preview.`);
  assert.equal(repairDemoSeparator(`${biz.url_demo}services/`, biz.url_demo), `${biz.url_demo}services/`);
  assert.equal(cleanMessage('<b>safe</b>\x00\ntext'), 'bsafe/b\ntext');
});
test('email permission is mandatory and tied to recipient', () => {
  assert.equal(eligibility(biz), 'email_permission_required');
  assert.equal(eligibility(biz, { consent }), null);
  assert.equal(eligibility({ ...biz, email: 'other@example.com' }, { consent }), 'email_permission_required');
  assert.equal(eligibility(biz, { consent, crm: { status: 'declined' } }), 'already_in_conversation');
});
test('unknown site filter, language and outside URL rejected', () => {
  for (const patch of [{ has_own_site: undefined }, { language: 'auto' }, { url_demo: 'http://169.254.169.254/' }]) assert.ok(eligibility({ ...biz, ...patch }, { consent }));
});
test('English and Spanish templates keep the link separate', () => {
  assert.match(opener(biz, 'https://example.com/unsubscribe').text, /\n\nhttps:.*\/\n\n/);
  assert.match(opener({ ...biz, language: 'es' }, 'https://example.com/unsubscribe').text, /sin compromiso/);
  assert.doesNotMatch(opener(biz, 'https://example.com/unsubscribe').text, /José/);
});
test('QA checks stable HTML, manifest and immutable assets', async () => {
  const f = fixture();
  assert.equal((await verifyDemo(biz, f.fetcher)).assets, 2);
  assert.equal(f.requests.filter(r => r.options.method === 'HEAD').length, 2);
});
test('QA will not follow a redirect or fetch untrusted host', async () => {
  await assert.rejects(verifyDemo(biz, async () => new Response(null, { status: 302, headers: { location: 'http://localhost' } })), /qa_http_302/);
  let calls = 0;
  await assert.rejects(verifyDemo({ ...biz, url_demo: 'http://localhost/' }, async () => { calls++; }), /qa_invalid_demo/);
  assert.equal(calls, 0);
});
test('no permission -> no provider requests, no fake success', async () => {
  const f = fixture();
  assert.equal((await f.engine.run()).reason, 'no_eligible_candidates');
  assert.equal(providerCalls(f).length, 0);
  assert.equal((await f.engine.status()).confirmedClients, 0);
});
test('concurrent run, next tick and process restart do not duplicate', async () => {
  const f = fixture(); await f.engine.consent(consent);
  const results = await Promise.all([f.engine.run(), f.engine.run()]);
  assert.equal(results.filter(r => r.ok).length, 1);
  await f.engine.run();
  await new OutreachEngine(f.storage, f.env, f.fetcher).run();
  assert.equal(providerCalls(f).length, 1);
  assert.equal((await f.engine.status()).accepted, 1);
  assert.equal((await f.engine.status()).delivered, 0);
});
test('ambiguous timeout reserves recipient permanently for review', async () => {
  const f = fixture({ provider: () => { throw new Error('timeout'); } }); await f.engine.consent(consent);
  assert.equal((await f.engine.run()).reason, 'provider_result_unknown');
  await new OutreachEngine(f.storage, f.env, f.fetcher).run();
  assert.equal(providerCalls(f).length, 1);
  assert.equal((await f.engine.status()).needsReview, 1);
});
test('dead demo blocks outreach and records reason', async () => {
  const f = fixture({ qaFailure: true }); await f.engine.consent(consent);
  assert.equal((await f.engine.run()).reason, 'qa_http_404');
  assert.equal(providerCalls(f).length, 0);
});
test('duplicate business email under another slug stays blocked', async () => {
  const f = fixture({ leads: [biz, { ...biz, slug: 'other', outreach: 'sent' }] }); await f.engine.consent(consent);
  assert.equal((await f.engine.run()).reason, 'no_eligible_candidates');
});
test('pause, daily ceiling and untrusted permission input', async () => {
  const f = fixture(); await f.engine.consent(consent);
  await assert.rejects(f.engine.config({ enabled: true, dailyLimit: 21 }), /invalid_config/);
  await assert.rejects(f.engine.consent({ ...consent, source: 'google_maps' }), /evidence/);
  await f.engine.config({ enabled: false, dailyLimit: 20 });
  assert.equal((await f.engine.run()).reason, 'paused');
  await f.engine.config({ enabled: true, dailyLimit: 1 });
  await f.storage.put('send:old', { slug: 'prior', at: new Date().toISOString(), status: 'accepted' });
  assert.equal((await f.engine.run()).reason, 'daily_limit');
});
test('unsubscribe GET has no side effects; POST permanently suppresses', async () => {
  const f = fixture(); await f.engine.consent(consent); await f.engine.run();
  const [token] = [...(await f.storage.list({ prefix: 'token:' })).keys()];
  assert.equal(await f.engine.unsubscribe(token.slice(6)), true);
  assert.equal((await f.storage.list({ prefix: 'suppress:' })).size, 0);
  await f.engine.unsubscribe(token.slice(6), true);
  await assert.rejects(f.engine.consent(consent), /suppressed/);
});
test('Telnyx disabled until all credentials and registration approved', () => {
  assert.equal(smsReady({ TELNYX_API_KEY: 'test' }), false);
});
test('Telnyx SMS uses consented E164, receives STOP and does not claim a sale', async () => {
  const f = fixture({ provider: () => Response.json({ data: { id: 'telnyx-id' } }) });
  Object.assign(f.env, { TELNYX_API_KEY: 'test', TELNYX_FROM_NUMBER: '+13055550199', TELNYX_PUBLIC_KEY: 'test', TELNYX_MESSAGING_PROFILE_ID: 'profile', TELNYX_SMS_APPROVED: 'true' });
  await f.engine.consent({ ...consent, channel: 'sms', email: undefined, phone: biz.phone });
  const result = await f.engine.run();
  assert.equal(result.channel, 'sms');
  assert.equal(providerCalls(f)[0].url, 'https://api.telnyx.com/v2/messages');
  await f.engine.telnyxEvent({ id: 'event', event_type: 'message.received', payload: { messaging_profile_id: 'profile', from: { phone_number: biz.phone }, to: [{ phone_number: f.env.TELNYX_FROM_NUMBER }], text: 'STOP' } });
  assert.equal((await f.storage.list({ prefix: 'suppress:' })).size, 1);
  assert.equal((await f.engine.status()).confirmedClients, 0);
});
test('Telnyx webhook Ed25519 signature, tampering and replay window', async () => {
  const pair = await crypto.subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify']);
  const base64 = bytes => Buffer.from(bytes).toString('base64');
  const key = base64(await crypto.subtle.exportKey('raw', pair.publicKey));
  const timestamp = String(Math.floor(Date.now() / 1000));
  const raw = '{"data":{"id":"test"}}';
  const signature = base64(await crypto.subtle.sign('Ed25519', pair.privateKey, new TextEncoder().encode(`${timestamp}|${raw}`)));
  const headers = new Headers({ 'telnyx-timestamp': timestamp, 'telnyx-signature-ed25519': signature });
  assert.equal(await verifyTelnyxWebhook(raw, headers, key), true);
  assert.equal(await verifyTelnyxWebhook(raw + ' ', headers, key), false);
  assert.equal(await verifyTelnyxWebhook(raw, headers, key, Date.now() + 3600000), false);
});
test('untrusted webhook body size is bounded without Content-Length', async () => {
  await assert.rejects(boundedBody(new Request('https://test.local', { method: 'POST', body: 'x'.repeat(65) }), 64), /body_too_large/);
});
test('suppressed SMS permission also blocks email for the same business', async () => {
  const f = fixture(); await f.engine.consent(consent);
  await f.engine.consent({ ...consent, channel: 'sms', phone: biz.phone });
  await f.engine.event({ phone: biz.phone, type: 'declined', confirmed: true, evidence: 'Inbound reply explicitly declined further outreach' });
  assert.equal((await f.engine.status()).eligible, 0);
});
test('late consent change during QA prevents provider call', async () => {
  const f = fixture(); await f.engine.consent(consent);
  const fetcher = f.engine.fetcher;
  f.engine.fetcher = async (...args) => {
    const result = await fetcher(...args);
    if (args[1]?.method === 'HEAD') f.state.crm[biz.slug] = { status: 'declined' };
    return result;
  };
  assert.equal((await f.engine.run()).reason, 'eligibility_changed');
  assert.equal(providerCalls(f).length, 0);
});
