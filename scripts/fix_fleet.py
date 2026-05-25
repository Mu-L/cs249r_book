q = 'book/quarto/contents/vol2/fleet_orchestration/fleet_orchestration.qmd'
with open(q, 'r') as f: c = f.read()

# Replace all bandwidth.m_as with m_as
c = c.replace('.bandwidth.m_as', '.m_as')

# Then specifically add it back to ib_ndr
c = c.replace('ib_ndr.m_as', 'ib_ndr.bandwidth.m_as')

with open(q, 'w') as f: f.write(c)
