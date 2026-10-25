import pathlib,json,hashlib
h=pathlib.Path(__file__).resolve().parents[1]
left=json.loads((h/'engineering_mcu/plans/GPIO_left_joint_fanout_04.json').read_text(encoding='utf8'))
for v in ('2L','4L'):
 d=json.loads((h/f'plans/ordinary_remote_{v}_v7.json').read_text(encoding='utf8'))
 d['operations']=[o for o in d['operations'] if o['net']!='BOOT0' and o['id'] not in left['replacePendingOperationIds']]+[left['pendingReplacement']]
 d['proofs']=[x for x in d['proofs'] if not any(k.startswith('R28.') for k in (x['from'],x['to']))]
 d['batchId']=f'ordinary_remote_{v}_v8';d['notes']=['Old BOOT0 path removed for relocated R28. BOOT1 source via/TOP neck supplied by left04; only retained targetvia/R29 leg plus explicit BOTTOM replacement. Never execute remote08 alone without left04.']
 (h/f'plans/ordinary_remote_{v}_v8.json').write_text(json.dumps(d,indent=2),encoding='utf8')
 p=json.loads((h/f'plans/ordinary_policy_{v}_v6.json').read_text(encoding='utf8'));p['status']='ACTUAL_SPI_B012_WITH_DECLARED_FUTURE_SOURCES_V11';p['sourceCheckpoint']=f'inventory/checkpoints/SPI_external_{v}_b012';p['pendingOperations']=[];p['pendingDeleteSegments']=[];p['pendingDeleteVias']=[];p['pendingPlacementChanges']=[];p['pendingQuietReworks']=[];p['sourcePlans']=[];p['componentAnchors']=[]
 future=['engineering_mcu/plans/GPIO_north_joint_fanout_02.json','engineering_mcu/plans/GPIO_south_joint_fanout_05.json','engineering_mcu/plans/GPIO_left_joint_fanout_04.json','engineering_power/RIGHT10_source_joint_v2.json',f'plans/ordinary_remote_{v}_v8.json',f'plans/aux_remote_{v}_v9.json',f'plans/CC_entry_{v}_v4.json',f'plans/VBUS_entry_{v}_v3.json',f'plans/USB_aux_returns_{v}_03.json']
 for rel in future:
  fn=h/rel;x=json.loads(fn.read_text(encoding='utf8'));p['sourcePlans'].append({'path':rel,'sha256':hashlib.sha256(fn.read_bytes()).hexdigest()});p['pendingPlacementChanges']+=x.get('placementChanges',[])
  if x.get('oscillatorReferenceRework'):
   rw=x['oscillatorReferenceRework'];p['pendingQuietReworks'].append(rw)
   for area in p['reservedAreas']:
    if area['id']=='HSE_ACTUAL_MOAT_AND_STEM':area['polygon']=rw['applicationGroundVoidPolygon']
   p['noGlobalGroundViaAreas'][0]=rw['applicationGroundVoidPolygon']
  for op in x.get('operations',[])+x.get('commonOperations',[])+x.get('variantOperations',{}).get(v,[]):
   if op['type']=='deleteSegment':p['pendingDeleteSegments'].append(op)
   elif op['type']=='deleteVia':p['pendingDeleteVias'].append(op)
   else:p['pendingOperations'].append(op)
  for net,e in x.get('partialEndpoints',{}).items():
   p['componentAnchors']=[a for a in p['componentAnchors'] if a['net']!=net]
   p['componentAnchors'].append({'key':'ANCHOR_'+net,'net':net,'xy':e['xy'],'layers':[e['layer']],'connectedTo':e['connectedTo'],'replacePinAccess':True})
  for region in x.get('spacingExceptions',[]):
   for layer in region.get('layers',[region.get('layer','TOP')]):
    r={'id':region['id'],'layer':layer,'polygon':region['polygon'],'kinds':['line','via'],'gap':.16}
    if 'nets' in region:r['nets']=region['nets']
    elif 'netsA' in region:r['netPairs']=[[a,b] for a in region['netsA'] for b in region['netsB']]
    if set(region.get('onlyFields',{}).values())=={.2}:r['gap']=.2
    p['regionOverrides'].append(r)
 # Actual terminal groups retain connectivity; explicit service via is an allowed access point.
 p['manualOnlyNets']=[x for x in p['manualOnlyNets'] if x!='NRST']
 p['componentAnchors'].append({'key':'NRST_SERVICE','net':'NRST','xy':[38.7,35.3],'layers':['TOP','BOTTOM'],'connectedTo':'C21.1','replacePinAccess':True})
 p['disabledEndpointKeys']=['U1.7']
 for area in p['reservedAreas']:
  if area['id'].startswith('USB_SHARED_REFERENCE_'):area['allowedNets']+=['PA9_UART_TX','PA10_UART_RX','SWDIO','USB_ATTACH_N']
 p['notes']=['A bounded crossing under shared USB must be inspected in actual copper, not interpreted as continuous reference. No permission for ordinary long parallel routing under USB.','Right10 and left/south private via/spacing scopes still require native rule binding. Long-path geometry is not native approval.']
 (h/f'plans/ordinary_policy_{v}_v11.json').write_text(json.dumps(p,indent=2),encoding='utf8')
p=h/'scripts/plan_signal_paths.py';s=p.read_text(encoding='utf8');s=s.replace("for i,c in enumerate(comps) for a in c for b in connected)","for i,c in enumerate(comps) for a in c for b in connected if a['key'] not in policy.get('disabledEndpointKeys',[]) and b['key'] not in policy.get('disabledEndpointKeys',[]))")
p.write_text(s,encoding='utf8')