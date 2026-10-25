"""Run one read-only native Cadence Tclsh child; keep all logs in learning."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
log = root / "logs" / "capture_C_20261019"
if (log / "c12_freshprocess_launch.json").exists():
    raise SystemExit("Fresh-process experiment already recorded; refusing to overwrite. Review its logs instead.")
install = Path(r"C:\Program0\Cadence\spb172")
libraries = [root / "examples" / "lesson12_capture" / name for name in ("c12_qmi8610.olb", "c12_qmi8610_spi4.olb")]
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest().upper()
before = {str(path): sha(path) for path in libraries}
env = os.environ.copy()
env["CDSROOT"] = str(install)
env["PATH"] = str(install / "tools" / "bin") + os.pathsep + env.get("PATH", "")
command = [str(install / "tcltk" / "bin" / "tclsh.exe"), str(root / "scripts" / "c12_fresh_process_read.tcl")]
completed = subprocess.run(command, cwd=log, env=env, capture_output=True, timeout=45)
(log / "c12_freshprocess_stdout.txt").write_bytes(completed.stdout)
(log / "c12_freshprocess_stderr.txt").write_bytes(completed.stderr)
after = {str(path): sha(path) for path in libraries}
names = {path.name.lower() for path in libraries}
locks = [path for path in (root / "examples" / "lesson12_capture").iterdir()
         if any(path.name.lower() in {name + "lck", name + ".lck"} for name in names)]
report = {"command": command, "returncode": completed.returncode, "child_waited_to_exit": True,
          "native_library_hashes_before": before, "native_library_hashes_after": after,
          "native_libraries_unchanged": before == after, "library_lockfiles_after": [str(p) for p in locks],
          "stdout": str(log / "c12_freshprocess_stdout.txt"), "stderr": str(log / "c12_freshprocess_stderr.txt")}
(log / "c12_freshprocess_launch.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=True))
raise SystemExit(completed.returncode or int(before != after) or int(bool(locks)))
