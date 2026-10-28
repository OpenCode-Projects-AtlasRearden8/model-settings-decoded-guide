# Chapter 2 — System Prompts: The House Rules You Set Before the Cook Starts

*The instructions nobody sees but everybody tastes.*

## The note taped to the pot

Back at the cook-off, imagine every contestant has a note taped to their pot
before judging starts. Some say:

- "Traditional Texas-style, no beans, serve it straight."
- "Vegan chili, but don't mention it's vegan unless asked."
- "This is a demo pot, let judges sample freely and explain every ingredient."

Those notes are **system prompts**. They are instructions the model reads
*before* your message, and they shape everything that follows — the tone, the
format, the boundaries, the personality. Most chat apps hide them; some local
tools let you edit them freely.

This is also the honest answer to "why does the AI sound *like that*?" —
there is very often a system prompt you never asked for.

## What belongs in one

A good system prompt is three sentences, not three paragraphs:

1. **Who the model is.** "You are a patient cooking mentor for beginners."
2. **How it should talk.** "Plain English, warm, never sarcastic."
3. **What to avoid.** "Never mention brands; keep answers under 150 words."

That's it. Longer system prompts aren't automatically better — they are just
more rules to trip over. The prompt-writing skill itself (skeletons,
examples, iteration loops) is covered chapter-by-chapter in
*The Prompt-Writing Handbook*; here we only care about the *system* slot
specifically.

## What does NOT belong in one

- **Your current* question.** The system prompt is the house rules, not menu
  orders — the actual request goes in the chat, every time.
- **Secrets.** Never put API keys, passwords, client names, or personal data
  in a system prompt. It sits there for the whole session. Treat it like a
  note taped to a pot in a public gym — anyone can read it.
- **Everything plus the kitchen sink.** Five firm rules beat fifty soft ones.

## Settings interplay: system prompts meet the other knobs

Three ways the system prompt interacts with the settings this book covers:

- **It occupies context.** The house-rules note sits on the kitchen table
  (Chapter 3) for the whole conversation. A 2,000-word system prompt eats
  table space you might want for the actual work.
- **It steers, not controls.** A system prompt biases the samples; it does
  not cap them. With temperature at 1.8, even a beautifully written system
  prompt will produce odd output sometimes. Lower the temperature too.
- **It can be per-conversation.** In chat apps you usually can't change it;
  in local tools (Ollama's `SYSTEM` blocks in a Modelfile, LM Studio,
  anything OpenAI-compatible) you can, per model — which makes for excellent
  experiments (Recipe 3 in Chapter 8).

## A quick before/after

**No system prompt:** *"Explain temperature."* → you get whatever mood the
model's default rules produce: sometimes a physics answer, sometimes a
tutorial, sometimes both.

**With a system prompt:**
```
You are a friendly cooking teacher. Explanations use kitchen
analogies only. Keep replies under 100 words. If the topic is
not about food or heat, say so in one sentence and stop.
```
Now "explain temperature" gets a lid-tightening-from-simmer-to-boil answer,
consistently, in under 100 words. **That consistency is what system prompts
are actually for.**

## What to actually do

1. Open your AI tool's settings. Find the system prompt (sometimes called
   "custom instructions" or "personality"). Read it. Now you know why it
   talks the way it does.
2. Rewrite it to three sentences that say who/how/avoid.
3. Try the same question before and after. Notice how much a short note can
   move the meal.

**→ Next: [Context Windows](03-context-windows.html)**
