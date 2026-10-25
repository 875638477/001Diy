import pathlib,json,math,hashlib
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1]
def load(f):return json.loads(f.read_text(encoding='utf-8-sig'))
for v in ['2L','4L']:
 B=H/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING';n=load(B/'normalized.json');sourceSHA=load(B/'networks.json').get('sourceSHA256');deps=[str(B/'normalized.json')]
 if v=='4L':
  f=H/'plans/root_south_private_via_spacing_4L_01.json';deps.append(str(f))
  for o in load(f)['operations']:
   if o['type']=='deleteSegment':
    ms=[r for r in n['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and abs(r['width']-o['width'])<1e-6 and r['startEnd'] in [o['points'],list(reversed(o['points']))]];assert len(ms)==1;n['routes'].remove(ms[0])
   elif o['type']=='deleteVia':
    ms=[z for z in n['vias'] if z['net']==o['net'] and math.dist(z['xy'],o['xy'])<1e-6];assert len(ms)==1;n['vias'].remove(ms[0])
   elif o['type']=='route':
    for a,b in zip(o['points'],o['points'][1:]):n['routes'].append(dict(net=o['net'],layer='ETCH/'+o['layer'],width=o['width'],startEnd=[a,b]))
   elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack']))
 selected={'GPIO_PB12':'U1.25','GPIO_PB13':'U1.26','GPIO_PB14':'U1.27','GPIO_PB15':'U1.28'};ops=[];proofs=[];audit=[]
 for net,pin in selected.items():
  routes=[r for r in n['routes'] if r['net']==net and r['layer']=='ETCH/BOTTOM' and not r.get('generatedThermal')];vias=[z for z in n['vias'] if z['net']==net];assert len(vias)==1 and routes,(v,net);via=vias[0];degree={};points={}
  for i,r in enumerate(routes):
   assert len(r['startEnd'])==2
   for p in r['startEnd']:
    k=tuple(round(a,6)for a in p);degree[k]=degree.get(k,0)+1;points[k]=p
   ops.append(dict(type='deleteSegment',id=f'UNUSED_{net}_BOTTOM_{i}',net=net,layer='BOTTOM',width=r['width'],points=r['startEnd'],purpose='Delete explicitly superseded teaching partial tail, preserve TOP MCU-to-source-via copper and source via. This is not a hardware terminal connection.'))
  ends=[k for k,d in degree.items()if d==1];assert len(ends)==2 and all(d<=2 for d in degree.values());assert any(math.dist(p,via['xy'])<1e-5 for p in ends)
  phys=[(c['ref']+'.'+p['number'],p['xy']) for c in n['placements'] for p in c['pins'] if p['number']and p['net']==net];throughOthers=[(key,xy)for key,xy in phys if not key.startswith('U1.')];assert all(min(math.dist(xy,p)for r in routes for p in r['startEnd'])>10 for key,xy in throughOthers)
  top=[r for r in n['routes']if r['net']==net and r['layer']=='ETCH/TOP'];assert top;topHash=hashlib.sha256(json.dumps(top,sort_keys=True).encode()).hexdigest();proofs.append(dict(from_=pin,toVia=dict(xy=via['xy'],net=net,padstack=via['padstack']),mustRemainConnected=True));audit.append(dict(net=net,sourcePin=pin,actualSourceVia=via,oldTailTerminalEnd=[list(k)for k in ends if math.dist(k,via['xy'])>1e-5],tailDegree=dict((str(k),d)for k,d in degree.items()),hardwarePins=phys,topPreservedObjectCount=len(top),topRoutesSHA256=topHash))
 q=dict(status='FROZEN_EXPLICIT_UNUSED_PARTIAL_DELETION_REQUIRES_NATIVE_GRAPH_FILL_DRC',batchId=f'South_UNUSED_BOTTOM_PARTIALS_{v}_01',variant=v,base=str(B),afterMandatorySourceFixes=['root_south_private_via_spacing_4L_01'if v=='4L'else'No southern via shift'],operations=ops,sourceViaProofs=proofs,retireOldVirtualProofTargets={'GPIO_PB12':[35,21.25],'GPIO_PB13':[37.3,19.7],'GPIO_PB14':[35,22.7],'GPIO_PB15':[38.5,22.3]},audit=audit,preconditions=['Only these BOTTOM tail line objects uniquely match; no other same-net BOTTOM copper on source snapshot.','Each tail is one path with degree-one source via and degree-one nonhardware end; all original TOP source copper/source via preserved.','Do not delete any V3V3/GND copper or via. Unlike the erroneous R27 supply classification, the full source topology and all actual hardware terminals were checked.'],expectedOutcome='No hardware terminal contract removed. New proof targets U1 pin to real source via. Complete source-to-header long routes remain pending; refresh fill and prove WEST ground common and cumulative source pins, HSE isolation, no orphan branches.',inputs=[dict(path=f,sha256=hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest())for f in deps])
 f=P/f'South_UNUSED_BOTTOM_PARTIALS_{v}_01.json';f.write_text(json.dumps(q,indent=2),encoding='utf8');print(v,len(ops),hashlib.sha256(f.read_bytes()).hexdigest())
