"""Read-only validation of Capture's reopened A4 schematic TSV evidence.

No Cadence DLL, DSN mutation, GUI automation, or network access is used.  Run
after the native reader has produced after_*.tsv in the staging directory.
Only validation.json is written, beside that evidence, inside 01AIEDA.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import math
from pathlib import Path
import sys


LEARNING = Path(__file__).resolve().parents[1]
RECORD_ROOT = LEARNING.parent
DEFAULT_DATA = LEARNING / "staging" / "a4_review_20261019"
DEFAULT_SPEC = LEARNING / "examples" / "de_15_26_20261019" / "integrated_circuit.json"
TABLE_COLUMNS = {
    "pages": "page size metric width_native height_native pintopin doc_per_inch granularity doc_width doc_height draw_width draw_height".split(),
    "instances": "page reference value x y left top right bottom footprint".split(),
    "pins": "page reference number name nc net hotx hoty".split(),
    "wires": "page x1 y1 x2 y2".split(),
    "aliases": "page name x y font_height".split(),
    "offpages": "page name hotx hoty left top right bottom".split(),
}


def inside_records(path: Path) -> Path:
    path = path.resolve()
    if not path.is_relative_to(RECORD_ROOT.resolve()):
        raise ValueError(f"Path must remain inside {RECORD_ROOT}: {path}")
    return path


def number(value: object) -> float:
    result = float(str(value).strip())
    if not math.isfinite(result):
        raise ValueError(f"Non-finite coordinate: {value!r}")
    return result


def boolean(value: object) -> bool:
    value = str(value).strip().lower()
    if value in {"1", "true", "yes"}:
        return True
    if value in {"0", "false", "no"}:
        return False
    raise ValueError(f"Unrecognized boolean: {value!r}")


def run(args: argparse.Namespace) -> dict:
    data_dir = inside_records(args.data_dir)
    spec_path = inside_records(args.spec)
    failures: list[dict] = []
    categories: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    inputs: dict[str, str] = {"spec": str(spec_path)}
    tables: dict[str, list[dict[str, str]]] = {}

    def check(category: str, check_name: str, passed: bool, **details: object) -> None:
        categories[category]["total"] += 1
        categories[category]["passed" if passed else "failed"] += 1
        if not passed:
            failures.append({"category": category, "check": check_name, **details})

    for key, required in TABLE_COLUMNS.items():
        path = data_dir / f"after_{key}.tsv"
        inputs[key] = str(path)
        check("input", "evidence_file_exists", path.is_file(), table=key, path=str(path))
        if not path.is_file():
            continue
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            missing = sorted(set(required) - set(reader.fieldnames or []))
            check("input", "required_columns", not missing, table=key, missing=missing)
            if not missing:
                tables[key] = list(reader)

    check("input", "spec_exists", spec_path.is_file(), path=str(spec_path))
    if len(tables) != len(TABLE_COLUMNS) or not spec_path.is_file():
        return finish("INCOMPLETE", inputs, categories, failures, {}, {}, {}, {})

    spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    components = {c["ref"]: c for c in spec["components"]}
    expected_pins = {
        (c["ref"], str(pin["number"])): {
            "name": pin["name"], "net": c["pins"][str(pin["number"])] or "",
            "model": c["model"], "hot": pin["hot"],
        }
        for c in spec["components"] for pin in spec["models"][c["model"]]["pins"]
    }
    expected_nets = {p["net"] for p in expected_pins.values() if p["net"]}
    expected_nc = sum(not p["net"] for p in expected_pins.values())
    check("counts", "source_spec_baseline", (len(components), len(expected_pins), len(expected_nets), expected_nc) == (80, 272, 69, 6),
          expected=[80, 272, 69, 6], actual=[len(components), len(expected_pins), len(expected_nets), expected_nc])
    for key, expected in (("pages", args.expected_pages), ("instances", 80), ("pins", 272)):
        check("counts", f"{key}_count", len(tables[key]) == expected, expected=expected, actual=len(tables[key]))

    pages: dict[str, dict] = {}
    for row in tables["pages"]:
        page = row["page"]
        check("pages", "unique_page_name", page not in pages and bool(page), page=page)
        try:
            metric = boolean(row["metric"])
            width, height = number(row["width_native"]), number(row["height_native"])
            draw_width, draw_height = number(row["draw_width"]), number(row["draw_height"])
            doc_per_inch = number(row["doc_per_inch"])
            pages[page] = {**row, "draw_width": draw_width, "draw_height": draw_height}
            check("pages", "A4_preset", row["size"].strip().upper() == "A4", page=page, actual=row["size"])
            check("pages", "metric_units", metric, page=page, actual=row["metric"])
            # Metric native size uses 1/1000 mm.  Either A4 orientation is valid.
            check("pages", "A4_physical_size", metric and sorted([width, height]) == [210000, 297000],
                  page=page, expected_mm=[297, 210], actual_native=[width, height])
            scale = doc_per_inch / (25400 if metric else 1000)
            expected_draw = [width * scale, height * scale]
            check("pages", "drawing_coordinate_scale", doc_per_inch > 0 and all(abs(a - b) <= 1.1 for a, b in zip([draw_width, draw_height], expected_draw)),
                  page=page, expected_document_dimensions=expected_draw, actual=[draw_width, draw_height])
            check("pages", "document_dimensions", abs(number(row["doc_width"]) - draw_width) <= 1 and abs(number(row["doc_height"]) - draw_height) <= 1,
                  page=page, document=[row["doc_width"], row["doc_height"]], drawing=[draw_width, draw_height])
            # Preserve the established 0.100 inch pin-to-pin document scale.
            expected_pitch = 2540 if metric else 100
            check("pages", "pin_to_pin_0_100_inch", number(row["pintopin"]) == expected_pitch,
                  page=page, expected_native=expected_pitch, actual=row["pintopin"])
        except (ValueError, TypeError, KeyError) as exc:
            check("pages", "valid_dimensions", False, page=page, error=str(exc))

    extents: dict[str, dict[str, list[float]]] = collections.defaultdict(dict)
    geometry_counts = collections.Counter()

    def bounds(kind: str, page: str, identity: object, box: tuple[float, float, float, float]) -> None:
        geometry_counts[kind] += 1
        check("geometry", "object_page_exists", page in pages, kind=kind, object=identity, page=page)
        if page not in pages:
            return
        left, top, right, bottom = box
        check("geometry", "ordered_bounds", left <= right and top <= bottom,
              kind=kind, page=page, object=identity, bounds=list(box))
        width, height = pages[page]["draw_width"], pages[page]["draw_height"]
        check("geometry", "inside_A4_drawing_area", left >= -0.01 and top >= -0.01 and right <= width + 0.01 and bottom <= height + 0.01,
              kind=kind, page=page, object=identity, bounds=list(box), page_bounds=[0, 0, width, height])
        current = extents[page].get(kind)
        extents[page][kind] = [left, top, right, bottom] if current is None else [min(current[0], left), min(current[1], top), max(current[2], right), max(current[3], bottom)]

    def text_bounds(kind: str, page: str, identity: object, text: str, x: float, y: float, font_height: object = -10) -> None:
        height = abs(number(font_height or -10)) or 10
        # The writer uses horizontal, left-justified text.  Reserve a full font
        # height above and below its anchor; pin labels are in native part bbox.
        width = len(text) * height * 0.65
        bounds(kind, page, identity, (x, y - height, x + width, y + height))

    instances: dict[str, dict] = {}
    empty_native_bboxes: list[str] = []
    for row in tables["instances"]:
        ref, page = row["reference"], row["page"]
        check("instances", "unique_reference", ref not in instances, reference=ref)
        instances[ref] = row
        check("instances", "known_reference", ref in components, reference=ref)
        try:
            native_box = tuple(number(row[k]) for k in ("left", "top", "right", "bottom"))
            if native_box == (0, 0, 0, 0):
                # Capture's headless path does not populate this display cache.
                # Never count the empty cache as evidence that the part fits.
                empty_native_bboxes.append(ref)
            else:
                bounds("instance_native_bbox", page, ref, native_box)
            x, y = number(row["x"]), number(row["y"])
            bounds("instance_origin", page, ref, (x, y, x, y))
            if ref in components:
                c = components[ref]
                model = spec["models"][c["model"]]
                bounds("instance_model_body", page, ref, (x, y, x + model["width"], y + model["height"]))
                for pin in model["pins"]:
                    for point_kind in ("start", "hot"):
                        px, py = pin[point_kind]
                        bounds("instance_model_pin_geometry", page, [ref, str(pin["number"]), point_kind], (x + px, y + py, x + px, y + py))
                check("instances", "value_preserved", row["value"] == c["value"], reference=ref, expected=c["value"], actual=row["value"])
                check("instances", "footprint_preserved", row["footprint"] == model["footprint"], reference=ref, expected=model["footprint"], actual=row["footprint"])
                font = row.get("font_height", -10)
                text_bounds("reference_text_estimate", page, ref, ref,
                            number(row.get("reference_x") or x), number(row.get("reference_y") or y - 20), font)
                text_bounds("value_text_estimate", page, ref, row["value"],
                            number(row.get("value_x") or x), number(row.get("value_y") or y + model["height"] + 30), font)
        except (ValueError, TypeError, KeyError) as exc:
            check("geometry", "valid_instance_coordinates", False, reference=ref, error=str(exc))
    check("instances", "exact_reference_set", set(instances) == set(components), missing=sorted(set(components) - set(instances)), unexpected=sorted(set(instances) - set(components)))

    seen_pins: set[tuple[str, str]] = set()
    actual_nets: set[str] = set()
    actual_nc = 0
    for row in tables["pins"]:
        key = (row["reference"], str(row["number"]))
        page, net = row["page"], row["net"] or ""
        check("pins", "unique_physical_pin", key not in seen_pins, pin=list(key))
        seen_pins.add(key)
        check("pins", "known_physical_pin", key in expected_pins, pin=list(key))
        if net:
            actual_nets.add(net)
        try:
            nc = boolean(row["nc"])
            actual_nc += nc
            x, y = number(row["hotx"]), number(row["hoty"])
            bounds("pin_hotspot", page, list(key), (x, y, x, y))
            if key in expected_pins:
                expected = expected_pins[key]
                check("pins", "pin_name_preserved", row["name"] == expected["name"], pin=list(key), expected=expected["name"], actual=row["name"])
                check("pins", "pin_net_preserved", net == expected["net"], pin=list(key), expected=expected["net"], actual=net)
                check("pins", "NC_flag_preserved", nc == (not expected["net"]), pin=list(key), expected=not expected["net"], actual=nc)
                if key[0] in instances:
                    inst = instances[key[0]]
                    expected_hot = [number(inst["x"]) + expected["hot"][0], number(inst["y"]) + expected["hot"][1]]
                    check("pins", "absolute_hotspot_matches_unchanged_symbol", [x, y] == expected_hot,
                          pin=list(key), expected=expected_hot, actual=[x, y])
            check("pins", "pin_matches_instance_page", key[0] in instances and page == instances[key[0]]["page"], pin=list(key), page=page)
        except (ValueError, TypeError, KeyError) as exc:
            check("pins", "valid_pin_evidence", False, pin=list(key), error=str(exc))
    check("pins", "exact_physical_pin_set", seen_pins == set(expected_pins), missing=sorted(set(expected_pins) - seen_pins), unexpected=sorted(seen_pins - set(expected_pins)))
    check("counts", "net_set_69", actual_nets == expected_nets and len(actual_nets) == 69, actual_count=len(actual_nets), missing=sorted(expected_nets - actual_nets), unexpected=sorted(actual_nets - expected_nets))
    check("counts", "explicit_NC_6", actual_nc == 6, expected=6, actual=actual_nc)

    endpoints: dict[str, set[tuple[float, float]]] = collections.defaultdict(set)
    for index, row in enumerate(tables["wires"], 1):
        try:
            x1, y1, x2, y2 = (number(row[k]) for k in ("x1", "y1", "x2", "y2"))
            bounds("wire", row["page"], index, (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
            endpoints[row["page"]].update(((x1, y1), (x2, y2)))
            check("geometry", "nonzero_wire", (x1, y1) != (x2, y2), wire=index, page=row["page"])
        except (ValueError, TypeError, KeyError) as exc:
            check("geometry", "valid_wire_coordinates", False, wire=index, error=str(exc))

    for index, row in enumerate(tables["aliases"], 1):
        try:
            check("aliases", "known_network_alias", row["name"] in expected_nets, alias=index, page=row["page"], name=row["name"])
            text_bounds("alias_text_estimate", row["page"], f"{index}:{row['name']}", row["name"], number(row["x"]), number(row["y"]), row["font_height"])
        except (ValueError, TypeError, KeyError) as exc:
            check("geometry", "valid_alias_coordinates", False, alias=index, error=str(exc))

    net_pages: dict[str, set[str]] = collections.defaultdict(set)
    for (ref, _), pin in expected_pins.items():
        if pin["net"] and ref in instances:
            net_pages[pin["net"]].add(instances[ref]["page"])
    cross_pages = {net: sorted(page_set) for net, page_set in net_pages.items() if len(page_set) > 1}
    required_ports = {(page, net) for net, page_names in cross_pages.items() for page in page_names}
    observed_ports: set[tuple[str, str]] = set()
    native_port_name_anchors = 0
    for index, row in enumerate(tables["offpages"], 1):
        page, net = row["page"], row["name"]
        observed_ports.add((page, net))
        check("offpages", "known_network_port", net in expected_nets, port=index, page=page, name=net)
        try:
            port_box = tuple(number(row[k]) for k in ("left", "top", "right", "bottom"))
            bounds("offpage_native_bbox", page, f"{index}:{net}", port_box)
            point = (number(row["hotx"]), number(row["hoty"]))
            bounds("offpage_hotspot", page, f"{index}:{net}", (*point, *point))
            if row.get("name_x") not in {None, ""} and row.get("name_y") not in {None, ""}:
                name_x, name_y = number(row["name_x"]), number(row["name_y"])
                native_port_name_anchors += 1
                check("offpages", "port_name_displayed", row.get("name_display_type") == "1",
                      port=index, page=page, name=net, actual=row.get("name_display_type"))
            else:
                hot_on_left = abs(point[0] - port_box[0]) <= abs(point[0] - port_box[2])
                name_x = point[0] + 10 if hot_on_left else point[0] - 10 - len(net) * 10 * 0.65
                name_y = point[1]
            text_bounds("offpage_name_text_estimate", page, f"{index}:{net}", net, name_x, name_y, -10)
            check("offpages", "hotspot_on_actual_wire_endpoint", point in endpoints.get(page, set()), port=index, page=page, name=net, hotspot=list(point))
        except (ValueError, TypeError, KeyError) as exc:
            check("geometry", "valid_offpage_coordinates", False, port=index, error=str(exc))
    for page, net in sorted(required_ports):
        check("offpages", "cross_page_network_covered", (page, net) in observed_ports, page=page, net=net)

    module_boxes = []
    if args.layout_plan:
        plan_path = inside_records(args.layout_plan)
        inputs["layout_plan"] = str(plan_path)
        check("input", "layout_plan_exists", plan_path.is_file(), path=str(plan_path))
        if plan_path.is_file():
            plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
            module_boxes = plan.get("modules", [])
            for index, box in enumerate(module_boxes, 1):
                try:
                    rect = tuple(number(box[k]) for k in ("left", "top", "right", "bottom"))
                    bounds("module_planned_bbox", box["page"], box.get("name", index), rect)
                    for prior in module_boxes[:index - 1]:
                        if prior["page"] != box["page"]:
                            continue
                        overlap_x = min(rect[2], number(prior["right"])) - max(rect[0], number(prior["left"]))
                        overlap_y = min(rect[3], number(prior["bottom"])) - max(rect[1], number(prior["top"]))
                        check("layout", "module_boxes_do_not_overlap", overlap_x <= 0 or overlap_y <= 0,
                              page=box["page"], modules=[prior.get("name"), box.get("name")], overlap=[overlap_x, overlap_y])
                except (ValueError, TypeError, KeyError) as exc:
                    check("layout", "valid_module_box", False, module=index, error=str(exc))

    counts = {key: len(rows) for key, rows in tables.items()}
    counts.update(unique_references=len(instances), unique_physical_pins=len(seen_pins), connected_net_names=len(actual_nets), explicit_no_connect=actual_nc)
    geometry = {
        "objects_checked": dict(geometry_counts), "page_extents_by_kind": dict(extents),
        "empty_native_instance_bbox_references": empty_native_bboxes,
        "instance_boundary_source": "Nonempty native display bbox where available; otherwise original-spec body/pin geometry translated by native instance x/y, independently checked against absolute native pin hotspots, wires, ports and estimated Ref/Value/alias text. Zero native bbox is never counted as a passing object boundary.",
        "text_estimate_policy": "Horizontal left-justified text: width=len(text)*abs(font_height)*0.65; default font_height=-10; reserve one font height above and below anchor. Native instance bbox also covers pin labels and displayed attributes.",
        "module_plan_provided": bool(args.layout_plan), "module_boxes": len(module_boxes),
        "native_offpage_name_anchors": native_port_name_anchors,
        "estimated_offpage_name_anchors": len(tables["offpages"]) - native_port_name_anchors,
        "offpage_name_anchor_policy": "Use absolute native Name display-property name_x/name_y when supplied. For older TSV evidence only, estimate 10 units inward from the actual port hotspot. Font size -10 and text width remain conservative approximations; actual Capture glyph extents are not measured.",
        "coincident_endpoints_are_not_reported_as_text_or_module_overlap": True,
    }
    cross = {"net_pages": cross_pages, "required_page_net_pairs": len(required_ports),
             "observed_unique_page_net_pairs": len(observed_ports),
             "missing_page_net_pairs": [list(v) for v in sorted(required_ports - observed_ports)],
             "additional_page_net_pairs": [list(v) for v in sorted(observed_ports - required_ports)]}
    return finish("FAIL" if failures else "PASS", inputs, categories, failures, counts, pages, geometry, cross)


def finish(status: str, inputs: dict, categories: dict, failures: list, counts: dict, pages: dict, geometry: dict, cross: dict) -> dict:
    return {
        "schema": "capture_a4_readback_validation_v1",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": status, "inputs": inputs, "counts": counts,
        "checks": {"total": sum(v["total"] for v in categories.values()),
                   "passed": sum(v["passed"] for v in categories.values()),
                   "failed": sum(v["failed"] for v in categories.values()),
                   "by_category": dict(categories)},
        "failures": failures, "pages": pages, "geometry": geometry,
        "cross_page_connectivity": cross,
        "limitations": [
            "This validates native reopened TSV evidence; it does not independently parse the binary DSN.",
            "Text bounds are conservative estimates, not GUI-rendered glyph extents. Aliases have no native bbox in this evidence schema.",
            "Headless native instance display bboxes may be uncomputed (all zero); these are excluded and explicitly listed. The fallback assumes unchanged, unrotated source-spec symbol geometry and original display-property positions.",
            "Electrical pin-net comparison and off-page endpoint geometry do not replace Capture ERC, PCB ECO revalidation, or a visual page review.",
            "Only module rectangles supplied with --layout-plan are checked for mutual overlap; shared electrical endpoints are allowed.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--expected-pages", type=int, default=12)
    parser.add_argument("--layout-plan", type=Path)
    args = parser.parse_args()
    output = inside_records(args.data_dir) / "validation.json"
    if not output.parent.is_dir():
        parser.error(f"Evidence directory does not exist: {output.parent}")
    result = run(args)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": result["checks"], "failure_count": len(result["failures"]), "output": str(output)}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
