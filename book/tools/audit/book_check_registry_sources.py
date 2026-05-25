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

# Assignment targets in class bodies or module scope (including *_str / *_val_str).
ASSIGN_TARGET = re.compile(
    r"^\s*(?:class\s+\w+.*)?"
    r"([A-Za-z_][A-Za-z0-9_]*(?:_str|_val_str|_unit_str)?)\s*="
    r"(?!=)",
    re.M,
)

CONSTANTS_SPEC_ACCESS = re.compile(r"\bconstants\.([A-Za-z_][A-Za-z0-9_]*)")

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
            "MOBILE_TDP_W",
        )
    }
)

# Mirror mlsysim/tests/test_constants_allowlist.py — names belong in registries.
FORBIDDEN_NAME_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^(H100|A100|V100|B200|H200|MI300X|T4|TPU|JETSON|ESP32|DGX)_"),
    re.compile(r"^NVLINK_"),
    re.compile(r"^PCIE_GEN\d"),
    re.compile(r"^INFINIBAND_"),
    re.compile(r"^(H100|A100|V100|B200|H200|MI300X|T4|TPU).*(FLOPS|TOPS)"),
    re.compile(r"^(RESNET|BERT|MOBILENET|ALEXNET|YOLO|DLRM|GPT|LLAMA|STABLE_DIFFUSION).*(FLOPS|PARAMS|PARAM)"),
    re.compile(r"^GPT\d"),
    re.compile(r"^LLAMA"),
    re.compile(r"^IMAGENET"),
    re.compile(r"^MNIST"),
    re.compile(r"^CIFAR"),
    re.compile(r"^GPU_MTTF"),
    re.compile(r"^CLUSTER_"),
    re.compile(r"^GPUS_PER_HOST"),
    re.compile(r"^ALLREDUCE_FACTOR"),
    re.compile(r"^PUE_"),
    re.compile(r"^WUE_"),
    re.compile(r"^RACK_POWER_"),
    re.compile(r"^CARBON_"),
    re.compile(r"^OVERHEAD_"),
    re.compile(r"^MFU_"),
    re.compile(r"^SCALING_EFF_"),
    re.compile(r"^NIC_MTTF"),
    re.compile(r"^PSU_MTTF"),
    re.compile(r"^PCIE_SWITCH_MTTF"),
    re.compile(r"^CABLE_MTTF"),
    re.compile(r"^TOR_SWITCH_MTTF"),
    re.compile(r"^NODE_MTTF"),
    re.compile(r"^CLOUD_(EGRESS|ELECTRICITY|GPU_)"),
    re.compile(r"^FLEET_"),
    re.compile(r"^STORAGE_COST"),
    re.compile(r"^LABELING_COST"),
    re.compile(r"^TPU_POD_"),
)

# Physics-only symbols allowed via constants.* in LEGO cells.
CONSTANTS_PHYSICS_ALLOWLIST = frozenset(
    {
        "THOUSAND", "MILLION", "BILLION", "TRILLION",
        "HOURS_PER_DAY", "DAYS_PER_YEAR", "HOURS_PER_YEAR", "SECONDS_PER_HOUR",
        "BYTES_FP16", "BYTES_FP32", "BYTES_FP8", "BYTES_ADAM_STATE", "BYTES_FP32",
        "GB", "GiB", "TB", "MB", "KB", "KiB", "byte", "second", "watt", "USD",
        "TFLOPs", "PFLOPs", "Gbps", "Gparam", "Bparam", "param", "count",
        "ureg", "kilowatt", "NVME_SEQUENTIAL_BW",
    }
)

# Hardcoded grid/carbon literals that should use Infrastructure.Grids.*
HARDCODED_GRID = re.compile(
    r"(?:grid_ci|carbon_intensity|carbon_kg_per_kwh)\w*\s*=\s*(?:0\.429|0\.4|400\.0|0\.02)\b",
    re.I,
)

# Canonical dataset sizes belong in Datasets.*, not inline literals.
HARDCODED_DATASET = re.compile(
    r"\b(?:mnist_train_examples|training_examples)\s*=\s*60_000\b|"
    r"\bcifar10_full_labels\s*=\s*50_?000\b|"
    r"\bcifar10_num_classes\s*=\s*10\b|"
    r"\b(?:imagenet|mnist|cifar).*(?:size|examples|labels)\s*=\s*(?:1_?281_?167|1281167|50_?000|60_?000)\b",
    re.I,
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


def _strip_export_suffix(name: str) -> str:
    for suffix in ("_val_str", "_unit_str", "_str"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def _is_legacy_export_name(name: str) -> bool:
    base = _strip_export_suffix(name)
    if base in LEGACY_IMPORT_NAMES:
        return True
    return any(p.search(base) for p in FORBIDDEN_NAME_PATTERNS)


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
        for m in ASSIGN_TARGET.finditer(block):
            name = m.group(1)
            if name.startswith("_") or name in {"def", "class", "return", "if", "for"}:
                continue
            if _is_legacy_export_name(name):
                issues.append(
                    f"cell {idx}: legacy export name {name!r} — use descriptive registry-backed name"
                )
        for m in CONSTANTS_SPEC_ACCESS.finditer(block):
            sym = m.group(1)
            if sym not in CONSTANTS_PHYSICS_ALLOWLIST and (
                sym in LEGACY_IMPORT_NAMES or any(p.search(sym) for p in FORBIDDEN_NAME_PATTERNS)
            ):
                issues.append(
                    f"cell {idx}: forbidden constants.{sym} — use registry path"
                )
        if HARDCODED_GRID.search(block):
            issues.append(
                f"cell {idx}: hardcoded grid carbon intensity — use Infrastructure.Grids.*"
            )
        if HARDCODED_DATASET.search(block):
            issues.append(
                f"cell {idx}: hardcoded dataset size — use Datasets.ImageNet/CIFAR10/MNIST.*"
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
