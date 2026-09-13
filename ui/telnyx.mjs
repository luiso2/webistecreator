// No SDK/global credentials; Workers fetch + WebCrypto. Never log webhook bodies or keys.
export async function boundedBody(request, limit = 65536) {
  if (Number(request.headers.get('content-length')) > limit) throw new Error('body_too_large');
  if (!request.body) return '';
  const reader = request.body.getReader();
  const chunks = [];
  let total = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > limit) { await reader.cancel(); throw new Error('body_too_large'); }
      chunks.push(value);
    }
  } finally { reader.releaseLock(); }
  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
  return new TextDecoder().decode(bytes);
}

export async function verifyTelnyxWebhook(raw, headers, publicKey, now = Date.now()) {
  const timestamp = headers.get('telnyx-timestamp');
  const signature = headers.get('telnyx-signature-ed25519');
  if (!publicKey || !signature || !/^\d{10}$/.test(timestamp || '')
      || Math.abs(now / 1000 - Number(timestamp)) > 300 || raw.length > 65536) return false;
  try {
    const decode = value => Uint8Array.from(atob(value), c => c.charCodeAt(0));
    const key = await crypto.subtle.importKey('raw', decode(publicKey), { name: 'Ed25519' }, false, ['verify']);
    return await crypto.subtle.verify('Ed25519', key, decode(signature), new TextEncoder().encode(`${timestamp}|${raw}`));
  } catch { return false; }
}
