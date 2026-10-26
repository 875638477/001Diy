"""Owned fresh readonly full feedback from one independent0010 candidate."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,time
M=Path(__file__).resolve().parent
R=Path('D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025')
CAD=Path('C:/Program0/cadence/SPB172')
PUBLIC=Path('D:/001DIY/005lib/01brdlib/0010.brd')
OLD='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def need(v,m):
    if not v:raise ValueError(m)
def write(p,q):p.write_text(json.dumps(q,indent=2),encoding='utf-8')
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=Path,required=True);ap.add_argument('--sha256',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(a.input.resolve().is_relative_to(M.resolve()) and sha(a.input)==a.sha256 and sha(PUBLIC)==OLD,'Frozen candidate/public input failed')
    need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()),'Fresh owned maintenance output required');a.out.mkdir(parents=True)
    copy=a.out/'0010.brd';shutil.copy2(a.input,copy);need(not os.path.samefile(a.input,copy) and sha(copy)==a.sha256,'Independent exact copy failed')
    dest=a.out/'native_output';dest.mkdir();configs=[]
    for name,source in [('pxlBA.txt',R/'tools/pxlBA_full_component_identity_nobom.txt'),('pxlBA-rfpcb.txt',R/'tools/pxlBA-rfpcb_full_component_identity_nobom.txt')]:
        need(not source.read_bytes().startswith(b'\xef\xbb\xbf'),'Native extract BOM forbidden');shutil.copy2(source,a.out/name);configs.append(dict(path=str(source),sha256=sha(source)))
    cmd=[str(CAD/'tools/bin/genfeedformat.exe'),'-b',str(copy),'-o',str(dest),'-m','1','-c'];env=os.environ.copy();env['CDSROOT']=str(CAD);env['PATH']=str(CAD/'tools/bin')+';'+env.get('PATH','');start=time.time()
    with (a.out/'stdout.txt').open('w',encoding='utf-8') as so,(a.out/'stderr.txt').open('w',encoding='utf-8') as se:
        p=subprocess.Popen(cmd,cwd=a.out,env=env,stdout=so,stderr=se,creationflags=subprocess.CREATE_NO_WINDOW);write(a.out/'owned_process.json',dict(pid=p.pid,command=cmd,start_epoch=start))
        try:code=p.wait(timeout=90)
        except subprocess.TimeoutExpired:p.kill();p.wait();raise
    need(code==0,'Owned native process failed')
    names=['compView.dat','funcView.dat','netView.dat','pinView.dat','chipsView.dat','cmdbView.dat'];need(all((dest/n).is_file() for n in names),'Incomplete actual native views')
    lines=(dest/'compView.dat').read_text('utf-8-sig').splitlines();need(sum(l.startswith('S!') for l in lines)==572,'Expected all572 actual source components');need(all('!'+f+'!' in lines[0] for f in ['COMP_DEVICE_TYPE','COMP_VALUE','COMP_PACKAGE']),'Native omitted full component identity fields')
    need(sha(a.input)==sha(copy)==a.sha256 and sha(PUBLIC)==OLD,'Readonly native source/public binding failed')
    result=dict(status='PASS_FRESH_0010_FULL_NATIVE_FEEDBACK_READONLY_SEMANTICS_PENDING',source=str(a.input),source_sha256=a.sha256,protected_public_original=str(PUBLIC),protected_public_original_sha256=OLD,native_output=str(dest),declared_components=572,exit_code=code,elapsed_seconds=time.time()-start,configs=configs,files={n:dict(path=str(dest/n),sha256=sha(dest/n),bytes=(dest/n).stat().st_size) for n in names},runner_sha256=sha(__file__),public_files_written=0)
    write(a.out/'CANDIDATE_GENFEED_READONLY_RESULT.json',result);print(json.dumps(dict(status=result['status'],output=str(a.out))))
if __name__=='__main__':main()
