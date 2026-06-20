# Zero to Shipping — AI Training Pivot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition the static "Zero to Shipping" sales site + course app from "build & ship a website (AI as co-pilot)" to "learn to use AI, from browser chat to Claude Code," keeping the brand, prices, and backend untouched.

**Architecture:** Static site (HTML/CSS/vanilla JS) with a data-driven course app (`course/curriculum.js` is the single source of truth, rendered by `course/index.html` + `course/lesson.html`). Tests are pytest assertions over file contents and a live `http.server`. Work is copy/curriculum edits plus matching test updates; no backend, payments, or auth changes.

**Tech Stack:** HTML, CSS, vanilla JS, Python 3 + pytest.

## Global Constraints

- Brand name stays exactly **Zero to Shipping**. Do not rename.
- Prices stay exactly **$49 / $499 / $2,999**; tier names stay **Build It / Ship It / Get Launched**; tier card structure (`data-tier="1|2|3"`, `data-checkout="1|2"` on tiers 1&2 only, Tier 3 → `apply.html`) stays.
- The word/concept **"automation"** must not appear anywhere in shipped copy (case-insensitive).
- **Claude Code** is the top of the ladder and must be named in the landing page and the curriculum.
- Do **not** fabricate teaching prose, client names, or results. Lesson `body` fields are scaffolded (real `title`/`objective`/`tasks`; prose left as a marked draft), matching the repo's existing Module 4–6 pattern.
- Do **not** touch: Stripe Payment Link wiring/constants, `apps-script/Code.gs`, `apply.html`, `favicon.svg`, `sitemap.xml`/`robots.txt` structure.
- Run the full suite with `python3 -m pytest tests/ -q` from the repo root.

---

### Task 1: Landing page copy pivot (`index.html`)

Rewrite the marketing copy of every section of `index.html` to the AI-training positioning, and update the landing tests to assert the new promise. Tier card structure, prices, and Stripe JS are unchanged — only Tier 2's bullet wording changes (kill "automation").

**Files:**
- Modify: `index.html` (hero, "tutorial trap"→"AI gap", features, "is this you", Tier 2 bullets, proof, FAQ, CTA band; `<title>`/`<meta description>`)
- Test: `tests/test_landing.py`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the canonical landing copy and section headings that `docs/sales-copy.md` (Task 3) must mirror.

- [ ] **Step 1: Update the failing tests in `tests/test_landing.py`**

Replace `test_hero_promise_present` and add a Claude Code assertion:

```python
def test_hero_promise_present():
    html = read("index.html").lower()
    # The core promise: go from a browser chat to shipping with Claude Code
    assert "ship" in html
    assert "claude code" in html
    assert "chat" in html


def test_claude_code_named_on_landing():
    html = read("index.html").lower()
    assert "claude code" in html, "the ladder must name Claude Code"


def test_no_automation_language():
    html = read("index.html").lower()
    assert "automation" not in html, "automation framing was removed in the AI-training pivot"
```

Leave `test_index_exists`, `test_title_has_brand`, and `test_no_free_tier_language` as they are.

- [ ] **Step 2: Run the landing tests to verify they fail**

Run: `python3 -m pytest tests/test_landing.py -q`
Expected: FAIL — `test_no_automation_language` fails (Tier 2 still says "AI automation & bot project module") and `test_claude_code_named_on_landing`/`test_hero_promise_present` fail (no "claude code"/"chat" yet).

- [ ] **Step 3: Rewrite the hero in `index.html`**

Replace the `hero-copy` block (the `<p class="eyebrow">` through the closing `</div>` of `.trust`) with:

```html
<p class="eyebrow">// built by a developer who ships paid work with AI every day</p>
<h1>You don't need to learn to code. <span class="accent">You need to learn to drive AI.</span></h1>
<p class="lede">I'll take you from your very first chat message to building and shipping real things with Claude Code. Same ladder for everyone — you just climb on at your level.</p>
<div class="hero-actions">
  <a class="btn btn-accent btn-lg" href="#pricing">See the programs</a>
  <a class="btn btn-ghost btn-lg" href="#proof">See real work</a>
</div>
<div class="trust">
  <span><svg class="ico" viewBox="0 0 24 24"><use href="#i-check"/></svg> Start from your first chat</span>
  <span><svg class="ico" viewBox="0 0 24 24"><use href="#i-check"/></svg> Climb to Claude Code</span>
  <span><svg class="ico" viewBox="0 0 24 24"><use href="#i-check"/></svg> Ship one real thing</span>
</div>
```

Update the hero image `alt` to: `alt="A person working with an AI assistant on a dark workstation lit by green terminal screens"`.

- [ ] **Step 4: Rewrite the "tutorial trap" section as "The AI gap"**

Replace the `<h2>The tutorial trap</h2>` heading with `<h2>The AI gap</h2>` and replace the four `<p>` paragraphs in that section's `.prose` with:

```html
<p>You have AI now. Everyone does. You opened ChatGPT or Claude, typed a question, got something half-useful, and quietly decided the hype was overblown.</p>
<p>It wasn't. The tool is real. The gap is that nobody showed you how to actually drive it.</p>
<p>So you keep using it for trivia and one-liners while other people are getting real work out of the same screen — drafting, planning, building, shipping. The difference isn't the AI. It's that they learned to steer it and you were left to guess.</p>
<p>The people who pull ahead this decade won't be the ones who can code. They'll be the ones who can make AI do the work.</p>
```

- [ ] **Step 5: Re-point the four feature cards in "What you walk away with"**

Update the `sub` line to: `The skill to make AI work for you — from a browser chat to Claude Code — and one real thing you shipped with it.` Then replace the four `.feature` card `<h3>`/`<p>` pairs (keep each card's existing `<svg>` icon) with, in order:

```html
<div><h3>Talk to AI so it actually helps</h3><p>Get real, usable output from a browser chat instead of vague mush — the way power users do it.</p></div>
```
```html
<div><h3>Make AI yours</h3><p>Projects, custom instructions, and feeding it your own files so it works on your stuff, not generic answers.</p></div>
```
```html
<div><h3>Get unstuck when AI is wrong</h3><p>Spot when AI is confidently wrong, and know how to steer it back instead of giving up.</p></div>
```
```html
<div><h3>Ship it with Claude Code</h3><p>Step up from chat to Claude Code and put a real, working thing live on the internet.</p></div>
```

Update the closing centered `.prose` line to: `You finish able to use AI like the people pulling ahead — and with a real thing you shipped to prove it.`

- [ ] **Step 6: Rewrite the "Is this you?" columns**

Replace the `for` column `<ul>` items with:

```html
<li>You feel behind on AI and want to actually get good at it, fast</li>
<li>You already use ChatGPT or Claude for basic stuff and want to go much further</li>
<li>You're not a coder but you want AI to help you build and ship real things</li>
```

Replace the `not` column `<ul>` items with:

```html
<li>You want to watch, not do the reps</li>
<li>You're looking for a certificate to frame on a wall</li>
<li>You already live in Claude Code and ship daily</li>
```

- [ ] **Step 7: Re-skin the tier cards (remove "automation")**

In the Tier 1 (`data-tier="1"`) card, replace its three `<li>` items with:

```html
<li>The full self-paced ladder, chat to Claude Code</li>
<li>Ship one real thing with AI by the end</li>
<li>Follow-along lessons, lifetime access</li>
```

In the Tier 2 (`data-tier="2"`) card, replace the tagline and the `<ul>` with:

```html
<p class="tagline">Everything in Build It, plus real help so you never get stuck alone.</p>
<ul>
  <li>A prompt &amp; project-setup pack you can reuse</li>
  <li>Private Discord community access</li>
  <li>Feedback on what you build</li>
  <li>Group coaching calls</li>
</ul>
```

In the Tier 3 (`data-tier="3"`) card, replace the tagline and `<ul>` with:

```html
<p class="tagline">1-on-1. We use Claude Code together to build and ship your real thing.</p>
<ul>
  <li>Direct 1-on-1 mentorship with me</li>
  <li>A personalized roadmap</li>
  <li>Weekly private calls</li>
  <li>We build &amp; ship your project with Claude Code, together</li>
  <li>Strictly limited seats</li>
</ul>
```

Leave the `pricing` section heading, the `sub` line, all prices, `data-checkout` hooks, and the `apply.html` CTA exactly as they are.

- [ ] **Step 8: Reframe the proof section and FAQ**

In `#proof`, change the credibility paragraph (the one after `// clients who paid me to build, not to teach`) to:

```html
<p>I use these exact tools — browser chat to Claude Code — to ship paid client work right now. A local business owner hired me to design and build their website and paid the same day I delivered. Another client paid in full for an SEO build. I do this work for money with AI, which is why I can teach you to do it for real.</p>
```

Leave the two `.proof-shot` screenshot placeholders and their captions unchanged.

Replace the five FAQ `.faq-item` blocks with:

```html
<div class="faq-item reveal">
  <h3>Is this just ChatGPT tips?</h3>
  <p>No. Prompting is module one. The whole point is the climb: from a browser chat all the way to Claude Code building and shipping real things with you.</p>
</div>
<div class="faq-item reveal">
  <h3>Do I need to be technical to use Claude Code?</h3>
  <p>No. That's the entire reason this exists. We start at your first chat message and build up to it step by step. If you can use a web browser, you can start.</p>
</div>
<div class="faq-item reveal">
  <h3>Will AI just do it for me so I learn nothing?</h3>
  <p>The opposite. You learn to steer it, check it, and fix it when it's wrong. Driving AI well is the skill — and it's the one that pays.</p>
</div>
<div class="faq-item reveal">
  <h3>Isn't all of this free on YouTube?</h3>
  <p>The tips are. The path isn't. YouTube hands you ten thousand videos and no order. You're paying for the line from your first chat to a shipped thing, and for not quitting halfway.</p>
</div>
<div class="faq-item reveal">
  <h3>Can I really use this for my job or business?</h3>
  <p>That's the point. You finish able to put AI to work on real tasks, and with one real thing you shipped to show for it.</p>
</div>
```

Update the FAQ section `<h2>` to stay `Questions you're already asking` (no change needed).

- [ ] **Step 9: Update the CTA band and `<head>` meta**

In the `cta-band` section, replace the `.prose` line with:

```html
<p>You'll either be the person who learned to drive AI and shipped something, or the one still typing lazy prompts and calling it hype. You already know which you're tired of being.</p>
```

In `<head>`, set:
- `<title>Zero to Shipping | Learn to Drive AI, from Chat to Claude Code</title>`
- `<meta name="description" content="A developer who ships paid client work with AI teaches you to drive it — from your first browser chat to building and shipping real things with Claude Code. Three programs, self-paced to 1-on-1." />`

- [ ] **Step 10: Run the full suite to verify it passes**

Run: `python3 -m pytest tests/ -q`
Expected: PASS (all tests green — landing, pricing, ctas, serves, apply, appsscript, site_files).

- [ ] **Step 11: Commit**

```bash
git add index.html tests/test_landing.py
git commit -m "feat: pivot landing copy to AI training (chat to Claude Code)"
```

---

### Task 2: Rebuild the course curriculum (`course/curriculum.js`)

Replace the six build-a-website modules with the six AI-mastery modules from the spec, scaffolded (real titles/objectives/tasks; `body` left as the existing draft pattern). Add a curriculum test that locks the pivot.

**Files:**
- Modify: `course/curriculum.js` (the entire `window.CURRICULUM = [...]` array)
- Create: `tests/test_curriculum.py`

**Interfaces:**
- Consumes: the ladder + finish-line framing established in Task 1.
- Produces: lesson `id`s consumed by `course/progress.js` (localStorage keys) and rendered by `course/index.html` / `course/lesson.html`. IDs use the existing `"<module>-<lesson>"` format.

- [ ] **Step 1: Write the failing test `tests/test_curriculum.py`**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = (ROOT / "course" / "curriculum.js").read_text(encoding="utf-8")


def test_six_modules():
    # one "module:" key per module object
    assert SRC.count("module:") == 6


def test_ladder_endpoints_named():
    low = SRC.lower()
    assert "claude code" in low, "top of the ladder must be Claude Code"
    assert "chat" in low, "bottom of the ladder is a browser chat"


def test_no_automation_in_curriculum():
    assert "automation" not in SRC.lower()


def test_no_raw_html_css_teaching_modules():
    # the old build-a-site module titles are gone
    assert "HTML structure" not in SRC
    assert "CSS & layout" not in SRC


def test_every_lesson_has_objective_and_tasks():
    # cheap structural check: objective/tasks keys appear for each lesson
    assert SRC.count("objective:") == SRC.count("title:") - 6  # titles = 6 modules + N lessons
    assert "tasks:" in SRC
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m pytest tests/test_curriculum.py -q`
Expected: FAIL — current curriculum has "automation", "HTML structure", "CSS & layout", and module titles about building a site.

- [ ] **Step 3: Replace the `window.CURRICULUM` array in `course/curriculum.js`**

Keep the file's top comment block as-is. Replace the array with the six new modules. Modules 1–2 keep full scaffolded `body` prose drafts in the repo's voice; Modules 3–6 use the lighter scaffold (no `body`, so `lesson.html`'s draft fallback renders) exactly like the current Module 4–6 pattern.

```javascript
window.CURRICULUM = [
  {
    module: 1,
    title: "Your first real conversation",
    summary: "Open an AI chat and get genuinely useful output — starting from zero.",
    lessons: [
      {
        id: "1-1",
        title: "Welcome — how this works",
        duration: "6 min",
        objective: "Understand the one promise: you go from your first chat message to shipping something real with Claude Code.",
        body: `
<p>Welcome. You're here because you have AI on every screen you own and you're still not getting much out of it. This fixes that. By the end you won't just chat with AI — you'll drive it, all the way up to building and shipping a real thing with Claude Code.</p>
<p>I'm a self-taught developer and I use these exact tools to ship paid client work right now, from a browser chat to Claude Code. I'm not teaching theory. I'm teaching what I actually do on a normal workday.</p>
<h3>The ladder</h3>
<p>This course is one ladder. The bottom rung is a browser chat — the thing you've already touched. The top rung is Claude Code, where AI builds and ships real work with you. Everyone climbs the same ladder; you just start at whatever rung matches you today.</p>
<h3>How the lessons work</h3>
<p>Every lesson has a short video, a written walkthrough, and a "Do this" checklist. The checklist is the part that counts — watching me isn't the same as doing the reps. Do the task before you move on, and only check a lesson complete after you've actually done it.</p>
<p>Scroll to the task below, commit to a finish date, then meet me in the next lesson.</p>
`,
        tasks: [
          "Watch the welcome video",
          "Commit to a finish date",
        ],
      },
      {
        id: "1-2",
        title: "Open the chat and get a real answer",
        duration: "10 min",
        objective: "Send your first prompts and learn what AI is good at and where it falls down.",
        body: `
<p>Let's actually use it. Open a browser AI chat — Claude or ChatGPT, either works to start. This lesson is about getting a feel for the tool before we get good at it.</p>
<h3>What it is, what it isn't</h3>
<p>An AI chat is a very capable assistant that has read an enormous amount and will try to help with almost anything you type. It is not a search engine and it is not always right. It will sometimes state wrong things with total confidence. Knowing that from minute one is what separates people who use it well from people who get burned and quit.</p>
<h3>Send a few real prompts</h3>
<p>Don't ask it trivia. Give it a real, small job: "Rewrite this email to sound friendlier," "Explain what an invoice late fee is in plain English," "Give me three names for a dog-walking business." Notice how the more context you give, the better the answer gets. That's the whole game, and the next module drills it.</p>
<p>Do the tasks below. The point today is just to break the ice and see the tool respond to you.</p>
`,
        tasks: [
          "Open a browser AI chat (Claude or ChatGPT)",
          "Give it three real small jobs and read the results",
        ],
      },
      {
        id: "1-3",
        title: "The mindset: drive it, don't fear it",
        duration: "8 min",
        objective: "Adopt the habit of steering AI toward a finished result instead of accepting the first reply.",
        tasks: [
          "Take one first answer and push it twice to make it better",
        ],
      },
    ],
  },
  {
    module: 2,
    title: "Prompting that actually works",
    summary: "The difference between mush and real output: context, specificity, and iteration.",
    lessons: [
      {
        id: "2-1",
        title: "Give it context",
        duration: "12 min",
        objective: "Turn vague prompts into specific ones that get usable answers the first time.",
        body: `
<p>Most people's AI results are bad for one reason: they tell it almost nothing. "Write me a bio" gets a generic bio. The fix is context — who you are, what it's for, who reads it, and what good looks like.</p>
<h3>The shape of a good prompt</h3>
<p>A strong prompt usually has four parts: the role or job ("you're helping me write a bio"), the context ("I'm a self-taught developer who builds websites"), the task ("write a two-sentence bio for my homepage"), and the constraints ("plain, no buzzwords, first person"). Stack those and the quality jumps immediately.</p>
<p>Do the tasks below. Take a weak prompt and rebuild it with all four parts, then compare the two answers side by side.</p>
`,
        tasks: [
          "Rewrite a vague prompt with role, context, task, and constraints",
          "Compare the weak answer to the strong one",
        ],
      },
      {
        id: "2-2",
        title: "Iterate instead of restarting",
        duration: "11 min",
        objective: "Steer a conversation to a finished result by correcting and refining, not starting over.",
        body: `
<p>The first answer is a draft, not the deliverable. People who get great results don't write one perfect prompt — they have a conversation. They say "shorter," "more specific," "drop the third one," "now make it sound like me."</p>
<p>This is driving. You keep your hands on the wheel: react to what it gave you, tell it what's wrong, and let it adjust. Five quick corrections beat one giant prompt almost every time.</p>
<p>Do the tasks below on something real you need written or figured out.</p>
`,
        tasks: [
          "Take one task from mediocre to good using only follow-up corrections",
        ],
      },
      {
        id: "2-3",
        title: "Catch it when it lies",
        duration: "10 min",
        objective: "Spot confident-but-wrong answers and verify the things that matter.",
        tasks: [
          "Ask about something you already know and find where it's wrong or vague",
          "Decide which kinds of answers you'll always double-check",
        ],
      },
    ],
  },
  {
    module: 3,
    title: "Make the AI yours",
    summary: "Projects, custom instructions, and your own files — so it works on your stuff.",
    lessons: [
      {
        id: "3-1",
        title: "Custom instructions",
        duration: "10 min",
        objective: "Set up the AI so it already knows who you are and how you like answers.",
        tasks: [
          "Write custom instructions so you stop re-explaining yourself every chat",
        ],
      },
      {
        id: "3-2",
        title: "Projects & saved context",
        duration: "12 min",
        objective: "Use projects to keep a body of work and context together across chats.",
        tasks: [
          "Create a project for something real you're working on",
        ],
      },
      {
        id: "3-3",
        title: "Feed it your own files",
        duration: "11 min",
        objective: "Upload documents and work over your own material instead of generic answers.",
        tasks: [
          "Upload a real document and have the AI work over it",
        ],
      },
    ],
  },
  {
    module: 4,
    title: "Put AI to work",
    summary: "Multi-step tasks and real work — not just one-off answers.",
    lessons: [
      {
        id: "4-1",
        title: "Plan a real task with AI",
        duration: "11 min",
        objective: "Use AI to break a real job into steps before doing any of them.",
        tasks: [
          "Pick a real task and have AI break it into a step-by-step plan",
        ],
      },
      {
        id: "4-2",
        title: "Work the steps",
        duration: "13 min",
        objective: "Move through a multi-step task with AI doing the heavy lifting on each piece.",
        tasks: [
          "Complete one multi-step task end to end with AI",
        ],
      },
      {
        id: "4-3",
        title: "What an agent is (lightly)",
        duration: "8 min",
        objective: "Understand the jump from answering questions to taking actions for you.",
        tasks: [
          "Write down one task you wish AI could just do, not just describe",
        ],
      },
    ],
  },
  {
    module: 5,
    title: "From chat to the machine — meet Claude Code",
    summary: "Step off the browser and let AI touch your files and run real commands.",
    lessons: [
      {
        id: "5-1",
        title: "Why Claude Code changes the game",
        duration: "10 min",
        objective: "See what becomes possible when AI can read your files and run commands, not just chat.",
        tasks: [
          "Watch the walkthrough and note one thing chat can't do that Claude Code can",
        ],
      },
      {
        id: "5-2",
        title: "Install it and say hello",
        duration: "14 min",
        objective: "Get Claude Code installed and run your first real command with it.",
        tasks: [
          "Install Claude Code",
          "Have it create and change a file for you",
        ],
      },
      {
        id: "5-3",
        title: "Drive it like you learned to drive chat",
        duration: "11 min",
        objective: "Apply the same context-and-iterate skills to Claude Code.",
        tasks: [
          "Give Claude Code a small real task and steer it to done",
        ],
      },
    ],
  },
  {
    module: 6,
    title: "Ship something real",
    summary: "Use Claude Code to build and put one real thing live — your receipt.",
    lessons: [
      {
        id: "6-1",
        title: "Pick the thing you'll ship",
        duration: "9 min",
        objective: "Choose one small, real thing you can build and ship with Claude Code.",
        tasks: [
          "Write down the one thing you'll ship",
          "Cut it in half so it's small enough to finish",
        ],
      },
      {
        id: "6-2",
        title: "Build it with Claude Code",
        duration: "16 min",
        objective: "Use Claude Code to build your real thing, step by step.",
        tasks: [
          "Build the first working version with Claude Code",
        ],
      },
      {
        id: "6-3",
        title: "Put it live and make it count",
        duration: "12 min",
        objective: "Get your thing online at a real address and turn it into proof.",
        tasks: [
          "Put your project live at a real URL",
          "Send the link to one person",
        ],
      },
    ],
  },
];
```

- [ ] **Step 4: Run the curriculum tests to verify they pass**

Run: `python3 -m pytest tests/test_curriculum.py -q`
Expected: PASS.

- [ ] **Step 5: Run the full suite**

Run: `python3 -m pytest tests/ -q`
Expected: PASS (course app is data-driven; rendering is unchanged).

- [ ] **Step 6: Commit**

```bash
git add course/curriculum.js tests/test_curriculum.py
git commit -m "feat: rebuild curriculum as chat-to-Claude-Code ladder (scaffolded)"
```

---

### Task 3: Supporting copy — sales doc, README, course dashboard

Align the remaining copy artifacts with the pivot: the source-of-truth sales doc, the README description, and the course dashboard header.

**Files:**
- Modify: `docs/sales-copy.md`
- Modify: `README.md`
- Modify: `course/index.html` (dashboard `.dash-head` eyebrow/h1 + footer line)
- Test: `tests/test_site_files.py` (verify still passes; no rule changes needed)

**Interfaces:**
- Consumes: the canonical landing copy from Task 1 and the curriculum from Task 2.
- Produces: nothing other tasks depend on (final task).

- [ ] **Step 1: Rewrite `docs/sales-copy.md` to mirror the new `index.html`**

Keep the top operator note (the `> Drop-in copy...` block) verbatim. Replace the Hero, "The problem (agitate)", "What you walk away with", "Who this is for/not for", Proof, "The programs (tier copy)", "Objections (short FAQ)", and "Final CTA" sections so their wording matches the shipped copy from Task 1, Steps 3–9. In "The programs", Ship It's second bullet is "a prompt & project-setup pack you can reuse" (NOT an automation project). Leave the "Founding students" section as-is, and leave the honesty/proof operator notes intact.

- [ ] **Step 2: Update the description in `README.md`**

Replace the top line under the title with:

```markdown
Static three-tier sales site for the *Zero to Shipping* program — learn to drive AI, from your first browser chat to building and shipping real things with Claude Code.
```

Leave the file list, the **Go-live checklist** (Stripe / Apps Script / domain steps), and the **Tests** section unchanged.

- [ ] **Step 3: Update the course dashboard header in `course/index.html`**

Replace the `.dash-head` eyebrow and `<h1>`:

```html
<p class="eyebrow">Build It — self-paced course</p>
<h1>From your first chat to shipping with Claude Code.</h1>
```

Replace the dashboard footer line:

```html
<footer class="foot">
  Zero to Shipping — learn to drive AI, then ship something real with it.
</footer>
```

Leave all `<script>` rendering logic, the auth-gate comment, and progress wiring untouched.

- [ ] **Step 4: Run the full suite**

Run: `python3 -m pytest tests/ -q`
Expected: PASS. `test_site_files.py::test_readme_has_golive_checklist` still passes because the Stripe/Apps Script/domain checklist is unchanged.

- [ ] **Step 5: Commit**

```bash
git add docs/sales-copy.md README.md course/index.html
git commit -m "docs: align sales copy, README, and dashboard with AI-training pivot"
```

---

## Self-Review

**Spec coverage:**
- §1 Positioning/promise → Task 1 Steps 3–4 (hero, AI gap). ✓
- §2 Curriculum spine (6 modules, scaffolded, DNA carried, automation/HTML-CSS removed) → Task 2. ✓
- §3 Tiers (structure/prices kept, automation removed) → Task 1 Step 7. ✓
- §4 Marketing page section-by-section → Task 1 Steps 3–9. ✓
- §5 Course app files (curriculum, dashboard; progress IDs) → Task 2 + Task 3 Step 3. ✓
- §6 Supporting copy (sales-copy.md, README, SEO meta) → Task 1 Step 9 (meta) + Task 3 Steps 1–2. ✓
- §7 Untouched (Stripe, Apps Script, apply.html) → Global Constraints + no task edits them. ✓
- §8 Tests updated → Task 1 (test_landing), Task 2 (new test_curriculum); others verified green each task. ✓
- §9 Out of scope respected (no rename/price/backend changes; scaffold-only). ✓

**Placeholder scan:** No "TBD"/"handle edge cases"/"similar to" — every copy block and test is written out in full. The scaffolded lesson `body` drafts are intentional product content (the spec's chosen approach), not plan placeholders.

**Type/key consistency:** Lesson `id`s use the existing `"<module>-<lesson>"` format and stay within 6 modules; `data-tier`/`data-checkout` hooks are preserved so `tests/test_ctas.py` and `tests/test_pricing.py` keep passing. `course/progress.js` API is untouched.

One note on `tests/test_curriculum.py::test_every_lesson_has_objective_and_tasks`: it asserts `objective:` count equals `title:` count minus 6 (6 module titles). The new curriculum gives every lesson an `objective`, so this holds; if a future lesson omits `objective`, update that assertion rather than the curriculum.
