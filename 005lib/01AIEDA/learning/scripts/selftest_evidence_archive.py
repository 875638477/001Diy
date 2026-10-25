"""Small synthetic fixtures only. Never reads a CAD design or deletes a source."""
from pathlib import Path
import argparse
import json
import sys
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence_archive as tool


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.output.absolute()
    if root.exists():
        raise FileExistsError('Selftest output must be new')
    root.mkdir(parents=True)
    source = root / 'source'; source.mkdir()
    (source / 'nested').mkdir()
    (source / 'nested' / 'space and unicode \u4e2d\u6587.bin').write_bytes(bytes(range(256)) * 16)
    (source / 'empty.txt').write_bytes(b'')
    names = ['nested/space and unicode \u4e2d\u6587.bin', 'empty.txt']
    selection = root / 'selection.json'
    selection.write_text(json.dumps(names), encoding='utf-8')
    before = {n: tool.digest(tool.member_path(source, n)) for n in names}
    archive = root / 'evidence.zip'
    checks = []
    result = tool.create(source, selection, archive)
    assert result['source_files_deleted'] == 0
    assert before == {n: tool.digest(tool.member_path(source, n)) for n in names}
    checks.append('archive preserves source bytes/timestamps and supports Unicode/empty members')
    manifest, _ = tool.verify(archive)
    assert manifest['member_count'] == 2
    checks.append('CRC and every embedded member SHA verified')
    destination = root / 'restored'
    tool.restore(archive, destination)
    assert before == {n: tool.digest(tool.member_path(destination, n)) for n in names}
    checks.append('restores exact bytes, paths and nanosecond timestamps into a fresh root')
    def rejected(call):
        try:
            call()
        except (ValueError, FileExistsError):
            return
        raise AssertionError('Unsafe operation was not rejected')
    rejected(lambda: tool.restore(archive, destination))
    rejected(lambda: tool.create(source, selection, archive))
    checks.append('existing output/archive rejected without overwrite')
    for name in ['../outside', '/absolute', 'sub/../bad', 'a\\b', 'C:/bad', 'nul.txt', 'x.']:
        rejected(lambda n=name: tool.member_path(source, n))
    checks.append('traversal, absolute, ADS/device and ambiguous Windows paths rejected')
    bad = root / 'tampered.zip'
    with zipfile.ZipFile(archive) as origin, zipfile.ZipFile(bad, 'x') as output:
        for name in origin.namelist():
            payload = origin.read(name)
            output.writestr(name, b'tampered but CRC-valid' if name == names[0] else payload)
    rejected(lambda: tool.verify(bad))
    checks.append('CRC-valid payload tampering fails SHA verification')
    selection.write_text(json.dumps([names[0], names[0]]), encoding='utf-8')
    rejected(lambda: tool.create(source, selection, root / 'duplicate.zip'))
    checks.append('duplicate selection rejected before archive creation')
    report = {'status': 'PASS_SYNTHETIC_EVIDENCE_ARCHIVE_FIXTURES', 'checks': checks,
              'CAD_started': False, 'project_files_read_or_written': False}
    (root / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
