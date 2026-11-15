# Outreach Draft: Barking Lot Mobile Pet Grooming (barking-lot-mobile-pet-grooming)

Status: DRAFT ONLY. Not sent. Requires explicit user approval before send, per PIPELINE.md Fase 5.
No channel was contacted to produce this draft or this demo.

- Sender: Michael Vargas <michael@go.merktop.com> (never merktop.com directly)
- Reply-to: jose@merktop.com
- Tag: campaign=siteforge
- To: no public email found (see delivery note below)
- Idempotency-Key: siteforge-barking-lot-mobile-pet-grooming-2026-11-15
- Angle: has_own_site = false -> "we built you a free sample website"
- Language: English (site/registry language = en; Clearwater, FL market, reviews and the van's own signage are in English)

---

## No email draft included

No public email address was found for this business after web searches (business name + Clearwater, + Facebook, + Instagram, + Edina) and after checking the one domain tied to the business (thebarkinglotspa.com, printed on the van itself), which is an expired/parked GoDaddy domain with no content and no contact page. No Facebook or Instagram page was found either. Per PIPELINE.md Fase 5, outreach is registered as `pending_manual` with phone only; only the `dm_message` below is prepared, for a manual call/text by the user.

## dm_message (for the panel's DM/WhatsApp button / manual text, max 450 characters)

Hi! This is Michael from Merktop. I found Barking Lot Mobile Pet Grooming, saw your 4.5 rating from 24 reviews on Google, and since your site is an expired domain, I built a free sample website with your real photos: https://siteforge-demos.odd-forest-9504.workers.dev/barking-lot-mobile-pet-grooming/ Does not change how you work today. Like it? We put it on your domain. If not, I take it down.

(character count: 396, within the 450 limit)

## Delivery / verification notes

- **Phone**: (727) 657-3038 / tel:+17276573038, confirmed both by the task brief and independently by the business's own van signage photo ("THE BARKING LOT · 727-657-3038 · MOBILE PET GROOMING"), and by a MapQuest directory listing for "The Barking Lot" (also known as "The Barking Lot Mobile Pet Grooming") in Clearwater, FL.
- **Own-website check (PIPELINE.md Fase 1 punto 2)**: the van's own signage prints the URL `www.thebarkinglotspa.com`. Fetched with a Chrome UA via curl: the domain resolves (HTTP 200) but the page body is only a redirect script to `/lander`, which serves a GoDaddy parked-domain page (`window._trfd.push({ap:"parking"})`, cookies `lander_type=parkweb` and `traffic_target=gd`, zero business content). This is an expired/lapsed domain, not an active own website, so `has_own_site: false` stands and the "free sample website" angle applies.
- **Social**: no Facebook or Instagram page found after multiple targeted searches. `ig: null`.
- **Hours**: Tuesday to Saturday, 9 AM to 6 PM; closed Sunday and Monday (as given in the task brief; used in the site's service-area section and JSON-LD).
- **Address**: none used anywhere on the demo or in this draft. The business is mobile/service-area only; a "Service area: Clearwater, FL and the surrounding area" block replaces any map/address section, per the adapted-variant pattern (no fixed storefront, so no address is fabricated).
- **Reviews**: the 5 verbatim Google reviews supplied in the task brief (Krista "KnG" Vickery, Sarah Black, Lauren The Lady, Andrea Merritt, Laura Simmons), trimmed at the last complete sentence before any truncation/ellipsis, are shown verbatim with author name and 5 stars in the site's testimonial grid.
