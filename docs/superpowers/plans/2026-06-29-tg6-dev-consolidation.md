# TG6-Dev Site Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the `ai-training` repo into the single TG6-Dev digital-services site (AI Training becomes one service card), migrating the live contact form, GA4, recurring-costs page, and asset tooling out of `DigitalServices`, then deleting `DigitalServices`.

**Architecture:** Static HTML/CSS site (no build step). Verification is the existing `pytest` suite under `tests/` (a local `http.server` + file-content assertions). Each task makes a focused change, updates/adds the relevant test, runs `pytest`, and commits. Two final tasks are **GATED** (outward/irreversible) and are executed/approved by the user, never autonomously.

**Tech Stack:** HTML5, vanilla CSS/JS, Google Apps Script (form backends), Python 3 + pytest (test harness only).

## Global Constraints

- **Site domain:** `tg6-dev.com` (replaces every `REPLACE_WITH_DOMAIN` placeholder and every `glitch6-dev.github.io/DigitalServices` URL). `irl-stream-site` / `teamglitch6.com` is OUT OF SCOPE — do not touch it.
- **GA4 measurement ID:** `G-BJK86RFN9N` (reused from DigitalServices).
- **Do NOT modify `apps-script/Code.gs`** — that is the AI Training *application* backend (tab `Applications`), guarded by `tests/test_appsscript.py`. The *contact* backend goes to a separate path `apps-script/contact/Code.gs`.
- **Brand string:** every page keeps `TG6-Dev`; `index.html` must keep the literal substring `AI Training` (guarded by `tests/test_landing.py`).
- **Preserve in `index.html` (lowercased):** `ship`, `claude code`, `chat` (guarded by `test_hero_promise`).
- **Never push, rename the GitHub remote, or delete a remote repo without explicit per-action user consent.** Tasks 9 and 10 are gated; if a push needs the SSH passphrase, instruct the user to push manually.
- **Local commits only** in Tasks 1–8. No `git push`.
- Repo path is `/home/kali/Desktop/TG6/Repos/ai-training` until Task 8 renames it to `.../tg6-dev`.

---

### Task 1: Clean baseline — commit the dirty working tree + green the favicon tests

The working tree already contains an uncommitted favicon reorg (root `favicon.svg`/PNGs → `assets/favicon/` + `favicon.ico`) plus edits to `ai-training.html`/`apply.html`. Three tests are stale because of it. Get them green and commit a clean base. (`tests/test_serves.py::test_pages_serve_200` will remain red on its `"Digital services"` assertion until Task 4 — that is expected and called out below.)

**Files:**
- Modify: `tests/test_site_files.py`
- Commit: all currently-staged/modified files (favicon reorg + page edits)

**Interfaces:**
- Produces: a committed clean baseline; `assets/favicon/favicon-32x32.png` and root `favicon.ico` exist; `index.html` references `favicon.ico`.

- [ ] **Step 1: Inspect the working tree**

Run: `cd /home/kali/Desktop/TG6/Repos/ai-training && git status`
Expected: staged renames into `assets/favicon/`, modified `404.html`, `ai-training.html`, `apply.html`. Confirm root `favicon.ico` exists and root `favicon.svg` does NOT.

- [ ] **Step 2: Run the suite to see the 3 known failures**

Run: `python -m pytest -q -p no:cacheprovider 2>&1 | tail -6`
Expected: `3 failed, 34 passed` — failures: `test_standard_files_exist`, `test_index_links_favicon`, `test_pages_serve_200`.

- [ ] **Step 3: Update `tests/test_site_files.py` for the new favicon set**

Replace the two favicon-related tests with:

```python
def test_standard_files_exist():
    for f in ["robots.txt", "sitemap.xml", "favicon.ico", "README.md"]:
        assert (ROOT / f).exists(), f"missing {f}"
    # favicon set lives under assets/favicon/ after the reorg
    assert (ROOT / "assets" / "favicon" / "favicon-32x32.png").exists()


def test_index_links_favicon():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "favicon.ico" in html
```

Leave `test_readme_has_golive_checklist` unchanged.

- [ ] **Step 4: Run the favicon tests — expect pass**

Run: `python -m pytest tests/test_site_files.py -q -p no:cacheprovider`
Expected: `3 passed`.

- [ ] **Step 5: Run the full suite — expect only the one known-red**

Run: `python -m pytest -q -p no:cacheprovider 2>&1 | tail -4`
Expected: `1 failed, 36 passed` — the only failure is `test_pages_serve_200` (`"Digital services"`), owned by Task 4.

- [ ] **Step 6: Commit the clean baseline**

```bash
git add -A
git commit -m "chore: commit favicon reorg + reconcile favicon tests (clean base for consolidation)"
```

---

### Task 2: Port the live contact form + backend (non-colliding path, domain rewrite)

Bring `DigitalServices/contact.html` (live Apps Script `/exec` endpoint, GA already embedded) and its backend into the site. The backend must NOT overwrite `apps-script/Code.gs`.

**Files:**
- Create: `contact.html` (copied from `../DigitalServices/contact.html`, then rewritten)
- Create: `apps-script/contact/Code.gs` (copied from `../DigitalServices/apps-script/Code.gs`)
- Create: `og-image.png` (copied from `../DigitalServices/og-image.png`)
- Create: `tests/test_contact.py`

**Interfaces:**
- Consumes: nothing from prior tasks.
- Produces: `contact.html` at site root with `id="contactForm"`, live `ENDPOINT`, no stale domain; contact backend at `apps-script/contact/Code.gs` (tab `Leads`).

- [ ] **Step 1: Copy the three files in**

```bash
cd /home/kali/Desktop/TG6/Repos/ai-training
cp ../DigitalServices/contact.html ./contact.html
mkdir -p apps-script/contact
cp ../DigitalServices/apps-script/Code.gs ./apps-script/contact/Code.gs
cp ../DigitalServices/og-image.png ./og-image.png
```

- [ ] **Step 2: Rewrite the stale domain in `contact.html`**

```bash
sed -i 's#https://glitch6-dev.github.io/DigitalServices#https://tg6-dev.com#g' contact.html
```

Verify zero remain:

Run: `grep -c 'glitch6-dev.github.io' contact.html`
Expected: `0`

- [ ] **Step 3: Align `contact.html` nav + footer links to this site**

Open `contact.html`. Ensure the nav brand links to `index.html` and the nav/footer link set matches the site's real pages. Replace the footer link list (and any nav link list) so it reads exactly:

```html
<a href="index.html">Services</a>
<a href="ai-training.html#pricing">AI Training</a>
<a href="recurring-costs.html">Recurring costs</a>
<a href="privacy.html">Privacy</a>
<a href="terms.html">Terms</a>
<a href="mailto:dvelupr@proton.me">dvelupr@proton.me</a>
```

(Remove any link to pages that do not exist in this repo, e.g. a DigitalServices-only page.)

- [ ] **Step 4: Confirm the live endpoint and GA survived the copy**

Run: `grep -nE 'ENDPOINT *= *"https://script.google.com|G-BJK86RFN9N' contact.html`
Expected: one `ENDPOINT = "https://script.google.com/macros/s/.../exec"` line and the GA `G-BJK86RFN9N` line.

- [ ] **Step 5: Write `tests/test_contact.py`**

```python
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_contact_page_exists():
    assert (ROOT / "contact.html").exists()


def test_contact_form_and_honeypot():
    html = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert 'id="contactForm"' in html
    assert 'name="company_url"' in html  # spam honeypot


def test_contact_endpoint_is_live():
    html = (ROOT / "contact.html").read_text(encoding="utf-8")
    m = re.search(r'ENDPOINT\s*=\s*"([^"]+)"', html)
    assert m, "no ENDPOINT constant"
    assert m.group(1).startswith("https://script.google.com/macros/s/")
    assert m.group(1).endswith("/exec")


def test_contact_no_stale_domain():
    html = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert "glitch6-dev.github.io" not in html


def test_contact_backend_present_and_clean():
    gs = (ROOT / "apps-script" / "contact" / "Code.gs").read_text(encoding="utf-8")
    assert "Leads" in gs
    for col in ["Name", "Email", "Business", "Service", "Budget", "Message"]:
        assert col in gs, f"missing header {col}"
    assert "function doPost" in gs and "function doGet" in gs
    assert "dvelupr@proton.me" in gs
    assert "gmail.com" not in gs
    assert "spreadsheets/d/" not in gs  # no private Sheet id committed
```

- [ ] **Step 6: Run the contact tests — expect pass**

Run: `python -m pytest tests/test_contact.py -q -p no:cacheprovider`
Expected: `5 passed`.

- [ ] **Step 7: Confirm the application backend test still passes (no collision)**

Run: `python -m pytest tests/test_appsscript.py -q -p no:cacheprovider`
Expected: `5 passed` (it still reads `apps-script/Code.gs`).

- [ ] **Step 8: Commit**

```bash
git add contact.html apps-script/contact/Code.gs og-image.png tests/test_contact.py
git commit -m "feat: port live contact form + Leads backend (domain-rewritten, non-colliding path)"
```

---

### Task 3: Add GA4 to the remaining pages

`contact.html` already carries GA. Add the same snippet to the other pages so analytics is sitewide.

**Files:**
- Modify: `index.html`, `ai-training.html`, `apply.html`, `privacy.html`, `terms.html`, `404.html`
- Create: `tests/test_analytics.py`

**Interfaces:**
- Produces: every existing HTML page contains `G-BJK86RFN9N`.

- [ ] **Step 1: Insert the GA snippet into each page**

In each of `index.html`, `ai-training.html`, `apply.html`, `privacy.html`, `terms.html`, `404.html`, insert this block immediately AFTER the `<meta name="theme-color" ... />` line in `<head>`:

```html
  <!-- GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-BJK86RFN9N"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-BJK86RFN9N');
  </script>
```

- [ ] **Step 2: Write `tests/test_analytics.py`**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# recurring-costs.html is added in a later task; it is asserted there.
PAGES = ["index.html", "ai-training.html", "apply.html",
         "privacy.html", "terms.html", "404.html", "contact.html"]


def test_ga4_on_all_pages():
    for p in PAGES:
        html = (ROOT / p).read_text(encoding="utf-8")
        assert "G-BJK86RFN9N" in html, f"GA4 missing on {p}"
```

- [ ] **Step 3: Run — expect pass**

Run: `python -m pytest tests/test_analytics.py -q -p no:cacheprovider`
Expected: `1 passed`.

- [ ] **Step 4: Commit**

```bash
git add index.html ai-training.html apply.html privacy.html terms.html 404.html tests/test_analytics.py
git commit -m "feat: add GA4 (G-BJK86RFN9N) sitewide"
```

---

### Task 4: Curate the homepage catalog, reframe brand, route CTAs to the contact form

Broaden `index.html` to the curated 8-card catalog, fold E-commerce into the Website card, add the 3 new cards, reframe the brand to digital-services-led (keeping AI Training prominent), and swap every `mailto:` quote CTA to `contact.html`. This also adds the literal `Digital services` string that `test_pages_serve_200` needs, and requires updating the now-outdated `test_no_automation_language`.

**Files:**
- Modify: `index.html`
- Modify: `tests/test_landing.py`

**Interfaces:**
- Consumes: `contact.html` (Task 2).
- Produces: `index.html` containing `Digital services`, `Get a quote`, `Custom Software`, `Security & Pentest`, `href="ai-training.html"`, `href="contact.html"`, and still `TG6-Dev`/`AI Training`/`claude code`/`chat`/`ship`.

- [ ] **Step 1: Reframe `<title>` and social meta (keep required strings)**

In `index.html` `<head>`, set:

```html
  <title>TG6-Dev · Digital Services & AI Training | Built and Shipped</title>
```

Leave the existing `og:`/`twitter:` description lines that contain "Claude Code"/"chat"/"shipping" in place (they satisfy `test_hero_promise`). Do not remove the words `ship`, `chat`, or `Claude Code` anywhere in the file.

- [ ] **Step 2: Add the `Digital services` lead line to the services section**

In the `#services` section, change the section header block so it contains the exact substring `Digital services`. Replace:

```html
        <span class="kicker">// TG6-DEV · DIGITAL SERVICES</span>
        <h2 class="reveal">Built and tailored to you, then shipped.</h2>
```

with:

```html
        <span class="kicker">// TG6-DEV</span>
        <h2 class="reveal">Digital services, built and tailored to you, then shipped.</h2>
        <p class="sub reveal">Websites, stores, software, security, and AI training — designed, built, and run by one engineer.</p>
```

- [ ] **Step 3: Fold E-commerce into the Website card + route its CTA to the form**

Replace the existing `Website Design &amp; Build` `<article>` (the `#i-code` card) with:

```html
          <article class="svc reveal">
            <span class="badge-ico"><svg class="ico" viewBox="0 0 24 24"><use href="#i-code"/></svg></span>
            <h3>Website Design &amp; Build</h3>
            <p class="tagline">A complete website or online store, custom-built and launched.</p>
            <ul>
              <li>Custom design that looks great on every device</li>
              <li>Online stores &amp; e-commerce — sell products and take payments</li>
              <li>A working contact form, launched on your own domain</li>
            </ul>
            <div class="cta"><a class="btn btn-accent" href="contact.html?service=website">Get a quote</a></div>
          </article>
```

- [ ] **Step 4: Route the other three existing cards' CTAs to the form**

In the `SEO`, `Branding &amp; Design`, and `Hosting, Security &amp; Data` cards, replace each card's `mailto:` CTA anchor `href` with the form, preserving the button classes:
- SEO card CTA → `href="contact.html?service=seo"`
- Branding card CTA → `href="contact.html?service=branding"`
- Hosting card CTA → `href="contact.html?service=hosting"`

(Each is the single `<a class="btn ..." href="mailto:...">Get a quote</a>` inside that card's `<div class="cta">`.)

- [ ] **Step 5: Add the three new service cards**

Insert these `<article>` blocks into the `services-grid` (after the Hosting card, before the Consulting card):

```html
          <article class="svc reveal">
            <span class="badge-ico"><svg class="ico" viewBox="0 0 24 24"><use href="#i-bolt"/></svg></span>
            <h3>Custom Software &amp; Automation</h3>
            <p class="tagline">Bespoke tools, bots, and data pipelines that do the work for you.</p>
            <ul>
              <li>Custom apps and internal tools built to your workflow</li>
              <li>Bots and automations that remove repetitive work</li>
              <li>Data pipelines that move and clean your data</li>
            </ul>
            <div class="cta"><a class="btn btn-ghost" href="contact.html?service=software">Get a quote</a></div>
          </article>

          <article class="svc reveal">
            <span class="badge-ico"><svg class="ico" viewBox="0 0 24 24"><use href="#i-buoy"/></svg></span>
            <h3>Security &amp; Pentest</h3>
            <p class="tagline">Authorized security testing and hardening before the bad guys try.</p>
            <ul>
              <li>Authorized penetration testing of your site or app</li>
              <li>A prioritized findings report you can act on</li>
              <li>Hardening so issues stay fixed</li>
            </ul>
            <div class="cta"><a class="btn btn-ghost" href="contact.html?service=security">Get a quote</a></div>
          </article>

          <article class="svc reveal">
            <span class="badge-ico"><svg class="ico" viewBox="0 0 24 24"><use href="#i-chat"/></svg></span>
            <h3>AI Training</h3>
            <p class="tagline">Learn to drive AI — from your first browser chat to shipping with Claude Code.</p>
            <ul>
              <li>Self-paced to 1-on-1 programs</li>
              <li>Ship one real project by the end</li>
              <li>No coding background required</li>
            </ul>
            <div class="cta"><a class="btn btn-accent" href="ai-training.html#pricing">See the programs</a></div>
          </article>
```

- [ ] **Step 6: Add Services + Contact to nav, mobile menu, and footer**

In the nav `.nav-links`, the `.mobile-menu`, and the footer `.footer-links`, add links so each set includes (alongside the existing AI-training links):

```html
<a href="contact.html">Contact</a>
```

In the footer `.footer-links`, also add:

```html
<a href="recurring-costs.html">Recurring costs</a>
```

(Keep the existing `Programs`/`Apply`/`Course`/`Privacy`/`Terms` links.)

- [ ] **Step 7: Update proof captions to real shipped work**

In the `#proof` section, update the two figures' `<span class="url">` and `<figcaption>` to reference real properties: the first → `tg6-dev.com` ("This site — live contact form, real backend."), the second → `teamglitch6.com` ("A full product storefront — layout to checkout, end to end."). Leave the `.ph` placeholders for now (screenshots are a later asset task).

- [ ] **Step 8: Replace the outdated automation test in `tests/test_landing.py`**

Delete `test_no_automation_language` (the AI-training pivot banned the word; the site now sells Automation as a service). Replace it with:

```python
def test_services_catalog_present():
    html = read("index.html")
    # curated digital-services catalogue; AI Training is one card among many
    assert "Custom Software" in html
    assert "Security &amp; Pentest" in html
    assert 'href="ai-training.html#pricing"' in html  # AI Training is one service
    assert 'href="contact.html' in html               # CTAs route to the form
```

Leave every other test in the file unchanged (`test_title_has_brand` still requires `AI Training`; ensure it is still present in the title from Step 1).

- [ ] **Step 9: Run the full suite — expect all green**

Run: `python -m pytest -q -p no:cacheprovider 2>&1 | tail -4`
Expected: `0 failed` (all passed). In particular `test_pages_serve_200` now passes (`Digital services` + `Get a quote` present) and `test_services_catalog_present` passes.

- [ ] **Step 10: Commit**

```bash
git add index.html tests/test_landing.py
git commit -m "feat: curate 8-service catalog, route CTAs to contact form, reframe brand to digital-services-led"
```

---

### Task 5: Port the recurring-costs transparency page

**Files:**
- Create: `recurring-costs.html` (from `../DigitalServices/recurring-costs.html`)
- Modify: `tests/test_analytics.py`
- Create: `tests/test_recurring_costs.py`

**Interfaces:**
- Produces: `recurring-costs.html` at site root, footer-linked from `index.html` (added in Task 4), GA present, no stale domain.

- [ ] **Step 1: Copy and domain-rewrite**

```bash
cd /home/kali/Desktop/TG6/Repos/ai-training
cp ../DigitalServices/recurring-costs.html ./recurring-costs.html
sed -i 's#https://glitch6-dev.github.io/DigitalServices#https://tg6-dev.com#g' recurring-costs.html
grep -c 'glitch6-dev.github.io' recurring-costs.html   # expect 0
```

- [ ] **Step 2: Ensure GA is present (add if missing)**

Run: `grep -c 'G-BJK86RFN9N' recurring-costs.html`
If `0`, insert the GA snippet (from Task 3 Step 1) after the `<meta name="theme-color" ... />` line in `<head>`.

- [ ] **Step 3: Align nav/footer links to this site**

In `recurring-costs.html`, confirm the nav brand links to `index.html` and the `Contact` link points to `contact.html` (both already true per the source). Ensure no link points to a page that doesn't exist in this repo; fix any that do.

- [ ] **Step 4: Add `recurring-costs.html` to the analytics page list**

In `tests/test_analytics.py`, append `"recurring-costs.html"` to the `PAGES` list.

- [ ] **Step 5: Write `tests/test_recurring_costs.py`**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_recurring_costs_exists():
    assert (ROOT / "recurring-costs.html").exists()


def test_recurring_costs_clean_and_linked():
    html = (ROOT / "recurring-costs.html").read_text(encoding="utf-8")
    assert "glitch6-dev.github.io" not in html
    assert 'href="contact.html"' in html
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "recurring-costs.html" in index  # footer-linked from home
```

- [ ] **Step 6: Run — expect pass**

Run: `python -m pytest tests/test_recurring_costs.py tests/test_analytics.py -q -p no:cacheprovider`
Expected: `3 passed`.

- [ ] **Step 7: Commit**

```bash
git add recurring-costs.html tests/test_recurring_costs.py tests/test_analytics.py
git commit -m "feat: port recurring-costs transparency page (domain-rewritten, footer-linked)"
```

---

### Task 6: Port the asset-generation tooling

**Files:**
- Create: `tools/gen_assets.py` + `tools/fonts/*` (from `../DigitalServices/tools/`)

**Interfaces:**
- Produces: `tools/gen_assets.py` available in the repo (utility, not wired into tests).

- [ ] **Step 1: Copy the tooling in**

```bash
cd /home/kali/Desktop/TG6/Repos/ai-training
mkdir -p tools
cp -r ../DigitalServices/tools/* ./tools/
ls tools tools/fonts
```

- [ ] **Step 2: Sanity-check it imports/parses**

Run: `python -c "import ast; ast.parse(open('tools/gen_assets.py').read()); print('ok')"`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add tools
git commit -m "chore: port asset-generation tooling from DigitalServices"
```

---

### Task 7: Swap the domain placeholder + finalize README

Replace every `REPLACE_WITH_DOMAIN` with `tg6-dev.com` across the ai-training-origin files, and update the README go-live checklist (keeping the keywords `test_readme_has_golive_checklist` checks for).

**Files:**
- Modify: `index.html`, `ai-training.html`, `apply.html`, `privacy.html`, `terms.html`, `404.html`, `sitemap.xml`, `robots.txt`
- Modify: `README.md`

**Interfaces:**
- Produces: zero `REPLACE_WITH_DOMAIN` and zero `glitch6-dev.github.io` anywhere in the repo's shipped files.

- [ ] **Step 1: Replace the placeholder everywhere**

```bash
cd /home/kali/Desktop/TG6/Repos/ai-training
grep -rl 'REPLACE_WITH_DOMAIN' . --include=*.html --include=*.xml --include=*.txt \
  | xargs sed -i 's/REPLACE_WITH_DOMAIN/tg6-dev.com/g'
```

- [ ] **Step 2: Verify nothing stale remains**

Run: `grep -rn 'REPLACE_WITH_DOMAIN\|glitch6-dev.github.io' . --include=*.html --include=*.xml --include=*.txt`
Expected: no output.

- [ ] **Step 3: Update the README go-live checklist**

Edit `README.md` so it documents the consolidated site and still contains the substrings `domain`, `Stripe`, and `Apps Script` (or `endpoint`). Include, in plain language: the domain is `tg6-dev.com`; there are TWO Apps Script endpoints (the application form `apply.html` → `apps-script/Code.gs`, and the contact form `contact.html` → `apps-script/contact/Code.gs`); Stripe checkout for AI Training tiers is wired on `ai-training.html` but card payments are still pending activation.

- [ ] **Step 4: Run the full suite — expect all green**

Run: `python -m pytest -q -p no:cacheprovider 2>&1 | tail -4`
Expected: `0 failed`.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: point site at tg6-dev.com + refresh README go-live checklist"
```

---

### Task 8: Rename the local repo directory `ai-training` → `tg6-dev`

The GitHub remote keeps its old name until the gated Task 9; this step is local only.

**Files:**
- Rename: directory `ai-training/` → `tg6-dev/`
- Modify: `README.md` (any references to the old directory/repo name)

- [ ] **Step 1: Rename the directory**

```bash
cd /home/kali/Desktop/TG6/Repos
mv ai-training tg6-dev
cd tg6-dev
```

- [ ] **Step 2: Update name references in README**

In `README.md`, update any `ai-training` repo/path references to `tg6-dev`. (Leave URLs like `ai-training.html` — that page filename is unchanged.)

- [ ] **Step 3: Confirm tests still run from the new path**

Run: `python -m pytest -q -p no:cacheprovider 2>&1 | tail -4`
Expected: `0 failed`.

- [ ] **Step 4: Commit (local only — do NOT push)**

```bash
git add -A
git commit -m "chore: rename repo to tg6-dev to match its digital-services role"
```

---

### Task 9 — [GATED] Rename the GitHub repo + push

**Outward action. STOP and get the user's explicit go-ahead. The user runs this (or approves each command). If the push needs the SSH passphrase, the user pushes manually.**

- [ ] **Step 1: Confirm with the user** that they want to rename `glitch6-dev/ai-training` → `glitch6-dev/tg6-dev` on GitHub and push.

- [ ] **Step 2: Rename on GitHub** (user runs):

```bash
gh repo rename tg6-dev -R glitch6-dev/ai-training
```

- [ ] **Step 3: Point the local remote at the new name** (user runs):

```bash
cd /home/kali/Desktop/TG6/Repos/tg6-dev
git remote set-url origin git@github.com:glitch6-dev/tg6-dev.git
git remote -v   # verify
```

- [ ] **Step 4: Push** (user runs / approves; manual if passphrase prompts):

```bash
git push origin HEAD
```

---

### Task 10 — [GATED] Delete DigitalServices (local + GitHub)

**Irreversible + outward. Only after confirming everything valuable migrated (contact form + backend, GA4, recurring-costs, asset tooling). STOP and get the user's explicit go-ahead. The user runs this.**

- [ ] **Step 1: Final migration audit**

Run from `Repos/tg6-dev`:
`ls contact.html recurring-costs.html og-image.png apps-script/contact/Code.gs tools/gen_assets.py`
Expected: all present. Confirm the site builds/serves and the suite is green.

- [ ] **Step 2: Confirm with the user** they want `DigitalServices` deleted locally and on GitHub.

- [ ] **Step 3: Delete locally** (user runs):

```bash
rm -rf /home/kali/Desktop/TG6/Repos/DigitalServices
```

- [ ] **Step 4: Delete the GitHub repo** (user runs):

```bash
gh repo delete glitch6-dev/DigitalServices --yes
```

---

## Notes for the implementer

- The contact form posts `mode: "no-cors"`, so the browser cannot read success/failure — verify a real submission lands in the Google Sheet via the Apps Script execution log after go-live (known limitation, carried from DigitalServices).
- There are two independent Apps Script deployments/Sheets: applications (`apps-script/Code.gs`, tab `Applications`) and leads (`apps-script/contact/Code.gs`, tab `Leads`). Their `/exec` endpoints are NOT both committed — the contact endpoint ships hardcoded in `contact.html`; the application endpoint in `apply.html` is still the `PASTE_APPS_SCRIPT_URL` placeholder and is out of scope for this plan.
- Stripe tiles were intentionally NOT migrated (card payments not yet activated). The AI Training Stripe links on `ai-training.html` are untouched.
- `irl-stream-site` / `teamglitch6.com` is a separate product and must not be modified by this work.
```

