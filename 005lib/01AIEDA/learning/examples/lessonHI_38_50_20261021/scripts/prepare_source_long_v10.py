import pathlib,json,hashlib
h=pathlib.Path(__file__).resolve().parents[1]
paths=['engineering_mcu/plans/GPIO_north_joint_fanout_02.json','engineering_mcu/plans/GPIO_south_joint_fanout_04.json']
for v in ('2L','4L'):
 p=json.loads((h/f'plans/ordinary_policy_{v}_v6.json').read_text(encoding='utf8'));p['status']='FUTURE_JOINT_SOURCE_LONG_PATH_POLICY_V10';p['pendingPlacementChanges']=[]
 # Fresh native b012 already contains SPI. This policy remains anchored to actual b010
 # to represent all edits explicitly and independently before the final merged native source.
 future=paths+[f'engineering_power/SPI_external_{v}_engineered_v'+('10' if v=='2L' else '6')+'.json',f'plans/ordinary_remote_{v}_v7.json',f'plans/aux_remote_{v}_v9.json',f'plans/CC_entry_{v}_v3.json']
 p['sourcePlans']=[]
 for rel in future:
  fn=h/rel;d=json.loads(fn.read_text(encoding='utf8'));p['sourcePlans'].append({'path':rel,'sha256':hashlib.sha256(fn.read_bytes()).hexdigest()})
  p['pendingPlacementChanges']+=d.get('placementChanges',[])
  for op in d.get('operations',[])+d.get('commonOperations',[])+d.get('variantOperations',{}).get(v,[]):
   if op['type']=='deleteSegment':p['pendingDeleteSegments'].append(op)
   elif op['type']=='deleteVia':p.setdefault('pendingDeleteVias',[]).append(op)
   else:
    if op['type']=='via' and '026' in op['padstack']:op['padDiameterMM']=.52;op['drillDiameterMM']=.26
    # R28 has a new right-side pose; old R28-to-header copper not executed.
    if rel.endswith(f'ordinary_remote_{v}_v7.json') and op['net']=='BOOT0':continue
    p['pendingOperations'].append(op)
  for name,endpoint in d.get('partialEndpoints',{}).items():
   key='ANCHOR_'+name
   p.setdefault('componentAnchors',[]).append({'key':key,'net':name,'xy':endpoint['xy'],'layers':[endpoint['layer']],'connectedTo':endpoint['connectedTo'],'replacePinAccess':True})
 # Permit the tiny UART source antipad escape on BOTTOM only as a finite candidate.
 # The resulting USB reference interruption is separately reviewed, not called continuous plane.
 for area in p['reservedAreas']:
  if area['id'].startswith('USB_SHARED_REFERENCE_'):area['allowedNets']+=['PA10_UART_RX','SWDIO']
 (h/f'plans/ordinary_policy_{v}_v10.json').write_text(json.dumps(p,indent=2),encoding='utf8')