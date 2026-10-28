# Chapter 3 — Context Windows: The Kitchen Table

*How much room the model has to think, written as furniture.*

## The table

Imagine a very literal cook with a very literal memory: anything not
**physically on the kitchen table** doesn't exist. Doesn't matter that you
told her about your grandmother's chili recipe last week — it happened
elsewhere, so it's gone.

The kitchen table is the **context window**: everything the model can
"see" right now. That includes:

- the system prompt (the taped-on house rules — Chapter 2),
- your messages,
- the model's own replies,
- tool output if you've wired any up.

When the table gets full, something has to give. Different tools handle it
differently — some quietly drop the oldest plates, some refuse new ones,
some show you an error. Understanding the table explains all three.

## How big are these tables?

Tables are measured in **tokens** — chunks of text, roughly
3–4 characters or about ¾ of a word each. Common sizes you'll run into:

| Table size            | Rough words | Rough equivalent                        |
| --------------------- | ----------- | ---------------------------------------- |
| 4K tokens             | ~3,000      | a fairly long email                      |
| 8K tokens             | ~6,000      | a short story, or this chapter twice over|
| 32K tokens            | ~24,000     | a novella                                |
| 128K tokens           | ~96,000     | a short novel                            |
| 200K–1M+ tokens       | up to ~750K | increasingly common in 2025–2026 models  |

Small local models often still top out at modest sizes, so this chapter
matters *most* if you run things on your own machine.

## Not-all-tokens-are-equal: the middle-seat problem

Here's the part most guides skip: the model doesn't treat every plate on the
table the same. Attention research's consistent finding (and every
practitioner's experience) is:

- **Plates near the edges get noticed most.** The system prompt at one end
  and the newest messages at the other end get strong attention.
- **Plates in the middle get skimmed.** Long conversations, long documents:
  the stuff in the middle quietly matters less. "The model forgot section 3"
  is usually a middle-seat problem.

Practical translation: if something must be remembered, put it at the
**start** (system prompt) or **re-state it near the end** of your message.

## The four ways tables fill up

1. **Long conversations.** Every reply you keep is a plate that stays.
2. **Big pastes.** Congratulations, you put a whole book on the table; there
   is no room left for lunch.
3. **Attachments.** A 50-page PDF is a table-filler, whether you meant it to
   be or not.
4. **Bloated system prompts.** A 3,000-word personality from Chapter 2 is
   a permanent, non-negotiable plate.

## Symptoms of a full table

| Symptom                                        | Likely cause                          |
| ---------------------------------------------- | ------------------------------------- |
| Model "forgets" early instructions             | old plates dropped or drifted to the middle |
| It keeps answering the *earlier* question      | recent context lost when the table reset   |
| Nicely formatted refusal about "too much text" | overflow guard tripped                     |
| Repetition of things you already said          | it literally cannot see you said them      |
| Odd tone shift mid-conversation                | a long system prompt finally outnumbered by message history |

## What to actually do

1. **Start a fresh chat for a fresh task.** The cheapest fix. Old plates
   gone, full table for the new work.
2. **Paste only the relevant chunk.** "Summarize chapter 4" doesn't need
   chapters 1–3 on the table.
3. **Put the permanent stuff in the system prompt** (house rules) and the
   *current* stuff in the chat (tonight's plates).
4. **For local models, check the number.** Ollama often defaults to a small
   table (you may see `num_ctx: 2048`–`4096` hidden in logs); LM Studio
   shows a context-length slider per model. If your model has 8K and you're
   feeding it 10K tokens, *something* is silently going wrong.

**Chapter 8's Recipe 1 is a table-width experiment** designed to make the
edge visible: paste a long list, hide a secret word in the middle, and watch
the model find or miss it.

**→ Next: [Max Tokens](04-max-tokens.html)**
