import pytest
from pydantic import ValidationError
from mlsysim.hardware import Hardware, HardwareNode
from mlsysim.core.constants import Q_, ureg

def test_hardware_registry():
    a100 = Hardware.Cloud.A100
    assert a100.name == "NVIDIA A100"
    assert a100.release_year == 2020
    assert a100.compute.peak_flops.magnitude == 312.0  # Dense FP16 Tensor Core

    # Check ridge point calculation
    ridge = a100.ridge_point()
    assert "flop/B" in str(ridge.units) or "flop / byte" in str(ridge.units)
    assert 100 < ridge.magnitude < 200  # ~153 flop/byte (312 TFLOPS / 2.039 TB/s)

def test_hardware_validation():
    # Should raise error on invalid quantity string
    with pytest.raises(ValidationError):
        HardwareNode(
            name="Broken",
            release_year=2025,
            compute={"peak_flops": "not a number"},
            memory={"capacity": "10 GiB", "bandwidth": "100 GB/s"}
        )

def test_json_serialization():
    a100 = Hardware.Cloud.A100
    json_data = a100.model_dump_json()
    assert "NVIDIA A100" in json_data
    assert "312" in json_data  # FP16 Tensor Core peak


def test_tpuv4_is_not_alias_to_tpuv5p():
    assert Hardware.Cloud.TPUv4.name == "Google TPU v4"
    assert Hardware.Cloud.TPUv4 is not Hardware.Cloud.TPUv5p
    assert Hardware.Cloud.TPUv4.compute.peak_flops == (275 * ureg.TFLOPs / ureg.second)


def test_nvlink_on_cloud_gpus():
    """NVLink bandwidth lives on HardwareNode, not loose constants."""
    from mlsysim.core.constants import (
        NVLINK_V100_BW, NVLINK_A100_BW, NVLINK_H100_BW, NVLINK_B200_BW, GB, second,
    )

    assert Hardware.Cloud.V100.nvlink.name == "NVLink 2.0"
    assert Hardware.Cloud.V100.nvlink.bandwidth == NVLINK_V100_BW
    assert Hardware.Cloud.A100.nvlink.bandwidth == NVLINK_A100_BW
    assert Hardware.Cloud.H100.nvlink.bandwidth == NVLINK_H100_BW
    assert Hardware.Cloud.B200.nvlink.bandwidth == NVLINK_B200_BW
    assert Hardware.Cloud.B200.nvlink.bandwidth.m_as(GB / second) == 1800.0
