# Chapter 4 — Max Tokens: The Price Tag on the Pot

*The setting that stops the cook mid-sentence.*

## The check at the door

Every cook-off entry gets a price tag: **max tokens** is the hard cap on how
much the model can produce in one reply. When the cap is hit, the cook just
stops — mid-sentence if necessary, fork in hand, mouth still open.

Two things people mix up:

- **Max *output* tokens** — how long one reply can be.
- **Max *context* tokens** — how big the kitchen table is (Chapter 3).

Related, not the same. A 4K-max-token model does not have a 4K-token table;
the table holds the *conversation* and the reply *shares* that budget with
it. Table size minus what's already on it is roughly what's left for the
reply.

## The three failure modes of max tokens

**1. Truncation (the polite one).** The reply just stops. You see
"finish your answer" or half a paragraph hanging. Fix: raise max tokens, or
ask for a shorter reply.

**2. The silent cutoff.** Some tools truncate without saying so. The reply
looks *complete* to you but quietly lost its last section. This is the one
that bites hardest when you're generating lists, tables, or outlines —
items 28 to 40 of your 40-item list just evaporate.

**3. Waste (the less obvious one).** Set max tokens to 8,000 and ask for a
haiku: no truncation occurs (the model stops on its own), but in
pay-per-token settings you've reserved the *possibility* of a huge reply. In
local settings this mostly costs a bit of planning overhead, not money —
but in API/web tiers with quotas, it still matters.

## Common numbers

| Setting       | Roughly                                    |
| ------------- | ------------------------------------------ |
| 256 tokens    | a paragraph (~190 words)                   |
| 1,024         | about a page (~750 words)                  |
| 2,048         | common default in many local tools         |
| 4,096         | common default in chat apps                |
| 8,192+        | needed for long lists, outlines, full essays |

Those "~750 words per 1K tokens" framings are estimates; real text has
tokenization quirks (see the glossary). Treat these as round numbers, not
laws.

## The honest trick most pros use

Rather than fighting max tokens, most people just **ask for the right
length in the prompt** and keep the cap as a safety net. "Reply in under
150 words" works because models are *very* good at element-count and
word-count requests. Then set max tokens comfortably *above* the requested
length (say, double) so the cap never actually bites.

## What to actually do

1. If replies feel long: put the length request in the *prompt*, not the
   settings.
2. If replies get cut off: raise max tokens, or split the ask ("give me
   items 1–10 now, I'll ask for 11–20 next").
3. If you're generating code or lists: budget *generously*. Lists are the
   classic silent-truncation victim.

**→ Next: [Stop Sequences](05-stop-sequences.html)**
