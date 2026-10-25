from pathlib import Path
from datetime import datetime, timezone, timedelta
import json, shutil, subprocess, time

root = Path(__file__).resolve().parents[1]
log = root / 'logs/capture_C_20261019/gui_probe'
log.mkdir(parents=True, exist_ok=True)
exe = Path(r'C:\Program0\Cadence\spb172\tools\bin\Capture.exe')
ini = log / 'capture.ini'
if not ini.exists():
    shutil.copy2(exe.parent/'CAPTURE.INI', ini)
args = [str(exe), '-lite', '-i', str(ini), str(root/'scripts/c11_gui_boot_probe.tcl')]
startup = subprocess.STARTUPINFO()
startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startup.wShowWindow = 0
with (log/'stdout.txt').open('ab') as out, (log/'stderr.txt').open('ab') as err:
    process = subprocess.Popen(args, cwd=log, stdout=out, stderr=err,
                               startupinfo=startup, creationflags=subprocess.CREATE_NO_WINDOW)
record = dict(pid=process.pid, args=args, started_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
              scope='owned isolated blank startup; no user design')
(log/'launch.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
for i in range(20):
    if (log/'boot.tcldict').exists() or process.poll() is not None:
        break
    time.sleep(1)
record.update(exit_code=process.poll(), boot_probe_completed=(log/'boot.tcldict').exists())
(log/'launch.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
print(json.dumps(record))
