"""Publish only small records and a temporary, narrowly scoped Actions branch.

The actual library data is transferred between public repositories by GitHub's
runner. main is only updated by the guarded runner, never by this publisher.
"""
from datetime import datetime, timezone
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess

WORK = Path(__file__).resolve().parent
GH = WORK.parent / "git_upload_005lib_20261025/tools/gh/bin/gh.exe"
TARGET = "875638477/001Diy"
BRANCH = "codex/library-destination-fix-20261025-0800"
WORKFLOW = ".github/workflows/library-destination-migration.yml"
ENV = os.environ.copy()
ENV["HTTP_PROXY"] = ENV["HTTPS_PROXY"] = "http://127.0.0.1:7890"
ENV["GH_PROMPT_DISABLED"] = "1"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def api(path, method="GET", body=None):
    args = [str(GH), "api", "--method", method, path]
    data = None
    if body is not None:
        args += ["--input", "-"]
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    result = subprocess.run(args, input=data, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(result.returncode == 0, f"GitHub {method} {path}: " + result.stderr.decode("utf-8", "replace")[-2000:])
    return json.loads(result.stdout) if result.stdout.strip() else None


def blob(data):
    expected = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    answer = api(f"repos/{TARGET}/git/blobs", "POST", {"encoding": "base64", "content": base64.b64encode(data).decode("ascii")})
    require(answer["sha"] == expected, "API blob digest mismatch")
    return expected


def main():
    require(not (WORK / "helper_publication.json").exists(), "Helper was already published")
    plan = json.loads((WORK / "preparation.json").read_text(encoding="utf-8"))
    expected = plan["expected_target_main"]
    require(api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"] == expected, "Target main changed")
    runner = (WORK / "runner.py").read_text(encoding="utf-8")
    runner = runner.replace('HELPER_BRANCH = "__HELPER_BRANCH__"', 'HELPER_BRANCH = "' + BRANCH + '"')
    runner = runner.replace('EXPECTED_LIBRARY_TREE = "7829a103fd1e9aaaa7b467d2483c091da2a35411"',
                            'EXPECTED_LIBRARY_TREE = "' + plan["expected_library_tree"] + '"')
    runner = runner.replace('EXPECTED_LIBRARY_FILES = 39145', 'EXPECTED_LIBRARY_FILES = ' + str(plan["expected_library_file_count"]))
    require('EXPECTED_LIBRARY_TREE = "' + plan["expected_library_tree"] + '"' in runner, "Runner tree anchor not updated")
    require('HELPER_BRANCH = "' + BRANCH + '"' in runner, "Runner branch not updated")
    require(plan["strict_every_local_file_required"], "Strict synchronization is required")
    exact = json.loads((WORK / "exact_source_verification.json").read_text(encoding="utf-8"))
    require(exact["status"].startswith("PASS_") and exact["library_tree"] == plan["expected_library_tree"] and exact["excluded_files"] == 0,
            "No strict per-file local verification for this desired tree")
    clean_manifest = {key: plan[key] for key in (
        "source_commit", "source_tree", "expected_library_tree", "expected_library_file_count", "expected_target_main")}
    clean_manifest["payload"] = [{k: value for k, value in item.items() if k != "source"} for item in plan["payload"]]
    entries = []
    uploaded = set()
    for item in plan["payload"]:
        data = Path(item["source"]).read_bytes()
        require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"], "Source record changed")
        if item["blob"] not in uploaded:
            require(blob(data) == item["blob"], "Unexpected payload blob")
            uploaded.add(item["blob"])
        entries.append({"path": ".migration_payload/" + item["path"], "mode": "100644", "type": "blob", "sha": item["blob"]})
    manifest = (json.dumps(clean_manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    entries.append({"path": ".migration_payload/manifest.json", "mode": "100644", "type": "blob", "sha": blob(manifest)})
    workflow = (
        "name: Correct library destination\n"
        "on:\n  push:\n    branches:\n      - '" + BRANCH + "'\n"
        "permissions:\n  contents: write\n"
        "concurrency:\n  group: library-destination-fix-20261025\n  cancel-in-progress: false\n"
        "jobs:\n  migrate:\n    runs-on: ubuntu-latest\n    timeout-minutes: 30\n"
        "    if: github.repository == '875638477/001Diy'\n"
        "    steps:\n      - name: Transfer and verify the fixed library snapshot\n"
        "        env:\n          GH_TOKEN: ${{ github.token }}\n"
        "        shell: bash\n        run: |\n          python3 - <<'PY'\n"
        + "".join("          " + line + "\n" for line in runner.splitlines())
        + "          PY\n")
    (WORK / "migration_workflow.yml").write_text(workflow, encoding="utf-8")
    (WORK / "payload_manifest.json").write_bytes(manifest)
    entries.append({"path": WORKFLOW, "mode": "100644", "type": "blob", "sha": blob(workflow.encode("utf-8"))})
    tree = api(f"repos/{TARGET}/git/trees", "POST", {"tree": entries})["sha"]
    helper = api(f"repos/{TARGET}/git/commits", "POST", {
        "message": "Prepare temporary library destination migration runner",
        "tree": tree, "parents": [expected]})["sha"]
    # A push update on an existing temporary branch triggers the branch workflow.
    api(f"repos/{TARGET}/git/refs", "POST", {"ref": "refs/heads/" + BRANCH, "sha": expected})
    answer = api(f"repos/{TARGET}/git/refs/heads/{BRANCH}", "PATCH", {"sha": helper, "force": False})
    require(answer["object"]["sha"] == helper, "Temporary ref update mismatch")
    require(api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"] == expected, "main unexpectedly changed before job")
    result = {"status": "TEMPORARY_HELPER_PUSHED", "at_utc": datetime.now(timezone.utc).isoformat(),
              "repository": TARGET, "branch": BRANCH, "commit": helper, "tree": tree,
              "main_before": expected, "payload_files": len(plan["payload"]),
              "expected_library_tree": plan["expected_library_tree"]}
    (WORK / "helper_publication.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
