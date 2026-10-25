"""Read AVI headers and, if available, use Windows VfW to decode sample frames.

No source files are modified. Durations are header-derived, not a playback audit.
"""
from __future__ import annotations

import ctypes
import json
import pathlib
import re
import struct
from datetime import datetime, timezone, timedelta
from ctypes import wintypes

WORK = pathlib.Path(r"D:\001DIY\005lib\01AIEDA\study_records\evidence")
SOURCE = pathlib.Path(r"D:\005study\72讲速成视频【Cadence Allegro16.6视频教程】完整版")
ALTERNATE_SOURCE = pathlib.Path(r"D:\005study\72讲速成视频【Cadence Allegro16.6视频教程")


def chunks(data, start, end):
    pos = start
    while pos + 8 <= min(end, len(data)):
        tag, size = struct.unpack_from("<4sI", data, pos)
        body = pos + 8
        yield tag, body, size
        pos = body + size + (size & 1)


def inspect_header(path):
    with path.open("rb") as stream:
        data = stream.read(131072)
    if data[:4] != b"RIFF" or data[8:12] != b"AVI ":
        raise ValueError("Not a RIFF AVI file")
    result = {"riff_declared_size": struct.unpack_from("<I", data, 4)[0] + 8}
    for tag, body, size in chunks(data, 12, len(data)):
        if tag != b"LIST" or data[body:body+4] != b"hdrl":
            continue
        streams = []
        for htag, hbody, hsize in chunks(data, body+4, body+size):
            if htag == b"avih":
                fields = struct.unpack_from("<14I", data, hbody)
                result.update(microseconds_per_frame=fields[0], total_frames=fields[4],
                              stream_count=fields[6], width=fields[8], height=fields[9])
            if htag != b"LIST" or data[hbody:hbody+4] != b"strl":
                continue
            entry = {}
            for stag, sbody, ssize in chunks(data, hbody+4, hbody+hsize):
                if stag == b"strh":
                    fields = struct.unpack_from("<4s4sIHHIIIIIIIIhhhh", data, sbody)
                    entry.update(type=fields[0].decode("ascii", "replace"),
                                 handler=fields[1].decode("ascii", "replace"),
                                 scale=fields[6], rate=fields[7], start=fields[8],
                                 length=fields[9])
                if stag == b"strf" and entry.get("type") == "vids":
                    fields = struct.unpack_from("<IiiHH4sI", data, sbody)
                    entry.update(width=fields[1], height=fields[2], bit_count=fields[4],
                                 compression=fields[5].decode("ascii", "replace"))
                if stag == b"strf" and entry.get("type") == "auds":
                    fields = struct.unpack_from("<HHIIHH", data, sbody)
                    entry.update(format_tag=fields[0], channels=fields[1],
                                 samples_per_second=fields[2],
                                 average_bytes_per_second=fields[3],
                                 bits_per_sample=fields[5])
            if entry.get("rate"):
                entry["declared_duration_seconds"] = entry["length"] * entry["scale"] / entry["rate"]
            if entry.get("type") == "vids" and entry.get("scale"):
                entry["frames_per_second"] = entry["rate"] / entry["scale"]
            streams.append(entry)
        result["streams"] = streams
    video = next((s for s in result.get("streams", []) if s.get("type") == "vids"), {})
    result["duration_seconds"] = video.get("declared_duration_seconds")
    return result


def decode_samples(path, samples):
    from PIL import Image
    dll = ctypes.WinDLL("avifil32.dll")
    dll.AVIFileInit.argtypes = []
    dll.AVIFileInit.restype = None
    dll.AVIFileExit.argtypes = []
    dll.AVIFileExit.restype = None
    dll.AVIFileOpenW.argtypes = [ctypes.POINTER(ctypes.c_void_p), wintypes.LPCWSTR, wintypes.UINT, ctypes.c_void_p]
    dll.AVIFileOpenW.restype = wintypes.LONG
    dll.AVIFileGetStream.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), wintypes.DWORD, wintypes.LONG]
    dll.AVIFileGetStream.restype = wintypes.LONG
    dll.AVIStreamGetFrameOpen.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    dll.AVIStreamGetFrameOpen.restype = ctypes.c_void_p
    dll.AVIStreamGetFrame.argtypes = [ctypes.c_void_p, wintypes.LONG]
    dll.AVIStreamGetFrame.restype = ctypes.c_void_p
    dll.AVIStreamGetFrameClose.argtypes = [ctypes.c_void_p]
    dll.AVIStreamGetFrameClose.restype = wintypes.LONG
    dll.AVIStreamRelease.argtypes = [ctypes.c_void_p]
    dll.AVIStreamRelease.restype = wintypes.ULONG
    dll.AVIFileRelease.argtypes = [ctypes.c_void_p]
    dll.AVIFileRelease.restype = wintypes.ULONG
    avi_file, avi_stream, frame_reader = ctypes.c_void_p(), ctypes.c_void_p(), None
    outputs = []
    dll.AVIFileInit()
    try:
        code = dll.AVIFileOpenW(ctypes.byref(avi_file), str(path), 0, None)
        if code:
            raise RuntimeError(f"AVIFileOpenW failed: {code:#x}")
        code = dll.AVIFileGetStream(avi_file, ctypes.byref(avi_stream), int.from_bytes(b"vids", "little"), 0)
        if code:
            raise RuntimeError(f"AVIFileGetStream failed: {code:#x}")
        frame_reader = dll.AVIStreamGetFrameOpen(avi_stream, None)
        if not frame_reader:
            raise RuntimeError("AVIStreamGetFrameOpen did not find an available decoder")
        for sample in samples:
            pointer = dll.AVIStreamGetFrame(frame_reader, sample["frame_index"])
            if not pointer:
                outputs.append({**sample, "error": "AVIStreamGetFrame returned NULL"})
                continue
            header = ctypes.string_at(pointer, 40)
            size, width, height, planes, bits, compression, image_size, xppm, yppm, colors, important = struct.unpack("<IiiHHIIiiII", header)
            if compression not in (0, 3) or size > 4096:
                raise RuntimeError(f"Unsupported output DIB: {compression}, {size}")
            palette_bytes = colors * 4 if colors else ((1 << bits) * 4 if bits <= 8 else 0)
            mask_bytes = 12 if compression == 3 and size == 40 else 0
            stride = ((abs(width) * bits + 31) // 32) * 4
            pixel_bytes = stride * abs(height)
            dib_length = size + palette_bytes + mask_bytes + pixel_bytes
            dib = ctypes.string_at(pointer, dib_length)
            bmp_header = struct.pack("<2sIHHI", b"BM", 14 + dib_length, 0, 0, 14 + size + palette_bytes + mask_bytes)
            import io
            image = Image.open(io.BytesIO(bmp_header + dib))
            output = WORK / f"allegro_lesson01_{sample['seconds']:03d}s.png"
            image.save(output)
            outputs.append({**sample, "path": str(output), "width": image.width, "height": image.height})
    finally:
        if frame_reader:
            dll.AVIStreamGetFrameClose(frame_reader)
        if avi_stream:
            dll.AVIStreamRelease(avi_stream)
        if avi_file:
            dll.AVIFileRelease(avi_file)
        dll.AVIFileExit()
    return outputs


files = []
source_summaries = []
snapshot_started_at = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
for source_key, source in (("complete_named", SOURCE), ("short_named", ALTERNATE_SOURCE)):
    source_files = []
    source_scan_started_at = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    for path in sorted(source.glob("*.avi")):
        match = re.search(r"(\d+)", path.name)
        entry = {"lesson_number": int(match.group(1)) if match else None,
                 "source_key": source_key,
                 "name": path.name, "path": str(path), "bytes": path.stat().st_size,
                 "learning_status": "indexed_only"}
        try:
            entry["avi_header"] = inspect_header(path)
            entry["header_readable"] = True
        except Exception as exc:
            entry.update(header_readable=False, error=str(exc))
        entry["size_after_header_read"] = path.stat().st_size
        entry["size_changed_during_header_read"] = entry["bytes"] != entry["size_after_header_read"]
        files.append(entry)
        source_files.append(entry)
    source_numbers = [entry["lesson_number"] for entry in source_files]
    source_summaries.append({"source_key": source_key, "path": str(source),
                             "scan_started_at_local": source_scan_started_at,
                             "scan_finished_at_local": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
                             "download_status": "not_verified; user reports downloading into complete_named",
                             "avi_count": len(source_files),
                             "total_bytes": sum(entry["bytes"] for entry in source_files),
                             "missing_numbers": sorted(set(range(1, 73)) - set(source_numbers)),
                             "header_readable_count": sum(entry["header_readable"] for entry in source_files),
                             "declared_total_duration_seconds": sum(entry.get("avi_header", {}).get("duration_seconds") or 0 for entry in source_files)})

numbers = [entry["lesson_number"] for entry in files if entry["lesson_number"] is not None]
preferred_by_number = {}
for entry in sorted(files, key=lambda entry: entry["source_key"] != "short_named"):
    preferred_by_number.setdefault(entry["lesson_number"], entry)
preferred_files = [preferred_by_number[number] for number in sorted(preferred_by_number)]
overlap_numbers = sorted({number for number in numbers if numbers.count(number) > 1})
overlap_comparisons = []
for number in overlap_numbers:
    versions = [entry for entry in files if entry["lesson_number"] == number]
    overlap_comparisons.append({"lesson_number": number,
                                "names_equal": len({entry["name"] for entry in versions}) == 1,
                                "sizes_equal": len({entry["bytes"] for entry in versions}) == 1,
                                "durations_equal": len({entry.get("avi_header", {}).get("duration_seconds") for entry in versions}) == 1,
                                "content_hash_checked": False})
inventory = {"inventory_date_local": "2026-10-17", "timezone": "Asia/Shanghai",
             "snapshot_started_at_local": snapshot_started_at,
             "snapshot_finished_at_local": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
             "source_is_changing": True,
             "user_context": {"old_source_renamed_to_short_named": True, "complete_named_is_downloading": True,
                              "pdf_and_local_project_version": "17.2", "video_version": "16.6",
                              "user_says_main_workflow_common": True, "microcontroller_study": "deferred"},
             "historical_snapshots": [
                 {"when": "Earlier in this task; exact clock time not separately captured", "source_key": "short_named",
                  "avi_count": 69, "missing_numbers": [15, 17, 18], "note": "Old copy subsequently identified by the user as renamed"},
                 {"when": "During download, before the latest timestamped snapshot; exact clock time not separately captured",
                  "source_key": "complete_named", "avi_count": 47,
                  "absent_numbers_at_that_time": [42] + list(range(49, 73)), "note": "Transient count, not a fixed missing-lesson finding"}],
             "source_directory": str(SOURCE), "advertised_lesson_count": 72,
             "source_directories": source_summaries,
             "avi_count": len(files), "missing_numbers": sorted(set(range(1, 73)) - set(numbers)),
             "unique_lesson_count": len(preferred_files),
             "duplicate_numbers": overlap_numbers,
             "overlap_comparisons": overlap_comparisons,
             "total_bytes": sum(entry["bytes"] for entry in files),
             "header_readable_count": sum(entry["header_readable"] for entry in files),
             "declared_total_duration_seconds": sum(entry.get("avi_header", {}).get("duration_seconds") or 0 for entry in preferred_files),
             "all_files_declared_duration_seconds": sum(entry.get("avi_header", {}).get("duration_seconds") or 0 for entry in files),
             "subtitle_files": [str(p) for source in (SOURCE, ALTERNATE_SOURCE) for p in source.rglob("*") if p.suffix.lower() in (".srt", ".vtt", ".ass", ".ssa")],
             "duration_method": "AVI video stream length * scale / rate; headers only, not full playback validation",
             "preferred_file_method": "Use the old short_named source when available; otherwise index the currently present complete_named source. Do not assume downloads are complete.",
             "frame_decode_method": "Windows avifil32/VfW built-in decoder, no GUI, no installation",
             "limits": ["No complete video playback or audio transcription", "Sample frames do not establish the full lesson contents", "Filename topics are a learning index, not verified instructional claims"],
             "files": files, "preferred_files": preferred_files}
first = preferred_by_number[1]
inventory["lesson01_sample_source"] = {"path": first["path"], "source_key": first["source_key"],
                                       "source_bytes": first["bytes"],
                                       "method": "Samples re-decoded from the exact old-copy short_named path after the rename was identified"}
fps = next(s["frames_per_second"] for s in first["avi_header"]["streams"] if s["type"] == "vids")
try:
    inventory["lesson01_sample_frames"] = decode_samples(pathlib.Path(first["path"]),
            [{"seconds": seconds, "frame_index": round(seconds * fps)} for seconds in (0, 30, 60, 120, 180)])
    first["learning_status"] = "sampled_visual_only"
except Exception as exc:
    inventory["sample_decode_error"] = f"{type(exc).__name__}: {exc}"

WORK.mkdir(parents=True, exist_ok=True)
output = WORK / "video_inventory.json"
# ASCII Unicode escapes also survive Windows PowerShell 5's default ANSI reader.
# json.loads still restores the exact Unicode filesystem paths.
output.write_text(json.dumps(inventory, ensure_ascii=True, indent=2), encoding="utf-8")
summary = {key: value for key, value in inventory.items() if key not in ("files", "preferred_files", "source_directory", "overlap_comparisons", "duplicate_numbers")}
print(json.dumps(summary, ensure_ascii=True, indent=2))
