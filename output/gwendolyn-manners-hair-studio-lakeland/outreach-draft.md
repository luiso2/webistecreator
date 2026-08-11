# Outreach draft: Gwendolyn Manners Hair Studio (Lakeland, FL)

Status: no public email found after deep search (see research notes below). Email draft kept
below for future reference in case an email surfaces later. Primary outreach channel for now
is Instagram DM or a call/text to the phone number found on their storefront signage.

## Email (for reference, no confirmed inbox to send to yet)

Subject: A free sample website for Gwendolyn Manners Hair Studio

Hi Gwendolyn,

My name is Michael, I work with Merktop. I came across Gwendolyn Manners Hair Studio while
researching hair salons in Lakeland, 4.98 rating across 147 reviews on Booksy is genuinely
excellent.

I noticed you do not have your own website yet, only your Booksy page, so I went ahead and
built a free sample site for you with your real photos, your actual service menu and pricing,
and real reviews pulled from Booksy:

https://siteforge-demos.odd-forest-9504.workers.dev/gwendolyn-manners-hair-studio-lakeland/

It does not touch your Booksy booking system at all, clients would still book the exact same
way. If you like it, I am happy to put it on your own domain. If not, no obligation, I will
take it down, no cost either way.

Let me know what you think.

Michael Vargas
Merktop

## DM / WhatsApp message (dm_message, en, 439 chars)

Hi! I'm Michael with Merktop. I found Gwendolyn Manners Hair Studio in Lakeland, FL, 4.98 rating across 147 reviews on Booksy but no website of your own yet, so I built a free sample one with your real photos, menu and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/gwendolyn-manners-hair-studio-lakeland/ It does not touch your Booksy booking. Happy to put it on your domain, or take it down, no obligation. Michael, Merktop

## Contact research notes

- Booksy dossier (`scripts/booksy_dossier.py`): no `telephone` field published on the Booksy
  listing, no website_candidates, no email.
- Own domain check: `gwendolynmannershairstudio.com` and `myhairbywendy.com` both return DNS
  NXDOMAIN (getaddrinfo ENOTFOUND) via WebFetch, confirmed no own website exists.
- Instagram bio (`@myhairbywendy`): could not be fetched directly, WebFetch returned HTTP 429
  (Instagram rate-limits/blocks non-browser fetches) and no local Playwright/browser binary
  was available in this environment to render the profile and read the bio/external_url.
- Google search for the business name plus "email contact": no email surfaced, only the
  Booksy listing and unrelated salons with similar names.
- Business directory listing (beautynailhairsalons.com) for this address: lists hours and a
  generic Facebook page ID (facebook.com/103662771466084/) as the "website", no email, no
  phone. The Facebook page itself could not be read (login wall for unauthenticated fetch).
- Phone number: found written on the studio's real storefront sign, visible in a photo posted
  to the business Instagram feed and downloaded during research: **(407) 953-7223**. This is
  a real, publicly displayed number (also shown alongside the Facebook/Instagram/TikTok icons
  and the @myhairbywendy handle on the same sign), used here as the verified phone number even
  though Booksy itself does not publish it.
- No public email address was found through any of the above channels. Registering as null.
