#!/usr/bin/env python3
"""Flag hardcoded numeric literals in LEGO walkthrough prose.

When a line references ``{python} Class.field_str``, intermediate calculation
operands and results should also come from the cell—not be typed as literals
(``1,287,000 kWh``, ``times 429 g/kWh``, ``/ 1000``).
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
CALLOUT_START = re.compile(r"^:::+\s+\{#")
CALLOUT_END = re.compile(r"^:::\s*$")
PY_REF = re.compile(r"\{python\}\s+[A-Za-z_][A-Za-z0-9_.]*")

WALKTHROUGH_MARK = re.compile(
    r"^\*\*(?:Step|Math|Operational|Embodied|Comparison|Problem|Solution|Result|Parameters)\b",
    re.I,
)
WALKTHROUGH_CALC = re.compile(
    r"(?:=|≈|\\approx).*\{python\}|\{python\}.*(?:=|≈|\\approx|\s/\s|\s×\s|\stimes\s|\$\\times\$|\$times\$)"
)

SCI_NOTATION = re.compile(r"10\s*\^|10\^\{")
TENSOR_DIM = re.compile(r"\d+\s*[×x]\s*\d+")
SMALL_FACTOR = re.compile(r"(?:times|×|\\times)\s*[1-9]\b")

LITERAL_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\d{1,3}(?:,\d{3})+"), "comma-formatted number"),
    (
        re.compile(
            r"\b\d+(?:\.\d+)?\s*(?:kWh|kg(?:\s*CO[₂2~]?)?|MW|MWh|Wh|GB|MB|KB|"
            r"g/kWh|metric tons|hours|seconds|GPUs?|months|years|flights|TB/s|QPS)\b",
            re.I,
        ),
        "unit-suffixed quantity literal",
    ),
    (
        re.compile(r"(?:times|×|\\times)\s*\d{2,}(?:\.\d+)?"),
        "numeric multiplier (2+ digits)",
    ),
    (
        re.compile(r"/\s*\d{1,3}(?:,\d{3})+(?:\.\d+)?|\s/\s*\d{4,}(?:\.\d+)?"),
        "division by numeric literal",
    ),
)


def _strip_allowed_fragments(line: str) -> str:
    out = line
    while TENSOR_DIM.search(out):
        out = TENSOR_DIM.sub("", out)
    out = SCI_NOTATION.sub("", out)
    out = SMALL_FACTOR.sub("", out)
    out = PY_REF.sub("", out)
    out = re.sub(r"#(?:sec|tbl|fig|eq|lst)-[^\s`]+", "", out)
    out = re.sub(r"@[A-Za-z0-9_-]+", "", out)
    # Drop inline math blocks — often carry fixed scenario dimensions.
    out = re.sub(r"\$[^$]+\$", "", out)
    return out


def _is_walkthrough_line(line: str, in_callout: bool) -> bool:
    stripped = line.lstrip()
    if "fig-cap=" in line or stripped.startswith("|"):
        return False
    if "**Systems insight**" in line or "**Significance (quantitative)**" in line:
        return False
    if WALKTHROUGH_MARK.search(stripped):
        return True
    if not WALKTHROUGH_CALC.search(line):
        return False
    if in_callout and re.match(r"^\s*(?:[-*]|\d+\.)", line):
        return True
    return bool(re.search(r"(?:=|≈|\\approx|\s/\s)", line))


def _line_violations(line: str, in_callout: bool) -> list[str]:
    if "{python}" not in line:
        return []
    if line.lstrip().startswith(("#", "[^fn-", "|")):
        return []
    if not _is_walkthrough_line(line, in_callout):
        return []
    stripped = _strip_allowed_fragments(line)
    hits: list[str] = []
    for pattern, label in LITERAL_PATTERNS:
        if pattern.search(stripped):
            hits.append(label)
    return hits


def check_file(path: Path) -> list[tuple[int, str, list[str]]]:
    issues: list[tuple[int, str, list[str]]] = []
    in_python = False
    in_fence = False
    in_callout = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.rstrip()
        if CALLOUT_START.match(line):
            in_callout = True
        elif CALLOUT_END.match(line) and in_callout:
            in_callout = False
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
        hits = _line_violations(line, in_callout)
        if hits:
            issues.append((lineno, line.strip()[:120], hits))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="QMD files (default: all contents)")
    args = parser.parse_args()
    paths = args.paths or sorted(CONTENTS.rglob("*.qmd"))
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
        print(f"\n{failures} file(s) with LEGO prose literal violations")
        return 1
    print(f"OK LEGO prose literals ({total} QMD files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
