from .types import HardwareNode, ComputeCore, MemoryHierarchy, StorageHierarchy, IOInterconnect
from ..core.registry import Registry
from ..core.constants import (GB, GiB, PB, PFLOPs, TB, TFLOPs, TOPS, USD, kilowatt, second, ureg, watt)

class CloudHardware(Registry):
    """Datacenter-scale accelerators (Volume II)."""
    V100 = HardwareNode(
        name="NVIDIA V100",
        release_year=2017,
        compute=ComputeCore(peak_flops=125 * TFLOPs / second, precision_flops={"fp32": 15.7 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=32 * GiB, bandwidth=900 * GB / second),
        interconnect=IOInterconnect(name="PCIe Gen3 x16", bandwidth=15.75 * GB / second),
        tdp=300 * watt,
        unit_cost=10000 * USD,
        dispatch_tax=0.02 * ureg.ms
    )

    A100 = HardwareNode(
        name="NVIDIA A100",
        release_year=2020,
        compute=ComputeCore(peak_flops=312 * TFLOPs / second, precision_flops={"fp32": 19.5 * TFLOPs / second, "tf32": 156 * TFLOPs / second, "int8": 624 * TOPS}),
        memory=MemoryHierarchy(capacity=80 * GiB, bandwidth=2039 * GB / second),
        interconnect=IOInterconnect(name="PCIe Gen4 x16", bandwidth=32 * GB / second),
        tdp=400 * watt,
        unit_cost=15000 * USD,
        embodied_carbon_kg=130.0,  # Gupta et al. 2022 estimate
        dispatch_tax=0.015 * ureg.ms,
        metadata={"source_url": "https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf", "last_verified": "2025-03-06"}
    )

    H100 = HardwareNode(
        name="NVIDIA H100",
        release_year=2022,
        compute=ComputeCore(peak_flops=989 * TFLOPs / second, precision_flops={"tf32": 494 * TFLOPs / second, "fp8": 1979 * TFLOPs / second, "int8": 1979 * TOPS}),
        memory=MemoryHierarchy(capacity=80 * GiB, bandwidth=3.35 * TB / second),
        storage=StorageHierarchy(capacity=2 * ureg.TB, bandwidth=7.0 * GB / second),
        interconnect=IOInterconnect(name="PCIe Gen5 x16", bandwidth=64 * GB / second),
        tdp=700 * watt,
        unit_cost=30000 * USD,
        embodied_carbon_kg=150.0,  # Gupta et al. 2022 estimate for high-end datacenter GPU
        dispatch_tax=0.01 * ureg.ms,
        metadata={"source_url": "https://resources.nvidia.com/en-us-tensor-core/nvidia-h100-tensor-core-gpu-datasheet", "last_verified": "2025-03-06"}
    )

    H200 = HardwareNode(
        name="NVIDIA H200",
        release_year=2023,
        compute=ComputeCore(peak_flops=989 * TFLOPs / second, precision_flops={"tf32": 494 * TFLOPs / second, "fp8": 1979 * TFLOPs / second, "int8": 1979 * TOPS}),
        memory=MemoryHierarchy(capacity=131 * GiB, bandwidth=4.8 * TB / second),
        storage=StorageHierarchy(capacity=4 * ureg.TB, bandwidth=7.0 * GB / second),
        interconnect=IOInterconnect(name="PCIe Gen5 x16", bandwidth=64 * GB / second),
        tdp=700 * watt,
        unit_cost=35000 * USD,
        dispatch_tax=0.01 * ureg.ms
    )

    B200 = HardwareNode(
        name="NVIDIA B200",
        release_year=2024,
        compute=ComputeCore(peak_flops=2250 * TFLOPs / second, precision_flops={"fp8": 4500 * TFLOPs / second, "fp4": 9000 * TFLOPs / second, "int4": 9000 * TOPS}),
        memory=MemoryHierarchy(capacity=192 * GiB, bandwidth=8 * TB / second),
        tdp=1000 * watt,
        unit_cost=40000 * USD,
        dispatch_tax=0.008 * ureg.ms,
        metadata={"source_url": "https://www.nvidia.com/en-us/data-center/blackwell/", "last_verified": "2025-03-06"}
    )

    GB200_NVL72 = HardwareNode(
        name="NVIDIA GB200 NVL72",
        release_year=2024,
        compute=ComputeCore(
            peak_flops=162 * PFLOPs / second,
            precision_flops={
                "fp16": 162 * PFLOPs / second,
                "bf16": 162 * PFLOPs / second,
                "fp8": 324 * PFLOPs / second,
                "fp4": 720 * PFLOPs / second,
            },
        ),
        memory=MemoryHierarchy(capacity=13.8 * TB, bandwidth=576 * TB / second),
        interconnect=IOInterconnect(name="NVLink Switch (Bisection)", bandwidth=130 * TB / second),
        tdp=120 * kilowatt,
        unit_cost=3000000 * USD,
        dispatch_tax=0.005 * ureg.ms,
        metadata={"source_url": "https://www.nvidia.com/en-us/data-center/gb200-nvl72/"}
    )

    MI300X = HardwareNode(
        name="AMD MI300X",
        release_year=2023,
        compute=ComputeCore(peak_flops=1307 * TFLOPs / second, precision_flops={"fp8": 2614 * TFLOPs / second, "int8": 2614 * TOPS, "fp32": 163.4 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=192 * GiB, bandwidth=5.3 * TB / second),
        tdp=750 * watt,
        unit_cost=15000 * USD,
        dispatch_tax=0.012 * ureg.ms
    )

    MI250X = HardwareNode(
        name="AMD MI250X",
        release_year=2021,
        compute=ComputeCore(peak_flops=383 * TFLOPs / second, precision_flops={"fp32": 47.9 * TFLOPs / second, "int8": 383 * TOPS}),
        memory=MemoryHierarchy(capacity=128 * GiB, bandwidth=3.2 * TB / second),
        tdp=500 * watt,
        dispatch_tax=0.015 * ureg.ms
    )

    Gaudi2 = HardwareNode(
        name="Intel Gaudi 2",
        release_year=2022,
        compute=ComputeCore(peak_flops=432 * TFLOPs / second, precision_flops={"fp8": 865 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=96 * GiB, bandwidth=2.45 * TB / second),
        tdp=600 * watt,
        dispatch_tax=0.02 * ureg.ms
    )

    Gaudi3 = HardwareNode(
        name="Intel Gaudi 3",
        release_year=2024,
        compute=ComputeCore(peak_flops=1835 * TFLOPs / second, precision_flops={"fp8": 3670 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=128 * GiB, bandwidth=3.7 * TB / second),
        tdp=900 * watt,
        dispatch_tax=0.01 * ureg.ms
    )

    Trainium2 = HardwareNode(
        name="AWS Trainium 2",
        release_year=2024,
        compute=ComputeCore(peak_flops=380 * TFLOPs / second, precision_flops={"fp8": 760 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=96 * GiB, bandwidth=2.4 * TB / second),
        tdp=500 * watt,
        dispatch_tax=0.02 * ureg.ms
    )

    TPUv6 = HardwareNode(
        name="Google TPU v6 (Trillium)",
        release_year=2024,
        compute=ComputeCore(peak_flops=918 * TFLOPs / second),
        memory=MemoryHierarchy(capacity=32 * GiB, bandwidth=1600 * GB / second),
        tdp=300 * ureg.W,
        dispatch_tax=0.04 * ureg.ms
    )

    TPUv5p = HardwareNode(
        name="Google TPU v5p",
        release_year=2023,
        compute=ComputeCore(peak_flops=459 * TFLOPs / second, precision_flops={"int8": 918 * TOPS}),
        memory=MemoryHierarchy(capacity=95 * GiB, bandwidth=2.76 * TB / second),
        tdp=300 * watt,
        dispatch_tax=0.04 * ureg.ms
    )

    TPUv4 = HardwareNode(
        name="Google TPU v4",
        release_year=2021,
        compute=ComputeCore(peak_flops=275 * TFLOPs / second, precision_flops={"bf16": 275 * TFLOPs / second}),
        memory=MemoryHierarchy(capacity=32 * ureg.GiB, bandwidth=1200 * GB / second),
        tdp=200 * ureg.W,
        dispatch_tax=0.04 * ureg.ms,
    )

    T4 = HardwareNode(
        name="NVIDIA T4",
        release_year=2018,
        compute=ComputeCore(peak_flops=65 * TFLOPs / second, precision_flops={"int8": 130 * TOPS}),
        memory=MemoryHierarchy(capacity=16 * ureg.GiB, bandwidth=320 * GB / second),
        tdp=70 * watt,
        unit_cost=2500 * USD,
        dispatch_tax=0.03 * ureg.ms
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
        metadata={"source_url": "https://www.cerebras.net/product-system/"}
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
        tdp=250 * ureg.W,
        dispatch_tax=0.01 * ureg.ms
    )

    MacBookM3Max = HardwareNode(
        name="MacBook Pro (M3 Max)",
        release_year=2023,
        compute=ComputeCore(peak_flops=14.2 * ureg.TFLOPs/ureg.s),
        memory=MemoryHierarchy(capacity=128 * ureg.GB, bandwidth=400 * ureg.GB/ureg.s),
        tdp=100 * ureg.W,
        dispatch_tax=0.05 * ureg.ms
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
        dispatch_tax=1.0 * ureg.ms
    )

    Pixel8 = HardwareNode(
        name="Google Pixel 8 (Tensor G3)",
        release_year=2023,
        compute=ComputeCore(peak_flops=15 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=8 * ureg.GB, bandwidth=60 * ureg.GB/ureg.s),
        tdp=5 * ureg.W,
        dispatch_tax=1.2 * ureg.ms
    )

    Snapdragon8Gen3 = HardwareNode(
        name="Snapdragon 8 Gen 3",
        release_year=2023,
        compute=ComputeCore(peak_flops=45 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=12 * ureg.GB, bandwidth=77 * ureg.GB/ureg.s),
        tdp=5 * ureg.W,
        dispatch_tax=1.5 * ureg.ms
    )

class EdgeHardware(Registry):
    """Robotics and Industrial Edge (Volume I)."""
    JetsonOrinNX = HardwareNode(
        name="NVIDIA Jetson Orin NX",
        release_year=2023,
        compute=ComputeCore(peak_flops=25 * ureg.TFLOPs/ureg.s, precision_flops={"int8": 100 * ureg.TOPS}),
        memory=MemoryHierarchy(capacity=16 * ureg.GB, bandwidth=102 * ureg.GB/ureg.s),
        tdp=25 * ureg.W,
        dispatch_tax=0.2 * ureg.ms
    )

    Coral = HardwareNode(
        name="Google Coral Edge TPU",
        release_year=2019,
        compute=ComputeCore(peak_flops=4 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=1 * ureg.GB, bandwidth=8 * ureg.GB/ureg.s),
        tdp=2 * ureg.W,
        dispatch_tax=1.0 * ureg.ms
    )

    NUC_Movidius = HardwareNode(
        name="Intel NUC + Movidius",
        release_year=2020,
        compute=ComputeCore(peak_flops=1 * ureg.TOPS),
        memory=MemoryHierarchy(capacity=16 * ureg.GB, bandwidth=25 * ureg.GB/ureg.s),
        tdp=15 * ureg.W,
        dispatch_tax=2.0 * ureg.ms
    )

    GenericServer = HardwareNode(
        name="Edge Server",
        release_year=2024,
        compute=ComputeCore(peak_flops=1 * ureg.TFLOPs/ureg.s),
        memory=MemoryHierarchy(capacity=128 * ureg.GB, bandwidth=100 * ureg.GB/ureg.s),
        tdp=300 * ureg.W,
        dispatch_tax=0.1 * ureg.ms
    )

    # Backward-compatible alias
    Generic_Phone = MobileHardware.iPhone15Pro

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
            capacity=8 * ureg.MB,                     # Flash (primary weight storage)
            bandwidth=0.08 * ureg.GB/ureg.s,          # Flash read ~80 MB/s (XIP)
            sram_capacity=512 * ureg.KiB,             # On-chip SRAM
            sram_bandwidth=0.96 * ureg.GB/ureg.s,     # SRAM bandwidth @ 240 MHz
            flash_capacity=8 * ureg.MB,               # Explicit flash (same as capacity)
            flash_bandwidth=0.08 * ureg.GB/ureg.s,    # Flash read ~80 MB/s
        ),
        tdp=0.4 * ureg.W,              # Inference-only power (not WiFi-on 1.2W)
        embodied_carbon_kg=5.0,        # Including packaging and PCB assembly
        dispatch_tax=1.0 * ureg.ms     # TFLite Micro interpreter overhead
    )
    ESP32 = ESP32_S3 # Alias for backward compatibility

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
        dispatch_tax=0.5 * ureg.ms
    )

    HimaxWE1 = HardwareNode(
        name="Himax WE-I Plus",
        release_year=2020,
        compute=ComputeCore(peak_flops=0.0002 * ureg.TFLOPs/ureg.s),
        memory=MemoryHierarchy(capacity=2 * ureg.MB, bandwidth=0.1 * ureg.GB/ureg.s),
        tdp=0.005 * ureg.W,
        dispatch_tax=2.0 * ureg.ms
    )

class Hardware(Registry):
    Cloud = CloudHardware
    Workstation = WorkstationHardware
    Mobile = MobileHardware
    Edge = EdgeHardware
    Tiny = TinyHardware

    # Common Aliases (Vetted only)
    V100 = CloudHardware.V100
    A100 = CloudHardware.A100
    H100 = CloudHardware.H100
    H200 = CloudHardware.H200
    B200 = CloudHardware.B200
    NVL72 = CloudHardware.GB200_NVL72
    MI300X = CloudHardware.MI300X
    MI250X = CloudHardware.MI250X
    Gaudi2 = CloudHardware.Gaudi2
    Gaudi3 = CloudHardware.Gaudi3
    Trainium2 = CloudHardware.Trainium2
    TPUv6 = CloudHardware.TPUv6
    TPUv5p = CloudHardware.TPUv5p
    TPUv4 = CloudHardware.TPUv4
    T4 = CloudHardware.T4
    CerebrasCS3 = CloudHardware.Cerebras_CS3

    DGXSpark = WorkstationHardware.DGX_Spark
    MacBook = WorkstationHardware.MacBookM3Max

    iPhone = MobileHardware.iPhone15Pro
    Snapdragon = MobileHardware.Snapdragon8Gen3
    Jetson = EdgeHardware.JetsonOrinNX
    ESP32 = TinyHardware.ESP32_S3
    Himax = TinyHardware.HimaxWE1

from ..systems.registry import Fabrics
Hardware.Networks = Fabrics
