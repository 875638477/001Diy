"""Root-invoked six-asset no-save package audit in private actual0010 context."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,subprocess,time
M=Path(__file__).parent;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper();jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'));q=lambda p:json.dumps(str(p).replace('\\','/'))
def need(v,m):
 if not v:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for n in ['bundle','guard','out']:ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--timeout',type=int,default=240);a=ap.parse_args();need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()),'Fresh private output required')
 j=jr(a.bundle/'MANIFEST.json');need(j['schema']=='PUBLIC0010_CANONICAL6_RETURNED_FRESH_DEFINITION_SAME_CONTEXT_V2','Wrong audit scope')
 for e in j['files']:need(sha(e['path'])==e['sha256'],'Frozen public asset/helper changed '+e['path'])
 src=Path(j['source_board']);need(sha(src)==j['source_sha256'],'Protected board changed')
 spec=importlib.util.spec_from_file_location('gh',M/'publish_exact_public_olbs.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);guard=jr(a.guard);before=g.verify_guard(guard)
 a.out.mkdir();inp=a.out/'THROWAWAY_CONTEXT_COPY.brd';shutil.copyfile(src,inp)
 scr=a.out/'run.scr';scr.write_text('\n'.join(['set NOCONFIRM','skill errset(load('+q(j['helper'])+') t)','skill errset('+j['entry']+'('+q(a.out)+') t)','quit','fillin "yes"'])+'\n','utf-8')
 args=['C:/Program0/cadence/SPB172/tools/bin/allegro.exe','-product','Allegro_performance','-safe','-nographic','-s',str(scr),'-p',str(a.out),str(inp)];t=time.time();error=None
 with (a.out/'stdout.txt').open('wb') as out,(a.out/'stderr.txt').open('wb') as err:
  p=subprocess.Popen(args,cwd=a.out,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW);(a.out/'OWNED_PROCESS.json').write_text(json.dumps(dict(pid=p.pid,command=args),indent=2),'utf-8')
  try:code=p.wait(timeout=a.timeout)
  except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=30);code=p.returncode;error='TIMEOUT_OWNED_ONLY'
 complete=code==0 and (a.out/j['marker']).is_file() and len(list(a.out.glob('actual_*.sexp')))==len(list(a.out.glob('public_*.sexp')))==6
 after=g.verify_guard(guard);need(sha(src)==j['source_sha256'],'Protected source changed')
 for e in j['files']:need(sha(e['path'])==e['sha256'],'Public asset/helper changed during audit')
 r=dict(status='COMPLETE_SIX_UNIQUE_PACKAGE_ALIASES_REQUIRES_FULLGRAPH_PAD_REVIEW' if complete else 'FAIL',error=error,exit_code=code,elapsed_seconds=time.time()-t,source_board=str(src),source_sha256_before=j['source_sha256'],source_sha256_after=sha(src),public_unchanged=True,guard=str(a.guard),guard_sha256=sha(a.guard),full_public_files_before=before,full_public_files_after=after,manifest=str(a.bundle/'MANIFEST.json'),manifest_sha256=sha(a.bundle/'MANIFEST.json'),runner_sha256=sha(__file__),no_source_or_public_save=True,private_throwaway_input_may_be_dirty=True,existing_PAD_cache_reuse_is_not_public_PAD_manufacturing_proof=True)
 (a.out/'RUN_RECEIPT.json').write_text(json.dumps(r,indent=2),'utf-8');print(json.dumps(r,indent=2));return 0 if complete else 2
if __name__=='__main__':raise SystemExit(main())
