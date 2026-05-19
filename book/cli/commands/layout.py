"""
``binder layout`` — PDF page-layout diagnostics.

Subcommands:
    check    — Scan a built PDF for pages with excessive bottom whitespace
               in the main body column, and guess the likely cause (the
               block at the top of the next page that probably forced the
               break).

The check is read-only: it inspects the PDF, prints a report, and exits.
It does not modify source or PDF. Fixes happen in the QMD source by the
author, optionally guided by a /layout-fix skill.
"""

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

console = Console()


# --- geometry constants ---------------------------------------------------
# These are heuristic bands for the book's Tufte-style layout (main column
# left, margin notes right). They are intentionally generous so the tool
# works without per-volume calibration; tune later if needed.

HEADER_FRAC = 0.06   # top 6% of page height treated as running header
FOOTER_FRAC = 0.06   # bottom 6% treated as running footer / page number
MAIN_COL_RIGHT_FRAC = 0.55  # main column ends ~55% across the page
# Anything with x0 above this fraction is considered margin-note / sidebar.


@dataclass
class PageReport:
    sheet: int                    # 1-indexed PDF sheet number
    label: str                    # printed page number ("59", "iii", etc.)
    chapter: str                  # enclosing top-level outline title
    whitespace_pts: float         # vertical gap, in PDF points
    whitespace_frac: float        # gap / usable_text_height
    body_bottom_y: float          # y of last char in main column
    usable_bottom_y: float        # y of footer band top
    cause: str                    # best-effort guess for next-page culprit
    detail: str = ""              # caption / heading / title of the next-page element
    size_hint: str = ""           # element size: "10 rows", "380pt tall", etc.
    fix_hint: str = ""            # one-word suggested fix
    is_frontmatter: bool = False  # roman-numbered page (likely intentional gap)


class LayoutCommand:
    """Diagnose PDF page-break whitespace issues."""

    def __init__(self, config_manager, chapter_discovery):
        self.config_manager = config_manager
        self.chapter_discovery = chapter_discovery

    # ------------------------------------------------------------------
    # entry
    # ------------------------------------------------------------------

    def run(self, args: List[str]) -> bool:
        parser = argparse.ArgumentParser(
            prog="binder layout",
            description="PDF page-layout diagnostics.",
            add_help=True,
        )
        sub = parser.add_subparsers(dest="subcommand")

        check = sub.add_parser("check", help="Scan PDF for whitespace gaps.")
        check.add_argument("pdf", help="Path to PDF file to scan.")
        check.add_argument(
            "--threshold",
            type=float,
            default=0.25,
            help="Flag pages where bottom whitespace exceeds this "
                 "fraction of usable text height (default 0.25).",
        )
        check.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Only scan the first N pages (0 = all). For quick iteration.",
        )
        check.add_argument(
            "--only",
            type=str,
            default="",
            help="Comma-separated culprit classes to keep "
                 "(table,figure,heading,paragraph,callout/box,unknown,"
                 "end-of-document). Default: all.",
        )
        check.add_argument(
            "--skip-frontmatter",
            action="store_true",
            help="Hide pages with roman-numeral labels (frontmatter / "
                 "intentional whitespace).",
        )
        check.add_argument(
            "--csv",
            action="store_true",
            help="Emit one CSV row per flagged page to stdout instead of "
                 "the rich report. Columns: chapter,sheet,label,gap_pct,"
                 "pts,culprit,detail,size_hint,fix_hint,is_frontmatter.",
        )

        if not args:
            parser.print_help()
            return False

        opts = parser.parse_args(args)
        if opts.subcommand == "check":
            only = (
                set(s.strip() for s in opts.only.split(",") if s.strip())
                if opts.only
                else set()
            )
            return self._check(
                Path(opts.pdf),
                opts.threshold,
                opts.limit,
                only=only,
                skip_frontmatter=opts.skip_frontmatter,
                csv=opts.csv,
            )

        parser.print_help()
        return False

    # ------------------------------------------------------------------
    # check
    # ------------------------------------------------------------------

    def _check(
        self,
        pdf_path: Path,
        threshold: float,
        limit: int,
        only: Optional[set] = None,
        skip_frontmatter: bool = False,
        csv: bool = False,
    ) -> bool:
        if not pdf_path.exists():
            console.print(f"[red]PDF not found:[/red] {pdf_path}")
            return False

        try:
            import pdfplumber  # type: ignore
        except ImportError:
            console.print(
                "[red]pdfplumber not installed.[/red] "
                "Run: [cyan]pip install pdfplumber[/cyan]"
            )
            return False

        console.print(
            f"[bold blue]Scanning[/bold blue] {pdf_path.name} "
            f"[dim](threshold={int(threshold*100)}%, "
            f"main col <{int(MAIN_COL_RIGHT_FRAC*100)}% page width)[/dim]"
        )

        chapter_starts, labels = self._load_chapter_map(pdf_path)

        flagged: List[PageReport] = []
        scanned = 0

        with pdfplumber.open(str(pdf_path)) as pdf:
            n_pages = len(pdf.pages)
            n_scan = n_pages if limit <= 0 else min(limit, n_pages)

            for i in range(n_scan):
                page = pdf.pages[i]
                next_page = pdf.pages[i + 1] if i + 1 < n_pages else None
                sheet = i + 1
                label = labels[i] if i < len(labels) else str(sheet)
                chapter = self._chapter_for(sheet, chapter_starts)
                report = self._scan_page(page, next_page, sheet, label, chapter)
                scanned += 1
                if report and report.whitespace_frac >= threshold:
                    flagged.append(report)

        # Apply filters AFTER collection so the unfiltered counts are
        # available for the summary line.
        total_flagged = len(flagged)
        if skip_frontmatter:
            flagged = [r for r in flagged if not r.is_frontmatter]
        if only:
            flagged = [r for r in flagged if r.cause in only]

        if csv:
            self._render_csv(flagged)
        else:
            self._render(
                flagged,
                scanned,
                threshold,
                pdf_path,
                total_flagged=total_flagged,
            )
        return True

    # ------------------------------------------------------------------
    # CSV output
    # ------------------------------------------------------------------

    def _render_csv(self, flagged: List[PageReport]) -> None:
        import csv as _csv
        import sys
        writer = _csv.writer(sys.stdout)
        writer.writerow([
            "chapter", "sheet", "label", "gap_pct", "pts",
            "culprit", "detail", "size_hint", "fix_hint", "is_frontmatter",
        ])
        for r in flagged:
            writer.writerow([
                r.chapter,
                r.sheet,
                r.label,
                int(r.whitespace_frac * 100),
                int(r.whitespace_pts),
                r.cause,
                r.detail,
                r.size_hint,
                r.fix_hint,
                int(r.is_frontmatter),
            ])

    # ------------------------------------------------------------------
    # outline + page labels
    # ------------------------------------------------------------------

    def _load_chapter_map(
        self, pdf_path: Path
    ) -> Tuple[List[Tuple[int, str]], List[str]]:
        """Return (chapter_starts, labels).

        chapter_starts: [(start_sheet_1indexed, title)] for top-level outline
            entries only. Sorted ascending by start sheet.
        labels: list of printed page labels indexed by 0-based page index,
            same length as pdf.pages. Falls back to the 1-based sheet number
            when PageLabels are missing.
        """
        try:
            import pypdf  # type: ignore
        except ImportError:
            return [], []

        try:
            r = pypdf.PdfReader(str(pdf_path))
        except Exception:
            return [], []

        n = len(r.pages)

        # Printed page labels (PDF /PageLabels). Pad to len(pages).
        try:
            labels = list(r.page_labels or [])
        except Exception:
            labels = []
        if len(labels) < n:
            labels.extend(str(i + 1) for i in range(len(labels), n))

        # Top-level outline entries only — these are chapters in this book.
        chapter_starts: List[Tuple[int, str]] = []
        try:
            outline = r.outline or []
        except Exception:
            outline = []
        for item in outline:
            if isinstance(item, list):
                continue  # skip nested sub-entries
            try:
                page0 = r.get_destination_page_number(item)
                title = getattr(item, "title", None) or "(untitled)"
                chapter_starts.append((page0 + 1, title))
            except Exception:
                continue
        chapter_starts.sort(key=lambda x: x[0])
        return chapter_starts, labels

    def _chapter_for(
        self, sheet_1indexed: int, chapter_starts: List[Tuple[int, str]]
    ) -> str:
        """Return the title of the chapter whose range contains this sheet."""
        if not chapter_starts:
            return "(no outline)"
        current = "Frontmatter"
        for start, title in chapter_starts:
            if start <= sheet_1indexed:
                current = title
            else:
                break
        return current

    # ------------------------------------------------------------------
    # per-page analysis
    # ------------------------------------------------------------------

    def _scan_page(
        self, page, next_page, sheet: int, label: str, chapter: str
    ) -> Optional[PageReport]:
        chars = page.chars
        if not chars:
            return None

        page_h = page.height
        page_w = page.width

        header_y = page_h * HEADER_FRAC          # top band
        footer_y = page_h * (1.0 - FOOTER_FRAC)  # bottom band
        main_col_max_x = page_w * MAIN_COL_RIGHT_FRAC

        # Main-column chars only: exclude margin notes (right side) and
        # header/footer bands.
        body_chars = [
            c for c in chars
            if c["x0"] < main_col_max_x
            and c["top"] > header_y
            and c["bottom"] < footer_y
        ]
        if not body_chars:
            return None

        body_bottom = max(c["bottom"] for c in body_chars)
        body_top = min(c["top"] for c in body_chars)

        usable_height = footer_y - header_y
        whitespace_pts = footer_y - body_bottom
        # Normalize against usable column height, not full page.
        whitespace_frac = whitespace_pts / usable_height if usable_height > 0 else 0.0

        if next_page is None:
            cause, detail, size_hint = "end-of-document", "", ""
        else:
            cause, detail, size_hint = self._guess_cause(next_page)

        return PageReport(
            sheet=sheet,
            label=label,
            chapter=chapter,
            whitespace_pts=whitespace_pts,
            whitespace_frac=whitespace_frac,
            body_bottom_y=body_bottom,
            usable_bottom_y=footer_y,
            cause=cause,
            detail=detail,
            size_hint=size_hint,
            fix_hint=self._fix_hint(cause, size_hint),
            is_frontmatter=self._is_frontmatter_label(label),
        )

    @staticmethod
    def _is_frontmatter_label(label: str) -> bool:
        """Detect roman-numeral printed page labels (frontmatter)."""
        if not label:
            return False
        s = label.strip().lower()
        return bool(s) and all(c in "ivxlcdm" for c in s)

    @staticmethod
    def _fix_hint(cause: str, size_hint: str) -> str:
        """One-word suggested fix per culprit class."""
        if cause == "table":
            # Extract row count from size_hint if present.
            rows = 0
            if "rows" in size_hint:
                try:
                    rows = int(size_hint.split()[0])
                except (ValueError, IndexError):
                    rows = 0
            if rows >= 6:
                return "longtable?"
            if rows > 0:
                return "shrink/keep"
            return "longtable?"
        if cause == "figure":
            return "fig-pos?"
        if cause == "heading":
            return "relax-penalty?"
        if cause == "paragraph":
            return "rewrite"
        if cause == "callout/box":
            return "audit"
        if cause == "end-of-document":
            return "ignore"
        return "manual"

    # ------------------------------------------------------------------
    # cause guess: look at top of next page
    # ------------------------------------------------------------------

    def _guess_cause(self, page) -> Tuple[str, str, str]:
        """Best-effort guess at the block that probably forced the break.

        Inspects the top region of the next page (after the header band)
        and returns (cause, detail, size_hint):
            cause      — one of: table, figure, callout/box, heading,
                         paragraph, unknown
            detail     — caption / heading / title text (truncated)
            size_hint  — "10 rows", "380pt tall", etc., where extractable
        """
        if page is None:
            return ("end-of-document", "", "")

        page_h = page.height
        page_w = page.width
        header_y = page_h * HEADER_FRAC
        # "Top of next page" = first ~40% of usable height after header.
        zone_bottom = header_y + (page_h - header_y) * 0.40

        chars = [c for c in page.chars if header_y < c["top"] < zone_bottom]
        if not chars:
            return ("unknown", "", "")

        # 1. Figure? — any image object whose top is in the zone.
        images = getattr(page, "images", []) or []
        for im in images:
            if header_y < im.get("top", 0) < zone_bottom:
                im_h = im.get("height", 0) or (
                    im.get("bottom", 0) - im.get("top", 0)
                )
                size_hint = f"{int(im_h)}pt tall" if im_h else ""
                detail = self._extract_caption(page, prefix_pattern="Figure")
                return ("figure", detail, size_hint)

        # 2. Table? — many horizontal lines (rules) clustered in the zone.
        #    Tables in this book are typed with booktabs-style rules.
        lines = getattr(page, "lines", []) or []
        rects = getattr(page, "rects", []) or []
        horiz_lines_full = [
            ln for ln in lines
            if header_y < ln.get("top", 0) < zone_bottom
            and abs(ln.get("height", 0)) < 1.0
        ]
        # booktabs tables typically have >= 3 horizontal rules.
        if len(horiz_lines_full) >= 3:
            # Row estimate: count distinct text-line y-positions BETWEEN the
            # topmost and bottommost rule of the table. Booktabs uses only
            # 3 rules (top / mid / bottom) regardless of row count, so we
            # have to count baselines, not rules.
            rule_ys = sorted(ln.get("top", 0) for ln in horiz_lines_full)
            top_rule_y = rule_ys[0]
            bot_rule_y = rule_ys[-1]
            # Allow the table to extend somewhat below the zone (tables
            # often run further down the page); scan all chars within the
            # rule band.
            table_chars = [
                c for c in page.chars
                if top_rule_y - 2 <= c["top"] <= bot_rule_y + 2
            ]
            # Distinct baselines (y rounded to nearest pt).
            ys = {round(c["top"], 0) for c in table_chars}
            rows_est = max(0, len(ys) - 1)  # -1 for header row
            size_hint = f"{rows_est} rows" if rows_est else ""
            detail = self._extract_caption(page, prefix_pattern="Table")
            return ("table", detail, size_hint)

        # 3. Callout / box? — a large filled rectangle in the zone.
        #    Heuristic: a rect taller than ~30pt and at least 60% of main
        #    column width counts as a box.
        for r in rects:
            top = r.get("top", 0)
            if not (header_y < top < zone_bottom):
                continue
            height = r.get("height", 0) or (r.get("bottom", 0) - top)
            width = r.get("width", 0) or (r.get("x1", 0) - r.get("x0", 0))
            if height >= 30 and width >= page_w * 0.45:
                # First line of text inside the box = callout title.
                title = self._first_line_text(chars, top_y_min=top)
                return ("callout/box", title, "")

        # 4. Heading? — first line's font size is notably above median.
        sizes = [round(c.get("size", 0), 1) for c in chars if c.get("size")]
        if sizes:
            sorted_sizes = sorted(sizes)
            median = sorted_sizes[len(sorted_sizes) // 2]
            # First line: chars sharing the topmost band (within 2pt).
            top_y = min(c["top"] for c in chars)
            first_line_sizes = [
                round(c.get("size", 0), 1)
                for c in chars
                if abs(c["top"] - top_y) < 2.0 and c.get("size")
            ]
            if first_line_sizes:
                first_max = max(first_line_sizes)
                if first_max >= median + 1.5:
                    heading = self._first_line_text(chars)
                    return ("heading", heading, "")

        # 5. Paragraph fallback — return the first ~60 chars so it's
        # easy to grep back to the source.
        first_text = self._first_line_text(chars)
        return ("paragraph", first_text, "")

    # ------------------------------------------------------------------
    # text extraction helpers
    # ------------------------------------------------------------------

    def _first_line_text(self, chars, top_y_min: float = 0.0) -> str:
        """Reconstruct the topmost text line from a list of page chars."""
        if not chars:
            return ""
        candidates = [c for c in chars if c["top"] >= top_y_min]
        if not candidates:
            return ""
        top_y = min(c["top"] for c in candidates)
        line_chars = [c for c in candidates if abs(c["top"] - top_y) < 2.0]
        line_chars.sort(key=lambda c: c["x0"])
        text = "".join(c.get("text", "") for c in line_chars).strip()
        return self._truncate(text, 70)

    def _extract_caption(self, page, prefix_pattern: str) -> str:
        """Find a 'Table X.Y:' or 'Figure X.Y:' caption on a page.

        Captions in this book are rendered by Quarto as:
            Table N.M: Some caption text
        We extract the line beginning with the given prefix and return
        the caption text (truncated). Returns "" if not found.
        """
        try:
            text = page.extract_text() or ""
        except Exception:
            return ""
        for raw in text.splitlines():
            line = raw.strip()
            if not line.startswith(prefix_pattern):
                continue
            # Strip "Table N.M:" / "Figure N.M:" prefix. Allow up to 30
            # chars because pdfplumber sometimes drops spaces, producing
            # e.g. "Table5.3summarizes:" instead of "Table 5.3 summarizes:".
            colon = line.find(":")
            if colon != -1 and colon < 30:
                line = line[colon + 1:].strip()
            return self._truncate(line, 70)
        return ""

    @staticmethod
    def _truncate(s: str, n: int) -> str:
        s = s.replace("­", "").strip()  # strip soft hyphens
        if len(s) <= n:
            return s
        return s[: n - 1].rstrip() + "…"

    # ------------------------------------------------------------------
    # rendering
    # ------------------------------------------------------------------

    def _render(
        self,
        flagged: List[PageReport],
        scanned: int,
        threshold: float,
        pdf_path: Path,
        total_flagged: int = 0,
    ) -> None:
        if not flagged:
            extra = ""
            if total_flagged and total_flagged != len(flagged):
                extra = (
                    f" (filtered from {total_flagged} unfiltered flags)"
                )
            console.print(
                Panel(
                    f"No pages exceeded {int(threshold*100)}% bottom whitespace "
                    f"across {scanned} pages{extra}.",
                    title="✅ Layout check clean",
                    border_style="green",
                )
            )
            return

        # Group by chapter; sort each group DESCENDING by sheet so the
        # natural read order matches the fix order (back-to-front within
        # a chapter, so earlier fixes don't shift later diagnoses).
        by_chapter: Dict[str, List[PageReport]] = defaultdict(list)
        for r in flagged:
            by_chapter[r.chapter].append(r)
        # Chapter order: by first-flagged sheet ascending, so the report
        # reads forward through the book even though each chapter is
        # internally descending.
        chapter_order = sorted(
            by_chapter.keys(),
            key=lambda c: min(r.sheet for r in by_chapter[c]),
        )

        cause_counts = Counter(r.cause for r in flagged)
        summary = ", ".join(f"{n}× {c}" for c, n in cause_counts.most_common())

        console.print()
        filter_note = ""
        if total_flagged and total_flagged != len(flagged):
            filter_note = (
                f" [dim](filtered from {total_flagged} total)[/dim]"
            )
        console.print(
            f"[bold yellow]⚠ {len(flagged)}/{scanned} pages flagged[/bold yellow]"
            f"{filter_note} "
            f"[dim](≥{int(threshold*100)}% bottom whitespace · "
            f"fix order: back-to-front within chapter)[/dim]"
        )
        console.print(f"[dim]by culprit: {summary}[/dim]")
        fix_counts = Counter(r.fix_hint for r in flagged)
        fix_summary = ", ".join(
            f"{n}× {h}" for h, n in fix_counts.most_common()
        )
        console.print(f"[dim]by fix hint: {fix_summary}[/dim]")

        for chapter in chapter_order:
            rows = sorted(by_chapter[chapter], key=lambda x: -x.sheet)
            console.print()
            console.print(
                Rule(
                    f"[bold magenta]{chapter}[/bold magenta] "
                    f"[dim]({len(rows)} page{'s' if len(rows) != 1 else ''})[/dim]",
                    style="magenta",
                    align="left",
                )
            )

            table = Table(show_header=True, header_style="bold", box=None, pad_edge=False)
            table.add_column("p.", justify="right", style="cyan", width=5)
            table.add_column("sheet", justify="right", style="dim", width=6)
            table.add_column("gap%", justify="right", style="yellow", width=6)
            table.add_column("pts", justify="right", style="dim", width=5)
            table.add_column("culprit", style="white", width=11)
            table.add_column("size", style="dim", width=10)
            table.add_column("detail (next-page caption / heading / first-line)", style="white")
            table.add_column("hint", style="green", width=14)

            for r in rows:
                label = r.label
                if r.is_frontmatter:
                    label = f"{label}*"
                table.add_row(
                    label,
                    str(r.sheet),
                    f"{int(r.whitespace_frac * 100)}%",
                    f"{r.whitespace_pts:.0f}",
                    r.cause,
                    r.size_hint,
                    r.detail,
                    r.fix_hint,
                )
            console.print(table)

        console.print()
        console.print(
            f"[dim]PDF:[/dim] {pdf_path}\n"
            f"[dim]Within each chapter, fix the LAST flagged page first — "
            f"front-to-back fixes shift downstream pages and invalidate "
            f"later diagnoses.[/dim]\n"
            f"[dim]Asterisk (*) after p. = roman-numeral label "
            f"(frontmatter/backmatter — usually intentional). "
            f"Use --skip-frontmatter to hide.[/dim]"
        )
