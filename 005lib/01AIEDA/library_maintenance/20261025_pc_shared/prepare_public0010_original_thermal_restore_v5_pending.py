"""Save only a private UNAPPROVED result; fresh complete cache gate remains required."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 old=M/'public0010_original_thermal_restore_bundle13_v4';b=M/'public0010_original_thermal_restore_bundle13_v5_pending';assert not b.exists();b.mkdir()
 s=(old/'public0010_original_thermal_restore_v4.il').read_text()
 before='unless(equal(beforeCache pc25CacheSnapshot(strcat(dir "/AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist"))) error("Original thermal modified cached PSM/PAD/figure/textblock/property graphs\\n"))'
 after='''; Raw pad/proplist/opaque-path addresses can change on native refresh.
  ; Preserve this raw comparison as unapproved, never turn it into cache PASS.
  pc25AfterCache=pc25CacheSnapshot(strcat(dir "/AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist"))
  f=outfile(strcat(dir "/RAW_CACHE_COMPARISON_PENDING_FRESH_SEMANTIC_GATE.txt"))
  fprintf(f "RAW_ROWS_IDENTICAL=%L\\nCACHE_APPROVAL=UNAPPROVED_PENDING_FRESH_COMPLETE70_SCHEMA_AND_PUBLIC4_PAD_XML\\nNO_FORMAL_PUBLICATION_ALLOWED_BY_THIS_MARKER\\n" equal(beforeCache pc25AfterCache)) close(f)'''
 assert before in s;s=s.replace(before,after)
 s=s.replace('PUB0010_ORIGINAL_THERMAL_RESTORED.brd','PUB0010_ORIGINAL_THERMAL_UNAPPROVED.brd').replace('SOURCE21_ORIGINAL_THERMAL_RESTORE_COMPLETE.txt','SOURCE21_ORIGINAL_THERMAL_PENDING_CACHE_COMPLETE.txt').replace('ALL_CACHED_PSM_PAD_FIGURE_TEXTBLOCK_PROPERTY_GRAPHS_EXACT','RAW_CACHE_COMPARISON_RECORDED_NOT_APPROVED_FRESH_COMPLETE70_GRAPH_REQUIRED')
 h=b/'public0010_original_thermal_restore_v5_pending.il';h.write_text(s,'utf-8')
 man=json.loads((old/'MANIFEST.json').read_text());man.update(schema='PUBLIC0010_FINITE_ORIGINAL21_THERMAL_CU_PENDING_FRESH_CACHE_V5',helper=str(h),target_marker='SOURCE21_ORIGINAL_THERMAL_PENDING_CACHE_COMPLETE.txt',candidate_name='PUB0010_ORIGINAL_THERMAL_UNAPPROVED.brd',raw_cache_not_approved=True,formal_publication_prohibited_until_fresh_complete_cache=True)
 for p in [h,Path(__file__),old/'MANIFEST.json',M/'public0010_original_thermal_restore_run13_v4/RUN_RECEIPT.json',M/'public0010_original_thermal_restore_run13_v4/BEFORE_ALL_CACHED_DEFINITION_GRAPHS.ilist',M/'public0010_original_thermal_restore_run13_v4/AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist']:
  man['files'].append(dict(path=str(p),sha256=sha(p)))
 (b/'MANIFEST.json').write_text(json.dumps(man,indent=2)+'\n','utf-8')
 runner=M/'run_public0010_original_thermal_restore_v5_pending.py';text=(M/'run_public0010_original_thermal_restore_v4.py').read_text().replace('PUBLIC0010_FINITE_ORIGINAL21_THERMAL_PATH_CU_RESTORE_V4',man['schema']).replace('PASS_FINITE_ORIGINAL21_THERMAL_PATH_PHASE_ONLY','SAVED_UNAPPROVED_PRIVATE_CANDIDATE_PENDING_FRESH_COMPLETE70_CACHE_915_CFX')
 runner.write_text(text,'utf-8')
 print(json.dumps(dict(bundle=str(b),manifest_sha256=sha(b/'MANIFEST.json'),helper_sha256=sha(h),runner=str(runner),runner_sha256=sha(runner)),indent=2))
if __name__=='__main__':main()
