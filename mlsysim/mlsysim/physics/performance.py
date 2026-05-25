"""Training time, scaling, roofline, and pipeline performance."""

from __future__ import annotations

from mlsysim.core.constants import ureg
from mlsysim.core._validation import validate_positive, validate_at_least, validate_range


def dTime(total_ops, num_devices, peak_flops_per_device, efficiency_eta):
    """Core training time calculation; returns duration in seconds."""
    validate_at_least(num_devices, 1, "num_devices")
    validate_positive(efficiency_eta, "efficiency_eta")
    effective_throughput = num_devices * peak_flops_per_device * efficiency_eta
    duration = total_ops / effective_throughput
    return duration.to(ureg.second)


calc_training_time = dTime


def calc_training_time_days(total_ops, num_devices, peak_flops_per_device, efficiency_eta):
    """Training duration in days."""
    duration = dTime(total_ops, num_devices, peak_flops_per_device, efficiency_eta)
    return duration.m_as(ureg.day)


def calc_amdahls_speedup(p, s):
    """Overall system speedup (Amdahl's Law)."""
    validate_range(p, 0.0, 1.0, "p (parallel fraction)")
    validate_positive(s, "s (speedup factor)")
    return 1 / ((1 - p) + (p / s))


def calc_bottleneck(ops, model_bytes, device_flops, device_bw):
    """Roofline bottleneck analysis (Williams et al., 2009)."""
    compute_time = ops / device_flops
    memory_time = model_bytes / device_bw
    t_comp_ms = compute_time.m_as(ureg.millisecond)
    t_mem_ms = memory_time.m_as(ureg.millisecond)

    if t_comp_ms < 1e-15:
        return {
            "compute_ms": 0.0,
            "memory_ms": t_mem_ms,
            "bottleneck": "Memory",
            "ratio": float("inf"),
            "intensity": 0.0,
        }

    if t_mem_ms < 1e-15:
        return {
            "compute_ms": t_comp_ms,
            "memory_ms": 0.0,
            "bottleneck": "Compute",
            "ratio": float("inf"),
            "intensity": float("inf"),
        }

    is_memory_bound = t_mem_ms > t_comp_ms
    ratio = t_mem_ms / t_comp_ms if is_memory_bound else t_comp_ms / t_mem_ms
    intensity = ops / model_bytes
    return {
        "compute_ms": t_comp_ms,
        "memory_ms": t_mem_ms,
        "bottleneck": "Memory" if is_memory_bound else "Compute",
        "ratio": ratio,
        "intensity": intensity.magnitude,
    }


def calc_pipeline_bubble(n_stages, n_microbatches, v_stages=1):
    """Pipeline bubble fraction (GPipe / 1F1B / Interleaved 1F1B)."""
    return (n_stages - 1) / (v_stages * n_microbatches + n_stages - 1)


def calc_effective_flops(peak_flops, mfu, scaling_eff, goodput_ratio):
    """Effective FLOPS after MFU, scaling efficiency, and goodput overheads."""
    from ._units import _ensure_unit

    pf = _ensure_unit(peak_flops, ureg.flop / ureg.second, "peak_flops")
    return (pf * mfu * scaling_eff * goodput_ratio).to(ureg.flop / ureg.second)
