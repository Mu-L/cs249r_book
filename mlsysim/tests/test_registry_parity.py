"""Parity tests: registry replacements must match legacy constants before deletion.

Populated incrementally as symbols migrate out of mlsysim.core.constants.
Run with: pytest mlsysim/tests/test_registry_parity.py -v
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = (
    REPO_ROOT / "book" / "tools" / "audit" / "artifacts" / "registry_migration_manifest.json"
)

# (constant_name, registry_getter) pairs added per migration step.
# Example after Hardware migration:
#   ("H100_FLOPS_FP16_TENSOR", lambda: Hardware.Cloud.H100.compute.peak_flops),
PARITY_CASES: list[tuple[str, str]] = []


def _load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        pytest.skip(f"missing manifest: {MANIFEST_PATH}")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize("constant_name,replacement", PARITY_CASES or [("_placeholder", None)])
def test_registry_parity(constant_name: str, replacement: str | None) -> None:
    if constant_name == "_placeholder":
        manifest = _load_manifest()
        migrate = [s for s in manifest.get("symbols", []) if s.get("action") == "migrate"]
        assert migrate, "manifest has no migrate symbols"
        pytest.skip("parity cases not yet wired; scaffold only")
    from mlsysim.core import constants as legacy

    legacy_val = getattr(legacy, constant_name)
    # Registry eval happens in step-specific commits once paths are stable.
    assert legacy_val is not None
    assert replacement is not None


def test_manifest_present() -> None:
    manifest = _load_manifest()
    assert manifest["symbol_count"] > 0
    assert "dead_count" in manifest
