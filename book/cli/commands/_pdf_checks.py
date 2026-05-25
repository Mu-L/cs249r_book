"""PDF post-build verification used by `binder build pdf` and `binder check pdf`.

Scans rendered PDF text (via ``pdftotext``) for defects Quarto/LuaLaTeX can
emit without failing the render: unresolved cross-refs (``?@sec-foo``),
undefined LaTeX references (``Figure ??``), and leaked Python tracebacks.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

PDF_BY_VOLUME = {
    "vol1": "Machine-Learning-Systems-Vol1.pdf",
    "vol2": "Machine-Learning-Systems-Vol2.pdf",
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


@dataclass
class PdfCheckItem:
    check_id: str
    label: str
    passed: bool
    skipped: bool = False
    detail: str = ""


@dataclass
class PdfValidationResult:
    volume: str
    pdf_path: Path
    issues: list[PdfIssue] = field(default_factory=list)
    checks: list[PdfCheckItem] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues and all(c.passed or c.skipped for c in self.checks)


def default_pdf_path(quarto_dir: Path, volume: str) -> Path:
    return quarto_dir / "_build" / f"pdf-{volume}" / PDF_BY_VOLUME[volume]


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


def scan_build_log(log_path: Path | None) -> list[PdfIssue]:
    """Return Quarto cross-ref warnings from a render log, if provided."""
    if log_path is None or not log_path.exists():
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
    issues.extend(scan_build_log(log_path))
    return issues


def verify_volume_pdf(
    quarto_dir: Path,
    volume: str,
    *,
    log_path: Path | None = None,
) -> PdfValidationResult:
    """Verify the default built PDF for ``volume`` (``vol1`` or ``vol2``)."""
    pdf_path = default_pdf_path(quarto_dir, volume)
    issues = verify_pdf(pdf_path, log_path=log_path)

    checks = [
        PdfCheckItem("artifact", "PDF artifact exists", pdf_path.is_file()),
        PdfCheckItem(
            "pdftotext",
            "pdftotext available",
            shutil.which("pdftotext") is not None,
            skipped=shutil.which("pdftotext") is None,
        ),
        PdfCheckItem(
            "unresolved-crossref",
            "No ?@sec/fig/tbl/eq/lst literals in PDF text",
            not any(i.code == "unresolved-crossref" for i in issues),
        ),
        PdfCheckItem(
            "undefined-latex-ref",
            "No Figure/Table/Section ?? in PDF text",
            not any(i.code == "undefined-latex-ref" for i in issues),
        ),
        PdfCheckItem(
            "python-traceback",
            "No Python tracebacks in PDF text",
            not any(i.code == "python-traceback" for i in issues),
        ),
        PdfCheckItem(
            "quarto-crossref-warning",
            "No Quarto crossref warnings in build log",
            not any(i.code == "quarto-crossref-warning" for i in issues),
            skipped=log_path is None,
        ),
    ]

    return PdfValidationResult(
        volume=volume,
        pdf_path=pdf_path,
        issues=issues,
        checks=checks,
    )


def format_checklist(result: PdfValidationResult) -> str:
    """Human-readable checklist for console output."""
    vol_label = "Volume I" if result.volume == "vol1" else "Volume II"
    lines = [f"PDF validation ({vol_label}): {result.pdf_path.name}", ""]
    for item in result.checks:
        if item.skipped:
            mark = "ⓘ"
            status = "skipped"
        elif item.passed:
            mark = "✓"
            status = "pass"
        else:
            mark = "✗"
            status = "fail"
        detail = f" — {item.detail}" if item.detail else ""
        lines.append(f"  [{mark}] {item.label} ({status}){detail}")

    if result.issues:
        lines.extend(["", "Issues:"])
        for idx, issue in enumerate(result.issues, start=1):
            suffix = f" ({issue.count} occurrence(s))" if issue.count > 1 else ""
            lines.append(f"  {idx}. [{issue.code}] {issue.message}{suffix}")
    return "\n".join(lines)


def format_failure_report(label: str, pdf_path: Path, issues: list[PdfIssue]) -> str:
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
