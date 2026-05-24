from ..core.constants import (
    CLOUD_LATENCY_RANGE_MS,
    CLOUD_MEM_GIB,
    EDGE_LATENCY_RANGE_MS,
    MOBILE_LATENCY_RANGE_MS,
    MOBILE_MEM_GIB,
    MOBILE_RAM_RANGE_GB,
    MOBILE_STORAGE_RANGE,
    MOBILE_TDP_RANGE_W,
    MCU_RAM_KIB,
    SMARTPHONE_RAM_GB,
    TINY_LATENCY_RANGE_MS,
    TINY_MEM_KIB,
    ureg,
)
from ..core.registry import Registry
from .types import PlatformEnvelope


class Platforms(Registry):
    Cloud = PlatformEnvelope(
        name="Cloud",
        ram=512 * ureg.GB,
        storage=10 * ureg.TB,
        typical_latency_budget=200 * ureg.ms,
        latency_range_ms=CLOUD_LATENCY_RANGE_MS,
        ram_range=f"{CLOUD_MEM_GIB.to('GiB').magnitude:.0f}+ GiB",
    )
    Edge = PlatformEnvelope(
        name="Edge",
        ram=32 * ureg.GB,
        storage=1 * ureg.TB,
        typical_latency_budget=50 * ureg.ms,
        latency_range_ms=EDGE_LATENCY_RANGE_MS,
    )
    Mobile = PlatformEnvelope(
        name="Mobile",
        ram=SMARTPHONE_RAM_GB,
        storage=256 * ureg.GB,
        typical_latency_budget=30 * ureg.ms,
        latency_range_ms=MOBILE_LATENCY_RANGE_MS,
        ram_range=MOBILE_RAM_RANGE_GB,
        storage_range=MOBILE_STORAGE_RANGE,
        tdp_range_w=MOBILE_TDP_RANGE_W,
    )
    Tiny = PlatformEnvelope(
        name="TinyML",
        ram=MCU_RAM_KIB,
        storage=4 * ureg.MB,
        typical_latency_budget=100 * ureg.ms,
        latency_range_ms=TINY_LATENCY_RANGE_MS,
        ram_range=f"{TINY_MEM_KIB.to('KiB').magnitude:.0f} KiB",
    )
