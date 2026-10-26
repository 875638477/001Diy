"""Add complete native guard coverage and immutable input hashes to ledger."""
from pathlib import Path
import ast,hashlib
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
s=(W/'review_native_material_ledger13_v2.py').read_text(encoding='utf-8')
s=s.replace('import argparse,collections,hashlib,json','import argparse,collections,csv,hashlib,json')
marker=" summary=collections.defaultdict(lambda:collections.defaultdict(list))"
assert marker in s
insert=r''' assert counts.get('GUARD_VERSION')==5,'Require final conservative native guard version5'
 guard_polys=[json.loads(x,parse_float=Decimal) for x in (n/'margin_validation_polygons.jsonl').read_text().splitlines()]
 with (n/'margin_validation_methods.tsv').open(newline='') as f:methods=list(csv.DictReader(f,delimiter='\t'))
 with (n/'cross_net_checks.tsv').open(newline='') as f:checks=list(csv.DictReader(f,delimiter='\t'))
 with (n/'actual_material_summary.tsv').open(newline='') as f:material_summary=list(csv.DictReader(f,delimiter='\t'))
 shape_summary=[x for x in material_summary if not x['key'].startswith('PC184_')]
 assert len(shape_summary)==11 and len({x['key'] for x in shape_summary})==11
 expected=collections.Counter(x['key'] for x in rows if x['side']=='ACTUAL_SHAPE_COPPER_ADDED')
 assert expected==collections.Counter({x['key']:int(x['added_polys']) for x in shape_summary if int(x['added_polys'])}), 'Native added pieces do not match native summary'
 assert collections.Counter(x['key'] for x in checks)==expected, 'Every addition must have direct and guard intersection checks'
 assert all(int(x['direct_intersections'])==int(x['margin_intersections'])==0 for x in checks)
 assert collections.Counter(x['key'] for x in methods)==expected, 'Every addition must have one recorded positive guard'
 method_counts=collections.Counter(x['method'] for x in methods)
 valid_methods={'NATIVE_EXPAND_0D01MIL','CONSERVATIVE_BBOX_0D03MIL_MIN_NATIVE_MARGIN_0D02MIL'}
 assert set(method_counts)<=valid_methods
 assert all(Decimal(x['input_native_area'])>0 and int(x['guard_polys'])>0 for x in methods)
 inputs=collections.Counter(x['key'] for x in guard_polys if x['side']=='POSITIVE_ADDED_COPPER_INPUT')
 assert inputs==expected
 expected_guard_counts=collections.Counter()
 for x in methods:expected_guard_counts[(x['key'],x['method'])]+=int(x['guard_polys'])
 assert collections.Counter((x['key'],x['side']) for x in guard_polys if x['side']!='POSITIVE_ADDED_COPPER_INPUT')==expected_guard_counts
 # Full shape+arc+hole content of every guarded input must be the exact
 # material difference output, not just equal areas or bounding boxes.
 canonical=lambda p:json.dumps(safe(p),sort_keys=True,separators=(',',':'))
 assert collections.Counter((x['key'],canonical(x['poly'])) for x in guard_polys if x['side']=='POSITIVE_ADDED_COPPER_INPUT')==collections.Counter((x['key'],canonical(x['poly'])) for x in rows if x['side']=='ACTUAL_SHAPE_COPPER_ADDED')
'''
s=s.replace(marker,insert+marker)
s=s.replace("additional_conservative_contact_margin_mil='0.01',", "additional_conservative_contact_margin_mil='0.01',guard_validation=dict(version=5,guarded_added_fragments=sum(expected.values()),methods=dict(method_counts),conservative_fallback='Native bbox rectangle expanded0.03mil, verified native margin>=0.02mil on every side and contains original fragment by exact native ANDNOT. This is a stricter other-net contact check, never an allowed difference envelope.'),")
s=s.replace("n/'cross_net_intersections.jsonl']", "n/'cross_net_intersections.jsonl',n/'margin_validation_polygons.jsonl',n/'margin_validation_methods.tsv',n/'launch_report.json']")
ast.parse(s)
out=W/'review_native_material_ledger13_v3.py'
assert not out.exists()
out.write_text(s,encoding='utf-8')
print(out)
print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
