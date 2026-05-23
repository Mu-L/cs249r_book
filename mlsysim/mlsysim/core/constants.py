# constants.py
# The Analytical Engine of Machine Learning Systems
# 
# ⚠️ ARCHITECTURAL RULE ⚠️
# This file is strictly for universal physics (e.g., speed of light), standard units,
# and generalized economic baselines.
# 
# DO NOT add specific hardware numbers (like H100 memory bandwidth) or specific 
# model definitions (like GPT-3 parameter counts) here. 
#
# Hardware specifications belong in: `mlsysim/hardware/registry.py`
# Model specifications belong in: `mlsysim/models/registry.py`
#
# Measurement units live in units.py; tuneable simulation defaults live in
# defaults.py. This module re-exports both for convenience.

from .units import *  # noqa: F401,F403 — re-export full unit registry

# --- Legacy System Ratios / Physics ---
# (Some derived capabilities are still here, but specific chips should live in registry.py)

# NVIDIA V100 (Volta, 2017) — Source: NVIDIA V100 Data Sheet

# NVIDIA A100 (Ampere, 2020) — Source: NVIDIA A100 Data Sheet
# NOTE: Dense (without structured sparsity) values. With 2:4 sparsity, double these.
A100_FLOPS_FP16_SPARSE = 624 * TFLOPs / second   # With 2:4 structured sparsity

# NVIDIA H100 (Hopper, 2022) — Source: NVIDIA H100 Data Sheet
H100_FLOPS_FP32_CUDA = 67 * TFLOPs / second  # FP32 on CUDA (vector) cores, no Tensor Core

# NVIDIA H200 (Hopper, 2023) — Source: NVIDIA H200 Data Sheet
# H200 shares the Hopper compute die with H100, only memory differs

# NVIDIA B100/B200 (Blackwell, 2024) — Source: NVIDIA Blackwell Architecture
B200_FLOPS_FP16_SPARSE = 4500 * TFLOPs / second

# NVIDIA GB200 NVL72 (Rack-scale, 2024) — Source: NVIDIA Blackwell Architecture
# This is a full rack containing 72 Blackwell GPUs and 36 Grace CPUs.
# We model the aggregate resources of the rack for macro-scale simulation.
NVL72_GPUs = 72 * count

# AMD Instinct MI300X (CDNA 3, 2023) — Source: AMD Instinct MI300X Data Sheet

# AMD Instinct MI250X (CDNA 2, 2021) — Source: AMD MI250X Data Sheet

# Intel Gaudi 2 (2022) — Source: Intel Gaudi 2 White Paper

# Intel Gaudi 3 (2024) — Source: Intel Gaudi 3 Architecture White Paper

# AWS Trainium 2 (2024) — Source: AWS re:Invent 2023 announcements

# NVIDIA T4 (Turing, 2018) — Source: NVIDIA T4 Data Sheet

# Google TPU v1 — Source: Jouppi et al. (2017)
TPUV1_TOPS_INT8 = 92 * TOPS
TPUV1_TDP = 75 * watt

# Google TPU v2 — Source: Google Cloud Documentation
TPUV2_FLOPS_BF16 = 45 * TFLOPs / second
TPUV2_MEM_BW = 700 * GB / second
TPUV2_MEM_CAPACITY = 16 * GiB

# Google TPU v3 — Source: Google Cloud Documentation
TPUV3_FLOPS_BF16 = 105 * TFLOPs / second
TPUV3_MEM_BW = 900 * GB / second
TPUV3_MEM_CAPACITY = 32 * GiB

# Google TPU v4 — Source: Google TPUv4 paper (Jouppi et al., 2023)

# Google TPU v5p — Source: Google Cloud Documentation (2024)
TPUV5P_ICI_BW = 1200 * GB / second        # Bidirectional Inter-Chip Interconnect

# Google TPU v6e (Trillium) — Source: Google Cloud Documentation

# Cerebras Wafer-Scale Engine (WSE) — Source: Cerebras Whitepapers
WSE1_CORES = 400000 * count
WSE1_MEM_CAPACITY = 18 * GB
WSE1_MEM_BW = 9 * PB / second
WSE1_TDP = 15000 * watt
WSE1_FLOPS_FP16 = 9 * PFLOPs / second  # Estimated

WSE2_CORES = 850000 * count
WSE2_MEM_CAPACITY = 40 * GB
WSE2_MEM_BW = 20 * PB / second
WSE2_TDP = 15000 * watt
WSE2_FLOPS_FP16 = 38 * PFLOPs / second  # Estimated

WSE3_CORES = 900000 * count

# High-end Desktop CPU (Reference)
CPU_FLOPS_FP32 = 1 * TFLOPs / second

# --- Latency Hierarchy (2025 Reference) ---
LATENCY_REGISTER_REF = 0.3 * NS
LATENCY_L1_REGISTER = 1 * NS
LATENCY_L2_CACHE = 4 * NS
LATENCY_HBM3 = 300 * NS
LATENCY_NVLINK = 500 * NS
LATENCY_PCIE_GEN5 = 1000 * NS
LATENCY_INFINIBAND = 5000 * NS
LATENCY_NVME_SSD = 100000 * NS

# Mobile NPU
MOBILE_FLAGSHIP_NPU_TOPS_INT8 = 100 * TOPS
MOBILE_INFERENCE_TDP_HIGH = 4 * watt

# Edge accelerators
JETSON_AGX_ORIN_TOPS_INT8 = 275 * TOPS
JETSON_AGX_ORIN_TDP_MIN = 15 * watt
JETSON_AGX_ORIN_TDP_MAX = 60 * watt

# --- Datasets ---
IMAGENET_IMAGES = 1_281_167 * count
IMAGENET_TEST_IMAGES = 50_000 * count
CIFAR10_IMAGES = 50_000 * count
CIFAR10_TEST_IMAGES = 10_000 * count

# Standard dimensions
IMAGE_DIM_RESNET = 224
IMAGE_CHANNELS_RGB = 3
COLOR_DEPTH_8BIT = 256

# --- Network & Interconnect ---
NETWORK_10G_BW = 10 * Gbps
NETWORK_100G_BW = 100 * Gbps
NETWORK_5G_ENERGY_PER_MB_MJ = 100 * ureg.millijoule / MB
FEC_LATENCY_LOW = 100 * NS
FEC_LATENCY_HIGH = 200 * NS
FABRIC_ALPHA_NDR = 1.5 * US
FABRIC_ALPHA_ROCE = 5.0 * US
FABRIC_HOP_LATENCY = 0.6 * US

# Optical Interconnects (2025-2026 Reference)
OPTICS_POWER_PLUGGABLE_400G_W = 20 * watt
OPTICS_POWER_CPO_400G_W = 10 * watt
OPTICS_POWER_LPO_400G_W = 12 * watt       # Linear Pluggable Optics
ETHERNET_400G_BW = 400 * Gbps
ETHERNET_800G_BW = 800 * Gbps
ETHERNET_1P6T_BW = 1600 * Gbps
SWITCH_ASIC_51T2_BW = 51_200 * Gbps
SWITCH_ASIC_102T4_BW = 102_400 * Gbps

# Intra-node interconnects
NVLINK_V100_BW = 300 * GB / second        # NVLink 2.0 (V100, 6 links × 50 GB/s)
NVLINK_A100_BW = 600 * GB / second        # NVLink 3.0 (A100, 12 links × 50 GB/s)
NVLINK_H100_BW = 900 * GB / second        # NVLink 4.0 (H100, 18 links × 50 GB/s)
NVLINK_B200_BW = 1800 * GB / second       # NVLink 5.0 (B200, 72 links × 25 GB/s)
PCIE_GEN3_BW = 15.75 * GB / second        # PCIe Gen3 x16 (after 128b/130b encoding)
PCIE_GEN4_BW = 32 * GB / second           # PCIe Gen4 x16 (unidirectional, per direction)
PCIE_GEN5_BW = 64 * GB / second           # PCIe Gen5 x16 (unidirectional, per direction)

# Inter-node interconnects
INFINIBAND_HDR_BW = 200 * Gbps            # HDR InfiniBand (25 GB/s)
INFINIBAND_NDR_BW = 400 * Gbps            # NDR InfiniBand (50 GB/s)
INFINIBAND_XDR_BW = 800 * Gbps            # XDR InfiniBand (100 GB/s)
INFINIBAND_GXDR_BW = 1600 * Gbps          # GXDR InfiniBand (200 GB/s, 2026)

# --- Energy (Horowitz, 2014 @ 45nm) ---
ENERGY_DRAM_ACCESS_PJ = 640 * ureg.picojoule
ENERGY_DRAM_PJ_PER_BYTE = 160 * ureg.picojoule / byte
ENERGY_FLOP_FP32_PJ = 3.7 * ureg.picojoule / flop   # FP32 multiply-add
ENERGY_FLOP_FP16_PJ = 1.1 * ureg.picojoule / flop   # FP16 multiply-add
ENERGY_OP_INT8_PJ = 0.2 * ureg.picojoule / count    # INT8 multiply-add
ENERGY_FLOP_PJ = 4.6 * ureg.picojoule / flop         # Generic (legacy alias)
ENERGY_SRAM_L1_PJ = 0.5 * ureg.picojoule             # L1 cache access
ENERGY_SRAM_L2_PJ = 2.0 * ureg.picojoule             # L2 cache access
ENERGY_REG_PJ = 0.01 * ureg.picojoule                # Register file access
ENERGY_MOBILENET_INF_MJ = 0.1 * ureg.millijoule  # millijoule (not megajoule); matches the ENERGY_*_PJ = picojoule convention used in this block

# Addition energy (Horowitz 2014, 45nm process)
ENERGY_ADD_FP32_PJ = 0.9 * ureg.picojoule
ENERGY_ADD_FP16_PJ = 0.4 * ureg.picojoule
ENERGY_ADD_INT32_PJ = 0.1 * ureg.picojoule
ENERGY_ADD_INT8_PJ = 0.03 * ureg.picojoule

# Network transfer energy (reference)
NETWORK_ENERGY_1KB_PJ = 1_000_000 * ureg.picojoule  # ~1 microjoule for 1KB

# --- Infrastructure & Grid ---
LEAD_TIME_GPU_MONTHS = 6
LEAD_TIME_SUBSTATION_MONTHS = 24
GRID_INTERCONNECTION_QUEUE_US_GW = 2000

# --- Physics ---
# --- Physical Constants ---
SPEED_OF_LIGHT_FIBER_KM_S = 200000 * ureg.kilometer / second

# --- Cloud Pricing ---
CLOUD_EGRESS_PER_GB = 0.09 * USD / GB  # AWS data transfer out (2024 baseline)
CLOUD_ELECTRICITY_PER_KWH = 0.12 * USD / ureg.kilowatt_hour
KG_PER_METRIC_TON = 1000

# Storage Pricing (2024 baseline)
STORAGE_COST_S3_STD = 23 * USD / TB / ureg.month
STORAGE_COST_GLACIER = 1 * USD / TB / ureg.month
STORAGE_COST_NVME_LOW = 100 * USD / TB / ureg.month
STORAGE_COST_NVME_HIGH = 300 * USD / TB / ureg.month
RETRIEVAL_COST_GLACIER = 0.02 * USD / GB

# Labeling Pricing (2024 estimates)
LABELING_COST_CROWD_LOW = 0.01 * USD
LABELING_COST_CROWD_HIGH = 0.05 * USD
LABELING_COST_EXPERT_LOW = 0.50 * USD
LABELING_COST_EXPERT_HIGH = 2.00 * USD
LABELING_COST_BOX_LOW = 0.05 * USD
LABELING_COST_BOX_HIGH = 0.20 * USD
LABELING_COST_SEG_LOW = 5 * USD
LABELING_COST_SEG_HIGH = 50 * USD
LABELING_COST_MEDICAL_LOW = 50 * USD
LABELING_COST_MEDICAL_HIGH = 200 * USD

# GPU pricing (scenario baselines)
CLOUD_GPU_TRAINING_PER_HOUR = 4.0 * USD / hour
CLOUD_GPU_INFERENCE_PER_HOUR = 2.5 * USD / hour
TPU_V4_PER_HOUR = 4.0 * USD / hour
FLEET_GPU_HOUR_COST_REF = 2.0 * USD / hour
FLEET_SPOT_GPU_HOUR_COST_REF = 0.70 * USD / hour
FLEET_INTERNAL_CHARGEBACK_PER_HOUR = 2.50 * USD / hour

# --- Carbon (Scenario Baseline) ---
CARBON_PER_GPU_HR_KG = 0.16 * ureg.kilogram

# --- Mobile / Battery ---
MOBILE_TDP_W = 3 * watt
PHONE_BATTERY_WH = 15 * watt * hour
OBJECT_DETECTOR_POWER_W = 2 * watt
SERVER_POWER_W = 300 * watt

# Reference energies
ENERGY_SMARTPHONE_CHARGE_J = 40000 * joule
ENERGY_BOILING_WATER_J = 100000 * joule

# --- Video ---
VIDEO_1080P_WIDTH = 1920
VIDEO_1080P_HEIGHT = 1080
VIDEO_BYTES_PER_PIXEL_RGB = 3 * byte
VIDEO_FPS_STANDARD = Q_(30, 'Hz')

# --- Models & Workloads ---

# GPT-2 (1.5B) — used in training chapter worked examples

# GPT-3 (175B)
GPT3_TRAINING_TOKENS = 300e9 * count
GPT3_TRAINING_ACCELERATORS_REF = 1024 * count
GPT3_TRAINING_DAYS_REF = 25 * day # Days on 1024 A100s
GPT3_TRAINING_ENERGY_MWH = 1287 # MWh, estimated per Patterson et al. (2021)

# GPT-4 (Reference) - Note: Unofficial public estimates
GPT4_CLASS_PUBLIC_ESTIMATE_GPU_COUNT_REF = 25_000 * count
GPT4_CLASS_PUBLIC_ESTIMATE_TRAINING_DAYS_REF = 90 * day
GPT4_CLASS_PUBLIC_ESTIMATE_HARDWARE_LABEL = "A100-class"
GPT4_TRAINING_GPU_DAYS = 2.5e6 # A100 days

# Llama-2 (70B) — Source: Touvron et al. (2023)
LLAMA2_70B_KV_HEADS = 8                       # Grouped-Query Attention (GQA)

# Llama 3.1
LLAMA3_405B_PARAMS = 405e9 * param

# BERT-Base — Source: Devlin et al. (2018)
BERT_BASE_FLOPs = 22e9 * flop              # Per inference (seq_len=512)

# BERT-Large — Source: Devlin et al. (2018)
BERT_LARGE_FLOPs = 72e9 * flop             # Per inference (seq_len=512)

# AlexNet (Reference)
ALEXNET_FLOPs = 1.5e9 * flop               # Estimated per inference

# ResNet-18
RESNET18_PARAMS = 11.7e6 * param

# YOLOv8-nano — Source: Ultralytics (2023)
YOLOV8_NANO_FLOPs = 8.7e9 * flop  # 640x640

# WakeVision (Doorbell) — Source: Banbury et al. (2021)
WAKEVISION_FLOPs = 25e6 * flop

# Mamba-130M — Source: Gu & Dao (2023)

# Mamba-2.8B — Source: Gu & Dao (2023)

# Stable Diffusion v1.5 — Source: Rombach et al. (2022)
STABLE_DIFFUSION_V1_5_FLOPs_PER_STEP = 20e9 * flop

# Reference model/dataset dimensions
TRANSFORMER_DECODE_FLOPS_PER_PARAM = 2
TRANSFORMER_TRAINING_FLOPS_PER_PARAM_TOKEN = 6
TRANSFORMER_HIDDEN_DIM_EXAMPLE = 768
TRANSFORMER_SEQ_LEN_EXAMPLE = 512
TRANSFORMER_HEADS_EXAMPLE = 12
SYSTOLIC_ARRAY_DIM = 128
SIMD_REGISTER_BITS = 512
FP32_BITS = 32
INT8_BITS = 8
MNIST_IMAGE_WIDTH = 28
MNIST_IMAGE_HEIGHT = 28
MNIST_NUM_CLASSES = 10
MNIST_TRAINING_EXAMPLES = 60_000 * count

# Synthetic Data Constraints
SYNTHETIC_PROVENANCE_OVERHEAD = 0.4
SYNTHETIC_VERIFICATION_PASSES = 3

# Inference Scaling
LOGIC_WALL_REASONING_STEPS_EXAMPLE = 128

# Statistics
KS_TEST_COEFFICIENT = 1.36
PSI_WARN_THRESHOLD = 0.10
PSI_REVIEW_THRESHOLD = 0.20
PSI_CRITICAL_THRESHOLD = 0.25

# ML workflow lifecycle stages
ML_WORKFLOW_STAGE_PROBLEM_DEFINITION = 1
ML_WORKFLOW_STAGE_DEPLOYMENT = 5
ML_WORKFLOW_STAGE_MONITORING = 6
ML_WORKFLOW_CONSTRAINT_COST_BASE = 2

# --- Deployment Tiers (Reference Envelopes) ---
CLOUD_LATENCY_RANGE_MS = "100-500"
EDGE_LATENCY_RANGE_MS = "10-100"
MOBILE_LATENCY_RANGE_MS = "5-50"
TINY_LATENCY_RANGE_MS = "1-10"

MOBILE_RAM_RANGE_GB = "8-16"
MOBILE_STORAGE_RANGE = "128 GB-1 TB"
MOBILE_TDP_RANGE_W = "3-5"

# Deployment tiers (reference capacities)
SMARTPHONE_RAM_GB = 8 * GB
MCU_RAM_KIB = 512 * KiB
CLOUD_MEM_GIB = 100 * GiB
MOBILE_MEM_GIB = 8 * GiB
TINY_MEM_KIB = 512 * KiB

# Communication assumptions
ALLREDUCE_FACTOR = 2
GPUS_PER_HOST = 8

# Google Search (Reference)
GOOGLE_SEARCHES_PER_DAY = 8.5e9
GMAIL_EMAILS_PER_DAY = 121e9

# ResNet-50
RESNET50_FLOPs = 4.1e9 * flop

# MobileNetV2
MOBILENETV2_FLOPs = 0.3e9 * flop

# MobileNetV1
MOBILENET_V1_PARAMS = 4.2e6 * param

# KWS DS-CNN (Keyword Spotting Depthwise Separable CNN)
KWS_DSCNN_FLOPs = 20e6 * flop

# DLRM (Deep Learning Recommendation Model) — Meta benchmark
DLRM_EMBEDDING_ENTRIES = 25e9  # 25 Billion entries (dimensionless count)
DLRM_EMBEDDING_DIM = 128

# --- Hardware Unit Costs (Approximate, 2024 baseline) ---

# --- Hardware TDP (where not already defined above) ---

# --- Storage (I/O Bandwidth) ---
NVME_GEN3_SEQUENTIAL_BW = 3.5 * GB / second
NVME_SEQUENTIAL_BW = 7.0 * GB / second    # NVMe SSD sequential read (Gen 4)
NVME_GEN5_SEQUENTIAL_BW = 14.0 * GB / second
SYSTEM_MEMORY_BW = 50 * GB / second        # DDR4/DDR5 typical
HOST_DRAM_BW = 200 * GB / second
LOCAL_NVME_DRIVES_PER_NODE_REF = 4 * count
LOCAL_NVME_DRIVE_CAPACITY_REF = 7.68 * TB

# --- Case Studies ---
WAYMO_DATA_PER_HOUR_LOW = 1 * TB / hour
WAYMO_DATA_PER_HOUR_HIGH = 19 * TB / hour

# --- Anomaly Detection Case Study ---
ANOMALY_MODEL_LATENCY = 10.4 * ureg.ms
ANOMALY_MODEL_AUC = 0.86
ANOMALY_MODEL_ENERGY = 516 * ureg.microjoule

# --- Additional Constants for ML Systems Chapter ---
BATTERY_CAPACITY_MAH = 3000 * ureg.milliampere_hour
BATTERY_VOLTAGE_V = 3.7 * ureg.volt
BATTERY_ENERGY_J = (BATTERY_CAPACITY_MAH * BATTERY_VOLTAGE_V).to(joule)

# TinyML Hardware (ESP32-CAM)
ESP32_RAM = 520 * KiB
ESP32_FLASH = 4 * MB
ESP32_POWER_MIN = 0.05 * watt
ESP32_POWER_MAX = 1.2 * watt
ESP32_PRICE = 10 * USD

# Edge Hardware (NVIDIA DGX/Workstation)
DGX_RAM = 128 * GB
DGX_STORAGE = 4 * TB
DGX_POWER = 200 * watt
DGX_PRICE_MIN = 3000 * USD
DGX_PRICE_MAX = 5000 * USD

# Cloud Hardware (TPU Pod)
TPU_POD_CHIPS = 4096
TPU_POD_MEM = 131 * TB
TPU_POD_POWER = 3 * ureg.megawatt

# Hardware security and cache references
IMAGENET_NUM_CLASSES = 1000
H100_L2_CACHE = 50 * MB
TPUV5P_L2_SRAM = 100 * MB
SGX_EPC_CAPACITY = 128 * MB
SGX_BASE_LATENCY = 5 * ms
SGX_OVERFLOW_LATENCY = 150 * ms

# Reliability and diagnostic thresholds
MEMORY_BIT_ERROR_RATE_PER_BIT = 1e-17
DAM_IO_OVERHEAD_WARN_THRESHOLD = 0.10
DAM_ACTIVE_PARAMETER_SPARSE_THRESHOLD = 0.01
DAM_MFU_LOW_THRESHOLD = 0.30
DAM_LOW_UTILIZATION_THRESHOLD = 0.50
DAM_HIGH_UTILIZATION_THRESHOLD = 0.80

# --- Shared Precision Map ---
# Used by Engine, ServingModel, SynthesisSolver to map precision strings to byte widths.
PRECISION_MAP = {
    "fp32": BYTES_FP32,      # 4 bytes
    "tf32": BYTES_FP32,      # 4 bytes storage, TF32 compute (19-bit effective mantissa)
    "bf16": BYTES_FP16,      # 2 bytes (Brain Float 16, default training precision)
    "fp16": BYTES_FP16,      # 2 bytes (IEEE half-precision)
    "fp8":  BYTES_INT8,      # 1 byte  (E4M3/E5M2, Hopper+ training/inference)
    "int8": BYTES_INT8,      # 1 byte  (quantized inference)
    "int4": BYTES_INT4,      # 0.5 bytes (aggressive quantization)
}

# Fleet-Scale Constants (Volume II)
# Re-exported from defaults.py for backward compatibility.
from .defaults import *  # noqa: E402,F401,F403
