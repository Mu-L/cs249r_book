import re
import glob

def r(f):
    with open(f, 'r') as fh: return fh.read()

def w(f, c):
    with open(f, 'w') as fh: fh.write(c)

for q in glob.glob('book/quarto/contents/**/*.qmd', recursive=True):
    c = r(q)
    orig = c

    if 'edge_intelligence.qmd' in q:
        c = c.replace('fmt(efficiency_drop, precision=1, allow_zero=True', 'fmt(efficiency_drop, precision=3, allow_zero=True')

    if 'fleet_orchestration.qmd' in q:
        c = c.replace('nvme_drive_capacity_tb_val.bandwidth.m_as', 'nvme_drive_capacity_tb_val.m_as')

    if 'inference.qmd' in q:
        c = c.replace('sp_high = _speedup(alpha_high_val, K)', 'sp_high = _speedup(alpha_high, K)')
        c = c.replace('sp_med = _speedup(alpha_med_val, K)', 'sp_med = _speedup(alpha_med, K)')
        c = c.replace('sp_low = _speedup(alpha_low_val, K)', 'sp_low = _speedup(alpha_low, K)')
        
        c = c.replace('et_high = sum(alpha_high_val', 'et_high = sum(alpha_high')
        c = c.replace('et_med = sum(alpha_med_val', 'et_med = sum(alpha_med')
        c = c.replace('et_low = sum(alpha_low_val', 'et_low = sum(alpha_low')
        
        if 'alpha_high = 0.9' not in c:
            c = c.replace('alpha_high_val = 0.9', 'alpha_high = 0.9')
            c = c.replace('alpha_med_val = 0.7', 'alpha_med = 0.7')
            c = c.replace('alpha_low_val = 0.5', 'alpha_low = 0.5')

    if 'network_fabrics.qmd' in q:
        c = c.replace('ib_ndr.m_as(', 'ib_ndr.bandwidth.m_as(')
        c = c.replace('ib_hdr.m_as(', 'ib_hdr.bandwidth.m_as(')
        c = c.replace('roce.m_as(', 'roce.bandwidth.m_as(')
        c = c.replace('tcp.m_as(', 'tcp.bandwidth.m_as(')
        c = c.replace('nvlink_bw = nvlink_bw.m_as', 'nvlink_bw = nvlink_bw.bandwidth.m_as')

    if 'performance_engineering.qmd' in q:
        c = c.replace("h.compute.precision_flops['fp16']", "h.compute.precision_flops.get('fp16', h.compute.peak_flops)")
        c = c.replace("h.compute.precision_flops['fp32']", "h.compute.precision_flops.get('fp32', h.compute.peak_flops)")

    if 'robust_ai.qmd' in q:
        c = c.replace('.items', '.items()')
        c = c.replace('.items()()', '.items()')
        
    if 'fault_tolerance.qmd' in q:
        c = c.replace('.items', '.items()')
        c = c.replace('.items()()', '.items()')

    if 'sustainable_ai.qmd' in q:
        if 'h_h100 = Hardware.Cloud.H100' not in c:
            c = c.replace('h_h100.', 'Hardware.Cloud.H100.')
            c = c.replace('h_h100 = Hardware.Cloud.H100', '')

    if c != orig:
        w(q, c)
        print(f"Updated {q}")
