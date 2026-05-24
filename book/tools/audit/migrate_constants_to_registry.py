#!/usr/bin/env python3
"""Replace legacy mlsysim.core.constants hardware symbols with registry paths in QMD cells."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MAP_PATH = REPO_ROOT / "scripts" / "map_constants.py"

CELL_OPEN = re.compile(r"^```\{python\}")
CELL_CLOSE = re.compile(r"^```\s*$")

INTERCONNECT_MAP = {
    "NVLINK_V100_BW": "Hardware.Cloud.V100.nvlink.bandwidth",
    "NVLINK_A100_BW": "Hardware.Cloud.A100.nvlink.bandwidth",
    "NVLINK_H100_BW": "Hardware.Cloud.H100.nvlink.bandwidth",
    "NVLINK_B200_BW": "Hardware.Cloud.B200.nvlink.bandwidth",
    "PCIE_GEN3_BW": "Hardware.Cloud.V100.interconnect.bandwidth",
    "PCIE_GEN4_BW": "Hardware.Cloud.A100.interconnect.bandwidth",
    "PCIE_GEN5_BW": "Hardware.Cloud.H100.interconnect.bandwidth",
    "INFINIBAND_HDR_BW": "Systems.Fabrics.InfiniBand_HDR.bandwidth",
    "INFINIBAND_NDR_BW": "Systems.Fabrics.InfiniBand_NDR.bandwidth",
    "INFINIBAND_XDR_BW": "Systems.Fabrics.InfiniBand_XDR.bandwidth",
    "INFINIBAND_GXDR_BW": "Systems.Fabrics.InfiniBand_GXDR.bandwidth",
    "H100_FLOPS_FP32_CUDA": 'Hardware.Cloud.H100.compute.precision_flops["fp32_cuda"]',
    "CPU_FLOPS_FP32": "Hardware.Cloud.ReferenceCPU.compute.peak_flops",
    "H100_L2_CACHE": "Hardware.Cloud.H100.memory.l2_cache",
    "TPUV5P_L2_SRAM": "Hardware.Cloud.TPUv5p.memory.l2_cache",
    "SGX_EPC_CAPACITY": "Hardware.Cloud.IntelSGX.memory.capacity",
    "SGX_BASE_LATENCY": "Hardware.Cloud.IntelSGX.dispatch_tax",
    "SGX_OVERFLOW_LATENCY": "Hardware.Cloud.IntelSGX.dispatch_tax",
}

HARDWARE_MAP = {
    "A100_FLOPS_FP16_SPARSE": 'Hardware.Cloud.A100.compute.precision_flops["fp16_sparse"]',
    "TPUV5P_ICI_BW": "Hardware.Cloud.TPUv5p.nvlink.bandwidth",
    "TPUV1_TOPS_INT8": 'Hardware.Cloud.TPUv1.compute.precision_flops["int8"]',
    "TPUV1_TDP": "Hardware.Cloud.TPUv1.tdp",
    "JETSON_AGX_ORIN_TOPS_INT8": 'Hardware.Edge.JetsonAGXOrin.compute.precision_flops["int8"]',
    "JETSON_AGX_ORIN_TDP_MIN": "Hardware.Edge.JetsonAGXOrin.tdp_min",
    "JETSON_AGX_ORIN_TDP_MAX": "Hardware.Edge.JetsonAGXOrin.tdp_max",
    "ESP32_RAM": "Hardware.Tiny.ESP32_S3.memory.sram_capacity",
    "ESP32_FLASH": "Hardware.Tiny.ESP32_S3.memory.flash_capacity",
    "ESP32_POWER_MIN": "Hardware.Tiny.ESP32_S3.tdp_min",
    "ESP32_POWER_MAX": "Hardware.Tiny.ESP32_S3.tdp_max",
    "ESP32_PRICE": "10",
    "DGX_RAM": "Hardware.Workstation.DGX_Spark.memory.capacity",
    "DGX_STORAGE": "Hardware.Workstation.DGX_Spark.storage.capacity",
    "DGX_POWER": "Hardware.Workstation.DGX_Spark.tdp",
    "DGX_PRICE_MIN": "Hardware.Workstation.DGX_Spark.unit_cost",
    "DGX_PRICE_MAX": "Hardware.Workstation.DGX_Spark.unit_cost_max",
    "STABLE_DIFFUSION_V1_5_FLOPs_PER_STEP": "Models.GenerativeVision.StableDiffusion_v1_5.inference_flops",
    "DLRM_EMBEDDING_ENTRIES": "Models.Recommendation.DLRM.embedding_entries",
}


def load_map_constants() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location("map_constants", MAP_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(getattr(mod, "mapping", {}))


_MAPPING_CACHE: dict[str, str] | None = None

DEFAULTS_MAP = {
    "CLOUD_EGRESS_PER_GB": "defaults.CLOUD_EGRESS_PER_GB",
    "CLOUD_ELECTRICITY_PER_KWH": "defaults.CLOUD_ELECTRICITY_PER_KWH",
    "CLOUD_GPU_TRAINING_PER_HOUR": "defaults.CLOUD_GPU_TRAINING_PER_HOUR",
    "CLOUD_GPU_INFERENCE_PER_HOUR": "defaults.CLOUD_GPU_INFERENCE_PER_HOUR",
    "TPU_V4_PER_HOUR": "defaults.TPU_V4_PER_HOUR",
    "FLEET_GPU_HOUR_COST_REF": "defaults.FLEET_GPU_HOUR_COST_REF",
    "FLEET_SPOT_GPU_HOUR_COST_REF": "defaults.FLEET_SPOT_GPU_HOUR_COST_REF",
    "FLEET_INTERNAL_CHARGEBACK_PER_HOUR": "defaults.FLEET_INTERNAL_CHARGEBACK_PER_HOUR",
    "CARBON_PER_GPU_HR_KG": "defaults.CARBON_PER_GPU_HR_KG",
    "STORAGE_COST_S3_STD": "defaults.STORAGE_COST_S3_STD",
    "STORAGE_COST_GLACIER": "defaults.STORAGE_COST_GLACIER",
    "STORAGE_COST_NVME_LOW": "defaults.STORAGE_COST_NVME_LOW",
    "STORAGE_COST_NVME_HIGH": "defaults.STORAGE_COST_NVME_HIGH",
    "RETRIEVAL_COST_GLACIER": "defaults.RETRIEVAL_COST_GLACIER",
    "LABELING_COST_CROWD_LOW": "defaults.LABELING_COST_CROWD_LOW",
    "LABELING_COST_CROWD_HIGH": "defaults.LABELING_COST_CROWD_HIGH",
    "LABELING_COST_BOX_LOW": "defaults.LABELING_COST_BOX_LOW",
    "LABELING_COST_BOX_HIGH": "defaults.LABELING_COST_BOX_HIGH",
    "LABELING_COST_MEDICAL_LOW": "defaults.LABELING_COST_MEDICAL_LOW",
    "LABELING_COST_MEDICAL_HIGH": "defaults.LABELING_COST_MEDICAL_HIGH",
    "LEAD_TIME_GPU_MONTHS": "defaults.LEAD_TIME_GPU_MONTHS",
    "LEAD_TIME_SUBSTATION_MONTHS": "defaults.LEAD_TIME_SUBSTATION_MONTHS",
    "GRID_INTERCONNECTION_QUEUE_US_GW": "defaults.GRID_INTERCONNECTION_QUEUE_US_GW",
    "PUE_LIQUID_COOLED": "defaults.PUE_LIQUID_COOLED",
    "PUE_BEST_AIR": "defaults.PUE_BEST_AIR",
    "PUE_TYPICAL": "defaults.PUE_TYPICAL",
    "PUE_LEGACY": "defaults.PUE_LEGACY",
    "CARBON_US_AVG_GCO2_KWH": "defaults.CARBON_US_AVG_GCO2_KWH",
    "CARBON_QUEBEC_GCO2_KWH": "defaults.CARBON_QUEBEC_GCO2_KWH",
    "CARBON_IOWA_GCO2_KWH": "defaults.CARBON_IOWA_GCO2_KWH",
    "CARBON_POLAND_GCO2_KWH": "defaults.CARBON_POLAND_GCO2_KWH",
    "CARBON_NORWAY_GCO2_KWH": "defaults.CARBON_NORWAY_GCO2_KWH",
    "CARBON_EU_AVG_GCO2_KWH": "defaults.CARBON_EU_AVG_GCO2_KWH",
    "CARBON_FRANCE_GCO2_KWH": "defaults.CARBON_FRANCE_GCO2_KWH",
    "MEMORY_BIT_ERROR_RATE_PER_BIT": "defaults.MEMORY_BIT_ERROR_RATE_PER_BIT",
    "KS_TEST_COEFFICIENT": "defaults.KS_TEST_COEFFICIENT",
    "PSI_WARN_THRESHOLD": "defaults.PSI_WARN_THRESHOLD",
    "PSI_REVIEW_THRESHOLD": "defaults.PSI_REVIEW_THRESHOLD",
    "PSI_CRITICAL_THRESHOLD": "defaults.PSI_CRITICAL_THRESHOLD",
    "INFINIBAND_NDR_BW_GBS": "defaults.INFINIBAND_NDR_BW_GBS",
    "INFINIBAND_HDR_BW_GBS": "defaults.INFINIBAND_HDR_BW_GBS",
    "INFINIBAND_XDR_BW_GBS": "defaults.INFINIBAND_XDR_BW_GBS",
    "ETHERNET_400G_BW_GBS": "defaults.ETHERNET_400G_BW_GBS",
    "ETHERNET_800G_BW_GBS": "defaults.ETHERNET_800G_BW_GBS",
    "ROCE_100G_BW_GBS": "defaults.ROCE_100G_BW_GBS",
    "IB_NDR_LATENCY_US": "defaults.IB_NDR_LATENCY_US",
    "IB_HDR_LATENCY_US": "defaults.IB_HDR_LATENCY_US",
    "ROCE_LATENCY_US": "defaults.ROCE_LATENCY_US",
    "TCP_LATENCY_US": "defaults.TCP_LATENCY_US",
    "TPU_POD_CHIPS": "defaults.TPU_POD_CHIPS",
    "TPU_POD_MEM": "defaults.TPU_POD_MEM",
    "TPU_POD_POWER": "defaults.TPU_POD_POWER",
}

DATASETS_MAP = {
    "IMAGENET_IMAGES": "Datasets.ImageNet.training_examples",
    "IMAGENET_TEST_IMAGES": "Datasets.ImageNet.test_examples",
    "IMAGENET_NUM_CLASSES": "Datasets.ImageNet.num_classes",
    "CIFAR10_IMAGES": "Datasets.CIFAR10.training_examples",
    "CIFAR10_TEST_IMAGES": "Datasets.CIFAR10.test_examples",
    "MNIST_IMAGE_WIDTH": "Datasets.MNIST.image_width",
    "MNIST_IMAGE_HEIGHT": "Datasets.MNIST.image_height",
    "MNIST_NUM_CLASSES": "Datasets.MNIST.num_classes",
    "MNIST_TRAINING_EXAMPLES": "Datasets.MNIST.training_examples",
}

TRAINING_MAP = {
    "GPT3_TRAINING_TOKENS": "Models.Language.GPT3.training_tokens",
    "GPT3_TRAINING_ACCELERATORS_REF": "Models.Language.GPT3.training_accelerators_ref",
    "GPT3_TRAINING_DAYS_REF": "Models.Language.GPT3.training_days_ref",
    "GPT3_TRAINING_ENERGY_MWH": "Models.Language.GPT3.training_energy_mwh",
    "GPT4_TRAINING_GPU_DAYS": "Models.Language.GPT4.training_gpu_days",
    "GPT4_CLASS_PUBLIC_ESTIMATE_GPU_COUNT_REF": "Models.Language.GPT4.training_accelerators_ref",
    "GPT4_CLASS_PUBLIC_ESTIMATE_TRAINING_DAYS_REF": "Models.Language.GPT4.training_days_ref",
    "GPT4_CLASS_PUBLIC_ESTIMATE_HARDWARE_LABEL": "Models.Language.GPT4.training_hardware_label",
    "LLAMA2_70B_KV_HEADS": "Models.Language.Llama2_70B.kv_heads",
}


def merged_mapping() -> dict[str, str]:
    global _MAPPING_CACHE
    if _MAPPING_CACHE is None:
        out = {**load_map_constants(), **INTERCONNECT_MAP, **HARDWARE_MAP, **DEFAULTS_MAP, **DATASETS_MAP, **TRAINING_MAP}
        _MAPPING_CACHE = dict(sorted(out.items(), key=lambda kv: len(kv[0]), reverse=True))
    return _MAPPING_CACHE


def substitute_cell(cell: str, mapping: dict[str, str]) -> tuple[str, list[str]]:
    replaced: list[str] = []
    out = cell
    for sym, target in mapping.items():
        cpat = re.compile(rf"\bconstants\.{re.escape(sym)}\b")
        if cpat.search(out):
            out = cpat.sub(target, out)
            replaced.append(sym)
            continue
        pat = re.compile(rf"(?<![.\w]){re.escape(sym)}\b")
        if pat.search(out):
            out = pat.sub(target, out)
            replaced.append(sym)
    return out, replaced


def ensure_registry_imports(cell: str) -> str:
    needs_hardware = "Hardware." in cell and "import Hardware" not in cell and "from mlsysim import *" not in cell
    needs_systems = "Systems." in cell and "import Systems" not in cell and "from mlsysim import *" not in cell
    needs_models = "Models." in cell and "import Models" not in cell and "from mlsysim import *" not in cell
    needs_datasets = "Datasets." in cell and "from mlsysim import *" not in cell
    needs_defaults = "defaults." in cell and "from mlsysim.core import defaults" not in cell
    prefix = []
    if needs_hardware or needs_systems or needs_models or needs_datasets:
        if "from mlsysim import *" not in cell:
            prefix.append("from mlsysim import *")
    if needs_defaults and "from mlsysim.core import defaults" not in cell:
        prefix.append("from mlsysim.core import defaults")
    if not prefix:
        return cell
    lines = cell.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("#|") or line.startswith("# ") or line.startswith("#┌"):
            insert_at = i + 1
        elif line.strip() and not line.startswith("#"):
            break
    return "\n".join(lines[:insert_at] + prefix + lines[insert_at:])


def migrate_file(path: Path, mapping: dict[str, str], dry_run: bool) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out_lines: list[str] = []
    stats = {"cells": 0, "cells_changed": 0, "symbols": set()}
    i = 0
    while i < len(lines):
        if CELL_OPEN.match(lines[i]):
            start = i
            j = i + 1
            while j < len(lines) and not CELL_CLOSE.match(lines[j]):
                j += 1
            block = "\n".join(lines[i + 1 : j])
            new_block, replaced = substitute_cell(block, mapping)
            new_block = ensure_registry_imports(new_block)
            stats["cells"] += 1
            if replaced:
                stats["cells_changed"] += 1
                stats["symbols"].update(replaced)
            out_lines.extend(lines[i : i + 1])
            out_lines.extend(new_block.splitlines())
            out_lines.append(lines[j])
            i = j + 1
        else:
            out_lines.append(lines[i])
            i += 1
    new_text = "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")
    if not dry_run and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    stats["symbols"] = sorted(stats["symbols"])
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qmd", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path = args.qmd if args.qmd.is_absolute() else REPO_ROOT / args.qmd
    mapping = merged_mapping()
    stats = migrate_file(path, mapping, dry_run=args.dry_run)
    print(f"{path}: {stats['cells_changed']}/{stats['cells']} cells, {len(stats['symbols'])} symbols")
    for sym in stats["symbols"]:
        print(f"  - {sym}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
