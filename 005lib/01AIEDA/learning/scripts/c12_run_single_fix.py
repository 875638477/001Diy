"""Build single-unit revision, then reopen it in a separate native process."""
import csv
import hashlib
import json
import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
log = root / "logs" / "capture_C_20261019"
example = root / "examples" / "lesson12_capture"
report_path = log / "c12_single_fix_validation.json"
if report_path.exists():
    raise SystemExit("Single-fix experiment already recorded; refusing overwrite")
install = Path(r"C:\Program0\Cadence\spb172")
env = os.environ.copy()
env["CDSROOT"] = str(install)
env["PATH"] = str(install / "tools" / "bin") + os.pathsep + env.get("PATH", "")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest().upper()
old_libraries = [example / n for n in ("c12_qmi8610.olb", "c12_qmi8610_spi4.olb")]
old_before = {str(p): sha(p) for p in old_libraries}
runs = []
for label, script in [("create", "c12_build_single_fix.tcl"), ("fresh_reopen", "c12_reopen_single_fix.tcl")]:
    command = [str(install / "tcltk" / "bin" / "tclsh.exe"), str(root / "scripts" / script)]
    completed = subprocess.run(command, cwd=log, env=env, capture_output=True, timeout=45)
    (log / f"c12_single_{label}_stdout.txt").write_bytes(completed.stdout)
    (log / f"c12_single_{label}_stderr.txt").write_bytes(completed.stderr)
    runs.append({"label": label, "command": command, "returncode": completed.returncode, "waited_to_exit": True})
    if completed.returncode:
        raise SystemExit(f"Native {label} failed with {completed.returncode}; review saved logs")

comparisons = []
for old_dir, new_dir in [("c12_i2c_verified", "c12_single_fresh_i2c"), ("c12_spi4_verified", "c12_single_fresh_spi4")]:
    for filename in ["c12_pins.tsv", "c12_vectors.tsv", "c12_display_properties.tsv", "c12_readback_result.tcldict"]:
        comparisons.append({"file": f"{new_dir}/{filename}", "unchanged_vs_first_symbol": (log / old_dir / filename).read_bytes() == (log / new_dir / filename).read_bytes()})
    def props(folder):
        with (log / folder / "c12_properties.tsv").open(encoding="utf-8", newline="") as stream:
            return {r["property"]: r["value"] for r in csv.DictReader(stream, delimiter="\t")}
    old, new = props(old_dir), props(new_dir)
    expected = dict(old, **{"Symbol Revision": "C12_REV2_SINGLE"})
    comparisons.append({"file": f"{new_dir}/c12_properties.tsv", "only_expected_revision_change": new == expected})
old_after = {str(p): sha(p) for p in old_libraries}
new_libraries = [example / n for n in ("c12_qmi8610_single.olb", "c12_qmi8610_spi4_single.olb")]
new_names = {p.name.lower() for p in new_libraries}
locks = [str(p) for p in example.iterdir()
         if any(p.name.lower() in {name + "lck", name + ".lck"} for name in new_names)]
ok = all(v for c in comparisons for k, v in c.items() if k != "file") and old_before == old_after and not locks
report = {"date_asia_shanghai": "2026-10-19", "status": "PASS" if ok else "FAIL", "runs": runs,
          "old_libraries_unchanged": old_before == old_after, "old_library_hashes": old_after,
          "new_library_hashes": {str(p): sha(p) for p in new_libraries}, "comparisons": comparisons,
          "lockfiles_after": locks, "lock_check_scope": "New single libraries only; matches .OLBlck and .OLB.lck names case-insensitively",
          "suffix_check": "Native fresh-process GetDesignator empty assertion passed; see c12_single_freshprocess_result.tcldict"}
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "report": str(report_path), "new_libraries": [str(p) for p in new_libraries]}, ensure_ascii=True))
raise SystemExit(not ok)
