# Outreach draft: Cherry Barber (cherrybarbermiamibeach)

- has_own_site: false (confirmed: Booksy JSON-LD sameAs has no independent domain; Instagram
  web_profile_info external_url is a Booksy subdomain, http://cherrybarber.booksy.com/h/, not an
  owned domain; only other bio link is a TikTok profile)
- email: not found (see notes below) -> outreach: pending_manual
- phone: not found (Instagram business_phone_number is null, Booksy page has no published
  telephone)
- demo link: https://siteforge-demos.odd-forest-9504.workers.dev/cherrybarbermiamibeach/
- language: en
- angle: has_own_site false -> "we built you a sample website"

## Email draft (for manual send if an email is ever found, or for IG/WhatsApp follow-up as a longer message)

Subject: A sample website for Cherry Barber

Hi Cherry,

I came across Cherry Barber on Booksy and saw the 5.0 rating across 203 reviews, that's a
serious track record in Miami Beach. I put together a sample website to show what it could look
like beyond the Booksy listing:

https://siteforge-demos.odd-forest-9504.workers.dev/cherrybarbermiamibeach/

It's just a demo, it doesn't touch your real booking or client data at all. If you like it, I can
help put it on your own domain. If not, no problem at all, I'll take it down, no obligation either
way.

Let me know what you think.

Best,
Michael Vargas
Merktop

## dm_message (for Instagram DM / WhatsApp, ~450 char max)

Hi! I found Cherry Barber on Booksy, 5.0 rating across 203 reviews is impressive for a one-chair
shop in Miami Beach. I put together a sample website for you to see how it could look:
https://siteforge-demos.odd-forest-9504.workers.dev/cherrybarbermiamibeach/
Just a demo, doesn't touch your real booking. Happy to put it on your own domain if you like it,
or take it down, no obligation. Let me know what you think!
Michael, Merktop

(char count: 433)

## Notes on research attempts
- data.json (from booksy_dossier.py): no email field, phone: null.
- curl on the Booksy page HTML: no `mailto:` link found.
- Instagram web_profile_info (x-ig-app-id header, no auth needed): business_email null,
  business_phone_number null, business_contact_method "UNKNOWN". Bio has two links only: the
  Booksy subdomain booking link and a TikTok profile (@cherryoffwhite), no linktree/beacons page
  to follow.
- WebFetch on instagram.com/cherrybarberst/ returned HTTP 429 (rate limited); the direct
  web_profile_info endpoint worked and is the authoritative source above.
- Conclusion: email null, outreach status pending_manual (contact via Instagram DM, @cherrybarberst,
  16k followers, verified account).
