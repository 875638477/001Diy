from pathlib import Path
import json,hashlib,argparse,re
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
a=argparse.ArgumentParser();a.add_argument('--variant',choices=['2L','4L'],required=True);a.add_argument('--output',required=True);a.add_argument('--extra-plan',action='append',default=[]);a=a.parse_args();v=a.variant
source=json.loads((R/f'inventory/current_{v}.json').read_text());C=Path(source['checkpointDirectory']);N=json.loads((C/'normalized.json').read_text());D=json.loads((C/'networks.json').read_text());realNets={n['net'] for n in D['nets']};terminals={};contracts=[]
for c in N['placements']:
 for p in c['pins']:
  number=p['number']
  if p.get('mechanical') or not number:continue
  key=c['ref']+'.'+str(number);assert key not in terminals
  net=p['net'] if p['net'] in realNets else None
  rec={'key':key,'ref':c['ref'],'pin':str(number),'net':net,'padstack':p['padstack']};terminals[key]=rec;contracts.append(rec)
assert len(contracts)==272 and sum(r['net'] is not None for r in contracts)==266

def proof(a,b,prov,net=None):
 assert a in terminals and b in terminals,(a,b,prov)
 assert terminals[a]['net']==terminals[b]['net'] is not None,(a,b,terminals[a]['net'],terminals[b]['net'])
 if net is not None:assert terminals[a]['net']==net
 return {'from':a,'to':b,'connected':True,'net':terminals[a]['net'],'provenance':prov}
preservation=[];final=[]
for n in D['nets']:
 for comp in n['components']:
  tt=sorted(t['key'] for t in comp['terminals'])
  for t in tt[1:]:preservation.append(proof(tt[0],t,{'type':'mustPreserveCurrentNativePhysicalComponent','baselineComponent':comp['id'],'net':n['net'],'baselineBoardSHA':source['sha256']},n['net']))
 tt=sorted(t['key'] for comp in n['components'] for t in comp['terminals'])
 for t in tt[1:]:final.append(proof(tt[0],t,{'type':'requiredOnlyAtFinalCompleteRouting','net':n['net']},n['net']))
assert len(preservation)==266-69-int(D['summary']['nativeRemainingConnections'])
assert len(final)==197
extras=[];skipped=[];sources=[]
def term(x):
 if isinstance(x,dict):return str(x.get('ref'))+'.'+str(x.get('pin'))
 if isinstance(x,list) and len(x)==2:return str(x[0])+'.'+str(x[1])
 return x
for name in a.extra_plan:
 p=Path(name);assert p.resolve().is_relative_to(R.resolve());d=json.loads(p.read_text(encoding='utf-8-sig'));sources.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()})
 rows=[]
 for fld in ['proofs','expectedProofs','requiredProofs','returnProofs']:
  rows += [(fld,x) for x in d.get(fld,[])]
 rows += [('routeEndpoints',o) for o in d.get('operations',[]) if o.get('from') and o.get('to')]
 for fld,row in rows:
  x,y=term(row.get('from',row.get('source'))),term(row.get('to',row.get('target')))
  if x not in terminals or y not in terminals:
   skipped.append({'source':str(p),'field':fld,'row':row,'reason':'Not two stable physical component pins; retain separate plan-specific alias/via/XY native proofs, not part of this cumulative physical-pin contract.'});continue
  assert row.get('connected',row.get('expectedConnected',True)) is True
  extras.append(proof(x,y,{'type':'explicitCriticalPhysicalPinPair','source':str(p),'field':fld},row.get('net')))
merged={}
for row in preservation+extras:
 key=tuple(sorted([row['from'],row['to']]))
 if key not in merged:merged[key]={**row,'provenance':[row['provenance']]}
 else:merged[key]['provenance'].append(row['provenance'])
report={'status':'PREPARED_CUMULATIVE_PHYSICAL_PIN_CONTRACT_NOT_NATIVE_EXECUTED','variant':v,'sourceBoard':source,'baselineInputEvidence':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()} for p in [C/'networks.json',C/'normalized.json']],'extraPlanSources':sources,'terminalContract':contracts,'baselineComponentPreservationProofs':preservation,'explicitCriticalPinProofs':extras,'cumulativePreservationAndCriticalPinProofs':list(merged.values()),'finalCompleteAll69NetPhysicalPinProofs':final,'nonPhysicalPlanProofsKeptSeparate':skipped,'counts':{'physicalLogicalPins':272,'nettedPhysicalPins':266,'ncPseudoNetPins':6,'baselinePositivePinEdges':len(preservation),'explicitCriticalPinProofs':len(extras),'deduplicatedCumulativeProofs':len(merged),'finalAllNetPinEdges':197},'scope':['Stable refdes.pin endpoints intentionally survive all placement/route/via/shape rework. No old XY alias is treated as durable identity.','Current native-connected components become must-preserve physical-pin graphs; new critical pinpairs may be added. New merges are allowed.','Final197 edge contract is for fully routed release only and is not asserted against partial intermediate boards.','Net/padstack identity for all272 physical packagepins must also match; electrical NC pseudo nets are explicitly kept outside69realnets.','Actual return-via endpoints, HSE single-anchor negative, native branch audit/DRC/real reference coverage remain separate required evidence.']}
out=Path(a.output);assert out.resolve().is_relative_to(R.resolve());out.write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report['counts'],indent=2))
