import pathlib,json,hashlib,datetime,re
ROOT=pathlib.Path(r'D:\001DIY\005lib\01AIEDA').resolve()
BASE=ROOT/'learning/staging/f_27_29_20261019'
cfg=json.loads((BASE/'integration_payload.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def inside(p):
 p=p.resolve();assert p.is_relative_to(ROOT),p;return p
checked=[]
for item in cfg['required']:
 p=inside(ROOT/item['path']);x=json.loads(p.read_text(encoding='utf-8-sig'))
 assert x['status']==item['status'],(p,x.get('status'))
 checks=x.get('checks',[])
 assert all(c.get('pass',True) for c in checks),(p,'failed checks')
 checked.append({'path':str(p),'status':x['status'],'sha256':sha(p),'checks':len(checks)})
for n in cfg['notes']:assert (ROOT/n).is_file(),n
for n,v in cfg['sourceFiles'].items():assert sha(ROOT/n)==v,(n,'input identity changed')
manifests=[]
for name in cfg['manifests']:
 p=inside(ROOT/name);m=json.loads(p.read_text(encoding='utf-8-sig'))
 def hash_entries(node):
  if isinstance(node,dict):
   if 'path' in node and ('sha256' in node or 'SHA256' in node):yield node
   for value in node.values():yield from hash_entries(value)
  elif isinstance(node,list):
   for value in node:yield from hash_entries(value)
 entries=list(hash_entries(m));assert entries,(p,'empty artifact hash manifest')
 unique=set()
 for e in entries:
  q=pathlib.Path(e['path']);q=q if q.is_absolute() else p.parent/q
  q=inside(q);assert q.is_file(),q
  expected=e.get('sha256',e.get('SHA256'));assert expected and sha(q)==expected.upper(),(q,'artifact hash mismatch')
  unique.add(q)
 manifests.append({'path':str(p),'hashEntriesVerified':len(entries),'uniqueFilesVerified':len(unique),'status':'PASS'})
summary=inside(ROOT/cfg['summaryPath']);assert not summary.exists(),summary
reportPath=ROOT/'learning/logs/f_lessons_27_29_20261019.json'
planned=[]
for op in cfg['edits']:
 p=inside(ROOT/op['path']);raw=p.read_bytes();txt=raw.decode('utf-8-sig')
 eol='\r\n' if '\r\n' in txt else '\n'
 for old,new in op.get('replacements',[]):
  assert txt.count(old)==1,(p,'expected text changed or ambiguous',old)
  txt=txt.replace(old,new)
 if op.get('append'):
  assert op['marker'] not in txt,(p,'already integrated')
  txt=txt.rstrip()+eol+eol+op['append'].replace('\r\n','\n').replace('\n',eol)+eol
 out=txt.encode('utf-8')
 if raw.startswith(b'\xef\xbb\xbf'):out=b'\xef\xbb\xbf'+out
 planned.append((p,raw,out))
# Verify new local links before committing any records.
for q,parts in [(summary,[cfg['summary']])]+[(ROOT/o['path'],[n for _,n in o.get('replacements',[])]+[o.get('append','')]) for o in cfg['edits']]:
 for part in parts:
  for target in re.findall(r'\]\(([^)]+)\)',part):
   target=target.strip('<>').split('#')[0]
   if not target or '://' in target:continue
   t=(q.parent/target).resolve()
   assert t.exists() or t in [summary,reportPath.resolve()],(q,'missing link',target)
stamp=datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y%m%d_%H%M%S')
backup=ROOT/'backups'/('before_F_27_29_'+stamp);backup.mkdir(parents=True,exist_ok=False)
changes=[]
for p,raw,out in planned:
 b=backup/p.relative_to(ROOT);b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(raw)
 assert b.read_bytes()==raw
 changes.append({'path':str(p),'backup':str(b),'beforeSHA256':hashlib.sha256(raw).hexdigest().upper(),'afterSHA256':hashlib.sha256(out).hexdigest().upper()})
for p,raw,out in planned:assert p.read_bytes()==raw,(p,'concurrent change')
for p,raw,out in planned:p.write_bytes(out)
summary.write_text(cfg['summary'],encoding='utf-8')
# User-authored preamble remains byte-for-byte equal before first H2.
eda=ROOT/'EDA.md'
entry=next(c for c in changes if pathlib.Path(c['path'])==eda)
assert eda.read_text(encoding='utf-8-sig').split('\n## ',1)[0]==pathlib.Path(entry['backup']).read_text(encoding='utf-8-sig').split('\n## ',1)[0]
records=[summary]+[ROOT/n for n in cfg['notes']]+[p for p,_,_ in planned]
report={'date':'2026-10-19 Asia/Shanghai','status':'PASS_NATIVE_CAD_F_27_29','courseChecks':checked,'manifestChecks':manifests,'summary':str(summary),'recordRoot':str(ROOT),'changes':changes,'scopeAndOpenItems':cfg['scopeAndOpenItems'],'originalSourceIdentity':cfg['sourceFiles'],'userPreamblePreserved':True,'recordFiles':[{'path':str(q),'sha256':sha(q),'bytes':q.stat().st_size} for q in dict.fromkeys(records)],'inventory':[]}
for folder in cfg['inventoryFolders']:
 for q in sorted((ROOT/folder).rglob('*')):
  if q.is_file():report['inventory'].append({'path':str(q.relative_to(ROOT)),'bytes':q.stat().st_size,'sha256':sha(q)})
reportPath.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':report['status'],'summary':str(summary),'report':str(reportPath),'recordFiles':len(report['recordFiles']),'inventoryFiles':len(report['inventory'])},ensure_ascii=True))
