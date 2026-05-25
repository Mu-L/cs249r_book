import glob

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    with open(q, 'r') as f: c = f.read()
    orig = c
    
    if 'data_selection.qmd' in q:
        c = c.replace('c.Models', 'Models')
        c = c.replace('c.Hardware', 'Hardware')

    if c != orig:
        with open(q, 'w') as f: f.write(c)

