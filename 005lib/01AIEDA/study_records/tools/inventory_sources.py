"""Read local study file metadata and save a timestamped inventory.

Run from any directory. Does not extract archives or execute study materials.
"""

from datetime import datetime, timezone, timedelta
from pathlib import Path
import json

SOURCE = Path(r"D:\005study")
RECORDS = Path(__file__).resolve().parents[1]
TZ = timezone(timedelta(hours=8))


def main():
    files = []
    for path in sorted(SOURCE.rglob("*"), key=lambda p: str(p).casefold()):
        if not path.is_file():
            continue
        stat = path.stat()
        files.append({
            "relative_path": str(path.relative_to(SOURCE)),
            "path": str(path),
            "size_bytes": stat.st_size,
            "modified_time": datetime.fromtimestamp(stat.st_mtime, TZ).isoformat(),
            "mtime_ns": stat.st_mtime_ns,
        })
    result = {
        "captured_at": datetime.now(TZ).isoformat(),
        "timezone": "Asia/Shanghai",
        "source_root": str(SOURCE),
        "scope": "文件路径、大小和修改时间快照；不代表阅读、下载完成或内容完整性验证",
        "file_count": len(files),
        "total_size_bytes": sum(f["size_bytes"] for f in files),
        "files": files,
    }
    evidence = RECORDS / "evidence"
    evidence.mkdir(exist_ok=True)
    target = evidence / "source_manifest.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(target), "captured_at": result["captured_at"],
                      "file_count": len(files)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
