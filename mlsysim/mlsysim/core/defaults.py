"""Simulation parameters and tuneable defaults.

These are reasonable starting points for analytical modeling — override them
for your specific scenario. Every value cites its source.
"""

from .units import USD, ureg, GB, TB, hour, count, day
from .provenance import TraceableConstant, fleet_mttf_hours
from . import appendix_lineage
from .provenance_catalog import (
    BOOK_CLUSTER_TIERS,
    BOOK_CLOUD_PRICING_2024,
    BOOK_DGX_GPUS_PER_HOST,
    BOOK_FABRIC_LATENCY,
    BOOK_ILLUSTRATIVE_IOWA_CARBON,
    BOOK_OVERHEAD_BUDGETS,
    BOOK_RACK_POWER,
    BOOK_RECOVERY_ASSUMPTIONS,
    BOOK_SCALING_EFFICIENCY_TIERS,
    BOOK_SCALING_RULE_OF_THUMB,
    BOOK_WUE_ANCHORS,
    CHINCHILLA,
    ETHERNET_400G_GBS,
    ETHERNET_800G_GBS,
    GIBIANSKY_ALLREDUCE,
    IEA_WEO_2023,
    INFINIBAND_HDR_GBS,
    INFINIBAND_NDR_GBS,
    INFINIBAND_XDR_GBS,
    MEGASCALE,
    MFU_INFERENCE_BATCHED_LIT,
    MEGATRON_OVERLAP,
    PALM_MFU,
    POPE_INFERENCE,
    ROCE_100G_GBS,
    UPTIME_PUE_2022,
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

# Recovery time assumptions (seconds) — appendix-facing
HEARTBEAT_TIMEOUT_S = TraceableConstant(
    30,
    name="Heartbeat timeout",
    description="Failure detection latency before reschedule.",
    source=BOOK_RECOVERY_ASSUMPTIONS.ref,
    provenance=BOOK_RECOVERY_ASSUMPTIONS,
    kind=BOOK_RECOVERY_ASSUMPTIONS.kind,
)
RESCHEDULE_TIME_S = TraceableConstant(
    60,
    name="Reschedule time",
    description="Time to allocate a replacement node after failure detection.",
    source=BOOK_RECOVERY_ASSUMPTIONS.ref,
    provenance=BOOK_RECOVERY_ASSUMPTIONS,
    kind=BOOK_RECOVERY_ASSUMPTIONS.kind,
)
CHECKPOINT_WRITE_BW_GBS = TraceableConstant(
    100,
    name="Checkpoint write bandwidth",
    description="Aggregate checkpoint write bandwidth to storage (GB/s).",
    source=BOOK_RECOVERY_ASSUMPTIONS.ref,
    provenance=BOOK_RECOVERY_ASSUMPTIONS,
    kind=BOOK_RECOVERY_ASSUMPTIONS.kind,
)

# --- Cluster Scale References ---
# Editorial tier sizes for Volume II worked examples (not from a single deployment).
CLUSTER_SMALL_GPUS = TraceableConstant(
    256,
    name="Small cluster GPU count",
    description="Research-lab scale tier for fleet napkin math.",
    source=BOOK_CLUSTER_TIERS.ref,
    provenance=BOOK_CLUSTER_TIERS,
    kind=BOOK_CLUSTER_TIERS.kind,
)
CLUSTER_MEDIUM_GPUS = TraceableConstant(
    2_048,
    name="Medium cluster GPU count",
    description="Medium production tier.",
    source=BOOK_CLUSTER_TIERS.ref,
    provenance=BOOK_CLUSTER_TIERS,
    kind=BOOK_CLUSTER_TIERS.kind,
)
CLUSTER_LARGE_GPUS = TraceableConstant(
    8_192,
    name="Large cluster GPU count",
    description="Large training cluster tier; failure becomes steady state.",
    source=BOOK_CLUSTER_TIERS.ref,
    provenance=BOOK_CLUSTER_TIERS,
    kind=BOOK_CLUSTER_TIERS.kind,
)
CLUSTER_MEGA_GPUS = TraceableConstant(
    100_000,
    name="Mega cluster GPU count",
    description="Hyperscale fleet tier for order-of-magnitude examples.",
    source=BOOK_CLUSTER_TIERS.ref,
    provenance=BOOK_CLUSTER_TIERS,
    kind=BOOK_CLUSTER_TIERS.kind,
)

# Fleet topology assumptions (override for non-DGX node counts).
GPUS_PER_HOST = TraceableConstant(
    8,
    name="GPUs per host",
    description="Accelerators per DGX-class training node.",
    source=BOOK_DGX_GPUS_PER_HOST.ref,
    provenance=BOOK_DGX_GPUS_PER_HOST,
    kind=BOOK_DGX_GPUS_PER_HOST.kind,
)
ALLREDUCE_FACTOR = TraceableConstant(
    2,
    name="AllReduce factor",
    description="Ring AllReduce communication multiplier (2×).",
    source=GIBIANSKY_ALLREDUCE.ref,
    url=GIBIANSKY_ALLREDUCE.url,
    provenance=GIBIANSKY_ALLREDUCE,
    kind=GIBIANSKY_ALLREDUCE.kind,
)

# --- Cloud TPU Pod (reference fleet envelope) ---
TPU_POD_CHIPS = 4096
TPU_POD_MEM = 131 * TB
TPU_POD_POWER = 3 * ureg.megawatt

# --- Inter-Node Network (Fleet-Scale Byte Rates) ---
# Byte-per-second equivalents for bandwidth calculations.
# These complement the Gbps values defined in units.py for bit-rate contexts.
INFINIBAND_NDR_BW_GBS = TraceableConstant(
    50,
    name="InfiniBand NDR bandwidth (GB/s)",
    description="Per-port byte bandwidth for NDR.",
    source=INFINIBAND_NDR_GBS.ref,
    url=INFINIBAND_NDR_GBS.url,
    provenance=INFINIBAND_NDR_GBS,
    kind=INFINIBAND_NDR_GBS.kind,
)
INFINIBAND_HDR_BW_GBS = TraceableConstant(
    25,
    name="InfiniBand HDR bandwidth (GB/s)",
    description="Per-port byte bandwidth for HDR.",
    source=INFINIBAND_HDR_GBS.ref,
    url=INFINIBAND_HDR_GBS.url,
    provenance=INFINIBAND_HDR_GBS,
    kind=INFINIBAND_HDR_GBS.kind,
)
INFINIBAND_XDR_BW_GBS = TraceableConstant(
    100,
    name="InfiniBand XDR bandwidth (GB/s)",
    description="Per-port byte bandwidth for XDR.",
    source=INFINIBAND_XDR_GBS.ref,
    url=INFINIBAND_XDR_GBS.url,
    provenance=INFINIBAND_XDR_GBS,
    kind=INFINIBAND_XDR_GBS.kind,
)
ETHERNET_400G_BW_GBS = TraceableConstant(
    50,
    name="400 GbE bandwidth (GB/s)",
    description="Byte bandwidth for 400 GbE.",
    source=ETHERNET_400G_GBS.ref,
    provenance=ETHERNET_400G_GBS,
    kind=ETHERNET_400G_GBS.kind,
)
ETHERNET_800G_BW_GBS = TraceableConstant(
    100,
    name="800 GbE bandwidth (GB/s)",
    description="Byte bandwidth for 800 GbE.",
    source=ETHERNET_800G_GBS.ref,
    provenance=ETHERNET_800G_GBS,
    kind=ETHERNET_800G_GBS.kind,
)
ROCE_100G_BW_GBS = TraceableConstant(
    12.5,
    name="100 GbE RoCE bandwidth (GB/s)",
    description="Byte bandwidth for 100 GbE RoCE.",
    source=ROCE_100G_GBS.ref,
    provenance=ROCE_100G_GBS,
    kind=ROCE_100G_GBS.kind,
)

# Communication model parameters (α-β model) — appendix-facing
IB_NDR_LATENCY_US = TraceableConstant(
    5,
    name="InfiniBand NDR latency (μs)",
    description="One-way α latency for NDR fabrics.",
    source=BOOK_FABRIC_LATENCY.ref,
    provenance=BOOK_FABRIC_LATENCY,
    kind=BOOK_FABRIC_LATENCY.kind,
)
IB_HDR_LATENCY_US = TraceableConstant(
    7,
    name="InfiniBand HDR latency (μs)",
    description="One-way α latency for HDR fabrics.",
    source=BOOK_FABRIC_LATENCY.ref,
    provenance=BOOK_FABRIC_LATENCY,
    kind=BOOK_FABRIC_LATENCY.kind,
)
ROCE_LATENCY_US = TraceableConstant(
    10,
    name="RoCE latency (μs)",
    description="One-way α latency for RoCE v2.",
    source=BOOK_FABRIC_LATENCY.ref,
    provenance=BOOK_FABRIC_LATENCY,
    kind=BOOK_FABRIC_LATENCY.kind,
)
TCP_LATENCY_US = TraceableConstant(
    50,
    name="TCP latency (μs)",
    description="One-way α latency for TCP over Ethernet.",
    source=BOOK_FABRIC_LATENCY.ref,
    provenance=BOOK_FABRIC_LATENCY,
    kind=BOOK_FABRIC_LATENCY.kind,
)

# --- Sustainability ---
# Power Usage Effectiveness (PUE) — total facility power / IT equipment power
PUE_LIQUID_COOLED = TraceableConstant(
    1.06,
    name="PUE (Liquid-Cooled)",
    description="Best-in-class liquid-cooled AI datacenter PUE.",
    source=UPTIME_PUE_2022.ref,
    provenance=UPTIME_PUE_2022,
    kind=UPTIME_PUE_2022.kind,
)
PUE_BEST_AIR = TraceableConstant(
    1.12,
    name="PUE (Best Air-Cooled)",
    description="Best-in-class air-cooled hyperscale datacenter PUE.",
    source=UPTIME_PUE_2022.ref,
    provenance=UPTIME_PUE_2022,
    kind=UPTIME_PUE_2022.kind,
)
PUE_TYPICAL = TraceableConstant(
    1.40,
    name="PUE (Industry Average)",
    description="Industry average traditional datacenter PUE.",
    source=UPTIME_PUE_2022.ref,
    provenance=UPTIME_PUE_2022,
    kind=UPTIME_PUE_2022.kind,
)
PUE_LEGACY = TraceableConstant(
    1.58,
    name="PUE (Legacy Air-Cooled)",
    description="Older enterprise datacenter PUE tier.",
    source=UPTIME_PUE_2022.ref,
    provenance=UPTIME_PUE_2022,
    kind=UPTIME_PUE_2022.kind,
)
PUE_STATE_OF_ART = 1.10            # Modern highly optimized datacenter benchmark

# Water Usage Effectiveness (WUE) — liters per kWh — appendix-facing
WUE_AIR_COOLED = TraceableConstant(
    0.5,
    name="WUE (air-cooled)",
    description="Water usage effectiveness for air-cooled facilities.",
    source=BOOK_WUE_ANCHORS.ref,
    provenance=BOOK_WUE_ANCHORS,
    kind=BOOK_WUE_ANCHORS.kind,
)
WUE_EVAPORATIVE = TraceableConstant(
    1.8,
    name="WUE (evaporative)",
    description="Water usage effectiveness for evaporative cooling.",
    source=BOOK_WUE_ANCHORS.ref,
    provenance=BOOK_WUE_ANCHORS,
    kind=BOOK_WUE_ANCHORS.kind,
)
WUE_LIQUID = TraceableConstant(
    0.0,
    name="WUE (liquid-cooled)",
    description="Closed-loop liquid cooling (near-zero WUE).",
    source=BOOK_WUE_ANCHORS.ref,
    provenance=BOOK_WUE_ANCHORS,
    kind=BOOK_WUE_ANCHORS.kind,
)

# Regional carbon intensity (gCO2 per kWh) — IEA WEO 2023 unless noted
CARBON_US_AVG_GCO2_KWH = TraceableConstant(
    429,
    name="Carbon Intensity (US Average)",
    description="US national average grid carbon intensity in gCO2/kWh.",
    source=IEA_WEO_2023.ref,
    url=IEA_WEO_2023.url,
    provenance=IEA_WEO_2023,
    kind=IEA_WEO_2023.kind,
)
CARBON_EU_AVG_GCO2_KWH = TraceableConstant(
    270,
    name="Carbon Intensity (EU Average)",
    description="EU average grid carbon intensity in gCO2/kWh.",
    source=IEA_WEO_2023.ref,
    url=IEA_WEO_2023.url,
    provenance=IEA_WEO_2023,
    kind=IEA_WEO_2023.kind,
)
CARBON_QUEBEC_GCO2_KWH = TraceableConstant(
    20,
    name="Carbon Intensity (Quebec)",
    description="Quebec grid carbon intensity in gCO2/kWh (hydroelectric dominant).",
    source=IEA_WEO_2023.ref,
    url=IEA_WEO_2023.url,
    provenance=IEA_WEO_2023,
    kind=IEA_WEO_2023.kind,
)
CARBON_FRANCE_GCO2_KWH = TraceableConstant(
    50,
    name="Carbon Intensity (France)",
    description="France grid carbon intensity in gCO2/kWh (nuclear dominant).",
    source=IEA_WEO_2023.ref,
    url=IEA_WEO_2023.url,
    provenance=IEA_WEO_2023,
    kind=IEA_WEO_2023.kind,
)
CARBON_IOWA_GCO2_KWH = TraceableConstant(
    680,
    name="Carbon Intensity (Iowa reference)",
    description="High-carbon US grid mix for tutorial contrast (not IEA country average).",
    source=BOOK_ILLUSTRATIVE_IOWA_CARBON.ref,
    provenance=BOOK_ILLUSTRATIVE_IOWA_CARBON,
    kind=BOOK_ILLUSTRATIVE_IOWA_CARBON.kind,
)
CARBON_POLAND_GCO2_KWH = TraceableConstant(
    820,
    name="Carbon Intensity (Poland)",
    description="Poland grid carbon intensity in gCO2/kWh (coal dominant).",
    source=IEA_WEO_2023.ref,
    url=IEA_WEO_2023.url,
    provenance=IEA_WEO_2023,
    kind=IEA_WEO_2023.kind,
)
CARBON_NORWAY_GCO2_KWH = TraceableConstant(
    10,
    name="Carbon Intensity (Norway)",
    description="Norway grid carbon intensity in gCO2/kWh (hydroelectric).",
    source=IEA_WEO_2023.ref,
    url=IEA_WEO_2023.url,
    provenance=IEA_WEO_2023,
    kind=IEA_WEO_2023.kind,
)

# Power density — appendix-facing
RACK_POWER_TRADITIONAL_KW = TraceableConstant(
    12,
    name="Rack power (traditional)",
    description="Traditional enterprise rack power (kW).",
    source=BOOK_RACK_POWER.ref,
    provenance=BOOK_RACK_POWER,
    kind=BOOK_RACK_POWER.kind,
)
RACK_POWER_AI_TYPICAL_KW = TraceableConstant(
    70,
    name="Rack power (AI typical)",
    description="Typical AI cluster rack power (kW).",
    source=BOOK_RACK_POWER.ref,
    provenance=BOOK_RACK_POWER,
    kind=BOOK_RACK_POWER.kind,
)
RACK_POWER_AI_HIGH_KW = TraceableConstant(
    100,
    name="Rack power (AI high)",
    description="High-density AI rack power (kW).",
    source=BOOK_RACK_POWER.ref,
    provenance=BOOK_RACK_POWER,
    kind=BOOK_RACK_POWER.kind,
)
AIR_COOLING_LIMIT_KW = TraceableConstant(
    30,
    name="Air cooling limit (kW)",
    description="Approximate rack power where air cooling becomes impractical.",
    source=BOOK_RACK_POWER.ref,
    provenance=BOOK_RACK_POWER,
    kind=BOOK_RACK_POWER.kind,
)

# --- MFU and Scaling Efficiency References ---
# Model FLOPS Utilization (MFU) — actual FLOPS / peak FLOPS
MFU_TRAINING_LOW = TraceableConstant(
    0.30,
    name="MFU Training (Lower Bound)",
    description="Lower bound MFU for well-optimized large-model training.",
    source=PALM_MFU.ref,
    url=PALM_MFU.url,
    provenance=PALM_MFU,
    kind=PALM_MFU.kind,
)
MFU_TRAINING_HIGH = TraceableConstant(
    0.50,
    name="MFU Training (Upper Bound)",
    description="Upper bound MFU for excellent large-model training runs.",
    source=PALM_MFU.ref,
    url=PALM_MFU.url,
    provenance=PALM_MFU,
    kind=PALM_MFU.kind,
)
MFU_INFERENCE_BATCH1 = TraceableConstant(
    0.05,
    name="MFU Inference (Batch 1)",
    description="MFU for single-request inference, heavily memory-bandwidth-bound.",
    source=POPE_INFERENCE.ref,
    url=POPE_INFERENCE.url,
    provenance=POPE_INFERENCE,
    kind=POPE_INFERENCE.kind,
)
MFU_INFERENCE_BATCHED = TraceableConstant(
    0.40,
    name="MFU Inference (Batched)",
    description="Illustrative MFU upper bound for large-batch inference.",
    source=MFU_INFERENCE_BATCHED_LIT.ref,
    url=MFU_INFERENCE_BATCHED_LIT.url,
    provenance=MFU_INFERENCE_BATCHED_LIT,
    kind=MFU_INFERENCE_BATCHED_LIT.kind,
)

# --- Software Tax ---
# Latency overhead for a single kernel launch on a modern GPU.
# Source: NVIDIA (2024), "CUDA C++ Programming Guide."
KERNEL_LAUNCH_LATENCY_US = 15.0    # 15 μs typical launch overhead
FRAMEWORK_LAYER_TAX_MS = 0.01      # 10 μs typical framework tax per model layer (assumes graph compilation/fused kernels)

# Scaling efficiency η = T_1 / (N × T_N)
SCALING_EFF_32GPU = TraceableConstant(
    0.90,
    name="Scaling Efficiency (32 GPUs)",
    description="Near-linear scaling regime.",
    source=BOOK_SCALING_EFFICIENCY_TIERS.ref,
    provenance=BOOK_SCALING_EFFICIENCY_TIERS,
    kind=BOOK_SCALING_EFFICIENCY_TIERS.kind,
)
SCALING_EFF_256GPU = TraceableConstant(
    0.70,
    name="Scaling Efficiency (256 GPUs)",
    description="Communication begins to reduce scaling efficiency.",
    source=BOOK_SCALING_EFFICIENCY_TIERS.ref,
    provenance=BOOK_SCALING_EFFICIENCY_TIERS,
    kind=BOOK_SCALING_EFFICIENCY_TIERS.kind,
)
SCALING_EFF_1024GPU = TraceableConstant(
    0.50,
    name="Scaling Efficiency (1024 GPUs)",
    description="Significant communication overhead at 1k GPUs.",
    source=BOOK_SCALING_EFFICIENCY_TIERS.ref,
    provenance=BOOK_SCALING_EFFICIENCY_TIERS,
    kind=BOOK_SCALING_EFFICIENCY_TIERS.kind,
)
SCALING_EFF_8192GPU = TraceableConstant(
    0.35,
    name="Scaling Efficiency (8192 GPUs)",
    description="Illustrative scaling efficiency at 8192 GPUs for LLM training.",
    source=f"{PALM_MFU.ref}; {MEGASCALE.ref}",
    provenance=MEGASCALE,
    kind=MEGASCALE.kind,
)

# Overhead budgets (fraction of wall time) — appendix-facing
OVERHEAD_PIPELINE_BUBBLE = TraceableConstant(
    0.05,
    name="Pipeline bubble overhead",
    description="Pipeline-parallel bubble overhead (well-tuned).",
    source=BOOK_OVERHEAD_BUDGETS.ref,
    provenance=BOOK_OVERHEAD_BUDGETS,
    kind=BOOK_OVERHEAD_BUDGETS.kind,
)
OVERHEAD_CHECKPOINT = TraceableConstant(
    0.03,
    name="Checkpoint overhead",
    description="Async checkpointing overhead fraction.",
    source=BOOK_OVERHEAD_BUDGETS.ref,
    provenance=BOOK_OVERHEAD_BUDGETS,
    kind=BOOK_OVERHEAD_BUDGETS.kind,
)
OVERHEAD_FAILURE_RECOVERY = TraceableConstant(
    0.10,
    name="Failure recovery overhead",
    description="Failure and restart overhead at 10k+ GPU scale.",
    source=BOOK_OVERHEAD_BUDGETS.ref,
    provenance=BOOK_OVERHEAD_BUDGETS,
    kind=BOOK_OVERHEAD_BUDGETS.kind,
)
OVERHEAD_MAINTENANCE = TraceableConstant(
    0.05,
    name="Maintenance overhead",
    description="Rolling upgrade and maintenance windows.",
    source=BOOK_OVERHEAD_BUDGETS.ref,
    provenance=BOOK_OVERHEAD_BUDGETS,
    kind=BOOK_OVERHEAD_BUDGETS.kind,
)

# --- Scaling Laws (Chinchilla Physics) ---
# Source: Hoffmann et al. (2022), "Training Compute-Optimal Large Language Models"
CHINCHILLA_TOKENS_PER_PARAM = TraceableConstant(
    20,
    name="Compute-Optimal Token Ratio",
    description="The optimal number of training tokens per model parameter (D ≈ 20P) to minimize loss for a given compute budget.",
    source=CHINCHILLA.ref,
    url=CHINCHILLA.url,
    provenance=CHINCHILLA,
    kind=CHINCHILLA.kind,
)

CHINCHILLA_COMPUTE_CONSTANT = TraceableConstant(
    6,
    name="Training Compute Constant (C ≈ 6PD)",
    description="The multiplier for calculating total training FLOPs. 2 FLOPs per parameter for the forward pass, and 4 FLOPs for the backward pass.",
    source=CHINCHILLA.ref,
    url=CHINCHILLA.url,
    provenance=CHINCHILLA,
    kind=CHINCHILLA.kind,
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

# Cloud pricing (2024 baselines) — magnitudes are appendix-facing
CLOUD_EGRESS_PER_GB = 0.09 * USD / GB
CLOUD_GPU_TRAINING_PER_HOUR = 4.0 * USD / hour
CLOUD_GPU_INFERENCE_PER_HOUR = 2.5 * USD / hour

appendix_lineage.register_quantity_provenance(
    {
        "CLOUD_EGRESS_PER_GB": BOOK_CLOUD_PRICING_2024,
        "CLOUD_GPU_TRAINING_PER_HOUR": BOOK_CLOUD_PRICING_2024,
        "CLOUD_GPU_INFERENCE_PER_HOUR": BOOK_CLOUD_PRICING_2024,
        "CLOUD_ELECTRICITY_PER_KWH": BOOK_CLOUD_PRICING_2024,
    }
)
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
    source=BOOK_SCALING_RULE_OF_THUMB.ref,
    provenance=BOOK_SCALING_RULE_OF_THUMB,
    kind=BOOK_SCALING_RULE_OF_THUMB.kind,
)

# Default communication overlap efficiency (e.g., Megatron-LM can overlap ~85% of communication)
DEFAULT_OVERLAP_EFFICIENCY = TraceableConstant(
    0.85,
    name="Communication Overlap Efficiency",
    description="The fraction of network communication time that can be successfully hidden behind compute operations.",
    source=MEGATRON_OVERLAP.ref,
    url=MEGATRON_OVERLAP.url,
    provenance=MEGATRON_OVERLAP,
    kind=MEGATRON_OVERLAP.kind,
)

# Default compute efficiency (MFU baseline)
DEFAULT_COMPUTE_EFFICIENCY = TraceableConstant(
    0.50,
    name="Baseline Model FLOPs Utilization (MFU)",
    description="A highly optimized large language model typically achieves around 50% MFU due to communication overhead and memory bandwidth constraints.",
    source=PALM_MFU.ref,
    url=PALM_MFU.url,
    provenance=PALM_MFU,
    kind=PALM_MFU.kind,
)
