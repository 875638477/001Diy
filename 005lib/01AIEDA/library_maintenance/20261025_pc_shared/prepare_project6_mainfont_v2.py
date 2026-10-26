"""Fix absent-slot detection: axlGetParam may return a truthy placeholder."""
from pathlib import Path
import json,hashlib,shutil
M=Path(__file__).parent;A=M/'project6_mainfont_plan13';B=M/'project6_mainfont_plan13_v2';assert not B.exists();B.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def q(p):return json.dumps(str(p).replace('\\','/'))
shutil.copy2(A/'MAIN_SOURCE64_FONT_CONTEXT.ilist',B/'MAIN_SOURCE64_FONT_CONTEXT.ilist')
s=(A/'mainfont_context.il').read_text().replace('/project6_mainfont_plan13/','/project6_mainfont_plan13_v2/')
old='''  for(i 1 64
   unless(axlGetParam(sprintf(nil "paramTextBlock:%d" i))
    unless(equal(axlDBTextBlockCreate(1) i) error("Cannot allocate exact source font slot\\n"))))'''
new='''  for(i 1 64
   p=axlGetParam(sprintf(nil "paramTextBlock:%d" i))
   ; axlGetParam can return a truthy objType-only placeholder for absent slots.
   unless(p && equal(p->name sprintf(nil "%d" i))
    unless(equal(axlDBTextBlockCreate(1) i) error("Cannot allocate exact source font slot\\n"))))'''
assert old in s;s=s.replace(old,new);f=B/'mainfont_context.il';f.write_text(s,encoding='utf-8')
helper=M/'psm_native_units_mainfont_v2.il';assert not helper.exists();helper.write_text((M/'psm_native_units_mainfont_v1.il').read_text().replace('/project6_mainfont_plan13/','/project6_mainfont_plan13_v2/'),encoding='utf-8')
runner=M/'run_project6_mainfont_cold_v2.py';assert not runner.exists();runner.write_text((M/'run_project6_mainfont_cold.py').read_text().replace('psm_native_units_mainfont_v1.il','psm_native_units_mainfont_v2.il'),encoding='utf-8')
plan=json.loads((A/'PROJECT6_MAINFONT_PLAN.json').read_text());plan['helpers']=[x for x in plan['helpers'] if not ('project6_mainfont_plan13' in x['path'] or Path(x['path']).name=='psm_native_units_mainfont_v1.il')]
plan['helpers'].extend({'path':str(p),'sha256':sha(p)} for p in (B/'MAIN_SOURCE64_FONT_CONTEXT.ilist',f,helper))
p=B/'PROJECT6_MAINFONT_PLAN.json';p.write_text(json.dumps(plan,indent=2),encoding='utf-8')
report={'status':'PREPARED_ONLY','change':'Absent parameter slot must have matching name, not merely a truthy param placeholder. Every64 full-field equality guard retained.',
 'runner':str(runner),'runner_sha256':sha(runner),'helper':str(helper),'helper_sha256':sha(helper),'plan':str(p),'plan_sha256':sha(p),'initializer_sha256':sha(f)}
(B/'PREPARATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
