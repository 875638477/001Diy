"""Keep the actual old-land-only FAIL and quantify its precise external thermal gaps."""
from pathlib import Path
from collections import Counter
from decimal import Decimal
import argparse,hashlib,json,sys
M=Path(__file__).parent
sys.path.insert(0,'D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025')
from sexpr import parse_many,Atom,attrs
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def plain(v):
 if isinstance(v,Atom):return {'native_atom':str(v)}
 if isinstance(v,Decimal):return str(v)
 if isinstance(v,list):return [plain(x) for x in v]
 return v
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--run',type=Path,required=True);a=ap.parse_args();r=a.run
 rec=json.loads((r/'RUN_RECEIPT.json').read_text('utf-8-sig'))
 assert rec['status']=='FAIL' and rec['no_create'] and rec['no_save'] and rec['public_unchanged'] and rec['source_and_partial_copies_unchanged']
 assert rec['source_sha256']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898' and rec['partial_sha256']=='1ABA0FDC27DE553535CDE454840EA245CBEBB5FDC1392A0B07E0218D11CDE26A'
 native=lambda p:parse_many(p.read_text('utf-8-sig'))
 source=native(r/'SOURCE25_ACTUAL_OWNER_CHAIN.ilist');lines=[x for x in source if len(x)==5]
 assert len(lines)==25 and set(int(x[0]) for x in lines)==set(range(1,26))
 thermal={}
 for line in lines:
  assert line[3]==Atom('nil')
  paths=[x for x in line[4] if x[1]=='path'];assert len(paths)==1
  p=paths[0];aa=attrs(p[4]);assert aa['thermal']==Atom('t') and aa['symbolEtch']==Atom('nil') and p[2]==Atom('nil')
  thermal[int(line[0])]=dict(objtype=p[1],thermal=True,symbolEtch=False,source_line_and_path_properties_nil=True)
 rows=native(r/'SOURCE25_TARGET_WHOLE_CU_RELATIONS.ilist');assert len(rows)==25
 summaries=[];total=Decimal(0);external=Decimal(0);expected=[]
 for row in rows:
  i=int(row[0]);assert row[2::2]==['OLD_SYMBOL_OWNERS','OLD_INTERSECTING_PIN_IDS','WHOLE_LINE','SOURCE_LINE_OUTSIDE_OLD_PADS','TARGET_MISSING_SOURCE_CU','SOURCE_LINE_OUTSIDE_NEW_PADS','MISSING_THERMAL_OUTSIDE_OLD_ACTUAL_PAD','MISSING_THERMAL_INSIDE_NEW_ACTUAL_PAD']
  assert row[3]==Atom('nil') and row[17][0]==0 and row[17][1]==0
  total+=row[11][1];external+=row[15][1]
  if row[15][0]>0:expected.append(i)
  summaries.append(dict(key=i,source=plain(row[1]),source_pin_identity=plain(row[5]),source_owner_thermal=thermal[i],all_missing_mm2=str(row[11][1]),missing_outside_old_actual_pad_mm2=str(row[15][1]),missing_outside_old_actual_pad_bbox=plain(row[15][2]),old_land_internal_missing_mm2=str(row[11][1]-row[15][1]),missing_intersection_new_actual_pad_polygons=0))
 assert expected==[1,2,4,5,7,8,9,10,11,13,14,15,16,17,18,19,20,21,23,24,25]
 report=dict(status='ACTUAL_OLD_LAND_ONLY_THERMAL_ACCEPTANCE_FAIL_PRESERVED_PRECISE_EXTERNAL_RESTORE_REQUIRED',source_board_sha256=rec['source_sha256'],partial_board_sha256=rec['partial_sha256'],actual_thermal_paths=25,symbol_owned_paths=0,actual_source_path_thermal_true=25,actual_source_path_symbolEtch_nil=25,actual_old_regular_pad_method='axlPolyFromDB(actual source pin ?layer ETCH/BOTTOM ?padType REGULAR ?holes t); actual world coordinates include native instance rotation and mirror; no bbox/rectangle reconstruction',old_pad_identities='All source endpoints are actual 1MM1X1MM0 pads on the 11 frozen 0603 refs; nearby pads are included only on positive native intersection, same typed net, actual pad polygons.',all_missing_mm2=str(total),missing_outside_old_actual_pad_mm2=str(external),old_pad_internal_canonical_land_change_mm2=str(total-external),external_restore_exact_keys=expected,all_missing_intersection_new_actual_pad_zero=True,do_not_restore_whole_old_land=True,restoration_requires_native_other_net_zero_and_created_source_poly_both_directions_exact=True,full915_exact_partitions_is_separate_existing_gate=True,no_create=True,no_save=True,rows=summaries,evidence=[dict(path=str(p),sha256=sha(p)) for p in [r/'RUN_RECEIPT.json',r/'SOURCE25_ACTUAL_OWNER_CHAIN.ilist',r/'SOURCE25_TARGET_WHOLE_CU_RELATIONS.ilist',r/'SOURCE25_ACTUAL_POLYGONS.jsonl',r/'SOURCE25_TARGET_ACTUAL_POLYGONS.jsonl']])
 out=r/'SOURCE25_THERMAL_EXTERNAL_CU_DIAGNOSTIC.json';out.write_text(json.dumps(report,indent=2)+'\n','utf-8')
 print(json.dumps(dict(report=str(out),sha256=sha(out),all_missing_mm2=str(total),external_mm2=str(external),oldland_internal_mm2=str(total-external)),indent=2))
if __name__=='__main__':main()
