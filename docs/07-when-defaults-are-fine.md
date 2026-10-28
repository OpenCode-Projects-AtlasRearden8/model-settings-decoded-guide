# Chapter 7 — When Defaults Are Fine: The Honest Chapter

*The unpopular truth: most of the time, you should touch nothing.*

## The confession

You made it this far. You know what the knobs do. And now this chapter
exists to talk you out of using them.

Here's the truth: for probably 90% of what people actually do with AI —
ask questions, write drafts, summarize things, get help with ideas —
**the defaults are already good.** Someone at the model lab or your
front-end of choice ran thousands of tests to pick them. Your input is
more likely to make things *worse* than better, for the same reason a
cook-off judge who has never cooked shouldn't adjust the recipe mid-taste.

## When the defaults ARE fine

Just leave everything alone if you're doing any of these:

- **Everyday Q&A.** "Explain X." "Help me draft Y." Defaults are tuned
  for exactly this.
- **Summaries and rewrites.** The house style is a *good* style for most
  communication tasks.
- **Learning something.** Explanations don't need spiciness; they need
  clarity. Temperature high makes learning *harder*, not richer.
- **Anything where being wrong is costly.** Facts, code, advice,
  **anything health/medical/legal-adjacent** — mild pot, short tray, and
  check things.
- **You just started.** You don't have a baseline! Tweak *after* you've
  seen what the default does for *your* kind of task.

## When to actually reach for a knob

The short honest list:

| Situation                                       | Knob to touch          | Chapter |
| ------------------------------------------------ | ---------------------- | ------- |
| Replies feel stiff, same-y, corporate            | temperature up a bit   | 1       |
| Replies wander off-topic or hallucinate-ish      | temperature down a bit | 1       |
| The tone is wrong for your audience              | system prompt (not temp) | 2     |
| Long conversation forgets things                 | work the context, new chat | 3    |
| Replies cut off mid-list or mid-code             | max tokens up          | 4       |
| A specific string keeps showing up               | stop sequence          | 5       |
| You're testing/comparing and runs vary           | seed fixed             | 6       |
| Naming a product, brainstorming nametags         | temperature up + seed random | 1, 6 |

**"Wrong tone" is almost always a system-prompt problem, not a
temperature problem.** Newcomers reach for temperature when a chat is
*too formal*. Temperature won't fix formality. Chapter 2 will.

## The meta-rule

> **Tweak only after the default has failed you for a *specific* reason you
> can name.**

Not "it feels off." Name what's wrong: too repetitive? too long? too
formal? forgot the beginning? Each autumn season maps to one knob, and
Chapter 8's recipes are designed to teach you which is which *experientially*,
not from a table in a book.

## A truth-telling aside about "advanced" settings

If a settings panel has eight sliders and you use one (temperature, on
occasion), you are not "missing out." You're using the 20% that does the
work. The other 80% — repetition penalty, frequency penalty, presence
penalty, Mirostat, min-p — are variations on the two you already know, and
they exist for people doing specific, technical things. You will know when
you need them. And when you do, you'll reach for them the same way you'd
reach for a whisk you've seen used — not by default, but when a *recipe*
calls for it.

**→ Next: [Experiment Recipes](08-experiment-recipes.html)**
