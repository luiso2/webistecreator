import { DurableObject } from 'cloudflare:workers';
import { OutreachEngine } from './outreach-engine.mjs';

export class OutreachCampaign extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.engine = new OutreachEngine(ctx.storage, env);
  }
  status() { return this.engine.status(); }
  salesList() { return this.engine.salesList(); }
  salesSave(input) { return this.engine.salesSave(input); }
  salesHistory(slug) { return this.engine.salesHistory(slug); }
  inbox(threadId) { return this.engine.inbox(threadId); }
  readReply(input) { return this.engine.readReply(input); }
  configure(input) { return this.engine.config(input); }
  consent(input) { return this.engine.consent(input); }
  event(input) { return this.engine.event(input); }
  run(slug) { return this.engine.run(slug); }
  unsubscribe(token, apply) { return this.engine.unsubscribe(token, apply); }
  telnyxEvent(event) { return this.engine.telnyxEvent(event); }
}
