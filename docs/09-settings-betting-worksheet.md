# Chapter 9 — The Settings-Betting Worksheet

*Turn poking at sliders into an honest little betting game you can win.*

## Why a worksheet

Here's the mistake everyone makes with settings: they change three knobs,
get better output, and have *no idea* which knob helped. The worksheet
fixes that with a tiny psychological trick: **you have to write down what
you expect before you run.** That turns "poke and hope" into a bet — and
you win by learning which knob did what.

Also — and this is real — beginners are *shockingly* bad at predicting what
a knob will do at first. The gamiest way to fix that is five minutes of
betting against your own intuition. It's a worksheet by way of a chili
cook-off pool: low stakes, quick rounds, you learn who to put money on.

## The worksheet

Print this, or copy it into a notebook, or just use the headings as a
template. One row per experiment. One knob per experiment.

```
EXPERIMENT LOG — one knob at a time
-----------------------------------
Date:            Model:            Size:      Backend: (Ollama / LM Studio / other)

Experiment #___    Knob being tested: ________
  Other knobs held at:  temp ___ | top-p ___ | seed ___ | max tokens ___

  What I predict will happen (be specific,
  e.g., "the two runs will be word-for-word the same"):

  ...predicting ABOVE the line. Run below the line.

  -----------------------------------------------------------------
  Run 1 output summary (3-10 words): _____________________________
  Run 2 output summary: _____________________________
  Same idea?  Y / N    Nearly same text?  Y / N

  What ACTUALLY changed vs my prediction:

  My rating:   sense  /5     freshness  /5

 VERDICT for this knob (fits in a tweet):
  ___________________________________________________
```

## A filled-in example

To show what "done" looks like:

```
Experiment #3     Knob being tested: seed (fixed vs random)
  Other knobs held at:  temp 1.2 | top-p 0.9 | seed 42 | max tokens 512

  What I predict will happen:
  With seed 42 both runs will be the same, or nearly.

  -----------------------------------------------------------------
  Run 1 output summary: "The Golden Ladle of Fire"
  Run 2 output summary: "The Golden Ladle of Fire"
  Same idea?  Y    Nearly same text?  Y

  What ACTUALLY changed vs my prediction:
  Nothing on run 2. Then I tried seed 7 and got "Big Pot Energy Cup"
  — different idea, same vibe. Seed is the re-roll button, temp sets the vibe.

  My rating:   sense  4 /5     freshness  3 /5

VERDICT for this knob:
Seed = re-roll dice (fresh idea). Temperature = set the vibe of all dice.
```

## The five-bet challenge

If you do nothing else from this book, do this: **no more than five
bets**, one per knob, in one sitting (roughly 30 minutes with a local
model). One per knob — temperature, top-p, seed, max tokens, system
prompt. Fill out one row per bet.

At the end, read your *verdicts* column. Those five sentences are now
the most useful "advanced settings" knowledge in your head, and they're
in **your** words about **your** model's **actual** behavior — worth more
than any table in this book, including ours.

## Scoring yourself (it's not about being right)

- **Bet right?** Great. Confidence earned.
- **Bet wrong?** Even better. You found something your intuition gets
  wrong *for your specific setup*. That's exactly what you want to find
  on day one. Circled and remembered.
- **Same result both runs, different from prediction?** Usually a
  background default you didn't know about (a hidden system prompt, a
  backend that ignores top-p, etc.). Now you know to check it — labs run
  lab-grade defaults, home setups run interesting ones.

## Printing

The one-page cheat sheet (Chapter 10) prints three worksheets per sheet
if you shrink to ~85%. And there is a companion printable `worksheet.md`
in this guide's repository (`docs/printables/`) if you want the plain file
without the book around it.

**→ Next: [Glossary](10-glossary.html)**
