import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(P/f'GPIO_PB1_inward_{v}_80_snapshot.json');nw=load(P/f'GPIO_PB1_inward_{v}_80_networks.json');rs=load(P/f'GPIO_PB1_inward_{v}_80_rules.json');p=load(P/f'GPIO_PB1_inward_{v}_80_policy.json')
 for op in load(P/f'GPIO6_{v}_manualPortal81.json')['operations']:
  if op['type']=='via':n['vias'].append(dict(op,pads=[]))
  elif op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):n['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=[a,b],generatedThermal=False,futureCandidate=op['id']))
 for z in p['reservedAreas']:
  if z['id'].startswith('USB_SHARED_REFERENCE_') and v=='4L':z['layers']=[]
 p['routeWindows']=[dict(nets=['GPIO_PB15'],polygon=[[43.5,23],[69,23],[69,57],[43.5,57]])]
 p['bottomCost']=1.05 if v=='4L' else 1.6;p['viaCostMM']=3.0
 for a in p['componentAnchors']:
  if a['net']=='GPIO_PB15':a['xy']=[47.1,23.3];a['layers']=['BOTTOM'];a['qualification']='Explicit conditional portal. Source-prefix is separate; this file only completes east-corridor route.'
 p['candidateQualification']='CONDITIONAL east-corridor extension only; source portal 85 depends on independently verified PB14 source/PB1-L joint changes. Never execute these derived snapshots.'
 for t,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',p)]: (P/f'PB15_east_{v}_86_{t}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
