"""Root-executed cold process audit. Every PSM gets an independent EMPTY4 and owned Allegro PID."""
import argparse,concurrent.futures,hashlib,importlib.util,json,pathlib,shutil,subprocess,time

def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest().upper()
def dump(p,x):pathlib.Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--plan',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--timeout-per-asset',type=int,default=60);ap.add_argument('--max-assets',type=int,default=0);ap.add_argument('--start-index',type=int,default=0)
 a=ap.parse_args();assert 1<=a.workers<=4 and a.timeout_per_asset>0;assert not a.output.exists(),'Fresh output required'
 plan=json.loads(a.plan.read_text(encoding='utf-8-sig'));assert plan['schema']=='GLOBAL_SUFFIX_PUBLIC_NATIVE_AUDIT_PLAN_V1'
 guards=json.loads(pathlib.Path(plan['public_guard_manifest']).read_text(encoding='utf-8-sig'))['files']
 for x in plan['helpers']:assert sha(x['path'])==x['sha256'],'Frozen helper changed'
 helper=next(pathlib.Path(x['path']) for x in plan['helpers'] if pathlib.Path(x['path']).name=='run_pc_native_audit.py')
 empty=next(pathlib.Path(x['path']) for x in plan['helpers'] if pathlib.Path(x['path']).name=='EMPTY4.brd')
 native=pathlib.Path(__file__).with_name('psm_native_units_mainfont_v1.il');assert native.is_file()
 spec=importlib.util.spec_from_file_location('cold_native_audit_base',helper);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
 def check_guards(label):
  bad=[x['path'] for x in guards if not pathlib.Path(x['path']).is_file() or sha(x['path'])!=x['sha256']]
  if bad:raise RuntimeError('Public guard changed '+label+': '+repr(bad[:20]))
 a.output.mkdir(parents=True);check_guards('before_all')
 selected=plan['representatives'][a.start_index:]
 if a.max_assets:selected=selected[:a.max_assets]
 assert selected
 bindings={'schema':'PROJECT6_MAIN_MILS2_FOUR_LAYER_ALL64_FONT_CONTEXT_COLD_V1','plan':str(a.plan),'plan_sha256':sha(a.plan),'guard_manifest':plan['public_guard_manifest'],'guard_manifest_sha256':sha(plan['public_guard_manifest']),'guarded_files':len(guards),'helpers':plan['helpers'],'runner':str(pathlib.Path(__file__)),'runner_sha256':sha(__file__),'first_only_native_helper':str(native),'first_only_native_helper_sha256':sha(native),'workers':a.workers,'timeout_per_asset':a.timeout_per_asset,'planned':len(plan['representatives']),'selected':len(selected),'selected_start_index':a.start_index,'cold_process_policy':'Exactly one PSM per process. Current startup EMPTY4 is used without any axlOpenDesignForBatch call; distinct isolated temp/pcbenv/output per source.'}
 dump(a.output/'INPUT_BINDINGS.json',bindings)
 def run_one(pair):
  i,item=pair;r=a.output/f'e{i+a.start_index:05}';r.mkdir();(r/'units').mkdir();(r/'output').mkdir();env=b.envfor(r);before=sha(item['path']);assert before==item['sha256'],'Source changed before asset'
  row=dict(mode='public_global_suffix_cold',source_name=item['stem'],stem=item['stem'],path=item['path'],source_path=item['path'],source_sha256=item['sha256'],alias_sha256=item['sha256'],audit_output=str(r/'output/0000.sexp'),byte_identical_members=item['byte_identical_members'],frozen_classification=item['classification'],canonical_candidate=item['canonical_candidate'])
  rec={};start=time.time()
  try:
   b.metadata(row,r,env,0)
   blank=r/'blankA.brd';shutil.copyfile(empty,blank);assert sha(blank)==sha(empty)
   box=row['original_extents'];lit='(('+' '.join(box[0])+') ('+' '.join(box[1])+'))'
   job='('+b.q(row['stem'])+' '+b.q(row['audit_output'])+' '+b.q('mils')+' 2 ((-33500.0 -33500.0) (33500.0 33500.0)))'
   row['audit_context_units']='mils';row['audit_context_accuracy']=2;row['audit_context_copper_layers']=['TOP','L2','L3','BOTTOM']
   (r/'jobs.il').write_text('pcSharedNativeBatchV2('+b.q(blank)+' '+b.q(blank)+" '("+job+') '+b.q(r/'status.tsv')+' '+b.q(plan['psmpath'])+' '+b.q(plan['padpath'])+')\n',encoding='ascii')
   (r/'run.scr').write_text('set NOCONFIRM\nskill errset(load('+b.q(native)+') t)\nskill errset(load('+b.q(r/'jobs.il')+') t)\nquit\nfillin "yes"\n',encoding='ascii')
   dump(r/'manifest.json',[row])
   cmd=[b.CAD/'tools/bin/allegro.exe','-product','Allegro_performance','-safe','-nographic','-s',r/'run.scr','-p',r,blank]
   try:rec=b.launch(cmd,r,env,a.timeout_per_asset,'allegro')
   except subprocess.TimeoutExpired:rec={'command':[str(x) for x in cmd],'exit_code':None,'timeout_seconds':a.timeout_per_asset,'status':'OWNED_PROCESS_TIMEOUT_KILLED_BY_SUBPROCESS_RUN'}
  except Exception as ex:rec.update(exit_code=rec.get('exit_code'),error=repr(ex))
  after=sha(item['path']);status=(r/'status.tsv').read_text(encoding='utf-8',errors='replace') if (r/'status.tsv').exists() else '';out=pathlib.Path(row['audit_output']);raw=out.read_text(encoding='utf-8',errors='replace') if out.exists() else ''
  row['source_sha256_after']=after;dump(r/'manifest.json',[row])
  rec.update(index=i+a.start_index,stem=item['stem'],expected=1,outputs=int(out.exists()),complete=status.rstrip().endswith('COMPLETE') and raw.rstrip().endswith('(complete t)'),source_sha256_before=before,source_sha256_after=after,source_unchanged=before==after==item['sha256'],manifest=str(r/'manifest.json'),manifest_sha256=sha(r/'manifest.json'),audit_output=str(out),audit_output_sha256=sha(out) if out.exists() else None,total_asset_seconds=round(time.time()-start,3))
  rec['passed']=rec.get('exit_code')==0 and rec['complete'] and rec['source_unchanged'];dump(r/'launch_report.json',rec)
  return row,rec
 done=[];records=[];print(json.dumps({'stage':'cold_native_begin','selected':len(selected),'workers':a.workers,'public_guard_files':len(guards)}),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
  futures=[pool.submit(run_one,pair) for pair in enumerate(selected)]
  for f in concurrent.futures.as_completed(futures):
   row,rec=f.result();done.append(row);records.append(rec);n=len(records)
   if n%20==0 or n==len(selected) or not rec['passed']:
    dump(a.output/'manifest.json',sorted(done,key=lambda x:x['stem'].casefold()));dump(a.output/'PROGRESS.json',{'completed':n,'expected':len(selected),'passed':sum(r['passed'] for r in records),'failed':[r for r in records if not r['passed']]});print(json.dumps({'stage':'cold_native_progress','completed':n,'expected':len(selected),'passed':sum(r['passed'] for r in records),'last':rec['stem'],'last_passed':rec['passed']}),flush=True)
   if n%100==0:check_guards('after_completed_'+str(n))
 check_guards('after_all')
 failed=[r for r in records if not r['passed']]
 result={'status':'RAW_COMPLETE_NATIVE_EXPORTS_REQUIRE_FULL_GEOMETRY_PAD_ATTRIBUTE_REVIEW' if not failed else 'INCOMPLETE_NATIVE_EXPORTS_NO_CONSOLIDATION_ALLOWED','planned_psm_count':len(plan['representatives']),'selected_psm_count':len(selected),'selected_start_index':a.start_index,'all_plan_assets_selected':a.start_index==0 and len(selected)==len(plan['representatives']),'native_representatives':len(selected),'outputs':sum(r['outputs'] for r in records),'all_assets_passed':not failed,'public_files_unchanged':True,'guarded_file_count':len(guards),'cold_independent_cache_every_source':True,'process_workers':a.workers,'failed':failed,'launches':sorted(records,key=lambda x:x['index']),'not_established':'Export success alone is not equivalence, safe deletion, or rewritten OLB/BRD references.'}
 dump(a.output/'manifest.json',sorted(done,key=lambda x:x['stem'].casefold()));dump(a.output/'report.json',result);print(json.dumps({k:v for k,v in result.items() if k!='launches'}),flush=True)
 if failed:raise SystemExit(2)
if __name__=='__main__':main()
