"""Independently classify source25 gaps from read-only native owner/pad proofs."""
from pathlib import Path
from collections import Counter
from decimal import Decimal
import argparse,hashlib,json,sys
M=Path(__file__).parent
sys.path.insert(0,'D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025')
from sexpr import parse_many,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def native(p):return parse_many(p.read_text('utf-8-sig'))
def plain(v):
 if isinstance(v,Atom):return {'native_atom':str(v)}
 if isinstance(v,Decimal):return str(v)
 if isinstance(v,list):return [plain(x) for x in v]
 return v
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--run',type=Path,required=True);a=ap.parse_args();r=a.run
 receipt=json.loads((r/'RUN_RECEIPT.json').read_text('utf-8-sig'))
 assert receipt['status']=='PASS_READONLY_SOURCE25_OWNERSHIP_AND_PAD_RELATIONS' and receipt['public_unchanged'] and receipt['source_and_partial_copies_unchanged'] and receipt['no_create'] and receipt['no_save']
 assert receipt['source_sha256']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898'
 assert receipt['partial_sha256']=='1ABA0FDC27DE553535CDE454840EA245CBEBB5FDC1392A0B07E0218D11CDE26A'
 src=native(r/'SOURCE25_ACTUAL_OWNER_CHAIN.ilist');targets=native(r/'SOURCE25_TARGET_WHOLE_CU_RELATIONS.ilist')
 actual=[x for x in src if len(x)==5];old=[x for x in src if len(x)==3]
 assert len(old)==25 and len(targets)==25 and set(int(x[0]) for x in actual)==set(range(1,26))
 polys={}
 for name in ['SOURCE25_ACTUAL_POLYGONS.jsonl','SOURCE25_TARGET_ACTUAL_POLYGONS.jsonl']:
  for line in (r/name).read_text('utf-8').splitlines():
   p=json.loads(line,parse_float=Decimal);key=(p['key'],p['role']);polys.setdefault(key,[]).extend(p['polys'])
 review=[]
 for row in targets:
  i=int(row[0]);source=row[1]
  assert row[2::2]==['OLD_SYMBOL_OWNERS','OLD_INTERSECTING_PIN_IDS','WHOLE_LINE','SOURCE_LINE_OUTSIDE_OLD_PADS','TARGET_MISSING_SOURCE_CU','SOURCE_LINE_OUTSIDE_NEW_PADS']
  owned=row[3];old_outside=row[9];missing=row[11];source_outside_new=row[13]
  source_owned=bool(isinstance(owned,list) and owned)
  is_outside_old=int(old_outside[0])>0
  is_missing=int(missing[0])>0
  if not is_missing:classification='ACTUAL_SOURCE_NATIVE_CU_ALREADY_COVERED'
  elif source_owned and not is_outside_old:classification='SYMBOL_OWNED_WHOLE_SOURCE_CU_INSIDE_OLD_PAD_NEEDS_APPROVED_GEOMETRY_DELTA_BINDING'
  elif source_owned:classification='SYMBOL_OWNED_CU_EXTENDS_OUTSIDE_OLD_PAD_NEEDS_EXPLICIT_SCOPE_REVIEW'
  elif is_outside_old:classification='BOARD_ROUTE_SOURCE_CU_EXTENDS_OUTSIDE_OLD_PAD_RESTORATION_REVIEW_REQUIRED'
  else:classification='BOARD_ROUTE_WITHIN_OLD_PAD_BUT_OUTSIDE_NEW_TOTAL_CU_REVIEW_REQUIRED'
  review.append(dict(key=i,net=source[1],layer=source[2],source_line=plain(source),source_symbol_owners=plain(owned),classification=classification,source_whole_polygon_summary=plain(row[7]),source_outside_old_pad_union_summary=plain(old_outside),target_missing_source_cu_summary=plain(missing),source_outside_new_pad_union_summary=plain(source_outside_new),actual_source_object_records=[plain(x) for x in actual if int(x[0])==i]))
 report=dict(status='COMPLETE_READONLY_SOURCE25_FACTS_NO_AUTOMATIC_ACCEPTANCE_OR_RESTORE',source_sha256=receipt['source_sha256'],partial_sha256=receipt['partial_sha256'],counts_by_classification=dict(Counter(x['classification'] for x in review)),counts_by_net=dict(Counter(x['net'] for x in review)),full_915_partitions_already_preserved_but_not_a_copper_manufacturing_equivalence_proof=True,all1739_vias_source_exact=True,no_create=True,no_save=True,rows=review,evidence=[dict(path=str(p),sha256=sha(p)) for p in [r/'RUN_RECEIPT.json',r/'SOURCE25_ACTUAL_OWNER_CHAIN.ilist',r/'SOURCE25_TARGET_WHOLE_CU_RELATIONS.ilist',r/'SOURCE25_ACTUAL_POLYGONS.jsonl',r/'SOURCE25_TARGET_ACTUAL_POLYGONS.jsonl']])
 dest=r/'SOURCE25_OWNERSHIP_AND_PAD_FACTS_REVIEW.json';dest.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(dict(report=str(dest),sha256=sha(dest),classifications=report['counts_by_classification']),indent=2))
if __name__=='__main__':main()
