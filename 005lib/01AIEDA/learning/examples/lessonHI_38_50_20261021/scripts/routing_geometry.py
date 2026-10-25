"""Task-local geometric candidate planning. Native DRC/graph/return checks remain authoritative."""
import pathlib,sys,json,math,csv
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tooling/packages'))
import numpy as np,shapely
from shapely.geometry import box,Point,LineString,Polygon
from shapely.ops import unary_union
sys.path.insert(0,str(ROOT/'engineering_power/scripts'))
from cadence_poly import plane_from_native,polygon_from_vertices
from native_sexpr_data import parse as parse_native_data
LAYERS=('TOP','BOTTOM')
def load(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def padkey(ref,pin):return ref+'.'+str(pin)
class CopperScene:
 def __init__(self,snapshot,networks,rules,policy=None):
  self.snapshot=snapshot;self.networks=networks;self.policy=policy or {};self.rules={(r['net'],r['layer']):r for r in rules['rules']};self.obstacles=[];self.pins={}
  terms={p['key']:p for n in networks['nets'] for c in n['components'] for p in c['terminals']}
  self.board=Polygon([(2,0),(78,0),(80,2),(80,58),(78,60),(2,60),(0,58),(0,2)])
  self.regions=[]
  direct=pathlib.Path(snapshot['readbackDirectory'])/'direct_geometry.tsv'
  self.nativeKeepoutEvidence=str(direct)
  with direct.open(encoding='utf8',newline='') as source:
   for row in csv.DictReader(source,delimiter='\t'):
    layer=row['layer'].strip('"')
    if row['role']!='KEEPOUT' or not layer.startswith('ROUTE KEEPOUT/'):continue
    geometry=polygon_from_vertices(parse_native_data(row['vertices']))
    for target in LAYERS:
     if layer.endswith('/ALL') or layer.endswith('/'+target):self.add(None,target,geometry,'keepout','nativeROUTE_KEEPOUT')

  for r in self.policy.get('regionOverrides',[]):self.regions.append((Polygon(r['polygon']),r))
  for p in snapshot['placements']:
   for a in p['pins']:
    if not a['number']:continue
    key=padkey(p['ref'],a['number']);bb=a['padBBox'];geom=box(bb[0][0],bb[0][1],bb[1][0],bb[1][1]);through=bool(terms.get(key,{}).get('through'))
    self.pins[key]={'key':key,'ref':p['ref'],'pin':a['number'],'net':a['net'],'xy':a['xy'],'geom':geom,'through':through,'componentXY':p['xy']}
    for layer in LAYERS if through else ('TOP',):self.add(a['net'],layer,geom,'thrupin' if through else 'smdpin',key)
  # Real unnumbered mechanical drill data, independently read from native pad definitions.
  # These are NOT the zero-sized regular-copper BBOX of a NULL mechanical pad.
  mechSource=ROOT/f'inventory/mechanical_pins_{snapshot["variant"]}_b012.json'
  self.mechanicalDrillEvidence=str(mechSource)
  mech=load(mechSource)
  for hole in mech['mechanicalPins']:
   if hole['refdes']!='J2':continue # Four mounting bores already have stricter diameter5 teaching zones below.
   actual=next(p for p in snapshot['placements'] if p['ref']==hole['refdes'])
   assert any(x['mechanical'] and x['padstack']==hole['padstack'] and math.dist(x['xy'],hole['xy'])<1e-6 for x in actual['pins']),'Mechanical drill location must match source snapshot'
   assert hole['holeType']=='circle_drill' and hole['drillDiameter']>0
   for layer in LAYERS:self.add(None,layer,Point(hole['xy']).buffer(hole['drillDiameter']/2,quad_segs=24),'hole','nativeMechanical:'+hole['padstack'])
  for a in self.policy.get('componentAnchors',[]):
   key=a['key'];self.pins[key]={'key':key,'ref':'EXPLICIT_ANCHOR','pin':key,'net':a['net'],'xy':a['xy'],'geom':Point(a['xy']),'through':False,'layers':a['layers'],'synthetic':True,'connectedTo':a['connectedTo']}
  for a in snapshot.get('vias',[]):
   for layer in LAYERS:
    pads=[p for p in a.get('pads',[]) if p.get('layer','').removeprefix('ETCH/')==layer]
    radius=max((max(abs(x) for pt in p['bbox'] for x in pt) for p in pads),default=.3)
    self.add(a['net'],layer,Point(a['xy']).buffer(radius,quad_segs=12),'via','native_via')
  for a in snapshot.get('planes',[]):
   layer=a['layer'].removeprefix('ETCH/')
   if layer in LAYERS and a.get('filled') and not a.get('generated'):
    self.add(a['net'],layer,plane_from_native(dict(a,holes=a.get('holes') or [])),'shape','native_static_shape')
  for a in snapshot.get('routes',[]):
   if a.get('generatedThermal'):continue
   layer=a['layer'].removeprefix('ETCH/')
   # Preserve actual GND spokes as conservative obstacles; dynamic shape itself is separately reviewed.
   if layer not in LAYERS:continue
   pts=a['startEnd'];w=a['width']
   if pts and len(pts)>1 and w:self.add(a['net'],layer,LineString(pts).buffer(w/2,quad_segs=10),'line','native_route')
 def add(self,net,layer,geometry,kind,source):self.obstacles.append({'net':net or None,'layer':layer,'geometry':geometry,'kind':kind,'source':source})
 def rule(self,net,layer):return self.rules.get((net,layer),{'spacingClass':'','spacingMM':{},'widthMinMM':.2,'allowEtch':True})
 def space(self,net,other,layer,kind,via=False):
  if kind=='keepout':return 0.0
  a=self.rule(net,layer);b=self.rule(other,layer)
  key=({'smdpin':'smdpin_via','thrupin':'thrupin_via','via':'via_via','line':'via_line','shape':'via_shape','hole':'hole_via'}.get(kind,'via_'+kind) if via else ('line_shape' if kind=='shape' else kind+'_line'))
  value=max(a.get('allSpacingKeys',a['spacingMM']).get(key,.2),b.get('allSpacingKeys',b['spacingMM']).get(key,.2))
  ca=a.get('spacingClass','');cb=b.get('spacingClass','')
  switching=lambda c:'SWITCH' in c
  sensitive=lambda c:any(t in c for t in ('ANALOG','OSCILLATOR','USB_FS'))
  if (switching(ca) and sensitive(cb)) or (switching(cb) and sensitive(ca)):value=max(value,1.)
  if (('USB_FS' in ca and 'DIGITAL_GENERAL' in cb) or ('USB_FS' in cb and 'DIGITAL_GENERAL' in ca)):value=max(value,.5)
  for pair in self.policy.get('netPairSpacing',[]):
   if (net in pair['netsA'] and other in pair['netsB']) or (other in pair['netsA'] and net in pair['netsB']):value=max(value,pair['gap'])
  return float(value)
 def forbidden(self,net,layer,width,via=False,gridMargin=0):
  radius=.3 if via else width/2;out=[]
  for a in self.obstacles:
   if a['layer']!=layer or a['net']==net:continue
   gap=self.space(net,a['net'],layer,a['kind'],via)
   g=a['geometry'].buffer(gap+radius+gridMargin,quad_segs=8)
   if not via:
    for poly,r in self.regions:
     if r.get('layer','TOP')!=layer:continue
     pairs=r.get('netPairs');nets=r.get('nets',[])
     applies=(not pairs and (net in nets or a['net'] in nets)) or (pairs and any(set((net,a['net']))==set(v) for v in pairs))
     if applies and a['kind'] in r.get('kinds',['smdpin','line']):
      local=a['geometry'].buffer(float(r['gap'])+radius+gridMargin,quad_segs=8)
      insideOther=a['geometry'].intersection(poly);outsideOther=a['geometry'].difference(poly)
      outsideFootprint=outsideOther.buffer(gap+radius+gridMargin,quad_segs=8).union(insideOther.buffer(float(r['gap'])+radius+gridMargin,quad_segs=8))
      g=g.intersection(outsideFootprint).difference(poly).union(local.intersection(poly))
   out.append(g)
  for x,y in ((5,5),(75,5),(75,55),(5,55)):out.append(Point(x,y).buffer(2.5+radius+gridMargin,quad_segs=20))
  for a in self.policy.get('reservedAreas',[]):
   if layer not in a.get('layers',['TOP','BOTTOM']) or net in a.get('allowedNets',[]):continue
   out.append(Polygon(a['polygon']).buffer(radius+gridMargin,quad_segs=8))
  if via:
   # Avoid drill-in-SMD-pad even on the same net: no unapproved via-in-pad/fill assumptions.
   out.extend(p['geom'].buffer((.5 if p['through'] else .35)+gridMargin,quad_segs=8) for p in self.pins.values() if not p.get('synthetic'))
  allowed=self.board.buffer(-(.5+radius+gridMargin),quad_segs=8)
  for window in self.policy.get('routeWindows',[]):
   if net in window['nets'] and layer in window.get('layers',LAYERS):allowed=allowed.intersection(Polygon(window['polygon']).buffer(-(radius+gridMargin),quad_segs=8))
  return unary_union(out),allowed
 def masks(self,net,width,step=.05):
  xs=np.arange(0,80+step/2,step);ys=np.arange(0,60+step/2,step);xx,yy=np.meshgrid(xs,ys)
  masks=[];viaMasks=[];margin=step/math.sqrt(2)+.002
  for layer in LAYERS:
   bad,inside=self.forbidden(net,layer,width,False,margin)
   masks.append(shapely.contains_xy(bad,xx,yy)|~shapely.contains_xy(inside,xx,yy))
   bad,inside=self.forbidden(net,layer,width,True,margin)
   viaMasks.append(shapely.contains_xy(bad,xx,yy)|~shapely.contains_xy(inside,xx,yy))
  return masks,viaMasks
 def path_clear(self,net,layer,points,width):
  bad,allowed=self.forbidden(net,layer,width,False,.001)
  line=LineString(points)
  return allowed.covers(line) and not bad.intersects(line)
 def add_operation(self,o):
  if o['type']=='route':
   pts=o['points'];ws=o.get('widths',[o.get('width',.2)]*(len(pts)-1))
   for a,b,w in zip(pts,pts[1:],ws):
    if math.dist(a,b)>1e-8:self.add(o['net'],o['layer'],LineString([a,b]).buffer(w/2,quad_segs=10),'line',o['id'])
  elif o['type']=='via':
   for layer in LAYERS:self.add(o['net'],layer,Point(o['xy']).buffer(o.get('padDiameterMM',.6)/2,quad_segs=12),'via',o['id'])
  elif o['type']=='shape' and not o.get('dynamic') and o['layer'] in LAYERS:
   g=Polygon(o['polygon'])
   for v in o.get('voids',[]):g=g.difference(Polygon(v))
   self.add(o['net'],o['layer'],g,'shape',o['id'])
 def endpoint_port(self,key,width):
  p=self.pins[key];xy=p['xy'];ref=p['ref']
  if p.get('synthetic'):return list(xy),[list(xy)]
  if ref=='U1':
   cx,cy=p['componentXY'];dx,dy=xy[0]-cx,xy[1]-cy
   direction=(math.copysign(1,dx),0) if abs(dx)>abs(dy) else (0,math.copysign(1,dy))
   for length in (1.,.9,.8,1.1,1.2,.7):
    port=[xy[0]+direction[0]*length,xy[1]+direction[1]*length]
    if self.path_clear(p['net'],'TOP',[xy,port],width):return port,[list(xy),port]
   raise ValueError(key+': no clear outward MCU fanout; explicit engineering revision required')
  return list(xy),[list(xy)]