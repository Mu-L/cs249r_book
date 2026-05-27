#!/usr/bin/env python3
"""Targeted coherence fixes for training.qmd."""
from pathlib import Path

QMD = Path(__file__).resolve().parents[3] / "book/quarto/contents/vol1/training/training.qmd"
text = QMD.read_text()

replacements = [
    ("gpt2_total_flops_str        = fmt_sci(gpt2_total_flops)",
     "gpt2_total_flops_str        = MarkdownStr(f\"{fmt_sci(gpt2_total_flops)} FLOPs\")"),
    ("gpt2_total_flops_str     = fmt_sci(gpt2_total_flops)",
     "gpt2_total_flops_str     = MarkdownStr(f\"{fmt_sci(gpt2_total_flops)} FLOPs\")"),
    ("1.  **Significance (quantitative)**: Training memory cost is `{python} TrainingScenarios.adam_training_memory_multiplier_str`$\\\\times$ the inference memory cost",
     "1.  **Significance (quantitative)**: Training memory cost is `{python} TrainingScenarios.adam_training_memory_multiplier_str` the inference memory cost"),
    ("activation storage across `{python} TrainingMemoryPressure.gpt2_layers_str` transformer layers can double",
     "activation storage across `{python} TrainingMemoryPressure.gpt2_layers_str` can double"),
    ("v100_tflops_fp16_str = fmt(v100_tflops_fp16, precision=0, commas=False)\n    v100_tflops_fp32_str = fmt(v100_tflops_fp32, precision=1, commas=False)",
     "v100_tflops_fp16_str = fmt(v100_tflops_fp16, precision=0, commas=False, suffix=' TFLOP/s')\n    v100_tflops_fp32_str = fmt(v100_tflops_fp32, precision=1, commas=False, suffix=' TFLOP/s')"),
    ("v100_mem_str         = fmt(v100_mem, precision=1, commas=False)\n```",
     "v100_mem_str         = fmt(v100_mem, precision=1, commas=False, suffix=' GB')\n```"),
    ("1. **Gradient size**: `{python} NetworkWall.model_params_b_str` $\\times 10^9 \\times 2$ bytes = `{python} NetworkWall.gradient_size_str` per step.",
     "1. **Gradient size** (FP16): `{python} NetworkWall.gradient_size_str` per step."),
    ("That gives `{python} NetworkWall.allreduce_factor_str` `{python} NetworkWall.gradient_size_str` = `{python} NetworkWall.allreduce_str` total.",
     "That gives `{python} NetworkWall.allreduce_factor_str` $\\times$ `{python} NetworkWall.gradient_size_str` = `{python} NetworkWall.allreduce_str` total."),
    ("    vram_gpu_capacity_str = fmt(gpu_capacity_gb, precision=0, commas=False, suffix=' GB')",
     "    vram_gpu_capacity_str = fmt(gpu_capacity_gb, precision=0, commas=False, suffix=' GB GPU')"),
    ("    batch_size = 32\n    seq_len = 1024\n    bytes_per_val = 2",
     "    batch_size = 8\n    seq_len = 1024\n    bytes_per_val = 2"),
    ("- Batch size: 32, Sequence length: 1024",
     "- Batch size: 8, Sequence length: 1024"),
    ("class GPT2SummaryScalingRecap:\n    batch_size = 32",
     "class GPT2SummaryScalingRecap:\n    batch_size = 8"),
    ("    b_total_mem_str = f\"{fmt(b_total_mem, precision=1, commas=False)} GB\"\n    o_total_mem_str = f\"{fmt(o_total_mem, precision=1, commas=False)} GB\"",
     "    b_total_mem_str = fmt(b_total_mem, precision=1, commas=False, suffix=' GB')\n    o_total_mem_str = fmt(o_total_mem, precision=1, commas=False, suffix=' GB')"),
    ("    num_workers_str             = fmt(num_workers, precision=0, commas=False)\n    prefetch_factor_str         = fmt(prefetch_factor, precision=0, commas=False)",
     "    num_workers_str             = MarkdownStr(\"num_workers=4\")\n    prefetch_factor_str         = MarkdownStr(\"prefetch_factor=2\")"),
    ("training our lighthouse GPT-2 model (`{python} CrossGenPrecisionCalc.gpt2_params_b_str` parameters) on",
     "training our lighthouse GPT-2 model (`{python} CrossGenPrecisionCalc.gpt2_params_b_str`) on"),
    ("With `{python} AttentionMemoryCalc.fa_n_heads_str` attention heads, this grows",
     "With `{python} AttentionMemoryCalc.fa_n_heads_str`, this grows"),
    ("- Cost: USD 16/hour$\\times$ `{python} GradientAccumulation.gpus_naive_str` = USD `{python} GradientAccumulation.naive_hourly_str`",
     "- Cost: USD 16/hour $\\times$ `{python} GradientAccumulation.gpus_naive_str` = USD `{python} GradientAccumulation.naive_hourly_str`"),
    ("    naive_hourly_str = fmt(naive_hourly, precision=0, commas=False, suffix='/hour')",
     "    naive_hourly_str = fmt(naive_hourly, precision=0, commas=False)"),
    ("- FP16: ~\\$`{python} MixedPrecisionLossScaling.fp16_cost_str` for `{python} MixedPrecisionLossScaling.fp16_weeks_str` on `{python} MixedPrecisionLossScaling.n_v100_gpus_str` V100",
     "- FP16: ~\\$`{python} MixedPrecisionLossScaling.fp16_cost_str` for `{python} MixedPrecisionLossScaling.fp16_weeks_str` on `{python} MixedPrecisionLossScaling.n_v100_gpus_str`"),
    ("- FP32: ~\\$`{python} MixedPrecisionLossScaling.fp32_cost_str` for `{python} MixedPrecisionLossScaling.fp32_weeks_str` on `{python} MixedPrecisionLossScaling.n_v100_gpus_str` V100",
     "- FP32: ~\\$`{python} MixedPrecisionLossScaling.fp32_cost_str` for `{python} MixedPrecisionLossScaling.fp32_weeks_str` on `{python} MixedPrecisionLossScaling.n_v100_gpus_str`"),
    ("functions requiring transcendental operations are significantly more expensive than simple thresholding: in software, GELU's `exp()`",
     "functions requiring transcendental operations are significantly more expensive than simple thresholding: in software, GELU `exp()`"),
    ("    resnet_layers_str = fmt(resnet_layers, precision=0, commas=False)",
     "    resnet_layers_str = fmt(resnet_layers, precision=0, commas=False, suffix=' layers')"),
    ("As the network progresses through its `{python} ResNetMemoryScaling.resnet_layers_str}`, the cumulative",
     "As the network progresses through its `{python} ResNetMemoryScaling.resnet_layers_str`, the cumulative"),
    ("Across all `{python} ResNetMemoryScaling.resnet_layers_str}`, gradient storage",
     "Across all `{python} ResNetMemoryScaling.resnet_layers_str`, gradient storage"),
    ("f\"6 \\\\times {ub_params_b_str} \\\\times 10^9 \\\\times {ub_tokens_t_str} \\\\times 10^{{12}}\"",
     "f\"6 \\\\times {model.parameters.m_as(Bparam):.0f} \\\\times 10^9 \\\\times {ub_tokens_t_str} \\\\times 10^{{12}}\""),
    ("check(total_ckpt_gb < v100_mem_gb * 4.0, f\"Checkpointed GPT-2 walkthrough: {total_ckpt_gb:.1f} GB.\")",
     "check(total_ckpt_gb < v100_mem_gb, f\"Checkpointed GPT-2 walkthrough should fit V100: {total_ckpt_gb:.1f} GB vs {v100_mem_gb:.1f} GB.\")"),
]

# Ensure MarkdownStr import in TrainingScenarios cell
if "from mlsysim.fmt import fmt, check" in text and "MarkdownStr" not in text.split("class TrainingScenarios")[0][-500:]:
    text = text.replace(
        "from mlsysim.fmt import fmt, check\n\nclass TrainingScenarios:",
        "from mlsysim.fmt import fmt, check, MarkdownStr\n\nclass TrainingScenarios:",
        1,
    )
if "class GPT2LighthouseSpecs:" in text:
    text = text.replace(
        "from mlsysim.fmt import fmt\n\nclass GPT2LighthouseSpecs:",
        "from mlsysim.fmt import fmt, MarkdownStr\n\nclass GPT2LighthouseSpecs:",
        1,
    )

for old, new in replacements:
    if old not in text:
        print("MISSING:", old[:60])
    else:
        text = text.replace(old, new, 1)

QMD.write_text(text)
print("Done")
