# Outreach draft: Bareface Esthetics (West Palm Beach, FL)

Status: public email found (bareface.esthetics@yahoo.com, cross-referenced across multiple
directory listings, not opened directly). Draft below is prepared for human approval per
pipeline rules; nothing has been sent. Language: English (business language detected from
IG captions, about text, and reviews).

## Email draft

To: bareface.esthetics@yahoo.com
From: Michael Vargas <michael@go.merktop.com>
Reply-To: jose@merktop.com
Subject: A free sample website for Bareface Esthetics

Hi Rebecca,

I came across Bareface Esthetics on your reviews page, 5.0 rating across 32 reviews, and
noticed you do not have a website of your own yet, just your GlossGenius booking page. So I
put together a free sample site for you with your real facial menu, your prices, your
photos and a few of your reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/bareface-esthetics-wpb/

It does not touch your GlossGenius booking at all, clients would still book the exact same
way. If you like it, I can help you put it on your own domain. If not, no problem, I will
take it down, no obligation either way.

Michael Vargas
Merktop

## dm_message (WhatsApp/DM, English, under 450 chars)

Hi Rebecca! I found Bareface Esthetics online, 5.0 rating across 32 reviews, but no website of your own yet, just GlossGenius. So I built a free sample site with your real facial menu, prices and photos: https://siteforge-demos.odd-forest-9504.workers.dev/bareface-esthetics-wpb/ It does not touch your booking at all. Happy to put it on your own domain, or take it down, no obligation. Michael, Merktop.

(392 characters)

## Contact research notes

Channels checked for a public email, in order (per PIPELINE.md Fase 1 punto 7):
1. GlossGenius booking page (barefaceestheticsfl.glossgenius.com) and its /about subpage:
   no email listed, no mailto link in the page.
2. Instagram bio (@bareface.estheticsfl): profile fetch via web_profile_info was rate
   limited (429) on this pass; the ig_photos.py photo service does not expose bio/email
   fields, only image URLs, so it could not be used for this check either.
3. Facebook page (facebook.com/barefaceestheticsfl/): direct fetch returned only Facebook's
   logged-out shell (no About section content reachable without login).
4. Business directory aggregation: the email bareface.esthetics@yahoo.com and phone
   (561) 692-6083 appear consistently across independent directory sources (Yelp business
   listing snippet, guidetoflorida.com, addonbiz-style aggregators) tied to the exact same
   address (1500 A Elizabeth Avenue, Studio 23, West Palm Beach). Treated as reliable given
   the cross-source consistency, though no single Bareface-controlled page was opened
   directly to confirm it firsthand.
5. Sola Salon Studios booking page (book.solasalonstudios.com/bareface-esthetics-llc/pro):
   no email or phone rendered in the fetched content (JS-heavy page).

Phone (561) 692-6083 confirmed the same way (consistent across directory sources) and also
matches the tel: number surfaced by the GlossGenius booking widget itself.

## Discovery notes

- Searched via Google web search for "facial studio Boca Raton", "med spa Boca Raton",
  "facial studio Port St. Lucie" and GlossGenius directory listings for estheticians in
  West Palm Beach / Boca Raton (zones checked in the order requested: West Palm Beach,
  Boca Raton, Port St. Lucie).
- IMPORTANT disambiguation: there is a second, unrelated business with a near-identical
  name, "BareFace Aesthetics" (2161 Palm Beach Lakes Blvd, WPB; esthetician "Nicole";
  4.9 rating, 169 reviews; HAS its own site at barefaceaesthetic.com). That is a different
  business and was NOT used for this build. Bareface Esthetics LLC (this build) is at
  1500 Elizabeth Avenue Suite 23 (Sola Salon Studios), owned by Rebecca Valenti, 5.0 rating
  across 32 reviews, no own site.
- Candidates discarded before accepting this one:
  - Happy Skin Boutique | Med Spa & Facial Spa (Boca Raton): has its own site,
    happyskinmedspa.com. Discarded per "has own site" rule.
  - Gentle Touch Facial Studio (Port St. Lucie): has its own site,
    gentletouchfacialstudio.com. Discarded.
  - True Beauty Face & Body Aesthetics (Port St. Lucie), solo aesthetician Lays De
    Oliveira: has its own site, truebeautyflorida.com. Discarded.
  - Boca Skin Spa (Boca Raton, GlossGenius): already built in this repo as
    `output/boca-skin-spa-bocaraton/` (checked before accepting Bareface).
