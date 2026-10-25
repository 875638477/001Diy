"""Audit and inventory the C-stage deliverables without modifying CAD files."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib, json, re

root = Path(__file__).resolve().parents[2]
learning = root/'learning'
out = learning/'logs/capture_C_20261019/c_stage_manifest.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

final11 = learning/'examples/lesson11_capture/final'
assert sha(final11/'c11_basics.dsn') == sha(final11/'c11_basics_baseline.dsn'), 'restored baseline differs'
assert sha(final11/'c11_saved_move_marked.dsn') != sha(final11/'c11_basics.dsn'), 'moved file must differ'
for name in ('fresh_reopen_result.tcldict','saved_move_result.tcldict'):
    text = (learning/'logs/capture_C_20261019/c11_final'/name).read_text(encoding='utf-8-sig')
    assert text.startswith('code 0 result {PASS '), name
opj = final11/'c11_basics.opj'
opj_resources = []
for entry in re.findall(r'\(File "([^"]+)"',opj.read_text(encoding='utf-8')):
    path = (opj.parent/entry.replace('\\','/')).resolve()
    assert path.is_relative_to(root) and path.is_file(), entry
    opj_resources.append(str(path.relative_to(root)))

files=[]
patterns = ('scripts/c1[1-4]*','scripts/capture_request.py','scripts/c_stage_manifest.py','notes/lesson1[1-4]*',
            'notes/lessonC*','examples/lesson1[1-4]_capture/**/*',
            'logs/capture_C_20261019/**/*','logs/lesson13_capture_20261019/**/*',
            'logs/lesson14_capture_20261019/**/*','staging/capture_C_20261019/**/*')
selected=set()
for pattern in patterns:
    selected.update(p for p in learning.glob(pattern) if p.is_file())
selected.update((root/'EDA.md', root/'课程索引.md'))
selected.update(p for p in (root/'backups/before_capture_C_20261019').iterdir() if p.is_file())

lesson13=json.loads((learning/'logs/capture_C_20261019/c13_acceptance.json').read_text(encoding='utf-8-sig'))
assert lesson13['counts']['checks']==17 and lesson13['counts']['passed']==17
lesson14=json.loads((learning/'logs/lesson14_capture_20261019/validation.json').read_text(encoding='utf-8-sig'))
assert lesson14['status']=='passed' and not lesson14['errors']
assert len(lesson14['checks'])==81 and all(x['passed'] for x in lesson14['checks'])
assert len(lesson14['artifact_identity']['checked_files'])==8
for rel in ('logs/capture_C_20261019/c13_manifest.json','logs/lesson14_capture_20261019/artifact_manifest.json'):
    document=json.loads((learning/rel).read_text(encoding='utf-8-sig'))
    for entry in document['files']:
        p=learning/entry['path']
        assert p.is_file() and sha(p).lower()==entry['sha256'].lower(), ('native artifact changed',str(p))
for folder in (final11, learning/'examples/lesson14_capture/final'):
    assert not any(p.name.lower().endswith(('dsnlck','olblck')) for p in folder.rglob('*') if p.is_file()), 'Final directory has native lock'
for path in sorted(selected):
    if path==out or path.name.lower().endswith(('dsnlck','olblck')):
        continue
    assert path.resolve().is_relative_to(root), str(path)
    files.append(dict(path=str(path.relative_to(root)),size=path.stat().st_size,sha256=sha(path)))

broken=[]
notes=list((learning/'notes').glob('lesson1[1-4]*.md'))+list((learning/'notes').glob('lessonC*.md'))
for note in notes:
    for target in re.findall(r'\]\(([^)]+)\)',note.read_text(encoding='utf-8')):
        if '://' in target or target.startswith('#'): continue
        clean=target.strip('<>').split('#')[0]
        if clean and (note.parent/clean).resolve()!=out.resolve() and not (note.parent/clean).exists():
            broken.append(dict(note=str(note.relative_to(root)),target=target))
assert not broken, broken
report=dict(date=datetime.now(timezone(timedelta(hours=8))).isoformat(),
            scope='All self-created C-stage artifacts remain inside 01AIEDA; native files are read only by this audit',
            c11_baseline_restored_sha256=sha(final11/'c11_basics.dsn'),
            c11_native_checks='PASS; two independent-process checks recorded',
            c13_native_checks='17/17 PASS; v8 full RefDes and graph verified',
            c14_native_checks='81/81 PASS; 8 native artifact identities match delivered versions',
            opj_resources=opj_resources,opj_gui_open_verified=False,
            note_link_errors=broken,files=files)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(files=len(files),note_link_errors=len(broken),report=str(out)),ensure_ascii=True))
