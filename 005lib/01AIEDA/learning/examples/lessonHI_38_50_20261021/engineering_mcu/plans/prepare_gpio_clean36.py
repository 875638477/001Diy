import pathlib,json,sys,math,copy,hashlib
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
from shapely import affinity
for v in ['2L','4L']:
 B=H/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING';n=load(B/'normalized.json');nw=load(B/'networks.json');rs=load(B/'base_net_rules.json');pol=load(P/f'GPIO_future_{v}_32_policy.json');assert nw.get('nativeLog',nw.get('readback'))==n['readbackDirectory'];sources=[]
 fs=[P/'GPIO_LEFT_NORTH_spacing_fix_09.json',H/f'engineering_power/RIGHT_actual_clearance_{v}_01.json',H/f'plans/root_source_clearance_cleanup_{v}_01.json',H/f'plans/remaining_services_{v}_b015_01.json']
 if v=='4L':fs.append(H/'plans/root_south_private_via_spacing_4L_01.json')
 fs.append(H/f'engineering_power/J12_south_supply_study_{v}_01.json')
 for f in fs:
  q=load(f);sources.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
  for ch in q.get('placementChanges',[]):
   c=next(c for c in n['placements'] if c['ref']==ch['ref']);cx,cy=c['xy'];rot=ch['rotation']-c['rotation'];dx,dy=ch['xy'][0]-cx,ch['xy'][1]-cy
   def tr(p):pp=affinity.translate(affinity.rotate(Point(p),rot,origin=[cx,cy]),dx,dy);return [round(pp.x,8),round(pp.y,8)]
   for pin in c['pins']:
    pin['xy']=tr(pin['xy']);g=affinity.translate(affinity.rotate(box(*pin['padBBox'][0],*pin['padBBox'][1]),rot,origin=[cx,cy]),dx,dy);b=g.bounds;pin['padBBox']=[list(b[:2]),list(b[2:])]
   for k in ['bodyExtent','bbox']:
    g=affinity.translate(affinity.rotate(box(*c[k][0],*c[k][1]),rot,origin=[cx,cy]),dx,dy);b=g.bounds;c[k]=[list(b[:2]),list(b[2:])]
   c['xy']=ch['xy'];c['rotation']=ch['rotation']
  for op in q['operations']:
   if op['type']=='deleteSegment':
    ms=[r for r in n['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-6 and r['startEnd'] in [op['points'],list(reversed(op['points']))]];assert len(ms)==1,(v,f.name,op,len(ms));n['routes'].remove(ms[0])
   elif op['type']=='deleteVia':
    ms=[z for z in n['vias'] if z['net']==op['net'] and math.dist(z['xy'],op['xy'])<1e-6];assert len(ms)==1,(v,f.name,op,len(ms));n['vias'].remove(ms[0])
   elif op['type']=='via':n['vias'].append(dict(net=op['net'],xy=op['xy'],padstack=op['padstack'],padDiameterMM=op.get('padDiameterMM',.52 if '026_C052' in op['padstack'].upper() else .6),drillDiameterMM=op.get('drillDiameterMM',.26 if '026_C052' in op['padstack'].upper() else .3),futureCandidate=op['id']))
   elif op['type']=='route':
    for a,b,w in zip(op['points'],op['points'][1:],op.get('widths',[op.get('width',.2)]*(len(op['points'])-1))):
     if a!=b:n['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],width=w,startEnd=[a,b],kind='line',generatedThermal=False,fixedManualCline=True,futureCandidate=op['id']))
   else:raise ValueError(op)
 for a in pol['componentAnchors']:
  ep=load(P/'GPIO_LEFT_NORTH_spacing_fix_09.json')['partialEndpoints'].get(a['net'])
  if ep:a['xy']=ep['xy']
 pinxy={c['ref']+'.'+p['number']:p['xy'] for c in n['placements'] for p in c['pins'] if p['number']}
 for nn in nw['nets']:
  for cc in nn['components']:
   for t in cc['terminals']:
    if t['key'] in pinxy:t['xy']=pinxy[t['key']]
 for q in pol['routeWindows']:
  if any(z.startswith('GPIO_') for z in q['nets']):q['polygon']=[[7,7],[70,7],[70,57],[7,57]]
 pol['pendingOperations']=[];pol['pendingDeleteSegments']=[];pol['bottomCost']=1.15;pol['viaCostMM']=2.;pol['derivedInputs']=sources;n['candidateInputs']=sources;n['status']='ACTUAL_B015_PLUS_EXPLICIT_ALLFIX_AND_J12_SOUTH_STUDY_NOT_NATIVE'
 for typ,q in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_future_{v}_36_{typ}.json').write_text(json.dumps(q,indent=2),encoding='utf8')
 print(v,len(n['routes']),len(n['vias']),len(sources))
