from pathlib import Path
import json,argparse,math,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=argparse.ArgumentParser();p.add_argument('--plan',required=True);p.add_argument('--variant',choices=['2L','4L'],required=True);p.add_argument('--output',required=True);a=p.parse_args();planpath=Path(a.plan);plan=json.loads(planpath.read_text(encoding='utf-8-sig'));identity=plan.get('inputBoardIdentity') or json.loads((R/f'inventory/current_{a.variant}.json').read_text());snapshot=Path(identity['checkpointDirectory'])/'normalized.json';N=json.loads(snapshot.read_text());board=Path(identity['board']);assert hashlib.sha256(board.read_bytes()).hexdigest().upper()==identity['sha256'];ops=plan['operations'];assert len({o['id'] for o in ops})==len(ops)
def near(a,b):return len(a)==len(b) and all(abs(x-y)<.00011 for x,y in zip(a,b))
def pointsEqual(a,b):return len(a)==len(b) and all(near(x,y) for x,y in zip(a,b))
checks=[];seenTargets=set()
for i,o in enumerate(ops):
 if o['type']=='deleteVia':
  k=('via',o['net'],tuple(o['xy']),o['padstack'].upper());matches=[x for x in N['vias'] if x['net']==o['net'] and near(x['xy'],o['xy']) and x['padstack'].upper()==o['padstack'].upper()]
 elif o['type']=='deleteSegment':
  assert len(o['points'])==2
  k=('segment',o['net'],o['layer'],tuple(sorted(map(tuple,o['points']))),round(o['width'],4));matches=[x for x in N['routes'] if x['net']==o['net'] and x['layer']=='ETCH/'+o['layer'] and abs(x['width']-o['width'])<.00001 and (pointsEqual(x['startEnd'],o['points']) or pointsEqual(list(reversed(x['startEnd'])),o['points']))]
  assert all(not x['generatedThermal'] for x in matches),'Cannot explicitly delete generated thermal line'
 else:continue
 duplicate=k in seenTargets;seenTargets.add(k)
 checks.append({'operation':o['id'],'index':i,'type':o['type'],'normalizedCandidateMatches':len(matches),'duplicateDestructionRequest':duplicate,'pass':len(matches)==1 and not duplicate,'target':o,'nativeDBIDUniqueCheckStillRequired':True})
# Moves are defined once; deleting old vias first preserves exact original net membership.
viaPositions=[i for i,o in enumerate(ops) if o['type']=='deleteVia'];segPositions=[i for i,o in enumerate(ops) if o['type']=='deleteSegment'];nonDeletes=[i for i,o in enumerate(ops) if o['type'] not in ['deleteVia','deleteSegment']]
ordered=not(viaPositions and segPositions) or max(viaPositions)<min(segPositions)
prefix=not(viaPositions or segPositions) or not nonDeletes or max(viaPositions+segPositions)<min(nonDeletes)
poses=plan.get('placementChanges',[]);uniquePoses=len({x['ref'] for x in poses})==len(poses)
out={'status':'PASS_NORMALIZED_CONTROLLED_DELETION_PREFLIGHT_NATIVE_UNIQUENESS_PENDING' if all(x['pass'] for x in checks) and ordered and prefix and uniquePoses else 'FAIL_NORMALIZED_CONTROLLED_DELETION_PREFLIGHT','variant':a.variant,'plan':str(planpath),'planSHA256':hashlib.sha256(planpath.read_bytes()).hexdigest().upper(),'sourceBoard':identity,'inputNormalizedSnapshot':str(snapshot),'checks':checks,'destructiveOperations':len(checks),'allDeleteViasBeforeDeleteSegments':ordered,'deletionsFormInitialPrefix':prefix,'placementSequence':plan.get('placementSequence'),'allPosesUnique':uniquePoses,'scope':['Read-only candidate preflight against immutable normalized actual geometry. No native process launched and no board changed.','Normalizer can collapse same-coordinate duplicate vias; native hiUniqueVia still must verify unique DBID and preserve all other via identities at execution.','Actual native cline topology may split/merge; native exact old segment matching and source SHA before execution remain mandatory.']}
path=Path(a.output);assert path.resolve().is_relative_to(R.resolve());path.write_text(json.dumps(out,indent=2),encoding='utf8');print(out['status'],len(checks))
assert out['status'].startswith('PASS_'),[(c['operation'],c['normalizedCandidateMatches']) for c in checks if not c['pass']]
