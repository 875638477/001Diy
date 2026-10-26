"""Root-invoked read-only native preflight. Never mutates public/design inputs."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,subprocess,time
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
q=lambda p:json.dumps(str(p).replace('\\','/'))
def need(v,m):
 if not v:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--bundle',type=Path,required=True);ap.add_argument('--guard',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--timeout',type=int,default=1800);a=ap.parse_args()
 need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()),'Fresh isolated maintenance output required')
 man=jr(a.bundle/'MANIFEST.json');need(man['schema']=='PUBLIC0010_ALL_SOURCE_BRANCH_READONLY_STUB_PREFLIGHT_V1' and man['units']==['millimeters',4] and man['does_not_create_paths_or_save'],'Unexpected bundle scope')
 for e in man['files']:need(sha(e['path'])==e['sha256'],'Frozen input/helper changed '+e['path'])
 inp=Path(man['candidate_board']);expected=man['candidate_board_sha256'];need(sha(inp)==expected,'Actual candidate SHA changed')
 spec=importlib.util.spec_from_file_location('guard_helper',M/'publish_exact_public_olbs.py');gh=importlib.util.module_from_spec(spec);spec.loader.exec_module(gh)
 guard=jr(a.guard);before=gh.verify_guard(guard);a.out.mkdir();copy=a.out/'INPUT_COPY.brd';shutil.copyfile(inp,copy);need(sha(copy)==expected,'Independent input copy mismatch')
 lines=['set NOCONFIRM','skill errset(load('+q(man['helper'])+') t)','skill errset('+man['entry']+'('+q(a.out)+') t)','quit','fillin "yes"'];scr=a.out/'run.scr';scr.write_text('\n'.join(lines)+'\n','utf-8')
 args=['C:/Program0/cadence/SPB172/tools/bin/allegro.exe','-product','Allegro_performance','-safe','-nographic','-readonly','-s',str(scr),'-p',str(a.out),str(copy)]
 start=time.time();error=None
 with (a.out/'stdout.txt').open('wb') as out,(a.out/'stderr.txt').open('wb') as err:
  proc=subprocess.Popen(args,cwd=a.out,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
  (a.out/'OWNED_PROCESS.json').write_text(json.dumps(dict(pid=proc.pid,start_epoch=start,command=args),indent=2),'utf-8')
  try:code=proc.wait(timeout=a.timeout)
  except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=30);code=proc.returncode;error='TIMEOUT_OWNED_PROCESS_ONLY_TERMINATED'
 marker=a.out/man['marker'];complete=code==0 and marker.is_file()
 if not complete and error is None:error='CAD_EXIT_OR_COMPLETE_MARKER_FAILED'
 after=gh.verify_guard(guard);need(sha(inp)==sha(copy)==expected,'Read-only protected input changed')
 for e in man['files']:need(sha(e['path'])==e['sha256'],'Frozen input/helper changed while running')
 stats={}
 if complete:
  for line in marker.read_text().splitlines():
   if '=' in line:
    k,v=line.split('=',1);stats[k]=int(v)
  if man.get('phase')=='exact_line_and_via_net_diagnostic':need(stats['SOURCE_LINES']==2068 and stats['ACTUAL_VIAS']==1739,'Incomplete exact2068/1739 diagnostics')
  else:need(stats['GROUPS']==man['branch_groups'] and stats['FIT_GROUPS']+stats['FAILED_GROUPS']==man['branch_groups'],'Incomplete all-branch classification')
 receipt=dict(status='COMPLETE_READONLY_ALL_BRANCH_PREFLIGHT' if complete else 'FAIL',error=error,exit_code=code,elapsed_seconds=time.time()-start,candidate=str(inp),source_sha256_before=expected,source_sha256_after=sha(inp),public_unchanged=True,full_public_files_before=before,full_public_files_after=after,guard=str(a.guard),guard_sha256=sha(a.guard),manifest=str(a.bundle/'MANIFEST.json'),manifest_sha256=sha(a.bundle/'MANIFEST.json'),runner_sha256=sha(__file__),read_only_no_create_no_save=True,all_fit=(complete and stats['FAILED_GROUPS']==0) if man.get('phase')!='exact_line_and_via_net_diagnostic' else None,stats=stats,full_connection_and_copper_conservation_approved=False)
 (a.out/'RUN_RECEIPT.json').write_text(json.dumps(receipt,indent=2),'utf-8');print(json.dumps(receipt,indent=2));return 0 if complete else 2
if __name__=='__main__':raise SystemExit(main())
