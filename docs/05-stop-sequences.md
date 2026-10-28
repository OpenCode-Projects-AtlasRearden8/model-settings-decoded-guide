# Chapter 5 — Stop Sequences: The STOP Sign on the Counter

*The polite interrupt button that costs nothing.*

## The index card

In the cook-off kitchen there's an index card standing on the counter. It
says **STOP** in block letters. Rule of the gym: if the cook writes that
word — exactly that word, in that case — she must drop the spoon
immediately, mid-sentence, and stop cooking. Whatever she wrote *before* the
word stays on the plate. The stop word itself does not get served.

That card is the **stop sequence**. You write one or more short strings; when
the model produces the string, generation halts.

## What it's actually for

Stop sequences are a plumbing nicety with three real jobs:

1. **Trimming scaffolding in apps.** If you run a model that ends its turn
   with `"USER:"`, you don't want `"USER:"` appearing at the bottom of every
   reply you show. Add `"USER:"` as a stop sequence and it disappears
   cleanly at the boundary.
2. **Short-circuiting format repeats.** If you ask for exactly one recipe
   and the model helpfully offers "Would you like another one? Here's one
   more:" — a stop sequence on `"Here's"` trims that.
3. **Local-model persona chases.** In roleplay/fiction setups with two
   "voices," a stop sequence on the second speaker's name keeps the model
   from wandering into writing the other character's lines.

## What stop sequences are NOT for

- **Enforcing honesty.** They cut output; they don't check it.
- **Correcting safety.** If a model *shouldn't* have said something, a stop
  sequence won't stop *that*; it stops matching *strings*, not matching
  *ideas*.
- **Repeated trimming.** Each appearance wins once and generation ends on
  the first match. If your string is `"and"`, ask yourself whether you have
  thought this through.
- **Cross-model safety.** Stop sequences are a text match, not a token
  match. Some tools implement them at the whole-text level (case-sensitive,
  exact string), some at token level, and a few ignore them entirely.
  Local-model behavior varies — which is exactly why Chapter 8's Recipe 5
  tests them.

## A concrete example

Ask a local model: *"Give me a one-paragraph summary of chili peppers, then
stop and wait for my next question."*

Model behavior varies — some happily continue with two more paragraphs.
Add a stop sequence:

```
stop: ["## NEXT", "\n\nUser", "Wait, actually"]
```

Most continuation rambles die at the first match. It's a hack, but a useful
one.

## What to actually do

1. Leave stop sequences **empty** for normal chat and answering work. Empty
   is correct.
2. Reach for them when you see a *specific repeated string* you're tired of
   receiving. Copy that string (case matters) into stop sequences.
3. If nothing changes, your tool may ignore the setting or match it only at
   the start of lines. Test with a deliberately obvious stop word
   (Chapter 8, Recipe 5) before you trust it.

**→ Next: [Seeds](06-seeds.html)**
