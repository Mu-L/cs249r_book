import re
import os
import glob

mapping = {
    'GPT2_PARAMS': 'Models.Language.GPT2.parameters',
    'GPT2_LAYERS': 'Models.Language.GPT2.layers',
    'GPT2_HIDDEN_DIM': 'Models.Language.GPT2.hidden_dim',
    'GPT2_HEADS': 'Models.Language.GPT2.heads',
    
    'GPT3_PARAMS': 'Models.Language.GPT3.parameters',
    'GPT3_LAYERS': 'Models.Language.GPT3.layers',
    'GPT3_HIDDEN_DIM': 'Models.Language.GPT3.hidden_dim',
    'GPT3_HEADS': 'Models.Language.GPT3.heads',
    'GPT3_TRAINING_OPS': 'Models.Language.GPT3.training_ops',

    'GPT4_EST_PARAMS': 'Models.Language.GPT4.parameters',
    'GPT4_LAYERS': 'Models.Language.GPT4.layers',
    'GPT4_HIDDEN_DIM': 'Models.Language.GPT4.hidden_dim',
    'GPT4_HEADS': 'Models.Language.GPT4.heads',

    'BERT_BASE_PARAMS': 'Models.Language.BERT_Base.parameters',
    'BERT_BASE_LAYERS': 'Models.Language.BERT_Base.layers',
    'BERT_BASE_HIDDEN_DIM': 'Models.Language.BERT_Base.hidden_dim',
    'BERT_BASE_HEADS': 'Models.Language.BERT_Base.heads',
    'BERT_BASE_FLOPs': 'Models.Language.BERT_Base.inference_flops',

    'BERT_LARGE_PARAMS': 'Models.Language.BERT_Large.parameters',
    'BERT_LARGE_LAYERS': 'Models.Language.BERT_Large.layers',
    'BERT_LARGE_HIDDEN_DIM': 'Models.Language.BERT_Large.hidden_dim',
    'BERT_LARGE_HEADS': 'Models.Language.BERT_Large.heads',
    'BERT_LARGE_FLOPs': 'Models.Language.BERT_Large.inference_flops',

    'LLAMA2_70B_PARAMS': 'Models.Language.Llama2_70B.parameters',
    'LLAMA2_70B_LAYERS': 'Models.Language.Llama2_70B.layers',
    'LLAMA2_70B_HIDDEN_DIM': 'Models.Language.Llama2_70B.hidden_dim',
    'LLAMA2_70B_HEADS': 'Models.Language.Llama2_70B.heads',

    'LLAMA3_8B_PARAMS': 'Models.Language.Llama3_8B.parameters',
    'LLAMA3_8B_LAYERS': 'Models.Language.Llama3_8B.layers',
    'LLAMA3_8B_HIDDEN_DIM': 'Models.Language.Llama3_8B.hidden_dim',
    'LLAMA3_8B_HEADS': 'Models.Language.Llama3_8B.heads',
    'LLAMA3_8B_KV_HEADS': 'Models.Language.Llama3_8B.kv_heads',

    'LLAMA3_70B_PARAMS': 'Models.Language.Llama3_70B.parameters',
    'LLAMA3_70B_LAYERS': 'Models.Language.Llama3_70B.layers',
    'LLAMA3_70B_HIDDEN_DIM': 'Models.Language.Llama3_70B.hidden_dim',
    'LLAMA3_70B_HEADS': 'Models.Language.Llama3_70B.heads',
    'LLAMA3_70B_KV_HEADS': 'Models.Language.Llama3_70B.kv_heads',

    'RESNET50_PARAMS': 'Models.Vision.ResNet50.parameters',
    'RESNET50_FLOPs': 'Models.Vision.ResNet50.inference_flops',

    'MOBILENETV2_PARAMS': 'Models.Vision.MobileNetV2.parameters',
    'MOBILENETV2_FLOPs': 'Models.Vision.MobileNetV2.inference_flops',

    'ALEXNET_PARAMS': 'Models.Vision.AlexNet.parameters',
    'ALEXNET_FLOPs': 'Models.Vision.AlexNet.inference_flops',

    'YOLOV8_NANO_PARAMS': 'Models.Vision.YOLOv8_Nano.parameters',
    'YOLOV8_NANO_FLOPs': 'Models.Vision.YOLOv8_Nano.inference_flops',
    'YOLOV8_NANO_LAYERS': 'Models.Vision.YOLOv8_Nano.layers',

    'KWS_DSCNN_PARAMS': 'Models.Tiny.DS_CNN.parameters',
    'KWS_DSCNN_FLOPs': 'Models.Tiny.DS_CNN.inference_flops',

    'WAKEVISION_PARAMS': 'Models.Tiny.WakeVision.parameters',
    'WAKEVISION_FLOPs': 'Models.Tiny.WakeVision.inference_flops',

    'ANOMALY_MODEL_PARAMS': 'Models.Tiny.AnomalyDetector.parameters',

    'DLRM_MODEL_SIZE_FP32': 'Models.Recommendation.DLRM.model_size',

    'MAMBA_130M_PARAMS': 'Models.StateSpace.Mamba_130M.parameters',
    'MAMBA_130M_LAYERS': 'Models.StateSpace.Mamba_130M.layers',
    'MAMBA_130M_HIDDEN_DIM': 'Models.StateSpace.Mamba_130M.hidden_dim',
    'MAMBA_130M_STATE_SIZE': 'Models.StateSpace.Mamba_130M.state_size',

    'MAMBA_2_8B_PARAMS': 'Models.StateSpace.Mamba_2_8B.parameters',
    'MAMBA_2_8B_LAYERS': 'Models.StateSpace.Mamba_2_8B.layers',
    'MAMBA_2_8B_HIDDEN_DIM': 'Models.StateSpace.Mamba_2_8B.hidden_dim',
    'MAMBA_2_8B_STATE_SIZE': 'Models.StateSpace.Mamba_2_8B.state_size',

    'STABLE_DIFFUSION_V1_5_PARAMS': 'Models.GenerativeVision.StableDiffusion_v1_5.parameters',
    'STABLE_DIFFUSION_V1_5_RESOLUTION': 'Models.GenerativeVision.StableDiffusion_v1_5.resolution',
    'STABLE_DIFFUSION_V1_5_STEPS': 'Models.GenerativeVision.StableDiffusion_v1_5.denoising_steps',
    'STABLE_DIFFUSION_V1_5_FLOPs_PER_STEP': 'Models.GenerativeVision.StableDiffusion_v1_5.inference_flops',

    # Hardware constants mapping
    'V100_FLOPS_FP16_TENSOR': 'Hardware.Cloud.V100.compute.peak_flops',
    'V100_FLOPS_FP32': 'Hardware.Cloud.V100.compute.precision_flops["fp32"]',
    'V100_MEM_BW': 'Hardware.Cloud.V100.memory.bandwidth',
    'V100_MEM_CAPACITY': 'Hardware.Cloud.V100.memory.capacity',
    'V100_TDP': 'Hardware.Cloud.V100.tdp',
    'V100_UNIT_COST': 'Hardware.Cloud.V100.unit_cost',

    'A100_FLOPS_FP16_TENSOR': 'Hardware.Cloud.A100.compute.peak_flops',
    'A100_FLOPS_TF32': 'Hardware.Cloud.A100.compute.precision_flops["tf32"]',
    'A100_FLOPS_FP32': 'Hardware.Cloud.A100.compute.precision_flops["fp32"]',
    'A100_TOPS_INT8': 'Hardware.Cloud.A100.compute.precision_flops["int8"]',
    'A100_MEM_BW': 'Hardware.Cloud.A100.memory.bandwidth',
    'A100_MEM_CAPACITY': 'Hardware.Cloud.A100.memory.capacity',
    'A100_TDP': 'Hardware.Cloud.A100.tdp',
    'A100_UNIT_COST': 'Hardware.Cloud.A100.unit_cost',

    'H100_FLOPS_FP16_TENSOR': 'Hardware.Cloud.H100.compute.peak_flops',
    'H100_FLOPS_FP8_TENSOR': 'Hardware.Cloud.H100.compute.precision_flops["fp8"]',
    'H100_FLOPS_TF32': 'Hardware.Cloud.H100.compute.precision_flops["tf32"]',
    'H100_TOPS_INT8': 'Hardware.Cloud.H100.compute.precision_flops["int8"]',
    'H100_MEM_BW': 'Hardware.Cloud.H100.memory.bandwidth',
    'H100_MEM_CAPACITY': 'Hardware.Cloud.H100.memory.capacity',
    'H100_TDP': 'Hardware.Cloud.H100.tdp',
    'H100_UNIT_COST': 'Hardware.Cloud.H100.unit_cost',

    'H200_MEM_BW': 'Hardware.Cloud.H200.memory.bandwidth',
    'H200_MEM_CAPACITY': 'Hardware.Cloud.H200.memory.capacity',
    'H200_TDP': 'Hardware.Cloud.H200.tdp',
    'H200_UNIT_COST': 'Hardware.Cloud.H200.unit_cost',

    'B200_FLOPS_FP16_TENSOR': 'Hardware.Cloud.B200.compute.peak_flops',
    'B200_FLOPS_FP8_TENSOR': 'Hardware.Cloud.B200.compute.precision_flops["fp8"]',
    'B200_FLOPS_FP4_TENSOR': 'Hardware.Cloud.B200.compute.precision_flops["fp4"]',
    'B200_TOPS_INT4': 'Hardware.Cloud.B200.compute.precision_flops["int4"]',
    'B200_MEM_BW': 'Hardware.Cloud.B200.memory.bandwidth',
    'B200_MEM_CAPACITY': 'Hardware.Cloud.B200.memory.capacity',
    'B200_TDP': 'Hardware.Cloud.B200.tdp',
    'B200_UNIT_COST': 'Hardware.Cloud.B200.unit_cost',

    'NVL72_GPUs': '72',
    'NVL72_FLOPS_FP16_TENSOR': 'Hardware.Cloud.GB200_NVL72.compute.peak_flops',
    'NVL72_FLOPS_FP8_TENSOR': 'Hardware.Cloud.GB200_NVL72.compute.precision_flops["fp8"]',
    'NVL72_FLOPS_FP4_TENSOR': 'Hardware.Cloud.GB200_NVL72.compute.precision_flops["fp4"]',
    'NVL72_MEM_CAPACITY': 'Hardware.Cloud.GB200_NVL72.memory.capacity',
    'NVL72_MEM_BW': 'Hardware.Cloud.GB200_NVL72.memory.bandwidth',
    'NVL72_NVLINK_BW': 'Hardware.Cloud.GB200_NVL72.interconnect.bandwidth',
    'NVL72_TDP': 'Hardware.Cloud.GB200_NVL72.tdp',
    'NVL72_UNIT_COST': 'Hardware.Cloud.GB200_NVL72.unit_cost',

    'MI300X_FLOPS_FP16_TENSOR': 'Hardware.Cloud.MI300X.compute.peak_flops',
    'MI300X_FLOPS_FP8': 'Hardware.Cloud.MI300X.compute.precision_flops["fp8"]',
    'MI300X_TOPS_INT8': 'Hardware.Cloud.MI300X.compute.precision_flops["int8"]',
    'MI300X_FLOPS_FP32': 'Hardware.Cloud.MI300X.compute.precision_flops["fp32"]',
    'MI300X_MEM_BW': 'Hardware.Cloud.MI300X.memory.bandwidth',
    'MI300X_MEM_CAPACITY': 'Hardware.Cloud.MI300X.memory.capacity',
    'MI300X_TDP': 'Hardware.Cloud.MI300X.tdp',
    'MI300X_UNIT_COST': 'Hardware.Cloud.MI300X.unit_cost',

    'MI250X_FLOPS_FP16_TENSOR': 'Hardware.Cloud.MI250X.compute.peak_flops',
    'MI250X_FLOPS_FP32': 'Hardware.Cloud.MI250X.compute.precision_flops["fp32"]',
    'MI250X_TOPS_INT8': 'Hardware.Cloud.MI250X.compute.precision_flops["int8"]',
    'MI250X_MEM_BW': 'Hardware.Cloud.MI250X.memory.bandwidth',
    'MI250X_MEM_CAPACITY': 'Hardware.Cloud.MI250X.memory.capacity',
    'MI250X_TDP': 'Hardware.Cloud.MI250X.tdp',

    'GAUDI2_FLOPS_BF16': 'Hardware.Cloud.Gaudi2.compute.peak_flops',
    'GAUDI2_FLOPS_FP8': 'Hardware.Cloud.Gaudi2.compute.precision_flops["fp8"]',
    'GAUDI2_MEM_BW': 'Hardware.Cloud.Gaudi2.memory.bandwidth',
    'GAUDI2_MEM_CAPACITY': 'Hardware.Cloud.Gaudi2.memory.capacity',
    'GAUDI2_TDP': 'Hardware.Cloud.Gaudi2.tdp',

    'GAUDI3_FLOPS_BF16': 'Hardware.Cloud.Gaudi3.compute.peak_flops',
    'GAUDI3_FLOPS_FP8': 'Hardware.Cloud.Gaudi3.compute.precision_flops["fp8"]',
    'GAUDI3_MEM_BW': 'Hardware.Cloud.Gaudi3.memory.bandwidth',
    'GAUDI3_MEM_CAPACITY': 'Hardware.Cloud.Gaudi3.memory.capacity',
    'GAUDI3_TDP': 'Hardware.Cloud.Gaudi3.tdp',

    'TRAINIUM2_FLOPS_BF16': 'Hardware.Cloud.Trainium2.compute.peak_flops',
    'TRAINIUM2_FLOPS_FP8': 'Hardware.Cloud.Trainium2.compute.precision_flops["fp8"]',
    'TRAINIUM2_MEM_BW': 'Hardware.Cloud.Trainium2.memory.bandwidth',
    'TRAINIUM2_MEM_CAPACITY': 'Hardware.Cloud.Trainium2.memory.capacity',
    'TRAINIUM2_TDP': 'Hardware.Cloud.Trainium2.tdp',

    'TPUV4_FLOPS_BF16': 'Hardware.Cloud.TPUv4.compute.peak_flops',
    'TPUV4_MEM_BW': 'Hardware.Cloud.TPUv4.memory.bandwidth',

    'TPUV5P_FLOPS_BF16': 'Hardware.Cloud.TPUv5p.compute.peak_flops',
    'TPUV5P_TOPS_INT8': 'Hardware.Cloud.TPUv5p.compute.precision_flops["int8"]',
    'TPUV5P_MEM_BW': 'Hardware.Cloud.TPUv5p.memory.bandwidth',
    'TPUV5P_MEM_CAPACITY': 'Hardware.Cloud.TPUv5p.memory.capacity',
    'TPUV5P_TDP': 'Hardware.Cloud.TPUv5p.tdp',

    'TPUV6_FLOPS_BF16': 'Hardware.Cloud.TPUv6.compute.peak_flops',
    'TPUV6_MEM_BW': 'Hardware.Cloud.TPUv6.memory.bandwidth',
    'TPUV6_MEM_CAPACITY': 'Hardware.Cloud.TPUv6.memory.capacity',

    'T4_FLOPS_FP16_TENSOR': 'Hardware.Cloud.T4.compute.peak_flops',
    'T4_TOPS_INT8': 'Hardware.Cloud.T4.compute.precision_flops["int8"]',
    'T4_MEM_BW': 'Hardware.Cloud.T4.memory.bandwidth',
    'T4_TDP': 'Hardware.Cloud.T4.tdp',
    'T4_UNIT_COST': 'Hardware.Cloud.T4.unit_cost',

    'WSE3_FLOPS_FP16': 'Hardware.Cloud.Cerebras_CS3.compute.peak_flops',
    'WSE3_MEM_CAPACITY': 'Hardware.Cloud.Cerebras_CS3.memory.capacity',
    'WSE3_MEM_BW': 'Hardware.Cloud.Cerebras_CS3.memory.bandwidth',
    'WSE3_TDP': 'Hardware.Cloud.Cerebras_CS3.tdp',
    'CEREBRAS_CS3_UNIT_COST': 'Hardware.Cloud.Cerebras_CS3.unit_cost',

    'MOBILE_NPU_TOPS_INT8': 'Hardware.Mobile.iPhone.compute.peak_flops',
    'MOBILE_NPU_MEM_BW': 'Hardware.Mobile.iPhone.memory.bandwidth',
}

files = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    for k, v in mapping.items():
        content = re.sub(r'\b' + k + r'\b', v, content)
        
    if content != original_content:
        # Rewrite `from mlsysim.core.constants import ...` to `from mlsysim import *`
        content = re.sub(r'from mlsysim\.core\.constants import \([^)]+\)', 'from mlsysim import *', content, flags=re.DOTALL)
        content = re.sub(r'from mlsysim\.core\.constants import .*\n', 'from mlsysim import *\n', content)
        
        # Deduplicate `from mlsysim import *`
        content = re.sub(r'(from mlsysim import \*\n)+', 'from mlsysim import *\n', content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

for f in files:
    process_file(f)
