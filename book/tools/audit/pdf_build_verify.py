#!/usr/bin/env python3
"""Post-build PDF verification for full-volume Quarto PDF artifacts.

Scans rendered PDF text (via ``pdftotext``) for defects that Quarto/LuaLaTeX
can emit without failing the render: unresolved cross-refs (``?@sec-foo``),
undefined LaTeX references (``Figure ??``), and leaked Python tracebacks.

Usage (repo root)::

    python3 book/tools/audit/pdf_build_verify.py --vol1
    python3 book/tools/audit/pdf_build_verify.py --vol2
    python3 book/tools/audit/pdf_build_verify.py --pdf book/quarto/_build/pdf-vol1/Machine-Learning-Systems-Vol1.pdf
    python3 book/tools/audit/pdf_build_verify.py --vol1 --log /tmp/build_pdf_vol1.log

Exit 0 when clean; exit 1 and print a numbered issue list when not.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
BOOK_DIR = REPO_ROOT / "book" / "quarto"

PDF_BY_VOLUME = {
    "vol1": BOOK_DIR / "_build/pdf-vol1/Machine-Learning-Systems-Vol1.pdf",
    "vol2": BOOK_DIR / "_build/pdf-vol2/Machine-Learning-Systems-Vol2.pdf",
}

RESIDUAL_XREF = re.compile(r"\?@((?:sec|fig|tbl|eq|lst)-[\w.-]+)")
LATEX_UNDEF = re.compile(r"\b(?:Figure|Table|Section|Equation|Listing)\s+\?\?+")
PYTHON_LEAK = re.compile(
    r"(?:Traceback \(most recent call last\)|"
    r"NameError:|AttributeError:|ModuleNotFoundError:|Error rendering)",
    re.I,
)
QUARTO_XREF_WARN = re.compile(
    r"Unable to resolve crossref (@(?:sec|fig|tbl|eq|lst)-[\w.-]+)"
)


@dataclass(frozen=True)
class PdfIssue:
    code: str
    message: str
    count: int = 1


def _pdftotext(pdf_path: Path) -> str:
    proc = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"pdftotext failed on {pdf_path}: {(proc.stderr or proc.stdout or '').strip()}"
        )
    return proc.stdout or ""


def scan_pdf_text(pdf_path: Path) -> list[PdfIssue]:
    """Return issues found in extracted PDF text."""
    body = _pdftotext(pdf_path)
    issues: list[PdfIssue] = []

    xref_counts = Counter(m.group(1) for m in RESIDUAL_XREF.finditer(body))
    for slug, count in sorted(xref_counts.items()):
        issues.append(
            PdfIssue(
                code="unresolved-crossref",
                message=f"?@{slug} appears in PDF text (Quarto cross-ref did not resolve)",
                count=count,
            )
        )

    undef_counts = Counter(m.group(0) for m in LATEX_UNDEF.finditer(body))
    for text, count in sorted(undef_counts.items()):
        issues.append(
            PdfIssue(
                code="undefined-latex-ref",
                message=f'"{text}" appears in PDF text (LaTeX reference undefined)',
                count=count,
            )
        )

    if PYTHON_LEAK.search(body):
        issues.append(
            PdfIssue(
                code="python-traceback",
                message="Python error/traceback text leaked into PDF output",
            )
        )

    return issues


def scan_build_log(log_path: Path) -> list[PdfIssue]:
    """Return Quarto cross-ref warnings from a render log, if provided."""
    if not log_path.exists():
        return []
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [PdfIssue(code="log-read-error", message=str(exc))]

    issues: list[PdfIssue] = []
    warn_counts = Counter(m.group(1) for m in QUARTO_XREF_WARN.finditer(text))
    for ref, count in sorted(warn_counts.items()):
        issues.append(
            PdfIssue(
                code="quarto-crossref-warning",
                message=f"{ref} flagged in build log (Unable to resolve crossref)",
                count=count,
            )
        )
    return issues


def verify_pdf(
    pdf_path: Path,
    *,
    log_path: Path | None = None,
    label: str | None = None,
) -> list[PdfIssue]:
    """Scan ``pdf_path`` (and optional ``log_path``) and return all issues."""
    if not pdf_path.is_file():
        return [PdfIssue(code="missing-pdf", message=f"PDF not found: {pdf_path}")]

    if shutil.which("pdftotext") is None:
        return [
            PdfIssue(
                code="pdftotext-missing",
                message="pdftotext not installed; install poppler (e.g. brew install poppler)",
            )
        ]

    issues = scan_pdf_text(pdf_path)
    if log_path is not None:
        issues.extend(scan_build_log(log_path))
    return issues


def _format_report(label: str, pdf_path: Path, issues: list[PdfIssue]) -> str:
    lines = [
        f"PDF validation failed for {label}:",
        f"  artifact: {pdf_path}",
        "",
    ]
    for idx, issue in enumerate(issues, start=1):
        suffix = f" ({issue.count} occurrence(s))" if issue.count > 1 else ""
        lines.append(f"  {idx}. [{issue.code}] {issue.message}{suffix}")
    lines.extend(
        [
            "",
            "Fix the source QMD (missing {#tbl-...} label, broken @ref, blank lines",
            "inside pipe tables, etc.) and rebuild. Bypass with --skip-validate only",
            "when you intentionally need a broken artifact.",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify a built volume PDF for render defects.")
    parser.add_argument("--vol1", action="store_true", help="Verify Volume I default PDF path")
    parser.add_argument("--vol2", action="store_true", help="Verify Volume II default PDF path")
    parser.add_argument("--pdf", type=Path, help="Explicit PDF path to verify")
    parser.add_argument("--log", type=Path, help="Optional Quarto render log to scan for warnings")
    parser.add_argument("--quiet", action="store_true", help="Only print output when issues are found")
    args = parser.parse_args(argv)

    volumes: list[tuple[str, Path]] = []
    if args.pdf:
        volumes.append(("custom PDF", args.pdf.resolve()))
    elif args.vol1:
        volumes.append(("Volume I", PDF_BY_VOLUME["vol1"]))
    elif args.vol2:
        volumes.append(("Volume II", PDF_BY_VOLUME["vol2"]))
    else:
        parser.error("specify --vol1, --vol2, or --pdf")

    overall_ok = True
    for label, pdf_path in volumes:
        issues = verify_pdf(pdf_path, log_path=args.log, label=label)
        if issues:
            overall_ok = False
            print(_format_report(label, pdf_path, issues))
            if len(volumes) > 1:
                print()
        elif not args.quiet:
            print(f"PDF validation passed for {label}: {pdf_path}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
