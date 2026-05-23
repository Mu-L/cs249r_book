import glob
import re

qmd_files = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)

for filepath in qmd_files:
    with open(filepath, 'r') as f:
        content = f.read()
        
    original = content
    # Remove all "from mlsysim import *"
    content = re.sub(r'^[ \t]*from mlsysim import \*\n', '', content, flags=re.MULTILINE)
    
    # Add "from mlsysim import *" to the start of every python block
    # Actually, it's safer to just replace ```{python} with ```{python}\nfrom mlsysim import *\nfrom mlsysim.core.constants import *
    # But only for blocks that actually use it or just all blocks?
    # All blocks is fine, it's cheap.
    
    content = re.sub(r'```\{python\}\n', '```{python}\nfrom mlsysim import *\nfrom mlsysim.core.constants import *\n', content)
    
    # Clean up double imports if we added them multiple times
    content = re.sub(r'(from mlsysim import \*\n)+', 'from mlsysim import *\n', content)
    content = re.sub(r'(from mlsysim.core.constants import \*\n)+', 'from mlsysim.core.constants import *\n', content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
print("Added global imports to all python blocks.")
