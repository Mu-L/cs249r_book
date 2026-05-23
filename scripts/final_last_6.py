import glob

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    with open(q, 'r') as f: c = f.read()
    orig = c
    
    if 'from mlsysim import *' in c and 'from mlsysim.core.constants import *' not in c:
        c = c.replace('from mlsysim import *', 'from mlsysim import *\nfrom mlsysim.core.constants import *')
        # Clean up duplicates
        c = c.replace('from mlsysim.core.constants import *\nfrom mlsysim.core.constants import *', 'from mlsysim.core.constants import *')
        c = c.replace('from mlsysim import *\nfrom mlsysim import *', 'from mlsysim import *')

    if c != orig:
        with open(q, 'w') as f: f.write(c)

