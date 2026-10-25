from pathlib import Path
import sys,json,collections,math,hashlib,csv
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
sys.path[:0]=[str(H/'scripts'),str(H/'tooling/packages')]
from routing_geometry import *
def key(a):return(a['net'],a['layer'],round(a['width'],7),tuple(sorted(tuple(round(v,5)for v in p)for p in a['startEnd'])))
def data(p):return json.loads(p.read_text())
def pose(n):return sorted((c['ref'],c['package'],tuple(c['xy']),c['rotation'],tuple(sorted((p['number'],p['net'],tuple(p['xy']),p['padstack'],str(p['padBBox']))for p in c['pins'])))for c in n['placements'])
result=[]
for v in ['2L','4L']:
 a=H/f'inventory/checkpoints/TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING';b=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';old=data(a/'normalized.json');new=data(b/'normalized.json');p=data(O/f'RIGHT_PADENTRY_NORMALIZE_{v}_01.json');checks=[]
 def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail));assert ok,(v,name,detail)
 counter=collections.Counter(key(r)for r in old['routes']if r.get('fixedManualCline')and not r.get('generatedThermal'))
 for op in p['operations']:
  if op['type']=='deleteSegment':
   k=key(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=op['points']));check(op['id']+'_unique',counter[k]==1);counter[k]-=1
  elif op['type']=='route':
   for aa,bb in zip(op['points'],op['points'][1:]):counter[key(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=[aa,bb]))]+=1
 target=collections.Counter(key(r)for r in new['routes']if r.get('fixedManualCline')and not r.get('generatedThermal'));check('exactDeclaredManualRouteCounter',+counter==target)
 check('all80Poses272PadsNetsPreserved',pose(old)==pose(new));check('allViaGeometryDefinitionsPreserved',old['vias']==new['vias']);check('allGeneratedAndQuietCopperGeometryPreserved',old['planes']==new['planes'])
 for net in ['BOOT0','GPIO_PA15','GPIO_PB4','I2C_SCL']:
  gs=[]
  for n in [old,new]:
   z=[box(*q['padBBox'][0],*q['padBBox'][1])for c in n['placements']for q in c['pins']if q['net']==net]
   z+=[LineString(r['startEnd']).buffer(r['width']/2,quad_segs=32)for r in n['routes']if r['net']==net and r['layer']=='ETCH/TOP'and not r.get('generatedThermal')];gs.append(unary_union(z))
  area=gs[0].symmetric_difference(gs[1]).area;check(net+'_actualPadRouteUnionSymmetricDifferenceZero',area<1e-12,area)
 for filename in ['physical_csets.tsv','spacing_csets.tsv','electrical_csets.tsv','group_members.tsv','net_rules.tsv','stackup_full.tsv','films_full.tsv']:
  x=(Path(old['readbackDirectory'])/filename).read_text();y=(Path(new['readbackDirectory'])/filename).read_text();check(filename+'_unchanged',x==y)
 summary=data(b/'networks.json')['summary'];check('7SouthJoinsRetainedAndNoTerminalFree',summary['nativeRemainingConnections']==7 and summary['nativeTerminalFreeBranches']==0)
 result.append(dict(variant=v,boardSHA256=data(b/'networks.json')['sha256'],checks=checks,limits='Read-only b018→b019 representation verification. Native65normal0/strict1.7→actual1.7414/restored2.0 evidence belongs to review/b019_native_report.json; USB and wholeDRC remainpending. Physical exteriorneck1.541421 unchanged.'))
out=O/'readouts/B019_padentry_independent_actual_review.json';out.write_text(json.dumps(dict(status='PASS_INDEPENDENT_PAD_INTERNAL_NORMALIZATION_NATIVE_GEOMETRY_PRESERVATION',boards=result),indent=2)+'\n');print(json.dumps(dict(output=str(out),checks=sum(len(a['checks'])for a in result),passed=True)))
