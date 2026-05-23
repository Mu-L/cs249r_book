from .types import TransformerWorkload, CNNWorkload, Workload, SSMWorkload, DiffusionWorkload
from ..core.registry import Registry
from ..core.constants import (flop, param, ureg)

class LanguageModels(Registry):
    GPT2 = TransformerWorkload(
        name="GPT-2 (1.5B)",
        architecture="Transformer",
        parameters=1.5e9 * param,
        layers=48,
        hidden_dim=1600,
        heads=25,
        inference_flops=2 * 1.5e9 * ureg.flop
    )
    GPT3 = TransformerWorkload(
        name="GPT-3 (175B)",
        architecture="Transformer",
        parameters=175e9 * param,
        layers=96,
        hidden_dim=12288,
        heads=96,
        training_ops=3.14e23 * flop,
        inference_flops=2 * 175e9 * ureg.flop
    )
    GPT4 = TransformerWorkload(
        name="GPT-4",
        architecture="Transformer",
        parameters=1.76e12 * param,
        layers=120,
        hidden_dim=16384,
        heads=128,
        inference_flops=2 * 1.76e12 * ureg.flop
    )
    BERT_Base = TransformerWorkload(
        name="BERT-Base",
        architecture="Transformer",
        parameters=110e6 * param,
        layers=12,
        hidden_dim=768,
        heads=12,
        inference_flops=22e9 * ureg.flop
    )
    BERT_Large = TransformerWorkload(
        name="BERT-Large",
        architecture="Transformer",
        parameters=340e6 * param,
        layers=24,
        hidden_dim=1024,
        heads=16,
        inference_flops=68e9 * ureg.flop
    )
    Llama2_7B = TransformerWorkload(
        name="Llama-2-7B",
        architecture="Transformer",
        parameters=7e9 * param,
        layers=32,
        hidden_dim=4096,
        heads=32,
        inference_flops=2 * 7e9 * ureg.flop
    )
    Llama2_70B = TransformerWorkload(
        name="Llama-2-70B",
        architecture="Transformer",
        parameters=70e9 * param,
        layers=80,
        hidden_dim=8192,
        heads=64,
        kv_heads=8,
        inference_flops=2 * 70e9 * ureg.flop
    )
    Llama3_8B = TransformerWorkload(
        name="Llama-3.1-8B",
        architecture="Transformer",
        parameters=8.03e9 * param,
        layers=32,
        hidden_dim=4096,
        heads=32,
        kv_heads=8,
        inference_flops=2 * 8.03e9 * ureg.flop
    )
    Llama3_70B = TransformerWorkload(
        name="Llama-3.1-70B",
        architecture="Transformer",
        parameters=70.6e9 * param,
        layers=80,
        hidden_dim=8192,
        heads=64,
        kv_heads=8,
        inference_flops=2 * 70.6e9 * ureg.flop
    )

class VisionModels(Registry):
    ResNet50 = CNNWorkload(
        name="ResNet-50",
        architecture="CNN",
        parameters=25.6e6 * param,
        inference_flops=4.1e9 * ureg.flop,
        layers=50
    )
    MobileNetV2 = CNNWorkload(
        name="MobileNetV2",
        architecture="CNN",
        parameters=3.5e6 * param,
        inference_flops=0.3e9 * ureg.flop,
        layers=54
    )
    YOLOv8_Nano = CNNWorkload(
        name="YOLOv8-Nano",
        architecture="CNN",
        parameters=3.2e6 * param,
        inference_flops=8.7e9 * ureg.flop,
        layers=225
    )
    AlexNet = CNNWorkload(
        name="AlexNet",
        architecture="CNN",
        parameters=60e6 * param,
        inference_flops=1.5e9 * ureg.flop,
        layers=8
    )

class TinyModels(Registry):
    DS_CNN = CNNWorkload(
        name="DS-CNN (KWS)",
        architecture="CNN",
        parameters=200e3 * param,
        inference_flops=20e6 * ureg.flop
    )
    WakeVision = CNNWorkload(
        name="Wake Vision (Doorbell)",
        architecture="CNN",
        parameters=0.25e6 * param,
        inference_flops=25e6 * ureg.flop
    )
    AnomalyDetector = Workload(
        name="Anomaly Detector",
        architecture="MLP",
        parameters=270e3 * param,
        inference_flops=2 * 270e3 * ureg.flop
    )

class RecommendationModels(Registry):
    DLRM = Workload(
        name="DLRM",
        architecture="DLRM",
        model_size=100 * ureg.GB
    )

class StateSpaceModels(Registry):
    Mamba_130M = SSMWorkload(
        name="Mamba-130M",
        architecture="SSM",
        parameters=130e6 * param,
        layers=24,
        hidden_dim=768,
        state_size=16,
        inference_flops=2 * 130e6 * ureg.flop
    )
    Mamba_2_8B = SSMWorkload(
        name="Mamba-2.8B",
        architecture="SSM",
        parameters=2.8e9 * param,
        layers=64,
        hidden_dim=2560,
        state_size=16,
        inference_flops=2 * 2.8e9 * ureg.flop
    )

class GenerativeVisionModels(Registry):
    StableDiffusion_v1_5 = DiffusionWorkload(
        name="Stable Diffusion v1.5",
        architecture="Diffusion/U-Net",
        parameters=860e6 * param,
        resolution=512,
        denoising_steps=50,
        inference_flops=800e9 * ureg.flop
    )

class Models(Registry):
    Language = LanguageModels
    Vision = VisionModels
    Tiny = TinyModels
    Recommendation = RecommendationModels
    StateSpace = StateSpaceModels
    GenerativeVision = GenerativeVisionModels
