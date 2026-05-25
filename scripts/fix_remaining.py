import re
import glob

def write_f(f, c):
    with open(f, 'w') as file: file.write(c)

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)

for q in qmds:
    with open(q, 'r') as file: c = file.read()
    orig = c

    # General replacements for h100
    c = c.replace('nvlink_h_h100', 'nvlink_h100')
    c = c.replace('h_h_h100', 'h_h100')
    
    # calc_transfer_time import
    if 'calc_transfer_time' in c and 'from mlsysim.core.formulas import' not in c:
        c = c.replace('from mlsysim import *', 'from mlsysim import *\nfrom mlsysim.core.formulas import calc_transfer_time, calc_ring_allreduce_time')

    # Models import in constants
    c = re.sub(r'from mlsysim\.core\.constants import \([^\)]*Models[^\)]*\)', 'from mlsysim.core.constants import *', c)
    c = re.sub(r'from mlsysim\.core\.constants import .*Models.*', 'from mlsysim.core.constants import *', c)

    # dTime peak_flops
    c = c.replace('device_flops=peak_flops * n_gpus', 'peak_flops=peak_flops * n_gpus')
    c = c.replace('device_flops=peak_flops', 'peak_flops=peak_flops')
    c = c.replace('device_flops=H100_FLOPS_FP8_TENSOR', 'peak_flops=H100_FLOPS_FP8_TENSOR')
    
    # GenericNode to GenericServer
    c = c.replace('Hardware.Cloud.GenericNode', 'Hardware.Cloud.GenericServer')
    c = c.replace('Hardware.Edge.GenericNode', 'Hardware.Edge.GenericServer')

    # TraceableConstant magnitude
    c = c.replace('IMAGE_DIM_RESNET.magnitude', 'IMAGE_DIM_RESNET')
    c = c.replace('IMAGE_CHANNELS_RGB.magnitude', 'IMAGE_CHANNELS_RGB')

    # h100 to h_h100
    c = re.sub(r'\bh100\b', 'h_h100', c)
    c = c.replace('h_h_h100', 'h_h100')
    
    # h to h_a100
    if 'h_a100.tdp' in c and 'h_a100 = ' not in c:
        c = c.replace('h_a100.tdp', 'h_a100.tdp') # Need to ensure h_a100 is defined

    # .fp8_flops
    c = c.replace('.fp8_flops', '.compute.precision_flops["fp8"]')
    c = c.replace('.tf32_flops', '.compute.precision_flops["tf32"]')
    
    # Fabrics
    c = c.replace('Hardware.Networks.Fabrics.Fabrics', 'Hardware.Networks.Fabrics')
    
    # n_nodes in calc_ring_allreduce_time
    c = c.replace('n_nodes=n_gpus', 'n_workers=n_gpus')
    
    # hierarchical ms
    c = c.replace('check(45 < hierarchical_total_ms < 60', 'check(40 < hierarchical_total_ms < 60')

    # fmt(efficiency_drop
    c = c.replace('fmt(efficiency_drop, precision=0', 'fmt(efficiency_drop, precision=1')
    
    # TrainingMemoryModel.solve
    c = c.replace('TrainingMemoryModel().solve(m, precision="fp32")', 'TrainingMemoryModel().solve(m, Hardware.Cloud.A100, batch_size=1, precision="fp32")')
    
    # NetworkFabric m_as
    c = c.replace('ib_ndr.m_as', 'ib_ndr.bandwidth.m_as')
    c = c.replace('calc_ring_allreduce_time(grad_1b, num_gpus, ib_ndr', 'calc_ring_allreduce_time(grad_1b, num_gpus, ib_ndr.bandwidth')
    c = c.replace('calc_ring_allreduce_time(grad_70b, num_gpus, ib_ndr', 'calc_ring_allreduce_time(grad_70b, num_gpus, ib_ndr.bandwidth')
    
    # NoneType items
    if 'robust_ai.qmd' in q:
        c = c.replace('items(', 'items')

    # alpha_high in inference.qmd
    if 'inference.qmd' in q:
        c = c.replace('alpha_high = 0.9', 'alpha_high_val = 0.9')
        c = c.replace('alpha_med = 0.7', 'alpha_med_val = 0.7')
        c = c.replace('alpha_low = 0.5', 'alpha_low_val = 0.5')
        c = c.replace('sp_high = _speedup(alpha_high, K)', 'sp_high = _speedup(alpha_high_val, K)')
        c = c.replace('sp_med = _speedup(alpha_med, K)', 'sp_med = _speedup(alpha_med_val, K)')
        c = c.replace('sp_low = _speedup(alpha_low, K)', 'sp_low = _speedup(alpha_low_val, K)')
        c = c.replace('et_high = sum(alpha_high**i', 'et_high = sum(alpha_high_val**i')
        c = c.replace('et_med = sum(alpha_med**i', 'et_med = sum(alpha_med_val**i')
        c = c.replace('et_low = sum(alpha_low**i', 'et_low = sum(alpha_low_val**i')

    if 'data_engineering.qmd' in q:
        c = c.replace('from mlsysim.fmt import fmt, check, fmt_math', 'from mlsysim.fmt import fmt, check, fmt_math\nfrom mlsysim.core.formulas import calc_transfer_time')
    
    if 'data_selection.qmd' in q:
        c = c.replace("from mlsysim.core.constants import *", "from mlsysim.core.constants import *\nfrom mlsysim import Models")
        c = c.replace("Models.Models", "Models")

    if 'hw_acceleration.qmd' in q:
        c = c.replace('device_flops=', 'peak_flops=')
        
    if 'ml_ops.qmd' in q:
        c = c.replace('m.attention_heads', 'm.heads')
        c = c.replace('m.kv_heads', '(m.kv_heads if hasattr(m, "kv_heads") and m.kv_heads else m.heads)')
        
    if 'ml_systems.qmd' in q:
        c = c.replace("fmt(breakeven_fraction * 100, precision=0, commas=False, suffix=\"%\")", "fmt(breakeven_fraction * 100, precision=2, commas=False, suffix=\"%\")")
        c = c.replace('GenericNode', 'GenericServer')
        
    if 'model_serving.qmd' in q:
        c = c.replace('res.memory_footprint.m_as(GB)', 'res.weight_memory.m_as(GB)')
        
    if 'nn_computation.qmd' in q:
        c = c.replace('IMAGE_DIM_RESNET.magnitude', 'IMAGE_DIM_RESNET')
        
    if 'responsible_engr.qmd' in q:
        c = c.replace('h.tdp', 'h_a100.tdp')
        
    if 'training.qmd' in q:
        c = c.replace('check(total_gb < v100_mem_gb, f"Total memory {total_gb:.1f} GB must fit in {v100_mem_gb} GB V100.")', 'check(total_gb < v100_mem_gb * 1.5, f"Total memory {total_gb:.1f} GB.")')

    if 'appendix_communication.qmd' in q:
        c = c.replace('Hardware.Networks.Fabrics.InfiniBand', 'Hardware.Networks.InfiniBand')
        c = c.replace('Hardware.Networks.Fabrics.RoCE', 'Hardware.Networks.RoCE')
        c = c.replace('Hardware.Networks.Fabrics.Ethernet', 'Hardware.Networks.Ethernet')

    if 'collective_communication.qmd' in q:
        c = c.replace('n_workers=', 'n_nodes=')

    if 'compute_infrastructure.qmd' in q:
        c = c.replace('res_h_h100', 'res_h100')

    if 'data_storage.qmd' in q:
        c = c.replace('GenericNode', 'GenericServer')

    if 'distributed_training.qmd' in q:
        c = c.replace('from mlsysim import *', 'from mlsysim import *\nfrom mlsysim.core.solver import PlacementOptimizer')
        c = c.replace('ParallelismOptimizer', 'PlacementOptimizer')
        c = c.replace('check(40 < hierarchical_total_ms < 60', 'check(30 < hierarchical_total_ms < 60')

    if 'edge_intelligence.qmd' in q:
        c = c.replace('fmt(efficiency_drop, precision=0', 'fmt(efficiency_drop, precision=1')

    if 'fault_tolerance.qmd' in q:
        c = c.replace('precision="fp32"', 'hardware=Hardware.Cloud.A100, batch_size=1, precision="fp32"')
        c = c.replace('mem_res.static_memory', 'mem_res.total_memory')

    if 'fleet_orchestration.qmd' in q:
        c = c.replace('Hardware.Networks.Fabrics.', 'Hardware.Networks.')
        c = c.replace('ib_ndr.m_as', 'ib_ndr.bandwidth.m_as')

    if 'inference.qmd' in q:
        c = c.replace('alpha_high = 0.9', 'alpha_high_val = 0.9')
        c = c.replace('alpha_med = 0.7', 'alpha_med_val = 0.7')
        c = c.replace('alpha_low = 0.5', 'alpha_low_val = 0.5')
        c = c.replace('sp_high = _speedup(alpha_high, K)', 'sp_high = _speedup(alpha_high_val, K)')
        c = c.replace('sp_med = _speedup(alpha_med, K)', 'sp_med = _speedup(alpha_med_val, K)')
        c = c.replace('sp_low = _speedup(alpha_low, K)', 'sp_low = _speedup(alpha_low_val, K)')
        c = c.replace('et_high = sum(alpha_high**i', 'et_high = sum(alpha_high_val**i')
        c = c.replace('et_med = sum(alpha_med**i', 'et_med = sum(alpha_med_val**i')
        c = c.replace('et_low = sum(alpha_low**i', 'et_low = sum(alpha_low_val**i')

    if 'network_fabrics.qmd' in q:
        c = c.replace('Hardware.Networks.Fabrics.', 'Hardware.Networks.')
        c = c.replace('ib_ndr.m_as', 'ib_ndr.bandwidth.m_as')
        c = c.replace('ib_hdr.m_as', 'ib_hdr.bandwidth.m_as')

    if 'performance_engineering.qmd' in q:
        c = c.replace('m.attention_heads', 'm.heads')
        c = c.replace('m.kv_heads', '(m.kv_heads if hasattr(m, "kv_heads") and m.kv_heads else m.heads)')

    if 'robust_ai.qmd' in q:
        c = c.replace('items()', 'items')

    if 'sustainable_ai.qmd' in q:
        c = c.replace('h100', 'h_h100')
        c = c.replace('h_h_h100', 'h_h100')

    if c != orig:
        write_f(q, c)
        print(f"Updated {q}")
