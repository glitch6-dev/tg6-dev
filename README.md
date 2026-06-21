# Zero to Shipping — course sales site

Static three-tier sales site for the *Zero to Shipping* program — learn to drive AI, from your first browser chat to building and shipping real things with Claude Code.

- `index.html` — landing + pricing (Build It $49 / Ship It $499 / Get Launched $2,999)
- `apply.html` — Tier 3 application form (posts to Apps Script)
- `privacy.html` / `terms.html` — legal pages
- `404.html` — not-found page (uses root-absolute paths; serve at domain root)
- `course/` — self-paced course dashboard + lesson reader (data-driven)
- `apps-script/` — application backend (Sheet + email)
- `styles.css` — shared design system (glitch editorial + telemetry)

## Assets to upload (placeholders left in place)

Drop these into `assets/` and the marked spots pick them up automatically:

- `assets/hero-dev.webp` — hero image (split layout). Restore the commented
  `<img>` in `index.html` and delete the `.art-ph` placeholder.
- `assets/ship-rocket.webp` — CTA-band background image. Restore the commented
  `<img class="bgimg">` in `index.html`.
- `assets/og-cover.png` — 1200×630 social share image (referenced by the OG/Twitter
  tags in `index.html` and `apply.html`).
- `assets/proof-tg6dev.png` and `assets/proof-storefront.png` — real screenshots
  for the "Real work" section. In `index.html`, swap each `.ph` placeholder
  `<div>` for the commented `<img>` directly above it.

## Go-live checklist

1. **Domain:** publish to the new domain. Add a `CNAME` file containing just the
   bare domain (e.g. `example.com`) for GitHub Pages, then replace
   `REPLACE_WITH_DOMAIN` in `robots.txt`, `sitemap.xml`, `index.html`,
   `apply.html`, `privacy.html`, and `terms.html` (canonical + OG/Twitter URLs).
2. **Apps Script:** follow `apps-script/README.md`, then paste the `/exec`
   URL into `ENDPOINT` in `apply.html`. Tier 3 applications work after this —
   no Stripe required.
3. **Stripe (when Cards are activated):** create a Payment Link for Tier 1
   ($49) and Tier 2 ($499), then paste them into `TIER1_CHECKOUT_URL` and
   `TIER2_CHECKOUT_URL` in `index.html`. Until then the buttons show a
   "checkout opens soon" message — Tier 3 still works.
4. **Validation goal:** first paid sale (any tier) validates the offer →
   green-light full course production.

## Tests

`python3 -m pytest tests/ -v`
