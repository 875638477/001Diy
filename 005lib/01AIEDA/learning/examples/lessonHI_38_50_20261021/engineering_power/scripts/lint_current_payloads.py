from pathlib import Path
import json,re,math,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');H=R.parent
b=json.loads((H/'inventory/checkpoints/mcu_4L_b006/normalized.json').read_text(encoding='utf-8'))
pins={c['ref']+'.'+p['number']:p for c in b['placements'] for p in c['pins'] if p['number']}
nets={p['net'] for p in pins.values() if p['net']}
files=['STAR_reroute_07b.json','V3_peripheral_distribution_06b.json','interface_CAN_routes_04.json','CAN_local_supply_05.json','ESD_ground_routes_04c.json']
C=[]
def ck(i,x,d=None):C.append(dict(id=i,passed=bool(x),detail=d))
for f in files:
 p=json.loads((R/f).read_text(encoding='utf-8'));ids=[]
 for o in p['operations']:
  ids.append(o['id']);tag=f+'.'+o['id']
  ck(tag+'.knownRealNet',o['net'] in nets,o['net'])
  if o['type'] in ['route','deleteSegment']:
   ck(tag+'.outerLayer',o['layer'] in ['TOP','BOTTOM'])
   ck(tag+'.positiveFiniteCoords',all(len(x)==2 and all(math.isfinite(y) for y in x) for x in o['points']))
   if o['type']=='route':ck(tag+'.segmentWidths',len(o['widths'])==len(o['points'])-1 and all(w>0 for w in o['widths']))
   else:
    hits=[r for r in b['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and abs(r['width']-o['width'])<1e-7 and(r['startEnd']==o['points'] or r['startEnd']==o['points'][::-1])]
    ck(tag+'.uniqueDeleteInMCU6',len(hits)==1)
  elif o['type']=='via':ck(tag+'.approvedVia',o['padstack']=='L28_VIA030_C060')
  else:ck(tag+'.knownOperation',False,o['type'])
  for side in ['from','to']:
   v=o.get(side)
   if isinstance(v,list):v='.'.join(str(t) for t in v)
   if isinstance(v,str) and re.fullmatch(r'[A-Z][A-Z0-9]*\.[A-Za-z0-9_]+',v):
    ck(tag+'.'+side+'.actualTerminal',v in pins,v)
    if v in pins:ck(tag+'.'+side+'.terminalNetMatches',pins[v]['net']==o['net'],[v,pins[v]['net'],o['net']])
 ck(f+'.uniqueOperationIds',len(ids)==len(set(ids)))
out=dict(status='PASS_CURRENT_ENGINEERING_PAYLOAD_SCHEMA_NET_PIN_LINT' if all(c['passed'] for c in C) else'FAIL',results=C,checks=len(C),failed=[c for c in C if not c['passed']],files=files,scope='Semantic schema/69net/pinterminal checks andexact2delete matches only. Not route topology/clearance/native validation. ESD placement prerequisite must stillbeapplied.')
(R/'readouts/current_payload_lint.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=out['status'],checks=len(C),failed=out['failed'])))
