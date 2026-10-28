# Chapter 6 — Seeds: The Broad-Shouldered Replay Dial

*The setting that makes spicy pots repeatable.*

## The dartboard

Picture the model picking its next word as throwing a dart at a dartboard
covered in words — bigger words get bigger boards. Every throw is a dice
roll. The model's scoring (the *probability distribution*) chooses the board
sizes; a wheel-of-fortune spin picks where the dart lands.

The **seed** is the wheel's rig: fixed ahead of time, in a shed, before the
show. Same seed + same board sizes -> same landing spot, every throw, on
every run.

- A **fixed seed** (e.g., `seed = 42`) is a fair, well-oiled wheel. Same
  inputs and same seed produce the same output — *mostly exactly*, as we'll
  see.
- A **random seed** (every run a new one, the default in most tools) is a
  wheel whose rig gets re-strung each time. Same board sizes, new landing
  every time.

## Why you'd want a fixed seed

**Testing.** You want the *same output* across runs so a change in your
setup is really a change in your *prompt/settings* and not a re-roll of the
dice. "Change one thing, re-run, compare" — Chapter 8's core loop — only
works cleanly when the randomness is pinned.

**Bug reports.** "It produced this specific weirdness" — with a seed, a
friend can reproduce it. Without one, you sound like a tale from a
campfire.

**Deliberate reruns.** Same-prompt-same-seed *is* useful when you want
consistency more than surprise.

## Why you'd want it random

**Variety by design.** If you want a fresh take on "name my food truck"
every run, you need new darts. Random seeds give you that for free.

**Avoiding anchoring.** If you always reuse seed 42, you always get the
same "spicy" vibes; a pool of ideas sampled from one fixed seed is a
sample of *one* random path, not a distribution. Random is better when
diversity is the goal.

## The trap: seeds are not magic reproducibility

Here's the honest caveat most guides gloss: **seed + same settings usually,
not always, produces the same output**. Even if you pin the seed:

- The model's math isn't always fully deterministic on GPUs (parallel
  floating-point addition order can differ run to run).
- Batching, server load, or "speculative decoding" can change results
  between even same-seed calls with identical parameters.
- Some providers apply soft server-side tweaks (safety re-ranking, model
  version bumps) you can't see or control.

So "seed = 42" is a *strong hint*, not a signed contract. Treat it as
"these five runs should be very similar" rather than "byte-identical."

## The combo move everyone gets wrong

There's a specific mistake worth naming: **high temperature + fixed seed**.
You get a *very* spicy pot — but the *same* spicy pot every time. It's
still chaotic, it's just now the *same* chaos, evenly. If you're
brainstorming, you probably want temperature high and the seed random; if
you're testing, temperature low and seed fixed is the calmer, more honest
combo. (Chapter 8's Recipe 4 shows both sides.)

## What to actually do

1. **Leave the seed unset** (`-1`, `random`, or blank, depending on the
   tool) for everyday use. Random is fine.
2. **Set a seed when comparing.** Any change you make to prompt/temperature/
   top-p is only meaningful if the dice are pinned.
3. **Don't treat the seed as a guarantee.** When comparing outputs
   with a fixed seed, ask "are these the *same idea* or the *same text*?"
   If they're the same idea but different wording, the seed is doing its
   job; your eyes were expecting more.
4. **Change the seed to explore.** At your current temperature, cycling
   through seeds 1, 2, 3, 4, 5 is a cheaper way to get 5 fresh ideas than
   raising temperature.

**→ Next: [When Defaults Are Fine](07-when-defaults-are-fine.html)**
