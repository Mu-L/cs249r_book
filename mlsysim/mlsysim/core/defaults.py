"""Simulation parameters and tuneable defaults.

These are reasonable starting points for analytical modeling — override them
for your specific scenario. Every value cites its source.
"""

from .units import USD, ureg, GB, TB, hour, count, day
from .provenance import (
    TraceableConstant,
    SOURCE_CONVENTION,
    SOURCE_ILLUSTRATIVE,
    SOURCE_INDUSTRY_REPORT,
    SOURCE_LITERATURE,
    fleet_mttf_hours,
)

# --- Reliability (Component MTTF) ---
# Order-of-magnitude steady-state MTTF; see appendix_reliability @tbl-component-fit.
GPU_MTTF_HOURS = fleet_mttf_hours(50_000, component="GPU", failure_mode="die defect, thermal fatigue")
NIC_MTTF_HOURS = fleet_mttf_hours(150_000, component="NIC", failure_mode="transceiver degradation")
PSU_MTTF_HOURS = fleet_mttf_hours(100_000, component="PSU", failure_mode="capacitor aging")
PCIE_SWITCH_MTTF_HOURS = fleet_mttf_hours(200_000, component="PCIe switch", failure_mode="solder joint, ESD")
CABLE_MTTF_HOURS = fleet_mttf_hours(50_000, component="optical cable / transceiver", failure_mode="fiber bend, connector wear")
TOR_SWITCH_MTTF_HOURS = fleet_mttf_hours(300_000, component="top-of-rack switch", failure_mode="ASIC, fan bearing")
HBM_MTTF_HOURS = fleet_mttf_hours(200_000, component="HBM", failure_mode="bit-flip accumulation, TSV")

# Silent Data Corruption (SDC) Assumptions
P_SDC_PER_GPU_HR = 1e-6

# Recovery time assumptions (seconds)
HEARTBEAT_TIMEOUT_S = 30            # Failure detection latency
RESCHEDULE_TIME_S = 60              # Time to allocate replacement node
CHECKPOINT_WRITE_BW_GBS = 100       # Aggregate storage write BW for checkpoints (GB/s)

# --- Cluster Scale References ---
# Editorial tier sizes for Volume II worked examples (not from a single deployment).
CLUSTER_SMALL_GPUS = TraceableConstant(
    256,
    name="Small cluster GPU count",
    description="Research-lab scale tier for fleet napkin math.",
    citation="MLSysBook editorial convention",
    source_type=SOURCE_CONVENTION,
    bib_keys="kokolis2025",
    last_verified="2025-03-06",
)
CLUSTER_MEDIUM_GPUS = TraceableConstant(
    2_048,
    name="Medium cluster GPU count",
    description="Medium production tier.",
    citation="MLSysBook editorial convention",
    source_type=SOURCE_CONVENTION,
    last_verified="2025-03-06",
)
CLUSTER_LARGE_GPUS = TraceableConstant(
    8_192,
    name="Large cluster GPU count",
    description="Large training cluster tier; failure becomes steady state.",
    citation="MLSysBook editorial convention",
    source_type=SOURCE_CONVENTION,
    bib_keys="kokolis2025",
    last_verified="2025-03-06",
)
CLUSTER_MEGA_GPUS = TraceableConstant(
    100_000,
    name="Mega cluster GPU count",
    description="Hyperscale fleet tier for order-of-magnitude examples.",
    citation="MLSysBook editorial convention",
    source_type=SOURCE_CONVENTION,
    last_verified="2025-03-06",
)

# Fleet topology assumptions (override for non-DGX node counts).
GPUS_PER_HOST = 8
ALLREDUCE_FACTOR = 2

# --- Cloud TPU Pod (reference fleet envelope) ---
TPU_POD_CHIPS = 4096
TPU_POD_MEM = 131 * TB
TPU_POD_POWER = 3 * ureg.megawatt

# --- Inter-Node Network (Fleet-Scale Byte Rates) ---
# Byte-per-second equivalents for bandwidth calculations.
# These complement the Gbps values defined in units.py for bit-rate contexts.
INFINIBAND_NDR_BW_GBS = 50         # 400 Gbps / 8 = 50 GB/s per port
INFINIBAND_HDR_BW_GBS = 25         # 200 Gbps / 8 = 25 GB/s per port
INFINIBAND_XDR_BW_GBS = 100        # 800 Gbps / 8 = 100 GB/s per port (2025)
ETHERNET_400G_BW_GBS = 50          # 400 GbE = 50 GB/s
ETHERNET_800G_BW_GBS = 100         # 800 GbE = 100 GB/s (2025)
ROCE_100G_BW_GBS = 12.5            # 100 GbE RoCE = 12.5 GB/s

# Communication model parameters (α-β model)
IB_NDR_LATENCY_US = 5              # InfiniBand NDR one-way latency (μs)
IB_HDR_LATENCY_US = 7              # InfiniBand HDR one-way latency (μs)
ROCE_LATENCY_US = 10               # RoCE v2 one-way latency (μs)
TCP_LATENCY_US = 50                # TCP/IP over Ethernet one-way latency (μs)

# --- Sustainability ---
# Power Usage Effectiveness (PUE) — total facility power / IT equipment power
PUE_LIQUID_COOLED = TraceableConstant(
    1.06,
    name="PUE (Liquid-Cooled)",
    description="Best-in-class liquid-cooled AI datacenter PUE.",
    citation="Uptime Institute Global Data Center Survey 2022",
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys="davis2022uptime; thegreengrid2007pue",
    last_verified="2025-03-06",
)
PUE_BEST_AIR = TraceableConstant(
    1.12,
    name="PUE (Best Air-Cooled)",
    description="Best-in-class air-cooled hyperscale datacenter PUE.",
    citation="Uptime Institute Global Data Center Survey 2022",
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys="davis2022uptime",
    last_verified="2025-03-06",
)
PUE_TYPICAL = TraceableConstant(
    1.40,
    name="PUE (Industry Average)",
    description="Industry average traditional datacenter PUE.",
    citation="Uptime Institute Global Data Center Survey 2022",
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys="davis2022uptime",
    last_verified="2025-03-06",
)
PUE_LEGACY = TraceableConstant(
    1.58,
    name="PUE (Legacy Air-Cooled)",
    description="Older enterprise datacenter PUE tier.",
    citation="Uptime Institute Global Data Center Survey 2022",
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys="davis2022uptime",
    last_verified="2025-03-06",
)
PUE_STATE_OF_ART = 1.10            # Modern highly optimized datacenter benchmark

# Water Usage Effectiveness (WUE) — liters per kWh
WUE_AIR_COOLED = 0.5               # Air-cooled (minimal water)
WUE_EVAPORATIVE = 1.8              # Evaporative cooling towers
WUE_LIQUID = 0.0                   # Closed-loop liquid cooling (near zero)

# Regional carbon intensity (gCO2 per kWh) — Source: IEA (2023)
_IEA_CARBON_CITATION = "IEA World Energy Outlook 2023 (rounded gCO2/kWh)"
_IEA_CARBON_BIB = "iea2023weo"
_IEA_CARBON_URL = "https://www.iea.org/reports/world-energy-outlook-2023"
_IEA_VERIFIED = "2025-03-06"

CARBON_US_AVG_GCO2_KWH = TraceableConstant(
    429,
    name="Carbon Intensity (US Average)",
    description="US national average grid carbon intensity in gCO2/kWh.",
    citation=_IEA_CARBON_CITATION,
    url=_IEA_CARBON_URL,
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys=_IEA_CARBON_BIB,
    last_verified=_IEA_VERIFIED,
)
CARBON_EU_AVG_GCO2_KWH = TraceableConstant(
    270,
    name="Carbon Intensity (EU Average)",
    description="EU average grid carbon intensity in gCO2/kWh.",
    citation=_IEA_CARBON_CITATION,
    url=_IEA_CARBON_URL,
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys=_IEA_CARBON_BIB,
    last_verified=_IEA_VERIFIED,
)
CARBON_QUEBEC_GCO2_KWH = TraceableConstant(
    20,
    name="Carbon Intensity (Quebec)",
    description="Quebec grid carbon intensity in gCO2/kWh (hydroelectric dominant).",
    citation=_IEA_CARBON_CITATION,
    url=_IEA_CARBON_URL,
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys=_IEA_CARBON_BIB,
    last_verified=_IEA_VERIFIED,
)
CARBON_FRANCE_GCO2_KWH = TraceableConstant(
    50,
    name="Carbon Intensity (France)",
    description="France grid carbon intensity in gCO2/kWh (nuclear dominant).",
    citation=_IEA_CARBON_CITATION,
    url=_IEA_CARBON_URL,
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys=_IEA_CARBON_BIB,
    last_verified=_IEA_VERIFIED,
)
CARBON_IOWA_GCO2_KWH = TraceableConstant(
    680,
    name="Carbon Intensity (Iowa reference)",
    description="High-carbon US grid mix for tutorial contrast (not IEA country average).",
    citation="MLSysBook illustrative regional contrast",
    source_type=SOURCE_ILLUSTRATIVE,
    last_verified=_IEA_VERIFIED,
)
CARBON_POLAND_GCO2_KWH = TraceableConstant(
    820,
    name="Carbon Intensity (Poland)",
    description="Poland grid carbon intensity in gCO2/kWh (coal dominant).",
    citation=_IEA_CARBON_CITATION,
    url=_IEA_CARBON_URL,
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys=_IEA_CARBON_BIB,
    last_verified=_IEA_VERIFIED,
)
CARBON_NORWAY_GCO2_KWH = TraceableConstant(
    10,
    name="Carbon Intensity (Norway)",
    description="Norway grid carbon intensity in gCO2/kWh (hydroelectric).",
    citation=_IEA_CARBON_CITATION,
    url=_IEA_CARBON_URL,
    source_type=SOURCE_INDUSTRY_REPORT,
    bib_keys=_IEA_CARBON_BIB,
    last_verified=_IEA_VERIFIED,
)

# Power density
RACK_POWER_TRADITIONAL_KW = 12     # Traditional datacenter rack (kW)
RACK_POWER_AI_TYPICAL_KW = 70      # AI cluster rack, current generation (kW)
RACK_POWER_AI_HIGH_KW = 100        # AI cluster rack, high-density (kW)
AIR_COOLING_LIMIT_KW = 30          # Approximate rack power where air cooling fails (kW)

# --- MFU and Scaling Efficiency References ---
# Model FLOPS Utilization (MFU) — actual FLOPS / peak FLOPS
MFU_TRAINING_LOW = TraceableConstant(
    0.30,
    name="MFU Training (Lower Bound)",
    description="Lower bound MFU for well-optimized large-model training.",
    citation="Chowdhery et al. (2022), PaLM; Narayanan et al. (2021), Megatron-LM",
    source_type=SOURCE_LITERATURE,
    bib_keys="chowdhery2022palm; narayanan2021",
    url="https://arxiv.org/abs/2204.02311",
    last_verified="2025-03-06",
)
MFU_TRAINING_HIGH = TraceableConstant(
    0.50,
    name="MFU Training (Upper Bound)",
    description="Upper bound MFU for excellent large-model training runs.",
    citation="Chowdhery et al. (2022), PaLM",
    source_type=SOURCE_LITERATURE,
    bib_keys="chowdhery2022palm",
    url="https://arxiv.org/abs/2204.02311",
    last_verified="2025-03-06",
)
MFU_INFERENCE_BATCH1 = TraceableConstant(
    0.05,
    name="MFU Inference (Batch 1)",
    description="MFU for single-request inference, heavily memory-bandwidth-bound.",
    citation="Pope et al. (2023), Efficiently Scaling Transformer Inference",
    source_type=SOURCE_LITERATURE,
    bib_keys="pope2023efficiently",
    url="https://proceedings.mlsys.org/paper_files/paper/2023/hash/c4be71ab8d24cdfb45e3d06dbfca2780-Abstract-mlsys2023.html",
    last_verified="2025-03-06",
)
MFU_INFERENCE_BATCHED = 0.40       # Inference at large batch size

# --- Software Tax ---
# Latency overhead for a single kernel launch on a modern GPU.
# Source: NVIDIA (2024), "CUDA C++ Programming Guide."
KERNEL_LAUNCH_LATENCY_US = 15.0    # 15 μs typical launch overhead
FRAMEWORK_LAYER_TAX_MS = 0.01      # 10 μs typical framework tax per model layer (assumes graph compilation/fused kernels)

# Scaling efficiency η = T_1 / (N × T_N)
SCALING_EFF_32GPU = 0.90           # Near-linear regime
SCALING_EFF_256GPU = 0.70          # Communication starts to bite
SCALING_EFF_1024GPU = 0.50         # Significant overhead
SCALING_EFF_8192GPU = TraceableConstant(
    0.35,
    name="Scaling Efficiency (8192 GPUs)",
    description="Illustrative scaling efficiency at 8192 GPUs for LLM training.",
    citation="Chowdhery et al. (2022); Jiang et al. (2024), MegaScale",
    source_type=SOURCE_LITERATURE,
    bib_keys="chowdhery2022palm; jiang2024megascale",
    last_verified="2025-03-06",
)

# Overhead budgets (fraction of wall time)
OVERHEAD_PIPELINE_BUBBLE = 0.05    # ~5% for well-tuned pipeline parallelism
OVERHEAD_CHECKPOINT = 0.03         # ~3% for optimized async checkpointing
OVERHEAD_FAILURE_RECOVERY = 0.10   # ~10% for failure and restart at 10K+ scale
OVERHEAD_MAINTENANCE = 0.05        # ~5% for rolling upgrades, maintenance windows

# --- Scaling Laws (Chinchilla Physics) ---
# Source: Hoffmann et al. (2022), "Training Compute-Optimal Large Language Models"
CHINCHILLA_TOKENS_PER_PARAM = TraceableConstant(
    20,
    name="Compute-Optimal Token Ratio",
    description="The optimal number of training tokens per model parameter (D ≈ 20P) to minimize loss for a given compute budget.",
    citation="Hoffmann et al. (2022). Training Compute-Optimal Large Language Models.",
    url="https://arxiv.org/abs/2203.15556",
    bib_keys="hoffmann2022chinchilla",
    last_verified="2025-03-06",
)

CHINCHILLA_COMPUTE_CONSTANT = TraceableConstant(
    6,
    name="Training Compute Constant (C ≈ 6PD)",
    description="The multiplier for calculating total training FLOPs. 2 FLOPs per parameter for the forward pass, and 4 FLOPs for the backward pass.",
    citation="Hoffmann et al. (2022). Training Compute-Optimal Large Language Models.",
    url="https://arxiv.org/abs/2203.15556",
    bib_keys="hoffmann2022chinchilla",
    last_verified="2025-03-06",
)

# --- Critical Batch Size (McCandlish et al. 2018) ---
# Source: McCandlish et al. (2018), "An Empirical Model of Large-Batch Training"
# Estimates for when Data Parallelism hits diminishing returns.
CRITICAL_BATCH_SIZE_BERT = 256
CRITICAL_BATCH_SIZE_GPT3 = 4096
CRITICAL_BATCH_SIZE_DEFAULT = 1024

# --- Orchestration & Queueing (Little's Law) ---
# Typical cluster utilization targets and arrival rates for scenarios.
TARGET_CLUSTER_UTILIZATION = 0.80  # 80% is high for shared research clusters
QUEUE_DISCIPLINE = "FIFO"          # First-In-First-Out (Baseline)
AVERAGE_RESEARCHER_JOB_DAYS = 2.0  # Median job length in research clusters

# --- Economics defaults ---
# Source: Barroso et al. (2018)
ANNUAL_MAINTENANCE_RATIO = 0.05      # 5% of CapEx per year
GPU_UNIT_COST_H100 = 30000 * USD     # NVIDIA H100 SXM (2024 street price)
GPU_UNIT_COST_A100 = 15000 * USD     # NVIDIA A100 SXM (2024 street price)
GPU_UNIT_COST_B200 = 40000 * USD     # NVIDIA B200 (2025 estimated)

# Default electricity price — Source: AWS US baseline (2024)
DEFAULT_KWH_PRICE = 0.12             # USD per kWh
CLOUD_ELECTRICITY_PER_KWH = 0.12 * USD / ureg.kilowatt_hour

# Cloud pricing (2024 baselines)
CLOUD_EGRESS_PER_GB = 0.09 * USD / GB
CLOUD_GPU_TRAINING_PER_HOUR = 4.0 * USD / hour
CLOUD_GPU_INFERENCE_PER_HOUR = 2.5 * USD / hour
TPU_V4_PER_HOUR = 4.0 * USD / hour

# Fleet economics references
FLEET_GPU_HOUR_COST_REF = 2.0 * USD / hour
FLEET_SPOT_GPU_HOUR_COST_REF = 0.70 * USD / hour
FLEET_INTERNAL_CHARGEBACK_PER_HOUR = 2.50 * USD / hour
CARBON_PER_GPU_HR_KG = 0.16 * ureg.kilogram

# Storage pricing (2024 baseline)
STORAGE_COST_S3_STD = 23 * USD / TB / ureg.month
STORAGE_COST_GLACIER = 1 * USD / TB / ureg.month
STORAGE_COST_NVME_LOW = 100 * USD / TB / ureg.month
STORAGE_COST_NVME_HIGH = 300 * USD / TB / ureg.month
RETRIEVAL_COST_GLACIER = 0.02 * USD / GB

# Labeling pricing (2024 estimates)
LABELING_COST_CROWD_LOW = 0.01 * USD
LABELING_COST_CROWD_HIGH = 0.05 * USD
LABELING_COST_BOX_LOW = 0.05 * USD
LABELING_COST_BOX_HIGH = 0.20 * USD
LABELING_COST_MEDICAL_LOW = 50 * USD
LABELING_COST_MEDICAL_HIGH = 200 * USD

# Infrastructure lead times
LEAD_TIME_GPU_MONTHS = 6
LEAD_TIME_SUBSTATION_MONTHS = 24
GRID_INTERCONNECTION_QUEUE_US_GW = 2000

# Reliability / monitoring thresholds
MEMORY_BIT_ERROR_RATE_PER_BIT = 1e-17
KS_TEST_COEFFICIENT = 1.36
PSI_WARN_THRESHOLD = 0.10
PSI_REVIEW_THRESHOLD = 0.20
PSI_CRITICAL_THRESHOLD = 0.25

# --- Quantization accuracy deltas ---
# Source: Gholami et al. (2021) survey medians
QUANT_ACCURACY_DELTA_INT8 = -0.005   # Median INT8 PTQ accuracy drop
QUANT_ACCURACY_DELTA_INT4 = -0.025   # Median INT4 GPTQ accuracy drop
QUANT_ACCURACY_DELTA_FP8 = -0.002    # FP8 (negligible for most models)

# --- Pruning accuracy ---
# Source: Blalock et al. (2020) survey
PRUNING_ACCURACY_THRESHOLD = 0.5     # Sparsity threshold where degradation accelerates
PRUNING_MILD_DELTA = -0.001          # Accuracy delta below threshold
PRUNING_STEEP_COEFFICIENT = 0.01     # Coefficient for exponential degradation above threshold
PRUNING_STEEP_EXPONENT = 2.0         # Exponent for degradation curve

# --- EfficiencyModel MFU adjustment (heuristic calibrations) ---
# These are empirically calibrated caps, NOT derived from first principles.
# Source: Dao et al. (2022) reports ~2-4x speedup for FlashAttention.
# Source: Chowdhery et al. (2022) PaLM reports MFU 0.46-0.57 for large Transformers.
MFU_FLASH_ATTENTION = 0.75           # Calibrated MFU for FlashAttention attention layers
MFU_FLASH_ATTENTION_CAP = 0.85      # Practical maximum for FlashAttention
MFU_FFN_CAP = 0.60                   # Practical maximum for FFN (GEMM-dominated)
MFU_CONV_CAP = 0.55                  # Practical maximum for convolution (im2col+GEMM)
HFU_MFU_RATIO = 1.1                  # HFU ≈ 1.1 × MFU (Chowdhery et al. 2022, PaLM)

# --- InferenceScalingModel ---
# Heuristic: average tokens per CoT reasoning step.
# Varies widely (10-1000+); 50 is a moderate default.
TOKENS_PER_REASONING_STEP = 50

# --- ScalingModel ---
# Conservative sustained MFU for GPU-day-to-FLOP conversion.
REFERENCE_MFU_SUSTAINED = 0.40

# --- ResponsibleEngineeringModel (heuristic calibration) ---
# DP-SGD slowdown model: slowdown ≈ 1 + k/ε.
# NOT derived from Abadi et al. (2016) — calibrated to match reported
# slowdowns: ~3x at ε=1.0, ~1.2x at ε=10.0.
DP_SGD_SLOWDOWN_COEFFICIENT = 2.0

# --- Engine Default Overrides ---

# Default scaling efficiency for parallel clusters
DEFAULT_SCALING_EFFICIENCY = TraceableConstant(
    0.90,
    name="Scaling Efficiency (η)",
    description="The efficiency of parallel scaling. A value of 0.90 means 90% of theoretical linear speedup is achieved.",
    citation="Common industry rule-of-thumb for highly optimized clusters."
)

# Default communication overlap efficiency (e.g., Megatron-LM can overlap ~85% of communication)
DEFAULT_OVERLAP_EFFICIENCY = TraceableConstant(
    0.85,
    name="Communication Overlap Efficiency",
    description="The fraction of network communication time that can be successfully hidden behind compute operations.",
    citation="Shoeybi et al. (2019). Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism.",
    url="https://arxiv.org/abs/1909.08053"
)

# Default compute efficiency (MFU baseline)
DEFAULT_COMPUTE_EFFICIENCY = TraceableConstant(
    0.50,
    name="Baseline Model FLOPs Utilization (MFU)",
    description="A highly optimized large language model typically achieves around 50% MFU due to communication overhead and memory bandwidth constraints.",
    citation="Chowdhery et al. (2022). PaLM: Scaling Language Modeling with Pathways.",
    url="https://arxiv.org/abs/2204.02311"
)
