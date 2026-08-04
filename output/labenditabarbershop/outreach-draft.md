# Outreach draft: La Bendita Barbershop (labenditabarbershop)

- has_own_site: false (verified via Booksy dossier website_candidates = empty, plus two
  WebSearch passes for "La Bendita Barbershop" Miami Beach website/phone: only Booksy, Atly
  and Instagram listings found, no independent domain)
- email: not found (see notes below) -> outreach: pending_manual
- phone: not published (Booksy dossier phone field is null; not found via WebSearch either;
  no mailto/tel found anywhere public)
- demo link: https://siteforge-demos.odd-forest-9504.workers.dev/labenditabarbershop/
- language: en (Booksy reviews are majority English: 9 of 10 sampled reviews in English, 1 in
  Spanish; no clear Spanish majority, so default to English per pipeline rule)
- angle: has_own_site false -> "we built you a sample website"

## Email draft

Subject: A sample website for La Bendita Barbershop

Hi Valeria,

I came across La Bendita Barbershop on Booksy and saw the perfect 5.0 rating across 36
reviews, that's a strong track record for a Miami Beach barbershop. I put together a sample
website to show what it could look like beyond the Booksy listing:

https://siteforge-demos.odd-forest-9504.workers.dev/labenditabarbershop/

It's just a demo, it doesn't touch your real Booksy booking or client data at all. If you like
it, I can help put it on your own domain. If not, no problem at all, I'll take it down, no
obligation either way.

Let me know what you think.

Best,
Michael Vargas
Merktop

## dm_message (for Instagram DM / WhatsApp, ~450 char max)

Hi! I came across La Bendita Barbershop on Booksy, a perfect 5.0 across 36 reviews is a great
track record. I put together a sample website to show how it could look:
https://siteforge-demos.odd-forest-9504.workers.dev/labenditabarbershop/ It's just a demo,
doesn't touch your real Booksy booking. Happy to put it on your own domain if you like it, or
take it down, no obligation either way!
Michael, Merktop

(char count: 408)

## Notes on research attempts
- Booksy dossier (scripts/booksy_dossier.py) pulled name, address, geo, rating (5.0),
  reviews_count (36), hours, 1 staff member (Valeria Perez), Instagram handle (labenditav),
  13 services with prices/durations, 10 reviews (3 with author names), and 16 candidate
  photos. website_candidates was empty (no own-domain signal from Booksy).
- WebSearch for "La Bendita Barbershop" Miami Beach phone number / website: no independent
  domain found; one result (Atly listing) independently confirms the business "specializes in
  Afro hair", used to ground the Afro-hair-specialty angle in the site copy alongside the
  Men Hair Straightening and Perm/Curls/Waves menu items and the curl-texture photo.
- Email hunt: no email field in Booksy dossier data.json, no mailto: found via curl on the
  Booksy page HTML, no business_email available (IG web_profile_info and instagram.com/labenditav/
  both returned HTTP 429 rate limits on repeated attempts via WebFetch and curl). Conclusion:
  email null, outreach status pending_manual (contact via Instagram DM to @labenditav).
- Photo curation: Booksy dossier returned 16 candidate files; visual review (contact sheet)
  kept 5 real, high-quality finished-haircut photos (bk-3, bk-5, bk-6, bk-7, bk-8) for hero,
  experience and gallery, plus the owner's Booksy staff portrait (bk-4) reused ONLY as a small
  avatar in the experience section and footer, never in the gallery. Discarded: the business
  logo graphic, a cartoon/illustration image, a green placeholder-initial avatar, and five
  100x100px thumbnail-only images with no usable resolution, plus two low-relevance client
  headshot/portrait photos that did not show finished hair work.
- IG rescue attempt (scripts/ig_photos.py labenditav labenditabarbershop) ran successfully but
  returned mostly personal/fitness/lifestyle content from the owner's feed, not barbershop
  client work, and would have overwritten the good Booksy photos under the same bk-N filenames.
  Re-ran booksy_dossier.py to deterministically restore the original curated Booksy photo set
  before building.
