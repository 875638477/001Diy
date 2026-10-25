"""Cross-check native Capture readback against datasheet-reviewed pin expectations.

This reads artifacts; it does not import or call the symbol creation helper.
All outputs remain in the learning tree.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "logs" / "capture_C_20261019"
EXAMPLE = ROOT / "examples" / "lesson12_capture"


def table(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    spec_path = EXAMPLE / "qmi8610_pin_spec.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    # Independently transcribed after visual review of source PDF pages 8-9,
    # not obtained by importing c12_helpers.tcl or its embedded pin table.
    names = ["RESV3", "VDDa", "GNDa", "RESV2", "RESV1", "SDA2", "SCL2", "VDDd",
             "SA0/SDO", "CS", "INT2/DRDY", "INT1/CLKout", "SDA/SDI/SDIO", "SCL/SPC", "GNDd", "RST"]
    i2c_types = [4, 7, 7, 4, 4, 1, 2, 7, 0, 0, 2, 2, 1, 0, 7, 0]
    spi_types = i2c_types.copy()
    spi_types[8], spi_types[12] = 2, 0
    powers = {2, 3, 8, 15}
    errors = []
    checked = []
    artifacts = []

    def check(condition, label):
        checked.append(label)
        if not condition:
            errors.append(label)

    source_path = Path(spec["source"]["path"])
    check(digest(source_path) == spec["source"]["sha256"], "source PDF sha256 unchanged")
    for profile, folder, library, types in [
        ("HOST_I2C", "c12_i2c_verified", "c12_qmi8610.olb", i2c_types),
        ("HOST_SPI4", "c12_spi4_verified", "c12_qmi8610_spi4.olb", spi_types),
    ]:
        report = LOG / folder
        rows = table(report / "c12_pins.tsv")
        check(len(rows) == 16, profile + " exactly 16 native pins")
        numbers = [int(row["number"]) for row in rows]
        check(sorted(numbers) == list(range(1, 17)), profile + " unique physical numbers 1..16; no EP17")
        by_number = {int(row["number"]): row for row in rows}
        spec_by_number = {pin["number"]: pin for pin in spec["profiles"][profile]["pins"]}
        for number in range(1, 17):
            row, pin = by_number[number], spec_by_number[number]
            check(row["name"] == names[number-1] == pin["display_name"], f"{profile} pin{number} name")
            check(int(row["type"]) == types[number-1] == pin["capture_enum_expected"], f"{profile} pin{number} electrical type")
            check(int(row["position"]) == number - 1 == pin["position"], f"{profile} pin{number} physical/position mapping")
            check(row["visible"] == row["numberVisible"] == "1", f"{profile} pin{number} visibility")
            check(int(row["global"]) == int(number in powers), f"{profile} pin{number} recorded raw POWER bit")
            check(int(row["noConnect"]) == int(number in {4, 5}), f"{profile} pin{number} NC policy")
            check([int(row[k]) for k in ("startX", "startY")] == pin["symbol_start"], f"{profile} pin{number} body endpoint")
            check([int(row[k]) for k in ("hotX", "hotY")] == pin["symbol_hotpoint"], f"{profile} pin{number} connection hotspot")
        props = {row["property"]: row["value"] for row in table(report / "c12_properties.tsv")}
        expected_props = {"Manufacturer": "QST", "Manufacturer Part Number": "QMI8610",
                          "PCB Footprint": spec["physical_footprint"],
                          "packagePCBFootprint": spec["physical_footprint"], "partValue": "QMI8610",
                          "Interface Profile": profile, "Symbol Revision": "C12_REV1",
                          "Source Revision": "13-52-14 Rev A, 2018-05-10",
                          "partPinNamesVisible": "1", "partPinNumbersVisible": "1"}
        for key, value in expected_props.items():
            check(props.get(key) == value, f"{profile} property {key}")
        vectors = table(report / "c12_vectors.tsv")
        expected_vectors = {("0", "0", "220", "0"), ("220", "0", "220", "180"),
                            ("220", "180", "0", "180"), ("0", "180", "0", "0")}
        check(len(vectors) == 4 and all(row["type"] == "LINE" for row in vectors)
              and {tuple(row[k] for k in ("startX", "startY", "endX", "endY")) for row in vectors} == expected_vectors,
              profile + " native four-line body")
        display = table(report / "c12_display_properties.tsv")
        check(len(display) == 2 and {(r["name"], r["x"], r["y"], r["displayType"]) for r in display}
              == {("Part Reference", "0", "-20", "1"), ("Value", "100", "200", "1")},
              profile + " native reference/value display properties")
        for path in [EXAMPLE / library, *sorted(report.glob("*"))]:
            artifacts.append({"path": str(path), "size": path.stat().st_size, "sha256": digest(path)})

    # Physical-library native readback from lesson 8 is an independent existing artifact.
    physical_path = ROOT / "examples" / "qmi8610" / "logs" / "reopen" / "pins.tsv"
    physical = {int(row["number"]): row for row in table(physical_path)}
    check(set(physical) == set(range(1, 17)), "B8 native footprint pin numbers match C12 physical set")
    for pin in spec["profiles"]["HOST_I2C"]["pins"]:
        actual = physical[pin["number"]]
        check([float(actual["x"]), float(actual["y"])] == pin["physical_footprint_xy_mm"],
              f"pin{pin['number']} existing physical footprint position")

    flags_path = LOG / "c12_power_flags_probe.tsv"
    flags = table(flags_path)
    final_flags = [row for row in flags if row["stage"] == "reopened"]
    check(len(final_flags) == 4 and {int(r["number"]) for r in final_flags} == powers
          and all((r["type"], r["visible"], r["rawGlobal"]) == ("7", "1", "1") for r in final_flags),
          "POWER flag probe reopened: type7 visible1 rawGlobal1 for all four pins")
    check(any(r["number"] == "15" and r["stage"] == "1_SetPinType_0" and r["rawGlobal"] == "0" for r in flags)
          and any(r["number"] == "15" and r["stage"] == "4_SetPinType_7" and r["rawGlobal"] == "1" for r in flags),
          "probe distinguishes type-derived rawGlobal from visibility")
    result = {"date_asia_shanghai": "2026-10-19", "review_method": "source-PDF visual review plus independent Python comparison; creator helper not imported",
              "source_visual_pages_reviewed_by_reviewer": [8, 9], "source_pdf_sha256": digest(source_path),
              "spec_sha256": digest(spec_path), "checks": len(checked), "errors": errors,
              "status": "PASS" if not errors else "FAIL", "artifacts": artifacts,
              "scope": "Verifies native saved/closed/reloaded database readback logs. Does not establish GUI rendering, placed-net connectivity, ERC results or hardware operation."}
    out = LOG / "c12_independent_review.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": result["checks"], "errors": errors, "report": str(out)}, ensure_ascii=True))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
