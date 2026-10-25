"""Validate JSON encoding and every absolute filesystem path in the saved snapshot.

This does not rescan lesson contents, replace the snapshot time, or regenerate frames.
"""
from pathlib import Path
import json
import re
from datetime import datetime, timezone, timedelta

root = Path(r"D:\001DIY\005lib\01AIEDA\study_records\evidence")
input_path = root / "video_inventory.json"
raw = input_path.read_bytes()
data = json.loads(raw.decode("utf-8", errors="strict"))
strings_checked = 0
replacement_character_locations = []
paths_checked = []


def visit(value, location="root"):
    global strings_checked
    if isinstance(value, str):
        strings_checked += 1
        if "\ufffd" in value:
            replacement_character_locations.append(location)
        if re.match(r"^[A-Za-z]:[\\/]", value):
            paths_checked.append({"location": location, "path": value,
                                  "exists": Path(value).exists()})
    elif isinstance(value, dict):
        for key, child in value.items():
            visit(key, location + ".<key>")
            visit(child, location + "." + key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            visit(child, location + "[" + str(index) + "]")


visit(data)
missing = [item for item in paths_checked if not item["exists"]]
result = {
    "validated_at_local": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
    "snapshot_started_at_local": data["snapshot_started_at_local"],
    "snapshot_finished_at_local": data["snapshot_finished_at_local"],
    "snapshot_timestamp_preserved": True,
    "frame_files_not_regenerated": True,
    "strict_utf8_decode_succeeded": True,
    "raw_bytes_ascii_only": raw.isascii(),
    "utf8_replacement_character_byte_sequences": raw.count(b"\xef\xbf\xbd"),
    "strings_and_keys_checked": strings_checked,
    "replacement_character_locations": replacement_character_locations,
    "absolute_path_occurrences_checked": len(paths_checked),
    "distinct_absolute_paths_checked": len({item["path"] for item in paths_checked}),
    "missing_paths": missing,
    "all_paths_exist": not missing,
    "all_paths": paths_checked,
}
output_path = root / "video_inventory_validation.json"
output_path.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")
summary = {key: value for key, value in result.items() if key != "all_paths"}
print(json.dumps(summary, ensure_ascii=True, indent=2))
if replacement_character_locations or missing:
    raise SystemExit(1)
