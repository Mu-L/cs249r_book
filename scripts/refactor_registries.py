import re
import os

CONSTANTS_FILE = 'mlsysim/mlsysim/core/constants.py'
HARDWARE_REG_FILE = 'mlsysim/mlsysim/hardware/registry.py'
MODELS_REG_FILE = 'mlsysim/mlsysim/models/registry.py'

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)

# 1. Parse constants.py
content = read_file(CONSTANTS_FILE)
constants = {}
for line in content.split('\n'):
    match = re.match(r'^([A-Z0-9_]+)\s*=\s*(.*)', line)
    if match:
        name, value = match.groups()
        value = value.split('#')[0].strip()
        constants[name] = value

# 2. Refactor a registry file
def refactor_registry(filepath):
    content = read_file(filepath)
    
    # Extract the import block for constants
    import_pattern = r'from \.\.core\.constants import \((.*?)\)'
    match = re.search(import_pattern, content, re.DOTALL)
    if not match:
        return
        
    imported_names = [name.strip() for name in match.group(1).replace('\n', ' ').split(',') if name.strip()]
    
    # We will need to figure out what base units are used in the values
    used_base_units = set()
    base_units = ['ureg', 'Q_', 'byte', 'bit', 'second', 'ms', 'us', 'ns', 'hour', 'day', 'year', 'KB', 'MB', 'GB', 'TB', 'PB', 'Kbps', 'Mbps', 'Gbps', 'Tbps', 'flop', 'kflop', 'MFLOPs', 'GFLOPs', 'TFLOPs', 'PFLOPs', 'EFLOPs', 'ZFLOPs', 'watt', 'milliwatt', 'kilowatt', 'picojoule', 'nanojoule', 'microjoule', 'millijoule', 'joule', 'kilojoule', 'THOUSAND', 'MILLION', 'BILLION', 'TRILLION', 'count', 'GiB', 'TOPS', 'USD', 'param', 'Mparam', 'Bparam', 'Kparam', 'BYTES_FP32', 'BYTES_FP16', 'BYTES_INT8', 'BYTES_INT4', 'BYTES_INT32', 'BYTES_ADAM_STATE']
    
    new_content = content
    for name in imported_names:
        if name in constants:
            val = constants[name]
            # Find which base units are in the value
            for unit in base_units:
                if re.search(rf'\b{unit}\b', val):
                    used_base_units.add(unit)
            
            # Replace the constant in the text (only as whole word)
            # Exclude the import block itself by doing this carefully, or just replace everywhere and then fix the import.
            new_content = re.sub(rf'\b{name}\b', val, new_content)
    
    # Fix the import block
    if 'ureg' not in used_base_units:
        used_base_units.add('ureg')
    
    new_import = f"from ..core.constants import ({', '.join(sorted(list(used_base_units)))})"
    new_content = re.sub(import_pattern, new_import, new_content, flags=re.DOTALL)
    
    write_file(filepath, new_content)

refactor_registry(HARDWARE_REG_FILE)
refactor_registry(MODELS_REG_FILE)
print("Registries refactored.")
