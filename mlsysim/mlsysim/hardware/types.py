from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
from ..core.constants import Q_
from ..core.types import Quantity, Metadata
from typing import ClassVar

class ComputeCore(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    peak_flops: Quantity
    precision_flops: Dict[str, Quantity] = Field(default_factory=dict)

class MemoryHierarchy(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    capacity: Quantity           # Primary memory (HBM for GPUs, SRAM for MCUs)
    bandwidth: Quantity          # Primary memory bandwidth
    # On-chip SRAM (optional — for modeling FlashAttention tiling on GPUs,
    # or the fast scratchpad on microcontrollers)
    sram_capacity: Optional[Quantity] = None
    sram_bandwidth: Optional[Quantity] = None
    # Flash storage (optional — for TinyML devices where weights live in flash)
    flash_capacity: Optional[Quantity] = None
    flash_bandwidth: Optional[Quantity] = None
    l2_cache: Optional[Quantity] = None

class StorageHierarchy(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    capacity: Quantity
    bandwidth: Quantity
    latency: Optional[Quantity] = None

class IOInterconnect(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str # e.g., "PCIe Gen4 x16"
    bandwidth: Quantity
    latency: Optional[Quantity] = None

class HardwareNode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    release_year: int
    compute: ComputeCore
    memory: MemoryHierarchy
    storage: Optional[StorageHierarchy] = None
    interconnect: Optional[IOInterconnect] = None  # Host I/O (e.g., PCIe)
    nvlink: Optional[IOInterconnect] = None        # Intra-node GPU-GPU (NVLink/ICI)
    tdp: Optional[Quantity] = None
    battery_capacity: Optional[Quantity] = None
    unit_cost: Optional[Quantity] = None
    embodied_carbon_kg: Optional[float] = Field(
        default=None,
        description="Embodied CO2e in kg from manufacturing, packaging, and transport (Gupta et al. 2022)."
    )
    dispatch_tax: Quantity = Field(default_factory=lambda: Q_("0.01 ms"))
    metadata: Metadata = Field(default_factory=Metadata)

    # Backward-compatible flat access properties (chapters use these)
    @property
    def peak_flops(self) -> Quantity:
        return self.compute.peak_flops

    @property
    def peak_flops_fp32(self) -> Optional[Quantity]:
        return self.compute.precision_flops.get('fp32')

    @property
    def memory_bw(self) -> Quantity:
        return self.memory.bandwidth

    @property
    def memory_capacity(self) -> Quantity:
        return self.memory.capacity

    @property
    def ram(self) -> Quantity:
        return self.memory.capacity

    @property
    def power_budget(self) -> Optional[Quantity]:
        return self.tdp

    def ridge_point(self, precision: Optional[str] = None) -> Quantity:
        """
        Calculates the Roofline ridge point (Intensity threshold).
        
        Args:
            precision: Optional precision string (e.g., 'fp16', 'fp8', 'int8').
                If provided, uses the corresponding precision flops from ComputeCore.
                If None (default), uses the default peak_flops.
        """
        flops = self.compute.peak_flops
        if precision:
            if precision.lower() in self.compute.precision_flops:
                flops = self.compute.precision_flops[precision.lower()]
            else:
                import warnings
                warnings.warn(
                    f"Precision '{precision}' not found in hardware '{self.name}'; "
                    f"using default peak_flops.",
                    stacklevel=2
                )
        return (flops / self.memory.bandwidth).to('flop/byte')

    def __repr__(self):
        return f"HardwareNode({self.name}, {self.release_year})"