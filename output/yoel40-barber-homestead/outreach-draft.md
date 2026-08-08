# Outreach draft: Yoel40 Barber (Homestead, FL)

## Research status
- Booksy dossier pulled live (2026-08-08): name, address, geo, hours, 10 services with real
  prices/durations, and 10 verbatim reviews (3 with a named, verified author) all came straight
  from Booksy's own JSON-LD/DOM payload. Rating/review count are live and higher than the
  discovery brief (was 4.9/77): the current Booksy page shows `aggregateRating` ratingValue
  4.9677.../reviewCount 124, which rounds to the 5.0 the page itself displays. Used 5.0 / 124.
- Phone: not published anywhere in the Booksy payload (checked `telephone`, `phone`, `tel:`
  links directly in the raw HTML: none present). -> null.
- Email: not published anywhere in the Booksy payload or page (no `mailto:`, no business email
  field). -> null.
- Instagram: Booksy's own `sameAs` field links to `instagram.com/yoel_ariel01`. Pulled that
  profile's visible public photos to verify correspondence (address/photos/owner name) per the
  task's verification requirement. Result: the account's visible content is personal/lifestyle
  (a soccer field, a group photo with friends, a dog, a Miami skyline selfie, a camera pose) with
  ZERO barbershop content, no shop interior, no haircuts, no mention of "Yoel40 Barber." Could
  NOT confirm it as the business's account with any confidence, so per the rule ("si no puedes
  confirmar con certeza, usa null") Instagram is left null and not used anywhere in the build.
  The dubious handles named in the brief (@yoel_barber_, @yoelbarbershop.rd) were not used either;
  no evidence tied them to this specific shop.
- Own website: no `website_candidates` in the Booksy payload, no domain found for
  "yoel40barber.com" / "yoel40.com" style guesses, and a web search for "Yoel40 Barber Homestead
  website" returns only the Booksy listing. `has_own_site: false`.
- Photos: 16 real photos came down from Booksy's own business gallery (not Instagram). Curated
  visually one by one (Read tool, not by filename): 10 kept for the finished site (gallery +
  hero + experience), 2 discarded (one blurry 150x150 thumbnail, one near-duplicate of a kept
  photo), and the 1 close-up barber portrait was used only as a small avatar (nav/footer/about),
  never as a gallery tile, per the portrait rule. No IG rescue was needed since Booksy alone gave
  far more than the 5-photo minimum.
- Language: all 10 reviews and every piece of scraped text are in English; set `language: en`.

## Outreach channel available
No public email, no public phone, and Instagram could not be confirmed. The only real, verified
public channel for this business is its Booksy listing itself, which has no direct messaging.
**Outreach: `pending_manual`**. Nothing can be sent by this pipeline. The email draft below is
prepared for whenever a channel (email, confirmed IG, or phone) becomes available, and the
`dm_message` is ready to paste into Booksy's own messaging (if the owner replies to a booking
inquiry) or any channel discovered later.

---

## Email draft (English, ready for whenever an address is found)

Subject: A sample website for Yoel40 Barber

Hi Yoel,

I came across Yoel40 Barber on Booksy and saw the 5.0 rating across 124 reviews, that is a
really strong track record for a one-chair shop in Homestead.

I noticed you don't have your own website yet, just the Booksy page, so I put together a free
sample site to show what it could look like: real photos from your shop, your actual menu and
prices, and your real reviews.

Take a look here: https://siteforge-demos.odd-forest-9504.workers.dev/yoel40-barber-homestead/

It does not touch your Booksy booking at all, it just links out to it the same way your bio
would. If you like it, I can put it on your own domain. If not, no problem, I will take it down,
no strings attached.

Let me know what you think.

Michael Vargas
Merktop

---

## dm_message (English, for Booksy message / any confirmed channel, ~430 chars)

Hi! I'm Michael with Merktop. Found Yoel40 Barber on Booksy, 5.0 with 124 reviews is great work.
Since you don't have your own website yet, I built a free sample site with your real photos,
menu and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/yoel40-barber-homestead/
It doesn't touch your Booksy booking. Like it? I can put it on your own domain. If not, no
worries, I'll take it down. No strings attached.
