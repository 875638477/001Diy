from pathlib import Path
import json,copy,hashlib
P=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
def read(p):return json.loads((P/p).read_text(encoding='utf8'))
def write(p,q):
 o=P/p;assert not o.exists(),str(o);o.write_text(json.dumps(q,indent=2),encoding='utf8')
def sha(p):return hashlib.sha256((P/p).read_bytes()).hexdigest().upper()
rejections=[]
for v in ['2L','4L']:
 old=f'plans/root_source_clearance_cleanup_{v}_01.json';q=copy.deepcopy(read(old));removed=[o for o in q['operations'] if o['type']=='deleteSegment' and o['net']=='V3V3'];assert len(removed)==2
 q['operations']=[o for o in q['operations'] if o not in removed];assert len(q['operations'])==6
 q.update(batchId=f'root_source_clearance_cleanup_{v}_02',status='CORRECTED_SOURCE_DELTA_PRESERVE_LIVE_NRST_FEED_REQUIRES_NATIVE',supersedes={'path':old,'sha256':sha(old),'reason':'Two V3 segments were wrongly classified as old R25 deadbranch. Both boards continue from38.1016,47 toR27.1(38.1016,41.3). Preserve all livefeed; native C11.1-R27.1 rejected unsaved edits.'},withdrawnOperations=removed)
 q['measurements'].pop('removedDeadBranchLengthMM',None);q['measurements']['preservedLiveNRSTFeedSegments']=2
 q['proofs'].append({'net':'V3V3','source':'C11.1','target':'R27.1'})
 q['scope']='Only PA10 source geometric clearance plus finite SMT source rules. No V3 deletion. Actual total-branch summary is not proof that a selected feed is unused.'
 out=f'plans/root_source_clearance_cleanup_{v}_02.json';write(out,q)
 rejections.append({'path':old,'sha256':sha(old),'replacement':out,'reason':'REJECTED_LIVE_NRST_FEED_DELETION_BOTH_VARIANTS','permittedUse':'Historical failure evidence only, never replay as accepted cleanup.'})
 # Canonical J2 entry: end normal-width legs at actual pin centers, not only pad bounding box.
 old=f'plans/J2_GND_entry_{v}_01.json';q=copy.deepcopy(read(old));q['batchId']=f'J2_GND_entry_{v}_02';q['status']='CORRECTED_PHYSICAL_PIN_CENTER_ENDPOINTS_REQUIRES_NATIVE'
 for o in q['operations']:
  if o['id']=='J2_LEFT_GND_SHELL_WIDE':assert o['points']==[[35.9,7.355],[35.68,7.355]];o['points'].append([35.68,6.78])
  if o['id']=='J2_RIGHT_GND_SHELL_WIDE':assert o['points']==[[44.1,7.355],[44.32,7.355]];o['points'].append([44.32,6.78])
 q['supersedes']={'path':old,'sha256':sha(old),'reason':'Actual4L creation and GND net identity did not establish SH pin connectivity at old offset endpoint. Explicitly end at original SH1/SH2 physical pin center, preserve .35neck .9mm/normal .6 width and all keepouts; actual native graph remains authoritative.'}
 out=f'plans/J2_GND_entry_{v}_02.json';write(out,q)
 rejections.append({'path':old,'sha256':sha(old),'replacement':out,'reason':'FAILED_NATIVE_PIN_CONNECTIVITY_OFFSET_ENDPOINT','permittedUse':'Historical geometry candidate only; not connectivity acceptance.'})
 # Rebuild service aggregate with only canonical J2 changes.
 old=f'plans/remaining_services_{v}_b015_01.json';s=copy.deepcopy(read(old));s['batchId']=f'remaining_services_{v}_b015_02';s['supersedes']={'path':old,'sha256':sha(old),'reason':'Only J2 canonical wideleg endpoints corrected to actual SH pin centers.'};changes={o['id']:o for o in q['operations']}
 count=0
 for i,o in enumerate(s['operations']):
  if o['id'] in changes:s['operations'][i]=copy.deepcopy(changes[o['id']]);count+=1
 assert count==4
 for inp in s['inputs']:
  if inp['path']==f'plans/J2_GND_entry_{v}_01.json':inp.update(path=out,sha256=sha(out))
 new=f'plans/remaining_services_{v}_b015_02.json';write(new,s)
 rejections.append({'path':old,'sha256':sha(old),'replacement':new,'reason':'SUPERSEDED_J2_PHYSICAL_PIN_ENDPOINT_CORRECTION','permittedUse':'Historical service aggregate; use02 for new execution.'})
 print(v,'sourceops',len(q.get('operations',[])),'remainingops',len(s['operations']))
index=P/'review/deprecated_root_candidates_20261022.json';assert not index.exists();index.write_text(json.dumps({'status':'DO_NOT_REPLAY_AS_ACCEPTED','records':rejections,'retiredGenerator':'scripts/prepare_b015_root_deltas.py','retiredGeneratorReason':'Generates rejected01 cleanup; historical code retained unchanged. Corrected02 generator is prepare_b015_root_deltas_v2.py.'},indent=2),encoding='utf8')
