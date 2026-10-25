from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');D={'status':'B016_NATIVE_COMPONENT_GRAPH_DERIVED_PHYSICAL_PRESERVATION_CONTRACT_FOR_NEXT_BATCH','scope':'Derived from fresh axlDBGetConnect physicalcomponents; no newnativeprocess run here. Nextbatch must executeevery181physicalpin edge, all272identity, plusnewrouteproofs. Supersedes usingonlyb015172preservation edges while retaining allcritical304/299scopeproofs.','variants':{}}
for v in ['2L','4L']:
 C=R/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING';d=json.loads((C/'networks.json').read_text());N=json.loads((C/'normalized.json').read_text());edges=[]
 for n in d['nets']:
  for c in n['components']:
   pins=[p['key'] for p in c['terminals']]
   edges += [{'from':pins[0],'to':p,'connected':True,'net':n['net']} for p in pins[1:]]
 assert len(edges)==181;D['variants'][v]={'board':d['board'],'sha256':d['sha256'],'actualReadback':d['readback'],'proofs':edges,'count':181,'newFinalTopGroundProofTargets':[{'physicalPin':x['ref']+'.'+p['number'],'xy':p['xy'],'net':'GND','expectedCommonTarget':'C1.2'} for x in N['placements'] for p in x['pins'] if p['net']=='GND' and p['number']],'newFinalTopAllGroundViaProofTargets':[{'xy':p['xy'],'padstack':p['padstack'],'expectedCommonTarget':'C1.2','net':'GND'} for p in N['vias'] if p['net']=='GND'],'nonplatedMechanicalHolesNotGroundConnections':6,'limitation':'Allgroundvia targets positive common check only whenquietanchor ispresent; quietisland negative challenge must separateselectedquiet GND graph after removingoneactualanchor. NotallNPTHholes shouldbegrounded.'}
(R/'review/cumulative_physical_pin_contract_b016.json').write_text(json.dumps(D,indent=2),encoding='utf8');print({v:{'physicalEdges':d['count'],'GNDphysicalPins':len(d['newFinalTopGroundProofTargets']),'GNDvias':len(d['newFinalTopAllGroundViaProofTargets'])} for v,d in D['variants'].items()})