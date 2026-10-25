import json,pathlib,hashlib,copy,math
ROOT=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
def load(p): return json.loads((ROOT/p).read_text(encoding='utf8'))
def save(p,x): (ROOT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def digest(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper()
for v in ['2L','4L']:
 cp=ROOT/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING'
 if not (cp/'normalized.json').exists():continue
 source=load(f'inventory/checkpoints/source_{v}_b015_DRC_PENDING/normalized.json')
 original=[[40.25,22.75],[40.25,22.05],[40.22,22.02],[40.22,21.3],[40,21.08],[40,20.5]]
 new=[[40.25,22.75],[40.25,22.05],[40.205,22.005],[40.205,21.285],[40,21.08],[40,20.5]]
 ops=[]
 for i,(a,b) in enumerate(zip(original,original[1:])):
  matches=[r for r in source['routes'] if r['net']=='PA10_UART_RX' and r['layer']=='ETCH/TOP' and abs(r['width']-.16)<1e-8 and (r['startEnd']==[a,b] or r['startEnd']==[b,a])]
  assert len(matches)==1,(v,a,b,len(matches))
  ops.append(dict(type='deleteSegment',id=f'SOUTH_RX_CLEARANCE_RIP_{i}',net='PA10_UART_RX',layer='TOP',points=[a,b],width=.16))
 ops.append(dict(type='route',id='SOUTH_RX_CLEARANCE_REPLACE',net='PA10_UART_RX',layer='TOP',points=new,width=.16,purpose='Move source neck .015mm left to preserve actual USB line-line .2mm rule; source MCU pad and existing private via unchanged.'))
 for i,pts in enumerate([[[31.11,55],[31.11,47]],[[31.11,47],[38.1016,47]]]):
  matches=[r for r in source['routes'] if r['net']=='V3V3' and r['layer']=='ETCH/TOP' and abs(r['width']-.6)<1e-8 and (r['startEnd']==pts or r['startEnd']==list(reversed(pts)))]
  assert len(matches)==1,(v,pts,len(matches))
  ops.append(dict(type='deleteSegment',id=f'NSS_OLD_R25_V3_BRANCH_CLEANUP_{i}',net='V3V3',layer='TOP',points=pts,width=.6,purpose='Remove old R25-only supply dead branch after actual R25 relocation; preserve live J12 supply from north and main y58.2 bus.'))
 delta=dict(batchId=f'root_source_clearance_cleanup_{v}_01',variant=v,status='EXPLICIT_ACTUAL_B015_DELTA_REQUIRES_NATIVE',sourceCheckpoint=str(cp),sourceExpectedSHA256=digest(f'native_candidates/HI_{v}_source_b015_DRC_PENDING.brd'),operations=ops,proofs=[dict(net='PA10_UART_RX',source='U1.31',targetAlias='SOUTH_SOURCE_31_VIA'),dict(net='V3V3',source='J12.1',target='C9.1'),dict(net='V3V3',source='R25.1',target='C9.1')],spacingExceptions=[dict(id='HI_RX_USB_SOURCE_SMD_ONLY',layer='TOP',polygon=[[39.65,20],[40.55,20],[40.55,23.4],[39.65,23.4]],netsA=['PA10_UART_RX'],netsB=['PA11_SHARED','PA12_SHARED'],onlyFields={'smdpin_line':.2},basis='Local .5mm pitch MCU source escape; native cache reported .27/.284/.3216 vs inherited USB-other .5. Existing line-line/via-line .2 retained; outside finite area .5 unchanged. Verify exact effective native overlap, scoped stricter challenge and full DRC. No reduction of source line-line .2; geometric .19 fixed by moving source copper.')],measurements={'oldUSBLineGapMM':.19,'newUSBVerticalLineGapMM':.205,'removedDeadBranchLengthMM':14.9916,'newSourceNeckCenterlineMM':sum(math.dist(a,b) for a,b in zip(new,new[1:]))},scope='Actual manual geometry correction and dead branch cleanup. No final native spacing/return/whole-board DRC claim.')
 save(f'plans/root_source_clearance_cleanup_{v}_01.json',delta)
 # Aggregate remaining services from canonical reviewed candidates; preserve each input digest.
 files=[f'plans/root_remaining_{v}_v19.json',f'engineering_power/UART_RX_receiver_bridge_{v}_03.json',f'engineering_power/remaining_returns_{v}_v19_02.json',f'plans/J2_GND_entry_{v}_01.json']
 if v=='2L':files.append('engineering_power/CAN_RXD_2L_engineered_07.json')
 agg=dict(batchId=f'remaining_services_{v}_b015_01',variant=v,status='REBASED_TO_ACTUAL_B015_REQUIRES_NATIVE_AND_REFERENCE_REVIEW',sourceCheckpoint=str(cp),sourceExpectedSHA256=delta['sourceExpectedSHA256'],inputs=[{'path':p,'sha256':digest(p)} for p in files],operations=[],placementChanges=[],proofs=[],rebaseDecisions=[])
 ids=set()
 for p in files:
  q=load(p)
  for op in q.get('operations',[]):
   if v=='2L' and p.endswith('root_remaining_2L_v19.json') and op['id']=='HI_2L_VBUS_PRESENT_N_1_R1':
    agg['rebaseDecisions'].append('Exclude old pending VBUS BOTTOM operation exactly once; replace using CAN07 canonical payload.');continue
   assert op['id'] not in ids,(p,op['id']);ids.add(op['id']);agg['operations'].append(copy.deepcopy(op))
  agg['placementChanges']+=copy.deepcopy(q.get('placementChanges',[]))
  for pr in q.get('proofs',[]):
   r=copy.deepcopy(pr)
   if 'targetAlias' in r:r['toAlias']=r.pop('targetAlias')
   agg['proofs'].append(r)
  if 'returnReview' in q:
   for o in q.get('operations',[]):
    if o['type']=='via' and o['net']=='GND':agg['proofs'].append(dict(net='GND',source='U1.35',toAlias=o['id']))
 for op in agg['operations']:
  if op['type']=='deleteSegment':
   matches=[r for r in source['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-7 and (r['startEnd']==op['points'] or r['startEnd']==list(reversed(op['points'])))];assert len(matches)==1,(v,op,len(matches))
  elif op['type']=='deleteVia':
   matches=[r for r in source['vias'] if r['net']==op['net'] and math.dist(r['xy'],op['xy'])<1e-7 and r['padstack']==op['padstack']];assert len(matches)==1,(v,op,len(matches))
 agg['rebaseDecisions']+=['Actual b015 is service18: apply UART03 exact two-segment PA10 ripup and R17 90deg relocation, do not replay SOURCE.','Source-only operations and placement metadata from old root_remaining19 are already actual b015; no source plans replayed.','Current b014 aliases remain qualified baseline; source b015 has cached violations and incomplete wholeboard DRC.','Return-via historical frozen-plane coverage does not certify new actual fill/reference; final HSE negative and actual-common-ground proof required.']
 save(f'plans/remaining_services_{v}_b015_01.json',agg)
 print(v,'rootDeltaOps',len(ops),'remainingOps',len(agg['operations']),'proofs',len(agg['proofs']))
