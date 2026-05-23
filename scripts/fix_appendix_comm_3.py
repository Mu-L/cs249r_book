import re
q = 'book/quarto/contents/vol2/backmatter/appendix_communication.qmd'
with open(q, 'r') as f: c = f.read()

c = c.replace('.magnitude)', ')')

with open(q, 'w') as f: f.write(c)
