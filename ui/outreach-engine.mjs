import { DEFAULT_CONFIG, eligibility, emailKey, validEmail, validPhone, phoneMatches, smsReady, smsOpener, opener, verifyDemo } from './outreach-policy.mjs';
import { businessIdentityKeys } from './control-plane.mjs';
import { validateSales, validSlug } from './public/sales.mjs';

const hash = async text => [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text)))].map(b => b.toString(16).padStart(2, '0')).join('');
const iso = () => new Date().toISOString();

// One coordinator for this bounded 20/day pilot. Durable state, never an in-memory send log.
export class OutreachEngine {
  constructor(storage, env, fetcher = fetch) {
    this.storage = storage;
    this.env = env;
    this.fetcher = fetcher;
    this.running = null;
  }

  async config(input) {
    if (input) {
      if (typeof input.enabled !== 'boolean' || !Number.isInteger(input.dailyLimit)
          || input.dailyLimit < 1 || input.dailyLimit > 20) throw new Error('invalid_config');
      await this.storage.put('config', { ...DEFAULT_CONFIG, enabled: input.enabled, dailyLimit: input.dailyLimit });
    }
    return await this.storage.get('config') || DEFAULT_CONFIG;
  }

  async salesList() {
    const [records, sends] = await Promise.all([this.storage.list({ prefix: 'sales:' }), this.storage.list({ prefix: 'send:' })]);
    const sales = Object.fromEntries([...records].map(([key, value]) => [key.slice(6), value]));
    const delivery = {};
    for (const s of sends.values()) if (!delivery[s.slug] || s.at > delivery[s.slug].at) {
      delivery[s.slug] = { status: s.status, delivery: s.delivery || null, at: s.at, channel: s.channel || 'email', source: 'provider' };
    }
    return { sales, delivery };
  }

  async salesSave(input) {
    const record = validateSales(input);
    const registry = await this.env.SITEFORGE_KV.get('registry', 'json') || [];
    const biz = registry.find(b => b.slug === record.slug);
    if (!biz) throw new Error('unknown_business');
    const at = iso();
    return this.storage.transaction(async tx => {
      const key = `sales:${record.slug}`;
      const previous = await tx.get(key);
      if ((previous?.revision || 0) !== input.revision) return { ok: false, conflict: true };
      // Opt-outs cannot be undone by a sales edit; permission has a separate audited flow.
      if (previous?.stage === 'opted_out' && record.stage !== 'opted_out') throw new Error('recipient_suppressed');
      const next = { ...record, at, identities: businessIdentityKeys(biz), revision: input.revision + 1, source: 'operator_attested' };
      await tx.put(key, next);
      await tx.put(`sales-history:${record.slug}:${String(next.revision).padStart(10, '0')}`, next);
      return { ok: true, record: next };
    });
  }

  async salesHistory(slug) {
    if (!validSlug(slug)) throw new Error('invalid_slug');
    return [...(await this.storage.list({ prefix: `sales-history:${slug}:`, reverse: true, limit: 30 })).values()];
  }

  async consent(input) {
    const channel = input.channel || 'email';
    if (!['email', 'sms'].includes(channel) || !/^[a-z0-9-]{1,40}$/.test(input.slug || '')
        || (channel === 'email' ? !validEmail(input.email) : !validPhone(input.phone))
        || input.confirmed !== true || !['inbound_request', 'double_opt_in'].includes(input.source)
        || typeof input.evidence !== 'string' || input.evidence.trim().length < 12 || input.evidence.length > 1000) {
      throw new Error('explicit_permission_evidence_required');
    }
    const email = channel === 'email' ? emailKey(input.email) : undefined;
    const phone = channel === 'sms' ? input.phone : undefined;
    const key = await hash(channel === 'email' ? email : `sms:${phone}`);
    if (await this.storage.get(`suppress:${key}`)) throw new Error('recipient_suppressed');
    const record = { slug: input.slug, channel, ...(email ? { email } : { phone }), source: input.source, evidence: input.evidence.trim(), at: iso() };
    await this.storage.put(`consent:${channel}:${input.slug}`, record);
    return { ok: true, slug: input.slug, at: record.at };
  }

  async event(input) {
    if ((!validEmail(input.email) && !validPhone(input.phone)) || !['replied', 'declined', 'client', 'unsubscribed'].includes(input.type)
        || typeof input.evidence !== 'string' || input.evidence.trim().length < 12 || input.evidence.length > 1000
        || input.confirmed !== true) throw new Error('verified_event_required');
    const key = await hash(validEmail(input.email) ? emailKey(input.email) : `sms:${input.phone}`);
    const record = { type: input.type, at: iso(), evidence: input.evidence.trim() };
    await this.storage.put(`suppress:${key}`, record);
    await this.storage.put(`event:${key}`, record);
    return { ok: true, type: record.type };
  }

  async unsubscribe(token, apply = false) {
    if (!/^[a-f0-9]{64}$/.test(token || '')) return false;
    const key = await this.storage.get(`token:${token}`);
    if (!key) return false;
    if (apply) await this.storage.put(`suppress:${key}`, { type: 'unsubscribed', at: iso() });
    return true;
  }

  async inbox(threadId) {
    const registry = (await this.env.SITEFORGE_KV.get('registry', 'json')) || [];
    const replies = await this.storage.list({ prefix: 'reply:' });
    const threads = [...replies.entries()].map(([key, reply]) => {
      const matches = registry.filter(b => reply.phone && phoneMatches(b.phone, reply.phone));
      const biz = matches.length === 1 ? matches[0] : null;
      return { id: key.slice(6), ...reply, slug: biz?.slug || reply.slug || null, name: biz?.name || null,
        language: biz?.language || null, matched: Boolean(biz || reply.slug) };
    }).sort((a, b) => b.at.localeCompare(a.at));
    if (threadId !== undefined) {
      if (!/^[a-f0-9]{64}$/.test(threadId)) throw new Error('invalid_thread');
      const thread = threads.find(t => t.id === threadId);
      if (!thread) return { thread: null, messages: [] };
      const rows = await this.storage.list({ prefix: `message:${threadId}:`, reverse: true, limit: 50 });
      return { thread, messages: [...rows.values()].sort((a, b) => a.at.localeCompare(b.at)).slice(-50) };
    }
    return { threads: threads.slice(0, 50), total: threads.length, unread: threads.filter(t => t.readEventId !== t.eventId).length };
  }

  async readReply(input) {
    if (!/^[a-f0-9]{64}$/.test(input?.threadId || '') || typeof input.eventId !== 'string') throw new Error('invalid_thread');
    return this.storage.transaction(async tx => {
      const key = `reply:${input.threadId}`;
      const reply = await tx.get(key);
      if (!reply || reply.eventId !== input.eventId) return { ok: false, reason: 'new_reply_received' };
      await tx.put(key, { ...reply, readEventId: input.eventId });
      return { ok: true };
    });
  }

  async notifyReplies() {
    if (!this.env.RESEND_API_KEY) return { reason: 'email_provider_required' };
    const notices = await this.storage.list({ prefix: 'notice:' });
    if ([...notices.values()].filter(n => n.at.startsWith(iso().slice(0, 10))).length >= 20) return { reason: 'owner_alert_daily_limit' };
    const inbox = await this.inbox();
    // A first reply from a known lead warrants an owner alert, not another cold pitch.
    // Unknown inbound senders are visible in the inbox but cannot trigger email floods.
    for (const reply of inbox.threads.filter(t => t.matched && t.type === 'replied' && t.readEventId !== t.eventId)) {
      const noticeKey = `notice:${reply.id}`;
      if (await this.storage.get(noticeKey)) continue;
      const reserved = await this.storage.transaction(async tx => {
        if (await tx.get(noticeKey)) return false;
        await tx.put(noticeKey, { status: 'sending', at: iso(), eventId: reply.eventId });
        return true;
      });
      if (!reserved) continue;
      try {
        const response = await this.fetcher('https://api.resend.com/emails', {
          method: 'POST', signal: AbortSignal.timeout(8000),
          headers: { authorization: `Bearer ${this.env.RESEND_API_KEY}`, 'content-type': 'application/json', 'Idempotency-Key': `siteforge-reply-alert-${reply.id}` },
          body: JSON.stringify({ from: 'Siteforge | Merktop <jose@merktop.com>', to: ['jose@merktop.com'],
            subject: 'Siteforge: un negocio respondió',
            // Keep phone, SMS body and other private conversation data inside the authenticated panel.
            text: 'Hay una nueva respuesta de un negocio en la bandeja de Siteforge. Revísala en https://siteforge-panel.odd-forest-9504.workers.dev/#outreachInbox. Una respuesta no implica que se haya cerrado una venta.' }),
        });
        const data = await response.json().catch(() => ({}));
        await this.storage.put(noticeKey, { status: response.ok && data.id ? 'accepted' : 'needs_review', providerId: data.id || null, at: iso(), eventId: reply.eventId });
      } catch { await this.storage.put(noticeKey, { status: 'needs_review', at: iso(), eventId: reply.eventId }); }
      return { notified: reply.id }; // At most one owner alert per cron, once per conversation.
    }
    return { notified: null };
  }

  async snapshot() {
    const [registry, crm, legacyLog, consents, sends, suppressed, sales] = await Promise.all([
      this.env.SITEFORGE_KV.get('registry', 'json'), this.env.SITEFORGE_KV.get('crm', 'json'),
      this.env.SITEFORGE_KV.get('sent_log', 'json'), this.storage.list({ prefix: 'consent:' }),
      this.storage.list({ prefix: 'send:' }), this.storage.list({ prefix: 'suppress:' }),
      this.storage.list({ prefix: 'sales:' }),
    ]);
    const contacted = (registry || []).filter(b => b.outreach === 'sent' || legacyLog?.[b.slug]);
    const already = new Set(contacted.filter(b => b.email).map(b => emailKey(b.email)));
    const identities = new Set(contacted.flatMap(businessIdentityKeys));
    const sentSlugs = new Set([...sends.values()].map(s => s.slug));
    for (const s of sends.values()) for (const id of s.identities || []) identities.add(id);
    const candidates = [];
    const reasons = {};
    const salesIdentities = new Set((registry || []).filter(b => sales.get(`sales:${b.slug}`)?.stage && sales.get(`sales:${b.slug}`).stage !== 'new').flatMap(businessIdentityKeys));
    for (const raw of registry || []) {
      const commercial = sales.get(`sales:${raw.slug}`);
      const biz = { ...raw, sales: commercial, language: commercial?.language || raw.language };
      const smsConsent = consents.get(`consent:sms:${biz.slug}`);
      const emailConsent = consents.get(`consent:email:${biz.slug}`);
      const channel = emailConsent && this.env.RESEND_API_KEY ? 'email' : smsConsent ? 'sms' : 'email';
      const consent = channel === 'email' ? emailConsent : smsConsent;
      const key = await hash(channel === 'email' ? emailKey(biz.email) : `sms:${consent?.phone}`);
      const alternate = channel === 'email' && smsConsent?.phone ? await hash(`sms:${smsConsent.phone}`)
        : channel === 'sms' && validEmail(biz.email) ? await hash(emailKey(biz.email)) : null;
      let reason = eligibility(biz, {
        crm: crm?.[biz.slug], consent, channel,
        suppressed: suppressed.has(`suppress:${key}`) || (alternate && suppressed.has(`suppress:${alternate}`)), sent: already.has(emailKey(biz.email)) || sends.has(`send:${key}`)
          || sentSlugs.has(biz.slug) || businessIdentityKeys(biz).some(id => identities.has(id)),
      });
      if (businessIdentityKeys(biz).some(id => salesIdentities.has(id))) reason = 'sales_conversation_active';
      if (!reason && channel === 'sms' && !smsReady(this.env)) reason = 'telnyx_setup_required';
      if (!reason && channel === 'email' && !this.env.RESEND_API_KEY) reason = 'email_provider_required';
      if (reason) reasons[reason] = (reasons[reason] || 0) + 1;
      else candidates.push({ biz, key, channel, recipient: channel === 'email' ? emailKey(biz.email) : consent.phone });
    }
    return { candidates, reasons, sends: [...sends.values()], total: (registry || []).length };
  }

  async status() {
    const [state, config, lastRun, events, replies, notices] = await Promise.all([
      this.snapshot(), this.config(), this.storage.get('lastRun'), this.storage.list({ prefix: 'event:' }), this.storage.list({ prefix: 'reply:' }), this.storage.list({ prefix: 'notice:' }),
    ]);
    return {
      config, provider: this.env.RESEND_API_KEY ? 'resend' : null,
      channels: { email: !!this.env.RESEND_API_KEY, sms: smsReady(this.env), whatsapp: false },
      telnyx: { keyConfigured: !!this.env.TELNYX_API_KEY, numberConfigured: validPhone(this.env.TELNYX_FROM_NUMBER),
        profileConfigured: !!this.env.TELNYX_MESSAGING_PROFILE_ID, webhookKeyConfigured: !!this.env.TELNYX_PUBLIC_KEY,
        registrationApproved: this.env.TELNYX_SMS_APPROVED === 'true' },
      automaticReplies: false, automaticFollowups: false,
      inboundSMS: !!this.env.TELNYX_PUBLIC_KEY,
      repliesReceived: replies.size,
      unreadReplies: [...replies.values()].filter(r => r.readEventId !== r.eventId).length,
      ownerAlertsAccepted: [...notices.values()].filter(n => n.status === 'accepted').length,
      ownerAlertsNeedReview: [...notices.values()].filter(n => n.status !== 'accepted').length,
      total: state.total, eligible: state.candidates.length, blocked: state.reasons,
      accepted: state.sends.filter(s => s.providerId).length,
      delivered: state.sends.filter(s => s.delivery === 'delivered').length,
      needsReview: state.sends.filter(s => ['sending', 'uncertain', 'rejected'].includes(s.status)).length,
      confirmedClients: [...events.values()].filter(e => e.type === 'client').length,
      lastRun: lastRun || null,
      recent: state.sends.sort((a, b) => b.at.localeCompare(a.at)).slice(0, 20)
        .map(({ slug, status, delivery, at, reason }) => ({ slug, status, delivery, at, reason })),
    };
  }

  async reconcileDelivery() {
    const sends = await this.storage.list({ prefix: 'send:' });
    const pending = [...sends.entries()].filter(([, s]) => s.channel !== 'sms' && s.providerId && !['bounced', 'complained', 'failed'].includes(s.delivery)
      && Date.now() - Date.parse(s.at) < 7 * 86400000 && Date.now() - Date.parse(s.polledAt || 0) > 3600000).slice(0, 2);
    for (const [key, s] of pending) {
      try {
        const response = await this.fetcher(`https://api.resend.com/emails/${encodeURIComponent(s.providerId)}`, {
          headers: { authorization: `Bearer ${this.env.RESEND_API_KEY}` }, signal: AbortSignal.timeout(5000),
        });
        const data = await response.json();
        if (!response.ok) continue;
        const delivery = String(data.last_event || 'sent').replace(/^email\./, '');
        await this.storage.put(key, { ...s, delivery, polledAt: iso() });
        if (['bounced', 'complained', 'failed'].includes(delivery)) {
          await this.storage.put(key.replace('send:', 'suppress:'), { type: delivery, at: iso() });
        }
      } catch { /* Accepted sends remain reserved even if status cannot be refreshed. */ }
    }
  }

  async run(slug) {
    if (this.running) return { ok: false, reason: 'already_running' };
    this.running = this.execute(slug);
    try { return await this.running; } finally { this.running = null; }
  }

  async execute(slug) {
    const config = await this.config();
    const finish = async result => {
      await this.storage.put('lastRun', { ...result, at: iso() });
      return result;
    };
    if (!config.enabled) return finish({ ok: false, reason: 'paused' });
    await this.notifyReplies();
    if (!this.env.RESEND_API_KEY && !smsReady(this.env)) return finish({ ok: false, reason: 'provider_not_configured' });
    if (this.env.RESEND_API_KEY) await this.reconcileDelivery();
    const state = await this.snapshot();
    const today = iso().slice(0, 10);
    if (state.sends.filter(s => s.at.startsWith(today)).length >= config.dailyLimit) return finish({ ok: false, reason: 'daily_limit' });
    let candidate;
    for (const item of state.candidates) {
      if (slug && item.biz.slug !== slug) continue;
      const cooldown = await this.storage.get(`qa:${item.biz.slug}`);
      if (!cooldown || Date.now() - cooldown.at >= 3600000) { candidate = item; break; }
    }
    if (!candidate) return finish({ ok: false, reason: 'no_eligible_candidates', blocked: state.reasons });
    const { biz, key, channel, recipient } = candidate;
    let qa;
    try { qa = await verifyDemo(biz, this.fetcher); }
    catch (error) {
      const reason = /^qa_/.test(error.message) ? error.message : 'qa_network_failure';
      await this.storage.put(`qa:${biz.slug}`, { at: Date.now(), reason });
      return finish({ ok: false, slug: biz.slug, reason });
    }
    // Refresh all suppression/CRM state after slow QA, immediately before reserving a send.
    if (!(await this.config()).enabled || !(await this.snapshot()).candidates.some(c => c.key === key && c.biz.slug === biz.slug)) {
      return finish({ ok: false, reason: 'eligibility_changed' });
    }
    const token = await hash(crypto.randomUUID() + crypto.randomUUID());
    const at = iso();
    const record = { slug: biz.slug, channel, identities: businessIdentityKeys(biz), status: 'sending', at, qa };
    const reserved = await this.storage.transaction(async tx => {
      if (await tx.get(`send:${key}`)) return false;
      const sales = await tx.list({ prefix: 'sales:' });
      if ([...sales.values()].some(s => s.stage !== 'new' && (s.slug === biz.slug || (s.identities || []).some(id => record.identities.includes(id))))) return false;
      await tx.put(`send:${key}`, record);
      await tx.put(`token:${token}`, key);
      return true;
    });
    if (!reserved) return finish({ ok: false, reason: 'already_reserved' });
    // Never automatically retry an ambiguous result, even after a crash / 24h provider expiry.
    const message = opener(biz, `https://siteforge-panel.odd-forest-9504.workers.dev/unsubscribe/${token}`);
    try {
      const response = await this.fetcher(channel === 'sms' ? 'https://api.telnyx.com/v2/messages' : 'https://api.resend.com/emails', {
        method: 'POST', signal: AbortSignal.timeout(10000),
        headers: { authorization: `Bearer ${channel === 'sms' ? this.env.TELNYX_API_KEY : this.env.RESEND_API_KEY}`, 'content-type': 'application/json', 'Idempotency-Key': `siteforge-pilot-v1-${key}` },
        body: JSON.stringify(channel === 'sms' ? {
          from: this.env.TELNYX_FROM_NUMBER, messaging_profile_id: this.env.TELNYX_MESSAGING_PROFILE_ID,
          to: recipient, text: smsOpener(biz), type: 'SMS',
          webhook_url: 'https://siteforge-panel.odd-forest-9504.workers.dev/webhooks/telnyx',
        } : { from: 'Michael | Merktop <jose@merktop.com>', reply_to: 'jose@merktop.com', to: [recipient], ...message,
          tags: [{ name: 'campaign', value: 'siteforge-permission-pilot' }] }),
      });
      const data = await response.json().catch(() => ({}));
      const providerId = channel === 'sms' ? data.data?.id : data.id;
      const explicitlyRejected = channel === 'sms' && (data.data?.errors?.length > 0
        || data.data?.to?.some(to => ['delivery_failed', 'sending_failed'].includes(to.status)));
      if (!response.ok || !providerId || explicitlyRejected) {
        const status = explicitlyRejected || (response.status >= 400 && response.status < 500) ? 'rejected' : 'uncertain';
        await this.storage.put(`send:${key}`, { ...record, status, reason: `provider_http_${response.status}` });
        return finish({ ok: false, slug: biz.slug, reason: status });
      }
      await this.storage.put(`send:${key}`, { ...record, status: 'accepted', providerId, delivery: 'sent' });
      if (channel === 'sms') {
        await this.storage.put(`provider:${providerId}`, key);
        const receipt = await this.storage.get(`receipt:${providerId}`);
        if (receipt) await this.telnyxEvent(receipt);
      }
      // Legacy panel projection is best-effort; durable send ledger remains authoritative.
      try { await this.env.QUEUE_CLAIMS.getByName('siteforge-queue').markOutreachSent(biz.slug, providerId, at, channel); }
      catch { /* A failed projection must never trigger a second send. */ }
      return finish({ ok: true, slug: biz.slug, channel, status: 'accepted', id: providerId });
    } catch {
      await this.storage.put(`send:${key}`, { ...record, status: 'uncertain', reason: 'provider_result_unknown' });
      return finish({ ok: false, slug: biz.slug, reason: 'provider_result_unknown' });
    }
  }

  async telnyxEvent(event) {
    if (!event || typeof event.id !== 'string' || event.id.length > 100 || !event.payload) throw new Error('invalid_event');
    const payload = event.payload;
    // Signature validated at HTTP boundary; account/profile/number still have to match.
    if (payload.messaging_profile_id !== this.env.TELNYX_MESSAGING_PROFILE_ID) return { ok: true, ignored: true };
    if (event.event_type === 'message.received') {
      if (!payload.to?.some(to => to.phone_number === this.env.TELNYX_FROM_NUMBER) || !validPhone(payload.from?.phone_number)) return { ok: true, ignored: true };
      const key = await hash(`sms:${payload.from.phone_number}`);
      const text = String(payload.text || '').trim().slice(0, 1600);
      const type = /^(?:stop|stopall|unsubscribe|cancel|end|quit|baja|no)\b/i.test(text) ? 'unsubscribed' : 'replied';
      const eventKey = await hash(event.id);
      const occurredAt = Date.parse(event.occurred_at);
      const at = Number.isFinite(occurredAt) ? new Date(occurredAt).toISOString() : iso();
      // Commit suppression, dedup marker, history and latest summary in one transaction.
      // Replayed or out-of-order webhooks must not lose messages or resurrect an opt-out.
      return this.storage.transaction(async tx => {
        if (await tx.get(`seen-inbound:${eventKey}`)) return { ok: true, duplicate: true };
        const previous = await tx.get(`reply:${key}`);
        const suppression = await tx.get(`suppress:${key}`);
        const record = { type, at, receivedAt: iso(), text, eventId: event.id, phone: payload.from.phone_number, channel: 'sms' };
        await tx.put(`seen-inbound:${eventKey}`, { at });
        await tx.put(`message:${key}:${at}:${eventKey}`, record);
        if (!suppression || suppression.type === 'replied' || type === 'unsubscribed') {
          await tx.put(`suppress:${key}`, { type, at });
        }
        if (!previous || at >= previous.at) {
          await tx.put(`reply:${key}`, { ...record, ...(previous?.readEventId ? { readEventId: previous.readEventId } : {}) });
        }
        return { ok: true };
      });
    }
    if (['message.sent', 'message.finalized'].includes(event.event_type)) {
      const key = await this.storage.get(`provider:${payload.id}`);
      if (!key) {
        // Telnyx may deliver its webhook before the POST response reaches this Worker.
        if (typeof payload.id === 'string' && payload.id.length <= 100) await this.storage.put(`receipt:${payload.id}`, event);
        return { ok: true, pending: true };
      }
      const s = await this.storage.get(`send:${key}`);
      const delivery = payload.to?.[0]?.status;
      if (s && ['delivered', 'sent', 'delivery_failed', 'delivery_unconfirmed'].includes(delivery)
          && !['delivered', 'delivery_failed', 'delivery_unconfirmed'].includes(s.delivery)) {
        await this.storage.put(`send:${key}`, { ...s, delivery, updatedAt: iso() });
      }
    }
    return { ok: true };
  }
}
