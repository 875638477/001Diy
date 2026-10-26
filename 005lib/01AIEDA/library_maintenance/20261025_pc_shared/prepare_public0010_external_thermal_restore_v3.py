"""V3: expose the first actual native create error; unchanged bounded Cu guards."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 old=M/'public0010_external_thermal_restore_bundle13_v2';b=M/'public0010_external_thermal_restore_bundle13_v3';assert not b.exists();b.mkdir()
 s=(old/'public0010_external_thermal_restore_v2.il').read_text('utf-8')
 s=s.replace('key=car(item) source=nth(1 item)\n   foreach(poly nth(2 item)','key=car(item) source=nth(1 item)\n   fprintf(pc25CreateStepPort "KEY_BEGIN %L SOURCE=%L POLYS=%L\\n" key source pc25Summary(nth(2 item))) drain(pc25CreateStepPort)\n   foreach(poly nth(2 item)')
 s=s.replace('requested=list(poly) result=axlDBCreateShape(poly t nth(2 source) nth(1 source) nil)','requested=list(poly) fprintf(pc25CreateStepPort "BEFORE_CREATE %L\\n" key) drain(pc25CreateStepPort)\n    result=axlDBCreateShape(poly t nth(2 source) nth(1 source) nil)\n    fprintf(pc25CreateStepPort "AFTER_CREATE %L RESULT=%L\\n" key result) drain(pc25CreateStepPort)')
 before='f=outfile(strcat(dir "/CREATED_EXTERNAL_THERMAL_SHAPES.ilist")) count=axlDBCloak(\'pc25CreateExternal(rows f) \'shape) close(f)'
 after='''f=outfile(strcat(dir "/CREATED_EXTERNAL_THERMAL_SHAPES.ilist"))
  pc25CreateStepPort=outfile(strcat(dir "/CREATE_STEP.txt"))
  fprintf(pc25CreateStepPort "PRE_CREATE_EXACT_ROWS=%d KEYS=%L\\n" length(rows) keys) drain(pc25CreateStepPort)
  ; Official axlDBCloak documentation recommends direct calls for debugging.
  ; errset(t) preserves the real first native error; no partial save follows it.
  count=errset(pc25CreateExternal(rows f) t) close(f) close(pc25CreateStepPort)
  unless(count error("External thermal direct create failed; see actual stdout and CREATE_STEP;NO_SAVE\\n")) count=car(count)'''
 assert before in s;s=s.replace(before,after)
 h=b/'public0010_external_thermal_restore_v3.il';h.write_text(s,'utf-8')
 man=json.loads((old/'MANIFEST.json').read_text());man.update(schema='PUBLIC0010_SOURCE_ONLY_EXTERNAL_THERMAL_CU_RESTORE_V3',helper=str(h),diagnostic_direct_create=True,unchanged_strict_21_source_only_geometry=True)
 man['files'] += [dict(path=str(p),sha256=sha(p)) for p in [h,Path(__file__),old/'MANIFEST.json']]
 (b/'MANIFEST.json').write_text(json.dumps(man,indent=2)+'\n','utf-8')
 runner=M/'run_public0010_external_thermal_restore_v3.py';runner.write_text((M/'run_public0010_external_thermal_restore_v2.py').read_text().replace('PUBLIC0010_SOURCE_ONLY_EXTERNAL_THERMAL_CU_RESTORE_V2',man['schema']),'utf-8')
 print(json.dumps(dict(bundle=str(b),manifest_sha256=sha(b/'MANIFEST.json'),helper_sha256=sha(h),runner=str(runner),runner_sha256=sha(runner)),indent=2))
if __name__=='__main__':main()
