"""Collective communication time models (α–β)."""

from __future__ import annotations

import math

from mlsysim.core.constants import ureg, Q_
from mlsysim.core._validation import validate_positive, validate_at_least

from ._units import _ensure_unit


def calc_ring_allreduce_time(message_bytes, n_gpus, bandwidth_bytes_s, latency_s):
    """Ring AllReduce: T = 2(N-1)/N × M/β + 2(N-1) × α."""
    validate_at_least(n_gpus, 1, "n_gpus")
    if n_gpus == 1:
        return Q_("0 second")
    msg = _ensure_unit(message_bytes, ureg.byte, "message_bytes")
    bw = _ensure_unit(bandwidth_bytes_s, ureg.byte / ureg.second, "bandwidth_bytes_s")
    validate_positive(bw, "bandwidth_bytes_s")
    lat = _ensure_unit(latency_s, ureg.second, "latency_s")
    n = n_gpus
    bw_term = 2 * (n - 1) / n * msg / bw
    lat_term = 2 * (n - 1) * lat
    return (bw_term + lat_term).to(ureg.second)


def calc_tree_allreduce_time(message_bytes, n_gpus, bandwidth_bytes_s, latency_s):
    """Tree AllReduce: T = 2 log₂(N) × M/β + 2 log₂(N) × α."""
    validate_at_least(n_gpus, 1, "n_gpus")
    if n_gpus == 1:
        return Q_("0 second")
    msg = _ensure_unit(message_bytes, ureg.byte, "message_bytes")
    bw = _ensure_unit(bandwidth_bytes_s, ureg.byte / ureg.second, "bandwidth_bytes_s")
    validate_positive(bw, "bandwidth_bytes_s")
    lat = _ensure_unit(latency_s, ureg.second, "latency_s")
    log_n = math.ceil(math.log2(max(n_gpus, 2)))
    bw_term = 2 * log_n * msg / bw
    lat_term = 2 * log_n * lat
    return (bw_term + lat_term).to(ureg.second)


def calc_all_to_all_time(message_bytes, n_gpus, bandwidth_bytes_s, latency_s):
    """All-to-All: T = (N-1)/N × M/β + (N-1) × α."""
    validate_at_least(n_gpus, 1, "n_gpus")
    msg = _ensure_unit(message_bytes, ureg.byte, "message_bytes")
    bw = _ensure_unit(bandwidth_bytes_s, ureg.byte / ureg.second, "bandwidth_bytes_s")
    lat = _ensure_unit(latency_s, ureg.second, "latency_s")
    n = n_gpus
    bw_term = (n - 1) / n * msg / bw
    lat_term = (n - 1) * lat
    return (bw_term + lat_term).to(ureg.second)


def calc_hierarchical_allreduce_time(
    message_bytes,
    n_nodes,
    gpus_per_node,
    intra_node_bw,
    inter_node_bw,
    intra_node_lat=Q_("500 ns"),
    inter_node_lat=Q_("5 us"),
):
    """Hierarchical AllReduce (intra-node NVLink + inter-node IB)."""
    t_reduce = calc_ring_allreduce_time(
        message_bytes, gpus_per_node, intra_node_bw, intra_node_lat
    )
    reduced_message = _ensure_unit(message_bytes, ureg.byte, "message_bytes") / gpus_per_node
    t_allreduce_inter = calc_ring_allreduce_time(
        reduced_message, n_nodes, inter_node_bw, inter_node_lat
    )
    t_broadcast = calc_ring_allreduce_time(
        reduced_message, gpus_per_node, intra_node_bw, intra_node_lat
    )
    return t_reduce + t_allreduce_inter + t_broadcast
