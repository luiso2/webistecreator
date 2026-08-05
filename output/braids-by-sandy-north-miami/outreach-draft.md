# Outreach draft: Braids By Sandy LLC

**Status:** no public email found (see research notes below). Draft kept on file for
if/when a public email turns up; primary outreach channel for this business is
WhatsApp/IG DM using `dm_message` below, sent to (786) 457-8137 / @braidsbysandyllc84.

**Angle:** has_own_site = false (see verification notes) -> "we built you a sample website".

---

**Subject:** A sample website for Braids By Sandy

Hi Sandy,

I came across Braids By Sandy on Booksy, 5.0 stars across 83 reviews is not easy to
pull off, so I put together a sample website for the shop:

https://siteforge-demos.odd-forest-9504.workers.dev/braids-by-sandy-north-miami/

It does not touch your booking setup at all, everything still runs through Booksy
exactly like it does today. This is just a home base people can find when they
search for braids in North Miami, with your real photos, your menu and your reviews.

If you like it, I am happy to put it on your own domain. If not, no worries at all,
just let me know and I will take it down, no strings attached.

Best,
Michael Vargas
Merktop

---

## Research notes (for the record)

- **Own website check:** `braidsbysandy.com` resolves but returns HTTP 402 "Payment
  required / DEPLOYMENT_DISABLED" (a suspended Vercel deployment), not a live site.
  `braidsbysandyllc.com` and `braidsbysandymiami.com` do not resolve. No
  `website_candidates` in the Booksy JSON-LD. Treated as **no live own site**
  (has_own_site: false).
- **Email search:** none in Booksy data.json (`phone` and email both null there,
  phone recovered separately from prior discovery + confirmed via an Instagram post
  caption screenshot: "Text 7864578137 to book"). Instagram profile fetch (WebFetch
  and the `web_profile_info` endpoint) was rate-limited (HTTP 429) / blocked on two
  attempts each. Facebook page hit a login wall, About section not accessible without
  an authenticated session. No linktree/beacons link was reachable. Email recorded as
  **null**.
