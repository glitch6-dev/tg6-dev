# TG6-Dev site consolidation — design

**Date:** 2026-06-29
**Status:** Approved (design); pending spec review → implementation plan

## Goal

Collapse two overlapping repos into **one** digital-services website. Keep
`Repos/ai-training` as the base, broaden it into the full TG6-Dev digital-services
site (AI Training becomes one service among several), migrate everything worth
keeping out of `Repos/DigitalServices`, then delete DigitalServices.

`irl-stream-site` (domain **teamglitch6.com**) is a separate product and is **out
of scope** for this work.

## Domains

| Site | Repo | Domain |
|------|------|--------|
| Digital-services hub (this work) | `glitch6-dev/ai-training` → rename to `tg6-dev` | **tg6-dev.com** |
| IRL backpack storefront (untouched) | `irl-stream-site` | teamglitch6.com |

## Decisions (locked)

1. **Service breadth:** curated middle set (not the full DS catalog, not the lean 5).
2. **Contact:** port the live contact form (Sheets + email); keep mailto out.
3. **Repo:** rename `ai-training` → `tg6-dev` (local + GitHub).
4. **recurring-costs.html:** keep it.

## 1. Repo identity & domain

- Rename local dir `Repos/ai-training` → `Repos/tg6-dev`.
- Rename GitHub repo `glitch6-dev/ai-training` → `glitch6-dev/tg6-dev`. **GATED:**
  outward action — user runs/approves (never-push-without-consent rule).
- Replace every `REPLACE_WITH_DOMAIN` occurrence → `tg6-dev.com` across:
  canonical link, og:url, og:image, twitter:image, `sitemap.xml`, `robots.txt`,
  and any other page (`ai-training.html`, `apply.html`, `privacy.html`,
  `terms.html`, `404.html`, `contact.html`, `recurring-costs.html`).
- **Pre-req:** commit the current dirty working tree first (favicon reorg +
  page edits already staged) so migration lands on a clean base. Local commit
  only — no push.

## 2. Curated service catalog (final, approved)

Homepage service cards:

1. **Website Design & Build** — **explicitly advertises E-commerce / online stores** as a named capability within this card (copy + sub-bullet), not as a separate card
2. **SEO & Local Search**
3. **Branding & Design**
4. **Custom Software & Automation** — merges DS's Custom Software + Automation/Bots + Data Pipelines
5. **Hosting, Security & Care** — merges Hosting/Security/Data + Care Plans
6. **Security & Pentest** — billable tg6-soc angle, distinct from hosting security
7. **AI Training** — original offering, now one card → `ai-training.html`
8. **Consulting**

Dropped as thin/overlapping: Database Design, Security Training. E-commerce is
**not** dropped — it is advertised inside the Website Design & Build card rather
than as its own card.

## 3. Contact / lead capture

- Port DigitalServices' `contact.html` + `apps-script/Code.gs` (appends to a
  Google Sheet + emails `dvelupr@proton.me`) into the site as the primary
  "Get a quote" path.
- Rewire homepage service-card CTAs from per-service `mailto:` links to the
  contact form.
- Keep `apply.html` unchanged for AI Training applications (its own Apps Script
  endpoint + Sheet).
- Result: two forms — general quote (`contact.html`) + training application
  (`apply.html`). Their Apps Script endpoints/Sheets stay separate.

## 4. Migrate from DigitalServices, then delete it

Carry over:
- **GA4 analytics** snippet → all pages.
- **`recurring-costs.html`** transparency page → footer-linked.
- **Portfolio/proof** — reconcile DS's project list with ai-training's existing
  "Paid client work I designed, built, and run" section; keep the real shipped
  projects, no duplicates.
- **`tools/gen_assets.py`** + bundled fonts → into the repo's tools/.

Do **not** migrate now:
- **Stripe catalog tiles** — Stripe card payments are still blocked (not
  activated in dashboard), so the quote form stays the conversion path. Stripe
  folds in a later pass. (YAGNI for this consolidation.)

Then delete DigitalServices:
- Local dir `Repos/DigitalServices`.
- GitHub repo `glitch6-dev/DigitalServices`. **GATED:** irreversible + outward —
  user runs/approves.

## 5. Order of operations

Reversible until the gated steps:

1. Commit ai-training's dirty working tree (local).
2. Migrate: contact form + apps-script, GA4 snippet, recurring-costs.html,
   portfolio reconciliation, tools/gen_assets.py + fonts.
3. Curate the homepage service catalog (§2) + swap CTAs to the contact form.
4. Domain swap: `REPLACE_WITH_DOMAIN` → `tg6-dev.com` everywhere.
5. Rename local dir → `Repos/tg6-dev`.
6. **[GATED]** GitHub repo rename + push (user approves each push).
7. **[GATED]** Delete DigitalServices — local dir + GitHub repo (user approves).

## Out of scope

- `irl-stream-site` / teamglitch6.com — untouched.
- Stripe activation and tiles — later pass.
- Any deploy/hosting wiring beyond domain placeholder swap.

## Risks / notes

- The contact form posts `no-cors`, so the browser can't read success/failure
  (known limitation, carried from DS) — verify via the Apps Script execution log
  and a live test submission after go-live.
- Two Apps Script deployments must each have their `/exec` endpoint set correctly
  (one for contact, one for apply); endpoints are not committed to the repo.
- Footer/nav links must be updated to include recurring-costs, contact, privacy,
  terms consistently across all pages.
