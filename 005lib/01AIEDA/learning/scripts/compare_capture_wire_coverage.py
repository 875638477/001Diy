"""Read-only Capture WireScalar geometry/style comparison, independent of segmentation.

Maps are same-version native TSVs with page/id/net_name columns. A planned XML
needs an explicitly reviewed map for any newly allocated wire IDs. This checks
geometry and native net names; it does not replace a complete PST pin comparison.
"""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET


def read_map(path):
    result = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not {"page", "id", "net_name"} <= set(reader.fieldnames or []):
            raise ValueError("Wire map requires page/id/net_name columns")
        for row in reader:
            key = (row["page"], row["id"])
            if key in result:
                raise ValueError("Duplicate native wire identity: " + repr(key))
            if not row["net_name"]:
                raise ValueError("Unbound native net identity: " + repr(key))
            result[key] = row["net_name"]
    return result


def normalize(xml, wire_nets):
    groups = collections.defaultdict(list)
    seen = set()
    count = 0
    for page in ET.parse(xml).getroot().findall("./Schematic/Page"):
        name = page.find("Defn").get("name")
        for wire in page.findall("./NetScalar/WireScalar"):
            data = wire.find("Defn").attrib
            identity = (name, data["dbId"])
            if identity in seen:
                raise ValueError("Duplicate XML wire identity: " + repr(identity))
            seen.add(identity)
            net = wire_nets[identity]
            x1, y1, x2, y2 = (int(data[k]) for k in ("startX", "startY", "endX", "endY"))
            style = tuple(wire.find(tag + "/Defn").get("val")
                          for tag in ("WireColor", "WireLineStyle", "WireLineWidth"))
            dx, dy = x2 - x1, y2 - y1
            divisor = math.gcd(abs(dx), abs(dy))
            count += 1
            if not divisor:
                groups[(name, net, style, "POINT", x1, y1)].append((0, 0))
                continue
            ux, uy = dx // divisor, dy // divisor
            if ux < 0 or (ux == 0 and uy < 0):
                ux, uy = -ux, -uy
            line = ux * y1 - uy * x1
            interval = tuple(sorted((ux * x1 + uy * y1, ux * x2 + uy * y2)))
            groups[(name, net, style, ux, uy, line)].append(interval)
    if not count:
        raise ValueError("No WireScalar objects in the Capture design XML")
    result = {}
    for key, intervals in groups.items():
        merged = []
        for low, high in sorted(intervals):
            if merged and low <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(high, merged[-1][1]))
            else:
                merged.append((low, high))
        result[key] = tuple(merged)
    return result, count


def compare(reference_xml, candidate_xml, reference_map, candidate_map):
    before, before_count = normalize(reference_xml, reference_map)
    after, after_count = normalize(candidate_xml, candidate_map)
    missing = sorted(before.keys() - after.keys(), key=repr)
    extra = sorted(after.keys() - before.keys(), key=repr)
    changed = [{"key": key, "reference": before[key], "candidate": after[key]}
               for key in sorted(before.keys() & after.keys(), key=repr)
               if before[key] != after[key]]
    return {"status": "PASS" if not (missing or extra or changed) else "FAIL",
            "scope": "Exact integer coverage by page, native net name, color, style and width. No pin, junction or manufacturing signoff.",
            "reference_wire_objects": before_count, "candidate_wire_objects": after_count,
            "normalized_groups": len(before), "missing_groups": missing,
            "extra_groups": extra, "changed_intervals": changed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("reference-xml", "candidate-xml", "reference-map", "candidate-map", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.output.suffix.lower() != ".json":
        raise ValueError("Output must be a new .json report; refusing overwrite")
    result = compare(args.reference_xml, args.candidate_xml,
                     read_map(args.reference_map), read_map(args.candidate_map))
    result["input_sha256"] = {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                              for path in (args.reference_xml, args.candidate_xml,
                                           args.reference_map, args.candidate_map)}
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("input_sha256", "missing_groups", "extra_groups", "changed_intervals")}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
