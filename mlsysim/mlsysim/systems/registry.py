from .types import Node, Fleet, NetworkFabric, PodEnvelope
from .reliability import Reliability
from .orchestration import Orchestration
from ..core.units import ureg, Q_, Gbps, TB
from ..core.constants import (
    NETWORK_10G_BW, NETWORK_100G_BW, ETHERNET_400G_BW, ETHERNET_800G_BW,
)
from ..core.provenance import sourced
from ..hardware.registry import Hardware
from ..core.registry import Registry
from ..core.types import Metadata
from ..core import provenance_catalog as pc

# Fabric α latencies (appendix α–β model)
IB_NDR_LATENCY_US = sourced(5, pc.BOOK_FABRIC_LATENCY, name="InfiniBand NDR latency (μs)", description="One-way α latency for NDR fabrics.")
IB_HDR_LATENCY_US = sourced(7, pc.BOOK_FABRIC_LATENCY, name="InfiniBand HDR latency (μs)", description="One-way α latency for HDR fabrics.")
ROCE_LATENCY_US = sourced(10, pc.BOOK_FABRIC_LATENCY, name="RoCE latency (μs)", description="One-way α latency for RoCE v2.")
TCP_LATENCY_US = sourced(50, pc.BOOK_FABRIC_LATENCY, name="TCP latency (μs)", description="One-way α latency for TCP over Ethernet.")

_INFINIBAND_HDR_BW = 200 * Gbps
_INFINIBAND_NDR_BW = 400 * Gbps
_INFINIBAND_XDR_BW = 800 * Gbps
_INFINIBAND_GXDR_BW = 1600 * Gbps

_FABRIC_PROV = {
    "hdr": pc.INFINIBAND_HDR_GBS,
    "ndr": pc.INFINIBAND_NDR_GBS,
    "xdr": pc.INFINIBAND_XDR_GBS,
    "eth400": pc.ETHERNET_400G_GBS,
    "eth800": pc.ETHERNET_800G_GBS,
    "roce": pc.ROCE_100G_GBS,
}


class Nodes(Registry):
    """Vetted reference nodes."""
    DGX_H100 = Node(
        name="DGX H100",
        accelerator=Hardware.Cloud.H100,
        accelerators_per_node=8,
        intra_node_bw=Hardware.Cloud.H100.nvlink.bandwidth,
        nics_per_node=8,
        metadata=Metadata(provenance=pc.BOOK_DGX_GPUS_PER_HOST),
    )
    DGX_A100 = Node(
        name="DGX A100",
        accelerator=Hardware.Cloud.A100,
        accelerators_per_node=8,
        intra_node_bw=Hardware.Cloud.A100.nvlink.bandwidth,
        nics_per_node=8,
    )
    DGX_B200 = Node(
        name="DGX B200",
        accelerator=Hardware.Cloud.B200,
        accelerators_per_node=8,
        intra_node_bw=Hardware.Cloud.B200.nvlink.bandwidth,
        nics_per_node=8,
    )


class Fabrics(Registry):
    """Vetted network fabrics (canonical bandwidth + latency)."""
    Ethernet_10G = NetworkFabric(
        name="10GbE", bandwidth=NETWORK_10G_BW, latency=Q_(TCP_LATENCY_US, "us"),
        metadata=Metadata(provenance=pc.BOOK_FABRIC_LATENCY),
    )
    Ethernet_100G = NetworkFabric(
        name="100GbE", bandwidth=NETWORK_100G_BW, latency=Q_(TCP_LATENCY_US, "us"),
        metadata=Metadata(provenance=pc.BOOK_FABRIC_LATENCY),
    )
    Ethernet_400G = NetworkFabric(
        name="400GbE", bandwidth=ETHERNET_400G_BW, latency=Q_(TCP_LATENCY_US, "us"),
        metadata=Metadata(provenance=_FABRIC_PROV["eth400"]),
    )
    Ethernet_800G = NetworkFabric(
        name="800GbE", bandwidth=ETHERNET_800G_BW, latency=Q_(TCP_LATENCY_US, "us"),
        metadata=Metadata(provenance=_FABRIC_PROV["eth800"]),
    )
    RoCE_100G = NetworkFabric(
        name="100GbE RoCE", bandwidth=NETWORK_100G_BW, latency=Q_(ROCE_LATENCY_US, "us"),
        metadata=Metadata(provenance=_FABRIC_PROV["roce"]),
    )
    InfiniBand_HDR = NetworkFabric(
        name="IB HDR", bandwidth=_INFINIBAND_HDR_BW, latency=Q_(IB_HDR_LATENCY_US, "us"),
        metadata=Metadata(provenance=_FABRIC_PROV["hdr"]),
    )
    InfiniBand_NDR = NetworkFabric(
        name="IB NDR", bandwidth=_INFINIBAND_NDR_BW, latency=Q_(IB_NDR_LATENCY_US, "us"),
        metadata=Metadata(provenance=_FABRIC_PROV["ndr"]),
    )
    InfiniBand_XDR = NetworkFabric(
        name="IB XDR", bandwidth=_INFINIBAND_XDR_BW, latency=Q_(IB_NDR_LATENCY_US, "us"),
        metadata=Metadata(provenance=_FABRIC_PROV["xdr"]),
    )
    InfiniBand_GXDR = NetworkFabric(
        name="IB GXDR", bandwidth=_INFINIBAND_GXDR_BW, latency=Q_(IB_NDR_LATENCY_US, "us"),
        metadata=Metadata(provenance=_FABRIC_PROV["xdr"]),
    )


_TIER_PROV = pc.BOOK_CLUSTER_TIERS


class Clusters(Registry):
    """Book reference fleet tiers (256 / 1k / 2k / 8k / 10k / 100k GPUs)."""
    Research_256 = Fleet(
        name="Research Cluster (256 GPUs)",
        node=Nodes.DGX_H100,
        count=32,
        fabric=Fabrics.Ethernet_100G,
        metadata=Metadata(provenance=_TIER_PROV, description="Small cluster tier (256 GPUs)."),
    )
    Production_2K = Fleet(
        name="Production Cluster (2048 GPUs)",
        node=Nodes.DGX_H100,
        count=256,
        fabric=Fabrics.InfiniBand_HDR,
        metadata=Metadata(provenance=_TIER_PROV, description="Medium cluster tier (2048 GPUs)."),
    )
    Training_1K = Fleet(
        name="Training Cluster (1024 GPUs)",
        node=Nodes.DGX_H100,
        count=128,
        fabric=Fabrics.InfiniBand_HDR,
        metadata=Metadata(provenance=_TIER_PROV, description="Mid cluster tier (1024 GPUs)."),
    )
    Frontier_8K = Fleet(
        name="Frontier Cluster (8192 GPUs)",
        node=Nodes.DGX_H100,
        count=1024,
        fabric=Fabrics.InfiniBand_NDR,
        metadata=Metadata(provenance=_TIER_PROV, description="Large cluster tier (8192 GPUs)."),
    )
    Training_10K = Fleet(
        name="Training Cluster (10000 GPUs)",
        node=Nodes.DGX_H100,
        count=1250,
        fabric=Fabrics.InfiniBand_NDR,
        metadata=Metadata(provenance=_TIER_PROV, description="Large training tier (10000 GPUs)."),
    )
    Mega_100K = Fleet(
        name="Mega Cluster (100000 GPUs)",
        node=Nodes.DGX_H100,
        count=12500,
        fabric=Fabrics.InfiniBand_NDR,
        metadata=Metadata(provenance=_TIER_PROV, description="Mega cluster tier (100k GPUs)."),
    )


class Pods(Registry):
    """Reference accelerator pod envelopes (not K8s runtime)."""
    TPUv4_4096 = PodEnvelope(
        name="Cloud TPU v4 Pod (4096 chips)",
        chips=4096,
        memory=131 * TB,
        power=3 * ureg.megawatt,
        metadata=Metadata(
            provenance=pc.BOOK_CLUSTER_TIERS,
            description="Reference TPU pod envelope for Volume I cloud-scale examples.",
        ),
    )



class Systems(Registry):
    """Registry namespace for Systems."""
    Nodes = Nodes
    Clusters = Clusters
    Fabrics = Fabrics
    Pods = Pods
    Reliability = Reliability
    Orchestration = Orchestration()
