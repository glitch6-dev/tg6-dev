# TG6-Dev · AI Training — course sales site

Static three-tier sales site for the *TG6-Dev · AI Training* program — learn to drive AI, from your first browser chat to building and shipping real things with Claude Code.

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

1. **Domain — `tg6-dev.com`:** the site targets `tg6-dev.com`. All canonical,
   OG/Twitter, robots.txt, and sitemap URLs already contain this domain (the
   `REPLACE_WITH_DOMAIN` placeholder has been swapped). To deploy on GitHub
   Pages add a `CNAME` file containing just `tg6-dev.com`; point the DNS
   A/CNAME records at GitHub's IPs, then enable GitHub Pages in the repo
   settings.

2. **Apps Script — two endpoints:**
   - **Application form** (`apply.html`) → `apps-script/Code.gs`. Follow
     `apps-script/README.md`, deploy as a Web App, and paste the `/exec` URL
     into the `ENDPOINT` constant in `apply.html`. Tier 3 applications flow to
     a Google Sheet + email after this step.
   - **Contact form** (`contact.html`) → `apps-script/contact/Code.gs`. Deploy
     that script separately and paste its `/exec` endpoint into `contact.html`.
     General contact enquiries work after this step.

3. **Stripe (card payments pending activation):** Stripe checkout for the AI
   Training tiers is wired on `ai-training.html`, but card payments are still
   pending activation in the Stripe dashboard. Once Cards are activated, create
   Payment Links for Tier 1 ($49) and Tier 2 ($499) and paste them into
   `TIER1_CHECKOUT_URL` and `TIER2_CHECKOUT_URL` in `ai-training.html`. Until
   then the buttons show a "checkout opens soon" message — the Tier 3
   application form works without Stripe.

4. **Validation goal:** first paid sale (any tier) validates the offer →
   green-light full course production.

## Tests

`python3 -m pytest tests/ -v`
