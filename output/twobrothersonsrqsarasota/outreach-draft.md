# Outreach draft - 2 Brothers On SRQ

**Channel:** email (public email found: carcare@svk2bronsrq.com)
**Backup channel:** phone / SMS at (941) 735-8003 (Google Maps listed number)
**Email:** carcare@svk2bronsrq.com
**Phone:** +1 941-735-8003
**Demo URL:** https://siteforge-demos.odd-forest-9504.workers.dev/twobrothersonsrqsarasota/
**Language:** English (primary)
**Sender:** Michael Vargas <michael@go.merktop.com> (reply-to jose@merktop.com, tag campaign=siteforge)
**Idempotency-Key:** siteforge-twobrothersonsrqsarasota-2026-08-15

---

Subject: A sample website for 2 Brothers On SRQ

Hi, this is Michael Vargas with Merktop.

We came across 2 Brothers On SRQ on Google (5.0 rating, 10 reviews) and noticed you don't have a website yet, so we went ahead and built a free sample site for you using your real photos and packages from your Google Business profile:

https://siteforge-demos.odd-forest-9504.workers.dev/twobrothersonsrqsarasota/

We even pulled in your real Longboat Key, Lido Key and Siesta Key pricing from your flyer, so it's ready to show as-is. No strings attached, this doesn't touch your current operation at all, it's just a preview of what a site for your business could look like. If you like it, we can put it live on your own domain. If not, no problem, we'll take it down, just let us know either way.

Happy to answer any questions by email, call or text.

Michael Vargas
Merktop

---

## Notes for internal use
- has_own_site: false (verified: `2brothersonsrq.com` and `svk2bronsrq.com`, their own email's domain, both fail DNS resolution entirely via WebFetch, ENOTFOUND. Google Maps confirms "Add website", no site on file.)
- Email carcare@svk2bronsrq.com found printed directly on two of the business's own Google Maps photos (a business-card style graphic and their pricing flyer), not guessed or pattern-generated. High confidence: it appears twice, consistently, alongside their own phone number.
- Google Maps' live listing phone is +1 941-735-8003 (used consistently as the site's primary CTA/tel: link, per instructions). Their own printed marketing materials (shirt, flyer, business card) instead show (941) 879-3762 for "call/text/email", which is likely their day-to-day operating line. Worth a heads up to Jose before sending in case the phone number on the demo should be double-checked with the owners directly, since it's borderline which number they'd rather have surfaced.
- No verbatim Google review text was retrieved (scripts/gmaps_detail.js and scripts/gmaps_verify.js both returned empty reviewSamples on live runs), so the site uses the no-testimonials variant (`social_proof.modo: "razones"`) with 3 real, evidence-backed reasons (owner-operated, published pricing, all-vehicle-types) instead of inventing quotes, while still showing the real 5.0 / 10 numbers.
- Review count (10) could not be independently re-derived from a live Google Maps view in this session (same tooling limitation as several prior builds); it is carried forward from the discovery/qualification phase, which already gated on rating >= 4.5 and reviews >= 10. Rating 5.0 was independently re-confirmed live.
- Owners identified as Oscar and Felix (Yelp: "Oscar and Felix G."; Florida Sunbiz LLC record independently names registered agent "Oscar D. Guerrero"), used by first name only on the site since only one surname could be confirmed.
- Real published pricing used directly (Longboat Key $25, Lido Key $15 at their location only, Siesta Key Full Detail $99 starting), sourced from the business's own flyer photo, not estimated.
