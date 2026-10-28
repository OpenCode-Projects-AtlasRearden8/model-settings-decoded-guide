# Model Settings, Decoded

"Temperature? Top-p? Seed? What am I supposed to do with these?" — answered
like a friend would.

**Model Settings, Decoded** is a beginner-friendly manual for the numbered
knobs hiding in every AI tool's settings panel. No physics degree required,
no condescension — just two ordinary analogies that refuse to leave:

- **temperature and top-p** as a **chili cook-off** (how spicy is the pot,
  and how many contestant samples get on the judge's tray)
- **context windows** as a **kitchen table** (how much food fits before
  things fall off the edges)

Plus system prompts (house rules taped to the pot), max tokens, stop
sequences, seed, and — the honest chapter — **when defaults are fine**
(most of the time).

Built and maintained by **Asdale Dynamics, LLC** as part of a
beginner-first AI toolkit. Local-first, standard library only (no
dependencies), and the built website makes zero external requests, so it
works offline from `file://` — USB-stick ready.

## What's inside

| Path                  | What it is                                               |
| --------------------- | -------------------------------------------------------- |
| `docs/`               | The book: front matter + 11 chapters in plain Markdown   |
| `docs/printables/`    | The settings-betting worksheet as a standalone printable |
| `scripts/build_site.py` | Stdlib-only static site builder (build + `--check` lint) |
| `site/`               | The built website (generated; open `index.html`)         |
| `tests/`              | Test suite for the markdown converter, builder, and lint  |

### The chapters

0. Introduction — who this is for, the 60-second experiment
1. Temperature & top-p — the chili cook-off (mild pot / sample tray)
2. System prompts — the house rules you set before the cook starts
3. Context windows — the kitchen table, and how tables fill up
4. Max tokens — the price tag on the pot
5. Stop sequences — the STOP sign on the counter
6. Seeds — the replay dial, and why it is not a guarantee
7. When defaults are fine — the honest chapter
8. Experiment recipes — five hands-on evenings with a local model
9. The settings-betting worksheet — predict, run, record, learn
10. Glossary — plain-English definitions
11. One-page cheat sheet — printable summary

## How to use it

Nothing to install. Python 3.9+ (standard library only).

```bash
# build site/ from docs/
python3 scripts/build_site.py

# lint the book (links, anchors, heading sanity, secret scan, hygiene)
python3 scripts/build_site.py --check

# run the test suite
python3 -m unittest discover -s tests

# render one markdown file to HTML on stdout
python3 scripts/build_site.py --from-md docs/01-temperature-and-top-p.md
```

Then open `site/index.html` in a browser. No server needed. Every experiment
in Chapter 8 runs against a local model (Ollama or LM Studio) on your own
machine — no accounts, no API keys.

## The experiment loop this book teaches

One knob at a time. Write your prediction **before** you run. Run twice.
Record the verdict in a tweet's worth of words. Five bets, one per knob,
about 30 minutes — after that you know these settings better than most
people who talk about them confidently online.

## Companions (read them together, they don't overlap)

- **ai-model-picker** — answers "which model will actually *run* on my
  machine?" by reading your hardware. This book starts *after* that
  question: you have a model; now what do the knobs do?
- **The Prompt-Writing Handbook** — teaches you to *write* better prompts
  (roles, examples, iteration). This book covers the *settings* that shape
  every prompt's output; the two are referenced but never repeated.

## Repo hygiene

MIT licensed — see `LICENSE`. No secrets, no API keys, no personal data in
any file (the test suite scans for this). Commit only as the repository's
existing git identity; never push or publish from this repo.

*Copyright (c) 2026 Asdale Dynamics, LLC*
