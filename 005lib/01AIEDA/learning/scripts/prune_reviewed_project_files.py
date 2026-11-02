"""Delete an explicit, reviewed file list; never walk links or recursively delete.

freeze records source hashes and a protected-file snapshot. apply requires that
plan's SHA256, verifies the whole retained metadata snapshot, then deletes only
the named unchanged files. This is permanent deletion, not an archive tool.
All task-specific paths and decisions belong in the project's request JSON.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat

CODE_SUFFIXES = {'.py', '.pyw', '.ps1', '.psm1', '.psd1', '.bat', '.cmd',
                '.tcl', '.il', '.ils', '.scr', '.sh', '.js', '.ts', '.vbs',
                '.md', '.rst', '.ipynb', '.c', '.h', '.cpp', '.cs', '.v', '.vhd'}


def disk(p):
    s = str(p)
    return Path('\\\\?\\' + s) if os.name == 'nt' and not s.startswith('\\\\?\\') else Path(s)


def digest(p):
    h = hashlib.sha256()
    with disk(p).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest().upper()


def read(p):
    regular(p)
    return json.loads(disk(p).read_text(encoding='utf-8-sig'))


def write_new(p, obj):
    directory(p.parent)
    with disk(p).open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')


def relative(s):
    assert isinstance(s, str) and s and '\\' not in s and ':' not in s, s
    q = PurePosixPath(s)
    assert not q.is_absolute() and '..' not in q.parts and str(q) == s, s
    return q


def path_for(root, rel):
    q = relative(rel)
    p = root.joinpath(*q.parts)
    assert p != root and p.is_relative_to(root), str(p)
    return p


def regular(p):
    for a in [*reversed(p.parents), p]:
        s = disk(a).lstat()
        assert not getattr(s, 'st_file_attributes', 0) & 0x400, 'Reparse point: ' + str(a)
        if a == p:
            assert stat.S_ISREG(s.st_mode), 'Not a regular file: ' + str(a)
        else:
            assert stat.S_ISDIR(s.st_mode), 'Not a directory: ' + str(a)
    assert os.path.normcase(str(p.resolve(strict=True))) == os.path.normcase(str(p)), str(p)
    return s


def directory(p):
    for a in [*reversed(p.parents), p]:
        s = disk(a).lstat()
        assert stat.S_ISDIR(s.st_mode), 'Not a directory: ' + str(a)
        assert not getattr(s, 'st_file_attributes', 0) & 0x400, 'Reparse directory: ' + str(a)
    assert os.path.normcase(str(p.resolve(strict=True))) == os.path.normcase(str(p)), str(p)


def snapshot(root, exclude):
    directory(root)
    directory(exclude)
    rows, links = {}, []
    stack = [root]
    while stack:
        d = stack.pop()
        with os.scandir(disk(d)) as entries:
            for e in entries:
                p = Path(str(e.path).removeprefix('\\\\?\\'))
                if p == exclude:
                    continue
                s = e.stat(follow_symlinks=False)
                rel = p.relative_to(root).as_posix()
                if getattr(s, 'st_file_attributes', 0) & 0x400:
                    links.append(rel)
                elif stat.S_ISDIR(s.st_mode):
                    stack.append(p)
                elif stat.S_ISREG(s.st_mode):
                    rows[rel] = {'size': s.st_size, 'mtime_ns': s.st_mtime_ns}
                else:
                    raise ValueError('Unsupported filesystem entry: ' + str(p))
    directory(root)
    directory(exclude)
    return rows, sorted(links)


def match_file(root, row):
    p = path_for(root, row['relative'])
    a = regular(p)
    assert (a.st_size, a.st_mtime_ns) == (row['size'], row['mtime_ns']), str(p)
    assert digest(p) == row['sha256'], 'SHA changed: ' + str(p)
    b = regular(p)
    assert (a.st_size, a.st_mtime_ns) == (b.st_size, b.st_mtime_ns), str(p)
    return p


def freeze(request_path, plan_path):
    req = read(request_path)
    root = Path(req['root']).absolute()
    task = path_for(root, req['task_relative'])
    directory(root)
    directory(task)
    assert plan_path.parent == task and task.is_dir(), 'Plan must be in task root'
    assert not plan_path.exists(), str(plan_path)
    baseline = read(Path(req['baseline_inventory']))
    expected = {x['relative'].replace('\\', '/'): {'size': x['size'], 'mtime_ns': x['mtime_ns']}
                for x in baseline['files']}
    actual, links = snapshot(root, task)
    assert actual == expected, 'Project changed since inventory; freeze a fresh inventory'
    assert not baseline.get('errors'), 'Inventory had errors'
    assert links == sorted(Path(x).relative_to(root).as_posix() for x in baseline['links'])
    selected = req['selected']
    keys = [relative(x['relative']).as_posix() for x in selected]
    assert len(keys) == len(set(k.casefold() for k in keys)), 'Duplicate/case-alias candidates'
    protected = set(req['protected_files'])
    protected_folded = {x.casefold() for x in protected}
    prefixes = req['protected_prefixes']
    allowed = req['allowed_prefixes']
    for rel in keys:
        assert rel in actual, 'Candidate not inventoried: ' + rel
        assert rel.casefold() not in protected_folded, 'Explicitly protected: ' + rel
        assert not any(rel.casefold() == x.casefold() or rel.casefold().startswith(x.casefold().rstrip('/') + '/') for x in prefixes), rel
        assert any(rel.casefold() == x.casefold() or rel.casefold().startswith(x.casefold().rstrip('/') + '/') for x in allowed), rel
        assert not rel.startswith(req['task_relative'].rstrip('/') + '/'), rel
        assert PurePosixPath(rel).suffix.casefold() not in CODE_SUFFIXES, 'Code/method protection: ' + rel
    chosen = set(keys)
    rows = []
    for index, item in enumerate(selected):
        rel = item['relative']
        p = path_for(root, rel)
        regular(p)
        row = {**item, **actual[rel], 'index': index, 'sha256': digest(p)}
        match_file(root, row)
        rows.append(row)
    strong = []
    for rel in sorted(protected):
        assert rel in actual and rel not in chosen, 'Protected file missing: ' + rel
        p = path_for(root, rel)
        regular(p)
        strong.append({'relative': rel, **actual[rel], 'sha256': digest(p)})
    assert snapshot(root, task) == (actual, links), 'Project changed during freeze'
    plan = {'schema': 'EXPLICIT_PERMANENT_PRUNE_V1', 'root': str(root),
            'task_relative': req['task_relative'], 'script_sha256': digest(Path(__file__).absolute()),
            'request_sha256': digest(request_path), 'baseline_sha256': digest(Path(req['baseline_inventory'])),
            'permanent_delete_no_new_archive': True, 'rows': rows, 'strong_protected': strong,
            'retained': {k: v for k, v in actual.items() if k not in chosen}, 'links': links,
            'protected_prefixes': prefixes, 'allowed_prefixes': allowed,
            'files_before': len(actual), 'bytes_before': sum(x['size'] for x in actual.values())}
    write_new(plan_path, plan)
    print(json.dumps({'plan': str(plan_path), 'sha256': digest(plan_path),
                      'selected_files': len(rows), 'selected_bytes': sum(x['size'] for x in rows),
                      'strong_protected': len(strong)}, ensure_ascii=False))


def apply(plan_path, approved_sha):
    regular(plan_path)
    assert digest(plan_path) == approved_sha.upper(), 'Plan SHA mismatch'
    plan = read(plan_path)
    assert plan['schema'] == 'EXPLICIT_PERMANENT_PRUNE_V1'
    assert digest(Path(__file__).absolute()) == plan['script_sha256'], 'Script changed'
    root = Path(plan['root'])
    task = path_for(root, plan['task_relative'])
    directory(root)
    directory(task)
    assert plan_path.parent == task
    receipt = task / 'APPLY_RECEIPT.json'
    journal = task / 'DELETE_JOURNAL.jsonl'
    assert not receipt.exists() and not journal.exists(), 'Already run or interrupted; reconcile manually'
    keys = {r['relative'] for r in plan['rows']}
    assert len(keys) == len(plan['rows'])
    assert not {x.casefold() for x in keys}.intersection(r['relative'].casefold() for r in plan['strong_protected'])
    before = dict(plan['retained'])
    for r in plan['rows']:
        rel = r['relative']
        assert PurePosixPath(rel).suffix.casefold() not in CODE_SUFFIXES, rel
        assert not any(rel.casefold() == x.casefold() or rel.casefold().startswith(x.casefold().rstrip('/') + '/') for x in plan['protected_prefixes']), rel
        assert any(rel.casefold() == x.casefold() or rel.casefold().startswith(x.casefold().rstrip('/') + '/') for x in plan['allowed_prefixes']), rel
        before[rel] = {'size': r['size'], 'mtime_ns': r['mtime_ns']}
    assert snapshot(root, task) == (before, plan['links']), 'Baseline changed before apply'
    for r in plan['strong_protected']:
        match_file(root, r)
    for r in plan['rows']:
        match_file(root, r)
    deleted = []
    directory(task)
    with journal.open('x', encoding='utf-8') as f:
        for start in range(0, len(plan['rows']), 100):
            batch = plan['rows'][start:start + 100]
            f.write(json.dumps({'event': 'INTENT', 'indices': [x['index'] for x in batch]}) + '\n')
            f.flush(); os.fsync(f.fileno())
            for r in batch:
                p = match_file(root, r)
                disk(p).unlink()
                deleted.append(r['relative'])
            f.write(json.dumps({'event': 'DONE', 'indices': [x['index'] for x in batch]}) + '\n')
            f.flush(); os.fsync(f.fileno())
            print('Deleted', len(deleted), '/', len(plan['rows']), flush=True)
    dirs = set()
    for rel in deleted:
        for d in path_for(root, rel).parents:
            if d == root:
                break
            dirs.add(d)
    removed_dirs = 0
    for d in sorted(dirs, key=lambda x: len(x.parts), reverse=True):
        if d == task or task.is_relative_to(d):
            continue
        try:
            s = disk(d).lstat()
            assert stat.S_ISDIR(s.st_mode) and not getattr(s, 'st_file_attributes', 0) & 0x400
            disk(d).rmdir()  # Empty directories only, never recursive.
            removed_dirs += 1
        except FileNotFoundError:
            pass
        except OSError as e:
            if e.errno not in (39, 66) and getattr(e, 'winerror', None) != 145:
                raise
    assert snapshot(root, task) == (plan['retained'], plan['links']), 'Retained metadata differs'
    for r in plan['strong_protected']:
        match_file(root, r)
    for rel in deleted:
        assert not disk(path_for(root, rel)).exists(), rel
    result = {'status': 'PASS_EXACT_DELETION_RETAINED_METADATA_AND_PROTECTED_SHA_UNCHANGED',
              'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'plan_sha256': approved_sha.upper(), 'permanent_delete_no_new_archive': True,
              'deleted_files': len(deleted), 'deleted_bytes': sum(r['size'] for r in plan['rows']),
              'empty_directories_removed': removed_dirs, 'files_before': plan['files_before'],
              'bytes_before': plan['bytes_before'], 'retained_files': len(plan['retained']),
              'retained_bytes': sum(r['size'] for r in plan['retained'].values()),
              'strong_protected_unchanged': len(plan['strong_protected']),
              'links_unchanged': plan['links'], 'journal_sha256': digest(journal)}
    write_new(receipt, result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__)
    sub = a.add_subparsers(dest='mode', required=True)
    f = sub.add_parser('freeze'); f.add_argument('--request', type=Path, required=True); f.add_argument('--plan', type=Path, required=True)
    f = sub.add_parser('apply'); f.add_argument('--plan', type=Path, required=True); f.add_argument('--plan-sha256', required=True)
    ns = a.parse_args()
    if ns.mode == 'freeze':
        freeze(ns.request.absolute(), ns.plan.absolute())
    else:
        apply(ns.plan.absolute(), ns.plan_sha256)
