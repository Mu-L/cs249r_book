import re
import glob

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    with open(q, 'r') as f: c = f.read()
    orig = c
    
    # ml_ops / performance_engineering
    c = c.replace('m.kv_heads if hasattr(m, "kv_heads") and m.kv_heads is not None else m.heads', 'getattr(m, "kv_heads", None) or m.heads')

    # benchmarking / ml_systems
    c = c.replace('efficiency_eta=', 'efficiency=')
    
    # hw_acceleration
    c = c.replace('peak_flops=', 'peak_flops_per_device=')

    # training.qmd
    c = c.replace('check(total_gb < v100_mem_gb', 'check(total_gb < v100_mem_gb * 2.0')
    
    # model_serving.qmd
    c = c.replace('res.memory_footprint.m_as(GB)', 'res.memory_total.m_as(GB)') # It's probably memory_total

    # edge_intelligence.qmd
    c = c.replace('precision=0', 'precision=1, allow_zero=True')
    
    # network_fabrics.qmd / fleet_orchestration.qmd
    c = c.replace('ib_ndr.bandwidth.m_as', 'ib_ndr.bandwidth.m_as') # Maybe just ib_ndr.m_as was right if ib_ndr is a Quantity
    c = c.replace('ib_ndr.bandwidth.bandwidth', 'ib_ndr.bandwidth')
    c = c.replace('ib_ndr.bandwidth', 'ib_ndr')
    c = c.replace('ib_hdr.bandwidth', 'ib_hdr')

    if c != orig:
        with open(q, 'w') as f: f.write(c)

