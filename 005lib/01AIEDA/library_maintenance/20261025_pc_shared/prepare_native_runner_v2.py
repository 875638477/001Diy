from pathlib import Path
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
s=(M/'run_global_suffix_psm_native_audit.py').read_text(encoding='utf-8-sig')
s=s.replace('import argparse,collections,concurrent.futures,hashlib,importlib.util,json,pathlib,shutil,time','import argparse,collections,concurrent.futures,hashlib,importlib.util,json,pathlib,shutil,time,subprocess')
s=s.replace(' ap.add_argument("--timeout-per-chunk",type=int,default=1200)',' ap.add_argument("--timeout-per-chunk",type=int,default=1200)\n ap.add_argument("--max-assets",type=int,default=0)\n ap.add_argument("--start-index",type=int,default=0)')
s=s.replace(' native=next(pathlib.Path(x["path"]) for x in plan["helpers"] if pathlib.Path(x["path"]).name=="psm_native_units.il")',' native=pathlib.Path(__file__).with_name("psm_native_units_alternating_v2.il")\n assert native.is_file()')
s=s.replace('"runner_sha256":sha(__file__)}','"runner_sha256":sha(__file__),"alternating_native_helper":str(native),"alternating_native_helper_sha256":sha(native)}')
s=s.replace(' rows=plan["representatives"];allrows=[];launches=[]',' rows=plan["representatives"][a.start_index:]\n if a.max_assets:rows=rows[:a.max_assets]\n assert rows,"No selected assets"\n allrows=[];launches=[]')
s=s.replace('  blank=r/"blank.brd";shutil.copyfile(empty,blank)','  blank=r/"blankA.brd";blankB=r/"blankB.brd"\n  shutil.copyfile(empty,blank);shutil.copyfile(empty,blankB)\n  assert sha(blank)==sha(blankB)==sha(empty)')
s=s.replace('"psmNativeBatch("+b.q(blank)+" \'("','"pcSharedNativeBatchV2("+b.q(blank)+" "+b.q(blankB)+" \'("')
old='  rec=b.launch([b.CAD/"tools/bin/allegro.exe","-product","Allegro_performance","-safe","-nographic","-s",r/"run.scr","-p",r,blank],r,env,a.timeout_per_chunk,"allegro")'
new='''  cmd=[b.CAD/"tools/bin/allegro.exe","-product","Allegro_performance","-safe","-nographic","-s",r/"run.scr","-p",r,blank]
  try:rec=b.launch(cmd,r,env,a.timeout_per_chunk,"allegro")
  except subprocess.TimeoutExpired:
   rec={"command":[str(x) for x in cmd],"exit_code":None,"timeout_seconds":a.timeout_per_chunk,"status":"OWNED_SUBPROCESS_TIMEOUT_KILLED_BY_SUBPROCESS_RUN_INCOMPLETE"}'''
s=s.replace(old,new)
s=s.replace('"selected_psm_count":plan["selected_psm_count"],"native_representatives":len(rows)','"planned_psm_count":plan["selected_psm_count"],"selected_psm_count":len(rows),"selected_start_index":a.start_index,"all_plan_assets_selected":a.start_index==0 and len(rows)==len(plan["representatives"]),"native_representatives":len(rows)')
s=s.replace('no preloaded symdefs/padstacks','first current EMPTY4 skips self-reopen; subsequent byte-identical EMPTY4 A/B alternating files; empty-cache assertion before every source')
(M/'run_global_suffix_psm_native_audit_v2.py').write_text(s,encoding='utf-8')
compile(s,str(M/'run_global_suffix_psm_native_audit_v2.py'),'exec')
print('Python compile PASS')
