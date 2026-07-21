# Outreach draft - Lash Mastery & Aesthetics Co. (lashmasteryco)

## Status
- has_own_site: false (no independent domain found; only GlossGenius booking subdomain + directory listings)
- email: not found (GlossGenius dossier could not be extracted automatically; IG bio and Facebook page were not accessible for scraping, see data.json `instagram_note` and `booking_url_status`)
- outreach channel: **pending_manual**, send via Instagram DM (@lashnride) or WhatsApp/call to (954) 591-8060. No email send is possible for this business yet.
- angle: "I built you a free sample website" (has_own_site = false)
- language: English

## dm_message (for IG DM / WhatsApp, 355 characters)

```
Hi! I came across Lash Mastery & Aesthetics Co. (5.0 stars, 22 Google reviews) and built you a free sample website: https://siteforge-demos.odd-forest-9504.workers.dev/lashmasteryco/

It does not touch your GlossGenius booking, just a showcase site linking to it. Happy to put it on your own domain or take it down, no strings attached. What do you think?
```

## Longer version (if a channel with more room becomes available, e.g. email if one is found later)

Subject: A free sample website for Lash Mastery & Aesthetics Co.

Hi Daisy,

I came across Lash Mastery & Aesthetics Co. while looking at top-rated lash studios in Boca Raton (5.0 stars, 22 Google reviews is genuinely impressive) and I put together a free sample website for the studio:

https://siteforge-demos.odd-forest-9504.workers.dev/lashmasteryco/

A few things about it:
- It does not touch your GlossGenius booking at all. Every "Book" button just links straight to your existing GlossGenius page.
- All the photos, reviews and services on it are real, pulled from your Instagram and your Google reviews.
- If you like it, I can help you put it on your own domain. If not, no worries at all, I will take it down, no strings attached.

Let me know what you think.

Michael Vargas
Merktop

## Notes for the human approving this batch
- No fabricated prices or durations are on the site: GlossGenius (lashmama.glossgenius.com) returned a 302 redirect to the generic GlossGenius marketing homepage for every automated fetch attempt during research (curl, WebFetch, and a third-party reader proxy, from multiple CloudFront edge locations), so the usual "PASO 1" dossier script could not extract the real menu/prices/photos/email. The business's real identity, address and phone were independently cross-verified via Fresha, Birdeye, Atly, LashLookup and Hotfrog, so the build went ahead with verified-name-only services (no price) and photos rescued from the public Instagram feed via a mirror service. See data.json for full detail.
- Real verbatim reviews used (sourced from Google via Birdeye, which the task confirmed cites "Google: 22"): Madison Ella, LaShanda M., Rebeca Rodríguez.
- If GlossGenius becomes reachable again in a later session, it would be worth re-running `scripts/glossgenius_dossier.py` to backfill real prices/durations and a business email, then updating the services section accordingly.
