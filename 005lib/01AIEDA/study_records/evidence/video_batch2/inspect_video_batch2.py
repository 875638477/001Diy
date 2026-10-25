"""Batch 2: read-only RIFF boundary checks and sequential video decoding.

Reuse only the header helper definitions from batch 1; never execute its write code.
No original evidence, source media, application settings, or source programs are changed.
"""
from pathlib import Path
import ast
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone, timedelta
import hashlib
import io
import json
import re
import struct
from PIL import Image, ImageChops, ImageDraw, ImageStat

ROOT = Path(r"D:\001DIY\005lib\01AIEDA\study_records")
OUT = ROOT / "evidence" / "video_batch2"
SOURCE = Path(r"D:\005study\72讲速成视频【Cadence Allegro16.6视频教程】完整版")
OLD_SOURCE = Path(r"D:\005study\72讲速成视频【Cadence Allegro16.6视频教程")
LOCAL_TZ = timezone(timedelta(hours=8))


def now():
    return datetime.now(LOCAL_TZ).isoformat(timespec="seconds")


def dump(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")


helper_path = ROOT / "evidence" / "inspect_allegro_videos.py"
tree = ast.parse(helper_path.read_text(encoding="utf-8"))
helper_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ("chunks", "inspect_header")]
exec(compile(ast.Module(body=helper_defs, type_ignores=[]), str(helper_path), "exec"), globals())


def check_riff(path):
    result = {"method": "Top-level RIFF chunk boundaries, trailing bytes, idx1 metadata and last 32 index references; video payloads not decoded by this check"}
    file_size = path.stat().st_size
    with path.open("rb") as stream:
        head = stream.read(12)
        if len(head) != 12 or head[:4] != b"RIFF" or head[8:] != b"AVI ":
            return {**result, "status": "invalid_riff_avi_header"}
        riff_end = struct.unpack_from("<I", head, 4)[0] + 8
        result.update(file_size=file_size, riff_declared_end=riff_end,
                      riff_declared_length_within_file=riff_end <= file_size)
        if riff_end > file_size:
            return {**result, "status": "declared_riff_exceeds_current_file"}
        pos, top, errors, movi, index = 12, [], [], None, None
        while pos + 8 <= riff_end:
            stream.seek(pos)
            tag, size = struct.unpack("<4sI", stream.read(8))
            body = pos + 8
            end = body + size
            item = {"tag": tag.decode("ascii", "backslashreplace"), "offset": pos,
                    "size": size, "end": end}
            if end > riff_end:
                errors.append(f"Top-level chunk at {pos} exceeds RIFF boundary")
                top.append(item)
                break
            if tag == b"LIST":
                list_type = stream.read(4)
                item["list_type"] = list_type.decode("ascii", "backslashreplace")
                if list_type == b"movi":
                    movi = {"type_offset": body, "data_start": body + 4, "end": end}
            if tag == b"idx1":
                index = {"body": body, "size": size, "end": end}
            top.append(item)
            pos = end + (size & 1)
        if pos != riff_end:
            errors.append(f"Top-level chunks finish at {pos}, RIFF ends at {riff_end}")
        result.update(top_level_chunks=top, top_level_boundary_errors=errors,
                      top_level_chunks_end_at_declared_riff_end=pos == riff_end,
                      movi_found=bool(movi), idx1_found=bool(index))
        stream.seek(riff_end)
        trailing = stream.read()
        result.update(trailing_byte_count=len(trailing), trailing_bytes_all_zero=not any(trailing),
                      trailing_sha256=hashlib.sha256(trailing).hexdigest())
        if index:
            index_result = {"size_is_multiple_of_16": index["size"] % 16 == 0,
                            "entry_count": index["size"] // 16,
                            "last_index_entries_checked": []}
            count = min(32, index["size"] // 16)
            stream.seek(index["end"] - count * 16)
            tail = stream.read(count * 16)
            for offset in range(0, len(tail), 16):
                chunk_id, flags, chunk_offset, chunk_size = struct.unpack_from("<4sIII", tail, offset)
                candidates = [("absolute", chunk_offset)]
                if movi:
                    candidates = [("movi_type_relative", movi["type_offset"] + chunk_offset),
                                  ("movi_data_relative", movi["data_start"] + chunk_offset)] + candidates
                matched = None
                for base_name, absolute in candidates:
                    if absolute < 0 or absolute + 8 + chunk_size > riff_end:
                        continue
                    stream.seek(absolute)
                    actual = stream.read(8)
                    if len(actual) == 8 and actual[:4] == chunk_id and struct.unpack_from("<I", actual, 4)[0] == chunk_size:
                        matched = {"basis": base_name, "absolute_offset": absolute,
                                   "payload_within_movi": bool(movi and movi["data_start"] <= absolute and absolute+8+chunk_size <= movi["end"])}
                        break
                index_result["last_index_entries_checked"].append({
                    "chunk_id": chunk_id.decode("ascii", "backslashreplace"),
                    "index_flags": flags, "index_offset": chunk_offset,
                    "chunk_size": chunk_size, "matching_reference": matched})
            index_result["all_sampled_references_match_headers"] = all(item["matching_reference"] for item in index_result["last_index_entries_checked"])
            result["idx1"] = index_result
        passed = not errors and movi and index and index_result["size_is_multiple_of_16"] and index_result["all_sampled_references_match_headers"]
        result["status"] = "boundary_and_tail_sample_checks_passed" if passed else "needs_review"
    return result


def refresh_directory():
    started = now()
    previous = json.loads((ROOT / "evidence" / "video_inventory.json").read_text(encoding="utf-8"))
    previous_by_path = {entry["path"]: entry for entry in previous["files"]}
    manifest = json.loads((ROOT / "evidence" / "source_manifest.json").read_text(encoding="utf-8-sig"))
    manifest_by_path = {entry["path"]: entry for entry in manifest["files"]}
    files = []
    for path in sorted(SOURCE.glob("*.avi")):
        stat = path.stat()
        prior_video = previous_by_path.get(str(path))
        prior_manifest = manifest_by_path.get(str(path))
        item = {"name": path.name, "path": str(path), "lesson_number": int(re.search(r"\d+", path.name).group()),
                "bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns,
                "modified_at_local": datetime.fromtimestamp(stat.st_mtime, LOCAL_TZ).isoformat(),
                "avi_header": inspect_header(path), "riff_check": check_riff(path),
                "prior_video_snapshot_size_equal": prior_video["bytes"] == stat.st_size if prior_video else None,
                "prior_manifest_size_equal": prior_manifest["size_bytes"] == stat.st_size if prior_manifest else None,
                "prior_manifest_mtime_ns_equal": prior_manifest["mtime_ns"] == stat.st_mtime_ns if prior_manifest else None}
        after = path.stat()
        item["size_and_mtime_unchanged_during_check"] = (stat.st_size, stat.st_mtime_ns) == (after.st_size, after.st_mtime_ns)
        files.append(item)
    old_numbers = sorted(int(re.search(r"\d+", path.name).group()) for path in OLD_SOURCE.glob("*.avi"))
    result = {"snapshot_started_at_local": started, "snapshot_finished_at_local": now(),
              "source_directory": str(SOURCE), "old_directory": str(OLD_SOURCE),
              "primary_avi_count": len(files), "primary_missing_lesson_numbers": sorted(set(range(1,73)) - {item["lesson_number"] for item in files}),
              "primary_total_bytes": sum(item["bytes"] for item in files),
              "old_avi_count": len(old_numbers), "old_missing_lesson_numbers": sorted(set(range(1,73)) - set(old_numbers)),
              "previous_video_snapshot_at_local": previous["snapshot_started_at_local"],
              "previous_source_manifest_at_local": manifest["captured_at"],
              "files_equal_to_prior_video_size": sum(item["prior_video_snapshot_size_equal"] is True for item in files),
              "files_equal_to_prior_manifest_size_and_mtime": sum(item["prior_manifest_size_equal"] is True and item["prior_manifest_mtime_ns_equal"] is True for item in files),
              "riff_boundary_tail_checks_passed": sum(item["riff_check"]["status"] == "boundary_and_tail_sample_checks_passed" for item in files),
              "download_completion_confirmed": False, "full_media_integrity_confirmed": False,
              "limits": ["No all-video full decode", "No all-payload hash or download manifest verification", "RIFF boundary and tail index sampling do not establish error-free playback"],
              "attached_files": [{"path": str(path), "bytes": path.stat().st_size, "status": "presence_only_unread"} for path in SOURCE.iterdir() if path.suffix.lower() in (".pdf", ".jpg")],
              "files": files}
    dump("directory_snapshot.json", result)
    return result


class Reader:
    def __init__(self, path):
        self.path = path
        self.dll = ctypes.WinDLL("avifil32.dll")
        signatures = {
            "AVIFileInit": ([], None), "AVIFileExit": ([], None),
            "AVIFileOpenW": ([ctypes.POINTER(ctypes.c_void_p), wintypes.LPCWSTR, wintypes.UINT, ctypes.c_void_p], wintypes.LONG),
            "AVIFileGetStream": ([ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), wintypes.DWORD, wintypes.LONG], wintypes.LONG),
            "AVIStreamGetFrameOpen": ([ctypes.c_void_p, ctypes.c_void_p], ctypes.c_void_p),
            "AVIStreamGetFrame": ([ctypes.c_void_p, wintypes.LONG], ctypes.c_void_p),
            "AVIStreamGetFrameClose": ([ctypes.c_void_p], wintypes.LONG),
            "AVIStreamRelease": ([ctypes.c_void_p], wintypes.ULONG),
            "AVIFileRelease": ([ctypes.c_void_p], wintypes.ULONG)}
        for name, (args, restype) in signatures.items():
            function = getattr(self.dll, name)
            function.argtypes, function.restype = args, restype
        self.file, self.stream, self.reader = ctypes.c_void_p(), ctypes.c_void_p(), None

    def __enter__(self):
        self.dll.AVIFileInit()
        code = self.dll.AVIFileOpenW(ctypes.byref(self.file), str(self.path), 0, None)
        if code:
            raise RuntimeError(f"AVIFileOpenW {code:#x}")
        code = self.dll.AVIFileGetStream(self.file, ctypes.byref(self.stream), int.from_bytes(b"vids", "little"), 0)
        if code:
            raise RuntimeError(f"AVIFileGetStream {code:#x}")
        self.reader = self.dll.AVIStreamGetFrameOpen(self.stream, None)
        if not self.reader:
            raise RuntimeError("No VfW video decoder")
        return self

    def read(self, index):
        pointer = self.dll.AVIStreamGetFrame(self.reader, index)
        if not pointer:
            raise RuntimeError(f"AVIStreamGetFrame({index}) returned NULL")
        header = ctypes.string_at(pointer, 40)
        size, width, height, planes, bits, compression, image_size, xp, yp, colors, important = struct.unpack("<IiiHHIIiiII", header)
        if compression not in (0, 3) or size > 4096:
            raise RuntimeError("Unsupported output DIB")
        palette = colors * 4 if colors else ((1 << bits) * 4 if bits <= 8 else 0)
        masks = 12 if compression == 3 and size == 40 else 0
        pixels = ((abs(width) * bits + 31) // 32) * 4 * abs(height)
        length = size + palette + masks + pixels
        dib = ctypes.string_at(pointer, length)
        bmp = struct.pack("<2sIHHI", b"BM", 14+length, 0, 0, 14+size+palette+masks) + dib
        return Image.open(io.BytesIO(bmp)).convert("RGB")

    def __exit__(self, *args):
        if self.reader:
            self.dll.AVIStreamGetFrameClose(self.reader)
        if self.stream:
            self.dll.AVIStreamRelease(self.stream)
        if self.file:
            self.dll.AVIFileRelease(self.file)
        self.dll.AVIFileExit()


def decode_lesson(path, number=1, step_seconds=1, scene_threshold=6.5):
    started = now()
    header = inspect_header(path)
    video = next(stream for stream in header["streams"] if stream["type"] == "vids")
    fps, count = video["frames_per_second"], video["length"]
    frames, saved, errors = [], [], []
    last_small = None
    with Reader(path) as reader:
        for index in range(count):
            try:
                picture = reader.read(index)
                small = picture.resize((256,144)).convert("L")
                change = ImageStat.Stat(ImageChops.difference(small, last_small)).mean[0] if last_small else 0
                regular = index % round(step_seconds * fps) == 0
                scene = change >= scene_threshold
                item = {"frame_index": index, "seconds": index / fps,
                        "mean_thumbnail_luma_change": round(change, 4),
                        "decoded_pixel_sha256": hashlib.sha256(picture.tobytes()).hexdigest()}
                if regular or scene or index == count-1:
                    output = OUT / f"lesson{number:02d}_f{index:04d}.png"
                    picture.save(output)
                    item.update(path=str(output), regular_time_sample=regular,
                                scene_change_sample=scene, width=picture.width, height=picture.height)
                    saved.append(item)
                frames.append(item)
                last_small = small
            except Exception as exc:
                errors.append({"frame_index": index, "error": f"{type(exc).__name__}: {exc}"})
    contact_sheets = []
    for page, start in enumerate(range(0, len(saved), 24)):
        subset = saved[start:start+24]
        sheet = Image.new("RGB", (1360, 6*178), "#e5e7eb")
        draw = ImageDraw.Draw(sheet)
        for tile, entry in enumerate(subset):
            x, y = (tile % 4)*340, (tile//4)*178
            thumbnail = Image.open(entry["path"])
            thumbnail.thumbnail((336,151))
            sheet.paste(thumbnail, (x+2,y+2))
            draw.text((x+6,y+155), f"{entry['seconds']:06.1f}s  frame {entry['frame_index']:04d}" + (" scene" if entry['scene_change_sample'] else ""), fill="black")
        output = OUT / f"lesson{number:02d}_contact_{page:02d}.png"
        sheet.save(output)
        contact_sheets.append({"path": str(output), "sample_count": len(subset),
                               "first_seconds": subset[0]["seconds"], "last_seconds": subset[-1]["seconds"]})
    result = {"decode_started_at_local": started, "decode_finished_at_local": now(),
              "source_path": str(path), "source_bytes": path.stat().st_size,
              "source_mtime_ns": path.stat().st_mtime_ns, "lesson_number": number,
              "video_header": video, "declared_duration_seconds": header["duration_seconds"],
              "decode_method": "Sequential Windows VfW decoding of every declared video frame; no audio playback",
              "regular_sampling_interval_seconds": step_seconds, "scene_change_mean_luma_threshold": scene_threshold,
              "scene_change_metric": "Mean absolute difference of consecutive decoded 256x144 grayscale thumbnails on 0-255 scale",
              "declared_frame_count": count, "decoded_frame_count": len(frames),
              "decode_errors": errors, "saved_sample_count": len(saved),
              "saved_samples": saved, "contact_sheets": contact_sheets,
              "all_frame_measurements": frames,
              "learning_status": "decoded_and_sampled_visual_review_pending; audio_not_understood",
              "limits": ["Successful frame API return is not an independent codec correctness proof", "All decoded frames were not individually read by the assistant", "Audio not played or understood by this script"]}
    dump(f"lesson{number:02d}_frames.json", result)
    return result


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", type=int, default=1)
    parser.add_argument("--skip-directory", action="store_true")
    parser.add_argument("--sample-seconds", type=int, default=1)
    args = parser.parse_args()
    if not args.skip_directory:
        snapshot = refresh_directory()
        print(json.dumps({key:value for key,value in snapshot.items() if key not in ("files","attached_files")}, ensure_ascii=True))
    path = next(path for path in sorted(SOURCE.glob("*.avi")) if int(re.search(r"\d+", path.name).group()) == args.lesson)
    result = decode_lesson(path, args.lesson, args.sample_seconds)
    print(json.dumps({key:value for key,value in result.items() if key not in ("all_frame_measurements","saved_samples","contact_sheets","video_header")}, ensure_ascii=True))
