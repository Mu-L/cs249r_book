from pydantic import BaseModel, ConfigDict

from ..core.types import Quantity


class PlatformEnvelope(BaseModel):
    """Abstract deployment envelope (RAM, storage, latency budget)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    ram: Quantity
    storage: Quantity
    typical_latency_budget: Quantity
    latency_range_ms: str | None = None
    ram_range: str | None = None
    storage_range: str | None = None
    tdp_range_w: str | None = None
