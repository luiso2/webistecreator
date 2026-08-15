# Outreach draft - Good Neighbors Lawn Services

**Channel:** phone / SMS (no public email found; email = null in data.json)
**Phone:** +1 772-259-3864
**Demo URL:** https://siteforge-demos.odd-forest-9504.workers.dev/goodneighborslawnportstlucie/
**Language:** English (primary)

---

Hi, this is Michael Vargas with Merktop.

We came across Good Neighbors Lawn Services on Google (4.7 rating) and noticed you do not have a website yet, so we went ahead and built a free sample site for you using your real photos and info from your Google Business profile:

https://siteforge-demos.odd-forest-9504.workers.dev/goodneighborslawnportstlucie/

No strings attached, this does not touch your current operation at all, it is just a preview of what a site for your business could look like. If you like it, we can put it live on your own domain. If not, no problem, we will take it down, just let us know either way.

Happy to answer any questions by call or text.

Michael Vargas
Merktop

---

## Notes for internal use
- has_own_site: false (verified: `goodneighborslawnservices.com`, `goodneighborslawn.com`, `goodneighborslawnservicesfl.com` do not resolve; `goodneighborslawncare.com` resolves but redirects to a completely unrelated business, lockettlawnandlandscape.com; Google Maps shows "Add website", no Website button)
- No email found after checking Nextdoor (2 listings), Thumbtack, Yelp search snippets, and Facebook. Contact is phone/SMS only, consistent with the trades pattern noted in FORGE-BRIEF.md.
- No verbatim Google review text was retrievable (gmaps_detail.js returned rating but empty reviewSamples, and the review count itself is not shown at all in Google Maps' unauthenticated view), so the site uses the no-testimonials variant (`social_proof.modo: "razones"`). The 4.7 rating shown is independently verified directly from Google Maps; no specific review count is published anywhere on the site because it could not be confirmed.
- No public street address exists for this business anywhere (service-area business): the site omits a map/address section and uses a real work photo instead, per the variante adaptada.
- IMPORTANT: a differently named business, "Good Neighbor Lawn Care" (singular "Neighbor", LLC, Facebook/@goodneighborlawns on Instagram, phone 980-254-2713, founded 2001), repeatedly surfaced in search results for similar queries. That business's email, phone, social handles and founding year were explicitly NOT used anywhere in this build; everything here is scoped strictly to "Good Neighbors Lawn Services" at +1 772-259-3864 per the Google Maps listing given in the brief. See data.json's `different_business_warning` for the full detail if this ever needs to be re-verified.
