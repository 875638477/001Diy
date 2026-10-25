"""Compare every current local 01 file to an immutable Git library tree.

Outputs only to workspace. No exclusions, no implicit archives, no source writes.
The complete path set, file count, byte count and Git content digest must match.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

from prepare_fix_records import git, require, WORK, SOURCE


def files():
    found = {}
    roots = sorted(p for p in SOURCE.iterdir() if p.is_dir() and p.name.startswith("01"))
    require(len(roots) == 9, "Source does not have nine 01 directories")
    for root in roots:
        for folder, dirs, names in os.walk(root, followlinks=False):
            for name in dirs + names:
                path = Path(folder) / name
                s = path.lstat()
                require(not stat.S_ISLNK(s.st_mode) and not getattr(s, "st_file_attributes", 0) & 0x400,
                        "Unexpected reparse point: " + str(path))
            for name in names:
                path = Path(folder) / name
                require(path.is_file(), "Nonregular file")
                relative = path.relative_to(SOURCE).as_posix()
                require(relative not in found, "Repeated source filename")
                found[relative] = path
    require(len({p.casefold() for p in found}) == len(found), "Case-colliding local filenames")
    return found


def hash_file(item):
    relative, path = item
    before = path.stat()
    oid = hashlib.sha1(b"blob " + str(before.st_size).encode() + b"\0")
    sha256 = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            oid.update(chunk)
            sha256.update(chunk)
    after = path.stat()
    require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), "File changed during hash: " + relative)
    return relative, {"bytes": before.st_size, "blob": oid.hexdigest(), "sha256": sha256.hexdigest()}


def main():
    tree = sys.argv[1]
    expected = {}
    for row in git("ls-tree", "-r", "-z", tree).split(b"\0"):
        if row:
            attrs, path = row.split(b"\t", 1)
            mode, kind, oid = attrs.split()
            require(mode == b"100644" and kind == b"blob", "Nonregular committed entry")
            expected[path.decode("utf-8")] = {"blob": oid.decode("ascii")}
    current = files()
    missing = sorted(set(current) - set(expected))
    extra = sorted(set(expected) - set(current))
    if missing or extra:
        result = {"status": "PATH_DIFFERENCES", "local_files": len(current), "tree_files": len(expected),
                  "local_only": missing, "remote_only": extra}
        (WORK / "source_path_differences.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in result.items() if not isinstance(v, list)}))
        raise RuntimeError("Local and tree filenames differ; see source_path_differences.json")
    hashes = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for count, (name, info) in enumerate(pool.map(hash_file, sorted(current.items())), 1):
            # Git blob hashes bind the byte count in their header as well as all bytes.
            require(info["blob"] == expected[name]["blob"], "Content or byte-count mismatch: " + name)
            hashes[name] = info
            if count % 5000 == 0:
                print("verified_files=" + str(count), flush=True)
    require(set(files()) == set(current), "Local filename set changed during verification")
    result = {"status": "PASS_EVERY_LOCAL_FILENAME_COUNT_SIZE_AND_CONTENT_MATCHES", "at_utc": datetime.now(timezone.utc).isoformat(),
              "library_tree": tree, "files": len(hashes), "bytes": sum(row["bytes"] for row in hashes.values()),
              "excluded_files": 0, "all_source_relative_paths_identical": True, "all_file_sizes_and_git_content_hashes_identical": True,
              "per_root_files": {root: sum(name.split("/", 1)[0] == root for name in hashes) for root in sorted({name.split("/", 1)[0] for name in hashes})}}
    (WORK / "exact_source_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (WORK / "exact_source_file_hashes.json").write_text(json.dumps(hashes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2), flush=True)


if __name__ == "__main__":
    main()
