"""Statistical and workflow propagation helpers."""

from __future__ import annotations

import math


def calc_population_stability_index(expected, actual, epsilon=1e-12):
    """Population Stability Index for aligned probability distributions."""
    if len(expected) != len(actual):
        raise ValueError("expected and actual distributions must have the same length")

    total = 0.0
    for exp, act in zip(expected, actual):
        exp = max(float(exp), epsilon)
        act = max(float(act), epsilon)
        total += (act - exp) * math.log(act / exp)
    return total


def calc_two_proportion_sample_size(baseline_rate, detectable_lift, z_alpha=1.96, z_beta=0.84):
    """Per-arm sample size for a two-proportion A/B test."""
    p = float(baseline_rate)
    delta = float(detectable_lift)
    variance = p * (1 - p)
    return 2 * (float(z_alpha) + float(z_beta)) ** 2 * variance / delta ** 2


def calc_constraint_propagation_factor(stage_from, stage_to, base=2):
    """Cost multiplier for finding a workflow constraint at a later lifecycle stage."""
    if stage_to < stage_from:
        raise ValueError("stage_to must be greater than or equal to stage_from")
    return int(base ** (stage_to - stage_from))
