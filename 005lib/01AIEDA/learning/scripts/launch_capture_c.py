"""Launch an owned Capture 17.2 lesson process with an isolated INI and cwd."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib, json, os, shutil, subprocess, time

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / 'logs/capture_C_20261019/runtime'
LOG.mkdir(parents=True, exist_ok=True)
exe = Path(r'C:\Program0\Cadence\spb172\tools\bin\Capture.exe')
script = ROOT / 'scripts/c11_capture_runtime.tcl'
ini = LOG / 'capture.ini'
if not ini.exists():
    shutil.copy2(exe.parent / 'CAPTURE.INI', ini)
args = [str(exe), '-product=OrCAD Capture CIS', '-i', str(ini), str(script)]
startup = subprocess.STARTUPINFO()
startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startup.wShowWindow = 0
with (LOG/'stdout.txt').open('ab') as out, (LOG/'stderr.txt').open('ab') as err:
    proc = subprocess.Popen(args, cwd=LOG, stdout=out, stderr=err,
                            startupinfo=startup, creationflags=subprocess.CREATE_NO_WINDOW)
record = {'started_at': datetime.now(timezone(timedelta(hours=8))).isoformat(),
          'pid': proc.pid, 'args': args, 'script_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
          'scope': 'owned isolated lesson process; no user design supplied'}
(LOG/'launch.json').write_text(json.dumps(record, ensure_ascii=True, indent=2), encoding='utf-8')
for _ in range(25):
    if (LOG/'ready.tcldict').exists() or proc.poll() is not None:
        break
    time.sleep(1)
record['poll_exit_code'] = proc.poll()
record['ready_exists'] = (LOG/'ready.tcldict').exists()
(LOG/'launch.json').write_text(json.dumps(record, ensure_ascii=True, indent=2), encoding='utf-8')
print(json.dumps(record, ensure_ascii=True))
if record['ready_exists']:
    print((LOG/'ready.tcldict').read_text(encoding='utf-8'))
