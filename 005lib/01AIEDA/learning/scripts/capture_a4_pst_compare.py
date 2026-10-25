"""Read-only, independent comparison of the A4 Capture design's native PST export.

All file writes are confined to the requested JSON report under 01AIEDA/learning.
This script neither opens nor modifies a Cadence database. The PST files were
produced separately by the installed Cadence pstswp.exe, rather than generated
from the JSON requirements used here as the independent comparison target.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import re
from datetime import datetime, timezone


LEARNING = pathlib.Path(__file__).resolve().parents[1]
EXAMPLE = LEARNING / "examples/de_15_26_20261019"
STAGING = LEARNING / "staging/a4_review_20261019"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(path: pathlib.Path) -> dict:
    return {
        "path": path.relative_to(LEARNING).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def parse_pst(netdir: pathlib.Path) -> tuple[dict, dict, set, set]:
    """Parse the actual exported primitives, instances, and physical nodes.

    Preserve NC as None, distinct from a missing node or an empty net name.
    Reject duplicate primitives, instances, or physical nodes rather than
    silently accepting the last occurrence.
    """
    primitives = {}
    for name, body in re.findall(
        r"primitive '([^']+)';(.*?)end_primitive;",
        (netdir / "pstchip.dat").read_text(encoding="utf-8-sig"),
        re.S,
    ):
        if name in primitives:
            raise ValueError(f"Duplicate PST primitive: {name}")
        pin_section, body_section = body.split("  body", 1)
        physical_pins = []
        for numbers in re.findall(r"PIN_NUMBER='\(([^)]*)\)';", pin_section):
            physical_pins.extend(p.strip() for p in numbers.split(","))
        if len(physical_pins) != len(set(physical_pins)):
            raise ValueError(f"Duplicate physical pin in primitive: {name}")
        primitives[name] = {
            "properties": dict(re.findall(r"([\w_]+)='([^']*)';", body_section)),
            "pins": set(physical_pins),
        }

    parts = {}
    physical_pins = set()
    part_text = (netdir / "pstxprt.dat").read_text(encoding="utf-8-sig")
    for ref, model in re.findall(r"PART_NAME\s+(\S+) '([^']+)':", part_text):
        if ref in parts:
            raise ValueError(f"Duplicate PST component: {ref}")
        primitive = primitives[model]
        parts[ref] = primitive["properties"]
        physical_pins.update((ref, pin) for pin in primitive["pins"])

    pins = {}
    net_names = set()
    net = None
    pending_name = False
    for line in (netdir / "pstxnet.dat").read_text(encoding="utf-8-sig").splitlines():
        if line.strip() == "NET_NAME":
            pending_name = True
            continue
        if pending_name:
            match = re.fullmatch(r"\s*'([^']+)'\s*", line)
            if not match:
                raise ValueError(f"Malformed PST net name: {line!r}")
            net = match.group(1)
            net_names.add(net)
            pending_name = False
            continue
        match = re.match(r"NODE_NAME\s+(\S+)\s+(\S+)", line)
        if match:
            key = tuple(match.groups())
            if net is None or key in pins:
                raise ValueError(f"Unscoped or duplicate PST physical node: {key}")
            pins[key] = None if net == "NC" else net
    if not parts or not pins or pending_name:
        raise ValueError("Incomplete or empty PST export")
    return parts, pins, physical_pins, net_names


def parse_before(path: pathlib.Path) -> dict:
    pins = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            key = (row["reference"], row["number"])
            if key in pins:
                raise ValueError(f"Duplicate original snapshot pin: {key}")
            if row["nc"] not in {"0", "1"}:
                raise ValueError(f"Unexpected NC flag: {key} {row['nc']}")
            if row["nc"] == "0" and not row["net"]:
                raise ValueError(f"Original pin is neither connected nor NC: {key}")
            pins[key] = None if row["nc"] == "1" else row["net"]
    return pins


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=pathlib.Path, default=STAGING / "pst_compare.json")
    args = parser.parse_args()
    output = args.out.resolve()
    if not output.is_relative_to(LEARNING):
        parser.error("The output report must remain inside 01AIEDA/learning")

    spec_path = EXAMPLE / "integrated_circuit.json"
    before_path = STAGING / "before_pins.tsv"
    native_path = EXAMPLE / "a4_review/native/DE_INTEGRATED_A4.DSN"
    source_path = EXAMPLE / "native/DE_INTEGRATED_BASELINE.DSN"
    snapshot_path = STAGING / "baseline_snapshot.dsn"
    netdir = STAGING / "packaging/netlist"
    launch_path = STAGING / "packaging_verified_process/launch.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    expected_parts = {c["ref"]: c for c in spec["components"]}
    expected_pins = {
        (c["ref"], str(pin)): net
        for c in spec["components"]
        for pin, net in c["pins"].items()
    }
    expected_nets = {net for net in expected_pins.values() if net is not None}
    parts, pins, chip_pins, exported_names = parse_pst(netdir)
    before = parse_before(before_path)
    launch = json.loads(launch_path.read_text(encoding="utf-8-sig"))
    checks = []

    def check(ok: bool, label: str, **evidence) -> None:
        checks.append({"pass": bool(ok), "check": label, **evidence})

    check(launch.get("completed") is True and launch.get("exitCode") == 0,
          "Cadence pstswp native export completed with exit code 0")
    identity = json.loads((STAGING / "pst_input_identity.json").read_text(encoding="utf-8"))
    check(identity['working_copy_sha256_before'] == identity['source_sha256_before'] == identity['source_sha256_after'] == sha256(native_path),
          "Working input matched the final A4 design before packaging; original design remained unchanged")
    check(len(parts) == 80, "80 native exported components", actual=len(parts))
    check(set(parts) == set(expected_parts), "Exact exported and requirement reference sets")
    check(len(chip_pins) == 272, "272 physical package pins in primitive/instance expansion",
          actual=len(chip_pins))
    check(chip_pins == set(expected_pins), "Exact primitive physical pin set versus requirements")
    check(set(pins) == chip_pins, "Every native primitive physical pin has exactly one exported node")
    check(set(pins) == set(expected_pins), "Exact exported physical node set versus requirements")
    actual_nets = {net for net in pins.values() if net is not None}
    check(len(actual_nets) == 69, "69 connected native nets; NC is excluded", actual=len(actual_nets))
    check(actual_nets == expected_nets, "Exact native net-name set versus requirements")
    check(exported_names == expected_nets | {"NC"}, "No unexpected or empty PST net sections")
    check(sum(net is None for net in pins.values()) == 6,
          "Six explicitly NC physical pins", actual=sum(net is None for net in pins.values()))
    check(sum(net is not None for net in pins.values()) == 266,
          "266 connected physical pins", actual=sum(net is not None for net in pins.values()))

    for ref, component in sorted(expected_parts.items()):
        attrs = parts.get(ref, {})
        actual_value = attrs.get("VALUE")
        expected_value = component["value"]
        check(actual_value is not None and actual_value.casefold() == expected_value.casefold(),
              f"{ref}: native value equals requirement", expected=expected_value, actual=actual_value)
        actual_footprint = attrs.get("JEDEC_TYPE")
        expected_footprint = spec["models"][component["model"]]["footprint"]
        check(actual_footprint is not None and actual_footprint.casefold() == expected_footprint.casefold(),
              f"{ref}: native footprint equals requirement",
              expected=expected_footprint, actual=actual_footprint)
    for key, expected_net in sorted(expected_pins.items()):
        check(key in pins and pins[key] == expected_net,
              f"{key[0]}.{key[1]}: native connection/NC equals requirement",
              expected=expected_net, actual=pins.get(key))

    check(set(before) == set(pins), "Exact original user-saved snapshot and A4 export physical pin sets")
    pin_changes = []
    for key in sorted(set(before) | set(pins)):
        equal = key in before and key in pins and before[key] == pins[key]
        check(equal, f"{key[0]}.{key[1]}: original snapshot to A4 connection/NC unchanged",
              before=before.get(key), after=pins.get(key))
        if not equal:
            pin_changes.append({"reference": key[0], "number": key[1],
                                "before": before.get(key), "after": pins.get(key),
                                "presentBefore": key in before, "presentAfter": key in pins})

    source_hash = sha256(source_path)
    snapshot_hash = sha256(snapshot_path)
    source_unchanged = source_hash == snapshot_hash
    # This is an observation, not a reason to overwrite a user-edited/open DSN.
    source_observation = {
        "currentSource": artifact(source_path),
        "savedSnapshot": artifact(snapshot_path),
        "currentlyIdentical": source_unchanged,
        "note": (
            "Original source and saved snapshot still have identical SHA-256."
            if source_unchanged else
            "Original source differs from the saved snapshot; the user may have saved further edits. "
            "No source database was changed or overwritten by this read-only comparison."
        ),
    }

    failures = [item for item in checks if not item["pass"]]
    inputs = [native_path, spec_path, before_path, launch_path]
    inputs.extend(netdir / name for name in ("pstchip.dat", "pstxprt.dat", "pstxnet.dat"))
    report = {
        "status": "PASS_A4_NATIVE_PST_COMPARE" if not failures else "FAIL_A4_NATIVE_PST_COMPARE",
        "createdUTC": datetime.now(timezone.utc).isoformat(),
        "scope": "Native PST component values, package identities, physical pins, nets and explicit NC; "
                 "comparison against requirements and every pin of the original user-saved snapshot.",
        "comparisonPolicy": "Values and footprint names compare case-insensitively; "
                            "reference designators, physical pin numbers and net names compare exactly; "
                            "PST NC maps to JSON null and explicit snapshot nc=1.",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "components": len(parts),
        "physicalPins": len(chip_pins),
        "exportedNodes": len(pins),
        "connectedPins": sum(net is not None for net in pins.values()),
        "netsExcludingNC": len(actual_nets),
        "explicitNCPins": [f"{ref}.{pin}" for (ref, pin), net in sorted(pins.items()) if net is None],
        "electricalChangesFromOriginalSnapshot": pin_changes,
        "sourceFileObservation": source_observation,
        "inputArtifacts": [artifact(path) for path in inputs],
        "details": checks,
        "limits": "This comparison does not certify GUI ERC, graphical readability or electrical hardware behavior.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "status", "checks", "passed", "failed", "components", "physicalPins", "exportedNodes",
        "connectedPins", "netsExcludingNC", "explicitNCPins", "electricalChangesFromOriginalSnapshot"
    )}, ensure_ascii=False, indent=2))
    print(json.dumps(source_observation, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
