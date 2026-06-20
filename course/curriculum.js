/* Zero to Shipping — course curriculum (single source of truth).
 *
 * Both index.html (dashboard) and lesson.html render from this array.
 * Lesson bodies are intentionally scaffolded — drop the real teaching content
 * into `body` (HTML string) as you produce each lesson. Do NOT invent results,
 * client names, or proof here. Titles, objectives, and tasks are the real plan.
 *
 * Lesson id format: "<module>-<lesson>" (e.g. "2-3"). IDs are stable keys for
 * progress tracking in localStorage — don't renumber existing ones.
 */
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
