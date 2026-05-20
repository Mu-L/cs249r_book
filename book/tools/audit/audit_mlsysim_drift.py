#!/usr/bin/env python3
"""
audit_mlsysim_drift.py — find hand-coded values in chapter QMDs that should
come from mlsysim's canonical constants.

Approach:
  1. Build a registry of (canonical_name, numeric_value, magnitude_tolerance)
     from mlsysim.core.constants.
  2. Walk every chapter QMD's Python cells. For each numeric literal
     assignment, check if (a) the variable name resembles a canonical name
     fragment AND (b) the literal matches the canonical value (within
     tolerance to allow for unit conversions and rounding).
  3. Report drift.

This is a one-time audit (a recurring lint can be added separately to
audit_math_canonical if drift is significant).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Hand-curated registry of canonical (name fragment, value, tolerance, mlsysim path).
# Tolerance is fractional (0.02 = 2%) to allow for rounding and unit conversions.
# Names are *fragments* — we substring-match against variable identifiers in QMDs.
CANONICAL = [
    # GPU compute (TFLOPS)
    ("v100_fp16",      125,   0.02, "V100_FLOPS_FP16_TENSOR"),
    ("v100_tflops",    125,   0.02, "V100_FLOPS_FP16_TENSOR"),
    ("v100_fp32",      15.7,  0.05, "V100_FLOPS_FP32"),
    ("a100_fp16",      312,   0.02, "A100_FLOPS_FP16_TENSOR"),
    ("a100_tflops",    312,   0.02, "A100_FLOPS_FP16_TENSOR"),
    ("a100_tf32",      156,   0.02, "A100_FLOPS_TF32"),
    ("a100_fp32",      19.5,  0.05, "A100_FLOPS_FP32"),
    ("a100_int8",      624,   0.02, "A100_FLOPS_INT8"),
    ("a100_sparse",    624,   0.02, "A100_FLOPS_FP16_SPARSE"),
    ("h100_fp16",      989,   0.02, "H100_FLOPS_FP16_TENSOR"),
    ("h100_tflops",    989,   0.02, "H100_FLOPS_FP16_TENSOR"),
    ("h100_fp8",       1979,  0.02, "H100_FLOPS_FP8_TENSOR"),
    ("h100_tf32",      494,   0.02, "H100_FLOPS_TF32"),
    ("h100_int8",      1979,  0.02, "H100_FLOPS_INT8"),
    ("b200_fp16",      2250,  0.02, "B200_FLOPS_FP16_TENSOR"),
    ("b200_fp8",       4500,  0.02, "B200_FLOPS_FP8_TENSOR"),
    ("mi300x_fp16",    1307,  0.02, "MI300X_FLOPS_FP16_TENSOR"),

    # GPU memory (GiB, GB/s, TB/s)
    ("v100_mem_gb",    32,    0.05, "V100_MEM_CAPACITY"),
    ("v100_mem_bw",    900,   0.02, "V100_MEM_BW"),
    ("a100_mem_gb",    80,    0.05, "A100_MEM_CAPACITY"),
    ("a100_mem_bw",    2039,  0.02, "A100_MEM_BW"),
    ("a100_mem_tbs",   2.04,  0.02, "A100_MEM_BW (TB/s)"),
    ("h100_mem_gb",    80,    0.05, "H100_MEM_CAPACITY"),
    ("h100_mem_bw",    3350,  0.02, "H100_MEM_BW (GB/s)"),
    ("h100_mem_tbs",   3.35,  0.02, "H100_MEM_BW (TB/s)"),
    ("h200_mem_gb",    141,   0.05, "H200_MEM_CAPACITY"),
    ("h200_mem_tbs",   4.8,   0.02, "H200_MEM_BW (TB/s)"),
    ("b200_mem_gb",    192,   0.05, "B200_MEM_CAPACITY"),
    ("b200_mem_tbs",   8,     0.05, "B200_MEM_BW (TB/s)"),

    # GPU power (W)
    ("v100_tdp",       300,   0.05, "V100_TDP"),
    ("a100_tdp",       400,   0.05, "A100_TDP"),
    ("h100_tdp",       700,   0.05, "H100_TDP"),
    ("h200_tdp",       700,   0.05, "H200_TDP"),
    ("b200_tdp",       1000,  0.05, "B200_TDP"),

    # Model parameters (count)
    ("gpt3_params_b",  175,   0.02, "GPT3_PARAMS (in B)"),
    ("gpt3_params_billion", 175, 0.02, "GPT3_PARAMS (in B)"),
    ("llama2_70b_params_b", 70, 0.02, "LLAMA2_70B_PARAMS (in B)"),
    ("llama2_70b_layers",   80, 0.05, "LLAMA2_70B_LAYERS"),
    ("llama2_70b_hidden",   8192, 0.02, "LLAMA2_70B_HIDDEN_DIM"),
    ("llama2_70b_heads",    64, 0.05, "LLAMA2_70B_HEADS"),
    ("llama2_70b_kv_heads", 8,  0.05, "LLAMA2_70B_KV_HEADS"),
    ("gpt2_params_m",       1500, 0.05, "GPT2_PARAMS (XL, in M)"),

    # GPT-3 training (energy + ops)
    ("gpt3_train_energy_mwh", 1287, 0.05, "GPT3_TRAINING_ENERGY_MWH"),
    ("gpt3_train_ops",       3.14e23, 0.05, "GPT3_TRAINING_OPS"),

    # Interconnect bandwidth (GB/s)
    ("pcie_gen4_gb",   32,    0.05, "PCIE_GEN4_BW (x16)"),
    ("pcie_gen5_gb",   64,    0.05, "PCIE_GEN5_BW (x16)"),
    ("nvlink_h100",    900,   0.02, "NVLink 4.0 (H100)"),
    ("nvlink_a100",    600,   0.02, "NVLink 3.0 (A100)"),
]


# Python LEGO cells are fenced ```{python} ... ```
CELL_OPEN_RE = re.compile(r"^```\s*\{python\b[^}]*\}\s*$")
CELL_CLOSE_RE = re.compile(r"^```\s*$")

# Match `var = LITERAL` where LITERAL is a number (possibly with _N or scientific)
ASSIGN_RE = re.compile(
    r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([0-9][0-9_]*(?:\.[0-9_]+)?(?:[eE][+\-]?[0-9]+)?)\b"
)


def python_cells(qmd_text: str):
    """Yield (start_line, line) for each line inside a {python} fence."""
    in_cell = False
    for i, line in enumerate(qmd_text.splitlines(), start=1):
        if not in_cell and CELL_OPEN_RE.match(line):
            in_cell = True
            continue
        if in_cell and CELL_CLOSE_RE.match(line):
            in_cell = False
            continue
        if in_cell:
            yield i, line


def parse_literal(s: str) -> float | None:
    try:
        return float(s.replace("_", ""))
    except ValueError:
        return None


def matches_canonical(var_name: str, value: float):
    """Return list of canonical matches for this (var, value) pair."""
    matches = []
    lower = var_name.lower()
    for fragment, canon_value, tol, path in CANONICAL:
        if fragment not in lower:
            continue
        # Magnitude tolerance check
        if canon_value == 0:
            continue
        rel_error = abs(value - canon_value) / canon_value
        if rel_error <= tol:
            matches.append((fragment, canon_value, path))
    return matches


def audit_file(path: Path) -> list:
    text = path.read_text(encoding="utf-8", errors="ignore")
    findings = []
    for lineno, line in python_cells(text):
        # Skip comments (a bare assignment in a comment shouldn't fire)
        if line.lstrip().startswith("#"):
            continue
        m = ASSIGN_RE.match(line)
        if not m:
            continue
        var, lit = m.group(1), m.group(2)
        val = parse_literal(lit)
        if val is None:
            continue
        canon = matches_canonical(var, val)
        if canon:
            findings.append((path, lineno, line.rstrip(), var, val, canon))
    return findings


def main():
    root = Path("book/quarto/contents")
    if not root.exists():
        print(f"ERROR: run from MLSysBook root (expected {root})", file=sys.stderr)
        sys.exit(2)
    qmds = sorted(root.rglob("*.qmd"))
    all_findings = []
    for q in qmds:
        all_findings.extend(audit_file(q))
    if not all_findings:
        print("✓ no hand-coded canonical-constant drift detected")
        return 0
    # Group by file
    print(f"Found {len(all_findings)} potential drift sites:\n")
    last_file = None
    for path, lineno, line, var, val, canon in all_findings:
        if path != last_file:
            print(f"\n📄 {path}")
            last_file = path
        canon_str = ", ".join(f"{p}" for _, _, p in canon)
        print(f"  L{lineno}: {var} = {val}")
        print(f"           → matches mlsysim.{canon_str}")
        print(f"           {line.strip()}")
    print(f"\nTotal: {len(all_findings)} drift candidates")
    return 1


if __name__ == "__main__":
    sys.exit(main())
