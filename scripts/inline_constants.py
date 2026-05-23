import re

def load_constants(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Match CONSTANT_NAME = <value>
    # We want to be careful with multi-line or complex ones, but most are simple single lines.
    constants = {}
    for line in content.split('\n'):
        match = re.match(r'^([A-Z0-9_]+)\s*=\s*(.*)', line)
        if match:
            name, value = match.groups()
            # remove comments from value
            value = value.split('#')[0].strip()
            constants[name] = value
    return constants

def inline_in_file(filepath, constants):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We need to replace occurrences of the constant, but only as whole words.
    # Also, we should probably just remove the huge import block at the top of registry.py
    # and let ruff/isort or manual fixing handle imports.
    
    for name, value in constants.items():
        if name in content:
            # We don't want to replace inside the import statement if we can help it, 
            # or maybe we do, and we just clean up the import later.
            pass
            
if __name__ == '__main__':
    c = load_constants('mlsysim/mlsysim/core/constants.py')
    print(f"Loaded {len(c)} constants.")
