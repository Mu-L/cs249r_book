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
     ``fmt_*`` helpers from ``mlsysim.fmt``:

       * ``_str``  — ``fmt(...)``, ``fmt_val(...)``, ``fmt_unit(...)``,
                     ``fmt_percent(...)``, ``fmt_sci(...)``, or
                     ``MarkdownStr(...)`` for non-numeric literals.
       * ``_math`` — ``fmt_math(...)`` or ``MarkdownStr(f"$...$")``.
       * ``_eq``   — same as ``_math``.
       * ``_frac`` — ``fmt_frac(...)`` only.

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

# Pattern: a numeric formatter whose first positional arg is itself an
# already-formatted value. The numeric formatters (fmt, fmt_percent, fmt_sci,
# fmt_val, fmt_unit) expect a Number/Quantity; passing a MarkdownStr or str
# from another helper fails at render time with ValueError.
#
# NOTE: fmt_math() and fmt_frac() are EXCLUDED from the outer set because
# they legitimately accept LaTeX strings (e.g., the canonical pattern
# `fmt_math(sci_latex(x))` embeds Unicode scientific notation in inline math).
#
# Caught shapes (all numeric outer):
#   fmt(fmt(x, precision=0), precision=0, prefix="$")           # MarkdownStr
#   fmt(sci_latex(P, precision=1), precision=0, prefix="$")     # plain str
#   fmt(MarkdownStr(label), precision=0)                        # MarkdownStr
#   fmt(gpt3_params_b_str, precision=0, suffix=" billion")      # MarkdownStr
DOUBLE_WRAP_CALL = re.compile(
    r"\b(?:fmt|fmt_percent|fmt_sci|fmt_val|fmt_unit)\(\s*(?:"
    r"fmt[a-z_]*\(|"          # fmt(fmt_*(...))
    r"sci_latex\(|"           # fmt(sci_latex(...))
    r"MarkdownStr\(|"         # fmt(MarkdownStr(...))
    r"[A-Za-z_]\w*_(?:str|math|eq|frac)\b"  # fmt(VAR_str/math/eq/frac, ...)
    r")"
)

# Pattern: small float literal assignment, e.g. `devops_fte = 0.1` or
# `edge_inf_cost = 0.001`. Captures (variable, literal value text). The
# audit function parses the literal as a float and only flags when
# `f"{val:.0f}" == "0"` (i.e., the precision-loss guard would actually
# fire at runtime).
SMALL_FLOAT_ASSIGN = re.compile(
    r"^\s*([A-Za-z_]\w*)\s*=\s*(0\.\d+(?:e-?\d+)?)\b"
)

# Pattern: fmt() call with precision=0 (only fmt itself; fmt_percent etc.
# have their own semantics). Captures the variable being formatted.
PRECISION_ZERO_CALL = re.compile(
    r"\bfmt\(\s*([A-Za-z_][\w.]*)\s*,[^)]*\bprecision\s*=\s*0\b"
)

# Pattern: fmt-family helper names used as calls in a cell body. Any of these
# requires a matching `from mlsysim.fmt import ...` line in the file.
FMT_FAMILY_USE = re.compile(
    r"\b(fmt|fmt_math|fmt_percent|fmt_val|fmt_unit|fmt_sci|fmt_frac|sci_latex|MarkdownStr|check)\s*\("
)

# Pattern: `from mlsysim.fmt import ...` block (possibly multi-line in parens
# — we collapse parens before matching, so this single-line form is enough).
FMT_IMPORT_LINE = re.compile(
    r"\bfrom\s+mlsysim\.fmt\s+import\s+([^#\n]+)"
)



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
                    f"canonical helper family (fmt/fmt_math/fmt_frac/MarkdownStr). "
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


def _audit_double_wrap(qmd_path: Path) -> list[Violation]:
    """Find fmt-family calls whose first positional arg is itself a fmt-family
    call or a _str/_math/_eq/_frac variable.

    Both shapes pass a MarkdownStr into fmt(), which fails at render time
    with ``ValueError: Unknown format code 'f' for object of type 'MarkdownStr'``.
    Seen in 2026-05 codemod artifacts.
    """
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
        m = DOUBLE_WRAP_CALL.search(line)
        if not m:
            continue
        out.append(
            Violation(
                file=rel,
                line=i,
                code="double_wrap_fmt",
                message=(
                    "Double-wrap detected: a fmt-family call receives a "
                    "MarkdownStr (either another fmt(...) call or a "
                    "_str/_math/_eq/_frac variable) as its first arg. The "
                    "outer fmt() will raise ValueError at render time. "
                    "Pass the underlying numeric value directly, and use "
                    "prefix=/suffix= to compose the final string."
                ),
                context=line.strip()[:160],
            )
        )
    return out


def _audit_precision_loss_on_small_floats(qmd_path: Path) -> list[Violation]:
    """Find fmt(VAR, precision=0, ...) calls where VAR is assigned a literal
    float that would round to "0" at precision=0.

    This combination always triggers fmt()'s runtime precision-loss guard
    because the rounded result is "0" for a non-zero input, which the
    guard rejects as silently hiding the value.

    Sound check: only flags when the parsed literal would actually round to
    "0" under Python's `f"{val:.0f}"` formatting (banker's rounding). Values
    like 0.85 or 1.8 do NOT fire the guard at runtime, so they are skipped
    here too.
    """
    out: list[Violation] = []
    lines = qmd_path.read_text(encoding="utf-8").splitlines()
    rel = str(qmd_path)
    in_cell = False
    cell_assignments: dict[str, tuple[int, float]] = {}
    for i, line in enumerate(lines, 1):
        if CELL_START.match(line):
            in_cell = True
            cell_assignments = {}
            continue
        if in_cell and CELL_END.match(line):
            in_cell = False
            continue
        if not in_cell:
            continue

        # Record literal-float assignments where the value would round to "0"
        # at precision=0 (the precondition for fmt()'s guard to fire).
        m_assign = SMALL_FLOAT_ASSIGN.match(line)
        if m_assign:
            varname = m_assign.group(1)
            try:
                value = float(m_assign.group(2))
            except ValueError:
                continue
            if value > 0 and f"{value:.0f}" == "0":
                cell_assignments[varname] = (i, value)
            continue

        # Check fmt(VAR, precision=0, ...) calls.
        m_call = PRECISION_ZERO_CALL.search(line)
        if not m_call:
            continue
        var = m_call.group(1).split(".")[-1]
        if var not in cell_assignments:
            continue
        assign_line, value = cell_assignments[var]
        out.append(
            Violation(
                file=rel,
                line=i,
                code="precision_zero_on_small_float",
                message=(
                    f"`{var}` was assigned `{value}` at line {assign_line} "
                    f"and is formatted with `precision=0`. Rounding "
                    f"`{value}` to integer produces '0', which trips "
                    f"fmt()'s precision-loss guard at render time. Fix "
                    f"options: (a) bump precision (e.g. `precision=3` for "
                    f"`{value}`), (b) set `allow_zero=True` if rounding to "
                    f"zero is intentional, or (c) use `MarkdownStr(f\"{{x}}\")` "
                    f"for value ranges that span orders of magnitude."
                ),
                context=line.strip()[:160],
            )
        )
    return out


def _audit_missing_fmt_imports(qmd_path: Path) -> list[Violation]:
    """Find files where a fmt-family helper is called in a cell before any
    cell imports it from mlsysim.fmt.

    Quarto cells share a Jupyter kernel namespace, so an import in an
    earlier cell satisfies later uses — but a use in cell N that imports
    only in cell N+1 fails at execution time. This check walks cells in
    document order, accumulating imported names, and flags any helper
    call whose name is not yet in the cumulative import set.
    """
    out: list[Violation] = []
    lines = qmd_path.read_text(encoding="utf-8").splitlines()
    rel = str(qmd_path)
    in_cell = False
    imported: set[str] = set()  # cumulative across cells in document order
    flagged: set[tuple[str, int]] = set()  # dedupe per (name, line)

    # Buffer to handle multi-line `from mlsysim.fmt import ( ... )`. When we
    # see the opening line, accumulate until the closing `)`.
    pending_import_buffer: list[str] = []
    in_paren_import = False

    for i, line in enumerate(lines, 1):
        if CELL_START.match(line):
            in_cell = True
            continue
        if in_cell and CELL_END.match(line):
            in_cell = False
            in_paren_import = False
            pending_import_buffer = []
            continue
        if not in_cell:
            continue

        # Multi-line paren import handling.
        if in_paren_import:
            pending_import_buffer.append(line)
            if ")" in line:
                blob = " ".join(pending_import_buffer)
                for name in re.findall(r"[A-Za-z_]\w*", blob):
                    if name not in ("as", "import", "from", "mlsysim", "fmt"):
                        imported.add(name)
                in_paren_import = False
                pending_import_buffer = []
            continue

        # Single-line `from mlsysim.fmt import ...` (with or without parens).
        m_imp = FMT_IMPORT_LINE.search(line)
        if m_imp:
            blob = m_imp.group(1)
            if "(" in blob and ")" not in blob:
                pending_import_buffer = [blob]
                in_paren_import = True
                continue
            for name in re.findall(r"[A-Za-z_]\w*", blob):
                if name != "as":
                    imported.add(name)
            continue

        # Skip comment lines.
        if line.strip().startswith("#"):
            continue

        # Check fmt-family uses.
        for m in FMT_FAMILY_USE.finditer(line):
            name = m.group(1)
            if name in imported:
                continue
            if (name, i) in flagged:
                continue
            flagged.add((name, i))
            out.append(
                Violation(
                    file=rel,
                    line=i,
                    code="missing_fmt_import",
                    message=(
                        f"`{name}(...)` is used here but `{name}` has not yet "
                        f"been imported from `mlsysim.fmt` in any prior cell. "
                        f"Quarto evaluates cells in document order; add "
                        f"`{name}` to this cell's import block (or an earlier "
                        f"cell's) so the call resolves at exec time."
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
            all_violations.extend(_audit_double_wrap(f))
            all_violations.extend(_audit_precision_loss_on_small_floats(f))
            all_violations.extend(_audit_missing_fmt_imports(f))
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
