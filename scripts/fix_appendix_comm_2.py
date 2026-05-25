import re
q = 'book/quarto/contents/vol2/backmatter/appendix_communication.qmd'
with open(q, 'r') as f: c = f.read()

c = c.replace('ib_ndr, ib_ndr_alpha_us', 'ib_ndr.bandwidth, ib_ndr_alpha_us')
c = c.replace('ib_hdr, ib_hdr_alpha_us', 'ib_hdr.bandwidth, ib_hdr_alpha_us')

with open(q, 'w') as f: f.write(c)
