#!/usr/bin/env python3
"""Flag redundant unit/currency tokens after ``{python} *_str`` prose refs.

Policy
------
1. **Prose suffix** — a ``{python} Class.field_str`` ref must not be followed by
   a hand-typed unit (``ms``, ``mW``, ``GB``, ``kWh``, ``percent``, ``$``, etc.).
   The ``fmt(..., suffix=...)`` export should carry the unit.

2. **Duplicate suffix** — when the cell already sets ``suffix=`` on the matching
   ``*_str`` export, prose must not repeat that same unit token.

Lines with ``<!-- lego-ok: ... -->`` are skipped.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTENTS = REPO_ROOT / "book" / "quarto" / "contents"

CELL_START = re.compile(r"^```\{python\}")
CELL_END = re.compile(r"^```\s*$")
FENCE_START = re.compile(r"^```")
CLASS = re.compile(r"^class\s+(\w+)", re.M)
FMT_SUFFIX = re.compile(
    r"(\w+_str)\s*=\s*fmt(?:_int|_percent|_unit|_val)?\([^)]*suffix\s*=\s*['\"]([^'\"]+)['\"]",
    re.M,
)

# Unit/currency tokens immediately after a closing backtick on a _str ref.
PROSE_UNIT_AFTER_REF = re.compile(
    r"`\{python\}\s+([A-Za-z_][\w.]*_str)`\s*"
    r"(ms|mW|MW|GW|kW|Wh|kWh|MWh|GWh|"
    r"GB|MB|KB|GiB|TiB|TB|"
    r"seconds?|secs?|minutes?|mins?|hours?|hrs?|weeks?|months?|years?|"
    r"percent|GPUs?|QPS|FLOPS|TFLOP/?s|PFLOP/?s|"
    r"flights?|tokens?|images?|nodes?|servers?|"
    r"USD|\$|%|×|x\b)",
    re.I,
)


def _suffix_map_from_cells(lines: list[str]) -> dict[str, str]:
    """Map ``Class.export_str`` → normalized suffix text from fmt(..., suffix=)."""
    out: dict[str, str] = {}
    in_cell = False
    buf: list[str] = []
    for line in lines:
        if CELL_START.match(line):
            in_cell = True
            buf = []
            continue
        if in_cell and CELL_END.match(line):
            in_cell = False
            code = "\n".join(buf)
            cls_m = CLASS.search(code)
            if not cls_m:
                continue
            cls = cls_m.group(1)
            for attr, suffix in FMT_SUFFIX.findall(code):
                out[f"{cls}.{attr}"] = suffix.strip().lower()
            continue
        if in_cell:
            buf.append(line)
    return out


def _normalize_unit(token: str) -> str:
    t = token.strip().lower()
    if t in {"$", "usd"}:
        return "$"
    if t in {"%", "percent"}:
        return "%"
    if t in {"x", "×"}:
        return "x"
    return t


def _line_hits(line: str, suffix_map: dict[str, str]) -> list[str]:
    if "<!-- lego-ok" in line:
        return []
    hits: list[str] = []
    for m in PROSE_UNIT_AFTER_REF.finditer(line):
        ref = m.group(1)
        unit_token = m.group(2)
        after = line[m.end() :].lstrip()
        if unit_token == "$" and after.startswith("\\"):
            continue
        norm = _normalize_unit(unit_token)
        hits.append(f"prose unit '{unit_token}' after {ref.split('.')[-1]}")
        cell_suffix = suffix_map.get(ref, "")
        if cell_suffix:
            cell_norm = cell_suffix.lstrip("~").strip().lower()
            if cell_norm == norm or cell_norm.endswith(norm) or norm in cell_norm:
                hits.append(f"duplicate unit (fmt suffix={cell_suffix!r} on {ref})")
    return hits


def check_file(path: Path) -> list[tuple[int, str, list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    suffix_map = _suffix_map_from_cells(lines)
    issues: list[tuple[int, str, list[str]]] = []

    in_python = False
    in_fence = False
    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if CELL_START.match(line):
            in_python = True
            continue
        if in_python:
            if CELL_END.match(line):
                in_python = False
            continue
        if FENCE_START.match(line) and not line.startswith("```{python}"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        hits = _line_hits(line, suffix_map)
        if hits:
            issues.append((lineno, line.strip()[:120], hits))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="QMD files (default: all contents)")
    args = parser.parse_args()
    if args.paths:
        expanded: list[Path] = []
        for path in args.paths:
            p = path if path.is_absolute() else REPO_ROOT / path
            if p.is_dir():
                expanded.extend(sorted(p.rglob("*.qmd")))
            elif p.suffix == ".qmd":
                expanded.append(p)
        paths = expanded
    else:
        paths = sorted(CONTENTS.rglob("*.qmd"))
    failures = 0
    total = 0
    for path in paths:
        p = path if path.is_absolute() else REPO_ROOT / path
        if not p.exists() or p.suffix != ".qmd":
            continue
        issues = check_file(p)
        total += 1
        if not issues:
            continue
        failures += 1
        print(f"\n{p.relative_to(REPO_ROOT)}")
        for lineno, snippet, labels in issues:
            uniq = ", ".join(dict.fromkeys(labels))
            print(f"  L{lineno}: {uniq}")
            print(f"    {snippet}")
    if failures:
        print(f"\n{failures} file(s) with LEGO prose unit violations")
        return 1
    print(f"OK LEGO prose units ({total} QMD files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
