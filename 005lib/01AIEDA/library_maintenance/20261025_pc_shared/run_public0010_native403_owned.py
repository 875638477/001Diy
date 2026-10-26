"""Root-owned isolated source806 probe /Alt403/fresh runner; never use user session.

Preparation is not native proof. This script launches CAD only when root explicitly
invokes it. Full six-root guard before/after, separate board copy, fixed mm4 helpers,
bound case bundle, owned PID timeout only. A CAD exit0 without complete marker fails.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,time
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
def quote(p):return json.dumps(str(p).replace('\\','/'))
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--bundle',type=Path,required=True);ap.add_argument('--guard',type=Path,required=True);ap.add_argument('--phase',choices=['source-adjacency','apply','target-adjacency','fresh'],required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--input',type=Path);ap.add_argument('--input-sha256');ap.add_argument('--snapshot',type=Path);ap.add_argument('--timeout',type=int,default=1800);a=ap.parse_args()
 need(not a.out.exists(),'Fresh isolated output required');need(a.out.resolve().is_relative_to(M.resolve()),'Output must stay below maintenance root');need(a.timeout>=60,'Timeout must allow startup')
 man=jr(a.bundle/'BUNDLE_MANIFEST.json');need(man['schema']=='PUBLIC0010_403_NATIVE_CASE_BUNDLE_V1' and man['source_units']==['millimeters',4],'Unexpected bundle schema/units')
 for e in man['bundle_files']+man['external_proofs']:need(sha(e['path'])==e['sha256'],'Frozen bundle or source proof changed '+e['path'])
 spec=importlib.util.spec_from_file_location('guard_helper',M/'publish_exact_public_olbs.py');guardhelper=importlib.util.module_from_spec(spec);spec.loader.exec_module(guardhelper)
 guard=jr(a.guard);before=guardhelper.verify_guard(guard)
 source=Path(man['source_board']);need(sha(source)==man['source_board_sha256'],'Original0010 source changed')
 if a.phase in ['source-adjacency','apply']:
  need(a.input is None and a.input_sha256 is None,'Source/apply fixed to original680500 only');inp=source;expected=man['source_board_sha256']
 else:
  need(a.input is not None and a.input_sha256 is not None,'Candidate phase requires explicit input SHA');inp=a.input;expected=a.input_sha256.upper();need(sha(inp)==expected,'Candidate input SHA mismatch')
 if a.phase=='fresh':need(a.snapshot is not None and a.snapshot.is_file(),'Fresh phase requires source593 text/property snapshot')
 a.out.mkdir(parents=True);copy=a.out/'INPUT_COPY.brd';shutil.copyfile(inp,copy);need(sha(copy)==expected,'Independent board copy SHA mismatch')
 if a.phase=='source-adjacency':expression='pub403SourceOnly('+quote(a.out)+')';marker='PUB403_SOURCE_COMPLETE.txt'
 elif a.phase=='apply':expression='pub403Apply('+quote(a.out)+')';marker='PUB403_APPLY_COMPLETE.txt'
 elif a.phase=='target-adjacency':expression='pub403TargetOnly('+quote(a.out)+')';marker='TARGET_ADJACENCY_ONLY_COMPLETE.txt'
 else:expression='pub403Fresh('+quote(a.snapshot)+' '+quote(a.out)+')';marker='PUB403_FRESH_COMPLETE.txt'
 lines=['set NOCONFIRM','skill pub403Bundle='+quote(a.bundle),'skill errset(load('+quote(a.bundle/'public0010_native403_v1.il')+') t)','skill errset('+expression+' t)']
 lines+=['quit','fillin "yes"'];scr=a.out/'run.scr';scr.write_text('\n'.join(lines)+'\n',encoding='utf-8')
 args=['C:/Program0/cadence/SPB172/tools/bin/allegro.exe','-product','Allegro_performance','-safe','-nographic']
 if a.phase!='apply':args.append('-readonly')
 args+=['-s',str(scr),'-p',str(a.out),str(copy)];start=time.time();status='FAIL';error=None
 with (a.out/'stdout.txt').open('wb') as out,(a.out/'stderr.txt').open('wb') as err:
  proc=subprocess.Popen(args,cwd=a.out,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
  (a.out/'OWNED_PROCESS.json').write_text(json.dumps({'pid':proc.pid,'start_epoch':start,'command':args},indent=2),encoding='utf-8')
  try:code=proc.wait(timeout=a.timeout)
  except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=30);code=proc.returncode;error='TIMEOUT_OWNED_PROCESS_ONLY_TERMINATED'
  if error is None:
   if code==0 and (a.out/marker).is_file():status='PASS_NATIVE_CASE_PHASE_ONLY'
   else:error='CAD_EXIT_OR_REQUIRED_NATIVE_COMPLETE_MARKER_FAILED'
 after=guardhelper.verify_guard(guard);need(sha(inp)==expected and sha(source)==man['source_board_sha256'],'Protected source/candidate bytes changed')
 # Readonly phases cannot alter the independent opened input copy either.
 if a.phase!='apply':need(sha(copy)==expected,'Readonly native input copy changed')
 receipt={'status':status,'error':error,'phase':a.phase,'exit_code':code,'elapsed_seconds':time.time()-start,'bundle_manifest':str(a.bundle/'BUNDLE_MANIFEST.json'),'bundle_manifest_sha256':sha(a.bundle/'BUNDLE_MANIFEST.json'),'runner_sha256':sha(__file__),'source':str(inp),'source_sha256_before':expected,'source_sha256_after':sha(inp),'original_source_680500_sha256':sha(source),'guard':str(a.guard),'guard_sha256':sha(a.guard),'full_public_files_before':before,'full_public_files_after':after,'public_unchanged':True,'marker':str(a.out/marker),'write_candidate':a.phase=='apply','actual_native_connections_copper_CFX_final_approval':False}
 if a.phase=='apply' and (a.out/'PUB0010_ALT403.brd').is_file():receipt.update(candidate=str(a.out/'PUB0010_ALT403.brd'),candidate_sha256=sha(a.out/'PUB0010_ALT403.brd'))
 (a.out/'RUN_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False,indent=2));return 0 if status.startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
