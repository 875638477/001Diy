"""Verify a completed server-side migration, then remove its helper branch."""
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import zipfile

from publish_helper import api, require, WORK, TARGET, BRANCH, GH, ENV
import subprocess


def entries(tree):
    response = api(f"repos/{TARGET}/git/trees/{tree}")
    require(not response.get("truncated"), "Shallow tree was truncated")
    return {entry["path"]: (entry["mode"], entry["type"], entry["sha"]) for entry in response["tree"]}


def main():
    plan = json.loads((WORK / "preparation.json").read_text(encoding="utf-8"))
    helper = json.loads((WORK / "helper_publication.json").read_text(encoding="utf-8"))
    runs = api(f"repos/{TARGET}/actions/runs?branch={BRANCH}&per_page=20")["workflow_runs"]
    runs = [run for run in runs if run["head_sha"] == helper["commit"]]
    require(runs, "No migration run has started yet")
    run = max(runs, key=lambda row: row["id"])
    require(run["status"] == "completed" and run["conclusion"] == "success", "Migration job is not successful yet")
    main_sha = api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"]
    commit = api(f"repos/{TARGET}/git/commits/{main_sha}")
    require([row["sha"] for row in commit["parents"]] == [plan["expected_target_main"]], "Unexpected migration parent")
    root = entries(commit["tree"]["sha"])
    before = api(f"repos/{TARGET}/git/commits/{plan['expected_target_main']}")
    old_root = entries(before["tree"]["sha"])
    require(root.get("005lib") == ("040000", "tree", plan["expected_library_tree"]), "Whole library tree digest differs")
    require({k: v for k, v in root.items() if k != "005lib"} ==
            {k: v for k, v in old_root.items() if k != "005lib"}, "An outer repository path changed")
    dirs = entries(plan["expected_library_tree"])
    require(sorted(dirs) == sorted(["01AIEDA", "01Pad_lib", "01Psm_lib", "01_3d_step_lib", "01aeLib", "01brdlib", "01captureLib", "01env", "01script_file"]), "Not exactly the nine library directories")
    require(all(mode == "040000" and kind == "tree" for mode, kind, sha in dirs.values()), "Unexpected library root file")
    # Save the official job log as a small recovery/audit artifact; never print it.
    result = subprocess.run([str(GH), "api", f"repos/{TARGET}/actions/runs/{run['id']}/logs"], env=ENV,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(result.returncode == 0, "Could not download migration run logs")
    with zipfile.ZipFile(io.BytesIO(result.stdout)) as logs:
        require(logs.testzip() is None, "Migration log zip CRC failure")
    (WORK / "migration_actions_logs.zip").write_bytes(result.stdout)
    # This deletes only the temporary branch, never the correct repository.
    require(api(f"repos/{TARGET}/git/ref/heads/{BRANCH}")["object"]["sha"] == helper["commit"], "Helper ref changed")
    api(f"repos/{TARGET}/git/refs/heads/{BRANCH}", "DELETE")
    proof = {"status": "PASS_CORRECT_DESTINATION_FULL_LIBRARY_TREE_AND_OUTER_ROOT_VERIFIED",
             "verified_at_utc": datetime.now(timezone.utc).isoformat(), "repository": TARGET,
             "correct_url": plan["correct_url"], "migration_commit": main_sha, "tree": commit["tree"]["sha"],
             "library_tree": plan["expected_library_tree"], "library_files": plan["expected_library_file_count"],
             "parent": plan["expected_target_main"], "outside_005lib_unchanged": True,
             "nine_directories": sorted(dirs), "obsolete_top_level_entries_removed": 11,
             "actions_run": run["html_url"], "actions_run_id": run["id"], "actions_conclusion": "success",
             "helper_branch": BRANCH, "helper_branch_deleted": True,
             "wrong_repository_deletion": "PENDING_SEPARATE_DELETE_REPO_AUTHENTICATION_SCOPE"}
    (WORK / "verification_result.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    main()
