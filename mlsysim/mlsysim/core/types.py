from typing import Any, Annotated, Optional
from pydantic import AfterValidator, PlainSerializer, BaseModel, model_validator
from .constants import Q_
from .provenance import Provenance, ProvenanceKind

def validate_quantity(v: Any) -> Q_:
    if isinstance(v, Q_):
        return v
    if isinstance(v, (int, float, str)):
        try:
            return Q_(v)
        except Exception as e:
            raise ValueError(f"Could not parse Quantity from {v}: {e}")
    raise ValueError(f"Expected Quantity, got {type(v)}")

def serialize_quantity(v: Q_) -> str:
    # Use compact format for serialization
    return f"{v:~P}"

Quantity = Annotated[
    Any,
    AfterValidator(validate_quantity),
    PlainSerializer(serialize_quantity, return_type=str)
]

class Metadata(BaseModel):
    """Provenance for registry entries (hardware, models, fabrics)."""

    provenance: Optional[Provenance] = None
    source: Optional[str] = None  # legacy; prefer provenance
    source_url: Optional[str] = None
    description: Optional[str] = None
    last_verified: Optional[str] = None  # YYYY-MM-DD
    version: Optional[str] = None

    @model_validator(mode="after")
    def _coalesce_provenance(self) -> Metadata:
        if self.provenance is not None:
            return self
        if not self.source and not self.source_url:
            return self
        kind = ProvenanceKind.DATASHEET if self.source_url else ProvenanceKind.LITERATURE
        ref = self.source or "(see source_url)"
        self.provenance = Provenance(
            kind=kind,
            ref=ref,
            url=self.source_url,
            verified=self.last_verified,
        )
        return self

    @property
    def source_label(self) -> Optional[str]:
        """Human-readable source (provenance.ref or legacy source)."""
        if self.provenance is not None:
            return self.provenance.ref
        return self.source
