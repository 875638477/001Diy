from pathlib import Path
import datetime
import hashlib
import json
import tkinter

ROOT = Path(r"D:\001DIY\005lib\01AIEDA\learning")
EXAMPLE = ROOT / "examples" / "lesson12_capture"
HELPER = ROOT / "scripts" / "c12_helpers.tcl"
EXAMPLE.mkdir(parents=True, exist_ok=True)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


source = read_json(ROOT / "examples/qmi8610/source/source.json")
physical = read_json(ROOT / "examples/qmi8610/qmi8610_spec.json")
publication = read_json(ROOT / "examples/qmi8610/publication.json")
assert sha(Path(source["path"])) == source["sha256"]
interpreter = tkinter.Tcl()
interpreter.eval(HELPER.read_text(encoding="utf-8"))

reasons = {
    1: "RESV3 must connect to board GND. PASSIVE is an explicit ERC choice; it is not NC.",
    2: "Analog supply in Table 2.",
    3: "Analog ground in Table 2.",
    4: "RESV2 is NC in Table 2. Keep pin visible and set NoConnect.",
    5: "RESV1 is NC in Table 2. Keep pin visible and set NoConnect.",
    6: "Master I2C serial data. BIDIRECTIONAL is an ERC inference from bus function.",
    7: "Master I2C serial clock. OUTPUT models master clock; clock stretching not certified.",
    8: "Digital/IO supply in Table 2.",
    9: "SA0 is input in host I2C; SDO is output in host four-wire SPI.",
    10: "CS input; high selects I2C mode. Internal 200k pull-up noted.",
    11: "INT2/DRDY output function. Open-drain versus push-pull is not inferred.",
    12: "INT1/CLKout interrupt/clock output function.",
    13: "SDA bidirectional in I2C; SDI input in four-wire SPI. Three-wire SDIO not covered.",
    14: "Host clock input SCL/SPC.",
    15: "Digital ground in Table 2.",
    16: "Reset input. No inversion dot inferred merely from assert wording.",
}
primary = {
    1: "RESV3", 2: "VDDa", 3: "GNDa", 4: "RESV2", 5: "RESV1", 6: "SDA2",
    7: "SCL2", 8: "VDDd", 9: "SA0", 10: "CS", 11: "INT2", 12: "INT1",
    13: "SDA", 14: "SCL", 15: "GNDd", 16: "RST",
}
type_codes = {"INPUT": 0, "BIDIRECTIONAL": 1, "OUTPUT": 2, "PASSIVE": 4, "POWER": 7}
profiles = {}
for mode in ("HOST_I2C", "HOST_SPI4"):
    pins = []
    for number, name, kind, nc, page in interpreter.call("::C12::spec_rows", mode):
        number, nc, page = int(number), int(nc), int(page)
        points = [int(v) for v in interpreter.call("::C12::pin_points", number)]
        footprint_pin = next(p for p in physical["pins"] if p["number"] == number)
        pins.append({
            "number": number, "position": number - 1, "source_primary_name": primary[number],
            "display_name": name, "electrical_type": kind, "capture_enum_expected": type_codes[kind],
            "electrical_type_basis": reasons[number], "source_pdf_page": page,
            "source_locator": "Table 2 Pin Definitions; Figure 4 top view on PDF8",
            "visible": True, "number_visible": True,
            "global": kind == "POWER", "raw_global_expected_after_native_save": kind == "POWER",
            "global_field_meaning": "Raw library metadata only; wired-net scope must be verified on placed instances.",
            "no_connect": bool(nc),
            "symbol_start": points[:2], "symbol_hotpoint": points[2:],
            "physical_footprint_number": number,
            "physical_footprint_pin_name_for_reference": footprint_pin["name"],
            "physical_footprint_xy_mm": [footprint_pin["x"], footprint_pin["y"]],
        })
    profiles[mode] = {"pins": pins}

artifact_state = []
for artifact in publication["artifacts"]:
    target = Path(artifact["target"])
    staged = Path(artifact["source"])
    staged_sha = sha(staged)
    assert staged_sha == artifact["sha256"]
    artifact_state.append({
        "B8_public_target": str(target), "public_target_exists_now": target.is_file(),
        "public_sha256_now": sha(target) if target.is_file() else None,
        "learning_artifact": str(staged), "learning_sha256_now": staged_sha,
        "learning_matches_B8": True, "B8_expected_sha256": artifact["sha256"],
    })

spec = {
    "date_asia_shanghai": "2026-10-19",
    "state": "source reviewed and helper prepared; Capture native execution pending parent",
    "part": "QMI8610", "package_name": "QMI8610_C12", "cell_name": "QMI8610_C12",
    "normal_part_name": "QMI8610_C12.Normal", "device_designator": "1",
    "default_profile": "HOST_I2C", "target_library": str(EXAMPLE / "c12_qmi8610.olb"),
    "source": source, "source_document": "13-52-14 Rev A, 2018-05-10",
    "source_visually_reviewed_pages": [8, 9, 14, 15],
    "physical_footprint": "qmi8610_lga16_3d3_p0d5",
    "physical_padstack": "qmi8610_smd061x032_m05_p100",
    "physical_pin_count": 16, "center_ep_pin17": False,
    "profiles": profiles,
    "visibility_policy": "All pins/numbers/names visible. Native POWER metadata GetIsGlobal=1 is recorded separately; no hidden/global net behavior inferred from this raw bit.",
    "electrical_model_boundary": "Types are engineering ERC classifications from function, not analog models or output transistor topology guarantees.",
    "voltage_domains": {
        "VDDa_recommended_V": [2.7, 3.3, 3.47], "VDDd_recommended_V": [1.62, 1.8, 1.98],
        "source_pdf_page": 15, "absolute_max_VDDd_V": 2.05, "absolute_max_source_pdf_page": 14,
        "note": "Do not treat VDDd as a 3.3V rail because VDDa is 3.3V typical; no powered hardware test performed.",
    },
    "physical_artifact_current_state": artifact_state,
    "helper": {
        "path": str(HELPER), "sha256": sha(HELPER), "loaded_in_plain_tcl_for_syntax": True,
        "native_api_invoked_by_this_agent": False, "auto_exec_on_source": False,
        "output_guard_root": str(ROOT),
    },
    "native_acceptance_pending": [
        "Create library/package/cell/part/pins and physical numbering inside Capture",
        "SavePackageAll/SaveLib, remove and reload library",
        "Read back 16 unique numbers, names, profile types and visibility/noConnect flags",
        "Read back body vectors, properties and display properties",
        "Independent-process reopen when parent can arrange it",
        "C14 instance mapping and library update propagation",
    ],
}
(EXAMPLE / "qmi8610_pin_spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
checks = {
    "helper": str(HELPER), "procedure_count": len(interpreter.call("info", "procs", "::C12::*")),
    "HOST_I2C_rows": 16, "HOST_SPI4_rows": 16, "learning_artifacts_match_B8": True,
    "source_pdf_matches_B8": True, "native_api_executed": False,
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
}
(ROOT / "staging/capture_C_20261019/c12_plain_tcl_checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
print("Wrote pin spec. Source PDF and learning PAD/DRA/PSM match B8. Public targets checked separately.")
