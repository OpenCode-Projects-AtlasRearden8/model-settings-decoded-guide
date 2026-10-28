# Model Settings, Decoded: A Friendly Guide to the Knobs Behind the Chat Box

*Copyright (c) 2026 Asdale Dynamics, LLC — MIT licensed.*

## Who this is for

You. Yes, you — the person who opened a chat box, used it for a while, then
peeked at the settings panel and thought, *"Temperature? Top-p? Seed? What am
I supposed to do with these?"*

This guide is for anyone who uses AI (chat apps, local models, coding
assistants) and wants to understand what those numbered sliders actually do —
without a physics degree, without being talked down to, and without a wall of
jargon. If you can follow a recipe, you can follow this guide.

## What you'll learn

There are only a handful of settings that matter, and each one gets its own
chapter, each one explained with a picture from ordinary life:

1. **Temperature and top-p** — explained as a **chili cook-off**: how spicy is
   the pot, and how many contestant samples get to influence the judge.
2. **System prompts** — the house rules you give the cook before they enter.
3. **Context windows** — the **kitchen table**: how much food (conversation)
   fits on the table before things start falling off the edges.
4. **Max tokens** — the price-per-word line items on a sign.
5. **Stop sequences** — a block-letter sign on the kitchen counter that says
   **STOP** when the cook writes it.
6. **Seed** — the random-number dial that makes spicy pots reproducible (or not).
7. **When defaults are fine** — the honest chapter: for most everyday uses,
   you can leave almost all of this alone.

Then two practical chapters:

8. **Experiment recipes** — five hands-on experiments you can run tonight
   against a *local* model (Ollama, LM Studio, or anything
   OpenAI-compatible), each one changing a single setting so you can *see*
   what it does.
9. **The settings-betting worksheet** — a fill-in-the-blanks scorecard that
   turns "guess and poke at sliders" into an honest little betting game
   against your own predictions.

Plus a **glossary** of plain-English definitions and a printable
one-page **cheat sheet**.

## How to read this guide

You have three honest options:

- **Re-read the analogies.** The chili cook-off and the kitchen table are
  designed to stick. If you remember the picture, you remember the setting.
- **Do the recipes.** Chapter 8's experiments require a local model —
  download one, run five short experiments over a couple of evenings, and
  you will *own* these concepts, not just recognize them.
- **Cheat shamelessly.** The cheat sheet at the end is designed to be
  printed and taped somewhere visible. We will not be offended. We made it
  for exactly this.

## Our rules for this book

- **Warm, not academic.** Written like a friend would explain it.
- **Local-first.** Every experiment in the recipes chapter works offline,
  against a model on your own computer. No accounts, no API keys required
  for the core experiences.
- **Tested.** The static website is built from these Markdown files by a
  build script with its own test suite, so the pages you read are the pages
  we verified.
- **Never condescending.** "Beginner-friendly" means the *first* few minutes
  are easy. It does not mean the book is shallow. By the final chapter you
  will understand why seed + top-p at the extreme end produce
  degenerate output — in plain English.

## What this guide is NOT

- **Not a prompt-writing course.** Companion book
  *The Prompt-Writing Handbook* (Asdale Dynamics, LLC) covers that in depth;
  we will reference it where relevant but never re-explain it.
- **Not a "which model should I run" guide.** That's *ai-model-picker*'s
  job — it reads your hardware and tells you what will fit. This guide
  assumes you *have* a model running and asks what the knobs do.
- **Not medical, financial, or legal advice.** It is never anything but
  education, written for your general curiosity.

## A one-minute experiment before you turn the page

In your AI tool's settings (or a local-model front end), find **temperature**.
Set it to **0**. Send a prompt like: *"Give me a one-line chili recipe."*
Send it three times, same text. Notice the replies come back nearly
identical.

Now set temperature to **1.9** (or the highest your tool allows) and repeat.
Notice the replies go chaotic — one is great, one is nonsense, one looks like
a haiku written by a caffeinated squirrel.

That's the whole book in sixty seconds: what the knob does, why you might
want it higher or lower, and when to leave it alone. Turn the page —
we're going to a chili cook-off.

**→ Next: [Temperature and Top-P](01-temperature-and-top-p.html)**
