# Glitch-Editorial + Telemetry Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-skin Zero to Shipping (landing, apply, course) in the `irl-stream-site` "glitch editorial + telemetry" design language — near-black, mono kickers, grain/glow, scanlines, glitch headline, telemetry stats, an interactive tier finder — while aggressively cutting prose and keeping green as the primary brand color.

**Architecture:** One shared `styles.css` token set + component library drives every page. The reference stylesheet `../irl-stream-site/css/style.css` is the canonical source for the signature components (grain, glow, scanline, glitch, finder, accordion); we port those blocks recolored to a green-primary palette. Markup in each HTML page is restructured to consume the new classes. No build step — static HTML/CSS/JS. The course app keeps all its JavaScript untouched and only adopts the new tokens/atmosphere.

**Tech Stack:** Static HTML5, hand-written CSS (custom properties), vanilla JS. Fonts via Google Fonts (Archivo, Archivo Black, Space Mono). Tests: pytest (existing suite under `tests/`).

## Global Constraints

These are project-wide and apply to **every** task. Exact values are non-negotiable; many are asserted by the existing pytest suite.

- **No build step.** Edit static files in place. Pages must serve as-is over `python3 -m http.server`.
- **Reference source of truth:** the neighbor repo at `/home/kali/Desktop/TG6/Repos/irl-stream-site` (read-only) — copy signature CSS blocks from `css/style.css` and patterns from `index.html`.
- **Palette (green primary):** `--bg:#07060c`, `--panel:#0c120f`, `--line:#1b2620`, `--accent:#34d399` (green, primary), `--cyan:#22d3ee` (secondary), `--magenta:#e879f9` (tier-3 only), `--text/--ink:#e7e9ee`, `--body:#94a3b8`, `--muted:#64748b`, `--grad:linear-gradient(90deg,var(--accent),var(--cyan))`.
- **Recolor map when porting reference CSS:** reference `--purple` → our `--accent` (green); reference `--cyan` stays `--cyan`; reference `--green` → fold into `--accent`; keep `--magenta` only for tier-3 accents. The reference's purple→cyan gradient becomes green→cyan.
- **Fonts:** Google Fonts link on every page: `https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Archivo+Black&family=Space+Mono:wght@400;700&display=swap`. `--font-display:"Archivo Black"`, `--font:"Archivo"`, `--mono:"Space Mono"`.
- **Backward-compatible tokens:** keep the token names the course already uses — `--accent --panel --line --ink --muted --mono --font --radius --max` — re-pointed to new values, so `course/course.css` keeps working. `--ink` and `--text` are aliases (same value); `--font` and `--font-body` aliases.
- **`theme-color` meta = `#07060c`** on every page.
- **Reduced motion:** all animation (`reveal`, `glitch`, `scanline::after`, finder caret, hover transitions) gated behind `@media (prefers-reduced-motion: reduce)`.
- **`index.html` invariant strings (pytest-pinned) — DO NOT remove or alter:** brand `Zero to Shipping`; lowercase tokens `ship`, `claude code`, `chat`; tier names `Build It` / `Ship It` / `Get Launched`; prices `$49` / `$499` / `$2,999`; `1-on-1`; `discord`; `coaching` or `feedback`; `limited` or `seats`; `favicon.svg`. Must NOT contain: `automation`, `free lesson`, `free course`.
- **`index.html` pricing structure invariant:** exactly **three** occurrences of the literal `data-tier="` (one per `<article>`). The finder tiles MUST use `data-level=` (NOT `data-tier=`). Tier-3 `<article>` contains `href="apply.html"` and NO `data-checkout`; tier-1/tier-2 `<article>`s contain `data-checkout="1"` / `data-checkout="2"`. Keep the JS constants `TIER1_CHECKOUT_URL` / `TIER2_CHECKOUT_URL` (both `https://buy.stripe.com/...`) and the `PASTE_STRIPE_LINK` fallback guard.
- **`apply.html` invariants (pytest-pinned):** `id="applyForm"`; field `name="..."` for each of name, email, background, goal, project, timeline, why; `name="company_url"` honeypot; `PASTE_APPS_SCRIPT_URL`; `mode: "no-cors"`. Must NOT contain `$2,999` or `data-checkout`.
- **Do not touch** `course/curriculum.js`, `course/progress.js`, `apps-script/`, or any test file.
- **Verification after every task:** `python3 -m pytest -q` must stay green, and the touched page must load over a local server without console errors.

---

### Task 1: New design system in `styles.css`

Rewrite `styles.css` as the shared design system. This file alone changes no behavior (HTML still references old classes until Task 2), but it must (a) keep the backward-compatible tokens so the course renders, and (b) define every class Task 2–4 consume.

**Files:**
- Modify (rewrite): `styles.css`
- Reference (read-only): `/home/kali/Desktop/TG6/Repos/irl-stream-site/css/style.css`

**Interfaces — Produces** (classes later tasks rely on):
- Tokens: all variables in Global Constraints.
- Atmosphere: `.grain`, `.glow` (fixed overlays), `.scanline` (divider).
- Text/util: `.kicker`, `.mono`, `.status-dot`, `.accent`, `.glitch`, `.reveal`/`.reveal.in`, `.wrap`, `.section`, `.section.alt`.
- Buttons: `.btn`, `.btn-accent`, `.btn-ghost`, `.btn-lg`, `.nav-cta`.
- Nav/footer: `.nav`, `.nav.scrolled`, `.logo`, `.foot`/`.footer`.
- Hero: `.hero-split`, `.grid`, `.eyebrow`, `.hero-actions`, `.hero-art`, `.hero-stats` (`dl` with `dt/dd`), `.trust`.
- Features: `.feature-grid`, `.feature`, `.badge-ico`, `.ico`.
- Finder: `.finder-tiles`, `.finder-tile`, `.finder-tile.is-active`, `.finder-line`, `.finder-line .caret`, `.lineup.has-pick`.
- Pricing: `.tiers`, `.tier`, `.tier.featured`, `.tier.is-rec`, `.tiers.has-pick .tier:not(.is-rec)`, `.pop`, `.price`, `.per`, `.tier[data-tier]` accent coding (1=green,2=cyan,3=magenta).
- Proof/founding: `.proof-grid`, `.proof-shot`, `.browser` (`.bar`, `.url`, `.ph`), `.founding`.
- FAQ: `details.qa`, `details.qa summary`, `.qa-body`.
- CTA band: `.cta-band`, `.bgimg`, `.scrim`, `.cta-center`.

- [ ] **Step 1: Replace the token block + base.** Open `styles.css`. Replace the entire `:root{…}` and base rules with the new tokens (Global Constraints values) plus base reset. Set body font to `var(--font)`, headings to `var(--font-display)` with `font-weight:400; line-height:1.1`. Keep `--ink`/`--text` and `--font`/`--font-body` as aliases. Example token block:

```css
:root{
  --bg:#07060c; --panel:#0c120f; --line:#1b2620;
  --accent:#34d399; --cyan:#22d3ee; --magenta:#e879f9;
  --ink:#e7e9ee; --text:#e7e9ee; --body:#94a3b8; --muted:#64748b;
  --grad:linear-gradient(90deg,var(--accent),var(--cyan));
  --font:"Archivo",system-ui,sans-serif; --font-body:"Archivo",system-ui,sans-serif;
  --font-display:"Archivo Black",sans-serif; --mono:"Space Mono",ui-monospace,monospace;
  --radius:10px; --max:1140px; --wrap:1140px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--body);font-family:var(--font);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:var(--cyan);text-decoration:none}
h1,h2,h3{font-family:var(--font-display);color:var(--text);line-height:1.1;font-weight:400}
h1{font-size:clamp(2.4rem,6vw,4.2rem)}
h2{font-size:clamp(1.6rem,3.5vw,2.4rem)}
h3{font-size:1.15rem}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}
.section{padding:84px 0;position:relative}
.section h2{text-align:left}
```

- [ ] **Step 2: Port atmosphere blocks from the reference, recolored.** From `irl-stream-site/css/style.css` copy the `.grain, .glow`, `main/header/footer` z-index, `.scanline`/`@keyframes scan`, `.reveal`, `.glitch`/`@keyframes glitch-tick`, and the `@media (prefers-reduced-motion)` blocks (lines ~52–91). Recolor: in `.glow` swap the purple `#a855f7` radial for green `#34d399` (e.g. `radial-gradient(600px 400px at 85% -5%, #34d3991f, transparent 70%)` + a cyan one). In `.glitch` keep magenta/cyan split (it reads as chromatic aberration, leave as-is). Paste recolored.

- [ ] **Step 3: Port utilities + buttons, recolored.** Copy `.kicker` (color → `var(--accent)`), `.mono`, `.status-dot` (already green), `.btn` (background `var(--grad)`, color `#07060c`), `.btn:hover` (swap shadow to `#34d39955`), `.btn-ghost`. Add `.btn-lg{font-size:17px;padding:16px 32px}`, `.accent{color:var(--accent)}`, `.eyebrow{font-family:var(--mono);font-size:.8rem;letter-spacing:.04em;color:var(--accent);margin:0 0 14px}`.

- [ ] **Step 4: Nav + footer.** Port reference `.nav`/`.nav.scrolled`/`.nav-inner` recolored, but adapt to ZtS's `.logo` markup (flex logo with `<img>` + text, `.logo b{color:var(--accent)}`). Add `.nav-cta{font-size:.92rem;padding:10px 18px}`. Port `.footer`/`.foot` (keep `.foot` class — landing/apply use it) with `border-top:1px solid var(--line)`, mono `.footer-tag{color:var(--accent)}`.

- [ ] **Step 5: Hero (split) + telemetry stats.** Write `.hero-split` keeping ZtS's two-column grid (`.grid` → `grid-template-columns:1.05fr .95fr` ≥900px), `.hero-art img` with `border-radius:18px;border:1px solid var(--line)` + green glow `::after`. Add reference-style `.hero-stats{display:flex;gap:36px;margin-top:36px}` with `dt{font-family:var(--mono);font-size:26px;color:var(--accent)}` and `dd{font-size:13px;color:var(--muted);letter-spacing:2px}`. Keep `.trust` row.

- [ ] **Step 6: Feature cards.** Keep ZtS `.feature-grid`/`.feature`/`.badge-ico`/`.ico` but restyle borders to `var(--line)`, hover `border-color:var(--accent)`, `.badge-ico` background `rgba(52,211,153,.12)` color `var(--accent)`.

- [ ] **Step 7: Finder (Signal Check).** Port reference `.finder-tiles`, `.finder-tile` (border `#2a3a32`, hover/active `border-color:var(--accent);color:var(--accent)`), `.finder-line` (`color:var(--accent)`), `.finder-line .caret` blink, and the mobile `@media` rules. Add `.lineup .kicker{text-align:center}`.

- [ ] **Step 8: Pricing tiers + finder recommendation link.** Keep ZtS `.tiers` grid + `.tier` cards (panel/line, hover lift), `.tier.featured`, `.pop` badge, `.price .per`. Add tier accent coding and finder states:

```css
.tier{position:relative;transition:transform .15s,border-color .15s,box-shadow .15s}
.tier[data-tier="1"]{--tac:var(--accent)} .tier[data-tier="2"]{--tac:var(--cyan)} .tier[data-tier="3"]{--tac:var(--magenta)}
.tier h3{color:var(--tac)}
.tier.is-rec{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent),0 10px 40px #34d3992c}
.tiers.has-pick .tier:not(.is-rec){opacity:.45}
.tier .price{font-family:var(--mono)}
```

- [ ] **Step 9: Proof, founding, FAQ accordion, CTA band.** Keep ZtS `.proof-grid`/`.proof-shot`/`.browser` (recolor borders/lines to `var(--line)`, `.ph` mono). Keep `.founding` with `border-color:var(--accent)`. Port reference `details.qa` accordion (`summary::after` `+`/`–` in `var(--cyan)`). Keep `.cta-band`/`.bgimg`/`.scrim`/`.cta-center`; update scrim to `rgba(7,6,12,.85)`.

- [ ] **Step 10: Verify CSS parses + nothing regressed.** Run:

```bash
python3 -m pytest -q
```
Expected: all tests PASS (CSS changes don't touch asserted strings). Then start a server and load the course (which already consumes these tokens) to confirm no visual breakage:
```bash
python3 -m http.server 8123 >/dev/null 2>&1 & sleep 1; curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8123/course/index.html; kill %1
```
Expected: `200`.

- [ ] **Step 11: Commit.**

```bash
git add styles.css
git commit -m "feat(design): glitch-editorial + telemetry design system (green primary)"
```

---

### Task 2: Restructure + retighten `index.html`

Rewrite the landing markup to consume Task 1 classes, cut prose to telemetry density, add the Signal Check finder, and keep every pinned string/structure.

**Files:**
- Modify (rewrite body + head): `index.html`
- Reference (read-only): `/home/kali/Desktop/TG6/Repos/irl-stream-site/index.html`

**Interfaces:**
- Consumes: all classes from Task 1.
- Produces: finder behavior contract — finder tiles carry `data-level="never|chat|ship"`; clicking one writes a recommendation line into `.finder-line` and toggles `is-rec` on the matching `.tier[data-tier]` (never→1, chat→2, ship→3) and `has-pick` on `.tiers`.

- [ ] **Step 1: Head + atmosphere.** Update `<head>`: swap the Google Fonts `<link>` to the Archivo/Space Mono URL (Global Constraints), keep `favicon.svg` link, keep `<title>` containing `Zero to Shipping`, keep meta description, keep `theme-color` → `#07060c`. Immediately inside `<body>`, add `<div class="grain" aria-hidden="true"></div><div class="glow" aria-hidden="true"></div>`. Keep the existing SVG icon sprite block verbatim.

- [ ] **Step 2: Nav.** Keep the existing `.nav > .wrap > .logo` block (logo img + "Zero to **Shipping**") and the `.btn .nav-cta` "Start now" → `#pricing`. Add a `<span class="status-dot">● READY</span>` before the CTA (optional flourish).

- [ ] **Step 3: Hero.** Rebuild `<header class="hero-split" id="top">` as a `.grid`: left `.hero-copy` = `<p class="eyebrow">// built by a developer who ships paid work with AI every day</p>` + `<h1 class="glitch">` with the **existing headline verbatim**: `You don't need to learn to code. <span class="accent">You need to learn to drive AI.</span>` + a one-line lede + `.hero-actions` (primary `#pricing`, ghost `#proof`) + a telemetry `<dl class="hero-stats mono">` with three `<div><dt>…</dt><dd>…</dd></div>`: `01`/`YOUR FIRST CHAT`, `→`/`CLAUDE CODE`, `1`/`THING SHIPPED`. Right `.hero-art` keeps `assets/hero-dev.webp`. (Lowercase `chat` + `claude code` now satisfied here.)

- [ ] **Step 4: The AI gap — cut to telemetry.** Replace the 5-paragraph `.prose` with a `.section.alt`: `<span class="kicker">// THE AI GAP</span>`, an `<h2>`, and 3–4 one-line `<p>`s (each ≤ ~12 words), e.g. "You have AI. So does everyone.", "You got mush and decided it was hype.", "It wasn't. Nobody showed you how to drive it.", "The people who pull ahead won't code — they'll make AI do the work." No `automation`.

- [ ] **Step 5: What you walk away with.** Keep the 4 `.feature` cards and their icons; tighten each `<p>` to one line. Add a leading `<span class="kicker">// WHAT YOU WALK AWAY WITH</span>`.

- [ ] **Step 6: Signal Check finder.** Before `#pricing`, add:

```html
<section class="section lineup" id="finder">
  <div class="wrap">
    <span class="kicker">// SIGNAL CHECK · WHERE ARE YOU NOW?</span>
    <div class="finder-tiles" role="group" aria-label="Where are you now?">
      <button type="button" class="finder-tile" data-level="never">NEVER USED AI</button>
      <button type="button" class="finder-tile" data-level="chat">I USE CHAT</button>
      <button type="button" class="finder-tile" data-level="ship">READY TO SHIP</button>
    </div>
    <p class="finder-line mono" aria-live="polite"></p>
  </div>
</section>
```

- [ ] **Step 7: Pricing — preserve every pinned structure.** Keep the three `<article class="tier" data-tier="N">` exactly: tier 1 "Build It" `$49` with `data-checkout="1"`; tier 2 `featured` "Ship It" `$499` with `.pop` "Most popular", `data-checkout="2"`, and value props mentioning `Discord` + `coaching`/`feedback`; tier 3 "Get Launched" `$2,999` with `href="apply.html"`, `1-on-1`, and `limited`/`seats`, NO `data-checkout`. Only restyle/tighten taglines — do not remove the pinned tokens. Add `<span class="kicker">// PICK HOW FAR YOU GO</span>`.

- [ ] **Step 8: Proof / founding / CTA — compress.** Proof: keep both `.proof-shot .browser` figures (and their `assets/...` replacement comments) under a `// I TEACH THIS BECAUSE I DO IT` kicker + 2 lines. Founding: compress `.founding` to 3 short `<p>`s. Convert the FAQ `.faq-item`s into `<details class="qa"><summary>…</summary><div class="qa-body">…</div></details>` (keep the FAQ answers, including the "prompting is an early module" / Claude Code answers). Keep the `.cta-band` with `assets/ship-rocket.webp`, one headline + one line + `.cta-center` CTA → `#pricing`. Keep `.foot` footer with mailto.

- [ ] **Step 9: Finder JS.** Inside the existing `<script>` (after the checkout + reveal logic), append the finder handler. Use `data-level`, NOT `data-tier`:

```html
<script>
  // ── Signal Check finder ────────────────────────────────────────────
  const REC = {
    never: { tier: "1", line: "→ START AT BUILD IT — the full self-paced ladder, chat to Claude Code." },
    chat:  { tier: "2", line: "→ SHIP IT FITS — chat habits + real help so you never stall alone." },
    ship:  { tier: "3", line: "→ GET LAUNCHED — 1-on-1, we ship your real thing together." }
  };
  const tilesWrap = document.querySelector(".finder-tiles");
  const lineEl = document.querySelector(".finder-line");
  const tiersWrap = document.querySelector(".tiers");
  if (tilesWrap && tiersWrap) {
    tilesWrap.addEventListener("click", (e) => {
      const btn = e.target.closest(".finder-tile");
      if (!btn) return;
      const rec = REC[btn.getAttribute("data-level")];
      tilesWrap.querySelectorAll(".finder-tile").forEach((t) => t.classList.toggle("is-active", t === btn));
      lineEl.innerHTML = rec.line + '<span class="caret">_</span>';
      tiersWrap.classList.add("has-pick");
      tiersWrap.querySelectorAll(".tier").forEach((c) =>
        c.classList.toggle("is-rec", c.getAttribute("data-tier") === rec.tier));
    });
  }
</script>
```
Keep the existing checkout `<script>` (TIER1/TIER2 constants, `PASTE_STRIPE_LINK` guard) and the reveal IntersectionObserver intact.

- [ ] **Step 10: Verify all invariants.** Run:

```bash
python3 -m pytest -q
```
Expected: PASS (landing, pricing, ctas, serves, site_files suites). Then assert finder didn't break the tier count:
```bash
grep -c 'data-tier="' index.html   # expect 3
grep -c 'data-level=' index.html   # expect 3
```

- [ ] **Step 11: Commit.**

```bash
git add index.html
git commit -m "feat(landing): telemetry redesign + Signal Check finder, prose cut"
```

---

### Task 3: Re-skin `apply.html`

Visual re-skin only; the form fields, honeypot, endpoint constant, and submit JS are unchanged.

**Files:**
- Modify: `apply.html`
- Test relevance: `tests/test_apply.py`, `tests/test_serves.py`

**Interfaces:** Consumes Task 1 classes (`.nav`, `.grain`, `.glow`, `.kicker`, `.btn-accent`, `.foot`, form classes). Produces nothing downstream.

- [ ] **Step 1: Head + shell.** Swap the Google Fonts link to the Archivo/Space Mono URL; add `theme-color` `#07060c` if missing; keep `styles.css` + `favicon.svg` links. After `<body>` add `.grain` + `.glow` overlays. Add the same `.nav` as the landing page (logo → `index.html`, ghost CTA "Back to programs" → `index.html`).

- [ ] **Step 2: Hero + form skin.** Replace the `.hero` header with a kicker hero: `<span class="kicker">// APPLY · GET LAUNCHED</span>` + existing `<h1>` ("Apply for <span class="accent">Get Launched</span>") + one-line lede. Keep the `<form class="form-card" id="applyForm">` and **all** field markup (`name="name|email|background|goal|project|timeline|why"`, honeypot `name="company_url"`). Ensure `.form-card`, labels, inputs adopt panel/line styling (already covered by Task 1 if form classes are ported; if not, port `.form-card`/input styles from old `styles.css` recolored). Keep submit `.btn .btn-accent`. Confirm page still has NO `$2,999` and NO `data-checkout`.

- [ ] **Step 3: Keep JS verbatim.** Leave the `<script>` block unchanged — `PASTE_APPS_SCRIPT_URL`, honeypot branch, `mode: "no-cors"` fetch, status handling.

- [ ] **Step 4: Verify.** Run:

```bash
python3 -m pytest -q tests/test_apply.py tests/test_serves.py
```
Expected: PASS.

- [ ] **Step 5: Commit.**

```bash
git add apply.html
git commit -m "feat(apply): re-skin application page in telemetry style"
```

---

### Task 4: Re-skin the course app

Adopt the new tokens/atmosphere across the course dashboard + reader. Keep ALL JS.

**Files:**
- Modify: `course/index.html`, `course/lesson.html`, `course/course.css`
- Do NOT touch: `course/curriculum.js`, `course/progress.js`
- Test relevance: `tests/test_curriculum.py` (must stay green — content untouched)

**Interfaces:** Consumes Task 1 tokens (`--accent` green already aligns) + `.grain`/`.glow`/`.scanline`/`.kicker`. Produces nothing downstream.

- [ ] **Step 1: Font + overlays on both course pages.** In `course/index.html` and `course/lesson.html`, swap the Google Fonts link to the Archivo/Space Mono URL; add `.grain` + `.glow` overlays right after `<body>`; ensure `theme-color` `#07060c`. Keep the existing `.nav`, the `<svg>` sprite, and all inline `<script>` renderers verbatim.

- [ ] **Step 2: Restyle `course.css`.** Re-point platform-specific UI to the new system without renaming classes the JS relies on: progress `.fill{background:var(--grad)}`; module `.num` → `color:var(--cyan)`, font `var(--mono)`; `.module` border `var(--line)`; lesson-row hover `border-color:var(--accent)`; TOC `.toc-mod` → `color:var(--accent)`; `.toc a.current` → `background:rgba(52,211,153,.12);color:var(--accent)`; `.dash-head .eyebrow` already uses `.eyebrow` from Task 1. Optionally add a `.scanline` divider style usage. Convert any hardcoded `#0b100e` panel insets to `var(--panel)` or a near-bg shade consistent with `#07060c`.

- [ ] **Step 3: Verify.** Run:

```bash
python3 -m pytest -q
```
Expected: full suite PASS. Then load both course pages:
```bash
python3 -m http.server 8124 >/dev/null 2>&1 & sleep 1; \
for p in /course/index.html /course/lesson.html; do curl -s -o /dev/null -w "$p %{http_code}\n" "http://127.0.0.1:8124$p"; done; kill %1
```
Expected: both `200`.

- [ ] **Step 4: Commit.**

```bash
git add course/index.html course/lesson.html course/course.css
git commit -m "feat(course): adopt telemetry design tokens + atmosphere"
```

---

## Final verification (after all tasks)

- [ ] Run the full suite once more: `python3 -m pytest -q` → all green.
- [ ] Manual pass over `index.html`, `apply.html`, `course/index.html`, `course/lesson.html`:
  - Finder buttons highlight and recommend a tier (and dim the others).
  - FAQ `<details>` accordions open/close with `+`/`–`.
  - Grain/glow visible; scanline animates; hero headline glitches occasionally.
  - With OS "reduce motion" on, animations are inert.
  - Mobile (≤600px): finder tiles fit in a row; tiers stack; nav collapses gracefully.

## Self-Review against spec

- **Palette / fonts / atmosphere / scanline / glitch:** Task 1 (all steps). ✓
- **Aggressive prose cut:** Task 2 steps 4, 5, 8. ✓
- **Signal Check finder:** Task 2 steps 6, 9 (uses `data-level`, preserving the 3× `data-tier` invariant). ✓
- **Pricing invariants preserved:** Task 2 step 7 + Global Constraints. ✓
- **Apply re-skin, JS untouched:** Task 3. ✓
- **Course re-skin, JS untouched:** Task 4. ✓
- **Backward-compatible tokens for course:** Global Constraints + Task 1 step 1. ✓
- **No build step / static:** Global Constraints. ✓
- **Tests stay green:** verify step in every task. ✓
- No placeholders, no undefined classes (every consumed class is produced in Task 1), `data-level` vs `data-tier` naming consistent across Task 2 steps 6/9/10. ✓
