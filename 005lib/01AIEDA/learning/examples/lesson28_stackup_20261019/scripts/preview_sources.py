from pathlib import Path
import sys,html,json,hashlib
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
sys.path.insert(0,r'D:\001DIY\005lib\01AIEDA\learning\tools\pymupdf_1_28_2')
import pymupdf
for name,pages in [('Kingboard_KB6167F.pdf',[0,1]),('TI_SCAA082A.pdf',[])]:
 doc=pymupdf.open(B/'source'/name)
 texts=[]
 for i,p in enumerate(doc):
  t=p.get_text();texts.append('=== PDF PAGE %d ===\n%s'%(i+1,t))
  if name.startswith('TI') and ('return path' in t.lower() or 'stackup' in t.lower()):
   print('TI relevant page',i+1);pages.append(i)
 (B/'source'/name.replace('.pdf','.txt')).write_text('\n'.join(texts),encoding='utf-8')
 for i in sorted(set(pages))[:5]:
  doc[i].get_pixmap(matrix=pymupdf.Matrix(1.25,1.25)).save(B/'source'/(Path(name).stem+'_page%02d.png'%(i+1)))
spec=json.loads((B/'specification.json').read_text())
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1450" height="1210" viewBox="0 0 1450 1210"><rect width="1450" height="1210" fill="#f5f7fb"/>']
def text(x,y,s,size=18,color='#1e293b',weight='normal'):
 svg.append('<text x="%s" y="%s" font-family="Arial,sans-serif" font-size="%s" font-weight="%s" fill="%s">%s</text>'%(x,y,size,weight,color,html.escape(s)))
text(40,48,'Lesson 28 | Native 2-layer / 4-layer cross sections',30,weight='bold')
text(40,80,'Allegro 17.2 S045. Reopened native database values; diagram uses a minimum visible row height.',18)
for n,xoff in [(2,40),(4,750)]:
 t=spec['targets'][str(n)]
 text(xoff,132,t['name'],24,weight='bold')
 text(xoff,164,'CAD copper order: '+('TOP - BOTTOM' if n==2 else 'TOP - L2 - L3 - BOTTOM'),20)
 y=205
 for row in t['nativeCrossSection']:
  typ=row['type'].strip('"');name=row['name'].strip('"');mat=row['material'].strip('"')
  thick=float(row['thickness'])
  h=max(36,thick*225)
  color={'CONDUCTOR':'#d98c36','DIELECTRIC':'#9fc7e8','MASK':'#b5a5e8'}[typ]
  svg.append('<rect x="%s" y="%s" width="635" height="%s" fill="%s" stroke="#ffffff" stroke-width="2"/>'%(xoff,y,h,color))
  short=name if name!='nil' else ('CORE' if thick>0.5 else 'PREPREG 7628')
  desc='%s  |  %.5f mm'%(short,thick)
  if typ in ('DIELECTRIC','MASK'):
   desc+='  |  Dk '+row['dk'].strip('"')
   if n==2 and typ=='MASK':desc+=' [unqualified default]'
  text(xoff+12,y+24,desc,17)
  y+=h
 text(xoff,y+35,'Copper + dielectric = %.5f mm'%t['copperDielectricSum_mm'],19,weight='bold')
 text(xoff,y+65,'Including modeled mask = %.5f mm'%t['sumIncludingModeledMasks_mm'],19)
 text(xoff,y+95,'Factory order nominal thickness = 1.6 mm (separate datum)',17)
text(40,900,'Teaching through-via: 0.30 mm finished hole / 0.60 mm regular copper, TOP through BOTTOM.',20)
text(40,935,'Confirmed: 80 components, 69 nets, 22 placed physical pins; 6 NPTHs remain copper-free on every layer.',19)
text(40,970,'4-layer intent: TOP signal/power - L2 continuous GND - L3 continuous GND - BOTTOM signal/power.',19)
text(40,1005,'L2/L3 planes have NOT been poured yet. The numeric stackup does not prove a valid return path.',19,color='#9a3412')
text(40,1040,'90-ohm USB trace width / spacing remains subject to the actual factory impedance stackup.',19,color='#9a3412')
text(40,1075,'JLC mask: flat C2 model only. Df defaults / 2L purple-mask Dk are not qualified material data.',18)
text(40,1110,'Source tables, deviations, raw readback, challenge logs and validation.json are archived in this lesson directory.',16)
text(40,1150,'2L fabrication release: inherited USB mask web 0.100 mm is below OSH minimum 0.1016 mm.',18,color='#9a3412')
svg.append('</svg>')
p=B/'preview.svg';p.write_text('\n'.join(svg),encoding='utf-8')
doc=pymupdf.open('svg',p.read_bytes());doc[0].get_pixmap(matrix=pymupdf.Matrix(1,1)).save(B/'preview.png')
print('Preview SVG/PNG created')
