from pathlib import Path
import json,hashlib,re,datetime
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
A=Path(r'D:\001DIY\005lib\01AIEDA')
note=A/'learning/notes/lesson29_constraints_20261019.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
# Register every additional primary local API actually used after the initial inventory.
src=R/'source/official_local_sources.json'
lst=json.loads(src.read_text());existing={x['path'].lower() for x in lst}
cds=Path(r'C:\Program0\Cadence\SPB172')
more=['share/pcb/examples/skill/dbcreate/pad.il','share/pcb/examples/skill/DOC/FUNCS/axlDBAddProp.txt','share/pcb/examples/skill/DOC/FUNCS/axlDBCreateComponent.txt','share/pcb/examples/skill/DOC/FUNCS/axlDBAssignNet.txt','share/pcb/examples/skill/DOC/FUNCS/axlPinsOfNet.txt','share/pcb/examples/skill/DOC/FUNCS/axlDBFindByName.txt','share/pcb/examples/skill/DOC/FUNCS/axlDiffPairDBID.txt','doc/algrolibdev/chap5.html','share/pcb/examples/board_design/devices/connector.txt']
for v in more:
 p=cds/v
 if str(p).lower() not in existing:lst.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'kind':'installed_Cadence_17_2_primary_documentation'})
src.write_text(json.dumps(lst,indent=2),encoding='utf8')
links=[]
for target in re.findall(r'\]\(([^)]+)\)',note.read_text(encoding='utf8')):
 if target.startswith(('http:','https:')):continue
 p=(note.parent/target).resolve()
 if p.name=='artifact_manifest.json':continue
 links.append({'target':target,'resolved':str(p),'exists':p.exists()})
assert all(x['exists'] for x in links),[x for x in links if not x['exists']]
assert not '\ufffd' in note.read_text(encoding='utf8')
validation=json.loads((R/'validation.json').read_text())
assert validation['allChecksPass'] and validation['status']=='PASS_NATIVE_CAD_CONSTRAINT_LESSON'
native=R/'native/F29_CONSTRAINTS_v3.brd';assert sha(native)=='6276201EF1750D3A318D901CCF1ADFBB1CA41A4301329CD21E32A0E22B3FA607'
review=A/'learning/examples/lesson29_constraints_20261019_review/review_final.json'
rv=json.loads(review.read_text());assert rv.get('status')=='PASS_INDEPENDENT_REVIEW_LESSON29',rv.get('status')
dependencies=[A/'learning/scripts/de_board_read.il',A/'learning/examples/lesson28_stackup_20261019/scripts/more28.il',A/'learning/examples/lesson28_stackup_20261019/scripts/mechanical28.il',review,A/'learning/notes/lesson29_independent_review_20261019.md']
items=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and p.name!='artifact_manifest.json':
  assert p.resolve().is_relative_to(A)
  items.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)})
rec={'schema':'lesson29_native_artifact_manifest_v1','date':'2026-10-19 Asia/Shanghai','status':'COMPLETE_DECLARED_NATIVE_CAD_SCOPE','root':str(R),'finalBoard':{'path':str(native),'sha256':sha(native)},'notes':{'path':str(note),'sha256':sha(note),'bytes':note.stat().st_size},'validation':{'path':'validation.json','status':validation['status'],'checks':validation['checkCount']},'independentReview':{'path':str(review),'sha256':sha(review),'status':rv['status']},'localLinks':links,'dependencies':[{'path':str(p),'sha256':sha(p)} for p in dependencies],'runtimeLibraryPaths':[str(A/'learning/examples/de_15_26_20261019/library'),str(A/'learning/examples/lesson28_stackup_20261019/native')],'sourceScope':'F28 original unchanged; main profile4layer only; actual USB W/S provisional; no ground plane/complete placement/routing/fabrication release; GUI/DCFX export not performed; automatic internalbem2d errors not used asSI/impedance approval.','fileCount':len(items),'files':items}
(R/'artifact_manifest.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
print(json.dumps({'status':rec['status'],'files':len(items),'noteLinks':len(links),'validation':validation['status'],'checks':validation['checkCount'],'independent':rv['status']},indent=2))
