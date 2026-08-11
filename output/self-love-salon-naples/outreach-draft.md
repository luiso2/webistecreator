# Outreach draft: Self Love Salon (Naples, FL)

Slug: `self-love-salon-naples`
Demo: https://siteforge-demos.odd-forest-9504.workers.dev/self-love-salon-naples/
Language of business: English (all Booksy reviews and bio content are in English)
Angle: `has_own_site: false` -> "we built a free sample website for you"

## Contact research notes

- `selflovesalon.com` DOES resolve, but it belongs to a different, unrelated business: a UK
  hair salon in Saint Helens, Merseyside (address "5 Junction Lane, Saint Helens, WA9 3JN",
  UK phone, brands O+M/Everygreen, "wellbeing and nature" positioning). No mention of Naples,
  FL, Tamiami Trail, or nail services anywhere on that site. Confirmed via direct fetch of the
  domain. This is not the Naples business, so `has_own_site: false` stands for Self Love Salon
  (Naples, FL).
- Booksy dossier (`scripts/booksy_dossier.py`) gave name, address, geo, rating (5.0), review
  count (73), full 33-item service menu with prices/durations, hours, staff (Gabby), and 3
  named verbatim reviews. `website_candidates` from Booksy only pointed to the linktr.ee, not a
  real domain.
- linktr.ee/Selflove.salon was opened directly (raw HTML fetched with curl, since the rendered
  WebFetch view truncated some links): it lists Booksy booking, Google Business page, Instagram
  (@selflovesalon.nailtech), Yelp, Facebook, and a WhatsApp link (`wa.me/3054677751`), plus a
  `mailto:Selflove.salon101@gmail.com` link embedded in the page markup.
- Phone found: +1 (305) 467-7751 (via the linktree WhatsApp button; not published directly on
  Booksy).
- Email found: Selflove.salon101@gmail.com (mailto link inside the linktree page HTML).
- Instagram bio (instagram.com/selflovesalon.nailtech) could not be fetched directly (429 rate
  limit on the attempt), but the handle, owner name (Gabby Ruiz), and address were all
  independently confirmed via Booksy and the linktree, so no data here depends on the IG bio.
- Facebook page found via linktree: facebook.com/profile.php?id=100076276538014 (listed under
  the Booksy dossier's `same_as` as belonging to Gabby Ruiz).

Because a public email was found, `outreach: draft` (not `pending_manual`) in the registry.

## Email (draft, for future manual send if approved)

Subject: A free sample website for Self Love Salon

Hi Gabby,

My name is Michael Vargas. I came across Self Love Salon on Booksy, 5.0 stars with 73
reviews, genuinely impressive. I noticed the salon does not have its own website yet, just the
Booksy booking page and social links, so I went ahead and built a free sample site for Self
Love Salon to show what it could look like:

https://siteforge-demos.odd-forest-9504.workers.dev/self-love-salon-naples/

It uses your real menu, prices, and reviews from Booksy, nothing invented. It does not touch
your booking system at all; the "Book" buttons still send people straight to your Booksy page.

No obligation here. If you like it, I can help you put it on your own domain. If not, no
worries at all, feel free to ignore this.

Best,
Michael Vargas
Merktop

(Sender for actual send: Michael Vargas <michael@go.merktop.com>, reply-to jose@merktop.com,
tag campaign=siteforge. NOT sent, awaiting human approval per pipeline rules.)

## DM / WhatsApp message (dm_message, English, under 450 characters)

Hi Gabby! I came across Self Love Salon on Booksy, 5.0 stars with 73 reviews, and love the
work you do. I noticed you don't have your own website yet, so I put together a free sample
site for you: https://siteforge-demos.odd-forest-9504.workers.dev/self-love-salon-naples/ No
strings attached, just wanted you to see it. Let me know what you think!

(348 characters, fits WhatsApp/DM box in registry as `dm_message`.)

## Status

Not sent. Awaiting explicit human approval for this batch before any email or DM goes out, per
pipeline Fase 5 rules. No outbound contact has been made with this business.
