"""Lineage gates for numbers that appear in assumption appendices."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .provenance import Provenance, TraceableConstant

_REPO_ROOT = Path(__file__).resolve().parents[3]
APPENDIX_ASSUMPTIONS_QMD = (
    _REPO_ROOT / "book/quarto/contents/vol1/backmatter/appendix_assumptions.qmd",
    _REPO_ROOT / "book/quarto/contents/vol2/backmatter/appendix_assumptions.qmd",
)

_DEFAULTS_REF = re.compile(r"\bdefaults\.([A-Z][A-Z0-9_]+)\b")

# Pint quantities in appendices: provenance keyed by defaults symbol name.
QUANTITY_PROVENANCE: dict[str, Provenance] = {}


def register_quantity_provenance(mapping: dict[str, Provenance]) -> None:
    """Called from defaults.py after catalog is populated."""
    QUANTITY_PROVENANCE.clear()
    QUANTITY_PROVENANCE.update(mapping)


def defaults_symbols_in_appendices() -> set[str]:
    symbols: set[str] = set()
    for path in APPENDIX_ASSUMPTIONS_QMD:
        if path.is_file():
            symbols.update(_DEFAULTS_REF.findall(path.read_text(encoding="utf-8")))
    return symbols


def provenance_for_default(name: str, value: Any) -> Provenance | None:
    if isinstance(value, TraceableConstant):
        return getattr(value, "provenance", None)
    return QUANTITY_PROVENANCE.get(name)


def audit_appendix_defaults() -> list[str]:
    """Every ``defaults.*`` referenced in assumption appendices must have provenance."""
    from . import defaults as defaults_mod

    issues: list[str] = []
    for symbol in sorted(defaults_symbols_in_appendices()):
        if not hasattr(defaults_mod, symbol):
            issues.append(f"defaults.{symbol}: referenced in appendix but undefined")
            continue
        value = getattr(defaults_mod, symbol)
        if provenance_for_default(symbol, value) is None:
            issues.append(
                f"defaults.{symbol}: used in appendix_assumptions.qmd without provenance"
            )
    return issues
