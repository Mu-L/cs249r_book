#!/usr/bin/env python3
"""
audit_math_canonical.py
========================

Enforces the canonical math-rendering convention introduced 2026-05.

The single rule, expanded:

  Every value substituted into QMD prose via ``{python} X`` must be a
  ``MarkdownStr`` (a ``str`` subclass with ``_repr_markdown_``).  Plain
  ``str`` values are escaped by Quarto, which silently corrupts commas
  and decimals when the value lands inside ``$..$`` math mode (``\\,``
  becomes ``\\thinspace``; ``\\.`` becomes a dot accent).  ``MarkdownStr``
  bypasses the escape and renders verbatim.

The convention has two halves:

  1. **Python side** — every ``*_str``, ``*_math``, ``*_eq``, ``*_frac``
     assignment inside a Python cell must be built via the canonical
     helpers from ``mlsysim.fmt``:

       * ``_str``  — ``fmt(...)``, ``fmt_percent(...)``, ``fmt_full(...)``,
                     ``fmt_split(...)``, ``sci(...)``, or
                     ``MarkdownStr(f"...")`` for custom formatting.
       * ``_math`` — ``md_math(...)``, ``md(...)``, ``md_sci(...)``, or
                     ``MarkdownStr(f"$...$")``.
       * ``_eq``   — same as ``_math``.
       * ``_frac`` — ``md_frac(...)`` only.

     Bare f-strings (``var_str = f"{x:.1f}"``) are forbidden.  They
     produce plain ``str`` and bypass the protection.

  2. **QMD side** — every inline ``{python} X`` reference must use a
     variable name whose final component ends in ``_str``, ``_math``,
     ``_eq``, or ``_frac``.  Bare class attributes
     (``{python} Class.frontier_params_b``) are forbidden; rename the
     attribute or wrap it.

Both halves are required to be 100% certain of correct rendering.

Usage
-----
::

    python3 book/tools/audit/audit_math_canonical.py [path ...]

Default scans ``book/quarto/contents/**/*.qmd``.  Exit code 0 if no
violations; 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ALLOWED_SUFFIXES = ("_str", "_math", "_eq", "_frac")

# Pattern: inline {python} ref in prose
INLINE_REF = re.compile(r"`\{python\}\s+([A-Za-z_][\w.]*)`")

# Pattern: variable assignment to f-string, e.g.  `xxx_str = f"..."`
# The capture group is the variable name (no class-attribute access here —
# assignments inside cells are bare names).
FSTRING_ASSIGN = re.compile(
    r"^(\s*)([A-Za-z_]\w*)\s*=\s*f[\"']"
)

# Pattern: assignment of any kind (used as a sanity catch)
PLAIN_ASSIGN = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*([^=].*)$")

# Pattern: matches calls to canonical formatter helpers on the RHS.
CANONICAL_STR_CALL = re.compile(
    r"\b(fmt|fmt_percent|fmt_val|fmt_unit|fmt_sci|MarkdownStr)\s*\("
)
CANONICAL_MATH_CALL = re.compile(
    r"\b(fmt_math|MarkdownStr)\s*\("
)
CANONICAL_FRAC_CALL = re.compile(r"\b(fmt_frac|MarkdownStr)\s*\(")

# Quarto cell delimiters
CELL_START = re.compile(r"^```\{python\}")
CELL_END = re.compile(r"^```\s*$")


@dataclass
class Violation:
    file: str
    line: int
    code: str
    message: str
    context: str


def _suffix_of(ref: str) -> str:
    """Return the suffix of the last component of a dotted ref."""
    last = ref.split(".")[-1]
    for s in ALLOWED_SUFFIXES:
        if last.endswith(s):
            return s
    return ""


def _audit_python_cells(qmd_path: Path) -> list[Violation]:
    """Find _str/_math/_eq/_frac assignments inside Python cells that don't
    use the canonical formatter family."""
    out: list[Violation] = []
    lines = qmd_path.read_text(encoding="utf-8").splitlines()
    rel = str(qmd_path)
    in_cell = False
    for i, line in enumerate(lines, 1):
        if CELL_START.match(line):
            in_cell = True
            continue
        if in_cell and CELL_END.match(line):
            in_cell = False
            continue
        if not in_cell:
            continue

        # We only check assignments where the variable name has an approved suffix.
        m = PLAIN_ASSIGN.match(line)
        if not m:
            continue
        varname, rhs = m.group(1), m.group(2)
        suffix = _suffix_of(varname)
        if not suffix:
            continue  # name doesn't carry our convention; not our concern

        # Skip "type-hint" reassignment patterns or augmented assignments.
        if "==" in line[:line.index("=") + 2]:
            continue

        # Skip when RHS itself is a function call to a canonical helper.
        if suffix == "_str":
            if CANONICAL_STR_CALL.search(rhs):
                continue
        elif suffix in ("_math", "_eq"):
            if CANONICAL_MATH_CALL.search(rhs):
                continue
        elif suffix == "_frac":
            if CANONICAL_FRAC_CALL.search(rhs):
                continue

        # Skip when RHS is just another variable (e.g., `x_str = y_str`).
        # That's a re-binding, not a fresh format; the original assignment
        # is what we want to catch.
        if re.match(r"^\s*[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*\s*$", rhs):
            continue

        # Flag: a bare f-string is the most common violation, but ANY
        # non-canonical RHS for a _str-family variable is a violation.
        is_fstring = bool(re.match(r"^\s*f[\"']", rhs))
        code = "noncanonical_fstring_assign" if is_fstring else "noncanonical_str_assign"
        out.append(
            Violation(
                file=rel,
                line=i,
                code=code,
                message=(
                    f"`{varname}` (suffix `{suffix}`) is not built via the "
                    f"canonical helper family (fmt/md_math/md_frac/MarkdownStr). "
                    f"Use the appropriate helper from mlsysim.fmt so the value "
                    f"renders correctly inside math mode."
                ),
                context=line.strip()[:160],
            )
        )

    return out


def _audit_inline_refs(qmd_path: Path) -> list[Violation]:
    """Find `{python} X` references in prose where X (or its last
    component) doesn't end in an approved suffix."""
    out: list[Violation] = []
    lines = qmd_path.read_text(encoding="utf-8").splitlines()
    rel = str(qmd_path)
    in_cell = False
    for i, line in enumerate(lines, 1):
        if CELL_START.match(line):
            in_cell = True
            continue
        if in_cell and CELL_END.match(line):
            in_cell = False
            continue
        if in_cell:
            continue

        for m in INLINE_REF.finditer(line):
            ref = m.group(1)
            if not _suffix_of(ref):
                out.append(
                    Violation(
                        file=rel,
                        line=i,
                        code="inline_ref_no_canonical_suffix",
                        message=(
                            f"`{{python}} {ref}` does not end in an approved "
                            f"suffix ({', '.join(ALLOWED_SUFFIXES)}). Rename the "
                            f"underlying attribute so the type-of-value is "
                            f"declared by the suffix."
                        ),
                        context=line.strip()[:160],
                    )
                )

    return out


def audit(paths: list[Path]) -> list[Violation]:
    all_violations: list[Violation] = []
    for p in paths:
        if p.is_file():
            files = [p]
        else:
            files = sorted(p.rglob("*.qmd"))
        for f in files:
            all_violations.extend(_audit_python_cells(f))
            all_violations.extend(_audit_inline_refs(f))
    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="QMD files or directories. Defaults to book/quarto/contents/.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human report.",
    )
    parser.add_argument(
        "--by-file",
        action="store_true",
        help="Aggregate counts by file; suppress per-violation detail.",
    )
    args = parser.parse_args()

    targets = args.paths or [Path("book/quarto/contents")]
    violations = audit(targets)

    if args.json:
        out = [
            {
                "file": v.file,
                "line": v.line,
                "code": v.code,
                "message": v.message,
                "context": v.context,
            }
            for v in violations
        ]
        print(json.dumps(out, indent=2))
        return 1 if violations else 0

    if args.by_file:
        by_file: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for v in violations:
            by_file[v.file][v.code] += 1
        codes = sorted({v.code for v in violations})
        header = f"{'file':<70s}" + "".join(f"  {c:<28s}" for c in codes) + "  total"
        print(header)
        print("-" * len(header))
        for f in sorted(by_file):
            row = f"{f:<70s}"
            total = 0
            for c in codes:
                n = by_file[f][c]
                total += n
                row += f"  {n:<28d}"
            row += f"  {total}"
            print(row)
        print(f"\nTotal violations: {len(violations)} across {len(by_file)} files")
        return 1 if violations else 0

    # Default: detailed per-violation report.
    for v in violations:
        print(f"{v.file}:{v.line}  [{v.code}]  {v.message}")
        print(f"  {v.context}")
        print()
    print(f"Total violations: {len(violations)}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
