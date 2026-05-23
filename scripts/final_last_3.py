import re
import glob

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    with open(q, 'r') as f: c = f.read()
    orig = c
    
    # Remove allow_zero=True from fmt_percent
    c = re.sub(r'(fmt_percent\([^)]*)allow_zero=True,\s*', r'\1', c)
    c = re.sub(r'(fmt_percent\([^)]*),\s*allow_zero=True', r'\1', c)

    if c != orig:
        with open(q, 'w') as f: f.write(c)

