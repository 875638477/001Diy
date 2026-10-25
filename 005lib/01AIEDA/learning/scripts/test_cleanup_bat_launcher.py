"""Exercise the deployed BAT wrapper with a harmless embedded PowerShell stub.

This is a CMD subprocess test, not an Explorer/GUI double-click test. No EDA
cleanup payload is executed and no files outside this test's fixtures are changed.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time
import winreg
from datetime import datetime, timezone
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "0000Ad_Keil_Cadence_dat_iar_txt.bat"
STAGE = ROOT / "01AIEDA/learning/staging/cleanup_review_20261019/double_click"
RUN = STAGE / ("run_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_") + uuid4().hex[:8])
MARKER = "#__EDA_CLEAN_POWERSHELL__"

STUB = r"""
$ErrorActionPreference='Stop'
Write-Host ('STUB_ROOT=' + $env:EDA_CLEAN_ROOT)
Write-Host ('STUB_SELF=' + $env:EDA_CLEAN_SELF)
Write-Host ('STUB_ARG_1=' + $env:EDA_CLEAN_ARG_1)
Write-Host ('STUB_ARG_2=' + $env:EDA_CLEAN_ARG_2)
if($env:EDA_CLEAN_ARG_1 -eq '/invalid') {
    Write-Host 'STUB_INVALID_OPTION'
    Write-Host 'STUB_READY_FOR_WRAPPER'
    exit 37
}
if($env:EDA_TEST_FORCE_FAILURE -eq '1') {
    Write-Host 'STUB_FORCED_FAILURE'
    Write-Host 'STUB_READY_FOR_WRAPPER'
    exit 23
}
Write-Host 'STUB_READY_FOR_WRAPPER'
exit 0
""".lstrip()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reader(stream, target: bytearray) -> None:
    while True:
        block = stream.read(1)
        if not block:
            return
        target.extend(block)


def read_bat_association() -> list[dict]:
    results = []
    for hive, name, path, value in (
        (winreg.HKEY_CLASSES_ROOT, "HKEY_CLASSES_ROOT", ".bat", ""),
        (winreg.HKEY_CLASSES_ROOT, "HKEY_CLASSES_ROOT", r"batfile\shell\open\command", ""),
        (winreg.HKEY_CURRENT_USER, "HKEY_CURRENT_USER", r"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.bat\UserChoice", "ProgId"),
    ):
        try:
            with winreg.OpenKey(hive, path, 0, winreg.KEY_READ) as key:
                data, kind = winreg.QueryValueEx(key, value)
                results.append({"key": name + "\\" + path, "value": value, "data": data, "kind": kind})
        except FileNotFoundError:
            results.append({"key": name + "\\" + path, "exists": False})
    return results


def run_case(bat: Path, args: list[str], delayed: bool, fail: bool, missing_ps: bool = False) -> dict:
    expected_code = 9009 if missing_ps else 37 if args and args[0] == "/invalid" else 23 if fail else 0
    expected_pause = not args
    env = os.environ.copy()
    env["EDA_TEST_FORCE_FAILURE"] = "1" if fail else "0"
    # Each invocation must replace inherited argument state, including empty slots.
    env["EDA_CLEAN_ARG_1"] = "STALE_ARGUMENT_MUST_NOT_SURVIVE"
    env["EDA_CLEAN_ARG_2"] = "STALE_ARGUMENT_MUST_NOT_SURVIVE"
    if missing_ps:
        # Only this child's environment is changed; no global state or registry
        # is written. The real absolute COMSPEC remains available to launch it.
        env["SYSTEMROOT"] = str(RUN / "missing Windows directory")
    command = '"{}" /d /v:{} /s /c ""{}"{}"'.format(
        env.get("COMSPEC") or str(Path(os.environ["SystemRoot"]) / "System32/cmd.exe"),
        "on" if delayed else "off", bat,
        " " + " ".join(args) if args else "",
    )
    proc = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = bytearray(), bytearray()
    threads = [threading.Thread(target=reader, args=(proc.stdout, stdout), daemon=True),
               threading.Thread(target=reader, args=(proc.stderr, stderr), daemon=True)]
    for thread in threads:
        thread.start()
    paused_before_input = False
    try:
        if expected_pause:
            deadline = time.monotonic() + 20
            ready = b"[Cleanup] FAILED" if missing_ps else b"STUB_READY_FOR_WRAPPER"
            while ready not in stdout and proc.poll() is None and time.monotonic() < deadline:
                time.sleep(0.02)
            assert ready in stdout, ("wrapper did not start", command, bytes(stdout), bytes(stderr))
            # Wait after PowerShell has produced its final line. With stdin still
            # open and empty, a real PAUSE must keep CMD running here.
            time.sleep(0.4)
            paused_before_input = proc.poll() is None
            assert paused_before_input, ("no-argument wrapper exited before input", proc.returncode, bytes(stdout), bytes(stderr))
            proc.stdin.write(b"\r\n")
            proc.stdin.flush()
        proc.wait(timeout=20)
        for thread in threads:
            thread.join(timeout=5)
        output = bytes(stdout).decode("utf-8", errors="strict")
        error = bytes(stderr).decode("utf-8", errors="strict")
        normalized_output = output.replace("\r\n", "\n")
        assert proc.returncode == expected_code, ("exit code changed", proc.returncode, expected_code, output, error)
        if not missing_ps:
            assert "STUB_SELF=" + str(bat) in output, ("path changed", command, output, error)
            assert "STUB_ROOT=" + str(bat.parent) + "\\" in output, ("root changed", command, output, error)
            assert "STUB_ARG_1=" + (args[0] if args else "") + "\n" in normalized_output, ("arg1 changed", output)
            assert "STUB_ARG_2=" + (args[1] if len(args) > 1 else "") + "\n" in normalized_output, ("arg2 changed", output)
        else:
            assert "Windows PowerShell was not found" in output, output
            assert "STUB_READY_FOR_WRAPPER" not in output, output
        assert "STALE_ARGUMENT_MUST_NOT_SURVIVE" not in output, output
        if expected_code:
            assert "FAILED" in output and str(expected_code) in output, ("missing failure result", output)
        else:
            assert "OK" in output, ("missing success result", output)
        if not missing_ps:
            assert "STUB_READY_FOR_WRAPPER" in output, output
        return {"path": str(bat), "args": args, "parent_delayed_expansion": delayed,
                "forced_failure": fail, "exit_code": proc.returncode,
                "powershell_missing_in_child_environment": missing_ps,
                "expected_pause": expected_pause, "paused_before_input": paused_before_input,
                "stdout": output, "stderr": error, "passed": True}
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=10)
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            if stream is not None:
                stream.close()


def run_real_payload_case(bat: Path, preview: bool) -> dict:
    sentinel = bat.parent / "sentinel.log"
    sentinel.write_bytes(b"Test fixture only; not user project data.\r\n")
    sentinel_before = sha(sentinel.read_bytes())
    powershell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
    snapshot = subprocess.run([str(powershell), "-NoLogo", "-NoProfile", "-Command",
        "@(Get-Process -ErrorAction SilentlyContinue | Where-Object {$_.ProcessName -match '^(?i:capture|allegro|pcb_editor|padstack_editor|dxp|x2|altiumdesigner|uv4|iaridepm|iaride|ewb|devenv_iar)$'} | Select-Object -ExpandProperty ProcessName -Unique) | ConvertTo-Json -Compress"],
        capture_output=True, timeout=20, check=True)
    names = json.loads(snapshot.stdout.decode("utf-8")) if snapshot.stdout.strip() else []
    if isinstance(names, str):
        names = [names]
    command = '"{}" /d /v:off /s /c ""{}"{}"'.format(os.environ["COMSPEC"], bat, " /preview" if preview else "")
    proc = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = bytearray(), bytearray()
    threads = [threading.Thread(target=reader, args=(proc.stdout, stdout), daemon=True),
               threading.Thread(target=reader, args=(proc.stderr, stderr), daemon=True)]
    for thread in threads:
        thread.start()
    paused = False
    try:
        if not preview:
            deadline = time.monotonic() + 30
            while b"Press any key to close this window" not in stdout and proc.poll() is None and time.monotonic() < deadline:
                time.sleep(0.02)
            assert b"Press any key to close this window" in stdout, ("real payload pause missing", bytes(stdout), bytes(stderr))
            time.sleep(0.4)
            paused = proc.poll() is None
            assert paused, ("real payload auto-closed", bytes(stdout), bytes(stderr))
            proc.stdin.write(b"\r\n")
            proc.stdin.flush()
        proc.wait(timeout=30)
        for thread in threads:
            thread.join(timeout=5)
        output = bytes(stdout).decode("utf-8", errors="strict")
        error = bytes(stderr).decode("utf-8", errors="strict")
        expected = 0 if preview or not names else 1
        assert proc.returncode == expected, ("unexpected real payload status", expected, proc.returncode, names, output, error)
        if preview or names:
            assert sentinel.exists() and sha(sentinel.read_bytes()) == sentinel_before, ("fixture sentinel unexpectedly changed", output, error)
        else:
            assert not sentinel.exists(), ("fixture-only normal cleanup did not remove sentinel", output, error)
        assert ("[Cleanup] OK" if expected == 0 else "[Cleanup] FAILED") in output, (output, error)
        if preview:
            assert "preview=True" in output and "removed=0;" in output, output
            assert "Press any key to close this window" not in output, output
        elif names:
            assert "running" in (output + error).lower() or "open" in (output + error).lower(), (output, error)
        return {"path": str(bat), "args": ["/preview"] if preview else [], "production_payload": True,
                "process_snapshot": names, "expected_pause": not preview, "paused_before_input": paused,
                "exit_code": proc.returncode, "sentinel_exists_after": sentinel.exists(),
                "sentinel_unchanged": sentinel.exists() and sha(sentinel.read_bytes()) == sentinel_before,
                "only_fixture_can_be_deleted": True, "stdout": output, "stderr": error, "passed": True}
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=10)
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            if stream is not None:
                stream.close()


def main() -> None:
    association_before = read_bat_association()
    original = SOURCE.read_bytes()
    source_text = original.decode("utf-8", errors="strict").replace("\r\n", "\n")
    parts = re.split(r"^" + re.escape(MARKER) + r"\n", source_text, maxsplit=1, flags=re.M)
    assert len(parts) == 2, "independent payload marker missing"
    header = parts[0]
    assert re.search(r"(?im)^\s*pause(?:\s|$)", header), "production header has no PAUSE"
    assert "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" in header, "PowerShell path is not absolute"
    RUN.mkdir(parents=True, exist_ok=False)
    fixtures = [RUN / "normal" / "cleanup.bat", RUN / "\u4e2d\u6587 ! & (\u76ee\u5f55)" / "\u6e05\u7406 ! & (\u5165\u53e3).bat"]
    stub_bytes = (header + MARKER + "\n" + STUB).replace("\n", "\r\n").encode("utf-8")
    for bat in fixtures:
        assert bat.resolve().is_relative_to(RUN.resolve())
        bat.parent.mkdir(parents=True, exist_ok=True)
        bat.write_bytes(stub_bytes)
    results, failures = [], []
    cases = [([], False), ([], True), (["/preview"], False), (["/help"], False),
             (["/invalid"], False), (["/preview", "/history"], False)]
    for bat in fixtures:
        for delayed in (False, True):
            for args, fail in cases:
                try:
                    results.append(run_case(bat, args, delayed, fail))
                except Exception as exc:
                    failures.append({"path": str(bat), "args": args, "parent_delayed_expansion": delayed,
                                     "forced_failure": fail, "error": repr(exc)})
        for args in ([], ["/preview"]):
            try:
                results.append(run_case(bat, args, False, False, missing_ps=True))
            except Exception as exc:
                failures.append({"path": str(bat), "args": args, "powershell_missing_in_child_environment": True,
                                 "error": repr(exc)})
    real_bat = RUN / "real_payload" / "cleanup.bat"
    real_bat.parent.mkdir(parents=True, exist_ok=True)
    real_bat.write_bytes(original)
    for preview in (False, True):
        try:
            results.append(run_real_payload_case(real_bat, preview))
        except Exception as exc:
            failures.append({"path": str(real_bat), "args": ["/preview"] if preview else [], "production_payload": True,
                             "error": repr(exc)})
    assert SOURCE.read_bytes() == original, "production source changed during fixture tests"
    association_after = read_bat_association()
    assert association_after == association_before, "BAT registry association changed"
    report = {"passed": not failures, "checks": len(results) + len(failures), "failures": failures,
              "source": str(SOURCE), "source_sha256": sha(original),
              "header_sha256": sha(original.split(b"\r\n" + MARKER.encode("ascii") + b"\r\n", 1)[0] + b"\r\n"),
              "sourcepayload_sha256": sha((ROOT / "01AIEDA/learning/scripts/eda_cleanup_payload.ps1").read_bytes()),
              "fixture_wrapper_sha256": sha(stub_bytes), "source_unchanged": True,
              "registry_association_read_only": association_before, "registry_association_unchanged": True,
              "test_method": "Windows CMD subprocess with controlled stdin; not an Explorer GUI test",
              "production_cleanup_payload_executed": True, "production_payload_scope": "self-created fixture only",
              "real_user_cleanup_executed": False,
              "results": results}
    (RUN / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (STAGE / "launcher_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "checks": report["checks"], "failures": len(failures),
                      "results": str(RUN / "results.json"), "real_user_cleanup_executed": False}, ensure_ascii=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
