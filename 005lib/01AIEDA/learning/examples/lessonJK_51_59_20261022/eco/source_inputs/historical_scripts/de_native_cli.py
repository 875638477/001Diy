"""Run an owned Cadence batch command with isolated output and bounded lifetime."""
import argparse, datetime, json, os, pathlib, subprocess, sys, re
from de_skill_syntax import validate_skill

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIN=pathlib.Path(r'C:\Program0\Cadence\spb172\tools\bin')
p=argparse.ArgumentParser()
p.add_argument('--log',required=True)
p.add_argument('--timeout',type=int,default=45)
p.add_argument('--library')
p.add_argument('executable',choices=['pstswp.exe','netrev.exe','netin.exe','extracta.exe','allegro.exe','padstack_editor.exe','genfeedformat.exe','tclsh.exe'])
p.add_argument('arguments',nargs=argparse.REMAINDER)
a=p.parse_args()
if a.executable=='allegro.exe' and '-s' in a.arguments:
    scr=pathlib.Path(a.arguments[a.arguments.index('-s')+1]).resolve()
    assert scr.is_file() and scr.is_relative_to(ROOT)
    for source in re.findall(r'load\("([^"]+)"\)',scr.read_text(encoding='utf-8')):
        source=pathlib.Path(source).resolve()
        assert source.is_file() and source.is_relative_to(ROOT)
        validate_skill(source.read_text(encoding='utf-8'))
log=pathlib.Path(a.log).resolve()
assert log.is_relative_to(ROOT)
log.mkdir(parents=True,exist_ok=False)
(log/'temp').mkdir()
env=os.environ.copy()
env['PATH']=str(BIN)+os.pathsep+env.get('PATH','')
env['CDSROOT']=str(BIN.parents[1])
env['TEMP']=env['TMP']=str(log/'temp')
env['ALLEGRO_PCBENV']=str(log/'pcbenv')
(log/'pcbenv').mkdir()
if a.library:
    library=pathlib.Path(a.library).resolve()
    assert library.is_dir() and library.is_relative_to(ROOT)
    (log/'pcbenv'/'env').write_text('source $TELENV\nset psmpath = '+library.as_posix()+'\nset padpath = '+library.as_posix()+'\n',encoding='ascii')
si=subprocess.STARTUPINFO(); si.dwFlags|=subprocess.STARTF_USESHOWWINDOW; si.wShowWindow=0
exe=BIN.parents[1]/'tcltk/bin/tclsh.exe' if a.executable=='tclsh.exe' else BIN/a.executable
args=[str(exe),*a.arguments]
record={'args':args,'startUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
    proc=subprocess.Popen(args,cwd=log,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
    record['pid']=proc.pid
    try:
        record['exitCode']=proc.wait(timeout=a.timeout); record['completed']=True
    except subprocess.TimeoutExpired:
        proc.terminate(); record['exitCode']=proc.wait(timeout=10); record['completed']=False;record['ownedProcessTerminated']=True
record['endUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(log/'launch.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(record,indent=2))
for name in ['stdout.txt','stderr.txt']:
    print(name+': '+(log/name).read_text(encoding='utf-8',errors='replace')[-12000:])
