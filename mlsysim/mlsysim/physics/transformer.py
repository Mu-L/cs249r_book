"""Transformer FLOP accounting identities."""

from __future__ import annotations

from mlsysim.core.constants import (
    ureg,
    TRANSFORMER_DECODE_FLOPS_PER_PARAM,
    TRANSFORMER_TRAINING_FLOPS_PER_PARAM_TOKEN,
)

from ._units import _ensure_unit


def calc_transformer_training_flops(n_params, n_tokens):
    """Training FLOPs for a Transformer (6PD rule, Kaplan et al. 2020)."""
    p = _ensure_unit(n_params, ureg.param, "n_params").to(ureg.count).magnitude
    d = _ensure_unit(n_tokens, ureg.count, "n_tokens").magnitude
    return (TRANSFORMER_TRAINING_FLOPS_PER_PARAM_TOKEN * p * d) * ureg.flop


def calc_transformer_decode_flops(n_params, n_tokens=1):
    """Autoregressive decode FLOPs using the 2P rule."""
    p = _ensure_unit(n_params, ureg.param, "n_params").to(ureg.count).magnitude
    t = _ensure_unit(n_tokens, ureg.count, "n_tokens").magnitude
    return (TRANSFORMER_DECODE_FLOPS_PER_PARAM * p * t) * ureg.flop
