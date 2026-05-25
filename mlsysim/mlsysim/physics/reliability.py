"""Reliability, checkpointing, and availability models."""

from __future__ import annotations

import math

from mlsysim.core.constants import ureg
from mlsysim.core._validation import validate_positive

from ._units import _ensure_unit


def calc_young_daly_interval(checkpoint_cost_s, mtbf_s):
    """Optimal checkpoint interval (Young's first-order approximation)."""
    delta = _ensure_unit(checkpoint_cost_s, ureg.second, "checkpoint_cost_s")
    mtbf = _ensure_unit(mtbf_s, ureg.second, "mtbf_s")
    seconds = math.sqrt(2 * delta.m_as(ureg.second) * mtbf.m_as(ureg.second))
    return seconds * ureg.second


def calc_mtbf_cluster(component_mtbf_hours, n_components, correlation_factor=1.0):
    """Cluster MTBF from identical independent components."""
    mtbf = _ensure_unit(component_mtbf_hours, ureg.hour, "component_mtbf_hours")
    return (mtbf / n_components * correlation_factor).to(ureg.hour)


def calc_mtbf_node(
    gpu_mtbf_h,
    n_gpus,
    nic_mtbf_h,
    n_nics,
    psu_mtbf_h,
    n_psus,
    other_mtbf_h=None,
    n_other=0,
):
    """Compound node MTBF from heterogeneous components."""
    gpu = _ensure_unit(gpu_mtbf_h, ureg.hour, "gpu_mtbf_h")
    nic = _ensure_unit(nic_mtbf_h, ureg.hour, "nic_mtbf_h")
    psu = _ensure_unit(psu_mtbf_h, ureg.hour, "psu_mtbf_h")
    rate = n_gpus / gpu + n_nics / nic + n_psus / psu
    if other_mtbf_h is not None and n_other > 0:
        rate += n_other / _ensure_unit(other_mtbf_h, ureg.hour, "other_mtbf_h")
    return (1.0 / rate).to(ureg.hour)


def calc_availability_stacked(single_availability, n_replicas):
    """System availability with k independent replicas."""
    return 1.0 - (1.0 - single_availability) ** n_replicas


def calc_failure_probability(mtbf, job_duration):
    """Probability of at least one failure during a job."""
    validate_positive(mtbf, "mtbf")
    both_qty = isinstance(mtbf, ureg.Quantity) and isinstance(job_duration, ureg.Quantity)
    either_qty = isinstance(mtbf, ureg.Quantity) or isinstance(job_duration, ureg.Quantity)
    if either_qty and not both_qty:
        raise TypeError(
            "calc_failure_probability: both arguments must be Quantities or both raw numbers. "
            "Mixed types are ambiguous — attach units to the raw number first."
        )
    if both_qty:
        ratio = job_duration.to(ureg.second).magnitude / mtbf.to(ureg.second).magnitude
    else:
        ratio = job_duration / mtbf
    return 1.0 - math.exp(-ratio)
