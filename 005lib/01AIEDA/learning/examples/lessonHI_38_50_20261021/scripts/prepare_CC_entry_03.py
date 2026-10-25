import json,pathlib
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 d=json.loads((h/f'plans/CC_entry_{v}_v2.json').read_text(encoding='utf8'))
 for o in d['operations']:
  if o['id']=='CC2_ENTRY':o['points']=[[41.75,7.355],[41.75,8.01],[42.1,8.36],[44.4,8.36],[45.5,9.46],[45.5,10.1016]]
  if o['id']=='CC_R3_GND':o['points']=[[35,11.6764],[36.1,11.6764]]
  if o['id']=='CC_R3_GND_V':o['xy']=[36.1,11.6764]
 d['constraintOperations']=[]
 if v=='2L':
  d['constraintOperations']=[{'type':'csetCopy','domain':'spacing','name':'HI_USB_CC1_J2_S_2L','copyFrom':'HI2L_S_CLASSCLASS_10','values':{'smdpin_line':'0.2 MM','line_line':'0.2 MM'}},{'type':'region','id':'HI_USB_CC1_J2_ESCAPE','layer':'TOP','polygon':[[38.35,7.25],[39.6,7.25],[39.6,8.95],[38.35,8.95]],'assignments':[{'domain':'spacing','netClass':'HI2L_USB_FS_S','otherNetClass':'HI2L_USB_AUX_S','cset':'HI_USB_CC1_J2_S_2L'}]}]
 d['notes']=['v1 rejected actual C10 and Q2 overlap; v2 rejected .196985<.20 connector edge gap and GND via touching V3 perimeter, corrected geometry instead of loosening rules.','2L sole new finite J2 CC escape copies full existing Class-Class CSet and lowers line_line/smdpin_line to.20mm here only; outside.50 and DP internal gaps unchanged. Native negative challenge plus actual return/reference review required.']
 (h/f'plans/CC_entry_{v}_v3.json').write_text(json.dumps(d,indent=2),encoding='utf8')
p=h/'scripts/review_candidate_paths.py';s=p.read_text(encoding='utf8').replace("policy=load(ROOT/'plans/ordinary_routing_policy_v0.json');policy['reservedAreas']=[]", "policy=load(ROOT/f'plans/ordinary_policy_{snapshot[\"variant\"]}_v6.json');policy['reservedAreas']=[]")
p.write_text(s,encoding='utf8')