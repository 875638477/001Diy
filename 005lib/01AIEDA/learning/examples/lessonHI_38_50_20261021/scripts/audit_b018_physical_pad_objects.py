from pathlib import Path
import json,hashlib
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
def vk(v):return (v['net'],tuple(round(x,5) for x in v['xy']),v['padstack'])
def pins(s):
 return {p['ref']:{'package':p['package'],'model':p.get('model'),'value':p.get('value'),'xy':p['xy'],'rotation':p['rotation'],'mirrored':p.get('mirrored'),'pins':[{k:a.get(k) for k in ['number','xy','net','padstack','rotation','mechanical','figure','padLocalBBox','padBBox']} for a in p['pins']]} for p in s['placements']}
result={}
for v in ['2L','4L']:
 c0=H/'inventory/checkpoints'/('clearance_'+v+'_b016_DRC_PENDING');c1=H/'inventory/checkpoints'/('TOP_trial_'+v+'_b018_PRE_ALL69_DRC_PENDING')
 a=json.loads((c0/'normalized.json').read_text(encoding='utf8'));b=json.loads((c1/'normalized.json').read_text(encoding='utf8'))
 pa,pb=pins(a),pins(b);assert pa==pb,('Component physicalpad drift',v,[k for k in pa if pa[k]!=pb[k]])
 va={vk(x):x for x in a['vias']};vb={vk(x):x for x in b['vias']};kept=set(va)&set(vb)
 errs=[]
 for k in kept:
  for field in ['drill','pads']:
   if va[k].get(field)!=vb[k].get(field):errs.append({'via':k,'field':field})
 assert not errs,errs
 removed=sorted(set(va)-set(vb));added=sorted(set(vb)-set(va))
 plan=json.loads((H/'engineering_power'/('GPIO_NORTH6_'+v+'_51.json')).read_text(encoding='utf8'))
 expectedRemoved={(op['net'],tuple(op['xy']),op['padstack']) for op in plan['operations'] if op['type']=='deleteVia'}
 expectedAdded={(op['net'],tuple(op['xy']),op['padstack']) for op in plan['operations'] if op['type']=='via'}
 assert set(removed)==expectedRemoved,(v,'unexpectedremoved',removed,expectedRemoved)
 assert set(added)==expectedAdded,(v,'unexpectedadded',added,expectedAdded)
 q0=[p for p in a['planes'] if not p.get('generated') and abs(p['area']-62.895)<.001];q1=[p for p in b['planes'] if not p.get('generated') and abs(p['area']-62.895)<.001];assert q0==q1,(v,'Quietstatic copper drift')
 result[v]={'status':'PASS_PHYSICAL_PAD_IDENTITY_AND_DECLARED_VIA_DELTA_ONLY','source':str(c0),'target':str(c1),'componentCount':len(pa),'physicalNumberedPads':sum(bool(p['number']) for c in pa.values() for p in c['pins']),'allComponentPinPhysicalFieldsExactlyEqual':True,'retainedViaCount':len(kept),'retainedViaDrillAndAllCopperPadLayersExactlyEqual':True,'removedViasExactlyDeclared':removed,'newViasExactlyDeclared':added,'expectedDelta':'+9 -2 = +7 vias','quietStaticCopperExactlyEqual':True,'scope':'Normalized native physical objects, not all raw manufacturing/padstack properties or HF acceptance'}
p=H/'review/b018_physical_pad_object_independent_audit.json';p.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print(json.dumps({v:{k:a[k] for k in ['status','componentCount','physicalNumberedPads','retainedViaCount','expectedDelta','quietStaticCopperExactlyEqual']} for v,a in result.items()}))
