from pathlib import Path
import sys,json,csv,hashlib,math,colorsys,html
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
sys.path[:0]=[str(H/'scripts'),str(O/'scripts'),str(H/'tooling/packages'),r'D:/001DIY/005lib/01AIEDA/learning/tools/pymupdf_1_28_2']
from cadence_poly import plane_from_native,polygon_from_vertices
from native_sexpr_data import parse
from shapely.geometry import Polygon,box,Point,LineString
import pymupdf
cp=H/'inventory/checkpoints/padentry_2L_b019_DRC_PENDING';n=json.loads((cp/'normalized.json').read_text());w=json.loads((cp/'networks.json').read_text());p=json.loads((O/'N49_2L_policy.json').read_text());log=Path(n['readbackDirectory'])
pads={a['name'].strip('"'):a for a in csv.DictReader((log/'padstacks.tsv').open(),delimiter='\t')};bounds=(32,18,48,33);window=box(*bounds)
nets=['GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15'];sources={a['net']:a['xy']for a in n['vias']if a['net']in nets};u1=next(c for c in n['placements']if c['ref']=='U1');pins={a['net']:a for a in u1['pins']if a['net']in nets};feed=[a for a in n['vias']if a['net']in ['GND','V3V3']and window.covers(Point(a['xy']))];feed.sort(key=lambda a:(a['net'],a['xy'][1],a['xy'][0]));boundary=list(csv.DictReader((log/'hi_dynamic_boundaries.tsv').open(),delimiter='\t'))
S=64;W=2350;HEIGHT=1570
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HEIGHT}" viewBox="0 0 {W} {HEIGHT}"><rect width="100%" height="100%" fill="#f7fafc"/><style>text{{font-family:Arial,sans-serif}}</style><text x="50" y="28" font-size="24">Actual 2L b019 MCU source bank / same TOP-view XY / no candidate copper</text><text x="50" y="55" font-size="15">SHA '+w['sha256']+'; bounds x32..48 / y18..33mm; .5mm grid, labels each1mm. Whole-board DRC pending.</text>']
def color(net):
 if net=='GND':return '#4a8165'
 if net=='V3V3':return '#a95200'
 if net in nets:return ['#e52f27','#a51583','#3050c9','#ce7d00','#008679','#7e47a9','#789205'][nets.index(net)]
 if net in ['USB_DP','PA12_SHARED']:return '#cc292a'
 if net in ['USB_DM','PA11_SHARED']:return '#145bc8'
 h=int(hashlib.sha256(str(net).encode()).hexdigest()[:4],16)/65535;return '#'+''.join(f'{int(z*255):02x}'for z in colorsys.hsv_to_rgb(h,.64,.66))
def parts(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return[g]
 return[p for a in getattr(g,'geoms',[])for p in parts(a)]
for panel,layer in enumerate(['TOP','BOTTOM']):
 ox=70+panel*1165;oy=125
 def xy(q):return ox+(q[0]-32)*S,oy+(33-q[1])*S
 def path(g,fill,alpha=1,stroke='none',sw=0,dash=''):
  for q in parts(g.intersection(window)):
   d=' '.join('M '+' L '.join(f'{a:.3f},{b:.3f}'for a,b in[xy(z)for z in r.coords])+' Z'for r in[q.exterior]+list(q.interiors));svg.append(f'<path d="{d}" fill="{fill}" fill-opacity="{alpha}" fill-rule="evenodd" stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')
 def text(q,s,size=11,fill='#24374a',anchor='middle',offset=(0,0)):
  x,y=xy(q);svg.append(f'<text x="{x+offset[0]:.2f}" y="{y+offset[1]:.2f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}">{html.escape(s)}</text>')
 svg.append(f'<text x="{ox}" y="{oy-28}" font-size="21">{layer} actual / original J12 stays at(40,55)</text>');path(window,'white',1,'#6e7e8c',1)
 for a in n['planes']:
  if a['layer']=='ETCH/'+layer and a.get('filled'):path(plane_from_native(dict(a,holes=a.get('holes')or[])),'#659b7c'if a.get('generated')else'#b685bd',.18)
 for j in range(65):
  x=32+j*.25
  if x>48:break
  if j%2:continue
  a,b=xy((x,18)),xy((x,33));svg.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#b7c6d0" stroke-width="{.7 if j%4 else 1.2}" opacity=".6"/>')
  if not j%4:text((x,33),f'{x:g}',12,offset=(0,-7));text((x,18),f'{x:g}',12,offset=(0,17))
 for j in range(31):
  y=18+j*.5;a,b=xy((32,y)),xy((48,y));svg.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#b7c6d0" stroke-width="{.7 if j%2 else 1.2}" opacity=".6"/>')
  if not j%2:text((32,y),f'{y:g}',12,anchor='end',offset=(-8,4))
 for c in n['placements']:
  if c.get('bodyExtent'):path(box(*c['bodyExtent'][0],*c['bodyExtent'][1]),'none',1,'#8c98a2',.8,'5,4')
 for a in boundary:
  if a['layer'].strip('"')=='BOUNDARY/'+layer:
   holes=parse(a['permanentVoids'])or[]
   if holes:path(polygon_from_vertices(holes[0]),'none',1,'#8d49ae',2,'9,5')
 for a in p.get('reservedAreas',[]):
  if a['id'].startswith('USB')and layer in a['layers']:path(Polygon(a['polygon']),'none',1,'#b99a00',1.2,'7,5')
 for a in n['routes']:
  if a['layer']=='ETCH/'+layer and not a.get('generatedThermal'):path(LineString(a['startEnd']).buffer(a['width']/2,quad_segs=20),color(a['net']),.9)
 for c in n['placements']:
  for a in c['pins']:
   through=pads[a['padstack']]['through']=='t'
   if layer=='BOTTOM'and not through:continue
   bb=a['padBBox'];g=Point(a['xy']).buffer((bb[1][0]-bb[0][0])/2,quad_segs=24)if a['figure']=='CIRCLE'else box(*bb[0],*bb[1]);path(g,color(a['net']),1,'#ffffff',.4)
   if through and float(pads[a['padstack']]['drill'])>0:path(Point(a['xy']).buffer(float(pads[a['padstack']]['drill'])/2,quad_segs=20),'white')
   if c['ref']=='U1'and window.covers(Point(a['xy'])):text(a['xy'],a['number'],11,'#172b3b',offset=(0,3))
 for a in n['vias']:
  if not window.covers(Point(a['xy'])):continue
  pad=next(q for q in a['pads']if q['layer']=='ETCH/'+layer);rad=(pad['bbox'][1][0]-pad['bbox'][0][0])/2;path(Point(a['xy']).buffer(rad,quad_segs=24),color(a['net']),1,'#1d3948',.8);path(Point(a['xy']).buffer(a['drill']/2,quad_segs=20),'white')
 for c in n['placements']:
  if c['ref']=='U1':text((40,27),'U1 / TOP component outline',15);continue
  if window.covers(Point(c['xy'])):text((c['xy'][0],c['xy'][1]+.5),c['ref'],12)
 for i,net in enumerate(nets):
  q=sources[net];path(Point(q).buffer(.38,quad_segs=24),'none',1,color(net),1.7);text((q[0]-.42,q[1]+.32),'S'+str(i+1),12,color(net),anchor='end')
 for i,a in enumerate(feed):
  q=a['xy'];text((q[0]+.25,q[1]-.22),'F'+str(i+1),10,color(a['net']),anchor='start')
svg.append('<text x="70" y="1127" font-size="16">Numbers inside U1 lands are actual pin numbers. S1..S7 identify unconnected source vias; F# identifies existing GND/V3V3 feed vias.</text><text x="70" y="1151" font-size="16">Same XY on both panels (BOTTOM not mirrored); reference/PlaceBound/USB overlays are not candidate routes. All regular pads/vias from native dimensions.</text>')
for i,net in enumerate(nets):
 a=pins[net];q=sources[net];s=f'S{i+1} {net}: via({q[0]:g},{q[1]:g}) / U1.{a["number"]} pad({a["xy"][0]:g},{a["xy"][1]:g})';svg.append(f'<text x="{70+(i%2)*1165}" y="{1190+(i//2)*25}" font-size="17" fill="{color(net)}">{s}</text>')
for i,a in enumerate(feed):
 q=a['xy'];svg.append(f'<text x="{70+(i%4)*575}" y="{1320+(i//4)*24}" font-size="14" fill="{color(a["net"])}">F{i+1} {a["net"]} ({q[0]:g},{q[1]:g}) {a["padstack"]}</text>')
svg.append('</svg>');out=O/'readouts/B019_2L_sourcebank_actual_zoom.svg';out.write_text(''.join(svg));doc=pymupdf.open(out);pdf=pymupdf.open('pdf',doc.convert_to_pdf());page=pdf[0];page.get_pixmap().save(out.with_suffix('.png'))
for i,layer in enumerate(['TOP','BOTTOM']):page.get_pixmap(matrix=pymupdf.Matrix(1.4,1.4),clip=pymupdf.Rect(i*1165,65,(i+1)*1165,1110)).save(O/f'readouts/B019_2L_sourcebank_{layer}_actual_zoom.png')
meta=dict(status='ACTUAL_ONLY_READ_ONLY_VISUAL',boardSHA=w['sha256'],bounds=bounds,sourcePins={k:dict(source=sources[k],U1=pins[k]['number'],padXY=pins[k]['xy'])for k in nets},feedVias=feed,files=[str(out),str(out.with_suffix('.png'))]);(O/'readouts/B019_2L_sourcebank_actual_zoom.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(dict(svg=str(out),png=str(out.with_suffix('.png')),feedCount=len(feed))))
