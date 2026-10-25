"""Inventory this A4 revision without rewriting historical course manifests."""
from pathlib import Path
import hashlib,json,re
from datetime import datetime,timezone

LEARNING=Path(__file__).resolve().parents[1]
RECORDS=LEARNING.parent
STAGE=LEARNING/'staging/a4_review_20261019'
A4=LEARNING/'examples/de_15_26_20261019/a4_review'
validation=json.loads((STAGE/'validation.json').read_text(encoding='utf-8'))
pst=json.loads((STAGE/'pst_compare.json').read_text(encoding='utf-8'))
assert validation['status']=='PASS' and validation['checks']['failed']==0
assert pst['failed']==0 and not pst['electricalChangesFromOriginalSnapshot']
documents=[RECORDS/'EDA.md',RECORDS/'课程索引.md',LEARNING/'notes/capture_page_defaults.md',
 LEARNING/'notes/capture_a4_review_20261019.md',LEARNING/'notes/lessonDE_15_26_20261019.md',
 LEARNING/'examples/de_15_26_20261019/native/README.md',A4/'README.md']
broken=[]
for doc in documents:
    for dest in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
        dest=dest.split('#',1)[0].strip('<>')
        if not dest or re.match(r'^[a-zA-Z]+://',dest): continue
        path=doc.parent/dest
        # This file is written after the links are checked.
        if path.resolve()==(STAGE/'a4_manifest.json').resolve(): continue
        if not path.exists(): broken.append({'document':str(doc),'target':dest})
assert not broken,broken
files=set(documents)
files.update(p for p in A4.rglob('*') if p.is_file())
files.update(LEARNING/'scripts'/name for name in ['capture_page_defaults.tcl','de_capture_helpers.tcl','de_capture_batch.tcl'])
files.update((LEARNING/'scripts').glob('capture_a4_*'))
for name in ['validation.json','pst_compare.json','pst_input_identity.json','layout_plan.json',
             'before_pages.tsv','before_pins.tsv','after_pages.tsv','after_instances.tsv','after_pins.tsv',
             'after_wires.tsv','after_aliases.tsv','after_offpages.tsv','a4_spec.json','a4_spec.tcl']:
    files.add(STAGE/name)
files.update((STAGE/'packaging/netlist').glob('pst*.dat'))
files.add(STAGE/'packaging_verified_process/launch.json')
entries=[{'path':p.relative_to(RECORDS).as_posix(),'bytes':p.stat().st_size,
          'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
report={'scope':'A4 revision only; historical manifests preserved',
 'createdUTC':datetime.now(timezone.utc).isoformat(),'pages':12,'components':80,'pins':272,'nets':69,'NC':6,
 'geometry_and_connectivity_checks':validation['checks'],'pst_checks':pst['checks'],
 'broken_document_links':broken,'original_user_file_unchanged':pst['sourceFileObservation']['currentlyIdentical'],
 'electrical_changes':pst['electricalChangesFromOriginalSnapshot'],
 'gui_display_print_and_ERC':'pending','files':entries}
(STAGE/'a4_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'files':len(entries),'broken_links':len(broken),'pages':12,'electrical_changes':0,'geometry_checks':validation['checks']['passed'],'pst_checks':pst['passed']}))
