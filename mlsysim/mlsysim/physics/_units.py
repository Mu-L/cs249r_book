"""Shared unit helpers for physics formulas."""

from __future__ import annotations

import pint

from mlsysim.core.constants import ureg


def _ensure_unit(val, expected_unit, param_name="Value"):
    """
    Attach a unit if val is a raw number; verify dimensional correctness
    if it is already a Pint Quantity.
    """
    if isinstance(val, (int, float)):
        return val * expected_unit
    if isinstance(val, ureg.Quantity):
        if not val.check(expected_unit):
            raise pint.DimensionalityError(
                val.units,
                expected_unit,
                extra_msg=(
                    f"\n[Pedagogical Error] '{param_name}' requires units of "
                    f"{expected_unit.dimensionality}. You provided '{val.units}'."
                ),
            )
        return val
    raise TypeError(
        f"Expected a number or Pint Quantity for {param_name}, got {type(val).__name__}"
    )
