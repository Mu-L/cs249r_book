import re
q = 'book/quarto/contents/vol2/fault_tolerance/fault_tolerance.qmd'
with open(q, 'r') as f: c = f.read()

c = c.replace('from mlsysim.core.formulas import calc_transfer_time', '')
c = c.replace('calc_transfer_time(total_ckpt_qty, nfs_bw)', '(total_ckpt_qty / nfs_bw)')
c = c.replace('calc_transfer_time(per_node_shard_qty, pcie_bw)', '(per_node_shard_qty / pcie_bw)')

with open(q, 'w') as f: f.write(c)
