import json,pathlib,math,sys,copy
H=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
sys.path.insert(0,str(H/'scripts'))
from routing_geometry import *
P=H/'engineering_mcu/plans';out=H/'review'
results={}
for v in ['2L','4L']:
 n=load(P/f'GPIO_PB1_inward_{v}_80_snapshot.json');nw=load(P/f'GPIO_PB1_inward_{v}_80_networks.json');rs=load(P/f'GPIO_PB1_inward_{v}_80_rules.json');p=load(P/f'GPIO_PB1_inward_{v}_80_policy.json')
 def apply(o):
  t=o['type']
  if t=='deleteVia':
   a=[z for z in n['vias'] if z['net']==o['net'] and math.dist(z['xy'],o['xy'])<1e-5];assert len(a)==1,(o,a);n['vias'].remove(a[0])
  elif t=='deleteSegment':
   a=[z for z in n['routes'] if not z.get('generatedThermal') and z['net']==o['net'] and z['layer']=='ETCH/'+o['layer'] and abs(z['width']-o['width'])<1e-6 and z['startEnd'] in [o['points'],o['points'][::-1]]];assert len(a)==1,(o,a);n['routes'].remove(a[0])
  elif t=='via':n['vias'].append(dict(o,pads=[]))
  elif t=='route':
   for a,b in zip(o['points'],o['points'][1:]):n['routes'].append(dict(net=o['net'],layer='ETCH/'+o['layer'],width=o['width'],startEnd=[a,b],futureCandidate=o['id'],generatedThermal=False))
  else:raise Exception(o)
 for o in load(P/f'GPIO6_{v}_manualPortal81.json')['operations']:apply(o)
 ops=[]
 def add(o):o['id']='ROOT_PB14_GATE01_'+str(len(ops));ops.append(o)
 def dv(net,xy):add(dict(type='deleteVia',net=net,xy=xy))
 def ds(z):add(dict(type='deleteSegment',net=z['net'],layer=z['layer'].removeprefix('ETCH/'),width=z['width'],points=z['startEnd']))
 def via(net,xy):add(dict(type='via',net=net,xy=xy,padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26))
 def route(net,lay,pts,w):add(dict(type='route',net=net,layer=lay,points=pts,width=w))
 for z in list(n['routes']):
  if z['net']=='USB_ATTACH_N' and not z.get('generatedThermal') and (z['layer']=='ETCH/TOP' or max(q[0] for q in z['startEnd'])<=39.7001):ds(z)
 dv('USB_ATTACH_N',[39,21.2]);dv('GND',[38.8,19.7]);via('USB_ATTACH_N',[39,18.6]);via('GND',[38.45,19.7])
 route('USB_ATTACH_N','TOP',[[39.25,22.75],[39,22.5],[39,21.8]],.16)
 route('USB_ATTACH_N','TOP',[[39,21.8],[39,18.6]],.2)
 route('USB_ATTACH_N','BOTTOM',[[39,18.6],[39.7,18.6]],.2)
 route('GPIO_PB14','BOTTOM',[[38,21.25],[39.25,21.25],[39.45,21.05],[39.45,19.15],[37.9,19.15],[37.9,18.0]],.2)
 for o in ops:
  if o['type'] in ['deleteVia','deleteSegment','via']:apply(o)
 s=CopperScene(n,nw,rs,p)
 for oo in s.obstacles:
  if oo['kind']=='via' and oo['source']=='native_via':
   c=oo['geometry'].centroid
   z=next(z for z in n['vias'] if z['net']==oo['net'] and math.dist(z['xy'],[c.x,c.y])<1e-5)
   radius=max((max(abs(t) for a in pad['bbox'] for t in a) for pad in z.get('pads',[]) if pad['layer'] in ['ETCH/TOP','ETCH/BOTTOM']),default=z.get('padDiameterMM',.3 if 'C060' in z['padstack'] else .26)*2)/2
   oo['geometry']=Point(z['xy']).buffer(radius,quad_segs=64)
 checks=[]
 for o in ops:
  if o['type']=='route':
   clear=s.path_clear(o['net'],o['layer'],o['points'],o['width']);line=LineString(o['points']);hits=[]
   for a in s.obstacles:
    if a['net']==o['net'] or a['layer']!=o['layer']:continue
    gap=line.distance(a['geometry'])-o['width']/2;required=s.space(o['net'],a['net'],o['layer'],a['kind'])
    if gap<required+.01:hits.append(dict(net=a['net'],kind=a['kind'],source=a['source'],bbox=list(a['geometry'].bounds),actualGapMM=gap,globalRequiredMM=required))
   if not clear:
    forbidden,allowed=s.forbidden(o['net'],o['layer'],o['width'],False,.001)
    collision=line.intersection(forbidden);location=collision.wkt[:250]
   else:location=None
   checks.append(dict(id=o['id'],type='route',net=o['net'],clearUnderPolicy=clear,collision=location,nearGlobalRuleHits=hits))
   s.add_operation(o);apply(o)
  elif o['type']=='via':
   hits=[]
   for lay in LAYERS:
    for a in s.obstacles:
     if a['net']==o['net'] or a['layer']!=lay:continue
     gap=Point(o['xy']).distance(a['geometry'])-o['padDiameterMM']/2;required=s.space(o['net'],a['net'],lay,a['kind'],True)
     if gap<required+.01:hits.append(dict(layer=lay,net=a['net'],kind=a['kind'],source=a['source'],bbox=list(a['geometry'].bounds),actualGapMM=gap,globalRequiredMM=required))
   padKeepout=any(z['geom'].distance(Point(o['xy'])) < (.5 if z['through'] else .35) for z in s.pins.values() if not z.get('synthetic'))
   checks.append(dict(id=o['id'],type='via',net=o['net'],clearGlobal=not hits and not padKeepout,padKeepoutHit=padKeepout,hits=hits))
 delta={'status':'DERIVED_GEOMETRY_REVIEW_ONLY_NOT_NATIVE_NOT_RELEASED','basis':'PB1_80 plus GPIO6_81 four connected candidate nets; current actual remains b019','variant':v,'operations':ops,'scope':'ATTACH ordinary GPIO source migration, one ordinary GND via move, PB14 escape only. No V3/USBdata/C14/HSE geometry moved. PI/reference/role and all-net native checks pending.'}
 (out/f'root_PB14_GATE01_{v}_delta.json').write_text(json.dumps(delta,indent=2),encoding='utf8')
 (out/f'root_PB14_GATE01_{v}_snapshot.json').write_text(json.dumps(n,indent=2),encoding='utf8')
 result=dict(variant=v,checks=checks,operationCount=len(ops),status=delta['status'])
 (out/f'root_PB14_GATE01_{v}_checks.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 results[v]=result
 print(v,json.dumps(result))
