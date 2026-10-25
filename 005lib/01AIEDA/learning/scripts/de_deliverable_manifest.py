"""Final read-only CAD identity and record-link audit; inventory local artifacts."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json,re,shutil
root=Path(__file__).resolve().parents[2];learning=root/'learning'
base=learning/'examples/de_15_26_20261019';logs=learning/'logs/de_15_26_20261019'
out=logs/'deliverable_manifest.json';stage=learning/'staging/de_15_26_20261019'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
spec=read(base/'integrated_circuit.json')
used=sorted({spec['models'][c['model']]['footprint'] for c in spec['components']})
assert len(used)==18
for name in used:assert (base/'library'/(name+'.psm')).is_file(),name
(base/'used_footprints.json').write_text(json.dumps(dict(count=len(used),footprints=used,prepared_and_native_verified_count=19,unused_verified_candidate='do-214aa_smb',note='The historical selected_footprints file lists the prepared19; this file lists the actual18 used by80components.'),ensure_ascii=False,indent=2),encoding='utf-8')

# Preserve the backend-endpoint manifest, then refresh only changed document data.
# A native CAD/output hash difference is an error, never silently accepted.
manifest_path=base/'native_backend_manifest.json';backend=read(manifest_path)
old=stage/'native_backend_manifest_before_final_record_sync.json'
if not old.exists():shutil.copy2(manifest_path,old)
refreshed=[]
critical={'.dsn','.olb','.psm','.dra','.pad','.brd','.dat','.swp'}
for entry in backend['files']:
    p=base/entry['path'];assert p.is_file(),str(p)
    current=sha(p)
    if current.lower()!=entry['sha256'].lower():
        assert p.suffix.lower() not in critical,('Native evidence changed',str(p))
        refreshed.append(dict(path=entry['path'],old_sha256=entry['sha256'],new_sha256=current))
        entry.update(bytes=p.stat().st_size,sha256=current)
if refreshed:
    backend['post_native_record_sync']='Current project budget150mA/0..40C and source hashes updated after document-only review. No native CAD files changed; old endpoint manifest preserved in staging.'
    backend['post_native_record_changes']=backend.get('post_native_record_changes',[])+refreshed
    manifest_path.write_text(json.dumps(backend,ensure_ascii=False,indent=2),encoding='utf-8')

flow=read(base/'native_flow_final/flow_result.json')
assert flow['status']=='PASS_NATIVE_EXPORT_IMPORT_ECO_REVERSE_COMPARE'
assert flow['independentChecks']==1578
assert len(flow['nativeProcesses'])==8 and all(p['exitCode']==0 and p['completed'] for p in flow['nativeProcesses'])
for name,digest in flow['originalDsnHashesUnchanged'].items():assert sha(Path(name))==digest
for entry in flow['files']:assert sha(Path(entry['path']))==entry['sha256']
acceptance=read(logs/'native_acceptance.json');assert acceptance['status']=='PASS' and acceptance['checks']==acceptance['passed']==1519
mcu=read(logs/'mcu_native_review.json');assert mcu['pass'] and mcu['check_count']==53
power=read(logs/'power_native_review.json');assert power['checked']==power['passed']==1577
assert spec['constraints']['V3V3_load_max_A']==.15 and spec['constraints']['ambient_C']==[0,40]

notes=[learning/'notes'/n for n in ('lessonDE_15_26_20261019.md','lessonDE_mcu_15_19_20261019.md','lessonDE_power_interfaces_20_25_20261019.md','lesson26_native_backend_20261019.md')]
note_texts=[(p,p.read_text(encoding='utf-8')) for p in notes]
eda=root/'EDA.md';index=root/'课程索引.md'
note_texts.append((eda,eda.read_text(encoding='utf-8').split('## 26. D与E',1)[1]))
idx=index.read_text(encoding='utf-8');note_texts.append((index,idx.split('### D/E.',1)[1].split('### F.',1)[0]))
broken=[]
for path,text in note_texts:
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if '://' in link or link.startswith('#'):continue
        target=(path.parent/link.strip('<>').split('#')[0]).resolve()
        if target==out.resolve():continue
        if not target.exists():broken.append(dict(file=str(path),target=link))
assert not broken,broken
opj_resources=[]
for project in (base/'native').glob('*.opj'):
    for ref in re.findall(r'\(File "([^"]+)"',project.read_text(encoding='utf-8')):
        target=(project.parent/ref).resolve();assert target.is_relative_to(root) and target.is_file()
        opj_resources.append(str(target.relative_to(root)))

files=set(notes+[eda,index])
for folder in ('examples/de_15_26_20261019','logs/de_15_26_20261019','staging/de_15_26_20261019','sources/de_15_26_20261019'):
    files.update(p for p in (learning/folder).rglob('*') if p.is_file())
files.update((learning/'scripts').glob('de_*'))
files.update(p for p in (root/'backups/before_DE_15_26_20261019').iterdir() if p.is_file())
inventory=[]
for path in sorted(files):
    if path==out or path.name.lower().endswith(('dsnlck','olblck','brdlck')):continue
    assert path.resolve().is_relative_to(root)
    inventory.append(dict(path=str(path.relative_to(root)),bytes=path.stat().st_size,sha256=sha(path)))
report=dict(date=datetime.now(timezone(timedelta(hours=8))).isoformat(),scope='All self-created learning artifacts under01AIEDA. CAD files were only read by this audit.',
    result='PASS_WITH_EXPLICIT_GUI_AND_HARDWARE_PENDING',native=dict(components=80,pins=272,connected_pins=266,nets=69,NC=6,used_footprints=18,prepared_native_verified_footprints=19),
    separate_checks=dict(native_readback_custom_rules=1519,MCU_review=53,power_interface_review=1577,native_PST_BRD_ECO=1578,footprint_validation=717),
    check_counts_overlap_not_additive=True,broken_note_links=broken,opj_resources=opj_resources,OPJ_GUI_open_verified=False,
    pending=['Capture GUI fullERC and ApplySWP','GUI visual schematic review','Hardware/electrical/compliance tests','Production PCB placement/routing/stackup/manufacturing release'],files=inventory)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(result=report['result'],files=len(inventory),broken_links=len(broken),native=report['native'],report=str(out)),ensure_ascii=True))
