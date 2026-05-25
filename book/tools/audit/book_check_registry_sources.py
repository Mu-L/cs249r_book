#!/usr/bin/env python3
"""Scan chapter QMD LEGO cells for banned legacy registry/constant patterns."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTENTS = REPO_ROOT / "book" / "quarto" / "contents"

CELL_START = re.compile(r"^```\{python\}")
CELL_END = re.compile(r"^```\s*$")

ALIAS_BANNED = re.compile(
    r"Systems\.Tiers\b|"
    r"\bHardware\.(H100|A100|V100|B200|ESP32|Jetson|iPhone)\b|"
    r"\bInfra\.|"
    r"\bdefaults\.|"
    r"\bGPUS_PER_HOST\b(?!_)|"
    r"\bALLREDUCE_FACTOR\b(?!_)"
)

# Re-exporting registry scalars under legacy flat names (use registry paths inline).
REGISTRY_REEXPORT = re.compile(
    r"^[A-Z][A-Z0-9_]+ = (Systems|Infrastructure|Literature|Ops|calibration)\.",
    re.M,
)

FROM_CONSTANTS = re.compile(r"^\s*from\s+mlsysim\.core\.constants\s+import\s+(.+)$", re.M)

# Legacy flat symbols that must not be imported by name from constants anymore.
LEGACY_IMPORT_NAMES = frozenset(
    {
        sym
        for sym in (
            "H100_FLOPS_FP16_TENSOR",
            "H100_MEM_BW",
            "H100_MEM_CAPACITY",
            "H100_TDP",
            "A100_FLOPS_FP16_TENSOR",
            "A100_TDP",
            "NVLINK_H100_BW",
            "NVLINK_A100_BW",
            "INFINIBAND_NDR_BW",
            "GPT3_PARAMS",
            "GPT3_TRAINING_TOKENS",
            "GPU_MTTF_HOURS",
            "CLUSTER_LARGE_GPUS",
            "IMAGENET_IMAGES",
            "RESNET50_FLOPs",
            "CLOUD_LATENCY_RANGE_MS",
            "CLOUD_MEM_GIB",
            "EDGE_LATENCY_RANGE_MS",
            "MOBILE_LATENCY_RANGE_MS",
            "TINY_LATENCY_RANGE_MS",
            "MOBILE_RAM_RANGE_GB",
            "MOBILE_STORAGE_RANGE",
            "MOBILE_TDP_RANGE_W",
            "SMARTPHONE_RAM_GB",
            "MCU_RAM_KIB",
            "MOBILE_MEM_GIB",
            "TINY_MEM_KIB",
        )
    }
)

def _parse_imported_names(import_clause: str) -> set[str]:
    names: set[str] = set()
    for part in import_clause.split(","):
        part = part.strip()
        if not part or part == "*":
            continue
        if " as " in part:
            part = part.split(" as ", 1)[0].strip()
        names.add(part)
    return names

def python_cells(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[str] = []
    i = 0
    while i < len(lines):
        if CELL_START.match(lines[i]):
            j = i + 1
            while j < len(lines) and not CELL_END.match(lines[j]):
                j += 1
            blocks.append("\n".join(lines[i + 1 : j]))
            i = j + 1
        else:
            i += 1
    return blocks

def check_file(path: Path) -> list[str]:
    issues: list[str] = []
    for idx, block in enumerate(python_cells(path), start=1):
        if ALIAS_BANNED.search(block):
            issues.append(f"cell {idx}: banned legacy alias (use registry paths)")
        if REGISTRY_REEXPORT.search(block):
            issues.append(
                f"cell {idx}: registry re-export alias — use Systems.* / Infrastructure.* / Literature.* inline"
            )
        for m in FROM_CONSTANTS.finditer(block):
            imported = _parse_imported_names(m.group(1))
            if "*" in m.group(1):
                continue
            bad = sorted(imported & LEGACY_IMPORT_NAMES)
            if bad:
                issues.append(
                    f"cell {idx}: legacy symbol import from constants: {', '.join(bad)}"
                )
    return issues

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="QMD files (default: all chapter contents)",
    )
    args = parser.parse_args()
    paths = args.paths or sorted(CONTENTS.rglob("*.qmd"))
    failures = 0
    for path in paths:
        p = path if path.is_absolute() else REPO_ROOT / path
        if not p.exists() or p.suffix != ".qmd":
            continue
        issues = check_file(p)
        if issues:
            failures += 1
            print(f"\n{p.relative_to(REPO_ROOT)}")
            for issue in issues:
                print(f"  {issue}")
    if failures:
        print(f"\n{failures} file(s) with registry source violations")
        return 1
    print(f"OK registry sources ({len(paths)} QMD files checked)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
