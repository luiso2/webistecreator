# Outreach draft: Pet Stylez Grooming and Boarding (pet-stylez-kissimmee)

Status: DRAFT ONLY. Not sent. Requires explicit human approval before sending (PIPELINE.md fase 5).

- Business language: English (IG bio and majority of reviews are in English; 2 of 3 named reviews happen to be in Spanish, kept verbatim in their original language per DESIGN.md).
- has_own_site: false -> angle: "I built you a sample website". Only public web presence found: Instagram (@pet_stylez), Facebook (facebook.com/petstylezgrooming), and a Square booking micro-site (pet-stylez-grooming.square.site), none of which count as an owned domain.
- Public email: NOT FOUND after a genuine multi-source search (Instagram web_profile_info API: business_email/public_email both null; bio external_url only points to the Booksy booking page; Facebook page is login-walled from this environment; Square booking micro-site is JS-rendered and returns no contact info via curl/WebFetch; web search turned up no email). Recorded as `email: null`.
- Phone: NOT FOUND (Instagram API fields public_phone_number/contact_phone_number both null; Facebook login-walled; web search only surfaced a phone number for a different, unrelated business, "Fusion Pet Stylez" at 2660 Simpson Rd, which was correctly NOT used). Recorded as `phone: null`.
- Outreach channel: no email possible. `outreach: pending_manual` via Instagram DM (@pet_stylez) using the dm_message below.
- Sender (if an email channel is ever found): Michael Vargas <michael@go.merktop.com>, reply-to jose@merktop.com, tag campaign=siteforge
- Demo URL: https://siteforge-demos.odd-forest-9504.workers.dev/pet-stylez-kissimmee/

---

**Subject:** A sample website for Pet Stylez Grooming and Boarding

Hi there,

I came across Pet Stylez while looking at well-reviewed dog groomers in Kissimmee. A perfect 5.0 rating across 69 reviews on Booksy is genuinely great, and it is easy to see why once you read them, people keep saying their dogs come home looking (and acting) like their best selves.

I noticed you do not have your own website yet (just Instagram, Facebook and your Square booking page), so I went ahead and built you a sample one using your real photos and real reviews, to show what it could look like:

https://siteforge-demos.odd-forest-9504.workers.dev/pet-stylez-kissimmee/

It does not touch how you take appointments at all. Booking still goes straight to your Booksy page exactly like it does now.

If you like it, I can help put it on your own domain. If not, no problem at all, just let me know and I will take it down, no strings attached.

Best,
Michael Vargas
Merktop

---

## dm_message (for Instagram DM, max 450 chars, English)

Hi! I built a sample website for Pet Stylez using your real 5.0 rating (69 reviews) and real photos: https://siteforge-demos.odd-forest-9504.workers.dev/pet-stylez-kissimmee/ It does not touch your Booksy booking at all, just links straight to it like now. Happy to put it on your own domain, or take it down if it is not for you, no strings attached. Michael Vargas, Merktop

(375 characters)

## Note on contact channel

No public email or phone was found for this business despite checking the Instagram bio and API fields, the Facebook page (login-walled), the Square booking micro-site (JS-rendered, no contact data via curl), and a web search. The realistic outreach path is an Instagram DM to @pet_stylez using the dm_message above. This should be registered as `outreach: pending_manual`.
