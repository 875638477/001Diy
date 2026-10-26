"""Freeze the exact 25 source-stroke gaps; prepare read-only native ownership proof."""
from pathlib import Path
from decimal import Decimal
from collections import Counter
import hashlib, importlib.util, json, sys

M=Path(__file__).parent
G=Path('D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025')
sys.path.insert(0,str(G))
from sexpr import parse_many, Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def sk(v):
 if isinstance(v,Atom):return str(v)
 if isinstance(v,str):return json.dumps(v,ensure_ascii=True)
 if isinstance(v,Decimal):return str(v)
 if isinstance(v,list):return '('+' '.join(map(sk,v))+')'
 raise ValueError(type(v))
def main():
 bundle=M/'public0010_source25_owner_probe_bundle13_v1'
 if bundle.exists():raise ValueError('Fresh bundle required')
 coverage=M/'public0010_nil_route_stub_run13_v2_partial/FULL2068_SOURCE_OWN_NET_CU_COVERAGE.ilist'
 rows=parse_many(coverage.read_text('utf-8-sig'))
 assert len(rows)==2068 and all(len(r)==2 and len(r[1])==1 for r in rows)
 missing=[r[0] for r in rows if r[1][0]==Atom('nil')]
 assert len(missing)==25
 source=M/'public_brd_genfeed13/02_0010/0010.brd'
 target=M/'public0010_nil_route_stub_run13_v2_partial/PUB0010_PARTIAL_UNAPPROVED.brd'
 assert sha(source)=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898'
 assert sha(target)=='1ABA0FDC27DE553535CDE454840EA245CBEBB5FDC1392A0B07E0218D11CDE26A'
 bundle.mkdir()
 (bundle/'SOURCE25_ACTUAL_UNCOVERED_STROKES.ilist').write_text('\n'.join(map(sk,missing))+'\n','utf-8')
 helper=bundle/'public0010_source25_owner_probe_v1.il'
 helper.write_text((M/'public0010_source25_owner_probe_template_v1.il').read_text('utf-8').replace('__PLAN__',str(bundle/'SOURCE25_ACTUAL_UNCOVERED_STROKES.ilist').replace('\\','/')),'utf-8')
 base=json.loads((M/'public0010_nil_route_stub_bundle13_v2_partial/MANIFEST.json').read_text('utf-8-sig'))
 files={e['path']:e for e in base['files']}
 deps=[coverage,helper,bundle/'SOURCE25_ACTUAL_UNCOVERED_STROKES.ilist',M/'public0010_nil_route_stub_bundle13_v1/public0010_nil_route_stub_repair_v1.il',M/'public0010_source25_owner_probe_template_v1.il']
 for p in deps:files[str(p)]=dict(path=str(p),sha256=sha(p))
 manifest=dict(schema='PUBLIC0010_SOURCE25_OWNER_AND_ACTUAL_PAD_CONTAINMENT_READONLY_V1',source_board=str(source),source_sha256=sha(source),target_board=str(target),target_sha256=sha(target),source_units=['millimeters',4],helper=str(helper),entry_source='pub0010Source25Prepare',entry_target='pub0010Source25Target',source_marker='SOURCE25_OWNER_PREPARE_COMPLETE.txt',target_marker='SOURCE25_PAD_RELATION_COMPLETE.txt',files=list(files.values()),source_strokes=2068,prior_exact_missing=87,covered_original_strokes=2043,uncovered_source_strokes=25,uncovered_by_net=dict(Counter(r[1] for r in missing)),no_create=True,no_save=True)
 (bundle/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n','utf-8')
 print(json.dumps(dict(bundle=str(bundle),manifest_sha256=sha(bundle/'MANIFEST.json'),helper_sha256=sha(helper),uncovered_by_net=manifest['uncovered_by_net']),indent=2))
if __name__=='__main__':main()
