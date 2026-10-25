"""Prepare the authorized 005lib snapshot; never run Git or modify source libraries.

Execution writes maintenance records outside the default workspace and therefore
must use the caller's approved elevated filesystem invocation. Review first.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import zipfile
import zlib


WORK = Path(r"D:\001DIY\004computer\lga1700\git_upload_005lib_20261025")
SOURCE = Path(r"D:\001DIY\005lib")
REPOSITORY = WORK / "repository"
RECORD_RELATIVE = Path("01AIEDA/library_maintenance/20261025_github_upload")
RECORD = SOURCE / RECORD_RELATIVE
EXPECTED_DIRECTORIES = (
    "01aeLib", "01AIEDA", "01brdlib", "01captureLib", "01env",
    "01Pad_lib", "01Psm_lib", "01script_file", "01_3d_step_lib",
)
REMOVED_ARCHIVE = SOURCE / "01AIEDA/library_maintenance/20261025_pad_psm_merge/cadence_library_maintenance_20261025_full.zip"
SELF_OUTPUT_NAMES = ("upload_manifest.csv", "snapshot_verification.json")
SELF_OUTPUT_RELATIVES = {RECORD_RELATIVE / name for name in SELF_OUTPUT_NAMES}
MAX_GIT_FILE_BYTES = 100 * 1024 * 1024
SCAN_REPORT_NAMES = (
    "sensitive_scan_report.json", "sensitive_env_rar_report.json",
    "sensitive_unquoted_config_report.json",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def reject_reparse(path: Path) -> os.stat_result:
    result = path.stat(follow_symlinks=False)
    if stat.S_ISLNK(result.st_mode) or getattr(result, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError(f"Reparse point or symbolic link is forbidden: {path}")
    return result


def validate_exact_path(path: Path, *, directory: bool = True) -> None:
    if not path.is_absolute():
        raise ValueError(f"Expected an absolute path: {path}")
    for ancestor in reversed((path, *path.parents)):
        reject_reparse(ancestor)
    if path.resolve(strict=True) != path:
        raise ValueError(f"Resolved path differs from the exact authorized path: {path}")
    if directory and not path.is_dir():
        raise ValueError(f"Expected a directory: {path}")


def safe_mkdir(path: Path, root: Path) -> None:
    relative = path.relative_to(root)
    cursor = root
    reject_reparse(cursor)
    for part in relative.parts:
        cursor /= part
        if not cursor.exists():
            cursor.mkdir()
        reject_reparse(cursor)
        if not cursor.is_dir():
            raise ValueError(f"Expected a directory while preparing destination: {cursor}")


def walk_plain(root: Path) -> tuple[list[Path], list[Path]]:
    directories, files, pending = [], [], [root]
    while pending:
        current = pending.pop()
        info = reject_reparse(current)
        if not stat.S_ISDIR(info.st_mode):
            raise ValueError(f"Directory changed type: {current}")
        directories.append(current)
        with os.scandir(current) as entries:
            for entry in sorted(entries, key=lambda e: e.name.casefold()):
                path = Path(entry.path)
                info = reject_reparse(path)
                if stat.S_ISDIR(info.st_mode):
                    pending.append(path)
                elif stat.S_ISREG(info.st_mode):
                    files.append(path)
                else:
                    raise ValueError(f"Unsupported filesystem object: {path}")
    return sorted(directories), sorted(files)


def source_tree() -> tuple[list[Path], list[Path]]:
    actual = sorted(p.name for p in SOURCE.iterdir() if p.is_dir() and p.name.startswith("01"))
    if actual != sorted(EXPECTED_DIRECTORIES):
        raise ValueError(f"Top-level 01 directory scope changed: {actual}")
    directories, files = [], []
    for name in EXPECTED_DIRECTORIES:
        d, f = walk_plain(SOURCE / name)
        directories.extend(d)
        files.extend(f)
    seen = set()
    for path in directories + files:
        relative = path.relative_to(SOURCE).as_posix()
        if relative.casefold() in seen:
            raise ValueError(f"Case-insensitive path collision: {relative}")
        seen.add(relative.casefold())
    return sorted(directories), sorted(files)


def signature(info: os.stat_result) -> tuple[int, int, int, int, int]:
    return info.st_size, info.st_mtime_ns, info.st_ctime_ns, info.st_dev, info.st_ino


def hash_file(path: Path) -> dict[str, object]:
    before = reject_reparse(path)
    if not stat.S_ISREG(before.st_mode):
        raise ValueError(f"Not a regular file: {path}")
    sha256 = hashlib.sha256()
    git_blob = hashlib.sha1(b"blob " + str(before.st_size).encode("ascii") + b"\0")
    crc = 0
    read = 0
    with path.open("rb") as stream:
        while chunk := stream.read(4 * 1024 * 1024):
            read += len(chunk)
            sha256.update(chunk)
            git_blob.update(chunk)
            crc = zlib.crc32(chunk, crc)
    after = reject_reparse(path)
    if signature(before) != signature(after) or read != before.st_size:
        raise ValueError(f"File changed while hashing: {path}")
    return {"bytes": read, "sha256": sha256.hexdigest(), "git_blob_sha1": git_blob.hexdigest(), "crc32": f"{crc & 0xFFFFFFFF:08x}", "signature": signature(after)}


def verified_copy(source: Path, destination: Path, destination_root: Path) -> dict[str, object]:
    source_info = hash_file(source)
    safe_mkdir(destination.parent, destination_root)
    if destination.exists():
        existing = reject_reparse(destination)
        if not stat.S_ISREG(existing.st_mode):
            raise ValueError(f"Copy destination is not a regular file: {destination}")
    shutil.copy2(source, destination)
    target_info = hash_file(destination)
    if signature(reject_reparse(source)) != tuple(source_info["signature"]):
        raise ValueError(f"Source changed during copy: {source}")
    for key in ("bytes", "sha256", "git_blob_sha1"):
        if source_info[key] != target_info[key]:
            raise ValueError(f"Source/destination content mismatch ({key}): {source}")
    return source_info


def write_json(path: Path, value: object) -> None:
    if path.exists():
        reject_reparse(path)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> object:
    reject_reparse(path)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def is_fixture(path: Path) -> bool:
    return any(part.casefold() == ".git" for part in path.relative_to(SOURCE).parts)


def validate_fixtures(directories: list[Path], files: list[Path], inventory: dict) -> list[Path]:
    if any(p.name.casefold() == ".git" for p in files):
        raise ValueError("Unexpected .git regular file; do not silently omit it")
    expected = {str(entry["relative"]).replace("\\", "/") for entry in inventory["gitEntries"]}
    if len(expected) != 13 or any(not entry["isDirectory"] for entry in inventory["gitEntries"]):
        raise ValueError("Expected exactly the 13 inventoried .git test fixture directories")
    actual_paths = [p for p in directories if p.name.casefold() == ".git"]
    actual = {p.relative_to(SOURCE).as_posix() for p in actual_paths}
    if actual != expected:
        raise ValueError("Live .git test fixtures differ from the reviewed original inventory")
    return sorted(actual_paths)


def prepare_fixture_archive(directories: list[Path], files: list[Path], fixture_roots: list[Path]) -> dict:
    archive_path = WORK / "git_test_fixtures.zip"
    manifest_path = WORK / "git_test_fixtures_manifest.csv"
    fixture_directories = [p for p in directories if is_fixture(p)]
    fixture_files = [p for p in files if is_fixture(p)]
    rows, expected_names = [], set()
    for path in fixture_directories:
        arcname = path.relative_to(SOURCE).as_posix() + "/"
        expected_names.add(arcname)
        rows.append({"source": str(path), "archive_relative": arcname, "kind": "directory", "bytes": 0, "sha256": "", "crc32": "00000000"})
    source_hashes = {path: hash_file(path) for path in fixture_files}
    for path, content in source_hashes.items():
        arcname = path.relative_to(SOURCE).as_posix()
        expected_names.add(arcname)
        rows.append({"source": str(path), "archive_relative": arcname, "kind": "file", **{k: content[k] for k in ("bytes", "sha256", "crc32")}})
    if archive_path.exists():
        reject_reparse(archive_path)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, strict_timestamps=False) as archive:
        for path in fixture_directories + fixture_files:
            relative = path.relative_to(SOURCE).as_posix()
            archive.write(path, relative + "/" if path.is_dir() else relative)
    with zipfile.ZipFile(archive_path) as archive:
        infos = archive.infolist()
        if len(infos) != len(expected_names) or {i.filename for i in infos} != expected_names:
            raise ValueError("Fixture ZIP member set differs from the source paths")
        for row in rows:
            info = archive.getinfo(row["archive_relative"])
            if row["kind"] == "directory":
                if not info.is_dir():
                    raise ValueError(f"Fixture ZIP directory marker missing: {info.filename}")
                continue
            digest = hashlib.sha256()
            crc, count = 0, 0
            with archive.open(info) as member:
                while chunk := member.read(1024 * 1024):
                    digest.update(chunk)
                    crc = zlib.crc32(chunk, crc)
                    count += len(chunk)
            if count != row["bytes"] or digest.hexdigest() != row["sha256"] or f"{crc & 0xFFFFFFFF:08x}" != row["crc32"] or info.CRC != crc & 0xFFFFFFFF:
                raise ValueError(f"Fixture ZIP CRC/SHA-256 verification failed: {info.filename}")
    for path, content in source_hashes.items():
        if signature(reject_reparse(path)) != tuple(content["signature"]):
            raise ValueError(f"Fixture source changed while archiving: {path}")
    with manifest_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["source", "archive_relative", "kind", "bytes", "sha256", "crc32"])
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["archive_relative"]))
    archive_content = hash_file(archive_path)
    if archive_content["bytes"] > MAX_GIT_FILE_BYTES:
        raise ValueError("Fixture archive exceeds the regular GitHub file limit")
    report = {
        "status": "PASS_ALL_FIXTURE_PATHS_EMPTY_DIRECTORIES_CRC_AND_SHA256",
        "fixture_root_count": len(fixture_roots), "directory_entries": len(fixture_directories),
        "regular_file_entries": len(fixture_files), "source_files_unmodified": True,
        "archive_relative": (RECORD_RELATIVE / archive_path.name).as_posix(),
        "archive_bytes": archive_content["bytes"], "archive_sha256": archive_content["sha256"],
        "mapping": [{"source_relative": p.relative_to(SOURCE).as_posix(), "archive_member_prefix": p.relative_to(SOURCE).as_posix() + "/"} for p in fixture_roots],
        "preservation": "Each original source-relative path, every regular-file byte and every directory entry (including empty directories) is retained. ZIP member size, CRC32 and SHA256 were checked against live source files. Original .git fixture directories are not altered.",
    }
    write_json(WORK / "git_test_fixtures_verification.json", report)
    for path in (archive_path, manifest_path, WORK / "git_test_fixtures_verification.json"):
        verified_copy(path, RECORD / path.name, SOURCE)
    return report


def copy_record_inputs() -> None:
    paths = [Path(__file__).resolve(), WORK / "upload_inventory.json", WORK / "upload_inventory.csv", WORK / "tools/portable_tools_verification.json"]
    paths += [WORK / name for name in SCAN_REPORT_NAMES]
    paths += [WORK / name for name in ("sensitive_scan_findings.csv", "sensitive_scan_review.json", "sensitive_test_zip_report.json", "scan_sensitive_005lib.py", "scan_env_rar_005lib.py", "scan_unquoted_config_005lib.py", "scan_test_zip_fixtures_005lib.py", "inventory_005lib.ps1", "prepare_portable_git_tools.py", "finalize_upload_records.py") if (WORK / name).is_file()]
    for path in paths:
        verified_copy(path, RECORD / path.name, SOURCE)


def verify_fixture_sources() -> None:
    """Read back original fixture bytes again after the main snapshot copy."""
    with (WORK / "git_test_fixtures_manifest.csv").open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            path = Path(row["source"])
            if row["kind"] == "directory":
                if not stat.S_ISDIR(reject_reparse(path).st_mode):
                    raise ValueError(f"Fixture source directory changed: {path}")
                continue
            content = hash_file(path)
            if content["bytes"] != int(row["bytes"]) or content["sha256"] != row["sha256"] or content["crc32"] != row["crc32"]:
                raise ValueError(f"Fixture source bytes changed after archiving: {path}")


def write_readme() -> None:
    text = """GitHub 005lib 上传快照记录（2026-10-25）

源根目录：D:\\001DIY\\005lib
目标仓库：https://github.com/875638477/005lib
仓库根目录对应上述本机源根目录；9 个 01 开头目录直接放在仓库根目录，内部路径保持原样：
01aeLib、01AIEDA、01brdlib、01captureLib、01env、01Pad_lib、01Psm_lib、01script_file、01_3d_step_lib。
包含隐藏文件、原有忽略文件、工具文件和 __pycache__ 文件；不自行清理源文件。
按用户最新指令，以今天本机这 9 个 01 目录为 GitHub 内容基准；删除远端不在该范围内的旧文件，保持目录层级一致。本次经核验原远端仅有根 README.md，因此删除该旧文件，最终仓库根仅保留这 9 个目录。快照脚本只复制和验证，不执行 Git add、commit 或 push。

Git 兼容归档特例：13 个历史测试样本 .git 目录不直接进入 Git 工作树。
它们的原相对路径、所有文件内容和包括空目录在内的目录项无损保存在本目录 git_test_fixtures.zip。
git_test_fixtures_manifest.csv 记录逐项映射，git_test_fixtures_verification.json 记录 CRC32/SHA256 读回核验。
这些源测试目录保持原样。解压到本机源根目录可恢复原路径；请勿将其直接添加至版本库。

upload_manifest.csv 逐项记录源绝对路径、仓库相对路径、字节数、SHA256 和原始 Git blob SHA1。
每项均对源文件与工作树副本进行 SHA256 比对；复制使用 copy2 保留通常文件时间和属性。
Git blob SHA1 是文件原始字节的哈希；后续 Git 应关闭换行转换并核对索引 blob。
源目录中已有的 .gitignore 不构成快照排除规则；后续应将清单中所有文件纳入提交。
普通空目录会在工作树复制阶段保留，并在 empty_directories.json 中记录；Git 本身不记录普通空目录。

覆盖边界：upload_manifest.csv 和 snapshot_verification.json 为枚举结束后生成的两份自引用输出，
不列入 upload_manifest.csv 自身；生成后另行复制到源记录目录及仓库记录目录并逐份核验 SHA256。
13 个 .git 测试目录的原文件不逐项复制到工作树，而在上述 ZIP 及 ZIP 成员清单中验证保存。
其他全部源文件均应列入上传清单。快照后的修改、后续 Git 压缩包及认证数据不在快照范围内。
本次不将便携 Git/gh/LFS 可执行文件写入源库，仅保留官方下载校验证据。

upload_inventory.json/csv 是准备开始时的原始盘点，可能包含后来按用户指示删除的重复备份 ZIP，
当前快照以 upload_manifest.csv 和 snapshot_verification.json 为准。
备份 ZIP 核验及删除记录见 README_backup_removal.txt、backup_zip_removal.json。
敏感内容扫描报告及复核记录保留在本目录；执行前必须完成上层人工复核。
"""
    path = RECORD / "README.txt"
    begin = b"\n\n--- BEGIN 20261025_GITHUB_UPLOAD_SNAPSHOT ---\n"
    end = b"--- END 20261025_GITHUB_UPLOAD_SNAPSHOT ---\n"
    section = begin + text.encode("utf-8") + end
    if path.exists():
        reject_reparse(path)
        before = path.read_bytes()
        if begin in before or end in before:
            if before.count(begin) != 1 or before.count(end) != 1:
                raise ValueError("Existing task README has ambiguous upload section markers")
            start = before.index(begin)
            stop = before.index(end) + len(end)
            if stop < start:
                raise ValueError("Existing task README upload markers have reversed order")
            after = before[:start] + section + before[stop:]
        else:
            backup = RECORD / "README_before_upload.txt"
            if backup.exists() and backup.read_bytes() != before:
                raise ValueError("Existing README backup differs; preserve and review it before merging")
            verified_copy(path, backup, SOURCE)
            # Keep every original byte, including its encoding/newline choices.
            after = before + section
    else:
        after = section
    path.write_bytes(after)


def copy_snapshot_file(path: Path) -> dict[str, object]:
    relative = path.relative_to(SOURCE)
    content = verified_copy(path, REPOSITORY / relative, REPOSITORY)
    if content["bytes"] > MAX_GIT_FILE_BYTES:
        raise ValueError(f"File exceeds the regular GitHub file limit: {relative}")
    return {"source": str(path), "repository_relative": relative.as_posix(), **{k: content[k] for k in ("bytes", "sha256", "git_blob_sha1")}, "signature": content["signature"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sensitive-review-approved", action="store_true", help="Explicitly attest that the caller has reviewed all scanning findings and coverage exceptions")
    args = parser.parse_args()
    if not args.sensitive_review_approved:
        parser.error("Complete review first, then pass --sensitive-review-approved")
    started = utc_now()
    for root in (WORK, SOURCE, REPOSITORY):
        validate_exact_path(root)
    if Path(__file__).resolve() != WORK / "prepare_repository_snapshot.py":
        raise ValueError("Run only the reviewed script at its exact workspace path")
    if REPOSITORY.is_relative_to(SOURCE) or SOURCE.is_relative_to(REPOSITORY) or WORK.is_relative_to(SOURCE):
        raise ValueError("Source, workspace output and repository roots must not overlap")
    validate_exact_path(REPOSITORY / ".git")
    # Inspect destination including its real root .git before any copying, without changing it.
    repository_directories, repository_files = walk_plain(REPOSITORY)
    if any(p.name.casefold() == ".git" and p != REPOSITORY / ".git" for p in repository_directories) or any(p.name.casefold() == ".git" for p in repository_files):
        raise ValueError("Unexpected nested .git metadata already exists in destination")
    inventory = read_json(WORK / "upload_inventory.json")
    if inventory["sourceRoot"] != str(SOURCE) or inventory.get("scanErrors") or inventory.get("reparsePoints"):
        raise ValueError("Original inventory root/errors/reparse state is unexpected")
    removal = read_json(RECORD / "backup_zip_removal.json")
    if removal.get("status") != "PASS_BACKUP_ZIP_REMOVED_ORIGINALS_RETAINED" or REMOVED_ARCHIVE.exists():
        raise ValueError("Wait for the separately verified duplicate backup ZIP removal")
    scan_reports = {name: read_json(WORK / name) for name in SCAN_REPORT_NAMES}
    if "stats" not in scan_reports["sensitive_scan_report.json"] or "findings" not in scan_reports["sensitive_scan_report.json"]:
        raise ValueError("Main sensitive scan report is incomplete")
    directories, files = source_tree()
    fixtures = validate_fixtures(directories, files, inventory)
    oversized = [str(p) for p in files if p.stat().st_size > MAX_GIT_FILE_BYTES]
    if oversized:
        raise ValueError(f"Live source has files over 100MiB: {oversized}")
    safe_mkdir(RECORD, SOURCE)
    fixture_report = prepare_fixture_archive(directories, files, fixtures)
    copy_record_inputs()
    write_readme()
    directories, files = source_tree()
    ordinary_directories = [p for p in directories if not is_fixture(p)]
    ordinary_files = [p for p in files if not is_fixture(p) and p.relative_to(SOURCE) not in SELF_OUTPUT_RELATIVES]
    has_child = {p.parent for p in ordinary_directories + ordinary_files}
    empty_directories = sorted(p.relative_to(SOURCE).as_posix() for p in ordinary_directories if p not in has_child)
    write_json(RECORD / "empty_directories.json", {"source_relative_empty_directories": empty_directories, "git_boundary": "Ordinary empty directory names are recorded here because Git does not track empty directories. The .git test fixtures are preserved separately in ZIP."})
    # This final enumeration is fixed. Generated manifest/report names are excluded exactly,
    # not with a broad glob; subsequent output copying cannot recursively enter the manifest.
    directories, files = source_tree()
    fixtures_after = validate_fixtures(directories, files, inventory)
    if fixtures_after != fixtures:
        raise ValueError("Fixture root set changed during preparation")
    ordinary_directories = [p for p in directories if not is_fixture(p)]
    snapshot_files = [p for p in files if not is_fixture(p) and p.relative_to(SOURCE) not in SELF_OUTPUT_RELATIVES]
    expected_paths = {p.relative_to(SOURCE).as_posix() for p in snapshot_files}
    for directory in ordinary_directories:
        safe_mkdir(REPOSITORY / directory.relative_to(SOURCE), REPOSITORY)
    records = []
    print(json.dumps({"phase": "copy_and_verify_source_to_repository", "files": len(snapshot_files)}), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(copy_snapshot_file, path) for path in snapshot_files]
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            records.append(future.result())
            if index % 1000 == 0 or index == len(snapshot_files):
                print(json.dumps({"phase": "copy_and_verify_source_to_repository", "completed": index, "total": len(snapshot_files)}), flush=True)
    records.sort(key=lambda row: row["repository_relative"])
    manifest = WORK / "upload_manifest.csv"
    if manifest.exists():
        reject_reparse(manifest)
    fields = ["source", "repository_relative", "bytes", "sha256", "git_blob_sha1"]
    with manifest.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    # Detect added/removed/retouched source files after copying; hashes were checked per item.
    final_directories, final_files = source_tree()
    final_paths = {p.relative_to(SOURCE).as_posix() for p in final_files if not is_fixture(p) and p.relative_to(SOURCE) not in SELF_OUTPUT_RELATIVES}
    initial_all_names = {p.relative_to(SOURCE) for p in files if p.relative_to(SOURCE) not in SELF_OUTPUT_RELATIVES}
    final_all_names = {p.relative_to(SOURCE) for p in final_files if p.relative_to(SOURCE) not in SELF_OUTPUT_RELATIVES}
    if final_paths != expected_paths or final_all_names != initial_all_names or set(final_directories) != set(directories):
        raise ValueError("Source file/directory set changed during snapshot")
    verify_fixture_sources()
    for row in records:
        if signature(reject_reparse(Path(row["source"]))) != tuple(row["signature"]):
            raise ValueError(f"Source file changed after copying: {row['source']}")
    destination_only = []
    for name in EXPECTED_DIRECTORIES:
        _, destination_files = walk_plain(REPOSITORY / name)
        if any(p.stat().st_size > MAX_GIT_FILE_BYTES for p in destination_files):
            raise ValueError("Destination scope contains a file over 100MiB")
        destination_only += [p.relative_to(REPOSITORY).as_posix() for p in destination_files if p.relative_to(REPOSITORY).as_posix() not in expected_paths and p.relative_to(REPOSITORY) not in SELF_OUTPUT_RELATIVES]
    manifest_info = hash_file(manifest)
    report = {
        "status": "PASS_SOURCE_SNAPSHOT_SIZE_SHA256_AND_GIT_BLOB_HASHES_VERIFIED",
        "started_utc": started, "finished_utc": utc_now(),
        "source_root": str(SOURCE), "repository_worktree": str(REPOSITORY),
        "remote": "https://github.com/875638477/005lib", "root_mapping": "Repository root is D:\\001DIY\\005lib; all nine 01 directories are direct children with original internal paths.",
        "top_level_directories": list(EXPECTED_DIRECTORIES),
        "manifest_files": len(records), "manifest_source_bytes": sum(int(row["bytes"]) for row in records),
        "largest_manifest_file_bytes": max((int(row["bytes"]) for row in records), default=0),
        "files_over_100MiB": 0, "source_reparse_points": 0,
        "manifest_sha256": manifest_info["sha256"], "manifest_git_blob_sha1": manifest_info["git_blob_sha1"],
        "per_file_validation": "For every manifest entry, stable source bytes and copied worktree bytes matched in length, SHA256 and raw Git blob SHA1. Source names and stat signatures were checked again at the end.",
        "fixture_archive": fixture_report,
        "empty_directories_record": (RECORD_RELATIVE / "empty_directories.json").as_posix(),
        "preserved_destination_only_files_in_scope": sorted(destination_only),
        "source_library_files_modified": False,
        "source_record_directory_written": str(RECORD),
        "sensitive_review": {"approval": "Caller explicitly passed --sensitive-review-approved after review", "reports": {name: {"sha256": hash_file(WORK / name)["sha256"], "findings": len(value.get("findings", [])), "reported_errors": value.get("errors", [])} for name, value in scan_reports.items()}, "coverage_boundary": "Scanner findings and any archive/error exceptions require caller review; copying is not an additional secret scanner."},
        "coverage": {"included": "All regular files under the nine source directories, including hidden, ignored and pycache files, except exactly the exclusions below.", "compatibility_archive_only": "All contents of the 13 .git test fixture directories, with original relative paths and empty directories verified inside git_test_fixtures.zip; source fixture directories are unchanged.", "self_reference_exclusions": sorted(p.as_posix() for p in SELF_OUTPUT_RELATIVES), "generated_outputs_validation": "The two exact self-reference exclusions are generated in workspace after enumeration, then separately copied to source and repository record folders with SHA256 readback verification.", "ordinary_empty_directories": "Created in the worktree and recorded in empty_directories.json; Git itself does not store empty directories.", "git_actions": "No git add, commit, push or repository configuration changes are performed by this script. Later staging must include ignored files and preserve raw bytes."},
    }
    verification = WORK / "snapshot_verification.json"
    write_json(verification, report)
    for generated in (manifest, verification):
        if generated.stat().st_size > MAX_GIT_FILE_BYTES:
            raise ValueError(f"Generated artifact exceeds 100MiB: {generated}")
        verified_copy(generated, RECORD / generated.name, SOURCE)
        verified_copy(generated, REPOSITORY / RECORD_RELATIVE / generated.name, REPOSITORY)
    # Generated outputs cannot invalidate any already-listed source file.
    for row in records:
        if signature(reject_reparse(Path(row["source"]))) != tuple(row["signature"]):
            raise ValueError(f"Listed source changed while publishing generated outputs: {row['source']}")
    result = {"status": report["status"], "manifest": str(manifest), "verification": str(verification), "files": len(records), "bytes": report["manifest_source_bytes"], "fixture_roots": len(fixtures), "generated_artifacts": [{"relative": (RECORD_RELATIVE / p.name).as_posix(), **{key: hash_file(p)[key] for key in ("bytes", "sha256", "git_blob_sha1")}} for p in (manifest, verification)]}
    print(json.dumps(result, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    main()
