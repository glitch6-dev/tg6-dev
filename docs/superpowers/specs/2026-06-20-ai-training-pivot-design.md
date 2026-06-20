# Zero to Shipping — AI Training Pivot (Design)

**Date:** 2026-06-20
**Status:** Approved (design), pending implementation plan
**Scope:** Full repositioning of the product from "learn to build & ship a website (AI as co-pilot)" to "learn to use AI, from browser chat to Claude Code." Brand name "Zero to Shipping" is retained.

---

## 1. Positioning & promise

**Core promise:** *You don't need to learn to code. You need to learn to drive AI. This takes you from your first chat message to building and shipping real things with Claude Code.*

**Audience:** one ladder, three rungs — total AI beginners climb in at the bottom, casual ChatGPT/Claude users join partway up, non-coders who want to build reach the payoff at the top. Everyone exits having shipped one real thing.

**Finish line:** skill **and** artifact. The primary payoff is AI fluency (chat → Claude Code); every student also ships one real thing as the receipt that proves they can do it.

---

## 2. Curriculum spine (the ladder)

Six modules replace the six build-a-website modules. The spine climbs from browser chat to Claude Code.

| # | Module | Rung |
|---|--------|------|
| 1 | **Your first real conversation** — what AI is/isn't, opening a browser chat, getting genuinely useful answers | total beginners climb in |
| 2 | **Prompting that actually works** — context, specificity, iterating, catching when AI lies, checking its work | |
| 3 | **Make the AI yours** — projects, custom instructions, feeding it your own files & docs | casual users level up |
| 4 | **Put AI to work** — multi-step tasks, planning real work/life tasks with AI, light intro to agents | |
| 5 | **From chat to the machine — meet Claude Code** — install it, what changes when AI can touch your files & run commands | non-coders reach the payoff |
| 6 | **Ship something real** — use Claude Code to build & ship one real thing, live | finish line |

**DNA carried over (philosophy, not web-dev content):**
- "Ship small, don't collect courses" mindset
- "Get unstuck on your own" — reframed as: what to do when AI gets stuck or is wrong
- "A real shipped thing beats a certificate"

**Removed:**
- HTML/CSS teaching lessons (the tag-by-tag / CSS-rule lessons of the old Module 3)
- The word and concept "automation" everywhere, including Tier 2's "AI automation & bot project module"

**Lesson content depth:** lessons are **scaffolded**, matching the repo's existing honest pattern (real `title`/`objective`/`tasks`; `body` prose left as a marked TODO for the operator to write in their own voice). No fabricated teaching prose, client names, or results.

---

## 3. Tiers

Structure and prices unchanged. Only framing changes; the forced change is removing Tier 2's "automation" module.

| Tier | Price | Framing |
|------|-------|---------|
| **Build It** | $49 | The full self-paced ladder, chat → Claude Code. Climb it alone, lifetime access, ship one real thing. |
| **Ship It** (featured) | $499 | Everything in Build It, plus a **prompt & project-setup pack** (replaces the automation module), private Discord, feedback on what you build, group coaching calls. |
| **Get Launched** | $2,999 | 1-on-1. We use Claude Code together to build & ship *your* real thing. By application, limited seats. |

---

## 4. Marketing page (`index.html`) changes, section by section

- **Hero** — headline → *"You don't need to learn to code. You need to learn to drive AI."* Subhead: from first chat message to shipping with Claude Code. Trust badges: `Start from your first chat` · `Climb to Claude Code` · `Ship one real thing`.
- **"The tutorial trap" → "The AI gap"** — same agitation shape, new wound: everyone has AI now, almost nobody gets real work out of it; one lazy prompt → mush → "it's hype."
- **"What you walk away with"** — 4 feature cards re-pointed: *Talk to AI so it actually helps* / *Make AI yours (projects & files)* / *Get unstuck when AI is wrong* / *Ship it with Claude Code*.
- **"Is this you?"** — for: anyone who feels behind on AI, casual ChatGPT users who want more, non-coders who want to build. Not for: people who just want to watch; devs already living in Claude Code.
- **Pricing** — re-skin per §3.
- **Proof** — keep the instructor-credibility section, reframed: *"I use these exact tools — chat to Claude Code — to ship paid client work right now."* Two browser screenshot placeholders stay (real sites shipped with AI).
- **Founding students** — unchanged in shape; wording lightly aligned to AI framing.
- **FAQ** — swap math / "is AI writing my code" questions for: *Is this just ChatGPT tips? / Do I need to be technical for Claude Code? / Will AI just do it for me so I learn nothing? / Isn't this all free on YouTube?*
- **Final CTA band** — keep "Six months from now," reframed around AI fluency vs. another unfinished course.

## 5. Course app files

- `course/curriculum.js` — rebuilt to the 6 new modules (scaffolded bodies).
- `course/index.html` (dashboard) and `course/lesson.html` — render from curriculum; verify any hardcoded copy matches the new framing.
- `course/progress.js` — lesson IDs change with the new modules; localStorage keys are fine to reset (pre-launch, no real users).

## 6. Supporting copy & docs

- `docs/sales-copy.md` — rewritten to match the new positioning (it is the source-of-truth copy for `index.html`).
- `README.md` — update the one-line description / go-live checklist if it references the old positioning.
- SEO: `index.html` `<title>`/`<meta description>`, `sitemap.xml`/`robots.txt` unchanged structurally; meta text updated to new framing.

## 7. Untouched

- Stripe Payment Links wiring (`index.html` checkout JS) — same links, prices unchanged.
- Apps Script backend (`apps-script/Code.gs`) and Tier 3 application flow (`apply.html`).
- Test *plumbing* under `tests/`.

## 8. Tests

Several tests assert on specific copy/curriculum content and **will** break with the pivot. They are updated as part of this work to assert the new copy:
- `tests/test_landing.py`, `tests/test_pricing.py`, `tests/test_ctas.py` — landing/pricing/CTA copy.
- `tests/test_apply.py`, `tests/test_appsscript.py`, `tests/test_site_files.py`, `tests/test_serves.py` — verify still pass; update only where they reference changed copy.

## 9. Out of scope / YAGNI

- No rename, no new domain, no new tier structure, no new pricing.
- No real lesson prose (scaffold only).
- No new backend, payments, or auth changes.
