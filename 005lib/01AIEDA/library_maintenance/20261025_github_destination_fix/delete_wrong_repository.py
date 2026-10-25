"""Delete only the explicitly rejected standalone repository after migration."""
from datetime import datetime, timezone
import json
import subprocess

from publish_helper import api, require, WORK, TARGET, GH, ENV

WRONG = "875638477/005lib"


def main():
    verification = json.loads((WORK / "verification_result.json").read_text(encoding="utf-8"))
    require(verification["status"].startswith("PASS_CORRECT_DESTINATION"), "Correct destination has not been verified")
    plan = json.loads((WORK / "preparation.json").read_text(encoding="utf-8"))
    exact = json.loads((WORK / "exact_source_verification.json").read_text(encoding="utf-8"))
    require(exact["status"] == "PASS_EVERY_LOCAL_FILENAME_COUNT_SIZE_AND_CONTENT_MATCHES"
            and exact["excluded_files"] == 0 and exact["library_tree"] == plan["expected_library_tree"]
            and exact["files"] == plan["expected_library_file_count"], "Strict local name/count/content verification did not pass")
    require(verification["library_tree"] == plan["expected_library_tree"], "Published library is not the verified local tree")
    require(TARGET == "875638477/001Diy" and WRONG == "875638477/005lib" and TARGET != WRONG, "Repository guard failed")
    expected_main = verification["migration_commit"]
    require(api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"] == expected_main, "Correct main changed after verification")
    correct = api(f"repos/{TARGET}")
    wrong = api(f"repos/{WRONG}")
    require(correct["full_name"] == TARGET and wrong["full_name"] == WRONG, "Repository identity mismatch")
    require(correct["permissions"]["push"] and wrong["permissions"]["admin"], "Insufficient repository permissions")
    expected_source = plan["source_commit"]
    require(api(f"repos/{WRONG}/git/ref/heads/main")["object"]["sha"] == expected_source, "Wrong repository received unexpected new work")
    # User explicitly requested deletion of this exact standalone repository.
    result = subprocess.run([str(GH), "api", "--include", "--method", "DELETE", f"repos/{WRONG}"],
                            env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(result.returncode == 0, "Delete authentication/action failed: " + result.stderr.decode("utf-8", "replace")[-1500:])
    first_line = result.stdout.splitlines()[0].decode("ascii", "replace")
    require("204" in first_line, "Unexpected delete HTTP status")
    absent = subprocess.run([str(GH), "api", "--include", f"repos/{WRONG}"], env=ENV,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(absent.returncode != 0 and b"404" in absent.stdout.splitlines()[0], "Deleted repository still resolves")
    require(api(f"repos/{TARGET}")["full_name"] == TARGET, "Correct repository is not readable after deletion")
    require(api(f"repos/{TARGET}/git/ref/heads/main")["object"]["sha"] == expected_main, "Correct repository main changed")
    require(api(f"repos/{TARGET}/contents/005lib?ref=main")[0], "Correct library is not readable")
    proof = {"status": "PASS_WRONG_STANDALONE_REPOSITORY_DELETED_CORRECT_REPOSITORY_PRESERVED",
             "at_utc": datetime.now(timezone.utc).isoformat(), "deleted_repository": WRONG,
             "delete_http_status": 204, "authenticated_readback_http_status": 404,
             "preserved_repository": TARGET, "preserved_main": expected_main,
             "migration_verification": verification["status"], "user_authorization": "User explicitly requested deletion of 875638477/005lib and migration to 875638477/001Diy/005lib"}
    (WORK / "repository_deletion_result.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    main()
