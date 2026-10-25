"""Explicit optional Python module directories; never installs packages."""
import argparse
import os
import pathlib
import sys


def configure():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--python-module-dir', action='append', default=[])
    options, _ = parser.parse_known_args()
    roots = options.python_module_dir + [
        p for p in os.environ.get('CAPTURE_LAYOUT_PYTHON_MODULE_DIRS', '').split(os.pathsep) if p
    ]
    for path in reversed(roots):
        resolved = pathlib.Path(path).expanduser().resolve(strict=True)
        if not resolved.is_dir():
            raise ValueError('Python module directory is not a directory: ' + str(resolved))
        sys.path.insert(0, str(resolved))


def add_options(parser):
    parser.add_argument('--python-module-dir', action='append', default=[],
                        help='Directory containing Shapely/NumPy or optional PyMuPDF; repeat as needed')
