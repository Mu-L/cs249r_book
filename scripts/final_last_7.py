import glob

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    with open(q, 'r') as f: c = f.read()
    orig = c
    
    if 'hw_acceleration.qmd' in q:
        c = c.replace('total_ops=Models.Language.GPT3.training_ops,', 'total_ops=Models.Language.GPT3.training_ops,\n        num_devices=1,')
        c = c.replace('efficiency=1.0\n    )', 'efficiency_eta=1.0\n    )')

    if c != orig:
        with open(q, 'w') as f: f.write(c)

