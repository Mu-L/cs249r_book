"""Hardware technology-class reference facts (exposed as ``Hardware.Tech``).

Technology-CLASS properties — access latency, per-operation/per-byte energy, and generic
component bandwidth — that are ~constant across parts of a generation. This is the
counterpart to the per-instance specs on the Hardware.Cloud/Edge/Mobile/Tiny nodes
(capacity, bandwidth, TDP, price), which genuinely vary part-to-part.
See .claude/rules/mlsysim.md -> Canonical organization (the instance-vs-tech-class split).

Energy figures are Horowitz (2014), 45 nm — process-stamped in the names and provenance
so a future process node can coexist rather than overwrite the teaching anchor (invariant #3).
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..core.types import Quantity, Metadata
from ..core.registry import Registry
from ..core import provenance_catalog as pc
from ..core.units import ureg, GB, byte, flop, count, second

_ns = ureg.ns
_pj = ureg.picojoule


def _md(prov):
    return Metadata(provenance=prov)


class MemoryTier(BaseModel):
    """On-chip / off-chip memory technology tier: access latency + access energy."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    latency: Optional[Quantity] = None            # access latency
    energy_per_access: Optional[Quantity] = None  # pJ per access
    energy_per_byte: Optional[Quantity] = None    # pJ per byte
    metadata: Metadata = Field(default_factory=Metadata)


class StorageTier(BaseModel):
    """Generic storage/memory bandwidth tier (sequential bandwidth + optional latency)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    bandwidth: Quantity
    latency: Optional[Quantity] = None
    metadata: Metadata = Field(default_factory=Metadata)


class OpEnergy(BaseModel):
    """Per-operation energy for an arithmetic op (technology/process-class)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    energy: Quantity
    metadata: Metadata = Field(default_factory=Metadata)


class Memory(Registry):
    """On-chip memory hierarchy tiers (access latency + 45 nm access energy)."""

    Register = MemoryTier(name="Register file", latency=0.3 * _ns, energy_per_access=0.01 * _pj, metadata=_md(pc.HOROWITZ_ENERGY))
    L1 = MemoryTier(name="L1 / SRAM", latency=1 * _ns, energy_per_access=0.5 * _pj, metadata=_md(pc.HOROWITZ_ENERGY))
    L2 = MemoryTier(name="L2 cache", latency=4 * _ns, energy_per_access=2.0 * _pj, metadata=_md(pc.HOROWITZ_ENERGY))
    HBM3 = MemoryTier(name="HBM3", latency=300 * _ns, energy_per_access=640 * _pj, energy_per_byte=160 * _pj / byte, metadata=_md(pc.HOROWITZ_ENERGY))


class Storage(Registry):
    """Generic storage / off-chip memory bandwidth tiers."""

    NvmeGen3 = StorageTier(name="NVMe SSD (Gen3)", bandwidth=3.5 * GB / second, metadata=_md(pc.BOOK_STORAGE_TIERS))
    NvmeGen4 = StorageTier(name="NVMe SSD (Gen4)", bandwidth=7.0 * GB / second, metadata=_md(pc.BOOK_STORAGE_TIERS))
    NvmeGen5 = StorageTier(name="NVMe SSD (Gen5)", bandwidth=14.0 * GB / second, metadata=_md(pc.BOOK_STORAGE_TIERS))
    SystemMemory = StorageTier(name="System memory (DDR4/5)", bandwidth=50 * GB / second, metadata=_md(pc.BOOK_STORAGE_TIERS))
    HostDram = StorageTier(name="Host DRAM", bandwidth=200 * GB / second, metadata=_md(pc.BOOK_STORAGE_TIERS))


class Op(Registry):
    """Per-operation arithmetic energy (Horowitz 2014, 45 nm)."""

    FlopFp32 = OpEnergy(name="FP32 multiply-add (45 nm)", energy=3.7 * _pj / flop, metadata=_md(pc.HOROWITZ_ENERGY))
    FlopFp16 = OpEnergy(name="FP16 multiply-add (45 nm)", energy=1.1 * _pj / flop, metadata=_md(pc.HOROWITZ_ENERGY))
    OpInt8 = OpEnergy(name="INT8 multiply-add (45 nm)", energy=0.2 * _pj / count, metadata=_md(pc.HOROWITZ_ENERGY))
    AddFp32 = OpEnergy(name="FP32 add (45 nm)", energy=0.9 * _pj, metadata=_md(pc.HOROWITZ_ENERGY))
    AddFp16 = OpEnergy(name="FP16 add (45 nm)", energy=0.4 * _pj, metadata=_md(pc.HOROWITZ_ENERGY))
    AddInt32 = OpEnergy(name="INT32 add (45 nm)", energy=0.1 * _pj, metadata=_md(pc.HOROWITZ_ENERGY))
    AddInt8 = OpEnergy(name="INT8 add (45 nm)", energy=0.03 * _pj, metadata=_md(pc.HOROWITZ_ENERGY))


class Tech(Registry):
    """Technology-class reference facts: latency / energy / generic bandwidth."""

    Memory = Memory
    Storage = Storage
    Op = Op


def resolve_latency(instance_latency, tech_default):
    """Invariant #1 fallback: use the instance's own measured value when set, else the
    technology-class default. e.g. ``resolve_latency(node.memory.latency, Tech.Memory.HBM3.latency)``.
    Lets a specific chip override a class fact without forcing per-instance values everywhere."""
    return instance_latency if instance_latency is not None else tech_default
