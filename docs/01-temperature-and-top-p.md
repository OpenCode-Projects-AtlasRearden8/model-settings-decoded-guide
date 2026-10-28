# Chapter 1 — Temperature and Top-P: The Chili Cook-Off

*The two settings everyone asks about, explained at a church basement cook-off.*

## Meet the cook-off

Picture a chili cook-off in a school gym. Rows of contestants, each tending a
pot. Judges walk the line, taste, and score.

In this picture:

- **The model** is the head cook of one pot.
- **The pot's spiciness** is **temperature**.
- **The sample tray** is **top-p** (a.k.a. nucleus sampling).
- **The judge** is you, reading the model's next word.

Every time the model picks its *next word*, it walks the gym lineup and
chooses one. Temperature decides how spicy the pot is — how much the pot
encourages the cook to be bold. Top-p decides how many of that lineup get to
be considered at all.

They're the same two knobs in every AI tool that exposes "advanced settings,"
and they do different jobs. Once you can picture both, the sliders stop being
scary.

## Temperature: the pot's spiciness

Models don't pick one word. They produce a *score* for every word they know,
like each contestant getting a preliminary flavor score. Temperature changes
how spiky those scores are before the pick:

- **Low temperature (0 to 0.3):** mild pot. The cook tastes once and serves
  the obvious one. Reliable, repetitive, kind of beige. Great for facts,
  code, summaries, instructions-following.
- **Medium (0.5 to 0.8):** balanced. A little personality, a lot of sense.
  This is where most defaults sit (often 0.7 to 1.0).
- **High (1.2 and up):** five-alarm pot. Surprises everywhere: odd word
  choices, weird tangents, occasionally brilliance, occasionally a keyword
  salad. Great for brainstorming, terrible for a lawyer letter.

**The spicy-pot trap.** High temperature doesn't make chili *better* — it
makes it *bolder*. Bold is great on taco night and terrible when the judge
just wants to know if the chili is safe to eat. Match the heat to the dish:

| You want...                        | Temperature vibe |
| ---------------------------------- | ---------------- |
| Correct, boring, repeatable        | low (0 – 0.3)    |
| Everyday chat and drafts           | mid (0.5 – 0.8)  |
| Naming ideas, jokes, brainstorming | high (0.9 – 1.3) |
| Chaos for chaos's sake             | 1.4+ (good luck) |

## Top-p: the sample tray

Now, top-p. When the cook finally serves a spoonful, top-p decides how many
contestants' samples get onto the judge's tray.

Technically, top-p is a *probability cutoff*: keep adding words to the
"considered" tray, in order of likelihood, until their combined probability
adds up to `p`. Then the model picks from just that tray.

- **top-p = 0.1:** only the very top few candidates even get a spoon to the
  judge. Predictable.
- **top-p = 0.5:** a modest tray. The safe picks plus a couple of
  reasonable alternatives.
- **top-p = 0.9 to 1.0:** the whole gym is on the tray, including the
  contestant whose "chili" is actually sorbet. Wild.

Why bother with a second knob when temperature already controls boldness?
Because they fight different fires. Temperature reshuffles **scores**
(with one strong favorite, everything gets more likely together). Top-p
prunes **the roster** (with one strong favorite, the weird ones get cut
entirely). In practice:

- If your output is *too repetitive*, bump temperature a little **or** widen
  top-p — then check which fixed it.
- If your output is *incoherent*, lower temperature first (it's the blunt,
  safe instrument). Top-p is the scalpel; save it for when you need one.

## The classic combo moves

Real-world recipes, stated as a cook-off:

| Situation                          | Temperature | Top-p     | Why                                                            |
| ---------------------------------- | ----------- | --------- | -------------------------------------------------------------- |
| Math, code, data, legal-ish text   | 0 – 0.3     | 0.1 – 0.5 | Mild pot, short tray. Predictability wins.                     |
| Everyday chat, email drafts        | 0.7         | 0.9       | The house default. Balanced pot, generous tray.                 |
| Story/character names, taglines    | 1.0 – 1.3   | 0.9 – 1.0 | Spicy pot, big tray. Surprises welcome.                         |
| Anti-repetition rescue             | raise temp 0.1–0.2 | keep top-p | Small fixes first; escalate only if needed.                  |
| "It's going off the rails"         | lower temp 0.2 | lower top-p 0.1 | Two dials clamp the weirdness fast.                      |

## The "why does this exist" aside

You may have seen **top-k** too. It's top-p's older, simpler cousin: "keep
exactly the top *k* contestants, no matter their scores." Top-p is usually
smarter because it adapts — when one word is a runaway favorite, the tray is
tiny; when ten words are close, the tray gets roomy. If your tool shows
top-k, that number behaves like a fixed roster cap.

## What to actually do

1. **Notice which knob your tool exposes.** Many chat UIs hide top-p
   entirely and give you only temperature. That's fine — temperature is the
   80% button.
2. **Change one knob at a time.** Chapter 8 has five recipes that do exactly
   this.
3. **Write down what you expect before you run.** That's the worksheet in
   Chapter 9: predict, run, compare. It's a tiny game, and you win by
   learning.

**→ Next: [System Prompts](02-system-prompts.html)**
