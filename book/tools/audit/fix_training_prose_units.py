#!/usr/bin/env python3
"""Fix training.qmd suffix mistakes and prose duplicates after unit migration."""

from __future__ import annotations

import re
from pathlib import Path

QMD = Path(__file__).resolve().parents[3] / "book/quarto/contents/vol1/training/training.qmd"


def main() -> None:
    text = QMD.read_text(encoding="utf-8")

    # Cell fixes
    text = text.replace("suffix=' B parameters'", "suffix=' B'")
    text = text.replace('suffix=" B parameters"', 'suffix=" B"')

    # Prose: strip duplicate rate units after suffixed refs
    text = re.sub(
        r"(`\{python\}\s+[A-Za-z_][\w.]*(?:gbs|tbs|bw|nvlink|pcie|network|token_rate|random_access|nvme)[\w.]*_str)`/s",
        r"\1",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(`\{python\}\s+GPT2DataPipeline\.tokens_per_batch_str)`/batch",
        r"\1",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+GPT2DataPipeline\.token_rate_str)`/s",
        r"\1",
        text,
    )

    # Prose: duplicate × after suffixed speedup/factor refs
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:speedup|factor|multiplier|ratio|reduction|over_v100|memory_reduction)_str)`\s*\$\\times\$",
        r"\1",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+NetworkWall\.allreduce_factor_str`)\$\\times\$",
        r"\1",
        text,
    )

    # Prose: duplicate FLOP/byte
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:ridge|intensity|flop_byte)_str)` FLOP/byte",
        r"\1",
        text,
    )

    # Prose: B / billion duplication
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:params_b|_b)_str`)-billion-parameter",
        r"\1-parameter",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:params_b|_b)_str`)\s+billion\b",
        r"\1",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:params_b|_b)_str`)\s+B\s+\$\\times\$",
        r"\1 $\times$",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+MixedPrecisionMemory\.gpt2_b_str`)\s+B\b",
        r"\1",
        text,
    )
    text = text.replace(
        "`{python} GPT2LighthouseSpecs.gpt2_params_b_str` Billion (XL)",
        "`{python} GPT2LighthouseSpecs.gpt2_params_b_str` (XL)",
    )
    text = re.sub(
        r"(`\{python\}\s+GPT2Optimizer\.model_params_b_str`)\s+billion\s+\$\\times\$",
        r"\1 $\times$",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+OptimizerScenarios\.adam_7b_params_str`)-billion-parameter",
        r"\1-parameter",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+TrainingScenarios\.adam_example_params_b_str`)-billion-parameter",
        r"\1-parameter",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+VRAMRequirements\.vram_params_b_str`)-billion-parameter",
        r"\1-parameter",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+VRAMRequirements\.vram_params_b_str`)\s+billion parameters",
        r"\1 parameters",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+NetworkWall\.model_params_b_str`)-billion-parameter",
        r"\1-parameter",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+OptimizerStateRecap\.model_params_b_str`)-billion-parameter",
        r"\1-parameter",
        text,
    )

    # Prose: layers duplication
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:layers|n_layers|ckpt_layers|gpt2_layers|resnet_layers|vram_layers)_str`)\s+layers\b",
        r"\1",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(`\{python\}\s+VRAMRequirements\.vram_layers_str`)\s+Layers\b",
        r"\1",
        text,
    )

    # Prose: GB/MB duplication
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:gb|mb|kb|mem|capacity|weights|grad|opt|act|total|subtotal|peak|state|adam|p_|g_|t_|ckpt|param|gradient|allreduce|nvlink|network_bw|pcie|random_access|nvme)[\w.]*_str`)&nbsp;GB",
        r"\1",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:gb|mb|kb|mem|capacity|weights|grad|opt|act|total|subtotal|peak|state|adam|p_|g_|t_|ckpt|param|gradient|allreduce)[\w.]*_str`)\s+GB\b",
        r"\1",
        text,
    )

    # Prose: percent duplication
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:pct|percent|util|overhead|reduction|speedup_pct|degrade|prefetch_reduction)[\w.]*_str`)\s+%",
        r"\1",
        text,
    )

    # Prose: TFLOP/s duplication in hardware prose
    text = re.sub(
        r"(`\{python\}\s+[\w.]+tflops[\w.]*_str`)\s+peak FP16",
        r"\1 peak",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+TrainingHardware\.v100_tflops_fp32_str`)\s+FP32",
        r"\1",
        text,
    )

    # Prose: W / hosts / CO2 duplication
    text = re.sub(
        r"(`\{python\}\s+TrainingCarbonFootprint\.cf_gpu_tdp_str`)\s+W\b",
        r"\1",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+TrainingCarbonFootprint\.cf_cpu_tdp_per_host_w_str`)\s+W\b",
        r"\1",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+TrainingCarbonFootprint\.cf_hosts_str`)\s+hosts\b",
        r"\1",
        text,
    )
    text = text.replace(
        "`{python} TrainingCarbonFootprint.cf_co2_str` tons of CO~2~",
        "`{python} TrainingCarbonFootprint.cf_co2_str`",
    )

    # Prose: V100 GPU phrasing
    text = text.replace(
        "on `{python} MixedPrecisionLossScaling.n_v100_gpus_str` V100s",
        "on `{python} MixedPrecisionLossScaling.n_v100_gpus_str` V100 GPUs",
    )

    # Prose: PipelineTimingRecap percent vs speedup label
    text = text.replace(
        "a `{python} PipelineTimingRecap.pipeline_speedup_pct_str` speedup achieved",
        "a `{python} PipelineTimingRecap.pipeline_speedup_pct_str` reduction in wall-clock time achieved",
    )
    text = text.replace(
        "a `{python} PipelineTimingRecap.pipeline_speedup_pct_str` speedup.",
        "a `{python} PipelineTimingRecap.pipeline_speedup_pct_str` reduction in wall-clock time.",
    )

    # Prose: FallaciesPitfallsSetup
    text = text.replace(
        "achieving only `{python} FallaciesPitfallsSetup.fp_actual_speedup_range_str` speedup instead of `{python} FallaciesPitfallsSetup.fp_gpu_count_str`.",
        "achieving only `{python} FallaciesPitfallsSetup.fp_actual_speedup_range_str`× speedup instead of `{python} FallaciesPitfallsSetup.fp_gpu_count_str`×.",
    )
    text = text.replace(
        "Small models on `{python} FallaciesPitfallsSetup.fp_gpu_count_str` spend",
        "Small models on `{python} FallaciesPitfallsSetup.fp_gpu_count_str` GPUs spend",
    )

    # Prose: NetworkWall trailing s after time ref
    text = re.sub(
        r"(`\{python\}\s+NetworkWall\.network_time_str`)\s+s\.",
        r"\1.",
        text,
    )

    # Prose: MixedPrecisionHardwareDetail
    text = text.replace(
        "about `{python} MixedPrecisionHardwareDetail.h100_fp8_speedup_vs_fp16_str` the H100",
        "about `{python} MixedPrecisionHardwareDetail.h100_fp8_speedup_vs_fp16_str`× the H100",
    )

    # Prose: PreprocessingScenarios
    text = text.replace(
        "where `num_workers=4` (`{python} PreprocessingScenarios.num_workers_str`) enables four parallel preprocessing threads and `prefetch_factor=2` (`{python} PreprocessingScenarios.prefetch_factor_str`) maintains",
        "where `num_workers=` `{python} PreprocessingScenarios.num_workers_str` enables parallel preprocessing threads and `prefetch_factor=` `{python} PreprocessingScenarios.prefetch_factor_str` maintains",
    )
    text = text.replace(
        "With `{python} PreprocessingScenarios.num_workers_str` workers and `prefetch_factor=2` (`{python} PreprocessingScenarios.prefetch_factor_str`), the",
        "With `num_workers=` `{python} PreprocessingScenarios.num_workers_str` and `prefetch_factor=` `{python} PreprocessingScenarios.prefetch_factor_str`, the",
    )
    text = text.replace(
        "A practical starting point is setting `num_workers` (typically `{python} PreprocessingScenarios.num_workers_str` on a quad-core host) equal to the number of available CPU cores",
        "A practical starting point is setting `num_workers` equal to the number of available CPU cores (often `{python} PreprocessingScenarios.num_workers_str` on a quad-core host)",
    )

    # Prose: GPT2DataPipeline PCIe line
    text = text.replace(
        "PCIe Gen3 x16: `{python} GPT2DataPipeline.pcie_gen3_str`/s theoretical",
        "PCIe Gen3 x16: `{python} GPT2DataPipeline.pcie_gen3_str` theoretical",
    )

    # Prose: ActivationBenchmarks subject
    text = text.replace(
        "in software, `exp()` takes `{python} ActivationBenchmarks.exp_cycles_min_str`",
        "in software, GELU's `exp()` takes `{python} ActivationBenchmarks.exp_cycles_min_str`",
    )

    # Prose: GPT2LighthouseSpecs compute row
    text = text.replace(
        "~ `{python} GPT2LighthouseSpecs.gpt2_total_flops_str` total",
        "~ `{python} GPT2LighthouseSpecs.gpt2_total_flops_str` FLOPs total",
    )

    # Prose: TrainingCarbonFootprint energy line
    text = text.replace(
        "(`{python} TrainingCarbonFootprint.cf_num_gpus_str` `{python} TrainingCarbonFootprint.cf_gpu_tdp_str` + `{python} TrainingCarbonFootprint.cf_hosts_str` × `{python} TrainingCarbonFootprint.cf_cpu_tdp_per_host_w_str`)",
        "(`{python} TrainingCarbonFootprint.cf_num_gpus_str` × `{python} TrainingCarbonFootprint.cf_gpu_tdp_str` + `{python} TrainingCarbonFootprint.cf_hosts_str` × `{python} TrainingCarbonFootprint.cf_cpu_tdp_per_host_w_str`)",
    )

    # Prose: GradientAccumulation clarity
    text = text.replace(
        "(`{python} GradientAccumulation.gpus_accum_str` GPUs × `{python} GradientAccumulation.micro_batch_str` micro-batch × `{python} GradientAccumulation.accum_steps_str` accumulation steps",
        "(`{python} GradientAccumulation.gpus_accum_str` × `{python} GradientAccumulation.micro_batch_str` micro-batch × `{python} GradientAccumulation.accum_steps_str` accumulation steps",
    )

    # MixedPrecisionHardwareTable coverage prose
    needle = ": **Precision Format Comparison**:"
    insert = (
        "On A100, FP16 and BF16 Tensor Cores reach "
        "`{python} MixedPrecisionHardwareTable.a100_fp16_speedup_str` the FP32 CUDA-core peak.\n\n"
    )
    if insert.strip() not in text and needle in text:
        text = text.replace(needle, insert + needle)

    # MixedPrecisionHardwareTable duplicate × in cells
    text = text.replace(
        "`{python} MixedPrecisionHardwareTable.a100_fp16_speedup_str`$\\times$",
        "`{python} MixedPrecisionHardwareTable.a100_fp16_speedup_str`",
    )

    # Prose: duplicate time units
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:days|cluster_days|years|hours|time_hours)_str`)\s+(?:days|hours)\b",
        r"\1",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+GradientAccumulation\.(?:naive|accum|savings)_hourly_str`)/hour\b",
        r"\1",
        text,
    )

    # Prose: duplicate samples/s
    text = re.sub(
        r"(`\{python\}\s+CrossGenPrecisionCalc\.\w+_sps_str`)\s+samples/sec\b",
        r"\1",
        text,
    )

    # Prose: duplicate × after suffixed speedup refs
    text = re.sub(
        r"(`\{python\}\s+[\w.]+(?:speedup|factor|reduction|over_v100|mp_speedup|memory_reduction|fa_reduction|time_speedup|checkpoint_factor|allreduce_factor)_str`)\s*\$\\times\$",
        r"\1",
        text,
    )
    text = re.sub(
        r"(`\{python\}\s+FallaciesPitfallsSetup\.fp_mp_speedup_v100_str`)\$\\times\$",
        r"\1",
        text,
    )

    # Prose: Fallacies ideal linear speedup (not "8 GPUs")
    text = text.replace(
        "achieving only `{python} FallaciesPitfallsSetup.fp_actual_speedup_range_str` speedup instead of the ideal `{python} FallaciesPitfallsSetup.fp_gpu_count_str}`.",
        "achieving only `{python} FallaciesPitfallsSetup.fp_actual_speedup_range_str` speedup instead of the ideal `{python} FallaciesPitfallsSetup.fp_gpu_ideal_speedup_str}`.",
    )

    # Prose: MixedPrecisionMemory parameter byte math
    text = text.replace(
        "`{python} MixedPrecisionMemory.gpt2_b_str` $\\times$ 4 bytes =",
        "`{python} MixedPrecisionMemory.gpt2_b_str` parameters at 4 bytes each =",
    )
    text = text.replace(
        "`{python} MixedPrecisionMemory.gpt2_b_str` $\\times$ 2 bytes =",
        "`{python} MixedPrecisionMemory.gpt2_b_str` parameters at 2 bytes each =",
    )

    # Prose: AttentionMemoryCalc duplicate "heads"
    text = re.sub(
        r"(`\{python\}\s+AttentionMemoryCalc\.fa_n_heads_str`)\s+attention heads\b",
        r"\1",
        text,
    )

    # Prose: MixedPrecisionHardwareDetail duplicate × in equation line
    text = text.replace(
        "`{python} MixedPrecisionHardwareDetail.a100_tflops_fp32_str`$\\times 10^{12}\\times 4$",
        "`{python} MixedPrecisionHardwareDetail.a100_tflops_fp32_str` × $10^{12}$ × 4 bytes",
    )

    QMD.write_text(text, encoding="utf-8")
    print(f"Patched {QMD.name}")


if __name__ == "__main__":
    main()
