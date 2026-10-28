#!/usr/bin/env python3
"""Model Settings, Decoded — static site builder.

Standard library only. Zero dependencies, zero network access.
Builds a static HTML site from docs/*.md so it works offline from
file:// (USB-stick ready, no server needed).

Usage:
  python3 scripts/build_site.py             # build site/ from docs/
  python3 scripts/build_site.py --check     # lint docs and links
  python3 scripts/build_site.py --from-md FILE   # render one file to HTML

Copyright (c) 2026 Asdale Dynamics, LLC — MIT licensed.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCS = PROJECT_ROOT / "docs"
DEFAULT_OUT = PROJECT_ROOT / "site"

TITLE = "Model Settings, Decoded"
SUBTITLE = "The knobs behind the chat box, explained like a friend would"
OWNER = "Asdale Dynamics, LLC"
LICENSE_LINE = "Copyright (c) 2026 Asdale Dynamics, LLC"

FRONT_STEMS = ("00-",)
SECRET_PATTERNS = [
    re.compile(r"\b(AIza[0-9A-Za-z_\-=]{20,})\b"),
    re.compile(r"\b(sk-[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(ghp_[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(gho_[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\b(xox[bpars]-[A-Za-z0-9\-]{10,})\b"),
    re.compile(r"BEGIN (RSA|OPENSSH|EC|PGP|DSA) PRIVATE KEY"),
    re.compile(r"\b(AKIA[0-9A-Z]{16})\b"),
]

BLOCK_TAGS = ("p", "h1", "h2", "h3", "h4", "ul", "ol", "table", "blockquote", "pre")


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _inline(text: str) -> str:
    """Render inline markdown: code, strong, em, links. Escapes HTML first."""
    out = html.escape(text, quote=False)
    # inline code
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    # bold then italics (bold first avoids *** mangling)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", out)
    # links [text](target)
    def _link(m: re.Match) -> str:
        text_, target = m.group(1), m.group(2)
        return f'<a href="{html.escape(target, quote=True)}">{text_}</a>'
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _link, out)
    return out


def _strip_inline_tags(text: str) -> str:
    """Plain text of an inline fragment (for table cells / heading ids)."""
    stripped = re.sub(r"<[^>]+>", "", text)
    return html.unescape(stripped)


def _heading_slug(text: str) -> str:
    text = _strip_inline_tags(_inline(text)).lower()
    text = re.sub(r"[^a-z0-9\s\-]+", "", text)
    return re.sub(r"[\s]+", "-", text.strip()) or "section"


def _render_list(items: list[tuple[int, str]], kind: str) -> str:
    """Render a (possibly nested) list. items = [(indent_level, text)]."""

    def helper(k: int, level: int) -> tuple[str, int]:
        out = [f"<{kind}>"]
        while k < len(items):
            lvl, text = items[k]
            if lvl < level:
                break
            if lvl > level:
                child, k = helper(k, lvl)
                out.append(child)
                continue
            k += 1
            if k < len(items) and items[k][0] > level:
                child, k = helper(k, items[k][0])
                out.append(f"<li>{_inline(text)}\n{child}</li>")
            else:
                out.append(f"<li>{_inline(text)}</li>")
        out.append(f"</{kind}>")
        return "\n".join(out), k

    rendered, _ = helper(0, items[0][0])
    return rendered


def markdown_to_html(md: str) -> str:
    """Render the markdown subset used by this book to HTML."""
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    first_h1_seen = False

    def close_list() -> None:
        if out and out[-1] == "</ul>":
            return
        if out and out[-1] == "</ol>":
            return

    while i < len(lines):
        line = lines[i]

        # fenced code block
        if line.startswith("```"):
            lang = line[3:].strip()
            body: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1  # closing fence
            cls = f' class="lang-{html.escape(lang, quote=True)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(body))}</code></pre>")
            continue

        # heading
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = _inline(m.group(2).strip())
            slug = _heading_slug(m.group(2))
            if level == 1 and not first_h1_seen:
                # page title rendered by the template; keep an anchor
                out.append(f'<h1 id="{slug}">{text}</h1>')
                first_h1_seen = True
            else:
                out.append(f'<h{level} id="{slug}">{text}</h{level}>')
            i += 1
            continue

        # horizontal rule
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        # blockquote (possibly multi-line)
        if line.startswith("> "):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out.append(f"<blockquote>{_inline(' '.join(quote))}</blockquote>")
            continue

        # table
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:\-\|]+\|?\s*$", lines[i + 1]) and "-" in lines[i + 1]:
            rows: list[list[str]] = []
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(header)
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table>", "<thead>", "<tr>"]
            for cell in rows[0]:
                t.append(f"<th>{_inline(cell)}</th>")
            t.append("</tr></thead>")
            if len(rows) > 1:
                t.append("<tbody>")
                for row in rows[1:]:
                    t.append("<tr>")
                    for cell in row:
                        t.append(f"<td>{_inline(cell)}</td>")
                    t.append("</tr>")
                t.append("</tbody>")
            t.append("</table>")
            out.extend(t)
            continue

        # lists, unordered and ordered, with nesting and continuation lines
        m_ul = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        m_ol = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if m_ul or m_ol:
            kind = "ul" if m_ul else "ol"
            items: list[tuple[int, str]] = []
            while i < len(lines):
                raw = lines[i]
                mu = re.match(r"^(\s*)[-*]\s+(.*)$", raw)
                mo = re.match(r"^(\s*)(\d+)\.\s+(.*)$", raw)
                got = mu if kind == "ul" else mo
                if got:
                    text_idx = 2 if mu else 3
                    items.append(
                        (len(got.group(1)), got.group(text_idx).rstrip())
                    )
                    i += 1
                elif items and raw.strip() and raw[0] == " ":
                    # continuation of the previous item
                    lvl, text = items[-1]
                    items[-1] = (lvl, (text + " " + raw.strip()))
                    i += 1
                else:
                    break
            out.append(_render_list(items, kind))
            continue

        # blank line
        if not line.strip():
            i += 1
            continue

        # paragraph (merge consecutive plain lines)
        para = [line.rstrip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{1,4}\s|>|\s*[-*]\s|\s*\d+\.\s|```)", lines[i]
        ):
            # table rows start a (checked) table on the outer loop; treat
            # a '|'-containing line directly after a paragraph as its own row
            if "|" in lines[i] and i + 1 < len(lines) and re.match(
                r"^\s*\|?[\s:\-\|]+\|?\s*$", lines[i + 1]
            ):
                break
            para.append(lines[i].rstrip())
            i += 1
        out.append(f"<p>{_inline(' '.join(para))}</p>")

    return "\n".join(out)


# ---------------------------------------------------------------- chapters

def list_chapters(docs: Path) -> list[Path]:
    files = sorted(docs.glob("*.md"))
    return files


def stem_of(p: Path) -> str:
    return p.stem


def is_front(p: Path) -> bool:
    return p.stem.startswith(FRONT_STEMS)


def chapter_title(md_text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def _page(title: str, body: str, nav: str = "", css: bool = True) -> str:
    style = '    <link rel="stylesheet" href="style.css">\n' if css else ""
    nav_html = f'<nav class="sidebar">\n{nav}\n</nav>\n' if nav else ""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n"
        f"{style}"
        "</head>\n<body>\n"
        f'{nav_html}'
        '<main class="content">\n'
        f"{body}\n"
        "</main>\n"
        f'<footer><p>{html.escape(TITLE)} — {LICENSE_LINE}. Local-first, offline-ready.</p></footer>\n'
        "</body>\n</html>\n"
    )


def build_nav(chapters: list[Path], active_stem: str = "", titles: dict[str, str] | None = None) -> str:
    titles = titles or {}
    items = [f'<div class="nav-title">{TITLE}</div>', f'<div class="nav-sub">{SUBTITLE}</div>']
    for p in chapters:
        stem = stem_of(p)
        title = titles.get(stem, stem)
        cls = ' class="active"' if stem == active_stem else ""
        items.append(f'<a href="{stem}.html"{cls}>{html.escape(title)}</a>')
    return "\n".join(items)


def build(docs: Path, out: Path) -> list[Path]:
    docs = docs.resolve()
    out = out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    chapters = list_chapters(docs)
    titles: dict[str, str] = {}
    rendered: dict[str, str] = {}
    for p in chapters:
        text = _read(p)
        titles[stem_of(p)] = chapter_title(text, p.stem)
        rendered[stem_of(p)] = markdown_to_html(text)

    # printables are copied verbatim
    printable_dir = docs / "printables"
    printables: list[Path] = []
    if printable_dir.is_dir():
        pr_dir = out / "printables"
        pr_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(printable_dir.glob("*.md")):
            (pr_dir / f.name).write_text(_read(f), encoding="utf-8")
            printables.append(pr_dir / f.name)

    nav_fragments: dict[str, str] = {}
    for p in chapters:
        nav_fragments[stem_of(p)] = build_nav(chapters, stem_of(p), titles)

    pages: list[Path] = []

    # index page
    front = [p for p in chapters if is_front(p)]
    guides = [p for p in chapters if not is_front(p)]
    front_html = rendered[stem_of(front[0])] if front else ""
    toc = ['<section class="toc"><h2>The chapters</h2><ol>']
    for p in guides:
        stem = stem_of(p)
        toc.append(f'<li><a href="{stem}.html">{html.escape(titles[stem])}</a></li>')
    toc.append("</ol></section>")
    if printables:
        toc.append('<section class="toc"><h2>Printables</h2><ul>')
        for f in printables:
            toc.append(f'<li><a href="printables/{f.name}">{html.escape(f.stem)}</a></li>')
        toc.append("</ul></section>")
    body = front_html + "\n" + "\n".join(toc)
    (out / "index.html").write_text(
        _page(f"{TITLE} — {SUBTITLE}", body, nav_fragments.get(stem_of(front[0]), build_nav(chapters, "", titles))),
        encoding="utf-8",
    )
    pages.append(out / "index.html")

    # chapter pages
    ordered = chapters
    for idx, p in enumerate(ordered):
        stem = stem_of(p)
        prev_stem = ordered[idx - 1].stem if idx > 0 else None
        next_stem = ordered[idx + 1].stem if idx + 1 < len(ordered) else None
        pager = ['<nav class="pager">']
        if prev_stem:
            pager.append(f'<a class="prev" href="{prev_stem}.html">← {html.escape(titles[prev_stem])}</a>')
        pager.append(f'<a href="index.html">Home</a>')
        if next_stem:
            pager.append(f'<a class="next" href="{next_stem}.html">{html.escape(titles[next_stem])} →</a>')
        pager.append("</nav>")
        body = rendered[stem] + "\n" + "\n".join(pager)
        (out / f"{stem}.html").write_text(
            _page(f"{titles[stem]} — {TITLE}", body, nav_fragments[stem]), encoding="utf-8"
        )
        pages.append(out / f"{stem}.html")

    # whole-book single page
    book_parts = []
    for p in ordered:
        stem = stem_of(p)
        book_parts.append(f'<section class="book-chapter" id="{stem}">{rendered[stem]}</section>')
        book_parts.append("<hr>")
    (out / "book.html").write_text(
        _page(f"{TITLE} — the whole book", "\n".join(book_parts), css=True), encoding="utf-8"
    )
    pages.append(out / "book.html")

    # stylesheet
    (out / "style.css").write_text(STYLE, encoding="utf-8")
    pages.append(out / "style.css")

    return pages


STYLE = """\
:root { --bg: #fdfcf9; --fg: #2b2a27; --accent: #8a3324; --link: #7a4a1f;
        --muted: #6b6862; --card: #f4efe6; --border: #e2dcd0; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #23211e; --fg: #e8e3da; --accent: #d97b5f; --link: #d0a169;
          --muted: #a09b92; --card: #2e2b26; --border: #45413a; }
}
* { box-sizing: border-box; }
body { margin: 0; font-family: Georgia, 'Times New Roman', serif;
       background: var(--bg); color: var(--fg); line-height: 1.65; }
nav.sidebar { position: sticky; top: 0; float: left; width: 240px; padding: 1.2rem;
       border-right: 1px solid var(--border); height: 100vh; overflow-y: auto;
       font-family: system-ui, sans-serif; font-size: 0.9rem; }
nav.sidebar .nav-title { font-weight: bold; color: var(--accent); margin-bottom: 0.2rem; }
nav.sidebar .nav-sub { color: var(--muted); font-size: 0.78rem; margin-bottom: 1rem; }
nav.sidebar a { display: block; color: var(--link); text-decoration: none;
       padding: 0.25rem 0; border-radius: 4px; }
nav.sidebar a.active { color: var(--fg); font-weight: bold; }
nav.sidebar a:hover { text-decoration: underline; }
main.content { max-width: 44rem; margin: 0 auto; padding: 2.5rem 1.4rem 3rem;
       margin-left: max(0px, calc((100% - 44rem) / 2 + 2rem)); }
h1, h2, h3 { line-height: 1.3; color: var(--accent); }
h1 { font-size: 1.7rem; margin-top: 0; }
h2 { margin-top: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
a { color: var(--link); }
code { font-family: ui-monospace, 'Cascadia Code', Menlo, Consolas, monospace;
       font-size: 0.88em; background: var(--card); padding: 0.1em 0.35em;
       border-radius: 4px; }
pre { background: var(--card); border: 1px solid var(--border); border-radius: 6px;
      padding: 0.9rem 1.1rem; overflow-x: auto; }
pre code { background: none; padding: 0; line-height: 1.5; }
blockquote { margin: 1rem 0; padding: 0.4rem 1rem; border-left: 4px solid var(--accent);
      background: var(--card); font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.93rem; }
th, td { border: 1px solid var(--border); padding: 0.45rem 0.65rem; text-align: left; }
th { background: var(--card); }
section.toc { background: var(--card); border: 1px solid var(--border);
      border-radius: 8px; padding: 1rem 1.3rem; margin: 1.5rem 0; }
section.toc ol, section.toc ul { margin: 0.4rem 0 0.2rem 1.2rem; padding: 0; }
nav.pager { display: flex; justify-content: space-between; gap: 1rem;
      margin-top: 2.5rem; font-family: system-ui, sans-serif; font-size: 0.9rem; }
nav.pager a { flex: 1; }
nav.pager a.next { text-align: right; }
footer { max-width: 60rem; margin: 0 auto; padding: 1rem 1.4rem 2rem;
      color: var(--muted); font-size: 0.8rem; font-family: system-ui, sans-serif; }
@media (max-width: 900px) {
  nav.sidebar { position: static; float: none; width: auto; height: auto;
      border-right: none; border-bottom: 1px solid var(--border); }
  main.content { margin-left: auto; margin-right: auto; }
}
@media print {
  nav.sidebar, nav.pager, footer { display: none; }
  main.content { max-width: 100%; padding: 0; margin: 0; }
  body { background: white; color: black; }
  h2 { break-after: avoid; }
  pre, table, blockquote { break-inside: avoid; }
}
"""


# ---------------------------------------------------------------- lint

def lint(docs: Path) -> list[str]:
    """Check links, anchors, heading quality, secret patterns, hygiene."""
    problems: list[str] = []
    chapters = list_chapters(docs)

    # anchors per file
    anchors: dict[str, set[str]] = {}
    for p in chapters:
        text = _read(p)
        heads = re.findall(r"^#{1,4}\s+(.+)$", text, re.MULTILINE)
        anchors[p.stem] = {_heading_slug(h) for h in heads}

    stems = {p.stem for p in chapters}
    for p in chapters:
        text = _read(p)
        rel = p.name
        # links
        for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)", text):
            target = m.group(2)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                slug = target[1:]
                if slug not in anchors[p.stem]:
                    problems.append(f"{rel}: dead anchor #{slug}")
                continue
            piece = target.split("#")[0]
            frag = target.split("#")[1] if "#" in target else None
            if piece.endswith(".html"):
                stem = piece[:-5]
                if not piece.startswith("printables/"):
                    if stem not in stems:
                        problems.append(f"{rel}: link to missing page {piece}")
                        continue
                if frag and frag not in anchors.get(stem, set()) and not piece.startswith("printables/"):
                    problems.append(f"{rel}: link to missing anchor {piece}#{frag}")
            elif piece.endswith(".md"):
                problems.append(f"{rel}: raw .md link (use .html): {piece}")
            # else: relative asset, skip in lint (printables handled above)
        # heading sanity: each numbered chapter has exactly one H1
        h1s = re.findall(r"^#\s+(?!#)(.+)$", text, re.MULTILINE)
        if len(h1s) != 1:
            problems.append(f"{rel}: expected exactly one H1, found {len(h1s)}")
        # non-ASCII except common punctuation/curly quotes/em dashes
        for ch in text:
            if ord(ch) > 0x2122 and ch not in "⟶→←↔✓✗":
                problems.append(f"{rel}: unexpected non-ASCII character {ch!r} (U+{ord(ch):04X})")

    # secret scan across docs
    for p in chapters:
        text = _read(p)
        for pat in SECRET_PATTERNS:
            m = pat.search(text)
            if m:
                problems.append(f"{p.name}: possible secret matching {pat.pattern[:40]}")

    printables = docs / "printables"
    if printables.is_dir():
        for p in sorted(printables.glob("*.md")):
            text = _read(p)
            for pat in SECRET_PATTERNS:
                if pat.search(text):
                    problems.append(f"printables/{p.name}: possible secret")

    expected = {
        "00-introduction.md",
        "01-temperature-and-top-p.md",
        "02-system-prompts.md",
        "03-context-windows.md",
        "04-max-tokens.md",
        "05-stop-sequences.md",
        "06-seeds.md",
        "07-when-defaults-are-fine.md",
        "08-experiment-recipes.md",
        "09-settings-betting-worksheet.md",
        "10-glossary.md",
        "11-cheat-sheet.md",
    }
    actual = {p.name for p in chapters}
    missing = expected - actual
    extra = actual - expected
    if missing:
        problems.append(f"missing expected chapters: {sorted(missing)}")
    if extra:
        print(f"note: extra chapters present (fine, not an error): {sorted(extra)}")

    # repo hygiene: LICENSE line, README credit
    lic = PROJECT_ROOT / "LICENSE"
    if lic.exists():
        if LICENSE_LINE not in _read(lic):
            problems.append("LICENSE: missing exact copyright line")
    else:
        problems.append("LICENSE: file not found")
    readme = PROJECT_ROOT / "README.md"
    if readme.exists():
        if OWNER not in _read(readme):
            problems.append(f"README: missing credit for {OWNER}")
    else:
        problems.append("README: file not found")

    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the Model Settings, Decoded site")
    ap.add_argument("--docs", type=Path, default=DEFAULT_DOCS)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="lint docs and exit")
    ap.add_argument("--from-md", type=Path, help="render one markdown file to HTML on stdout")
    args = ap.parse_args(argv)

    if args.from_md:
        path = args.from_md
        print(markdown_to_html(_read(path)))
        return 0

    if args.check:
        problems = lint(args.docs)
        if problems:
            for p in problems:
                print(f"PROBLEM: {p}", file=sys.stderr)
            print(f"Checked {len(list_chapters(args.docs))} markdown files: "
                  f"{len(problems)} problem(s)", file=sys.stderr)
            return 1
        print(f"Checked {len(list_chapters(args.docs))} markdown files: clean")
        return 0

    pages = build(args.docs, args.out)
    print(f"Built {len(pages)} files into {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
