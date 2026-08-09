# Outreach Draft: Polynesian Tattoo (polynesian-tattoo-miramar)

Status: DRAFT ONLY. Not sent. Requires explicit user approval before send, per PIPELINE.md Fase 5.

- Sender: Michael Vargas <michael@go.merktop.com> (never merktop.com directly)
- Reply-to: jose@merktop.com
- Tag: campaign=siteforge
- To: no public email or phone found -> outreach: pending_manual, contact via Instagram DM (@polynesian_tatto0)
- Idempotency-Key: siteforge-polynesian-tattoo-miramar-2026-08-09
- Angle: has_own_site = false -> "we built you a sample website"
- Language: English (Miramar/Hollywood FL market, all reviews and business copy found in English)

---

**Subject:** A sample website for Polynesian Tattoo

Hi Jorge,

I found Polynesian Tattoo while looking at tattoo studios in Miramar: 4.9 stars from 38 reviews on Booksy is a great track record, and your Polynesian and Melanesian sleeve work is really striking. Since you don't have your own website, I built you a free sample using your real tattoo photos:

https://siteforge-demos.odd-forest-9504.workers.dev/polynesian-tattoo-miramar/

It does not touch anything about how you book today: the booking button goes straight to your real Booksy page, and everything on the site comes from your own Booksy listing and Instagram feed. Prices for the brow tattoo and microblading sessions are the ones you already publish on Booksy, and larger custom pieces still point people to book a consultation first, the same as now.

If you like it, I can help you put it on your own domain. If not, I will take it down, no hard feelings, just let me know.

Best,
Michael Vargas
Merktop
https://merktop.com

---

## DM message corto

Hi! This is Michael from Merktop. I found Polynesian Tattoo, saw your 4.9 rating from 38 Booksy reviews, and since you do not have your own website, I built you a free sample using your real tattoo photos: https://siteforge-demos.odd-forest-9504.workers.dev/polynesian-tattoo-miramar/ It does not change how you book today. Like it? We put it on your own domain. If not, I take it down, no hard feelings.

(character count: 404, within the 450 limit)

## Delivery note

No public email found and no phone published: the Booksy dossier (`data.json`) returned `"phone": null`, and no `website_candidates` were found on the listing. Re-verified with a fresh search for "Polynesian Tattoo" Jorge Ramirez Miramar/Hollywood FL website and by probing obvious domains: `polynesiantattoo.com` resolves but is a parked GoDaddy for-sale page, not a live business site, and no other candidate domain resolved. A separate "Jorge Ramirez" tattoo artist profile found on tattooswizard.com is a different person based in Frankfurt, Germany, unrelated to this business. Confirmed `has_own_site: false`.

Since there is no email or phone, outreach must go by Instagram DM to https://www.instagram.com/polynesian_tatto0/ (@polynesian_tatto0, 33K followers). No DM was sent per the hard rule against contacting the business during this build.

Rating and review note: 4.9 rating (4.894736842105263 raw) and 38 reviews are Booksy figures pulled directly via `scripts/booksy_dossier.py`, along with the 5 real services with prices/durations and 3 named verbatim reviews (Priya K., Jeff S., Peter B.) used as testimonials on the site.

Studio note: the address on Booksy, 2201 SW 101st Ave, Unit 4-206, Miramar, FL 33025, is a shared multi-artist studio suite. Rather than embed a generic map pin for a suite number, the site's location section uses a real studio photo instead, per FORGE-BRIEF's adapted-variant guidance for addresses that are not meaningfully mappable. The address text and a "get directions" link are still shown.

Photo note: the Booksy dossier alone returned only 1 usable photo (a mid-procedure shot with equipment in frame, which is excluded from the gallery per the visual curation rule). Re-running `ig_photos.py polynesian_tatto0` against the public Instagram profile (via the Railway photo service) returned 12 additional real photos, 11 of which passed visual curation as finished, healed tattoo results in good light.
