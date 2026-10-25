from pathlib import Path
import json,math,hashlib
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
for v in ['2L','4L']:
 q=json.loads((O/f'GPIO_NORTH6_{v}_51.json').read_text());n=json.loads((H/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING/normalized.json').read_text());nets={a['net'] for a in q['operations'] if a['type']=='route'};nets.discard('GND');deleted=[a for a in q['operations'] if a['type']=='deleteSegment'];retained={nn:0.0 for nn in nets};segments={nn:0 for nn in nets}
 for a in n['routes']:
  if a['net'] not in nets or a.get('generatedThermal'):continue
  if any(a['net']==b['net'] and a['layer']=='ETCH/'+b['layer'] and abs(a['width']-b['width'])<1e-6 and a['startEnd'] in [b['points'],list(reversed(b['points']))] for b in deleted):continue
  retained[a['net']]+=sum(math.dist(x,y) for x,y in zip(a['startEnd'],a['startEnd'][1:]));segments[a['net']]+=1
 q['completePlanarRouteLengthsMM']={nn:dict(retainedSourceMM=retained[nn],newRouteMM=q['newRouteLengthsMM'][nn],completePlanarMM=retained[nn]+q['newRouteLengthsMM'][nn],excludes='verticalvia barrel distance, delay, package bondwire and external cable; notmatched-length or SI certification') for nn in sorted(nets)}
 q['nativeContract']=dict(only39Operations=True,ruleChanges=[],normalSignalWidthMM=.2,newPrivateVias=False,newApprovedViaRegions=False,stockPTH='L28_VIA030_C060',orderedDeleteViasBeforeSegments=True,realU1ToJ11Proofs=6,newCommonGNDProofs=4,finalGNDRefillAndHSEUniqueAnchorNegative=True,allPriorProofsAndPinIdentityMustRemain=True,noGlobalOrInnerEtchChanges=True,finalWholeBoardFreshDRCStillRequired=True)
 q['status']='FROZEN_COMPLETE_6_NET_CANDIDATE_ACTUAL_B016_NATIVE_GRAPH_AND_FINAL_REFERENCE_PENDING';p=O/f'GPIO_NORTH6_{v}_51.json';p.write_text(json.dumps(q,indent=2));print(v,hashlib.sha256(p.read_bytes()).hexdigest().upper(),q['sourceExpectedSHA256'],q['completePlanarRouteLengthsMM'])