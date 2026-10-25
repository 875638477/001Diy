"""Prepare the corrected GitHub destination records and an exact desired tree.

No remote mutation. Source writes are restricted to 01AIEDA documentation and
this task's new maintenance folder; all existing library blobs are reused.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess

WORK = Path(__file__).resolve().parent
ROOT = WORK.parent
SOURCE = Path(r"D:\001DIY\005lib")
REPO = ROOT / "git_upload_005lib_20261025/repository"
GIT = ROOT / "git_upload_005lib_20261025/tools/mingit/cmd/git.exe"
REL = "01AIEDA/library_maintenance/20261025_github_destination_fix"
LOG = SOURCE / REL
BASE = "98b94676da011958839790566d18575b5793a85f"
BASE_TREE = "96dbcfad837bd1cb2f24b6b16f55655d3c1e58ec"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def git(*args, data=None):
    result = subprocess.run([str(GIT), "-c", f"safe.directory={REPO.as_posix()}",
                             "-c", "gc.auto=0", "-C", str(REPO), *args],
                            input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(result.returncode == 0, result.stderr.decode("utf-8", "replace"))
    return result.stdout


def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def tree_entries(oid):
    out = {}
    for item in git("ls-tree", "-z", oid).split(b"\0"):
        if item:
            attrs, name = item.split(b"\t", 1)
            mode, kind, sha = attrs.decode("ascii").split()
            out[name.decode("utf-8")] = (mode, kind, sha)
    return out


def update_tree(old, changes):
    entries = tree_entries(old) if old else {}
    grouped = {}
    for path, blob in changes.items():
        first, sep, tail = path.partition("/")
        require(first not in ("", ".", "..", ".git"), "Unsafe tree path")
        if sep:
            grouped.setdefault(first, {})[tail] = blob
        else:
            require(first not in grouped, "Directory/file collision")
            entries[first] = ("100644", "blob", blob)
    for name, nested in grouped.items():
        existing = entries.get(name)
        require(existing is None or existing[1] == "tree", "Expected directory")
        entries[name] = ("040000", "tree", update_tree(existing[2] if existing else None, nested))
    raw = b"".join(f"{mode} {kind} {sha}\t".encode("ascii") + name.encode("utf-8") + b"\0"
                   for name, (mode, kind, sha) in sorted(entries.items()))
    return git("mktree", "-z", data=raw).decode().strip()


def main():
    require(git("rev-parse", BASE + "^{tree}").decode().strip() == BASE_TREE, "Baseline tree changed")
    require(not LOG.exists(), "Do not overwrite an existing correction task")
    inventory = json.loads((WORK / "target_inventory.json").read_text(encoding="utf-8"))
    require(inventory["observed_main_commit"] == "30fbcf36722b39852fb24b254f3bc3f995149afb", "Target inventory changed")
    originals = {}
    for name in ("01AIEDA/EDA.md", "01AIEDA/library_maintenance/INDEX.txt"):
        data = (SOURCE / name).read_bytes()
        require(data == git("show", BASE + ":" + name), "Source documentation changed: " + name)
        originals[name] = data
    old = "GitHub同步按本机目录层级进行：仓库根对应D:/001DIY/005lib，9个01目录直接位于仓库根；上传清单、扫描、Git校验和兼容归档见[GitHub上传记录](library_maintenance/20261025_github_upload/README.txt)。"
    new = "GitHub当前正确位置为[001Diy/005lib](https://github.com/875638477/001Diy/tree/main/005lib)：D:/001DIY对应001Diy仓库根，D:/001DIY/005lib对应仓库内005lib子目录，9个01目录位于005lib下。以本机最新目录为准更新此子目录并清理旧项，仓库外层文件保留；见[路径纠正记录](library_maintenance/20261025_github_destination_fix/README.txt)。此前[上传记录](library_maintenance/20261025_github_upload/README.txt)中的独立005lib仓库地址属于历史错误位置。"
    eda = originals["01AIEDA/EDA.md"].decode("utf-8")
    require(eda.count(old) == 1, "Expected one current GitHub mapping paragraph")
    modified = {"01AIEDA/EDA.md": eda.replace(old, new).encode("utf-8")}
    index = originals["01AIEDA/library_maintenance/INDEX.txt"]
    modified["01AIEDA/library_maintenance/INDEX.txt"] = index + (
        "\r\n2026-10-25  GitHub位置纠正：迁移至001Diy仓库的005lib子目录，核验后删除独立005lib误建仓库。\r\n"
        "入口：20261025_github_destination_fix\\README.txt\r\n"
        "当前地址：https://github.com/875638477/001Diy/tree/main/005lib\r\n").encode("utf-8")
    LOG.mkdir(parents=True)
    for name, data in originals.items():
        target = LOG / "documentation_before" / Path(name).name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for name, data in modified.items():
        (SOURCE / name).write_bytes(data)
    (SOURCE / "01AIEDA/GITHUB_LOCATION.txt").write_text(
        "当前GitHub库位置（2026-10-25按用户纠正）\n"
        "https://github.com/875638477/001Diy/tree/main/005lib\n"
        "本机 D:\\001DIY\\005lib 对应 001Diy 仓库内的 005lib 子目录。\n"
        "9个01目录继续保持本机内部层级。旧独立仓库875638477/005lib为错误位置，迁移核验后删除。\n"
        "维护记录：library_maintenance/20261025_github_destination_fix/README.txt\n", encoding="utf-8")
    (LOG / "README.txt").write_text(
        "GitHub库目录纠正记录\n\n"
        "用户明确要求：删除错误的独立仓库875638477/005lib；正确位置是875638477/001Diy仓库中的005lib目录。\n"
        "正确浏览地址：https://github.com/875638477/001Diy/tree/main/005lib\n"
        "本机D:/001DIY/005lib的9个01目录映射到001Diy/main/005lib下，内部文件路径保持。\n\n"
        "执行范围：以已逐文件核验的本机最新快照为基础，仅补充当前路径说明和本次记录；替换远端005lib完整子树，清理旧文件，保留仓库外层README.md及原有提交历史。\n"
        "基准内容提交：98b94676da011958839790566d18575b5793a85f\n"
        "原始文件树：96dbcfad837bd1cb2f24b6b16f55655d3c1e58ec\n"
        "基准39139个已上传文件，13个Git测试样例目录仍按此前兼容方案无损打包；已核验删除的大备份ZIP不恢复。\n\n"
        "方法：在正确仓库创建一次性辅助分支运行GitHub Actions，从公开的错误仓库读取固定提交，在云端挂接为005lib；临时分支含少量本次说明，main只包含正确目录及原外层文件。无用户令牌写入脚本、日志或仓库，任务使用GitHub短期令牌。\n"
        "发布前将本次文件逐字节计算Git对象与SHA256；云端对完整005lib树SHA、原始快照树、目标父提交及外层条目逐项断言；发布后通过GitHub API再次核对。\n"
        "只有正确位置核验通过后才删除错误独立仓库，并清理临时分支。完成证据在后续verification_result.json及completion记录；本说明不包含其所在提交SHA，避免自引用。\n"
        "历史20261025_github_upload记录保留原始内容，表示当时错误位置的操作证据；当前入口以本任务和GITHUB_LOCATION.txt为准。\n", encoding="utf-8")
    (LOG / "target_inventory.json").write_bytes((WORK / "target_inventory.json").read_bytes())
    (LOG / "prepare_fix_records.py").write_bytes(Path(__file__).read_bytes())
    changes = {**{name: SOURCE / name for name in modified},
               "01AIEDA/GITHUB_LOCATION.txt": SOURCE / "01AIEDA/GITHUB_LOCATION.txt"}
    for file in LOG.rglob("*"):
        require(not file.is_symlink(), "Unexpected link")
        if file.is_file():
            changes[file.relative_to(SOURCE).as_posix()] = file
    payload = []
    blobs = {}
    for name, file in sorted(changes.items()):
        data = file.read_bytes()
        oid = git("hash-object", "-w", "--stdin", data=data).decode().strip()
        require(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == oid, "Blob identity mismatch")
        blobs[name] = oid
        payload.append({"path": name, "source": str(file), "mode": "100644", "blob": oid,
                        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    desired = update_tree(BASE_TREE, blobs)
    count = sum(bool(x) for x in git("ls-tree", "-r", "-z", desired).split(b"\0"))
    source_entries = tree_entries(BASE_TREE)
    new_entries = tree_entries(desired)
    require(set(source_entries) == set(new_entries), "Nine directory set changed")
    require(all(new_entries[name] == entry for name, entry in source_entries.items() if name != "01AIEDA"), "Library directory changed")
    result = {"status": "READY_FOR_CORRECTED_DESTINATION_PUBLICATION", "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
              "source_commit": BASE, "source_tree": BASE_TREE, "expected_library_tree": desired,
              "expected_library_file_count": count, "expected_target_main": inventory["observed_main_commit"],
              "target_prefix": "005lib", "correct_repository": "875638477/001Diy",
              "correct_url": "https://github.com/875638477/001Diy/tree/main/005lib",
              "wrong_repository_to_delete_after_verification": "875638477/005lib",
              "all_eight_non_AI_library_subtrees_unchanged": True, "payload": payload}
    (WORK / "preparation.json").write_bytes(json_bytes(result))
    print(json.dumps({k: v for k, v in result.items() if k != "payload"}, ensure_ascii=True, indent=2))
    print("prepared_payload_files=" + str(len(payload)))


if __name__ == "__main__":
    main()
