# Outreach draft: Restore Therapeutic Massage & Spa (restoretherapeuticlakeland)

- **Status**: pending_approval (do NOT send without explicit user OK)
- **To**: no public email found. Deep search performed: Booksy business page (phone/email fields
  both empty), Facebook page (facebook.com/monicapiconLMT, About section not reachable without a
  login session), Instagram bio (instagram.com/monicapdlmt, blocked by Instagram/WebFetch with a
  429 on every attempt in this session, so bio text and any business_email were not visible),
  Vagaro listings (two legacy profiles, vagaro.com/restoretherapeuticmassageandspa and
  vagaro.com/restoretherapeuticmassage1, neither exposes an email publicly), Healthgrades provider
  listing (phone only, no email), and the domain-squatted lookalikes below (parked pages, no
  contact form). No email surfaced anywhere. Best real channels: phone and Facebook/Instagram DM.
- **From**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-restoretherapeuticlakeland-2026-08-01
- **Angle**: no website found (has_own_site: false). Checked and ruled out: restoretherapeuticmassage.com
  resolves but belongs to an unrelated business in Illinois (same generic name, confirmed via page
  content showing `"state":"IL"`, no Lakeland/Picon reference anywhere); restoretherapeuticspa.com
  and restoretherapeuticmassagespa.com both return HTTP 200 but are empty domain-parking stubs
  (114-byte page that just redirects to `/lander`); restoretherapeuticmassage.net does not resolve
  (DNS NXDOMAIN) despite being indexed by search engines as a stale/dead listing. Two Vagaro
  booking-platform pages exist (subdomains, do not count as an own site) alongside their current,
  active Booksy listing. No independent, real, loading website was found anywhere.
- **Language**: English (all Booksy reviews and business copy are in English; Lakeland is not a
  majority-Hispanic market like the previous Miami-area builds).
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/restoretherapeuticlakeland/
  (built locally, gate-passed; NOT deployed/live in this session, see build note below)
- **Available channel**: no public email. Registered as `outreach: pending_manual`, with phone
  (813) 876-8771 and Facebook facebook.com/monicapiconLMT / Instagram @monicapdlmt as the channels
  for manual outreach (call or DM).
- **Note on research / rating verification**: rating and review count (5.0, 110 reviews) come
  directly from the live Booksy JSON-LD for this listing (`booksy_dossier.py`, fetched 2026-08-01),
  cross-checked against the Booksy category/search page for "massage" in Lakeland (booksy.com/en-us/s/massage/16013_lakeland,
  fetched independently via a second tool call) which shows the same business, same rating, same
  110 review count at the same address. Two independent Booksy surfaces agreeing satisfies the
  cross-verification requirement.
- **Note on phone**: (813) 876-8771 is NOT published on the Booksy listing itself (Booksy's phone
  field is empty). It comes from a Healthgrades provider listing for "Monica Picon, LMT" in
  Lakeland, FL (a healthcare directory that sources numbers from the NPI registry), which matches
  her exact name, license type and city. The Healthgrades address on file (1826 N Crystal Lake Dr)
  differs from the current Booksy studio address (4530 E County Road 540A), likely an older
  registered location, but the phone number is presented with that caveat understood: it is the
  best available real number, not confirmed by the business's own current listing. Worth a light
  verification call before relying on it for anything beyond a first outreach attempt.
- **Note on business identity / owner**: staff name and full bio (LMT since 2014, Physical
  Therapist Assistant since 2023, certified in manual lymphatic drainage, specializing in
  therapeutic medical massage and post-surgery massage) come verbatim from the Booksy staff
  description field for "Monica Picon" on this listing.
- **Note on Instagram handle**: @monicapdlmt was identified via a web search whose indexed page
  title read "Monica Picon @ Restore Therapeutic Massage ..." for instagram.com/monicapdlmt,
  tying the handle to both the owner's name and the business name. Instagram itself returned
  HTTP 429 on every direct fetch attempt in this session (both curl/Playwright, which get a
  network-level connection reset in this sandbox, and the WebFetch tool, which got rate-limited),
  so the bio text, follower count and any business_email field could not be directly inspected.
  The handle is used on the site as the best-evidenced real link; it was not possible to fully
  confirm bio content or find a bio email.
- **Note on reviews**: 3 named, verbatim, star-rated reviews were recoverable from the Booksy
  JSON-LD reviews array: Tony S. ("Excellent care"), Bethany M. ("Spectacular!"), and Kristina B.
  ("Monica is a wonderful therapist!! I feel great for days after getting a massage. Highly
  recommend her!!"). These meet the 3-quote minimum, so the site uses `social_proof.modo:
  "testimonios"` with these exact quotes and first-name-plus-last-initial as published by Booksy
  (no invented surnames). Several longer unattributed reviews also exist on the listing but were
  not used as quotes since they lack a name.
- **Note on services/pricing**: all 18 services and prices (Therapeutic Massage $85/1h and
  $45/30min, Deep Tissue $85/1h, Sports Massage $80/1h, Cupping $35/30min, Manual Lymphatic
  Drainage $90/1h upper body up to $180/2h full body, several post-op/multi-session packages)
  come directly from the Booksy JSON-LD service catalog for this listing. The site surfaces the
  4 most representative services with their real prices; the note text points to Booksy for the
  full menu and multi-session packages.
- **Note on photos**: 14 photos were downloaded from the Booksy gallery for this listing. All 14
  decode as valid JPEGs and were visually reviewed one by one (not by filename) before selection.
  6 were used in the final site (storefront exterior, a therapist portrait, an assisted-stretch
  technique photo, and 3 close-up massage/technique shots), all genuine photos of Monica Picon's
  studio and practice, no stock imagery. Excluded from the gallery per the curation rules: 4 images
  that were clearly reviewer/client profile photos unrelated to the business (a man in sunglasses,
  a woman at a bar, a dark portrait, a woman with a baby) and 1 pre-op surgical-marking photo that
  was too clinical/unflattering for a public gallery. The owner portrait (bk-10.jpg) was placed
  only as the small avatar in the About section, never as a gallery tile, per the no-owner-portraits-
  in-gallery rule.
- **Note on build**: light-v2 skeleton (Lash Bloom base, plum-pink accent) recolored with a hue
  shift (dh=-150, ds=+6, dl=-2 via `scripts/_forge/recolor.py`) to a deep teal palette
  (`--accent-deep: #409ca0`, `--bg: #eaf8f8`), matching the business's own teal-and-gold "Restore"
  logo and distinct from the two other massage/bodywork builds already in the registry
  (by-orly-massage-brickell uses a dark emerald green, king-salomons-massage-naples uses a dark
  caramel/bronze). One inline color that had leaked outside the protected merktop-badge CSS block
  (`text-[#f4eee2]` on the "Powered by Merktop" label) was manually reverted to its original value
  after the automated recolor pass, so the badge text stays on-brand gold as required.
  `python3 scripts/gate.py restoretherapeuticlakeland --lang en --forbid "Lash Bloom,Yesi,West
  Palm Beach,Cresthaven,519855,lash,eyelash"` returned GATE OK on the first run. Manually verified
  with Playwright: no horizontal overflow at 390px, all reveal-on-scroll content renders correctly
  once scrolled into view (desktop 1440px and mobile 390px full-page screenshots checked), JSON-LD
  parses, and all referenced images resolve on disk.
- **Note on deploy**: this session has no Cloudflare deploy credentials
  (`CLOUDFLARE_API_TOKEN` not set, `wrangler` not authenticated) and the task instructions
  prohibit touching `data/processed.json` or running `scripts/publish.py`. The site is fully
  built and gate-passed in `output/restoretherapeuticlakeland/` but has NOT been deployed or
  verified live in this session. A session with deploy credentials needs to push/deploy before
  the demo URL above actually resolves.

## Subject (for if an email surfaces later)

A sample website for Restore Therapeutic Massage & Spa (it's ready)

## Body (reference, for email or as the base for a longer DM)

Hi Monica,

I'm Michael, from Merktop. I came across Restore Therapeutic Massage & Spa looking at massage
therapists in Lakeland, and a perfect 5.0 across 110 reviews on Booksy really stood out.

I noticed you don't have your own website, just Booksy and Facebook, so I went ahead and built
you a sample one with your real photos, your real services and prices, and your real rating:

https://siteforge-demos.odd-forest-9504.workers.dev/restoretherapeuticlakeland/

Two things worth knowing:
- It doesn't touch how you run things today. Every booking button still points straight to your
  Booksy page, exactly like it works now.
- All the photos, services and reviews are pulled from your real Booksy listing, nothing made up.

If you like it, I can put it on your own domain. If it's not for you, I'll take it down, no hard
feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Short version for DM / phone text (dm_message)

Hi Monica! I'm Michael from Merktop. I found Restore Therapeutic Massage & Spa on Booksy, 5.0 rating from 110 reviews, and noticed you don't have your own website yet. I built a free sample site with your real photos and services: https://siteforge-demos.odd-forest-9504.workers.dev/restoretherapeuticlakeland/ It does not touch your Booksy booking. Like it, I can put it on your own domain. Not for you, I will take it down, no strings attached.
