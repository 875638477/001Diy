import sys,pathlib,xml.etree.ElementTree as ET
b=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning')
sys.path.insert(0,str(b/'tools'/'pymupdf_1_28_2'))
import pymupdf
s=b/'examples'/'lesson07_completion_20261018'/'preview.svg'
# Flatten CSS text fills in memory for MuPDF SVG support; original SVG is unchanged.
r=ET.fromstring(s.read_bytes())
for t in r.iter('{http://www.w3.org/2000/svg}text'):
 t.set('fill','#0b1420' if t.get('y')=='390' and float(t.get('x','0'))<820 else '#edf3fa')
 t.set('font-family','Arial')
d=pymupdf.open(stream=ET.tostring(r),filetype='svg')
q=pymupdf.open('pdf',d.convert_to_pdf())
q[0].get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(s.with_suffix('.png'))
print(str(s.with_suffix('.png')))
