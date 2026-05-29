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
# Architecture formulas belong in: `mlsysim/physics/`
#
# Measurement units live in units.py; domain assumptions live in registries
# (Systems, Literature, Infrastructure) and core/calibration.py — not re-exported here.
#
# CI: mlsysim/tests/test_constants_allowlist.py guards this contract.

from .units import *  # noqa: F401,F403 — re-export full unit registry

# --- System ratios / physics ---
# (Chip-specific numbers live in mlsysim/hardware/registry.py)

# --- Latency Hierarchy --- (tech-class access latency -> Hardware.Tech)
# register/L1/L2/HBM3 -> Hardware.Tech.Memory.*.latency
# NVLink/PCIe-Gen5    -> Hardware.Tech.Interconnect.*.latency
# NVMe SSD            -> Hardware.Tech.Storage.NvmeGen4.latency
# InfiniBand (fabric) -> Systems.Fabrics.InfiniBand_NDR.latency

# Mobile NPU
MOBILE_INFERENCE_TDP_HIGH = 4 * watt

# Standard dimensions
IMAGE_DIM_RESNET = 224  # TODO(taxonomy P7): -> Datasets.ImageNet.image_width
# IMAGE_CHANNELS_RGB, COLOR_DEPTH_8BIT -> core/units.py (encoding facts)

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

# --- Energy --- (per-op / per-byte energy is a tech-class fact -> Hardware.Tech)
# FLOP/ADD/INT8 op energy   -> Hardware.Tech.Op.*.energy        (Horowitz 2014, 45 nm)
# DRAM access / per-byte    -> Hardware.Tech.Memory.HBM3.energy_per_access / energy_per_byte
# SRAM L1/L2, register file  -> Hardware.Tech.Memory.{L1,L2,Register}.energy_per_access
# Architecture-class efficiency + per-byte movement hierarchy -> Literature.Energy.*
ENERGY_MOBILENET_INF_MJ = 0.1 * ureg.millijoule  # TODO(taxonomy): MobileNet inference energy -> Models/Scenarios

# Network transfer energy (reference) — TODO(taxonomy): -> Systems network-energy
NETWORK_ENERGY_1KB_PJ = 1_000_000 * ureg.picojoule  # ~1 microjoule for 1KB

# --- Physics ---
# --- Physical Constants ---
SPEED_OF_LIGHT_FIBER_KM_S = 200000 * ureg.kilometer / second

# --- Mobile / Battery ---
MOBILE_TDP_W = 3 * watt
PHONE_BATTERY_WH = 15 * watt * hour
OBJECT_DETECTOR_POWER_W = 2 * watt

# Reference energy-scale anchors -> Scenarios.EnergyAnchors.{SmartphoneCharge,BoilingWater}

# --- Video --- (VIDEO_* encoding/format facts -> core/units.py)

# Reference model/dataset dimensions
# TRANSFORMER FLOP ratios -> Literature.Chinchilla.{ComputeConstant(6PD), DecodeConstant(2P)}
# TRANSFORMER_*_EXAMPLE dims -> inlined in the one worked example that used them (hw_acceleration)
SYSTOLIC_ARRAY_DIM = 128
# SIMD_REGISTER_BITS, FP32_BITS, INT8_BITS -> core/units.py (bit widths)
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

# GOOGLE_SEARCHES_PER_DAY, GMAIL_EMAILS_PER_DAY -> Scenarios.Workloads

# --- Storage (I/O Bandwidth) ---
# NVME_*/SYSTEM_MEMORY_BW/HOST_DRAM_BW -> Hardware.Tech.Storage (tech-class bandwidth)
LOCAL_NVME_DRIVES_PER_NODE_REF = 4 * count  # TODO(taxonomy): node config -> Systems

# --- Case Studies --- (WAYMO_*, ANOMALY_MODEL_* -> Scenarios.Workloads / Scenarios.AnomalyModel)

# --- Additional Constants for ML Systems Chapter ---
BATTERY_CAPACITY_MAH = 3000 * ureg.milliampere_hour
BATTERY_VOLTAGE_V = 3.7 * ureg.volt
BATTERY_ENERGY_J = (BATTERY_CAPACITY_MAH * BATTERY_VOLTAGE_V).to(joule)

# PRECISION_MAP -> core/units.py (precision-string -> byte-width is a measurement fact)

