"""Sequential owned readonly all-reference inventory for the seven public BRDs.
Root owns native CAD scheduling; this runner starts only when explicitly invoked.
"""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,time
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');PUBLIC=Path(r'D:\001DIY\005lib\01brdlib');NAMES=('00012.brd','0010.brd','002.brd','004.brd','006.brd','008.brd','VCU16.brd')
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,indent=2),encoding='utf-8')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--guard',type=Path,required=True);ap.add_argument('--guard-sha256',required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--board',choices=NAMES,action='append',default=[]);a=ap.parse_args();need(sha(a.guard)==a.guard_sha256.upper(),'Explicit final public guard SHA changed');guard=load(a.guard);files=guard['files'];index={str(Path(r['path']).resolve()).casefold():r for r in files};need(len(index)==len(files),'Duplicate public guard path');expected={n:index[str((PUBLIC/n).resolve()).casefold()]['sha256'] for n in NAMES}
 need(all(sha(PUBLIC/n)==h for n,h in expected.items()),'One of seven public BRDs differs from exact guard');need(not a.out.exists() and a.out.resolve().is_relative_to((M/'w').resolve()),'Fresh maintenance/w output required');a.out.mkdir(parents=True);rows=[];helper=M/'tools/public_all_reference_inventory27.il';wrapper=M/'Invoke-PublicNativeLocal.ps1';selected=[n for n in NAMES if not a.board or n in a.board]
 for i,n in enumerate(selected,1):
  d=a.out/(str(i).zfill(2)+'_'+Path(n).stem);cmd=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(wrapper),'-InputBoard',str(PUBLIC/n),'-OutputDirectory',str(d),'-SkillFile',str(helper),'-Expression','pub27AllReferenceInventory','-TimeoutSeconds','180'];t=time.time();p=subprocess.run(cmd,capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW);row={'source':str(PUBLIC/n),'source_sha256':expected[n],'native_dir':str(d),'status':'FAIL_NATIVE_REFERENCE_INVENTORY','elapsed_seconds':time.time()-t,'wrapper_exit_code':p.returncode};(a.out/(Path(n).stem+'_wrapper_stdout.txt')).write_text(p.stdout);(a.out/(Path(n).stem+'_wrapper_stderr.txt')).write_text(p.stderr)
  try:
   need(p.returncode==0,'Native wrapper failed');j=load(d/'launch_report.json');need(j['source_sha256_before']==j['source_sha256_after']==j['staged_sha256']==sha(d/'INPUT_COPY.brd')==expected[n] and j['input_unchanged'] and j['write_candidate'] is False and j['exit_code']==0 and '-readonly' in j['arguments'],'Native readonly/source binding failed');need(sha(j['script'])==j['script_sha256']==sha(helper),'Executed inventory helper changed');marker=(d/'ALL_NATIVE_REFERENCE_INVENTORY_COMPLETE.txt').read_text();need(marker.startswith('COMPLETE_ALL_COMPONENTS_INCLUDING_UNPLACED_ALL_SYMBOLS_ALL_SAVED_SYMDEFS\n'),'Complete native source-class marker missing')
   for f,counter,header in [('ALL_COMPONENT_PACKAGE_REFERENCES.tsv','COMPONENTS','refdes\tdevice_type\tpackage\tplaced'),('ALL_SYMBOL_NAME_DEFINITION_REFERENCES.tsv','SYMBOLS','symbol_name\tdefinition_name\trefdes\tobjType'),('ALL_PACKAGE_DEFINITIONS.tsv','DEFINITIONS','name\tobjType\tusedCount')]:
    lines=(d/f).read_text().splitlines();need(lines and lines[0]==header,'Complete exact native field headers missing '+f);count=next(int(l.split('=')[1]) for l in marker.splitlines() if l.startswith(counter+'='));need(len(lines)-1==count,'Native complete count/actual rows differ '+f)
   need('*Error*' not in (d/'stdout.txt').read_text(),'Native inner error');row.update({'status':'PASS_COMPLETE_NATIVE_REFERENCE_INVENTORY_NO_SEMANTIC_DESIGN_CHANGES','evidence':{str(f):sha(f) for f in [d/'launch_report.json',d/'ALL_NATIVE_REFERENCE_INVENTORY_COMPLETE.txt',d/'ALL_COMPONENT_PACKAGE_REFERENCES.tsv',d/'ALL_SYMBOL_NAME_DEFINITION_REFERENCES.tsv',d/'ALL_PACKAGE_DEFINITIONS.tsv']}})
  except Exception as ex:row['error']=str(ex)
  rows.append(row);write(a.out/(Path(n).stem+'_INVENTORY_RESULT.json'),row);need(all(sha(PUBLIC/name)==h for name,h in expected.items()),'One of seven public BRDs changed during inventory')
  if not row['status'].startswith('PASS'):break
 result={'status':'PASS_ALL_SELECTED_PUBLIC_BRD_NATIVE_REFERENCE_INVENTORIES' if len(rows)==len(selected) and all(r['status'].startswith('PASS') for r in rows) else 'FAIL_PUBLIC_BRD_REFERENCE_INVENTORY','guard':str(a.guard),'guard_sha256':sha(a.guard),'all_seven_expected_source_shas':expected,'selected':selected,'rows':rows,'script_sha256':sha(__file__),'CAD_writes_public_files':0};write(a.out/'PUBLIC_BRD_COMPLETE_REFERENCE_INVENTORY_BATCH.json',result);print(json.dumps({'status':result['status'],'rows':[{'source':r['source'],'status':r['status'],'error':r.get('error')} for r in rows]}));return 0 if result['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
