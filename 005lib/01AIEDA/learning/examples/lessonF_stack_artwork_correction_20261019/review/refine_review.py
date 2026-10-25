from pathlib import Path
import shutil
r=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019\review')
shutil.copy2(r/'review.json',r/'review_preliminary.json')
shutil.copy2(r/'independent_review.py',r/'independent_review_initial.py')
p=r/'independent_review.py';s=p.read_text(encoding='utf-8')
s=s.replace("re.sub(r'dbid:[0-9A-Fa-f]+','DBID',s)","re.sub(r'(dbid|propList):[0-9A-Fa-f]+',lambda m:m[1]+':PROCESS_ADDRESS',s)")
s=s.replace("for folder in (before,after):","blp=json.loads(text(before/'launch.json'))\n check(key+' baseline readonly completed exit0',blp['completed'] and blp['exitCode']==0 and blp['readonly'])\n eq(key+' baseline SHA matches original',blp['beforeSHA256'],entry['sha256'])\n eq(key+' baseline readonly disk hash preserved',blp['afterSHA256'],entry['sha256'])\n for folder in (before,after):")
s=s.replace("lr=table(legacy_file)","olp=json.loads(text(legacy_file.parent/'launch.json'))\n  check(key+' legacy direct-outline readonly completed exit0',olp['completed'] and olp['exitCode']==0 and olp['readonly'])\n  eq(key+' legacy readback expected board hash',olp['beforeSHA256'],lp['afterSHA256'])\n  eq(key+' legacy direct read leaves board unchanged',olp['afterSHA256'],lp['afterSHA256'])\n  check(key+' legacy direct reader completed','FCOR_OUTLINE_COMPLETE' in text(legacy_file))\n  lr=table(legacy_file)\n  root=[x for x in lr if q(x['role'])=='AUTHORITATIVE_ROOT']\n  eq(key+' authoritative root still DESIGN_OUTLINE',[q(x['layer']) for x in root],['BOARD GEOMETRY/DESIGN_OUTLINE'])")
s=s.replace("R.mkdir(exist_ok=True)","for source in ['scripts/correction.il','scripts/full_template_2.il','scripts/full_template_4.il','scripts/launch_fix.py','review/independent_review.py']:\n sha(C/source)\nR.mkdir(exist_ok=True)")
p.write_text(s,encoding='utf-8')
