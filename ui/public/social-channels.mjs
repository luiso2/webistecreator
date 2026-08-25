const INSTAGRAM_RESERVED_PATHS = new Set([
  'about', 'accounts', 'challenge', 'developer', 'direct', 'directory', 'emails',
  'explore', 'legal', 'p', 'press', 'privacy', 'reel', 'reels', 'stories', 'terms', 'tv',
]);

function cleanInstagramHandle(value) {
  const handle = String(value || '').trim().replace(/^@/, '');
  if (!/^[A-Za-z0-9._]{1,30}$/.test(handle)) return null;
  if (handle.startsWith('.') || handle.endsWith('.') || handle.includes('..')) return null;
  if (INSTAGRAM_RESERVED_PATHS.has(handle.toLowerCase())) return null;
  return handle;
}

// Acepta solamente un @handle, un handle desnudo o una URL de perfil directa.
// Nunca "arregla" texto arbitrario quitando caracteres: esa conducta convertía
// "Google Maps" en el usuario inexistente "GoogleMaps".
export function normalizeInstagramHandle(value) {
  if (typeof value !== 'string') return null;
  const raw = value.trim();
  if (!raw) return null;

  let parsed = null;
  const looksLikeInstagramUrl = /^(?:https?:\/\/)?(?:[a-z0-9-]+\.)*instagram\.com\//i.test(raw);
  if (looksLikeInstagramUrl) {
    try { parsed = new URL(/^https?:\/\//i.test(raw) ? raw : `https://${raw}`); }
    catch { return null; }
  } else if (raw.includes('://') || raw.includes('/') || raw.includes('?') || raw.includes('#')) {
    return null;
  }

  if (!parsed) return cleanInstagramHandle(raw);
  if (!['http:', 'https:'].includes(parsed.protocol)) return null;
  const host = parsed.hostname.toLowerCase().replace(/^www\./, '');
  if (host !== 'instagram.com' && !host.endsWith('.instagram.com')) return null;
  let parts;
  try { parts = parsed.pathname.split('/').filter(Boolean).map(part => decodeURIComponent(part)); }
  catch { return null; }
  const profileParts = parts[0]?.toLowerCase() === '_u' ? parts.slice(1) : parts;
  if (profileParts.length !== 1) return null;
  return cleanInstagramHandle(profileParts[0]);
}

export function instagramDmUrl(value) {
  const handle = normalizeInstagramHandle(value);
  return handle ? `https://ig.me/m/${encodeURIComponent(handle)}` : null;
}

export function normalizeGoogleMapsUrl(value) {
  if (typeof value !== 'string' || !value.trim()) return null;
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:') return null;
    const host = url.hostname.toLowerCase().replace(/^www\./, '');
    const canonical = (host === 'google.com' || host.endsWith('.google.com'))
      && url.pathname.startsWith('/maps/');
    const shortLink = host === 'maps.app.goo.gl' && url.pathname.length > 1;
    return canonical || shortLink ? url.href : null;
  } catch {
    return null;
  }
}
