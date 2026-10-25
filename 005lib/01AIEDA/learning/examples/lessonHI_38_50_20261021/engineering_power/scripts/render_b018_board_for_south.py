from pathlib import Path
import sys,json,csv,hashlib,math,colorsys,html
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
sys.path[:0]=[str(H/'scripts'),str(O/'scripts'),str(H/'tooling/packages'),r'D:/001DIY/005lib/01AIEDA/learning/tools/pymupdf_1_28_2']
from cadence_poly import plane_from_native,polygon_from_vertices
from native_sexpr_data import parse
from shapely.geometry import Polygon,box,Point,LineString
import pymupdf
cp=H/'inventory/checkpoints/TOP_trial_2L_b018_PRE_ALL69_DRC_PENDING';n=json.loads((cp/'normalized.json').read_text());w=json.loads((cp/'networks.json').read_text());p=json.loads((O/'N49_2L_policy.json').read_text());log=Path(n['readbackDirectory'])
outline=next(csv.DictReader((log/'outline_exact.tsv').open(),delimiter='\t'));outline=polygon_from_vertices(parse(outline['vertices']))
pads={a['name'].strip('"'):a for a in csv.DictReader((log/'padstacks.tsv').open(),delimiter='\t')}
sourceNets=['GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15']
sources={a['net']:a['xy']for a in n['vias']if a['net']in sourceNets};assert len(sources)==7
boundary=list(csv.DictReader((log/'hi_dynamic_boundaries.tsv').open(),delimiter='\t'))
S=20;W=3580;HEIGHT=1620
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HEIGHT}" viewBox="0 0 {W} {HEIGHT}"><rect width="100%" height="100%" fill="#f7fafc"/><style>text{{font-family:Arial,sans-serif}}</style>']
svg.append('<text x="55" y="28" font-size="24">Actual 2L b018 - South7 manual routing map (same TOP-view XY on both panels; BOTTOM is NOT mirrored)</text>')
svg.append('<text x="55" y="52" font-size="16">Source SHA '+w['sha256']+'; 7 GPIO joins pending; whole-board DRC pending. No proposed copper is drawn.</text>')
colors={}
def color(net):
 if net=='GND':return '#487c64'
 if net in ['V3V3','V5_BUCK','VIN_RAW','VIN_FUSED','VIN_PROTECTED','USB_VBUS']:return '#ad5c03'
 if net in sourceNets:return ['#eb3026','#a41783','#304fd4','#dc7e06','#078975','#8b51bb','#688d06'][sourceNets.index(net)]
 if net in ['USB_DP','PA12_SHARED']:return '#cf292c'
 if net in ['USB_DM','PA11_SHARED']:return '#155ad2'
 h=int(hashlib.sha256(str(net).encode()).hexdigest()[:4],16)/65535
 rgb=colorsys.hsv_to_rgb(h,.72,.68);return '#'+''.join(f'{int(v*255):02x}'for v in rgb)
def polys(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return [g]
 return [p for q in getattr(g,'geoms',[])for p in polys(q)]
counts={}
for panel,layer in enumerate(['TOP','BOTTOM']):
 ox=65+panel*1775;oy=110
 def xy(q):return ox+q[0]*S,oy+(60-q[1])*S
 def path(g,fill,opacity=1,stroke='none',sw=0,dash=''):
  out=[]
  for poly in polys(g):
   ds=[]
   for ring in [poly.exterior]+list(poly.interiors):
    pts=[xy(q)for q in ring.coords];ds.append('M '+' L '.join(f'{a:.3f},{b:.3f}'for a,b in pts)+' Z')
   out.append(f'<path d="{" ".join(ds)}" fill="{fill}" fill-opacity="{opacity}" fill-rule="evenodd" stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')
  svg.extend(out)
 def text(q,s,size=13,fill='#172c3e',anchor='middle',dy=0):
  x,y=xy(q);svg.append(f'<text x="{x:.2f}" y="{y+dy:.2f}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" stroke="#ffffff" stroke-width="2.2" paint-order="stroke">{html.escape(s)}</text>')
 svg.append(f'<text x="{ox}" y="{oy-25}" font-size="22">{layer} copper / native pads and drills / 5mm coordinates</text>')
 path(outline,'#ffffff',1,'#1e293b',2)
 # Native actual generated GND is deliberately faint to reveal routing channels.
 for a in n['planes']:
  if a['layer']!='ETCH/'+layer or not a.get('filled'):continue
  g=plane_from_native(dict(a,holes=a.get('holes')or[]));assert abs(g.area-a['area'])<.01
  path(g,'#669c85'if a.get('generated')else'#bb8ec2',.17 if a.get('generated')else .22)
 for x in range(0,81,5):
  a,b=xy((x,0)),xy((x,60));svg.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#bcc8d2" stroke-width="{1.3 if x%10==0 else .7}" opacity=".7"/>');text((x,60),str(x),13,dy=-7);text((x,0),str(x),13,dy=19)
 for y in range(0,61,5):
  a,b=xy((0,y)),xy((80,y));svg.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#bcc8d2" stroke-width="{1.3 if y%10==0 else .7}" opacity=".7"/>');text((-.7,y),str(y),13,anchor='end');text((80.7,y),str(y),13,anchor='start')
 # Component bodies shown as placement context on both panels, not bottom components.
 for c in n['placements']:
  bb=c.get('bodyExtent');
  if bb:path(box(*bb[0],*bb[1]),'none',1,'#87919a',.65,'4,3')
 # Native first permanent void is deliberate HSE keep-apart, not island deletion.
 for a in boundary:
  if a['layer'].strip('"')=='BOUNDARY/'+layer:
   holes=parse(a['permanentVoids'])or[]
   if holes:path(polygon_from_vertices(holes[0]),'none',1,'#8f45b3',2.5,'9,5')
 for area in p.get('reservedAreas',[]):
  if not area['id'].startswith('USB')or layer not in area.get('layers',[]):continue
  path(Polygon(area['polygon']),'none',1,'#cf9d00',1.2,'7,6')
 # Actual trace copper, coloured per net, never an airwire or guessed path.
 count=0
 for a in n['routes']:
  if a['layer']!='ETCH/'+layer or a.get('generatedThermal'):continue
  if a['kind']!='line':raise AssertionError(a['kind'])
  path(LineString(a['startEnd']).buffer(a['width']/2,quad_segs=12),color(a['net']),.85 if a['net']=='GND'else 1);count+=1
 # True native regular-pad dimensions; non-circular figures use actual transformed pad bbox.
 pinCount=0
 for c in n['placements']:
  for a in c['pins']:
   pd=pads[a['padstack']];through=pd['through']=='t'
   if layer=='BOTTOM'and not through:continue
   bb=a['padBBox'];g=box(*bb[0],*bb[1])
   if a['figure']=='CIRCLE':g=Point(a['xy']).buffer((bb[1][0]-bb[0][0])/2,quad_segs=24)
   path(g,color(a['net']),.92,'#ffffff',.45);pinCount+=1
   drill=float(pd['drill'])
   if through and drill>0:path(Point(a['xy']).buffer(drill/2,quad_segs=16),'#ffffff',1,'#3b5263',.45)
 # Stock and private via radius from actual per-layer definition, not global .3 assumption.
 for a in n['vias']:
  ps=next(q for q in a['pads']if q['layer']=='ETCH/'+layer);rr=(ps['bbox'][1][0]-ps['bbox'][0][0])/2
  path(Point(a['xy']).buffer(rr,quad_segs=20),color(a['net']),.95,'#283943',.55)
  path(Point(a['xy']).buffer(a['drill']/2,quad_segs=16),'#ffffff',1)
 for a in n['mechanicalPins']:
  path(Point(a['xy']).buffer(a['drillDiameter']/2,quad_segs=24),'#ffffff',1,'#1e293b',1)
 # Legible component reference only, exact material bodies/heights remain separate.
 for c in n['placements']:
  if c['ref']in ['J12','J13']:continue
  q=c['xy'];text((q[0],q[1]+.72),c['ref'],11 if c['ref'].startswith(('R','C'))else 14)
 # Seven unconnected physical source vias are marked, not connected to destination by fake copper.
 for i,net in enumerate(sourceNets):
  q=sources[net];path(Point(q).buffer(.65,quad_segs=16),'none',1,color(net),2.1)
  text((q[0]-.7,q[1]-.6),'S'+str(i+1),14,color(net),anchor='end')
 for c in n['placements']:
  if c['ref']not in ['J12','J13']:continue
  text((c['xy'][0],58.8),c['ref']+' actual',18)
  for a in c['pins']:
   text((a['xy'][0],57.8),a['number'],12)
   net=a['net'].removeprefix('GPIO_');text((a['xy'][0],56.7),net,10,color(a['net']))
 # Ghost only, no supply or signal proposals implied.
 c=next(a for a in n['placements']if a['ref']=='J12');dx,dy=18-c['xy'][0],9-c['xy'][1];bb=c['bodyExtent'];path(box(bb[0][0]+dx,bb[0][1]+dy,bb[1][0]+dx,bb[1][1]+dy),'none',1,'#de9b1e',2.0,'12,6');text((18,11.1),'J12 SOUTH GHOST (not applied)',15,'#9b6600')
 for a in c['pins']:
  q=(a['xy'][0]+dx,a['xy'][1]+dy);path(Point(q).buffer(.35,quad_segs=12),'none',1,'#de9b1e',1);text((q[0],7.0),a['number'],11,'#9b6600')
 counts[layer]=dict(manualSegments=count,shownPads=pinCount)
svg.append('<text x="65" y="1375" font-size="17">Green faint = actual GND fill; colored solid = actual manual trace/pad copper; circles = true drill/pad sizes; dashed gray = native PlaceBound context.</text><text x="65" y="1401" font-size="17">Purple dashed = actual deliberate HSE void; mustard dashed = USB engineering reference-protection overlay (not copper); orange J12 ghost is a comparison only.</text><text x="65" y="1427" font-size="17">Regular non-circular pads shown from native transformed copper bbox. Signal-only view; mask apertures/assembly clearance and board manufacturing remain separate checks.</text>')
for i,net in enumerate(sourceNets):
 q=sources[net];svg.append(f'<text x="{65+(i%4)*870}" y="{1465+(i//4)*32}" font-size="19" fill="{color(net)}">S{i+1}: {net} actual via ({q[0]:g}, {q[1]:g})</text>')
svg.append('</svg>');out=O/'readouts/B018_2L_wholeboard_South7_manual_map.svg';out.write_text(''.join(svg),encoding='utf8');doc=pymupdf.open(out);pdf=pymupdf.open('pdf',doc.convert_to_pdf());page=pdf[0];pix=page.get_pixmap(matrix=pymupdf.Matrix(1,1));png=out.with_suffix('.png');pix.save(png)
# Independent separate panels support zooming without resizing both at once.
for i,layer in enumerate(['TOP','BOTTOM']):
 rect=pymupdf.Rect(0 if i==0 else 1775,65,(1800 if i==0 else 3580),1350)
 page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3),clip=rect).save(O/f'readouts/B018_2L_{layer}_South7_manual_map.png')
meta=dict(status='READ_ONLY_ACTUAL_NATIVE_COPPER_VISUAL_NOT_ROUTE_OR_REFERENCE_ACCEPTANCE',sourceCheckpoint=str(cp),boardSHA=w['sha256'],counts=counts,sources=sources,files=[str(out),str(png)],wholeDRC=w['summary']['nativeDRC'],remaining=w['summary']['nativeRemainingConnections'],policyOverlaySource=str(O/'N49_2L_policy.json'),scope='Actual native b018 only. J12southghost and USB engineering reservations are overlays, not applied copper. Both panels same top-view XY; PCBbottomnotmirrored.')
(O/'readouts/B018_2L_wholeboard_South7_manual_map.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
