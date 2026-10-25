"""Apply the user's explicit 13 fixture-directory renames and refresh payload."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat
import zipfile

from prepare_fix_records import WORK, SOURCE, LOG, REL, BASE_TREE, git, require, json_bytes, update_tree, tree_entries


def confined(path):
    resolved = path.resolve()
    require(resolved.is_relative_to((SOURCE / "01AIEDA/learning/staging/cleanup_review_20261019").resolve()), "Rename outside the approved test fixture tree")
    return resolved


def main():
    require(not (LOG / "fixture_directory_renames.json").exists(), "Renames already applied")
    old_task = SOURCE / "01AIEDA/library_maintenance/20261025_github_upload"
    fixtures = json.loads((old_task / "git_test_fixtures_verification.json").read_text(encoding="utf-8"))
    archive = old_task / "git_test_fixtures.zip"
    require(hashlib.sha256(archive.read_bytes()).hexdigest() == fixtures["archive_sha256"], "Fixture safety archive changed")
    require(len(fixtures["mapping"]) == 13, "Expected exactly thirteen approved fixture roots")
    moves = []
    with zipfile.ZipFile(archive) as backup:
        require(backup.testzip() is None, "Safety archive CRC failure")
        for mapping in fixtures["mapping"]:
            before = confined(SOURCE / mapping["source_relative"])
            after = confined(before.with_name("git_fixture"))
            require(before.name == ".git" and before.is_dir() and not after.exists(), "Unsafe or colliding rename")
            require(not (before / "HEAD").exists() and not (before / "config").exists(), "A fixture became a real Git repository")
            records = []
            for file in sorted(before.rglob("*")):
                info = file.lstat()
                require(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400, "Link in fixture")
                require(file.is_file(), "Unexpected nested fixture directory")
                data = file.read_bytes()
                require(data == backup.read(file.relative_to(SOURCE).as_posix()), "Fixture bytes differ from verified safety archive")
                records.append({"name": file.relative_to(before).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
            moves.append({"before": before.relative_to(SOURCE).as_posix(), "after": after.relative_to(SOURCE).as_posix(), "files": records})
    # All thirteen absolute source/destination paths have been confined and
    # checked before the first same-parent directory rename is performed.
    for move in moves:
        before, after = SOURCE / move["before"], SOURCE / move["after"]
        before.rename(after)
        require(not before.exists() and after.is_dir(), "Rename readback failed")
        for row in move["files"]:
            data = (after / row["name"]).read_bytes()
            require(len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"], "Renamed fixture bytes changed")
    proof = {"status": "PASS_USER_AUTHORIZED_FIXTURE_RENAMES_BYTES_PRESERVED", "at_utc": datetime.now(timezone.utc).isoformat(),
             "authorization": "User selected local test-directory rename before strict filename/count synchronization", "directories": 13,
             "files": sum(len(m["files"]) for m in moves), "all_file_bytes_unchanged": True,
             "safety_archive_preserved": str(archive), "mapping": moves}
    (LOG / "fixture_directory_renames.json").write_bytes(json_bytes(proof))
    (LOG / "rename_fixtures_and_refresh.py").write_bytes(Path(__file__).read_bytes())
    (LOG / "verify_source_exact.py").write_bytes((WORK / "verify_source_exact.py").read_bytes())
    readme = LOG / "README.txt"
    content = readme.read_text(encoding="utf-8")
    content = content.replace("基准39139个已上传文件，13个Git测试样例目录仍按此前兼容方案无损打包；已核验删除的大备份ZIP不恢复。",
        "基准39139个已上传文件。为满足用户逐文件名称和数量一致的要求，经用户明确同意，将13个历史测试.git目录改名git_fixture，并新增同步其28个原始文件，全部字节不变；旧ZIP作为历史备份保留且两端同名同数。已核验删除的大备份ZIP不恢复。")
    content += "\n严格一致验收：不排除本机任何文件，9个01目录内的所有相对文件名、文件数量及完整内容哈希必须与Git树一致；空目录无法由Git单独表示，原空目录清单仍保留。测试目录改名清单见fixture_directory_renames.json。\n"
    readme.write_text(content, encoding="utf-8")
    plan = json.loads((WORK / "preparation.json").read_text(encoding="utf-8"))
    changes = {item["path"]: Path(item["source"]) for item in plan["payload"]}
    for file in LOG.rglob("*"):
        if file.is_file():
            changes[file.relative_to(SOURCE).as_posix()] = file
    for move in moves:
        for row in move["files"]:
            path = SOURCE / move["after"] / row["name"]
            changes[path.relative_to(SOURCE).as_posix()] = path
    blobs = {}
    payload = []
    for name, file in sorted(changes.items()):
        data = file.read_bytes()
        oid = git("hash-object", "-w", "--stdin", data=data).decode().strip()
        blobs[name] = oid
        payload.append({"path": name, "source": str(file), "mode": "100644", "blob": oid,
                        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    tree = update_tree(BASE_TREE, blobs)
    count = sum(bool(x) for x in git("ls-tree", "-r", "-z", tree).split(b"\0"))
    baseline, desired = tree_entries(BASE_TREE), tree_entries(tree)
    require(set(baseline) == set(desired) and all(desired[n] == v for n, v in baseline.items() if n != "01AIEDA"), "Non-AI library subtree changed")
    plan.update({"expected_library_tree": tree, "expected_library_file_count": count,
                 "strict_every_local_file_required": True, "fixture_rename_directories": 13, "fixture_rename_files": 28, "payload": payload})
    (WORK / "preparation.json").write_bytes(json_bytes(plan))
    print(json.dumps({"status": proof["status"], "renamed_directories": 13, "renamed_files": proof["files"],
                      "expected_library_tree": tree, "expected_library_file_count": count, "payload_files": len(payload)}, indent=2))


if __name__ == "__main__":
    main()
