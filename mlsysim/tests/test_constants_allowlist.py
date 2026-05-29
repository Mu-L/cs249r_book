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

# Spec categories being migrated OUT of constants.py to their domain homes
# (taxonomy refactor 2026-05, plan_mlsysim_taxonomy_refactor). These are not yet
# hard-forbidden because the migration is in flight — instead a RATCHET keeps the
# count monotonically shrinking: new mis-homed constants can't be added, and each
# migration phase lowers BACKLOG_CEILING. When it reaches 0, fold these into
# FORBIDDEN_NAME_PATTERNS and delete the ratchet (phase P8).
MIGRATION_PENDING_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^LATENCY_"),
    re.compile(r"^ENERGY_"),
    re.compile(r"^(NETWORK_|ETHERNET_|SWITCH_|OPTICS_|FABRIC_|FEC_)"),
    re.compile(r"^(NVME_|SYSTEM_MEMORY_BW|HOST_DRAM_BW|LOCAL_NVME)"),
    re.compile(r"^(MOBILE_|PHONE_|BATTERY_|OBJECT_DETECTOR_)"),
    re.compile(r"^(TRANSFORMER_|SYSTOLIC_)"),
    re.compile(r"^(GMAIL_|GOOGLE_|WAYMO_|ANOMALY_)"),
    re.compile(r"^(VIDEO_|IMAGE_|COLOR_DEPTH)"),
    re.compile(r"^(ML_WORKFLOW_|SYNTHETIC_|LOGIC_WALL_)"),
)
# Lower this with each migration phase; it must never increase.
BACKLOG_CEILING = 68  # P7a moved TRANSFORMER_* (ratios->Literature, dims inlined); target 0


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

def test_constants_migration_backlog_ratchets_down() -> None:
    """Spec constants pending migration to domain homes may only shrink, never grow."""
    source = CONSTANTS_PATH.read_text(encoding="utf-8")
    defined = _defined_names(source)
    pending = sorted(
        name for name in defined
        if any(p.search(name) for p in MIGRATION_PENDING_PATTERNS)
    )
    assert len(pending) <= BACKLOG_CEILING, (
        f"migration backlog grew to {len(pending)} (ceiling {BACKLOG_CEILING}); "
        "new spec constants must go to their domain registry, not constants.py:\n  "
        + "\n  ".join(pending)
    )


def test_constants_size_budget() -> None:
    """Guard against re-accumulating deleted constants."""
    line_count = len(CONSTANTS_PATH.read_text(encoding="utf-8").splitlines())
    assert line_count <= 220, f"constants.py grew to {line_count} lines (budget 220)"
