# Outreach draft: Get Naked Wax Bar (getnakedwaxbarbrandon)

- has_own_site: false (verified via web search: only Booksy/Fresha/Instagram/Facebook/Yelp
  listings found, no independent domain)
- email: not found (see notes below) -> outreach: pending_manual
- phone: (910) 373-8228 / +19103738228 (confirmed directly from the raw Fresha listing page
  JSON payload for this exact business at this exact address; not published on Booksy itself)
- demo link: https://siteforge-demos.odd-forest-9504.workers.dev/getnakedwaxbarbrandon/
- language: en
- angle: has_own_site false -> "we built you a sample website"

## Email draft (for manual send if an email is ever found, or for IG/WhatsApp follow-up as a longer message)

Subject: A sample website for Get Naked Wax Bar

Hi Tatiana,

I came across Get Naked Wax Bar on Booksy and saw the 5.0 rating across 164 reviews, that is a
serious track record for a one-woman studio. I put together a sample website to show what it
could look like beyond the Booksy listing:

https://siteforge-demos.odd-forest-9504.workers.dev/getnakedwaxbarbrandon/

It's just a demo, it doesn't touch your real booking or client data at all. If you like it, I can
help put it on your own domain. If not, no problem at all, I'll take it down, no obligation either way.

Let me know what you think.

Best,
Michael Vargas
Merktop

## dm_message (for Instagram DM / WhatsApp, ~450 char max)

Hi! I came across Get Naked Wax Bar on Booksy, 5.0 rating across 164 reviews is impressive for a
one-woman studio. I put together a sample website for you to see how it could look:
https://siteforge-demos.odd-forest-9504.workers.dev/getnakedwaxbarbrandon/
It's just a demo, doesn't touch your real booking. Happy to put it on your own domain if you like
it, or take it down, no obligation either way. Let me know what you think!
Michael, Merktop

(char count: ~445)

## Notes on research attempts

- Web search for "Get Naked Wax Bar" Brandon FL website: no independent domain found, only
  Booksy/Fresha/Instagram/Facebook/Yelp listings.
- Phone found and cross-verified: WebSearch surfaced (910) 373-8228 via a Fresha listing snippet;
  confirmed directly by curling the raw Fresha page HTML for this exact business
  (fresha.com/lvp/get-naked-wax-bar-east-bloomingdale-avenue-brandon-k9K4Zv), which embeds
  `"phone":"(910) 373-8228"` in its page JSON. Not present on Booksy itself. Area code (910, NC)
  does not match the FL location, which is common for a mobile number kept from out of state; two
  independent sources agree on the number so it is used with reasonable confidence, flagged here
  for a spot-check before a live send.
- WebFetch on instagram.com/getnakedwaxbar/: HTTP 429 twice (rate limited), no bio/external_url
  retrieved.
- WebFetch on facebook.com/Getnakedwaxbar/: returned Facebook's login wall, no About/contact data
  retrieved.
- curl on the Booksy listing HTML: no `mailto:` link present.
- Conclusion: email null, outreach status pending_manual (contact via Instagram DM, Facebook, or
  the phone number above).

## Photo desert note (for whoever approves this batch)

The Instagram feed (@getnakedwaxbar) is almost entirely text-overlay promo graphics and owner
selfies rather than studio/work photography; the Booksy gallery is mostly customer avatar
placeholders. After visual curation per the quality gate (no text overlays, no selfies as gallery
tiles, no explicit/mid-procedure closeups), only 3 real usable source photos survived: the
physical wall signage, one owner-with-equipment shot, and one treatment-room interior. The site
was built leaner rather than padded: gallery has 2 real tiles instead of the usual 6, and the
owner photo is used only in the "experience" section (not as a gallery result), consistent with
the pipeline's "fewer good photos beats padding with bad ones" rule.
