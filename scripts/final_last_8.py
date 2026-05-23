import re
import glob

qmds = glob.glob('book/quarto/contents/**/*.qmd', recursive=True)
for q in qmds:
    with open(q, 'r') as f: c = f.read()
    orig = c
    
    # Check for dTime kwargs
    c = c.replace('efficiency=', 'efficiency_eta=')
    # Re-fix Engine.solve since that actually uses efficiency=
    c = c.replace('Engine.solve(m_bert, h_a100, batch_size=batch_1, precision="fp32", efficiency_eta=1.0)', 'Engine.solve(m_bert, h_a100, batch_size=batch_1, precision="fp32", efficiency=1.0)')
    c = c.replace('Engine.solve(m_bert, h_a100, batch_size=batch_32, precision="fp32", efficiency_eta=0.85)', 'Engine.solve(m_bert, h_a100, batch_size=batch_32, precision="fp32", efficiency=0.85)')
    c = re.sub(r'Engine\.solve\(([^,]+),\s*([^,]+),\s*batch_size=([^,]+),\s*precision="([^"]+)",\s*efficiency_eta=([^\)]+)\)', r'Engine.solve(\1, \2, batch_size=\3, precision="\4", efficiency=\5)', c)

    if c != orig:
        with open(q, 'w') as f: f.write(c)

