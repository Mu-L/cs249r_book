"""Inference serving and queueing models."""

from __future__ import annotations

import math

from mlsysim.core.constants import ureg

from ._units import _ensure_unit


def calc_queue_latency_mmc(arrival_rate_hz, service_rate_hz, num_servers):
    """
    M/M/c queueing model for inference tail latency (Erlang C).

    Calculates the expected queueing delays (P50 and P99) for a system with 
    Markovian arrivals, Markovian service times, and `c` parallel servers.

    This implementation uses the Log-Sum-Exp trick to calculate the Erlang C 
    formula. This prevents floating-point overflow (`math.inf`) or underflow 
    to `0.0` when dealing with large-scale clusters (e.g., c > 100).

    Parameters
    ----------
    arrival_rate_hz : Quantity or float
        The average rate of incoming requests (λ) in requests per second (Hz).
    service_rate_hz : Quantity or float
        The average rate at which a single server completes requests (μ) in Hz.
    num_servers : int
        The number of active parallel serving replicas (c).

    Returns
    -------
    tuple
        A 3-tuple containing:
        - rho (float): Server utilization (λ / (c * μ)).
        - p50_wait (Quantity): The 50th percentile queueing wait time.
        - p99_wait (Quantity): The 99th percentile queueing wait time.
    """
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
