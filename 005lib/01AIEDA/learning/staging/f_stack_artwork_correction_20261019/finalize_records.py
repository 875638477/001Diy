from pathlib import Path
import json,hashlib,datetime,re
ROOT=Path(r'D:\001DIY\005lib\01AIEDA').resolve()
BASE=ROOT/'learning/staging/f_stack_artwork_correction_20261019'
cfg=json.loads((BASE/'integration_payload.json').read_text(encoding='utf-8'))
completion=json.loads((BASE/'completion_payload.json').read_text(encoding='utf-8'))
cfg.update(completion)
cfg['noteText']=cfg['noteDraft']
for old,new in cfg['noteReplacements']:
 assert cfg['noteText'].count(old)==1,old
 cfg['noteText']=cfg['noteText'].replace(old,new)
assert '{{' not in cfg['noteText'],'unresolved note placeholder'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def inside(p):
 p=p.resolve();assert p.is_relative_to(ROOT),p;return p
evidence=[]
for item in cfg['requiredEvidence']:
 p=inside(ROOT/item['path']);x=json.loads(p.read_text(encoding='utf-8-sig'))
 assert x.get('status')==item['status'],(p,x.get('status'))
 for flag in ['allChecksPass','allCoreChecksPass']:
  if flag in x:assert x[flag] is True,(p,flag)
 assert not x.get('failedChecks'),(p,'failed check list')
 for key in ['failed','failedCount']:
  if isinstance(x.get(key),(int,float)):assert x[key]==0,(p,key)
 if isinstance(x.get('checks'),list):
  assert all(not isinstance(c,dict) or c.get('pass',True) for c in x['checks']),(p,'failed check')
 evidence.append({'path':str(p),'status':x['status'],'sha256':sha(p)})
def entries(node):
 if isinstance(node,dict):
  if 'path' in node and ('sha256' in node or 'SHA256' in node):yield node
  for value in node.values():yield from entries(value)
 elif isinstance(node,list):
  for value in node:yield from entries(value)
manifestResults=[]
for name in cfg.get('artifactManifests',[]):
 p=inside(ROOT/name);x=json.loads(p.read_text(encoding='utf-8-sig'));count=0
 for e in entries(x):
  q=Path(e['path']);q=q if q.is_absolute() else p.parent/q
  assert q.is_file(),q
  assert sha(q)==e.get('sha256',e.get('SHA256')).upper(),(q,'manifest identity')
  count+=1
 assert count>0,(p,'empty manifest')
 manifestResults.append({'path':str(p),'sha256':sha(p),'hashEntriesVerified':count})
for name,expected in cfg['unchangedSources'].items():assert sha(Path(name))==expected,(name,'original changed')
notePath=inside(ROOT/cfg['notePath']);reportPath=inside(ROOT/cfg['reportPath'])
assert not notePath.exists() and not reportPath.exists(),'already integrated'
planned=[]
for op in cfg['edits']:
 p=inside(ROOT/op['path']);raw=p.read_bytes();s=raw.decode('utf-8-sig')
 eol='\r\n' if '\r\n' in s else '\n'
 # Normalize only during editing and restore this file's original line endings.
 s=s.replace('\r\n','\n')
 for old,new in op.get('replacements',[]):
  assert s.count(old)==1,(p,'replacement not unique',old)
  s=s.replace(old,new)
 if op.get('prepend'):
  first,sep,rest=s.partition('\n')
  s=first+'\n\n'+op['prepend'].strip()+'\n\n'+rest.lstrip()
 if op.get('append'):
  assert op['append'].split('\n',1)[0] not in s,(p,'duplicate amendment')
  s=s.rstrip()+'\n\n'+op['append'].strip()+'\n'
 out=s.replace('\n',eol).encode('utf-8')
 if raw.startswith(b'\xef\xbb\xbf'):out=b'\xef\xbb\xbf'+out
 planned.append((p,raw,out))
oldReport=ROOT/'learning/logs/f_lessons_27_29_20261019.json'
raw=oldReport.read_bytes();historical=json.loads(raw.decode('utf-8-sig'))
historical['formerStatus']=historical['status']
historical['status']='HISTORICAL_CHECKS_WITH_USER_REQUIREMENT_GAPS'
historical['supersededBy']=str(reportPath)
historical['scopeCorrection']='Original checks omitted no-physical-MASK and complete drill2/drill4 film requirements; old counts and hashes are historical snapshots. Current files and record revisions are in supersededBy.'
planned.append((oldReport,raw,json.dumps(historical,ensure_ascii=False,indent=2).encode('utf-8')))
# Check only added/replaced links, plus the new full correction note.
linkParts=[(notePath,cfg['noteText'])]
for op in cfg['edits']:
 p=ROOT/op['path']
 linkParts.extend((p,n) for _,n in op.get('replacements',[]))
 linkParts.extend((p,op[k]) for k in ['prepend','append'] if op.get(k))
linkCount=0
for p,part in linkParts:
 for target in re.findall(r'\]\(([^)]+)\)',part):
  target=target.strip('<>').split('#')[0]
  if not target or '://' in target:continue
  q=(p.parent/target).resolve()
  assert q.exists() or q in [notePath,reportPath],(p,'missing new local link',target)
  linkCount+=1
stamp=datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y%m%d_%H%M%S')
backup=ROOT/'backups'/('before_stack_artwork_correction_'+stamp);backup.mkdir(parents=True,exist_ok=False)
changes=[]
for p,raw,out in planned:
 b=backup/p.relative_to(ROOT);b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(raw)
 assert b.read_bytes()==raw
 changes.append({'path':str(p),'backup':str(b),'beforeSHA256':hashlib.sha256(raw).hexdigest().upper(),'afterSHA256':hashlib.sha256(out).hexdigest().upper()})
for p,raw,out in planned:assert p.read_bytes()==raw,(p,'concurrent change')
for p,raw,out in planned:p.write_bytes(out)
notePath.write_text(cfg['noteText'],encoding='utf-8')
eda=ROOT/'EDA.md';entry=next(x for x in changes if Path(x['path'])==eda)
assert eda.read_bytes().split(b'\n## ',1)[0]==Path(entry['backup']).read_bytes().split(b'\n## ',1)[0],'user preamble changed'
records=[notePath]+[p for p,_,_ in planned]
report={'date':'2026-10-19 Asia/Shanghai','status':'PASS_STACK_ARTWORK_USER_CORRECTION','note':str(notePath),'recordRoot':str(ROOT),'userPreambleBytesUnchanged':True,'newLocalLinksChecked':linkCount,'evidence':evidence,'artifactManifestChecks':manifestResults,'unchangedOriginalSources':cfg['unchangedSources'],'currentBoards':[{'path':str(ROOT/n),'sha256':sha(ROOT/n)} for n in cfg['currentBoards']],'recordRevisions':changes,'recordFiles':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in records],'inventory':[],'limitations':cfg['limitations']}
for folder in cfg['inventoryFolders']:
 for p in sorted((ROOT/folder).rglob('*')):
  if p.is_file():report['inventory'].append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
reportPath.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':report['status'],'report':str(reportPath),'recordFiles':len(records),'inventoryFiles':len(report['inventory']),'links':linkCount},ensure_ascii=True))
