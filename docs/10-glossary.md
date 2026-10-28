# Chapter 10 — Glossary

*Plain-English definitions, alphabetical, no jargon left un-jargoned-then-rescued.*

**Batch** — when a server handles several requests at once. Can change
results slightly run-to-run even with the same seed.

**Chat template** — the invisible wrapper that turns your conversation
into the format the underlying model was trained on. You rarely touch it;
local tools manage it for you.

**Context window** — the kitchen table. Everything the model can "see"
right now: system prompt, your messages, its replies. Measured in tokens.

**Default** — the value the developers picked after testing many. Usually
good. Chapter 7 is about trusting it.

**Deterministic** — same input, same output, every time. Models are
*mathematically* deterministic in principle; in practice, batching and
GPU quirks can sneak in tiny changes even with a fixed seed (Chapter 6).

**Greedy sampling** — temperature 0, conceptually: always pick the single
most likely word. Very repetitive, very reliable, occasionally stuck in a
loop.

**Max tokens** — the cap on how much the model can produce in one reply.
When reached, output stops, possibly mid-sentence (Chapter 4).

**Min-p / top-k / Mirostat** — other sampling variations. Cousins of
temperature and top-p. Top-k is a fixed roster cap; min-p and Mirostat are
fancier dials. Not needed for everyday use (Chapter 7).

**Nucleus sampling** — the fancy name for top-p. "Nucleus" = the
top-scoring core of candidates whose probabilities add up to `p`.

**Penalty (frequency / presence / repetition)** — settings that lower the
score of words already used. Another anti-repetition tool; usually not
needed if temperature is set well.

**Prompt** — anything you send the model. **System prompt** = house rules
sent first (Chapter 2). **User prompt** = your actual message.

**Sampling** — how the model picks the *next word* from its scores.
Temperature and top-p are both sampling settings; they're the dials on
the picking process (Chapter 1).

**Seed** — the dice-rigging dial. Fixed seed -> same (or near-same)
output across runs, same settings. Random seed -> fresh output every time
(Chapter 6).

**Stop sequence** — a short string (like `"STOP"` or `"User:"`) that
makes the model halt the instant it writes it. Exact text match, honored
or not depending on your backend (Chapter 5).

**Temperature** — the pot's spiciness. Low = mild, predictable, beige.
High = bold, surprising, occasionally word salad (Chapter 1).

**Token** — the chunk of text models actually count in: roughly 3–4
characters or about ¾ of an English word. Not a syllable, not a word, and
definitely not a character.

**Top-p** — the sample tray. How many candidate words (by cumulative
probability) are even considered for the next pick. Low = short, safe
tray. High = whole-gym tray (Chapter 1).

**Truncation** — output silently cut short, usually by max tokens. The
classic victim: item 28 through 40 of your 40-item list (Chapter 4).

**VRAM** — your GPU's memory. Determines *which* model fits — that's
`ai-model-picker`'s job, not this book's.
