from pathlib import Path
p=Path(r'D:\001DIY\005lib\01AIEDA\learning\staging\b_lessons_20261018\finish_b_records.py')
s=p.read_text()
s=s.replace("assert (path.parent/target).resolve().exists(),(path,'missing new Markdown target',target)","assert (path.parent/target).resolve().exists() or (path.parent/target).resolve() in {(ROOT/cfg['summaryPath']).resolve(),(ROOT/'learning/logs/b_lessons_07_10_20261018.json').resolve()},(path,'missing new Markdown target',target)")
insertion="""manifest_checks=[]
for name in cfg['manifests']:
 p=inside(ROOT/name);m=json.loads(p.read_text(encoding='utf-8-sig'));entries=m if isinstance(m,list) else m['files']
 for e in entries:
  q=inside(pathlib.Path(e['path']));assert q.is_file(),q;assert sha(q.read_bytes())==e['sha256'].upper(),(q,'artifact SHA mismatch')
 manifest_checks.append({'path':str(p),'filesVerified':len(entries),'status':'PASS'})
"""
s=s.replace('planned=[]',insertion+'planned=[]')
s=s.replace("report['inventory']=inventory","report['inventory']=inventory\nreport['manifestChecks']=manifest_checks")
p.write_text(s,encoding='utf-8')
print('Prepared artifact hashes and planned-link guards')
