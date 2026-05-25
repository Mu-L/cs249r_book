import re
import glob

def read(f):
    with open(f, 'r') as file: return file.read()
def write(f, c):
    with open(f, 'w') as file: file.write(c)

# Fix __init__.py to export formulas
init_path = 'mlsysim/mlsysim/__init__.py'
init_content = read(init_path)
if 'calc_transfer_time' not in init_content:
    init_content = init_content.replace(
        'from .fmt import fmt, check, MarkdownStr',
        'from .core.formulas import *\nfrom .fmt import fmt, check, MarkdownStr'
    )
    write(init_path, init_content)

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    c = read(q)
    orig = c
    
    # 2. Fix Models.* aliases
    models = ['GPT2', 'GPT3', 'GPT4', 'BERT_Base', 'BERT_Large', 'Llama2_70B', 'Llama2_7B', 'Llama3_8B', 'Llama3_70B']
    for m in models:
        c = re.sub(rf'\bModels\.{m}\b', f'Models.Language.{m}', c)
    c = c.replace('Models.Language.Language.', 'Models.Language.')
    c = c.replace('Models.Language.Vision.', 'Models.Vision.')
    
    # 3. Fix ServingResult.weight_memory -> memory_footprint
    c = c.replace('res.weight_memory.m_as', 'res.memory_footprint.m_as')
    
    # 4. Fix iPhone15Pro15Pro
    c = c.replace('iPhone15Pro15Pro', 'iPhone15Pro')
    
    # 5. Fix constants.Hardware
    c = c.replace('constants.Hardware', 'Hardware')
    c = c.replace('constants.Models', 'Models')
    
    # 6. Fix Hardware.Networks.Fabrics
    c = c.replace('Hardware.Networks.Fabrics.', 'Hardware.Networks.')
    
    # 8. Fix GenericNode
    c = c.replace('Hardware.Cloud.GenericNode', 'Hardware.Cloud.GenericServer')
    
    # 10. Fix Formatting Precision Error
    c = c.replace('fmt(e_cpu_j / 50.0, precision=3, commas=False)', 'fmt(e_cpu_j / 50.0, precision=4, commas=False)')
    
    # 13. Fix attention_heads -> heads
    c = c.replace('.attention_heads', '.heads')
    
    # 15. Fix IMAGENET_CLASSES
    if 'IMAGENET_CLASSES' in c:
        c = c.replace('IMAGENET_CLASSES', '1000') # Hardcode since it's 1000
        
    # 16. Fix h100
    if 'h100.tdp' in c:
        c = c.replace('h100.tdp', 'h_h100.tdp')
        c = c.replace('h100 = Hardware.Cloud.H100', 'h_h100 = Hardware.Cloud.H100')
    
    # Fix calc_ring_allreduce_time
    if 'calc_ring_allreduce_time(grad_70b, num_gpus, ib_ndr)' in c:
        c = c.replace('calc_ring_allreduce_time(grad_70b, num_gpus, ib_ndr)', 'calc_ring_allreduce_time(grad_70b, num_gpus, ib_ndr, 0*ureg.ms)')
        c = c.replace('calc_ring_allreduce_time(grad_1b, num_gpus, ib_ndr)', 'calc_ring_allreduce_time(grad_1b, num_gpus, ib_ndr, 0*ureg.ms)')
    
    if 'calc_ring_allreduce_time(gradient_tensor, gpus_per_node, nvlink_bw)' in c:
        c = c.replace('calc_ring_allreduce_time(gradient_tensor, gpus_per_node, nvlink_bw)', 'calc_ring_allreduce_time(gradient_tensor, gpus_per_node, nvlink_bw, 0*ureg.ms)')

    if c != orig:
        write(q, c)
        print(f"Updated {q}")

