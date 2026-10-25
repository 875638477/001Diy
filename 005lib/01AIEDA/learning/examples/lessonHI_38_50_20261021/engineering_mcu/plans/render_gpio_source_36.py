import pathlib,json,sys,math,html
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
sys.path.insert(0,str(R.parents[2]/'tools/pymupdf_1_28_2'));import pymupdf as fitz
n=load(P/'GPIO_future_2L_36_snapshot.json');pol=load(P/'GPIO_future_2L_36_policy.json');s=CopperScene(n,load(P/'GPIO_future_2L_36_networks.json'),load(P/'GPIO_future_2L_36_rules.json'),pol)
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="2140" height="1100"><rect width="2140" height="1100" fill="white"/>']
cols={'GND':'#a7c9b0','V3V3':'#e09569','GPIO_PA1':'#d94a68','GPIO_PA2':'#d98d08','GPIO_PA3':'#0033cc','GPIO_PC13':'#773399','GPIO_PC15':'#a737d4','GPIO_PB10':'#174a6e','GPIO_PB11':'#ff5d4e','GPIO_PB1':'#cc9900','BOOT1':'#8f7c23'}
for layer,ox in [('TOP',30),('BOTTOM',1080)]:
 scale=55;x0,y0,x1,y1=28,18,49,36.5
 def screen(g):return affinity.affine_transform(g,[scale,0,0,-scale,ox-scale*x0,40+scale*y1])
 from shapely import affinity
 clip=box(x0,y0,x1,y1)
 parts.append(f'<text x="{ox}" y="25" font-size="20">{layer} FUTURE only, not native readback</text>')
 for x in range(28,50):parts.append(f'<path d="M {ox+(x-x0)*scale} 40 v1018" stroke="#ddd"/><text x="{ox+(x-x0)*scale}" y="1080" font-size="12">{x}</text>')
 for y in range(18,37):parts.append(f'<path d="M{ox} {40+(y1-y)*scale} h1045" stroke="#ddd"/><text x="{ox-20}" y="{40+(y1-y)*scale}" font-size="12">{y}</text>')
 for area in pol['reservedAreas']:
  if layer in area.get('layers',LAYERS):
   g=Polygon(area['polygon']).intersection(clip)
   if not g.is_empty and g.area>1e-10:parts.append(screen(g).svg(fill_color='#cccccc').replace('opacity="0.6"','opacity="0.3"'))
 for o in s.obstacles:
  if o['layer']!=layer:continue
  g=o['geometry'].intersection(clip)
  if g.is_empty or g.area<1e-10:continue
  parts.append(screen(g).svg(fill_color=cols.get(o['net'],'#627480')).replace('stroke="#555555"','stroke="#333333"').replace('stroke-width="2.0"','stroke-width=".25"'))
  if o['kind']=='smdpin':
   cc=screen(g).centroid;parts.append(f'<text x="{cc.x}" y="{cc.y}" font-size="9">{o["source"]}</text>')
 for a in pol['componentAnchors']:
  if clip.covers(Point(a['xy'])):
   x,y=a['xy'];sx,sy=ox+(x-x0)*scale,40+(y1-y)*scale
   parts.append(f'<circle cx="{sx}" cy="{sy}" r="3" fill="black"/><text x="{sx+5}" y="{sy-4}" font-size="12">{a["net"].removeprefix("GPIO_")}</text>')
parts.append('</svg>');svg=''.join(parts);(P/'GPIO_future_source_36.svg').write_text(svg,encoding='utf8');d=fitz.open(stream=svg.encode(),filetype='svg');d.get_page_pixmap(0,alpha=False).save(P/'GPIO_future_source_36.png');print('rendered')


