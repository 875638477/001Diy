import pathlib,sys,json,csv,re
BASE=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE.parents[1]/'tools'/'pymupdf_1_28_2'))
import pymupdf
spec=json.loads((BASE/'lesson09_spec.json').read_text(encoding="utf-8-sig"))
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig'),delimiter='\t'))
def box(v):return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',v)]
doc=pymupdf.open();p=doc.new_page(width=1600,height=850)
p.draw_rect(p.rect,color=None,fill=(1,1,1))
p.insert_text((40,55),'LESSON 09 | QFP / QFN / EXPOSED PAD',fontsize=28,color=(.12,.2,.3))
p.insert_text((40,88),'Preview from saved Allegro pad / shape read-back. Not a Cadence screenshot. Units: mm.',fontsize=16)
for index,sp in enumerate(spec['packages']):
 d=BASE/'logs'/(sp['name']+'_reopen03');pins=rows(d/'pins.tsv');pads=rows(d/'pads.tsv');shapes=rows(d/'shapes.tsv')
 ox=280+index*520;oy=410;scale=40 if index==0 else 112
 def pt(x,y):return (ox+x*scale,oy-y*scale)
 def rect(bb):return pymupdf.Rect(pt(bb[0],bb[3]),pt(bb[2],bb[1]))
 p.insert_text((ox-225,140),sp['part'],fontsize=23,color=(.12,.2,.3))
 sub=['LQFP48 | manufacturer land','VQFN16 + EP17 | TI single aperture','VQFN16 + EP17 | teaching split paste'][index]
 p.insert_text((ox-225,169),sub,fontsize=17)
 body=sp['body']/2
 p.draw_rect(rect([-body,-body,body,body]),color=(.3,.5,.8),width=1.2,dashes='[5 3] 0')
 for pin in pins:
  x,y=float(pin['x']),float(pin['y']);n=pin['number']
  for layer,color,fill in [('PIN/SOLDERMASK_TOP',(.65,.3,.78),None),('ETCH/TOP',(.77,.4,.06),(1,.75,.3)),('PIN/PASTEMASK_TOP',(.8,.1,.2),(1,.65,.68))]:
   row=next(r for r in pads if r['number']==n and r['layer']==layer)
   if row['figure']=='NULL':continue
   w,h,r=float(row['width']),float(row['height']),float(row['radius'])
   bb=[x-w/2,y-h/2,x+w/2,y+h/2]
   p.draw_rect(rect(bb),color=color,fill=fill,width=.8 if layer!='PIN/SOLDERMASK_TOP' else 1.2,radius=r/min(w,h) if r else None,fill_opacity=.75)
  if 'ep' in sp and n=='17':lx,ly=0,0
  else:
   mult=1.33 if index else 1.29;lx,ly=x*mult,y*mult
  p.insert_text((pt(lx,ly)[0]-5,pt(lx,ly)[1]+4),n,fontsize=9 if index==0 else 12,color=(.12,.15,.2))
 for row in shapes:
  if row['layer']=='PACKAGE GEOMETRY/PASTEMASK_TOP':p.draw_rect(rect(box(row['bbox'])),color=(.8,.1,.2),fill=(1,.65,.68),width=1)
 p.draw_line(pt(-.08,0),pt(.08,0),color=(0,0,0),width=1);p.draw_line(pt(0,-.08),pt(0,.08),color=(0,0,0),width=1)
 captions=[['48 pins, 0.50 pitch; origin at package center','Land 1.20 x 0.30; outer span 9.70','Height MAX 1.60; min copper gap 0.20','ST reference rotated 90 deg clockwise'],['16 + EP17 pins, 0.50 pitch; center span 2.80','Land 0.60 x 0.24 R0.05; EP 1.68 sq R0.05','Paste 1.55 sq R0.05; 85.11% area','Height MAX 1.00; min copper gap 0.26'],['Same copper / mask / numbering as single','4 windows 0.65 sq; gutter 0.20','Paste coverage 59.92% of rounded EP area','Teaching alternative; assembly approval required']][index]
 for j,t in enumerate(captions):p.insert_text((ox-225,665+j*28),t,fontsize=14)
p.insert_text((40,805),'Purple = solder mask opening; orange = copper; pink = paste; dashed blue = body. Pin labels are illustrative.',fontsize=14)
p.insert_text((40,830),'QFN center REF DES silk is retained at (0,0) per user rule and must be relocated or clipped in manufacturing output.',fontsize=14,color=(.7,.15,.1))
p.get_pixmap(matrix=pymupdf.Matrix(1,1)).save(BASE/'preview'/'lesson09_footprints.png')
print('Saved lesson09_footprints.png')


