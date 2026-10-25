from pathlib import Path
O=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson28_stackup_20261019_review')
p=O/'review28.py';s=p.read_text()
s=s.replace("(O/'review.json').write_text", """report['findings'].extend([
 {'id':'R28-04','severity':'closed evidence gap','issue':'Legacy fgeo geometry omitted DESIGN_OUTLINE. Three explicit readonly mechanical-direct exports now prove source/2L/4L outline and keepin/out identical with unchanged board hashes.'},
 {'id':'R28-05','severity':'assembly open item and corrected documentation','issue':'GCT S0.95+/-0.15mm is Shell Stake Length from connector mounting/SMT datum, not bottom-of-finished-board protrusion. Nominal1.6mm board compatibility with selected GF-A stake and soldering process remains unqualified; lesson27 note corrected with before-copy retained.'}
])
(O/'review.json').write_text""")
p.write_text(s)
