"""Native Capture PST -> native BRD -> ECO -> native VIEW/SWP with readback.

Only copies of supplied DSNs are netlisted. Existing output directories are refused.
The schematic GUI/ERC and SWP application are separate, explicitly unverified steps.
"""
import argparse,csv,hashlib,json,pathlib,re,shutil,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];CLI=ROOT/'scripts/de_native_cli.py'
p=argparse.ArgumentParser();p.add_argument('--baseline',required=True);p.add_argument('--eco',required=True);p.add_argument('--out',required=True)
a=p.parse_args();baseline=pathlib.Path(a.baseline).resolve();eco=pathlib.Path(a.eco).resolve();out=pathlib.Path(a.out).resolve();LIB=ROOT/'examples/de_15_26_20261019/library'
for path in [baseline,eco,out]:assert path.is_relative_to(ROOT)
assert baseline.is_file() and eco.is_file() and not out.exists()
out.mkdir();(out/'logs').mkdir()
cfg=out/'allegro.cfg';shutil.copy2(pathlib.Path(r'C:\Program0\Cadence\spb172\tools\capture\allegro.cfg'),cfg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputHashes={str(p):sha(p) for p in [baseline,eco]}
def run(name,exe,args,complete=None):
    log=out/'logs'/name
    result=subprocess.run([sys.executable,str(CLI),'--log',str(log),'--library',str(LIB),'--timeout','40',exe,*map(str,args)],capture_output=True)
    (out/'logs'/(name+'_driver.txt')).write_bytes(result.stdout+result.stderr)
    record=json.loads((log/'launch.json').read_text())
    assert record['completed'] and record['exitCode']==0,(name,record)
    stdout=(log/'stdout.txt').read_text(errors='replace')
    assert not re.search(r'(?:ERROR\(|\*Error\*|unclosed on EOF|ASSERT|FATAL)',stdout,re.I),(name,stdout)
    if complete:assert complete in stdout,(name,'missing completion marker')
    return log
def readboard(name,board):
    report=out/name;report.mkdir();scr=out/(name+'.scr')
    scr.write_text('set NOCONFIRM\nskill errset(load("'+(ROOT/'scripts/de_board_read.il').as_posix()+'") t)\nskill errset(deBoardRead("'+report.as_posix()+'") t)\nquit\nfillin "yes"\n',encoding='ascii')
    before=sha(board)
    run(name,'allegro.exe',['-product','Allegro_performance','-safe','-nographic','-readonly','-s',scr,board])
    assert before==sha(board),'readonly changed database'
    assert 'DE_BOARD_READ_COMPLETE' in (report/'native_summary.txt').read_text()
    return report
sources={};netdirs={}
for name,source in [('baseline',baseline),('eco',eco)]:
    folder=out/name;folder.mkdir();dsn=folder/'DE_CONTROL.dsn';shutil.copy2(source,dsn);sources[name]=dsn
    netlist=folder/'netlist';netlist.mkdir();netdirs[name]=netlist
    run('pst_'+name,'pstswp.exe',['-pst','-d',dsn,'-n',netlist,'-c',cfg,'-v','3','-l','255','-j','PCB Footprint'],'packaging the design view')
    for f in ['pstchip.dat','pstxprt.dat','pstxnet.dat']:assert (netlist/f).stat().st_size>0
basebrd=out/'DE_BASELINE.brd';ecobrd=out/'DE_ECO.brd'
run('import_baseline','netrev.exe',['-n','-e','-i',netdirs['baseline'],basebrd],'saved to disk')
baseRead=readboard('baseline_readback',basebrd)
run('import_eco','netrev.exe',['-e','-i',netdirs['eco'],basebrd,ecobrd],'saved to disk')
ecoRead=readboard('eco_readback',ecobrd)
feedback=out/'feedback';feedback.mkdir()
for name in ['pstchip.dat','pstxprt.dat','pstxnet.dat']:shutil.copy2(netdirs['eco']/name,feedback/name)
if (netdirs['eco']/'pxlBA.txt').is_file():shutil.copy2(netdirs['eco']/'pxlBA.txt',ecobrd.parent/'pxlBA.txt')
run('feedback_view','genfeedformat.exe',['-x','-b',ecobrd,'-o',feedback],'execution completed')
for name in ['compView.dat','funcView.dat','netView.dat','pinView.dat']:assert (feedback/name).stat().st_size>0
swp=feedback/'DE_ECO.swp'
run('feedback_swp','pstswp.exe',['-swp','-d',sources['eco'],'-n',feedback,'-s',swp,'-c',cfg,'-hpath','HPathForCollision','-backwd'],'Exiting the Swp file dumping process')
assert swp.is_file()
for path,expected in inputHashes.items():assert sha(pathlib.Path(path))==expected,'source DSN changed'
result={'status':'NATIVE_FLOW_CREATED_PENDING_INDEPENDENT_COMPARE','originalDsnHashesUnchanged':inputHashes,'baselineBoard':str(basebrd),'ecoBoard':str(ecobrd),'baselineReadback':str(baseRead),'ecoReadback':str(ecoRead),'feedbackSwap':str(swp),'limitations':['Capture GUI ERC not run.','SWP generation is verified; applying SWP inside Capture GUI is not verified.','BRD imports contain unplaced components; no layout/routing/manufacturing signoff is claimed.'],'files':[{'path':str(p),'sha256':sha(p)} for p in [basebrd,ecobrd,swp]]}
(out/'flow_result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(result,indent=2))
