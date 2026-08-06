# Outreach draft: Dominican Cakes & Bridal Shop (dominican-cakes-bridal-pompano-beach)

- **Status**: `draft` (no public email independently confirmed; outreach recommended as `pending_manual` via phone/IG DM, NOT email)
- **To**: no confirmed email (see verification note below)
- **From**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-dominican-cakes-bridal-pompano-beach-2026-08-06
- **Angle**: no site of their own (`has_own_site: false`) -> "I built you a sample website"
- **Language**: English (all 5 verbatim Google reviews collected are in English; IG auto-captions
  gave no usable language signal since the profile could not be reached directly this session; the
  site is fully bilingual EN/ES per DESIGN.md regardless, EN is just the default)
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/dominican-cakes-bridal-pompano-beach/
- **Phone verified**: (954) 970-9669 (matches Wanderlog, caffecake.com, and the business listing
  used for discovery)
- **Address**: 2428 N State Road 7, Pompano Beach, FL 33063 (right on the Pompano Beach/Margate
  line; some listings, including a smaller separate Yelp profile, tag it "Margate")
- **Instagram**: https://www.instagram.com/dominicancakesandbridalshop/ (@dominicancakesandbridalshop)
- **Facebook**: https://www.facebook.com/DomincanCakesandBridalShop/ (handle spelled "Domincan", not
  "Dominican"; page exists publicly but its About section is login-walled, could not be scraped this
  session via WebFetch, mbasic.facebook.com, or curl)

## Rating verification
- **Primary source used on the site**: Wanderlog (wanderlog.com/place/details/10963169/dominican-cakes--bridal-shop),
  which aggregates Google Places data: **4.7 stars, 121 reviews**. Re-fetched independently this
  session and confirmed the same figure, address, phone and hours, plus 5 full verbatim reviews with
  reviewer names, all in English.
- **Discrepancy noted**: a separate, smaller Yelp listing tagged "Margate" shows only **30 reviews**
  ("DOMINICAN CAKES AND BRIDAL SHOP - Updated September 2025 - 21 Photos & 30 Reviews", Yelp biz page
  `dominican-cakes-and-bridal-shop-margate`, direct fetch returned HTTP 403 so only the search-result
  title could be confirmed). This reads as the same business's secondary/duplicate platform listing
  with a smaller review pool, not a different business (identical address, phone and name). The
  Wanderlog/Google figure (4.7 / 121) is used as primary because Google is the pipeline's source of
  truth and has by far the larger, more representative sample.

## Own-website check
- `dominicancakesbridalshop.com` returns **HTTP 503 Service Unavailable**, confirmed independently
  this session via a direct fetch. This is a borderline case: the domain exists and is presumably
  registered to the business (name matches exactly), but it does not serve a working website right
  now, whether abandoned, parked, or mid-migration could not be determined. Per pipeline rules this
  is treated as **no functioning site** (`has_own_site: false`), and the outreach angle is "I built
  you a sample site", but this finding is flagged here explicitly since it is not a clean "never had
  a domain" case.
- No other bio links, linktree, or booking-platform subdomain was found to contradict this.

## Email verification (deep search, Fase 1 punto 7)
- **Lead investigated**: `Cakesbridalshop@aol.com`, surfaced only in an AI-summarized web search
  answer with no traceable primary source page (a follow-up WebSearch repeated the same address but
  again without a citable source page; `cakes.com`'s own bakery page returned 404 on direct fetch,
  and `caffecake.com`'s contact page explicitly lists phone and address but **no email**).
- **Instagram business_email**: the `web_profile_info` endpoint with header `x-ig-app-id:
  936619743392459` returned HTTP 401 (no session) as expected per PIPELINE.md; a direct profile page
  fetch (both curl and WebFetch) hit HTTP 429/rate-limit before the bio could be read, so the IG bio
  and business_email field could not be inspected this session.
- **Facebook About**: the page is real and public (`facebook.com/DomincanCakesandBridalShop`) but
  both `www.facebook.com` and `mbasic.facebook.com` served a login wall / browser-compatibility page
  to the fetch tools available, with no About content exposed.
- **Own domain**: dead (503), so no mailto or contact page to check there.
- **Conclusion**: the `Cakesbridalshop@aol.com` lead could **not be independently confirmed** this
  session via any primary source (IG bio, FB About, own domain). It is **not used** anywhere in the
  site or in this outreach draft. Recorded here only as an unverified lead for a future session that
  can reach the IG bio directly (e.g. once past the rate limit) or log into Facebook to check About.
  Outreach for this business should go out as `pending_manual` via phone call or Instagram DM, not
  email.

## Subject (reference, for if a verified email is found later)
A free sample website for Dominican Cakes & Bridal Shop

## Body (reference)

```
Hi,

I came across Dominican Cakes & Bridal Shop looking for custom cake bakeries around Pompano Beach.
A 4.7 rating with 121 reviews, and reviewers going out of their way to mention the dulce de leche
and guava flavors, said enough for me to want to reach out.

I noticed Dominican Cakes & Bridal Shop does not have a working website right now (the domain I
found returns an error page), so I built a free sample one, no cost and no obligation:

https://siteforge-demos.odd-forest-9504.workers.dev/dominican-cakes-bridal-pompano-beach/

It uses your real cake photos, your real address and real reviews from your customers. It does not
touch anything about how you currently run things: it is not your official page, it replaces
nothing, and the main button just calls your phone.

If you like the direction, I can hand over the files or help you point your own domain to it. If
it is not for you, no hard feelings, I will take it down.

Happy to adjust anything (colors, photos, text) before you decide.

Best,
Michael Vargas
Merktop
```

---

## Short DM / WhatsApp version (dm_message)

```
Hi! I'm Michael with Merktop. I found Dominican Cakes & Bridal Shop on State Road 7 (4.7 rating,
121 Google reviews, cakes people love) and built you a free sample website with your real cakes
and info: https://siteforge-demos.odd-forest-9504.workers.dev/dominican-cakes-bridal-pompano-beach/
It does not touch your business, just adds a call button. Like it, its yours free. If not, no
problem, I will take it down. Michael Vargas, Merktop.
```

(441 characters, in English as the site's primary language, no em-dash, has_own_site: false angle.)
