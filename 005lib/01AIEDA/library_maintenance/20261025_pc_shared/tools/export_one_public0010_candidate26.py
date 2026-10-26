"""Readonly feedback for exactly public0010's owned final candidate, source protected."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,time
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');CAD=Path(r'C:\Program0\cadence\SPB172');SOURCE=Path(r'D:\001DIY\005lib\01brdlib\0010.brd');SOURCE_SHA='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898'
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def write(p,x):p.write_text(json.dumps(x,indent=2),encoding='utf-8')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--sha256',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h=a.sha256.upper();need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()),'Fresh owned output required');need(a.candidate.resolve().is_relative_to(M.resolve()) and not a.candidate.resolve().is_relative_to(SOURCE.parent.resolve()),'Only independent0010 maintenance candidate accepted');need(sha(a.candidate)==h and sha(SOURCE)==SOURCE_SHA,'Exact candidate/source SHA protection failed');a.out.mkdir(parents=True);p=a.out/'CANDIDATE0010.brd';shutil.copy2(a.candidate,p);need(not os.path.samefile(p,a.candidate) and sha(p)==h,'Independent byte copy failed');out=a.out/'native_output';out.mkdir()
 for target,config in [('pxlBA.txt','pxlBA_full_component_identity_nobom.txt'),('pxlBA-rfpcb.txt','pxlBA-rfpcb_full_component_identity_nobom.txt')]:shutil.copy2(R/'tools'/config,a.out/target)
 env=os.environ.copy();env['CDSROOT']=str(CAD);env['PATH']=str(CAD/'tools/bin')+';'+env.get('PATH','');cmd=[str(CAD/'tools/bin/genfeedformat.exe'),'-b',str(p),'-o',str(out),'-m','1','-c'];t=time.time()
 with (a.out/'stdout.txt').open('w') as so,(a.out/'stderr.txt').open('w') as se:
  proc=subprocess.Popen(cmd,cwd=a.out,env=env,stdout=so,stderr=se,creationflags=subprocess.CREATE_NO_WINDOW);write(a.out/'owned_process.json',{'pid':proc.pid,'command':cmd})
  try:code=proc.wait(timeout=60)
  except subprocess.TimeoutExpired:proc.kill();proc.wait();raise
 need(code==0 and all((out/f'{k}View.dat').is_file() for k in ['comp','func','pin','net']),'Native feedback incomplete');header=(out/'compView.dat').read_text().splitlines()[0];need(all('!'+k+'!' in header for k in ['COMP_DEVICE_TYPE','COMP_VALUE','COMP_PACKAGE']),'Full identity fields missing');need(sum(l.startswith('S!') for l in (out/'compView.dat').read_text().splitlines())==572,'Full572 components changed');need(sha(p)==sha(a.candidate)==h and sha(SOURCE)==SOURCE_SHA,'Readonly export altered source/candidate')
 r={'status':'PASS_0010_CANDIDATE_READONLY_FRESH_FULL_VIEWS_SEMANTIC_REVIEW_PENDING','source':str(a.candidate),'source_sha256':h,'original_public_source':str(SOURCE),'original_public_source_sha256':SOURCE_SHA,'input_copy':str(p),'input_copy_sha256':sha(p),'command':cmd,'elapsed_seconds':time.time()-t,'native_output':str(out),'files':{str(p):sha(p) for p in out.iterdir() if p.is_file()},'script_sha256':sha(__file__)};write(a.out/'0010_CANDIDATE_GENFEED_READONLY_EXPORT.json',r);print(r['status'])
if __name__=='__main__':main()
