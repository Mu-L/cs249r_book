"""Published literature anchors cited in the book (MFU, scaling, Chinchilla, …)."""

from ..core.provenance import sourced
from ..core.registry import Registry
from ..core import provenance_catalog as pc


class Training(Registry):
    MfuLow = sourced(0.30, pc.PALM_MFU, name="MFU Training (Lower Bound)", description="Lower bound MFU for well-optimized large-model training.")
    MfuHigh = sourced(0.50, pc.PALM_MFU, name="MFU Training (Upper Bound)", description="Upper bound MFU for excellent large-model training runs.")
    MfuInferenceBatch1 = sourced(0.05, pc.POPE_INFERENCE, name="MFU Inference (Batch 1)", description="MFU for single-request inference, heavily memory-bandwidth-bound.")
    MfuInferenceBatched = sourced(0.40, pc.MFU_INFERENCE_BATCHED_LIT, name="MFU Inference (Batched)", description="Illustrative MFU upper bound for large-batch inference.")


class Scaling(Registry):
    Eff32Gpu = sourced(0.90, pc.BOOK_SCALING_EFFICIENCY_TIERS, name="Scaling Efficiency (32 GPUs)", description="Near-linear scaling regime.")
    Eff256Gpu = sourced(0.70, pc.BOOK_SCALING_EFFICIENCY_TIERS, name="Scaling Efficiency (256 GPUs)", description="Communication begins to reduce scaling efficiency.")
    Eff1024Gpu = sourced(0.50, pc.BOOK_SCALING_EFFICIENCY_TIERS, name="Scaling Efficiency (1024 GPUs)", description="Significant communication overhead at 1k GPUs.")
    Eff8192Gpu = sourced(0.35, pc.MEGASCALE, name="Scaling Efficiency (8192 GPUs)", description="Illustrative scaling efficiency at 8192 GPUs for LLM training.")


class Overheads(Registry):
    PipelineBubble = sourced(0.05, pc.BOOK_OVERHEAD_BUDGETS, name="Pipeline bubble overhead", description="Pipeline-parallel bubble overhead (well-tuned).")
    Checkpoint = sourced(0.03, pc.BOOK_OVERHEAD_BUDGETS, name="Checkpoint overhead", description="Async checkpointing overhead fraction.")
    FailureRecovery = sourced(0.10, pc.BOOK_OVERHEAD_BUDGETS, name="Failure recovery overhead", description="Failure and restart overhead at 10k+ GPU scale.")
    Maintenance = sourced(0.05, pc.BOOK_OVERHEAD_BUDGETS, name="Maintenance overhead", description="Rolling upgrade and maintenance windows.")


class Chinchilla(Registry):
    TokensPerParam = sourced(20, pc.CHINCHILLA, name="Compute-Optimal Token Ratio", description="Optimal training tokens per parameter (D ≈ 20P).")
    ComputeConstant = sourced(6, pc.CHINCHILLA, name="Training Compute Constant (C ≈ 6PD)", description="Training FLOPs multiplier (6PD).")


class Communication(Registry):
    RingAllreduceFactor = sourced(2, pc.GIBIANSKY_ALLREDUCE, name="AllReduce factor", description="Ring AllReduce communication multiplier (2×).")


class BatchSize(Registry):
    """McCandlish et al. (2018) critical batch size estimates."""
    Bert = 256
    Gpt3 = 4096
    Default = 1024


class Energy(Registry):
    """Simplified pedagogical energy hierarchy for the sustainability chapter.

    Architecture-class EFFECTIVE energy per FLOP (CPU->ASIC) and per-byte
    data-movement cost (register->network). Order-of-magnitude teaching figures,
    distinct from the device-level Horowitz raw-MAC/per-access constants in
    ``core.constants`` (e.g. ``ENERGY_FLOP_FP32_PJ``). DRAM per-byte is NOT
    duplicated here -- it uses the canonical device value
    ``constants.ENERGY_DRAM_PJ_PER_BYTE`` (160).
    """
    # Architecture-class effective efficiency (pJ/FLOP)
    EffCpuPjFlop = sourced(100, pc.BOOK_ENERGY_HIERARCHY, name="CPU energy efficiency (pJ/FLOP)", description="General-purpose CPU effective energy per FLOP.")
    EffGpuPjFlop = sourced(10, pc.BOOK_ENERGY_HIERARCHY, name="GPU energy efficiency (pJ/FLOP)", description="GPU dense-tensor effective energy per FLOP.")
    EffTpuPjFlop = sourced(1, pc.BOOK_ENERGY_HIERARCHY, name="TPU energy efficiency (pJ/FLOP)", description="TPU / systolic-array effective energy per FLOP.")
    EffAsicPjFlop = sourced(0.1, pc.BOOK_ENERGY_HIERARCHY, name="ASIC energy efficiency (pJ/FLOP)", description="Custom low-precision ASIC effective energy per operation.")
    # Per-byte data-movement hierarchy (pJ/byte); DRAM uses constants.ENERGY_DRAM_PJ_PER_BYTE
    MoveRegPjByte = sourced(0.1, pc.BOOK_ENERGY_HIERARCHY, name="Register move energy (pJ/byte)", description="Per-byte register-file access energy.")
    MoveL1PjByte = sourced(1, pc.BOOK_ENERGY_HIERARCHY, name="L1 cache move energy (pJ/byte)", description="Per-byte L1 cache access energy.")
    MoveL2PjByte = sourced(5, pc.BOOK_ENERGY_HIERARCHY, name="L2 cache move energy (pJ/byte)", description="Per-byte L2 cache access energy.")
    MoveNvmePjByte = sourced(1000, pc.BOOK_ENERGY_HIERARCHY, name="NVMe move energy (pJ/byte)", description="Per-byte NVMe SSD access energy.")
    MoveNetPjByte = sourced(10000, pc.BOOK_ENERGY_HIERARCHY, name="Network move energy (pJ/byte)", description="Per-byte network transfer energy (lower bound).")


class Literature(Registry):
    """Registry namespace for Literature."""
    Training = Training
    Scaling = Scaling
    Overheads = Overheads
    Chinchilla = Chinchilla
    Communication = Communication
    BatchSize = BatchSize
    Energy = Energy
