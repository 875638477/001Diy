import pathlib,json,re,hashlib,datetime,urllib.parse
G=pathlib.Path(__file__).resolve().parents[1];R=G.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def putj(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
native=read(G/'review/native_final_report.json')
assert native['status']=='PASS_NATIVE_G_LAYOUT_AND_LOCAL_DECOUPLING'
assert native['validation']['failures']==0
root=read(G/'review/root_geometry_review.json')
for v in ('4L','2L'):
 b=native['boards'][v];assert sha(pathlib.Path(b['path']))==b['sha256']
 a=root['variants'][v];assert a['status']=='PASS_PLACEMENT_GEOMETRY_LOGICAL_MAPPING' and a['checks']==597
 p=pathlib.Path(b['normalized']);assert sha(p)==a['snapshotSHA256'].upper()
 assert read(p)['readbackDirectory']==b['readback']
 assert b['placed']==80 and b['logicalPins']==272 and b['nets']==69 and b['drcCount']==0 and b['vias']==4
expected={
 R/'learning/examples/lessonF_stack_artwork_correction_20261019/current/F29_CONSTRAINTS_v4.brd':'18ED6701C902A0918558AB13072290046F88299D73432C6882239919CD3C0233',
 R/'learning/examples/lessonF_stack_artwork_correction_20261019/current/F28_2L_USERFIX.brd':'A8E00C31A0B1D16FCF24972518244580244025164F0898CA760F31AFA559CCFB',
 R.parent/'01env/drill2.txt':'CAF62F092C045234C3C1E6E3000E8525EE69B3A60D9E82D429395E93BA73365E',
 R.parent/'01env/drill4.txt':'65ED4A1F8682015A5E6D2B19E0ED8CAC0996AABC2DADAA1EC5D13D9E011A2C46'}
# Some source registers render letter case differently; compare exact file content by SHA.
inputs=[]
for p,want in expected.items():
 actual=sha(p);inputs.append({'path':str(p),'sha256':actual,'expected':want,'unchanged':actual==want})
 assert actual==want,(str(p),actual,want)
bak=R/'backups/before_G_30_37_20261020/EDA.md';old=bak.read_bytes();new=(R/'EDA.md').read_bytes();mark='## 当前学习计划'.encode()
assert old[:old.index(mark)]==new[:new.index(mark)],'User preamble changed'
idx=(R/'课程索引.md').read_text(encoding='utf-8-sig');prior=(R/'backups/before_G_30_37_20261020/课程索引.md').read_text(encoding='utf-8-sig')
for n in (6,11,14,26,51):
 assert re.search(rf'^\| {n} \|.*$',idx,re.M).group()==re.search(rf'^\| {n} \|.*$',prior,re.M).group(),n
for n in range(30,38):assert '待学习' not in re.search(rf'^\| {n} \|.*$',idx,re.M).group()
# Audit all links in the new G notes/guide/plan; existing root-doc failures are compared with their saved baseline.
generatedTargets={(R/'learning/logs/g_lessons_30_37_20261020.json').resolve(),(G/'review/deliverable_manifest.json').resolve()}
docs=[R/'EDA.md',R/'课程索引.md',R/'learning/notes/lessonG_30_37_20261020.md',R/'learning/notes/lessonG_mcu_20261020.md',R/'learning/notes/lessonG_power_20261020.md',G/'README.md',G/'learning_plan.md']
def broken(p,base=None):
 data=p.read_text(encoding='utf-8-sig');out=[];total=0
 for m in re.finditer(r'\[[^\]]*\]\(([^)\n]+)\)',data):
  t=m.group(1).strip().strip('<>');t=t.split('#',1)[0]
  if not t or re.match(r'^(https?|mailto|app|plugin|skill)://',t):continue
  q=pathlib.Path(urllib.parse.unquote(t));q=q if q.is_absolute() else (base or p.parent)/q
  total+=1
  if not q.exists() and q.resolve() not in generatedTargets:out.append({'target':t,'resolved':str(q)})
 return total,out
links=[];newbroken=[]
for p in docs:
 total,missing=broken(p);known=[]
 if p.name in ('EDA.md','课程索引.md'):
  _,known=broken(R/'backups/before_G_30_37_20261020'/p.name,p.parent)
 knownTargets={x['target'] for x in known};unexplained=[x for x in missing if x['target'] not in knownTargets]
 links.append({'file':str(p.relative_to(R)),'checked':total,'preExistingBroken':[x for x in missing if x['target'] in knownTargets],'newBroken':unexplained})
 newbroken.extend(unexplained)
assert not newbroken,newbroken
reportPath=R/'learning/logs/g_lessons_30_37_20261020.json'
report={'status':'PASS_DECLARED_G30_37_LAYOUT_LEARNING_SCOPE','sessionStartDate':'2026-10-20','recordsFinalizedDate':'2026-10-21','generatedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(R),'lessons':list(range(30,38)),'currentBoards':native['boards'],'nativeValidation':native['validation'],'independentGeometry':{v:{k:root['variants'][v][k] for k in ('status','checks','logicalPinsCompared','snapshotSHA256')} for v in ('4L','2L')},'checksMustNotBeAddedTogether':True,'sourceAndTemplateHashes':inputs,'userPreambleBytePreserved':True,'unrelatedCourseRowsPreserved':[6,11,14,26,51],'links':links,'allCreatedFilesInside01AIEDA':True,'notes':[str(p.relative_to(R)) for p in docs],'backupDirectory':'backups/before_G_30_37_20261020','deliverableManifest':'learning/examples/lessonG_30_37_20261020/review/deliverable_manifest.json','limitations':native['limitations'],'nextLesson':{'number':38,'name':'逐段交互走线与精确几何操作','status':'not_started'}}
putj(reportPath,report)
manifestPath=G/'review/deliverable_manifest.json'
files={p for p in G.rglob('*') if p.is_file() and p!=manifestPath}
files.update(docs);files.add(reportPath);files.update(p for p in (R/'backups/before_G_30_37_20261020').rglob('*') if p.is_file())
entries=[{'path':str(p.relative_to(R)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files,key=lambda p:str(p).lower())]
manifest={'scope':'All files under this G task directory plus root EDA/course index, three current G notes, before-G record backups and session report; manifest itself excluded to avoid circular hashing. Source references outside G separately hashed in session report.','createdUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(R),'fileCount':len(entries),'files':entries}
putj(manifestPath,manifest)
assert all(sha(R/e['path'])==e['sha256'] for e in entries)
assert all(p.exists() for p in generatedTargets)
print(json.dumps({'status':report['status'],'manifestFiles':len(entries),'manifestSHA256':sha(manifestPath),'linksChecked':sum(x['checked'] for x in links),'preExistingBroken':sum(len(x['preExistingBroken']) for x in links),'newBroken':len(newbroken)},ensure_ascii=False))