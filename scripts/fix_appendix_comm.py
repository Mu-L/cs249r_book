import re
q = 'book/quarto/contents/vol2/backmatter/appendix_communication.qmd'
with open(q, 'r') as f: c = f.read()

c = c.replace('ib_ndr.m_as', 'ib_ndr.bandwidth.m_as')
c = c.replace('ib_hdr.m_as', 'ib_hdr.bandwidth.m_as')
c = c.replace('roce.m_as', 'roce.bandwidth.m_as')
c = c.replace('tcp.m_as', 'tcp.bandwidth.m_as')

with open(q, 'w') as f: f.write(c)
