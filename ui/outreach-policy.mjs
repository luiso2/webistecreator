export const DEMO_ORIGIN = 'https://siteforge-demos.odd-forest-9504.workers.dev';
export const DEFAULT_CONFIG = Object.freeze({ enabled: true, dailyLimit: 20, channel: 'email' });
export const emailKey = value => String(value || '').trim().toLowerCase();
export const validEmail = value => typeof value === 'string' && value.length <= 254 && /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(value);
export const validPhone = value => typeof value === 'string' && /^\+[1-9]\d{7,14}$/.test(value);
export function phoneMatches(stored, explicit) {
  const digits = String(stored || '').replace(/\D/g, '');
  return validPhone(explicit) && (digits === explicit.slice(1)
    || (explicit.startsWith('+1') && digits.length === 10 && digits === explicit.slice(2)));
}
export const smsReady = env => !!(env.TELNYX_API_KEY && validPhone(env.TELNYX_FROM_NUMBER)
  && env.TELNYX_MESSAGING_PROFILE_ID && env.TELNYX_PUBLIC_KEY && env.TELNYX_SMS_APPROVED === 'true');

export function eligibility(biz, { crm = {}, consent, suppressed, sent = false, channel = 'email' } = {}) {
  if (!biz || !/^[a-z0-9-]{1,40}$/.test(biz.slug)) return 'invalid_business';
  if (suppressed) return 'suppressed';
  if (['client', 'declined', 'contacted', 'replied'].includes(crm.status)) return 'already_in_conversation';
  if (sent || ['sent', 'skip_duplicate'].includes(biz.outreach)) return 'already_contacted';
  if (biz.has_own_site !== false) return 'website_filter_not_confirmed';
  if (channel === 'email' && !validEmail(biz.email)) return 'missing_email';
  if (channel === 'sms' && !phoneMatches(biz.phone, consent?.phone)) return 'sms_permission_required';
  if (biz.url_demo !== `${DEMO_ORIGIN}/${biz.slug}/`) return 'invalid_demo_url';
  if (!['en', 'es'].includes(biz.language)) return 'unknown_language';
  if (!consent || consent.revoked || (channel === 'email' && consent.email !== emailKey(biz.email))
      || (consent.channel || 'email') !== channel
      || consent.slug !== biz.slug || !consent.evidence || !consent.at) return `${channel}_permission_required`;
  return null;
}

export function smsOpener(biz) {
  return biz.language === 'en'
    ? `Michael at Merktop: your website demo is ready: ${biz.url_demo} Would you like the details? Reply STOP to opt out.`
    : `Michael de Merktop: su demo está lista: ${biz.url_demo} ¿Le envío los detalles? Responda STOP para darse de baja.`;
}

export function opener(biz, unsubscribeUrl) {
  const en = biz.language === 'en';
  const subject = en ? `${biz.name}: your website preview` : `${biz.name}: la vista previa de su website`;
  const lines = en ? [
    `Hi ${biz.name},`,
    'Here is the website concept for your business. It gives customers one place to see your services and get in touch:',
    biz.url_demo,
    'This is a demo, with no obligation and no changes to your domain. Would you like me to explain how to make it yours?',
    'Michael | Merktop',
    `No more emails: ${unsubscribeUrl}`,
  ] : [
    `Hola ${biz.name},`,
    'Aquí está el concepto de website para su negocio: un lugar donde sus clientes pueden conocer sus servicios y contactarles:',
    biz.url_demo,
    'Es una demo, sin compromiso y sin cambios en su dominio. ¿Les gustaría que les explique cómo hacerla suya?',
    'Michael | Merktop',
    `No recibir más correos: ${unsubscribeUrl}`,
  ];
  return { subject, text: lines.join('\n\n') };
}

async function checkedFetch(url, fetcher, method = 'GET') {
  if (new URL(url).origin !== DEMO_ORIGIN) throw new Error('qa_unauthorized_url');
  const res = await fetcher(url, { method, redirect: 'manual', signal: AbortSignal.timeout(8000) });
  if (res.status !== 200) throw new Error(`qa_http_${res.status}`);
  return res;
}

export async function verifyDemo(biz, fetcher = fetch) {
  if (biz.url_demo !== `${DEMO_ORIGIN}/${biz.slug}/`) throw new Error('qa_invalid_demo');
  const res = await checkedFetch(biz.url_demo, fetcher);
  if (!res.headers.get('content-type')?.includes('text/html')) throw new Error('qa_not_html');
  const html = await res.text();
  if (html.length > 2_000_000 || !html.includes('</html>')) throw new Error('qa_invalid_html');
  const normalize = s => String(s).normalize('NFKD').replace(/[^a-z0-9]/gi, '').toLowerCase();
  if (!normalize(html).includes(normalize(biz.name)) || !normalize(biz.name)) throw new Error('qa_wrong_business');
  const version = html.match(new RegExp(`/_siteforge/assets/${biz.slug}/([a-f0-9]{64})/`))?.[1];
  // Only independently published bundles are eligible for autonomous sending.
  if (!version) throw new Error('qa_independent_bundle_required');
  const manifestUrl = `${DEMO_ORIGIN}/_siteforge/manifests/${biz.slug}/${version}.json`;
  const manifest = await (await checkedFetch(manifestUrl, fetcher)).json();
  if (!Array.isArray(manifest.files) || !manifest.files.length || manifest.files.length > 160) throw new Error('qa_invalid_manifest');
  const prefix = `${DEMO_ORIGIN}/_siteforge/assets/${biz.slug}/${version}/`;
  const urls = manifest.files.map(file => {
    if (typeof file.url !== 'string' || !file.url.startsWith(prefix)
        || new URL(file.url).href !== file.url || !/^[a-f0-9]{64}$/.test(file.sha256)) throw new Error('qa_invalid_asset');
    return file.url;
  });
  const refs = [...html.matchAll(/(?:src|href)=["']([^"']+)["']/g)].map(m => m[1]);
  for (const ref of refs.filter(r => r.includes('/_siteforge/assets/'))) {
    if (!urls.includes(new URL(ref, biz.url_demo).href)) throw new Error('qa_unlisted_asset');
  }
  // Six parallel requests, bounded bundle size, no redirects or arbitrary hosts.
  for (let i = 0; i < urls.length; i += 6) {
    await Promise.all(urls.slice(i, i + 6).map(async url => {
      const asset = await checkedFetch(url, fetcher, 'HEAD');
      if (!asset.headers.get('cache-control')?.includes('immutable')) throw new Error('qa_mutable_asset');
    }));
  }
  return { html: 200, manifest: 200, assets: urls.length, version, checkedAt: new Date().toISOString() };
}
