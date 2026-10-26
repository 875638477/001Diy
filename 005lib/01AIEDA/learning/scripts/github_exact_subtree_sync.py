"""Exact byte mirror of explicit local directories into one Git subtree.

Run snapshot/prepare first, inspect its plan, then publish. No local source is
modified. All task data is written under --work. Fetch a shallow blob:none bare
repository into --repository before prepare. Never force updates or rewrite
entries outside --prefix. Credentials remain in the existing gh credential helper.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import time


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def oid(raw, kind="blob"):
    return hashlib.sha1(f"{kind} {len(raw)}\0".encode() + raw).hexdigest()


def write_json(path, value):
    require(not path.exists(), f"Refusing to overwrite evidence: {path.name}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now():
    return datetime.now(timezone.utc).isoformat()


def file_info(path, root):
    before = path.stat(follow_symlinks=False)
    require(stat.S_ISREG(before.st_mode) and not (getattr(before, "st_file_attributes", 0) & 1024), "Not an ordinary file")
    require(before.st_size < 100 * 1024 * 1024, f"GitHub blob limit requires review: {path}")
    h256 = hashlib.sha256()
    h1 = hashlib.sha1(f"blob {before.st_size}\0".encode())
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h256.update(block)
            h1.update(block)
            size += len(block)
    after = path.stat(follow_symlinks=False)
    require(size == before.st_size == after.st_size and before.st_mtime_ns == after.st_mtime_ns, f"File changed during hashing: {path}")
    return {"path": path.relative_to(root).as_posix(), "bytes": size, "sha256": h256.hexdigest(),
            "blob": h1.hexdigest(), "mtime_ns": after.st_mtime_ns, "mode": "100644"}


class Mirror:
    def __init__(self, a):
        self.a = a
        self.source = Path(a.source).resolve(strict=True)
        self.work = Path(a.work).resolve(strict=True)
        self.repo = Path(a.repository).resolve(strict=True)
        self.git_executable = str(Path(a.git).resolve(strict=True))
        self.dirs = a.directories.split(",")
        require(len(self.dirs) == len(set(x.casefold() for x in self.dirs)), "Duplicate roots")
        for name in self.dirs:
            require(name and "/" not in name and "\\" not in name and name not in (".", "..") and name.casefold() != ".git", "Invalid selected root")
        require(a.prefix and a.prefix not in (".", "..") and "/" not in a.prefix and "\\" not in a.prefix and a.prefix.casefold() != ".git" and not any(ord(c) < 32 for c in a.prefix), "Prefix must be one root directory")
        require(not self.work.is_relative_to(self.source) and not self.repo.is_relative_to(self.source), "Task outputs must be outside the source snapshot")
        self.env = os.environ.copy()
        for key in list(self.env):
            if key.startswith("GIT_TRACE") or key in ("GIT_CURL_VERBOSE", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
                self.env.pop(key, None)
        self.env.update({"GIT_TERMINAL_PROMPT": "0", "GIT_NO_LAZY_FETCH": "1", "GH_PROMPT_DISABLED": "1"})
        if a.proxy:
            self.env["HTTP_PROXY"] = self.env["HTTPS_PROXY"] = a.proxy

    def cmd(self, *args, network=False):
        command = [self.git_executable, "--git-dir", str(self.repo), "-c", "core.longpaths=true", "-c", "core.autocrlf=false", "-c", "gc.auto=0"]
        if network:
            command += ["-c", "http.version=HTTP/1.1", "-c", "credential.helper="]
            if self.a.proxy:
                command += ["-c", "http.proxy=" + self.a.proxy]
            if self.a.gh:
                helper = Path(self.a.gh).resolve(strict=True).as_posix()
                require("'" not in helper and "\n" not in helper, "Unsafe credential helper path")
                command += ["-c", "credential.helper=!'" + helper + "' auth git-credential"]
        return command + list(args)

    def git(self, *args, raw=None, network=False, timeout=120):
        result = subprocess.run(self.cmd(*args, network=network), input=raw, capture_output=True, env=self.env, timeout=timeout)
        require(result.returncode == 0, f"git {args[0]} failed: " + result.stderr.decode("utf-8", "replace")[-3000:])
        return result.stdout

    def text(self, *args, **kwargs):
        return self.git(*args, **kwargs).decode("utf-8", "strict").strip()

    def inventory(self):
        paths, empty = [], []
        for name in self.dirs:
            root = self.source / name
            require(root.is_dir(), "Selected source root is missing")
            pending = [root]
            while pending:
                directory = pending.pop()
                attrs = directory.stat(follow_symlinks=False)
                require(not directory.is_symlink() and not (getattr(attrs, "st_file_attributes", 0) & 1024), f"Reparse directory requires review: {directory}")
                # DirEntry retains Windows enumeration metadata. Avoid separate
                # Path.stat/is_symlink calls for tens of thousands of entries;
                # file_info still checks live metadata before/after reading.
                with os.scandir(directory) as iterator:
                    entries = sorted(iterator, key=lambda entry: entry.name.casefold())
                if not entries:
                    empty.append(directory.relative_to(self.source).as_posix())
                for entry in entries:
                    path = directory / entry.name
                    require(path.name.casefold() != ".git" and not any(ord(c) < 32 for c in path.name), f"Unsafe Git path: {path}")
                    attrs = entry.stat(follow_symlinks=False)
                    require(not stat.S_ISLNK(attrs.st_mode) and not (getattr(attrs, "st_file_attributes", 0) & 1024), f"Reparse entry requires review: {path}")
                    if stat.S_ISDIR(attrs.st_mode):
                        pending.append(path)
                    else:
                        require(stat.S_ISREG(attrs.st_mode), "Unsupported source entry")
                        paths.append(path)
        with ThreadPoolExecutor(max_workers=4) as pool:
            rows = list(pool.map(lambda path: file_info(path, self.source), paths))
        rows.sort(key=lambda r: r["path"].encode("utf-8"))
        require(len({r["path"].casefold() for r in rows}) == len(rows), "Case-colliding source paths")
        return rows, sorted(empty)

    def snapshot(self):
        rows, empty = self.inventory()
        value = {"status": "FROZEN_EXACT_LOCAL_BYTES", "created_at": now(), "source": str(self.source),
                 "roots": self.dirs, "repository": self.a.remote, "prefix": self.a.prefix,
                 "files": len(rows), "bytes": sum(r["bytes"] for r in rows), "excluded_files": 0,
                 "empty_directories_git_cannot_store": empty, "rows": rows}
        write_json(self.work / "LOCAL_SNAPSHOT.json", value)
        print(json.dumps({k: v for k, v in value.items() if k != "rows"}, ensure_ascii=False), flush=True)

    def load_snapshot(self):
        p = self.work / "LOCAL_SNAPSHOT.json"
        d = json.loads(p.read_text("utf-8"))
        require(d["source"] == str(self.source) and d["roots"] == self.dirs and d["repository"] == self.a.remote and d["prefix"] == self.a.prefix, "Snapshot configuration differs")
        return d, sha(p.read_bytes())

    def check_source(self, frozen):
        rows, empty = self.inventory()
        clean = lambda r: {k: v for k, v in r.items() if k != "mtime_ns"}
        require([clean(r) for r in rows] == [clean(r) for r in frozen["rows"]], "Local source bytes/path set changed after snapshot")
        require(empty == frozen["empty_directories_git_cannot_store"], "Empty directory set changed")
        return {"status": "PASS_EXACT_LOCAL_REHASH", "files": len(rows), "bytes": sum(r["bytes"] for r in rows), "checked_at": now()}

    def flat_tree(self, ref):
        result = {}
        for entry in self.git("ls-tree", "-r", "-z", ref).split(b"\0"):
            if entry:
                attrs, path = entry.split(b"\t", 1)
                mode, kind, object_id = attrs.decode("ascii").split()
                require(kind == "blob", "Unexpected non-file entry in library subtree")
                result[path.decode("utf-8")] = {"mode": mode, "blob": object_id}
        return result

    def root_tree(self, ref):
        result = {}
        for entry in self.git("ls-tree", "-z", ref).split(b"\0"):
            if entry:
                attrs, name = entry.split(b"\t", 1)
                mode, kind, object_id = attrs.decode("ascii").split()
                result[name] = (mode.lstrip("0"), kind, object_id)
        return result

    def import_blobs(self, rows, remote_oids):
        unique = {}
        for r in rows:
            old = unique.setdefault(r["blob"], r)
            require(old["sha256"] == r["sha256"] and old["bytes"] == r["bytes"], "OID collision/inconsistent snapshot")
        missing = [r for blob, r in unique.items() if blob not in remote_oids]
        stdout = self.work / "fast_import.stdout"
        stderr = self.work / "fast_import.stderr"
        with stdout.open("xb") as output, stderr.open("xb") as errors:
            process = subprocess.Popen(self.cmd("-c", "fastimport.unpackLimit=0", "fast-import", "--done"), env=self.env, stdin=subprocess.PIPE, stdout=output, stderr=errors)
            try:
                for r in missing:
                    raw = (self.source / r["path"]).read_bytes()
                    require(len(raw) == r["bytes"] and sha(raw) == r["sha256"] and oid(raw) == r["blob"], "Source changed while importing")
                    process.stdin.write(f"blob\ndata {len(raw)}\n".encode() + raw + b"\n")
                process.stdin.write(b"done\n")
                process.stdin.close()
                require(process.wait(timeout=300) == 0, "Fast-import failed; inspect task logs")
            except BaseException:
                if process.poll() is None:
                    process.kill()
                    process.wait()
                raise
        return {"unique_local_blobs": len(unique), "new_unique_blobs": len(missing), "new_blob_bytes": sum(r["bytes"] for r in missing)}

    def store_trees(self, rows, before):
        tree = {}
        for r in rows:
            node = tree
            parts = r["path"].split("/")
            for part in parts[:-1]:
                node = node.setdefault(part.encode("utf-8"), {})
            require(parts[-1].encode("utf-8") not in node, "Duplicate file/tree name")
            node[parts[-1].encode("utf-8")] = (r["mode"], "blob", r["blob"])
        objects = {}

        def raw_entries(entries):
            ordered = sorted(entries.items(), key=lambda item: item[0] + (b"/" if item[1][1] == "tree" else b""))
            return b"".join(v[0].encode("ascii") + b" " + name + b"\0" + bytes.fromhex(v[2]) for name, v in ordered)

        def materialize(node):
            entries = {name: ("40000", "tree", materialize(value)) if isinstance(value, dict) else value for name, value in node.items()}
            raw = raw_entries(entries)
            object_id = oid(raw, "tree")
            objects[object_id] = raw
            return object_id

        library_tree = materialize(tree)
        after = dict(before)
        after[self.a.prefix.encode("utf-8")] = ("40000", "tree", library_tree)
        root_raw = raw_entries(after)
        root_oid = oid(root_raw, "tree")
        objects[root_oid] = root_raw
        temporary = self.work / "tree_objects"
        temporary.mkdir()
        files = []
        for object_id, raw in objects.items():
            path = temporary / object_id
            path.write_bytes(raw)
            files.append(path)
        output = self.git("hash-object", "-w", "-t", "tree", "--no-filters", "--stdin-paths", raw=("\n".join(str(p) for p in files) + "\n").encode("utf-8"))
        require(output.decode("ascii").splitlines() == [p.name for p in files], "Git tree object hashes differ")
        return library_tree, root_oid, after

    def prepare(self):
        frozen, snapshot_sha = self.load_snapshot()
        source_check = self.check_source(frozen)
        base = self.text("rev-parse", "refs/remotes/origin/main")
        before = self.root_tree(base)
        require(self.a.prefix.encode() in before and before[self.a.prefix.encode()][1] == "tree", "Expected remote library subtree is missing")
        old = self.flat_tree(base + ":" + self.a.prefix)
        expected = {r["path"]: {"mode": r["mode"], "blob": r["blob"]} for r in frozen["rows"]}
        added = sorted(set(expected) - set(old))
        deleted = sorted(set(old) - set(expected))
        changed = sorted(p for p in set(expected) & set(old) if expected[p] != old[p])
        imports = self.import_blobs(frozen["rows"], {r["blob"] for r in old.values()})
        library, root, after = self.store_trees(frozen["rows"], before)
        require(self.flat_tree(library) == expected, "Prepared tree does not match exact local snapshot")
        require(self.root_tree(root) == after and {k: v for k, v in after.items() if k != self.a.prefix.encode()} == {k: v for k, v in before.items() if k != self.a.prefix.encode()}, "Directory-external entries changed")
        env = self.env.copy()
        env.update({"GIT_AUTHOR_NAME": self.a.author, "GIT_COMMITTER_NAME": self.a.author,
                    "GIT_AUTHOR_EMAIL": self.a.email, "GIT_COMMITTER_EMAIL": self.a.email})
        result = subprocess.run(self.cmd("commit-tree", root, "-p", base), input=(self.a.message + "\n").encode("utf-8"), env=env, capture_output=True, timeout=30)
        require(result.returncode == 0, "Unable to create descendant commit")
        commit = result.stdout.decode("ascii").strip()
        self.git("update-ref", "refs/heads/prepared-library-sync", commit)
        require(self.text("rev-list", "--parents", "-n", "1", commit).split() == [commit, base], "Prepared commit parent differs")
        plan = {"status": "PASS_EXACT_SUBTREE_DESCENDANT_COMMIT_READY", "created_at": now(), "repository": self.a.remote,
                "prefix": self.a.prefix, "base": base, "commit": commit, "library_tree": library, "root_tree": root,
                "snapshot_sha256": snapshot_sha, "files": len(expected), "bytes": frozen["bytes"],
                "other_root_entries_unchanged": True, "outside_entries": [{"name": k.decode("utf-8"), "mode": v[0], "type": v[1], "sha": v[2]} for k, v in before.items() if k != self.a.prefix.encode()],
                "added": added, "changed": changed, "deleted": deleted, "counts": {"added": len(added), "changed": len(changed), "deleted": len(deleted), "unchanged": len(expected) - len(added) - len(changed)},
                "source_check": source_check, "imports": imports}
        write_json(self.work / "SYNC_PLAN.json", plan)
        print(json.dumps({k: v for k, v in plan.items() if k not in ("added", "changed", "deleted", "outside_entries")}, ensure_ascii=False), flush=True)

    def publish(self):
        frozen, digest = self.load_snapshot()
        plan_raw = (self.work / "SYNC_PLAN.json").read_bytes()
        plan = json.loads(plan_raw)
        require(digest == plan["snapshot_sha256"] and plan["repository"] == self.a.remote and plan["prefix"] == self.a.prefix, "Plan/snapshot configuration differs")
        require(plan["status"] == "PASS_EXACT_SUBTREE_DESCENDANT_COMMIT_READY", "Plan is not ready")
        require(self.text("rev-list", "--parents", "-n", "1", plan["commit"]).split() == [plan["commit"], plan["base"]], "Commit parent no longer matches the plan")
        require(self.text("rev-parse", plan["commit"] + "^{tree}") == plan["root_tree"], "Commit root differs from the plan")
        before = self.root_tree(plan["base"])
        after = self.root_tree(plan["commit"])
        prefix = self.a.prefix.encode("utf-8")
        require({k: v for k, v in before.items() if k != prefix} == {k: v for k, v in after.items() if k != prefix}, "Commit changes entries outside the mirror prefix")
        require(after[prefix] == ("40000", "tree", plan["library_tree"]), "Committed library subtree differs")
        expected = {r["path"]: {"mode": r["mode"], "blob": r["blob"]} for r in frozen["rows"]}
        require(self.flat_tree(plan["commit"] + ":" + self.a.prefix) == expected, "Committed file set does not equal the local snapshot")
        source_check = self.check_source(frozen)
        url = "https://github.com/" + self.a.remote + ".git"
        current = self.text("ls-remote", "--exit-code", url, "refs/heads/main", network=True).split()[0]
        require(current == plan["base"], "Remote advanced; prepare a new reviewed descendant without forcing")
        output = self.git("push", "--porcelain", url, plan["commit"] + ":refs/heads/main", network=True, timeout=600)
        readback = self.text("ls-remote", "--exit-code", url, "refs/heads/main", network=True).split()[0]
        require(readback == plan["commit"], "Remote main readback differs; reconcile before further changes")
        receipt = {"status": "PUSH_COMPLETED_REMOTE_REF_VERIFIED", "at": now(), "repository": self.a.remote,
                   "commit": plan["commit"], "parent": plan["base"], "library_tree": plan["library_tree"],
                   "root_tree": plan["root_tree"], "plan_sha256": sha(plan_raw), "source_check": source_check,
                   "stdout": output.decode("utf-8", "replace"), "force": False}
        write_json(self.work / "PUSH_RECEIPT.json", receipt)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)

    def verify(self):
        frozen, digest = self.load_snapshot()
        plan = json.loads((self.work / "SYNC_PLAN.json").read_text("utf-8"))
        require(digest == plan["snapshot_sha256"], "Frozen snapshot changed")
        require(Path(self.a.gh).is_file(), "gh is required for independent server API readback")

        def api(endpoint):
            result = subprocess.run([self.a.gh, "api", endpoint], env=self.env, capture_output=True, timeout=90)
            require(result.returncode == 0, "GitHub verification API failed")
            return json.loads(result.stdout)

        ref = api(f"repos/{self.a.remote}/git/ref/heads/main")
        require(ref["object"]["sha"] == plan["commit"], "Remote HEAD changed since publication")
        commit = api(f"repos/{self.a.remote}/git/commits/{plan['commit']}")
        require(commit["tree"]["sha"] == plan["root_tree"] and [r["sha"] for r in commit["parents"]] == [plan["base"]], "Server commit ancestry/tree differs")
        root = api(f"repos/{self.a.remote}/git/trees/{plan['root_tree']}")
        outside = [{"name": r["path"], "mode": r["mode"].lstrip("0"), "type": r["type"], "sha": r["sha"]} for r in root["tree"] if r["path"] != self.a.prefix]
        require(sorted(outside, key=lambda r: r["name"]) == sorted(plan["outside_entries"], key=lambda r: r["name"]), "Remote outside subtree entries changed")
        require(next(r for r in root["tree"] if r["path"] == self.a.prefix)["sha"] == plan["library_tree"], "Remote library tree differs")
        api_reads, cache, visiting = [], {}, set()

        def read_tree(object_id, recursive=True):
            suffix = "?recursive=1" if recursive else ""
            answer = api(f"repos/{self.a.remote}/git/trees/{object_id}{suffix}")
            require(answer["sha"] == object_id, "Server returned an unexpected tree object")
            api_reads.append({"tree": object_id, "recursive": recursive, "truncated": bool(answer.get("truncated")),
                              "entries": len(answer["tree"]), "response_sha256": sha(json.dumps(answer, sort_keys=True).encode("utf-8"))})
            return answer

        def complete_tree(object_id):
            if object_id in cache:
                return cache[object_id]
            require(object_id not in visiting, "Cycle in server trees")
            visiting.add(object_id)
            answer = read_tree(object_id)
            require(all(r["type"] in ("tree", "blob") for r in answer["tree"]), "Remote has an unexpected gitlink")
            if not answer.get("truncated"):
                result = {r["path"]: {"mode": r["mode"], "blob": r["sha"], "bytes": r["size"]} for r in answer["tree"] if r["type"] == "blob"}
                require(len(result) == sum(r["type"] == "blob" for r in answer["tree"]), "Duplicate remote file path")
            else:
                # GitHub caps recursive responses by both entry count and bytes.
                # Discard the partial answer and partition along actual subtrees.
                direct = read_tree(object_id, recursive=False)
                require(not direct.get("truncated"), "Nonrecursive remote tree was truncated")
                result = {}
                for r in direct["tree"]:
                    require(r["path"] and "/" not in r["path"] and r["path"] not in (".", ".."), "Invalid direct tree path")
                    if r["type"] == "blob":
                        additions = {r["path"]: {"mode": r["mode"], "blob": r["sha"], "bytes": r["size"]}}
                    else:
                        require(r["type"] == "tree", "Remote has an unexpected gitlink")
                        additions = {r["path"] + "/" + path: value for path, value in complete_tree(r["sha"]).items()}
                    require(not (set(result) & set(additions)), "Duplicate remote path after partitioning")
                    result.update(additions)
            visiting.remove(object_id)
            cache[object_id] = result
            return result

        remote = complete_tree(plan["library_tree"])
        expected = {r["path"]: {"mode": r["mode"], "blob": r["blob"], "bytes": r["bytes"]} for r in frozen["rows"]}
        require(remote == expected, "Remote file set/blob hashes/bytes differ from local snapshot")
        local = self.check_source(frozen)
        write_json(self.work / "REMOTE_SERVER_TREE.json", {"sha": plan["library_tree"], "status": "COMPLETE_SERVER_FILE_MAP",
                   "method": "recursive_with_nonrecursive_partition_on_truncation", "api_reads": api_reads, "files": remote})
        receipt = {"status": "PASS_REMOTE_EXACT_BYTES_AND_DELETIONS_LOCAL_REHASH", "at": now(), "repository": self.a.remote,
                   "url": f"https://github.com/{self.a.remote}/tree/main/{self.a.prefix}", "commit": plan["commit"], "parent": plan["base"],
                   "library_tree": plan["library_tree"], "root_tree": plan["root_tree"], "files": len(remote), "bytes": frozen["bytes"],
                   "excluded_local_files": 0, "outside_subtree_unchanged": True, "original_history_preserved": True,
                   "differences_applied": plan["counts"], "every_remote_path_mode_blob_size_matches": True,
                   "server_tree_complete": True, "truncated_responses_partitioned": sum(r["truncated"] for r in api_reads),
                   "server_tree_api_reads": len(api_reads), "local_rehash": local, "snapshot_sha256": digest}
        write_json(self.work / "REMOTE_EXACT_VERIFICATION.json", receipt)
        print(json.dumps(receipt, ensure_ascii=False), flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("snapshot", "prepare", "publish", "verify"))
    for name in ("source", "work", "repository", "git", "remote", "prefix", "directories"):
        p.add_argument("--" + name, required=True)
    p.add_argument("--gh")
    p.add_argument("--proxy", default="")
    p.add_argument("--author", default="Library maintenance")
    p.add_argument("--email", default="library-maintenance@users.noreply.github.com")
    p.add_argument("--message", default="Synchronize local library subtree and remove obsolete remote files")
    a = p.parse_args()
    getattr(Mirror(a), a.action)()


if __name__ == "__main__":
    main()
