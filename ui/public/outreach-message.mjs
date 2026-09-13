// Preserve paragraph boundaries: deleting LF used to turn `<demo>/\n\nIt` into `/It`.
export function cleanMessage(value, max = 1200) {
  return String(value ?? '').replace(/\r\n?/g, '\n')
    .replace(/[<>\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '').slice(0, max);
}

export function repairDemoSeparator(message, demoUrl) {
  const text = cleanMessage(message);
  if (!demoUrl || !/^https:\/\/siteforge-demos\.odd-forest-9504\.workers\.dev\/[a-z0-9-]+\/$/.test(demoUrl)) return text;
  // Only repair a known URL immediately followed by prose; leave genuine page links alone.
  return text.split(demoUrl).map((part, index) => index && /^(?:It\b|No\b|Would\b|Le\b|Este\b|Esta\b|¿)/.test(part)
    ? '\n\n' + part : part).join(demoUrl);
}
