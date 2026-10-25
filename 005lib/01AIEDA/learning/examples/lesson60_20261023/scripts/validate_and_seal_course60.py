from pathlib import Path
import json,hashlib,re,urllib.parse,datetime,zipfile
R=Path(r'D:\001DIY\005lib\01AIEDA');L=R/'learning/examples/lesson60_20261023';S=R/'learning/skills/cadence17-learning'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def load(p):return json.loads(p.read_text(encoding='utf8'))
errors=[];checks=[]
def ck(name,ok,detail=None):
 checks.append({'name':name,'pass':bool(ok),'detail':detail})
 if not ok:errors.append(checks[-1])
for sub in ['sources/source_group_artifact_manifest.json','inventory/artifact_manifest.json']:
 m=load(L/sub);rows=m['files']
 for row in rows:
  key=row.get('root_relative_path',row.get('path'));p=Path(key)
  if not p.is_absolute():p=R/p
  ck(sub+':'+str(key),p.is_file()and sha(p)==row['sha256'].upper())
for pkg,tag in [(L/'package','final03'),(L/'native/R Space','move01')]:
 m=load(pkg/'package_manifest.json')
 for rel,expected in m['files'].items():ck(str(pkg.relative_to(L))+':source:'+rel,sha(pkg/rel)==expected)
 d=load(pkg/f'runs/{tag}/verification.json');ck(str(pkg.relative_to(L))+':accepted_run42',d['status']=='PASS'and d['passCount']==42 and d['totalCount']==42)
 for phase,folder in [('before','build'),('memory','build'),('fresh','fresh')]:
  p=pkg/f'runs/{tag}/{folder}/{phase}_geometry.txt';rows=p.read_text(encoding='ascii').splitlines();n=sum(x.startswith('ETCH_LINE ')for x in rows)
  ck(str(pkg.relative_to(L))+':'+phase+':raw932',n==932,n)
d=load(L/'review/independent_replay_review.json');ck('independent raw semantic review313',d['independent_checks']['pass_count']==313 and d['independent_checks']['fail_count']==0)
d=load(L/'sources/source_validation.json');ck('source learning74',d['pass_count']==74 and d['fail_count']==0)
d=load(L/'review/preflight_forward_fix_validation.json');ck('forward bug fix4',d['passed']and len(d['checks'])==4)
d=load(L/'review/skill_final_validation.json');ck('final skill validator',d['status']=='PASS_FINAL_SKILL_SOURCE_VALIDATION')
jk=R/'learning/examples/lessonJK_51_59_20261022'
ck('priorJK sealed manifest bytes unchanged',sha(jk/'artifact_manifest.json')=='D20CFAA4DE732D53DC980270F941B8EB582776DD294140AD10748DD48AEFC794')
ck('priorJK source BRD unchanged',sha(jk/'native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd')=='471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9')
mapping=load(L/'review/live_to_frozen_snapshot_mapping.json')
for row in mapping['mapping']:
 ck('frozen snapshot:'+row['frozenSnapshot'],sha(L/row['frozenSnapshot'])==row['sha256']and sha(Path(row['liveSourceAtSeal']))==row['sha256'])
docs=[R/'learning/notes/lesson60_20261023.md',L/'README.md',L/'MIGRATION.md']+list((R/'learning/notes').glob('lesson60_*_20261023.md'))
parts=[(p,p.read_text(encoding='utf8'))for p in docs]
parts.append((R/'EDA.md',(R/'EDA.md').read_text(encoding='utf8').split('## 上一轮J/K学习进度')[0]))
idx=R/'\u8bfe\u7a0b\u7d22\u5f15.md';parts.append((idx,'\n'.join(x for x in idx.read_text(encoding='utf8').splitlines()if x.startswith('| 60 |'))))
links=[]
for p,t in parts:
 for target in re.findall(r'\]\(([^)]+)\)',t):
  if re.match(r'^[a-z]+://',target)or target.startswith('#'):continue
  q=Path(urllib.parse.unquote(target.strip('<>').split('#')[0]))
  if not q.is_absolute():q=p.parent/q
  links.append({'source':str(p),'target':str(q),'exists':q.exists()})
  if not q.exists():errors.append({'name':'local link missing','source':str(p),'target':str(q)})
zipreport=load(L/'review/portable_kit_validation.json');archive=L/'eda60-portable-kit.zip';ck('ZIP exact verified bytes',sha(archive)==zipreport['sha256'])
with zipfile.ZipFile(archive)as z:
 ck('ZIP CRC',z.testzip()is None)
 for row in zipreport['files']:ck('ZIP:'+row['path'],hashlib.sha256(z.read(row['path'])).hexdigest().upper()==row['sha256'])
report={'status':'PASS_LESSON60_LOCAL_LEARNING_AND_RELOCATION_PHYSICAL_PC_PENDING'if not errors else'FAIL_RECORD_VALIDATION','createdUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'passedChecks':sum(x['pass']for x in checks),'failed':errors,'localLinks':len(links),'scope':{'twoDirectoriesSamePC':True,'nativeChecksEach':42,'independentSemanticChecks':313,'sourceReadingChecks':74,'secondPhysicalComputerTested':False,'GUICoexistenceTested':False,'GUIControlled':False,'OCRPerformed':False,'newVideoPlaybackCount':0,'productionBoardReleased':False},'frozenSnapshotMapping':'live_to_frozen_snapshot_mapping.json'}
(L/'review/final_record_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
if errors:print(json.dumps({'errors':errors},ensure_ascii=True));raise SystemExit(2)
files=[p for p in L.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.name!='artifact_manifest.json']
# Include the dependency group's artifact_manifest as an explicitly frozen member.
files.append(L/'inventory/artifact_manifest.json')
rows=[{'path':p.relative_to(L).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(set(files))]
manifest={'status':'LESSON60_LOCAL_TRAINING_ARCHIVE_SEALED_NEW_PHYSICAL_PC_PENDING','createdUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Lesson-contained source/outputs/logs/failure history, frozen master-note/skill snapshots, portable kit; no future mutable EDA/index expectations. Accepted native runs are final03/move01 only.','files':rows,'fileCount':len(rows),'totalBytes':sum(x['bytes']for x in rows),'rootRecordChecksPassed':report['passedChecks'],'localLinksValidated':len(links),'scopeLimits':report['scope']}
p=L/'artifact_manifest.json';p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
assert all(sha(L/r['path'])==r['sha256']for r in rows)
print(json.dumps({'checksPass':report['passedChecks'],'links':len(links),'failures':0,'sealedFiles':len(rows),'manifestSHA256':sha(p)}))
