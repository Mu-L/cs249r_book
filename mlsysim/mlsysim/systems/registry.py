from .types import Node, Fleet, NetworkFabric
from ..core.units import ureg, Q_, Gbps
from ..core.constants import (
    NETWORK_10G_BW, NETWORK_100G_BW, ETHERNET_400G_BW, ETHERNET_800G_BW,
)
from ..core.defaults import IB_NDR_LATENCY_US, IB_HDR_LATENCY_US, TCP_LATENCY_US
from ..hardware.registry import Hardware
from ..core.registry import Registry

# Canonical fabric bit-rates (Systems.Fabrics is the public API).
_INFINIBAND_HDR_BW = 200 * Gbps
_INFINIBAND_NDR_BW = 400 * Gbps
_INFINIBAND_XDR_BW = 800 * Gbps
_INFINIBAND_GXDR_BW = 1600 * Gbps


class Nodes(Registry):
    """Vetted reference nodes."""
    DGX_H100 = Node(
        name="DGX H100",
        accelerator=Hardware.Cloud.H100,
        accelerators_per_node=8,
        intra_node_bw=900 * ureg.GB / ureg.second,
        nics_per_node=8,
    )
    DGX_A100 = Node(
        name="DGX A100",
        accelerator=Hardware.Cloud.A100,
        accelerators_per_node=8,
        intra_node_bw=600 * ureg.GB / ureg.second,
        nics_per_node=8,
    )
    DGX_B200 = Node(
        name="DGX B200",
        accelerator=Hardware.Cloud.B200,
        accelerators_per_node=8,
        intra_node_bw=1800 * ureg.GB / ureg.second,
        nics_per_node=8,
    )


class Fabrics(Registry):
    """Vetted network fabrics."""
    Ethernet_10G = NetworkFabric(name="10GbE", bandwidth=NETWORK_10G_BW, latency=Q_(TCP_LATENCY_US, "us"))
    Ethernet_100G = NetworkFabric(name="100GbE", bandwidth=NETWORK_100G_BW, latency=Q_(TCP_LATENCY_US, "us"))
    Ethernet_400G = NetworkFabric(name="400GbE", bandwidth=ETHERNET_400G_BW, latency=Q_(TCP_LATENCY_US, "us"))
    Ethernet_800G = NetworkFabric(name="800GbE", bandwidth=ETHERNET_800G_BW, latency=Q_(TCP_LATENCY_US, "us"))
    InfiniBand_HDR = NetworkFabric(name="IB HDR", bandwidth=_INFINIBAND_HDR_BW, latency=Q_(IB_HDR_LATENCY_US, "us"))
    InfiniBand_NDR = NetworkFabric(name="IB NDR", bandwidth=_INFINIBAND_NDR_BW, latency=Q_(IB_NDR_LATENCY_US, "us"))
    InfiniBand_XDR = NetworkFabric(name="IB XDR", bandwidth=_INFINIBAND_XDR_BW, latency=Q_(IB_NDR_LATENCY_US, "us"))
    InfiniBand_GXDR = NetworkFabric(name="IB GXDR", bandwidth=_INFINIBAND_GXDR_BW, latency=Q_(IB_NDR_LATENCY_US, "us"))


class Clusters(Registry):
    """Vetted production fleets."""
    Research_256 = Fleet(
        name="Research Cluster (256 GPUs)",
        node=Nodes.DGX_H100,
        count=32,
        fabric=Fabrics.Ethernet_100G,
    )
    Frontier_8K = Fleet(
        name="Frontier Cluster (8192 GPUs)",
        node=Nodes.DGX_H100,
        count=1024,
        fabric=Fabrics.InfiniBand_NDR,
    )
    Production_2K = Fleet(
        name="Production Cluster (2048 GPUs)",
        node=Nodes.DGX_H100,
        count=256,
        fabric=Fabrics.InfiniBand_HDR,
    )
    Mega_100K = Fleet(
        name="Mega Cluster (100000 GPUs)",
        node=Nodes.DGX_H100,
        count=12500,
        fabric=Fabrics.InfiniBand_NDR,
    )


class Pods(Registry):
    """Kubernetes-style pod scaffold (populated in later phases)."""


class Systems(Registry):
    Nodes = Nodes
    Clusters = Clusters
    Fabrics = Fabrics
    Pods = Pods
