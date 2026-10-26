"""Minimal immutable v2: exact old-land containment of the 25 thermal gaps."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 src=M/'public0010_source25_owner_probe_bundle13_v1';dest=M/'public0010_source25_owner_probe_bundle13_v2'
 assert not dest.exists();dest.mkdir()
 plan=dest/'SOURCE25_ACTUAL_UNCOVERED_STROKES.ilist';plan.write_bytes((src/plan.name).read_bytes())
 helper=dest/'public0010_source25_owner_probe_v2.il'
 text=(src/'public0010_source25_owner_probe_v1.il').read_text('utf-8')
 old=str(src/'SOURCE25_ACTUAL_UNCOVERED_STROKES.ilist').replace('\\','/')
 text=text.replace(old,str(plan).replace('\\','/'))
 before='pc25Frozen=cons(list(key row ps own cadr(relation) pc25Summary(inside)) pc25Frozen)'
 after='pc25Frozen=cons(list(key row ps own cadr(relation) pc25Summary(inside) pc25Copy(car(relation))) pc25Frozen)'
 assert text.count(before)==1;text=text.replace(before,after)
 before='let((f pf key row ps same missing relation outside oldDrc oldFill)'
 after='let((f pf key row ps same missing relation outside oldDrc oldFill missingOutsideOld missingInsideNew failures)'
 assert text.count(before)==1;text=text.replace(before,after)
 before='pc25PolyPort=outfile(strcat(dir "/SOURCE25_TARGET_ACTUAL_POLYGONS.jsonl"))'
 after=before+' failures=nil'
 assert text.count(before)==1;text=text.replace(before,after)
 before='outside=pc13RingOp(ps car(relation) \'ANDNOT)\n   pc25WritePolys(key "SOURCE_LINE_OUTSIDE_NEW_SAME_NET_PADS" outside)'
 after=before+'''
   missingOutsideOld=pc13RingOp(missing nth(6 item) 'ANDNOT)
   missingInsideNew=pc13RingOp(missing car(relation) 'AND)
   pc25WritePolys(key "EXACT_MISSING_THERMAL_CU_OUTSIDE_DETACHED_OLD_ACTUAL_PAD" missingOutsideOld)
   pc25WritePolys(key "EXACT_MISSING_THERMAL_CU_INTERSECTION_NEW_ACTUAL_PAD" missingInsideNew)
   when(missingOutsideOld || missingInsideNew failures=cons(key failures))'''
 assert text.count(before)==1;text=text.replace(before,after)
 before='"SOURCE_LINE_OUTSIDE_NEW_PADS" pc25Summary(outside)))'
 after='"SOURCE_LINE_OUTSIDE_NEW_PADS" pc25Summary(outside) "MISSING_THERMAL_OUTSIDE_OLD_ACTUAL_PAD" pc25Summary(missingOutsideOld) "MISSING_THERMAL_INSIDE_NEW_ACTUAL_PAD" pc25Summary(missingInsideNew)))'
 assert text.count(before)==1;text=text.replace(before,after)
 before='f=outfile(strcat(dir "/SOURCE25_PAD_RELATION_COMPLETE.txt"))'
 after='unless(null(failures) error("SOURCE25 bounded old-land thermal delta failed keys %L\\n" failures))\n  '+before
 assert text.count(before)==1;text=text.replace(before,after)
 text=text.replace('NO_CREATE_NO_SAVE_NO_APPROVAL_INFERRED\\n','ALL25_THERMAL_MISSING_OUTSIDE_OLD_ACTUAL_PAD_EMPTY\\nALL25_MISSING_INTERSECTION_NEW_ACTUAL_PAD_EMPTY\\nNO_CREATE_NO_SAVE_NO_UNBOUNDED_ACCEPTANCE\\n')
 helper.write_text(text,'utf-8')
 man=json.loads((src/'MANIFEST.json').read_text('utf-8'))
 man.update(schema='PUBLIC0010_SOURCE25_THERMAL_GAP_EXACT_OLD_LAND_CONTAINMENT_READONLY_V2',helper=str(helper),exact_missing_old_pad_containment_required=True,exact_missing_new_pad_intersection_empty_required=True)
 man['files'] += [dict(path=str(p),sha256=sha(p)) for p in [plan,helper,Path(__file__)]]
 (dest/'MANIFEST.json').write_text(json.dumps(man,indent=2)+'\n','utf-8')
 runner=M/'run_public0010_source25_owner_probe_v2.py'
 r=(M/'run_public0010_source25_owner_probe_v1.py').read_text('utf-8').replace('PUBLIC0010_SOURCE25_OWNER_AND_ACTUAL_PAD_CONTAINMENT_READONLY_V1',man['schema']).replace('PASS_READONLY_SOURCE25_OWNERSHIP_AND_PAD_RELATIONS','PASS_READONLY_SOURCE25_EXACT_OLD_LAND_THERMAL_DELTA')
 runner.write_text(r,'utf-8')
 print(json.dumps(dict(bundle=str(dest),helper_sha256=sha(helper),manifest_sha256=sha(dest/'MANIFEST.json'),runner=str(runner),runner_sha256=sha(runner)),indent=2))
if __name__=='__main__':main()
