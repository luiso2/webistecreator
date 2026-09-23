import { STAGES, BENEFITS, OBJECTIONS, commercialMessage, salesStage } from './sales.mjs';
export function salesCard(b, esc) {
  const s=b.sales||{}, slug=esc(b.slug), stage=salesStage(b);
  const options=(values,selected)=>Object.entries(values).map(([key,label])=>`<option value="${key}" ${key===selected?'selected':''}>${esc(label)}</option>`).join('');
  const d=b.delivery_evidence;
  const delivery=d?`Proveedor (${d.channel}): ${d.status} · entrega: ${d.delivery||'sin confirmar'}`:'Sin confirmación de entrega del proveedor';
  const date=s.followupAt?new Date(Date.parse(s.followupAt)-new Date(s.followupAt).getTimezoneOffset()*60000).toISOString().slice(0,16):'';
  return `<details class="sales-card"><summary>Gestión comercial · ${esc(STAGES[stage])}</summary>
  <p class="hint">${esc(delivery)}. Abrir WhatsApp o copiar texto no acredita entrega.</p>
  <label>Estado<select id="sale-stage-${slug}">${options(STAGES,stage)}</select></label>
  <label>Canal<select id="sale-channel-${slug}">${options({email:'Email',whatsapp:'WhatsApp manual',sms:'SMS',dm:'Instagram',call:'Llamada',other:'Otro'},s.channel||'email')}</select></label>
  <label>Idioma confirmado<select id="sale-language-${slug}"><option value="">Seleccionar</option>${options({es:'Español',en:'English'},s.language||b.language)}</select></label>
  <label>Objetivo propuesto<select id="sale-benefit-${slug}">${options(Object.fromEntries(Object.entries(BENEFITS).map(([k,v])=>[k,v[0]])),s.benefit||'contact')}</select></label>
  <label>Observación verificada (opcional, en el idioma del cliente)<textarea id="sale-observation-${slug}" maxlength="240" rows="2">${esc(s.observation||'')}</textarea></label>
  <label>Objeción<select id="sale-objection-${slug}">${options(OBJECTIONS,s.objection||'none')}</select></label>
  <label>Seguimiento (hora local; no envía mensajes)<input id="sale-followup-${slug}" type="datetime-local" value="${esc(date)}"></label>
  <label>Evidencia / nota de la conversación<textarea id="sale-note-${slug}" maxlength="1000" rows="3" placeholder="Qué respondió, cuándo y dónde. Para una venta: referencia del acuerdo o pago.">${esc(s.note||'')}</textarea></label>
  <p class="hint">Guardar confirma que la nota es real. No concede consentimiento ni verifica un pago. Para cerrar o dar de baja, borra la fecha de seguimiento.</p>
  <button class="link-btn primary" onclick="saveSales('${slug}',this)">Guardar gestión</button>
  <button class="link-btn" onclick="salesHistory('${slug}')">Ver historial</button><div id="sale-history-${slug}" class="hint"></div>
  <div class="actions"><button class="link-btn" onclick="salesDraft('${slug}','intro')">Preparar presentación</button><button class="link-btn" onclick="salesDraft('${slug}','offer')">Propuesta US$600</button><button class="link-btn" onclick="salesDraft('${slug}','followup')">Preparar seguimiento</button></div>
  <p class="hint">Los borradores usan la gestión guardada. Revisa contenido y permiso del canal antes de enviar.</p>
  <textarea id="sale-draft-${slug}" rows="7" aria-label="Borrador comercial editable" hidden></textarea>
  <button class="link-btn" onclick="copySales('${slug}')">Copiar borrador revisado</button></details>`;
}
export function installSalesUI({getBiz,headers,render,notice,esc}) {
  const el=id=>document.getElementById(id);
  window.saveSales=async(slug,button)=>{
    button.disabled=true;
    try {
      const v=key=>el(`sale-${key}-${slug}`).value;
      const input={slug,revision:getBiz(slug).sales?.revision||0,stage:v('stage'),channel:v('channel'),language:v('language'),benefit:v('benefit'),observation:v('observation'),objection:v('objection'),note:v('note'),followupAt:v('followup')?new Date(v('followup')).toISOString():null,confirmed:true};
      if(['won','lost','opted_out'].includes(input.stage)&&!confirm('¿Confirmas este resultado con la evidencia escrita? No se enviarán mensajes desde esta acción.'))return;
      const r=await fetch('/api/outreach/sales',{method:'POST',headers:headers(),body:JSON.stringify(input)}),d=await r.json();
      if(!r.ok)throw new Error(r.status===409?'Otro cambio fue guardado: recarga antes de editar.':d.error);
      getBiz(slug).sales=d.record;render();notice('Gestión guardada. No se ha enviado ningún mensaje.');
    }catch(e){notice(e.message,false);}finally{button.disabled=false;}
  };
  window.salesDraft=(slug,kind)=>{try{const b=el(`sale-draft-${slug}`);b.value=commercialMessage(getBiz(slug),kind);b.hidden=false;}catch(e){notice(e.message,false);}};
  window.copySales=async slug=>{const b=el(`sale-draft-${slug}`);if(!b?.value||b.hidden)return notice('Prepara y revisa primero el borrador.',false);try{await navigator.clipboard.writeText(b.value);notice('Copiado; todavía no enviado.');}catch{b.focus();b.select();notice('Selecciona y copia el texto.',false);}};
  window.salesHistory=async slug=>{const box=el(`sale-history-${slug}`);box.textContent='Cargando…';try{const r=await fetch('/api/outreach/sales?slug='+encodeURIComponent(slug),{headers:headers()});if(!r.ok)throw new Error('No se pudo leer el historial.');const d=await r.json();box.innerHTML=d.history.map(h=>`<p><strong>${esc(STAGES[h.stage])}</strong> · ${esc(new Date(h.at).toLocaleString())}<br>${esc(h.note)}</p>`).join('')||'Sin eventos registrados.';}catch(e){box.textContent=e.message;}};
}
