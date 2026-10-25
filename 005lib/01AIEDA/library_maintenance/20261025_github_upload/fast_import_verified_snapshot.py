"""Prepare one verified descendant commit via pack-based fast-import; never push.

Run the workspace copy only, after the prior git-add process has stopped and its
stale index.lock has been reviewed/removed. Original library bytes are not read
again. Only new maintenance records are copied into the source record folder.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

TASK = Path(__file__).resolve().parent
REPO = TASK / "repository"
SOURCE_LOG = Path(r"D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_github_upload")
REL_LOG = "01AIEDA/library_maintenance/20261025_github_upload"
GIT = TASK / "tools/mingit/cmd/git.exe"
BASE = "6e478a7603b6adbe790ea0ad0409fba48ca27e43"
TEMP_REF = "refs/heads/library-upload-20261025"
DIRS = ["01aeLib", "01AIEDA", "01brdlib", "01captureLib", "01env", "01Pad_lib", "01Psm_lib", "01script_file", "01_3d_step_lib"]
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
BLOCK = 1024 * 1024
POSTCOMMIT_LOG_NAMES = (
    "fast_import.stdout.log", "fast_import.stderr.log",
    "fast_import_object_check.stdout.log", "fast_import_object_check.stderr.log",
    "fast_import_tree.stdout.log", "fast_import_tree.stderr.log", "fast_import.marks",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_command(*args: str) -> list[str]:
    return [str(GIT), "-c", f"safe.directory={REPO.as_posix()}",
            "-c", "core.longpaths=true", "-c", "core.autocrlf=false",
            "-c", "gc.auto=0", "-C", str(REPO), *args]


def git_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PATH"] = str(GIT.parent) + os.pathsep + env.get("PATH", "")
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def git(*args: str, allowed: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess:
    # Only short metadata responses use pipes. Object and import outputs use files.
    result = subprocess.run(git_command(*args), env=git_env(),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(result.returncode in allowed,
            f"git {args[0]} failed ({result.returncode}): "
            + result.stderr.decode("utf-8", "replace")[-4000:])
    return result


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8").strip()


def write_json(path: Path, data: dict) -> None:
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(raw)
    require(path.read_bytes() == raw, f"Record readback mismatch: {path.name}")


def file_hashes(path: Path) -> dict:
    size = path.stat().st_size
    sha256 = hashlib.sha256()
    sha1 = hashlib.sha1(f"blob {size}\0".encode("ascii"))
    count = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(BLOCK), b""):
            sha256.update(block)
            sha1.update(block)
            count += len(block)
    require(count == size, f"Record size changed while reading: {path.name}")
    return {"bytes": size, "sha256": sha256.hexdigest(), "git_blob_sha1": sha1.hexdigest()}


def validate_relative(path: str) -> None:
    require(bool(path) and "\\" not in path and "\0" not in path,
            "Noncanonical repository path")
    require(all(part not in ("", ".", "..", ".git") for part in path.split("/")),
            "Unsafe repository path component")
    require(path.split("/", 1)[0] in DIRS, "Path outside the nine source directories")
    # Windows source names cannot contain these. Reject JSON \u escapes that are
    # not part of fast-import's C-quoted path syntax rather than guessing at them.
    require(not any(ord(character) < 32 for character in path),
            "Unexpected control character in repository path")
    path.encode("utf-8", "strict")


def copy_new_record(name: str, raw: bytes) -> dict:
    for destination in (SOURCE_LOG / name, REPO / REL_LOG / name):
        require(destination.parent.is_dir(), "Maintenance record directory is missing")
        destination.write_bytes(raw)
        require(destination.read_bytes() == raw, f"New record copy mismatch: {name}")
    return file_hashes(REPO / REL_LOG / name)


def load_expected() -> tuple[dict[str, dict], dict, dict]:
    proof_path = SOURCE_LOG / "snapshot_verification.json"
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    require(proof["status"].startswith("PASS"), "Source snapshot has not passed")
    require(proof.get("snapshot_amendment", {}).get("status", "").startswith("PASS"),
            "Mirror-policy amendment has not passed")
    require(set(proof["top_level_directories"]) == set(DIRS), "Snapshot root set differs")
    policy = json.loads((SOURCE_LOG / "mirror_policy.json").read_text(encoding="utf-8"))
    require(policy["status"].startswith("PASS"), "Mirror policy has not passed")
    require(policy["original_base_commit"] == BASE, "Mirror policy base differs")
    require({entry["path"] for entry in policy["remote_deletions"]} == {"README.md"},
            "Unexpected authorized remote deletion set")
    manifest = SOURCE_LOG / "upload_manifest.csv"
    manifest_hash = hashlib.sha256(manifest.read_bytes()).hexdigest()
    require(manifest_hash == proof["manifest_sha256"], "Manifest differs from verified proof")
    expected: dict[str, dict] = {}
    with manifest.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames == ["source", "repository_relative", "bytes", "sha256", "git_blob_sha1"],
                "Unexpected manifest columns")
        for row in reader:
            path = row["repository_relative"]
            validate_relative(path)
            require(path not in expected, "Duplicate manifest path")
            record = {"bytes": int(row["bytes"]), "sha256": row["sha256"],
                      "git_blob_sha1": row["git_blob_sha1"]}
            require(record["bytes"] >= 0 and HEX64.fullmatch(record["sha256"])
                    and HEX40.fullmatch(record["git_blob_sha1"]), "Invalid manifest hashes/size")
            expected[path] = record
    require(len(expected) == proof["manifest_files"], "Manifest row count differs from proof")
    return expected, proof, {"manifest_sha256": manifest_hash,
                             "snapshot_proof_sha256": hashlib.sha256(proof_path.read_bytes()).hexdigest()}


def add_record_expected(expected: dict[str, dict], name: str) -> None:
    relative = f"{REL_LOG}/{name}"
    validate_relative(relative)
    source_path = SOURCE_LOG / name
    repository_path = REPO / relative
    require(source_path.read_bytes() == repository_path.read_bytes(),
            f"Source/repository maintenance record mismatch: {name}")
    record = file_hashes(repository_path)
    require(relative not in expected or expected[relative] == record,
            f"Record would overwrite a different verified manifest row: {name}")
    expected[relative] = record


def group_expected(expected: dict[str, dict]) -> dict[str, tuple[str, dict]]:
    unique = {}
    for path, record in expected.items():
        oid = record["git_blob_sha1"]
        if oid in unique:
            require(unique[oid][1] == record, "One expected OID has inconsistent size/SHA256")
        else:
            unique[oid] = (path, record)
    return unique


def existing_objects(unique: dict[str, tuple[str, dict]]) -> tuple[set[str], list[str]]:
    ordered = sorted(unique)
    stdout_path = TASK / "fast_import_object_check.stdout.log"
    stderr_path = TASK / "fast_import_object_check.stderr.log"
    with stdout_path.open("wb") as output, stderr_path.open("wb") as errors:
        result = subprocess.run(git_command("cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"),
                                env=git_env(), input=("\n".join(ordered) + "\n").encode("ascii"),
                                stdout=output, stderr=errors)
    require(result.returncode == 0, f"Object existence check failed; see {stderr_path.name}")
    lines = stdout_path.read_bytes().splitlines()
    require(len(lines) == len(ordered), "Object existence response count differs")
    present, missing = set(), []
    for oid, line in zip(ordered, lines):
        fields = line.decode("ascii").split()
        require(fields and fields[0] == oid, "Object existence response order differs")
        if fields == [oid, "missing"]:
            missing.append(oid)
        else:
            require(len(fields) == 3 and fields[1] == "blob"
                    and int(fields[2]) == unique[oid][1]["bytes"],
                    "Existing object is not the expected blob/size")
            present.add(oid)
    return present, missing


def stream_missing_blob(pipe, path: Path, record: dict, mark: int) -> None:
    size = record["bytes"]
    require(path.is_file() and path.stat().st_size == size, "Missing-blob representative size differs")
    sha1 = hashlib.sha1(f"blob {size}\0".encode("ascii"))
    sha256 = hashlib.sha256()
    pipe.write(f"blob\nmark :{mark}\ndata {size}\n".encode("ascii"))
    remaining = size
    with path.open("rb") as handle:
        while remaining:
            block = handle.read(min(BLOCK, remaining))
            require(bool(block), "Unexpected EOF in missing-blob representative")
            sha1.update(block)
            sha256.update(block)
            pipe.write(block)
            remaining -= len(block)
        require(not handle.read(1), "Missing-blob representative grew during import")
    require(sha1.hexdigest() == record["git_blob_sha1"]
            and sha256.hexdigest() == record["sha256"],
            "Missing-blob representative SHA1/SHA256 differs from verified snapshot")
    pipe.write(b"\n")


def import_pack(expected: dict[str, dict], unique: dict[str, tuple[str, dict]],
                present: set[str], missing: list[str]) -> dict:
    name = git_text("config", "user.name")
    email = git_text("config", "user.email")
    require(name and email and not any(c in name + email for c in "\r\n<>"),
            "Review Git author identity before import")
    ident = f"{name} <{email}> {int(time.time())} +0800"
    message = b"Synchronize local 01 library folders and remove obsolete remote files\n"
    marks = {oid: number for number, oid in enumerate(missing, 1)}
    started = utc_now()
    stdout_path = TASK / "fast_import.stdout.log"
    stderr_path = TASK / "fast_import.stderr.log"
    with stdout_path.open("wb") as output, stderr_path.open("wb") as errors:
        command = git_command("-c", "fastimport.unpackLimit=0", "fast-import", "--done", "--date-format=raw",
                              f"--export-marks={(TASK / 'fast_import.marks').as_posix()}")
        process = subprocess.Popen(command, env=git_env(), stdin=subprocess.PIPE,
                                   stdout=output, stderr=errors)
        try:
            pipe = process.stdin
            require(pipe is not None, "Fast-import stdin unavailable")
            for number, oid in enumerate(missing, 1):
                relative, record = unique[oid]
                stream_missing_blob(pipe, REPO / relative, record, marks[oid])
                if number % 1000 == 0 or number == len(missing):
                    print(json.dumps({"phase": "streaming_missing_unique_blobs", "completed": number,
                                      "total": len(missing)}, ensure_ascii=False), flush=True)
            pipe.write(f"commit {TEMP_REF}\nmark :{len(missing) + 1}\n".encode("ascii"))
            pipe.write(f"author {ident}\ncommitter {ident}\ndata {len(message)}\n".encode("utf-8"))
            pipe.write(message)
            pipe.write(f"\nfrom {BASE}\ndeleteall\n".encode("ascii"))
            for relative in sorted(expected, key=lambda value: value.encode("utf-8")):
                oid = expected[relative]["git_blob_sha1"]
                dataref = oid if oid in present else f":{marks[oid]}"
                quoted = json.dumps(relative, ensure_ascii=False)
                pipe.write(f"M 100644 {dataref} {quoted}\n".encode("utf-8"))
            pipe.write(b"\ndone\n")
            pipe.close()
            code = process.wait()
            require(code == 0, f"Fast-import failed ({code}); see {stderr_path.name}")
        except BaseException:
            if process.stdin is not None and not process.stdin.closed:
                try:
                    process.stdin.close()
                except (BrokenPipeError, OSError):
                    pass
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            raise
    return {"started_utc": started, "finished_utc": utc_now(),
            "unique_expected_blobs": len(unique), "reused_existing_blobs": len(present),
            "missing_unique_blobs_sha1_sha256_verified": len(missing),
            "stdout_log": stdout_path.name, "stderr_log": stderr_path.name}


def verify_entire_tree(commit: str, expected: dict[str, dict]) -> tuple[str, dict]:
    require(HEX40.fullmatch(commit) is not None, "Imported commit OID is invalid")
    require(git_text("rev-list", "--parents", "-n", "1", commit).split() == [commit, BASE],
            "Imported commit does not have exactly BASE as its single parent")
    tree = git_text("rev-parse", f"{commit}^{{tree}}")
    stdout_path = TASK / "fast_import_tree.stdout.log"
    stderr_path = TASK / "fast_import_tree.stderr.log"
    with stdout_path.open("wb") as output, stderr_path.open("wb") as errors:
        result = subprocess.run(git_command("ls-tree", "-r", "-z", "--full-tree", commit),
                                env=git_env(), stdout=output, stderr=errors)
    require(result.returncode == 0, f"Tree enumeration failed; see {stderr_path.name}")
    indexed = {}
    for entry in stdout_path.read_bytes().split(b"\0"):
        if not entry:
            continue
        attrs, raw_path = entry.split(b"\t", 1)
        path = raw_path.decode("utf-8", "strict")
        mode, kind, oid = attrs.decode("ascii").split()
        require(path not in indexed, "Duplicate imported tree path")
        require(mode == "100644" and kind == "blob", "Imported mode/type differs")
        require(path in expected and oid == expected[path]["git_blob_sha1"],
                f"Imported tree path/blob differs from expected snapshot: {path}")
        indexed[path] = oid
    require(set(indexed) == set(expected), "Imported complete path set differs")
    roots = {}
    for entry in git("ls-tree", "-z", "--full-tree", commit).stdout.split(b"\0"):
        if entry:
            attrs, raw_path = entry.split(b"\t", 1)
            mode, kind, _oid = attrs.decode("ascii").split()
            require(mode == "040000" and kind == "tree", "Imported root contains a file/non-directory")
            roots[raw_path.decode("utf-8")] = True
    require(set(roots) == set(DIRS) and len(roots) == 9, "Imported root is not exactly nine directories")
    require("README.md" not in indexed, "Obsolete root README remains")
    return tree, {"all_expected_paths_modes_types_and_blob_oids_match": True,
                  "entire_tree_entries_checked": len(indexed), "unexpected_tree_entries": 0,
                  "missing_expected_entries": 0, "root_directories": sorted(roots),
                  "single_parent": BASE, "authorized_root_readme_absent": True}


def main() -> None:
    require(REPO.is_dir() and GIT.is_file(), "Run the workspace copy with its prepared repository/tools")
    require(git_text("symbolic-ref", "HEAD") == "refs/heads/main", "HEAD must name main for push-runner compatibility")
    require(git_text("rev-parse", "refs/heads/main") == BASE, "Main changed before import")
    require(not (REPO / ".git/index.lock").exists(), "Stop/review old git-add and index.lock before import")
    require(git("show-ref", "--verify", "--quiet", TEMP_REF, allowed=(0, 1)).returncode == 1,
            "Temporary import ref already exists; inspect it before retrying")
    expected, snapshot, anchors = load_expected()
    base_paths = []
    for entry in git("ls-tree", "-r", "-z", BASE).stdout.split(b"\0"):
        if entry:
            base_paths.append(entry.split(b"\t", 1)[1].decode("utf-8"))
    require(base_paths == ["README.md"], "Review unexpected base tree before deleteall")

    # These new records are the only source writes, and are outside the immutable
    # original manifest. Self-reference outputs and the existing runner are only
    # read/compared here; the original manifest file is never rewritten.
    script_raw = Path(__file__).read_bytes()
    copy_new_record(Path(__file__).name, script_raw)
    method = {"status": "REVIEWED_PACK_BASED_IMPORT_PLAN", "recorded_at_utc": utc_now(),
              "method": "git fast-import with exact binary lengths, unique-blob reuse and full-tree verification",
              "base_commit": BASE, "temporary_ref": TEMP_REF,
              "fastimport_unpackLimit": 0, "force": False, "network_operations": False,
              "final_root_directories": DIRS, "authorized_remote_deletions": ["README.md"],
              "original_manifest_modified": False, "source_originals_rehashed": False,
              "new_blobs": "Only missing unique blob representatives are read from the verified repository snapshot and checked by size, SHA256 and Git blob SHA1 before completion.",
              "existing_blobs": "Already verified manifest OIDs are reused only after cat-file confirms blob type and exact byte length.",
              "verification": "Every entry of the complete imported tree is compared against expected path, mode, type and OID; exact nine roots and single BASE parent are required before main moves.",
              "postcommit_records_not_in_tree": ["git_import_verification.json", "commit_preparation.json", "upload_result.json", *POSTCOMMIT_LOG_NAMES],
              "script_sha256": hashlib.sha256(script_raw).hexdigest(), **anchors,
              "documentation": ["https://git-scm.com/docs/git-fast-import", "https://git-scm.com/docs/git-ls-tree", "https://git-scm.com/docs/git-cat-file"]}
    method_raw = (json.dumps(method, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    (TASK / "git_import_method.json").write_bytes(method_raw)
    copy_new_record("git_import_method.json", method_raw)
    for name in ("upload_manifest.csv", "snapshot_verification.json", "commit_and_push.py",
                 Path(__file__).name, "git_import_method.json"):
        add_record_expected(expected, name)
    unique = group_expected(expected)
    present, missing = existing_objects(unique)
    print(json.dumps({"phase": "object_reuse_checked", "expected_files": len(expected),
                      "unique_blobs": len(unique), "existing_blobs": len(present),
                      "missing_blobs": len(missing)}), flush=True)
    imported = import_pack(expected, unique, present, missing)
    commit = git_text("rev-parse", TEMP_REF)
    tree, tree_proof = verify_entire_tree(commit, expected)
    require(git_text("rev-parse", "refs/heads/main") == BASE, "Main changed during import; no promotion performed")
    require(not (REPO / ".git/index.lock").exists(), "Unexpected index.lock before promotion")
    # CAS promotion preserves the original base and never force-updates a ref.
    git("update-ref", "-m", "Verified pack-based library snapshot", "refs/heads/main", commit, BASE)
    try:
        git("read-tree", "HEAD")
    except BaseException:
        # If index refresh fails, restore only our own ref update using another
        # compare-and-swap. Never overwrite an intervening update by another actor.
        git("update-ref", "-m", "Rollback failed library index refresh", "refs/heads/main", BASE, commit)
        raise
    require(git_text("rev-parse", "HEAD") == commit, "HEAD differs after promotion")
    result = {"status": "PASS_COMMIT_READY", "commit": commit, "tree": tree, "base_commit": BASE,
              "library_files": len(expected), "directories": DIRS,
              "object_statistics": git_text("count-objects", "-vH")}
    postcommit_logs = []
    for name in POSTCOMMIT_LOG_NAMES:
        origin = TASK / name
        if name == "fast_import.marks" and not origin.exists():
            continue
        raw = origin.read_bytes()
        destination = SOURCE_LOG / name
        destination.write_bytes(raw)
        require(destination.read_bytes() == raw, f"Postcommit log readback differs: {name}")
        postcommit_logs.append({"name": name, "bytes": len(raw),
                                "sha256": hashlib.sha256(raw).hexdigest(),
                                "retained_in_source_01AIEDA": True,
                                "included_in_commit_tree": False})
    proof = {"status": "PASS_ENTIRE_IMPORTED_TREE_MATCHES_VERIFIED_SOURCE_SNAPSHOT",
             "verified_at_utc": utc_now(), "commit": commit, "tree": tree, "base_commit": BASE,
             "manifest_rows": snapshot["manifest_files"], "expected_files_in_complete_tree": len(expected),
             "verification_scope": "Entire imported commit tree, not a sample or changed-file subset.",
             "added_expected_records": [f"{REL_LOG}/{name}" for name in
                                        ("upload_manifest.csv", "snapshot_verification.json", "commit_and_push.py",
                                         Path(__file__).name, "git_import_method.json")],
             "postcommit_record_note": "This proof, commit_preparation.json, all import/object-check/tree stdout/stderr logs and optional marks are generated after or during the commit preparation and retained under source 01AIEDA and workspace; these postcommit records are intentionally outside the committed tree.",
             "postcommit_logs": postcommit_logs,
             "original_manifest_modified": False, "source_originals_rehashed": False,
             "main_compare_and_swap_promoted": True, "index_refreshed_from_HEAD": True,
             "network_operations": False, "import": imported, "tree_verification": tree_proof, **anchors}
    for parent in (TASK, SOURCE_LOG):
        write_json(parent / "git_import_verification.json", proof)
        write_json(parent / "commit_preparation.json", result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
