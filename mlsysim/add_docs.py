import os
import ast

def insert_docstring(filepath, node_name, docstring):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    tree = ast.parse(source)
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == node_name:
            if not ast.get_docstring(node):
                line_idx = node.lineno - 1
                # Find the line ending with :
                while line_idx < len(lines) and not lines[line_idx].strip().endswith(':'):
                    # handle multi-line defs
                    if ':' in lines[line_idx].split('#')[0]: # naive check
                        break
                    line_idx += 1
                
                indent = " " * (node.col_offset + 4)
                doc = f'{indent}"""{docstring}"""\n'
                lines.insert(line_idx + 1, doc)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                return True
    return False

# Core engine and types
insert_docstring('mlsysim/mlsysim/core/engine.py', 'PerformanceProfile', 'The resulting performance metrics bounded by hardware limits.')
insert_docstring('mlsysim/mlsysim/models/types.py', 'TransformerWorkload', 'Workload representation of an autoregressive Transformer (e.g., LLMs).')
insert_docstring('mlsysim/mlsysim/models/types.py', 'SparseTransformerWorkload', 'Workload representation of a Mixture-of-Experts (MoE) Transformer.')
insert_docstring('mlsysim/mlsysim/models/types.py', 'CNNWorkload', 'Workload representation of a Convolutional Neural Network (e.g., Vision).')
insert_docstring('mlsysim/mlsysim/models/types.py', 'SSMWorkload', 'Workload representation of a State Space Model (e.g., Mamba).')
insert_docstring('mlsysim/mlsysim/models/types.py', 'DiffusionWorkload', 'Workload representation of a Diffusion generative model.')

# Registries
for reg in ['Hardware', 'Models', 'Systems', 'Infrastructure', 'Datasets', 'Literature', 'Ops', 'LanguageModels', 'VisionModels', 'TinyModels', 'Datacenters', 'Racks']:
    for root, _, files in os.walk('mlsysim'):
        for file in files:
            if file == 'registry.py':
                insert_docstring(os.path.join(root, file), reg, f'Registry namespace for {reg}.')

