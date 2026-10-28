"""Tests for the Model Settings, Decoded site builder.

Covers: markdown converter, chapter metadata, site building, lint rules,
CLI behavior, reproducible builds, offline-ness, and repo hygiene.
Run: python3 -m unittest discover -s tests
"""

import io
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))
import build_site as pipeline


class TestInline(unittest.TestCase):
    def test_bold(self):
        self.assertEqual(pipeline._inline("**hi**"), "<strong>hi</strong>")

    def test_emphasis(self):
        self.assertEqual(pipeline._inline("*soft*"), "<em>soft</em>")

    def test_inline_code(self):
        self.assertEqual(pipeline._inline("`x=1`"), "<code>x=1</code>")

    def test_link(self):
        self.assertEqual(
            pipeline._inline("[a](b.html)"), '<a href="b.html">a</a>'
        )

    def test_link_quotes_escaped(self):
        self.assertIn('<a href="a&quot;b.html">', pipeline._inline('[t](a"b.html)'))

    def test_html_escaped(self):
        self.assertEqual(
            pipeline._inline("a <b> & c"), "a &lt;b&gt; &amp; c"
        )

    def test_bold_and_em_combined(self):
        self.assertEqual(
            pipeline._inline("**bold** and *soft*"),
            "<strong>bold</strong> and <em>soft</em>",
        )

    def test_bold_forbidden_username_nor(self):
        # two separate bolds on one line both render
        self.assertIn("<strong>a</strong>", pipeline._inline("**a** **b**"))
        self.assertIn("<strong>b</strong>", pipeline._inline("**a** **b**"))


class TestHeadingsAndSlugs(unittest.TestCase):
    def test_slug_basic(self):
        self.assertEqual(
            pipeline._heading_slug("Chapter 1 — Temperature and Top-P"),
            "chapter-1-temperature-and-top-p",
        )

    def test_slug_removes_punct(self):
        self.assertEqual(
            pipeline._heading_slug("Why, me? (yes)"), "why-me-yes"
        )

    def test_heading_anchors_h2(self):
        html_out = pipeline.markdown_to_html("## Cool Heading\n\ntext")
        self.assertIn('<h2 id="cool-heading">Cool Heading</h2>', html_out)

    def test_h1_anchor(self):
        html_out = pipeline.markdown_to_html("# Title Here\n\nbody")
        self.assertIn('<h1 id="title-here">Title Here</h1>', html_out)


class TestBlocks(unittest.TestCase):
    def test_paragraph_run_merges(self):
        html_out = pipeline.markdown_to_html("one two\nthree")
        self.assertIn("<p>one two three</p>", html_out)

    def test_paragraph_breaks_on_heading(self):
        html_out = pipeline.markdown_to_html("text\n## Head\n\nmore")
        self.assertIn("<p>text</p>", html_out)
        self.assertIn("<h2", html_out)

    def test_fence_code(self):
        html_out = pipeline.markdown_to_html("```bash\ncurl -d '{}'\n```")
        self.assertIn("<pre><code", html_out)
        self.assertIn("curl -d &#x27;{}&#x27;", html_out)

    def test_fence_lang_class(self):
        html_out = pipeline.markdown_to_html("```python\nx=1\n```")
        self.assertIn('class="lang-python"', html_out)

    def test_fence_open_at_eof(self):
        html_out = pipeline.markdown_to_html("```\nno close")
        self.assertIn("<pre><code", html_out)

    def test_blockquote(self):
        html_out = pipeline.markdown_to_html("> A quote\n> continued here")
        self.assertIn("<blockquote>A quote continued here</blockquote>", html_out)

    def test_hr(self):
        self.assertIn("<hr>", pipeline.markdown_to_html("---"))

    def test_table_renders(self):
        md = "| A | B |\n| --- | --- |\n| 1 | 2 |\n"
        html_out = pipeline.markdown_to_html(md)
        self.assertIn("<table>", html_out)
        self.assertIn("<th>A</th>", html_out)
        self.assertIn("<td>1</td>", html_out)
        self.assertIn("<td>2</td>", html_out)

    def test_table_inline_md_in_cells(self):
        md = "| a | b |\n| --- | --- |\n| **bold** | `code` |\n"
        html_out = pipeline.markdown_to_html(md)
        self.assertIn("<strong>bold</strong>", html_out)
        self.assertIn("<code>code</code>", html_out)

    def test_table_with_leading_pipe(self):
        md = "| A | B |\n| --- | --- |\n| x | y |\n"
        self.assertIn("<table>", pipeline.markdown_to_html(md))

    def test_unordered_list(self):
        md = "- one\n- two\n"
        html_out = pipeline.markdown_to_html(md)
        self.assertIn("<ul>", html_out)
        self.assertIn("<li>one</li>", html_out)
        self.assertIn("<li>two</li>", html_out)
        self.assertIn("</ul>", html_out)

    def test_list_continuation_joins(self):
        md = "- alpha\n  continued\n- beta\n"
        html_out = pipeline.markdown_to_html(md)
        self.assertIn("<li>alpha continued</li>", html_out)

    def test_ordered_list(self):
        html_out = pipeline.markdown_to_html("1. first\n2. second\n")
        self.assertIn("<ol>", html_out)
        self.assertIn("<li>first</li>", html_out)
        self.assertIn("<li>second</li>", html_out)

    def test_ordered_continuation_joins(self):
        html_out = pipeline.markdown_to_html("1. first\n   more words\n2. second\n")
        self.assertIn("<li>first more words</li>", html_out)

    def test_nested_list(self):
        md = "- outer\n  - inner\n"
        html_out = pipeline.markdown_to_html(md)
        self.assertIn("<ul>", html_out)
        # nested list must appear between the outer li open and close
        self.assertIn("<li>outer", html_out)
        self.assertIn("<li>inner</li>", html_out)

    def test_ast_marker_list(self):
        html_out = pipeline.markdown_to_html("* a\n* b\n")
        self.assertIn("<li>a</li>", html_out)

    def test_blank_lines_no_empty_paragraphs(self):
        html_out = pipeline.markdown_to_html("\n\n\n\ntext\n\n\n")
        self.assertNotIn("<p></p>", html_out)
        self.assertIn("<p>text</p>", html_out)


class TestBuilding(unittest.TestCase):
    """Build the real book into a temp dir; assertions over the output."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="msd-build-")
        cls.out = Path(cls.tmp) / "site"
        cls.chapters = pipeline.build(pipeline.DEFAULT_DOCS, cls.out)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_all_pages_built(self):
        names = {p.name for p in self.chapters}
        expected_pages = {"index.html", "book.html", "style.css"}
        for p in pipeline.list_chapters(pipeline.DEFAULT_DOCS):
            expected_pages.add(p.stem + ".html")
        self.assertEqual(names, expected_pages)

    def test_index_links_all_chapters(self):
        text = (self.out / "index.html").read_text(encoding="utf-8")
        for p in pipeline.list_chapters(pipeline.DEFAULT_DOCS):
            self.assertIn(f'href="{p.stem}.html"', text)

    def test_chapter_pages_have_pager(self):
        text = (self.out / "03-context-windows.html").read_text(encoding="utf-8")
        self.assertIn('class="pager"', text)
        self.assertIn('href="02-system-prompts.html"', text)
        self.assertIn('href="04-max-tokens.html"', text)

    def test_nav_active_class(self):
        text = (self.out / "05-stop-sequences.html").read_text(encoding="utf-8")
        self.assertIn('href="05-stop-sequences.html" class="active"', text)

    def test_book_contains_all_chapters(self):
        text = (self.out / "book.html").read_text(encoding="utf-8")
        for p in pipeline.list_chapters(pipeline.DEFAULT_DOCS):
            self.assertIn(f'<section class="book-chapter" id="{p.stem}">', text)

    def test_analogies_present_in_output(self):
        text = (self.out / "book.html").read_text(encoding="utf-8")
        for phrase in ("chili cook-off", "kitchen table", "top-p", "seed"):
            self.assertIn(phrase, text.lower())

    def test_printable_copied(self):
        pr = self.out / "printables" / "worksheet.md"
        self.assertTrue(pr.exists())

    def test_no_external_urls_in_html(self):
        """No remote URLs — localhost endpoint docs in code samples are fine."""
        for pg in self.out.glob("*.html"):
            text = pg.read_text(encoding="utf-8")
            for m in re.finditer(r"https?://[^\"'\s<>]+", text):
                url = m.group(0)
                self.assertTrue(
                    url.startswith(("http://localhost", "http://127.0.0.1")),
                    f"{pg.name}: non-local URL {url}",
                )

    def test_css_uses_prefers_color_scheme(self):
        css = (self.out / "style.css").read_text(encoding="utf-8")
        self.assertIn("prefers-color-scheme", css)
        self.assertIn("@media print", css)

    def test_html_tag_balance(self):
        from html.parser import HTMLParser

        class Balance(HTMLParser):
            VOID = {
                "area", "base", "br", "col", "embed", "hr", "img", "input",
                "link", "meta", "param", "source", "track", "wbr",
            }

            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.stack = []
                self.problems = 0

            def handle_starttag(self, tag, attrs):
                if tag not in self.VOID:
                    self.stack.append(tag)

            def handle_endtag(self, tag):
                if tag in self.VOID:
                    return
                if self.stack and self.stack[-1] == tag:
                    self.stack.pop()
                else:
                    self.problems += 1

        for pg in self.out.glob("*.html"):
            parser = Balance()
            parser.feed(pg.read_text(encoding="utf-8"))
            parser.close()
            self.assertEqual(
                (parser.problems, parser.stack), (0, []), f"{pg.name} unbalanced"
            )

    def test_chapter_ids_unique_and_real(self):
        text = (self.out / "index.html").read_text(encoding="utf-8")
        m = re.search(r'<li><a href="([^"]+)"', text)
        self.assertTrue(m)


class TestReproducible(unittest.TestCase):
    def test_two_builds_identical(self):
        d1 = Path(tempfile.mkdtemp(prefix="msd-r1-"))
        d2 = Path(tempfile.mkdtemp(prefix="msd-r2-"))
        try:
            pipeline.build(pipeline.DEFAULT_DOCS, d1)
            pipeline.build(pipeline.DEFAULT_DOCS, d2)
            files1 = sorted(str(p.relative_to(d1)) for p in d1.rglob("*") if p.is_file())
            files2 = sorted(str(p.relative_to(d2)) for p in d2.rglob("*") if p.is_file())
            self.assertEqual(files1, files2)
            for name in files1:
                self.assertEqual(
                    (d1 / name).read_bytes(), (d2 / name).read_bytes(),
                    f"file differs: {name}",
                )
        finally:
            shutil.rmtree(d1, ignore_errors=True)
            shutil.rmtree(d2, ignore_errors=True)


class TestLint(unittest.TestCase):
    def test_real_docs_clean(self):
        problems = pipeline.lint(pipeline.DEFAULT_DOCS)
        # LICENSE and README exist in the repo, so should be no problems
        self.assertEqual(problems, [], f"lint problems: {problems}")

    def test_dead_anchor_caught(self):
        docs = Path(tempfile.mkdtemp(prefix="msd-l1-"))
        try:
            (docs / "00-intro.md").write_text(
                "# Hello\n\nSee [x](#no-such-anchor)\n", encoding="utf-8"
            )
            problems = pipeline.lint(docs)
            self.assertTrue(any("no-such-anchor" in p for p in problems))
        finally:
            shutil.rmtree(docs, ignore_errors=True)

    def test_dead_page_link_caught(self):
        docs = Path(tempfile.mkdtemp(prefix="msd-l2-"))
        try:
            (docs / "00-intro.md").write_text(
                "# Hello\n\nSee [x](99-missing.html)\n", encoding="utf-8"
            )
            problems = pipeline.lint(docs)
            self.assertTrue(any("99-missing.html" in p for p in problems))
        finally:
            shutil.rmtree(docs, ignore_errors=True)

    def test_raw_md_link_caught(self):
        docs = Path(tempfile.mkdtemp(prefix="msd-l3-"))
        try:
            (docs / "00-intro.md").write_text(
                "# Hello\n\nSee [x](01-other.md)\n", encoding="utf-8"
            )
            problems = pipeline.lint(docs)
            self.assertTrue(any("raw .md link" in p for p in problems))
        finally:
            shutil.rmtree(docs, ignore_errors=True)

    def test_multiple_h1_caught(self):
        docs = Path(tempfile.mkdtemp(prefix="msd-l4-"))
        try:
            (docs / "00-intro.md").write_text(
                "# One\n\ntext\n\n# Two\n", encoding="utf-8"
            )
            problems = pipeline.lint(docs)
            self.assertTrue(any("exactly one H1" in p for p in problems))
        finally:
            shutil.rmtree(docs, ignore_errors=True)

    def test_secret_pattern_caught(self):
        docs = Path(tempfile.mkdtemp(prefix="msd-l5-"))
        try:
            fake = "sk-" + "a" * 40
            (docs / "00-intro.md").write_text(
                f"# Hello\n\nkey {fake}\n", encoding="utf-8"
            )
            problems = pipeline.lint(docs)
            self.assertTrue(any("possible secret" in p for p in problems))
        finally:
            shutil.rmtree(docs, ignore_errors=True)

    def test_missing_chapter_caught(self):
        docs = Path(tempfile.mkdtemp(prefix="msd-l6-"))
        try:
            (docs / "00-introduction.md").write_text("# Hi\n\ntext\n", encoding="utf-8")
            problems = pipeline.lint(docs)
            self.assertTrue(any("missing expected chapters" in p for p in problems))
        finally:
            shutil.rmtree(docs, ignore_errors=True)


class TestCLI(unittest.TestCase):
    def test_check_exit_zero(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "build_site.py"), "--check"],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("clean", r.stdout)

    def test_check_exit_nonzero_on_problems(self):
        docs = Path(tempfile.mkdtemp(prefix="msd-cli-"))
        try:
            (docs / "99-not-expected.md").write_text("# X\n\ntext\n")
            r = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_site.py"),
                 "--check", "--docs", str(docs)],
                capture_output=True, text=True,
            )
            self.assertEqual(r.returncode, 1)
        finally:
            shutil.rmtree(docs, ignore_errors=True)

    def test_from_md_outputs_html(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "build_site.py"),
             "--from-md", str(pipeline.DEFAULT_DOCS / "10-glossary.md")],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("<h1", r.stdout)

    def test_build_cli(self):
        out = Path(tempfile.mkdtemp(prefix="msd-cli-build-"))
        try:
            r = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_site.py"),
                 "--out", str(out)],
                capture_output=True, text=True,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn(f"Built 15 files into {out}", r.stdout)
            self.assertIn("Built", r.stdout)
            self.assertTrue((out / "index.html").exists())
        finally:
            shutil.rmtree(out, ignore_errors=True)


class TestRepoHygiene(unittest.TestCase):
    def test_license_exact_line(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)
        self.assertNotIn("Co-authored-by", text)

    def test_readme_credit(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", text)

    def test_no_secrets_anywhere_in_repo(self):
        scan_paths = [ROOT / "docs", SCRIPTS, ROOT / "tests"]
        for base in scan_paths:
            for p in base.rglob("*"):
                # text sources only; skip caches and binaries
                if p.is_file() and p.suffix in {".md", ".py"} and \
                        "__pycache__" not in p.parts:
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    for pat in pipeline.SECRET_PATTERNS:
                        self.assertIsNone(
                            pat.search(text),
                            f"secret pattern in {p}: {pat.pattern}",
                        )
        # also the repo root files
        for name in ("README.md", "LICENSE"):
            text = (ROOT / name).read_text(encoding="utf-8")
            for pat in pipeline.SECRET_PATTERNS:
                self.assertIsNone(pat.search(text), f"secret pattern in {name}")

    def test_expected_chapters_present(self):
        stems = {p.stem for p in pipeline.list_chapters(pipeline.DEFAULT_DOCS)}
        for stem in (
            "00-introduction", "01-temperature-and-top-p", "02-system-prompts",
            "03-context-windows", "04-max-tokens", "05-stop-sequences",
            "06-seeds", "07-when-defaults-are-fine", "08-experiment-recipes",
            "09-settings-betting-worksheet", "10-glossary", "11-cheat-sheet",
        ):
            self.assertIn(stem, stems)

    def test_companions_not_repeated(self):
        """The book references companions but does not re-teach them."""
        book = " ".join(p.read_text(encoding="utf-8")
                        for p in pipeline.list_chapters(pipeline.DEFAULT_DOCS))
        # mentions companion works
        self.assertIn("Prompt-Writing Handbook", book)
        self.assertIn("ai-model-picker", book)
        # but does not include full prompt-writing pattern card taxonomies etc.
        self.assertNotIn("Pattern Card", book)


if __name__ == "__main__":
    unittest.main()
