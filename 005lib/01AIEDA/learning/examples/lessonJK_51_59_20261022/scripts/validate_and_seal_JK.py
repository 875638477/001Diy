from pathlib import Path
import json,hashlib,re,datetime,urllib.parse
R=Path(r'D:\001DIY\005lib\01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022'
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
manifests=[J/'native/native56_artifact_manifest.json',J/'audits/j51_54_artifact_manifest.json',J/'audits/j55_57_artifact_manifest.json',J/'audits/jk_release_gate_manifest.json',J/'review/independent_K58/artifact_manifest.json',J/'review/independent_newstack/artifact_manifest.json',J/'audits/jk_newstack4L_identity_manifest.json']
def entries(a):
 if isinstance(a,dict):
  if isinstance(a.get('path'),str) and isinstance(a.get('sha256'),str):yield a
  else:
   for v in a.values():yield from entries(v)
 elif isinstance(a,list):
  for v in a:yield from entries(v)
cache={};failures=[];exceptions=[];groups=[]
for manifest in manifests:
 m=json.loads(manifest.read_text(encoding='utf8'));seen=set();matched=0;snapshots=0;count=0
 for row in entries(m):
  p=Path(row['path'])
  if not p.is_absolute():
   p=next((q for q in [J/p,manifest.parent/p,R/p]if q.exists()),J/p)
  expected=row['sha256'].upper();key=(str(p),expected)
  if key in seen:continue
  seen.add(key);count+=1
  if not p.exists():failures.append({'manifest':str(manifest),'path':str(p),'reason':'MISSING'});continue
  actual=cache.setdefault(str(p),sha(p)) if str(p)not in cache else cache[str(p)]
  if actual==expected:matched+=1
  elif p==J/'review/user_four_layer_function_rule_20261022.json' and expected=='121D022097B029EBB16198EC5A0726D4419DE89D30988A7C87244EFC1CCC8CD6':
   snap=J/'backups/layer_function_policy_before_actual_application_20261022.json'
   if sha(snap)!=expected:failures.append({'path':str(snap),'reason':'HISTORICAL_SNAPSHOT_MISMATCH'})
   else:
    snapshots+=1;exceptions.append({'manifest':str(manifest),'mutablePath':str(p),'oldExpectedSHA256':expected,'currentSHA256':actual,'matchingHistoricalByteSnapshot':str(snap),'mapping':str(J/'review/layer_policy_history_mapping.json')})
  else:failures.append({'manifest':str(manifest),'path':str(p),'expected':expected,'actual':actual,'reason':'UNEXPECTED_HASH_CHANGE'})
 groups.append({'manifest':str(manifest),'sha256':sha(manifest),'uniqueSHAEntries':count,'matchedCurrentBytes':matched,'matchedHistoricalSnapshotForIntentionalProgressUpdate':snapshots})
accepted=[]
for rel,counts in [('review/independent_CAM/summary.json',{'2L':77,'4L':85}),('review/independent_CAM_J55/summary.json',{'2L':77,'4L':85}),('review/companion_and_J55_CAM/summary.json',{'2L':22,'4L':24}),('review/independent_CAM_NEWSTACK/summary.json',{'4L':85})]:
 d=json.loads((J/rel).read_text(encoding='utf8'))
 for v,n in counts.items():
  x=d[v];ok=x.get('passed')==n and not x.get('failed',[]) and not x.get('failures',[]) and x.get('visualReviewed') is True
  accepted.append({'report':str(J/rel),'variant':v,'expectedPassCount':n,'passed':ok})
for rel,countkey,expected in [('audits/j55_corrected_independent_summary.json','checks',1644),('review/independent_K58/review.json','checkCount',1453),('review/independent_newstack/review.json','checkCount',73),('audits/jk_newstack4L_assembly_identity_review.json','checks',929)]:
 d=json.loads((J/rel).read_text(encoding='utf8'));accepted.append({'report':str(J/rel),'expectedPassCount':expected,'passed':d.get(countkey)==expected and not d.get('failed')})
d=json.loads((J/'review/independent_CAM_NEWSTACK/geometry_delta.json').read_text(encoding='utf8'));accepted.append({'report':'newstack actual CAM delta','expectedPassCount':34,'passed':d['passed']==34 and not d['failures']})
for check in accepted:
 if not check['passed']:failures.append({'reason':'ACCEPTED_REPORT_NOT_PASS','detail':check})
docs=[R/'learning/notes/lessonJK_51_59_20261022.md',R/'learning/notes/lessonJK_independent56_20261022.md',R/'learning/notes/lessonJK_59_bench_20261022.md',J/'README.md',J/'learning_plan.md']
textsections=[(p,p.read_text(encoding='utf8'))for p in docs]
textsections.append((R/'EDA.md',(R/'EDA.md').read_text(encoding='utf8').split('### 学习目标与执行方式')[0]))
textsections.append((R/'课程索引.md','\n'.join(l for l in (R/'课程索引.md').read_text(encoding='utf8').splitlines()if re.match(r'^\| (?:5[1-9]) \|',l))))
links=[]
for p,text in textsections:
 for target in re.findall(r'\]\(([^)]+)\)',text):
  if target.startswith(('http:','https:','#','app:','plugin:')):continue
  target=urllib.parse.unquote(target.strip('<>').split('#')[0]);q=Path(target)
  if not q.is_absolute():q=p.parent/q
  links.append({'source':str(p),'target':str(q),'exists':q.exists()})
  if not q.exists():failures.append({'reason':'LOCAL_LINK_MISSING','source':str(p),'target':str(q)})
qa={'status':'THIS_ROUND_TRAINING_RECORDS_VALIDATED_WITH_DESIGN_RELEASE_OPEN'if not failures else'FINAL_RECORD_VALIDATION_FAILED','createdUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifestGroups':groups,'historicalMutablePointerExceptions':exceptions,'acceptedScopedReports':accepted,'localLinkChecks':len(links),'missingLinks':[x for x in links if not x['exists']],'failures':failures,'fullBoardReleased':False,'physicalTestsPerformed':False,'stillOpen':['seven GPIO connections per training board','USB four data/shared nets and fresh whole-board DRC','new L2GND-to-L3V3 reference conversion SI/PI review','mask/silk/stencil/actual MPN-height and factory rotation approval','physical board powerup/EMI measurements NOT_RUN']}
dump(J/'review/final_record_validation.json',qa)
if failures:
 print(json.dumps({'failures':failures,'sourceGroups':groups},ensure_ascii=True));raise SystemExit(2)
owned=set([R/'EDA.md',R/'课程索引.md',R/'learning/notes/pcb_layer_naming.md',J/'README.md',J/'learning_plan.md',J/'review/final_record_validation.json'])
owned.update((R/'learning/notes').glob('lessonJK*.md'))
for directory in [J/'scripts',J/'bench',J/'source/bench_datasheets',J/'backups']:
 owned.update(p for p in directory.rglob('*')if p.is_file() and '__pycache__'not in p.parts)
for directory in [J/'review/independent_CAM',J/'review/independent_CAM_J55',J/'review/independent_CAM_NEWSTACK',J/'review/companion_and_J55_CAM']:
 owned.update(p for p in directory.rglob('*')if p.is_file())
for name in ['cam56_visual_qa.json','cam56_parser_corrections.md','root_record_update_corrections.md','user_four_layer_function_rule_20261022.json','layer_policy_history_mapping.json']:
 owned.add(J/'review'/name)
owned.update(manifests);owned.update((J/'tooling').glob('*.json'))
rows=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(owned)if p.exists()]
final={'status':'J_K_THIS_ROUND_ARTIFACTS_SEALED_NOT_PRODUCTION_RELEASE','createdUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Root notes/entrypoints/CAM/bench and references to seven frozen specialist manifests; negative history retained, only explicit accepted reports are passes.','files':rows,'manifestGroupValidation':groups,'historicalMutablePointerExceptions':exceptions,'validatedLocalLinks':len(links),'fullBoardReleased':False,'physicalTestsPerformed':False}
p=J/'artifact_manifest.json';dump(p,final)
mismatches=[r['path']for r in rows if sha(Path(r['path']))!=r['sha256']];assert not mismatches,mismatches
print(json.dumps({'status':qa['status'],'groups':len(groups),'groupSHAEntries':sum(x['uniqueSHAEntries']for x in groups),'intentionalHistoricalSnapshotMatches':len(exceptions),'localLinks':len(links),'failures':0,'rootManifestFiles':len(rows),'rootManifestSHA256':sha(p)}))
