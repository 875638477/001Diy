from pathlib import Path
p=Path(r'D:\001DIY\005lib\01AIEDA\learning\staging\b_lessons_20261018\finish_b_records.py')
s=p.read_text()
start=s.index('# Validate each local Markdown link introduced')
s=s[:start]+"""print(json.dumps({'status':report['status'],'summary':str(note),'report':str(out),'inventoryFiles':len(inventory),'editedFiles':len(changes)},ensure_ascii=True))
"""
insert="""# Check new links before changing records; do not reinterpret historical snapshots.
for path,texts in [(ROOT/cfg['summaryPath'],[cfg['summary']])]+[(ROOT/o['path'],[n for _,n in o.get('replacements',[])]+[o.get('append','')]) for o in cfg['edits']]:
 for body in texts:
  for target in re.findall(r'\\]\\(([^)]+)\\)',body):
   target=target.strip('<>').split('#')[0]
   if not target or '://' in target:continue
   assert (path.parent/target).resolve().exists(),(path,'missing new Markdown target',target)
"""
s=s.replace("planned=[]",insert+"planned=[]")
p.write_text(s,encoding='utf-8')
print('Prepared pre-write link guard')
