"""Render all reopened Capture A4 TSV pages as explicitly labelled diagrams.

These PNG/SVG previews are not screenshots and do not invoke Capture.  Part
bodies and pin starts come from the unchanged source symbol specification;
instance origins, absolute pin hotspots, wires, aliases and off-page objects
come from native database readback.  Font metrics and port silhouettes are
approximate.  No layout is moved or fitted to improve its appearance.
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


LEARNING = Path(__file__).resolve().parents[1]
RECORD_ROOT = LEARNING.parent.resolve()
DEFAULT_DATA = LEARNING / "staging" / "a4_review_20261019"
DEFAULT_SPEC = LEARNING / "examples" / "de_15_26_20261019" / "integrated_circuit.json"
DEFAULT_OUTPUT = LEARNING / "examples" / "de_15_26_20261019" / "a4_review" / "preview"


def record_path(path: Path) -> Path:
    path = path.resolve()
    if not path.is_relative_to(RECORD_ROOT):
        raise ValueError(f"Path must be inside {RECORD_ROOT}: {path}")
    return path


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def n(value: object) -> float:
    return float(value)


class Canvas:
    def __init__(self, width: float, height: float, scale: float, font_path: Path):
        self.scale = scale
        self.font_path = font_path
        self.image = Image.new("RGB", (round(width * scale), round(height * scale)), "#eef1f5")
        self.draw = ImageDraw.Draw(self.image)
        self.fonts = {}
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                    '<title>Capture native database readback diagram; not a Capture screenshot</title>',
                    '<desc>Unchanged model geometry at native instance coordinates. Font metrics, pin labels and port outlines are approximations.</desc>',
                    f'<rect width="{width}" height="{height}" fill="#eef1f5"/>']

    def xy(self, point):
        return tuple(v * self.scale for v in point)

    def rect(self, box, fill="white", color="#111827", width=1):
        left, top, right, bottom = box
        self.draw.rectangle(self.xy(box), fill=fill, outline=color, width=max(1, round(width * self.scale)))
        self.svg.append(f'<rect x="{left:g}" y="{top:g}" width="{right-left:g}" height="{bottom-top:g}" fill="{fill or "none"}" stroke="{color}" stroke-width="{width}"/>')

    def line(self, points, color="#111827", width=1):
        self.draw.line([self.xy(p) for p in points], fill=color, width=max(1, round(width * self.scale)))
        points_attr = " ".join(f"{x:g},{y:g}" for x, y in points)
        self.svg.append(f'<polyline points="{points_attr}" fill="none" stroke="{color}" stroke-width="{width}"/>')

    def polygon(self, points, fill="white", color="#b45309", width=1):
        self.draw.polygon([self.xy(p) for p in points], fill=fill)
        self.draw.line([self.xy(p) for p in points + [points[0]]], fill=color, width=max(1, round(width * self.scale)))
        points_attr = " ".join(f"{x:g},{y:g}" for x, y in points)
        self.svg.append(f'<polygon points="{points_attr}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>')

    def text(self, x, baseline, value, size=10, color="#111827", anchor="start"):
        pixel_size = max(1, round(size * self.scale))
        if pixel_size not in self.fonts:
            self.fonts[pixel_size] = ImageFont.truetype(str(self.font_path), pixel_size)
        pillow_anchor = {"start": "ls", "middle": "ms", "end": "rs"}[anchor]
        self.draw.text(self.xy((x, baseline)), str(value), fill=color, font=self.fonts[pixel_size], anchor=pillow_anchor)
        self.svg.append(f'<text x="{x:g}" y="{baseline:g}" font-family="Arial, sans-serif" font-size="{size:g}" text-anchor="{anchor}" fill="{color}">{html.escape(str(value))}</text>')

    def save(self, png_path: Path, svg_path: Path):
        self.image.save(png_path, optimize=True)
        svg_path.write_text("\n".join(self.svg + ["</svg>"]) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--scale", type=float, default=1.8)
    args = parser.parse_args()
    data, source, output = map(record_path, (args.data_dir, args.spec, args.output_dir))
    if args.scale <= 0 or args.scale > 5:
        parser.error("--scale must be greater than 0 and at most 5")
    font_path = Path("C:/Windows/Fonts/arial.ttf")
    if not font_path.is_file():
        parser.error("Arial font is unavailable; no font substitution is silently applied")
    tables = {key: read_tsv(data / f"after_{key}.tsv") for key in ("pages", "instances", "pins", "wires", "aliases", "offpages")}
    spec = json.loads(source.read_text(encoding="utf-8-sig"))
    components = {c["ref"]: c for c in spec["components"]}
    output.mkdir(parents=True, exist_ok=True)
    margin, top, foot = 22, 78, 62
    page_results = []
    native_port_anchors = sum(bool(p.get("name_x")) and bool(p.get("name_y")) for p in tables["offpages"])
    all_port_anchors_native = native_port_anchors == len(tables["offpages"])
    for page_index, page in enumerate(tables["pages"], 1):
        name = page["page"]
        if not name.replace("_", "").isalnum():
            raise ValueError(f"Unsafe page filename: {name!r}")
        width, height = n(page["draw_width"]), n(page["draw_height"])
        canvas = Canvas(width + margin * 2, height + top + foot, args.scale, font_path)
        canvas.text(margin, 25, f'{page_index:02d}  {name}  |  A4 {n(page["width_native"])/1000:g} x {n(page["height_native"])/1000:g} mm', 16)
        canvas.text(margin, 44, "DATABASE READBACK DIAGRAM - NOT A CAPTURE SCREENSHOT", 11, "#9a3412")
        canvas.text(margin, 61, "Actual geometry and port-name anchors; approximate Arial font and port outlines." if all_port_anchors_native else "Actual geometry coordinates; approximate Arial font, port outlines and port-name anchors.", 10, "#475569")
        canvas.rect((margin, top, margin + width, top + height), color="#94a3b8")

        def point(x, y):
            return (n(x) + margin, n(y) + top)

        page_tables = {key: [r for r in rows if r["page"] == name] for key, rows in tables.items() if key != "pages"}
        for row in page_tables["wires"]:
            canvas.line([point(row["x1"], row["y1"]), point(row["x2"], row["y2"])], "#18844c", 1.15)
        pins_by_ref = collections.defaultdict(list)
        for pin in page_tables["pins"]:
            pins_by_ref[pin["reference"]].append(pin)
        for instance in page_tables["instances"]:
            ref = instance["reference"]
            c = components[ref]
            model = spec["models"][c["model"]]
            x, y = n(instance["x"]), n(instance["y"])
            body_width, body_height = model["width"], model["height"]
            canvas.rect((*point(x, y), *point(x + body_width, y + body_height)), color="#111827", width=0.9)
            model_pins = {str(p["number"]): p for p in model["pins"]}
            for pin in pins_by_ref[ref]:
                mp = model_pins[pin["number"]]
                sx, sy = x + mp["start"][0], y + mp["start"][1]
                hx, hy = n(pin["hotx"]), n(pin["hoty"])
                canvas.line([point(sx, sy), point(hx, hy)], width=0.9)
                canvas.text(*point((sx + hx) / 2, hy - 3), pin["number"], 6.7, anchor="middle")
                if len(model["pins"]) > 2:
                    left_side = mp["side"] == "left"
                    tx = x + 6 if left_side else x + body_width - 6
                    canvas.text(*point(tx, sy + 3), pin["name"], 8, anchor="start" if left_side else "end")
                if pin["nc"].strip().lower() in {"1", "true", "yes"}:
                    canvas.line([point(hx - 3, hy - 3), point(hx + 3, hy + 3)], "#dc2626", 1.3)
                    canvas.line([point(hx - 3, hy + 3), point(hx + 3, hy - 3)], "#dc2626", 1.3)
            font_height = abs(n(instance.get("font_height") or -10)) or 10
            rx, ry = n(instance.get("reference_x") or x), n(instance.get("reference_y") or y - 20)
            vx, vy = n(instance.get("value_x") or x), n(instance.get("value_y") or y + body_height + 30)
            canvas.text(*point(rx, ry), ref, font_height)
            canvas.text(*point(vx, vy), instance["value"], font_height)
        for row in page_tables["offpages"]:
            left, pt, right, bottom = (n(row[k]) for k in ("left", "top", "right", "bottom"))
            hx, hy = n(row["hotx"]), n(row["hoty"])
            # Orange footprint uses the actual native bbox and hotspot.  The
            # detailed Capture library glyph is deliberately not reconstructed.
            hot_on_left = abs(hx - left) <= abs(hx - right)
            far_x = right if hot_on_left else left
            canvas.polygon([point(hx, hy), point(far_x, pt), point(far_x, bottom)], fill="#fff7ed")
            canvas.line([point(hx - 1.5, hy), point(hx + 1.5, hy)], "#b45309", 1.1)
            if row.get("name_x") not in {None, ""} and row.get("name_y") not in {None, ""}:
                if row.get("name_display_type") == "1":
                    canvas.text(*point(row["name_x"], row["name_y"]), row["name"], 10, "#1d4ed8")
            else:
                # Compatibility with older evidence that omitted the native
                # display-property anchor; this fallback is explicitly counted.
                canvas.text(*point(hx + 10 if hot_on_left else hx - 10, hy - 3), row["name"], 10, "#1d4ed8",
                            anchor="start" if hot_on_left else "end")
        for row in page_tables["aliases"]:
            size = abs(n(row["font_height"] or -10)) or 10
            canvas.text(*point(row["x"], n(row["y"]) - 3), row["name"], size, "#1d4ed8")
        canvas.text(margin, top + height + 23, f'{len(page_tables["instances"])} parts | {len(page_tables["pins"])} pins | {len(page_tables["wires"])} wires | {len(page_tables["offpages"])} off-page ports', 10, "#334155")
        canvas.text(margin, top + height + 43, "Source: reopened DE_INTEGRATED_A4.DSN TSVs. Electrical connectivity is checked separately in validation.json.", 9, "#475569")
        png, svg = output / f"{name}.png", output / f"{name}.svg"
        canvas.save(png, svg)
        page_results.append({"page": name, "png": str(png), "svg": str(svg), "pixel_dimensions": list(canvas.image.size),
                             "drawing_document_dimensions": [width, height], "counts": {k: len(v) for k, v in page_tables.items()}})

    thumb_width, cols, gap, header_height = 660, 3, 18, 88
    thumbs = []
    for result in page_results:
        with Image.open(result["png"]) as picture:
            thumb = picture.copy()
        thumb.thumbnail((thumb_width, 2000), Image.Resampling.LANCZOS)
        thumbs.append(thumb)
    tile_height = max(t.height for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_width + (cols + 1) * gap, header_height + rows * tile_height + (rows + 1) * gap), "#dce3eb")
    draw = ImageDraw.Draw(sheet)
    heading_font = ImageFont.truetype(str(font_path), 25)
    sub_font = ImageFont.truetype(str(font_path), 19)
    draw.text((gap, 13), f"All {len(thumbs)} A4 pages - database readback diagrams", fill="#0f172a", font=heading_font)
    draw.text((gap, 49), "Not Capture screenshots. Native coordinates preserved; fonts and port shapes approximated.", fill="#9a3412", font=sub_font)
    for index, thumb in enumerate(thumbs):
        sheet.paste(thumb, (gap + (index % cols) * (thumb_width + gap), header_height + gap + (index // cols) * (tile_height + gap)))
    contact = output / "contact_sheet.png"
    sheet.save(contact, optimize=True)
    input_paths = [source] + [data / f"after_{key}.tsv" for key in tables]
    metadata = {
        "schema": "capture_a4_native_readback_preview_v1", "page_count": len(page_results),
        "source": "Native database readback of DE_INTEGRATED_A4.DSN; not Capture GUI screenshots",
        "input_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths},
        "rendering": {"scale_pixels_per_document_unit": args.scale, "font_file": str(font_path),
                      "font_metrics_approximate": True, "port_outline_approximate": True,
                      "port_name_text_anchor_approximate": not all_port_anchors_native,
                      "native_port_name_anchors": native_port_anchors,
                      "estimated_port_name_anchors": len(tables["offpages"]) - native_port_anchors,
                      "layout_changed": False, "body_and_pin_start_source": "Unchanged integrated_circuit.json model geometry translated by native instance x/y",
                      "absolute_pin_hotspots_source": "Native after_pins.tsv", "zero_instance_display_bbox_used": False},
        "limitations": ["Pillow/Arial is not the Capture GDI renderer; this is geometry review evidence, not GUI visual acceptance.",
                        "Off-page triangle silhouettes are approximate; native bbox and electrical hotspot coordinates are preserved. Port-name anchors use native absolute Name display-property positions when present; older evidence falls back to a recorded estimate 10 units inward from the hotspot.",
                        "Reference/value anchors follow unchanged source properties unless optional explicit TSV anchors are present."],
        "pages": page_results, "contact_sheet": str(contact),
    }
    (output / "preview_manifest.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(page_results), "output_dir": str(output), "contact_sheet": str(contact)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
