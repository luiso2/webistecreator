# Outreach draft: Blading BAE (bladingbaebrandon)

- has_own_site: false (verified via web search + Booksy sameAs, no independent domain found)
- email: not found (see notes below) -> outreach: pending_manual
- phone: (813) 666-5038 (found stamped on a promotional tattoo photo in the Booksy gallery, "To
  book 813-666-5038", cross-referenced against Groupon/Haircutnow listings for Blading BAE's
  Tampa location; the Brandon Booksy listing itself does not publish a phone number, and this
  operator has at least two locations, so spot-check this number belongs to Brandon before using
  it in a live send)
- demo link: https://siteforge-demos.odd-forest-9504.workers.dev/bladingbaebrandon/
- language: en
- angle: has_own_site false -> "we built you a sample website"

## Email draft (for manual send if an email is ever found, or for IG/WhatsApp follow-up as a longer message)

Subject: A sample website for Blading BAE

Hi Robertson,

I came across Blading BAE on Booksy and saw the 5.0 rating across 77 reviews, that's a serious
track record for microblading and brow work. I put together a sample website to show what it
could look like beyond the Booksy listing:

https://siteforge-demos.odd-forest-9504.workers.dev/bladingbaebrandon/

It's just a demo, it doesn't touch your real booking or client data at all. If you like it, I can
help put it on your own domain. If not, no problem at all, I'll take it down, no obligation either way.

Let me know what you think.

Best,
Michael Vargas
Merktop

## dm_message (for Instagram DM / WhatsApp, ~450 char max)

Hi! I came across Blading BAE on Booksy, 5.0 rating across 77 reviews is a great track record for
microblading and brow work. I put together a sample website for you to see how it could look:
https://siteforge-demos.odd-forest-9504.workers.dev/bladingbaebrandon/
It's just a demo, doesn't touch your real booking. Happy to put it on your own domain if you like
it, or take it down, no obligation either way. Let me know what you think!
Michael, Merktop

(char count: ~403)

## Notes on research attempts
- data.json (Booksy dossier) returned phone: null for the Brandon listing; no email field.
- WebFetch on instagram.com/bladingbae/: returned HTTP 429 (rate limited), no bio/link text
  retrieved.
- WebFetch on facebook.com/bladingbae/: page required login, no About/contact info retrievable
  without authentication.
- WebSearch for "Blading BAE" Brandon FL email contact Robertson Fleurine: surfaced a second
  Blading BAE Booksy listing and physical address in Tampa (8405 N Himes Ave, Suite 106), a
  Groupon listing with phone (813) 666-5038, and a Sunbiz FL corporate registration confirming
  Robertson Fleurine as the registered agent/manager of "BLADINGBAE LLC". No email address
  surfaced anywhere.
- Photo curation on the Booksy gallery also independently surfaced the same phone number,
  813-666-5038, stamped as a caption on one of the tattoo photos (excluded from the site gallery
  for having a text overlay, per curation rules).
- Conclusion: email null, outreach status pending_manual (contact via Instagram DM or the phone
  number above, after confirming it rings through to the Brandon location specifically).

## Curation notes
- Booksy dossier returned 16 raw photos; ~6 were usable (no text overlays, no mid-procedure/
  eyes-closed shots, no masks-only selfies, no owner selfies). Ran the Instagram rescue script
  (scripts/ig_photos.py) to check for a stronger set; the IG feed's own photos leaned more heavily
  on text-overlay infographics, mid-procedure and casual mask selfies than the Booksy set, so the
  final build uses the curated Booksy photos only (bk-1, bk-2 logo, bk-3, bk-4, bk-6, bk-7).
- Business is a microblading / permanent makeup studio that also does custom tattoo work
  (5 real services on Booksy: Microblading, Ombre Powder Brows, Microblading & Shading Combo,
  Touch Up, and Any Tattoo). No lash-extension services are actually published despite the
  Booksy category label "brows-lashes" and the business name; the site was built strictly from
  the real service menu, not the assumed niche.
- One named review (Seadrinta F.) contained an unrelated political aside in parentheses; it was
  trimmed from the on-site quote (kept verbatim otherwise) to keep the demo presentable as a
  business testimonial. Full original text is preserved in data.json.
