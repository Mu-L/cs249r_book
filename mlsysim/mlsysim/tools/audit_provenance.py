#!/usr/bin/env python3
"""Report missing or weak provenance on registry entries and sourced defaults."""

from __future__ import annotations

import argparse
import sys
from typing import Any, Iterable

from mlsysim.core import defaults
from mlsysim.core.appendix_lineage import audit_appendix_defaults
from mlsysim.core.provenance import Provenance, ProvenanceKind, Sourced, TraceableConstant
from mlsysim.hardware.registry import (
    CloudHardware,
    EdgeHardware,
    MobileHardware,
    TinyHardware,
    WorkstationHardware,
)
from mlsysim.infra.registry import Grids
from mlsysim.models.registry import (
    GenerativeVisionModels,
    LanguageModels,
    RecommendationModels,
    StateSpaceModels,
    TinyModels,
    VisionModels,
)


def _registry_nodes(registry_cls: type) -> Iterable[Any]:
    if not hasattr(registry_cls, "list"):
        return []
    return registry_cls.list()


def _validate_provenance_record(path: str, prov: Provenance | None) -> list[str]:
    if prov is None:
        return [f"{path}: missing provenance"]
    issues: list[str] = []
    if not prov.ref.strip():
        issues.append(f"{path}: empty provenance.ref")
    if prov.kind == ProvenanceKind.DATASHEET and not prov.url:
        issues.append(f"{path}: datasheet without url")
    if prov.kind == ProvenanceKind.ESTIMATE and not prov.notes:
        issues.append(f"{path}: estimate without notes")
    if prov.kind == ProvenanceKind.DERIVED and not prov.notes:
        issues.append(f"{path}: derived without notes")
    if prov.verified and len(prov.verified) != 10:
        issues.append(f"{path}: verified date must be YYYY-MM-DD")
    return issues


def _check_node(path: str, node: Any) -> list[str]:
    meta = getattr(node, "metadata", None)
    if meta is None:
        return [f"{path}: no metadata"]
    return _validate_provenance_record(path, getattr(meta, "provenance", None))


def audit_registries(*, scope_cloud: bool = False) -> list[str]:
    issues: list[str] = []
    groups = (
        [("Hardware.Cloud", CloudHardware)]
        if scope_cloud
        else [
            ("Hardware.Cloud", CloudHardware),
            ("Hardware.Workstation", WorkstationHardware),
            ("Hardware.Mobile", MobileHardware),
            ("Hardware.Edge", EdgeHardware),
            ("Hardware.Tiny", TinyHardware),
            ("Models.LanguageModels", LanguageModels),
            ("Models.VisionModels", VisionModels),
            ("Models.TinyModels", TinyModels),
            ("Models.RecommendationModels", RecommendationModels),
            ("Models.StateSpaceModels", StateSpaceModels),
            ("Models.GenerativeVisionModels", GenerativeVisionModels),
        ]
    )
    for prefix, reg in groups:
        for node in _registry_nodes(reg):
            name = getattr(node, "name", type(node).__name__)
            issues.extend(_check_node(f"{prefix}.{name}", node))
    return issues


def audit_infra_grids() -> list[str]:
    issues: list[str] = []
    for grid in _registry_nodes(Grids):
        name = getattr(grid, "name", type(grid).__name__)
        issues.extend(_check_node(f"Infrastructure.Grids.{name}", grid))
    return issues


def audit_defaults_traceable() -> list[str]:
    issues: list[str] = []
    for name in dir(defaults):
        if name.startswith("_"):
            continue
        val = getattr(defaults, name)
        if isinstance(val, TraceableConstant):
            issues.extend(
                _validate_provenance_record(f"defaults.{name}", getattr(val, "provenance", None))
            )
        elif isinstance(val, Sourced):
            issues.extend(_validate_provenance_record(f"defaults.{name}", val.provenance))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=("defaults", "cloud", "all", "textbook"),
        default="defaults",
        help="What to scan (textbook = full gates for assumption appendices)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when any issue is found (default: report only)",
    )
    args = parser.parse_args(argv)

    issues: list[str] = []
    if args.scope in ("defaults",):
        issues.extend(audit_defaults_traceable())
    if args.scope == "cloud":
        issues.extend(audit_registries(scope_cloud=True))
    if args.scope in ("all", "textbook"):
        issues.extend(audit_defaults_traceable())
        issues.extend(audit_registries(scope_cloud=False))
        issues.extend(audit_infra_grids())
    if args.scope == "textbook":
        issues.extend(audit_appendix_defaults())

    if issues:
        print(f"Provenance audit ({args.scope}): {len(issues)} issue(s)")
        for line in sorted(issues):
            print(f"  - {line}")
        return 1 if args.strict else 0

    print(f"Provenance audit OK (scope={args.scope}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
