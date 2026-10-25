"""Publish the completed upload's maintenance records as a second small commit.

The workspace copy runs only after the first content push is verified. It writes
this script and README_completion.txt to the source task folder before committing.
It never updates source upload_result.json or any source record after the commit.
Final publication evidence is written only to workspace/final_publication_result.json;
the final metadata commit is discoverable from GitHub history, avoiding self-reference.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

TASK = Path(__file__).resolve().parent
REPO = TASK / "repository"
SOURCE_LOG = Path(r"D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_github_upload")
REL_LOG = "01AIEDA/library_maintenance/20261025_github_upload"
GIT = TASK / "tools/mingit/cmd/git.exe"
GH = TASK / "tools/gh/bin/gh.exe"
CONTENT_COMMIT = "e6c4470941a5cabc3c21fcf66d3f5d77dfab929f"
REMOTE_REPOSITORY = "https://github.com/875638477/005lib"
DIRS = ["01aeLib", "01AIEDA", "01brdlib", "01captureLib", "01env", "01Pad_lib", "01Psm_lib", "01script_file", "01_3d_step_lib"]
POSTCOMMIT_RECORDS = {
    "fast_import.stdout.log", "fast_import.stderr.log", "fast_import_object_check.stdout.log",
    "fast_import_object_check.stderr.log", "fast_import_tree.stdout.log", "fast_import_tree.stderr.log",
    "fast_import.marks", "git_import_verification.json", "commit_preparation.json", "upload_result.json",
}
ALLOWED_METADATA_CHANGES = POSTCOMMIT_RECORDS | {Path(__file__).name, "README_completion.txt"}
BLOCK = 1024 * 1024


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def env(network: bool = False) -> dict[str, str]:
    result = os.environ.copy()
    result["PATH"] = str(GIT.parent) + os.pathsep + result.get("PATH", "")
    result["GIT_TERMINAL_PROMPT"] = "0"
    if network:
        result["HTTPS_PROXY"] = result["HTTP_PROXY"] = "http://127.0.0.1:7890"
    return result


def git(*args: str, network: bool = False) -> bytes:
    command = [str(GIT), "-c", f"safe.directory={REPO.as_posix()}",
               "-c", "core.longpaths=true", "-c", "core.autocrlf=false", "-c", "gc.auto=0"]
    if network:
        command += ["-c", "http.proxy=http://127.0.0.1:7890", "-c", "http.version=HTTP/1.1",
                    "-c", "credential.helper=", "-c", f"credential.helper=!{GH.as_posix()} auth git-credential"]
    command += ["-C", str(REPO), *args]
    result = subprocess.run(command, env=env(network), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(result.returncode == 0,
            f"git {args[0]} failed ({result.returncode}): "
            + result.stderr.decode("utf-8", "replace")[-4000:])
    return result.stdout


def git_text(*args: str, network: bool = False) -> str:
    return git(*args, network=network).decode("utf-8").strip()


def remote_main() -> str:
    fields = git_text("ls-remote", "origin", "refs/heads/main", network=True).split()
    require(len(fields) == 2 and fields[1] == "refs/heads/main", "Unexpected remote main response")
    return fields[0]


def api(path: str):
    response = subprocess.run([str(GH), "api", path], env=env(True),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(response.returncode == 0,
            "GitHub API request failed: " + response.stderr.decode("utf-8", "replace")[-2000:])
    return json.loads(response.stdout)


def within_task(path: str) -> bool:
    return path.startswith(REL_LOG + "/")


def tree_map(commit: str) -> dict[str, tuple[str, str, str]]:
    result = {}
    for entry in git("ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
        if not entry:
            continue
        attrs, raw_path = entry.split(b"\t", 1)
        path = raw_path.decode("utf-8", "strict")
        mode, kind, oid = attrs.decode("ascii").split()
        require(path not in result, "Duplicate committed tree path")
        result[path] = (mode, kind, oid)
    return result


def index_map() -> dict[str, tuple[str, str, str]]:
    result = {}
    for entry in git("ls-files", "-s", "-z").split(b"\0"):
        if not entry:
            continue
        attrs, raw_path = entry.split(b"\t", 1)
        path = raw_path.decode("utf-8", "strict")
        mode, oid, stage = attrs.decode("ascii").split()
        require(stage == "0" and path not in result, "Unexpected index stage/duplicate")
        require(mode == "100644", "Unexpected index mode")
        result[path] = (mode, "blob", oid)
    return result


def root_directories(commit: str) -> list[str]:
    roots = []
    for entry in git("ls-tree", "-z", "--full-tree", commit).split(b"\0"):
        if entry:
            attrs, raw_path = entry.split(b"\t", 1)
            mode, kind, _oid = attrs.decode("ascii").split()
            require(mode == "040000" and kind == "tree", "Root contains a non-directory entry")
            roots.append(raw_path.decode("utf-8"))
    require(sorted(roots) == sorted(DIRS) and len(roots) == 9, "Root must remain exactly nine directories")
    return sorted(roots)


def task_files(root: Path) -> dict[str, Path]:
    require(root.is_dir(), "Maintenance task folder is missing")
    files = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            info = path.lstat()
            require(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
                    "Reparse point in maintenance task folder")
            relative = path.relative_to(root).as_posix()
            require(all(part not in ("", ".", "..", ".git") for part in relative.split("/")),
                    "Unsafe maintenance relative path")
            if path.is_dir():
                pending.append(path)
            else:
                require(path.is_file(), "Non-regular maintenance entry")
                files[relative] = path
    return files


def hashes(path: Path) -> dict:
    size = path.stat().st_size
    sha256 = hashlib.sha256()
    blob = hashlib.sha1(f"blob {size}\0".encode("ascii"))
    count = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(BLOCK), b""):
            count += len(block)
            sha256.update(block)
            blob.update(block)
    require(count == size, "Maintenance record changed while reading")
    return {"bytes": size, "sha256": sha256.hexdigest(), "git_blob_sha1": blob.hexdigest()}


def write_new_source_record(name: str, raw: bytes) -> None:
    require(name in ALLOWED_METADATA_CHANGES, "Unexpected source write target")
    path = SOURCE_LOG / name
    if path.exists() and path.read_bytes() == raw:
        return
    path.write_bytes(raw)
    require(path.read_bytes() == raw, f"Source maintenance record readback differs: {name}")


def main() -> None:
    require(REPO.is_dir() and GIT.is_file() and GH.is_file(), "Run the prepared workspace copy")
    first_raw = (TASK / "upload_result.json").read_bytes()
    first = json.loads(first_raw)
    require(first["status"] == "PASS_PUSH_AND_REMOTE_REF_VERIFIED"
            and first["commit"] == CONTENT_COMMIT
            and first["remote_commit"] == CONTENT_COMMIT
            and first["fetched_remote_commit"] == CONTENT_COMMIT,
            "The first content push has not passed independent remote verification")
    require((SOURCE_LOG / "upload_result.json").read_bytes() == first_raw,
            "Source first-push result differs from the verified workspace result")
    require(git_text("symbolic-ref", "HEAD") == "refs/heads/main", "HEAD must name main")
    require(git_text("rev-parse", "HEAD") == CONTENT_COMMIT, "Local HEAD differs from the content commit")
    require(remote_main() == CONTENT_COMMIT, "Remote main differs from the content commit")
    require(not (REPO / ".git/index.lock").exists(), "Unexpected index.lock")
    original = tree_map(CONTENT_COMMIT)
    require(index_map() == original, "The starting index differs from the content commit")
    root_directories(CONTENT_COMMIT)
    require(git_text("rev-parse", f"{CONTENT_COMMIT}^{{tree}}") == first["tree"],
            "Content tree differs from its first-push proof")

    # Both new source records are finalized before staging. No source writes are
    # performed after the commit, and the first upload_result remains untouched.
    write_new_source_record(Path(__file__).name, Path(__file__).read_bytes())
    completion = (
        "GitHub库上传完成记录\n\n"
        f"首轮库主体提交：{CONTENT_COMMIT}\n"
        f"仓库：{REMOTE_REPOSITORY}\n"
        "首轮提交已完成远端引用、GitHub API目录、父提交和树核验。\n"
        "本次第二次提交仅发布本任务目录内的导入日志、marks、完整树验证证明、提交准备和首轮上传结果，"
        "同时保存本发布脚本与本说明。库文件沿用已核验的首轮提交。\n"
        "源任务目录既有初始记录逐字节哈希核对；相同文件不重写，只复制本任务目录的新增记录差异。\n"
        "upload_result.json保留首轮库主体提交的核验结果。最新元数据提交请查看GitHub main历史，"
        "本说明不嵌入它自身所在提交的SHA，避免自引用。\n"
        "发布脚本和本说明均在元数据提交前写入源01AIEDA与工作副本；提交后不再修改源任务记录。"
        "最终发布验证结果仅保存于本地工作目录final_publication_result.json并输出到控制台，"
        "不会再写入源01AIEDA或追加另一轮提交。\n"
    ).encode("utf-8")
    write_new_source_record("README_completion.txt", completion)
    source_files = task_files(SOURCE_LOG)
    require(POSTCOMMIT_RECORDS <= set(source_files), "One of the ten completed upload records is missing")
    repository_files = task_files(REPO / REL_LOG)
    require(not (set(repository_files) - set(source_files)), "Unexpected repository-only task records")
    source_records, copied, unchanged = {}, [], []
    expected = dict(original)
    for relative, source in sorted(source_files.items()):
        repository_relative = f"{REL_LOG}/{relative}"
        record = hashes(source)
        source_records[relative] = record
        prior = original.get(repository_relative)
        desired = ("100644", "blob", record["git_blob_sha1"])
        if prior != desired:
            require(relative in ALLOWED_METADATA_CHANGES,
                    f"Unexpected change to an initial task record: {relative}")
        destination = REPO / repository_relative
        if destination.exists() and hashes(destination) == record:
            unchanged.append(repository_relative)
        else:
            require(relative in ALLOWED_METADATA_CHANGES, "Only final metadata records may be copied")
            destination.parent.mkdir(parents=True, exist_ok=True)
            raw = source.read_bytes()
            require(len(raw) == record["bytes"] and hashlib.sha256(raw).hexdigest() == record["sha256"],
                    "Source maintenance record changed before copying")
            destination.write_bytes(raw)
            require(hashes(destination) == record, "Copied maintenance record SHA256/blob mismatch")
            copied.append(repository_relative)
        expected[repository_relative] = desired
    original_task = {path[len(REL_LOG) + 1:] for path in original if within_task(path)}
    require(original_task <= set(source_files), "An original task record disappeared from source")
    require({path: item for path, item in expected.items() if not within_task(path)}
            == {path: item for path, item in original.items() if not within_task(path)},
            "Expected tree would change a library path outside the task")
    require(copied, "There are no final metadata records to publish")
    require((SOURCE_LOG / "upload_result.json").read_bytes() == first_raw,
            "First-push source result was changed")

    git("add", "-f", "--", REL_LOG)
    require(index_map() == expected, "Entire staged index does not match original tree plus verified task updates")
    require(git_text("rev-parse", "HEAD") == CONTENT_COMMIT, "HEAD changed before metadata commit")
    git("commit", "-m", "Publish verified library upload audit records")
    commit = git_text("rev-parse", "HEAD")
    require(git_text("rev-list", "--parents", "-n", "1", commit).split() == [commit, CONTENT_COMMIT],
            "Metadata commit must have exactly the content commit as its parent")
    require(tree_map(commit) == expected, "Entire metadata commit tree differs from verified staged tree")
    roots = root_directories(commit)
    tree = git_text("rev-parse", f"{commit}^{{tree}}")
    require(remote_main() == CONTENT_COMMIT, "Remote changed; reconcile before a normal push")
    git("push", "origin", "HEAD:refs/heads/main", network=True)
    require(remote_main() == commit, "Remote main does not match metadata commit")
    git("fetch", "origin", "main", network=True)
    require(git_text("rev-parse", "origin/main") == commit, "Fetched remote ref differs")
    server_root = api("repos/875638477/005lib/contents?ref=main")
    require(len(server_root) == 9 and all(item["type"] == "dir" for item in server_root)
            and sorted(item["name"] for item in server_root) == sorted(DIRS),
            "GitHub API root is not exactly the nine library directories")
    server_commit = api(f"repos/875638477/005lib/git/commits/{commit}")
    require(server_commit["sha"] == commit and server_commit["tree"]["sha"] == tree
            and [parent["sha"] for parent in server_commit["parents"]] == [CONTENT_COMMIT],
            "GitHub API commit/tree/parent differs")
    # This second pass touches only the small task folder, not the 3 GB library.
    # No source changes are made here or after this point.
    final_source_files = task_files(SOURCE_LOG)
    require(set(final_source_files) == set(source_records), "Source task file set changed during publication")
    require(all(hashes(final_source_files[name]) == record for name, record in source_records.items()),
            "Source task record changed during publication")
    require(tree_map(commit) == expected and index_map() == expected,
            "Local committed tree/index changed during publication")
    require((SOURCE_LOG / "upload_result.json").read_bytes() == first_raw,
            "Source first-push proof must remain unchanged")
    result = {
        "status": "PASS_FINAL_AUDIT_RECORDS_PUBLISHED",
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": REMOTE_REPOSITORY, "branch": "main", "content_commit": CONTENT_COMMIT,
        "commit": commit, "tree": tree, "single_parent": CONTENT_COMMIT,
        "remote_commit": commit, "fetched_remote_commit": commit,
        "root_directories": roots, "total_tree_files": len(expected),
        "source_task_file_count": len(source_records), "copied_task_records": copied,
        "unchanged_task_files_not_rewritten": len(unchanged),
        "all_source_task_file_bytes_match_final_commit": True,
        "all_paths_outside_task_unchanged_from_content_commit": True,
        "entire_staged_and_committed_trees_verified": True,
        "original_source_library_rehashed": False,
        "source_first_upload_result_preserved": True,
        "source_task_sha256_and_blob_manifest": source_records,
        "final_result_boundary": "This result exists only in workspace/stdout. Source task records were finalized before committing and were not changed afterward.",
    }
    output = TASK / "final_publication_result.json"
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    output.write_bytes(raw)
    require(output.read_bytes() == raw, "Final workspace result readback differs")
    print(json.dumps({key: result[key] for key in
                      ("status", "repository", "commit", "tree", "content_commit", "total_tree_files",
                       "source_task_file_count", "all_source_task_file_bytes_match_final_commit")},
                     ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
