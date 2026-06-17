# Zero to Shipping — course sales site

Static three-tier sales site for the *Zero to Shipping* course program.

- `index.html` — landing + pricing (Build It $49 / Ship It $499 / Get Launched $2,999)
- `apply.html` — Tier 3 application form (posts to Apps Script)
- `apps-script/` — application backend (Sheet + email)
- `styles.css` — shared styles

## Go-live checklist

1. **Domain:** publish to the new domain. Replace `REPLACE_WITH_DOMAIN` in
   `robots.txt` and `sitemap.xml`.
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
