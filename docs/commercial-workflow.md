# Commercial workflow

The panel now separates operator-attested sales outcomes from provider delivery
receipts. Historical CRM data is retained; no historical contact is reclassified
as delivered or converted. Existing closed CRM outcomes retain precedence until
explicitly reopened in the legacy CRM. A recorded opt-out always takes precedence.

## Operator flow

1. Search by business and use **Prioridad comercial**: warm conversations, due
   follow-ups, new leads or closed records. Due follow-ups and interested leads
   are listed ahead of new leads. This is a worklist, not an automatic send queue.
2. Open **Gestión comercial**, confirm the language and channel, choose a proposed
   benefit, and add only a verified observation in the recipient's language.
3. Record the actual reply/objection, its evidence and the next follow-up date.
   Local date entry is converted to UTC. Closing a lead requires clearing its date.
4. Prepare an intro, the approved US$600 offer, or a follow-up. Review and copy it
   for an eligible channel. Preparing/copying never marks a message sent.
5. Record proposal or sale only with real evidence. A requested price is interest,
   not payment. Renewal price and maintenance scope remain to be agreed; the
   template does not invent either or promise a particular domain is available.

The automatic email opener and new manual drafts share deterministic bilingual
copy. Existing operator-edited manual text is preserved. The manual text editor
does not change automatic email content, and now explicitly says so. Unknown
languages require confirmation instead of silently defaulting to Spanish.

## Persistence and permissions

- Authenticated `GET /api/outreach/sales` returns records and provider receipt
  summaries. `?slug=...` returns the latest 30 history entries.
- Authenticated `POST /api/outreach/sales` validates an 8 KiB bounded body,
  exact registry slug, revision, stage, language, channel, benefit, objection,
  observation, evidence note and follow-up date. `confirmed: true` attests evidence.
- Existing campaign Durable Object stores `sales:<slug>` and append-only
  `sales-history:<slug>:<revision>` atomically. Stale updates return 409. No binding
  or destructive migration is required. Records survive registry synchronization.
- A non-new sales conversation blocks automatic first contact across known
  business identity aliases. The guard is checked again in send reservation.
- Opt-out cannot be cleared through a sales edit. Consent/provider readiness
  checks remain separate and are never granted by a CRM edit.
- Editing an open sales form pauses the panel's timed refresh to preserve inputs.

## Limits that remain explicit

This release does not connect the email inbox, WhatsApp Business API, automatic
follow-up sending, click analytics, or payment reconciliation. SMS replies remain
in the existing verified inbox; record the commercial outcome after reviewing
them. Manual WhatsApp/email conversations must be entered with evidence. No
customer records or real outreach messages are created by tests or deployment.

Tests: `node --test ui/sales.test.mjs ui/outreach.test.mjs
ui/outreach-runtime.test.mjs ui/control-plane.test.mjs ui/social-channels.test.mjs`.
Browser QA uses an isolated local fixture, not the production ledger.
