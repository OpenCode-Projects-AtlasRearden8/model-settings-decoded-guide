# Chapter 8 — Experiment Recipes: Five Hands-On Evenings With a Local Model

*Learn the knobs by turning them, one at a time, tonight.*

## What you need

- A local model running. **Ollama** (free, one command, `ollama pull
  llama3.2` or `qwen2.5:7b`) or **LM Studio** (point-and-click, shows every
  knob with a slider). If you're unsure what will fit on your machine,
  that's literally what `ai-model-picker` is for.
- Somewhere to send requests. LM Studio's UI works with zero code. If you
  like the terminal, `curl` against the OpenAI-compatible endpoint is
  enough:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "temperature": 0.7,
    "top_p": 0.9,
    "messages": [
      {"role": "system", "content": "You are a chili judge. Answer briefly."},
      {"role": "user", "content": "Rate my chili recipe in one sentence."}
    ]
  }'
```

- A notebook (paper is fine) or the worksheet from Chapter 9.
- **The golden rule of all five recipes: change ONE setting at a time.**
  Everything else stays put. That's what makes the result mean something.

## Recipe 1 — Prove the kitchen table has edges (context window)

**Goal:** feel where the table ends.

1. Ask: *"Remember the number: [pick one, e.g., 47 apples]."*
2. Paste a long filler — 20+ pages of some public-domain text, or several
   long Wikipedia paragraphs about chili peppers.
3. Ask again at the end: *"What number did I ask you to remember?"*

**What you'll see:** small local models (4K–8K context) will "forget" the
number once the filler is long enough. Larger models hold longer. You have
just *seen* the table's edge. Note where it fell off on your setup — that
number is your model's real, felt context window, more useful than the one
on the box.

**Bonus round:** for tools that let you set context length (Ollama's
`num_ctx`, LM Studio's context slider), back the number down to 2,048 and
watch it break even sooner. That's the slider doing its job.

## Recipe 2 — Watch temperature move the pot (temperature)

**Goal:** run one question at three temperatures and compare.

Ask, at **temperature 0.1**, then **0.7**, then **1.4** (re-run each 3
times):

> *"Give me five totally unique ways to describe chili peppers to someone who has never had one."*

**What you'll see:**

- **0.1:** the same five descriptions, every run. Reliable. A little dry.
- **0.7:** mostly the same answers, one or two swaps. The house style.
- **1.4:** five wildly different lists each time. Some gems. Some word
  salad. It's a grab bag.

On the worksheet, rate each run for **sense** and **freshness** on a 1–5
scale and watch the trade-off appear on paper. That trade-off IS the
temperature knob, felt.

## Recipe 3 — System prompts are house rules (system prompt)

**Goal:** same question, three different house-rule notes.

Keep temperature fixed at 0.7. Run the same user prompt —

> *"What do I need to make good chili?"*

— under three different system prompts:

- **A (default):** whatever your tool has (or blank).
- **B:** `You are a terse hardcore pitmaster. Answers in 20 words max.`
- **C:** `You are a caring grandma. Warm, chatty, always ends with a gentle nudge to eat something.`

**What you'll see:** three different *personalities* from the same model
at the same temperature. That's the system prompt doing real work. Notice
that B feels *different* even though the temperature didn't move — this is
the chapter-7 lesson in action: tone lives in the system prompt, not the
temp knob.

## Recipe 4 — Pin the dart (seed)

**Goal:** see what a fixed seed does, and what it doesn't.

Run the same prompt twice with `seed: 42`, `temperature: 1.2`:

> *"Invent a chili cookoff prize name."*

- **Case A:** temperature 1.2, seed 42, twice. Expect the same idea, often
  the near-same text.
- **Case B:** temperature 1.2, seed 42, then seed 7, then seed 123.
  Three different ideas, similar overall flavor.
- **Case C:** temperature 0.2, seed 42, twice. Same as each other —
  and *boring*.

**What you'll see:** fixed seed = same idea re-served. Different seed =
new idea, same pot. Boring temperature, same seed, still boring. This is
the seed/temperature partnership, seen directly.

## Recipe 5 — The STOP sign (stop sequences)

**Goal:** make the sign work, then break it.

Add a stop sequence of `"STOP"`:

1. Ask: *"Explain chili peppers in three sentences, then write STOP, then
   invent a chili-themed haiku."*
2. Run it with `stop: ["STOP"]`. The haiku never lands. The card worked.
3. Run it with `stop: ["stop"]` (lowercase). Depending on your backend,
   the sign may not match — no stop.
4. Run it with `stop: ["STOP ", "STOP\n", "STOP."]` (with trailing
   variations). Now it catches all the variants.

**What you'll see:** stop sequences are *exact string matches*, and local
implementations vary in what they honor. Note which variant of the STOP
the model actually emits on your setup, and learn your backend's habits
by testing, not by hoping.

## Recipe 6 (bonus) — max tokens, the hard cap

**Goal:** watch the reply get guillotined.

Ask for a 10-item chili-pepper top-ten list with `max_tokens: 64`.
Count what comes back. Then try 256. Note how the cap feels when it's
*too low*, and where it stops mattering.

## Keeping the experiments honest

- Write your prediction **before** you run (Chapter 9's worksheet exists
  for exactly this and prints on one sheet).
- Run each *twice*. A once-run "surprise" is often a random seed, not a
  property of the setting. Twice tells you whether it's repeatable.
- Note your model name and size. A 1B model and a 70B model behave very
  differently at temperature 1.4; only your own notes describe *your*
  pot.

**→ Next: [The Settings-Betting Worksheet](09-settings-betting-worksheet.html)**
