"""Explicit-file evidence ZIP creation, CRC/SHA verification and safe restoration.

Never selects files by extension or deletes originals. --root and --selection
belong to the current project, not to the learning library. No CAD is started.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import uuid
import zipfile

SCHEMA = 'EXPLICIT_EVIDENCE_ARCHIVE_V1'
MANIFEST = '_EVIDENCE_MANIFEST.json'


def ordinary(path, directory=False):
    path = Path(os.path.abspath(path))
    for item in (path, *path.parents):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('Symlink/reparse path rejected: ' + str(item))
    info = path.stat()
    if not (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)):
        raise ValueError('Unexpected file type: ' + str(path))
    return info


def relative_name(value):
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError('Expected a nonempty POSIX relative filename')
    parts = value.split('/')
    if any(p in ('', '.', '..') or ':' in p for p in parts):
        raise ValueError('Unsafe relative path: ' + value)
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {f'{x}{i}' for x in ('COM', 'LPT') for i in range(1, 10)}
    if any(p.rstrip(' .') != p or p.split('.')[0].upper() in reserved or
           any(ord(c) < 32 or c in '<>"|?*' for c in p) for p in parts):
        raise ValueError('Nonportable Windows filename: ' + value)
    if value == MANIFEST:
        raise ValueError('Reserved manifest filename')
    return value


def member_path(root, value):
    relative_name(value)
    result = Path(os.path.abspath(root.joinpath(*value.split('/'))))
    if os.path.commonpath((str(root), str(result))).casefold() != str(root).casefold():
        raise ValueError('Member escaped root')
    return result


def digest(path):
    before = ordinary(path)
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    after = ordinary(path)
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('File changed during hashing: ' + str(path))
    return {'size_bytes': after.st_size, 'sha256': h.hexdigest().upper(),
            'mtime_ns': after.st_mtime_ns}


def same_bytes(a, b):
    return (a['size_bytes'], a['sha256']) == (b['size_bytes'], b['sha256'])


def validate_manifest(data):
    if data.get('schema') != SCHEMA or not isinstance(data.get('members'), list) or not data['members']:
        raise ValueError('Unknown or empty evidence manifest')
    seen = set()
    for row in data['members']:
        name = relative_name(row['relative_path'])
        if name.casefold() in seen:
            raise ValueError('Duplicate/case-colliding member: ' + name)
        seen.add(name.casefold())
        if not isinstance(row['size_bytes'], int) or row['size_bytes'] < 0:
            raise ValueError('Invalid member size')
        if not isinstance(row.get('mtime_ns'), int) or row['mtime_ns'] < 0:
            raise ValueError('Invalid member timestamp')
        value = row['sha256']
        if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789ABCDEF' for c in value):
            raise ValueError('Invalid member SHA256')
    if data.get('member_count') != len(seen) or data.get('raw_bytes') != sum(r['size_bytes'] for r in data['members']):
        raise ValueError('Manifest count/size totals differ')
    return data['members']


def verify(archive_path):
    before = digest(archive_path)
    with zipfile.ZipFile(archive_path) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        if len(names) != len(set(names)) or len(names) != len({n.casefold() for n in names}):
            raise ValueError('Duplicate/case-colliding ZIP entries')
        if MANIFEST not in names or archive.getinfo(MANIFEST).file_size > 16 * 1024 * 1024:
            raise ValueError('Missing or oversized embedded manifest')
        data = json.loads(archive.read(MANIFEST).decode('utf-8'))
        members = validate_manifest(data)
        if set(names) != {r['relative_path'] for r in members} | {MANIFEST}:
            raise ValueError('Unexpected, missing or directory ZIP member')
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC failure')
        for row in members:
            info = archive.getinfo(row['relative_path'])
            if info.file_size != row['size_bytes'] or (info.external_attr >> 16) & 0o170000 == stat.S_IFLNK:
                raise ValueError('Invalid ZIP member type/size')
            h = hashlib.sha256()
            with archive.open(info) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(chunk)
            if h.hexdigest().upper() != row['sha256']:
                raise ValueError('ZIP member SHA mismatch: ' + row['relative_path'])
    if not same_bytes(before, digest(archive_path)):
        raise ValueError('Archive changed during verification')
    return data, before


def create(root, selection, archive_path):
    ordinary(root, directory=True)
    ordinary(archive_path.parent, directory=True)
    if archive_path.exists():
        raise FileExistsError('Refusing existing archive')
    selected = json.loads(selection.read_text(encoding='utf-8-sig'))
    selected = selected.get('files') if isinstance(selected, dict) else selected
    if not isinstance(selected, list) or not selected:
        raise ValueError('Selection must be a nonempty list, or {"files": [...]}')
    members = []
    for name in selected:
        source = member_path(root, name)
        if source == archive_path:
            raise ValueError('Archive cannot select itself')
        members.append({'relative_path': name, **digest(source)})
    data = {'schema': SCHEMA, 'source_root': str(root), 'member_count': len(members),
            'raw_bytes': sum(r['size_bytes'] for r in members), 'members': members,
            'scope': 'Bytes, relative paths and mtime_ns; no ACL/ADS guarantee. Originals are never removed.'}
    validate_manifest(data)
    temp = archive_path.with_name(archive_path.name + '.part_' + uuid.uuid4().hex)
    try:
        with zipfile.ZipFile(temp, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as archive:
            for row in members:
                source = member_path(root, row['relative_path'])
                if not same_bytes(row, digest(source)):
                    raise ValueError('Source changed before archive')
                archive.write(source, row['relative_path'])
            archive.writestr(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
        verify(temp)
        for row in members:
            if not same_bytes(row, digest(member_path(root, row['relative_path']))):
                raise ValueError('Source changed during archive')
        # No-clobber publish: fails if another process created the output meanwhile.
        with archive_path.open('xb') as output, temp.open('rb') as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b''):
                output.write(chunk)
        verified, archive_identity = verify(archive_path)
        return {'status': 'PASS_ARCHIVE_ORIGINALS_RETAINED', 'member_count': len(verified['members']),
                'archive': str(archive_path), 'archive_identity': archive_identity, 'source_files_deleted': 0}
    finally:
        if temp.exists():
            temp.unlink()  # Only this invocation's exact generated temporary ZIP.


def restore(archive_path, destination):
    data, identity = verify(archive_path)
    if destination.exists():
        raise FileExistsError('Restore destination must be new; no existing files are overwritten')
    ordinary(destination.parent, directory=True)
    destination.mkdir()
    with zipfile.ZipFile(archive_path) as archive:
        for row in data['members']:
            target = member_path(destination, row['relative_path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            ordinary(target.parent, directory=True)
            with archive.open(row['relative_path']) as source, target.open('xb') as output:
                for chunk in iter(lambda: source.read(1024 * 1024), b''):
                    output.write(chunk)
            os.utime(target, ns=(row['mtime_ns'], row['mtime_ns']))
            if not same_bytes(row, digest(target)):
                raise ValueError('Restored member SHA mismatch')
    if not same_bytes(identity, digest(archive_path)):
        raise ValueError('Archive changed during restoration')
    return {'status': 'PASS_RESTORED_BYTES_AND_RELATIVE_PATHS', 'member_count': len(data['members']),
            'destination': str(destination), 'archive_identity': identity}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('create', 'verify', 'restore'))
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--root', type=Path)
    parser.add_argument('--selection', type=Path)
    parser.add_argument('--destination', type=Path)
    args = parser.parse_args()
    archive = Path(os.path.abspath(args.archive))
    if args.mode == 'create':
        if args.root is None or args.selection is None:
            parser.error('create requires --root and --selection')
        result = create(Path(os.path.abspath(args.root)), args.selection, archive)
    elif args.mode == 'restore':
        if args.destination is None:
            parser.error('restore requires --destination')
        result = restore(archive, Path(os.path.abspath(args.destination)))
    else:
        data, identity = verify(archive)
        result = {'status': 'PASS_ZIP_CRC_ALL_MEMBER_SHA', 'member_count': len(data['members']), 'archive_identity': identity}
    print(json.dumps(result, ensure_ascii=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status': 'FAIL', 'error': str(error)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
