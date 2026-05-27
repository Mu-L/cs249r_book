from .types import HardwareNode, ComputeCore, MemoryHierarchy, StorageHierarchy, IOInterconnect
from ..core.registry import Registry
from ..core.provenance import Provenance, ProvenanceKind
from ..core import provenance_catalog as pc
from ..core.constants import (
    GB, GiB, MB, PB, PFLOPs, TB, TFLOPs, TOPS, USD, kilowatt, ms, second, ureg, watt,
    LATENCY_NVLINK,
)

_H100_L2_CACHE = 50 * MB
_TPUV5P_L2_SRAM = 100 * MB
_SGX_EPC_CAPACITY = 128 * MB
_SGX_BASE_LATENCY = 5 * ms
_REFERENCE_CPU_FP32 = 1 * TFLOPs / second

class CloudHardware(Registry):
    """Datacenter-scale accelerators (Volume II)."""
    V100 = HardwareNode(
        name="NVIDIA V100",
        release_year=2017,
        compute=ComputeCore(peak_flops=125 * TFLOPs / second, precision_flops={"fp32": 15.7 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=32 * GiB, bandwidth=900 * GB / second),
        interconnect=IOInterconnect(name="PCIe Gen3 x16", bandwidth=15.75 * GB / second),
        nvlink=IOInterconnect(name="NVLink 2.0", bandwidth=300 * GB / second, latency=LATENCY_NVLINK),
        tdp=300 * watt,
        unit_cost=10000 * USD,
        dispatch_tax=0.02 * ureg.ms,
        metadata={
            "provenance": Provenance(
                id="prov:nvidia-v100-datasheet",
                kind=ProvenanceKind.DATASHEET,
                ref="NVIDIA V100 architecture whitepaper",
                url="https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf",
                verified="2025-03-06",
            ),
        },
    )

    A100 = HardwareNode(
        name="NVIDIA A100",
        release_year=2020,
        compute=ComputeCore(peak_flops=312 * TFLOPs / second, precision_flops={"fp32": 19.5 * TFLOPs / second, "tf32": 156 * TFLOPs / second, "int8": 624 * TOPS, "fp16_sparse": 624 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=80 * GiB, bandwidth=2039 * GB / second),
        interconnect=IOInterconnect(name="PCIe Gen4 x16", bandwidth=32 * GB / second),
        nvlink=IOInterconnect(name="NVLink 3.0", bandwidth=600 * GB / second, latency=LATENCY_NVLINK),
        tdp=400 * watt,
        unit_cost=15000 * USD,
        embodied_carbon_kg=130.0,  # Gupta et al. 2022 estimate
        dispatch_tax=0.015 * ureg.ms,
        metadata={
            "provenance": Provenance(
                id="prov:nvidia-a100-datasheet",
                kind=ProvenanceKind.DATASHEET,
                ref="NVIDIA A100 datasheet; Choquette et al. (2021), IEEE Micro",
                url="https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf",
                verified="2025-03-06",
            ),
        },
    )

    H100 = HardwareNode(
        name="NVIDIA H100",
        release_year=2022,
        compute=ComputeCore(peak_flops=989 * TFLOPs / second, precision_flops={"tf32": 494 * TFLOPs / second, "fp8": 1979 * TFLOPs / second, "int8": 1979 * TOPS, "fp32_cuda": 67 * TFLOPs / second}),
        memory=MemoryHierarchy(
            capacity=80 * GiB,
            bandwidth=3.35 * TB / second,
            l2_cache=_H100_L2_CACHE,
        ),
        storage=StorageHierarchy(capacity=2 * ureg.TB, bandwidth=7.0 * GB / second),
        interconnect=IOInterconnect(name="PCIe Gen5 x16", bandwidth=64 * GB / second),
        nvlink=IOInterconnect(name="NVLink 4.0", bandwidth=900 * GB / second, latency=LATENCY_NVLINK),
        tdp=700 * watt,
        unit_cost=30000 * USD,
        embodied_carbon_kg=150.0,  # Gupta et al. 2022 estimate for high-end datacenter GPU
        dispatch_tax=0.01 * ureg.ms,
        metadata={
            "provenance": Provenance(
                id="prov:nvidia-h100-datasheet",
                kind=ProvenanceKind.DATASHEET,
                ref="NVIDIA H100 datasheet; Choquette (2023), IEEE Micro",
                url="https://resources.nvidia.com/en-us-tensor-core/nvidia-h100-tensor-core-gpu-datasheet",
                verified="2025-03-06",
            ),
        },
    )

    H200 = HardwareNode(
        name="NVIDIA H200",
        release_year=2023,
        compute=ComputeCore(peak_flops=989 * TFLOPs / second, precision_flops={"tf32": 494 * TFLOPs / second, "fp8": 1979 * TFLOPs / second, "int8": 1979 * TOPS, "fp32_cuda": 67 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=131 * GiB, bandwidth=4.8 * TB / second),
        storage=StorageHierarchy(capacity=4 * ureg.TB, bandwidth=7.0 * GB / second),
        interconnect=IOInterconnect(name="PCIe Gen5 x16", bandwidth=64 * GB / second),
        nvlink=IOInterconnect(name="NVLink 4.0", bandwidth=900 * GB / second, latency=LATENCY_NVLINK),
        tdp=700 * watt,
        unit_cost=35000 * USD,
        dispatch_tax=0.01 * ureg.ms,
        metadata={"provenance": pc.NVIDIA_H200},
    )

    B200 = HardwareNode(
        name="NVIDIA B200",
        release_year=2024,
        compute=ComputeCore(peak_flops=4500 * TFLOPs / second, precision_flops={"fp8": 9000 * TFLOPs / second, "fp4": 18000 * TFLOPs / second, "int4": 18000 * TOPS}),
        memory=MemoryHierarchy(capacity=192 * GiB, bandwidth=8 * TB / second),
        interconnect=IOInterconnect(name="PCIe Gen5 x16", bandwidth=64 * GB / second),
        nvlink=IOInterconnect(name="NVLink 5.0", bandwidth=1800 * GB / second, latency=LATENCY_NVLINK),
        tdp=1000 * watt,
        unit_cost=40000 * USD,
        dispatch_tax=0.008 * ureg.ms,
        metadata={
            "provenance": Provenance(
                id="prov:nvidia-b200-datasheet",
                kind=ProvenanceKind.DATASHEET,
                ref="NVIDIA Blackwell product documentation",
                url="https://www.nvidia.com/en-us/data-center/blackwell/",
                verified="2025-03-06",
            ),
        },
    )

    GB200_NVL72 = HardwareNode(
        name="NVIDIA GB200 NVL72",
        release_year=2024,
        compute=ComputeCore(
            peak_flops=324 * PFLOPs / second,
            precision_flops={
                "fp16": 324 * PFLOPs / second,
                "bf16": 324 * PFLOPs / second,
                "fp8": 648 * PFLOPs / second,
                "fp4": 1440 * PFLOPs / second,
            },
        ),
        memory=MemoryHierarchy(capacity=13.8 * TB, bandwidth=576 * TB / second),
        interconnect=IOInterconnect(name="NVLink Switch (Bisection)", bandwidth=130 * TB / second),
        tdp=120 * kilowatt,
        unit_cost=3000000 * USD,
        accelerator_count=72,
        dispatch_tax=0.005 * ureg.ms,
        metadata={"provenance": pc.NVIDIA_GB200_NVL72},
    )

    MI300X = HardwareNode(
        name="AMD MI300X",
        release_year=2023,
        compute=ComputeCore(peak_flops=1307 * TFLOPs / second, precision_flops={"fp8": 2614 * TFLOPs / second, "int8": 2614 * TOPS, "fp32": 163.4 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=192 * GiB, bandwidth=5.3 * TB / second),
        tdp=750 * watt,
        unit_cost=15000 * USD,
        dispatch_tax=0.012 * ureg.ms,
        metadata={
            "provenance": Provenance(
                id="prov:amd-mi300x-datasheet",
                kind=ProvenanceKind.DATASHEET,
                ref="AMD Instinct MI300X product documentation",
                url="https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html",
                verified="2025-03-06",
            ),
        },
    )

    MI250X = HardwareNode(
        name="AMD MI250X",
        release_year=2021,
        compute=ComputeCore(peak_flops=383 * TFLOPs / second, precision_flops={"fp32": 47.9 * TFLOPs / second, "int8": 383 * TOPS}),
        memory=MemoryHierarchy(capacity=128 * GiB, bandwidth=3.2 * TB / second),
        tdp=500 * watt,
        dispatch_tax=0.015 * ureg.ms,
        metadata={"provenance": pc.AMD_MI250X},
    )

    Gaudi2 = HardwareNode(
        name="Intel Gaudi 2",
        release_year=2022,
        compute=ComputeCore(peak_flops=432 * TFLOPs / second, precision_flops={"fp8": 865 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=96 * GiB, bandwidth=2.45 * TB / second),
        tdp=600 * watt,
        dispatch_tax=0.02 * ureg.ms,
        metadata={"provenance": pc.INTEL_GAUDI2},
    )

    Gaudi3 = HardwareNode(
        name="Intel Gaudi 3",
        release_year=2024,
        compute=ComputeCore(peak_flops=1835 * TFLOPs / second, precision_flops={"fp8": 3670 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=128 * GiB, bandwidth=3.7 * TB / second),
        tdp=900 * watt,
        dispatch_tax=0.01 * ureg.ms,
        metadata={"provenance": pc.INTEL_GAUDI3},
    )

    Trainium2 = HardwareNode(
        name="AWS Trainium 2",
        release_year=2024,
        compute=ComputeCore(peak_flops=380 * TFLOPs / second, precision_flops={"fp8": 760 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=96 * GiB, bandwidth=2.4 * TB / second),
        tdp=500 * watt,
        dispatch_tax=0.02 * ureg.ms,
        metadata={"provenance": pc.AWS_TRAINIUM2},
    )

    TPUv6 = HardwareNode(
        name="Google TPU v6 (Trillium)",
        release_year=2024,
        compute=ComputeCore(peak_flops=918 * TFLOPs / second),
        memory=MemoryHierarchy(capacity=32 * GiB, bandwidth=1600 * GB / second),
        tdp=300 * ureg.W,
        dispatch_tax=0.04 * ureg.ms,
        metadata={"provenance": pc.GOOGLE_TPU_V6},
    )

    TPUv5p = HardwareNode(
        name="Google TPU v5p",
        release_year=2023,
        compute=ComputeCore(peak_flops=459 * TFLOPs / second, precision_flops={"int8": 918 * TOPS}),
        memory=MemoryHierarchy(
            capacity=95 * GiB,
            bandwidth=2.76 * TB / second,
            l2_cache=_TPUV5P_L2_SRAM,
        ),
        nvlink=IOInterconnect(name="ICI", bandwidth=1200 * GB / second),
        tdp=300 * watt,
        dispatch_tax=0.04 * ureg.ms,
        metadata={"provenance": pc.GOOGLE_TPU_V5P},
    )

    TPUv1 = HardwareNode(
        name="Google TPU v1",
        release_year=2017,
        compute=ComputeCore(peak_flops=92 * TOPS, precision_flops={"int8": 92 * TOPS}),
        memory=MemoryHierarchy(capacity=8 * GiB, bandwidth=34 * GB / second),
        tdp=75 * watt,
        dispatch_tax=0.05 * ureg.ms,
        metadata={"provenance": pc.GOOGLE_TPU_V1},
    )

    TPUv2 = HardwareNode(
        name="Google TPU v2",
        release_year=2018,
        compute=ComputeCore(peak_flops=45 * TFLOPs / second, precision_flops={"bf16": 45 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=16 * GiB, bandwidth=700 * GB / second),
        tdp=200 * watt,
        dispatch_tax=0.04 * ureg.ms,
        metadata={"provenance": pc.GOOGLE_TPU_V2_V3},
    )

    TPUv3 = HardwareNode(
        name="Google TPU v3",
        release_year=2019,
        compute=ComputeCore(peak_flops=105 * TFLOPs / second, precision_flops={"bf16": 105 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=32 * GiB, bandwidth=900 * GB / second),
        tdp=250 * watt,
        dispatch_tax=0.04 * ureg.ms,
        metadata={"provenance": pc.GOOGLE_TPU_V2_V3},
    )

    TPUv4 = HardwareNode(
        name="Google TPU v4",
        release_year=2021,
        compute=ComputeCore(peak_flops=275 * TFLOPs / second, precision_flops={"bf16": 275 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=32 * ureg.GiB, bandwidth=1200 * GB / second),
        tdp=200 * ureg.W,
        dispatch_tax=0.04 * ureg.ms,
        metadata={"provenance": pc.GOOGLE_TPU_V4},
    )

    ReferenceCPU = HardwareNode(
        name="Reference Desktop CPU",
        release_year=2024,
        compute=ComputeCore(
            peak_flops=_REFERENCE_CPU_FP32,
            precision_flops={"fp32": _REFERENCE_CPU_FP32},
        ),
        memory=MemoryHierarchy(capacity=64 * GiB, bandwidth=50 * GB / second),
        tdp=150 * watt,
        dispatch_tax=0.1 * ureg.ms,
        metadata={"provenance": pc.BOOK_REFERENCE_CPU},
    )

    IntelSGX = HardwareNode(
        name="Intel SGX Enclave (Reference)",
        release_year=2020,
        compute=ComputeCore(peak_flops=_REFERENCE_CPU_FP32, precision_flops={"fp32": _REFERENCE_CPU_FP32}),
        memory=MemoryHierarchy(
            capacity=_SGX_EPC_CAPACITY,
            bandwidth=10 * GB / second,
            sram_capacity=_SGX_EPC_CAPACITY,
        ),
        dispatch_tax=_SGX_BASE_LATENCY,
        metadata={"provenance": pc.INTEL_SGX},
    )

    T4 = HardwareNode(
        name="NVIDIA T4",
        release_year=2018,
        compute=ComputeCore(peak_flops=65 * TFLOPs / second, precision_flops={"int8": 130 * TOPS}),
        memory=MemoryHierarchy(capacity=16 * ureg.GiB, bandwidth=320 * GB / second),
        tdp=70 * watt,
        unit_cost=2500 * USD,
        dispatch_tax=0.03 * ureg.ms,
        metadata={
            "provenance": Provenance(
                id="prov:nvidia-t4-datasheet",
                kind=ProvenanceKind.DATASHEET,
                ref="NVIDIA Tesla T4 product documentation",
                url="https://www.nvidia.com/en-us/data-center/tesla-t4/",
                verified="2025-03-06",
            ),
        },
    )

    Cerebras_CS3 = HardwareNode(
        name="Cerebras CS-3 (WSE-3)",
        release_year=2024,
        # A single WSE acts as a gigantic compute core with minimal dispatch tax
        compute=ComputeCore(peak_flops=125 * PFLOPs / second),
        # Memory reflects the 44GB on-wafer SRAM, meaning large weights must stream from MemoryX
        memory=MemoryHierarchy(capacity=44 * GB, bandwidth=21 * PB / second),
        # Injection bandwidth from MemoryX (approx 1.2 TB/s per WSE)
        interconnect=IOInterconnect(name="SwarmX / MemoryX", bandwidth=1.2 * ureg.TB / ureg.second),
        tdp=23000 * watt,
        unit_cost=2000000 * USD,
        dispatch_tax=0.001 * ureg.ms,
        metadata={"provenance": pc.CEREBRAS_CS3},
    )

class WorkstationHardware(Registry):
    """Personal computing systems used for local development."""
    DGX_Spark = HardwareNode(
        name="NVIDIA DGX Spark (GB10)",
        release_year=2024,
        compute=ComputeCore(
            peak_flops=250 * ureg.TFLOPs/ureg.s,
            precision_flops={"fp8": 500 * ureg.TFLOPs/ureg.s, "fp4": 1000 * ureg.TFLOPs/ureg.s}
        ),
        memory=MemoryHierarchy(capacity=128 * ureg.GB, bandwidth=500 * ureg.GB/ureg.s),
        storage=StorageHierarchy(capacity=4 * TB, bandwidth=7 * GB / second),
        tdp=200 * watt,
        unit_cost=3000 * USD,
        unit_cost_max=5000 * USD,
        dispatch_tax=0.01 * ureg.ms,
        metadata={"provenance": pc.NVIDIA_DGX_SPARK},
    )

    MacBookM3Max = HardwareNode(
        name="MacBook Pro (M3 Max)",
        release_year=2023,
        compute=ComputeCore(peak_flops=14.2 * ureg.TFLOPs/ureg.s),
        memory=MemoryHierarchy(capacity=128 * ureg.GB, bandwidth=400 * ureg.GB/ureg.s),
        tdp=100 * ureg.W,
        dispatch_tax=0.05 * ureg.ms,
        metadata={"provenance": pc.APPLE_M3_MAX},
    )

class MobileHardware(Registry):
    """Smartphone and handheld devices (Volume I)."""
    iPhone15Pro = HardwareNode(
        name="iPhone 15 Pro (A17 Pro)",
        release_year=2023,
        compute=ComputeCore(peak_flops=35 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=8 * ureg.GB, bandwidth=100 * ureg.GB/ureg.s),
        tdp=5 * ureg.W,
        battery_capacity=15 * ureg.Wh,
        dispatch_tax=1.0 * ureg.ms,
        metadata={"provenance": pc.MOBILE_SOC_ESTIMATE},
    )

    Pixel8 = HardwareNode(
        name="Google Pixel 8 (Tensor G3)",
        release_year=2023,
        compute=ComputeCore(peak_flops=15 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=8 * ureg.GB, bandwidth=60 * ureg.GB/ureg.s),
        tdp=5 * ureg.W,
        dispatch_tax=1.2 * ureg.ms,
        metadata={"provenance": pc.MOBILE_SOC_ESTIMATE},
    )

    Snapdragon8Gen3 = HardwareNode(
        name="Snapdragon 8 Gen 3",
        release_year=2023,
        compute=ComputeCore(peak_flops=45 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=12 * ureg.GB, bandwidth=77 * ureg.GB/ureg.s),
        tdp=5 * ureg.W,
        dispatch_tax=1.5 * ureg.ms,
        metadata={"provenance": pc.MOBILE_SOC_ESTIMATE},
    )

class EdgeHardware(Registry):
    """Robotics and Industrial Edge (Volume I)."""
    JetsonAGXOrin = HardwareNode(
        name="NVIDIA Jetson AGX Orin",
        release_year=2022,
        compute=ComputeCore(peak_flops=275 * TOPS, precision_flops={"int8": 275 * TOPS}),
        memory=MemoryHierarchy(capacity=64 * ureg.GB, bandwidth=204 * ureg.GB/ureg.s),
        tdp=60 * watt,
        tdp_min=15 * watt,
        tdp_max=60 * watt,
        dispatch_tax=0.2 * ureg.ms,
        metadata={"provenance": pc.NVIDIA_JETSON_AGX_ORIN},
    )
    JetsonOrinNX = HardwareNode(
        name="NVIDIA Jetson Orin NX",
        release_year=2023,
        compute=ComputeCore(peak_flops=25 * ureg.TFLOPs/ureg.s, precision_flops={"int8": 100 * ureg.TOPS}),
        memory=MemoryHierarchy(capacity=16 * ureg.GB, bandwidth=102 * ureg.GB/ureg.s),
        tdp=25 * ureg.W,
        dispatch_tax=0.2 * ureg.ms,
        metadata={"provenance": pc.NVIDIA_JETSON_ORIN_NX},
    )

    Coral = HardwareNode(
        name="Google Coral Edge TPU",
        release_year=2019,
        compute=ComputeCore(peak_flops=4 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=1 * ureg.GB, bandwidth=8 * ureg.GB/ureg.s),
        tdp=2 * ureg.W,
        dispatch_tax=1.0 * ureg.ms,
        metadata={"provenance": pc.GOOGLE_CORAL},
    )

    NUC_Movidius = HardwareNode(
        name="Intel NUC + Movidius",
        release_year=2020,
        compute=ComputeCore(peak_flops=1 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=16 * ureg.GB, bandwidth=25 * ureg.GB/ureg.s),
        tdp=15 * ureg.W,
        dispatch_tax=2.0 * ureg.ms,
        metadata={"provenance": pc.INTEL_NUC_MOVIDIUS},
    )

    GenericServer = HardwareNode(
        name="Edge Server",
        release_year=2024,
        compute=ComputeCore(peak_flops=1 * ureg.TFLOPs/ureg.s),
        memory=MemoryHierarchy(capacity=128 * ureg.GB, bandwidth=100 * ureg.GB/ureg.s),
        tdp=300 * ureg.W,
        dispatch_tax=0.1 * ureg.ms,
        metadata={"provenance": pc.BOOK_EDGE_SERVER},
    )

class TinyHardware(Registry):
    """Microcontrollers and sub-watt devices."""
    ESP32_S3 = HardwareNode(
        name="ESP32-S3 (AI)",
        release_year=2022,
        # ESP32-S3 has no FP16 hardware; INT8 via vector extensions.
        # ~2.4 GOPS INT8 (240 MHz dual-core, vector instructions)
        compute=ComputeCore(
            peak_flops=0.0005 * ureg.TFLOPs/ureg.s,
            precision_flops={"int8": 0.0024 * ureg.TOPS}
        ),
        # 512 KiB SRAM (usable ~256 KiB after RTOS/stack); 8 MB flash for weights
        # capacity/bandwidth = flash (default path for large models)
        # sram_capacity/bandwidth = on-chip SRAM (used when model fits)
        memory=MemoryHierarchy(
            capacity=4 * ureg.MB,
            bandwidth=0.08 * ureg.GB/ureg.s,
            sram_capacity=520 * ureg.KiB,
            sram_bandwidth=0.96 * ureg.GB/ureg.s,
            flash_capacity=4 * ureg.MB,
            flash_bandwidth=0.08 * ureg.GB/ureg.s,
        ),
        tdp=0.4 * ureg.W,
        tdp_min=0.05 * watt,
        tdp_max=1.2 * watt,
        embodied_carbon_kg=5.0,
        dispatch_tax=1.0 * ureg.ms,
        metadata={"provenance": pc.ESP32_S3},
    )

    nRF52840 = HardwareNode(
        name="Nordic nRF52840 (Cortex-M4F)",
        release_year=2018,
        # MLPerf Tiny reference platform. Cortex-M4F @ 64 MHz.
        compute=ComputeCore(
            peak_flops=0.000064 * ureg.TFLOPs/ureg.s,  # ~64 MFLOP/s (single-precision)
            precision_flops={"int8": 0.000128 * ureg.TOPS}  # ~128 MOPS INT8
        ),
        memory=MemoryHierarchy(
            capacity=1 * ureg.MB,                     # Flash (primary weight storage)
            bandwidth=0.064 * ureg.GB/ureg.s,         # Flash read ~64 MB/s
            sram_capacity=256 * ureg.KiB,             # On-chip SRAM
            sram_bandwidth=0.256 * ureg.GB/ureg.s,    # SRAM bandwidth @ 64 MHz
            flash_capacity=1 * ureg.MB,               # 1 MB internal flash
            flash_bandwidth=0.064 * ureg.GB/ureg.s,   # Flash read ~64 MB/s
        ),
        tdp=0.015 * ureg.W,            # ~15 mW active inference
        dispatch_tax=0.5 * ureg.ms,
        metadata={"provenance": pc.NORDIC_NRF52840},
    )

    HimaxWE1 = HardwareNode(
        name="Himax WE-I Plus",
        release_year=2020,
        compute=ComputeCore(peak_flops=0.0002 * ureg.TFLOPs/ureg.s),
        memory=MemoryHierarchy(capacity=2 * ureg.MB, bandwidth=0.1 * ureg.GB/ureg.s),
        tdp=0.005 * ureg.W,
        dispatch_tax=2.0 * ureg.ms,
        metadata={"provenance": pc.HIMAX_WE1},
    )

class Hardware(Registry):
    """Registry namespace for Hardware."""
    Cloud = CloudHardware
    Workstation = WorkstationHardware
    Mobile = MobileHardware
    Edge = EdgeHardware
    Tiny = TinyHardware

