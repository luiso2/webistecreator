# Outreach draft: Friends Day Spa & Salon (friendsdayspa)

- **Status**: pending_approval (do NOT send without explicit user OK)
- **To**: no public email found. Deep search performed: Fresha business profile (GraphQL
  location object has no email field exposed publicly, only `contactNumber`), no dedicated
  Instagram or Facebook page linked from the Fresha profile (only Fresha's own corporate
  social icons appear in the page footer), domain guesses `friendsdayspaandsalon.com` and
  `friendsdayspa.com` do not resolve (no website to pull a contact address from), no
  linktree/beacons page found. Best real channel: phone.
- **From**: Michael Vargas <michael@go.merktop.com>
- **Reply-To**: jose@merktop.com
- **Tag**: campaign=siteforge
- **Idempotency-Key**: siteforge-friendsdayspa-2026-08-01
- **Angle**: no website found (has_own_site: false). Their only online presence found is their
  Fresha booking profile; `friendsdayspaandsalon.com` and `friendsdayspa.com` do not resolve
  (DNS failure), and no other domain candidate surfaced in the Fresha listing or in aggregator
  results.
- **Language**: English (Fresha profile description, all 10 recovered verbatim reviews, and
  service names are in English).
- **Demo**: https://siteforge-demos.odd-forest-9504.workers.dev/friendsdayspa/ (built locally,
  gate-passed; NOT deployed/live in this session, see build note below)
- **Available channel**: no public email, no confirmed social account. Registered as
  `outreach: pending_manual`, with phone (904) 215-6585 as the only channel found for manual
  outreach (call).
- **Note on research (rating/reviews)**: rating (5.0) and review count (216) were read directly
  from Fresha's own first-party GraphQL data embedded in the business's live booking page
  (`__NEXT_DATA__` -> `props.pageProps.data.location.reviews`), not a third-party aggregator.
  Internal consistency check: `rating5Count: 216` with all other star buckets at 0, summing
  exactly to `totalCount: 216`, average 5.0 (this is the business's own platform of record,
  where every review is tied to a paid, verified booking). Yelp, TripAdvisor and Google Maps
  could not be cross-checked directly in this session (403/blocked to automated fetches without
  a residential browser), so the rating is read first-hand off the booking platform rather than
  triangulated across aggregators; documenting this gap rather than fabricating a second source.
- **Note on reviews**: 10 named, verbatim reviews were recovered from the same Fresha GraphQL
  payload (author first name + last initial, matching Fresha's own display convention, e.g.
  "Karen K", "Heather K", "Ethel W", "Vee W", "Robbin T", "William E"). Multiple reviews name
  specific staff (massage therapists Kristina and Rose, esthetician Madison) which reads as
  genuine repeat-client testimony. Three of the strongest, most detailed quotes were used
  verbatim in the site's testimonials section (`social_proof.modo: "testimonios"`); one is
  attributed "Anonymous" per Fresha's own review-author field (kept as "Anonymous" rather than
  inventing a name, consistent with the hard rule against fabricated attribution).
- **Note on services/pricing**: all 7 listed services and their exact prices/durations came
  directly from the same Fresha payload (Swedish Massage 30min $55, Signature Massage 1h $85,
  Deep Tissue Massage 1h $95, Signature Massage 90min $125, 90 Minute Deep Tissue $150, Custom
  Facial 1h $85, LED add-on 15min $15). Nothing invented; the "also on the menu" footnote lists
  the remaining real services not shown on the 4 featured cards.
- **Note on photos**: 10 real photos downloaded from the business's own Fresha gallery (their
  venue-uploaded photos, not stock): storefront with signage, 4 different treatment/massage
  rooms, a lounge area, a salon/reception area, a close-up of finished nail art, a close-up of a
  facial/skin treatment in progress, and a close-up of a client's finished hairstyle (no face
  shown). All 10 decode as valid JPEGs and were visually reviewed via the contact sheet before
  selection; none show closed eyes mid-procedure, text/caption overlays, or staff/owner
  portraits. 9 of the 10 are used across hero/about/gallery; the 10th (`bk-7.jpg`, another
  massage room, near-duplicate of `bk-5.jpg`) was left out of the gallery to avoid repetition
  but kept on disk.
- **Note on build**: light-v2 skeleton (Lash Bloom base, plum-pink accent) kept as-is per
  pipeline precedent (derive.py does not require a palette retint; magicsbarbershop and other
  builds keep the original skeleton palette when there is no niche+city collision, which is the
  case here: no other massage/day-spa build exists yet in Middleburg/Jacksonville).
  `python3 scripts/gate.py friendsdayspa --lang en --forbid "Lash Bloom,Yesi,West Palm
  Beach,Cresthaven,519855,lash studio,_lashbloom"` returned GATE OK on the first run.
  Build note on contact channel: this business has no confirmed Instagram or Facebook, only a
  real, actively-used Fresha booking page. The dark/light-v2 skeleton hardcodes the word
  "Instagram" in two spots outside derive.py's content-driven anchors (the CTA-final section's
  secondary button, and the footer's "Follow" row) for businesses whose `ig_handle` is not a
  real Instagram handle. Following the same pattern already shipped in
  `output/king-salomons-massage-naples` (a Facebook-only business, where derive.py's literal
  "Instagram · Facebook" text was corrected post-generation to just "Facebook"), these two spots
  were corrected after running derive.py to accurately read "Call · (904) 215-6585" and "Book
  online · Fresha" respectively, instead of the incorrect auto-generated "Follow on Instagram" /
  "Instagram · Fresha". No content was invented in this correction, only an inaccurate
  auto-generated label was fixed to match the business's real, verified contact channels.
- **Note on deploy**: this session has no Cloudflare deploy credentials and the task instructions
  prohibit touching `data/processed.json` (which the normal `publish.py` step writes to as part
  of deploying/registering). The site is fully built and gate-passed in
  `output/friendsdayspa/` but has NOT been deployed or verified live in this session. A session
  with wrangler credentials needs to run the deploy + registration step before the demo URL
  below actually resolves.

## Subject (for if an email surfaces later)

A sample website for Friends Day Spa & Salon (it's ready)

## Body (reference, for email or as the base for a longer conversation)

Hi there,

I'm Michael, from Merktop. I found Friends Day Spa & Salon looking at massage and day spas in
the Middleburg/Jacksonville area, and a perfect 5.0 rating across 216 reviews really stood out,
so I looked closer at the spa.

I noticed you don't have your own website, just a Fresha booking page, so I went ahead and
built you a sample one with your real rating, real photos of the spa, and your real massage and
facial menu with prices:

https://siteforge-demos.odd-forest-9504.workers.dev/friendsdayspa/

Two things worth knowing:
- It doesn't touch how you run things today. Every "Book" button still points straight to your
  Fresha page, exactly like booking works now.
- All the photos, prices and the rating are pulled from your real Fresha profile, nothing made
  up.

If you like it, I can put it on your own domain. If it's not for you, I'll take it down, no hard
feelings either way.

Best,
Michael Vargas
Merktop . merktop.com

## Short version for phone text (dm_message)

Hi! I'm Michael from Merktop. I saw Friends Day Spa & Salon has a perfect 5.0 rating across 216 reviews on Fresha, so I built you a sample website with your real photos, menu and rating: https://siteforge-demos.odd-forest-9504.workers.dev/friendsdayspa/ It does not touch your Fresha booking at all. If you like it I can put it on your own domain, if not I will take it down, no pressure either way.
