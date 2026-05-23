import re
import glob

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    with open(q, 'r') as f: c = f.read()
    orig = c
    
    if 'data_engineering.qmd' in q:
        c = c.replace('calc_transfer_time(dataset_pb * ureg.petabyte, network_bw)', '(dataset_pb * ureg.petabyte) / network_bw')
        c = c.replace('calc_transfer_time(dataset_pb * ureg.petabyte, 10 * Gbps)', '(dataset_pb * ureg.petabyte) / (10 * Gbps)')
        c = c.replace('from mlsysim.core.formulas import calc_transfer_time', '')

    if c != orig:
        with open(q, 'w') as f: f.write(c)

