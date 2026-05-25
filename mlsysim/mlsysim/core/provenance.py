"""Provenance types for registry entries and book-facing defaults."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, Optional, TypeVar, Union

from pydantic import BaseModel, Field, model_validator

T = TypeVar("T")
Scalar = Union[int, float]


class ProvenanceKind(str, Enum):
    DATASHEET = "datasheet"
    LITERATURE = "literature"
    INDUSTRY_REPORT = "industry_report"
    CONVENTION = "convention"
    ESTIMATE = "estimate"
    DERIVED = "derived"
    ILLUSTRATIVE = "illustrative"
    HEURISTIC = "heuristic"


class Provenance(BaseModel):
    """How we know a numeric value (package audit trail; not BibTeX)."""

    kind: ProvenanceKind
    ref: str = Field(min_length=1)
    url: Optional[str] = None
    verified: Optional[str] = None  # YYYY-MM-DD
    notes: Optional[str] = None
    id: Optional[str] = None  # stable slug, e.g. prov:iea-weo-2023-carbon

    @model_validator(mode="after")
    def _validate_kind_rules(self) -> Provenance:
        if self.kind == ProvenanceKind.DATASHEET and not self.url:
            raise ValueError(f"datasheet provenance requires url: {self.ref!r}")
        if self.kind == ProvenanceKind.ESTIMATE and not self.notes:
            raise ValueError(f"estimate provenance requires notes: {self.ref!r}")
        if self.kind == ProvenanceKind.DERIVED and not self.notes:
            raise ValueError(f"derived provenance requires notes: {self.ref!r}")
        return self


def scalar_value(x: Scalar | "Sourced[Scalar]" | "TraceableConstant") -> float:
    """Plain float for arithmetic and Quarto ``{python}`` cells."""
    if isinstance(x, Sourced):
        v = x.value
    elif isinstance(x, TraceableConstant):
        v = float(x)
    else:
        v = x
    return float(v)


@dataclass(frozen=True)
class Sourced(Generic[T]):
    """Value with mandatory provenance (use ``scalar_value`` or ``float()`` in math)."""

    value: T
    provenance: Provenance

    def __float__(self) -> float:
        return float(self.value)

    def __int__(self) -> int:
        return int(self.value)

    # Appendix/table formatting often uses ``val:g`` on scalars.
    def __format__(self, format_spec: str) -> str:
        return format(self.value, format_spec)

    @property
    def source(self) -> str:
        """Human-readable source (compat with TraceableConstant)."""
        return self.provenance.ref

    @property
    def url(self) -> Optional[str]:
        return self.provenance.url


class TraceableConstant(float):
    """
    Float assumption with provenance (appendix-safe arithmetic).

    Prefer ``Sourced`` for new code; this type remains for existing defaults
    and LEGO cells that rely on ``float`` behavior.
    """

    def __new__(
        cls,
        value,
        name: str,
        description: str,
        source: str,
        url: Optional[str] = None,
        *,
        provenance: Optional[Provenance] = None,
        kind: ProvenanceKind = ProvenanceKind.LITERATURE,
    ):
        if provenance is None:
            provenance = Provenance(kind=kind, ref=source, url=url)
        obj = super().__new__(cls, value)
        obj._sourced = Sourced(value, provenance)  # type: ignore[attr-defined]
        obj.name = name
        obj.description = description
        obj.provenance = provenance
        obj.source = provenance.ref
        obj.url = provenance.url
        return obj

    def render_markdown(self) -> str:
        lines = [
            f"**Assumption: {self.name}** = `{float(self)}`",
            "",
            f"_{self.description}_",
            "",
            f"> **Kind:** {self.provenance.kind.value}",
        ]
        if self.url:
            lines.append(f"> **Source:** [{self.source}]({self.url})")
        else:
            lines.append(f"> **Source:** {self.source}")
        if self.provenance.notes:
            lines.append(f"> **Notes:** {self.provenance.notes}")
        return "\n".join(lines)


def fleet_mttf_hours(
    hours: float,
    *,
    component: str,
    failure_mode: str = "",
) -> TraceableConstant:
    """MTTF anchor aligned with appendix_reliability @tbl-component-fit."""
    from .provenance_catalog import RELIABILITY_MTTF_LITERATURE

    desc = f"Steady-state MTTF for {component} in continuous datacenter operation."
    if failure_mode:
        desc += f" Typical mode: {failure_mode}."
    return TraceableConstant(
        hours,
        name=f"{component} MTTF (hours)",
        description=desc,
        source=RELIABILITY_MTTF_LITERATURE.ref,
        url=RELIABILITY_MTTF_LITERATURE.url,
        provenance=RELIABILITY_MTTF_LITERATURE,
    )
