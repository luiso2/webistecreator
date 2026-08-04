# Outreach draft: Cocoa Cowrie Beauty (cocoa-cowrie-beauty-largo)

- has_own_site: false (confirmed via web search; only presence is Booksy/Instagram/Facebook,
  no independent domain found)
- email: cocoacowrie@gmail.com (public, found via directory listing search)
- phone: (727) 458-3585 (public, found via directory listing search)
- demo link: https://siteforge-demos.odd-forest-9504.workers.dev/cocoa-cowrie-beauty-largo/
- language: en
- angle: has_own_site false -> "we built you a sample website"

## Email draft

Subject: A sample website for Cocoa Cowrie Beauty

Hi Kylah and Phoebe,

I came across Cocoa Cowrie Beauty on Booksy and saw the 4.9 rating across 353 reviews, that is a
serious track record for a Largo hair salon. I put together a sample website to show what it
could look like beyond the Booksy listing:

https://siteforge-demos.odd-forest-9504.workers.dev/cocoa-cowrie-beauty-largo/

It is just a demo, it does not touch your real booking or client data at all. If you like it, I
can help put it on your own domain. If not, no problem at all, I will take it down, no obligation
either way.

Let me know what you think.

Best,
Michael Vargas
Merktop

## dm_message (for Instagram DM / WhatsApp, max 450 char)

Hi! I came across Cocoa Cowrie Beauty on Booksy, a 4.9 rating across 353 reviews is amazing for a Largo hair salon. I put together a sample website to show how it could look: https://siteforge-demos.odd-forest-9504.workers.dev/cocoa-cowrie-beauty-largo/ It's just a demo, doesn't touch your real booking. Happy to put it on your own domain, or take it down, no obligation either way. What do you think?
Michael, Merktop

(char count: 419)

## Notes on research attempts
- data.json (Booksy dossier) had phone: null and no email field; both were located separately
  via directory listing web search and were explicitly confirmed as legitimately public by the
  task brief before use here.
- No independent website domain found for "Cocoa Cowrie Beauty" or "Cocoa Cowrie House of Beauty"
  in Largo, FL; only Booksy, Instagram (@cocoacowrie) and Facebook presence exists.

## Curation notes (important: original downloaded assets were mostly unusable)
- The pre-downloaded `assets/raw/bk-1.jpg` through `bk-16.jpg` turned out, on pixel inspection,
  to be mostly 100x100px thumbnails (Booksy review-avatar crops), not full business photos, plus
  one generic 748x420 stock tool flat-lay (bk-1) and the 150x150 brand logo (bk-2). None of the
  100x100 files were usable at hero/gallery display sizes without severe pixelation, even though
  several of them (the bridal/updo portraits) looked visually striking on the contact sheet at
  thumbnail size.
- Ran the Instagram photo rescue (`scripts/ig_photos.py cocoacowrie cocoa-cowrie-beauty-largo 17`)
  per FORGE-BRIEF section 0 ("IG media: SOLO como rescate... o menos de 5 fotos reales
  utilizables"). Got 12 real photos at proper resolution (360-640px) from the public IG feed.
- Visually inspected each of the 12 rescued photos individually (not by filename). Rejected:
  bk-17, bk-18, bk-19 (text-overlay graphics/product ad), bk-20 (blurry macro), bk-24 (candid
  selfie holding sunglasses, not a hair result), bk-25 (PicCollage with cursive text overlay).
  Kept 6: bk-21 (crown braid pattern, top-down), bk-22 (color detail macro), bk-23 (box braids
  with burgundy ombre, back view), bk-26 (feed-in braids side profile, sharp), bk-27 (loc updo
  with gold cuffs, client smiling), bk-28 (feed-in braids with golden ends, side profile; had a
  "Book with me at..." Booksy caption band across the bottom, cropped out with PIL before use,
  keeping only the clean photo above the band).
- Final photo set used across hero/about/gallery is 6 real, sharp, non-text-overlay, non-selfie
  photos plus the logo (used only as a small brand mark in nav/footer/avatar, never as a gallery
  tile). This is fewer than the usual 6-8 gallery target; per DESIGN.md/PIPELINE.md ("menos fotos
  buenas > rellenar con malas"), the gallery was built with 3 tiles (1 wide + 2) rather than
  padding it with the unusable thumbnails or the generic stock photo.
- Reviews: data.json has 3 fully-attributed named reviews (Jewlana S., Andrea M., Patricia R.)
  used verbatim; the rest are anonymized snippets without author names and were not used as
  attributed testimonials.
