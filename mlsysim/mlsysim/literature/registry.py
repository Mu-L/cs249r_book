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


class Literature(Registry):
    Training = Training
    Scaling = Scaling
    Overheads = Overheads
    Chinchilla = Chinchilla
    Communication = Communication
    BatchSize = BatchSize
