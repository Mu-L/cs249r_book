import os
import glob
import subprocess
import tempfile

qmd_files = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)

for qmd in qmd_files:
    with open(qmd, 'r') as f:
        content = f.read()
    
    # Extract all python code blocks
    import re
    blocks = re.findall(r'```\{python\}(.*?)```', content, re.DOTALL)
    if not blocks:
        continue
        
    combined_code = "\n".join(blocks)
    
    # Write to a temp file and run pyflakes
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as temp:
        temp.write(combined_code)
        temp_name = temp.name
        
    result = subprocess.run(['python3', '-m', 'pyflakes', temp_name], capture_output=True, text=True)
    if result.stdout or result.stderr:
        print(f"\n--- Errors in {qmd} ---")
        # Filter out unused imports for this check, focus on undefined names
        errors = [line for line in result.stdout.split('\n') if 'undefined name' in line]
        for e in errors:
            print(e.split(':', 1)[1].strip())
            
    os.remove(temp_name)
