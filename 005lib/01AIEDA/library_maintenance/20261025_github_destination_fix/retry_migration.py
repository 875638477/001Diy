"""Preserve the failed attempt, delete its disposable branch, retry fixed fetch."""
from datetime import datetime, timezone
import json
import subprocess
import io
import zipfile

from publish_helper import api, require, WORK, TARGET, BRANCH, GH, ENV


def main():
    helper = json.loads((WORK / "helper_publication.json").read_text(encoding="utf-8"))
    plan = json.loads((WORK / "preparation.json").read_text(encoding="utf-8"))
    require(api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"] == plan["expected_target_main"], "main changed after the failed attempt")
    run = api(f"repos/{TARGET}/actions/runs/40175721448")
    require(run["head_sha"] == helper["commit"] and run["conclusion"] == "failure", "Wrong failed attempt")
    logs = subprocess.run([str(GH), "api", f"repos/{TARGET}/actions/runs/{run['id']}/logs"], env=ENV,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(logs.returncode == 0, "Failed attempt log download failed")
    with zipfile.ZipFile(io.BytesIO(logs.stdout)) as archive:
        require(archive.testzip() is None, "Failed log zip CRC mismatch")
    (WORK / "migration_actions_attempt1_logs.zip").write_bytes(logs.stdout)
    (WORK / "migration_workflow_attempt1.yml").write_bytes((WORK / "migration_workflow.yml").read_bytes())
    (WORK / "helper_publication_attempt1.json").write_bytes((WORK / "helper_publication.json").read_bytes())
    require(api(f"repos/{TARGET}/git/ref/heads/{BRANCH}")["object"]["sha"] == helper["commit"], "Failed helper ref advanced")
    api(f"repos/{TARGET}/git/refs/heads/{BRANCH}", "DELETE")
    (WORK / "helper_publication.json").unlink()
    proof = {"at_utc": datetime.now(timezone.utc).isoformat(), "failed_run": run["html_url"],
             "failed_commit": helper["commit"], "failure": "Partial target fetch omitted README blob required by mktree",
             "main_unchanged": plan["expected_target_main"], "failed_helper_branch_deleted": True,
             "fix": "Fetch complete snapshots in the cloud; no partial-clone filter", "source_snapshot_unchanged": True}
    (WORK / "migration_retry_record.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    main()
