"""Run one isolated Capture database SDK job; all files remain in learning."""
import argparse, json, os, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('script');args=p.parse_args()
if not args.id.replace('_','').isalnum():raise ValueError('Invalid id')
script=Path(args.script).resolve()
if not script.is_relative_to(root):raise ValueError('Outside learning')
log=root/'logs/lesson14_capture_20261019/batch'/args.id
log.mkdir(parents=True,exist_ok=False)
env=os.environ.copy();env['PATH']=r'C:\Program0\Cadence\spb172\tools\bin;'+env['PATH'];env['CDSROOT']=r'C:\Program0\Cadence\spb172'
cmd=[r'C:\Program0\Cadence\spb172\tcltk\bin\tclsh.exe',str(root/'scripts/c14_native_batch.tcl'),str(script),str(log/'result.tcldict')]
process=subprocess.Popen(cmd,cwd=log,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
meta={'command':cmd,'pid':process.pid,'status':'running'}
(log/'process.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
try:
    stdout,stderr=process.communicate(timeout=55)
except subprocess.TimeoutExpired:
    process.kill();stdout,stderr=process.communicate();meta['timed_out_after_seconds']=55
(log/'stdout.txt').write_bytes(stdout);(log/'stderr.txt').write_bytes(stderr)
meta.update(status='finished',exit_code=process.returncode)
(log/'process.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'log':str(log),'exit_code':process.returncode},ensure_ascii=False))
if (log/'result.tcldict').exists():print((log/'result.tcldict').read_text(encoding='utf-8'))
sys.exit(0 if process.returncode==0 else 1)
