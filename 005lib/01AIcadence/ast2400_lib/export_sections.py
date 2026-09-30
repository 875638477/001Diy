# -*- coding: utf-8 -*-
"""Split AST2400_pins.csv into per-section CSVs + Capture pin-add checklist."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "AST2400_pins.csv"
OUT_DIR = ROOT / "sections"
CAP_DIR = Path(r"D:\001DIY\005lib\01captureLib\AST2400")
SCRIPT_DIR = Path(r"D:\001DIY\005lib\01script_file\AST2400")


def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig")))
    by = defaultdict(list)
    for r in rows:
        by[r["PartSection"]].append(r)

    for d in (OUT_DIR, CAP_DIR, SCRIPT_DIR):
        d.mkdir(parents=True, exist_ok=True)

    fields = list(rows[0].keys())
    for part, items in by.items():
        for dest in (OUT_DIR, CAP_DIR / "sections", SCRIPT_DIR / "sections"):
            dest.mkdir(parents=True, exist_ok=True)
            path = dest / f"AST2400_{part}.csv"
            with path.open("w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerows(items)

    # master copies
    for dest in (CAP_DIR, SCRIPT_DIR):
        (dest / "AST2400_pins.csv").write_bytes(SRC.read_bytes())
        readme = ROOT / "AST2400_library_readme.md"
        if readme.exists():
            (dest / "AST2400_library_readme.md").write_bytes(readme.read_bytes())
        parts = ROOT / "AST2400_parts_summary.csv"
        if parts.exists():
            (dest / "AST2400_parts_summary.csv").write_bytes(parts.read_bytes())

    # Pin order checklist for Capture Part Editor (one file)
    checklist = CAP_DIR / "AST2400_pin_checklist.txt"
    lines = [
        "AST2400 Capture pin checklist",
        "Package: LFBGA-408 19x19mm",
        "Create heterogeneous part with 8 sections, then add pins below.",
        "",
    ]
    for part in sorted(by.keys()):
        lines.append(f"===== {part} ({len(by[part])} pins) =====")
        lines.append("Order\tBall\tName\tElectrical\tSide")
        for r in by[part]:
            lines.append(
                f"{r['Order']}\t{r['PinNumber']}\t{r['PinName']}\t{r['Electrical']}\t{r['Side']}"
            )
        lines.append("")
    checklist.write_text("\n".join(lines), encoding="utf-8")
    (SCRIPT_DIR / "AST2400_pin_checklist.txt").write_text("\n".join(lines), encoding="utf-8")

    print(f"OK sections={len(by)} -> {CAP_DIR}")
    print(f"also -> {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
