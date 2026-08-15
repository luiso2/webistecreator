# Outreach draft - Alpine Alltrades Inc

**Channel:** phone / SMS (no public email found; email = null in data.json)
**Phone:** +1 352-792-4619
**Demo URL:** https://siteforge-demos.odd-forest-9504.workers.dev/alpinealltradesgainesville/
**Language:** English (primary)

---

Hi, this is Michael Vargas with Merktop.

We came across Alpine Alltrades Inc on Google (5.0 rating, 10 reviews) and noticed you do not have a website yet, so we went ahead and built a free sample site for you using your real photos and info from your Google Business profile:

https://siteforge-demos.odd-forest-9504.workers.dev/alpinealltradesgainesville/

No strings attached, this does not touch your current operation at all, it is just a preview of what a site for your business could look like. If you like it, we can put it live on your own domain. If not, no problem, we will take it down, just let us know either way.

Happy to answer any questions by call or text.

Michael Vargas
Merktop

---

## Notes for internal use
- has_own_site: false (verified: `alpinealltrades.com`, `alpinealltradesinc.com`, `alpinealltrades.net`, `alpine-alltrades.com` and www variants do not resolve; the Google Maps "website" field and the BBB profile both only point to `facebook.com/alpinealltrades`, which per pipeline rule does not count as an own website).
- No email found after checking the Google Maps listing, the Facebook page (WebFetch hit a login wall, no About page content accessible), the BBB accredited business profile, and general web search. Contact is phone/SMS only, consistent with the trades pattern noted in FORGE-BRIEF.md (82% of home-trade businesses publish phone vs only 29% for beauty).
- BBB profile identifies the owner as Troy Romantini and the business as established 1/1/2010 (16 years in business), BBB Accredited (A+) since 4/20/2023, with a detailed services list (handyman, painting, siding, gutters, remodeling, home repair/renovation, window replacement, door installation, pressure washing) used to write the site copy alongside what the Google Maps business photos actually show (kitchen and bathroom remodels, tile flooring, structural/insulation repair).
- No verbatim Google review text was retrieved (gmaps_detail.js returned `reviewSamples: []` despite the 5.0/10 rating being real and confirmed), so the site uses the no-testimonials variant (`social_proof.modo: "razones"`) while still showing the real 5.0 / 10 review numbers.
- A data-corruption bug was caught and fixed during build: the address unit "#140306" was initially misread by the palette hue-shift script as a hex color code and silently altered to "#040913" in the JSON-LD and footer. Fixed by writing the unit as "Suite 140306" instead of "#140306" in content.json (same real data, different literal format) and re-deriving the page; verified the corrected address appears correctly everywhere in the final index.html.
