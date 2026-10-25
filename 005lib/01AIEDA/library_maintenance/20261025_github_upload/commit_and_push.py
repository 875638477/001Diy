"""Commit a verified library snapshot and push without replacing remote history."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone

TASK = Path(__file__).resolve().parent
REPO = TASK / "repository"
SOURCE_LOG = Path(r"D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_github_upload")
REL_LOG = Path("01AIEDA/library_maintenance/20261025_github_upload")
GIT = TASK / "tools/mingit/cmd/git.exe"
GH = TASK / "tools/gh/bin/gh.exe"
DIRS = ["01aeLib", "01AIEDA", "01brdlib", "01captureLib", "01env", "01Pad_lib", "01Psm_lib", "01script_file", "01_3d_step_lib"]
BASE = "6e478a7603b6adbe790ea0ad0409fba48ca27e43"


def git(*args: str, network: bool = False) -> bytes:
    cmd = [str(GIT), "-c", f"safe.directory={REPO.as_posix()}", "-c", "core.longpaths=true", "-c", "core.autocrlf=false"]
    if network:
        cmd += ["-c", "http.proxy=http://127.0.0.1:7890", "-c", "http.version=HTTP/1.1",
                "-c", "credential.helper=", "-c", f"credential.helper=!{GH.as_posix()} auth git-credential"]
    cmd += ["-C", str(REPO), *args]
    env = os.environ.copy()
    env["PATH"] = str(GIT.parent) + os.pathsep + env.get("PATH", "")
    env["GIT_TERMINAL_PROMPT"] = "0"
    if network:
        env["HTTPS_PROXY"] = env["HTTP_PROXY"] = "http://127.0.0.1:7890"
    result = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(f"git {args[0]} failed: " + result.stderr.decode("utf-8", "replace")[-6000:])
    return result.stdout


def write_both(name: str, data: dict) -> None:
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    (SOURCE_LOG / name).write_bytes(raw)
    (REPO / REL_LOG / name).write_bytes(raw)
    (TASK / name).write_bytes(raw)


def blob_sha(path: Path) -> str:
    obj = hashlib.sha1(f"blob {path.stat().st_size}\0".encode())
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            obj.update(block)
    return obj.hexdigest()


def verify_entire_index(expected: dict[str, str]) -> None:
    policy = json.loads((SOURCE_LOG / "mirror_policy.json").read_text(encoding="utf-8"))
    deletions = {entry["path"] for entry in policy["remote_deletions"]}
    assert deletions == {"README.md"}, "Review any new remote deletion separately."
    outside_base = {}
    for entry in git("ls-tree", "-r", "-z", BASE).split(b"\0"):
        if entry:
            attrs, raw_path = entry.split(b"\t", 1)
            path = raw_path.decode("utf-8")
            mode, kind, oid = attrs.decode().split()
            if path.split("/", 1)[0] not in DIRS and path not in deletions:
                outside_base[path] = (mode, oid)
    indexed, outside_index = {}, {}
    for entry in git("ls-files", "-s", "-z").split(b"\0"):
        if not entry:
            continue
        attrs, raw_path = entry.split(b"\t", 1)
        path = raw_path.decode("utf-8")
        mode, oid, stage = attrs.decode("ascii").split()
        assert stage == "0", (path, stage)
        if path.split("/", 1)[0] in DIRS:
            assert mode == "100644", (path, mode)
            indexed[path] = oid
        else:
            outside_index[path] = (mode, oid)
    assert outside_base == outside_index, "Directory-external index changes exceed the user's exact mirror deletion plan."
    mismatch = [path for path in expected if indexed.get(path) != expected[path]]
    unexpected = sorted(set(indexed) - set(expected))
    if mismatch or unexpected:
        raise RuntimeError(json.dumps({"mismatch_count": len(mismatch), "unexpected_count": len(unexpected), "examples": (mismatch + unexpected)[:20]}))


def prepare() -> None:
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert json.loads((SOURCE_LOG / "snapshot_verification.json").read_text(encoding="utf-8"))["status"].startswith("PASS")
    shutil.copy2(__file__, SOURCE_LOG / Path(__file__).name)
    shutil.copy2(__file__, REPO / REL_LOG / Path(__file__).name)
    manifest = SOURCE_LOG / "upload_manifest.csv"
    with manifest.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    # Column names are checked explicitly after the independent snapshot script is reviewed.
    path_key = "repository_relative"
    hash_key = "git_blob_sha1"
    if path_key not in rows[0]:
        raise RuntimeError(f"Review manifest columns before staging: {list(rows[0])}")
    expected = {row[path_key]: row[hash_key] for row in rows}
    for name in ("upload_manifest.csv", "snapshot_verification.json", Path(__file__).name):
        path = REPO / REL_LOG / name
        expected[path.relative_to(REPO).as_posix()] = blob_sha(path)
    git("add", "-f", "--", *DIRS)
    git("add", "-u", "--", "README.md")
    verify_entire_index(expected)
    proof = {
        "status": "PASS_GIT_INDEX_MATCHES_SOURCE_SNAPSHOT",
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "library_file_count_before_this_report": len(expected),
        "manifest_rows": len(rows),
        "every_index_blob_matches_source_content_hash": True,
        "directory_external_index_entries_match_base_except_authorized_deletions": True,
        "authorized_remote_deletions": ["README.md"],
        "source_directories": DIRS,
        "remote_repository": "https://github.com/875638477/005lib",
        "base_commit": BASE,
        "scope": "Manifest entries plus the manifest, snapshot report and this runner; this report is added after verification.",
        "large_backup_zip": "Removed after every original passed SHA256, as requested by user.",
    }
    write_both("git_index_verification.json", proof)
    git("add", "-f", "--", (REL_LOG / "git_index_verification.json").as_posix())
    expected[(REL_LOG / "git_index_verification.json").as_posix()] = blob_sha(SOURCE_LOG / "git_index_verification.json")
    verify_entire_index(expected)
    git("commit", "-m", "Synchronize local 01 library folders and remove obsolete remote files")
    head = git("rev-parse", "HEAD").decode().strip()
    tree = git("rev-parse", "HEAD^{tree}").decode().strip()
    result = {"status": "PASS_COMMIT_READY", "commit": head, "tree": tree, "base_commit": BASE,
              "library_files": len(expected), "directories": DIRS,
              "object_statistics": git("count-objects", "-vH").decode().strip()}
    (TASK / "commit_preparation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SOURCE_LOG / "commit_preparation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False), flush=True)


def push() -> None:
    proof = json.loads((TASK / "commit_preparation.json").read_text(encoding="utf-8"))
    head = git("rev-parse", "HEAD").decode().strip()
    assert proof["commit"] == head
    remote = git("ls-remote", "origin", "refs/heads/main", network=True).decode().split()[0]
    if remote != BASE:
        raise RuntimeError("Remote main changed; reconcile it before pushing.")
    output = git("push", "origin", "HEAD:refs/heads/main", network=True).decode("utf-8", "replace")
    after = git("ls-remote", "origin", "refs/heads/main", network=True).decode().split()[0]
    assert after == head
    git("fetch", "origin", "main", network=True)
    fetched = git("rev-parse", "origin/main").decode().strip()
    assert fetched == head
    api_env = os.environ.copy()
    api_env["HTTPS_PROXY"] = api_env["HTTP_PROXY"] = "http://127.0.0.1:7890"
    api_env["PATH"] = str(GIT.parent) + os.pathsep + api_env.get("PATH", "")
    def api(path: str):
        response = subprocess.run([str(GH), "api", path], env=api_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return json.loads(response.stdout)
    contents = api("repos/875638477/005lib/contents?ref=main")
    assert len(contents) == 9 and all(item["type"] == "dir" for item in contents)
    assert sorted(item["name"] for item in contents) == sorted(DIRS)
    server_commit = api(f"repos/875638477/005lib/git/commits/{head}")
    assert server_commit["sha"] == head and server_commit["tree"]["sha"] == proof["tree"]
    assert [parent["sha"] for parent in server_commit["parents"]] == [BASE]
    result = {"status": "PASS_PUSH_AND_REMOTE_REF_VERIFIED", "completed_at": datetime.now(timezone.utc).isoformat(),
              "repository": "https://github.com/875638477/005lib", "branch": "main", "commit": head,
              "tree": proof["tree"], "remote_commit": after, "fetched_remote_commit": fetched,
              "library_files": proof["library_files"], "directories": DIRS,
              "github_api_root_directories": sorted(item["name"] for item in contents),
              "github_api_tree": server_commit["tree"]["sha"], "original_history_preserved": True,
              "obsolete_remote_files_deleted": ["README.md"],
              "push_stdout": output, "final_record_note": "Generated after push; retained locally under 01AIEDA."}
    # Do not modify the already verified checkout after the push.
    for path in (TASK / "upload_result.json", SOURCE_LOG / "upload_result.json"):
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["prepare", "push"])
    args = parser.parse_args()
    prepare() if args.action == "prepare" else push()
