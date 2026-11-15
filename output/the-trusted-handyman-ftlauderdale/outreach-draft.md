# Outreach draft: The Trusted Handyman (Fort Lauderdale, FL)

Status: **draft only, nothing sent**. No public email was found after a deep search
(Google Maps listing, web search for the business name + "Fort Lauderdale" + "email"
and + "facebook"). The only indexed third-party profile is an unclaimed Birdeye page
(different, unreliable rating/review numbers: 4.3/43, not used anywhere in this build).
Outreach channel for this business is **phone**: (954) 419-8566.

- has_own_site: false (verified: Google Maps listing has no website field)
- rating/reviews verified against the live Maps listing: 4.6 / 36 (matches the brief exactly)
- angle: "I built you a sample website" (has_own_site = false)
- language: English (reviews, listing and expected customer base are English-speaking Fort Lauderdale)
- outreach: `pending_manual` (call or walk-in; no email/IG DM channel available)

## DM / SMS / call-script version (used as `dm_message`, 431 chars)

```
Hi! I found The Trusted Handyman on Google (4.6 stars, 36 reviews) while looking at Fort Lauderdale handyman businesses. I noticed there is no dedicated website, so I built a sample one using your real photos and info:

https://siteforge-demos.odd-forest-9504.workers.dev/the-trusted-handyman-ftlauderdale/

No cost, no change to how you work. If it is useful I can tailor it or put it on your own domain. If not, just ignore this.
```

## Longer version (email-equivalent, for if an email surfaces later, or to read over a call)

**Subject:** A sample website for The Trusted Handyman

Hi,

I came across The Trusted Handyman while looking at handyman and remodeling businesses
in Fort Lauderdale, your 4.6 rating from 36 reviews on Google stood out. I could not find
a dedicated website linked from your listing, so I put together a sample page using your
own public photos and contact info:

https://siteforge-demos.odd-forest-9504.workers.dev/the-trusted-handyman-ftlauderdale/

It gives a new customer one clear place to see real examples of your work (the kitchen
remodels, the before/after repaints, the flooring jobs) and call you directly. It does not
touch how you currently take calls or book jobs, it is just a page that points to your phone
number.

If you like it, I can tailor the colors and copy and put it on your own domain. If it is not
useful, no worries, just let me know and I will not follow up again.

Best,
Michael Vargas
Merktop

## Notes for the human approving this batch
- Call script works too: the dm_message text above reads fine out loud and has the link
  for a follow-up text message.
- An older, unfinished build of this exact business exists at `output/the-trusted-handyman/`
  (same Google Maps place id, same phone/rating/reviews). It was never registered in
  `data/processed.json` or `data/queue_done.json`, and its gallery/about sections used 4
  stock photos (iStock-dimension images: gmaps-4, gmaps-5, gmaps-8, gmaps-9) that this build
  intentionally excluded. Recommend deleting or ignoring that orphan folder before any
  registration step, to avoid two demo slugs for the same business identity.
