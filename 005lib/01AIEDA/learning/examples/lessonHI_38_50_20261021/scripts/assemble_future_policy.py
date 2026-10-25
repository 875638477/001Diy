"""Compile auditable explicit future-copper policy; no native PCB writes."""
import sys,pathlib,json,copy,argparse
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from routing_geometry import ROOT,load,LineString
A=argparse.ArgumentParser();A.add_argument('--variant',required=True);A.add_argument('--version',required=True);A.add_argument('--plans',nargs='+',required=True);A.add_argument('--provisional',action='store_true');a=A.parse_args();v=a.variant
p=load(ROOT/f'plans/ordinary_policy_{v}_v14.json')
for k in ['pendingOperations','pendingPlacementChanges','pendingDeleteSegments','pendingDeleteVias','pendingQuietReworks','componentAnchors','pendingConnectivityProofs']:p[k]=[]
p['sourcePlans']=a.plans;p['policyVersion']=a.version;p['status']='PROVISIONAL_FUTURE_GEOMETRY_NOT_NATIVE' if a.provisional else 'FUTURE_COPPER_REQUIRES_NATIVE_VALIDATION'
changes={};anchors={};seen=set()
for f in a.plans:
 d=load(ROOT/f)
 for op in d.get('operations',[])+d.get('commonOperations',[])+d.get('variantOperations',{}).get(v,[]):
  assert op['id'] not in seen,('Duplicate candidate operation',op['id']);seen.add(op['id'])
  if op['type']=='deleteSegment':p['pendingDeleteSegments'].append(op)
  elif op['type']=='deleteVia':p['pendingDeleteVias'].append(op)
  else:p['pendingOperations'].append(op)
 for c in d.get('placementChanges',[]):changes[c['ref']]=c
 if d.get('oscillatorReferenceRework'):p['pendingQuietReworks'].append(d['oscillatorReferenceRework'])
 for net,x in d.get('partialEndpoints',{}).items():
  if not isinstance(x,dict) or 'connectedTo' not in x:continue
  anchors[net]={'key':'ANCHOR_'+net,'net':net,'xy':x['xy'],'layers':x.get('layers',[x.get('layer','BOTTOM')]),'connectedTo':x['connectedTo'],'replacePinAccess':True}
 for q in d.get('proofs',[])+d.get('expectedProofs',[])+d.get('requiredProofs',[]):
  f1=q.get('from',q.get('source'));t=q.get('to',q.get('target'))
  if isinstance(f1,str) and isinstance(t,str) and '.' in f1 and '.' in t and q.get('connected',q.get('expectedConnected',True)):p['pendingConnectivityProofs'].append({'from':f1,'to':t,'connected':True})
p['pendingPlacementChanges']=list(changes.values());p['componentAnchors']=list(anchors.values())+[{'key':'NRST_SERVICE','net':'NRST','xy':[38.7,35.3],'layers':['TOP','BOTTOM'],'connectedTo':'C21.1','replacePinAccess':True}]
p['reservedAreas']=[r for r in p['reservedAreas'] if r['id'] not in ['ADC_REFERENCE_ADC_CAP_SERIES','ADC_REFERENCE_ADC_INPUT']]
for o in p['pendingOperations']:
 if o['id'] in ['NSS01_ADC_SERIES_TO_LOCAL_CAP','NSS01_ADC_INPUT']:
  g=LineString(o['points']).buffer(.65,quad_segs=8);p['reservedAreas'].append({'id':'ADC_REFERENCE_'+o['id'],'polygon':list(map(list,g.exterior.coords)),'layers':['BOTTOM'],'allowedNets':['GND','ADC0','ADC_IN'],'basis':'Protect opposite-layer return below explicitly relocated R32 series/input path; MCU-to-C24 path remains original.'})
out=ROOT/f'plans/ordinary_policy_{v}_v{a.version}.json';out.write_text(json.dumps(p,indent=2,ensure_ascii=False),encoding='utf8');print(out);print('ops',len(p['pendingOperations']),'proofs',len(p['pendingConnectivityProofs']),'anchors',len(p['componentAnchors']))
