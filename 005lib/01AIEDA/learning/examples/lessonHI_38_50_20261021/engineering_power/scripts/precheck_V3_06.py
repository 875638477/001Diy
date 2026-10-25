from pathlib import Path
import json,math
R=Path(r'D:\001DIY\005lib\01AIEDA/learning/examples/lessonHI_38_50_20261021/engineering_power')
base=json.loads((R.parent/'inventory/checkpoints/power_4L_b003c/normalized.json').read_text())
files=['interface_CAN_routes_04.json','CAN_local_supply_05.json','V3_peripheral_distribution_06.json']
plans=[json.loads((R/f).read_text()) for f in files]
segments=[];vias=[];pads=[]
for r in base['routes']:
 if r['net'] and r['layer'].startswith('ETCH/') and r['kind']=='line':segments.append(dict(id='BASE_G',net=r['net'],layer=r['layer'].split('/')[1],a=r['startEnd'][0],b=r['startEnd'][1],width=r['width'],candidate=False))
for v in base['vias']:vias.append(dict(id='BASE_G_VIA',net=v['net'],xy=v['xy'],r=.3,candidate=False))
for c in base['placements']:
 for p in c['pins']:
  if p['figure']=='NULL':continue
  b=[list(v) for v in p['padBBox']]
  pads.append(dict(id=c['ref']+'.'+p['number'],net=p['net'],box=b,ref=c['ref'],layer='TOP'))
for fn,plan in zip(files,plans):
 for o in plan['operations']:
  if o['type']=='route':
   for i,(a,b) in enumerate(zip(o['points'],o['points'][1:])):segments.append(dict(id=o['id']+':'+str(i),net=o['net'],layer=o['layer'],a=a,b=b,width=o['widths'][i] if 'widths' in o else o['width'],candidate=True,file=fn))
  if o['type']=='via':vias.append(dict(id=o['id'],net=o['net'],xy=o['xy'],r=.3,candidate=True,file=fn))
def ps(p,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];den=dx*dx+dy*dy
 t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0
 return math.dist(p,[a[0]+t*dx,a[1]+t*dy])
def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def sd(a,b,c,d):
 if orient(a,b,c)*orient(a,b,d)<=0 and orient(c,d,a)*orient(c,d,b)<=0 and max(min(a[0],b[0]),min(c[0],d[0]))<=min(max(a[0],b[0]),max(c[0],d[0]))+1e-9 and max(min(a[1],b[1]),min(c[1],d[1]))<=min(max(a[1],b[1]),max(c[1],d[1]))+1e-9:return 0
 return min(ps(a,c,d),ps(b,c,d),ps(c,a,b),ps(d,a,b))
def rect(p,b):
 return math.hypot(max(b[0][0]-p[0],0,p[0]-b[1][0]),max(b[0][1]-p[1],0,p[1]-b[1][1]))
def sr(a,b,box):
 if rect(a,box)==0 or rect(b,box)==0:return 0
 x0,y0=box[0];x1,y1=box[1];v=[[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
 return min(sd(a,b,c,d) for c,d in zip(v,v[1:]+v[:1]))
def clearance(a,b):
 if a in {'CAN_H','CAN_L'} or b in {'CAN_H','CAN_L'}:return .3 if a in {'V3V3','GND','V5'} or b in {'V3V3','GND','V5'} else .25
 sw={'BUCK_SW','BUCK_BOOT'};sens={'BUCK_FB','OSC_IN','OSC_OUT','XTAL_OUT','ADC0','ADC_IN'}
 power={'GND','V3V3','V5','VIN_RAW','VIN_FUSED','VIN_PROT','VDDA'}
 if (a in sw and b in sens) or (b in sw and a in sens):return 1.0
 if a in sw or b in sw:return .5
 if a in power or b in power or a in sens or b in sens:return .3
 return .2
issues=[];tests=0
def add(kind,a,b,gap,required):
 issues.append(dict(kind=kind,a=a,b=b,geometryLowerBoundGap_mm=round(gap,6),requiredAssumed_mm=required))
for i,s in enumerate(segments):
 if s['candidate']:
  for p in pads:
   if s['layer']!=p['layer'] or s['net']==p['net']:continue
   req=clearance(s['net'],p['net'])
   if s['id'].startswith('STAR_U1_') and p['ref']=='U1':req=.2
   gap=sr(s['a'],s['b'],p['box'])-s['width']/2;tests+=1
   if gap<req-1e-5:add('segment-pad-AABB',s['id'],p['id'],gap,req)
 for t in segments[i+1:]:
  if not(s['candidate'] or t['candidate']) or s['net']==t['net'] or s['layer']!=t['layer']:continue
  req=clearance(s['net'],t['net'])
  if (s['id'].startswith('STAR_U1_') and t['id']=='BASE_G') or (t['id'].startswith('STAR_U1_') and s['id']=='BASE_G'):req=.2
  gap=sd(s['a'],s['b'],t['a'],t['b'])-(s['width']+t['width'])/2;tests+=1
  if gap<req-1e-5:add('segment-segment',s['id'],t['id'],gap,req)
 for v in vias:
  if not(s['candidate'] or v['candidate']) or s['net']==v['net']:continue
  req=clearance(s['net'],v['net']);gap=ps(v['xy'],s['a'],s['b'])-v['r']-s['width']/2;tests+=1
  if gap<req-1e-5:add('segment-via',s['id'],v['id'],gap,req)
for i,v in enumerate(vias):
 if v['candidate']:
  for p in pads:
   gap=rect(v['xy'],p['box'])-v['r'];tests+=1
   if v['net']!=p['net']:
    req=clearance(v['net'],p['net'])
    if gap<req-1e-5:add('via-pad-AABB',v['id'],p['id'],gap,req)
   elif rect(v['xy'],p['box'])<.15:add('unapproved-drill-on-pad',v['id'],p['id'],rect(v['xy'],p['box'])-.15,0)
 for w in vias[i+1:]:
  if not(v['candidate'] or w['candidate']) or v['net']==w['net']:continue
  req=clearance(v['net'],w['net']);gap=math.dist(v['xy'],w['xy'])-v['r']-w['r'];tests+=1
  if gap<req-1e-5:add('via-via',v['id'],w['id'],gap,req)
out={'status':'CLEARANCE_CANDIDATE_NEEDS_NATIVE' if not issues else 'REVIEW_REQUIRED','tests':tests,'issues':issues,'files':files,'scope':'Independent sufficient conservative AABB clearance precheck only, not native rules or planes. FrozenHI4L03c actual snapshot; no pendingplacementchanges. All candidates crosschecked together and against actual G routes/vias; SMT pads only TOP, THT bottom apertures and mechanical keepout not yet included.'}
(R/'readouts/V3_06_CAN_04_05_geometry_precheck.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'status':out['status'],'tests':tests,'issues':issues[:30],'issueCount':len(issues)}))
