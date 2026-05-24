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

# NVIDIA H200 (Hopper, 2023) — Source: NVIDIA H200 Data Sheet
# H200 shares the Hopper compute die with H100, only memory differs

# NVIDIA B100/B200 (Blackwell, 2024) — Source: NVIDIA Blackwell Architecture

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

# Google TPU v3 — Source: Google Cloud Documentation

# Google TPU v4 — Source: Google TPUv4 paper (Jouppi et al., 2023)

# Google TPU v5p — Source: Google Cloud Documentation (2024)
TPUV5P_ICI_BW = 1200 * GB / second        # Bidirectional Inter-Chip Interconnect

# Google TPU v6e (Trillium) — Source: Google Cloud Documentation

# Cerebras Wafer-Scale Engine (WSE) — Source: Cerebras Whitepapers

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
MOBILE_INFERENCE_TDP_HIGH = 4 * watt

# Edge accelerators
JETSON_AGX_ORIN_TOPS_INT8 = 275 * TOPS
JETSON_AGX_ORIN_TDP_MIN = 15 * watt
JETSON_AGX_ORIN_TDP_MAX = 60 * watt

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
ETHERNET_400G_BW = 400 * Gbps
ETHERNET_800G_BW = 800 * Gbps
ETHERNET_1P6T_BW = 1600 * Gbps
SWITCH_ASIC_51T2_BW = 51_200 * Gbps
SWITCH_ASIC_102T4_BW = 102_400 * Gbps

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

# --- Physics ---
# --- Physical Constants ---
SPEED_OF_LIGHT_FIBER_KM_S = 200000 * ureg.kilometer / second

# --- Mobile / Battery ---
MOBILE_TDP_W = 3 * watt
PHONE_BATTERY_WH = 15 * watt * hour
OBJECT_DETECTOR_POWER_W = 2 * watt

# Reference energies
ENERGY_SMARTPHONE_CHARGE_J = 40000 * joule
ENERGY_BOILING_WATER_J = 100000 * joule

# --- Video ---
VIDEO_1080P_WIDTH = 1920
VIDEO_1080P_HEIGHT = 1080
VIDEO_BYTES_PER_PIXEL_RGB = 3 * byte
VIDEO_FPS_STANDARD = Q_(30, 'Hz')

# --- Models & Workloads ---
# Model FLOPs and parameter counts live in mlsysim/models/registry.py.

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
# Synthetic Data Constraints
SYNTHETIC_PROVENANCE_OVERHEAD = 0.4
SYNTHETIC_VERIFICATION_PASSES = 3

# Inference Scaling
LOGIC_WALL_REASONING_STEPS_EXAMPLE = 128

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

# DLRM (Deep Learning Recommendation Model) — Meta benchmark
DLRM_EMBEDDING_ENTRIES = 25e9  # 25 Billion entries (dimensionless count)

# --- Hardware Unit Costs (Approximate, 2024 baseline) ---

# --- Hardware TDP (where not already defined above) ---

# --- Storage (I/O Bandwidth) ---
NVME_GEN3_SEQUENTIAL_BW = 3.5 * GB / second
NVME_SEQUENTIAL_BW = 7.0 * GB / second    # NVMe SSD sequential read (Gen 4)
NVME_GEN5_SEQUENTIAL_BW = 14.0 * GB / second
SYSTEM_MEMORY_BW = 50 * GB / second        # DDR4/DDR5 typical
HOST_DRAM_BW = 200 * GB / second
LOCAL_NVME_DRIVES_PER_NODE_REF = 4 * count

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
