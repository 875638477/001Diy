"""Root-only read-only native probe; source25 ownership and old/new pad containment."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,subprocess,time
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
q=lambda p:json.dumps(str(p).replace('\\','/'))
def need(v,m):
 if not v:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--bundle',type=Path,required=True);ap.add_argument('--guard',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--timeout',type=int,default=240);a=ap.parse_args()
 need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()),'Fresh isolated maintenance output required')
 man=jr(a.bundle/'MANIFEST.json');need(man['schema']=='PUBLIC0010_SOURCE25_THERMAL_GAP_EXACT_OLD_LAND_CONTAINMENT_READONLY_V2' and man['source_units']==['millimeters',4] and man['no_create'] and man['no_save'],'Unexpected read-only scope')
 for e in man['files']:need(sha(e['path'])==e['sha256'],'Frozen input/helper changed '+e['path'])
 source=Path(man['source_board']);target=Path(man['target_board']);need(sha(source)==man['source_sha256'] and sha(target)==man['target_sha256'],'Source/partial SHA changed')
 spec=importlib.util.spec_from_file_location('guard_helper',M/'publish_exact_public_olbs.py');gh=importlib.util.module_from_spec(spec);spec.loader.exec_module(gh)
 before=gh.verify_guard(jr(a.guard));a.out.mkdir();s=a.out/'ORIGINAL_SOURCE_COPY.brd';t=a.out/'PARTIAL_COMPARE_COPY.brd';shutil.copyfile(source,s);shutil.copyfile(target,t)
 need(sha(s)==man['source_sha256'] and sha(t)==man['target_sha256'],'Independent copies mismatch')
 lines=['set NOCONFIRM','skill errset(load('+q(man['helper'])+') t)','skill errset('+man['entry_source']+'('+q(a.out)+') t)','open '+q(t),'skill errset('+man['entry_target']+'('+q(a.out)+') t)','quit','fillin "no"']
 scr=a.out/'run.scr';scr.write_text('\n'.join(lines)+'\n','utf-8')
 args=['C:/Program0/cadence/SPB172/tools/bin/allegro.exe','-product','Allegro_performance','-safe','-nographic','-s',str(scr),'-p',str(a.out),str(s)]
 start=time.time();error=None
 with (a.out/'stdout.txt').open('wb') as out,(a.out/'stderr.txt').open('wb') as err:
  proc=subprocess.Popen(args,cwd=a.out,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
  (a.out/'OWNED_PROCESS.json').write_text(json.dumps(dict(pid=proc.pid,start_epoch=start,command=args),indent=2),'utf-8')
  try:code=proc.wait(timeout=a.timeout)
  except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=30);code=proc.returncode;error='TIMEOUT_OWNED_PROCESS_ONLY_TERMINATED'
 complete=code==0 and all((a.out/man[k]).is_file() for k in ['source_marker','target_marker'])
 if not complete and error is None:error='CAD_EXIT_OR_READONLY_COMPLETE_MARKERS_FAILED'
 after=gh.verify_guard(jr(a.guard))
 need(sha(source)==sha(s)==man['source_sha256'] and sha(target)==sha(t)==man['target_sha256'],'Protected source/partial/input copies changed')
 for e in man['files']:need(sha(e['path'])==e['sha256'],'Frozen input/helper changed while running')
 receipt=dict(status='PASS_READONLY_SOURCE25_EXACT_OLD_LAND_THERMAL_DELTA' if complete else 'FAIL',error=error,exit_code=code,elapsed_seconds=time.time()-start,source_board=str(source),source_sha256=sha(source),partial_board=str(target),partial_sha256=sha(target),source_and_partial_copies_unchanged=True,public_unchanged=True,public_files_before=before,public_files_after=after,guard=str(a.guard),guard_sha256=sha(a.guard),manifest=str(a.bundle/'MANIFEST.json'),manifest_sha256=sha(a.bundle/'MANIFEST.json'),runner_sha256=sha(__file__),no_create=True,no_save=True)
 (a.out/'RUN_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n','utf-8');print(json.dumps(receipt,indent=2));return 0 if complete else 2
if __name__=='__main__':raise SystemExit(main())
