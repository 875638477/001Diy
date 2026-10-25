"""Amend the completed snapshot for the user's exact remote mirror policy.

Review before execution. This writes only the named maintenance records and
deletes only the verified, old worktree-root README.md. No network, staging,
commit, push, source-library deletion or full library rehash is performed.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess


WORK = Path(r"D:\001DIY\004computer\lga1700\git_upload_005lib_20261025")
SOURCE = Path(r"D:\001DIY\005lib")
REPO = WORK / "repository"
REL_LOG = Path("01AIEDA/library_maintenance/20261025_github_upload")
SOURCE_LOG = SOURCE / REL_LOG
REPO_LOG = REPO / REL_LOG
GIT = WORK / "tools/mingit/cmd/git.exe"
BASE = "6e478a7603b6adbe790ea0ad0409fba48ca27e43"
OLD_README_BLOB = "497548eeb3d973939ca8f5ba7a0ca2d8dfa4e069"
DIRECTORIES = {"01aeLib", "01AIEDA", "01brdlib", "01captureLib", "01env", "01Pad_lib", "01Psm_lib", "01script_file", "01_3d_step_lib"}
FIELDS = ["source", "repository_relative", "bytes", "sha256", "git_blob_sha1"]
LIMIT = 100 * 1024 * 1024
OLD_POLICY = "仓库已有的其他文件保留。"
NEW_POLICY = "按用户最新指令，以今天本机这 9 个 01 目录为 GitHub 内容基准；删除远端不在该范围内的旧文件，保持目录层级一致。本次经核验原远端仅有根 README.md，因此删除该旧文件，最终仓库根仅保留这 9 个目录。"
USER_INSTRUCTION = "GitHub以本机今天9个01目录为准更新，远端旧文件也删。"


def check_plain(path: Path, *, directory: bool = False) -> os.stat_result:
    for ancestor in reversed((path, *path.parents)):
        info = ancestor.stat(follow_symlinks=False)
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f"Reparse point forbidden: {ancestor}")
    info = path.stat(follow_symlinks=False)
    if path.resolve(strict=True) != path:
        raise ValueError(f"Resolved path differs: {path}")
    if directory and not stat.S_ISDIR(info.st_mode):
        raise ValueError(f"Expected a directory: {path}")
    if not directory and not stat.S_ISREG(info.st_mode):
        raise ValueError(f"Expected a regular file: {path}")
    return info


def content_info(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "git_blob_sha1": hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()}


def read_stable(path: Path) -> bytes:
    before = check_plain(path)
    raw = path.read_bytes()
    after = check_plain(path)
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino) or len(raw) != before.st_size:
        raise ValueError(f"File changed while reading: {path}")
    return raw


def write_exact(path: Path, raw: bytes) -> None:
    check_plain(path.parent, directory=True)
    if path.exists():
        check_plain(path)
    path.write_bytes(raw)
    if read_stable(path) != raw:
        raise ValueError(f"Write/readback mismatch: {path}")


def copy_verified(source: Path, destination: Path, expected: bytes) -> None:
    check_plain(destination.parent, directory=True)
    if destination.exists():
        check_plain(destination)
    if read_stable(source) != expected:
        raise ValueError(f"Copy source changed: {source}")
    shutil.copy2(source, destination)
    if content_info(read_stable(destination)) != content_info(expected):
        raise ValueError(f"Copy SHA256/blob verification failed: {destination}")


def git_read(*args: str) -> bytes:
    check_plain(GIT)
    result = subprocess.run([str(GIT), "-c", f"safe.directory={REPO.as_posix()}", "-c", "core.longpaths=true", "-C", str(REPO), *args], capture_output=True)
    if result.returncode:
        raise RuntimeError("Read-only Git inspection failed: " + result.stderr.decode("utf-8", "replace")[-2000:])
    return result.stdout


def json_bytes(data: dict) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def replace_policy(raw: bytes, label: str) -> bytes:
    before, after = OLD_POLICY.encode("utf-8"), NEW_POLICY.encode("utf-8")
    if raw.count(before) != 1:
        raise ValueError(f"Expected one exact policy sentence in {label}")
    return raw.replace(before, after, 1)


def csv_row_bytes(row: dict, eol: str) -> bytes:
    output = io.StringIO(newline="")
    csv.DictWriter(output, fieldnames=FIELDS, lineterminator=eol).writerow(row)
    return output.getvalue().encode("utf-8")


def main() -> None:
    for root in (WORK, SOURCE, REPO, SOURCE_LOG, REPO_LOG, REPO / ".git"):
        check_plain(root, directory=True)
    if Path(__file__).resolve() != WORK / "apply_remote_mirror_policy.py":
        raise ValueError("Run the exact reviewed workspace script")
    if WORK.is_relative_to(SOURCE) or REPO.is_relative_to(SOURCE) or SOURCE.is_relative_to(REPO):
        raise ValueError("Workspace and source must be disjoint")
    # PASS and three identical proof copies ensure the original snapshot finished
    # publishing before any source record is changed by this amendment.
    old_proof_raw = read_stable(WORK / "snapshot_verification.json")
    for root in (SOURCE_LOG, REPO_LOG):
        if read_stable(root / "snapshot_verification.json") != old_proof_raw:
            raise ValueError("Wait for the completed snapshot proof publication")
    proof = json.loads(old_proof_raw.decode("utf-8"))
    if proof.get("status") != "PASS_SOURCE_SNAPSHOT_SIZE_SHA256_AND_GIT_BLOB_HASHES_VERIFIED" or "snapshot_amendment" in proof:
        raise ValueError("Expected the original, completed, unamended PASS snapshot")
    if proof.get("source_root") != str(SOURCE) or proof.get("repository_worktree") != str(REPO):
        raise ValueError("Snapshot roots do not match the exact authorized roots")
    if set(proof.get("top_level_directories", [])) != DIRECTORIES:
        raise ValueError("Snapshot scope must be exactly the nine requested directories")
    old_manifest_raw = read_stable(WORK / "upload_manifest.csv")
    for root in (SOURCE_LOG, REPO_LOG):
        if read_stable(root / "upload_manifest.csv") != old_manifest_raw:
            raise ValueError("Original manifest copies differ")
    old_manifest_info = content_info(old_manifest_raw)
    if old_manifest_info["sha256"] != proof.get("manifest_sha256") or old_manifest_info["git_blob_sha1"] != proof.get("manifest_git_blob_sha1"):
        raise ValueError("Original manifest SHA256/blob differs from the PASS proof")
    text = old_manifest_raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames != FIELDS:
        raise ValueError(f"Unexpected manifest fields: {reader.fieldnames}")
    rows = list(reader)
    physical_lines = text.splitlines(keepends=True)
    if len(physical_lines) != len(rows) + 1 or not old_manifest_raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("Expected one physical CSV line per original row and UTF-8 BOM")
    if len(rows) != proof["manifest_files"] or sum(int(row["bytes"]) for row in rows) != proof["manifest_source_bytes"] or max(int(row["bytes"]) for row in rows) != proof["largest_manifest_file_bytes"]:
        raise ValueError("Original manifest aggregates differ from the PASS proof")
    indexed = {}
    for row in rows:
        relative = PurePosixPath(row["repository_relative"])
        if relative.is_absolute() or not relative.parts or ".." in relative.parts or relative.parts[0] not in DIRECTORIES or any(part.casefold() == ".git" for part in relative.parts):
            raise ValueError(f"Invalid manifest relative path: {relative}")
        if row["source"] != str(SOURCE / Path(relative.as_posix())) or row["repository_relative"] in indexed:
            raise ValueError("Manifest source path mismatch or duplicate")
        if int(row["bytes"]) > LIMIT:
            raise ValueError("Original manifest contains an oversized file")
        indexed[row["repository_relative"]] = row
    expected_base_tree = f"100644 blob {OLD_README_BLOB}\tREADME.md\0".encode("ascii")
    if git_read("ls-tree", "-r", "-z", BASE) != expected_base_tree:
        raise ValueError("BASE must contain exactly the known README.md blob")
    if git_read("rev-parse", "HEAD").decode().strip() != BASE:
        raise ValueError("Expected the original BASE checkout before the mirror amendment")
    if git_read("config", "--get", "remote.origin.url").decode().strip() not in ("https://github.com/875638477/005lib", "https://github.com/875638477/005lib.git"):
        raise ValueError("Unexpected repository origin")
    readme_to_delete = REPO / "README.md"
    old_remote_readme = read_stable(readme_to_delete)
    if len(old_remote_readme) != 9 or content_info(old_remote_readme)["git_blob_sha1"] != OLD_README_BLOB:
        raise ValueError("Worktree README.md size/blob differs; do not delete")
    source_readme = SOURCE_LOG / "README.txt"
    source_prepare = SOURCE_LOG / "prepare_repository_snapshot.py"
    baseline_record_bytes = {}
    for path in (source_readme, source_prepare):
        relative = path.relative_to(SOURCE).as_posix()
        if relative not in indexed:
            raise ValueError(f"Expected an existing source record manifest row: {relative}")
        raw = read_stable(path)
        info = content_info(raw)
        if any(str(info[key]) != indexed[relative][key] for key in ("bytes", "sha256", "git_blob_sha1")):
            raise ValueError(f"Existing source record differs from snapshot: {relative}")
        if read_stable(REPO / relative) != raw:
            raise ValueError(f"Existing worktree record differs: {relative}")
        baseline_record_bytes[relative] = raw
    prepare_raw = read_stable(WORK / "prepare_repository_snapshot.py")
    if prepare_raw != baseline_record_bytes[source_prepare.relative_to(SOURCE).as_posix()]:
        raise ValueError("Workspace snapshot script differs from the archived original")
    script_raw = read_stable(Path(__file__).resolve())
    new_names = ("mirror_policy.json", Path(__file__).name)
    for name in new_names:
        if (SOURCE_LOG / name).exists() or (REPO_LOG / name).exists() or (REL_LOG / name).as_posix() in indexed:
            raise ValueError(f"Refusing to overwrite an unexpected pre-existing amendment record: {name}")
    timestamp = datetime.now(timezone.utc).isoformat()
    previous_proof_sha256 = content_info(old_proof_raw)["sha256"]
    changed = {
        source_readme.relative_to(SOURCE).as_posix(): replace_policy(baseline_record_bytes[source_readme.relative_to(SOURCE).as_posix()], "source README.txt"),
        source_prepare.relative_to(SOURCE).as_posix(): replace_policy(prepare_raw, "workspace snapshot script"),
        (REL_LOG / Path(__file__).name).as_posix(): script_raw,
    }
    policy = {
        "status": "PASS_USER_AUTHORIZED_REMOTE_MIRROR_POLICY_RECORDED",
        "recorded_at_utc": timestamp, "user_instruction": USER_INSTRUCTION,
        "local_source_root": str(SOURCE), "repository": "https://github.com/875638477/005lib",
        "final_repository_root_directories": sorted(DIRECTORIES),
        "relative_paths": "Nine 01 directories are direct children of the repository root; internal source paths stay unchanged, with the already verified .git test-fixture ZIP compatibility exception.",
        "original_base_commit": BASE, "original_base_tree": [{"relative": "README.md", "bytes": 9, "git_blob_sha1": OLD_README_BLOB}],
        "remote_deletions": [{"path": "README.md", "bytes": 9, "git_blob_sha1": OLD_README_BLOB}],
        "authorized_worktree_deletion": {"absolute": str(readme_to_delete), "relative": "README.md", "bytes": 9, "git_blob_sha1": OLD_README_BLOB},
        "deletion_scope": "Only the exact verified worktree-root README.md is deleted; no source file or library is deleted. Original remote history remains in BASE; later publication uses a normal descendant commit.",
        "previous_snapshot_proof_sha256": previous_proof_sha256,
        "previous_upload_manifest_sha256": old_manifest_info["sha256"],
        "changed_source_record_paths": sorted([*changed, (REL_LOG / "mirror_policy.json").as_posix()]),
        "validation_boundary": "The original completed full snapshot remains the proof for every untouched manifest row. Only these four maintenance records are incrementally hashed and copied. No full-library scan or rehash is repeated.",
    }
    changed[(REL_LOG / "mirror_policy.json").as_posix()] = json_bytes(policy)
    updates = {}
    changes_report = []
    for relative, raw in changed.items():
        info = content_info(raw)
        if info["bytes"] > LIMIT:
            raise ValueError("An amendment record exceeds 100MiB")
        updates[relative] = {"source": str(SOURCE / relative), "repository_relative": relative, **info}
        changes_report.append({"repository_relative": relative, "previous_sha256": indexed.get(relative, {}).get("sha256"), **info})
    # Preserve every unaffected CSV row byte-for-byte and in its original order.
    eol = "\r\n" if physical_lines[0].endswith("\r\n") else "\n"
    new_lines = [b"\xef\xbb\xbf" + physical_lines[0].encode("utf-8")]
    for row, original_line in zip(rows, physical_lines[1:], strict=True):
        relative = row["repository_relative"]
        new_lines.append(csv_row_bytes(updates[relative], eol) if relative in updates else original_line.encode("utf-8"))
    for relative in sorted(set(updates) - set(indexed)):
        new_lines.append(csv_row_bytes(updates[relative], eol))
    new_manifest_raw = b"".join(new_lines)
    updated_rows = [updates.get(row["repository_relative"], row) for row in rows]
    updated_rows += [updates[relative] for relative in sorted(set(updates) - set(indexed))]
    new_manifest_info = content_info(new_manifest_raw)
    proof.update({
        "manifest_files": len(updated_rows), "manifest_source_bytes": sum(int(row["bytes"]) for row in updated_rows),
        "largest_manifest_file_bytes": max(int(row["bytes"]) for row in updated_rows),
        "manifest_sha256": new_manifest_info["sha256"], "manifest_git_blob_sha1": new_manifest_info["git_blob_sha1"],
        "last_amended_utc": timestamp,
        "snapshot_amendment": {
            "status": "PASS_INCREMENTAL_MIRROR_POLICY_RECORD_AMENDMENT", "amended_at_utc": timestamp,
            "user_instruction": USER_INSTRUCTION, "previous_snapshot_proof_sha256": previous_proof_sha256,
            "previous_manifest_sha256": old_manifest_info["sha256"], "original_base_commit": BASE,
            "changed_records": sorted(changes_report, key=lambda row: row["repository_relative"]),
            "unchanged_original_manifest_rows": len(rows) - len(set(updates) & set(indexed)),
            "unchanged_row_preservation": "Every unaffected original CSV row is preserved byte-for-byte and in its original order; its original full snapshot verification remains in force.",
            "worktree_readme_deleted": policy["authorized_worktree_deletion"],
            "source_library_files_deleted": 0, "source_library_files_modified": False,
            "validation": "Only the four named maintenance records are incrementally copied and compared by bytes, SHA256 and Git blob SHA1; both generated self-reference outputs are separately copied/read back. No repeated full-library hashing.",
        },
    })
    proof["coverage"]["remote_mirror_policy"] = "Final repository root contains exactly the nine local 01 directories; the original remote-only root README.md is removed by explicit user instruction. Prior history is retained."
    proof["per_file_validation"] += " A later authorized mirror-policy amendment incrementally reverified the four named maintenance records; all untouched original rows retain their completed snapshot proof."
    new_proof_raw = json_bytes(proof)
    if len(new_manifest_raw) > LIMIT or len(new_proof_raw) > LIMIT:
        raise ValueError("Generated manifest/proof exceeds 100MiB")
    # Recheck the exact original inputs immediately before the bounded mutation.
    if read_stable(WORK / "snapshot_verification.json") != old_proof_raw or read_stable(WORK / "upload_manifest.csv") != old_manifest_raw:
        raise ValueError("Original snapshot proof/manifest changed during planning")
    for relative, before in baseline_record_bytes.items():
        if read_stable(SOURCE / relative) != before or read_stable(REPO / relative) != before:
            raise ValueError("A source/worktree maintenance record changed during planning")
    if read_stable(WORK / "prepare_repository_snapshot.py") != prepare_raw or read_stable(Path(__file__).resolve()) != script_raw:
        raise ValueError("A workspace script changed during planning")
    write_exact(WORK / "prepare_repository_snapshot.py", changed[source_prepare.relative_to(SOURCE).as_posix()])
    write_exact(WORK / "mirror_policy.json", changed[(REL_LOG / "mirror_policy.json").as_posix()])
    for relative, raw in changed.items():
        write_exact(SOURCE / relative, raw)
        copy_verified(SOURCE / relative, REPO / relative, raw)
    # The one deletion target is a literal exact path, not a manifest-derived path.
    if readme_to_delete != Path(r"D:\001DIY\004computer\lga1700\git_upload_005lib_20261025\repository\README.md"):
        raise ValueError("Unexpected computed README deletion target")
    current_readme = read_stable(readme_to_delete)
    if len(current_readme) != 9 or content_info(current_readme)["git_blob_sha1"] != OLD_README_BLOB:
        raise ValueError("Worktree README changed before deletion")
    readme_to_delete.unlink()
    if readme_to_delete.exists():
        raise ValueError("Verified worktree README still exists after deletion")
    for name, raw in (("upload_manifest.csv", new_manifest_raw), ("snapshot_verification.json", new_proof_raw)):
        write_exact(WORK / name, raw)
        copy_verified(WORK / name, SOURCE_LOG / name, raw)
        copy_verified(WORK / name, REPO_LOG / name, raw)
    for relative, raw in changed.items():
        if content_info(read_stable(SOURCE / relative)) != content_info(raw) or content_info(read_stable(REPO / relative)) != content_info(raw):
            raise ValueError("Amended source/worktree record changed during final publication")
    print(json.dumps({"status": proof["snapshot_amendment"]["status"], "changed_records": sorted(changed), "manifest_files": len(updated_rows), "manifest_sha256": new_manifest_info["sha256"], "previous_snapshot_proof_sha256": previous_proof_sha256, "new_snapshot_proof_sha256": content_info(new_proof_raw)["sha256"], "deleted_worktree_path": str(readme_to_delete), "source_files_deleted": 0}, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    main()
