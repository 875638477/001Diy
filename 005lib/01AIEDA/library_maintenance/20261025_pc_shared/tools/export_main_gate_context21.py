"""Two immutable main13 boards: native identity feedback for exact Gate remap only."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,time,argparse
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');CAD=Path(r'C:\Program0\cadence\SPB172')
ROWS=[('source49AF',R/'w/via_alt13/PC13_FINAL.brd','49AF5EE7252CA9E8C4C48D8F60AD4D1113DA559814585356B14F6150A195C063'),('candidateA965',R/'w/all81_full4/INPUT_COPY.brd','A9651E39CBD8DAC0B67566686AF3D2CA38B2AA517C5C1ADCD74E81336D563F51')]
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def write(p,v):p.write_text(json.dumps(v,indent=2),encoding='utf-8')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()),'Fresh owned output required');need(all(sha(p)==h for n,p,h in ROWS),'One of two immutable source boards changed');a.out.mkdir(parents=True);env=os.environ.copy();env['CDSROOT']=str(CAD);env['PATH']=str(CAD/'tools/bin')+';'+env.get('PATH','');rr=[]
 for name,src,h in ROWS:
  d=a.out/name;d.mkdir();dst=d/'native_output';dst.mkdir();p=d/'MAIN_INPUT_COPY.brd';shutil.copy2(src,p);need(sha(p)==h and not os.path.samefile(p,src),'Owned main copy protection failed')
  for f,c in [('pxlBA.txt','pxlBA_full_component_identity_nobom.txt'),('pxlBA-rfpcb.txt','pxlBA-rfpcb_full_component_identity_nobom.txt')]:shutil.copy2(R/'tools'/c,d/f)
  cmd=[str(CAD/'tools/bin/genfeedformat.exe'),'-b',str(p),'-o',str(dst),'-m','1','-c'];t=time.time()
  with (d/'stdout.txt').open('w') as out,(d/'stderr.txt').open('w') as err:
   proc=subprocess.Popen(cmd,cwd=d,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW);write(d/'owned_process.json',{'pid':proc.pid,'command':cmd})
   try:code=proc.wait(timeout=60)
   except subprocess.TimeoutExpired:proc.kill();proc.wait();raise
  need(code==0 and all((dst/f'{k}View.dat').is_file() for k in ['comp','func','pin','net']),'Native full identity feedback failed');need(sha(p)==sha(src)==h,'Readonly main native input changed');count=sum(l.startswith('S!') for l in (dst/'compView.dat').read_text().splitlines());need(count==1066,'Main exact1066 components changed')
  row={'source':str(src),'source_sha256':h,'status':'PASS_NATIVE_READONLY_CONTEXT_EXPORT_NOT_SEMANTIC_ACCEPTANCE','elapsed_seconds':time.time()-t,'command':cmd,'files':{str(f):sha(f) for f in dst.iterdir() if f.is_file()}};write(d/'MAIN_IDENTITY_READONLY_EXPORT.json',row);rr.append(row)
 need(all(sha(p)==h for n,p,h in ROWS),'Two immutable source boards changed');write(a.out/'MAIN_GATE_CONTEXT_READONLY_EXPORT.json',{'status':'PASS_TWO_FROZEN_MAIN_BOARD_CONTEXT_EXPORTS','rows':rr,'script_sha256':sha(__file__)});print('PASS_TWO_FROZEN_MAIN_BOARD_CONTEXT_EXPORTS')
if __name__=='__main__':main()
