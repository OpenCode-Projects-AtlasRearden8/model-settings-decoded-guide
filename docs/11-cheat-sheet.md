# Chapter 11 — The One-Page Cheat Sheet

*Print me. Tape me near the sliders.*

## Every knob, one line each

| Setting              | Do what                                              | When you care                                      |
| -------------------- | ---------------------------------------------------- | -------------------------------------------------- |
| **Temperature**      | low 0–0.3 for facts/code · mid 0.5–0.8 default · high 1.0+ for brainstorming | repetitive ↔ weird output trade-off |
| **Top-p**            | leave at default (often 0.9–1.0); lower for extra safety | your tool actually exposes it AND temp tweaks weren't enough |
| **System prompt**    | 3 sentences: who / how / avoid                       | tone or persona is wrong (almost never temperature's job) |
| **Context window**   | fresh chat for fresh task; paste only relevant chunks | long chats forget; big pastes overflow             |
| **Max tokens**       | ask length IN the prompt; keep cap ~2× above it       | replies cut off mid-list/mid-code                  |
| **Stop sequences**   | leave empty; add a string only when it keeps appearing | app plumbing, format repeats, persona chases       |
| **Seed**             | random for normal use; fixed when comparing runs      | testing/comparing needs repeatable output          |
| **Defaults**         | touch nothing until a *named* problem appears          | 90% of everything you ever do                      |

## The five-bet challenge (Chapter 9)

One knob per experiment. Write your prediction **before** running. Run
twice. Write the verdict in a tweet's worth of words. Five bets about  30
minutes and you'll know more than most.

## The three analogies, final form

- **Temperature** = the chili pot's spiciness. Mild pot = safe but beige.
  Five-alarm = bold but risky.
- **Top-p** = the sample tray. Short tray = only the favorites. Whole-gym
  tray = surprises included.
- **Context window** = the kitchen table. What's not on the table right
  now doesn't exist. Full table = things get dropped or skimmed.
- **System prompt** = the note taped to the pot. It shapes the whole meal
  before you ever walk up.
- **Seed** = the wheel's rigging. Constancy when pinned; novelty when not.

## Cross-references

- **Which model will fit my machine?** → `ai-model-picker` (companion CLI).
- **How do I *write* a better prompt?** → *The Prompt-Writing Handbook*
  (companion book).
- **What do the weird knobs actually do?** → This guide. You've read it.
  Go run the five bets.

---

*Model Settings, Decoded — © 2026 Asdale Dynamics, LLC. Free to share;
MIT at the project root.*
