"""Render explicitly selected 1-based PDF pages for visual reading.

Example: python render_pdf_pages.py 229 230 231
Requires the already available pymupdf package.
"""

from pathlib import Path
import argparse
import pymupdf


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", type=int, nargs="+")
    args = parser.parse_args()
    source = next(Path(r"D:\005study").glob("*.pdf"))
    evidence = Path(__file__).resolve().parents[1] / "evidence"
    evidence.mkdir(exist_ok=True)
    with pymupdf.open(source) as doc:
        if any(p < 1 or p > len(doc) for p in args.pages):
            parser.error(f"page numbers must be between 1 and {len(doc)}")
        for page in args.pages:
            out = evidence / f"pdf_{page:03d}.png"
            doc[page - 1].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(str(out))
            print(out)


if __name__ == "__main__":
    main()
