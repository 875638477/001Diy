from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from datetime import datetime, timezone
import zipfile


TASK = Path(r"D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_github_upload")
MAINT = Path(r"D:\001DIY\005lib\01AIEDA\library_maintenance")
OLD = MAINT / "20261025_pad_psm_merge"
ARCHIVE = OLD / "cadence_library_maintenance_20261025_full.zip"
EXPECTED_ARCHIVE_SHA = "d544cd9d1c1facffd630b03cc915487bf2c5912165e441271be19ef48272d5eb"
EXPECTED_MANIFEST_SHA = "ad5280f53fb2dbdc58efd77e74632e4baad27dd27fcde87e7fb838ff53864710"
EXPECTED_JSON_MANIFEST_SHA = "bc5429cf7e5f4b4eccaa1f9e82fe0abe10ab5dc60487a61e3d4a89f7e96d7879"
EXPECTED_SIZE = 375805598
EXPECTED_COUNT = 26476
EXPECTED_SOURCE_BYTES = 1955833097
ROOTS = (
    Path(r"D:\001DIY\004computer\lga1700\cadence_library_cleanup_20261025"),
    Path(r"D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025"),
    Path(r"D:\001DIY\005lib\_library_suffix_backup_20261025"),
    Path(r"D:\001DIY\005lib\_library_merge_backup_20261025"),
    Path(r"D:\001DIY\005lib\_library_geometry_backup_20261025"),
)


def sha256(p: Path) -> str:
    with p.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_row(row: dict[str, str]) -> tuple[dict[str, object], str | None]:
    p = Path(row["source"])
    real = p.resolve(strict=True)
    matching = [r for r in ROOTS if real.is_relative_to(r.resolve(strict=True))]
    if len(matching) != 1:
        raise ValueError(f"source outside the five authorized original roots: {p}")
    before = p.stat()
    actual = sha256(p)
    after = p.stat()
    issue = None
    if not p.is_file() or before.st_size != int(row["bytes"]) or actual != row["sha256"]:
        issue = "source_missing_or_size_sha256_mismatch"
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        issue = "source_changed_while_reading"
    return {
        "source": str(p),
        "root": str(matching[0]),
        "bytes": before.st_size,
        "sha256": actual,
        "status": "PASS" if issue is None else "FAIL",
        "issue": issue or "",
    }, issue


def replace_once_bytes(path: Path, old: str, new: str) -> tuple[bytes, bytes]:
    before = path.read_bytes()
    a, b = old.encode("utf-8"), new.encode("utf-8")
    if before.count(a) != 1:
        raise ValueError(f"expected exactly one byte-level replacement in {path}: {old}")
    return before, before.replace(a, b, 1)


def plan_docs() -> dict[Path, tuple[bytes, bytes]]:
    p = OLD / "README.txt"
    before = p.read_bytes()
    after = before
    replacements = (
        (
            "完整原始记录与恢复原件：cadence_library_maintenance_20261025_full.zip。",
            "汇总备份ZIP：cadence_library_maintenance_20261025_full.zip 已按用户2026-10-25指示删除。删除前逐项核验26476个原始文件的大小与SHA256全部一致；直接可读记录、两轮完整原始记录树及下面三套原始恢复目录继续保留。",
        ),
        (
            "归档共26476个原始文件、1955833097字节；ZIP中的5个目录分别保留两轮完整记录树和三套恢复备份。",
            "删除前ZIP收录26476个原始文件、1955833097字节，来自两轮完整记录树和三套恢复备份；ZIP为这些原件的重复汇总副本，不是Cadence库依赖。",
        ),
        (
            "ZIP及逐条原始文件的验证结果见 archive_verification.json；不是只检查压缩文件是否能打开。",
            "archive_manifest.csv/json、archive_verification.json、publication_verification.json是删除前归档的历史清单与验证证据；不表示ZIP目前仍存在。此次重新核验原件及删除结果见 ../20261025_github_upload/backup_zip_removal.json。",
        ),
        (
            "ZIP中backups/同时包含上述恢复原件及脚本的逐文件副本。",
            "上述三套恢复原件及脚本未删除；此前ZIP中backups/的重复副本随ZIP一并删除。两轮完整记录树仍位于 D:\\001DIY\\004computer\\lga1700\\cadence_library_cleanup_20261025 与 D:\\001DIY\\004computer\\lga1700\\cadence_geometry_merge_20261025。",
        ),
    )
    for old, new in replacements:
        a, b = old.encode("utf-8"), new.encode("utf-8")
        if after.count(a) != 1:
            raise ValueError(f"README replacement count differs: {old}")
        after = after.replace(a, b, 1)
    result = {p: (before, after)}

    p = OLD / "STATUS.txt"
    before = p.read_bytes()
    before.decode("utf-8")
    eol = b"\r\n" if b"\r\n" in before else b"\n"
    after = eol.join(
        s.encode("utf-8") for s in (
            "PASS_ORIGINALS_REVERIFIED_BACKUP_ZIP_REMOVED_BY_USER_REQUEST",
            "2026-10-25：汇总备份ZIP已删除；26476个原件的大小和SHA256重新核验全部通过。",
            "直接可读记录、两轮原始记录树和三套原始恢复目录仍在；历史归档清单与验证文件保留为删除前证据。",
            "详见 ../20261025_github_upload/backup_zip_removal.json",
            "",
        )
    )
    result[p] = (before, after)

    p = MAINT / "INDEX.txt"
    before = p.read_bytes()
    eol = "\r\n" if b"\r\n" in before else "\n"
    old = "入口：20261025_pad_psm_merge\\README.txt"
    new = old + eol + "说明：汇总备份ZIP已按用户指示删除，直接可读记录及原始恢复目录保留。" + eol + eol + "2026-10-25  GitHub上传准备：核验并删除重复汇总备份ZIP。" + eol + "入口：20261025_github_upload\\README_backup_removal.txt"
    result[p] = replace_once_bytes(p, old, new)

    p = Path(r"D:\001DIY\005lib\01AIEDA\EDA.md")
    old = "数字0402/0603/0805带后缀封装的删除清单、兼容旧名映射、原生验证与恢复备份均在归档中。"
    new = "数字0402/0603/0805带后缀封装的删除清单、兼容旧名映射和原生验证可直接查看。2026-10-25按用户指示删除重复的汇总备份ZIP；删除前26476个原件的大小和SHA256重新核验全部一致，两轮原始记录树及三套原始恢复目录保留，详见[ZIP核验与删除记录](library_maintenance/20261025_github_upload/README_backup_removal.txt)。历史归档清单与验证文件仅代表删除前状态。"
    result[p] = replace_once_bytes(p, old, new)
    return result


def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    # Never compute a deletion target from an input row or a glob.
    exact = Path(r"D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pad_psm_merge\cadence_library_maintenance_20261025_full.zip")
    if ARCHIVE.resolve(strict=True) != exact or ARCHIVE.is_symlink():
        raise ValueError("resolved archive target does not match the single explicitly authorized file")
    if not ARCHIVE.is_file() or ARCHIVE.stat().st_size != EXPECTED_SIZE:
        raise ValueError("archive type/size differs")
    if sha256(ARCHIVE) != EXPECTED_ARCHIVE_SHA:
        raise ValueError("archive SHA256 differs")
    manifest = OLD / "archive_manifest.csv"
    if sha256(manifest) != EXPECTED_MANIFEST_SHA:
        raise ValueError("archive source manifest SHA256 differs")
    if sha256(OLD / "archive_manifest.json") != EXPECTED_JSON_MANIFEST_SHA:
        raise ValueError("historically recorded JSON manifest SHA256 differs")
    with manifest.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != EXPECTED_COUNT or sum(int(r["bytes"]) for r in rows) != EXPECTED_SOURCE_BYTES:
        raise ValueError("source count/byte total differs")
    if len({r["source"].casefold() for r in rows}) != len(rows):
        raise ValueError("source manifest has duplicate paths")
    expected_members = {r["archive_path"]: int(r["bytes"]) for r in rows}
    with zipfile.ZipFile(ARCHIVE) as z:
        infos = z.infolist()
        expected_members["archive_manifest.json"] = (OLD / "archive_manifest.json").stat().st_size
        if len(infos) != len(rows) + 1 or {i.filename: i.file_size for i in infos} != expected_members:
            raise ValueError("ZIP content headers differ from complete source manifest")
        if hashlib.sha256(z.read("archive_manifest.json")).hexdigest() != EXPECTED_JSON_MANIFEST_SHA:
            raise ValueError("ZIP embedded manifest differs from retained original manifest")
        archive_top_roots = sorted({i.filename.split("/")[0] for i in infos if i.filename != "archive_manifest.json"})
        if archive_top_roots != ["backups", "cadence_geometry_merge_20261025", "cadence_library_cleanup_20261025"]:
            raise ValueError("unexpected ZIP content category")
    docs = plan_docs()  # All replacements must be reviewable before deleting the duplicate ZIP.
    TASK.mkdir(parents=True, exist_ok=True)
    verification = []
    failures = []
    print(json.dumps({"phase": "verify_all_originals", "files": len(rows), "bytes": EXPECTED_SOURCE_BYTES}), flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(check_row, row): row for row in rows}
        for done, future in enumerate(as_completed(futures), 1):
            row = futures[future]
            try:
                result, issue = future.result()
                verification.append(result)
                if issue:
                    failures.append(result)
            except Exception as e:
                failures.append({"source": row["source"], "error": type(e).__name__ + ": " + str(e)})
            if done % 2000 == 0 or done == len(rows):
                print(json.dumps({"phase": "verify_all_originals", "completed": done, "failures": len(failures)}), flush=True)
    if failures:
        write_json(TASK / "backup_zip_removal_blocked.json", {"status": "BLOCKED_ORIGINALS_DIFFER", "failures": failures, "archive_untouched": True})
        raise ValueError(f"{len(failures)} original files missing or differ; archive retained")
    counts = Counter(str(v["root"]) for v in verification)
    byte_counts = Counter()
    for v in verification:
        byte_counts[str(v["root"])] += int(v["bytes"])
    if len(verification) != EXPECTED_COUNT or sum(int(v["bytes"]) for v in verification) != EXPECTED_SOURCE_BYTES:
        raise ValueError("verified original aggregate differs")
    before_dir = TASK / "backup_zip_removal_metadata_before"
    before_dir.mkdir(exist_ok=True)
    for p, (before, after) in docs.items():
        if p.read_bytes() != before:
            raise ValueError(f"documentation changed during source verification: {p}")
        (before_dir / p.name).write_bytes(before)
    pre = {
        "status": "PASS_ALL_ORIGINALS_REVERIFIED_READY_TO_REMOVE_DUPLICATE_ZIP",
        "started_utc": started,
        "source_manifest": str(manifest),
        "source_manifest_sha256": EXPECTED_MANIFEST_SHA,
        "original_files_verified": len(verification),
        "original_bytes_verified": EXPECTED_SOURCE_BYTES,
        "verification": "Every source file in the immutable historical manifest was reopened and compared by byte count and SHA256; all match.",
        "source_roots": [{"path": str(r), "files": counts[str(r)], "bytes": byte_counts[str(r)]} for r in ROOTS],
        "archive": str(ARCHIVE),
        "archive_sha256_before_deletion": EXPECTED_ARCHIVE_SHA,
        "archive_bytes_before_deletion": EXPECTED_SIZE,
        "classification": "Duplicate ZIP copy of two full maintenance evidence trees and three rollback backup trees, not a live Cadence library file.",
        "archive_top_roots": archive_top_roots,
        "user_authorization": "User instructed: inspect large files and delete if they are backup files (2026-10-25).",
        "scope": "Only the exact named ZIP is removed. All 26476 originals, all readable records and all three rollback directories are retained.",
    }
    write_json(TASK / "backup_zip_originals_verification.json", pre)
    # Recheck the exact path and size immediately before the one-file deletion.
    if ARCHIVE.resolve(strict=True) != exact or ARCHIVE.is_symlink() or ARCHIVE.stat().st_size != EXPECTED_SIZE:
        raise ValueError("archive target changed after verification")
    ARCHIVE.unlink()
    if ARCHIVE.exists():
        raise ValueError("archive still exists after unlink")
    for p, (before, after) in docs.items():
        p.write_bytes(after)
        if p.read_bytes() != after:
            raise ValueError(f"updated documentation failed readback: {p}")
    after_dir = TASK / "backup_zip_removal_metadata_after"
    after_dir.mkdir(exist_ok=True)
    for p, (before, after) in docs.items():
        (after_dir / p.name).write_bytes(after)
    record = dict(pre)
    record.update({
        "status": "PASS_BACKUP_ZIP_REMOVED_ORIGINALS_RETAINED",
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "archive_exists_after_deletion": ARCHIVE.exists(),
        "deleted_file_count": 1,
        "released_bytes": EXPECTED_SIZE,
        "documentation_updates": [
            {"path": str(p), "before_sha256": hashlib.sha256(before).hexdigest(), "after_sha256": hashlib.sha256(after).hexdigest(), "encoding_preserved": "UTF-8; exact byte replacement or STATUS rewrite preserving original newline"}
            for p, (before, after) in docs.items()
        ],
        "retained_original_root_presence": {str(r): r.is_dir() for r in ROOTS},
        "historical_manifests_and_verifications": "Preserved unchanged as evidence of the pre-deletion archive. README, STATUS, INDEX and EDA explicitly state the ZIP has been deleted.",
    })
    write_json(TASK / "backup_zip_removal.json", record)
    text = (
        "GitHub上传准备：重复汇总备份ZIP核验与删除记录\n"
        "日期：2026-10-25\n\n"
        "用户指示：查看大文件，若为备份则可以删除。\n"
        f"已删除唯一汇总备份ZIP：{ARCHIVE}\n"
        f"删除大小：{EXPECTED_SIZE}字节（约358.4MiB）；文件SHA256：{EXPECTED_ARCHIVE_SHA}\n"
        "该ZIP只是两轮维护记录与三套原始恢复目录的重复汇总包，不是实际PAD/PSM/DRA库依赖。\n"
        "删除前按历史archive_manifest.csv对26476个原始文件共1955833097字节重新读取，大小和SHA256全部一致。\n"
        "原始记录树、三套原始恢复目录、readable内直接可读记录及所有实际公共库均保留。\n"
        "旧archive_manifest和verification文件保留为删除前历史证据；旧README、STATUS、总索引与EDA.md已局部修正，不再声称ZIP仍在。\n\n"
        "本次核验与删除结果：backup_zip_removal.json\n"
        "删除前原件全量验证：backup_zip_originals_verification.json\n"
        "文档修改前后副本：backup_zip_removal_metadata_before/ 与 backup_zip_removal_metadata_after/\n"
        "本次执行脚本：remove_verified_backup_zip.py（历史脚本，不自动执行）\n\n"
        "保留的原件目录：\n" + "\n".join(str(r) for r in ROOTS) + "\n"
    )
    (TASK / "README_backup_removal.txt").write_text(text, encoding="utf-8")
    script = Path(__file__).resolve()
    if script != TASK / script.name:
        shutil.copy2(script, TASK / script.name)
    print(json.dumps({"status": record["status"], "originals": len(verification), "deleted_bytes": EXPECTED_SIZE, "record": str(TASK / "backup_zip_removal.json")}), flush=True)


if __name__ == "__main__":
    main()
