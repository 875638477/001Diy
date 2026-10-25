"""Archive the completed migration/deletion evidence and publish only records.

Final commit proof is workspace-only to avoid changing source files after their
last committed snapshot. Every earlier local library file remains identical.
"""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import os

from publish_helper import api, blob, require, WORK, TARGET
from prepare_fix_records import SOURCE, LOG, REL, git, update_tree, tree_entries


def main():
    require(not (WORK / "final_destination_result.json").exists(), "Completion already published")
    plan = json.loads((WORK / "preparation.json").read_text(encoding="utf-8"))
    verified = json.loads((WORK / "verification_result.json").read_text(encoding="utf-8"))
    deleted = json.loads((WORK / "repository_deletion_result.json").read_text(encoding="utf-8"))
    exact = json.loads((WORK / "exact_source_verification.json").read_text(encoding="utf-8"))
    require(deleted["status"].startswith("PASS_WRONG_STANDALONE"), "Wrong repository was not deleted")
    require(exact["status"] == "PASS_EVERY_LOCAL_FILENAME_COUNT_SIZE_AND_CONTENT_MATCHES"
            and exact["library_tree"] == plan["expected_library_tree"] and exact["excluded_files"] == 0
            and exact["files"] == plan["expected_library_file_count"], "No complete strict local verification")
    parent = verified["migration_commit"]
    require(api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"] == parent, "Target main changed")
    old_commit = api(f"repos/{TARGET}/git/commits/{parent}")
    old_root = {row["path"]: (row["mode"], row["type"], row["sha"]) for row in api(f"repos/{TARGET}/git/trees/{old_commit['tree']['sha']}")["tree"]}
    require(old_root["005lib"] == ("040000", "tree", plan["expected_library_tree"]), "Unexpected existing library tree")
    records = ["preparation.json", "helper_publication.json", "verification_result.json", "repository_deletion_result.json",
               "payload_manifest.json", "migration_workflow.yml", "runner.py", "publish_helper.py", "verify_migration.py",
               "delete_wrong_repository.py", "publish_completion.py", "migration_actions_logs.zip",
               "helper_publication_attempt1.json", "migration_workflow_attempt1.yml", "migration_actions_attempt1_logs.zip",
               "migration_retry_record.json", "retry_migration.py", "post_migration_independent_review.json",
               "final_cli_readiness_review.json"]
    for name in records:
        data = (WORK / name).read_bytes()
        (LOG / name).write_bytes(data)
    (LOG / "source_verification_before_completion.json").write_bytes((WORK / "exact_source_verification.json").read_bytes())
    (LOG / "source_file_hashes_before_completion.json.gz").write_bytes(
        gzip.compress((WORK / "exact_source_file_hashes.json").read_bytes(), mtime=0))
    (LOG / "README_completion.txt").write_text(
        "GitHub正确目录同步完成\n\n"
        "浏览：https://github.com/875638477/001Diy/tree/main/005lib\n"
        "本机D:/001DIY/005lib的9个01目录位于001Diy仓库的005lib下，名称和内部相对文件路径保持一致。\n"
        "首次完整逐文件核验：39176个文件，零排除，所有名称、数量、字节数和内容哈希通过；随后仅增加本次完成记录并更新当前地址说明。\n"
        "测试目录：经用户同意，13个非真实仓库的历史.git样例目录已改名git_fixture，28个样例文件字节完整保留，两端逐文件对应。历史ZIP及原审计记录均保留且两端一致。\n"
        "远端005lib旧11个顶层项目已移除，当前只含本机9个01目录。外层README.md及001Diy原提交历史保持。\n"
        "正确位置迁移提交：" + parent + "\n"
        "错误独立仓库875638477/005lib已按用户指示删除，DELETE返回204、认证读回404；正确仓库保持可读且提交不变。一次性辅助分支已删除，main内无辅助workflow或payload目录。\n"
        "原始阶段证据中的PENDING表示该阶段状态；最终删除结果以repository_deletion_result.json为准。\n"
        "本次完成记录在发布前已写定，最终提交、树和最终文件数由工作目录final_destination_result.json及GitHub历史给出，不再回写源目录以避免自引用。\n",
        encoding="utf-8")
    location = SOURCE / "01AIEDA/GITHUB_LOCATION.txt"
    text = location.read_text(encoding="utf-8")
    text = text.replace("旧独立仓库875638477/005lib为错误位置，迁移核验后删除。", "旧独立仓库875638477/005lib为错误位置，已完成迁移核验并删除。")
    location.write_text(text, encoding="utf-8")
    # Build exact immutable blob replacements from the finalized source records.
    paths = {p.relative_to(SOURCE).as_posix(): p for p in LOG.rglob("*") if p.is_file()}
    paths["01AIEDA/GITHUB_LOCATION.txt"] = location
    changes = {}
    raw_files = {}
    for name, path in sorted(paths.items()):
        data = path.read_bytes()
        oid = git("hash-object", "-w", "--stdin", data=data).decode().strip()
        changes[name] = oid
        raw_files[name] = data
    before = {}
    for row in git("ls-tree", "-r", "-z", plan["expected_library_tree"]).split(b"\0"):
        if row:
            attrs, name = row.split(b"\t", 1)
            before[name.decode("utf-8")] = attrs.decode("ascii").split()[2]
    replacements = {name: oid for name, oid in changes.items() if before.get(name) != oid}
    expected_library = update_tree(plan["expected_library_tree"], replacements)
    roots_before = tree_entries(plan["expected_library_tree"])
    roots_after = tree_entries(expected_library)
    require(set(roots_before) == set(roots_after) and all(roots_after[n] == v for n, v in roots_before.items() if n != "01AIEDA"), "Library assets changed")
    desired_root = dict(old_root)
    desired_root["005lib"] = ("040000", "tree", expected_library)
    root_raw = b"".join(f"{mode} {kind} {oid}\t".encode("ascii") + name.encode("utf-8") + b"\0"
                        for name, (mode, kind, oid) in desired_root.items())
    expected_root = git("mktree", "-z", "--missing", data=root_raw).decode().strip()
    cached = json.loads((WORK / "exact_source_file_hashes.json").read_text(encoding="utf-8"))
    expected_hashes = {name: row["blob"] for name, row in cached.items()}
    expected_hashes.update(replacements)
    prepared_entries = {}
    for row in git("ls-tree", "-r", "-z", expected_library).split(b"\0"):
        if row:
            attrs, name = row.split(b"\t", 1)
            mode, kind, oid = attrs.decode("ascii").split()
            require(mode == "100644" and kind == "blob", "Unexpected prepared file mode")
            prepared_entries[name.decode("utf-8")] = oid
    require(expected_hashes == prepared_entries, "Prepared whole file tree differs from the complete source verification and explicit records")
    local_paths = {}
    for directory in SOURCE.iterdir():
        if directory.is_dir() and directory.name.startswith("01"):
            for folder, dirs, names in os.walk(directory, followlinks=False):
                for name in names:
                    path = Path(folder) / name
                    local_paths[path.relative_to(SOURCE).as_posix()] = path
    require(set(local_paths) == set(expected_hashes), "Current source names/count differ from the final desired file set")
    cutoff_ns = int(datetime.fromisoformat(plan["prepared_at_utc"]).timestamp() * 1_000_000_000)
    for name, path in local_paths.items():
        info = path.stat()
        if name in replacements or info.st_mtime_ns > cutoff_ns:
            raw = path.read_bytes()
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            require(oid == expected_hashes[name], "A current source file changed after verification: " + name)
        elif name in cached:
            require(info.st_size == cached[name]["bytes"], "An older local file changed size: " + name)
    uploaded = set()
    entries = []
    for name, oid in sorted(replacements.items()):
        if oid not in uploaded:
            require(blob(raw_files[name]) == oid, "Completion API blob differs")
            uploaded.add(oid)
        entries.append({"path": "005lib/" + name, "mode": "100644", "type": "blob", "sha": oid})
    tree = api(f"repos/{TARGET}/git/trees", "POST", {"base_tree": old_commit["tree"]["sha"], "tree": entries})
    require(tree["sha"] == expected_root, "Whole target root digest differs")
    new_commit = api(f"repos/{TARGET}/git/commits", "POST", {
        "message": "Record verified library destination correction and remove mistaken repository", "tree": expected_root, "parents": [parent]})
    require([row["sha"] for row in new_commit["parents"]] == [parent], "Completion parent differs")
    require(api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"] == parent, "Target main advanced before record publication")
    final_sha = new_commit["sha"]
    api(f"repos/{TARGET}/git/refs/heads/main", "PATCH", {"sha": final_sha, "force": False})
    require(api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"] == final_sha, "Final main readback differs")
    actual_root = {row["path"]: (row["mode"], row["type"], row["sha"]) for row in api(f"repos/{TARGET}/git/trees/{expected_root}")["tree"]}
    require(actual_root == desired_root, "Final root entries differ")
    final_entries = {}
    for row in git("ls-tree", "-r", "-z", expected_library).split(b"\0"):
        if row:
            attrs, name = row.split(b"\t", 1)
            mode, kind, oid = attrs.decode("ascii").split()
            require(mode == "100644" and kind == "blob", "Unexpected final file mode")
            final_entries[name.decode("utf-8")] = oid
    # Cached hashes cover every previously validated file; only the explicit
    # new/changed completion records need new reads and hashes.
    require(expected_hashes == final_entries, "Final whole file tree differs from verified source plus exact completion records")
    for name, raw in raw_files.items():
        require(paths[name].read_bytes() == raw, "Source completion record changed after publishing")
    result = {"status": "PASS_FINAL_CORRECT_DESTINATION_AND_LOCAL_FILE_MIRROR", "completed_at_utc": datetime.now(timezone.utc).isoformat(),
              "correct_url": plan["correct_url"], "repository": TARGET, "branch": "main", "commit": final_sha,
              "root_tree": expected_root, "library_tree": expected_library, "files": len(final_entries),
              "nine_directories": sorted(roots_after), "excluded_local_files": 0,
              "all_previously_validated_file_names_and_contents_preserved_except_explicit_completion_records": True,
              "completion_records_changed_or_added": len(replacements), "source_completion_files_byte_verified": len(raw_files),
              "outside_005lib_unchanged": True, "helper_branch_deleted": True,
              "wrong_repository_deleted": True, "wrong_repository": "875638477/005lib",
              "deletion_http_status": 204, "deletion_authenticated_readback_http_status": 404,
              "fixture_directories_renamed": 13, "fixture_file_bytes_preserved": 28,
              "migration_commit": parent, "source_records_finalized_before_commit": True,
              "final_proof_boundary": "Workspace only, no source mutation after the final published snapshot."}
    (WORK / "final_destination_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
