import pathlib,json,hashlib,datetime,re
ROOT=pathlib.Path(r'D:\001DIY\005lib\01AIEDA')
P=ROOT/'learning/staging/b_lessons_20261018/integration_payload.json'
cfg=json.loads(P.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest().upper()
def inside(p):
 p=p.resolve();assert p.is_relative_to(ROOT.resolve()),p;return p
for item in cfg['required']:
 p=inside(ROOT/item['path']);assert p.is_file(),p
 if 'status' in item:
  x=json.loads(p.read_text(encoding='utf-8-sig'));assert x['status']==item['status'],(p,x.get('status'))
for note in cfg['notes']:assert (ROOT/note).is_file(),note
# Check new links before changing records; do not reinterpret historical snapshots.
for path,texts in [(ROOT/cfg['summaryPath'],[cfg['summary']])]+[(ROOT/o['path'],[n for _,n in o.get('replacements',[])]+[o.get('append','')]) for o in cfg['edits']]:
 for body in texts:
  for target in re.findall(r'\]\(([^)]+)\)',body):
   target=target.strip('<>').split('#')[0]
   if not target or '://' in target:continue
   assert (path.parent/target).resolve().exists() or (path.parent/target).resolve() in {(ROOT/cfg['summaryPath']).resolve(),(ROOT/'learning/logs/b_lessons_07_10_20261018.json').resolve()},(path,'missing new Markdown target',target)
manifest_checks=[]
for name in cfg['manifests']:
 p=inside(ROOT/name);m=json.loads(p.read_text(encoding='utf-8-sig'));entries=m if isinstance(m,list) else m['files']
 for e in entries:
  q=inside(pathlib.Path(e['path']));assert q.is_file(),q;assert sha(q.read_bytes())==e['sha256'].upper(),(q,'artifact SHA mismatch')
 manifest_checks.append({'path':str(p),'filesVerified':len(entries),'status':'PASS'})
planned=[]
for op in cfg['edits']:
 p=inside(ROOT/op['path']);raw=p.read_bytes();txt=raw.decode('utf-8-sig');eol='\r\n' if '\r\n' in txt else '\n'
 for old,new in op.get('replacements',[]):
  if old in txt:assert txt.count(old)==1,(p,'ambiguous replacement');txt=txt.replace(old,new)
  else:assert new in txt,(p,'expected text changed',old)
 if op.get('append') and op['marker'] not in txt:txt=txt.rstrip()+eol+eol+op['append'].replace('\r\n','\n').replace('\n',eol)+eol
 out=txt.encode('utf-8');out=(b'\xef\xbb\xbf'+out) if raw.startswith(b'\xef\xbb\xbf') else out
 planned.append((p,raw,out))
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup=inside(ROOT/'backups'/('b_lessons_'+stamp));backup.mkdir(parents=True,exist_ok=False)
changes=[]
for p,raw,out in planned:
 rel=p.relative_to(ROOT);bp=backup/rel;bp.parent.mkdir(parents=True,exist_ok=True);bp.write_bytes(raw)
 assert sha(bp.read_bytes())==sha(raw)
 changes.append({'path':str(p),'beforeSHA256':sha(raw),'afterSHA256':sha(out),'backup':str(bp)})
for p,raw,out in planned:assert p.read_bytes()==raw,(p,'concurrent change')
for p,raw,out in planned:p.write_bytes(out)
note=inside(ROOT/cfg['summaryPath']);assert not note.exists(),note;note.write_text(cfg['summary'],encoding='utf-8')
report={'date':'2026-10-18','status':'PASS_CAD_COURSE_BLOCK_07_10','method':'Official native Cadence creation, compilation and independent persisted read-back; source drawing review and external geometry checks','summary':str(note),'changes':changes,'courseValidations':[],'allSelfCreatedLearningFilesRoot':str(ROOT),'publicQMIArtifacts':'Unchanged; verified by lesson08 re-audit','limits':cfg['limits']}
for item in cfg['required']:
 if 'status' in item:
  p=ROOT/item['path'];report['courseValidations'].append({'path':str(p),'sha256':sha(p.read_bytes()),'status':item['status']})
inventory=[]
for folder in cfg['inventoryFolders']:
 for p in sorted((ROOT/folder).rglob('*')):
  if p.is_file():inventory.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
report['inventory']=inventory
report['manifestChecks']=manifest_checks
out=inside(ROOT/'learning/logs/b_lessons_07_10_20261018.json');out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':report['status'],'summary':str(note),'report':str(out),'inventoryFiles':len(inventory),'editedFiles':len(changes)},ensure_ascii=True))
