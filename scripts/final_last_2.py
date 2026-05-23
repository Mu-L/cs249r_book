import glob

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    with open(q, 'r') as f: c = f.read()
    orig = c
    
    # Remove allow_zero=True from fmt_percent
    c = c.replace('fmt_percent(bert_util_peak, precision=1, allow_zero=True, commas=False)', 'fmt_percent(bert_util_peak, precision=1, commas=False)')
    
    # Remove allow_zero=True from fmt_percent generally
    c = c.replace('fmt_percent(val, precision=1, allow_zero=True', 'fmt_percent(val, precision=1')

    if c != orig:
        with open(q, 'w') as f: f.write(c)

