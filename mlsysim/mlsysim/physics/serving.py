"""Inference serving and queueing models."""

from __future__ import annotations

import math

from mlsysim.core.constants import ureg

from ._units import _ensure_unit


def calc_queue_latency_mmc(arrival_rate_hz, service_rate_hz, num_servers):
    """M/M/c queueing model for inference tail latency (Erlang C)."""
    lam = _ensure_unit(arrival_rate_hz, ureg.hertz, "arrival_rate_hz").magnitude
    mu = _ensure_unit(service_rate_hz, ureg.hertz, "service_rate_hz").magnitude
    c = max(1, int(num_servers))

    if lam >= c * mu or mu == 0:
        return 1.0, float("inf") * ureg.second, float("inf") * ureg.second

    rho = lam / (c * mu)
    a = c * rho
    try:
        log_last = c * math.log(a) - math.lgamma(c + 1) - math.log(1 - rho)
        log_terms = [
            i * math.log(a) - math.lgamma(i + 1) if a > 0 else (-math.inf if i > 0 else 0.0)
            for i in range(c)
        ]
        max_log = max(max(log_terms) if log_terms else -math.inf, log_last)
        sum_exp = sum(math.exp(t - max_log) for t in log_terms) + math.exp(log_last - max_log)
        p_wait = math.exp(log_last - max_log) / sum_exp
    except (OverflowError, ValueError, ZeroDivisionError):
        p_wait = rho

    if math.isnan(p_wait) or math.isinf(p_wait):
        p_wait = rho
    p_wait = max(0.0, min(1.0, p_wait))

    rate_param = c * mu * (1 - rho)
    p50_wait = 0.0 if p_wait < 0.5 else -math.log(0.5 / p_wait) / rate_param
    p99_wait = 0.0 if p_wait < 0.01 else -math.log(0.01 / p_wait) / rate_param
    return rho, p50_wait * ureg.second, p99_wait * ureg.second
