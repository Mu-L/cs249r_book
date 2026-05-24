#!/usr/bin/env python3
"""Replace legacy mlsysim.core.constants hardware symbols with registry paths in QMD cells."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MAP_PATH = REPO_ROOT / "scripts" / "map_constants.py"

CELL_OPEN = re.compile(r"^```\{python\}")
CELL_CLOSE = re.compile(r"^```\s*$")

INTERCONNECT_MAP = {
    "NVLINK_V100_BW": "Hardware.Cloud.V100.nvlink.bandwidth",
    "NVLINK_A100_BW": "Hardware.Cloud.A100.nvlink.bandwidth",
    "NVLINK_H100_BW": "Hardware.Cloud.H100.nvlink.bandwidth",
    "NVLINK_B200_BW": "Hardware.Cloud.B200.nvlink.bandwidth",
    "PCIE_GEN3_BW": "Hardware.Cloud.V100.interconnect.bandwidth",
    "PCIE_GEN4_BW": "Hardware.Cloud.A100.interconnect.bandwidth",
    "PCIE_GEN5_BW": "Hardware.Cloud.H100.interconnect.bandwidth",
    "INFINIBAND_HDR_BW": "Systems.Fabrics.InfiniBand_HDR.bandwidth",
    "INFINIBAND_NDR_BW": "Systems.Fabrics.InfiniBand_NDR.bandwidth",
    "INFINIBAND_XDR_BW": "Systems.Fabrics.InfiniBand_XDR.bandwidth",
    "INFINIBAND_GXDR_BW": "Systems.Fabrics.InfiniBand_GXDR.bandwidth",
    "CPU_FLOPS_FP32": "Hardware.Cloud.ReferenceCPU.compute.peak_flops",
    "H100_L2_CACHE": "Hardware.Cloud.H100.memory.l2_cache",
    "TPUV5P_L2_SRAM": "Hardware.Cloud.TPUv5p.memory.l2_cache",
    "SGX_EPC_CAPACITY": "Hardware.Cloud.IntelSGX.memory.capacity",
    "SGX_BASE_LATENCY": "Hardware.Cloud.IntelSGX.dispatch_tax",
    "SGX_OVERFLOW_LATENCY": "Hardware.Cloud.IntelSGX.dispatch_tax",
}


def load_map_constants() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location("map_constants", MAP_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(getattr(mod, "mapping", {}))


def merged_mapping() -> dict[str, str]:
    out = {**load_map_constants(), **INTERCONNECT_MAP}
    return dict(sorted(out.items(), key=lambda kv: len(kv[0]), reverse=True))


def substitute_cell(cell: str, mapping: dict[str, str]) -> tuple[str, list[str]]:
    replaced: list[str] = []
    out = cell
    for sym, target in mapping.items():
        pat = re.compile(rf"\b{re.escape(sym)}\b")
        if pat.search(out):
            out = pat.sub(target, out)
            replaced.append(sym)
    return out, replaced


def ensure_registry_imports(cell: str) -> str:
    needs_hardware = "Hardware." in cell and "import Hardware" not in cell and "from mlsysim import *" not in cell
    needs_systems = "Systems." in cell and "import Systems" not in cell and "from mlsysim import *" not in cell
    needs_models = "Models." in cell and "import Models" not in cell and "from mlsysim import *" not in cell
    prefix = []
    if needs_hardware or needs_systems or needs_models:
        if "from mlsysim import *" not in cell:
            prefix.append("from mlsysim import *")
    if not prefix:
        return cell
    lines = cell.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("#|") or line.startswith("# ") or line.startswith("#┌"):
            insert_at = i + 1
        elif line.strip() and not line.startswith("#"):
            break
    return "\n".join(lines[:insert_at] + prefix + lines[insert_at:])


def migrate_file(path: Path, mapping: dict[str, str], dry_run: bool) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out_lines: list[str] = []
    stats = {"cells": 0, "cells_changed": 0, "symbols": set()}
    i = 0
    while i < len(lines):
        if CELL_OPEN.match(lines[i]):
            start = i
            j = i + 1
            while j < len(lines) and not CELL_CLOSE.match(lines[j]):
                j += 1
            block = "\n".join(lines[i + 1 : j])
            new_block, replaced = substitute_cell(block, mapping)
            new_block = ensure_registry_imports(new_block)
            stats["cells"] += 1
            if replaced:
                stats["cells_changed"] += 1
                stats["symbols"].update(replaced)
            out_lines.extend(lines[i : i + 1])
            out_lines.extend(new_block.splitlines())
            out_lines.append(lines[j])
            i = j + 1
        else:
            out_lines.append(lines[i])
            i += 1
    new_text = "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")
    if not dry_run and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    stats["symbols"] = sorted(stats["symbols"])
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qmd", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path = args.qmd if args.qmd.is_absolute() else REPO_ROOT / args.qmd
    mapping = merged_mapping()
    stats = migrate_file(path, mapping, dry_run=args.dry_run)
    print(f"{path}: {stats['cells_changed']}/{stats['cells']} cells, {len(stats['symbols'])} symbols")
    for sym in stats["symbols"]:
        print(f"  - {sym}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
