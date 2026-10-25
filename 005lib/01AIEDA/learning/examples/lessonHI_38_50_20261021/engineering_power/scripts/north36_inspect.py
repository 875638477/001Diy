import pathlib,sys,json,math
H=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *

P=H/'engineering_mcu/plans';n=load(P/'GPIO_future_2L_36_snapshot.json');w=load(P/'GPIO_future_2L_36_networks.json');r=load(P/'GPIO_future_2L_36_rules.json');p=load(P/'GPIO_future_2L_36_policy.json');scene=CopperScene(n,w,r,p)
sel=['GPIO_PA1','GPIO_PA2','GPIO_PA3','GPIO_PC13','GPIO_PC14','GPIO_PC15'];cols=['#c12b20','#cf8515','#227b19','#722a9c','#1491aa','#cf207c'];colors=dict(zip(sel,cols));colors.update(GND='#708c71',V3V3='#dc3bac',VDDA='#c63bb8',ADC0='#08a3ab',ADC_IN='#00aeb7')
print('Anchors',json.dumps([a for a in p['componentAnchors'] if a['net'] in sel]))
print('ROUTES',json.dumps([a for a in n['routes'] if a['net'] in sel]))
print('VIAS',json.dumps([a for a in n['vias'] if a['net'] in sel]))
for layer in LAYERS:
 x0,y0,x1,y1=30,27,44,34;scale=140
 shapes=[]
 def pp(pt):return ((pt[0]-x0)*scale,(y1-pt[1])*scale)
 for a in scene.obstacles:
  if a['layer']!=layer:continue
  geom=a['geometry'];parts=[geom] if geom.geom_type=='Polygon' else list(getattr(geom,'geoms',[]))
  for poly in parts:
   if poly.geom_type!='Polygon':continue
   color=colors.get(a['net'],'#c1a14e' if a['kind'] in ['smdpin','thrupin','via'] else '#315292');shapes.append('<polygon points="'+' '.join(str(pp(q)[0])+' ,'+str(pp(q)[1]) for q in poly.exterior.coords)+'" fill="'+color+'"/>')
 for y in range(27,35):
  shapes.append(f'<text x="0" y="{pp([30,y])[1]}" font-size="16">{y}</text>')
 for x in range(30,45):shapes.append(f'<text x="{pp([x,34])[0]}" y="16" font-size="16">{x}</text>')
 for a in p['componentAnchors']:
  if a['net'] in sel:shapes.append(f'<text x="{pp(a["xy"])[0]}" y="{pp(a["xy"])[1]}" font-size="14" fill="black">{a["net"]}</text>')
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="1960" height="980">'+''.join(shapes)+'</svg>'
 (H/f'engineering_power/readouts/north36_{layer}.svg').write_text(svg)
 sys.path.insert(0,r'D:/001DIY/005lib/01AIEDA/learning/tools/pymupdf_1_28_2')
 import pymupdf
 z=pymupdf.open(stream=svg.encode(),filetype='svg');pdf=pymupdf.open(stream=z.convert_to_pdf(),filetype='pdf');pdf[0].get_pixmap().save(str(H/f'engineering_power/readouts/north36_{layer}.png'))