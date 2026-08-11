# Outreach draft: Sérénité Esthetics Inc.

**Status:** pending_manual (no public email found after deep search)
**Channel:** Phone (786) 672-4501 or Instagram DM @sereniteesthetics.
**Demo:** https://siteforge-demos.odd-forest-9504.workers.dev/serenite-esthetics-kendall/

---

## Email version (for reference / if an email is ever found)

**Subject:** A free sample website for Sérénité Esthetics

Hi Rosalie,

I'm Michael Vargas, with Merktop. I came across Sérénité Esthetics while looking at facial and skin care studios in Kendall, 5.0 rating across 163 reviews on Fresha, with clients specifically calling out how attentive and professional you are, and more than one saying they travel from as far as Tampa just to see you.

Since your Fresha page is only a booking page and Sérénité Esthetics does not have a real website of its own yet, I put together a free sample one using your real studio photos, your actual treatment menu and prices, and real reviews from your Fresha clients:
https://siteforge-demos.odd-forest-9504.workers.dev/serenite-esthetics-kendall/

It does not touch how clients book with you today, still Fresha or a call to (786) 672-4501. Nothing about your booking process changes.

If you like it, I can help you put it on your own domain. If it is not for you, just say so and I will take it down, no obligation either way.

Best,
Michael Vargas
Merktop

---

## DM message (Instagram / WhatsApp, 431 characters)

Hi! I'm Michael with Merktop. I found Serenite Esthetics while researching facial studios in Kendall, 5.0 rating across 163 reviews on Fresha. You don't have your own website yet, so I built a free sample one with real photos, your menu and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/serenite-esthetics-kendall/ It doesn't touch your Fresha booking. Happy to put it on your domain, or take it down, no obligation.

---

## Research notes on contact channels

- **Phone:** (786) 672-4501, published on Fresha (`contactNumber`) and matches the studio's own signage photographed in the gallery. Verified.
- **Email:** not found after checking (1) Fresha's `location.email` field (null), (2) the Fresha `owner.onlineLinks` object (only `instagramUrl` and a TikTok `websiteUrl`, no Facebook, no email), (3) the Instagram profile directly (blocked/rate-limited on every attempt: `web_profile_info` returned 400 as documented, direct page fetches returned 429/login-wall), (4) TikTok bio (@serenite.esthetics, bio is just "Make Your Day", no link), (5) a Linktree that surfaced in search under a similar name ("SerenityEsthetics") was checked and confirmed to belong to an unrelated esthetician (Kasmira Joseph), not this business, (6) Florida Sunbiz corporate filing (blocked the fetch with a 403 WAF page). Given no public email surfaced through any of these channels, outreach for this business is `pending_manual` via phone or Instagram DM, per pipeline rules (never fabricate a contact channel).
- **Google rating:** the 5.0 / 163 reviews figure is sourced from Fresha's own embedded data (`location.rating`, `location.reviewsCount`, cross-checked against the individual verbatim review edges, which total the same 5-star distribution). Attempts to independently confirm via a live Google Business/Maps listing did not surface a renderable Google card through available tools (Google Search and Google Maps both require JS execution that the sandbox's fetch tools could not perform; no cached Google Business snippet appeared in search results). The site copy therefore cites "Fresha" as the explicit source of the rating/review count rather than claiming "Google," to stay strictly accurate.
