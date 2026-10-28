# STATUS

Project: Model Settings, Decoded (the "knobs behind the chat box" guide)
Owner: Asdale Dynamics, LLC
State: complete and verified (October 2026)

## What was built

A beginner-facing manual that decodes the numbered settings in every AI
tool's panel — written "like a friend would": warm, plain English, never
condescending — plus the tooling that turns it into a static offline
website.

- **docs/** (12 Markdown files: front matter + 11 chapters + 1 printable):
  - `00-introduction.md` — audience, reading paths, a one-minute before/after temperature experiment.
  1. Temperature & Top-P — the **chili cook-off**: the pot's spiciness vs. the sample tray; low/mid/high recipes table; anti-repetition and anti-chaos moves; top-k aside.
  2. System Prompts — house rules taped to the pot; who/how/avoid three-sentence pattern; what belongs (and never belongs — no secrets); interplay with context, temperature, local Modelfiles.
  3. Context Windows — the **kitchen table**: what counts as a plate, token sizes table, the middle-seat attention problem, four ways tables fill, symptoms checklist.
  4. Max Tokens — the price tag on the pot; truncation, the silent cutoff, and waste; the "ask length in the prompt, cap as a net" trick.
  5. Stop Sequences — the STOP sign index card; real use cases (app plumbing, format repeats, persona chases); what they are NOT for; exact-string-match caveats.
  6. Seeds — the dartboard/rigged wheel; testing vs. brainstorming; why seed + pinned settings is a strong hint, not a guarantee (GPU/batching caveats); the seed-temperature combo people get wrong.
  7. When Defaults Are Fine — the honest chapter; when to leave everything alone; a short "when to actually turn a knob" table; tone lives in the system prompt, not the temperature.
  8. Experiment Recipes — six hands-on recipes (five + one bonus) for a local model (Ollama/LM Studio, OpenAI-compatible): kitchen-table edges, temperature three-way, system-prompt personalities, seed pinning, stop-sign behavior testing, max-token guillotine.
  9. The Settings-Betting Worksheet — predict-before-you-run log; filled-in example; the five-bet challenge (five knobs, ~30 minutes).
  10. Glossary — ~30 plain-English definitions (Nucleus sampling, tokens, VRAM vs. this book's scope, etc.).
  11. Cheat Sheet — printable one-page summary of every knob, the three analogies' final form, and cross-references to companions.
  - `printables/worksheet.md` — the standalone printable worksheet.
- **scripts/build_site.py**: standard-library-only static site builder (zero dependencies, zero network). Produces a landing page, one page per chapter with sidebar nav + prev/next pager, a single-page `book.html`, a light/dark-aware stylesheet with print styles, and emits `printables/` verbatim. `--check` lints links (dead pages/anchors, raw `.md` links), heading sanity (exactly one H1 per file), non-ASCII hygiene, secret-pattern scans, and repo hygiene (exact MIT line, README credit).
- **tests/test_site.py**: 57 tests covering the Markdown converter (inline, headings, fences, tables, nested lists with continuation lines, escaping), the builder (pagination, nav, printables, offline-reference check, HTML tag-balance via html.parser), reproducible builds (byte-identical), lint rules (each individually), the CLI (build, check exit codes, --from-md), and repo hygiene (exact copyright, README credit, secret scan, chapter inventory, and a companion-overlap check asserting the book references but never re-teaches the companion projects).
- **README.md, LICENSE** (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC"), **.gitignore**.

## How to run it

```bash
python3 scripts/build_site.py            # build site/ from docs/
python3 scripts/build_site.py --check    # lint docs (links, anchors, hygiene)
python3 -m unittest discover -s tests    # run the 57-test suite
python3 scripts/build_site.py --from-md docs/10-glossary.md   # one file -> HTML
```

Then open `site/index.html` in a browser — no server needed; the site makes
zero external requests (only localhost endpoint examples inside code
samples), so it works offline and from `file://` (USB-stick ready).
Experiments in Chapter 8 need a local model (Ollama/LM Studio) but no
accounts and no API keys.

## Positioning vs. companions (no repetition)

- `ai-model-picker-cli` answers "which model will *run* on my machine?"
  (hardware fit). This book starts after that: you have a model, here is
  what the settings do.
- `prompt-writing-handbook` teaches *writing* prompts. This book covers the
  *settings* shaping every prompt's output. A repo-hygiene test
  (`test_companions_not_repeated`) enforces that the book references both
  without re-teaching them.

## Verification results (run in this folder)

- `python3 scripts/build_site.py --check` → "Checked 12 markdown files: clean"
- `python3 scripts/build_site.py` → "Built 15 files into .../site" (14 HTML pages + style.css + printables/)
- HTML structural check (`html.parser` tag balance over all generated pages) → 0 problems, enforces no unbalanced markup
- `python3 -m unittest discover -s tests` → 57 tests, OK (0 failures, 0 errors)
- Reproducible-build test: two consecutive builds into fresh dirs produce byte-identical files, including printables/
- Offline test: no `http(s)://` URLs outside localhost examples in any built page
- Secret-pattern scan across docs/scripts/tests/README/LICENSE → 0 matches
- Link lint: every `.html` link resolves to a built chapter; every `#anchor` matches a real heading slug; no raw `.md` links
- Git initialized with the existing configured identity; committed, nothing pushed, no remote, no Co-authored-by trailers

## Known gaps

- The book *describes* Ollama/LM Studio behavior from common knowledge and
  does not execute a live model in CI (no model downloads here — the
  recipes are deliberately for the reader's own machine).
- Chapter 8's recipe count says "five evenings" but includes a sixth bonus
  recipe; the numbering is explained in-line rather than renamed.
- `balanced two-level list nesting is supported; deeper nesting (3+ levels)
  normalizes to the second level rather than rendering deeper hierarchy.
- No e-reader export (EPUB/PDF) — `book.html` with print styles is the
  printing stopgap, same approach as the sibling handbook.
- The site builder does not render Markdown inside table cells spanning
  multiple lines, or reference-style links `[x][1]`; the book's own
  Markdown subset avoids both (and `--check` keeps it that way).
