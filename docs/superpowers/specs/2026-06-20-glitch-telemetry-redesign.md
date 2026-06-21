# Zero to Shipping — "Glitch Editorial + Telemetry" Redesign

**Date:** 2026-06-20
**Goal:** Redesign Zero to Shipping to match the design language of the reference
site `irl-stream-site` ("glitch editorial + telemetry"), and aggressively cut the
current wall-of-prose so the page is punchy and scannable.

## Why

The current site reads as heavy, prose-first. The reference site is terse, visual,
and scannable: near-black background, mono kickers, telemetry stat blocks, grain +
glow atmosphere, scanline dividers, glitch headline, and an interactive "finder."
We port that system onto Zero to Shipping while keeping its own brand (green primary).

## Decisions (locked)

- **Palette:** Keep **green `#34d399` as primary**; **cyan `#22d3ee` secondary**;
  near-black `--bg:#07060c`; gradient `green → cyan`. Magenta `#e879f9` used sparingly
  as the tier-3 accent only.
- **Prose:** Aggressive cut — convert paragraphs to kickers, short lines, stat
  blocks, and cards. Match reference density.
- **Finder:** Yes — a "Where are you now?" Signal Check that recommends a tier.
- **Scope:** Everything — `index.html`, `apply.html`, `course/` (dashboard + reader).
- **Fonts:** All in — **Archivo Black** (display), **Archivo** (body),
  **Space Mono** (mono).

## Design System (`styles.css`)

Single shared token set drives all pages so landing, apply, and course stay
consistent. The course's existing `--accent/--panel/--line/--mono/--ink/--muted/--font/--radius`
token names are preserved (re-pointed to new values) so `course.css` keeps working.

### Tokens
```
--bg:#07060c;  --panel:#0c120f;  --line:#1b2620;
--accent:#34d399 (green, primary);  --cyan:#22d3ee;  --magenta:#e879f9;
--ink/--text:#e7e9ee;  --body:#94a3b8;  --muted:#64748b;
--grad: linear-gradient(90deg, var(--accent), var(--cyan));
--font (body): "Archivo"; --font-display: "Archivo Black"; --mono: "Space Mono";
--radius:10px; --max/--wrap:1140px;
```
Google Fonts link swapped to `Archivo:wght@400;600;700&Archivo+Black&Space+Mono:wght@400;700`
on every page. `theme-color` → `#07060c`.

### Shared atmosphere / components
- `.grain` + `.glow` fixed overlays (`aria-hidden`), `z-index` layering with
  `main/header/footer` above.
- `.scanline` divider with animated traveling highlight between sections.
- `.reveal` scroll-in (already present) retained.
- `.glitch` text-shadow tick animation on hero headline only.
- `.kicker` mono uppercase label; `.status-dot` (`● ONLINE`-style); `.mono`.
- `.btn` gradient fill + lift; `.btn-ghost` outline.
- All animation gated behind `@media (prefers-reduced-motion: reduce)`.

## Page: `index.html`

Replace Inter/JetBrains markup-level assumptions; keep the SVG icon sprite and the
existing reveal + checkout `<script>`. Sections, top to bottom:

1. **Nav** — wordmark/logo + `● READY` status dot + "Start now" gradient CTA; sticky,
   blurs on scroll.
2. **Hero (split)** — `// BUILT BY A DEV WHO SHIPS PAID WORK WITH AI` kicker →
   `h1.glitch` keeping the **existing headline verbatim**: "You don't need to learn
   to code. <span class="accent">You need to learn to drive AI.</span>" → primary CTA →
   telemetry `<dl>` stats: `01 · YOUR FIRST CHAT`, `→ CLAUDE CODE`, `1 · THING SHIPPED`.
   Keep `hero-dev.webp` art.
3. **The AI gap** — kicker + 3–4 one-liners (was ~5 paragraphs). ~80% less text.
4. **What you walk away with** — 4 feature cards restyled as glitch cards with mono
   labels; keep icons.
5. **Signal Check finder (new)** — `// WHERE ARE YOU NOW?` + three `.finder-tile`
   buttons (`NEVER USED AI` / `I USE CHAT` / `READY TO SHIP`); a live `aria-live`
   mono line names the recommended tier and adds `is-rec` to the matching pricing
   card (and `has-pick` dims the others), mirroring the reference finder.
6. **Pricing** — 3 tier cards, tier-coded accents (green / cyan / magenta), mono
   prices, "Most popular" badge on Ship It, `data-tier` hooks for the finder.
7. **Proof** — browser-framed shots kept; surrounding prose cut to a kicker + 2 lines.
8. **Founding students** — compressed to ~3 short lines in a bordered panel.
9. **FAQ** — converted to `<details class="qa">` `+/–` accordions.
10. **CTA band** — keep rocket bg; headline + one line + CTA.
11. **Footer** — wordmark, links, mono tagline `// CHAT → SHIPPED.`

Scanline dividers between major sections.

## Page: `apply.html`

Re-skin only. Same form fields, same JS/endpoint, same honeypot. Add kicker header
(`// APPLY · GET LAUNCHED`), panel-style inputs with mono labels, gradient submit,
grain/glow + nav/footer consistent with landing. No logic change.

## Course app: `course/index.html`, `course/lesson.html`, `course/course.css`

Keep ALL JS (`curriculum.js`, `progress.js`, inline renderers) untouched. Restyle:
- Update font link + add grain/glow overlays + nav consistency.
- `course.css`: mono module numbers in `--cyan`, gradient progress `.fill`, scanline
  touches, `is-rec`-free (no finder here). Keep lesson reader layout; just adopt new
  tokens (green `--accent` already aligns).

## New / changed files

- `styles.css` — rewritten design system (new tokens + components), backward-compatible
  token names.
- `index.html` — restructured markup + tightened copy + finder markup; inline finder JS
  (small enough to inline alongside existing script; no separate file needed).
- `apply.html` — re-skinned markup, font link, overlays.
- `course/index.html`, `course/lesson.html` — font link + overlays + nav tweaks.
- `course/course.css` — token-aligned restyle.
- `favicon.svg` — unchanged (still valid).

## Non-goals

- No copy rewrite beyond tightening; no new images/screenshots.
- No Stripe/Apps Script endpoint changes.
- No build step — remains static HTML/CSS/JS.
- No `products/`, `inStock`, or backpack concepts (irl-only).

## Testing / verification

- Existing `tests/` (pytest) must still pass — they assert on copy/CTA/pricing/curriculum
  presence. Tightened copy must preserve the strings those tests check (verify each test
  before cutting a line it asserts on).
- Manual: load `index.html`, `apply.html`, `course/index.html`, `course/lesson.html`;
  confirm finder highlights tiers, FAQ accordions toggle, reduced-motion disables
  animation, mobile layout holds.
