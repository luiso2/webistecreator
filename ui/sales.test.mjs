import test from 'node:test';
import assert from 'node:assert/strict';
import { validateSales, commercialMessage, salesPriority, salesStage } from './public/sales.mjs';
import { salesCard } from './public/sales-ui.mjs';
const biz={slug:'shop',name:'Shop',language:'es',url_demo:'https://siteforge-demos.odd-forest-9504.workers.dev/shop/'};
const input={slug:'shop',revision:0,stage:'interested',channel:'email',language:'es',benefit:'quotes',objection:'price',note:'Respondió preguntando precio; referencia de correo.',observation:'',followupAt:null,confirmed:true};
test('sales validates evidence, enums, dates, slug and explicit confirmation',()=>{
  assert.equal(validateSales(input).stage,'interested');
  for(const patch of [{slug:'../x'},{stage:'__proto__'},{benefit:'constructor'},{revision:-1},{confirmed:false},{note:'x'},{language:'auto'},{followupAt:'bad'},{followupAt:'2020-01-01'},{stage:'lost',followupAt:new Date(Date.now()+86400000).toISOString()}]) assert.throws(()=>validateSales({...input,...patch}));
});
test('messages use explicit locale, selected benefit, agreed price and no invented observation',()=>{
  const b={...biz,sales:input};
  assert.match(commercialMessage(b),/solicitar presupuesto/);
  assert.match(commercialMessage(b,'offer'),/US\$600/);
  assert.match(commercialMessage(b,'offer'),/renovación/);
  assert.match(commercialMessage({...b,sales:{...input,language:'en'}},'offer'),/one year/);
  assert.doesNotMatch(commercialMessage(b),/no vi|no website|garantiz/i);
  assert.throws(()=>commercialMessage({...biz,language:'unknown'}));
  assert.throws(()=>commercialMessage(biz,'followup'));
  assert.throws(()=>commercialMessage({...b,sales:{...input,stage:'opted_out'}}));
  assert.throws(()=>commercialMessage({...b,url_demo:'https://evil.example'}));
});
test('priorities favor due and warm conversations, not closed records',()=>{
  assert.equal(salesPriority({...biz,sales:{...input,followupAt:'2020-01-01'}}),0);
  assert.ok(salesPriority({...biz,sales:input})<salesPriority(biz));
  assert.equal(salesPriority({...biz,sales:{...input,stage:'lost',followupAt:'2020-01-01'}}),9);
  assert.equal(salesStage({...biz,crm_status:'client',sales:input}),'won');
});
test('UI explicitly distinguishes prepared, manual and provider status; escapes notes',()=>{
  const escape=s=>String(s??'').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
  const html=salesCard({...biz,sales:{...input,note:'<script>alert(1)</script>'}},escape);
  assert.match(html,/Sin confirmación de entrega/);
  assert.match(html,/WhatsApp manual/);
  assert.doesNotMatch(html,/<script>/);
});
