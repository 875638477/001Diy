"""Run one isolated Capture Tcl job; record only its owned process and outputs.

No global process control. Caller must pass a fresh job directory.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest().upper()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cadence-root', type=Path, required=True)
    parser.add_argument('--job-dir', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=240)
    parser.add_argument('--protect', type=Path, action='append', default=[])
    parser.add_argument('script', type=Path)
    parser.add_argument('args', nargs='*')
    args = parser.parse_args()
    args.job_dir.mkdir(parents=True, exist_ok=False)
    before = {str(p.resolve()): digest(p) for p in args.protect}
    env = os.environ.copy()
    env['CDSROOT'] = str(args.cadence_root)
    env['PATH'] = str(args.cadence_root / 'tools/bin') + ';' + env.get('PATH', '')
    command = [str(args.cadence_root / 'tools/bin/tclsh.exe'), str(args.script), *args.args]
    started = time.time()
    with (args.job_dir / 'console.txt').open('w', encoding='utf-8') as output:
        process = subprocess.Popen(command, cwd=args.job_dir, env=env,
            stdout=output, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        (args.job_dir / 'owned_process.json').write_text(json.dumps(
            {'pid': process.pid, 'start_epoch': started, 'command': command}, indent=2), encoding='utf-8')
        try:
            code = process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            code = process.wait()
            status = 'TIMEOUT_OWNED_PROCESS_TERMINATED'
        else:
            status = 'COMPLETE' if code == 0 else 'FAILED'
    after = {str(p.resolve()): digest(p) for p in args.protect}
    result = {'status': status, 'exit_code': code, 'elapsed_seconds': round(time.time()-started, 2),
              'protected_before': before, 'protected_after': after, 'protected_unchanged': before == after}
    (args.job_dir / 'job_result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))
    if code or before != after:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
