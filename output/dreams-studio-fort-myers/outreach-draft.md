# Outreach draft: Dreams Studio (Fort Myers, FL)

Status: NO public email found. Do not send anything. Drafts below are for future reference
only, in case a human finds a direct contact later (WhatsApp is the only verified channel).

## Email (draft, no recipient yet)

Subject: A free sample website for Dreams Studio

Hi Yilian and Claudia,

I came across Dreams Studio on Booksy, 5.0 rating from 24 reviews, and noticed you do not
have a website of your own yet, just the Booksy page. So I put together a free sample site
for you with your real lash and brow menu, your prices, your photos and your reviews:

https://siteforge-demos.odd-forest-9504.workers.dev/dreams-studio-fort-myers/

It does not touch your Booksy booking at all, clients would still book the exact same way.
If you like it, I can help you put it on your own domain. If not, no problem, I will take
it down, no obligation either way.

Michael Vargas
Merktop

## dm_message (WhatsApp/DM, English, under 450 chars)

Hi! I found Dreams Studio on Booksy, 5.0 rating with 24 reviews, but no website of your own yet, so I built a free sample one with your real lash menu, photos and reviews: https://siteforge-demos.odd-forest-9504.workers.dev/dreams-studio-fort-myers/ It does not touch your Booksy booking. Happy to put it on your own domain if you like it, or take it down, no obligation either way. Michael, Merktop.

(400 characters)

## Contact research notes

Channels checked for a public email, in order:
1. `linktr.ee/Dreamstudio3` (the linktree in their Booksy/IG bio): opened and listed every
   link. Contains a Booksy booking widget link, a WhatsApp link (`wa.me/2394704217`), TikTok
   (`@dreams_studio_oficial`) and Instagram (`@dreams_studio_oficial`). No email link anywhere
   on the page.
2. Instagram profile `instagram.com/dreams_studio_oficial/`: direct fetch returned HTTP 429
   (rate limited) and the `web_profile_info` API endpoint returned 401 "please wait a few
   minutes" (both known-broken per FORGE-BRIEF). Not retried further since 16 real photos
   were already available from the Booksy dossier (well above the 5-photo minimum), so an
   IG photo/bio rescue was not needed. Bio/email could not be confirmed through this channel.
3. Booksy listing HTML (`booksy.com/en-us/1001801_dreams-studio_brows-lashes_15819_fort-myers`):
   fetched raw HTML and grepped for `mailto:` and email patterns. None found. No phone
   published either (`data.json` phone field is null from the dossier).
4. Facebook: found a candidate page "Dreams Studio | Fort Myers Estates FL"
   (facebook.com/100078751692561/) via web search, but Facebook served a login wall on
   fetch, so the About section could not be read. Unconfirmed as this business's page.
5. Domain checks: `dreamsstudiofl.com` does not resolve (confirmed, matches the brief).
   `dreamsstudio.com` resolves (HTTP 200) but is an unrelated art portfolio site for an
   artist named Claudio Berni, not this business. `dreamslashbrowstudio.com` ("DREAM'S
   STUDIO", note the apostrophe) turned up in a general web search and does load, but its
   contact page 404s and its homepage text contains no mention of Fort Myers, Evans Ave, or
   any matching phone/address, so it could not be confirmed as the same business. Treated as
   unrelated/unverified, not counted as an owned site.

Conclusion: `has_own_site: false` (no real, confirmed website of their own). `email: null`.
The only verified direct contact channel is WhatsApp, sourced from their own linktree:
+1 (239) 470-4217 (`wa.me/2394704217`, missing the country code prefix on the linktree link
itself, added `+1` here since 239 is a Fort Myers area code).

## Business identity notes
- Two Booksy listings exist for "Dreams Studio" in Fort Myers. `1001801` (used for this
  build) is the active one: it resolves with the full menu, 24 reviews, staff (Yilian,
  Claudia Castro), rating 5.0, and matches the Booksy widget link published on their own
  linktree. The second id mentioned in the brief, `1542423`, no longer resolves to a
  business page (Booksy redirects it to a category listing), confirming `1001801` is the
  correct, current listing.
- Booksy's own `sameAs` field listed Instagram handle `myspace.oficial`, which looks like a
  mismatched/incorrect scrape on Booksy's side. The real handle, confirmed directly from the
  business's own linktree (`linktr.ee/Dreamstudio3`), is `@dreams_studio_oficial`. Used that
  one for the site and JSON-LD instead.
- Owners: "Castro Sisters" per the linktree bio, matching staff name "Claudia Castro" from
  the Booksy dossier plus "Yilian".
