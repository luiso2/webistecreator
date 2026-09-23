// Shared, deterministic commercial copy. No LLM, fabricated observations or sales claims.
export const STAGES = Object.freeze({ new: 'Sin conversación', contacted: 'Contacto manual registrado', replied: 'Respondió', interested: 'Interesado', proposal: 'Propuesta enviada', won: 'Venta confirmada', lost: 'No interesado', opted_out: 'No contactar' });
export const BENEFITS = Object.freeze({ contact: ['mostrar servicios y facilitar el contacto', 'show services and make it easy to get in touch'], quotes: ['presentar servicios para solicitar presupuesto', 'present services so visitors can request a quote'], booking: ['orientar al visitante hacia su canal de reservas', 'guide visitors to your booking channel'], menu: ['presentar el menú y los datos de contacto', 'present your menu and contact details'] });
export const OBJECTIONS = Object.freeze({ none: 'Sin objeción registrada', price: 'Precio', timing: 'No es el momento', trust: 'Confianza', no_need: 'No lo necesita', existing_site: 'Ya tiene web', other: 'Otra' });
export const validSlug = s => typeof s === 'string' && /^[a-z0-9-]{1,40}$/.test(s);
const own = (o, k) => Object.hasOwn(o, k);
const clean = v => String(v || '').replace(/[<>\x00-\x1f\x7f]/g, ' ').trim();
export function validateSales(input) {
  if (!input || !validSlug(input.slug) || !Number.isInteger(input.revision) || input.revision < 0
    || !own(STAGES, input.stage) || !own(BENEFITS, input.benefit) || !own(OBJECTIONS, input.objection)
    || !['email','whatsapp','sms','dm','call','other'].includes(input.channel)
    || !['en','es'].includes(input.language) || input.confirmed !== true) throw new Error('invalid_sales_record');
  if (typeof input.note !== 'string' || input.note.trim().length < 12 || input.note.length > 1000
    || typeof input.observation !== 'string' || input.observation.length > 240) throw new Error('evidence_required');
  const followupAt = input.followupAt || null;
  if (followupAt && (typeof followupAt !== 'string' || !Number.isFinite(Date.parse(followupAt))
    || Date.parse(followupAt) < Date.now() - 60000 || Date.parse(followupAt) > Date.now() + 366 * 86400000)) throw new Error('invalid_followup');
  if (['won','lost','opted_out'].includes(input.stage) && followupAt) throw new Error('closed_followup');
  return { slug: input.slug, stage: input.stage, benefit: input.benefit, objection: input.objection,
    language: input.language, channel: input.channel, note: clean(input.note), observation: clean(input.observation),
    followupAt: followupAt ? new Date(followupAt).toISOString() : null };
}
export function salesStage(b) {
  if (b.sales?.stage === 'opted_out') return 'opted_out';
  // Historical closed outcomes remain authoritative until reconciled explicitly.
  if (b.crm_status === 'client') return 'won';
  if (b.crm_status === 'declined') return 'lost';
  return b.sales?.stage || (b.crm_status === 'contacted' || b.outreach === 'sent' ? 'contacted' : 'new');
}
export function salesPriority(b, now = Date.now()) {
  const stage = salesStage(b);
  if (['won','lost','opted_out'].includes(stage)) return 9;
  if (b.sales?.followupAt && Date.parse(b.sales.followupAt) <= now) return 0;
  return ({ interested: 1, replied: 2, proposal: 3, contacted: 5, new: 6 })[stage] ?? 6;
}
export function commercialMessage(b, kind = 'intro') {
  const language = b.sales?.language || b.language;
  if (!['en','es'].includes(language)) throw new Error('Confirma el idioma antes de preparar el mensaje.');
  if (!['intro','offer','followup'].includes(kind)) throw new Error('invalid_message_kind');
  const en = language === 'en', s = b.sales || {}, stage = salesStage(b);
  if (['won','lost','opted_out'].includes(stage)) throw new Error('Contacto cerrado: no se prepara otro mensaje comercial.');
  if (kind !== 'intro' && !['contacted','replied','interested','proposal'].includes(stage)) throw new Error('Registra primero la conversación real.');
  if (!/^https:\/\/siteforge-demos\.odd-forest-9504\.workers\.dev\/[a-z0-9-]+\/$/.test(b.url_demo || '')) throw new Error('Demo válida requerida.');
  const name = clean(b.name), benefit = BENEFITS[s.benefit || 'contact'] || BENEFITS.contact;
  const observation = clean(s.observation);
  const intro = en ? `Hi ${name}, I’m Michael from Merktop.` : `Hola ${name}, soy Michael de Merktop.`;
  const body = kind === 'offer'
    ? (en ? 'The proposal is US$600, including the domain and maintenance for one year. Before you decide, we will agree on the scope of maintenance and the renewal price after year one.' : 'La propuesta es de US$600 e incluye dominio y mantenimiento durante un año. Antes de decidir, acordaremos el alcance del mantenimiento y el precio de renovación después del primer año.')
    : kind === 'followup'
      ? (en ? 'Following up on our conversation about your website concept. If now is not the right time, let me know and I will close the follow-up.' : 'Retomo nuestra conversación sobre la propuesta de web. Si ahora no es el momento, dímelo y cierro el seguimiento.')
      : (en ? `I prepared a website concept for ${name}. The proposed goal is to ${benefit[1]}.` : `Preparé un concepto de web para ${name}. El objetivo propuesto es ${benefit[0]}.`);
  const question = kind === 'offer' ? (en ? 'What would you change before moving forward?' : '¿Qué cambiarías antes de avanzar?')
    : kind === 'followup' ? (en ? 'Is your main question about the price, the content, or the timing?' : '¿Tu principal duda es el precio, el contenido o el momento?')
    : (en ? 'Would something like this be useful for your business?' : '¿Algo así sería útil para tu negocio?');
  return [intro, observation, body, b.url_demo,
    en ? 'This is a demo, with no obligation and no changes to your domain.' : 'Es una demo, sin compromiso y sin cambios en tu dominio.', question, 'Michael — Merktop'].filter(Boolean).join('\n\n');
}
