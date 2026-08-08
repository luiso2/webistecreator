# Outreach draft: Vogue Nail Spa (Pompano Beach, FL)

Status: DRAFT ONLY. Not sent. No contact made with the business through any channel.
Per PIPELINE.md Fase 5, sending requires explicit human approval for this batch.

## Research status (Fase 1, punto 7: busqueda profunda)

- **Phone**: (954) 464-3812 / +19544643812. CONFIRMED, independently, via 3 sources:
  the discovery brief, a live WebSearch snippet citing Yelp, and the maby.us business
  directory listing.
- **Email**: `voguenailspa21@gmail.com` (candidate carried over from the discovery brief).
  **NOT independently re-verified this session.** I attempted verification via: direct
  WebFetch of instagram.com/vogue.nail.spa (HTTP 429, rate-limited), the IG
  `web_profile_info` API (401, rate-limited), `ig_scrape_fixed.js` with the
  proxy-safe Chrome launch (`net::ERR_HTTP_RESPONSE_CODE_FAILURE`, two attempts),
  Facebook About (login wall), the Booksy JSON payload (no email field exposed),
  and the business's Square booking site `voguenailspa.square.site` (no real email
  in the page source, only Square's own placeholder `hi@mystore.com`). Several
  WebSearch queries for the exact address also returned no publicly indexed email.
  Instagram access was blocked/rate-limited for this entire session, which is the
  channel most likely to hold the real address. **Treat this email as unconfirmed.**
  Recommend leading with phone/DM, and trying the email as a secondary channel at
  the user's discretion.
- **Instagram**: `@vogue.nail.spa`. CONFIRMED via the Booksy `sameAs` field
  (`https://www.instagram.com/vogue.nail.spa/`) and a WebSearch snippet showing the
  live bio: "Private Nail Spa • Pompano Beach • By appointment only • Curated nail
  artistry", 780 followers, 417 posts.
- **Website**: none. `voguenailspa.com` and `hiddengemnailboutique.com` do not
  resolve (no DNS). The only web presence beyond social/booking is
  `voguenailspa.square.site`, a Square platform subdomain, which per pipeline rules
  does **not** count as an owned website. `has_own_site: false`.
- **Naming note**: the business is universally known as "Vogue Nail Spa" (Yelp,
  Facebook, Instagram, Groupon, TikTok, and the meta title of its own Square site
  all say "Vogue Nail Spa"). Its Booksy listing itself has been renamed to "Hidden
  Gem Nail Boutique" (same venue ID 736882, same address, same Instagram, same
  owner Marcela, rating 5.0 / 66 reviews), likely a recent rebrand-in-progress on
  that one platform only. The demo uses "Vogue Nail Spa" to match how the business
  presents itself everywhere else and how it was assigned in this brief; the Booksy
  booking link still works correctly (the original URL redirects to the current
  listing).

## Draft email (English, not sent)

**Subject:** A sample website for Vogue Nail Spa

Hi Marcela,

I came across Vogue Nail Spa on Booksy while looking at nail salons in Pompano
Beach. A perfect 5.0 rating across 66 reviews is rare, so I went ahead and built
a sample website to see how it would look:

https://siteforge-demos.odd-forest-9504.workers.dev/vogue-nail-spa-pompano-beach/

It does not touch your Booksy booking at all, this is just a preview built from
your public menu, prices and reviews. If you like it, I can help put it on your
own domain. If it is not for you, no problem, I will take it down, no strings
attached.

Would love to hear what you think.

Michael Vargas
Merktop

## dm_message (short version for IG DM / WhatsApp, English, 358 chars)

Hi! I came across Vogue Nail Spa on Booksy, love the 5.0 rating across 66 reviews. I built a free sample website to show how it could look: https://siteforge-demos.odd-forest-9504.workers.dev/vogue-nail-spa-pompano-beach/ It does not touch your Booksy booking at all. Happy to put it on your own domain, or take it down, no strings attached. Michael, Merktop
