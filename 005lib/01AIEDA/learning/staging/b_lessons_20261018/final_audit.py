import pathlib,json,hashlib,re
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA')
cfg=json.loads((R/'learning/staging/b_lessons_20261018/integration_payload.json').read_text(encoding='utf-8'))
p=R/'learning/logs/b_lessons_07_10_20261018.json'
report=json.loads(p.read_text(encoding='utf-8'))
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest().upper()
for c in report['changes']:assert sha(pathlib.Path(c['path']))==c['afterSHA256']
eda=R/'EDA.md';old=pathlib.Path(next(c['backup'] for c in report['changes'] if pathlib.Path(c['path'])==eda))
assert eda.read_text(encoding='utf-8-sig').split('\n## ',1)[0]==old.read_text(encoding='utf-8-sig').split('\n## ',1)[0]
index=(R/cfg['edits'][1]['path']).read_text(encoding='utf-8-sig')
block=index.split('### B.',1)[1].split('### C.',1)[0]
assert '\u5f85\u5b66\u4e60' not in block
links=0
for rel in cfg['notes']+[cfg['summaryPath']]:
 q=R/rel
 for target in re.findall(r'\]\(([^)]+)\)',q.read_text(encoding='utf-8-sig')):
  target=target.strip('<>').split('#')[0]
  if not target or '://' in target:continue
  assert (q.parent/target).resolve().exists(),(q,target)
  links+=1
v7=json.loads((R/cfg['required'][0]['path']).read_text());assert v7['allChecksPass'] and not v7.get('failures')
v10=json.loads((R/cfg['required'][3]['path']).read_text());assert all(c['pass'] for c in v10['checks'])
records=[eda,R/cfg['edits'][1]['path'],R/cfg['summaryPath']]+[R/n for n in cfg['notes']]+[R/o['path'] for o in cfg['edits'][2:]]
report['recordFiles']=[{'path':str(q),'sha256':sha(q),'bytes':q.stat().st_size} for q in records]
report['finalAudit']={'status':'PASS','userPreamblePreserved':True,'allFourCourseRowsComplete':True,'localLinksChecked':links,'lesson7Checks':len(v7['checks']),'lesson10Checks':v10['checks_count'],'nativeSourceAndGeometryPreviewsReviewed':True}
report['inventory']=[{'path':str(q.relative_to(R)),'bytes':q.stat().st_size,'sha256':sha(q)} for folder in cfg['inventoryFolders'] for q in sorted((R/folder).rglob('*')) if q.is_file()]
p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'PASS','linksChecked':links,'inventoryFiles':len(report['inventory']),'recordFiles':len(report['recordFiles']),'course7Checks':len(v7['checks']),'course10Checks':v10['checks_count']},ensure_ascii=True))
