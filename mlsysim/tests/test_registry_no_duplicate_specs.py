"""CI gate: registry entries must not duplicate hardware interconnect specs."""

from __future__ import annotations

from mlsysim.hardware.registry import Hardware
from mlsysim.systems.registry import Systems


def _qty_equal(a, b) -> bool:
    return abs(a.m_as("byte/second") - b.m_as("byte/second")) < 1e-6


def test_nodes_intra_node_bw_matches_accelerator_nvlink() -> None:
    pairs = (
        (Systems.Nodes.DGX_H100, Hardware.Cloud.H100),
        (Systems.Nodes.DGX_A100, Hardware.Cloud.A100),
        (Systems.Nodes.DGX_B200, Hardware.Cloud.B200),
    )
    violations: list[str] = []
    for node, accel in pairs:
        expected = accel.nvlink.bandwidth
        actual = node.intra_node_bw
        if not _qty_equal(actual, expected):
            violations.append(
                f"{node.name}: intra_node_bw={actual:~P} != {accel.name} nvlink={expected:~P}"
            )
    assert not violations, "Nodes must source intra_node_bw from Hardware nvlink:\n  " + "\n  ".join(
        violations
    )


def test_fabrics_bandwidth_matches_canonical_constants() -> None:
    from mlsysim.core.constants import (
        ETHERNET_400G_BW,
        ETHERNET_800G_BW,
        NETWORK_10G_BW,
        NETWORK_100G_BW,
    )

    pairs = (
        (Systems.Fabrics.Ethernet_10G, NETWORK_10G_BW),
        (Systems.Fabrics.Ethernet_100G, NETWORK_100G_BW),
        (Systems.Fabrics.Ethernet_400G, ETHERNET_400G_BW),
        (Systems.Fabrics.Ethernet_800G, ETHERNET_800G_BW),
    )
    violations: list[str] = []
    for fabric, expected in pairs:
        actual = fabric.bandwidth
        if abs(actual.m_as("gigabit/second") - expected.m_as("gigabit/second")) > 1e-6:
            violations.append(f"{fabric.name}: {actual:~P} != canonical {expected:~P}")
    assert not violations, "Fabrics must use canonical bandwidth constants:\n  " + "\n  ".join(
        violations
    )
