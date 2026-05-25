"""CI gate: constants.py must remain physics/units only (no hardware/model/fleet specs)."""

from __future__ import annotations

import ast
import re
from pathlib import Path

CONSTANTS_PATH = Path(__file__).resolve().parents[1] / "mlsysim" / "core" / "constants.py"

# Names matching these patterns belong in registries or core/calibration.py — not constants.py.
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
    re.compile(r"^PUE_"),
    re.compile(r"^CLOUD_(EGRESS|ELECTRICITY|GPU_)"),
    re.compile(r"^FLEET_"),
    re.compile(r"^CARBON_"),
    re.compile(r"^STORAGE_COST"),
    re.compile(r"^LABELING_COST"),
    re.compile(r"^TPU_POD_"),
)

def _defined_names(source: str) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names

def test_constants_has_no_forbidden_symbol_names() -> None:
    source = CONSTANTS_PATH.read_text(encoding="utf-8")
    defined = _defined_names(source)
    violations = sorted(
        name for name in defined
        if any(p.search(name) for p in FORBIDDEN_NAME_PATTERNS)
    )
    assert not violations, (
        "constants.py must not define hardware/model/fleet symbols:\n  "
        + "\n  ".join(violations)
    )

def test_constants_does_not_reexport_defaults() -> None:
    source = CONSTANTS_PATH.read_text(encoding="utf-8")
    assert "from .defaults import" not in source
    assert "import defaults" not in source

def test_constants_size_budget() -> None:
    """Guard against re-accumulating deleted constants."""
    line_count = len(CONSTANTS_PATH.read_text(encoding="utf-8").splitlines())
    assert line_count <= 220, f"constants.py grew to {line_count} lines (budget 220)"
